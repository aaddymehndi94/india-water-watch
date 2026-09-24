"""Inventory a built static site against the canonical approved snapshot."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from tools.release_gate import COLLECTIONS, snapshot_digest

ROOT = Path(__file__).resolve().parents[1]


def build_manifest(root: Path, dist: Path | None = None) -> dict:
    data = {}
    for name in COLLECTIONS:
        approved = root / "data" / "approved" / f"{name}.json"
        path = approved if approved.is_file() else root / "data" / f"{name}.json"
        data[name] = json.loads(path.read_text(encoding="utf-8"))
    digest = snapshot_digest(data)
    dist = dist or root / "dist"
    if not (dist / "index.html").is_file():
        raise FileNotFoundError("dist/index.html missing; build first")
    files = {}
    for path in sorted(dist.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink in dist: {path}")
        if path.is_file() and path != dist / "release.json":
            files[path.relative_to(dist).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    observations = [row for row in data["observations"] if row.get("public") is True]
    claims = [row for row in data["claims"] if row.get("public") is True]
    watermarks = {row["id"]: row["period"]["end"][:10] for row in observations}
    git_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    working_tree_dirty = bool(subprocess.run(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=root, capture_output=True, text=True, check=True).stdout.strip())
    return {
        "release_id": f"candidate-{datetime.now(timezone.utc):%Y%m%d}-{digest[:12]}",
        "status": "candidate",
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_head_at_build": git_head,
        "working_tree_dirty_at_build": working_tree_dirty,
        "snapshot_sha256": digest,
        "source_watermarks": watermarks,
        "approved_observation_ids": [row["id"] for row in observations],
        "approved_claim_ids": [row["id"] for row in claims],
        "files_sha256": files,
        "file_count": len(files),
        "total_bytes": sum((dist / path).stat().st_size for path in files),
        "scope": f"{len(observations)} reviewed public observations and {len(claims)} source-linked public claims; each observation retains its own status date and source. Coverage limits are recorded in state/COVERAGE_AND_FRESHNESS.md.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dist", type=Path)
    args = parser.parse_args()
    dist = args.dist or args.root / "dist"
    manifest = build_manifest(args.root, dist)
    path = dist / "release.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path} ({manifest['file_count']} files)")


if __name__ == "__main__":
    main()
