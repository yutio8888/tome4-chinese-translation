## 40条译文复核判定表（entry-03533 至 entry-03572）

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03533 | 存在问题 | C01, C02, C03, C04 |
| entry-03534 | 未发现问题 | 章节标题翻译准确 |
| entry-03535 | 存在问题 | C05, C06 |
| entry-03536 | 未发现问题 | 章节标题翻译准确 |
| entry-03537 | 未发现问题 | 章节标题翻译准确 |
| entry-03538 | 未发现问题 | 章节标题翻译准确 |
| entry-03539 | 未发现问题 | 章节标题翻译准确 |
| entry-03540 | 仅建议 | C07 |
| entry-03541 | 存在问题 | C08 |
| entry-03542 | 未发现问题 | 章节标题翻译准确 |
| entry-03543 | 仅建议 | C09 |
| entry-03544 | 存在问题 | C10, C11, C12, C13 |
| entry-03545 | 未发现问题 | 章节标题翻译准确 |
| entry-03546 | 存在问题 | C14, C15, C16 |
| entry-03547 | 未发现问题 | 章节标题翻译准确 |
| entry-03548 | 未发现问题 | 章节标题翻译准确 |
| entry-03549 | 仅建议 | C17 |
| entry-03550 | 未发现问题 | 章节标题翻译准确 |
| entry-03551 | 未发现问题 | 章节标题翻译准确 |
| entry-03552 | 未发现问题 | 章节标题翻译准确 |
| entry-03553 | 未发现问题 | 章节标题翻译准确 |
| entry-03554 | 未发现问题 | 章节标题翻译准确 |
| entry-03555 | 存在问题 | C18, C19 |
| entry-03556 | 未发现问题 | 章节标题翻译准确 |
| entry-03557 | 未发现问题 | 章节标题翻译准确 |
| entry-03558 | 未发现问题 | 克诺什库尔Lore叙事翻译准确流畅 |
| entry-03559 | 未发现问题 | 奎科加Lore叙事翻译准确流畅 |
| entry-03560 | 未发现问题 | 乌鲁洛克Lore叙事翻译准确流畅 |
| entry-03561 | 未发现问题 | 刺客领主消息翻译准确 |
| entry-03562 | 存在问题 | C20 |
| entry-03563 | 存在问题 | C21, C22 |
| entry-03564 | 未发现问题 | 谜题日志翻译准确，格式控制符与%s占位符完整 |
| entry-03565 | 存在问题 | C23 |
| entry-03566 | 未发现问题 | 幸运汲取技能数值与占位符完整对应，逻辑准确 |
| entry-03567 | 未发现问题 | 衰亡技能数值与占位符完整对应，机制准确 |
| entry-03568 | 仅建议 | C24 |
| entry-03569 | 存在问题 | C25, C26 |
| entry-03570 | 存在问题 | C27 |
| entry-03571 | 存在问题 | C28 |
| entry-03572 | 未发现问题 | 触手舔舐技能5处占位符及属性术语完全正确 |

---

## 详细审核观察

### C01 | entry-03533 | 存在问题
- **原文短引**：`The messengers may have been killed, but the message they spread persisted.`
- **译文短引**：`信使的同伙们可能已经被杀了，但他们传播的信息仍然存在。`
- **问题内容**：主语对象篡改/过度脑补。原文“The messengers may have been killed”指被抓捕处决的煽动者/传播者（信使）本人可能已死，译文擅自增添“同伙们”，将受刑对象由信使本人歪曲为其同伙，改变了叙事逻辑。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:312`（DLC `cults` 公开快照，源码仓库与 commit 未固定），段首紧承前文“They publicly executed those who they believed to be the culprits...”，其主旨是处决信使本身无法阻断思想传播。

---

### C02 | entry-03533 | 存在问题
- **原文短引**：`The halfling trailed off to take a breath before continuing with the final sentence.`
- **译文短引**：`半身人拖着脚步喘口气，然后继续念最后一句话。`
- **问题内容**：动词短语严重误译。“trail off”在语境中意指语声渐弱、说话声音拖尾收声以换气（take a breath），译文望文生义将其错译为物理动作“拖着脚步”，且将并未照本宣科的口头说话（continuing with the final sentence）误译为“继续念”，动作完全走样。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:312`（DLC `cults` 公开快照，源码仓库与 commit 未固定），前句为半身人的话语以省略号结尾（`"... twist nature to their whims..."`），表明为语声停顿而非脚步移动。

---

