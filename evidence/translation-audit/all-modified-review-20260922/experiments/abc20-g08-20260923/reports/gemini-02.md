## 复核判定汇总（恰好40条）

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03453 | 未发现问题 | 日志参数占位符与颜色标记完整无损，战斗提示语义准确 |
| entry-03454 | 存在问题 | C01（漏译句末独立确认短句 Nope.）、C02（肢体解剖措辞偏好建议） |
| entry-03455 | 存在问题 | C03（Maj'Eyal 违规使用被取代旧称）、C04（Fire Imps 误译火焰恶魔）、C05（Fearscape 译名自相矛盾）、C06（scrutiny 误译破坏） |
| entry-03456 | 未发现问题 | 序幕文本流畅通顺，格式标记与 @name@ 占位符完好 |
| entry-03457 | 未发现问题 | 母系（Corruptor）与子职业（Demonologist）层级关系符合中文界面惯例，标记完整 |
| entry-03458 | 存在问题 | C07（created dark cults 严重曲解为黑暗仪式）、C08（to do your binding 漏译）、C09（ranged 远程定位词遗漏） |
| entry-03459 | 未发现问题 | 种族解锁标题格式与专名规范，无遗漏 |
| entry-03460 | 存在问题 | C10（Instant cast phase door 误译为使用加速技能）、C11（解锁角色资格说明被文学化转写丢失） |
| entry-03461 | 未发现问题 | 属性比较前缀与尾随空格完整，强度术语使用准确 |
| entry-03462 | 未发现问题 | 成就描述准确完整，标点匹配 |
| entry-03463 | 未发现问题 | 力量/敏捷/体质三项基础属性名称与加值完全匹配 |
| entry-03464 | 存在问题 | C12（核心战斗属性 Magic 违背术语规范误译为魔法） |
| entry-03465 | 未发现问题 | 每等级生命加值与格式标记准确 |
| entry-03466 | 未发现问题 | 每等级生命加值负值与格式标记准确 |
| entry-03467 | 未发现问题 | 力量/敏捷/体质三项基础属性名称与加值完全匹配 |
| entry-03468 | 存在问题 | C13（核心战斗属性 Magic 违背术语规范误译为魔法） |
| entry-03469 | 未发现问题 | 基础生命加值与格式标记准确 |
| entry-03470 | 未发现问题 | 经验惩罚比例与格式标记准确 |
| entry-03471 | 未发现问题 | 力量/敏捷/体质三项基础属性名称与加值完全匹配 |
| entry-03472 | 存在问题 | C14（核心战斗属性 Magic 违背术语规范误译为魔法） |
| entry-03473 | 未发现问题 | 基础生命加值与格式标记准确 |
| entry-03474 | 未发现问题 | 经验惩罚比例与格式标记准确 |
| entry-03475 | 存在问题 | C15（漏译时序副词 suddenly 且句意产生偏离） |
| entry-03476 | 未发现问题 | 对话口吻自然贴切，语意完整 |
| entry-03477 | 未发现问题 | 紧密呼应上文对话语境，口语应答自然准确 |
| entry-03478 | 未发现问题 | 事件日志语义准确，颜色标记无损 |
| entry-03479 | 仅建议 | C16（burst out 译为掉了出来，动词表现力较弱建议优化） |
| entry-03480 | 未发现问题 | 事件日志语义准确，颜色标记无损 |
| entry-03481 | 仅建议 | C17（找遍了搜刮对象措辞略显翻译腔建议润色） |
| entry-03482 | 未发现问题 | 觉醒点加值与占位符匹配正确 |
| entry-03483 | 未发现问题 | 技能树解锁点加值与占位符匹配正确 |
| entry-03484 | 未发现问题 | 职业技能点加值与占位符匹配正确 |
| entry-03485 | 未发现问题 | 通用技能点加值与占位符匹配正确 |
| entry-03486 | 未发现问题 | 属性点加值与占位符匹配正确 |
| entry-03487 | 未发现问题 | 标点与排版规范，信息完整 |
| entry-03488 | 未发现问题 | 密室门交互提示清晰准确 |
| entry-03489 | 未发现问题 | 密室门交互提示清晰准确 |
| entry-03490 | 未发现问题 | 密室门交互提示清晰准确 |
| entry-03491 | 存在问题 | C18（漏译状态修饰词 oozing 且臆造“这团绿泥”实体描述）、C19（专名偏离建议） |
| entry-03492 | 未发现问题 | 攻击细胞机制与组织特征描述准确，语序顺畅 |

