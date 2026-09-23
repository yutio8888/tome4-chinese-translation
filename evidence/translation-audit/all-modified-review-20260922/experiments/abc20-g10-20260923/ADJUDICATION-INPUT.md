# 匿名源码核验与归并：40 条 / 187 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方187项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好187行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03533

### C01 | entry-03533 | 存在问题

原文“**The messengers may have been killed**”，译文“**信使的同伙们可能已经被杀了**”：被杀者从信使变成其同伙。证据：`fay-willows.lua:312`。



## O002 | entry-03533

### C01 | entry-03533 | 存在问题

原文“The messengers may have been killed”，译文“信使的同伙们可能已经被杀了”。被杀的是传播信息的人本身，译文增加“同伙”，改变了人物关系与被处决对象。证据：`L/fay-willows.lua:312`，同段“传播者被杀、信息仍流传”的对应关系。



## O003 | entry-03533

### C01 | entry-03533 | 存在问题
- **原文短引**："The halfling trailed off to take a breath before continuing with the final sentence."
- **译文短引**：“半身人拖着脚步喘口气，然后继续念最后一句话。”
- **具体问题**：短语 "trailed off" 指半身人说话的声音逐渐减弱、语声渐歇（结合随后 "to take a breath before continuing with the final sentence" 明确为口语发言节奏），译文将其错误理解为物理行动 "拖着脚步"，导致人物动作与场景语义失真。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:329`，语境纯文本语义；trail off 针对言语语声衰减，非脚步拖曳。



## O004 | entry-03533

### C01 | entry-03533 | 存在问题
原文 “The messengers may have been killed, but the message they spread persisted.” 译为“信使的同伙们可能已经被杀了”。原文说被杀的是这些“信使”本人，也就是上句被处决的罪魁。译文多出“同伙们”，说错了被杀的对象。依据是语境：上句写他们公开处决了罪魁祸首。



## O005 | entry-03533

### C02 | entry-03533 | 存在问题

原文“**disbelief and dismay**”，译文“**不信任和沮丧**”：`disbelief` 是难以置信，并未说此人不信任半身人。证据：`fay-willows.lua:314`。



## O006 | entry-03533

### C02 | entry-03533 | 存在问题

原文“take random people from their homes”，译文“把无辜的人从他们的家里带走”。原文指控的是任意抓人，译文改成对这些人无罪的直接断言，丢失了抓捕方式。随后半身人专门回应他们经过仔细甄别，因此这一区别影响争论内容。证据：`L/fay-willows.lua:324`、`:326`。



## O007 | entry-03533

### C02 | entry-03533 | 存在问题
- **原文短引**："This THALORE has turned HER BACK on NATURE! She Must Di-"
- **译文短引**：“这个自然精灵已经背叛了大自然！她必须被…”
- **具体问题**：原文 "She Must Di-" 是人类暴怒喊叫 "She Must Die-" 时被半身人动作打断的未竟词（Die 词尾截断），属于主动语态表达“她必须死——”。译文误译为被动态“她必须被…”，不仅丢失了核心动作“死/被处决”，且臆增被动标记，导致戏剧冲突与断句信息结构丢失。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:273`，戏剧对白截断处理错误。



## O008 | entry-03533

### C02 | entry-03533 | 存在问题
“To take random people from their homes” 译为“把无辜的人从他们的家里带走”。“random”（随意抓人）被改成“无辜”，意思变了。下文半身人答 “If you are referring to the people we named”，正是反驳“随意抓人”，强调人是点名选定的。改成“无辜”后，这层对立没了。



## O009 | entry-03533

### C03 | entry-03533 | 存在问题

原文“**trailed off to take a breath**”，译文“**拖着脚步喘口气**”：说话声渐止被写成了走路动作。证据：`fay-willows.lua:326`。



## O010 | entry-03533

### C03 | entry-03533 | 存在问题

原文“twist nature to their whims”，译文“把自然扭曲成自己的突发奇想”。原文表示为满足个人意愿而扭曲自然，译文把个人意愿变成自然被扭曲后的结果，改变目的与结果关系。证据：`L/fay-willows.lua:326`。



## O011 | entry-03533

### C03 | entry-03533 | 存在问题
- **原文短引**："It was my turn to pause as this question was put to me."
- **译文短引**：“当被问到这个问题之后，我了停下来。”
- **具体问题**：译文出现明显语病与错字重排倒错：“我了停下来”（应为“我停了下来”），属于未校对导致的文字排版错误。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:290`，中文句式严重语病。



## O012 | entry-03533

### C03 | entry-03533 | 存在问题
“The halfling trailed off to take a breath” 译为“半身人拖着脚步喘口气”。“trail off” 指说话声音渐弱、停顿，不是“拖着脚步”，动作译错了。依据是语境：紧接着就是 “before continuing with the final sentence”。



## O013 | entry-03533

### C04 | entry-03533 | 存在问题

原文“**made of sterner composition**”，译文“**更加顽固**”：评价的是坚韧、能承受严酷场面，译文改为固执。证据：`fay-willows.lua:328`。



## O014 | entry-03533

### C04 | entry-03533 | 存在问题

原文“trailed off to take a breath”，译文“拖着脚步喘口气”。这里是说话声音收住、停顿换气，没有移动脚步的动作。译文新增人物动作。证据：`L/fay-willows.lua:326`，前后均在描写同一段发言。



## O015 | entry-03533

### C04 | entry-03533 | 存在问题
- **原文短引**："Of course, you seem like you are made of sterner composition than most."
- **译文短引**：“当然，你看起来比其他人都要更加顽固。”
- **具体问题**："made of sterner composition"（源自 made of sterner stuff）意指“性格更为坚毅、更能经受严酷考验”，上下文紧承半身人所言“也许你没胆量见识火刑场面，那建议你回小森林去……当然，你看起来比多数人要坚强刚毅得多”。译文误译为负面贬义词“更加顽固”，将意志坚强刚毅曲解为执拗固执，扭曲了半身人对主角性格的评价与引导动机。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:330`，上下文对话语境直接可证。



## O016 | entry-03533

### C04 | entry-03533 | 存在问题
“Perhaps you may not have the stomach for it” 译为“也许你对它没有胃口”。英文习语的意思是“受不了、承受不了”那种场面，中文“没有胃口”是“不感兴趣、不合口味”，把“承受力”说成了“兴趣”。



## O017 | entry-03533

### C05 | entry-03533 | 存在问题

原文“may not have the stomach for it”，译文“也许你对它没有胃口”。其对象是公开焚杀的残酷场面，意思是无法承受或忍受；译文变成食欲或兴趣，未传达承受能力。证据：`L/fay-willows.lua:326`。



## O018 | entry-03533

### C05 | entry-03533 | 存在问题
- **原文短引**："To take random people from their homes, charge them with what you see as wrongdoings, and then execute them in a fiery display?"
- **译文短引**：“把无辜的人从他们的家里带走，指控他们做了你认为是错误的事，然后在火刑架上处决他们？”
- **具体问题**：原文 "random people" 是指狂热分子在城中“任意挑选/随机抓取的人”，后文半身人反驳正是基于此点（声称这些人并非随机抓取，而是经过仔细甄别辨认的药剂师、符文师等）。译文将 "random people" 译为“无辜的人”，不仅丢失了“随意/随机挑选”的关键指控，还使前后文关于“是否随机抓人 vs 是否精挑细选”的对话逻辑链断裂。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:324-328`，前后对话辩驳逻辑。



## O019 | entry-03533

### C05 | entry-03533 | 存在问题
“you seem like you are made of sterner composition than most” 译为“你看起来比其他人都要更加顽固”。原文是在夸对方更坚强、更有韧性，半身人借此平息菲的怒火（“Attempting to redirect my anger”）。“顽固”是贬义，说话意图从恭维变成了批评。



## O020 | entry-03533

### C06 | entry-03533 | 仅建议
“我了停下来”字序错了，应为“我停了下来”。属于错字，不影响理解。



## O021 | entry-03533

### C06 | entry-03533 | 存在问题

原文“made of sterner composition than most”，译文“比其他人都要更加顽固”。原文承接能否承受残酷场面的讨论，评价其性情坚韧；“顽固”改成不肯改变意见，“其他人都”还把“大多数”扩大为全部。证据：`L/fay-willows.lua:328`。



## O022 | entry-03533

### C07 | entry-03533 | 存在问题

译文“当被问到这个问题之后，我了停下来”存在明显缺字或错字，句法不成立；原文“It was my turn to pause”表达的是叙述者轮到自己停顿。该问题属于实际文字错误，不只是措辞偏好。证据：冻结条目第四段；`L/fay-willows.lua:318`。



## O023 | entry-03534

### C05 | entry-03534 | 存在问题

标题“**Blackened Shoreline**”译作“**黑暗的海岸**”，丢失海岸被烧黑的状态；紧接的正文明确写有焦黑地面与烧毁植被。证据：`fay-willows.lua:339–344`。



## O024 | entry-03534

### C06 | entry-03534 | 存在问题
- **原文短引**："Escapades of Fay Willows [Book 3, Chapter 1] - Blackened Shoreline"
- **译文短引**：“菲·维莉欧斯的冒险 [第3卷，第1章] - 黑暗的海岸”
- **具体问题**：原文 "Blackened" 为被动分词形容词（由 blacken 派生，意为“被灼烧变黑的/焦黑的”），紧密对应正文第一段与第二段对南部海岸遭受魔法大爆炸摧残的物理描述（"the ground was charred black", "burnt out trees"）。译文将其译为“黑暗的”（对应 dark），混淆了物理上遭受灾变烈火焦化变黑的地貌特征与无光照的“黑暗”，丢失了特定受灾物理状态的语义信息。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:339` 结合 342-351 正文描述 "ground was charred black"。



## O025 | entry-03534

### C07 | entry-03534 | 仅建议
“Blackened Shoreline” 译为“黑暗的海岸”。“Blackened” 是烧焦变黑，正文也写“地面烧黑了”。“黑暗”偏向“暗”，只是标题措辞精度问题，正文已经交代清楚，不算信息缺失。



