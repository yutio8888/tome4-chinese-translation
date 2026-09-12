#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build canonical adjudications from host decisions, never from model verdicts.

The two-position CLI retains the historical ENGINE checkout and output overwrite
semantics. The contextual chain uses frozen inputs and a SHA-bound source root.
Importing this module performs no preflight, source reads or output writes.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from i18nlib import production_review_v2_lite_batch as B
from i18nlib import production_review as wp1
from orchestration import build_evidence_pack as facts

CONTRACT = {'surface': 'translation_surface_screen_v1', 'contextual': 'translation_contextual_v2'}
ENGINE = Path('/workspace/t-engine4')


def fresh_output(root, output, *, create=False):
    """Check ordinary parents and a fresh name within the dedicated scratch tree.

    Empty directories created here may survive failure; only our own temporary
    file is removed. Publishing uses link, never replace, so a racing name wins.
    """
    path = Path(output).absolute()
    boundary = Path(root).absolute() / '.artifacts/i18n/adjudication-chain'
    if '..' in path.parts or not path.is_relative_to(boundary) or path == boundary:
        raise ValueError('output must be a fresh file below root/.artifacts/i18n/adjudication-chain/')
    for parent in reversed(path.parents):
        if not parent.exists() and not parent.is_symlink() and create:
            parent.mkdir(exist_ok=True)
        try:
            mode = parent.lstat().st_mode
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(mode):
            raise ValueError(f'output parent is not an ordinary directory: {parent}')
    if os.path.lexists(path):
        raise ValueError(f'output already occupied: {path}')
    return path


def publish_fresh(root, output, raw):
    path = fresh_output(root, output, create=True)
    fd, temporary = tempfile.mkstemp(prefix='.adjudication-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        fresh_output(root, path)
        os.link(temporary, path)  # atomic publication without clobbering a rival
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        os.unlink(temporary)


def freeze_inputs(spec_path):
    """Read each decision/workset once. These bytes, not later disk edits, win."""
    spec_raw = facts.ordinary_bytes(spec_path)
    spec = facts.strict_json(spec_raw)
    if (not isinstance(spec, dict) or set(spec) != {'workset', 'decisions'} or
            not isinstance(spec['workset'], str) or not spec['workset'] or
            not isinstance(spec['decisions'], dict)):
        raise ValueError('spec requires workset path and decisions object')
    for key, value in spec['decisions'].items():
        if not re.fullmatch(r'[0-9a-f]{10}\|(surface|contextual)', key):
            raise ValueError(f'invalid decision key: {key}')
        if (not isinstance(value, dict) or
                set(value) != {'disposition', 'repair_required', 'conclusion'} or
                not isinstance(value['disposition'], str) or
                value['disposition'] not in {'confirmed', 'pending', 'advisory', 'refuted'} or
                type(value['repair_required']) is not bool or
                not isinstance(value['conclusion'], str) or
                (value['disposition'] != 'confirmed' and value['repair_required'])):
            raise ValueError(f'invalid decision disposition/repair/conclusion: {key}')
    raw = facts.ordinary_bytes(spec['workset'])
    ws = facts.strict_json(raw)
    if (not isinstance(ws, dict) or not isinstance(ws.get('entries'), list) or
            any(not isinstance(row, dict) or not isinstance(row.get('entry_revision_identity'), str)
                for row in ws['entries'])):
        raise ValueError('invalid workset entries')
    # Structural/unique/SHA checks now; actual checkpoint binding is under the
    # generator's lock after contextual-import, without another projection here.
    structural = {key: ws.get(key) for key in ('batch_id', 'catalog_id', 'base_commit')}
    structural.update(selected=[row['entry_revision_identity'] for row in ws['entries']],
                      entry_snapshots=ws['entries'])
    facts.validate_workset(raw, structural)
    return spec, raw


def _assemble(checkpoint, spec, verifications, source_root, *, strict):
    observations = B._accepted_observations(checkpoint)
    want = {}
    for key, value in spec['decisions'].items():
        rev, kind = key.split('|')
        want[(rev, CONTRACT[kind])] = value
    cache, out, missing = {}, [], []
    for observation in observations:
        key = (observation['entry_revision_identity'][:10], observation['contract'])
        if key not in want:
            missing.append(key)
            continue
        value = want.pop(key)
        snapshot = None
        if value['disposition'] == 'confirmed':
            verification = verifications[observation['entry_revision_identity']]
            rel = verification['public_source_path']
            if strict:
                facts.public_path(rel)
            if rel not in cache:
                path = Path(source_root) / rel
                raw = facts.ordinary_bytes(path) if strict else path.read_bytes()
                cache[rel] = {'content': raw.decode('utf-8'), 'sha256': hashlib.sha256(raw).hexdigest()}
            snapshot = cache[rel]
            if strict and snapshot['sha256'] != verification['source_file_sha256']:
                raise ValueError(f'{rel}: source SHA mismatch with frozen workset')
        out.append({'conclusion': value['conclusion'], 'disposition': value['disposition'],
                    'entry_revision_identity': observation['entry_revision_identity'],
                    'evidence_commit': None, 'evidence_path': None, 'evidence_snapshot': snapshot,
                    'observation_contract': observation['contract'],
                    'observation_identity': observation['observation_identity'],
                    'observation_sha256': hashlib.sha256((observation['observation'] or '').encode()).hexdigest(),
                    'repair_required': value['repair_required'] if strict else bool(value['repair_required'])})
    if missing:
        raise ValueError(f'spec 缺这些观察的裁决：{missing}')
    if want:
        raise ValueError(f'spec 里有多余、对不上任何观察的裁决：{sorted(want)}')
    return out


def generate(root, spec_path, output, *, source_root=None, frozen=None):
    """Independently lock/preflight/read accepted observations/build/publish.

    No carry scope here: the caller may share only its projection, never a
    checkpoint, observation list or database connection with this operation.
    """
    strict = frozen is not None
    with B.queue.writer_lock(root):
        checkpoint = B.preflight(root)
        if checkpoint is None:
            raise ValueError('adjudication generation requires an active batch')
        if strict:
            if checkpoint['phase'] != 'deep_collected':
                raise ValueError('chain generation requires collected contextual results')
            if source_root is None:
                raise ValueError('chain generation requires explicit source-root')
            fresh_output(root, output)
            spec, workset_raw = frozen
            _, verifications = facts.validate_workset(workset_raw, checkpoint)
        else:
            spec = json.loads(Path(spec_path).read_text())
            ws = json.loads(Path(spec['workset']).read_text())
            verifications = {v['entry_revision_identity']: v for v in ws['source_verification']}
        out = _assemble(checkpoint, spec, verifications,
                        ENGINE if source_root is None else source_root, strict=strict)
        raw = wp1.canonical_bytes({'batch_id': checkpoint['batch_id'], 'decisions': out})
        if strict:
            publish_fresh(root, output, raw)
        else:
            Path(output).write_bytes(raw)
    print(f'{len(out)} 条裁决', dict(Counter(d['disposition'] for d in out)),
          '| repair', sum(1 for d in out if d['repair_required']))
    return raw


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        raise SystemExit('usage: make_adjudication.py <spec.json> <out.json>')
    try:
        generate(Path('.'), args[0], args[1])
    except (OSError, ValueError, KeyError, TypeError, wp1.ProductionReviewError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
