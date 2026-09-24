# G16 · Replayable IMD source snapshot

The IMD adapter already saved exact fetched HTML bytes under `data/raw/imd/<full SHA-256>.html`, a Git-ignored path. G16 makes that path and its full SHA-256 explicit in both the parsed candidate's `source` metadata and each successful refresh attempt report. It does not create a second raw copy. The path is relative to the repository root so a candidate can be replayed on a machine where the ignored raw snapshot has been transferred securely.

`save_raw_snapshot` writes with an immutable, atomic no-overwrite operation and verifies the hash after writing. If a file already exists at the content-addressed path with different bytes, the adapter fails rather than replacing it. The refresh persists exact bytes even for a no-change observation check, while reusing the parsed candidate when its source and metadata are already current. Older candidates without the new path metadata receive one repair candidate; subsequent identical checks are no-change. Raw snapshots, candidate JSON and attempt reports remain outside approved/public data, and no promotion or deployment occurs.

## Verification

```sh
python -m unittest tests.test_imd_adapter tests.test_refresh -v
python pipeline/refresh.py --scope all --as-of 2026-09-24T17:06:00+05:30
```

All **13 focused tests passed**, including exact-byte replay, matching hashes in candidate and attempt metadata, no duplicate snapshot on a no-change run, and refusal to overwrite a corrupted existing snapshot. The live refresh on 24 September 2026 created candidate `data/candidates/imd/2026-09-24-5d1d35cb5f1bdbd6-20260924113602834064.json` and attempt report `data/candidates/refresh/attempts/20260924T113600Z-20260924113602834064-5d1d35cb5f1bdbd6.json`. A second live run returned `no_change` and reused that candidate. Both reports identify `data/raw/imd/5d1d35cb5f1bdbd62ffe11ad0e7854ff91aaafec37dce8298550d0e510baeb34.html`; independently hashing its **255,416 exact bytes** matched the recorded SHA-256. The candidate remains unapproved.
