import pathlib,json
P=pathlib.Path('.ai/task/batch-096b5470a753566196f9')
D={
'540fd310':('refuted',False,'shadows.lua:139/229/601（624a6732）：Shadow Mages 描述中的 Flames 是阴影学会的 SHADOW_FLAMES 技能（name="Shadow Flames"，现行技能名“暗影之火”），不是法术 Flame；译作“暗影之火”与实际技能一致（2026-09-23 Flame 改名裁决同步修订）。'),
'cd2bba07':('refuted',False,'cunning/stealth.lua:24–36 stealthDetection 只累计半径内敌对、未致盲且 act.fov.actors[self]（该敌人能看见你）的角色；“能看见你的敌人”贴合实现，为窗口9已确认的修复文本，不是方向反转。'),
'eaacc62b':('confirmed',True,'world-artifacts.lua:5135 Plate of the Blackened Mind 描述：primal, yet aware 被省略并另加原文没有的“邪恶的”；absorbs all light that touches it 被译成“吸收了附近的所有光线”，deep black 被弱化。完整性缺陷，整句有界修复。'),
'eab2ffb6':('pending',False,'spells/staff-combat.lua:141 Blunt Thrust 为法杖近战单体攻击并眩晕；Thrust 为刺击/戳击，现名“钝器挥击”把动作译成挥击。属技能名改名（需同步技能引用与日志文本），按用户指示列入 pending 集中裁定，不在本批修复。'),
'eab82680':('advisory',False,'Combat.lua:2395–2399 combatMovementSpeed 仅当目标格含 creepingDark 时加算 Dark Vision 移速，即“移动进入黑暗之雾的格子”；“在黑暗之雾中增加移动速度”在实际移动（格内→格内）上基本等价，仅“从外部进入”语感略窄，记 advisory。'),
'eae1dd46':('refuted',False,'objects/egos/digger.lua:69 woodsman\'s 为 prefix 词缀；中文词缀全库惯例不保留尾随空格（如“倒刺的”“致命的”“燃烧的”），与中文名称直接拼接，非格式缺陷。'),
'eafab19d':('confirmed',True,'timed_effects/other.lua:3333–3342 ZONE_AURA_SPELLBLAZE：原文为确定语气 reflects teleportation magic（反射传送魔法），译文“可能干扰传送法术”既把 reflects 弱化为“干扰”又添加原文没有的“可能”。activate 仅改抗性、未实现传送逻辑，源码无法支持更弱或更强的说法，故以原文为准；独立语境复核同向。忠实度缺陷，有界修复警告句。'),
'eb0868d5':('confirmed',True,'lore/misc.lua:725/729：a few decades in the Age of Dusk 被译成“黄昏纪的一些时代”（几十年→时代，时长错误）；cheat at a few lotteries 被译成“和概率开个玩笑”，丢失彩票作弊。忠实度缺陷，两处有界修复。'),
'eb14aef1':('refuted',False,'objects/egos/robe.lua:284 timebroken 为 prefix 词缀；中文词缀惯例不保留尾随空格，非格式缺陷。'),
'eb3a77b2':('refuted',False,'timed_effects/physical.lua:3543 "Caught in a bear trap: "..table.concat(desc)，中文全角冒号后直接接内容为既有排版惯例，非格式缺陷。'),
'eb47fec6':('advisory',False,'dialogs/GraphicMode.lua:81：“每个贴图须按现有贴图集命名”与“所有材质的文件名必须和已存在的默认材质文件名相同”实义一致（按现有贴图集同名），仅 tile 用“材质”用词不一，记 advisory。'),
'eb509ae5':('confirmed',True,'cunning/traps.lua:391–425 bladestorm construct on_act 仅对 reactionToward<0 的相邻敌人 attackTarget；译文“每回合攻击周围生物”把敌人扩大为所有生物并删去“所有”，主语“构造体”也缺失。机制描述缺陷，整句修复。'),
'eb5c2ab3':('confirmed',True,'timed_effects/physical.lua:1494–1502 CRUSHING_HOLD（现行效果名“碾压擒抱”，grapple/pin）；on_lose 文本“脱离了击碎效果”把 crushing hold 误作击碎效果，与效果名不一致，确认修复为挣脱碾压擒抱。'),
'eb6bf55a':('pending',False,'lore/misc.lua:623 传说标题 If I Should Die Before I Wake（睡前祷词句式）；现译“从噩梦中惊醒，还是在梦魇中永眠？”为意译改写，非机制内容，是否直译属风格取舍，列入 pending 待用户集中裁定。'),
'eb71935d':('pending',False,'boss-artifacts-maj-eyal.lua:643–648 Crystal Shard 为 BASE_STAFF magestaff 唯一神器（未鉴定名 crystalline tree branch）；现译“水晶之杖”以物品类型替换 Shard（碎片），属神器专名改名；surface 与 contextual 均提出，是否改为“水晶碎片”等属命名决定，列入 pending 待用户集中裁定。'),
'eb71ffb9':('advisory',False,'zones/tutorial-combat-stats/npcs.lua:495 教程 NPC BORED_ELF_3；Loitering（闲逛）译“流浪的”语义接近，不影响教程理解，记 advisory。'),
'eb7b7fc8':('refuted',False,'class/Actor.lua:2095 ts:add(color, "Resists: ") 后追加抗性列表；中文全角冒号后不留空格为既有排版惯例，非格式缺陷。'),
}
rows=[]
for f in sorted(pathlib.Path('.artifacts/i18n/continuation-20260923/review256-surface-raw').glob('*.json')):
 for r in json.loads(f.read_text())['results']:
  if r['verdict']=='ISSUE':
   m=[v for k,v in D.items() if r['entry_revision_identity'].startswith(k)];assert len(m)==1,r['entry_revision_identity']
   d,rep,why=m[0];rows.append(dict(revision_key=r['entry_revision_identity'],stage='surface',observation=r['observation'],disposition=d,repair_required=rep,conclusion=why))
assert len(rows)==17,len(rows)
(P/'HOST-SURFACE-DECISIONS.json').write_text(json.dumps(dict(status='host adjudicated surface observations; contextual observations adjudicated separately',slid_observations=None,slide_check='each of 17 observations compared against its own entry source/target; none slid',rows=rows),ensure_ascii=False,indent=2)+'\n')
print({d:sum(r['disposition']==d for r in rows) for d in ('confirmed','refuted','advisory','pending')})
