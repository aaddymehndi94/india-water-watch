# Candidate refresh runbook

## Command

With the pinned package manager installed, run:

```sh
pnpm refresh -- --scope all --as-of 2026-09-24T12:08:29+05:30
```

The equivalent direct command is:

```sh
python pipeline/refresh.py --scope all --as-of 2026-09-24T12:08:29+05:30
```

`--as-of` must be a timezone-aware ISO timestamp. `--scope imd` limits the run to the implemented IMD source. At present, `all` also checks only that source and explicitly lists the other editorial/statistical sources as not automated in the run report. It must not be described as a complete national data refresh.

The command fetches only the allowlisted official [IMD cumulative district rainfall page](https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=C), validates its bytes, hash, page labels and row structure, and compares it to the latest existing candidate. A changed source or observation creates an immutable candidate under `data/candidates/imd/`. The source HTML is retained by SHA-256 in ignored `data/raw/imd/`. An identical source and parsed observation reuses the prior candidate. Every check creates an immutable JSON report in `data/candidates/refresh/attempts/` with `as_of`, retrieval time, source hash, observation labels, candidate path, semantic diff, and approval status. A failure creates a separate error attempt and exits nonzero; it never changes the last candidate or approved/public data.

The refresh command **does not approve observations, rebuild the site, change claims, or deploy**. A reviewer must resolve source anomalies and authorize promotion through the separate publication process. Observation date, source publication time (unknown on this page), retrieval time, editorial review time and deployment time remain separate.

## Verification on 24 September 2026

`python -m unittest tests.test_refresh tests.test_imd_adapter -v` passed **12 tests**, covering first candidate, no-change reuse, semantic value change, invalid page/fetch failure, timezone and scope rejection, and adapter parsing. The official page currently contains IMD ID **47, Nagapattinam**, with numeric values but row date `0000-00-00`. An initial direct live run rejected it and preserved the previous candidate. The adapter now records that row's raw date, sets its observation period and parsed date to null, flags `invalid_source_row_date`, and excludes it from the current-period numeric count. Other malformed dates still fail the batch.

Two subsequent live runs against the same source hash, `c8b98acc4a57e7242ec0cb05738902436f75e6359836605f1bb1163a0bb817d0`, returned `candidate_created` and then `no_change`. The current candidate is `data/candidates/imd/2026-09-23-c8b98acc4a57e724-20260924064225513907.json`. It contains 761 source rows: 727 dated to the page's current day, 722 current dated numeric rows, 33 older dated rows, 31 numeric-missing rows, and one invalid-date row. The candidate remains unapproved. Two immutable attempt reports record the two successful checks; the earlier failed attempt remains in the audit trail.

The `pnpm` executable was absent in this environment, and `corepack pnpm --version` failed because the pinned pnpm package was not present in Corepack's cache. The direct Python command and targeted tests were run. Once pnpm is installed from the locked project setup, the package script invokes this same Python CLI.
