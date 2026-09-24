"""Candidate-only adapter for IMD's cumulative district rainfall map.

The source embeds a JSON ``dataProvider.areas`` array in an HTML page. No
source JavaScript or HTML is executed. Output uses IMD's own district IDs;
these are not silently joined to LGD administrative boundaries.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SOURCE_URL = "https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C"
MAX_BYTES = 2_000_000
TIMEOUT_SECONDS = 15
AREA_MARKER = re.compile(r'"dataProvider"\s*:\s*\{[^{}]{0,500}?"areas"\s*:\s*(\[)', re.S)
START_LABEL = re.compile(r'Cumulative\s*\(\s*From\s+(\d{2}-\d{2}-\d{4})\s*\)', re.I)
END_LABEL = re.compile(r'Daily\s*\(\s*(\d{2}-\d{2}-\d{4})\s*\)', re.I)
TOOLTIP = re.compile(
    r'Date\s*:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*'
    r'Departure\s*:\s*([^|]+)\s*\|\s*'
    r'Actual\s*:\s*([^|]+)\s*\|\s*'
    r'Normal\s*:\s*([^|]+)', re.I
)
NUMBER = re.compile(r'(?:0|[1-9]\d*)(?:\.\d+)?')
PERCENT = re.compile(r'-?\d+(?:\.\d+)?%')


class SourceError(ValueError):
    """Source content is unsafe, incomplete or outside this adapter's contract."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise SourceError(f"IMD source redirected (HTTP {code}); refusing new URL")


def fetch() -> tuple[bytes, dict]:
    """Fetch only the exact official URL, with a size, time and redirect bound."""
    parts = urlsplit(SOURCE_URL)
    if (parts.scheme, parts.hostname, parts.path, parts.query) != (
        "https", "mausam.imd.gov.in", "/responsive/rainfallinformation.php", "msg=C"
    ):
        raise SourceError("source URL is outside the approved IMD endpoint")
    request = Request(SOURCE_URL, headers={
        "User-Agent": "IndiaWaterWatch/0.1 (source audit; static publication)",
        "Accept": "text/html",
    })
    with build_opener(NoRedirect()).open(request, timeout=TIMEOUT_SECONDS) as response:
        if response.status != 200:
            raise SourceError(f"IMD returned HTTP {response.status}")
        content_type = response.headers.get("Content-Type", "").lower()
        if not content_type.startswith("text/html"):
            raise SourceError(f"unexpected content type: {content_type}")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise SourceError("IMD response exceeds byte limit")
        metadata = {
            "source_url": SOURCE_URL,
            "retrieved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "http_status": response.status,
            "content_type": content_type,
            "response_bytes": len(body),
            "source_sha256": hashlib.sha256(body).hexdigest(),
            "http_last_modified": response.headers.get("Last-Modified"),
            "http_date": response.headers.get("Date"),
        }
    return body, metadata


def _parse_date(value: str, fmt: str) -> str:
    try:
        return datetime.strptime(value, fmt).date().isoformat()
    except ValueError as exc:
        raise SourceError(f"invalid source date: {value}") from exc


def _decimal(value: str, unit: str) -> float | None:
    value = value.strip()
    if value.lower() in {"no data", "no data mm", "n/a", "na"}:
        return None
    if unit == "mm":
        if not value.endswith(" mm"):
            raise SourceError(f"expected rainfall in mm: {value!r}")
        value = value[:-3].strip()
        expression = NUMBER
    else:
        expression = PERCENT
    if not expression.fullmatch(value):
        raise SourceError(f"invalid {unit} value: {value!r}")
    try:
        result = Decimal(value.rstrip("%"))
    except InvalidOperation as exc:
        raise SourceError(f"invalid numeric value: {value!r}") from exc
    if unit == "mm" and result < 0:
        raise SourceError("negative rainfall")
    return float(result)