## O026 | entry-03534

### C08 | entry-03534 | 存在问题

原文“Blackened Shoreline”，译文“黑暗的海岸”。本章明确描写地面被烧黑、植物烧焦，标题中的 blackened 指遭受破坏后变黑，译文只表达昏暗，遗漏了焦黑地貌的含义。证据：entry-03535 第二个正文段；`L/fay-willows.lua:339` 及该章正文。



## O027 | entry-03535

### C06 | entry-03535 | 存在问题

原文希望此地警醒“**the Shaloren**”，译文改为“**提醒人们**”，把特指永恒精灵扩大为所有人。证据：`fay-willows.lua:340`。



## O028 | entry-03535

### C07 | entry-03535 | 存在问题

原文说动物尸体“**left untouched by the bugs and worms**”，译文说尸体里“**连虫子和蛆虫都没有**”。未被啃食不等于虫子不存在，场景细节被改写。证据：`fay-willows.lua:344`。



## O029 | entry-03535

### C07 | entry-03535 | 存在问题
- **原文短引**："These lands will never fully heal, but I do hope it will serve as a reminder the to Shaloren, to never brashly use magic in such a way again."
- **译文短引**：“这里的土地永远不会完全愈合，我真的希望它能提醒人们，不要再以这种方式肆无忌惮地使用魔法。”
- **具体问题**：原文明确为 "serve as a reminder the to Shaloren"（提醒永恒精灵；原文含上游轻微拼写失误 the to，指称对象极其清晰）。叙述者菲·维莉欧斯作为自然精灵，离开故土的核心动机与愤恨目标正是引发魔法大爆炸的永恒精灵。译文将核心种族专名 "Shaloren" 粗暴泛化遗漏为“人们”，丢失了关键种族指涉与全篇故事的核心矛盾驱动力。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:343` 叙事上下文。



## O030 | entry-03535

### C08 | entry-03535 | 存在问题

原文区分两件事：如今的岩石险境“**would certainly kill anyone inside it**”，魔法大爆炸时原住民“**likely**”遇难。译文写成平原“**被尖石所碾碎了，这个过程恐怕杀死了里面的所有人**”，将后来进入者所面对的危险改成过去灾变中的死亡过程。证据：`fay-willows.lua:346`。



## O031 | entry-03535

### C08 | entry-03535 | 存在问题
- **原文短引**："Now the plains had been replaced by this deadly gauntlet of rock that would certainly kill anyone inside it, and likely anyone who had been living on the plains before the Spellblaze."
- **译文短引**：“现在平原已经被这些致命的尖石所碾碎了，这个过程恐怕杀死了里面的所有人，很可能是在魔法大爆炸之前生活在平原上的任何物种。”
- **具体问题**：
  1. 结构与主谓关系误译：原文 "the plains had been replaced by this deadly gauntlet of rock" 是平原被这片致命的岩石险道/石林所取代，译文误译为平原“被这些致命的尖石所碾碎了”。
  2. 概念错译：原文 "anyone who had been living on the plains" 明明白白是指曾生活在平原上的“任何人”，译文误译为“任何物种”（any species），将人类/精灵等居民群体错误扩大为所有生物物种。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:358-360`，语法主谓结构及词义证据。



## O032 | entry-03535

### C08 | entry-03535 | 存在问题
“I do hope it will serve as a reminder the to Shaloren” 译为“提醒人们”。原文特指永恒精灵（Shaloren，术语“永恒精灵”），也就是魔法大爆炸的肇事方。泛化成“人们”，丢了针对的对象。



## O033 | entry-03535

### C09 | entry-03535 | 存在问题

原文“serve as a reminder … to Shaloren”，译文“提醒人们”。警示的明确对象是永恒精灵，译文泛化为所有人，丢失了叙述者对施法族群的归责。证据：冻结条目斜体首段。



## O034 | entry-03535

### C09 | entry-03535 | 存在问题
“the lands jaggedly shooting out unnaturally towards the sky” 译为“那些荒芜的土地不自然地向天空伸去”。“jaggedly”（参差、锯齿状）丢了，还多出原文没有的“荒芜”。下段说这些岩石形成“扭曲的裂缝和尖刺”，外形信息应该从这里开始交代。



## O035 | entry-03535

### C10 | entry-03535 | 存在问题

原文平原被危险岩石地带取代，“would certainly kill anyone inside it”，并另推测原先居民已经遇难。译文“被这些致命的尖石所碾碎了，这个过程恐怕杀死了里面的所有人”，把目前仍会杀死进入者的危险改成过去一次灾变的结果；随后“任何物种”又扩大了原文“anyone”的对象。证据：冻结条目描写米德瓦尔平原的段落。



## O036 | entry-03535

### C10 | entry-03535 | 存在问题
“this deadly gauntlet of rock that would certainly kill anyone inside it, and likely anyone who had been living on the plains before the Spellblaze” 译为“这个过程恐怕杀死了里面的所有人，很可能是在魔法大爆炸之前生活在平原上的任何物种”。
- 原文前半句说的是岩石地带现在仍然会让任何进入者丧命，属于持续的危险。译文改成过去的过程已经杀死了人。
- “certainly” 被弱化成“恐怕”。
- “replaced” 被译成“碾碎”。

时态、确定程度和范围都变了。



## O037 | entry-03535

### C11 | entry-03535 | 存在问题

原文“The waters bubbled as if being boiled”，译文“水沸腾了”。原文只是根据冒泡现象作类比，译文断言水已沸腾，改变了观察与判断的确定程度。证据：冻结条目到达南部海岸的段落。



## O038 | entry-03535

### C11 | entry-03535 | 存在问题
“The action seemed to take the beings back a bit” 译为“这一举动似乎让他们后退了一点”。“take aback” 是“使吃惊”，不是身体后退。依据是语境：接着说 “though still on edge they assumed a less aggressive stance”。



## O039 | entry-03535

### C12 | entry-03535 | 仅建议
“一只小队”量词不对，应为“一支”。不影响理解。



## O040 | entry-03535

### C12 | entry-03535 | 存在问题

原文“what I assumed was a forest”，译文“一片森林的烧尽的残骸”。原文对残骸原先是否为森林保留推测，译文删去这一限定，变成确定事实。证据：冻结条目沿熔岩河寻找通路的段落。



## O041 | entry-03535

### C13 | entry-03535 | 存在问题

原文“a path leading downwards”，译文只保留“通向……另一边的路”。路径向下延伸的方向信息丢失；这是穿越高原、山隙时的具体地形描述。证据：冻结条目遇见食人魔之前的段落。



## O042 | entry-03540

### C09 | entry-03540 | 仅建议

“**Hateful Wrath**”译作“**仇恨愤怒**”较生硬；两个情绪要素仍在，没有可确认的信息错误，属于标题措辞偏好。证据：`fay-willows.lua:464`。



## O043 | entry-03540

### C09 | entry-03540 | 仅建议
- **原文短引**："Escapades of Fay Willows [Book 3, Chapter 6] - Hateful Wrath"
- **译文短引**：“菲·维莉欧斯的冒险 [第3卷，第6章] - 仇恨愤怒”
- **具体问题**：原文 "Hateful Wrath" 为形容词修饰名词结构，译文将其处理为两个汉语名词“仇恨”与“愤怒”生硬并列拼接，缺乏连词或偏正修饰关系，略显生硬翻译腔。建议考虑中文习惯调整为偏正结构。
- **状态**：仅建议
- **偏好说明**：原译文已涵盖 hateful 与 wrath 的字面核心情绪，读者能够理解章节主旨，不构成不可逆的信息缺失或事实错误，故仅作为行文自然度的润色建议。



## O044 | entry-03540

### C13 | entry-03540 | 仅建议
“Hateful Wrath” 译为“仇恨愤怒”，两个名词硬凑在一起，读着别扭，意思没错。



## O045 | entry-03540

### C14 | entry-03540 | 仅建议

“Hateful Wrath”译为“仇恨愤怒”较像两个名词并列，汉语标题略生硬。但仇恨与愤怒均保留，没有可证的叙事事实错误，因此仅属表达偏好。



## O046 | entry-03541

### C10 | entry-03541 | 存在问题

“**Exhaustive Travel**”是令人精疲力竭的旅途；“**穷途末路**”表示走投无路，改变标题事件的含义。证据：`fay-willows.lua:490`。



## O047 | entry-03541

