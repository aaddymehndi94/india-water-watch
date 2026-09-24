"""Offline structural starter check. This does NOT certify reporting accuracy."""
from __future__ import annotations
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "AGENTS.md", "START_HERE.md", "FIRST_PROMPT.txt", "UPDATE_PROMPT.txt", "RESUME_PROMPT.txt", "AUDIT_PROMPT.txt", "PUBLISH_PROMPT.txt", "docs/00-TRUTH_RESET.md", "docs/09-EXECUTION_GATES.md", "references/source_registry.json", "references/technical_sources.json", "state/PROJECT_STATE.json", "state/PUBLICATION_POLICY.json", "project/tasks.json", "project/acceptance.csv", "tools/release_gate.py"]


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")
    for path in root.rglob("*.json"):
        if any(p in {"node_modules", ".git", ".cache", "dist", "raw"} for p in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            errors.append(f"Invalid JSON {path.relative_to(root)}: {exc}")
    try:
        sources = json.loads((root / "references/source_registry.json").read_text(encoding="utf-8"))
        ids = [s["id"] for s in sources]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate discovery source IDs")
        for s in sources:
            if s["access_status"] == "lead_only" and s.get("checked_on"):
                errors.append(f"Unchecked source has a checked date: {s['id']}")
        tasks = json.loads((root / "project/tasks.json").read_text(encoding="utf-8"))
        tids = {t["id"] for t in tasks}
        if len(tids) != len(tasks):
            errors.append("Duplicate task IDs")
        for t in tasks:
            if set(t["depends_on"]) - tids:
                errors.append(f"Unknown task dependency: {t['id']}")
        visited, visiting = set(), set()
        by_id = {t["id"]: t for t in tasks}
        def walk(tid: str) -> None:
            if tid in visiting:
                raise ValueError("Cycle in task graph")
            if tid in visited:
                return
            visiting.add(tid)
            for dep in by_id[tid]["depends_on"]:
                if dep in by_id:
                    walk(dep)
            visiting.remove(tid); visited.add(tid)
        for tid in tids:
            walk(tid)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Registry/task structure: {exc}")
    try:
        import tomllib
    except ImportError:
        tomllib = None
    for path in (root / ".codex/agents").glob("*.toml"):
        if tomllib is not None:
            try:
                data = tomllib.loads(path.read_text(encoding="utf-8"))
                if not all(data.get(k) for k in ("name", "description", "developer_instructions")):
                    errors.append(f"Missing agent fields: {path.name}")
            except Exception as exc:
                errors.append(f"Invalid agent TOML {path.name}: {exc}")
    if tomllib is not None:
        try:
            tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid project TOML: {exc}")
    return errors


if __name__ == "__main__":
    problems = validate()
    for item in problems:
        print("ERROR:", item)
    if not problems:
        print("PASS: starter structure, JSON, task graph and available TOML checks.")
        print("NOT CHECKED: factual accuracy, full JSON Schema semantics, website implementation, publication readiness.")
    sys.exit(1 if problems else 0)
