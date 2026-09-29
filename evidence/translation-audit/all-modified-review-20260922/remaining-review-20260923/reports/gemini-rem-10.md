# rem-10 批次译文审核报告（Gemini 全量初审阶段）

**审核阶段与身份声明**：本报告由只读 REVIEWER（Gemini 3.8 Flash）执行第一阶段全量初审。本阶段仅完成 Gemini 侧的独立审查与疑点提取，严格遵守单阶段执行纪律，**不替后续 GPT 6 Sol 声称复核已完成**，不宣称正式 contract `DONE_VERIFIED`。

---

## 一、逐条审核判定表（按输入顺序）

| 条目编号 | 判定状态 | Claim 编号 / 判定依据 |
| :--- | :--- | :--- |
| **entry-04116** | **存在问题** | **C01**：专名/实体错译。"Doomed Shade" 对应暗影地穴克隆体 Boss，"Doomed" 误译为"被诅咒的"（Cursed），应为"末日阴影"。 |
| **entry-04117** | **未发现问题** | 语法与逻辑完全等价。原句为 A 或 B 双向互杀成就，译文双向均完整表达，人名专名准确无误。 |
| **entry-04118** | **未发现问题** | 人名、头衔及主谓宾结构准确，术语符合 `terms.json` 规范。 |
| **entry-04122** | **未发现问题** | 占位符 `%d%%`、`%d`、`%0.2f`、`%d` 顺序与数量一致，技能机制描述准确，符合原文。 |
| **entry-04123** | **未发现问题** | 占位符与数值准确，盾牌/格挡力场减伤机制及反击触发条件完整无误。 |
| **entry-04124** | **未发现问题** | 样式标记 `#{italic}#`、`#{normal}#` 及占位符 `%d` 均完整保留，语义通顺准确。 |
| **entry-04125** | **未发现问题** | 占位符 `%s` 保留，术语"灵能仆从"与技能名称完全一致。 |
| **entry-04129** | **存在问题** | **C02**：严重机制漏译。漏译关键贯穿机制从句 `"and all those in straight line behind it"`，将群体贯穿冲锋误写为单体冲锋。 |
| **entry-04130** | **未发现问题** | 玩家日志文本，状态检查提示准确，与同文件其他"占据躯体"译法一致。 |
| **entry-04131** | **未发现问题** | 颜色代码 `#CRIMSON#` 与斜体标记完整，叙事感与文学风格契合。 |
| **entry-04132** | **未发现问题** | 动态阶级格式占位符 `%s%s#LAST#` 完整无损，阶级判定语义准确。 |
| **entry-04134** | **未发现问题** | 占位符 `%d%%` 保留，属性项（闪避、暴击、强度、豁免）翻译准确。 |
| **entry-04135** | **未发现问题** | 占位符 `%d%%`、`%0.1f` 正确无误，附身属性继承与技能等级上限机制完整。 |
| **entry-04136** | **未发现问题** | 6 个技能等级条目翻译完整规范，"固定减伤"准确表达 "flat resistances" 机制。 |
| **entry-04137** | **仅建议** | **C03**：叙事风格与意象偏移。"send a psionic impulse to tell it to simply die" 被简化为"射出一道冲击波"，建议还原灵能意象。 |
| **entry-04139** | **未发现问题** | 范围攻击与克隆体延时机制准确，占位符 `%d`、`%d%%`、`%d` 对应无误。 |
| **entry-04140** | **未发现问题** | 触发阈值 80%、虐待狂层数及原始精神强度增益机制表达清晰准确。 |
| **entry-04141** | **存在问题** | **C04**：主客体与动作语义偏差。"radiate agony" 误译为"将自己的痛苦分享给"，无中生有增译"自己的"，并与次句"专注于他们自己的痛苦"产生混淆。 |
| **entry-04143** | **未发现问题** | 状态效果描述简短准确，占位符 `%d` 与术语"精神强度（原始值）"匹配。 |

---

## 二、疑点详细报告（Claims）

