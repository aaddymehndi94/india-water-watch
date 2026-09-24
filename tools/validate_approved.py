"""Validate the canonical approved snapshot before any public projection is built."""
from __future__ import annotations

import argparse
from datetime import datetime
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

COLLECTIONS = {"evidence": "evidence", "geographies": "geography", "observations": "observation", "claims": "claim"}
ROOT = Path(__file__).resolve().parents[1]


def _safe_source_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            return False
        if parsed.hostname.lower() in {"localhost", "localhost.localdomain"} or parsed.hostname.lower().endswith(".local"):
            return False
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if not ip.is_global:
                return False
        except ValueError:
            pass
        return True
    except (TypeError, ValueError):
        return False


def load_collections(root: Path = ROOT) -> dict[str, list[dict]]:
    result = {}
    for name in COLLECTIONS:
        path = root / "data" / "approved" / f"{name}.json"
        rows = json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"non-finite value: {x}")))
        if not isinstance(rows, list):
            raise ValueError(f"{path}: expected an array")
        result[name] = rows
    return result


def validate(root: Path = ROOT, collections: dict[str, list[dict]] | None = None) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    try:
        rows = collections if collections is not None else load_collections(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema is required for full approved-record validation; install requirements.lock"]
    indexes: dict[str, dict[str, dict]] = {}
    for name, schema_name in COLLECTIONS.items():
        records = rows.get(name)
        if not isinstance(records, list):
            errors.append(f"{name}: expected an array")
            indexes[name] = {}
            continue
        schema = json.loads((root / "schemas" / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        index: dict[str, dict] = {}
        for n, record in enumerate(records):
            label = f"{name}[{n}]"
            if not isinstance(record, dict):
                errors.append(f"{label}: expected an object")
                continue
            errors.extend(f"{label}.{'.'.join(map(str, e.path))}: {e.message}" for e in validator.iter_errors(record))
            ident = record.get("id")
            if not isinstance(ident, str) or not ident:
                errors.append(f"{label}: missing ID")
            elif ident in index:
                errors.append(f"{name}: duplicate ID {ident}")
            else:
                index[ident] = record
        indexes[name] = index
    evidence, geographies, observations, claims = (indexes[x] for x in COLLECTIONS)
    def period_order(record: dict, label: str) -> None:
        period = record.get("period")
        if not isinstance(period, dict):
            return
        try:
            start = datetime.fromisoformat(period["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(period["end"].replace("Z", "+00:00"))
            if end < start:
                errors.append(f"{label}: period ends before it starts")
        except (KeyError, TypeError, ValueError):
            pass  # JSON Schema reports malformed timestamps when available.
    def refs(record: dict, field: str, target: dict, label: str) -> None:
        values = record.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{label}.{field}: expected array")
            return
        for ref in values:
            if not isinstance(ref, str) or ref not in target:
                errors.append(f"{label}.{field}: missing reference {ref!r}")
    for ev in evidence.values():
        label = f"evidence {ev['id']}"
        refs(ev, "upstream_evidence_ids", evidence, label)
        if not _safe_source_url(ev.get("url", "")):
            errors.append(f"{label}: unsafe source URL")
    for geo in geographies.values():
        label = f"geography {geo['id']}"
        refs(geo, "parent_ids", geographies, label)
        refs(geo, "evidence_ids", evidence, label)
    for obs in observations.values():
        label = f"observation {obs['id']}"
        period_order(obs, label)
        refs(obs, "evidence_ids", evidence, label)
        geo = geographies.get(obs.get("geography_id"))
        if not geo:
            errors.append(f"{label}: missing geography {obs.get('geography_id')!r}")
        elif geo.get("boundary_version") != obs.get("boundary_version"):
            errors.append(f"{label}: geography boundary version mismatch")
        if obs.get("status") == "missing" and (obs.get("value") is not None or not obs.get("missing_reason")):
            errors.append(f"{label}: missing status needs null value and reason")
        if obs.get("status") != "missing" and obs.get("value") is None:
            errors.append(f"{label}: non-missing status needs value")
        if obs.get("public") is True:
            if obs.get("synthetic") is not False:
                errors.append(f"{label}: synthetic or unclassified data cannot publish")
            if obs.get("status") in {"projected", "estimated"}:
                errors.append(f"{label}: projected/estimated observations need separate reviewed forecast or scenario path")
            for ref in obs.get("evidence_ids", []) if isinstance(obs.get("evidence_ids"), list) else []:
                if ref in evidence and evidence[ref].get("source_inspected") is not True:
                    errors.append(f"{label}: evidence {ref} was not inspected")
    for claim in claims.values():
        label = f"claim {claim['id']}"
        period_order(claim, label)
        refs(claim, "evidence_ids", evidence, label)
        refs(claim, "observation_ids", observations, label)
        refs(claim, "geography_ids", geographies, label)
        refs(claim, "input_claim_ids", claims, label)
        if claim.get("public") is True:
            if claim.get("status") not in {"verified", "attributed", "corrected"} or not claim.get("reviewer_id") or not claim.get("reviewed_at"):
                errors.append(f"{label}: public claim must be reviewed and verified/attributed/corrected")
            if claim.get("requires_human_review") and not claim.get("human_review_receipt"):
                errors.append(f"{label}: missing human review receipt")
            for ref in claim.get("evidence_ids", []) if isinstance(claim.get("evidence_ids"), list) else []:
                if ref in evidence and evidence[ref].get("source_inspected") is not True:
                    errors.append(f"{label}: evidence {ref} was not inspected")
            for ref in claim.get("observation_ids", []) if isinstance(claim.get("observation_ids"), list) else []:
                if ref in observations and observations[ref].get("public") is not True:
                    errors.append(f"{label}: observation {ref} is not public")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    problems = validate(args.root)
    for problem in problems:
        print("BLOCK:", problem)
    if problems:
        print(f"Approved snapshot validation failed: {len(problems)} issue(s)")
        return 1
    print("Approved snapshot structure and publication references validated. Source support still needs independent editorial review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
