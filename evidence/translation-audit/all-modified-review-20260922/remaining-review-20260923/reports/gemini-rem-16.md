# 译文审查报告：rem-16 批次（20条）

- **任务性质**：只读 REVIEWER 自然语言审查旁路（用户授权）
- **审核入口**：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-16.md`
- **来源与版本限制**：
  - Engine 固定 Commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（读取 `Combat.lua` 与 `Game.lua` 调用链）
  - DLC `orcs` 源码：基于 `source-access.json` 登记快照核验，`other.lua`（SHA256: `78dd56833a...`）、`physical.lua`（SHA256: `d333209914...`）；DLC 仓库 commit 与 1.7.4 目标版本未全局固定，本报告仅对公开冻结源码及快照一致性负责，不宣称已核验 1.7.4 最终发版行为。

---

## 一、逐条审核判定表

| entry-ID | 判定状态 | claim 编号 / 依据简述 |
| :--- | :--- | :--- |
| entry-04012 | 未发现问题 | 词义准确，叹号保留完整 |
| entry-04014 | 仅建议 | C01（被动句式微含翻译腔，建议优化表述） |
| entry-04015 | 仅建议 | C02（译文补充说明了代码中生命回满解除的机制，占位符对应无误） |
| entry-04016 | 未发现问题 | 放电柱术语对齐，换行符与冒号结构完好 |
| entry-04017 | 未发现问题 | “超速”与前序技能“超速子弹”及状态名统一，数值占位符完好 |
| entry-04018 | 仅建议 | C03（省略触发时机状语 When striking，虽不影响理解仍建议补全） |
| entry-04019 | 存在问题 | C04（遗漏“命中目标时发生爆炸”核心触发与中心判定点，存在歧义） |
| entry-04020 | 未发现问题 | 专名药剂与标签 `#Target#` 正确，时态自然 |
| entry-04021 | 未发现问题 | 伤害亲和术语一致，占位符及数值格式完好 |
| entry-04022 | 仅建议 | C05（上游源码复制粘贴笔误，译文主动修正为“烈火光环”，属合理修正） |
| entry-04023 | 仅建议 | C06（上游源码复制粘贴笔误，译文主动修正为“静水光环”，属合理修正） |
| entry-04024 | 未发现问题 | 术语对齐，末尾空格属静态格式，依规不计缺陷 |
| entry-04025 | 未发现问题 | 动态拼接子串与宿主句契合良好，浮点格式符无误 |
| entry-04026 | 未发现问题 | 颜色高亮标签闭合正确，实体名规范 |
| entry-04027 | 未发现问题 | 动态拼接参数顺序与空格/标点组合完备，主被动自然 |
| entry-04028 | 仅建议 | C07（“主人的方向”略显拟人化修辞，建议优化为“施加者”） |
| entry-04029 | 未发现问题 | 源码确认 `#Source#` 即为受害者主体，无主客体颠倒 |
| entry-04030 | 未发现问题 | 充能层数/叠加次数简明 UI 化表达，占位符完好 |
| entry-04032 | 未发现问题 | 状态解除日志清晰准确，动态标签保留 |
| entry-04033 | 未发现问题 | 状态施加短句自然生动，动态标签保留 |

---

## 二、疑点与建议清单（Claims）

### C01: entry-04014 被动式翻译腔
- **完整 entry-ID**：entry-04014
- **原译短引**：
  - 原文：`The target has been injected with chemicals, reducing all saves by %d.`
  - 译文：`目标被化学药剂注射，降低所有豁免 %d。`
