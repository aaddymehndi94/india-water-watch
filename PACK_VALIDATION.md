# Validation of this starter pack

Prepared and checked on 24 September 2026 using Python 3.13.5.

| Check actually performed | Result |
|---|---|
| `python tools/validate_starter.py` | PASS: required files, JSON parsing, task DAG and TOML parsing |
| `python -m unittest discover -s tests -v` | PASS: 60 tests |
| Parse all shipped Python source with `ast.parse` | PASS |
| Check all 9 JSON Schemas with the Draft 2020-12 meta-schema | PASS |
| `python tools/release_gate.py --publication` | EXPECTED REJECTION: no real site/data/reviews/authorization |

Actual command logs are under `validation/`. The separate schema meta-check used the container's installed `jsonschema`; it is not required for the dependency-free starter tests. Codex must add full production record/schema/format and foreign-key validation during implementation.

## Not established by these checks
No production website was built or browser-tested. No live dataset, historical rank, 2026 crisis assessment, hydrological model, economic estimate or journalism claim was verified by this suite. No interview occurred. No Codex worker was executed in the user's environment. No host, public repository, domain or scheduled job was created.

The source registry is a discovery/access ledger with explicit limitations, not proof of numerical source support. Role configuration follows documentation inspected on the preparation date; actual CLI compatibility must be checked during G0. The release gate is structural, not an authentication system or a substitute for source support and human publication review.

The tests use illustrative arithmetic and temporary structural fixtures. They do not export a fake site or any synthetic observations into production stores. The correct behavior of the unimplemented starter is to pass its starter tests and fail publication.
