# Schema contracts

## 1. Common rules, roots, and closed domains

P0 implements none of these future schemas. Every JSON object is exact-keyed. Unless stated otherwise, strings are nonempty, integers are non-boolean, hashes are 64 lowercase hex, timestamps are RFC 3339 UTC, and booleans are literal JSON booleans. Parsers reject duplicate keys, BOM, invalid UTF-8, NaN/Infinity, extra bytes, and noncanonical serialization. Canonical JSON is compact UTF-8 with object keys recursively sorted lexicographically, arrays preserved in declared order, and no terminal newline.

Package paths are relative to `evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v2/`; receipt paths are relative to `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v2/`. Checked-in `bin` location determines both roots. Every selected path is a declared ordinary non-symlink file contained by its root. Consumers never scan directories and never select by glob, basename, mtime, or “newest”. Package code never reads task `STATE.json`.

Closed domains:

- `implementation_phase=P0|P1|P2|P3`; `execution_phase=discovery|confirmation`.
- `protocol=A|B|C|D`; `run=1|2`; `shard=1|2`; `attempt=1|2`.
- `role=CONTEXT_MUTANT|SURFACE_MUTANT|CLEAN_CONTROL`.
- `finish_classification=FINISHED_SUCCESS|FINISHED_RETRYABLE|FINISHED_FATAL`.
- `attempt_state=ABSENT|IN_PROGRESS|FINISHED_RETRYABLE|FINISHED_FATAL|FINISHED_SUCCESS_RAW_MISSING|FINISHED_SUCCESS_RAW_PRESENT|STOP_AMBIGUOUS_STARTED`.
- `namespace_status=IN_PROGRESS|INCOMPLETE|STOP_NOT_SCORE|COMPLETE`; `NO_RUN` is in-memory only.
- `mutation_evidence_class=MECHANICAL_FIXTURE_ONLY|SEMANTIC_MUTATION_EVIDENCE`; `capture_label=REAL_CAPTURE|SIMULATED_CAPTURE`.

`cell_id` is exactly `<execution_phase>-<protocol>-run-<run>-shard-<shard>`. Unselected confirmation directories are absent.

## 2. Activation and identities

`receipts/ACTIVATION.json` has exact keys `schema_version,task_id,workspace_id,orchestrator_agent_id,activation_scope_sha256,activated_at`, schema `gemini-context-v5-execution-v2-activation/1`, and is ORCHESTRATOR write-once.

The exact `activation_scope_sha256` preimage is canonical JSON of this exact-key object:

```text
{allowed_paths,orchestrator_agent_id,task_id,user_authorization,workspace_id}
```

`allowed_paths` is the seven workspace-relative P0 paths in `SCOPE.json` order. `user_authorization` has exact keys `formal_inference,mutation_authoring,p0_p3_zero_call_implementation,qualification` and values `false,false,true,false`. The other three values equal the activation receipt. For the existing activation the canonical bytes hash to `a0b489eea1a622e677950792c85b01463e676e53a5500383ef967804d90f38a6`.

Two identities are independent:

```text
orchestration_candidate_ref = SHA256(SPEC raw bytes || 0x00 || bounded diff raw bytes)
package_candidate_sha256 = SHA256(canonical package candidate body)
```

The package candidate body has exact keys `schema_version,implementation_phase,activation_receipt_sha256,files,export_ids,exports,predecessor_pin_sha256s`, schema `gemini-context-v5-execution-v2-candidate/5`. `files` is a path-lexicographic nonempty array of exact `{path,sha256}` raw-byte records. `export_ids` is a unique subsequence of fixed order `p0-contracts,core,store,evidence,bin,integration`; `exports` has the same order and exact objects `export_id,files,exported_contract_sha256`. Every export hash is SHA-256 of canonical exact `{schema_version:"gemini-context-v5-execution-v2-export/1",export_id,files}`. The body excludes candidate hash, orchestration ref, phase ID, plan, manifest, review, gate, and pin hashes.

P0 has `export_ids=["p0-contracts"]`, no predecessor pins, and both candidate/export file arrays contain in this exact order: `ACCEPTANCE.md`, `ARCHITECTURE.md`, `MIGRATION.json`, `README.md`, `SCHEMA-CONTRACTS.md`, `STATE-MACHINE.json`, `TRUST-ROOTS.json`. ORCHESTRATOR derives both identities in memory. No pre-review artifact enters either preimage.

## 3. Receipt envelope and immutable pre-review plan

Every task receipt has exact envelope keys `schema_version,task_id,receipt_kind,receipt_variant,phase_id,orchestration_candidate_ref,package_candidate_sha256,activation_receipt_sha256,subject,issued_at,orchestrator_agent_id`, schema `gemini-context-v5-execution-v2-task-receipt/5`. Writer is the activation ORCHESTRATOR. Receipt fields copy already-frozen identities; package code cannot mint or modify receipts.

