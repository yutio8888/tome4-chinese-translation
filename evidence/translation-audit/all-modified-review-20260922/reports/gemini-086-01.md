### 批次核验概况

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-086.md`
- **文件校验**：`sha256sum` 实测结果为 `ed1b27b040aae8c6432ad823a109bbb34b0bd99d1f16ba0312d163aa4e6fff7b`，与冻结哈希一致。
- **条目范围**：`entry-02812` 至 `entry-02851`，共 40 条。
- **源码基准**：公开固定 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4)（涵盖 `game/modules/tome/data/timed_effects/other.lua`、`game/modules/tome/data/timed_effects/physical.lua` 与相关战斗机制调用）。

---

### 逐条复核报告

#### entry-02812
- **原文**：`+Marked!`
- **译文**：`+标记！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:3563`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L3563)（`newEffect{ name = "MARKED" ... on_gain = function(self, err) return nil, _t"+Marked!" end }`）。前缀浮动符号 `+` 与感叹号保留正确，译名与效果名 `Marked`（标记）一致。

#### entry-02813
- **原文**：`The target is lit up by a flare, reducing its stealth and invisibility power by %d, defense by %d and removing all evasion bonus from being unseen.`
- **译文**：`目标被照明弹照亮，潜行和隐身强度减少 %d，闪避减少 %d 并失去不可见状态带来的闪避加成。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:3580`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L3580)（`FLARE` 效果 `long_desc`，传入 `eff.power, eff.power`）。代码分别扣减 `inc_stealth`、`invisible`、`combat_def` 并赋予 `blind_fighted = 1`。两个 `%d` 占位符顺序与类型一致，机制术语（潜行、隐身强度、闪避）完全对齐。

#### entry-02814
- **原文**：`#Target# is struggling to keep his footing!`
- **译文**：`#Target#很难保持平衡！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:3686`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L3686)（`SLIPPERY_GROUND` 获得时的战报文本）。实体占位符 `#Target#` 正确保留，与效果结束时的 `regains their balance`（恢复了平衡）语义互补呼应。

#### entry-02815
- **原文**：`#Target# is energized by the cold!`
- **译文**：`#Target#被寒冷强化！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:3703`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L3703)（`FROZEN_GROUND` 获得时的战报文本）。实体占位符 `#Target#` 与感叹号保留无误。

#### entry-02816
- **原文**：`#Target# regains balance.`
- **译文**：`#Target#重新恢复了平衡。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:3704`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L3704)（`FROZEN_GROUND` 消失时的战报文本）。占位符 `#Target#` 与句末句号完整保留。

#### entry-02817
- **原文**：`Self-Judgement`
- **译文**：`自我审判`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:4163`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L4163)（`SELF_JUDGEMENT` 效果名称）。与对应技能 `Self-Judgement`（自我审判）名称一致。

#### entry-02818
- **原文**：`+Self-Judgement`
- **译文**：`+自我审判`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:4169`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L4169)（`SELF_JUDGEMENT` 获得时的浮动状态标签）。`+` 符号与效果名称一致。

#### entry-02819
- **原文**：`-Self-Judgement`
- **译文**：`-自我审判`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/other.lua:4170`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/other.lua#L4170)（`SELF_JUDGEMENT` 消失时的浮动状态标签）。`-` 符号与效果名称一致。

#### entry-02820
- **原文**：`Scoured by natural acid, reducing their offensive power ratings by %d%%.`
- **译文**：`被自然酸液冲刷，降低攻击强度 %d%%。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:36`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L36)（`ITEM_ANTIMAGIC_SCOURED` 描述）。在 [`game/modules/tome/class/interface/Combat.lua:1387, 1752, 1807, 2137`](file:///workspace/t-engine4/game/modules/tome/class/interface/Combat.lua#L1387) 中，`scoured` 属性将命中基础值及物理、法术、精神攻击强度均除以 1.2。`%d%%` 占位符完整，翻译涵盖了进攻强度的削弱。

#### entry-02821
- **原文**：`#Target# power has recovered.`
- **译文**：`#Target#的强度恢复了。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:41`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L41)（`ITEM_ANTIMAGIC_SCOURED` 消失提示）。占位符 `#Target#` 与句末句号正确保留。

