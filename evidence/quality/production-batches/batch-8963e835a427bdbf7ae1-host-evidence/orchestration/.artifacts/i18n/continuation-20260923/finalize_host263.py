import pathlib,json,collections
b='batch-8963e835a427bdbf7ae1';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f2b2afec':('confirmed',True,'与 surface 同向：Combat.lua:975 Exploit Weakness 只在近战攻击命中流程中触发，现译删去 with a melee attack 限定。整条修复（含结尾 \\n\\t\\t）。'),
'f2d8717e':('confirmed',True,'与 surface 同向：TOOLTIP_SPECIFIC_IMMUNE 为单项免疫行的回退提示（CharacterSheet.lua:1298/1307），应为“完全抵抗该特定效果的几率”，标题勿与 Status resistance 混同。'),
'f30327e6':('confirmed',True,'与 surface 同向：done.lua:20–31 无对应断行，现译在词中插入 3 处硬换行，违反换行不变量。'),
}
raw=json.loads((A/'review263-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==16
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=75,repair_required=5,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest; no hand attribution in this batch. lane-000-2 notification showed a leading --- separator but the native-log final message is exact JSON.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f277b46e (headhunter) and f33c065a (thought-forms); host keeps both confirmed on objective evidence: GameState.lua:3671-3675 clears enemy targets rather than pausing them, and thought-forms target has 7 LF vs source 3 LF.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==16
(A/'review263-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW17-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 263',window=17,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第263批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：67 OK / 13 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致；lane-000-2 通知前多一行“---”分隔，但原生日志最终消息为纯 JSON，harvest 通过。full contextual（claude/claude-opus-5-5）full-000：10 OK / 3 ISSUE，与 surface 确认项同向。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对16个观察裁决%s，结果75条完成、5条修复、0条pending。修复范围：猎头者挑战“暂停敌人”误述（实为敌人失去对你的锁定）、Exploit Weakness 删近战限定、单项效果抵抗提示泛化为全部状态异常、教程结束文本词中硬换行、思维形态说明多余换行与“狂战士”名不一致。contextual 对猎头者与思维形态判 OK，宿主据源码行为与换行计数维持确认。驳回：全角冒号标签/前缀 ego 末尾空格、翻转胡、暗影割伤结束提示、Hunter! 状态名。advisory：育种棚区域命名族内不一致、entities=怪物。\n\n按1:1节奏，推送后进入修复窗口17，仅处理这5条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