Closed kind/variant pairs are:

```text
PLAN/PHASE_PLAN                 PLAN/MUTATION_PLAN
AUTHORIZATION/QUALIFICATION_CAPTURE
AUTHORIZATION/DISCOVERY         AUTHORIZATION/CONFIRMATION
OBSERVATION/CHILD_WAITING        OBSERVATION/CHILD_STATUS
DISPATCH/GENERIC_DISPATCH        DISPATCH/QUALIFICATION_DISPATCH
COMPLETION/GENERIC_COMPLETION    COMPLETION/QUALIFICATION_COMPLETION
ARCHIVE/GENERIC_ARCHIVE          ARCHIVE/QUALIFICATION_ARCHIVE
AUDIT/ORPHAN_AUDIT               REVIEW/PHASE_REVIEW
GATE/PHASE_GATE                  GATE/MUTATION_GATE
GATE/FREEZE_GATE                 GATE/QUALIFICATION_CAPTURE_GATE
GATE/QUALIFICATION_GATE          GATE/DISCOVERY_GATE
GATE/CONFIRMATION_GATE           GATE/RESULT_GATE
PIN/MODULE_PIN                   QUALIFICATION_STARTED/QUALIFICATION_STARTED
```

Version is `v` plus three decimal digits. A phase plan path is `receipts/phases/<P0|P1|P2|P3>/versions/<vNNN>/PHASE-PLAN.json`; a repair plan path is `receipts/repairs/<repair-id>/versions/<vNNN>/PHASE-PLAN.json`. `repair_id` is null for a phase and `<implementation_phase>-R<NNN>` for a repair. `phase_id` is `<implementation_phase>-<version>` or `<repair_id>-<version>` and originates in this PHASE_PLAN, not in STATE or a later manifest.

PHASE_PLAN is issued exactly once after both candidate identities and `candidate_author_agent_id` have frozen and before either controlling review dispatch. Its subject exact keys are:

```text
implementation_phase,phase_id,version,repair_id,
orchestration_candidate_ref,package_candidate_sha256,candidate_author_agent_id,
normal_review_slot,senior_review_slot,prospective_manifest_path,prospective_gate_path
```

Each review slot has exact keys `dispatch_id,controlling_review_record_path,reviewer_role,purpose`; normal values are `REVIEWER,normal_review`, senior values are `senior-reviewer,cross_review`, and paths are the prospective `.ai/reviews/<task-id>/review-NN.json` and `senior-audit-NN.json`. Dispatch IDs, paths, roles, purposes, and the two agent identities eventually recorded must be distinct where applicable. The plan does not contain agent IDs because those are selected after the plan. It is immutable; infrastructure-invalid review requires a fresh versioned plan and content change requires a fresh repair/version plan.

The first conforming current-P0 instantiation is fixed as follows: plan `receipts/phases/P0/versions/v001/PHASE-PLAN.json`; `phase_id=P0-v001`; `version=v001`; `repair_id=null`; normal slot `dispatch_id=p0-normal-04`, record `.ai/reviews/research-gemini-context-counterexample-reviewer-v5-execution-v2/review-04.json`, role/purpose `REVIEWER/normal_review`; senior slot `dispatch_id=p0-senior-04`, record `.ai/reviews/research-gemini-context-counterexample-reviewer-v5-execution-v2/senior-audit-04.json`, role/purpose `senior-reviewer/cross_review`; prospective manifest `receipts/phases/P0/versions/v001/MANIFEST.json`; prospective gate `receipts/phases/P0/versions/v001/GATE.json`. It may lawfully be issued after these seven files and both identities freeze and before either dispatch, because it is excluded from both candidate hashes.

Every controlling review receives and records `phase_plan_path` and `phase_plan_sha256`. Its response document is the immutable controlling review JSON, exact keys:

```text
task_id,review_contract,review_phase,cycle,attempt,reviewer_role,purpose,
dispatch_id,agent_id,candidate_ref,package_candidate_sha256,
phase_plan_path,phase_plan_sha256,candidate_locator,completion_status,findings
```

`candidate_locator` is exact `{spec_path,diff_path}`; each finding is exact `{id,summary}`; `completion_status=PASS|CHANGES_REQUIRED|INVALID_INFRASTRUCTURE`. This response embeds no package completion/archive/review receipt hash. Existing earlier review records are historical and are not retrofitted.

