本批次译文复核报告如下。

### 批次核验信息
- **批次编号**：batch-068
- **条目范围**：`entry-02108` 至 `entry-02147`（共 40 条）
- **文件哈希**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-068.md` SHA-256 校验值为 `887f891134eb8228fa1f6d38a2d6528a3e286a37f002cad895f9753151c13a15`，与冻结哈希一致。
- **源码对照版本**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（公开源码 `mod-tome`）。本批全部条目均属于核心游戏 `mod-tome` 灵能系技能（`psionic`），不涉及 DLC。
- **译文对照终点**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核详情

#### entry-02108
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/kinetic-mastery.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/kinetic-mastery.lua) 中的 `Kinetic Surge`。占位符 `%d`、`%0.1f`、`%d`、`%0.1f`、`%d%%`、`%0.1f`、`%d` 共 7 处，类型与顺序同源码 `tformat(range, dam, math.floor(range/2), dam/2, t.getKBResistPen(self, t), dam, math.floor(range/2))` 完全吻合；震慑（stunned）、击退抗性（knockback resistance）、精神强度（Mindpower）等术语与机制逻辑准确一致。

#### entry-02109
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mental-discipline.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mental-discipline.lua) 中的 `Aura Discipline`。
  1. 原文 "Your expertise in the art of energy projection grows." 译为“你增加了在灵能值运用方面的知识。”在灵能技能体系中，`energy projection` 对应技能树 `psionic/projection`（能量投射），译为“灵能值运用”略微偏离字面。
  2. 译文“光环消耗灵能值变的更慢”中，“变”字属于字词瑕疵（通常作“变得更慢”）。
  3. 占位符 `%d` 与 `%0.2f` 数量及格式与源码 `tformat(cooldown, mast)` 保持一致。

#### entry-02110
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mental-discipline.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mental-discipline.lua) 中的 `Shield Discipline`。
  1. 原文 "...the maximum energy you can gain from each shield is increased by %0.1f per turn." 译为“每个护盾的最大能量吸收量增加 %0.1f 每回合。”源码机制中 `absorbLimit`（代码注释为 "Limit of bonus psi on shield hit per turn"）指的是每回合从护盾受击反哺所获得的灵能值上限（energy = psi），译为“最大能量吸收量”容易被误解为护盾本身的伤害吸收量上限。
  2. 同一句内对 `energy` 的处理前后不一：前半句译为“灵能值”（“护盾额外增加灵能值所需伤害值”），后半句译为“能量”（“最大能量吸收量”）。
  3. 占位符 `%d`、`%0.1f`、`%0.1f` 数量及顺序与源码 `tformat(cooldown, mast, t.absorbLimit(self, t))` 一致。

#### entry-02111
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mental-discipline.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mental-discipline.lua) 中的 `Highly Trained Mind`。占位符 `%d` 对应 `2*self:getTalentLevelRaw(t)`；属性名 Willpower（意志）、Cunning（灵巧）翻译规范准确。

#### entry-02112
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mentalism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mentalism.lua) 中的 `Psychometry`。占位符 `%0.1f`、`%d%%`、`%d` 与源码 `tformat(max, 100*t.getMaterialMult(self,t), t.getPsychometryCount(self,t))` 匹配；在 [`game/modules/tome/class/interface/Combat.lua`](file:///workspace/t-engine4/game/modules/tome/class/interface/Combat.lua) 中 `psychometry_power` 同时增益物理强度与精神强度，译文“物理和精神强度”与源码机制相符。

#### entry-02113
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mentalism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mentalism.lua) 中的 `Mental Shielding`。
  1. 原文为 "Clears your mind of current mental effects, and blocks additional ones over 6 turns. At most, %d mental effects will be affected."，译文为“净化你当前所有的精神状态，并在接下来的 6 回合内免疫新增的精神状态。最多一共（净化和免疫）能影响 %d 种精神状态。”代码逻辑是总配额由 `getRemoveCount` 限制，若当前负面状态多于 `%d` 则无法“净化所有”，但译文后半句明确说明“最多一共（净化和免疫）能影响 %d 种”，准确解释了配额共享机制。
  2. 占位符 `%d` 正确对应。

#### entry-02114
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mentalism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mentalism.lua) 中的 `Projection`。无占位符，属于空间不足无法生成投影时的 `logPlayer` 提示，译文表达准确。

#### entry-02115
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mentalism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mentalism.lua) 中的 `Projection`。
  1. 术语表中 `ghost`（生物子类型）标准译名为“幽灵”，译文此处作“‘鬼魂’类怪物”。
  2. 原文括号说明 `(mind damage only in the second case.)` 在译文中被拆分为独立行“注：后一种情况下只能造成精神伤害。”，语义清晰无误。
  3. 3 处占位符 `%d` 与源码 `tformat(duration, power, power)` 顺序与格式均一致。

#### entry-02116
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/mentalism.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/mentalism.lua) 中的 `Mind Link`。占位符 `%d%%` 与 `%d` 对应 `tformat(damage, range)`；英文原文末尾存在括号手误 `(%d))`，中文译文规范化为全角括号 `（%d 码）`；心灵感应及精神强度加成描述准确。

#### entry-02117
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/nightmare.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/nightmare.lua) 及 [`game/modules/tome/data/timed_effects/mental.lua`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/mental.lua) 的 `INNER_DEMONS`。占位符 `%d` 与 `%d%%` 对应 `tformat(duration, chance)`；对睡眠目标判定减半、抵抗则提前结束、具现化时清除睡眠效果等机制与代码完全一致。

#### entry-02118
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Telekinetic Grasp` 的物品选择对话框标题。无占位符，译文清晰准确。

