# 批阅裁决台账 — batch-14

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`23f6041a24b497f74746ffcfcdd939c25ecaa2be6db8f08a71a50e22bb540234`
- 决策行：40；冻结修订（含孪生载体）：25
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 25 |

## 被驳回／未采纳的模型主张

| entry | 模型主张 | 裁决 | 理由 |
| --- | --- | --- | --- |
| entry-00244 | 去掉 ` area effect` 的前导空格造成中文拼接缺陷 | rejected | 模型主张补回空格。固定源码 MapEffects.lua:23 为 `dam_def.name .. _t" area effect"` 直接拼接，补空格会显示「火焰 范围效果」，反证模型建议有害。 |
| entry-00221 | 「离开地图」构成明显误译 | rejected | 模型自标 advisory。源码 Game.lua:926-936 的 can_change_level 阻止任何换层/换区域，「离开地图」覆盖该限制，功能含义正确；level/zone 统一译法属跨条目策略，非本条缺陷。 |
| entry-00345 | 「使这次攻击发生偏斜」弱化招架，应改「招架」 | rejected | 模型自标 advisory。源码确认招架成功挡住攻击，现译保留防御成功含义，属文风偏好，不构成缺陷。 |
| entry-00185 | 方括号内多空格 | rejected | 模型自标 advisory。用户策略明确纯静态排版不算缺陷；方括号不属「括号不一致」策略范围。 |
| entry-00254 | 「最大 50%」与同组「最大40%」排版不一致 | rejected | 模型自标 advisory；仅为数字前空格差异，属纯静态排版，按用户策略不整理。 |
| entry-00419 | 「超过1500点」与同组「超过 600 点」空格不一致 | rejected | 模型自标 advisory；纯静态排版差异，按用户策略不整理。 |
| entry-00428 | 三扇传送门句式与同系列不平行 | rejected | 模型自标 advisory；条件、数量、机制均正确，句式平行属文风偏好。 |
| entry-00334 | 「杀死」应为「击杀」 | rejected | 模型自标 advisory；日志在敌人 on_die 中输出，「杀死」与触发事实一致，击杀仅为界面习惯差异。 |
| entry-00434 | 「珠宝匠托付」应改为更贴近源码关系 | rejected | 模型自标 advisory；Master Jeweler 对应珠宝匠，译文为可接受意译，任务名已增补，无缺陷。 |
| entry-00393 | 复合后缀外层半角括号 | rejected_on_entry | 本条 entry-00393 本身已是全角；模型所指的半角外层括号实际出现在 entry-00395–00400（同一 hrq-00046 行的其他载体），已按 bracket_fullwidth 修复那些载体。 |
| entry-00184 | 「勇敢的向前」语病、段间缺空行 | accepted_upstream | 缺陷成立，但主工作区 HEAD 11b3e963 已修（已核逐字）。按 SPEC 规则不在本 worktree 重复修改，记 defer；不接受在本分支重复改。 |

## 逐条裁决

