### 复核准备核对

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-069.md`
- **SHA-256 核对结果**：`2c349073a9d239b6b816ccb0f216bc882fd8a79f4969d1ceefd3afc9fc9fec2b`（一致）
- **复核范围**：`entry-02149` 至 `entry-02187`（共 39 条，已排除 `entry-02148`）
- **源码比对基准**：`/workspace/t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 查阅）

---

### 条目逐项复核报告

#### entry-02149
- **位置**：`mod-tome.lua:27906` / `mod-tome/data/talents/psionic/solipsism.lua`（唯我论 `Solipsism`）
- **判定**：存在疑点
- **可核验依据**：
  1. **术语疑点**：原文末句 `reducing your global speed by 1%% for each percentage...` 被翻译为“你的所有速度减少 1 %%”。术语库规范（快照第 661–662、706–707 行）明确指出 `global speed` 应译为“全局速度”，并特别标注“不写作‘整体速度’或‘全体速度’”。“所有速度”与“全局速度”概念存在偏差。
  2. **信息减损**：原文 `(%0.1f%% from character level with the remainder further reduced by %0.1f%% from talent level)` 表达的是在角色等级减免后的“剩余部分”再由技能等级按比例减少（源码 `100 - (100 - talentmod)/lifemod`），译文“%0.1f%% 来自于人物等级，%0.1f%% 来自于技能等级。”略去了乘算/剩余部分逻辑，表述易被误解为简单加算。
  3. **非原文增补说明**：译文中增加了“（高于基础值 10 的）”和“（若低于基础值 10 则增加生命上限）”，这是译者基于底层代码 `(self:getWil()-10)` 自行添加的说明，英文原文无此文本。
  4. **占位符**：6 个占位符（`%d%%`, `%d%%`, `%0.1f%%`, `%0.1f%%`, `%0.1f%%`, `%d%%`）数量及顺序与源码一致。第 2 行末尾中文缺少句号。

#### entry-02150
- **位置**：`mod-tome.lua:27917` / `mod-tome/data/talents/psionic/solipsism.lua`（平衡 `Balance`）
- **判定**：细微观察
- **可核验依据**：
  1. 占位符数量与类型匹配（3 个 `%d%%`，依次对应精神豁免替代物理/法术豁免比例、唯我临界点增加值）。
  2. 与 entry-02149 类似，译文包含原文未出现的代码机制增补解释“（高于基础值 10 的）每点意志...（若低于基础值 10 则增加生命上限）”。
  3. 数字与百分号间存在多余空格（`100 %%`、`10 %%`）。

#### entry-02151
- **位置**：`mod-tome.lua:27923` / `mod-tome/data/talents/psionic/solipsism.lua`（明晰 `Clarity`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d%%`、`%+d%%`、`%d%%` 数量与带符号格式符匹配；`global speed` 正确翻译为“全局速度”；未包含冗余括号说明，机制表述清晰准确。

#### entry-02152
- **位置**：`mod-tome.lua:27927` / `mod-tome/data/talents/psionic/solipsism.lua`（忽视 `Dismissal` 日志）
- **判定**：未发现问题
- **可核验依据**：颜色代码 `#TAN#` 与实体占位符 `#Source#` 完整保留，语义“精神上豁免了部分伤害！”忠实对应原文 `mentally dismisses some damage!`。

#### entry-02153
- **位置**：`mod-tome.lua:27929` / `mod-tome/data/talents/psionic/solipsism.lua`（忽视 `Dismissal` 描述）
- **判定**：细微观察
- **可核验依据**：
  1. 占位符 `%d%%`、`%d%%` 数量与顺序一致。
  2. 选词微瑕：原文 `roll %d%% of your mental save against it` 译为“使用 %d%% 精神豁免来鉴定”，RPG 语境中豁免通常称为“检定”或“判定”，“鉴定”多用于物品识别。
  3. 同样含有译者对体质/意志低于基础值 10 时的额外注释。

#### entry-02154
- **位置**：`mod-tome.lua:27976` / `mod-tome/data/talents/psionic/thermal-mastery.lua`（热量转移 `Heat Shift`）
- **判定**：未发现问题
- **可核验依据**：5 个占位符 `%d`、`%0.1f`、`%0.1f`、`%d`、`%d` 顺序与类型完全对应（半径、寒冷伤害、火焰伤害、持续回合、护甲及豁免削减）；状态名“定身（冻足）”与“缴械”符合机制。

