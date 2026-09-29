### 复核信息概述

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-007.md`
- **文件哈希**：`b25ab480915f6ffeec298d324307069a2ad3216207d3ff3022e43cca3a340585`（已通过 `sha256sum` 核对一致）
- **公开源码基线**：`/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`mod-tome/` 对应 `game/modules/tome/`）
- **译文基准**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（当前工作树 `mod-tome.lua` 无改动）
- **覆盖范围**：`entry-00241` 至 `entry-00280`，共 40 条，逐条列出核验依据。

---

### 逐条复核报告

#### entry-00241
- **位置**：`mod-tome.lua:608`；section：`mod-tome/class/GameState.lua`
- **原文**：`Proceed to the next Infinite Dungeon level with -7 sight range for a reward.`
- **译文**：`在-7视野下到达无尽地下城的下一层，以获得奖励。`
- **复核结论**：未发现问题
- **核验依据**：源码 `game/modules/tome/class/GameState.lua:3585` 处近视挑战逻辑 `actor:effectTemporaryValue(eff, "sight", -7)`，目标为下一层楼层退出检测；术语 `Infinite Dungeon` 译为“无尽地下城”契合术语库，语义与机制完全吻合。

#### entry-00242
- **位置**：`mod-tome.lua:622`；section：`mod-tome/class/GameState.lua`
- **原文**：`%d / %d demon spawn killed.`
- **译文**：`已杀死 %d/%d 个恶魔子嗣。`
- **复核结论**：未发现问题
- **核验依据**：源码 `GameState.lua:3662` 传入 `self.nb_killed` 与 `self.to_kill`。占位符 `%d/%d` 保留完整且顺序一致，增加了中文自然量词“个”，词义准确。

#### entry-00243
- **位置**：`mod-tome.lua:634`；section：`mod-tome/class/GameState.lua`
- **原文**：`#LIGHT_BLUE#%s has received: %s.`
- **译文**：`#LIGHT_BLUE#%s获得了：%s。`
- **复核结论**：未发现问题
- **核验依据**：源码 `GameState.lua:3774` 中 `game.log("#LIGHT_BLUE#%s has received: %s.", who:getName():capitalize(), reward_name)`。颜色标记 `#LIGHT_BLUE#` 保留完整，两个 `%s` 顺序一致，全角标点符合习惯。

#### entry-00244
- **位置**：`mod-tome.lua:674`；section：`mod-tome/class/MapEffects.lua`
- **原文**：` area effect`
- **译文**：`范围效果`
- **复核结论**：细微观察
- **核验依据**：源码 `game/modules/tome/class/MapEffects.lua:23` 为 `engine.DamageType.dam_def[self.damtype].name.._t" area effect"`。英文中前导空格用于与伤害类型名称拼接（如 `fire area effect`）；译文未保留前导空格，拼接后为“火焰范围效果”，符合中文不使用词间空格的书写规范，运行显示正常。

#### entry-00245
- **位置**：`mod-tome.lua:675`；section：`mod-tome/class/MapEffects.lua`
- **原文**：`area effect`
- **译文**：`范围效果`
- **复核结论**：未发现问题
- **核验依据**：源码 `MapEffects.lua:23` 作为无伤害类型时的后备名称 `_t"area effect"`，译文准确且无格式问题。

#### entry-00246
- **位置**：`mod-tome.lua:718`；section：`mod-tome/class/Object.lua`
- **原文**：`%s, %d apr, %s damage`
- **译文**：`%s, %d 护甲穿透，%s 伤害`
- **复核结论**：未发现问题
- **核验依据**：源码 `game/modules/tome/class/Object.lua:461` 为 `COMBAT_DAMTYPE` 描述，参数分别为 `power(c)`、`apr` 与伤害类型名称；占位符 `%s`、`%d`、`%s` 数量与类型完全对应，术语 `apr -> 护甲穿透` 准确。

#### entry-00247
- **位置**：`mod-tome.lua:719`；section：`mod-tome/class/Object.lua`
- **原文**：`%s, %d apr, %s element`
- **译文**：`%s, %d 护甲穿透，%s 伤害`
- **复核结论**：细微观察
- **核验依据**：源码 `Object.lua:464` 为 `COMBAT_ELEMENT` 属性（被 `data/general/objects/staves.lua:29` 的法杖所使用），传入 `power(c)`、`apr` 及 `DamageType:get(c.element).name`。此处将 `element` 亦译作“伤害”（如显示为“火焰 伤害”），与上一条 entry-00246（`%s damage`）译文完全一致。从法杖显示效果来看意译通顺，但字面上未体现 `element` 与普通武器 `damage` 的词义区分（“元素/属性” vs “伤害”）。

