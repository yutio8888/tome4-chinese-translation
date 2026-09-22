本批次为 **batch-041**，已在核验前完成文件哈希校验：
- 文件路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-041.md`
- 校验哈希（SHA-256）：`5472c56d9c45046bd3faee5d99fe73c84cc206da9bad0f90643b95aeeb5c1985`（核对一致）
- 源码依据：固定版本公开源码 `t-engine4` commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/lore/...`）
- 覆盖条目：`entry-01250` 至 `entry-01268`，共 19 条

以下为逐条复核报告：

---

### entry-01250
- **位置**：`mod-tome.lua:16602`
- **对应源码**：`game/modules/tome/data/lore/keepsake.lua:79` (`keepsake-vault-entrance`)
- **复核结论**：未发现问题
- **核验依据**：叙事文本翻译忠实顺畅，术语“凯勒斯”（Kyless，Keepsake 任务线首领）与术语库 preferred 统一，“藏宝室”（vault）与前置名称词条一致。标点、句式完整，段尾换行符（`\n\n`）与原文严格保持一致。

---

### entry-01251
- **位置**：`mod-tome.lua:16621`
- **对应源码**：`game/modules/tome/data/lore/keepsake.lua:93` (`keepsake-kyless-encounter` 名称)
- **复核结论**：未发现问题
- **核验依据**：原文为专名 `Kyless`，译文作“凯勒斯”，符合术语库 preferred 裁定（`T.PN.PERSON`，替代旧译“克里斯”）。

---

### entry-01252
- **位置**：`mod-tome.lua:16622`
- **对应源码**：`game/modules/tome/data/lore/keepsake.lua:95` (`keepsake-kyless-encounter` 正文)
- **复核结论**：未发现问题（附细微观察）
- **核验依据**：整体语义准确传达了凯勒斯陷入疯狂并向主角发起袭击的紧张氛围。末尾空行换行与原文一致。
- **细微观察**：原文末句为实心句号 `Kyless smiles and then attacks.`，译文作“凯勒斯嘴角扬起一抹微笑，向你发起了攻击……”，添加了中文省略号以增强战斗触发前的悬念氛围，属修辞润色，核心信息未缺失。

---

### entry-01253
- **位置**：`mod-tome.lua:16634`
- **对应源码**：`game/modules/tome/data/lore/keepsake.lua:107` (`keepsake-berethh-death-good`)
- **复核结论**：未发现问题
- **核验依据**：对应被诅咒者（Cursed）在遗物任务善线（意志坚定）下的结局文本。核心句“The cold iron hardens your resolve.”准确译为“冰冷的铁质橡果让你的意志变得坚定”，专名“贝里斯”（Berethh）、“凯勒斯”（Kyless）拼写与译法一致，换行及标点无误。

---

### entry-01254
- **位置**：`mod-tome.lua:16649`
- **对应源码**：`game/modules/tome/data/lore/keepsake.lua:123` (`keepsake-berethh-death-evil`)
- **复核结论**：未发现问题
- **核验依据**：对应恶线（复仇怒火）结局文本，与 01253 的差异句“The acorn now serves as a focus for your anger. Though the curse may consume you, there are many who deserve your wrath. And they will feel it.”准确译为“如今，这颗橡果承载着你所有的愤怒。尽管诅咒可能会吞噬你，但仍然有许多人理应承受你的怒火。他们会尝到这怒火的滋味”，情绪与语义传达精准，格式无误。

---

### entry-01255
- **位置**：`mod-tome.lua:16670`
- **对应源码**：`game/modules/tome/data/lore/kor-pul.lua:34` (`kor-pul-note-1`)
- **复核结论**：未发现问题
- **核验依据**：太阳骑士泰尔沙（Telthar）的日记文本。专名“泽梅基斯”（Zemekkys）、职业“太阳骑士”（Sun Paladin）、阵营“不死族”（undead）翻译符合设定；“Why in the blackest night...”结合太阳骑士设定传神译为“至暗长夜在上”；四个段落的段间双换行与末尾格式完全契合。

---

