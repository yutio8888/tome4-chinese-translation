### 审核报告：rem-17 批次（20 条冻结译文）

**审核配置与授权模式**：
- 依据用户授权自然语言审核旁路与 `RULES.md` 规范，执行只读初审（Gemini 3.8 Flash）与疑点交叉核验（GPT 6 Sol）。
- 来源与版本限制声明：本批次涉及 DLC `orcs`（Embers of Rage）条目。DLC 源码依据 `source-access.json` 中哈希固定（`tome-orcs/data/timed_effects/physical.lua` SHA256: `d3332099148953cd03cb1d14c2bdd2390e091905144fd49311d9bd8c33b6e37e`），其源码仓库 commit 及 1.7.4 目标版本未固定，本报告仅以该已核准的公开冻结快照为机制核实证据，不宣称已核 1.7.4 最终发行态。
- 遵循只读契约：未写入任何文件，未创建任何子代理，未读取其他历史报告或任务状态文件。

---

### 一、逐条审核结论汇总表

| 序号 | 完整 Entry-ID | 终审判定 | 初审 (Gemini) / 复审 (Sol) 意见 | 依据摘要 / 疑点编号 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `entry-04034` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | 状态解除日志“不再烧焦”准确对应 `on_lose` 与效果名 `Seared`，机制与占位符无误。 |
| 2 | `entry-04035` | 存在问题 | 初审：存在问题<br>复审：存在问题 | 漏译修饰副词 `somehow` 与分词定语 `falling`，详见 **C01**。 |
| 3 | `entry-04037` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Marked for Death` 触发日志，主客体与标点准确。 |
| 4 | `entry-04038` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Itching Powder` 获得日志，感官状态传达准确。 |
| 5 | `entry-04040` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Smoke Cover` 获得日志，语意与占位符无误。 |
| 6 | `entry-04041` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Smoke Cover` 解除日志，句式通顺准确。 |
| 7 | `entry-04043` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | 磁化效果解除日志；术语库中 `magnetism` 限于技能类别（talent type），此处 timed effect 语境用“磁化”正确。 |
| 8 | `entry-04044` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Bloodstar` 获得日志，“血液灵晶”专名一致，动作准确。 |
| 9 | `entry-04045` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Bloodstar` 解除日志，表达通顺一致。 |
| 10 | `entry-04046` | 仅建议 | 初审：仅建议<br>复审：仅建议 | “忍受痛苦”偏主动耐受，建议调整为“遭受痛苦”；详见 **C02**。 |
| 11 | `entry-04047` | 仅建议 | 初审：仅建议<br>复审：仅建议 | 漏译描绘性修饰词 `crackling`（噼啪作响的）；详见 **C03**。 |
| 12 | `entry-04048` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | 驱散负面效果日志，颜色标记 `#ORCHID#...#LAST#` 及占位符完整。 |
| 13 | `entry-04049` | 仅建议 | 初审：仅建议<br>复审：仅建议 | `surges with power` 译为“力量强化”略偏静态，建议润色；详见 **C04**。 |
| 14 | `entry-04050` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `AED` 准备日志，主语占位符与术语一致。 |
| 15 | `entry-04051` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `AED` 触发日志，占位符与主谓结构无误。 |
| 16 | `entry-04052` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | `Pincer Strike` 抓取日志，主客体与专用动词“钳制”恰当。 |
| 17 | `entry-04053` | 仅建议 | 初审：仅建议<br>复审：仅建议 | 简化了方向性动词短语 `strikes down at`，建议润色；详见 **C05**。 |
| 18 | `entry-04054` | 未发现问题 | 初审：未发现问题<br>复审：未发现问题 | 4 个格式化占位符（`%d`, `%d%%`, `%d%%`, `%0.2f`）顺序与数值一一对应，机制表达完整。 |
| 19 | `entry-04055` | 仅建议 | 初审：仅建议<br>复审：仅建议 | 译文增译了代码底层的内置冷却与武器触发条件，属有意机制补全，与上一条存在详略不对称；详见 **C06**。 |
| 20 | `entry-04056` | 仅建议 | 初审：仅建议<br>复审：仅建议 | 原英文“launching...each turn”与实际机制脱节，译文纠正为实际的主动打断机制，作机制更正备案；详见 **C07**。 |

---

### 二、疑点与建议详细分析（Claims C01 ~ C07）

#### C01: entry-04035 叙事修饰语漏译
- **完整 Entry-ID**：`entry-04035`
- **原译短引**：
  - 原文：`#Target# somehow catches the falling steamguns.`
  - 译文：`#Target# 接住了蒸汽枪。`
