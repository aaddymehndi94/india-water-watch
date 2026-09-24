# 08 · Multi-agent execution

## Use native workers, not an orchestration project

The parent is the interactive editor-engineer lead. There are eleven specialist role definitions in `.codex/agents/`, but **no more than six workers active at once**. Roles are capabilities, not an instruction to launch eleven continuous sessions. Two heavy browser/geospatial tasks at most. No recursive workers and no background token-burning watchdog.

Verify the installed CLI and the current official subagent documentation before activating project configuration. This starter uses the documented standalone custom-agent file form (`name`, `description`, `developer_instructions`) and the project concurrency setting as checked on 24 September 2026. Model selection inherits the user's active environment; do not hardcode a model name, assume account entitlement or alter global configuration. If local support differs, adapt the project config with a recorded decision, not silent degradation.

## Specialist desks

| Role | Owns | Deliverable | Independence |
|---|---|---|---|
| `source_auditor` | Legacy-claim/source audit | Exact source support and gap ledger | Separate from initial claim author |
| `hydrology` | Rainfall, reservoirs, groundwater methods | Comparable measurements and method notes | Reviewed by fact checker |
| `history_demography` | Historical analogues, population/demand | Eligibility sets and limitations | No inherited rankings |
| `economy_access` | Livelihoods, inequality, shared dependencies | Evidence-backed impact reporting | No invented losses |
| `institutions_reporter` | Official responses, local reporting, voices | Dated documentary tracker | Neutral, no external contact |
| `data_engineer` | Adapters, contracts, snapshots, transformations | Reproducible data pipeline | Cannot approve own headline math |
| `editor` | Narrative, information hierarchy, claim references | Plain-language coherent reporting | Works from reviewed evidence |
| `visual_designer` | Design system, charts/maps, reading journeys | Working components and screenshots | Not mere moodboards |
| `frontend_engineer` | Site integration, static routes, exports | Browser-tested build | Shared contracts controlled by lead |
| `fact_checker` | Numerical, source and editorial review | Blocking findings and recheck | Read-only independent audit |
| `quality_engineer` | Accessibility, performance, security, deployment | Reproducible test evidence | Separate from implementer |

The lead also owns release engineering and can merge roles when scope is small. It should not assign a subagent every five-line task.

## Wave plan

**Wave A:** source auditor + hydrology + history/demography establish the evidence reset and modern baseline; designer develops the reading/navigation system; lead resolves toolchain/contracts. No public data claims are rendered yet.

**Wave B:** data engineer builds adapters and normalization; economy/access and institutions desks research; frontend implements the verified vertical slice; editor drafts from accepted claims. Designers can work with clearly isolated synthetic fixtures in development.

**Wave C:** extend geography/history/outlooks; integrate reporting and update workflow; editor and designer perform a coherence pass. Rotate specialists out when their tasks finish.

**Wave D:** independent fact checker and quality engineer audit the complete candidate. Implementers fix findings; reviewers recheck. Lead prepares a publisher decision packet and artifacts.

No worker may write to another worker's ownership area without a handoff. Use task-owned files/worktrees. Lead alone merges changes to schemas, source registry, lockfiles, project state and release manifests. Workers can propose structured patches for shared records.

## Assignment contract

Each task gets: task ID; objective; input paths/source scope; owned paths; non-goals; acceptance checks; dependency IDs; limits; output paths; reviewer. Use `templates/AGENT_TASK.md`.

A task result includes findings, evidence IDs, changed files, calculation/test commands, test results, uncertainties, blockers and recommended next action. Avoid long raw browsing transcripts in the lead thread. Persist detailed logs locally; return concise actionable summaries.

## Safe concurrency

A read-only role file is not a guaranteed security boundary when the parent session changes runtime permissions. Current official Codex documentation says live parent overrides, including `--yolo`, can override child defaults. Inspect effective permissions during preflight. Prefer workspace-scoped permissions for a project ingesting untrusted external documents, and never treat the role label as a substitute for path ownership or independent review. If the operator has chosen a broader mode, do not secretly change it; explain the implication and keep task-level restrictions.

Before editing, inspect `git status`. A worker operates in disjoint paths or an isolated branch/worktree. Never have parallel package installs updating the same lockfile. Heavy tests run in a coordinated queue. Do not terminate unrelated user processes or reset branches to clean the workspace. Checkpoint only owned work. Review diffs and secret/rights exclusions before commits.

## Continuity and progress

Lead updates `state/PROJECT_STATE.json` and `state/HANDOFF.md` atomically after a gate or interruption. Track actual deliverables/tests, not invented percentages. Build a small local progress page or markdown view from task records only after the first vertical slice; it must not consume the project.

If a worker stalls, request a concise handoff and reassign once. If a source fails after three different legitimate attempts, log it and proceed with other work. Repeated reopening of the same source is not verification. Close completed workers to conserve context.

## Review hierarchy

Source discovery is not evidence inspection. Automated schema validation is not numerical verification. Numerical verification is not editorial support. Agent review is not external expert or human review. Each gets a distinct status. High-impact publication needs the appropriate checks, not four workers agreeing with the same unsupported sentence.

## Stopping conditions

Continue local work until the requested candidate and handoff are complete. Stop a particular publication claim/module when evidence is inadequate, not the entire project. Escalate only actual permission/credential/spending/right-of-reply barriers. Do not publish to prove progress. Do not weaken the contract or mark missing tests passed.
