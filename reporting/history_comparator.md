# Completed southwest monsoon comparator: IMD South Peninsula

Research/calculation note, 24 September 2026. This is an internal source note for a narrowly defined, **completed June–September** comparison. It does not establish a 2026 rank, water shortage, or demand pressure. The two IMD pages below are one provider/evidence chain, not independent corroboration.

## Source snapshot and exact records

- Provider and scope: India Meteorological Department, Climate Research & Services, Pune, [all-India and homogeneous-region monthly rainfall HTML](https://www.imdpune.gov.in/cmpg/Product/homo.html), **South Peninsula (10 sub-divisions)** table, actual monthly precipitation in millimetres. Retrieved by HTTPS `curl -L` on 24 September 2026. Full response-body byte count **136,001**; SHA-256 `6d27dc1a012e1abf4eedd682afc53a6f38984cb5f11c976452e83afb37fc71fb`. The temporary raw snapshot is `/tmp/iww_imd_homo.html`; it is excluded from publication and is not a durable committed snapshot. Re-fetch and rehash for any public update to detect revisions.
- Table's `(1971-2020) NORM` row, June/July/August/September: **161.0 / 204.5 / 190.6 / 160.0 mm** (source HTML line 595; annual normal is a separate 1127.2 mm).
- `2002 ACTL` row, same months: **136.4 / 89.3 / 172.3 / 68.9 mm** (source HTML line 697; annual actual is 798.4 mm).
- `2025 ACTL` row, same months: **156.7 / 201.0 / 250.4 / 179.1 mm** (source HTML line 720; annual actual is 1355.1 mm).
- A separate IMD [June–September rainfall table](https://www.imdpune.gov.in/cmpg/Product/Rainfall_Data.html), retrieved 24 September 2026,  SHA-256 `3d8ce01a22dd10f5b63f8174f94bebd50aba7fabaaffd7a5c857008b4d4c6062`, directly prints the **South Peninsula (10 sub-divisions)** 2002 row as 466.9 mm and −34.8%, and 2025 row as 787.2 mm and +9.9% (response HTML lines 690 and 713). This cross-check catches a transcription/arithmetic error, but the two pages likely derive from the same IMD data.

## Recalculation

Using decimal arithmetic and the same region/season/normal:

| Period | Actual June–September (mm) | 1971–2020 normal (mm) | Actual ÷ normal | Derived departure |
|---|---:|---:|---:|---:|
| 2002 | 136.4 + 89.3 + 172.3 + 68.9 = **466.9** | **716.1** | 65.2% | **−34.8%** |
| 2025 | 156.7 + 201.0 + 250.4 + 179.1 = **787.2** | **716.1** | 109.9% | **+9.9%** |

Formula: `100 × (sum(monthly actual mm) / sum(monthly normal mm) − 1)`, then round to one decimal. The completed-season 2025 total exceeds the 2002 total by **320.3 mm** on this regional series. A relative `68.6%` increase over 2002 can be calculated, but it is less clear than the millimetre comparison and should not be recast as water supply or demand. The distinct **October 2002** value is 164.9 mm; neither annual nor northeast-monsoon conditions can be inferred from June–September alone.

This supports a possible sentence: “In IMD's South Peninsula 10-subdivision series, the **completed June–September 2002 season** measured 466.9 mm, 34.8% below that table's 1971–2020 normal; **2025** measured 787.2 mm, 9.9% above the same normal.” Link the sentence directly to the IMD table and name the series, region, season and normal. This is an IMD reported/derived rainfall comparison, **not** an inference about 2026 household water access. Before publication, an independent reviewer should inspect the source and repeat the calculation, and an editor should confirm the public reuse approach below.

## Exclusions and publication constraints

- **2026 through 23 September is excluded.** The 2002 and 2025 totals include 24–30 September; a partial 2026 season must be compared only to prior years truncated at the same observation cutoff from the same daily footprint, or await a complete 2026 September. A June–August comparison may be possible once all 2026 month values and revisions are checked. No `rank of N` or rarity estimate follows from the two rows above.
- The IMD table's South Peninsula is a meteorological aggregate, not an administrative sum of southern states, a basin, or a service population. Do not join it directly to a projected state-population sum or treat rain as accessible water.
- The 1971–2020 normal is the table's current baseline. Do not blend percentage departures from older 1901–2000, 1951–2000 or 1961–2010 normals. The ratio here is computed from displayed one-decimal monthly values; exact underlying unrounded values may differ slightly.
- **Rights:** The same IMD Pune site's [disclaimer](https://www.imdpune.gov.in/disclaimer.html) states that data on the site are for information and should not be reproduced elsewhere without prior permission. A citation of a few factual observations in original prose differs from republishing its table or bulk dataset, but that distinction has not been cleared for this project. Hold any public reproduced chart/table or downloadable dataset from this series pending publisher rights review or permission. The source-link and internal calculation may remain in reporting records. Do not bundle the raw HTML in `dist` or journalist exports.
- The source page offers no stable publication timestamp or revision log in the inspected table. Retrieval date is **24 September 2026**; observation years are **2002 and 2025**; editorial review and deployment dates must be recorded separately. A later rebuild must not imply fresh observations.

## Verification and next action

Verification run: direct HTTPS retrieval of two original HTML tables, SHA-256 hashing, exact source-line inspection, decimal recomputation, and comparison with IMD's own separately displayed June–September totals/departures. No independent analyst calculation or rights approval has occurred. Next: independent review of this memo's extraction and arithmetic, then a rights decision before any public visualization or data export; separately obtain a same-cutoff daily series if a 2026 comparator is wanted.