- **具体意义差异**：“被化学药剂注射”语序稍显生硬，属于典型的英式被动句式直译；逻辑上是被施加者注入化学药剂，而非化学药剂作为施动者进行注射。
- **最强等价读法与处理**：当前译文无机制歧义，属于二级风格与语感范畴。建议优化为：“目标被注射了化学药剂，降低所有豁免 %d。”
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua:521`
- **缺失证据**：无

---

### C02: entry-04015 译文补充机制事实（提前说明回满解除）
- **完整 entry-ID**：entry-04015
- **原译短引**：
  - 原文：`Engaged in automated repairs, preventing any action but increasing life regen by %d, all resistances by %d%% and preventing death until falling below -%d life.`
  - 译文：`进入自动修复模式，无法行动，但生命恢复速率增加 %d，生命值回满时立即结束该模式，全部抗性提升 %d%%，死亡生命下限为 -%d。`
- **具体意义差异**：原文字面并无“生命值回满时立即结束该模式”这一分句。
- **源码核验与机制依据**：核验 `other.lua:538-556` 可知，该效果参数包含 `decrease = 0`（即持续时间不随回合递减），且在 `on_timeout` 函数中明确定义 `if self.life == self.max_life then self:removeEffect(self.EFF_AUTOMATED_REPAIR_SYSTEM) end`。译者系主动将底层代码中的退出机制告知玩家。此外，译文占位符顺序依次为生命回复（`eff.heal`）、抗性（`eff.resist`）、死亡下限（`eff.life`），与格式化参数严格一一对应，未破坏数据槽位。
- **最强等价读法与处理**：此补充完全符合游戏实际代码运行机制。若追求字面严格忠实原文，可移除该分句；在游戏本地化实践中属于有益的机制阐释，列为提示性建议。
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua:541, 554-556`
- **缺失证据**：无

---

### C03: entry-04018 触发条件状语省略
- **完整 entry-ID**：entry-04018
- **原译短引**：
  - 原文：`Bullets shot are percussive:  When striking, they have a %d%% chance to knock back and a %d%% chance to stun.`
  - 译文：`子弹处于冲击状态：%d%% 概率击退，%d%% 概率震慑。`
- **具体意义差异**：译文省略了原句的触发条件短语 `When striking`（命中时 / 击中时）。
- **最强等价读法与处理**：由于子弹具有击退和震慑概率天然可由玩家常识推断为“命中目标时触发”，省略后未造成严重机制曲解；但对照英文原句存在完整性轻微缺失。建议优化补全：“子弹处于冲击状态：击中时有 %d%% 概率击退，%d%% 概率震慑。”
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:98`
- **缺失证据**：无

---

### C04: entry-04019 漏译命中爆炸触发机制与判定中心
- **完整 entry-ID**：entry-04019
- **原译短引**：
  - 原文：`Bullets shot are combustive:  When striking their target, they explode (radius 2) for %d fire damage.`
  - 译文：`子弹处于爆炸状态：对 2 码范围内的敌人造成 %d 火焰伤害。`
- **具体意义差异**：严重遗漏了关键时机与中心判定描述 `When striking their target, they explode`（命中目标时，发生爆炸）。现译文“对 2 码范围内的敌人造成 %d 火焰伤害”缺失了触发前提“命中目标时”，且未指明爆炸中心是“被命中的目标”，极易让玩家误读为以射手自身为中心散发火焰伤害，或子弹飞行沿途 2 码范围均受伤害。
- **源码核验与机制依据**：核验 `tome-orcs/superload/mod/class/interface/Archery.lua:85-88`，在 `Combat:archeryHit` 挂钩中，当触发 `combustive` 效果时，是以被击中者的坐标（`x=data.target.x, y=data.target.y`）为中心生成一个半径 2（`radius=2`）的范围爆炸火球投影。原文字面“命中目标时爆炸”是界定该伤害触发点与范围的核心要素。
- **最强等价读法与处理**：确认存在完整性与歧义缺陷。建议修正为：“子弹处于爆炸状态：命中目标时会发生爆炸（半径 2），对范围内的敌人造成 %d 火焰伤害。”
- **明确 status**：`存在问题`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:108` 及 `tome-orcs/superload/mod/class/interface/Archery.lua:85-88`
- **缺失证据**：无

---

### C05: entry-04022 上游源码文案笔误，译文主动修正
- **完整 entry-ID**：entry-04022
- **原译短引**：
  - 原文：`Provides a frost aura, giving you +%d%% fire, light, and lightning affinity.`
  - 译文：`提供烈火光环，使你获得 +%d%% 火焰、光系和闪电伤害亲和。`
