# Gemini context-counterexample reviewer v1

Status: **NO_GO / zero inference**. No model or network call was made. Do not invoke `qualify.mjs` or `run.mjs` while blocked.

## Exact frozen-frame availability

`rebuild-reviewed.mjs` reconstructs the canonical frame from the four exact cycle-1 extracted streams, verifies their sealed hashes, scans tracked model-probe text blobs at explicit baseline commit `31cb74af595567cd803a010e6fe5fceea4a29db6`, and scans the content-addressed preserved-dirty archive. Production and fixtures use the same locale-independent `presentationMatch` implementation for raw/normalized equality, containment, and folded-token presentation across source, target, context, revision ID, and authored mutation candidates in every prior scalar or plain-text/request value. Assignment fails closed when any mutation presentation matches the frozen manipulation/all-presentation corpus.

The exact result for this **frozen 127-row frame only** is **2 eligible / 64 required, shortfall 62**: 106 primary semantic/path rejections and 19 additional source-or-revision presentation rejections. This is not a full-inventory availability claim. `HISTORICAL_TASK_BINDING` and `FULL_INVENTORY_AVAILABILITY_NOT_ESTABLISHED` remain explicit hard gates.

## Dormant execution integrity

Qualification must preserve exact request, RAW stdout/stderr, CLI-version stdout/stderr, and model-list stdout/stderr bytes in `QUALIFICATION-MANIFEST.json`; verification rebuilds the request, reparses RAW, rejects tool signals, recomputes fixture assertions, and enforces freshness. Immediately before every experimental invocation, the runner immutably captures exact `agy --version` and `agy models` stdout/stderr bytes; phase RAW manifests and scoring bind that execution CLI snapshot alongside canonical request-manifest/map, shard, sample, request, RAW, phase/protocol/run, and candidate hashes. Atom credit allows exact one-character spans but never awards one-character substring credit. `produce-selection.mjs` persists and validates the frozen critical-path latency tie-break; selection remains blocked until that artifact exists.

`post-run-validate.mjs` enumerates dynamic artifact classes. It emits `NO_RUN` only when none exists; orphan or partial dynamic files are `NO_GO`.

## Zero-call checks

```bash
node rebuild-reviewed.mjs
node test-fixtures.mjs
node preflight.mjs --phase qualification
node post-run-validate.mjs
for f in *.mjs; do node --check "$f"; done
```

Preflight is expected to return `NO_GO` because the pool and authorization gates are closed.
