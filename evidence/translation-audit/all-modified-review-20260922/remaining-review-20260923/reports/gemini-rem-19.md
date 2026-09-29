# 翻译审核初审报告（rem-19）

**任务角色说明**：只读 REVIEWER（自然语言审核旁路）。本报告仅负责并完成 **Gemini Flash 全量初审**，未执行且不声称已经执行 GPT Sol 复核或终审。

---

## 一、逐条审核判定表（共20条）

| 序号 | 完整 entry-ID | 判定结果 | claim 编号 / 简短依据 |
| :--- | :--- | :--- | :--- |
| 1 | entry-04082 | 未发现问题 | 神器描述，语气与机制对应准确，无格式缺陷 |
| 2 | entry-04084 | 未发现问题 | 与 entry-04082 同文副本，准确一致 |
| 3 | entry-04085 | 未发现问题 | NPC 喊话，占位符 `%s` 与颜色标签 `#PURPLE#` 完整，语义准确 |
| 4 | entry-04088 | 存在问题 | C01：主语名词错译，“the Amulet”被错译为“神” |
| 5 | entry-04090 | 未发现问题 | 简述物品说明，准确无误 |
| 6 | entry-04091 | 未发现问题 | 解锁标题，术语“科技法师（元素法师）”及颜色标签无误 |
| 7 | entry-04092 | 仅建议 | C02：特性概括中“damage and debilitate”简化为“毁灭”，略去削弱机制特征 |
| 8 | entry-04093 | 未发现问题 | 解锁战役职业选项标题，语义明确，高亮标签完整 |
| 9 | entry-04094 | 未发现问题 | 符合术语库 Mage -> 法师系 规范，高亮标签完整 |
| 10 | entry-04095 | 未发现问题 | 符合术语库 Rogue -> 盗贼系 规范，高亮标签完整 |
| 11 | entry-04096 | 未发现问题 | Age of Ascendancy 意译为原版战役，符合通用译法 |
| 12 | entry-04097 | 未发现问题 | 术语 Whitehoof -> 白蹄 准确，标签完整 |
| 13 | entry-04098 | 未发现问题 | 术语 Yeti -> 雪人 准确，标签完整 |
| 14 | entry-04099 | 未发现问题 | 术语 Annihilator -> 歼灭者、Tinker -> 工匠系 准确无误 |
| 15 | entry-04101 | 存在问题 | C03：“weaken ... to your gunslinging”错译为“在你的枪法前无处遁形”，词义严重偏离 |
| 16 | entry-04104 | 未发现问题 | 人物面板数值 tooltip 格式化串，占位符与颜色无误 |
| 17 | entry-04105 | 未发现问题 | 机制限制提示，对应底层 `T_SHOOT` 与重装武器判定，准确清晰 |
| 18 | entry-04106 | 仅建议 | C04：“experimenting tinker”译为“实验的工匠”稍显生硬翻译腔 |
| 19 | entry-04107 | 未发现问题 | 任务选项提示，语境意译对应工匠大师洞穴机制，准确自然 |
| 20 | entry-04108 | 未发现问题 | 制作插件日志，占位符 `%s` 完整，动词与术语准确 |

---

## 二、疑点详细清单

### C01: entry-04088
- **条目 ID**：`entry-04088`
- **原译短引**：
  - 原文：`#GOLD#The light of the Amulet envelops you, then subsides. You feel stronger. (+1 Prodigy Points)`
  - 原译：`#GOLD#神的光辉充盈着你的全身，然后渐渐消退。你感觉更加强大了。（+1觉醒点）`
- **具体意义差异**：原文主语是 `The light of the Amulet`（护符的光辉/光芒）。原译将其误译为“神的光辉”，把物理发光实体“护符”（Amulet）错误替换为“神”。虽然该神器全称为“Gardanion, the Light of God”，但此处叙事主体是佩戴该护符时“护符的光芒包裹了你”，译文篡改主语导致动作实体错位，并带入了原文不存在的神圣降临宗教语境，属于明确的语义 fidelity 偏差。
- **最强等价读法与处理**：译者可能因物品名称后缀含有“the Light of God”而联想套改，但原文字面非常明确是护符发光。即使作为文学意译，抹去“护符”主体也属于过度发挥。建议修正为：“#GOLD#护符的光芒包裹了你，然后渐渐消退。你感觉更加强大了。（+1觉醒点）”。
- **明确 status**：`confirmed`（存在问题）
- **来源路径行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:7456`
  - 冻结源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/slumbering-caves/objects.lua:57-58`
- **缺失证据**：无缺失证据。

---

### C02: entry-04092
- **条目 ID**：`entry-04092`
- **原译短引**：
  - 原文：`- Terrene Technomancy: Craft and control swarms of micro spiderbots to damage and debilitate your foes with water and earth forces`
  - 原译：`- 科技法术：寒岩系——创造和控制蜘蛛机器人虫群，用水和土的力量毁灭敌人。`