| queue_id | entry_id | 文件:行 | 模型意见 | ORCHESTRATOR 裁决 | 是否落实 | 理由 |
| --- | --- | --- | --- | --- | --- | --- |
| hrq-00532 | entry-03933 | tome-orcs.lua:5112 | fix | accepted | 是 | 独立核验通过；hrq-00532：最强反证是“最多弹射 %d 次”与“弹射至其他目标”已概括主要效果；但冻结源码 on_stop_check 在未命中生物时区分撞上阻挡地形（照常弹射）与落空（直接终止），这两项条件和“你能看到的敌人”（canSee 过滤）均为原文明确且源码实现的条件，现译缺失，属完整性缺陷。cunning and dexterity 按术语库 Cunning=灵巧、Dexterity=敏捷补全。按模型提醒，不写“距当前撞击点最近”， |
| hrq-00533 | entry-03939 | tome-orcs.lua:5186 | fix | accepted | 是 | 独立核验通过；hrq-00533：最强反证是两句都报告抵抗震慑、结果可理解；但冻结源码中 blow 是对主目标的日志，shock 是半径 3 冲击波波及的次要目标日志，两条不同原文现译完全相同，丢失了冲击波来源信息。改为“震慑冲击”，与同族 blow=打击 区分，成本低且不影响其他条目。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00534 | entry-03940 | tome-orcs.lua:5210 | fix | accepted | 是 | 独立核验通过；hrq-00534：最强反证是“击中”可宽泛表示碰撞；但冻结源码该日志在 knockback 回调中、检测到 block_move 后输出，%s 是被击退后撞上障碍的目标，“击中了某物”把被动撞击写成主动攻击且丢失 solid。改为“撞上了坚固的物体”；pulse 与同节说明“静电脉冲”对齐为“脉冲”。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00535 | entry-03946 | tome-orcs.lua:5320 | fix | accepted | 是 | 独立核验通过；hrq-00535：最强反证是“冷却时间减半”在多数情况下结果等价；但冻结源码 MECHARACHNID_PILOTING_BUFF 的 on_timeout 是每回合对已有冷却额外再减 1（跳过 fixed_cooldown），并非改写基础冷却时长，“冷却时间减半”会被读成使用技能时冷却值减半。改为“冷却速度加倍”，并与 mod-tome 既有“刻印冷却速度加倍”（cooldown twice as fast）同族一致。英文 all  |
| hrq-00536 | entry-03950 | tome-orcs.lua:5374 | fix | accepted | 是 | 独立核验通过；hrq-00536：①“灵晶射击”不是同节技能名，冻结源码技能名 Metalstar 本仓译“金属灵晶”（tome-orcs.lua 同节 talent name），改为“发射金属灵晶”；②shrapnel still inside 被略成“灵晶碎片”，补“仍残留在目标体内的弹片”（同节 Metalstar 说明亦用“弹片”）；③冻结源码 free=getTalentRadius(mt)*2，格式化参数同样已乘 2，现译“范围（当前 % |
| hrq-00537 | entry-03951 | tome-orcs.lua:5403 | no_change | accepted | 否 | 无需修改；hrq-00537：模型自标 advisory。tinker 术语记录“蒸汽工具”为 existing（非 preferred），不强制改名；现译“制造药剂、附着物等道具”与同节技能名“制造道具”一致，所举药剂与附着物均为冻结源码中可制造的 tinker 类别，未失义。仅记表达建议。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00538 | entry-03953 | tome-orcs.lua:5416 | fix | accepted | 是 | 独立核验通过；hrq-00538：冻结源码明确把弹药的 ranged_project 转为 melee_project 后调用 attackTargetWith，即“远程近战攻击，但也触发弹药远程特效”；现译“射击是远程攻击将会触发弹药特效”丢失 melee 与转折，属机制性缺失。voratun 术语库 preferred=沃瑞钽，“沃瑞钽钢”不符，同条修正。额外射击实际由技能等级≥5 决定而非材质，属英文原文与实现不一致，中文沿袭英文，不计中文错误 |
| hrq-00539 | entry-03960 | tome-orcs.lua:5483 | fix | accepted | 是 | 独立核验通过；hrq-00539：最强反证是施法语境可推知治疗他人；但冻结源码 heal_check 明确要求 act ~= self，且 cone 设 selffire=false，原文 other 是实际限制，现译“修复机械生物”未排除自身。补“其他”，其余文字与换行不动。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00540 | entry-03967 | tome-orcs.lua:5552 | fix | accepted | 是 | 独立核验通过；hrq-00540：冻结源码 action 先 archeryAcquireTargets/archeryShoot，archery_onhit 再在命中点 project 爆炸，“每一个弹片”把 each shot 写成爆炸后碎片，顺序颠倒，改为“每发子弹抵达目标时”。hrq-00541：as it is the ammo 的因果被省略，按同节其他三条爆炸弹／钩索弹已用的“这个技能本身就是弹药，因此不消耗弹药”补全。hrq-00542 |
| hrq-00543 | entry-03970 | tome-orcs.lua:5594 | fix | accepted | 是 | 独立核验通过；hrq-00543：冻结源码 pull(x,y,distance) 以数值为上限，受阻挡时移动不足额，两处补“至多”。hrq-00544：补“技能本身就是弹药”因果，同 hrq-00541。hrq-00545（advisory）：hook shot 的钩索特征与“打击”暗示伤害的问题成立，源码 action 只拉动不造成伤害，顺带改为“发射特殊的钩索弹”，不引入新机制。各行无句末标点的原样式保持。兽人 DLC 来源未固定（仅核冻结快照） |
| hrq-00546 | entry-03971 | tome-orcs.lua:5610 | fix | accepted | 是 | 独立核验通过；hrq-00546：冻结源码续发效果为 type="beam" 投射配 lightning 粒子，不是球体，“闪电球”给出错误形状，改为“每道闪电”“闪电伤害”。hrq-00547：循环上限为 floor(技能等级)，敌人不足即 return，补“附近至多 %d 名敌人”。hrq-00548：补“技能本身就是弹药”因果。hrq-00549（advisory）：voltaic 被泛化，补“电能弹”使首句完整。兽人 DLC 来源未固定（仅核 |
| hrq-00550 | entry-03972 | tome-orcs.lua:5628 | fix | accepted | 是 | 独立核验通过；hrq-00550：冻结源码 addEffect 使用 DamageType.NOURISHING_MOSS，Nourishing Moss 为具名效果；本仓 mod-tome 已有同名技能译“生命苔藓”，按既有译名补全，不新造译名。hrq-00551：补“技能本身就是弹药”因果。hrq-00552：“造成…伤害对…每一个敌人”语序不通，改为“对…造成…伤害”；botanical 顺带补为“植物弹”。占位符顺序（半径、回合）不变。兽人  |
| hrq-00553 | entry-03973 | tome-orcs.lua:5649 | fix | accepted | 是 | 独立核验通过；hrq-00553：global speed 术语库 tformat/global 为 preferred=全局速度，notes 明确不写“整体速度”，必须采用。hrq-00554：冻结源码 getPower 同时作为 METAL_POISONING 的 power 与 speed（-10），Toxin strength 涵盖伤害与减速，“枯萎伤害受…加成”限缩为伤害，改为“毒素强度”。hrq-00555：补“技能本身就是弹药”因果。h |
| hrq-00557 | entry-03977 | tome-orcs.lua:5742 | fix | accepted | 是 | 独立核验通过；hrq-00557（advisory）：原文 The power and damage 两项，现译只写“伤害”，删去一项属完整性缺失，补“强化效果与伤害”；接受模型更正：冻结源码实际流血增幅调用 getDamage，getDamageInc 仅用于说明格式化，这是英文与实现差异，不计中文错误，译文仅对齐原文两项。hrq-00558（advisory）：“放在伤口上”丢失 slam into 的猛烈动作与反讽，改为“猛插进”；按判据 5  |
| hrq-00560 | entry-03984 | tome-orcs.lua:5853 | fix | accepted | 是 | 独立核验通过；hrq-00560（advisory）：最强反证是“进入其大脑”已传达侵入与干扰；但 latch on 与 bore into its skull 的附着、钻入动作被合并省略，且需与同批 entry-04008（bores into→钻入）同族一致，故补为“附着其上并钻入其头骨”。模型所述 -%d%% 双重负号不可照译、现译“减少 %d%%”正确，予以确认不改（冻结源码 fear_immune/sleep_immune 为减值）。兽人  |
| hrq-00561 | entry-03985 | tome-orcs.lua:5890 | refuted | accepted | 否 | 驳回模型主张；hrq-00561：模型结论已为 refuted。现译“没有足够的空间召唤！”与原文语义、感叹号一致；初审所引 preferred 记录 source_tag 为 logSeen，本条为 logPlayer，不构成必须逐字匹配依据；该原文在多组件（mod-tome/cults/ashes）存在同源孪生，单改本条反会制造族内不一致。无缺陷。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00562 | entry-03990 | tome-orcs.lua:5951 | fix | accepted | 是 | 独立核验通过；hrq-00562（advisory）：最强反证是“（或任何其他目标）”位于施加动作主语位置，可读作施加方；但“目标”在本句同时指承受效果的生物，容易被读成受害方。冻结源码 superload Combat.lua 的 crossTierEffect 在受效果者身上判定 INCOMING_DISASTERS，未限定施加者，any others 即任意施加方，改为“其他任何人”。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00563 | entry-03996 | tome-orcs.lua:6002 | fix | accepted | 是 | 独立核验通过；hrq-00563：冻结源码 callbackOnTakeDamage 首行 src ~= self.summoner 即返回，只有召唤者造成的法术伤害才触发；现译“其受到的法术伤害”扩大了触发来源，补“你对其造成的”。源码实际倍率 1.3 而英文描述 160%，属英文与实现差异，中文沿袭英文，不改数值。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00564 | entry-03997 | tome-orcs.lua:6019 | fix | accepted | 是 | 独立核验通过；hrq-00564：C03.1 冻结源码 electricity.lua 奥术发电机为 tinker，需装入长袍（衣物槽）而非玩家“装备长袍”，末段“装备在长袍中”不能消除本句前提偏差，改为“将奥术发电机装入长袍后”；C03.2 冻结源码 getSpellpower 读取 getSteam()/100，是当前蒸汽量，改“当前蒸汽量”。hrq-00565：dabble in 为涉猎、尝试，现译“精通于”提升了程度，改“涉猎”；同句“他”与 |
| hrq-00566 | entry-04000 | tome-orcs.lua:6060 | fix | accepted | 是 | 独立核验通过；hrq-00566（advisory）：最强反证是“启动时”可理解为自启动起持续；但冻结源码该技能 mode=sustained，疲劳在持续开启期间生效，while active 更精确对应“开启期间”，改为“开启期间会增加 20%% 疲劳”，其余不动。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00567 | entry-04001 | tome-orcs.lua:6074 | no_change | accepted | 否 | 无需修改；hrq-00567：模型自标 advisory 并承认等价读法。冻结源码为 steam_regen/stamina_regen 等回复属性，回复值在游戏中按回合结算，“蒸汽回复 +6”“体力回复 + 4”数值与效果无偏差；“+ 4”空格属纯静态排版，按判据 6 不改。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00568 | entry-04008 | tome-orcs.lua:6167 | fix | accepted | 是 | 独立核验通过；hrq-00568：冻结源码 MIND_DRONE 的 on_gain 日志在效果施加时输出，对应技能说明“附着并钻入头骨”，而非飞行过程；“飞入”只表达移动，改“钻进”。量词“一个”改“一只”，与同族“5 只精神雄蜂”一致。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00569 | entry-04014 | tome-orcs.lua:6269 | no_change | accepted | 否 | 无需修改；hrq-00569：模型自标 advisory。“目标被化学药剂注射”语序略生硬，但被动句主体仍是目标、三类豁免（冻结源码 combat_mentalresist/spellresist/physresist）降低含义无偏差，属二级语感问题，仅记 advisory。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00570 | entry-04015 | tome-orcs.lua:6272 | fix | accepted | 是 | 独立核验通过；hrq-00570：最强反证是冻结源码 on_timeout 确在 life==max_life 时移除效果，现译的增补有依据；但 on_timeout 在定时效果每回合结算时才检查（固定 engine ActorTemporaryEffects.lua timedEffects），并非生命回满当刻，“立即”给出源码未保证的时序，改为“回满后结束”。三个占位符顺序不变。兽人 DLC 来源未固定（仅核冻结快照）。 |
| hrq-00571 | entry-04018 | tome-orcs.lua:6318 | fix | accepted | 是 | 独立核验通过；hrq-00571（advisory）：最强反证是句首已限定为射出的子弹，可自然理解为命中时判定；但 When striking 是原文明确的触发条件，冻结源码 superload Archery.lua 亦仅在命中挂钩中判定，补“命中时有”成本低且不改占位符顺序。兽人 DLC 来源未固定（仅核冻结快照）。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
