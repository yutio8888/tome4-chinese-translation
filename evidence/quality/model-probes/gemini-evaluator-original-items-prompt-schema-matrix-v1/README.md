# Gemini original-items prompt/schema matrix v1

Fresh ZERO-CALL package for a reference-free 2×2 serialization-conformance matrix. It freezes P0/S0 from execution-v5, P1/S2 from the clarified conformance package (S2 changes only the item-id regex to `^[DC]-I[0-9]{3}$`), and the exact original 16 D items/order.

Base P1 is SHA-256 `af8729b37404cd2a3b84b6f626bf65d79f1709384cdc86cefa3f3bfba2406e6c`. S2 registers the field name `evidence_quote`; preserving the source conformance behavior therefore mechanically substitutes the exact token `` `evidence` `` with `` `evidence_quote` `` when P1 is paired with S2. This is an S2 factor operation, not another prompt treatment. The effective P1S2 prompt is SHA-256 `26e8b83830b8a8588f352dabc66d298948df69eb83985816b9e2ebc12ff72aed`. The frozen request manifest records both base and effective prompt identities and the registered transform.

## Zero-call workflow

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs   # expected: NO_GO_REQUIRED_GATES, NO_RUN, 0/0
```

The package only reads task-owned gates. It never creates or edits them. After independent package review and authorization, run each registered cell once in `frozen/REQUEST-MANIFEST.json` order with `node run.mjs --cell CELL`; no retry is permitted. Membership failures and zero candidates continue; structural or infrastructure failures stop. `node post-run.mjs --write` deterministically creates the reference-free result after execution.

No sealed reference, adjudication, predecessor capture/RAW/result, model output, correctness score, effectiveness claim, model-list call, qualification call, or network call belongs in this package at P0.

A zero-candidate run makes the primary interpretation `INCOMPLETE_MATRIX`. Null rates are never treated as zero; paired gain requires finite non-null rates for both members of every pair, and `DESCRIPTIVE_MATRIX_NO_OBSERVED_DIFFERENCE` requires all four conditions and all 12 informative runs. Partial condition aggregates remain descriptive, while contrasts are null for an incomplete matrix.
