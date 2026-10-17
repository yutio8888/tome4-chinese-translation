"""Round isolation, frozen v2 bytes, negative import and recovery contracts."""
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from tools.i18nlib import full_review as fr
import contextual_result_check as contextual
from tools.i18nlib import production_review_v2_lite as catalog
from orchestration.review_prompts import build_contextual_prompt


class FullRoundTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.directory = self.root / 'round'
        self.directory.mkdir()
        self.manifest = SimpleNamespace(root=self.root, raw_bytes=b'manifest')
        self.source = 'hello'
        row = {'component': 'engine', 'translation_path': 'engine.lua', 'document_ordinal': 0,
               'function_name': 't', 'section': 'engine/test.lua', 'source': 'hello', 'target': '你好',
               'source_tag': None, 'args_order': None, 'special': None, 'schema_version': 1}
        formal, _ = catalog.formal_rows([row], terminology='terms', sources={'engine': 'commit:' + 'a'*40})
        self.row = formal[0]
        self.unit = {'unit_id': self.row['logical_entry_identity'], 'revision_key': self.row['entry_revision_identity'],
                     'guard': 'g', 'occurrence': row, 'disposition': 'release-required',
                     'catalog_row': self.row, 'fixed_source_identity': 'commit:' + 'a'*40}
        self.key = self.unit['unit_id']
        self.ledger = {'round_id': 'test-round', 'manifest_sha256': fr.sha(b'manifest'),
                      'terminology_snapshot': 'terms', 'units': [self.unit], 'supplements': [{'pending': True}]}
        self.ledger['inventory_identity'] = fr.sha(fr.canonical(self.ledger))
        self.save(self.directory / 'inventory.json', self.ledger)
        (self.root / 'engine.lua').write_text('--------------------------------------------------\nsection "engine/test.lua"\nt("hello", "你好")\n', encoding='utf-8')
        self.workset = {'round_id': 'test-round', 'entries': [{'unit_id': self.key, 'context': 'neutral usage',
            'source_files': [{'component': 'engine', 'public_source_path': 'engine/test.lua', 'sha256': fr.sha(b'hello')}],
            'b_reasons': [], 'b_exemption': 'short interface label; no mechanics'}]}
        self.scope = {'schema_version': 1, 'allowed_files': ['engine.lua'], 'anchor_scopes': [
            {'file': 'engine.lua', 'section_path': 'engine/test.lua', 'ordered_titles': []}]}
        self.save(self.root / 'workset.json', self.workset)
        self.save(self.root / 'scope.json', self.scope)
        self.live_patch = patch.object(fr, 'current_units', return_value=([self.unit], 'unrelated-terms'))
        self.live_patch.start()
        self.addCleanup(self.live_patch.stop)
        self.source_patch = patch.object(fr, 'source_file', return_value={'content': 'hello', 'sha256': fr.sha(b'hello')})
        self.source_patch.start()
        self.addCleanup(self.source_patch.stop)

    def save(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(fr.canonical(value))

    def export(self, name='a', lane='A'):
        return fr.export(self.manifest, self.directory, [self.key], self.root / 'workset.json',
                         self.root / 'scope.json', export_id=name, lane=lane, task_id='task-one',
                         dispatch_id='d1', workspace_id='w1', parent_agent_id='parent')

    def producer(self, ref):
        self.binding = {'round_id': 'test-round', 'export_id': ref['export_id'],
            **ref['planned_producer'],
            'model': 'exact-model-a', 'input_sha256': ref['input_sha256']}
        self.raw = fr.canonical({'contract': 'translation_contextual_v2', 'candidate_identity': ref['candidate_identity'],
            'verdicts': [{'revision_key': self.unit['revision_key'], 'verdict': 'OK'}]})
        self.binding['raw_sha256'] = fr.sha(self.raw)
        self.save(self.root / 'binding.json', self.binding)
        (self.root / 'raw.json').write_bytes(self.raw)
        child = {**{k:ref['planned_producer'][k] for k in ('dispatch_id','workspace_id','parent_agent_id')},
                 'role': 'REVIEWER', 'purpose': 'translation_contextual_v2',
                 'archive_confirmed': True, 'lifecycle': 'archived', 'lineage_verified': True,
                 'output_valid': True, 'raw_output_sha256': fr.sha(self.raw), 'candidate_identity': ref['candidate_identity'],
                 'runtime_observation': {'model': {'presence': 'present', 'value': 'exact-model-a'}}}
        self.state = {'task_id': ref['planned_producer']['task_id'], 'mode': 'review_only', 'schema_version': 5,
            'workspace_id': 'w1', 'orchestrator_agent_id': 'parent', 'child_dispatches': [child]}
        self.state_path = self.root / '.ai/task' / ref['planned_producer']['task_id'] / 'STATE.json'
        self.save(self.state_path, self.state)
        (self.state_path.parent / 'SCOPE.json').write_bytes((self.root / 'scope.json').read_bytes())
        round_binding = {key: ref[key] for key in ('round_id','export_id','freeze_sha256','input_sha256')}
        (self.state_path.parent / 'SPEC.md').write_text('full_review_binding=' + fr.canonical(round_binding).decode(), encoding='utf-8')
        self.gate_fixture(ref)

    def gate_fixture(self, ref):
        """Controlled full-set receipt; commands simulated, validator remains real."""
        import shutil
        from tools.i18nlib import gate_results as gates
        self.save(self.state_path.parent/'BASELINE-MANIFEST.json', {'head':'a'*40})
        adapter = self.root/'tools/i18nlib/full_review.py'
        adapter.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(fr.__file__), adapter)
        selected = fr.gate_selection(self.manifest, ref)
        b = {'candidate':selected,'candidate_sha256':gates.digest(selected),
             'worktree_sha256':'b'*64,'tool_commit':'a'*40,'tool_version':'1.0.0',
             'runner_version':gates.VERSION,'python_version':'3.11.0',
             'config_sha256':'c'*64,'check_set_sha256':gates.digest(gates.checks()),'skip_build':False}
        def execute(argv, root, log):
            log.write_bytes(b'controlled receipt test; not production execution')
            return 0
        import contextlib, io
        with patch.object(gates,'binding',return_value=b), contextlib.redirect_stdout(io.StringIO()):
            result = gates.run(self.root,selected=selected,execute=execute)
        dest = self.root/'evidence/full-review/test-round/task-gates'/ref['planned_producer']['task_id']/ref['export_id']
        for record in result['checks']:
            path = dest/record['id']/'output.log'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes((self.root/record['log_path']).read_bytes())
        self.save(dest/'results.json',result)
        self.binding.update(gate_evidence_path=(dest/'results.json').relative_to(self.root).as_posix(),
                            gate_evidence_sha256=fr.sha((dest/'results.json').read_bytes()))
        self.save(self.root/'binding.json',self.binding)

    def real_done(self, ref, directory=None):
        import ai_state_check
        task_id = ref['planned_producer']['task_id']
        input_path = '.ai/task/' + task_id + '/CONTEXTUAL-ENVELOPE-final-full.json'
        raw_path = '.ai/reviews/' + task_id + '/raw-' + ref['planned_producer']['dispatch_id'] + '.txt'
        record_path = '.ai/reviews/' + task_id + '/review.json'
        self.save(self.root/input_path, fr.read((directory or self.directory)/'exports'/ref['export_id']/'input.json'))
        (self.root/raw_path).parent.mkdir(parents=True,exist_ok=True)
        (self.root/raw_path).write_bytes(self.raw)
        record = {'task_id':task_id,'review_contract':'translation_contextual_v2',
            'purpose':'translation_contextual_v2','review_kind':'full','review_phase':'REVIEW',
            'cycle':0,'attempt':1,'result':'PASS','reviewer_role':'REVIEWER',
            'agent_id':'controlled-fixture-reviewer', 'dispatch_id':ref['planned_producer']['dispatch_id'],
            'candidate_identity':ref['candidate_identity'],'input_path':input_path,
            'raw_output_path':raw_path,'raw_output_sha256':fr.sha(self.raw)}
        self.save(self.root/record_path,record)
        child = self.state['child_dispatches'][0]
        child['runtime_observation'].update(schema_version=1,source='live_agent_metadata',
            captured_at='controlled-fixture',capture_status='captured',
            provider={'presence':'missing'},mode={'presence':'missing'},thinking={'presence':'missing'})
        child.update(agent_id=record['agent_id'],input_path=input_path,
            labels={'task_id':task_id,'role':'reviewer','purpose':'translation_contextual_v2',
                'dispatch_id':child['dispatch_id'],'candidate_identity':ref['candidate_identity']})
        self.state.update(state='DONE', change_class='standard',cycle=0,max_cycles=3,
            review_contracts=['translation_contextual_v2'],pending_review_contracts=[],
            completed_review_contracts=['translation_contextual_v2'],open_accepted_findings=[],deferred_findings=[],
            review_records=[record_path],senior_review_records=[],
            contextual_reviewers=[{k:child[k] for k in ('role','purpose','candidate_identity','dispatch_id','input_path','agent_id')}])
        self.save(self.state_path,self.state)
        result = ai_state_check.check_state(self.state_path,workspace_root=self.root)
        self.assertEqual(result.outcome,'DONE_VERIFIED',result.detail)

    def test_real_done_predicate_plus_task_gate_receipt_and_tracked_replay(self):
        ref = self.export()
        self.producer(ref)
        self.real_done(ref)
        # No terminal predicate or receipt validator mocks. Only gate command outputs
        # are the explicitly controlled fixture generated by gate_fixture().
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        self.assertEqual(fr.check(self.manifest,self.directory)['A_validated_outputs'],1)
        import ai_state_check
        snapshot = self.directory/'imports/a/task-anchors'
        self.assertEqual(ai_state_check.check_state(snapshot/'.ai/task/task-one/STATE.json',
            workspace_root=snapshot).outcome,'DONE_VERIFIED')
        missing = dict(self.binding)
        del missing['gate_evidence_path']
        self.save(self.root/'missing.json',missing)
        with self.assertRaisesRegex(fr.FullReviewError,'task-specific'):
            fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'missing.json')
        receipt = self.root/self.binding['gate_evidence_path']
        original = fr.read(receipt)
        import copy
        for mutation in ('task','candidate','order','input','context','build','log'):
            changed = copy.deepcopy(original)
            if mutation == 'task': changed['binding']['candidate']['full_review_task']['task_id'] = 'other-task'
            if mutation == 'candidate': changed['binding']['candidate']['candidate_identity'] = '0'*64
            if mutation == 'order': changed['binding']['candidate']['ordered_revisions'] = []
            if mutation == 'input': changed['binding']['candidate']['input_sha256'] = '0'*64
            if mutation == 'context': changed['binding']['candidate']['workset_sha256'] = '0'*64
            if mutation == 'build': changed['checks'] = changed['checks'][:-1]
            if mutation == 'log': changed['checks'][0]['output_sha256'] = '0'*64
            self.save(receipt,changed)
            bad = dict(self.binding,gate_evidence_sha256=fr.sha(receipt.read_bytes()))
            with self.subTest(mutation=mutation), self.assertRaises(fr.FullReviewError):
                fr.producer(self.manifest,ref,bad,(self.directory/'exports/a/input.json').read_bytes(),self.raw)
            with self.subTest(historical_mutation=mutation), self.assertRaises(fr.FullReviewError):
                fr.producer(self.manifest,ref,bad,(self.directory/'exports/a/input.json').read_bytes(),self.raw,
                    accepted_selection=original['binding']['candidate'])
        self.save(receipt,original)
        self.state['child_dispatches'][0]['archive_confirmed'] = False
        self.save(self.state_path,self.state)
        with self.assertRaisesRegex(fr.FullReviewError,'DONE_VERIFIED'):
            fr.producer(self.manifest,ref,self.binding,(self.directory/'exports/a/input.json').read_bytes(),self.raw)

    def test_accepted_import_replays_frozen_gates_after_unrelated_tool_and_runner_change(self):
        ref = self.export(); self.producer(ref); self.real_done(ref)
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        (self.root/'tools/unrelated.py').write_text('unrelated = True\n')
        with patch.object(fr.gate_results,'VERSION','ci-gates-v999'), patch.object(
                fr.gate_results,'checks',return_value=[('new-definition',['new-command'])]):
            self.assertEqual(fr.check(self.manifest,self.directory)['A_validated_outputs'],1)
            self.export()  # export pre-check uses accepted history
            fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        # A partial import has no historical authority, even with all anchors present.
        (self.directory/'imports/a/receipt.json').unlink()
        with self.assertRaisesRegex(fr.FullReviewError,'gate candidate binding mismatch'):
            fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')

    def test_first_import_stale_execution_input_rejected(self):
        ref = self.export(); self.producer(ref); self.real_done(ref)
        (self.root/'tools/unrelated.py').write_text('unrelated = True\n')
        with self.assertRaisesRegex(fr.FullReviewError,'gate candidate binding mismatch'):
            fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        self.assertFalse((self.directory/'imports/a/receipt.json').exists())

    def test_accepted_history_rejects_identity_receipt_log_and_terminal_tampering(self):
        import copy
        ref = self.export(); self.producer(ref); self.real_done(ref)
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        path = self.directory/'imports/a/receipt.json'
        accepted = fr.read(path)
        for field in fr.gate_selection(self.manifest,ref,execution=False):
            changed = copy.deepcopy(accepted)
            changed['gate_selection'][field] = 'tampered'
            self.save(path,changed)
            with self.subTest(field=field), self.assertRaises(fr.FullReviewError):
                fr.check(self.manifest,self.directory)
        self.save(path,accepted)
        result_path = self.root/self.binding['gate_evidence_path']
        result = fr.read(result_path)
        log = result_path.parent/result['checks'][0]['id']/'output.log'
        before = log.read_bytes(); log.write_bytes(b'tampered log')
        with self.assertRaises(fr.FullReviewError): fr.check(self.manifest,self.directory)
        log.write_bytes(before)
        state = self.state_path.read_bytes(); self.state_path.write_bytes(state+b' ')
        with self.assertRaisesRegex(fr.FullReviewError,'terminal anchor drift'):
            fr.check(self.manifest,self.directory)
        self.state_path.write_bytes(state)
        changed = copy.deepcopy(accepted); changed['binding']['round_id'] = 'other-round'
        self.save(path,changed)
        with self.assertRaises(fr.FullReviewError): fr.check(self.manifest,self.directory)

    def test_task_gate_archival_entry_recovers_exact_run_and_rejects_other_export(self):
        import shutil
        directory = self.root/'evidence/full-review/test-round'
        directory.parent.mkdir(parents=True)
        shutil.move(self.directory,directory)
        self.directory = directory
        ref = self.export(); self.producer(ref); self.real_done(ref)
        original = dict(self.binding)
        results_path = self.root/self.binding['gate_evidence_path']
        result = fr.task_gates(self.manifest,directory,'a',results_path)
        self.assertEqual(result['gate_evidence_sha256'],original['gate_evidence_sha256'])
        fr.import_result(self.manifest,directory,'a',self.root/'raw.json',self.root/'binding.json')
        changed = fr.read(results_path)
        changed['binding']['candidate']['export_id'] = 'borrowed'
        self.save(self.root/'wrong-gates.json',changed)
        with self.assertRaises(fr.gate_results.GateError):
            fr.task_gates(self.manifest,directory,'a',self.root/'wrong-gates.json')

    def test_arbitrary_current_unit_exports_existing_seven_key_envelope(self):
        ref = self.export()
        envelope = fr.read(self.directory / 'exports/a/input.json')
        payload, _ = contextual.validate_envelope(envelope)
        self.assertEqual(set(payload), contextual.PAYLOAD_KEYS)
        self.assertEqual(payload['translation_snapshot'][0]['target'], '你好')
        self.assertLessEqual(len(build_contextual_prompt(ref['candidate_identity'], 'input.json').encode()), 800)
        self.assertEqual(self.export(), ref)

    def test_preflight_rejects_wrong_scope_and_no_freeze(self):
        self.scope['anchor_scopes'][0]['section_path'] = 'wrong.lua'
        self.save(self.root / 'scope.json', self.scope)
        with self.assertRaises(fr.FullReviewError):
            self.export()
        self.assertFalse((self.directory / 'exports').exists())

    def test_duplicate_selection_and_cross_round_rejected(self):
        with self.assertRaises(fr.FullReviewError):
            fr.export(self.manifest, self.directory, [self.key]*2, self.root/'workset.json', self.root/'scope.json', export_id='a', lane='A')
        self.workset['round_id'] = 'old-round'
        self.save(self.root/'workset.json', self.workset)
        with self.assertRaises(fr.FullReviewError):
            self.export()

    def test_special_guard_drift_rejects_and_terminology_does_not(self):
        self.assertEqual(fr.validate_current(self.manifest, self.ledger)[self.key]['revision_key'], self.unit['revision_key'])
        self.ledger['units'][0] = dict(self.unit, guard='old-special')
        with self.assertRaises(fr.FullReviewError):
            fr.validate_current(self.manifest, self.ledger)

    def test_import_recovery_is_idempotent_and_not_effective_coverage(self):
        ref = self.export()
        self.producer(ref)
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            first = fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
            # Orphan raw after interruption is accepted only when exact bytes match.
            (self.directory/'imports/a/receipt.json').unlink()
            self.assertEqual(first, fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json'))
            self.assertEqual(first, fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json'))
            progress = fr.check(self.manifest, self.directory)
            self.assertEqual(progress['A_validated_outputs'], 1)
            self.assertEqual(progress['A_effective_complete'], 0)
            self.assertFalse(progress['denominator_frozen'])
            with self.assertRaises(fr.FullReviewError):
                fr.check(self.manifest, self.directory, require_complete=True)

    def test_unarchived_unknown_model_and_no_done_fail_closed(self):
        ref = self.export()
        self.producer(ref)
        for mutation in ['archive', 'model', 'done']:
            self.producer(ref)
            if mutation == 'archive':
                self.state['child_dispatches'][0]['archive_confirmed'] = False
            if mutation == 'model':
                self.state['child_dispatches'][0]['runtime_observation']['model'] = {'presence': 'missing'}
            self.save(self.state_path, self.state)
            with patch.object(fr.batch, '_contextual_done_verified', return_value=mutation != 'done'):
                with self.assertRaises(fr.FullReviewError):
                    fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
            self.assertFalse((self.directory/'imports/a/receipt.json').exists())

    def test_partial_wrong_hash_conflicting_raw_and_input_drift_fail(self):
        ref = self.export()
        self.producer(ref)
        self.binding['raw_sha256'] = '0'*64
        self.save(self.root/'binding.json', self.binding)
        with self.assertRaises(fr.FullReviewError):
            fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        self.producer(ref)
        value = json.loads(self.raw)
        value['verdicts'] = []
        raw = fr.canonical(value)
        (self.root/'raw.json').write_bytes(raw)
        self.binding['raw_sha256'] = fr.sha(raw)
        self.save(self.root/'binding.json', self.binding)
        with self.assertRaises(contextual.ContractError):
            fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        self.producer(ref)
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
            (self.directory/'imports/a/raw.json').write_bytes(b'conflict')
            with self.assertRaises(fr.FullReviewError):
                fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        (self.directory/'exports/a/input.json').write_bytes(b'{}')
        with self.assertRaises(fr.FullReviewError):
            fr.check(self.manifest, self.directory)

    def test_old_task_spec_cannot_be_borrowed_even_with_same_candidate_bytes(self):
        ref = self.export()
        self.producer(ref)
        old = {key: ref[key] for key in ('round_id', 'export_id', 'freeze_sha256', 'input_sha256')}
        old['round_id'] = 'old-round'
        (self.state_path.parent / 'SPEC.md').write_text('full_review_binding=' + fr.canonical(old).decode(), encoding='utf-8')
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            with self.assertRaises(fr.FullReviewError):
                fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        self.assertFalse((self.directory/'imports/a/receipt.json').exists())

    def test_prepared_input_drift_is_checked_before_any_results_exist(self):
        self.export()
        (self.directory/'exports/a/input.json').write_bytes(b'{}')
        with self.assertRaises(fr.FullReviewError):
            fr.check(self.manifest, self.directory)

    def test_opposite_frozen_lane_rejects_context_and_source_files_both_orders(self):
        import copy
        for first, second in [('A','B'),('B','A')]:
            for field in ('context','source_files'):
                with self.subTest(first=first,field=field):
                    self.directory = self.root/(first+field)
                    self.directory.mkdir()
                    self.save(self.directory/'inventory.json',self.ledger)
                    entry = copy.deepcopy(self.workset)
                    entry['entries'][0]['b_reasons'] = ['mechanics']
                    self.save(self.root/'workset.json',entry)
                    self.export('first',first)
                    if field == 'context': entry['entries'][0][field] = 'another usage'
                    else: entry['entries'][0][field][0]['line_end'] = 1
                    self.save(self.root/'workset.json',entry)
                    with self.assertRaisesRegex(fr.FullReviewError,'neutral source/context'):
                        self.export('second',second)
                    self.assertFalse((self.directory/'imports').exists())

    def test_frozen_b_policy_cannot_shrink_before_import(self):
        self.workset['entries'][0]['b_reasons'] = ['mechanics','long-text']
        self.save(self.root/'workset.json',self.workset)
        self.export()
        self.workset['entries'][0]['b_reasons'] = ['mechanics']
        self.save(self.root/'workset.json',self.workset)
        with self.assertRaisesRegex(fr.FullReviewError,'applicability cannot shrink'):
            self.export('b','B')

    def test_host_closure_conserves_real_lua_keys_and_separates_release_readiness(self):
        # A one-key synthetic host fixture, parsed by the actual Lua bridge.
        # This proves the closure consumer, never production review completion.
        from tools.i18nlib import release_candidate as rc
        from tools.i18nlib.config import load_manifest
        from tools.i18nlib.locale_model import LocaleLoader
        from tools.i18nlib.runtime import LuaRuntime
        import zipfile
        candidate = self.root/'.artifacts/i18n/release-candidate/closure-test'
        engine = candidate/'engine'/rc.ENGINE_LOCALE
        engine.parent.mkdir(parents=True)
        engine.write_bytes(b't("hello", "' + '你好'.encode() + b'")\n')
        (candidate/'addon').mkdir()
        later = candidate/'addon/late.lua'
        later.write_bytes(b't("hello", "' + '你好'.encode() + b'", "some-tag")\n')
        engine.write_bytes(b't("hello", "early")\n')
        (candidate/'addon/init.lua').write_bytes(b'for_module="tome"\nshort_name="test"\n')
        with zipfile.ZipFile(candidate/'tome-test.teaa', 'w', compression=zipfile.ZIP_STORED) as package:
            package.writestr('init.lua', (candidate/'addon/init.lua').read_bytes())
            package.writestr('late.lua', later.read_bytes())
        seal = {'files': rc.file_manifest(candidate), 'engine_build_sha256': fr.sha(engine.read_bytes()),
                'package': 'tome-test.teaa', 'input_hashes': {}}
        self.save(candidate/'candidate.json', seal)
        proof = self.root/'evidence/closure-test.txt'
        proof.parent.mkdir(exist_ok=True)
        proof.write_bytes(b'Host fixture source/runtime and exclusion evidence')
        evidence = [{'path':'evidence/closure-test.txt','sha256':fr.sha(proof.read_bytes())}]
        unit = dict(self.unit, runtime_key=['hello', None])
        supplement = {'supplement_id':'one-source-occurrence', 'kind':'source-visible', 'component':'engine',
                      'record':{'source':'hello','source_tag':None}}
        ledger = dict(self.ledger, supplements=[supplement])
        closure = {'round_id':'test-round', 'inventory_sha256':fr.sha((self.directory/'inventory.json').read_bytes()),
            'candidate_path':str(candidate),'candidate_sha256':fr.sha((candidate/'candidate.json').read_bytes()),
            'evidence':evidence, 'runtime_semantics':fr.I18N_SOURCE,
            'runtime_keys':[{'key':['hello',None], 'layers':[{'origin':'candidate','path':'engine/'+rc.ENGINE_LOCALE,
                'sha256':fr.sha(engine.read_bytes()),'layer':'Engine-full','language':'zh_hans'},
                {'origin':'candidate','path':'addon/late.lua','sha256':fr.sha(later.read_bytes()),
                 'layer':'addon-late','language':'zh_hans'}],
                'query':{'source':'hello','tag':None,'method':'_t'},
                'effective_registration':{'layer':'addon-late','ordinal':1,'line':1,'source_tag':'some-tag'},
                'effective_layer':'addon-late','target':'你好','args_order':None,'special':None}],
            'occurrences':[{'unit_id':self.key,'revision_key':unit['revision_key'],'guard':unit['guard'],
                'disposition':'release-required','runtime_key':['hello',None],'effective_target':'你好','evidence':evidence}],
            'supplements':[{'supplement_id':supplement['supplement_id'],'supplement_sha256':fr.sha(fr.canonical(supplement)),
                'disposition':'release-required','runtime_key':['hello',None],'review_units':[self.key],'evidence':evidence}],
            'release_readiness':{'engine_actual_loading':'untested','game_launch':'untested'}}
        for field in ('retained_layers','dynamic_contexts','relations','successors'):
            closure[field] = {'status':'closed','evidence':evidence}
        self.save(self.directory/'closure.json', closure)
        runtime = LuaRuntime(load_manifest())
        with patch.object(rc,'input_hashes',return_value={}), patch.object(fr,'LuaRuntime',return_value=runtime):
            result = fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},{'A':{self.key},'B':set()})
            self.assertEqual(result['final_runtime_denominator'], 1)
            self.assertFalse(result['release_ready'])
            import copy
            official_bytes = b't("hello", "early")\n'
            official_record = LocaleLoader(runtime).load_bytes(official_bytes,logical_path='fixture-official.lua').translations[0]
            official = {'supplement_id':'one-source-occurrence','kind':'official-inheritance','component':'engine',
                'record':official_record,'commit':fr.I18N_SOURCE['commit'],'public_source_path':'fixture-official.lua',
                'sha256':fr.sha(official_bytes)}
            official_ledger = dict(ledger,supplements=[official])
            official_closure = copy.deepcopy(closure)
            official_closure['runtime_keys'][0]['layers'][0].update(origin='official',path='fixture-official.lua',
                repository='engine',commit=fr.I18N_SOURCE['commit'])
            mapping = official_closure['supplements'][0]
            mapping.update(supplement_sha256=fr.sha(fr.canonical(official)),disposition='shadowed',
                reason='controlled official first registration shadowed by later reviewed candidate',source_verified=True,
                shadowed_registration={'layer':'Engine-full','ordinal':1,'line':1,'source_tag':None})
            real_manifest = load_manifest()
            self.manifest.repositories = real_manifest.repositories
            self.manifest.repository_path = real_manifest.repository_path
            pinned = fr.FixedReader.pinned
            def fixture_official(reader, repository, commit, path):
                if path == 'fixture-official.lua': return official_bytes, {}
                return pinned(reader,repository,commit,path)
            self.save(self.directory/'closure.json',official_closure)
            with patch.object(fr.FixedReader,'pinned',fixture_official):
                self.assertEqual(fr.closure_check(self.manifest,self.directory,official_ledger,{self.key:unit},
                    {'A':{self.key},'B':set()})['final_runtime_denominator'],1)
                mapping.update(disposition='loading-only')
                self.save(self.directory/'closure.json',official_closure)
                with self.assertRaisesRegex(fr.FullReviewError,'non-Boot official language'):
                    fr.closure_check(self.manifest,self.directory,official_ledger,{self.key:unit},{'A':{self.key},'B':set()})
            excluded = copy.deepcopy(closure)
            excluded['supplements'][0].update(disposition='unreachable',source_verified=True,
                reason='controlled source proof for supplementary unreachable occurrence')
            self.save(self.directory/'closure.json',excluded)
            with self.assertRaisesRegex(fr.FullReviewError,'concrete source proof'):
                fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},{'A':{self.key},'B':set()})
            excluded['supplements'][0]['source_proof'] = [dict(self.workset['entries'][0]['source_files'][0],
                line_start=1,line_end=1)]
            self.save(self.directory/'closure.json',excluded)
            self.assertEqual(fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},
                {'A':{self.key},'B':set()})['final_runtime_denominator'],1)
            for component, kind in (('engine','official-inheritance'), ('tome','copy'),
                                    ('release-addon','retained-layer'), ('boot','official-inheritance'),
                                    ('outside','retained-layer')):
                outside = dict(supplement, component=component, kind=kind)
                case = copy.deepcopy(excluded)
                case['supplements'][0].update(disposition='outside-release-followup',
                    supplement_sha256=fr.sha(fr.canonical(outside)))
                self.save(self.directory/'closure.json',case)
                with self.subTest(component=component,kind=kind), self.assertRaisesRegex(
                        fr.FullReviewError,'requires an outside-release'):
                    fr.closure_check(self.manifest,self.directory,dict(ledger,supplements=[outside]),
                        {self.key:unit},{'A':{self.key},'B':set()})
            for component, kind, fate in (('outside','source-visible','outside-release-followup'),
                                           ('boot','official-inheritance','loading-only'),
                                           ('tome','copy','loading-only'),
                                           ('release-addon','retained-layer','loading-only'),
                                           ('ashes-urhrok','wrapper-addon','loading-only')):
                outside = dict(supplement, component=component, kind=kind)
                if kind in {'copy', 'retained-layer'}:
                    raw = (Path(fr.__file__).resolve().parents[2]/'engine.copy.lua').read_bytes()
                    (self.root/'engine.copy.lua').write_bytes(raw)
                    outside.update(path='engine.copy.lua',content=raw.decode(),sha256=fr.sha(raw))
                    if kind == 'retained-layer':
                        outside.update(commit=self.manifest.repositories['addon'].commit)
                wrapper_spec = None
                if kind == 'wrapper-addon':
                    inner = self.root/'tome-ashes-urhrok'
                    inner.mkdir(exist_ok=True)
                    raw = b'forceFontPackage("chinese")\n'
                    (inner/'wrapper.lua').write_bytes(raw)
                    outside.update(path=inner.name+'/wrapper.lua',sha256=fr.sha(raw))
                    self.manifest.component = lambda _:SimpleNamespace(source_repository=None,
                        protected_source=SimpleNamespace(visibility='public',mount=inner.name))
                    wrapper_spec = dict(component=component,public_source_path=outside['path'],
                        sha256=fr.sha(raw),inner_root=str(inner))
                case = copy.deepcopy(excluded)
                case['supplements'][0].update(disposition=fate,language_literals=[],
                    supplement_sha256=fr.sha(fr.canonical(outside)))
                if wrapper_spec:
                    case['supplements'][0]['source_file'] = wrapper_spec
                self.save(self.directory/'closure.json',case)
                def retained_bytes(reader, repository, commit, path):
                    if path == 'engine.copy.lua': return raw, {}
                    return pinned(reader,repository,commit,path)
                if wrapper_spec: self.source_patch.stop()
                with patch.object(fr.FixedReader,'pinned',retained_bytes) if kind == 'retained-layer' else __import__('contextlib').nullcontext():
                    self.assertEqual(fr.closure_check(self.manifest,self.directory,dict(ledger,supplements=[outside]),
                        {self.key:unit},{'A':{self.key},'B':set()})['final_runtime_denominator'],1)
                if wrapper_spec: self.source_patch.start()
            # Actual randart copy bytes cannot be waived by a declared empty list.
            raw = (Path(fr.__file__).resolve().parents[2]/'mod-tome.copy.lua').read_bytes()
            (self.root/'mod-tome.copy.lua').write_bytes(raw)
            actual = dict(supplement,kind='copy',component='tome',path='mod-tome.copy.lua',
                content=raw.decode(),sha256=fr.sha(raw))
            case = copy.deepcopy(excluded)
            case['supplements'][0].update(disposition='loading-only',language_literals=[],
                supplement_sha256=fr.sha(fr.canonical(actual)))
            self.save(self.directory/'closure.json',case)
            with self.assertRaisesRegex(fr.FullReviewError,'actual language literals'):
                fr.closure_check(self.manifest,self.directory,dict(ledger,supplements=[actual]),
                    {self.key:unit},{'A':{self.key},'B':set()})
            self.save(self.directory/'closure.json',closure)
            for mutation in ('missing-supplement', 'wrong-effective-text', 'duplicate-key',
                             'wrong-args', 'wrong-special', 'wrong-layer', 'wrong-registration',
                             'wrong-pin', 'missing-query', 'wrong-chain', 'wrong-query-tag', 'wrong-query-method'):
                import copy
                wrong = copy.deepcopy(closure)
                if mutation == 'missing-supplement': wrong['supplements'] = []
                if mutation == 'wrong-effective-text': wrong['runtime_keys'][0]['target'] = '错误'
                if mutation == 'duplicate-key': wrong['runtime_keys'].append(wrong['runtime_keys'][0])
                if mutation == 'wrong-args': wrong['runtime_keys'][0]['args_order'] = [2,1]
                if mutation == 'wrong-special': wrong['runtime_keys'][0]['special'] = True
                if mutation == 'wrong-layer': wrong['runtime_keys'][0]['effective_layer'] = 'Engine-full'
                if mutation == 'wrong-registration': wrong['runtime_keys'][0]['effective_registration']['source_tag'] = None
                if mutation == 'wrong-pin': wrong['runtime_semantics'] = dict(fr.I18N_SOURCE, sha256='0'*64)
                if mutation == 'wrong-query-tag': wrong['runtime_keys'][0]['query']['tag'] = 'other-tag'
                if mutation == 'wrong-query-method': wrong['runtime_keys'][0]['query'].update(method='string.tformat',tag='tformat')
                if mutation == 'missing-query': del wrong['runtime_keys'][0]['query']
                if mutation == 'wrong-chain':
                    other = copy.deepcopy(wrong['runtime_keys'][0])
                    other['key'] = ['hello','some-tag']
                    other['layers'].reverse()
                    wrong['runtime_keys'].append(other)
                self.save(self.directory/'closure.json',wrong)
                with self.assertRaises(fr.FullReviewError):
                    fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},{'A':{self.key},'B':set()})

        # Accept retained args/special from the actual older registration; the
        # final target row has null metadata. Then reject last-row predictions.
        engine.write_bytes(b't("hello", "early", "tformat", {2,1}, {mode="old"})\n')
        later.write_bytes(b't("hello", "' + '你好'.encode() + b'", "tformat")\n')
        with zipfile.ZipFile(candidate/'tome-test.teaa', 'w', compression=zipfile.ZIP_STORED) as package:
            package.writestr('init.lua', (candidate/'addon/init.lua').read_bytes())
            package.writestr('late.lua', later.read_bytes())
        seal['files'] = rc.file_manifest(candidate)
        seal['files'].pop('candidate.json',None)
        seal['engine_build_sha256'] = fr.sha(engine.read_bytes())
        self.save(candidate/'candidate.json',seal)
        closure['candidate_sha256'] = fr.sha((candidate/'candidate.json').read_bytes())
        mapping = closure['runtime_keys'][0]
        mapping['layers'][0]['sha256'] = fr.sha(engine.read_bytes())
        mapping['layers'][1]['sha256'] = fr.sha(later.read_bytes())
        mapping['key'] = ['hello','tformat']
        unit['runtime_key'] = ['hello','tformat']
        closure['occurrences'][0]['runtime_key'] = ['hello','tformat']
        closure['supplements'][0]['runtime_key'] = ['hello','tformat']
        mapping['query'] = {'source':'hello','tag':'tformat','method':'default_tformat'}
        mapping['effective_registration']['source_tag'] = 'tformat'
        mapping.update(args_order=[2,1], special={'mode':'old'})
        unit['occurrence'] = dict(unit['occurrence'], args_order=[2,1], special={'mode':'old'})
        self.save(self.directory/'closure.json',closure)
        with patch.object(rc,'input_hashes',return_value={}), patch.object(fr,'LuaRuntime',return_value=runtime):
            self.assertEqual(fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},
                {'A':{self.key},'B':set()})['final_runtime_denominator'],1)
            for field in ('args_order','special'):
                wrong = copy.deepcopy(closure)
                wrong['runtime_keys'][0][field] = None
                self.save(self.directory/'closure.json',wrong)
                with self.assertRaisesRegex(fr.FullReviewError,'semantics mismatch'):
                    fr.closure_check(self.manifest,self.directory,ledger,{self.key:unit},{'A':{self.key},'B':set()})

    def test_duplicate_json_keys_and_immutable_conflicts(self):
        path = self.root / 'strict.json'
        path.write_bytes(b'{"x":1,"x":2}')
        with self.assertRaises(contextual.ContractError):
            fr.read(path)
        fr.immutable(self.root/'raw', b'first')
        with self.assertRaises(fr.FullReviewError):
            fr.immutable(self.root/'raw', b'second')
        self.assertEqual((self.root/'raw').read_bytes(), b'first')

    def test_inventory_parse_reused_but_each_replay_reads_exact_bytes(self):
        self.export('a')
        self.export('a2')
        expected = fr.check(self.manifest, self.directory, _details=True)
        decode = contextual.strict_json_bytes
        ordinary = fr.ordinary
        decodes, reads = [], []

        def counted_decode(raw, *, label):
            if str(label).endswith('/inventory.json'):
                decodes.append(label)
            return decode(raw, label=label)

        def counted_read(path):
            if Path(path) == self.directory/'inventory.json':
                reads.append(path)
            return ordinary(path)

        with patch.object(contextual, 'strict_json_bytes', side_effect=counted_decode), patch.object(
                fr, 'ordinary', side_effect=counted_read):
            self.assertEqual(fr.check(self.manifest, self.directory, _details=True), expected)
        self.assertEqual(len(decodes), 1)
        self.assertEqual(len(reads), 3)  # initial parse plus both independent replay hashes
        self.assertEqual(len(expected['obligations'][self.key]), 2)
        self.export('a3')
        self.assertEqual(len(fr.check(self.manifest, self.directory, _details=True)['obligations'][self.key]), 3)
        with patch.object(contextual, 'strict_json_bytes', side_effect=counted_decode):
            ref, raw = fr.replay_export(self.manifest, self.directory, 'a', {self.key: self.unit})
        self.assertEqual(len(decodes), 2)  # standalone has its own strict parse
        self.assertEqual(ref['input_sha256'], fr.sha(raw))
        with self.assertRaisesRegex(fr.FullReviewError, 'stale export revision/guard'):
            fr.replay_export(self.manifest, self.directory, 'a',
                             {self.key: dict(self.unit, guard='wrong')})

    def test_reused_inventory_does_not_allow_duplicate_current_lane_coverage(self):
        for name in ('a', 'a2'):
            ref = fr.export(self.manifest, self.directory, [self.key], self.root/'workset.json',
                self.root/'scope.json', export_id=name, lane='A', task_id='task-'+name,
                dispatch_id='d-'+name, workspace_id='w1', parent_agent_id='parent')
            self.producer(ref)
            self.real_done(ref)
            fr.import_result(self.manifest, self.directory, name, self.root/'raw.json', self.root/'binding.json')
        with self.assertRaisesRegex(fr.FullReviewError, 'duplicate current lane coverage'):
            fr.check(self.manifest, self.directory)

    def test_inventory_mutation_between_replays_rejects_even_with_rebound_ref(self):
        import os
        self.export('a')
        self.export('a2')
        path = self.directory/'inventory.json'
        original = path.read_bytes()
        stat = path.stat()
        ref_path = self.directory/'exports/a2/ref.json'
        original_ref = ref_path.read_bytes()
        replay = fr._replay_export
        for rewrite_ref in (False, True):
            calls = []

            def mutate(*args, **kwargs):
                if calls:
                    changed = original.replace(b'test-round', b'best-round')
                    if rewrite_ref:
                        ledger = json.loads(changed)
                        ledger['inventory_identity'] = fr.sha(fr.canonical({
                            k: v for k, v in ledger.items() if k != 'inventory_identity'}))
                        changed = fr.canonical(ledger)
                    self.assertEqual(len(changed), len(original))
                    path.write_bytes(changed)
                    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
                    if rewrite_ref:
                        ref = json.loads(original_ref)
                        ref['inventory_sha256'] = fr.sha(changed)
                        ref['round_id'] = 'best-round'
                        ref['freeze_sha256'] = fr.sha(fr.canonical({k: v for k, v in ref.items() if k != 'freeze_sha256'}))
                        self.save(ref_path, ref)
                result = replay(*args, **kwargs)
                calls.append(result)
                return result

            with self.subTest(rewrite_ref=rewrite_ref), patch.object(fr, '_replay_export', side_effect=mutate):
                with self.assertRaisesRegex(fr.FullReviewError, 'snapshot bytes drift'):
                    fr.check(self.manifest, self.directory)
            self.assertEqual(len(calls), 1)
            self.assertEqual(path.stat().st_mtime_ns, stat.st_mtime_ns)
            self.assertFalse((self.directory/'imports').exists())
            path.write_bytes(original)
            ref_path.write_bytes(original_ref)

    def test_inventory_strict_bytes_and_snapshot_directory_are_not_caller_dicts(self):
        self.export()
        path = self.directory/'inventory.json'
        original = path.read_bytes()
        snapshot = fr._InventorySnapshot(self.directory)
        with self.assertRaises(TypeError):
            fr.check(self.manifest, self.directory, _inventory=snapshot)
        with self.assertRaises(TypeError):
            fr.replay_export(self.manifest, self.directory, 'a', {self.key: self.unit}, _inventory={})
        other = self.root/'other'
        other.mkdir()
        (other/'inventory.json').write_bytes(original)
        with self.assertRaisesRegex(fr.FullReviewError, 'snapshot path mismatch'):
            snapshot.verify(other)
        for invalid in (b'{"round_id":"test-round","round_id":"test-round"}', b'{"x":NaN}'):
            path.write_bytes(invalid)
            with self.assertRaises(contextual.ContractError):
                fr.replay_export(self.manifest, self.directory, 'a', {self.key: self.unit})
        path.write_bytes(original + b'\n')
        with self.assertRaisesRegex(fr.FullReviewError, 'inventory binding drift'):
            fr.replay_export(self.manifest, self.directory, 'a', {self.key: self.unit})

    def test_sequential_replays_keep_ref_input_and_source_checks(self):
        self.export('a')
        self.export('a2')
        replay = fr._replay_export
        dest = self.directory/'exports/a2'
        for mutation in ('ref', 'round', 'input', 'source', 'preflight'):
            files = {p: p.read_bytes() for p in dest.rglob('*') if p.is_file()}
            calls = []

            def mutate(*args, **kwargs):
                if calls:
                    if mutation in ('ref', 'round'):
                        ref = fr.read(dest/'ref.json')
                        ref['round_id'] = 'wrong-round'
                        if mutation == 'round':
                            ref['freeze_sha256'] = fr.sha(fr.canonical({k: v for k, v in ref.items() if k != 'freeze_sha256'}))
                        self.save(dest/'ref.json', ref)
                    else:
                        path = (next((dest/'source-anchors').glob('*.bin')) if mutation == 'source'
                                else dest/('input.json' if mutation == 'input' else 'preflight.json'))
                        path.write_bytes(path.read_bytes() + b' ')
                result = replay(*args, **kwargs)
                calls.append(result)
                return result

            with self.subTest(mutation=mutation), patch.object(fr, '_replay_export', side_effect=mutate):
                with self.assertRaises(fr.FullReviewError):
                    fr.check(self.manifest, self.directory)
            self.assertEqual(len(calls), 1)
            self.assertFalse((self.directory/'imports').exists())
            for path, raw in files.items():
                path.write_bytes(raw)

    def test_reused_inventory_still_validates_current_source_for_every_replay(self):
        self.export('a')
        self.export('a2')
        with patch.object(fr, 'source_file', side_effect=[
                {'content': 'hello', 'sha256': fr.sha(b'hello')},
                fr.FullReviewError('source file hash mismatch')]) as source:
            with self.assertRaisesRegex(fr.FullReviewError, 'source file hash mismatch'):
                fr.check(self.manifest, self.directory)
        self.assertEqual(source.call_count, 2)
        self.assertFalse((self.directory/'imports').exists())


