## 40条译文复核判定总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03292 | 未发现问题 | 技能权重乘数设定，语义与对话框逻辑一致 |
| entry-03293 | 未发现问题 | 0与1的技能开关及默认状态说明准确 |
| entry-03294 | 未发现问题 | 格式标记完整，持续技能关闭/重开机制说明准确 |
| entry-03295 | 未发现问题 | 技能专名“奥术格斗”符合术语 |
| entry-03296 | 未发现问题 | 触发与随机施法规则准确，结尾换行一致 |
| entry-03297 | 未发现问题 | 随机可用法术触发机制准确 |
| entry-03298 | 未发现问题 | 已学会的可用法术列表描述准确 |
| entry-03299 | 未发现问题 | 背景介绍专名、阵营与格式标签完整无误 |
| entry-03300 | 存在问题 | C01（“tactically reposition”漏译且“重新占位”存在别字） |
| entry-03301 | 未发现问题 | 烈火纪兽人学习魔法历史叙述准确 |
| entry-03302 | 未发现问题 | 卓越纪兽人灭绝及蛰伏传言描述准确 |
| entry-03303 | 未发现问题 | 炼金术士宝石爆炸及随行傀儡描述准确 |
| entry-03305 | 未发现问题 | 死灵术思想与造物叙述通顺达意 |
| entry-03306 | 未发现问题 | 魔法大爆炸历史叙事准确，上游孤立双引号排版处理得当 |
| entry-03307 | 未发现问题 | 被诅咒者精神力量与仇恨生涯描述准确 |
| entry-03308 | 未发现问题 | 恐惧王座地宫与盘踞黑暗力量描述准确 |
| entry-03309 | 存在问题 | C02（主语限定词Some误作传闻从句“虽然有人说...”导致事实变虚传） |
| entry-03310 | 未发现问题 | 奥术之刃魔武双修与训练描述准确 |
| entry-03311 | 未发现问题 | 巨魔被兽人训练及智力提升描述准确 |
| entry-03312 | 未发现问题 | 半身人之足与打听传闻描述生动准确 |
| entry-03313 | 未发现问题 | 炼金术士装备与首饰镶嵌描述准确 |
| entry-03314 | 未发现问题 | 格斗家双拳运用与战斗力描述准确 |
| entry-03315 | 未发现问题 | 混沌雷电元素与亲和者发狂描述准确 |
| entry-03316 | 未发现问题 | 斗篷保暖与魔法效果描述准确 |
| entry-03317 | 仅建议 | C08（“Sandals or boots”概括为“鞋子”，建议还原为“凉鞋或靴子”） |
| entry-03318 | 未发现问题 | 就绪弹药描述准确 |
| entry-03319 | 未发现问题 | 副武器套主手装备与按键说明准确 |
| entry-03320 | 未发现问题 | 副武器套副手持盾/双持与按键说明准确 |
| entry-03321 | 未发现问题 | 副武器套念动力抓取与按键说明准确 |
| entry-03322 | 未发现问题 | 无影手即时使用物品列表机制说明准确 |
| entry-03323 | 存在问题 | C03（“the Cataclysm”误译为“大爆炸”，混淆大灾变历史事件） |
| entry-03324 | 存在问题 | C04、C05、C06、C07（首句句意颠倒、巨魔高级语言能力漏误译、时间尺度错误、恶魔生理反应机制曲解） |
| entry-03325 | 未发现问题 | 矮人社会公会、材质精工与世界之砧手札叙述准确 |
| entry-03326 | 未发现问题 | 奎科加时空神话、莱娜尼尔大法师手札及格式标签准确 |
| entry-03327 | 待确认 | C09（“Logs written to %s”译为“日志目录”，源码缺失无法核验参数类型） |
| entry-03328 | 待确认 | C10（“Logs written to %s”译为“日志目录”，源码缺失无法核验参数类型） |
| entry-03329 | 未发现问题 | 插件init.lua包含tags表字段与代码示例准确 |
| entry-03330 | 未发现问题 | 上传插件错误提示准确 |
| entry-03331 | 未发现问题 | 插件更新与预览图上传成功提示准确 |
| entry-03332 | 未发现问题 | 插件更新上传成功提示准确 |

---

## 详细观察与 Claim 记录

