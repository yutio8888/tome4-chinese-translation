#!/usr/bin/env node
// One-shot authoring helper for the canonical contract JSON files of this package.
// Kept in-tree so every contract byte in MANIFEST.json is reproducible by rerunning it.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {jsonBytes,readCanonical,sha256} from '../lib.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const route=readCanonical(path.join(root,'ROUTE-CONTRACT.json'));
const qualifiedSha256='d492241f19f90ea06cb9f85f7788c371dbce3386206d734ddc2c7ec84fa3ddca';
const originalPath='/home/yun/.local/bin/agy',relocatedPath='/home/yun/.local/bin/agy.1788410029995956792.old';
const generatedRoute={
  schema_version:'gemini-context-v5-execution-route-v5',
  status:'UNQUALIFIED_EXECUTION_UNAUTHORIZED',
  host_specific:'contains a verified local absolute agy path; this is not a portable release artifact',
  cli_contract:{...route.cli_contract,executable:relocatedPath,executable_sha256:qualifiedSha256},
  environment:{...route.environment,allowlist_rationale:'spawnSync replaces the environment wholesale, so anything absent from this list is absent from the agy process. HOME/XDG_*/TMPDIR are where agy resolves its own config, cache and credential store; the five credential names are read by the binary (each occurs in `strings /home/yun/.local/bin/agy.1788410029995956792.old`). Without them call 1 exits non-zero and spends an authorized process.'},
  qualification:{...route.qualification,model_list_argv:['models']},
  runner_may_execute_only_after:['PACKAGE_REVIEW','QUALIFICATION','EXECUTION_AUTHORIZATION'],
  invoked_during_freeze:false
};
const relocatedRouteSha256=sha256(jsonBytes(generatedRoute));
const docs={
'EXPERIMENT.json':{
  schema_version:'gemini-context-v5-execution-experiment-v4',
  experiment_id:'gemini-context-counterexample-reviewer-v5-execution-v4',
  task_id:'research-gemini-context-counterexample-reviewer-v5-execution-v4',
  status:'NO_RUN_P0_PACKAGE_PENDING_PACKAGE_REVIEW',
  question:'Does a checklist prompt and/or bounded source context change the gemini-3.7-flash-high review route context-hit, surface-hit and clean-false-positive counts?',
  predecessor_terminal_gate_sha256:'8495fd3bbe3211314607db67314360fd983d30f9455063b49d0e0a28a587d907',
  predecessor_active_frame_sha256:'e905cc4b6537427f183137e9cb4694cdc2baa7c43215211e85b904a1e864c6c3',
  predecessor_terminal_result_sha256:'44726a9f538cb5ec3e63c64be64437fb2f0014f496b80d312647e240b8b550bd',
  predecessor_trees_byte_immutable:['evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5','evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v1','evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v2'],
  predecessor_execution_v3_tree:{root:'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5-execution-v3',file_count:74,tree_sha256:'83201688dfa55420330766ef8b1c75954058cd4103ed10f4fee418979d5867c6'},
  route_evidence:{agy_binary_path:relocatedPath,agy_binary_sha256:qualifiedSha256,original_capture_path:originalPath,original_route_contract_sha256:'742529e3c3d1d76bbc324e66cbdae48b3286cc37d3bea8f8e4260cea4ccac8b7',route_relocation_contract:'ROUTE-RELOCATION-CONTRACT.json',rejected_upgraded_binary_sha256:'f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e',v3_tree_sha256:'83201688dfa55420330766ef8b1c75954058cd4103ed10f4fee418979d5867c6'},
  bases:64,
  request_identities:32,
  mutations_authored:0,
  mutation_authoring_in_scope:false,
  qualification_run:false,
  agy_processes_spawned:0,
  inference_calls_made:0,
  network_calls_made:0,
  pilot_authorization:{agy_process_budget:4,inference_call_budget:3,retries:0,cells:['qualification-models-list','qualification-synthetic','discovery-A-run-1-shard-1','discovery-C-run-1-shard-1'],cells_journaled_in:'execution/LEDGER.jsonl',process_counters_source:'DERIVED_FROM_LEDGER_START_ROWS',full_run:'SEPARATE_AUTHORIZATION_REQUIRED'},
  claims_excluded:['pretraining novelty','contamination freedom','repository-wide prevalence','generalization beyond the frozen sample','model effectiveness before inference','any protocol comparison derived from the pilot'],
  qualification_driver_tested:'MOCK_PROCESS_ONLY_NOT_REAL_CLI'
},
'GATES.json':{
  schema_version:'gemini-context-v5-execution-gates-v1',
  status:'NO_RUN_NO_GATE_SATISFIED',
  authoritative_gate_logic:'gates.mjs. Exactly three blocking gates, each a task-owned file that this package reads and never writes.',
  gate_count:3,
  gate_order:['PACKAGE_REVIEW','QUALIFICATION','EXECUTION_AUTHORIZATION'],
  gates:{
    PACKAGE_REVIEW:{path:'.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/PACKAGE-REVIEW-GATE.json',satisfied:false,meaning:'frozen checklist C01-C14 all PASS against this MANIFEST.json'},
    QUALIFICATION:{path:'.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/QUALIFICATION-GATE.json',satisfied:false,meaning:'archived two-stage route qualification evidence, reported model gemini-3.7-flash-high'},
    EXECUTION_AUTHORIZATION:{path:'.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/EXECUTION-AUTHORIZATION.json',satisfied:false,meaning:'exact authorized cells, route contract hash, request manifest hash and process budget'}
  },
  identity_binding:'manifest_sha256 only; gates 2 and 3 additionally bind the byte hash of their direct predecessor gate',
  removed_in_predecessor:['CANDIDATE-IDENTITY','HASH-DAG','dual-review predicates','mutation gate','freeze gate','discovery completion receipt','confirmation authorization'],
  agy_processes_spawned:0,
  inference_calls_made:0,
  network_calls_made:0,
  qualification_is_scored:false
},
'DESIGN-CONTRACT.json':{
  schema_version:'gemini-context-v5-execution-design-v5',
  status:'FROZEN_NO_RUN',
  sample:{total:64,items_per_cohort_profile:16,reselection:false,reserve_replacement:false},
  mutations:{authored:false,in_scope_for_this_task:false,consequence:'every sealed reference row is a CLEAN_CONTROL with zero atoms, so only clean_with_findings is exercised by a real call; context_hits and surface_hits are exercised by the scorer fixture'},
  protocols:{
    A:{prompt:'model-facing/prompts/GENERIC.md',context:false},
    B:{prompt:'model-facing/prompts/ENHANCED.md',context:false},
    C:{prompt:'model-facing/prompts/GENERIC.md',context:true},
    D:{prompt:'model-facing/prompts/ENHANCED.md',context:true}
  },
  execution:{runs:2,items_per_shard:16,shards_per_cohort:2,cohorts:['discovery','confirmation'],frozen_request_count:32,cell_id:'<cohort>-<protocol>-run-<run>-shard-<shard>',cells_runnable:'only the ids listed in the task-owned EXECUTION-AUTHORIZATION'},
  scoring:{scorer:'scorer.mjs',span_containment:'one direction: the reported target_span must contain the frozen atom span',counts:['context_hits','surface_hits','clean_with_findings'],winner_selection:'NOT_IN_THIS_TASK'},
  stopping:{attempts_per_cell_max:1,second_attempt_allowed:false,started_without_finished_blocks_replay:true,exit_zero_with_unextractable_envelope_is_terminal_failure:true,raw_derived_from_captured_stdout_only:true,raw_overwrite:false},
  context_render_schema:'runtime-context-text-v2',
  source_construct_policy:'COMPLETE_NEVER_RENDERER_TRUNCATED_EXACT_SOURCE_PRESENT'
},
'REQUEST-CONTRACT.json':{
  schema_version:'gemini-context-v5-execution-request-contract-v5',
  status:'FROZEN_NO_RUN',
  request_count:32,
  cell_axes:{cohorts:['discovery','confirmation'],protocols:['A','B','C','D'],runs:[1,2],shards:[1,2]},
  items_per_request:16,
  manifest:'frozen/REQUEST-MANIFEST.json',
  context_render:{schema:'runtime-context-text-v2',segment_order:['BEFORE','SOURCE_CONSTRUCT','AFTER'],segment_max_utf8_bytes:8192,request_max_utf8_bytes:120000,coordinates:['line_start','line_end','byte_start','byte_end_exclusive'],source_and_renderer_truncation_are_separate:true,deterministic_sentinels_required:true,source_construct_never_renderer_truncated:true,exact_item_source_required:true,exact_source_appended_count:7},
  model_facing_item_keys:{A_B:['item_id','source','target'],C_D:['item_id','source','target','source_context']},
  leakage_policy:{structured_key_scan:true,explicit_marker_and_path_scan:true,ordinary_words_in_natural_text_are_not_blanket_banned:['reference','sealed','defect'],internal_identifiers_forbidden:['proposal_sha256','row_sha256','base_item_id','planned_role','public_source_file','revision_uid','normalized_context_sha256']},
  parser:{exact_outer_and_inner_schemas:true,duplicate_keys_rejected_at_all_json_layers:true,exact_item_order_and_count:true,candidate_cap_per_item:4,evidence_and_target_membership_required:true,runtime_model_self_report_not_trusted:true,scorable_identity_tier:'QUALIFIED_ROUTE_BOUND',agy_dual_channel:{structured_output_authoritative:true,response_when_present_must_be_json_string:true,response_items_must_equal_structured_output_items:true,response_metadata_outside_items_allowed:true,single_channel_supported:true,mismatch_fails_closed:true}},
  recovery:{ledger:'execution/LEDGER.jsonl',ledger_form:'append-only JSONL, keys {attempt, cell, started_at, finished_at, exit, stdout_sha256, stderr_sha256}',state_source:'DERIVED_FROM_LEDGER_ROWS_ONLY',journaled_cells:'the 32 execution cell ids plus qualification-models-list and qualification-synthetic',process_counters_source:'DERIVED_FROM_LEDGER_START_ROWS',attempts_max:1,attempt_sequence:['[1]'],second_attempt_allowed:false,started_without_finished_blocks_replay:true,exit_zero_with_unextractable_envelope_is_terminal_failure:true,captures:'execution/captures/<cell>-attempt-<n>.std{out,err}.bin',qualification_captures:'qualification/captures/<cell>-attempt-<n>.std{out,err}.bin',raw:'execution/RAW/<cell>-attempt-<n>.json',raw_exclusive_create:true,raw_derived_from_captured_stdout_only:true}
},
'ROUTE-CONTRACT.json':generatedRoute,
'ROUTE-RELOCATION-CONTRACT.json':{
  schema_version:'gemini-context-v5-execution-route-relocation-v1',
  status:'SAME_BYTE_RELOCATION_ONLY',
  original_route:{path:'ROUTE-CONTRACT.json',sha256:'742529e3c3d1d76bbc324e66cbdae48b3286cc37d3bea8f8e4260cea4ccac8b7'},
  relocated_route:{path:'ROUTE-CONTRACT.json',sha256:relocatedRouteSha256},
  original_executable:{path:originalPath,sha256:qualifiedSha256},
  relocated_executable:{path:relocatedPath,sha256:qualifiedSha256},
  rejected_upgraded_executable:{path:originalPath,sha256:'f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e'},
  identity_rule:'Captured qualification provenance retains the original route hash and executable path. It is accepted only because this contract binds the currently configured relocated path to identical qualified executable bytes; the upgraded bytes at the original path are rejected and cannot inherit the qualified identity.'
}
};
for(const [name,value] of Object.entries(docs))fs.writeFileSync(path.join(root,name),jsonBytes(value));
console.log(JSON.stringify({written:Object.keys(docs)}));
