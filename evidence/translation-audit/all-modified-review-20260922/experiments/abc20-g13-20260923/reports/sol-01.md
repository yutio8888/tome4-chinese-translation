以下是对冻结包 `entry-03653` 至 `entry-03692` 的独立审核观察。DLC 源码快照的文件哈希已与 `source-access.json` 核对；其源码仓库和 commit 未固定，因此涉及目标版本机制适用性的疑点仍标为待确认。

| 完整 entry-ID | 四类判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03653 | 未发现问题 | 转移状态一致 |
| entry-03654 | 未发现问题 | 减伤及施加时解除效果一致 |
| entry-03655 | 未发现问题 | “混乱免疫”对应源码属性 `confusion_immune` |
| entry-03656 | 未发现问题 | 状态提示一致 |
| entry-03657 | 未发现问题 | 状态提示一致 |
| entry-03658 | 存在问题 | C01 |
| entry-03659 | 未发现问题 | 裂隙提示一致 |
| entry-03660 | 未发现问题 | 训练对象及用途一致 |
| entry-03661 | 未发现问题 | 人类学徒一致 |
| entry-03662 | 未发现问题 | 永恒精灵学徒一致 |
| entry-03663 | 未发现问题 | 半身人学徒一致 |
| entry-03664 | 未发现问题 | 尖叫提示一致 |
| entry-03665 | 未发现问题 | 说话者及动作一致 |
| entry-03666 | 未发现问题 | 发言标签及参数一致 |
| entry-03667 | 未发现问题 | 存放物品的用途一致 |
| entry-03668 | 存在问题 | C02 |
| entry-03669 | 存在问题 | C03 |
| entry-03670 | 未发现问题 | 两个参数及章节提示一致 |
| entry-03671 | 未发现问题 | 尖叫提示一致 |
| entry-03672 | 未发现问题 | 胃部浪潮预警与躲避动作一致 |
| entry-03673 | 未发现问题 | 商店名称可对应铸剑铺 |
| entry-03674 | 未发现问题 | 店名语义一致 |
| entry-03675 | 未发现问题 | 店名语义一致 |
| entry-03676 | 未发现问题 | 代词标记保留 |
| entry-03677 | 未发现问题 | 德瑞姆邪教徒一致 |
| entry-03678 | 未发现问题 | 商店名称可对应铸剑铺 |
| entry-03679 | 未发现问题 | 店名语义一致 |
| entry-03680 | 未发现问题 | 店名语义一致 |
| entry-03681 | 存在问题 | C04 |
| entry-03682 | 未发现问题 | 回答一致 |
| entry-03683 | 存在问题 | C05 |
| entry-03684 | 存在问题 | C06、C07 |
| entry-03685 | 存在问题 | C08、C09 |
| entry-03686 | 未发现问题 | 职业及类别一致 |
| entry-03687 | 未发现问题 | 起源和种族特色一致 |
| entry-03688 | 未发现问题 | 种族名称一致 |
| entry-03689 | 存在问题 | C10、C11；另有待确认 C12 |
| entry-03690 | 未发现问题 | 技能类别名称无可证缺陷 |
| entry-03691 | 存在问题 | C13、C14 |
| entry-03692 | 存在问题 | C15 |

以下源码路径均相对于冻结包内的 `sources/dlc/cults/tome-cults/`。

### C01 | entry-03658 | 存在问题

原文 “at the sight of the horror” 指目标**看到恐魔**而获得强化；译文“在恐魔的视线中”变成**被恐魔看到**，颠倒了视线关系。`data/timed_effects.lua:2323-2339` 的 `HORRIFIC_FORTRESS` 将增益施于目标，并以来源恐魔 `eff.src` 是否仍存活控制效果。状态：已证实。

### C02 | entry-03668 | 存在问题

“A page **of the tome**”译为“书页”，丢失了书页属于那本特定书册的关系。`data/zones/ft-horrors/objects.lua:25-36` 将这段描述用于同一区域的书页实体，并定义了禁忌之书。状态：已证实的语义遗漏。

### C03 | entry-03669 | 存在问题

“An object **rolls** from the chest”译成物品从宝箱中“掉了出来”，把滚出写成掉出。`data/zones/ft-illusory-castle/grids.lua:92-97` 在开箱并放置物品时显示这条消息。状态：已证实的动作差异。

### C04 | entry-03681 | 存在问题

原文骨杖在手中“creeking **and vibrating**”；译文只有“颤动”，遗漏骨头作响的信息。`hooks/bonestaff.lua:22-25` 是骨杖对话的开场文本。状态：已证实。

### C05 | entry-03683 | 存在问题

“pathetic excuse of a ‘necromancer’”是在辱骂**对方不配称为死灵法师**；译文“会用这样蹩脚的借口”却说对方提出了借口，改变了被指责的内容。`hooks/bonestaff.lua:114-117` 显示这是骨杖对玩家的回答。状态：已证实。

### C06 | entry-03684 | 存在问题

原文外界敌视的是“such **activities**”，即这些研究活动；译文“对这些**知识**并不友好”改了敌视对象。`overload/data/texts/intro-cults.lua:23`。状态：已证实。

