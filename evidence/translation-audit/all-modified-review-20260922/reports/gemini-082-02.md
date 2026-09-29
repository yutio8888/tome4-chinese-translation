### batch-082 译文复核报告

#### 基础信息与哈希核验
- **复核批次**：`batch-082`（共 40 条，范围：`entry-02652` 至 `entry-02691`）
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-082.md`
- **文件 SHA-256 核验**：
  - 预期哈希：`de41835bb43127ed8a20024fcbb4ca6af653ddaaa2d844fe977ea74219fd3df0`
  - 实测哈希：`de41835bb43127ed8a20024fcbb4ca6af653ddaaa2d844fe977ea74219fd3df0`（一致，核验通过）
- **核验依据版本**：
  - 公开引擎与本体源码：commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取对应文件）
  - 译文终点基准：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

### 逐条复核详情

#### entry-02652
- **位置**：`mod-tome.lua:35504`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`Target is reeling from an lightning shock, halving its stun and pinning resistance.`
- **译文**：`目标被强力的闪电所震撼，震慑与定身免疫减半。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3429`（状态 `SHOCKED`），激活代码为 `self:effectTemporaryValue(eff, "stun_immune", -self:attr("stun_immune") / 2)` 及 `self:effectTemporaryValue(eff, "pin_immune", -self:attr("pin_immune") / 2)`，机制确实是将底层震慑免疫（`stun_immune`）与定身免疫（`pin_immune`）削减一半。原文存在语法笔误“an lightning shock”，译文平滑处理为“强力的闪电所震撼”，语义通顺且与游戏底层逻辑一致。无占位符，标点完整。

#### entry-02653
- **位置**：`mod-tome.lua:35555`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Unravels!`
- **译文**：`解体！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3755`（状态 `UNRAVEL` 失效且生命值低于阈值时的地图漂浮文字 `game.flyers:add(..., _t"Unravels!", {255,0,255})`）。短语简洁准确，感叹号保留。

#### entry-02654
- **位置**：`mod-tome.lua:35556`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`logSeen`
- **原文**：`%s has unraveled!`
- **译文**：`%s 被解体了！`
- **核验结果**：未发现问题（细微观察）
- **可核验依据**：源码位于 `timed_effects/magical.lua:3756`（`game.logSeen(self, "%s has unraveled!", self:getName():capitalize())`）。占位符 `%s` 匹配，感叹号保留。细微观察：原文动词为主动完成时（指自身崩溃解体），译文加上被动语态“被解体了”，符合技能造成致死效果的语境，不影响理解。

#### entry-02655
- **位置**：`mod-tome.lua:35569`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Attenuate`
- **译文**：`衰减`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3807, 3846`（时空系负面/增益状态 `ATTENUATE_DET` 与 `ATTENUATE_BEN` 的 `desc`）。译名“衰减”准确规范。

#### entry-02656
- **位置**：`mod-tome.lua:35572`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`+Attenuate`
- **译文**：`+衰减`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3813, 3852`（状态获得浮动文字）。前缀 `+` 保留，状态名称与 entry-02655 统一。

#### entry-02657
- **位置**：`mod-tome.lua:35573`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# survived the attenuation.`
- **译文**：`#Target#从衰减中存活了下来。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3814`（`on_lose` 回调提示）。实体标记 `#Target#` 保持原样，时空系衰减伤害结束未致死的日志提示翻译准确。

#### entry-02658
- **位置**：`mod-tome.lua:35574`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`-Attenuate`
- **译文**：`-衰减`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3814, 3853`（状态消失浮动文字）。前缀 `-` 保留，状态名称统一。

#### entry-02659
- **位置**：`mod-tome.lua:35575`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`logSeen`
- **原文**：`%s has been removed from the timeline!`
- **译文**：`%s 被移出时间线！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3833`（状态 `ATTENUATE_DET` 在目标生命值低于 20% 触发秒杀时的日志）。占位符 `%s` 匹配，感叹号保留，翻译精准。

#### entry-02660
- **位置**：`mod-tome.lua:35582`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# enters an ogric frenzy.`
- **译文**：`#Target#陷入食人魔般的狂怒。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:3876`（食人魔符文状态 `OGRIC_WRATH` 的 `on_gain` 日志）。实体标记 `#Target#` 保留完整，句号保留，译文贴合符文背景设定。

