# 匿名源码核验与归并：40 条 / 108 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方108项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好108行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03294

### C01 | entry-03294 | 存在问题

原文要求黄色名称的光环“**After turning them on here**”再手动关闭、启用；译文说“在这里调整之后”，把操作条件扩成任何调整。`ShimmerRemoveSustains.lua:94–106,150–157` 显示黄色对应 `no_sustain_autoreset`，在界面重新开启时不会执行自动重置。状态：已证实。



## O002 | entry-03294

### C01 | entry-03294 | 存在问题

原文：“After turning them on here”；译文：“在你在这里调整之后”。

**confirmed，译文扩大操作条件。** 原文要求在这里重新开启光环后，手动关闭并重启持续技能；“调整之后”也包含隐藏光环的操作。

`G/dialogs/shimmer/ShimmerRemoveSustains.lua:94` 的 `toggleAura` 在隐藏分支直接移除粒子；恢复分支才考虑重启技能。第 103 行跳过 `no_sustain_autoreset` 技能的自动重启，第 155 行将这些技能标黄。因此手动重启要求具体对应恢复显示，不能泛指所有调整。



## O003 | entry-03294

### C01 | entry-03294 | 存在问题
- **原文**：「After turning them on here, you need to unsustain and resustain them manually.」
- **译文**：「在你在这里调整之后，需要手动先关闭再重新启用这些持续技能。」
- **问题**：条件范围被扩大。原文只在「在此处重新开启光环」这个方向上要求手动关再开；「调整」把关闭方向也包括了进去。
- **源码**：`ShimmerRemoveSustains.lua:94-110` `toggleAura`
  - 隐藏方向只调用 `removeAura`，不需要任何手动操作。
  - 只有重新开启方向（`shimmer_sustains_hide[tid]=false`）才在 `not t.no_sustain_autoreset` 时，连续两次 `forceUseTalent` 自动重置。
  - 黄色名称来自 `generateList`（:155），对应 `no_sustain_autoreset`。所以手动关再开只在「黄色光环、重新开启后」才需要。
- **结论**：玩家会误以为隐藏光环之后也要手动操作。



## O004 | entry-03294

### C02 | entry-03294 | 仅建议
- 「It may explode!」译为「它随时可能出现问题！」，把原文的夸张玩笑弱化成了普通说法。警告的实际含义保留了，属于风格偏好。
- 格式标记 `#{bold}#`、`#CRIMSON#`、`#LAST#`、`#YELLOW#` 以及换行都完整保留。



## O005 | entry-03296

### C02 | entry-03296 | 存在问题

原文：“a spell selected automatically with each attack”；译文：“每次攻击时会随机施放一个法术”。

**confirmed，译文把选取写成必然施放。** `G/data/talents/techniques/magical-combat.lua:78` 的 `do_trigger` 先取得触发概率，第 86 行通过 `rng.percent(chance)` 后才建立候选并随机选择；第 124 行才执行 `forceUseTalent`。还存在资源与可用法术检查。

英文对话提示本身较简略，但明确使用的是“selected”；译文进一步作出了每次攻击都会施法的断言。



## O006 | entry-03296

### C03 | entry-03296 | 仅建议
- 原文用 `'Random spells'` 引号标出界面选项，译文「如果你选择随机法术」去掉了引号。选项文本「随机法术」（context.lua:55）仍能对应上，信息没有丢失。
- 「with each attack」译为「每次攻击时会随机施放」，这是沿袭上游的表述。该选项自己的说明是「Each time Arcane Combat is triggered」（MagicalCombatArcaneCombat.lua:139），上游措辞本身就不严谨，不算翻译新增的错误。



## O007 | entry-03299

### C02 | entry-03299 | 存在问题

原文在欢迎来到 *Maj’Eyal* 后称“**This is the Age of Ascendancy**”；译文称“现在的**埃亚尔大陆**是卓越纪”。`init.lua:131` 明确区分 Eyal 世界与 Maj’Eyal 大陆，“埃亚尔大陆”混淆两者。状态：已证实。



## O008 | entry-03299

### C03 | entry-03299 | 存在问题

“**over ten thousand years**”译为“长达一万年”，丢失“超过”的数量界限。依据：`init.lua:30`。状态：已证实。



## O009 | entry-03299

### C03 | entry-03299 | 存在问题

原文：“over ten thousand years”；译文：“长达一万年”。

**confirmed，数量下限遗漏。** 冻结条目第二段及 `G/init.lua:30` 明确表示超过一万年，译文只给出一万年这一时长。



## O010 | entry-03299

### C04 | entry-03299 | 存在问题

“**ruled … with fairness**”译为“王国天下太平”：和平不等于公正施政，后者的信息未保留。依据：`init.lua:33–34`。状态：已证实。



## O011 | entry-03299

### C04 | entry-03299 | 存在问题

原文：“The last effects … have been tamed”；译文：“所造成的影响已经渐渐减轻”。

**confirmed，灾害控制状态发生变化。** `G/init.lua:31` 表示最后的残余影响已经得到控制；译文表示影响逐渐减轻，遗漏“最后残余”及已被控制的结果状态。后句的大地缓慢恢复不能替代这项信息。



## O012 | entry-03299

### C04 | entry-03299 | 存在问题
- **原文**：「This is the Age of Ascendancy.」
- **译文**：「现在的埃亚尔大陆是卓越纪。」
- **问题**：新增了「埃亚尔大陆」，把 Eyal 说成了大陆。同包上下文（context.lua:153）明确写着「Maj'Eyal is the biggest continent in the world of Eyal」，Eyal 是世界，不是大陆。这是翻译新增的地理事实错误。



## O013 | entry-03299

### C05 | entry-03299 | 存在问题

原文：“ruled the kingdoms with fairness”；译文：“王国天下太平”。

**confirmed，治理方式被替换。** `G/init.lua:34` 说明两位统治者公平治理；“天下太平”描述社会安定，没有保留公平性，也不能从原句推出。



## O014 | entry-03299

### C05 | entry-03299 | 存在问题

