# 40条译文独立复核报告（entry-03333 至 entry-03372）

本报告为 REVIEWER 角色独立只读复核产物（purpose: `translation_contextual_v1`）。依据冻结输入、`entries.json`、`context.lua`、`source-access.json` 及其声明的源码单文件完成，未创建子 agent，未修改仓库文件，不提供修改方案，不声称生产 `DONE_VERIFIED`。

---

## 40条判定总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03333 | 未发现问题 | 占位符、颜色标记及提示语义完全匹配 |
| entry-03334 | 未发现问题 | 首行换行符、占位符及重启提示语义一致 |
| entry-03335 | 仅建议 | C01（目标插件介词搭配与书面语措辞偏好） |
| entry-03336 | 仅建议 | C02（量词“个”建议调整为“种”以贴合 kinds 类别定义） |
| entry-03337 | 未发现问题 | 专名、术语与成就达成条件准确对应 |
| entry-03338 | 未发现问题 | 颜色标记与专名译名一致 |
| entry-03339 | 未发现问题 | 专名译名一致 |
| entry-03340 | 未发现问题 | 属性名称及数值修正准确 |
| entry-03341 | 仅建议 | C03（属性名“魔法”建议统一为面板标准词“魔力”，existing状态不作强制缺陷） |
| entry-03342 | 未发现问题 | 数值与每等级生命标签准确对应 |
| entry-03343 | 未发现问题 | 属性名称及数值修正准确 |
| entry-03344 | 未发现问题 | 数值与每等级生命标签准确对应 |
| entry-03345 | 存在问题 | C04（诗歌背景定语关系信息遗漏与动作缺失） |
| entry-03346 | 未发现问题 | 属性名称及数值修正准确 |
| entry-03347 | 仅建议 | C05（属性名“魔法”建议统一为“魔力”，同 C03） |
| entry-03348 | 未发现问题 | 基础生命成长数值准确对应 |
| entry-03349 | 未发现问题 | 经验惩罚百分比标签准确对应 |
| entry-03350 | 未发现问题 | 恶魔雕像专名译名准确 |
| entry-03351 | 未发现问题 | 技能名与破墙特殊效果准确对应 |
| entry-03352 | 仅建议 | C06（伤害治疗后半句表达偏好） |
| entry-03353 | 存在问题 | C07（遗漏状态抗性转移的渐进时序特征信息） |
| entry-03354 | 未发现问题 | 卸下与重置状态限制描述准确 |
| entry-03355 | 未发现问题 | 卸下与重置可用状态描述准确 |
| entry-03356 | 未发现问题 | 阴影强度对应全豁免加成机制准确 |
| entry-03357 | 未发现问题 | 阴影强度对应法术强度等值加成机制准确 |
| entry-03358 | 存在问题 | C08（遗漏范围修饰词 "all"，未指明为全抗性穿透） |
| entry-03359 | 未发现问题 | 移速百分比加成数值及机制准确 |
| entry-03360 | 未发现问题 | 法术暴击率半值加成计算准确 |
| entry-03361 | 存在问题 | C09（空间介词短语误译曲解客观场景描写） |
| entry-03362 | 未发现问题 | 阴影强度对应物理强度等值加成机制准确 |
| entry-03363 | 未发现问题 | 全体伤害加成百分比准确 |
| entry-03364 | 未发现问题 | 全体抗性百分比加成准确 |
| entry-03365 | 存在问题 | C10（恶魔生物实体名 "wretchling" 错译为口语词） |
| entry-03366 | 存在问题 | C11（关键机关道具 "plate" 漏译，"bindings" [拘束具] 错译） |
| entry-03367 | 未发现问题 | 标题格式与职业术语准确 |
| entry-03368 | 未发现问题 | 标题格式与职业术语准确 |
| entry-03369 | 未发现问题 | 标题格式与种族术语准确 |
| entry-03370 | 未发现问题 | 标题翻译准确一致 |
| entry-03371 | 存在问题 | C12（武器修饰词漏译、构装体实体漏译及书写中断语义丢失） |
| entry-03372 | 存在问题 | C13（作战主体实体 "our casters" 错译为抽象名词“法术”） |

---

## 详细观察与 Claim 分析

