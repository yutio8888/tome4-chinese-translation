# Deterministic Chinese hard-linebreak holdout preflight v2

Status: `NO_GO_INSUFFICIENT_INDEPENDENT_CANDIDATES`.

This zero-inference package qualifies the unchanged `deterministic-linebreak-lint-v1` rule on baseline commit `31cb74af595567cd803a010e6fe5fceea4a29db6`. Design qualification disclosed that the 30,308-row snapshot emits exactly the five v1 development candidates. `EXCLUSIONS.json` registers each revision, boundary, tier, and source/target identity. Exact exclusion leaves zero independent candidates.

`SOURCE-AUDIT.json` is deliberately empty and cryptographically bound to the empty independent candidate set. It does not copy, relabel, pool, or score the v1 audit. With a zero denominator, independent precision and recall are undefined. The result does not establish a zero false-alarm rate, pooled-v1 performance, cross-component performance, deployment readiness, or authority to integrate the rule into production lint.

The inventory covers `addon-dev`, `ashes-urhrok`, `boot`, `cults`, `engine`, `example`, `example-realtime`, `items-vault`, `orcs`, `possessors`, and `tome`. All five exposed emissions are in `tome`; every component has zero independent emissions after exclusion. This is a coverage shortfall, not evidence of cross-component performance.

No future candidate minimum is defined here. Any future warning-only gate requires a separately versioned preregistration on an unseen future snapshot whose candidate membership was not inspected during v1 development or this qualification.

The scanner uses only local files. Supply repository and engine roots at runtime; no local absolute path is persisted:

```bash
node evidence/quality/model-probes/deterministic-linebreak-lint-holdout-v2/test-scanner.mjs
TOME_ENGINE_ROOT=<ENGINE_ROOT> node evidence/quality/model-probes/deterministic-linebreak-lint-holdout-v2/verify.mjs --repo <SOURCE_REPO>
```

The verifier clones the requested repository locally, checks out the frozen commit detached, rebuilds the canonical inventory, verifies every frozen hash, compares the v1 and v2 raw scanner outputs by value, applies exact exclusions, and regenerates `CANDIDATES.json`, `SOURCE-AUDIT.json`, and `RESULT.json` byte-for-byte. It also checks JSON, JavaScript syntax, 10/10 fixtures, artifact bindings, forbidden path and credential markers, absence of network-capable code surfaces, zero call accounting, and the frozen executor fixture hash. Run `git diff --check` separately in the task worktree.
