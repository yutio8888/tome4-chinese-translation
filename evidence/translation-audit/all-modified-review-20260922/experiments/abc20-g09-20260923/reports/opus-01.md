审核完毕，下面是全部 40 条的复核结果。

**范围说明：**
- 这是审核观察，不是生产结论，不声称 DONE_VERIFIED。
- 我没有修改仓库，没有创建临时目录，没有读取其他模型的报告，也没有创建子 agent。
- 所有 DLC 机制结论都来自 cults 快照。该快照的哈希已核对一致，但源码仓库和 commit 未固定。这些结论能否适用于目标版本，仍待确认。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03493 | 待确认 | C01 |
| entry-03494 | 未发现问题 | "reddish"译作「红色」，属合理近似 |
| entry-03495 | 未发现问题 | 符合 radiant horror→光芒恐魔 术语 |
| entry-03496 | 存在问题 | C02、C03 |
| entry-03497 | 存在问题 | C04 |
| entry-03498 | 存在问题 | C05 |
| entry-03499 | 未发现问题 | 与 on_cantakeoff 的 in_combat 分支一致 |
| entry-03500 | 未发现问题 | %s 保留，与 on_wear 的消费一致 |
| entry-03501 | 仅建议 | C06 |
| entry-03502 | 未发现问题 | combat_spellcrit +3 |
| entry-03503 | 未发现问题 | combat_spellresist +10，符合法术豁免术语 |
| entry-03504 | 未发现问题 | incIncStat mag +5，魔力 |
| entry-03505 | 未发现问题 | wil +5，意志 |
| entry-03506 | 未发现问题 | combat_def +10 |
| entry-03507 | 未发现问题 | movement_speed +0.1 |
| entry-03508 | 未发现问题 | dex +5，敏捷 |
| entry-03509 | 未发现问题 | cun +5，灵巧 |
| entry-03510 | 未发现问题 | 两个 %s 的顺序对应 物品名、目标名 |
| entry-03511 | 仅建议 | C07 |
| entry-03512 | 未发现问题 | on_set_complete 的语境一致 |
| entry-03513 | 存在问题 | C08（另有建议 C09） |
| entry-03514 | 仅建议 | C10 |
| entry-03515 | 未发现问题 | %s 对应 施放者、his_her（已本地化）、物品名 |
| entry-03516 | 未发现问题 | 巡逻单位 movement_speed 减半，且永久生效 |
| entry-03517 | 存在问题 | C11–C20（另有建议 C21） |
| entry-03518 | 未发现问题 | 标题与魔法大爆炸术语一致 |
| entry-03519 | 未发现问题 | 符合 infusions→纹身 |
| entry-03520 | 未发现问题 | 符合 Shaloren→永恒精灵 |
| entry-03521 | 未发现问题 | 标题 |
| entry-03522 | 存在问题 | C22–C28（另有建议 C29） |
| entry-03523 | 未发现问题 | 人名与 context 同族条目一致 |
| entry-03524 | 未发现问题 | 埃尔瓦拉与 context 一致 |
| entry-03525 | 未发现问题 | 标题 |
| entry-03526 | 未发现问题 | 标题 |
| entry-03527 | 存在问题 | C30–C39（另有建议 C40、C41） |
| entry-03528 | 未发现问题 | 标题 |
| entry-03529 | 未发现问题 | 标题 |
| entry-03530 | 未发现问题 | 标题 |
| entry-03531 | 存在问题 | C42–C48（另有建议 C49） |
| entry-03532 | 仅建议 | C50 |

---

### C01 | entry-03493 | 待确认
- 原文 "defence cell of **the Maggot**"，译文「巨大蛆虫的防御细胞」。
- 原文大写并加定冠词，指某个特定存在；译文加了原文没有的「巨大」，把它处理成描述性名词。
- 本条 section 文件（corrupted_blobs.lua:58）里没有任何代码说明 the Maggot 指哪个区域或实体。沿调用链也找不到加载这个 npc 文件的区域文件，所以无法判断「巨大」是否有依据，也无法判断是否该与某个既定专名对齐。
- 缺的证据：定义 the Maggot 的区域或实体源码及其既定译名。

### C02 | entry-03496 | 存在问题
- "pulsing with **nether** energies" 被译作「虚空能量」。
- 同一 section 的相邻条目中，nethergate 译「彼世之门」，"portal of nether energies" 译「彼世能量」。术语 nether→彼世，void→虚空，两者是不同的词。
- 这个实体本身的伤害类型就是 `DamageType.VOID`（horror.lua:131 之后的 combat 字段）。把 nether 译成「虚空」会让玩家混淆这两个概念，属于术语和语义错误。

