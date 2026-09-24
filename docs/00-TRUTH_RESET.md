# 00 · Evidence reset before design

## Why this comes first

The project began with a conversation that asserted a large 2026 southern rainfall deficit, a rare historical rank, and a population-adjusted comparison with 2002. An exploratory HTML page then presented a “~30% more pressure” headline. **Those earlier responses did not establish the source trail and comparability needed for a public journalism product.** Do not cite the conversation or reuse its numbers as verified observations.

This is a correction to the project's evidentiary starting point, not a claim that every earlier number is false. Each must be independently checked. The project must be free to conclude that some were correct, some wrong, some stale, and some not meaningfully comparable.

## Claims to quarantine

See `data/quarantine/prior_claims.json`. In particular:

- The precise 2026 national/regional/state departures, observation cut-offs and current weather claims.
- South Peninsula 2002 rainfall expressed as 78% of normal, alongside different much lower percentages in different older peninsular series.
- “Seven in 193 years,” “five in 146 years,” and the “once every 25–30 years” framing. Different regions, baselines and station networks cannot be treated as one interchangeable series.
- The 2001 state population total and the projected 2026 total, including column/year alignment, reference date, geography and projection-versus-count status.
- The 51.8% southern reservoir number and last-year comparison; inspect the actual CWC bulletin and its reservoir inventory.
- The 2002 national reservoir figure, which is not directly comparable to a 2026 southern-region snapshot.
- The demand/groundwater/economic assertions made without a consistent regional time series.

## What is wrong with the “pressure index” as journalism

The algebra `population ratio × rainfall-fraction ratio` is a hypothetical population/rainfall comparison. It does **not** measure usable water, household supply, water demand, groundwater extraction, service reliability, or suffering. It also combines a near-2002 census baseline with 2026 projections and may compare unlike seasonal cut-offs and normal periods.

Even if each input is confirmed, present such a result only as a tightly labeled illustrative calculation with explicit assumptions. It must not be the site's lead statistic, a drought classification, or a “worst effective water crisis” ranking. Prefer a set of interpretable observed indicators with their own denominators over a composite number that suggests more certainty than exists.

## Required first audit

Create `artifacts/audits/prior-claims-audit.md` with one row per quarantined claim: exact statement, originally alleged source, exact retrieved source/locator, period/geography/baseline, recomputation, result (`confirmed`, `corrected`, `not_comparable`, `unverified`, `retired`), reviewer and publication action.

For any correction, preserve what changed and why. Do not delete the earlier record to make the project look error-free. If the old HTML was shared, generate a concise correction note for the publisher to distribute; do not send it without authorization.

Do not replace missing primary material with search snippets. A secondary report can support an attributed reporting statement, but not silently become a directly inspected official dataset.

## Gate

G1 passes when the inherited claims have dispositions and there is a fresh, reproducible evidence plan. It does not require proving a severe crisis. A lack of verified current data must lead to an explicit limitation, not to invented values. The software/design work can continue with synthetic fixtures isolated from the public build.
