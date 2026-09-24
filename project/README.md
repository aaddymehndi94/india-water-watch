# Work and acceptance contracts
`tasks.json` contains the dependency graph. It is a starting work breakdown, not proof that workers ran. The lead can split tasks and change ordering with a reason, but must not delete difficult coverage requirements to claim completion. All tasks start `not_started`.

`acceptance.csv` is a review matrix. `not_run` is intentional. Use `passed`, `failed`, `blocked`, or `not_applicable_with_reason` only with a concrete evidence path and reviewer. A feature can be withheld instead of fabricated; explain the withheld scope. A P0 requirement for something that is published cannot be waived by calling it a prototype.

The graph is not an instruction to launch every ready node simultaneously. Respect six-worker concurrency, shared-path leases and the lead-owned integration order. Tasks with `lead` ownership run in the interactive parent; they are not a missing custom-agent definition.
