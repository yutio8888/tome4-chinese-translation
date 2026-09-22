本批次（batch-087，条目 `entry-02852` 至 `entry-02891`，共 40 条）译文复核基于固定公开源码 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 中的 [`game/modules/tome/data/timed_effects/physical.lua`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua) 及当前译文上下文（终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`）进行了逐条核对。

batch-087.md 文件校验哈希完全匹配：`86fd341d06549aaa34ae825daba077576dfd32def9af06497abfc5ebe422a0f4`。

以下为逐条复核报告：

---

### entry-02852
- **判定**：未发现问题
- **核验依据**：源码 `CORROSIVE_NATURE` 效果的 `long_desc` 返回 `("Acid damage increased by %d%%."):tformat(eff.power)`。占位符 `%d%%` 完整保留，伤害类型“酸性”与源码中 `DamageType.ACID` 增益机制一致，标点准确。

### entry-02853
- **判定**：未发现问题
- **核验依据**：源码 `CORROSIVE_NATURE` 的 `on_merge` 中 `game.logSeen(self, "%s's corrosive nature intensifies!", self:getName():capitalize())`。占位符 `%s` 接收角色名，感叹号完整保留，“腐蚀性增强了”准确传达了叠加层数增强酸伤的机制。

### entry-02854
- **判定**：未发现问题
- **核验依据**：源码 `NATURAL_ACID` 效果的 `long_desc` 返回 `("Nature damage increased by %d%%."):tformat(eff.power)`。占位符 `%d%%` 一致，伤害类型“自然”与源码中 `DamageType.NATURE` 增益机制一致，标点准确。

### entry-02855
- **判定**：未发现问题
- **核验依据**：源码 `CORRODE` 效果的 `long_desc` 传入参数为 `(eff.atk, eff.armor, eff.defense)`，分别削减 `combat_atk`、`combat_armor` 与 `combat_def`。译文三个 `%d` 顺序严格对应“命中”、“护甲值”与“闪避”，未发生错位，标点符号完整。

### entry-02856
- **判定**：细微观察
- **核验依据**：源码 `NATURE_REPLENISHMENT` 的 `on_gain` 中传入参数为 `string.his_her(self)`。译文保留 `%s` 并置于名词前（`建立%s联系`），代词代入后语序顺畅。原文副词 `defiantly`（桀骜不驯地/坚决地）略去未译，属于精简意译，对游戏机制理解无负面影响。

### entry-02857
- **判定**：未发现问题
- **核验依据**：源码 `SKIRMISHER_STUN_INCREASE` 的 `on_gain` 中返回 `("#Target# is stunned further! (now %d turns)"):tformat(stun.dur)`。实体标签 `#Target#`、占位符 `%d` 与半角括号完整保留，术语 stun 译为“震慑”符合规范。

### entry-02858
- **判定**：细微观察
- **核验依据**：源码 `SKIRMISHER_ETERNAL_WARRIOR` 的 `long_desc` 传入 `(eff.res, eff.cap)` 分别增加 `resists.all` 与 `resists_cap.all`。两个 `%0.1f%%` 占位符完全匹配。标点上包含一个半角逗号 `, `（`全体抗性 %0.1f%%, 全体抗性上限`）；原文 "stands strong" 译为“十分强大”，略偏意译，但核心增益机制表述准确。

### entry-02859
- **判定**：未发现问题
- **核验依据**：源码 `SKIRMISHER_DEFENSIVE_ROLL` 的 `on_gain` 文本。标签 `#Target#` 与叹号完整保留，防守姿态与躲避伤害的表述与减免 50% 伤害的机制一致。

### entry-02860
- **判定**：未发现问题
- **核验依据**：源码 `ANTI_GRAVITY` 的 `long_desc`。术语 anti-gravity（反重力）与 knockback resistance（击退抗性）翻译准确，数值减半逻辑与源码激活减值一致。

### entry-02861
- **判定**：未发现问题
- **核验依据**：源码 `PARASITIC_LEECHES` 的效果描述名 `desc = _t"Parasitic Leeches"`。译名“寄生水蛭”准确标准。

### entry-02862
- **判定**：未发现问题
- **核验依据**：源码 `PARASITIC_LEECHES` 的 `charges` 函数中 `("Parasitic Leeches: %d masses"):tformat(eff.nb)`。占位符 `%d` 对应水蛭堆数层数，冒号规范。

