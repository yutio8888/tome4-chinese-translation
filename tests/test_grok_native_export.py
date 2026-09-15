"""Synthetic Grok native session directory fixtures; no host session access."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/orchestration'))
sys.path.insert(0, str(ROOT / 'tools'))
import review_lifecycle as life


def jsonl(records):
    return b''.join(json.dumps(r, ensure_ascii=False).encode('utf-8') + b'\n' for r in records)


class GrokNativeExportTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='grok-native-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.cwd = '/workspace/grok fixture'
        self.prompt = 'frozen prompt\nwith whitespace '
        self.path = self.root / 'sessions' / quote(self.cwd, safe='') / 'session'
        self.summary = dict(info=dict(id='session', cwd=self.cwd), current_model_id='grok-4.6')
        self.events = [dict(type='turn_started', session_id='session', turn_number=0, model_id='grok-4.6'),
                       dict(type='phase_changed', phase='answer'),
                       dict(type='turn_ended', outcome='completed')]
        self.chat = [dict(type='system', content='host instructions'),
                     dict(type='user', content=f'<user_info>\nWorkspace Path: {self.cwd}\n</user_info>\n'
                                               f'<user_query>\n{self.prompt}\n</user_query>'),
                     dict(type='assistant', content=''),
                     dict(type='tool_result', content='tool output'),
                     dict(type='assistant', content=' \n中文\t\r\n')]
        self.write_session()

    def write_session(self):
        self.path.mkdir(parents=True, exist_ok=True)
        (self.path / 'summary.json').write_bytes(json.dumps(self.summary, ensure_ascii=False).encode('utf-8'))
        (self.path / 'events.jsonl').write_bytes(jsonl(self.events))
        (self.path / 'chat_history.jsonl').write_bytes(jsonl(self.chat))

    def read_final(self):
        return life.read_native_final(self.path, provider='grok', session_id='session',
                                      cwd=self.cwd, prompt=self.prompt, natural_success=True)

    def test_accept_preserves_exact_final_bytes_and_binds_all_sources(self):
        raw, proof = self.read_final()
        self.assertEqual(raw, self.chat[-1]['content'].encode('utf-8'))
        self.assertEqual(proof['session_id'], 'session')
        self.assertEqual(proof['prompt_sha256'], life.digest(self.prompt.encode()))
        self.assertEqual(proof['raw_sha256'], life.digest(raw))
        for name in ('summary.json', 'events.jsonl', 'chat_history.jsonl'):
            self.assertEqual(proof['source_file_sha256'][name], life.digest((self.path / name).read_bytes()))
        self.assertNotIn(self.prompt, json.dumps(proof))
        self.chat.append(dict(type='tool_result', content='later non-assistant record'))
        self.write_session()
        self.assertEqual(self.read_final()[0], raw)

    def test_export_binds_child_input_and_terminal_capture(self):
        from tests.i18n.test_review_lifecycle import LifecycleTests
        fixture = LifecycleTests('test_native_exact_text_not_earlier_json_tool_or_thinking')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        row, cap, _ = fixture.native_child('grok')
        shutil.rmtree(self.path.parent)
        self.cwd = str(fixture.root)
        self.prompt = row['create_parameters']['prompt']
        self.path = self.root / 'sessions' / quote(self.cwd, safe='') / 'session'
        self.summary['info']['cwd'] = self.cwd
        self.chat[1]['content'] = (f'<user_info>\nWorkspace Path: {self.cwd}\n</user_info>\n'
                                   f'<user_query>\n{self.prompt}\n</user_query>')
        self.chat[-1]['content'] = fixture.raw(row).decode('utf-8')
        self.write_session()
        out = self.root / 'export'
        raw = life.export_native_final(fixture.j, fixture.j.key(row), cap, self.path, out, notified=True)
        self.assertEqual(raw, fixture.raw(row))
        proof = life.read(out / row['task_id'] / row['dispatch_id'] / 'provenance.json')
        self.assertEqual(proof['agent_id'], row['agent_id'])
        self.assertEqual(proof['input_sha256'], row['input_sha256'])
        self.assertEqual(proof['terminal_capture_sha256'], life.digest(life.surface.canonical_bytes(cap)))
        self.assertEqual(proof['source_path'], str(self.path))

    def test_directory_and_source_files_fail_closed(self):
        missing = self.path / 'summary.json'
        missing.unlink()
        with self.assertRaises((life.LifecycleError, OSError)):
            self.read_final()
        self.write_session()
        for name in ('summary.json', 'events.jsonl', 'chat_history.jsonl'):
            with self.subTest(missing=name):
                file = self.path / name
                file.unlink()
                with self.assertRaises((life.LifecycleError, OSError)):
                    self.read_final()
                self.write_session()
        for bad in (self.root / 'absent', self.root / 'sessions', self.path / 'summary.json'):
            with self.subTest(path=bad), self.assertRaises((life.LifecycleError, OSError)):
                life.read_native_final(bad, provider='grok', session_id='session', cwd=self.cwd,
                                       prompt=self.prompt, natural_success=True)
        duplicate = self.root / 'sessions' / 'other-cwd' / 'session'
        duplicate.mkdir(parents=True)
        with self.assertRaisesRegex(life.LifecycleError, 'duplicate'):
            self.read_final()
        shutil.rmtree(duplicate.parent)
        source = self.path / 'summary.json'
        original = source.read_bytes()
        source.unlink()
        source.symlink_to(self.path / 'events.jsonl')
        with self.assertRaises(life.LifecycleError):
            self.read_final()
        source.unlink()
        source.write_bytes(original)
        with self.assertRaises(life.LifecycleError):
            life.read_native_final(self.path, provider='grok', session_id='session',
                                   cwd=self.cwd, prompt=self.prompt, natural_success=False)

    def test_identity_and_completion_fail_closed(self):
        cases = [
            ('summary session', lambda: self.summary['info'].update(id='other')),
            ('summary cwd', lambda: self.summary['info'].update(cwd='/other')),
            ('summary model', lambda: self.summary.update(current_model_id='other')),
            ('event session', lambda: self.events[0].update(session_id='other')),
            ('event cwd', lambda: self.events[1].update(cwd='/other')),
            ('event model', lambda: self.events[0].update(model_id='other')),
            ('duplicate start', lambda: self.events.insert(1, deepcopy(self.events[0]))),
            ('missing start', lambda: self.events.pop(0)),
            ('no completed tail', lambda: self.events[-1].update(outcome='failed')),
            ('trailing event', lambda: self.events.append(dict(type='phase_changed', phase='late'))),
            ('event shape', lambda: self.events[0].pop('turn_number')),
            ('chat cwd', lambda: self.chat[1].update(content=self.chat[1]['content'].replace(self.cwd, '/other'))),
            ('chat prompt', lambda: self.chat[1].update(content=self.chat[1]['content'].replace(self.prompt, 'other'))),
            ('prompt wrapper', lambda: self.chat[1].update(content=self.chat[1]['content'].replace('</user_query>', ''))),
            ('chat identity', lambda: self.chat[2].update(session_id='other')),
            ('duplicate user', lambda: self.chat.insert(2, deepcopy(self.chat[1]))),
            ('trailing user', lambda: self.chat.append(dict(type='user', content='later'))),
            ('zero final', lambda: self.chat[-1].update(content='')),
            ('zero assistant', lambda: self.chat.pop(-1)),
            ('multiple final', lambda: self.chat[2].update(content='other text')),
            ('unknown chat type', lambda: self.chat[2].update(type='mystery')),
            ('unknown chat shape', lambda: self.chat[2].update(content=['text'])),
            ('unknown event type', lambda: self.events[1].update(type='mystery')),
        ]
        for label, change in cases:
            with self.subTest(label=label):
                old = deepcopy((self.summary, self.events, self.chat))
                change()
                self.write_session()
                with self.assertRaises(life.LifecycleError):
                    self.read_final()
                self.summary, self.events, self.chat = old
                self.write_session()

    def test_json_encoding_and_limits_fail_closed(self):
        for name, bad in [
            ('summary.json', b'{"info":{},"info":{}}'),
            ('summary.json', b'\xef\xbb\xbf{}'),
            ('summary.json', b'\xff'),
            ('events.jsonl', b'{"type":"turn_started","type":"turn_ended"}\n'),
            ('events.jsonl', b'\xef\xbb\xbf{}\n'),
            ('events.jsonl', b'\xff\n'),
            ('chat_history.jsonl', b'{"type":"user","type":"assistant"}\n'),
            ('chat_history.jsonl', b'\xef\xbb\xbf{}\n'),
            ('chat_history.jsonl', b'\xff\n'),
            ('chat_history.jsonl', b'{"type":"system","content":"\\ud800"}\n'),
            ('chat_history.jsonl', b'{}'),
        ]:
            with self.subTest(name=name, bad=bad[:8]):
                file = self.path / name
                original = file.read_bytes()
                file.write_bytes(bad)
                with self.assertRaises(life.LifecycleError):
                    self.read_final()
                file.write_bytes(original)
        with patch.object(life, 'NATIVE_MAX_BYTES', 10), self.assertRaises(life.LifecycleError):
            self.read_final()
        size = max((self.path / name).stat().st_size for name in
                   ('summary.json', 'events.jsonl', 'chat_history.jsonl'))
        with patch.object(life, 'NATIVE_MAX_BYTES', size), self.assertRaises(life.LifecycleError):
            self.read_final()
        with patch.object(life, 'NATIVE_MAX_LINES', 2), self.assertRaises(life.LifecycleError):
            self.read_final()
        summary_file = self.path / 'summary.json'
        original = summary_file.read_bytes()
        summary_file.write_bytes(original[:-1] + b'\n' * 20 + original[-1:])
        with patch.object(life, 'NATIVE_MAX_LINES', 15), self.assertRaises(life.LifecycleError):
            self.read_final()
        summary_file.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
