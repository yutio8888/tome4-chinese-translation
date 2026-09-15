"""Grok native session-directory export tests using trimmed real sessions."""
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


FIXTURES = ROOT / 'tests/fixtures/grok'
SIDS = ('01a0a5aa-d667-7e32-a7f1-3059e248dc43',
        '01a0a533-505a-7f80-9381-29b7df50148a')
EVENT_TYPES = {'mcp_config_resolved', 'mcp_server_starting', 'turn_started',
               'mcp_server_connected', 'mcp_init_completed', 'loop_started',
               'phase_changed', 'first_token', 'tool_started', 'tool_completed',
               'permission_requested', 'permission_resolved', 'turn_ended'}
FINAL_SHA256 = {
    SIDS[0]: '922c643f53d65c98cca10b35e94f1786ffbf3871d7678291f92bc1ddbdf5043e',
    SIDS[1]: '8a9a7881aa6789af9b0b253b57cf7c671d9c943873a930ddcfe4821716093afa',
}


class GrokNativeExportTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='grok-native-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.copy_count = 0

    @staticmethod
    def records(path):
        return [json.loads(line) for line in path.read_bytes().splitlines()]

    def copy_fixture(self, sid):
        source = FIXTURES / sid
        summary = json.loads((source / 'summary.json').read_bytes())
        cwd = summary['info']['cwd']
        self.copy_count += 1
        path = self.root / str(self.copy_count) / 'sessions' / quote(cwd, safe='') / sid
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, path)
        chat = self.records(path / 'chat_history.jsonl')
        query = next(''.join(block['text'] for block in record['content'])
                     for record in chat if record['type'] == 'user'
                     and '<user_query>' in ''.join(block['text'] for block in record['content']))
        prompt = query.split('<user_query>', 1)[1].split('</user_query>', 1)[0]
        if prompt.startswith('\n') and prompt.endswith('\n'):
            prompt = prompt[1:-1]
        return path, summary, cwd, prompt

    def read_final(self, sid):
        path, summary, cwd, prompt = self.copy_fixture(sid)
        result = life.read_native_final(path, provider='grok', session_id=summary['info']['id'],
                                        cwd=cwd, prompt=prompt, natural_success=True)
        return path, result, cwd, prompt

    def test_real_session_fixtures_accept_and_preserve_final_bytes(self):
        for sid in SIDS:
            with self.subTest(sid=sid):
                path, (raw, proof), cwd, prompt = self.read_final(sid)
                chat = self.records(path / 'chat_history.jsonl')
                final_text = [r['content'] for r in chat if r['type'] == 'assistant'][-1]
                self.assertEqual(raw, final_text.encode())
                self.assertEqual(life.digest(raw), FINAL_SHA256[sid])
                self.assertEqual(proof['session_id'], sid)
                self.assertEqual(proof['raw_sha256'], life.digest(raw))
                events = self.records(path / 'events.jsonl')
                self.assertEqual({event['type'] for event in events}, EVENT_TYPES)
                self.assertGreater(proof['complete_line'], 1)
                for name in ('summary.json', 'events.jsonl', 'chat_history.jsonl'):
                    self.assertEqual(proof['source_file_sha256'][name],
                                     life.digest((path / name).read_bytes()))
                self.assertEqual([r['type'] for r in chat].count('user'), 5)
                self.assertTrue(all(isinstance(r['content'], list)
                                    for r in chat if r['type'] == 'user'))
                self.assertTrue(all('content' not in r and isinstance(r['summary'], list)
                                    for r in chat if r['type'] == 'reasoning'))
                prompt_record = chat[proof['prompt_line'] - 1]
                self.assertEqual(prompt_record['type'], 'user')
                prompt_record_text = ''.join(block['text'] for block in prompt_record['content'])
                self.assertIn('<user_query>', prompt_record_text)
                self.assertIn(prompt, prompt_record_text)
                info_record = chat[proof['info_line'] - 1]
                self.assertIn('Workspace Path:', ''.join(block['text']
                                                         for block in info_record['content']))
                calls = {call['id'] for record in chat if record['type'] == 'assistant'
                         for call in record.get('tool_calls', [])}
                results = {record['tool_call_id'] for record in chat
                           if record['type'] == 'tool_result'}
                self.assertTrue(calls)
                self.assertTrue(calls <= results)
                self.assertTrue(all(set(call) == {'id', 'name', 'arguments'}
                                    for record in chat if record['type'] == 'assistant'
                                    for call in record.get('tool_calls', [])))
                chat[7]['content'] = 'earlier progress'
                chat.append({'type': 'tool_result', 'tool_call_id': 'after-final',
                             'content': 'non-assistant tail'})
                (path / 'chat_history.jsonl').write_bytes(
                    b''.join(json.dumps(r, ensure_ascii=False).encode() + b'\n' for r in chat))
                self.assertEqual(self.read_path_final(path, sid, cwd, prompt), raw)

    def test_user_record_count_is_not_a_runtime_invariant(self):
        for count in (4, 6):
            with self.subTest(user_count=count):
                path, summary, cwd, prompt = self.copy_fixture(SIDS[0])
                chat = self.records(path / 'chat_history.jsonl')
                user_indices = [i for i, record in enumerate(chat) if record['type'] == 'user']
                if count == 4:
                    chat.pop(user_indices[1])
                else:
                    first_assistant = next(i for i, record in enumerate(chat)
                                           if record['type'] == 'assistant')
                    chat.insert(first_assistant, {
                        'type': 'user',
                        'content': [{'type': 'text', 'text': '[additional host user record]'}],
                    })
                (path / 'chat_history.jsonl').write_bytes(
                    b''.join(json.dumps(record, ensure_ascii=False).encode() + b'\n'
                             for record in chat))
                raw, proof = life.read_native_final(
                    path, provider='grok', session_id=summary['info']['id'], cwd=cwd,
                    prompt=prompt, natural_success=True)
                self.assertEqual(life.digest(raw), FINAL_SHA256[SIDS[0]])
                self.assertIn('<user_query>', ''.join(
                    block['text'] for block in chat[proof['prompt_line'] - 1]['content']))

    def test_query_and_later_user_records_after_assistant_are_rejected(self):
        cases = ('trailing user', 'query after final assistant')
        for case in cases:
            with self.subTest(case=case):
                path, summary, cwd, prompt = self.copy_fixture(SIDS[0])
                chat = self.records(path / 'chat_history.jsonl')
                if case == 'trailing user':
                    chat.append({'type': 'user', 'content': [
                        {'type': 'text', 'text': '[later host user record]'},
                    ]})
                else:
                    query_index = next(i for i, record in enumerate(chat)
                                       if record['type'] == 'user' and '<user_query>' in
                                       ''.join(block['text'] for block in record['content']))
                    chat.append(chat.pop(query_index))
                (path / 'chat_history.jsonl').write_bytes(
                    b''.join(json.dumps(record, ensure_ascii=False).encode() + b'\n'
                             for record in chat))
                with self.assertRaises(life.LifecycleError):
                    life.read_native_final(path, provider='grok', session_id=summary['info']['id'],
                                           cwd=cwd, prompt=prompt, natural_success=True)

    @staticmethod
    def read_path_final(path, sid, cwd, prompt):
        return life.read_native_final(path, provider='grok', session_id=sid,
                                      cwd=cwd, prompt=prompt, natural_success=True)[0]

    def test_grok_acp_runtime_identity_accepts_only_acp(self):
        base = dict(provider='grok', cwd='/fixture', persistence=dict(
            provider='grok', sessionId='session', nativeHandle='session',
            metadata=dict(provider='acp', cwd='/fixture')))
        self.assertEqual(life.native_identity(base), ('grok', 'session'))
        for value in ('grok', 'codex', 'claude', 'other'):
            bad = deepcopy(base)
            bad['persistence']['metadata']['provider'] = value
            with self.subTest(provider=value), self.assertRaises(life.LifecycleError):
                life.native_identity(bad)

    def test_export_binds_child_input_and_terminal_capture(self):
        # Exercise the real directory parser through the lifecycle export
        # path as well as through read_native_final above.
        from tests.i18n.test_review_lifecycle import LifecycleTests
        lifecycle = LifecycleTests('test_native_exact_text_not_earlier_json_tool_or_thinking')
        lifecycle.setUp()
        self.addCleanup(lifecycle.doCleanups)
        row, terminal, _ = lifecycle.native_child('grok')
        sid = SIDS[0]
        cwd = str(lifecycle.root)
        prompt = row['create_parameters']['prompt']
        source = FIXTURES / sid
        path = lifecycle.root / 'sessions' / quote(cwd, safe='') / sid
        path.parent.mkdir(parents=True)
        shutil.copytree(source, path)
        summary = json.loads((path / 'summary.json').read_bytes())
        summary['info'].update(id=sid, cwd=cwd)
        (path / 'summary.json').write_bytes(json.dumps(summary, ensure_ascii=False).encode())
        events = self.records(path / 'events.jsonl')
        for event in events:
            if event['type'] == 'turn_started':
                event['session_id'] = sid
        (path / 'events.jsonl').write_bytes(b''.join(json.dumps(r, ensure_ascii=False).encode() + b'\n'
                                                   for r in events))
        chat = self.records(path / 'chat_history.jsonl')
        for record in chat:
            if record['type'] != 'user':
                continue
            for block in record['content']:
                if '<user_info>' in block['text']:
                    block['text'] = block['text'].replace(
                        'Workspace Path: /workspace/tome4-chinese-translation',
                        'Workspace Path: ' + cwd)
                if '<user_query>' in block['text']:
                    block['text'] = '<user_query>\n' + prompt + '\n</user_query>'
        chat[-1]['content'] = lifecycle.raw(row).decode('utf-8')
        (path / 'chat_history.jsonl').write_bytes(b''.join(json.dumps(r, ensure_ascii=False).encode() + b'\n'
                                                        for r in chat))
        for capture in (terminal, row['first_live_capture']):
            capture['snapshot']['persistence']['sessionId'] = sid
            capture['snapshot']['persistence']['nativeHandle'] = sid
            capture['snapshot']['persistence']['metadata']['provider'] = 'acp'
            capture['snapshot']['persistence']['metadata']['cwd'] = cwd
            capture['snapshot']['runtimeInfo']['sessionId'] = sid
        out = lifecycle.root / 'export'
        raw = life.export_native_final(lifecycle.j, lifecycle.j.key(row), terminal, path, out, notified=True)
        self.assertEqual(raw, lifecycle.raw(row))
        proof = life.read(out / row['task_id'] / row['dispatch_id'] / 'provenance.json')
        self.assertEqual(proof['session_id'], sid)
        self.assertEqual(proof['source_path'], str(path))

    def test_real_shape_requirements_fail_closed(self):
        # One negative for each reworked real-log requirement.  Provider
        # identity has its dedicated accept/reject test above.
        mutations = {
            'event vocabulary': lambda summary, events, chat: events[8].update(type='tool_unknown'),
            'turn prefix and uniqueness': lambda summary, events, chat: events.insert(0, events.pop(2)),
            'reasoning has no content': lambda summary, events, chat: next(
                record.update(content='must be absent') for record in chat if record['type'] == 'reasoning'),
            'user text-block list and split prompt': lambda summary, events, chat: next(
                record.update(content=record['content'][0]['text']) for record in chat
                if record['type'] == 'user' and '<user_query>' in record['content'][0]['text']),
            'last assistant is final': lambda summary, events, chat: chat[-1].update(content=''),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                path, summary, cwd, prompt = self.copy_fixture(SIDS[0])
                events_path = path / 'events.jsonl'
                chat_path = path / 'chat_history.jsonl'
                events = self.records(events_path)
                chat = self.records(chat_path)
                mutate(summary, events, chat)
                events_path.write_bytes(b''.join(json.dumps(r, ensure_ascii=False).encode() + b'\n'
                                                 for r in events))
                chat_path.write_bytes(b''.join(json.dumps(r, ensure_ascii=False).encode() + b'\n'
                                               for r in chat))
                with self.assertRaises(life.LifecycleError):
                    life.read_native_final(path, provider='grok', session_id=summary['info']['id'],
                                           cwd=cwd, prompt=prompt, natural_success=True)

    def test_directory_and_source_files_fail_closed(self):
        path, summary, cwd, prompt = self.copy_fixture(SIDS[0])
        for name in ('summary.json', 'events.jsonl', 'chat_history.jsonl'):
            with self.subTest(missing=name):
                target = path / name
                original = target.read_bytes()
                target.unlink()
                with self.assertRaises((life.LifecycleError, OSError)):
                    life.read_native_final(path, provider='grok', session_id=SIDS[0],
                                           cwd=cwd, prompt=prompt, natural_success=True)
                target.write_bytes(original)
        for bad in (self.root / 'absent', self.root / 'sessions', path / 'summary.json'):
            with self.subTest(path=bad), self.assertRaises((life.LifecycleError, OSError)):
                life.read_native_final(bad, provider='grok', session_id=SIDS[0],
                                       cwd=cwd, prompt=prompt, natural_success=True)
        duplicate = path.parent.parent / 'other-cwd' / SIDS[0]
        duplicate.mkdir(parents=True)
        with self.assertRaisesRegex(life.LifecycleError, 'duplicate'):
            life.read_native_final(path, provider='grok', session_id=SIDS[0],
                                   cwd=cwd, prompt=prompt, natural_success=True)

    def test_json_encoding_and_limits_fail_closed(self):
        path, summary, cwd, prompt = self.copy_fixture(SIDS[0])
        for name, bad in [('summary.json', b'\xef\xbb\xbf{}'),
                          ('events.jsonl', b'\xff\n'),
                          ('chat_history.jsonl', b'{"type":"user","content":"bad"}\n')]:
            with self.subTest(name=name):
                target = path / name
                original = target.read_bytes()
                target.write_bytes(bad)
                with self.assertRaises(life.LifecycleError):
                    life.read_native_final(path, provider='grok', session_id=SIDS[0],
                                           cwd=cwd, prompt=prompt, natural_success=True)
                target.write_bytes(original)
        with patch.object(life, 'NATIVE_MAX_BYTES', 10):
            with self.assertRaises(life.LifecycleError):
                life.read_native_final(path, provider='grok', session_id=SIDS[0],
                                       cwd=cwd, prompt=prompt, natural_success=True)


if __name__ == '__main__':
    unittest.main()
