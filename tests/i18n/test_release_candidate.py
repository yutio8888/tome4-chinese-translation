"""Isolated VFS placement and byte-exact rollback (bare and archived Engine)."""
import io
from pathlib import Path
from types import SimpleNamespace
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import shutil

from tools.i18nlib import release_candidate as rc
from tools.i18nlib.full_review import FullReviewError, canonical, sha


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = SimpleNamespace(root=self.root, version='tome-1.7.6',
            repositories={'engine': SimpleNamespace(commit='a'*40)}, repository_path=lambda name: self.root/'source')
        self.candidate = self.root/'.artifacts/i18n/release-candidate/test'
        self.candidate.mkdir(parents=True)
        engine = self.candidate / 'engine' / rc.ENGINE_LOCALE
        engine.parent.mkdir(parents=True)
        engine.write_bytes(b'-- candidate Engine with COPY flags\n')
        self.engine = engine.read_bytes()
        (self.candidate/'addon').mkdir()
        (self.candidate/'addon/init.lua').write_bytes(b'init')
        with zipfile.ZipFile(self.candidate/'tome-test.teaa', 'w', compression=zipfile.ZIP_STORED) as archive:
            archive.writestr('init.lua', b'init')
        self.seal()
        self.target = self.root/'.artifacts/i18n/isolated-game/test'
        (self.target/'game/loader').mkdir(parents=True)
        (self.target/'game/loader/init.lua').write_bytes(b'fixed-loader')
        self.fixed = {'game/loader/init.lua': b'fixed-loader',
            'game/engines/default/engine/init.lua': b'fixed-init',
            'game/engines/default/engine/version.lua': b'fixed-version'}
        self.reader = patch('orchestration.build_evidence_pack.FixedReader.pinned',
            side_effect=lambda root, commit, name: (self.fixed[name], 'oid'))
        self.reader.start()
        self.addCleanup(self.reader.stop)

    def seal(self):
        files = rc.file_manifest(self.candidate)
        files.pop('candidate.json', None)
        record = {'files': files, 'engine_build_sha256': sha(self.engine), 'package': 'tome-test.teaa'}
        (self.candidate/'candidate.json').write_bytes(canonical(record))

    def setup_target(self, layout):
        if layout == 'teae':
            shutil.rmtree(self.target/'game/engines/default', ignore_errors=True)
        self.spec = {'version': 'tome-1.7.6', 'layout': layout,
            'engine_path': 'game/engines/default' if layout == 'bare' else 'game/engines/te4-1.7.6.teae',
            'guards': [{'path': 'game/loader/init.lua', 'sha256': sha(b'fixed-loader')}]}
        if layout == 'bare':
            root = self.target/self.spec['engine_path']
            (root/'engine').mkdir(parents=True)
            (root/'engine/init.lua').write_bytes(b'fixed-init')
            (root/'engine/version.lua').write_bytes(b'fixed-version')
            self.resource = root / rc.ENGINE_LOCALE
            self.resource.parent.mkdir(parents=True, exist_ok=True)
            self.before = b'old-Engine'
            self.resource.write_bytes(self.before)
        else:
            self.resource = self.target/self.spec['engine_path']
            self.resource.parent.mkdir(parents=True, exist_ok=True)
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w') as archive:
                archive.writestr('engine/init.lua', b'fixed-init')
                archive.writestr('engine/version.lua', b'fixed-version')
                archive.writestr(rc.ENGINE_LOCALE, b'old-Engine')
            self.before = stream.getvalue()
            self.resource.write_bytes(self.before)
        self.spec['original_sha256'] = sha(self.before)
        self.spec_path = self.root/'spec.json'
        self.spec_path.write_bytes(canonical(self.spec))

    def test_bare_and_teae_place_engine_in_pre_init_vfs_and_restore_exact_bytes(self):
        for layout in ['bare', 'teae']:
            with self.subTest(layout=layout):
                self.setup_target(layout)
                result = rc.install(self.manifest, self.candidate, self.target, self.spec_path, layout)
                self.assertEqual(result['GUI'], 'untested')
                self.assertEqual(result['homepath'],'home-unverified')
                self.assertEqual(result['init_before_module_vfs'],'game-dir-structure-only')
                self.assertEqual(rc.install(self.manifest, self.candidate, self.target, self.spec_path, layout), result)
                self.assertTrue((self.target/'game/addons/tome-test.teaa').is_file())
                if layout == 'teae':
                    self.assertEqual(rc.zip_members(self.resource.read_bytes())[rc.ENGINE_LOCALE], self.engine)
                else:
                    self.assertEqual(self.resource.read_bytes(), self.engine)
                rc.restore(self.manifest, self.target, layout)
                self.assertEqual(self.resource.read_bytes(), self.before)
                rc.restore(self.manifest, self.target, layout)

    def test_all_install_publication_boundaries_recover_with_existing_addon(self):
        self.setup_target('bare')
        addon = self.target/'game/addons/tome-test.teaa'
        addon.parent.mkdir(parents=True); addon.write_bytes(b'original-addon')
        self.spec['addon_original_sha256'] = sha(addon.read_bytes())
        self.spec_path.write_bytes(canonical(self.spec))
        original_immutable, original_replace = rc.immutable, rc.atomic_replace
        for boundary in ('backup.bin','addon-backup.bin','intent.json','engine-replaced','addon-replaced','installed.json'):
            def freeze(path, raw):
                original_immutable(path,raw)
                if Path(path).name == boundary:
                    raise OSError('controlled interruption after '+boundary)
            def replace(path, raw):
                original_replace(path,raw)
                if (boundary == 'engine-replaced' and Path(path) == self.resource or
                        boundary == 'addon-replaced' and Path(path) == addon):
                    raise OSError('controlled interruption after '+boundary)
            with self.subTest(boundary=boundary):
                with patch.object(rc,'immutable',side_effect=freeze), patch.object(rc,'atomic_replace',side_effect=replace):
                    with self.assertRaises(OSError):
                        rc.install(self.manifest,self.candidate,self.target,self.spec_path,boundary.replace('.','-'))
                op = self.target/'.full-review-install'/boundary.replace('.','-')
                if not (op/'intent.json').exists():
                    # No published transaction: identical backups allow normal retry.
                    rc.install(self.manifest,self.candidate,self.target,self.spec_path,boundary.replace('.','-'))
                rc.restore(self.manifest,self.target,boundary.replace('.','-'))
                self.assertEqual(self.resource.read_bytes(),self.before)
                self.assertEqual(addon.read_bytes(),b'original-addon')

    def test_legacy_missing_backup_only_recovers_exact_before_bytes(self):
        self.setup_target('bare')
        original = rc.atomic_replace
        with patch.object(rc,'atomic_replace',side_effect=OSError('before replacement')):
            with self.assertRaises(OSError):
                rc.install(self.manifest,self.candidate,self.target,self.spec_path,'legacy')
        backup = self.target/'.full-review-install/legacy/backup.bin'
        backup.unlink()
        rc.restore(self.manifest,self.target,'legacy')
        self.assertEqual(self.resource.read_bytes(),self.before)
        self.resource.write_bytes(self.engine)
        with self.assertRaisesRegex(FullReviewError,'missing rollback backup'):
            rc.restore(self.manifest,self.target,'legacy')

    def test_release_readiness_requires_each_exact_candidate_target_operation_proof(self):
        from tools.i18nlib import full_review as fr
        import copy
        self.setup_target('bare')
        rc.install(self.manifest,self.candidate,self.target,self.spec_path,'measured')
        intent = fr.read(self.target/'.full-review-install/measured/installed.json')
        binding = {'candidate_sha256':sha((self.candidate/'candidate.json').read_bytes()),
            'target':str(self.target),'spec_sha256':intent['spec_sha256'],'operation_id':'measured',
            'installed_sha256':sha(canonical(intent))}
        proof_root = self.root/'evidence/full-review/test-round'
        proof_root.mkdir(parents=True)
        proofs = []
        for name in ('engine','launch','scenario'):
            artifact = proof_root/(name+'.json')
            artifact.write_bytes(canonical({'status':'passed','binding':binding,'measurement':'controlled test proof'}))
            proofs.append({'status':'passed','binding':binding,'evidence':[
                {'path':artifact.relative_to(self.root).as_posix(),'sha256':sha(artifact.read_bytes())}]})
        readiness = {'engine_actual_loading':proofs[0],'game_launch':proofs[1],'scenarios':[proofs[2]]}
        self.assertTrue(fr.release_readiness(self.manifest,self.candidate,readiness))
        for field, value in [('candidate_sha256','0'*64),('spec_sha256','0'*64),
                             ('operation_id','wrong-op'),('installed_sha256','0'*64)]:
            bad = copy.deepcopy(readiness)
            bad['engine_actual_loading']['binding'][field] = value
            with self.subTest(field=field), self.assertRaises((FullReviewError,OSError)):
                fr.release_readiness(self.manifest,self.candidate,bad)
        old = {'engine_actual_loading':'passed','game_launch':'passed','scenarios':[proofs[2]]}
        self.assertFalse(fr.release_readiness(self.manifest,self.candidate,old))
        bad = copy.deepcopy(readiness)
        artifact = proof_root/'engine.json'
        artifact.write_bytes(canonical({'status':'passed','binding':dict(binding,candidate_sha256='0'*64)}))
        bad['engine_actual_loading']['evidence'][0]['sha256']=sha(artifact.read_bytes())
        with self.assertRaisesRegex(FullReviewError,'artifact binding mismatch'):
            fr.release_readiness(self.manifest,self.candidate,bad)
        rc.restore(self.manifest,self.target,'measured')
        with self.assertRaises(FullReviewError):
            fr.release_readiness(self.manifest,self.candidate,readiness)

    def test_wrong_version_layout_and_original_hash_do_not_write(self):
        self.setup_target('bare')
        for field, value in [('version', 'wrong'), ('engine_path', 'other/default'), ('original_sha256', '0'*64)]:
            wrong = dict(self.spec, **{field: value})
            self.spec_path.write_bytes(canonical(wrong))
            with self.assertRaises(FullReviewError):
                rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'reject')
            self.assertEqual(self.resource.read_bytes(), self.before)

    def test_drifted_resource_or_backup_rejects_restore(self):
        self.setup_target('bare')
        rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'drift')
        self.resource.write_bytes(b'user-edit')
        with self.assertRaises(FullReviewError):
            rc.restore(self.manifest, self.target, 'drift')
        self.assertEqual(self.resource.read_bytes(), b'user-edit')
        self.resource.write_bytes(self.engine)
        (self.target/'.full-review-install/drift/backup.bin').write_bytes(b'wrong-backup')
        with self.assertRaises(FullReviewError):
            rc.restore(self.manifest, self.target, 'drift')
        self.assertEqual(self.resource.read_bytes(), self.engine)

    def test_interruption_after_replace_recovers_from_durable_intent(self):
        self.setup_target('bare')
        original = rc.immutable
        def interrupted(path, raw):
            if Path(path).name == 'installed.json':
                raise OSError('interrupted before success receipt')
            return original(path, raw)
        with patch.object(rc, 'immutable', side_effect=interrupted):
            with self.assertRaises(OSError):
                rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'interrupt')
        self.assertEqual(self.resource.read_bytes(), self.engine)
        rc.restore(self.manifest, self.target, 'interrupt')
        self.assertEqual(self.resource.read_bytes(), self.before)

    def test_missing_engine_copy_or_external_link_is_rejected(self):
        resource = self.candidate/'engine'/rc.ENGINE_LOCALE
        resource.unlink()
        with self.assertRaises(FullReviewError):
            rc.verify_candidate(self.candidate)
        resource.write_bytes(self.engine+b'copy drift')
        with self.assertRaises(FullReviewError):
            rc.verify_candidate(self.candidate)
        resource.unlink()
        resource.symlink_to(self.root/'outside')
        with self.assertRaises(FullReviewError):
            rc.verify_candidate(self.candidate)

    def test_formal_or_symlink_target_refused(self):
        with self.assertRaises(FullReviewError):
            rc.isolated(self.manifest, self.root/'formal-game', 'isolated-game')
        (self.target/'external').symlink_to(self.root)
        with self.assertRaises(FullReviewError):
            rc.file_manifest(self.target)

    def test_normalized_target_escape_and_ambiguous_engine_are_rejected(self):
        escape = self.root/'.artifacts/i18n/isolated-game/test/../../../../formal-game'
        with self.assertRaises(FullReviewError):
            rc.isolated(self.manifest, escape, 'isolated-game')
        self.setup_target('bare')
        other = self.target/'game/engines/other/engine/version.lua'
        other.parent.mkdir(parents=True)
        other.write_bytes(b'fixed-version')
        with self.assertRaises(FullReviewError):
            rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'ambiguous')
        self.assertEqual(self.resource.read_bytes(), self.before)

    def test_archive_traversal_duplicates_and_links_rejected(self):
        for names in [('engine/init.lua', 'engine/init.lua'), ('../external',), ('/external',)]:
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w') as archive:
                for name in names:
                    archive.writestr(name, b'data')
            with self.assertRaises(FullReviewError):
                rc.zip_members(stream.getvalue())
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            info = zipfile.ZipInfo('engine/link')
            info.external_attr = 0o120777 << 16
            archive.writestr(info, b'outside')
        with self.assertRaises(FullReviewError):
            rc.zip_members(stream.getvalue())

    def test_git_archive_link_refused_before_extraction(self):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w') as archive:
            info = tarfile.TarInfo('link')
            info.type = tarfile.SYMTYPE
            info.linkname = '/outside'
            archive.addfile(info)
        with patch.object(rc, 'run', return_value=stream.getvalue()):
            with self.assertRaises(FullReviewError):
                rc.archive_tree(self.root, 'a'*40, self.root/'archive')
        self.assertFalse((self.root/'archive').exists())

    def test_partial_engine_then_addon_interruption_restores_both(self):
        self.setup_target('bare')
        replace = rc.atomic_replace
        def interrupt(path, raw):
            if Path(path).suffix == '.teaa':
                raise OSError('interrupted before addon replacement')
            replace(path, raw)
        with patch.object(rc, 'atomic_replace', side_effect=interrupt):
            with self.assertRaises(OSError):
                rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'partial')
        self.assertEqual(self.resource.read_bytes(), self.engine)
        rc.restore(self.manifest, self.target, 'partial')
        self.assertEqual(self.resource.read_bytes(), self.before)
        self.assertFalse((self.target/'game/addons/tome-test.teaa').exists())

    def test_addon_drift_blocks_rollback_before_any_resource_change(self):
        self.setup_target('bare')
        rc.install(self.manifest, self.candidate, self.target, self.spec_path, 'addon-drift')
        (self.target/'game/addons/tome-test.teaa').write_bytes(b'user-change')
        with self.assertRaises(FullReviewError):
            rc.restore(self.manifest, self.target, 'addon-drift')
        self.assertEqual(self.resource.read_bytes(), self.engine)
