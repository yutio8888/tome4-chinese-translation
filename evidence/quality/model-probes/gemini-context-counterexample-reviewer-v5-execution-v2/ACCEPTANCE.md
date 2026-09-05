# Acceptance contract

## Current boundary

P0 is contracts written, not implementation. Positive P0 requires exactly seven package files, separately frozen repository and package candidate identities, an immutable pre-review PHASE_PLAN, and independent normal/senior PASS records binding that plan. It authorizes only future P1. P1–P3 are unimplemented zero-call phases; P3 positive is only `ZERO_CALL_IMPLEMENTATION_COMPLETE`. Mutation, qualification, model/provider/network execution, discovery, confirmation, and result creation remain unauthorized.

The package does not edit or interpret task `STATE.json`. Repository orchestration alone maintains `candidate_author_agent_id`; PHASE_PLAN copies the already-frozen value. This resolves the author-provenance advisory in package documentation without changing STATE.

## Canonical JSON acceptance

The three JSON files must reject duplicate keys and equal compact recursively key-sorted UTF-8 serialization, with no BOM, nonstandard constants, extra bytes, or terminal newline. Their exact top-level key sets are:

- `TRUST-ROOTS.json`: `artifact_classes,candidate_identities,canonical_json,package_receipt_policy,predecessors,schema_version,state_authority,task_activation_anchor,threat_model`.
- `STATE-MACHINE.json`: `attempt,formal_namespace,gate_order,module_pins,phase,qualification,schema_version`.
- `MIGRATION.json`: `execution_v1,inventory,migration_rules,predecessor_bindings,retained_design,schema_version`.

## Mandatory checks