def _tooltip_fields(value: str) -> tuple[str, str, str, str]:
    # IMD uses </br> separators in its HTML fragment. Strip every other tag.
    value = re.sub(r"<\s*/?br\s*/?\s*>", " | ", value, flags=re.I)
    value = unescape(re.sub(r"<[^>]*>", "", value))
    match = TOOLTIP.search(value)
    if not match:
        raise SourceError("district tooltip lacks date/departure/actual/normal")
    return tuple(part.strip() for part in match.groups())


def parse(body: bytes, metadata: dict) -> dict:
    """Strictly parse a candidate; fail closed on changed source structure."""
    source_hash = hashlib.sha256(body).hexdigest()
    if metadata.get("source_sha256") != source_hash:
        raise SourceError("source hash mismatch before parsing")
    metadata = {**metadata,
                "raw_snapshot_path": f"data/raw/imd/{source_hash}.html",
                "raw_snapshot_sha256": source_hash}
    try:
        page = body.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise SourceError("source is not valid UTF-8") from exc
    start_match = START_LABEL.search(page)
    end_match = END_LABEL.search(page)
    area_match = AREA_MARKER.search(page)
    if not (start_match and end_match and area_match):
        raise SourceError("expected cumulative/daily labels or dataProvider.areas missing")
    start = _parse_date(start_match.group(1), "%d-%m-%Y")
    displayed_end = _parse_date(end_match.group(1), "%d-%m-%Y")
    if start > displayed_end:
        raise SourceError("cumulative start follows displayed end")
    try:
        areas, consumed = json.JSONDecoder().raw_decode(page[area_match.start(1):])
    except json.JSONDecodeError as exc:
        raise SourceError("embedded areas are not JSON") from exc
    if not isinstance(areas, list) or not 1 <= len(areas) <= 2000:
        raise SourceError("implausible district count")
    if page[area_match.start(1) + consumed:].lstrip()[:1] != "}":
        raise SourceError("unexpected dataProvider structure after areas")
    rows = []
    seen = set()
    for area in areas:
        if not isinstance(area, dict) or not {"id", "title", "info", "balloonText"} <= area.keys():
            raise SourceError("district record missing required fields")
        raw_id = area["id"]
        if not isinstance(raw_id, str) or not raw_id.isdigit() or raw_id in seen:
            raise SourceError(f"invalid or duplicate IMD ID: {raw_id!r}")
        seen.add(raw_id)
        name = area["title"]
        if not isinstance(name, str) or not 1 <= len(name) <= 120 or any(ord(c) < 32 for c in name):
            raise SourceError(f"invalid district name for IMD ID {raw_id}")
        if not isinstance(area["info"], str) or not isinstance(area["balloonText"], str):
            raise SourceError(f"invalid tooltip fields for IMD ID {raw_id}")
        row_date_raw, departure_text, actual_text, normal_text = _tooltip_fields(area["balloonText"])
        # IMD sometimes emits this explicit zero-date sentinel alongside
        # numeric values. Its period is unknown; retain the raw fields for
        # audit but never count it as a current dated observation.
        if row_date_raw == "0000-00-00":
            row_date = None
        else:
            try:
                row_date = _parse_date(row_date_raw, "%Y-%m-%d")
            except SourceError as exc:
                raise SourceError(f"invalid source row date for IMD ID {raw_id}: {row_date_raw}") from exc
        if row_date is not None and row_date > displayed_end:
            raise SourceError(f"district date exceeds page date for IMD ID {raw_id}")
        actual = _decimal(actual_text, "mm")
        normal = _decimal(normal_text, "mm")
        departure = _decimal(departure_text, "%")
        info = _decimal(area["info"], "%")
        if departure != info:
            raise SourceError(f"tooltip/map departure differs for IMD ID {raw_id}")
        missing = actual is None or normal is None or departure is None
        if missing and not (actual is None and normal is None and departure is None):
            raise SourceError(f"partial missing row for IMD ID {raw_id}")
        if not missing and normal == 0:
            raise SourceError(f"zero normal with departure for IMD ID {raw_id}")
        flags = (["invalid_source_row_date"] if row_date is None else
                 ["older_row_date"] if row_date != displayed_end else [])
        # The displayed mm values are rounded. A generous 1.5 percentage
        # point tolerance catches substantive conflicts without rewriting
        # the provider's published percentage from rounded inputs.
        if not missing and normal and abs(100 * (actual / normal - 1) - departure) > 1.5:
            flags.append("published_departure_arithmetic_mismatch")
        rows.append({
            "geography_id": f"imd_district:{raw_id}",
            "imd_id": raw_id,
            "name_as_published": name,
            "source_row_date": row_date,
            "source_row_date_raw": row_date_raw,
            "observation_period": {
                "start_date": start,
                "end_date": row_date,
                "timezone": "Asia/Kolkata",
                "cutoff_convention": "IMD cumulative calendar labels; precise observation hour not stated on this page",
            } if row_date == displayed_end else None,
            "period_missing_reason": "IMD displays zero-date sentinel" if row_date is None else None,
            "actual_mm": actual,
            "normal_mm": normal,
            "departure_percent_published": departure,
            "status": "missing" if missing else "reported",
            "missing_reason": "IMD displays No Data" if missing else None,
            "current_page_period": row_date == displayed_end,
            "quality_flags": flags,
        })
    if not any(row["current_page_period"] for row in rows):
        raise SourceError("no rows match current displayed date")
    rows.sort(key=lambda row: int(row["imd_id"]))
    return {
        "candidate_type": "imd_cumulative_district_rainfall",
        "review_status": "candidate_unapproved",
        "source": metadata,
        "page_period": {"start_date": start, "displayed_end_date": displayed_end},
        "geography_namespace": "IMD dashboard district IDs; no LGD crosswalk asserted",
        "normal_period": None,
        "normal_period_note": "Normal baseline not identified on the source page; do not compare with other normal series",
        "source_publication_time": None,
        "source_publication_note": "No distinct issue timestamp found; displayed date is observation date, not publication time",
        "counts": {
            "rows": len(rows),
            "current_dated": sum(row["current_page_period"] for row in rows),
            "older_dated": sum(row["source_row_date"] is not None and not row["current_page_period"] for row in rows),
            "invalid_row_dates": sum(row["source_row_date"] is None for row in rows),
            "missing": sum(row["status"] == "missing" for row in rows),
            "current_nonmissing": sum(row["current_page_period"] and row["status"] == "reported" for row in rows),
            "departure_arithmetic_mismatches": sum("published_departure_arithmetic_mismatch" in row["quality_flags"] for row in rows),
        },
        "rows": rows,
    }


