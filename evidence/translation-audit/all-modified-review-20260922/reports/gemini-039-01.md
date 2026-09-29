### batch-039 译文复核报告

- **复核批次**：batch-039
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-039.md`
  - 校验哈希（SHA-256）：`333facfeaecef4b2ed50db758a8c2df69433fad36ab939cfc73df79af725b173`（核对一致）
- **核验源码基准**：固定公开源码 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取），译文终点版本 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。
- **条目范围**：entry-01226 至 entry-01229，共 4 条。

---

### entry-01226
- **位置**：`mod-tome.lua:15571`
- **Section**：`mod-tome/data/lore/fearscape.lua`
- **源码参考**：`game/modules/tome/data/lore/fearscape.lua`（lore id: `kryl-feijan-altar`）及 `game/modules/tome/data/zones/crypt-kryl-feijan/zone.lua:75`
- **复核结论**：**未发现问题**
- **可核验依据**：
  - **标签与排版**：原文无特殊颜色/样式标签与格式化占位符；段落为两个正文段落，译文严格保留了一致的换行与空行结构。
  - **标点与格式**：原文对话单引号 `'Intruder! Protect the seed of Kryl-Feijan!'` 规范转换为全角双引号中文对话格式 `：“入侵者！保护克里尔·费扬之种！”`。
  - **术语与语境**：专名 `Kryl-Feijan` 译为“克里尔·费扬”，与全游戏及梅琳达（Melinda）解救任务剧情、成就、NPC 名称完全统一；`female human` 译为“人类女子”，`naked flesh` 与 `twisted sigils scored into` 分别准确传达为“赤身裸体”与“扭曲的符印深深刻入她的肌肤”，与地宫祭坛仪式的实际游戏叙事完全吻合。

---

### entry-01227
- **位置**：`mod-tome.lua:15732`
- **Section**：`mod-tome/data/lore/fun.lua`
- **源码参考**：`game/modules/tome/data/lore/fun.lua:126`（lore id: `how-to-be-a-necromancer-3`）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - **标签与排版**：小节标题样式 `#{italic}#3. Unwanted Attention#{normal}#` 精确对应 `#{italic}#3. 不受欢迎的关注#{normal}#`，开闭标签完整；正文共 3 个自然段，段落划分与空行完全对齐。
  - **标点与修辞**：原文的多处强调引号（`"virtuous"`、`"ripples"`、`"conductors"`、`"corrupted"`、`"true ambitions"`）均完整保留并正确映射为中文全角引号（`“高尚”`、`“涟漪”`、`“导体”`、`“腐化”`、`“真正的野心”`）。
  - **术语与语境**：
    - 源码中带有问号的流派名 `The Tren? method`（由源码 `fun.lua:113, 126, 145` 原文固有）译作“崔恩流派”，与同文件第 2 章、第 4 章译法呼应；
    - `Beinagrind method` 统一译作“贝纳格雷德流派”；
    - 叙事语境下的 `archmage cousins` 译为“大法师同道”，符合剧情文本既有惯例；
    - 全文语义通顺，精准传达了死灵法师讽刺傲慢的口吻，无漏译或错译。

---

