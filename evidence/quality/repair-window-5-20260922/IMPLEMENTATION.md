# 修复窗口 5 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次只修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 18 个 target；source、section、source_tag、args_order、special、printf placeholder 和 markup 均未改变。除 `e56b636891…` 外，所有 target 的 LF/TAB 序列保持 baseline；该条按 source 恢复为 1 个 LF、2 个 TAB，合并原译首段的额外分段，并把伤害加成句放在唯一换行之后。

其中 16 条来自两个真实 production repair preflight，`e68cd1e92d…` 与 `e6976768f9…` 是独立宿主补充；`HOST-WORKSET.json` 明确保留 `not_a_single_production_batch=true`，未把它们伪装成单一生产批次。本目录两个 `PREFLIGHT-BATCH*.json`、`HOST-WORKSET.json` 和 `SOURCE-ANCHORS.json` 均为任务冻结输入的逐字节副本。

## 实际修复

- `323606655f…` 只补回水晶大厅所有表面发光，并把缓慢旋转的星云恢复到高台之上；未接纳该回忆录的其他 pending/advisory。
- `e5dc6a60be…` 只修死亡人数、`none of this` 对前述灾变的回指、对医生下达最严格指令，以及固定源码 368—396 行对应直接引语的句末标点；未全面重译第六章。
- 地下建筑喊话去掉引号外重复句号；森林尸妖恢复整体人形；自然精灵的 `lands` 恢复为多处领地；炼金术士对白恢复搭话语气与“肢解”；伐木工日志恢复语无伦次、难以言说的恐怖和潜伏关系。
- 啃噬只为“感染后后续死亡”补回感染限定；源码中命中即死且可染病时直接 `spawn_ghoul` 的分支仍成立，译文没有否定该分支。黑暗触手补回“最多 12 回合”，并恢复冻结布局。生命之泉恢复只有 living 分类受益，覆盖 undead、construct 和 crystal 等全部 unliving 分类。
- 元素法师说明恢复“初始掌握”；移动防御去掉错误的近身限定；沃瑞钽盾恢复“抵挡”与烈火战争高峰期；击退日志恢复撞上另一目标的关系；诅咒之体恢复对所受伤害的反馈；战术显示恢复战术边框限定。
- 精神暴击日志不再限定攻击，兼容 `mindCrit` 用于治疗；精神暴击触发的失衡值属性改为中性的“变化”，兼容正负属性值。未修改 Archmage 类名、人物音译、术语库、专名或全局策略。

## 数值 placeholder 值流

`index` 按 source 中需要实参数值替换的 placeholder 出现顺序计数；字面量 `%%` 不占实参 index。

| revision | index | token | quantity_kind | producer | consumer |
| --- | ---: | --- | --- | --- | --- |
| `e56b636891…` | 1 | `%d` | pin_duration_turns | `t.getPinDuration(self,t)`，即 `floor(combatTalentScale(t,2.5,4.5))` | 命中时传给 `EFF_PINNED`，并作为触手命中后的 final countdown 及黑暗最短保留期 |
| `e56b636891…` | 2 | `%0.2f` | darkness_damage_per_turn | `t.getDamage(self,t)`，由 `combatTalentMindDamage(t,0,80)` 生成；施放时经 `mindCrit` 得到实际值 | `createDark` 保存为 `dark.damage`，黑暗格每次 act 对其中非施法者且非其直接召唤物投射 `DamageType.DARKNESS` |
| `e56b636891…` | 3 | `%d%%` | creeping_dark_damage_bonus_percent | `getDamageIncrease(self)` 汇总四个 darkness 天赋原始等级后经 `combatScale(total,5,1,40,20)` 生成 | `createDark` 保存为 `dark.damageIncrease`；`damage_types.lua` 在来源本人攻击已进入其 creeping dark 的目标时加入伤害百分比，黑暗自身 tick 以 `dark.projecting` 排除该加成 |
| `e5666d20d3…` | 1 | `%d%%` | gnaw_weapon_damage_percent | `100 * t.getDamage(self,t)`，底层为 `combatTalentScale(t,1,1.6)` | `attackTarget(..., t.getDamage(...), true)` 作为啃噬近战伤害倍率 |
| `e5666d20d3…` | 2 | `%d` | ghoul_rot_duration_turns | `t.getDuration(self,t)`，由受限天赋缩放后取整 | 非致死且成功染病时作为 `EFF_GHOUL_ROT` 持续时间 |
| `e5666d20d3…` | 3 | `%0.2f` | blight_damage_per_turn | 显示值为 `damDesc(..., t.getDiseaseDamage(self,t))`；原始值由体质经 `combatTalentStatDamage(t,"con",10,70)` 生成 | 保存为 `EFF_GHOUL_ROT.eff.dam`，每回合投射枯萎伤害；若目标有 `purify_disease` 则同值改为治疗 |
| `e5666d20d3…` | 4 | `%d` | summoned_ghoul_duration_turns | `t.getGhoulDuration(self,t)`，由受限天赋缩放后取整 | `spawn_ghoul` 写入复生食尸鬼的 `summon_time` |
| `e571821f55…` | 1 | `%+0.2f` | life_regeneration_per_turn | living 目标上 `eff.power = 3 + adjusted_level / 2` | `effectTemporaryValue(eff,"life_regen",eff.power)` |
| `e571821f55…` | 2 | `%+0.2f` | equilibrium_regeneration_per_turn | `eff.equilibrium = -eff.psi` | `effectTemporaryValue(eff,"equilibrium_regen",eff.equilibrium)`；负值使失衡值向下变化 |
| `e571821f55…` | 3 | `%+0.2f` | stamina_regeneration_per_turn | `eff.stamina = eff.psi` | `effectTemporaryValue(eff,"stamina_regen",eff.stamina)` |
| `e571821f55…` | 4 | `%+0.2f` | psi_regeneration_per_turn | `eff.psi = (eff.power/5)^0.75` | `effectTemporaryValue(eff,"psi_regen",eff.psi)` |
| `e66d53860d…` | 1 | `%d%%` | defense_multiplier_bonus_percent | `t.getDef(self,t) * 100`，底层为限制在 100% 以下的天赋缩放 | 轻甲条件下加入 `combatDefenseBase` 的乘数；`combatDefense` 与 `combatDefenseRanged` 均消费该 base，因此同时影响近战和远程防御 |
| `e66d53860d…` | 2 | `%d%%` | armour_hardiness_bonus_percent | `t.getHardiness(self,t)`，底层为 `combatTalentLimit(t,100,6,30)` | 轻甲条件下由 `combatArmorHardiness` 加入硬度，决定护甲最多可削减一次打击的比例 |
| `e68cd1e92d…` | 1 | `%d` | knockback_distance_tiles | 击退逐格推进时累积的 `knockbackCount` | 仅格式化碰撞日志；到达受阻格且存在 `nextTarget` 时说明来源被轰飞该距离后撞上目标 |

