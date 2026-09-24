# 14 · Journalist desk and public reuse

Build a first-class `/journalists/` page, not an afterthought containing a giant bibliography.

## Core reader need

A journalist must be able to find a precise current finding, understand its limitations, reproduce the number, reuse an original chart where permitted and locate the underlying source without asking the site owner to explain the code.

## Deliverables

- A dated briefing of the most material verified findings, each with scope, caveat, claim ID and exact sources. Do not invent a fixed number of findings if evidence is thin.
- A chart catalogue with thumbnail, title, date, geography, unit, method, accessible description and SVG/PNG/CSV downloads. Export source/date/caveat/release IDs on the chart itself.
- A downloadable source/data manifest, normalized CSVs where redistribution is permitted, calculation instructions and hashes. Restricted originals remain links.
- A claim ledger view with verified/attributed/derived status, exact locator and version history, not hidden chain-of-thought or private interview notes.
- A corrections log and stable citation format. Provide `CITATION.cff` only once actual project metadata is known; no invented DOI, affiliations or author names.
- A reporting-leads section containing well-founded unanswered questions, not insinuations. Local data absence is a reporting opportunity, not evidence of misconduct.
- A media/contact method after a genuine channel is configured; no fabricated emails or experts' private contact details.

## Journalist bundle structure

`briefing.md`, `findings.csv`, `sources.json`, `data-dictionary.md`, `methods.md`, `coverage.md`, `corrections.md`, `manifest.json`, permitted data tables and `charts/` with PNG/SVG/CSV/alt-text. Include build/release IDs and source observation dates. Include rights and attribution for each asset, with third-party exclusions.

A bundle must be tied to the approved snapshot, not fetch latest data independently while exporting. Do not publish blank or synthetic chart files as completed exports.

## Sharing design

Stable deep links to state/district/metric and historical comparison states. Social/WhatsApp preview text must reflect the exact page and observation date. Never put a striking number on a card without its scope and source period. No URL shortener or tracker is required.

## Reuse license

The publisher may offer a permissive license for original charts/editorial text after review. Do not claim rights over underlying third-party material. Public CSV download does not imply unrestricted redistribution of all source documents. Embed attribution and licensing metadata in exports wherever feasible.
