#!/usr/bin/env python3
"""Bounded public source facts. Importing this module performs no I/O.

The CLI keeps the historical ``<batch> [--context 3] [--siblings 4]`` shape;
``--siblings`` is accepted for compatibility but never scans translations.
All construction completes before the CLI writes its single output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess

MAX_ANCHORS = 8
MAX_LINES = 120
MAX_FACT_BYTES = 32 * 1024
MAX_RUN_BYTES = 512 * 1024
CONTEXT_MARKER = '\nsource_facts_v1:'
_CONV = r'%[-+#0]*[0-9]*(?:\.[0-9]+)?[diouxXeEfFgGcsq]'
PLACEHOLDER_RE = re.compile(rf'(?:{_CONV}%%)|(?:{_CONV})|%%')


class SourceFactsError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise SourceFactsError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    def constant(value):
        raise SourceFactsError(f'invalid JSON constant: {value}')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)


def public_path(value):
    if (not isinstance(value, str) or not value or '\\' in value or '\x00' in value
            or ':' in value or value.startswith('/')
            or any(p in ('', '.', '..') for p in value.split('/'))):
        raise SourceFactsError(f'noncanonical public path: {value!r}')
    return value


def ordinary_bytes(path):
    """Reject symlinks in every component, before opening an ordinary file."""
    path = Path(path).absolute()
    for parent in reversed((path, *path.parents)):
        mode = parent.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise SourceFactsError(f'symlink source/input: {parent}')
        if parent != path and not stat.S_ISDIR(mode):
            raise SourceFactsError(f'non-directory source parent: {parent}')
    if not stat.S_ISREG(path.lstat().st_mode):
        raise SourceFactsError(f'non-ordinary source/input: {path}')
    return path.read_bytes()


def git(root, *args):
    proc = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if proc.returncode:
        raise SourceFactsError(f'git object unavailable: {args!r}: {proc.stderr.decode(errors="replace").strip()}')
    return proc.stdout


class FixedReader:
    """One build's cache: tree listings once per repository/commit, blobs once."""
    def __init__(self):
        self.trees = {}
        self.blobs = {}
        self.files = {}

    def tree(self, root, commit):
        if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit):
            raise SourceFactsError('source commit must be a full lowercase Git OID')
        key = (str(root), commit)
        if key not in self.trees:
            git(root, 'cat-file', '-e', commit + '^{commit}')
            values = {}
            for record in git(root, 'ls-tree', '-rz', commit).split(b'\0'):
                if not record:
                    continue
                metadata, name = record.split(b'\t', 1)
                mode, kind, oid = metadata.decode('ascii').split()
                values[name.decode('utf-8')] = (mode, kind, oid)
            self.trees[key] = values
        return self.trees[key]

    def pinned(self, root, commit, path):
        public_path(path)
        item = self.tree(root, commit).get(path)
        if item is None or item[0] not in ('100644', '100755') or item[1] != 'blob':
            raise SourceFactsError(f'fixed tree lacks ordinary blob: {commit}:{path}')
        oid = item[2]
        key = (str(root), oid)
        if key not in self.blobs:
            self.blobs[key] = git(root, 'cat-file', 'blob', oid)
        return self.blobs[key], oid

    def unpinned(self, root, path):
        public_path(path)
        key = (str(root), path)
        if key not in self.files:
            self.files[key] = ordinary_bytes(Path(root) / path)
        return self.files[key]


def load_config(root):
    # Delayed import: no queue, checkpoint, or production projection is loaded.
    from dataclasses import replace
    from i18nlib.config import load_manifest
    return replace(load_manifest(manifest_path=Path(root) / 'i18n/versions/tome-1.7.6.json'), root=Path(root))


