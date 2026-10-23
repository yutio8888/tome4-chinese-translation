"""Lossless historical replay, complete observations, and disposable cache faults."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.i18nlib import full_review as fr
from tools.i18nlib import full_review_cache as cache
from tests.i18n import test_full_review as fixtures


class CacheTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.manifest = SimpleNamespace(root=self.root, raw_bytes=b'manifest')
        self.file = self.root / 'input'
        self.file.write_bytes(b'one')
        self.round = self.root / 'round'
        self.round.mkdir()
        self.calls = 0
        # Synthetic tests control identity only; real implementation fingerprinting
        # and hot edits are exercised separately without replacing the algorithm.
        identity = patch.object(cache, 'implementation_identity', return_value={'code': 'fixed'})
        identity.start()
        self.addCleanup(identity.stop)
        self.identity = identity
        environment = patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='on', I18N_FULL_REVIEW_CACHE_TRACE='0')
        environment.start()
        self.addCleanup(environment.stop)
        cache.events.clear()

    def compute(self):
        self.calls += 1
        return {'data': self.file.read_bytes().decode(), ('lane', 1): (set([1, 2]), [True, None]),
                'real': [1.0, -0.0]}

    def run_cache(self, compute=None, outputs=False, seal=None):
        return cache.predecessor(self.manifest, self.round, seal or {'seal': 1}, outputs, compute or self.compute)

    def entries(self):
        return list((self.root / cache.CACHE_RELATIVE).glob('v1-*.json'))

    def hit(self):
        self.assertEqual(cache.events[-1]['event'], 'hit', cache.events)

    def test_cold_warm_fidelity_no_alias_and_disabled_no_directory(self):
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='off'):
            reference = self.run_cache()
        self.assertFalse((self.root / cache.CACHE_RELATIVE).exists())
        cold = self.run_cache()
        warm = self.run_cache()
        self.hit()
        self.assertEqual(cache.canonical(cache.pack(reference)), cache.canonical(cache.pack(cold)))
        self.assertEqual(reference, warm)
        self.assertIs(type(warm['real'][0]), float)
        self.assertEqual(cache.canonical(cache.pack(reference)), cache.canonical(cache.pack(warm)))
        self.assertEqual(self.calls, 2)
        warm[('lane', 1)][1].append('mutation')
        self.assertEqual(self.run_cache(), reference)
        self.hit()
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='ON'), patch.object(cache, '_directory', side_effect=AssertionError):
            self.assertEqual(self.run_cache(), reference)

    def test_every_dependency_kind_is_recorded_and_mutation_recomputes(self):
        listed = self.root / 'listed'
        listed.mkdir()
        (listed/'old').write_text('x')
        missing = self.root/'absent'
        task = self.root/'.ai/task/test/STATE.json'
        task.parent.mkdir(parents=True)
        task.write_bytes(b'task')
        older = self.root/'older/inventory.json'
        older.parent.mkdir()
        older.write_bytes(b'older')
        link = self.root/'link'
        link.symlink_to(self.file)
        def compute():
            self.calls += 1
            # Path.glob and rglob discovery exercise scandir + DirEntry type probes.
            return [self.file.read_bytes().hex(), sorted(p.name for p in listed.glob('*')),
                    sorted(p.name for p in listed.rglob('*')), missing.exists(),
                    task.read_text(), older.read_text(), os.readlink(link)]
        self.run_cache(compute)
        self.run_cache(compute)
        self.hit()
        payload = json.loads(self.entries()[0].read_bytes())['payload']
        kinds = {row[0] for row in payload['dependencies']}
        self.assertEqual(kinds, {'file', 'probe', 'names', 'link'})
        stat_before = self.file.stat()
        mutations = [lambda: (self.file.write_bytes(b'two'), os.utime(self.file, ns=(stat_before.st_atime_ns, stat_before.st_mtime_ns))),
                     lambda: (listed/'new').write_text('x'), lambda: (listed/'old').unlink(),
                     lambda: missing.touch(), lambda: task.write_bytes(b'TASK'),
                     lambda: older.write_bytes(b'OLDER'),
                     lambda: (link.unlink(), link.symlink_to(older))]
        for mutate in mutations:
            before = self.calls
            mutate()
            actual = self.run_cache(compute)
            self.assertEqual(self.calls, before + 1, cache.events)
            self.assertEqual(actual, compute())
            self.run_cache(compute)
            self.hit()

    def test_unrelated_siblings_hit_but_semantic_probe_and_listing_changes_miss(self):
        # Model the actual ordinary() ancestor probes without writing task records
        # in the repository. Only directories explicitly enumerated bind names.
        parents = [self.root, self.root/'.ai/task', self.root/'.ai/reviews',
                   self.root/'evidence/full-review/release-20261013']
        files = []
        for parent in parents:
            path = parent/'existing/input'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fixed')
            files.append(path)
        probe = self.root/'probed'
        probe.mkdir()
        absent = self.root/'absent'
        listed = self.root/'listed'
        listed.mkdir()
        def compute():
            self.calls += 1
            return [[fr.ordinary(p).hex() for p in files], probe.is_dir(),
                    probe.exists(), absent.exists(), sorted(os.listdir(listed))]
        expected = self.run_cache(compute)
        self.run_cache(compute)
        self.hit()
        for parent in parents:
            sibling = parent/'unrelated-new-task-or-round'
            sibling.mkdir()
            self.assertEqual(self.run_cache(compute), expected)
            self.hit()
            sibling.rmdir()
            self.assertEqual(self.run_cache(compute), expected)
            self.hit()
        self.assertEqual(self.calls, 1)
        # Permission/mtime/size/inode changes are irrelevant to these probes.
        probe.chmod(0o700)
        os.utime(probe, (1, 1))
        self.run_cache(compute)
        self.hit()
        for mutate in (lambda: (probe.rmdir(), probe.touch()), probe.unlink,
                       absent.touch, lambda: (listed/'new').touch(),
                       lambda: (listed/'new').unlink()):
            before = self.calls
            mutate()
            actual = self.run_cache(compute)
            self.assertEqual(self.calls, before + 1, cache.events)
            self.assertEqual(actual, compute())
            self.run_cache(compute)
            self.hit()

    def test_direntry_inode_refuses_publication(self):
        def compute():
            with os.scandir(self.round) as entries:
                return [entry.inode() for entry in entries]
        (self.round/'file').touch()
        self.assertTrue(self.run_cache(compute))
        self.assertEqual(self.entries(), [])
        self.assertIn('inode', cache.events[-1]['reason'])

    def test_absent_listing_and_caught_failed_open_are_dependencies(self):
        directory = self.root/'future-directory'
        missing = self.root/'future-file'
        def compute():
            self.calls += 1
            try:
                with os.scandir(directory) as stream:
                    names = sorted(e.name for e in stream)
            except FileNotFoundError:
                names = None
            try:
                text = missing.read_text()
            except FileNotFoundError:
                text = None
            return [names, text]
        self.assertEqual(self.run_cache(compute), [None, None])
        self.run_cache(compute)
        self.hit()
        directory.mkdir()
        self.assertEqual(self.run_cache(compute), [[], None])
        self.assertEqual(self.calls, 2)
        missing.write_text('new')
        self.assertEqual(self.run_cache(compute), [[], 'new'])
        self.assertEqual(self.calls, 3)

    def test_open_records_actual_descriptor_and_trace_failure_is_harmless(self):
        replacement = self.root/'replacement'
        replacement.write_bytes(b'two')
        original_pread = os.pread
        def observed_pread(fd, size, offset):
            block = original_pread(fd, size, offset)
            if offset == 0 and replacement.exists():
                os.replace(replacement, self.file)
            return block
        def compute():
            with open(self.file, 'rb') as stream:
                return stream.read().decode()
        with patch.object(os, 'pread', side_effect=observed_pread):
            self.assertEqual(self.run_cache(compute), 'one')
        self.assertEqual(self.entries(), [])  # path is now different from observed fd
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE_TRACE='1'), patch(
                'builtins.print', side_effect=BrokenPipeError):
            self.assertEqual(self.run_cache(), self.compute())
        self.run_cache()
        self.hit()

    def test_fifo_dependency_and_cache_file_do_not_block(self):
        # A real checker ordinary read rejects FIFO by its type before opening.
        # Cache verification must fall back to exactly that error, without a
        # blocking open of the replaced dependency. The suite has a short timeout.
        def compute():
            return fr.ordinary(self.file).decode()
        self.assertEqual(self.run_cache(compute), 'one')
        self.file.unlink()
        os.mkfifo(self.file)
        with self.assertRaisesRegex(fr.FullReviewError, 'not an ordinary file'):
            self.run_cache(compute)
        self.file.unlink()
        self.file.write_bytes(b'one')
        self.run_cache(compute)
        path = self.entries()[0]
        path.unlink()
        os.mkfifo(path)
        self.assertEqual(self.run_cache(compute), 'one')
        self.assertTrue(path.is_file())

    def test_flags_seal_manifest_and_implementation_separate_keys(self):
        self.run_cache()
        for kwargs in ({'outputs': True}, {'seal': {'seal': 2}}):
            before = self.calls
            self.run_cache(**kwargs)
            self.assertEqual(self.calls, before + 1)
        self.manifest.raw_bytes = b'changed'
        self.run_cache()
        self.assertEqual(self.calls, 4)
        with patch.object(cache, 'implementation_identity', return_value={'code': 'changed'}):
            self.run_cache()
        self.assertEqual(self.calls, 5)

    def test_corruption_truncation_mistypes_digest_and_symlink_miss(self):
        self.run_cache()
        path = self.entries()[0]
        for raw in (b'', b'{', b'[]', b'{"payload":{},"sha256":"bad"}',
                    b'{"payload":{},"payload":{},"sha256":"bad"}', b'NaN'):
            path.write_bytes(raw)
            before = self.calls
            self.assertEqual(self.run_cache(), self.compute())
            self.assertEqual(self.calls, before + 2)
        raw = path.read_bytes()
        target = self.root/'target'
        target.write_bytes(raw)
        path.unlink()
        path.symlink_to(target)
        before = self.calls
        self.run_cache()
        self.assertEqual(self.calls, before + 1)
        self.assertEqual(target.read_bytes(), raw)
        self.assertFalse(path.is_symlink())
        envelope = json.loads(raw)
        envelope['payload']['value'] = ['unknown', []]
        envelope['sha256'] = cache.digest(cache.canonical(envelope['payload']))
        path.write_bytes(cache.canonical(envelope))
        before = self.calls
        self.run_cache()
        self.assertEqual(self.calls, before + 1)

    def test_failures_propagate_and_never_publish(self):
        error = fr.FullReviewError('original failure')
        def fail():
            self.file.read_bytes()
            raise error
        for _ in range(2):
            with self.assertRaises(fr.FullReviewError) as caught:
                self.run_cache(fail)
            self.assertIs(caught.exception, error)
        self.assertEqual(self.entries(), [])
        self.run_cache()
        self.file.unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_cache()

    def test_cache_read_write_errors_only_cost_replay(self):
        with patch.object(cache, '_load', side_effect=PermissionError), patch.object(cache, '_publish', side_effect=PermissionError):
            self.assertEqual(self.run_cache(), self.compute())
        self.assertEqual(self.entries(), [])
        with patch.object(cache, '_directory', side_effect=PermissionError):
            self.assertEqual(self.run_cache(), self.compute())
        self.assertEqual(cache._active.get(), None)

    def test_nested_dependencies_compose_and_original_error_returns(self):
        older = self.root/'older'
        older.write_bytes(b'good')
        def nested():
            if older.read_bytes() != b'good':
                raise fr.FullReviewError('old evidence drift')
            return {'inner': (1, 2)}
        def outer():
            self.file.read_bytes()
            return self.run_cache(nested, seal={'inner': 1})
        self.run_cache(nested, seal={'inner': 1})
        self.run_cache(outer)
        self.assertTrue(any(e['event'] == 'hit' for e in cache.events))
        self.run_cache(outer)
        self.hit()
        self.assertEqual(len(self.entries()), 2)
        older.write_bytes(b'fail')
        with self.assertRaisesRegex(fr.FullReviewError, 'old evidence drift'):
            self.run_cache(outer)

    def test_untracked_git_fd_and_warm_fixedreader_refuse_publication(self):
        from orchestration.build_evidence_pack import FixedReader
        reader = FixedReader()
        reader.files[(str(self.root), 'input')] = b'one'
        operations = [lambda: subprocess.run(['git', '--version'], check=True, capture_output=True),
                      lambda: reader.unpinned(self.root, 'input'),
                      lambda: os.close(os.open(self.file, os.O_RDONLY))]
        for operation in operations:
            def compute():
                self.file.read_bytes()
                operation()
                return {'success': True}
            self.assertEqual(self.run_cache(compute), {'success': True})
            self.assertEqual(cache.events[-1]['event'], 'skip', cache.events)
            self.assertEqual(self.entries(), [])

    def test_unsupported_value_never_approximated(self):
        def compute():
            self.file.read_bytes()
            return {'path': Path('unsupported')}
        self.assertEqual(self.run_cache(compute), {'path': Path('unsupported')})
        self.assertEqual(self.entries(), [])

    def test_concurrent_same_key_atomic_and_eviction_bounds(self):
        self.run_cache()
        raw = self.entries()[0].read_bytes()
        name = self.entries()[0].name
        # Workers never patch os.environ. Readers must see complete payloads
        # throughout concurrent atomic replacements of exactly the same key.
        def publish(_):
            cache._publish(self.root, name, raw)
            return json.loads((self.root/cache.CACHE_RELATIVE/name).read_bytes())
        with ThreadPoolExecutor(max_workers=4) as executor:
            for value in executor.map(publish, range(16)):
                self.assertEqual(value, json.loads(raw))
        directory = self.root/cache.CACHE_RELATIVE
        foreign = directory/'foreign.json'
        foreign.write_bytes(b'foreign')
        link = directory/('v1-'+'f'*64+'.json')
        link.symlink_to(self.file)
        for i in range(12):
            self.run_cache(seal={'seal': i+10})
        ordinary = [p for p in self.entries() if not p.is_symlink()]
        self.assertLessEqual(len(ordinary), cache.MAX_ENTRIES)
        self.assertLessEqual(sum(p.stat().st_size for p in ordinary), cache.MAX_TOTAL_BYTES)
        self.assertTrue(link.is_symlink())
        self.assertEqual(foreign.read_bytes(), b'foreign')
        with patch.object(cache, 'MAX_TOTAL_BYTES', len(raw)*2+100):
            self.run_cache(seal={'byte-bound': 1})
            self.run_cache(seal={'byte-bound': 2})
            ordinary = [p for p in self.entries() if not p.is_symlink()]
            self.assertLessEqual(sum(p.stat().st_size for p in ordinary), cache.MAX_TOTAL_BYTES)
        with patch.object(cache, 'MAX_TOTAL_BYTES', 2):
            self.run_cache(seal={'oversized': True})
        self.assertEqual(cache.events[-1]['event'], 'skip')

    def test_caps_retain_export_and_merge_entries_for_recent_rounds(self):
        # Regression: two ~300 MB keys (outputs-only export, complete merge) for
        # each of two recent rounds must coexist with headroom for growth.
        self.assertGreaterEqual(cache.MAX_ENTRIES, 4)
        self.assertGreaterEqual(cache.MAX_TOTAL_BYTES, 4 * 500 * 1024 * 1024)

    def test_real_implementation_identity_and_hot_edit_refusal(self):
        self.identity.stop()
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'tools').mkdir()
            (root/'i18n/quality').mkdir(parents=True)
            code = root/'tools/checker.py'
            code.write_bytes(b'x = 1\n')
            # Use a fixed start bound to prove both code and non-Python rules
            # are refused after startup, without sleeping in the test.
            start = code.stat().st_mtime_ns + 10_000_000_000
            with patch.object(cache.precedent, '_process_start_ns', return_value=start), patch.object(
                    cache.precedent, '_loaded_modules', return_value=[]):
                first = cache.precedent.implementation_identity(root)
                code.write_bytes(b'x = 2\n')
                with self.assertRaises(cache.precedent._Skip):
                    cache.precedent.implementation_identity(root)
            self.assertIn('code_sha256', first)
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'tools').mkdir()
            (root/'i18n/quality').mkdir(parents=True)
            rule = root/'i18n/quality/policy.json'
            rule.write_bytes(b'{}')
            start = rule.stat().st_mtime_ns + 10_000_000_000
            with patch.object(cache.precedent, '_process_start_ns', return_value=start), patch.object(
                    cache.precedent, '_loaded_modules', return_value=[]):
                cache.precedent.implementation_identity(root)
                rule.write_bytes(b'[]')
                with self.assertRaises(cache.precedent._Skip):
                    cache.precedent.implementation_identity(root)
        with patch.object(cache, 'implementation_identity', side_effect=ValueError('hot code')):
            self.assertEqual(self.run_cache(), self.compute())
            self.assertEqual(self.entries(), [])

    def test_newer_round_reuses_inner_hit_and_composes_its_dependencies(self):
        fixture = fixtures.SuccessorTests('runTest')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='off'):
            first, middle, last, expected = fixture.three_round_chain()
        self.assertEqual(fr.check(fixture.manifest, middle), expected)
        cache.events.clear()
        original = fr._check
        historical = []
        def observed(manifest, directory, **kwargs):
            if kwargs.get('_historical'):
                historical.append(Path(directory))
            return original(manifest, directory, **kwargs)
        with patch.object(fr, '_check', side_effect=observed):
            self.assertEqual(fr.check(fixture.manifest, last), expected)
        self.assertEqual(historical, [middle])  # first was reverified from cache
        self.assertTrue(any(e['event'] == 'hit' for e in cache.events))
        entries = list((fixture.root/cache.CACHE_RELATIVE).glob('v1-*.json'))
        payloads = [json.loads(p.read_bytes())['payload'] for p in entries]
        outer = next(p for p in payloads if p['key']['directory'] == str(middle))
        self.assertIn(str(first/'inventory.json'), [r[1] for r in outer['dependencies']])
        # Terminal .ai inputs lie outside both sealed round trees. A later hit
        # still notices their drift and raises exactly the original checker error.
        path = fixture.state_path
        state = json.loads(path.read_bytes())
        state['child_dispatches'][0]['archive_confirmed'] = False
        path.write_bytes(fr.canonical(state))
        with self.assertRaises(fr.FullReviewError) as cached:
            fr.check(fixture.manifest, last)
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='off'):
            with self.assertRaises(fr.FullReviewError) as fresh:
                fr.check(fixture.manifest, last)
        self.assertEqual(str(cached.exception), str(fresh.exception))

    def test_three_round_checker_differential_and_current_checks_survive_hit(self):
        fixture = fixtures.SuccessorTests('runTest')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        with patch.dict(os.environ, I18N_FULL_REVIEW_CACHE='off'):
            first, middle, last, _ = fixture.three_round_chain()
            reference = fr.check(fixture.manifest, last, _details=True)
        cache.events.clear()
        cold = fr.check(fixture.manifest, last, _details=True)
        warm = fr.check(fixture.manifest, last, _details=True)
        self.hit()
        self.assertEqual(cache.canonical(cache.pack(reference)), cache.canonical(cache.pack(cold)))
        self.assertEqual(cold, warm)
        self.assertEqual(len(list((fixture.root/cache.CACHE_RELATIVE).glob('v1-*.json'))), 1)
        with patch.object(fr, 'source_file', return_value={'content': 'hello', 'sha256': fr.sha(b'hello')}) as sources:
            self.assertEqual(fr.check(fixture.manifest, last, _details=True), reference)
            self.hit()
            self.assertGreater(sources.call_count, 0)
        # Current state is checked before lookup; older evidence is reverified
        # from the dependency list even though the immediate middle seal is intact.
        with patch.object(fr, 'validate_current', side_effect=fr.FullReviewError('current failure')):
            with self.assertRaisesRegex(fr.FullReviewError, 'current failure'):
                fr.check(fixture.manifest, last)
        old = first/'inventory.json'
        old.write_bytes(old.read_bytes()+b' ')
        with self.assertRaisesRegex(fr.FullReviewError, 'predecessor frozen evidence drift'):
            fr.check(fixture.manifest, last)
        self.assertEqual(cache.events[-1]['event'], 'miss')


class EntryScriptTests(unittest.TestCase):
    def test_native_profiler_is_preserved(self):
        source = """
