# G13 visual and interaction review

Reviewed 24 September 2026 from the local Astro build at 360 × 850 and 1440 × 900 CSS pixels. Captures: `/tmp/g13-audit-home-fold-360.png`, `/tmp/g13-audit-home-fold-1440.png`, and `/tmp/g13-audit-home-1440.png`. This is an agent design review, not a human editorial or accessibility approval.

## Candid verdict

The G11 edition is clearer and more credible than the starter, but the publisher's complaint remains justified. It reads as a handsome long article with several data cards, rather than an interactive national feature. The full desktop page repeats the same dark or paper section, serif heading, pull quote and three-card rhythm for most of its length. The mobile first screen offers a question and a static abstract background, while the finding begins only at the fold. Motion is limited to a small number reveal and gentle entry effects. The reader cannot yet *do* much inside the main narrative.

| Severity | Finding from the screenshots / implementation | Effect on reader |
|---|---|---|
| High | The cover spends nearly a whole mobile screen on headline and deck before a useful data control or complete finding. | It feels like a poster before it feels like a working water publication. |
| High | Chapter sections rely on repeated signal cards and prose blocks, with little change in visual grammar. | The page becomes predictable and tiring over a long scroll. |
| High | The IMD chart is a static conventional bar chart below several text blocks. The dynamic atlas lives on another route. | The strongest evidence does not create an exploratory moment in the story. |
| High | The Places stage had only an alphabetic tile directory, not even a schematic spatial locator. | Readers expecting a map-like way into their place cannot orient themselves. |
| Medium | The top navigation is functional but still resembles a compact institutional site. On mobile it is hidden behind a standard Menu button. | It does not contribute to the feature's identity or reveal a narrative path. |
| Medium | The AI-generated cover art is beautiful but resembles aerial terrain. It is labeled, yet the label is small relative to the image. | A quick glance could mistake symbolic art for documentary geography. |
| Medium | The hero's −14.9% is striking but the denominator/date/source and its limits live in a conventional boxed aside. | Visual emphasis exceeds explanatory interaction; the finding does not unfold. |
| Low | Light and dark themes are accessible, but the main cover remains nearly the same dark composition in both. | The toggle changes reading surfaces more than the first impression. |

## Directions considered

1. **Documentary imagery first.** A large geographic photograph or satellite-like map would give an immediate spectacle. Rejected as the main reporting grammar because no dated, licensed documentary visual with the required place and 2026 context is approved. The existing abstract image stays visibly labeled as symbolic.
2. **Map newsroom first.** An India boundary map with state shading could make local navigation obvious. Rejected for current evidence: reusable geometry/provenance is held, and there are no approved state numeric water values to shade. A schematic 36-tile locator can provide spatial orientation without pretending to be data or official borders.
3. **Evidence journey.** A fullscreen editorial narrative with a sticky, source-linked visual stage, exact dated numbers, and reader controlled transitions between rain, storage, official action, access and uncertainty. Selected. It can be implemented with the approved subset and keeps each system's date and denominator visible.

## Design decisions being implemented

- Keep the abstract cover art with a prominent illustration label and complete caption. Strengthen the mobile first screen so the measured number and story affordance arrive sooner.
- Introduce a sticky visual stage in the homepage narrative with reader controlled states. An external React island will own its data interaction; the page will provide a no-JavaScript evidence path.
- Vary chapter composition: some fullscreen dark visual scenes, some bright paper evidence sections, narrower prose and direct source drawers. Use motion to reveal exact values and relationships, never to count through invented measurements.
- Finish an explicitly **schematic**, approximate 36-place tile cartogram in Explore with equal-size units, no political borders, no state rainfall shading, and an A–Z alternative.
- Keep the existing approved claims, observation dates, local gaps, forecast labels and AI assessment uncertainty. Visual drama must not create a stronger claim than the documents support.

## Acceptance checks

360, 390, 768 and 1440 widths; root and GitHub subpath builds; mouse, touch and keyboard selection; no-JavaScript fallback; reduced motion; light and dark contrast; stable source links; no page overflow; no geographic/severity inference from locator tiles. Release screenshots must include the cover, sticky stage and schematic locator in mobile and desktop views.