class SuccessorTests(FullRoundTests):
    def setUp(self):
        super().setUp()
        self.supplement = {'supplement_id': 'source-one', 'kind': 'source-visible',
                           'component': 'engine', 'record': {'source': 'hello'}}
        self.ledger['supplements'] = [self.supplement]
        self.ledger.pop('inventory_identity')
        self.ledger['inventory_identity'] = fr.sha(fr.canonical(self.ledger))
        self.save(self.directory/'inventory.json', self.ledger)
        proof = self.root/'evidence/host.txt'
        proof.parent.mkdir(exist_ok=True)
        proof.write_bytes(b'Host source/runtime adjudication fixture, not production review')
        self.evidence = [{'path': 'evidence/host.txt', 'sha256': fr.sha(proof.read_bytes())}]
        self.next = self.root/'successor'

    def accepted(self):
        ref = self.export()
        self.producer(ref)
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        decision = {'round_id': 'test-round', 'unit_id': self.key, 'revision_key': self.unit['revision_key'],
            'raw_sha256': {'A': fr.sha(self.raw)}, 'source_verified': True, 'accepted_successor': True,
            'confirmed': [], 'blocking_pending': [], 'status': 'effective-complete', 'evidence': self.evidence}
        self.save(self.directory/'adjudications/one.json', decision)

    def request(self, status='unchanged', language=None):
        language = language or []
        units = [self.unit] + [fr.supplemental_unit(self.manifest, x, [self.supplement], 'unrelated-terms') for x in language]
        contexts = {self.key: self.workset['entries'][0]}
        for unit in units[1:]:
            spec = unit['supplement_spec']
            contexts[unit['unit_id']] = {'unit_id': unit['unit_id'], 'context': spec['context'],
                'source_files': spec['source_files'], 'b_reasons': [], 'b_exemption': 'short literal'}
        return {'round_id': 'test-round', 'before_sha256': fr.sha((self.directory/'inventory.json').read_bytes()),
            'evidence': self.evidence, 'supplements': [self.supplement], 'language_units': language,
            'mapping': [{'unit_id': self.key, 'status': status, 'reason': 'host current bytes'}] +
                       [{'unit_id': u['unit_id'], 'status': 'added', 'reason': 'actual supplemental language'} for u in units[1:]],
            'supplement_mapping': [{'supplement_id': 'source-one', 'status': 'unchanged', 'reason': 'same origin'}],
            'contexts': contexts}

    def migrate(self, request):
        self.save(self.root/'request.json', request)
        return fr.successor(self.manifest, self.directory, self.next, self.root/'request.json')

    def import_lane(self, directory, lane, entry, *, issue=False):
        self.save(self.root/'lane-workset.json',{'round_id':'test-round','entries':[entry]})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            ref = fr.export(self.manifest,directory,[self.key],self.root/'lane-workset.json',self.root/'scope.json',
                export_id=lane.lower(),lane=lane,task_id='task-'+lane.lower(),dispatch_id='d-'+lane.lower(),
                workspace_id='w1',parent_agent_id='parent')
        self.producer(ref)
        if issue:
            value = json.loads(self.raw)
            value['verdicts'][0].update(verdict='ISSUE',observation='private A observation; never in B')
            self.raw = fr.canonical(value)
        self.binding.update(model='exact-model-'+lane.lower(),raw_sha256=fr.sha(self.raw))
        self.state['child_dispatches'][0].update(raw_output_sha256=fr.sha(self.raw),
            runtime_observation={'model':{'presence':'present','value':self.binding['model']}})
        self.save(self.state_path,self.state)
        self.save(self.root/'binding.json',self.binding)
        (self.root/'raw.json').write_bytes(self.raw)
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            fr.import_result(self.manifest,directory,lane.lower(),self.root/'raw.json',self.root/'binding.json')
        return fr.sha(self.raw)

    def decide(self, directory, hashes):
        self.save(directory/'adjudications/one.json',{'round_id':'test-round','unit_id':self.key,
            'revision_key':self.unit['revision_key'],'raw_sha256':hashes,'source_verified':True,
            'accepted_successor':True,'confirmed':[],'blocking_pending':[],
            'status':'effective-complete','evidence':self.evidence})

    def test_real_done_successor_keeps_accepted_coverage_after_tool_and_runner_change(self):
        ref = self.export(); self.producer(ref); self.real_done(ref)
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        self.decide(self.directory,{'A':fr.sha(self.raw)})
        (self.root/'tools/unrelated.py').write_text('unrelated = True\n')
        with patch.object(fr.gate_results,'VERSION','ci-gates-v999'), patch.object(
                fr.gate_results,'checks',return_value=[('new-definition',['new-command'])]):
            self.assertEqual(fr.check(self.manifest,self.directory)['A_effective_complete'],1)
            self.migrate(self.request())
            result = fr.check(self.manifest,self.next)
            self.assertEqual((result['A_validated_outputs'],result['A_effective_complete']),(1,1))

    def test_multi_export_predecessor_reuses_parses_and_preserves_seal_validation(self):
        ref = self.export()
        self.producer(ref)
        self.real_done(ref)
        fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        self.decide(self.directory, {'A': fr.sha(self.raw)})
        self.export('a2')
        self.migrate(self.request())
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            expected = fr.check(self.manifest, self.next)
            decode = contextual.strict_json_bytes
            labels = []

            def counted(raw, *, label):
                if str(label).endswith('/inventory.json'):
                    labels.append(str(label))
                return decode(raw, label=label)

            with patch.object(contextual, 'strict_json_bytes', side_effect=counted):
                self.assertEqual(fr.check(self.manifest, self.next), expected)
            self.assertEqual(len(labels), 2)  # one strict parse per round, byte recheck on handoff
            self.assertEqual(expected['A_effective_complete'], 1)
            original = (self.directory/'exports/a2/input.json').read_bytes()
            (self.directory/'exports/a2/input.json').write_bytes(original + b' ')
            with self.assertRaisesRegex(fr.FullReviewError, 'predecessor frozen evidence drift'):
                fr.check(self.manifest, self.next)
            (self.directory/'exports/a2/input.json').write_bytes(original)
        ref = fr.export(self.manifest, self.next, [self.key], self.root/'workset.json',
            self.root/'scope.json', export_id='new-a', lane='A', task_id='task-new-a',
            dispatch_id='d-new-a', workspace_id='w1', parent_agent_id='parent')
        self.producer(ref)
        self.real_done(ref, self.next)
        fr.import_result(self.manifest, self.next, 'new-a', self.root/'raw.json', self.root/'binding.json')
        with self.assertRaisesRegex(fr.FullReviewError, 'duplicate inherited/current coverage'):
            fr.check(self.manifest, self.next)

    def three_round_chain(self):
        ref = self.export()
        self.producer(ref)
        self.real_done(ref)
        fr.import_result(self.manifest, self.directory, 'a', self.root/'raw.json', self.root/'binding.json')
        self.decide(self.directory, {'A': fr.sha(self.raw)})
        first = self.directory
        expected = fr.check(self.manifest, first)
        self.migrate(self.request())
        self.directory, self.next = self.next, self.root/'third'
        self.migrate(self.request())
        return first, self.directory, self.next, expected

    def test_three_round_exact_results_one_decode_each_and_independent_reload(self):
        first, middle, last, expected = self.three_round_chain()
        expected_details = fr.check(self.manifest, middle, _details=True)
        decode = contextual.strict_json_bytes
        labels = []

        def counted(raw, *, label):
            if str(label).endswith('/inventory.json'):
                labels.append(str(label))
            return decode(raw, label=label)

        with patch.object(contextual, 'strict_json_bytes', side_effect=counted):
            self.assertEqual(fr.check(self.manifest, last), expected)
            self.assertEqual(labels, [str(p/'inventory.json') for p in (last, middle, first)])
            labels.clear()
            self.assertEqual(fr.check(self.manifest, last, _details=True), expected_details)
            self.assertEqual(len(labels), 3)  # separate invocation owns fresh snapshots
        path = last/'inventory.json'
        original = path.read_bytes()
        path.write_bytes(b'{"x":NaN}')
        with self.assertRaises(contextual.ContractError):
            fr.check(self.manifest, last)
        path.write_bytes(original)
        fr.export(self.manifest, last, [self.key], self.root/'workset.json', self.root/'scope.json',
                  export_id='fresh', lane='A', task_id='fresh', dispatch_id='fresh',
                  workspace_id='w1', parent_agent_id='parent')
        self.assertEqual(len(fr.check(self.manifest, last, _details=True)['obligations'][self.key]), 2)

    def test_handoff_rechecks_exact_bytes_and_paths_after_parent_seal(self):
        import os
        first, middle, last, expected = self.three_round_chain()
        check = fr._check
        for target in (middle, first):
            path = target/'inventory.json'
            original = path.read_bytes()
            stat = path.stat()
            for mode in ('same-size', 'rebound', 'duplicate', 'nan', 'symlink'):
                called = []
                ref_path = first/'exports/a/ref.json'
                ref_original = ref_path.read_bytes()

                def mutate(manifest, directory, **kwargs):
                    if Path(directory) == target and kwargs.get('_inventory') is not None:
                        called.append(directory)
                        if mode == 'symlink':
                            backup = self.root/'inventory-copy.json'
                            backup.write_bytes(original)
                            path.unlink()
                            path.symlink_to(backup)
                        else:
                            changed = original.replace(b'test-round', b'best-round')
                            if mode == 'rebound':
                                ledger = json.loads(changed)
                                ledger['inventory_identity'] = fr.sha(fr.canonical({
                                    k: v for k, v in ledger.items() if k != 'inventory_identity'}))
                                changed = fr.canonical(ledger)
                                ref = json.loads(ref_original)
                                ref.update(inventory_sha256=fr.sha(changed), round_id='best-round')
                                ref['freeze_sha256'] = fr.sha(fr.canonical({
                                    k: v for k, v in ref.items() if k != 'freeze_sha256'}))
                                self.save(ref_path, ref)
                            elif mode == 'duplicate':
                                changed = b'{"x":1,"x":2}'
                            elif mode == 'nan':
                                changed = b'{"x":NaN}'
                            if mode in ('same-size', 'rebound'):
                                self.assertEqual(len(changed), len(original))
                            path.write_bytes(changed)
                            os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
                    return check(manifest, directory, **kwargs)

                with self.subTest(target=target.name, mode=mode), patch.object(fr, '_check', side_effect=mutate):
                    with self.assertRaisesRegex(fr.FullReviewError, 'snapshot bytes drift|not an ordinary file'):
                        fr.check(self.manifest, last)
                self.assertEqual(len(called), 1)
                if path.is_symlink():
                    path.unlink()
                path.write_bytes(original)
                os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
                ref_path.write_bytes(ref_original)
                self.assertEqual(fr.check(self.manifest, last), expected)

    def test_removed_legacy_unit_does_not_gain_new_mapping_field_requirements(self):
        self.ledger['units'].append({'unit_id': 'retired', 'disposition': 'release-required'})
        self.ledger.pop('inventory_identity')
        self.ledger['inventory_identity'] = fr.sha(fr.canonical(self.ledger))
        self.save(self.directory/'inventory.json', self.ledger)
        request = self.request()
        request['mapping'].append({'unit_id': 'retired', 'status': 'removed', 'reason': 'legacy unit removed'})
        self.migrate(request)
        self.assertEqual(fr.check(self.manifest, self.next)['provisional_applicable_units'], 1)

    def test_parent_mapping_projection_does_not_alias_child_ledger(self):
        # Structured guards make shallow copies observably unsafe even though
        # production guards currently are strings. No private native data used.
        import copy
        self.unit['guard'] = {'nested': ['original']}
        self.ledger.pop('inventory_identity')
        self.ledger['inventory_identity'] = fr.sha(fr.canonical(self.ledger))
        self.save(self.directory/'inventory.json', self.ledger)
        self.migrate(self.request())
        copied = []
        check = fr._check

        def project(value):
            result = copy.deepcopy(value)
            copied.append(result)
            return result

        def observe(manifest, directory, **kwargs):
            snapshot = kwargs.get('_inventory')
            if snapshot is not None:
                guard = snapshot.ledger['units'][0]['guard']
                guard['nested'].append('child')
                self.assertEqual(copied[-1]['guard'], {'nested': ['original']})
                copied[-1]['guard']['nested'].append('parent')
                self.assertEqual(guard['nested'], ['original', 'child'])
                guard['nested'].pop()
                copied[-1]['guard']['nested'].pop()
            return check(manifest, directory, **kwargs)

        with patch.object(fr, 'deepcopy', side_effect=project), patch.object(fr, '_check', side_effect=observe):
            result = fr.check(self.manifest, self.next)
        self.assertEqual(len(copied), 1)
        self.assertEqual(result['A_validated_outputs'], 0)

    def test_concurrent_freeze_pair_complete_and_policy_only_growth(self):
        import copy
        entry = copy.deepcopy(self.workset['entries'][0])
        entry['b_reasons'] = ['mechanics']
        self.save(self.root/'lane-workset.json',{'round_id':'test-round','entries':[entry]})
        for lane in ('A','B'):
            fr.export(self.manifest,self.directory,[self.key],self.root/'lane-workset.json',self.root/'scope.json',
                export_id=lane.lower(),lane=lane,task_id='task-'+lane.lower(),dispatch_id='d-'+lane.lower(),
                workspace_id='w1',parent_agent_id='parent')
        a = self.import_lane(self.directory,'A',entry)
        b = self.import_lane(self.directory,'B',entry)
        self.decide(self.directory,{'A':a,'B':b})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            result = fr.check(self.manifest,self.directory)
            self.assertEqual((result['A_effective_complete'],result['B_effective_complete']),(1,1))
        grown = copy.deepcopy(entry)
        grown.update(b_reasons=['mechanics','long-text'],b_exemption='expanded policy only')
        self.save(self.root/'grown.json',{'round_id':'test-round','entries':[grown]})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            fr.export(self.manifest,self.directory,[self.key],self.root/'grown.json',self.root/'scope.json',
                export_id='grown-b',lane='B',task_id='grown',dispatch_id='grown',workspace_id='w1',parent_agent_id='parent')

    def freeze_pending_b(self):
        import copy
        entry = copy.deepcopy(self.workset['entries'][0])
        entry['b_reasons'] = ['mechanics']
        self.save(self.root/'pending.json', {'round_id':'test-round','entries':[entry]})
        return fr.export(self.manifest,self.directory,[self.key],self.root/'pending.json',self.root/'scope.json',
            export_id='pending-b',lane='B',task_id='pending-b',dispatch_id='pending-b',
            workspace_id='w1',parent_agent_id='parent')

    def import_real_b(self, directory, ref):
        self.producer(ref)
        self.binding['model'] = 'exact-model-b'
        self.state['child_dispatches'][0]['runtime_observation']['model']['value'] = 'exact-model-b'
        self.save(self.root/'binding.json',self.binding)
        self.real_done(ref, directory)
        fr.import_result(self.manifest,directory,ref['export_id'],self.root/'raw.json',self.root/'binding.json')
        return fr.sha(self.raw)

    def test_pending_frozen_b_blocks_a_only_decision_then_real_merged_raw_passes(self):
        ref = self.export(); self.producer(ref); self.real_done(ref)
        a = fr.sha(self.raw)
        pending = self.freeze_pending_b()  # A exempt, same neutral B grows before either import.
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        result = fr.check(self.manifest,self.directory)
        self.assertEqual((result['A_validated_outputs'],result['B_validated_outputs'],result['A_effective_complete']),(1,0,0))
        self.decide(self.directory,{'A':a})
        with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
            fr.check(self.manifest,self.directory)
        with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
            fr.check(self.manifest,self.directory,require_complete=True)
        b = self.import_real_b(self.directory,pending)
        with self.assertRaisesRegex(fr.FullReviewError,'raw binding mismatch'):
            fr.check(self.manifest,self.directory)
        self.decide(self.directory,{'A':a,'B':b})
        result = fr.check(self.manifest,self.directory)
        self.assertEqual((result['A_effective_complete'],result['B_effective_complete']),(1,1))

    def test_successor_carries_pending_frozen_b_despite_omitted_host_reason(self):
        import copy
        ref = self.export(); self.producer(ref); self.real_done(ref)
        a = fr.sha(self.raw)
        fr.import_result(self.manifest,self.directory,'a',self.root/'raw.json',self.root/'binding.json')
        self.decide(self.directory,{'A':a})
        self.assertEqual(fr.check(self.manifest,self.directory)['A_effective_complete'],1)
        self.freeze_pending_b()
        # A stale merged decision cannot silently survive a new frozen duty.
        self.migrate(self.request())
        with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
            fr.check(self.manifest,self.next)
        # Independent successor after host withdraws stale decision safely inherits
        # the pending obligation although contexts omit the mechanics reason.
        (self.directory/'adjudications/one.json').unlink()
        self.next = self.root/'safe-successor'
        self.migrate(self.request())
        self.assertEqual(fr.check(self.manifest,self.next)['A_effective_complete'],0)
        self.decide(self.next,{'A':a})
        with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
            fr.check(self.manifest,self.next)
        (self.next/'adjudications/one.json').unlink()
        self.save(self.root/'exempt.json', self.workset)
        with self.assertRaisesRegex(fr.FullReviewError,'cannot shrink'):
            fr.export(self.manifest,self.next,[self.key],self.root/'exempt.json',self.root/'scope.json',
                export_id='exempt',lane='A',task_id='exempt',dispatch_id='exempt',workspace_id='w1',parent_agent_id='parent')
        entry = copy.deepcopy(self.workset['entries'][0]); entry['b_reasons'] = ['mechanics']
        self.save(self.root/'fresh.json',{'round_id':'test-round','entries':[entry]})
        fresh = fr.export(self.manifest,self.next,[self.key],self.root/'fresh.json',self.root/'scope.json',
            export_id='fresh-b',lane='B',task_id='fresh-b',dispatch_id='fresh-b',workspace_id='w1',parent_agent_id='parent')
        b = self.import_real_b(self.next,fresh)
        self.decide(self.next,{'A':a,'B':b})
        self.assertEqual(fr.check(self.manifest,self.next)['B_effective_complete'],1)
        # A genuinely different neutral context starts independently under existing rules.
        self.next = self.root/'different-context'
        request = copy.deepcopy(self.request()); request['contexts'][self.key]['context'] = 'independent usage'
        self.migrate(request)
        details = fr.check(self.manifest,self.next,_details=True)
        self.assertEqual(details['obligations'],{})
        self.assertEqual(details['outputs']['A'],{})

    def test_issue_forces_b_and_successor_merges_old_a_new_b_neutrally(self):
        import copy
        entry = copy.deepcopy(self.workset['entries'][0])
        a_hash = self.import_lane(self.directory,'A',entry,issue=True)
        self.decide(self.directory,{'A':a_hash})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
                fr.check(self.manifest,self.directory)
        (self.directory/'adjudications/one.json').unlink()
        old_raw = (self.directory/'imports/a/raw.json').read_bytes()
        request = self.request()
        request['contexts'][self.key]['b_reasons'] = ['A-observation']
        self.migrate(request)
        entry['b_reasons'] = ['A-observation']
        for field in ('context','source_files'):
            wrong = copy.deepcopy(entry)
            if field == 'context': wrong[field] = 'different inherited usage'
            else: wrong[field][0]['line_end'] = 1
            self.save(self.root/'wrong.json',{'round_id':'test-round','entries':[wrong]})
            with self.assertRaises(fr.FullReviewError):
                fr.export(self.manifest,self.next,[self.key],self.root/'wrong.json',self.root/'scope.json',
                    export_id='wrong-'+field,lane='B',task_id='wrong',dispatch_id='wrong',workspace_id='w1',parent_agent_id='parent')
        b_hash = self.import_lane(self.next,'B',entry)
        envelope = (self.next/'exports/b/input.json').read_bytes()
        self.assertNotIn(b'private A observation',envelope)
        self.assertEqual(fr.read(self.next/'exports/b/input.json')['payload']['bounded_context'],
                         fr.read(self.directory/'exports/a/input.json')['payload']['bounded_context'])
        self.decide(self.next,{'A':a_hash,'B':b_hash})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            result = fr.check(self.manifest,self.next)
            self.assertEqual((result['A_effective_complete'],result['B_effective_complete']),(1,1))
        self.assertEqual(old_raw,(self.directory/'imports/a/raw.json').read_bytes())

    def test_dropped_b_cannot_inherit_merged_completion_but_a_stays_validated(self):
        import copy
        entry = copy.deepcopy(self.workset['entries'][0]); entry['b_reasons'] = ['mechanics']
        a_hash = self.import_lane(self.directory,'A',entry)
        b_hash = self.import_lane(self.directory,'B',entry)
        self.decide(self.directory,{'A':a_hash,'B':b_hash})
        # A successor widens obligation even without changing neutral context.
        request = self.request(); request['contexts'][self.key]['b_reasons'] = ['mechanics']
        # Controlled historical B context differs: re-freeze its own workset/ref bytes
        # with actual export path instead of mocking current coverage.
        b_ref_path = self.directory/'exports/b/ref.json'
        b_ref = fr.read(b_ref_path)
        workset_path = self.directory/'exports/b/workset.json'
        workset = fr.read(workset_path); workset['entries'][0]['context'] = 'distinct neutral B usage'
        self.save(workset_path,workset)
        b_ref['workset_sha256'] = fr.sha(workset_path.read_bytes())
        b_ref['freeze_sha256'] = fr.sha(fr.canonical({k:v for k,v in b_ref.items() if k != 'freeze_sha256'}))
        self.save(b_ref_path,b_ref)
        # Host reproduction deliberately has lane-specific historical context; only
        # the narrow inheritance filter is controlled, all merged completion logic runs.
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            # Rebind fixture task SPEC/gates/terminal bytes to changed freeze.
            self.producer(b_ref)
            self.binding.update(model='exact-model-b')
            self.state['child_dispatches'][0]['runtime_observation']['model']['value']='exact-model-b'
            self.save(self.state_path,self.state); self.save(self.root/'binding.json',self.binding)
            import shutil
            shutil.rmtree(self.directory/'imports/b')
            fr.import_result(self.manifest,self.directory,'b',self.root/'raw.json',self.root/'binding.json')
            # The formerly admitted mismatched historical pair is now rejected.
            with self.assertRaisesRegex(fr.FullReviewError,'neutral source/context'):
                fr.check(self.manifest,self.directory)
            # A valid A-only predecessor still cannot satisfy the widened B duty.
            shutil.rmtree(self.directory/'exports/b')
            shutil.rmtree(self.directory/'imports/b')
            (self.directory/'adjudications/one.json').unlink()
            self.migrate(request)
            result = fr.check(self.manifest,self.next)
            self.assertEqual(result['A_validated_outputs'],1)
            self.assertEqual(result['B_validated_outputs'],0)
            self.assertEqual(result['A_effective_complete'],0)
            # Legal preserved A can be remerged with a new current B and decision.
            fresh_entry = copy.deepcopy(request['contexts'][self.key])
            self.save(self.root/'fresh.json',{'round_id':'test-round','entries':[fresh_entry]})
            ref = fr.export(self.manifest,self.next,[self.key],self.root/'fresh.json',self.root/'scope.json',
                export_id='fresh-b',lane='B',task_id='fresh-b',dispatch_id='fresh-b',workspace_id='w1',parent_agent_id='parent')
            self.producer(ref)
            self.binding['model']='fresh-b-model'
            self.state['child_dispatches'][0]['runtime_observation']['model']['value']='fresh-b-model'
            self.save(self.state_path,self.state); self.save(self.root/'binding.json',self.binding)
            fr.import_result(self.manifest,self.next,'fresh-b',self.root/'raw.json',self.root/'binding.json')
            self.decide(self.next,{'A':a_hash,'B':fr.sha(self.raw)})
            self.assertEqual(fr.check(self.manifest,self.next)['A_effective_complete'],1)

    def test_unchanged_effective_coverage_survives_without_rewriting_old_raw(self):
        self.accepted()
        seal = fr.tree_seal(self.directory)
        req = self.request()
        first = self.migrate(req)
        self.assertEqual(first, self.migrate(req))
        # Recover an interrupted migration before publication of inventory.
        (self.next/'inventory.json').unlink()
        self.assertEqual(first, self.migrate(req))
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            self.assertEqual(fr.check(self.manifest, self.next)['A_effective_complete'], 1)
        self.assertEqual(seal, fr.tree_seal(self.directory))
        req['evidence'][0]['sha256'] = '0'*64
        with self.assertRaises(fr.FullReviewError):
            self.migrate(req)

    def test_target_special_source_args_and_context_cannot_inherit(self):
        import copy
        for change in ('target', 'special', 'source', 'args', 'context', 'source-file'):
            with self.subTest(change=change):
                # Each independent version starts from the same effective predecessor.
                if not (self.directory/'imports/a/receipt.json').exists():
                    self.accepted()
                old = copy.deepcopy(self.unit)
                if change in ('target', 'source'):
                    self.unit['occurrence'][change] = 'changed'
                    self.unit['revision_key'] = 'b'*64
                    self.unit['guard'] = 'changed'
                elif change in ('special', 'args'):
                    self.unit['guard'] = 'changed-' + change
                    if change == 'special':
                        self.unit['occurrence']['special'] = True
                    else:
                        self.unit['occurrence']['source'] = 'hello %s'
                        self.unit['occurrence']['args_order'] = [1]
                        self.unit['revision_key'] = 'c'*64
                req = self.request('changed' if change not in ('context','source-file') else 'unchanged')
                if change == 'context': req['contexts'][self.key]['context'] = 'new usage'
                if change == 'source-file': req['contexts'][self.key]['source_files'][0]['sha256'] = 'b'*64
                self.next = self.root/('successor-' + change)
                self.migrate(req)
                with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
                    self.assertEqual(fr.check(self.manifest, self.next)['A_effective_complete'], 0)
                with self.assertRaises(fr.FullReviewError):
                    fr.import_result(self.manifest, self.next, 'a', self.root/'raw.json', self.root/'binding.json')
                self.unit.clear(); self.unit.update(old)
                self.workset['entries'][0]['context'] = 'neutral usage'
                self.workset['entries'][0]['source_files'][0]['sha256'] = fr.sha(b'hello')

    def test_conservation_old_round_and_frozen_conflict(self):
        req = self.request()
        for field, value in [('round_id','old-round'), ('mapping', []), ('supplement_mapping', [])]:
            bad = dict(req, **{field:value})
            with self.assertRaises(fr.FullReviewError): self.migrate(bad)
        self.migrate(req)
        changed = dict(req, evidence=self.evidence, contexts={self.key: dict(req['contexts'][self.key], context='changed')})
        with self.assertRaises(fr.FullReviewError): self.migrate(changed)
        (self.directory/'late.json').write_bytes(b'{}')
        with self.assertRaises(fr.FullReviewError): fr.check(self.manifest, self.next)

    def language_spec(self, kind):
        # Three real noncanonical language forms, with exact UTF-8 byte evidence.
        contents = {'source-only': 'hello', 'inheritance': 'hello\n继承译文', 'copy': 'hello\n复制文本'}
        text = contents[kind]
        path = self.root/(kind + '.txt')
        path.write_text(text, encoding='utf-8')
        raw = path.read_bytes()
        target = 'hello' if kind == 'source-only' else text.split('\n')[1]
        start = raw.index(target.encode())
        return {'language_id': kind, 'origins': ['source-one'], 'evidence': self.evidence,
            'language': {'source':'hello', 'target':target, 'source_tag':None, 'args_order':None, 'special':None},
            'anchors': {'source': {'path':path.name, 'sha256':fr.sha(raw), 'start':0, 'end':5},
                        'target': {'path':path.name, 'sha256':fr.sha(raw), 'start':start, 'end':start+len(target.encode())}},
            'context':'neutral actual runtime literal: ' + kind,
            'source_files':self.workset['entries'][0]['source_files']}

    def test_three_noncanonical_forms_real_envelope_preflight_and_strict_import(self):
        # Exercise the actual public unpinned source/hash reader, not its mock.
        self.source_patch.stop()
        inner = self.root/'tome-ashes-urhrok'
        inner.mkdir()
        source = inner/'actual.lua'
        source.write_bytes(b'hello')
        component = SimpleNamespace(source_repository=None,protected_source=SimpleNamespace(visibility='public',mount=inner.name))
        self.manifest.component = lambda name: component
        self.workset['entries'][0]['source_files'] = [{'component':'ashes-urhrok',
            'public_source_path':inner.name+'/actual.lua','sha256':fr.sha(source.read_bytes()),'inner_root':str(inner)}]
        for kind in ('source-only', 'inheritance', 'copy'):
            with self.subTest(kind=kind):
                spec = self.language_spec(kind)
                req = self.request(language=[spec])
                self.next = self.root/('language-' + kind)
                self.migrate(req)
                ledger = fr.read(self.next/'inventory.json')
                unit = ledger['units'][1]
                key = unit['unit_id']
                workset = {'round_id':'test-round', 'entries':[req['contexts'][key]]}
                scope = {'schema_version':1, 'allowed_files':[kind+'.txt'],
                    'anchor_scopes':[{'file':kind+'.txt', 'section_path':'actual-runtime-bytes', 'ordered_titles':[]}]}
                self.save(self.root/'language-workset.json', workset)
                self.save(self.root/'language-scope.json', scope)
                ref = fr.export(self.manifest,self.next,[key],self.root/'language-workset.json',self.root/'language-scope.json',
                    export_id='supp-a',lane='A',task_id='task-one',dispatch_id='d1',workspace_id='w1',parent_agent_id='parent')
                payload, _ = contextual.validate_envelope(fr.read(self.next/'exports/supp-a/input.json'))
                self.assertEqual(set(payload), contextual.PAYLOAD_KEYS)
                self.assertEqual(payload['translation_snapshot'][0]['target'], spec['language']['target'])
                self.assertIn('supplement_origin=', payload['bounded_context'][0]['context'])
                self.assertNotIn('call_locator', unit)
                receipt = fr.read(self.next/'exports/supp-a/preflight.json')
                self.assertEqual(receipt['status'],'PREFLIGHT_VERIFIED')
                self.assertEqual(fr.sha((self.next/'exports/supp-a/preflight.json').read_bytes()),ref['preflight_sha256'])
                self.assertIn('unpinned',payload['bounded_context'][0]['context'])
                self.assertLessEqual(len((self.next/'exports/supp-a/prompt.txt').read_bytes()),800)
                # Controlled task fixture with real strict output/receipt validation.
                self.producer(ref)
                (self.state_path.parent/'SCOPE.json').write_bytes((self.root/'language-scope.json').read_bytes())
                self.gate_fixture(ref)
                self.raw = fr.canonical({'contract':'translation_contextual_v2','candidate_identity':ref['candidate_identity'],
                    'verdicts':[{'revision_key':unit['revision_key'],'verdict':'OK'}]})
                self.binding['raw_sha256'] = fr.sha(self.raw)
                self.state['child_dispatches'][0]['raw_output_sha256'] = fr.sha(self.raw)
                self.save(self.state_path,self.state)
                self.save(self.root/'binding.json',self.binding)
                (self.root/'raw.json').write_bytes(self.raw)
                with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
                    fr.import_result(self.manifest,self.next,'supp-a',self.root/'raw.json',self.root/'binding.json')
                    result = fr.check(self.manifest,self.next)
                    self.assertEqual(result['A_validated_outputs'],1)
                    self.assertEqual(result['A_effective_complete'],0)
                    with self.assertRaises(fr.FullReviewError): fr.check(self.manifest,self.next,require_complete=True)
                bad = fr.canonical({'contract':'translation_contextual_v2','candidate_identity':ref['candidate_identity'],'verdicts':[]})
                with self.assertRaises(contextual.ContractError):
                    contextual.validate_result_bytes((self.next/'exports/supp-a/input.json').read_bytes(),bad)
                (self.root/(kind+'.txt')).write_bytes(b'drift')
                with self.assertRaises(fr.FullReviewError): fr.check(self.manifest,self.next)

    def test_b_is_required_and_same_model_cannot_complete_supplement(self):
        spec = self.language_spec('copy')
        req = self.request(language=[spec])
        key = next(k for k in req['contexts'] if k != self.key)
        req['contexts'][key]['b_reasons'] = ['mechanics']
        self.migrate(req)
        unit = fr.read(self.next/'inventory.json')['units'][1]
        self.save(self.root/'workset-b.json', {'round_id':'test-round','entries':[req['contexts'][key]]})
        scope = {'schema_version':1,'allowed_files':['copy.txt'],
            'anchor_scopes':[{'file':'copy.txt','section_path':'actual-bytes','ordered_titles':[]}]}
        self.save(self.root/'scope-b.json',scope)
        for lane, dispatch, task in [('A','d1','task-one'),('B','d2','task-two')]:
            with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
                ref = fr.export(self.manifest,self.next,[key],self.root/'workset-b.json',self.root/'scope-b.json',
                export_id=lane.lower(),lane=lane,task_id=task,dispatch_id=dispatch,workspace_id='w1',parent_agent_id='parent')
            self.producer(ref)
            self.binding.update(task_id=task,dispatch_id=dispatch)
            raw = fr.canonical({'contract':'translation_contextual_v2','candidate_identity':ref['candidate_identity'],
                               'verdicts':[{'revision_key':unit['revision_key'],'verdict':'OK'}]})
            self.binding['raw_sha256'] = fr.sha(raw)
            self.save(self.root/'binding.json',self.binding)
            (self.root/'raw.json').write_bytes(raw)
            self.state.update(task_id=task)
            self.state['child_dispatches'][0].update(dispatch_id=dispatch,raw_output_sha256=fr.sha(raw))
            path = self.root/'.ai/task'/task/'STATE.json'
            self.save(path,self.state)
            (path.parent/'SCOPE.json').write_bytes((self.root/'scope-b.json').read_bytes())
            binding = {k:ref[k] for k in ('round_id','export_id','freeze_sha256','input_sha256')}
            (path.parent/'SPEC.md').write_text('full_review_binding='+fr.canonical(binding).decode())
            self.state_path = path
            self.gate_fixture(ref)
            with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
                fr.import_result(self.manifest,self.next,lane.lower(),self.root/'raw.json',self.root/'binding.json')
            if lane == 'A':
                self.save(self.next/'adjudications/supp.json',{'round_id':'test-round','unit_id':key,
                    'revision_key':unit['revision_key'],'source_verified':True,'accepted_successor':True,
                    'confirmed':[],'blocking_pending':[],'status':'effective-complete','evidence':self.evidence,
                    'raw_sha256':{'A':fr.sha(raw),'B':fr.sha(raw)}})
                with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
                    with self.assertRaisesRegex(fr.FullReviewError,'missing required B'):
                        fr.check(self.manifest,self.next)
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            with self.assertRaisesRegex(fr.FullReviewError,'different exact models'):
                fr.check(self.manifest,self.next)

    def test_changed_target_requires_new_export_own_done_and_adjudication(self):
        self.accepted()
        self.unit['occurrence']['target'] = '新译文'
        rows, _ = catalog.formal_rows([self.unit['occurrence']],terminology='terms',sources={'engine':'commit:'+'a'*40})
        self.unit.update(catalog_row=rows[0], revision_key=rows[0]['entry_revision_identity'],guard='new-target')
        self.migrate(self.request('changed'))
        # A bare accepted flag cannot manufacture coverage for a changed successor.
        self.save(self.next/'adjudications/new.json',{'round_id':'test-round','unit_id':self.key,
            'revision_key':self.unit['revision_key'],'accepted_successor':True})
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            with self.assertRaisesRegex(fr.FullReviewError,'requires validated A'): fr.check(self.manifest,self.next)
        (self.next/'adjudications/new.json').unlink()
        with patch.object(fr.batch, '_contextual_done_verified', return_value=True):
            ref = fr.export(self.manifest,self.next,[self.key],self.root/'workset.json',self.root/'scope.json',
            export_id='new-a',lane='A',task_id='new-task',dispatch_id='new-d',workspace_id='w1',parent_agent_id='parent')
        self.producer(ref)
        with patch.object(fr.batch,'_contextual_done_verified',return_value=False):
            with self.assertRaisesRegex(fr.FullReviewError,'DONE_VERIFIED'):
                fr.import_result(self.manifest,self.next,'new-a',self.root/'raw.json',self.root/'binding.json')
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            fr.import_result(self.manifest,self.next,'new-a',self.root/'raw.json',self.root/'binding.json')
            self.assertEqual(fr.check(self.manifest,self.next)['A_effective_complete'],0)
            self.save(self.next/'adjudications/new.json',{'round_id':'test-round','unit_id':self.key,
                'revision_key':self.unit['revision_key'],'accepted_successor':True,'source_verified':True,
                'raw_sha256':{'A':fr.sha(self.raw)},'confirmed':[],'blocking_pending':[],
                'status':'effective-complete','evidence':self.evidence})
            self.assertEqual(fr.check(self.manifest,self.next)['A_effective_complete'],1)

    def test_added_removed_occurrences_conserve_and_do_not_inherit(self):
        self.accepted()
        import copy
        new = copy.deepcopy(self.unit)
        new.update(unit_id='new-unit',guard='new-guard')
        fr.current_units.return_value = ([new],'unrelated-terms')
        req = self.request()
        req['mapping'] = [{'unit_id':self.key,'status':'removed','reason':'host removed occurrence'},
                          {'unit_id':'new-unit','status':'added','reason':'host added occurrence'}]
        req['contexts'] = {'new-unit':dict(self.workset['entries'][0],unit_id='new-unit')}
        self.migrate(req)
        with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
            self.assertEqual(fr.check(self.manifest,self.next)['A_effective_complete'],0)

    def test_language_byte_runtime_closure_requires_own_current_coverage(self):
        from tools.i18nlib import release_candidate as rc
        from tools.i18nlib.config import load_manifest
        from tools.i18nlib.runtime import LuaRuntime
        import zipfile
        spec = self.language_spec('copy')
        req = self.request(language=[spec])
        self.migrate(req)
        ledger = fr.read(self.next/'inventory.json')
        live = fr.validate_current(self.manifest,ledger)
        language = ledger['units'][1]
        key = language['unit_id']
        # Distinct source context supplies a copy literal; closure parses the
        # canonical Lua chain and byte-checks the procedural layer independently.
        candidate = self.root/'.artifacts/i18n/release-candidate/byte-closure'
        engine = candidate/'engine'/rc.ENGINE_LOCALE
        engine.parent.mkdir(parents=True)
        engine.write_text('t("hello", "复制文本")\n',encoding='utf-8')
        (candidate/'addon').mkdir()
        (candidate/'addon/init.lua').write_bytes(b'for_module="tome"\nshort_name="test"\n')
        copy_file = candidate/'copy.txt'
        copy_file.write_text('hello\n复制文本',encoding='utf-8')
        with zipfile.ZipFile(candidate/'tome-test.teaa','w',compression=zipfile.ZIP_STORED) as z:
            z.writestr('init.lua',(candidate/'addon/init.lua').read_bytes())
        self.save(candidate/'candidate.json',{'files':rc.file_manifest(candidate),
            'engine_build_sha256':fr.sha(engine.read_bytes()),'package':'tome-test.teaa','input_hashes':{}})
        runtime = {'key':['hello',None],'kind':'language-bytes','target':'复制文本','args_order':None,'special':None,
            'evidence':self.evidence,'effective_layer':'copy-runtime',
            'layers':[{'origin':'candidate','path':'copy.txt','sha256':fr.sha(copy_file.read_bytes()),
                       'layer':'copy-runtime','language':'zh_hans','target_anchor':{'start':6,'end':len(copy_file.read_bytes())}}]}
        live[self.key]['runtime_key'] = ['hello',None]
        closure = {'round_id':'test-round','inventory_sha256':fr.sha((self.next/'inventory.json').read_bytes()),
            'candidate_path':str(candidate),'candidate_sha256':fr.sha((candidate/'candidate.json').read_bytes()),
            'evidence':self.evidence,'runtime_keys':[runtime],
            'occurrences':[{'unit_id':u['unit_id'],'revision_key':u['revision_key'],'guard':u['guard'],
                'disposition':u['disposition'],'runtime_key':['hello',None],'effective_target':'复制文本','evidence':self.evidence} for u in live.values()],
            'supplements':[{'supplement_id':'source-one','supplement_sha256':fr.sha(fr.canonical(self.supplement)),
                'disposition':'release-required','runtime_key':['hello',None],'review_units':[key],'evidence':self.evidence}],
            'release_readiness':{}}
        for field in ('retained_layers','dynamic_contexts','relations','successors'):
            closure[field] = {'status':'closed','evidence':self.evidence}
        self.save(self.next/'closure.json',closure)
        with patch.object(rc,'input_hashes',return_value={}), patch.object(fr,'LuaRuntime',return_value=LuaRuntime(load_manifest())):
            with self.assertRaisesRegex(fr.FullReviewError,'missing adjudicated current'):
                fr.closure_check(self.manifest,self.next,ledger,live,{'A':{self.key},'B':set()})
            result = fr.closure_check(self.manifest,self.next,ledger,live,{'A':{self.key,key},'B':set()})
            self.assertEqual(result['final_unit_denominator'],2)
            self.assertFalse(result['release_ready'])
            closure['supplements'][0]['review_units'] = [self.key]
            self.save(self.next/'closure.json',closure)
            with self.assertRaisesRegex(fr.FullReviewError,'bound language unit'):
                fr.closure_check(self.manifest,self.next,ledger,live,{'A':{self.key,key},'B':set()})

    def test_duplicate_language_and_unproved_merge_rejected(self):
        spec = self.language_spec('copy')
        twin = dict(spec,language_id='copy-twin')
        with self.assertRaises(fr.FullReviewError): self.migrate(self.request(language=[spec,twin]))
        spec['origins'].append('missing-source')
        with self.assertRaises(fr.FullReviewError): self.migrate(self.request(language=[spec]))