### entry-02863
- **判定**：未发现问题
- **核验依据**：源码 `PARASITIC_LEECHES` 的 `long_desc` 依次传入参数为堆数 `eff.nb`（%d）、物理伤害 `eff.dam*eff.nb/2`（%0.2f）、酸性伤害 `eff.dam*eff.nb/2`（%0.2f）与孵化倒计时 `eff.gestation - eff.turns`（%d）。译文四个占位符 `%d`、`%0.2f`、`%0.2f`、`%d` 的类型和顺序完全匹配源码投影计算逻辑。

### entry-02864
- **判定**：未发现问题
- **核验依据**：源码 `PARASITIC_LEECHES` 的 `on_gain`。实体标签 `#Target#` 与颜色控制标签 `#GREEN#`、`#LAST#` 闭合完整，感叹号保留。

### entry-02865
- **判定**：未发现问题
- **核验依据**：源码 `PARASITIC_LEECHES` 的 `on_gain` 浮动提示文本。前缀 `+` 保留，名称与条目 `entry-02861` 保持一致。

### entry-02866
- **判定**：存在疑点
- **核验依据**：源码 `PARASITIC_LEECHES` 在孵化或提前解除时调用 `game.logSeen(self, "Some leeches drop off %s!", self:getName():capitalize())`。同效果条目（`entry-02861` 至 `02865`）均统一译为“水蛭”/“寄生水蛭”，而此处译文为“寄生虫从%s处脱落！”，将 `leeches` 译为“寄生虫”，在同效果内部存在用词不一致。

### entry-02867
- **判定**：未发现问题
- **核验依据**：源码 `GARROTE` 的 `on_gain` 返回 `("%s has garroted #Target#!"):tformat(eff.src and eff.src:getName() or _t"Something")`。占位符 `%s`（施加者）与标签 `#Target#`（受害者）主谓宾语序准确，感叹号保留。

### entry-02868
- **判定**：未发现问题
- **核验依据**：源码 `GARROTE` 的 `on_lose` 返回 `("#Target# is free from %s's garrote."):tformat(eff.src and eff.src:getName() or _t"something")`。标签 `#Target#` 与占位符 `%s` 顺序和句意均准确无误。

### entry-02869
- **判定**：未发现问题
- **核验依据**：源码 `GARROTE` 在 `on_timeout` 中执行 `eff.src:logCombat(self, "#Source# #LIGHT_RED#strangles#LAST# #Target#!")`。标签 `#Source#`、`#LIGHT_RED#`、`#LAST#`、`#Target#` 全部保留，着色代码闭合正确。

### entry-02870
- **判定**：未发现问题
- **核验依据**：源码 `MARKED_FOR_DEATH` 的 `long_desc` 依次传入 `(eff.power, eff.dam, eff.perc*100)`。源码在受击回调中实时把伤害按比例累加进 `eff.dam`（`eff.dam = eff.dam + (cb.value * eff.perc)`）并在失效时结算物理伤害。译文三个占位符 `%d%%`、`%0.1f`、`%d%%` 顺序完全一致，“已追加标记期间受到总伤害的 %d%%”准确反映了该动态累积与结算机制。

### entry-02871
- **判定**：未发现问题
- **核验依据**：源码 `MARKED_FOR_DEATH` 的 `on_gain` 文本。标签 `#Target#` 与感叹号保留，译文简明准确。

### entry-02872
- **判定**：未发现问题
- **核验依据**：源码 `MARKED_FOR_DEATH` 的 `on_gain` 浮动文本。前缀 `+` 与感叹号保留，译名一致。

### entry-02873
- **判定**：未发现问题
- **核验依据**：源码 `DEADLY_POISON` 的 `long_desc` 子句。源码在激活时通过 `self:addTemporaryValue("healing_factor", -eff.insidious / 100)` 扣减治疗系数，前置空格保留，占位符 `%d%%` 与句号完整，“治疗系数”精准对应底层的 `healing_factor` 机制。

### entry-02874
- **判定**：未发现问题
- **核验依据**：源码 `DEADLY_POISON` 的 `long_desc` 子句。前置空格保留，占位符 `%d%%` 与句号完整，准确对应其削弱输出（`numbed`）机制。

### entry-02875
- **判定**：未发现问题
- **核验依据**：源码 `RAZORWIRE` 的 `long_desc` 传入 `(eff.power, eff.power, eff.power)`，分别对应 accuracy、armour 与 defense（代码中均扣减 `eff.power`）。三个 `%d` 占位符顺序完全匹配“命中”、“护甲”与“闪避”，数值对应正确。

