import pathlib,json,collections
b='batch-6b8acfddd3cc0c11f471';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'ef7d5a43':('confirmed',True,'chats/jewelry-store.lua:168–169 珠宝师对话：原文为冬潮之月的一部分因离太阳过近而 melted（融化）并从天空坠落，译文漏“融化”并凭空加“融入了大地，使那个地方充满能量”的因果；potent amulets 为“强力的项链”，译文“更强大的”多出比较义。忠实性缺陷，整段对照原文修复（amulet 仍用项链）。'),
'ef9f97a2':('confirmed',True,'与 surface 同向：psi-archery.lua:50 漏译 telekinetic nudges（念力微调导引），“精确的”应作“精确地”。'),
'efe21d07':('confirmed',True,'与 surface 同向：canine.lua:62 snaps at you 为猛咬/扑咬，“咆哮”误译动作。'),
}
raw=json.loads((A/'review260-contextual-raw/full-001.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==10
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==3,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=77,repair_required=3,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-001; full-000 rejected for prose prefix, archived, superseded)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==10
(A/'review260-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW14-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 260',window=14,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第260批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：73 OK / 7 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致，无错位；full contextual（claude/claude-opus-5-5）首次 full-000 在 JSON 前多一句英文导语被判 output_valid=False，归档确认后以 full-001（attempt 2，retry_of full-000）重派，4 OK / 3 ISSUE。6个独立reviewer child 严格收取、原生读取边界人工审计（均只读）、全部归档确认。\n\n宿主对10个观察裁决%s，结果77条完成、3条修复、0条pending。修复范围：珠宝师对话冬潮之月传说（漏融化、增添融入大地、更强大）、Guided Shot 念力导引、巨狼描述 snaps at you。驳回：Roguelike/Adventure 永久死亡模式说明、amulet=项链。advisory：Higher“普通人类”、Oozewalk“粘液探戈”、异常日志“几率发生了倾斜”。\n\n按1:1节奏，推送后进入修复窗口14，仅处理这3条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