- **具体意义差异**：原文字面为 `frost aura`（寒霜光环），译文译作“烈火光环”，表面看存在词义偏差。
- **源码核验与机制依据**：源码 `physical.lua:179-182` 显示，该效果为 `FIERY_SALVE`（烈火药剂），其子类型为 `subtype = { fire=true }`，提供的亲和属性为火焰/光系/闪电；上游作者在编写 `long_desc` 时直接复制了 `FROST_SALVE` 的文案而遗留了 `frost aura` 笔误；在 DLC 道具和技能说明（如 `snapshots/tome-orcs.lua:1450, 6781`）中均统一写作 `fiery aura`。
- **最强等价读法与处理**：译者主动修正了上游文本缺陷，使译文与药剂本质及实际属性亲和相符，属于合理修正，不判定为错译。
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:182`
- **缺失证据**：无

---

### C06: entry-04023 上游源码文案笔误，译文主动修正
- **完整 entry-ID**：entry-04023
- **原译短引**：
  - 原文：`Provides a frost aura, giving you +%d%% blight, mind and acid affinity.`
  - 译文：`提供静水光环，使你获得 +%d%% 枯萎、精神和酸性伤害亲和。`
- **具体意义差异**：原文字面为 `frost aura`（寒霜光环），译文译作“静水光环”，表面看存在词义偏差。
- **源码核验与机制依据**：源码 `physical.lua:207-210` 显示，该效果为 `WATER_SALVE`（静水药剂），其子类型为 `subtype = { water=true }`，提供的亲和属性为枯萎/精神/酸性；上游作者同样复制了 `FROST_SALVE` 文案且未修改 `frost aura`；在其他关联文本（`snapshots/tome-orcs.lua:1452, 6785`）中均定义为 `water aura`。
- **最强等价读法与处理**：译者主动修正了上游文本笔误，与药剂效果真实机制完全吻合，属于合理修正，不判定为错译。
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:210`
- **缺失证据**：无

---

### C07: entry-04028 飞回来源表述偏拟人化
- **完整 entry-ID**：entry-04028
- **原译短引**：
  - 原文：`The saw embedded in #Target# flies back its source.`
  - 译文：`#Target#身上的链锯飞回主人的方向。`
- **具体意义差异**：原文 `its source`（其来源 / 发射者，英文原文遗漏介词 to），译文处理为“主人的方向”。
- **源码核验与机制依据**：核验 `physical.lua:456, 465-472`，该效果为爆炸飞锯的减益结束日志，飞锯在此阶段飞回攻击者（`eff.src`）处。虽然攻击者可被视为主机/主人，但将“来源”代换为“主人”略带拟人色彩，且“主人的方向”相比“飞回其来源处”稍欠严谨。
- **最强等价读法与处理**：战斗情境下玩家能完全理解其指向发射飞锯的敌人或主角自身，不构成实质机制错误。建议未来润色为：“嵌入#Target#体内的链锯飞回其来源。”
- **明确 status**：`advisory`
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua:456`
- **缺失证据**：无

---

## 三、审核汇总统计

- **总审核条目数**：20 条
- **未发现问题（Pass）**：14 条（entry-04012, 04016, 04017, 04020, 04021, 04024, 04025, 04026, 04027, 04029, 04030, 04032, 04033 等）
- **存在问题（Confirmed）**：1 条（entry-04019 / C04 漏译触发条件与爆炸中心）
- **仅建议（Advisory）**：5 条（entry-04014 / C01 翻译腔微调；entry-04015 / C02 机制补充说明；entry-04018 / C03 状语省略；entry-04022 / C05 与 entry-04023 / C06 确认系上游源码文案笔误的主动修正；entry-04028 / C07 拟人修辞润色）
- **待确认（Pending）**：0 条

---

## 四、实际读取路径与版本限制说明

1. **实际读取的文件路径**：
   - 批次入口：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-16.md`
   - 规则与清单：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`、`source-access.json`、`terms.json`
   - 上下文快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
   - 冻结源码（DLC orcs）：
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/bullets-mastery.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Archery.lua`
   - 引擎源码（git show 固定 commit）：`/workspace/t-engine4` 之 `game/modules/tome/class/interface/Combat.lua` 及 `game/modules/tome/class/Game.lua`

2. **版本限制声明**：
   - 本次审核依据本地登记并校验哈希的公开源码，引擎核心逻辑严格基于 Commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 进行调用链推导；
   - DLC `orcs` 源码仅依凭哈希快照进行静态逻辑核验，DLC 外部仓库对应之 commit 未固定，本审查不作为对应官方正式 1.7.4 发行版本二进制的排他性证明。
