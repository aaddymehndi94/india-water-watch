# Updating India Water Watch

The site is a static publication. A rebuild refreshes the **build date**, not the underlying water observation date. Only reviewed records in `data/approved/` appear in public charts and claims.

## Prompt-driven update

From this repository, ask Codex:

> Update India Water Watch as of the current India date. Check the official IMD rainfall product, the CWC reservoir bulletin list and the latest reachable original PDF, and any new official drought orders or response documents. Record each source's observation/status date, issue date, retrieval time and exact URL; log broken feeds and keep the last verified version visibly dated. Run the IMD candidate refresh and report missing/stale/invalid district rows and semantic differences. Independently verify every proposed public claim, calculation, geography, denominator and rights status. Add only supported records to the approved ledger, update the story, response and coverage pages, then regenerate journalist exports, run tests and root/GitHub static builds, inspect the release diff, and push a reviewed progress update. Do not promote candidate rows merely because a fetch succeeded. Never relabel old observations with the new build date.

To update another beat, name the exact source and question in the prompt. The CWC bulletin currently needs a source review/manual import; the existing automated refresh covers IMD only. An inaccessible source should produce a logged gap and a legitimate manual-import proposal; it must not cause fabricated data. The site has no background updater: reviewed changes reach GitHub Pages only after a commit and push.

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

Use the actual evaluation timestamp in `--as-of`. The refresh command checks only the currently implemented IMD adapter and writes under ignored `data/candidates/`; it does not approve or deploy anything. The release gate checks the exact `dist/` manifest and review evidence, so a new approved source snapshot requires fresh reviews and a new `state/RELEASE_REVIEW.json` binding. Commit reviewed changes and push `main`; the existing GitHub Actions workflow deploys https://aaddymehndi94.github.io/india-water-watch/ . Inspect its run and smoke-test the live site. GitHub Pages is the maintained public host. Do not automate candidate promotion.

For a quick local root preview after `build:compact`:

```bash
python -m http.server 8000 --directory dist-compact
```

Open `http://127.0.0.1:8000/`. For the repository-prefix build, run `npm exec --yes --package=pnpm@12.6.0 -- pnpm preview -- --host 127.0.0.1` and open the printed `/india-water-watch/` address.

## Corrections and rollback

Record a correction in the claim ledger with a superseding claim ID and dated explanation; rebuild all exports and indexes. Preserve old source snapshots and release manifests. To roll back a hosted progress build, redeploy an earlier reviewed commit through the Pages workflow; do not rewrite history or silently change the observation date.