After both controlling records exist and PASS, ORCHESTRATOR writes the manifest and then one normal and one senior `REVIEW/PHASE_REVIEW` receipt. These are one-way attestations to completed controlling records; they do not assert, fabricate, mirror, or require package DISPATCH/RESPONSE/COMPLETION/ARCHIVE events. PHASE_REVIEW subject exact keys are `reviewer_role,purpose,dispatch_id,agent_id,phase_plan_path,phase_plan_sha256,manifest_path,manifest_sha256,controlling_review_record_path,controlling_review_record_sha256,orchestration_candidate_ref,reviewed_package_candidate_sha256,verdict`. All values must equal the plan, manifest, and controlling record; verdict must be PASS for a positive phase gate.

## 4. Manifests, modules, and pins

Manifest paths are the plan’s `prospective_manifest_path`: `receipts/phases/<phase>/versions/<version>/MANIFEST.json` or `receipts/repairs/<repair-id>/versions/<version>/MANIFEST.json`. Manifests are authoritative ORCHESTRATOR task receipts/artifacts, not package-derived views.

A phase manifest exact keys are `schema_version,implementation_phase,phase_id,version,repair_id,phase_plan_path,phase_plan_sha256,orchestration_candidate_ref,package_candidate_sha256,activation_receipt_sha256,changed_modules,module_manifests,predecessor_pin_refs,pin_paths,paths,path_sha256s,receipt_paths,controlling_review_records`. `repair_id` is null. A repair manifest uses the same keys except `changed_modules,module_manifests,predecessor_pin_refs` are replaced by `invalidated_modules,fresh_module_manifests,unchanged_pin_refs`, and `repair_id` is non-null. Schemas are `...-phase-manifest/5` and `...-repair-manifest/5`. `controlling_review_records` is exactly `[normal,senior]`, each exact `{reviewer_role,path,sha256,dispatch_id,candidate_ref,package_candidate_sha256,phase_plan_sha256,completion_status}` and PASS. `receipt_paths` exact keys are `normal_review,senior_review,gate`; no mirrored lifecycle slots exist.

Each module manifest has exact keys `module,files,module_content_sha256,export_files,exported_contract_sha256,dependency_edges`. `files` is a nonempty path-lexicographic array of exact `{path,sha256}` where SHA-256 covers raw file bytes. `dependency_edges` is an ordered array of exact `{module,module_content_sha256,exported_contract_sha256}` in topological order. The exact module-content preimage is canonical JSON of exact:

```text
{schema_version:"gemini-context-v5-execution-v2-module-content/1",module,files,dependency_edges}
```

`module_content_sha256=SHA256` of those bytes. It excludes itself, exports, pins, plan, manifest, and review/gate hashes. `export_files` is the candidate export’s exact ordered file array and an ordered subset of `files`; `exported_contract_sha256` uses the export preimage in §2. Candidate exports, phase manifests, repair manifests, and pins must carry byte-identical module/file/edge hashes.

Edges are exactly `core=[]`, `store=[core]`, `evidence=[core,store]`, `bin=[core,store,evidence]`, and `integration=[core,store,evidence,bin]`. The integration module is not a directory scan: its `files` are exactly `integration/COMPOSITION.json` and `route/ROUTE.json` in lexical order; its `export_files` is exactly those same two records. `COMPOSITION.json` names the six fixed bin entry paths and their export hashes; integration imports no executable source and attests only fixed composition/route semantics. The bin module owns the six executable files.

Pin path is `receipts/pins/<module>/<phase_id>.json`. PIN subject exact keys are `module,module_content_sha256,exported_contract_sha256,dependency_pin_sha256s,normal_review_sha256,senior_review_sha256,orchestration_candidate_ref,package_candidate_sha256,manifest_sha256`. Pins issue in `core,store,evidence,bin,integration` order; each dependency pin already exists. Changed modules invalidate their exact reverse closure. Repairs bind exact unchanged pin `{module,path,sha256}` refs and fresh module manifests; preserved pins retain historical review hashes.

## 5. Fixed lifecycle and orphan audit

Generic DISPATCH subject exact keys are `dispatch_id,agent_id,parent_agent_id,workspace_id,role,purpose,input_path,input_sha256`. Generic COMPLETION is `dispatch_id,agent_id,output_path,output_sha256,terminal_status`, with `COMPLETED`. Generic ARCHIVE is `dispatch_id,agent_id,completion_receipt_path,completion_receipt_sha256,archive_confirmed`, with literal true. They are one-way: output documents never embed completion/archive hashes.

Formal orphan evidence paths for an exact authorized cell/attempt are:

```text
receipts/formal/status-observations/<cell-id>/attempt-<1|2>.json
receipts/formal/orphan-audits/<cell-id>/attempt-<1|2>.json
```

Qualification paths are `receipts/qualification/STATUS-OBSERVATION.json` and `receipts/qualification/ORPHAN-AUDIT.json`. ORCHESTRATOR exclusively creates each at most once.