#### entry-02822
- **原文**：
  ```text
  Attuning to the flow of combat, increasing their combat stats.  
  Defense:  %d
  All Damage:  %d%%
  Stamina Regeneration:  %d
  %s
  ```
- **译文**：
  ```text
  进入战斗节奏。增加以下数据：
  闪避：%d
  全体伤害：%d%%
  体力回复：%d
  %s
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:50`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L50)（`RELENTLESS_TEMPO` 效果长描述）。参数按顺序依次传递 `eff.cur_defense`、`eff.cur_damage`、`eff.cur_stamina` 及第 5 层条件追加文本 `%s`。占位符 `%d`、`%d%%`、`%d`、`%s` 顺序、类型与换行行数完全对应。

#### entry-02823
- **原文**：`All Resistance:  20%`
- **译文**：`全体抗性：20%`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:52`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L52)（在 `RELENTLESS_TEMPO` 满 5 层时填充入 entry-02822 末尾的 `%s`）。与代码中 `resists = {all=20}` 机制完全一致。

#### entry-02824
- **原文**：`The target has %d%% chance to evade melee and ranged attacks`
- **译文**：`目标有 %d%% 概率躲闪近战和远程攻击`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:578`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L578)（`EVASION` 描述头部）。源码后接防御加成子串并在最外层拼接 `.. "."`，因此本条末尾不带句号是正确的代码拼合设计；`%d%%` 占位符完整无误。

#### entry-02825
- **原文**：`The target takes on the properties of the hydra, gaining %d%% affinity to lightning, acid, and nature damage and regenerating %d life per turn.`
- **译文**：`目标展现出多头蛇的特性，获得 %d%% 闪电、酸性和自然伤害亲和，每回合回复 %d 生命。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:870`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L870)（`SERPENTINE_NATURE` 描述）。代码赋予 `damage_affinity` 与 `life_regen`。占位符 `%d%%` 与 `%d` 顺序与类型一致，机制表达准确。

#### entry-02826
- **原文**：`The target is attuned to the wild, increasing all damage affinity by %d%% and reducing a random debuff duration by %d each turn.`
- **译文**：`目标和自然协调，增加全体伤害亲和 %d%%，每回合随机减少一个负面状态 %d 回合持续时间。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:898`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L898)（`PRIMAL_ATTUNEMENT` 描述）。代码在 `on_timeout` 中执行 `eff2.dur = eff2.dur - eff.reduce`。占位符 `%d%%` 与 `%d` 保留正确，机制解释清晰。

#### entry-02827
- **原文**：`The target is infused with the power of nature, reducing all blight damage taken by %d%%, increasing spell saves by %d, and granting immunity to diseases.`
- **译文**：`目标得到了自然的力量，减少所有枯萎伤害 %d%%，提升法术豁免 %d，并使其对疾病免疫。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:928`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L928)（`PURGE_BLIGHT` 描述）。占位符 `%d%%` 与 `%d` 对应抗性与豁免提升，术语完全一致。

#### entry-02828
- **原文**：`Improves senses, allowing the detection of unseen things.`
- **译文**：`强化感知，可以看到看不到的东西。`
- **复核结论**：细微观察
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:952`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L952)（`SENSE` 效果长描述）。译文“可以看到看不到的东西”用词偏口语化（较“侦测隐形/未见事物”更直白），但语义对应英文“detection of unseen things”，且无格式/占位符问题，不构成实质缺陷。

#### entry-02829
- **原文**：`#Target# is pinned by a bone spike.`
- **译文**：`#Target#被骨刺定身。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1055`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1055)（`BONE_GRAB` 获得提示）。实体占位符 `#Target#` 正确保留，定身（pin）效果对应准确。

#### entry-02830
- **原文**：`#Target# prepares %s!`
- **译文**：`#Target#准备了%s！`
- **复核结论**：细微观察
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1242`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1242)（`HUNTER_SPEED` 获得提示，`%s` 分别传入 `_t"to escape"`（逃跑）或 `_t"for the next kill"`（为下一次击杀））。拼合后出现“#Target#准备了为下一次击杀！”，带“了”字接介词短语语感略生硬，但格式占位符 `%s`、`#Target#` 及标点完整无损。

