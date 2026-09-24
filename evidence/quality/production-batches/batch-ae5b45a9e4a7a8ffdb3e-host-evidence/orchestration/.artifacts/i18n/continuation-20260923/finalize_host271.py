import pathlib,json,collections
b='batch-ae5b45a9e4a7a8ffdb3e';P=pathlib.Path('.ai/task')/b;A=pathlib.Path('.artifacts/i18n/continuation-20260923')
S=json.loads((P/'HOST-SURFACE-DECISIONS.json').read_text());rows=S['rows']
C={
'fab2d8a9':('confirmed',True,'与 surface 同向：疲劳圣印陷阱 canTrigger 仅对敌对单位触发，现译“所有经过的目标”删去敌方限定。并入同条整句修复。'),
'fac87ff0':('confirmed',True,'与 surface 同向：Dark visions fill your mind，现译丢“幻象/脑海”并增“无尽”。并入同条修复。'),
'fad7958e':('confirmed',True,'与 surface 同向并补充：Actor.lua:5580/5600 bloodcasting 属性改变堕落技能的活力消耗，Corruptions 指堕落系技能/法术，非施法者。并入同条修复。'),
'fae9336c':('confirmed',True,'升级 surface advisory：world-artifacts.lua:3618–3645（624a673）Morrigor（摄魂剑·莫瑞格）special_on_kill 吞噬被杀者灵魂（日志 CONSUMES THE SOUL），取其一项技能作为 use_talent 并可反复充能使用，灵魂并未被放出；taps the trapped soul 是“汲取被困的灵魂”，manifesting %s 是“显现/施展 %s”。现译“放出了…被束缚的灵魂，模仿了%s”把汲取写成释放、施展写成模仿（一级机制）。整条修复，@Source@、#SALMON#…#LAST#、两个 %s 顺序保持（第一个为被杀者名，第二个为技能名）。'),
'fb0879a6':('confirmed',True,'与 surface 同向并补充：archery.lua:64–77 标记判定仅在已学 Master Marksman 或有 mark_steady 时进行，(if capable of marking) 是真实条件；archery.lua:87 incStamina 位于 archery_onhit。两处限定都要补回。'),
'fb643ca9':('confirmed',True,'与 surface 同向并补充：All that this light touches shall be mine 是“光所照之处皆归我有”，现译“阳光所至，即我所至”亦偏。并入同条整句修复（petty gods 保持“伪神”）。'),
'fb817eec':('confirmed',True,'与 surface 同向并补充：第三段 leave that idiot burnt on a stake 是“绑在柱上烧死”，现译“穿在柱子上”（刺穿）与后文火刑不一致。并入同条修复。'),
}
raw=json.loads((A/'review271-contextual-raw/full-000.json').read_text());out=[]
for r in raw['verdicts']:
    if r['verdict']=='OK':continue
    m=[v for k,v in C.items() if r['revision_key'].startswith(k)];assert len(m)==1
    d,rep,why=m[0];out.append(dict(revision_key=r['revision_key'],stage='contextual',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
rows=rows+out;assert len(rows)==22
rep=sorted({r['revision_key'] for r in rows if r['repair_required']});assert len(rep)==8,rep
pend=sorted({r['revision_key'] for r in rows if r['disposition']=='pending'});assert len(pend)==0,pend
counts=dict(collections.Counter(r['disposition'] for r in rows))
final=dict(batch_id=b,observations=len(rows),observation_dispositions=counts,repair_revision_keys=rep,pending_revision_keys=pend,expected_final_states=dict(done=72,repair_required=8,blocked=0),rows=rows,
  reviewers=dict(surface='codex/gpt-6-sol medium auto-review (4 lanes)',contextual='claude/claude-opus-5-5 medium auto (full-000, single accepted attempt)',selection='user instruction 2026-09-23'),
  native_parser='repo review_lifecycle.py accepts Codex 0.156.0 / Claude Code 2.1.280 since b626eaf1; all 80 surface identity echoes pre-checked exact against envelopes before harvest; all 4 lanes and the contextual child harvested via --native-log.',
  notes=['Surface and contextual observations adjudicated independently.','No slid surface observations.','Contextual raised 7 ISSUEs: six agree with host-confirmed surface rows (details added: light-touches line, burnt on a stake, marking condition, bloodcasting mechanism); fae9336c upgraded from surface advisory to confirmed after host verified the Morrigor soul is consumed, not released.','Contextual passed fae23672 (Speed Sap); host keeps it confirmed on the objective newline invariant (source ends with \\n\\t\\t, target has none).','Contextual passed faca87fd, faef48ce, three ego prefixes, fafbf773 and fb9166e7, matching host refuted.','No advisories remain unrepaired.','No pending, no glossary/global rename; old pending/blocked unchanged.'])
(P/'HOST-FINAL-DECISIONS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
dec={r['revision_key'][:10]+'|'+r['stage']:{k:r[k] for k in ('disposition','repair_required','conclusion')} for r in rows};assert len(dec)==22
(A/'review271-host-decisions.json').write_text(json.dumps(dict(workset=f'evidence/quality/production-batches/{b}-source-workset.json',decisions=dec),ensure_ascii=False,indent=2)+'\n')
(P/'WINDOW25-REPAIR-DECISION.json').write_text(json.dumps(dict(trigger='1:1 review/repair cadence after batch 271',window=25,batches=[b],bounded_revision_keys=rep,provisional_until_contextual_adjudication=False,default_max_cycles=3,excluded='all nonblocking advisory; unrelated existing blocked/repair records; no global term renames',revision_count=len(rep)),ensure_ascii=False,indent=2)+'\n')
(P/'HOST-SUMMARY.md').write_text('第271批：80条，全部固定ToME源码，冻结 80/80 命中。四组surface（codex/gpt-6-sol）：65 OK / 15 ISSUE；harvest 前逐位比对 80 个回显 identity，全部一致。full contextual（claude/claude-opus-5-5）full-000：8 OK / 7 ISSUE。5个独立reviewer child 严格收取、原生读取边界人工审计、全部归档确认。\n\n宿主对22个观察裁决%s，结果72条完成、8条修复、0条pending。修复范围：疲劳圣印说明补“敌人”限定；指令水晶球（亡灵）描述改“黑暗的幻象充满脑海”；血祭施法效果说明 Corruptions 改指堕落系法术；减速（Speed Sap）说明补末尾换行；摄魂剑·莫瑞格日志改“汲取被困的灵魂，施展%%s”；第一滴血补“命中时”与“（若能标记）”；夏图尔壁画阿马克泰尔创世文本（伪神逃离、以气息造出太阳、光所照之处皆归我有）；盗匪日志（贵族迟早追杀、绑在柱上烧死）。驳回：成就“伤害很重要”（按条件本地化）、“还没呢，抱歉！”、三个 ego 前缀尾空格、守护药剂（同族命名）、元素法师（本库职业名）。\n\n按1:1节奏，推送后进入修复窗口25，仅处理这8条。\n'%json.dumps(counts,ensure_ascii=False))
print(json.dumps(dict(dispositions=counts,results=final['expected_final_states']),ensure_ascii=False))
