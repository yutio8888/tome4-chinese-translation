# Architecture contract

## Boundary, authority, and activation

This is contracts-only P0: no implementation, child creation, mutation work, qualification, provider/model/network call, formal request, RAW, score, or result. P1–P3 remain future zero-call phases.

The non-adversarial fail-closed threat model covers interruption between writes, duplicate starts, stale informational state, malformed/partial capture, missing derived RAW, operator path/config mistakes, fixture/evidence confusion, and detectable deterministic defects. It assumes a contract-following ORCHESTRATOR, collision-resistant SHA-256, and non-malicious host, worktree, filesystem/kernel, credentials, and provider transport. Malicious actors/infrastructure, compromise, and denial of service are excluded.

`receipts/ACTIVATION.json` is the write-once local trust anchor. Its scope hash is SHA-256 of canonical exact `{allowed_paths,orchestrator_agent_id,task_id,user_authorization,workspace_id}` bytes specified in `SCHEMA-CONTRACTS.md`; the existing value is reproducible. It authenticates only post-activation package candidates/receipts, not historical orchestration.

ORCHESTRATOR alone writes activation, PHASE_PLAN/MUTATION_PLAN, authorization, observation/audit, dispatch, qualification-started, completion, archive, review-attestation, manifest, gate, and pin receipts. Manifests are authoritative task receipt artifacts. Package code only fixed-reads and validates them. Execution facts are package-created write-once STARTED/capture/FINISHED bytes. RAW, ledger, qualification evidence, scores, and result are deterministic derived views. Task `STATE.json` is informational and never a package input.

## Modules and production composition

Dependency direction is `core <- store <- evidence <- bin`:

| module | responsibility | imports | forbidden |
|---|---|---|---|
| core | strict JSON/schema/hash/render/score/predicate functions | pure standard libraries | filesystem, process/network, receipt creation |
| store | fixed roots, ordinary-file/exclusive-create/durable attempt facts | core | invocation, task-receipt interpretation, overwrite |
| evidence | validate supplied fixed receipt/fact bytes; derive evidence/RAW/ledger/score/result | core, store | invocation or task-receipt writes |
| bin | fixed-path composition and sole production invocation | core, store, evidence | injectable roots/routes/state/receipts/invoke capability |

A fifth `integration` pin is composition metadata, not executable source. Its module files and export are exactly `integration/COMPOSITION.json` and `route/ROUTE.json`; COMPOSITION fixes the six bin exports. Bin owns those executable files. Module content hashes canonical exact `{schema_version,module,files,dependency_edges}` with ordered raw file hashes and ordered dependency edges; exports use the separate exact export preimage. Candidate, manifest, repair, and pins use identical values.

At P2 the executable is frozen before review as an absolute ordinary-file realpath/hash/mode. Production performs no PATH lookup, inherits no environment, accepts no arguments, and has no root/STATE/route/executable/authorization/receipt/invoke override. `{output_mode}` is exactly `json`.

## Attempts and authoritative orphan facts

Formal attempts are append-only, with sequence exactly `[1]` or `[1,2]`; attempt 2 requires valid retryable attempt 1. Durable STARTED binds authorization, fixed dispatch and child before spawn. Captures/CAPTURE precede strict adaptation and FINISHED. Success FINISHED hashes only canonical strict response bytes and never hashes RAW. RAW embeds that response and FINISHED hash, yielding one-way FINISHED→response and RAW→FINISHED binding. Missing success RAW is exact-byte derivable without invocation; mismatch is never overwritten.

STARTED/no FINISHED remains `IN_PROGRESS` while the child is active or status is unknown. Formal fixed status/audit paths are `receipts/formal/status-observations/<cell>/attempt-<n>.json` and `receipts/formal/orphan-audits/<cell>/attempt-<n>.json`; qualification equivalents are fixed under `receipts/qualification/`. ORCHESTRATOR writes both once. Only a valid exact-child terminal observation with no active turn, plus an audit binding STARTED and still-absent FINISHED with sole conclusion `TERMINAL_NO_FINISHED`, permits `STOP_AMBIGUOUS_STARTED`. These receipts are authoritative derivation facts. Unknown, stale, absent, or contradictory evidence remains IN_PROGRESS. Audited ambiguity gives STOP_NOT_SCORE and cannot replay in the namespace. NO_RUN is in-memory only for an entirely empty namespace.

## Qualification: gate before release, closed capture, pure finalization

Qualification has one direct EXECUTOR child and no retry:

