"""Real small Git source inputs; no production queue or agent operations."""
from __future__ import annotations

import ast
import copy
from dataclasses import replace
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from orchestration import build_evidence_pack as facts
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
import contextual_result_check as contextual
import contextual_anchor_preflight as anchor_preflight


def commit(root, message):
    facts.git(root, 'add', '.')
    facts.git(root, 'commit', '-qm', message)
    return facts.git(root, 'rev-parse', 'HEAD').decode().strip()


def init_git(root):
    root.mkdir(parents=True, exist_ok=True)
    facts.git(root, 'init', '-q')
    facts.git(root, 'config', 'user.name', 'Fixture')
    facts.git(root, 'config', 'user.email', 'fixture@example.invalid')


def put(root, path, raw):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw.encode() if isinstance(raw, str) else raw)
    return target


def install_sources(root, rows):
    """Add valid version inputs to an existing disposable catalog fixture."""
    source = root / '.artifacts/source'
    init_git(source)
    put(source, 'i18n_tools/i18n_extractor.lua', '-- extractor A\nkey:gsub("_", " ")\n')
    extractor_commit = commit(source, 'extractor fixed independently')
    for index, row in enumerate(rows):
        name = 'a' + (str(index) if index else '') + '.lua'
        for prefix in ('game/modules/tome/', 'game/engines/default/engine/'):
            put(source, prefix + name, 't(' + json.dumps(row['source']) + ') -- args_order=untrusted\n')
    put(source, 'i18n_tools/i18n_extractor.lua', '-- later extractor B\n')
    source_commit = commit(source, 'source A')
    manifest = json.loads((ROOT / 'i18n/versions/tome-1.7.6.json').read_bytes())
    manifest['repositories']['engine'].update(commit=source_commit, default='.artifacts/source', env='P1C_FIXTURE_ENGINE_ROOT')
    manifest['extractor']['commit'] = extractor_commit
    for component in manifest['components']:
        if component.get('source_baseline'):
            component['source_baseline']['extractor_commit'] = extractor_commit
    put(root, 'i18n/versions/tome-1.7.6.json', json.dumps(manifest))
    put(root, 'TERMINOLOGY.md', 'fixture terminology\n')
    put(root, 'terminology/terms.tsv', 'source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\nsource\t术语\tT.UI.LABEL\tui\t\treview\tcore\tonly if section applies\n')
    term_sha = wp1.terminology_snapshot(root)
    identities = wp1.source_identities_from_manifest(facts.load_config(root))
    rebuilt = []
    for index, old in enumerate(rows):
        row = copy.deepcopy(old)
        component = row['component']
        name = 'a' + (str(index) if index else '') + '.lua'
        row.update(normalized_path='engine.lua' if component == 'engine' else 'mod-tome.lua',
                   section=('engine/engine/' if component == 'engine' else 'mod-tome/') + name,
                   fixed_source_identity=identities[component], terminology_snapshot_sha256=term_sha)
        if component == 'cults':
            row['section'] = 'tome-cults/' + name
            row['normalized_path'] = 'tome-cults.lua'
            dlc = source / 'dlc/cults'
            put(dlc, row['section'], 't(' + json.dumps(row['source']) + ') -- args_order=untrusted\n')
            # Avoid dependence on the host's DLC environment in CLI fixtures.
            manifest['protected_source_roots']['dlc'].update(env='P1C_FIXTURE_DLC_ROOT', relative_path='dlc')
        core = dict(component=component, duplicate_index=0, function_name='t', normalized_source_tag=row['source_tag'] or '',
                    section=row['section'], source=row['source'], translation_path=row['normalized_path'])
        row['call_locator'] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, 'locator', core)
        row['logical_entry_identity'] = wp1.surface.logical_entry_identity(component=component, normalized_path=row['normalized_path'], call_locator=row['call_locator'], source_tag=row['source_tag'])
        row['entry_revision_identity'] = wp1.surface.entry_revision_identity(logical_entry_identity=row['logical_entry_identity'], source=row['source'], target=row['target'], fixed_source_identity=row['fixed_source_identity'], terminology_snapshot=term_sha, rules_version=row['rules_version'], args_order=row['risk']['args_order'])
        rebuilt.append(row)
    put(root, 'i18n/versions/tome-1.7.6.json', json.dumps(manifest))
    return rebuilt, source


