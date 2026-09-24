# 03 · Quantitative and geospatial contract

## Principle

Use several transparent indicators, not a single invented water-crisis score. Rainfall, reservoir storage, groundwater, delivered supply, demand, crop stress and economic impact measure different things, at different intervals and footprints. A composite index is out of launch scope unless independently specified, validated and clearly distinguished from official classifications.

## Record every denominator

For any quantitative record preserve metric definition, value, unit, geography ID and version, start/end/cutoff/timezone, source series, observation status, normal/reference period, evidence ID, retrieval/publication dates and missingness. Do not coerce source footnotes away during cleaning.

### Rainfall

- `departure_pct = 100 × (actual_mm / normal_mm − 1)` only when normal > 0 and periods/geography agree. A missing/zero normal returns unavailable, not infinity or zero.
- `rain_volume_m3 = rainfall_mm × area_km2 × 1000` is **precipitation volume**, not usable water. Surface runoff, evaporation, soil storage, recharge, quality and transfers still matter.
- Area-average rainfall uses appropriate area weights and masks. Do not average district departures or state percentages unweighted.
- To aggregate a departure, calculate the ratio of the weighted actual and weighted normal totals for exactly the same covered footprint. Report excluded coverage.
- Match provider observation cutoff, not assumed midnight. IMD products may use a morning observation day; inspect the product's convention. Display dates in IST while retaining unambiguous machine timestamps.
- Never rank a June-to-23-September total against full June-to-30-September totals. Compute all years to the same cutoff, or wait for completed seasons.
- Track provider revisions and normal-period changes. Recompute a common climatology where permitted; otherwise show separate incompatible series.
- Do not equate rainfall departure classes with official drought declarations. Source the precise classification threshold/rule; do not make up an orange/red risk scheme that looks official.

### Historical ranks and frequencies

Define the sample before calculating a rank: source, geography, months/day cutoff, baseline, years with adequate coverage, tie rule and exclusion rule. Sort absolute comparable seasonal precipitation or consistently recalculated anomalies, not mixed published percentages from different normals.

Publish `rank of N comparable seasons`, included years, excluded years, coverage and current-season provisional status. For “how many as dry,” count `value <= threshold` on unrounded data. Empirical `k/N` is a historical frequency, not a modern annual event probability or recurrence interval. Do not label it “once in 28 years” without a defensible stationarity/model discussion.

Treat sparse early instrumental reconstructions separately. Shared gauges or derived products are not independent confirmations. Preserve uncertainty bands only when sourced or computed through a documented method; never invent them for visual effect.

### Reservoirs and river flow

- `fill_pct = 100 × live_storage / live_capacity`, with consistent units and actual capacity definition.
- Aggregate by total storage / total capacity over a common reservoir cohort, never by average fill percentages.
- Track reservoir IDs, names/aliases, capacity revisions/siltation, commissioning dates, purpose, location, catchment and service area.
- For historical comparison, show both a stable cohort and current-system totals when available; do not compare a changed inventory as if it were constant.
- Match the same seasonal date/window, not arbitrary latest dates. Publish cohort count and capacity coverage.
- Distinguish current live storage, gross storage, full-reservoir water level, percent of full-reservoir level, and percent of long-term-average storage. A water level percentage is not a volume percentage.
- A national 2002 reservoir statistic cannot be used to compare southern storage in 2026.
- River discharge, reservoir release and rainfall are not additive supplies without a flow accounting model. Avoid counting the same water in an upstream river and downstream reservoir twice.
- No “days of water left” by dividing total reservoir stock by a guessed city's daily demand. A defensible estimate needs usable allocation, dead storage, inflows/outflows, losses, supply priority, treatment constraints and demand assumptions, and still carries uncertainty.

### Groundwater

Separate well water-level observations from annual resource assessments and extraction estimates. A deeper water level generally has different meaning from more stored groundwater; conversion requires aquifer-specific properties. Report measurement season and well-network changes. Do not upsample an annual assessment into a daily live line.

Extraction stage is generally a ratio against an assessed extractable annual resource; confirm the applicable source definition. Values above 100% are possible and must not be clipped. Recharge may include rainfall and non-rainfall components; do not assume rainfall is the only recharge source. Avoid double-counting groundwater/surface-water exchanges in total resource calculations.

### Population, exposure and demand

Use the latest verified Census/projection series with reference dates, revisions, geography and projection method. Do not assert which Census is “latest” without checking at build time. Match historical reorganizations, including undivided/split states, and administrative-versus-urban-agglomeration definitions.

For a count of people **living in areas with a particular observed indicator**, require a matched population layer and an explicit spatial crosswalk. That is exposure, not the number experiencing shortage. Do not redistribute a state projection uniformly to districts and label it measured district population. Estimated gridded populations need source, year, method and uncertainty.

Distinguish withdrawal, consumptive use, delivery, requirement, projected demand and economic water footprint. Do not mix daily litres with annual cubic metres. Household per-capita supply is not total national per-capita renewable resource. Gross precipitation per person is not drinking water availability. Agriculture share figures need a dated country/product/definition; do not transfer a global share to India.

The inherited population/rainfall index is not a production headline metric. A sensitivity exercise may only be shown as a non-hydrological illustration with verified consistent inputs and explicit disclaimers. Do not combine it with unrelated reservoir percentages to imply a validated stress measure.

### Economics

Separate association from causation. Use transparent observed series or attributed model results within their original scope. Record fiscal/calendar year, nominal/real units, base year, price geography, missing observations and crop season. Missing production data is not zero loss. Prevent double-counting intermediate supply-chain losses. No exact GDP loss or food-price forecast from a chosen rainfall multiplier.

### Geography

Use current authoritative administrative IDs with a version date and aliases. Preserve the source's historical geography; build reviewed crosswalks rather than string-only fuzzy joins. Never join solely on district names. Unmatched units remain unmatched and visible in a coverage report.

Basins, districts, states, city limits, utility service areas and meteorological subdivisions are distinct. Record many-to-many intersections and weights if a transform is genuinely needed. Do not assign an entire district to one basin by centroid without disclosure. Do not infer reservoir-to-city supply from proximity.

Boundary source, date, simplification method, rights and any cartographic caveat must be documented. Verify applicable current map-publication requirements and rights before release. Do not manufacture borders, silently erase disputed areas, or present a map as an official territorial endorsement. Where legally/technically unresolved, provide a clearly labeled table alternative and hold that map layer.

### Derived metrics and approval

All headline calculations run from committed permitted data or reproducibly retrievable snapshots. Store formulas, inputs, exclusions and output hashes. Separate implementation author and reviewer. Reproduce at least one headline using an independent method or script, not the same function twice.

The starter's reference math has unit tests; it is not a full hydrological model. Production schema validation, spatial coverage checks and source support must still be implemented and reviewed.