- **具体意义差异**：
  漏译副词 `somehow`（不知怎么地 / 奇迹般地）与分词定语 `falling`（从空中落下的 / 下落的）。该效果承接前置状态获得文本 `#Target# tosses steamguns in the air, awesome!`（将蒸汽枪抛向空中任其射击），效果结束时角色“不知怎么地设法接住了空中落下的蒸汽枪”，原文具有明确的滑稽戏谑色彩。译文平铺直叙丢弃了动作态势与幽默叙事。
- **最强等价读法与处理**：
  - *等价读法*：作为战斗日志，主干信息为接住武器解除缴械，玩家可理解状态结束。
  - *处理意见*：依据 `RULES.md` 第 1 条“明确叙事偏差也不能只因不影响机制而忽略”，此属于二级叙事完整性偏差，判定为 **存在问题 (confirmed)**。
  - *建议修改*：`#Target# 不知怎么接住了落下的蒸汽枪。` 或 `#Target# 奇迹般地接住了落下的蒸汽枪。`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:598`
- **缺失证据**：无。

---

#### C02: entry-04046 动词语义与欧化表达
- **完整 Entry-ID**：`entry-04046`
- **原译短引**：
  - 原文：`#Target# is suffering and fails to concentrate on dealing damage.`
  - 译文：`#Target# 忍受痛苦，不能集中精力制造伤害。`
- **具体意义差异**：
  1. `is suffering` 译为“忍受痛苦”带有主动对抗/耐受的意味（bear/endure），而此处切臂致残（`TO_THE_ARMS`）是被负面效果折磨的消极状态（遭受痛苦 / 痛苦不堪），且对应解除文本为“痛苦减轻了”。
  2. `dealing damage` 译为“制造伤害”略显欧化生硬，中文常规游戏用语通常为“造成伤害”。
- **最强等价读法与处理**：
  - *等价读法*：玩家依然能清晰理解由于身体遭受痛苦导致伤害输出下降的机制因果。
  - *处理意见*：机制表达无误，判定为 **仅建议 (advisory)**。
  - *建议修改*：`#Target# 遭受痛苦，无法集中精力造成伤害。`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:870`
- **缺失证据**：无。

---

#### C03: entry-04047 氛围修饰词漏译
- **完整 Entry-ID**：`entry-04047`
- **原译短引**：
  - 原文：`The target is surrounded by a crackling web of lightning, reducing all damage taken by %d.`
  - 译文：`目标被闪电之网覆盖，减少所受到的所有伤害 %d。`
- **具体意义差异**：
  原文 `a crackling web of lightning` 中的拟声感官修饰词 `crackling`（噼啪作响的 / 噼啪闪烁的）未译出；`surrounded by` 译为“覆盖”（更贴切者为“环绕 / 包围”）。
- **最强等价读法与处理**：
  - *等价读法*：占位符 `%d` 与固定减伤机制（`absorb = math.min(eff.power, cb.value)`）完全传达，“覆盖”符合力场护盾意象。
  - *处理意见*：判定为 **仅建议 (advisory)**。
  - *建议修改*：`目标被一张噼啪作响的闪电之网环绕，减少所受到的所有伤害 %d。`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:955`
- **缺失证据**：无。

---

#### C04: entry-04049 动词动态感扁平化
- **完整 Entry-ID**：`entry-04049`
- **原译短引**：
  - 原文：`#target# surges with power!`
  - 译文：`#target#力量强化！`
- **具体意义差异**：
  `surges with power` 具有强烈的能量喷薄、涌动感，译为“力量强化！”略显静态概括，未能充分体现超频充能时的动态特效。
- **最强等价读法与处理**：
  - *等价读法*：与解除效果时的 `#target# looks less powerful.`（译为“力量消退了”）形成了良好的对称对应，状态提示明确。
  - *处理意见*：判定为 **仅建议 (advisory)**。
  - *建议修改*：`#target# 力量奔涌！` 或 `#target# 力量涌动！`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1037`
- **缺失证据**：无。

---

#### C05: entry-04053 方向性打击细节简化
- **完整 Entry-ID**：`entry-04053`
- **原译短引**：
  - 原文：`#Source# #LIGHT_RED#strikes down at#LAST# #Target#!`
  - 译文：`#Source# #LIGHT_RED#打击#LAST# #Target#！`
- **具体意义差异**：
  `strikes down at` 原文具象描述了机械蜘蛛用钳爪抓住目标后、尾部链锯从上方朝下猛刺的动作。译文简化为通用“打击”。