CHILD_STATUS observation subject exact keys are `namespace_kind,subject_id,attempt,dispatch_id,agent_id,parent_agent_id,workspace_id,observed_status,active_turn_present,observation_source,observed_at`; `namespace_kind=FORMAL|QUALIFICATION`, qualification attempt is 1, `observed_status=COMPLETED|FAILED|CANCELLED|STOPPED|ACTIVE|UNKNOWN`, and `observation_source=live_agent_metadata`. It must bind the same child as STARTED. An observation with ACTIVE, UNKNOWN, missing identity proof, or `active_turn_present=true` cannot support an orphan audit.

ORPHAN_AUDIT subject exact keys are `audit_id,namespace_kind,subject_id,attempt,started_path,started_sha256,finished_path,status_observation_path,status_observation_sha256,dispatch_id,agent_id,parent_agent_id,workspace_id,finished_absent,conclusion`. `finished_path` is the fixed expected FINISHED path; `finished_absent` must be literal true. The sole allowed positive conclusion is `TERMINAL_NO_FINISHED`. It is valid only if STARTED is valid, the status observation is valid and identity-equal, observed status is one of COMPLETED/FAILED/CANCELLED/STOPPED, active turn is false, and FINISHED is still absent when the audit is exclusive-created. Unknown evidence remains `IN_PROGRESS`; only this valid audit permits `STOP_AMBIGUOUS_STARTED`, which maps to `STOP_NOT_SCORE`. Audit/observation are authoritative state-derivation facts and cannot be inferred from STATE, elapsed time, a stale status, or missing files alone.

## 6. Formal STARTED, FINISHED, RAW, and ledger

`STARTED.json` exact keys are `schema_version,cell_id,execution_phase,protocol,run,shard,attempt,request_sha256,route_document_sha256,expanded_argv_sha256,authorization_receipt_sha256,dispatch_receipt_sha256,dispatch_id,agent_id,parent_agent_id,workspace_id,started_at`, schema `...-started/4`. Durable STARTED precedes spawn.

`CAPTURE.json` exact keys are `schema_version,capture_kind,subject_id,attempt,route_document_sha256,executable_realpath,executable_sha256,argv,argv_sha256,child_env_sha256,timeout_ms,stdin_policy,stdout_path,stderr_path,stdout_sha256,stderr_sha256`, with `capture_kind=FORMAL|QUALIFICATION`.

`FINISHED.json` exact keys are `schema_version,cell_id,attempt,started_sha256,capture_metadata_sha256,stdout_sha256,stderr_sha256,exit_code,classification,adapted_response_sha256,finished_at`, schema `...-finished/4`. Success response hash preimage is exactly `UTF8(canonical_json(strict_adapted_response_object))`; it excludes every FINISHED/RAW envelope field. Retryable/fatal use null. FINISHED contains no RAW hash.

`execution/RAW/<cell-id>.json` exact keys are `schema_version,cell_id,attempt,request_sha256,route_document_sha256,started_sha256,finished_sha256,stdout_sha256,stderr_sha256,response`, schema `...-raw/4`. Validation order is response schema/hash, FINISHED bytes/hash, then all remaining bindings. Missing success RAW is exclusive-created from facts without invocation; exact existing bytes pass and mismatch stops without overwrite.

`execution/RECOVERY-LEDGER.json` exact keys are `schema_version,namespace_status,cells`, schema `...-recovery-ledger/4`. Cells are in authorized cell order and exact `cell_id,attempts,attempt_state,raw_path,raw_sha256,orphan_audit_path,orphan_audit_sha256`; nonapplicable values are null. Authoritative derivation reads only fixed authorization/dispatch, STARTED/capture/FINISHED, status-observation/orphan-audit facts and RAW. Attempt sequences are `[1]` or `[1,2]`; attempt 2 requires valid attempt-1 retryable FINISHED. Ledger is exact-byte idempotent.

The formal namespace is empty only if no authorization, dispatch, attempt directory, STARTED, status observation/audit, capture, FINISHED, RAW, ledger, SCORES, gate, or RESULT exists. Only then may an in-memory `NO_RUN` be reported.

## 7. Qualification closure

Fixed paths are:

```text
receipts/qualification/AUTHORIZATION.json
receipts/qualification/WAITING-OBSERVATION.json
receipts/qualification/DISPATCH.json
receipts/qualification/QUALIFICATION-STARTED.json
receipts/qualification/CAPTURE-GATE.json
qualification/stdout.bin
qualification/stderr.bin
qualification/CAPTURE.json
qualification/FINISHED.json
qualification/CAPTURE-SUMMARY.json
receipts/qualification/COMPLETION.json
receipts/qualification/ARCHIVE-QUALIFICATION.json
qualification/QUALIFICATION-EVIDENCE.json
receipts/qualification/FINAL-GATE.json
```

