import pathlib,json,collections
b='batch-b7ce18a7bdce48ba8086';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fa2a8ff2':('confirmed',True,'与 surface 同向：slaughter.lua:125–146 Frenzy（狂热）for i=1,4 每次攻击各自选目标，附近有被追踪猎物时四次都打它；damage each 指每次攻击，现译“每个目标造成”误挂，“优先攻击”弱化 always。并入同条整句修复（含 fast 与盾牌句前空行）。'),
'fa9d429c':('confirmed',True,'升级 surface advisory：本条源串为 load.lua:186 属性定义，只列 mana/stamina/PSI capacity 与抗精神攻击几率，不含 Mindpower；TooltipsData.lua:243 是另一条字符串。现译多出“精神力”既是增译，又与本库 Mindpower=“精神强度”不一致（术语一级）。整条修复：去掉“精神力”，按原文四项译出，“抵抗精神攻击的几率”可沿用“精神豁免”一类本库说法。'),
}
raw=json.loads((A/'review270-contextual-raw/full-001.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==16
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==6,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=74,repair_required=6,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-001 accepted; full-000 rejected for a prose prefix before the JSON, archived and confirmed)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations; lane 2 built its result JSON in memory and its observations land on the correct entries.','Contextual full-000 was rejected by harvest (English prose sentence before the JSON); per procedure it was archived and a fresh attempt full-001 (retry_of full-000, attempt 2) produced the accepted result. The rejected output is not counted; its staff set-item lead was independently verified by the host from pinned source.','Contextual passed f99ebf3a, f9b4a1d5, fa465502, fa46681a; host keeps them confirmed on objective grounds (effect name 被镇静; newline invariant; added 直觉; set-item alone reversed).','Contextual raised fa9d429c; host upgrades surface advisory to confirmed (addition plus nonstandard term 精神力 vs 精神强度).','Four surface advisories not repaired: exploration achievements wording, quest title 绝望的坟墓, martyrdom wording (fa9d429c advisory superseded by contextual confirm).','dc8e68d2 (Arcane Vortex) and e246982c (yeek) are window 23 successors; both refuted as source-backed / user-decided.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==16
(A/'review270-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW24-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 270',window=24,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第270批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：66 OK / 14 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）：full-000 因 JSON 前带英文导语被判无效并归档，重派 full-001 得 12 OK / 2 ISSUE。6个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对16个观察裁决%s，结果74条完成、6条修复、0条pending。修复范围：飞镖发射器抵抗日志“睡眠”改与效果名“被镇静”一致；敏锐直觉说明去“直觉”并恢复 3 行；狂热（4 次快速攻击）each 指每次攻击、always 总是攻击被追踪猎物、盾牌句前空行；奥术至上法杖描述恢复换行并改“单独一件似乎并不完整”；吸食抗性说明删多余换行；意志属性说明删增译“精神力”。驳回：奥术漩涡（窗口23源码收敛）、夺心魔（用户裁定）、急速通关“回合内”（实现允许用满）、两个 ego 前缀尾空格。advisory：探索模式成就措辞、任务名“绝望的坟墓”、殉难效果措辞。\n\n按1:1节奏，推送后进入修复窗口24，仅处理这6条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
