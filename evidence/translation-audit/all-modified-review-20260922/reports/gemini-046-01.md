### 校验前提与环境状态

- **复核批次**：`batch-046`
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-046.md`
- **冻结 SHA-256 核验**：经 `sha256sum` 校验，哈希值为 `e2442112f4610a93eb94d0f0223a419b91b627f4f7178a80479dd8937cb7a9de`，与指令完全一致。
- **源码依据**：依据 [`evidence/translation-audit/all-modified-review-20260922/source-access.json`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/source-access.json)，本批 9 条（`entry-01308` 至 `entry-01316`）全部属于引擎核心 Tome 模块（`mod-tome/data/lore/misc.lua`），均使用固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 读取公开源码及关联调用链；译文基准对应终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。
- **操作原则**：全程只读，未修改、创建或删除任何文件，未派发子代理，不宣布最终裁决。

---

### 逐条复核报告

#### entry-01308
- **条目位置**：[`mod-tome.lua:18137`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18137)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:497`，Lore ID: `races-9`（野蛮怪物种族手札）。
- **核验结论**：**存在疑点**
- **可核验依据**：
  1. **存在疑点（词义错译）**：第 3 段中，原文为 `There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare...`，译文写为“有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击**市民**，但是这极其少见……”。`communities` 在低地地理语境下指村落、定居点或聚居社群；“市民”（citizens/townsfolk）系混淆，属于词义误译。
  2. **细微观察（语意重复冗余）**：第 2 段描述森林巨魔时，原文为 `They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons...`，译文写为“他们比岩石巨魔同胞有着**更为敏捷的速度**和更为发达的言语能力，并且**以移动迅速**和能够使用精工武器**闻名**……”。译文将 `move faster` 翻译了两次（前句的“更为敏捷的速度”与后句的“以移动迅速……闻名”），造成句内同义重复。
  3. **细微观察（漏译/淡化）**：第 2 段 `towards the end of the Age of Pyre` 仅译为“在烈火纪时”，遗漏了 `towards the end of`（走向末期/尾声）；第 3 段 `much longer, swinging limbs` 译为“更长的四肢”，漏译了 `swinging`（摆动/晃荡的）。

---

#### entry-01309
- **条目位置**：[`mod-tome.lua:18154`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18154)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:510`，Lore ID: `races-10` 标题。
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 11 - Dragons`
- **译文**：`博学者格雷诺特关于种族的调查——第十一章——龙族`
- **核验结论**：**未发现问题**
- **可核验依据**：与同章节系列前 10 章的统一标题格式（见 [`mod-tome.lua:17943-18136`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L17943-L18136)）完全保持一致；双破折号规范，专名与数字序号准确，无控制符或占位符问题。

---

#### entry-01310
- **条目位置**：[`mod-tome.lua:18155`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18155)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:511`，Lore ID: `races-10` 正文。
- **核验结论**：**存在疑点**
- **可核验依据**：
  1. **存在疑点（错别字）**：第 1 段中，“龙族是**另人难以置信**的长寿生命……”存在明显错别字，“另人”应为“令人”。
  2. **存在疑点（指代关系误读）**：第 5 段描述巨龙素材市场时，原文为 `...there is an increasing market for "naturally harvested" drake materials - those taken from dragons which have died of natural causes.`，译文译为“……并且交易“自然采集”的龙族材料的市场也日益增多——**那些人**只取自然死亡的龙族身上的材料。”。原文破折号后的代词 `those` 指代前面的核心名词 `drake materials`（巨龙材料），即“即那些取自自然死亡巨龙的材料”；译文误将 `those` 判定为代指人群（“那些人”），导致主干关系产生逻辑偏移。
  3. **细微观察（语意重心偏差）**：第 2 段 `However this theory may be borne purely from the fanatical delusions of certain wyrmics...` 译为“然而这个理论只有那些狂热的研究了龙族太久的龙战士信徒们才会相信”，原文 `borne purely from` 表示理论“纯粹源于/产生于某些龙战士的妄想”，译文转为主观接受者的“相信”，重心略有偏移。

---

#### entry-01311
- **条目位置**：[`mod-tome.lua:18207`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18207)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:551`，Lore ID: `eden-guile`；关联固定源码神器 `Eden's Guile`（`data/general/objects/world-artifacts.lua:519-520`，黄色跑鞋）。
- **核验结论**：**未发现问题**
- **可核验依据**：诗歌为 3 节、每节 4 行的歌谣；译文保持了每节 4 行与空行排版；节奏明快，完全契合盗贼流放者艾登穿鞋逃跑、保命重于荣誉的角色背景与神器描述；关键专有名词及“日与月”翻译得体，无占位符或控制字符。

