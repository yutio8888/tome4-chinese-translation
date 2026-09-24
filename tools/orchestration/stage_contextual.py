#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 checkpoint 的 contextual refs 建 .ai/task/<batch>-contextual-NNN/ 布局。

用法：python3 -B tools/orchestration/stage_contextual.py <batch-id> [--out /tmp/ctx.json]
"""
import json, sys, pathlib, datetime, argparse, os, hashlib, tempfile
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _orch


CKPT = pathlib.Path('.artifacts/i18n/production-review-v2-lite/active-batch.json')


def canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def _write_new(path, raw):
    # Publish a complete file without replacing an existing candidate, state, or report.
    # Task file temporaries live beside the task directory, so an interrupted write
    # cannot make an otherwise recoverable partial task appear to contain raw output.
    parent = path.parent.parent if path.name in {'STATE.json', 'CONTEXTUAL-ENVELOPE-final-full.json'} else path.parent
    fd, name = tempfile.mkstemp(prefix=f'.{path.name}.stage-', dir=parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
        os.link(name, path)
    finally:
        os.unlink(name)


def _initial_state(cp, task, now):
    return {
        'schema_version': 5, 'task_id': task, 'mode': 'review_only', 'state': 'REVIEW',
        'review_phase': 'REVIEW', 'cycle': 0, 'max_cycles': 3,
        'review_contracts': ['translation_contextual_v2'],
        'completed_review_contracts': [], 'pending_review_contracts': [],
        'child_dispatches': [], 'review_records': [], 'senior_review_records': [],
        'deferred_findings': [], 'open_accepted_findings': [],
        'baseline': {'commit': cp['base_commit']}, 'orchestration_transport': 'cli',
        'workspace_id': _orch.workspace_id(), 'final_validation_passed': False,
        'last_error': None, 'wait': None, 'updated_at': now, 'change_class': 'standard',
        'candidate_author_agent_id': None, 'orchestrator_agent_id': None,
    }


def _validate_frozen_sources(cp, workset, checkout):
    from orchestration import build_evidence_pack as source_facts
    raw = source_facts.ordinary_bytes(workset)
    ws, _ = source_facts.validate_workset(raw, cp)
    workset_sha = hashlib.sha256(raw).hexdigest()
    ashes = [ver for ver in ws['source_verification'] if ver['component'] == 'ashes-urhrok']
    for ver in ashes:
        path = checkout / source_facts.public_path(ver['public_source_path'])
        if hashlib.sha256(source_facts.ordinary_bytes(path)).hexdigest() != ver['source_file_sha256']:
            raise ValueError(f'Ashes workset source SHA mismatch: {path}')
    seen_facts = 0
    seen_ashes = 0
    for ref in cp['contextual']:
        envelope = json.loads(source_facts.ordinary_bytes(ref['input_path']))
        if hashlib.sha256(canon(envelope)).hexdigest() != ref['input_sha256']:
            raise ValueError('frozen contextual input SHA differs')
        for item in envelope['payload']['bounded_context']:
            seen_facts += 1
            context = item['context']
            marker = source_facts.CONTEXT_MARKER
            if context.count(marker) != 1:
                raise ValueError('frozen source facts missing or ambiguous')
            fact = json.loads(context.split(marker, 1)[1])
            if fact['binding']['source_workset_sha256'] != workset_sha:
                raise ValueError('frozen source workset SHA differs')
            if fact['fact']['source_component'] == 'ashes-urhrok':
                seen_ashes += 1
                location = f' source_checkout={checkout} (local evidence location; source/commit unpinned)'
                if location not in context.split(marker, 1)[0]:
                    raise ValueError('frozen Ashes checkout differs')
    if not seen_facts or (ashes and not seen_ashes):
        raise ValueError('frozen source facts do not cover the workset')


def _existing_stage(d, envelope_raw, expected_state):
    """Only continue an untouched, unstarted stage for the same frozen input."""
    if d.is_symlink() or not d.is_dir():
        raise ValueError(f'contextual task is not ordinary directory: {d}')
    allowed = {'CONTEXTUAL-ENVELOPE-final-full.json', 'STATE.json'}
    if any(p.name not in allowed or p.is_symlink() or not p.is_file() for p in d.iterdir()):
        raise ValueError(f'contextual task has non-stage contents: {d}')
    candidate = d / 'CONTEXTUAL-ENVELOPE-final-full.json'
    if candidate.exists() and candidate.read_bytes() != envelope_raw:
        raise ValueError(f'contextual staged candidate differs: {candidate}')
    state_path = d / 'STATE.json'
    if state_path.exists():
        state = json.loads(state_path.read_bytes())
        if (not isinstance(state, dict) or not isinstance(state.get('updated_at'), str) or
            {k: v for k, v in state.items() if k != 'updated_at'} !=
            {k: v for k, v in expected_state.items() if k != 'updated_at'}):
            raise ValueError(f'contextual task has started or drifted: {d}')
        if not candidate.exists():
            raise ValueError(f'contextual state exists without candidate: {d}')
    return candidate.exists(), state_path.exists()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch')
    parser.add_argument('--out', default='/tmp/ctx.json')
    parser.add_argument('--refreeze-id')
    parser.add_argument('--source-workset', type=pathlib.Path)
    parser.add_argument('--ashes-checkout', type=pathlib.Path)
    args = parser.parse_args()
    batch = args.batch
    out = args.out if args.out != '/tmp/ctx.json' or not args.refreeze_id else f'/tmp/ctx-{batch}-refreeze-{args.refreeze_id}.json'
    current = json.loads(CKPT.read_text())
    if current['batch_id'] != batch:
        raise ValueError(f'active batch differs: {current["batch_id"]}')
    report = pathlib.Path(out)
    suffix = f'-refreeze-{args.refreeze_id}' if args.refreeze_id else None
    already_frozen = bool(suffix and current.get('contextual') and all(
        r.get('task_id') == f'{batch}-contextual-{i:03d}{suffix}'
        for i, r in enumerate(current['contextual'])))
    if (report.exists() or report.is_symlink()) and not already_frozen:
        raise FileExistsError(f'contextual stage report already exists: {out}')
    for parent in report.parents:
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise ValueError(f'contextual stage report parent is not ordinary directory: {parent}')
    if not report.parent.is_dir():
        raise ValueError(f'contextual stage report parent does not exist: {report.parent}')
    if args.refreeze_id:
        if args.source_workset is None or args.ashes_checkout is None:
            parser.error('refreeze requires --source-workset and --ashes-checkout')
        checkout = args.ashes_checkout.resolve(strict=True)
        if checkout != args.ashes_checkout or not checkout.is_dir():
            parser.error('Ashes checkout must be a canonical absolute directory')
        if already_frozen:
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
            _validate_frozen_sources(current, args.source_workset, checkout)
        else:
            os.environ['TOME_DLC_ASHES_ROOT'] = str(checkout)
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
            from i18nlib import production_review_v2_lite_batch as batch_module
            batch_module.contextual_export(
                pathlib.Path.cwd(), source_workset=args.source_workset,
                refreeze_id=args.refreeze_id, source_checkout=checkout)
    cp = json.loads(CKPT.read_text())
    assert cp['batch_id'] == batch, cp['batch_id']
    if already_frozen and (cp['phase'] != 'deep_ready' or not cp['contextual']):
        raise ValueError('refreeze checkpoint is not ready')
    staged = []
    for i, r in enumerate(cp['contextual']):
        task = r['task_id']
        expected_task = f'{batch}-contextual-{i:03d}{suffix or ""}'
        if task != expected_task:
            raise ValueError('invalid contextual task binding')
        d = pathlib.Path('.ai/task') / task
        if (d.exists() or d.is_symlink()) and not already_frozen:
            raise FileExistsError(f'contextual task already exists: {d}')
        input_path = pathlib.Path(r['input_path'])
        raw = input_path.read_bytes()
        env = json.loads(raw)
        if (hashlib.sha256(raw).hexdigest() != r['input_sha256'] or
            env['candidate_identity'] != r['candidate_identity']):
            raise ValueError('contextual candidate identity drift')
        envelope_raw = canon(env)
        expected_state = _initial_state(cp, task, '')
        present = _existing_stage(d, envelope_raw, expected_state) if d.exists() or d.is_symlink() else (False, False)
        staged.append((d, env, envelope_raw, present))
    rows = [{'task_id': r['task_id'], 'dispatch_id': f'full-{i:03d}',
             'candidate_identity': r['candidate_identity'],
             'input_path': str(staged[i][0] / 'CONTEXTUAL-ENVELOPE-final-full.json'),
             'entries': len(staged[i][1]['payload']['ordered_revision_keys'])}
            for i, r in enumerate(cp['contextual'])]
    if report.exists() or report.is_symlink():
        if report.is_symlink() or not report.is_file() or json.loads(report.read_bytes()) != rows:
            raise ValueError(f'contextual stage report differs: {report}')
    for i, r in enumerate(cp['contextual']):
        run = f'{i:03d}'
        task = r['task_id']
        d, env, envelope_raw, (candidate_exists, state_exists) = staged[i]
        if not d.exists():
            d.mkdir(parents=True, exist_ok=False)
        p = d / 'CONTEXTUAL-ENVELOPE-final-full.json'
        if not candidate_exists:
            _write_new(p, envelope_raw)
        n = len(env['payload']['ordered_revision_keys'])
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        state_raw = json.dumps(_initial_state(cp, task, now), ensure_ascii=False, indent=1, sort_keys=True).encode('utf-8')
        if not state_exists:
            _write_new(d / 'STATE.json', state_raw)
        print(task, 'entries=', n)
    if not report.exists():
        _write_new(report, json.dumps(rows, ensure_ascii=False, indent=1).encode('utf-8'))


main()
