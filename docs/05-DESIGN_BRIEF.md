# 05 · Art direction and interaction brief

## Design target

An original, calm, beautifully typeset data publication. The visual authority should come from exceptional hierarchy, careful maps, annotations, space and typography, not enormous alarming numbers. Think long-form editorial craft and an approachable observatory, not a generic SaaS admin dashboard or a cinematic disaster trailer. Do not copy a publication's proprietary design, logo or signature layout.

## Default direction: “The Water Ledger”

Warm paper backgrounds, deep ink text, restrained blue/teal for water, ochre for concern, and a limited rust accent for actual adverse categories. Avoid all-red maps, neon gradients, glassmorphism, decorative gauge widgets and endless equal-sized statistic cards.

Use a characterful readable editorial serif for headlines and an excellent sans for body/UI, with tabular numerals for data. Start with system fonts; source licensed fonts only later from legitimate upstreams and self-host permitted subsets. No more than two font families. Body type should be comfortably readable on a phone, line length approximately 60–75 characters on wide screens, generous paragraph rhythm and visible link/focus treatment.

The user has requested a polished website, so intentional color is appropriate. Verify contrast rather than guessing. Colors may not be the only way to encode categories. Blue never automatically means safe, and grey missing data must not resemble a normal category.

## Homepage composition

Top: small independent-publication masthead, simple section navigation and search. A concise descriptive headline, one sentence saying what the site is, observation dates, and a clear “Explore your state or district” entry. The hero should answer a reader's question, not announce an unsupported national emergency.

Below: one chosen national visual with an immediately useful legend; a short “What changed / What this does not tell us” pair; a small set of regional stories; a path into historical context; human/economic consequences; outlook/recovery signals; evidence desk and methodology. Use editorial pacing rather than ten full-screen panels.

No fake real-time counter. No animated green dot unless its exact meaning is visible. Prefer “Latest verified observations” and the source date to “LIVE” when the data is daily or weekly.

## Reading modes and navigation

A reader can stay in the overview, choose “Explain this” for plain-language context, or “Inspect data” for definitions and downloads. Long explainers get sticky in-page contents on desktop and an accessible collapsible contents control on mobile. Keep global navigation to roughly five grouped entries: Overview, Explore, Understand, Outlook & updates, Sources.

Every local page has breadcrumbs, source dates, a compact location summary, the relevant indicators, a season explanation, local response/reporting links, gaps and source controls. A district view must explicitly say which metrics are unavailable there.

Search should find regions, stories, methods and sources. A location selector uses aliases and a reviewed administrative index, not geolocation permission or free-text guesses. Remember preferences in the URL first; optional local storage must not be required.

## Charts

Each chart answers one question. Provide a human-readable chart title, short takeaway only if supported, units, range, reference period, legend, exact data date, source control, method control, accessible description and a table. Hover tooltips are optional enhancement; keyboard and touch must work.

Historical observed lines are solid; forecasts are visually separate and dashed; scenarios are marked as hypothetical. Uncertainty bands must come from real inputs, not decoration. Missing periods break lines. Use direct labeling where possible. Avoid dual-axis charts that imply correlations and 3D/pie effects that distort comparisons.

Export a chart with its title, units, source/date, caveat and release ID embedded. The screenshot must not lose the uncertainty in a hidden tooltip. Provide SVG/PNG and CSV for key charts, with original-source rights noted.

## Maps

State/UT view first, district resolution on demand, basin context as a separate layer. Use honest fixed category definitions or disclosed continuous scales. No quantile recoloring just to make every map dramatic. Keep legends stable across compared dates. Show no-data, stale, unmatched geography and official classifications differently.

Offer metric, date/season and location controls with a shareable URL; zoom/reset and a non-map table path. Avoid a pinch/scroll trap. Include island territories and small regions with meaningful insets or equivalent navigation. Boundaries must be reviewed for source, version, rights and applicable publication requirements.

Do not stream tiles for a simple choropleth. Prefer compact static vectors, lazy-load district geometry by state, and keep the initial page light. A basemap library is optional only when it adds explanatory value and its licensing/hosting is handled.

## Signature modules

- **Follow a drop:** a sourced rainfall-to-river/storage/groundwater-to-service-area diagram. Where links are unknown, label them unknown.
- **Same season, different year:** a cutoff-matched history explorer with explicit comparability status.
- **What changed since the previous bulletin:** absolute changes, not just percentages, with revised-versus-new observations separated.
- **What money can and cannot buffer:** reported coping mechanisms connected to shared-resource dependencies, not a speculative class caricature.
- **What would change this assessment:** recovery and worsening signals linked to observable indicators.
- **Show me the evidence:** a side panel with exact locator, dates, definitions, source, methods and data download, plus a fully accessible source page.

These are requirements for informative interactions, not an excuse for needless animation. Pick the strongest feasible modules and fully finish them.

## Responsive and inclusive requirements

Design at 360, 390, 768 and 1440 CSS pixels. Test 200% zoom, keyboard only, reduced motion, high contrast and no JavaScript. Charts get table fallbacks; the national briefing and source links remain readable without JS. Interactive controls have labels and adequate touch targets. Dialogs manage focus and escape; sticky elements do not hide content.

English first, architecture ready for Hindi and regional-language content. Do not launch unreviewed machine translations of safety/legal instructions. Include original-language titles and attributed translations where reviewed. No screen-reader-unfriendly scrolling marquee or autoplay video.

## Design process and acceptance

Explore up to three restrained directions at thumbnail/wireframe level, choose one with reasons, then build one complete homepage/local-page/chart slice. Do not spend all credits on moodboards. Make two substantive visual review passes on actual browser screenshots: hierarchy/content first, polish/interaction second. Fix generic layouts, awkward chart labels, empty states and mobile overflow.

No stock images of cracked earth as evidence of this year's conditions. Documentary photographs require exact place/date/context and license. Illustrations must be labeled; no generated disaster imagery presented as reporting.