---

#### entry-01312
- **条目位置**：[`mod-tome.lua:18235`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18235)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:570`，Lore ID: `channelers-set`；关联固定源码神器套装引言（`data/general/objects/world-artifacts-maj-eyal.lua:1095`）。
- **核验结论**：**存在疑点**
- **可核验依据**：
  1. **存在疑点（语法误解导致词义错译）**：第 2 节原文为 `Whilst crops fell dead in drought and blight / And children grew diseased`，译文译为“当作物死于干旱和枯萎 / **感染疾病的孩童增长**”。此处 `grew diseased` 系系表连用结构（grow + adj，表示“变得患病/染病”，与上句的作物枯死对称）；译文误将连系动词 grew 当作表示数量增长的不及物动词（“孩童增长”），属于语法误读导致的明显翻译错误（应为“孩童纷纷染病/身患重疾”）。
  2. **存在疑点（感情色彩擅自颠倒）**：第 8 节描写法师倒下时，原文为 `From loose grip flew his staff so wroth / Thus fell the mage renowned`，译文译为“法杖也因失去控制而落下 / **臭名昭著的**法师终于陨落”。`renowned` 意为“闻名遐迩的、著名的”，呼应第 1 节中法师威名（`rose an archmage high with power beyond compare`）；译文将其擅自反译为贬义词“臭名昭著”（notorious/infamous），背离了原文词义。
  3. **细微观察（核心内涵偏移）**：第 3 节 `Not seeking fame or high reward / He followed but his zeal` 译为“不求名利与荣耀 / **但求问心无愧**”。`zeal` 意为“狂热、满腔热诚”，体现的是伊格兰斯反魔追随者（Ziguranth）消灭奥术的狂热执念；译为“但求问心无愧”严重偏离了反魔狂热的背景内涵。
  4. **细微观察（核心意象漏译）**：第 10 节末句 `Now to Nature you are dust` 译为“如今你已归于尘土”，漏译了全诗反复强调的反魔核心受词 `to Nature`（对大自然而言/向自然归为尘土）。

---

#### entry-01313
- **条目位置**：[`mod-tome.lua:18334`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18334)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:624`，Lore ID: `dreamscape-entry`；关联固定源码灵能催眠系天赋 `Dreamscape`（`data/talents/psionic/slumber.lua:232`）。
- **核验结论**：**存在疑点**
- **可核验依据**：
  1. **存在疑点（多处漏译、误译并添加无源省略号）**：第 1 段末尾原文为 `A strange psychedelic haze permeates the air and otherworldly colors and shadows flicker in and out of your peripheral vision.`，译文译为“迷幻的烟雾弥漫在空气中，**各色阴影在视野中飞舞……**”。
     - `otherworldly`（超凡的/来自异界的）被漏译；
     - `peripheral vision`（外围视野/余光）漏译了 `peripheral`；
     - `flicker in and out`（闪烁隐现/忽明忽暗）被误译为“飞舞”；
     - 句末擅自添加了原文不存在的省略号“……”。
  2. **细微观察（机制呼应修饰词淡化）**：第 4 段原文 `your lucid mind races on how to handle such an insane and horrible situation` 译为“但你的大脑也开始思考……”，遗漏了 `lucid`（清醒的）。在灵能者催眠系中，核心被动天赋即为“清醒梦者”（`Lucid Dreamer`，见 `slumber.lua:244`），此处的 `lucid mind` 属于明确的设定呼应；同段中短语 `On a whim`（灵机一动/心血来潮）在译文中亦被略去。

---

#### entry-01314
- **条目位置**：[`mod-tome.lua:18345`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18345)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:636`，Lore ID: `loot-vault-empty`（宝库嘲弄字条）。
- **原文**：
  ```text
  Dear graverobber,

  Try to be a little faster next time.

  Love, #{italic}#Eden#{normal}#
  ```
- **译文**：
  ```text
  亲爱的盗墓贼，

  下次记得快一点。

  你钟爱的#{italic}#艾登#{normal}#
  ```
- **核验结论**：**细微观察**
- **可核验依据**：
  - 英文信末常用落款 `Love, [Name]` 为写信人表达主动问候/爱意（“爱你的艾登”）；译文处理为“你钟爱的艾登”（相当于被动态 Your beloved Eden），主客关系发生了颠倒。由于该字条是嘲讽盗墓贼空手而归的戏谑字条（Mocking Note），带有一丝自恋调侃风味，未造成恶性机制理解障碍，但字面表达不够严谨。
  - 样式标签 `#{italic}#...#{normal}#` 配对完整，换行格式无误。

