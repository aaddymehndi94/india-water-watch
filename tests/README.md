# Starter tests
Run `python -m unittest discover -s tests -v` from the repository root. Python 3.10+ is supported; no third-party packages are required. TOML structural checking uses `tomllib` when Python 3.11+ provides it.

These tests exercise illustrative arithmetic, strict comparison contexts, freshness/expiry handling, failure-closed structural release checks and pack integrity. Fixtures are invented, temporary and not real observations. There is no tested production website yet. Do not mislabel this suite as verified journalism, scientific peer review or a deployment test.

When implementation starts, replace starter-only invariants with real app tests. Add full JSON Schema validation with format enforcement and foreign-key checks; source-adapter fixtures; cross-geography/cohort tests; unit/e2e/accessibility/visual tests; root/subpath hosting tests; and independent source support review. See docs/12-QUALITY_AND_TESTS.md.
