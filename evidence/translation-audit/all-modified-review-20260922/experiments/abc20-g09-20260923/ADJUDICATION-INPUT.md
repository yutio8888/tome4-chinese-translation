# 匿名源码核验与归并：40 条 / 129 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方129项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好129行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03493

### C01 | entry-03493 | 待确认
- 原文 "defence cell of **the Maggot**"，译文「巨大蛆虫的防御细胞」。
- 原文大写并加定冠词，指某个特定存在；译文加了原文没有的「巨大」，把它处理成描述性名词。
- 本条 section 文件（corrupted_blobs.lua:58）里没有任何代码说明 the Maggot 指哪个区域或实体。沿调用链也找不到加载这个 npc 文件的区域文件，所以无法判断「巨大」是否有依据，也无法判断是否该与某个既定专名对齐。
- 缺的证据：定义 the Maggot 的区域或实体源码及其既定译名。



## O002 | entry-03496

### C01 | entry-03496 | 存在问题

原文“crystal pusling with nether energies”，译文“发射出虚空能量的高大水晶”。原文虽将 *pulsing* 拼错，但描述的是能量脉动；译文改成向外发射，丢失脉动这一动态特征。状态：confirmed。证据：`horror.lua:131` 的实体描述。此项不依据 `nether` 的 existing 术语要求改名。



## O003 | entry-03496

### C01 | entry-03496 | 存在问题
- **原文短引**：`A strange tall crystal pusling with nether energies.`
- **译文短引**：`一团发射出虚空能量的高大水晶。`
- **问题说明**：将 `nether energies` 错译为“虚空能量”。在 ToME4 及本 DLC（Cults of Entropy）机制与世界观中，Nether（彼世）与 Void（虚空）为两种完全不同的能量属性与技能派系（对应底层独立的 `DamageType.NETHER` 与 `DamageType.VOID`，以及 `talents/demented/nether.lua` 与 `void.lua`）。同文件 `horror.lua:31` 中的 nethergate 正确且统一地译作“彼世能量”。此处错译为“虚空能量”造成机制属性与设定的混淆。此外，“高大水晶”使用量词“一团”亦不妥。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/npcs/horror.lua:131`（实体 `bursting entropic shard` 的 `desc` 字段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O004 | entry-03496

### C02 | entry-03496 | 存在问题
- "pulsing with **nether** energies" 被译作「虚空能量」。
- 同一 section 的相邻条目中，nethergate 译「彼世之门」，"portal of nether energies" 译「彼世能量」。术语 nether→彼世，void→虚空，两者是不同的词。
- 这个实体本身的伤害类型就是 `DamageType.VOID`（horror.lua:131 之后的 combat 字段）。把 nether 译成「虚空」会让玩家混淆这两个概念，属于术语和语义错误。



## O005 | entry-03496

### C03 | entry-03496 | 存在问题
- "A **strange** tall crystal **pulsing** with…" 被译作「一团**发射出**…的高大水晶」。
- "strange"被删掉了。"pulsing"（有节律地搏动、涌动）被改成「发射」（向外射出），描写信息出错。
- 影响较低，但信息确实丢失或被改写。



## O006 | entry-03497

### C02 | entry-03497 | 存在问题

原文“a writhing mass of tentacles”，译文“大量扭曲的触须弯曲成了指环的形状”。原文说明触须正在蠕动扭动，译文仅呈现扭曲、弯成指环的形态，遗漏持续运动的特征。状态：confirmed。证据：`world-artifacts.lua:99`。



## O007 | entry-03497

### C04 | entry-03497 | 存在问题
- "**roughly** warped into the form of a ring" 被译作「弯曲成了指环的形状」。
- "roughly"（粗略地、勉强地）被删，原文说的「形状只是大致像指环」变成了「完全是指环形状」。影响较低。



## O008 | entry-03498

### C01 | entry-03498 | 存在问题

原文“the ring attunes to you”在译文中消失；译文只说首次佩戴时选择觉醒技能。调谐关系是原说明的一项独立信息。证据：`general/objects/world-artifacts.lua:104`。



## O009 | entry-03498

### C02 | entry-03498 | 存在问题
- **原文短引**：`When first worn the ring attunes to you, letting you choose a prodigy...`
- **译文短引**：`当你第一次戴上戒指的时候，选择一个觉醒技能...`
- **问题说明**：关键叙事机制从句 `the ring attunes to you`（指环与你建立调谐/共鸣）被完全漏译。译文从时间从句突兀地跳跃至祈使句“选择一个觉醒技能”，脱落了“指环与佩戴者调谐/共鸣”这一核心叙事设定信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:104`（`special_desc` 函数），对应第 205 行穿戴时的共鸣判定 `feel more attuned to...`。DLC 快照 hash 验证一致，未固定 commit。

---



## O010 | entry-03498

### C03 | entry-03498 | 存在问题

原文“the ring attunes to you”，译文直接进入“选择一个觉醒技能”。首次佩戴时戒指与佩戴者产生协调、共鸣的叙事信息被省略。状态：confirmed。证据：`world-artifacts.lua:104`。选择、不可更换和初次拒选后重新佩戴的说明仍然保留，本项不指控这些机制错误。



## O011 | entry-03498

### C05 | entry-03498 | 存在问题
- "When first worn **the ring attunes to you**, letting you choose…" 被译作「当你第一次戴上戒指的时候，选择一个觉醒技能」。
- 「指环与你相合」这一句被整句删掉。机制部分我核对过，译文是正确的：
  - 选择通过 RingOfTheHunter 对话写入 `prodigy_granted`。
  - 效果通过 `wielder.learn_talent` 实现，只在佩戴时生效。
  - 未选择时 `prodigy_granted` 为 nil，重新佩戴会再次弹出对话（world-artifacts.lua 的 on_wear；RingOfTheHunter.lua 的 `unload`）。
- 这里的缺陷只是叙事从句丢失，影响较低。



## O012 | entry-03501

### C06 | entry-03501 | 仅建议
- "willing **and able** to talk" 只译出了「愿意」，但「愿意交谈」已经隐含「能交谈」，没有实质信息损失，属于措辞偏好。



## O013 | entry-03510

