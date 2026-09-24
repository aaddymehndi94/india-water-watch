"""Create a deterministic host-ready ZIP and inventory from an existing dist directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from tools.validate_approved import ROOT

FORBIDDEN = {".git", ".env", ".private", "quarantine", "raw", "fixtures", "state", "node_modules"}


def package_site(dist: Path, output: Path) -> dict:
    dist = Path(dist).resolve()
    output = Path(output).resolve()
    if not (dist / "index.html").is_file():
        raise ValueError("dist/index.html is missing")
    if output == dist or output.is_relative_to(dist):
        raise ValueError("ZIP output must be outside dist")
    files: list[tuple[str, Path]] = []
    for path in dist.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symlink in public output: {path}")
        if not path.is_file():
            continue
        if path.resolve() == output:
            raise ValueError("ZIP output must be outside dist")
        relative = path.relative_to(dist).as_posix()
        if any(part in FORBIDDEN or part.startswith(".env.") for part in path.relative_to(dist).parts):
            raise ValueError(f"Forbidden public path: {relative}")
        files.append((relative, path))
    files.sort()
    output.parent.mkdir(parents=True, exist_ok=True)
    inventory = {}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, path in files:
            content = path.read_bytes()
            inventory[relative] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return {"zip": str(output), "zip_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "file_count": len(files), "uncompressed_bytes": sum(x["bytes"] for x in inventory.values()),
            "zip_bytes": output.stat().st_size, "files": inventory}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "release" / "india-water-watch-site.zip")
    parser.add_argument("--summary", type=Path, default=ROOT / "release" / "package-summary.json")
    args = parser.parse_args()
    try:
        result = package_site(args.dist, args.output)
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"BLOCK: {exc}")
        return 1
    print(f"Packaged {result['file_count']} files: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
