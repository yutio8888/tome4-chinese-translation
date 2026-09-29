| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03333 | 未发现问题 | 上传对象可由插件开发语境确定；参数和标记保留 |
| entry-03334 | 未发现问题 | 重启、切换语言及确认操作完整 |
| entry-03335 | 仅建议 | C01 |
| entry-03336 | 待确认 | C02 |
| entry-03337 | 未发现问题 | 三个目标、事件时间及专名对应完整 |
| entry-03338 | 未发现问题 | 专名与完成状态颜色保留 |
| entry-03339 | 未发现问题 | 专名一致 |
| entry-03340 | 未发现问题 | 三项属性及数值完整 |
| entry-03341 | 未发现问题 | 属性及数值对应；existing 术语不构成强制改名 |
| entry-03342 | 未发现问题 | 每级生命增量 +3 对应 |
| entry-03343 | 未发现问题 | 三项属性及数值完整 |
| entry-03344 | 未发现问题 | 每级生命增量 +2 对应 |
| entry-03345 | 存在问题 | C03、C04、C05、C06 |
| entry-03346 | 未发现问题 | 属性数值及负号完整 |
| entry-03347 | 未发现问题 | 属性及数值对应；existing 术语不构成强制改名 |
| entry-03348 | 未发现问题 | 每级生命增长数值 9 对应 |
| entry-03349 | 未发现问题 | 经验惩罚及 12% 完整 |
| entry-03350 | 未发现问题 | 雕像名称与同包专名一致 |
| entry-03351 | 未发现问题 | 技能及破墙效果对应 |
| entry-03352 | 未发现问题 | 范围、火焰伤害、周期及治疗比例对应 |
| entry-03353 | 存在问题 | C07 |
| entry-03354 | 未发现问题 | 可卸下、不可重置两个状态完整 |
| entry-03355 | 未发现问题 | 可卸下和可重置对应 |
| entry-03356 | 未发现问题 | 阴影强度与三项豁免的比例对应 |
| entry-03357 | 未发现问题 | 阴影强度与法术强度的比例对应 |
| entry-03358 | 未发现问题 | 未限定元素的“抗性穿透”可承载此处全系含义 |
| entry-03359 | 未发现问题 | 每点 2.5% 的移动速度比例对应 |
| entry-03360 | 待确认 | C08 |
| entry-03361 | 存在问题 | C09 |
| entry-03362 | 未发现问题 | 阴影强度与物理强度的比例对应 |
| entry-03363 | 未发现问题 | 全伤害加成及比例对应 |
| entry-03364 | 未发现问题 | 全抗及比例对应；已见装备提供的强度为 5 的倍数 |
| entry-03365 | 存在问题 | C10；刻意误译的方括号隐喻未作为缺陷 |
| entry-03366 | 存在问题 | C11、C12、C13 |
| entry-03367 | 未发现问题 | 标题及职业身份对应 |
| entry-03368 | 未发现问题 | 标题及职业身份对应 |
| entry-03369 | 未发现问题 | 标题及种族身份对应 |
| entry-03370 | 未发现问题 | 标题含义完整 |
| entry-03371 | 存在问题 | C14、C15、C16、C17、C18、C19、C20 |
| entry-03372 | 存在问题 | C21 |

