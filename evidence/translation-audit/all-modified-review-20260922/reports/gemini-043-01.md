### batch-043 译文复核报告

#### 基础信息核验
- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-043.md`
- **文件 SHA-256 校验**：`bc94c9d782a20242e5c0cdfe9665532b25f6372fde247c945f8ce7e33d0c8e13`（经核对一致）
- **条目范围**：`entry-01282` 至 `entry-01291`，共 10 条
- **源码参考基准**：公开源码 `engine/mod-tome` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（对应文件：`game/modules/tome/data/lore/misc.lua`）
- **译文比对基准**：固定 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

### 逐条复核结果

#### 【entry-01282】
- **位置**：`mod-tome.lua:17791`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `creation-halfling`，半身人创世哲学）
- **复核结论**：**存在疑点** / **细微观察**
- **可核验依据**：
  1. **严重词义反转错译（存在疑点）**：第 7 段原文 `No, clearly other gods were responsible, lesser gods than our own which copied his grand design.`，结合前文矮人与人类是“扭曲畸形生物”的论述，此句意为“不，显然是其他神明造的孽（其他神明负有责任），是比我们的神更次等的神抄袭了他的宏伟构想”。译文误将表示因果归咎的谓语短语 `were responsible`（责任在……/是……所为）理解为形容词品性，译作“不，很显然其他创造者也很负责，但比起我们的创造者来差了一些”，将贬低次等神明粗制滥造的语境完全错译成了夸赞对方“工作认真负责”，与前后文逻辑彻底脱节相悖。
  2. **世界观概念突兀（细微观察）**：同在第 7 段，原文 `It is impossible that they were made by the same god` 被译为“因为他们不可能由同一个上帝所创造”。ToME4 世界观中为多神/原始造物主设定，且文本上下文均统称“神/神明/造物者”，此处使用带有现实宗教专有色彩的“上帝”略显违和。
  3. **说话者种族同位语漏译（细微观察）**：第 1 段末句 `Indeed, it is only through our battles with the others that we halflings have any ancient records at all.` 中，`we halflings`（我们半身人）被漏译为简单的“我们”。在整篇文本的起始段落中，原文借此表明叙述者是半身人，译文遗失了明确的种族自称。

---

#### 【entry-01283】
- **位置**：`mod-tome.lua:17826`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `moons-human`，“双月传说”）
- **复核结论**：**细微观察**
- **可核验依据**：
  1. **意象与修辞信息微损**：第 4 节中 `When both sisters are slimly seen on each side of Eyal` 描摹的是双月在天空中呈现为细弯残月/新月的天文月相（纤细隐现），译文“两姐妹只能在埃亚尔两端”遗漏了 `slimly seen` 的修辞细节。
  2. **古雅动词与句式理解偏差**：末尾两行 `Let no man walk abroad this night` 与 `Aye, and Gerlyk did walk abroad that night` 中，`walk abroad` 在古英语诗歌体裁中表示“在户外走动、在室外游荡出行”。盖里克告诫世人“今夜任何人不得在室外走动”，而他自己当夜却亲自外出走向了彼端的无尽黑暗。译文将其译为“走入今晚的黑夜 / 走入了这样的黑夜”，虽然在诗歌叙事上勉强通顺，但稍偏离了词汇本义；叹词 `Aye, and...`（是啊，然而……）在两句中也均被略去。
  3. **专名后缀增译**：第 3 节中两处 `moonsister` 被增译为“月亮女神亚缇娅”和“月亮女神菲莉娅”（原文通篇称呼为 moonsister，前文译作“月亮姐妹”）。

---

#### 【entry-01284】
- **位置**：`mod-tome.lua:17883`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `ancient-elven-ruins-note-1`）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 译文完整忠实地还原了古代精灵领袖在面对死亡逼近时的傲慢与挣扎。
  - 核心术语与专名匹配准确（`firstborn` -> 首生者、`Shaloren` -> 永恒精灵）。
  - 标点符号、省略号、破折号及末尾空行格式与源码完全一致。

---

#### 【entry-01285】
- **位置**：`mod-tome.lua:17885`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `ancient-elven-ruins-note-2`）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 对遗体防腐、化学药剂处理以及古代通灵实验过程的描写表达精准、文笔生动（如 `animate them, make them shuffle about...` 译作“驱动他们，让他们在我陵寝空荡的厅堂间蹒跚游荡”）。
  - 段落结构、换行与问号、省略号完全对应，未见漏译或误译。

---

#### 【entry-01286】
- **位置**：`mod-tome.lua:17921`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `valley-moon-3`，“月之谷日志·第三部分”）
- **复核结论**：**存在疑点** / **细微观察**
- **可核验依据**：
  1. **严重过度脑补增译（存在疑点）**：第 1 段英文原文仅有两句话 `I fell asleep in a dark hollow, but my sleep was troubled by terrible dreams. The dreams are so vivid in my mind!`。译文第二句凭空添加了长句“即使刚睡醒的脑袋仍然一团浆糊”，属脱离原文证据的无中生有。
  2. **方向介词误译与代词指代偏差（存在疑点）**：
     - 第 2 段 `beyond the red star, far beyond was a dim world`（越过红星、远在红星的彼方是一片暗淡的世界），译文误将 `beyond` 译成了垂直空间方位的“在红色星星的上方遥远的地方”。
     - 第 2 段末句 `keep it held together` 中的代词 `it` 指代被撕裂的世界（即下文乌鲁洛克双手托举支撑的恶魔母星），译文误译为复数“试图将他们固定在一起”。
  3. **专名单复数与时态偏误（细微观察）**：
     - 末段 `the lovely moonstone` 特指月亮之谷中央的那块月之石（参考同系列 `valley-moon-1` 中研究的 moonstone），译文误译为复数“月亮石们”。
     - 末段 `A strange nightmare that I shall wake up from`（一场我终将醒来的怪异噩梦），译文时态误译为“我早该从这个怪梦里醒来了”，并擅自增添了“该死的戒指”等语气修饰。
     - 第 2 段 `lava spilled up`（熔岩喷涌而出）被发散意译为“岩浆的波浪浮浮沉沉”。

---

#### 【entry-01287】
- **位置**：`mod-tome.lua:17943`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `races-0` 标题）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 原文：`Loremaster Greynot's Analysis of the Races - Introduction`
  - 译文：`博学者格雷诺特关于种族的调查——引言`
  - 专有名词 `Loremaster`（博学者）、`Greynot`（格雷诺特）符合规范，中英文破折号转换无误。