### Claim C01
- **条目编号**：`entry-04116`
- **原译短引**：
  - 原文：`Kill your own Doomed Shade in the body of Bill.`
  - 译文：`使用比尔的身体杀死你自己的被诅咒的影子。`
- **具体意义差异**：
  1. 实体与职业名严重混淆。在 ToME4 苦痛系（Afflicted）中，存在两个平行职业：`Cursed`（诅咒者）与 `Doomed`（末日使者，见 `terms.json`）。
  2. 原文 "Doomed Shade" 指代的是暗影地穴（Shadow Crypt）中生成的玩家克隆体 Boss（本体源码 `game/modules/tome/data/zones/shadow-crypt/npcs.lua:92` 明确定义非食灵族玩家克隆体为 `("Doomed Shade of %s"):format(plr.name)`，且具有末日使者技能树）。
  3. 原译将 "Doomed" 误译为"被诅咒的"（对应 Cursed），导致玩家误以为成就要去寻找诅咒相关的影子，混淆了游戏核心职业实体名称。
- **最强等价读法与处理**：
  若仅从自然语言词典来看，"doomed" 包含"注定遭劫/在劫难逃"的语境，译者可能望文生义选用了"被诅咒的"。但在 ToME4 语境中，"Doomed" 具有唯一专名对应（末日使者）。建议修正为"末日阴影"或"末日使者之影"，例如：`附身比尔的身体杀死你自己的末日阴影。`
- **判定状态**：`存在问题` (confirmed)
- **来源路径与行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:5`
  - 关联本体机制源码：`/workspace/t-engine4/game/modules/tome/data/zones/shadow-crypt/npcs.lua:92`
  - 术语参照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json` (Doomed -> 末日使者)
- **缺失证据**：Possessors DLC 成就注册源码未独立定位，但不影响本体 `shadow-crypt/npcs.lua` 中固定实体命名的确证性。

---

### Claim C02
- **条目编号**：`entry-04129`
- **原译短引**：
  - 原文：`For a brief moment your whole body becomes etheral and you dash into a nearby creature and all those in straight line behind it (in range %d).\n\t\tYou reappear on the other side, with %d more psi and having dealt %0.2f mind damage to your targets.`
  - 译文：`短暂的一瞬间，你的整个身体变得飘渺，你对附近一个生物进行一次直线冲锋 (范围 %d)。\n\t\t你再次出现在另一边，获得 %d 灵能值并对目标造成 %0.2f 精神伤害。`
- **具体意义差异**：
  关键机制文本严重漏译。原文明确说明该冲锋为贯穿直线上的所有目标：`"dash into a nearby creature and all those in straight line behind it (in range %d)"`，因此后句造成的精神伤害承受者也是复数目标 `"your targets"`。原译完全删漏了 `"and all those in straight line behind it"`，翻译成"对附近一个生物进行一次直线冲锋"，将穿透型群体 AoE 冲锋描述成了单体冲锋，丢失了核心机制描述。
- **最强等价读法与处理**：
  原译漏译事实明确，不存在合理等价读法。必须补译该从句。建议修正为：`短暂的一瞬间，你的整个身体变得飘渺，你冲向附近一个生物以及其后方一条直线上的所有目标 (范围 %d)。\n\t\t你再次出现在另一边，获得 %d 灵能值并对这些目标造成 %0.2f 精神伤害。`
- **判定状态**：`存在问题` (confirmed)
- **来源路径与行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:119-122`
- **缺失证据**：无（快照文本自身直接可证）。

---

### Claim C03
- **条目编号**：`entry-04137`
- **原译短引**：
  - 原文：`You point your ghastly finger at a foe affected by Ghastly Wail and send a psionic impulse to tell it to simply die.`
  - 译文：`用手指对受到恐怖嚎叫效果影响的敌人射出一道冲击波。`
- **具体意义差异**：
  叙事意象与原作者风格偏移。
  1. 该技能为 "Finger of Death"（死亡一指）。原文叙述为 `"point your ghastly finger... and send a psionic impulse to tell it to simply die"`（伸出你阴森的手指指向目标……并发送一道灵能脉冲命令其直接受死）。
  2. 原译略去了与前置技能 Ghastly Wail（恐怖嚎叫）同词根的形容词 `"ghastly"`（可怕的/阴森的），并将 `"send a psionic impulse to tell it to simply die"` 简化翻译为 `"射出一道冲击波"`，丢失了死亡一指标志性的精神下令致死风味。
- **最强等价读法与处理**：
  原译后文关于已损失生命值百分比伤害、Boss 上限、身体吸收及武器切换等机制均准确表达。将该句概括为"射出一道冲击波"不影响玩家理解其机制判定。但依 RULES.md 规定"明确叙事偏差也不能只因不影响机制而忽略"，建议后续润色时更贴合原文本意。
- **判定状态**：`仅建议` (advisory)
- **来源路径与行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:270`
- **缺失证据**：无。

