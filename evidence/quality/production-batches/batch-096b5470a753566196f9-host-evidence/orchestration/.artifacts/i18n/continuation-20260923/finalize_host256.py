import pathlib,json,collections
b='batch-096b5470a753566196f9';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'eaacc62b':('confirmed',True,'与 surface 键同一缺陷的独立语境复核：world-artifacts.lua:5135 Plate of the Blackened Mind，primal, yet aware 被删、dark 改“邪恶”、absorbs all light that touches it 误作“吸收附近的所有光线”。确认整句修复。'),
'eafab19d':('confirmed',True,'与 surface 键同向：other.lua:3336 reflects teleportation magic 被弱化为“可能干扰传送法术”；activate 不实现传送逻辑，以原文为准。确认修复警告句。'),
'eb0868d5':('confirmed',True,'独立语境复核补充并经宿主核验 lore/misc.lua:725–735：除 surface 键的 a few decades→“一些时代”与 cheat at a few lotteries 丢失外，fair game 习语被直译为“公平竞赛”（原意为可以随意下手、不受约束的时段），what is, quite literally, the best roast-yeti restaurant 被误译为“只有我们可以毫不客气地说”。四处一并有界修复。'),
'eb509ae5':('confirmed',True,'与 surface 键同一缺陷：traps.lua bladestorm construct on_act 仅 attackTarget reactionToward<0 的相邻目标；译文缺主语“构造体”，“周围生物”扩大对象并删“所有”。确认整句修复。'),
'eb5c2ab3':('confirmed',True,'与 surface 键同一缺陷：physical.lua:1494–1502 CRUSHING_HOLD（grapple/pin，现行效果名“碾压擒抱”），“脱离了击碎效果”误译，确认修复为挣脱碾压擒抱。'),
'eb71935d':('pending',False,'与 surface 键同一命名问题：Crystal Shard（magestaff 唯一神器）现译“水晶之杖”，Shard 未保留；属神器专名改名，列入 pending 待用户集中裁定。'),
}
raw=json.loads((A/'review256-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==23
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==5,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==3
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=72,repair_required=5,blocked=3),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; harvested via --native-log directly, no bypass; surface lane-000-0 re-harvested via --raw after host hand-attribution of one mis-echoed identity (original bytes in captures256/lane0-original.raw).',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Pending per user 2026-09-23 instruction: disputed items go to evidence/quality/pending-user-review.md, state blocked, not repaired.','No glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==23
(A/'review256-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW10-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 256',window=10,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; 3 pending (blocked) revisions awaiting user review; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第256批：80条，全部固定ToME源码。四组surface（codex/gpt-6-sol）：63 OK / 17 ISSUE，逐条比对无错位（lane-000-0 一条 OK 结果回显 identity 错 17 位，经原生日志核实后宿主 hand-attribution 恢复）；一组full contextual（claude/claude-opus-5-5）：10 OK / 7 ISSUE。5个独立reviewer严格收取、原生读取边界人工审计（lane-000-2 因 sandbox 失败经 Paseo 终端只读读取，终端已关闭）、全部归档确认。\n\n宿主对23个观察裁决%s，结果72条完成、5条修复、3条pending（blocked）。修复范围：Plate of the Blackened Mind 描述、魔法大爆炸区域效果传送警告、时空特工入职信（几十年/fair game/彩票/quite literally）、刀刃风暴构造体 short_info、碾压擒抱解除提示。驳回：Shadow Mages 暗影之火、潜行“能看见你的敌人”、两个前缀尾空格、两处冒号尾空格。pending：技能名 Blunt Thrust（钝器挥击）、传说标题 If I Should Die Before I Wake、神器名 Crystal Shard（水晶之杖）。\n\n按1:1节奏，推送后进入修复窗口10，仅处理这5条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
