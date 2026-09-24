from pathlib import Path
import ast
import copy
import hashlib
import json
import os
import re
import runpy
import sys
import tempfile
import unittest
from contextlib import nullcontext
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
ORCHESTRATION = ROOT / "tools/orchestration"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ORCHESTRATION))

import contextual_lane_manifest
import dispatch_contextual
import dispatch_surface
import review_prompts
import surface_screen_result_check
from i18nlib import production_review_v2_lite_batch as batch


def contract_prompt(relative: str, marker: str) -> str:
    text = (ROOT / relative).read_text(encoding="utf-8")
    tail = text.split(marker, 1)[1]
    match = re.search(r"```text\n(.*?)\n```", tail, re.S)
    if match is None:
        raise AssertionError(f"missing formal prompt after {marker!r}")
    return match.group(1)


class ReviewPromptTests(unittest.TestCase):
    CI = "a" * 64

    def test_formal_templates_are_exactly_the_contract_templates(self):
        self.assertEqual(
            review_prompts.CONTEXTUAL_PROMPT_TEMPLATE,
            contract_prompt(
                "docs/paseo-translation-context-review-v2-contract.md",
                "固定三行 prompt：",
            ),
        )
        self.assertEqual(
            review_prompts.SURFACE_PROMPT_TEMPLATE,
            contract_prompt(
                "docs/paseo-translation-surface-screen-v1-contract.md",
                "固定三行 dispatch prompt",
            ),
        )

    def test_contextual_search_scope_is_bounded(self):
        prompt = review_prompts.build_contextual_prompt(self.CI, '.ai/task/new/CONTEXTUAL-ENVELOPE-final-full.json')
        self.assertIn('禁从 / 或无关目录全盘搜索', prompt)
        self.assertIn('仅限输入指定位置', prompt)
        self.assertIn('可沿调用链查冻结版相关源码', prompt)
        self.assertNotIn('禁从 /', review_prompts.SURFACE_PROMPT_TEMPLATE)

    def test_refreeze_requires_archived_invalid_input_and_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            task = 'old-contextual'
            source = root / 'old-input.json'
            source.write_bytes(b'old frozen envelope')
            state_path = root / 'task/STATE.json'
            state_path.parent.mkdir()
            state = {'task_id': task, 'review_records': [], 'child_dispatches': [
                {'archive_confirmed': True, 'lifecycle': 'archived', 'role': 'REVIEWER',
                 'purpose': 'translation_contextual_v2', 'candidate_identity': 'c' * 64,
                 'input_path': 'task/CONTEXTUAL-ENVELOPE-final-full.json',
                 'output_valid': True}]}
            state_path.write_text(json.dumps(state))
            checkpoint = {'phase': 'deep_ready', 'contextual': [{
                'task_id': task, 'task_state_path': 'task/STATE.json',
                'validator_status': 'prepared', 'output_path': None,
                'candidate_identity': 'c' * 64,
                'input_path': str(source), 'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            }]}
            original = source.read_bytes()
            batch._validate_refreeze_old_refs(root, checkpoint)
            self.assertEqual(source.read_bytes(), original)
            for key, invalid in [('role', 'SCOUT'), ('purpose', 'other'),
                                 ('candidate_identity', 'd' * 64), ('input_path', 'other.json')]:
                old = state['child_dispatches'][0][key]
                state['child_dispatches'][0][key] = invalid
                state_path.write_text(json.dumps(state))
                with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'not fully archived'):
                    batch._validate_refreeze_old_refs(root, checkpoint)
                state['child_dispatches'][0][key] = old
            state['child_dispatches'][0]['archive_confirmed'] = False
            state_path.write_text(json.dumps(state))
            with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'not fully archived'):
                batch._validate_refreeze_old_refs(root, checkpoint)
            state['child_dispatches'][0]['archive_confirmed'] = True
            state['review_records'] = ['accepted-record.json']
            state_path.write_text(json.dumps(state))
            with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'not fully archived'):
                batch._validate_refreeze_old_refs(root, checkpoint)
            self.assertEqual(source.read_bytes(), original)

    def test_refreeze_export_resumes_only_identical_precheckpoint_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint_path = batch.queue.checkpoint_path(root)
            checkpoint_path.parent.mkdir(parents=True)
            old = {'batch_id': 'batch-test', 'phase': 'deep_ready', 'contextual': [{
                'task_id': 'batch-test-contextual-000',
            }]}
            old_raw = batch._checkpoint_bytes(old)
            checkpoint_path.write_bytes(old_raw)
            checkout = root / 'ashes'
            checkout.mkdir()
            workset = root / 'workset.json'
            workset.write_bytes(b'{}')
            run = {'run_index': 0, 'parent_indexes': [0]}
            input_path = checkpoint_path.parent / 'contextual/run-000-refreeze-retry-input.json'
            original_atomic = batch._atomic
            checkpoint_state = old

            def interrupted(path, raw):
                if path == checkpoint_path:
                    raise batch._err('simulated interruption before checkpoint publication')
                original_atomic(path, raw)

            with (mock.patch.object(batch.queue, 'writer_lock', return_value=nullcontext()),
                  mock.patch.object(batch, 'preflight', side_effect=lambda root: copy.deepcopy(checkpoint_state)),
                  mock.patch.object(batch, '_validate_refreeze_old_refs'),
                  mock.patch.object(batch, 'partition_contextual_entries', return_value=[run]),
                  mock.patch.object(batch, '_contextual_payload', return_value={'bounded_context': []}),
                  mock.patch.object(batch.contextual, 'canonical_payload_bytes', return_value=b'payload'),
                  mock.patch('orchestration.build_evidence_pack.validate_workset',
                             return_value=({'source_verification': []}, None)),
                  mock.patch('orchestration.build_evidence_pack.build_source_facts',
                             return_value={0: {'entries': []}})):
                options = {'source_workset': workset, 'source_checkout': checkout,
                           'refreeze_id': 'retry'}
                with mock.patch.object(batch, '_atomic', side_effect=interrupted):
                    with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'simulated interruption'):
                        batch.contextual_export(root, **options)
                frozen_input = input_path.read_bytes()
                self.assertEqual(checkpoint_path.read_bytes(), old_raw)

                self.assertTrue(batch.contextual_export(root, **options)['ok'])
                self.assertEqual(input_path.read_bytes(), frozen_input)
                published = checkpoint_path.read_bytes()
                self.assertEqual(json.loads(checkpoint_path.read_bytes())['contextual'][0]['input_sha256'],
                                 hashlib.sha256(frozen_input).hexdigest())

                checkpoint_path.write_bytes(old_raw)
                input_path.write_bytes(frozen_input + b'drift')
                with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'input differs'):
                    batch.contextual_export(root, **options)
                self.assertEqual(checkpoint_path.read_bytes(), old_raw)
                self.assertEqual(input_path.read_bytes(), frozen_input + b'drift')

                input_path.write_bytes(frozen_input)
                task_dir = root / '.ai/task/batch-test-contextual-000-refreeze-retry'
                task_dir.mkdir(parents=True)
                with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'task already exists'):
                    batch.contextual_export(root, **options)
                self.assertEqual(checkpoint_path.read_bytes(), old_raw)
                task_dir.rmdir()

                input_path.unlink()
                input_path.symlink_to(workset)
                with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'input path is symlink'):
                    batch.contextual_export(root, **options)
                self.assertEqual(checkpoint_path.read_bytes(), old_raw)
                input_path.unlink()
                input_path.write_bytes(frozen_input)
                checkpoint_state = copy.deepcopy(old)
                checkpoint_state['contextual'][0]['task_id'] += '-refreeze-other'
                checkpoint_path.write_bytes(batch._checkpoint_bytes(checkpoint_state))
                with self.assertRaisesRegex(batch.wp1.ProductionReviewError, 'different checkpoint event'):
                    batch.contextual_export(root, **options)
                self.assertEqual(checkpoint_path.read_bytes(), batch._checkpoint_bytes(checkpoint_state))
                self.assertNotEqual(checkpoint_path.read_bytes(), published)

    def test_refreeze_report_conflict_preserves_checkpoint_and_new_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint = root / '.artifacts/i18n/production-review-v2-lite/active-batch.json'
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text('{"batch_id":"batch-test","phase":"deep_ready"}')
            original_checkpoint = checkpoint.read_bytes()
            new_input = root / 'new-input.json'
            new_input.write_bytes(b'existing input sentinel')
            original_input = new_input.read_bytes()
            checkout = root / 'ashes'
            checkout.mkdir()
            report = root / 'report.json'
            report.write_bytes(b'existing report')

            def export_if_called(*args, **kwargs):
                checkpoint.write_bytes(b'changed checkpoint')
                new_input.write_bytes(b'changed input')

            script = ORCHESTRATION / 'stage_contextual.py'
            argv = [str(script), 'batch-test', '--refreeze-id', 'retry',
                    '--source-workset', str(root / 'workset.json'),
                    '--ashes-checkout', str(checkout), '--out', str(report)]
            previous = Path.cwd()
            try:
                os.chdir(root)
                with mock.patch.object(sys, 'argv', argv), mock.patch.object(
                    batch, 'contextual_export', side_effect=export_if_called
                ) as export:
                    with self.assertRaisesRegex(FileExistsError, 'stage report already exists'):
                        runpy.run_path(str(script), run_name='__main__')
                    export.assert_not_called()
            finally:
                os.chdir(previous)
            self.assertEqual(checkpoint.read_bytes(), original_checkpoint)
            self.assertEqual(new_input.read_bytes(), original_input)
            self.assertEqual(report.read_bytes(), b'existing report')

    def test_refreeze_stage_resumes_partial_task_and_report_without_replacing_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch_id, token = 'batch-test', 'retry'
            task = f'{batch_id}-contextual-000-refreeze-{token}'
            checkout = root / 'ashes'
            checkout.mkdir()
            (checkout / 'source.lua').write_text('source')
            workset = root / 'workset.json'
            workset.write_text('{}')
            fact = {'binding': {'source_workset_sha256': hashlib.sha256(workset.read_bytes()).hexdigest()},
                    'fact': {'source_component': 'ashes-urhrok'}}
            context = (f' source_checkout={checkout} (local evidence location; source/commit unpinned)'
                       '\nsource_facts_v1:' + json.dumps(fact))
            envelope = {'candidate_identity': 'c' * 64, 'payload': {
                'ordered_revision_keys': ['one'], 'bounded_context': [{'context': context}]}}
            raw = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
            input_path = root / 'input.json'
            input_path.write_bytes(raw)
            checkpoint = root / '.artifacts/i18n/production-review-v2-lite/active-batch.json'
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text(json.dumps({'batch_id': batch_id, 'phase': 'deep_ready', 'base_commit': 'base',
                'contextual': [{'task_id': task, 'input_path': str(input_path),
                                'input_sha256': hashlib.sha256(raw).hexdigest(),
                                'candidate_identity': 'c' * 64}]}))
            task_dir = root / '.ai/task' / task
            task_dir.mkdir(parents=True)
            candidate = task_dir / 'CONTEXTUAL-ENVELOPE-final-full.json'
            candidate.write_bytes(raw)
            report = root / 'report.json'
            script = ORCHESTRATION / 'stage_contextual.py'
            argv = [str(script), batch_id, '--refreeze-id', token,
                    '--source-workset', str(workset), '--ashes-checkout', str(checkout),
                    '--out', str(report)]
            previous = Path.cwd()
            try:
                os.chdir(root)
                verification = {'component': 'ashes-urhrok', 'public_source_path': 'source.lua',
                                'source_file_sha256': hashlib.sha256(b'source').hexdigest()}
                with mock.patch('orchestration.build_evidence_pack.validate_workset',
                                return_value=({'source_verification': [verification]}, None)):
                    with mock.patch.object(sys, 'argv', argv):
                        runpy.run_path(str(script), run_name='__main__')
                    first_state = (task_dir / 'STATE.json').read_bytes()
                    first_report = report.read_bytes()
                    with mock.patch.object(sys, 'argv', argv):
                        runpy.run_path(str(script), run_name='__main__')
                    self.assertEqual(candidate.read_bytes(), raw)
                    self.assertEqual((task_dir / 'STATE.json').read_bytes(), first_state)
                    self.assertEqual(report.read_bytes(), first_report)
                    self.assertEqual(json.loads(first_report)[0]['task_id'], task)
                    report.unlink()
                    with mock.patch.object(sys, 'argv', argv):
                        runpy.run_path(str(script), run_name='__main__')
                    self.assertEqual(report.read_bytes(), first_report)
                    (task_dir / 'raw.txt').write_text('do not touch')
                    with mock.patch.object(sys, 'argv', argv), self.assertRaisesRegex(ValueError, 'non-stage contents'):
                        runpy.run_path(str(script), run_name='__main__')
                    self.assertEqual(candidate.read_bytes(), raw)
                    (task_dir / 'raw.txt').unlink()
                    for missing in ('--source-workset', '--ashes-checkout'):
                        shortened = argv[:]
                        offset = shortened.index(missing)
                        del shortened[offset:offset + 2]
                        with mock.patch.object(sys, 'argv', shortened), self.assertRaises(SystemExit):
                            runpy.run_path(str(script), run_name='__main__')
                    other_workset = root / 'other-workset.json'
                    other_workset.write_text('{"changed":true}')
                    changed = argv[:]
                    changed[changed.index('--source-workset') + 1] = str(other_workset)
                    with mock.patch.object(sys, 'argv', changed), self.assertRaisesRegex(ValueError, 'workset SHA differs'):
                        runpy.run_path(str(script), run_name='__main__')
                    other_checkout = root / 'other-ashes'
                    other_checkout.mkdir()
                    (other_checkout / 'source.lua').write_text('source')
                    changed = argv[:]
                    changed[changed.index('--ashes-checkout') + 1] = str(other_checkout)
                    with mock.patch.object(sys, 'argv', changed), self.assertRaisesRegex(ValueError, 'checkout differs'):
                        runpy.run_path(str(script), run_name='__main__')
                    state_path = task_dir / 'STATE.json'
                    original_state = json.loads(first_state)
                    for key, value in [('mode', 'implement'), ('review_phase', 'FINAL_REVIEW'),
                                       ('baseline', {'commit': 'other'}), ('workspace_id', 'other'),
                                       ('pending_review_contracts', ['translation_contextual_v2']),
                                       ('cycle', 1), ('child_dispatches', [{'started': True}])]:
                        drifted = copy.deepcopy(original_state)
                        drifted[key] = value
                        state_path.write_text(json.dumps(drifted))
                        with mock.patch.object(sys, 'argv', argv), self.subTest(key=key), self.assertRaisesRegex(ValueError, 'started or drifted'):
                            runpy.run_path(str(script), run_name='__main__')
                    state_path.write_bytes(first_state)
                    timestamp_only = copy.deepcopy(original_state)
                    timestamp_only['updated_at'] = 'later'
                    state_path.write_text(json.dumps(timestamp_only))
                    with mock.patch.object(sys, 'argv', argv):
                        runpy.run_path(str(script), run_name='__main__')
            finally:
                os.chdir(previous)

    def test_dispatch_entrypoints_use_the_shared_builders(self):
        self.assertIs(dispatch_contextual.build_prompt, review_prompts.build_contextual_prompt)
        self.assertIs(dispatch_surface.build_prompt, review_prompts.build_surface_prompt)

        source = (ORCHESTRATION / "dispatch_reviewers.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "review_prompts"
            for alias in node.names
        }
        calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertIn("build_surface_prompt", imports)
        self.assertIn("build_surface_prompt", calls)
        self.assertNotIn("candidate_identity=<candidate_identity>", source)

    def test_three_lines_and_longest_legal_actual_paths_fit(self):
        task = "t" * 128
        dispatch = "d" * 32
        cases = (
            (
                review_prompts.build_contextual_prompt,
                f".ai/task/{task}/CONTEXTUAL-ENVELOPE-{dispatch}.json",
            ),
            (
                review_prompts.build_surface_prompt,
                f".ai/task/{task}/SURFACE-SCREEN-ENVELOPE-{dispatch}.json",
            ),
        )
        for builder, path in cases:
            with self.subTest(builder=builder.__name__):
                prompt = builder(self.CI, path)
                self.assertEqual(len(prompt.splitlines()), 3)
                self.assertLessEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)
                self.assertIn(path, prompt)

        real_consumers = (
            (contextual_lane_manifest.render_dispatch_prompt, cases[0][1]),
            (surface_screen_result_check.render_dispatch_prompt, cases[1][1]),
        )
        for renderer, path in real_consumers:
            with self.subTest(renderer=renderer.__module__):
                prompt = renderer(self.CI, path)
                self.assertEqual(len(prompt.splitlines()), 3)
                self.assertLessEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)

    def test_over_limit_and_invalid_identity_fail_closed(self):
        with self.assertRaises(review_prompts.PromptError):
            review_prompts.build_surface_prompt(self.CI, "x" * 801)
        with self.assertRaises(review_prompts.PromptError):
            review_prompts.build_contextual_prompt("not-a-hash", "input.json")

        with self.assertRaises(contextual_lane_manifest.result_check.ContractError):
            contextual_lane_manifest.render_dispatch_prompt(self.CI, "x" * 801)
        with self.assertRaises(surface_screen_result_check.ContractError):
            surface_screen_result_check.render_dispatch_prompt(self.CI, "x" * 801)

    def test_exact_utf8_byte_boundary(self):
        builders = (
            review_prompts.build_contextual_prompt,
            review_prompts.build_surface_prompt,
        )
        for builder in builders:
            one_byte_path_size = len(builder(self.CI, "x").encode("utf-8"))
            path_size = review_prompts.MAX_PROMPT_BYTES - one_byte_path_size + 1
            with self.subTest(builder=builder.__name__):
                prompt = builder(self.CI, "x" * path_size)
                self.assertEqual(len(prompt.encode("utf-8")), review_prompts.MAX_PROMPT_BYTES)
                with self.assertRaises(review_prompts.PromptError):
                    builder(self.CI, "x" * (path_size + 1))

    def test_every_splitlines_separator_is_rejected_by_all_public_renderers(self):
        separators = ("\n", "\r", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")
        renderers = (
            (review_prompts.build_contextual_prompt, review_prompts.PromptError),
            (review_prompts.build_surface_prompt, review_prompts.PromptError),
            (contextual_lane_manifest.render_dispatch_prompt, contextual_lane_manifest.result_check.ContractError),
            (surface_screen_result_check.render_dispatch_prompt, surface_screen_result_check.ContractError),
        )
        for separator in separators:
            self.assertGreater(len(f"before{separator}after".splitlines()), 1)
            for renderer, error in renderers:
                with self.subTest(separator=ascii(separator), renderer=renderer.__module__):
                    with self.assertRaises(error):
                        renderer(self.CI, f"before{separator}after")

    def test_real_consumers_share_templates_without_changing_replay_bindings(self):
        contextual_path = ".ai/task/legacy-task/CONTEXTUAL-ENVELOPE-legacy-dispatch.json"
        surface_path = ".ai/task/legacy-task/SURFACE-SCREEN-ENVELOPE-legacy-dispatch.json"
        self.assertIs(contextual_lane_manifest.PROMPT_TEMPLATE, review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIs(surface_screen_result_check.PROMPT_TEMPLATE, review_prompts.SURFACE_PROMPT_TEMPLATE)
        self.assertEqual(
            contextual_lane_manifest.render_dispatch_prompt(self.CI, contextual_path),
            review_prompts.build_contextual_prompt(self.CI, contextual_path),
        )
        self.assertEqual(
            surface_screen_result_check.render_dispatch_prompt(self.CI, surface_path),
            review_prompts.build_surface_prompt(self.CI, surface_path),
        )

    def test_role_and_prompts_preserve_the_source_permission_difference(self):
        role = (ROOT / ".ai/roles/reviewer.md").read_text(encoding="utf-8")
        contextual = (ROOT / "docs/paseo-translation-context-review-v2-contract.md").read_text(encoding="utf-8")
        surface = (ROOT / "docs/paseo-translation-surface-screen-v1-contract.md").read_text(encoding="utf-8")
        self.assertIn("文件、行号和 hash 只证明来源，不扩大读取权限", role)
        self.assertIn("surface 不得据此补查源码", role)
        self.assertIn("仅可沿调用链补查冻结版本", role)
        self.assertIn("唯一可用的译文输入", contextual)
        self.assertIn("source_facts_v1.fact.terminology", contextual)
        self.assertIn("常是摘要", contextual)
        self.assertIn("不追溯改写已冻结的 prompt、candidate/hash", contextual)
        self.assertIn("唯一可用的译文", surface)
        self.assertIn("只是摘要或 hash", surface)
        self.assertIn("不自动构成译文缺陷", surface)
        self.assertIn("surface 不得借引用、provenance 或完整契约增加源码调查", surface)
        self.assertIn("不追溯改写已冻结的 prompt、candidate/hash", surface)
        self.assertIn("完整 docs/paseo-translation-context-review-v2-contract.md", review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIn("可沿调用链查冻结版相关源码", review_prompts.CONTEXTUAL_PROMPT_TEMPLATE)
        self.assertIn("完整 docs/paseo-translation-surface-screen-v1-contract.md", review_prompts.SURFACE_PROMPT_TEMPLATE)
        self.assertIn("禁补查源码", review_prompts.SURFACE_PROMPT_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
