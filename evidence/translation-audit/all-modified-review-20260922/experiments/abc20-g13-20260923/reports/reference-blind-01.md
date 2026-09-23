| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03653 | 未发现问题 | 转移过程与目的地一致 |
| entry-03654 | 未发现问题 | 减伤数值、负面效果解除时机一致 |
| entry-03655 | 未发现问题 | 五项参数顺序及作用对象一致 |
| entry-03656 | 未发现问题 | 身体进化含义及目标标记保留 |
| entry-03657 | 未发现问题 | 熵能包围的含义一致 |
| entry-03658 | 存在问题 | C01：看见恐魔与被恐魔看见颠倒 |
| entry-03659 | 未发现问题 | 去向不明的语气保留 |
| entry-03660 | 未发现问题 | 训练对象与用途一致 |
| entry-03661 | 未发现问题 | 人类学徒身份一致 |
| entry-03662 | 未发现问题 | 永恒精灵学徒身份一致 |
| entry-03663 | 未发现问题 | 半身人学徒身份一致 |
| entry-03664 | 未发现问题 | 声音描述与颜色标记保留 |
| entry-03665 | 未发现问题 | 格朗格激怒伟大存在的关系正确 |
| entry-03666 | 未发现问题 | 发言者、颜色及消息参数一致 |
| entry-03667 | 未发现问题 | 安全存放物品的用途保留 |
| entry-03668 | 存在问题 | C02：遗漏书页属于特定书册的关系 |
| entry-03669 | 未发现问题 | 宝箱产出物品的事件含义一致 |
| entry-03670 | 未发现问题 | 颜色参数与章节名称参数顺序正确 |
| entry-03671 | 未发现问题 | 声音描述与颜色标记保留 |
| entry-03672 | 未发现问题 | 胃液来袭预警与躲避指令保留 |
| entry-03673 | 未发现问题 | 源码为商店实体；existing不强制改名 |
| entry-03674 | 未发现问题 | 商店名称语义成立 |
| entry-03675 | 未发现问题 | 商店名称语义一致 |
| entry-03676 | 未发现问题 | 攻击指令及代词标记保留 |
| entry-03677 | 未发现问题 | 种族与邪教徒身份一致 |
| entry-03678 | 未发现问题 | 源码为商店实体；existing不强制改名 |
| entry-03679 | 未发现问题 | 商店名称语义成立 |
| entry-03680 | 未发现问题 | 商店名称语义一致 |
| entry-03681 | 存在问题 | C03：遗漏骨骼吱嘎作响的描写 |
| entry-03682 | 未发现问题 | 肯定回应与对话语境一致 |
| entry-03683 | 存在问题 | C04、C05：辱骂习语误解；状态延续误作变化 |
| entry-03684 | 存在问题 | C06—C08：保密范围、掘进方式与安全离开信息 |
| entry-03685 | 存在问题 | C09、C10：身体改造因果关系及明确术语要求 |
| entry-03686 | 未发现问题 | 职业及所属类别一致 |
| entry-03687 | 待确认 | C11、C12：冷却适用范围与黑血归属的快照差异 |
| entry-03688 | 未发现问题 | 新种族提示一致 |
| entry-03689 | 存在问题 | C13—C15：让步信息遗漏、专名指称与抗性范围 |
| entry-03690 | 未发现问题 | 新技能类别提示一致 |
| entry-03691 | 存在问题 | C16：腐化程度误作腐化原因 |
| entry-03692 | 未发现问题 | 全文保留随机幅度、几率及随疯狂值增长关系 |

以下源码路径以 `tome-cults/` 开头；完整读取位置列于文末。所有 DLC 源码证据均来自哈希匹配的公开快照，**源码仓库、commit及目标版本对应关系未固定**。纯语义问题直接依据冻结原译文；涉及快照与机制差异的观察另列待确认。

### C01 | entry-03658 | 存在问题

