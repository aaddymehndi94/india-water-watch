# G16 independent IMD district refresh review — 24 September 2026

**Disposition:** Confirmed source revision, not a parser artifact. The official [IMD All India District Rainfall Statistics cumulative page](https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C) itself changed Nagapattinam (`id 47`) from a numeric row dated `2026-06-01` in the 10:50 UTC snapshot to a numeric row with the literal invalid date `0000-00-00` in the 11:34 UTC snapshot. The values and displayed departure did not change. Do not treat the new row as dated 1 June or 24 September; mark its observation end date **unknown** and exclude it from dated/current district subsets.

## Source, retrieval, exact change

| Source snapshot | Retrieval / response | SHA-256 | Row 47 embedded `balloonText` date and values |
| --- | --- | --- | --- |
| Earlier independent snapshot, same URL | 2026-09-24 10:50:15 UTC; HTTPS 200, `text/html`, 255,416 bytes | `d9c8fb1e4f299a14527cec166a74964e4ff51cd2da8b116a04b91d3025b1f7e4` | `Date : 2026-06-01`, `Departure : -40%`, `Actual : 39.7 mm`, `Normal : 65.9 mm`. |
| Fresh independent GET, same URL, verified TLS and no-cache request headers | 2026-09-24 11:34:47 UTC; HTTPS 200, `text/html`, 255,416 bytes; response Date `Thu, 24 Sep 2026 11:34:45 GMT`; no Last-Modified header | `5d1d35cb5f1bdbd62ffe11ad0e7854ff91aaafec37dce8298550d0e510baeb34` | **Literal source HTML:** `Date : 0000-00-00`, `Departure : -40%`, `Actual : 39.7 mm`, `Normal : 65.9 mm`. |

The relevant locator is the embedded JavaScript `dataProvider.areas` array, object with `id: "47"`, `title: "NAGAPATTINAM"`, and its `balloonText`. A line-by-line diff of both raw HTML snapshots shows the old Nagapattinam object removed from near the end and an otherwise identical object appended as the final array entry with only that date string changed. Object-wise comparison by ID found **one changed row out of 761**; all other row objects matched. Thus the parser did not invent or normalize `0000-00-00`. The source changed both the row's array position and its date; row order must not be used as a stable identity. The stable source-native key for this comparison is `id 47`, but this is not an approved administrative-boundary crosswalk.

The displayed numbers themselves are arithmetically coherent: `100 × (39.7 / 65.9 − 1) = −39.757…%`, consistent with the displayed rounded `−40%`. That does **not** restore a valid observation date. The page-level cumulative control says “From 01-06-2026”; it does not supply a valid end date to override a row's invalid embedded date. The live HTML has no source-level explanation for the revision, so its cause and intended date are unknown.

## Whole-page classifications from the fresh raw HTML

I independently extracted the JSON array with `json.JSONDecoder.raw_decode`, keyed rows by their source `id`, and parsed each row's embedded date and numeric/missing values. There are **761 total entries, 761 unique IDs and 761 unique titles**:

| Embedded date | Numeric actual and normal | Explicit `No Data` | Total |
| --- | ---: | ---: | ---: |
| `2026-09-24` | 722 | 5 | 727 |
| `2024-05-24` | 6 | 0 | 6 |
| `2025-10-08` | 1 | 0 | 1 |
| `2023-07-03` | 0 | 26 | 26 |
| `0000-00-00` (invalid/unknown) | 1 | 0 | 1 |
| **Total** | **730** | **31** | **761** |

Therefore this snapshot has **722 dated 24 September numeric rows**, **7 older dated numeric rows**, **1 undated numeric row**, and **31 explicit missing rows**. Earlier wording of “8 older numeric rows” is correct for the earlier 10:50 UTC snapshot but stale for the new source snapshot. The actual/normal values were not changed, so the numeric and missing totals stayed 730 and 31. The 26 `No Data` rows still carry `2023-07-03`; missing is not zero. The Kargil and Leh/Ladakh displayed-percent arithmetic anomalies identified in the G15 independent review remain unchanged in this one-row-only source revision.

## Rights and editorial caveat

The IMD page footer states © 2026 India Meteorological Department. Its [disclaimer](https://mausam.imd.gov.in/responsive/disclaimer.php) says the data can change without notice and are subject to scientific/technical uncertainty. The inspected pages do not provide an explicit bulk-data or map-geometry reuse licence. This review involved an ignored `/tmp/iww-g16-imd-district.html` working copy and did not copy the source HTML or linked `india_gj_2024.geojson` into the public build. It is an audit of a changing official source, not rights clearance to mirror its table or geometry. Per-row provenance and retrieval hash are necessary for any future publication of independently rendered facts. No district map or all-district current label is approved by this review; boundary matching, normal-period definition and exact cutoff remain open, along with the two arithmetic anomalies.

## Checks and next action

Checks actually run: independent verified-HTTPS fetch of the exact public URL; response-header/time and SHA-256 capture; direct comparison against the earlier raw source snapshot; source-object comparison for all 761 IDs; fresh row-date/numeric/`No Data` counts; row 47 departure arithmetic. No public data, pages, ledgers, shared state, release artifact or deployment was modified. This is an **agent review**, not human or legal review.

**Next action for lead:** Update any G16 wording/report that still says “eight older numeric rows” for the 11:34 snapshot to “seven older dated numeric rows plus one undated numeric row”; retain the earlier wording only when explicitly discussing the 10:50 snapshot. Keep row 47 as `date_unknown`/invalid with its exact source literal, do not silently inherit `2026-06-01`, and continue holding it out of 24 September district figures and the map.