### C10 | entry-03541 | 存在问题
- **原文短引**："Escapades of Fay Willows [Book 4, Chapter 1] - Exhaustive Travel"
- **译文短引**：“菲·维莉欧斯的冒险 [第4卷，第1章] - 穷途末路”
- **具体问题**：原文 "Exhaustive Travel"（作者在此使用 exhaustive 指代极为耗费体力、使人筋疲力竭的旅途），正文全篇核心就是描写菲与食人魔在漫长迁徙中精疲力竭、极度疲惫瘫倒的状态（"collapsed from exhaustion", "heavy weight of exhaustion from so much running"）。译文将其误译为“穷途末路”（陷入绝境、走投无路），完全背离正文关于“疲劳跋涉”的叙事主题，属于彻底的词义曲解。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:490` 章节标题及对应正文 `491-496` 行。



## O048 | entry-03541

### C14 | entry-03541 | 存在问题
“Exhaustive Travel” 译为“穷途末路”。原标题指的是“令人精疲力竭的旅程”。“穷途末路”是走投无路、陷入绝境，意思完全不同。依据是快照 `fay-willows.lua:490-492`：本章写菲因疲惫而倒下、食人魔耐力惊人、一行人抵达绿地，并没有绝境的内容。



## O049 | entry-03541

### C15 | entry-03541 | 存在问题

“Exhaustive Travel”译为“穷途末路”，把旅途造成的极度疲劳改成走投无路。正文描写菲累倒、食人魔坚持行进、补充食物后继续前往埃尔瓦拉，并非已无路可走。证据：`L/fay-willows.lua:491`、`:499`、`:507`。



## O050 | entry-03543

### C11 | entry-03543 | 仅建议
- **原文短引**："Escapades of Fay Willows [Book 4, Chapter 3] - The Enchantress"
- **译文短引**：“菲·维莉欧斯的冒险 [第4卷，第3章] - 女巫”
- **具体问题**：章节主角阿尔雷温·泰尔在正文中是制作高超魔法符文（如回归符文）的奥术制造大师（"a masterwork produced by the best enchantress in Elvala"），其定位更偏向奇幻设定中的“附魔师/女法师”，而非具有邪恶或荒野巫术色彩的“女巫”（Witch）。
- **状态**：仅建议
- **偏好说明**：术语库中未冻结 Enchantress 专属条目，“女巫”在通俗奇幻文本中偶有宽泛指代女性施法者的用法，且全章统一使用该称谓，未造成情节机制误导，故判定为角色定位精度建议。



## O051 | entry-03543

### C15 | entry-03543 | 仅建议
“The Enchantress” 译为“女巫”。在本系列里，阿尔雷温是制作符文的附魔者（“the best enchantress in Elvala”“the rune I crafted”）。“女巫”带有 witch 的含义，但全系列（context.lua:760、779、785 等）都用这个译法，统一是一种风格选择。



## O052 | entry-03544

### C11 | entry-03544 | 存在问题

原文问及“**the treatment of the ogres**”，后续谈的是狂热分子为何囚禁、实验而不杀死食人魔；译文“**对食人魔进行治疗**”将处置方式误作医疗。证据：`fay-willows.lua:539` 及同段问答。



## O053 | entry-03544

### C12 | entry-03544 | 存在问题

叙述者原话“**I see little reason for you or any shalore to care**”在译文的回答中缺失，漏掉了他对女巫及永恒精灵为何关心此事的质疑。证据：`fay-willows.lua:541`。



## O054 | entry-03544

### C12 | entry-03544 | 存在问题
- **原文短引**："the ones involving the treatment of the ogres have stuck out in my mind the most."
- **译文短引**：“那些涉及对食人魔进行治疗的问题在我脑海中最为突出。”
- **具体问题**：此处上下文是年轻法师追问狂热分子俘获食人魔后为何没有当场杀死他们、究竟在对食人魔做什么残酷实验（"treatment" 指蒙面狂热分子对食人魔的处置、虐待与折磨手段）。译文望文生义将 "treatment" 误译为医疗上的“治疗”，将狂热邪教徒对食人魔的残害折磨匪夷所思地变成了“给食人魔治病”，造成荒谬的逻辑颠倒。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:540-545`，后文阿尔雷温明确提出 "what purpose do you think they would be kept alive?"。



## O055 | entry-03544

### C13 | entry-03544 | 存在问题

原文是将军“**Standing above the young shalore**”，并由“**him**”抱起双臂；译文成了“**女巫站在年轻的永恒精灵前方……双臂合拢**”，颠倒人物关系和动作主体。证据：`fay-willows.lua:549`。



## O056 | entry-03544

### C13 | entry-03544 | 存在问题
- **原文短引**："For what purpose would you attempt to discern any meaning from their mad actions anyways? I see little reason for you or any shalore to care."
- **译文短引**：“不管怎样，你想从他们疯狂的行为中辨别出什么意义？”
- **具体问题**：原文菲·维莉欧斯所说的整整一句话 "I see little reason for you or any shalore to care."（我认为你或任何永恒精灵都没有理由去关心这件事）在译文中被彻底漏译，丢失了自然精灵对永恒精灵漠不关心冷酷态度的直接对白表达。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:548`，文本行完全缺失对应译文。



## O057 | entry-03544

### C14 | entry-03544 | 存在问题

同一句“**she slowly caught her breath**”指女巫逐渐缓过气；译文“**她慢慢地屏住呼吸**”写成停止呼吸。证据：`fay-willows.lua:549`。



## O058 | entry-03544

### C14 | entry-03544 | 存在问题
- **原文短引**："Standing above the young shalore as she slowly caught her breathe, I could see him fold his arms."
- **译文短引**：“我看到女巫站在年轻的永恒精灵前方，她慢慢地屏住呼吸，双臂合拢。”
- **具体问题**：
  1. 人物身份错乱：前文明确女巫阿尔雷温正是“年轻的永恒精灵”（the young shalore），施法开启迷雾隧道后精疲力竭仰面瘫倒在地上大口喘气；而将军（男性，him）大步走来居高临下站在瘫倒的女巫上方抱起双臂。译文将其拆解为“女巫站在年轻的永恒精灵前方”，凭空制造了两个人物，且让瘫倒在地的女巫站了起来。
  2. 动作与生理状态误译："caught her breath" 指缓过气来、喘匀呼吸，译文误译为反向的“屏住呼吸”。
  3. 动作归属颠倒：抱臂者是将军（"I could see him fold his arms"），译文误将动作归于女巫（“她……双臂合拢”），丢失了主语代词 him 指向的将军体态威严。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:568-574`。



## O059 | entry-03544

### C15 | entry-03544 | 存在问题
- **原文短引**："As the general began to approach the enchantress... given several anesthetic infusions"
- **译文短引**：“当将军走进向巫时……给了我几次麻醉剂注射”
- **具体问题**：
  1. 错字与断句失误：“当将军走进向巫时”属于未校对的字词粘连错误（应为“走向女巫”）。
  2. 游戏术语误译：游戏设定中的 "infusions" 是反魔/自然体系的“纹身”，前文与后文（如再生纹身）均严格遵循术语，此处将 "anesthetic infusions" 误译为现代医疗概念“麻醉剂注射”，破坏世界观统一性。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:571, 582`；术语表 `infusions 纹身 T.GAME.TALENT_CATEGORY`。



## O060 | entry-03544

### C16 | entry-03544 | 存在问题

原文“questions … involving the treatment of the ogres”，译文“涉及对食人魔进行治疗的问题”。后面的提问全部围绕狂热者为何囚禁、实验而不直接杀死食人魔，treatment 在此指对待方式，译文误成医疗。证据：冻结条目第二段。



## O061 | entry-03544

### C16 | entry-03544 | 存在问题
“the ones involving the treatment of the ogres” 译为“那些涉及对食人魔进行治疗的问题”。这里的 treatment 指食人魔受到的对待，也就是被邪教徒囚禁、做实验。后面的提问（“why … they wouldn't have killed the ogres outright”“For what purpose … kept alive”）都围绕这一点，与医疗无关。



## O062 | entry-03544

### C17 | entry-03544 | 存在问题

原文“For what purpose … would be kept alive?”，译文“你认为他们为什么会活着？”原文询问迫害者刻意留活口的目的，译文变成食人魔为何存活，丢失施动者及有意保留生命这一前提。证据：冻结条目第二段，紧接“不直接杀死”的讨论。



## O063 | entry-03544

### C17 | entry-03544 | 存在问题
“what more reason is there for someone who hates magic to just kill them then and there” 译为“在各处屠杀他们”。“then and there” 是“当场”，被错成了地点上的“各处”。



## O064 | entry-03544

### C18 | entry-03544 | 存在问题

原文“I see little reason for you or any shalore to care.”没有对应译文。该句明确表现菲对女巫乃至整个永恒精灵族群关心此事的怀疑，删去后人物态度和下一句回应的语境均减弱。证据：冻结条目第三段。



## O065 | entry-03544

### C18 | entry-03544 | 存在问题
原文 “…from their mad actions anyways? I see little reason for you or any shalore to care.” 的后一句完全漏译。这句是菲对永恒精灵的冷淡表态，下文对方回答 “perhaps you are right” 正是回应它。



## O066 | entry-03544

### C19 | entry-03544 | 存在问题

原文将军站在年轻永恒精灵上方，“I could see him fold his arms”；译文“我看到女巫站在年轻的永恒精灵前方……双臂合拢”。站立和抱臂的执行者从将军变成女巫，还把同一名女巫拆成两个角色。证据：冻结条目将军到场段落。



## O067 | entry-03544

### C19 | entry-03544 | 存在问题
“almost immediately the misty smoke began to part” 译为“迷雾几乎立刻烟消云散”。原文是雾“开始分开”，随后形成隧道；译文说雾完全消散，和紧接着的“一条……隧道形成在我们面前”以及后文“帷幕也随之合上了”相矛盾。



## O068 | entry-03544

### C20 | entry-03544 | 存在问题

同句“she slowly caught her breathe”译成“她慢慢地屏住呼吸”。原文承接施法后大口喘气，表示逐渐缓过气来；屏住呼吸是相反的动作。证据：冻结条目女巫耗尽精力及将军到场两段。



## O069 | entry-03544

### C20 | entry-03544 | 存在问题
“Finished, she too fell backwards to the ground” 译为“说完，她也倒在地上”。“Finished” 指她施法结束，而她此前没有说话，“说完”凭空加了一个动作。



## O070 | entry-03544

### C21 | entry-03544 | 存在问题

原文要求讲述“after you had left **for** the Nargol Kingdom”直到返回埃尔瓦拉的经历；译文变成“离开纳格尔王国回到埃尔瓦拉的路途中”。调查起点被从前往纳格尔之前推后至离开纳格尔，排除了在王国内的经历。证据：冻结条目最后一段；entry-03546 随即明确复述了王国内的经历。



## O071 | entry-03544

### C21 | entry-03544 | 存在问题
“made a simple statement in between deep breaths” 译为“在两次深呼吸之后作了一个简单的陈述”。原文是在大口喘气的间隙断续说话，译文变成恰好两次深呼吸之后才说，时序和数量都错了。



## O072 | entry-03544

### C22 | entry-03544 | 存在问题

译文“当将军走进向巫时”存在明显文字损坏，“向巫”也无法在该句中形成有效人物称谓。原文为“the general began to approach the enchantress”，动作关系本来明确。证据：冻结条目将军到场段落。



## O073 | entry-03544

### C22 | entry-03544 | 存在问题
“当将军走进向巫时”字词残缺（应为“走向女巫”），宾语无法辨认。原文 “As the general began to approach the enchantress”。



## O074 | entry-03544

### C23 | entry-03544 | 存在问题
“Standing above the young shalore as she slowly caught her breathe, I could see him fold his arms.” 译为“我看到女巫站在年轻的永恒精灵前方，她慢慢地屏住呼吸，双臂合拢。”
- 原文是将军（him）站在倒地的年轻永恒精灵（也就是女巫本人）身旁俯视她、抱起双臂，而她慢慢缓过气来。
- 译文把动作者换成“女巫”，把同一个人拆成了两个人。
- “caught her breath”（缓过气）被译成“屏住呼吸”，意思相反。
- 抱臂的主语也从将军变成了她。



## O075 | entry-03544

### C24 | entry-03544 | 存在问题
“what transpired after you had left for the Nargol Kingdom to the point when you came back to Elvala” 译为“有关你离开纳格尔王国回到埃尔瓦拉的路途中”。原文的时间段是从动身前往纳格尔王国起，直到回到埃尔瓦拉，包括在纳格尔王国的经历（下一条 03546 确实详细讲了“在纳格尔王国的经历”）。译文缩成了离开纳格尔之后的归途。



## O076 | entry-03544

### C25 | entry-03544 | 存在问题
“I realize you have only woken up, but…” 译为“你终于醒了，但……”。原文是体谅对方“刚醒”，带歉意地转折；“终于醒了”变成了带催促意味的完成，“但”字前后的让步关系也随之丢失。



## O077 | entry-03544

### C26 | entry-03544 | 仅建议
“Rune of Return” 在本条译为“回归符文”，而同系列多数处（context.lua:243、525、743、745、749、939、1113）作“返回符文”。不属于术语库条目，但同一物品的译名不统一。



## O078 | entry-03544

### C27 | entry-03544 | 仅建议
“‘这么落后’吗”后面缺问号。



## O079 | entry-03546

### C15 | entry-03546 | 存在问题

原文“**the same rage that I had filled those fanatics with**”说叙述者曾把愤怒灌入狂热分子；译文“**我从前对那些狂热分子充满的愤怒**”改成叙述者对他们怀有愤怒，作用对象反转。证据：`fay-willows.lua:562`。



## O080 | entry-03546

### C16 | entry-03546 | 存在问题

原文“**turned my head to look away from the enchantress**”，译文“**转过头去看那个女巫**”，回避视线变为看向她。证据：`fay-willows.lua:568`。



## O081 | entry-03546

### C16 | entry-03546 | 存在问题
- **原文短引**：""I wouldn't know why that would be.” I replied as I turned my head to look away from the enchantress."
- **译文短引**：““我不知道为什么会这样。”我转过头去看那个女巫，回答说。”
- **具体问题**：原文 "look away from the enchantress" 明确是指菲扭过头、将目光避开女巫（不看她），紧随其后的下一句正是“尽管我看不见那个永恒精灵的脸（Despite not being able to see the shalore's face）”。译文完全反向误译为“转过头去【看】那个女巫”，直接造成上下文“看着她却又看不见她的脸”的前后自相矛盾。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:620-621`，动作方向与后文逻辑自毁。