#### entry-02119
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 的 `logSeen`。占位符 `%s`、`%s` 分别对应施法者与物品名称，参数顺序与语义一致。

#### entry-02120
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Telekinetic Grasp` 技能说明。无占位符，装备限制例外说明翻译准确。

#### entry-02121
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 的 `logCombat`。战斗标签 `#Source#` 与 `#target#` 保持原样，灵晶术语正确。

#### entry-02122
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 的 `logSeen`。占位符 `%s`、`%s` 顺序对应施法者与被拉取目标，格式正确。

#### entry-02123
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 施法前置检查提示。无占位符，译文准确。

#### entry-02124
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 基础描述。经核验 [`game/modules/tome/class/interface/Combat.lua`](file:///workspace/t-engine4/game/modules/tome/class/interface/Combat.lua) 第 1377、1394、1660-1668 行，`use_psi_combat` 下确实以灵巧替代敏捷计算命中，以意志替代力量计算伤害；译文“分别以 60% 灵巧替代敏捷、以 60% 意志替代力量”准确还原了对应关系；末尾空行与格式一致。

#### entry-02125
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 远程武器面板说明。
  1. 英文原文存在原作者笔误："uses Willpower in place of Strength, and Cunning in place of Dexterity, to determine Accuracy and damage respectively."。实际底层代码（`Combat.lua`）中是灵巧替代敏捷决定命中（Accuracy），意志替代力量决定伤害（Damage）。原文在此处颠倒了 Accuracy 与 damage 的书写顺序（对比近战版本 entry-02126 为 damage and Accuracy）。中文译文忠实直译了该英文原文。
  2. 占位符包括 4 个 `%d` 和 2 个 `%0.1f%%`，数量、顺序与源码 `tformat(range, atk, dam, apr, crit, speed*100)` 完全对应。

#### entry-02126
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/other.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/other.lua) 中 `Beyond the Flesh` 近战武器面板说明。占位符 `%d`、`%d`、`%d`、`%0.2f`、`%0.2f` 与源码 `tformat(atk, dam, apr, crit, speed)` 完全一致；此处的“决定伤害和命中”与意志决定伤害、灵巧决定命中正确对应。

