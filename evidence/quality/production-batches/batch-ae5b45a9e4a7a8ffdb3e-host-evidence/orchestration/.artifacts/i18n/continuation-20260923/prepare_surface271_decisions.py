import pathlib,json
P=pathlib.Path('.ai/task/batch-ae5b45a9e4a7a8ffdb3e')
D={
'fab2d8a9':('confirmed',True,'talents/celestial/other.lua:385–420（624a673）Glyph of Fatigue（疲劳圣印）：陷阱 canTrigger 仅在 who:reactionToward(summoner)<0（敌对）时触发；原文 All enemies walking over the glyph，现译“所有经过的目标”删去敌方限定（删限定词类，读作对任何经过者生效）。整条修复为“所有经过圣印的敌人”一类，其余逐句对照。'),
'fac87ff0':('confirmed',True,'general/objects/quest-artifacts.lua:177 Orb of Undeath（指令水晶球（亡灵））描述：Dark visions fill your mind as you lift the orb.——现译“无尽的黑暗扑面而来”丢了“幻象”“充满脑海”并增添“无尽”（一级 fidelity）。整条修复为“黑暗的幻象充满你的脑海”一类，第二句保持。'),
'faca87fd':('refuted',False,'achievements/kills.lua:26–28 成就 Size matters 描述 Did over 600 damage in one attack.；“伤害很重要”是按成就条件本地化双关，非错译，驳回。'),
'fad7958e':('confirmed',True,'timed_effects/magical.lua:2456–2460 BLOODCASTING（血祭施法）效果说明：Corruptions consume health instead of vim.——Corruptions 指堕落系法术（本库同类说法“堕落系法术需要消耗…”），现译“堕落者”把法术误作施法者（一级 fidelity）。整条修复为“堕落系法术消耗生命值而非活力值”一类。'),
'fae23672':('confirmed',True,'talents/misc/npcs.lua:1650–1655 Speed Sap（减速）说明（tformat）：原文以 \\\\n\\\\t\\\\t 结尾（1 个 LF、2 个 TAB），现译 0 个 LF（一级换行不变量，与既往裁决一致）。整条修复：末尾补回 \\\\n\\\\t\\\\t，其余逐句对照（for three turns 持续三回合）。'),
'fae9336c':('advisory',False,'general/objects/world-artifacts.lua:3642：第一个 %s 为被束缚灵魂的主人名、第二个为 use_talent.name（施放的技能名）；中文“%s的被束缚的灵魂”语序调整合法，占位符顺序未变；manifesting 译“模仿了”不如“显现出”贴切，但读者可理解为施放该技能，记 advisory。'),
'faef48ce':('refuted',False,'chats/elisa-orb-scrying.lua:94–99：伊莉莎问“有新东西给我看吗？”，选项 Not yet sorry! 是“还没有，抱歉！”（原文省逗号），现译正确，驳回。'),
'faf17c19':('refuted',False,'ego 前缀 naturalist\'s（prefix，与物品名拼接）；中文前缀全库惯例不保留尾随空格，与既往 exposing/starlit/timebroken 裁决一致，驳回。'),
'faf4b270':('refuted',False,'ego 前缀 dragonslayer\'s（prefix）；同 faf17c19，驳回。'),
'fafbf773':('refuted',False,'chats/alchemist-elvala.lua:39、quests/brotherhood-of-alchemists.lua:275 炼金兄弟会药剂名；本库同族药剂按效果意译（elixir of the fox→“狡诈药剂”，mod-tome.lua:20149），“守护药剂”为既有同族命名，非错译，驳回。'),
'fb0879a6':('confirmed',True,'talents/techniques/marksmanship.lua:38–49 First Blood（第一滴血）；archery.lua:80–87 incStamina 位于 archery_onhit 回调，仅命中时回复体力。现译“回复 %0.1f 体力”删去 on hit（删限定词类），且漏 (if capable of marking)。整条修复：补“命中时”“（若能标记）”，其余逐句对照。'),
'fb2278dc':('refuted',False,'ego 前缀 aegis（prefix）；同 faf17c19，驳回。'),
'fb643ca9':('confirmed',True,'lore/shertul.lua（624a673）夏图尔壁画文本（阿马克泰尔创世）：the petty gods fled before his glory 是“逃离”，现译“慑服”；he made the Sun from his breath 是“以气息造出太阳”，现译“他深呼吸后把太阳高举”丢了创造；his might surpassed all else 译“震慑了众人”亦偏（一级 fidelity）。整条修复，#{italic}#/#{normal}# 保持。'),
'fb817eec':('confirmed',True,'lore/misc.lua:656 起盗匪日志：Only a matter of time until that nobleman catches wind and comes after us 是贵族迟早会追杀他们（威胁），We were about to get more gold … for his lassie back 是本来即将拿到赎金；现译合成“只要再等贵族听到风声过来找我们就可以榨取一大笔钱”，把威胁写成计划（一级 fidelity）。整条修复该段，其余段落逐句对照、3 处 \\\\n\\\\n 保持。'),
'fb9166e7':('refuted',False,'Archmage 本库职业名为“元素法师”（birth descriptor name，mod-tome.lua:3021），现译与职业名一致，驳回。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review271-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==15,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 15 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