### C03 | entry-03510 | 仅建议
- **原文短引**：`The %s reaches for %s with a tentacle!`
- **译文短引**：`%s使用触手抓握%s！`
- **问题说明**：现有译文占位符顺序与数量消费正确，且代码底层确实通过 `target:pull` 触发拉拽至身边。此处“使用触手抓握”表述稍显机械，若作“伸出触手抓向%s”或“伸出触手抓取%s”在中文中更为顺畅。现有译文表达清晰无事实性缺陷，本条仅属措辞表达偏好建议。
- **状态**：`advisory`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:566`（`CUT_DREM_ARM` 的 `callbackOnAct` 中的 `game.logSeen`）。

---



## O014 | entry-03511

### C04 | entry-03511 | 存在问题
- **原文短引**：`As you wear the sword you feel it attuning to your Krog body, increasing in power!`
- **译文短引**：`你感受到你的剑和克罗格的身躯共鸣，解放了强大的力量！`
- **问题说明**：遗漏了触发动作的时间条件状语 `As you wear the sword`（当你装备/佩戴此剑时），导致日志脱离了玩家即时穿戴装备的行为语境；同时第二人称所有格 `your Krog body` 被稀释并泛化为类似第三人称的“克罗格的身躯”（丢失了“你身为克罗格的身躯/你的克罗格身躯”的第二人称认同）。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:689`（`ART_PAIR_PERSEVERANCE` 的 `on_wear` 回调中的 `game.logPlayer`）。DLC 快照 hash 验证一致，未固定 commit。

---



## O015 | entry-03511

### C07 | entry-03511 | 仅建议
- "increasing in power" 被译作「解放了强大的力量」。按 on_wear，剑获得 dam +12 等加成，即「剑变强」。「解放力量」表达的意思大体相近，只是措辞偏好。



## O016 | entry-03513

### C05 | entry-03513 | 存在问题
- **原文短引**：`...you somehow do not like the idea of having so many parasitic creatures so close to your vulnerable flesh.`
- **译文短引**：`...但是让这么多寄生生物如此接近你脆弱的肉体……实在是太恶心了。`
- **问题说明**：原文核心谓语与主干为表达主角心理上的隐隐抗拒与不情愿（`you somehow do not like the idea of...`，不知怎的你并不喜欢让寄生生物贴近肉体这个念头/感到排斥），译文完全漏译了这一心理主干，而是凭空添加了主观感叹“……实在是太恶心了”，属于叙事语义信息的脱落与不当添枝加叶。此外第 2 句“上面的小蠕虫有时会从上面跳出来”存在“上面”重复累赘。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:800`（实体 `Worm Nest` 的 `desc` 字段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O017 | entry-03513

### C08 | entry-03513 | 存在问题
- 原文 "you somehow do not like the idea of having so many parasitic creatures so close…" 是克制的轻描淡写。
- 译文「……实在是太恶心了」改变了说话人的态度强度，删掉了 "somehow"（说不清为什么），还加入了原文没有的「恶心」判断，属于语义改写。



## O018 | entry-03513

### C09 | entry-03513 | 仅建议
- 「上面的小蠕虫有时会从上面跳出来」重复了「上面」，只是行文问题，不丢信息。



## O019 | entry-03514

### C04 | entry-03514 | 仅建议

原文“the two pair of shoes”，译文“这两件鞋子”。“件”作为鞋类量词不够自然，但此处也可以指两件鞋类装备；快照中确实是两个装备对象参与合并，不能据此断定数量被改成两只鞋。仅属措辞建议。证据：`world-artifacts.lua:938`、`:971–994`，合并逻辑查找并移除另一件鞋类装备，再转换当前物品。



## O020 | entry-03514

### C06 | entry-03514 | 存在问题
- **原文短引**：`As you combine the two pair of shoes you make something marvelous: %s`
- **译文短引**：`当你将这两件鞋子结合时，你制造出了神奇的道具：%s`
- **问题说明**：量词与数量概念错误。原文明确指出 `the two pair of shoes`（指慢行之鞋与快行之鞋“两双鞋”），中文鞋类量词规范应为“双”，误译为“两件”，存在明确的量词使用错误。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/general/objects/world-artifacts.lua:994`（`Shoes of Moving Slowly` 的 `use_simple` 触发合成后的 `game.logPlayer` 日志）。DLC 快照 hash 验证一致，未固定 commit。

---



## O021 | entry-03514

### C10 | entry-03514 | 仅建议
- "two pair of shoes" 被译作「两件鞋子」。量词别扭，但两件物品的含义还在，属于措辞问题。



## O022 | entry-03517

### C02 | entry-03517 | 存在问题

原文玻璃管宽到“one of our party”可进入且仍有余地；译文称“足够让我们的一个小队在里面行走”，把一名队员扩大为整支小队。证据：`lore/dremwarves.lua:58`。



## O023 | entry-03517

### C03 | entry-03517 | 存在问题

原文在该房间发现的是“Some great machine”这一台机器，后文才说明不止这一台；译文在发现时写成“一些巨大的机器”，改变了现场数量。证据：`lore/dremwarves.lua:62,66`。



## O024 | entry-03517

### C04 | entry-03517 | 存在问题

原文断液后爬出的是“feeble and half formed fetuses”；译文称“虚弱的、不成型的生命体”，遗漏“胎儿”这一与起源揭示有关的生长阶段。证据：`lore/dremwarves.lua:64`。



## O025 | entry-03517

### C05 | entry-03517 | 存在问题

原文“one of our party … with room to spare”，译文“足够让我们的一个小队在里面行走”。可容纳一名队员且有余量，被扩大成可供一个小队行走。状态：confirmed。证据：`dremwarves.lua:58`。



## O026 | entry-03517

### C05 | entry-03517 | 存在问题

原文生物“latched onto my arm”，译文确定为“在我的手臂上咬了一口”。原文只证实攀附、扣住手臂，未说明咬伤。证据：`lore/dremwarves.lua:66`。



## O027 | entry-03517

### C06 | entry-03517 | 存在问题

原文“I am not the only one”表示除叙述者外还有感染者；译文“其他人也都感染了”扩大为其余所有人。证据：`lore/dremwarves.lua:68`。



## O028 | entry-03517

### C06 | entry-03517 | 存在问题

原文“Some great machine”，译文“那是一些巨大的机器”。这里是一台连接多根玻璃管的机器；`:66` 又明确说明他们破坏的只是其中一台。译文将眼前机器改成复数。状态：confirmed。证据：`dremwarves.lua:62`、`:66`。



## O029 | entry-03517

### C07 | entry-03517 | 存在问题

原文“feeble and half formed fetuses”，译文“虚弱的、不成型的生命体”。“胎儿”这一发育阶段信息被泛化掉，而它直接参与后文对制造过程和族群起源的推断。状态：confirmed。证据：`dremwarves.lua:64`、`:72`。



## O030 | entry-03517

### C07 | entry-03517 | 存在问题

原文吞没机器的是“black growth”，译文称“黑色怪物”，把增生物确定为怪物。证据：`lore/dremwarves.lua:72`。



## O031 | entry-03517

