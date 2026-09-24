# Source adapter contract
ID / owner / authoritative publisher:
Landing page (discovery only):
Exact permitted product URL or manual-import interface:
Authentication/terms/rights and redistribution decision:
Geographic unit and boundary version:
Metric definition / units / normal / cohort / population basis:
Observation cutoff and timezone / publication cadence / expected latency:
Retrieval timestamp / source document date / snapshot hash:
Parsing strategy and precise evidence locator:
Validation rules, sanity bounds and permitted exceptional values:
Known revisions and historical backfills:

## Fixtures and tests
Keep minimal permitted fixtures, or synthetic fixtures explicitly isolated from production. Test valid input, source redesign, truncated download, duplicate rows, missing cells, changed units, revised values and unavailable sources. Never silently scrape around access controls.

## Failure behavior
Return structured failure; preserve last-known-good; show its observation age; log retry/backoff and legitimate fallback/manual-import path. A fresh HTTP response does not imply fresh observations. Never put credentials or restricted raw files in public outputs.