AUTHORIZATION/QUALIFICATION_CAPTURE subject exact keys are `authorization_id,scope,qualification_id,dispatch_id,dispatch_receipt_path,request_manifest_path,request_manifest_sha256,request_path,request_sha256,route_path,route_document_sha256,allowed_agent_id,parent_agent_id,workspace_id`; scope is `QUALIFICATION_CAPTURE`. The qualification dispatch ID originates only here after the waiting child identity freezes; DISPATCH must copy it.

CHILD_WAITING subject exact keys are `qualification_id,dispatch_id,agent_id,parent_agent_id,workspace_id,role,purpose,provider_process_spawned,active_turn_waiting,observed_at`; role/purpose are `EXECUTOR,qualification_capture`, `provider_process_spawned=false`, and `active_turn_waiting=true`.

QUALIFICATION_DISPATCH extends generic DISPATCH with exact additional keys `qualification_id,authorization_receipt_sha256,request_sha256,route_document_sha256,expanded_argv_sha256`; all identities equal authorization/waiting evidence. QUALIFICATION_STARTED subject exact keys are `qualification_id,authorization_receipt_sha256,waiting_observation_sha256,dispatch_receipt_sha256,request_sha256,route_document_sha256,expanded_argv_sha256,dispatch_id,agent_id,parent_agent_id,workspace_id,purpose,started_at`.

CAPTURE-GATE ordered inputs are AUTHORIZATION, WAITING-OBSERVATION, DISPATCH, QUALIFICATION-STARTED, request, and route. The waiting child may be released only after package code validates the exact gate and decision `QUALIFICATION_CAPTURE_GO`; `qualify-capture` must consume that gate before spawn. A missing/negative/mismatched gate leaves the child waiting and invokes nothing.

Qualification FINISHED exact keys are `schema_version,qualification_id,started_receipt_sha256,capture_metadata_sha256,stdout_sha256,stderr_sha256,exit_code,classification,adapted_response_sha256,finished_at`, schema `...-qualification-finished/3`; retryable is forbidden.

`adapter_result` is exact `{schema_version,status,response_sha256,response_item_count}` with schema `gemini-context-v5-execution-v2-adapter-result/1`, `status=PASS`, response hash equal FINISHED, and item count equal the frozen request count. `qualification/CAPTURE-SUMMARY.json` exact keys are `schema_version,qualification_id,request_sha256,route_document_sha256,started_receipt_sha256,capture_metadata_path,capture_metadata_sha256,stdout_path,stdout_sha256,stderr_path,stderr_sha256,finished_path,finished_sha256,adapter_result`, schema `...-capture-summary/1`. Its hash preimage is exactly its canonical full object bytes. QUALIFICATION_COMPLETION extends generic completion with `qualification_id,capture_metadata_sha256,stdout_sha256,stderr_sha256,finished_sha256`; `output_path` is this fixed summary and `output_sha256` is its canonical-byte hash. QUALIFICATION_ARCHIVE extends generic archive with `qualification_id,dispatch_receipt_sha256,request_sha256,capture_metadata_sha256,finished_sha256`.

`qualification/QUALIFICATION-EVIDENCE.json` exact keys are `schema_version,qualification_id,package_candidate_sha256,request_sha256,route_document_sha256,capture_gate_sha256,capture_summary_sha256,capture_metadata_sha256,started_receipt_sha256,completion_receipt_sha256,archive_receipt_sha256,adapted_response_sha256,adapter_result,status`, schema `...-qualification-evidence/5`, status `QUALIFIED`. Pure finalization validates in order: activation/phase pins; authorization/waiting/dispatch/STARTED/CAPTURE-GATE; request/route; stdout/stderr/CAPTURE/FINISHED; strict adaptation and adapter_result; CAPTURE-SUMMARY; COMPLETION; ARCHIVE. It then exclusive-creates evidence and cannot invoke. FINAL-GATE consumes all of these. Qualification has no retry; orphan semantics are §5.

## 8. Class M and Class S plan

Class M path is `tests/fixtures/mechanical/MUTATIONS.json`, schema `...-mechanical-fixture/3`, exact top keys `schema_version,evidence_class,fixture_id,generator_id,generator_description,rows`, class `MECHANICAL_FIXTURE_ONLY`. It can never satisfy MUTATION_GO.

Class S first creates two distinct direct children, both waiting without work. ORCHESTRATOR then writes fixed `receipts/mutation/PLAN.json` as PLAN/MUTATION_PLAN before either dispatch. Subject exact keys are:

```text
plan_id,author_agent_id,validator_agent_id,parent_agent_id,workspace_id,
author_role,author_purpose,validator_role,validator_purpose,
author_dispatch_id,author_dispatch_path,validator_dispatch_id,validator_dispatch_path,
proposal_path,validation_path,mutation_gate_path
```