def _write_new(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise SourceError(f"immutable path collision: {path}")
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".candidate-", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        # Link creation fails if another process already wrote the immutable
        # destination; unlike replace(), it cannot overwrite that file.
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != content:
                raise SourceError(f"immutable path collision: {path}")
    finally:
        temporary.unlink(missing_ok=True)


def semantic_diff(previous: dict, current: dict) -> dict:
    """Compare observations, excluding retrieval-only metadata and HTML layout."""
    if previous.get("candidate_type") != current.get("candidate_type"):
        raise SourceError("incompatible candidates for IMD semantic diff")
    old = {row["geography_id"]: row for row in previous["rows"]}
    new = {row["geography_id"]: row for row in current["rows"]}
    fields = ("name_as_published", "source_row_date", "source_row_date_raw", "observation_period",
              "period_missing_reason", "actual_mm", "normal_mm",
              "departure_percent_published", "status", "missing_reason", "quality_flags")
    changed = []
    for key in sorted(old.keys() & new.keys()):
        # A newly added audit-only field in the parser is not a change to
        # every historical source row. Compare it once both snapshots carry
        # it; compare established observation fields across versions.
        changed_fields = [field for field in fields
                          if field in old[key] and field in new[key]
                          and old[key][field] != new[key][field]]
        if changed_fields:
            changed.append({"geography_id": key, "fields": changed_fields})
    return {
        "previous_sha256": previous["source"]["source_sha256"],
        "current_sha256": current["source"]["source_sha256"],
        "source_bytes_changed": previous["source"]["source_sha256"] != current["source"]["source_sha256"],
        "page_period_changed": previous["page_period"] != current["page_period"],
        "added_ids": sorted(new.keys() - old.keys()),
        "removed_ids": sorted(old.keys() - new.keys()),
        "changed_rows": changed,
        "observation_changed": bool(changed or new.keys() != old.keys() or previous["page_period"] != current["page_period"]),
    }


def save_candidate(root: Path, body: bytes, metadata: dict, candidate: dict) -> Path:
    """Persist a validated candidate without changing approved/public data."""
    source_hash = hashlib.sha256(body).hexdigest()
    if metadata.get("source_sha256") != source_hash:
        raise SourceError("source hash mismatch before candidate save")
    raw_path = save_raw_snapshot(root, body)
    if candidate["source"].get("raw_snapshot_path") != str(raw_path.relative_to(root)):
        raise SourceError("candidate raw snapshot path mismatch")
    if candidate["source"].get("raw_snapshot_sha256") != source_hash:
        raise SourceError("candidate raw snapshot hash mismatch")
    retrieval_slug = re.sub(r"[^0-9]", "", metadata["retrieved_at"])
    candidate_path = root / "data/candidates/imd" / f"{candidate['page_period']['displayed_end_date']}-{source_hash[:16]}-{retrieval_slug}.json"
    encoded = (json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _write_new(candidate_path, encoded)
    return candidate_path


def save_raw_snapshot(root: Path, body: bytes) -> Path:
    """Write exact fetched bytes once under their full SHA-256; verify reuse."""
    source_hash = hashlib.sha256(body).hexdigest()
    raw_path = root / "data/raw/imd" / f"{source_hash}.html"
    _write_new(raw_path, body)
    if hashlib.sha256(raw_path.read_bytes()).hexdigest() != source_hash:
        raise SourceError("raw snapshot failed post-write hash check")
    return raw_path


def run(root: Path, *, body: bytes | None = None, retrieved_at: str | None = None) -> Path:
    if body is None:
        body, metadata = fetch()
    else:
        if retrieved_at is None:
            raise SourceError("offline import requires explicit retrieval timestamp")
        parsed_retrieval = datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
        if parsed_retrieval.tzinfo is None:
            raise SourceError("retrieval timestamp must include a timezone")
        metadata = {
            "source_url": SOURCE_URL,
            "retrieved_at": retrieved_at,
            "http_status": None,
            "content_type": "text/html (manual import)",
            "response_bytes": len(body),
            "source_sha256": hashlib.sha256(body).hexdigest(),
            "http_last_modified": None,
            "http_date": None,
        }
    candidate = parse(body, metadata)
    # Validate before writing. Raw source is ignored by Git; both files are
    # content-addressed or immutable and never replace approved observations.
    return save_candidate(root, body, metadata, candidate)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--from-file", type=Path, help="parse a previously saved official HTML response")
    parser.add_argument("--retrieved-at", help="required ISO timestamp for --from-file")
    parser.add_argument("--compare", type=Path, help="previous candidate JSON for semantic change report")
    args = parser.parse_args(argv)
    try:
        if args.from_file:
            if not args.retrieved_at:
                raise SourceError("--retrieved-at is required with --from-file")
            if args.from_file.stat().st_size > MAX_BYTES:
                raise SourceError("offline source exceeds byte limit")
            path = run(args.root, body=args.from_file.read_bytes(), retrieved_at=args.retrieved_at)
        else:
            path = run(args.root)
        if args.compare:
            prior = json.loads(args.compare.read_text(encoding="utf-8"))
            current = json.loads(path.read_text(encoding="utf-8"))
            diff = semantic_diff(prior, current)
            diff_path = path.with_suffix(".diff.json")
            _write_new(diff_path, (json.dumps(diff, indent=2, sort_keys=True) + "\n").encode())
            print(diff_path)
    except (OSError, SourceError) as exc:
        print(f"IMD candidate failed: {exc}", file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
