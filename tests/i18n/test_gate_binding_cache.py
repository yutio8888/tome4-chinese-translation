"""Cache/reference equivalence and explicit, identity-bound receipt reuse."""
import copy
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
from unittest import mock, TestCase

from tests.i18n.test_ci_gates import GateResultsTests as _Fixture
from tools.i18nlib import gate_results as gates


# Do not re-export the fixture TestCase: the registry owns it in test_ci_gates.
class BindingCacheTests(TestCase):
    setUp = _Fixture.setUp
    git = _Fixture.git
    execute = _Fixture.execute
    def test_reference_equivalence_and_invalidation(self):
        def equal():
            cached = gates.binding(self.root)
            self.assertEqual(gates.canonical(cached), gates.canonical(gates.binding(self.root, use_cache=False)))
            return cached
        initial = equal()
        with mock.patch.object(gates, '_file_identity', wraps=gates._file_identity) as reader:
            self.assertEqual(initial, equal())
            # Only the uncached reference calls the reader on warm files.
            self.assertEqual(reader.call_count, 2)
        path = self.root / 'source'
        before = path.stat()
        path.write_bytes(b'Candidate\n')  # same size; restored mtime must not hide ctime
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        self.assertNotEqual(initial, equal())
        previous = equal()
        os.utime(path, None)
        with mock.patch.object(gates, '_file_identity', wraps=gates._file_identity) as reader:
            self.assertEqual(previous, gates.binding(self.root))
            self.assertEqual(reader.call_count, 1)
        self.assertEqual(previous, equal())  # touch changes the key, not byte identity
        path.chmod(0o755)
        self.assertNotEqual(previous, equal())
        path.unlink()
        equal()
        path.symlink_to('missing')
        first = equal()
        path.unlink(); path.symlink_to('different')
        self.assertNotEqual(first, equal())
        (self.root / 'added').write_text('new')
        equal()
        cache = self.root / '.artifacts/i18n/gate-binding-cache.json'
        for raw in (b'{', b'{"version":NaN}', b'{"version":1,"version":1}', b'[]',
                    b'{"version":1,"entries":null,"entries_sha256":"bad"}', b'[' * 2000):
            cache.write_bytes(raw)
            equal()
        payload = json.loads(cache.read_bytes())
        payload['entries']['added'][1][1] = 'a' * 64
        cache.write_text(json.dumps(payload))
        equal()  # valid JSON accidental corruption also discards the cache
        with mock.patch('tools.i18nlib.gate_binding_cache.os.replace', side_effect=OSError('disk')):
            equal()
        with mock.patch('tools.i18nlib.gate_binding_cache.fingerprint', side_effect=OSError('stat error')):
            equal()
        with mock.patch.dict(os.environ, {'I18N_GATE_BINDING_CACHE': 'off'}):
            self.assertEqual(gates.binding(self.root), gates.binding(self.root, use_cache=False))

    def test_change_between_cache_hit_and_second_stat_rehashes(self):
        from tools.i18nlib.gate_binding_cache import BindingCache, fingerprint
        gates.binding(self.root)
        cache = BindingCache(self.root)
        path = self.root / 'source'
        calls = []
        def race(p):
            calls.append(p)
            if len(calls) == 2:
                path.write_bytes(b'Candidate\n')
            return fingerprint(p)
        with mock.patch('tools.i18nlib.gate_binding_cache.fingerprint', side_effect=race):
            observed = cache.identity('source', path, gates._file_identity)
        self.assertEqual(observed, gates._file_identity(path))
        self.assertNotIn('source', cache.updated)
        self.assertEqual(len(calls), 2)  # bounded fallback, no retry loop

    def test_midrun_same_size_restored_mtime(self):
        path = self.root / 'source'
        before = path.stat()
        def mutate(argv, root, log):
            path.write_bytes(b'Candidate\n')
            os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
            return self.execute(argv, root, log)
        with redirect_stdout(io.StringIO()):
            result = gates.run(self.root, self.selected, execute=mutate)
        self.assertFalse(result['success'])
        self.assertIn('binding changed', result['error'])