### C07 | entry-03517 | 存在问题
- **原文短引**：`wide enough for one of our party to fit in with room to spare.`
- **译文短引**：`管径很宽，足够让我们的一个小队在里面行走。`
- **问题说明**：严重曲解叙事实体与物理尺度。`one of our party`（我们队伍中的一人/单个成员）被误译为整支“我们的小队”；`to fit in with room to spare`（容纳一人进入且尚有空余空间，描述圆柱形培养/培育管道容积）被严重曲解为“在里面行走”。结合下文事实，这些管道是浸泡、孕育单个矮人或怪物的培养管（"dwarves sleeping inside tubes"），并非供整支小队行走的巨大隧道，该误译彻底扭曲了叙事场景。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:58`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O032 | entry-03517

### C08 | entry-03517 | 存在问题

原文“my flesh wither away and turned into dried leather”，译文“我的肌肉萎缩，看起来如同晒干的皮革”。原文的肉体枯萎、皮革化被缩窄成肌肉萎缩，改变疾病表现的对象。状态：confirmed。证据：`dremwarves.lua:66`。



## O033 | entry-03517

### C08 | entry-03517 | 存在问题
- **原文短引**：`...for such a concentration of these energies simply couldn't exist on Eyal.`
- **译文短引**：`...因为这些能量根本不可能存在于埃亚尔集中出现...`
- **问题说明**：中文语序错乱与语法语病。“存在于埃亚尔集中出现”词序杂糅颠倒，且丢失了 `such a concentration of these energies`（如此高浓度的这种能量）中的核心定语信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:56`（第 3 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O034 | entry-03517

### C09 | entry-03517 | 存在问题

原文“I am not the only one … infected”，译文“其他人也都感染了”。原文仅确认还有其他感染者，译文增加全员感染的范围。状态：confirmed。证据：`dremwarves.lua:68`。



## O035 | entry-03517

### C09 | entry-03517 | 存在问题
- **原文短引**：`We wandered into the back of the room where there were yet more tubes.`
- **译文短引**：`我们徘徊到那些还有更多管子的房间里面。`
- **问题说明**：空间方位理解错误。`the back of the room` 指该大厅/房间的后部区域（深处），与前段发现培育机器的中心房间为同一房间；译文误译为“房间里面”，误导玩家以为是穿行进入了另一个独立的新房间。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/dremwarves.lua:70`（第 10 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O036 | entry-03517

### C10 | entry-03517 | 存在问题

原文“I am content with this fate”，译文“我们……却只感到充实和满足”。叙述者个人对死亡的接受，被扩展为整个队伍的共同态度。状态：confirmed。证据：`dremwarves.lua:68`。



## O037 | entry-03517

### C11 | entry-03517 | 存在问题

原文“into the back of the room”，译文“到那些还有更多管子的房间里面”。他们是在已经封闭的同一房间内走向后部，译文变成进入其他房间，丢失并改变空间关系。状态：confirmed。证据：`dremwarves.lua:66`、`:70`。



## O038 | entry-03517

### C11 | entry-03517 | 存在问题
- 原文 "such a **concentration** of these energies simply couldn't exist on Eyal"，译文「这些能量根本不可能存在于埃亚尔集中出现」。
- 这句话两个结构混在一起，语法不通，读者容易理解成「这种能量在埃亚尔根本不可能存在」。这与前文德瑞姆熟悉这种能量的说法矛盾。原文说的是「如此高的浓度」不可能存在。
- 源码位置：dremwarves.lua:52 起的 lore。



## O039 | entry-03517

### C12 | entry-03517 | 存在问题

原文“Feral Drem”，译文“原生的德瑞姆”。*Feral* 描述野生、未驯化的状态，不表示“原生”的起源身份。状态：confirmed。证据：`dremwarves.lua:72`。



## O040 | entry-03517

### C12 | entry-03517 | 存在问题
- "wide enough for **one of our party** to fit in with room to spare" 被译作「足够让我们的**一个小队**在里面行走」。
- 原文说的是队伍中的一个人，译文变成了一整支小队，数量和规模都错了（dremwarves.lua:58）。



## O041 | entry-03517

### C13 | entry-03517 | 存在问题

原文“further disrepair and corruption … black growth which engulfs the machine”，译文归因为“年久失修而进一步退化”，并将附着物写成“吞噬着这些机器的黑色怪物”。译文遗漏腐化因素，并把包覆机器的黑色增生物改成了怪物，改变这段起源推断的证据及因果。状态：confirmed。证据：`dremwarves.lua:62`、`:72`；前文已将同类对象描述为附着的恶性增生物。



## O042 | entry-03517

### C13 | entry-03517 | 存在问题
- "**I imagine** the … teeth **aren't entirely natural either**" 被译作「显得十分不自然」。
- 推测语气「我猜」被删，程度也从「并不完全天然」变成了「十分不自然」。这属于删除限定词，把推测说成了断言（dremwarves.lua:60）。



## O043 | entry-03517

### C14 | entry-03517 | 存在问题
- "There was **obviously a source** of these things" 被译作「显然，**这里就是**这些怪物的来源」。
- 原文只是推断「必然有一个源头」，后文才说 "We found the source"。译文提前断言「这里就是来源」，造成时序和逻辑错误（dremwarves.lua:62）。



## O044 | entry-03517

### C15 | entry-03517 | 存在问题
- "Some great machine" 被译作「一些巨大的机器」。原文是单数，并且后文强调 "that was only one machine"。
- 同段的 "judging by the black growth which engulfs **the machine in this room**" 也被译成「这些机器」（复数）。数量错误。



## O045 | entry-03517

### C16 | entry-03517 | 存在问题
- "**I am not the only one** who has been infected" 被译作「**其他人也都**感染了」。
- 原文说「不止我一人感染」，译文变成了「其他人全部感染」，范围被夸大。



## O046 | entry-03517

### C17 | entry-03517 | 存在问题
- "But, **I am content** with this fate" 被译作「但是，**我们**…却只感到充实和满足」。
- 原文只有说话人自己「坦然接受」，译文把这种感受套到了所有人身上，主语范围错了，还加了「充实」。



## O047 | entry-03517

### C18 | entry-03517 | 存在问题
- "We wandered into **the back of the room**" 被译作「我们徘徊到那些还有更多管子的**房间**里面」。
- 原文是「同一房间的后部」，译文变成了「其他房间」，地点关系错误。影响较低。



## O048 | entry-03517

### C19 | entry-03517 | 存在问题
- "**Feral** Drem must have emerged from this egg" 被译作「**原生的**德瑞姆」。
- feral 的意思是野生、未开化，不是「原生」，语义错误（dremwarves.lua:72）。
- 术语子集里没有这个词条，这里只按语义判断，不涉及专名统一。



## O049 | entry-03517

