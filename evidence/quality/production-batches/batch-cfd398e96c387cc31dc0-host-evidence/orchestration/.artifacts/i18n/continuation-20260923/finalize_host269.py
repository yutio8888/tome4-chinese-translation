import pathlib,json,collections
b='batch-cfd398e96c387cc31dc0';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f8f6be5a':('confirmed',True,'与 surface 同向并补充：ARCANE_VORTEX on_timeout 有敌人时被附身目标自身先受 eff.dam，再向随机敌人发射 beam，路径上所有单位受伤；现译只写“随机对……目标造成”，漏射线贯穿与本体同时受伤。整条修复。'),
}
raw=json.loads((A/'review269-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==10
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==3,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=77,repair_required=3,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f8a393e3 (yeek quest) and f8f18f94 (eyal\'s fury); host keeps both confirmed on direct source comparison: “at least” is dropped (dropped-qualifier class) and “around you” is dropped.','Contextual passed f8b95de7, f8f3b8de, f95b1ff4, matching host refuted.','Three surface advisories (starseers keyword, gloves or gauntlets, plan-to-fail nuance) not repaired.','One surface lane listed Paseo terminal tool names during tool discovery; no terminal tool was invoked and list_terminals(all) was empty.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==10
(A/'review269-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW23-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 269',window=23,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第269批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：71 OK / 9 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000：8 OK / 1 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对10个观察裁决%s，结果77条完成、3条修复、0条pending。修复范围：夺心魔任务“至少清除一个威胁”（漏 at least）、埃亚尔之怒（eyal\'s fury）技能类别说明漏“周围的”、奥术漩涡说明漏射线贯穿路径上全部目标与本体同时受伤。驳回：+碎骨压制（沿用技能名）、疾射姿态“命中”条件（实现要求 hitted）、永久死亡/冒险两档名称。advisory：观星者关键词、手套/臂铠“和”、“不打算失败”语感。\n\n按1:1节奏，推送后进入修复窗口23，仅处理这3条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
