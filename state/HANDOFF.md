# Current handoff · 24 September 2026

**Maintained host:** https://aaddymehndi94.github.io/india-water-watch/ . The G13a revision is live; the G13b press/market candidate is locally built, independently reviewed and ready for the next scoped GitHub Pages checkpoint. GitHub Pages is public. There is no unattended source-to-publication updater.

**G13b local candidate:** `candidate-20260924-9a7e43a1017a`; 30 claims, nine numeric observations, 25 evidence records and 44 geographies. The dated first-screen IMD figures, reader-controlled rainfall comparison, 36-place schematic state/UT locator, five-card linked press collage and five-gate market module are built. The latter does not claim 2026 water-caused earnings or share-price changes. Source review is `reporting/g13_independent_source_review.md`; independent browser, axe, security and visual review is `reporting/g13b_quality_review.md`. The structural gate passed. Root, compact and GitHub-prefix builds plus journalist exports and portable ZIPs are present locally; see `state/RELEASE_REPORT.md`.

**Exact next executable action:** `git status --short`; stage only the reviewed G13b files, commit, push `main`, inspect the new GitHub Pages Actions run and cache-busted live home/impacts pages. Then write the run ID, served time, content commit and live smoke results into `state/DEPLOYMENT_REPORT.md`, update `state/PROJECT_STATE.json` and `project/tasks.json`, and make a scoped postdeployment checkpoint.

**Reporting next:** seek direct, licensed 2026 imagery and independently reviewed farmer/official quotes; acquire matched state/district service, groundwater and basin data with boundary rights; verify aid delivery and 2026 company operational effects before publishing them. The current matched historic result concerns completed June only. `state/COVERAGE_AND_FRESHNESS.md` lists the exact unknowns. The media-silence hypothesis was rejected by a non-exhaustive source audit.

**Preview:** `python -m http.server 8000 --directory dist-compact`, then `http://127.0.0.1:8000/`. **Update prompt and process:** `docs/UPDATE_PLAYBOOK.md`. Reviewed `main` pushes trigger the existing GitHub Actions Pages workflow.