### C03 | entry-03533 | 存在问题
- **原文短引**：`It was my turn to pause as this question was put to me.`
- **译文短引**：`当被问到这个问题之后，我了停下来。`
- **问题内容**：语法与字词倒错硬伤。译文出现“我了停下来”明显错别字/语病（应为“我停了下来”）。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:312`（DLC `cults` 公开快照，源码仓库与 commit 未固定），纯文本语病证据。

---

### C04 | entry-03533 | 存在问题
- **原文短引**：`"Of course, you seem like you are made of sterner composition than most."`
- **译文短引**：`“当然，你看起来比其他人都要更加顽固。”`
- **问题内容**：词义色彩颠倒与曲解。“made of sterner composition”指心智/意志比常人更为坚毅、坚韧（因此半身人才指引其前往反魔基地寻找导师），译文将其翻译为贬义的“更加顽固”（stubborn/obstinate），背离语境与人设立场。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:312`（DLC `cults` 公开快照，源码仓库与 commit 未固定），下文紧接半身人对主角坚毅性格的认可并指引其基地路线。

---

### C05 | entry-03535 | 存在问题
- **原文短引**：`I do hope it will serve as a reminder the to Shaloren, to never brashly use magic in such a way again.`
- **译文短引**：`我真的希望它能提醒人们，不要再以这种方式肆无忌惮地使用魔法。`
- **问题内容**：关键种族专名丢失与泛化。原文明确指明“serve as a reminder to the Shaloren”（作为给永恒精灵的警示），因魔法大爆炸系永恒精灵施法引发，菲·维莉欧斯作为自然精灵对此深感痛恨。译文泛化译为“提醒人们”，丢失了剧情核心的种族矛头与背景事实。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:340`（DLC `cults` 公开快照，源码仓库与 commit 未固定），结合固定世界观背景及下文对永恒精灵士兵撤退的描述。

---

### C06 | entry-03535 | 存在问题
- **原文短引**：`The action seemed to take the beings back a bit, and though still on edge they assumed a less aggressive stance.`
- **译文短引**：`这一举动似乎让他们后退了一点，尽管仍然和我对峙着，但他们采取了一种不那么咄咄逼人的姿态。`
- **问题内容**：习惯表达字面错译。“take sb back”（此处为 take aback 的同义变形）意指“让对方吃了一惊/感到意外”，译文望文生义硬译为物理动作“让他们后退了一点”；后文紧接着明确说明食人魔只是在心理戒备状态下放缓了攻击姿态（assumed a less aggressive stance），并非物理后撤。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:340`（DLC `cults` 公开快照，源码仓库与 commit 未固定），纯语义与语境证据。

---

### C07 | entry-03540 | 仅建议
- **原文短引**：`Escapades of Fay Willows [Book 3, Chapter 6] - Hateful Wrath`
- **译文短引**：`菲·维莉欧斯的冒险 [第3卷，第6章] - 仇恨愤怒`
- **问题内容**：措辞偏硬。“Hateful Wrath”直译为“仇恨愤怒”系两个名词简单拼合，语感略生硬，更自然的中文表达为“满怀仇恨的狂怒”或“仇恨与狂怒”。但当前译文已传达核心意义，不构成实质缺陷。
- **状态**：仅建议
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:464`（DLC `cults` 公开快照，源码仓库与 commit 未固定），章节名属于修辞偏好。

---

### C08 | entry-03541 | 存在问题
- **原文短引**：`Escapades of Fay Willows [Book 4, Chapter 1] - Exhaustive Travel`
- **译文短引**：`菲·维莉欧斯的冒险 [第4卷，第1章] - 穷途末路`
- **问题内容**：章节标题实质性误译。“Exhaustive Travel”结合正文内容指历经漫长奔波而筋疲力尽的长途跋涉（exhaustion from running, I collapsed），主角与食人魔一行成功脱离焦黑海岸并向埃尔瓦拉避难；译文错译为“穷途末路”（陷入绝境走投无路），完全颠倒了章节走向与原意。
- **状态**：已证实
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:490`（DLC `cults` 公开快照，源码仓库与 commit 未固定）及正文 491-507 行。

---

### C09 | entry-03543 | 仅建议
- **原文短引**：`Escapades of Fay Willows [Book 4, Chapter 3] - The Enchantress`
- **译文短引**：`菲·维莉欧斯的冒险 [第4卷，第3章] - 女巫`
- **问题内容**：术语区分度偏好。Enchantress 通常对应“附魔师”或“惑控师”，译为“女巫”易与巫术类（Witch）混淆。但在本任务冻结术语快照未单独强制收录 Enchantress 词条的前提下，译为“女巫”属于译者选词偏好，不计为硬性错误。
- **状态**：仅建议
- **源码与消费依据**：`sources/dlc/cults/tome-cults/data/lore/fay-willows.lua:536`（DLC `cults` 公开快照，源码仓库与 commit 未固定）。

---

### C10 | entry-03544 | 存在问题
- **原文短引**：`Of those questions asked though, the ones involving the treatment of the ogres have stuck out in my mind the most.`
- **译文短引**：`不过，在她提出的这些问题中，那些涉及对食人魔进行治疗的问题在我脑海中最为突出
