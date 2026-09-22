### batch-073 译文复核报告

#### 预检与文件哈希核对
- **复核文件**：[`evidence/translation-audit/all-modified-review-20260922/batches/batch-073.md`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/batches/batch-073.md)
- **预检 SHA-256**：`201bd420e8cdca8c7f9842d6ca444a7af4db2ea7059d9895d19685b11f2a9fe0`
- **核对结果**：经计算完全一致。
- **条目范围**：`entry-02308` 至 `entry-02348`（剔除未编入的 entry-02309），共计 40 条。
- **源码与译文基准**：
  - 公开引擎固定 Commit：[`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4)
  - 译文终点 Commit：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（[`mod-tome.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua)）

---

### 逐条复核记录

#### entry-02308
- **位置**：`mod-tome.lua:30050`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码第 44 行 `message = _t"@Source@ shoots!"`，实体标签 `@Source@` 完整保留，英文标点感叹号转换为全角 `！`，与射击技能动作信息一致。

#### entry-02310
- **位置**：`mod-tome.lua:30064`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Fragmentation Shot` 的 `info` 返回 `tformat(rad, dam, dur, speed, chance)`，译文中 5 个占位符 `%d`、`%d%%`、`%d`、`%d%%`、`%d%%` 顺序与类型完全对应。源码第 299 行致残判定传入 `apply_power=self:combatAttack()`（命中），而标记几率使用独立随机，因此将“status chance”译为“致残几率”符合具体机制。

#### entry-02311
- **位置**：`mod-tome.lua:30070`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Scatter Shot` 震慑豁免日志 `game.logSeen(target, "%s resists the scattershot!", target:getName():capitalize())`，占位符 `%s` 正常保留，技能名“分散射击”与段内一致，标点正常。

#### entry-02312
- **位置**：`mod-tome.lua:30077`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：细微观察
- **可核验依据**：占位符 `%d%%` 位置正确。但原文“This shot will bypass other enemies between you and your target.”（该射击会穿过/绕过你与目标之间的其他敌人）译为“且能穿透目标以外单位”，不仅缺少了“你与目标之间”的空间语境，且“穿透……单位”在中文游戏习惯中容易被误读为对沿途敌人造成穿透伤害（源码第 471 行实际仅对 target 单一目标结算，不会对沿途单位造成判定或伤害）。

#### entry-02313
- **位置**：`mod-tome.lua:30082`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Volley` 的 `info` 返回 `tformat(dam, rad, dam*0.75)`，译文中 `%d%%`（主伤害）、`%d`（杀伤半径）、`%d%%`（追加齐射伤害）三处占位符位置与参数顺序完全一致，机制描述准确。

#### entry-02314
- **位置**：`mod-tome.lua:30087`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Called Shots` 日志 `game.logSeen(target, "%s resists the disarm!", ...)`，占位符 `%s` 与缴械术语对应无误。

#### entry-02315
- **位置**：`mod-tome.lua:30088`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Called Shots` 日志 `game.logSeen(target, "%s resists the slow!", ...)`，占位符 `%s` 与减速术语对应无误。

#### entry-02316
- **位置**：`mod-tome.lua:30089`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Called Shots` 的 `info` 返回 `tformat(dam, dur, dam*0.25)`，译文中 `%d%%`、`%d`、`%d%%` 顺序完全一致，常量 `50%%` 保持双写转义，“for the duration”译为“在相同的持续时间内”，机制与占位符无误。

#### entry-02317
- **位置**：`mod-tome.lua:30095`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Bullseye` 返回 `tformat(speed, nb, cd)`，译文依次为 `%d%%` 攻速加成、`%d` 个技能、`%d` 回合冷却，占位符顺序完全对应；源码判定 `tt.type[1]:find("^technique/")`，译为“战斗技巧系技能”与分类设定一致。

#### entry-02318
- **位置**：`mod-tome.lua:30106`（`mod-tome/data/talents/techniques/archery.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Pinning Shot` 的 `info` 返回 `tformat(self:combatTalentWeaponDamage(...) * 100, t.getDur(...))`，译文 `%d%%` 与 `%d` 回合严格对应，原文“Dexterity”对应译为“敏捷”。

#### entry-02319
- **位置**：`mod-tome.lua:30115`（`mod-tome/data/talents/techniques/assassination.lua`）
- **核验结论**：细微观察
- **可核验依据**：原文为 `You cannot use Coup de Grace without dual wielding!`，译文为 `你需要双持武器来施展这个技能！`。译文传达了双持前置限制，但将原技能专名“Coup de Grace”（致命一击）泛化意译为“这个技能”。

#### entry-02320
- **位置**：`mod-tome.lua:30116`（`mod-tome/data/talents/techniques/assassination.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 combat log `self:logCombat(target, "#Source# delivers a Coup de Grace against #Target#!")`，两处实体标签 `#Source#`、`#Target#` 保持完好，专名“致命一击”准确，感叹号全角化。