class PositionGuardTests(unittest.TestCase):
    def test_real_loader_insert_remove_retains_unmodified_units_and_special_guard(self):
        from dataclasses import replace
        from tools.i18nlib.config import load_manifest
        import shutil
        original = load_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bridge = root/'tools/lua/load_locale.lua'
            bridge.parent.mkdir(parents=True)
            shutil.copyfile(original.root/'tools/lua/load_locale.lua',bridge)
            manifest = replace(original,root=root,components=(replace(original.component('engine'),translation='engine.lua'),))
            text = 'section "engine/test.lua"\nt("hello", "你好")\nt("%s", "%s", "tformat", {1}, "old")\n'
            path = root/'engine.lua'; path.write_text(text,encoding='utf-8')
            with patch.object(fr.wp1,'terminology_snapshot',return_value='fixed-fixture-terms'):
                before, _ = fr.current_units(manifest)
                path.write_text(text.replace('t("hello"','t("inserted", "新增")\nt("hello"'),encoding='utf-8')
                inserted, _ = fr.current_units(manifest)
                unchanged = {u['unit_id']:u for u in inserted if u['occurrence']['source'] != 'inserted'}
                self.assertEqual(len(unchanged),2)
                for unit in before:
                    now = unchanged[unit['unit_id']]
                    self.assertEqual((unit['guard'],unit['revision_key']),(now['guard'],now['revision_key']))
                    self.assertNotEqual(unit['line'],now['line'])
                path.write_text(text,encoding='utf-8')
                removed, _ = fr.current_units(manifest)
                self.assertEqual([(u['unit_id'],u['guard'],u['revision_key']) for u in before],
                                 [(u['unit_id'],u['guard'],u['revision_key']) for u in removed])
                path.write_text(text.replace(', "old"',', "new"'),encoding='utf-8')
                changed, _ = fr.current_units(manifest)
                self.assertEqual(before[0]['guard'],changed[0]['guard'])
                self.assertEqual(before[1]['revision_key'],changed[1]['revision_key'])
                self.assertNotEqual(before[1]['guard'],changed[1]['guard'])


    def test_real_loader_successor_coverage_survives_insert_and_remove(self):
        from dataclasses import replace
        from tools.i18nlib.config import load_manifest
        import shutil, copy
        fixture = SuccessorTests(methodName='test_unchanged_effective_coverage_survives_without_rewriting_old_raw')
        fixture.setUp()
        try:
            fixture.live_patch.stop()  # All identities/guards below use actual Lua loader.
            original = load_manifest()
            manifest = replace(original,root=fixture.root,
                components=(replace(original.component('engine'),translation='engine.lua'),))
            bridge = fixture.root/'tools/lua/load_locale.lua'
            bridge.parent.mkdir(parents=True)
            shutil.copyfile(original.root/'tools/lua/load_locale.lua',bridge)
            fixture.manifest = manifest
            with patch.object(fr.wp1,'terminology_snapshot',return_value='terms'):
                units, _ = fr.current_units(manifest)
                fixture.unit = units[0]; fixture.key = units[0]['unit_id']
                fixture.row = units[0]['catalog_row']
                fixture.workset['entries'][0]['unit_id'] = fixture.key
                fixture.save(fixture.root/'workset.json',fixture.workset)
                fixture.ledger.update(manifest_sha256=fr.sha(manifest.raw_bytes),units=units)
                fixture.ledger.pop('inventory_identity')
                fixture.ledger['inventory_identity']=fr.sha(fr.canonical(fixture.ledger))
                fixture.save(fixture.directory/'inventory.json',fixture.ledger)
                fixture.accepted()
                path = fixture.root/'engine.lua'; before=path.read_text()
                path.write_text(before.replace('t("hello"','t("inserted", "新增")\nt("hello"'))
                inserted, _ = fr.current_units(manifest)
                req = fixture.request()
                added = next(u for u in inserted if u['unit_id'] != fixture.key)
                req['mapping'].append({'unit_id':added['unit_id'],'status':'added','reason':'controlled loader insertion'})
                req['contexts'][added['unit_id']]=dict(fixture.workset['entries'][0],unit_id=added['unit_id'])
                fixture.migrate(req)
                with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
                    self.assertEqual(fr.check(manifest,fixture.next)['A_effective_complete'],1)
                predecessor = fixture.next
                path.write_text(before)
                req['before_sha256']=fr.sha((predecessor/'inventory.json').read_bytes())
                req['mapping'][-1]['status']='removed'
                del req['contexts'][added['unit_id']]
                request_path=fixture.root/'remove.json';fixture.save(request_path,req)
                last=fixture.root/'after-remove'
                fr.successor(manifest,predecessor,last,request_path)
                with patch.object(fr.batch,'_contextual_done_verified',return_value=True):
                    self.assertEqual(fr.check(manifest,last)['A_effective_complete'],1)
        finally:
            fixture.doCleanups()


