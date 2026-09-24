# Progress site deployment · 24 September 2026

**Live URL:** https://india-water-watch.aaddy.chatgpt.site

The user authorized a publicly shareable progress site. GitHub Pages remains disabled in the repository, so the same reviewed static candidate was published through ChatGPT Sites as a root-path build. Sites project ID `appgprj_6ab4cac60b7c8191baca4aba1fd9ef2f` is persisted in `.openai/hosting.json`; source commit `e2518e5298256761ea436082e1bfcb697efc2c05` was pushed to its source repository. Saved version 1 ID `appgprj_6ab4cac60b7c8191baca4aba1fd9ef2f~appgver_f6f5adae2a0c8191a602bfe936ec0954` used the locally built `dist/` archive. Deployment `appgdep_6ab4cba0ce2c8191a4e968bc0706285f` reported `succeeded`; a subsequent site read confirmed `access_mode: public` and the live URL.

Live smoke checks returned HTTP 200 for `/`, `/states/`, `/states/karnataka/`, `/search/`, `/explore/`, `/sources/E-IMD-ALLINDIA-20260923/`, `/downloads/observations.csv`, `/downloads/manifest.json` and `/pagefind/pagefind.js`; an unknown path returned 404. Headless Chrome loaded the homepage, Karnataka, Explore and Search with HTTP 200, and Pagefind returned **21** `rainfall` matches (20 displayed). The source snapshot remains five IMD rainfall observations through 23 September 2026; hosting does not make those observations newer.

The public Site is open to anyone with its URL. No named colleague was invited, and no email was sent. This is a progress publication with agent-reviewed, narrowly attributed claims. The final editorial release still lacks genuine human sign-off; no sensitive allegation or high-stakes instruction was published.

Version 2 was saved from Git commit `129b3c044951f98643bdf1d747b2c4e0815eb310` as `appgprj_6ab4cac60b7c8191baca4aba1fd9ef2f~appgver_ca75577cb2a88191a7fd6db07c0299ac` and deployed as `appgdep_6ab4cd3159d0819182807cb588d96ab7`. The host reported `succeeded` at the same URL. A fresh public Chrome smoke check returned HTTP 200 for home, progress, Karnataka and search; the progress page now says “Recorded as deployed,” and search again returned 21 `rainfall` matches. The public observation CSV returned HTTP 200.

GitHub source remains at https://github.com/aaddymehndi94/india-water-watch . GitHub Pages itself still returns 404 because the owner has not enabled Pages. The Sites URL above is the verified public site. Updates require a reviewed source commit, root static build, saved Sites version, deployment and fresh smoke test; no autonomous background updater is running.
