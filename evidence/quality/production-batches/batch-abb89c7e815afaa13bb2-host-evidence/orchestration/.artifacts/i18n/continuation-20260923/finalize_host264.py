import pathlib,json,collections
b='batch-abb89c7e815afaa13bb2';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f36a77c6':('confirmed',True,'与 surface 同向：physical.lua:1501/1876 CRUSHING_HOLD 与 IMPLODING 的 on_gain，持续挤压状态（配对 on_lose 为挣脱/摆脱），“被击碎”误述为已毁坏，改“正被碾压”。'),
'f3bf7c41':('confirmed',True,'与 surface 同向：dualweapon.lua:176–205 Offhand Jab 以徒手突袭替代副手常规攻击（action 仅主手+barehand），现译删去替代关系与 surprise；并修正多出的第 3 个换行。'),
'f431fee2':('confirmed',True,'与 surface 同向：lore/misc.lua:768–778 trivial 误译为“太次”、corruption of his own name 误译为“拥有一个堕落的名字”；另同句“它/他”混用（原文均 He）一并修正，Ruby of Eldoral 补“红宝石”。整条修复。'),
}
raw=json.loads((A/'review264-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==13
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==4,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=76,repair_required=4,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; all 80 surface identity echoes pre-checked exact against envelopes before harvest; no hand attribution in this batch. lane-000-3 first MCP create_agent call was rejected by client-side schema validation before creation; exactly one lane-000-3 child exists and was bound.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f3756e2f (Standby); host keeps it confirmed on objective evidence: Behavior.lua:51–61 logs the chosen behavior via _t(item.set) and engine.lua:98 renders standby as 待命, so the menu label 乖乖站好 disagrees with the log output for the same option and with sibling labels 默认/近战/远程/肉盾.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==13
(A/'review264-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW18-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 264',window=18,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; no pending in this batch; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第264批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：70 OK / 10 ISSUE，harvest 前逐位比对 80 个回显 identity 全部一致。full contextual（claude/claude-opus-5-5）full-000：7 OK / 3 ISSUE，与 surface 确认项同向。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对13个观察裁决%s，结果76条完成、4条修复、0条pending。修复范围：“#Target# is being crushed”误译“被击碎”（持续挤压状态）、队友行为菜单 Standby“乖乖站好”与日志“待命”及同族不一致、Offhand Jab 删去“替代副手攻击”并多一处换行、Z’quikzshl 日记两处语义误译与 Ruby of Eldoral 丢“红宝石”。contextual 对 Standby 判 OK，宿主据日志输出与同族译法维持确认。驳回：Strength 说明（贴合物理强度实现）、sliding rock、卓越动能（同族系名）、集火（贴合机制）。advisory：Aeons Stasis“沉睡千年”意译、Lich Regalia“巫妖王冠”族内一致但偏窄。\n\n按1:1节奏，推送后进入修复窗口18，仅处理这4条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
