# 06 · Information architecture and reader journeys

## Routes

| Route | Purpose | Required behavior |
|---|---|---|
| `/` | National briefing | Context in first screen; dates; selected evidence; local entry |
| `/explore/` | All-India atlas/table | Shareable metric/region/date filters; table fallback |
| `/states/` | State/UT index | Complete verified directory; not a ranking of governments |
| `/states/[slug]/` | Local water briefing | Relevant seasons, current indicators, history, response, gaps |
| `/districts/` | District selector/explorer | Availability-aware, versioned codes, no invented local demand |
| `/districts/[id]/` | Full-build district page where supported | Do not make thin placeholder SEO pages |
| `/basins/` | Basin context | Clearly distinguish administrative and hydrological borders |
| `/history/` | Comparable past | Modern series plus separate reconstructed/documentary eras |
| `/water-and-people/` | Population, use, access | Definitions; comparable denominators; no fake pressure score |
| `/impacts/` | Economy/livelihoods/inequality | Evidence-backed themes and actual local reporting |
| `/response/` | Documented institutional actions | Dated action-stage tracker; original documents; no political scoring |
| `/outlook/` | Official outlooks and scenarios | Issue/validity labels; conditional branches; recovery paths |
| `/updates/` | Curated latest developments | Event date versus publication date; duplicate/source-chain control |
| `/understand/[slug]/` | Durable explainers | Question-led stories, definitions, visuals, claim-level sources |
| `/what-you-can-do/` | Practical information | Roles, local official guidance, dates, limits and safeguards |
| `/journalists/` | Reuse/reporting desk | Verified findings, chart/data bundle, methodology and correction channel |
| `/sources/` | Evidence catalogue | Searchable publisher, dataset, geography, dates, locator, limitations |
| `/sources/[id]/` | Exact evidence record | Source link, metadata, rights, where used, provenance |
| `/methodology/` | Full methods | Definitions, comparability, uncertainty, version history |
| `/data-status/` | Coverage and freshness | Last observation/success/attempt; no-data and source failures |
| `/corrections/` | Transparent correction log | What changed, why, date, affected release/claims |
| `/about/` | Publisher and process | Actual contributors, AI disclosure, independence, contacts |
| `/search/` | Static full-text search | Keyboard-friendly; deep links; no private/test content |

Routes are a destination contract, not permission to publish unsourced filler. The publisher may release the verified subset with honest scope. The full project must account for every route as implemented, merged into another clear route, or explicitly deferred with reason.

## Reader journey 1: “What is this?”

Landing → brief explanation → three supported findings → current map → uncertainty → choose local detail or history. A user should not have to understand “LPA,” “BCM,” or a meteorological subdivision to navigate.

## Reader journey 2: “What about my district?”

Location search → district/state → what is observed locally versus inherited regional context → relevant local season → source/coverage → verified local official information. No implication that rainfall coverage equals household-service coverage.

## Reader journey 3: “Has this happened before?”

History → choose region/season/cutoff → see eligible comparison set → rank/frequency only if allowed → analogue story → changes in infrastructure/population/demand → limitations. If incompatible, explain exactly why and offer a defensible narrower comparison.

## Reader journey 4: “I am a journalist”

Journalist desk → verified current findings with caveats → source record → chart/table download → reproducibility manifest → reporting leads/interview question bank → correction/contact mechanism. Downloads carry dates and must not look like live measurements after sharing.

## Reader journey 5: “What happens next?”

Official outlook cards → issue/expiry and scope → conditional pathways → observable trigger/recovery signals → what remains unknown. No probabilistic story unless a sourced forecast actually gives the probability for that event.

## URL state

Shareable filters should encode validated metric ID, location ID/version, season, cutoff, comparison year and view mode. Invalid values fall back safely with an explanation. All internal links, search paths, download URLs and source anchors must respect the deployment base path.

## Compact host profile

The drag-and-drop export may use `/districts/?id=...` and `/sources/?id=...` instead of hundreds of individual HTML files. The full GitHub build may prerender substantive district pages. Keep the same data and meaning across profiles; do not remove citations to meet an asset cap. Test both profiles and document the navigation/SEO tradeoff.
