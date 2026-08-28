# Route-familiarity reference execution v1

This directory is a completely preserved but incomplete historical execution
record. It is not a completed four-route experiment and is not eligible for
formal comparison, four-route consensus, reference derivation, adjudication,
or scoring.

## Corrected interpretation

The record contains 22 CLI process invocations. A process start is not called
a model call. Nine preserved RAW envelopes contain non-synthetic model-response
payloads; eight directly identify a runtime model, and six identify both
runtime provider and model. The two Claude authentication errors contain
CLI-generated assistant payloads marked `model=<synthetic>` and
`is_api_error_message=true`; they are explicitly excluded from the response
count. Three Codex candidates
(SHARD-03/04/05) pass the frozen canonical Draft 2020-12 schemas and exact
neutral-ID/evidence bindings.

The predecessor froze lane-04 with provider exactly `Z.ai/GLM` and model
exactly `opencode-go/glm-5.3`. All six preserved Pi invocations instead
requested and reported provider `zai-standard-cn` and model `glm-5.3-flash`.
They are retained as out-of-protocol exploratory calls. Every frozen lane-04
cell is therefore `UNEXECUTED_EXACT_FROZEN_ROUTE`, and none of the six calls
may participate in consensus, reference derivation, scoring, adjudication, or
formal comparison.

Frozen/requested route identity is separate from confirmed runtime identity.
Codex and Gemini have no confirmed runtime provider or model evidence. Claude
has model-only `system.init.model=claude-opus-5` evidence in two attempts and
no confirmed runtime provider. Pi has exact provider+model evidence in all six
RAW envelopes, but that identity is the preserved lane-04 mismatch; runtime
effort is unverified for every lane.

The six Pi commands did not place a response schema in the model-facing
request or command. Their status is `SCHEMA_NOT_MODEL_FACING`: this is a
harness/input protocol failure, not evidence about answer quality. The prior
invalid-answer attribution is withdrawn.

## Evidence and provenance

- `ATTEMPT-LINEAGE.json` freezes the complete attempt-directory file set,
  hashes every immutable artifact, and separates process, response, identity,
  candidate-validity, route, schema, and parser classifications.
- `HARNESS-LINEAGE.json` records the frozen contract hashes separately from
  current scripts. The historical preimages for `runner-lib.mjs`, `run.mjs`,
  `finalize.mjs`, and `verify.mjs` remain unresolved and explicitly
  `UNVERIFIABLE_HISTORICAL_PREIMAGE`. The contracted `test-runner.mjs`
  revision is classified
  `CONTRACT_HASH_BOUND_HISTORICAL_PREIMAGE_UNAVAILABLE`; the current scripts
  remain later correction revisions and do not match the contract.

The contracted historical test-runner.mjs revision is hash-bound by RUN-CONTRACT.json, but its historical preimage bytes are unavailable and unverifiable in this persistent package; exact preimage reconstruction is not claimed.
- `CORRECTION.json` records frozen-versus-runtime route identities, all 20
  frozen-cell statuses, exact counts, and the mechanical downstream block.
- `RUN-REPORT.json` and `EXPERIMENT.json` expose only the corrected incomplete
  status. Canonical post-validation is bound separately from historical
  model-facing transport schemas.

Transport-schema bytes are named only when immutable evidence proves the
preimage. Claude SHARD-01 attempt-001 is explicitly
`UNVERIFIABLE_HISTORICAL_PREIMAGE`: its `[EXACT_SCHEMA_BYTES]` marker does not
preserve exact argument bytes, and the producing runner preimage is unavailable.
The verifier never substitutes the current predecessor schema for missing
historical transport bytes. The three valid Codex candidates are replayed
directly from their preserved `RAW.last-message.json`. Other parser histories
remain explicitly unverifiable rather than being reconstructed from current
parser code.

## Verification

Run `node test-runner.mjs` for credential-free focused and mutation tests, then
`node verify.mjs --write` for the execution verifier. Ordinary verification
does not construct a runtime, inspect the host home, or read/copy live Codex,
Claude, Gemini, or Pi credentials. The verifier scans every task artifact type,
including RAW text, without echoing matched secret content; checks all
immutable hashes, JSON, whitespace, final-newline exceptions, and unscoped
repository status against the task's exact allowed dirty-file set; compares
the predecessor route manifest independently; validates
the three canonical candidates; and proves that downstream derivation remains
blocked. The focused tests also build an isolated sparse checkout containing
only this package and its tracked predecessor/fixture inputs, confirm that no
ignored orchestration directory is present, and run finalize, the focused
tests, and ordinary verification there.

Do not run `run.mjs` or `preflight.mjs` in this closed historical package. An
exact execution of the frozen lane-04 route requires a newly frozen experiment
directory and fresh authorization under the applicable workflow.