### C01 | entry-03335 | 仅建议
- **短引**：
  - 原文：`Choose the addon you want to copy translation file to.`
  - 译文：`选择你想要将翻译文件拷贝去的插件。`
- **问题说明**：译文“拷贝去的插件”带方言或口语色彩，介词与动词搭配略显生硬；但目标对象与操作含义准确完整，未造成歧义或信息丢失。
- **状态**：仅建议。
- **依据与语境**：所属组件 `addon-dev` 源码未提供（`unavailable`），纯文本语义核对。仅属措辞自然度与书面语润色偏好，不构成缺陷。

### C02 | entry-03336 | 仅建议
- **短引**：
  - 原文：`Activated all 23 different kinds of demon statues.`
  - 译文：`启动全部23个不同的恶魔雕像。`
- **问题说明**：原文为 "23 different kinds of demon statues"；在代码逻辑中，该成就统计的是23种恶魔雕像（`statue_kind = kind`）。中文译文使用了量词“个”（“23个不同的恶魔雕像”），虽然表达了23个各不相同，但从分类属性上看，量词“种”更符合 "different kinds" 的范畴概念。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/grids/demon_statues.lua:22-59` 中定义了23个 `kind`，成就 `ASHES_ALL_STATUES` 统计该激活计数。译文对成就达成条件无实质误导，仅属量词精确度偏好。

### C03 | entry-03341 | 仅建议
- **短引**：
  - 原文：`#LIGHT_BLUE# * +2 Magic, +0 Willpower, +1 Cunning`
  - 译文：`#LIGHT_BLUE# * +2 魔法，+0 意志，+1 灵巧`
- **问题说明**：角色六大基础属性中的 Magic 在角色面板与通用术语中统一称为“魔力”；此处译文采用了“魔法”。因术语快照中 `Magic -> 魔力` 的 status 为 `existing`，依据规则 `existing不构成强制改名依据`，且玩家在属性修正列表中完全能够理解其指代魔力属性，故不列为缺陷。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/corrupted.lua:57`，属于创角面板描述文本，建议全库统一为“魔力”。

### C04 | entry-03345 | 存在问题
- **短引**：
  - 原文：`One rages and torments in deep oceans blue, / one fights for the third with the cultists she taught.`
  - 译文：`之一在无尽的深海中永远咆哮 / 之一召集邪徒为复活另一者而战`
- **问题说明**：
  1. 第4句原文为 "with the cultists she taught"（带着她所传授/教导的邪教徒），体现了莎西·凯希传授信徒腐化知识并率领其战斗的师徒/从属关系；译文意译为“召集邪徒”，将定语从句 "she taught"（她所教导）完全遗漏。
  2. 第3句原文 "torments"（折磨/肆虐）未译出，意译加入了“无尽”与“永远”。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:27-32`（魔化精灵解锁诗歌）。诗中逐一对应被困埃亚尔的三大恶魔（深海的乌尔罗格、带领被其教导信徒的莎西·凯希，以及第三者克里尔·费扬）。遗漏 "she taught" 丢失了背景剧情中莎西·凯希与邪教徒的关系信息。

### C05 | entry-03347 | 仅建议
- **短引**：
  - 原文：`#LIGHT_BLUE# * +3 Magic, +2 Willpower, +0 Cunning`
  - 译文：`#LIGHT_BLUE# * +3 魔法，+2 意志，+0 灵巧`