## O082 | entry-03546

### C17 | entry-03546 | 存在问题
- **原文短引**："you have been in this hospital bed for several months now, despite injuries that should have healed in a few weeks."
- **译文短引**：“你已经在这张病床上躺了几个月了，尽管几周后你应该会痊愈。”
- **具体问题**：时态与虚拟事实倒错。原文指出菲已经在病床上躺了几个月，而她所受的伤势按常理“本来应该在几周内痊愈（should have healed）”，这是过去与虚拟反差。译文误译为将来时“几周后你应该会痊愈”，彻底颠倒了时间线和治疗师震惊的因由。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:615-617`。



## O083 | entry-03546

### C18 | entry-03546 | 存在问题
- **原文短引**："You wouldn't perhaps have an explanation for why this is?"
- **译文短引**：“你可能没有知道这是为什么？”
- **具体问题**：原文为典型的委婉疑问句（“也许你碰巧知道这是怎么回事/对此有什么解释吗？”）。译文呈现为严重不通顺的语病畸形句“你可能没有知道这是为什么？”，语法破碎。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:617`。



## O084 | entry-03546

### C23 | entry-03546 | 存在问题

原文“the same rage that I had filled those fanatics with”，译文“就像我从前对那些狂热分子充满的愤怒一样”。原文是把愤怒灌入狂热者体内，译文改成自己对他们怀有愤怒，改变了情绪作用对象。证据：`L/fay-willows.lua:562`，同段与把愤怒灌入女巫体内作比较。



## O085 | entry-03546

### C24 | entry-03546 | 存在问题

原文“that mostly concludes … what Aranion sent me here for”，译文“这基本上可以断定，艾伦尼恩派我来这里是为了什么”。原文宣布受命进行的询问已经基本完成，译文变成推断受命目的。证据：冻结条目第三段，随后转入治疗师另托的问题。



## O086 | entry-03546

### C25 | entry-03546 | 存在问题

原文伤势“should have healed in a few weeks”，译文“尽管几周后你应该会痊愈”。原文比较通常只需几周与实际已躺了几个月，译文却预测从现在起几周后痊愈，改变时序。证据：冻结条目第三段。



## O087 | entry-03546

### C26 | entry-03546 | 存在问题

原文“turned my head to look away from the enchantress”，译文“转过头去看那个女巫”。避开对方的动作被翻成看向对方，也与下一句“看不见……脸”形成矛盾。证据：冻结条目第四段。



## O088 | entry-03546

### C27 | entry-03546 | 存在问题

原文“How were you so paramount in the ogres getting here?”，译文“你怎么能在食人魔面前这么重要？”询问的是菲为何对食人魔成功抵达起决定性作用，译文变成在食人魔心目中的重要地位。证据：冻结条目第五段，前后都在追问战斗贡献与生还原因。



## O089 | entry-03546

### C28 | entry-03546 | 存在问题

原文“You wouldn't perhaps have an explanation …?”是委婉询问原因；译文“你可能没有知道这是为什么？”句法不成立，并加入了难以理解的否定。读者无法清楚获得原有提问。证据：冻结条目第三段。



## O090 | entry-03546

### C28 | entry-03546 | 存在问题
“So, that mostly concludes more or less what Aranion sent me here for” 译为“所以，这基本上可以断定，艾伦尼恩派我来这里是为了什么”。原文的 “concludes” 是“差不多问完了”（交代的任务已完成），被译成“可以推断出目的”，意思偏了。



## O091 | entry-03546

### C29 | entry-03546 | 存在问题
“despite injuries that should have healed in a few weeks” 译为“尽管几周后你应该会痊愈”。原文是“这些伤本该几周就好”，与“已经躺了几个月”形成对比。译文变成对将来的预测，把“恢复异常缓慢”这个要点说反了。



## O092 | entry-03546

### C30 | entry-03546 | 存在问题
“I replied as I turned my head to look away from the enchantress” 译为“我转过头去看那个女巫”，方向反了。下一句 “Despite not being able to see the shalore's face” 说明她是把头转开。



## O093 | entry-03546

### C31 | entry-03546 | 存在问题
“How were you so paramount in the ogres getting here?” 译为“你怎么能在食人魔面前这么重要？”。原文问的是“你在把食人魔带到这里一事中为何如此关键”，译文丢了“把他们带到这里”这个所指，变成了意义不明的“在食人魔面前”。



## O094 | entry-03546

### C32 | entry-03546 | 仅建议
“你可能没有知道这是为什么？”不合语法，大意还能看懂。



## O095 | entry-03548

### C17 | entry-03548 | 存在问题

“**Rebuilding Anew**”描述重新建设的行动；“**焕然一新**”描述已呈现的新面貌，标题的过程信息丢失。证据：`fay-willows.lua:609`。



## O096 | entry-03548

### C29 | entry-03548 | 仅建议

“Rebuilding Anew”强调重新建设，“焕然一新”更侧重结果。正文同时涉及定居、重建生活和学习新技能，现标题可以概括这些变化；区别主要在叙事重心，未据此认定缺陷。证据：`L/fay-willows.lua:610`、`:612`、`:614`。



## O097 | entry-03548

### C33 | entry-03548 | 仅建议
“Rebuilding Anew” 译为“焕然一新”，淡化了“重建”这个动作（本章内容是食人魔“rebuild new lives”）。作为标题的意译可以接受。



## O098 | entry-03549

### C18 | entry-03549 | 存在问题

“**Dead On Arrival**”指抵达时已经死亡；“**死亡到来**”指死亡降临，时序和主体均不同。证据：`fay-willows.lua:637`。



## O099 | entry-03549

### C19 | entry-03549 | 存在问题
- **原文短引**："Escapades of Fay Willows [Book 5, Chapter 1] - Dead On Arrival"
- **译文短引**：“菲·维莉欧斯的冒险 [第5卷，第1章] - 死亡到来”
- **具体问题**："Dead On Arrival"（DOA）是英语固定医学/法律习语，意为“送达时已死亡/到场即死”，在此呼应本章开头卫兵脚下出现的腐烂尸体以及食尸鬼袭击。译文将其拆解并误解为“死亡（Dead）到来（On Arrival）”，将形容状态的介词短语曲解为主谓结构的“死亡到来”，属于对固定英语习语的常识性误译。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:680`，DOA 固定习语语义。



## O100 | entry-03549

### C30 | entry-03549 | 仅建议

“Dead On Arrival”具有“抵达时已经死亡”的惯用含义；“死亡到来”未保留这一表达层次。但本章实际讲述尸体和不死生物抵达、袭击城市，现标题仍与事件相符，因此仅记录标题双关表现上的偏好。证据：`L/fay-willows.lua:642`、`:650`、`:652`。



## O101 | entry-03549

### C34 | entry-03549 | 仅建议
“Dead On Arrival” 译为“死亡到来”，没有保留习语“到场即已死亡”的双关。本章开篇写食尸鬼和腐尸，“死亡到来”勉强贴合情节。标题意译，属于偏好问题。



## O102 | entry-03551

### C19 | entry-03551 | 存在问题

“**Leadership From The Front**”指在前线亲自带领；“**前线的领袖**”只标示领袖所在位置，漏掉其领导方式。证据：`fay-willows.lua:683`。



## O103 | entry-03555

### C20 | entry-03555 | 存在问题

死灵法师原话是从纳格尔人对抗孔克雷夫的经历中获得骨巨人灵感，并另称纳格尔人使用过死灵法术；译文“**这是他们……使用的武器**”进一步断言纳格尔人当年使用骨巨人，原文没有此断言。证据：`fay-willows.lua:757`。



## O104 | entry-03555

### C20 | entry-03555 | 存在问题
- **原文短引**："Snapping my eyes to what had hit me, I immediately realized that the bone giant was indeed not defeated"
- **译文短引**：“我猛地一眨眼睛，立刻意识到这个骨巨人并没有被打败”
- **具体问题**："Snapping my eyes to what had hit me" 意为“猛地将目光投向刚才击中我的事物”。译文误译为“我猛地一眨眼睛”，完全曲解动作（将转动目光看目标误译为闭合眼皮眨眼），并彻底遗漏了目光投向的具体宾语 "to what had hit me"。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:745`。