### C07 | entry-03684 | 存在问题

“Age of **Haze**”译为“**混沌**纪”，将 haze 的含义换成 chaos，改变了所指时代名称。`overload/data/texts/intro-cults.lua:23`。状态：已证实。

### C08 | entry-03685 | 存在问题

原文说反魔力量来自伊格兰斯**对克罗格身体所作改造**；译文“作为上面条件的附加作用”将原因接到前句的生存条件上。`overload/data/texts/intro-krog.lua:24-26`。状态：已证实的因果关系差异。

### C09 | entry-03685 | 存在问题

冻结术语子集明确要求 `_t` 世界地名 `Maj'Eyal` 使用“马基·埃亚尔”；译文“马基埃亚尔”缺少名称中的间隔点。原文见 `overload/data/texts/intro-krog.lua:26`。状态：已证实的适用术语差异。

### C10 | entry-03689 | 存在问题

原文 “**Zigur** was finally able to create…”指据点“伊格”；译文写“**伊格兰斯**终于创造…”，换成教团。冻结术语子集明确区分两者；原文见 `overload/data/texts/unlock-race_krog.lua:25`。状态：已证实。

### C11 | entry-03689 | 存在问题

原文克罗格是 “protectors of **Zigur**”；译文成了“**伊格兰斯**的坚实保护者”，再次把保护的据点换成教团。`overload/data/texts/unlock-race_krog.lua:26`。状态：已证实。

### C12 | entry-03689 | 待确认

“resist the **elements** themselves”译成抵抗“**元素魔法伤害**”，增加了“魔法”这一限制。`overload/data/texts/unlock-race_krog.lua:32` 只给出特色文案；本次允许的已读调用链没有确定该抗性的实际伤害范围，因此不能以文案单独裁定目标版本机制。缺少对应种族能力的目标版本源码证据。

### C13 | entry-03691 | 存在问题

“corrupted **beyond hope**”指腐化到无可挽回；译文“被**绝望**所腐化”把程度描述改成腐化原因。`overload/data/texts/unlock-wyrmic_scourge.lua:21`。状态：已证实。

### C14 | entry-03691 | 存在问题

“Hit where it hurts”结合后半句“伤害随负面效果增加”，指利用对方弱点；译文“击打对手**受伤的地方**”增加了原文没有的实体伤口条件。`overload/data/texts/unlock-wyrmic_scourge.lua:29`。状态：已证实。

### C15 | entry-03692 | 存在问题

原文说伤害和冷却时间“**have a chance** to increase or decrease”；译文“将会……上下浮动”遗漏了触发具有概率这一条件。`overload/mod/class/CultsDLC.lua:47-52` 定义资源说明及状态数值显示。状态：已证实。

### 读取范围与版本

冻结输入为 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923/INPUT.md)、同目录 `entries.json`、`context.lua`、`source-access.json`。其 SHA-256 依次为 `6277281276894b34d13bcef1e0482313f4ad4548b9de1cc132f766b1ae8709e6`、`f9d0f95a3ba5854e9844306ad99571498f695a21fa9452e689eff9dcf39301e7`、`fe560318e9bdbc1e66c6fd711194edfba4c65d738eda0fe91312823bc48dad54`、`1507e3568e4ffdb182e563f8868cdac60d85cd6c92a03c8c43d8dc168909d885`。`context.lua` 仅作哈希读取，未用其中邻近译文立论。

实际还读取了 `source-access.json` 的全部 23 个 `sections` 源码文件以核对哈希；逐段查看内容的是其中与上述条目相关的文件。23 个路径共同前缀为同目录的 `sources/dlc/cults/tome-cults/`，后缀如下：

- `data/timed_effects.lua`
- `data/zones/entropic-void/grids.lua`
- `data/zones/ft-cultist/npcs.lua`
- `data/zones/ft-haze-cave/grids.lua`、`npcs.lua`、`zone.lua`
- `data/zones/ft-home/grids.lua`
- `data/zones/ft-horrors/objects.lua`
- `data/zones/ft-illusory-castle/grids.lua`、`zone.lua`
- `data/zones/ft-yaech/grids.lua`
- `data/zones/godfeaster/zone.lua`
- `data/zones/test/traps.lua`
- `data/zones/town-kroshkkur/npcs.lua`、`traps.lua`
- `hooks/bonestaff.lua`
- `overload/data/texts/intro-cults.lua`、`intro-krog.lua`、`unlock-demented_cultist_entropy.lua`、`unlock-race_drem.lua`、`unlock-race_krog.lua`、`unlock-wyrmic_scourge.lua`
- `overload/mod/class/CultsDLC.lua`

23 个文件的 SHA-256 均与 `source-access.json` 所列值相符。它们是 **DLC 公开快照，源码仓库及 commit 未固定**；没有读取额外 DLC 源码或本体源码，因此没有新增文件的调用链。C12 是本次无法核验的机制疑点。未读取其他报告，未越界，未创建临时文件或修改仓库。以上仅为 REVIEWER 观察，不声称生产 `DONE_VERIFIED`。
