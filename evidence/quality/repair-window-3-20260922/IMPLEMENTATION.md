# 修复窗口 3 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次只修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 14 个 target；source、section、source_tag、args_order、special、占位符、markup 以及各 target 原有换行和 tab 序列保持不变。

其中 11 条来自三个已成功的真实 production repair preflight；`dff11a9be5…`、`e1343327ea…`、`e200845e1a…` 是宿主独立授权补充。三条补充没有被伪装成 `repair_required`，也没有拼成虚构的单一生产批次。三个原始 `PREFLIGHT-BATCH*.json` 在本目录逐字节保存，schema 未改。

## 数值 placeholder 值流

`index` 按 source 中格式占位符出现顺序计数。`%s` 虽非数值，也列出以闭合 grapple 的完整参数排列。

| revision | index | token | quantity_kind | producer | consumer |
| --- | ---: | --- | --- | --- | --- |
| `df61b36589…` | 1 | `%d` | duration_turns | `duration = floor(combatTalentScale(4,8))` | `setEffect(EFF_MASTERFUL_TELEKINETIC_ARCHERY, duration)`；持续期间 `callbackOnActBase` 每回合攻击 |
| `df8f5280bf…` | 1 | `%d` | summon_cap | `getMaxShadows()` | `summonShadow()` 在 `shadowCount >= cap` 时停止补召 |
| `df8f5280bf…` | 2 | `%d` | actor_level | `getLevel() = self.level` | 新阴影 `forceLevelup(level)` |
| `df8f5280bf…` | 3 | `%d` | talent_level | `getHealLevel()` | 阴影的 `T_HEAL` 等级 |
| `df8f5280bf…` | 4 | `%d` | talent_level | `getBlindsideLevel()` | 阴影的 `T_SHADOW_BLINDSIDE` 等级 |
| `df8f5280bf…` | 5 | `%d` | damage_reduction_percent | `getAvoidMasterDamage()` | 阴影保存剩余伤害倍率 `(100-value)/100`；主人造成伤害时由 `onTakeHit` 乘该倍率 |
| `dfdfbe6089…` | 1 | `%0.1f` | damage_bonus_percent | `getDamageIncrease()` | `inc_damage[DamageType.ARCANE]` |
| `dfdfbe6089…` | 2 | `%d` | resistance_penetration_percent | `getResistPenalty()` | `resists_pen[DamageType.ARCANE]` |
| `dfdfbe6089…` | 3 | `%d` | effect_removal_cap | `getNbRemove()` | 5 级时 `removeEffectsFilter(..., count)`，最多移除该数量的魔法或物理负面效果 |
| `dff11a9be5…` | 1 | `%d` | heal_conversion_percent | `getConversion()*100` | 每个流血效果贡献 `eff.power*eff.dur*conversion`，逐项计入总治疗 |
| `dff11a9be5…` | 2 | `%d` | minimum_heal_per_bleed | `getMinHeal()` | 每个流血效果分别执行 `math.max(converted_remaining_damage, healMin)` |
| `dff11a9be5…` | 3 | `%d` | duration_extension_turns | `getExtension()` | 睡眠时长为目标最长流血剩余时长 `dur` 加该值 |
| `e0886c07f…` | 1 | `%d` | ranged_defense_modifier | `eff.power` | `combat_def_ranged += eff.power` |
| `e0886c07f…` | 2 | `%d` | ranged_accuracy_modifier | `eff.power` | `combat_atk_ranged -= eff.power` |
| `e128c83148…` | 1 | `%0.1f` | turn_gain_percent_per_100_actual_heal | `getTurn()*100` | `(actual_heal/100) * (getTurn()*energy_to_act)` 加入能量，随后封顶为 2 回合能量 |
| `e128c83148…` | 2 | `%0.1f` | equilibrium_reduction_per_turn | `getEq()` | `REGENERATION.on_timeout` 每回合执行 `incEquilibrium(-value)` |
| `e1343327ea…` | 1 | `%d` | stamina_cost_per_turn | `eff.drain` | `GRAPPLING.on_timeout` 对状态持有者执行 `incStamina(-eff.drain)` |
| `e1343327ea…` | 2 | `%d` | redirected_damage_percent | `eff.sharePct*100` | `callbackOnHit` 计算 `share=incoming*sharePct`，以物理伤害投射给 `eff.trgt`，持有者保留 `incoming-share` |
| `e1343327ea…` | 3 | `%s` | actor_name | `eff.trgt.name` | 显示承受转移伤害的抓取目标名称 |
| `e172753e04…` | 1 | `%d` | mental_save_scale_percent | `getSavePercentage()*100` | `saving_throw=mental_save*scale`；仅 `checkHit` 成功分支调用 `mindCrit(2)` 并降低伤害 |
| `e172753e04…` | 2 | `%d` | current_threshold_percent | `min(solipsism_threshold, clarity_threshold)*100` | 只用于显示当前唯我临界点 |
| `e1884052fc…` | 1 | `%d` | range_tiles | `getTalentRange()` | `type="hit"` 的目标范围；消费者接受任意 `Map.ACTOR`，不限定敌对怪物 |
| `e1884052fc…` | 2 | `%d` | confusion_power_percent | `getConfuseEfficency()` | `DamageType.CONFUSION` 参数 `dam` |
| `e1884052fc…` | 3 | `%d` | duration_turns | `getConfuseDuration()` | `DamageType.CONFUSION` 参数 `dur` |
| `e200845e1a…` | 1 | `%d` | cone_radius_tiles | `getTalentRadius()` | `target={type="cone", ... radius=value}` 的前方锥形投射范围 |
| `e200845e1a…` | 2 | `%d` | defense_reduction | `7*getTalentLevel()` | `EFF_BATTLE_CRY` 的 `combat_def -= power`，持续固定 7 回合 |

