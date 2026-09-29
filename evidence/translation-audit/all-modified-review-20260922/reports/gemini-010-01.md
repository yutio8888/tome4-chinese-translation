### batch-010 译文复核报告

#### 基础校验信息
- **复核批次**：batch-010（条目编号：`entry-00361` ～ `entry-00400`，共 40 条）
- **文件 SHA-256 核对**：`fc7d81ad844ddc4fddecac9eadbac7bb5498e4fe732d74b97594c2047303cb8e`（核验一致）
- **公开源码基准**：`/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`
- **译文基准提交**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（同 section 语境核对）

---

### 逐条复核详情

#### entry-00361
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:73` 对应 `status == engine.Quest.COMPLETED` 分支。占位符 `%s` 映射 `quest.name`，颜色码 `#LIGHT_GREEN#` 与 `#WHITE#` 匹配完整；快捷键提示 `(Press 'j' to see the quest log)` 准确译为 `（按 J 键查看任务日志）`，标点全角化自然。

#### entry-00362
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:74` 对应 `saySimple` 大字弹窗。占位符 `%s` 正确保留，颜色代码 `#LIGHT_GREEN#` 完整闭合，句意表达准确。

#### entry-00363
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:77` 对应 `status == engine.Quest.DONE` 分支。`%s` 与 `#LIGHT_GREEN#`、`#WHITE#` 完整保留，日志快捷键按键说明翻译一致，语意通顺。

#### entry-00364
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:78` 对应 `saySimple` 广播。格式占位符 `%s` 与颜色标记 `#LIGHT_GREEN#` 保留完整，句末标点匹配。

#### entry-00365
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:81` 对应 `status == engine.Quest.FAILED` 分支。占位符 `%s` 与 `#LIGHT_RED#`、`#WHITE#` 匹配，快捷键与失败状态提示准确。

#### entry-00366
- **状态**：未发现问题
- **可核验依据**：源码 `PlayerQuestPopup.lua:82` 对应 `saySimple` 广播。占位符 `%s` 与颜色代码 `#LIGHT_RED#` 完好，译文符合大字提示口吻。

#### entry-00367
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:67`（`TOOLTIP_HEALING_MOD`）。机制对应生命恢复与治疗结算时的 `healing_factor` 乘数，译文准确指出“对你的生效程度”、“所有治疗的基础值需要乘上这个系数（包括生命自然恢复）”以及体质影响，`#GOLD#` 与 `#LAST#` 标签及末尾换行均保留。

#### entry-00368
- **状态**：细微观察
- **可核验依据**：源码 `TooltipsData.lua:105`（`TOOLTIP_EQUILIBRIUM`）。首句原文 `Equilibrium reflects your standing in the grand balance of nature` 译为“失衡值是你保持自然平衡的能力”，失衡值本质是一项表征失衡程度的资源状态（越接近 0 越平衡，使用野性技能增加），译为“能力”稍显意译偏离；但后两句准确说明了“越接近0破坏自然平衡的量越少”及“失衡值过高使用野性系技能可能会失败”的底层机制，格式标签正常。

#### entry-00369
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:131`（`TOOLTIP_FEEDBACK`）及 `Actor.lua:5724`。源码证实衰减计算为 `math.max(1, self.psionic_feedback*mult / 10)`，与译文“按 10% 或 1 点（取较大者）衰减”完全吻合；受击增加反馈的数值机制（1级损失50%得100、50级损失20%得100）翻译准确；`psionic grounding` 按术语规范译为“灵能的定锚”，标签完整。

#### entry-00370
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:137`（`TOOLTIP_NECROTIC_AURA`）。译文准确传达了光环范围内击杀提供召唤不死随从原材料（灵魂）的机制，颜色标签及换行一致。

#### entry-00371
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:160`（`TOOLTIP_INSCRIPTIONS`）。严格遵循术语：`Inscriptions` 译为“刻印”，`infusions` 译为“纹身”，`runes` 译为“符文”，`regeneration infusion` 译为“回复纹身”，机制描述清晰，格式完好。

#### entry-00372
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:175`（`TOOLTIP_ACTIVATED`）。将 `activation (i.e. time)` 准确译为“主动（花费时间）”，说明了主动技能消耗时间行动的机制特征，标签对齐。

#### entry-00373
- **状态**：细微观察
- **可核验依据**：源码 `TooltipsData.lua:184`（`TOOLTIP_PASSIVE`）。原文 `permanently alter the user in some way` 中的 `the user` 译为了“给玩家带来改变”。虽然在玩家升级面板界面中面向的是玩家，但游戏中所有 Actor 均可学习拥有被动技能，译为“给使用者”会比“给玩家”在底层概念上更为精确；机制说明与标签本身无异常。