---

## 详细观察与 Claim 说明

### C01 | entry-03454 | 存在问题
- **原文短引**：`For experiment. Not for fun. Nope.`
- **译文短引**：`不是娱乐，而是实验。`
- **问题具体内容**：句末独立的断言短句 `Nope.`（“才怪 / 绝非如此 / 绝无玩笑”）在译文中被完全漏译。原文通过短促的四个句子片段构成了鲜明的黑色幽默语气，漏译导致原作者特有的调侃与确认语气丢失。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/zones/searing-halls/npcs.lua:73`（DLC公开快照，源码commit未固定），作为 `mutilator`（恶魔切割者）的 NPC 实体描述（`desc`）显示给玩家查看。

### C02 | entry-03454 | 仅建议
- **原文短引**：`A demon with 3 arms`
- **译文短引**：`一个长着三只手的恶魔`
- **建议内容**：`3 arms` 译为“三只手”，在中文俗语中容易引起“扒手/窃贼”的不必要联想。建议使用“三条手臂”以更清晰准确地表现其变异解剖结构。此项仅属用词偏好，不影响事实理解。
- **状态**：仅建议

### C03 | entry-03455 | 存在问题
- **原文短引**：`Many in Maj'Eyal have heard of "demons"`
- **译文短引**：`在马基埃亚尔，很多人都曾听闻“恶魔”的大名`
- **问题具体内容**：译文使用了旧称 `马基埃亚尔`。根据术语快照明确规定，`Maj'Eyal` 的统一规范译名为 `马基·埃亚尔`（`T.PN.WORLD`，places，preferred，规则注记：“维护者于 2026-08-25 裁定采用‘马基·埃亚尔’；‘马基埃亚尔’已被取代”）。译文直接违反了明确适用的首选术语要求。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28`（DLC公开快照，源码commit未固定），作为 DLC 的描述（`description`）展示在游戏模组与 DLC 选择列表中。

### C04 | entry-03455 | 存在问题
- **原文短引**：`call forth a squad of Fire Imps to pelt your enemies to death`
- **译文短引**：`召唤火焰恶魔将敌人烧成灰烬`
- **问题具体内容**：
  1. 生物/召唤物类型误译：`Fire Imps` 是游戏内明确的怪物与恶魔使者召唤仆从“火焰小鬼”（Imp 在 ToME4 中恒为“小鬼”，如水小鬼、火小鬼，不同于大恶魔 Demon）。译为“火焰恶魔”混淆了恶魔阶级与召唤物实际实体类别。
  2. 战术动作曲解：`pelt your enemies to death while they exhaust themselves on your impenetrable defenses`（在敌人耗尽体力于你坚不可摧的防御前，召唤小鬼小队不断投掷火弹将他们砸死/风筝击毙）被随意偏离转写为“将敌人烧成灰烬”，丢失了防御反击配合持续骚扰的战术描述特征。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:32`（DLC公开快照，源码commit未固定），恶魔使者职业特性说明。

### C05 | entry-03455 | 存在问题
- **原文短引**：`Their Fearscape floats far above the skies` vs `plains of the Fearscape`
- **译文短引**：`他们的恐惧空间高浮于天幕之上` vs `恶魔空间的平原`
- **问题具体内容**：同一文本内对专有位面名称 `Fearscape` 的翻译自相矛盾。第 1 段译为 `恐惧空间`，特性第 3 点却译为 `恶魔空间`。依据术语快照，`fearscape` 的统一译名为 `恶魔空间`（`T.NARRATIVE.LORE`，narrative，existing dlc）。同一文本内部译名不一致破坏了专名统一性。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28, 33`（DLC公开快照，源码commit未固定），DLC 背景叙事与新区域介绍。

### C06 | entry-03455 | 存在问题
- **原文短引**：`As the barrier between our worlds begins to crack under their scrutiny`
- **译文短引**：`隔绝两端世界的屏障，在他们的破坏下开始破碎`
- **问题具体内容**：原文 `under their scrutiny` 意为在恶魔持续的严密窥探/审视之下，裂隙悄然产生。译文误译为 `在他们的破坏下`，曲解了原句中恶魔尚未全面突破、仅凭窥视与法术试探便引起裂痕的悬疑紧张氛围。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28`（DLC公开快照，源码commit未固定），世界背景说明。