法师帮助结束的是“**the terrors of the Spellblaze**”，译文却说他们“终止了……魔法大爆炸”，将灾难造成的恐怖后果改成事件本身。依据：`init.lua:42`。状态：已证实。



## O015 | entry-03299

### C05 | entry-03299 | 存在问题
- **原文**：「After over ten thousand years of strife」
- **译文**：「在长达一万年的冲突痛苦和混乱之后」
- **问题**：丢掉了「over」（超过）这个数量限定，「长达一万年」读起来像是恰好一万年。



## O016 | entry-03299

### C06 | entry-03299 | 存在问题
- **原文**：「The last effects of the Spellblaze have been tamed.」
- **译文**：「所造成的影响已经渐渐减轻」
- **问题**：原文是「最后残余的影响已被平息」，表示已经完成。译文变成了「正在逐渐减轻」的进行态，「last」（最后残余的）也丢了。时序和完成状态都被改变。



## O017 | entry-03299

### C07 | entry-03299 | 存在问题
- **原文**：「Together they ruled the kingdoms with fairness」
- **译文**：「在他们的统治下，王国天下太平」
- **问题**：「公正地统治」被换成了「天下太平」，统治者「公正」这一信息丢失。



## O018 | entry-03299

### C08 | entry-03299 | 待确认
- 「under the leadership of Aranion Gayaeil」译为「在精灵王艾伦尼恩·加威尔的统治下」，新增了「精灵王」这个头衔。
- 本包允许读取的材料里没有证据证明该人物的头衔。缺少 lore 或 NPC 定义源码作证据。



## O019 | entry-03299

### C09 | entry-03299 | 仅建议
- 「healing the wounds of thousands of years of conflict」译为「所有的文明在过去数千年中经历的不幸正在好转」，是意译：「冲突」泛化为「不幸」，并加了「所有的」。主旨没变，属于措辞偏好。
- 「冲突痛苦和混乱」之间缺少顿号，属于排版问题。
- 颜色码 `#FF0000#…#WHITE#`、`#14fffc#…#ffffff#` 完整保留。



## O020 | entry-03300

### C01 | entry-03300 | 存在问题
- **原文引据**：`...giving you the opportunity to tactically reposition or finish them off at less risk.`
- **译文引据**：`...为你制造机会重新占位，或以更低的风险将其解决。`
- **具体问题**：
  1. “占位”（意为占据席位/空间，如占位符）属于“站位”（战斗中的走位/站立位置）的别字与词义错位；
  2. 漏译修饰副词 "tactically"（战术性地 / 战术走位）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/init.lua:87`（`load_tips`）。该提示在加载界面向玩家阐述核心战斗走位机制，同文件 line 88 明确强调战术走位（"seek the position of greatest tactical advantage... 调整你的走位以保持你的优势"），此处“重新占位”用字不当且丢失战术修饰。

---



## O021 | entry-03300

### C06 | entry-03300 | 仅建议

“tactically reposition”译作“重新占位”仍能传达调整位置，但搭配略生硬；这是表达偏好，没有可证的信息错误。依据：`init.lua:87`。



## O022 | entry-03305

### C07 | entry-03305 | 存在问题

“**drive people to necromancy**”指驱使人研习或施行死灵术；“使一个人成为死灵法师”缩窄为取得某种职业身份。依据：`init.lua:96`。状态：已证实。



## O023 | entry-03306

### C10 | entry-03306 | 存在问题
- **原文**：「The Spellblaze tore Eyal apart」
- **译文**：「撕裂了埃亚尔大陆」
- **问题**：同 C04，把 Eyal（世界）说成了大陆，证据同样是 context.lua:153。
- 原文开头有一个不成对的 `"`，译文去掉了。这是上游残留，不计为缺陷。



## O024 | entry-03309

### C02 | entry-03309 | 存在问题
- **原文引据**：`Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.`
- **译文引据**：`虽然有人说还能在某些隐秘之地找到夏·图尔的神器，但据说不可轻慢它们。`
- **具体问题**：主干语法与事实定性错误。原文主干为客观陈述事实："Some Sher'Tul artifacts [主语] can still be found in hidden places [谓语/状语]"（某些夏·图尔神器仍可在隐秘之处找到），后半句才引入传闻定性 "but it is said they are not to be trifled with"（但据说不可轻慢它们）。译文将主语限定词 "Some"（某些/部分）误解为 "Some [say]"（有人说），强行增添“虽然有人说...”，将客观事实描述改写为让步传闻从句，且导致前后文出现累赘的传闻表述（“虽然有人说...但据说...”）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/init.lua:102`（`load_tips`）。世界观与探索事实提示。

---



## O025 | entry-03309

### C06 | entry-03309 | 存在问题

原文：“Some Sher'Tul artifacts can still be found”；译文：“虽然有人说还能……找到夏·图尔的神器”。

**confirmed，事实陈述被降为传闻。** `G/init.lua:102` 的传闻限定“it is said”只修饰不可轻率对待神器的警告。译文额外把神器仍可发现这一陈述也归为“有人说”。



## O026 | entry-03309

### C08 | entry-03309 | 存在问题

原文肯定仍可找到某些夏·图尔神器，传闻所修饰的是“**they are not to be trifled with**”；译文“虽然有人说还能……找到”把可找到一事也改为传闻。依据：`init.lua:102`。状态：已证实。



## O027 | entry-03309

### C11 | entry-03309 | 存在问题
- **原文**：「Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.」
- **译文**：「虽然有人说还能在某些隐秘之地找到……但据说不可轻慢它们。」
- **问题**：前半句在原文里是直接断言，译文加了「有人说」，改成了传闻。只有后半句才是原文的「it is said」，前半句的确定程度被改变。



## O028 | entry-03317

### C07 | entry-03317 | 存在问题

原文：“Sandals or boots”；译文：“鞋子”。

**confirmed，具体装备种类遗漏。** `G/load.lua:131` 将这段文字注册为 `FEET` 装备栏说明，明确列出凉鞋和靴子。译文保留穿戴部位，但丢失了两个具体种类；这是信息泛化，不只是措辞偏好。



## O029 | entry-03317

### C08 | entry-03317 | 仅建议
- **原文引据**：`Sandals or boots can be worn on your feet.`
- **译文引据**：`你的脚上可以穿上鞋子。`
- **具体原因**：原文在部位说明中具体列出 "Sandals or boots"（凉鞋或靴子）。译文概括为“鞋子”，虽符合脚部槽位（`FEET`）常理且无游戏机制误导，但若偏好与同组头部部位（line 128 `HEAD` "helmets or crowns" 译为“头盔或王冠”）保持相同细致度，建议还原为“凉鞋或靴子”。此项纯属表述精度偏好，不记作缺陷。
- **状态**：仅建议
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:131`（`ActorInventory:defineInventory("FEET", ...)`）。

