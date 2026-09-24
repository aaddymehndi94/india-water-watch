# G10 data and build review · 24 September 2026

Scope: revised public progress candidate. This is a lead-engineer structural and provenance review, not a human editorial sign-off or an independent source audit. Independent source review is recorded separately in `reporting/g10_fact_review.md`.

## Approved snapshot

- The generated publication contains **17 public claims, 7 numeric observations, 43 geography entries and 11 cited evidence records**. Five rainfall observations end 23 September 2026; two CWC monitored-reservoir observations have status date 10 September 2026. The source periods are not relabeled by the 24 September build.
- Karnataka's 22 September gazette order is a public **reported action claim**, not a water observation. The approved wording distinguishes its 53 additional declared taluks, relief authorization and directed crop-loss survey from unverified delivery/outcomes. Earlier referenced declarations are not summed into a statewide total.
- The IMD forecast has a separate validity end of 30 September 2026 and no `observedThrough` watermark. Its 31 August publication is date precision, as is the Karnataka order. Source projection and CSV export carry `validityEnd` distinctly.
- Brief historical completed-season claims for 2002, 2009 and 2025 use the preserved IMD monthly product. There is no 2026 historical rank or bulk historical source export.

## Checks performed by lead

- `python -m tools.validate_approved`: passed after each promotion.
- `python tools/validate_starter.py`: passed.
- `python -m unittest discover -s tests -q`: 80 tests passed, including forecast validity versus observation and order publication-date precision assertions.
- `pnpm check`: 43 Astro/TypeScript files, zero errors, warnings or hints.
- Root and GitHub `/india-water-watch/` static builds: 110 HTML pages and Pagefind index in each profile.
- CWC cached PDF SHA-256 `47b7b3779abf4107cb8b1349456e5ace4d7e3fe7fe8ab1a8248faaeee7aabec7`; Karnataka gazette SHA-256 `f1453449104e8b96098c931fdf724265740b89e8c430284e69278c035fdbb6d5`. Local candidate snapshots are excluded from static packages.
- Journalist CSV generation completed. The exports are formula-safe and include source publication/retrieval dates and separate forecast validity.

## Coverage limits

No approved state rainfall, district numeric water data, basin flow, groundwater trend, September household service measure, measured crop loss or economy estimate is present. The CWC bulletin is for a named monitored reservoir cohort and is older than the rainfall graphic; its 17 September successor was listed but the official PDF returned 404. Sources that could not be checked were not filled with invented values.
