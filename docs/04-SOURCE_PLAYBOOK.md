# 04 · Source discovery and evidence acquisition

## Registry versus evidence

`references/source_registry.json` is a starting map of sources, not a certified dataset catalogue. Each entry has an access status. Several government portals were blocked or timed out during starter preparation. A failed request does not prove a source is unavailable to Codex, nor may it be labeled successfully inspected.

An entry URL supports discovery. Publication requires a separate evidence record containing the exact document/data endpoint, observed scope, locator and content hash. Do not cite a homepage for a statistic supposedly found deep inside a report.

## Evidence hierarchy, used intelligently

Prefer exact primary observations and official documents for what was measured or announced; original research for scientific claims; original on-the-ground reporting for lived conditions; and transparent secondary synthesis for context. Official statements are evidence of statements, not automatically independent evidence that implementation succeeded. A secondary report can be used with honest attribution when the primary source is inaccessible.

One authoritative primary dataset with an independent extraction/recalculation can support a measurement. Do not impose a fake requirement for two sources for every cell. High-impact interpretive or contested claims need appropriate independent corroboration and counterevidence. Identify common upstream source chains.

## Initial discovery tasks

1. IMD current rainfall at national, state, subdivision, district and basin levels; actual product observation window, normals, archive, download rights and revisions.
2. IMD/IITM historical series and documentation; actual start/end, regional definitions, station network, licensing and comparable modern subset.
3. CWC current and historical reservoir bulletins; stable IDs, inventories, capacity and same-date archives. NWIC/India-WRIS as supplementary official catalogue paths, not assumed universal APIs.
4. CGWB observations and dynamic resource assessments; actual assessment years, well-network coverage, extraction/recharge definitions and district/basin compatibility.
5. Census/official demographic projections and LGD geography; boundary vintage, revisions and historical crosswalks.
6. Agriculture statistics, crop/sowing advisories, market prices, MOSPI and RBI series; definition, geography and revision history.
7. NDMA/department/state/utility documents and orders; actual effective date and institutional responsibility.
8. Original local-language/national reporting, independent researchers and community accounts; event date, original report, rights and corroboration.
9. Public-health/water-quality advisories from competent authorities; no unsupported potability inferences.
10. Current official seasonal outlooks and climate indices; issue date, validity, skill information and regional scope.

## Source-access ladder

Use documented public downloads/API first. Next use structured public pages or a permitted HTML/PDF adapter. If navigation is required, use a browser without bypassing controls. Inspect PDF tables visually as well as parsed text; preserve page/row and check footnotes/units. OCR is a last resort and OCR-derived numerals require independent visual checking. If blocked, try a legitimately accessible official mirror or a cited secondary original. A manual file import is acceptable if its provenance and hash are recorded.

Do not endlessly hammer a fragile portal. Default one in-flight request per host, a conservative delay, conditional requests and exponential backoff, respecting robots and terms. Honor `Retry-After`. Large historical/gridded downloads are optional and should be bounded, cached and never fetched per visitor or every update. Record access limitations honestly.

## Source record checklist

Publisher and canonical URL; exact title; publication/update time if known; event/observation time; retrieval time; geography; dataset version; locator; license/rights; local snapshot path if permitted; SHA-256; parser version; extracted record count; validation outcome; relation to upstream source; review status.

Store raw licensed working files in ignored local storage by default. Commit only permitted normalized data, metadata and hashes. The public site links to original sources; it does not mirror whole newspapers or restricted datasets.

## News and voices

Curate, do not carpet-bomb. Search by meaningful topic and geography, including regional-language variants. Resolve canonical links, syndication and updates. Separate new publication from old event. Preserve the date of a quote and the original speaker's context. Do not use search snippets as final quotations or pretend an article has been read when it is paywalled.

Classify items as official notice, original reporting, research, expert interpretation or opinion. Present a short original description of why it matters and what it does not establish. Do not copy article bodies or wholesale abstracts. Default to very brief extracts, preferably paraphrase with attribution; rights review is still required.

## Current access failures are part of the product test

Create fixtures for timeout, 403/401, rate limit, HTML login masquerading as CSV, PDF schema change, source revision, deleted page and backdated announcement. The last verified observation remains available with its original date and a stale badge. “Last attempted” and “last successful” are separate fields. A successful homepage request must not mark an adapter healthy if its data request failed.