### C20 | entry-03517 | 存在问题
- "**judging by** the black **growth** which engulfs the machine" 被译作「**正如**我们…看到的，吞噬着这些机器的黑色**怪物一样**」。
- 这里有两处错误：
  - "judging by"（依据什么推断）被改成了「正如……一样」（类比），证据关系变了。
  - "growth"（增生物，前文译作「恶性的生长物」）被错译成「怪物」，与前文不一致，也改变了事实。



## O050 | entry-03517

### C21 | entry-03517 | 仅建议
- 译文新增了「考虑到它卓越的防御力」和「本能地」。"tore into them"（猛扑上去）被译作「撕成了碎片」。
- 这些都是补足语气或推理，与后文不矛盾，属于偏好层面的增译，列出来供参考。



## O051 | entry-03522

### C08 | entry-03522 | 存在问题

原文说明延后使用纹身会使患者日后用得更多，因为除了修复身体，还得用纹身抵御开放伤口的感染。译文虽保留“更多地使用”，随后只说不及时修补会感染，遗漏额外使用纹身来抵御感染的因果环节。证据：`lore/fay-willows.lua:113`。



## O052 | entry-03522

### C09 | entry-03522 | 存在问题

原文逐渐减少的是“wounded soldiers”的人数；译文称“痊愈士兵的数量开始达到一定程度”，把正在减少的伤员换成了康复者。证据：`lore/fay-willows.lua:131`。



## O053 | entry-03522

### C10 | entry-03522 | 存在问题

一名士兵走近时，原文主治医师“looked behind me”；译文写“看着我”，改变了视线所指。证据：`lore/fay-willows.lua:131`。



## O054 | entry-03522

### C10 | entry-03522 | 存在问题
- **原文短引**：`Seemingly they would rather tempt fate and avoid using them.`
- **译文短引**：`似乎他们宁愿接受命运，也要避免使用它们。`
- **问题说明**：严重词义反转。`tempt fate` 为英文常用成语，意为“玩命、铤而走险、抱侥幸心理冒险”，译文却将其完全反向误译为“接受命运”（accept fate），彻底颠倒了永恒精灵宁可抱侥幸心理冒险赌命也不用纹身的心态刻画。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:113`（第 1 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O055 | entry-03522

### C11 | entry-03522 | 存在问题
- **原文短引**：`Well, I should say to the shalore it may have been basic food and drink, but by thalore standards I was treated pretty lavishly.`
- **译文短引**：`好吧，我应该对永恒精灵说，这可能对它们来说是基本的食物和饮料，但按照自然精灵的标准...`
- **问题说明**：句法断句严重错误。原句 `to the shalore` 是后半句 `it may have been basic food and drink` 的状语（“对于永恒精灵而言，这或许只是粗茶淡饭”），主干为 `Well, I should say [that]...`（“好吧，我得承认/我得说……”）。译文错误将 `to the shalore` 挂在 `say` 后面译作“我应该对永恒精灵说”，破坏了叙事逻辑。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:115`（第 2 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O056 | entry-03522

### C12 | entry-03522 | 存在问题
- **原文短引**：`When their numbers began to reach more manageable amounts, the chief healer approached to thank me...`
- **译文短引**：`当痊愈士兵的数量开始达到一定程度时，主治医师代表永恒精灵来感谢我的努力。`
- **问题说明**：主语与事实颠倒。`their numbers` 紧承前句 `the number of wounded soldiers began to dwindle`，指需要救治的伤员数量减少到了更容易应付的程度；译文却颠倒主语译为“当痊愈士兵的数量开始达到一定程度时”，歪曲了原文事实陈述。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:131`（第 10 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O057 | entry-03522

### C14 | entry-03522 | 存在问题

原文“rather tempt fate”，译文“宁愿接受命运”。原文强调冒险、拿性命碰运气，译文变成接受命运，改变拒绝治疗的态度。状态：confirmed。证据：`fay-willows.lua:113`。



## O058 | entry-03522

### C15 | entry-03522 | 存在问题

原文“I should say to the shalore it may have been basic food and drink”，译文“我应该对永恒精灵说，这可能对它们来说是基本的食物和饮料”。原文是叙述者补充说明“按永恒精灵的标准”，没有向永恒精灵说话的行为；译文错误拆分句法，增加说话对象。状态：confirmed。证据：`fay-willows.lua:115`，后半句紧接自然精灵的生活标准作比较。



## O059 | entry-03522

### C16 | entry-03522 | 存在问题

原文“move northwards around this area”，译文“在这个地区向北移动”。原文说的是从北面绕过这片区域，译文丢失“绕行”，改变解释返程受阻时的路线关系。状态：confirmed。证据：`fay-willows.lua:119–121`。



## O060 | entry-03522

### C17 | entry-03522 | 存在问题

原文“huge gashes”，译文“一道巨大的伤口”。复数伤口被明确改成一道；同段后文也继续使用复数“wounds”。状态：confirmed。证据：`fay-willows.lua:125`。



## O061 | entry-03522

### C18 | entry-03522 | 存在问题

原文“their numbers … more manageable amounts”，译文“当痊愈士兵的数量开始达到一定程度时”。原文承接尚待处理的伤兵数量下降，译文改成痊愈士兵数量达到某个程度，改变主治医师得以抽身致谢的条件。状态：confirmed。证据：`fay-willows.lua:131` 的前后两句。



## O062 | entry-03522

### C19 | entry-03522 | 存在问题

原文“looked behind me as a soldier approached”，译文“当一名士兵走近时……看着我”。视线落点由叙述者身后改成叙述者本人，丢失医师看到接近士兵的动作关系。状态：confirmed。证据：`fay-willows.lua:131`。



## O063 | entry-03522

### C20 | entry-03522 | 存在问题

原文“fulfilling my end of the bargain”，译文“完成了我的交易”。原文限定为履行自己一方的约定，译文写成整项交易已经完成；随后安排会见将军，正是在推进对方应提供的部分。状态：confirmed。证据：`fay-willows.lua:131`。



## O064 | entry-03522

### C22 | entry-03522 | 存在问题
- "they would rather **tempt fate**" 被译作「宁愿**接受命运**」。
- tempt fate 的意思是冒险、玩命，译文意思接近相反（fay-willows.lua:113）。



## O065 | entry-03522

### C23 | entry-03522 | 存在问题
- "Well, **I should say** to the shalore it may have been basic food and drink" 被译作「好吧，**我应该对永恒精灵说**，这可能对它们来说是……」。
- 原文是「我得更正一下：对永恒精灵来说那也许只是基本饮食」。译文误读成「我应该对永恒精灵说」，把一个自我更正变成了对永恒精灵说话，语义错误。



## O066 | entry-03522

### C24 | entry-03522 | 存在问题
- "The scarce few that were still alive after **had traveled back** to Elvala" 被译作「**准备返回**埃尔瓦拉」。
- 原文是已经抵达，译文变成了还在准备，时序错误，也与下一句「只有几百人设法活着回来」冲突。



## O067 | entry-03522

### C25 | entry-03522 | 存在问题
- "there would have been no need to move northwards **around** this area" 被译作「在这个地区向北移动」。
- 原文是向北「绕行」避开平原，译文丢了绕行，变成在区域内向北走，空间关系错误。影响较低。



## O068 | entry-03522

### C26 | entry-03522 | 存在问题
- "Turning to see … I noticed the huge **gashes** through the **blackened** armor" 被译作「黑色盔甲上有**一道**巨大的伤口」。
- 原文的伤口是复数，被译成「一道」。"blackened"（烧焦、熏黑）被译成「黑色」，丢失了盔甲曾被烧过的信息。影响较低。



## O069 | entry-03522

### C27 | entry-03522 | 存在问题
- "When **their numbers** began to reach more manageable amounts" 被译作「当**痊愈士兵**的数量开始达到一定程度时」。
- 原文指伤兵人数减少到可以应付的程度，译文变成痊愈士兵增加，对象和趋势都反了。



## O070 | entry-03522

### C28 | entry-03522 | 存在问题
- "I **noted** that I had been fulfilling my end of the bargain. Nodding to this the chief healer **looked behind me** as a soldier approached" 被译作「意识到……主治医师向我点头，**看着我**，回答说」。
- 这里有两处错误：
  - "noted" 在这里是「我（向对方）提出」，译成「意识到」后变成心理活动，导致治疗师「点头回答」没有了对象。
  - "looked behind me" 被错译成「看着我」，丢了治疗师看向身后走来士兵这一动作。



## O071 | entry-03522

### C29 | entry-03522 | 仅建议
- 「我甚至从来没有听说过符文的，甚至不知道……」句子残缺，但意思可以理解，属于二级语法问题，列作建议。



## O072 | entry-03527

### C11 | entry-03527 | 存在问题

信使说“quite a surprise to see them out here”，惊讶的是在此地看到矮人；译文“看到他们这样做，我有点惊讶”指向纳格尔人筹措食物和酒，所指对象错误。证据：`lore/fay-willows.lua:218`。



## O073 | entry-03527

### C12 | entry-03527 | 存在问题

原文说法师使矮人的住处坍塌；译文写成“法师制造的爆炸摧毁了他们的家园”，新增了原句没有说明的爆炸。证据：`lore/fay-willows.lua:220`。



## O074 | entry-03527

### C13 | entry-03527 | 存在问题

原文询问信使是否知道守门卫兵会没收矮人的**什么物品**；译文变成告知信使“士兵会没收矮人们携带的物品”，丢失对物品种类的询问。证据：`lore/fay-willows.lua:222`。



## O075 | entry-03527

### C13 | entry-03527 | 存在问题
- **原文短引**：`Noting it I said, "You wouldn't happen to know anything regarding items the dwarves might be carrying that the guards at the city gates would confiscate would you?"`
- **译文短引**：`想到这一点，我问道：“你可能还不知道，士兵会没收矮人们携带的物品，知道吗？”`
- **问题说明**：严重反转问话意图与信息流向。原句为委婉提问句型 `You wouldn't happen to know... would you?`（“你碰巧知道城门守卫会没收矮人携带的什么物品吗？”），主角是向信使探听情况；译文却翻译成向信使反问告知的居高临下语气：“你可能还不知道……知道吗？”，彻底颠倒了对话双方的信息交互逻辑。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:222`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O076 | entry-03527

