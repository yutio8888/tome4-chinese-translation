# batch-037 译文复核报告

### 1. 冻结哈希与文件核验
- **目标文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-037.md`
- **预期 SHA-256**：`9a60a2f0049af85e538fc4cfd66d61f72c95266b971e731bd02d7698decd0557`
- **实测 SHA-256**：`9a60a2f0049af85e538fc4cfd66d61f72c95266b971e731bd02d7698decd0557`（核对一致）
- **复核范围**：`entry-01224` 至 `entry-01224`，共 1 条。
- **源码基准**：固定 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4) 之 `game/modules/tome/data/lore/elvala.lua:413-448`。
- **译文基准**：当前工作树固定终点 [`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua#L15300) 之 `mod-tome.lua:15300`。

---

### 2. 逐条复核详情

#### 【存在疑点】entry-01224
- **位置**：`mod-tome.lua:15300`
- **Section**：`mod-tome/data/lore/elvala.lua`
- **Source Tag**：`_t`
- **原文标识**：`The Spellblaze Chronicles(7): Into Darkness`（《魔法大爆炸纪事(7)：进入黑暗》）

##### 格式与标记核对
1. **控制码与样式标签**：原文首尾包含 `#{italic}#...#{normal}#` 与 `#{bold}#...#{normal}#`，译文格式标签成对匹配且闭合正确。
2. **段落与空行**：原文共 16 个自然段落（含标题与副标），译文段落数与换行结构 1:1 严格对齐，无串行或并段。
3. **占位符**：纯叙事文本，无 `%s`、`%d` 等变量占位符。

##### 术语与专名核对
- **Spellhunt** 译为「魔法狩猎」（符合术语库 preferred 规范，与 Spellblaze「魔法大爆炸」区分清晰）。
- **Ziguranth** 译为「伊格兰斯」（此处指代反魔教团组织，符合教团用「伊格兰斯」、据点用「伊格」的区分规则）。
- **stralite mail** 译为「斯莱特锁甲」（材质名符合 stralite preferred 统一为「斯莱特」的要求）。
- **Shaloren / Shalore** 译为「永恒精灵」，**halfling** 译为「半身人」，**necromancers** 译为「死灵法师」，人名 **Aranion Gawaeil**「艾伦尼恩·加威尔」、**Linaniil**「莱娜尼尔」及地名 **Elvala**「埃尔瓦拉」均与全系列各章节保持一致。
- **Wintertide moon** 译为「霜华之月的月牙」（符合游戏历法及近地卫星 Wintertide「霜华」设定）。

##### 疑点与核验依据
1. **存在疑点（同音错别字）**：
   - **原文**（段落 8）：
     `Fifteen long years passed before I awoke one night in my council chambers, the crescent Wintertide moon softly illuminating a shape near the end of my bed.`
   - **译文**：
     `十五年后的一个夜晚，我在我的议会室里醒来，看到霜华之月的月牙微光照亮了我床位的一个身影。`
   - **证据与分析**：
     `the end of my bed` 指床尾（与床头相对的一端）。同系列第二章（`mod-tome.lua:14726` / `14770`）描写莱娜尼尔夜访时，原文 `at the foot of my bed` 准确译为了「我的床尾」。此处「照亮了我床位的一个身影」中的「床位」明显为同音字误（chuang wei），在汉语中「床位」指卧铺、病床或铺位编号，置于此语境中表意不当，宜校正为「床尾」。

##### 细微观察（供主代理裁决参考）
1. **指代与修辞冗余**（段落 9）：
   - **原文**：
     `She turned to me, and I saw those same dark eyes I remembered. But they were surrounded by lines of care, the markings of years of strain and responsibility clear on her face.`
   - **译文**：
     `她的身体转向我，我看到我记忆中的那双黑色的眼睛。然而，她的脸上已经充满了操劳的痕迹，岁月、压力和责任已经在她的脸上留下了痕迹。`
   - **证据与分析**：
     原文 `they were surrounded by lines of care` 的主语代词 `they` 指代前面的 `dark eyes`，意为「那双眼睛周围布满了操劳的皱纹」。译文将其概括为「她的脸上已经充满了操劳的痕迹」，导致紧接着的后半句又出现「已经在她的脸上留下了痕迹」，在同一句内连续重复相同的句式与「痕迹」一词，且削弱了原文对眼角皱纹（lines of care）的特写。
2. **直接引语标点位置**（段落 11）：
   - **原文**：`“I have come for help, Aranion,” she said in a low voice...`
   - **译文**：`“我是来这里请求帮忙的，艾伦尼恩”，她用低沉的声音说道...`
   - **证据与分析**：逗号置于后双引号之外（`“...”，`），属于常见排版习惯差异，不影响剧情阅读。

---

### 3. 复核结论汇总
- **覆盖条目**：1 条（`entry-01224`）
- **核验结果**：
  - `entry-01224`：**存在疑点**（「床位」疑为「床尾」同音错字；附带 2 处修辞/排版细微观察）。