原文：“bolstered at the sight of the horror”；译文：“在恐魔的视线中被强化”。

**状态：已证实的语义错误。** 原文是目标看见恐魔而受到鼓舞，译文变成目标处于恐魔的视线之中，颠倒了观看者与被观看者。

证据：`data/timed_effects.lua:2330`，`HORRIFIC_FORTRESS.on_gain`。这是效果获得时的提示；`data/talents/misc/races.lua:164–165` 在召唤恐魔后给召唤者施加此效果，并没有把提示写成恐魔注视目标。此处确认语言关系错误，不据此断言目标版本的视线判定机制。

### C02 | entry-03668 | 存在问题

原文：“A page of the tome.”；译文：“书页。”

**状态：已证实的信息遗漏。** 原文说明这是所指书册中的一页；译文只留下物品类别，没有保留属于该书的关系。

证据：`data/zones/ft-horrors/objects.lua:25–29`，三份 `NOTE` 实体共用此描述，分别关联 `cults-tome-horrors-1/2/3`。冻结 `context.lua:460` 同样仅给出“书页”，没有在这条描述中补回所属关系。

### C03 | entry-03681 | 存在问题

原文：“creeking and vibrating”；译文：“颤动”。

**状态：已证实的信息遗漏。** 此处 `creeking` 是语境明确的拼写误差，描写骨杖骨骼吱嘎作响；译文只保留振动，丢失声音描写。

证据：`hooks/bonestaff.lua:22–24`，`CommandStaff:SentientOptions` 的 `intro` 分支直接提供这段叙述。不是运行时音效是否播放的问题。

### C04 | entry-03683 | 存在问题

原文：“Stupid useless pathetic excuse of a … ‘necromancer’”；译文：“像你这样的……‘死灵法师’竟然会用这样蹩脚的借口”。

**状态：已证实的语义错误。** `pathetic excuse of a necromancer` 是直接辱骂对方不配称为死灵法师；译文把 `excuse` 当成对方提出的借口，虚构了“使用借口”的行为，同时丢失“愚蠢、无用”的辱骂内容。

证据：`hooks/bonestaff.lua:114–117`，`bone_horror_disabled` 对话。紧接着的玩家回答为“I have my reasons!”，并不能将前一句的习语解释为对方已经给出了借口。

### C05 | entry-03683 | 存在问题

原文：“The staff stays calm.”；译文：“法杖平静了下来。”

**状态：已证实的状态关系错误。** 原文描述继续保持平静；译文描述从不平静转为平静，新增了状态变化。

证据：`hooks/bonestaff.lua:115`，同一拒绝启用力量的对话叙述。与 C04 属于不同语义缺陷。

### C06 | entry-03684 | 存在问题

原文：“the only rules … secrecy and safeguarding the accrued knowledge”；译文：“唯一规则就是必须对在里面学到的知识进行严格的保密和保护”。

**状态：已证实的范围缩减。** 前一句明确说明避难所一旦被发现就会遭毁灭，因此这里的保密要求包括隐匿避难所及其活动；译文把保密对象全部收束为“学到的知识”，丢失这项生存规则的范围。

证据：`overload/data/texts/intro-cults.lua:25`，发现避难所、摧毁避难所与保密规则位于同一段，构成直接语境证据。

### C07 | entry-03684 | 存在问题

原文：“a giant worm that is tunneling directly towards Kroshkkur”；译文：“一条直接冲向克诺什库尔的巨型蠕虫”。

**状态：已证实的信息遗漏。** `tunneling` 明确说明蠕虫正在掘进；“冲向”没有保留穿掘通道的移动方式，并带入了冲刺意味。

证据：`overload/data/texts/intro-cults.lua:27`。这是原文直接提供的威胁场景信息，不依赖推测蠕虫的运行时代码。

### C08 | entry-03684 | 存在问题

原文：“leave now while it is safe to do so”；译文：“或者就这样离开”。

