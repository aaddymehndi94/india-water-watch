# Current handoff

Status: G0 toolchain passed; G1 evidence audit and G2 site/data vertical slice underway. Six bounded native workers were started; read their owned `reporting/`, `pipeline/`, and `src/` output before integration.
Next command: `npm exec --yes --package=pnpm@12.6.0 -- pnpm check` after the frontend files land. Then run `python -m unittest discover -s tests -v` and review `data/candidates/` without promoting stale or missing rows.
Do not reuse the earlier HTML as verified data. Exact next publication action: create a claim-reviewed local build and test GitHub Pages subpath before any push.
