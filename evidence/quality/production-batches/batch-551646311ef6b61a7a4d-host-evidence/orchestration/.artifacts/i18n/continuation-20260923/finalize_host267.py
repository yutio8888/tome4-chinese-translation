import pathlib,json,collections
b='batch-551646311ef6b61a7a4d';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f6cc31f2':('pending',False,'与 surface 同向（contextual 另指 blight 为腐化/枯萎伤害而非气体，PartyDeath.lua:71,107 代入“was %s to death by %s”）。死亡描述词表整族由用户 2026-09-16 裁定继续 pending，本条作为该族新证据列入 pending-user-review，不单改。'),
'f6e111a3':('confirmed',True,'与 surface 同向：agility.lua:69–71 %d 为 lastdam-dam 即被盾牌偏转抵消的伤害量；现译“敏捷防御”读作技能名。整条修复为“(%d 被偏转)”一类。'),
'f6eae8d3':('confirmed',True,'与 surface 同向：blighted-ruins.lua:27 单段无换行，现译插入 \\n\\t（一级换行不变量）。整条修复。'),
'f6f9c010':('confirmed',True,'与 surface 同向，并补充：下一行 psionic.lua:141 讲“the collective vision of those that experience it”，现译“许多个梦境”与之矛盾；unlock the potential of your dreams 被改为“打开通往梦境之门”。整条修复。'),
'f72ac3de':('confirmed',True,'与 surface 同向：damage_types.lua:3935–3946 每回合在网中给予 STATIC_CHARGE，mental.lua:2812–2813 on_merge 叠加 power，故加成按停留回合累加；现译漏 for each turn you spend within its area。整条修复。'),
}
raw=json.loads((A/'review267-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==12
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==1,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=74,repair_required=5,blocked=1),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all 80 surface identity echoes pre-checked exact against envelopes before harvest; lanes 0,2,3 and the contextual child harvested via --native-log; lane-000-1 results[16] identity echo was wrong at an OK position (65 chars, first 29 match); host hand-attributed and harvested via --raw with the corrected identity, original bytes kept (captures267/lane1-original.raw, lane1-attribution.md).',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f6a545d0 (Sun Flare); host keeps it confirmed on objective evidence: flare is 耀斑 while 日珥 is a solar prominence, a different phenomenon; the talent name row is the only occurrence of either term, so the fix is a single-row correction, not a global rename.','Contextual passed f6e9cd9b (Magical Status), matching host refuted.','f6cc31f2 (blight death message) is pending: the death-description family stays pending per user 2026-09-16; added to evidence/quality/pending-user-review.md as new family evidence; state blocked, not repaired.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==12
(A/'review267-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW21-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 267',window=21,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; pending f6cc31f2 (death-description family); unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第267批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：73 OK / 7 ISSUE；harvest 前逐位比对 80 个回显 identity，lane-000-1 一处判 OK 的 identity 回显错误（第17条，前29位一致、尾部不属于本组任何条目），宿主手工归因并以更正 raw 收取，原字节留档。full contextual（claude/claude-opus-5-5）full-000：2 OK / 5 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对12个观察裁决%s，结果74条完成、5条修复、1条pending。修复范围：Sun Flare 技能名（日珥→耀斑）、盾牌敏捷格挡日志“(%%d deflected)”误作“敏捷防御”、枯萎遗迹 lore 多出的换行与制表符、Solipsist 职业引语（共同之梦、发掘梦境潜能）、静电网漏“每停留一回合”累加。contextual 对 Sun Flare 判 OK，宿主据术语客观差异维持确认。驳回：Magical Status 列标题尾随空格（英文对齐填充）。pending：枯萎死亡描述“吸入过多剧毒瘴气”，随死亡描述词表整族待用户裁定。\n\n按1:1节奏，推送后进入修复窗口21，仅处理这5条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