## 方向值流与新增限定

- 念动弓：持续时间增加会增加逐回合自动攻击的可用回合数；实际目标由敌对且有视线的候选集通过 `rng.table` 随机选取，未恢复错误的“最近目标”。无武器分支仍说明意志替代力量、灵巧替代敏捷，同时决定命中和伤害。
- 召唤阴影：技能激活时每 10 个基础行动回调尝试补召一个阴影，数量只向上补到上限；每只成功召唤消耗 5 仇恨。主人伤害减免百分比越高，阴影实际承受的主人伤害越低。
- 纯净以太：第 3 个值是清除上限；可清除数量不会保证恰好达到该值。
- 血绽：每个流血效果的剩余伤害越高，按 20% 转换得到的治疗越高，但每个效果至少贡献最低治疗；所有效果累加后治疗施法者。睡眠时长随最长流血剩余时长及额外时长增加；后续伤害会缩短睡眠。
- 尖啸漩涡：`slow_projectiles=30` 作用于飞向状态目标的抛射物；未泛化为目标自己发射的全部抛射物。
- 原始生命：先以 `max_life-life` 截断到实际治疗量，再换算回合能量，因此溢出治疗不会增加能量；能量总值向上增加但不超过 2 个回合。回复效果每回合让失衡值向下减少。
- 擒抱：体力值每回合从状态持有者向下扣减，不读取或消耗生命；传入伤害按比例拆分，抓取目标受到正向物理伤害，持有者受到的剩余伤害向下减少。
- 唯我豁免：伤害进入时先进行豁免检定；失败保持原伤害，成功才按精神暴击结果降低伤害，且降低至少 50%。
- 时空交换：与范围内另一个生物交换位置；目标混乱时长随第 3 个值增加。没有加入敌对怪物限定。
- 战吼：只在前方锥形范围投射；固定 7 回合内闪避向下减少，同时禁用躲闪和隐匿带来的未命中优势。没有降低 Willpower。
- 叙事条目：壁画保留水晶城后方的小型石质岛、前景夏·图尔及伸向天空的手；书信恢复德斯周边、狼的三项特征、等长獠牙与“传奇流传”，删除原译杜撰。

## 固定源码锚点

本目录 `SOURCE-ANCHORS.json` 是任务冻结文件的逐字节副本。补查同一固定 commit 得到以下消费者锚点：

- `game/modules/tome/data/talents/psionic/psi-archery.lua:214-254`：无弓分支绑定 `duration`；有弓分支在 `use_psi_combat` 下分别计算 Accuracy 与 Damage，确认两种替代属性同时影响命中和伤害。
- `game/modules/tome/data/talents/cursed/shadows.lua:190-335`：阴影技能等级、主人伤害剩余倍率及 `onTakeHit` 消费链。
- `game/modules/tome/data/talents/gifts/fungus.lua:66-106`：实际治疗截断、能量换算和 2 回合封顶。
- `game/modules/tome/data/timed_effects/physical.lua:192-205`：回复效果每回合调用 `getEq()` 并降低失衡值。

## 尚未执行的后续阶段

本记录只覆盖 EXECUTOR 实施和本次指定的定向验证。独立四成员 review、FINAL 全量复审、完整 17 门禁、严格 addon 构建、`DONE_VERIFIED`、提交、catalog/migration、queue rebuild 与 push 均未由本 EXECUTOR 执行，也不在此记录中声称通过。