### C14 | entry-03527 | 存在问题

原文另有纳格尔人的公开理由：“平民携带这类物品太危险”；译文从没收魔法物品直接转到信使自己的看法，遗漏了官方理由，也削弱了随后“任何人携带都危险”的对照。证据：`lore/fay-willows.lua:224`。



## O077 | entry-03527

### C14 | entry-03527 | 存在问题
- **原文短引**：`They say that it's too dangerous for civilians to carry such items. Personally I say it is too dangerous for anyone to be carrying such items, them included.`
- **译文短引**：`我个人认为任何人携带这样的物品都是非常危险的，包括他们自己。`
- **问题说明**：关键句整句脱落漏译。原文前半句 `They say that it's too dangerous for civilians to carry such items.`（他们声称平民携带此类物品太危险了）在译文中完全缺失，导致后半句“我个人认为……”失去了官方说辞作为对比铺垫。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:224`（第 5 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O078 | entry-03527

### C15 | entry-03527 | 存在问题

原文“a couple of halflings”在此只说明两名半身人；译文两次确定为“半身人夫妇”，新增了婚姻关系。证据：`lore/fay-willows.lua:226`。



## O079 | entry-03527

### C15 | entry-03527 | 存在问题
- **原文短引**：`...since the blasted mages caused their home to collapse in on them.`
- **译文短引**：`...因为法师制造的爆炸摧毁了他们的家园。`
- **问题说明**：词性与修辞语法误译。`blasted` 在此处为修饰痛恨辱骂法师的形容词（“那些该死的法师们”），译文却将其错译为名词事件“法师制造的爆炸”，改变了主从关系与修辞色彩。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:220`（第 3 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O080 | entry-03527

### C16 | entry-03527 | 存在问题

叙述者原问信使是否有“plans to deal with the Shaloren”；译文问“你对永恒精灵有什么想法”，把行动计划改为一般看法。证据：`lore/fay-willows.lua:228`。



## O081 | entry-03527

### C16 | entry-03527 | 存在问题
- **原文短引**：`...for unleashing the Spellblaze on Maj'Eyal.`
- **译文短引**：`...终将会为在马基埃亚尔引发魔法大爆炸的行为付出代价。`
- **问题说明**：违反明确适用的 preferred 术语规范。本包术语快照明确规定：维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代。译文依然使用已被废止的旧译“马基埃亚尔”，未按规范使用间隔号。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:228`（第 7 段），对应术语快照第 142 行。DLC 快照 hash 验证一致，未固定 commit。

---



## O082 | entry-03527

### C17 | entry-03527 | 存在问题

原文 `Maj'Eyal` 译为“马基埃亚尔”，与本包适用术语快照中 `_t`、`T.PN.WORLD` 的首选译名“马基·埃亚尔”不符。证据：`lore/fay-willows.lua:228`及 `INPUT.md` 术语子集。



## O083 | entry-03527

### C21 | entry-03527 | 存在问题

原文“a … plot that I would learn the day after”，译文“一场我事后知道的……阴谋”。“次日得知”被泛化成“事后知道”，遗漏明确的时间关系。状态：confirmed。证据：`fay-willows.lua:216`。



## O084 | entry-03527

### C22 | entry-03527 | 存在问题

