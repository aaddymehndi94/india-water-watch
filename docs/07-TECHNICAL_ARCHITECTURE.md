# 07 · Technical architecture

## Decision

Use a static editorial site with selective React interactivity. **Astro + React + TypeScript + Tailwind** is the default, not a suggestion to debate indefinitely. Current official docs are in `references/technical_sources.json`. Resolve compatible current stable versions during G0, test them together and commit exact lockfiles. Do not assume an old framework major or model name is current.

## Layers

```text
source registry / discovery
        ↓ controlled fetch + raw metadata/hash
candidate extraction → schema + semantic/geography checks
        ↓ reviewed normalized observations
versioned calculations → claims / charts / stories / updates
        ↓ independent data + editorial review
static HTML + small interactive islands + indexed public JSON
        ↓ browser/accessibility/security/rights checks
immutable release manifest → host profile → authorized publish
```

The visitor never scrapes IMD/CWC, sees a private API token, runs a model, or depends on an external news widget. A third-party outage affects freshness, not page availability. The build does not require live source access: it uses the last approved snapshot. Refresh is a separate command that produces candidate data.

## Frontend

Astro pages/layouts and content collections for pre-rendered prose, sources and SEO. React islands for map/table filtering, tooltips, comparison controls and scenario exploration. TypeScript strict, semantic HTML and a shared design-token system. Tailwind through the currently supported integration, not obsolete setup pasted from memory.

Use a shared chart layer based on D3 utilities/Observable Plot with a consistent accessible wrapper and data-table export. Avoid several competing chart libraries. Render key static SVGs at build time so reading does not depend on hydration. Client-only interactive enhancements must never hide the essential meaning when JavaScript fails.

Use compact locally served TopoJSON/GeoJSON and D3 geo projections for choropleths. Add MapLibre only through an architecture decision if genuine basemap navigation requires it, with offline fallback, rights and tile cost handling. No paid basemap is required for launch.

Static Pagefind search, lazily loaded. Search only published content, not private notes, quarantined claims or test fixtures. Structured filters use deterministic IDs and URL state. Do not add a database just for search.

## Ingestion and analysis

Python with an isolated, locked environment for fetching/tabular/geospatial transforms where needed. Prefer stdlib/httpx and small adapters; add pandas, DuckDB, xarray or geospatial dependencies only for demonstrated tasks. Do not require a multi-gigabyte stack to parse one CSV. JavaScript-only ingestion is acceptable for simple adapters if it reduces maintenance without duplicating logic; record the decision.

Canonical data contracts are JSON Schema 2020-12 in `schemas/`. Implement schema validation in the pipeline and at the build boundary, generate TypeScript types, and avoid hand-maintaining incompatible Python/TS definitions. The starter schemas are a baseline and may be extended with reviewed migrations; do not remove required provenance to simplify rendering.

Use stable IDs, atomic writes, immutable source snapshots where rights permit, SHA-256, semantic diffs and a dependency index linking evidence → observations → calculations → claims → pages → exports. A revised source invalidates downstream review until checked. Cache source documents in ignored local storage; only permitted normalized outputs enter public Git.

## Repository destination

```text
src/{pages,layouts,components,styles,lib,content}
public/{data,geometry,charts,downloads}
pipeline/{sources,normalize,analyze,publish}
data/{approved,candidates,quarantine}  # raw/private excluded
schemas/
references/
tests/{unit,integration,e2e,fixtures}
artifacts/{audits,qa,releases}         # no sensitive notes
state/
.github/workflows/
```

The starter's empty `data/*.json` are bootstrap contracts. Migrate explicitly into a versioned approved/candidate snapshot structure rather than silently reading a mix of both.

## Interface Codex must implement

| Command | Contract |
|---|---|
| `pnpm dev` | Local website preview; no live scraping |
| `pnpm check` | Types, schemas and lint |
| `pnpm test` | Deterministic units and fixture-based adapters |
| `pnpm test:e2e` | Browser journeys, accessibility and map/table checks |
| `pnpm verify` | All production publication checks and report |
| `pnpm refresh -- --scope all --as-of <ISO>` | Candidate retrieval/diff; never blind overwrite or deploy |
| `pnpm build` | Static build from an approved snapshot |
| `pnpm build:compact` | Root-path limited-file static build |
| `pnpm package:site` | Host-ready ZIP plus manifest/size/file-count report |
| `pnpm export:journalists` | Reproducible chart/data/story evidence bundle |
| `pnpm audit:links` | Local links plus rate-limited external checks |

Use cross-platform wrappers, not POSIX-only assumptions in package scripts. Node and Python versions are recorded. `pnpm install --frozen-lockfile` and the locked Python sync must reproduce CI. No floating `latest` dependency at routine builds.

## Content safety

Use controlled local Markdown/components, not MDX code imported from outside sources. Sanitize source-provided strings/HTML, allowlist link schemes and validate redirects. Reject CSV spreadsheet formulas in downloads; serialize JSON safely so `</script>` cannot become code. Apply host-appropriate CSP/security headers where supported, documenting GitHub Pages limitations.

No public write API, user uploads, comments or contact form backend at launch. Use an explicit public correction channel only after configured. Do not invent an email address. Avoid third-party analytics by default; any opt-in measurement is privacy-preserving and documented.

## Two release axes

`software_ready` and `editorially_ready` are separate. A polished app can show “data not available” correctly but is not a completed investigation. Conversely, verified prose without working navigation is not the requested product. Track both rather than one arbitrary completion percentage.
