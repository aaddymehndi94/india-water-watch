# Lead release checks · 24 September 2026

Scope: local candidate represented by `dist/release.json` and `dist-compact/release.json`. This is engineering evidence, not human editorial sign-off.

## Data and comparability

The approved validator and 80 unit tests pass. The public projection selects only 11 agent-reviewed claims, five IMD rainfall observations, eight exact evidence records and 41 geography entries. The IMD district refresh is candidate-only; one invalid source date, 33 stale source rows and 31 explicit No Data rows are excluded from current dated numeric counts. The approved snapshot contains no district rainfall imputation. National rainfall arithmetic was independently replayed; regional provider percentages are labeled as such because the cumulative denominators are not printed. The 2018 survey, 2024 sampled functionality survey and 2026 administrative connection count are not plotted as one trend. Historical rainfall and reservoir ranks remain withheld pending matching periods and cohorts. See `reporting/final_fact_review.md`, `reporting/imd_adapter.md`, `reporting/history_comparator.md` and `state/COVERAGE_AND_FRESHNESS.md`.

## Editorial and rights

Public assertions use approved claim IDs and source pages. The prior “worst year,” return-period and reservoir figures are retired or unverified, per `artifacts/audits/prior-claims-audit.md`. Forecast copy says issued 31 August, September 2026 validity, latest-issue status unknown; its category is not described as observed rainfall. Government funding is ministry-reported release, not expenditure or outcome. No first-hand interview, quotation or human review is claimed. No original IMD graphic, restricted raw PDF, Survey of India map geometry or other downloaded copyrighted material is copied into `dist`; only brief attributed numeric facts and source metadata are used. Public source links point to issuing bodies, and the final build scan found no raw, quarantine, fixture, private or state paths. This is an agent/editor engineering review and does not establish a legal opinion on rights.

## Hosting and artifacts

The exact GitHub Pages repository prefix `/india-water-watch/` and root-path compact profile build successfully. Their Pagefind indexes include 104 pages, and each output contains 233 files, including `release.json`. Browser deep-link, search, link, asset and download results are in `reporting/final_quality_review.md` and `artifacts/qa/final_browser_qa.json`. The deterministic ZIPs in `release/` each pass `ZipFile.testzip()`; their individual checksums and file inventories are in the adjacent package summaries. No deployment or remote smoke-test is represented by these local checks.