### C03 | entry-03496 | 存在问题
- "A **strange** tall crystal **pulsing** with…" 被译作「一团**发射出**…的高大水晶」。
- "strange"被删掉了。"pulsing"（有节律地搏动、涌动）被改成「发射」（向外射出），描写信息出错。
- 影响较低，但信息确实丢失或被改写。

### C04 | entry-03497 | 存在问题
- "**roughly** warped into the form of a ring" 被译作「弯曲成了指环的形状」。
- "roughly"（粗略地、勉强地）被删，原文说的「形状只是大致像指环」变成了「完全是指环形状」。影响较低。

### C05 | entry-03498 | 存在问题
- "When first worn **the ring attunes to you**, letting you choose…" 被译作「当你第一次戴上戒指的时候，选择一个觉醒技能」。
- 「指环与你相合」这一句被整句删掉。机制部分我核对过，译文是正确的：
  - 选择通过 RingOfTheHunter 对话写入 `prodigy_granted`。
  - 效果通过 `wielder.learn_talent` 实现，只在佩戴时生效。
  - 未选择时 `prodigy_granted` 为 nil，重新佩戴会再次弹出对话（world-artifacts.lua 的 on_wear；RingOfTheHunter.lua 的 `unload`）。
- 这里的缺陷只是叙事从句丢失，影响较低。

### C06 | entry-03501 | 仅建议
- "willing **and able** to talk" 只译出了「愿意」，但「愿意交谈」已经隐含「能交谈」，没有实质信息损失，属于措辞偏好。

### C07 | entry-03511 | 仅建议
- "increasing in power" 被译作「解放了强大的力量」。按 on_wear，剑获得 dam +12 等加成，即「剑变强」。「解放力量」表达的意思大体相近，只是措辞偏好。

### C08 | entry-03513 | 存在问题
- 原文 "you somehow do not like the idea of having so many parasitic creatures so close…" 是克制的轻描淡写。
- 译文「……实在是太恶心了」改变了说话人的态度强度，删掉了 "somehow"（说不清为什么），还加入了原文没有的「恶心」判断，属于语义改写。

### C09 | entry-03513 | 仅建议
- 「上面的小蠕虫有时会从上面跳出来」重复了「上面」，只是行文问题，不丢信息。

### C10 | entry-03514 | 仅建议
- "two pair of shoes" 被译作「两件鞋子」。量词别扭，但两件物品的含义还在，属于措辞问题。

### C11 | entry-03517 | 存在问题
- 原文 "such a **concentration** of these energies simply couldn't exist on Eyal"，译文「这些能量根本不可能存在于埃亚尔集中出现」。
- 这句话两个结构混在一起，语法不通，读者容易理解成「这种能量在埃亚尔根本不可能存在」。这与前文德瑞姆熟悉这种能量的说法矛盾。原文说的是「如此高的浓度」不可能存在。
- 源码位置：dremwarves.lua:52 起的 lore。

### C12 | entry-03517 | 存在问题
- "wide enough for **one of our party** to fit in with room to spare" 被译作「足够让我们的**一个小队**在里面行走」。
- 原文说的是队伍中的一个人，译文变成了一整支小队，数量和规模都错了（dremwarves.lua:58）。

### C13 | entry-03517 | 存在问题
- "**I imagine** the … teeth **aren't entirely natural either**" 被译作「显得十分不自然」。
- 推测语气「我猜」被删，程度也从「并不完全天然」变成了「十分不自然」。这属于删除限定词，把推测说成了断言（dremwarves.lua:60）。

### C14 | entry-03517 | 存在问题
- "There was **obviously a source** of these things" 被译作「显然，**这里就是**这些怪物的来源」。
- 原文只是推断「必然有一个源头」，后文才说 "We found the source"。译文提前断言「这里就是来源」，造成时序和逻辑错误（dremwarves.lua:62）。

### C15 | entry-03517 | 存在问题
- "Some great machine" 被译作「一些巨大的机器」。原文是单数，并且后文强调 "that was only one machine"。
- 同段的 "judging by the black growth which engulfs **the machine in this room**" 也被译成「这些机器」（复数）。数量错误。

### C16 | entry-03517 | 存在问题
- "**I am not the only one** who has been infected" 被译作「**其他人也都**感染了」。
- 原文说「不止我一人感染」，译文变成了「其他人全部感染」，范围被夸大。