#### entry-02127
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/projection.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/projection.lua) 中的 `Kinetic Aura`。占位符 `%0.1f`、`%0.1f`、`%0.1f`、`%0.1f`、`%d`、`%d`、`%d` 共 7 处，类型与顺序同源码完全吻合；样式标记 `#{bold}#` 与 `#{normal}#` 闭合完整无损。

#### entry-02128
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/projection.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/projection.lua) 中的 `Charged Aura`。
  1. 原文 "To turn off an aura without spiking it..." 译为“如果要关闭光环且不发射射线...”。代码中电能光环关闭爆发（spike）为连锁闪电（chain lightning / 在目标间跳跃），动能光环才为射线（beam）；译文沿用了动能光环的“发射射线”表述，但指代明确，不影响实际玩法操作理解。
  2. 状态术语 "daze" 译为“眩晕”，与 ToME 核心状态术语一致；占位符 4 个 `%0.1f`、2 个 `%d`、1 个 `%0.1f` 及转义 `50%%` 均精准匹配；`#{bold}#` 与 `#{normal}#` 完整。

#### entry-02129
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psi-archery.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psi-archery.lua) 中的 `Augmented Shot`。占位符 `%d` 与 `%d%%` 对应 `tformat(t.apr_boost(self, t), t.dam_mult(self, t) * 100)`；护甲穿透与武器伤害百分比表述清晰准确。

#### entry-02130
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psi-fighting.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psi-fighting.lua) 中的 `Impale`。颜色标记 `#CRIMSON#` 完整，占位符 `%s`、`%s` 顺序对应施法者与目标，译文“粉碎了%s的护盾！”准确贴合。

#### entry-02131
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/absorption` 技能系说明。无占位符，译文简练准确。

#### entry-02132
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/projection` 技能系说明。无占位符，译文准确。

#### entry-02133
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/psi-fighting` 技能系说明。无占位符，译文准确。

#### entry-02134
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/voracity` 技能系说明。无占位符，译文准确。

#### entry-02135
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/other` 技能系说明。无占位符，译文准确。

#### entry-02136
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/distortion` 技能系说明。无占位符，译文准确。

#### entry-02137
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/dream-smith` 技能系说明。无占位符，译文准确。

#### entry-02138
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/nightmare` 技能系说明。无占位符，译文准确。

#### entry-02139
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/psychic-assault` 技能系说明。无占位符，译文准确。

#### entry-02140
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/slumber` 技能系说明。无占位符，译文准确。

#### entry-02141
- **结论**：细微观察
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/solipsism` 技能系说明。
  1. 原文 "Nothing exists outside the minds ability to perceive it." 为唯我论哲学名言（字面意为“在心灵的感知能力之外，万物皆不存在”）。译文作“没有任何事物能逃脱精神力量的感知”，有一定意译色彩，但作为技能系概述流畅，无机制偏差。

#### entry-02142
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/thought-forms` 技能系说明。无占位符，译文准确。

#### entry-02143
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/dreaming` 技能系说明。无占位符，译文准确。

#### entry-02144
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psionic.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psionic.lua) 中的 `psionic/mentalism` 技能系说明。无占位符，译文准确。

#### entry-02145
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/psychic-assault.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/psychic-assault.lua) 中的 `Psychic Lobotomy`。占位符 `%0.2f`、`%d`、`%d%%`、`%d` 与源码 `tformat(damDesc(self, DamageType.MIND, (damage)), cunning_damage, power, duration)` 顺序与格式完全吻合；灵巧惩罚与混乱强度术语准确。

#### entry-02146
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/slumber.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/slumber.lua) 中的 `Dreamscape` 前置检查（投影状态下禁止入梦）。无占位符，`logPlayer` 提示翻译通顺贴合。

#### entry-02147
- **结论**：未发现问题
- **依据**：源码见 [`game/modules/tome/data/talents/psionic/slumber.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/psionic/slumber.lua) 中的 `Dreamscape` 释放失败提示。无占位符，中文省略号对应规范，译文准确。