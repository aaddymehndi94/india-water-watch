"""Build a portable root-path static profile from approved records."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

from tools.validate_approved import ROOT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["compact", "root"], default="compact")
    parser.add_argument("--site-url", help="Canonical root URL of the chosen host; omit for portable preview")
    args = parser.parse_args()
    dist = ROOT / ("dist-compact" if args.profile == "compact" else "dist-root")
    env = os.environ.copy()
    env["PUBLIC_BASE_PATH"] = "/"
    env["IWW_OUT_DIR"] = str(dist)
    if args.site_url:
        env["PUBLIC_SITE_URL"] = args.site_url
    else:
        env.pop("PUBLIC_SITE_URL", None)
    bindir = ROOT / "node_modules" / ".bin"
    suffix = ".cmd" if os.name == "nt" else ""
    subprocess.run([sys.executable, "-m", "tools.build_publication_data"], cwd=ROOT, check=True)
    subprocess.run([str(bindir / ("astro" + suffix)), "build"], cwd=ROOT, env=env, check=True)
    subprocess.run([str(bindir / ("pagefind" + suffix)), "--site", str(dist)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "tools.make_release_manifest", "--dist", str(dist)], cwd=ROOT, check=True)
    print(f"Built {dist}")


if __name__ == "__main__":
    main()