### C01 | entry-03300 | 存在问题
- **原文引据**：`...giving you the opportunity to tactically reposition or finish them off at less risk.`
- **译文引据**：`...为你制造机会重新占位，或以更低的风险将其解决。`
- **具体问题**：
  1. “占位”（意为占据席位/空间，如占位符）属于“站位”（战斗中的走位/站立位置）的别字与词义错位；
  2. 漏译修饰副词 "tactically"（战术性地 / 战术走位）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/init.lua:87`（`load_tips`）。该提示在加载界面向玩家阐述核心战斗走位机制，同文件 line 88 明确强调战术走位（"seek the position of greatest tactical advantage... 调整你的走位以保持你的优势"），此处“重新占位”用字不当且丢失战术修饰。

---

### C02 | entry-03309 | 存在问题
- **原文引据**：`Some Sher'Tul artifacts can still be found in hidden places, but it is said they are not to be trifled with.`
- **译文引据**：`虽然有人说还能在某些隐秘之地找到夏·图尔的神器，但据说不可轻慢它们。`
- **具体问题**：主干语法与事实定性错误。原文主干为客观陈述事实："Some Sher'Tul artifacts [主语] can still be found in hidden places [谓语/状语]"（某些夏·图尔神器仍可在隐秘之处找到），后半句才引入传闻定性 "but it is said they are not to be trifled with"（但据说不可轻慢它们）。译文将主语限定词 "Some"（某些/部分）误解为 "Some [say]"（有人说），强行增添“虽然有人说...”，将客观事实描述改写为让步传闻从句，且导致前后文出现累赘的传闻表述（“虽然有人说...但据说...”）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/init.lua:102`（`load_tips`）。世界观与探索事实提示。

---

### C03 | entry-03323 | 存在问题
- **原文引据**：`...and are few in number since the Cataclysm tore much of their land into the sea.`
- **译文引据**：`...自从大爆炸将他们大部分土地沉入海洋后，他们的数量急剧减少。`
- **具体问题**：专有名词与世界历史事实混淆。原文为 "since the Cataclysm tore much of their land into the sea"，译文将其中的 "the Cataclysm"（大灾变）误译为“大爆炸”（即 Spellblaze，魔法大爆炸）。在 ToME 历史设定中，"Spellblaze"（魔法大爆炸）与数个世纪后导致大陆东南部崩塌沉海的 "Cataclysm"（大灾变）是两个不同的独立历史大事件（在 `game/modules/tome/init.lua:132` 明确区分：“The effects of the Spellblaze were not all instant, and many centuries later the Cataclysm tore the continent apart once more...”）。将 Cataclysm 译为“大爆炸”严重混淆了游戏核心历史线。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:244`（人类手札 Lore 第三段）。

---

### C04 | entry-03324 | 存在问题
- **原文引据**：`No text would be complete without at least a brief note of some of the more brutish races which infest our world.`
- **译文引据**：`没有任何文字可以诠释那些影响我们世界的野蛮种族。`
- **具体问题**：宏观句意完全颠倒。原文为常见的总述修辞句式“如果不简要记录...任何著述都是不完整的”，旨在表达作者必须在本书中对这些野蛮种族作一番记载；译文误解为“没有任何文字可以诠释...”，将必然加以记录的陈述逆转为不可言说的感叹，语义严重失真；且将 "infest"（侵扰、滋生于）弱化误译为“影响”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第一段）。

---

### C05 | entry-03324 | 存在问题
- **原文引据**：`They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons...`
- **译文引据**：`他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名...`
- **具体问题**：关键叙事机制信息遗漏并错译。原文明确指出森林巨魔相比山地巨魔具有更高级的言语/语言表达形式（"a more advanced form of speech"），随后才说明移动更快（"move faster"）。译文将 "a more advanced form of speech" 错译为“更为敏捷的速度”，不仅彻底丢失了森林巨魔语言能力的叙事设定，还与后半句“以移动迅速...闻名”造成完全重复；此外该段首句“岩石巨魔生存与东北部的山脉地区”中“生存与”存在别字（应为“生存于”）。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第二段）。

---

### C06 | entry-03324 | 存在问题
- **原文引据**：`Records of them exist only from the last few hundred years...`
- **译文引据**：`有关他们的记载只有近一百年的...`
- **具体问题**：时间尺度数量级翻译错误。原文为 "the last few hundred years"（近几百年 / 过去数百年），译文误译为“近一百年”，时间跨度被缩减为一个世纪。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第四段，关于娜迦族的记载历史）。

---

