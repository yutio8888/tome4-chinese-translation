#!/usr/bin/env python3
"""把 surface-export 的产物落成 consumer 期望的 .ai/task/<task>/ 布局，并写 dispatch-plan。

用法：python3 -B tools/orchestration/stage_surface.py <batch_id>
权威来源是 active checkpoint 的 surface[].input_path，**不是** glob 目录——
.artifacts/.../surface/ 会跨批残留上一批文件（runbook §9）。
三种批次形态都要支持：单 run（task_id == batch_id）、多 run（<batch>-surface-NNN）、
n<=3 的 full 模式（单成员、无 group manifest）。
"""
import json, os, re, sys
from pathlib import Path
B=sys.argv[1]
ROOT=Path(os.environ.get('TOME_TRANSLATION_ROOT', Path(__file__).resolve().parents[2]))
def canon(o): return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',',':'), allow_nan=False).encode()
cp=json.load(open('.artifacts/i18n/production-review-v2-lite/active-batch.json'))
assert cp['batch_id']==B, cp['batch_id']
S=ROOT/'.artifacts/i18n/production-review-v2-lite/surface'

# 以 checkpoint surface refs 为权威（scratch 目录会残留上一批文件）
runs={}
for i,ref in enumerate(cp['surface']):
    ip=Path(ref['input_path'])
    m=re.match(r'run-(\d+)-lane-(\d+)\.json$', ip.name)
    assert m, ip.name
    runs.setdefault(m.group(1), []).append((int(m.group(2)), i, ip))
plan={}
single = len(runs)==1
for rn in sorted(runs):
    members=sorted(runs[rn])
    # 单 run 批次 exporter 用 task_id == batch_id；多 run 才带 -surface-NNN 后缀
    task = B if single else f'{B}-surface-{rn}'
    T=ROOT/'.ai/task'/task; T.mkdir(parents=True, exist_ok=True)
    n_entries=sum(len(json.loads(p.read_bytes())['payload']['entries']) for _,_,p in members)
    gpath=S/f'run-{rn}-group.json'
    e={'task_id':task,'ref_indexes':[i for _,i,_ in members],'entries':n_entries,'lanes':[]}
    if len(members)==1:
        # full 模式（n<=3）：无 group manifest，权威 artifact 是单个 envelope
        env=json.loads(members[0][2].read_bytes())
        did=f'full-{rn}'
        dest=T/f'SURFACE-SCREEN-ENVELOPE-{did}.json'; dest.write_bytes(canon(env))
        draft=dict(env['payload']); draft.setdefault('contract','translation_surface_screen_v1')
        (T/'SURFACE-SCREEN-INPUT-DRAFT.json').write_bytes(canon(draft))
        e.update({'mode':'full','group':None,'group_id':None,'manifest':None,
                  'draft':str((T/'SURFACE-SCREEN-INPUT-DRAFT.json').relative_to(ROOT))})
        e['lanes'].append({'dispatch_id':did,'index':0,'candidate_identity':env['candidate_identity'],
                           'input_path':str(dest.relative_to(ROOT))})
    else:
        g=json.loads(gpath.read_bytes())
        assert g['payload']['task_id']==task, (g['payload']['task_id'], task)
        assert len(members)==g['payload']['lane_count']==4
        gid_name=g['payload']['group_id']
        mpath=T/f'SURFACE-SCREEN-GROUP-{gid_name}.json'; mpath.write_bytes(canon(g))
        draft=dict(g['payload']['workset']); draft['contract']='translation_surface_screen_v1'
        (T/'SURFACE-SCREEN-INPUT-DRAFT.json').write_bytes(canon(draft))
        e.update({'mode':'lane','group':g['group_identity'],'group_id':gid_name,
                  'manifest':str(mpath.relative_to(ROOT)),
                  'draft':str((T/'SURFACE-SCREEN-INPUT-DRAFT.json').relative_to(ROOT))})
        for (li,_,p),lane in zip(members, g['payload']['lanes']):
            env=json.loads(p.read_bytes())
            assert env['candidate_identity']==lane['candidate_identity'], (task, li)
            dest=Path(lane['input_path']); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(canon(env))
            e['lanes'].append({'dispatch_id':lane['dispatch_id'],'index':lane['index'],
                               'candidate_identity':lane['candidate_identity'],'input_path':str(dest)})
    plan[task]=e
    print(f"staged run {rn} task {task} mode {e['mode']} entries {n_entries} members {len(e['lanes'])}")
total=sum(v['entries'] for v in plan.values())
assert total==len(cp['selected']), (total, len(cp['selected']))
Path(f'/tmp/dispatch-plan-{B}.json').write_text(json.dumps(plan,indent=1)+'\n')
for task,e in plan.items():
    Path(f'.ai/task/{task}/dispatch-plan.json').write_text(json.dumps({task:e},indent=1)+'\n')
print('total entries', total, '| runs', len(plan))