**状态：已证实的信息遗漏。** 原文明确告知当前离开仍然安全，属于玩家选择的条件信息；译文没有保留这一安全性说明。前段“在蠕虫到来之前离开”保留了时间关系，但不能替代明确的安全性判断。

证据：`overload/data/texts/intro-cults.lua:29`，传送入虫体与安全离开的选择段落。

### C09 | entry-03685 | 存在问题

原文：“as a result of the changes made to their bodies by the Ziguranth”；译文：“作为上面条件的附加作用……被伊格兰斯的反魔法力量所灌注”。

**状态：已证实的因果与修饰关系错误。** 原文明确把反魔力量灌注归因于伊格兰斯对身体的改造；译文用不明确的“上面条件”取代改造行为，并把“伊格兰斯”改成力量的所属者。这超出了单纯措辞不自然。

证据：`overload/data/texts/intro-krog.lua:24–26`。前段讲符文被剥除及自然力量维生，后段另行明确身体改造导致反魔力量灌注。

### C10 | entry-03685 | 存在问题

原文：“Maj'Eyal”；译文：“马基埃亚尔”。

**状态：已证实的术语不符合。** 冻结术语子集明确将“马基·埃亚尔”列为 `preferred`，并注明旧写法“马基埃亚尔”已被取代。本条是 `_t` 的世界地名叙述，适用该要求。

证据：INPUT 术语快照的 `Maj'Eyal / T.PN.WORLD / _t` 条目；`overload/data/texts/intro-krog.lua:26`。

### C11 | entry-03687 | 待确认

原文：“eliminate cooldown on talents”；译文：“使技能不进入冷却”。

**状态：快照内适用范围差异已证实；目标版本适用性待确认。** 快照中并非所有技能、每次使用都不进入冷却：

- `data/talents/misc/races.lua:36–43`：施加持续三回合的 `DREM_FRENZY`。
- `superload/mod/class/Actor.lua:113–123`：排除刻印、通用技能、超系技能、被动、固定冷却及部分瞬发技能；仅在该技能未记入 `used_talents` 时将 `data.cd` 置零。

英文解锁摘要本身也省略了这些限制，因此不能全部归为翻译新增。尚缺该 DLC 快照与审核目标版本一致的来源证据，故不将此项作为目标版本已确认缺陷。

### C12 | entry-03687 | 待确认

原文：“Bleed your black blood on your attackers”；译文：“让黑血溅到攻击你的人身上”。

**状态：快照内流血主体差异已证实；目标版本适用性待确认。** 快照实际给攻击者施加黑血流血效果，而非表现为自身黑血溅到攻击者身上：

- `data/talents/misc/races.lua:57–60`：`callbackOnMeleeHit` 对攻击来源 `src` 调用 `setEffect`。
- `data/timed_effects.lua:85–95`：受效果者“starts to bleed black blood”，并在其坐标结算暗影伤害。

英文摘要也含有自身黑血的表述，存在上游描述与实现不一致，不能只归责译文。缺少目标 DLC 版本与快照对应证明，保留待确认。

### C13 | entry-03689 | 存在问题

原文：“But while they are magic users Ziguranth took pity on them”；译文：“然而，伊格兰斯同情他们被强迫而无法选择的命运”。

**状态：已证实的信息遗漏。** 译文保留了同情的原因，却遗漏“尽管他们使用魔法”的让步条件，削弱了反魔教团为何对这群魔法使用者破例的叙事关系。

证据：`overload/data/texts/unlock-race_krog.lua:24`。前段的符文维生事实不能替代这里明确提出的让步关系。

### C14 | entry-03689 | 存在问题

原文：“Zigur was finally able to create an offshoot”；译文：“伊格兰斯终于创造出食人魔的一个亚种”。

**状态：已证实的专名指称替换。** 原文这里使用 `Zigur`，译文却替换成 `Ziguranth` 对应的教团名。即使地点名称在句中借代当地共同体，也不等于英文改用了教团名称。

