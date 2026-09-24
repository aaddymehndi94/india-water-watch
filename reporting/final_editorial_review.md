# Independent final editorial and rights review — 24 September 2026

**Scope.** Read-only review of the current Astro public-page copy, shared claim/chart components, approved publication snapshot, eight evidence records and existing independent fact/quality reports. This is **agent review, not human editorial approval or legal rights clearance**. I changed no public copy or approved data.

## Disposition

**Pass for the narrow, attributed public findings in the reviewed source after the copy correction below.** The current snapshot contains eleven claims, five dated IMD rainfall observations, eight approved evidence records and a 28-state/eight-UT directory. The homepage attaches its national and regional IMD statements to source-detail links, and the chart retains exact values, period, normal and un-recomputed regional-denominator caveat. The site does not convert rainfall departure into a drought, service, health, crop or loss finding. The six added access/response/outlook claims appear as attributed source records with date and scope; the NSO 2018, JJM 2024 and administrative 2026 numbers are explicitly kept apart. The 31 August IMD forecast is identified as a dated September outlook whose latest-issue status is unverified, not an observed outcome or an asserted current forecast.

### Correction closed in the integrated source

| Priority | Location | Finding and correction |
| --- | --- | --- |
| **P1 editorial contradiction — resolved** | `src/pages/corrections.astro` | The former sentence said this build had no approved current findings, contradicting the integrated snapshot. It now says no **earlier** public release/correction history is recorded and explicitly counts current public claims and observations. I re-read that source after the frontend edit. |

### Clarity improvements

- The earlier bare “reviewed” date in `src/components/ClaimBlock.astro` and `src/pages/sources/[id].astro` now reads “agent checked.” I re-read both edited source lines; this closes the deep-link review-identity ambiguity.
- The site has the full **route structure** but only a verified subset of reporting. State and UT pages are directory/coverage pages, not local briefings; district inventory, basins, reservoir, groundwater, river flow, water quality, economic outcomes, local public actions, recovery and a matched historical rank are unavailable. Preserve this language in release notes and hosting description. Do not market those routes as completed investigations.
- The public progress page copies `project/tasks.json` and test status at build time. It clearly labels these as a build snapshot, but the lead must rebuild after updating those records; a GitHub Pages workflow alone cannot make the page continuously live.

## Evidence and public-interest checks

- **National framing:** No “worst year,” India-wide crisis verdict, district inference, population-at-risk total or famine prediction appears in the reviewed public copy. The homepage shows all-India 713.3 mm versus 837.7 mm through 23 September 2026, IMD's −14.9%, and regional disagreement. Its source links lead to exact locator and retrieval metadata. This is one IMD provider chain, not independent corroboration of water stress.
- **Comparability:** The regional IMD percentages are attributed, with the missing cumulative normal denominators made visible. No historical rank, district measurement, service inference or synthetic series is published. State/UT slugs are correctly marked internal and LGD joins pending.
- **Outlook:** The forecast is separated from observed rainfall and conditional scenarios. The current-card area says a later issue has not been checked. No probability, impact forecast or expiry claim beyond the September validity month is invented.
- **Response and access:** The JJM financial release is separated from spending and outcomes; reported tap connections are separated from reliability/quality. The 2024 functionality claim identifies sampled declared-covered villages and tested-sample microbiology, and its limitations remain attached. The 2018 survey is not styled as a 2026 service observation.
- **Practical information and sensitive reporting:** The site directs readers to current local authorities instead of giving unverified contacts, clinical advice or water treatment instructions. It publishes no accusation of misconduct, no interview claim, no protected person's location, no political score and no invented byline. The `journalists` page says its document questions were not sent.
- **Rights and privacy:** Public source records link to originals and reproduce limited numerical facts, not the official GIFs/PDFs or government marks. The normalized CSV and SVG contain IDs, dates, values and caveats. No private reporting notes, raw source documents, candidate districts or obvious personal data were found in the reviewed public copy. This is an editorial scope check, not legal permission to republish bulk third-party material.
- **Review identity:** `/about/` accurately discloses AI assistance and lack of configured correction contact. It does not invent a publisher identity. A real publisher name/contact and a naming-conflict check remain publication operations before presenting the project as a settled independent outlet.

## Checks and limits

I read the relevant page/component source and the eleven claim/eight evidence records, and compared the integrated copy with `reporting/final_fact_review.md` and `reporting/final_quality_review.md`. I did not run a new build, browse a new source version, inspect every byte of the generated ZIP, perform a human interview or grant rights clearance. The separate fact report independently checked official-source snapshots and arithmetic; the separate quality report tested static browser output. Final bundle, release manifest and GitHub deployment must be checked against the post-correction build, and this review must not be represented as human sign-off.

**Next action for lead:** Regenerate both static profiles and exports after these copy edits, confirm the final build still excludes internal files, and state the actual verified subset and outstanding coverage gaps in the release report.
