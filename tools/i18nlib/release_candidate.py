"""Isolated release assembly and init-before-module Engine installation.

No writes to the formal release repository. Only explicit artifact candidates
and artifact game copies are mutation targets; archives reject links and traversal.
"""
from __future__ import annotations

from contextlib import contextmanager
import io
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

from .full_review import FullReviewError, canonical, immutable, ordinary, read, safe_path, sha, token
from .build import build_full_locales
from .locale_model import LocaleLoader
from .runtime import LuaRuntime
from .publish import publish_addon

ENGINE_LOCALE = 'data/locales/engine/zh_hans.lua'


def run(args, *, cwd=None, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=240)
    if result.returncode:
        raise FullReviewError(f'{args[0]} failed: {result.stderr.decode(errors="replace")[-2000:]}')
    return result.stdout


def isolated(manifest, path, category):
    path = Path(path).absolute()
    if '..' in path.parts or path != path.resolve():
        raise FullReviewError('isolated root must have an exact normalized physical path')
    base = manifest.root.absolute() / '.artifacts/i18n' / category
    if path == base or not path.is_relative_to(base):
        raise FullReviewError(f'only explicit isolated {category}/<id> allowed')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise FullReviewError('symlink isolated root')
    return path


def file_manifest(root):
    root = Path(root)
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise FullReviewError('release/target tree contains symlink')
        if path.is_file() and '.git' not in path.relative_to(root).parts:
            result[path.relative_to(root).as_posix()] = sha(ordinary(path))
        elif not path.is_dir() and not path.is_file():
            raise FullReviewError('nonordinary tree member')
    return result


@contextmanager
def addon_environment(path):
    old = os.environ.get('TOME_ADDON_ROOT')
    os.environ['TOME_ADDON_ROOT'] = str(path)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop('TOME_ADDON_ROOT', None)
        else:
            os.environ['TOME_ADDON_ROOT'] = old


def archive_tree(repository, commit, destination):
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise FullReviewError('release commit must be exact full OID')
    raw = run(['git', '-C', str(repository), 'archive', '--format=tar', commit])
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = archive.getmembers()
        for member in members:
            safe_path(destination, member.name.rstrip('/'))
            if not member.isfile() and not member.isdir():
                raise FullReviewError('archive symlink/submodule/special member rejected')
        for member in members:
            path = safe_path(destination, member.name.rstrip('/'))
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(archive.extractfile(member).read())
                path.chmod(member.mode & 0o777)
    return sha(raw)


def assemble(manifest, candidate_id, release_commit):
    token(candidate_id)
    destination = isolated(manifest, manifest.root / '.artifacts/i18n/release-candidate' / candidate_id,
                           'release-candidate')
    if destination.exists():
        # Recovery accepts only a fully sealed identical candidate; never republish drift.
        record = verify_candidate(destination)
        if record['release_commit'] != release_commit or record['input_hashes'] != input_hashes(manifest):
            raise FullReviewError('candidate recovery input drift')
        return record
    formal = manifest.repository_path('addon')
    destination.mkdir(parents=True)
    addon = destination / 'addon'
    addon.mkdir()
    archive_sha = archive_tree(formal, release_commit, addon)
    # Independent local metadata includes the selected upstream OID for doctor.
    # git clone copies objects rather than linking them; no shared writable object store.
    metadata = destination / 'upstream-objects'
    run(['git', 'clone', '--bare', '--no-hardlinks', '--no-local', str(formal), str(metadata)])
    run(['git', 'init', str(addon)])
    shutil.copytree(metadata / 'objects', addon / '.git/objects', dirs_exist_ok=True)
    shutil.rmtree(metadata)
    run(['git', '-C', str(addon), 'update-ref', 'refs/heads/input', release_commit])
    # No staging or commits: archive working files are publish's isolated inputs.
    runtime = LuaRuntime(manifest)
    loader = LocaleLoader(runtime)
    with addon_environment(addon):
        run(['python3', '-B', str(manifest.root / 'tools/i18n'), 'doctor', '--json'])
        dry = publish_addon(manifest, loader, apply=False, bump=False, commit=False)
        applied = publish_addon(manifest, loader, apply=True, bump=False, commit=False)
    engine = build_full_locales(manifest, loader, [manifest.component('engine')])
    resource = destination / 'engine' / ENGINE_LOCALE
    resource.parent.mkdir(parents=True)
    built = Path(engine['components'][0]['output'])
    resource.write_bytes(ordinary(built))
    if sha(ordinary(resource)) != engine['components'][0]['sha256']:
        raise FullReviewError('Engine build bytes drift')
    # Engine is an explicit companion resource in release root, never addon-only.
    init = ordinary(addon / 'init.lua').decode('utf-8')
    names = {}
    for key in ('for_module', 'short_name'):
        match = re.search(r'\b' + key + r'\s*=\s*["\']([a-zA-Z0-9_-]+)["\']', init)
        if not match:
            raise FullReviewError('addon root init lacks safe package identity')
        names[key] = match[1]
    package = destination / (names['for_module'] + '-' + names['short_name'] + '.teaa')
    run(['zip', '-r', '-0', str(package.absolute()), '.', '-x', '.git/*'], cwd=addon)
    with zipfile.ZipFile(package) as archive:
        if 'init.lua' not in archive.namelist() or any(i.compress_type != zipfile.ZIP_STORED for i in archive.infolist()):
            raise FullReviewError('addon packaging layout/compression mismatch')
    instructions = ('GPL v3 or later; retain upstream copyright and supply corresponding source.\n'
        'Engine companion: engine/data/locales/engine/zh_hans.lua.\n'
        'Use full_review install only with an isolated-game target manifest.\n'
        'Placement checks game-dir structure only; homepath/VFS priority remains home-unverified.\n'
        'Final exact candidate must be launched with a recorded isolated home and actual loading evidence.\n'
        'Restore checks installed and backup hashes; reject drift. GUI/game scenarios untested.\n')
    (destination / 'INSTALL.txt').write_text(instructions, encoding='utf-8')
    record = {'schema_version': 1, 'candidate_id': candidate_id, 'release_commit': release_commit,
        'archive_sha256': archive_sha, 'input_hashes': input_hashes(manifest),
        'engine_build_sha256': engine['components'][0]['sha256'], 'package': package.name,
        'publish_dry_run': dry, 'publish_apply': applied,
        'corresponding_source': {'release_commit': release_commit,
            'engine_commit': manifest.repositories['engine'].commit,
            'canonical_inputs': input_hashes(manifest), 'DLC_source_commit': None,
            'DLC_source_pinning': 'unpinned', 'license': 'GPL-3.0-or-later'},
        'engine_loading': 'unmeasured', 'game_launch': 'unmeasured for this exact candidate; official binary capability separately verified',
        'GUI': 'untested', 'files': file_manifest(destination)}
    immutable(destination / 'candidate.json', canonical(record))
    return record


