import pathlib,json,collections
b='batch-448e3278fde3f8dfbea2';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'ea047c36':('confirmed',True,'独立语境复核补充并经宿主核验：cunning/stealth.lua:24–36 stealthDetection 仅累计半径内敌对、未致盲且 act.fov.actors[self]（能看见你）的角色，原文 foes in sight within range 的 in sight 被译文“敌人在半径内”漏掉；action→技能的缩窄与 surface 键同一缺陷（Combat.lua:121/258、Object.lua:340 亦打破潜行）。确认整句有界修复两处。'),
'ea36045f':('confirmed',True,'与 surface 键同一缺陷的独立语境复核：world-artifacts.lua:8068 bright warm light 被译作“微光”，语义相反，确认修复。'),
'ea4c9e1c':('confirmed',True,'与 surface 键同一缺陷的独立语境复核：quest-artifacts.lua:319 bend space 被译作“撕裂空间”，raw magical energies 的“原始”亦未体现；与 surface 所指 rod→法杖 合并为整句有界修复。'),
}
raw=json.loads((A/'review255-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==14
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==3
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=72,repair_required=5,blocked=3),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==14
(A/'review255-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW9-EARLY-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='confirmed mechanism finding in ea047c36 (stealth: in sight omitted and action narrowed to talents); finish and push current formal review batch before repair',window=9,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; 3 pending (blocked) revisions awaiting user review; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第255批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：69 OK / 11 ISSUE，逐条比对无错位；一组full contextual（claude/claude-opus-5-5）：8 OK / 3 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对14个观察裁决%s，结果72条完成、5条修复、3条pending（blocked）。修复范围：高阶奇术师解锁文本 Flame 技能名（火球术→火焰）、潜行说明（漏 in sight、action 缩成技能）、死灵符文 runes active、夏之眼 bright→微光、回归之杖描述（法杖/撕裂/raw）。黑暗传送门落点与实现一致而驳回；巫妖外观名、触手 Ewwww 语气记建议。pending：yeek 叙事 cunning、毒素风暴等概率措辞（均为窗口8待审项的另一副本）、技能名 Matter is Energy。\n\n潜行为已确认机制缺陷，批次推送后提前进入窗口9，仅处理这5条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