#### entry-02661
- **位置**：`mod-tome.lua:35603`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Warden's Focus`
- **译文**：`守卫者专注`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4036`（时空守卫同名技能状态的 `desc`）。译名“守卫者专注”符合职业专长统一称谓。

#### entry-02662
- **位置**：`mod-tome.lua:35604`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`Focused on %s, +%d%% critical damage and +%d%% critical hit chance against this target.`
- **译文**：`集中于 %s，对其增加 %d%% 暴击伤害与 %d%% 暴击率。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4038`，传参为 `tformat(eff.target:getName(), eff.power, eff.power)`。占位符 `%s`（目标名称）、`%d%%`（暴击伤害增量）、`%d%%`（暴击率增量）顺序、数量与格式完全吻合，机制对应准确。

#### entry-02663
- **位置**：`mod-tome.lua:35605`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`+Warden's Focus`
- **译文**：`+守卫者专注`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4043`（状态获得浮动文字）。前缀 `+` 保留，名称与 entry-02661 一致。

#### entry-02664
- **位置**：`mod-tome.lua:35606`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`-Warden's Focus`
- **译文**：`-守卫者专注`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4044`（状态移除浮动文字）。前缀 `-` 保留，名称与 entry-02661 一致。

#### entry-02665
- **位置**：`mod-tome.lua:35611`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# weaves fate.`
- **译文**：`#Target#编织命运。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4077`（时空系技能状态 `FATEWEAVER` 的 `on_gain` 日志）。实体标记 `#Target#` 保留，句号保留，翻译准确。

#### entry-02666
- **位置**：`mod-tome.lua:35613`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# stops weaving fate.`
- **译文**：`#Target#停止编织命运。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4078`（状态 `FATEWEAVER` 的 `on_lose` 日志）。实体标记 `#Target#` 保留，句号保留，与 entry-02665 形成准确动作对照。

#### entry-02667
- **位置**：`mod-tome.lua:35617`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# is nearing the end.`
- **译文**：`#Target#接近末日。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4122`（状态 `FOLD_FATE` 削弱目标物理与时空抗性时的 `on_gain` 日志）。实体标记 `#Target#` 保持完整，句意简练通顺。

#### entry-02668
- **位置**：`mod-tome.lua:35627`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# is poisoned with blight!`
- **译文**：`#Target#中了枯萎毒素！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4181`（状态 `BLIGHT_POISON` 的 `on_gain` 日志）。实体标记 `#Target#` 保留，感叹号保留，术语 blight（枯萎）与 poison（毒素）使用准确。

#### entry-02669
- **位置**：`mod-tome.lua:35633`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# is poisoned with insidious blight!!`
- **译文**：`#Target#中了阴险枯萎毒素！！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4206`（状态 `INSIDIOUS_BLIGHT` 的 `on_gain` 日志）。双感叹号 `!!` 精确还原，实体标记完整，术语 insidious blight 译为“阴险枯萎毒素”一致。

#### entry-02670
- **位置**：`mod-tome.lua:35639`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# is poisoned with crippling blight!`
- **译文**：`#Target#中了致残枯萎毒素！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4238`（状态 `CRIPPLING_BLIGHT` 的 `on_gain` 日志）。实体标记保留，感叹号保留，术语 crippling blight 对应“致残枯萎毒素”规范。

#### entry-02671
- **位置**：`mod-tome.lua:35645`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# is poisoned numbing blight!`
- **译文**：`#Target#中了麻痹枯萎毒素！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4266`（状态 `NUMBING_BLIGHT` 的 `on_gain` 日志）。原文源码遗漏介词 with，译文不受影响，平滑译为“中了麻痹枯萎毒素！”，标记与感叹号完整。

#### entry-02672
- **位置**：`mod-tome.lua:35668`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`Fire and Light damage increased by %d%%.`
- **译文**：`火焰和光系伤害增加 %d%%。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4427`（状态 `BATHE_IN_LIGHT` 的 `long_desc`），激活代码增加 `DamageType.FIRE` 与 `DamageType.LIGHT`。占位符 `%d%%` 精确匹配，伤害类型“火焰”与“光系”（符合术语表光系伤害规范）一致。

#### entry-02673
- **位置**：`mod-tome.lua:35669`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# glows intensely!`
- **译文**：`#Target#发出强光！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4432`（状态 `BATHE_IN_LIGHT` 的 `on_gain` 提示）。实体标记 `#Target#` 保留，感叹号保留，翻译简洁自然。

#### entry-02674
- **位置**：`mod-tome.lua:35673`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`Detects creatures of type %s/%s in radius 15.`
- **译文**：`在15格范围内感知以下种族：%s/%s。`
- **核验结果**：未发现问题（细微观察）
- **可核验依据**：源码位于 `timed_effects/magical.lua:4445`（高等人类天赋状态 `OVERSEER_OF_NATIONS`），参数为 `type="humanoid", subtype="human"`，底层 `esp_range` 增加 5（基础 10+5=15）。占位符 `%s/%s` 匹配，范围 15 格匹配。细微观察：type/subtype 译为“种族”通俗易懂，符合此类感知技能的显示习惯。

