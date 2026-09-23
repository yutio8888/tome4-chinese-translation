import pathlib,json,collections
b='batch-73136994056fb59bf591';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'ee646924':('confirmed',True,'与 surface 同向的独立语境复核：stone.lua activate 设 never_move，Actor.lua:1486 仅在实际发生移动（只能是强制位移）时 forceUseTalent 关闭 Body of Stone；译文删 forced 易让人以为尝试移动即结束。随整句修复（化为石头、强制位移、冷却缩减百分比）。'),
'eea3b16d':('confirmed',True,'与 surface 同向：GRAPPLED 以 global_speed_add -eff.slow 实现（physical.lua:1475），冻结术语 combat.tsv:137 global action speed=全局速度（preferred）；“目标减速”丢机制名。改“降低目标 %d%% 全局速度”一类。'),
}
raw=json.loads((A/'review259-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==14
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==4,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=76,repair_required=4,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==14
(A/'review259-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW13-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 259',window=13,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第259批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：68 OK / 12 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致，无错位；一组full contextual（claude/claude-opus-5-5）：10 OK / 2 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计（均只读；lane-000-0 经 Paseo 终端只读读取，残留终端已由宿主关闭）、全部归档确认。\n\n宿主对14个观察裁决%s，结果76条完成、4条修复、0条pending。修复范围：Self-Judgement 流血死亡信息（死得其所→罪有应得）、Body of Stone 描述（化为石头、强制位移、冷却缩减百分比）、魔杖类型描述（漏制造者）、Crushing Hold 全局速度术语。驳回：Rich merchant 地图入口“富商的家”、item acid corrode 护甲、compare_fields 冒号尾空格、X 键大小写。advisory：梦之巨锤、Rolf 信“回去”、凤凰卷轴火球方向、Abyssal Shroud“堕入”。\n\n按1:1节奏，推送后进入修复窗口13，仅处理这4条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