证据：`overload/data/texts/unlock-race_krog.lua:24–26` 连续分别使用 `Ziguranth`、`Zigur`、`Zigur`；冻结术语子集明确区分“伊格”与“伊格兰斯”，要求不得互换。

### C15 | entry-03689 | 存在问题

原文：“resist the elements themselves”；译文：“抵抗元素魔法伤害”。

**状态：已证实的文本范围缩减。** 原文未限定元素伤害来自魔法；译文新增“魔法”条件，把描述范围缩窄。此项文本差异不依赖目标版本机制即可成立。

快照补充证据：`data/talents/misc/races.lua:224–235` 的 `Drake-Infused Blood.passives` 添加按伤害类型索引的 `resists`；该分支没有按攻击来源是否为魔法加条件。这里仅陈述快照中的赋值行为，不将其提升为已固定目标版本的完整抗性消费证明。

### C16 | entry-03691 | 存在问题

原文：“corrupted beyond hope”；译文：“被绝望所腐化”。

**状态：已证实的语义错误。** `beyond hope` 描述腐化已达到无可挽救的程度；译文却把“绝望”写成造成腐化的原因，改变了程度与因果关系。

证据：`overload/data/texts/unlock-wyrmic_scourge.lua:21`。该判断来自完整句法语境，无需推定任何“绝望”机制。

实际读取材料与边界如下。

冻结包根目录 `P`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923
```

读取了 `P/INPUT.md`、`P/entries.json`、`P/context.lua`、`P/source-access.json`，以及以下全部源码路径；下列路径均相对 `P/sources/dlc/cults/tome-cults/`：

```text
data/timed_effects.lua
data/zones/entropic-void/grids.lua
data/zones/ft-cultist/npcs.lua
data/zones/ft-haze-cave/grids.lua
data/zones/ft-haze-cave/npcs.lua
data/zones/ft-haze-cave/zone.lua
data/zones/ft-home/grids.lua
data/zones/ft-horrors/objects.lua
data/zones/ft-illusory-castle/grids.lua
data/zones/ft-illusory-castle/zone.lua
data/zones/ft-yaech/grids.lua
data/zones/godfeaster/zone.lua
data/zones/test/traps.lua
data/zones/town-kroshkkur/npcs.lua
data/zones/town-kroshkkur/traps.lua
hooks/bonestaff.lua
overload/data/texts/intro-cults.lua
overload/data/texts/intro-krog.lua
overload/data/texts/unlock-demented_cultist_entropy.lua
overload/data/texts/unlock-race_drem.lua
overload/data/texts/unlock-race_krog.lua
overload/data/texts/unlock-wyrmic_scourge.lua
overload/mod/class/CultsDLC.lua
```

额外源码根目录 `A`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults
```

| 实际额外读取路径（相对 A） | 已读材料中的追查来源 |
|---|---|
| `tome-cults/data/talents/misc/races.lua` | 德瑞姆、克罗格解锁说明中的 Frenzy、黑血及龙血种族能力 |
| `tome-cults/superload/mod/class/Actor.lua` | `CultsDLC.lua:51` 的 `insanityEffectForce()`；并核验 `DREM_FRENZY` 冷却消费 |
| `tome-cults/data/talents/demented/scourge-drake.lua` | 解锁说明明确列出的四个技能名称 |

23 个包内源码文件与3个额外源码文件均核对 SHA-256，与 `source-access.json` 一致。未读取本体源码；清单中的本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 未用于替代 DLC 版本证明。

共覆盖 **40 条：存在问题8条、待确认1条、仅建议0条、未发现问题31条**。无法核验之处为上述 DLC 目标版本对应关系，具体未决观察见 C11、C12。未越界读取，未读取其他报告，未创建临时文件或子 agent，未修改仓库。本输出仅为独立审核观察，不代表生产验收结论。
