import pathlib,json
P=pathlib.Path('.ai/task/batch-2a0994cfc83862de29c3')
D={
'f471c037':('refuted',False,'objects/egos/cloak.lua:321 前缀 ego murderer’s （prefix=true）与物品名拼接；中文前缀直接连写（“谋杀者的斗篷”），无需保留英文分词空格，与既往 alchemist’s 裁决一致。'),
'f4754d3c':('confirmed',True,'talents/psionic/psi-archery.lua:238–245 念动弓说明：uses Willpower in place of Strength and Cunning in place of Dexterity to determine attack and damage，现译“决定攻击”漏“伤害”（info 同时显示 combatDamage）；另原文第二行行首为 3 个 TAB，现译为 2 个（一级 TAB 不变量）。整条修复，LF/TAB 与原文逐处一致。'),
'f4765ec9':('advisory',False,'talents/gifts/gifts.lua:31–35 五个龙系天赋类别说明 Take on the defining aspects of a X Drake 全部译为“化身成为X龙形态使你能使用X龙技能”（mod-tome.lua:24999–25007）；“使你能使用……技能”为意译，类别确实提供该系技能，不误导机制；单改本条会破坏族内一致，记 advisory。'),
'f4d315f2':('confirmed',True,'talents/gifts/sand-drake.lua:155–167 Burrow 说明：原文四行均以 \\n\\t\\t 分隔，现译第三行为“\\n”加 5 个空格（一级 TAB 不变量）；burrow into earthen walls 漏“土质”限定。整条修复。'),
'f52f924e':('advisory',False,'general/npcs/troll.lua:146–148 Forest Troll Hedge-Wizard desc：old-looking / muscles appear atrophied 被译为确定的“老迈”“年老力衰”，a certain power 译“一股强大的能量”略有强化；该 NPC str=8、mag=20 为施法者，与外表描述相符，不误导，记 advisory。'),
'f5318eee':('refuted',False,'achievements/quests.lua:221–225 成就 Antimagic!（desc: Completed antimagic training in the Ziguranth camp，mod-tome.lua:2813 译“完成反魔法训练”）；名称“反魔法训练”与说明一致，属成就名意译，同族 Anti-Antimagic!=摧毁反魔法！亦为意译，不误导。'),
'f5651a16':('confirmed',True,'talents/cunning/traps.lua:2182–2211 Nightshade trap short_info：触发时分别 setEffect EFF_STUNNED（canBe stun）与 EFF_POISONED（canBe poison，power=dam/10）；现译“震慑且每回合造成自然伤害”丢失“中毒”状态（中毒免疫可抵挡，可被解毒），机制描述不全。整条修复。'),
'f56e57b6':('confirmed',True,'lore/misc.lua:497 野蛮种族记载；该行位于 mod-tome.lua:43247 的 section "mod-tome/load.lua"（冻结 MISS：load.lua 无此串），但 I18N.lua:100–101/141–143 section 在游戏中不生效、t() 按 src+tag 后写覆盖，故此行覆盖 18126 行（lore/misc 段）成为实际生效译文。现译多处错误：首句误作“没有任何文字可以诠释”、infest 误作“影响”；more advanced form of speech 误作“更为敏捷的速度”；Records … only from the last few hundred years 误作“近一百年”；release hideous acids or belching clouds of darkness 误作“藏在酸雾里或黑暗中”。整条逐句修复（可参照 18126 行较新的译文，但须按原文核对，不照搬其“更为敏捷的速度”增译）。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review265-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==8,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 8 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
