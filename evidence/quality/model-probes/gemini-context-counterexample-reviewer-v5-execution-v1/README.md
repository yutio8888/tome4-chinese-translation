# Gemini context-counterexample REVIEWER V5 execution package

This is an **in-progress implementation candidate with pristine experimental `NO_RUN / NO_GO` state**. It binds the immutable V5 terminal frame, 64 bases, 40 planned mutants, 24 controls, and all 32 possible request identities. The real package contains no mutation evidence, qualification call, scored RAW output, score, or model-effect result.

## Candidate and gates

`candidate_ref` hashes exactly the 32 ordered reviewed content files. `CANDIDATE-MANIFEST.json` and `HASH-DAG.json` are outside that root and are frozen by a future task-owned `CANDIDATE-IDENTITY.json`. Every gate consumer reruns full file existence/hash/order/root, manifest/DAG schema, and closed-world verification; a recorded status or hash alone is insufficient. Normal and senior reviews bind distinct archived dispatches plus selected/runtime model identity. The senior route is exactly requested `claude-fable-5-1[1m]`, runtime `claude-fable-5-1`.

## Context and freeze seam

`runtime-context-text-v2` preserves `BEFORE → SOURCE_CONSTRUCT → AFTER`. BEFORE/AFTER may be deterministically truncated at 8192 UTF-8 bytes. SOURCE_CONSTRUCT is never renderer-truncated. Seven predecessor rows do not contain the exact item source in the source construct; for exactly those rows `exact_source_appended=true`, and the renderer appends a delimited exact source. Frozen samples and the request manifest bind `exact_source_appended_count=7`.

Line and byte coordinates are optional inherited diagnostics: `-` means unavailable, and present byte coordinates are not claimed to be independently remeasured here. The route contract currently contains the verified local absolute `agy` executable path, so this candidate is intentionally host-specific and is not a portable release artifact.

The freezer emits `SAMPLES.json`, sealed `REFERENCE.json`, 32 request files, and `REQUEST-MANIFEST.json`. Validation independently regenerates every byte. Atom matching is one-directional: a reported target span must contain the frozen atom span; the reverse containment is not accepted.

## Qualification

Qualification is non-scored and remains unrun. It is truthful and two-stage:

1. `captureQualificationStage1()` runs only after review→mutation→freeze semantics pass. While the EXECUTOR is running it writes the exact `D-I001..D-I016` synthetic request, raw stdout/stderr captures, hashes, expanded argv, and `EVIDENCE-DRAFT.json`.
2. Only after that dispatch is uniquely archived may task-owned `finalizeQualification()` write the lifecycle receipt, deterministic RAW reconstructed from captured real-shape `agy` stdout, and candidate/manifest/DAG-bound finalized evidence.

The adapter duplicate-safely parses the captured `agy` envelope and requires exactly one non-null response channel. Tests use a checked-in redacted real-shape envelope and a mock process function; they do not run `agy`, a model, or a network call.

## Execution and recovery

The sole public execution primitive is `authorizeAndRun()`. It reloads the current candidate and reruns candidate, mutation, freeze, qualification, request, and exact authorization semantics. Discovery is 16 cells. Confirmation is separately authorized and limited to A plus the mechanically derived winner (8 cells). Caller-supplied gate or qualification objects cannot authorize execution.

Before invoking, the runner exclusively writes exact `STARTED.json`; it then captures stdout/stderr and writes exact `FINALIZED.json`. RAW is created only afterward by deterministic adaptation of captured `agy` stdout. A `FINALIZED` success without RAW fails closed: it is not replayed or silently completed. STARTED without FINALIZED is also ambiguous and blocks replay. The ledger, both journal schemas, all capture bytes, and RAW must form an exact bijection.

## Post-run and outputs

`postRun()` reruns all current gates and semantics, regenerates frozen artifacts, validates qualification, reconstructs RAW, and checks ledger/journal/capture identity and honest invocation counts. No winner forbids confirmation RAW. `SCORES.json` and `RESULT.json` are forbidden before the proper phase and are exclusive-create; only exact existing bytes may be reused.

## Safe commands now

```bash
node --check *.mjs tests/test-package.mjs
node tests/test-package.mjs
node build-frozen-base.mjs --check
node preflight.mjs          # expected static PASS, NO_GO_REQUIRED_GATES
node post-run-validate.mjs  # expected NO_RUN, zero RAW
```

Do not run qualification, `agy`, model/network calls, or formal execution without future exact gates.
