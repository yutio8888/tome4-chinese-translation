# Gemini original-items prompt/schema matrix v2 envelope recovery

Fresh ZERO-CALL successor for the reference-free 2×2 serialization-conformance matrix. It preserves all 12 v1 model-facing requests byte-for-byte, including order, factors, exact original 16 D items, metrics, aggregates, null/zero handling, contrasts, DiD, and interpretation rules. No v1 execution ledger, captures, RAW, RESULT, metric, process count, or model output is imported.

`PREDECESSOR-BINDING.json` binds the immutable full terminal v1 tree, RESULT, and MANIFEST. Source bindings remain read-only. The only behavioral change is local envelope parsing: `structured_output` is authoritative; a simultaneous `response` must be exact or may add only top-level `toolAction` and/or `toolSummary`, while every payload key remains present and deeply equal. Duplicate keys, missing payload keys, payload mismatches, invalid response JSON, and unknown extras fail closed. Observed allowed extra-key names are recorded only in canonical RAW envelope metadata and never enter metrics. A response-only envelope must itself satisfy the exact output schema and may not contain envelope extras.

## Zero-call workflow

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs   # expected: NO_GO_REQUIRED_GATES, NO_RUN, 0/0
```

The package only reads task-owned gates. It never creates or edits them. After independent package review and authorization, run each registered cell once in `frozen/REQUEST-MANIFEST.json` order with `node run.mjs --cell CELL`; no retry is permitted. Membership failures and zero candidates continue; structural or infrastructure failures stop. `node post-run.mjs --write` deterministically creates the reference-free result after execution.

No sealed reference, adjudication, predecessor dynamics, correctness score, effectiveness claim, model-list call, qualification call, or network call belongs in this package at P0. A zero-candidate run makes the primary interpretation `INCOMPLETE_MATRIX`; null rates are never treated as zero.