#### entry-02675
- **位置**：`mod-tome.lua:35683`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`The target is hexed.  Each time it uses an ability it takes %0.2f fire damage, and talent cooldowns are increased by %s plus 1 turn.`
- **译文**：`目标受邪术影响，每次施放技能都会受到 %0.2f 火焰伤害，技能冷却延长 %s 再延长 1 回合。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4492`（状态 `BURNING_HEX`），传参为 `eff.dam` 与格式化百分比字符串（如 `"30%"` 或空）。占位符 `%0.2f` 与 `%s` 顺序、类型完全一致。译文“技能冷却延长 %s 再延长 1 回合”结构能妥善嵌合百分比数值，机制表达准确。

#### entry-02676
- **位置**：`mod-tome.lua:35687`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`The target is hexed, creating an empathic bond with its victims. It takes %d%% feedback damage from all damage done.`
- **译文**：`目标受到邪术影响，与其受害者之间建立起共感联结。它所造成的全部伤害中有 %d%% 会作为反馈伤害返还其自身。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4508`（状态 `EMPATHIC_HEX`），底层机制为 `self:addTemporaryValue("martyrdom", eff.power)`。占位符 `%d%%` 匹配。译文将“feedback damage from all damage done”阐明为“造成的全部伤害中有 %d%% 会作为反馈伤害返还其自身”，准确无歧义。

#### entry-02677
- **位置**：`mod-tome.lua:35692`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`The target is hexed, temporarily changing its faction to %s.`
- **译文**：`目标受邪术影响，暂时改变阵营至 %s。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4531`（状态 `DOMINATION_HEX`），传参为阵营名称 `engine.Faction.factions[eff.faction].name`。占位符 `%s` 匹配，阵营机制对应准确。

#### entry-02678
- **位置**：`mod-tome.lua:35739`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`The mere sight of a Lich sent you into a frightened state, reducing all saves by %d, all damage by %d%% and movement speed by %d%%.`
- **译文**：`巫妖的恐怖存在让你陷入深度恐惧之中，所有豁免降低 %d，所有伤害减少 %d%%，移动速度降低 %d%%。`
- **核验结果**：未发现问题（细微观察）
- **可核验依据**：源码位于 `timed_effects/magical.lua:4731`（巫妖威压状态 `LICH_FEAR`），传参为 `eff.saves, eff.dam, eff.speed`。代码实际扣减全部豁免、全部伤害百分比和移动速度。三个占位符 `%d`、`%d%%`、`%d%%` 顺序与类型完全对应。细微观察：前半句“The mere sight of a Lich”（仅目睹巫妖一眼）意译为“巫妖的恐怖存在”，受到其对应天赋名“Frightening Presence（恐慌存在）”影响，在保证机制数值完全准确的前提下，中文行文符合奇幻氛围。

#### entry-02679
- **位置**：`mod-tome.lua:35751`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Lord of Skulls (warrior)`
- **译文**：`骷髅王（战士）`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4809`（状态 `LORD_OF_SKULLS` 作用于骷髅战士随从时的重命名）。术语 Lord of Skulls 统一为“骷髅王”，括号职业对应战士，准确无误。

#### entry-02680
- **位置**：`mod-tome.lua:35752`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Lord of Skulls (archer)`
- **译文**：`骷髅王（弓箭手）`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4810`。术语统一，弓箭手随从对应准确。

#### entry-02681
- **位置**：`mod-tome.lua:35753`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Lord of Skulls (mage)`
- **译文**：`骷髅王（法师）`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4811`。随从类型对应骷髅法师，译为“骷髅王（法师）”准确。

#### entry-02682
- **位置**：`mod-tome.lua:35754`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Lord of Skulls (bone giant)`
- **译文**：`骷髅王（骨巨人）`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4812`。随从类型对应骨巨人，译为“骷髅王（骨巨人）”规范。

#### entry-02683
- **位置**：`mod-tome.lua:35755`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Spike of Decrepitude`
- **译文**：`衰老尖刺`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:4857`（死灵法术负面状态 `SPIKE_OF_DECREPITUDE` 的 `desc`）。译名“衰老尖刺”准确规范。

#### entry-02684
- **位置**：`mod-tome.lua:35780`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# summons a corpselight!`
- **译文**：`#Target#召唤阴燃鬼火！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:5037`（状态 `CORPSELIGHT` 的 `on_gain` 日志）。实体标记 `#Target#` 保留，感叹号保留，技能名与死灵天赋 Corpselight（阴燃鬼火，参见 `mod-tome.lua:29065`）统一。

#### entry-02685
- **位置**：`mod-tome.lua:35791`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`tformat`
- **原文**：`Magically frozen wound that deals %0.2f cold damage per turn and movement speed reduced by %d%%.`
- **译文**：`被魔法冻结的伤口，每回合受到 %0.2f 寒冷伤害，移动速度降低 %d%%。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:5148`（状态 `FROST_CUT` 的 `long_desc`），传参为 `eff.power, eff.speed`。占位符 `%0.2f` 与 `%d%%` 匹配，伤害类型 cold->寒冷 准确，状态描述符合游戏常规行文。

