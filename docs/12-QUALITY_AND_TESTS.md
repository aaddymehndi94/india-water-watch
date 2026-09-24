# 12 · Quality gates and test strategy

The acceptance matrix in `project/acceptance.csv` is the executable work queue for QA. The starter tests exercise reference helpers and packaging rules only; they do not prove the site or reporting exists. Codex must implement production tests and attach real evidence to every completed requirement.

## 1. Data and units

Test rainfall departure with zero/missing normal; correct mm-to-volume units; ratio-of-sums aggregation; unweighted-average failure; missing versus observed zero; source rounding versus exact derived values; valid extraction ratios above 100%; inconsistent storage units; source-footnote changes; non-finite numeric values.

Test schema validation for every record type; foreign-key references; orphan claims; invalid timestamps; wrong geography; zero-denominator behavior; duplicate observations; revisions; unknown projection vintage; inherited fake current dates; traceable source locators. Reject a successful HTTP response that is an error page.

## 2. Comparability

Fixture tests must deliberately mix partial/full seasons, normal periods, changed boundaries, reservoir inventories, national/regional figures and population definitions. The comparison should block or explicitly separate these, not output a precise rank. Test tie handling and incomplete historical years; verify baseline/cutoff rules independently.

Check all public maps against tables from the same snapshot. Test renamed/split districts, aliases, unmatched units, island territories, basin intersections and projected-versus-measured populations. No fuzzy name match may silently resolve two plausible units.

## 3. Source and editorial support

Open exact original sources for all headlines, featured charts, record claims, public safety guidance, official declarations and material economic figures. Validate date/geography/locator. Sample routine cells after automated complete consistency checks, and enlarge the sample on any failure. A working URL is not proof of support.

Check every public claim ID's evidence chain; distinguish measurements from attributed reports; verify quotes and translations; identify syndicated duplicates; reject invented field reporting/bylines/endorsements; maintain counterevidence and correction history. Review neutral presentation of institutions and political matters without verdict/ranking.

## 4. Updates and failures

Repeat an identical refresh and assert identical normalized output; preserve observation dates; generate no fake changed story. Simulate revised historical data, withdrawn notice, expired forecast, stale annual data, timeout, permission error, malformed PDF/table and a changed admin boundary. Ensure approved data is never overwritten by failed candidates. Verify dependent prose, charts, exports, search and feeds all update or are explicitly withheld.

## 5. Browser and accessibility

Use Playwright and an appropriate accessibility scanner, with manual keyboard/reading checks. Automated scans cannot establish full WCAG conformance. Target WCAG 2.2 AA; test contrast, names/roles, focus, skip links, headings, dialogs, hover-independent information, reduced motion and 200% zoom.

Run actual journeys at mobile/tablet/desktop. No horizontal page overflow at 360px, except intentional internally scrollable tables. Ensure chart values can be reached by keyboard/table, color is not the only cue, map selection is reversible, browser back/forward restores filters and no-JS pages retain core meaning.

## 6. Visual design

Review screenshots for hierarchy, legibility, legend position, units, annotations, mobile chart labels, source-link prominence, long titles, empty states and content rhythm. Recheck both light/default design and any secondary mode. Do not equate an attractive hero with a polished publication.

Two independent critique passes should produce specific defects and fixes. The reviewer reports observed quality, not a fabricated “95/100 journalism score.” Screenshots must be from the actual built site, not generated mockups.

## 7. Performance and scalability

Proposed engineering budgets, not claimed benchmark results: initial compressed JavaScript under 200 KB on the landing page; initial transfer under 1 MB excluding user-triggered downloads; defer district geometry and search; no external runtime API request required to read the briefing. Document justified exceptions.

Use mobile-throttled synthetic tests and report environment, runs and median, not fabricated real-user metrics. Aim for good Core Web Vitals, but distinguish lab estimates from field results. Test large data/filtering paths and memory on representative low-end conditions.

## 8. Security, rights and privacy

Secret scan source and dist; inspect build output allowlist; sanitize external text and link schemes; test injection payloads in titles/news/CSV/JSON; reject unsafe redirects and private-network fetch targets; ensure no external MDX execution. Verify no untrusted-PR deployment secrets, no unauthorized analytics and no private notes in search.

Review rights for normalized data, geometry, photos, quotes and exports. Do not bundle copyrighted whole reports by accident. Verify public-contact fields and safety guidance are current. Sensitive claims require actual human review and right-of-reply status when appropriate.

## 9. Hosting and portability

Build root and `/<repo>/` profiles. Serve over HTTP and test direct deep links, refresh, 404s, assets, sources, search, print and downloads. Inspect manifest hashes and ZIP structure. Test compact file count/asset sizes. Confirm no dependency on a development server or runtime backend.

## Publication blockers

Any fabricated data, unsupported headline, untraceable quote, false currentness, disguised forecast, materially incompatible comparison, synthetic fixture in production, secret/private-data leak, unlicensed material, broken core navigation or unreviewed sensitive allegation blocks the affected publication. Fix or withhold; never mark it passed for schedule pressure.

## Report statuses

Use `passed`, `failed`, `not_run`, `not_applicable`, `human_review_required`. Every pass points to a real test/audit artifact and the reviewed snapshot. A missing artifact is not a pass. Tests passing before a content revision do not certify the revised release.