def source_location(manifest, row):
    """Longest manifest mount wins; catalog component is a separate identity."""
    section = row['section']
    matches = []
    for component in manifest.components:
        if section == '.always_merge' and component.id == 'engine':
            return component, component.official_locale
        if (component.id == 'engine' and row['normalized_path'] == component.translation
                and section.startswith('engine/')):
            # freeze_workset's engine.lua sections are relative to the engine
            # root, including engine/, modules/boot/ and data/ below that root.
            mount = next(m for m in component.sources if m.mount == 'engine')
            path = Path(mount.git_path).parent.as_posix() + section[len('engine'):]
            return component, public_path(path)
        for mount in component.sources:
            if section.startswith(mount.mount + '/'):
                matches.append((len(mount.mount), component,
                                mount.git_path + section[len(mount.mount):]))
        source = component.protected_source
        if source and section.startswith(source.mount + '/'):
            matches.append((len(source.mount), component, section))
    if not matches:
        raise SourceFactsError(f'no manifest source mount for section: {section}')
    longest = max(m[0] for m in matches)
    matches = [m for m in matches if m[0] == longest]
    if len(matches) != 1:
        raise SourceFactsError(f'ambiguous manifest section: {section}')
    return matches[0][1], public_path(matches[0][2])


def component_root(manifest, component):
    source = component.protected_source
    explicit = os.environ.get(source.path_env)
    if explicit:
        root = Path(explicit).expanduser()
        if not root.is_absolute():
            raise SourceFactsError(f'{source.path_env} must be absolute')
        return root
    parent = manifest.protected_source_roots[source.root].path(manifest)
    candidates = [parent / name for name in source.directory_candidates
                  if (parent / name).exists() or (parent / name).is_symlink()]
    if len(candidates) != 1:
        raise SourceFactsError(f'{component.id}: need one explicit public component root; found {len(candidates)}')
    return candidates[0]


def terminology_rows(root, base_commit, expected, reader):
    from i18nlib.production_review import production_hash
    tree = reader.tree(root, base_commit)
    paths = [p for p, item in tree.items() if item[0] in ('100644', '100755')
             and (p == 'TERMINOLOGY.md' or p.startswith('terminology/'))]
    paths.sort(key=lambda p: (p != 'TERMINOLOGY.md', Path(p).parts))
    files = [(p, reader.pinned(root, base_commit, p)[0]) for p in paths]

    def digest(values):
        framed = bytearray()
        for name, body in values:
            name = name.encode('utf-8')
            framed += len(name).to_bytes(8, 'big') + name + len(body).to_bytes(8, 'big') + body
        return production_hash('terminology-snapshot', bytes(framed))

    if digest(files) not in expected or len(expected) != 1:
        # Current files may replace an unavailable/mismatched base snapshot only
        # when their complete production-framed digest is exactly the row digest.
        paths = [Path(root) / 'TERMINOLOGY.md'] + sorted((Path(root) / 'terminology').rglob('*'))
        files = [(p.relative_to(root).as_posix(), ordinary_bytes(p)) for p in paths
                 if p.is_file() and not p.is_symlink()]
        if len(expected) != 1 or digest(files) not in expected:
            raise SourceFactsError('terminology snapshot differs from frozen row/base')
    rows = []
    fields = ('source', 'target', 'category', 'domain', 'source_tag', 'status', 'scope', 'notes')
    for name, raw in files:
        if not name.endswith('.tsv'):
            continue
        lines = raw.decode('utf-8').splitlines()
        if not lines:
            raise SourceFactsError(f'empty terminology TSV: {name}')
        header = lines[0].split('\t')
        if len(set(header)) != len(header) or not set(fields).issubset(header):
            raise SourceFactsError(f'invalid terminology header: {name}')
        for number, line in enumerate(lines[1:], 2):
            if not line.strip():
                continue
            cells = line.split('\t')
            if len(cells) != len(header):
                raise SourceFactsError(f'invalid terminology row: {name}:{number}')
            data = dict(zip(header, cells))
            rows.append({**{key: data[key] for key in fields}, 'file': name,
                         'line': number, 'file_sha256': sha(raw)})
    return rows


