# IMD cumulative district rainfall: candidate adapter

Source: [India Meteorological Department cumulative district rainfall page](https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C). The adapter also uses the [IMD API documentation](https://mausam.imd.gov.in/imd_latest/contents/api.pdf) only to identify the provider's district `OBJ_ID` namespace; the parsed observations come from the displayed page's embedded `dataProvider.areas` JSON. No downloaded JavaScript is executed.

## Reproduce

```sh
python -m pipeline.sources.imd_cumulative
python -m unittest tests.test_imd_adapter -v
```

The command permits only the exact HTTPS page, rejects redirects, imposes a 15-second timeout and a 2 MB response limit, and requires HTML/UTF-8 and expected product structure. It writes a SHA-256 named source snapshot under ignored `data/raw/imd/` and an immutable, unapproved candidate under `data/candidates/imd/`. To parse an already retrieved official HTML file without network access:

```sh
python -m pipeline.sources.imd_cumulative --from-file data/raw/imd/FILE.html --retrieved-at 2026-09-24T06:15:01Z
```

Add `--compare path/to/previous-candidate.json` to write a semantic diff. The diff ignores retrieval-only metadata and HTML formatting; it identifies page-period, row, value, missingness and source-hash changes. This adapter never writes `data/approved/`, public assets or release state.

## Retrieved candidate, 24 September 2026

The official page displayed a cumulative start of **1 June 2026** and a daily/date label of **23 September 2026** when retrieved at **2026-09-24T06:21:19Z**. The exact within-day cumulative cutoff hour and normal baseline period were not stated on this page, so the candidate records date labels and leaves those details unknown. The page does not provide a separate publication timestamp. The response SHA-256 was `cebad46abd11197515c01bb22dec449471201710a8cb409a50bb35e5627f6d46` (255,963 bytes). Corrected candidate: `data/candidates/imd/2026-09-23-cebad46abd111975-20260924062119376400.json`.

Two earlier development candidates, ending `20260924061501324127.json` and `20260924061554741512.json`, used the same raw source but incorrectly assigned the current page's 2026 start date to 33 older rows. They remain immutable for the audit trail and **must not be approved**. The corrected candidate keeps each old `source_row_date`, sets its `observation_period` to null, and flags it `older_row_date`; the source does not establish its cumulative start date.

Of **761** IMD district rows, **728** carry the displayed 23 September 2026 date; **723** of those have numeric values. **31** rows say “No Data” and are represented by null values, never zero. **33** rows have older row dates (2023–2025), including seven with numeric values; all are flagged and must be excluded from any current-date aggregate or current map. IMD IDs are stored as `imd_district:<ID>`. No LGD match, administrative boundary, state assignment or national coverage percentage is claimed.

Two rows have a material mismatch between the published departure and calculation from displayed rounded totals: IMD IDs **660 (Kargil)** and **703 (Leh and Ladakh)**. Both retain IMD's published percentage and carry `published_departure_arithmetic_mismatch`. The difference may involve provider calculations from unrounded values or source errors; this adapter cannot resolve it. A reviewer should inspect those records before publication.

## Approval boundary and limits

This is **candidate data, not an approved public observation**. The source's district IDs and names are not a reviewed join to the current administrative inventory. The page offers no explicit normal-period metadata here. Rows with older dates are not representative of the page's current cumulative period. A separate source/methodology reviewer must assess the provider, rights, geographic crosswalk, period convention, missingness, arithmetic flags and any proposed aggregate before approving a public release. The existence or severity of a drought cannot be inferred from this adapter alone.