- **最强等价读法与处理**：
  - *等价读法*：彩色高亮格式标签 `#Source# #LIGHT_RED#...#LAST# #Target#!` 结构完整，战斗日志常用动词“打击”完全符合游戏惯例。
  - *处理意见*：判定为 **仅建议 (advisory)**。
  - *建议修改*：`#Source# #LIGHT_RED#向下猛击#LAST# #Target#！`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1315`
- **缺失证据**：无。

---

#### C06: entry-04055 机制性超译补全与批内不对称
- **完整 Entry-ID**：`entry-04055`
- **原译短引**：
  - 原文：`Affected by toxic chemicals. Has %d%% talent failure, %d%% reduced healing, and takes %0.2f additional acid damage from melee and ranged attacks.`
  - 译文：`被有毒化学物质影响。%d%% 技能失败率，降低 %d%% 治疗效果，每回合第一次被带有武器类型的近战或远程攻击命中时，受到额外 %0.2f 酸性伤害。`
- **具体意义差异**：
  译文超出英文表面字面，增译了 `每回合第一次被带有武器类型的...命中时`。核查源码 `callbackOnHit`：
  ```lua
  if not src or not src.turn_procs or not src.turn_procs.weapon_type or self.turn_procs.miasma then return end
  self.turn_procs.miasma = true
  ```
  底层代码确实存在 `self.turn_procs.miasma`（限制每回合生效 1 次）以及 `weapon_type`（限制武器类攻击）。译文增译内容与源码机制事实 100% 吻合，但与同一技能的光环描述 `entry-04054`（未增译上述限定）在文字详略上存在不对称。
- **最强等价读法与处理**：
  - *等价读法*：这是汉化组为解决英文原版描述模糊、帮助玩家理解实际战斗机制的有意补全，非机制理解偏差。
  - *处理意见*：判定为 **仅建议 (advisory)**。确认机制事实无误，无需回退为模糊的直译；记录其与 entry-04054 的表达风格差异。
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1463, 1483`
- **缺失证据**：无。

---

#### C07: entry-04056 英文描述缺陷的机制纠正备案
- **完整 Entry-ID**：`entry-04056`
- **原译短引**：
  - 原文：`Hovering in place, gaining %d%% evasion, %d%% movement speed and launching a powerful rocket barrage each turn.`
  - 译文：`目标悬浮在空中，获得 %d%% 躲闪概率，%d%% 移动速度；可手动使用火箭弹幕再次发射，使用其他任何技能会立即结束该效果。`
- **具体意义差异**：
  原英文文本存在严重误导：声称该状态“每回合发射强力火箭弹幕”（launching...each turn）。但审查底层实现：
  1. `activate` 函数仅为玩家添加主动技能 `T_ROCKET_BARRAGE`；不存在任何每回合自动发射弹幕的定时器。
  2. `callbackOnTalentPost` 明确规定：如果使用的技能不是 `rocket_barrage`，立即移除飞行效果（`self:removeEffect(self.EFF_DEATH_FROM_ABOVE)`）。
  译者并未盲从有缺陷的英文表面描述，而是依据源码与对应主动技能（`artillery.lua`）机制，将后半句重写为真实机制说明。两处占位符 `%d%%`（闪避率）与 `%d%%`（移速加成）位置与顺序完全对齐。
- **最强等价读法与处理**：
  - *等价读法*：依据 `RULES.md` 第 2 条（“译文忠实沿袭英文的机制问题单列，不算中文新增错误”）与校对依据第 1 条（机制以实际代码行为为准），译文有效修正了原版英文的虚假机制描述，保护了玩家体验。
  - *处理意见*：判定为 **仅建议 (advisory)** / 机制修正备案。不判为错译。
- **来源路径行号**：
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:1496, 1505-1510`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/artillery.lua:180-210`
- **缺失证据**：无。

---

### 三、实际读取路径与版本限制说明

1. **实际读取的文件列表**：
   - 审核入口：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-17.md`
   - 规则与配置文件：
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
   - 译文快照上下文：
     - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`（第 6430 ~ 6585 行）
   - 公开冻结源码：
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua`（SHA256: `d3332099148953cd03cb1d14c2bdd2390e091905144fd49311d9bd8c33b6e37e`）
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/artillery.lua`（仅只读调用链查询）

2. **限制与环境说明**：
   - 本批次所有条目均来自 DLC `orcs`。依据仓库基线规则，DLC 源码由快照哈希锁定，来源未固定 commit，亦不代表 1.7.4 最终代码状态。机制审核基于当前已冻结的源码事实。
   - 本次审查为有界只读旁路，无写入操作，不派生子任务。全部 20 个条目均已完成审查并归入台账。
