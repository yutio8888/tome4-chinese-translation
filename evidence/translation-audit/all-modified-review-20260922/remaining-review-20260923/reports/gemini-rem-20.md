# 只读 REVIEWER 审核报告（批次：rem-20）

本报告为自然语言审核旁路阶段输出，仅执行本次只读审核职责，不替其他模型声称复核已完成，不宣称正式 contract `DONE_VERIFIED`。

---

## 逐条审核汇总表

| 序号 | entry-ID | 审核结论 | Claim编号 / 简短依据 |
| :--- | :--- | :--- | :--- |
| 1 | `entry-04109` | 仅建议 | C01：动词“制造/制作”较“创造”更贴合工匠语境；“插件”为现存译名不强制改名 |
| 2 | `entry-04110` | 仅建议 | C02：修饰语 `tinker` 略省未译，建议补全“工匠/插件配方”以提高完备性 |
| 3 | `entry-04114` | 未发现问题 | 机制、占位符、语态与文本完全吻合 |
| 4 | `entry-04115` | 存在问题 | C03（`relevant` 反义错译）、C04（主客体倒错误加“我们”）、C05（`filthy` 词义错译为“狡猾”）、C06（公文用语润色建议） |

---

## 疑点详细清单 (Claims)

### C01
- **完整 entry-ID**：`entry-04109`
- **原译短引**：`Created tinker: %s` -> `创造插件：%s`
- **具体意义差异**：在工匠系统制造物品语境下，`Created` 译为“制作/制造”比“创造”更自然贴切；此外 `tinker` 在 `terms.json` 中为 `蒸汽工具`（status: existing, notes: "Embers of Rage 实体类型"），但同 section 及历史 UI 广泛使用“插件”。
- **最强等价读法与处理**：原译表达“造出了该物品”之意，且按规则“existing 不强制改名”，整体可理解且无机制分歧。列为表达风格优化建议。
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua:139`
- **缺失证据**：无

---

### C02
- **完整 entry-ID**：`entry-04110`
- **原译短引**：`Learnt new tinker schematic: #LIGHT_GREEN#%s` -> `已学习新的配方：#LIGHT_GREEN#%s`
- **具体意义差异**：原文含有定语 `tinker` 修饰 `schematic`，译文仅译为“已学习新的配方”，略过了 `tinker`（工匠/插件/蒸汽工具）的限定。
- **最强等价读法与处理**：在 Embers of Rage DLC 中所有 schematic 均为工匠插件配方，且后接具体配方名称，玩家理解不受阻；但显性补齐修饰词（如“已学习新的插件配方：#LIGHT_GREEN#%s”）在完备性上更为精确严谨。
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua:159`
- **缺失证据**：无

---

### C03
- **完整 entry-ID**：`entry-04115`
- **原译短引**：`Holds up hand to silence Councilor Emeritus Kasyros. "This IS relevant, I assure you."` -> `举起手打断荣誉终身议员卡西罗斯。“我保证，真的无关紧要。”`
- **具体意义差异**：**确凿反义错译**。前文坦塔洛斯（Tantalos）两度用 `irrelevant`（无关紧要）打断卡西罗斯关于既定议程的发言，随后坦塔洛斯转而盘算借助西方大陆联军力量。面对卡西罗斯的再次打断，坦塔洛斯用全大写强调 `This IS relevant`（意为“这【确实与此相关/这绝对切题】”）。译文完全搞反，错译成了反义词“真的无关紧要”，直接颠倒了坦塔洛斯的真实论点与角色行为动机，造成对话逻辑彻底崩塌。
- **最强等价读法与处理**：无法做任何合理等价解释。必须纠正为肯定含义，如：“我保证，这确实切题/这绝对与此相关。”
- **明确 status**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua:107`（快照挂载于 `tome-orcs/superload/mod/dialogs/debug/DebugMain.lua:8341`）
- **缺失证据**：无

---

### C04
- **完整 entry-ID**：`entry-04115`
- **原译短引**：`Some want the Kruk exterminated, others imprisoned. Neither can afford direct intervention, but some form of support will assuredly be available.` -> `有些人想消灭克鲁克兽人，也有人想监禁他们。不论是哪种，我们都没法直接介入，不过确实可以提供某种支持。`
- **具体意义差异**：**主客体倒错**。前文明确在讨论西方大陆的矮小种族联军（"those silly little waist-height warriors"）对待兽人的态度。主语 `Neither` 指西方联军内部的两派势力（主张斩草除根派与主张监禁派）均无力直接派兵介入远东，但必然愿向蒸汽巨人提供间接支持。译文凭空增添第一人称代词“我们”（“我们都没法直接介入”），将西方各派势力的客观局限错误套在蒸汽巨人头上，与下文坦塔洛斯明确指示“由我们采取行动……让他们提供协助与武器”产生严重前后矛盾。
- **最强等价读法与处理**：无法作为等价解读。应剔除误增的“我们”，修正为主语对应的两派势力，如：“两方都无力直接出兵干预，但肯定能提供某种形式的支持。”
- **明确 status**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua:110`
- **缺失证据**：无

---

### C05
- **完整 entry-ID**：`entry-04115`
- **原译短引**：`More than they want those filthy little greenskins around...` -> `比起想要那些狡猾的小绿人们在身边……`
- **具体意义差异**：**词义偏差**。`filthy` 为“肮脏的、污秽的、下流的”，是坦塔洛斯对兽人（greenskins）极其露骨的种族蔑称；译文译作“狡猾的”（cunning/sly），曲解了原文字面词义，严重削弱了角色台词的蔑视语气。
- **最强等价读法与处理**：无法等价。应更正词义，如：“比起留着那些肮脏的小绿皮在身边……”。
- **明确 status**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua:122`
- **缺失证据**：无

---

### C06
- **完整 entry-ID**：`entry-04115`
- **原译短引**：`So! It's resolved that we have much to gain from this...` -> `所以！这决定了我们从这方案里获益良多……`
- **具体意义差异**：`It's resolved that...` 是正式议会表决公文用语（“兹决议……” / “决议确认……”）。原译“这决定了……”将其弱化为因果事理陈述，削弱了议会会议纪要的公文语体风格。
- **最强等价读法与处理**：通俗口语语境下能大致理解为“议会定下了方案”，不构成事实性阻断，列为文体风格润色建议。
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua:123`
- **缺失证据**：无

---

## 实际读取路径与版本限制说明

1. **实际读取的文件路径**：
   - 入口批次：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-20.md`
   - 规则与清单：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - 源码访问登记：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - 术语库：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
   - 译文快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`（行 8165-8400）
   - 冻结源码（SHA256 校验核对一致）：
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua` (`719808907832f6a22a8e296d30cb7e590603a5e03912bc185937d19109dbb258`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/class/interface/Archery.lua` (`27dd73133f11c6e3a9ac8b84a1097ea098b0b442a0e40bd035a215f3afac0f8a`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/superload/mod/dialogs/debug/DebugMain.lua` (`2787c9bf9441350c61156cb6fa7097b57b7eccdbcb9c63cb87d8f3fbc047096b`)
     - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/lore/palace-fumes.lua` (`b57c1122b56037bd86ca9815e8a59700db548755d9c401e5ee17959a5cf3fc2a`)
2. **版本限制声明**：
   - 本批次所有条目均来自 `orcs` (Embers of Rage) DLC。
   - 依据 `source-access.json` 与审核规则，DLC 源码仅哈希（SHA256）固定，仓库 commit 及目标版本未固定；本审核严格基于已固定的源码快照与文本进行比对，**不宣称已核验 1.7.4 版本行为**。