#### entry-02155
- **位置**：`mod-tome.lua:27997` / `mod-tome/data/talents/psionic/thought-forms.lua`（召唤失败日志）
- **判定**：未发现问题
- **可核验依据**：原文 `Not enough space to summon!` 对应“没有足够的空间召唤！”，感叹号及语义与日志上下文完全吻合。

#### entry-02156
- **位置**：`mod-tome.lua:27999` / `mod-tome/data/talents/psionic/thought-forms.lua`（精神体弓箭手描述）
- **判定**：未发现问题
- **可核验依据**：无占位符，纯文本描述准确传达原文 `A thought-forged bowman. It appears ready for battle.`。

#### entry-02157
- **位置**：`mod-tome.lua:28000` / `mod-tome/data/talents/psionic/thought-forms.lua`（思维形态：弓箭手描述）
- **判定**：未发现问题
- **可核验依据**：3 个 `%d`（力量、敏捷、体质）占位符完整；涉及技能（弓术掌握、强化命中、稳固射击、致残射击、急速射击）与源码 `T_WEAPON_COMBAT`、`T_BOW_MASTERY` 等命名一致。

#### entry-02158
- **位置**：`mod-tome.lua:28005` / `mod-tome/data/talents/psionic/thought-forms.lua`（技能名）
- **判定**：未发现问题
- **可核验依据**：`Thought-Form: Warrior` 译为“思维形态：战士”，符合术语库（快照第 684–685 行）对 `Thought-Forms` 为“思维形态”的标准规范。

#### entry-02159
- **位置**：`mod-tome.lua:28006` / `mod-tome/data/talents/psionic/thought-forms.lua`（实体名称）
- **判定**：未发现问题
- **可核验依据**：`thought-forged warrior` 译为“精神体战士”，与同系召唤物命名保持统一。

#### entry-02160
- **位置**：`mod-tome.lua:28007` / `mod-tome/data/talents/psionic/thought-forms.lua`（精神体战士描述）
- **判定**：未发现问题
- **可核验依据**：忠实翻译手持巨型战斧、身穿重甲等装备外观特征，标点与语义准确。

#### entry-02161
- **位置**：`mod-tome.lua:28008` / `mod-tome/data/talents/psionic/thought-forms.lua`（思维形态：战士描述）
- **判定**：未发现问题
- **可核验依据**：3 个 `%d` 属性加成占位符完全匹配；技能列表“武器掌握、强化命中、嗜血、死亡之舞和冲锋”对应源码 `T_WEAPONS_MASTERY`, `T_WEAPON_COMBAT`, `T_BERSERKER`, `T_DEATH_DANCE`, `T_RUSH`。

#### entry-02162
- **位置**：`mod-tome.lua:28016` / `mod-tome/data/talents/psionic/thought-forms.lua`（思维形态：盾战士描述）
- **判定**：未发现问题
- **可核验依据**：3 个 `%d` 占位符完整对应力量、敏捷、体质；技能列表“护甲掌握、武器掌握、强化命中、盾牌连击和盾墙”准确对应源码 `T_ARMOUR_TRAINING` 至 `T_SHIELD_WALL`。

#### entry-02163
- **位置**：`mod-tome.lua:28022` / `mod-tome/data/talents/psionic/thought-forms.lua`（思维形态基底技能）
- **判定**：未发现问题
- **可核验依据**：3 个 `%d`（主属性增益、副属性增益、维持范围）占位符一致；随技能等级解锁的三种召唤物描述层级分明，数值与机制说明准确。

#### entry-02164
- **位置**：`mod-tome.lua:28037` / `mod-tome/data/talents/psionic/thought-forms.lua`（主脑支配 `Over Mind`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d%%`（加成百分比）匹配；技能 1、3、5 级阶梯效果（反馈值共享、精神豁免共享、精神伤害加成共享）翻译完全符合源码逻辑。

#### entry-02165
- **位置**：`mod-tome.lua:28047` / `mod-tome/data/talents/psionic/thought-forms.lua`（思维形态合一 `Thought-Form Unity`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d%%`（精神速度）、`%d`（精神强度）、`%d%%`（全抗性）顺序及类型与源码 `tformat(speed, offense, defense, speed)` 完全对应；技能名与属性术语统一。

#### entry-02166
- **位置**：`mod-tome.lua:28057` / `mod-tome/data/talents/psionic/trance.lua`（纯净入定 `Trance of Purity`）
- **判定**：未发现问题
- **可核验依据**：占位符 `-%d%%`（衰减几率）与 `%d`（所有豁免）类型正确，译文用“再降低 %d%%”妥善处理负号；`trance` 遵循术语库标准（快照第 743 行）译为“入定”。