class PublicSourceRootTests(unittest.TestCase):
    def test_dlc_inner_root_strips_logical_mount_exactly_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            inner = Path(temporary) / 'tome-ashes-urhrok'
            path = inner / 'data/test.lua'
            path.parent.mkdir(parents=True)
            path.write_bytes(b'public DLC text')
            component = SimpleNamespace(source_repository=None, protected_source=SimpleNamespace(
                visibility='public', mount='tome-ashes-urhrok'))
            manifest = SimpleNamespace(component=lambda name: component)
            spec = {'component': 'ashes-urhrok', 'public_source_path': 'tome-ashes-urhrok/data/test.lua',
                    'sha256': fr.sha(path.read_bytes()), 'inner_root': str(inner)}
            result = fr.source_file(manifest, spec)
            self.assertEqual(result['source_pinning'], 'unpinned')
            self.assertIsNone(result['commit'])
            spec['sha256'] = '0'*64
            with self.assertRaises(fr.FullReviewError):
                fr.source_file(manifest, spec)
            spec['public_source_path'] = 'other/data/test.lua'
            with self.assertRaises(fr.FullReviewError):
                fr.source_file(manifest, spec)


class FixedI18NOracleTests(unittest.TestCase):
    def setUp(self):
        from tools.i18nlib.config import load_manifest
        from tools.i18nlib.runtime import LuaRuntime
        self.runtime = LuaRuntime(load_manifest())

    def replay(self, early, later, queries):
        return fr.i18n_effective(self.runtime,
            [({'layer':'early'}, early.encode()), ({'layer':'later'}, later.encode())], queries)

    def test_actual_pin_tagged_target_replaces_nil_and_unknown_fallback(self):
        rows = self.replay('t("hello","early")', 't("hello","later","some-tag")',
            [{'source':'hello','tag':tag,'method':'_t'} for tag in (None,'unknown','some-tag')])
        for row in rows:
            self.assertEqual(row['target'],'later')
            self.assertEqual(row['effective_layer'],'later')
            self.assertEqual(row['effective_registration'],
                {'layer':'later','ordinal':1,'line':1,'source_tag':'some-tag'})

    def test_actual_pin_null_preserves_nil_args_and_special(self):
        formatted = self.replay('t("%d %d","%d %d","tformat",{2,1})',
            't("%d %d","%d %d","tformat")',
            [{'source':'%d %d','tag':'tformat','method':'string.tformat','arguments':[1,2]}])[0]
        self.assertEqual(formatted['formatted'],'2 1')  # actual string.tformat execution
        rows = self.replay('t("%d %d","%d %d","tformat",{2,1},{mode="old"})',
            't("%d %d","%d %d","tformat")',
            [{'source':'%d %d','tag':'tformat','method':'default_tformat','arguments':[1,2]},
             {'source':'%d %d','tag':'tformat','method':'string.tformat'}])
        self.assertEqual(rows[0]['formatted'],'2 1')  # actual default_tformat execution
        for row in rows:
            self.assertEqual(row['args_order'],[2,1])
            self.assertEqual(row['special'],{'mode':'old'})
            self.assertEqual(row['effective_layer'],'later')

    def test_actual_pin_bucket_clear_changes_another_key(self):
        early = ('t("%d %d","%d %d","tformat",{2,1},{mode="tagged"})\n'
                 't("%d %d","%d %d","new-tag",{1,2},{mode="fallback"})')
        before = self.replay(early,'',
            [{'source':'%d %d','tag':'tformat','method':'default_tformat','arguments':[1,2]}])[0]
        after = self.replay(early,'t("different","different","tformat")',
            [{'source':'%d %d','tag':'tformat','method':'default_tformat','arguments':[1,2]}])[0]
        self.assertEqual(before['formatted'],'2 1')
        self.assertEqual(before['special'],{'mode':'tagged'})
        self.assertEqual(after['formatted'],'1 2')
        self.assertEqual(after['args_order'],[1,2])
        self.assertEqual(after['special'],{'mode':'fallback'})
        # Target still comes from the older tagged registration, not the clearing row.
        self.assertEqual(after['effective_registration']['ordinal'],1)
        self.assertEqual(after['effective_registration']['source_tag'],'tformat')

    def test_missing_source_is_kept_and_query_tag_is_explicit(self):
        rows = self.replay('t("hello","tagged","_t")\nt("hello","fallback","other")','',
            [{'source':'hello','tag':None,'method':'_t'},
             {'source':'hello','tag':'nil','method':'_t'},
             {'source':'missing','tag':None,'method':'_t'},
             {'source':'1','tag':None,'method':'_t'}])
        self.assertEqual(rows[0]['target'],'tagged')
        self.assertEqual(rows[1]['target'],'fallback')
        self.assertEqual(rows[2]['target'],'missing')
        self.assertEqual(rows[2]['effective_layer'],'source-fallback')
        self.assertIsNone(rows[2].get('effective_registration'))
        self.assertEqual(rows[3]['effective_layer'],'source-fallback')

    def test_unsupported_dynamic_semantics_and_wrong_source_hash_fail_closed(self):
        query = [{'source':'hello','tag':None,'method':'_t'}]
        for raw in ('t("hello",os.getenv("LANG"))',
                    'setFlag("tformat_special",true)', 'tc("hello","target")',
                    'locale("en_US")'):
            with self.subTest(raw=raw), self.assertRaises(fr.FullReviewError):
                self.replay(raw,'',query)
        with patch.object(fr.FixedReader,'pinned',return_value=(b'wrong checkout bytes',{})):
            with self.assertRaisesRegex(fr.FullReviewError,'hash mismatch'):
                self.replay('t("hello","target")','',query)
        with self.assertRaises(fr.FullReviewError):
            self.replay('', '', [{'source':'hello','method':'_t'}])

    def test_finite_chain_replays_all_queries_in_one_execution(self):
        source = '\n'.join('t("key%d","value%d","tag")' % (n,n) for n in range(100))
        queries = [{'source':'key%d'%n,'tag':'unknown','method':'_t'} for n in range(100)]
        rows = self.replay(source,'',queries)
        self.assertEqual([row['target'] for row in rows], ['value%d'%n for n in range(100)])