## O105 | entry-03555

### C21 | entry-03555 | 存在问题
- **原文短引**："I rushed into the bone giant, taking a quick swipe that knocked a few bones away... my heat beam rune... my heat beam rune"
- **译文短引**：“我冲进了骨巨人……热能射线符文……热束符文”
- **具体问题**：
  1. 动作误译："rushed into the bone giant" 在近战交锋语境下是指向骨巨人冲锋/扑去交战，译文直译为“冲进了骨巨人”，字面含义变成了进入骨巨人身体内部。
  2. 同条目内译名割裂：同在 entry-03555 内，刻印在左臂上的同一枚 "heat beam rune"，第7段和第10段译为“热能射线符文”，第8段却突兀译为“热束符文”，同一段落间同一术语翻译不一致。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:763, 770, 775, 781`。



## O106 | entry-03555

### C31 | entry-03555 | 存在问题

原文“Snapping my eyes to what had hit me”，译文“我猛地一眨眼睛”。原文是迅速把目光转向袭击者，译文改成眨眼，丢失视线转移的动作。证据：冻结条目第三段。



## O107 | entry-03555

### C32 | entry-03555 | 存在问题

原文死灵法师说自己从纳格尔人对抗孔克雷夫的战争中得到灵感，并补充他们使用过死灵术；译文新增“这是他们……使用的武器”。原文没有断言纳格尔人当时已经使用这种骨巨人，译文把灵感来源升级为具体武器的历史。证据：冻结条目第三段。



## O108 | entry-03555

### C33 | entry-03555 | 存在问题

原文“causing it to stumble a bit”，译文“导致它绊倒了”。原文只是略微踉跄，译文变成已经倒地，改变战斗状态。随后骨巨人仍继续维持形体、主动攻击，进一步支持两种动作不能等同。证据：冻结条目全力攻击骨巨人中段的段落。



## O109 | entry-03555

### C34 | entry-03555 | 仅建议

同一 heat beam rune 出现“热能射线符文”和“热束符文”，Rune of Return 又与邻条“回归符文”呈现不同措辞。上下文仍能辨认同一刻印，允许的术语子集也没有规定这些名称，因此只记录局部称谓一致性的建议，不认定强制术语错误。



## O110 | entry-03555

### C35 | entry-03555 | 存在问题
“Snapping my eyes to what had hit me” 译为“我猛地一眨眼睛”。原文是猛地把视线转向打中自己的东西，译成了眨眼，动作和对象都丢了。



## O111 | entry-03555

### C36 | entry-03555 | 仅建议
同一条里 “heat beam rune” 有两种译法，“热能射线符文”（3 处）和“热束符文”（1 处），读者可能以为是两种不同的符文。不属于术语库条目。



## O112 | entry-03557

### C35 | entry-03557 | 仅建议

“From the Brink of Death”译成“自死亡的边缘”有明显直译感，但标题允许省略谓语，来源方向和濒死含义仍在。没有足够依据把这种标题措辞判为信息错误。



## O113 | entry-03558

### C21 | entry-03558 | 存在问题

“**seekers of forbidden knowledge**”译成“**寻求着禁忌知识的先知**”，无依据地赋予这群求知者“先知”身份。证据：`kroshkkur.lua:28`。



## O114 | entry-03558

### C22 | entry-03558 | 存在问题
- **原文短引**："Intelligent beings who do not belong anywhere else, seekers of forbidden knowledge and those who have seen too much for mortal eyes to bear are just a few who have made their homes here."
- **译文短引**：“他们当中有在别处无处容身的智慧生物、有寻求着禁忌知识的先知，还有目睹了太多凡人的目光所不能承受之物的人。”
- **具体问题**：原文 "seekers of forbidden knowledge" 是指“禁忌知识的探求者/求索者”。译文将 "seekers" 篡改为了具有预言能力或宗教神职色彩的“先知”（Prophets），虚构并曲解了这群地下流亡者的身份定位。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua` 及 `kroshkkur.lua:34`，词义直接篡改。



## O115 | entry-03558

### C36 | entry-03558 | 存在问题

原文“seekers of forbidden knowledge”，译文“寻求着禁忌知识的先知”。寻求知识的人不等于先知，译文新增具体身份或能力。证据：`L/kroshkkur.lua:28`，原文在列举定居者群体。



## O116 | entry-03558

### C37 | entry-03558 | 存在问题
“seekers of forbidden knowledge” 译为“寻求着禁忌知识的先知”。“seekers” 只是“追寻者”，“先知”是凭空加的身份。原文列举的是流亡者类别，不含“先知”。



## O117 | entry-03558

### C38 | entry-03558 | 仅建议
“当做害虫一样轻轻扫开”增添了“害虫”这个比喻，“发现了……禁忌魔法”增添了“禁忌”。都是润色性增译，没有改变叙述主旨。



## O118 | entry-03559

### C22 | entry-03559 | 存在问题

奎科加任命的是自己的“**librarians**”；译文“**记录者**”只保留工作，漏掉图书馆员身份，而下句的争议正围绕那座图书馆的记录。证据：`kroshkkur.lua:103`。



## O119 | entry-03559

### C23 | entry-03559 | 仅建议
- **原文短引**："appointing its own librarians to record its tales. Since there are no surviving records of this library existing"
- **译文短引**：“指派了自己的记录者来记录自己的故事，但并没有证据表明有这样一个图书馆存在”
- **具体问题**：原文中奎科加指派的是 "librarians"（图书管理员/典籍编纂者），因此紧随其后的句子自然提及 "this library"（这座图书馆）。译文将 librarians 译为“记录者”，导致后文突然冒出“这样一个图书馆”在中文上下文逻辑承接中稍显突兀。建议统合为“图书典籍编纂者/图书管理员”。
- **状态**：仅建议
- **偏好说明**：原译文对奎科加神话矛盾性的事实传递清晰，“记录者”在宽泛意义下能解释记录故事的行为，无实质机制或事实错误，故仅作为行文连贯性偏好。



## O120 | entry-03559

### C37 | entry-03559 | 存在问题

原文“appointing its own librarians to record its tales”，译文“指派了自己的记录者来记录自己的故事”。记录职能保留，但图书馆员身份被删去，导致下一句“这样一个图书馆”失去前文建立的关联。证据：`L/kroshkkur.lua:103`。



## O121 | entry-03559

### C39 | entry-03559 | 仅建议
“librarians” 译为“记录者”，后文“这样一个图书馆”就少了照应的前词。补回“图书管理员”会更连贯，意思本身没错。



## O122 | entry-03560

### C23 | entry-03560 | 存在问题

故乡由“**fragmented continents**”组成，译文为“**一片破碎的大陆**”，复数大陆变成单块大陆。证据：`kroshkkur.lua:141`。



## O123 | entry-03560

### C38 | entry-03560 | 存在问题

原文“a collection of fragmented continents”，译文“一片破碎的大陆”。原文是多块破碎大陆组成的集合，译文收窄为一片大陆，改变世界地理构成的数量信息。证据：`L/kroshkkur.lua:141`。



## O124 | entry-03560

### C40 | entry-03560 | 仅建议
“a collection of fragmented continents” 译为“一片破碎的大陆”，“多块大陆”的复数感变弱了，但“聚集在一起”仍然表达了由碎块组成。



## O125 | entry-03562

### C24 | entry-03562 | 存在问题

原文“**despite the failure of her fellow students and the horror of what she saw**”分别指同学们的失败和她所见的恐怖；译文“**同学们失败地召唤出了……恐怖**”把失败直接限定为召唤失败，与开头不可名状之物已被召唤的叙述冲突。证据：`misc.lua:100`。



## O126 | entry-03562

### C24 | entry-03562 | 存在问题
- **原文短引**："She believed that, despite the failure of her fellow students and the horror of what she saw, The Teacher's wisdom still had value"
- **译文短引**：“她坚信，尽管她的同学们失败地召唤出了她所看到的无法言说的恐怖，但导师的智慧教诲……仍然有着无法替代的价值。”
- **具体问题**：语法关系严重粘连错位。原文为两个并列的名词短语：`despite [the failure of her fellow students] and [the horror of what she saw]`（尽管同学们遭遇了失败，尽管她亲眼目睹了恐怖景象）。译文却将 "failure" 强行当作副词“失败地”，并与第二项拼合，拼凑出“同学们失败地召唤出了……恐怖”这种不知所云的错乱语法结构，曲解了召唤失败且只有她一人生还的前置背景。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/misc.lua:101`，英语句式结构与对应译文语法错误。



## O127 | entry-03562

### C25 | entry-03562 | 存在问题

“**pass on the power of entropy**”译为“**传授有关熵的力量的知识**”，将传递熵的力量改为仅传授相关知识。证据：`misc.lua:100`。



## O128 | entry-03562

### C25 | entry-03562 | 存在问题
- **原文短引**："After all, is it not better to know about the horrors out there than it is to be ignorant of their existence?"
- **译文短引**：“毕竟，比起那些恐怖本身，对恐怖的无知不是更加糟糕吗？”
- **具体问题**：比较对象完全错构与遗漏。原文所对比的两个主体是 `to know about the horrors out there`（去了解外面的恐怖）与 `to be ignorant of their existence`（对其存在一无所知），主旨是“了解恐怖胜过无知”。译文遗漏了第一项“去了解”，并无中生有地构拟出“比起那些恐怖本身”，将原句思想完全曲解为“无知比恐怖实体本身更糟糕”。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/misc.lua:103`，逻辑比较项彻底错乱。