#### entry-02686
- **位置**：`mod-tome.lua:35792`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# starts to bleed ice.`
- **译文**：`#Target# 开始渗出寒冰。`
- **核验结果**：未发现问题（细微观察）
- **可核验依据**：源码位于 `timed_effects/magical.lua:5154`（状态 `FROST_CUT` 的 `on_gain` 日志）。实体标记 `#Target#` 完整，bleed ice 结合寒冰伤口状态译为“渗出寒冰”生动贴切。细微观察：`#Target#` 标记后包含一个半角空格，运行时虽不影响标记替换，但与本批次部分无空格条目略有排版差异。

#### entry-02687
- **位置**：`mod-tome.lua:35794`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# stops bleeding ice.`
- **译文**：`#Target# 不再渗出寒冰。`
- **核验结果**：未发现问题（细微观察）
- **可核验依据**：源码位于 `timed_effects/magical.lua:5155`（状态 `FROST_CUT` 的 `on_lose` 日志）。实体标记 `#Target#` 完整，与 entry-02686 对应。同样含有标记后的半角空格排版。

#### entry-02688
- **位置**：`mod-tome.lua:35800`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`#Target# picks up the remains of its fallen comrade.`
- **译文**：`#Target# 捡起了同伴的骨头。`
- **核验结果**：存在疑点
- **可核验依据**：源码位于 `timed_effects/magical.lua:5186`（死灵骷髅随从状态 `SHATTERED_REMAINS` 的 `on_gain` 日志，对应失去状态为 `drops its additional bones`）。
  1. 漏译修饰词：原文中的修饰词“fallen”（阵亡的/倒下的）在译文中被漏译，仅译为“同伴”，丢失了“同伴已倒下/牺牲”的核心语境信息；
  2. 意译用词偏差：原文“the remains”（遗骸/残骸）被口语化替换为“骨头”。虽然骷髅随从机制上确实是拼装额外碎骨，但日志文本使用庄重的“the remains of its fallen comrade”，译为“捡起了同伴的骨头”存在风格降级和字面漏译。建议后续考量优化为“#Target# 捡起了倒下同伴的遗骸。”或“#Target# 捡起了阵亡同伴的残骸。”。

#### entry-02689
- **位置**：`mod-tome.lua:35804`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Rime Wraith (Gelid Host)`
- **译文**：`远古冰魂（霜寒宿主）`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:5288`。怪物及状态前缀 Rime Wraith 统一为“远古冰魂”，副标题 Gelid Host 译为“霜寒宿主”准确。

#### entry-02690
- **位置**：`mod-tome.lua:35822`；**section**：`mod-tome/data/timed_effects/magical.lua`；**source_tag**：`_t`
- **原文**：`Can move once for free, this turn only.`
- **译文**：`仅限本回合可以不耗时间移动一次。`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/magical.lua:5411`（状态 `SLIPSTREAM` 的 `long_desc`），底层赋予临时属性 `free_movement=1`（移动不消耗回合时间与能量）。译文“仅限本回合可以不耗时间移动一次”精准直白地揭示了底层机制，且无多余修饰。

#### entry-02691
- **位置**：`mod-tome.lua:35862`；**section**：`mod-tome/data/timed_effects/mental.lua`；**source_tag**：`_t`
- **原文**：`#Target#'s is vulnerable to attacks and effects!`
- **译文**：`#Target#易受攻击和效果的影响！`
- **核验结果**：未发现问题
- **可核验依据**：源码位于 `timed_effects/mental.lua:38`（精神状态 `ITEM_EXPOSED` 的 `on_gain` 日志）。原文源码存在笔误“#Target#'s is vulnerable...”（多出所有格 `'s`），译文不受源码语病干扰，准确表达出该状态削弱豁免与防御的本质，实体标记与感叹号保留完整。

---

### 复核总结
- **核验总量**：40 条（`entry-02652` 至 `entry-02691` 已全部逐条覆盖）。
- **核验通过（未发现问题）**：39 条。
  - 占位符（`%s`、`%d`、`%d%%`、`%0.2f` 等）及参数顺序均与源码实现严格对齐。
  - 实体标记（`#Target#`）及符号标记（`+`、`-`、感叹号）均保持原样。
  - 包含若干细微观察（如 entry-02654 被动语态、entry-02678 氛围化意译、entry-02686/02687 格式半角空格），均不影响功能与阅读。
- **存在疑点**：1 条。
  - **`entry-02688`**：`#Target# picks up the remains of its fallen comrade.` -> `#Target# 捡起了同伴的骨头。`（漏译了修饰词“fallen”，且将“the remains”具象化意译为“骨头”，存在关键信息缺失）。