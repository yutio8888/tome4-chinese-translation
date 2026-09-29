本批次（batch-047）文件校验与源码核验准备已完成：
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-047.md` 的 SHA-256 为 `afaec4a6ab67d1c4b908505470cc7fa63003ae6f83d146a0312956bb03a09999`，校验一致。
- **源码依据**：公开源码基于 `source-access.json` 规定的固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/lore/misc.lua`、`old-forest.lua`、`orc-prides.lua`）及实体数据定义；译文基准对应提交 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### entry-01317
- **位置**：[`mod-tome.lua:18417`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18417)
- **section**：`mod-tome/data/lore/misc.lua`
- **结论**：存在疑点
- **可核验依据**：
  1. **过度意译与严重扩写（加料）**：第 4 段原文为单纯并列的名词短语列举：`think of derelict, crumbling crypts, cults and demons, hungry forests full of monsters and forces beyond time and place.`（意为“想象一下破败崩塌的地宫、邪教与恶魔、充满怪物的饥饿森林，以及超越时空的力量”）。译文大幅虚构并加入了大量原文完全没有的具体动作与描写：“废弃的远古地宫里巨岩崩碎跌落；疯狂的邪教徒将恶魔从异次元唤来；随着远处猛兽的咆哮，外表平和的森林展露了它嗜血的本性；还有，与之伴随的，超越时空约束的强大力量。”，存在严重的过度脑补。
  2. **群体指代无端添加**：第 3 段原文 `Nowadays most don't really recognize...` 中的 `most` 为“大多数人”，译文译为“现在，许多年轻人根本无法理解”，凭空限制并添加了“年轻人”这一人群标签。
  3. **介词短语曲解**：第 4 段原文 `it is before all danger and a constant threat of death` 中的 `before all` 为固定短语，意为“首要的是/首先是（危险与死亡威胁）”，译文误译为“那是前所未有的危险”。
  4. **人称与指代混乱**：
     - 第 1 段末句 `blinded too many with promise of easy fame and riches, with no eye for the other kind of fortune` 原指流浪英雄的神话蒙蔽了“太多人（too many）”，译文突兀转为第二人称并添加内容：“蒙蔽了你的双眼，让你们忽视了真正的财富就在我们的身边”。
     - 第 5 段末句 `Clad in half the age of important events which he probably has no idea about`（身披半个时代的重要事件见证物，而他自己对此很可能一无所知），译文译作“其中至少有一半连他的主人都没有丝毫了解”，将代词 `he`（指代英雄本人）错译为“他的主人”，导致语义逻辑错乱。

---

### entry-01318
- **位置**：[`mod-tome.lua:18444`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18444)
- **section**：`mod-tome/data/lore/misc.lua`
- **结论**：存在疑点
- **可核验依据**：
  1. **习语望文生义（严重误译）**：第 3 段原文 `there are a few decades in the Age of Dusk we and a few other squads recognize as "fair game" - whatever experiments you've wondered about or horrors you want to inflict...`。“fair game”为英语常用习语，意指“可以任意猎捕/随意处置的对象，法外之地/可自由折腾的区域”（语境为时空守卫可以在黄昏纪被遗忘的年代任意施展恐怖实验而不用担心破坏大局）。译文望文生义直译为“被我和其他几个小队当做了‘公平竞赛’的区域”，将法外放任误译为体育精神式的公平竞争，与上下文语境完全相悖。
  2. **时间概念与频度副词误译**：
     - 原文 `a few decades`（几十年）被译为“一些时代”。
     - 原文 `(and you do have to do the work once in a while, or you'll only be capable of seeing yourself procrastinating)` 中的 `once in a while` 意为“偶尔/时不时”，说明守卫偶尔还是得亲自办案，否则未来视只会看见自己在摸鱼。译文误译为“而且总有一天你要亲自做这件事”，将“时不时”误译为“总有一天”。
  3. **理解偏差与生硬翻译腔**：
     - 第 6 段原文 `to what is, quite literally, the best roast-yeti restaurant that could possibly exist`（毫不夸张地说/实实在在地是可能存在的最棒烤雪人餐厅），译文译为“只有我们可以毫不客气地说”，语义偏移。
     - 结尾 `Thank me later.` 直译为“一会儿谢。”，略显生硬（通常为“回头再谢我吧”）。
  4. **单复数前后矛盾**：附言（PS）开头原文为单数 `a... benefactor of sorts`（指代单人/机制实体），译文译为“遇到一些……某种意义上的恩人”，但在下一句又接“它正笨拙地把它的傀儡……”，前后数词与代词指代不合。
  5. **语病**：第 1 段“被限制在于魔法大爆炸后的埃亚尔”存在“被限制在”与“在于”杂糅的语法语病。

---

### entry-01319
- **位置**：[`mod-tome.lua:18474`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18474)
- **section**：`mod-tome/data/lore/misc.lua`
- **结论**：细微观察
- **可核验依据**：
  1. **排版格式**：末行原文粗体标签包含句点 `[b]ours.[/b] `，译文中句号被移到了标签外部 `[b]属于我们[/b]。 `（尾随空格保留）。前 13 行诗句原文含分号、逗号与句点，译文统一未加行末标点，属于现代中文诗歌排版风格化处理。
  2. **语气微调**：第 2 行 `the traps of this tomb won't claim me today.` 原文为充满决意的将来否定语气（“今天也休想收走我的性命”），译文“今天仍未能索我的命”略微偏向对已发生事实的回顾性陈述（“未能”）。核心专名 `Spydrë` 译为“斯派德”，与同 section 上下文及装备译名一致。

