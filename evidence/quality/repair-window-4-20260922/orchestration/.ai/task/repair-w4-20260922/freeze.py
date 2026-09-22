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
if (P/'HOST-SOURCE-SUPPLEMENT.json').exists():
 anchors+=json.loads((P/'HOST-SOURCE-SUPPLEMENT.json').read_text())['queries']
terms=json.loads((P/'TERM-SNAPSHOT.json').read_text())
snap=[];context=[]
for item in w['items']:
 pairs=[(i,r) for i,r in enumerate(rs) if all(r[k]==item[k] for k in ('section','source','source_tag'))]
 assert len(pairs)==1
 idx,r=pairs[0];key=item['entry_revision_identity']
 snap.append(dict(revision_key=key,source=r['source'],target=r['target']))
 neutral=dict(file='mod-tome.lua',section=r['section'],source_tag=r['source_tag'],line=r['line'],source_excerpts=[a for a in anchors if key in a['revision_keys']],adjacent_translations=[{k:n[k] for k in ('source','target','source_tag')} for n in rs[max(0,idx-1):idx+2] if n['section']==r['section'] and n['source']!=r['source']])
 if key.startswith('e433115e63'):
  neutral['edit_scope']={'public_source_path':'game/modules/tome/data/lore/elvala.lua','source_lines':[138,154,158,174,186],'scope':'本次仅修改这些源码行对应段落；其他段落保留作冻结语境。编辑边界不限制全文不变量、跨段关系核验或有据observation。'}
 context.append(dict(revision_key=key,context=json.dumps(neutral,ensure_ascii=False,sort_keys=True,separators=(',',':'))))
payload=dict(contract='translation_contextual_v2',ordered_revision_keys=[r['revision_key'] for r in snap],translation_snapshot=snap,fixed_source_identity='commit:624a67329fe2ad440c5b344785a9c73fcf22ae63',terminology_snapshot=json.dumps(terms,ensure_ascii=False,sort_keys=True,separators=(',',':')),bounded_context=context,rendered_briefing='以冻结版本源码实际行为核对全部条目的语义完整性、机制、术语、占位符及跨条关系。源码逐字摘录和术语正文已内嵌；文件/行号仅为来源信息。译文仅读本输入快照；必要时沿调用链补查同固定版本的相关公开源码。不得读取当前译文/术语库、其他任务、历史意见或宿主裁决。邻近冻结译文仅供语境，不增加可修改范围。')
draft=P/f'PAYLOAD-{phase}-{cycle}-{attempt}.json';assert not draft.exists();draft.write_bytes(canonical_bytes(payload))
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(['python3','-B','tools/contextual_anchor_preflight.py',str(P/'SCOPE.json'),str(draft)],capture_output=True,text=True)
receipt=dict(argv=r.args,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,draft_sha256=hashlib.sha256(draft.read_bytes()).hexdigest())
(P/f'ANCHOR-PREFLIGHT-{phase}-{cycle}-{attempt}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
assert r.returncode==0,r.stdout+r.stderr
if phase in ('REVIEW','RE_REVIEW'):
 gid=f'r{cycle}a{attempt}';ids=[f'{gid}l{i}' for i in range(1,5)]
 manifest,envs=build_group(payload,task_id=P.name,group_id=gid,review_phase=phase,cycle=cycle,attempt=attempt,dispatch_ids=ids)
 mp=P/f'CONTEXTUAL-LANE-GROUP-{gid}.json';assert not mp.exists();mp.write_bytes(canonical_bytes(manifest))
 for path,env in envs:
  assert not Path(path).exists();Path(path).write_bytes(canonical_bytes(env));render_dispatch_prompt(env['candidate_identity'],str(path))
 print(mp)
else:
 assert phase=='FINAL_REVIEW'
 ci=hashlib.sha256(canonical_bytes(payload)).hexdigest();env=dict(candidate_identity=ci,payload=payload);path=P/f'CONTEXTUAL-ENVELOPE-f{cycle}a{attempt}.json';assert not path.exists();path.write_bytes(canonical_bytes(env));render_dispatch_prompt(ci,str(path));print(path)
s.update(state=phase,review_phase=phase,cycle=cycle,contextual_reviewers=[],current_translation_sha256=hashlib.sha256(Path('mod-tome.lua').read_bytes()).hexdigest())
(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