### entry-01228
- **位置**：`mod-tome.lua:15875`
- **Section**：`mod-tome/data/lore/fun.lua`
- **源码参考**：`game/modules/tome/data/lore/fun.lua`（lore id: `undead-hunter-guide`）
- **复核结论**：**存在疑点**（含实质疑点与细微观察）
- **可核验依据**：
  1. **第 4 节（吸血鬼）末句凭空增译与动作虚构（存在疑点）**：
     - **原文**：`So, in turn, treat them as you would a necromancer - with cold steel.`
     - **译文**：`所以，请你也像对付死灵法师一样对付他们——用钢剑刺穿他们的喉咙。`
     - **分析**：`with cold steel` 是经典英文习语，意为“以冰冷的兵刃相见 / 用冰冷的刀剑回击”。译文凭空添加了“刺穿他们的喉咙”这一具体攻击动作，属于无中生有的严重增译。此外，前半句 `It is for this reason that vampires often end up becoming rulers of lesser undead themselves, commanding them as a normal necromancer would.` 中，`It is for this reason`（正因如此）被意译成了“借助团体的力量”，且将 `commanding them` 译成了“操作指挥着自己的奴隶”，多出了原文没有的“奴隶”。
  2. **第 6 节（骸骨巨人）第 2 段主观臆造与偏离原文（存在疑点）**：
     - **原文**：`Wilful and fey as they are, normal mages often only craft golems for utility and their own protection, while necromancers create bone giants for the sole purpose of dealing death...`
     - **译文**：`尽管这些法师老头们偏执又古怪，但通常法师们制造傀儡的目的只是用来当苦力或自卫。`
     - **分析**：原文主语仅为 `normal mages`（通常法师），译文擅自加入“老头们”（old men）；
     - **原文**：`Ever fought a snow giant? Imagine one with six arms and fingers like blades, wrought of sharpened ribs. Imagine one with countless skulls lining every inch of its wretched body, all screaming for your blood to be spilt as it thrashes spinal columns like whips from its disfigured hands! After facing one of these grotesque amalgamations...`
     - **译文**：`你有没有与一向被视为力量象征的雪巨人战斗过？那就想象一下长着六只胳膊的骸骨巨人吧——手指由削尖的肋骨制成，如刀刃般锋利；再想象无数头颅悬挂在这具骸骨巨人每一寸肢体上，它们都尖叫着怒吼着，因为你的每滴鲜血都令其饥渴无比。它用畸形的双手挥舞脊柱作鞭！你若有幸见识了这扭曲的混合体……`
     - **分析**：① 原文 `Ever fought a snow giant?` 无“一向被视为力量象征的”；② 原文 `all screaming for your blood to be spilt`（尖叫着要让你的鲜血流淌）被大幅改写为“因为你的每滴鲜血都令其饥渴无比”；③ 原文 `After facing one of these grotesque amalgamations`（在直面这样一具丑恶聚合体之后）被加入了主观反讽修饰“你若有幸见识了”。
  3. **第 2 节（骷髅）保留了旧版粗鄙化与过度口语化（存在疑点）**：
     - **原文**：`What guide to the undead would be complete without mentioning the humble skeleton? Despite these clattering and chittering bones of the deceased often looking so fragile that a stiff breeze could break them apart...`
     - **译文**：`要是不死族狩猎指南里都没有最常见的骷髅那还算个屁指南？虽然这些亡灵身上的白骨在走路时上下乱颤，搞得一副弱柳扶风的样子……`
     - **分析**：原文是普通的设问与客观描写（“若不提及卑微的骷髅，又有哪本不死猎人指南称得上完整？尽管这些死者咔哒作响的骨骼看起来脆弱得强风一吹即散……”），译文残留了早期汉化带有强烈个人情绪的粗话“那还算个屁指南”，并将骨头脆弱易碎过度发挥为“在走路时上下乱颤，搞得一副弱柳扶风的样子”。此外，第 3 段中 `effort`（死灵法师维持复苏所花的心力/精力）被窄化翻译为具体的游戏资源“法力”（“驱动它们所要消耗的法力就越大……附着于其身上的微弱法力”）。
  4. **第 7 节（巫妖）代词男性化与原意曲解（细微观察）**：
     - **原文**：`Whatever you know liches as, I can tell you that they do not match the countless myths and legends that surround their terrible figures. They surpass them.`
     - **译文**：`他的身体由憎恨组成，他是纯粹的邪恶、死亡的化身……我能明确的告诉你巫妖并不是你想象中的那样，关于它的无数传奇和神话也的确有所失实。他的恐怖远超于此。`
     - **分析**：原文统用中性/复数 `they / their / them`，译文通篇强行赋予单数男性代词“他 / 他的”；原文 `do not match... They surpass them` 意思是神话传说的描绘根本比不上现实中巫妖的可怖（巫妖超越了传说），而译文作“神话也的确有所失实”，语意重心发生偏移。另外 `abyssal power` 意译为“地狱力量”（在 ToME 机制与语境中 abyssal 多对应“深渊”）。
  5. **第 3 节（尸妖）主观情感添加（细微观察）**：
     - **原文**：`Regardless of this and their ghostly appearance however, it has been recorded that steel and strength of arms is yet enough to destroy them...`
     - **译文**：`万幸的是，尸妖虽然看上去很像鬼魂，已经被证实它们还是能被武器和腕力所消灭……`
     - **分析**：原文为转折让步连词 `Regardless of this... however`（尽管如此 / 即便它们有着幽灵般的外貌），译文主观添加了“万幸的是”。
  6. **段落切分与标点格式（细微观察）**：
     - 原文在第 3 节第 2 段、第 4 节第 1 及第 2 段、第 5 节第 1 及第 2 段、第 7 节第 1 段中原本均为单一大段，译文在多处中间自行插入了换行空行拆成了 2~3 个短段落（例如第 7 节将“他的恐怖远超于此。”单独成段）；
     - 各节小节标题编号英文为数字后加点（`1. Ghouls`），译文采用了顿号（`1、食尸鬼`）。