### C17 | entry-03517 | 存在问题
- "But, **I am content** with this fate" 被译作「但是，**我们**…却只感到充实和满足」。
- 原文只有说话人自己「坦然接受」，译文把这种感受套到了所有人身上，主语范围错了，还加了「充实」。

### C18 | entry-03517 | 存在问题
- "We wandered into **the back of the room**" 被译作「我们徘徊到那些还有更多管子的**房间**里面」。
- 原文是「同一房间的后部」，译文变成了「其他房间」，地点关系错误。影响较低。

### C19 | entry-03517 | 存在问题
- "**Feral** Drem must have emerged from this egg" 被译作「**原生的**德瑞姆」。
- feral 的意思是野生、未开化，不是「原生」，语义错误（dremwarves.lua:72）。
- 术语子集里没有这个词条，这里只按语义判断，不涉及专名统一。

### C20 | entry-03517 | 存在问题
- "**judging by** the black **growth** which engulfs the machine" 被译作「**正如**我们…看到的，吞噬着这些机器的黑色**怪物一样**」。
- 这里有两处错误：
  - "judging by"（依据什么推断）被改成了「正如……一样」（类比），证据关系变了。
  - "growth"（增生物，前文译作「恶性的生长物」）被错译成「怪物」，与前文不一致，也改变了事实。

### C21 | entry-03517 | 仅建议
- 译文新增了「考虑到它卓越的防御力」和「本能地」。"tore into them"（猛扑上去）被译作「撕成了碎片」。
- 这些都是补足语气或推理，与后文不矛盾，属于偏好层面的增译，列出来供参考。

### C22 | entry-03522 | 存在问题
- "they would rather **tempt fate**" 被译作「宁愿**接受命运**」。
- tempt fate 的意思是冒险、玩命，译文意思接近相反（fay-willows.lua:113）。

### C23 | entry-03522 | 存在问题
- "Well, **I should say** to the shalore it may have been basic food and drink" 被译作「好吧，**我应该对永恒精灵说**，这可能对它们来说是……」。
- 原文是「我得更正一下：对永恒精灵来说那也许只是基本饮食」。译文误读成「我应该对永恒精灵说」，把一个自我更正变成了对永恒精灵说话，语义错误。

### C24 | entry-03522 | 存在问题
- "The scarce few that were still alive after **had traveled back** to Elvala" 被译作「**准备返回**埃尔瓦拉」。
- 原文是已经抵达，译文变成了还在准备，时序错误，也与下一句「只有几百人设法活着回来」冲突。

### C25 | entry-03522 | 存在问题
- "there would have been no need to move northwards **around** this area" 被译作「在这个地区向北移动」。
- 原文是向北「绕行」避开平原，译文丢了绕行，变成在区域内向北走，空间关系错误。影响较低。

### C26 | entry-03522 | 存在问题
- "Turning to see … I noticed the huge **gashes** through the **blackened** armor" 被译作「黑色盔甲上有**一道**巨大的伤口」。
- 原文的伤口是复数，被译成「一道」。"blackened"（烧焦、熏黑）被译成「黑色」，丢失了盔甲曾被烧过的信息。影响较低。

### C27 | entry-03522 | 存在问题
- "When **their numbers** began to reach more manageable amounts" 被译作「当**痊愈士兵**的数量开始达到一定程度时」。
- 原文指伤兵人数减少到可以应付的程度，译文变成痊愈士兵增加，对象和趋势都反了。

### C28 | entry-03522 | 存在问题
- "I **noted** that I had been fulfilling my end of the bargain. Nodding to this the chief healer **looked behind me** as a soldier approached" 被译作「意识到……主治医师向我点头，**看着我**，回答说」。
- 这里有两处错误：
  - "noted" 在这里是「我（向对方）提出」，译成「意识到」后变成心理活动，导致治疗师「点头回答」没有了对象。
  - "looked behind me" 被错译成「看着我」，丢了治疗师看向身后走来士兵这一动作。

### C29 | entry-03522 | 仅建议
- 「我甚至从来没有听说过符文的，甚至不知道……」句子残缺，但意思可以理解，属于二级语法问题，列作建议。

### C30 | entry-03527 | 存在问题
- "I believe he **may have been** a member" 被译作「我**极大程度上**相信他还是……成员」。
- 原文的推测语气被反转成强烈确信，删除了限定词（fay-willows.lua:216 起）。

