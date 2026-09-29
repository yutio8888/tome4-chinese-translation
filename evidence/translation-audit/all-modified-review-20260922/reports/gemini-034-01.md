# 译文复核报告：batch-034

## 1. 批次与环境核验

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-034.md`
- **文件 SHA-256 哈希核对**：`e04092a0a1a441ac829983e3c57fab623b96d5b32486e02cb94786d623813dcc`（核对一致）
- **条目范围**：`entry-01221` 至 `entry-01221`（共 1 条，已完成逐条核查）
- **源码参考基准**：
  - 仓库：`t-engine4`（固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
  - 对应源码路径：`game/modules/tome/data/lore/elvala.lua`（第 226–369 行，`id = "spellblaze-chronicles-4"`）
  - 译文仓库语境端点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00:mod-tome.lua`（section `"mod-tome/data/lore/elvala.lua"`，第 14988–15091 行）

---

## 2. 逐条复核详情

### entry-01221

- **位置**：`mod-tome.lua:14988`
- **Section**：`mod-tome/data/lore/elvala.lua`
- **Source Tag**：`_t`
- **分类**：**存在疑点**

#### 格式与控制符核验
- **样式标记**：
  - 标题一 `#{italic}#...#{normal}#` 完整保留。
  - 标题二 `#{bold}#...#{normal}#` 完整保留。
- **变量与占位符**：无变量占位符或颜色控制代码。
- **段落结构**：原文由 27 个逻辑段落/对话块组成，译文同样由 27 段构成，段落结构整体对应。

---

#### 详细疑点与可核验依据

##### 1. 第 17 段存在严重错译、逻辑颠倒与无中生有的增译（Fidelity / Completeness 疑点）
- **英文原文**：
  > `“It may well be that this is no dream. For this is no normal day, and even in all the legends of ages past this will stand out as a day of reckoning. Our civilisation in under peril, our way of life threatened from the orcish scourge. We rest upon a knife edge, the world balancing on a pivot, and the wrong sway could tip us into darkness and despair forever. Our actions today will decide this. So yes, you have had a warning, you have had a message, and that message is to be strong. For today we all hold the reins of fate in our palms, and only the steady hand can guide us past the threat of doom that is to come. Neira, can you be that steady hand?”`
- **当前译文**：
  > `“这很可能确实不是一个梦。你知道，世界上没有一天不处在危险之中，而今天则是比任何时代的任何传奇中的日子都要重要的一天。我们的文明正处在危险之中，我们的生活方式正遭受兽人们野蛮侵袭的威胁。我们的命运宛如悬于刀尖之上，我们的和平生活正摇摇欲坠，任何错误的决断都会让我们跌入黑暗和绝望的深渊。今天，我们将会做出最大的决断。所以你说的对，你收到了一个消息，你受到了一条警告。而我们所应该做的，就是回应这个警告，就是变得足够坚强。今天，我们要紧握希望的缰绳，我们要扼住命运的咽喉，只有这双真正坚实的双手才能引领我们逃离袭来的毁灭，才能给我们带来真正的和平。尼耶拉小姐，你能成为我们坚实的双手吗？”`
- **可核验依据**：
  1. **错译与句意反转**：
     - 原文为 `For this is no normal day, and even in all the legends of ages past this will stand out as a day of reckoning.`（因为今天绝非寻常之日，即便在过往所有世代的传说之中，今日也将作为清算/审判之日而彪炳史册）。
     - 译文处理为“**你知道，世界上没有一天不处在危险之中**，而今天则是比任何时代的任何传奇中的日子都要重要的一天”。
     - 译者将 `no normal day` 误读并脑补为“世界上没有一天不处在危险之中”，不仅无中生有，且逻辑颠倒（原文强调“今天不平常、极其特殊”，译文却成了“每天都很危险”），并漏译了 `day of reckoning`（清算之日）。
  2. **过度臆造与非原文修辞套用（加字扩充）**：
     - 原文为 `For today we all hold the reins of fate in our palms, and only the steady hand can guide us past the threat of doom that is to come.`（因为今天我们都将命运的缰绳握在手心，只有沉稳坚定的手，才能指引我们越过即将降临的毁灭威胁）。
     - 译文扩写为：“**我们要紧握希望的缰绳，我们要扼住命运的咽喉**，只有**这双真正坚实的双手**才能引领我们逃离袭来的毁灭，**才能给我们带来真正的和平**。”
     - 原文只有“握住命运的缰绳”（`reins of fate`），译文凭空扩充编造出两句排比（“紧握希望的缰绳”、“扼住命运的咽喉”），并在末尾凭空增添了“才能给我们带来真正的和平”。
  3. **单复数与语法脱节**：
     - 原文是单数 `the steady hand`，比喻能稳住局势的坚定之人（“Neira, can you be that steady hand?” 尼耶拉，你能成为这只稳健之手吗？）。
     - 译文译为复数“这双真正坚实的双手”，导致下文问句变成“你能成为我们坚实的双手吗？”，单复数与代词指向失调。

---

##### 2. 第 8 段存在实体化误译、漏译与曲解（Fidelity 疑点）
- **英文原文**：
  > `...those pillars of smoke suddenly seemed to look like a demonic hand stretching over the world, ready to dig its claws into the earth and rip out the flesh beneath. This, I knew, was the threat the orcs faced to us all, a menace to all civilisation. Whatever price we paid to stop them would be a small one. So I thought. So we all thought.`