## O129 | entry-03562

### C39 | entry-03562 | 存在问题

原文比较“了解恐怖存在”与“不知道它们存在”；译文“比起那些恐怖本身，对恐怖的无知不是更加糟糕吗？”改成比较“恐怖本身”与“无知”。这是不同的论证：前者说明知识优于无知，后者声称无知比恐怖实体还糟。证据：`L/misc.lua:100`。



## O130 | entry-03562

### C40 | entry-03562 | 存在问题

原文“The Teacher's wisdom still had value”，译文“仍然有着无法替代的价值”。“仍有价值”没有表达不可替代性，译文额外强化了幸存者对导师学说的评价。证据：`L/misc.lua:100`。



## O131 | entry-03562

### C41 | entry-03562 | 存在问题
“is it not better to know about the horrors out there than it is to be ignorant of their existence?” 译为“比起那些恐怖本身，对恐怖的无知不是更加糟糕吗？”。原文比较的是“了解恐怖”和“对其一无所知”，译文换成了“恐怖本身”和“无知”，比较项错了，论证也变了。



## O132 | entry-03562

### C42 | entry-03562 | 仅建议
“it” 译为“他”。另外 “somewhere far beyond Eyal” 增译为“遥远繁星中的家园”，属于润色性增译。



## O133 | entry-03563

### C26 | entry-03563 | 存在问题

“**I won't go back, not after what happened**”是因已经发生的惨事而不愿回去；“**不管发生了什么都不会**”变成不论发生什么都不回去，因果与时间指向改变。证据：`zones.lua:50`。



## O134 | entry-03563

### C26 | entry-03563 | 存在问题
- **原文短引**："The whispers... Even as I'm running away, the whispers don't stop."
- **译文短引**：“那些低语……我想要逃跑，可这些低语丝毫没有停止。”
- **具体问题**：原文 "Even as I'm running away" 是现在进行时表示实际奔逃行动（即便/哪怕我正在逃跑途中）。译文误译为意愿态“我想要逃跑”，将客观正在发生的奔逃动作篡改为主观心理愿望。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/zones.lua:50`。



## O135 | entry-03563

### C27 | entry-03563 | 存在问题
- **原文短引**："I won't go back, not after what happened."
- **译文短引**：“我绝不会回去，不管发生了什么都不会。”
- **具体问题**：时序与因果逻辑倒错。原文 "not after what happened" 是回顾已经发生的惨案（“在发生了那件事之后，我绝不可能回去”）。译文将其误译为面向未来的让步状语“不管发生了什么都不会”（whatever may happen），将基于既成事实的因果决绝扭曲为面对未知事件的假设。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/lore/zones.lua:51`。



## O136 | entry-03563

### C41 | entry-03563 | 存在问题

原文“Even as I'm running away”，译文“我想要逃跑”。原文已在逃跑，译文只表达逃跑意愿，改变行动是否已经发生。证据：`L/zones.lua:50`。



## O137 | entry-03563

### C42 | entry-03563 | 存在问题

原文“I won't go back, not after what happened”，译文“不管发生了什么都不会”。原文明确因已经发生的惨剧而拒绝返回，译文改成无论发生什么都不返回，丢失过去事件与决定之间的因果关系。证据：`L/zones.lua:50`，下一句立即讲述同伴全部遇难。



## O138 | entry-03563

### C43 | entry-03563 | 存在问题

原文“All of my mortal emotions, thoughts and dreams”，译文“思维、情感，还有那份挥之不去的噩梦”。原文概括全部内心活动，译文把 dreams 限定为一个特定、持续的噩梦，缩小被看透的内容范围。证据：`L/zones.lua:50`。



## O139 | entry-03563

### C43 | entry-03563 | 存在问题
“I won't go back, not after what happened.” 译为“我绝不会回去，不管发生了什么都不会。”。原文是“发生了那样的事之后，我绝不回去”，是因果关系；译文变成“无论发生什么”的无条件让步，而下文正是在交代“发生了什么”。



## O140 | entry-03563

### C44 | entry-03563 | 存在问题

原文“a horrid, psychic shriek”，译文“恐怖，癫狂的尖笑”。psychic 描写精神性或心灵层面的尖啸，并不等于癫狂，译文丢失声音作用方式、增加疯狂状态。证据：`L/zones.lua:50`；同文件 `:41` 已明确这些存在正在触及人物心智。



## O141 | entry-03563

### C44 | entry-03563 | 存在问题
“It wants me to return so it can finish what it started.” 译为“它要我回去，完成它的任务。”。原文的动作者是“它”，要了结它开了头的事（结合前文，就是吞噬他）。译文最自然的读法是“我回去替它完成任务”，动作者和目的都变了。



## O142 | entry-03563

### C45 | entry-03563 | 仅建议
“All of my mortal emotions, thoughts and dreams” 中的 dreams 译为“那份挥之不去的噩梦”。结合前文 “just like in my dreams”，这个理解说得通，只是收窄了原文的泛指。



## O143 | entry-03563

### C45 | entry-03563 | 存在问题

原文“so **it** can finish what it started”，译文“它要我回去，完成它的任务”。原文让怪物完成自己已经开始的事情；译文自然读作要求“我”回去执行怪物的任务，同时遗漏“已经开始、尚未完成”的信息。证据：`L/zones.lua:52`。



## O144 | entry-03563

### C46 | entry-03563 | 存在问题

原文“he did not make it back to Zigur”，译文“他并没能把这个消息带回伊格”。原文说明人物没有返回，译文只说明消息没有送达，降低了对人物去向的断言。证据：`L/zones.lua:52`。地点“伊格”和教团“伊格兰斯”的区分本身正确。



## O145 | entry-03564

### C27 | entry-03564 | 存在问题

冒险者循环中的“**spend all the loot money you made**”在译文变成“**把装备卖掉换成钱**”，增加卖装备动作，却漏掉花掉所得钱财。证据：`zones.lua:131`。



## O146 | entry-03564

### C46 | entry-03564 | 存在问题
“grab some loot, spend all the loot money you made and repeat” 译为“捡捡装备，把装备卖掉换成钱，然后再重复一遍”。“把钱花光”被改成“卖装备换钱”。原文循环的关键是钱花光了才要再去冒险，这一环丢了。



## O147 | entry-03564

### C47 | entry-03564 | 存在问题

原文“spend all the loot money you made”，译文“把装备卖掉换成钱”。花掉所得金钱被改成出售装备挣钱，改变冒险循环中的具体行为。证据：`L/zones.lua:131`。



## O148 | entry-03564

### C48 | entry-03564 | 存在问题

原文“The way this stupid thing works doesn't make any sense”，译文“这种愚蠢的东西根本毫无意义”。原文抱怨装置的运作规律难以理解，译文否定整个东西的意义或价值，丢失与“尝试组合、寻找线索”直接关联的抱怨对象。证据：`L/zones.lua:131`。

格式方面，`:136` 的 `%s` 消费 `CultsDLC.effectGlyphsSequence("EGRESS_SPLATTER")`；译文保留了占位符及其独立位置，未发现该处显示结构问题。



## O149 | entry-03565

### C28 | entry-03565 | 存在问题

译文“**如果在过去 2 回合里目标消失在你的视线中**”可读作这段期间只要失去过视线便清除诅咒，漏掉**持续**失去视线的条件。快照中 `calamity.lua:46–50` 施加 `EFF_JINX`；`timed_effects.lua:1583–1591` 逐回合累计未见到来源者的次数，恢复视线即清零，累计到 2 才移除。原文写“more than 2 turns”，与快照实现的 `>= 2` 自身也有差异；此处确认的是译文丢失连续性，快照适用版本仍未固定。



## O150 | entry-03565

