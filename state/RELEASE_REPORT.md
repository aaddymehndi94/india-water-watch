# India Water Watch · G10 reviewed progress candidate

**Candidate:** `candidate-20260924-6705f01bb901` · built 24 September 2026. This is an agent-reviewed static progress publication; no human editorial sign-off is claimed. Primary host: https://aaddymehndi94.github.io/india-water-watch/ . The commit and live deployment status are recorded separately in `state/DEPLOYMENT_REPORT.md` after each push.

## Built and verified

- Astro 7.3.4 static site with original responsive editorial layout, system-aware saved light/dark theme, React evidence workbench, Pagefind search, source pages, journalist desk, 36 state/UT records, district and basin context, and chaptered national story. Root and GitHub repository-prefix builds each generated **110 HTML pages and 250 files**. There is no runtime server or paid dependency.
- Approved public projection: **17 source-linked claims, seven numeric observations, 11 evidence records and 43 geography entries**. Five IMD rainfall observations end **23 September 2026**; two CWC monitored-reservoir observations are dated **10 September 2026**. The Karnataka order was issued **22 September** following an assessment through **16 September**. Three brief IMD historical cases cover completed 2002, 2009 and 2025 seasons; 2026 is not ranked against them.
- Homepage now distinguishes rainfall, reservoir storage, household access and documented response. Karnataka's 53 additional declared taluks are reported as a formal government action, not as proof of relief delivery or measured loss. The dated IMD forecast is separated from observed conditions and its validity is not an observation watermark.
- `python tools/validate_starter.py`, approved-schema validation, **80 Python tests**, Astro check (**43 files, zero diagnostics**), root and repository-prefix builds, journalist exports, ZIP integrity and the structural release gate passed. Independent agent source/arithmetic/editorial review is in `reporting/g10_fact_review.md`; independent browser, visual, sampled accessibility and security review is in `reporting/g10_quality_review.md`. That QA passed **75/75 browser checks per profile** and found zero broken or wrong-base local targets among **2,579 references per profile**.

## Coverage and review limits

- State/UT pages provide a sourced roster and coverage status, not state rainfall measurements. Karnataka has a sourced action record. No approved numeric district, basin-flow, groundwater, September household-service, crop-loss or economy outcome series is published. No licensed boundary map is bundled. Missing remains unknown, not zero or evidence of normal conditions.
- The 17 September CWC bulletin appears on the official index, but its PDF returned 404 during this review; the approved 10 September values retain their own date. IMD historical comparison uses a hashed official HTML snapshot because the live page timed out on an independent revisit. Brief factual extracts are published with attribution; source HTML, graphics and PDFs are excluded from the static packages.
- Agent checks are not human review. Full screen-reader/WCAG certification, external legal rights opinion, field reporting, mobile network performance benchmark and verified later IMD/CWC issues were **not** completed. No India-wide drought or “worst year” conclusion is asserted. See `state/COVERAGE_AND_FRESHNESS.md` for source watermarks and gaps.

## Portable files and exact commands

- GitHub repository-path ZIP: `release/site-github.zip` (unzip into the project Pages path).
- Root-path ZIP: `release/site-compact.zip` (drag its contents to a static root host).
- Journalist files: `exports/journalists/` and `release/journalist-exports.zip`.
- Screenshots and browser reports: `artifacts/qa/g10/` (local ignored artifacts).

```bash
# Local root preview
python -m http.server 8000 --directory dist-compact
# Open http://127.0.0.1:8000/

# Rebuild repository-path publication after reviewed changes
PUBLIC_SITE_URL=https://aaddymehndi94.github.io PUBLIC_BASE_PATH=/india-water-watch/ npm exec --yes --package=pnpm@12.6.0 -- pnpm build
python tools/release_gate.py
```

The prompt-driven source refresh and update procedure is `docs/UPDATE_PLAYBOOK.md`. The existing GitHub Actions workflow deploys reviewed `main` pushes; inspect the workflow and smoke-test the hosted release. The secondary Sites URL requires a separate synchronized version push/deployment. There is no unattended source-promotion or site-update process.
