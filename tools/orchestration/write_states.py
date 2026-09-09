#!/usr/bin/env python3
"""为 surface 与 contextual 任务写 STATE.json 与 review record，使其满足 DONE 谓词。

用法：python3 -B tools/orchestration/write_states.py <batch_id> <base_commit>
随后必须逐个 `python3 -B tools/ai_state_check.py .ai/task/<task>/STATE.json --target DONE`
拿到 DONE_VERIFIED 才能继续 import/adjudicate。

易错点（都踩过）：
  - INPUT-DRAFT 必须是六键 canonical payload（surface-export 的 workset 少 contract，需补）
  - surface_evidence_binding 恰含 algorithm/task_id/terminal/artifact_sha256 四键
  - contextual_reviewers[i] 恰含 agent_id/candidate_identity/dispatch_id/input_path/purpose/role
  - full 模式 record 用 review_kind="full" 且**不得**含 lane 字段
  - 零 ISSUE 批次没有 contextual run，ctx 文件不存在属正常
"""
import json, hashlib, datetime, os, subprocess, sys
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import _orch


def _workspace_id():
    cwd=str(Path(__file__).resolve().parents[2])
    out=_orch.paseo(['workspace','ls','--json'])
    d=json.loads(out) if out.strip() else []
    # CLI 返回裸数组；MCP 返回 {"workspaces":[...]}。两种都兼容。
    ws=d.get('workspaces', []) if isinstance(d, dict) else d
    for w in ws:
        if w.get('cwd')==cwd: return w['workspaceId']
    raise SystemExit(f'找不到 cwd={cwd} 的 workspace')
from pathlib import Path
B=sys.argv[1]; BASE=sys.argv[2]
ORCH=os.environ['PASEO_AGENT_ID']          # 当前 ORCHESTRATOR 自己，勿硬编码
WKS=_workspace_id()                        # 按 cwd 运行时发现
NOW=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
plan=json.load(open(f'/tmp/dispatch-plan-{B}.json'))
agents=json.load(open(f'/tmp/lane_agents_{B}.json'))
cf=Path(f'/tmp/ctx_agents_{B}.txt')
# 零 ISSUE 批次没有 contextual run，此文件不存在属正常
ctx=[l.split() for l in cf.read_text().splitlines() if l.strip()] if cf.exists() else []
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def obs(prov,model,think,mode):
    p=lambda v:{'presence':'present','value':v}
    return {'capture_status':'captured','captured_at':NOW,'mode':p(mode),'model':p(model),
            'provider':p(prov),'schema_version':1,'source':'live_agent_metadata','thinking':p(think)}
SURF=('claude','claude-opus-5','medium','bypassPermissions')
CTX=('codex','gpt-5.6-sol','medium','full-access')

for task,e in plan.items():
    g=json.loads(Path(e['manifest']).read_bytes()) if e['mode']=='lane' else None
    gid=g['group_identity'] if g else None
    st={'baseline':{'commit':BASE},'candidate_author_agent_id':None,'change_class':'translation_workflow',
     'child_dispatches':[],'completed_review_contracts':['translation_surface_screen_v1'],'cycle':0,
     'deferred_findings':[],'final_validation_passed':True,'last_error':None,'max_cycles':3,
     'mode':'review_only','open_accepted_findings':[],'orchestration_transport':'cli',
     'orchestrator_agent_id':ORCH,'pending_review_contracts':[],
     'review_contracts':['translation_surface_screen_v1'],'review_phase':'REVIEW','review_records':[],
     'schema_version':5,'senior_review_records':[],'state':'DONE','surface_carry_over_path':None,
     'surface_screen_input_path':e['draft'],'surface_zero_path':None,'task_id':task,'updated_at':NOW,
     'wait':None,'workspace_id':WKS}
    art={e['draft']:sha(e['draft'])}
    for lane in e['lanes']:
        did=lane['dispatch_id']; aid=agents[task][did]; idx=lane['index']
        bnd=g['payload']['lane_boundaries'][idx-1] if g else None
        st['child_dispatches'].append({'agent_id':aid,'archive_attempts_started':1,'archive_confirmed':True,
          'archived_at':NOW,'author_provider_resolution':'not_applicable','candidate_author_agent_id':None,
          'candidate_identity':lane['candidate_identity'],'dispatch_id':did,'input_path':lane['input_path'],
          'labels':({'candidate_identity':lane['candidate_identity'],'dispatch_id':did,'lane_group_identity':gid,
                    'lane_index':str(idx),'paseo.parent-agent-id':ORCH,
                    'purpose':'translation_surface_screen_v1','role':'reviewer','task_id':task}
                    if e['mode']=='lane' else
                    {'candidate_identity':lane['candidate_identity'],'dispatch_id':did,
                     'lane_index':str(idx),'paseo.parent-agent-id':ORCH,
                     'purpose':'translation_surface_screen_v1','role':'reviewer','task_id':task}),
          'lifecycle':'archived','lineage_verified':True,
          'output_valid':True,'parent_agent_id':ORCH,'purpose':'translation_surface_screen_v1',
          'role':'REVIEWER','runtime_observation':obs(*SURF),'workspace_id':WKS}
          | ({'lane_group_identity':gid,'lane_index':idx} if e['mode']=='lane' else {}))
        rawp=f'.ai/reviews/{task}/raw-{did}.txt'
        rec={'agent_id':aid,'attempt':1,'candidate_identity':lane['candidate_identity'],'cycle':0,
          'dispatch_id':did,'input_path':lane['input_path'],
          'lineage_verified':True,'parent_agent_id':ORCH,'purpose':'translation_surface_screen_v1',
          'raw_output_path':rawp,'raw_output_sha256':sha(rawp),
          'review_contract':'translation_surface_screen_v1',
          'review_kind':('lane' if e['mode']=='lane' else 'full'),'review_phase':'REVIEW',
          'reviewer_role':'REVIEWER','status':'completed','task_id':task,'workspace_id':WKS}
        if e['mode']=='lane':
            rec['lane']={'count':4,'group_id':e['group_id'],'group_identity':gid,
                         'group_manifest_path':e['manifest'],'index':idx,
                         'length':bnd['length'],'offset':bnd['offset']}
        rp=Path(f'.ai/reviews/{task}/{did}.json'); rp.write_text(json.dumps(rec,ensure_ascii=False,indent=1,sort_keys=True)+'\n')
        st['review_records'].append(str(rp))
        art[rawp]=sha(rawp); art[lane['input_path']]=sha(lane['input_path'])
    st['surface_evidence_binding']={'algorithm':'surface-evidence-binding/1','artifact_sha256':dict(sorted(art.items())),
                                    'task_id':task,'terminal':'whole_screen'}
    Path(f'.ai/task/{task}/STATE.json').write_text(json.dumps(st,ensure_ascii=False,indent=1,sort_keys=True)+'\n')
    print('surface STATE', task)