#### entry-00374
- **状态**：存在疑点
- **可核验依据**：源码 `TooltipsData.lua:239`（`TOOLTIP_MAG`）。标题与正文均将该属性译为“魔法/魔法属性”（`#GOLD#魔法#LAST#`、`提升魔法可以提高...`）。但在 ToME 核心定义 `tome/load.lua`（`ActorStats:defineStat("Magic", "mag", ...)`）及术语快照中，六大基础属性之一的 Magic 规范译名是**魔力**（`Magic` -> `魔力`，`mag` -> `魔力`，用于区分 Damage/Category 的“魔法”）。此处提示框标题与角色面板属性名“魔力”产生不一致。

#### entry-00375
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:245`（`TOOLTIP_CUN`）。术语准确对齐：`Cunning` 译为“灵巧”，`Mindpower` 译为“精神强度”，`Mental Save` 译为“精神豁免”，数值关联解释完整无误，格式标签正确。

#### entry-00376
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:272`（`TOOLTIP_COMBAT_APR`）及 `Combat.lua`。明确指出护甲穿透仅针对护甲值、对伤害抗性无效，且减免不会超过护甲上限转换为额外伤害，机制与标签完全准确。

#### entry-00377
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:306`（`TOOLTIP_ARMOR`）及 `Combat.lua`。源码证实武器命中时护甲的减免判定先于暴击和各类百分比乘数结算（`applied before all kinds of critical damage increase...`），译文精确解释了吸收机制与优先判定逻辑，占位与颜色标签完好。

#### entry-00378
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:311`（`TOOLTIP_ARMOR_HARDINESS`）。准确解释了护甲强度即单次攻击所能作用并吸收武器伤害的最大百分比，参数说明与标签无误。

#### entry-00379
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:318`（`TOOLTIP_CRIT_SHRUG`）。准确反映了直接伤害暴击时针对暴击附加伤害部分（bonus critical damage）进行免除判定的机制，括注攻击类型完整，标签完备。

#### entry-00380
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:330`（`TOOLTIP_PHYS_SAVE`）。准确反映物理豁免的双重机制：摆脱判定几率与每超过对手强度 1 点减少 5% 负面状态持续时间，标签保留无误。

#### entry-00381
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:346`（`TOOLTIP_PHYSICAL_CRIT`）。属性影响关联（Cunning -> 灵巧）翻译准确，物理技能暴击额外伤害机制解释清晰，标签匹配。

#### entry-00382
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:354`（`TOOLTIP_SPELL_POWER`）。术语规范对齐（Spellpower -> 法术强度，Spell save -> 法术豁免），精确表述了对手豁免超过法术强度时每点减少 5% 持续时间的机制，格式完备。

#### entry-00383
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:358`（`TOOLTIP_SPELL_CRIT`）。对应法术伤害暴击率，灵巧（Cunning）加成表述明确，标签及换行完整。

#### entry-00384
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:367`（`TOOLTIP_SPELL_COOLDOWN`）。准确解释法术与符文技能冷却乘数机制（数值越低冷却越快），标签保留。

#### entry-00385
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:378`（`TOOLTIP_MIND_CRIT`）。对应精神攻击暴击几率，灵巧（Cunning）影响表述准确，格式标签无误。

#### entry-00386
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:419`（`TOOLTIP_RESIST_SPEED`）及 `Actor.lua:speed_resist`。源码计算公式为 `100 - (util.bound(self.global_speed * self.movement_speed, ...) * 100)`，即整体移动速度越低抗性减免比例越高，并在常规伤害类型抗性之后结算，译文机制与文本一致。

#### entry-00387
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:426`（`TOOLTIP_AFFINITY_ALL`）。机制对应伤害亲和（按比例回血），译文准确翻译了堆叠规则并强调“发生在伤害结算之后，不能防止死亡”（先扣血致死则无法回血）的核心机制，标签匹配。

#### entry-00388
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:431`（`TOOLTIP_AFFINITY`）。特定伤害类型亲和机制与注意条款翻译无误，格式一致。

#### entry-00389
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:435`（`TOOLTIP_STATUS_IMMUNE`）与 `CharacterSheet.lua:1255`。对应角色面板“Effect resistances:”状态免疫栏目，解释百分比完全免除及与豁免判定叠加逻辑准确，标签完好。

#### entry-00390
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:513`（`TOOLTIP_VISION_STEALTH`）。准确解释需要潜行技能激活、隐藏视线、被发现后增加敌人失手几率以及敌方感知识破判定的机制，格式对齐。

