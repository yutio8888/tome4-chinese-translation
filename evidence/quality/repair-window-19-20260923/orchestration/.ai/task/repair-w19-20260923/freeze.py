import json,sys,hashlib,subprocess,datetime
from pathlib import Path
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
from contextual_lane_manifest import canonical_bytes,build_group,render_dispatch_prompt
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
phase=sys.argv[1];cycle=int(sys.argv[2]);attempt=int(sys.argv[3])
s=json.loads((P/'STATE.json').read_text())
assert all(d['archive_confirmed'] for d in s['child_dispatches'])
assert s['executor']['agent_id'] and s['candidate_author_agent_id']
w=json.loads((P/'WORKSET.json').read_text())
rs=LocaleLoader(LuaRuntime(load_manifest())).load_path(Path('mod-tome.lua')).translations
anchors=json.loads((P/'SOURCE-ANCHORS.json').read_text())['queries']
for sup in sorted(P.glob('HOST-SOURCE-SUPPLEMENT*.json')):
 anchors+=json.loads(sup.read_text())['queries']
terms=json.loads((P/'TERM-SNAPSHOT.json').read_text())
snap=[];context=[]
for item in w['items']:
 pairs=[(i,r) for i,r in enumerate(rs) if all(r[k]==item[k] for k in ('section','source','source_tag'))]
 assert len(pairs)==1
 idx,r=pairs[0];key=item['entry_revision_identity']
 snap.append(dict(revision_key=key,source=r['source'],target=r['target']))
 neutral=dict(file='mod-tome.lua',section=r['section'],source_tag=r['source_tag'],line=r['line'],source_excerpts=[a for a in anchors if key in a['revision_keys']],adjacent_translations=[{k:n[k] for k in ('source','target','source_tag')} for n in rs[max(0,idx-1):idx+2] if n['section']==r['section'] and n['source']!=r['source']])
 context.append(dict(revision_key=key,context=json.dumps(neutral,ensure_ascii=False,sort_keys=True,separators=(',',':'))))
payload=dict(contract='translation_contextual_v2',ordered_revision_keys=[r['revision_key'] for r in snap],translation_snapshot=snap,fixed_source_identity='commit:624a67329fe2ad440c5b344785a9c73fcf22ae63',terminology_snapshot=json.dumps(terms,ensure_ascii=False,sort_keys=True,separators=(',',':')),bounded_context=context,rendered_briefing='公开固定版本源码仓库位于 /workspace/t-engine4，可用 git -C /workspace/t-engine4 show 固定commit读取。以冻结版本源码实际行为核对全部条目的语义完整性、机制、术语、占位符及跨条关系。源码逐字摘录和术语正文已内嵌；文件/行号仅为来源信息。译文仅读本输入快照；必要时沿调用链补查同固定版本的相关公开源码。不得读取当前译文/术语库、其他任务、历史意见或宿主裁决。邻近冻结译文仅供语境，不增加可修改范围。')
if False:  # full stages only (contract: n>=4 may, not must, use lanes)
 gate_path=P/f'REVIEW-READY-{phase}-{cycle}-{attempt}.json'
 gate_payload=dict(task_id=P.name,review_phase=phase,cycle=cycle,attempt=attempt,all_four_live_bindings_verified=True)
 gate_bytes=canonical_bytes(gate_payload)
 gate_spec=P/f'REVIEW-READY-SPEC-{phase}-{cycle}-{attempt}.json';assert not gate_spec.exists();gate_spec.write_bytes(canonical_bytes(dict(path=str(gate_path),payload=gate_payload,sha256=hashlib.sha256(gate_bytes).hexdigest())))
 payload['rendered_briefing']+=f' 启动前置条件：仅在精确引用的只读启动凭据 {gate_path} 存在且SHA256为{hashlib.sha256(gate_bytes).hexdigest()}时开始实质审核。该凭据的预定正文只包含本task/stage及四名child均已完成live绑定的布尔声明，不包含裁决或译文；宿主在四名child全部创建并核验后一次性发布。若文件尚不存在，在当前一次运行内等待，每次等待不超过30秒，不提前审核、输出结果或结束，不读取其他宿主文件。'
draft=P/f'PAYLOAD-{phase}-{cycle}-{attempt}.json';assert not draft.exists();draft.write_bytes(canonical_bytes(payload))
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(['python3','-B','tools/contextual_anchor_preflight.py',str(P/'SCOPE.json'),str(draft)],capture_output=True,text=True)
receipt=dict(argv=r.args,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,draft_sha256=hashlib.sha256(draft.read_bytes()).hexdigest())
(P/f'ANCHOR-PREFLIGHT-{phase}-{cycle}-{attempt}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
assert r.returncode==0,r.stdout+r.stderr
if False:  # full stages only (contract: n>=4 may, not must, use lanes)
 gid=f'r{cycle}a{attempt}';ids=[f'{gid}l{i}' for i in range(1,5)]
 manifest,envs=build_group(payload,task_id=P.name,group_id=gid,review_phase=phase,cycle=cycle,attempt=attempt,dispatch_ids=ids)
 mp=P/f'CONTEXTUAL-LANE-GROUP-{gid}.json';assert not mp.exists();mp.write_bytes(canonical_bytes(manifest))
 for path,env in envs:
  assert not Path(path).exists();Path(path).write_bytes(canonical_bytes(env));render_dispatch_prompt(env['candidate_identity'],str(path))
 print(mp)
else:
 assert phase in ('REVIEW','RE_REVIEW','FINAL_REVIEW')
 ci=hashlib.sha256(canonical_bytes(payload)).hexdigest();env=dict(candidate_identity=ci,payload=payload);prefix='f' if phase=='FINAL_REVIEW' else 'r';path=P/f'CONTEXTUAL-ENVELOPE-{prefix}{cycle}a{attempt}.json';assert not path.exists();path.write_bytes(canonical_bytes(env));render_dispatch_prompt(ci,str(path));print(path)
s.update(state=phase,review_phase=phase,cycle=cycle,contextual_reviewers=[],current_translation_sha256=hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest())
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