#### entry-02831
- **原文**：`#Target# prepares for the next kill!`
- **译文**：`#Target#为下一次杀戮做好了准备！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1278`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1278)（`STEP_UP` 获得提示）。实体占位符 `#Target#` 与感叹号正确保留。

#### entry-02832
- **原文**：`Each melee blow landed has a %d%% chance to trigger an additional melee blow (up to once per turn for each weapon).`
- **译文**：`每次近战命中都有 %d%% 几率触发额外一击（每回合每把武器至多一次）。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1390`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1390)（`GREATER_WEAPON_FOCUS` 描述）。占位符 `%d%%` 保留无误，括号中对触发限制的翻译完全忠实于代码机制。

#### entry-02833
- **原文**：`#Target# is moving defensively!`
- **译文**：`#Target#获得防御步法！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1620`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1620)（`DEFENSIVE_MANEUVER` 获得提示）。实体占位符 `#Target#` 保留完整，与同效果结束提示（“防御步法消失”）术语统一。

#### entry-02834
- **原文**：`#Target# is recovering from the damage!`
- **译文**：`#Target#从伤害中恢复！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1661`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1661)（`Recovery` 获得提示）。占位符 `#Target#` 与标点正确保留。

#### entry-02835
- **原文**：`Increases life regen by %0.2f.`
- **译文**：`增加生命回复 %0.2f。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1749`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1749)（`ELEMENTAL_HARMONY` 触发酸性分支时的长描述）。浮点占位符 `%0.2f` 保留完整无误。

#### entry-02836
- **原文**：`All direct healing done to the target fails, and is instead redirected to %s at %d%% effectiveness.`
- **译文**：`目标受到的直接治疗将被转移至 %s (%d%% 效率)。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1808`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1808)（`HEALING_NEXUS` 长描述）。代码通过 `callbackOnHeal` 将原治疗量设为 0 并按比例转移至来源。占位符 `%s` 与 `%d%%` 顺序与类型完全对应。

#### entry-02837
- **原文**：`#YELLOW_GREEN##Source# steals healing from #Target#!`
- **译文**：`#YELLOW_GREEN##Source#从#Target#偷取了治疗！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1814`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1814)（`HEALING_NEXUS` 窃取治疗战报）。颜色代码 `#YELLOW_GREEN#` 与实体占位符 `#Source#`、`#Target#!` 均完整且无多余空格。

#### entry-02838
- **原文**：`All direct healing done to the target is increased by %d%% and each heal restores %0.1f equilibrium.`
- **译文**：`目标受到的所有直接治疗提高 %d%%，且每次治疗降低 %0.1f 点失衡值。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1831`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1831)（`HEALING_NEXUS_BUFF` 描述）。代码机制为 `self:incEquilibrium(-eff.eq)`，即失衡值减少（趋向平衡）。译文使用“降低 %0.1f 点失衡值”极其精准地体现了数值变动逻辑；占位符 `%d%%` 与 `%0.1f` 正确保留。

#### entry-02839
- **原文**：`#YELLOW_GREEN##Source#'s healing is amplified!`
- **译文**：`#YELLOW_GREEN##Source#的治疗被增幅了！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1838`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1838)（`HEALING_NEXUS_BUFF` 触发战报）。颜色代码 `#YELLOW_GREEN#` 与占位符 `#Source#` 完整保留。

#### entry-02840
- **原文**：`#F53CBE##Target# is bound by telekinetic forces!`
- **译文**：`#F53CBE##Target#被念力困住！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1856`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1856)（`PSIONIC_BIND` 获得提示）。颜色代码 `#F53CBE#` 与占位符 `#Target#` 保留完整。

#### entry-02841
- **原文**：`+Imploding`
- **译文**：`+碎骨压制`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1879`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1879)（`IMPLODING` 获得时的浮动文字）。`+` 符号保留，名称与对应技能 `Implode`（碎骨压制）一致。

#### entry-02842
- **原文**：`-Imploding`
- **译文**：`-碎骨压制`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1880`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1880)（`IMPLODING` 消失时的浮动文字）。`-` 符号与效果名对齐。

#### entry-02843
- **原文**：`#Target# feels a surge of adrenaline.`
- **译文**：`#Target#感到肾上腺素激增。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1921`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1921)（`ADRENALINE_SURGE` 获得提示）。占位符 `#Target#` 与句末句号正确保留。