def validate_workset(raw, checkpoint):
    ws = strict_json(raw)
    if not isinstance(ws, dict):
        raise SourceFactsError('source workset must be an object')
    for key in ('batch_id', 'catalog_id', 'base_commit'):
        if type(ws.get(key)) is not str or ws[key] != checkpoint[key]:
            raise SourceFactsError(f'workset {key} mismatch')
    if 'schema_version' in ws and (type(ws['schema_version']) is not int or ws['schema_version'] != 1):
        raise SourceFactsError('invalid workset schema_version')
    selected = checkpoint['selected']
    if 'entry_count' in ws and (type(ws['entry_count']) is not int or ws['entry_count'] != len(selected)):
        raise SourceFactsError('invalid workset entry_count')
    maps = []
    for key in ('entries', 'source_verification'):
        values = ws.get(key)
        if not isinstance(values, list):
            raise SourceFactsError(f'workset {key} must be an array')
        by_revision = {}
        for value in values:
            if not isinstance(value, dict) or not isinstance(value.get('entry_revision_identity'), str):
                raise SourceFactsError(f'invalid {key} entry')
            rev = value['entry_revision_identity']
            if rev in by_revision:
                raise SourceFactsError(f'duplicate {key} revision: {rev}')
            by_revision[rev] = value
        if set(by_revision) != set(selected):
            raise SourceFactsError(f'{key} does not exactly cover selected')
        maps.append(by_revision)
    entries, verifications = maps
    for row in checkpoint['entry_snapshots']:
        rev = row['entry_revision_identity']
        # Canonical bytes distinguish JSON true/1, null/empty string and extras.
        if canonical(entries[rev]) != canonical(row):
            raise SourceFactsError(f'{rev}: frozen entry/row_sha256 mismatch')
        ver = verifications[rev]
        digest = ver.get('source_file_sha256')
        hits = ver.get('matching_literal_lines')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise SourceFactsError(f'{rev}: invalid source_file_sha256')
        if 'matching_literal_lines' not in ver or (hits is not None and (not isinstance(hits, list) or
                any(type(n) is not int or n < 1 for n in hits) or len(hits) != len(set(hits)))):
            raise SourceFactsError(f'{rev}: invalid matching_literal_lines')
        for key in ('source', 'section', 'source_tag'):
            if key not in ver or canonical(ver[key]) != canonical(row[key]):
                raise SourceFactsError(f'{rev}: verification {key} mismatch')
        if 'args_order' not in ver or canonical(ver['args_order']) != canonical(row.get('risk', {}).get('args_order')):
            raise SourceFactsError(f'{rev}: verification args_order mismatch')
    return ws, verifications


def order_ok(src_specs, tgt_specs, args_order):
    if args_order is None:
        return src_specs == tgt_specs
    if (not isinstance(args_order, list) or any(type(i) is not int for i in args_order)
            or len(args_order) != len(tgt_specs)
            or sorted(args_order) != list(range(1, len(src_specs) + 1))):
        return False
    return [src_specs[i - 1] for i in args_order] == tgt_specs