class ReuseTests(TestCase):
    base_setup = _Fixture.setUp
    git = _Fixture.git
    execute = _Fixture.execute
    def setUp(self):
        self.base_setup()
        self.selected.update(full_review_task={'task_id': 'fixture'}, round_id='round-one')
        self.round = '.artifacts/i18n/measurement-round'
        (self.root / 'tools').mkdir()
        (self.root / 'tools/tool.py').write_text('input')

    def run_schema3(self, **kw):
        with redirect_stdout(io.StringIO()):
            return gates.run(self.root, self.selected, execute=self.execute, reuse_round=self.round, **kw)

    def archive(self, result, export):
        path = self.root / self.round / 'task-gates' / 'fixture' / export / 'results.json'
        for record in result['checks']:
            log = path.parent / record['id'] / 'output.log'
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_bytes(gates.record_output(self.root, record))
        path.write_bytes(gates.canonical(result))
        return path

    def test_reuse_only_tests_and_off_switch(self):
        first = self.run_schema3(reuse=False)
        source = self.archive(first, 'one')
        self.calls.clear()
        second = self.run_schema3()
        gates.validate(second, selected=self.selected, root=self.root)
        reused = [r for r in second['checks'] if 'reuse' in r]
        self.assertEqual({r['id'] for r in reused}, gates.REUSABLE_TESTS)
        self.assertEqual(len(self.calls), len(gates.CHECKS) - len(gates.REUSABLE_TESTS))
        self.assertTrue(all(not {'started_at', 'finished_at', 'exit_code', 'log_path'} & r.keys() for r in reused))
        self.assertTrue(all(r['reuse']['receipt_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest() for r in reused))
        archived = self.archive(second, 'two')
        gates.validate_historical(second, selected=self.selected, root=self.root, receipt_path=archived)
        self.calls.clear()
        third = self.run_schema3(reuse=False)
        self.assertEqual(len(self.calls), len(gates.CHECKS))
        self.assertFalse(any('reuse' in r for r in third['checks']))
        (self.root / 'tools/tool.py').write_text('changed')
        self.assertFalse(any('reuse' in r for r in self.run_schema3()['checks']))
        # Historical identities remain valid after current tools change.
        gates.validate_historical(second, selected=self.selected, root=self.root, receipt_path=archived)
        with self.assertRaises(gates.GateError):
            gates.validate(second, selected=self.selected, root=self.root,
                           expected_test_identities=gates.test_identities(self.root))

    def test_strict_reuse_rejections(self):
        first = self.run_schema3()
        source = self.archive(first, 'one')
        raw = source.read_bytes()
        second = self.run_schema3()
        index = next(i for i, r in enumerate(second['checks']) if 'reuse' in r)
        def rejected(result):
            with self.assertRaises(gates.GateError):
                gates.validate_historical(result, selected=self.selected, root=self.root)
        for field, value in [('receipt_path', self.round + '/task-gates/f/missing/results.json'),
                             ('receipt_path', '.artifacts/i18n/other/task-gates/f/e/results.json'),
                             ('receipt_sha256', 'a'*64), ('log_sha256', 'b'*64)]:
            bad = copy.deepcopy(second); bad['checks'][index]['reuse'][field] = value; rejected(bad)
        bad = copy.deepcopy(second); bad['checks'][index]['test_identity_sha256'] = 'c'*64; rejected(bad)
        bad = copy.deepcopy(second); bad['checks'][0] = dict(bad['checks'][index], id='01-doctor'); rejected(bad)
        bad = copy.deepcopy(second); bad['checks'][index]['exit_code'] = 0; rejected(bad)
        for change in ('failed', 'identity', 'cycle'):
            damaged = copy.deepcopy(first)
            if change == 'failed':
                damaged['checks'][0]['exit_code'] = 1
            elif change == 'identity':
                damaged['checks'][index]['test_identity_sha256'] = 'd'*64
            else:
                damaged['checks'][index] = copy.deepcopy(second['checks'][index])
            source.write_bytes(gates.canonical(damaged))
            bad = copy.deepcopy(second)
            bad['checks'][index]['reuse']['receipt_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
            rejected(bad)
            source.write_bytes(raw)
        log = source.parent / first['checks'][index]['id'] / 'output.log'
        log.write_bytes(b'changed')
        rejected(second)
        source.unlink(); rejected(second)

    def test_corrupt_source_falls_back_and_explicit_validation_rejects(self):
        first = self.run_schema3()
        source = self.archive(first, 'one')
        second = self.run_schema3()
        index = next(i for i, r in enumerate(second['checks']) if 'reuse' in r)
        for raw in (b'[]', b'null', b'{', b'{"success":true,"success":false}'):
            source.write_bytes(raw)
            self.assertFalse(any('reuse' in r for r in self.run_schema3()['checks']))
            bad = copy.deepcopy(second)
            bad['checks'][index]['reuse']['receipt_sha256'] = hashlib.sha256(raw).hexdigest()
            with self.assertRaises(gates.GateError):
                gates.validate_historical(bad, selected=self.selected, root=self.root)

    def test_environment_off_never_consults_sources(self):
        self.archive(self.run_schema3(), 'one')
        with mock.patch.dict(os.environ, {'I18N_GATE_TEST_REUSE': 'off'}), mock.patch.object(
                gates, '_reuse_sources', side_effect=AssertionError('must execute')):
            result = self.run_schema3()
        self.assertTrue(result['success'])
        self.assertFalse(any('reuse' in r for r in result['checks']))

    def test_identity_environment_argv_and_candidate_independence(self):
        original = gates.test_identities(self.root)
        (self.root / 'source').write_text('candidate change')
        changed_inputs = gates.test_identities(self.root)
        for name in gates.REUSABLE_TESTS:
            self.assertEqual(original[name] == changed_inputs[name], name in gates.NARROW_TESTS)
        with mock.patch.dict(os.environ, {'GATE_TEST_ENV': 'different'}):
            self.assertNotEqual(original, gates.test_identities(self.root))
        changed = copy.deepcopy(gates.CHECKS)
        changed[2][1].append('--different')
        with mock.patch.object(gates, 'CHECKS', changed):
            self.assertNotEqual(original, gates.test_identities(self.root))

    def test_broad_dependency_edits_invalidate_reuse(self):
        paths = ('AGENTS.md', 'docs/rules.md', 'mod-tome.lua',
                 'evidence/quality/regression.json', 'evidence/production-review/fixture.json',
                 gates.TEST_IGNORED_INPUTS[0], 'tools/__pycache__/fixture.pyc')
        for name in paths:
            with self.subTest(path=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('before')
                self.archive(self.run_schema3(reuse=False), 'source')
                path.write_text('after')
                result = self.run_schema3()
                self.assertTrue(result['success'])
                reused = {r['id'] for r in result['checks'] if 'reuse' in r}
                self.assertFalse(reused & gates.BROAD_TESTS)
                self.assertEqual(reused, set() if name.startswith('tools/') else gates.NARROW_TESTS)

    def test_lane_writes_do_not_change_test_identity(self):
        original = gates.test_identities(self.root)
        for name in ('evidence/full-review/round-one/task-gates/new/results.json',
                     'evidence/full-review/round-one/pilot.json', '.ai/task/new/STATE.json',
                     '.ai/reviews/new/raw.txt', '.artifacts/i18n/ci-gates/new/output.log'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            for text in ('new', 'edited'):
                path.write_text(text)
                self.assertEqual(original, gates.test_identities(self.root))

    def test_head_index_and_git_inputs_invalidate_broad_identity(self):
        original = gates.test_identities(self.root)
        real_git = gates._git
        for args in (('rev-parse', 'HEAD'), ('ls-files', '--stage', '-z'),
                     ('for-each-ref', '--format=%(refname) %(objectname)'),
                     ('config', '--null', '--list', '--show-origin')):
            with self.subTest(args=args):
                def changed(root, *command):
                    value = real_git(root, *command)
                    return value + b'changed' if command == args else value
                with mock.patch.object(gates, '_git', side_effect=changed):
                    current = gates.test_identities(self.root)
                for name in gates.REUSABLE_TESTS:
                    self.assertEqual(original[name] == current[name], name in gates.NARROW_TESTS)
        path = self.root / '.git/info/exclude'
        path.write_text('changed-exclusion\n')
        current = gates.test_identities(self.root)
        self.assertTrue(all(original[n] != current[n] for n in gates.BROAD_TESTS))

    def test_quality_facts_always_executes(self):
        self.archive(self.run_schema3(), 'one')
        second = self.run_schema3()
        record = next(r for r in second['checks'] if r['id'] == '04-quality-facts-unit-tests')
        self.assertNotIn('reuse', record)
        self.assertNotIn('test_identity_sha256', record)

    def test_external_content_change_prevents_broad_reuse(self):
        from tools.i18nlib.gate_binding_cache import BindingCache
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            native = Path(directory) / 'native'
            native.write_bytes(b'before')
            def external(root, cache):
                return {'files': {str(native): cache.identity(str(native), native, gates._file_identity)
                                  if cache else gates._file_identity(native)}}
            with mock.patch.object(gates, '_test_external_inputs', side_effect=external):
                self.archive(self.run_schema3(), 'one')
                native.write_bytes(b'after')
                second = self.run_schema3()
            self.assertEqual({r['id'] for r in second['checks'] if 'reuse' in r}, gates.NARROW_TESTS)

    def test_symlink_content_and_uncovered_targets(self):
        target = self.root / 'tools/target'
        target.write_bytes(b'before')
        link = self.root / 'i18n/config'
        link.parent.mkdir()
        link.symlink_to('../tools/target')
        self.archive(self.run_schema3(), 'one')
        target.write_bytes(b'after')
        self.assertFalse(any('reuse' in r for r in self.run_schema3()['checks']))
        excluded = self.root / '.ai/task/hidden'
        excluded.parent.mkdir(parents=True)
        excluded.write_bytes(b'before')
        link.unlink()
        link.symlink_to('../.ai/task/hidden')
        self.assertEqual(gates.test_identities(self.root), {})
        self.archive(self.run_schema3(), 'excluded')
        excluded.write_bytes(b'after')
        result = self.run_schema3()
        self.assertTrue(result['success'])
        self.assertFalse(any('reuse' in r for r in result['checks']))
        gates.validate(result, selected=self.selected, root=self.root)
        link.unlink()
        link.symlink_to('/etc/hosts')
        self.assertEqual(gates.test_identities(self.root), {})

    def test_external_symlink_to_excluded_lane_refuses_reuse(self):
        excluded = self.root / '.ai/task/hidden'
        excluded.parent.mkdir(parents=True)
        excluded.write_text('before')
        link = self.root / '.git/info/exclude'
        link.unlink()
        link.symlink_to(excluded)
        self.assertEqual(gates.test_identities(self.root), {})
        self.archive(self.run_schema3(), 'one')
        excluded.write_text('after')
        result = self.run_schema3()
        self.assertTrue(result['success'])
        self.assertFalse(any('reuse' in r for r in result['checks']))

    def test_broad_cache_matches_reference_and_preserves_excluded_entries(self):
        from tools.i18nlib.gate_binding_cache import BindingCache
        path = self.root / 'evidence/full-review/round-one/large'
        path.parent.mkdir(parents=True)
        path.write_text('expensive evidence')
        gates.binding(self.root)
        original = gates.test_identities(self.root)
        self.assertIn(path.relative_to(self.root).as_posix(), BindingCache(self.root).entries)
        # Keep the environment fixed while selecting the reference implementation.
        with mock.patch.object(gates, 'BindingCache', return_value=None):
            self.assertEqual(original, gates.test_identities(self.root))


# The registry owns the base fixture in test_ci_gates.
del _Fixture