- **具体意义差异**：原文机制特性为 `damage and debilitate your foes`（造成伤害并削弱你的敌人）。寒岩系技能主打水/土复合属性及多种负面减益状态（debilitate）。原译将其概括压缩为“毁灭敌人”，略去了“削弱/虚弱”（debilitate）这一机制特性。
- **最强等价读法与处理**：在解锁界面的特性介绍中，译者为追求四字排比与句子对仗（撕碎敌人、烧毁敌人、毁灭敌人）而对复合动词进行了概括意译，整体未造成严重误导。但若追求机制说明的完整性，建议调整为：“用水和土的力量伤害并削弱敌人。”
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:7901`
  - 冻结源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-mage_technomancer.lua:35`
- **缺失证据**：无缺失证据。

---

### C03: entry-04101
- **条目 ID**：`entry-04101`
- **原译短引**：
  - 原文：`- Inspire dread to weaken your foes to your gunslinging`
  - 原译：`- 激发敌人的恐惧，让敌人在你的枪法前无处遁形。`
- **具体意义差异**：英文原意是 `weaken your foes to your gunslinging`，即“削弱敌人对你枪械攻击的抗性 / 使敌人面对你的射击时更脆弱”（对应灵能射手的 dread 恐惧技能树施加虚弱/减益，让其后续枪弹造成更大打击）。原译将其译为“让敌人在你的枪法前无处遁形”，将“weaken（削弱）”篡改为“无处遁形（无法躲藏/反潜行）”，核心动词及机制含义出现根本性偏离。
- **最强等价读法与处理**：译者可能把“weaken”在文学修辞上脑补为“让敌人无力抵抗/无法遁逃”，但“无处遁形”直接导向了“识破隐形/躲避”的误导性机制联想。建议修正为：“激发敌人的恐惧，削弱敌人以使其更容易受到你枪法的打击。”或“激发敌人的恐惧，让敌人在你的枪法面前更加脆弱。”
- **明确 status**：`confirmed`（存在问题）
- **来源路径行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:8071`
  - 冻结源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-tinker_psyshot.lua:31`；技能树源码：`tome-orcs/data/talents/steam/dread.lua`
- **缺失证据**：无缺失证据。

---

### C04: entry-04106
- **条目 ID**：`entry-04106`
- **原译短引**：
  - 原文：`%s, the experimenting tinker`
  - 原译：`%s，实验的工匠`
- **具体意义差异**：`experimenting` 是现在分词定语，表示正在进行实验的工匠（护送对话说明该工匠因测试新型蒸汽科技而迷路）。原译“实验的工匠”带有字面直译痕迹，偏生硬，略有歧义（可能被误读为“被用来实验的工匠”）。
- **最强等价读法与处理**：在短称号中“实验的工匠”仍能被多数玩家领会为正在搞实验的工匠，未造成严重剧情扭曲。建议可优化为“%s，进行实验的工匠”或“%s，醉心实验的工匠”。
- **明确 status**：`advisory`（仅建议）
- **来源路径行号**：
  - 快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua:8143`
  - 冻结源码：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/OrcCampaign.lua:392`
- **缺失证据**：无缺失证据。

---

## 三、报告汇总统计

- **审查总条数**：20 条
- **未发现问题**：16 条
- **存在问题 (confirmed)**：2 条（entry-04088: C01, entry-04101: C03）
- **待确认 (pending)**：0 条
- **仅建议 (advisory)**：2 条（entry-04092: C02, entry-04106: C04）

---

## 四、实际读取路径与来源及版本限制说明

### 1. 实际读取的文件路径
- 规则与授权：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
- 来源索引：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
- 术语库：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
- 输入批次：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-19.md`
- 上下文快照：`evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`
- 冻结源码文件（SHA256 均已核验匹配）：
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/kaltor-shop/objects.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/shertul-cave/objects.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/slumbering-caves/npcs.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/slumbering-caves/objects.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/zones/town-kruk/objects.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-mage_technomancer.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-orcs_campaign_all_classes.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-orcs_campaign_mage.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-orcs_campaign_rogue.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-orcs_tinker_eyal.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-race_whitehooves.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-race_yeti.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-tinker_annihilator.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/data/texts/unlock-tinker_psyshot.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/OrcCampaign.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/overload/mod/class/interface/PartyTinker.lua`
  - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/dread.lua`

### 2. 来源与版本限制
- 本批次 20 条全部来自 `Embers of Rage` (orcs) DLC。
- **来源与版本未固定**：依据 `RULES.md` 第 5 条与 `source-access.json` 登记，DLC 源码仅哈希（SHA256）固定于 `.artifacts/i18n/all-modified-review-20260922/sources/orcs/` 快照，外部源码仓库 commit 及具体目标版本未固定；本次审核**未宣称亦不得宣称已核验 1.7.4 正式版本**。
- 本次审核严格遵循只读约束，未对工作区进行任何文件写入，未创建子代理，未读取历史审核报告，仅作为 Flash 初审交付。