#### entry-02844
- **原文**：`Blindside Bonus`
- **译文**：`闪电突袭加成`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:1933`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L1933)（`BLINDSIDE_BONUS` 效果名称）。完全契合术语库规范（`Blindside` -> `闪电突袭`）。

#### entry-02845
- **原文**：`#Target# has a cursed wound!`
- **译文**：`#Target#遭受了被诅咒的创伤！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2097`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2097)（`CURSED_WOUND` 获得提示）。占位符 `#Target#` 与感叹号正确保留。

#### entry-02846
- **原文**：`%s has re-opened a cursed wound!`
- **译文**：`%s再次遭受被诅咒的创伤！`
- **复核结论**：细微观察
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2112`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2112)（`CURSED_WOUND` 触发 `on_merge` 叠加时的战报日志，传入受害者名 `%s`）。英文表面意为“%s的诅咒创伤重新裂开”，译文采取意译“再次遭受被诅咒的创伤！”，准确体现了 debuff 被重新刷新的机制事实，属合理意译。

#### entry-02847
- **原文**：`#CRIMSON##Source# heals from blocking with %s shield!`
- **译文**：`#CRIMSON##Source#用%s盾牌格挡，获得了治疗！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2350`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2350)（`BLOCKING` 触发格挡吸血战报，`%s` 传入 `string.his_her(self)`）。颜色代码 `#CRIMSON#` 与占位符 `#Source#`、`%s` 正确保留，拼合后语义通顺。

#### entry-02848
- **原文**：`Countering melee attacks: Has a %d%% chance to get an automatic counter attack when avoiding a melee attack. (%0.1f counters remaining)`
- **译文**：`反击近战攻击：有 %d%% 几率在闪避近战攻击后反击对方。（剩余次数 %0.1f）`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2434`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2434)（`COUNTER_ATTACKING` 长描述）。占位符 `%d%%` 与 `%0.1f` 保留正确，机制逻辑完整传达。

#### entry-02849
- **原文**：`each turn.`
- **译文**：`每回合。`
- **复核结论**：存在疑点
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2531`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2531)。本条作为 `ravaged` 变量的默认值，拼接入 `mod-tome.lua:37433` 的宿主句式中：
  `t("The target is being ravaged by distortion, taking %0.2f physical damage %s", "目标被疯狂扭曲，%s受到 %0.2f 物理伤害", "tformat", {2,1})`。
  宿主句子通过 `{2, 1}` 参数重排将 `%s` 放置在句子中间。此时本条译文中的句号 `。` 导致实际游戏文本渲染为：
  `目标被疯狂扭曲，每回合。受到 <数值> 物理伤害`。
  句号截断了句子中间的语义，属于断句与标点协同缺陷。

#### entry-02850
- **原文**：`and is losing one physical effect turn.`
- **译文**：`每回合失去一个物理效果并`
- **复核结论**：存在疑点
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2532`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2532)。本条是 `RAVAGE` 在 `eff.ravage = true` 时的拼装分支：
  1. 机制语义方面：英文原句字面为“and is losing one physical effect turn.”（减少一个物理效果的回合），但实际上源码 [`physical.lua:2543-2557`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2543) 中执行的是 `self:dispel(eff[2], eff.src)` 随机驱散 1 个物理增益或战技。译者意译为“失去一个物理效果并”虽贴近底层驱散事实，但强行塞入了“每回合”三字；
  2. 模板协同失调：由于译者将本条作为前置从句设计，导致宿主条目 37433 行末尾缺少标点，同时导致 entry-02849（`每回合。`）在同一模板中拼接时产生中间句号断句错误。两条拼装分支在宿主模板下的标点和句式未能协同闭合。

#### entry-02851
- **原文**：`#LIGHT_RED#%s is being ravaged by distortion!`
- **译文**：`#LIGHT_RED#%s被疯狂扭曲了！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 [`game/modules/tome/data/timed_effects/physical.lua:2562`](file:///workspace/t-engine4/game/modules/tome/data/timed_effects/physical.lua#L2562)（`RAVAGE` 强化分支激活时的战报日志）。颜色代码 `#LIGHT_RED#` 与占位符 `%s` 保留完整，与技能/效果名“疯狂扭曲”一致。