# Prospective source-context truth audit v1

Status: `FROZEN_BEFORE_TARGET_LINK`.

This directory freezes Phase 1 contracts and fail-closed tooling for linking the already frozen 120-item source-only presentation to its production translation targets. It does not contain a real target-bound queue, audit candidate, truth label, sealed reference or scoring result. No production binder or verifier has been run in this phase; only the synthetic fixtures are exercised.

## Boundary

The immutable upstream presentation is `8deda776d84cdcca0794ea2dcec34f2dbb5d5971b2d937d2653b1f60b95886c5`. `TARGET-JOIN-CONTRACT.json` separately pins the production commit, canonical membership, provenance snapshot, source frame, evidence packets and the 58-file terminal-input manifest. Linking target text is a new phase: the source-only hash is never reinterpreted as covering target bytes.

The binder reads target text only from the 58 individually fingerprinted terminal envelopes. It joins on exact `task_id + NUL + original_revision_key`, recomputes SHA-256 over the raw target UTF-8 bytes, and requires equality with the frozen canonical membership. It rejects every missing, duplicate or conflicting identity, even if duplicate values happen to be byte-identical.

## Planned target-link outputs

An authorized bind run writes six deterministic files to an explicitly supplied output directory:

- `TARGET-BINDING-REGISTRY.json` records the internal identity, membership and terminal-fingerprint binding for every item.
- `AUDIT-QUEUE.json` is the 120-item internal target-bound queue.
- `SURFACE-QUEUE-{1,2,3}.json` are three globally disjoint, complete 40-item source/target-only candidate queues.
- `TARGET-JOIN-REPORT.json` records counts, gates and output hashes.

The binder cannot generate context queues. `release-context.mjs` releases one `CONTEXT-QUEUE-N.json` only after the complete matching `SURFACE-CANDIDATE-N.json` passes its exact schema, ordered 40-ID binding and an explicitly supplied pre-frozen byte SHA-256. `verify-adjudication.mjs` then mechanically binds the final 120 ordered identities and all six candidate files to `AUDIT-QUEUE.json`. No real version of any queue or candidate is present now.

## Audit and pilot design

`AUDIT-CONTRACT.json` freezes the two-pass audit, the five truth labels and the two material axes. Three workers each review 40 non-overlapping items, surface first and context second. The lead verifies and adjudicates all 120. Every non-clean result, disagreement, override or unresolved axis requires written evidence.

The downstream GLM pilot is GO only if at least 108 items are determinate and the frozen context/surface/clean pools meet all item, task and category minima. Context cases are strictly `CONTEXT_DEPENDENT_DEFECT`; `MIXED_DEFECT`, `UNRESOLVED` and insufficient packets are excluded. Its fixed composition is 8 context cases, 4 surface controls and 8 clean controls, selected in that pool order with a global cap of two items per task. The GLM route, A/B difference, two runs per arm, atom-hit definition and all performance thresholds are frozen in `AUDIT-CONTRACT.json`. Any pool shortage is `NO_GO`.

## Commands

The only authorized command in the current phase is the synthetic test:

```bash
node test-target-join.mjs
```

Future target linking requires an explicit production checkout and output directory:

```bash
node build-target-queue.mjs --root /path/to/research-checkout --production-repo /path/to/production-checkout --out /path/to/frozen-output
node verify-target-queue.mjs --root /path/to/research-checkout --production-repo /path/to/production-checkout --queue-dir /path/to/frozen-output
node release-context.mjs --queue-dir /path/to/frozen-output --surface-candidate /path/to/SURFACE-CANDIDATE-1.json --surface-candidate-sha256 FROZEN_SHA256 --shard 1 --out /path/to/frozen-output/CONTEXT-QUEUE-1.json
node verify-adjudication.mjs --audit-dir /path/to/completed-audit
```

Do not run any production command until the relevant phase is explicitly authorized. After a real bind, inspect `TARGET-JOIN-REPORT.json`, freeze all six file hashes, run JSON parsing and `git diff --check`, and keep model/network calls at zero until the surface audit dispatch protocol is ready.
