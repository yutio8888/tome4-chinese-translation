import pathlib,json
P=pathlib.Path('.ai/task/batch-abb89c7e815afaa13bb2')
D={
'f36a77c6':('confirmed',True,'timed_effects/physical.lua:1501 CRUSHING_HOLD（grapple，long_desc 每回合受 %d 伤害）与 1876 IMPLODING（缓慢+每回合碾压伤害）的 on_gain 共用该消息，表示正在持续受压；现译“被击碎”表示已被打碎（完成态、毁坏），与持续挤压效果不符。改为“#Target#正被碾压。”。'),
'f36ec8bc':('refuted',False,'load.lua:183 Strength 属性说明原文写 melee damage；实际机制 Combat.lua:1748–1750 combatPhysicalpowerRaw 将 getStr() 直接计入物理强度，TooltipsData.lua:231 同名提示亦写 increases Physical Power、Physical Save。现译“物理强度／物理豁免”贴合实现与游戏内另一处正式说明，不误导。'),
'f3756e2f':('confirmed',True,'dialogs/orders/Behavior.lua:57–61 队友行为菜单 Default/Melee/Ranged/Tank/Standby，同族现译 默认/近战/远程/肉盾；选中后 game.logPlayer 以 _t(item.set) 记录，engine.lua:98 standby=待命。菜单项“乖乖站好”与同族术语风格及选择后的日志“待命”不一致（resolvers.lua:947 standby 战术即原地待命）。改为“待命”。'),
'f3a46f07':('refuted',False,'general/traps/natural_forest.lua:32 自然陷阱 sliding rock（图 trap_slippery_rocks_01，message @Target@ slides on a rock!，未鉴定名 slippery rock=湿滑的石块）；“光滑的石块”指令人滑倒的石头，与陷阱机制（踩上滑倒被震慑）一致，陷阱名不需直译 sliding。'),
'f3bf7c41':('confirmed',True,'talents/techniques/dualweapon.lua:176–205 Offhand Jab：action 先主手 attackTargetWith，再以 barehand 徒手攻击，不使用副手武器；info 原文 in place of your normal offhand attack 与 surprise 被删，现译未说明以徒手攻击替代副手攻击。另原文 2 个 LF，现译在“徒手伤害。”后插入第 3 个换行（一级换行不变量）。整条修复，LF 与原文一致。'),
'f3cf4840':('advisory',False,'timed_effects/other.lua:3024–3046 AEONS_STASIS（temporal，无敌、免疫状态、never_act，long_desc 译“目标处于静滞时空中”），用于 zones/conclave-vault/npcs.lua:37 封存多年的食人魔；“沉睡千年”是意译，与静滞无行动的表现相符但未体现 stasis，且可能与睡眠状态混淆。非机制误导，记 advisory。'),
'f3fa95c7':('refuted',False,'talents/psionic/kinetic-mastery.lua:21 Transcendent Telekinesis 属 psionic/kinetic-mastery（动能系），与 Transcendent Pyrokinesis=卓越热能、Transcendent Electrokinesis=卓越电能（27942/27128）对应灵能三系 kinetic/thermal/charged；“卓越动能”是有意的同族系名映射，技能名与效果名（36326）一致。'),
'f431fee2':('confirmed',True,'lore/misc.lua:768–778 Z’quikzshl 日记：The other ingredients were trivial and in possession of my master 意为其他材料易得且主人手中就有，现译“都太次，并且完全被主人所掌控”错译；末句 all he can manage is a corruption of his own name: Z’quikzshl 指他施法只能吐出自己名字的走样读音，现译“他所能做的只是拥有一个堕落的名字”错译；Ruby of Eldoral 现译“艾德瑞尔之石”丢失“红宝石”。整条修复，保留标记与换行。'),
'f4479615':('refuted',False,'talents/psionic/discharge.lua:186–227 Focused Wrath：把所有攻击性 Discharge 效果集中到单一目标（diverting all offensive Discharge talent effects to it），效果 timed_effects/mental.lua:2284；“集火”贴合实际机制，并与技能名（27194）及效果名（36233）一致。'),
'f44d201c':('advisory',False,'birth/races/undead.lua:330–339 骷髅外观 face 类 Lich Regalia 1–10（gfx/shockbolt/player/skeleton/face_lich_regalia_*.png）；已查看 02/05/09 图层，多为头顶冠饰，个别为小饰物/垂饰。“巫妖王冠”对部分款式偏窄但不误导，且 10 条同族一致，单改本条会破坏族内一致，记 advisory。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review264-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==10,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 10 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