### entry-01256
- **位置**：`mod-tome.lua:16683`
- **对应源码**：`game/modules/tome/data/lore/kor-pul.lua:46` (`kor-pul-note-2`)
- **复核结论**：存在疑点
- **核验依据**：
  1. **非预期硬换行截断**：源码原文第 2 段为一个完整的单一自然段（`I've found myself an old shield... poisonous bites before I get my sword to their necks. I also found a few gems...`）。但在译文中，在“阻止它们带毒的撕咬。”之后插入了一个单换行符 `\n`，将该段硬生生切成了两行（“我还发现了一些宝石……”换到了新行）。在游戏 Lore 弹窗排版中会造成异常断行。
  2. **标点连用**：第 3 段末尾原文为 `Diamonds are my favourite, so sparkly.`，译文作“我最喜欢钻石了，一闪一闪亮晶晶～。”，末尾存在波浪号与实心句号连用（`～。`）。

---

### entry-01257
- **位置**：`mod-tome.lua:16805`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:107` (`last-hope-toknor-statue`)
- **复核结论**：未发现问题
- **核验依据**：图库纳国王雕像铭文。纪元日历“烈火纪”（Age/Year of Pyre）、“卓越纪”（Age of Ascendancy）、月份“厄流月”（Allure）与“炎华”（Summertide，对照 `mod-tome.lua` 中的 `calendar allied` 规范）完全一致；地名“最后的希望”（Last Hope）、专名“图库纳国王”（King Toknor）、种族“兽人”（Orcs）统一且引文完整。

---

### entry-01258
- **位置**：`mod-tome.lua:16815`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:117`
- **复核结论**：未发现问题
- **核验依据**：米雯尼雅女王雕像铭文。日历月份“辉耀月”（Flare）、“炎华”（Summertide）准确；身份“炼金术士”（alchemist）、战役“最后的希望战役的救世主”与引文“Nothing moves me more than seeing the sun set over Last Hope...”对应无误，段落与格式一致。

---

### entry-01259
- **位置**：`mod-tome.lua:16826`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:125` (`southspar-note-1`)
- **复核结论**：存在疑点
- **核验依据**：
  1. **实质概念错译与信息窄化**：原文第 8 段为 `Southspar celebrated its peace and its newly found military might, but for Drake, the celebration was short-lived.`，译文作“南晶岛欢庆胜利和它新建的游击力量。但是对德瑞克来说，这番庆祝没有持续多久。”。原文中的 `peace`（和平）被实质错译为“胜利”；且 `newly found military might`（新获得的军事力量）被擅自窄化并改写为“新建的游击力量”。
  2. **专名/军号过度意译**：德瑞克组建的军队在原文中被冠以特定名称 `"Army of Rogues"`（以及后文 `Army of Rogues' knives and armour`），译文多处意译为“游击军”，虽然上下文体现了游击刺杀战术，但剥离了与盗贼（Rogue）职业专名的词源对应与双关色彩。
  3. **标点与数字规范不一**：内部小标题序号原文为西文点（`1.`、`2.`），译文改为中文顿号（`1、`、`2、`）；后文数字在前段写作汉字“二十倍”，末尾协议处写作半角“30倍”。

---

### entry-01260
- **位置**：`mod-tome.lua:17001`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:253` (`celia-letter`)
- **复核结论**：未发现问题
- **核验依据**：塞莉亚（Celia）写给塞西尔（Cecil）的绝笔信。7 个自然段结构完整，空行完全对应；情感表达准确，“tinctures”（药剂）、“with child”（怀孕）、“abominations”（畸形怪物）、“gentle kick”（指代腹中胎动，准确译为“腹中轻轻一踢”）等细节翻译精准，未发现缺漏或逻辑偏离。

---

### entry-01261
- **位置**：`mod-tome.lua:17099`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:309` (`last-hope-graveyard-7`)
- **复核结论**：未发现问题
- **核验依据**：德斯镇格兰（Golan of Derth）的墓碑。地名“德斯镇”（Derth）符合术语库；样式标签 `#{bold}#`、`#{normal}#`、`#{italic}#` 闭合配对与换行完全正确。

---

