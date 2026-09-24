# 17 · Cost, reliability and maintainability

## Default operational footprint

One public source repository; static hosting; an operator-triggered refresh; no user accounts; no mandatory paid APIs; no browser-side LLM; no commercial tile dependency. Optional schedules create reviewed candidates after authorization. A domain is optional and paid domain purchases require approval.

This architecture avoids a per-reader model call and most backend operations. Actual hosting bandwidth/build/storage limits still apply. Measure published asset bytes and request paths; do not promise unlimited free scale or quote a monthly bill without current pricing and usage assumptions.

## Agent cost discipline

Six workers maximum, not eleven simultaneously. Cache retrievals, normalize once, reuse common calculations and avoid regenerating all stories for a small update. Keep substantive source work in specialist threads and deliver concise structured results to the lead. No endless aesthetics loop, source retry loop or automatic model upgrade.

Use expensive reasoning for contested source interpretation and methodology, not repetitive file transformations. Do not assume any particular model is cheaper/available without checking the active account and current documentation. Inherit the user's chosen model unless a change is justified and authorized.

## Data volume

Do not put national daily gridded archives, source PDFs, raw imagery or hundreds of duplicate build snapshots in Git. Keep permitted compact normalized tables and release metadata; cache heavy working material locally or in authorized storage. Chunk district data by state/year; lazy-load only what the reader requests. Keep a source re-fetch recipe and integrity hashes when redistribution is restricted.

## Observability

Maintain source health, last successful/attempted retrieval, observation watermark, parser version, error history and coverage. Public status excludes internal secrets and personal details. Alerting/notifications are optional integrations requiring real configuration; do not claim them installed because a document describes them.

## Reliability

No partial release. Validate a full candidate snapshot and atomically publish it. Retain the last verified snapshot when sources fail and show data age. A hard failure of one feed does not require taking down explanatory content. Maintain a rollback bundle and a correction process that survives rollback.

## Maintenance ownership

Document who may approve publication, update methods, approve sensitive reporting and manage hosting. Keep decisions and source contracts in the repo. The maintainer should be able to say “refresh and tell me material changes” rather than manually edit twenty files.