以下源码简写中，`D/` 指本包 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/`，`A/` 指允许的附加快照根目录下 `tome-ashes-urhrok/`。**DLC 均为哈希已核验的公开快照，源码仓库、commit 和目标版本未固定**；本体引用均使用指定 commit。文本直接可证的问题不依赖把该快照认定为目标运行版本。

### C01 | entry-03335 | 仅建议

原文：“copy translation file to”；译文：“将翻译文件拷贝去的插件”。

“拷贝去的插件”略显生硬，但文件、操作和目的地关系均明确。`context.lua:95–106` 的插件选择及复制成功提示也支持这一理解。属于措辞偏好，无已证实信息损失。

### C02 | entry-03336 | 待确认

原文：“all 23 different kinds”；译文：“全部23个不同的恶魔雕像”。

文本确有“种类”与“个体”计量差异，但快照实现不能支持直接把“必须覆盖23种”认定为正确机制：

- `D/data/achievements/all.lua:35–39` 的 `can_gain` 仅增加 `self.nb`，达到23即满足条件。
- `D/data/general/grids/demon_statues.lua:87–92` 只对当前雕像实例防止重复激活，调用 `world:gainAchievement` 时不传种类。
- `A/data/general/events/demon-statue.lua:25–35` 每次事件重新建立候选种类；移除已选种类只作用于本次事件。
- 本体 `game/engines/default/engine/interface/WorldAchievements.lua:131–146` 按成就保存计数数据并调用 `can_gain`，未增加种类去重。

快照内可证的是累计激活数量，英文的种类要求属于上游描述与实现的疑点，不能简单判成译文漏译机制。**缺少目标 DLC 版本来源及其实际实现，保留待确认。**

### C03 | entry-03345 | 存在问题

原文：“One rages and torments”；译文：“之一……永远咆哮”。

译文保留了愤怒表现，却遗漏“折磨”这一行为，并新增永久持续的描述。证据为冻结诗歌及 `D/data/birth/doomelf.lua:29`；这是行为信息变化，不只是诗体取舍。状态：**confirmed，文本语义问题**。

### C04 | entry-03345 | 存在问题

原文：“with the cultists she taught”；译文：“召集邪徒”。

原文明确邪教徒受她教导；“召集”不能表达这一关系。`D/data/birth/doomelf.lua:30` 是直接证据。`D/data/lore/demon.lua:456–460` 支持组织追随者及恢复恋人的背景，因此不将“复活”单独判错；这里确认的是**教导关系遗漏**。

状态：**confirmed，文本语义问题**。

### C05 | entry-03345 | 存在问题

原文：“maintain your deception”；译文：“隐藏你的踪影”。

维持欺骗与掩藏行踪是不同目的。前文说明三者可能向恶魔揭露精灵造成的恐怖，灭口服务于继续蒙骗恶魔，而非避免被追踪。证据：`D/data/birth/doomelf.lua:27–32`。

状态：**confirmed，目的关系误译**。

### C06 | entry-03345 | 存在问题

原文：“and then you may witness”；译文：“新的精灵终将诞生”。

原文说明完成前述行动后，玩家才可能见证诞生；译文变为诞生终将发生，丢失“之后才可能”及玩家见证的关系。证据：`D/data/birth/doomelf.lua:31–32`。

状态：**confirmed，条件和情态信息变化**。

### C07 | entry-03353 | 存在问题

原文：“shift over time”；译文：“依据……改变”。

译文遗漏抗性随时间调整的过程，仅保留按状态改变。`D/data/general/objects/world-artifacts.lua:322–427` 的 `act` 会读取当前效果，并在反复执行时逐步转移各项免疫数值；这支持英文时间信息确有意义。

“状态免疫”本身不判错：实际修改的正是 `confusion_immune`、`stun_immune` 等数值。状态：**confirmed，冻结文本的时间信息遗漏**；快照机制仅作支持，不外推目标版本。

### C08 | entry-03360 | 待确认

原文：“equal to half”；译文：“每点……增加0.5%”。

`D/data/general/objects/world-artifacts.lua:731–732` 实际使用 `math.ceil(power / 2)`。戒指自身提供5点阴影强度（第725行），因此该状态下加成为3，而非2.5。

`A/superload/mod/class/Actor.lua:61–67` 将实际阴影强度传入更新函数并重新应用装备；本体 `game/modules/tome/class/interface/Combat.lua:1887–1890、2012–2025` 将该属性纳入暴击百分比并消费。

这是**英文与译文共同遗漏取整**，不是译文新增错误。快照行为已证，但目标 DLC 版本适用性未固定，故总状态为**待确认**。

### C09 | entry-03361 | 存在问题

原文：“Wreckage all about you. Is there anything left inside?”；译文：“己身若残，何物能存？”

原文以周围／包围自身的残破景象，追问内部是否仍有东西；译文改成“自身若残破”的假设，并泛问何物能够存留。外部与内部的对照、既存景象与疑问的关系均发生变化。

证据：`D/data/general/objects/world-artifacts.lua:737–743`，该句为黑之铠的物品描述。状态：**confirmed，意象关系和句意变化**，不以文风是否优美为依据。

### C10 | entry-03365 | 存在问题

原文：“a wretchling”；译文：“一个猥琐小怪”。

这里指特定恶魔种类，译文变成泛称，丢失实施强制改造者的身份。`D/data/lore/demon.lua:60` 为直接原文；同文件第116–118行描述这种生物的酸液袭击，第294–295行明确以其为雕像介绍对象。冻结 `context.lua:203` 和 entry-03372 也将同一对象识别为“酸液树魔”。

这是**实体身份丢失**，不只是要求统一一个既有译名。状态：**confirmed**。此处位于正常叙事段落，不属于文中刻意误译的方括号隐喻。

### C11 | entry-03366 | 存在问题

原文：“standard-issue alteration”；译文：“标准化思维修改”。

原文只说常规改造，没有限定为思维修改；译文额外指定了改造对象。上下文将防火、忠诚强化、改造和意识连接分别列举，不能由附近出现意识或忠诚就把一般改造限定为思维改造。

证据：`D/data/lore/demon.lua:135`。状态：**confirmed，译文新增范围限制**。

### C12 | entry-03366 | 存在问题

原文：“step on the plate here”；译文：“站在那里别动”。

原文要求踏上此处的平台／板面；译文变为在某处保持不动，遗漏具体承载物并改变动作。证据：`D/data/lore/demon.lua:135` 的连续操作指示。

状态：**confirmed，叙事动作信息变化**；这是回忆中的指示，不宣称它构成当前可操作任务。

### C13 | entry-03366 | 存在问题

原文：“get the bindings in place”；译文：“把它放好”。

“bindings”明确指束缚装置，译文只剩不明对象“它”，还可能被理解为前述水晶。由此丢失研究助理“晋升”实际伴随束缚的叙事信息。

证据：`D/data/lore/demon.lua:135`，紧接摆放手臂的指示。状态：**confirmed，对象及束缚动作遗漏**。

### C14 | entry-03371 | 存在问题

原文：“Highest priority is now isolating”；译文：“启动最高优先级措施”。

译文只保留优先级，未交代措施是隔离玩家。后面的体育场及平台分离描写不能替代这项明确行动目标。

证据：`D/data/lore/demon.lua:226`。状态：**confirmed，行动目标遗漏**。

### C15 | entry-03371 | 存在问题

原文：“Blow all connectors”；译文：“关闭所有链接传送门”。

原文要求炸毁连接设施，译文变为关闭传送门，同时改变动作和对象。紧接的“break platform off the continent”提供物理连接／平台分离语境；本句没有将 connectors 指定为传送门。

证据：`D/data/lore/demon.lua:226`。状态：**confirmed，文本可证的动作和对象误译**；未据此推断地图中的具体执行脚本。

### C16 | entry-03371 | 存在问题

原文：“spotlights”；译文：“闪光灯”。

体育场演出布置中的聚光照明被改为闪光灯，两者照明方式不同。证据：`D/data/lore/demon.lua:226`，与焰火、音响系统并列的舞台布置语境。

状态：**confirmed，对象误译**。

### C17 | entry-03371 | 存在问题

原文：“double-bladed katana”；译文：“武士刀”。

译文遗漏“双刃”的武器特征。该特征是涂鸦刻意夸张的内容，不能由普通武士刀自动表达。证据：`D/data/lore/demon.lua:228`。

状态：**confirmed，描述信息遗漏**。

### C18 | entry-03371 | 存在问题

原文：“a giant construct labelled ‘Ninja Atamathon’”；译文：“‘忍者王阿塔玛森’”。

译文遗漏对手是巨大构装体这一实体描述，并新增“王”的身份。即使读者认识阿塔玛森，也不能以背景知识替代本句明示的信息。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，实体特征遗漏及身份增译**；不涉及全局专名调整。

### C19 | entry-03371 | 存在问题

原文：“like the pen was rapidly jerked away”；译文：“那是笔从手上滑落留下的痕迹”。

原文根据笔迹推测笔被猛然扯开；译文将其确定为笔从手中滑落。动作原因与证据确定程度均改变。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，动作及推测语气变化**。将末尾字母改称“最后一个字”属于本地化适配，不另计缺陷。

### C20 | entry-03371 | 存在问题

原文：“must have interrupted this demon's writing”；译文：“把这个恶魔吓尿了”。

原文推断玩家的霸气打断恶魔写作；译文变成惊恐失禁，遗漏被打断的写作行为，并增加不同事件。幽默语体可以调整，但这里改变了叙述内容。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，事件替换**。

### C21 | entry-03372 | 存在问题

原文：“does an incredible service to our cause”；译文：“为我们的目标奉献了一切”。

原文赞扬每个参战者作出的巨大贡献；译文把贡献程度绝对化为奉献全部。前文分别说明愿意牺牲以及少数能够存活，结尾并未断言每个参战者都已付出一切。

证据：`D/data/lore/demon.lua:295` 的整段论述。状态：**confirmed，贡献程度被加强**。

实际读取范围与限制如下：

- 冻结包根目录 `B`：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923`。
- 读取 `B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。核对 entries 恰好40条、顺序正确，原译文与 INPUT 对应；格式检查未发现占位符、模板表达式或显示标记序列差异。
- 读取以下六份 `B/sources/dlc/ashes-urhrok/tome-ashes-urhrok/` 下源码，SHA-256 均与清单完整匹配：`data/achievements/all.lua`、`data/birth/corrupted.lua`、`data/birth/doomelf.lua`、`data/general/grids/demon_statues.lua`、`data/general/objects/world-artifacts.lua`、`data/lore/demon.lua`。
- 附加快照根目录为清单指定的 `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok`。读取并核验哈希的单文件为：
  - `tome-ashes-urhrok/superload/mod/class/Actor.lua`：由装备的 `on_obsidian_power_update`／`artifact_power_obsidian` 引入。
  - `tome-ashes-urhrok/data/talents/corruptions/brutality.lua`：由装备列出的技能类别及 `T_OBLITERATING_SMASH` 定位需要引入；未找到该技能定义。
  - `tome-ashes-urhrok/data/talents/corruptions/wrath.lua`：同一装备列出的另一技能类别；找到破墙消费代码。
  - `tome-ashes-urhrok/data/general/events/demon-statue.lua`：由雕像的 `demon_statues_list`、种类及 `demon_statue_actived` 生成／回调关系引入。
- 本体只通过 `git show` 读取 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的以下单文件：
  - `game/modules/tome/data/damage_types.lua`：追踪 `FIRE_DRAIN`。
  - `game/modules/tome/class/interface/Combat.lua`：追踪 `combat_spellcrit` 的消费。
  - `game/engines/default/engine/World.lua`、`game/modules/tome/class/World.lua`：定位 `world:gainAchievement`。
  - `game/modules/tome/class/interface/WorldAchievements.lua`、`game/engines/default/engine/interface/WorldAchievements.lua`：沿前者明确的 require／继承和调用继续核验。
- 曾尝试同一固定提交的 `engine/World.lua`；该路径不存在，未读到内容。默认沙箱首次读取失败后，使用获准的只读执行完成读取。
- addon-dev 源码缺失，前三条仅依据冻结文本、参数及允许语境判断。DLC 目标版本适用性未核验；C02、C08 保留待确认。
- 未创建临时文件、子 agent，未修改仓库，未读取其他报告或清单外材料；无已知越界。本结果仅为独立审核观察，不宣称生产 `DONE_VERIFIED`。
