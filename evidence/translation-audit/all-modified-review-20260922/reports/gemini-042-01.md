### batch-042 译文复核报告

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核批次**：`batch-042`（条目 `entry-01269` 至 `entry-01281`，共 13 条）
- **文件 SHA-256 核验**：
  - 预期值：`2e76acb85d75f4be1078d18e506d459e4530c6d76fc9a825af835a4f14700f6c`
  - 实测值：`2e76acb85d75f4be1078d18e506d459e4530c6d76fc9a825af835a4f14700f6c`
  - 校验结果：**哈希一致**。
- **源码与上下文依据**：
  - 固定公开源码库：`/workspace/t-engine4`（commit: `624a67329fe2ad440c5b344785a9c73fcf22ae63`，对应文件 [`game/modules/tome/data/lore/misc.lua`](file:///workspace/t-engine4/game/modules/tome/data/lore/misc.lua)、[`game/modules/tome/data/zones/deep-bellow/npcs.lua`](file:///workspace/t-engine4/game/modules/tome/data/zones/deep-bellow/npcs.lua)）
  - 译文版本终点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（[`mod-tome.lua`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua)）

---

#### entry-01269
- **位置**：`mod-tome.lua:17584`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**未发现问题**
- **依据说明**：
  - 格式标签 `#{bold}#...#{normal}#` 正确保留且对称闭合，段落换行与原文一致。
  - 精灵族群专名（Shalorën 永恒精灵、Thalorën 自然精灵、Nalorën 纳鲁精灵、Sher'Tul 夏·图尔、nagas 娜迦）符合设定与术语快照。
  - 正文叙事完整通顺，末句适度润色增补“历史将会延续”，属常规文学修辞，未扭曲剧情主旨。（存在两处“的/地/得”字词微瑕：“身体变的”应为“变得”，“自由的呼吸”应为“自由地呼吸”，属轻微观察）。

---

#### entry-01270
- **位置**：`mod-tome.lua:17594`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **核心句意与口吻反差**：原文 “nature couldn't have hoped to create such a race as nagas.” 为否定式虚拟语气，意在强调娜迦的完美超越了自然造化的极限（大自然做梦也造不出像娜迦这般完美的种族），表现娜迦领袖斯拉苏尔（Slasul）极度狂妄自负的心态。译文作“大自然怎么会创造出娜迦这样的种族？”，在中文习惯中表现为对事物怪异的反诘或疑问，未能准确传达原句中“大自然根本无法企及”的自负赞叹。
  2. **术语不一致**：原文 “Temple of Creation” 在术语快照中明确规范为“造物者神庙”（`T.NARRATIVE.LORE`），译文此处译作“造物主神庙之门为我打开”，与既定术语存在偏差。
  3. **别字瑕疵**：“我们可以变的更加强大”中“变的”为别字，应为“变得”。

---

#### entry-01271
- **位置**：`mod-tome.lua:17598`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **核心地名漏译**：原文第二段 “Truly, as I travelled the lands surrounding Derth did I come across such a monstrous, awe-inspiring, lupine adversary.” 明确给出了关键冒险地点 “the lands surrounding Derth”（德斯镇周边的土地）；译文译作“事实上，当我在周围的旅行时”，完全漏译了核心地名“德斯镇”（Derth）。
  2. **叙事递进结构打乱与脑补加料**：
     - 原文第二段采用循序渐进的修辞逻辑：先让读者想象普通的饿狼（wolf）-> 再写力量凶暴堪比整群弱小同类的座狼（warg）-> 最后递进至“庞大如熊”（one the size of a bear）。
     - 译文开篇直接将后文的“庞大如熊”前置，并凭空脑补添加了原文不存在的描写：“赤眼如炙，饥渴的吞噬着它周围一切的生命”、“这只暴君所带来的威胁”、“好家伙”等。
  3. **动宾搭配不当**：“它挥舞的獠牙比我的剑还要长”，獠牙长于口中无法“挥舞”，原文为 “With fangs of a length to match my own blade, I entered combat...”。
  4. **主观增饰扩写**：第三段原文 “but legends must live on. They are what give this world its very spirit!”，译文擅自添加了“但我的内心告诉自己这种传说中的生物必须让其繁衍下去”。

---

#### entry-01272
- **位置**：`mod-tome.lua:17618`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **地图专名偏离**：原文 “trekking through the Old Forest” 指游戏经典核心区域 Old Forest（德斯镇外著名副本）。术语快照明确规定 `old forest 古老森林 T.NARRATIVE.LORE`；译文作“远古丛林”，偏离既定专名。
  2. **生物与设定严重篡改**：
     - 原文生物为 “the giant ants' repulsive progenitor”（巨蚁令人作呕的始祖/蚁后）。译文篡改为“满地的史前巨型白蚁，它们在可怕的蚁王指挥下蜂拥而出”；不仅无端添加“史前”，且将“巨蚁”（ant）改成了“白蚁”（termite），并将负责繁衍的雌性始祖/母体 “progenitor” 改成了“蚁王”。
     - 原文 “a most hideous, bloated, oozing and chittering horror”（极其丑恶、臃肿肥硕、脓液渗流且吱吱作响的恐怖之物），译文篡改为“世上最可怕、最犀利、最凶猛的生物”，将臃肿流脓的特征改为了反差极大的“最犀利”。
     - 原文 “it was as though the ground itself was swarming forward to devour me”，译文擅自改写为“试图用那巨大的前颚将我碎尸万段”。
  3. **漏译短句**：第一段末尾 “Such bravery! Such pluck and derring-do!”，译文仅译出“这真是充满勇气！”，漏译了后半句 “Such pluck and derring-do!”（如此胆魄与英勇大冒险！）。
  4. **排版格式被破坏**：原文第二段为一个完整自然段，译文在中间强行切断换行，拆分成了两个自然段。

---

#### entry-01273
- **位置**：`mod-tome.lua:17637`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **现代词汇违和出戏**：原文 “I shall deliver this joyous news to Last Hope with all haste”，译文作“我真该用加急快递将你这英雄事迹传到最后的希望”。在剑与魔法的奇幻背景信件中出现“加急快递”具有强烈的现代违和感（原文仅为“火速送达/万急送去”）。
  2. **擅自添加推断主语**：原文第三段中作者自始至终未指明该生物名称，仅以烈焰之翼与利爪进行悬念描写（“With wings of fire... alighted on a rocky outcrop mere yards away from me”）；译文擅自添加了具体主语“巨鸟”（且“煽动”为别字，应为“扇动”）。
  3. **粗俗语加料**：原文 “Forget dragons and demons”，译文作“去他妈的巨龙与恶魔”，添加了原文完全没有的脏话粗口。
  4. **格式切分**：原文第 2 段与第 3 段在译文中均被中途各切断拆分成两个自然段，破坏了原信件格式。

---

#### entry-01274
- **位置**：`mod-tome.lua:17661`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**未发现问题**
- **依据说明**：
  - 称谓、正文、署名格式完整一致，段落与原文严密对应。
  - “badinage”（插科打诨）、“birdwatching session”（观鸟之行，呼应前信）对仗精准，德斯镇（Derth）及北面遗迹传闻的叙述准确传神。

---

#### entry-01275
- **位置**：`mod-tome.lua:17677`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **核心梗意误译反转**：
     - 原文结尾罗尔夫对威斯曼的嘱托：“Make sure you write the words on your next letter nice and big,”
     - 结合正文剧情：威斯曼在此次遭遇战中被打瞎了一只眼睛（“It may have taken your eye”），视力严重受损，因此罗尔夫特意嘱咐他下次写信时把字写得“大大的”（口语中 “nice and big” 是加强语气的“足够大/大大的”）。
     - 译文误译为：“希望你下封信上的字又大又美，”；望文生义将 “nice and” 拆译为“又大又美”，彻底扭曲了历劫生还的两位好友间针对伤残特征的调侃与关怀。
  2. **代词与动作偏差**：原文 “The tentacles... They have lashed into my mind as they lashed into my flesh.” 描写触手如皮鞭般抽打抽挞入血肉与心灵；译文使用代词“他们”（触手应为“它们”），并将 “lashed” 译为“插入”，改变了动作形态。
  3. **排版格式被破坏**：原文第 2 段为一个完整的内心独白段落，译文被强行切分成了三个独立自然段。

---

#### entry-01276
- **位置**：`mod-tome.lua:17701`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**未发现问题**
- **依据说明**：
  - 称呼、正文、落款段落结构完全对应。
  - 面对不可战胜之强敌时的恐惧与逃避心理、内心的挣扎以及重返战斗的决心，译文表达准确贴切，人名（Rolf 罗尔夫、Weisman 威斯曼）一致。

---

#### entry-01277
- **位置**：`mod-tome.lua:17714`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**细微观察**
- **依据说明**：
  - 原文首句：“By my ancestors' profits I hope you receive this message in good health and spirits.” 
  - 矮人罗尔夫独特的誓言 “By my ancestors' profits”（以我祖先的利润起誓 / 凭我祖先的收益作保），体现了矮人族重财富收益的文化特征及谐音双关幽默（profits vs prophets）。
  - 译文弱化意译为通用的“祖先保佑”，抹平了矮人种族专属的语言特色。主干剧情与劝阻语义无重大偏离。

---

#### entry-01278
- **位置**：`mod-tome.lua:17728`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **背景机制与口吻遭抒情脑补篡改**：
     - 原文结尾旁注：`#{italic}#(the ink blotch seems to indicate Weisman had caught up to his old friend, one-half of that abomination)#{normal}#`
     - 对照公开源码 `game/modules/tome/data/zones/deep-bellow/npcs.lua` 中备份守护者 `ABOMINATION`（憎恶）的设定：其描述为具有双头（“Two heads glare malevolently at you”），并掉落此信件（`ADV_LTR_8`）。设定上罗尔夫与威斯曼最终被腐化融合成为了同一个恐魔怪物“憎恶”的两个组成部分，因此原文客观记录 “one-half of that abomination”（作为那憎恶怪物的另一半）。
     - 译文将该客观同位语成分改写为抒情句：“他们以这种怪物的形式永远地团聚在了一起”，带有明显的过度主观脑补与煽情色彩。
  2. **程度词翻译过重**：原文 “Weisman was already half-gone”（威斯曼当时神智已迷失了一半），译文译作“威斯曼已经神智尽失”，程度偏重。

---

#### entry-01279
- **位置**：`mod-tome.lua:17736`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**未发现问题**
- **依据说明**：
  - 标题条目 “memories of Artelia Firstborn”。
  - 译文纠正了旧版本将 “Firstborn” 误译为“长子”的硬伤，准确译为“首生者”；专名音译“亚特莱”与仓库内同一实体的标题（如第 11460 行 `entity name`）保持了一致。

---

#### entry-01280
- **位置**：`mod-tome.lua:17737`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**存在疑点**
- **依据说明**：
  1. **时间感知词义严重翻反（硬伤）**：
     - 原文第 3 段：“I watched her for what felt like a century, and she watched me...” 描写初生的主角凝视造物女神，“感觉仿佛过了一个世纪般漫长”。
     - 译文翻译为：“看到她的一瞬几乎让我的时间停滞……”；将极漫长的时间心理尺度（a century，一个世纪）颠倒反转成了极短的“一瞬”，存在确凿的词义翻反硬伤。
  2. **核心问答逻辑断层**：
     - 原文第 4 段：主角醒来后四顾无人，因而在担忧孤独中发问：“Am I alone?”（我只是孤身一人吗？），女神回答 “There are no others like you.”，主角因而感到伤感孤寂（“At this I felt sad, and she could see the loneliness in my heart.”）。
     - 译文将 “Am I alone?” 翻译为：“我是独一无二的吗？”。若问句是“我是独一无二的吗”，得到肯定答复本为赞美，后文却突然转入悲伤孤寂，导致前后因果逻辑产生裂痕。
  3. **乱码规避与文字微瑕**：
     - 原文第 5 段源码中因编码残留问号出现 `Alor?.`，译文规范音译为“阿洛”，处理恰当。
     - 存在文字微瑕：“大声的歌唱着欢乐”与“不停的寻找”中，“的”均应为“地”。

---

#### entry-01281
- **位置**：`mod-tome.lua:17763`
- **Section**：`mod-tome/data/lore/misc.lua`
- **审查结果**：**未发现问题**
- **依据说明**：
  - 创世神话的 14 行文本逐行对应，格式排版与原文完全吻合。
  - 创世神专名 Gerlyk（盖里克）、神话元素及种族名称（Human 人类、Halfling 半身人、Dwarf 矮人、Elf 精灵、Eyal 埃亚尔、Darkness 黑暗）均与术语快照严格统一。
  - 个别行有适度添加转折关联词（“虽然……但……”）和修辞扩展（“散发出无穷的热量”），但完全符合上古创世神话叙事风格，未见事实偏离。