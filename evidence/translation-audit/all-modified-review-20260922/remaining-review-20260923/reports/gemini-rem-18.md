# 译文只读审核报告（批次 rem-18）

**审核角色**：只读 REVIEWER（用户授权自然语言审核旁路）  
**审核阶段**：Gemini 3.8 Flash 全量初审（**未执行且不得声称已经执行 GPT 6 Sol 复核或终审**）  
**审核入口**：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-18.md`  
**审核范围**：本批次全部 20 条条目（entry-04057 至 entry-04081）及相关疑点

---

## 一、逐条审核判定表

| entry-ID | 审核结论 | Claim 编号 / 简短依据 |
| :--- | :--- | :--- |
| **entry-04057** | 未发现问题 | 主谓宾完整传达，“斯莱特”术语符合 global 规范，机制与原义吻合。 |
| **entry-04058** | 未发现问题 | 原文略带语法瑕疵（to invade），译文顺畅补全且准确传达“侵入心灵、控制其行动”。 |
| **entry-04059** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04060** | 未发现问题 | 配方宝石材料名，“蓝宝石”译名准确无误。 |
| **entry-04061** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04062** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04063** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04064** | 未发现问题 | 口语反问句风格生动，完全符合配方“装甲加固”语境，语义忠实。 |
| **entry-04065** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04066** | 仅建议 | 见 **C01**。`grant a frost aura` 译为“获得一个寒霜光环”，主语搭配略有瑕疵，但不影响机制理解。 |
| **entry-04069** | 未发现问题 | 配方宝石材料名，“火蛋白石”译名准确无误。 |
| **entry-04070** | 未发现问题 | 战斗日志占位符 `#Source#`、`#Target#` 保持完整，时序与语意忠实。 |
| **entry-04071** | 未发现问题 | 区域层名“巨魔帝国港口”统一，末尾问号排版差异按规则 6 不计缺陷。 |
| **entry-04072** | 未发现问题 | 地点实体名，专名“最后的希望”与术语表完全一致，远行传送门译名规范。 |
| **entry-04073（无此编号）** | - | 本批次无此条目，按原批次顺序直接跳转至 entry-04074。 |
| **entry-04074** | 未发现问题 | 艾琳 NPC 外貌叙事描述，行文流畅自然，语义无偏差。 |
| **entry-04075** | 未发现问题 | 戒指特殊描述，格式标记 `#{bold}#...#{normal}#` 闭合完整，表达地道。 |
| **entry-04076** | 未发现问题 | 商店入口实体名，“萨拉的草药浸剂店”符合同区域门面命名一致性。 |
| **entry-04077** | 未发现问题 | 实体名，“泽梅基斯的家”与人名/建筑对应正确。 |
| **entry-04079** | 未发现问题 | 实体手札碟片描述，G.E.M. 缩写保留正确，句义完整。 |
| **entry-04081** | 未发现问题 | 开箱掉落日志，颜色占位符 `#GOLD#` 完整，动作表述自然。 |

---

## 二、疑点详细清单

### C01: entry-04066 - 主动动词 "grant" 译为受动视角 "获得" 造成主语轻微失调
- **entry-ID**：`entry-04066`
- **原译短引**：
  - 原文：`A powerful salve that can clean physical detrimental effects from your body and grant a frost aura ...`
  - 译文：`一个可以清除你身上的负面物理效果并获得一个寒霜光环（增加寒冷、暗影和自然伤害亲和）的强大药剂。`
- **具体意义差异**：
  - 原文结构为定语从句修饰 salve，谓语动词并列为 `can clean ... and grant ...`（药剂能清除……并赋予……）。
  - 译文中“可以清除……并获得……”若直接作“药剂”的定语，字面主谓搭配变为“药剂获得寒霜光环”，属于主谓受动混淆（实际应为使用者获得）。
- **最强等价读法与处理**：
  - 中文紧缩结构下读者通常会自行脑补逻辑主语“（使你）获得一个寒霜光环”，且对伤害亲和（affinity）机制与植入体使用前提的说明完全准确，在游戏物品描述语境中歧义极小，不构成实质机制错译。
  - **建议修改**（仅供参考）：改为“一个可以清除你身上的负面物理效果并**赋予**寒霜光环（增加寒冷、暗影和自然伤害亲和）的强大药剂。”或“……并**使你获得**寒霜光环……”。
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：
  - 快照：`snapshots/tome-orcs.lua:6777`
  - 源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/therapeutics.lua:51-53`
- **缺失证据**：无（语义与代码完全可见，无未决外部事实）。

---

## 三、批次初审汇总统计

- **批次总条数**：20 条
- **未发现问题**：19 条
- **仅建议（advisory）**：1 条（C01: entry-04066）
- **存在问题（confirmed）**：0 条
- **待确认（pending）**：0 条

---

## 四、实际读取路径与来源及版本限制说明

1. **实际读取的文件路径**：
   - 审核规则：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - 数据登记：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - 术语库：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
   - 输入批次：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-18.md`
   - 上下文快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`（行 6580～7140）
   - 冻结源码（DLC `orcs`）：
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/chemistry.lua` (SHA256: `2a912861...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/electricity.lua` (SHA256: `495edeff...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/explosive.lua` (SHA256: `93dec33c...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/mechanical.lua` (SHA256: `0d61ef7b...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/smith.lua` (SHA256: `06314e2c...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/tinkers/therapeutics.lua` (SHA256: `d24b6e7c...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/general/objects/tinkers/chemistry.lua`
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/dominion-port/grids.lua` (SHA256: `50e2a03f...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/dominion-port/zone.lua` (SHA256: `b53a4098...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/gates-of-morning/grids.lua` (SHA256: `7a58724e...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/gates-of-morning/npcs.lua` (SHA256: `ec9bd053...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/gates-of-morning/objects.lua` (SHA256: `dab3bb57...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/gates-of-morning/traps.lua` (SHA256: `b8bbebee...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/gem/objects.lua` (SHA256: `a3e97e48...`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/kaltor-shop/grids.lua` (SHA256: `ff8b3109...`)

2. **来源与版本限制说明**：
   - 本批次所有条目均来自 DLC `orcs`（Embers of Rage）。
   - 根据 `source-access.json` 登记与项目规范，DLC 源码来源与 commit 为**未固定状态（unpinned）**，仅通过本地快照 SHA256 哈希进行了完整性核验。
   - 本报告**不得且未宣称**已核对 1.7.4 官方正式发布源码；所有机制判定均基于冻结快照事实。
   - 本次审核为纯只读审核旁路之 **Gemini Flash 初审**，未执行、亦不代表 GPT 6 Sol 交叉复审或主代理终审结论。
