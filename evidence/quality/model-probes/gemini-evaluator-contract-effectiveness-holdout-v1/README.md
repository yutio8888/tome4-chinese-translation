# Gemini evaluator contract effectiveness holdout v1

Zero-call frozen package comparing **BASELINE P0+S0** with **HARDENED P1+S2** under mandatory authoritative `structured_output`.

## Frozen samples

- H1: 24 items = the 12 registered controlled mutations plus 12 independently source/host-verified clean controls from 12 other origins. All 24 source strings and origin revisions are unique.
- H2: 24 natural items = 12 tracked confirmed-defect historical revisions and 12 independently fixed-source-verified clean revisions.
- H2 defect targets are reconstructed from the bound production batch and translation baseline commit, never repaired HEAD.
- The 12 former clean siblings were replaced by clean controls from bound P1/P2 inventories. H1 controls are disjoint from H1 mutation origins, all H2 origins, and the predecessor P1/S2 design request.
- `sealed/REFERENCE.json` contains labels, hidden mutation originals/correct targets, adjudication bindings and deterministic matching anchors. Hidden mutation targets do not occur verbatim in any model-facing target or request.
- `host-validation.mjs` is the local value-level validation API. It proves H1 source/origin uniqueness, inventory/host bindings, design/H2 exclusion, and hidden-target disjointness. It is intentionally outside the runner dependency closure.

## Conditions and execution

`DESIGN-CONTRACT.json` freezes the 12-cell interleaving, three repetitions per dataset/condition, one process/call per cell, one attempt and no retry. `ROUTE-CONTRACT.json` pins agy and the requested model/effort/mode. Each spawn runs with `cwd` set to a fresh private directory containing only `request.txt` and `schema.json`; temporary runtime storage is a sibling directory and the whole private root is removed after capture.

All 12 requests uniformly compact-serialize input and schema JSON and omit a terminal newline. These are registered deviations from the predecessor's pretty-printed serialization and trailing LF; applying them identically to both conditions removes request formatting as a between-condition confound.

`structured_output` is the sole payload. `response` is never interpreted or used as fallback; canonical RAW records only its presence/type and, for a string, UTF-8 byte length/hash. Duplicate keys anywhere in the outer envelope or nested payload are rejected. Exact quote/span membership failures and zero-candidate payloads remain valid outcomes; infrastructure or strict structural failures stop later cells.

The runner import closure deliberately excludes `scorer.mjs`, `host-validation.mjs`, `post-run.mjs`, and `preflight.mjs`. Only the local host validator and scorer paths can parse the sealed reference. `post-run.mjs` calls the scorer only after all 12 cells are strictly successful.

## Deterministic effectiveness scoring

`METRICS-CONTRACT.json` defines one-to-one maximum-cardinality matching for multiple natural defects. A `FINDING` must have an accepted class and overlap a registered target localization anchor. Occurrence scans include overlaps by advancing one Unicode code point. Correction acceptability is exact: replacing one exact occurrence of `target_span` must produce one preregistered full corrected target. H1 reports controlled-mutation sensitivity; no pair-sensitivity metric remains. Localization uses only FINDING candidates on defective items as its explicit denominator, so clean false positives are not penalized twice. Evidence-field correctness is a strict structural prerequisite, not a measured candidate metric. H1 and H2 are always reported separately. Three measured runs are distinct from descriptive union and 2-of-3 consensus.

## Read-only gates

Package code never writes task or review gates. `gate-reader.mjs` only reads these external files, each bound to final `MANIFEST.json`. It requires the exact blocking `REVIEWER`/`claude-opus-5` and advisory `ADVISOR`/`gemini-3.7-flash` roles/models and rejects model identity reuse:

1. `.ai/reviews/research-gemini-evaluator-contract-effectiveness-holdout-v1/BLOCKING_REVIEW.json`
2. `.ai/reviews/research-gemini-evaluator-contract-effectiveness-holdout-v1/ADVISORY_REVIEW.json`
3. `.ai/task/research-gemini-evaluator-contract-effectiveness-holdout-v1/EXECUTION_AUTHORIZATION.json`

Until all three are valid and current, preflight intentionally returns `NO_GO_REQUIRED_GATES`; this is a normal zero-call state, not an experiment failure. Source evidence paths must be tracked and byte-clean against the Git index. The task handoff is separately hash-bound as proposal-only input and is not represented as tracked evidence.

## Offline commands

```bash
node freezer.mjs --check
node build-manifest.mjs --check
node tests/test-package.mjs
node preflight.mjs
```

After independent gates are supplied, execute only the next exact cell from `DESIGN-CONTRACT.json`, for example:

```bash
node run.mjs h1-baseline-r1
```

Never loop past a nonzero exit. The package ships with neither `PREFLIGHT.json` nor `RESULT.json`. After the terminal cell, and only while `RESULT.json` is absent, run `node post-run.mjs --write`; it replays every successful binary capture against canonical RAW before opening the sealed reference and creates the result exactly once. Any existing result is a hard collision, even if its bytes would match.