class FactBuilder:
    def __init__(self, root, manifest, reader, terms, context=3):
        if type(context) is not int or not 0 <= context <= 3:
            raise SourceFactsError('context must be between 0 and 3')
        self.root, self.manifest, self.reader = Path(root), manifest, reader
        self.terms, self.context = terms, context
        self.roots = {}

    def read(self, component, path, expected=None, *, extractor=False):
        public_path(path)
        manifest = self.manifest
        if extractor:
            repository = manifest.extractor.repository
            commit = manifest.extractor.commit
            if not path.startswith(manifest.extractor.git_path + '/'):
                raise SourceFactsError('extractor path outside manifest mount')
        elif component.source_repository:
            repository = component.source_repository
            commit = manifest.repositories[repository].commit
        else:
            repository, commit = None, None
        if repository:
            if manifest.repositories[repository].visibility != 'public':
                raise SourceFactsError('repository is not configured public input')
            raw, blob = self.reader.pinned(manifest.repository_path(repository), commit, path)
            provenance = dict(repository=repository, source_pinning='pinned', commit=commit, blob_oid=blob)
        else:
            source = component.protected_source
            if source is None or source.visibility != 'public':
                raise SourceFactsError('source is not configured public input')
            if not path.startswith(source.mount + '/'):
                # Older sibling attribution records use component-dir/mount/path.
                prefix, _, rest = path.partition('/')
                if prefix not in source.directory_candidates or not rest.startswith(source.mount + '/'):
                    raise SourceFactsError('auxiliary path outside source component mount')
                path = rest
            if component.id not in self.roots:
                self.roots[component.id] = component_root(manifest, component)
            raw = self.reader.unpinned(self.roots[component.id], path)
            provenance = dict(repository=None, source_pinning='unpinned', commit=None, blob_oid=None,
                              disclosure='Public source repository/version not pinned; extraction snapshot is not a source commit.',
                              independent_version_basis=False)
        digest = sha(raw)
        if expected is not None and (not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected) or expected != digest):
            raise SourceFactsError(f'source SHA mismatch: {path}')
        text = raw.decode('utf-8').replace('\r\n', '\n')
        return dict(provenance, source_component='extractor' if extractor else component.id,
                    public_source_path=path, source_file_sha256=digest), text.split('\n')

    def fact(self, row, ver):
        from i18nlib.workset import _scope_matches, _source_tag_matches
        rev = row['entry_revision_identity']
        component, path = source_location(self.manifest, row)
        pin = 'pinned' if component.source_repository else 'unpinned'
        commit = self.manifest.repositories[component.source_repository].commit if component.source_repository else None
        for key, value in [('component', component.id), ('public_source_path', path),
                           ('source_pinning', pin), ('fixed_source_commit', commit)]:
            if key not in ver or canonical(ver[key]) != canonical(value):
                raise SourceFactsError(f'{rev}: verification {key} contradicts manifest/section')
        if ver.get('source_commit') is not None and pin == 'unpinned':
            raise SourceFactsError(f'{rev}: unpinned source cannot declare a commit')
        if not isinstance(ver.get('source_file_sha256'), str):
            raise SourceFactsError(f'{rev}: missing main source SHA')
        main, main_lines = self.read(component, path, ver['source_file_sha256'])
        anchors = []

        def anchor(kind, numbers, public=path, digest=None, *, owner=component, extractor=False, tokens=()):
            if not isinstance(numbers, list) or not numbers or any(type(n) is not int for n in numbers) or len(numbers) != len(set(numbers)):
                raise SourceFactsError(f'{rev}: invalid {kind} line numbers')
            if len(numbers) > MAX_LINES or len(anchors) >= MAX_ANCHORS:
                raise SourceFactsError(f'{rev}: source facts exceed {MAX_ANCHORS} anchors/{MAX_LINES} lines')
            provenance, lines = self.read(owner, public, digest, extractor=extractor)
            if any(n < 1 or n > len(lines) for n in numbers):
                raise SourceFactsError(f'{rev}: {kind} line outside {public}')
            matched = '\n'.join(lines[n - 1] for n in sorted(numbers))
            for token in tokens:
                if not isinstance(token, str) or not token or token not in matched:
                    raise SourceFactsError(f'{rev}: {kind} declared key/token not at lines')
            display = sorted({i for n in numbers for i in range(max(1, n-self.context), min(len(lines), n+self.context)+1)})
            anchors.append(dict(provenance, kind=kind, matching_lines=numbers,
                                snippet=[dict(line=i, text=lines[i-1], is_match=i in numbers) for i in display]))

        hits = ver.get('matching_literal_lines')
        if hits is not None and not isinstance(hits, list):
            raise SourceFactsError(f'{rev}: matching_literal_lines must be array or null')
        if hits:
            variants = [row['source'], row['source'].replace('\n', '\\n').replace('\t', '\\t'),
                        row['source'].replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')]
            if any(type(n) is not int or n < 1 or n > len(main_lines) for n in hits):
                raise SourceFactsError(f'{rev}: literal line outside source')
            matched = '\n'.join(main_lines[n-1] for n in hits)
            if not any(v in matched for v in variants):
                raise SourceFactsError(f'{rev}: literal not at declared lines')
            anchor('literal', hits, digest=ver['source_file_sha256'])
        for kind in ('interface_mixin', 'host_generated_key', 'dynamic_tag_sibling_key',
                     'concatenated_entity_name', 'lowercased_entity_name',
                     'always_merge_locale', 'legacy_locale_entry'):
            key = kind + '_verification'
            if key not in ver:
                continue
            data = ver[key]
            if not isinstance(data, dict):
                raise SourceFactsError(f'{rev}: {key} must be object')
            for field, value in data.items():
                if field.endswith('_sha256') and (not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value)):
                    raise SourceFactsError(f'{rev}: invalid declared auxiliary SHA: {field}')
            if kind == 'interface_mixin':
                anchor(kind + ':require', data['including_file_require_lines'], tokens=('require', data['require_package']))
                anchor(kind + ':literal', data['literal_lines'], data['literal_public_source_path'],
                       data.get('literal_file_sha256'), tokens=(row['source'].replace('\n', '\\n'),))
            elif kind == 'host_generated_key':
                if data['extractor_commit'] != self.manifest.extractor.commit:
                    raise SourceFactsError('extractor commit mismatch')
                anchor(kind + ':data', data['source_lines'], tokens=(data['source_key'],))
                anchor(kind + ':extractor', data['extractor_lines'], data['extractor_path'], data.get('extractor_sha256'), extractor=True)
            elif kind == 'dynamic_tag_sibling_key':
                anchor(kind + ':call', data['dynamic_call_lines'], tokens=('_t(', row['source_tag']))
                anchor(kind + ':key', data['key_lines'], data['key_public_source_path'], data.get('key_file_sha256'), tokens=(data['source_key'],))
            elif kind == 'concatenated_entity_name':
                anchor(kind + ':concat', data['concat_lines'], tokens=('..', data['literal_prefix']))
                anchor(kind + ':argument', data['argument_lines'])
                if not isinstance(data['resolved_argument'], str) or not data['resolved_argument'] or not any(
                        data['resolved_argument'].lower() in main_lines[n-1].lower() for n in data['argument_lines']):
                    raise SourceFactsError('concatenation argument missing')
            elif kind == 'lowercased_entity_name':
                anchor(kind + ':lower', data['lower_lines'], tokens=('name:lower()',))
                anchor(kind + ':argument', data['argument_lines'])
                if not isinstance(data['resolved_argument'], str) or not data['resolved_argument'] or not any(
                        data['resolved_argument'].lower() in main_lines[n-1].lower() for n in data['argument_lines']):
                    raise SourceFactsError('lowercased argument missing')
            else:
                owner = next(c for c in self.manifest.components if c.id == 'engine')
                locale = data['locale_public_source_path']
                locale_section = (data.get('locale_section', row['section'])
                                  if kind == 'always_merge_locale' else data['locale_section'])
                if (locale != owner.official_locale or locale_section != row['section']
                        or (kind == 'always_merge_locale' and row['section'] != '.always_merge')):
                    raise SourceFactsError('locale attribution differs from section/manifest')
                provenance, lines = self.read(owner, locale, data.get('locale_sha256'))
                numbers = data['source_lines']
                if not isinstance(numbers, list) or not numbers or any(type(n) is not int or n < 1 or n > len(lines) for n in numbers):
                    raise SourceFactsError('invalid locale definition lines')
                sections = [i for i in range(1, min(numbers)+1) if lines[i-1].startswith('section ')]
                expected_section = 'section ' + json.dumps(row['section'], ensure_ascii=False)
                if not sections or lines[sections[-1]-1].strip() != expected_section:
                    raise SourceFactsError('locale section not found before definition')
                anchor(kind + ':section', [sections[-1]], locale, owner=owner)
                anchor(kind + ':definition', numbers, locale, data.get('locale_sha256'), owner=owner, tokens=(row['source'],))
                if kind == 'legacy_locale_entry':
                    marker = data['locale_marker_line']
                    if type(marker) is not int or not sections[-1] < marker < min(numbers):
                        raise SourceFactsError('legacy marker outside section/definition')
                    anchor(kind + ':marker', [marker], locale, owner=owner, tokens=('-- old translated text',))
        placeholders = [dict(spec=m.group(), offset=m.start(), literal_percent=m.group() == '%%', quantity_kind='unknown')
                        for m in PLACEHOLDER_RE.finditer(row['source'])]
        src_specs = [p['spec'] for p in placeholders if not p['literal_percent']]
        tgt_specs = [m.group() for m in PLACEHOLDER_RE.finditer(row['target']) if m.group() != '%%']
        terms = [t for t in self.terms if t['source'] and _scope_matches(t['scope'], row['component'])
                 and _source_tag_matches(t['source_tag'], row['source_tag'])
                 and re.search(r'(?<!\w)' + re.escape(t['source']) + r'(?!\w)', row['source'])]
        result = dict(entry_revision_identity=rev, catalog_component=row['component'], source_component=component.id,
                      main_source=main, anchors=anchors, evidence_status='available' if anchors else 'pending',
                      missing_evidence=None if anchors else 'No literal or supported attribution anchors declared.',
                      placeholders=placeholders, placeholders_in_target=tgt_specs,
                      args_order=ver['args_order'], placeholder_order_matches=order_ok(src_specs, tgt_specs, ver['args_order']),
                      terminology=terms)
        if len(anchors) > MAX_ANCHORS or sum(len(a['snippet']) for a in anchors) > MAX_LINES or len(canonical(result)) > MAX_FACT_BYTES:
            raise SourceFactsError(f'{rev}: source facts exceed {MAX_ANCHORS} anchors/{MAX_LINES} lines/{MAX_FACT_BYTES} bytes')
        return result


