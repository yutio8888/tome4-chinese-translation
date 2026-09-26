import sys,json,pathlib,subprocess,datetime
R=pathlib.Path.cwd();sys.path.insert(0,str(R/'tools'))
from i18nlib import production_review_v2_lite_batch as B
from orchestration import build_evidence_pack as F
import contextual_anchor_preflight as P
cp=json.loads((R/'.artifacts/i18n/production-review-v2-lite/active-batch.json').read_text());assert cp['phase']=='surface_collected'
b=cp['batch_id'];runs=B.partition_contextual_entries(cp)
assert runs
packages=F.build_source_facts(R,F.ordinary_bytes(R/'evidence/quality/production-batches'/f'{b}-source-workset.json'),cp,runs)
for run in runs:
 payload=B._contextual_payload(run);package=packages[run['run_index']]
 for ctx,fact in zip(payload['bounded_context'],package['entries']): ctx['context']+=F.bound_context(package,fact)
 d=R/'.ai/task'/f"{b}-contextual-{run['run_index']:03d}";d.mkdir(parents=True,exist_ok=True)
 draft=d/'CONTEXTUAL-INPUT-DRAFT.json';assert not draft.exists()
 draft.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
 scopes=sorted(set((e['normalized_path'],e['section']) for e in run['entries']))
 # Titled sections must declare every actual chapter title in file order; untitled ones use the whole-section form.
 def titles(f,s):
  secs,calls=P._scan_lua((R/f).read_text(encoding='utf-8'));sec=[x for x in secs if x.path==s];assert len(sec)==1
  end=min((x.start for x in secs if x.start>sec[0].start),default=10**12)
  return [c.source for c in calls if sec[0].start<c.start<end and P._is_chapter_title(c.source)]
 (d/'SCOPE.json').write_text(json.dumps(dict(schema_version=1,allowed_files=sorted(set(x[0] for x in scopes)),anchor_scopes=[dict(file=f,section_path=s,ordered_titles=titles(f,s)) for f,s in scopes]),ensure_ascii=False,indent=2)+'\n')
 (d/'SPEC.md').write_text(f"审核315上下文full（reviewer: claude/claude-opus-5-5），范围仅draft冻结的{len(run['entries'])}条revision；只读，术语限冻结正文。{'+'.join(sorted({{'tome-ashes-urhrok.lua':'Ashes','tome-cults.lua':'Cults','tome-orcs.lua':'Orcs'}.get(e['normalized_path'],e['normalized_path']) for e in run['entries']}))} 公开源码按本批文件 SHA 核验，仓库和 commit 未固定；只按 envelope 与契约允许的有限引用核查。宿主独立裁决，不改译文、术语或范围外记录。\n")
 (d/'PLAN.md').write_text("1. 依据已收集surface精确构建draft及中立source facts。\n2. 先执行anchor preflight，通过后才production contextual export并核对payload字节一致；stage冻结及派发。\n3. 单次reviewer终态后校验strict/native/边界并归档，宿主裁决及DONE验证。\n")
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(['python3','-B','tools/contextual_anchor_preflight.py',str(d/'SCOPE.json'),str(draft)],capture_output=True,text=True)
 receipt=dict(argv=result.args,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
 (d/'ANCHOR-PREFLIGHT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False));assert result.returncode==0
