import pathlib,json,collections
b='batch-13b90e85d842da2d4f41';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'ed8673e4':('confirmed',True,'与 surface 同向的独立语境复核：birth/classes/warrior.lua:343 漏 pit-fighter；“门外汉”（外行）与 practitioner（实际习练者）相反；the Brawler\'s skills 被泛化为“格斗技能”，丢职业名“格斗家”。整句修复。'),
'ed86ff05':('confirmed',True,'与 surface 同向：town-point-zero/npcs.lua:134 A timeless elf…age is impossible to determine，“中年精灵”凭空断定年龄且与后句矛盾。修为“不显年岁的精灵”一类。'),
}
raw=json.loads((A/'review258-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==11
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==3,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=77,repair_required=3,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==11
(A/'review258-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW12-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 258',window=12,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第258批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：71 OK / 9 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致，无错位；一组full contextual（claude/claude-opus-5-5）：7 OK / 2 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计（均只读）、全部归档确认。\n\n宿主对11个观察裁决%s，结果77条完成、3条修复、0条pending。修复范围：格斗家职业描述（漏 pit-fighter、门外汉、职业名）、零点城镇 NPC timeless elf（中年精灵）、岱卡拉任务日志 huge fire dragon。驳回：Torment 每技能分别判定（窗口11按实现修复）、毒龙系技能（venom-drake 树名）、ego 前缀尾空格、Hidden Resources 结束提示。advisory：Mental Domination shaken→被支配、Tannen 对话“带着答案回来”。\n\n按1:1节奏，推送后进入修复窗口12，仅处理这3条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