原文“a surprise to see them out here”，译文“看到他们这样做，我有点惊讶”。信使惊讶的是矮人出现在这里，译文变成惊讶于前述提供食物、酒水的行为，改变评价对象。状态：confirmed。证据：`fay-willows.lua:218–220`；紧接着讨论的正是矮人为何居住在钢铁王座以外。



## O085 | entry-03527

### C23 | entry-03527 | 存在问题

原文“Hard to really know with how secretive the dwarves are”，译文“要想真正了解矮人们的隐秘程度是很难的”。难以知道的是矮人是否还有其他家园；矮人保密是原因。译文把原因改成了需要了解的对象。状态：confirmed。证据：`fay-willows.lua:218`。



## O086 | entry-03527

### C24 | entry-03527 | 存在问题

原文询问是否知道矮人携带了什么会被城门守卫没收的物品，译文“你可能还不知道，士兵会没收矮人们携带的物品，知道吗？”变成告知、确认没收行为。询问内容及信息流向均改变。状态：confirmed。证据：`fay-willows.lua:222`，答复具体指向附魔物品。



## O087 | entry-03527

### C25 | entry-03527 | 存在问题

原文“They say that it's too dangerous for civilians to carry such items”在译文中整句遗漏。官方以平民携带危险为由的说辞因此消失，只剩信使认为任何人都不应携带的个人意见。状态：confirmed。证据：`fay-willows.lua:224`。



## O088 | entry-03527

### C26 | entry-03527 | 存在问题

原文“a couple of halflings”，译文两次写成“一对半身人夫妇”。原文只说明人数，没有婚姻或伴侣关系。状态：confirmed；同条重复出现合并为一个 claim。证据：`fay-willows.lua:226`。



## O089 | entry-03527

### C27 | entry-03527 | 存在问题

原文“any plans to deal with the Shaloren”，译文“你对永恒精灵有什么想法？”原文试探对付永恒精灵的行动计划，译文泛化成态度或看法，削弱了探查阴谋的具体询问。状态：confirmed。证据：`fay-willows.lua:228`，后续邀请也围绕即将实施的计划展开。



## O090 | entry-03527

### C28 | entry-03527 | 存在问题

原文“Maj'Eyal”，译文“马基埃亚尔”。冻结术语子集明确记录该世界地名采用“马基·埃亚尔”，并注明旧写法已被取代；本条是 `_t` 下的相同地名语境。状态：confirmed。证据：INPUT 术语子集的 `Maj'Eyal / T.PN.WORLD / _t` 条目及 `fay-willows.lua:228`。此观察不提出新的全局命名策略。



## O091 | entry-03527

### C30 | entry-03527 | 存在问题
- "I believe he **may have been** a member" 被译作「我**极大程度上**相信他还是……成员」。
- 原文的推测语气被反转成强烈确信，删除了限定词（fay-willows.lua:216 起）。



## O092 | entry-03527

### C31 | entry-03527 | 存在问题
- "it was quite a surprise to see **them out here**" 被译作「看到他们**这样做**，我有点惊讶」。
- 原文惊讶的是矮人「出现在这里」，下一句才会接着问矮人在铁王座以外有没有家园。译文把惊讶的对象改成了「纳格尔人这样做」，逻辑链断了。



## O093 | entry-03527

### C32 | entry-03527 | 存在问题
- "Hard to really know **with how secretive** the dwarves are" 被译作「要想真正了解矮人们的**隐秘程度**是很难的」。
- 原文是「矮人这么隐秘，所以很难得知（他们是否另有家园）」，译文变成「很难了解矮人有多隐秘」，意思错了。



## O094 | entry-03527

### C33 | entry-03527 | 存在问题
- "**You wouldn't happen to know** anything regarding items … the guards at the city gates would confiscate **would you?**" 被译作「**你可能还不知道**，士兵会没收矮人们携带的物品，知道吗？」。
- 原文是向信使打听消息，译文变成主角告诉信使，言语行为反了。信使接下来的解释因此失去了上下文。



## O095 | entry-03527

### C34 | entry-03527 | 存在问题
- 译文漏掉了整句 "They say that it's too dangerous for civilians to carry such items."。
- 下一句 "Personally I say it is too dangerous for **anyone** … them included" 是在反驳这一句。缺了它，「包括他们自己」的对比就说不通了。



## O096 | entry-03527

### C35 | entry-03527 | 存在问题
- "a table with **a couple of halflings**" 被译作「一对半身人**夫妇**」，后文又重复了一次。
- 原文只是两三个半身人，没有说是夫妻，译文新增了一段不存在的关系。



## O097 | entry-03527

### C36 | entry-03527 | 存在问题
- "You wouldn't happen to have any **plans to deal with** the Shaloren?" 被译作「你对永恒精灵有什么**想法**？」。
- 原文是主角有意试探对方有没有行动计划，所以才会有下文「看看他知道多少」和对方姿态骤变。译文变成询问看法，试探的意图丢失了。



## O098 | entry-03527

### C37 | entry-03527 | 存在问题
- "on Maj'Eyal" 被译作「马基埃亚尔」。
- 术语快照中 Maj'Eyal 的 source_tag 为 `_t`，状态 preferred，规定用「马基·埃亚尔」，并注明「马基埃亚尔」已被取代。本条 source_tag 同为 `_t`，属于叙事中的地名，术语明确适用。



## O099 | entry-03527

### C38 | entry-03527 | 存在问题
- "Spellblaze, is that what **they** call it?" 被译作「**你们**把那个叫做魔法大爆炸？」。
- 原文问的是「他们」（第三方）这样称呼，信使的回答 "or so I have been told" 正好对应。改成「你们」后，问答对不上了。



## O100 | entry-03527

### C39 | entry-03527 | 存在问题
- "and **possibly** ones that required secrecy" 被译作「他们进行的计划还需要保密」。
- "possibly" 被删，推测变成了断言，属于删除限定词。



## O101 | entry-03527

### C40 | entry-03527 | 仅建议
- "the **blasted** mages caused their home to collapse in on them" 被译作「法师制造的爆炸摧毁了他们的家园」。
- "blasted" 在这里是咒骂语（该死的），被当成了「爆炸」。但「魔法大爆炸导致坍塌」在剧情上大致成立，主要损失是咒骂语气，所以列作建议。



## O102 | entry-03527

### C41 | entry-03527 | 仅建议
- 「我突然**会**想起」应为「回想起」，这是错字。
- 「**今早**进城的时候」是增译。fay-willows.lua 第 192 行起的上一章没有明确说是当天早上，但也不矛盾。



## O103 | entry-03531

### C17 | entry-03531 | 存在问题
- **原文短引**：`I had thought better of you since you killed that Eldoral halfling.`
- **译文短引**：`自从你杀了那个艾德瑞尔半身人，我就更想念你了。`
- **问题说明**：极其荒谬的灾难级误译。`thought better of you` 为英文固定成语，表示“我本以为你还算有骨气/原本还高看你一眼/以为你还算明事理”，译文居然望文生义将其误译为“我就更想念你了”，彻底破坏了反派角色充满杀意与质问的狂热氛围，严重损害叙事质量。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:295`（第 4 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O104 | entry-03531

