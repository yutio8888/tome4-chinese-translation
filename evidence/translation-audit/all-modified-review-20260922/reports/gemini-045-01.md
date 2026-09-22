### batch-045 译文只读复核报告

#### 1. 文件哈希核对
- 文件路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-045.md`
- 预期 SHA-256：`893562fd5fbd8f5c9bbbc6af49b965a7c69919f768862d7c643dd1437575c6e3`
- 实际 SHA-256：`893562fd5fbd8f5c9bbbc6af49b965a7c69919f768862d7c643dd1437575c6e3`
- 核验结果：一致。

本批共 6 条（`entry-01302` 至 `entry-01307`），全部位于 `mod-tome/data/lore/misc.lua`。公开源码依据固定 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/lore/misc.lua`](file:///workspace/t-engine4/game/modules/tome/data/lore/misc.lua)，译文上下文依据终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。逐条复核结果如下：

---

### 条目逐条复核

#### entry-01302
- **位置**：`mod-tome.lua:18083`（section: `mod-tome/data/lore/misc.lua`，lore `races-ogre` 正文）
- **状态**：**存在疑点** / **细微观察**
- **可核验依据**：
  1. **存在疑点（核心机制术语语义漂移）**：
     - 原文第 3 段：`the necessity of careful inscription has made their finger dexterity (and penmanship) rather impressive`
     - 译文作：“并且对于管理符文的重要性使他们手指变得十分灵巧，就连写出来的书法也令人印象深刻。”
     - 核验分析：在 ToME4 中，`inscription` 是贯穿食人魔生理与设定的核心机制专名「铭刻/刻印」（符文与纹身统称刻印，食人魔身体各处均需铭刻符文与草药纹身维系生命与结构完整，见下文 `runic inscription`、`inscribed patterns`）。原文表意为“精细铭刻（刻印）的必要性使得他们的手指十分灵巧（书法笔迹亦然）”，这是手部精细书写刻画带来的灵活性；译文译为“管理符文的重要性”，将“精细铭刻”曲解为“管理”，断裂了与后文手指灵巧、书法的因果逻辑。
  2. **细微观察（语意偏离与增减译）**：
     - 原文第 3 段：`to know the patient study and artistic vision they are capable of, if properly motivated`
       译文作：“就能了解到他们只要需要的情况下就能发挥出多么伟大的艺术造诣和技术水平”
       核验分析：原文 `patient study`（耐心的钻研/研习）被译为“技术水平”，`if properly motivated`（若受到恰当激励）被译为“只要需要的情况下”，偏离了原作者强调食人魔能耐心治学与艺术构想的语意。
     - 原文第 1 段：`from the Conclave's Overseers` -> 译文作“孔克雷夫的长老会”。Conclave 的 `Overseer` 官制（如 `High Overseer of Loyalty`）原意为监督官/监工，译为“长老会”略有泛化。
     - 原文第 5 段：`hijacked shipment of grain` -> 译文作“满载粮食的货船被劫”。`shipment` 在内陆奇幻语境下为批次物资运送，译为“货船”属于过度具象化。
  3. **格式与不变量核对**：无代码占位符，段落划分与原文 5 段严格对应，专名「马基·埃亚尔」「厄流纪」「魔法大爆炸」「魔法狩猎」「伊格兰斯」「埃尔瓦拉」均符合术语规范。

---

#### entry-01303
- **位置**：`mod-tome.lua:18100`（section: `mod-tome/data/lore/misc.lua`，lore `races-7` 标题）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 8 - Orcs (extinct)`
- **译文**：`博学者格雷诺特关于种族的调查——第八章——兽人（灭绝）`
- **状态**：**未发现问题**
- **可核验依据**：
  - 章节系列名 `Loremaster Greynot's Analysis of the Races` 译为“博学者格雷诺特关于种族的调查”，与同 section 下 Chapter 1 至 Chapter 11 译名体系完全统一；
  - 专名 `Orcs` 对应“兽人”，`(extinct)` 对应“（灭绝）”，破折号与标点符号格式规范，无占位符或参数问题。

---

#### entry-01304
- **位置**：`mod-tome.lua:18101`（section: `mod-tome/data/lore/misc.lua`，lore `races-7` 正文）
- **状态**：**未发现问题**
- **可核验依据**：
  - 关键专名与时代术语完全对齐：`Maj'Eyal` -> “马基·埃亚尔”（符合首选快照）、`Age of Ascendancy` -> “卓越纪”、`King Toknor the Brave` -> “勇者图库纳国王”、`Age of Pyre` -> “烈火纪”（符合规范）、`Spellblaze` -> “魔法大爆炸”、`Garkul the Devourer` -> “吞噬者加库尔”、`Battle of Nargol` -> “纳格尔之战”、`arcane abilities` -> “奥术能力”；
  - 数据与数值准确：`6'1"` -> “6英尺1英寸”、`10,000 halflings` -> “一万名半身人”、`100 years` -> “100多年”；
  - 5 段结构完整，语义忠实，准确传达了原文博学者的口吻与叙事色彩，标点及换行无异常。

---

#### entry-01305
- **位置**：`mod-tome.lua:18118`（section: `mod-tome/data/lore/misc.lua`，lore `races-8` 标题）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 9 - Sher'Tul (extinct)`
- **译文**：`博学者格雷诺特关于种族的调查——第九章——夏·图尔人（灭绝）`
- **状态**：**未发现问题**
- **可核验依据**：
  - 系列标题格式与 Chapter 8、Chapter 10 完全一致；
  - `Sher'Tul` 在术语库标准名为“夏·图尔”，此处译为“夏·图尔人”符合种族章节标题（对齐“人类”、“矮人”、“兽人”）的中文表达习惯，在库内有 27 处同类使用，且括号与破折号正确。

---

#### entry-01306
- **位置**：`mod-tome.lua:18119`（section: `mod-tome/data/lore/misc.lua`，lore `races-8` 正文）
- **状态**：**存在疑点** / **细微观察**
- **可核验依据**：
  1. **存在疑点（谓语漏译导致句式悬空与逻辑残缺）**：
     - 原文第 5 段：`Other theories hold weight though - Archiman Garybald, Professor of Demonic Studies, believes that the extensive uses of arcane energies by the Sher'Tul may have attracted twisted forces from other worlds which wiped out the ancient race.`
     - 译文作：“其他理论——阿奇曼·加里伯德，恶魔研究教授则相信，夏·图尔人大量使用奥术能量，可能因此引来了异界的扭曲力量，最终导致整个种族的毁灭。”
     - 核验分析：原文分句 `Other theories hold weight though` 意为“不过，其他理论也颇有分量／同样站得住脚——”，破折号后跟具体的学者观点作为例证。译文完全遗漏了谓语 `hold weight though`，将“其他理论”直接当作同位破折号引语引向学者姓名，导致中文缺少谓语成分，语义残缺断裂。
  2. **细微观察（词义缩窄与修饰语略译）**：
     - 原文第 5 段：`The most popular in academic circles at the moment...`
       译文作：“在考古界最流行的说法是……”
       核验分析：`academic circles` 为“学术界”，格雷诺特本人为 Loremaster（博学者），译为“考古界”缩小了学术范围。
     - 原文第 1 段：`this crucible race` -> 译文略译为“该种族”，略去了 `crucible`（严酷试炼／熔炉／创生摇篮）这一历史修饰语。
  3. **其他术语核对**：
     - `Age of Haze` -> “混沌纪”（与游戏内远古神明历史一致）；
     - `Age of Allure` -> “厄流纪”；
     - `farportals` -> “传送门”；
     - `Spellblaze` -> “魔法大爆炸”；
     - 段落结构与尺寸（`5'4"` -> 5英尺4英寸）均准确对应。

---

#### entry-01307
- **位置**：`mod-tome.lua:18136`（section: `mod-tome/data/lore/misc.lua`，lore `races-9` 标题）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 10 - Monstrous Races`
- **译文**：`博学者格雷诺特关于种族的调查——第十章——怪物种族`
- **状态**：**未发现问题**
- **可核验依据**：
  - 标题结构、章节编号（`Chapter 10` -> “第十章”）、系列译名与前后章节保持严格统一；
  - `Monstrous Races` 译为“怪物种族”通顺准确，标点排版正确，无占位符问题。