Roles are both `EXECUTOR`; purposes are `semantic_mutation_author` and `semantic_mutation_validator`; agent IDs and dispatch IDs differ; both children are direct children of the exact activation ORCHESTRATOR in the activation workspace. Paths are exactly the fixed paths below. PLAN is immutable and one-way; children, dispatches, or lifecycle records cannot be reused across roles.

```text
receipts/mutation/PLAN.json
receipts/mutation/AUTHOR-DISPATCH.json
mutation/SEMANTIC-PROPOSALS.json
receipts/mutation/AUTHOR-COMPLETION.json
receipts/mutation/AUTHOR-ARCHIVE.json
receipts/mutation/VALIDATOR-DISPATCH.json
mutation/SEMANTIC-VALIDATIONS.json
receipts/mutation/VALIDATOR-COMPLETION.json
receipts/mutation/VALIDATOR-ARCHIVE.json
receipts/mutation/GATE.json
```

Proposal exact keys are `schema_version,evidence_class,package_candidate_sha256,predecessor_sha256s,mutation_plan_sha256,author_dispatch_receipt_sha256,rows`; validation exact keys are `schema_version,evidence_class,package_candidate_sha256,mutation_plan_sha256,proposal_sha256,validator_dispatch_receipt_sha256,rows`; schemas are `...-semantic-proposals/5` and `...-semantic-validations/5`. Proposal has exactly 40 frozen rows (24 context, 16 surface). Row schemas remain those in the retained design: proposal exact `item_id,role,cohort,profile,kind,source,target,normalized_context,source_sha256,target_sha256,normalized_context_sha256,claim_type,atom,edit_original,edit_mutated,mutated_target,reconstruction_occurrence_count,row_sha256`; validation exact `item_id,proposal_row_sha256,source_sha256,target_sha256,normalized_context_sha256,one_atom,minimal_unique_edit,surface_verdict,context_verdict,pass,validation_row_sha256`. Row hashes exclude themselves.

AUTHOR-DISPATCH copies plan identity and binds assignment/predecessors; completion points to proposal; archive points to completion. Only after author archive may validator be released. VALIDATOR-DISPATCH copies plan identity and binds proposal; completion points to validation; archive points to completion. Outputs embed no downstream lifecycle/gate hash. MUTATION consumes PLAN, both documents, and all six lifecycle receipts and validates direct-child independence.

## 9. Discovery/confirmation authorization and score/result documents

AUTHORIZATION/DISCOVERY subject exact keys are `authorization_id,scope,phase_id,freeze_gate_path,freeze_gate_sha256,qualification_gate_path,qualification_gate_sha256,request_manifest_path,request_manifest_sha256,route_path,route_document_sha256,ordered_cells`; scope is `DISCOVERY`. `ordered_cells` is the exact 16-cell order from the request manifest; each exact object is `cell_id,dispatch_id,dispatch_receipt_path,request_path,request_sha256`. This is the sole source of formal discovery dispatch IDs.

AUTHORIZATION/CONFIRMATION subject exact keys are `authorization_id,scope,phase_id,discovery_gate_path,discovery_gate_sha256,discovery_scores_path,discovery_scores_sha256,winner_protocol,request_manifest_path,request_manifest_sha256,route_path,route_document_sha256,ordered_cells`; scope is `CONFIRMATION`. Winner is B/C/D and ordered_cells is exactly A then winner, each run then shard (8 cells), or no confirmation authorization exists after `STOP_NO_WINNER`. It is the sole source of confirmation dispatch IDs.

Two immutable score documents prevent retrospective overwrite. `execution/discovery/SCORES.json` is exclusive-created at discovery closure; root `SCORES.json` is exclusive-created only after successful confirmation. Both have exact top-level keys `schema_version,namespace_status,discovery,confirmation,scores_sha256`, schema `...-scores/1`; the hash is canonical top-level object excluding itself. `discovery` exact keys are `status,cell_scores,protocol_summaries,winner_protocol`; `confirmation` is null in discovery SCORES and, in root SCORES, has exact keys `status,cell_scores,protocol_summaries`. Status is `COMPLETE`. Every `cell_scores` entry follows authorization order and exact keys `cell_id,protocol,run,shard,raw_sha256,context_hits,surface_hits,clean_with_findings`. Every summary follows protocol order and exact keys `protocol,context_hits,surface_hits,clean_with_findings`; values are exact sums of cells. Discovery winner applies per-run context gain versus A >=3, surface hits >=A, clean-with-findings <=A, then ranks aggregate context gain descending, clean-with-findings ascending, D/C/B. `winner_protocol` is B/C/D or null. The root SCORES discovery object must byte-semantically equal the immutable discovery SCORES discovery object.

