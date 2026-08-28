# Route-familiarity reference collection v1

Status: `FROZEN_ZERO_INFERENCE_COLLECTION_PACKAGE`.

This directory deterministically partitions the committed 145-row audit queue
into five contiguous 29-row model-facing shards. It freezes a provider-neutral
prompt, one strict Draft 2020-12 response schema per shard, and a local-only
four-lane execution manifest. It performs no inference, annotation,
adjudication, model call, or network call, and contains no RAW, acquisition,
candidate, or populated response file.

The planned later collection is `EXPLORATORY_NON_ISOLATED_REFERENCE`. The same
model families may later be scored, so its outputs are not a formally isolated
gold standard. Both derivations use the manifest's ordered, first-match-wins
rules. For four-route derivation, any `UNRESOLVED` label and then any material
evidence conflict are evaluated before consensus; only afterward do unanimous
or 3-of-4 labels form provisional consensus and a 2-2 split require lead
adjudication. Every unmatched pattern, including a resolved 2-1-1 split,
defaults to `LEAD_ADJUDICATION_REQUIRED`. A lane's exploratory reference score
uses leave-one-lane-out consensus plus lead adjudication. For that score, only
the three non-held-out lanes participate. Any non-held-out `UNRESOLVED` and then
any material evidence conflict are evaluated before consensus; only afterward
do 3-of-3 or ordinary resolved 2-of-3 matching labels form provisional
consensus, while all-distinct labels require lead adjudication. Every unmatched
leave-one-out pattern also defaults to `LEAD_ADJUDICATION_REQUIRED`. Thus
`[CLEAN,CLEAN,UNRESOLVED]` and `[UNRESOLVED,UNRESOLVED,CLEAN]` adjudicate rather
than reaching the 2-of-3 rule. The held-out lane's label, evidence,
unresolved state, and every other judgment artifact are excluded from
consensus, conflict detection, and lead-adjudication inputs. Union and consensus
are derived outputs, not measured model calls.

## Artifacts

- `OUTBOUND-SHARD-01.json` through `OUTBOUND-SHARD-05.json` contain neutral
  shard metadata, unchanged seven-key queue items, and 29 ordered
  `source_evidence` records aligned one-to-one with those items. Each strict
  four-key record binds the exact UTF-8 bytes of `text` (byte-equal to the
  item's `bounded_fixed_context`) to a lowercase SHA-256. Every `response`
  remains `null`. A shard does not contain its own SHA-256.
- `RESPONSE-SCHEMA-SHARD-01.json` through
  `RESPONSE-SCHEMA-SHARD-05.json` bind the parent queue hash, shard ID,
  complete emitted shard-file hash, exact count, and exact neutral-ID order.
  Their five predecessor `$defs` values are reused exactly, with a per-item
  constraint allowing only that item's expected source-evidence hash.
- `PROMPT.md` defines the annotation task, four label definitions, evidence
  requirements, and strict JSON output contract without lane identities,
  historical exposure cells, local paths, sealed truth, or example answers.
- `LOCAL-ROUTE-MANIFEST.json` is local-only (`outbound_allowed=false`). It
  records exactly four later lanes, identical shard/prompt/schema bindings,
  filename templates, and mandatory pre-inference availability/version checks.
- `BUILD-REPORT.json` hashes every generated artifact that precedes it.
  `EXPERIMENT.json` hashes those artifacts plus the build report. Neither file
  contains its own hash, so the dependency graph is acyclic.
- `build.mjs`, `test-builder.mjs`, and `verify.mjs` implement the stdlib-only
  build, focused mutation tests, and independent verification.

The local manifest is never model-facing. Before any later inference, the
actual CLI versions, requested-model availability, and runtime identity rules
must be rechecked and frozen. The present package deliberately records those
route checks as `MUST_RECHECK_BEFORE_INFERENCE`. Later RAW, acquisition, and
candidate outputs belong only in the later execution task directory and must
never be written into this frozen package.

## Rebuild and verification

The builder uses Node standard-library modules only. Schema compilation in the
tests and verifier requires `ajv/dist/2020` from system-resolved Ajv major 8.
The preflight fails with an actionable installation message if that module is
missing or resolves to another major version.

This package was locally verified with Node `v22.22.1` and system-resolved Ajv
`8.17.1`. Those versions are local verification prerequisites/observations,
not inference route-version checks. Ajv is not vendored or patch-pinned;
patch-level drift within major 8 is an accepted reproducibility limitation,
matching the predecessor package.

Run from the repository root:

```bash
node --check evidence/quality/model-probes/route-familiarity-reference-collection-v1/build.mjs
node --check evidence/quality/model-probes/route-familiarity-reference-collection-v1/test-builder.mjs
node --check evidence/quality/model-probes/route-familiarity-reference-collection-v1/verify.mjs
node evidence/quality/model-probes/route-familiarity-reference-collection-v1/build.mjs
node evidence/quality/model-probes/route-familiarity-reference-collection-v1/test-builder.mjs
node evidence/quality/model-probes/route-familiarity-reference-collection-v1/verify.mjs
```

The verifier rebuilds into a uniquely named temporary directory and compares
all 14 generated files byte-for-byte. Independently of report claims, it checks
frozen input/output hashes, the executor fixture, exact field sets, contiguous
concatenation, all ordered source-evidence text/hash bindings, all shard/schema
bindings, all five Ajv schemas, the acyclic hash graph, four-lane equality,
zero responses/calls, absence of later-run placeholders, and recursive hygiene
across the prompt, shards, and all emitted response schemas.

Focused tests begin from passing emitted baselines and then cover wrong shard
and parent hashes, swapped IDs/order, 28/30 items, unknown fields and labels,
label-branch violations, positive context-dependent fixtures, empty/all-zero/
unknown/cross-item evidence hashes, missing/reordered/tampered evidence records,
evidence text/hash drift, whitespace-only text, historical-cell/provider/local-
path/provenance/sealed-reference injection (including emitted schemas), lane
binding drift, ordered derivation-rule/default mutation, overlapping
`UNRESOLVED`/consensus patterns, ordinary resolved 2-of-3 consensus, four-route
2-1-1 fallback, and source/target/context mutation.
