# G15 independent source and method review — 24 September 2026

**Role and disposition:** Read-only independent agent review of the G15 subnational research memo. The original sources were fetched anew with normal TLS verification. No public claim, source record, map, page or release was edited. **Data/method decision: yes, a narrowly worded historical Karnataka 2024 survey fact is supported. Publication/rights decision: conditional, because the JJM website expressly requests prior permission for reproduction and inbound links; this review is not that permission or legal clearance.** The district rainfall layer is **not cleared** for a current district map or a blanket 24 September claim.

## Originals and locators

| Original | Independent retrieval and fingerprint | Relevant locators |
| --- | --- | --- |
| [JJM, *Functionality Assessment of Household Tap Connections: State Report 2024 — Karnataka*](https://jaljeevanmission.gov.in/sites/default/files/2025-12/FHTC_Karnataka_State%20Report.pdf) | HTTPS 200, `application/pdf`, 59 pages, 9,427,483 bytes; SHA-256 `ef579651ee96899d92060a7dab7555a7990c531bab0428e829cd81390721912a`; fetched 2026-09-24 10:50:15 UTC. HTTP Last-Modified 2025-12-08 11:33:27 GMT and PDF creation 2025-10-09 13:05:51 IST are file metadata, not service observation dates. | Printed pp. 3 (2022/2024 noncomparability), 5–6 (definitions/factsheet), 11–14 (sample/measurement), 18–19 (weights), 20 (inconsistent administrative snapshot), 23–26 (coverage/Koppal values). PDF printed p. 26 corresponds to zero-index page 25. Parsed text was checked against the rendered PDF p. 26 table. |
| [IMD, All India District Rainfall Statistics, cumulative](https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C) | HTTPS 200, `text/html`, 255,416 bytes; SHA-256 `d9c8fb1e4f299a14527cec166a74964e4ff51cd2da8b116a04b91d3025b1f7e4`; fetched 2026-09-24 10:50:15 UTC. | Embedded `dataProvider.areas` JSON, each `balloonText` row's `Date`, `Departure`, `Actual`, `Normal`; page control says cumulative from 01-06-2026. The page does not identify the normal-period years or exact end hour. |
| [JJM Website Policies](https://jaljeevanmission.gov.in/website-policies) | HTTPS 200, SHA-256 `7c4d61e5a1b6413fc45bee390a02be67730d54741b44009550e54aca35bc5105`; fetched 2026-09-24 10:50:16 UTC. | “Hyperlink Policies,” “Terms Of Use,” “Copyright Policy.” These request prior permission for incoming hyperlinks and partial/full reproduction and source acknowledgment. |

The PDF source URL path contains `2025-12`, but the report itself dates fieldwork **July–October 2024** and fixes the Har Ghar Jal (HGJ) village sampling frame at **1 May 2024** (pp. 11–12, 18). These dates must not be collapsed into “current,” “September 2026” or the file metadata date.

## JJM claim audit

The factsheet (printed p. 6) has Karnataka household estimates of **96.4% working taps**, **91.1% supply according to the scheme schedule**, and **72.6% in the report's adequate quantity category**. The glossary (p. 5) defines working as water received through the tap in the prior week; regularity is receipt per schedule, which does not mean uninterrupted or daily supply. The survey covers only villages recorded as HGJ at the 1 May 2024 frame, excluding villages with fewer than 20 households; its Karnataka sample is **744 villages, 8,928 interviewed households, 31 source-named districts** (p. 23). Household percentages are **weighted estimates**, not `numerator ÷ 8,928` raw fractions: p. 19 specifies inverse selection-probability weights at village and household level. The report does not give an independently auditable indicator-specific unweighted denominator or microdata for each of these three percentages. Never describe these percentages as the share of all Karnataka homes or all rural homes.

Koppal's district row on printed p. 26 shows **48.9% adequate, 17.9% partially adequate, 33.2% inadequate** in the estimated quantity category; the three reported rounded shares add to **100.0%**. Printed p. 24 lists **276 sampled households with piped-water-scheme taps** in Koppal, but p. 14 and p. 26 say flow was directly measured at **one household per hamlet/habitation**, then combined with supply duration (weekly estimate for non-daily service). The 276 is neither a flow-measurement count nor a disclosed denominator for the weighted 48.9%. The factsheet writes `≥55 LPCD`, whereas the quantity table writes `>55 LPCD`; use the report's unmodified category label “adequate quantity” until the threshold convention is reconciled. No district confidence intervals or microdata were verified; the method's nominal 273-household target is not achieved in several rows (e.g. Kolar 73, Bengaluru Urban 96, Uttara Kannada 228). Do not rank districts by small differences.

The report itself warns against direct 2022-to-2024 comparison because sampling, season and testing differed (foreword p. 3). The chapter 4 administrative snapshot has a visibly suspect `Total FHTC: 3` for Karnataka (p. 20); that cell was **not** endorsed or used. It does not invalidate the separately described chapter 5 sampled survey on its own, but warrants restricting the claim to the checked survey indicators.

**Supported public wording, subject to the rights decision:** “In a July–October 2024 survey limited to villages already listed as Har Ghar Jal, Jal Jeevan Mission estimated that 96.4% of sampled-frame Karnataka households had received tap water in the previous week, 91.1% received it according to the scheme schedule, and 72.6% fell in its adequate-quantity category. These are separately weighted estimates; they do not measure September 2026 supply.” The lead may shorten this if the sample-frame/date qualification stays adjacent to the numbers. A Koppal callout may say “The same 2024 report estimated 48.9% in its adequate-quantity category for sampled-frame Koppal households” with the flow-method and precision caveats nearby. This is **not** evidence of a current Koppal shortage, a 2026 monsoon effect, a statewide service level, or a district trend.

**Mapping:** the PDF gives names, not stable administrative IDs or a polygon/boundary vintage. Use Koppal only as a source-native named district callout. Neither name matching to a current polygon nor a district choropleth is approved. In particular, the JJM service estimate cannot be joined to 2026 IMD rainfall to imply causation.

**Rights:** The policy page says material may be reproduced after permission and separately requests prior permission for incoming hyperlinks. A brief original paraphrase of factual findings is a lower-risk editorial use than copying the PDF table, artwork or substantial text, but I cannot certify it as permitted under that policy. Do not mirror the report, embed PDF screenshots, replicate its tables/charts, or label rights cleared. Record a publisher/legal decision for the source link and brief factual quotation/paraphrase before treating the item as publication cleared; no external rights request was made by this reviewer.

## IMD district row audit

Independent JSON extraction found **761 entries with 761 unique IDs and titles**, with these embedded row dates:

| Row date | Numeric actual/normal rows | Explicit `No Data` | Total |
| --- | ---: | ---: | ---: |
| 2026-09-24 | 722 | 5 | 727 |
| 2026-06-01 | 1 | 0 | 1 |
| 2025-10-08 | 1 | 0 | 1 |
| 2024-05-24 | 6 | 0 | 6 |
| 2023-07-03 | 0 | 26 | 26 |
| **Total** | **730** | **31** | **761** |

Thus **722/761** entries are numeric and dated 24 September, **8** are stale numeric rows and **31** are explicit missing entries, not zero rainfall. The eight stale numeric IDs are Nagapattinam `47` (2026-06-01), Sribhumi `340` (2025-10-08), and Gangtok `449`, Mangan `473`, Namchi `450`, Gyalshing `455`, Cooch Behar `11`, Purba Bardhaman `283` (all 2024-05-24). The 26 `No Data` rows dated 2023-07-03 must not be interpreted as current observations.

For each numeric row, I recomputed `100 × (actual_mm / normal_mm − 1)` from the displayed millimetres and compared it with IMD's displayed whole-percent departure. Two rows diverge by more than one percentage point:

| Source ID and name | Displayed actual / normal | Displayed departure | Recomputed from displayed values | Difference |
| --- | --- | ---: | ---: | ---: |
| `660` Kargil | 21.6 / 10.1 mm | +97% | +113.861% | +16.861 percentage points |
| `703` Leh and Ladakh | 58.1 / 25.7 mm | +123% | +126.070% | +3.070 percentage points |

Even allowing each displayed millimetre value to represent a true value within ±0.05 mm (ordinary one-decimal rounding), the plausible Kargil departure is **112.315%–115.423%** and Leh/Ladakh **125.437%–126.706%**. Neither range explains the displayed departure. I cannot determine whether IMD has unshown source values, a stale percent field, or another processing issue. The page links `../imd_latest/contents/district_shapefiles/india_gj_2024.geojson`; neither geometry reuse rights nor a current administrative crosswalk/disputed-border treatment was cleared. No map approval follows from the fact that 722 rows share the date.

**IMD disposition:** hold the district map and any all-district “through 24 September” wording. A future adapter could present a source-native table of strictly filtered 24 September numeric rows with per-row dates and an anomaly flag, after reconciling the IMD definition, normal period and district ID/boundary use. Exclude both arithmetic anomalies from derived comparisons until IMD explains or corrects them. Rainfall departure is not a household-water or drought diagnosis.

## Checks, limitations and next action

Checks actually run: independent verified-HTTPS GET and SHA-256 for three originals; `pdfinfo`, `pdftotext -layout`, direct visual inspection of rendered PDF p. 26; PDF locator/sample-method check; extraction/date/missingness/ID audit of all 761 IMD JSON rows; recomputation of all numeric departures; one-decimal rounding envelopes for both exceptions. No source data, public page or shared state was modified. The cached originals and rendered image used in this review are in `/tmp/iww-review-*`, outside the repository.

Not verified: exact survey indicator-level denominators, design-adjusted district uncertainty, independent 2026 household service observations, IMD district normal climatology years/end hour, IMD geometry license and boundary crosswalk, publisher/legal permission under JJM's hyperlink/reproduction policy. No human field reporting or human review is implied.

**Next action for lead:** If the publisher's existing rights policy permits a brief original fact statement and source link despite JJM's stated request, promote the narrowly scoped historical Karnataka fact with the survey frame/date beside the numbers; otherwise hold it pending a rights decision. Keep Koppal as a cautious named source-native district callout at most. Keep the IMD district map on hold and implement per-row date/anomaly filtering before any district rainfall publication.
