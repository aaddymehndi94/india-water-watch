# Current handoff · 24 September 2026

The agent-reviewed progress candidate is publicly hosted at https://india-water-watch.aaddy.chatgpt.site and its source is in GitHub. Approved public scope is 11 attributed claims and five IMD rainfall observations through 23 September 2026. The final editorial release remains unsigned by a human. GitHub Pages is still disabled, so the verified live host is ChatGPT Sites.

**Next executable action:** run `python pipeline/refresh.py --scope all --as-of <actual-IST-timestamp>` for a candidate check; review and approve only defensible changed records. Then rebuild, test, push the reviewed commit to GitHub and the Sites source repository, save/deploy a new Sites version and smoke-test the same public URL. There is no background updater. If a GitHub Pages URL is also desired, the owner can enable **Settings → Pages → Source: GitHub Actions** separately.

Local preview: `python -m http.server 8000 --directory dist-compact`, then open `http://127.0.0.1:8000/`. Review `state/RELEASE_REPORT.md`, `state/COVERAGE_AND_FRESHNESS.md`, `reporting/final_fact_review.md`, `reporting/final_editorial_review.md` and `reporting/final_quality_review.md` for exact limits. Prompt-driven updates are in `docs/UPDATE_PLAYBOOK.md`. The IMD refresh writes only ignored unapproved candidates.
