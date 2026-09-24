# G11 independent browser, accessibility and build review

**Reviewer:** independent quality-engineer Codex agent. **Status:** passed for the tested local release candidate; this is agent review, not human editorial review or a WCAG certification. **Reviewed snapshot:** `data/approved/publication.json` SHA-256 `6fb054552ffb09e9ebb07dfc893b267643b53c10b5d614a8308a3438b55efef4`, `claims.json` `f6403aa88a5e21b117d5ded499ff40650216c538cacefcd27991504333dca5e7`, `evidence.json` `1b7d8f758bc6d7819e59afbb3e5efe4e04179d29a0249432c82c1745424d7dee`. CSS SHA-256 `296fa0d09830f6826f93ff06c0bebca6d0ddef63ecc169bfa60e814f4f22f004`.

## Tests actually run

| Check | Result | Evidence |
| --- | --- | --- |
| Astro type/content check | 43 files, 0 errors, warnings or hints | `node_modules/.bin/astro check` console result, 24 Sep 2026 14:08 IST |
| Static root and `/india-water-watch/` builds | Both built 120 pages; Pagefind indexed 120 pages each | `artifacts/qa/g11/final-root-build.log`, `final-subpath-build.log`, Pagefind logs |
| Browser journeys, Chrome headless, 360/768/1440, dark/light | 131/131 checks each profile, 262/262 total; zero page errors and zero external runtime requests | `artifacts/qa/g11/final-root-browser-report.json`, `final-subpath-browser-report.json` |
| Axe-core 4.13.0 WCAG 2.0/2.1/2.2 A/AA and best-practice scan | 14 cases each profile, 28 total; zero violations after a fix | `artifacts/qa/g11/final-root-axe-report.json`, `final-subpath-axe-report.json` |
| Internal links, public-output paths and package sizes | 271 files each, 120 HTML pages, zero broken internal links, sensitive path hits or files above 25 MiB | `artifacts/qa/g11/final-root-asset-report.json`, `final-subpath-asset-report.json` |
| Targeted G11 paths and content | Root/subpath: 177 taluk text, AI Author assessment, 24 Sep weather and 17 Sep extended-range source pages, scenario claim anchor, no-JS explorer fallback all present | `artifacts/qa/g11/final-targeted-report.json` |

The root build is 2,475,402 bytes across 271 files; the repository-prefix build is 2,539,470 bytes across 271 files. Browser journeys covered direct route loads for overview, explorer, states, history, response, outlook, impacts, updates, sources, journalist desk, search, data status and about; 360 px overflow checks; search results; five journalist downloads; skip link; keyboard opening path; mobile menu; theme toggle and persistence; atlas selection/search/back navigation; and no-JS reading paths. The no-JS explorer now links to the CWC storage explanation and state directory while inert interactive controls are disabled. Reduced-motion mode was used throughout browser journeys; a targeted computed-style check found hero number animation `0s` under reduced motion and `0.85s` with normal motion.

I inspected actual browser screenshots at 360, 768 and 1440 px in both themes. The first-screen decorative hero now carries a visible **AI-generated illustration** badge; the figure caption states it is not a photograph, map or 2026 observation. Headlines, labels and primary navigation remain legible at mobile width. Additional route screenshots cover explorer, outlook, history, response and impacts at 360/1440 px. Files are under `artifacts/qa/g11/` with `final-root-` or `final-subpath-` prefixes.

## Defect found and fixed during review

Axe initially found `scrollable-region-focusable` on the horizontally scrollable rainfall chart at 360 px. The chart wrapper was given keyboard focus, a region role and descriptive accessible name in `src/components/RainfallChart.astro`; the root and subpath builds were rebuilt and rescanned. Both full scans had zero violations. An **incomplete** `aria-prohibited-attr` check on `.atlas-coverage` was then resolved by adding `role="group"`; a targeted axe rerun at 360 and 1440 px found zero violations and zero incomplete results for that rule (`artifacts/qa/g11/final-atlas-aria-report.json`). Contrast checks still returned incomplete results for text over image/complex layered backgrounds. I visually inspected the first-screen dark/light screenshots and found the hero, number card, badge and navigation legible; I cannot certify every text contrast ratio from that spot check.

## Security and release observations

The inspected production builds made no external runtime requests during homepage journeys. The static-link audit found no `javascript:` or local-host links, no missing internal assets, and no private/development directories in `dist`. A literal `@gmail.com` search hit in bundled Pagefind UI came from an upstream translator credit, not the publisher's private address. GitHub Pages workflow deploys only on `main`/manual dispatch, uses immutable action SHAs and minimal job permissions. These are bounded checks, not a dependency security audit or external-link verification.

## Limits and next action

Chrome headless was the only browser engine run. No physical device, screen reader, real-user performance, actual browser 200% zoom, external-link availability or live GitHub Pages smoke test was run in this review. Automated axe results cannot establish full WCAG 2.2 AA conformance. Source support and rights are covered by separate review, not this document. **Next action:** bind this report and the approved snapshot to the release gate, publish the reviewed GitHub Pages checkpoint, then smoke-test the actual hosted URL and record its deployment commit/time separately from source observation dates.