### C18 | entry-03531 | 存在问题

原文说帐篷里所见之事可能是灵能奴役者**造成的结果**；译文“我在帐篷里看到的可能是一个灵能奴役者”把所见对象直接认定为奴役者。证据：`lore/fay-willows.lua:289`。



## O105 | entry-03531

### C18 | entry-03531 | 存在问题
- **原文短引**：`...it was entirely possible that I could have become enthralled to the slavers will and made to do their bidding unquestioningly.`
- **译文短引**：`...我完全有可能被奴役者的意志所吸引，毫无疑问地服从他们的命令。`
- **问题说明**：核心设定与心智控制机制误译。`enthralled to someone's will` 在奇幻心智控制/灵能背景下意为“受其心智控制/彻底被其奴役/沦为受支配的奴仆”（术语快照明确标明 Thrall 为精神支配后的奴仆身份），译文却望文生义误译为“被……所吸引”；同时 `unquestioningly`（毫无异议/盲目不折不扣）被误译为“毫无疑问地”。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:289`（第 1 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O106 | entry-03531

### C19 | entry-03531 | 存在问题

原文“become enthralled to the slavers will”指意志受到支配；译文“被奴役者的意志所吸引”变成吸引，失去控制关系。证据：`lore/fay-willows.lua:289`。



## O107 | entry-03531

### C19 | entry-03531 | 存在问题
- **原文短引**：`...leaving a faceless humanoid.`
- **译文短引**：`...留下了一个面目全非的人形。`
- **问题说明**：专有名词与种族特征误译。`faceless` 意为“无脸的/没有面孔五官的”（对应 DLC 中 Drem 族“无面”的核心生理特征，与前文第 340 行 "found a faceless dwarf inside. In other words, a Drem" 严格对应），译文却误译为“面目全非”（面部被毁损残缺），丢失了该心象破灭后露出无面人形的重要种族特征信息。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:299`（第 6 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O108 | entry-03531

### C20 | entry-03531 | 存在问题

叙述者起身想看“who had thrown me”；译文写“是谁在拉我”，把扔进帐篷的动作改成拉。证据：`lore/fay-willows.lua:291`。



## O109 | entry-03531

### C20 | entry-03531 | 存在问题
- **原文短引**：`...who had thrown me` / `why have you thrown me in here?`
- **译文短引**：`是谁在拉我` / `为什么把我拉到这里？`
- **问题说明**：动作动词误译。`throw` 意为暴力地“扔/摔进”，译文两处均误译为缓和的“拉”，弱化了主角被粗暴摔入帐篷并导致头晕目眩的动作冲击力与遇袭情节。
- **状态**：`confirmed`
- **源码依据**：`tome-cults/data/lore/fay-willows.lua:291`（第 2 段）。DLC 快照 hash 验证一致，未固定 commit。

---



## O110 | entry-03531

### C21 | entry-03531 | 存在问题

信使原话“I had thought better of you since you killed that Eldoral halfling”是曾因此对她评价更高；译文“我就更想念你了”改变了态度含义。证据：`lore/fay-willows.lua:295`。



## O111 | entry-03531

### C22 | entry-03531 | 存在问题

幻象露出的是“faceless humanoid”，即没有脸的人形；译文“面目全非的人形”表示面容变得难以辨认，丢失“无脸”特征。证据：`lore/fay-willows.lua:299`。



## O112 | entry-03531

### C23 | entry-03531 | 存在问题

原文披斗篷的人曾短暂拜访信使；译文“我在客栈和信使谈话时短暂拜访过的那个人”改成叙述者拜访披斗篷者，颠倒了动作主体。证据：`lore/fay-willows.lua:301`。



## O113 | entry-03531

### C29 | entry-03531 | 存在问题

原文“become enthralled to the slavers will”，译文“被奴役者的意志所吸引”。原文描述意志受控制、被奴役，译文变成被吸引，改变灵能控制的性质；后面的服从命令不能使这两个状态等同。状态：confirmed。证据：`fay-willows.lua:289`，同段明确提到挣脱控制并驱散幻象。这里不适用鲜血之环“奴隶贩子”的术语语境。



## O114 | entry-03531

### C30 | entry-03531 | 存在问题

原文两次使用“thrown me”，译文分别为“谁在拉我”“为什么把我拉到这里”。被扔进帐篷的暴力动作被改成拉入。状态：confirmed；两处合并为一个 claim。证据：`fay-willows.lua:291`，前章 `:282` 也明确写出伸手将她扔进帐篷。



## O115 | entry-03531

### C31 | entry-03531 | 存在问题

原文“another kick with the back of the heel to my face”，译文“又踢了我一脚，脚踩在我的脸上”。原文是一记以脚跟击中面部的踢击，译文改变为踢后踩脸的动作。状态：confirmed。证据：`fay-willows.lua:295`。



## O116 | entry-03531

### C32 | entry-03531 | 存在问题

原文“I had thought better of you”，译文“我就更想念你了”。原文是因她杀死半身人而对她评价较高，译文变成思念。状态：confirmed。证据：`fay-willows.lua:295`，后句紧接曾把她视为自然盟友、如今失望的解释。



## O117 | entry-03531

### C33 | entry-03531 | 存在问题

原文“a faceless humanoid”，译文“一个面目全非的人形”。原文明确表示没有面孔，译文仅表示面貌变得无法辨认，丢失幻象失去脸部形态的特征。状态：confirmed。证据：`fay-willows.lua:299`，随后该形象彻底消失。



## O118 | entry-03531

### C34 | entry-03531 | 存在问题

原文是斗篷人“briefly visited the messenger when I was talking to him”，译文“我在客栈和信使谈话时短暂拜访过的那个人”。拜访者由斗篷人变成叙述者，受访者也随之改变。状态：confirmed。证据：`fay-willows.lua:301`；`:226` 明确记载斗篷人走近信使交谈。



## O119 | entry-03531

### C35 | entry-03531 | 存在问题

原文“a bit confused … a moment to realize”，译文“困惑许久，我才意识到”。短暂反应被改成持续很久，改变紧接刺杀受阻这一瞬间的时间尺度。状态：confirmed。证据：`fay-willows.lua:305`。

实际读取与边界记录：

