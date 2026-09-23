| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03613 | 未发现问题 | 护甲、护盾数值、持续时间及恢复限制表达一致 |
| entry-03614 | 存在问题 | C01；另有待确认 C02 |
| entry-03615 | 未发现问题 | 日志实际增加 Void Stars 的数量，“虚空之星”有源码支持 |
| entry-03616 | 存在问题 | C03 |
| entry-03617 | 仅建议 | C04；参数重排正确 |
| entry-03618 | 未发现问题 | 地名与本包传送状态名称一致 |
| entry-03619 | 未发现问题 | 准确表达施法未成功 |
| entry-03620 | 仅建议 | C05；“至多”符合候选不足时退出的实现 |
| entry-03621 | 未发现问题 | 所在技能及施加状态均为玻璃碎片 |
| entry-03622 | 存在问题 | C06 |
| entry-03623 | 存在问题 | C07；可见性及黑血限定有快照支持 |
| entry-03624 | 存在问题 | C08 |
| entry-03625 | 未发现问题 | 召唤空间不足表达准确；未强套 logSeen 条目 |
| entry-03626 | 待确认 | C09；段落重排不改变参数归属 |
| entry-03627 | 待确认 | C10 |
| entry-03628 | 未发现问题 | 当前选项含义及斜体、颜色标记保留 |
| entry-03629 | 待确认 | C11；六个参数的重排正确 |
| entry-03630 | 存在问题 | C12 |
| entry-03631 | 未发现问题 | 尝试啃咬及双方角色保留 |
| entry-03632 | 待确认 | C13、C14 |
| entry-03633 | 存在问题 | C16；另有措辞建议 C15 |
| entry-03634 | 未发现问题 | 战斗指令及堡垒救援信息保留 |
| entry-03635 | 未发现问题 | 黑血流血开始日志准确 |
| entry-03636 | 未发现问题 | 黑血流血结束日志准确 |
| entry-03637 | 未发现问题 | 触须捕获及目标标记准确 |
| entry-03638 | 未发现问题 | 触须束缚解除信息准确 |
| entry-03639 | 未发现问题 | 触手缠绕含义及目标标记准确 |
| entry-03640 | 未发现问题 | 快照实际由近距离光环施加，不要求攻击命中 |
| entry-03641 | 未发现问题 | 恐魔攻击与目标惊恐的关系保留 |
| entry-03642 | 未发现问题 | 层数、全部伤害增幅及参数顺序准确 |
| entry-03643 | 存在问题 | C17 |
| entry-03644 | 未发现问题 | 此处是恐魔外形语境，非效果类别名称 |
| entry-03645 | 存在问题 | C18 |
| entry-03646 | 待确认 | C19 |
| entry-03647 | 未发现问题 | 快照使用跨越至小于等于阈值的判断，“降低至”可成立 |
| entry-03648 | 未发现问题 | 创伤转移方向与日志双方标记一致 |
| entry-03649 | 未发现问题 | `%s` 消费受影响生物名称，译文所属关系一致 |
| entry-03650 | 未发现问题 | 本句用于超过六层的分支；不能套用一层幸运的符号问题 |
| entry-03651 | 待确认 | C20；新增的层数消耗与治疗覆盖顺序有快照支持 |
| entry-03652 | 未发现问题 | 与同包传送技能名称一致 |

下文源码路径采用这些前缀：

- `S/`：本包 `sources/dlc/cults/tome-cults/`。
- `D/`：白名单追加快照根目录下的 `tome-cults/`。
- `T/`：本体仓库 `/workspace/t-engine4` 的固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

所有 DLC 证据均来自哈希匹配的公开快照；**DLC 源码仓库、commit 及目标版本适用性未固定**。下列机制疑点只陈述快照内事实，不将本体 commit 当作 DLC 版本。

### C01 | entry-03614 | 存在问题

原文明确说“**attempt to daze**”，译文为“每半回合……**施加眩晕2回合**”，没有保留“尝试”的限定，弱化了能否成功施加的不确定性。这是可直接对照的语义遗漏。

补充证据：`S/data/talents/demented/void.lua:242–257` 将召唤者法术强度传给 `MESMERIZE`；`D/data/damage_types.lua:106–114` 先检查 `target:canBe("stun")`，通过后才调用 `setEffect(EFF_DAZED, 2, ...)`。并非对范围内所有敌人无条件生效。

### C02 | entry-03614 | 待确认

原文与译文都宣称“**every half a turn／每半回合**”。

