### 批次复核说明与哈希核对

- **批次编号**：batch-038
- **条目范围**：entry-01225 至 entry-01225（共 1 条）
- **文件校验**：
  - 目标文件：`evidence/translation-audit/all-modified-review-20260922/batches/batch-038.md`
  - 预期 SHA-256：`4afdf6d8e8eb4fcb636e783f7b3e2f76c007be9a727f419b8a2a727484f8bbe7`
  - 实际计算结果：`4afdf6d8e8eb4fcb636e783f7b3e2f76c007be9a727f419b8a2a727484f8bbe7`
  - 核对结论：一致，文件完整有效。
- **源码与译文对照基准**：
  - 公开源码：`t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（对应文件 `game/modules/tome/data/lore/elvala.lua`）。
  - 仓库译文端点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（对应 `mod-tome.lua` 行 15366 前后上下文）。

---

### 逐条复核报告

#### entry-01225
- **位置**：`mod-tome.lua:15366`
- **Section**：`mod-tome/data/lore/elvala.lua`
- **条目类型**：Lore 文本（《魔法大爆炸纪事(8)：禁忌》 / The Spellblaze Chronicles(8): Forbidden）
- **复核结论**：**存在疑点**（含动作方位与语意失真、断句残缺病句、结尾漏标点，以及实体术语与表达偏差点）

##### 1. 结构性病句与断句残缺（存在疑点）
- **原文第 25 段**：
  > `Dark grey skin covered a bulging head, topped with three great curved horns, which sat atop a long, thick body with six limbs.`
- **当前译文第 25 段**：
  > `深灰色的皮肤覆盖着它凸起的头部，顶部有三个巨大的弯角，长着六肢的长而厚的身体之上。`
- **可核验事实与证据**：
  原文后半句从句 `which sat atop a long, thick body with six limbs` 修饰头部（整颗头生于粗长六肢躯体之上）。译文后半句直译介词短语 `atop ...` 为「长着六肢的长而厚的身体之上」，遗漏了核心谓语动词（如“位于/立于……之上”），导致全句后半截成为缺乏谓语的残缺碎句，语法严重脱节。

##### 2. 动作方位逻辑错误与违和翻译腔（存在疑点）
- **原文第 18 段**：
  > `“Over here!” shouted Linaniil, as she dashed through the door she had split apart. I followed, slashing my blade through the mass of worms, causing it to lurch back screeching in pain, and spearing a blast of lightning through one of the spiked creatures, splitting open its head. It continued to attack me, but I parried and cut its arm off, dancing around it and reaching the doorway. With my back to the opening I brought up a wall of water and sent it flooding into the chamber, pushing the horrors away as I leapt backwards through the door.`
- **当前译文第 18 段**：
  > `“走这里！”莱娜尼尔大声喊道，她冲破了她分开的门。我紧跟向前，用我的刀片切开了那些蠕虫团，使它在痛苦中尖叫起来。同时，我发出一道闪电，穿过了某个长着尖刺的怪物，打破了他的脑袋。它试图继续攻击我，但我格挡了它，切下了它的手臂，在怪物的包围下起舞般闪避着他们的攻击，终于到达了门口。我面对着背后的怪物，建起一座水墙，然后释放一股洪水冲进了这个房间，把那些恐魔推到了外面，顺便跳进了我背后的门中。`
- **可核验事实与证据**：
  - **方位逻辑严重混乱**：原文 `With my back to the opening` 意为主人公退到石门前，“背对入口/门洞”（面对追击而来的虫群与恐魔）。译文写成「我面对着背后的怪物」，在同一分句中自相矛盾，且扭曲了背向门洞的防御站位。
  - **严重失真的语气词**：原文 `as I leapt backwards through the door` 是撤退的高潮动作（“当我向后纵身跃入门中时” / “随即倒跃退入门内”）。译文翻译为「顺便跳进了我背后的门中」，在千钧一发的大逃亡死斗描写中使用闲散轻率的「顺便」，不仅脱离原文词义，也破坏了叙事张力。
  - **生硬字面机翻**：主人公艾伦尼恩（Aranion）佩带的是名剑斩月（Mooncutter，大剑），原文 `slashing my blade through the mass of worms` 译为「用我的刀片切开了那些蠕虫团」，将大剑剑刃/佩剑直译为「刀片」，产生明显的翻译腔与违和感。
  - **语义别扭**：`she dashed through the door she had split apart` 原指莱娜尼尔穿过刚才被她奥术轰开的门洞（前文已轰碎石门），译文「冲破了她分开的门」用词不当。

##### 3. 标点符号遗漏与格式瑕疵（存在疑点 / 细微观察）
- **末尾漏句号**：
  - 原文第 41 段：`“Now, ye go home, and I go to make mine home, a sanctuary for me and mine people.”`
  - 译文第 41 段：`“现在，你可以回家，而我则要建造我的家园，一个为我和我的人民建立的避难所”`
  - 证据：引语末尾完全缺失句号（引号内外皆无标点）。
- **多处引号外标点倒置**（细微观察）：
  - 第 20 段：`“阿马克泰尔的子嗣”，她冷静地回答道。`
  - 第 22 段：`“奎科加”，她回答道。`
  - 第 26 段：`“它就在这里”，莱娜尼尔说道。`
  - 第 34 段：`“不！”，我大叫着`
  - 第 44 段：`“不过现在，再见，艾伦尼恩”，她的身体……`
  - 证据：对话末尾将句读点或叹号置于引号外或叹号后再加逗号，不符合标准的中文标点排版习惯。

##### 4. 实体怪物术语与细节动作偏差（细微观察）
- **怪物名称未对齐核心实体术语**：
  - 原文第 36 段：`two more luminous horrors, and some fiend of darkness and nightmares`
  - 译文：`另外两个闪烁着光辉的恐魔，还有一些某种暗影和噩梦的魔鬼`
  - 证据：对照源码 `game/modules/tome/data/general/npcs/horror.lua` 及术语快照，`luminous horror` 为核心游戏实体「金色恐魔」（已固定实体名），此处译文处理成了描述性短语「闪烁着光辉的恐魔」；且后半句 `some fiend`（单数）译为「一些某种」，同时出现复数“一些”与单数“某种”，产生词义重叠语病。
- **关键战斗动作漏译**：
  - 原文第 35 段：`The being of light and tentacles passed through my flames without resistance, and I ran sparks along my sword as I tore it up the centre of the monster.`
  - 译文：`那些发着光的触手怪物轻松穿过了我所造出的火墙，我冲上前去，试图用我的剑刃刺穿这个怪物的核心。`
  - 证据：
    1. 单复数不符：原文主语 `The being of light and tentacles` 为单数特指，译文变为复数「那些发着光的触手怪物」。
    2. 原文法术剑士引导雷电附魔长剑的标志性动作 `I ran sparks along my sword`（我令剑刃上迸射出电火花/跃动电光）在译文中被直接省略，笼统概括为“试图用我的剑刃刺穿……”。
- **姿态与词汇细节**：
  - 原文第 32 段 `hanging with one hand from her staff`（单手悬挂在插入冰中的法杖上），译文作「一只手紧握她的法杖」，遗漏了莱娜尼尔悬空的身体姿态细节。
  - 原文第 33 段 `her staff shattered` 译为「她的法杖被瞬间破碎」（被动语态生硬），`The corpse of the dead god` 译为「已死神的尸体」（脱字，前文均为“已死之神”）。
  - 原文第 3 段 `all my senses seemed on edge`（感官高度戒备/神经紧绷）被误解译为「感觉我的感官快要到极限了」。

##### 5. 格式与无问题部分核验
- **格式码验证**：`#{italic}#...#{normal}#` 以及 `#{bold}#...#{normal}#` 开闭匹配完整，未见损坏。
- **变量与占位符**：本段无 `%s`、`%d` 等格式化占位符。
- **关键人名与地名保持准确一致**：
  - Aranion Gawaeil -> 艾伦尼恩·加威尔
  - Elvala -> 埃尔瓦拉
  - Linaniil -> 莱娜尼尔
  - Mooncutter -> 斩月剑
  - Sher’Tul -> 夏·图尔 / 夏·图尔人
  - Quekorja -> 奎科加
  - Scions of Amakthel -> 阿马克泰尔的子嗣
  - Angolwen -> 安格利文
  - Age of Pyre -> 烈火纪
  - Garkul the Devourer -> 吞噬者加库尔
  - Tales of Maj’Eyal -> 马基·埃亚尔的传说
  - Ring of Kar’Krul -> 卡库罗尔的戒指（与同文本传记前序章节译名严格一致）

---

### 复核总结表

| 条目编号 | 检查状态 | 核心问题摘要 |
| :--- | :--- | :--- |
| **entry-01225** | **存在疑点** | 1. 第 25 段末句缺少谓语动词形成断裂病句；<br>2. 第 18 段动作方位逻辑矛盾（“面对背后的怪物”）、违和翻译腔（佩剑译为“刀片”、倒跃跃入译为“顺便跳进”）；<br>3. 第 41 段末尾完全遗漏句号，多处引语存在引号外标点；<br>4. 第 36 段核心实体 `luminous horror`（金色恐魔）未统一且出现“一些某种”语病，第 35 段漏译剑刃附电火花动作并混淆单复数。 |