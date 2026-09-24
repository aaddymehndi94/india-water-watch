# India Water Watch · Codex newsroom starter

**A build brief and executable safeguards, not a completed website or a verified 2026 crisis report.**
Prepared 24 September 2026. Working name: **India Water Watch**. Suggested repository: `india-water-watch`.

Build an independent, public-interest India-wide water reporting platform: deeply sourced journalism, local exploration, reproducible history, current observations, official outlooks, conditional scenarios, and practical public information. Report improvement as prominently as deterioration. Discover the story; do not manufacture a crisis to fit the brief.

## Start

1. Extract the contents of this folder into a new or existing repository. Keep hidden `.codex` and `.github` folders.
2. Open that folder in your interactive Codex terminal, on Windows, Linux or macOS.
3. Paste **`FIRST_PROMPT.txt`**. Codex should read `AGENTS.md`, inspect its tools, delegate bounded work, and proceed through the gates without routine check-ins.
4. Review the final local preview and `state/RELEASE_REPORT.md` before publishing. Account creation, paid services, public deployment and outside contact require explicit authorization.

`START_HERE.md` explains the operator workflow. `docs/08-AGENT_RUNBOOK.md` explains orchestration. `docs/09-EXECUTION_GATES.md` defines completion.

## What is here

- A full editorial assignment, research desk plan, data/methodology contract and design direction.
- Native Codex custom-agent TOML files plus first-run, refresh, resume, audit and publish prompts.
- A source-discovery registry with honest access statuses; **a discovered homepage is not evidence for a numeric claim**.
- Empty production data stores and JSON Schemas, deliberately not seeded with suspect figures.
- A quarantine ledger for earlier conversation claims, including the earlier “~30% pressure” calculation.
- Tested Python reference arithmetic and comparison checks; fail-closed starter release checks.
- Work breakdown, acceptance matrix, persistent state, reporting templates and hosting workflow specifications.

## Commands that actually exist in this pack

```text
python tools/validate_starter.py
python -m unittest discover -s tests -v
python tools/release_gate.py
```

The first two should pass on a supported Python 3 installation using only the standard library. The third **must fail before a real site and review evidence exist**. No package install, scraping, paid API, or hosting action runs merely by opening this pack.

Commands such as `pnpm dev`, `pnpm verify`, `pnpm refresh` and `pnpm package:site` are the specified **implementation interface Codex must create**, not commands already implemented here.

## Architecture decision

Use **Astro static output + React interactive islands + TypeScript + Tailwind CSS**. Use shared D3/Observable Plot chart components, compact versioned geography and a static search index. Keep ingestion and analysis out of the browser. Build a portable `dist/` and a host-ready ZIP. GitHub Pages is the default first host; a root-path build supports Cloudflare Pages or an S3/CloudFront deployment.

Resolve compatible current stable package versions at G0 and commit the lockfiles. No speculative version numbers, new custom agent framework, mandatory database, or visitor-funded AI calls.

## Evidence reset

The earlier chat and HTML report are **not source data**. Their inputs, historical rankings and reservoir comparisons have not been adequately established for publication. Even numerically correct population/rainfall arithmetic is not a measurement of water availability or a “crisis severity” index. See `docs/00-TRUTH_RESET.md` before anything else.

## Editorial independence

No predetermined national catastrophe, state-government scorecard, party ranking, invented interviews, fake bylines, unsupported disaster probability, or countdown to water exhaustion. Describe documented conditions and responses, attribute contested interpretations, and make uncertainty visible. The site must remain useful in a recovery, flood episode, ordinary season, or mixed regional picture.

## License

Original starter text and code are licensed under `LICENSE`. Third-party datasets, maps, reporting, photos and quotes retain their own rights. `RIGHTS.md` is not permission to republish them.
