import pathlib,json
P=pathlib.Path('.ai/task/batch-13b90e85d842da2d4f41')
D={
'3572191c':('refuted',False,'corruptions/torment.lua:144–149（624a6732）对每个冷却中且非 fixed_cooldown 的技能分别 rng.percent(c)；“每个冷却中的技能各有 %d%% 概率减少 1 回合冷却时间”为修复窗口11经 REVIEW/FINAL 独立复核确认的按实现表述（AGENTS.md：机制以源码实际行为为准），英文原文措辞与实现不符。'),
'ed3323c6':('refuted',False,'gifts/venom-drake.lua:21–22、gifts.lua:35：Acidic Spray 属 wild-gift/venom-drake 技能树（venom drake aspect=毒龙形态，venom drake=毒龙）；acid drake talents 指该树，“毒龙系技能”与游戏内树名一致，并非元素误译。'),
'ed41bdd6':('advisory',False,'timed_effects/mental.lua:220–229 DOMINANT_WILL_BOSS（desc Mental Domination=精神控制，subtype dominate，on_gain “mind is dominated”=精神被操控）：shaken 字面为“动摇”，“精神被支配”与效果机制一致，不构成机制误导；可选改“动摇”更贴字面。'),
'ed521ffd':('refuted',False,'general/objects/egos/shield.lua:224 ego 前缀 "exposing "；中文前缀同族约定不带尾空格（barbed →倒刺的、deadly →致命的等，mod-tome.lua:9568/9571），拼接后无显示问题。'),
'ed8673e4':('confirmed',True,'birth/classes/warrior.lua:343 Brawler 描述：列举 pit-fighter、boxer、amateur practitioner 三类，译文漏 pit-fighter（地下格斗士/角斗拳手），且 the Brawler\'s skills 被泛化为“格斗技能”丢失职业名“格斗家”（classes.tsv:23 Brawler=格斗家）。整句修复。'),
'ed86ff05':('confirmed',True,'zones/town-point-zero/npcs.lua:134：A timeless elf…his age is impossible to determine；译文“中年精灵”凭空断定年龄，与后句“不知道他活了多久”自相矛盾。修为“一位看不出年岁的精灵”一类。'),
'edc13e8a':('advisory',False,'chats/tannen.lua:153–157：Tannen 让玩家回去问精灵时空术士是 inverted 还是 reverted 概率场，玩家答 I\'ll return with the answer（会带着答案回来）；“我会回去寻找答案的”意图相近（回去问→带回），方向表述不同但不误导玩法；可选改“我会带着答案回来的”。'),
'edc38802':('refuted',False,'timed_effects/mental.lua:2622–2629 HIDDEN_RESOURCES 的 on_lose 在效果结束时触发（on_gain “#Target#\'s focuses.”），效果整体结束，“不再集中意志”与机制一致；原文 loses some focus 为上游措辞（且有语法错误），非漏译程度词的机制缺陷。'),
'edc794ff':('confirmed',True,'quests/starter-zones.lua:56 岱卡拉任务日志：the huge fire dragon that dwelled there，译文“这里的火龙”漏 huge（巨大的）且 there→“这里”视角偏差。修为“盘踞在那里的巨型火龙”一类。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review258-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==9,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 9 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