#### entry-02167
- **位置**：`mod-tome.lua:28075` / `mod-tome/data/talents/psionic/trance.lua`（深度入定 `Deep Trance`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d%%` 匹配；UI 引用字段 `'when wielded/worn'` 准确翻译为游戏中对应的装备描述“当使用或装备时：”，对反魔力量与自身生效逻辑表述准确。

#### entry-02168
- **位置**：`mod-tome.lua:28108` / `mod-tome/data/talents/psionic/voracity.lua`（贪得无厌 `Insatiable`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`、`%0.1f`、`%0.1f` 匹配；英文原文 `maximum energy` 实际上在代码中为 `self:talentTemporaryValue(p, "max_psi", recover*5)`，译文译为“灵能值上限”准确对齐源码实际机制。

#### entry-02169
- **位置**：`mod-tome.lua:28120` / `mod-tome/data/talents/spells/acid-alchemy.lua`（腐蚀傀儡 `Caustic Golem`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（持续回合）、`%d%%`（反击几率）、`%0.1f`（酸性伤害）顺序完全对应；`Acid Infusion` 按炼金术师技能规范译为“酸性充能”，机制阐述精准。

#### entry-02170
- **位置**：`mod-tome.lua:28126` / `mod-tome/data/talents/spells/acid-alchemy.lua`（腐蚀酸沼 `Caustic Mire`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（半径）、`%0.1f`（酸性伤害）、`%d`（持续回合）、`%d%%`（减速比例）数量与顺序完全一致。

#### entry-02171
- **位置**：`mod-tome.lua:28144` / `mod-tome/data/talents/spells/advanced-golemancy.lua`（生命汲取 `Life Tap`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（吸取生命数值）准确，简短表述符合技能执行逻辑。

#### entry-02172
- **位置**：`mod-tome.lua:28146` / `mod-tome/data/talents/spells/advanced-golemancy.lua`（宝石镶嵌 `Gem Golem`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（宝石等级）匹配；镶嵌/取下不损坏宝石机制及物品栏操作提示说明清晰。

#### entry-02173
- **位置**：`mod-tome.lua:28159` / `mod-tome/data/talents/spells/advanced-golemancy.lua`（符文傀儡 `Runic Golem`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%0.2f`（回复速度增益）与源码格式完全吻合；符文槽位成长说明忠实原文。

#### entry-02174
- **位置**：`mod-tome.lua:28206` / `mod-tome/data/talents/spells/aether.lua`（以太射线 `Aether Beam`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%0.2f`（奥术伤害）匹配；固定数值（25% 沉默、10% 中心伤害、1600% 旋转速度、3 次命中限制）转译完整无误。

#### entry-02175
- **位置**：`mod-tome.lua:28222` / `mod-tome/data/talents/spells/aether.lua`（以太化身惩罚日志）
- **判定**：未发现问题
- **可核验依据**：颜色标签 `#VIOLET#`、`#LAST#` 及实体占位符 `%s` 完好无损，法力扣除数值与原因说明准确。

#### entry-02176
- **位置**：`mod-tome.lua:28274` / `mod-tome/data/talents/spells/age-of-dusk.lua`（死灵黄金时代 `Golden Age of Necromancy`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（全豁免）、`%d%%`（混乱与传送抗性）匹配；5 级穿过 1 点生命线获得无敌 1 回合的描述与源码 `checkLifeThreshold(1, ...)` 一致。

#### entry-02177
- **位置**：`mod-tome.lua:28284` / `mod-tome/data/talents/spells/air.lua`（闪电术 `Lightning`）
- **判定**：未发现问题
- **可核验依据**：3 个 `%0.2f` 占位符完整匹配（伤害下限、伤害上限、平均伤害）；波浪号连接区间符号符合中文习惯。

#### entry-02178
- **位置**：`mod-tome.lua:28302` / `mod-tome/data/talents/spells/air.lua`（雷暴 `Thunderstorm`）
- **判定**：未发现问题
- **可核验依据**：占位符 `%d`（目标数）、`%0.2f`（伤害上限）、`%0.2f`（平均伤害）数量与顺序无误；常数 1.00 伤害下限及半径参数准确。

#### entry-02179
- **位置**：`mod-tome.lua:28312` / `mod-tome/data/talents/spells/animus.lua`（灵魂汲取 `Soul Leech`）
- **判定**：未发现问题
- **可核验依据**：4 组 `%s`（品级颜色）与 `%d`（偷取回合间隔）、末尾 `#WHITE#` 颜色闭合标签，以及最后的容量占位符 `%d` 均精确对齐源码 `tformat` 9 参数调用；排版缩进保持一致。

