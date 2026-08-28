# Prospective source-context truth audit v1

Status: `LEAD_ADJUDICATION_COMPLETE / FORMAL_GLM_NO_GO`.

This directory began as the Phase 1 freeze for linking the 120-item source-only presentation to production translation targets. The target bind, three separated surface/context candidate audits, three auxiliary challenger reviews and the independent 120-item lead adjudication are now complete. `RESULT.json` is the current outcome; `EXPERIMENT.json` and `AUDIT-CONTRACT.json` remain the original pre-target-link freeze records and are not rewritten to make the completed run appear pre-registered after the fact.

The final truth audit contains 119 determinate items: 113 `CLEAN`, five `SURFACE_VISIBLE_DEFECT`, one `CONTEXT_DEPENDENT_DEFECT`, and one `UNRESOLVED`. The formal GLM pilot is `NO_GO_INSUFFICIENT_TRUTH_SET`: the contract requires at least eight pure context-dependent cases across six tasks and both categories, but only one Narrative case was found; the five surface controls are also all Narrative, leaving the required Runtime surface cell empty. No formal pilot sample was generated and no model call was made from this directory.

## Boundary

The immutable upstream presentation is `8deda776d84cdcca0794ea2dcec34f2dbb5d5971b2d937d2653b1f60b95886c5`. `TARGET-JOIN-CONTRACT.json` separately pins the production commit, canonical membership, provenance snapshot, source frame, evidence packets and the 58-file terminal-input manifest. The completed target link has its own target-bound presentation hash in `AUDIT-QUEUE.json`; the source-only hash is never reinterpreted as covering target bytes.

The binder reads target text only from the 58 individually fingerprinted terminal envelopes. It joins on exact `task_id + NUL + original_revision_key`, recomputes SHA-256 over the raw target UTF-8 bytes, and requires equality with the frozen canonical membership. It rejects every missing, duplicate or conflicting identity, even if duplicate values happen to be byte-identical.

## Target-link outputs

The authorized bind run wrote six deterministic files:

- `TARGET-BINDING-REGISTRY.json` records the internal identity, membership and terminal-fingerprint binding for every item.
- `AUDIT-QUEUE.json` is the 120-item internal target-bound queue.
- `SURFACE-QUEUE-{1,2,3}.json` are three globally disjoint, complete 40-item source/target-only candidate queues.
- `TARGET-JOIN-REPORT.json` records counts, gates and output hashes.

The binder cannot generate context queues. `release-context.mjs` released each `CONTEXT-QUEUE-N.json` only after the complete matching `SURFACE-CANDIDATE-N.json` passed its exact schema, ordered 40-ID binding and explicitly supplied pre-frozen byte SHA-256. `verify-adjudication.mjs` mechanically binds the final 120 ordered identities and all six candidate files to `AUDIT-QUEUE.json`.

## Audit and pilot design

`AUDIT-CONTRACT.json` freezes the two-pass audit, the five truth labels and the two material axes. Three workers each review 40 non-overlapping items, surface first and context second. The lead verifies and adjudicates all 120. Every non-clean result, disagreement, override or unresolved axis requires written evidence.

The downstream GLM pilot is GO only if at least 108 items are determinate and the frozen context/surface/clean pools meet all item, task and category minima. Context cases are strictly `CONTEXT_DEPENDENT_DEFECT`; `MIXED_DEFECT`, `UNRESOLVED` and insufficient packets are excluded. Its fixed composition is 8 context cases, 4 surface controls and 8 clean controls, selected in that pool order with a global cap of two items per task. The GLM route, A/B difference, two runs per arm, atom-hit definition and all performance thresholds are frozen in `AUDIT-CONTRACT.json`. `score-truth-audit.mjs` found a pool shortage and therefore produced `NO_GO`; it did not relax thresholds or create a pilot sample.

`CHALLENGER-{1,2,3}.json` are independent auxiliary reviews, not votes. `LEAD-SUPPLEMENTAL-EVIDENCE.json` records three lead-only resolutions whose fixed source or authoritative terminology was outside the 12-line item packet; none of that supplemental material may be added to later model inputs. `FINAL-ADJUDICATION.json` is the ordered lead truth record.

## Commands

Core verification and scoring commands are:

```bash
node test-target-join.mjs
node verify-adjudication.mjs --audit-dir .
node score-truth-audit.mjs
```

Future target linking requires an explicit production checkout and output directory:

```bash
node build-target-queue.mjs --root /path/to/research-checkout --production-repo /path/to/production-checkout --out /path/to/frozen-output
node verify-target-queue.mjs --root /path/to/research-checkout --production-repo /path/to/production-checkout --queue-dir /path/to/frozen-output
node release-context.mjs --queue-dir /path/to/frozen-output --surface-candidate /path/to/SURFACE-CANDIDATE-1.json --surface-candidate-sha256 FROZEN_SHA256 --shard 1 --out /path/to/frozen-output/CONTEXT-QUEUE-1.json
node verify-adjudication.mjs --audit-dir /path/to/completed-audit
```

Do not overwrite any frozen queue, candidate, challenger, supplemental evidence, adjudication or result file when extending this work. A separately versioned exploratory model comparison may reuse these frozen inputs, but its outputs cannot be represented as the formal GLM pilot and cannot change this directory's `NO_GO` result.
