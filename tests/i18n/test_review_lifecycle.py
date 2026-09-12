from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/orchestration'))
sys.path.insert(0, str(ROOT / 'tools'))
import review_lifecycle as life
import close_review_tasks as close
import dispatch_surface
import dispatch_contextual
import ai_state_check
from tests.i18n.test_surface_screen_result_check import ordered_payload


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(life.surface.canonical_bytes(value))


class FakeTransport:
    def __init__(self, test, row, raw=None, *, archive_error=False, confirms=True, crash=False):
        self.test, self.row, self.raw = test, row, raw
        self.archive_error, self.confirms, self.crash = archive_error, confirms, crash
        self.archived = False
        self.calls = []

    def status(self, key):
        self.calls.append('status')
        if not self.archived and self.row.get('native_provenance'):
            return deepcopy(self.row['terminal_capture'])  # preserve verified native identity in this fixture
        return self.test.capture(self.row, 'closed' if self.archived else 'idle')

    def terminal_bytes(self, key):
        self.calls.append('raw')
        return self.raw if self.raw is not None else self.test.raw(self.row)

    def archive(self, key):
        self.calls.append('archive')
        # Read durable journal AND STATE at the actual mutation boundary.
        disk = life.Journal(self.test.j.path, root=self.test.root).get(key)
        self.test.assertGreater(disk['archive_attempts_started'], 0)
        state = life.read(self.test.root / '.ai/task' / self.row['task_id'] / 'STATE.json')
        child = next(c for c in state['child_dispatches'] if c['dispatch_id'] == self.row['dispatch_id'])
        self.test.assertEqual(child['archive_attempts_started'], disk['archive_attempts_started'])
        self.test.assertFalse(child['archive_confirmed'])
        self.archived = self.confirms
        if self.crash:
            raise KeyboardInterrupt('simulated process crash after archive')
        if self.archive_error:
            raise RuntimeError('already archived')


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='review-lifecycle-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.j = life.Journal(self.root / 'journal.json', root=self.root)
        self.parent, self.ws = 'parent', 'workspace'
        self.selection = dict(provider='test/model', thinkingOptionId='xhigh', modeId='auto')
        self.profiles = self.root / 'profiles.json'
        write(self.profiles, {'profiles': [{'id': 'test', 'notes': 'fixture only'}]})
        # No new test can accidentally talk to a daemon.
        self.no_paseo = patch.object(life._orch, 'paseo', side_effect=AssertionError('real Paseo forbidden'))
        self.no_paseo.start()
        self.addCleanup(self.no_paseo.stop)

    def state(self, task, purpose):
        value = dict(schema_version=5, task_id=task, mode='review_only', state='REVIEW',
                     change_class='translation_workflow' if purpose == life.SURFACE else 'standard',
                     review_phase='REVIEW', cycle=0, max_cycles=3, workspace_id=self.ws,
                     orchestrator_agent_id=self.parent, orchestration_transport='mcp',
                     review_contracts=[purpose], pending_review_contracts=[], completed_review_contracts=[],
                     child_dispatches=[], review_records=[], senior_review_records=[],
                     deferred_findings=[], open_accepted_findings=[])
        write(self.root / '.ai/task' / task / 'STATE.json', value)

    def contextual(self, *, retry=None):
        task = 'context-task'
        if retry is None:
            self.state(task, life.CONTEXTUAL)
        payload = dict(contract=life.CONTEXTUAL, ordered_revision_keys=['a', 'b'],
                       translation_snapshot=[dict(revision_key=k, source='source', target='target') for k in ('a', 'b')],
                       fixed_source_identity='commit:' + '1' * 40, terminology_snapshot='terms',
                       bounded_context=[dict(revision_key=k, context='fixed context') for k in ('a', 'b')],
                       rendered_briefing='fixture review only')
        ci = life.digest(life.surface.canonical_bytes(payload))
        ip = f'.ai/task/{task}/CONTEXTUAL-ENVELOPE-final-full.json'
        write(self.root / ip, dict(candidate_identity=ci, payload=payload))
        spec = dict(task_id=task, dispatch_id='full-1' if retry is None else 'full-2', candidate_identity=ci, input_path=ip)
        if retry:
            spec.update(attempt=2, retry_of=retry)
        return [spec]

    def surface(self, *, count=8, attempt=1):
        task = 'surface-task'
        if attempt == 1:
            self.state(task, life.SURFACE)
        payload = ordered_payload(count)
        write(self.root / f'.ai/task/{task}/SURFACE-SCREEN-INPUT-DRAFT.json', payload)
        if count <= 3:
            did = 'full-1'
            ip = f'.ai/task/{task}/SURFACE-SCREEN-ENVELOPE-{did}.json'
            ci = life.digest(life.surface.canonical_bytes(payload))
            write(self.root / ip, dict(candidate_identity=ci, payload=payload))
            return [dict(task_id=task, dispatch_id=did, candidate_identity=ci, input_path=ip, review_kind='full')]
        g, gp, envs = life.manifests.build_group(payload, task_id=task, group_id=f'group-{attempt}',
                           review_phase='REVIEW', cycle=0, attempt=attempt,
                           dispatch_ids=[f'lane-{attempt}-{n}' for n in range(1, 5)])
        write(self.root / gp, g)
        for ip, env in envs:
            write(self.root / ip, env)
        return [dict(lane, task_id=task, review_kind='lane', group_manifest_path=gp) for lane in g['payload']['lanes']]

    def prepare(self, specs, purpose=life.CONTEXTUAL):
        prompt = dispatch_contextual.build_prompt if purpose == life.CONTEXTUAL else dispatch_surface.build_prompt
        return self.j.prepare(specs, purpose, self.parent, self.ws, prompt, self.selection)

    def capture(self, row, status='running'):
        s = dict(id=row.get('agent_id') or 'agent-' + row['dispatch_id'], workspaceId=self.ws,
                 cwd=str(self.root), labels=deepcopy(row['labels']), status=status,
                 attentionReason='finished' if status == 'idle' else None,
                 attentionTimestamp='2026-09-12T01:01:00Z' if status == 'idle' else None,
                 provider='actual-provider', model='actual-model', currentModeId=None,
                 activeTurn=dict(startedAt='2026-09-12T01:00:00Z', turnId='turn') if status == 'running' else None)
        if status == 'closed':
            del s['activeTurn']  # actual archived MCP responses omit this field
            s['archivedAt'] = '2026-09-12T01:02:00Z'
        return dict(status=status, snapshot=s)

    def bind(self, specs):
        for spec in specs:
            row = self.j.get(self.j.key(spec))
            self.j.create_intent(self.j.key(row), self.profiles)
            self.j.bind(self.j.key(row), self.capture(row))
        return [self.j.get(self.j.key(s)) for s in specs]

    def raw(self, row):
        env = life.read(self.root / row['input_path'])
        result = dict(contract=row['purpose'], candidate_identity=row['candidate_identity'])
        if row['purpose'] == life.SURFACE:
            result['results'] = [dict(entry_revision_identity=e['entry_revision_identity'], verdict='OK') for e in env['payload']['entries']]
        else:
            result['verdicts'] = [dict(revision_key=k, verdict='OK') for k in env['payload']['ordered_revision_keys']]
        return life.surface.canonical_bytes(result)

    def finish(self, row, **kwargs):
        t = FakeTransport(self, row, **kwargs)
        self.j.harvest_and_archive(self.j.key(row), t, self.root / 'raw', notified=True)
        return t

    def test_full_contextual_real_consumer_and_idempotent_publication(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        result = close.publish(self.j, [self.j.key(row)], self.root / 'import')
        self.assertEqual(result.outcome, 'DONE_VERIFIED')
        result = close.publish(self.j, [self.j.key(row)], self.root / 'import')
        self.assertEqual(result.exit_code, 0)
        state = life.read(self.root / '.ai/task/context-task/STATE.json')
        self.assertEqual(len(state['child_dispatches']), 1)
        self.assertNotIn('runtime_observation', life.read(self.root / state['review_records'][0]))

    def test_four_lane_real_consumer(self):
        specs = self.surface()
        recipes = self.prepare(specs, life.SURFACE)
        self.assertEqual([r['labels']['lane_index'] for r in recipes], ['1', '2', '3', '4'])
        self.assertEqual(len({r['labels']['lane_group_identity'] for r in recipes}), 1)
        rows = self.bind(specs)
        for row in rows:
            self.finish(row)
        result = close.publish(self.j, [self.j.key(r) for r in rows], self.root / 'import')
        self.assertEqual(result.outcome, 'DONE_VERIFIED')
        state = life.read(self.root / '.ai/task/surface-task/STATE.json')
        self.assertEqual(len(state['review_records']), 4)
        self.assertEqual(ai_state_check.check_state(self.root / '.ai/task/surface-task/STATE.json',
                                                  workspace_root=self.root).exit_code, 0)

    def test_small_surface_full_real_consumer(self):
        specs = self.surface(count=2)
        self.prepare(specs, life.SURFACE)
        row, = self.bind(specs)
        self.finish(row)
        self.assertEqual(close.publish(self.j, [self.j.key(row)], self.root / 'import').exit_code, 0)

    def test_all_inputs_checked_before_any_preparation(self):
        specs = self.surface()
        (self.root / specs[-1]['input_path']).write_bytes(b'invalid')
        with self.assertRaises((life.contextual.ContractError, life.surface.ContractError)):
            self.prepare(specs, life.SURFACE)
        self.assertFalse(self.j.path.exists())

    def test_partial_stage_rejected_at_prepare_and_publish(self):
        specs = self.surface()
        with self.assertRaisesRegex(life.LifecycleError, 'partial'):
            self.prepare(specs[:3], life.SURFACE)
        self.prepare(specs, life.SURFACE)
        rows = self.bind(specs)
        for row in rows[:3]:
            self.finish(row)
        for keys in ([self.j.key(r) for r in rows[:3]], [self.j.key(r) for r in rows]):
            with self.assertRaises(life.LifecycleError):
                close.publish(self.j, keys, self.root / 'import')
        self.assertFalse((self.root / '.ai/reviews/surface-task').exists())
        self.assertEqual(life.read(self.root / '.ai/task/surface-task/STATE.json')['state'], 'REVIEW')

    def test_strict_output_failures_preserve_exact_raw(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        valid = self.raw(row)
        parsed = json.loads(valid)
        variants = [b' ' + valid, valid + b'\n', b'```json\n' + valid + b'\n```',
                    b'intro\n' + valid, valid + b'trailer', b'\xff' + valid,
                    valid.replace(row['candidate_identity'].encode(), b'f' * 64)]
        for rows in (parsed['verdicts'][::-1], parsed['verdicts'][:1], parsed['verdicts'] + [parsed['verdicts'][0]]):
            variants.append(life.surface.canonical_bytes(dict(parsed, verdicts=rows)))
        for index, raw in enumerate(variants):
            with self.subTest(index=index):
                original = deepcopy(row)
                out = self.root / f'bad-{index}'
                self.assertFalse(self.j.harvest(self.j.key(row), self.capture(row, 'idle'), raw, out, notified=True))
                self.assertEqual((self.root / row['raw_output_path']).read_bytes(), raw)
                self.assertIn('validation_error', row)
                row.clear()
                row.update(original)
        self.j.save()

    def test_first_live_presence_and_idempotence(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        original = deepcopy(row['runtime_observation'])
        self.assertEqual(original['thinking'], {'presence': 'missing'})
        self.assertEqual(original['mode'], {'presence': 'present', 'value': None})
        changed = self.capture(row)
        changed['snapshot']['model'] = 'different-model'
        self.j.bind(self.j.key(row), changed)
        self.assertEqual(original, row['runtime_observation'])
        self.assertEqual(row['first_live_capture']['snapshot']['model'], 'actual-model')

    def test_invalid_live_identity_never_binds(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        self.j.create_intent(self.j.key(row), self.profiles)
        for field, value in [('id', self.parent), ('cwd', '/wrong'), ('workspaceId', 'wrong'), ('labels', {})]:
            cap = self.capture(row)
            cap['snapshot'][field] = value
            with self.subTest(field=field), self.assertRaises(life.LifecycleError):
                self.j.bind(self.j.key(row), cap)
            self.assertNotIn('runtime_observation', row)
        cap = self.capture(row)
        del cap['snapshot']['activeTurn']
        with self.assertRaisesRegex(life.LifecycleError, 'activeTurn'):
            self.j.bind(self.j.key(row), cap)
        with self.assertRaises(life.LifecycleError):
            self.j.bind(self.j.key(row), {'Id': 'cli-id', 'Provider': 'test'})

    def test_duplicate_agent_ids_rejected(self):
        specs = self.surface()
        self.prepare(specs, life.SURFACE)
        first = self.bind(specs[:1])[0]
        second = self.j.get(self.j.key(specs[1]))
        self.j.create_intent(self.j.key(second), self.profiles)
        cap = self.capture(second)
        cap['snapshot']['id'] = first['agent_id']
        with self.assertRaisesRegex(life.LifecycleError, 'duplicate agent'):
            self.j.bind(self.j.key(second), cap)

    def test_ambiguous_creation_no_blind_retry(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        self.j.create_intent(self.j.key(row), self.profiles)
        with self.assertRaisesRegex(life.LifecycleError, 'ambiguous create'):
            self.prepare(specs)
        with self.assertRaises(life.LifecycleError):
            self.j.create_intent(self.j.key(row), self.profiles)
        self.j.bind(self.j.key(row), self.capture(row))
        self.assertEqual(self.prepare(specs), [])

    def test_idle_alone_or_missing_notification_not_terminal(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        cap = self.capture(row, 'idle')
        for field in ('activeTurn', 'attentionReason', 'attentionTimestamp'):
            broken = deepcopy(cap)
            del broken['snapshot'][field]
            with self.subTest(field=field), self.assertRaises(life.LifecycleError):
                self.j.harvest(self.j.key(row), broken, self.raw(row), self.root / 'raw', notified=True)
        cap['snapshot']['attentionReason'] = None
        with self.assertRaises(life.LifecycleError):
            self.j.harvest(self.j.key(row), cap, self.raw(row), self.root / 'raw', notified=True)
        with self.assertRaises(life.LifecycleError):
            self.j.harvest_and_archive(self.j.key(row), FakeTransport(self, row), self.root / 'raw', notified=False)
        self.assertFalse((self.root / 'raw').exists())

    def test_archive_error_with_positive_readback_is_success(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row, archive_error=True)
        self.assertTrue(row['archive_confirmed'])
        self.assertEqual(row['archive_attempts_started'], 1)

    def test_archive_zero_return_without_readback_is_failure_and_bounded(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        transport = FakeTransport(self, row, confirms=False)
        for attempt in (1, 2):
            with self.assertRaisesRegex(life.LifecycleError, 'readback not confirmed'):
                self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True)
            self.assertEqual(row['archive_attempts_started'], attempt)
        with self.assertRaisesRegex(life.LifecycleError, 'budget exhausted'):
            self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True)
        self.assertEqual(transport.calls.count('archive'), 2)
        self.assertFalse(row['archive_confirmed'])

    def test_archive_crash_recovery_reads_before_retry(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        transport = FakeTransport(self, row, crash=True)
        with self.assertRaises(KeyboardInterrupt):
            self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True)
        self.j = life.Journal(self.j.path, root=self.root)
        self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True)
        self.assertEqual(transport.calls.count('archive'), 1)
        self.assertTrue(self.j.rows[0]['archive_confirmed'])

    def test_invalid_attempt_archived_before_exact_full_retry(self):
        specs = self.contextual()
        self.prepare(specs)
        old, = self.bind(specs)
        self.finish(old, raw=b'not a result')
        specs2 = self.contextual(retry=self.j.key(old))
        self.prepare(specs2)
        row, = self.bind(specs2)
        self.assertNotEqual(row['dispatch_id'], old['dispatch_id'])
        self.assertNotEqual(row['agent_id'], old['agent_id'])
        self.assertEqual(row['input_sha256'], old['input_sha256'])
        self.finish(row)
        self.assertEqual(close.publish(self.j, [self.j.key(row)], self.root / 'import').exit_code, 0)
        state = life.read(self.root / '.ai/task/context-task/STATE.json')
        self.assertEqual(len(state['child_dispatches']), 2)
        self.assertEqual(state['review_records'], ['.ai/reviews/context-task/full-2.json'])
        self.assertEqual((self.root / old['raw_output_path']).read_bytes(), b'not a result')

    def test_unconfirmed_archive_blocks_retry(self):
        specs = self.contextual()
        self.prepare(specs)
        old, = self.bind(specs)
        with self.assertRaises(life.LifecycleError):
            self.finish(old, raw=b'bad', confirms=False)
        with self.assertRaisesRegex(life.LifecycleError, 'archive all'):
            self.prepare(self.contextual(retry=self.j.key(old)))

    def test_retry_input_drift_is_rejected(self):
        specs = self.contextual()
        self.prepare(specs)
        old, = self.bind(specs)
        self.finish(old, raw=b'bad')
        nextspec = self.contextual(retry=self.j.key(old))
        env = life.read(self.root / nextspec[0]['input_path'])
        env['payload']['bounded_context'][0]['context'] = 'new context'
        env['candidate_identity'] = life.digest(life.surface.canonical_bytes(env['payload']))
        write(self.root / nextspec[0]['input_path'], env)
        nextspec[0]['candidate_identity'] = env['candidate_identity']
        with self.assertRaisesRegex(life.LifecycleError, 'fresh retry changed'):
            self.prepare(nextspec)

    def test_surface_failed_group_archives_and_fresh_whole_group(self):
        specs = self.surface()
        self.prepare(specs, life.SURFACE)
        rows = self.bind(specs)
        for index, row in enumerate(rows):
            self.finish(row, raw=b'bad' if index == 0 else None)
        with self.assertRaises(life.LifecycleError):
            close.publish(self.j, [self.j.key(r) for r in rows], self.root / 'import')
        specs2 = self.surface(attempt=2)
        self.prepare(specs2, life.SURFACE)
        rows2 = self.bind(specs2)
        for row in rows2:
            self.finish(row)
        self.assertEqual(close.publish(self.j, [self.j.key(r) for r in rows2], self.root / 'import').exit_code, 0)
        state = life.read(self.root / '.ai/task/surface-task/STATE.json')
        self.assertEqual(len(state['child_dispatches']), 8)
        self.assertEqual(len(state['review_records']), 4)

    def test_failed_consumer_does_not_publish_records_or_done(self):
        specs = self.surface(count=2)
        self.prepare(specs, life.SURFACE)
        row, = self.bind(specs)
        self.finish(row)
        draft = self.root / '.ai/task/surface-task/SURFACE-SCREEN-INPUT-DRAFT.json'
        draft.write_bytes(b'{}')
        with self.assertRaisesRegex(life.LifecycleError, 'consumer rejected'):
            close.publish(self.j, [self.j.key(row)], self.root / 'import')
        self.assertFalse((self.root / '.ai/reviews/surface-task').exists())
        self.assertEqual(life.read(self.root / '.ai/task/surface-task/STATE.json')['state'], 'REVIEW')

    def test_repeated_harvest_does_not_replace_raw(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        with self.assertRaisesRegex(life.LifecycleError, 'immutable artifact'):
            self.j.harvest(self.j.key(row), self.capture(row, 'idle'), b'changed', self.root / 'raw', notified=True)
        self.assertTrue(row['archive_confirmed'])

    def test_prepare_and_mirror_recovery_idempotent(self):
        specs = self.contextual()
        self.prepare(specs)
        self.prepare(specs)
        row, = self.bind(specs)
        statepath = self.root / '.ai/task/context-task/STATE.json'
        state = life.read(statepath)
        state['child_dispatches'] = []
        write(statepath, state)
        self.j = life.Journal(self.j.path, root=self.root)
        self.j.save()
        self.assertEqual(len(life.read(statepath)['child_dispatches']), 1)
        self.assertEqual(len(self.j.rows), 1)

    def test_timing_unions_do_not_sum_parallel_models(self):
        specs = self.surface()
        self.prepare(specs, life.SURFACE)
        for row in self.bind(specs):
            self.finish(row)
        report = self.j.timing_report()
        self.assertEqual(report['union_seconds_by_category']['model_window'], 60)
        self.assertEqual({i['category'] for i in report['intervals']},
                         {'tool_call', 'harvest_validation', 'archive_confirmation', 'model_window', 'orchestration_gap'})
        self.assertTrue(all(i['elapsed_s'] >= 0 for i in report['intervals'] if 'elapsed_s' in i))

    def test_scope_rejection_preserves_strict_raw_and_allows_retry(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        evidence = self.root / 'scope-audit.json'
        write(evidence, {'observed_read': 'outside frozen input'})
        original = (self.root / row['raw_output_path']).read_bytes()
        self.j.reject(self.j.key(row), 'read outside frozen references', evidence)
        self.assertFalse(row['output_valid'])
        self.assertEqual((self.root / row['raw_output_path']).read_bytes(), original)
        self.prepare(self.contextual(retry=self.j.key(row)))
        self.assertEqual(len(self.j.rows), 2)

    def test_transport_output_failure_is_recoverable_without_archive(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        transport = FakeTransport(self, row)
        with patch.object(transport, 'terminal_bytes', side_effect=RuntimeError('transport failed')):
            self.assertFalse(self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True))
        self.assertNotIn('output_valid', row)
        self.assertNotIn('raw_output_path', row)
        self.assertFalse(row['archive_confirmed'])
        self.assertEqual(row['terminal_fetch_errors'][0]['error'], 'transport failed')
        self.assertNotIn('archive', transport.calls)
        self.assertTrue(self.j.harvest_and_archive(self.j.key(row), transport, self.root / 'raw', notified=True))
        self.assertTrue(row['archive_confirmed'])
        self.assertEqual(len(row['terminal_fetch_errors']), 1)

    def test_archive_exhaustion_wait_and_readonly_recovery(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        t = FakeTransport(self, row, confirms=False)
        for _ in range(2):
            with self.assertRaises(life.LifecycleError):
                self.j.harvest_and_archive(self.j.key(row), t, self.root / 'raw', notified=True)
        path = self.root / '.ai/task/context-task/STATE.json'
        self.assertEqual(life.read(path)['state'], 'WAIT_USER')
        self.assertEqual(life.read(path)['wait'], {'reason': 'archive_pending', 'resume_state': 'REVIEW'})
        self.j.save()
        self.assertEqual(life.read(path)['wait']['resume_state'], 'REVIEW')
        self.assertNotIn('resume_state', life.read(path))
        t.archived = True
        self.j.harvest_and_archive(self.j.key(row), t, self.root / 'raw', notified=True)
        self.assertEqual(t.calls.count('archive'), 2)
        self.assertEqual(life.read(path)['state'], 'REVIEW')

    def test_cli_emit_record_and_live_capture_are_connected(self):
        specs = self.surface(count=2)
        plan = self.root / 'plan.json'
        emit = self.root / 'emit.json'
        write(plan, {'surface-task': {'lanes': specs}})
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root),
                   PASEO_AGENT_ID=self.parent, TOME_PASEO_WORKSPACE=self.ws)
        cmd = [sys.executable, '-B', str(ROOT / 'tools/orchestration/dispatch_surface.py'),
               str(plan), str(self.j.path)]
        result = subprocess.run(cmd + ['--emit', str(emit)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(life.read(emit)), 1)
        self.j = life.Journal(self.j.path, root=self.root)
        row = self.j.rows[0]
        self.j.create_intent(self.j.key(row), self.profiles)
        ids = self.root / 'ids.json'
        write(ids, {self.j.key(row): 'created-agent'})
        result = subprocess.run(cmd + ['--record', str(ids)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.j = life.Journal(self.j.path, root=self.root)
        row = self.j.rows[0]
        self.assertEqual(row['status'], 'created')
        live = self.root / 'live.json'
        write(live, {self.j.key(row): self.capture(row)})
        result = subprocess.run(cmd + ['--live', str(live)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(life.Journal(self.j.path, root=self.root).rows[0]['status'], 'dispatched')
        terminal = self.root / 'terminal.json'
        raw = self.root / 'terminal.raw'
        captures = self.root / 'captures.json'
        write(terminal, self.capture(row, 'idle'))
        raw.write_bytes(self.raw(row))
        write(captures, {self.j.key(row): {'terminal_path': str(terminal), 'raw_path': str(raw)}})
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/orchestration/harvest_reviews.py'),
                                 str(self.j.path), str(self.root / 'raw'), '--captures', str(captures),
                                 '--notified'], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        lifecycle_cmd = [sys.executable, '-B', str(ROOT / 'tools/orchestration/review_lifecycle.py')]
        result = subprocess.run(lifecycle_cmd + ['archive-intent', str(self.j.path), self.j.key(row),
                                                '--capture', str(terminal)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        archived = self.root / 'archived.json'
        write(archived, self.capture(row, 'closed'))
        result = subprocess.run(lifecycle_cmd + ['archive-confirm', str(self.j.path), self.j.key(row),
                                                '--capture', str(archived)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/orchestration/close_review_tasks.py'),
                                 'surface', str(plan), str(self.j.path), str(self.root / 'import')],
                                env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b'DONE_VERIFIED', result.stdout)

    def test_cli_no_complete_transport_fails_before_create(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/orchestration/dispatch_contextual.py'),
                                 'unused-plan', str(self.j.path)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b'no agent created', result.stderr)
        self.assertFalse(self.j.path.exists())

    def test_original_symlink_cannot_publish_done(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        envelope = self.root / row['input_path']
        real = envelope.with_name('real.json')
        envelope.rename(real)
        envelope.symlink_to(real.name)
        with self.assertRaisesRegex(life.LifecycleError, 'ordinary file'):
            close.publish(self.j, [self.j.key(row)], self.root / 'import')
        with self.assertRaises(ai_state_check.InputError):
            ai_state_check._ordinary_workspace_file(row['input_path'], 'envelope', root=self.root)
        self.assertEqual(life.read(self.root / '.ai/task/context-task/STATE.json')['state'], 'REVIEW')
        self.assertFalse((self.root / '.ai/reviews/context-task').exists())

    def test_original_output_symlink_cannot_publish(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        target = self.root / '.ai/reviews/context-task/raw-full-1.txt'
        target.parent.mkdir(parents=True)
        actual = target.with_name('actual.txt')
        actual.write_bytes(self.raw(row))
        target.symlink_to(actual.name)
        with self.assertRaises(ai_state_check.InputError):
            close.publish(self.j, [self.j.key(row)], self.root / 'import')
        self.assertEqual(life.read(self.root / '.ai/task/context-task/STATE.json')['state'], 'REVIEW')

    def test_interrupted_validation_reloads_saved_raw_without_refetch(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        key = self.j.key(row)
        save = self.j.save
        def crash():
            save()
            raise KeyboardInterrupt('after pending raw saved')
        with patch.object(self.j, 'save', side_effect=crash):
            with self.assertRaises(KeyboardInterrupt):
                self.j.harvest(key, self.capture(row, 'idle'), self.raw(row), self.root / 'raw', notified=True)
        self.j = life.Journal(self.j.path, root=self.root)
        row = self.j.get(key)
        self.assertEqual(row['validation_state'], 'pending')
        self.assertNotIn('output_valid', row)
        with self.assertRaisesRegex(life.LifecycleError, 'completed validation'):
            self.j.archive_intent(key, self.capture(row, 'idle'))
        transport = FakeTransport(self, row)
        with patch.object(transport, 'terminal_bytes', side_effect=AssertionError('must use saved raw')):
            self.assertTrue(self.j.harvest_and_archive(key, transport, self.root / 'raw', notified=True))
        self.assertEqual(row['validation_state'], 'completed')

    def test_actual_validation_failure_is_not_revalidated(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        key = self.j.key(row)
        self.assertFalse(self.j.harvest(key, self.capture(row, 'idle'), b'bad', self.root / 'raw', notified=True))
        self.j = life.Journal(self.j.path, root=self.root)
        with patch.object(life.contextual, 'validate_result_bytes', side_effect=AssertionError('do not retry verdict')):
            self.assertFalse(self.j.harvest(key, self.capture(row, 'idle'), b'bad', self.root / 'raw', notified=True))

    def test_explicit_abandonment_requires_evidence_and_cannot_be_reaccepted(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        key = self.j.key(row)
        transport = FakeTransport(self, row)
        with patch.object(transport, 'terminal_bytes', side_effect=RuntimeError('unavailable')):
            self.j.harvest_and_archive(key, transport, self.root / 'raw', notified=True)
        audit = self.root / 'abandonment.json'
        write(audit, {'facts': ['raw export unavailable'], 'decision': 'abandon this run'})
        self.j.reject(key, 'explicitly abandon after source audit', audit)
        self.assertFalse(self.j.harvest(key, self.capture(row, 'idle'), self.raw(row), self.root / 'raw', notified=True))
        self.assertEqual(row['validation_state'], 'rejected')
        self.assertTrue(self.j.archive_intent(key, self.capture(row, 'idle')))
        self.assertTrue(row['rejection']['evidence_sha256'])

    def test_invalid_capture_leaves_same_journal_unmodified(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        key = self.j.key(row)
        self.j.create_intent(key, self.profiles)
        before = deepcopy(row)
        capture = self.capture(row, 'idle')
        capture['snapshot']['attentionReason'] = None
        with self.assertRaises(life.LifecycleError):
            self.j.bind(key, capture)
        self.assertEqual(row, before)
        good = self.capture(row, 'idle')
        self.j.bind(key, good)
        self.assertEqual(row['first_live_capture'], good)
        self.assertEqual(row['lifecycle'], 'terminal')
        with self.assertRaises(life.LifecycleError):
            self.j.bind(key, capture)
        self.assertEqual(row['first_live_capture'], good)

    def absent_audit(self, row, *, snapshots=None):
        return dict(schema='review-create-reconciliation/1', key=self.j.key(row),
                    create_attempt=row['create_attempts_started'], queried_at=life.now(),
                    filter=dict(workspace_id=row['workspace_id'], cwd=row['cwd'], labels=row['labels']),
                    complete=True, includes_archived=True, lifecycle_filter=None,
                    excluded_history_ids=sorted(r['agent_id'] for r in self.j.rows if r.get('agent_id')),
                    pages=[dict(cursor=None, next_cursor=None, has_more=False,
                                request={'tool': 'list_agents', 'arguments': dict(includeArchived=True, cwd=row['cwd'], sinceHours=720, limit=200)},
                                response={'structuredContent': {'agents': [
                                    {k: item[k] for k in ('id', 'cwd', 'labels')} for item in (snapshots or [])]}},
                                snapshots=snapshots or [])])

    def test_absent_reconciliation_one_retry_and_history(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        key = self.j.key(row)
        path = self.root / 'audit.json'
        for attempt in (1, 2):
            self.j.create_intent(key, self.profiles)
            write(path, self.absent_audit(row))
            self.j.reconcile_absent(key, path)
            self.assertEqual(row['status'], 'confirmed_absent')
            self.assertFalse(row['archive_confirmed'])
            self.assertEqual(row['create_attempts_started'], attempt)
        self.assertEqual(len(row['reconciliations']), 2)
        self.assertEqual(len(row['create_attempts']), 2)
        self.assertEqual(life.read(self.root / '.ai/task/context-task/STATE.json')['child_dispatches'], [])
        with self.assertRaisesRegex(life.LifecycleError, 'budget exhausted'):
            self.j.create_intent(key, self.profiles)
        with self.assertRaises(life.LifecycleError):
            close.publish(self.j, [key], self.root / 'import')

    def test_reconciliation_rejects_incomplete_stale_or_matching_capture(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        key = self.j.key(row)
        self.j.create_intent(key, self.profiles)
        baseline = deepcopy(row)
        variants = []
        for field, value in [('complete', False), ('includes_archived', False), ('lifecycle_filter', 'active'),
                             ('key', 'wrong|dispatch'), ('create_attempt', 0), ('excluded_history_ids', ['alien']),
                             ('queried_at', '2000-01-01T00:00:00Z'), ('filter', {})]:
            bad = self.absent_audit(row)
            bad[field] = value
            variants.append(bad)
        for status in ('running', 'idle', 'closed'):
            variants.append(self.absent_audit(row, snapshots=[self.capture(row, status)['snapshot']]))
        bad = self.absent_audit(row)
        bad['pages'][0]['has_more'] = True
        variants.append(bad)
        for audit in variants:
            with self.subTest(audit=audit):
                path = self.root / 'bad-audit.json'
                write(path, audit)
                with self.assertRaises(life.LifecycleError):
                    self.j.reconcile_absent(key, path)
                self.assertEqual(row, baseline)

    def test_partial_plan_can_retry_only_after_all_real_children_archived(self):
        specs = self.surface()
        self.prepare(specs, life.SURFACE)
        rows = self.j.rows[:]
        self.j.create_intent(self.j.key(rows[0]), self.profiles)
        self.j.bind(self.j.key(rows[0]), self.capture(rows[0]))
        self.j.create_intent(self.j.key(rows[1]), self.profiles)
        audit = self.absent_audit(rows[1], snapshots=[self.capture(rows[0], 'closed')['snapshot']])
        path = self.root / 'absent.json'
        write(path, audit)
        self.j.reconcile_absent(self.j.key(rows[1]), path)
        with self.assertRaisesRegex(life.LifecycleError, 'archive all'):
            self.prepare(self.surface(attempt=2), life.SURFACE)
        self.finish(rows[0], raw=b'failed')
        self.prepare(self.surface(attempt=2), life.SURFACE)
        with self.assertRaises(life.LifecycleError):
            self.j.create_intent(self.j.key(rows[2]), self.profiles)
        new = self.bind(self.surface(attempt=2))
        for row in new:
            self.finish(row)
        result = close.publish(self.j, [self.j.key(r) for r in new], self.root / 'import')
        self.assertEqual(result.outcome, 'DONE_VERIFIED')
        state = life.read(self.root / '.ai/task/surface-task/STATE.json')
        self.assertEqual(len(state['child_dispatches']), 5)  # three uncreated members are not children
        self.assertEqual(len(self.j.rows), 8)

    def test_fake_cli_creation_then_real_shape_binding_and_order(self):
        specs = self.surface()
        statepath = self.root / '.ai/task/surface-task/STATE.json'
        state = life.read(statepath)
        state['orchestration_transport'] = 'cli'  # actual stage_* initial shape
        write(statepath, state)
        plan = self.root / 'cli-plan.json'
        write(plan, {'surface-task': {'lanes': specs}})
        fakebin = self.root / 'bin'
        fakebin.mkdir()
        fake = fakebin / 'paseo'
        fake.write_text('#!' + sys.executable + '\n' + '''import json, os, sys
from pathlib import Path
p=Path(os.environ['FAKE_JOURNAL'])
rows=json.loads(p.read_text())
r=next(r for r in rows if r['status']=='dispatching')
assert r['create_attempts_started']==1 and r['profiles_sha256']
assert r['creation_transport']=='cli'
args=sys.argv[1:]
assert args[0]=='run' and '--background' in args and '--workspace' in args
assert '--label' in args and 'lane_index=1' in args
Path(os.environ['FAKE_LOG']).write_text(json.dumps(args))
print(json.dumps({'agentId':'fake-cli-child','status':'created'}))
''')
        fake.chmod(0o755)
        log = self.root / 'fake-cli-log.json'
        env = dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ['PATH'],
                   TOME_TRANSLATION_ROOT=str(self.root), PASEO_AGENT_ID=self.parent,
                   TOME_PASEO_WORKSPACE=self.ws, FAKE_JOURNAL=str(self.j.path), FAKE_LOG=str(log))
        cmd = [sys.executable, '-B', str(ROOT / 'tools/orchestration/dispatch_surface.py'),
               str(plan), str(self.j.path)]
        result = subprocess.run(cmd + ['--profiles', str(self.profiles)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b'CREATED', result.stdout)
        self.assertTrue(log.exists())
        self.j = life.Journal(self.j.path, root=self.root)
        row = self.j.rows[0]
        self.assertEqual(row['status'], 'created')
        self.assertEqual(row['agent_id'], 'fake-cli-child')
        self.assertNotIn('runtime_observation', row)
        before_log = log.read_bytes()
        result = subprocess.run(cmd + ['--profiles', str(self.profiles)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(log.read_bytes(), before_log)
        live = self.root / 'cli-live.json'
        write(live, {self.j.key(row): self.capture(row)})
        result = subprocess.run(cmd + ['--live', str(live)], env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.j = life.Journal(self.j.path, root=self.root)
        self.assertEqual(self.j.rows[0]['status'], 'dispatched')
        self.assertEqual(life.read(statepath)['orchestration_transport'], 'cli')
        self.assertEqual(self.j.rows[0]['runtime_observation']['model']['value'], 'actual-model')
        self.assertEqual([r['status'] for r in self.j.rows[1:]], ['prepared'] * 3)

    def test_transport_selection_and_save_cannot_migrate_history(self):
        specs = self.contextual()
        self.j.select_transport({'context-task'}, 'cli')
        with self.assertRaisesRegex(life.LifecycleError, 'transport mismatch'):
            self.prepare(specs)
        self.j.select_transport({'context-task'}, 'mcp')
        self.prepare(specs)
        row, = self.bind(specs)
        with self.assertRaisesRegex(life.LifecycleError, 'without history'):
            self.j.select_transport({'context-task'}, 'cli')
        path = self.root / '.ai/task/context-task/STATE.json'
        state = life.read(path)
        state['orchestration_transport'] = 'cli'
        write(path, state)
        journal_before = self.j.path.read_bytes()
        with self.assertRaisesRegex(life.LifecycleError, 'transport mismatch'):
            self.j.save()
        self.assertEqual(self.j.path.read_bytes(), journal_before)
        self.assertEqual(life.read(path)['orchestration_transport'], 'cli')

    def test_done_and_stop_mirrors_keep_bytes(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        self.finish(row)
        close.publish(self.j, [self.j.key(row)], self.root / 'import')
        path = self.root / '.ai/task/context-task/STATE.json'
        for phase in ('DONE', 'STOP'):
            state = life.read(path)
            state['state'] = phase
            write(path, state)
            before = path.read_bytes()
            self.j.save()
            self.assertEqual(path.read_bytes(), before)

    def test_absence_cannot_drop_raw_list_ids_or_claim_full_limit(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        self.j.create_intent(self.j.key(row), self.profiles)
        audit = self.absent_audit(row, snapshots=[self.capture(row)['snapshot']])
        path = self.root / 'audit.json'
        dropped = deepcopy(audit)
        dropped['pages'][0]['snapshots'] = []
        write(path, dropped)
        with self.assertRaisesRegex(life.LifecycleError, 'snapshot coverage'):
            self.j.reconcile_absent(self.j.key(row), path)
        audit['pages'][0]['request']['arguments']['limit'] = 1
        write(path, audit)
        with self.assertRaisesRegex(life.LifecycleError, 'truncated'):
            self.j.reconcile_absent(self.j.key(row), path)

    def native_records(self, provider, text, *, prompt='frozen prompt', cwd='/fixture'):
        """Synthetic versioned shapes; no real session, prompts, IDs or thinking."""
        if provider == 'codex':
            def record(kind, **payload):
                return dict(type=kind, payload=payload)
            def message(role, text, **fields):
                return record('response_item', type='message', role=role, id=role + '-message',
                              content=[dict(type='input_text' if role == 'user' else 'output_text', text=text)],
                              internal_chat_message_metadata_passthrough=dict(turn_id='turn'), **fields)
            rows = [record('session_meta', id='session', session_id='session', cwd=cwd, cli_version='0.153.0'),
                    record('event_msg', type='task_started', turn_id='turn'),
                    record('response_item', type='message', id='bootstrap', role='user', content=[
                        dict(type='input_text', text='<recommended_plugins>\nfixture</recommended_plugins>'),
                        dict(type='input_text', text='# AGENTS.md instructions for ' + cwd),
                        dict(type='input_text', text='<environment_context>\nfixture</environment_context>')]),
                    record('turn_context', turn_id='turn', cwd=cwd), message('user', prompt),
                    message('assistant', '{"earlier":"valid JSON is not final"}', phase='commentary'),
                    record('response_item', type='custom_tool_call_output', output='{"tool":"not final"}'),
                    message('assistant', text, phase='final_answer'),
                    record('token_usage_record', turn_id='turn', session_id='session'),
                    record('event_msg', type='task_complete', turn_id='turn', last_agent_message=text)]
            for i, row in enumerate(rows): row['ordinal'] = i
            return rows
        def node(kind, uid, parent, **fields):
            return dict(type=kind, uuid=uid, parentUuid=parent, sessionId='session', cwd=cwd,
                        version='2.1.259', isSidechain=False, **fields)
        def assistant(uid, parent, kind, text, mid, stop, index=0):
            block = dict(type=kind, **({'text': text} if kind == 'text' else {'thinking': 'synthetic private block'}))
            return node('assistant', uid, parent, apiBlockIndex=index, requestId='request',
                        message=dict(role='assistant', id=mid, content=[block], stop_reason=stop))
        return [dict(type='queue-operation', operation='dequeue', sessionId='session'),
                node('user', 'prompt', None, message=dict(role='user', content=[dict(type='text', text=prompt)])),
                assistant('early', 'prompt', 'text', '{"earlier":"JSON"}', 'earlier-message', 'tool_use'),
                node('user', 'result', 'early', message=dict(role='user', content=[dict(type='tool_result', content='not final')])),
                node('attachment', 'attachment', 'result'),
                assistant('thinking', 'attachment', 'thinking', None, 'final-message', 'end_turn'),
                assistant('final', 'thinking', 'text', text, 'final-message', 'end_turn', 1),
                dict(type='last-prompt', leafUuid='final', sessionId='session')]

    @staticmethod
    def native_bytes(records):
        return b''.join(json.dumps(r, ensure_ascii=False).encode('utf-8') + b'\n' for r in records)

    def parse_native(self, provider, records):
        return life.parse_native_final(self.native_bytes(records), provider=provider, session_id='session',
                                       cwd='/fixture', prompt='frozen prompt')

    def native_child(self, provider='codex'):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.get(self.j.key(specs[0]))
        self.j.create_intent(self.j.key(row), self.profiles)
        live = self.capture(row)
        live['snapshot'].update(provider=provider, persistence=dict(provider=provider, sessionId='session',
                nativeHandle='session', metadata=dict(provider=provider, cwd=str(self.root))),
                runtimeInfo=dict(provider=provider, sessionId='session'))
        self.j.bind(self.j.key(row), live)
        terminal = deepcopy(live)
        terminal.update(status='idle')
        terminal['snapshot'].update(status='idle', activeTurn=None, attentionReason='finished',
                                    attentionTimestamp='2026-09-12T01:01:00Z')
        native = self.root / 'native.jsonl'
        native.write_bytes(self.native_bytes(self.native_records(provider, self.raw(row).decode(),
                           cwd=str(self.root), prompt=row['create_parameters']['prompt'])))
        return row, terminal, native

    def test_native_exact_text_not_earlier_json_tool_or_thinking(self):
        for provider in ('codex', 'claude'):
            text = ' \n---\n\n{"中文":"原样"}\t\r\n'
            raw, proof = self.parse_native(provider, self.native_records(provider, text))
            self.assertEqual(raw, text.encode())
            self.assertEqual(proof['raw_sha256'], life.digest(raw))
            self.assertNotIn('synthetic private block', json.dumps(proof))
            self.assertNotIn('frozen prompt', json.dumps(proof))
            # No JSON search: unstructured true final is returned as-is.
            self.assertEqual(self.parse_native(provider, self.native_records(provider, 'later prose'))[0], b'later prose')

    def test_native_whitespace_and_markdown_preserved_then_strict_rejected(self):
        specs = self.contextual()
        self.prepare(specs)
        row = self.j.rows[0]
        env = (self.root / row['input_path']).read_bytes()
        for provider in ('codex', 'claude'):
            for text in (' \n' + self.raw(row).decode() + '\t\n', '---\n\n' + self.raw(row).decode(),
                         '```json\n' + self.raw(row).decode() + '\n```'):
                with self.subTest(provider=provider, text=text[:4]):
                    raw, _ = self.parse_native(provider, self.native_records(provider, text))
                    self.assertEqual(raw, text.encode())
                    with self.assertRaises(life.contextual.ContractError):
                        life.contextual.validate_result_bytes(env, raw)

    def test_native_codex_rejects_unproven_boundaries_and_identity(self):
        original = self.native_records('codex', '{}')
        variants = []
        for index, path, value in [
            (0, ('payload', 'cli_version'), '0.154.0'), (0, ('payload', 'id'), 'other'),
            (0, ('payload', 'cwd'), '/other'), (3, ('payload', 'turn_id'), 'other'),
            (4, ('payload', 'content'), [dict(type='input_text', text='different prompt')]),
            (7, ('payload', 'phase'), 'commentary'), (7, ('payload', 'content'), [dict(type='thinking', text='{}')]),
            (7, ('payload', 'internal_chat_message_metadata_passthrough'), dict(turn_id='other')),
            (9, ('payload', 'last_agent_message'), 'changed'), (9, ('payload', 'turn_id'), 'other'),
            (5, ('ordinal',), 999), (2, ('payload', 'content'), [dict(type='input_text', text='new user')]),
            (8, ('payload', 'session_id'), 'other')]:
            bad = deepcopy(original)
            target = bad[index]
            for key in path[:-1]: target = target[key]
            target[path[-1]] = value
            variants.append(bad)
        for extra in (deepcopy(original[4]), deepcopy(original[7]), deepcopy(original[1])):
            bad = deepcopy(original)
            bad.insert(8, extra)
            for i, r in enumerate(bad): r['ordinal'] = i
            variants.append(bad)
        variants.extend([original[:-1], original + [dict(type='world_state', payload={}, ordinal=10)]])
        for n, bad in enumerate(variants):
            with self.subTest(case=n), self.assertRaises(life.LifecycleError): self.parse_native('codex', bad)

    def test_native_claude_rejects_thinking_leaf_branches_and_new_user_turn(self):
        original = self.native_records('claude', '{}')
        variants = []
        for index, path, value in [
            (1, ('version',), 'unknown'), (3, ('sessionId',), 'other'), (4, ('cwd',), '/other'),
            (7, ('leafUuid',), 'thinking'), (7, ('leafUuid',), 'early'), (7, ('sessionId',), 'other'),
            (6, ('parentUuid',), 'missing'), (6, ('uuid',), 'thinking'), (6, ('isSidechain',), True),
            (6, ('message', 'stop_reason'), 'tool_use'), (5, ('message', 'id'), 'other'),
            (6, ('apiBlockIndex',), 2), (6, ('message', 'content'), [dict(type='text', text='a'), dict(type='text', text='b')]),
            (3, ('message', 'content'), [dict(type='text', text='frozen prompt')]),
            (6, ('parentUuid',), 'prompt'), (2, ('message', 'id'), 'final-message')]:
            bad = deepcopy(original)
            target = bad[index]
            for key in path[:-1]: target = target[key]
            target[path[-1]] = value
            variants.append(bad)
        variants.extend([original[:-1], original + [dict(type='ai-title', sessionId='session')]])
        for n, bad in enumerate(variants):
            with self.subTest(case=n), self.assertRaises(life.LifecycleError): self.parse_native('claude', bad)

    def test_native_rejects_partial_json_unknown_provider_and_byte_line_limits(self):
        for provider in ('codex', 'claude'):
            data = self.native_bytes(self.native_records(provider, '{}'))
            for bad in (data[:-1], data + b'{"incomplete":\n', data + b'\n', data + b'{"a":1,"a":2}\n',
                        data + b'\xff\n', b'null\n'):
                with self.subTest(provider=provider), self.assertRaises(life.LifecycleError):
                    life.parse_native_final(bad, provider=provider, session_id='session', cwd='/fixture', prompt='frozen prompt')
            with patch.object(life, 'NATIVE_MAX_BYTES', 10), self.assertRaises(life.LifecycleError):
                self.parse_native(provider, self.native_records(provider, '{}'))
            with patch.object(life, 'NATIVE_MAX_LINES', 2), self.assertRaises(life.LifecycleError):
                self.parse_native(provider, self.native_records(provider, '{}'))
        with self.assertRaises(life.LifecycleError): self.parse_native('unknown', self.native_records('codex', '{}'))

    def test_native_requires_ordinary_stable_file_and_never_blocks_on_fifo(self):
        path = self.root / 'session.jsonl'
        path.write_bytes(self.native_bytes(self.native_records('codex', '{}')))
        binding = dict(provider='codex', session_id='session', cwd='/fixture', prompt='frozen prompt')
        link = self.root / 'symlink'
        link.symlink_to(path)
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        for invalid in (link, fifo, self.root):
            with self.assertRaises(life.LifecycleError): life.read_native_final(invalid, **binding)
        original = life.parse_native_final
        def changed(data, **kwargs):
            result = original(data, **kwargs)
            path.write_bytes(data + b'\n')
            return result
        with patch.object(life, 'parse_native_final', changed), self.assertRaisesRegex(life.LifecycleError, 'changed during read'):
            life.read_native_final(path, **binding)
        path.write_bytes(self.native_bytes(self.native_records('codex', '{}')))
        def replaced(data, **kwargs):
            result = original(data, **kwargs)
            replacement = self.root / 'replacement'
            replacement.write_bytes(data)
            replacement.replace(path)
            return result
        with patch.object(life, 'parse_native_final', replaced), self.assertRaisesRegex(life.LifecycleError, 'changed during read'):
            life.read_native_final(path, **binding)

    def test_native_identity_aliases_are_scoped_and_conflicts_refused(self):
        row, cap, native = self.native_child()
        for scope, key, value in [('snapshot', 'provider', 'claude'), ('snapshot', 'sessionId', 'other'),
                                  ('runtimeInfo', 'provider', 'claude'), ('runtimeInfo', 'sessionId', 'other'),
                                  ('persistence', 'sessionId', None), ('persistence', 'provider', 'claude'),
                                  ('persistence', 'nativeHandle', 'other'), ('metadata', 'cwd', '/other'),
                                  ('metadata', 'threadId', 'other')]:
            bad = deepcopy(cap)
            target = bad['snapshot']
            if scope == 'metadata': target = target['persistence']['metadata']
            elif scope != 'snapshot': target = target[scope]
            target[key] = value
            with self.subTest(scope=scope, key=key), patch.object(life, 'read_native_final') as reader:
                with self.assertRaises(life.LifecycleError):
                    life.export_native_final(self.j, self.j.key(row), bad, native, self.root / 'out', notified=True)
                reader.assert_not_called()
        self.assertNotIn('output_valid', row)
        self.assertEqual(row['archive_attempts_started'], 0)
        self.assertFalse(list((self.root / 'out').rglob('terminal.raw')))

    def test_native_export_checks_notification_complete_identity_and_frozen_prompt_first(self):
        row, cap, native = self.native_child()
        variants = []
        for field, value in [('id', 'other'), ('workspaceId', 'other'), ('cwd', '/other'),
                             ('parentAgentId', 'other'), ('activeTurn', {}), ('attentionReason', None)]:
            bad = deepcopy(cap)
            bad['snapshot'][field] = value
            variants.append(bad)
        bad = deepcopy(cap)
        del bad['snapshot']['activeTurn']
        variants.append(bad)
        bad = deepcopy(cap)
        bad['snapshot']['labels']['role'] = 'executor'
        variants.append(bad)
        with patch.object(life, 'read_native_final') as reader:
            with self.assertRaises(life.LifecycleError):
                life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=False)
            for bad in variants:
                with self.assertRaises(life.LifecycleError):
                    life.export_native_final(self.j, self.j.key(row), bad, native, self.root / 'out', notified=True)
            row['create_parameters']['prompt'] += ' changed'
            with self.assertRaisesRegex(life.LifecycleError, 'frozen creation prompt'):
                life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
            reader.assert_not_called()

    def test_native_registered_state_and_first_session_checked_before_source(self):
        row, cap, native = self.native_child()
        changed = deepcopy(cap)
        changed['snapshot']['persistence'].update(sessionId='other', nativeHandle='other')
        changed['snapshot']['runtimeInfo']['sessionId'] = 'other'
        with patch.object(life, 'read_native_final') as reader:
            with self.assertRaisesRegex(life.LifecycleError, 'immutable live native identity'):
                life.export_native_final(self.j, self.j.key(row), changed, native, self.root / 'out', notified=True)
            path = self.root / '.ai/task' / row['task_id'] / 'STATE.json'
            state = life.read(path)
            state['child_dispatches'][0]['agent_id'] = 'different-registered-child'
            write(path, state)
            before = path.read_bytes()
            with self.assertRaises(life.LifecycleError):
                life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
            self.assertEqual(path.read_bytes(), before)
            reader.assert_not_called()
        self.assertNotIn('output_valid', row)

    def test_native_export_source_failure_recovers_without_archive_or_verdict(self):
        row, cap, native = self.native_child('claude')
        source = native.read_bytes()
        native.write_bytes(source[:-1])
        with self.assertRaisesRegex(life.LifecycleError, 'incomplete'):
            life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
        self.assertNotIn('output_valid', row)
        self.assertFalse(row['archive_confirmed'])
        self.assertTrue(list((self.root / 'out').rglob('error-1.json')))
        native.write_bytes(source)
        raw = life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
        self.assertEqual(raw, self.raw(row))
        self.assertTrue(self.j.harvest(self.j.key(row), cap, raw, self.root / 'raw', notified=True))
        provenance = life.read(self.root / 'out' / row['task_id'] / row['dispatch_id'] / 'provenance.json')
        self.assertEqual(provenance['source_sha256'], life.digest(source))
        self.assertEqual(provenance['terminal_capture_sha256'], life.digest(life.surface.canonical_bytes(cap)))
        self.assertNotIn('synthetic private block', json.dumps(provenance))

    def test_native_cli_export_harvest_then_real_consumer(self):
        row, cap, native = self.native_child()
        capture = self.root / 'terminal.json'
        write(capture, cap)
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root))
        cli = [sys.executable, '-B', str(ROOT / 'tools/orchestration/review_lifecycle.py')]
        outdir = self.root / 'export'
        result = subprocess.run(cli + ['native-export', str(self.j.path), self.j.key(row), '--capture', str(capture),
                    '--native-log', str(native), '--outdir', str(outdir), '--notified'], env=env, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        raw = outdir / row['task_id'] / row['dispatch_id'] / 'terminal.raw'
        self.assertEqual(raw.read_bytes(), self.raw(row))
        result = subprocess.run(cli + ['harvest', str(self.j.path), self.j.key(row), '--capture', str(capture),
                    '--native-log', str(native), '--outdir', str(self.root / 'raw'), '--notified'],
                    env=env, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.j = life.Journal(self.j.path, root=self.root)
        row = self.j.get(self.j.key(row))
        self.finish(row)
        # Existing real strict consumer and publication contract, not mocked.
        close.publish(self.j, [self.j.key(row)], self.root / 'published')
        state = life.read(self.root / '.ai/task' / row['task_id'] / 'STATE.json')
        self.assertEqual(state['state'], 'DONE')
        with self.assertRaisesRegex(life.LifecycleError, 'precede archive'):
            life.export_native_final(self.j, self.j.key(row), cap, native, outdir, notified=True)

    def error_child(self):
        specs = self.contextual()
        self.prepare(specs)
        row, = self.bind(specs)
        cap = self.capture(row, 'error')
        cap['snapshot'].update(attentionReason='error', attentionTimestamp='2026-09-12T01:01:00Z')
        evidence = self.root / 'error-audit.json'
        write(evidence, {'provider_failure': 'run ended with error before producing a final answer'})
        return row, cap, evidence

    def assert_reject_unchanged(self, row, capture, evidence, *, reason='provider failed before final', notified=True):
        before = deepcopy(self.j.rows)
        observation = row['runtime_observation']
        files = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with self.assertRaises((life.LifecycleError, life.contextual.ContractError, OSError, ValueError, TypeError)):
            self.j.reject(self.j.key(row), reason, evidence, capture=capture, notified=notified)
        self.assertEqual(self.j.rows, before)
        self.assertIs(row['runtime_observation'], observation)
        self.assertEqual({p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}, files)

    def test_error_terminal_cli_reject_archive_readback_and_fresh_retry_without_native_final(self):
        for persistence in ('missing', 'no-session', 'session-without-final'):
            with self.subTest(persistence=persistence), tempfile.TemporaryDirectory(dir=self.root) as tmp:
                original_root, original_journal = self.root, self.j
                self.root = Path(tmp)
                self.j = life.Journal(self.root / 'journal.json', root=self.root)
                try:
                    row, cap, evidence = self.error_child()
                    if persistence != 'missing':
                        cap['snapshot']['persistence'] = {'provider': 'codex'}
                        if persistence == 'session-without-final':
                            cap['snapshot']['persistence']['sessionId'] = 'session'
                    key = self.j.key(row)
                    observation = deepcopy(row['runtime_observation'])
                    first = deepcopy(row['first_live_capture'])
                    capture_path = self.root / 'error.json'
                    write(capture_path, cap)
                    env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root), PATH='')
                    cli = [sys.executable, '-B', str(ROOT / 'tools/orchestration/review_lifecycle.py')]

                    def run(action, *args):
                        return subprocess.run(cli + [action, str(self.j.path), key, *args],
                                              env=env, capture_output=True, timeout=15)

                    result = run('native-export', '--capture', str(capture_path), '--native-log',
                                 str(self.root / 'absent-native.jsonl'), '--outdir', str(self.root / 'export'), '--notified')
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(b'native source needs successful natural completion', result.stderr)
                    self.j = life.Journal(self.j.path, root=self.root)
                    row = self.j.get(key)
                    self.assertNotIn('terminal_capture', row)
                    self.assertNotIn('output_valid', row)
                    self.assertFalse(list(self.root.rglob('*.raw')))
                    fetch_errors = deepcopy(row['terminal_fetch_errors'])
                    result = run('reject', '--reason', 'provider failed before final', '--evidence', str(evidence))
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(b'terminal evidence required', result.stderr)
                    result = run('reject', '--capture', str(capture_path), '--reason', 'provider failed before final',
                                 '--evidence', str(evidence), '--notified')
                    self.assertEqual(result.returncode, 0, result.stderr.decode())
                    self.j = life.Journal(self.j.path, root=self.root)
                    row = self.j.get(key)
                    self.assertEqual(row['validation_state'], 'rejected')
                    self.assertIs(row['output_valid'], False)
                    self.assertEqual(row['terminal_capture'], cap)
                    self.assertEqual(Path(row['rejection']['evidence_path']).read_bytes(), evidence.read_bytes())
                    self.assertEqual(row['archive_attempts_started'], 0)
                    self.assertNotIn('raw_output_path', row)
                    self.assertFalse(list(self.root.rglob('*.raw')))
                    with self.assertRaisesRegex(life.LifecycleError, 'archive all'):
                        self.prepare(self.contextual(retry=key))
                    result = run('archive-intent', '--capture', str(capture_path))
                    self.assertEqual(result.returncode, 0, result.stderr.decode())
                    transport = FakeTransport(self, row)
                    transport.archive(key)  # asserts durable journal AND STATE budget at the action boundary
                    self.assertEqual(life.read(self.j.path)[0]['archive_attempts_started'], 1)
                    archived = self.root / 'archived.json'
                    write(archived, transport.status(key))
                    result = run('archive-confirm', '--capture', str(archived))
                    self.assertEqual(result.returncode, 0, result.stderr.decode())
                    self.j = life.Journal(self.j.path, root=self.root)
                    row = self.j.get(key)
                    self.assertTrue(row['archive_confirmed'])
                    self.assertEqual(row['archived_at'], '2026-09-12T01:02:00Z')
                    self.assertEqual(row['runtime_observation'], observation)
                    self.assertEqual(row['first_live_capture'], first)
                    self.assertEqual(row['terminal_fetch_errors'], fetch_errors)
                    failed = deepcopy(row)
                    retry = self.contextual(retry=key)
                    self.prepare(retry)
                    successor, = self.bind(retry)
                    self.assertNotEqual(successor['agent_id'], row['agent_id'])
                    self.assertNotEqual(successor['dispatch_id'], row['dispatch_id'])
                    self.assertEqual(successor['input_sha256'], row['input_sha256'])
                    self.assertEqual(self.j.get(key), failed)
                    self.assertEqual(life.read(self.root / '.ai/task/context-task/STATE.json')['review_records'], [])
                finally:
                    self.root, self.j = original_root, original_journal

    def test_reject_capture_bad_identity_terminal_and_notification_leave_same_journal_unchanged(self):
        row, cap, evidence = self.error_child()
        variants = [None, {}, self.capture(row)]
        for field, value in [('id', 'another-child'), ('id', self.parent), ('workspaceId', 'other'),
                             ('cwd', '/other-root'), ('parentAgentId', 'other-parent'), ('labels', {}),
                             ('activeTurn', {'turnId': 'still-running'}), ('attentionReason', None),
                             ('attentionTimestamp', None), ('attentionTimestamp', '2026-09-12T01:01:00')]:
            bad = deepcopy(cap)
            bad['snapshot'][field] = value
            variants.append(bad)
        for field in cap['snapshot']:
            if field in ('provider', 'model', 'currentModeId'):
                continue  # runtime/native fields are not required for rejection
            bad = deepcopy(cap)
            del bad['snapshot'][field]
            variants.append(bad)
        for label in row['labels']:
            bad = deepcopy(cap)
            bad['snapshot']['labels'][label] = 'wrong'
            variants.append(bad)
        bad = deepcopy(cap)
        bad['status'] = 'idle'
        variants.append(bad)
        for index, bad in enumerate(variants):
            with self.subTest(index=index):
                self.assert_reject_unchanged(row, bad, evidence)
        self.assert_reject_unchanged(row, cap, evidence, notified=False)
        self.j.reject(self.j.key(row), 'provider failed before final', evidence, capture=cap, notified=True)
        # Invalid capture must still be checked after a successful, repeatable reject.
        self.assert_reject_unchanged(row, variants[-1], evidence)

    def test_reject_reason_and_evidence_validated_before_terminal_persistence(self):
        row, cap, evidence = self.error_child()
        for reason in (None, '', ' \n\t', 123):
            with self.subTest(reason=reason):
                self.assert_reject_unchanged(row, cap, evidence, reason=reason)
        self.assert_reject_unchanged(row, cap, self.root / 'missing')
        self.assert_reject_unchanged(row, cap, self.root)
        empty = self.root / 'empty'
        for content in (b'', b' \n\t'):
            empty.write_bytes(content)
            self.assert_reject_unchanged(row, cap, empty)
        self.assertNotIn('terminal_capture', row)
        self.assertEqual(row['archive_attempts_started'], 0)

    def test_reject_checks_registered_state_root_and_frozen_input_before_mutation(self):
        row, cap, evidence = self.error_child()
        state_path = self.root / '.ai/task/context-task/STATE.json'
        state = life.read(state_path)
        variants = []
        for field, value in [('task_id', 'other'), ('workspace_id', 'other'), ('orchestrator_agent_id', 'other'),
                             ('orchestration_transport', 'cli'), ('review_records', ['published.json']),
                             ('state', 'DONE'), ('child_dispatches', [])]:
            bad = deepcopy(state)
            bad[field] = value
            variants.append(bad)
        for field in ('agent_id', 'labels', 'runtime_observation', 'candidate_identity', 'parent_agent_id'):
            bad = deepcopy(state)
            bad['child_dispatches'][0][field] = 'changed'
            variants.append(bad)
        for index, bad in enumerate(variants):
            with self.subTest(index=index):
                write(state_path, bad)
                self.assert_reject_unchanged(row, cap, evidence)
        write(state_path, state)
        for field, value in [('cwd', '/other-root'), ('lineage_verified', False), ('agent_id', None),
                             ('parent_agent_id', 'other-parent'), ('labels', {})]:
            original = row[field]
            row[field] = value
            self.assert_reject_unchanged(row, cap, evidence)
            row[field] = original
        input_path = self.root / row['input_path']
        original = input_path.read_bytes()
        input_path.write_bytes(original + b'\n')
        self.assert_reject_unchanged(row, cap, evidence)
        input_path.write_bytes(original)
        observation = row['runtime_observation']
        before = deepcopy(observation)
        self.j.reject(self.j.key(row), 'provider failed before final', evidence, capture=cap, notified=True)
        self.assertIs(row['runtime_observation'], observation)
        self.assertEqual(observation, before)

    def test_reject_mirror_validation_failure_leaves_no_partial_rejection(self):
        row, cap, evidence = self.error_child()
        # A different task's mirror can fail save after the target's identity checks.
        self.prepare(self.surface(count=2), life.SURFACE)
        state_path = self.root / '.ai/task/surface-task/STATE.json'
        state = life.read(state_path)
        state['workspace_id'] = 'wrong-workspace'
        write(state_path, state)
        self.assert_reject_unchanged(row, cap, evidence)
        path = self.j.path.parent / (row['task_id'] + '-' + row['dispatch_id'] + '-rejection-evidence')
        self.assertFalse(path.exists())
        path.write_bytes(evidence.read_bytes())
        self.assert_reject_unchanged(row, cap, evidence)
        self.assertEqual(path.read_bytes(), evidence.read_bytes())

    def test_reject_capture_and_evidence_are_immutable_and_repeated_calls_preserve_history(self):
        row, cap, evidence = self.error_child()
        key = self.j.key(row)
        reason = 'provider failed before final'
        self.j.reject(key, reason, evidence, capture=cap, notified=True)
        saved = deepcopy(row)
        observation = row['runtime_observation']
        for capture in (cap, None):
            self.j.reject(key, reason, evidence, capture=capture, notified=True)
            self.assertEqual(row, saved)
            self.assertIs(row['runtime_observation'], observation)
            self.assertEqual(life.read(self.j.path)[0], saved)
        self.assert_reject_unchanged(row, cap, evidence, reason='different reason')
        conflict = self.root / 'conflict.json'
        conflict.write_bytes(b'different evidence')
        self.assert_reject_unchanged(row, cap, conflict)
        changed = deepcopy(cap)
        changed['snapshot']['attentionTimestamp'] = '2026-09-12T01:03:00Z'
        self.assert_reject_unchanged(row, changed, evidence)
        self.assertTrue(self.j.archive_intent(key, cap))
        self.assertTrue(self.j.archive_intent(key, cap))
        budget_exhausted = deepcopy(row)
        self.j.reject(key, reason, evidence, capture=cap, notified=True)
        self.assertEqual(row, budget_exhausted)
        with self.assertRaisesRegex(life.LifecycleError, 'budget exhausted'):
            self.j.archive_intent(key, cap)
        self.j.confirm_archive(key, self.capture(row, 'closed'))
        archived = deepcopy(row)
        self.j.reject(key, reason, evidence, capture=cap, notified=True)
        self.assertEqual(row, archived)

    def test_reject_with_capture_preserves_existing_raw_and_scope_rejection(self):
        row, cap, native = self.native_child()
        key = self.j.key(row)
        raw = life.export_native_final(self.j, key, cap, native, self.root / 'export', notified=True)
        self.assertTrue(self.j.harvest(key, cap, raw, self.root / 'raw', notified=True))
        evidence = self.root / 'scope-audit.json'
        write(evidence, {'observed_read': 'outside frozen input'})
        changed = deepcopy(cap)
        changed['snapshot']['attentionTimestamp'] = '2026-09-12T01:03:00Z'
        self.assert_reject_unchanged(row, changed, evidence)
        proof = deepcopy(row['native_provenance'])
        self.j.reject(key, 'read outside frozen references', evidence, capture=cap, notified=True)
        self.j.reject(key, 'read outside frozen references', evidence)
        self.assertEqual(row['native_provenance'], proof)
        self.assertEqual((self.root / row['raw_output_path']).read_bytes(), raw)
        self.assertEqual(Path(row['native_raw_path']).read_bytes(), raw)
        self.assertFalse(self.j.harvest(key, cap, raw, self.root / 'raw', notified=True))
        self.assertEqual(row['validation_state'], 'rejected')

    def test_native_invalid_and_manual_reject_never_reaccepted(self):
        row, cap, native = self.native_child('claude')
        text = ' \n' + self.raw(row).decode() + '\t\n'
        native.write_bytes(self.native_bytes(self.native_records('claude', text, cwd=str(self.root),
                                                prompt=row['create_parameters']['prompt'])))
        raw = life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
        self.assertFalse(self.j.harvest(self.j.key(row), cap, raw, self.root / 'raw', notified=True))
        evidence = self.root / 'reject.json'
        evidence.write_text('explicit fixture rejection evidence')
        self.j.reject(self.j.key(row), 'fixture scope violation', evidence)
        with patch.object(life.contextual, 'validate_result_bytes', side_effect=AssertionError('cannot revalidate rejected')):
            self.assertEqual(life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True), raw)
            self.assertFalse(self.j.harvest(self.j.key(row), cap, raw, self.root / 'raw', notified=True))
        self.assertEqual((self.root / row['raw_output_path']).read_bytes(), text.encode())

    def test_p1_null_alias_pair_and_invalid_known_values(self):
        row, terminal, native = self.native_child('claude')
        # Same locations/relationships as batch91 first/terminal; IDs and content synthetic.
        first = row['first_live_capture']['snapshot']
        first['runtimeInfo']['sessionId'] = None
        original = deepcopy(first)
        observation = deepcopy(row['runtime_observation'])
        self.j.save()
        self.assertEqual(life.native_identity(first, required=False), ('claude', 'session'))
        self.assertEqual(life.native_identity(terminal['snapshot']), ('claude', 'session'))
        for alias in ('sessionId', 'threadId'):
            for invalid in ('', 0, False, {}, [], 'conflict'):
                bad = deepcopy(first)
                bad['runtimeInfo'][alias] = invalid
                with self.subTest(alias=alias, invalid=invalid), self.assertRaises(life.LifecycleError):
                    life.native_identity(bad, required=False)
        for invalid in ('', 0, False, {}, [], 'conflict'):
            bad = deepcopy(first)
            bad['persistence']['nativeHandle'] = invalid
            with self.assertRaises(life.LifecycleError):
                life.native_identity(bad, required=False)
        unknown = deepcopy(first)
        unknown['persistence'].update(sessionId=None, nativeHandle=None)
        self.assertEqual(life.native_identity(unknown, required=False), ('claude', None))
        with self.assertRaises(life.LifecycleError):
            life.native_identity(unknown)
        source = self.native_records('claude', self.raw(row).decode(), cwd=str(self.root),
                                     prompt=row['create_parameters']['prompt'])[:-1]
        native.write_bytes(self.native_bytes(source))
        raw = life.export_native_final(self.j, self.j.key(row), terminal, native, self.root / 'native-out', notified=True)
        self.assertEqual(raw, self.raw(row))
        self.assertEqual(first, original)
        self.assertEqual(row['runtime_observation'], observation)

    def test_p1_natural_tail_modes_preserve_source_and_reject_ambiguity(self):
        rows = self.native_records('claude', ' \n{"exact":true}\t\n')
        binding = dict(provider='claude', session_id='session', cwd='/fixture', prompt='frozen prompt')
        versions = [rows[:-1], rows, rows + [dict(type='ai-title', aiTitle='fixture', sessionId='session')]]
        raws, hashes = [], []
        for records in versions:
            data = self.native_bytes(records)
            raw, proof = life.parse_native_final(data, **binding, natural_success=True)
            raws.append(raw); hashes.append(proof['source_sha256'])
            self.assertEqual(proof['source_bytes'], len(data))
            self.assertEqual(proof['final_line'], len(rows) - 1)
        self.assertEqual(len(set(raws)), 1)
        self.assertEqual(len(set(hashes)), 3)
        with self.assertRaisesRegex(life.LifecycleError, 'missing Claude final leaf'):
            life.parse_native_final(self.native_bytes(rows[:-1]), **binding)
        bads = [rows[:-1] + [versions[2][-1]], versions[2] + [versions[2][-1]],
                rows + [dict(type='ai-title', aiTitle=1, sessionId='session')],
                rows + [dict(type='ai-title', aiTitle='x', sessionId='other')],
                rows + [dict(type='ai-title', aiTitle='x', sessionId='session', extra=True)],
                rows + [rows[1]], rows[:-1] + [dict(type='unknown')]]
        for records in bads:
            with self.assertRaises(life.LifecycleError):
                life.parse_native_final(self.native_bytes(records), **binding, natural_success=True)
        for mutate in (lambda r: r[-2].update(parentUuid='missing'),
                       lambda r: r[-1].update(leafUuid='early'),
                       lambda r: r[-2].update(isSidechain=True),
                       lambda r: r[-2].update(version='new'),
                       lambda r: r[-2].update(uuid=r[1]['uuid'])):
            bad = deepcopy(rows); mutate(bad)
            with self.assertRaises(life.LifecycleError):
                life.parse_native_final(self.native_bytes(bad), **binding, natural_success=True)

    def test_p1_natural_atis_latch_preserves_exact_final_bytes(self):
        text = ' \n---\n\n{"中文":"原样"}\t\r\n'
        rows = self.native_records('claude', text)
        binding = dict(provider='claude', session_id='session', cwd='/fixture', prompt='frozen prompt')
        tail_modes = [rows[:-1], rows, rows + [dict(type='ai-title', aiTitle='fixture', sessionId='session')]]
        for without_latch in tail_modes:
            with_latch = without_latch + [dict(type='atis-latch', atis='', sessionId='session')]
            plain, _ = life.parse_native_final(self.native_bytes(without_latch), **binding, natural_success=True)
            latched, proof = life.parse_native_final(self.native_bytes(with_latch), **binding, natural_success=True)
            self.assertEqual(latched, plain)
            self.assertEqual(latched, text.encode())
            self.assertEqual(proof['final_line'], len(rows) - 1)
            self.assertEqual(proof['complete_line'], len(with_latch))

    def test_p1_natural_atis_latch_rejects_invalid_shape_or_identity(self):
        rows = self.native_records('claude', '{}')
        binding = dict(provider='claude', session_id='session', cwd='/fixture', prompt='frozen prompt')
        invalid = [
            dict(type='atis-latch', sessionId='session'),
            dict(type='atis-latch', atis='', sessionId='session', extra=True),
            dict(type='atis-latch', atis='', sessionId='other'),
            dict(type='atis-latch', atis=None, sessionId='session'),
        ]
        for latch in invalid:
            with self.subTest(latch=latch), self.assertRaises(life.LifecycleError):
                life.parse_native_final(self.native_bytes(rows + [latch]), **binding, natural_success=True)

    def test_p1_natural_historical_metadata_and_lifecycle_guards(self):
        row, cap, native = self.native_child('claude')
        records = [json.loads(x) for x in native.read_bytes().splitlines()][:-1]
        historical = [dict(type='last-prompt', leafUuid='early', sessionId='session'),
                      dict(type='ai-title', aiTitle='intermediate title', sessionId='session')]
        records[3:3] = historical
        native.write_bytes(self.native_bytes(records))
        variants = []
        for field, value in [('activeTurn', {}), ('attentionReason', 'error'), ('attentionTimestamp', 'bad')]:
            bad = deepcopy(cap); bad['snapshot'][field] = value; variants.append(bad)
        bad = deepcopy(cap); del bad['snapshot']['activeTurn']; variants.append(bad)
        bad = deepcopy(cap); bad['status'] = bad['snapshot']['status'] = 'error'; variants.append(bad)
        with patch.object(life, 'read_native_final') as reader:
            for bad in variants:
                with self.assertRaises((ValueError, life.LifecycleError)):
                    life.export_native_final(self.j, self.j.key(row), bad, native, self.root / 'out', notified=True)
            with self.assertRaises(life.LifecycleError):
                life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=False)
            reader.assert_not_called()
        raw = life.export_native_final(self.j, self.j.key(row), cap, native, self.root / 'out', notified=True)
        self.assertEqual(raw, self.raw(row))
        self.assertEqual(row['archive_attempts_started'], 0)
        self.assertNotIn('output_valid', row)

    def test_p1_natural_cli_strict_before_archive_and_error_raw_refused(self):
        row, cap, native = self.native_child('claude')
        records = [json.loads(x) for x in native.read_bytes().splitlines()]
        native.write_bytes(self.native_bytes(records[:-1]))
        capture = self.root / 'terminal.json'; write(capture, cap)
        cli = [sys.executable, '-B', str(ROOT / 'tools/orchestration/review_lifecycle.py'),
               'harvest', str(self.j.path), self.j.key(row), '--capture', str(capture),
               '--outdir', str(self.root / 'output'), '--notified']
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root))
        done = subprocess.run(cli + ['--native-log', str(native)], env=env, capture_output=True, timeout=15)
        self.assertEqual(done.returncode, 0, done.stderr.decode())
        self.j = life.Journal(self.j.path, root=self.root); row = self.j.get(self.j.key(row))
        self.assertTrue(row['output_valid']); self.assertEqual(row['archive_attempts_started'], 0)
        proof = deepcopy(row['native_provenance'])
        native.unlink()  # fully frozen proof/raw survive source disappearance before archive
        self.assertEqual(life.export_native_final(self.j, self.j.key(row), cap, native,
                         self.root / 'output/native', notified=True), self.raw(row))
        self.assertEqual(row['native_provenance'], proof)
        for status, attention in [('error', 'error'), ('idle', 'error'), ('error', 'finished')]:
            bad = deepcopy(cap); bad['status'] = status
            bad['snapshot'].update(status=status, attentionReason=attention)
            write(capture, bad)
            failed = subprocess.run(cli + ['--raw', row['raw_output_path']], env=env, capture_output=True, timeout=15)
            self.assertNotEqual(failed.returncode, 0)
        changed = deepcopy(cap); changed['snapshot']['attentionTimestamp'] = '2026-09-12T01:03:00Z'
        with self.assertRaisesRegex(life.LifecycleError, 'frozen terminal'):
            self.j.archive_intent(self.j.key(row), changed)
        self.assertEqual(row['archive_attempts_started'], 0)

    @staticmethod
    def wire(payload, prefix=None):
        display = json.dumps(payload)
        if prefix:
            items = payload['availableModes' if prefix == 'availableModes' else 'profiles']
            display = f'{prefix}_count={len(items)}\n{prefix}_ids=' + ','.join(x['id'] for x in items) + '\n\n' + display
        return dict(content=[dict(type='text', text=display)], structuredContent=deepcopy(payload))

    def test_p1_wire_shell_complete_payload_conflicts_and_duplicates(self):
        payload = dict(agentId='fixture', type='codex', status='running', cwd='/fixture', workspaceId='fixture',
                       currentModeId='auto-review', availableModes=[dict(id='auto-review')],
                       lastMessage=None, permission=None, guidance='human guidance')
        wire = self.wire(payload, 'availableModes')
        self.assertEqual(life.mcp_payload(wire, 'create'), payload)
        bads = []
        bad = deepcopy(wire); bad['structuredContent']['agentId'] = 'conflict'; bads.append(bad)
        bad = deepcopy(wire); bad['structuredContent']['permission'] = 0
        bad['content'][0]['text'] = bad['content'][0]['text'].replace('\"permission\": null', '\"permission\": false'); bads.append(bad)
        bad = deepcopy(wire); bad['content'] *= 2; bads.append(bad)
        bad = deepcopy(wire); bad['isError'] = True; bads.append(bad)
        bad = deepcopy(wire); bad['content'][0]['text'] = 'unknown explanation'; bads.append(bad)
        bad = deepcopy(wire); bad['content'][0]['text'] = bad['content'][0]['text'].replace('count=1', 'count=2'); bads.append(bad)
        bad = deepcopy(wire); bad['content'][0]['text'] = '{"agentId":"a","agentId":"b"}'; bads.append(bad)
        for bad in bads:
            with self.assertRaises((life.LifecycleError, life.contextual.ContractError)):
                life.mcp_payload(bad, 'create')
        specs = self.contextual(); self.prepare(specs); key = self.j.key(specs[0])
        data = b'{"op":"recover","op":"create"}'
        with self.assertRaises((ValueError, life.contextual.ContractError)):
            life.host_event(self.j, key, data, outdir=self.root / 'out')
        self.assertEqual(next((self.root / 'out').rglob('*.json')).read_bytes(), data)
        self.assertEqual(self.j.get(key)['status'], 'prepared')

    def test_p1_profiles_mapping_uses_fields_and_rejects_drift(self):
        specs = self.contextual(); self.prepare(specs)
        row = self.j.get(self.j.key(specs[0]))
        profile = dict(id='chosen', name='Wrong model in title', provider='test', model='model',
                       modeId='auto', thinkingOptionId='xhigh', featureValues={'fast_mode': False})
        parameters = life.mcp_create_parameters(row, {'profiles': [profile]}, 'chosen')
        self.assertEqual(parameters['settings']['features'], {'fast_mode': False})
        self.assertEqual(parameters['provider'], 'test/model')
        for field, value in [('provider', 'other'), ('model', 'other'), ('modeId', 'other'),
                             ('thinkingOptionId', 'other')]:
            changed = dict(profile, **{field: value})
            with self.assertRaises(life.LifecycleError):
                life.mcp_create_parameters(row, {'profiles': [changed]}, 'chosen')

    def test_p1_readme_recipe_four_members_and_fault_recovery(self):
        import shutil
        self.assertIsNotNone(shutil.which('node'), 'Node is needed only to execute this README fixture')
        recipe = (ROOT / 'tools/orchestration/README.md').read_text().split('// BEGIN REVIEW_HOST_RECIPE\n')[1].split('// END REVIEW_HOST_RECIPE')[0]
        for fault in ('none', 'create-lost', 'id-crash', 'mirror-crash', 'archive-read-lost', 'archive-budget'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory(prefix='p1-recipe-') as directory:
                # Reuse real envelope/journal constructors; all state and source IO is temporary.
                old_root, old_j, old_selection = self.root, self.j, self.selection
                self.root = Path(directory); self.j = life.Journal(self.root / 'journal.json', root=self.root)
                self.selection = dict(provider='claude/claude-opus-5', modeId='auto', thinkingOptionId='medium',
                                      featureValues={'fast_mode': False})
                try:
                    specs = self.surface(); self.prepare(specs, life.SURFACE)
                    keys = [self.j.key(s) for s in specs]
                    profile = dict(id='chosen', name='Do not infer identity from me', provider='claude',
                                   model='claude-opus-5', modeId='auto', thinkingOptionId='medium', featureValues={'fast_mode': False})
                    captures, natives = {}, {}
                    for row in self.j.rows:
                        key = self.j.key(row); live = self.capture(row)
                        live['snapshot'].update(provider='claude', model='claude-opus-5',
                            persistence=dict(provider='claude', sessionId='session', nativeHandle='session'),
                            runtimeInfo=dict(provider='claude', sessionId=None), createdAt='2026-09-12T01:00:00Z')
                        end = deepcopy(live); end['status'] = 'idle'
                        end['snapshot'].update(status='idle', activeTurn=None, attentionReason='finished',
                                               attentionTimestamp='2026-09-12T01:01:00Z')
                        closed = deepcopy(end); closed['status'] = 'closed'
                        closed['snapshot'].update(status='closed', archivedAt='2026-09-12T01:02:00Z', attentionReason=None,
                                                  attentionTimestamp=None)
                        del closed['snapshot']['activeTurn']
                        create = dict(agentId=live['snapshot']['id'], type='claude', status='running', cwd=str(self.root),
                                      workspaceId=self.ws, currentModeId='auto', availableModes=[dict(id='auto')],
                                      lastMessage=None, permission=None, guidance='fixture')
                        captures[key] = dict(create=self.wire(create, 'availableModes'), live=self.wire(live),
                                             terminal=self.wire(end), closed=self.wire(closed))
                        path = self.root / (row['dispatch_id'] + '.jsonl'); natives[key] = str(path)
                        path.write_bytes(self.native_bytes(self.native_records('claude', self.raw(row).decode(),
                                  cwd=str(self.root), prompt=row['create_parameters']['prompt'])[:-1]))
                    cfg = dict(children=str(self.j.path), outdir=str(self.root / "out ' $(touch NEVER) `false`"),
                               helper=str(ROOT / 'tools/orchestration/review_lifecycle.py'), keys=keys,
                               profileIds={k: 'chosen' for k in keys}, nativeLogs=natives)
                    data = dict(cfg=cfg, captures=captures, profiles=self.wire({'profiles': [profile]}, 'profiles'),
                                archive=self.wire({'success': True}), fault=fault, root=str(self.root))
                    script = self.root / 'fixture.cjs'
                    script.write_text('const data = ' + json.dumps(data) + ';\n' + recipe + self.recipe_runner())
                    self.run_recipe_bridge(script)
                finally:
                    self.root, self.j, self.selection = old_root, old_j, old_selection

    def test_cycle1_direct_intent_stops_without_mutation_and_allows_binding(self):
        specs = self.surface(); self.prepare(specs, life.SURFACE)
        first, second = self.j.rows[:2]
        self.j.create_intent(self.j.key(first), self.profiles)
        self.j.record_id(self.j.key(first), self.capture(first)['snapshot']['id'])
        path = self.root / '.ai/task/surface-task/STATE.json'
        original = life.read(path)
        for stopped in ('WAIT_USER', 'DONE', 'STOP'):
            with self.subTest(state=stopped):
                state = dict(original, state=stopped,
                             wait={'reason': 'user_decision', 'resume_state': 'REVIEW'})
                write(path, state)
                before = self.j.path.read_bytes(), path.read_bytes(), deepcopy(self.j.rows)
                with self.assertRaisesRegex(life.LifecycleError, 'new create blocked: task ' + stopped):
                    self.j.create_intent(self.j.key(second), self.profiles)
                self.assertEqual(before, (self.j.path.read_bytes(), path.read_bytes(), self.j.rows))
                self.assertFalse(list(self.root.glob('*lane-1-2-create-*-profiles.json')))
                # A previously issued create may still complete its first binding.
                self.j.bind(self.j.key(first), self.capture(first))
                self.assertIn('runtime_observation', first)
                self.assertEqual(life.read(path)['state'], stopped)
        write(path, original)
        # Even stale open STATE cannot hide a journal's exhausted archive budget.
        first.update(archive_attempts_started=2, archive_confirmed=False)
        before = deepcopy(self.j.rows)
        with self.assertRaisesRegex(life.LifecycleError, 'unresolved archive budget exhausted'):
            self.j.create_intent(self.j.key(second), self.profiles)
        self.assertEqual(self.j.rows, before)
        self.assertEqual(life.read(path), original)

    def test_cycle1_real_astra_optional_settings(self):
        # Sanitized shape from profiles-execute-astra-01.json: modeId is absent.
        self.selection = dict(provider='codex/gpt-6-astra', thinkingOptionId='high',
                              modeId='auto-review')
        specs = self.contextual(); self.prepare(specs)
        row = self.j.rows[0]
        profile = dict(id='fixture-astra', name='Untrusted display name', provider='codex',
                       model='gpt-6-astra', thinkingOptionId='high', notes='Sanitized fixture')
        before = deepcopy(row)
        payload = life.mcp_payload(self.wire({'profiles': [profile]}, 'profiles'), 'profiles')
        parameters = life.mcp_create_parameters(row, payload, profile['id'])
        self.assertEqual(parameters['provider'], 'codex/gpt-6-astra')
        self.assertEqual(parameters['settings'], dict(modeId='auto-review', thinkingOptionId='high'))
        self.assertEqual(row, before)
        self.assertNotIn('runtime_observation', row)
        fields = [('modeId', 'modeId', 'auto-review', 'other'),
                  ('thinkingOptionId', 'thinkingOptionId', 'high', 'other'),
                  ('featureValues', 'features', {'fast_mode': False}, {'fast_mode': True})]
        for source, target, good, other in fields:
            for declared in ('neither', 'profile', 'frozen', 'both'):
                with self.subTest(source=source, declared=declared):
                    r, p = deepcopy(row), deepcopy(profile)
                    r['create_parameters'].pop(source, None); p.pop(source, None)
                    if declared in ('profile', 'both'): p[source] = good
                    if declared in ('frozen', 'both'): r['create_parameters'][source] = good
                    settings = life.mcp_create_parameters(r, {'profiles': [p]}, p['id'])['settings']
                    if declared == 'neither': self.assertNotIn(target, settings)
                    else: self.assertEqual(settings[target], good)
            p = dict(profile, **{source: other})
            r = deepcopy(row); r['create_parameters'][source] = good
            with self.assertRaisesRegex(life.LifecycleError, 'profile setting drift'):
                life.mcp_create_parameters(r, {'profiles': [p]}, p['id'])
            invalid = (None, '', 0, False, []) + (() if source == 'featureValues' else ({},))
            for value in invalid:
                for side in ('profile', 'frozen', 'both'):
                    with self.subTest(source=source, value=value, side=side):
                        r, p = deepcopy(row), deepcopy(profile)
                        r['create_parameters'].pop(source, None); p.pop(source, None)
                        if side in ('profile', 'both'): p[source] = value
                        if side in ('frozen', 'both'): r['create_parameters'][source] = value
                        with self.assertRaisesRegex(life.LifecycleError, 'invalid profile setting'):
                            life.mcp_create_parameters(r, {'profiles': [p]}, p['id'])
        # Full real-shaped wire to durable intent, without a remote create call.
        data = json.dumps(dict(op='profiles', profile_id=profile['id'],
                               response=self.wire({'profiles': [profile]}, 'profiles'))).encode()
        result = life.host_event(self.j, self.j.key(row), data, outdir=self.root / 'out')
        self.assertEqual(result['parameters'], parameters)
        self.assertEqual(row['create_attempts'][-1]['mcp_parameters'], parameters)
        self.assertEqual(row['create_parameters'], before['create_parameters'])
        self.assertNotIn('runtime_observation', row)

    def test_cycle1_readme_wait_user_other_member_frees_slot(self):
        specs = self.surface(); self.prepare(specs, life.SURFACE)
        a, b, c = self.bind(specs[:3]); d = self.j.rows[3]
        for r in (a, b, c):
            self.j.harvest(self.j.key(r), self.capture(r, 'idle'), self.raw(r),
                           self.root / 'raw', notified=True)
        for _ in range(2):
            self.j.archive_intent(self.j.key(a), self.capture(a, 'idle'))
            with self.assertRaises(life.LifecycleError):
                self.j.confirm_archive(self.j.key(a), self.capture(a, 'idle'))
        captures = {}
        for r in self.j.rows:
            live = self.capture(r)
            created = dict(agentId=live['snapshot']['id'], type='test', status='running',
                           cwd=str(self.root), workspaceId=self.ws, currentModeId='auto',
                           availableModes=[dict(id='auto')], lastMessage=None, permission=None,
                           guidance='fixture only')
            captures[self.j.key(r)] = dict(live=self.wire(live), terminal=self.wire(self.capture(r, 'idle')),
                closed=self.wire(self.capture(r, 'closed')), create=self.wire(created, 'availableModes'))
        cfg = dict(children=str(self.j.path), outdir=str(self.root / "out ' quoted"),
                   keys=[self.j.key(r) for r in self.j.rows],
                   profileIds={self.j.key(d): 'chosen'}, nativeLogs={},
                   helper=str(ROOT / 'tools/orchestration/review_lifecycle.py'))
        profile = dict(id='chosen', provider='test', model='model', modeId='auto', thinkingOptionId='xhigh')
        data = dict(cfg=cfg, captures=captures, profiles=self.wire({'profiles': [profile]}, 'profiles'),
                    archive=self.wire({'success': True}),
                    statepath=str(self.root / '.ai/task/surface-task/STATE.json'))
        recipe = (ROOT / 'tools/orchestration/README.md').read_text().split(
            '// BEGIN REVIEW_HOST_RECIPE\n')[1].split('// END REVIEW_HOST_RECIPE')[0]
        runner = r'''
const assert = require('assert'), fs = require('fs');
const input = require('readline').createInterface({input:process.stdin});
const disk = () => JSON.parse(fs.readFileSync(data.cfg.children));
const state = () => JSON.parse(fs.readFileSync(data.statepath));
const [a,b,c,d] = data.cfg.keys;
const archived = new Set(), archives = [], creates = [], profiles = [];
const keyFor = id => data.cfg.keys.find(k => data.captures[k].live.structuredContent.snapshot.id === id);
const tools = {
  exec_command: async args => {
    const r = await new Promise(resolve => {
      input.once('line', line => resolve(JSON.parse(line)));
      process.stdout.write(JSON.stringify(args) + '\n');
    });
    return {exit_code:r.status, output:r.stdout + r.stderr};
  },
  mcp__paseo__list_profiles: async () => { profiles.push('profiles'); return data.profiles; },
  mcp__paseo__create_agent: async args => {
    assert.equal(state().state, 'REVIEW');
    assert(disk().slice(0,3).every(r => r.archive_confirmed));
    assert.equal(disk()[3].status, 'dispatching');
    assert.equal(args.initialPrompt, disk()[3].create_parameters.prompt);
    creates.push(d); return data.captures[d].create;
  },
  mcp__paseo__get_agent_status: async ({agentId}) => {
    const k = keyFor(agentId);
    return data.captures[k][archived.has(k) ? 'closed' : k === d ? 'live' : 'terminal'];
  },
  mcp__paseo__archive_agent: async ({agentId}) => {
    const k = keyFor(agentId); assert.notEqual(k,a);
    archives.push(k); archived.add(k); return data.archive;
  }
};
const recover = k => reviewHost(tools, data.cfg, {type:'recover-archive', key:k,
  agentId:data.captures[k].live.structuredContent.snapshot.id});
(async () => {
  const beforeD = JSON.stringify(disk()[3]), beforeWait = state().wait;
  assert.deepEqual(beforeWait, {reason:'archive_pending', resume_state:'REVIEW'});
  await recover(b); // Same README archive+fill: B releases capacity while A remains unresolved.
  await reviewHost(tools, data.cfg, {type:'fill'});
  assert.equal(state().state, 'WAIT_USER'); assert.deepEqual(state().wait, beforeWait);
  assert.equal(disk()[0].archive_attempts_started,2); assert.equal(disk()[0].archive_confirmed,false);
  assert.equal(disk()[1].archive_confirmed,true); assert.equal(JSON.stringify(disk()[3]),beforeD);
  assert.equal(creates.length,0); assert.equal(profiles.length,0);
  assert.deepEqual(archives,[b]);
  archived.add(a); await recover(a); // Readback only; no third archive attempt or budget reset.
  assert.equal(disk()[0].archive_attempts_started,2); assert.equal(disk()[0].archive_confirmed,true);
  assert.equal(state().state,'WAIT_USER'); assert.equal(creates.length,0);
  await recover(c); // Existing member uses its remaining budget; normal all-settled recovery.
  assert.equal(state().state,'REVIEW'); assert.equal(state().wait,null);
  assert.deepEqual(archives,[b,c]); assert.deepEqual(creates,[d]); assert.equal(profiles.length,1);
  assert.equal(disk()[0].archive_attempts_started,2); assert.equal(disk()[3].status,'dispatched');
  process.stdout.write(JSON.stringify({verified:true}) + '\n'); input.close();
})().catch(e => {console.error(e); process.exit(1);});
'''
        script = self.root / 'cycle1.cjs'
        script.write_text('const data = ' + json.dumps(data) + ';\n' + recipe + runner)
        self.run_recipe_bridge(script)

    def run_recipe_bridge(self, script):
        # Some environments forbid Node child_process. Python executes the exact
        # recipe command received over a one-request-at-a-time stdio bridge.
        import selectors
        import time
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root))
        with tempfile.TemporaryFile() as errors:
            process = subprocess.Popen(['node', str(script)], env=env, cwd=self.root,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True)
            try:
                selector = selectors.DefaultSelector()
                self.addCleanup(selector.close)
                selector.register(process.stdout, selectors.EVENT_READ)
                deadline = time.monotonic() + 90
                verified = False
                while True:
                    remaining = deadline - time.monotonic()
                    self.assertGreater(remaining, 0, 'README fixture deadline')
                    self.assertTrue(selector.select(remaining), 'README fixture deadline')
                    line = process.stdout.readline()
                    if not line:
                        break
                    request = json.loads(line)
                    if request.get('verified'):
                        verified = True
                        break
                    result = subprocess.run(['/bin/bash', '-c', request['cmd']], env=env,
                                            cwd=self.root, capture_output=True, text=True, timeout=15)
                    process.stdin.write(json.dumps(dict(status=result.returncode, stdout=result.stdout, stderr=result.stderr)) + '\n')
                    process.stdin.flush()
                process.stdin.close()
                code = process.wait(timeout=10)
                errors.seek(0)
                self.assertEqual(code, 0, errors.read().decode())
                self.assertTrue(verified)
            finally:
                if process.poll() is None:
                    process.kill(); process.wait(timeout=10)
                process.stdout.close()
                if not process.stdin.closed:
                    process.stdin.close()

    @staticmethod
    def recipe_runner():
        return r'''
const fs = require('fs'), assert = require('assert');
const input = require('readline').createInterface({input:process.stdin});
const shell = args => new Promise(resolve => {
  input.once('line', line => resolve(JSON.parse(line)));
  process.stdout.write(JSON.stringify(args) + '\n');
});
const {cfg, fault} = data;
const calls = [], archived = new Set(), created = new Set();
let interrupted = false, finished = false, confirmAllowed = fault !== 'archive-budget';
const disk = () => JSON.parse(fs.readFileSync(cfg.children));
const statePath = data.root + '/.ai/task/surface-task/STATE.json';
const keyFor = id => cfg.keys.find(k => data.captures[k].create.structuredContent.agentId === id);
const tools = {
  exec_command: async args => {
    assert(args.cmd.startsWith("printf '%s' "));
    const before = fs.readFileSync(statePath);
    const r = await shell(args);
    if (r.status === 0 && args.cmd.includes('"op":"create"') && fault === 'id-crash' && !interrupted) {
      interrupted = true; throw Error('crash after ID persisted');
    }
    if (r.status === 0 && args.cmd.includes('"op":"bind"') && fault === 'mirror-crash' && !interrupted) {
      fs.writeFileSync(statePath, before); interrupted = true; throw Error('crash before STATE mirror');
    }
    return {exit_code:r.status, output:r.stdout + r.stderr};
  },
  mcp__paseo__list_profiles: async args => {assert.deepEqual(args, {}); calls.push('profiles'); return data.profiles;},
  mcp__paseo__create_agent: async args => {
    const k = cfg.keys.find(k => data.captures[k].live.structuredContent.snapshot.labels.dispatch_id === args.labels.dispatch_id);
    assert.equal(calls.at(-1), 'profiles');
    assert(!disk().some(r => r.status === 'created'));
    const r = disk().find(r => r.dispatch_id === args.labels.dispatch_id);
    assert.equal(r.status, 'dispatching');
    assert.equal(args.provider, 'claude/claude-opus-5'); assert.equal(args.initialPrompt, r.create_parameters.prompt);
    assert.deepEqual(args.settings, {modeId:'auto', thinkingOptionId:'medium', features:{fast_mode:false}});
    assert.deepEqual(Object.keys(args).sort(), ['provider','initialPrompt','title','workspaceId','labels','notifyOnFinish','settings'].sort());
    assert.equal(args.notifyOnFinish, true);
    calls.push('create:' + k); created.add(k);
    if (fault === 'create-lost' && !interrupted) {interrupted = true; throw Error('create response lost');}
    return data.captures[k].create;
  },
  mcp__paseo__get_agent_status: async ({agentId}) => {
    const k = keyFor(agentId); calls.push('status:' + k);
    if (archived.has(k) && fault === 'archive-read-lost' && !interrupted) {
      interrupted = true; throw Error('archive readback lost');
    }
    return data.captures[k][archived.has(k) ? 'closed' : finished ? 'terminal' : 'live'];
  },
  mcp__paseo__archive_agent: async ({agentId}) => {
    const k = keyFor(agentId), r = disk().find(r => r.agent_id === agentId);
    const mirror = JSON.parse(fs.readFileSync(statePath)).child_dispatches.find(c => c.agent_id === agentId);
    assert(r.archive_attempts_started > 0 && r.archive_attempts_started <= 2);
    assert.equal(r.archive_attempts_started, mirror.archive_attempts_started);
    assert.equal(r.validation_state, 'completed'); assert.equal(r.output_valid, true);
    assert(r.native_provenance && r.native_provenance.last_prompt_present === false);
    calls.push('archive:' + k); if (confirmAllowed) archived.add(k);
    return data.archive;
  }
};
(async () => {
  let caught = false;
  try { await reviewHost(tools, cfg, {type:'fill'}); } catch(e) {caught = true;}
  if (['create-lost','id-crash','mirror-crash'].includes(fault)) assert(caught);
  else assert(!caught);
  if (fault === 'create-lost') {
    assert.equal(disk()[0].status, 'dispatching');
    const count = calls.length;
    await assert.rejects(() => reviewHost(tools, cfg, {type:'fill'}), /Ambiguous create/);
    assert.equal(calls.length, count); assert.equal(created.size, 1);
    // Host's unique complete live reconciliation, using existing bind adapter.
    const input = JSON.stringify({op:'bind', response:data.captures[cfg.keys[0]].live});
    const quote = s => "'" + String(s).replace(/'/g, "'\\''") + "'";
    const p = await shell({cmd: "printf '%s' " + quote(input) + ' | ' +
      ['python3','-B',cfg.helper,'host-event',cfg.children,cfg.keys[0],'--outdir',cfg.outdir].map(quote).join(' ')});
    assert.equal(p.status, 0, p.stderr);
  }
  await reviewHost(tools, cfg, {type:'fill'});
  assert.equal(created.size, 3); assert(disk().slice(0,3).every(r => r.runtime_observation));
  assert.equal(JSON.parse(fs.readFileSync(statePath)).child_dispatches.length, 3);
  finished = true;
  const action = {type:'finish', key:cfg.keys[0], agentId:disk()[0].agent_id};
  if (fault === 'archive-budget') {
    await assert.rejects(() => reviewHost(tools, cfg, action));
    await assert.rejects(() => reviewHost(tools, cfg, {...action,type:'recover-archive'}));
    const n = calls.filter(c => c.startsWith('archive:')).length; assert.equal(n,2);
    await assert.rejects(() => reviewHost(tools, cfg, {...action,type:'recover-archive'}), /budget exhausted/);
    assert.equal(calls.filter(c => c.startsWith('archive:')).length, n);
    assert.equal(JSON.parse(fs.readFileSync(statePath)).state, 'WAIT_USER');
    archived.add(cfg.keys[0]); confirmAllowed = true;
    await reviewHost(tools, cfg, {...action,type:'recover-archive'});
    // WAIT_USER resumes only once all existing children are confirmed archived.
    assert.equal(created.size,3);
    for (const key of cfg.keys.slice(1,3)) {
      await reviewHost(tools, cfg, {type:'finish', key, agentId:data.captures[key].live.structuredContent.snapshot.id});
    }
  } else if (fault === 'archive-read-lost') {
    await assert.rejects(() => reviewHost(tools, cfg, action));
    assert.equal(created.size,3);
    await reviewHost(tools, cfg, {...action,type:'recover-archive'});
    assert.equal(calls.filter(c => c.startsWith('archive:')).length,1);
  } else await reviewHost(tools, cfg, action);
  assert.equal(created.size,4);
  assert(calls.indexOf('archive:' + cfg.keys[0]) < calls.indexOf('create:' + cfg.keys[3]));
  if (fault !== 'archive-budget')
    assert(!calls.includes('archive:' + cfg.keys[1]) && !calls.includes('archive:' + cfg.keys[2]));
  const count = calls.length;
  await reviewHost(tools, cfg, action); assert.equal(calls.length,count);
  assert(!fs.existsSync(data.root + '/NEVER'));
  process.stdout.write(JSON.stringify({verified:true, calls}) + '\n'); input.close();
})().catch(e => {console.error(e); process.exit(1);});
'''


if __name__ == '__main__':
    unittest.main()