---



## O030 | entry-03317

### C09 | entry-03317 | 存在问题

原文明确列出“**Sandals or boots**”，译文仅称“鞋子”，抹去了脚部栏说明中的两类物品。依据：`load.lua:131` 的 `FEET` 栏定义。状态：已证实。



## O031 | entry-03317

### C12 | entry-03317 | 仅建议
- 「Sandals or boots」泛化为「鞋子」。这是 FEET 栏说明（load.lua:131），「脚部装备栏」这个作用对象没错，只是例举丢了，属于措辞偏好。



## O032 | entry-03319

### C08 | entry-03319 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** `G/load.lua:135` 的英文已经写成 X；固定版本 `E/data/keybinds/inventory.lua:66` 定义 `QUICK_SWITCH_WEAPON` 的默认绑定为 `sym:=q:false:false:false:false`。

`G/load.lua:114` 加载 inventory 键位定义；同版本不存在模块侧 `G/data/keybinds/inventory.lua` 覆盖文件。问题是默认按键说明失实，不是译文大小写错误。



## O033 | entry-03320

### C09 | entry-03320 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** 本条对应 `G/load.lua:136` 的第二套副手说明；默认切换动作仍由 `E/data/keybinds/inventory.lua:66` 绑定至 Q。副手装备及技能条件部分未发现问题。



## O034 | entry-03321

### C10 | entry-03321 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** 本条对应 `G/load.lua:137` 的第二套灵能聚焦物说明；默认切换动作同样绑定至 Q，证据为 `E/data/keybinds/inventory.lua:66`。念动力持物及增益用途部分未发现问题。



## O035 | entry-03322

### C11 | entry-03322 | 存在问题

原文：“instantly used”；译文：“即时使用（不消耗回合）”。

**confirmed，译文增加了不成立的统一免耗时解释；上游措辞也有误导性。**

`G/data/talents/uber/dex.lua:117` 的 `no_energy=true` 属于无影手技能自身。其 action 在第 132 行调用 `playerUseObject`，后者在 `G/class/Player.lua:1483` 调用物品的 `use`。

`G/class/Object.lua:338` 只有在物品 `use_no_energy` 或使用结果 `ret.no_energy` 成立时才免耗时，否则调用 `useEnergy`。`use_talent` 分支在第 278 行读取的是物品所施放技能的 `no_energy`。无影手的物品栏初始化也没有统一设置零耗时。

因此物品是否耗时仍由其自身决定，不能统一解释为“不消耗回合”。



## O036 | entry-03322

### C13 | entry-03322 | 待确认
- 「instantly used by swift hands」译为「可即时使用（不消耗回合）」，括号里新增了一条机制说明。
- 已读源码只有 `load.lua:139` 定义 SWIFT_HANDS 栏位，看不到消费该栏位的技能怎么处理行动耗时。
- 本包允许的调用链里没有可追的文件，所以「不消耗回合」是否准确待确认。



## O037 | entry-03323