---

### entry-01229
- **位置**：`mod-tome.lua:16042`
- **Section**：`mod-tome/data/lore/high-peak.lua`
- **源码参考**：`game/modules/tome/data/lore/high-peak.lua:35`（lore id: `argoniel-1`）
- **复核结论**：**未发现问题**
- **可核验依据**：
  - **标签与颜色码**：
    - 原文包含 8 处行内样式/颜色标记，译文全部严格一一闭合且无遗漏错位：
      - `#{italic}#...#{normal}#`（首段与两处强调词 `two` / `her`）；
      - `#FIREBRICK#Pain#LAST#` $\rightarrow$ `#FIREBRICK#痛#LAST#`；
      - `#FIREBRICK#yes they're broken#LAST#` $\rightarrow$ `#FIREBRICK#果然断了#LAST#`；
      - `#{italic}#two#{normal}#` $\rightarrow$ `#{italic}#两伙#{normal}#`；
      - `#{italic}#her#{normal}#` $\rightarrow$ `#{italic}#她#{normal}#`；
      - `#FIREBRICK#hitting#LAST#` $\rightarrow$ `#FIREBRICK#撞上#LAST#`；
      - `#FIREBRICK#agony#LAST#` $\rightarrow$ `#FIREBRICK#剧痛#LAST#`；
      - `#FIREBRICK#painfully unnatural#LAST#` $\rightarrow$ `#FIREBRICK#反常得令人痛苦#LAST#`；
      - `#FIREBRICK#he#LAST#` $\rightarrow$ `#FIREBRICK#他#LAST#`（指代被阿戈尼尔误当成生命之血饮下的神祇盖里克 Gerlyk）。
  - **段落与标点**：正文 7 个段落结构及省略号占位符 `[...]`（译作 `[……]`）与原文完全一致；破折号与停顿节奏准确还原了濒死阿戈尼尔喘息断续的心理活动。
  - **专名与术语**：
    - `Sher'Tul` 译为“夏·图尔”；
    - `Ziguranth weapons` 译为“伊格兰斯的武器”（教团专名准确，符合教团/地点分立规则）；
    - `Angolwen` 译为“安格利文”（符合 2026-08-25 统一裁定）；
    - `Blood of Life` 译为“生命之血”；
    - `Elandar` 译为“埃兰达”。
  - 译文信实典雅，完全忠实于原文叙事与设定。

---

### 复核总结列表

| 条目编号 | 状态 | 主要结论与核验要点 |
| :--- | :--- | :--- |
| **entry-01226** | 未发现问题 | 梅琳达邪教献祭祭坛文本，专名与情节忠实，换行与标点无误。 |
| **entry-01227** | 未发现问题 | 死灵法师指南第 3 章，格式、引文全角引号与专名（崔恩/贝纳格雷德）一致。 |
| **entry-01228** | 存在疑点 | 不死猎人指南长文，存在明显增译与偏差：吸血鬼节末句脑补“刺穿喉咙”；骸骨巨人节脑补“法师老头们”并多处虚构修饰；骷髅节残留粗俗口语“算个屁指南”与过度意译；巫妖节单男化与误读；多处段落被人工拆分。 |
| **entry-01229** | 未发现问题 | 巅峰阿戈尼尔记忆钻石，8 处颜色与斜体标记完整对齐，术语与省略号准确。 |