def build_source_facts(root, workset_raw, checkpoint, runs, *, manifest=None, context=3):
    """Validate all selected bindings; build only deep run facts, with no writes."""
    ws, verifications = validate_workset(workset_raw, checkpoint)
    manifest = manifest if manifest is not None else load_config(root)
    from i18nlib.production_review import source_identities_from_manifest
    identities = source_identities_from_manifest(manifest)
    for row in checkpoint['entry_snapshots']:
        if identities.get(row['component']) != row['fixed_source_identity']:
            raise SourceFactsError(f'{row["entry_revision_identity"]}: catalog fixed source identity differs from manifest')
        # Non-deep entries receive binding checks only; their sources are not read.
        component, path = source_location(manifest, row)
        ver = verifications[row['entry_revision_identity']]
        commit = manifest.repositories[component.source_repository].commit if component.source_repository else None
        expected = dict(component=component.id, public_source_path=path,
                        source_pinning='pinned' if commit else 'unpinned', fixed_source_commit=commit)
        if any(k not in ver or canonical(ver[k]) != canonical(v) for k, v in expected.items()):
            raise SourceFactsError('verification source binding differs from manifest/section')
    reader = FixedReader()
    terms = terminology_rows(Path(root), ws['base_commit'],
                             {r['terminology_snapshot_sha256'] for r in checkpoint['entry_snapshots']}, reader)
    builder = FactBuilder(root, manifest, reader, terms, context)
    result = []
    for run in runs:
        facts = [builder.fact(row, verifications[row['entry_revision_identity']]) for row in run['entries']]
        package = dict(kind='review_source_facts_v1', batch_id=ws['batch_id'], catalog_id=ws['catalog_id'],
                       base_commit=ws['base_commit'], source_workset_sha256=sha(workset_raw),
                       manifest_sha256=sha(manifest.raw_bytes),
                       ordered_revisions=[r['entry_revision_identity'] for r in run['entries']], entries=facts)
        if len(canonical(package)) > MAX_RUN_BYTES:
            raise SourceFactsError(f'run {run["run_index"]}: facts exceed {MAX_RUN_BYTES} bytes')
        result.append(package)
    return result