1. Task-content changes are exactly `README.md`, `ARCHITECTURE.md`, `TRUST-ROOTS.json`, `STATE-MACHINE.json`, `SCHEMA-CONTRACTS.md`, `MIGRATION.json`, and `ACCEPTANCE.md`. No task/review/role/AGENTS/V5/execution-v1/other path changes are attributed to this repair; unrelated pre-existing dirty paths are preserved.
2. Threat assumptions/exclusions and trust writers/readers are explicit. ORCHESTRATOR alone writes task receipts, including authoritative plans/manifests and orphan evidence. Package code never reads STATE or mints lifecycle facts.
3. Activation’s exact hash preimage is canonical `{allowed_paths,orchestrator_agent_id,task_id,user_authorization,workspace_id}` with the documented exact nested authorization and seven paths; it reproduces `a0b489eea1a622e677950792c85b01463e676e53a5500383ef967804d90f38a6`.
4. Repository `candidate_ref` remains SPEC+NUL+bounded-diff. Package candidate has exact ordered file/export objects. PHASE_PLAN, manifest, review, gate, and pin bytes enter neither candidate preimage.
5. For every phase/repair, ORCHESTRATOR issues immutable `.../PHASE-PLAN.json` after both identities and candidate author freeze and before either review dispatch. Its exact subject is `implementation_phase,phase_id,version,repair_id,orchestration_candidate_ref,package_candidate_sha256,candidate_author_agent_id,normal_review_slot,senior_review_slot,prospective_manifest_path,prospective_gate_path`; each slot is exact `dispatch_id,controlling_review_record_path,reviewer_role,purpose`. Current P0 uses `receipts/phases/P0/versions/v001/PHASE-PLAN.json`, phase `P0-v001`, null repair, planned `p0-normal-04`/`review-04.json` and `p0-senior-04`/`senior-audit-04.json`, and same-directory MANIFEST/GATE. It is created after repaired seven-file freeze without changing either identity.
6. Both controlling review records have the exact response-document schema, bind PHASE_PLAN path/hash and both candidates, and occupy the planned dispatch IDs/paths/roles/purposes. Post-PASS manifest binds plan plus both exact records. PHASE_REVIEW receipts only attest those records; no mirrored package dispatch/completion/archive is fabricated. Content change uses a fresh repair/version.
7. `phase_id` originates in PHASE_PLAN and is copied by manifest/receipts. Manifest is an authoritative ORCHESTRATOR task artifact. Qualification dispatch ID originates in its AUTHORIZATION after waiting-child identity freeze. Discovery/confirmation dispatch IDs originate in each authorization’s ordered cells.
8. Every module-content hash uses canonical exact `{schema_version,module,files,dependency_edges}` where files are ordered `{path,raw-byte sha256}` and dependency edges are ordered. Candidate exports, phase/repair manifests, and pins agree. Integration files/export are exactly COMPOSITION and ROUTE; bin owns executable files.
9. Pins issue topologically after one dual PASS. Repairs preserve exact historical pins outside the reverse dependency closure and freshly review/pin the closure.
10. Formal STARTED is durable before spawn. Attempts are exactly `[1]` or `[1,2]`; attempt 2 requires retryable attempt 1. FINISHED hashes only canonical strict response bytes; RAW binds FINISHED one-way. Missing RAW is derivable without invocation and differing existing bytes are never overwritten.
11. Formal and qualification CHILD_STATUS/ORPHAN_AUDIT receipts have fixed paths and exact schemas, are authoritative derivation facts, and bind child/STARTED/status evidence. Unknown remains IN_PROGRESS. Only valid `TERMINAL_NO_FINISHED` permits STOP_AMBIGUOUS_STARTED and STOP_NOT_SCORE.
12. NO_RUN is in-memory only for a wholly empty formal namespace, including no authorization/gate/status/audit artifacts.
13. Qualification order is waiting child → AUTHORIZATION/WAITING/DISPATCH/STARTED → CAPTURE-GATE GO consumed → release/spawn → stdout/stderr/CAPTURE/FINISHED/CAPTURE-SUMMARY → COMPLETION/archive → pure evidence → FINAL-GATE. Missing or invalid CAPTURE-GATE invokes nothing.
14. CAPTURE-SUMMARY canonical full-object bytes are its hash preimage. Exact adapter_result is `schema_version,status,response_sha256,response_item_count`. Completion points to summary; finalization validates every ordered receipt/fact and cannot invoke.
15. Class M cannot satisfy semantic gates. Class S requires two distinct waiting direct children and fixed MUTATION_PLAN before either dispatch; plan freezes IDs, lineage/workspace, roles/purposes, dispatch IDs/paths, document paths, and gate path. Author archives before validator release; all links are one-way.
16. DISCOVERY/CONFIRMATION AUTHORIZATION subjects, SCORES nested cell/summary objects, and RESULT nested discovery/confirmation objects are exact. Winner rules retain all per-run constraints and D/C/B tie-break. No winner has no confirmation authorization/attempt/RAW.
17. All eleven gates have fixed paths, exact ordered path/hash inputs, closed predicates, and reject extra/missing/reordered inputs. P1 chain is exactly P0; P2 is P0/P1; P3 is P0/P1/P2. P3_GO is invalid. Negative/STOP decisions never authorize a later stage.
18. Production DAG/permissions and zero-argument entry points are exact. P2 freezes an absolute executable realpath/hash/mode, route, argv, closed stdin, and exact child environment before review; no PATH lookup or production override exists.
19. Retained V5 design remains 64 bases, roles 24/16/24, cohort/profile 6/4/6, 32 requests, 16 discovery cells, 8 confirmation cells, complete SOURCE_CONSTRUCT, seven fallback IDs, and 120000-byte ceiling.
20. `MIGRATION.json` inventory equals the complete sorted execution-v1 file set: exactly 34 distinct files, no omission/extra/duplicate. Prompt/schema assets may be byte-retained only at P1 after compatibility validation and dual review; no v1 authority/output migrates.
21. Predecessors remain byte-identical at terminal gate `8495fd3bbe3211314607db67314360fd983d30f9455063b49d0e0a28a587d907`, active frame `e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3`, and terminal result `44726a9f538cb5ec3e63c64be64437fb2f0014f496b80d312647e240b8b550bd`.
22. V5 terminal preflight remains static integrity PASS with `TERMINALIZATION_COMPLETE_NO_RELEASE_OR_ROUND_0004` and zero inference calls. `git diff --check` passes.

## Verification

ORCHESTRATOR records: exact-seven scope comparison against baseline; strict parse/duplicate/canonical checks for all three JSON files; 34-file v1 inventory equality; activation preimage reproduction; predecessor hashes; V5 terminal preflight; bounded forbidden-artifact/token checks; and `git diff --check`.

## Future boundaries

- P1 consumes exact P0 gate path/hash and implements core/store plus compatible byte-retained assets, offline only.
- P2 consumes P0/P1 chain and pins, resolves route, and implements evidence/bin/integration, offline only.
- P3 consumes P0/P1/P2 chain and all pins for labelled 64/32 offline simulation, zero calls.

Any real mutation, qualification, or inference stops pending its own scope, authorization, plans/receipts, and gates.
