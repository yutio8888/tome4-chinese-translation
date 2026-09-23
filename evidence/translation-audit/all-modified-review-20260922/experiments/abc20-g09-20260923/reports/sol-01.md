已独立复核冻结输入中的 40 条。下表按原顺序列出判定；本结果是审核观察，不是生产 `DONE_VERIFIED`。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03493 | 未发现问题 | 语义相符 |
| entry-03494 | 未发现问题 | 语义相符 |
| entry-03495 | 未发现问题 | 专名与语义相符 |
| entry-03496 | 未发现问题 | 语义相符 |
| entry-03497 | 未发现问题 | 语义相符 |
| entry-03498 | 存在问题 | C01：遗漏指环与佩戴者调谐 |
| entry-03499 | 未发现问题 | 战斗中无法摘下的条件相符 |
| entry-03500 | 未发现问题 | 参数与语义相符 |
| entry-03501 | 未发现问题 | 操作提示相符 |
| entry-03502 | 未发现问题 | 属性与数值相符 |
| entry-03503 | 未发现问题 | 属性与数值相符 |
| entry-03504 | 未发现问题 | 属性与数值相符 |
| entry-03505 | 未发现问题 | 属性与数值相符 |
| entry-03506 | 未发现问题 | 属性与数值相符 |
| entry-03507 | 未发现问题 | 属性与数值相符 |
| entry-03508 | 未发现问题 | 属性与数值相符 |
| entry-03509 | 未发现问题 | 属性与数值相符 |
| entry-03510 | 未发现问题 | 参数顺序与动作相符 |
| entry-03511 | 未发现问题 | 装备共鸣与力量提升相符 |
| entry-03512 | 未发现问题 | 成套触发语义相符 |
| entry-03513 | 未发现问题 | 描述信息相符 |
| entry-03514 | 未发现问题 | 两件鞋类物品组合的语境相符 |
| entry-03515 | 未发现问题 | 三个参数的位置保留 |
| entry-03516 | 未发现问题 | 永久减慢巡逻队的说明相符 |
| entry-03517 | 存在问题 | C02–C07：人数、机器数量、生物阶段、动作及感染范围等 |
| entry-03518 | 未发现问题 | 标题相符 |
| entry-03519 | 未发现问题 | 标题相符 |
| entry-03520 | 未发现问题 | 标题相符 |
| entry-03521 | 未发现问题 | 标题相符 |
| entry-03522 | 存在问题 | C08–C10：纹身用途、人数变化及视线方向 |
| entry-03523 | 未发现问题 | 标题相符 |
| entry-03524 | 未发现问题 | 标题相符 |
| entry-03525 | 未发现问题 | 标题相符 |
| entry-03526 | 未发现问题 | 标题相符 |
| entry-03527 | 存在问题 | C11–C17：所指对象、事件、问句、人物关系及专名 |
| entry-03528 | 未发现问题 | 标题相符 |
| entry-03529 | 未发现问题 | 标题相符 |
| entry-03530 | 未发现问题 | 标题相符 |
| entry-03531 | 存在问题 | C18–C23：幻象身份、支配、动作及人物关系 |
| entry-03532 | 存在问题 | C24：「获饶恕」变为「逃生」 |

以下源码路径均相对于本组 `sources/dlc/cults/tome-cults/data/`。

### C01 | entry-03498 | 存在问题

原文“the ring attunes to you”在译文中消失；译文只说首次佩戴时选择觉醒技能。调谐关系是原说明的一项独立信息。证据：`general/objects/world-artifacts.lua:104`。

### C02 | entry-03517 | 存在问题

原文玻璃管宽到“one of our party”可进入且仍有余地；译文称“足够让我们的一个小队在里面行走”，把一名队员扩大为整支小队。证据：`lore/dremwarves.lua:58`。

### C03 | entry-03517 | 存在问题

原文在该房间发现的是“Some great machine”这一台机器，后文才说明不止这一台；译文在发现时写成“一些巨大的机器”，改变了现场数量。证据：`lore/dremwarves.lua:62,66`。

### C04 | entry-03517 | 存在问题

原文断液后爬出的是“feeble and half formed fetuses”；译文称“虚弱的、不成型的生命体”，遗漏“胎儿”这一与起源揭示有关的生长阶段。证据：`lore/dremwarves.lua:64`。

### C05 | entry-03517 | 存在问题

原文生物“latched onto my arm”，译文确定为“在我的手臂上咬了一口”。原文只证实攀附、扣住手臂，未说明咬伤。证据：`lore/dremwarves.lua:66`。

### C06 | entry-03517 | 存在问题

原文“I am not the only one”表示除叙述者外还有感染者；译文“其他人也都感染了”扩大为其余所有人。证据：`lore/dremwarves.lua:68`。

### C07 | entry-03517 | 存在问题

原文吞没机器的是“black growth”，译文称“黑色怪物”，把增生物确定为怪物。证据：`lore/dremwarves.lua:72`。

### C08 | entry-03522 | 存在问题

