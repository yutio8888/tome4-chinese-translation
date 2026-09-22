### 批次与冻结哈希核验

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核目标**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-075.md`（补跑截断的后 4 条：`entry-02425` ~ `entry-02428`）
- **文件 SHA-256**：`05d4a4b7207fc5fcb07c8283cfc3d35709929576cbe7d1f12217c34296e35a90`（已比对，完全一致）
- **公开源码基准**：t-engine4 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4)（只读查验 [`game/modules/tome/data/talents/techniques/techniques.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/techniques.lua)、[`game/modules/tome/class/Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua) 与 [`game/modules/tome/class/interface/Combat.lua`](file:///workspace/t-engine4/game/modules/tome/class/interface/Combat.lua)）

---

### 译文复核报告（4 条）

#### entry-02425
- **位置**：`mod-tome.lua:30968`
- **section**：`mod-tome/data/talents/techniques/techniques.lua`（talent type `technique/pugilism` 的 `description`）
- **source_tag**：`_t`
- **原文**：
  ```text
  Unarmed Boxing techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
  ```
- **译文**：
  ```text
  徒手拳击格斗技术，你不能装备板甲、武器和盾牌。
  ```
- **状态**：**存在疑点**
- **格式核查**：
  - 占位符：无。
  - 颜色码：无。
  - 换行与标点：单行文本，标点符合中文规范，无多余空格。
- **源码与语境核验依据**：
  1. **源码机制**：查验固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 中 [`game/modules/tome/data/talents/techniques/techniques.lua:86`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/techniques.lua#L86)，该系定义为 `newTalentType{ is_unarmed=true, ... }`。
  2. **限制触发逻辑**：查验 [`game/modules/tome/class/Actor.lua:5787-5795`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5787-L5795) 与 [`Actor.lua:4434`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4434)：
     - 当技能具有 `is_unarmed = true` 时，引擎在施展时检测 `self:hasMassiveArmor()`（`subtype == "massive"`）以及 `not self:isUnarmed()`（主副手装备了武器或盾牌）；若不满足，禁止施展（提示 `too heavily armoured` 或 `can't use this talent while holding a weapon or shield`），若处于持续激活状态则强制解除。
     - **机制事实**：游戏并未禁止玩家装备板甲、武器或盾牌（角色背包与装备栏完全允许装备），而是**在身穿板甲或手持武器/盾牌时，无法使用/施展该系技能**。
  3. **同 section 语境对比**：同文件中邻近的同类技能系 `mod-tome.lua:30974`（`technique/unarmed-discipline`）相同后半句处理为：`身穿板甲或装备武器、盾牌时无法施展。`（准确反映了施展前提）。
- **疑点分析**：
  译文将修饰从句 `that may not be practiced in massive armor or while a weapon or shield is equipped` 译为独立句「你不能装备板甲、武器和盾牌」，将技能的“施展限制”误传达为角色的“装备禁令”，容易让玩家误以为系统锁定了装备位。
- **调整建议（供裁决）**：
  建议对齐同 section 的准确表述，调整为例如：「徒手拳击格斗技术；身穿板甲或装备武器、盾牌时无法施展。」

---

#### entry-02426
- **位置**：`mod-tome.lua:30970`
- **section**：`mod-tome/data/talents/techniques/techniques.lua`（talent type `technique/finishing-moves` 的 `description`）
- **source_tag**：`_t`
- **原文**：
  ```text
  Finishing moves that use combo points and may not be practiced in massive armor or while a weapon or shield is equipped.
  ```
- **译文**：
  ```text
  使用你累积的连击点数发动致命的终结一击，你不能装备板甲、武器和盾牌。
  ```
- **状态**：**存在疑点**
- **格式核查**：
  - 占位符：无。
  - 颜色码：无。
  - 换行与标点：单行文本，标点规范。
- **源码与语境核验依据**：
  1. **源码机制**：查验 [`game/modules/tome/data/talents/techniques/techniques.lua:87`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/techniques.lua#L87)，该系为 `technique/finishing-moves`（终结技），包含上勾拳（Uppercut）、震荡拳（Concussive Punch）、摆拳（Haymaker）等招式，机制上由 `combo points`（连击点）驱动，且具有 `is_unarmed = true` 限制。
  2. **后半句逻辑**：与 `entry-02425` 完全相同，`that may not be practiced in massive armor or while a weapon or shield is equipped` 属于使用/施展限制而非不可装备物品。
  3. **前半句语义**：原文为系别概括名词短语 `Finishing moves that use combo points`（消耗/使用连击点数的终结技）。译文增添了原文无对应的「致命的」（lethal / deadly），且将系别的招式复数概念写成了单一执行动作「发动...终结一击」。
- **疑点分析**：
  1. 存在与 `entry-02425` 相同的机制误导，将「身穿板甲或装备武器、盾牌时无法施展」误译为装备禁令「你不能装备板甲、武器和盾牌」。
  2. 前半句存在轻度翻译腔与非原文信息的衍生修饰（「致命的」）。
- **调整建议（供裁决）**：
  建议调整为例如：「消耗连击点数的终结技；身穿板甲或装备武器、盾牌时无法施展。」

---

#### entry-02427
- **位置**：`mod-tome.lua:30972`
- **section**：`mod-tome/data/talents/techniques/techniques.lua`（talent type `technique/grappling` 的 `description`）
- **source_tag**：`_t`
- **原文**：
  ```text
  Grappling techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
  ```
- **译文**：
  ```text
  抓取敌人的技巧，你不能装备板甲、武器和盾牌。
  ```
- **状态**：**存在疑点**
- **格式核查**：
  - 占位符：无。
  - 颜色码：无。
  - 换行与标点：单行文本，标点无格式错误。
- **源码与语境核验依据**：
  1. **源码机制**：查验 [`game/modules/tome/data/talents/techniques/techniques.lua:88`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/techniques.lua#L88) 及 [`game/modules/tome/data/talents/techniques/grappling.lua`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/grappling.lua)，该系包含纠缠（Clinch）、重压固锁（Crushing Hold）、摔跌（Take Down）、飓风摔（Hurricane Throw）等招式。同文件 `mod-tome.lua:30971` 中系别名翻译为「关节技」。
  2. **施展限制**：同样受 [`Actor.lua:5787`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5787) 的 `is_unarmed` 约束，装备板甲或武器盾牌会导致相关技能无法使用。
- **疑点分析**：
  1. 后半句同样存在将技能施展限制写成角色装备禁令的问题（「你不能装备板甲、武器和盾牌」）。
  2. （细微观察）前半句 `Grappling techniques` 译为「抓取敌人的技巧」稍显直白和局限（格斗术中 grappling 通常为擒拿/缠斗/关节技），但若考虑通俗理解亦可接受；主要疑点仍在于后半句的施展限制机制描述。
- **调整建议（供裁决）**：
  建议调整为例如：「缠斗与擒拿技巧；身穿板甲或装备武器、盾牌时无法施展。」（或保留「抓取敌人的技巧；身穿板甲或装备武器、盾牌时无法施展。」）。

---

#### entry-02428
- **位置**：`mod-tome.lua:30976`
- **section**：`mod-tome/data/talents/techniques/techniques.lua`（talent type `technique/unarmed-training` 的 `description`）
- **source_tag**：`_t`
- **原文**：
  ```text
  Teaches various martial arts techniques that may not be practiced in massive armor or while a weapon or shield is equipped.
  ```
- **译文**：
  ```text
  高级徒手格斗技能，不能装备板甲、武器和盾牌。
  ```
- **状态**：**存在疑点**
- **格式核查**：
  - 占位符：无。
  - 颜色码：无。
  - 换行与标点：单行文本，标点无格式错误。
- **源码与语境核验依据**：
  1. **源码机制与系别属性**：
     查验 [`game/modules/tome/data/talents/techniques/techniques.lua:89-90`](file:///workspace/t-engine4/game/modules/tome/data/talents/techniques/techniques.lua#L89-L90)：
     ```lua
     newTalentType{ is_unarmed=true, allow_random=true, type="technique/unarmed-discipline", name = _t("unarmed discipline", "talent type"), description = _t"Advanced unarmed techniques including kicks and blocks that may not be practiced in massive armor or while a weapon or shield is equipped." }
     newTalentType{ is_unarmed=true, allow_random=true, generic = true, type="technique/unarmed-training", name = _t("unarmed training", "talent type"), description = _t"Teaches various martial arts techniques that may not be practiced in massive armor or while a weapon or shield is equipped." }
     ```
     - 本条对应的系别是 `technique/unarmed-training`（通用技能系 `generic = true`，同文件 `mod-tome.lua:30975` 译名「徒手训练」），包含空手入白刃（Empty Hand）、徒手精通（Unarmed Mastery）等基础被动与通用技巧。
     - 而前一个职业系 `technique/unarmed-discipline`（`mod-tome.lua:30973` 译名「徒手格斗」）原文才是 `Advanced unarmed techniques...`（高级徒手格斗技巧）。
  2. **严重语意错位与漏译**：
     - 原文前半句为 `Teaches various martial arts techniques`（传授各种武术技巧 / 传授多种格斗技巧）。
     - 译文却写成了「高级徒手格斗技能」：明显是将前一条 `unarmed-discipline` 的「Advanced」（高级）误复制/串行代入了本条基础通用技能系中，且把主谓动词 `Teaches`（传授/学习）完全遗漏。
  3. **施展限制误译**：
     - 后半句同样误译为「不能装备板甲、武器和盾牌」，未准确表达技能施展前提。
- **疑点分析**：
  本条存在实质性的语义串行错位与漏译（将基础通用的「传授各种武术技巧」错误翻成「高级徒手格斗技能」），且同样继承了后半句关于装备/施展限制的机制表述缺陷。
- **调整建议（供裁决）**：
  建议调整为例如：「传授各种徒手武术技巧；身穿板甲或装备武器、盾牌时无法施展。」

---

### 复核总结汇总表

| 条目编号 | 位置 | 原文关键句 / 类别 | 状态 | 核心核验事实与疑点摘要 |
| :--- | :--- | :--- | :---: | :--- |
| **entry-02425** | `mod-tome.lua:30968` | `Unarmed Boxing techniques...` (`technique/pugilism`) | **存在疑点** | 源码 `Actor.lua:5787` 证实板甲与武器盾牌为技能施展限制，而非装备栏禁用。「你不能装备...」扭曲了机制；建议对齐同 section 的「身穿板甲或装备武器、盾牌时无法施展」。 |
| **entry-02426** | `mod-tome.lua:30970` | `Finishing moves that use combo points...` (`technique/finishing-moves`) | **存在疑点** | 后半句存在相同的施展限制误译（「你不能装备...」）；前半句名词短语添加了原文未有的「致命的」，并把系别招式复数改写为单一动作。 |
| **entry-02427** | `mod-tome.lua:30972` | `Grappling techniques...` (`technique/grappling`) | **存在疑点** | 后半句同样存在施展限制误译为装备禁令的问题；前半句「抓取敌人的技巧」偏窄（建议「缠斗与擒拿技巧」）。 |
| **entry-02428** | `mod-tome.lua:30976` | `Teaches various martial arts techniques...` (`technique/unarmed-training`) | **存在疑点** | 实质性错位与漏译：原文为通用系「传授各种武术技巧」，译文误套用邻近条目的「Advanced」翻成「高级徒手格斗技能」并漏译 `Teaches`；后半句同样存在装备禁令误译。 |