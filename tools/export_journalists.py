"""Export public, reviewed reporting as formula-safe CSVs for journalists."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import tempfile

from tools.build_publication_data import publication
from tools.validate_approved import ROOT


FIELDS = {
    "claims": ["id", "text", "kind", "status", "geographyIds", "observationIds", "evidenceIds", "reviewedAt", "limitations"],
    "observations": ["id", "geographyId", "metricId", "seriesId", "value", "unit", "status", "missingReason", "periodStart", "periodEnd", "periodPrecision", "cutoffConvention", "periodKind", "baselineId", "sourceId", "evidenceIds", "claimId"],
    "sources": ["id", "sourceId", "title", "publisher", "url", "observedThrough", "observedThroughPrecision", "publicationDate", "publicationDatePrecision", "retrievedAt", "locator", "sha256"],
    "geographies": ["id", "name", "type", "slug", "code", "version", "parentIds"],
}


def safe_cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    result = str(value)
    # Spreadsheet formula parsers also accept leading whitespace and control characters.
    if result.lstrip("\ufeff\t\r\n ").startswith(("=", "+", "-", "@")):
        return "'" + result
    return result


def write_exports(root: Path = ROOT, output: Path | None = None) -> Path:
    root = Path(root)
    target = output or root / "exports" / "journalists"
    data = publication(root)
    target.mkdir(parents=True, exist_ok=True)
    for name, fields in FIELDS.items():
        path = target / f"{name}.csv"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8-sig", newline="", dir=target, prefix=f".{name}-", delete=False) as tmp:
            writer = csv.DictWriter(tmp, fields, extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for record in data[name]:
                writer.writerow({field: safe_cell(record.get(field)) for field in fields})
            temporary = Path(tmp.name)
        os.replace(temporary, path)
    readme = (
        "India Water Watch journalist exports\n"
        f"Snapshot SHA-256: {data['snapshotSha256']}\n"
        f"Release ID: {data['releaseId']}\n"
        "Only public records tied to reviewed claims are included. Empty cells mean missing or inapplicable, never zero. "
        "Observation periods are calendar-date precision; no midnight observation hour is asserted. See cutoffConvention. Source publication/retrieval dates have distinct meanings. "
        "CSV text that could be interpreted as a spreadsheet formula is prefixed with an apostrophe. "
        "Use claims.csv evidenceIds and observations.csv sourceId to join sources.csv.\n"
    )
    (target / "README.txt").write_text(readme, encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        output = write_exports(args.root, args.output)
    except (OSError, ValueError) as exc:
        print(f"BLOCK: {exc}")
        return 1
    print(f"Wrote journalist exports to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
