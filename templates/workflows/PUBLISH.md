# Publication workflow specification (not an enabled workflow)
First release is manual, with an explicit destination and immutable candidate identifier. Use a reviewed static artifact, not a fresh unreviewed scrape in the deployment job. Run the release gate and bind approval to the exact manifest hash.

For GitHub Pages: verify current official setup, least-privilege contents/pages/id-token permissions, environment protection, upload/deploy actions and subpath configuration. Build commands and base URL come from the approved profile. No credential belongs in client JavaScript.

For Cloudflare Pages: separate root build; enforce current file/asset limits; compact variant if dashboard drag-and-drop is required. For S3/CloudFront: explicit account/bucket/domain authorization, private origin where appropriate, scoped upload, cache strategy and cost review. CloudFront is a CDN, not the upload folder.

After deployment, fetch actual public routes and a source drawer/data export; compare manifest and observation watermarks; record URL, deployment ID, checks and rollback target. A successful workflow alone does not establish correct public content.
