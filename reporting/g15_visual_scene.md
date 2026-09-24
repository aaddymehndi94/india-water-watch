# G15 visual scene: one dated national rainfall comparison

## Scope and source

This is an isolated, **unintegrated** homepage candidate in `src/components/RainDeficitScene.tsx` and `src/styles/rain-deficit-scene.css`. It is designed for the approved all-India IMD cumulative reading for **1 June–24 September 2026**: **723.6 mm recorded**, **843.2 mm same-date normal**, **−14.2%** after rounding, and a derived **119.6 mm** difference. The normal is IMD's **1971–2020** reference. The original source is the [IMD all-India GIF](https://mausam.imd.gov.in/ClimateInformation/imdweb/DAY_WEEK/all-india.gif), archived and independently checked in `reporting/g14_local_data.md`; the promoted public evidence is `E-IMD-ALLINDIA-20260924`, claim `C-IMD-RAINFALL-DEP-india-20260924`. The inspected original had SHA-256 `4114c80678444756c7d2a86e1fb58c799b43439a1d0ab2e5b0bcb8a365003f9f`. The graphic remains a dated national rainfall comparison; it cannot establish local supply, crop losses, storage or drought status.

## Design choice

The existing homepage cover has a large departure, and `WaterStoryStage` already supplies a two-window horizontal bar chart. This candidate uses a different, vertical shared-zero comparison. The normal and recorded columns have the same millimetre scale; the hatched 14.2% top of the normal column is the 119.6 mm gap. One large negative figure anchors the reading, while dates, denominator, the normal period, the source and the limitation remain in sight. The “Compare totals / Isolate the gap” buttons change emphasis and an explanatory sentence; they do not scrub between imaginary daily readings. The scene has a substantive server-rendered default, an explicit accessible plot description, keyboard controls and reduced-motion handling.

This should **replace or substantially shorten** the existing season-to-date part of `WaterStoryStage` if integrated on the homepage. Stacking both full charts in sequence would repeat the same finding and slow the story. Keep the June comparison elsewhere or retain its existing tab in a concise context module.

## Integration API

`RainDeficitSceneProps` requires `observedMm`, `normalMm`, `periodLabel`, `sourceHref`, `sourceLabel`, and `claimId`. It rejects invalid, above-normal or mismatched data rather than rendering a misleading “gap”. Use reviewed publication values and the Astro base-aware `source(rain.id)` URL, for example:

```astro
import RainDeficitScene from '../components/RainDeficitScene';
<RainDeficitScene client:load
  observedMm={723.6} normalMm={843.2}
  periodLabel="1 June–24 September 2026"
  sourceHref={source(rain.id)} sourceLabel="IMD 24 September graphic"
  claimId={rain.id} />
```

When the provider advances, update the values, period label and approved evidence together. Do not leave a current-looking scene pointing to an older source. The derived millimetre and percentage gap are calculated from the passed totals. The static no-JavaScript reading retains the exact totals and source link; enhancement enables the two buttons.

## Verification and visual review

- Read the current built homepage at **360, 768 and 1440 CSS px**. The current cover is strong, while the existing measurement stage already explains the same national denominator. This informed the replacement recommendation.
- `astro check`: **47 files; 0 errors, 0 warnings, 0 hints** after component/CSS edits. A previous check also passed, but scanned an unrelated generated preview tree; the later clean result is authoritative here.
- Isolated React browser harness with local Chrome at **360, 390, 768 and 1440 px** in dark mode and **360, 1440 px** in light mode: no horizontal overflow; the gap button becomes `aria-pressed="true"`; its caption says **119.6 mm / 14.2%**. Screenshots under `/tmp/iww-rds-polish-{360,768,1440}.png` and `/tmp/iww-rds-final-{360,390,768,1440}-{dark,light}.png` were inspected. The first visual pass revealed an annotation overlap on a phone and a caption/border overlap at tablet width; both were fixed in CSS and retested.
- Keyboard: Tab, Tab, Enter selected the gap view. `prefers-reduced-motion: reduce` gave **0s** transition duration. Static server render retained the heading, totals, date, source, plot description and limitation before hydration.

## Limits and next action

This agent has not edited the homepage, built a full release, performed an independent source review of the integrated page, or published. The scene intentionally has no simulated hourly/daily rain, no map, and no water-supply inference. The lead should decide whether it improves the story over the existing measurement stage, integrate it as a replacement if so, then run root/prefix build, source-link, no-JavaScript, mobile and accessibility review in the full page context.

### Independent QA correction

The integrated G15 independent review found that at 360/390 CSS px the `Recorded` column caption intersected the `723.6 mm · recorded` guide label. The mobile CSS now places `Recorded` **inside the top of its measured column** in dark ink, leaving the guide label above the line. Focused local Chrome checks at 360 and 390 px in both dark and light themes found no bounding-box intersection and no horizontal overflow. Screenshots were visually inspected at `/tmp/iww-rds-label-fix-{360,390}-{dark,light}.png`. A separate static server-rendered/no-JavaScript check at both widths also found no overlap; exact source text remained readable and enhancement buttons stayed disabled. The desktop label placement and server-rendered content were unchanged. A full integrated root/prefix rebuild and independent QA remain with the lead.