快照的 `S/data/talents/demented/void.lua:242–245` 在巨石 `on_act` 中投射眩晕并清空行动能量，召唤定义未设置双倍行动速度。本体 `T/game/modules/tome/class/Actor.lua:168–170、761–773` 的默认速度为 1，满足行动能量门槛才调用 `on_act`；`T/game/engines/default/engine/GameEnergyBased.lua:124–129` 按速度累积能量。

现有链条没有支持固定“半回合一次”的调度。这是**沿袭英文的频率疑点**；尚缺与目标 DLC 版本对应的完整初始化、运行调度证据，不能直接裁定目标版本中的实际间隔。

### C03 | entry-03616 | 存在问题

原文片段“**but is currently disabled**”的主语来自拼接宿主“**Your tentacle hand**”；译文自行指定为“**该技能暂时被禁用**”，改变了禁用对象。

`S/data/talents/demented/writhing-body.lua:53–64` 将本片段插入触手手部属性说明；`canTentacleCombat`（32–40 行）判断的是触手战斗是否可用。冻结语境支持“触手手部不可用”，不能据此扩大为整个技能被禁用。

### C04 | entry-03617 | 仅建议

“**a glorious explosion of gore**”译为“自爆成一团**光荣的血肉**”，修饰搭配生硬。但自爆、血肉爆炸、伤害、范围及主人死亡条件均可理解，未发现可独立证明的机制信息错误。

这属于自然度建议。`S/data/talents/misc/misc.lua:47–61` 的使用条件及两个参数与译文一致，`args_order=[2,1]` 正确。

### C05 | entry-03620 | 仅建议

“global speed”译为“整体速度”，在此仍能表达全局行动速度。冻结术语中的相关 preferred 行标为 `scope=core`，本条属于 Cults DLC；本包没有明确给出该范围向 DLC 强制扩展的规则，因此不据此确认术语违规。

这里只保留名称一致性的建议，不计缺陷。`S/data/talents/misc/misc.lua:242–260` 支持随机进化、至多指定数量、五回合及三种增益。

### C06 | entry-03622 | 存在问题

原文“**expertly hurls a pebble**”的译文只有“投掷鹅卵石”，遗漏了动作娴熟、熟练的方式信息。

这是轻微但明确的语义遗漏，不是单纯润色偏好。`S/data/talents/misc/misc.lua:325` 的完整战斗日志直接包含该修饰语；它不代表额外命中或伤害加成。

### C07 | entry-03623 | 存在问题

原文“**small spikes**”译为“尖刺”，遗漏了尖刺尺寸小这一外观信息。该信息在其他句子中也没有保留，属于轻微语义遗漏。

证据：冻结原文及 `S/data/talents/misc/races.lua:74`。另行核对后，译文增加的“可见”“流着黑血”并非无依据扩张：同文件 62–70 行同时检查可见性、黑血状态和距离。

### C08 | entry-03624 | 存在问题

原文“resist **mind tricks**”译为“抵抗**精神冲击**”，把精神欺骗、迷惑手段改成了冲击，丢失了原句的欺骗性含义。

`S/data/talents/misc/races.lua:83–97` 的语境是无面容、无情绪、精神豁免及混乱免疫，没有把这里的 `mind tricks` 指定为冲击或伤害。数值句本身没有发现问题。

### C09 | entry-03626 | 待确认

原文与译文都说巨口“**Each turn／每回合**”拉拽敌人。

`S/data/talents/misc/races.lua:149–162` 为巨口配置 `T_DREM_CALL_OF_AMAKTHEL`，召唤时强制使用一次；该技能在 `S/data/talents/misc/misc.lua:113–135` 设置 `cooldown=2`，通过技能动作执行拉拽。现有证据不能支持其随后固定每回合拉拽。

这是沿袭英文的频率疑点。尚缺该快照实际使用的 `dumb_talented` AI 调度实现及目标 DLC 版本映射；没有据此确认译文错误。

### C10 | entry-03627 | 待确认

译文说“**每回合攻击的第一个生物100%%**”，英文也是“first creature hit”。

快照 `S/data/timed_effects.lua:1945–1953` 先排除死亡目标、非正伤害及不能被震慑的目标，然后才检查或建立本回合的触发记录。因此首次命中若不符合这些条件，后续符合条件的目标仍可能享有第一次触发待遇。

“第一个生物”没有准确区分首次命中与首次符合条件的伤害事件。该简化也存在于英文；快照内条件已核实，但目标 DLC 版本未固定，故保留待确认。

### C11 | entry-03629 | 待确认

原文及译文均概括为杀死“**100 enemies／100个敌人**”。

`S/data/talents/misc/races.lua:238–241` 的计数回调先执行 `target:worthExp(self) <= 0` 则返回，只有通过此条件才增加计数；223 行以计数达到 100 决定能否使用，275 行在变更类型后清零。