class LoadingOnlyBytesTests(unittest.TestCase):
    def test_pair_reads_each_current_or_inherited_origin_and_rejects_drift(self):
        import copy
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {'unit_id':'one','context':'usage','source_files':[{'sha256':'a'*64}],
                     'b_reasons':[],'b_exemption':'short'}
            refs = []
            for name in ('current','previous'):
                path = root/name/'exports'/name/'workset.json'
                path.parent.mkdir(parents=True)
                raw = fr.canonical({'entries':[entry]})
                path.write_bytes(raw)
                refs.append({'export_id':name,'workset_sha256':fr.sha(raw),'_directory':str(root/name)})
            fr.match_pair(root,refs[0],refs[1],'one')
            for field in ('context','source_files','b_reasons'):
                changed = copy.deepcopy(entry)
                changed[field] = {'context':'other','source_files':[], 'b_reasons':['mechanics']}[field]
                path = root/'previous/exports/previous/workset.json'
                raw = fr.canonical({'entries':[changed]})
                path.write_bytes(raw)
                refs[1]['workset_sha256'] = fr.sha(raw)
                if field == 'b_reasons': fr.match_pair(root,refs[0],refs[1],'one')
                else:
                    with self.assertRaisesRegex(fr.FullReviewError,'neutral source/context'):
                        fr.match_pair(root,refs[0],refs[1],'one')
            path.write_bytes(b'{}')
            with self.assertRaisesRegex(fr.FullReviewError,'origin workset drift'):
                fr.match_pair(root,refs[0],refs[1],'one')

    def test_real_copy_and_conservative_literal_classification(self):
        root = Path(fr.__file__).resolve().parents[2]
        self.assertEqual(fr.loading_literals((root/'engine.copy.lua').read_bytes()), [])
        actual = (root/'mod-tome.copy.lua').read_bytes()
        self.assertEqual(len(actual),16419)
        self.assertIn('华美', ','.join(fr.loading_literals(actual)))
        for raw in (b'setFlag("randart_name_rules", {syllablesStart="Beautiful, Dark"})',
                    b'setFlag("custom", "English")', b'name="Sword"', b'desc=[[English text]]',
                    b't("source", "target")'):
            self.assertTrue(fr.loading_literals(raw))
        for raw in (b'setFlag(flag, value)',b'return compute()',b'while true do end',b'local x=123'):
            with self.assertRaises(fr.FullReviewError): fr.loading_literals(raw)
        self.assertEqual(fr.loading_literals(b'--[[ name="comment" ]]\nsetFlag("ego_always_prefix", false);'),[])

    def test_actual_pinned_retained_and_public_wrapper_bytes_hash_drift(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(['git','init','-q',str(root)],check=True)
            plain = b'forceFontPackage("chinese")\n'
            language = b'setFlag("names", {name="English Sword"})\n'
            (root/'plain.lua').write_bytes(plain)
            (root/'text.lua').write_bytes(language)
            subprocess.run(['git','-C',str(root),'add','plain.lua','text.lua'],check=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                            'commit','-qm','controlled pinned input'],check=True)
            commit = subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
            manifest = SimpleNamespace(root=root,repositories={'addon':SimpleNamespace(commit=commit,visibility='public')},
                repository_path=lambda _:root)
            inner = root/'tome-ashes-urhrok'
            inner.mkdir()
            manifest.component = lambda _:SimpleNamespace(source_repository=None,
                protected_source=SimpleNamespace(visibility='public',mount=inner.name))
            for kind in ('copy','retained-layer','wrapper-addon'):
                for path, raw in [('plain.lua',plain),('text.lua',language)]:
                    with self.subTest(kind=kind,path=path):
                        sup = dict(kind=kind,path=path,component='ashes-urhrok',content=raw.decode(),
                                   commit=commit,sha256=fr.sha(raw))
                        mapping = {'language_literals':[]}
                        if kind == 'wrapper-addon':
                            (inner/path).write_bytes(raw)
                            sup['path'] = inner.name+'/'+path
                            mapping['source_file'] = dict(component='ashes-urhrok',public_source_path=sup['path'],
                                sha256=fr.sha(raw),inner_root=str(inner))
                        bound = fr.loading_bytes(manifest,sup,mapping)
                        self.assertEqual(bound,raw)
                        self.assertEqual(bool(fr.loading_literals(bound)),path=='text.lua')
                        if path == 'text.lua':
                            with self.assertRaisesRegex(fr.FullReviewError,'actual language literals'):
                                fr.validate_loading_only(manifest,sup,mapping)
                        else:
                            fr.validate_loading_only(manifest,sup,mapping)
                        with self.assertRaises(fr.FullReviewError):
                            fr.loading_bytes(manifest,dict(sup,sha256='0'*64),mapping)
                        if kind == 'copy':
                            with self.assertRaises(fr.FullReviewError):
                                fr.loading_bytes(manifest,dict(sup,content='drift'),mapping)
                        if kind == 'retained-layer':
                            (root/path).write_bytes(b'dirty checkout ignored')
                            self.assertEqual(fr.loading_bytes(manifest,sup,mapping),raw)
                            (root/path).write_bytes(raw)
                            with self.assertRaises(fr.FullReviewError):
                                fr.loading_bytes(manifest,dict(sup,commit='0'*40),mapping)
                        if kind == 'wrapper-addon':
                            with self.assertRaises(fr.FullReviewError): fr.loading_bytes(manifest,sup,{})
                            (inner/path).write_bytes(b'drift')
                            with self.assertRaises(fr.FullReviewError): fr.loading_bytes(manifest,sup,mapping)
