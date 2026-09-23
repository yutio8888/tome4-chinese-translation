| 完整 entry-ID | 四类判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03613 | 未发现问题 | 护甲、护盾数值及时限对应 |
| entry-03614 | 存在问题 | C01：把尝试眩晕写成必然施加 |
| entry-03615 | 未发现问题 | 日志对象及数量对应 |
| entry-03616 | 未发现问题 | 禁用条件和颜色标记对应 |
| entry-03617 | 未发现问题 | 伤害与半径参数重排正确 |
| entry-03618 | 未发现问题 | 地名对应 |
| entry-03619 | 未发现问题 | 施法失败语义对应 |
| entry-03620 | 存在问题 | C02、C03：速度术语及增伤类别标签 |
| entry-03621 | 未发现问题 | 玻璃碎片日志对应 |
| entry-03622 | 存在问题 | C04：遗漏投掷动作的熟练程度 |
| entry-03623 | 未发现问题 | 黑血、可见目标及抗性条件对应 |
| entry-03624 | 存在问题 | C05：精神诡计被写成精神冲击 |
| entry-03625 | 未发现问题 | 召唤失败日志对应 |
| entry-03626 | 存在问题 | C06：复数地下生物被限定成单一某物 |
| entry-03627 | 存在问题 | C07：首次命中条件被写成首次攻击 |
| entry-03628 | 未发现问题 | 当前项标记及样式对应 |
| entry-03629 | 未发现问题 | 教团名称、参数重排及副手能力对应 |
| entry-03630 | 存在问题 | C08：教团被写成地点 |
| entry-03631 | 未发现问题 | 咬击日志对应 |
| entry-03632 | 待确认 | C09：快照内原文既有的处决概率误述 |
| entry-03633 | 存在问题 | C10：全局速度术语不符 |
| entry-03634 | 未发现问题 | 堡垒撤离提示对应 |
| entry-03635 | 未发现问题 | 黑血开始日志对应 |
| entry-03636 | 未发现问题 | 黑血结束日志对应 |
| entry-03637 | 未发现问题 | 触须捕获日志对应 |
| entry-03638 | 未发现问题 | 脱离触须日志对应 |
| entry-03639 | 未发现问题 | 触手缠绕日志对应 |
| entry-03640 | 存在问题 | C11：受攻击被写成恐魔现身 |
| entry-03641 | 未发现问题 | 受攻击而惊恐的日志对应 |
| entry-03642 | 仅建议 | C12：增伤说明的语序生硬 |
| entry-03643 | 仅建议 | C13：“牺牲者”的语感选择 |
| entry-03644 | 未发现问题 | 变成恐魔及颜色标记对应 |
| entry-03645 | 存在问题 | C14：略见恐怖的事件信息丢失 |
| entry-03646 | 存在问题 | C15：技能名称指向错误 |
| entry-03647 | 未发现问题 | 三个生命阈值、范围及伤害对应 |
| entry-03648 | 未发现问题 | 创伤转移双方及标记对应 |
| entry-03649 | 未发现问题 | 显现日志对应 |
| entry-03650 | 未发现问题 | 豁免、闪避、暴击及免伤数值对应 |
| entry-03651 | 未发现问题 | 幸运／不幸层数的条件说明符合快照代码 |
| entry-03652 | 未发现问题 | 传送状态名称对应 |

### C01 | entry-03614 | 存在问题

原文为“**attempt to daze**”，译文为“对……敌人**施加眩晕**”，将尝试写成必然生效。`tome-cults/data/talents/demented/void.lua:242–245,279–281` 每半回合投射 `MESMERIZE`；由该符号追到额外源码 `tome-cults/data/damage_types.lua:105–116`，其中先检查目标能否受震慑，再设置眩晕效果。状态：**已证实的译文偏差**。

### C02 | entry-03620 | 存在问题

原文“global speed”译为“整体速度”。本包术语快照对 `tformat` 的该机制明确采用“全局速度”；`tome-cults/data/talents/misc/misc.lua:257–260` 和 `tome-cults/data/timed_effects.lua:2209–2219` 也表明它作用于全局速度。状态：**已证实的适用术语问题**。

### C03 | entry-03620 | 存在问题

原文类别“Power”译成“力量”，容易指向力量属性；同句说明的是“增加所有伤害”。`misc.lua:246–249,257–260` 选择 `TWISTED_POWER`，`timed_effects.lua:2246–2257` 将其效果加到全部伤害，而非力量属性。状态：**已证实的类别标签偏差**。

### C04 | entry-03622 | 存在问题

原文“**expertly** hurls a pebble”中的熟练程度在“投掷鹅卵石”中消失。`misc.lua:320–326` 是这条战斗日志的消费位置。状态：**已证实的信息遗漏**。

### C05 | entry-03624 | 存在问题

原文“resist **mind tricks**”指精神诡计或蛊惑，译文“抵抗**精神冲击**”改成了冲击性作用。`tome-cults/data/talents/misc/races.lua:90–97` 的效果是精神豁免与混乱免疫，也未提供“冲击”的依据。状态：**已证实的语义偏差**。

### C06 | entry-03626 | 存在问题

