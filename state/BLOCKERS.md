# Blocker log · 24 September 2026

- GitHub Pages is **not enabled**. The tested candidate was pushed to `origin/main` as `789c58f`; [workflow run #1](https://github.com/aaddymehndi94/india-water-watch/actions/runs/35966962356) passed installation, tests and site build, then `actions/configure-pages` failed with “Get Pages site failed” / API 404. The expected Pages URL returned HTTP 404. The repository owner needs to set **Settings → Pages → Build and deployment → Source: GitHub Actions**. No authenticated Pages settings API access is available here; after enablement, trigger the workflow again and verify the public URL.
- Final editorial publication still lacks human sign-off tied to the release manifest. The user's instruction authorizes a source-safe progress site; `python tools/release_gate.py --publication` remains closed for the final publication.
- Survey of India geometry reproduction rights remain unresolved. No restricted map or raw source documents are bundled.
- No approved current district, reservoir, groundwater, river, service or health measures. The IMD district candidate has unknown/stale/missing rows and provider arithmetic flags. A future update must review those individually and crosswalk locations before promotion.

These limits do not block the local static candidate or GitHub source repository. They block a verified hosted Pages URL until the setting is changed.