#### entry-00248
- **位置**：`mod-tome.lua:722`；section：`mod-tome/class/Object.lua`
- **原文**：`%s def, %s armour`
- **译文**：`%s 闪避，%s 护甲`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:470` 针对 `ARMOR` 属性格式化，分别传入 `combat_def` 与 `combat_armor`；占位符 `%s`、`%s` 对应准确，术语对齐统一。

#### entry-00249
- **位置**：`mod-tome.lua:723`；section：`mod-tome/class/Object.lua`
- **原文**：`%s accuracy, %s apr, %s power`
- **译文**：`%s 命中，%s 护甲穿透，%s 强度`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:473` 针对 `ATTACK` 属性格式化，分别传入命中、护甲穿透与强度（`combat_dam`）；术语 `power` 在此效果属性语境下采用优选译名“强度”，占位符完备。

#### entry-00250
- **位置**：`mod-tome.lua:733`；section：`mod-tome/class/Object.lua`
- **原文**：` crit mult (max 40%)`
- **译文**：` 暴击伤害（最大40%）`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:673` 剑类命中加成，拼接在 `showpct(0.4, m)` 之后，前导空格保留无误，术语符合 `crit mult -> 暴击伤害` 规范。

#### entry-00251
- **位置**：`mod-tome.lua:734`；section：`mod-tome/class/Object.lua`
- **原文**：` crit chance (max 25%)`
- **译文**：` 暴击率（最大25%）`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:675` 斧类命中加成，前导空格保留，术语 `crit chance -> 暴击率` 规范统一。

#### entry-00252
- **位置**：`mod-tome.lua:735`；section：`mod-tome/class/Object.lua`
- **原文**：` base dam (max 20%)`
- **译文**：` 基础伤害（最大20%）`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:677` 钝器命中加成，前导空格保留，词义表达准确。

#### entry-00253
- **位置**：`mod-tome.lua:736`；section：`mod-tome/class/Object.lua`
- **原文**：` proc dam (max 200%)`
- **译文**：` 触发伤害（最大200%）`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:679` 法杖命中加成（触发法杖特效伤害），前导空格保留，`proc dam -> 触发伤害` 机制表达准确。

#### entry-00254
- **位置**：`mod-tome.lua:737`；section：`mod-tome/class/Object.lua`
- **原文**：` APR (max 50%)`
- **译文**：` 护甲穿透（最大 50%）`
- **复核结论**：细微观察
- **核验依据**：源码 `Object.lua:681` 匕首命中加成，前导空格保留，`APR` 译为“护甲穿透”准确。观察点在于同组 entry-00250~253 括号内均为紧凑无空格（`最大40%`、`最大25%`、`最大20%`、`最大200%`），唯独本条写作 `最大 50%`，存在批内排版微小不一致。

#### entry-00255
- **位置**：`mod-tome.lua:739`；section：`mod-tome/class/Object.lua`
- **原文**：`Power: %3d%% (%s)  Range: %.1fx (%s)`
- **译文**：`威力：%3d%% (%s)  浮动：%.1fx (%s)`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:876` 武器高级对比统计面板，参数依次为基础威力百分比、威力差异列表、伤害波动倍率、波动差异列表；四个占位符及其格式、双空格分隔符完全保留对齐。

#### entry-00256
- **位置**：`mod-tome.lua:740`；section：`mod-tome/class/Object.lua`
- **原文**：`Power: %3d%%  Range: %.1fx`
- **译文**：`威力：%3d%%  浮动：%.1fx`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:879` 无对比时的武器威力与波动显示，占位符 `%3d%%` 与 `%.1fx` 以及双空格保留完好。

#### entry-00257
- **位置**：`mod-tome.lua:751`；section：`mod-tome/class/Object.lua`
- **原文**：`Crit. power: `
- **译文**：`暴击伤害：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:923` 处 `compare_fields` 显示 `crit_power`，其后追加格式化数值；全角冒号自然具备字符间隔，符合术语库中“暴击伤害”的既定规则。

#### entry-00258
- **位置**：`mod-tome.lua:768`；section：`mod-tome/class/Object.lua`
- **原文**：`Damage Shield penetration (this weapon only): `
- **译文**：`伤害护盾穿透（仅该武器）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1127` 对应武器 combat 的 `phasing` 属性，仅对当前武器攻击生效；机制与限定范围译文完全一致。

#### entry-00259
- **位置**：`mod-tome.lua:769`；section：`mod-tome/class/Object.lua`
- **原文**：`Lifesteal (this weapon only): `
- **译文**：`吸血（仅该武器）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1129` 对应武器 combat 的 `lifesteal` 属性，译文简明准确。