### C28 | entry-03565 | 存在问题
- **原文短引**："This can only be applied once per target per turn and will fade entirely if you break line of sight with your target for more than 2 turns."
- **译文短引**：“每个目标每回合只能受到一层诅咒。如果在过去 2 回合里目标消失在你的视线中，所有诅咒都会消退。”
- **具体问题**：机制时序触发条件曲解。
  - 源码实装逻辑：`timed_effects.lua:1584-1588` 规定，当且仅当施法者对目标持续失去视线（`not self:hasLOS(...)`），计数器 `eff.fading` 逐回合累加；一旦恢复视线立即清空 `eff.fading = nil`，只有连续失视达到 2 回合以上（`eff.fading >= 2`）才会移除整个效果。
  - 译文“如果在过去 2 回合里目标消失在你的视线中”表达的是“在过去两回合的窗口内发生过脱离视线（哪怕只有1回合脱离又出现）”，将“连续中断视野超过2回合”这一时延要求错误篡改为时间窗口内的瞬态事件。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/talents/demented/calamity.lua:71-72` 与 `sources/cults/tome-cults/data/timed_effects.lua:1584-1590`（已显式标注快照来源未固定）。



## O151 | entry-03565

### C47 | entry-03565 | 存在问题
原文：“will fade entirely if you break line of sight with your target for more than 2 turns”。
译文：“如果在过去 2 回合里目标消失在你的视线中，所有诅咒都会消退。”
- **文本层面**：原文的持续条件（超过/持续 2 回合）没了。“消失在视线中”是一次性事件，读者会理解为 2 回合内只要短暂失去视线就全部清除。
- **快照佐证**（`timed_effects.lua:1585-1590`，JINX `on_timeout`）：每回合失去视线时 `eff.fading+1`，`>=2` 才 `removeEffect`；一旦恢复视线就 `eff.fading = nil` 重置。也就是说，需要连续 2 回合没有视线。
- 快照适用于哪个目标版本仍待确认；文本层面的缺失可直接成立。



## O152 | entry-03565

### C49 | entry-03565 | 存在问题

原文描述失去视线持续一段时间才完全消退；译文“如果在过去 2 回合里目标消失在你的视线中”没有表达持续性，容易涵盖过去两回合中曾短暂离开、随后恢复视线的情况。

这是条件表述的信息缺失。快照 `E:1583` 的 `JINX.on_timeout` 连续失去 LOS 才增加 `fading`，恢复 LOS 后将其清空，支持这一持续性区别；具体回合阈值另见 C50。



## O153 | entry-03565

### C50 | entry-03565 | 待确认

原文“more than 2 turns”与允许快照中的实现不完全一致：`E:1585` 检测失去 LOS，`:1588` 在 `fading >= 2` 时移除效果。不能只凭英文认定译文使用“2 回合”就是新增的提前消退错误。

快照内可以确认计数逻辑；尚缺目标 DLC 版本与此快照对应的证据，以及据此采用何种回合边界描述的确认。本项涉及上游描述差异。



## O154 | entry-03566

### C51 | entry-03566 | 待确认

原译文都说每层幸运增加豁免和闪避，但快照 `FORTUNE.activate` 在 `E:1646` 给 `combat_def`、`:1647` 至 `:1649` 给三类豁免加入的是负值；`on_merge` 在 `:1628` 起则改为正的叠层值。

因此，首次施加与后续叠层在快照内确有不同，不能把原译文的概括当作已验证机制。这属于沿袭上游说明的疑点；目标 DLC 版本未固定，保留待确认。

另一方面，超过六层的免伤几率由 `:1637` 的 `avoid*(stackCount-6)` 累加，译文“每层”有源码支持，未把它另报为误译。



## O155 | entry-03566

**上游附注（不计为翻译 claim）**：entry-03566 对应的 FORTUNE 效果在快照中有一处实现与文本不一致。`activate`（`timed_effects.lua:1645-1646` 起）对闪避和豁免加的是 `-eff.power*eff.stacks`（负值），而 `on_merge`（1628 起）加的是正值。首次获得时实际是降低而不是英文说的“增加”。这是上游英文与实现之间的矛盾，译文忠实跟随英文，不属于翻译缺陷；目标版本是否仍然如此待确认。

## O156 | entry-03567

### C29 | entry-03567 | 存在问题

“**feeds on the timelines of others**”译成“**吸收他人时间**”，把他人的时间线改为一般时间，漏掉技能所描述的时间线概念。证据：`chronophage.lua:130–132`。



## O157 | entry-03567

### C48 | entry-03567 | 存在问题
原文第二句 “Up to %d stacks total will be applied to enemies each cast” 译为“每次施法可以释放最多 %d 层加速衰老”，漏了 “to enemies”。第一句也只译作“随机目标”，整段都没说明只作用于敌人。
- **快照**：`chronophage.lua` 的 Atrophy `callbackOnTalentPost` 只收集 `self:reactionToward(target) < 0` 的目标。
- 版本适用性同上，待确认。



## O158 | entry-03567

### C52 | entry-03567 | 存在问题

原文第二句明确“applied to **enemies**”，译文“每次施法可以释放最多……层加速衰老”没有敌方限定；第一句仍只写“随机目标”。整条中文因此丢失了效果只分配给敌人的信息。

文本遗漏可以直接确认。快照 `T/chronophage.lua` 的 `callbackOnTalentPost` 只收集 `self:reactionToward(target) < 0` 的目标，与原文限定一致；该快照对目标版本的适用性仍未固定。



## O159 | entry-03567

### C53 | entry-03567 | 待确认

原译文均概括为每次施法触发，但 `T/chronophage.lua` 的 `callbackOnTalentPost` 先排除 `ab.mode == "sustained"`，随后要求 `ab.is_spell and not ab.no_energy`。快照实现不包括所有法术使用情形，尤其排除了不消耗行动能量的法术。

这是原译文共同的机制概括疑点。缺目标 DLC 版本对应证据，不判作译文新增错误。



## O160 | entry-03568

### C29 | entry-03568 | 仅建议
- **原文短引**："summon three decaying devourers for %d turns... All its primary stats will be set to %d (based on your Magic stat)"
- **译文短引**：“召唤三个持续 %d 轮的腐败的吞噬者……（基于你的魔法属性）”
- **具体问题**：
  1. ToME4 的核心时间单位在技能描述中通行为“回合”（本技能树其他3条技能均使用“回合”），此处“持续 %d 轮”建议统一为“回合”。
  2. 角色基础属性 Magic 的标准术语为“魔力”（术语库 `Magic 魔力 T.GAME.STAT combat stat name existing global`），建议优化为“魔力属性”以与角色面板属性名精确对齐。
- **状态**：仅建议
- **偏好说明**：术语库中 Magic 状态为 existing，非强制改名依据；数值与技能机制传达无遗漏，故仅定为统一性优化建议。



## O161 | entry-03568

### C30 | entry-03568 | 存在问题

“**Many other stats will scale with level**”译为“**许多其他属性与技能等级相关**”。这里召唤物的 `level_range` 取召唤者 `self.level`，并有 `autolevel`；技能等级另用于所列技能等级等数值。译文把前者说成技能等级。证据：`controlled-horrors.lua:59–63、85–88、156–160`。



## O162 | entry-03568

### C49 | entry-03568 | 存在问题
“Many other stats will scale with level.” 译为“许多其他属性与技能等级相关”。原文只说 level，译文增译“技能”，把依据说错了。
- **快照**：`controlled-horrors.lua:59-68` 中 `level_range = {self.level, self.level}`、`combat_armor = self.level`、`resists = {all = math.min(50, self.level)}`、`combat.dam/atk/apr` 都随召唤者的角色等级变化。技能等级只决定持续时间、生命成长和子技能等级，这几项已经单独列出。
- 版本适用性待确认。



## O163 | entry-03568

### C50 | entry-03568 | 仅建议
“持续 %d 轮”，同组其他条目都用“回合”，用词不统一，意思不受影响。



## O164 | entry-03568

### C54 | entry-03568 | 待确认

原文“Many other stats will scale with level”，译文“许多其他属性与技能等级相关”。快照 `T/controlled-horrors.lua:59` 将召唤物等级关联至 `self.level`，`:65` 至 `:68` 的护甲、抗性及攻击参数也直接使用角色等级；技能等级则另在 `:85` 的 `resolvers.talents` 中使用。

快照证据支持译文混淆角色等级与技能等级，但 DLC 源码仓库及目标 commit 未固定，目标版本适用性仍待确认。



## O165 | entry-03569

### C30 | entry-03569 | 存在问题
- **原文短引**："It possesses the talents Mind Disruption and Mind Sear... All its primary stats will be set to %d"
- **译文短引**：“它拥有精神干扰和精神光束技能。它们的所有主属性将设为 %d……”
- **具体问题**：
  1. 明确适用的 preferred 术语违规：术语快照明确载明 `Mind Sear 心灵灼烧 T.GAME.TALENT talents talent name preferred core sear 指灼烧；技能机制虽为射线，名称不增译“光束”`。译文直接违背该强制要求，增译误作“精神光束”。
  2. 单复数代词粗疏套用：本技能仅召唤单个浮肿恐魔（"a decaying bloated horror", "All its primary stats"），译文直接照抄上一技能 entry-03568 的复数代词写为“它们的所有主属性”和“它们将继承”，人称代词单复数混乱。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/talents/demented/controlled-horrors.lua:265-267` 与 INPUT.md 末尾术语快照 Mind Sear 行。



## O166 | entry-03569

### C31 | entry-03569 | 存在问题

技能名“**Mind Sear**”译为“**精神光束**”；冻结术语子集对此技能名明确采用“**心灵灼烧**”，并说明不能因射线机制增译“光束”。召唤物确实获得 `T_MIND_SEAR`。证据：`controlled-horrors.lua:224–227、265–268`；INPUT 术语子集 `Mind Sear` 行。



## O167 | entry-03569

### C32 | entry-03569 | 存在问题

此条也把“**other stats will scale with level**”写成“**与技能等级相关**”；召唤物的 `level_range={self.level, self.level}`、`autolevel` 与单独设定的技能等级是两项不同数据。证据：`controlled-horrors.lua:202–207、224–227、265–270`。



## O168 | entry-03569

### C33 | entry-03569 | 存在问题

原文仅召唤“**a decaying bloated horror**”，后文指该单个恐魔；译文后两句改用“**它们的所有主属性**”“**它们将继承**”，将一名召唤物写成多名。运行代码也只构造一个 `NPC.new` 并添加一次。证据：`controlled-horrors.lua:187–188、249、265–270`。



## O169 | entry-03569

### C51 | entry-03569 | 存在问题
“Mind Sear” 译为“精神光束”。术语快照中 Mind Sear→“心灵灼烧”是 preferred（talent name），备注写明“名称不增译‘光束’”。这是明确适用的术语要求，而这里引用的正是技能名。



## O170 | entry-03569

### C52 | entry-03569 | 存在问题
同 C49：“Many other stats will scale with level.” 译为“与技能等级相关”。
- **快照**：`controlled-horrors.lua:202-215` 中 `level_range`、`combat_def = self.level`、`combat = {dam=25+self.level…}`、`combat_spellpower = self.level*3` 都随角色等级变化。
- 版本适用性待确认。



## O171 | entry-03569

### C53 | entry-03569 | 仅建议
召唤物只有一个浮肿恐魔，后两句却用“它们”，指代单复数不一致，但对象不会被误认。



## O172 | entry-03569

### C55 | entry-03569 | 待确认

本条同样把“scale with level”解释成“与技能等级相关”。快照 `T/controlled-horrors.lua:202`、`:208` 至 `:211` 使用 `self.level` 设置等级、护甲、攻击及强度，`:224` 起才单独设置技能等级。

与 C54 相同，快照中的区别已核验；目标 DLC 版本尚未固定，不能据此直接关闭版本适用性缺口。



## O173 | entry-03569

### C56 | entry-03569 | 存在问题