---

### Claim C04
- **条目编号**：`entry-04141`
- **原译短引**：
  - 原文：`As long as you have at least a stack of Sadist you can radiate agony to all those you see in radius %d with 80%% or lower life left.\n\t\tFor 5 turns their mind will be so focused on their own pain that they will deal %d%% less damage to you.`
  - 译文：`当你至少有一层虐待狂效果时，你可以将自己的痛苦分享给半径 %d 内所有可见的、生命值 80%% 或更低的敌人。\n\t\t持续 5 回合，他们的头脑将如此专注于自己的痛苦，对你的伤害减少 %d%%。`
- **具体意义差异**：
  主客体痛苦归属与动作性质错位。
  1. 技能所属技能树为 "ravenous-mind"（极度饥渴），前置核心被动为 "Sadist"（虐待狂：玩家从敌人的痛苦中吸取养分强化精神）。技能名为 "Radiate Agony"（痛苦辐射），动作是向残血敌人精神中辐射/散播剧痛。
  2. 译文增译了 `"自己的"`，并将 `"radiate agony"` 意译为 `"分享自己的痛苦"`。这不仅将主动侵略性的灵能折磨动作变成了温和甚至带有救赎感的"分享自身痛苦"，而且使第一句的"自己的痛苦"（被理解为主播/玩家的痛苦）与第二句的 `"their own pain"`（"他们自己的痛苦"，即敌人自身的伤痛）发生严重指代冲突。
- **最强等价读法与处理**：
  若将"分享痛苦"勉强视为某种反语修辞尚能强行读通，但原文无 "my/own"，且与次句敌人专注于自身痛苦产生语义逻辑矛盾。建议将"将自己的痛苦分享给"修正为"向……辐射痛苦"，例如：`你可以向半径 %d 内所有可见且生命值不高于 80%% 的敌人辐射痛苦。`
- **判定状态**：`存在问题` (confirmed)
- **来源路径与行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua:356-358`
- **缺失证据**：无。

---

## 三、汇总统计

- **本批总条目数**：19 条（`entry-04116` 至 `entry-04143`）
- **未发现问题**：15 条
- **存在问题 (confirmed)**：3 条（`entry-04116`、`entry-04129`、`entry-04141`）
- **仅建议 (advisory)**：1 条（`entry-04137`）
- **待确认 (pending)**：0 条

---

## 四、实际读取路径与来源版本限制

1. **实际读取文件清单**：
   - 任务入口批次文件：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-10.md`
   - 审核规则：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - 源码访问登记：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - 术语库冻结快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
   - 译文条目快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-possessors.lua`
   - 关联本体固定源码：`/workspace/t-engine4/game/modules/tome/data/zones/shadow-crypt/npcs.lua`（commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
2. **版本与来源限制说明**：
   - **Possessors DLC 源码缺失**：Possessors 组件在 `source-access.json` 中未登记独立公开源码仓库或冻结目录，本批审核严格遵循用户授权约束，**只做许可文本核验，不以其他组件代替**。
   - **本体源码引用边界**：仅当 `entry-04116` 涉及本体既有实体专名（暗影地穴 `Doomed Shade`）时，借助版本清单中固定的 engine commit 进行实体定义交叉核实；其余条目均基于冻结快照英汉文本对比完成纯文本证据闭环，未宣称已核对未固定的 DLC 1.7.4 源码。
