| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03493 | 未发现问题 | 保留绿色黏液、防御细胞及所属关系 |
| entry-03494 | 未发现问题 | 接近、分散注意力及同时攻击的关系一致 |
| entry-03495 | 未发现问题 | 保留反讽与光芒恐魔的比较对象 |
| entry-03496 | 存在问题 | C01 |
| entry-03497 | 存在问题 | C02 |
| entry-03498 | 存在问题 | C03 |
| entry-03499 | 未发现问题 | 战斗中无法卸下的提示一致 |
| entry-03500 | 未发现问题 | 共鸣对象与物品名称参数一致 |
| entry-03501 | 未发现问题 | 保留交谈意愿及操作提示 |
| entry-03502 | 未发现问题 | 法术暴击率及数值一致 |
| entry-03503 | 未发现问题 | 法术豁免及数值一致 |
| entry-03504 | 未发现问题 | 魔力属性及数值一致 |
| entry-03505 | 未发现问题 | 意志属性及数值一致 |
| entry-03506 | 未发现问题 | 闪避属性及数值一致 |
| entry-03507 | 未发现问题 | 移动速度及百分比一致 |
| entry-03508 | 未发现问题 | 敏捷属性及数值一致 |
| entry-03509 | 未发现问题 | 心智主题、灵巧属性及数值一致 |
| entry-03510 | 未发现问题 | 触手动作、物品及目标参数对应 |
| entry-03511 | 未发现问题 | 剑与克罗格身体共鸣、增强力量的意思保留 |
| entry-03512 | 未发现问题 | 双武器重聚与力量增强的关系一致 |
| entry-03513 | 未发现问题 | 长袍蠕动、蠕虫缓冲攻击与厌恶感保留 |
| entry-03514 | 仅建议 | C04 |
| entry-03515 | 未发现问题 | 三个参数依次对应行动者、所属代词、物品 |
| entry-03516 | 未发现问题 | 瞬间感受与巡逻队永久减速未混淆 |
| entry-03517 | 存在问题 | C05–C13 |
| entry-03518 | 未发现问题 | 卷章编号及事件主题一致 |
| entry-03519 | 未发现问题 | 标题符合正文对纹身的排斥语境 |
| entry-03520 | 未发现问题 | 永恒精灵受苦的主题一致 |
| entry-03521 | 未发现问题 | 医疗主题一致 |
| entry-03522 | 存在问题 | C14–C20 |
| entry-03523 | 未发现问题 | 人物身份、姓名及卷章编号一致 |
| entry-03524 | 未发现问题 | 离开地点及卷章编号一致 |
| entry-03525 | 未发现问题 | 城门场景及卷章编号一致 |
| entry-03526 | 未发现问题 | 交换情报的主题一致 |
| entry-03527 | 存在问题 | C21–C28 |
| entry-03528 | 未发现问题 | 保留燃烧与疯狂的标题意象 |
| entry-03529 | 未发现问题 | 暴行及贬斥意味一致 |
| entry-03530 | 未发现问题 | 灵能欺骗的主题一致 |
| entry-03531 | 存在问题 | C29–C35 |
| entry-03532 | 未发现问题 | 结合后文，标题表达获免一死的结果 |

以下源码短路径均对应文末列出的实际读取路径。全部问题观察属于文本或语境可直接核对的偏差；不依赖将 DLC 快照认定为某个目标发行版本。

### C01 | entry-03496 | 存在问题

原文“crystal pusling with nether energies”，译文“发射出虚空能量的高大水晶”。原文虽将 *pulsing* 拼错，但描述的是能量脉动；译文改成向外发射，丢失脉动这一动态特征。状态：confirmed。证据：`horror.lua:131` 的实体描述。此项不依据 `nether` 的 existing 术语要求改名。

### C02 | entry-03497 | 存在问题

原文“a writhing mass of tentacles”，译文“大量扭曲的触须弯曲成了指环的形状”。原文说明触须正在蠕动扭动，译文仅呈现扭曲、弯成指环的形态，遗漏持续运动的特征。状态：confirmed。证据：`world-artifacts.lua:99`。

### C03 | entry-03498 | 存在问题

原文“the ring attunes to you”，译文直接进入“选择一个觉醒技能”。首次佩戴时戒指与佩戴者产生协调、共鸣的叙事信息被省略。状态：confirmed。证据：`world-artifacts.lua:104`。选择、不可更换和初次拒选后重新佩戴的说明仍然保留，本项不指控这些机制错误。