def input_hashes(manifest):
    paths = {component.translation for component in manifest.components}
    paths.update(c.copy_fragment for c in manifest.components if c.copy_fragment)
    paths.add(manifest.path.relative_to(manifest.root).as_posix())
    paths.update({manifest.policy, 'TERMINOLOGY.md', 'tools/i18nlib/build.py',
        'tools/i18nlib/publish.py', 'tools/i18nlib/locale_model.py', 'tools/i18nlib/runtime.py',
        'tools/i18nlib/config.py', 'tools/i18nlib/production_review_v2_lite.py',
        'tools/i18nlib/release_candidate.py', 'tools/lua/load_locale.lua'})
    paths.update(p.relative_to(manifest.root).as_posix() for p in (manifest.root/'terminology').rglob('*') if p.is_file())
    paths.update(p.relative_to(manifest.root).as_posix() for p in (manifest.root / 'locale').rglob('*') if p.is_file())
    return {name: sha(ordinary(safe_path(manifest.root, name))) for name in sorted(paths)}


def verify_candidate(directory):
    record = read(Path(directory) / 'candidate.json')
    actual = file_manifest(directory)
    actual.pop('candidate.json', None)
    if (not re.fullmatch('[0-9a-f]{64}', record.get('engine_build_sha256', '')) or
            actual != record['files'] or actual.get('engine/' + ENGINE_LOCALE) != record['engine_build_sha256']):
        raise FullReviewError('candidate Engine/copy/package bytes missing or drifted')
    package = record.get('package')
    if not isinstance(package, str) or not re.fullmatch('[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+\.teaa', package):
        raise FullReviewError('candidate package identity missing')
    with zipfile.ZipFile(io.BytesIO(ordinary(Path(directory) / package))) as archive:
        if any(i.compress_type != zipfile.ZIP_STORED for i in archive.infolist()):
            raise FullReviewError('candidate package must use zip -0')
    packaged = zip_members(ordinary(Path(directory) / package))
    addon = Path(directory) / 'addon'
    expected = {name: ordinary(addon / name) for name in file_manifest(addon)}
    if 'init.lua' not in packaged or packaged != expected:
        raise FullReviewError('candidate addon archive does not exactly represent release tree')
    if (addon / '.git/objects/info/alternates').exists() or (addon / '.git').is_file():
        raise FullReviewError('candidate Git metadata is not isolated')
    return record