原文“affinity with **things** that dwell deep beneath the surface”泛指地下深处的一类事物；“同地下深处**某物**的联系”将其收窄为一个特定对象。语境见 `races.lua:171–176`。状态：**已证实的范围收窄**。

### C07 | entry-03627 | 存在问题

原文是每回合“first creature **hit**”，译文为“攻击的第一个生物”。`races.lua:204–209` 给出说明；`timed_effects.lua:1945–1953` 在造成正数伤害后才进入首次目标的处理。攻击但未命中或未造成伤害不满足该条件。状态：**已证实的触发条件偏差**。

### C08 | entry-03630 | 存在问题

原文“created by **ziguranth**”译成“被**伊格**制造”。本包术语快照区分教团 **Ziguranth＝伊格兰斯** 与地点 **Zigur＝伊格**；`races.lua:361–364` 指创建者，是教团语境。状态：**已证实的专名指称错误**。

### C09 | entry-03632 | 待确认

原文与译文都称低于 20% 生命后有“`%d%%` 几率”直接杀死。冻结快照 `races.lua:381–383,387–405` 虽计算 `getChance`，实际咬击流程在满足生命阈值及 `canBe("instakill")` 后没有概率抽取。这是**原文已有、译文沿袭的机制误述**，不是译文新增。DLC 快照哈希已核对，但其源码仓库和提交未固定；缺少目标版本源码，故目标版本适用性仍**待确认**。

### C10 | entry-03633 | 存在问题

原文“Increases **global speed**”译为“**整体速度**增加”。本包术语快照明确规定此 `tformat` 机制用“全局速度”；`races.lua:422–429` 实际写入 `global_speed_add`。状态：**已证实的适用术语问题**。

### C11 | entry-03640 | 存在问题

原文因恐魔双体“**attacking them**”而惊恐，译文改成因“两只恐魔的**现身**”而惊恐，改变了原因。`timed_effects.lua:273–285` 是该减闪避和法术豁免状态的说明与生效逻辑。状态：**已证实的语义偏差**。

### C12 | entry-03642 | 仅建议

“`+%d%% 所有造成的伤害`”语序生硬；层数和全部已造成伤害的增幅仍可读出，与 `timed_effects.lua:289–292` 一致。状态：**仅措辞偏好**。

### C13 | entry-03643 | 仅建议

“victim”写成“牺牲者”带有献祭语感；这条日志仍能表达受害对象的痛苦强化了目标。`timed_effects.lua:465–483` 显示其生命吸取语境。状态：**仅措辞偏好**。

### C14 | entry-03645 | 存在问题

原文说目标“**briefly saw** what True Horror means”，译文只说“被真正的恐惧吓倒”，丢失了短暂目睹这一事件，并将所见之物改写为恐惧本身。`timed_effects.lua:554–565` 的状态说明及获得日志均保留“saw”。状态：**已证实的信息遗漏与语义偏差**。

### C15 | entry-03646 | 存在问题

原文“**Hideous Visions**”译成“**失智冲击**”；冻结邻近译文 `context.lua:398` 将同一效果名称译为“**惊骇幻象**”，`timed_effects.lua:759–779` 也分别定义 `HIDEOUS_VISIONS` 与本条 `CACOPHONY`。现译会把玩家指向错误名称。状态：**已证实的指称错误**。

### 读取范围与版本

冻结包目录为 [abc20-g12-20260923](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923)。实际读取的包文件：

- [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/INPUT.md)：SHA256 `fe700723351a`
- [entries.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/entries.json)：`7e5008a70fca`；核对为 40 条，首尾 ID 分别为 `entry-03613`、`entry-03652`
- [context.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/context.lua)：`450a73e47e1d`
- [source-access.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/source-access.json)：`0d185e24d6ee`

实际读取并与 `source-access.json` 中 SHA256 核对一致的五个 Cults DLC section 源文件：

- [void.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/sources/dlc/cults/tome-cults/data/talents/demented/void.lua)：`19cb982e3487`
- [writhing-body.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/sources/dlc/cults/tome-cults/data/talents/demented/writhing-body.lua)：`37c7c1f3ebe5`
- [misc.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/sources/dlc/cults/tome-cults/data/talents/misc/misc.lua)：`3b37fe925ecb`
- [races.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/sources/dlc/cults/tome-cults/data/talents/misc/races.lua)：`59b9b67cb0a3`
- [timed_effects.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923/sources/dlc/cults/tome-cults/data/timed_effects.lua)：`0d3139ebf8a4`

额外读取 [damage_types.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/damage_types.lua)，SHA256 `6ec5f1659e60`，与允许清单一致。调用链来源是 `void.lua:242–245` 的 `DamageType.MESMERIZE`，对应 `damage_types.lua:105–116`。

上述 DLC 源码均为哈希固定的公开快照，**源码仓库及提交未固定**；C09 的目标版本适用性因此无法核验。没有读取其他报告、其他实验文件或当前翻译文件；没有创建临时文件、子 agent 或修改仓库，未发生越界。本结果仅为 REVIEWER 审核观察，不宣称生产 `DONE_VERIFIED`。
