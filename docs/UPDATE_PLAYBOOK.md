# Updating India Water Watch

The site is a static publication. A rebuild refreshes the **build date**, not the underlying water observation date. Only reviewed records in `data/approved/` appear in public charts and claims.

## Prompt-driven update

From this repository, ask Codex:

> Check the official IMD cumulative rainfall source as of the current India date. Run the candidate refresh, report source dates, missing/stale/invalid rows and semantic differences. Independently verify any proposed public claim and its source locator. Update approved records only if the source, geography, baseline, arithmetic and rights checks pass. Then regenerate journalist exports, run tests and both static builds, inspect the release diff, and commit the reviewed change. Push the progress-site update only after local release checks pass. Do not promote candidate rows merely because the fetch succeeded.

To update a different beat, name the exact source and question in the prompt. An inaccessible source should produce a logged gap and a legitimate manual-import proposal; it must not cause fabricated data.

## Exact local commands

```bash
python pipeline/refresh.py --scope all --as-of 2026-09-24T12:00:00+05:30
python -m tools.validate_approved
python -m tools.export_journalists
python -m unittest discover -s tests -q
npm exec --yes --package=pnpm@12.6.0 -- pnpm check
python -m tools.build_profile --profile compact
PUBLIC_SITE_URL=https://aaddymehndi94.github.io PUBLIC_BASE_PATH=/india-water-watch/ npm exec --yes --package=pnpm@12.6.0 -- pnpm build
python tools/release_gate.py
```

Use the actual evaluation timestamp in `--as-of`. The refresh command checks only the currently implemented IMD adapter and writes under ignored `data/candidates/`; it does not approve or deploy anything. The release gate checks the exact `dist/` manifest and review evidence, so a new approved source snapshot requires fresh reviews and a new `state/RELEASE_REVIEW.json` binding. Commit reviewed changes and push `main` to preserve GitHub source. For the live ChatGPT Sites publication, ask Codex to push that exact commit to the configured Sites source repository, build a root-path `dist/`, save a version with the built archive, deploy it, and smoke-test https://india-water-watch.aaddy.chatgpt.site . `.openai/hosting.json` records the Sites project ID. GitHub Pages can additionally deploy on pushes once the repository owner enables Pages. Do not automate candidate promotion.

For a quick local root preview after `build:compact`:

```bash
python -m http.server 8000 --directory dist-compact
```

Open `http://127.0.0.1:8000/`. For the repository-prefix build, run `npm exec --yes --package=pnpm@12.6.0 -- pnpm preview -- --host 127.0.0.1` and open the printed `/india-water-watch/` address.

## Corrections and rollback

Record a correction in the claim ledger with a superseding claim ID and dated explanation; rebuild all exports and indexes. Preserve old source snapshots and release manifests. To roll back a hosted progress build, redeploy an earlier reviewed commit through the Pages workflow; do not rewrite history or silently change the observation date.
