"""Candidate-only refresh of the currently implemented official IMD source.

Usage: python pipeline/refresh.py --scope all --as-of 2026-09-24T12:00:00+05:30
No approved data, publication assets, deployment or shared state are changed.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Callable
from zoneinfo import ZoneInfo

# Support both ``python pipeline/refresh.py`` (the pnpm script) and module use.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.sources import imd_cumulative as imd


ROOT = Path(__file__).resolve().parents[1]
SCOPES = {"all", "imd"}


def parse_as_of(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise imd.SourceError("--as-of must be an ISO timestamp with timezone") from exc
    if parsed.tzinfo is None:
        raise imd.SourceError("--as-of must include a timezone")
    return parsed


def _read_previous(root: Path) -> tuple[Path | None, dict | None]:
    directory = root / "data/candidates/imd"
    paths = [p for p in directory.glob("*.json") if not p.name.endswith(".diff.json")]
    if not paths:
        return None, None
    # Candidate filenames begin with page date and end with retrieval time.
    # Read every candidate's own retrieval clock to avoid mtime dependence.
    candidates = []
    for path in paths:
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
            if content["candidate_type"] != "imd_cumulative_district_rainfall":
                raise ValueError("wrong candidate type")
            retrieved = datetime.fromisoformat(content["source"]["retrieved_at"].replace("Z", "+00:00"))
            if retrieved.tzinfo is None:
                raise ValueError("retrieval timestamp has no timezone")
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise imd.SourceError(f"invalid previous candidate {path}: {exc}") from exc
        candidates.append((retrieved, path, content))
    _, path, content = max(candidates, key=lambda item: (item[0], str(item[1])))
    return path, content


def _attempt_path(root: Path, as_of: datetime, checked_at: str, suffix: str) -> Path:
    as_of_slug = as_of.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    checked_slug = re.sub(r"[^0-9]", "", checked_at)
    return root / "data/candidates/refresh/attempts" / f"{as_of_slug}-{checked_slug}-{suffix}.json"


def refresh(
    root: Path,
    *,
    scope: str,
    as_of: datetime,
    fetcher: Callable[[], tuple[bytes, dict]] = imd.fetch,
) -> tuple[Path, dict]:
    """Fetch, validate, diff and record one candidate-only check.

    A repeated identical source reuses the existing candidate. Every check
    has its own immutable attempt record so retrieval clocks remain honest.
    """
    if scope not in SCOPES:
        raise imd.SourceError(f"unsupported scope {scope!r}; supported: all, imd")
    if as_of.tzinfo is None:
        raise imd.SourceError("as_of must include a timezone")
    previous_path, previous = _read_previous(root)
    body, metadata = fetcher()
    if not isinstance(body, bytes) or not isinstance(metadata, dict):
        raise imd.SourceError("source fetch did not return bytes and metadata")
    if len(body) > imd.MAX_BYTES:
        raise imd.SourceError("IMD response exceeds byte limit")
    source_hash = hashlib.sha256(body).hexdigest()
    if metadata.get("source_sha256") != source_hash:
        raise imd.SourceError("source hash mismatch")
    try:
        retrieved = datetime.fromisoformat(metadata["retrieved_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError) as exc:
        raise imd.SourceError("missing or invalid retrieval timestamp") from exc
    if retrieved.tzinfo is None:
        raise imd.SourceError("retrieval timestamp must include a timezone")
    candidate = imd.parse(body, metadata)
    page_end = datetime.fromisoformat(candidate["page_period"]["displayed_end_date"]).date()
    # A past evaluation timestamp cannot justify a later observed page date.
    if page_end > as_of.astimezone(ZoneInfo("Asia/Kolkata")).date():
        raise imd.SourceError("source observation date is after --as-of date in India")
    if previous is None:
        diff = {
            "baseline": True,
            "observation_changed": True,
            "added_ids": [row["geography_id"] for row in candidate["rows"]],
            "removed_ids": [],
            "changed_rows": [],
            "source_bytes_changed": True,
            "page_period_changed": True,
            "previous_sha256": None,
            "current_sha256": source_hash,
        }
    else:
        diff = imd.semantic_diff(previous, candidate)
        diff["baseline"] = False
    # Keep exact response bytes even when the parsed observation is unchanged.
    # Older candidates without a raw-path reference get one metadata repair
    # candidate; later identical checks reuse it.
    raw_path = imd.save_raw_snapshot(root, body)
    raw_relative = str(raw_path.relative_to(root))
    same_snapshot = (previous is not None and not diff["observation_changed"]
                     and not diff["source_bytes_changed"]
                     and previous["source"].get("raw_snapshot_path") == raw_relative
                     and previous["source"].get("raw_snapshot_sha256") == source_hash)
    if same_snapshot:
        candidate_path = previous_path
    else:
        candidate_path = imd.save_candidate(root, body, metadata, candidate)
    result = {
        "kind": "candidate_refresh_check",
        "status": "no_change" if same_snapshot else "candidate_created",
        "scope_requested": scope,
        "sources_checked": ["imd_cumulative_district_rainfall"],
        "sources_not_automated": ["other editorial and statistical sources"] if scope == "all" else [],
        "as_of": as_of.isoformat(),
        "checked_at": metadata["retrieved_at"],
        "source_url": imd.SOURCE_URL,
        "source_sha256": source_hash,
        "raw_snapshot_path": raw_relative,
        "raw_snapshot_sha256": source_hash,
        "source_observation_period": candidate["page_period"],
        "source_publication_time": candidate["source_publication_time"],
        "candidate_path": str(candidate_path.relative_to(root)),
        "previous_candidate_path": str(previous_path.relative_to(root)) if previous_path else None,
        "candidate_review_status": "candidate_unapproved",
        "diff": diff,
        "approval_required": True,
        "deployment_performed": False,
    }
    report_path = _attempt_path(root, as_of, metadata["retrieved_at"], source_hash[:16])
    imd._write_new(report_path, (json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return report_path, result


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if args and args[0] == "--":
        args.pop(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", default="all", help="all or imd")
    parser.add_argument("--as-of", required=True, help="fixed evaluation ISO timestamp with timezone")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parsed = parser.parse_args(args)
    try:
        as_of = parse_as_of(parsed.as_of)
        report_path, result = refresh(parsed.root, scope=parsed.scope, as_of=as_of)
    except (OSError, imd.SourceError) as exc:
        # Log failure separately. No candidate or approved data is replaced.
        checked_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        try:
            as_of = parse_as_of(parsed.as_of)
            failure = {"kind": "candidate_refresh_check", "status": "failed",
                       "scope_requested": parsed.scope, "as_of": as_of.isoformat(),
                       "checked_at": checked_at, "error": str(exc)[:500],
                       "approval_required": True, "deployment_performed": False}
            suffix = hashlib.sha256(str(exc).encode()).hexdigest()[:16]
            path = _attempt_path(parsed.root, as_of, checked_at, suffix)
            imd._write_new(path, (json.dumps(failure, indent=2, sort_keys=True) + "\n").encode())
        except (OSError, imd.SourceError):
            pass
        print(f"refresh failed: {exc}", file=sys.stderr)
        return 1
    print(f"{result['status']}: {result['candidate_path']}")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