def workset(root, checkpoint):
    config = facts.load_config(root)
    reader = facts.FixedReader()
    builder = facts.FactBuilder(root, config, reader, [])
    verifications = []
    for row in checkpoint['entry_snapshots']:
        component, path = facts.source_location(config, row)
        provenance, lines = builder.read(component, path)
        hits = [i for i, line in enumerate(lines, 1) if row['source'] in line]
        verifications.append(dict(entry_revision_identity=row['entry_revision_identity'], component=component.id,
                                  section=row['section'], source=row['source'], source_tag=row['source_tag'],
                                  args_order=row['risk']['args_order'], public_source_path=path,
                                  source_file_sha256=provenance['source_file_sha256'],
                                  source_pinning=provenance['source_pinning'], fixed_source_commit=provenance['commit'],
                                  matching_literal_lines=hits))
    return dict(batch_id=checkpoint['batch_id'], catalog_id=checkpoint['catalog_id'], base_commit=checkpoint['base_commit'],
                entries=copy.deepcopy(checkpoint['entry_snapshots']), source_verification=verifications)


class SourceFactsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='p1c-source.')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        init_git(self.root)
        put(self.root, '.gitignore', '.artifacts/\n')
        row = dict(component='tome', source='source %d%% %0.2f', target='目标 %d%% %0.2f', source_tag='',
                   rules_version=catalog.RULES_VERSION, risk=dict(args_order=None))
        self.rows, self.source = install_sources(self.root, [row])
        self.base = commit(self.root, 'terms and version inputs')
        self.cp = dict(batch_id='batch-fixture', catalog_id='catalog-fixture', base_commit=self.base,
                       selected=[r['entry_revision_identity'] for r in self.rows], entry_snapshots=self.rows)
        self.ws = workset(self.root, self.cp)
        self.ver = self.ws['source_verification'][0]
        self.config = facts.load_config(self.root)
        self.path = self.ver['public_source_path']

    def build(self, ws=None, cp=None):
        cp = cp or self.cp
        return facts.build_source_facts(self.root, facts.canonical(ws or self.ws), cp,
                                       [dict(run_index=0, entries=cp['entry_snapshots'])])[0]

    def direct(self, ver=None, row=None):
        return facts.FactBuilder(self.root, self.config, facts.FixedReader(), []).fact(row or self.rows[0], ver or self.ver)

    def repin(self, body=None):
        if body is not None:
            put(self.source, self.path, body)
        oid = commit(self.source, 'new source version')
        repo = replace(self.config.repositories['engine'], commit=oid)
        self.config = replace(self.config, repositories={**self.config.repositories, 'engine': repo})
        self.ver['fixed_source_commit'] = oid
        self.ver['source_file_sha256'] = facts.sha((self.source / self.path).read_bytes())

    def test_standalone_legacy_command_uses_same_facts_and_failure_keeps_pack(self):
        prefix = self.root / 'evidence/quality/production-batches'
        wsp = put(self.root, 'evidence/quality/production-batches/batch-fixture-source-workset.json', facts.canonical(self.ws))
        command = [sys.executable, '-B', str(ROOT/'tools/orchestration/build_evidence_pack.py'),
                   'batch-fixture', '--context', '3', '--siblings', '4']
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root))
        result = subprocess.run(command, cwd=self.root, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        dest = prefix / 'batch-fixture-evidence-pack.json'
        expected = dest.read_bytes()
        self.assertEqual(json.loads(expected), self.build())
        self.assertNotIn('existing_library_usage', expected.decode())
        result = subprocess.run(command, cwd=self.root, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        ws = copy.deepcopy(self.ws)
        ws['source_verification'][0]['source_file_sha256'] = '0'*64
        wsp.write_bytes(facts.canonical(ws))
        result = subprocess.run(command, cwd=self.root, env=env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(dest.read_bytes(), expected)

    def test_reader_cache_is_per_build_and_not_per_line(self):
        reader = facts.FixedReader()
        original = facts.git
        calls = []
        def counted(root, *args):
            calls.append(args)
            return original(root, *args)
        with mock.patch.object(facts, 'git', side_effect=counted):
            for _ in range(20):
                reader.pinned(self.source, self.ver['fixed_source_commit'], self.path)
        self.assertEqual(sum(args[0] == 'ls-tree' for args in calls), 1)
        self.assertEqual(sum(args[:2] == ('cat-file', 'blob') for args in calls), 1)
        self.assertEqual(len(calls), 3)

    def test_engine_producer_sections_fixed_blobs_and_binding_rejections(self):
        # Execute only the unchanged producer's resolver and literal maps, never
        # its top-level main (which would operate on a production checkpoint).
        tree = ast.parse((ROOT / 'tools/orchestration/freeze_workset.py').read_text())
        nodes = [n for n in tree.body if
                 (isinstance(n, ast.FunctionDef) and n.name == 'resolve') or
                 (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and
                  t.id in {'PINNED_MAP', 'DLC_MAP', 'ALWAYS_MERGE_LOCALE'} for t in n.targets))]
        namespace = dict(ENGINE_ROOT=self.source, DLC_ROOT=self.root / 'dlc')
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<producer-resolver>', 'exec'), namespace)
        relatives = ('engine/ActorsSeenDisplay.lua', 'modules/boot/load.lua', 'data/keybinds.lua')
        for relative in relatives:
            put(self.source, 'game/engines/default/' + relative, 't("' + self.rows[0]['source'] + '")\n')
        self.repin()
        for relative in relatives:
            row = dict(self.rows[0], component='engine', normalized_path='engine.lua', section='engine/' + relative)
            comp, path, local, pinned = namespace['resolve'](row)
            with self.subTest(section=row['section']):
                self.assertEqual(path, 'game/engines/default/' + relative)
                self.assertEqual(comp, 'engine')
                self.assertTrue(pinned)
                ver = dict(self.ver, component=comp, public_source_path=path,
                           source_file_sha256=facts.sha(local.read_bytes()), matching_literal_lines=[1])
                expected = self.direct(ver, row)
                self.assertEqual(expected['main_source']['public_source_path'], path)
                self.assertEqual(expected['source_component'], 'engine')
                self.assertEqual(expected['main_source']['source_file_sha256'], ver['source_file_sha256'])
                self.assertEqual(facts.sha(facts.git(self.source, 'cat-file', 'blob',
                                 expected['main_source']['blob_oid'])), ver['source_file_sha256'])
                local.write_bytes(b'checkout drift\n')
                self.assertEqual(self.direct(ver, row), expected)
                local.unlink()
                self.assertEqual(self.direct(ver, row), expected)
                for field, value in (('public_source_path', 'game/engines/default/engine/' + relative),
                                     ('component', 'boot'), ('fixed_source_commit', 'f'*40),
                                     ('source_file_sha256', '0'*64)):
                    with self.subTest(field=field), self.assertRaises(ValueError):
                        self.direct(dict(ver, **{field: value}), row)

    def test_standalone_exclusive_temp_rejects_symlinks_and_special_files(self):
        wsp = put(self.root, 'evidence/quality/production-batches/batch-fixture-source-workset.json', facts.canonical(self.ws))
        frozen = wsp.read_bytes()
        dest = wsp.with_name('batch-fixture-evidence-pack.json')
        temp = dest.with_suffix('.json.tmp')
        command = [sys.executable, '-B', str(ROOT/'tools/orchestration/build_evidence_pack.py'), 'batch-fixture']
        env = dict(os.environ, TOME_TRANSLATION_ROOT=str(self.root))
        def run():
            return subprocess.run(command, cwd=self.root, env=env, capture_output=True, timeout=15)
        expected = facts.canonical(self.build()) + b'\n'
        for existing in (False, True):
            for kind in ('input-symlink', 'dangling-symlink', 'fifo', 'directory', 'regular'):
                with self.subTest(existing=existing, kind=kind):
                    if existing:
                        dest.write_bytes(expected)
                    if kind == 'input-symlink': temp.symlink_to(wsp)
                    elif kind == 'dangling-symlink': temp.symlink_to(wsp.parent/'missing-victim')
                    elif kind == 'fifo': os.mkfifo(temp)
                    elif kind == 'directory': temp.mkdir()
                    else: temp.write_bytes(b'previous temporary bytes')
                    result = run()
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn(b'FileExistsError', result.stderr)
                    self.assertEqual(wsp.read_bytes(), frozen)
                    self.assertFalse(dest.is_symlink())
                    self.assertEqual(dest.read_bytes() if dest.exists() else None, expected if existing else None)
                    self.assertFalse((wsp.parent/'missing-victim').exists())
                    if kind == 'regular': self.assertEqual(temp.read_bytes(), b'previous temporary bytes')
                    if kind == 'directory': temp.rmdir()
                    else: temp.unlink()
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(dest.read_bytes(), expected)
            self.assertFalse(dest.is_symlink())
            self.assertFalse(temp.exists())
            self.assertEqual(wsp.read_bytes(), frozen)
            dest.unlink()

    def test_standalone_replace_failure_preserves_existing_pack_and_input(self):
        wsp = put(self.root, 'evidence/quality/production-batches/batch-fixture-source-workset.json', facts.canonical(self.ws))
        frozen = wsp.read_bytes()
        dest = wsp.with_name('batch-fixture-evidence-pack.json')
        expected = facts.canonical(self.build()) + b'\n'
        dest.write_bytes(expected)
        with mock.patch.dict(os.environ, {'TOME_TRANSLATION_ROOT': str(self.root)}), \
                mock.patch.object(Path, 'replace', side_effect=OSError('replace fixture failure')), \
                self.assertRaisesRegex(OSError, 'replace fixture failure'):
            facts.main(['batch-fixture'])
        self.assertEqual(wsp.read_bytes(), frozen)
        self.assertEqual(dest.read_bytes(), expected)
        self.assertFalse(dest.is_symlink())
        self.assertFalse(dest.with_suffix('.json.tmp').exists())

    def test_actual_32k_fact_limit_and_wrong_auxiliary_declarations(self):
        self.repin('t("' + self.rows[0]['source'] + '") -- ' + 'x'*32768 + '\n')
        with self.assertRaisesRegex(ValueError, '32768 bytes'):
            self.direct()
        kinds = self.attribution_fixture()
        for field, value in (('literal_lines', [999]), ('literal_public_source_path', 'absent.lua'),
                             ('literal_file_sha256', None), ('literal_file_sha256', 'bad')):
            data = dict(kinds['interface_mixin_verification'], **{field: value})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.direct(dict(self.ver, interface_mixin_verification=data))

    def test_import_has_no_io_or_queue_side_effect(self):
        code = "import sys; sys.path.insert(0, 'tools'); import orchestration.build_evidence_pack; assert 'i18nlib.production_review_v2_lite_queue' not in sys.modules"
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_fixed_A_survives_B_and_deletion_and_records_actual_blob_sha(self):
        expected = self.build()
        put(self.source, self.path, 'checkout B\n')
        self.assertEqual(self.build(), expected)
        bad = copy.deepcopy(self.ws)
        bad['source_verification'][0]['source_file_sha256'] = facts.sha(b'checkout B\n')
        with self.assertRaisesRegex(ValueError, 'SHA mismatch'):
            self.build(bad)
        (self.source / self.path).unlink()
        self.assertEqual(self.build(), expected)
        source = expected['entries'][0]['main_source']
        blob = facts.git(self.source, 'cat-file', 'blob', source['blob_oid'])
        self.assertEqual(facts.sha(blob), source['source_file_sha256'])

    def test_wrong_commit_missing_object_and_blob_fail(self):
        for change in ('commit', 'missing', 'path'):
            with self.subTest(change=change):
                ver = copy.deepcopy(self.ver)
                if change == 'commit':
                    ver['fixed_source_commit'] = 'f' * 40
                    with self.assertRaisesRegex(ValueError, 'commit'):
                        self.direct(ver)
                elif change == 'missing':
                    with self.assertRaisesRegex(ValueError, 'unavailable'):
                        facts.FixedReader().pinned(self.source, 'f' * 40, self.path)
                else:
                    with self.assertRaisesRegex(ValueError, 'ordinary blob'):
                        facts.FixedReader().pinned(self.source, ver['fixed_source_commit'], 'missing.lua')

    def test_crlf_is_hashed_raw_and_invalid_utf8_rejected(self):
        self.repin(('t("' + self.rows[0]['source'] + '")\r\n').encode())
        fact = self.direct()
        self.assertEqual(fact['main_source']['source_file_sha256'], facts.sha((self.source/self.path).read_bytes()))
        self.assertNotIn('\r', fact['anchors'][0]['snippet'][0]['text'])
        self.repin(b'\xff\n')
        with self.assertRaises(UnicodeError):
            self.direct()

    def test_paths_symlink_tree_mode_and_bad_line_or_hash_fail(self):
        for path in ('/a', '../a', 'a/../b', 'a//b', './a', 'a\\b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                facts.FixedReader().pinned(self.source, self.ver['fixed_source_commit'], path)
        (self.source / 'link.lua').symlink_to('game/modules/tome/a.lua')
        oid = commit(self.source, 'symlink fixture')
        with self.assertRaisesRegex(ValueError, 'ordinary blob'):
            facts.FixedReader().pinned(self.source, oid, 'link.lua')
        for numbers in ([0], [9999], [True], ['1'], [1, 1]):
            ver = dict(self.ver, matching_literal_lines=numbers)
            with self.subTest(lines=numbers), self.assertRaises(ValueError):
                self.direct(ver)
        with self.assertRaisesRegex(ValueError, 'SHA'):
            self.direct(dict(self.ver, source_file_sha256='0'*64))

    def test_strict_json_full_selected_binding_and_types(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}'):
            with self.assertRaises(ValueError): facts.strict_json(raw)
        for field in ('batch_id', 'base_commit', 'catalog_id'):
            ws = dict(self.ws, **{field: 'bad'})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field): self.build(ws)
        for key in ('entries', 'source_verification'):
            for value in ([], self.ws[key]*2, None):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError): self.build(dict(self.ws, **{key: value}))
        for key in ('source', 'target', 'section', 'source_tag', 'component', 'fixed_source_identity', 'row_sha256'):
            ws = copy.deepcopy(self.ws)
            ws['entries'][0][key] = 'tampered'
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'frozen entry'): self.build(ws)
        for key in ('source', 'section', 'source_tag', 'args_order'):
            ws = copy.deepcopy(self.ws)
            ws['source_verification'][0][key] = True
            with self.subTest(key=key), self.assertRaises(ValueError): self.build(ws)

    def test_format_quantities_always_unknown(self):
        for source in ('damage %d%%', 'resistance %d%%', 'chance %d%%', 'duration %0.2f', 'literal 50%%'):
            row = dict(self.rows[0], source=source, target=source)
            fact = self.direct(dict(self.ver, matching_literal_lines=None), row)
            self.assertEqual({p['quantity_kind'] for p in fact['placeholders']}, {'unknown'})
            self.assertNotIn('convention', facts.canonical(fact).decode())
        self.assertTrue(facts.order_ok(['%s', '%d'], ['%d', '%s'], [2, 1]))
        self.assertFalse(facts.order_ok(['%s', '%d'], ['%d', '%s'], [1, 2]))

    def test_pending_empty_and_none_do_not_inherit_claims(self):
        for hits in ([], None):
            fact = self.direct(dict(self.ver, matching_literal_lines=hits, verification_status='confirmed', rule='EXPECTED ANSWER'))
            self.assertEqual(fact['evidence_status'], 'pending')
            self.assertTrue(fact['missing_evidence'])
            self.assertEqual(fact['anchors'], [])
            self.assertNotIn('EXPECTED ANSWER', facts.canonical(fact).decode())

    def attribution_fixture(self):
        body = ('require "engine.Interface"\ncosmetic_key = {\n_t(value, "tag")\n'
                'name = "prefix "..name:lower()\nmake("Argument", 1)\n'
                'name = name:lower()\nnewGem("Argument", 1)\n')
        put(self.source, 'interface.lua', 't("' + self.rows[0]['source'] + '")\n')
        put(self.source, 'sibling.lua', '{ my_key = 1 }\n')
        locale = 'section "mod-tome/a.lua"\n-- old translated text\nt("' + self.rows[0]['source'] + '", "locale only")\n'
        put(self.source, self.config.component('engine').official_locale, locale)
        self.repin(body)
        self.ver['matching_literal_lines'] = None
        extractor_path = 'i18n_tools/i18n_extractor.lua'
        extractor_raw, _ = facts.FixedReader().pinned(self.source, self.config.extractor.commit, extractor_path)
        return {
            'interface_mixin_verification': dict(including_file_require_lines=[1], require_package='engine.Interface', literal_lines=[1], literal_public_source_path='interface.lua'),
            'host_generated_key_verification': dict(source_lines=[2], source_key='cosmetic_key', extractor_lines=[1,2], extractor_path=extractor_path, extractor_commit=self.config.extractor.commit, extractor_sha256=facts.sha(extractor_raw)),
            'dynamic_tag_sibling_key_verification': dict(dynamic_call_lines=[3], key_lines=[1], key_public_source_path='sibling.lua', source_key='my_key'),
            'concatenated_entity_name_verification': dict(concat_lines=[4], argument_lines=[5], literal_prefix='prefix ', resolved_argument='argument'),
            'lowercased_entity_name_verification': dict(lower_lines=[6], argument_lines=[7], resolved_argument='argument'),
            'legacy_locale_entry_verification': dict(locale_public_source_path=self.config.component('engine').official_locale, locale_section='mod-tome/a.lua', source_lines=[3], locale_marker_line=2),
        }

    def test_each_attribution_and_multiple_are_preserved_without_conclusions(self):
        kinds = self.attribution_fixture()
        for key, data in kinds.items():
            with self.subTest(key=key):
                row = dict(self.rows[0], source_tag='tag')
                fact = self.direct(dict(self.ver, **{key: dict(data, status='confirmed', rule='SECRET CONCLUSION')}), row)
                self.assertGreaterEqual(len(fact['anchors']), 2)
                self.assertNotIn('SECRET CONCLUSION', facts.canonical(fact).decode())
                for a in fact['anchors']:
                    self.assertTrue(a['snippet'])
                    self.assertEqual(len(a['source_file_sha256']), 64)
                if key.startswith('host'):
                    a = fact['anchors'][1]
                    self.assertEqual(a['commit'], self.config.extractor.commit)
                    self.assertIn('extractor A', a['snippet'][0]['text'])
        both = {k: kinds[k] for k in ('interface_mixin_verification', 'concatenated_entity_name_verification')}
        self.assertEqual(len(self.direct(dict(self.ver, **both))['anchors']), 4)
        bad = copy.deepcopy(kinds['interface_mixin_verification'])
        bad['literal_file_sha256'] = 'f' * 64
        with self.assertRaisesRegex(ValueError, 'SHA mismatch'):
            self.direct(dict(self.ver, interface_mixin_verification=bad))
        bad.pop('literal_file_sha256')
        bad['literal_public_source_path'] = '../escape'
        with self.assertRaisesRegex(ValueError, 'path'):
            self.direct(dict(self.ver, interface_mixin_verification=bad))

    def test_always_merge_locale_only_anchors(self):
        locale = self.config.component('engine').official_locale
        put(self.source, locale, 'section ".always_merge"\nt("' + self.rows[0]['source'] + '", "locale only")\n')
        self.repin()
        raw = (self.source / locale).read_bytes()
        row = dict(self.rows[0], component='engine', normalized_path='engine.lua', section='.always_merge')
        ver = dict(self.ver, component='engine', public_source_path=locale, source_file_sha256=facts.sha(raw),
                   matching_literal_lines=[], always_merge_locale_verification=dict(locale_public_source_path=locale, locale_section='.always_merge', source_lines=[2]))
        fact = self.direct(ver, row)
        self.assertEqual([a['kind'] for a in fact['anchors']], ['always_merge_locale:section', 'always_merge_locale:definition'])

    def test_lowercased_entity_name_matcher_is_the_empty_prefix_case(self):
        # Runbook §34.2 seventh category only matches the prefixed form
        # `"alchemist "..name:lower()`.  The lootable gems in gem.lua use the
        # bare `name = name:lower()`, which has no concatenation at all, so the
        # eighth category must match it and the seventh must not.
        source = (ROOT / 'tools/orchestration/freeze_workset.py').read_text()
        tree = ast.parse(source)
        patterns = {}
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == 'finditer' and isinstance(node.args[0], ast.Constant)):
                pattern = node.args[0].value
                if 'name:lower' in pattern:
                    patterns[pattern] = True
        self.assertEqual(len(patterns), 2, patterns)
        concat = next(p for p in patterns if '\\.\\.' in p)
        lowered = next(p for p in patterns if p != concat)
        prefixed = 'name = "alchemist "..name:lower()'
        bare = '\t\tname = name:lower(), subtype = color,'
        self.assertTrue(re.search(concat, prefixed))
        self.assertFalse(re.search(concat, bare))
        # The eighth category must claim the bare form and keep its hands off
        # the prefixed one, otherwise a gem would attribute under both rules.
        self.assertTrue(re.search(lowered, bare))
        self.assertFalse(re.search(lowered, prefixed))
        # The resolved argument is the lowercase of a named call argument.
        call = '\tnewGem("Fire Opal",\t"object/fireopal.png",5,\t18,\t"red",'
        args = re.findall(r'\(\s*"([^"\\]*)"\s*,', call)
        self.assertEqual([a for a in args if a.lower() == 'fire opal'], ['Fire Opal'])

    def test_always_merge_current_producer_and_missing_section_shapes(self):
        locale = self.config.component('engine').official_locale
        put(self.source, locale, 'section ".always_merge"\nt("' + self.rows[0]['source'] + '", "locale only")\n')
        self.repin()
        row = dict(self.rows[0], component='engine', normalized_path='engine.lua', section='.always_merge')
        # Read the real dictionary expression: current producer includes
        # locale_section, whereas the host's missing-key probe omits it.
        tree = ast.parse((ROOT / 'tools/orchestration/freeze_workset.py').read_text())
        expressions = [n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'always_merge' for t in n.targets)
                       and isinstance(n.value, ast.Dict)]
        self.assertEqual(len(expressions), 1)
        data = eval(compile(ast.Expression(expressions[0]), '<producer-attribution>', 'eval'),
                    {'ALWAYS_MERGE_LOCALE': locale, 'amlines': [2]})
        self.assertEqual(data['locale_section'], '.always_merge')
        for omit in (False, True):
            attribution = dict(data)
            if omit: attribution.pop('locale_section')
            ver = dict(self.ver, component='engine', public_source_path=locale,
                       source_file_sha256=facts.sha((self.source/locale).read_bytes()),
                       matching_literal_lines=[2], always_merge_locale_verification=attribution)
            with self.subTest(omit=omit):
                fact = self.direct(ver, row)
                self.assertEqual([a['kind'] for a in fact['anchors']],
                                 ['literal', 'always_merge_locale:section', 'always_merge_locale:definition'])
                for conflict in ('mod-tome/a.lua', None, ''):
                    with self.subTest(conflict=conflict), self.assertRaisesRegex(ValueError, 'locale attribution'):
                        self.direct(dict(ver, always_merge_locale_verification=dict(attribution, locale_section=conflict)), row)
                with self.assertRaisesRegex(ValueError, 'locale attribution'):
                    self.direct(dict(ver, always_merge_locale_verification=dict(attribution, locale_public_source_path='wrong.lua')), row)
        # A matching declared section cannot substitute for the real fixed text.
        put(self.source, locale, 'section "wrong"\nt("' + self.rows[0]['source'] + '", "locale only")\n')
        self.repin()
        ver.update(fixed_source_commit=self.ver['fixed_source_commit'],
                   source_file_sha256=facts.sha((self.source/locale).read_bytes()))
        with self.assertRaisesRegex(ValueError, 'locale section not found'):
            self.direct(ver, row)

    def test_unpinned_component_isolation_engine_catalog_and_ambiguity(self):
        parent = self.root / 'dlc'
        text = 't("' + self.rows[0]['source'] + '")\n'
        for comp in ('cults', 'orcs'):
            put(parent/comp, f'tome-{comp}/a.lua', text + '-- ' + comp + '\n')
        with mock.patch.dict(os.environ, {'TOME_DLC_ROOT': str(parent)}, clear=False):
            for comp in ('cults', 'orcs'):
                row = dict(self.rows[0], component='engine', normalized_path='engine.lua', section=f'tome-{comp}/a.lua')
                ver = dict(self.ver, component=comp, public_source_path=row['section'], fixed_source_commit=None,
                           source_pinning='unpinned', source_file_sha256=facts.sha((parent/comp/row['section']).read_bytes()))
                fact = self.direct(ver, row)
                self.assertEqual(fact['catalog_component'], 'engine')
                self.assertEqual(fact['source_component'], comp)
                self.assertIn('not pinned', fact['main_source']['disclosure'])
                self.assertIn('-- ' + comp, facts.canonical(fact).decode())
                put(parent/comp, row['section'], text + '-- drift')
                with self.assertRaisesRegex(ValueError, 'SHA mismatch'): self.direct(ver, row)
            (parent/'tome-cults').mkdir()
            with self.assertRaisesRegex(ValueError, 'found 2'):
                facts.component_root(self.config, self.config.component('cults'))

    def test_unpinned_file_and_directory_symlinks_rejected(self):
        root = self.root / 'public'
        put(root, 'real/a.lua', 'public')
        (root/'link').symlink_to('real', target_is_directory=True)
        (root/'a.lua').symlink_to('real/a.lua')
        for path in ('link/a.lua', 'a.lua'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'symlink'):
                facts.FixedReader().unpinned(root, path)
        os.mkfifo(root/'fifo')
        with self.assertRaisesRegex(ValueError, 'ordinary'):
            facts.FixedReader().unpinned(root, 'fifo')

    def test_terminology_exact_framing_scope_tag_status_notes_and_base(self):
        header = 'source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n'
        values = [('core', '', 'review'), ('global', 'nil', 'existing'), ('dlc', '', 'preferred'), ('multi', '', 'existing'), ('addon', '', 'review'), ('global', 'other', 'preferred')]
        raw = header + ''.join(f'source\tterm-{i}\tT.UI.LABEL\tui\t{tag}\t{status}\t{scope}\tnote-{i}\n' for i,(scope,tag,status) in enumerate(values))
        put(self.root, 'terminology/terms.tsv', raw)
        base = commit(self.root, 'scoped terms')
        digest = wp1.terminology_snapshot(self.root)
        rows = facts.terminology_rows(self.root, base, {digest}, facts.FixedReader())
        builder = facts.FactBuilder(self.root, self.config, facts.FixedReader(), rows)
        result = builder.fact(self.rows[0], self.ver)
        self.assertEqual([r['target'] for r in result['terminology']], ['term-0', 'term-3'])
        self.assertEqual([r['status'] for r in result['terminology']], ['review', 'existing'])
        self.assertEqual([r['notes'] for r in result['terminology']], ['note-0', 'note-3'])
        nil = builder.fact(dict(self.rows[0], source_tag=None), self.ver)
        self.assertEqual([r['target'] for r in nil['terminology']], ['term-1'])
        put(self.root, 'terminology/terms.tsv', raw.replace('term-', 'drift-'))
        self.assertEqual(facts.terminology_rows(self.root, base, {digest}, facts.FixedReader()), rows)
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            facts.terminology_rows(self.root, base, {'f'*64}, facts.FixedReader())
        # Current fallback uses the production digest, never the store digest.
        current = wp1.terminology_snapshot(self.root)
        self.assertEqual(facts.terminology_rows(self.root, base, {current}, facts.FixedReader())[0]['target'], 'drift-0')

    def test_nested_terminology_base_uses_production_path_order_after_deletion(self):
        header = 'source\ttarget\tcategory\tdomain\tsource_tag\tstatus\tscope\tnotes\n'
        for name in ('a-b.tsv', 'a-b/c.tsv'):
            put(self.root, 'terminology/' + name, header +
                f'source\t{name}\tT.UI.LABEL\tui\t\treview\tcore\tfixture\n')
        base = commit(self.root, 'nested terminology ordering')
        digest = wp1.terminology_snapshot(self.root)
        rows = facts.terminology_rows(self.root, base, {digest}, facts.FixedReader())
        self.assertEqual([r['file'] for r in rows],
                         ['terminology/a-b/c.tsv', 'terminology/a-b.tsv', 'terminology/terms.tsv'])
        shutil.rmtree(self.root / 'terminology')
        (self.root / 'TERMINOLOGY.md').unlink()
        self.assertEqual(facts.terminology_rows(self.root, base, {digest}, facts.FixedReader()), rows)
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            facts.terminology_rows(self.root, base, {'f'*64}, facts.FixedReader())

    def test_missing_producer_identity_metadata_is_not_defaulted(self):
        for key in ('source_pinning', 'fixed_source_commit'):
            ws = copy.deepcopy(self.ws)
            ws['source_verification'][0].pop(key)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'source binding'):
                self.build(ws)

    def test_pack_identity_equals_encoding_preflight_and_bounds(self):
        package = self.build()
        suffix = facts.bound_context(package, package['entries'][0])
        self.assertNotIn('=', suffix)
        decoded = json.loads(suffix.split(facts.CONTEXT_MARKER)[1])
        self.assertIn('args_order=untrusted', facts.canonical(decoded).decode())
        rebuilt = dict(decoded['binding'], entries=[decoded['fact']])
        self.assertEqual(decoded['package_sha256'], facts.sha(facts.canonical(rebuilt)))
        self.assertEqual(rebuilt, package)
        for remap in (None, [2, 1]):
            source, target = '%s %d', '%d %s' if remap else '%s %d'
            context = 'fixture' + (' args_order={2,1}' if remap else '') + suffix
            payload = dict(contract='translation_contextual_v2', ordered_revision_keys=['key'], translation_snapshot=[dict(revision_key='key',source=source,target=target)], fixed_source_identity='fixed', terminology_snapshot='terms', bounded_context=[dict(revision_key='key',context=context)],rendered_briefing='review')
            put(self.root, 'fixture.lua', 'section "fixture"\nt("%s %d", "' + target + '", ""' + (', {2,1}' if remap else '') + ')\n')
            scope = dict(schema_version=1, allowed_files=['fixture.lua'], anchor_scopes=[dict(file='fixture.lua',section_path='fixture',ordered_titles=[])])
            sp = put(self.root, 'scope.json', facts.canonical(scope))
            pp = put(self.root, 'payload.json', facts.canonical(payload))
            result = anchor_preflight.run_preflight(sp, pp, workspace_root=self.root)
            self.assertEqual(result.status, 'PREFLIGHT_VERIFIED', result.errors)
        with mock.patch.object(facts, 'MAX_FACT_BYTES', 1), self.assertRaisesRegex(ValueError, 'exceed'):
            self.build()
        with mock.patch.object(facts, 'MAX_RUN_BYTES', 1), self.assertRaisesRegex(ValueError, 'exceed'):
            self.build()
        kinds = self.attribution_fixture()
        with mock.patch.object(facts, 'MAX_ANCHORS', 1), self.assertRaisesRegex(ValueError, 'exceed'):
            self.direct(dict(self.ver, interface_mixin_verification=kinds['interface_mixin_verification']))
        with mock.patch.object(facts, 'MAX_LINES', 1), self.assertRaisesRegex(ValueError, 'exceed'):
            self.direct(dict(self.ver, interface_mixin_verification=kinds['interface_mixin_verification']))


if __name__ == '__main__':
    unittest.main()
