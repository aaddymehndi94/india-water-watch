# Empty production data is intentional

No current or historical water observations have been established by this starter. The JSON arrays are empty contracts for Codex to populate only after actual source retrieval, verification and rights review. The earlier chat/HTML figures are quarantined and are not imported into production.

Keep working source files in ignored `data/raw/` or `.private/`, not public Git. The implementation should introduce versioned `candidates/` and `approved/` snapshots with explicit migrations from these bootstrap files. Test fixtures belong under tests and must never reach public output.