因此快照并非所有敌人死亡都计入。这是英文已存在、译文继续沿用的条件遗漏疑点；目标 DLC 版本中的相同行为仍待确认。

### C12 | entry-03630 | 存在问题

原文“created by **ziguranth**”译成“被**伊格**制造”，将教团／人群换成了地点。

冻结术语明确区分 Ziguranth「伊格兰斯」与 Zigur「伊格」；同组 entry-03629 也将同一主体译作伊格兰斯。`S/data/talents/misc/races.lua:361` 明确写的是 `ziguranth`。这是指称错误，不依赖新的全局命名决定。

### C13 | entry-03632 | 待确认

原文及译文宣称存在随体质增长的“**%d%% chances／%d%%几率**”秒杀。

快照 `S/data/talents/misc/races.lua:382、398–403、412` 中，`getChance` 只用于说明文字；实际动作在生命条件满足后检查 `canBe("instakill")`，然后调用 `die`，没有消费该展示几率。本体 `T/game/modules/tome/class/Actor.lua:7599–7635` 的 `canBe` 消费免疫条件，不消费这里的体质派生展示值。

这是**沿袭英文的几率说明与动作实现不一致**。快照内事实明确，目标 DLC 版本适用性待确认。

### C14 | entry-03632 | 待确认

原文“**under 20%%**”与译文“生命**不足20%%**”都排除了恰好 20%。

快照 `S/data/talents/misc/races.lua:398` 仅在生命比例 **大于** 20 且目标未死亡时提前返回；恰好 20% 的存活目标会继续进入秒杀检查。译文沿袭了英文的边界误述。

此边界在快照内可核验，但 DLC 目标版本未固定，故不升级为目标版本的已确认缺陷。

### C15 | entry-03633 | 仅建议

“global speed／整体速度”的情况与 C05 相同：机制含义没有直接译错；冻结 preferred 行的 `scope=core` 不足以单独证明本 DLC 条目违反明确适用的命名要求。

这是名称一致性建议，与本条另一个已确认的语义遗漏分开计算。

### C16 | entry-03633 | 存在问题

原文“reacts **faster and better to aggressions**”，译文为“全凭本能行动，**反应速度更快**”。

译文保留了速度提升，但没有保留“对攻击／侵扰作出反应”的对象，以及“应对得更好”这一独立于快慢的描述。“全凭本能行动”不能完整承载这两项信息。

证据：冻结原文及 `S/data/talents/misc/races.lua:427–429`。本项为叙述信息遗漏，不主张存在未显示的额外战斗数值。

### C17 | entry-03643 | 存在问题

原文“the pain of **its victim**”译为“**牺牲者**的痛苦”，改变了受害者与施害者之间的关系，并引入了牺牲意味。

`S/data/timed_effects.lua:466–483` 的语境是内在触手吸取受伤目标的生命；回调在目标已死亡时直接退出。这里的 victim 是受到其伤害的对象，文本和机制都不要求其成为牺牲者。属于角色关系的语义偏移。

### C18 | entry-03645 | 存在问题

原文明确叙述目标“**briefly saw what True Horror means**”，译文只保留“被真正的恐惧吓倒”，遗漏了短暂目睹、领略真恐怖这一事件。

冻结邻文 `context.lua:365` 将状态称为“一瞥真惧”；`S/data/timed_effects.lua:555–563` 的状态名、说明及获得日志也共同指向“看见”。技能失败几率保留正确，但这项叙述信息仍有遗漏。

### C19 | entry-03646 | 待确认

原文引用“**Hideous Visions**”，译文引用“**失智冲击**”；冻结邻文 `context.lua:398` 将 Hideous Visions 称为“惊骇幻象”。仅按名称对照存在不一致，但不能据此直接确认错译。

实际消费链如下：

- `S/data/timed_effects.lua:741–754`：黑暗低语在心灵尖啸状态下增加幻象生成几率，并产生额外时空伤害。
- `D/data/talents/demented/madness.lua:118–134`：幻象死亡后的额外时空伤害位于 `T_SANITY_WARP` 条件分支内。
- 同文件 163–175 行：该技能名为 **Sanity Warp**，作用是幻象死亡时产生伤害爆发。

因此“失智冲击”可能是在按实现纠正英文的技能归属。冻结材料没有提供 **Sanity Warp ↔ 失智冲击** 的名称映射，且 DLC 目标版本未固定；需要这两项证据才能裁定。此前名称不一致的表面观察不作为已确认错误。

### C20 | entry-03651 | 待确认

原文与译文都宣称所选目标会“**die in its place／代替它死亡**”。

