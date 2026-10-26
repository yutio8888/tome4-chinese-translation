"""Offline full-round adapter. No provider calls or writes to existing queues.

Frozen exports and imports are append-only evidence; progress is replayed from
bytes, current occurrence guards and the existing task terminal predicate.
"""
from __future__ import annotations

from bisect import bisect_left
from collections import Counter, OrderedDict
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import contextual_result_check as contextual
import contextual_anchor_preflight as anchors
import surface_screen_result_check as identity
from orchestration.build_evidence_pack import FixedReader
from orchestration.review_prompts import build_contextual_prompt
from . import full_review_cache
from . import gate_results
from . import production_review as wp1
from . import production_review_v2_lite as catalog
from . import production_review_v2_lite_batch as batch
from .config import load_manifest
from .locale_model import LocaleLoader
from .runtime import LuaRuntime

RELEASE = frozenset({'engine', 'tome', 'ashes-urhrok', 'cults', 'orcs'})
B_REASONS = frozenset({'mechanics', 'long-text', 'A-observation'})


class FullReviewError(ValueError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


_parse_cache = ContextVar('full_review_parses', default=None)
_PARSE_BYTES = 64 * 1024 * 1024
_PARSE_ENTRIES = 4096


@contextmanager
def _parse_scope():
    if _parse_cache.get() is not None:
        yield
        return
    token = _parse_cache.set([OrderedDict(), 0])
    try:
        yield
    finally:
        _parse_cache.reset(token)


def _parsed(key, decode):
    state = _parse_cache.get()
    if state is None:
        return decode()
    entries = state[0]
    if key in entries:
        value = entries.pop(key)
        entries[key] = value
        return value
    value = decode()  # Never retain failed parses/validations.
    size = sum(len(item) for item in key[1:])
    if size <= _PARSE_BYTES:
        while entries and (state[1] + size > _PARSE_BYTES or len(entries) >= _PARSE_ENTRIES):
            old, _ = entries.popitem(last=False)
            state[1] -= sum(len(item) for item in old[1:])
        entries[key] = value
        state[1] += size
    return value


@full_review_cache.timed('json-parsing')
def _json_bytes(raw, *, label, whitespace=False):
    stripped = raw.strip() if whitespace else raw
    mode = 'json-whitespace' if stripped != raw else 'json'
    return _parsed((mode, raw), lambda: contextual.strict_json_bytes(stripped, label=label))


@full_review_cache.timed('import-result-parsing')
def _result_bytes(envelope, raw):
    return _parsed(('result', envelope, raw), lambda: contextual.validate_result_bytes(envelope, raw))


@full_review_cache.timed('file-reads')
def ordinary(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise FullReviewError(f'not an ordinary file: {path}')
    return full_review_cache.read_bytes(path)


def read(path):
    # Strict duplicate-key/NaN handling, with ordinary JSON file whitespace.
    return _json_bytes(ordinary(path), label=str(path), whitespace=True)


class _InventorySnapshot:
    """One check's parse, bound to the exact ordinary bytes it decoded.

    Only inventory data is retained; export discovery and every replay validator
    still run. A predecessor snapshot is moved into its recursive consumer, never
    shared with the parent mapping view or retained in an invocation-wide cache.
    """
    @full_review_cache.timed('inventory-parsing')
    def __init__(self, directory):
        self.path = Path(directory).absolute() / 'inventory.json'
        raw = ordinary(self.path)
        self.digest = sha(raw)
        self.ledger = contextual.strict_json_bytes(raw.strip(), label=str(self.path))

    def verify(self, directory):
        if Path(directory).absolute() / 'inventory.json' != self.path:
            raise FullReviewError('inventory snapshot path mismatch')
        # Read even on reuse: stat metadata and rewritten refs cannot authorize
        # a different inventory halfway through a verification invocation.
        if sha(ordinary(self.path)) != self.digest:
            raise FullReviewError('inventory snapshot bytes drift')

    @full_review_cache.timed('inventory-parsing')
    def reload(self, directory):
        # Restore a released parse. The digest binds these to the exact bytes the
        # strict decoder already accepted in this invocation, so the plain decoder
        # yields the identical value without repeating the duplicate-key hook.
        if Path(directory).absolute() / 'inventory.json' != self.path:
            raise FullReviewError('inventory snapshot path mismatch')
        raw = ordinary(self.path)
        if sha(raw) != self.digest:
            raise FullReviewError('inventory snapshot bytes drift')
        self.ledger = json.loads(raw.strip())


def safe_path(root, relative):
    normalized = identity.normalize_relative_path(relative)
    if normalized != relative:
        raise FullReviewError('noncanonical relative path')
    path = Path(root).absolute() / relative
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise FullReviewError('symlink path rejected')
    return path


def immutable(path, raw):
    """Idempotent byte-exact creation, including crash recovery before index write."""
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise FullReviewError('symlink evidence path')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if ordinary(path) != raw:
            raise FullReviewError(f'conflicting frozen bytes: {path}')
        return
    fd, name = tempfile.mkstemp(prefix='.full-review-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # link is no-clobber, unlike replace: concurrent conflicting writers fail.
        try:
            os.link(name, path)
        except FileExistsError:
            if ordinary(path) != raw:
                raise FullReviewError('concurrent evidence conflict')
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        os.unlink(name)


@contextmanager
def round_lock(directory):
    directory = Path(directory).absolute()
    if any(p.is_symlink() for p in (directory, *directory.parents)):
        raise FullReviewError('symlink round')
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / '.adapter.lock'
    if lock.is_symlink():
        raise FullReviewError('symlink lock')
    with lock.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def token(value):
    if not isinstance(value, str) or not re.fullmatch('[a-z0-9][a-z0-9-]{0,79}', value):
        raise FullReviewError('expected bounded path-safe token')
    return value


def current_units(manifest):
    occurrences = wp1.load_occurrences(manifest)
    terms = wp1.terminology_snapshot(manifest.root)
    sources = wp1.source_identities_from_manifest(manifest)
    formal, _ = catalog.formal_rows(occurrences, terminology=terms, sources=sources)
    by_locator = {r['call_locator']: r for r in formal}
    units = []
    call_lines = {}
    for component in manifest.components:
        text = ordinary(manifest.root / component.translation).decode('utf-8')
        _, calls = anchors._scan_lua(text)
        newlines = [index for index, char in enumerate(text) if char == '\n']
        call_lines[component.id] = [bisect_left(newlines, call.start) + 1 for call in calls]
    for row in occurrences:
        locator = catalog._plain_id(catalog.CALL_LOCATOR_KIND, 'locator', wp1.make_allocation(row))
        logical = identity.logical_entry_identity(component=row['component'],
            normalized_path=row['translation_path'], call_locator=locator, source_tag=row['source_tag'] or '')
        fixed = sources.get(row['component'])
        revision = None if fixed is None else identity.entry_revision_identity(
            logical_entry_identity=logical, source=row['source'], target=row['target'],
            fixed_source_identity=fixed, terminology_snapshot=terms,
            rules_version=catalog.RULES_VERSION, args_order=row['args_order'])
        disposition = ('release-required' if row['component'] in RELEASE else
                       'boot-inheritance-loading' if row['component'] == 'boot' else 'outside-release-followup')
        # special is intentionally outside the unchanged rules-v2 recipe.
        guard = sha(canonical({'occurrence': {k: v for k, v in row.items()
            if k not in {'document_ordinal', 'line', 'position'}}, 'fixed_source_identity': fixed}))
        units.append({'unit_id': logical, 'revision_key': revision, 'guard': guard,
            'occurrence': row, 'call_locator': locator, 'disposition': disposition,
            'fixed_source_identity': fixed, 'catalog_row': by_locator.get(locator),
            'runtime_key': [row['source'], row['source_tag']], 'runtime_chain': None,
            'line': call_lines[row['component']][row['document_ordinal']] if row['document_ordinal'] < len(call_lines[row['component']]) else None})
    if len({u['unit_id'] for u in units}) != len(units):
        raise FullReviewError('occurrence locator collision')
    return units, terms


def inventory(manifest, round_id, output, snapshot_reports, source_provenance=None):
    token(round_id)
    units, terms = current_units(manifest)
    if len(units) != 30308 or len({u['occurrence']['component'] for u in units}) != 11:
        raise FullReviewError('canonical 11-component/30308 vector drift')
    loader = LocaleLoader(LuaRuntime(manifest))
    supplements, inputs = [], []
    for report_path in snapshot_reports:
        report = read(report_path)
        for item in report['components']:
            raw = ordinary(item['snapshot'])
            if sha(raw) != item['snapshot_sha256']:
                raise FullReviewError('fixed extraction snapshot drift')
            records = [json.loads(line) for line in raw.splitlines() if line]
            if len(records) != item['tdef_count']:
                raise FullReviewError('snapshot count mismatch')
            component = item['component']
            expected = manifest.component(component)
            if expected.source_baseline and (sha(raw) != expected.source_baseline.snapshot_sha256 or
                    len(records) != expected.source_baseline.tdef_count):
                raise FullReviewError('DLC baseline mismatch')
            if expected.source_repository and item.get('source_commit') != manifest.repositories[expected.source_repository].commit:
                raise FullReviewError('fixed source commit mismatch')
            inputs.append({'kind': 'extract-snapshot', 'component': component, 'sha256': sha(raw),
                           'count': len(records), 'report_sha256': sha(ordinary(report_path))})
            keys = {tuple(u['runtime_key']) for u in units if u['occurrence']['component'] == component}
            for index, record in enumerate(records):
                # Every source-visible occurrence remains represented, even with a translation.
                supplements.append({'supplement_id': sha(canonical([component, 'source', index, record])),
                    'kind': 'source-visible', 'component': component, 'record': record,
                    'canonical_key_present': (record.get('source'), record.get('source_tag')) in keys,
                    'runtime_chain': None, 'status': 'pending-source-runtime-mapping'})
    required = {'engine': 904, 'boot': 319, 'tome': 25543, 'ashes-urhrok': 999, 'cults': 2444, 'orcs': 4493}
    if Counter({i['component']: i['count'] for i in inputs}) != Counter(required) or len(inputs) != 6:
        raise FullReviewError('all six previously verified snapshots required exactly once')
    for component in manifest.components:
        if component.copy_fragment:
            raw = ordinary(manifest.root / component.copy_fragment)
            supplements.append({'supplement_id': sha(canonical(['copy', component.id, sha(raw)])),
                'kind': 'copy', 'component': component.id, 'path': component.copy_fragment,
                'sha256': sha(raw), 'content': raw.decode('utf-8'), 'runtime_chain': None,
                'status': 'pending-copy-language-and-flags'})
        if component.official_locale:
            repository = manifest.repository_path(component.source_repository or 'engine')
            commit = manifest.repositories[component.source_repository or 'engine'].commit
            raw, _ = FixedReader().pinned(repository, commit, component.official_locale)
            document = loader.load_bytes(raw, logical_path=component.official_locale)
            for index, record in enumerate(document.translations):
                supplements.append({'supplement_id': sha(canonical(['official', component.id, index, record])),
                    'kind': 'official-inheritance', 'component': component.id, 'record': record,
                    'public_source_path': component.official_locale, 'commit': commit, 'sha256': sha(raw),
                    'runtime_chain': None, 'status': 'pending-inheritance-filter-dedup'})
    # Every retained release-tree file is an explicit pending layer, including
    # procedural/non-t() text. Host closure must classify it with evidence.
    release_reader = FixedReader()
    release_root = manifest.repository_path('addon')
    release_commit = manifest.repositories['addon'].commit
    for path, (mode, kind, _) in sorted(release_reader.tree(release_root, release_commit).items()):
        if mode not in ('100644', '100755') or kind != 'blob':
            raise FullReviewError('retained release input contains nonordinary entry')
        raw, _ = release_reader.pinned(release_root, release_commit, path)
        supplements.append({'supplement_id': sha(canonical(['retained-layer', release_commit, path, sha(raw)])),
            'kind': 'retained-layer', 'component': 'release-addon', 'path': path, 'sha256': sha(raw),
            'commit': release_commit, 'runtime_chain': None, 'status': 'pending-retained-layer-classification'})
    # Wrapper boot addons are separate source inputs. Do not assume an inner
    # extraction directory is its own logical-mount parent.
    if source_provenance is None:
        for component in sorted(RELEASE - {'engine', 'tome'}):
            supplements.append({'supplement_id': sha(canonical(['wrapper-enumeration', component])),
                'kind': 'wrapper-enumeration-obligation', 'component': component,
                'status': 'pending-explicit-public-wrapper-provenance', 'runtime_chain': None})
    else:
        provenance = read(source_provenance)
        if provenance.get('engine_commit') != manifest.repositories['engine'].commit:
            raise FullReviewError('source provenance fixed commit mismatch')
        inputs.append({'kind': 'public-source-provenance', 'sha256': sha(ordinary(source_provenance))})
        for dlc in provenance['dlcs']:
            component = dlc['component']
            mount = manifest.component(component).protected_source.mount
            for item in dlc['files']:
                path = identity.normalize_relative_path(item['path'])
                # Historical wrapper freezes nest the main addon under its mount.
                if path.startswith(mount + '/' + mount + '/'):
                    continue
                supplements.append({'supplement_id': sha(canonical(['wrapper', component, path, item['sha256']])),
                    'kind': 'wrapper-addon', 'component': component, 'path': path,
                    'sha256': item['sha256'], 'source_pinning': 'unpinned',
                    'runtime_chain': None, 'status': 'pending-wrapper-use'})
    value = {'schema_version': 1, 'round_id': round_id, 'manifest_sha256': sha(manifest.raw_bytes),
        'rules_version': catalog.RULES_VERSION, 'terminology_snapshot': terms, 'units': units,
        'supplements': supplements, 'inputs': inputs, 'canonical_occurrences': len(units),
        'component_counts': dict(Counter(u['occurrence']['component'] for u in units)),
        'final_unit_denominator': None, 'final_runtime_denominator': None,
        'retained_layer_status': 'pending-explicit-release-tree-selection',
        'dynamic_context_status': 'pending-host-enumeration', 'A': 0, 'B': 0}
    value['inventory_identity'] = sha(canonical(value))
    with round_lock(output):
        immutable(Path(output) / 'inventory.json', canonical(value))
    return {'round_id': round_id, 'canonical_occurrences': len(units), 'supplements': len(supplements),
            'A': 0, 'B': 0, 'denominator_frozen': False}


@full_review_cache.timed('current-inventory-validation')
def validate_current(manifest, ledger):
    body = {k: v for k, v in ledger.items() if k != 'inventory_identity'}
    if ledger.get('inventory_identity') != sha(canonical(body)):
        raise FullReviewError('frozen inventory bytes drift')
    if ledger['manifest_sha256'] != sha(manifest.raw_bytes):
        raise FullReviewError('manifest drift')
    live, terms = current_units(manifest)
    live = list(live) + [supplemental_unit(manifest, u['supplement_spec'], ledger['supplements'], terms)
             for u in ledger['units'] if 'supplement_spec' in u]
    expected = {u['unit_id']: u for u in live}
    if len(ledger['units']) != len(expected) or len({u['unit_id'] for u in ledger['units']}) != len(expected):
        raise FullReviewError('occurrence conservation mismatch')
    for unit in ledger['units']:
        current = expected.get(unit['unit_id'])
        if current is None or (unit['guard'], unit['revision_key']) != (current['guard'], current['revision_key']):
            raise FullReviewError(f'current occurrence drift: {unit["unit_id"]}')
    return expected



def tree_seal(directory):
    """Freeze every completed predecessor artifact; no mutable pointer or queue."""
    return {p.relative_to(directory).as_posix(): sha(ordinary(p))
            for p in sorted(Path(directory).rglob('*')) if p.is_file() and p.name != '.adapter.lock'}


def literal_binding(manifest, binding, text):
    raw = ordinary(safe_path(manifest.root, binding['path']))
    start, end = binding['start'], binding['end']
    if (type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(raw)
            or sha(raw) != binding['sha256'] or raw[start:end] != text.encode('utf-8')):
        raise FullReviewError('actual language byte anchor drift')


def supplemental_unit(manifest, spec, supplements, terms):
    origins = spec['origins']
    known = {s['supplement_id']: s for s in supplements}
    if (not origins or len(set(origins)) != len(origins) or not set(origins) <= set(known)):
        raise FullReviewError('unknown/duplicate supplement origin')
    evidence_files(manifest, spec['evidence'])
    if len(origins) > 1 and not spec.get('merge_reason'):
        raise FullReviewError('multiple origins require explicit host merge evidence')
    row = spec['language']
    if set(row) != {'source', 'target', 'source_tag', 'args_order', 'special'}:
        raise FullReviewError('explicit actual five-field language unit required')
    if not isinstance(row['source'], str) or not row['source'] or not isinstance(row['target'], str):
        raise FullReviewError('actual source/target strings required')
    if row['source_tag'] is not None and not isinstance(row['source_tag'], str):
        raise FullReviewError('invalid actual tag')
    args = identity.validate_args_order(row['args_order'], source=row['source'], label='supplement args')
    for field in ('source', 'target'):
        literal_binding(manifest, spec['anchors'][field], row[field])
    if not spec['context'].strip() or not spec['source_files']:
        raise FullReviewError('supplement needs neutral source/context workset')
    for source in spec['source_files']:
        source_file(manifest, source)
    # Separate namespace: this is a language byte unit, never a canonical t locator.
    key = sha(canonical(['full-review-supplement-language-v1', token(spec['language_id'])]))
    fixed = 'snapshot:' + sha(canonical(spec['source_files']))
    revision = identity.entry_revision_identity(logical_entry_identity=key,
        source=row['source'], target=row['target'], fixed_source_identity=fixed,
        terminology_snapshot=terms, rules_version=catalog.RULES_VERSION, args_order=args)
    guard = sha(canonical(spec))
    adapter_row = {'entry_revision_identity': revision, 'source': row['source'], 'target': row['target'],
        'section': spec['context'], 'rules_version': catalog.RULES_VERSION,
        'risk': {'args_order': args, 'has_args_order': args is not None}}
    return {'unit_id': key, 'revision_key': revision, 'guard': guard, 'occurrence': row,
        'disposition': 'release-required', 'fixed_source_identity': fixed, 'catalog_row': adapter_row,
        'runtime_key': [row['source'], row['source_tag']], 'supplement_spec': spec,
        'supplement_origins': origins}


def preflight_units(manifest, scope_path, payload, selected):
    anchors._validate_payload(payload)
    scope = read(scope_path)
    # Keep the established scope shape and path safety, but byte-unit anchors do
    # not pretend to be Lua calls. Canonical members still use ordinary preflight.
    anchors._validate_scope(scope, manifest.root)
    canonical_indices = []
    for index, unit in enumerate(selected):
        spec = unit.get('supplement_spec')
        if spec is None:
            canonical_indices.append(index)
            continue
        for field in ('source', 'target'):
            anchor = spec['anchors'][field]
            if anchor['path'] not in scope['allowed_files']:
                raise FullReviewError('supplement byte anchor outside frozen scope')
            literal_binding(manifest, anchor, unit['occurrence'][field])
        evidence_files(manifest, spec['evidence'])
    if canonical_indices:
        subset = dict(payload)
        for field in ('ordered_revision_keys', 'translation_snapshot', 'bounded_context'):
            subset[field] = [payload[field][i] for i in canonical_indices]
        with tempfile.TemporaryDirectory(prefix='full-review-preflight-') as temp:
            path = Path(temp) / 'payload.json'
            path.write_bytes(canonical(subset))
            result = anchors.run_preflight(scope_path, path, workspace_root=manifest.root)
            if result.status != 'PREFLIGHT_VERIFIED':
                raise FullReviewError(f'anchor preflight rejected: {result}')
    return {'status': 'PREFLIGHT_VERIFIED', 'adapter': 'canonical-and-language-bytes-v1',
            'scope_sha256': sha(ordinary(scope_path)), 'payload_sha256': sha(canonical(payload)),
            'units': [{'unit_id': u['unit_id'], 'guard': u['guard'],
                       'kind': 'language-bytes' if 'supplement_spec' in u else 'canonical'} for u in selected]}


def successor(manifest, directory, output, request_path):
    """One bounded immutable migration, including explicit supplement bindings.

    The predecessor remains byte-exact. New exports/tasks belong to the successor;
    only unchanged units with exact neutral worksets can consume old coverage.
    """
    directory, output = Path(directory).absolute(), Path(output).absolute()
    if output == directory or output.is_relative_to(directory) or directory.is_relative_to(output):
        raise FullReviewError('successor must be a separate sibling version')
    request = read(request_path)
    with round_lock(directory), round_lock(output):
        old = read(directory / 'inventory.json')
        validate_inventory(manifest, old)
        if old.get('predecessor') and tree_seal(Path(old['predecessor']['directory'])) != old['predecessor']['seal']:
            raise FullReviewError('predecessor frozen evidence drift')
        if (request['round_id'] != old['round_id'] or
                request['before_sha256'] != sha(ordinary(directory / 'inventory.json'))):
            raise FullReviewError('successor before/round conflict')
        evidence_files(manifest, request['evidence'])
        units, terms = current_units(manifest)
        units = list(units)
        supplements = request['supplements']
        old_sup = {s['supplement_id']: s for s in old['supplements']}
        new_sup = {s['supplement_id']: s for s in supplements}
        if len(new_sup) != len(supplements):
            raise FullReviewError('duplicate supplement')
        language = [supplemental_unit(manifest, x, supplements, terms) for x in request['language_units']]
        anchors_seen = [sha(canonical([u['supplement_spec']['anchors'], u['occurrence']])) for u in language]
        if len(anchors_seen) != len(set(anchors_seen)):
            raise FullReviewError('duplicate actual language unit; host must merge origins explicitly')
        units += language
        before = {u['unit_id']: u for u in old['units']}
        after = {u['unit_id']: u for u in units}
        if len(after) != len(units):
            raise FullReviewError('duplicate successor unit')
        changes = request['mapping']
        if (len(changes) != len({x['unit_id'] for x in changes}) or
                {x['unit_id'] for x in changes} != set(before) | set(after)):
            raise FullReviewError('successor occurrence/unit conservation mismatch')
        for item in changes:
            key = item['unit_id']
            expected = ('added' if key not in before else 'removed' if key not in after else
                        'unchanged' if (before[key]['guard'], before[key]['revision_key']) ==
                        (after[key]['guard'], after[key]['revision_key']) else 'changed')
            if item['status'] != expected or not item.get('reason'):
                raise FullReviewError('false successor mapping')
        sup_map = request['supplement_mapping']
        if (len(sup_map) != len({x['supplement_id'] for x in sup_map}) or
                {x['supplement_id'] for x in sup_map} != set(old_sup) | set(new_sup)):
            raise FullReviewError('supplement conservation mismatch')
        for item in sup_map:
            key = item['supplement_id']
            expected = ('added' if key not in old_sup else 'removed' if key not in new_sup else
                        'unchanged' if old_sup[key] == new_sup[key] else 'changed')
            if item['status'] != expected or not item.get('reason'):
                raise FullReviewError('false supplement mapping')
        if sum(x['status'] != 'unchanged' for x in changes) > 80:
            raise FullReviewError('successor migration limited to 80 changed/added/removed units')
        contexts = request['contexts']
        if set(contexts) != set(after):
            raise FullReviewError('successor requires exact current unit contexts')
        for key, entry in contexts.items():
            if entry['unit_id'] != key or not entry['context'].strip() or not entry['source_files']:
                raise FullReviewError('invalid successor context')
            for source in entry['source_files']:
                source_file(manifest, source)
        value = dict(old, units=units, supplements=supplements, terminology_snapshot=terms,
                     canonical_occurrences=len(units)-len(language),
                     component_counts=dict(Counter(u['occurrence']['component'] for u in units
                                                   if 'supplement_spec' not in u)))
        value.pop('inventory_identity')
        value['predecessor'] = {'directory': str(directory), 'seal': tree_seal(directory),
                                'request': request}
        value['inventory_identity'] = sha(canonical(value))
        # Manifest last is the publication point; identical interrupted writes recover.
        immutable(output / 'migration.json', canonical(request))
        immutable(output / 'inventory.json', canonical(value))
        return {'round_id': old['round_id'], 'units': len(units), 'status': 'successor-frozen'}


@full_review_cache.timed('inventory-validation')
def validate_inventory(manifest, ledger):
    body = {k: v for k, v in ledger.items() if k != 'inventory_identity'}
    if ledger.get('inventory_identity') != sha(canonical(body)) or ledger['manifest_sha256'] != sha(manifest.raw_bytes):
        raise FullReviewError('frozen inventory/manifest drift')


def source_file(manifest, spec):
    component = manifest.component(spec['component'])
    path = identity.normalize_relative_path(spec['public_source_path'])
    reader = FixedReader()
    if component.source_repository:
        repository = manifest.repositories[component.source_repository]
        if repository.visibility != 'public':
            raise FullReviewError('non-public source')
        raw, _ = reader.pinned(manifest.repository_path(component.source_repository), repository.commit, path)
        pin = {'source_pinning': 'pinned', 'commit': repository.commit,
               'source_checkout': str(manifest.repository_path(component.source_repository))}
    else:
        source = component.protected_source
        if source is None or source.visibility != 'public' or not path.startswith(source.mount + '/'):
            raise FullReviewError('source outside logical mount')
        # Explicit inner extraction root, strip logical mount exactly once.
        root = Path(spec['inner_root'])
        if not root.is_absolute() or not root.is_dir() or root.name != source.mount:
            raise FullReviewError('expected explicit inner DLC root named for logical mount')
        raw = ordinary(safe_path(root, path[len(source.mount) + 1:]))
        pin = {'source_pinning': 'unpinned', 'commit': None, 'inner_root': str(root),
               'disclosure': 'Public source/commit unpinned; extraction snapshot is not a source pin.'}
    if sha(raw) != spec['sha256']:
        raise FullReviewError('source file hash mismatch')
    return {**pin, 'public_source_path': path, 'sha256': sha(raw), 'content': raw.decode('utf-8')}


def neutral_entry(entry):
    # Policy metadata never enters reviewer context; reject unexpected fields.
    if set(entry) - {'unit_id', 'context', 'source_files', 'b_reasons', 'b_exemption'}:
        raise FullReviewError('workset must contain only neutral context and B policy')
    return {k: entry[k] for k in ('unit_id', 'context', 'source_files')}


@full_review_cache.timed('workset-parsing')
def output_entry(directory, ref, unit):
    """Read the exact frozen origin, including inherited references."""
    origin = Path(ref.get('_directory', directory))
    raw = ordinary(origin / 'exports' / ref['export_id'] / 'workset.json')
    if sha(raw) != ref['workset_sha256']:
        raise FullReviewError('pair origin workset drift')
    entries = [e for e in _json_bytes(raw, label='pair workset')['entries']
               if e['unit_id'] == unit]
    if len(entries) != 1:
        raise FullReviewError('pair origin unit missing/duplicate')
    return neutral_entry(entries[0])


def match_pair(directory, a, b, unit):
    if output_entry(directory, a, unit) != output_entry(directory, b, unit):
        raise FullReviewError('A/B neutral source/context mismatch')


@full_review_cache.timed('raw-result-validation')
def a_issue(directory, ref, revision):
    origin = Path(ref.get('_directory', directory))
    result = _result_bytes(ordinary(origin / 'exports' / ref['export_id'] / 'input.json'),
        ordinary(origin / 'imports' / ref['export_id'] / 'raw.json'))
    return any(v['revision_key'] == revision and v['verdict'] == 'ISSUE' for v in result['verdicts'])


def b_needed(ledger, obligations, unit):
    policies = [p for ref in obligations.get(unit, [])
                for p in ref['b_policy'] if p['unit_id'] == unit]
    current = ledger.get('predecessor', {}).get('request', {}).get('contexts', {}).get(unit, {})
    return any(p['reasons'] for p in policies) or bool(current.get('b_reasons'))


def export(manifest, directory, selection, workset_path, scope_path, *, export_id, lane,
           task_id=None, dispatch_id=None, workspace_id=None, parent_agent_id=None):
    token(export_id)
    token(task_id)
    token(dispatch_id)
    if len(dispatch_id) > 31 or any(not isinstance(value, str) or not value.strip() for value in (workspace_id, parent_agent_id)):
        raise FullReviewError('freeze exact planned task/dispatch/workspace/parent before export')
    if lane not in {'A', 'B'}:
        raise FullReviewError('lane must be A or B')
    directory = Path(directory)
    with round_lock(directory):
        ledger = read(directory / 'inventory.json')
        live = validate_current(manifest, ledger)
        if not isinstance(selection, list) or not 1 <= len(selection) <= 80 or len(set(selection)) != len(selection):
            raise FullReviewError('select 1..80 unique current units')
        try:
            selected = [live[key] for key in selection]
        except KeyError as error:
            raise FullReviewError('unknown selected unit') from error
        if any(u['disposition'] != 'release-required' or u['catalog_row'] is None for u in selected):
            raise FullReviewError('selection is not language-review applicable')
        fixed = {u['fixed_source_identity'] for u in selected}
        if len(fixed) != 1:
            raise FullReviewError('mixed source identities')
        workset = read(workset_path)
        if workset.get('round_id') != ledger['round_id'] or not isinstance(workset.get('entries'), list):
            raise FullReviewError('wrong round/source workset')
        entries = workset['entries']
        if [e['unit_id'] for e in entries] != selection:
            raise FullReviewError('workset must exactly match ordered selection')
        if 'predecessor' in ledger and any(neutral_entry(ledger['predecessor']['request']['contexts'][e['unit_id']]) != neutral_entry(e) for e in entries):
            raise FullReviewError('export differs from successor context binding')
        contexts, policies = [], []
        source_anchors = {}
        existing = check(manifest, directory, _details=True, _outputs_only=True)
        for unit, entry in zip(selected, entries):
            neutral_entry(entry)
            # Frozen opposite exports matter even before either result is imported.
            opposite = 'B' if lane == 'A' else 'A'
            refs = existing['obligations'].get(unit['unit_id'], [])
            for prior in refs:
                if prior['lane'] == opposite and unit['unit_id'] in prior['selection']:
                    if output_entry(directory, prior, unit['unit_id']) != neutral_entry(entry):
                        raise FullReviewError('A/B neutral source/context mismatch')
            spec = unit.get('supplement_spec')
            if spec and (entry['context'] != spec['context'] or entry['source_files'] != spec['source_files']):
                raise FullReviewError('supplement neutral context/source guard mismatch')
            if not isinstance(entry.get('context'), str) or not entry['context'].strip() or not entry.get('source_files'):
                raise FullReviewError('neutral context and source files required')
            reasons = entry.get('b_reasons')
            if not isinstance(reasons, list) or len(reasons) != len(set(reasons)) or not set(reasons) <= B_REASONS:
                raise FullReviewError('freeze B applicability before dispatch')
            if lane == 'B' and 'A-observation' in reasons:
                a = existing['outputs']['A'].get(unit['unit_id'])
                if a is None or not a_issue(directory, a, unit['revision_key']):
                    raise FullReviewError('A-observation requires validated A ISSUE raw')
            migration_policy = ledger.get('predecessor', {}).get('request', {}).get('contexts', {}).get(unit['unit_id'], {})
            if not set(migration_policy.get('b_reasons', [])) <= set(reasons):
                raise FullReviewError('B applicability cannot shrink from successor policy')
            prior_policies = [p for ref in refs for p in ref['b_policy']
                              if p['unit_id'] == unit['unit_id']]
            if lane == 'B':
                a = existing['outputs']['A'].get(unit['unit_id'])
                if a is not None:
                    origin = Path(a.get('_directory', directory))
                    a_entry = next(e for e in read(origin / 'exports' / a['export_id'] / 'workset.json')['entries']
                                   if e['unit_id'] == unit['unit_id'])
                    if neutral_entry(a_entry) != neutral_entry(entry):
                        raise FullReviewError('B must use the same neutral source/context as validated A')
            if any(not set(p['reasons']) <= set(reasons) for p in prior_policies):
                raise FullReviewError('B applicability cannot shrink')
            if lane == 'B' and not reasons:
                raise FullReviewError('B requires frozen applicability')
            if not reasons and not entry.get('b_exemption'):
                raise FullReviewError('nonapplicable B needs reason')
            facts = []
            for spec in entry['source_files']:
                fact = dict(source_file(manifest, spec))
                source_raw = fact.pop('content').encode('utf-8')
                if sha(source_raw) != spec['sha256']:
                    raise FullReviewError('source anchor bytes/hash mismatch')
                source_anchors[spec['sha256']] = source_raw
                lines = source_raw.decode('utf-8').splitlines()
                start, end = spec.get('line_start', 1), spec.get('line_end', min(100, len(lines)))
                if (type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines) or end - start >= 200):
                    raise FullReviewError('source excerpt requires bounded valid line range (<=200)')
                fact.update(line_start=start, line_end=end, excerpt='\n'.join(lines[start-1:end]))
                facts.append(fact)
            # A canonical component can quote another component or follow its call
            # chain; actual source component/pinning/hash stay in each frozen fact.
            context = batch._contextual_bound_context(unit['catalog_row']) + '\n' + entry['context']
            context += '\nactual_language_metadata=' + canonical({k: unit['occurrence'][k] for k in ('source_tag', 'args_order', 'special')}).decode('utf-8')
            if 'supplement_spec' in unit:
                context += '\nsupplement_origin=' + canonical(unit['supplement_spec']).decode('utf-8')
            context += '\nsource_files=' + canonical(facts).decode('utf-8')
            contexts.append({'revision_key': unit['revision_key'], 'context': context})
            policies.append({'unit_id': unit['unit_id'], 'reasons': reasons,
                             'exemption': entry.get('b_exemption')})
        payload = batch._contextual_payload({'entries': [u['catalog_row'] for u in selected],
                    'identity': (next(iter(fixed)), ledger['terminology_snapshot'])})
        payload['bounded_context'] = contexts
        payload['rendered_briefing'] = 'Full-round neutral language review; review_only/full; no previous review results.'
        envelope = {'candidate_identity': sha(contextual.canonical_payload_bytes(payload)), 'payload': payload}
        envelope_raw = canonical(envelope)
        preflight_raw = canonical(preflight_units(manifest, scope_path, payload, selected))
        dest = directory / 'exports' / export_id
        prompt = build_contextual_prompt(envelope['candidate_identity'], str((dest / 'input.json').absolute()))
        ref = {'round_id': ledger['round_id'], 'export_id': export_id, 'lane': lane,
            'selection': selection, 'revisions': [u['revision_key'] for u in selected],
            'guards': [u['guard'] for u in selected], 'candidate_identity': envelope['candidate_identity'],
            'input_sha256': sha(envelope_raw), 'workset_sha256': sha(ordinary(workset_path)),
            'scope_sha256': sha(ordinary(scope_path)), 'b_policy': policies,
            'source_anchor_hashes': sorted(source_anchors),
            'planned_producer': {'task_id': task_id, 'dispatch_id': dispatch_id,
                                 'workspace_id': workspace_id, 'parent_agent_id': parent_agent_id}}
        ref['preflight_sha256'] = sha(preflight_raw)
        ref['inventory_sha256'] = sha(ordinary(directory / 'inventory.json'))
        ref['freeze_sha256'] = sha(canonical(ref))
        for digest, data in source_anchors.items():
            immutable(dest / 'source-anchors' / (digest + '.bin'), data)
        immutable(dest / 'workset.json', ordinary(workset_path))
        immutable(dest / 'scope.json', ordinary(scope_path))
        immutable(dest / 'input.json', envelope_raw)
        immutable(dest / 'prompt.txt', prompt.encode('utf-8'))
        immutable(dest / 'preflight.json', preflight_raw)
        immutable(dest / 'ref.json', canonical(ref))
        return ref


def replay_export(manifest, directory, export_id, live, *, historical=False):
    return _replay_export(manifest, directory, export_id, live,
                          _InventorySnapshot(directory), historical=historical)


@full_review_cache.timed('export-validation')
def _replay_export(manifest, directory, export_id, live, inventory, *, historical=False):
    dest = Path(directory) / 'exports' / token(export_id)
    ref = read(dest / 'ref.json')
    inventory.verify(directory)
    ledger = inventory.ledger
    if ref.get('freeze_sha256') != sha(canonical({k: v for k, v in ref.items() if k != 'freeze_sha256'})):
        raise FullReviewError('frozen export reference drift')
    if ref.get('inventory_sha256') != inventory.digest:
        raise FullReviewError('export inventory binding drift')
    if set(ref.get('planned_producer', {})) != {'task_id', 'dispatch_id', 'workspace_id', 'parent_agent_id'}:
        raise FullReviewError('export lacks frozen planned producer')
    if ref['round_id'] != ledger['round_id']:
        raise FullReviewError('cross-round export')
    for name, key in [('input.json', 'input_sha256'), ('scope.json', 'scope_sha256'), ('workset.json', 'workset_sha256')]:
        if sha(ordinary(dest / name)) != ref[key]:
            raise FullReviewError('frozen input drift')
    if 'preflight_sha256' in ref and sha(ordinary(dest / 'preflight.json')) != ref['preflight_sha256']:
        raise FullReviewError('frozen preflight bytes drift')
    payload, candidate = contextual.validate_envelope(read(dest / 'input.json'))
    if candidate != ref['candidate_identity'] or payload['ordered_revision_keys'] != ref['revisions']:
        raise FullReviewError('export identity/order mismatch')
    if (len(set(ref['selection'])) != len(ref['selection']) or not 1 <= len(ref['selection']) <= 80 or
            len(ref['selection']) != len(ref['revisions']) or len(ref['guards']) != len(ref['selection'])):
        raise FullReviewError('duplicate export selection')
    for key, rev, guard in zip(ref['selection'], ref['revisions'], ref['guards']):
        if key not in live or (live[key]['revision_key'], live[key]['guard']) != (rev, guard):
            raise FullReviewError('stale export revision/guard')
    workset = read(dest / 'workset.json')
    hashes = sorted({spec['sha256'] for entry in workset['entries'] for spec in entry['source_files']})
    if hashes != ref.get('source_anchor_hashes'):
        raise FullReviewError('source anchor set drift')
    for digest in hashes:
        if not re.fullmatch('[0-9a-f]{64}', digest) or sha(ordinary(dest / 'source-anchors' / (digest+'.bin'))) != digest:
            raise FullReviewError('tracked source anchor drift')
    if ref['b_policy'] != [{'unit_id': e['unit_id'], 'reasons': e['b_reasons'], 'exemption': e.get('b_exemption')} for e in workset['entries']]:
        raise FullReviewError('B applicability freeze drift')
    if not historical:
        for entry in workset['entries']:
            for spec in entry['source_files']:
                source_file(manifest, spec)
        preflight_raw = canonical(preflight_units(manifest, dest / 'scope.json', payload, [live[k] for k in ref['selection']]))
        if 'preflight_sha256' in ref and sha(preflight_raw) != ref['preflight_sha256']:
            raise FullReviewError('current preflight differs from frozen receipt')
    return ref, ordinary(dest / 'input.json')


def gate_selection(manifest, ref, *, execution=True):
    task = manifest.root / '.ai/task' / ref['planned_producer']['task_id']
    selected = {'base_commit': read(task / 'BASELINE-MANIFEST.json')['head'],
        'full_review_task': ref['planned_producer'], 'round_id': ref['round_id'],
        'export_id': ref['export_id'], 'freeze_sha256': ref['freeze_sha256'],
        'candidate_identity': ref['candidate_identity'], 'ordered_revisions': ref['revisions'],
        'guards': ref['guards'], 'input_sha256': ref['input_sha256'],
        'workset_sha256': ref['workset_sha256'], 'scope_sha256': ref['scope_sha256'],
        'spec_sha256': sha(ordinary(task / 'SPEC.md'))}
    if execution:
        selected['execution_inputs'] = {p.relative_to(manifest.root).as_posix(): sha(ordinary(p))
            for base in ('tools', 'i18n', 'tests') for p in sorted((manifest.root / base).rglob('*'))
            if p.is_file() and p.suffix in {'.py', '.lua', '.json', '.sh'} and '__pycache__' not in p.parts}
    return selected


def task_gates(manifest, directory, export_id, results_path=None):
    """Execute full existing gates once for this exact task; archive all logs.

    No checkpoint/queue dependency. The task SPEC and frozen export must already
    exist; DONE may be established afterwards under the unchanged review_only contract.
    """
    directory = Path(directory)
    if not directory.absolute().is_relative_to(manifest.root / 'evidence/full-review'):
        raise FullReviewError('task gates require tracked round evidence directory')
    ledger = read(directory / 'inventory.json')
    ref, _ = replay_export(manifest, directory, export_id, validate_current(manifest, ledger))
    selected = gate_selection(manifest, ref)
    result = _execute_task_gates(manifest, directory, selected, results_path)
    if selected != gate_selection(manifest, ref):
        raise FullReviewError('task gate input drift during execution')
    return _archive_task_gates(manifest, directory, ref['planned_producer']['task_id'], export_id, result)


def _execute_task_gates(manifest, directory, selected, results_path=None):
    """Production receipt boundary, also usable for ignored measurement fixtures.

    Public task_gates performs tracked-directory authorization and export replay;
    this boundary grants no review, import or coverage credit.
    """
    directory = Path(directory)
    result = (gate_results.run(manifest.root, selected=selected, skip_build=False,
                               reuse_round=directory.resolve())
              if results_path is None else read(results_path))
    gate_results.validate(result, selected=selected, require_full=True, root=manifest.root,
                          expected_test_identities=gate_results.test_identities(manifest.root)
                          if result['schema_version'] == 3 else None)
    if result['schema_version'] == 3 and result['reuse_round'] != directory.resolve().relative_to(manifest.root).as_posix():
        raise FullReviewError('task gate reuse round drift')
    return result


def _archive_task_gates(manifest, directory, task_id, export_id, result):
    dest = Path(directory) / 'task-gates' / task_id / export_id
    # Different invocations have different timestamps: never overwrite a frozen receipt.
    for record in result['checks']:
        immutable(dest / record['id'] / 'output.log', gate_results.record_output(manifest.root, record))
    immutable(dest / 'results.json', canonical(result))
    return {'gate_evidence_path': (dest / 'results.json').relative_to(manifest.root).as_posix(),
            'gate_evidence_sha256': sha(canonical(result))}


def validate_task_gates(manifest, ref, binding, *, accepted_selection=None):
    path = binding.get('gate_evidence_path', '')
    task = ref['planned_producer']['task_id']
    suffix = '/task-gates/' + task + '/' + ref['export_id'] + '/results.json'
    if not path.startswith('evidence/full-review/') or not path.endswith(suffix):
        raise FullReviewError('missing task-specific tracked full gate/build receipt')
    receipt_path = safe_path(manifest.root, path)
    raw = ordinary(receipt_path)
    if sha(raw) != binding.get('gate_evidence_sha256'):
        raise FullReviewError('task gate receipt bytes drift')
    result = read(receipt_path)
    if result.get('schema_version') == 3 and result.get('reuse_round') != path.split('/task-gates/')[0]:
        raise FullReviewError('task gate reuse round drift')
    try:
        if accepted_selection is None:
            selected = gate_selection(manifest, ref)
            gate_results.validate(result, selected=selected, require_full=True,
                                  root=manifest.root if result.get("schema_version") == 3 else None,
                                  receipt_path=path if result.get("schema_version") == 3 else None)
        else:
            selected = accepted_selection
            if (not isinstance(selected, dict) or 'execution_inputs' not in selected or
                    {k: v for k, v in selected.items() if k != 'execution_inputs'} !=
                    gate_selection(manifest, ref, execution=False)):
                raise FullReviewError('accepted task gate identity drift')
            gate_results.validate_historical(result, selected=selected,
                root=manifest.root if result.get("schema_version") == 3 else None,
                receipt_path=path if result.get("schema_version") == 3 else None)
    except gate_results.GateError as error:
        raise FullReviewError('task full gate/build receipt rejected: ' + str(error)) from error
    for record in result['checks']:
        if sha(ordinary(receipt_path.parent / record['id'] / 'output.log')) != record['output_sha256']:
            raise FullReviewError('tracked task gate log drift')
    return selected


def task_anchors(manifest, binding):
    """Archive terminal inputs as real bytes, preserving root-relative locators.

    Recursive JSON path references within .ai are included, as are full-review
    evidence inputs. These tracked copies permit replay in a reconstructed root;
    no ignored-file hash alone is a terminal anchor.
    """
    task = manifest.root / '.ai/task' / binding['task_id']
    pending = list(task.rglob('*')) + list((manifest.root / '.ai/reviews' / binding['task_id']).rglob('*'))
    files = {}
    while pending:
        path = pending.pop()
        if not path.is_file():
            continue
        name = path.relative_to(manifest.root).as_posix()
        if name in files:
            continue
        raw = ordinary(path)
        files[name] = raw
        if path.suffix == '.json':
            value = read(path)
            def references(v):
                if isinstance(v, dict):
                    for child in v.values():
                        yield from references(child)
                elif isinstance(v, list):
                    for child in v:
                        yield from references(child)
                elif isinstance(v, str):
                    p = Path(v)
                    if p.is_absolute():
                        if not p.is_relative_to(manifest.root):
                            return
                        v = p.relative_to(manifest.root).as_posix()
                    if v.startswith(('.ai/', 'evidence/full-review/', '.artifacts/i18n/')):
                        p = safe_path(manifest.root, v)
                        if p.is_file():
                            yield p
            pending.extend(references(value))
    return files


@full_review_cache.timed('import-validation')
def validate_terminal_anchors(manifest, binding, dest):
    for name, data in task_anchors(manifest, binding).items():
        if ordinary(safe_path(dest / 'task-anchors', name)) != data:
            raise FullReviewError('tracked task terminal anchor drift')


@full_review_cache.timed('import-validation')
def producer(manifest, ref, binding, input_raw, raw, *, accepted_selection=None):
    # Bind task, fresh dispatch, live identity, workspace and direct lineage.
    task_id = token(binding['task_id'])
    state_path = manifest.root / '.ai/task' / task_id / 'STATE.json'
    state = read(state_path)
    if any(binding.get(key) != value for key, value in ref['planned_producer'].items()):
        raise FullReviewError('producer differs from frozen planned task/dispatch/lineage')
    spec_path = state_path.parent / 'SPEC.md'
    lines = ordinary(spec_path).decode('utf-8').splitlines()
    round_bindings = [line.removeprefix('full_review_binding=') for line in lines if line.startswith('full_review_binding=')]
    expected_binding = {'round_id': ref['round_id'], 'export_id': ref['export_id'],
                        'freeze_sha256': ref['freeze_sha256'], 'input_sha256': ref['input_sha256']}
    if len(round_bindings) != 1 or contextual.strict_json_bytes(round_bindings[0].encode(), label='task round binding') != expected_binding:
        raise FullReviewError('task SPEC is not bound to this exact round/export freeze')
    if sha(ordinary(state_path.parent / 'SCOPE.json')) != ref['scope_sha256']:
        raise FullReviewError('task SCOPE differs from host frozen scope')
    task_ref = {'task_id': task_id, 'task_state_path': str(state_path),
                'candidate_identity': ref['candidate_identity']}
    if (state.get('mode') != 'review_only' or state.get('schema_version', 0) < 5 or
            not batch._contextual_done_verified(manifest.root, task_ref, input_raw, raw)):
        raise FullReviewError('task itself lacks bound DONE_VERIFIED review_only/full')
    validate_task_gates(manifest, ref, binding, accepted_selection=accepted_selection)
    children = state.get('child_dispatches', [])
    matched = [c for c in children if c.get('dispatch_id') == binding['dispatch_id']]
    if len(matched) != 1:
        raise FullReviewError('exact dispatch missing/ambiguous')
    child = matched[0]
    for key in ('workspace_id', 'parent_agent_id'):
        if not isinstance(binding.get(key), str) or not binding[key] or child.get(key) != binding[key]:
            raise FullReviewError(f'unknown/mismatched producer {key}')
    observed = child.get('runtime_observation', {}).get('model', {})
    if observed.get('presence') != 'present' or observed.get('value') != binding.get('model') or not binding.get('model'):
        raise FullReviewError('unknown/mismatched exact runtime model')
    if state.get('workspace_id') != binding['workspace_id'] or state.get('orchestrator_agent_id') != binding['parent_agent_id']:
        raise FullReviewError('task workspace/lineage mismatch')
    if (child.get('role') != 'REVIEWER' or child.get('purpose') != 'translation_contextual_v2' or
            child.get('archive_confirmed') is not True or child.get('lifecycle') != 'archived' or
            child.get('lineage_verified') is not True or child.get('output_valid') is not True or
            child.get('raw_output_sha256') != sha(raw) or
            child.get('candidate_identity') != ref['candidate_identity']):
        raise FullReviewError('producer is not exact archived reviewer')
    return sha(ordinary(state_path))


def import_result(manifest, directory, export_id, raw_path, binding_path):
    directory = Path(directory)
    with round_lock(directory):
        ledger = read(directory / 'inventory.json')
        live = validate_current(manifest, ledger)
        ref, input_raw = replay_export(manifest, directory, export_id, live)
        raw, binding = ordinary(raw_path), read(binding_path)
        if (binding.get('round_id'), binding.get('export_id'), binding.get('input_sha256'),
                binding.get('raw_sha256')) != (ledger['round_id'], export_id, sha(input_raw), sha(raw)):
            raise FullReviewError('exact import binding mismatch')
        _result_bytes(input_raw, raw)
        if not binding.get('gate_evidence_path'):
            raise FullReviewError('missing task-specific tracked full gate/build receipt')
        dest = directory / 'imports' / export_id
        accepted = read(dest / 'receipt.json') if (dest / 'receipt.json').exists() else None
        selection = None
        if accepted is not None:
            if (accepted.get('export_id') != export_id or accepted.get('lane') != ref['lane'] or
                    accepted.get('binding') != binding or
                    accepted.get('status') != 'output-validated-and-archived' or
                    not isinstance(accepted.get('gate_selection'), dict) or
                    ordinary(dest / 'raw.json') != raw):
                raise FullReviewError('conflicting import bytes')
            validate_terminal_anchors(manifest, binding, dest)
            selection = accepted['gate_selection']
        state_hash = producer(manifest, ref, binding, input_raw, raw, accepted_selection=selection)
        if selection is None:
            selection = gate_selection(manifest, ref)
        receipt = {'export_id': export_id, 'lane': ref['lane'], 'binding': binding,
                   'state_sha256': state_hash, 'status': 'output-validated-and-archived',
                   'gate_selection': selection}
        # Inspect conflicts before any evidence write. Orphan identical raw is recoverable.
        for path, data in [(dest / 'raw.json', raw), (dest / 'receipt.json', canonical(receipt))]:
            if path.exists() and ordinary(path) != data:
                raise FullReviewError('conflicting import bytes')
        for name, data in task_anchors(manifest, binding).items():
            immutable(safe_path(dest / 'task-anchors', name), data)
        immutable(dest / 'raw.json', raw)
        immutable(dest / 'receipt.json', canonical(receipt))
        return {'status': receipt['status'], 'effective_completed': 0}


def check(manifest, directory, *, require_complete=False, _historical=False, _details=False, _outputs_only=False):
    with full_review_cache.timing(), _parse_scope():
        return _check(manifest, directory, require_complete=require_complete,
                      _historical=_historical, _details=_details, _outputs_only=_outputs_only)


def _check(manifest, directory, *, require_complete=False, _historical=False,
           _details=False, _outputs_only=False, _inventory=None):
    # Only the internal predecessor path supplies a snapshot. Public check/replay
    # always decode afresh; recursive entry still reads exact ordinary bytes.
    directory = Path(directory)
    inventory = _InventorySnapshot(directory) if _inventory is None else _inventory
    if _inventory is not None:
        inventory.verify(directory)
    ledger = inventory.ledger
    validate_inventory(manifest, ledger)
    live = ({u['unit_id']: u for u in ledger['units']} if _historical else validate_current(manifest, ledger))
    frozen = {}
    obligations = {}
    for path in sorted((directory / 'exports').glob('*/ref.json')):
        export_id = path.parent.name
        ref, input_raw = _replay_export(manifest, directory, export_id, live, inventory, historical=_historical)
        if ref['export_id'] != export_id:
            raise FullReviewError('export path/reference identity mismatch')
        frozen[export_id] = (ref, input_raw)
        for unit in ref['selection']:
            obligations.setdefault(unit, []).append(ref)
    outputs = {'A': {}, 'B': {}}
    models = {}
    for path in sorted((directory / 'imports').glob('*/receipt.json')):
        receipt = read(path)
        if receipt['export_id'] not in frozen:
            raise FullReviewError('import has no complete frozen export')
        ref, input_raw = frozen[receipt['export_id']]
        raw = ordinary(path.parent / 'raw.json')
        binding = receipt['binding']
        if ((binding.get('round_id'), binding.get('export_id')) != (ledger['round_id'], ref['export_id']) or
                sha(raw) != binding['raw_sha256'] or sha(input_raw) != binding['input_sha256']):
            raise FullReviewError('import recovery hash mismatch')
        _result_bytes(input_raw, raw)
        if (receipt.get('status') != 'output-validated-and-archived' or receipt.get('lane') != ref['lane'] or
                not isinstance(receipt.get('gate_selection'), dict)):
            raise FullReviewError('incomplete accepted import receipt')
        validate_terminal_anchors(manifest, binding, path.parent)
        if producer(manifest, ref, binding, input_raw, raw,
                    accepted_selection=receipt['gate_selection']) != receipt['state_sha256']:
            raise FullReviewError('import terminal task bytes drift')
        for unit in ref['selection']:
            if unit in outputs[ref['lane']]:
                raise FullReviewError('duplicate current lane coverage')
            outputs[ref['lane']][unit] = ref
            models[(ref['lane'], unit)] = (binding['model'], binding['dispatch_id'])
    for unit in set(outputs['A']) & set(outputs['B']):
        if any(a == b for a, b in zip(models[('A', unit)], models[('B', unit)])):
            raise FullReviewError('A/B require different exact models and fresh dispatches')
    predecessor = ledger.get('predecessor')
    if predecessor:
        previous = Path(predecessor['directory'])
        if tree_seal(previous) != predecessor['seal']:
            raise FullReviewError('predecessor frozen evidence drift')
        if read(directory / 'migration.json') != predecessor['request']:
            raise FullReviewError('successor migration freeze drift')
        evidence_files(manifest, predecessor['request']['evidence'])
        # The parent needs only mapping guards, not a second complete object graph.
        # pop transfers sole ownership before descending; deepcopy keeps even
        # structured guards independent of the child's mutable parsed objects.
        handoff = [_InventorySnapshot(previous)]
        if handoff[0].ledger['round_id'] != ledger['round_id']:
            raise FullReviewError('cross-round predecessor rejected')
        old_units = {u['unit_id']: deepcopy({k: u[k] for k in ('revision_key', 'guard') if k in u})
                     for u in handoff[0].ledger['units']}
        # Frozen export bytes are consumed by the import loop above. A historical
        # level also drops its parsed inventory before descending, so the chain
        # never holds one parse per round; it is re-read and digest-bound after.
        del frozen
        predecessor_seal = predecessor['seal']
        if _historical:
            inventory.ledger = None
            del ledger, live, predecessor
        def verify_predecessor():
            return _check(manifest, previous, _historical=True, _details=True,
                          _outputs_only=_outputs_only, _inventory=handoff.pop())
        prior = full_review_cache.predecessor(
            manifest, previous, predecessor_seal, _outputs_only, verify_predecessor)
        if _historical:
            inventory.reload(directory)
            ledger = inventory.ledger
            live = {u['unit_id']: u for u in ledger['units']}
            predecessor = ledger['predecessor']
        with full_review_cache.segment('coverage-inheritance'):
            unchanged = {x['unit_id'] for x in predecessor['request']['mapping'] if x['status'] == 'unchanged'}
            for unit in unchanged:
                if unit not in live or unit not in old_units or (live[unit]['revision_key'], live[unit]['guard']) != (old_units[unit]['revision_key'], old_units[unit]['guard']):
                    raise FullReviewError('invalid unchanged predecessor mapping')
                # Pending frozen lanes carry policy even without any imported output.
                # Only exact unchanged revision/guard and neutral context can inherit it.
                for old_ref in prior['obligations'].get(unit, []):
                    if output_entry(previous, old_ref, unit) != neutral_entry(predecessor['request']['contexts'][unit]):
                        continue
                    origin = Path(old_ref.get('_directory', previous))
                    if not _historical:
                        for spec in output_entry(previous, old_ref, unit)['source_files']:
                            source_file(manifest, spec)
                    obligations.setdefault(unit, []).append(dict(old_ref, _directory=str(origin)))
                for lane in ('A', 'B'):
                    old_ref = prior['outputs'][lane].get(unit)
                    if old_ref is None:
                        continue
                    origin = Path(old_ref.get('_directory', previous))
                    workset = read(origin / 'exports' / old_ref['export_id'] / 'workset.json')
                    entry = next(e for e in workset['entries'] if e['unit_id'] == unit)
                    if neutral_entry(entry) != neutral_entry(predecessor['request']['contexts'][unit]):
                        continue
                    if not _historical:
                        for spec in entry['source_files']:
                            source_file(manifest, spec)
                    if unit in outputs[lane]:
                        raise FullReviewError('duplicate inherited/current coverage')
                    outputs[lane][unit] = dict(old_ref, _directory=str(origin))

    with full_review_cache.segment('coverage-aggregation'):
        for unit in set(outputs['A']) & set(outputs['B']):
            refs = [outputs[lane][unit] for lane in ('A', 'B')]
            match_pair(directory, refs[0], refs[1], unit)
            bindings = [read(Path(ref.get('_directory', directory)) / 'imports' / ref['export_id'] / 'receipt.json')['binding'] for ref in refs]
            if any(bindings[0][k] == bindings[1][k] for k in ('model', 'dispatch_id')):
                raise FullReviewError('inherited A/B require different models and fresh dispatches')
        inherited_decisions = []
        if predecessor:
            for unit, decision in prior['decisions'].items():
                if unit in unchanged and all(
                        outputs[lane].get(unit) == prior['outputs'][lane].get(unit) or
                        outputs[lane].get(unit) == dict(prior['outputs'][lane].get(unit, {}),
                            _directory=prior['outputs'][lane].get(unit, {}).get('_directory', str(previous)))
                        for lane in ('A', 'B') if unit in prior['completed'][lane]):
                    a = outputs['A'].get(unit)
                    needed = b_needed(ledger, obligations, unit) or (a is not None and a_issue(directory, a, live[unit]['revision_key'])) or decision.get('a_observation_requires_b') is True
                    if not needed or unit in prior['completed']['B'] and unit in outputs['B']:
                        inherited_decisions.append(decision)
        # M1 intentionally does not synthesize host adjudication or denominator closure.
        # A receipt is output validation, never effective coverage. Host adjudicated evidence
        # is consumed only with exact raw hashes, source verification and a merged decision.
        completed = {'A': set(), 'B': set()}
        decisions = {}
        current_decisions = [] if _outputs_only else [read(path) for path in sorted((directory / 'adjudications').glob('*.json'))]
        if _outputs_only:
            inherited_decisions = []
        current_keys = {d.get('unit_id') for d in current_decisions}
        for decision in [d for d in inherited_decisions if d['unit_id'] not in current_keys] + current_decisions:
            unit = decision.get('unit_id')
            if (decision.get('round_id') != ledger['round_id'] or unit not in live or
                    decision.get('revision_key') != live[unit]['revision_key'] or unit in completed['A']):
                raise FullReviewError('invalid/duplicate adjudication identity')
            a = outputs['A'].get(unit)
            if a is None:
                raise FullReviewError('adjudication requires validated A')
            needed = b_needed(ledger, obligations, unit) or a_issue(directory, a, live[unit]['revision_key']) or decision.get('a_observation_requires_b') is True
            b = outputs['B'].get(unit)
            if needed and b is None:
                raise FullReviewError('merged adjudication missing required B')
            for lane, ref in [('A', a), ('B', b if needed else None)]:
                if ref and decision.get('raw_sha256', {}).get(lane) != sha(ordinary(Path(ref.get('_directory', directory)) / 'imports' / ref['export_id'] / 'raw.json')):
                    raise FullReviewError('adjudication raw binding mismatch')
            if (decision.get('source_verified') is not True or decision.get('accepted_successor') is not True or
                    decision.get('confirmed') != [] or decision.get('blocking_pending') != [] or
                    decision.get('status') != 'effective-complete' or not decision.get('evidence')):
                continue
            for evidence in decision['evidence']:
                if sha(ordinary(safe_path(manifest.root, evidence['path']))) != evidence['sha256']:
                    raise FullReviewError('adjudicated evidence drift')
            decisions[unit] = decision
            completed['A'].add(unit)
            if needed:
                completed['B'].add(unit)
        if _details:
            return {'outputs': outputs, 'obligations': obligations, 'completed': completed, 'decisions': decisions}
        applicable = sum(u['disposition'] == 'release-required' for u in live.values())
        result = {'round_id': ledger['round_id'], 'canonical_occurrences': sum('supplement_spec' not in u for u in live.values()),
            'provisional_applicable_units': applicable, 'A_validated_outputs': len(outputs['A']),
            'B_validated_outputs': len(outputs['B']), 'A_effective_complete': len(completed['A']),
            'B_effective_complete': len(completed['B']), 'A_remaining': applicable - len(completed['A']),
            'supplements_pending': len(ledger['supplements']), 'denominator_frozen': False,
            'review_progress_complete': False, 'release_ready': False,
            'blockers': ['source/runtime conservation not host-closed', 'supplement language units not frozen',
                         'retained/dynamic layers not host-closed', 'Engine/game final scenarios untested']}
        closure = None if _historical else closure_check(manifest, directory, ledger, live, completed)
        if closure is not None:
            result.update(closure)
            result.update(denominator_frozen=True, review_progress_complete=True, supplements_pending=0,
                          blockers=[] if closure['release_ready'] else ['final Engine/game scenarios not measured/accepted'])
        if require_complete and not result['review_progress_complete']:
            raise FullReviewError('round incomplete: ' + canonical(result).decode('utf-8'))
        return result


def evidence_files(manifest, records):
    if not isinstance(records, list) or not records:
        raise FullReviewError('host closure needs tracked evidence bindings')
    for item in records:
        path = item.get('path', '')
        if not path.startswith('evidence/') or sha(ordinary(safe_path(manifest.root, path))) != item.get('sha256'):
            raise FullReviewError('missing/drifted tracked host evidence')


# Only this audited engine implementation is supported. A new pin requires an
# explicit capability review, rather than silently using the current checkout.
I18N_SOURCE = {'repository': 'engine',
    'commit': '624a67329fe2ad440c5b344785a9c73fcf22ae63',
    'path': 'game/engines/default/engine/I18N.lua',
    'sha256': 'a099d023bcf9c91d83592331666aeaa86c901a469eadf59346bcbd279c7ef31d',
    'capability': 'fixed-i18n-literal-chain-v1'}


def _lua_literal(value):
    if value is None:
        return 'nil'
    if isinstance(value, str):
        return '"' + ''.join('\\%03d' % byte for byte in value.encode('utf-8')) + '"'
    if type(value) is bool:
        return 'true' if value else 'false'
    if type(value) in (int, float):
        canonical(value)  # Reject nonfinite JSON values.
        return str(value)
    if isinstance(value, list):
        return '{' + ','.join(_lua_literal(v) for v in value) + '}'
    if isinstance(value, dict):
        return '{' + ','.join('[' + _lua_literal(k) + ']=' + _lua_literal(v)
                              for k, v in value.items()) + '}'
    raise FullReviewError('unsupported runtime literal')


_I18N_DRIVER = r"""
class={make=function(m) return m end}
package.loaded['engine.class']=true
assert(loadfile(arg[1]))('engine.I18N')
local I=package.loaded['engine.I18N']
local get
for n=1,20 do
  local name,value=debug.getupvalue(default_tformat,n)
  if name=='get' then get=value; break end
end
assert(get, 'unsupported fixed I18N accessor')
local function encode(v)
  if v==nil then return 'null' end
  if type(v)=='boolean' or type(v)=='number' then return tostring(v) end
  if type(v)=='string' then
    return '"'..v:gsub('[%z\1-\31\\"]',function(c)
      return ('\\u%04x'):format(c:byte())
    end)..'"'
  end
  assert(type(v)=='table','unsupported runtime value')
  local out={}
  local count=0
  for k in pairs(v) do count=count+1 end
  if count>0 and count==#v then
    for n=1,#v do out[n]=encode(v[n]) end
    return '['..table.concat(out,',')..']'
  end
  for k,x in pairs(v) do
    assert(type(k)=='string','unsupported runtime table key')
    out[#out+1]=encode(k)..':'..encode(x)
  end
  return '{'..table.concat(out,',')..'}'
end
local input=assert(loadfile(arg[2]))()
local records={}
for index,layer in ipairs(input.layers) do
  local env={}
  env.locale=function(lc) assert(lc=='zh_hans','unsupported locale') end
  env.section=function(s) assert(type(s)=='string') end
  env.forceFontPackage=function(id) assert(type(id)=='string') end
  env.setFlag=function(flag,value)
    assert(flag~='tformat_special','dynamic special processor unsupported')
    assert(type(value)=='boolean' or type(value)=='string' or type(value)=='number',
      'dynamic flag unsupported')
    I.setFlag('zh_hans',flag,value)
  end
  local ordinal=0
  env.t=function(src,dst,tag,args,special)
    assert(type(src)=='string' and type(dst)=='string','unsupported translation')
    assert(tag==nil or type(tag)=='string','unsupported tag')
    encode(args); encode(special) -- Reject unsupported values even on shadowed rows.
    ordinal=ordinal+1
    local record={layer=layer.layer, ordinal=ordinal,
      line=debug.getinfo(2,'l').currentline, source_tag=tag}
    records[#records+1]=record
    I:t('zh_hans',src,dst,tag,args,special)
    -- The same actual setter/lookup tracks which registration supplied target.
    I:t('provenance',src,tostring(#records),tag)
  end
  setmetatable(env,{__index=function(_,k) error('unsupported locale global: '..tostring(k)) end})
  local chunk=assert(loadfile(layer.file))
  setfenv(chunk,env)
  chunk()
end
local output=assert(io.open(arg[3],'wb'))
for _,q in ipairs(input.queries) do
  I:setLocale('zh_hans')
  local _,targets,args,special=I:getLocalesData()
  local tag=q.tag
  if q.method=='_t' then tag=tag or '_t' end
  if q.method=='string.tformat' then tag='tformat' end
  local a=get(args,q.source,tag)
  local sp=get(special,q.source,tag)
  if q.method=='string.tformat' and get(special,q.source,nil) then
    a=get(args,q.source,nil)
  end
  local target=_t(q.source,tag)
  local formatted
  if q.arguments then
    if q.method=='string.tformat' then formatted=string.tformat(q.source,unpack(q.arguments))
    elseif q.method=='default_tformat' then formatted=default_tformat(q.source,tag,unpack(q.arguments))
    else error('arguments require format query') end
  end
  I:setLocale('provenance')
  local _,provenance=I:getLocalesData()
  local id=get(provenance,q.source,tag or '_t')
  local record=records[tonumber(id)]
  -- Missing keys are kept, with explicit source fallback provenance.
  local result={target=target, args_order=a, special=sp,
    effective_layer=record and record.layer or 'source-fallback',
    effective_registration=record, formatted=formatted}
  output:write(encode(result),'\n')
end
output:close()
"""


def i18n_effective(runtime, layers, queries):
    """Execute the pinned engine, with literal-only locale capability and timeout.

    All keys in one closure use the same complete ordered chain. No raw loader
    row dictionary is used as a substitute for the game's mutable tag buckets.
    """
    manifest = runtime.manifest
    repo = manifest.repositories['engine']
    if repo.commit != I18N_SOURCE['commit'] or repo.visibility != 'public':
        raise FullReviewError('unsupported I18N source pin')
    source, _ = FixedReader().pinned(manifest.repository_path('engine'), repo.commit, I18N_SOURCE['path'])
    if sha(source) != I18N_SOURCE['sha256']:
        raise FullReviewError('fixed I18N source hash mismatch')
    for q in queries:
        if (set(q) - {'source', 'tag', 'method', 'arguments'} or
                q.get('method') not in {'_t', 'default_tformat', 'string.tformat'} or
                not isinstance(q.get('source'), str) or 'tag' not in q or
                q['tag'] is not None and not isinstance(q['tag'], str) or
                q['method'] == 'string.tformat' and q['tag'] != 'tformat' or
                'arguments' in q and not isinstance(q['arguments'], list)):
            raise FullReviewError('unsupported/ambiguous runtime query')
    with tempfile.TemporaryDirectory(prefix='tome4-fixed-i18n-') as tmp:
        root = Path(tmp)
        (root/'I18N.lua').write_bytes(source)
        (root/'driver.lua').write_text(_I18N_DRIVER, encoding='utf-8')
        inputs = []
        for n, (layer, raw) in enumerate(layers):
            file = root/f'layer-{n}.lua'
            file.write_bytes(raw)
            inputs.append({'layer': layer['layer'], 'file': str(file)})
        (root/'input.lua').write_text('return ' + _lua_literal({'layers': inputs, 'queries': queries}), encoding='utf-8')
        result = runtime.run([root/'driver.lua', root/'I18N.lua', root/'input.lua', root/'output.jsonl'],
                             cwd=manifest.root, timeout=15)
        if result.returncode:
            raise FullReviewError('fixed I18N execution unsupported/failed: ' + result.stderr.strip())
        rows = [contextual.strict_json_bytes(line, label='fixed I18N output')
                for line in ordinary(root/'output.jsonl').splitlines()]
    for row in rows:
        if row.get('effective_registration') is not None:
            row['effective_registration'].setdefault('source_tag', None)
        if row.get('args_order') == {}:
            row['args_order'] = []
    if len(rows) != len(queries):
        raise FullReviewError('fixed I18N query output incomplete')
    return rows


def normalized_key_tag(tag):
    return '_t' if tag is None else tag


def normalized_query_tag(query):
    method = query.get('method')
    if method == 'string.tformat':
        if query.get('tag') != 'tformat':
            raise FullReviewError('string.tformat query tag mismatch')
        return 'tformat'
    if method not in {'_t', 'default_tformat'} or 'tag' not in query:
        raise FullReviewError('unsupported query method/tag')
    return normalized_key_tag(query['tag'])


def release_readiness(manifest, candidate, readiness):
    from .release_candidate import isolated, target_files
    scenes = readiness.get('scenarios')
    if not isinstance(scenes, list) or not scenes:
        return False
    proofs = [readiness.get('engine_actual_loading'), readiness.get('game_launch'), *scenes]
    for proof in proofs:
        if not isinstance(proof, dict):
            return False
        accepted = proof.get('status') == 'user-accepted-untested' and proof in scenes
        if proof.get('status') != 'passed' and not accepted:
            return False
        evidence_files(manifest, proof.get('user_acceptance') if accepted else proof.get('evidence'))
        binding = proof.get('binding', {})
        if binding.get('candidate_sha256') != sha(ordinary(candidate / 'candidate.json')):
            raise FullReviewError('release proof exact candidate mismatch')
        target = isolated(manifest, binding['target'], 'isolated-game')
        operation_id = token(binding['operation_id'])
        operation = target / '.full-review-install' / operation_id
        intent = read(operation / 'installed.json')
        if ((operation / 'restored.json').exists() or read(operation / 'intent.json') != intent or
                intent['candidate_sha256'] != binding['candidate_sha256'] or
                intent['spec_sha256'] != binding.get('spec_sha256') or
                sha(canonical(intent)) != binding.get('installed_sha256') or intent['target'] != str(target)):
            raise FullReviewError('release proof target/spec/install operation mismatch')
        target_files(manifest, target, intent['spec'])
        for resource, expected in [(intent['resource'], intent['after_sha256']),
                                   (intent['addon_resource'], intent['addon_after_sha256'])]:
            if sha(ordinary(safe_path(target, resource))) != expected:
                raise FullReviewError('release proof installed bytes drift')
        # The proof artifact carries the binding too; an old prototype log cannot be relabelled.
        for item in proof.get('user_acceptance') if accepted else proof['evidence']:
            artifact = read(safe_path(manifest.root, item['path']))
            if artifact.get('binding') != binding or artifact.get('status') != proof['status']:
                raise FullReviewError('release measurement artifact binding mismatch')
    return True


def loading_bytes(manifest, supplement, mapping):
    kind = supplement['kind']
    path = supplement.get('path')
    if not isinstance(path, str):
        raise FullReviewError('loading-only source path missing')
    if kind == 'copy':
        content = supplement.get('content')
        if not isinstance(content, str):
            raise FullReviewError('loading-only frozen copy bytes missing')
        raw = content.encode('utf-8')
        if ordinary(safe_path(manifest.root, path)) != raw:
            raise FullReviewError('loading-only copy bytes drift')
    elif kind == 'retained-layer':
        repo = manifest.repositories['addon']
        if repo.visibility != 'public' or supplement.get('commit') != repo.commit:
            raise FullReviewError('loading-only retained source pin mismatch')
        raw, _ = FixedReader().pinned(manifest.repository_path('addon'), repo.commit, path)
    else:
        spec = mapping.get('source_file')
        if (not isinstance(spec, dict) or spec.get('component') != supplement['component'] or
                spec.get('public_source_path') != path or spec.get('sha256') != supplement.get('sha256')):
            raise FullReviewError('loading-only wrapper needs exact public source_file')
        raw = source_file(manifest, spec)['content'].encode('utf-8')
    if sha(raw) != supplement.get('sha256'):
        raise FullReviewError('loading-only source hash mismatch')
    return raw


def loading_literals(raw):
    """Conservative, bounded Lua directive classifier, never executes input.

    Only audited scalar flags and font/locale control calls prove no language.
    Strings in tables, text fields or unknown calls remain possible language;
    unknown/dynamic syntax cannot prove absence even when it has no literals.
    """
    try:
        text = raw.decode('utf-8')
        tokens, cursor = [], 0
        syntax = re.compile(r'[A-Za-z_][A-Za-z_0-9]*|[0-9]+(?:\.[0-9]+)?|.')
        while cursor < len(text):
            cursor = anchors._skip_space_and_comments(text, cursor)
            if cursor == len(text):
                break
            char = text[cursor]
            if char in "\"'":
                value, cursor = anchors._decode_lua_string(text, cursor)
                tokens.append(('string', value))
            elif anchors._long_bracket_opening(text, cursor):
                value, cursor = anchors._decode_lua_long_bracket(text, cursor)
                tokens.append(('string', value))
            else:
                found = syntax.match(text, cursor)
                value = found.group()
                tokens.append(('syntax', value))
                cursor += len(value)
        i = 0
        while i < len(tokens):
            if tokens[i] == ('syntax', ';'):
                i += 1
                continue
            tail = tokens[i:i+6]
            if (len(tail) >= 4 and tail[0] in [('syntax', 'forceFontPackage'), ('syntax', 'locale')]
                    and tail[1] == ('syntax', '(') and tail[2][0] == 'string'
                    and re.fullmatch(r'[a-zA-Z0-9_-]+', tail[2][1]) and tail[3] == ('syntax', ')')):
                i += 4
            elif (len(tail) >= 6 and tail[0:2] == [('syntax', 'setFlag'), ('syntax', '(')]
                    and tail[2] in [('string', 'break_text_all_character'), ('string', 'ego_always_prefix')]
                    and tail[3] == ('syntax', ',') and tail[4] in [('syntax', 'true'), ('syntax', 'false')]
                    and tail[5] == ('syntax', ')')):
                i += 6
            else:
                literals = [v for k, v in tokens[i:] if k == 'string']
                if literals:
                    return literals
                raise FullReviewError('unsupported/dynamic loading-only bytes')
        return []
    except (UnicodeError, anchors.InputError) as error:
        raise FullReviewError('unsupported/dynamic loading-only bytes') from error


def validate_loading_only(manifest, supplement, mapping):
    if mapping.get('language_literals') != []:
        raise FullReviewError('copy language literals need review unit mappings')
    if loading_literals(loading_bytes(manifest, supplement, mapping)):
        raise FullReviewError('loading-only actual language literals need review unit mappings')


def closure_check(manifest, directory, ledger, live, completed):
    """Validate a host-frozen conservation map against actual candidate Lua bytes.

    No flag alone closes the denominator: every occurrence/supplement has a
    unique disposition, evidence and actual runtime chain. Language mappings
    must refer to adjudicated current units with matching effective text.
    """
    path = Path(directory) / 'closure.json'
    if not path.exists():
        return None
    closure = read(path)
    if (closure.get('round_id') != ledger['round_id'] or
            closure.get('inventory_sha256') != sha(ordinary(Path(directory) / 'inventory.json'))):
        raise FullReviewError('closure round/inventory drift')
    evidence_files(manifest, closure.get('evidence'))
    from .release_candidate import verify_candidate, isolated
    candidate = isolated(manifest, closure['candidate_path'], 'release-candidate')
    seal = verify_candidate(candidate)
    if closure.get('candidate_sha256') != sha(ordinary(candidate / 'candidate.json')):
        raise FullReviewError('closure candidate drift')
    # Candidate must represent current input bytes, including procedural copy content.
    from .release_candidate import input_hashes
    if seal.get('input_hashes') != input_hashes(manifest):
        raise FullReviewError('closure current candidate input drift')
    runtime = closure.get('runtime_keys')
    if not isinstance(runtime, list):
        raise FullReviewError('runtime denominator not a list')
    chains = {}
    engine_runtime = LuaRuntime(manifest)
    reader = FixedReader()
    full_chain = None
    replay_cache = {}
    for mapping in runtime:
        key = mapping.get('key')
        if (not isinstance(key, list) or len(key) != 2 or not isinstance(key[0], str) or
                key[1] is not None and not isinstance(key[1], str) or tuple(key) in chains):
            raise FullReviewError('invalid/duplicate final runtime key')
        layers = mapping.get('layers')
        if not isinstance(layers, list) or not layers:
            raise FullReviewError('runtime key missing actual load chain')
        effective = None
        actual_layers = []
        for layer in layers:
            if layer.get('language') != 'zh_hans' or not layer.get('layer'):
                raise FullReviewError('runtime layer language/identity missing')
            relative = identity.normalize_relative_path(layer['path'])
            if layer.get('origin') == 'candidate':
                raw = ordinary(safe_path(candidate, relative))
            elif layer.get('origin') == 'official':
                repository = manifest.repositories[layer['repository']]
                if repository.visibility != 'public' or layer['commit'] != repository.commit:
                    raise FullReviewError('official runtime source is not fixed manifest input')
                raw, _ = reader.pinned(manifest.repository_path(layer['repository']), layer['commit'], relative)
            else:
                raise FullReviewError('runtime origin must be actual candidate or official source')
            digest = sha(raw)
            if digest != layer['sha256']:
                raise FullReviewError('runtime layer bytes drift')
            if mapping.get('kind') == 'language-bytes':
                # Actual procedural/source-only runtime text is not parsed as t().
                # Host supplies execution evidence; byte anchors prove exact text.
                evidence_files(manifest, mapping.get('evidence'))
                anchor = layer.get('target_anchor', {})
                start, end = anchor.get('start'), anchor.get('end')
                text = mapping.get('target')
                if (not isinstance(text, str) or type(start) is not int or type(end) is not int
                        or not 0 <= start <= end <= len(raw) or raw[start:end] != text.encode('utf-8')):
                    raise FullReviewError('runtime language byte anchor drift')
                effective = (layer, {field: mapping.get(field) for field in ('target', 'args_order', 'special')})
                continue
            actual_layers.append((layer, raw))
        if mapping.get('kind') != 'language-bytes':
            if closure.get('runtime_semantics') != I18N_SOURCE:
                raise FullReviewError('closure fixed I18N capability binding missing/drift')
            chain_identity = canonical(layers)
            if full_chain is not None and full_chain != chain_identity:
                raise FullReviewError('runtime keys must share one actual ordered load chain')
            full_chain = chain_identity
            if len({layer['layer'] for layer in layers}) != len(layers):
                raise FullReviewError('duplicate runtime load layer identity')
            query = mapping.get('query')
            if not isinstance(query, dict) or query.get('source') != key[0] or normalized_query_tag(query) != normalized_key_tag(key[1]):
                raise FullReviewError('runtime query source/method/tag does not bind runtime key')
            query_identity = canonical(query)
            if not replay_cache:
                queries = [m.get('query') for m in runtime if m.get('kind') != 'language-bytes']
                if any(not isinstance(q, dict) for q in queries):
                    raise FullReviewError('runtime query missing')
                replay_cache.update(zip((canonical(q) for q in queries),
                                        i18n_effective(engine_runtime, actual_layers, queries)))
            result = replay_cache[query_identity]
            registration = result.get('effective_registration')
            if canonical(mapping.get('effective_registration')) != canonical(registration):
                raise FullReviewError('runtime effective registration mismatch')
            if 'formatted' in result and mapping.get('formatted') != result['formatted']:
                raise FullReviewError('runtime actual formatted output mismatch')
            effective = ({'layer': result['effective_layer']}, result)
        if effective is None or mapping.get('effective_layer') != effective[0]['layer']:
            raise FullReviewError('runtime effective layer not demonstrated')
        target = effective[1]
        for field in ('target', 'args_order', 'special'):
            if canonical(mapping.get(field)) != canonical(target.get(field)):
                raise FullReviewError('runtime effective semantics mismatch')
        chains[tuple(key)] = mapping
    units = closure.get('occurrences')
    supplements = closure.get('supplements')
    if not isinstance(units, list) or not isinstance(supplements, list):
        raise FullReviewError('closure occurrence/supplement maps missing')
    by_unit = {r['unit_id']: r for r in units}
    by_sup = {r['supplement_id']: r for r in supplements}
    if (len(by_unit) != len(units) or set(by_unit) != set(live) or
            len(by_sup) != len(supplements) or set(by_sup) != {s['supplement_id'] for s in ledger['supplements']}):
        raise FullReviewError('conservation map missing/duplicate/extra item')
    used_runtime = set()
    for unit_id, unit in live.items():
        mapping = by_unit[unit_id]
        evidence_files(manifest, mapping.get('evidence'))
        if (mapping.get('revision_key'), mapping.get('guard'), mapping.get('disposition')) != (
                unit['revision_key'], unit['guard'], unit['disposition']):
            raise FullReviewError('closure current occurrence identity/fate mismatch')
        if unit['disposition'] == 'release-required':
            if unit_id not in completed['A']:
                raise FullReviewError('closure missing adjudicated current A/B')
            key = tuple(unit['runtime_key'])
            if mapping.get('runtime_key') != list(key) or key not in chains:
                raise FullReviewError('occurrence runtime mapping missing')
            # Shadowed duplicate occurrences stay reviewed but disclose the effective target.
            if mapping.get('effective_target') != chains[key]['target']:
                raise FullReviewError('occurrence effective text/layer mismatch')
            used_runtime.add(key)
        elif not mapping.get('reason'):
            raise FullReviewError('Boot/outside-release disposition lacks host reason')
    for supplement in ledger['supplements']:
        mapping = by_sup[supplement['supplement_id']]
        evidence_files(manifest, mapping.get('evidence'))
        if mapping.get('supplement_sha256') != sha(canonical(supplement)):
            raise FullReviewError('supplement current identity drift')
        fate = mapping.get('disposition')
        if fate == 'outside-release-followup' and (
                supplement['component'] in RELEASE | {'boot', 'release-addon'} or
                supplement['kind'] == 'retained-layer'):
            raise FullReviewError('outside-release-followup requires an outside-release component/layer')
        if fate in {'unreachable', 'outside-release-followup', 'loading-only'}:
            if not mapping.get('reason') or mapping.get('source_verified') is not True:
                raise FullReviewError('supplement exclusion lacks source proof')
            if fate == 'loading-only' and supplement['kind'] not in {'copy', 'official-inheritance', 'retained-layer', 'wrapper-addon'} and supplement['component'] != 'boot':
                raise FullReviewError('source-visible language cannot silently become loading-only')
            if (fate == 'loading-only' and supplement['kind'] in {'copy', 'retained-layer', 'wrapper-addon'}
                    and mapping.get('language_literals') != []):
                raise FullReviewError('copy language literals need review unit mappings')
            if (fate == 'loading-only' and supplement['component'] != 'boot' and
                    supplement['kind'] in {'copy', 'retained-layer', 'wrapper-addon'}):
                validate_loading_only(manifest, supplement, mapping)
            if fate == 'loading-only' and supplement['kind'] == 'official-inheritance' and supplement['component'] != 'boot':
                raise FullReviewError('non-Boot official language requires review or proven shadow')
            if fate == 'unreachable':
                proof = mapping.get('source_proof')
                if not isinstance(proof, list) or not proof:
                    raise FullReviewError('unreachable exclusion needs concrete source proof')
                for spec in proof:
                    fact = source_file(manifest, spec)
                    start, end = spec.get('line_start'), spec.get('line_end')
                    if (type(start) is not int or type(end) is not int or
                            not 1 <= start <= end <= len(fact['content'].splitlines()) or end-start >= 200):
                        raise FullReviewError('unreachable source proof needs bounded line anchors')
            continue
        if fate not in {'release-required', 'shadowed'} or not mapping.get('review_units'):
            raise FullReviewError('supplement language unit unresolved')
        key = tuple(mapping.get('runtime_key', []))
        if key not in chains:
            raise FullReviewError('supplement runtime key unresolved')
        reviewed = mapping['review_units']
        bound = [u['unit_id'] for u in live.values() if supplement['supplement_id'] in u.get('supplement_origins', [])]
        if fate == 'shadowed':
            if supplement['kind'] != 'official-inheritance' or not mapping.get('reason') or mapping.get('source_verified') is not True:
                raise FullReviewError('shadow exclusion needs specific source proof')
            record = supplement['record']
            registration = mapping.get('shadowed_registration')
            chain = chains[key]
            if (not isinstance(registration, dict) or registration == chain.get('effective_registration') or
                    not any(layer['origin'] == 'official' and layer.get('commit') == supplement['commit'] and
                            layer['path'] == supplement['public_source_path'] and layer['sha256'] == supplement['sha256'] and
                            layer['layer'] == registration.get('layer') for layer in chain['layers']) or
                    record.get('source') != key[0] or registration.get('source_tag') != record.get('source_tag') or
                    normalized_key_tag(record.get('source_tag')) != normalized_key_tag(key[1])):
                raise FullReviewError('official shadow not bound to actual reviewed load chain')
            layer = next(l for l in chain['layers'] if l['layer'] == registration['layer'])
            raw, _ = reader.pinned(manifest.repository_path(layer['repository']), layer['commit'], layer['path'])
            document = LocaleLoader(engine_runtime).load_bytes(raw, logical_path=layer['path'])
            ordinal = registration.get('ordinal')
            if (type(ordinal) is not int or not 1 <= ordinal <= len(document.translations) or
                    document.translations[ordinal - 1] != record):
                raise FullReviewError('shadow registration does not identify actual official row')
        if fate != 'shadowed' and bound and reviewed != bound:
            raise FullReviewError('supplement must consume its bound language unit')
        if any(unit not in completed['A'] for unit in reviewed):
            raise FullReviewError('supplement missing adjudicated language coverage')
        # No merely related unit may stand in for an inherited or missing translation.
        if not any(tuple(live[u]['runtime_key']) == key and
                   all(live[u]['occurrence'][field] == chains[key][field] for field in ('target', 'args_order', 'special')) for u in reviewed):
            raise FullReviewError('supplement review does not bind actual effective text')
        record = supplement.get('record')
        if record and record.get('source') != key[0]:
            raise FullReviewError('supplement source key mismatch')
        used_runtime.add(key)
    if used_runtime != set(chains):
        raise FullReviewError('final runtime denominator has unaccounted keys')
    for field in ('retained_layers', 'dynamic_contexts', 'relations', 'successors'):
        summary = closure.get(field)
        if not isinstance(summary, dict) or summary.get('status') != 'closed':
            raise FullReviewError(f'{field} not host-closed')
        evidence_files(manifest, summary.get('evidence'))
    # Each proof independently binds exact candidate and durable installed operation.
    readiness = closure.get('release_readiness', {})
    ready = release_readiness(manifest, candidate, readiness)
    return {'final_unit_denominator': sum(u['disposition'] == 'release-required' for u in live.values()),
            'final_runtime_denominator': len(chains), 'release_ready': bool(ready)}
