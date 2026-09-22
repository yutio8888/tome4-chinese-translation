# 修复窗口 4 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次只修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 17 个 target；source、section、source_tag、args_order、special、printf placeholder、markup 和所有 target 的 TAB 序列保持不变。`e22d6fff0c…` 与 `e454e243b1…` 各由 baseline 的 5 个 LF 恢复为原文的 7 个 LF及对应段落位置，其余 target 的 LF 序列保持 baseline。

其中 16 条来自三个已成功的真实 production repair preflight，`e433115e63…` 是独立宿主补充；没有把它伪装成原批 `repair_required`，也没有把三个来源批次伪造成一个生产批次。本目录三个 `PREFLIGHT-BATCH*.json` 是任务冻结输入的逐字节副本，`HOST-WORKSET.json` 和 `SOURCE-ANCHORS.json` 也保留冻结宿主输入。

## 实际修复

- 恢复自定义贴图捐赠条件和原文段落；恢复宁静草地的段落和句间换行。
- 恢复腐化者“自身的腐化之血”、峰顶接近关系、地下建筑内部空间关系、已知毒素集合语义及 Telos 组装者/产物关系。
- 明确爆裂火球的目标处爆炸和伤害半径；去掉噩梦正文中不存在的“清醒状态”；恢复治疗逆转的敌方限定；修复潜行行动范围、状态用词和句界。
- 恢复完好白皮腰带、符文沃瑞钽带扣、“大罪”字幕、兽人种族层面的叙事及 Stone Warden 解锁诗句的可能情态。
- `thalore wilder` 译为“自然精灵自然师”，补回自然精灵亚种但不套用职业类别 `Wilder=野性系`；未改术语库或建立 NPC 全局命名策略。
- `e433115e63…` 仅修四项冻结内容：裸体/由自身念头激起欲望、来自群星并从天空坠落的水晶塔比喻、条件性的“不得不恨”、向东出发后气氛随即变化。其余长文、advisory 和“大小姐”称谓未改。

## 数值 placeholder 值流

`index` 按 source 中需要实参数值替换的 placeholder 出现顺序计数；字面量 `%%` 不占实参 index。

| revision | index | token | quantity_kind | producer | consumer |
| --- | ---: | --- | --- | --- | --- |
| `e359df96b1…` | 1 | `%0.2f` | fire_damage_amount | `t.getDamage(self,t)`，由 `combatTalentSpellDamage(t,28,330)` 生成 | `self:projectile(..., DamageType.FIRE, spellCrit(value), ...)` 在目标处按 ball 投射火焰伤害 |
| `e359df96b1…` | 2 | `%d` | explosion_radius_tiles | `self:getTalentRadius(t)`，底层为 `floor(combatTalentScale(t,2,5.5))` | `target.type="ball"` 的 `radius`，并传给目标处的伤害投射和粒子半径 |
| `e3b3e027a2…` | 1 | `%0.2f` | darkness_damage_per_turn | `eff.dam` | `on_timeout` 每回合调用 `DamageType.DARKNESS.projector(..., eff.dam)` 使状态目标受到暗影伤害 |
| `e3b3e027a2…` | 2 | `%d` | detrimental_effect_chance_percent | 基础 `eff.chance`；目标睡眠时变为 `100-(100-chance)/2` | `rng.percent(chance)` 成功后随机尝试施加致盲、震慑或混乱之一 |
| `e4c8e60909…` | 1 | `%d` | effect_radius_tiles | `self:getTalentRadius(t)`，固定 talent radius 为 4 | 选点后 `type="ball"` 的投射半径；`friendlyfire=false` 使投射跳过施法者及非敌对对象 |
| `e4c8e60909…` | 2 | `%d` | healing_to_blight_percent | `t.getPower(self,t)`，由法术强度缩放并限制在 100 以下 | 作为 `EFF_HEALING_INVERSION.power`；正的 raw healing 乘 `power/100` 后对目标投射枯萎伤害，同时本次治疗返回 0 |
| `e542306f47…` | 1 | `%0.2f` | stealth_power_multiplier | `t.stealthMult(self,t)` | 乘以潜行强度形成 `netstealth`，再与可见敌人的潜行侦测比较 |
| `e542306f47…` | 2 | `%d` | current_scaled_stealth_power | `t.getChance(self,t,true)` 直接返回 `netstealth` | 仅显示当前参与比较的缩放后潜行强度 |
| `e542306f47…` | 3 | `%0.1f` | estimated_maintain_stealth_chance_percent | `t.getChance(self,t,false,true)`，由 `checkHit(netstealth,detection)` 的估算值生成 | 仅显示当前维持潜行的估算成功率 |

`e407b46fe5…` 另有两个非数值 `%s`：index 1 由 `self:getName():capitalize()` 产生并显示组装者，index 2 由 `o:getName{...}` 产生并显示组装出的物品；参数顺序未变。

## 方向值流与限定

- 爆裂火球：第 1 个值增大时目标处 ball 内的火焰伤害向上增加；第 2 个值增大时爆炸覆盖半径向外增加。固定施法射程 7 与第 2 个半径值彼此独立，译文没有把半径写成射程。
- 清醒噩梦：`eff.dam` 向状态目标施加每回合正向暗影伤害；`eff.chance` 越高，随机负面效果触发概率越高，睡眠会进一步提高该概率。正文没有施加“目标必须清醒”的限定。
- 治疗逆转：ball 投射使用 `friendlyfire=false`，敌我方向为只把效果施加给敌对对象。效果固定持续 5 回合；持续期间正的 raw healing 被向下压为 0，并按第 2 个百分比转成对该目标的正向枯萎伤害；自然生命回复不在此治疗回调转换链中。百分比越高，等量治疗产生的伤害越高。
- 行动如风：第 1 个倍率越高，参与检定的 `netstealth` 越高；敌人距角色每远一格，其侦测值向下减少 10%，可见敌人越少越有利。第 2、3 个值是当前检定量和估算成功率的显示值，不反向修改状态。
- 其余获准条目不含数值 placeholder；叙事中的数量、方向或时态只按冻结原文恢复，不推导额外机制。

## 固定源码锚点

本目录 `SOURCE-ANCHORS.json` 是冻结源码锚点的逐字节副本，覆盖 17 个 revision 对应的 16 个 section，并固定到上述 commit。补查同一 commit 的 `game/modules/tome/data/timed_effects/magical.lua:3396-3424` 确认治疗逆转消费者：`callbackOnHeal` 读取正的 `raw_value`，以 `raw_value * eff.power / 100` 投射枯萎伤害并返回 `{value=0}`。

## 尚未执行的后续阶段

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向验证。独立四成员 review、whole-workset FINAL_REVIEW、完整 17 门禁、严格 addon 构建、`DONE_VERIFIED`、提交、catalog/migration、queue rebuild 与 push 均未由本 EXECUTOR 执行，也不在本记录中声称通过。
