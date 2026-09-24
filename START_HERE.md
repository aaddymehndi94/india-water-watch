# Start here

## What to do now

Create a folder called `india-water-watch`, extract the pack into it, and open Codex in that directory. You may initialize an empty Git repository first, or let Codex do that locally. Do not add any tokens or private files to the public repository.

Paste the full text of `FIRST_PROMPT.txt`. Keep the interactive lead session open so you can interrupt, ask questions, or redirect it. The lead owns the work plan and integration; specialists do bounded parallel assignments. This pack does not require a separate paid multi-agent orchestration service.

**Do not upload the earlier HTML as the site's evidence or landing page.** It is an unverified exploratory draft. The new project starts with an audit and fresh retrieval.

## What Codex should do without asking you

Inspect available tools and operating system; read the brief; identify current compatible stable dependencies; create the app and local environment; check source access; research the reporting questions; implement ingestion, charts, maps, story pages and tests; run independent reviews; correct failures; produce a local preview and portable release candidates. It should make reversible design/engineering decisions and record them rather than repeatedly asking you to choose colors or libraries.

If one source is blocked, Codex should log the limitation, try a legitimate alternate official endpoint or permitted manual-import path, and continue unrelated work. If a module cannot be supported, leave it honestly unavailable or omit it from publication rather than inventing facts. Do not stop the entire project for one missing district feed.

## When your involvement is genuinely needed

Public deployment; adding a domain; approving paid services; connecting credentials; contacting people; licensing third-party material; approving high-stakes reporting; or destructive changes to an existing repository. Codex can finish the local release candidate before asking for these actions. It must not spend money, send interview requests, or publish under your name automatically.

Human publication review is not the same as asking you to approve each coding step. The pack asks for one concise release review at the end, with the evidence needed to make that decision.

## What the first session should deliver

A real working website, not just another plan: national briefing, interactive geography explorer, meaningful historical comparison, sourced explainers, update desk, methodology and journalist downloads. Complete all feasible gates. Every visible module is either backed by reviewed evidence or explicitly shows why no current result is available.

The complete route and coverage targets are in the brief. The deliverable includes a host-ready `dist/`, ZIP, source code, frozen dependencies, data provenance, tests, local screenshots, update commands and a gap report. It must distinguish **built**, **data-verified**, **editorially reviewed**, and **deployed**. These are not interchangeable.

## Reopening tomorrow

Paste `RESUME_PROMPT.txt`. The lead reads persistent state and continues from the last defensible checkpoint. It should not re-read the entire web or rebuild already tested modules unless something changed.

## Updating the published site

Paste `UPDATE_PROMPT.txt`, optionally preceded by a scope such as “Refresh all current observations and news; keep the design unchanged.” The refresh runs discovery, retrieval, data validation, change detection, affected-claim review and tests. It produces a candidate release and a readable change brief. Routine updates should not redesign the site or reinstall the toolchain.

Use `AUDIT_PROMPT.txt` for an adversarial review. Use `PUBLISH_PROMPT.txt` only when you have approved a specific release and selected a destination.

## Hosting

Default: public GitHub repository + GitHub Pages with a tested subpath build. Alternative: a root-path static build for Cloudflare Pages. Drag-and-drop has a documented asset-count limit, so the pack specifies a compact export as well as the full build. AWS means uploading files to an origin such as S3 and configuring CloudFront; CloudFront is not itself a folder-upload service.

The starter creates no remote repository or hosting account. The publisher's 24 September 2026 instruction authorizes use of the existing `aaddymehndi94/india-water-watch` repository and GitHub Pages as a shareable progress site. Deploy tested, accurately labeled progress and reviewed public claims as checked checkpoints land. Candidate data must never become public merely because a scheduled build ran. See the hosting guide for deployment checks and limits.

## Inspect this pack before starting

```text
python tools/validate_starter.py
python -m unittest discover -s tests -v
```

On Windows, `py` may replace `python`. These checks need no third-party Python packages. They check the starter and reference logic, not whether India is in a water crisis. A passing starter check must never be shown as “the reporting is verified.”
