# India Water Watch · G13a visual news checkpoint

**Candidate:** `candidate-20260924-f22be1c28b6b`, built 24 September 2026 for the authorized GitHub Pages site, https://aaddymehndi94.github.io/india-water-watch/ . This report describes the local candidate. The currently live revision and its smoke-test result remain in `state/DEPLOYMENT_REPORT.md` until this checkpoint is pushed and verified. The prior G11 report is archived at `reporting/g11_release_report.md`.

## What changed

- The national cover now shows IMD's **sixth-lowest June since 1901** and the separate **−14.9% rainfall departure for 1 June–23 September** within the first mobile screen. The full feature has a reader-controlled, exact-value rainfall stage with distinct windows, source links, keyboard/touch and no-JavaScript content. These figures are different periods; neither measures household water supply.
- A 36-place **schematic, nongeographic** state/UT locator joins the atlas, alongside A–Z navigation and explicit missing state-level observations. No boundary map or unsupported state rain shading was published.
- History now presents the completed June rank and the June observed/normal pair, while explicitly refusing a rank for the incomplete full monsoon. Impacts presents two discrete DCA Bengaluru onion-centre prices, ₹23/kg on 23 September 2025 and ₹57/kg on 23 September 2026, without weather causation. Response presents the separate July Army-reported flood operation and 1 August Union flood approval alongside Karnataka's 177 declared taluks. Dated updates, journalist counters and progress copy follow the approved release.
- The design/decision audit, visual critique, source and media/markets research, and independent G12 source review are preserved in `reporting/`. The source reviewer found real national and regional 2026 coverage, so a media-silence claim is rejected. No unlicensed newsroom photograph or copied article screenshot is in this candidate.

## Data and review scope

The projected release has **27 public claims, 9 numeric observations, 22 source evidence records and 44 geography records**. Five IMD rainfall observations end **23 September 2026**; CWC's two monitored-reservoir values are **10 September**; the DCA prices are two separate calendar dates in 2025 and 2026. The completed **June** rank comes from IMD's June summary and does not rank the ongoing June–September season. The 177 Karnataka taluks are administrative declarations, not measured losses or delivered aid. A 26 July flood operation and 1 August flood-funding approval concern separate places/stages. The AI Author outlook remains conditional and low confidence.

Sources, calculations and G12 claim metadata passed an independent agent audit (`reporting/g12_independent_source_review.md`); the G13 media/markets desk and separate source audit are at `reporting/g13_media_voices.md`, `reporting/g13_markets.md` and `reporting/g13_independent_source_review.md`. A separate public-copy audit passed after corrections (`reporting/g13a_public_copy_review.md`). No human field reporting, Marathi translation review, photographic license or stock-market causation review is claimed.

## Checks actually run

- Approved-data validation passed; 80 Python tests passed; Astro check covered 45 files with zero errors/warnings/hints; static root, compact and GitHub-prefix builds generated **131 HTML pages** each. Pagefind indexed 131 pages.
- Chrome browser journeys: **131/131 at root** and **131/131 at GitHub repository prefix**, including 360/768/1440 dark/light opening screenshots, mobile navigation, source routes, search, downloads, no-JavaScript content and no horizontal overflow. Root screenshot/report artifacts are `artifacts/qa/g11/g13a-fixed-*`; prefix artifacts are `artifacts/qa/g11/g13a-prefix-*` (local QA paths, not public assets).
- Axe WCAG A/AA plus best-practice sample: **14 route/viewport/theme cases, zero violations after fixing chart contrast**. The initial scan exposed 14 contrast nodes in the pale chart on a dark section; these were corrected and the scan rerun. This is automated sampled testing, not a full manual screen-reader/WCAG certification.
- Journalist CSVs were regenerated with formula-safe cells. Both host-profile ZIPs and a journalist ZIP were regenerated. `release/site-github.zip` contains the GitHub-prefix build; `release/site-compact.zip` is root-path drag-and-drop output. The host ZIPs each contain 296 files. Exact per-file hashes are in `release/site-github-summary.json` and `release/site-compact-summary.json`.

## Known gaps and next checkpoint

The coverage report at `state/COVERAGE_AND_FRESHNESS.md` remains the precise scope statement. State/district water readings, current household-service outcomes, groundwater, 2026 water-caused crop/earnings/stock effects and delivered Karnataka aid are not verified. A geographic boundary map is held pending rights and border portrayal review. The next G13b task is a source-linked typographic press collage with verified reported voices, followed by a five-gate company/market evidence interaction. Any such public copy must pass the pending independent review and fresh browser/accessibility checks before a second live push.

**Local preview:** `python -m http.server 8000 --directory dist-compact` then `http://127.0.0.1:8000/`. **Reviewed update route:** follow `docs/UPDATE_PLAYBOOK.md`, regenerate approved data, run checks/build/export/package, then push the scoped commit to the existing GitHub Pages branch. There is no background updater or secondary deployment.
