#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 checkpoint 的 contextual refs 建 .ai/task/<batch>-contextual-NNN/ 布局。

用法：python3 -B tools/orchestration/stage_contextual.py <batch-id> [--out /tmp/ctx.json]
"""
import json, sys, pathlib, datetime

CKPT = pathlib.Path('.artifacts/i18n/production-review-v2-lite/active-batch.json')


def canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def main():
    batch = sys.argv[1]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/tmp/ctx.json'
    cp = json.loads(CKPT.read_text())
    assert cp['batch_id'] == batch, cp['batch_id']
    rows = []
    for i, r in enumerate(cp['contextual']):
        run = f'{i:03d}'
        task = f'{batch}-contextual-{run}'
        d = pathlib.Path('.ai/task') / task
        d.mkdir(parents=True, exist_ok=True)
        env = json.loads(pathlib.Path(r['input_path']).read_text())
        p = d / 'CONTEXTUAL-ENVELOPE-final-full.json'
        p.write_bytes(canon(env))
        n = len(env['payload']['ordered_revision_keys'])
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        (d / 'STATE.json').write_text(json.dumps({
            'schema_version': 5, 'task_id': task, 'mode': 'review_only', 'state': 'REVIEW',
            'review_phase': 'REVIEW', 'cycle': 0, 'max_cycles': 3,
            'review_contracts': ['translation_contextual_v2'],
            'completed_review_contracts': [], 'pending_review_contracts': [],
            'child_dispatches': [], 'review_records': [], 'senior_review_records': [],
            'deferred_findings': [], 'open_accepted_findings': [],
            'baseline': {'commit': cp['base_commit']}, 'orchestration_transport': 'cli',
            'workspace_id': 'wks_420314270844170b', 'final_validation_passed': False,
            'last_error': None, 'wait': None, 'updated_at': now, 'change_class': 'standard',
            'candidate_author_agent_id': None, 'orchestrator_agent_id': None,
        }, ensure_ascii=False, indent=1, sort_keys=True))
        rows.append({'task_id': task, 'dispatch_id': f'full-{run}',
                     'candidate_identity': r['candidate_identity'],
                     'input_path': str(p), 'entries': n})
        print(task, 'entries=', n)
    json.dump(rows, open(out, 'w'), ensure_ascii=False, indent=1)


main()