def bound_context(package, fact):
    binding = {key: value for key, value in package.items() if key != 'entries'}
    value = dict(binding=binding, package_sha256=sha(canonical(package)), fact=fact)
    return CONTEXT_MARKER + canonical(value).decode('utf-8').replace('=', '\\u003d')


def main(argv=None):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('batch')
    ap.add_argument('--context', type=int, default=3)
    ap.add_argument('--siblings', type=int, default=4, help='compatibility only; no library scan')
    args = ap.parse_args(argv)
    root = Path(os.environ.get('TOME_TRANSLATION_ROOT', Path(__file__).resolve().parents[2]))
    prefix = root / 'evidence/quality/production-batches'
    raw = ordinary_bytes(prefix / f'{args.batch}-source-workset.json')
    ws = strict_json(raw)
    checkpoint = dict(ws, selected=[r['entry_revision_identity'] for r in ws['entries']], entry_snapshots=ws['entries'])
    # The standalone legacy command validates against its frozen workset; export
    # additionally binds that workset to the locked, preflighted checkpoint.
    packages = build_source_facts(root, raw, checkpoint, [dict(run_index=0, entries=ws['entries'])], context=args.context)
    body = canonical(packages[0]) + b'\n'
    dest = prefix / f'{args.batch}-evidence-pack.json'
    if (dest.exists() or dest.is_symlink()) and ordinary_bytes(dest) != body:
        raise SourceFactsError('existing evidence pack differs; use a new freeze/recovery boundary')
    temp = dest.with_suffix('.json.tmp')
    # Exclusive creation refuses every pre-existing temp, including dangling
    # symlinks and special files, before any frozen input can be overwritten.
    stream = temp.open('xb')
    try:
        with stream:
            stream.write(body)
        temp.replace(dest)
    finally:
        temp.unlink(missing_ok=True)
    print(f'{dest.name}: {len(ws["entries"])} entries sha256={sha(body)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
