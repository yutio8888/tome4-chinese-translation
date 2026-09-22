import json,sys,hashlib,subprocess,datetime
from pathlib import Path
sys.path.insert(0,'tools')
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
from contextual_lane_manifest import canonical_bytes,render_dispatch_prompt
from contextual_result_check import validate_envelope
P=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
phase=sys.argv[1];cycle=int(sys.argv[2]);attempt=int(sys.argv[3])
s=json.loads((P/'STATE.json').read_text());assert all(d['archive_confirmed'] for d in s['child_dispatches'])
assert s['candidate_author_agent_id']
item=json.loads((P/'WORKSET.json').read_text())['items'][0]
loader=LocaleLoader(LuaRuntime(load_manifest()))
matches=[r for r in loader.load_path(Path('tome-cults.lua')).translations if all(r[k]==item[k] for k in ('source','source_tag','section'))]
assert len(matches)==1;r=matches[0]
paired=[r for r in loader.load_path(Path('mod-tome.lua')).translations if r['source']==item['source'] and r['source_tag']==item['source_tag']]
assert len(paired)==1
provenance=json.loads((P/'SOURCE-PROVENANCE.json').read_text())
source_raw=(P/'CULTS-PUBLIC-SOURCE.lua').read_bytes();assert hashlib.sha256(source_raw).hexdigest()==provenance['public_source_snapshot_sha256']
engine=subprocess.check_output(['git','-C','/workspace/t-engine4','show','624a67329fe2ad440c5b344785a9c73fcf22ae63:game/engines/default/engine/I18N.lua']).decode().splitlines()
context={'file':'tome-cults.lua','section':item['section'],'source_tag':item['source_tag'],'component':'cults','public_source_path':provenance['public_source_path'],'source_pinning':'unpinned','upstream_source_commit':None,'upstream_version':'unfixed','observed_source_snapshot_sha256':provenance['public_source_snapshot_sha256'],'public_source_excerpt':source_raw.decode(),'frozen_related_translation':{k:paired[0][k] for k in ('source','target','source_tag','section')},'runtime_source':{'component':'engine','fixed_commit':'624a67329fe2ad440c5b344785a9c73fcf22ae63','path':'game/engines/default/engine/I18N.lua','excerpts':'\n'.join(f'{i+1}: {line}' for i,line in enumerate(engine) if 52<=i+1<=60 or 99<=i+1<=107 or 141<=i+1<=153)}}
payload=dict(contract='translation_contextual_v2',ordered_revision_keys=[item['entry_revision_identity']],translation_snapshot=[dict(revision_key=item['entry_revision_identity'],source=r['source'],target=r['target'])],fixed_source_identity=item['fixed_source_identity'],terminology_snapshot=json.dumps(json.loads((P/'TERM-SNAPSHOT.json').read_text()),ensure_ascii=False,sort_keys=True,separators=(',',':')),bounded_context=[dict(revision_key=item['entry_revision_identity'],context=json.dumps(context,ensure_ascii=False,sort_keys=True,separators=(',',':')))],rendered_briefing='核对这一条NPC名称与公开来源、继承关系及冻结的同键关联译文。Cults提取快照固定但上游源码仓库、commit和版本未固定；公开源码按本输入实际SHA256冻结，不得声称它是manifest固定源码版本。术语仅读实际冻结正文；关联译文只供关系语境，不增加编辑范围。不得读取当前译文/术语、历史报告或宿主裁决。')
draft=P/f'PAYLOAD-{phase}-{cycle}-{attempt}.json';assert not draft.exists();draft.write_bytes(canonical_bytes(payload))
started=datetime.datetime.now(datetime.timezone.utc).isoformat();c=subprocess.run(['python3','-B','tools/contextual_anchor_preflight.py',str(P/'SCOPE.json'),str(draft)],capture_output=True,text=True)
receipt=dict(argv=c.args,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=c.returncode,stdout=c.stdout,stderr=c.stderr,draft_sha256=hashlib.sha256(draft.read_bytes()).hexdigest());(P/f'ANCHOR-PREFLIGHT-{phase}-{cycle}-{attempt}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');assert c.returncode==0,c.stdout+c.stderr
ci=hashlib.sha256(canonical_bytes(payload)).hexdigest();did=('f' if phase=='FINAL_REVIEW' else 'r')+f'{cycle}a{attempt}';ep=P/f'CONTEXTUAL-ENVELOPE-{did}.json';assert not ep.exists();env=dict(candidate_identity=ci,payload=payload);validate_envelope(env);ep.write_bytes(canonical_bytes(env))
labels=dict(task_id=P.name,role='reviewer',purpose='translation_contextual_v2',dispatch_id=did,candidate_identity=ci);labels['paseo.parent-agent-id']=s['orchestrator_agent_id']
intent=dict(role='REVIEWER',purpose='translation_contextual_v2',candidate_identity=ci,input_path=str(ep),candidate_author_agent_id=s['candidate_author_agent_id'],labels=labels)
(P/f'{did}-intent.json').write_text(json.dumps(intent,ensure_ascii=False,indent=2)+'\n');(P/f'{did}-prompt.txt').write_text(render_dispatch_prompt(ci,str(ep)))
s.update(state=phase,review_phase=phase,cycle=cycle,contextual_reviewers=[],current_translation_sha256=hashlib.sha256(Path('tome-cults.lua').read_bytes()).hexdigest());(P/'STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print(did,ci)
