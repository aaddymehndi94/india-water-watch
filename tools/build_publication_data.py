"""Build a deterministic, safe frontend projection from the approved snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from tools.validate_approved import ROOT, load_collections, validate


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def publication(root: Path = ROOT) -> dict:
    root = Path(root)
    rows = load_collections(root)
    problems = validate(root, rows)
    if problems:
        raise ValueError("Approved snapshot failed validation:\n" + "\n".join(problems))
    digest = hashlib.sha256(canonical_bytes(rows)).hexdigest()
    evidence = {row["id"]: row for row in rows["evidence"]}
    observations = {row["id"]: row for row in rows["observations"]}
    selected_claims = sorted((c for c in rows["claims"] if c["public"] is True), key=lambda c: c["id"])
    used_obs: dict[str, str] = {}
    for claim in selected_claims:
        for oid in claim["observation_ids"]:
            used_obs.setdefault(oid, claim["id"])
    forecast_only_evidence = {
        eid for claim in selected_claims if claim["kind"] == "forecast" for eid in claim["evidence_ids"]
    } - {
        eid for claim in selected_claims if claim["kind"] != "forecast" for eid in claim["evidence_ids"]
    }
    unclaimed = sorted(o["id"] for o in rows["observations"] if o["public"] is True and o["id"] not in used_obs)
    if unclaimed:
        raise ValueError("Public observations have no reviewed public claim: " + ", ".join(unclaimed))
    used_evidence = set()
    for claim in selected_claims:
        used_evidence.update(claim["evidence_ids"])
    for oid in used_obs:
        used_evidence.update(observations[oid]["evidence_ids"])
    # The geography roster is a public factual assertion too. Its source must
    # travel with state/UT exploration even when no observation is available.
    for geo in rows["geographies"]:
        if geo["kind"] in {"state", "ut", "union_territory"}:
            used_evidence.update(geo["evidence_ids"])
    sources = []
    for eid in sorted(used_evidence):
        ev = evidence[eid]
        period_end = ((ev["observation_period"] or {}).get("end") or "")[:10] or None
        date_only_publications = {"E-IMD-OUTLOOK-20260831", "E-IMD-EXTENDED-20260917", "E-NSO-WATER-2018", "E-KA-GAZETTE-DROUGHT-20260827", "E-KA-GAZETTE-DROUGHT-20260917", "E-KA-GAZETTE-DROUGHT-20260922"}
        sources.append({
            "id": eid, "sourceId": ev["source_id"], "title": ev["title"],
            "publisher": ev["publisher"], "url": ev["url"],
            "observedThrough": None if eid in forecast_only_evidence else period_end,
            "observedThroughPrecision": "unknown" if eid in forecast_only_evidence or not period_end else "date",
            "validityEnd": period_end if eid in forecast_only_evidence else None,
            "publicationDate": (ev["published_at"][:10] if eid in date_only_publications and ev["published_at"] else ev["published_at"]),
            "publicationDatePrecision": ("date" if eid in date_only_publications and ev["published_at"] else "datetime" if ev["published_at"] else "unknown"),
            "retrievedAt": ev["retrieved_at"],
            "locator": ev["locator"], "sha256": ev["sha256"],
        })
    geographies = [{
        "id": geo["id"], "name": geo["name"], "type": geo["kind"],
        "slug": geo["id"].split(":")[-1].lower().replace("_", "-"),
        "code": geo["authority_code"], "version": geo["boundary_version"],
        "parentIds": geo["parent_ids"],
    } for geo in sorted(rows["geographies"], key=lambda g: g["id"])]
    projected_obs = []
    for oid, cid in sorted(used_obs.items()):
        obs = observations[oid]
        projected_obs.append({
            "id": oid, "geographyId": obs["geography_id"], "metricId": obs["metric_id"],
            "seriesId": obs["series_id"], "value": obs["value"], "unit": obs["unit"],
            "periodStart": obs["period"]["start"][:10], "periodEnd": obs["period"]["end"][:10],
            "periodPrecision": "date", "cutoffConvention": obs["period"].get("cutoff_convention"),
            "periodKind": obs["period"]["kind"], "status": obs["status"],
            "missingReason": obs["missing_reason"], "baselineId": obs["baseline_id"],
            "sourceId": obs["evidence_ids"][0], "evidenceIds": obs["evidence_ids"],
            "claimId": cid,
        })
    claims = [{
        "id": c["id"], "text": c["text"], "evidenceIds": c["evidence_ids"],
        "observationIds": c["observation_ids"], "geographyIds": c["geography_ids"],
        "status": c["status"], "kind": c["kind"], "period": c["period"],
        "reviewedAt": c["reviewed_at"], "limitations": c["limitations"],
        "methodPath": c["method_path"], "inputClaimIds": c["input_claim_ids"],
    } for c in selected_claims]
    reviewed_at = max((c["reviewed_at"] for c in selected_claims), default=None)
    watermarks = {source["id"]: source["observedThrough"] for source in sources}
    return {
        "schemaVersion": "1", "releaseId": "approved-" + digest[:12],
        "snapshotSha256": digest, "reviewedAt": reviewed_at,
        "claims": claims, "observations": projected_obs, "geographies": geographies,
        "sources": sources, "sourceWatermarks": watermarks,
        "counts": {"claims": len(claims), "observations": len(projected_obs),
                   "geographies": len(geographies), "sources": len(sources)},
    }


def write_publication(root: Path = ROOT, output: Path | None = None) -> Path:
    root = Path(root)
    target = output or root / "data" / "approved" / "publication.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(publication(root), ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, prefix=".publication-", delete=False) as tmp:
        tmp.write(data)
        temporary = Path(tmp.name)
    os.replace(temporary, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        target = write_publication(args.root, args.output)
    except (OSError, ValueError) as exc:
        print(f"BLOCK: {exc}")
        return 1
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