---

### entry-01320
- **位置**：[`mod-tome.lua:18509`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18509)
- **section**：`mod-tome/data/lore/misc.lua`
- **结论**：存在疑点
- **可核验依据**：
  1. **核心情节与包袱曲解（严重误译）**：
     - 末句原文：`Oh, look. He is trying to harm me with spells, but all he can manage is a corruption of his own name: Z'quikzshl.`
     - 结合源码上下文，学徒 Zilquick（兹基克）盗用法师配方举行巫妖仪式，却因误用长了霉菌的龙骨导致法术变异，最终退化为固定稀有怪物 `Z'quikzshl the skeletal mold`（骨化霉菌兹基克茨，见 [`game/modules/tome/data/general/npcs/molds.lua:28`](file:///workspace/t-engine4/game/modules/tome/data/general/npcs/molds.lua#L28)）。此处情节为：变成霉菌的学徒试图用法术攻击法师，但他无法施法，嘴里唯一能费力发出的动静不过是他自己名字变形走样后的声音“兹基克茨（Z'quikzshl）”。
     - 原文中 `manage` 为“勉强发出/做到”，`corruption` 为语言学上的“词形/语音走样变体”。译文误将 corruption 理解为道德/状态上的“堕落”，将 manage 理解为“拥有”，错译为：“不过他所能做的只是拥有一个堕落的名字：兹基克茨”，彻底曲解了原文的剧情逻辑与黑色幽默。
  2. **同一句内代词冲突**：“哦，看呐，它正在试图用法术攻击我，不过他所能做的只是……”，前半分句代词用物称“它”，后半分句突变为人称“他”。
  3. **词义理解偏差导致逻辑矛盾**：第 1 段中 `The other ingredients were trivial and in possession of my master...`（意为“其他材料都很寻常，而且我师傅那儿就有现成的”）。译文将 trivial 理解为质量低劣，译为“其他材料都太次，并且完全被主人所掌控……”，既不合词义，又与后文法师提到学徒偷光了昂贵的艾德瑞尔宝石的剧情相矛盾。

---

### entry-01321
- **位置**：[`mod-tome.lua:18529`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18529)
- **section**：`mod-tome/data/lore/misc.lua`
- **结论**：细微观察
- **可核验依据**：
  1. **专名与逻辑语病**：
     - 第 1 节诗句交代了背景是一个村庄：`There once was a village / the Nalore held dear`。
     - 第 3 节：`So remember old Shellsea / as she was in the past, / for Ol' Walrog sent the gale / that drowned her at last.`。“Shellsea”（谢尔希/贝壳海村）为该被淹村庄的名字，因此后文用拟人代词 `she / her` 指代村庄被暴风淹入水中。
     - 译文将村名直译为“贝壳之海”，导致出现“因为乌尔罗格放出的飓风 / 终究将她（海）淹没”这一“风暴把大海淹没”的逻辑矛盾。
  2. **标点体例**：第 1、2 节各行完全不加标点，第 3 节首行与末行则出现逗号与句号（“所以，请记住贝壳之海……终究将她淹没。”），标点体例前后不一致。

---

### entry-01322
- **位置**：[`mod-tome.lua:18619`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18619)
- **section**：`mod-tome/data/lore/old-forest.lua`
- **结论**：未发现问题
- **可核验依据**：
  - 格式标记 `#{italic}#`、`#{bold}#`、`#{normal}#` 完整对称，段落换行与原文一致。
  - 核心术语与设定对齐精准：`Sher'Tul`（夏·图尔）、`Old Forest`（古老森林）、`Derth`（德斯）、`alchemists`（炼金术师）均符合术语规范。
  - 原文探险笔记的反讽语气（“只看这毫无新意的名字，你就能猜到德斯人有多么重视这里……”）传达准确自然，树木行走萌生心智与万物灵性（animism）的表述忠实流畅。

---

### entry-01323
- **位置**：[`mod-tome.lua:18655`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18655)
- **section**：`mod-tome/data/lore/old-forest.lua`
- **结论**：未发现问题
- **可核验依据**：
  - 格式标记层级完整对称，笔记残片与最后拾取发光小球（tiny, faintly glowing orb，对应诺尔湖底夏·图尔堡垒钥匙道具）的排版严格对应。
  - 临死残卷断句与破碎语流翻译得当：`Horrors` 准确译为实体类型“恐魔”，`worms, alive, walking tog ...` 精准对应怪物“Worm that Walks”（行走蠕虫）且中译“虫子，活着，成群行……”恰当再现了词尾残缺状态。
  - 语义与古老森林/诺尔湖剧情高度吻合，无错漏。

---

### entry-01324
- **位置**：[`mod-tome.lua:18757`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18757)
- **section**：`mod-tome/data/lore/orc-prides.lua`
- **结论**：未发现问题
- **可核验依据**：
  - 核心历史术语 `Age of Pyre` 严格按 1.8beta 统一标准译为“烈火纪”（符合术语快照）；
  - `farportal` 准确译为“远行传送门”，`Prides` 结合战役设定准确译为“各个兽人部落”；
  - 动词生动翻译：“puny elves and humans that were hoveling there already”准确译为“早已缩在简陋棚屋里的弱小精灵和人类”，表意极其贴切传神；
  - 全文逻辑通畅，情绪色彩饱满，无漏译、错译与排版瑕疵。