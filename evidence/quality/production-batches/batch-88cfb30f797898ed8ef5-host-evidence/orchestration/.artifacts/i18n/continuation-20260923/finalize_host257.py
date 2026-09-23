import pathlib,json,collections
b='batch-88cfb30f797898ed8ef5';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'ebc83778':('confirmed',True,'与 surface 同向的独立语境复核：lore/trollmire.lua:40–45 两处空行被删（换行不变量），get wind of me 为“察觉”习语却被字面译作掩盖气味。确认整条修复。'),
'ebcb3ef0':('confirmed',True,'与 surface 同向：torment.lua:136–140 判定 cb.value >= max_life*l/100（含等于），“超过至少”自相矛盾。确认修为“至少”；第二句 Blood Grasp 临时生命不计入阈值的译法可保留。'),
'ec13c4e9':('confirmed',True,'与 surface 同向：rat-lich.lua:50 dusty 为“落满灰尘”，“肮脏”改变语义；同条 skull 与鉴定名“鼠巫妖头骨”应一致。确认修复。'),
}
raw=json.loads((A/'review257-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==8
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==4,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=76,repair_required=4,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==8
(A/'review257-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW11-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 257',window=11,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第257批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：75 OK / 5 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致，无错位；一组full contextual（claude/claude-opus-5-5）：2 OK / 3 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计（均只读）、全部归档确认。\n\n宿主对8个观察裁决%s，结果76条完成、4条修复、0条pending。修复范围：Trollmire 日记残页（空行与 get wind of 习语）、Torment 伤害阈值“超过至少”、鼠巫妖头骨未鉴定名、角色面板“状态效果抗性”标题。advisory：物理豁免标签冒号尾空格（同族约定）。\n\n按1:1节奏，推送后进入修复窗口11，仅处理这4条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