### C03 | entry-03323 | 存在问题
- **原文引据**：`...and are few in number since the Cataclysm tore much of their land into the sea.`
- **译文引据**：`...自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。`
- **具体问题**：专有名词与世界历史事实混淆。原文为 "since the Cataclysm tore much of their land into the sea"，译文将其中的 "the Cataclysm"（大灾变）误译为“大爆炸”（即 Spellblaze，魔法大爆炸）。在 ToME 历史设定中，"Spellblaze"（魔法大爆炸）与数个世纪后导致大陆东南部崩塌沉海的 "Cataclysm"（大灾变）是两个不同的独立历史大事件（在 `game/modules/tome/init.lua:132` 明确区分：“The effects of the Spellblaze were not all instant, and many centuries later the Cataclysm tore the continent apart once more...”）。将 Cataclysm 译为“大爆炸”严重混淆了游戏核心历史线。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:244`（人类手札 Lore 第三段）。

---



## O038 | entry-03323

### C10 | entry-03323 | 存在问题

“**the Cataclysm**”译为“大爆炸”，与同批文本中 *Spellblaze* 的“魔法大爆炸”混淆。`misc.lua:376` 指灾变使肖尔塔土地沉海；`init.lua:131–132` 也分别提到 Spellblaze 与 Cataclysm。状态：已证实。



## O039 | entry-03323

### C11 | entry-03323 | 存在问题

少数马卓普人据传仍“**possess citadels and towers**”，译文改为“仍住在……城堡或高塔里”。拥有与居住不是同一关系。依据：`misc.lua:378`。状态：已证实。



## O040 | entry-03323

### C12 | entry-03323 | 存在问题

原文：“the Cataclysm”；译文：“大爆炸”。

**confirmed，译文给灾变加入了爆炸性质，并模糊了两个事件的区别。** 冻结条目第三段指土地沉海的 Cataclysm。`G/init.lua:132` 明确将其描述为魔法大爆炸数百年后再次撕裂大陆的灾变；第 131 行也将 Spellblaze 与 Cataclysm 并列。现有证据没有将后者定义为一次爆炸。

这项判断依据事件语境，不要求建立新的全局术语译名。



## O041 | entry-03323

### C13 | entry-03323 | 存在问题

原文：“are few in number since”；译文：“数量急剧减少”。

**confirmed，人口状态被改成带速度的变化过程。** 冻结条目第三段说明灾变后肖尔塔人数量稀少，没有说明人口减少的速度。“急剧”是译文新增判断，而当前数量稀少的状态也未直接保留。



## O042 | entry-03323

### C14 | entry-03323 | 存在问题
- **原文**：「few in number since the Cataclysm tore much of their land into the sea」
- **译文**：「自从大爆炸将他们大部分土地沉入海洋后」
- **问题**：Cataclysm（大灾变）被译成「大爆炸」，和 Spellblaze（魔法大爆炸）混淆了。同包 context.lua:153-154 把 Cataclysm 译作「大灾变」，并写明它发生在魔法大爆炸「数个世纪之后」，是两次不同的事件。



## O043 | entry-03323

### C15 | entry-03323 | 存在问题
- **原文**：「A few are rumoured to still possess citadels and towers in remote locations.」
- **译文**：「有部分传言说他们仍住在……」
- **问题**：
  - 原文的主体是「少数马卓普人」，译文变成了「部分传言」，并说「他们」全体，数量范围被改变。
  - 「possess」（拥有）变成了「住在」。



## O044 | entry-03323

### C16 | entry-03323 | 仅建议
- 末段「勇者图库纳国王统一了所有的人类王国，并仍然掌控于他的儿子……手中」主语衔接不通顺，但意思能还原。
- 「arcane experiments」只译成「实验」。
- Conclave 这里译作「秘法会」，而同包 context.lua:136 用的是「孔克雷夫」。术语快照未收录该词，不构成术语缺陷。
- 以上都只记为建议。



## O045 | entry-03324

### C04 | entry-03324 | 存在问题
- **原文引据**：`No text would be complete without at least a brief note of some of the more brutish races which infest our world.`
- **译文引据**：`没有任何文字可以诠释那些影响我们世界的野蛮种族。`
- **具体问题**：宏观句意完全颠倒。原文为常见的总述修辞句式“如果不简要记录...任何著述都是不完整的”，旨在表达作者必须在本书中对这些野蛮种族作一番记载；译文误解为“没有任何文字可以诠释...”，将必然加以记录的陈述逆转为不可言说的感叹，语义严重失真；且将 "infest"（侵扰、滋生于）弱化误译为“影响”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第一段）。

---



## O046 | entry-03324

### C05 | entry-03324 | 存在问题
- **原文引据**：`They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons...`
- **译文引据**：`他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名...`
- **具体问题**：关键叙事机制信息遗漏并错译。原文明确指出森林巨魔相比山地巨魔具有更高级的言语/语言表达形式（"a more advanced form of speech"），随后才说明移动更快（"move faster"）。译文将 "a more advanced form of speech" 错译为“更为敏捷的速度”，不仅彻底丢失了森林巨魔语言能力的叙事设定，还与后半句“以移动迅速...闻名”造成完全重复；此外该段首句“岩石巨魔生存与东北部的山脉地区”中“生存与”存在别字（应为“生存于”）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第二段）。

---



## O047 | entry-03324

### C06 | entry-03324 | 存在问题
- **原文引据**：`Records of them exist only from the last few hundred years...`
- **译文引据**：`有关他们的记载只有近一百年的...`
- **具体问题**：时间尺度数量级翻译错误。原文为 "the last few hundred years"（近几百年 / 过去数百年），译文误译为“近一百年”，时间跨度被缩减为一个世纪。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第四段，关于娜迦族的记载历史）。

---



## O048 | entry-03324

### C07 | entry-03324 | 存在问题
- **原文引据**：`...metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness.`
- **译文引据**：`...金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。`
- **具体问题**：恶魔生理反应机制曲解。原文描述的是恶魔独特的金属血肉在接触埃亚尔大陆大气时产生的奇异反应（"react oddly with our atmosphere"），并主动释放酸液或喷吐黑暗浓雾（"release hideous acids or belching clouds of darkness"）。译文将其曲解为“表现出超乎我们想象的形态”，并将主动释放酸液/浓云篡改为被动掩藏“藏在酸雾里或是可怕的黑暗中”，严重背离原作设定的恶魔生理机制叙事。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第五段）。

---



## O049 | entry-03324

### C12 | entry-03324 | 存在问题

“**No text would be complete without at least a brief note**”是说文章应简述这些种族；“没有任何文字可以诠释”变成文字无法描述，开篇论点反转。依据：`misc.lua:497`。状态：已证实。



## O050 | entry-03324

### C13 | entry-03324 | 存在问题

“**do not hold any civilised society of note**”谈的是没有值得一提的文明社会；“没有任何文化遗留”改成没有文化遗存。依据：`misc.lua:497`。状态：已证实。



## O051 | entry-03324

### C14 | entry-03324 | 存在问题

原文：“No text would be complete without at least a brief note”；译文：“没有任何文字可以诠释”。

**confirmed，开篇逻辑改变。** 冻结条目第一段说明完整著述应至少简述这些种族；译文却表示文字无法诠释它们，将“必须提及”变成“无法描述”。



## O052 | entry-03324

### C14 | entry-03324 | 存在问题

岩石巨魔有“**a thick, solid hide**”，其外观像煤或花岗岩；译文只说“厚厚的……外观”，漏掉厚实外皮这一身体特征。依据：`misc.lua:499`。状态：已证实。



## O053 | entry-03324

### C15 | entry-03324 | 存在问题

原文：“do not hold any civilised society of note”；译文：“没有任何文化遗留”。

**confirmed，描述对象变化。** 第一段讨论这些种族是否具有值得一提的文明社会；“文化遗留”讨论文化遗产或遗存。社会组织状态的信息没有保留。



## O054 | entry-03324

### C15 | entry-03324 | 存在问题

森林巨魔有更成熟的“**form of speech**”，译文对应位置说“更为敏捷的速度”，把语言能力误作速度；原文随后才另说它们移动更快。依据：`misc.lua:499`。状态：已证实。



## O055 | entry-03324

### C16 | entry-03324 | 存在问题

兽人训练巨魔发生在“**towards the end of the Age of Pyre**”；译文仅称“在烈火纪时”，丢失接近纪元末期的时点。依据：`misc.lua:499`。状态：已证实。



## O056 | entry-03324

### C16 | entry-03324 | 存在问题

原文：“a thick, solid hide”；译文：“厚厚的煤黑色或花岗岩状的外观”。

**confirmed，身体结构信息遗漏。** 第二段说明石巨魔具有厚实坚固的皮肤，其外观类似煤或花岗岩。译文把“厚厚的”接到“外观”，没有明确保留厚实坚固的皮肤这一特征。



## O057 | entry-03324

### C17 | entry-03324 | 存在问题

原文：“a more advanced form of speech”；译文：“更为敏捷的速度”。

**confirmed，语言能力误译成速度。** 第二段先比较森林巨魔与山地同类的语言能力，再另述移动更快。译文连续描述速度，遗漏了语言更发达这一独立特征。



## O058 | entry-03324

### C17 | entry-03324 | 存在问题

娜迦记载始于“**the last few hundred years**”，译文称“近一百年”，时间跨度由数百年缩为约一百年。依据：`misc.lua:503`。状态：已证实。



## O059 | entry-03324

### C17 | entry-03324 | 存在问题
- **原文**：「No text would be complete without at least a brief note of some of the more brutish races which infest our world.」
- **译文**：「没有任何文字可以诠释那些影响我们世界的野蛮种族。」
- **问题**：句义被颠倒。原文说「任何著述都少不了简述这些种族」，译文说成了「无法诠释它们」。



## O060 | entry-03324

### C18 | entry-03324 | 存在问题

原文说这些记载“**only more recently have … been interpreted**”为真实记录；译文说“越来越多的证据表明”，把解释方式的变化改成证据数量增长。依据：`misc.lua:503`。状态：已证实。



## O061 | entry-03324

### C18 | entry-03324 | 存在问题

原文：“towards the end of the Age of Pyre”；译文：“在烈火纪时”。

**confirmed，时代内的时间限定遗漏。** 第二段将兽人训练巨魔的时间限定在烈火纪接近结束时，译文扩大到了整个时代。



## O062 | entry-03324

### C18 | entry-03324 | 存在问题
- 同段还有三处偏差：
  - 「do not hold any civilised society of note」译为「没有任何文化遗留」，把「文明社会」换成了「文化遗留」。
  - 「nor … seem capable」中的「seem」没译，推测被说成了定论。
  - 「of interest to study for any who take delight in analysing…」译为「仍能激起大家研究……的兴趣」，把特定读者群扩大成了「大家」。



## O063 | entry-03324

### C19 | entry-03324 | 存在问题

原文：“their tails extend several feet further”；译文：“他们的尾巴可能更长”。

**confirmed，确定的长度关系变成不确定描述。** 第四段说明陆地站立高度约六英尺，尾巴还延伸数英尺。译文既遗漏“数英尺”，又加入原文没有的“可能”。



## O064 | entry-03324

### C19 | entry-03324 | 存在问题

恶魔“**can be summoned by certain magical rites**”说的是可被某些仪式召唤；“他们是由某种魔法仪式召唤而来”将召唤能力写成其来源。依据：`misc.lua:505`。状态：已证实。



## O065 | entry-03324

### C19 | entry-03324 | 存在问题
- **原文**：「They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster」
- **译文**：「他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速……闻名」
- **问题**：「更发达的语言能力」被错译成「速度」。语言信息丢失，速度信息重复出现。



## O066 | entry-03324

### C20 | entry-03324 | 存在问题

原文：“the last few hundred years”；译文：“近一百年”。

**confirmed，时间数量错误。** 第四段的数百年被缩短为一百年。



## O067 | entry-03324

### C20 | entry-03324 | 存在问题

金属化血肉会与“**our atmosphere**”异常反应，部分恶魔会释放酸或黑暗云雾；译文改成“超乎我们想象的形态”“藏在酸雾里”，遗漏大气反应，并将主动释放改为置身其中。依据：`misc.lua:505`。状态：已证实。



## O068 | entry-03324

### C20 | entry-03324 | 存在问题
- **原文**：「a thick, solid hide which bears the appearance of coal or granite」
- **译文**：「厚厚的煤黑色或花岗岩状的外观」
- **问题**：「hide」（外皮）这个主体丢了，变成了「厚厚的外观」。
- 同句前面还有两处小偏差：「生存与东北部」错把「于」写成「与」；「many mountain chains」中的「many」丢失。



## O069 | entry-03324

### C21 | entry-03324 | 存在问题

“**magic has fallen out of use**”指魔法较少被使用；“魔法淡出人们的视野”说的是较少被看见，改变恶魔减少所关联的条件。依据：`misc.lua:505`。状态：已证实。



## O070 | entry-03324

### C21 | entry-03324 | 存在问题

原文：“only more recently have they been interpreted as more than … fantasies”；译文：“越来越多的证据表明他们并不是……幻觉”。

**confirmed，认识转变的时间信息被替换。** 第四段说明直到较近时期，人们才不再把相关记载视为醉酒水手的幻想。译文改成证据数量持续增加，没有保留“直到较近时期才”的限制。



## O071 | entry-03324

### C21 | entry-03324 | 存在问题
- **原文**：「towards the end of the Age of Pyre many were trained as fighters by the orcs」
- **译文**：「然而在烈火纪时，他们被兽人当做战士般训练」
- **问题**：「烈火纪末期」这个时间点丢了；「many」（许多）变成了泛指全体。
- 另外「as they are colloquially known」被误解成「因为这更加通俗地为人所知」，多出了一个原文没有的因果关系。



## O072 | entry-03324

### C22 | entry-03324 | 存在问题

原文：“formed from layers of thick shark-hide”；译文：“用鲨鱼皮制成”。

**confirmed，材料结构遗漏。** 第四段明确描述多层厚鲨鱼皮，译文只保留材质，没有保留层叠结构和厚度。



## O073 | entry-03324

### C22 | entry-03324 | 存在问题
- **原文**：「Records of them exist only from the last few hundred years」
- **译文**：「有关他们的记载只有近一百年的」
- **问题**：数量错误，「几百年」被译成了「近一百年」。



## O074 | entry-03324

### C23 | entry-03324 | 存在问题

原文：“supported by certain studies by Shaloren archmages”；译文：“由永恒精灵魔导师们得出的”。

**confirmed，研究支持关系变成理论提出关系。** 第五段只说这些研究支持主要理论，没有说明该理论由这些法师提出或得出。译文改变了证据来源与观点归属的关系。



## O075 | entry-03324

### C23 | entry-03324 | 存在问题
- **原文**：「though their tails extend several feet further」
- **译文**：「尽管他们的尾巴可能更长」
- **问题**：「再长出几英尺」的具体数量丢了，还新增了原文没有的「可能」。



## O076 | entry-03324

### C24 | entry-03324 | 存在问题

原文：“react oddly with our atmosphere”；译文：“表现出超乎我们想象的形态”。

**confirmed，与埃亚尔大气发生反应的信息遗漏。** 第五段将异常现象与血肉、皮肤接触当地大气联系起来；译文改为一般的奇异外形描述，丢失环境作用关系。



## O077 | entry-03324

### C24 | entry-03324 | 存在问题
- **原文**：「which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness」
- **译文**：「可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中」
- **问题**：
  - 「与我们的大气发生异常反应」这一因果丢失。
  - 「释放酸液、喷出黑暗云雾」这个主动行为被改成「藏在里面」，行为方向错了。



## O078 | entry-03324

### C25 | entry-03324 | 存在问题

原文：“release hideous acids or belching clouds of darkness”；译文：“藏在酸雾里或是可怕的黑暗中”。

**confirmed，释放行为误成藏身状态。** 第五段说恶魔释放酸液或喷吐黑暗云团；译文表示恶魔躲藏在酸雾或黑暗中，改变了行为及其作用关系。



## O079 | entry-03324

### C25 | entry-03324 | 存在问题
- **第一处**：「they can be summoned by certain magical rites」译为「他们是由某种魔法仪式召唤而来」。原文是「可以被召唤」（可能性），译文成了对来源的断言。
- **第二处**：「The main theory, which is supported by certain studies by Shaloren archmages」译为「由永恒精灵魔导师们得出的」。原文说研究「支持」这个理论，译文改成理论由他们「得出」，归属关系变了。
- 以下只记为建议，不计缺陷：
  - Naga 段「craft weapons and armour from materials found on the sea-bed」的层次被合并。
  - 「communication… impossible」加了「几乎」。
  - 巨人段「seem」没译，「Daikara Pass」只写作「岱卡拉」。
  - 「臭名卓著」应为「臭名昭著」，是错字。



## O080 | entry-03324

### C26 | entry-03324 | 存在问题

原文：“attacking communities”；译文：“攻击市民”。

**confirmed，攻击对象被缩小。** 第三段讨论巨人下到低地袭扰人类聚落，与偷走农场动物并列；译文改为攻击市民个人，没有保留聚落或社区这一对象。



## O081 | entry-03325

### C22 | entry-03325 | 存在问题

“**unless hefty bribes are paid**”要求数额可观的贿赂；“除非你给他们点好处”既弱化数额，也不再明确是贿赂。依据：`misc.lua:403`。状态：已证实。



## O082 | entry-03325

### C23 | entry-03325 | 存在问题

“**for no known reason**”是外人不知道原因；“无缘无故”断言没有原因。依据：`misc.lua:403`。状态：已证实。



## O083 | entry-03325

### C24 | entry-03325 | 存在问题

作者获准与数位“**guild leaders**”交谈；“主要领导人”遗漏其公会领袖身份。依据：`misc.lua:403`。状态：已证实。



## O084 | entry-03325

### C25 | entry-03325 | 存在问题

“**resistant to any physical suffering**”描述能承受身体痛苦；“超强的物理抵抗能力”将其表述成抵抗物理伤害的能力。依据：`misc.lua:405`。状态：已证实。



## O085 | entry-03325

### C26 | entry-03325 | 存在问题

原文明确说可凭胡须上的珠饰识别**女性矮人**；“他们的性别……可以通过……珠饰来辨认”未说明珠饰识别的是女性。依据：`misc.lua:405`。状态：已证实。



## O086 | entry-03325

### C26 | entry-03325 | 存在问题
- **原文**：「speaking with several of their guild leaders」
- **译文**：「并有幸与他们的主要领导人对话」
- **问题**：「几位公会首领」被改成「主要领导人」。这与本文第三段「谁实际担任名义领袖，外人不得而知」以及 03299「not even their leader's name」直接矛盾，属于事实错误。



## O087 | entry-03325

### C27 | entry-03325 | 存在问题

“**allow no outsiders in**”是通常不准外人入城；“从不欢迎外来者”只表示态度，不再表达准入限制。前文作者获特准入城是原文写出的例外。依据：`misc.lua:403,409`。状态：已证实。



## O088 | entry-03325

### C27 | entry-03325 | 存在问题

原文：“unless hefty bribes are paid”；译文：“除非你给他们点好处”。

**confirmed，程度信息失真。** 第一段明确要求相当可观的贿赂，“点好处”却弱化为少量利益，改变了矮人透露自身信息的条件程度。



## O089 | entry-03325

### C27 | entry-03325 | 存在问题
- **原文**：「unless hefty bribes are paid」
- **译文**：「除非你给他们点好处」
- **问题**：程度被弱化。「重金贿赂」变成了「给点好处」。



## O090 | entry-03325

### C28 | entry-03325 | 存在问题

原文说有“大量年轻矮人”外出，没有增长趋势；译文“**越来越多**的年轻矮人”增加了趋势判断。依据：`misc.lua:411`。状态：已证实。



## O091 | entry-03325

### C28 | entry-03325 | 存在问题

原文：“for no known reason”；译文：“无缘无故”。

**confirmed，未知原因被改成没有原因。** 第一段只限定外界不知道断绝联系的原因，译文作出了客观上没有缘由的判断。



## O092 | entry-03325

### C28 | entry-03325 | 存在问题
- **原文**：「They trade heavily in their crafts from their capital the Iron Throne, but allow no outsiders in」
- **译文**：「他们在首都——钢铁王座中进行大量的交易，但是从不欢迎外来者」
- **问题**：
  - 原文是「以首都为基地向外输出货物」，译文变成「在首都里交易」，与「不许外人进入」自相矛盾。
  - 「不允许进入」被弱化成了「不欢迎」。



## O093 | entry-03325

### C29 | entry-03325 | 存在问题

原文：“several of their guild leaders”；译文：“他们的主要领导人”。

**confirmed，人物所属机构和数量信息遗漏。** 第一段明确是数位公会领袖；译文没有保留公会身份，并添加“主要”这一地位判断。后文公会委员会语境也不能补回会面对象的具体身份。



## O094 | entry-03325

### C29 | entry-03325 | 存在问题
- **原文**：「Their skill with metal is renowned above all else.」
- **译文**：「他们对金属的加工技艺也是举世闻名的。」
- **问题**：「最负盛名、居于其他一切之上」这个比较级丢了，变成了并列的「也」。



## O095 | entry-03325

### C30 | entry-03325 | 仅建议
- 「for no known reason」译为「无缘无故」，原意是「原因不明」，语气略有偏移。
- 「a great deal of young dwarves」译为「越来越多的年轻矮人」，加入了原文没有的增长趋势。
- 两处都影响不大，记为建议。



## O096 | entry-03325

### C30 | entry-03325 | 存在问题

原文：“Their females … can usually be identified by the beads”；译文：“他们的性别……可以通过……珠饰来辨认”。

**confirmed，识别标志与女性的对应关系遗漏。** 第二段告诉读者珠饰通常用于识别女性；译文只说珠饰可辨性别，没有说明该标志对应女性。



## O097 | entry-03325

### C31 | entry-03325 | 存在问题

原文：“allow no outsiders in”；译文：“从不欢迎外来者”。

**confirmed，准入禁令被弱化为态度。** 第四段说明不准外人进入，因此派商队到外界售卖；不欢迎外人并不等于禁止进入，改变了限制性质。



## O098 | entry-03325

### C32 | entry-03325 | 存在问题

原文：“a great deal of young dwarves who venture”；译文：“越来越多的年轻矮人更加倾向于……出去冒险”。

**confirmed，新增数量增长及偏好增强趋势。** 第五段只说明有很多年轻矮人外出冒险；原文没有前后比较，也没有数量持续增加或意愿增强的判断。



## O099 | entry-03326

### C29 | entry-03326 | 存在问题

奎科加任命的是自己的“**librarians**”，译文只称“记录者”，丢失图书管理员身份；紧接着的“这个图书馆”因此也少了对应依据。依据：冻结 `INPUT.md` 的 entry-03326 原文、译文。此项是文本语义判断，不据此断言游戏机制。状态：已证实。



## O100 | entry-03326

### C33 | entry-03326 | 存在问题

原文：“appointing its own librarians”；译文：“指派了自己的记录者”。

**confirmed，具体身份遗漏。** 第一段说明被任命者是图书管理员，随后立即讨论该图书馆是否存在。“记录者”保留了他们记录故事的工作，却没有保留其与图书馆相联系的具体身份。



## O101 | entry-03327

### C09 | entry-03327 | 待确认
- **原文引据**：`Logs written to %s`
- **译文引据**：`日志目录：%s`
- **具体疑点**：原文 "Logs written to %s" 为被动动作句（日志已写入 %s）。译文处理为偏正名词结构“日志目录：%s”，预设了 `%s` 传入的一定是目录路径。若运行时该格式化占位符传入的是具体日志文件名或文件绝对路径（如 `arrange_text.log`），则显示为“日志目录：.../arrange_text.log”存在属性描述错位。
- **证据缺口**：该条目所属 section 为 `tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua`，对应组件为 `addon-dev`，已明确列于 `source-access.json` 的 `unavailable_components`（源码缺失）。无法通过源码调用链核验 `%s` 实际传入的实参类型（目录还是具体文件）。依规则“缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认”，将此疑点标记为待确认。
- **状态**：待确认
- **源码路径与消费逻辑**：`tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua:28`（`tformat` 消费，组件源码缺失）。

---



## O102 | entry-03327

### C30 | entry-03327 | 待确认

“**Logs written to %s**”未指明 `%s` 是目录还是文件路径；“日志目录：%s”断言它是目录。`source-access.json` 将 addon-dev 列为源码不可用；缺少调用处传入 `%s` 的路径构造证据，不能确认错误。状态：待确认。



## O103 | entry-03327

### C31 | entry-03327 | 待确认
- 「Logs written to %s」译为「日志目录：%s」，把 `%s` 断定为目录。
- addon-dev 组件在 unavailable_components 中，没有源码，无法核实 `%s` 实际是日志文件路径还是目录，因此待确认。
- 占位符数量和 tformat 标签都保留了，没有运行时格式问题。



## O104 | entry-03327

### C34 | entry-03327 | 待确认

原文：“Logs written to %s”；译文：“日志目录：%s”。

**pending。** 原文只说明日志写入某处，译文将 `%s` 限定为目录。需要 `tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua` 的格式化调用参数及日志写入逻辑，确认参数代表目录还是单个文件。

`source-access.json` 明确将 `addon-dev` 列为源码不可用组件，冻结邻近译文不能证明参数类型。单个 `%s` 及两行信息结构均保留，没有已证实的格式错误。



## O105 | entry-03328

### C10 | entry-03328 | 待确认
- **原文引据**：`Logs written to %s`
- **译文引据**：`日志目录：%s`
- **具体疑点**：同 C09。原文 "Logs written to %s" 译为“日志目录：%s”，预设了 `%s` 为目录；若运行时传入具体文件路径则标签不匹配。
- **证据缺口**：组件 `addon-dev` 源码缺失（属于 `unavailable_components`），无法通过源码证实 `%s` 的运行时参数类型，机制依赖疑点标记为待确认。
- **状态**：待确认
- **源码路径与消费逻辑**：`tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua:31`（`tformat` 消费，组件源码缺失）。

---



## O106 | entry-03328

### C31 | entry-03328 | 待确认

同 C30，这条“**Logs written to %s**”也译成“日志目录：%s”。缺少本条调用处的参数来源，不能确定 `%s` 的路径类型。状态：待确认。

**读取范围与核验边界：**读取了指定实验目录中的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `sources/game/modules/tome/` 下获准的 `dialogs/orders/Talents.lua`、`dialogs/shimmer/ShimmerRemoveSustains.lua`、`dialogs/talents/MagicalCombatArcaneCombat.lua`、`init.lua`、`load.lua`；五份源码的 SHA-256 均与清单相符，本体版本为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。沿 `load.lua:111` → `data/lore/lore.lua` 的明确加载关系，在该固定提交只读检查了 `data/lore/lore.lua`、其中列出的 `data/lore/misc.lua`，以及为定位奎科加文本检查的 `data/lore/angolwen.lua`、`data/lore/shertul.lua`；后两文件未定位到该段，C29 只据冻结文本判断。addon-dev 源码不可用，C30–C31 保留待确认。未创建临时文件，未读取其他报告或模型输出，未修改仓库；无已知越界。本结果是独立审核观察，不代表生产 `DONE_VERIFIED`。


## O107 | entry-03328

### C32 | entry-03328 | 待确认
- 同 C31，「日志目录：%s」的参数类型因 addon-dev 源码不可用而待确认。

---

**读取范围与越界说明**
- 读取的路径：
  - `experiments/abc20-g04-20260923/` 下的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。
  - `sources/game/modules/tome/` 下的 `dialogs/orders/Talents.lua`、`dialogs/shimmer/ShimmerRemoveSustains.lua`、`dialogs/talents/MagicalCombatArcaneCombat.lua`、`init.lua`、`load.lua`。这 5 个文件的 sha256 都与 source-access.json 核对一致，对应本体 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63。
- 没有额外读取源码，没有执行 `git show`，也没有读取 DLC 快照。
- addon-dev 组件没有源码：C31、C32 待确认；03329–03332 只按文本判断。
- 03323–03326 这几条叙事文本来自 lore 定义（load.lua:111 `PartyLore:loadDefinition`），但没有继续追读 lore 文件。这几条只按语义和同包上下文判断，C08 因此待确认。
- 没有创建临时文件或子 agent，没有修改仓库，没有读取其他报告、SPEC、STATE 或生产结论，没有越界。


## O108 | entry-03328

### C35 | entry-03328 | 待确认

原文：“Logs written to %s”；译文：“日志目录：%s”。

**pending。** 本条是重新编排完成后的另一处提示，仍需核验其独立调用点的 `%s` 参数是否为目录。该组件源码缺失，不能假定它与检查完成提示一定传入同类路径。

占位符及换行结构本身未发现问题。

---

共复核 **40 条：存在问题 13 条、待确认 2 条、仅建议 0 条、未发现问题 25 条**。全部条目的占位符和受检格式标记序列一致；上述缺陷均未提供修改方案。

实际读取范围如下。冻结包根目录为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/`

