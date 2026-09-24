# 11 · Hosting and release packaging

## Default: GitHub repository + GitHub Pages

Use a public repository for source and permitted normalized data, with GitHub Pages for the initial static publication. Official GitHub docs checked on 24 September 2026 say Pages is available for public repositories on GitHub Free. They describe a 1 GB published-site cap and a soft 100 GB/month bandwidth limit; verify the current limits before launch. This is not unlimited hosting and is not intended as a transactional commercial SaaS host.

Build once in CI, deploy reviewed static artifacts, and keep source ingestion out of the visitor path. The site can support a large readership economically when initial payloads and map/data chunks are small, but do not promise a capacity figure without measuring requests and bytes.

The publisher's 24 September 2026 instruction authorizes a GitHub Pages **progress site** in the existing `aaddymehndi94/india-water-watch` repository. A successful local review and push to `main` may update it. The site must distinguish reported observations, evidence gaps, local build status, and deployment time. Candidate data do not auto-promote; a rebuild of old observations does not refresh their observation date. Final editorial release status and sensitive human review remain separate. Configure Pages from GitHub Actions using pinned immutable action SHAs and minimal workflow permissions. Never deploy untrusted pull-request code.

GitHub project sites commonly use a `/<repo>/` prefix. Set `site`/`base`, route helpers, asset paths, Pagefind base, chart downloads, canonical URLs, Open Graph images and internal links consistently. Test the exact prefix locally, including direct URL refresh. Do not fix paths with a brittle browser redirect hack.

## Drag-and-drop: Cloudflare Pages

Prepare an ordinary root-path static build. The official Direct Upload documentation checked for this pack lists **1,000 files for dashboard drag-and-drop**, versus **20,000 using Wrangler**, and **25 MiB per file**. Verify at deployment because limits can change. The documentation also distinguishes Direct Upload and Git integration project modes; check that choice before creating a project.

A full district/source-site plus search chunks can exceed 1,000 assets. Produce a **compact profile** that retains national/state pages and serves district/source details via grouped explorer data. Count the entire output, including search chunks, fonts and download assets. Target fewer than 900 files for margin. Otherwise use the full build through the supported CLI/Git path and state clearly that it is not dashboard-drag-and-drop compatible.

Outputs:

- `artifacts/releases/<id>/site-root.zip`: root-path build, includes `index.html` at ZIP root.
- `artifacts/releases/<id>/site-github.zip`: verified repository-prefix build when applicable.
- `artifacts/releases/<id>/site-compact.zip`: file-limited root-path build, same verified content semantics.
- `manifest.json`, file-count/size report, checksums, verification report and rollback notes.

Do not label one path-specific ZIP universally deployable without rebuilding. A static site is hosted over HTTP(S); double-clicking `index.html` from a local filesystem may not support module loading/search correctly. Provide a local HTTP preview command.

## AWS: S3 origin + CloudFront

CloudFront is a CDN, not a drag-and-drop file store. An AWS deployment uploads `dist/` to an origin such as S3 and configures distribution, HTTPS, caching and routing. Prefer a private S3 REST origin with appropriate origin access control when using this architecture; verify current official instructions before deploying.

Astro creates directory-style pages. A private REST origin does not automatically serve nested `index.html` for every directory request. Implement and test a suitable edge rewrite, explicit `.html` routes, or another documented routing strategy. A root default object alone is insufficient for nested routes. Avoid blindly mapping every error to homepage HTML, which breaks SEO, search and real 404s.

No buckets, domains, paid distributions or account permissions are created by this starter. The agent prepares infrastructure instructions and uses it only after explicit authorization. Record expected billing exposure and budgets before provisioning.

## Cache strategy

Fingerprint static assets. Serve release-scoped immutable data assets and keep the small current-release manifest/HTML with an appropriate refresh policy for the host. Updates should not mix data versions. Expired forecasts remain archived with dates, not highlighted as active. The browser must not cache an emergency instruction forever.

## Public build exclusions

Reject `.env`, secrets, private reporting notes, raw restricted documents, test fixtures, synthetic series, quarantine ledgers, development state and credential-bearing URLs. Only publish designated build output. The Git repository may contain audit metadata, but not private source material or invented current observations. Review Git history before first public push.

## Workflow contracts

Templates in `templates/workflows/` are specifications. The progress-site workflow runs checks, builds from reviewed `data/approved` records, and deploys on checked `main` pushes. A candidate-refresh job may retrieve and upload review artifacts but never write approved data or deploy automatically. The editor checks each proposed content update before merging. A safety gate's boolean field is not an identity/authentication mechanism by itself.

## Release manifest

Record release ID; build time; source observation watermarks; approved dataset/claim IDs; hashes; Git commit; schema/toolchain versions; exact scope; gaps; human review references where applicable; publisher authorization; target profile; test evidence; asset counts and sizes. A release's metadata must describe the actual files shipped.

## Final hosted smoke test

Load homepage, a state, a district deep link, history, an expiring forecast, a source record, search and one download. Test non-existent routes, mobile layout, source drawer, map/table agreement and date labels. Confirm the displayed release matches the approved manifest. Record the actual URL only after the deployment succeeds.