### C04 | entry-03514 | 仅建议

原文“the two pair of shoes”，译文“这两件鞋子”。“件”作为鞋类量词不够自然，但此处也可以指两件鞋类装备；快照中确实是两个装备对象参与合并，不能据此断定数量被改成两只鞋。仅属措辞建议。证据：`world-artifacts.lua:938`、`:971–994`，合并逻辑查找并移除另一件鞋类装备，再转换当前物品。

### C05 | entry-03517 | 存在问题

原文“one of our party … with room to spare”，译文“足够让我们的一个小队在里面行走”。可容纳一名队员且有余量，被扩大成可供一个小队行走。状态：confirmed。证据：`dremwarves.lua:58`。

### C06 | entry-03517 | 存在问题

原文“Some great machine”，译文“那是一些巨大的机器”。这里是一台连接多根玻璃管的机器；`:66` 又明确说明他们破坏的只是其中一台。译文将眼前机器改成复数。状态：confirmed。证据：`dremwarves.lua:62`、`:66`。

### C07 | entry-03517 | 存在问题

原文“feeble and half formed fetuses”，译文“虚弱的、不成型的生命体”。“胎儿”这一发育阶段信息被泛化掉，而它直接参与后文对制造过程和族群起源的推断。状态：confirmed。证据：`dremwarves.lua:64`、`:72`。

### C08 | entry-03517 | 存在问题

原文“my flesh wither away and turned into dried leather”，译文“我的肌肉萎缩，看起来如同晒干的皮革”。原文的肉体枯萎、皮革化被缩窄成肌肉萎缩，改变疾病表现的对象。状态：confirmed。证据：`dremwarves.lua:66`。

### C09 | entry-03517 | 存在问题

原文“I am not the only one … infected”，译文“其他人也都感染了”。原文仅确认还有其他感染者，译文增加全员感染的范围。状态：confirmed。证据：`dremwarves.lua:68`。

### C10 | entry-03517 | 存在问题

原文“I am content with this fate”，译文“我们……却只感到充实和满足”。叙述者个人对死亡的接受，被扩展为整个队伍的共同态度。状态：confirmed。证据：`dremwarves.lua:68`。

### C11 | entry-03517 | 存在问题

原文“into the back of the room”，译文“到那些还有更多管子的房间里面”。他们是在已经封闭的同一房间内走向后部，译文变成进入其他房间，丢失并改变空间关系。状态：confirmed。证据：`dremwarves.lua:66`、`:70`。

### C12 | entry-03517 | 存在问题

原文“Feral Drem”，译文“原生的德瑞姆”。*Feral* 描述野生、未驯化的状态，不表示“原生”的起源身份。状态：confirmed。证据：`dremwarves.lua:72`。

### C13 | entry-03517 | 存在问题

原文“further disrepair and corruption … black growth which engulfs the machine”，译文归因为“年久失修而进一步退化”，并将附着物写成“吞噬着这些机器的黑色怪物”。译文遗漏腐化因素，并把包覆机器的黑色增生物改成了怪物，改变这段起源推断的证据及因果。状态：confirmed。证据：`dremwarves.lua:62`、`:72`；前文已将同类对象描述为附着的恶性增生物。

### C14 | entry-03522 | 存在问题

原文“rather tempt fate”，译文“宁愿接受命运”。原文强调冒险、拿性命碰运气，译文变成接受命运，改变拒绝治疗的态度。状态：confirmed。证据：`fay-willows.lua:113`。

### C15 | entry-03522 | 存在问题

原文“I should say to the shalore it may have been basic food and drink”，译文“我应该对永恒精灵说，这可能对它们来说是基本的食物和饮料”。原文是叙述者补充说明“按永恒精灵的标准”，没有向永恒精灵说话的行为；译文错误拆分句法，增加说话对象。状态：confirmed。证据：`fay-willows.lua:115`，后半句紧接自然精灵的生活标准作比较。

### C16 | entry-03522 | 存在问题

原文“move northwards around this area”，译文“在这个地区向北移动”。原文说的是从北面绕过这片区域，译文丢失“绕行”，改变解释返程受阻时的路线关系。状态：confirmed。证据：`fay-willows.lua:119–121`。

### C17 | entry-03522 | 存在问题

原文“huge gashes”，译文“一道巨大的伤口”。复数伤口被明确改成一道；同段后文也继续使用复数“wounds”。状态：confirmed。证据：`fay-willows.lua:125`。

