import pathlib,json,collections
b='batch-b1809d747f471912638d';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f009c2b1':('pending',False,'与 surface 同条同向：PartyDeath.lua:71 以 rng.table 取 death_message 代入“was %s to death”位（中文模板 mod-tome.lua:1412“玩家%s……%s而死”），现译为以“你”开头的完整分句且改成衰老致死，人称与句法均错位。属用户 2026-09-16 裁定继续 pending 的死亡描述词表族，登记为该族新证据，待用户审阅。'),
'f09f7b5b':('pending',False,'与 surface 同向：scourge.lua:25–26 显示名 Virulent Strike、short_name REND，“撕裂”沿用旧名；实现为双持两击、命中则延长目标最短疾病持续时间。技能改名需同步日志引用，属命名决定，待用户审阅。'),
'f0d4b3e8':('confirmed',True,'lore/misc.lua:224–230 半身人创世论：宿主复核确认三处——other gods were responsible, lesser gods ... which copied his grand design 被误作“其他创造者也很负责”并漏译；ridiculous ideals 误作“可笑形象”；our natural feelings of entitlement ... must stem from this 被改写成“赋予了我们……天然的所有权”（把心态说成既成权利，失去讽刺）。与 surface 同向，整条对照原文修复。'),
}
raw=json.loads((A/'review261-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==10
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==2,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==2,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=76,repair_required=2,blocked=2),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked against envelopes before harvest; lane-000-2 results[16] echo dropped "199" (verdict OK), host hand-attributed and harvested via --raw with the corrected identity, original bytes kept (captures261/lane2-original.raw).',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==10
(A/'review261-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW15-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 261',window=15,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; 2 pending (user review) excluded; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第261批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：73 OK / 7 ISSUE；harvest 前逐位比对回显 identity，lane-000-2 第17条（判 OK）回显漏“199”，宿主手工归因并以更正 raw 收取，原字节留档；full contextual（claude/claude-opus-5-5）4 OK / 3 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计（均只读）、全部归档确认。\n\n宿主对10个观察裁决%s，结果76条完成、2条修复、2条pending。修复范围：半身人创世论（other gods were responsible / ideals / entitlement）、紧急召回提示多出“救他”。pending：Virulent Strike 技能名“撕裂”（旧名 Rend）、死亡描述 grandfathered（人称错位，归入死亡描述词表族）。advisory：堡垒能量“收集”、奇特水晶球 thick blood、转移负面状态“物理与魔法”。\n\n按1:1节奏，推送后进入修复窗口15，仅处理这2条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
