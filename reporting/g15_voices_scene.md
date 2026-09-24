# G15 voices scene: component handoff

**Scope:** `src/components/VoicesScene.tsx` and `src/styles/voices-scene.css`. This is a presentation component, not an editorial approval. The lead supplies reviewed, ledgered copy and links. I did not edit the homepage, claim ledger, state or release files.

## What it does

- Presents three dated perspectives as an original typographic scene: crop account, flood counterpoint and government response. The visual language uses number, line, circle and a supplied theme word; it copies no newspaper page, logo, photograph or masthead.
- First paint and no-JavaScript output contains all three complete articles, date/place/speaker/outlet/status, limits and source links. Disabled selection buttons and their instruction are hidden without hydration; all accounts remain visible.
- After React hydration, one perspective is visible at a time. Buttons support click, Arrow Left/Right/Up/Down, Home and End. The selected `?voice=<id>` value is shareable and responds to browser Back/Forward. The first perspective has no query parameter. Reduced-motion preference suppresses entrance animation.
- Each account is a named region labelled by its own headline. The scene heading has a stable React-generated ID; every source link is visible in the rendered article. Dark, explicit light and system light palettes are included.

## API / integration

`VoicesSceneProps` requires `eyebrow`, `title`, `introduction`, `sampleNote`, and a three-element `voices` tuple. Each `VoicePerspective` requires `id`, visual `kind` (`farm`, `flood`, `response`), `tabLabel`, human `date`, ISO `dateTime`, `place`, `speaker`, `descriptor`, `outlet`, `status`, short `displayWord`, `headline`, `account`, `context`, `limit`, and `source: { label, href, claimId? }`. `queryKey` defaults to `voice`. Import `VoicesScene` from `src/components/VoicesScene.tsx` and render with `client:load` only after final copy/claims are reviewed. The component imports its own scoped CSS.

The lead should keep voice copy narrow:

1. **16 Sep Telangana:** P Narsi Reddy told *The New Indian Express* that paddy without assured water was left for cattle. The source does not provide his village or district. Use original paraphrase or one brief attributed excerpt, not a state loss total.
2. **18 Sep Bihar:** Mongabay reported Geeta Devi's flooded home and temporary shelter in Manihari, Katihar. Use as a local flood counterpoint; do not infer a Bihar relief failure or disclose her shelter location.
3. **23 Sep remarks / 24 Sep report, Maharashtra:** *The Indian Express* reported Chief Minister Devendra Fadnavis's relief-funding pledge. Label this **reported pledge**. There is no checked GR, sanction, transfer or household receipt in this source review. Do not reuse the report's 1972 comparison or inconsistent area figure.

The scene is a curated sample of original reporting, not a census, current conditions in every named area, an in-house interview, or independent verification of a person's private losses. See `reporting/g15_people_voices.md` and `reporting/g15_voices_independent_review.md` for source-chain, rights and copy limits.

## Checks performed

- `./node_modules/.bin/astro check`: 48 files, 0 errors, 0 warnings, 0 hints.
- `git diff --check -- src/components/VoicesScene.tsx src/styles/voices-scene.css`: clean.
- Isolated React SSR via esbuild and `react-dom/server`: 3 articles, 3 source links, 3 machine-readable dates, 3 disabled controls before hydration, all expected source text present.
- Standalone Chrome rendering at 360, 768 and 1440 CSS px: no horizontal overflow; all three articles visible and inactive controls hidden before hydration. At 360 px, both dark and light system palettes rendered with no overflow. These checks used a local temporary harness with dummy copy and do not establish integrated homepage behavior or accessibility conformance.

**Outstanding independent check:** Visual and axe testing at 360/768/1440 widths after homepage integration, because this scoped task cannot modify a page to mount the component. The lead should inspect both light and dark modes, no-JavaScript state, URL query selection and Back/Forward. This report does not substitute for independent source review of final public wording or human review of sensitive claims.