### C31 | entry-03527 | 存在问题
- "it was quite a surprise to see **them out here**" 被译作「看到他们**这样做**，我有点惊讶」。
- 原文惊讶的是矮人「出现在这里」，下一句才会接着问矮人在铁王座以外有没有家园。译文把惊讶的对象改成了「纳格尔人这样做」，逻辑链断了。

### C32 | entry-03527 | 存在问题
- "Hard to really know **with how secretive** the dwarves are" 被译作「要想真正了解矮人们的**隐秘程度**是很难的」。
- 原文是「矮人这么隐秘，所以很难得知（他们是否另有家园）」，译文变成「很难了解矮人有多隐秘」，意思错了。

### C33 | entry-03527 | 存在问题
- "**You wouldn't happen to know** anything regarding items … the guards at the city gates would confiscate **would you?**" 被译作「**你可能还不知道**，士兵会没收矮人们携带的物品，知道吗？」。
- 原文是向信使打听消息，译文变成主角告诉信使，言语行为反了。信使接下来的解释因此失去了上下文。

### C34 | entry-03527 | 存在问题
- 译文漏掉了整句 "They say that it's too dangerous for civilians to carry such items."。
- 下一句 "Personally I say it is too dangerous for **anyone** … them included" 是在反驳这一句。缺了它，「包括他们自己」的对比就说不通了。

### C35 | entry-03527 | 存在问题
- "a table with **a couple of halflings**" 被译作「一对半身人**夫妇**」，后文又重复了一次。
- 原文只是两三个半身人，没有说是夫妻，译文新增了一段不存在的关系。

### C36 | entry-03527 | 存在问题
- "You wouldn't happen to have any **plans to deal with** the Shaloren?" 被译作「你对永恒精灵有什么**想法**？」。
- 原文是主角有意试探对方有没有行动计划，所以才会有下文「看看他知道多少」和对方姿态骤变。译文变成询问看法，试探的意图丢失了。

### C37 | entry-03527 | 存在问题
- "on Maj'Eyal" 被译作「马基埃亚尔」。
- 术语快照中 Maj'Eyal 的 source_tag 为 `_t`，状态 preferred，规定用「马基·埃亚尔」，并注明「马基埃亚尔」已被取代。本条 source_tag 同为 `_t`，属于叙事中的地名，术语明确适用。

### C38 | entry-03527 | 存在问题
- "Spellblaze, is that what **they** call it?" 被译作「**你们**把那个叫做魔法大爆炸？」。
- 原文问的是「他们」（第三方）这样称呼，信使的回答 "or so I have been told" 正好对应。改成「你们」后，问答对不上了。

### C39 | entry-03527 | 存在问题
- "and **possibly** ones that required secrecy" 被译作「他们进行的计划还需要保密」。
- "possibly" 被删，推测变成了断言，属于删除限定词。

### C40 | entry-03527 | 仅建议
- "the **blasted** mages caused their home to collapse in on them" 被译作「法师制造的爆炸摧毁了他们的家园」。
- "blasted" 在这里是咒骂语（该死的），被当成了「爆炸」。但「魔法大爆炸导致坍塌」在剧情上大致成立，主要损失是咒骂语气，所以列作建议。

### C41 | entry-03527 | 仅建议
- 「我突然**会**想起」应为「回想起」，这是错字。
- 「**今早**进城的时候」是增译。fay-willows.lua 第 192 行起的上一章没有明确说是当天早上，但也不矛盾。

### C42 | entry-03531 | 存在问题
- "become **enthralled** to the slavers will and made to do their bidding **unquestioningly**" 被译作「被奴役者的意志所**吸引**，**毫无疑问地**服从他们的命令」。
- 这里有两处错误：
  - enthralled 是「被奴役、被控制」，不是「被吸引」。
  - unquestioningly 是「不加质疑地」。「毫无疑问地」在中文里的常见意思是「无可怀疑地」，属于假朋友错译。
- 术语快照中 slaver→奴隶贩子 的注明适用范围是「鲜血之环语境」，本条讲的是灵能奴役者，这条术语不适用，所以这里不按术语算缺陷。

### C43 | entry-03531 | 存在问题
- "look up at who had **thrown** me" 以及后文 "why have you **thrown** me in here" 都被译成了「**拉**」。
- 上一章结尾写的是 "a hand reached out of its opening, **throwing** me inside"（fay-willows.lua 约第 285 行），被扔进来的动作与译文不符。