读取了该目录内：

- `INPUT.md`
- `entries.json`
- `context.lua`
- `source-access.json`
- `sources/game/modules/tome/dialogs/orders/Talents.lua`
- `sources/game/modules/tome/dialogs/shimmer/ShimmerRemoveSustains.lua`
- `sources/game/modules/tome/dialogs/talents/MagicalCombatArcaneCombat.lua`
- `sources/game/modules/tome/init.lua`
- `sources/game/modules/tome/load.lua`

五份冻结源码均与清单 SHA-256 匹配，并另外通过指定 commit 的 `git show` 确认一致。

额外源码全部通过 `/workspace/t-engine4` 的指定 commit 读取，路径及引入依据如下：

| 实际读取的额外源码路径 | 已读调用、符号或加载关系 |
|---|---|
| `G/data/talents.lua` | `G/load.lua:174` 的 `ActorTalents:loadDefinition` |
| `G/data/timed_effects.lua` | `G/load.lua:177` 的状态定义加载 |
| `G/data/lore/lore.lua` | `G/load.lua:111` 的 lore 定义加载 |
| `G/data/talents/techniques/techniques.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/talents/spells/spells.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/talents/uber/uber.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/timed_effects/physical.lua` | `data/timed_effects.lua` 的明确 `load`；核验震慑 |
| `G/data/talents/techniques/magical-combat.lua` | techniques 分类文件的明确 `load`；核验奥术格斗 |
| `G/data/talents/uber/cun.lua` | uber 分类文件的明确 `load`；查找无影手，未找到 |
| `G/data/talents/uber/dex.lua` | uber 分类文件的明确 `load`；找到并核验无影手 |
| `G/data/talents/spells/explosives.lua` | spells 分类文件的明确 `load`；核验宝石爆炸 |
| `G/data/talents/spells/stone-alchemy.lua` | spells 分类文件的明确 `load`；核验宝石镶嵌 |
| `G/class/Player.lua` | 无影手 action 调用 `playerUseObject` |
| `G/dialogs/SwiftHandsUse.lua` | 无影手 action 的明确 `require` |
| `G/class/Object.lua` | `playerUseObject` 调用物品 `o:use` |
| `G/class/Actor.lua` | Player 的明确继承引用；核验耗时处理 |
| `G/dialogs/SwiftHands.lua` | 无影手管理技能的明确 `require` |
| `E/engine/interface/ActorInventory.lua` | `load.lua` 的明确 `require` 及无影手 `initBody` 调用 |
| `E/engine/KeyBind.lua` | `load.lua` 的明确 `require`；核验键位加载路径 |
| `G/data/keybinds/tome.lua` | `load.lua` 的 `KeyBind:load` 包含 tome |
| `E/data/keybinds/inventory.lua` | 同一加载调用包含 inventory；核验默认切换键 |

另尝试读取同 commit 的 `G/data/keybinds/inventory.lua`，Git 明确返回该路径不存在；没有读取其他版本补替。

专属临时目录为 `/tmp/abc20-g04-20260923-554jakm3`，其中仅保存本次自行读取的固定版本源码副本。未读取他人临时材料、其他审核报告或当前译文文件，未创建子 agent，未修改仓库，未发生读取范围越界。

无法核验项为 C34、C35 的插件运行时参数。本包没有可读 DLC 源码，也未以本体 commit 代替 DLC 版本。本报告仅交付审核观察，不构成生产完成认证。

