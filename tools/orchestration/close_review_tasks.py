#!/usr/bin/env python3
"""Publish a complete accepted stage only after strict checks and all archives.

All original attempts stay in the journal/STATE. Validate a prospective workspace
with the existing consumer before publishing records and, last, terminal STATE.
No real transport action occurs here; archive budget/confirmation belongs to the
notification-driven lifecycle entry point.
"""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_lifecycle as lifecycle
import _orch
import ai_state_check


def publish(journal, keys, rawdir):
    rows = journal.stage([journal.get(k) for k in keys])
    first = rows[0]
    task, contract = first['task_id'], first['purpose']
    taskdir = Path('.ai/task') / task
    revdir = Path('.ai/reviews') / task
    statepath = taskdir / 'STATE.json'
    for directory in (taskdir, revdir):
        for relative in (directory, *directory.parents):
            target = journal.root / relative
            lifecycle.require(not target.is_symlink(), 'publication directory must not be a symlink')
    journal.save()  # interrupted mirror recovery; never rebuild child history
    state = lifecycle.read(journal.root / statepath)
    records, output = [], {}
    for row in rows:
        raw_path = str(revdir / ('raw-' + row['dispatch_id'] + '.txt'))
        raw = (journal.root / row['raw_output_path']).read_bytes()
        output[raw_path] = raw
        rec = {k: deepcopy(row[k]) for k in ('agent_id', 'candidate_identity', 'dispatch_id', 'input_path',
               'lineage_verified', 'parent_agent_id', 'purpose', 'workspace_id', 'labels', 'attempt',
               'cycle', 'review_kind')}
        rec.update(task_id=task, review_contract=contract, review_phase='REVIEW', reviewer_role='REVIEWER',
                   status='completed', raw_output_path=raw_path, raw_output_sha256=lifecycle.digest(raw))
        if row.get('lane'):
            rec['lane'] = deepcopy(row['lane'])
        record_path = str(revdir / (row['dispatch_id'] + '.json'))
        output[record_path] = lifecycle.surface.canonical_bytes(rec)
        records.append(record_path)
    lifecycle.require(not state.get('review_records') or state['review_records'] == records,
                      'existing acceptance records differ; do not overwrite history')
    state.update(state='DONE', completed_review_contracts=[contract], pending_review_contracts=[],
                 review_records=records, final_validation_passed=True, updated_at=lifecycle.now())
    if contract == lifecycle.SURFACE:
        draft = str(taskdir / 'SURFACE-SCREEN-INPUT-DRAFT.json')
        artifacts = {draft: lifecycle.digest((journal.root / draft).read_bytes())}
        for row in rows:
            artifacts[row['input_path']] = row['input_sha256']
            path = str(revdir / ('raw-' + row['dispatch_id'] + '.txt'))
            artifacts[path] = lifecycle.digest(output[path])
        # Do not delete carry-over or other bindings to force a passing terminal.
        if state.get('surface_carry_over_path'):
            path = state['surface_carry_over_path']
            artifacts[path] = lifecycle.digest((journal.root / path).read_bytes())
        state.update(change_class='translation_workflow', surface_screen_input_path=draft,
                     surface_evidence_binding=dict(algorithm='surface-evidence-binding/1', task_id=task,
                                                   terminal='whole_screen', artifact_sha256=artifacts))
    else:
        state['contextual_reviewers'] = [{k: row[k] for k in
            ('agent_id', 'candidate_identity', 'dispatch_id', 'input_path', 'purpose', 'role')} for row in rows]
    # Check original paths before copying; copytree must not erase the consumer's
    # ordinary-file/containment refusal semantics. Also guard publication targets.
    inputs = {str(statepath), *artifacts} if contract == lifecycle.SURFACE else {str(statepath)}
    inputs.update(r['input_path'] for r in journal.rows if r['task_id'] == task)
    for path in inputs:
        if path not in output:
            ai_state_check._ordinary_workspace_file(path, 'publication input', root=journal.root)
    for path in output:
        target = journal.root / path
        lifecycle.require(target.resolve().is_relative_to(journal.root), 'publication path escapes workspace')
        if target.exists() or target.is_symlink():
            ai_state_check._ordinary_workspace_file(path, 'publication output', root=journal.root)
    # Confined prospective workspace: no queue, no Git scan, no mutable consumer seam.
    with tempfile.TemporaryDirectory(prefix='review-close-') as tmp:
        stage = Path(tmp)
        shutil.copytree(journal.root / taskdir, stage / taskdir, symlinks=True)
        if (journal.root / revdir).exists():
            shutil.copytree(journal.root / revdir, stage / revdir, symlinks=True)
        for row in journal.rows:
            if row['task_id'] == task:
                ip = row['input_path']
                lifecycle.immutable(stage / ip, (journal.root / ip).read_bytes())
        for path, raw in output.items():
            lifecycle.immutable(stage / path, raw)
        _orch.write_json_atomic(stage / statepath, state)
        result = ai_state_check.check_state(stage / statepath, target='DONE', workspace_root=stage)
        lifecycle.require(result.exit_code == 0 and result.outcome == 'DONE_VERIFIED',
                          f'prospective consumer rejected: {result.outcome}: {result.detail}')
    # Idempotent per-file writes; interruption before STATE leaves no accepted stage.
    # The final STATE is the atomic publication pointer for all four records.
    for path, raw in output.items():
        lifecycle.immutable(journal.root / path, raw)
    _orch.write_json_atomic(journal.root / statepath, state)
    for row in rows:
        lifecycle.immutable(Path(rawdir) / (row['dispatch_id'] + '.json'),
                            output[str(revdir / ('raw-' + row['dispatch_id'] + '.txt'))])
    return result


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    lifecycle.require(len(args) == 4, 'usage: close_review_tasks.py surface|contextual spec children rawdir')
    kind, specpath, childpath, rawdir = args
    lifecycle.require(kind in ('surface', 'contextual'), 'unknown kind')
    journal = lifecycle.Journal(childpath)
    spec = lifecycle.read(specpath)
    tasks = ({task: [dict(lane, task_id=task) for lane in v['lanes']] for task, v in spec.items()}
             if kind == 'surface' else {r['task_id']: [r] for r in spec})
    for task, members in tasks.items():
        for member in members:
            row = journal.get(journal.key(member))
            for key in ('candidate_identity', 'input_path'):
                lifecycle.require(row[key] == member[key], f'close spec changed {key}')
            lifecycle.require(row['purpose'] == (lifecycle.SURFACE if kind == 'surface' else lifecycle.CONTEXTUAL),
                              'close contract mismatch')
        result = publish(journal, [journal.key(r) for r in members], rawdir)
        print(f'{task}: {result.outcome}: {result.detail}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, lifecycle.contextual.ContractError,
            lifecycle.contextual.InputError, lifecycle.surface.ContractError, lifecycle.surface.InputError) as error:
        print(f'CLOSE_FAILED: {error}', file=sys.stderr)
        sys.exit(1)