### C18 | entry-03522 | 存在问题

原文“their numbers … more manageable amounts”，译文“当痊愈士兵的数量开始达到一定程度时”。原文承接尚待处理的伤兵数量下降，译文改成痊愈士兵数量达到某个程度，改变主治医师得以抽身致谢的条件。状态：confirmed。证据：`fay-willows.lua:131` 的前后两句。

### C19 | entry-03522 | 存在问题

原文“looked behind me as a soldier approached”，译文“当一名士兵走近时……看着我”。视线落点由叙述者身后改成叙述者本人，丢失医师看到接近士兵的动作关系。状态：confirmed。证据：`fay-willows.lua:131`。

### C20 | entry-03522 | 存在问题

原文“fulfilling my end of the bargain”，译文“完成了我的交易”。原文限定为履行自己一方的约定，译文写成整项交易已经完成；随后安排会见将军，正是在推进对方应提供的部分。状态：confirmed。证据：`fay-willows.lua:131`。

### C21 | entry-03527 | 存在问题

原文“a … plot that I would learn the day after”，译文“一场我事后知道的……阴谋”。“次日得知”被泛化成“事后知道”，遗漏明确的时间关系。状态：confirmed。证据：`fay-willows.lua:216`。

### C22 | entry-03527 | 存在问题

原文“a surprise to see them out here”，译文“看到他们这样做，我有点惊讶”。信使惊讶的是矮人出现在这里，译文变成惊讶于前述提供食物、酒水的行为，改变评价对象。状态：confirmed。证据：`fay-willows.lua:218–220`；紧接着讨论的正是矮人为何居住在钢铁王座以外。

### C23 | entry-03527 | 存在问题

原文“Hard to really know with how secretive the dwarves are”，译文“要想真正了解矮人们的隐秘程度是很难的”。难以知道的是矮人是否还有其他家园；矮人保密是原因。译文把原因改成了需要了解的对象。状态：confirmed。证据：`fay-willows.lua:218`。

### C24 | entry-03527 | 存在问题

原文询问是否知道矮人携带了什么会被城门守卫没收的物品，译文“你可能还不知道，士兵会没收矮人们携带的物品，知道吗？”变成告知、确认没收行为。询问内容及信息流向均改变。状态：confirmed。证据：`fay-willows.lua:222`，答复具体指向附魔物品。

### C25 | entry-03527 | 存在问题

原文“They say that it's too dangerous for civilians to carry such items”在译文中整句遗漏。官方以平民携带危险为由的说辞因此消失，只剩信使认为任何人都不应携带的个人意见。状态：confirmed。证据：`fay-willows.lua:224`。

### C26 | entry-03527 | 存在问题

原文“a couple of halflings”，译文两次写成“一对半身人夫妇”。原文只说明人数，没有婚姻或伴侣关系。状态：confirmed；同条重复出现合并为一个 claim。证据：`fay-willows.lua:226`。

### C27 | entry-03527 | 存在问题

原文“any plans to deal with the Shaloren”，译文“你对永恒精灵有什么想法？”原文试探对付永恒精灵的行动计划，译文泛化成态度或看法，削弱了探查阴谋的具体询问。状态：confirmed。证据：`fay-willows.lua:228`，后续邀请也围绕即将实施的计划展开。

### C28 | entry-03527 | 存在问题