原文说明延后使用纹身会使患者日后用得更多，因为除了修复身体，还得用纹身抵御开放伤口的感染。译文虽保留“更多地使用”，随后只说不及时修补会感染，遗漏额外使用纹身来抵御感染的因果环节。证据：`lore/fay-willows.lua:113`。

### C09 | entry-03522 | 存在问题

原文逐渐减少的是“wounded soldiers”的人数；译文称“痊愈士兵的数量开始达到一定程度”，把正在减少的伤员换成了康复者。证据：`lore/fay-willows.lua:131`。

### C10 | entry-03522 | 存在问题

一名士兵走近时，原文主治医师“looked behind me”；译文写“看着我”，改变了视线所指。证据：`lore/fay-willows.lua:131`。

### C11 | entry-03527 | 存在问题

信使说“quite a surprise to see them out here”，惊讶的是在此地看到矮人；译文“看到他们这样做，我有点惊讶”指向纳格尔人筹措食物和酒，所指对象错误。证据：`lore/fay-willows.lua:218`。

### C12 | entry-03527 | 存在问题

原文说法师使矮人的住处坍塌；译文写成“法师制造的爆炸摧毁了他们的家园”，新增了原句没有说明的爆炸。证据：`lore/fay-willows.lua:220`。

### C13 | entry-03527 | 存在问题

原文询问信使是否知道守门卫兵会没收矮人的**什么物品**；译文变成告知信使“士兵会没收矮人们携带的物品”，丢失对物品种类的询问。证据：`lore/fay-willows.lua:222`。

### C14 | entry-03527 | 存在问题

原文另有纳格尔人的公开理由：“平民携带这类物品太危险”；译文从没收魔法物品直接转到信使自己的看法，遗漏了官方理由，也削弱了随后“任何人携带都危险”的对照。证据：`lore/fay-willows.lua:224`。

### C15 | entry-03527 | 存在问题

原文“a couple of halflings”在此只说明两名半身人；译文两次确定为“半身人夫妇”，新增了婚姻关系。证据：`lore/fay-willows.lua:226`。

### C16 | entry-03527 | 存在问题

叙述者原问信使是否有“plans to deal with the Shaloren”；译文问“你对永恒精灵有什么想法”，把行动计划改为一般看法。证据：`lore/fay-willows.lua:228`。

### C17 | entry-03527 | 存在问题

原文 `Maj'Eyal` 译为“马基埃亚尔”，与本包适用术语快照中 `_t`、`T.PN.WORLD` 的首选译名“马基·埃亚尔”不符。证据：`lore/fay-willows.lua:228`及 `INPUT.md` 术语子集。

### C18 | entry-03531 | 存在问题

原文说帐篷里所见之事可能是灵能奴役者**造成的结果**；译文“我在帐篷里看到的可能是一个灵能奴役者”把所见对象直接认定为奴役者。证据：`lore/fay-willows.lua:289`。

### C19 | entry-03531 | 存在问题

原文“become enthralled to the slavers will”指意志受到支配；译文“被奴役者的意志所吸引”变成吸引，失去控制关系。证据：`lore/fay-willows.lua:289`。

### C20 | entry-03531 | 存在问题

叙述者起身想看“who had thrown me”；译文写“是谁在拉我”，把扔进帐篷的动作改成拉。证据：`lore/fay-willows.lua:291`。

### C21 | entry-03531 | 存在问题

信使原话“I had thought better of you since you killed that Eldoral halfling”是曾因此对她评价更高；译文“我就更想念你了”改变了态度含义。证据：`lore/fay-willows.lua:295`。

### C22 | entry-03531 | 存在问题

幻象露出的是“faceless humanoid”，即没有脸的人形；译文“面目全非的人形”表示面容变得难以辨认，丢失“无脸”特征。证据：`lore/fay-willows.lua:299`。

### C23 | entry-03531 | 存在问题

原文披斗篷的人曾短暂拜访信使；译文“我在客栈和信使谈话时短暂拜访过的那个人”改成叙述者拜访披斗篷者，颠倒了动作主体。证据：`lore/fay-willows.lua:301`。

### C24 | entry-03532 | 存在问题

标题“Spared”对应紧接着的正文“spare her”，指半身人决定饶她一命；“死里逃生”只表达幸存，遗漏了他人放过她的关系。证据：`lore/fay-willows.lua:311,314`。

**读取范围与版本。** 实际读取了指定的 `INPUT.md`、同目录的 `entries.json`、`context.lua`、`source-access.json`，以及清单中本组的六个单文件：`corrupted_blobs.lua`、`horror.lua`、`world-artifacts.lua`、`cults.lua`、`dremwarves.lua`、`fay-willows.lua`（完整相对路径见 `source-access.json` 的 `sections`）。六个源码文件的 SHA-256 均与清单相符。未追读额外源码；本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 未用于推断 DLC 行为。DLC 快照的源码仓库及 commit 未固定；上述结论针对冻结原文、译文及该哈希快照，不据此断言其他目标版本的机制适用性。未创建临时文件，未读取其他报告，未发现越界读取。