- **当前译文**：
  > `...这些烟柱如同伸展到世界各地的魔爪，正准备撕开地面，吞噬一切。这个恶魔就是兽人，它是对我们任何种族的威胁。无论付出什么代价来阻止他们都不过分。这就是我当时的想法，这就是我们所有人当时的想法。`
- **可核验依据**：
  1. **遗漏生动意象**：`rip out the flesh beneath`（撕出地底的血肉，呼应前文被焚烧掠夺的村镇生灵）被概括为“吞噬一切”。
  2. **实体化误译与术语偏离**：
     - 原文 `This, I knew, was the threat the orcs faced to us all, a menace to all civilisation.`（句中 `This` 代指前句烟柱化作魔爪撕裂大地的可怖景象：“我深知，这便是兽人带给我们所有人的威胁，是对整个文明的祸患”）。
     - 译文误将前文的比喻 `demonic hand` 当成承前代词，译为“**这个恶魔就是兽人，它是对我们任何种族的威胁**”，不仅凭空把兽人定性为“这个恶魔”，还将 `all civilisation`（所有文明 / 整个文明）曲解错译为“任何种族”。

---

##### 3. 第 20 段存在错别字与主被动混淆（Fidelity / Grammar 疑点）
- **英文原文**：
  > `They all cheered and rushed to order their troops, taking courage from the duties of command. Neira went to her own mages, and I left the pavilion alone.`
- **当前译文**：
  > `被刚才的命令所鼓舞，所有人欢呼着冲向前去，组织起他们的部队。尼耶拉回身组织其她手下的法师，而我独自离开了帐篷。`
- **可核验依据**：
  1. **错别字**：“尼耶拉回身组织**其她**手下的法师”中，“其她”为明显错别字，应为“组织**起她**手下的法师”或“组织**其**手下的法师”。
  2. **主被动混淆**：原文 `taking courage from the duties of command` 主语是那些将领领袖（他们在行使指挥职责、给部队下达指令的过程中重新振作、获得勇气）。译文译为“被刚才的命令所鼓舞”，误将领袖行使指挥职责（`duties of command`）理解为被 Aranion 先前的命令鼓舞。

---

##### 4. 第 25 段动作与氛围误译（Fidelity 疑点）
- **英文原文**：
  > `“Thank you, Aranion,” she whispered. Turning up her face she kissed me, and it was the softest, most delicate kiss she ever gave me. It was also the last.`
- **当前译文**：
  > `“谢谢你，艾伦尼恩。”她悄然说道。她转过头，与我长吻。这是我和她所经历的最柔软，最细腻的一个吻，也是我和她的最后一个吻。`
- **可核验依据**：
  1. **肢体动作反向误译**：Aranion 正将莱娜尼尔拥入怀中（`wrapped my arms around her slender frame`），`Turning up her face` 是“仰起脸 / 抬起头迎向他”。译文译为“**转过头**”，在中文语境下转头通常指把头扭向一侧，与拥抱接吻的动作矛盾。
  2. **氛围增添失当**：原文明确描写吻的特征为 `the softest, most delicate kiss`（最轻柔、最纤巧细腻的吻），译文却添加了“**与我长吻**”，与后半句的细腻轻柔产生冲突。

---

##### 5. 细微观察（意译度高或语境微瑕，供参考）
- **第 10 段**：`Kar’Krul pavilion` 译为“卡库罗尔的营地”。前一段已是 `Kar’Krul camp`（卡库罗尔的营地），此处 `pavilion`（大帐 / 军帐）再次译为“营地”略有重复。
- **第 11 段**：`doubt evident in her eyes`（眼中明显流露出疑虑）译为“眼神却包含着无尽的困扰之情”，弱化了对计划本身的“疑虑（doubt）”。
- **第 16 段**：`as her sister raved`（当她妹妹胡乱嚷嚷/狂躁失态时）译为“在尼耶拉慷慨激昂的怒吼声中”，将贬义/失态的 `rave` 翻译为褒义正向的“慷慨激昂”；同句中 `bringing my face close`（将脸凑近）未体现，被替换成了下一段开头的“慢慢向她说道”。
- **第 23 段**：`beneath all the bravado and humour` 遗漏了 `bravado`（逞强 / 虚张声势），且译文“在她平日幽默的语调中”加入了原文没有的“平日”（原文指方才在空帐篷里玩笑时的故作坚强）。
- **人名称呼风格微差**：第 14 段 Neira 直呼 `Aranion` 译为“艾伦尼恩先生”，第 18 段直呼 `Aranion` 译为“艾伦尼恩阁下”，两处称谓不完全一致。

---

## 3. 复核结论汇总

| 条目编号 | 所在文件及位置 | 状态判定 | 主要事实依据概要 |
| :--- | :--- | :--- | :--- |
| `entry-01221` | `mod-tome.lua:14988` | **存在疑点** | 第 17 段严重错译（`no normal day` 颠倒为“世界上没有一天不处在危险之中”）及大量臆造加字；第 8 段将魔爪比喻实体化为“这个恶魔就是兽人”且将文明错译为“任何种族”；第 20 段存在错别字（“组织其她手下的法师”）及指挥职责主被动误译；第 25 段 `Turning up her face` 错译为“转过头”并擅加“长吻”。 |