def zip_members(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = [i.filename for i in archive.infolist()]
        if len(names) != len(set(names)):
            raise FullReviewError('duplicate engine archive members')
        for info in archive.infolist():
            path = PurePosixPath(info.filename.rstrip('/'))
            if (not info.filename or path.is_absolute() or '..' in path.parts or '\\' in info.filename or
                    any(part in ('', '.') for part in info.filename.rstrip('/').split('/'))):
                raise FullReviewError('unsafe engine archive member')
            mode = info.external_attr >> 16
            if mode & 0o170000 not in (0, 0o100000, 0o040000):
                raise FullReviewError('engine archive link/special member')
        return {i.filename: archive.read(i) for i in archive.infolist() if not i.is_dir()}


def target_files(manifest, target, spec):
    target = isolated(manifest, target, 'isolated-game')
    if spec.get('version') != manifest.version or spec.get('layout') not in {'bare', 'teae'}:
        raise FullReviewError('unsupported/wrong target version or layout')
    file_manifest(target)  # reject links throughout explicit isolated copy
    for item in spec.get('guards', []):
        if sha(ordinary(safe_path(target, item['path']))) != item['sha256']:
            raise FullReviewError('target guard drift')
    engine_path = spec['engine_path']
    available = [path.relative_to(target).as_posix() for path in (target/'game/engines').iterdir()
                 if path.is_file() and path.suffix == '.teae' or path.is_dir() and (path/'engine/version.lua').is_file()]
    if available != [engine_path]:
        raise FullReviewError('unsupported ambiguous Engine selection in isolated target')
    if spec['layout'] == 'bare':
        if not re.fullmatch(r'game/engines/[a-zA-Z0-9_-]+', engine_path):
            raise FullReviewError('bare Engine is outside loader mount')
        root = safe_path(target, engine_path)
        if not root.is_dir():
            raise FullReviewError('missing bare Engine')
        files = {name: ordinary(root / name) for name in ('engine/init.lua', 'engine/version.lua')}
    else:
        if not re.fullmatch(r'game/engines/te4-1\.7\.6\.teae', engine_path):
            raise FullReviewError('archive Engine is outside loader mount')
        files = zip_members(ordinary(safe_path(target, engine_path)))
    # Exact fixed loader, Engine init and version bind mount and version claims.
    reader = __import__('orchestration.build_evidence_pack', fromlist=['FixedReader']).FixedReader()
    source = manifest.repository_path('engine')
    commit = manifest.repositories['engine'].commit
    loader, _ = reader.pinned(source, commit, 'game/loader/init.lua')
    if ordinary(target / 'game/loader/init.lua') != loader:
        raise FullReviewError('unsupported loader bytes')
    for name in ('engine/init.lua', 'engine/version.lua'):
        expected, _ = reader.pinned(source, commit, 'game/engines/default/' + name)
        if files.get(name) != expected:
            raise FullReviewError('Engine fixed version/init mismatch')
    return target


def atomic_replace(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.engine-install-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def install(manifest, candidate, target, spec_path, operation_id):
    token(operation_id)
    candidate = isolated(manifest, candidate, 'release-candidate')
    record = verify_candidate(candidate)
    spec = read(spec_path)
    target = target_files(manifest, target, spec)
    engine = ordinary(candidate / 'engine' / ENGINE_LOCALE)
    path = safe_path(target, spec['engine_path'] + '/' + ENGINE_LOCALE if spec['layout'] == 'bare' else spec['engine_path'])
    operation = target / '.full-review-install' / operation_id
    package_name = record['package']
    if not re.fullmatch('[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+\.teaa', package_name):
        raise FullReviewError('unsafe candidate addon package name')
    addon_path = safe_path(target, 'game/addons/' + package_name)
    addon_bytes = ordinary(candidate / package_name)
    if (operation / 'intent.json').exists():
        old = read(operation / 'intent.json')
        if (old['target'] != str(target) or old['candidate_sha256'] != sha(ordinary(candidate / 'candidate.json')) or
                old['spec_sha256'] != sha(ordinary(spec_path))):
            raise FullReviewError('installation recovery identity drift')
        current = ordinary(path) if path.exists() else None
        installed_addon = ordinary(addon_path) if addon_path.exists() else None
        if (sha(current) if current is not None else None) == old['after_sha256'] and installed_addon == addon_bytes:
            immutable(operation / 'installed.json', canonical(old))
            return {'installed': True, 'resource': old['resource'], 'after_sha256': old['after_sha256'],
                    'init_before_module_vfs': 'game-dir-structure-only', 'homepath': 'home-unverified', 'game_launch': 'untested', 'GUI': 'untested'}
        raise FullReviewError('partial installation: restore durable intent, then choose fresh operation ID')
    before = ordinary(path) if path.exists() else None
    addon_before = ordinary(addon_path) if addon_path.exists() else None
    if (sha(addon_before) if addon_before is not None else None) != spec.get('addon_original_sha256'):
        raise FullReviewError('existing addon package hash mismatch')
    if (sha(before) if before is not None else None) != spec.get('original_sha256'):
        raise FullReviewError('existing target resource hash mismatch')
    if spec['layout'] == 'teae':
        members = zip_members(before)
        members[ENGINE_LOCALE] = engine
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
            for name, data in sorted(members.items()):
                archive.writestr(name, data)
        after = stream.getvalue()
    else:
        after = engine
    # Durable intent and backup precede replacement: restore handles crash on either side.
    intent = {'target': str(target), 'resource': path.relative_to(target).as_posix(),
        'before_sha256': sha(before) if before is not None else None, 'after_sha256': sha(after),
        'candidate_sha256': sha(ordinary(candidate / 'candidate.json')), 'spec': spec,
        'spec_sha256': sha(ordinary(spec_path)), 'engine_sha256': sha(engine),
        'addon_resource': addon_path.relative_to(target).as_posix(),
        'addon_before_sha256': sha(addon_before) if addon_before is not None else None,
        'addon_after_sha256': sha(addon_bytes)}
    if before is not None:
        immutable(operation / 'backup.bin', before)
    if addon_before is not None:
        immutable(operation / 'addon-backup.bin', addon_before)
    immutable(operation / 'intent.json', canonical(intent))
    # Freeze guard identity immediately before mutation.
    target_files(manifest, target, spec)
    if (ordinary(path) if path.exists() else None) != before:
        raise FullReviewError('target changed before installation')
    if (ordinary(addon_path) if addon_path.exists() else None) != addon_before:
        raise FullReviewError('addon changed before installation')
    atomic_replace(path, after)
    atomic_replace(addon_path, addon_bytes)
    if spec['layout'] == 'teae' and zip_members(ordinary(path)).get(ENGINE_LOCALE) != engine:
        raise FullReviewError('archive VFS Engine verification failed')
    if spec['layout'] == 'bare' and ordinary(path) != engine:
        raise FullReviewError('bare VFS Engine verification failed')
    immutable(operation / 'installed.json', canonical(intent))
    return {'installed': True, 'resource': intent['resource'], 'after_sha256': sha(after),
            'init_before_module_vfs': 'game-dir-structure-only', 'homepath': 'home-unverified', 'game_launch': 'untested', 'GUI': 'untested'}


def restore(manifest, target, operation_id):
    target = isolated(manifest, target, 'isolated-game')
    operation = target / '.full-review-install' / token(operation_id)
    intent = read(operation / 'intent.json')
    if intent['target'] != str(target):
        raise FullReviewError('rollback target identity mismatch')
    # Check version/init/mount guards again, excluding mutable locale/archive hash.
    target_files(manifest, target, intent['spec'])
    path = safe_path(target, intent['resource'])
    current = ordinary(path) if path.exists() else None
    digest = sha(current) if current is not None else None
    if digest not in {intent['before_sha256'], intent['after_sha256']}:
        raise FullReviewError('rollback installed-byte drift')
    before_hash = intent['before_sha256']
    backup = (ordinary(operation / 'backup.bin') if (operation / 'backup.bin').exists() else
              current if digest == before_hash else None) if before_hash is not None else None
    if before_hash is not None and backup is None:
        raise FullReviewError('missing rollback backup after replacement')
    if backup is not None and sha(backup) != before_hash:
        raise FullReviewError('rollback backup drift')
    addon_path = safe_path(target, intent['addon_resource'])
    addon_current = ordinary(addon_path) if addon_path.exists() else None
    addon_digest = sha(addon_current) if addon_current is not None else None
    if addon_digest not in {intent['addon_before_sha256'], intent['addon_after_sha256']}:
        raise FullReviewError('rollback addon drift')
    addon_backup = (ordinary(operation / 'addon-backup.bin') if (operation / 'addon-backup.bin').exists() else
                    addon_current if addon_digest == intent['addon_before_sha256'] else None) if intent['addon_before_sha256'] is not None else None
    if intent['addon_before_sha256'] is not None and addon_backup is None:
        raise FullReviewError('missing addon rollback backup after replacement')
    if addon_backup is not None and sha(addon_backup) != intent['addon_before_sha256']:
        raise FullReviewError('rollback addon backup drift')
    if addon_digest == intent['addon_after_sha256']:
        if addon_backup is None:
            addon_path.unlink()
        else:
            atomic_replace(addon_path, addon_backup)
    if digest == intent['after_sha256']:
        if backup is None:
            path.unlink()
        else:
            atomic_replace(path, backup)
    immutable(operation / 'restored.json', canonical(intent))
    return {'restored': True, 'sha256': before_hash}