原文明确列出技能“Mind Sear”，译文“精神光束”与冻结术语子集的 preferred 名称“心灵灼烧”冲突。该处是在列举拥有的具名技能，适用技能名语境，不能因为机制是射线就把名称增译成“光束”。

证据：本包术语快照 `Mind Sear` 条目；`T/controlled-horrors.lua:226` 的 `Talents.T_MIND_SEAR` 也确认所指技能。



## O174 | entry-03570

### C31 | entry-03570 | 存在问题
- **原文短引**："If the target fails a magical save against your Spellpower, its appearance turns into that of a horror for %d turns, making all other creatures hostile to it."
- **译文短引**：“如果目标生物未能通过魔法豁免，%d 回合内它的相貌将转变为恐魔，令周围其他生物与之敌对。”
- **具体问题**：遗漏核心机制对抗属性。在 ToME4 豁免机制中，豁免检定必须对抗施法者的特定强度属性（此处为 `against your Spellpower`，对应源码 `controlled-horrors.lua:292`: `target:checkHit(self:combatSpellpower(), target:combatSpellResist(), ...)`）。译文仅写“未能通过魔法豁免”，将关键的对抗基准属性（玩家自身的法术强度）完全漏译，使玩家无法获知该技能受何种属性影响生效。
- **状态**：存在问题
- **证据与依据**：`sources/dlc/cults/tome-cults/data/talents/demented/controlled-horrors.lua:292, 303`，技能判定消费逻辑直接可证。

---



## O175 | entry-03570

### C34 | entry-03570 | 存在问题

原文要求目标的魔法豁免与施法者的“**Spellpower**”对抗；译文仅说“**未能通过魔法豁免**”，漏掉判定所对抗的法术强度。代码使用 `target:checkHit(self:combatSpellpower(), target:combatSpellResist(), …)`。证据：`controlled-horrors.lua:293–307`。



## O176 | entry-03570

### C35 | entry-03570 | 存在问题

原文“**all other creatures hostile to it**”译成“**周围其他生物与之敌对**”，平添周围范围限制。效果给目标设置 `hated_by_everybody`；半径 10 的投射用于**施加瞬间清除附近单位当前目标**，不是敌对关系的范围。证据：`controlled-horrors.lua:303–306`；`timed_effects.lua:514–521`。



## O177 | entry-03570

### C54 | entry-03570 | 存在问题
“making all other creatures hostile to it” 译为“令周围其他生物与之敌对”，增加了“周围”这个范围限制。
- **快照**：`timed_effects.lua:521` HORRIFIC_DISPLAY 施加 `hated_by_everybody`。
- **本体**：固定 commit `game/modules/tome/class/Actor.lua:1769` 的 `reactionToward` 中，`rtarget:attr("hated_by_everybody")` 会对所有其他生物返回 -100，没有距离限制。
- DLC 快照的版本适用性待确认；原文 “all other creatures” 本身就能说明译文收窄了范围。



## O178 | entry-03570

### C55 | entry-03570 | 存在问题
“If the target fails a magical save against your Spellpower” 译为“如果目标生物未能通过魔法豁免”，漏了“对抗你的法术强度”，玩家不知道由哪项属性对抗豁免。快照 `controlled-horrors.lua:293`：`checkHit(self:combatSpellpower(), target:combatSpellResist(), …)`。



## O179 | entry-03570

### C57 | entry-03570 | 存在问题

原文“a magical save **against your Spellpower**”，译文仅为“未能通过魔法豁免”，遗漏与施法者法术强度对抗的关系。玩家因此无法从描述知道影响成功率的自身属性。

证据：冻结原译文；快照 `T/controlled-horrors.lua:293` 实际调用 `checkHit(self:combatSpellpower(), target:combatSpellResist(), ...)`。这里确认的是明确文本信息的遗漏。



## O180 | entry-03570

### C58 | entry-03570 | 存在问题

原文“making **all other creatures** hostile to it”，译文“令**周围**其他生物与之敌对”，新增了空间范围限制。

快照 `E:515` 的半径 10 用于清除攻击目标；`:521` 则单独设置 `hated_by_everybody`。固定本体 `game/modules/tome/class/Actor.lua:1762` 的 `reactionToward` 在 `:1769` 消费此属性时没有距离检查。因此不能把附近目标重置的范围套到敌对关系上。译文相对原文的范围收窄可直接确认；该 DLC 快照的目标版本适用性仍未固定。



## O181 | entry-03571

### C36 | entry-03571 | 存在问题

原文限定提升“**your summoned horrors damage**”，译文只说“**增加恐魔 %d%% 伤害**”，漏掉“召唤的”这一适用对象范围。快照分别在制造两种召唤物时给该召唤物的 `inc_damage.all` 加值。证据：`controlled-horrors.lua:98–100、243–245、319–323`。



## O182 | entry-03571

### C37 | entry-03571 | 仅建议

“**At talent level 3/5**”译为“**技能等级 3/5 后**”可能让读者迟疑是否含当级；它也可按“达到该级以后”理解，因此未确认为门槛错误，只记录清晰度建议。快照门槛为 `>=3`、`<5` 的相反判断。证据：`controlled-horrors.lua:123、245、319–322`；`timed_effects.lua:499`。



## O183 | entry-03571

### C38 | entry-03571 | 存在问题

“**attune your horrors to the dead god Amakthel**”指让恐魔与死神的力量调谐；“**将你的恐魔和已死之神……同化**”表示双方被变成同一种性质，改变了动作关系。证据：`controlled-horrors.lua:319`。



## O184 | entry-03571

### C56 | entry-03571 | 存在问题
“victims of your Horrific Display spell” 译为“恐怖展示的受害者”。同一 DLC 的技能名译文在 context.lua:1679 是 `t("Horrific Display", "恐魔具现化", "talent name")`。描述里引用的技能名和界面上的技能名对不上，玩家找不到所指的技能。同条的“腐败的吞噬者”与 context.lua:1655 一致，可作对照。



## O185 | entry-03571

### C57 | entry-03571 | 仅建议
距离单位用“码”，同批 03567 用“格”；末句“伤害加成受法术强度加成”重复了“加成”。都不影响意思。

---



## O186 | entry-03571

### C59 | entry-03571 | 存在问题

原文引用技能“Horrific Display”，译文“恐怖展示”；允许的邻近语境 `context.lua:1679` 中该技能名称为“恐魔具现化”。这使增强效果没有使用实际邻近技能名称，影响玩家识别对应技能。

证据：`context.lua:1679` 及本条；`T/controlled-horrors.lua:276` 确认为同一具名技能。这是本包内的指称一致性问题，不涉及全局改名。



## O187 | entry-03572

### C60 | entry-03572 | 待确认

原译文都说至少命中一个敌人就获得疯狂值，但快照 `T/disfigured-face.lua:56` 只有在 `hit and target:canBe("disease")` 时才将 `did_hit` 设为真，`:74` 又仅依据 `did_hit` 发放疯狂值。

因此，快照内“命中但不能承受疾病”的目标不满足资源获取条件。此限制是原译文共同遗漏，不能归为翻译新增；缺目标 DLC 版本与快照一致的证据，保留待确认。

实际读取范围与版本如下。设本包根路径为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g10-20260923/`

读取了以下四个冻结文件：

- `INPUT.md`
- `entries.json`
- `context.lua`
- `source-access.json`

读取并验证了以下八个本组源码文件；全部 SHA-256 与访问清单一致：

| 相对于本包根路径的文件 | SHA-256 |
|---|---|
| `sources/dlc/cults/tome-cults/data/lore/fay-willows.lua` | `05a3f93c9f5cd5baf52429155fcd4a09b6045ef45fbf3472562d55f5da0e4c6f` |
| `sources/dlc/cults/tome-cults/data/lore/kroshkkur.lua` | `00147ee5b29fdd6dd764ff07a77f7dce1c42634dc5673cbde9341312a50927d2` |
| `sources/dlc/cults/tome-cults/data/lore/misc.lua` | `ab9cf8e70d666816d79d0c4fddec2ce573072d5644f737d450b7731cbc42a0b3` |
| `sources/dlc/cults/tome-cults/data/lore/zones.lua` | `8b8dfe318f657f397aee0c608d95f551ce868e027e5404da6d2e56670c755f76` |
| `sources/dlc/cults/tome-cults/data/talents/demented/calamity.lua` | `7a65b4d2d7a91f83f32472a330aeff48e7ac983914fd672dc09673a812a06d80` |
| `sources/dlc/cults/tome-cults/data/talents/demented/chronophage.lua` | `6b669e4e3cbec766a6b37b3b3b8998b52a6ce6127996a247cfb16bfb9034e4b5` |
| `sources/dlc/cults/tome-cults/data/talents/demented/controlled-horrors.lua` | `a123514fa090c6d4d714dfb3ff977ade6c62d079aac1e7e4a101035bc3ee1399` |
| `sources/dlc/cults/tome-cults/data/talents/demented/disfigured-face.lua` | `92e1c785090559761bc7cbc0b3542816a1c0a1f3c91b2e4cd421302a2caa6c36` |

额外源码仅两项：

- `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/timed_effects.lua`。由已读技能中的 `EFF_JINX`、`EFF_FORTUNE`、`EFF_ATROPHY`、`EFF_HORRIFIC_DISPLAY` 引入；SHA-256 为 `0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c`，匹配清单。
- `/workspace/t-engine4` 仓库中的 `game/modules/tome/class/Actor.lua`。由已读效果中的 `mod.class.Actor`、`hated_by_everybody` 和 `reactionToward` 消费关系引入；仅通过 `git show` 读取固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

所有 DLC 文件均为**哈希固定、源码仓库与 commit 未固定**的公开快照，未套用本体 commit。未决机制及缺失证据已逐项注明。

40 条的 ID、原文和译文与 `entries.json` 一致；格式占位符数量和顺序一致。未发现可证的标记或换行显示缺陷。未读取其他报告、当前翻译文件或其他语言答案；未越界、未创建临时文件、未修改仓库、未创建子 agent。本输出仅为独立审核观察，不构成生产完成或 `DONE_VERIFIED` 声明。