### C07 | entry-03458 | 存在问题
- **原文短引**：`they have created many dark cults to spread fear and terror.`
- **译文短引**：`并通过黑暗仪式来传播不安与恐慌。`
- **问题具体内容**：原文 `created many dark cults`（建立了许多黑暗教派 / 创立了多个邪教组织）被严重曲解为 `通过黑暗仪式`。译文将核心实体名词 `cults`（教派/邪教）错译为“仪式”（rituals），且将谓语动作 `created`（建立/创立）丢失篡改为状语“通过”，丢失了恶魔在埃亚尔大陆扶植黑暗教派势力的核心叙事背景。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:22`（DLC公开快照，源码commit未固定），恶魔使者职业解锁说明正文。

### C08 | entry-03458 | 存在问题
- **原文短引**：`- Summon and control demons to do your binding.`
- **译文短引**：`- 召唤并控制恶魔`
- **问题具体内容**：原文职业特性第 3 项句末的目的状语 `to do your binding`（履行你的契约 / 听从你的役使差遣）在译文中被直接截断漏译。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:29`（DLC公开快照，源码commit未固定），职业特性条目列表。

### C09 | entry-03458 | 存在问题
- **原文短引**：`Corruptors are spellcasters, ranged attackers using magic.`
- **译文短引**：`堕落系是施法职业，能使用魔法攻击敌人。`
- **问题具体内容**：原文 `ranged attackers using magic`（使用魔法的远程攻击者）中，明确战斗距离特性的定位词 `ranged`（远程）在译文中被漏译，仅泛化为“能使用魔法攻击敌人”。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:26`（DLC公开快照，源码commit未固定），职业定位概括。

### C10 | entry-03460 | 存在问题
- **原文短引**：`- Instant cast phase door`
- **译文短引**：`- 使用加速技能，瞬间穿梭空间`
- **问题具体内容**：
  1. 机制理解严重错误：`Instant cast` 在 ToME4 引擎中专指不占用行动回合的瞬发特性（即 `no_energy = true`），译文将其曲解为“使用加速技能”，生造出了一个不存在的加速增益动作。
  2. 核心技能名称被改写丢失：`phase door`（相位之门）是游戏中标准的短距离传送技能（术语快照：`Phase Door` -> `相位之门`，`T.GAME.TALENT`）。魔化精灵的首个种族天赋 `Haste of the Doomed` 实际机制正是一个具有瞬发特性的定向短距离相位之门（DLC快照 `data/talents/misc/races.lua:42-43`：`is_teleport = true, no_energy = true`）。译文将“瞬发相位之门”错误翻译为“使用加速技能，瞬间穿梭空间”，造成严重机制误导。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua:28`（DLC公开快照，源码commit未固定；关联 `data/talents/misc/races.lua:36-44`）。