#### entry-02180
- **位置**：`mod-tome.lua:28332` / `mod-tome/data/talents/spells/animus.lua`（吞噬灵魂 `Consume Soul`）
- **判定**：未发现问题
- **可核验依据**：3 个 `%d` 占位符依次对应治疗量、法力获得量、生命值低于 1 时的法术强度增益，数值参数顺序正确。

#### entry-02181
- **位置**：`mod-tome.lua:28344` / `mod-tome/data/talents/spells/animus.lua`（收割 `Reaping`）
- **判定**：细微观察
- **可核验依据**：
  1. 原文第 4 行末尾为 `all your resistances are increased by %d.`（未带百分号）。
  2. 译文写为“你的全体伤害抗性增加 %d%%。”。
  3. 查阅源码 `animus.lua` 中的 `Reaping` 实现：`self:talentTemporaryValue(p, "resists", {all=t.getResists(self, t)})`，ToME 的抗性数值在系统内部确为百分比（例如 5% 至 10%），译者补充 `%%` 使得界面显示与游戏机制相符，但在字面上构成了对原文标点格式的微调（占位符仍接收单整数参数，不破坏格式化运行）。

#### entry-02182
- **位置**：`mod-tome.lua:28378` / `mod-tome/data/talents/spells/arcane.lua`（干扰护盾 `Disruption Shield`）
- **判定**：未发现问题
- **风控核验**：全文包含 7 个动态占位符（`%d`, `%0.2f`, `%d`, `%d`, `%d`, `%d`, `%d`），分别对应基础护盾值、法力/伤害吸收比、储能上限、风暴半径、法力有效上限、当前护盾值、当前储能；静态百分比 `20%%`, `10%%`, `50%%` 转义完整；逻辑翻译高度准确。

#### entry-02183
- **位置**：`mod-tome.lua:28402` / `mod-tome/data/talents/spells/conveyance.lua`（传送目标选择日志）
- **判定**：未发现问题
- **可核验依据**：`Select a target to teleport...` 对应“选择目标传送…”，省略号与语境一致。

#### entry-02184
- **位置**：`mod-tome.lua:28403` / `mod-tome/data/talents/spells/conveyance.lua`（法术失败日志）
- **判定**：未发现问题
- **可核验依据**：`The spell fizzles!` 准确翻译为“法术失败了！”，感叹号保留。

#### entry-02185
- **位置**：`mod-tome.lua:28404` / `mod-tome/data/talents/spells/conveyance.lua`（传送地点选择日志）
- **判定**：未发现问题
- **可核验依据**：`Select a teleport location...` 准确翻译为“选择传送位置…”。

#### entry-02186
- **位置**：`mod-tome.lua:28405` / `mod-tome/data/talents/spells/conveyance.lua`（相位之门失偏日志）
- **判定**：未发现问题
- **可核验依据**：`The targeted phase door fizzles and works randomly!` 准确译为“相位之门定位失败了，变为随机传送！”，技能名称与状态准确。

#### entry-02187
- **位置**：`mod-tome.lua:28406` / `mod-tome/data/talents/spells/conveyance.lua`（相位之门 `Phase Door` 描述）
- **判定**：细微观察
- **可核验依据**：
  1. 两个 `%d` 占位符（最大范围、等级 5 选择范围）位置正确。
  2. 译文第 2 行对 4 级效果补充了括号解释“（怪物或被护送者）”（原文为 `specify which creature to teleport`），属于为提示玩家用途的非原文增补。核心语义与占位符无问题。

---

### 复核总结

- **完成复核条数**：39 条（`entry-02149` 至 `entry-02187`）
- **存在疑点条目**：
  - `entry-02149`：`global speed` 被译为“所有速度”（规范要求为“全局速度”）；且计算逻辑存在细微减损并添加额外代码公式注释。
- **细微观察条目**：
  - `entry-02150`：数字与 `%` 间有多余空格；含有体质/意志代码增补说明。
  - `entry-02153`：豁免检定译为“鉴定”；含有属性底层公式增补说明。
  - `entry-02181`：原文漏写百分号，译文自行补全为 `%d%%`（与实际抗性机制吻合，但存在文本字面差异）。
  - `entry-02187`：译文增加“（怪物或被护送者）”的非原文说明。
- **未发现问题条目**：其余 34 条占位符、颜色码、格式转义及参数顺序均与固定版本源码严格一致。