#### entry-00260
- **位置**：`mod-tome.lua:771`；section：`mod-tome/class/Object.lua`
- **原文**：`Multiple attacks procs power reduction: `
- **译文**：`多重攻击触发效果衰减：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1137` 与 `game/modules/tome/class/interface/Combat.lua:690, 719`，机制为多重攻击（`attack_recurse`）后续击中时降低触发特效强度（`attack_recurse_procs_reduce`），译文“多重攻击触发效果衰减”准确传达机制。

#### entry-00261
- **位置**：`mod-tome.lua:776`；section：`mod-tome/class/Object.lua`
- **原文**：`Damage (radius 1) on hit: `
- **译文**：`击中时溅射伤害（1格半径）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1161` 对应武器 `burst_on_hit`（半径 1 范围伤害），译文清晰指明击中溅射与半径，准确无误。

#### entry-00262
- **位置**：`mod-tome.lua:777`；section：`mod-tome/class/Object.lua`
- **原文**：`Damage (radius 2) on crit: `
- **译文**：`暴击时溅射伤害（2格半径）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1166` 对应武器 `burst_on_crit`（暴击时半径 2 范围伤害），与 entry-00261 结构一致，准确无误。

#### entry-00263
- **位置**：`mod-tome.lua:818`；section：`mod-tome/class/Object.lua`
- **原文**：`#YELLOW#On shield block:#LAST#`
- **译文**：`#YELLOW#盾牌格挡时：#LAST#`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1502` 盾牌格挡触发效果标题，颜色标签保留，译文准确。

#### entry-00264
- **位置**：`mod-tome.lua:826`；section：`mod-tome/class/Object.lua`
- **原文**：`Changes damage: `
- **译文**：`伤害变化：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1538` 对应装备的 `inc_damage`（全系或单系增伤百分比），与同 section 的“抗性改变”、“属性变化”等条目行文风格一致。

#### entry-00265
- **位置**：`mod-tome.lua:829`；section：`mod-tome/class/Object.lua`
- **原文**：`Damage affinity(heal): `
- **译文**：`伤害亲和（治疗）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1570` 对应 `damage_affinity`（受到该类型伤害时按比例回复生命），括号说明 `（治疗）` 明确机制，准确无误。

#### entry-00266
- **位置**：`mod-tome.lua:837`；section：`mod-tome/class/Object.lua`
- **原文**：`%s cooldown:`
- **译文**：`%s冷却：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1684` 传入 `Talents` 或 `Talent`（对应译文为“技能”），形成“技能冷却：”；占位符 `%s` 保留完整，术语 `cooldown -> 冷却` 规范。

#### entry-00267
- **位置**：`mod-tome.lua:845`；section：`mod-tome/class/Object.lua`
- **原文**：`Reduces incoming crit damage: `
- **译文**：`降低受到的暴击伤害：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1764` 对应 `ignore_direct_crits` 属性，机制为减免直接受到的暴击额外伤害，译文机制准确。

#### entry-00268
- **位置**：`mod-tome.lua:849`；section：`mod-tome/class/Object.lua`
- **原文**：`Maximum encumbrance: `
- **译文**：`负重上限：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1769` 对应 `max_encumber`，译文表达完全符合常规。

#### entry-00269
- **位置**：`mod-tome.lua:850`；section：`mod-tome/class/Object.lua`
- **原文**：`Physical save: `
- **译文**：`物理豁免：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1771` 对应 `combat_physresist`，术语精确匹配术语库优选条目 `Physical Save -> 物理豁免`。

#### entry-00270
- **位置**：`mod-tome.lua:851`；section：`mod-tome/class/Object.lua`
- **原文**：`Spell save: `
- **译文**：`法术豁免：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1772` 对应 `combat_spellresist`，术语精确匹配术语库优选条目 `Spell Save -> 法术豁免`。

#### entry-00271
- **位置**：`mod-tome.lua:852`；section：`mod-tome/class/Object.lua`
- **原文**：`Mental save: `
- **译文**：`精神豁免：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1773` 对应 `combat_mentalresist`，术语精确匹配术语库优选条目 `Mental Save -> 精神豁免`。

#### entry-00272
- **位置**：`mod-tome.lua:885`；section：`mod-tome/class/Object.lua`
- **原文**：`Spellpower on spell critical (stacks up to 3 times): `
- **译文**：`法术暴击时增加法术强度（最多叠加3次）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1813` 与 `Combat.lua:2038`，对应 `spellsurge_on_crit`，暴击时触发 `EFF_SPELLSURGE` 效果提升法术强度且上限叠加 3 层；译文与机制完全吻合。

#### entry-00273
- **位置**：`mod-tome.lua:934`；section：`mod-tome/class/Object.lua`
- **原文**：`Damage Resonance (when hit): `
- **译文**：`伤害共振（受到攻击时）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1877` 与 `data/damage_types.lua:587`，对应 `damage_resonance` 属性（受击时获得共振增伤效果）；译文明确受击触发，准确无误。

#### entry-00274
- **位置**：`mod-tome.lua:937`；section：`mod-tome/class/Object.lua`
- **原文**：`Life regen bonus (wilder-summons): `
- **译文**：`生命回复加成（自然召唤）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1882` 与 `data/talents/gifts/gifts.lua:135`，作用于荒野召唤物（自然召唤兽）的基础生命回复；与同文件 922、936 行“自然召唤”的语境译法高度一致。

#### entry-00275
- **位置**：`mod-tome.lua:943`；section：`mod-tome/class/Object.lua`
- **原文**：`Reduces paradox anomalies(equivalent to willpower): `
- **译文**：`减少紊乱异常（等同意志）：`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1893` 与 `game/modules/tome/class/Actor.lua:5380`，对应 `paradox_reduce_anomalies`，机制为计算时空异常率时直接累加意志属性（`self:getWil() + paradox_reduce_anomalies`）；术语“紊乱”与“意志”契合术语库，机制说明准确。