#### entry-02321
- **位置**：`mod-tome.lua:30119`（`mod-tome/data/talents/techniques/assassination.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Coup de Grace` 的 `info` 返回 `tformat(dam, perc)`（源码字面仅含一个 `%d%%` 占位符，其余 50%、30%、20% 为硬编码文本），译文准确保留一个 `%d%%` 占位符，硬编码数值与物理豁免对抗命中、秒杀判定及潜行联动机制叙述完全一致。

#### entry-02322
- **位置**：`mod-tome.lua:30129`（`mod-tome/data/talents/techniques/assassination.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 combat log `self:logCombat(target, "#Target# avoids a garrote from #Source#!")`，实体标签 `#Target#` 与 `#Source#` 完整无误，绞杀动作译为“勒住喉咙”，感叹号正常全角化。

#### entry-02323
- **位置**：`mod-tome.lua:30160`（`mod-tome/data/talents/techniques/battle-tactics.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Bleeding Edge` 的 `info` 返回 `tformat(100 * dam1, 100 * dam2, heal)`，译文 3 个 `%d%%` 占位符按顺序出现，回合数 7 完整保留，流血与治疗降低减益准确。

#### entry-02324
- **位置**：`mod-tome.lua:30165`（`mod-tome/data/talents/techniques/battle-tactics.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `True Grit` 的 `info` 返回 `tformat(resistC, resistC*0.7, t.getCapApproach(...)*100, drain)`，译文依次对应 `%d%%`、`%d%%`、`%0.1f%%`、`%0.1f`，占位符格式与顺序完全匹配，硬编码示例 70%、100% 及体力递增 0.3 无误。

#### entry-02325
- **位置**：`mod-tome.lua:30189`（`mod-tome/data/talents/techniques/bloodthirst.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Bloodbath` 的 `info` 返回 `tformat(getHealth, regen, regen/5, getDuration, max_regen, max_regen/5)`，译文按顺序对应 `%d%%`、`%0.2f`、`%0.2f`、`%d`、`%0.2f`、`%0.2f`，全部 6 个占位符类型与顺序无偏差，叠加 5 次说明准确。

#### entry-02326
- **位置**：`mod-tome.lua:30194`（`mod-tome/data/talents/techniques/bloodthirst.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Bloody Butcher` 返回 `tformat(t.getDam(...), t.getResist(...))`，占位符 `%d` 与 `%d%%` 顺序正确，硬编码 `0%%` 转义正确；观察点为第二行句末英文原本为 `(but never below 0%%).`，译文 `（但不会小于 0%%）` 括号后遗漏句号直接换行。

#### entry-02327
- **位置**：`mod-tome.lua:30200`（`mod-tome/data/talents/techniques/bloodthirst.lua`）
- **核验结论**：存在疑点
- **可核验依据**：
  - 原文第三段为：`While Unstoppable is active, Berserker Rage critical bonus is disabled as you lose the thrill of the risk of death.`
  - 译文为：`当进入无双状态时，由于你失去了死亡的威胁，狂战之怒不能提供暴击加成。`
  - 疑点证据：该技能自身在同一段落前文（`mod-tome.lua:30199`）及全局实体中定译名称均为 `势不可挡`（`t("Unstoppable", "势不可挡", "talent name")`），而在本技能说明的最后一句中却将“While Unstoppable is active”译为了“当进入无双状态时”，残留了历史旧译“无双”，造成技能名与效果描述内部术语不统一。

#### entry-02328
- **位置**：`mod-tome.lua:30241`（`mod-tome/data/talents/techniques/buckler-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Buckler Mastery` 在检测到 `Bash and Smash` 等级 ≥ 5 时拼接此复数文本。对应技能在 `mod-tome.lua:30235` 定译为 `击退射击`，译文使用“你的击退射击的盾击必定暴击”完全对齐技能名。英文前置空格用于英文句号后衔接，中文前文有句号 `。`，省略空格符合中文排版习惯。

#### entry-02329
- **位置**：`mod-tome.lua:30242`（`mod-tome/data/talents/techniques/buckler-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码在 `Bash and Smash` 等级 < 5 时的单数文本分支持，中文译文表述与复数条目保持一致且完全适用。