### entry-01262
- **位置**：`mod-tome.lua:17299`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:447` (`last-hope-graveyard-18`)
- **复核结论**：存在疑点
- **核验依据**：专名音译残缺。原文墓主为 `Raymond Gaustadnes`（挪威语姓名，致敬为 ToME 绘制大量像素图的贡献画师 Raymond Gaustadnes，下句因此为“The Pixels finally got him...”）。译文作“雷蒙德·加斯塔德在这里长眠”，其姓氏 `Gaustadnes` 漏译了末尾音节 `-nes`（常见规范音译为“加斯塔德尼斯”或“高斯塔德尼斯”）。

---

### entry-01263
- **位置**：`mod-tome.lua:17473`
- **对应源码**：`game/modules/tome/data/lore/last-hope.lua:561` (`last-hope-graveyard-35`)
- **复核结论**：未发现问题（附细微观察）
- **核验依据**：墓碑格式标签匹配完整，生卒年数字一致。
- **细微观察**：原文墓主名字为 `Foursaw the Clown`，后文为双关短诗 `We laughed / Until we saw / The joke was over`（Foursaw 谐音 foresaw“预见”，与后文 saw“看见”形成双关）。译文处理为“小丑先觉”与“直到察觉”，以“先觉/察觉”成功传达了英文原作的字面双关游戏，处理精当。

---

### entry-01264
- **位置**：`mod-tome.lua:17555`
- **对应源码**：`game/modules/tome/data/lore/misc.lua:27` (`temple-creation-note-1` 名称)
- **复核结论**：未发现问题
- **核验依据**：造物主神庙三卷书册之一的名称词条，`tract of destruction` 准确译为“毁灭之卷”，与 entry-01265 内部大标题一致。

---

### entry-01265
- **位置**：`mod-tome.lua:17556`
- **对应源码**：`game/modules/tome/data/lore/misc.lua:28` (`temple-creation-note-1` 正文)
- **复核结论**：未发现问题
- **核验依据**：标题样式标签完整，专名“魔法大爆炸”（Spellblaze）、“纳鲁人”（Nalorën people）翻译正确，段落结构与叙事语境准确，无格式缺陷。

---

### entry-01266
- **位置**：`mod-tome.lua:17569`
- **对应源码**：`game/modules/tome/data/lore/misc.lua:40` (`temple-creation-note-2` 名称)
- **复核结论**：未发现问题
- **核验依据**：造物主神庙第二卷书册名称词条，`tract of anarchy` 准确译为“无序之卷”，符合卷册命名规范。

---

### entry-01267
- **位置**：`mod-tome.lua:17570`
- **对应源码**：`game/modules/tome/data/lore/misc.lua:41` (`temple-creation-note-2` 正文)
- **复核结论**：存在疑点（实质矛盾与词义误译）
- **核验依据**：
  1. **标题词义误译与卷册名冲突**：原文大标题为 `#{bold}#Tract of Anarchy#{normal}#`，译文误作 `#{bold}#无序之治#{normal}#`。在造物主神庙全系列书卷中，“Tract”均统一译为“卷”（参见 01264/01265 的 `Tract of Destruction` -> “毁灭之卷”，01268 的 `tract of acceptance` -> “接纳之卷”，以及同文件后续 Slasul 笔记中的 `The Tract of the Devourer` -> “吞噬者之卷”）。译作“无序之治”将“Tract（书卷/篇章）”误写/误译为政治统治相关的“治”。
  2. **与物品名称直接冲突**：该条目与其前置物品名称词条 entry-01266（`tract of anarchy` -> “无序之卷”）发生直接冲突，导致玩家在游戏中拾取物品名为“无序之卷”，打开后界面顶端标题却显示为“无序之治”。
  3. **逻辑语义矛盾**：Anarchy 意为无政府与混乱状态，“无序之治”产生严重自相矛盾的词义扭曲，违背原作意旨。

---

### entry-01268
- **位置**：`mod-tome.lua:17583`
- **对应源码**：`game/modules/tome/data/lore/misc.lua:53` (`temple-creation-note-3` 名称)
- **复核结论**：未发现问题
- **核验依据**：造物主神庙第三卷书册名称词条，`tract of acceptance` 准确译为“接纳之卷”，符合神庙卷册命名规范与后续正文标题。