### entry-02876
- **判定**：未发现问题
- **核验依据**：源码 `RAZORWIRE` 的 `on_gain` 文本。标签 `#Target#` 与感叹号保留，“刀片刺网”名词翻译准确。

### entry-02877
- **判定**：未发现问题
- **核验依据**：源码 `SHADOW_DANCE` 的 `on_gain` 玩家日志。颜色标签 `#GREY#` 保留，句号保留，文意准确。

### entry-02878
- **判定**：未发现问题
- **核验依据**：源码 `SHADOW_DANCE` 的 `on_lose` 玩家日志。颜色标签 `#GREY#` 保留，句号保留，文意准确。

### entry-02879
- **判定**：未发现问题
- **核验依据**：源码 `BEAR_TRAP` 的 `on_lose` 文本。标签 `#Target#` 保留，句号保留，摆脱陷阱描述准确。

### entry-02880
- **判定**：未发现问题
- **核验依据**：源码 `DWARVEN_RESILIENCE` 的 `on_gain` 文本。标签 `#Target#` 保留，句号保留，皮肤石化效果描述准确。

### entry-02881
- **判定**：未发现问题
- **核验依据**：源码 `STONE_LINK` 的 `long_desc` 返回 `("The target is protected by %s, redirecting all damage to it."):tformat(eff.src:getName())`。占位符 `%s` 对应保护者实体名称，所有伤害重定向机制描述准确。

### entry-02882
- **判定**：未发现问题
- **核验依据**：源码 `EXHAUSTION` 的 `long_desc` 传入 `(eff.fatigue)`。占位符 `%d%%` 保留，Mobility talents 译为“移动系技能”，体力消耗增加机制描述完全符合游戏实现。

### entry-02883
- **判定**：未发现问题
- **核验依据**：源码 `ESCAPE` 的 `on_gain` 浮动文本。前缀 `+` 与感叹号保留，技能译名“逃脱”一致。

### entry-02884
- **判定**：未发现问题
- **核验依据**：源码 `SENTINEL` 的 `on_gain` 浮动文本。前缀 `+` 与感叹号保留，技能译名“哨兵”一致。

### entry-02885
- **判定**：未发现问题
- **核验依据**：源码 `PUNCTURED_ARMOUR` 的 `on_gain` 文本。标签 `#Target#` 与感叹号保留，护甲被刺穿描述准确。

### entry-02886
- **判定**：未发现问题
- **核验依据**：源码 `PUNCTURED_ARMOUR` 的 `on_gain` 浮动文本。前缀 `+` 与感叹号保留，译名“护甲贯通”与技能统一。

### entry-02887
- **判定**：未发现问题
- **核验依据**：源码 `MAIM` 的 `on_gain` 文本。标签 `#Target#` 与感叹号保留，状态名称“伤残”一致。

### entry-02888
- **判定**：未发现问题
- **核验依据**：源码 `CONCEALMENT` 的 `long_desc` 传入 `(eff.sight, eff.power*eff.charges)`。占位符 `%d` 与 `%d%%` 顺序一致，增加“格”契合战棋视野射程网格机制，免伤几率机制描述准确。

### entry-02889
- **判定**：未发现问题
- **核验依据**：源码 `SHADOW_SMOKE` 的 `long_desc` 传入 `(eff.sight)` 对应缩减视野。占位符 `%d` 保留，句号保留，文意准确。

### entry-02890
- **判定**：未发现问题
- **核验依据**：源码 `CHROMATIC_RESISTANCE` 的 `on_gain` 返回 `("#Target##OLIVE_DRAB# resonates with %s%s#LAST# damage!"):tformat(dt.text_color or "#aaaaaa#", dt.name:capitalize())`。标签 `#Target#`、`#OLIVE_DRAB#`、`#LAST#` 及两处 `%s`（颜色代码与伤害类型名）位置正确，感叹号保留。

### entry-02891
- **判定**：细微观察
- **核验依据**：源码 `CHROMATIC_RESISTANCE` 的 `on_lose` 返回类似文本。标签与占位符齐全。与条目 `entry-02890`（`#Target##OLIVE_DRAB#和...`）相比，本条在 `#OLIVE_DRAB#` 与后接中文之间多了一个半角空格（`#Target##OLIVE_DRAB# 不再和...`）。该空格虽不影响游戏引擎富文本渲染，但同组条目排版格式存在微小差异。