---

#### entry-01315
- **条目位置**：[`mod-tome.lua:18375`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18375)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:669`，Lore ID: `renegade-pyromancers-vault`；关联固定源码宝库地图 `data/maps/vaults/renegade-pyromancers.lua:42`。
- **核验结论**：**存在疑点**
- **可核验依据**：
  1. **存在疑点（违和错译）**：第 3 段描述捆绑祭品时，原文为 `Bind them in place with flame secure bindings, and give a sound gag.`，译文译为“用**防火胶布**把他绑住，塞住他的嘴巴。”。在奇幻背景的邪法召唤仪式中，`bindings` 指束缚具、绑带或拘束绳索；将其译为带有现代工业消费品色彩的“防火胶布”（adhesive tape），既偏离词义又极为违和出戏（应为“耐火绑带/防火绳索”）。
  2. **细微观察（格式微调）**：第 4 段末尾原文截断处为 `brands the shape of --- `，译文写为“烙出——的形状——”，破折号由单侧截断变为了双侧包裹。
  3. **术语与排版核实**：材料清单中 `luminous horror dust` 准确采用了 preferred 规范术语“金色恐魔的粉尘”；`faeros ash` 采用了固定译名“法罗的灰烬”；材料列表每行的制表符与空格缩进（`\t  `）与原文严格保持一致；样式控制符 `#{bold}#...#{normal}#` 和 `#{italic}#...#{normal}#` 闭合完整。

---

#### entry-01316
- **条目位置**：[`mod-tome.lua:18410`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L18410)；section: `mod-tome/data/lore/misc.lua`
- **源码依据**：`game/modules/tome/data/lore/misc.lua:693`，Lore ID: `nature-vs-magic`；关联固定源码法系玩家拾取/装备反魔物品时的警示触发逻辑（`class/Player.lua:1569`）。
- **核验结论**：**细微观察**
- **可核验依据**：
  - 首句 `Your arcane abilities have been interfered with!` 中，`abilities`（技能/能力）被译为了“奥术能量”（“你的奥术能量被干扰了！”）。下文第二句中的 `arcane energies` 才是真正的“奥术能量”，反魔装备干扰的实际是法术施放能力（带来法术失败惩罚）；译为“能量”稍有概念漂移，但整体叙事与警示语境通畅，无实质误导。
  - 核心术语“埃亚尔”、“反魔”、“野性能力”使用准确，分段与标点规范，未发现硬伤。

---

### 复核总结汇总表

| 编号 | 位置 | 结论 | 核心依据摘要 |
| :--- | :--- | :--- | :--- |
| **entry-01308** | `mod-tome.lua:18137` | **存在疑点** | 错将 `communities`（聚落/社区）译为“市民”；第 2 段将 `move faster` 重复译了两次。 |
| **entry-01309** | `mod-tome.lua:18154` | **未发现问题** | 章节标题格式与全手札系列严格统一，专名与序号准确无误。 |
| **entry-01310** | `mod-tome.lua:18155` | **存在疑点** | 存在明显错别字“另人难以置信”（应为“令人”）；第 5 段代词 `those`（指代巨龙材料）被误译为“那些人”。 |
| **entry-01311** | `mod-tome.lua:18207` | **未发现问题** | 三段打油诗排版与押韵契合，对应神器 `Eden's Guile` 背景，行文生动自然。 |
| **entry-01312** | `mod-tome.lua:18235` | **存在疑点** | 语法误读将 `children grew diseased`（孩童患病）译为“孩童增长”；将 `mage renowned`（著名的法师）反向篡改为“臭名昭著的法师”。 |
| **entry-01313** | `mod-tome.lua:18334` | **存在疑点** | 第 1 段漏译 `otherworldly` 与 `peripheral`，将 `flicker in and out` 误译为“飞舞”并擅加省略号；第 4 段漏译机制呼应词 `lucid`。 |
| **entry-01314** | `mod-tome.lua:18345` | **细微观察** | 信末署名 `Love, Eden` 处理为“你钟爱的艾登”，存在主客颠倒，但在嘲弄字条语境下尚通顺。 |
| **entry-01315** | `mod-tome.lua:18375` | **存在疑点** | 将奇幻仪式中的束具 `flame secure bindings` 译为现代感极强的“防火胶布”，严重失真违和；清单缩进与术语（金色恐魔的粉尘）规范。 |
| **entry-01316** | `mod-tome.lua:18410` | **细微观察** | 首句将 `arcane abilities` 译为“奥术能量”，概念略有漂移，但整体叙事准确通顺。 |