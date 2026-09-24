# Progress site deployment · 24 September 2026

## Primary GitHub Pages site

**URL:** https://aaddymehndi94.github.io/india-water-watch/

The owner selected GitHub Actions as the Pages source. The existing `.github/workflows/pages.yml` builds the static Astro output on reviewed `main` pushes and deploys it. The latest G10 visual/content revision is commit `21be623d6029b10ed87dfceae58e86b960d404ad`; its [Pages workflow](https://github.com/aaddymehndi94/india-water-watch/actions/runs/35973399226) completed successfully. Two small hosted-search fixes followed: `faa51d7a21020538b1da7f99f7d3683696f26b08` and current commit `7b4cb0a4ceb2da897d9eda50cb6e85958be2ed51`. The [current Pages workflow](https://github.com/aaddymehndi94/india-water-watch/actions/runs/35974368904) completed successfully.

Public HTTP checks returned 200 for home, Explore, Karnataka, History, Response, CWC source, Search, approved observation/claim/source CSVs and `release.json`. A live Chrome check after the current search fix submitted `rainfall` immediately after page parsing three times; all three returned **65 matching pages**, 20 displayed, with zero page errors. The first fixed-delay live QA harness had reported an apparent search failure because the remote Pagefind fetch sometimes took longer than its 1.2-second wait; the later condition-based browser check verified the actual interaction. Search now displays a loading message while the remote index downloads. The hosted release remains a public progress publication.

## Secondary Sites publication

**URL:** https://india-water-watch.aaddy.chatgpt.site

The pre-existing Sites project is `appgprj_6ab4cac60b7c8191baca4aba1fd9ef2f` (`.openai/hosting.json`). Its access mode was checked as **public**. The exact current Git commit `7b4cb0a4ceb2da897d9eda50cb6e85958be2ed51` was pushed to its source repository, root-path static files were packaged in `release/sites-deploy.tar.gz`, saved as version **6** (`appgprj_6ab4cac60b7c8191baca4aba1fd9ef2f~appgver_71a1753b09d08191aaa150d0c4827113`), and deployed successfully as `appgdep_6ab4dcdbbf2081918d46b7c814d524de`. Public HTTP checks returned 200 for the same key routes and CSVs. A live Chrome search check submitted `rainfall` immediately three times; all three returned **65 matching pages**, 20 displayed, with zero page errors.

The owner subsequently said one live host is sufficient. GitHub Pages is now the primary update path; future G11 increments need not synchronize Sites. Anyone with either public URL can read it; no named colleague was invited and no email was sent. No unattended source or site updater is running. Every water observation retains its own date independent of deployment time.
