### 前置文件校验

- **复核批次**：`batch-031`
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-031.md`
- **SHA-256 校验**：`fbad9e6b870ad4487008fa3a9e6e2937e17f6115b58074fe70fef0150e66b27e`（经核对完全一致）
- **源码参考基准**：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git -C /workspace/t-engine4 show` 读取公开源码）；译文终点为 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核报告

#### entry-01205
- **位置**：`mod-tome.lua:13677`（section: `mod-tome/data/ingredients.lua`）
- **原文**：`Try to get any knots out before returning. Wear gloves.`
- **译文**：`在回来之前把打结在上面的其他蠕虫统统清理掉。戴上手套。`
- **复核结论**：**存在疑点**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/ingredients.lua` 中 `GREEN_WORM` 的定义：
  ```lua
  newIngredient{ id = "GREEN_WORM",
      ...
      desc = _t[[A dead green worm, painstakingly separated from its tangle of companions.]],
      alchemy_text = _t"Try to get any knots out before returning. Wear gloves.",
  }
  ```
  前一句物品描述已明确该绿色蠕虫是“费力地从纠缠成团的同伴中分拣出来的（painstakingly separated from its tangle of companions）”，此条为炼金术士交代的补充要求。“get knots out”是标准英语习语，意为“解开打结处 / 把结解开 / 理顺死结”（如理顺打结的绳线或软体）。译文将其增补并理解为“把打结在上面的其他蠕虫统统清理掉”，不仅偏离了“解开打结”的本义，也与前文单条蠕虫已被分离的语境有所脱节。

---

#### entry-01206
- **位置**：`mod-tome.lua:13682`（section: `mod-tome/data/ingredients.lua`）
- **原文**：`Looks much like any other rock, though this one was recently sentient and trying to murder you.`
- **译文**：`它看起来和其他石头没什么两样，只不过这块不久前还具有意识，并且曾试图杀死你。`
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/ingredients.lua` 中 `XORN_FRAGMENT`（索尔石怪碎片）的 `desc` 描述。译文语义完整对应原文，语气幽默自然，标点与句法处理得当，无占位符或控制字符缺失。

---

#### entry-01207
- **位置**：`mod-tome.lua:13690`（section: `mod-tome/data/ingredients.lua`）
- **原文**：`wretchling eyeball`
- **译文**：`小劣魔之眼`
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/ingredients.lua` 中 `WRETCHLING_EYE` 的实体名称。在同文件第 8451 行实体名 `wretchling` 统一译为“小劣魔”，第 11094、13591、13690 行均一致译作“小劣魔之眼”，术语规范且全仓一致。

---

#### entry-01208
- **位置**：`mod-tome.lua:13709`（section: `mod-tome/data/keybinds/tome.lua`）
- **原文**：`Show character sheet (player)`
- **译文**：`显示角色面板（玩家）`
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/keybinds/tome.lua` 中的快捷键动作定义 `SHOW_CHARACTER_SHEET`。译文准确表达为玩家查看自身角色面板，括号使用规范的全角中文括号，与动作功能完全吻合。

---

#### entry-01209
- **位置**：`mod-tome.lua:13710`（section: `mod-tome/data/keybinds/tome.lua`）
- **原文**：`Show character sheet (actor @ cursor)`
- **译文**：`显示角色面板（光标位置的角色）`
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/keybinds/tome.lua` 中的快捷键动作定义 `SHOW_CHARACTER_SHEET_CURSOR`（默认按键为 Ctrl+C，用于查看光标悬停处单位的角色面板）。`actor @ cursor` 译作“光标位置的角色”准确清晰，功能指向明确。

---

#### entry-01210
- **位置**：`mod-tome.lua:13785`（section: `mod-tome/data/lore/age-allure.lua`）
- **原文**：
  ```text
  #{bold}#Hompalan's Log Entry 4#{normal}#
  #{italic}#Age of Allure 4544#{normal}#
  ...
  Test subject A-C: Imploded during transition.
  Test subject D: Exploded during transition.
  ...
  ```
- **译文**：
  ```text
  #{bold}#红帕兰的日志记录四#{normal}#
  #{italic}#厄流纪 4544年#{normal}#
  ...
  实验品 A-C：在传送过程中向内爆裂。
  试验品 D：在传送过程中爆炸。
  ...
  ```
- **复核结论**：**细微观察**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/lore/age-allure.lua` 中 `halfling-research-note-2`。
  1. 专名“Hompalan”统一译作“红帕兰”，“Age of Allure”按术语表译作“厄流纪”，“yeeks”按术语表译作“夺心魔”，格式控制符 `#{bold}#...#{normal}#` 及 `#{italic}#...#{normal}#` 与空行分布完全对齐。
  2. 细微用词观察：在日志记录六的测试列表中，原文全部条目均为 `Test subject`，而译文首项使用了“**实验品** A-C：”，随后的 D 至 N 项以及后文第 133 行、同日志第 116、117 行均写作“**试验品**”，同一列表项首项存在“实验品”与“试验品”的微小不一致。整体情节与语义完整通顺。

---

#### entry-01211
- **位置**：`mod-tome.lua:13840`（section: `mod-tome/data/lore/age-allure.lua`）
- **原文**：
  ```text
  #{bold}#Hompalan's Log Entry 7#{normal}#
  ...
  Test subject X: Returned from second transition missing head. How bizarre.
  ...
  ```