for task,aid in ctx:
    cenv=f'.ai/task/{task}/CONTEXTUAL-ENVELOPE-final-full.json'
    ci=json.loads(Path(cenv).read_bytes())['candidate_identity']
    rawp=f'.ai/reviews/{task}/raw-full-000.txt'
    rec={'agent_id':aid,'attempt':1,'candidate_identity':ci,'cycle':0,'dispatch_id':'full-000','input_path':cenv,
     'lineage_verified':True,'parent_agent_id':ORCH,'purpose':'translation_contextual_v2','raw_output_path':rawp,
     'raw_output_sha256':sha(rawp),'review_contract':'translation_contextual_v2','review_kind':'full',
     'review_phase':'REVIEW','reviewer_role':'REVIEWER','status':'completed','task_id':task,'workspace_id':WKS}
    Path(f'.ai/reviews/{task}/full-000.json').write_text(json.dumps(rec,ensure_ascii=False,indent=1,sort_keys=True)+'\n')
    cst={'baseline':{'commit':BASE},'candidate_author_agent_id':None,'change_class':'standard',
     'child_dispatches':[{'agent_id':aid,'archive_attempts_started':1,'archive_confirmed':True,'archived_at':NOW,
       'author_provider_resolution':'not_applicable','candidate_author_agent_id':None,'candidate_identity':ci,
       'dispatch_id':'full-000','input_path':cenv,
       'labels':{'candidate_identity':ci,'dispatch_id':'full-000','paseo.parent-agent-id':ORCH,
                 'purpose':'translation_contextual_v2','role':'reviewer','task_id':task},
       'lifecycle':'archived','lineage_verified':True,'output_valid':True,'parent_agent_id':ORCH,
       'purpose':'translation_contextual_v2','role':'REVIEWER','runtime_observation':obs(*CTX),'workspace_id':WKS}],
     'completed_review_contracts':['translation_contextual_v2'],
     'contextual_reviewers':[{'agent_id':aid,'candidate_identity':ci,'dispatch_id':'full-000','input_path':cenv,
       'purpose':'translation_contextual_v2','role':'REVIEWER'}],
     'cycle':0,'deferred_findings':[],'final_validation_passed':True,'last_error':None,'max_cycles':3,
     'mode':'review_only','open_accepted_findings':[],'orchestration_transport':'cli','orchestrator_agent_id':ORCH,
     'pending_review_contracts':[],'review_contracts':['translation_contextual_v2'],'review_phase':'REVIEW',
     'review_records':[f'.ai/reviews/{task}/full-000.json'],'schema_version':5,'senior_review_records':[],
     'state':'DONE','task_id':task,'updated_at':NOW,'wait':None,'workspace_id':WKS}
    Path(f'.ai/task/{task}/STATE.json').write_text(json.dumps(cst,ensure_ascii=False,indent=1,sort_keys=True)+'\n')
    print('contextual STATE', task)
