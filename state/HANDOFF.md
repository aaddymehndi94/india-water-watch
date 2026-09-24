# Current handoff · 24 September 2026

The agent-reviewed progress candidate is publicly hosted at https://aaddymehndi94.github.io/india-water-watch/ and secondarily at https://india-water-watch.aaddy.chatgpt.site . Source is in GitHub. Approved public scope is 11 attributed claims and five IMD rainfall observations through 23 September 2026. The final editorial release remains unsigned by a human.

**Current revision:** G10 editorial rebuild has passed local structural, source and browser checks. The deployed URLs still show the earlier progress candidate until this reviewed revision is pushed and the live smoke test passes. Independent fact and quality agent reports are in `reporting/g10_fact_review.md` and `reporting/g10_quality_review.md`. There is no background updater.

**Next executable action:** run `git status --short`, commit the G10 reviewed paths with a scoped `git add`, push `main`, inspect the GitHub Pages Actions run and smoke-test the live homepage, theme toggle, explorer, search and downloads. Update this handoff with the deployed commit, then synchronize the secondary Sites URL if maintaining it.

Local preview: `python -m http.server 8000 --directory dist-compact`, then open `http://127.0.0.1:8000/`. Review `state/RELEASE_REPORT.md`, `state/COVERAGE_AND_FRESHNESS.md`, `reporting/final_fact_review.md`, `reporting/final_editorial_review.md` and `reporting/final_quality_review.md` for exact limits. Prompt-driven updates are in `docs/UPDATE_PLAYBOOK.md`. The IMD refresh writes only ignored unapproved candidates.