#### entry-02330
- **位置**：`mod-tome.lua:30245`（`mod-tome/data/talents/techniques/buckler-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Counter Shot` 的 combat log：`#ORCHID##Source# follows up with a countershot.#LAST#`，颜色标签 `#ORCHID#`、`#LAST#` 及实体 `#Source#` 保持完好，标点转为全角句号。

#### entry-02331
- **位置**：`mod-tome.lua:30254`（`mod-tome/data/talents/techniques/combat-techniques.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Rush` 触发信息 `message = _t"@Source@ rushes out!"`，实体标签 `@Source@` 完好，感叹号全角化。

#### entry-02332
- **位置**：`mod-tome.lua:30270`（`mod-tome/data/talents/techniques/combat-techniques.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `info` 返回 `tformat(t.getStamRecover(self, t))`，浮点占位符 `+%0.1f` 格式完好，全角括号匹配，体力回复概念无误。

#### entry-02333
- **位置**：`mod-tome.lua:30272`（`mod-tome/data/talents/techniques/combat-techniques.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Fast Metabolism` 的 `info` 返回 `tformat(t.getRegen(self, t))`，浮点占位符 `+%0.1f` 格式完好，全角括号匹配，生命值回复概念无误。

#### entry-02334
- **位置**：`mod-tome.lua:30274`（`mod-tome/data/talents/techniques/combat-techniques.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Spell Shield` 的 `info` 返回 `tformat(t.getSaves(self,t))`，整数占位符 `+%d` 完好，术语 `spell save` 对应“法术豁免”准确。

#### entry-02335
- **位置**：`mod-tome.lua:30286`（`mod-tome/data/talents/techniques/combat-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Heavy Armour Training` 对格斗家职业描述后缀，`brawlers` 对应“格斗家”，`massive armour` 对应“板甲”，全角括号完整。

#### entry-02336
- **位置**：`mod-tome.lua:30287`（`mod-tome/data/talents/techniques/combat-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码潜行惩罚后缀，`mail or plate armour` 对应“重甲或板甲”，全角括号完整，语义准确。

#### entry-02337
- **位置**：`mod-tome.lua:30288`（`mod-tome/data/talents/techniques/combat-training.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Heavy Armour Training` 返回 `tformat(armor, hardiness, criticalreduction, classrestriction)`，4 个占位符 `%d`、`%d%%`、`%d%%`、`%s` 顺序与格式完全吻合。观察点为：文中括号部分将 `heavy mail armour` 概括译为“重甲”，而等级 1 解锁部分将 `heavy mail armour` 译为“锁甲”，虽属同一大类下的不同表述（不影响实际装备判定），但词面稍有不一致。

#### entry-02338
- **位置**：`mod-tome.lua:30301`（`mod-tome/data/talents/techniques/combat-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Light Armour Training` 返回 `tformat(defense, t.getArmorHardiness(...), t.getFatigue(...), defense/2)`，4 个占位符 `%d`、`%d%%`、`%d%%`、`%d` 顺序完全一致，闪避、护甲强度与疲劳降低比例匹配，机制描述完整。

#### entry-02339
- **位置**：`mod-tome.lua:30313`（`mod-tome/data/talents/techniques/combat-training.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Exotic Weapons Mastery` 返回 `tformat(100*inc)`，占位符 `%d%%` 正确，常量 30 与物理强度（physical power）准确。

#### entry-02340
- **位置**：`mod-tome.lua:30319`（`mod-tome/data/talents/techniques/conditioning.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Vitality` 返回 `tformat(wounds, baseheal, duration, baseheal*duration, self:getTalentCooldown(t))`，5 个占位符 `%d%%`、`%0.1f`、`%d`、`%d`、`%d` 顺序与类型完全一致，硬编码 `50%%` 转义正确，触发冷却与生命回复叙述准确。

#### entry-02341
- **位置**：`mod-tome.lua:30325`（`mod-tome/data/talents/techniques/conditioning.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Unflinching Resolve` 清除减益日志 `game.logSeen(self, "#ORCHID#%s has recovered!#LAST#", ...)`，颜色标签 `#ORCHID#` 与 `#LAST#` 完好，占位符 `%s` 正确，感叹号全角化。

