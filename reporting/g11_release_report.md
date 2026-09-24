# India Water Watch · G11 reviewed progress release

**Candidate:** `candidate-20260924-0ff6e35ffc18`, built 24 September 2026 for GitHub Pages at https://aaddymehndi94.github.io/india-water-watch/ . The exact deployed commit and live smoke-test status are recorded separately in `state/DEPLOYMENT_REPORT.md`. This is an agent-reviewed public progress publication, without human field or editorial sign-off.

## Built and verified

- A redesigned dark-default, light-optional, responsive national feature with labeled symbolic artwork, exact-figure motion, source pills, interactive rainfall and reservoir panels, a 36-state/UT locator, static Pagefind search, and a visible IST site-build time. The build time is distinct from each source observation and forecast validity time.
- **22 public source-linked claims, seven numeric observations, 16 evidence records and 43 geography records.** Five IMD rainfall departures end **23 September 2026**; two CWC monitored-storage readings are dated **10 September 2026**. IMD's 24 September heavy-rain report is visible as a counter-signal, and its 17 September extended-range rainfall forecast is labeled valid **24–30 September** only.
- Three original Karnataka gazettes list **177 distinct taluks** declared drought-affected by 22 September, **161 severe and 16 moderate**. The count describes administrative orders, not households affected, crop loss or relief delivered. The dated **AI Author assessment** is a low-confidence conditional scenario with assumptions, evidence, and reversal tests; it does not predict which district will run short or what the 2027 rain will be.
- Independent source/editorial review: `reporting/g11_independent_source_review.md`. Independent browser, visual, accessibility and security review: `reporting/g11_quality_review.md`. Lead data review: `reporting/g11_data_review.md`. The structural release gate passed, bound to the candidate snapshot and report hashes.
- `python tools/validate_starter.py`, approved-schema validation, **80 Python tests**, Astro check (**43 files, zero diagnostics**), root and GitHub-prefix builds (**120 HTML pages, 271 inventoried files** each), Pagefind, journalist exports and ZIP integrity passed. Browser journeys passed **131/131 per profile**; 28 axe scans had zero violations after two accessibility fixes. Chrome screenshots at 360/768/1440 px in dark/light are under `artifacts/qa/g11/`.

## Coverage and limits

- No approved state/UT rainfall values, district observations, river-flow, current groundwater, post-10 September storage trend, 2026 household service, crop-loss or water-linked economic-loss series. State/UT pages are a sourced roster and honest coverage summary; no verified boundary geometry or false heat map is shown. Missing remains unknown. The CWC 17 September indexed PDF still returned 404 during review.
- Completed 2002/2009/2025 monsoon histories provide context, but **2026 cannot be ranked** against completed June–September seasons until a matching cutoff is available. Heavy rain on 24 September does not yet establish catchment recharge or safe service. The current official forecast inspected ends 30 September; the site's longer-range scenario is its own conditional analysis.
- External PDFs/graphics are linked, not copied into bundles. Hero art is an original AI-generated symbolic illustration, visibly labeled. Browser QA used Chrome headless and sampled axe cases; it is not a screen-reader or full WCAG certification. See `state/COVERAGE_AND_FRESHNESS.md` for exact source dates and gaps.

## Artifacts and use

- GitHub repository-path portable ZIP: `release/site-github.zip`; root-path drag-and-drop ZIP: `release/site-compact.zip`.
- Journalist CSVs: `exports/journalists/`; ZIP: `release/journalist-exports.zip`. They include claim/evidence IDs, dates and limitations.
- Local root preview: `python -m http.server 8000 --directory dist-compact`, then open `http://127.0.0.1:8000/`.
- Rebuild GitHub profile: `PUBLIC_SITE_URL=https://aaddymehndi94.github.io PUBLIC_BASE_PATH=/india-water-watch/ npm exec --yes --package=pnpm@12.6.0 -- pnpm build`.
- Ask Codex to follow the prompt in `docs/UPDATE_PLAYBOOK.md` for a reviewed source refresh and GitHub Pages update. There is no background data updater and no maintained secondary deployment.
