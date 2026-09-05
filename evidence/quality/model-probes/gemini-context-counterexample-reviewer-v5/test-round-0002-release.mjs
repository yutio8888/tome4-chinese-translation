#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {ROUND2_DECISIONS, ROUND2_EXPECTED_CORE_HASHES, ROUND2_MATERIALIZATION_BOUNDARIES, ROUND2_PREDECESSOR, ROUND2_RELEASE_EXCLUSIONS, ROUND2_RELEASE_HISTORY_PATHS, ROUND2_RELEASE_PATHS, ROUND2_RELEASE_RECEIPT_PATHS, deriveRound2Fixture, evaluateRound2ReleaseReviewGate, jsonBytes, materializeRound2CompletedFixture, materializeRound2Release, sha256, validateRound2PendingRelease} from './round-0002-release.mjs';
import {checkReplay} from './replay.mjs';
import {runPreflight} from './preflight.mjs';

const root = path.dirname(fileURLToPath(import.meta.url)), repo = path.resolve(root, '..', '..', '..', '..');
const EXPECTED_MATERIALIZATION_BOUNDARIES = [
  'after_create_transaction',
  'after_stage_round2_release', 'after_stage_active_frame', 'after_stage_lineage',
  'after_stage_reserve_state', 'after_stage_round_index', 'after_stage_release_state',
  'after_stage_experiment', 'after_backup_active_frame', 'after_backup_lineage',
  'after_backup_reserve_state', 'after_backup_round_index', 'after_backup_release_state',
  'after_backup_experiment', 'after_install_round2_release', 'after_install_active_frame',
  'after_install_lineage', 'after_install_reserve_state', 'after_install_round_index',
  'after_install_release_state', 'after_install_experiment', 'after_remove_pending_release'
];
assert.equal(ROUND2_MATERIALIZATION_BOUNDARIES.length, 22);
assert.equal(new Set(ROUND2_MATERIALIZATION_BOUNDARIES).size, 22);
assert.deepEqual([...ROUND2_MATERIALIZATION_BOUNDARIES], EXPECTED_MATERIALIZATION_BOUNDARIES);
const {pending, candidate} = validateRound2PendingRelease(root, repo);
assert.equal(pending.predecessor_release_sha256, ROUND2_PREDECESSOR);
assert.deepEqual(ROUND2_DECISIONS.map(item => [item.neutral_id, item.rejected_revision_id, item.replacement_revision_id, item.reserve_rank, item.skipped_incompatible_reserves.length]), [
  ['V4-D-D05','a75b87d16d74dd486b47c31f243306721f640023ad5d8fa9d3708d9e60ad7548','5c600589afed143e424216c060b1c3783e61566739dc61a56f220a702d452621',6,0],
  ['V4-C-D06','358d6a470b17724efda25d94a4e2a94359995915995cdc9715db603e86711614','a221c30995cab3709354ed6934c0fcbe2fdfa7ec420af228d46e5e600ff930e8',7,0]
]);
const derived = deriveRound2Fixture(root);
assert.equal(derived.expectedHashes.active_frame_sha256, ROUND2_EXPECTED_CORE_HASHES.active_frame_sha256);
assert.equal(derived.expectedHashes.lineage_sha256, ROUND2_EXPECTED_CORE_HASHES.lineage_sha256);
assert.equal(derived.expectedHashes.reserve_state_sha256, ROUND2_EXPECTED_CORE_HASHES.reserve_state_sha256);
assert.equal(derived.documents['ACTIVE-FRAME.json'].items.length, 64);
assert.equal(derived.documents['LINEAGE.json'].items.reduce((sum, item) => sum + item.edges.length, 0), 12);
assert.equal(derived.documents['RESERVE-STATE.json'].remaining_reserve_rows, 299);
assert.equal(derived.documents['RESERVE-STATE.json'].remaining_narrative_reserve_rows, 73);
assert.equal(derived.documents['RESERVE-STATE.json'].consumed_revision_ids.length, 12);
assert.equal(derived.documents['RESERVE-STATE.json'].banned_revision_ids.length, 12);
assert.equal(fs.existsSync(path.join(root, 'rounds/ROUND-0002/RELEASE.json')), false);
assert.equal(fs.existsSync(path.join(root, 'rounds/ROUND-0003')), false);
assert.deepEqual(ROUND2_RELEASE_EXCLUSIONS.map(item => item.path).sort(), [ROUND2_RELEASE_PATHS.gate, ROUND2_RELEASE_PATHS.normal, ROUND2_RELEASE_PATHS.senior, ROUND2_RELEASE_PATHS.manifest, '.ai/task/research-gemini-context-counterexample-reviewer-v5/STATE.json', ...Object.values(ROUND2_RELEASE_RECEIPT_PATHS), ...Object.values(ROUND2_RELEASE_HISTORY_PATHS)].sort());
const review = evaluateRound2ReleaseReviewGate(repo); assert.equal(review.satisfied, false); assert.equal(review.invalid, false);
function makeTransactionRepo(cycle = '001') {
  const transactionRepo = fs.mkdtempSync(path.join('/tmp', 'v5-round2-atomic-materializer-'));
  fs.mkdirSync(path.join(transactionRepo, path.dirname(ROUND2_RELEASE_PATHS.pending)), {recursive:true});
  fs.mkdirSync(path.join(transactionRepo, path.dirname(ROUND2_RELEASE_PATHS.manifest)), {recursive:true});
  fs.cpSync(root, path.join(transactionRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5'), {recursive:true});
  fs.cpSync(path.join(repo, '.ai/task/research-gemini-context-counterexample-reviewer-v5'), path.join(transactionRepo, '.ai/task/research-gemini-context-counterexample-reviewer-v5'), {recursive:true});
  const normalValue={schema_version:'gemini-context-v5-round-0002-release-review-v2',review_id:`V5-ROUND-0002-RELEASE-NORMAL-REVIEW-${cycle}`,round_id:'ROUND-0002',role:'REVIEWER',agent_id:'11111111-1111-4111-8111-111111111111',route:'Codex gpt-5.6-sol xhigh',status:'PASS',candidate_ref:candidate.candidate_ref,candidate_manifest_path:ROUND2_RELEASE_PATHS.manifest,candidate_manifest_sha256:candidate.manifest_sha256,dispatch_id:`UNVERIFIED-FIXTURE-DISPATCH-NORMAL-${cycle}`,completion_receipt_path:ROUND2_RELEASE_RECEIPT_PATHS.normal_completion,response_sha256:'',findings:[],repository_modified_by_review:false,recorded_at:'2026-08-31T08:00:00Z',provenance:'UNVERIFIED_FIXTURE_ONLY'};
  const seniorValue={...normalValue,review_id:`V5-ROUND-0002-RELEASE-SENIOR-REVIEW-${cycle}`,role:'SENIOR_REVIEWER',agent_id:'22222222-2222-4222-8222-222222222222',route:'Gemini 3.7 Flash high',dispatch_id:`UNVERIFIED-FIXTURE-DISPATCH-SENIOR-${cycle}`,completion_receipt_path:ROUND2_RELEASE_RECEIPT_PATHS.senior_completion};
  const receipt=(kind,value)=>{const dispatch={schema_version:'gemini-context-v5-round-0002-release-review-dispatch-receipt-v1',receipt_id:`UNVERIFIED-FIXTURE-${kind}-DISPATCH-${cycle}`,round_id:'ROUND-0002',role:value.role,agent_id:value.agent_id,route:value.route,dispatch_id:value.dispatch_id,candidate_ref:candidate.candidate_ref,candidate_manifest_path:ROUND2_RELEASE_PATHS.manifest,candidate_manifest_sha256:candidate.manifest_sha256,status:'DISPATCHED',agent_created_at:'2026-08-31T07:54:00Z',dispatched_at:'2026-08-31T07:55:00Z',orchestrator_authorization_scope:{production_materialization:false,derived_state_mutation:false,round_0003:false},expected_permitted_read_only_task:'READ_ONLY_REVIEW_OF_ROUND_0002_RELEASE_IMPLEMENTATION_CANDIDATE',completion_absent:true,opus_quota_override:false,provenance:'UNVERIFIED_FIXTURE_ONLY'};const text=`UNVERIFIED_FIXTURE_ONLY ${kind}`;return {dispatch,completion:{schema_version:'gemini-context-v5-round-0002-release-review-completion-receipt-v1',receipt_id:`V5-ROUND-0002-RELEASE-${kind}-COMPLETION-RECEIPT-${cycle}`,round_id:'ROUND-0002',role:value.role,agent_id:value.agent_id,route:value.route,dispatch_id:value.dispatch_id,dispatch_receipt_path:ROUND2_RELEASE_RECEIPT_PATHS[`${kind.toLowerCase()}_dispatch`],dispatch_receipt_sha256:sha256(jsonBytes(dispatch)),candidate_ref:candidate.candidate_ref,candidate_manifest_path:ROUND2_RELEASE_PATHS.manifest,candidate_manifest_sha256:candidate.manifest_sha256,status:'COMPLETED_NON_ERRORED',completed_at:'2026-08-31T08:05:00Z',response_sha256:sha256(Buffer.from(text)),verdict:'PASS',response_text:text,provenance:'UNVERIFIED_FIXTURE_ONLY'}}};
  const normalPair=receipt('NORMAL',normalValue),seniorPair=receipt('SENIOR',seniorValue),normalBytes=jsonBytes({...normalValue,response_sha256:normalPair.completion.response_sha256}),seniorBytes=jsonBytes({...seniorValue,response_sha256:seniorPair.completion.response_sha256});
  for(const [kind,pair] of [['normal',normalPair],['senior',seniorPair]]){fs.writeFileSync(path.join(transactionRepo,ROUND2_RELEASE_RECEIPT_PATHS[`${kind}_dispatch`]),jsonBytes(pair.dispatch));fs.writeFileSync(path.join(transactionRepo,ROUND2_RELEASE_RECEIPT_PATHS[`${kind}_completion`]),jsonBytes(pair.completion));}
  fs.writeFileSync(path.join(transactionRepo,ROUND2_RELEASE_PATHS.normal),normalBytes);fs.writeFileSync(path.join(transactionRepo,ROUND2_RELEASE_PATHS.senior),seniorBytes);
  const ref=(relative,bytes,value)=>({path:relative,sha256:sha256(bytes),agent_id:value.agent_id,role:value.role,route:value.route,status:'PASS',completion_verdict:'PASS',dispatch_id:value.dispatch_id,cycle,response_sha256:value.response_sha256});
  const gate={schema_version:'gemini-context-v5-round-0002-release-review-gate-v1',gate_id:'V5-ROUND-0002-RELEASE-DUAL-PASS-GATE-001',round_id:'ROUND-0002',status:'SATISFIED_FINAL_DUAL_PASS',candidate_ref:candidate.candidate_ref,candidate_manifest_path:ROUND2_RELEASE_PATHS.manifest,candidate_manifest_sha256:candidate.manifest_sha256,normal_review:ref(ROUND2_RELEASE_PATHS.normal,normalBytes,{...normalValue,response_sha256:normalPair.completion.response_sha256}),senior_review:ref(ROUND2_RELEASE_PATHS.senior,seniorBytes,{...seniorValue,response_sha256:seniorPair.completion.response_sha256}),permitted_action:'GO_ROUND_0002_RELEASE_ATOMIC_MATERIALIZATION_ONLY',forbidden_scope:['ROUND_0003','MODEL_CALL','NETWORK_CALL','GIT_STAGE','GIT_HISTORY'],recorded_at:'2026-08-31T08:00:00Z',provenance:'UNVERIFIED_FIXTURE_ONLY'};
  fs.writeFileSync(path.join(transactionRepo,ROUND2_RELEASE_PATHS.gate),jsonBytes(gate));
  return transactionRepo;
}

function assertPendingReviewLifecycle() {
  const lifecycleRepo = makeTransactionRepo();
  const lifecycleRoot = path.join(lifecycleRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
  try {
    for (const relative of [ROUND2_RELEASE_PATHS.normal, ROUND2_RELEASE_PATHS.senior, ROUND2_RELEASE_PATHS.gate]) fs.rmSync(path.join(lifecycleRepo, relative));
    let result = runPreflight(lifecycleRoot);
    assert.equal(result.decision, 'NO_GO_ROUND_0002_RELEASE_REVIEW_INVALID');
    assert.equal(result.static_integrity, 'FAIL_CLOSED');
    assert.match(result.reason, /FIXTURE_NOT_ALLOWED/u);
  } finally { fs.rmSync(lifecycleRepo, {recursive:true, force:true}); }
}

assertPendingReviewLifecycle();

function assertCycleRollover() {
  const rolloverRepo = makeTransactionRepo('003');
  try {
    const before = validateRound2PendingRelease(root, rolloverRepo).candidate;
    const rolloverRoot = path.join(rolloverRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
    const after = validateRound2PendingRelease(root, rolloverRepo).candidate;
    assert.deepEqual(after, before);
    const good = evaluateRound2ReleaseReviewGate(rolloverRepo, {allowUnverifiedFixture:true});
    assert.equal(good.satisfied, true);
    assert.equal(good.provenance.normal.dispatch_id.endsWith('-003'), true);
    assert.equal(good.provenance.senior.dispatch_id.endsWith('-003'), true);
    const seniorDispatchPath = path.join(rolloverRepo, ROUND2_RELEASE_RECEIPT_PATHS.senior_dispatch);
    const seniorDispatch = JSON.parse(fs.readFileSync(seniorDispatchPath));
    seniorDispatch.dispatch_id = seniorDispatch.dispatch_id.replace(/-003$/u, '-002');
    fs.writeFileSync(seniorDispatchPath, jsonBytes(seniorDispatch));
    const mixed = evaluateRound2ReleaseReviewGate(rolloverRepo, {allowUnverifiedFixture:true});
    assert.equal(mixed.invalid, true);
    assert.match(mixed.reason, /CYCLE|BINDING/u);
    assert.deepEqual(validateRound2PendingRelease(root, rolloverRepo).candidate, before);
    assert.equal(fs.existsSync(path.join(rolloverRoot, 'rounds/ROUND-0002/RELEASE.json')), false);
  } finally { fs.rmSync(rolloverRepo, {recursive:true, force:true}); }
}

assertCycleRollover();

function assertCompletedNegativeMatrix(completedRepo) {
  const packageRoot = path.join(completedRepo, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
  const evidenceTargets = [
    ['normal_dispatch', ROUND2_RELEASE_RECEIPT_PATHS.normal_dispatch, 'status'],
    ['senior_dispatch', ROUND2_RELEASE_RECEIPT_PATHS.senior_dispatch, 'status'],
    ['normal_completion', ROUND2_RELEASE_RECEIPT_PATHS.normal_completion, 'verdict'],
    ['senior_completion', ROUND2_RELEASE_RECEIPT_PATHS.senior_completion, 'verdict'],
    ['normal_review', ROUND2_RELEASE_PATHS.normal, 'status'],
    ['senior_review', ROUND2_RELEASE_PATHS.senior, 'status'],
    ['gate', ROUND2_RELEASE_PATHS.gate, 'status']
  ];
  const hashFields = {
    normal_dispatch: 'candidate_manifest_sha256', senior_dispatch: 'candidate_manifest_sha256',
    normal_completion: 'response_sha256', senior_completion: 'response_sha256',
    normal_review: 'response_sha256', senior_review: 'response_sha256', gate: 'candidate_manifest_sha256'
  };
  const candidateFields = new Set(evidenceTargets.map(([label]) => label));
  const negativeCases = [];
  for (const [label, relative, verdictField] of evidenceTargets) {
    negativeCases.push({label, kind: 'delete', relative});
    negativeCases.push({label, kind: 'byte_tamper', relative});
    negativeCases.push({label, kind: 'hash_mismatch', relative, field: hashFields[label]});
    negativeCases.push({label, kind: 'verdict_or_status_mismatch', relative, field: verdictField});
    if (!candidateFields.has(label)) throw Error('ROUND2_NEGATIVE_MATRIX_TARGET_MISSING');
    negativeCases.push({label, kind: 'candidate_mismatch', relative, field: 'candidate_ref'});
  }
  const transitionTargets = [
    ROUND2_RELEASE_PATHS.release,
    ...['ACTIVE-FRAME.json', 'LINEAGE.json', 'RESERVE-STATE.json', 'ROUND-INDEX.json', 'RELEASE-STATE.json', 'EXPERIMENT.json'].map(name => path.join(path.relative(completedRepo, packageRoot), name))
  ];
  for (const relative of transitionTargets) {
    negativeCases.push({label: relative, kind: 'transition_delete', relative});
    negativeCases.push({label: relative, kind: 'transition_tamper', relative});
    negativeCases.push({label: relative, kind: 'transition_wrong_hash', relative});
  }
  const candidateManifest = JSON.parse(fs.readFileSync(path.join(completedRepo, ROUND2_RELEASE_PATHS.manifest)));
  const candidateCode = candidateManifest.files.find(item => item.path.endsWith('/round-0002-release.mjs'))?.path;
  if (!candidateCode) throw Error('ROUND2_NEGATIVE_MATRIX_CANDIDATE_CODE_MISSING');
  negativeCases.push({label: candidateCode, kind: 'candidate_covered_delete', relative: candidateCode});
  negativeCases.push({label: candidateCode, kind: 'candidate_covered_tamper', relative: candidateCode});
  const expectedCount = 7 * 5 + 7 * 3 + 2;
  assert.equal(negativeCases.length, expectedCount);
  const observed = [];
  for (const testCase of negativeCases) {
    const clone = fs.mkdtempSync(path.join('/tmp', 'v5-round2-completed-negative-'));
    try {
      fs.cpSync(completedRepo, clone, {recursive: true, force: true});
      const file = path.join(clone, testCase.relative);
      if (testCase.kind.endsWith('delete')) fs.rmSync(file);
      else if (testCase.kind === 'byte_tamper' || testCase.kind === 'transition_tamper' || testCase.kind === 'transition_wrong_hash' || testCase.kind === 'candidate_covered_tamper') fs.appendFileSync(file, '\n');
      else {
        const value = JSON.parse(fs.readFileSync(file));
        if (testCase.kind === 'candidate_mismatch') value.candidate_ref = '0'.repeat(64);
        else if (testCase.kind === 'hash_mismatch') value[testCase.field] = 'f'.repeat(64);
        else value[testCase.field] = testCase.field === 'verdict' ? 'CHANGES_REQUIRED' : 'INVALID';
        fs.writeFileSync(file, jsonBytes(value));
      }
      const cloneRoot = path.join(clone, 'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
      assert.throws(() => checkReplay(cloneRoot, {allowUnverifiedFixture:true}), `${testCase.label}:${testCase.kind}:replay`);
      const preflight = runPreflight(cloneRoot, {allowUnverifiedFixture:true});
      assert.equal(preflight.static_integrity, 'FAIL_CLOSED', `${testCase.label}:${testCase.kind}:preflight`);
      assert.match(preflight.decision, /^NO_GO_/u, `${testCase.label}:${testCase.kind}:decision`);
      observed.push(`${testCase.label}:${testCase.kind}`);
    } finally { fs.rmSync(clone, {recursive:true, force:true}); }
  }
  assert.deepEqual(observed, negativeCases.map(item => `${item.label}:${item.kind}`));
  return {expected: expectedCount, observed: observed.length, cases: observed};
}

const originalNames=['ACTIVE-FRAME.json','LINEAGE.json','RESERVE-STATE.json','ROUND-INDEX.json','RELEASE-STATE.json','EXPERIMENT.json','PENDING-RELEASE.json'];
for (const boundary of ROUND2_MATERIALIZATION_BOUNDARIES) {
  const failureRepo=makeTransactionRepo(),failureRoot=path.join(failureRepo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
  try {
    const before=Object.fromEntries(originalNames.map(name=>[name,fs.readFileSync(path.join(failureRoot,name))]));
    assert.throws(()=>materializeRound2Release(failureRepo,{fail_after:boundary,allow_unverified_fixture:true}),new RegExp(`ROUND2_MATERIALIZATION_INJECTED_FAILURE:${boundary}`));
    for(const [name,bytes] of Object.entries(before))assert.equal(fs.readFileSync(path.join(failureRoot,name)).equals(bytes),true,`${boundary}:${name}`);
    assert.equal(fs.existsSync(path.join(failureRepo,ROUND2_RELEASE_PATHS.release)),false);
    assert.deepEqual(fs.readdirSync(failureRoot).filter(name=>name.startsWith('.round2-release-transaction-')),[]);
  } finally { fs.rmSync(failureRepo,{recursive:true,force:true}); }
}

const transactionRepo = makeTransactionRepo();
try {
  const normalReviewPath=path.join(transactionRepo,ROUND2_RELEASE_PATHS.normal), normalReviewBytes=fs.readFileSync(normalReviewPath), normalReviewValue=JSON.parse(normalReviewBytes); normalReviewValue.status='CHANGES_REQUIRED'; fs.writeFileSync(normalReviewPath,jsonBytes(normalReviewValue)); const negativeGate=evaluateRound2ReleaseReviewGate(transactionRepo,{allowUnverifiedFixture:true}); assert.equal(negativeGate.invalid,true); assert.equal(negativeGate.reason,'ROUND2_RELEASE_REPAIR_REQUIRED_REVIEW_VERDICT'); fs.writeFileSync(normalReviewPath,normalReviewBytes);
  const first=materializeRound2Release(transactionRepo,{allow_unverified_fixture:true}),second=materializeRound2Release(transactionRepo,{allow_unverified_fixture:true});
  assert.equal(first.status,'ROUND_0002_RELEASED_ROUND_0003_AUDIT_NOT_AUTHORIZED');assert.equal(second.status,'ALREADY_MATERIALIZED_IDEMPOTENT');
  assert.equal(fs.existsSync(path.join(transactionRepo,ROUND2_RELEASE_PATHS.pending)),false);assert.equal(fs.existsSync(path.join(transactionRepo,ROUND2_RELEASE_PATHS.release)),true);
  const transactionRoot=path.join(transactionRepo,'evidence/quality/model-probes/gemini-context-counterexample-reviewer-v5');
  assert.deepEqual(checkReplay(transactionRoot,{allowUnverifiedFixture:true}),{status:'PASS',completed_rounds:2,byte_identical_outputs:true});
  const completedPreflight=runPreflight(transactionRoot,{allowUnverifiedFixture:true});assert.equal(completedPreflight.decision,'NO_GO_ROUND_0003_AUDIT_NOT_AUTHORIZED');assert.equal(completedPreflight.static_integrity,'PASS');assert.equal(completedPreflight.completed_rounds,2);
  const completedNegatives = assertCompletedNegativeMatrix(transactionRepo);
  assert.equal(completedNegatives.expected, 58); assert.equal(completedNegatives.observed, 58);
} finally { fs.rmSync(transactionRepo,{recursive:true,force:true}); }
console.log(JSON.stringify({status:'PASS', candidate_ref:candidate.candidate_ref, manifest_sha256:candidate.manifest_sha256, file_count:candidate.file_count, expected_hashes:candidate.expected_hashes, observed_completed_replay:'PASS_FIXTURE_MODE', failure_injection_boundaries:ROUND2_MATERIALIZATION_BOUNDARIES, completed_negative_cases:58, tests:['exact two ordered mappings with no skips','OUT_OF_SCOPE_NON_PROSE replacement eligibility','all frozen ROUND2 audit hashes','post-state cardinalities and hashes','no real RELEASE or ROUND3','production rejects UNVERIFIED_FIXTURE_ONLY receipts','direct CHANGES_REQUIRED review verdict negative','-003 rollover GO and mixed-cycle rejection','rollback restores every original byte and PENDING at every atomic boundary','dual-pass atomic materializer and second-call idempotence','completed replay/preflight reject every external evidence deletion/hash/verdict/candidate mutation','completed replay/preflight reject candidate-covered code deletion/tamper and all seven transition-file deletion/tamper/wrong-hash cases']}, null, 2));