import cProfile, sys
sys.path.insert(0, 'tools')
p = cProfile.Profile()
p.enable()
previous_finders = tuple(sys.meta_path)
from i18nlib import full_review as f
from i18nlib import full_review_cache as c
assert sys.getprofile() is p
assert tuple(sys.meta_path) == previous_finders
p.disable()
"""
        result = subprocess.run([sys.executable, '-B', '-c', source],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cross_entry_shared_reader_and_progress_wrapper(self):
        # Real identities in separate processes, without synthetic identity mocks.
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'input').write_text('fixed')
            source = """
import json, sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, 'tools')
from i18nlib import full_review as f
from i18nlib import full_review_cache as c
root = Path(sys.argv[1])
if sys.argv[2] == 'wrapped':
    reader = f.FixedReader()
    f.FixedReader = lambda: reader
    original = f.read
    def progress(*args, **kwargs):
        return original(*args, **kwargs)
    f.read = progress
m = SimpleNamespace(root=root, raw_bytes=b'manifest')
assert c.predecessor(m, root/'round', {'seal': 1}, False,
                     lambda: (root/'input').read_text()) == 'fixed'
print(json.dumps(c.events))
"""
            first, second = root/'first.py', root/'second.py'
            first.write_text(source)
            second.write_text(source + '\n# A different entry script.\n')
            environment = {**os.environ, 'I18N_FULL_REVIEW_CACHE': 'on',
                           'I18N_FULL_REVIEW_CACHE_TRACE': '0'}

            def run(script, mode):
                result = subprocess.run([sys.executable, '-B', str(script), str(root), mode],
                                        env=environment, capture_output=True, text=True, check=True,
                                        timeout=20)
                return json.loads(result.stdout)

            events = run(first, 'normal')
            self.assertEqual(events[-1]['event'], 'publish', events)
            entries = list((root/cache.CACHE_RELATIVE).glob('v1-*.json'))
            self.assertEqual(len(entries), 1)
            self.assertEqual(run(second, 'normal')[-1]['event'], 'hit')
            self.assertEqual(run(second, 'wrapped')[-1]['event'], 'hit')
            entries[0].unlink()
            self.assertEqual(run(second, 'wrapped')[-1]['event'], 'publish')
            self.assertEqual(run(first, 'normal')[-1]['event'], 'hit')


if __name__ == '__main__':
    unittest.main()