- **问题说明**：同 C03，属性名 Magic 译为“魔法”，术语状态为 existing，不构成强制缺陷，建议与“魔力”统一。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:39`。

### C06 | entry-03352 | 仅建议
- **短引**：
  - 原文：`All enemies in radius 2 take 20 fire damage each turn and healing you for 10% of the damage dealt.`
  - 译文：`附近2码范围的敌人每回合受到20火焰伤害。你受到10%伤害值的治疗。`
- **问题说明**：后半句“你受到10%伤害值的治疗”略显生硬欧化，但作用对象（你）、数值比例（10%伤害）以及触发逻辑（治疗）完全准确。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:118, 142`（Fearfire Mantle）调用 `engine.DamageType.FIRE_DRAIN`，引擎固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/damage_types.lua:1251` 确认其 `healfactor = 0.1`，机制数值与译文完全吻合。仅属语感偏好。

### C07 | entry-03353 | 存在问题
- **短引**：
  - 原文：`Status resistances shift over time to match the statuses you are being hit by.`
  - 译文：`依据你中的负面状态改变你的状态免疫。`
- **问题说明**：原文核心机制短语 "shift over time"（随时间推移逐渐转移/调整），译文“依据你中的负面状态改变你的状态免疫”完全遗漏了 "over time"（随时间推移/逐步）的时间维度修饰，容易让玩家误解为受到状态攻击时立刻全额变更免疫。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:315, 358-374`。装备每次 `act()` 时，若检测到角色身上存在对应负面状态，仅在 5 次循环中每次转移 0.01（即 1%）的特定状态免疫属性。该机制为明确的“随时间逐步调整”，遗漏 "over time" 导致时序机制信息缺失。

### C08 | entry-03358 | 存在问题
- **短引**：
  - 原文：`Increases all damage penetration by 1% for each point of your Shadow Power.`
  - 译文：`每点“阴影强度”增加1%抗性穿透。`
- **问题说明**：原文为 "all damage penetration"；译文仅写为“抗性穿透”，遗漏了关键范围限定词 "all"（全/全部）。在游戏中，抗性穿透有单系穿透（如火焰穿透、暗影穿透）与全伤害抗性穿透之分，缺少“全”导致作用范围不明确。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:679-681`（The Black Spike）。代码明确更新 `self.wielder.resists_pen = {all = power}`，作用于所有属性抗性穿透。同套装的 entry-03363 译有“全体伤害加成”，entry-03364 译有“全体抗性”，唯独本条遗漏了“全”。

### C09 | entry-03361 | 存在问题
- **短引**：
  - 原文：`"Wreckage all about you. Is there anything left inside?"`
  - 译文：`己身若残，何物能存？`
- **问题说明**：原文 "Wreckage all about you" 中的 "about" 为空间介词（"all about you" 即 "all around you"，意为“四周/周遭各处尽是残骸”），描绘角色身穿重型铠甲、周遭化为一片废墟废土的客观外部场景，后句进而发问铠甲之内是否还有残留；译文误将空间介词 "about you" 理解为关于自身，将 "wreckage"（残骸废墟）意译为“若残”（若残破），严重曲解了原文的客观场景描写。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:743`（The Black Plate 描述）。黑石套装风格为冷酷极简描写，此处指周围全是毁灭的残骸，内部是否还有残存，属于语义层面的曲解。

### C10 | entry-03365 | 存在问题
- **短引**：
  - 原文：`... memories of being chained and bound while a wretchling presses it to your forehead flash through your mind.`
  - 译文：`……遭锁链缠身、动弹不得时，一个猥琐小怪把它按上你额头的记忆在脑海中闪回。`
- **问题说明**：原文中将恶魔石板按在主角额头上的生物是 "a wretchling"；译文将其错译为“一个猥琐小怪”。在 ToME4 本体及本 DLC 全文（包括本条目第15段及 entry-03372）中，`wretchling` 均为固定恶魔生物种类“酸液树魔”（对应 emerald 之子改造的恶魔形态）。译作“猥琐小怪”破坏了专名统一性与世界观生物设定的严肃性。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:261`（石板第16段）结合同文件第295行（entry-03372，`demon statue: wretchling` 译为“酸液树魔”）。此处属于实体专有名词误译。

### C11 | entry-03366 | 存在问题
- **短引**：
  - 原文：`"Just step on the plate here, and hold your arms like this so I can get the bindings in place..."`
  - 译文：`“站在那里别动，举起胳膊，这样我就能把它放好……”`
- **问题说明**：
  1. "Just step on the plate here"：看管人诱骗主角踩在特定装置踏板（plate）上，译文译为“站在那里别动”，遗漏了踏板/底板（plate）道具名词，且将指示代词 "here"（这里）错译为“那里”。
  2. "so I can get the bindings in place..."：看管人给主角套上拘束锁链（bindings，束缚具/拘束带），与前文“遭锁链缠身、动弹不得”呼应；译文误将复数名词 "bindings" 理解为代词“它”（误当成了放置水晶），译作“这样我就能把它放好”，彻底丢失了欺骗主角就擒并施加拘束的关键剧情动作。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:400`。剧情中恶魔看管人以“晋升研究助理”为诱饵，诱导主角站上特定底板并伸开双臂，以便扣上束缚用具。译文遗漏 plate 并严重误译 bindings。

