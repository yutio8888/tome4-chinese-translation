# ROUND-0003 context input

Status: `NO_GO_ROUND_0003_CONTEXT_INPUT_REVIEW_REQUIRED`.

The authorized surface auditor call was recovered byte-for-byte from durable Pi session `01a05826-b038-7d29-b437-c5c3e3f19578` for agent `216516d5-3b1c-4ec4-b0f6-8d0e984bf698`. The one-call allowance is consumed (`started=1`, `remaining=0`). The exact minified response SHA-256 is `59dcb66b519ee97e97b421b21405c1a0aee943f41c798c30cf5d150e8c4352e1`; it contains two ordered `PASS_SURFACE` verdicts.

Canonical ROUND-0003 surface results are frozen at:

- `SURFACE-RECORDS.json`: `157af1f76c6dfd055db28080e043d066b93ec5fd38afaa5aa083dd79b5eb841d`
- `SURFACE-AGGREGATE.json`: `de5db2dfd18898c4f65c9b8ad2ef90821f2ba331a15ef2ac73dcccb5f9f6dc33`

The context input contains exactly `V4-D-D05`, then `V4-C-D06`. It is derived from fixed source commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` and binds the unchanged completed-two-round state. Queue and anchors retain lineage/reserve integrity hashes; the auditor-facing view excludes prior verdict/evidence, lineage/reserve/rank, rejected revision, reviewer/model, reference and adjudication data.

Frozen context hashes:

- `CONTEXT-QUEUE.json`: `a8b4d2b864332422e8677e9c8c00e88489fb503df2311a23adfb54f4d980566d`
- `CONTEXT-SOURCE-ANCHORS.json`: `e91a195e38271ce4d9cb5611e9a87283921078cd15c61c688551c48dbce56dc1`
- `CONTEXT-QUEUE-VIEW.json`: `900fe68d898303e1fcd64567119c33d6471119a5b9a5cbfc74ad41cc7dc0e44e`

The two fixed source blobs are `sorcerer-end.lua` (`aedf48a1…`, source lines 228–231, bytes `[11672,11930)`) and `pre-charred-scar.lua` (`6e81e213…`, source lines 21–23, bytes `[799,1082)`). Each view item includes the complete `_t` construct and exact three-line before/after windows.

The separate `public-context-replay.mjs` and dedicated `round-0003-context-replay.mjs` report `completed_rounds=2`. `public-context-preflight.mjs` and `round-0003-context-preflight.mjs` return `NO_GO_ROUND_0003_CONTEXT_INPUT_REVIEW_REQUIRED` with static integrity PASS. The 169-file surface candidate, including its original public/dedicated surface entrypoints, remains byte-frozen. Independent normal and senior context-input review plus a combined gate are required before any context auditor call. No context dispatch/completion/review/gate record exists yet; the candidate contract reserves those mutable lifecycle paths but does not fabricate receipts or templates before an actual dispatch.

No context auditor call, context completion/results, replacement, release, ROUND-0004, formal experiment/network action, or Git action is authorized.