### C11 | entry-03460 | 存在问题
- **原文短引**：`thus have earned the right to make #LIGHT_GREEN#Doomelf#WHITE# characters.`
- **译文短引**：`#LIGHT_GREEN#魔化精灵#WHITE# 应运而生。`
- **问题具体内容**：原文直接陈述玩家达成的机制解锁结果——“从而获得了创建魔化精灵角色的资格”。译文将其过度文学化修饰为“魔化精灵应运而生”，丢弃了通知玩家获得新建角色资格的核心机制信息。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua:24`（DLC公开快照，源码commit未固定），种族解锁成就与建卡资格提示。

### C12 | entry-03464 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * +3 Magic, +0 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * +3 魔法，+0 意志，+0 灵巧`
- **问题具体内容**：在人物创建界面属性修正列表（`_t"#GOLD#Stat modifiers:"`）中，基础核心属性 `Magic` 必须依照六大战斗属性标准术语统一译为 `魔力`（术语快照：`Magic` -> `魔力`，`T.GAME.STAT`；短名 `mag` -> `魔力`）。译文将其误译为 `魔法`（混淆了属性 Magic 与法术/魔法类别 Magic），违背明确适用的战斗属性术语规范。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/demented.lua:83`（DLC公开快照，源码commit未固定），迷乱系职业创建界面属性加值展示。

### C13 | entry-03468 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * +2 Magic, -1 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * +2 魔法，-1 意志，+0 灵巧`
- **问题具体内容**：同 C12。在抓狂矮人（Drem）种族属性修正列表中，基础战斗属性 `Magic` 被错误译为 `魔法` 而非规范术语 `魔力`（`T.GAME.STAT`）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/drem.lua:33`（DLC公开快照，源码commit未固定），Drem 种族属性加值展示。

### C14 | entry-03472 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * -2 Magic, +2 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * -2 魔法，+2 意志，+0 灵巧`
- **问题具体内容**：同 C12、C13。在克罗格（Krog）种族属性修正列表中，基础战斗属性 `Magic` 被错误译为 `魔法` 而非规范术语 `魔力`（`T.GAME.STAT`）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/krog.lua:33`（DLC公开快照，源码commit未固定），Krog 种族属性加值展示。

### C15 | entry-03475 | 存在问题
- **原文短引**：`Oh, I suddenly feel like I have potential to grow.`
- **译文短引**：`哦，我觉得我的潜能增长了。`
- **问题具体内容**：
  1. 遗漏表即时时序的副词：原文 `suddenly`（突然）未予翻译。该对话分支是玩家选择赠予 NPC 属性点（`[Offer her stat increases.]`）后 NPC 的即时反应，“突然感到”体现了属性提升生效的当下感。
  2. 语义轻度偏离：`have potential to grow`（有了成长的潜力/潜能）表示具备了后续成长的空间，译文转写为“潜能增长了”，在表意重点上略有偏移。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu-escaped.lua:73`（DLC公开快照，源码commit未固定），救出玛露（Malyu）后的对话节点。

### C16 | entry-03479 | 仅建议
- **原文短引**：`#DARK_SEA_GREEN#A not yet digested foe burst out from the sack!`
- **译文短引**：`#DARK_SEA_GREEN#一个没有被完全消化的敌人从消化袋里掉了出来！`
- **建议内容**：原文动词短语为 `burst out from the sack`，表现尚未消化的强敌猛烈冲出、破囊而出的攻击性动态；译文使用“掉了出来”，动词表现力明显被弱化为被动掉落。但该句已准确传达“未被消化的敌人脱离消化袋出现”的事实，不构成事实误导，属修辞表现力提升建议。
- **状态**：仅建议

### C17 | entry-03481 | 仅建议
- **原文短引**：`You have already scavenged what you could understand and use.`
- **译文短引**：`你已经找遍了你能理解和使用的东西。`
- **建议内容**：原文 `scavenged what you could understand and use` 意为已将能理解和使用的物品搜刮带走。译文“找遍了你能理解和使用的东西”将搜刮对象误作了搜查范围，动宾搭配略显生硬（通常为“找遍了残骸”或“搜刮走了所有能用的物品”）。鉴于能正常传达残骸已无可搜刮物的游戏信息，属措辞润色建议。
- **状态**：仅建议

