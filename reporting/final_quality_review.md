# Final independent quality review

Reviewed 24 September 2026 against two isolated static builds made from the integrated source: a portable root build in `artifacts/qa/root-final/` and a GitHub Pages build in `artifacts/qa/subpath-final/`. Both were generated with Astro, indexed with Pagefind, and given a release manifest. This is an **agent review**, not human editorial or rights approval.

## Result

No release-blocking browser, navigation, accessibility smoke-test, or public-output leakage defect was observed in these snapshots. The tests below cover the generated files and actual HTTP-served pages; they do not certify source support, copyright clearance, or WCAG conformance.

| Check | Result | Evidence and scope |
| --- | --- | --- |
| Root and `/<repo>/` builds | Passed | `artifacts/qa/root-build.log`, `root-pagefind.log`, `subpath-build.log`, `subpath-pagefind.log`, and release manifest logs. Both generated 104 HTML routes. |
| Responsive route sweep | Passed | Chromium at 360 CSS px: all 104 routes in each profile returned 200, had one `h1` and one `main`, and had no document-level horizontal overflow. `artifacts/qa/final_browser_qa.json`. |
| Navigation and assets | Passed | Crawl reached 103 linked pages in each profile; no broken local links, missing assets, or links escaping the GitHub Pages base path. A direct state deep link returned 200 and an unknown route returned 404. |
| Mobile, tablet, desktop | Passed | Homepage at 360, 768 and 1440 CSS px had zero document overflow and zero page errors. Actual Chromium screenshots: `artifacts/qa/{root,subpath}-final-home-{360,768,1440}.png`; Explore at 360: `artifacts/qa/{root,subpath}-final-explore-360.png`. |
| Search and filter history | Passed | Query `rainfall` returned 21 matches (20 displayed by the interface); result URLs had the correct root or repository prefix. Atlas place selection restored `india` on Back and `imd:central` on Forward. |
| Downloads | Passed | CSV, JSON manifest and rainfall SVG returned HTTP 200 in both profiles with matching content types. The CSV contains period, date precision, cutoff convention, status, series, baseline, evidence, claim and source identifiers. All five approved CSV rows mark `periodPrecision=date` and explain that the IMD graphic gives calendar dates without a clock hour. |
| Keyboard and no-JS | Passed smoke test | First Tab shows the skip link; Enter then Tab reaches main content. The source detail disclosure opens with Enter. With JavaScript disabled, Explore retains two tables and nine body rows including source references. |
| Reduced motion and zoom | Passed limited check | `prefers-reduced-motion: reduce` gives `scroll-behavior: auto`. At simulated 200% CSS zoom, Explore had no document overflow at 768 and 1440 physical CSS viewport widths. This approximates browser text zoom; native browser zoom and full assistive-technology testing were not run. |
| Runtime dependencies and public-output scan | Passed spot check | Homepage requested only local HTML, stylesheet and favicon. Search made no external runtime request. Root build: 233 files, 1,523,588 bytes; subpath: 233 files, 1,563,833 bytes. No quarantine, fixture, raw, private, `.env` or state paths; no searched email, private-key or common token markers in text assets. Initial compressed JS assets total approximately 70 KB, though the homepage loads no JS. |

The root homepage HTML SHA-256 was `2b378b54b91ecbaa09bed2d6d3337b74177f23d9f6688de31cd6bb26ace60005`; the subpath homepage SHA-256 was `b655fd64aea947520f75fa16365461222cb3eef729193a56902132d8de82599e`. The full browser output and exact results are in `artifacts/qa/final_browser_qa.json`. This rerun included the revised source-date display, outlook copy, CSV date precision fields and source observation detail. The homepage hashes did not change because those edits affected other routes and downloads.

## Limits and follow-up

- No automated axe scan, complete WCAG 2.2 AA audit, screen-reader session, or mobile-throttled Core Web Vitals benchmark was run. Manual keyboard and layout tests cannot replace these.
- Source accuracy, data methods, rights and sensitive-claim approvals belong to the separate independent editorial/source reviews and genuine human review where required. This review only checked browser output and obvious leakage.
- The static server used for subpath testing mapped `/india-water-watch/` to the generated directory. The GitHub Pages deployment workflow itself was not executed by this reviewer.
- Final public deployment and remote response were not tested here.

To reproduce the browser run after serving `root-final` at `127.0.0.1:8770` and the subpath build at `127.0.0.1:8771/india-water-watch/`, run `node artifacts/qa/final_browser_qa.mjs`. The script writes `artifacts/qa/final_browser_qa.json` and screenshots.
