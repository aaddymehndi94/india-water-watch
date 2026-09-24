"""Fail-closed STRUCTURAL gate, to be supplemented by full schemas and real audits.

It checks provenance links, comparison flags, artifact hashes and review evidence.
It cannot establish whether a source supports a claim or authenticate a person.
The starter MUST fail this gate until a built/reviewed publication exists.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ("evidence", "observations", "claims", "geographies", "comparisons", "news", "forecasts", "scenarios")
CHECKS = {"data", "claims", "comparability", "editorial", "accessibility", "visual", "security", "rights", "hosting"}
COMPARISON_FIELDS = {"metric_definition", "unit", "geography", "boundary", "season_cutoff", "baseline", "cohort", "population_basis"}


def snapshot_digest(collections: dict) -> str:
    blob = json.dumps(collections, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(blob).hexdigest()


def safe_relative(root: Path, relative: str) -> Path | None:
    if not isinstance(relative, str) or not relative or "\x00" in relative:
        return None
    if Path(relative).is_absolute() or PureWindowsPath(relative).is_absolute():
        return None
    try:
        path = (root / relative).resolve()
        path.relative_to(root.resolve())
        return path
    except (ValueError, OSError):
        return None


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Expected an object")
    return value


def gate(root: Path = ROOT, publication: bool = False) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    collections: dict[str, list] = {}
    for name in COLLECTIONS:
        try:
            value = json.loads((root / "data" / f"{name}.json").read_text(encoding="utf-8"))
            if not isinstance(value, list):
                raise ValueError("Expected a collection array")
            collections[name] = value
        except (OSError, ValueError) as exc:
            errors.append(f"Cannot read {name}: {exc}")
            collections[name] = []
    evidence = {r["id"]: r for r in collections["evidence"] if isinstance(r, dict) and isinstance(r.get("id"), str)}
    observations = [r for r in collections["observations"] if isinstance(r, dict) and r.get("public") is True]
    claims = [r for r in collections["claims"] if isinstance(r, dict) and r.get("public") is True]
    if not observations or not claims:
        errors.append("No public observations and reviewed claims; an empty starter is not a publication")
    for name, rows in collections.items():
        ids = [r.get("id") for r in rows if isinstance(r, dict)]
        valid_ids = [x for x in ids if isinstance(x, str) and x]
        if len(valid_ids) != len(rows) or len(valid_ids) != len(set(valid_ids)):
            errors.append(f"Malformed or duplicate IDs in {name}")
        for record in rows:
            if not isinstance(record, dict):
                continue
            if "public" in record and not isinstance(record["public"], bool):
                errors.append(f"Invalid public flag: {record.get('id')}")
            if record.get("public") is not True:
                continue
            if record.get("synthetic"):
                errors.append(f"Synthetic record cannot publish: {record.get('id')}")
            refs = record.get("evidence_ids", [])
            if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
                errors.append(f"Malformed evidence references: {record.get('id')}")
                refs = []
            if name in {"claims", "observations", "news", "forecasts", "scenarios"} and not refs:
                errors.append(f"Missing evidence: {record.get('id')}")
            for ref in refs:
                item = evidence.get(ref)
                if not item or item.get("source_inspected") is not True or not item.get("locator"):
                    errors.append(f"Uninspected/orphan evidence {ref} for {record.get('id')}")
                else:
                    try:
                        url = urlparse(item.get("url", ""))
                        safe = url.scheme in {"http", "https"} and bool(url.hostname) and not url.username
                    except (TypeError, ValueError, AttributeError):
                        safe = False
                    if not safe:
                        errors.append(f"Unsafe evidence URL: {ref}")
            if record.get("requires_human_review") and not record.get("human_review_receipt"):
                errors.append(f"Missing genuine human-review reference: {record.get('id')}")
    for claim in claims:
        if claim.get("status") not in ("verified", "attributed", "corrected") or not claim.get("reviewer_id"):
            errors.append(f"Unreviewed claim cannot publish: {claim.get('id')}")
    for comparison in collections["comparisons"]:
        if not isinstance(comparison, dict) or comparison.get("public") is not True:
            continue
        if comparison.get("status") == "allowed":
            flags = comparison.get("checks")
            if not isinstance(flags, dict) or COMPARISON_FIELDS - set(flags):
                errors.append(f"Incomplete comparison checks: {comparison.get('id')}")
            elif any(v not in ("match", "harmonized", "not_applicable") for v in flags.values()):
                errors.append(f"Incompatible comparison allowed: {comparison.get('id')}")
            if isinstance(flags, dict) and "harmonized" in flags.values() and not comparison.get("harmonization_method"):
                errors.append(f"Missing harmonization method: {comparison.get('id')}")
            if not comparison.get("reviewer_id"):
                errors.append(f"Unreviewed comparison: {comparison.get('id')}")
    dist = root / "dist"
    if not (dist / "index.html").is_file():
        errors.append("dist/index.html is missing")
    manifest: dict = {}
    try:
        manifest = read_object(dist / "release.json")
    except (OSError, ValueError):
        errors.append("Built dist/release.json manifest missing/invalid")
    try:
        digest = snapshot_digest(collections)
    except (TypeError, ValueError):
        digest = None
        errors.append("Snapshot contains invalid non-finite/non-serializable values")
    if manifest:
        if manifest.get("snapshot_sha256") != digest:
            errors.append("Built manifest does not match reviewed input snapshot")
        if not manifest.get("release_id") or not manifest.get("source_watermarks"):
            errors.append("Missing release ID/source observation watermarks")
        expected = manifest.get("files_sha256", {})
        actual = {}
        for path in dist.rglob("*"):
            if path.is_symlink():
                errors.append("Symlink in public output")
                continue
            if not path.is_file() or path == dist / "release.json":
                continue
            rel = path.relative_to(dist).as_posix()
            try:
                contents = path.read_bytes()
            except OSError:
                errors.append(f"Cannot inspect public file: {rel}")
                continue
            actual[rel] = hashlib.sha256(contents).hexdigest()
            if any(part in {".env", ".git", ".private", "quarantine", "fixtures", "raw", "state"} or part.startswith('.env.') for part in path.relative_to(dist).parts):
                errors.append(f"Forbidden public output: {rel}")
            if path.suffix.lower() in {".html", ".js", ".json", ".csv", ".txt", ".md"}:
                text = contents.decode("utf-8", errors="replace")
                if "SYNTHETIC_TEST_FIXTURE" in text or "STARTER_ONLY_PLACEHOLDER" in text:
                    errors.append(f"Placeholder/test fixture leaked into {rel}")
        if not isinstance(expected, dict) or not expected or expected != actual:
            errors.append("Public file inventory/hash mismatch")
    try:
        review = read_object(root / "state/RELEASE_REVIEW.json")
        if review.get("snapshot_sha256") != digest or review.get("release_id") != manifest.get("release_id"):
            errors.append("Review is not tied to the built release/snapshot")
        if review.get("blocking_findings"):
            errors.append("Unresolved blocking review findings")
        passed = set()
        review_checks = review.get("checks", [])
        if not isinstance(review_checks, list):
            raise ValueError("Review checks must be an array")
        for check in review_checks:
            if not isinstance(check, dict):
                errors.append("Malformed review check")
                continue
            path = safe_relative(root, check.get("evidence_path", ""))
            if check.get("status") == "passed" and path and path.is_file() and check.get("reviewer"):
                if check.get("evidence_sha256") == hashlib.sha256(path.read_bytes()).hexdigest() and check.get("id") in CHECKS:
                    passed.add(check["id"])
        if CHECKS - passed:
            errors.append("Missing evidenced review checks: " + ", ".join(sorted(CHECKS-passed)))
    except (OSError, ValueError, TypeError):
        errors.append("Invalid or missing release review")
    if publication:
        try:
            policy = read_object(root / "state/PUBLICATION_POLICY.json")
            manifest_path = dist / "release.json"
            manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest() if manifest_path.is_file() else None
            if policy.get("first_deployment_authorized") is not True or not policy.get("approved_host"):
                errors.append("No explicit destination/publication authorization")
            if not manifest_hash or policy.get("approved_release_sha256") != manifest_hash:
                errors.append("Authorization is not tied to this release manifest hash")
        except (OSError, ValueError):
            errors.append("Missing publication policy")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publication", action="store_true")
    args = parser.parse_args()
    problems = gate(publication=args.publication)
    for problem in problems:
        print("BLOCK:", problem)
    if problems:
        print("NOT READY. Fix or withhold; do not fabricate approvals or test evidence.")
    else:
        print("Structural gate passed. Source support and real publisher/human approval still require the documented review process.")
    sys.exit(1 if problems else 0)