快照 `S/data/timed_effects.lua:1716–1738` 在即将承受致命伤害时，先治疗自身，再向所选位置投射等于本次伤害量的 `VOID` 伤害，随后调用 `on_fatebreaker_call` 并取消自身本次伤害。本体 `T/game/modules/tome/data/damage_types.lua:2863–2869` 将 `VOID` 分成时空和暗影伤害；这条投射本身不是无条件处死。

因此“所选目标必定死亡”的保证尚未由完整调用链证实。缺少具体目标的 `on_fatebreaker_call` 行为和目标 DLC 版本映射，保留待确认，归为沿袭英文的疑点。

译文新增的治疗说明另行核对无误：1719–1729 行先读取并消耗自身幸运，再由目标不幸的层数**覆盖**治疗量并消耗不幸；不是两者相加。

实际读取材料与边界记录如下。为避免重复长目录，以下前缀与相对路径组合即完整路径。

```text
B=/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923

A=/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults
```

| 实际读取路径 | 版本／核验 |
|---|---|
| `B/INPUT.md` | 本次冻结入口，v3-source |
| `B/entries.json` | 本次冻结的 entry-03613–entry-03652，共40条 |
| `B/context.lua` | 本次允许的冻结邻文 |
| `B/source-access.json` | 本次源码白名单及哈希清单 |
| `B/sources/dlc/cults/tome-cults/data/talents/demented/void.lua` | SHA-256 匹配，前缀 `19cb982e3487` |
| `B/sources/dlc/cults/tome-cults/data/talents/demented/writhing-body.lua` | SHA-256 匹配，前缀 `37c7c1f3ebe5` |
| `B/sources/dlc/cults/tome-cults/data/talents/misc/misc.lua` | SHA-256 匹配，前缀 `3b37fe925ecb` |
| `B/sources/dlc/cults/tome-cults/data/talents/misc/races.lua` | SHA-256 匹配，前缀 `59b9b67cb0a3` |
| `B/sources/dlc/cults/tome-cults/data/timed_effects.lua` | SHA-256 匹配，前缀 `0d3139ebf8a4` |
| `A/tome-cults/data/damage_types.lua` | SHA-256 匹配，前缀 `6ec5f1659e60` |
| `A/tome-cults/data/talents/demented/friend-of-the-worm.lua` | SHA-256 匹配，前缀 `e8c4508aa632` |
| `A/tome-cults/data/talents/demented/madness.lua` | SHA-256 匹配，前缀 `33e274b4e1f1` |

以下本体文件均只通过 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取，未读取当前源码工作树：

- `/workspace/t-engine4/game/modules/tome/class/Actor.lua`
- `/workspace/t-engine4/game/modules/tome/class/NPC.lua`
- `/workspace/t-engine4/game/modules/tome/data/damage_types.lua`
- `/workspace/t-engine4/game/engines/default/engine/Actor.lua`
- `/workspace/t-engine4/game/engines/default/engine/GameEnergyBased.lua`

追加源码的调用链来源：

| 追加文件 | 已读入口 |
|---|---|
| DLC `data/damage_types.lua` | 巨石的 `DamageType.MESMERIZE` 投射 |
| DLC `friend-of-the-worm.lua` | `WTW_TERRIBLE_SIGHT`、`WTW_SHARED_INSANITY` 状态及对应技能 |
| DLC `madness.lua` | `DARK_WHISPERS.on_timeout` 调用 `T_HIDEOUS_VISIONS.hideous_vision` |
| 本体 `class/Actor.lua` | DLC 的 Actor 引用、`canBe` 与 `on_act` 消费 |
| 本体 `class/NPC.lua` | 巨石、巨口定义中的 `require "mod.class.NPC"` |
| 本体 `data/damage_types.lua` | Fatebreaker 的 `DamageType.VOID` 投射 |
| 本体 `engine/Actor.lua` | `mod.class.Actor` 中的明确 require／继承调用 |
| 本体 `engine/GameEnergyBased.lua` | `NPC.act` 注释明确指定的 `tickLevel` 调度入口 |

三次单文件定位未取得内容：固定 commit 下的 `engine/Actor.lua`、`game/modules/tome/ai/dumb_talented.lua`、`game/modules/tome/data/ai/dumb_talented.lua` 不存在。第一项随后定位到上述实际路径；AI 文件未继续扩大搜索，相关缺口已写入 C09。

未创建临时文件，未修改仓库，未读取其他报告或当前译文，未创建子 agent；没有发现越界读取。首次默认沙箱启动失败后，读取通过只读命令执行。以上是独立审核观察，不是生产完成认证。
