# Gemini original-items prompt/schema matrix v3 structured output

Fresh ZERO-CALL successor for the reference-free 2×2 serialization-conformance matrix. It preserves all 12 reviewed v2 model-facing requests byte-for-byte, including order, factors, exact original 16 D items, metrics, aggregates, null/zero handling, contrasts, DiD, and interpretation rules. No predecessor ledger row, capture, RAW, RESULT content, metric, process count, or model output is imported.

`PREDECESSOR-BINDING.json` binds both immutable terminal predecessor trees and RESULT files by hashes only. Source bindings remain read-only. The sole behavioral change is local envelope parsing: outer stdout must be duplicate-free JSON object with `status === "SUCCESS"` and an own `structured_output` property whose value is a non-null, non-array object. `structured_output` is passed unchanged to the strict payload parser and is the only model-result channel. `response` is never parsed, projected, compared, normalized, or used for validity or metrics, and there is no response fallback.

Canonical RAW provenance records only `authoritative_channel`, response presence/type, and, for a string response, UTF-8 byte length and SHA-256. It never copies response content. Exact ledger replay regenerates byte-identical canonical RAW from captured stdout; the complete stdout capture hash remains the trust root for ignored response bytes.

## Zero-call workflow

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs   # expected: NO_GO_REQUIRED_GATES, NO_RUN, 0/0
```

The package only reads task-owned gates. It never creates or edits them. After independent package review and authorization, run each registered cell once in `frozen/REQUEST-MANIFEST.json` order with `node run.mjs --cell CELL`; no retry is permitted. Membership failures and zero candidates continue; structural or infrastructure failures stop. `node post-run.mjs --write` deterministically creates the reference-free result after execution.

No sealed reference, adjudication, predecessor dynamics, correctness score, effectiveness claim, model-list call, qualification call, or network call belongs in this package at P0. A zero-candidate run makes the primary interpretation `INCOMPLETE_MATRIX`; null rates are never treated as zero.