1. ORCHESTRATOR creates it waiting with no provider process, freezes its identity, and writes AUTHORIZATION (the sole qualification dispatch-ID source), WAITING-OBSERVATION, DISPATCH, and QUALIFICATION-STARTED.
2. ORCHESTRATOR writes CAPTURE-GATE over those exact records plus request/route. The waiting child remains blocked until `qualify-capture` consumes a valid `QUALIFICATION_CAPTURE_GO`.
3. After release, capture invokes at most once and durably writes stdout/stderr, CAPTURE, FINISHED, and canonical `CAPTURE-SUMMARY.json`. Summary contains exact capture hashes and exact `adapter_result={schema_version,status,response_sha256,response_item_count}`.
4. ORCHESTRATOR writes COMPLETION pointing to the summary hash, confirms archive, and writes ARCHIVE pointing to COMPLETION.
5. Pure finalization validates all prior bytes in fixed order, exclusive-creates QUALIFICATION-EVIDENCE, and cannot invoke. FINAL-GATE consumes capture gate, facts, summary, lifecycle, and evidence.

Capture/finalization never mint task lifecycle evidence. Qualification orphan handling uses the same explicit audit contract.

## Semantic mutation independence

Class M is `MECHANICAL_FIXTURE_ONLY` and cannot satisfy a semantic gate. Before Class S dispatch, two distinct direct children must already exist and wait. ORCHESTRATOR issues fixed `receipts/mutation/PLAN.json`, freezing both agent IDs, parent/workspace, exact roles/purposes, dispatch IDs/paths, proposal/validation paths, and gate path. Author and validator are independent EXECUTOR direct children with different purposes and identities.

The one-way graph is:

```text
MUTATION_PLAN -> AUTHOR-DISPATCH -> proposal -> AUTHOR-COMPLETION -> AUTHOR-ARCHIVE
MUTATION_PLAN + proposal -> VALIDATOR-DISPATCH -> validation -> VALIDATOR-COMPLETION -> VALIDATOR-ARCHIVE
PLAN + two documents + six lifecycle receipts -> MUTATION-GATE
```

The author is archived before validator release. Outputs contain only upstream plan/dispatch/proposal hashes, never downstream lifecycle/gate hashes.

## Candidate freeze, pre-review plan, manifest, and pins

The repository review identity remains `SHA256(SPEC raw || NUL || bounded diff raw)`. The package candidate separately hashes only its canonical body. Neither contains PHASE_PLAN, manifest, review, gate, or pin bytes.

After both identities and the current candidate author freeze—but before either review dispatch—ORCHESTRATOR writes an immutable versioned PHASE_PLAN. It is the authoritative source of phase_id and prospective manifest/gate path, and fixes two review slots: dispatch IDs, controlling review paths, roles, and purposes. Both controlling review records bind the plan path/hash and both candidate identities. Thus current P0 cycle 3 can plan after these seven files freeze without altering either hash.

Only after dual controlling PASS does ORCHESTRATOR write a post-PASS manifest binding PHASE_PLAN and the exact completed review records. Package PHASE_REVIEW receipts are one-way attestations to those existing records; they do not fabricate mirrored dispatch/response/completion/archive history. The phase gate then consumes plan, manifest, controlling records, and attestations. Content change requires a fresh repair/version plan.

Same-phase manifests bind exact ordered module file/raw hashes, canonical module-content hashes, export hashes, and DAG edges—not unavailable pins. P0’s synthetic export has no module pin. Later pins issue topologically after one shared dual PASS. Repair pins preserve exact old pins outside the reverse invalidation closure and issue fresh closure pins topologically.

## Authorization, gates, and result

Implementation and execution axes are distinct. P0–P2 positives are `<phase>_GO`; P3 positive is only `ZERO_CALL_IMPLEMENTATION_COMPLETE`. P1 explicitly chains P0 gate path/hash; P2 chains P0/P1; P3 chains P0/P1/P2. Downstream gates are MUTATION, FREEZE, QUALIFICATION_CAPTURE, QUALIFICATION, DISCOVERY, CONFIRMATION, RESULT. Every gate has a fixed path, exact ordered path/hash input list, closed predicate, and no scanning.

Discovery/confirmation AUTHORIZATION receipts have exact nested ordered-cell schemas and are the sole formal dispatch-ID sources. `SCORES.json` has exact nested cell/summary structures and deterministic winner rules. `RESULT.json` has exact nested discovery/confirmation structures. No winner yields `STOP_NO_WINNER` and no confirmation authorization/attempt/RAW. Invalid or ambiguous execution yields `STOP_NOT_SCORE` and no RESULT.