`RESULT.json` exact top-level keys are `schema_version,namespace_status,winner_protocol,discovery,confirmation,result_sha256`, schema `...-result/4`, status `COMPLETE`; hash excludes itself. `discovery` exact keys are `gate_sha256,scores_sha256,protocol_summaries,winner_protocol`; `confirmation` exact keys are `gate_sha256,scores_sha256,protocol_summaries,confirmed_winner_protocol`. Summary objects are exactly the SCORES summaries. `confirmed_winner_protocol` equals top-level winner and the authorized winner. No winner or STOP_NOT_SCORE produces no RESULT.

## 10. Eleven gate contracts

Every gate subject has exact keys `gate_name,decision,ordered_inputs,predecessor_gate_refs,output_document_sha256`. `ordered_inputs` is an array of exact `{path,sha256}` in the table order. `predecessor_gate_refs` is an array of exact `{implementation_phase,path,sha256}`; it is `[]` for P0 and every downstream non-implementation gate, `[P0]` for P1, `[P0,P1]` for P2, and `[P0,P1,P2]` for P3, with paths/hashes of the exact positive phase gates. `output_document_sha256` is null except RESULT.

Path tokens below are exact aliases: ACTIVATION=`receipts/ACTIVATION.json`; PHASE_PLAN/current MANIFEST/gate are the exact paths in the plan; normal/senior controlling records and PHASE_REVIEW are the exact paths in plan/manifest; BASES=`frozen/BASES.json`; ASSIGNMENT-PLAN=`frozen/ASSIGNMENT-PLAN.json`; SAMPLES=`frozen/SAMPLES.json`; REQUEST-MANIFEST=`frozen/REQUEST-MANIFEST.json`; REFERENCE=`sealed/REFERENCE.json`; ROUTE=`route/ROUTE.json`; discovery scores=`execution/discovery/SCORES.json`; root scores=`SCORES.json`; ledger=`execution/RECOVERY-LEDGER.json`; RESULT=`RESULT.json`. For an authorization-ordered cell and attempt `n`, its fact bundle is exactly: authorization-listed dispatch receipt, `execution/attempts/<cell-id>/attempt-<n>/STARTED.json`, `stdout.bin`, `stderr.bin`, `CAPTURE.json`, `FINISHED.json`, then `execution/RAW/<cell-id>.json`. Attempt 2 bundle replaces attempt 1 only after the attempt-1 bundle ending in retryable FINISHED (without RAW) is inserted immediately before it. An audited orphan bundle is exactly dispatch, STARTED, the authorization-derived fixed CHILD_STATUS path, and fixed ORPHAN_AUDIT path, and selects a STOP decision. Thus expansion is a pure function of a named immutable plan/authorization and validated attempt 1, never filesystem enumeration.

For every row, the named positive predicate selects only its positive decision; predicate false selects the listed NO_GO decision, except the separately stated STOP predicate. No decision may be chosen merely because an input is absent. Unknown/in-progress means no gate receipt is issuable.

