from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools import review_phase_timing as timing


class PhaseTimingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patcher = patch.object(timing, 'ROOT', self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.path = self.root / '.artifacts/i18n/timing/batch.json'

    def invoke(self, command, *args, seconds=0, domain='boot:namespace', utc='2026-09-05T12:00:00+00:00'):
        with patch.object(timing, 'clock_sample', return_value={
                'utc': utc, 'monotonic_ns': int(seconds * 1e9), 'clock_domain': domain}), \
                contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()) as err:
            code = timing.main([command, '--log', str(self.path), *args])
        return code, json.loads(out.getvalue()) if out.getvalue() else err.getvalue()

    def start(self, *args):
        return self.invoke('start', '--batch-id', 'batch-test', '--base-commit', 'a' * 40,
                           '--selected', '80', '--phase', 'source_verification', *args)

    def test_repeated_mutually_exclusive_phases_and_utc_adjustment(self):
        self.assertEqual(self.start('--concurrency', '3')[0], 0)
        for phase, seconds in [('prepare_dispatch', 10), ('wait_reviewers', 20),
                               ('prepare_dispatch', 80), ('wait_reviewers', 90),
                               ('import_adjudication', 110), ('gates', 130), ('closure', 160)]:
            self.assertEqual(self.invoke('mark', '--phase', phase, seconds=seconds)[0], 0)
        code, result = self.invoke('finish', '--child-count', '4', '--retry-count', '0', seconds=180,
                                   utc='2026-09-05T11:00:00+00:00')
        self.assertEqual(code, 0)
        self.assertEqual(result['phase_seconds_recorded'], dict(source_verification=10,
            prepare_dispatch=20, wait_reviewers=80, import_adjudication=20, gates=30, closure=20, unknown=0))
        self.assertEqual(result['total_wall_seconds'], 180)
        self.assertEqual(result['selected_per_hour'], 1600)
        self.assertEqual(result['counts'], dict(child_count=4, retry_count=0, actual_tokens='unknown'))
        self.assertEqual(result['concurrency'], 3)
        before = self.path.read_bytes()
        self.assertEqual(self.invoke('summary')[1], result)
        self.assertEqual(self.path.read_bytes(), before)

    def test_missing_data_and_unfinished_interval_are_not_estimated(self):
        self.assertEqual(self.start()[0], 0)
        _, ongoing = self.invoke('summary', seconds=500)
        self.assertEqual(ongoing['total_wall_seconds'], 'unknown')
        self.assertEqual(ongoing['recorded_wall_seconds'], 0)
        self.assertEqual(ongoing['concurrency'], 'unknown')
        self.assertEqual(ongoing['counts'], dict.fromkeys(timing.COUNTS, 'unknown'))
        self.invoke('mark', '--phase', 'unknown', '--missing-reason', 'unclassified', seconds=10)
        self.invoke('mark', '--phase', 'closure', seconds=30)
        _, result = self.invoke('finish', seconds=40)
        self.assertFalse(result['timing_complete'])
        self.assertEqual(result['phase_seconds_recorded']['unknown'], 20)
        self.assertEqual(result['selected_per_hour'], 'unknown')
        self.assertEqual(result['missing_reasons'], ['unclassified'])

    def test_explicit_incomplete_and_zero_duration(self):
        self.start()
        _, result = self.invoke('finish', '--incomplete-reason', 'late start')
        self.assertEqual(result['total_wall_seconds'], 'unknown')
        self.path = self.path.with_name('zero.json')
        self.start()
        _, result = self.invoke('finish')
        self.assertTrue(result['timing_complete'])
        self.assertEqual(result['total_wall_seconds'], 0)
        self.assertEqual(result['selected_per_hour'], 'unknown')

    def test_duplicate_and_invalid_commands_preserve_bytes(self):
        self.start()
        before = self.path.read_bytes()
        self.assertEqual(self.start()[0], 1)
        for args, kwargs in [(['--phase', 'unknown'], {}),
                             (['--phase', 'gates', '--missing-reason', 'wrong'], {}),
                             (['--phase', 'gates'], {'domain': 'different'}),
                             (['--phase', 'gates'], {'seconds': -1})]:
            self.assertEqual(self.invoke('mark', *args, **kwargs)[0], 1)
            self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.invoke('finish', '--retry-count', '-1')[0], 1)
        self.assertEqual(self.path.read_bytes(), before)
        self.invoke('finish')
        before = self.path.read_bytes()
        for command, args in [('finish', []), ('mark', ['--phase', 'gates'])]:
            self.assertEqual(self.invoke(command, *args)[0], 1)
            self.assertEqual(self.path.read_bytes(), before)

    def test_bad_logs_fail_without_replacement(self):
        self.start()
        valid = json.loads(self.path.read_bytes())
        variants = [b'{broken', b'{}', b'[]', b'null',
                    self.path.read_bytes().replace(b'"version": 1', b'"version": 9, "version": 1')]
        for mutate in (lambda d: d['events'][0].update(monotonic_ns=True),
                       lambda d: d['events'][0].update(utc='no date'),
                       lambda d: d.update(selected=81),
                       lambda d: d['events'].append(dict(d['events'][0])),
                       lambda d: d.update(concurrency=False)):
            data = json.loads(json.dumps(valid))
            mutate(data)
            variants.append(json.dumps(data).encode())
        for raw in variants:
            self.path.write_bytes(raw)
            for command in ('finish', 'summary'):
                self.assertEqual(self.invoke(command)[0], 1, raw)
                self.assertEqual(self.path.read_bytes(), raw)

    def test_write_failure_preserves_previous_log(self):
        self.start()
        before = self.path.read_bytes()
        with patch.object(timing.os, 'replace', side_effect=OSError('disk error')):
            self.assertEqual(self.invoke('mark', '--phase', 'gates', seconds=20)[0], 1)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_paths_fail_closed(self):
        self.start()
        original = self.path
        before = original.read_bytes()
        outside = self.root / 'outside'
        outside.mkdir()
        linked = original.parent / 'linked.json'
        linked.symlink_to(original)
        hardlink = original.parent / 'hard.json'
        hardlink.hardlink_to(original)
        escape = original.parent / 'escape'
        escape.symlink_to(outside, target_is_directory=True)
        for path in (self.root / 'evidence/log.json', self.root / '.ai/task/log.json',
                     self.root / '.artifacts/i18n/../bad.json', linked, hardlink,
                     escape / 'log.json', self.root / '.artifacts/i18n'):
            self.path = path
            self.assertEqual(self.start()[0], 1, path)
        self.assertEqual(original.read_bytes(), before)
        self.assertFalse((outside / 'log.json').exists())

    def test_real_cross_process_clock_and_concurrent_start(self):
        real_root = Path(timing.__file__).resolve().parents[1]
        artifact_root = real_root / '.artifacts/i18n'
        artifact_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=artifact_root) as folder:
            path = str(Path(folder) / 'test.json')
            cli = [sys.executable, '-B', str(real_root / 'tools/review_phase_timing.py')]
            args = ['start', '--log', path, '--batch-id', 'synthetic-clock-test',
                    '--base-commit', 'a' * 40, '--selected', '1', '--phase', 'source_verification']
            processes = [subprocess.Popen(cli + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                         for _ in range(2)]
            for process in processes:
                process.communicate(timeout=10)
            self.assertEqual(sorted(p.returncode for p in processes), [0, 1])
            result = subprocess.run(cli + ['finish', '--log', path], capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertTrue(data['timing_complete'])
            self.assertGreater(data['total_wall_seconds'], 0)
            self.assertEqual(data['counts']['actual_tokens'], 'unknown')

    def test_invalid_start_and_missing_log(self):
        self.assertEqual(self.invoke('finish')[0], 1)
        self.assertEqual(self.start('--selected', '81')[0], 1)
        self.assertFalse(self.path.exists())
        self.assertEqual(self.start('--base-commit', 'short')[0], 1)
        self.assertFalse(self.path.exists())


if __name__ == '__main__':
    unittest.main()
