# India Water Watch · local release candidate

**Candidate:** `candidate-20260924-c5c2701d6b3c` · built 24 September 2026. The GitHub Pages profile ZIP is `release/site-github.zip`; the root profile is hosted through ChatGPT Sites. This agent-reviewed progress candidate is publicly live at https://aaddymehndi94.github.io/india-water-watch/ and https://india-water-watch.aaddy.chatgpt.site .

## Built and verified

- Astro 7.3.4 static site with React exploration, Pagefind search, responsive pages, source detail, coverage and freshness report, public progress page, chart/table/CSV/SVG and 36 state/UT directory pages. Both profiles built **104 HTML pages and 233 total files**.
- **11 attributed public claims**, **five numeric IMD rainfall observations**, **eight source evidence records** and **41 geography entries** in the approved projection. National rainfall from 1 June through 23 September 2026 is provider reported at 713.3 mm versus 837.7 mm normal, −14.9%; four IMD reporting regions are provider reported and their cumulative denominators were not independently reconstructed. Other claims cover a dated IMD September outlook, rural water access surveys/administrative reports and a ministry release. See `state/COVERAGE_AND_FRESHNESS.md`.
- Inherited claims were independently reset in `artifacts/audits/prior-claims-audit.md`. Unverified reservoir, district, return-period and “worst year” claims were withheld.
- Approved data/reference validation passed; **80 Python tests passed**; Astro strict check passed **40 files, zero errors/warnings/hints**; root and GitHub subpath builds and Pagefind indexing passed. Independent browser QA checked 104 routes at 360px in each profile, 103 linked pages, search, downloads, keyboard/no-JS, reduced motion and simulated 200% zoom. Independent agent fact and editorial reviews have no remaining material blocker for this narrow public copy. `python tools/release_gate.py` passes against the exact approved snapshot and `dist/` inventory.
- ZIP integrity check passed (`ZipFile.testzip()` returned no corrupt member) for `release/site-github.zip` and `release/site-compact.zip`. Journalist CSVs are in `exports/journalists/` and `release/journalist-exports.zip`. ZIP hashes and file inventories are in `release/site-*-summary.json`.

## Limits and approvals

- No current approved district rainfall, licensed boundary map, reservoir/storage cohort, groundwater trend, river flow, household service, crop/economic loss or national crisis severity conclusion. State pages are a sourced geographic directory, not local condition reports. Basins and history explain method and gaps; no cross-series rank is published.
- The live IMD district adapter writes **unapproved candidates only**. Its latest inspected response had 761 rows: 727 current dated, 722 current dated numeric, 33 older, 31 explicit No Data and one invalid row date. Two current numeric rows had provider arithmetic discrepancies. No missing district value was filled.
- Agent review is not human review. No axe scan, full screen-reader/WCAG audit, native 200% zoom, mobile-throttled Core Web Vitals benchmark, external rights opinion or remote Pages smoke test was completed. The final-publication policy gate remains closed; sensitive claims and a settled publisher identity would require genuine human confirmation. The explicit user instruction authorizes a GitHub **progress site**, so a source-safe progress build may be pushed separately.

## Artifacts and commands

```bash
# Root local preview
python -m http.server 8000 --directory dist-compact
# Open http://127.0.0.1:8000/

# GitHub repository-prefix preview
npm exec --yes --package=pnpm@12.6.0 -- pnpm preview -- --host 127.0.0.1
# Open the printed /india-water-watch/ path

# Candidate-only update; supply the real evaluation time in IST
python pipeline/refresh.py --scope all --as-of 2026-09-24T12:00:00+05:30

# Rebuild and verify after review/promotion
python -m tools.export_journalists
python -m unittest discover -s tests -q
npm exec --yes --package=pnpm@12.6.0 -- pnpm check
python -m tools.build_profile --profile compact
PUBLIC_SITE_URL=https://aaddymehndi94.github.io PUBLIC_BASE_PATH=/india-water-watch/ npm exec --yes --package=pnpm@12.6.0 -- pnpm build
python tools/release_gate.py
```

The prompt-driven update guide is `docs/UPDATE_PLAYBOOK.md`. Root and GitHub ZIPs have different base paths. Host the contents of the appropriate ZIP over HTTP(S); do not assume `file://` supports search. Screenshots at 360, 768 and 1440 CSS px are in `artifacts/qa/`. Full evidence is in `reporting/final_fact_review.md`, `reporting/final_editorial_review.md`, `reporting/final_quality_review.md`, `reporting/release_checks.md` and `state/RELEASE_REVIEW.json`.

## Hosting

The primary public progress URL is https://aaddymehndi94.github.io/india-water-watch/ . The existing `.github/workflows/pages.yml` builds and deploys on reviewed `main` pushes; its latest checked run succeeded. The secondary root-path Sites URL is https://india-water-watch.aaddy.chatgpt.site . See `state/DEPLOYMENT_REPORT.md` for both hosts' live route/search checks and Sites version IDs. No scheduled candidate auto-promotion is configured.

To roll back, redeploy an earlier reviewed commit/workflow run or revert with a new commit. Keep prior source snapshots and release manifests; do not rewrite history or silently alter observation dates.