#### entry-02342
- **位置**：`mod-tome.lua:30344`（`mod-tome/data/talents/techniques/conditioning.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Adrenaline Surge` 返回 `tformat(attack_power, duration)`，占位符 `%d`（物理强度）与 `%d`（回合数）顺序与类型正确，无体力消耗施法及免回合机制叙述准确。

#### entry-02343
- **位置**：`mod-tome.lua:30369`（`mod-tome/data/talents/techniques/dualweapon.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Close Combat Management` 激活失败提示为 `You must dual wield to manage contact with your target!`，译文为 `你只有在双持状态下才能使用这个技能！`。与前一行 `on_pre_use` 的提示译文完全相同，将“manage contact with your target”的具象表述简化泛化为“使用这个技能”。

#### entry-02344
- **位置**：`mod-tome.lua:30377`（`mod-tome/data/talents/techniques/dualweapon.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Offhand Jab` 释放失败提示为 `You must dual wield to perform an Offhand Jab!`，译文为 `你只有在双持状态下才能使用这个技能！`，技能专名“Offhand Jab”（副手猛击）被泛化省略。

#### entry-02345
- **位置**：`mod-tome.lua:30379`（`mod-tome/data/talents/techniques/dualweapon.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `info` 返回 `tformat(dam, dam*1.25, t.getConfusePower(...), t.getConfuseDuration(...))`，4 个占位符 `%d%%`、`%d%%`、`%d%%`、`%d` 顺序与格式完全吻合。观察点为：首句“in place of your normal offhand attack”在译文中被略过（译文为“你迅速移动，用徒手攻击敌人”），虽后续数值和混乱机制完整准确，但未明确点出此动作为“取代常规副手攻击”。

#### entry-02346
- **位置**：`mod-tome.lua:30386`（`mod-tome/data/talents/techniques/dualweapon.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Dual Strike` 判定提示为 `You cannot use Dual Strike without dual wielding!`，译文为 `你只有在双持状态下才能使用这个技能！`，技能专名“Dual Strike”（双持打击）被泛化省略。

#### entry-02347
- **位置**：`mod-tome.lua:30393`（`mod-tome/data/talents/techniques/dualweapon.lua`）
- **核验结论**：细微观察
- **可核验依据**：源码 `Flurry` 判定提示为 `You cannot use Flurry without dual wielding!`，译文为 `你只有在双持状态下才能使用这个技能！`，技能专名“Flurry”（疾风连刺）被泛化省略。

#### entry-02348
- **位置**：`mod-tome.lua:30407`（`mod-tome/data/talents/techniques/duelist.lua`）
- **核验结论**：未发现问题
- **可核验依据**：源码 `Dual Weapon Mastery` 返回 `tformat(100 - mult, t.getDeflects(...), chance, block)`，4 个占位符 `%d%%`、`%0.1f`、`%d%%`、`%d` 顺序与类型严格对应，属性“灵巧”（Cunning）与装备“灵晶”（mindstar）术语准确，招架与减免规则表述清晰。

---

### 复核总结与疑点汇总

在本次复核的全部 40 条译文中，共核实发现 **1 条存在疑点** 与 **7 项细微观察**：

1. **存在疑点（术语不一致）**：
   - **entry-02327**（`bloodthirst.lua: Unstoppable`）：技能名称定译为“势不可挡”，但描述末句将“While Unstoppable is active”译为了“当进入**无双**状态时”，使用了旧译俗名，与本技能及全局标准译名脱节。

2. **细微观察（语意精度与专名处理）**：
   - **entry-02312**（`archery.lua: Headshot`）：“bypass other enemies between you and your target”被译为“且能穿透目标以外单位”，缺少中间阻挡方位语境，易引起是否造成穿透伤害的歧义。
   - **entry-02319, entry-02344, entry-02346, entry-02347**（`assassination.lua` / `dualweapon.lua` 前置双持失败提示）：原文均包含具体技能专名（Coup de Grace、Offhand Jab、Dual Strike、Flurry），译文均统一泛化为“这个技能”。
   - **entry-02343**（`dualweapon.lua: Close Combat Management`）：将具体动作提示“to manage contact with your target”泛化为“使用这个技能”。
   - **entry-02345**（`dualweapon.lua: Offhand Jab`）：首句意译略有简缩，省略了“取代常规副手攻击”的细节说明。
   - **entry-02326**（`bloodthirst.lua: Bloody Butcher`）：第二行末尾全角括号后遗漏句号直接换行。
   - **entry-02337**（`combat-training.lua: Heavy Armour Training`）：同段中对 `heavy mail armour` 分别出现“重甲”与“锁甲”两种译法。