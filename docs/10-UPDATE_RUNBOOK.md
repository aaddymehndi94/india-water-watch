# 10 · Refresh and maintenance

## Static does not mean stale, and “live” does not mean unreviewed

A static site publishes versioned reviewed snapshots. Source retrieval and reporting updates happen in an operator-triggered or explicitly configured scheduled workflow. Merely hosting the files does not keep them current. The site must make its actual update mode and dates obvious.

## Five clocks

Every relevant module preserves: observation period/cutoff; source publication/issue time; successful retrieval time; editorial verification time; release/deployment time. Also retain the last attempt time and error separately. A check with no new data does not advance the observation or “story updated” date.

Freshness is product-specific. Establish expected publication cadence and grace period during adapter review. A daily rainfall product can become stale quickly; an annual groundwater assessment remains annual even when retrieved today. Show both source age and cadence. No single global “updated today” stamp may imply all datasets are current.

## Operator interface

`UPDATE_PROMPT.txt` is the natural-language control. The implementation must map that to a reproducible refresh command, produce a candidate release, and summarize material changes. Changing the scope to “Karnataka only” should not inadvertently rebuild every historical dataset or rewrite unrelated articles.

## Transactional refresh sequence

1. Read approved release, source watermarks, state and last errors. Fix the evaluation `as_of` timestamp for reproducibility.
2. Select sources due by cadence and search for new relevant developments/corrections. Use conditional requests; log exact queries/retrievals. Discovery can add a candidate source but cannot instantly bless it.
3. Fetch into a new immutable candidate run; validate content type, bytes/hash, product date and expected schema. Reject error/login HTML disguised as a dataset.
4. Normalize and validate units, IDs, boundaries, ranges, completeness, duplicates and source revisions. Preserve previous approved data if any step fails.
5. Compute semantic changes: new observations, corrected observations, methodological revisions, expired forecasts, source loss and newly filled gaps. An HTML formatting change alone is not a new drought development.
6. Traverse evidence dependencies. Invalidate affected claim reviews and recompute charts, map bins, local summaries, exports, social cards, search and feeds. Do not leave contradictory old numbers in prose.
7. Review meaning. Numerical provider revisions, changes in classification, allegations, novel forecasts, major loss figures and actionable safety guidance require the appropriate independent/human review. A threshold crossing is not itself proof of crisis escalation.
8. Build/tests/preview from a single candidate snapshot. Never mix half-old/half-new data. Generate `UPDATE_BRIEF.md`, machine diff, source health and review queue.
9. Publish only under explicit authorization policy. Atomic release swap; preserve prior release and corrections. No half-written public JSON.
10. Check hosted version and essential routes if deployed. Record outcome. If nothing changed, record the successful check and leave original observation/story dates intact.

## Cadence defaults are proposals, not facts about sources

Discover actual source schedules first. A reasonable operator policy may check rainfall and current official bulletins daily, reservoir data when a bulletin is due, groundwater/population only for new releases, and selected news daily. Do not poll a yearly report hourly. No promises of minute-by-minute currentness from daily/weekly sources.

## Scheduled automation

Implement a manual `workflow_dispatch` path first. Optional schedules should run deterministic permitted-source retrieval, validation and creation of a reviewable candidate/change report. An LLM reporting run is optional and requires an authorized account/budget; do not assume interactive Codex login can be reused in CI or that an API is free.

Automatic publication is disabled initially. After explicit policy approval, low-risk mechanical updates to established datasets can be eligible if all checks pass. New sources, methods, narratives, declarations and sensitive claims remain review-required. A failed review must not cause the process to fall back to silent publication.

GitHub scheduled workflows are not a guaranteed real-time scheduler. Verify current delay/inactivity behavior and quotas in official documentation. Surface missed runs in `data-status`; do not hide behind a permanent “live” badge. The browser may compute stale/expired presentation from embedded expiry metadata, but cannot turn an old snapshot into new reporting.

## Corruption and rollback

Keep release-scoped JSON asset hashes and a small manifest. Roll back to an earlier **verified** snapshot only with its original dates and a visible reason. Never restore a retracted false claim merely because its software build works. Retain correction records across rollback. No service worker caching of active alerts at launch; otherwise an explicit validated cache-expiry policy is required.

## Monthly maintenance checklist

Review source terms/access, dependency/security updates in a separate change, boundary revisions, broken links, open corrections, stale human-information contacts, unmatched geographies, search-index leakage, hosting usage and unused features. Do not silently change a historical baseline in a normal daily update.