原文“Maj'Eyal”，译文“马基埃亚尔”。冻结术语子集明确记录该世界地名采用“马基·埃亚尔”，并注明旧写法已被取代；本条是 `_t` 下的相同地名语境。状态：confirmed。证据：INPUT 术语子集的 `Maj'Eyal / T.PN.WORLD / _t` 条目及 `fay-willows.lua:228`。此观察不提出新的全局命名策略。

### C29 | entry-03531 | 存在问题

原文“become enthralled to the slavers will”，译文“被奴役者的意志所吸引”。原文描述意志受控制、被奴役，译文变成被吸引，改变灵能控制的性质；后面的服从命令不能使这两个状态等同。状态：confirmed。证据：`fay-willows.lua:289`，同段明确提到挣脱控制并驱散幻象。这里不适用鲜血之环“奴隶贩子”的术语语境。

### C30 | entry-03531 | 存在问题

原文两次使用“thrown me”，译文分别为“谁在拉我”“为什么把我拉到这里”。被扔进帐篷的暴力动作被改成拉入。状态：confirmed；两处合并为一个 claim。证据：`fay-willows.lua:291`，前章 `:282` 也明确写出伸手将她扔进帐篷。

### C31 | entry-03531 | 存在问题

原文“another kick with the back of the heel to my face”，译文“又踢了我一脚，脚踩在我的脸上”。原文是一记以脚跟击中面部的踢击，译文改变为踢后踩脸的动作。状态：confirmed。证据：`fay-willows.lua:295`。

### C32 | entry-03531 | 存在问题

原文“I had thought better of you”，译文“我就更想念你了”。原文是因她杀死半身人而对她评价较高，译文变成思念。状态：confirmed。证据：`fay-willows.lua:295`，后句紧接曾把她视为自然盟友、如今失望的解释。

### C33 | entry-03531 | 存在问题

原文“a faceless humanoid”，译文“一个面目全非的人形”。原文明确表示没有面孔，译文仅表示面貌变得无法辨认，丢失幻象失去脸部形态的特征。状态：confirmed。证据：`fay-willows.lua:299`，随后该形象彻底消失。

### C34 | entry-03531 | 存在问题

原文是斗篷人“briefly visited the messenger when I was talking to him”，译文“我在客栈和信使谈话时短暂拜访过的那个人”。拜访者由斗篷人变成叙述者，受访者也随之改变。状态：confirmed。证据：`fay-willows.lua:301`；`:226` 明确记载斗篷人走近信使交谈。

### C35 | entry-03531 | 存在问题

原文“a bit confused … a moment to realize”，译文“困惑许久，我才意识到”。短暂反应被改成持续很久，改变紧接刺杀受阻这一瞬间的时间尺度。状态：confirmed。证据：`fay-willows.lua:305`。

实际读取与边界记录：

- 冻结包根目录 `B`：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923/`。
- 读取了 `B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。40 个 ID 连续，INPUT 与 entries.json 的原译文逐条一致；邻近译文仅查阅 context.lua。
- 读取并核验了下列六个源码文件，均位于 `B/sources/dlc/cults/tome-cults/`，SHA-256 均与 source-access 清单一致：

| 相对源码路径 | SHA-256 |
|---|---|
| `data/general/npcs/corrupted_blobs.lua` | `76cbc59be306a63bfa17d81904820c3838543a9b8b074554190bca408bbfbec4` |
| `data/general/npcs/horror.lua` | `8d63e86d5eb6f7552ec2cdfe598b45618460028236190f246202809c045f461d` |
| `data/general/objects/world-artifacts.lua` | `27af5b2ae30c5b2db7f1d585b8334bc28ee1284e771a8a9f5c198f892edbc92a` |
| `data/glyph_sequences/cults.lua` | `9d3b29fd6a91fb9ced64581b760fc0026b0fb0bcf9cc687a55399aed76faaabf` |
| `data/lore/dremwarves.lua` | `0b8133e8ef00f5b0ca5fcb2f7df1ebec355873ac5dfac9454a85a48084b326e9` |
| `data/lore/fay-willows.lua` | `05a3f93c9f5cd5baf52429155fcd4a09b6045ef45fbf3472562d55f5da0e4c6f` |

额外源码读取及调用来源：

- `world-artifacts.lua:210` 的 `require("mod.dialogs.RingOfTheHunter")` 引入获准文件 `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/overload/mod/dialogs/RingOfTheHunter.lua`。哈希核验为 `2894023dcca501a035239c74a9873ff4df4e1433f2513c6203e352a6705d33fa`。其 `unload()` 将所选技能写入装备的 `wielder.learn_talent`。
- `world-artifacts.lua:1029` 的 `who:his_her()` 引入本体调用追踪。仅通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取：
  - `game/modules/tome/class/Actor.lua`：确认继承 `engine.Actor`。
  - `game/engines/default/engine/Actor.lua`：`:607` 将调用转发给 `string.his_her(self)`。
  - `game/engines/default/engine/utils.lua`：`:939–943` 按性别返回本地化所属代词。没有读取其他语言译文，也未把未观察到的最终运行画面称为实测。

DLC 的源码仓库、commit 和目标发行版本适用性仍未固定；已核验的是上述快照内容，版本适用性缺口保留待确认。本体固定 commit 未套用于 DLC。未发现需要另外列为待确认的具体译文 claim。

未越界读取、未读取其他审核报告、未创建子 agent、未修改仓库，未创建临时目录或文件。本次交付仅为独立审核观察，不作生产完成认证。