---

#### 【entry-01288】
- **位置**：`mod-tome.lua:17944`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `races-0` 正文与目录）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 正文中学者身份（`Higher human` -> 高等人类）、供职背景（`King Tolak the Fair` -> 公正之王托拉克）及中立立场叙述准确。
  - 目录列表 1 至 11 章种族名称（人类、半身人、矮人、永恒精灵、自然精灵、纳鲁精灵、食人魔、兽人、夏·图尔人、怪物种族、龙族）与仓库统一术语库严格保持一致，灭绝标记 `(extinct)` 对应无误，末尾换行格式完全一致。

---

#### 【entry-01289】
- **位置**：`mod-tome.lua:17977`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `races-1` 标题）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 原文：`Loremaster Greynot's Analysis of the Races - Chapter 1 - Humans`
  - 译文：`博学者格雷诺特关于种族的调查——第一章——人类`
  - 章节序号与标题层级命名和前文 `entry-01287` 风格严格统一。

---

#### 【entry-01290】
- **位置**：`mod-tome.lua:17978`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `races-1` 正文）
- **复核结论**：**存在疑点** / **细微观察**
- **可核验依据**：
  1. **重大历史事件混淆错译（存在疑点）**：第 3 段原文在介绍肖尔塔人时写道 `since the Cataclysm tore much of their land into the sea`，译文错译为“自从大爆炸将他们大部分土地沉入海洋后”。在 ToME4 官方设定中，“大爆炸”特指法师引发的魔法大灾难 `Spellblaze`（魔法大爆炸），而 `The Cataclysm`（大灾变）是数百年后导致地壳剧变、肖尔塔故土与纳鲁精灵故土沉入大海的大板块撕裂事件（同文件 line 18075 纳鲁精灵篇及加载提示 line 43150/43151 中 `Cataclysm` 均严格定名为“大灾变”并与“魔法大爆炸”并列）。此处将 `Cataclysm` 译为“大爆炸”属于重大世界观历史事件的张冠李戴。
  2. **职业猎称习惯（细微观察）**：第 4 段中 `spellhunters`（猎杀施法者的魔法猎手）被译为“猎魔者”，容易与字面恶魔（demon）猎杀者产生混淆，在反魔与魔法狩猎（`Spellhunt`）语境下通常作“猎法者”或“魔法猎人”。其余专名（科纳克、最后的希望、黄昏纪、厄流纪、烈火纪、勇者图库纳国王、公正之王托拉克）均与术语一致。

---

#### 【entry-01291】
- **位置**：`mod-tome.lua:17999`
- **Section**：`mod-tome/data/lore/misc.lua`（Lore ID: `races-2` 标题）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - 原文：`Loremaster Greynot's Analysis of the Races - Chapter 2 - Halflings`
  - 译文：`博学者格雷诺特关于种族的调查——第二章——半身人`
  - 标题结构、中英文符号与整体系列章节严格对齐，准确无误。