- 冻结包根目录 `B`：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/`。
- 读取了 `B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。40 个 ID 连续，INPUT 与 entries.json 的原译文逐条一致；邻近译文仅查阅 context.lua。
- 读取并核验了下列六个源码文件，均位于 `B/sources/dlc/cults/tome-cults/`，SHA-256 均与 source-access 清单一致：

| 相对源码路径 | SHA-256 |
|---|---|
| `data/general/npcs/corrupted_blobs.lua` | `76cbc59be306a63bfa17d81904820c3838543a9b8b074554190bca408bbfbec4` |
| `data/general/npcs/horror.lua` | `8d63e86d5eb6f7552ec2cdfe598b45618460028236190f246202809c045f461d` |
| `data/general/objects/world-artifacts.lua` | `27af5b2ae30c5b2db7f1d585b8334bc28ee1284e771a8a9f5c198f892edbc92a` |
| `data/glyph_sequences/cults.lua` | `9d3b29fd6a91fb9ced64581b760fc0026b0fb0bcf9cc687a55399aed76faaabf` |
| `data/lore/dremwarves.lua` | `0b8133e8ef00f5b0ca5fcb2f7df1ebec355873ac5dfac9454a85a48084b326e9` |
| `data/lore/fay-willows.lua` | `05a3f93c9f5cd5baf52429155fcd4a09b6045ef45fbf3472562d55f5da0e4c6f` |

额外源码读取及调用来源：

- `world-artifacts.lua:210` 的 `require("mod.dialogs.RingOfTheHunter")` 引入获准文件 `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/overload/mod/dialogs/RingOfTheHunter.lua`。哈希核验为 `2894023dcca501a035239c74a9873ff4df4e1433f2513c6203e352a6705d33fa`。其 `unload()` 将所选技能写入装备的 `wielder.learn_talent`。
- `world-artifacts.lua:1029` 的 `who:his_her()` 引入本体调用追踪。仅通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取：
  - `game/modules/tome/class/Actor.lua`：确认继承 `engine.Actor`。
  - `game/engines/default/engine/Actor.lua`：`:607` 将调用转发给 `string.his_her(self)`。
  - `game/engines/default/engine/utils.lua`：`:939–943` 按性别返回本地化所属代词。没有读取其他语言译文，也未把未观察到的最终运行画面称为实测。

DLC 的源码仓库、commit 和目标发行版本适用性仍未固定；已核验的是上述快照内容，版本适用性缺口保留待确认。本体固定 commit 未套用于 DLC。未发现需要另外列为待确认的具体译文 claim。

未越界读取、未读取其他审核报告、未创建子 agent、未修改仓库，未创建临时目录或文件。本次交付仅为独立审核观察，不作生产完成认证。


## O120 | entry-03531

### C42 | entry-03531 | 存在问题
- "become **enthralled** to the slavers will and made to do their bidding **unquestioningly**" 被译作「被奴役者的意志所**吸引**，**毫无疑问地**服从他们的命令」。
- 这里有两处错误：
  - enthralled 是「被奴役、被控制」，不是「被吸引」。
  - unquestioningly 是「不加质疑地」。「毫无疑问地」在中文里的常见意思是「无可怀疑地」，属于假朋友错译。
- 术语快照中 slaver→奴隶贩子 的注明适用范围是「鲜血之环语境」，本条讲的是灵能奴役者，这条术语不适用，所以这里不按术语算缺陷。



## O121 | entry-03531

### C43 | entry-03531 | 存在问题
- "look up at who had **thrown** me" 以及后文 "why have you **thrown** me in here" 都被译成了「**拉**」。
- 上一章结尾写的是 "a hand reached out of its opening, **throwing** me inside"（fay-willows.lua 约第 285 行），被扔进来的动作与译文不符。



## O122 | entry-03531

### C44 | entry-03531 | 存在问题
- "I had **thought better of you** since you killed that Eldoral halfling" 被译作「我就更**想念**你了」。
- 原文是「（因此）对你评价更高」，译文变成了「想念」，意思错误（fay-willows.lua:295）。



## O123 | entry-03531

### C45 | entry-03531 | 存在问题
- "leaving a **faceless** humanoid" 被译作「留下了一个**面目全非**的人形」。
- faceless 是「没有面孔」，面目全非是「毁得认不出来」，事实错误（fay-willows.lua:299）。



## O124 | entry-03531

### C46 | entry-03531 | 存在问题
- "the same human **who had briefly visited the messenger** when I was talking to him in the inn" 被译作「这就是**我**在客栈和信使谈话时**短暂拜访过**的那个人」。
- 原文是斗篷人拜访信使，译文变成了「我拜访过他」，动作主体错了。



## O125 | entry-03531

### C47 | entry-03531 | 存在问题
- "likely the same one that had been **standing with** the human in the crowd" 被译作「和那个人类站在一起**蛊惑群众**的那个半身人」。
- 原文只说这个半身人与那人一同站在人群中。译文新增了「蛊惑群众」，给半身人加了原文没有的行为，而且这个半身人随后救了主角。



## O126 | entry-03531

### C48 | entry-03531 | 存在问题
- "it would take me **a moment** to realize" 被译作「困惑**许久**」。
- 片刻被译成了很久，时长信息相反。影响较低。



## O127 | entry-03531

### C49 | entry-03531 | 仅建议
- "Enough pain has been felt already without adding to it-" 被译作「**他们**已经感觉到了足够的痛苦……了。」
- 原文的破折号表示话被砸头打断，译文用句号收尾，打断感没了。「他们」是按语境补出的主语。整体属于表达层面的问题。



## O128 | entry-03532

### C24 | entry-03532 | 存在问题

标题“Spared”对应紧接着的正文“spare her”，指半身人决定饶她一命；“死里逃生”只表达幸存，遗漏了他人放过她的关系。证据：`lore/fay-willows.lua:311,314`。

**读取范围与版本。** 实际读取了指定的 `INPUT.md`、同目录的 `entries.json`、`context.lua`、`source-access.json`，以及清单中本组的六个单文件：`corrupted_blobs.lua`、`horror.lua`、`world-artifacts.lua`、`cults.lua`、`dremwarves.lua`、`fay-willows.lua`（完整相对路径见 `source-access.json` 的 `sections`）。六个源码文件的 SHA-256 均与清单相符。未追读额外源码；本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 未用于推断 DLC 行为。DLC 快照的源码仓库及 commit 未固定；上述结论针对冻结原文、译文及该哈希快照，不据此断言其他目标版本的机制适用性。未创建临时文件，未读取其他报告，未发现越界读取。


## O129 | entry-03532

### C50 | entry-03532 | 仅建议
- 标题 "Spared" 被译作「死里逃生」。原文强调「被人饶过」，这层意思在译文里弱化了，但大意相符，属于措辞偏好。

---