#### entry-00391
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:522`（`TOOLTIP_VISION_INVISIBLE`）。准确说明隐形机制以及仅能被具有侦测隐形（see invisible）能力的生物发觉，标签无误。

#### entry-00392
- **状态**：未发现问题
- **可核验依据**：源码 `TooltipsData.lua:268`（`TOOLTIP_COMBAT_BLOCK`）。原文特意转义为 `50%% bonus`，译文保留了转义的 `50%%`；精神伤害不可格挡、盾牌提供对应伤害类型抗性时获得 50% 格挡值加成的机制翻译准确。

#### entry-00393
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:62`（`t2.name = ("%s (Roguelike)"):tformat(t2.name)`）。占位符 `%s` 匹配，Roguelike 模式准确译为“永久死亡模式”。与后文 00395～00400 相比，本条使用无空格的全角括号 `（永久死亡模式）`，属于排版风格的不一致（见下文总结）。

#### entry-00394
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:70`（`t3.name = ("%s (Exploration mode)"):tformat(t3.name)`）。占位符 `%s` 匹配，Exploration mode 准确译为“探索模式”。同样采用无空格全角括号 `（探索模式）`，与 00395～00400 的嵌套括号排版存在风格差异。

#### entry-00395
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:79`（`t4.name = ("%s (Nightmare (Adventure) difficulty)"):tformat(t4.name)`）。占位符 `%s` 匹配，难度与模式术语（噩梦难度、冒险模式）完全正确。排版上采用了半角空格 + 外层半角括号 + 内层全角括号 ` %s (噩梦难度（冒险模式）)`，这是为了避免双重全角括号嵌套，但导致本文件内 00393/00394 与 00395～00400 成就名称后缀格式不统一。

#### entry-00396
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:86`（`t5.name = ("%s (Nightmare (Roguelike) difficulty)"):tformat(t5.name)`）。占位符 `%s` 匹配，术语（噩梦难度、永久死亡模式）准确。括号与空格排版与 00395 一致，同属风格差异。

#### entry-00397
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:94`（`t6.name = ("%s (Insane (Adventure) difficulty)"):tformat(t6.name)`）。占位符 `%s` 匹配，术语（疯狂难度、冒险模式）准确。括号与空格排版与 00395 一致。

#### entry-00398
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:101`（`t7.name = ("%s (Insane (Roguelike) difficulty)"):tformat(t7.name)`）。占位符 `%s` 匹配，术语（疯狂难度、永久死亡模式）准确。括号与空格排版与 00395 一致。

#### entry-00399
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:109`（`t8.name = ("%s (Madness (Adventure) difficulty)"):tformat(t8.name)`）。占位符 `%s` 匹配，Madness 对应开局选择及成就模式确立译名“绝望难度”，Adventure 对应“冒险模式”，术语机制准确。括号与空格排版与 00395 一致。

#### entry-00400
- **状态**：细微观察
- **可核验依据**：源码 `WorldAchievements.lua:116`（`t9.name = ("%s (Madness (Roguelike) difficulty)"):tformat(t9.name)`）。占位符 `%s` 匹配，术语（绝望难度、永久死亡模式）准确。括号与空格排版与 00395 一致。

---

### 复核疑点与观察汇总

1. **术语一致性疑点**：
   - **`entry-00374`（`TOOLTIP_MAG`）**：在角色属性定义与术语规范中，六大主属性之一的 `Magic` 规范译名为**「魔力」**（`mag` -> `魔力`）。此处提示框标题为 `#GOLD#魔法#LAST#`，正文为 `魔法属性影响你驾驭魔法能量的能力，提升魔法可以提高...`，导致提示框标题及属性代称与面板主属性名「魔力」不一致。

2. **细节观察与排版风格**：
   - **`entry-00368`（`TOOLTIP_EQUILIBRIUM`）**：首句将 `standing in the grand balance of nature` 译为“保持自然平衡的能力”，因失衡值本身是一项状态数值而非能力，措辞略偏意译，但后续机制解释准确。
   - **`entry-00373`（`TOOLTIP_PASSIVE`）**：原文 `alter the user` 译为“给玩家带来改变”，在底层概念上 `the user` 泛指所有拥有技能的单位，译为“使用者”更为严谨。
   - **`entry-00393` ～ `entry-00400`（`WorldAchievements.lua`）**：成就后缀字符串的括号格式不一致。单模式成就（`00393`、`00394`）采用无空格的全角括号（`%s（永久死亡模式）`、`%s（探索模式）`），而难度加模式成就（`00395`～`00400`）采用前导半角空格、外层半角括号加内层全角括号（`%s (XX难度（YY模式）)`）。建议后续批次统一排版风格。