### C07 | entry-03324 | 存在问题
- **原文引据**：`...metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness.`
- **译文引据**：`...金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。`
- **具体问题**：恶魔生理反应机制曲解。原文描述的是恶魔独特的金属血肉在接触埃亚尔大陆大气时产生的奇异反应（"react oddly with our atmosphere"），并主动释放酸液或喷吐黑暗浓雾（"release hideous acids or belching clouds of darkness"）。译文将其曲解为“表现出超乎我们想象的形态”，并将主动释放酸液/浓云篡改为被动掩藏“藏在酸雾里或是可怕的黑暗中”，严重背离原作设定的恶魔生理机制叙事。
- **状态**：存在问题
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:265`（手札 Lore 第五段）。

---

### C08 | entry-03317 | 仅建议
- **原文引据**：`Sandals or boots can be worn on your feet.`
- **译文引据**：`你的脚上可以穿上鞋子。`
- **具体原因**：原文在部位说明中具体列出 "Sandals or boots"（凉鞋或靴子）。译文概括为“鞋子”，虽符合脚部槽位（`FEET`）常理且无游戏机制误导，但若偏好与同组头部部位（line 128 `HEAD` "helmets or crowns" 译为“头盔或王冠”）保持相同细致度，建议还原为“凉鞋或靴子”。此项纯属表述精度偏好，不记作缺陷。
- **状态**：仅建议
- **源码路径与消费逻辑**：`game/modules/tome/load.lua:131`（`ActorInventory:defineInventory("FEET", ...)`）。

---

### C09 | entry-03327 | 待确认
- **原文引据**：`Logs written to %s`
- **译文引据**：`日志目录：%s`
- **具体疑点**：原文 "Logs written to %s" 为被动动作句（日志已写入 %s）。译文处理为偏正名词结构“日志目录：%s”，预设了 `%s` 传入的一定是目录路径。若运行时该格式化占位符传入的是具体日志文件名或文件绝对路径（如 `arrange_text.log`），则显示为“日志目录：.../arrange_text.log”存在属性描述错位。
- **证据缺口**：该条目所属 section 为 `tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua`，对应组件为 `addon-dev`，已明确列于 `source-access.json` 的 `unavailable_components`（源码缺失）。无法通过源码调用链核验 `%s` 实际传入的实参类型（目录还是具体文件）。依规则“缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认”，将此疑点标记为待确认。
- **状态**：待确认
- **源码路径与消费逻辑**：`tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua:28`（`tformat` 消费，组件源码缺失）。

---

### C10 | entry-03328 | 待确认
- **原文引据**：`Logs written to %s`
- **译文引据**：`日志目录：%s`
- **具体疑点**：同 C09。原文 "Logs written to %s" 译为“日志目录：%s”，预设了 `%s` 为目录；若运行时传入具体文件路径则标签不匹配。
- **证据缺口**：组件 `addon-dev` 源码缺失（属于 `unavailable_components`），无法通过源码证实 `%s` 的运行时参数类型，机制依赖疑点标记为待确认。
- **状态**：待确认
- **源码路径与消费逻辑**：`tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua:31`（`tformat` 消费，组件源码缺失）。

---

## 核验路径与环境记录

- **实际读取文件与版本**：
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/INPUT.md`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/entries.json`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/context.lua`
  - `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/source-access.json`
  - `sources/game/modules/tome/dialogs/orders/Talents.lua`（SHA256: `37fe0b54e0a00ed581908006c4a3c0c7c47d4950c33cb882f87be5e19cc9a1c3`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
  - `sources/game/modules/tome/dialogs/shimmer/ShimmerRemoveSustains.lua`（SHA256: `1f79a0d3e6e1acb806c9956a391460371403a0881d2c9481f71cabf9e77425bc`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
  - `sources/game/modules/tome/dialogs/talents/MagicalCombatArcaneCombat.lua`（SHA256: `6f219dc1061d0c88fcb2351d49bf29dc77db2f7b222a2fcd8312a99216381349`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
  - `sources/game/modules/tome/init.lua`（SHA256: `c10ebbd93388864680b10633d6fd310b5427f39d55fb96d7ecfeb42ee04e7264`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
  - `sources/game/modules/tome/load.lua`（SHA256: `e8ed64f78cfab8e5091ca6c6b64fa7dfe759dc1ba7e43c4bd191a329052703eb`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`）
- **额外源码路径与调用链来源**：无。所有本体条目均在 `source-access.json` sections 列明的 sources 单文件中直接覆盖。
- **缺失与无法核验组件**：`addon-dev` 组件在 `source-access.json` 中列为 `unavailable_components`，对应条目 entry-03327 至 entry-03332 缺失源码，机制依赖疑点按规范保留为待确认（C09、C10）。
- **越界与违规自查**：无越界，未读取其他实验目录或历史/外部报告，未修改仓库，未创建子 agent，未声明生产 `DONE_VERIFIED`。
- **临时文件路径**：创建并使用了 `/tmp/abc20-g04-20260923-difnZK`，任务完成后已全量清理删除。
