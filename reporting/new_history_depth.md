# Historical rainfall comparator: what the same IMD series can actually show

Internal desk memo, 24 September 2026. Status: **candidate for independent source, calculation, rights and editorial review**, not approved public data. This work covers precipitation only; it does not estimate water available to people, agriculture or industry.

## Source and reproducibility

Primary source: India Meteorological Department (IMD), Climate Research & Services Pune, [all-India and homogeneous-region monthly rainfall table](https://www.imdpune.gov.in/cmpg/Product/homo.html). Local, nonpublic snapshot: `data/candidates/history/imd-homo-2026-09-24.html`, retrieved 24 September 2026, 136,001 bytes, SHA-256 `6d27dc1a012e1abf4eedd682afc53a6f38984cb5f11c976452e83afb37fc71fb`. Its five tables run from 1901 to 2025 with one row for each year and a `(1971-2020) NORM` row. The source calls the region **South Peninsula (10 sub-divisions)**; do not replace this footprint with selected present-day southern states or the smaller six-subdivision IITM reconstruction.

`data/candidates/history/calculate.py` parses this exact snapshot with decimal arithmetic and writes `computed_summary.json` in the same ignored directory. It asserts all 125 years from 1901 through 2025 have numerical June–September values in each table. Selected-year calculations and the source hash are retained there. The HTML offers no visible table revision timestamp; retrieval is not observation or publication time. IMD's separate [June–September table](https://www.imdpune.gov.in/cmpg/Product/Rainfall_Data.html) reproduces seasonal totals, but it shares an IMD evidence chain and is not independent observational corroboration.

## Same-footprint, completed-season contrast

All values below sum the June, July, August and September **actual millimetres** printed to one decimal on the same IMD page. The comparison is 1 June–30 September in each year. The South Peninsula normal is 161.0 + 204.5 + 190.6 + 160.0 = **716.1 mm**, using the displayed 1971–2020 normal values. Departures use `100 × (actual/716.1 − 1)`, rounded to one decimal.

| Completed season | South Peninsula actual | Calculated departure | India actual | Calculated India departure | Meaning |
|---|---:|---:|---:|---:|---|
| 2002 | 466.9 mm | −34.8% | 687.2 mm | −20.9% | Both regional and national totals were far below their respective normals in this series. |
| 2009 | 681.6 mm | −4.8% | 709.1 mm | −18.4% | A dry national aggregate did not imply an equally dry southern regional aggregate. |
| 2025 | 787.2 mm | +9.9% | 935.7 mm | +7.7% | A recent higher-rainfall completed season, useful counterexample to an assumed monotonic decline. |

The **India normal** summed from displayed monthly values is 868.5 mm; some IMD products publish 868.6 mm due to unrounded spatial values. Do not combine an actual total from this table with a denominator from a different product and present the decimal as exact. The percentages above are calculations from *displayed* monthly values; IMD's published departure may differ by 0.1 percentage point after rounding or revisions. For 2002, the South Peninsula source row prints June 136.4, July 89.3, August 172.3 and September 68.9 mm. For 2009, it prints 110.4, 221.8, 155.7 and 193.7 mm. For 2025, 156.7, 201.0, 250.4 and 179.1 mm. These are exact source locators: `homo.html` → `South Peninsula (10 Sub-divisions) Rainfall` → year rows and the `(1971-2020) NORM` row.

This is a meaningful narrative contrast, not a causal explanation: a country-wide anomaly can hide different regional seasons. In particular, 2009 cannot stand as a generic illustration of equally severe southern rainfall deficit. The record also cannot establish household consequences, crop loss or state action without separate contemporary evidence.

## Rank audit and why it is withheld from the 2026 comparison

The script finds no blank June–September monthly cells in the 125 displayed 1901–2025 years. Sorting these one-decimal *completed-season* totals low to high, using competition rank `1 + number strictly lower`, yields South Peninsula **2002 = 2/125**, **2009 = 53/125**, **2025 = 94/125**; all-India **2002 = 2/125**, **2009 = 4/125**, **2025 = 86/125**. These are candidate arithmetic descriptions of the current HTML series, not hydrological drought or impact ranks. Completeness of printed cells alone cannot prove station-network stability or measurement uncertainty, and the source provides no visible per-year coverage or revision history. Use rankings only if a separate reviewer verifies extraction, region definition and tie handling, and an editor accepts those limitations. A selected-year exhibit needs no rank.

**No 2026 season rank is defensible yet from this table.** The approved 2026 IMD regional graphic ends **23 September**, whereas every historical June–September row includes 24–30 September. The displayed 2026 South Peninsula −25.7% through 23 September also uses a cumulative daily normal, not the full-season 716.1 mm denominator. Comparing either number with the completed-season −34.8% for 2002 would silently mix cutoffs. A same-cutoff 1901–2025 daily regional series, with a common geography and normal, is needed, or wait for IMD to publish the completed 2026 season. A June–August comparison could be built only after verified 2026 monthly totals for the same IMD homogeneous region are sourced, reconciled and reviewed. No such current-year three-month series has been approved here.

IMD's [June 2026 Monthly Climate Summary](https://www.imdpune.gov.in/cmpg/Product/Monthly_Climate_Summary/Monthly_Clim_Summary_6_2026.pdf), p. 1 and the table on p. 3, reports **102.5 mm** all-India June rainfall against 165.3 mm normal and describes it as the sixth-lowest June since 1901. This is a **single completed month**, not the 2026 monsoon rank. The preceding homogeneous table's 1901–2025 June values contain five lower years, so the sixth-place statement is arithmetically robust at the 102.5 mm threshold, though the PDF's listed historical millimetres differ slightly from the current monthly HTML (for example June 2009 87.6 versus 87.5 mm), indicating revision/rounding or product differences. Cite the PDF's own scoped finding if used; do not splice its historical values into the HTML without reconciliation. The PDF also documents intense June events despite the low monthly aggregate (p. 4), useful context against a false implication that low monthly rainfall means no heavy rainfall occurred.

## Population, reconstruction and rights boundaries

The IITM 1813–2005 South Peninsular reconstruction and a separate six-subdivision series have **different regions, baselines and station methods** from the IMD 10-subdivision modern series. Keep them as separate historiographic material. No nineteenth-century event is ranked against this 1901–2025 IMD series; no 2002 population/rainfall quotient is a water-stress measure. The 2011 Census and 2026 population projections cannot be overlaid onto a meteorological region without a documented geographic crosswalk, and projected demand is not measured water use.

The IMD Pune site's [disclaimer](https://www.imdpune.gov.in/disclaimer.html) restricts reproduction of site data without permission. The source HTML, full derivative annual rows, maps and bulk download must stay outside public builds and journalist exports pending a rights decision. A few attributed facts in original reporting may be defensible, but this agent has not made that publisher/legal decision. The safest proposed public exhibit is **three short text cards or a small original annotation** giving the 2002, 2009 and 2025 completed South Peninsula values and the national 2009 contrast, each linked to the exact IMD table with the common period/baseline in the visible caption. Do not reproduce the full IMD table or imply 2026 belongs on the same scale.

## Review handoff

1. Independent reviewer re-extracts the three source rows and normal from the cached HTML and repeats `actual / normal` arithmetic without using `calculate.py`; record any disagreement. Re-check a fresh original URL for later revisions before promotion.
2. Publisher/editor determines acceptable short factual quotation versus prohibited data reproduction under the IMD notice; withhold charts/exports until resolved.
3. If 2026 same-cutoff context is needed, obtain a legitimate IMD daily homogeneous-region series or a complete revised 2026 September release. Specify observation cutoff and footprint, and do not turn a historical frequency into a recurrence probability.

**Tests actually run:** parser assertions for five tables × 125 years, exact source SHA-256 check, decimal sums and ranks for selected years, and manual source-row spot check. **Not run:** independent analyst replication, a station-coverage audit, historical-impact source review, rights approval, or a full 2026 same-cutoff comparator.