### C44 | entry-03531 | 存在问题
- "I had **thought better of you** since you killed that Eldoral halfling" 被译作「我就更**想念**你了」。
- 原文是「（因此）对你评价更高」，译文变成了「想念」，意思错误（fay-willows.lua:295）。

### C45 | entry-03531 | 存在问题
- "leaving a **faceless** humanoid" 被译作「留下了一个**面目全非**的人形」。
- faceless 是「没有面孔」，面目全非是「毁得认不出来」，事实错误（fay-willows.lua:299）。

### C46 | entry-03531 | 存在问题
- "the same human **who had briefly visited the messenger** when I was talking to him in the inn" 被译作「这就是**我**在客栈和信使谈话时**短暂拜访过**的那个人」。
- 原文是斗篷人拜访信使，译文变成了「我拜访过他」，动作主体错了。

### C47 | entry-03531 | 存在问题
- "likely the same one that had been **standing with** the human in the crowd" 被译作「和那个人类站在一起**蛊惑群众**的那个半身人」。
- 原文只说这个半身人与那人一同站在人群中。译文新增了「蛊惑群众」，给半身人加了原文没有的行为，而且这个半身人随后救了主角。

### C48 | entry-03531 | 存在问题
- "it would take me **a moment** to realize" 被译作「困惑**许久**」。
- 片刻被译成了很久，时长信息相反。影响较低。

### C49 | entry-03531 | 仅建议
- "Enough pain has been felt already without adding to it-" 被译作「**他们**已经感觉到了足够的痛苦……了。」
- 原文的破折号表示话被砸头打断，译文用句号收尾，打断感没了。「他们」是按语境补出的主语。整体属于表达层面的问题。

### C50 | entry-03532 | 仅建议
- 标题 "Spared" 被译作「死里逃生」。原文强调「被人饶过」，这层意思在译文里弱化了，但大意相符，属于措辞偏好。

---

## 实际读取路径与越界说明

**冻结输入**（位于 `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/`）：
- `INPUT.md`（全文）
- `entries.json`：只看了结构和第一条记录
- `context.lua`：读了第 1–240 行，并在全文里检索了人名和译名计数
- `source-access.json`

**section 源码**（`sources/dlc/cults/tome-cults/data/`）：
- 以下 6 个文件的 sha256 都与 `files_sha256` 一致：`general/npcs/corrupted_blobs.lua`、`general/npcs/horror.lua`、`general/objects/world-artifacts.lua`、`glyph_sequences/cults.lua`、`lore/dremwarves.lua`、`lore/fay-willows.lua`。
- 都属于 DLC cults，来源未固定（unpinned）。

**额外 DLC 文件**：
- `…/experiments/abc20-20260923/sources/cults/tome-cults/overload/mod/dialogs/RingOfTheHunter.lua`
- 这个文件在 `dlc_additional_sources` 清单内，哈希 2894023d… 与清单一致。
- 引入原因：world-artifacts.lua 的 Writhing Ring `on_wear` 中调用了 `require("mod.dialogs.RingOfTheHunter")`，用于核实 C05 的机制。

**引擎文件**（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63，均通过 `git show` 单文件读取）：
- 引入原因：world-artifacts.lua:1029 调用了 `who:his_her()`。
- 为定位它的定义，我依次查看了三个候选单文件：
  - `game/modules/tome/class/Actor.lua`：没有定义
  - `game/engines/default/engine/Entity.lua`：没有定义
  - `game/engines/default/engine/Actor.lua`：第 607 行转调 `string.his_her`
- 随后读取 `game/engines/default/engine/utils.lua:939`，确认它返回 `_t"his"/"her"/"its"`。
- 需要说明：前两个文件是为寻找定义而查看的候选文件，不是调用链直接指向的文件。这属于在定位过程中多查看了单文件，我没有做整目录搜索。

**其他说明：**
- 工具输出过长时，harness 会自动把输出转存到 `~/.claude/projects/.../tool-results/` 下（INPUT.md 和 source-access.json 的查看结果）。这些是会话自己的输出副本，不是别人的材料。
- 我没有创建临时目录。
- 没有读取当前翻译文件、SPEC/STATE、其他报告或 locales。
- 仓库 `git status` 与会话开始时相同。

**无法核实的内容：**
- C01 中 the Maggot 指哪个实体：没有允许读取的调用链来源。
- 所有 DLC 机制结论都只在未固定的快照内成立，能否适用于目标版本仍待确认。
