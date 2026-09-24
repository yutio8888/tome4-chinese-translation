import pathlib,json,collections
b='batch-35fcb3df1560de7c5b2d';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'f7641a73':('confirmed',True,'与 surface 同向并补充：timed_effects/other.lua:2604–2621 CLOAK_OF_DECEPTION long_desc 为 making it look human，activate 设 fake_race="Human"、fake_subrace="Cornac" 并改阵营为 allied-kingdoms；是伪装成人类而非“像活着”。整条修复为“看起来像人类”。'),
'f8180dfe':('confirmed',True,'与 surface 同向并补充：world-artifacts-far-east.lua:57 unided_name 为 a gray and gold pendant，赤铁矿月亮为灰色；“红月”与灰金配色矛盾且丢失 golden。整条修复为“赤铁矿之月遮蔽金色太阳”一类。'),
'f83a8191':('confirmed',True,'与 surface 同向：npcs.lua:1386 Corrupted vapour rises at the target location；现译丢主语、把“蒸腾”作及物。整条修复。'),
'f894de79':('confirmed',True,'与 surface 同向并补充：ooze.lua:36 getMax 受 checkMaxSummon 召唤上限与技能等级双重限制；ooze.lua:112–119 伤害均摊只在技能生效期间成立；另漏 within your line of sight。整条修复。'),
}
raw=json.loads((A/'review268-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==12
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==6,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=74,repair_required=6,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual passed f78b208a (eel tail) and f7bd4de1 (Urkis achievement); host keeps both confirmed on direct source comparison: “It doesn\'t much matter” is not “没有确切的答案”, and “mad”/“onslaught” are dropped.','Contextual passed f7dcde0d and f82b8760, matching host refuted (both translations follow the implementation).','freeze_workset 1 MISS: “Oh well, maybe later then.” rowed under chats/last-hope-lost-merchant.lua while the string lives in chats/artifact-maker.lua:89; translation effective by string lookup, entry passed review.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==12
(A/'review268-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW22-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 268',window=22,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第268批：80条，全部固定ToME源码，冻结 79/80 命中（1 条孤儿目录行：artifact-maker 对话串挂在 last-hope-lost-merchant 段下，按字符串查找仍生效）。四组surface（codex/gpt-6-sol）：72 OK / 8 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000：4 OK / 4 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对12个观察裁决%s，结果74条完成、6条修复、0条pending。修复范围：欺诈斗篷“看起来像人类”（误作像活着）、电鳗尾“其实没多大关系”、厄奇斯成就漏 mad/onslaught、太阳堡垒创建者挂坠的赤铁矿之月与金色太阳、腐化蒸汽主语缺失、分裂（Mitosis）漏视线内/召唤上限/技能生效期间三处限定。驳回：瞬间技能失败日志（补出的“本回合无法再次使用”即实现行为）、难辨构造暴击说明（译文贴合 ignore_direct_crits 按比例削减暴击倍率的实现）。\n\n按1:1节奏，推送后进入修复窗口22，仅处理这6条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
