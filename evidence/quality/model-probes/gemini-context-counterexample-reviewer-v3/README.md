# Gemini context-counterexample reviewer v3

Status: **NO_GO / static integrity only / zero inference**. No model or network call was made. Do not invoke `qualify.mjs` or `run.mjs` without later task-owned authorization.

V3 is an independent package. Reviewed v2 is disclosed only as capacity motivation and as the predecessor for zero-inference harness behavior. No v2 direct-audit verdict, rejected-ID gate, mutation, sample, reference, request, qualification, raw output, score, selection result, or experiment result is imported.

Prior LLM exposure is `ALLOWED_NOT_EVALUATED`: it is not scanned or used as a gate. Runtime identity is `REQUESTED_ROUTE_ONLY_UNVERIFIED`. This package supports no novelty, contamination-free, unseen-performance, prevalence, generalization, or model-effectiveness claim.

## Frozen scope and capacity

The dependency is the hash-pinned complete 30,308-row canonical inventory and public source commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`. Dialogue accepts only top-level `mod-tome/data/chats/*.lua`. Narrative accepts only top-level `mod-tome/data/lore/*.lua` lore-body bindings and top-level `mod-tome/data/texts/` basenames beginning `intro-` or `message-`. Any basename containing `tutorial` and every `unlock-*` text are excluded. Tutorial subdirectories, achievements, mechanics, monetization/cosmetic unlocks, and every other narrative class are excluded.

All v2 target-present, single-occurrence, revision/base uniqueness, metadata-tag exclusion, normalized-source uniqueness, exact translatable-Lua-construct binding, normalized-context uniqueness, source-file disjointness, cohort/profile quota, and deterministic replacement rules remain active.

Independent selector measurement before ranking:

- 30,308 inventory rows; 1,695 rows in the exact path scope.
- Under the corrected scope, exact selection stops before ranking: 51 eligible narrative source files provide only 19 reserve files after 32 selected files, versus the fixed minimum of 50.
- Exact capacity shortfall: 31 narrative reserve files; therefore no corrected 64-base selection, packets, or downstream evidence is released.

Selection uses v3-specific seed `gemini-context-counterexample-reviewer-v3/canonical-selection/v1` and IDs `V3-{D|C}-{D|N}NN`. Source packets contain a bounded ±12-line fixed-source context with exactly one `[[SOURCE_MATCH_1]]` marker and exact occurrence/construct binding.

`V3_REJECTED_BASES_PATH` may point to a later v3 direct-audit rejection ledger. Before downstream bytes freeze, the selector consumes the next unused same-profile reserve rank while preserving slot cohort/profile and file/source/context disjointness; regenerated `EXPERIMENT.json` counters are derived from that replacement output. `OUT_OF_SCOPE_NON_PROSE` is tracked separately from translation defects and is never aggregated into context-audit eligibility. `V3_OUTPUT_DIR` supports isolated fixtures. V2 rejected IDs are not consulted.

## Capacity stop and absent downstream evidence

The corrected scope is frozen in `DESIGN-CONTRACT.json` and `CAPACITY-SHORTFALL.json`. Selection stops before ranking because the fixed reserve gate fails; prior selection-dependent files remain predecessor evidence only and are not acceptance evidence. The package remains zero-inference. `RESULT.json` is the terminal result; no selected/reserve/binding/packet/audit-queue artifacts remain, and no downstream audits, mutations, references, requests, qualification, raw outputs, or scores are released.

Not present: surface/context audit records, mutations, manipulation checks, assigned samples, sealed references, requests, qualification evidence, raw outputs, scores, protocol selection, or results. Surface and context audits must be newly performed for v3.

## Terminal gate vocabulary

`PENDING-GATES.json` is a terminal capacity report for this zero-inference stop. Its entries are not the canonical phase-verifier gates listed in `phase-verifier.mjs`; no phase-verifier phase is being released or claimed complete.

## Checks

```bash
node select-and-freeze.mjs --check
node test-source-binding.mjs
node test-assignment.mjs
node test-zero-call.mjs
node test-schemas.mjs
node test-fixtures.mjs
for f in *.mjs; do node --check "$f"; done
node preflight.mjs          # expected exit 3, NO_GO, static_integrity PASS
node post-run-validate.mjs  # expected NO_RUN
```

The terminal package contains no replacement fixture or direct-audit rejection results: selection stops before ranking because the reserve gate fails. The source-binding tests cover the resolved non-lore-field and unresolved-field rejection reasons; additional fixtures enforce the reserve target and exact accepted/rejected path classes.