#### entry-00276
- **位置**：`mod-tome.lua:950`；section：`mod-tome/class/Object.lua`
- **原文**：`Blind-Fight: `
- **译文**：`心眼： `
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1916` 处黄色词条前缀，其后直接拼接描述文本；译文采用全角冒号加空格，在有颜色标签间隔的情况下保留了合理的视觉留白，且“心眼”为 ToME 既有传统译名。

#### entry-00277
- **位置**：`mod-tome.lua:952`；section：`mod-tome/class/Object.lua`
- **原文**：`Lucid Dreamer: `
- **译文**：`清晰梦境： `
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1920` 与 `Actor.lua:1402`，对应 `lucid_dreamer` 属性，装备者在睡眠状态下可正常行动；译名“清晰梦境”准确，格式对齐。

#### entry-00278
- **位置**：`mod-tome.lua:956`；section：`mod-tome/class/Object.lua`
- **原文**：`This item allows the wearer to swap to their secondary weapon without spending a turn.`
- **译文**：`该物品允许装备者在切换至副武器时无需消耗一回合。`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1928` 与 `Actor.lua:4465`，对应 `quick_weapon_swap` 属性，设置 `free_swap = true` 从而免除副武器切换的能量消耗（回合花费）；译文流畅且忠实。

#### entry-00279
- **位置**：`mod-tome.lua:957`；section：`mod-tome/class/Object.lua`
- **原文**：`Avoid Pressure Traps: `
- **译文**：`避免压力陷阱： `
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1932` 与 `game/modules/tome/class/Trap.lua:273`，对应 `avoid_pressure_traps`，使角色不触发 `pressure_trap` 类陷阱；术语“陷阱”与排版均符合规范。

#### entry-00280
- **位置**：`mod-tome.lua:961`；section：`mod-tome/class/Object.lua`
- **原文**：`Learn an unarmed attack talent or enable 'Always show glove combat' to see combat stats.`
- **译文**：`学习徒手攻击技能，或者开启 '强制显示手套战斗数据' 选项来查看战斗数据。`
- **复核结论**：未发现问题
- **核验依据**：源码 `Object.lua:1958` 与设置项 `game/modules/tome/dialogs/GameOptions.lua:417`；游戏设置界面的对应选项名正为“强制显示手套战斗数据”（`#GOLD##{bold}#Always show glove combat properties#WHITE##{normal}#`），译文引用的单引号名称与游戏设置实际文本完全匹配。

---

### 复核总结汇总

- **覆盖条目**：40 条（`entry-00241` 至 `entry-00280` 全部覆盖）。
- **未发现问题**：37 条。
- **细微观察**：3 条：
  1. **entry-00244**：` area effect` -> `范围效果`（英文前导空格拼接在伤害类型后，中文省略空格连缀为“XX范围效果”，符合中文语法习惯）。
  2. **entry-00247**：`%s, %d apr, %s element` -> `%s, %d 护甲穿透，%s 伤害`（法杖属性中 `element` 意译为“伤害”，与 entry-00246 的 `%s damage` 译文相同；虽在法杖实际使用中易于理解，但字面偏离了“元素/属性”的辨识）。
  3. **entry-00254**：` APR (max 50%)` -> ` 护甲穿透（最大 50%）`（与同组 entry-00250~253 无空格的 `（最大40%）` 等相比，本条中多了一个空格，为批内细微排版不一致）。
- **阻断性疑点**：无。占位符类型及数量、颜色控制码及闭合、关键机制与数值计算全部经固定源码验证核实。