`e6976768f9…` 另有一个非数值 `%s`，由 `self:getName():capitalize()` 产生并标识触发精神暴击的角色；参数与 markup 均保持不变。

## 方向值流、治疗/伤害/时长与敌我限定

- 黑暗触手：追踪实体以固定 `duration=12` 创建，目标死亡、超出按剩余时长可追赶的距离或无可行路径时会提前消散，因此译为“最多持续12回合”。第 1 个值增大时定身及命中后的触手倒计时向上延长；第 2 个值增大时黑暗格对其中对象的每回合暗影伤害向上增加；第 3 个值增大时施法者对已进入其 creeping dark 的对象造成的其他伤害向上增加。黑暗 tick 排除施法者及其直接召唤物，但不是通用“仅敌人”过滤，译文使用中性的“目标/其中的目标”。
- 啃噬：第 1 个值增大时直接近战伤害向上增加；第 2 个值增大时感染持续更久；第 3 个原始值通常使每回合枯萎伤害向上增加，但 `purify_disease` 会把同值改作治疗；第 4 个值增大时友方复生食尸鬼存在更久。非致死目标必须成功获得带 `make_ghoul=1` 的腐烂疫病，才会在之后死亡时生成友方食尸鬼；命中即死且目标可染病时直接生成，未被译文排除。
- 生命之泉：只对 `checkClassification("living")` 为真的目标设置四项临时值；unliving 包含 undead、construct、crystal，均不受益。生命、体力、灵能回复值为正并使对应资源向上；失衡回复值为负并使失衡值向下。效果没有敌我阵营判断。
- 移动防御：第 1 个值同时提高近战和远程 Defense，第 2 个值提高护甲强度；两项都以穿轻甲或更轻护甲为条件，不含“仅近身”限定。
- 精神暴击：`mindCrit` 在暴击时把传入量乘以暴击倍率并返回；调用者既可把结果用于伤害，也可像 `call.lua` 的 `target:heal(self:mindCrit(...),self)` 一样用于治疗，日志不写成“精神攻击”。`equilibrium_on_crit` 是带符号属性并直接传给 `incEquilibrium`：正值使失衡值向上，负值使其向下，故标签不预设回复方向。
- 诅咒之体描述的触发语义是 `damage taken`，后续增伤/属性改变以受伤反馈为前提；击退碰撞日志在存在 `nextTarget` 时触发，关系是撞上目标而非进入目标体内。

## 固定源码锚点与副本校验

本目录 `SOURCE-ANCHORS.json` 固定了 18 个 revision 的 27 组公开源码摘录。EXECUTOR 另以只读 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 核对了上述 producer、consumer、分类、分支和直接引语。冻结副本 SHA-256 如下：

- `PREFLIGHT-BATCH250.json`: `4acdde5f353a1eabf0ad902017469cbad43f5e8b2422f8b01a4ff7b4b0ce10a5`
- `PREFLIGHT-BATCH251.json`: `9406f3aa9407793d4803a4d298f33dcce15580854f6790fdff60bd162f7748eb`
- `HOST-WORKSET.json`: `eec4c53b10ac3a1695649711c63a7434b39402c8bd96c860c0b7735c3667b37c`
- `SOURCE-ANCHORS.json`: `814dbf3754e16b224ee0bbc5d6319376dc071a6ed98727d4094ce597228f0ae2`

## 尚未执行的后续阶段

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向验证。独立四成员 REVIEW、whole-workset FINAL_REVIEW、完整 17 门禁、严格构建、`DONE_VERIFIED`、提交、catalog/migration、queue rebuild 与 push 均未由本 EXECUTOR 执行，也不在本记录中声称通过。
