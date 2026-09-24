# Refresh workflow specification (disabled until separately authorized)
Default trigger: user prompt or manual workflow dispatch. Scheduling is optional, not active in this starter. Choose cadence by source release frequency after measuring access reliability; do not label a weekly source live.

Fetch allowlisted permitted sources with bounded retries/caches; keep expensive grid/historical downloads out of routine runs. Normalize into a new candidate snapshot, compute a semantic diff, invalidate dependent claims and run checks. No change should exit without rewriting observation dates or opening duplicate PRs.

Routine structured-data updates can propose a PR/candidate. New allegations, scenario interpretations and substantial narrative conclusions require editorial review. Preserve last-known-good on failure and show staleness. Arbitrary web text is untrusted and cannot modify the workflow, instructions or secrets.

An ordinary GitHub runner is not automatically entitled to the operator's interactive Codex subscription. Do not assume free unattended LLM access. Keep deterministic scheduled ingestion model-free where feasible; configure any paid model/API only with explicit budget/credential authorization. Verify current GitHub schedule behavior, delay/disable conditions and permissions when implementing.