### C18 | entry-03491 | 存在问题
- **原文短引**：`A green oozing defence cell of the Maggot.`
- **译文短引**：`这团绿泥是巨大蛆虫的防御细胞。`
- **问题具体内容**：
  1. 状态修饰词漏译：`oozing`（渗液的 / 淌着黏液的）作为描述细胞生物体表特征的核心修饰语，在译文中被直接丢弃。
  2. 臆造实体称谓：原文核心为名词短语 `A green oozing defence cell`（一个渗液的绿色防御细胞），译文强行重组为判断句并凭空捏造了原文不存在的称谓“这团绿泥”（该 NPC 实体名为 plasmic disruptor，基础类型虽为 BLOB，但英文文本本身并无“泥/绿泥”词汇）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/general/npcs/blobs.lua:54`（DLC公开快照，源码commit未固定），等离子分裂细胞的怪物介绍。

### C19 | entry-03491 | 仅建议
- **原文短引**：`of the Maggot`
- **译文短引**：`巨大蛆虫的`
- **建议内容**：`the Maggot` 在 Cults of Entropy 中为特定巨型异形区域/生物的专名（术语快照：`maggot` -> `蛆虫`，`T.GAME.ENTITY`，creatures，entity subtype）。译文增添修饰词译为“巨大蛆虫”，虽然符合其实体背景事实，但相比标准专名稍显随意，建议与实体专名保持一致。
- **状态**：仅建议

---

## 读取路径、调用链与合规报告

### 1. 实际读取的全部路径与版本快照
- **冻结输入与包内文件**：
  - `INPUT.md`（完整40条冻结文本与术语快照）
  - `entries.json`（40条元数据、事件历史与哈希：`5f486f0b...` 至 `d0a17902...`）
  - `context.lua`（同目录上下文）
  - `source-access.json`（源码访问清单与哈希白名单）
- **DLC 基础 sources 单文件（公开快照，源码仓库/commit未固定，全部哈希核验匹配）**：
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua`（SHA256: `eb183d02...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/zones/searing-halls/npcs.lua`（SHA256: `0c85510c...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua`（SHA256: `6455aeba...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua`（SHA256: `313846d3...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua`（SHA256: `dd01f3f4...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua`（SHA256: `df3f2677...`）
  - `sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua`（SHA256: `58acfdf3...`）
  - `sources/dlc/cults/tome-cults/data/achievements/all.lua`（SHA256: `d3350e91...`）
  - `sources/dlc/cults/tome-cults/data/birth/demented.lua`（SHA256: `22fa8c40...`）
  - `sources/dlc/cults/tome-cults/data/birth/drem.lua`（SHA256: `a42cea27...`）
  - `sources/dlc/cults/tome-cults/data/birth/krog.lua`（SHA256: `5c802aa7...`）
  - `sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu-escaped.lua`（SHA256: `05dcccab...`）
  - `sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu.lua`（SHA256: `2d1e6af9...`）
  - `sources/dlc/cults/tome-cults/data/general/events/digestive-sack.lua`（SHA256: `e5ac894d...`）
  - `sources/dlc/cults/tome-cults/data/general/events/space-dwarf-ship.lua`（SHA256: `803471b4...`）
  - `sources/dlc/cults/tome-cults/data/general/grids/fonts.lua`（SHA256: `284d1e44...`）
  - `sources/dlc/cults/tome-cults/data/general/grids/fortress-multiverse.lua`（SHA256: `fb675dc3...`）
  - `sources/dlc/cults/tome-cults/data/general/grids/godfeaster.lua`（SHA256: `5fa06a43...`）
  - `sources/dlc/cults/tome-cults/data/general/grids/maggot.lua`（SHA256: `080d9cf7...`）
  - `sources/dlc/cults/tome-cults/data/general/grids/slimy_godfeaster.lua`（SHA256: `94ce5eaa...`）
  - `sources/dlc/cults/tome-cults/data/general/npcs/blobs.lua`（SHA256: `d0a17902...`）
- **额外追溯引入的单个 DLC 快照文件**：
  - `.../sources/ashes-urhrok/tome-ashes-urhrok/data/talents/misc/races.lua`（SHA256: `66694c67...`，列明于 `source-access.json` 的 `dlc_additional_sources.ashes-urhrok`）。
  - **调用链来源**：由 `entry-03460`（`unlock-race_doomelf.lua`）中种族特性 `Race features: - Instant cast phase door` 的技能机制疑点引入，用于单文件核验魔化精灵首个种族技能 `Haste of the Doomed` 的具体字段（证实其定义包含 `is_teleport = true` 与 `no_energy = true`）。
- **任务专属临时目录**：
  - `/tmp/abc20-g08-20260923-ohbjgmha`（已在分析校验完成后完全删除，未读取他人材料）。

### 2. 无法核验与越界自查
- **无法核验项**：无。40条对应源码均在允许的 DLC 公开快照单文件中定位，机制与格式均有可核验的源码与语境支撑。DLC 快照源码仓库/commit未固定，上述核验结论均基于公开快照内可证事实。
- **越界情况**：无任何越界。未读取翻译工作树当前文件、其他实验文件、SPEC/STATE 或历史报告；未创建子 agent；未修改仓库；未向其他模型查找比较结果；不声称生产 `DONE_VERIFIED`。本输出为独立只读审核观察。