### C12 | entry-03371 | 存在问题
- **短引**：
  - 原文：`... wielding a double-bladed katana and fighting a giant construct labelled "Ninja Atamathon." Your badassery must have interrupted this demon's writing.`
  - 译文：`……手里拿着武士刀，正在和“忍者王阿塔玛森”对战。看起来，你的霸气侧漏把这个恶魔吓尿了。`
- **问题说明**：
  1. "double-bladed katana" 中的 "double-bladed"（双刃/双头）漏译，仅译为“武士刀”。
  2. "fighting a giant construct labelled 'Ninja Atamathon.'" 中的实体类别 "giant construct"（巨型构装体）被彻底遗漏，直接抹去了阿塔玛森作为“构装体”的实体描述。
  3. "Your badassery must have interrupted this demon's writing."（一定是你的霸气打断了这个恶魔的书写），原文呼应便条结尾被拖出墨迹的断句 "befo--"；译文被随意替换为“把这个恶魔吓尿了”，完全丢失了“字迹被霸气当场打断”的画面解构关键语义。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:491`。文本为恶搞风格的战斗汇报便条，"double-bladed katana"（致敬流行文化中夸张双刃武士刀）与 "giant construct"（构装体为游戏核心生物实体分类）均为具象设定描述，结尾亦与笔画拖断的视觉细节紧密扣合。

### C13 | entry-03372 | 存在问题
- **短引**：
  - 原文：`... serving as obstructions and shields while their acid and our casters do their work ...`
  - 译文：`……以肉体充当屏障，令酸液和法术能够发挥作用……`
- **问题说明**：原文中并列的两个行动主体是 "their acid"（它们的酸液）与 "our casters"（我们的施法者，指后方的恶魔施法单位）；译文将实体人物主体 "our casters" 错译为抽象名词“法术”（“令酸液和法术能够发挥作用”），导致战场作战协同的主体角色发生性质改变。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:514`。恶魔军队战术为前排依靠酸液树魔肉身阻挡敌人并喷洒强酸，掩护后方恶魔施法者进行输出。"casters" 明确指代作战单位角色，不能直接等同于法术。

---

## 读取路径、版本与环境审计

1. **入口文件**：
   - `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/INPUT.md`
2. **冻结数据文件**：
   - `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/entries.json`
   - `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/context.lua`
   - `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923/source-access.json`
3. **源码与哈希核验**：
   - **本体引擎**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（读取 `game/modules/tome/data/damage_types.lua` 核验 `FIRE_DRAIN` 机制）。
   - **DLC 快照**：公开快照源码仓库/commit未固定（显式标注），哈希由 `source-access.json` 固定：
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/achievements/all.lua` (`9dac1c92...`)
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/corrupted.lua` (`a61a4733...`)
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua` (`d770eea7...`)
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/general/grids/demon_statues.lua` (`27ca6462...`)
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua` (`b8a9216d...`)
     - `dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua` (`d3adada5...`)
   - **额外追加单文件（由调用链/符号引入）**：
     - `tome-ashes-urhrok/data/general/events/demon-statue.lua` (`a061598f...`，由雕像激活事件调用链引入)
     - `tome-ashes-urhrok/data/talents/corruptions/wrath.lua` (`f2297854...`，由 `obliterating_smash_wall` 属性符号引入)
4. **组件可用性**：
   - `addon-dev` 组件在 `source-access.json` 中标记为 `unavailable`，相关条目（`entry-03333`–`entry-03335`）仅依据文本字面与占位符格式进行直接核验，机制未作越界推断。
5. **临时文件与越界说明**：
   - 任务期间按授权创建任务专属临时目录 `/tmp/abc20-g05-20260923-o2xdg4um` 执行只读对比脚本，未读取他人材料。
   - 全程只读，未修改仓库任何文件，未创建任何子 agent，未发生越界读取。