| gate / fixed path | exact ordered path/hash inputs | decision predicate |
|---|---|---|
| P0 / plan `prospective_gate_path` | ACTIVATION, PHASE_PLAN, MANIFEST, normal controlling review, senior controlling review, normal PHASE_REVIEW, senior PHASE_REVIEW | identities/plan/manifest exact, both controlling records and attestations PASS, seven-file P0 candidate valid; else `P0_NO_GO` |
| P1 / plan path | ACTIVATION, PHASE_PLAN, MANIFEST, normal controlling review, senior controlling review, normal PHASE_REVIEW, senior PHASE_REVIEW, exact P0 gate | P0 chain ref/hash exact, core/store module preimages and pins valid, dual PASS; else `P1_NO_GO` |
| P2 / plan path | ACTIVATION, PHASE_PLAN, MANIFEST, normal controlling review, senior controlling review, normal PHASE_REVIEW, senior PHASE_REVIEW, exact P0 gate, exact P1 gate | both chain refs/hashes exact, P1 pins and P2 evidence/bin/integration closure valid, dual PASS; else `P2_NO_GO` |
| P3 / plan path | ACTIVATION, PHASE_PLAN, MANIFEST, normal controlling review, senior controlling review, normal PHASE_REVIEW, senior PHASE_REVIEW, exact P0, P1, P2 gates | all three chain refs/hashes exact, all pins and labelled offline tests valid, zero calls; positive only `ZERO_CALL_IMPLEMENTATION_COMPLETE`, else `ZERO_CALL_IMPLEMENTATION_INCOMPLETE` |
| MUTATION / `receipts/mutation/GATE.json` | mutation PLAN, AUTHOR-DISPATCH, proposal, AUTHOR-COMPLETION, AUTHOR-ARCHIVE, VALIDATOR-DISPATCH, validation, VALIDATOR-COMPLETION, VALIDATOR-ARCHIVE | valid independent direct children, one-way links, all 40 Class S rows pass; else `NO_GO_MUTATION` |
| FREEZE / `receipts/formal/FREEZE-GATE.json` | positive MUTATION gate, `frozen/BASES.json`, `frozen/ASSIGNMENT-PLAN.json`, `frozen/SAMPLES.json`, `frozen/REQUEST-MANIFEST.json`, `sealed/REFERENCE.json`, `route/ROUTE.json` | retained counts/order/hashes/schema/fallback/size constraints exact and sealed reference excluded from requests; else `NO_GO_FREEZE` |
| QUALIFICATION_CAPTURE / `receipts/qualification/CAPTURE-GATE.json` | qualification AUTHORIZATION, WAITING-OBSERVATION, DISPATCH, QUALIFICATION-STARTED, authorized request, route | waiting direct child exact, no spawn, all hash/identity/argv bindings valid; `QUALIFICATION_CAPTURE_GO` is consumed before release, else `NO_GO_QUALIFICATION_CAPTURE` |
| QUALIFICATION / `receipts/qualification/FINAL-GATE.json` | CAPTURE-GATE, AUTHORIZATION, WAITING-OBSERVATION, DISPATCH, STARTED, request, route, stdout, stderr, CAPTURE, FINISHED, CAPTURE-SUMMARY, COMPLETION, ARCHIVE, QUALIFICATION-EVIDENCE; or STARTED, STATUS-OBSERVATION, ORPHAN-AUDIT for orphan terminal | full ordered successful closure gives `QUALIFICATION_GO`; sole valid audited orphan gives `STOP_AMBIGUOUS_STARTED`; otherwise `NO_GO_QUALIFICATION` and unknown remains IN_PROGRESS |
| DISCOVERY / `receipts/formal/DISCOVERY-GATE.json` | `receipts/formal/DISCOVERY-AUTHORIZATION.json`, then each of 16 authorized cell bundles, ledger, discovery scores | exact complete attempt/RAW bijection, valid immutable discovery score derivation, no orphan/fatal/ambiguity gives `DISCOVERY_GO`; any structurally invalid pre-execution input gives `NO_GO_DISCOVERY`; an audited/corrupt terminal execution leaves namespace STOP_NOT_SCORE and cannot issue DISCOVERY_GO |
| CONFIRMATION / `receipts/formal/CONFIRMATION-GATE.json` | `receipts/formal/DISCOVERY-GATE.json`, discovery scores; if winner: `receipts/formal/CONFIRMATION-AUTHORIZATION.json`, each of 8 authorized cell bundles, ledger, root scores | null winner in valid discovery scores plus complete absence of confirmation authorization/facts/root scores gives `STOP_NO_WINNER`; eligible winner plus complete valid closure/root score derivation gives `CONFIRMATION_GO`; invalid prerequisite gives `NO_GO_CONFIRMATION` |
| RESULT / `receipts/formal/RESULT-GATE.json` | `receipts/formal/DISCOVERY-GATE.json`, `receipts/formal/CONFIRMATION-GATE.json`, ledger, root scores, RESULT | COMPLETE namespace, positive confirmation, exact score/result derivation and `output_document_sha256=SHA256(RESULT raw canonical bytes)` gives `RESULT_GO`; any valid audited-orphan/fatal/corrupt terminal set with RESULT absent gives `STOP_NOT_SCORE`; incomplete/unknown issues no gate |

Negative decisions never authorize the next stage. `P3_GO` is invalid. Gate validators reject omitted/extra/reordered inputs even if hashes are otherwise valid.

## 11. Production surface

`route/ROUTE.json` exact keys are `schema_version,route_id,executable_absolute_path,executable_realpath,executable_sha256,executable_mode,model,effort,mode,argv_template,timeout_ms,stdin_policy,child_env`, schema `...-route/2`. P2 resolves one absolute ordinary non-symlink executable before review. `{request_absolute_path}` and `{output_mode}` are whole-token substitutions; output mode is exactly `json`; stdin is `CLOSED_EMPTY`; child environment is exact and uninherited.

Future production files are only `bin/freeze.mjs`, `bin/qualify-capture.mjs`, `bin/qualify-finalize.mjs`, `bin/run-discovery.mjs`, `bin/run-confirmation.mjs`, and `bin/post-run.mjs`. They are zero-argument programs, reject stdin/config/import/callback/environment capability overrides, and expose no root, STATE, route, executable, receipt, authorization, invoke, or `allowExecution` injection. They are absent in P0.