- **译文**：
  ```text
  #{bold}#红帕兰的日志记录七#{normal}#
  ...
  试验品 X：在传送回来时头没了，真古怪。
  ...
  ```
- **复核结论**：**细微观察**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/lore/age-allure.lua` 中 `halfling-research-note-3`。
  1. 格式标签与段落排版完全一致，破折号转换为中文破折号，叙事口吻贴合半身人法师狂妄残忍的性格。
  2. 细微观察：试验品 X 的原句为 `Returned from second transition missing head.`，译文译为“在传送回来时头没了”，漏译了“second（第二次）”。由于前一条 W 是“第一次传送（first transition）”，后一条 Z 是“两次传送（both transitions）”，此处虽按上下文往返流程意译为“传送回来”，但在计数结构上略有省减。

---

#### entry-01212
- **位置**：`mod-tome.lua:13887`（section: `mod-tome/data/lore/age-allure.lua`）
- **原文**：
  ```text
  #{bold}#Hompalan's Log Entry 9#{normal}#
  ...
  I saw him staring for a long time at the farportal earlier...
  ...
  Can they not understand how my genius is disturbed by---
  ```
- **译文**：
  ```text
  #{bold}#红帕兰的日志记录九#{normal}#
  ...
  之前我看见他盯着远行传送门看了很久...
  ...
  他们难道不明白自己如何打扰了我这位天才的——
  ```
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/lore/age-allure.lua` 中 `halfling-research-note-4`。
  1. 术语“farportal”准确译为“远行传送门”，专名“厄流纪”与格式控制符匹配无误。
  2. 日志十一末尾原文 `disturbed by---` 因突发袭击中断，译文“打扰了我这位天才的——”完整保留了被突发事件打断的中断破折号，语气还原到位。
  3. 关于试验品 Z 表现出的时空魔法特性（涉足阴影、主观经历 3 天而客观仅过数秒）等叙述严谨准确。

---

#### entry-01213
- **位置**：`mod-tome.lua:13952`（section: `mod-tome/data/lore/age-allure.lua`）
- **原文**：
  ```text
  Work in a hospital like this is more draining than I thought it'd be...
  ...Ready access to regeneration infusions ensures that... the Overseers have granted us access to their amnesia-inducing spells...
  ...variations on heroism infusions and shielding runes...
  ```
- **译文**：
  ```text
  在这样的医院工作，比我预想的更令人精疲力竭...
  ...随时可用的再生纹身确保...长老会还授予我们使用致人失忆的法术...
  ...由英勇纹身与护盾符文的实验性变体...
  ```
- **复核结论**：**未发现问题**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/lore/age-allure.lua` 中 `conclave-vault-1`（治疗师亚斯特莉的第一篇日志）。
  1. 专名与机制术语：`Conclave` 统一译作“孔克雷夫”，`Overseers` 译作“长老会”，`Higher` 译作“高等人类”，`Nargol` 译作“纳格尔”；铭刻术语 `regeneration infusions`（再生纹身）、`heroism infusions`（英勇纹身）、`shielding runes`（护盾符文）使用准确规范。
  2. 引言双引号转为中文全角引号 `“”`，分段、标点与原文完全对应，医学实验背景与剧情内涵传达准确。

---

#### entry-01214
- **位置**：`mod-tome.lua:14196`（section: `mod-tome/data/lore/angolwen.lua`）
- **原文**：
  ```text
  It were some years now since twain of our brightest students left Angolwen, sullied by our veil of secrecy and our silent duty...
  ...Still I remember mine sister Neira's shortened scream as she stood beside me...
  ...Aye, and humility is what I teach to ye now. Know ye well that there are forces out there which dwarf ye into insignificance...
  ```
- **译文**：
  ```text
  我们最聪慧的两名学生离开安格利文已有数年，他们厌倦了我们隐秘的帷幕和无声的职责...
  ...我仍记得姐姐尼拉站在我身旁时那声截然而止的尖叫...
  ...是的，这就是为何我要让你学习身为法师的谦卑。让你了解在绝对的力量下你是多么的渺小...
  ```
- **复核结论**：**存在疑点**
- **依据说明**：
  查固定版本源码 `game/modules/tome/data/lore/angolwen.lua` 中 `angolwen-linaniil-lecture`（大法师莱娜尼尔关于谦卑的演讲）。
  1. **明确别字**：第 4 段中“mine sister Neira's shortened scream”译作“那声**截然而止**的尖叫”。“截然而止”为常见词语混淆别字，汉语标准成语应为“**戛然而止**”（形容声音猝然停止）。
  2. **细微观察**：
     - 首段“sullied by our veil of secrecy and our silent duty”，原文“sullied”意为蒙受玷污/被玷污，译文意译为“厌倦了……”，尺度偏大。
     - 第 2 段已明确受众为复数的年轻学徒们（“你们——这些刚开始学习我们知识的年轻学徒 / ye, young acolytes”）；而在倒数第二段（第 8 段）“Aye, and humility is what I teach to ye now... dwarf ye into insignificance”，译文转成了单数的“你”（“这就是为何我要让你学习……你是多么的渺小”），前后人称单复数出现不一致。
     - 核心世界观术语“Angolwen”（安格利文）、“Spellblaze”（魔法大爆炸）、“Spellhunt”（魔法狩猎）、“Age of Dusk”（黄昏纪）、“Shaloren”（永恒精灵）均准确一致。