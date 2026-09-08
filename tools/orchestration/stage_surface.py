#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 checkpoint 的 surface refs 建 .ai/task/<batch>-surface-NNN/ 布局。

run 的构成**只**以 checkpoint refs 为准，绝不 ls .artifacts 目录推断——
该目录会残留上一批的 run-NNN-* 文件（runbook §28）。

用法：python3 -B tools/orchestration/stage_surface.py <batch-id> [--out /tmp/plan.json]
"""
import json, sys, pathlib, datetime, collections

ROOT = pathlib.Path('.')
CKPT = ROOT / '.artifacts/i18n/production-review-v2-lite/active-batch.json'


def canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def main():
    batch = sys.argv[1]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/tmp/plan.json'
    cp = json.loads(CKPT.read_text())
    assert cp['batch_id'] == batch, cp['batch_id']

    runs = collections.defaultdict(list)
    for i, r in enumerate(cp['surface']):
        run = pathlib.Path(r['input_path']).name.split('-')[1]
        runs[run].append((i, r))

    plan = {}
    for run, items in sorted(runs.items()):
        task = f'{batch}-surface-{run}'
        d = ROOT / '.ai/task' / task
        d.mkdir(parents=True, exist_ok=True)
        items.sort(key=lambda x: x[0])
        # 单 ref 且无 group manifest = full stage；否则四 lane 组
        full = len(items) == 1 and not items[0][1].get('group_manifest_path')
        lanes, entries, head = [], [], None
        for pos, (ref, r) in enumerate(items):
            env = json.loads(pathlib.Path(r['input_path']).read_text())
            payload = env['payload']
            if full:
                did = f'full-{run}'
                name = f'SURFACE-SCREEN-ENVELOPE-full-{run}.json'
            else:
                did = f'lane-{run}-{pos}'
                name = f'SURFACE-SCREEN-ENVELOPE-lane-{run}-{pos}.json'
            (d / name).write_bytes(canon(env))
            head = head or {k: payload[k] for k in (
                'contract', 'fixed_source_identity', 'rendered_briefing',
                'rules_version', 'terminology_snapshot')}
            entries += payload['entries']
            lanes.append({'dispatch_id': did, 'index': pos + 1, 'ref_index': ref,
                          'candidate_identity': r['candidate_identity'],
                          'input_path': str(d / name), 'entries': len(payload['entries']),
                          'review_kind': 'full' if full else 'lane'})
            if r.get('group_manifest_path'):
                g = json.loads(pathlib.Path(r['group_manifest_path']).read_text())
                gp = d / f"SURFACE-SCREEN-GROUP-{g['payload']['group_id']}.json"
                gp.write_bytes(canon(g))

        draft = dict(head)
        draft['entries'] = entries
        (d / 'SURFACE-SCREEN-INPUT-DRAFT.json').write_bytes(canon(draft))

        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        (d / 'STATE.json').write_text(json.dumps({
            'schema_version': 5, 'task_id': task, 'mode': 'review_only', 'state': 'REVIEW',
            'review_phase': 'REVIEW', 'cycle': 0, 'max_cycles': 3,
            'review_contracts': ['translation_surface_screen_v1'],
            'completed_review_contracts': [], 'pending_review_contracts': [],
            'child_dispatches': [], 'review_records': [], 'senior_review_records': [],
            'deferred_findings': [], 'open_accepted_findings': [],
            'baseline': {'commit': cp['base_commit']}, 'orchestration_transport': 'cli',
            'workspace_id': 'wks_420314270844170b', 'final_validation_passed': False,
            'last_error': None, 'wait': None, 'updated_at': now,
            'change_class': 'translation_workflow', 'candidate_author_agent_id': None,
            'orchestrator_agent_id': None,
        }, ensure_ascii=False, indent=1, sort_keys=True))

        plan[task] = {'task_id': task, 'ref_indexes': [l['ref_index'] for l in lanes],
                      'entries': len(entries), 'mode': 'full' if full else 'lane', 'lanes': lanes}
        (d / 'dispatch-plan.json').write_text(json.dumps({task: plan[task]}, ensure_ascii=False, indent=1))
        print(f"{task}  mode={plan[task]['mode']}  refs={plan[task]['ref_indexes']}  entries={len(entries)}")

    total = sum(v['entries'] for v in plan.values())
    assert total == len(cp['selected']), (total, len(cp['selected']))
    print('总 entries', total)
    json.dump(plan, open(out, 'w'), ensure_ascii=False, indent=1)


main()
