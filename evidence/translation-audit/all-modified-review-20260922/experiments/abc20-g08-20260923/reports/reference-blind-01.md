| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03453 | 未发现问题 | 爆炸中心及 `%s` 对应受击目标，颜色标记保留。 |
| entry-03454 | 存在问题 | C01、C02 |
| entry-03455 | 存在问题 | C03–C10；其中 C06 待确认，C10 仅建议。 |
| entry-03456 | 存在问题 | C11 |
| entry-03457 | 未发现问题 | 保留职业大类与恶魔使者的层级；未按 existing 术语强制改名。 |
| entry-03458 | 存在问题 | C12；另有 C13 待确认。 |
| entry-03459 | 未发现问题 | 解锁标题与种族名称完整。 |
| entry-03460 | 存在问题 | C14；另有 C15 待确认。 |
| entry-03461 | 未发现问题 | 属性比较标签对应 `artifact_power_obsidian`，未误作消耗资源。 |
| entry-03462 | 未发现问题 | 阅读禁忌之书的成就要求完整。 |
| entry-03463 | 未发现问题 | 三项属性及数值、正负号一致。 |
| entry-03464 | 仅建议 | C16 |
| entry-03465 | 待确认 | C17 |
| entry-03466 | 待确认 | C18 |
| entry-03467 | 未发现问题 | 三项属性及数值、正负号一致。 |
| entry-03468 | 仅建议 | C19 |
| entry-03469 | 待确认 | C20 |
| entry-03470 | 未发现问题 | 经验惩罚及 12% 保留。 |
| entry-03471 | 未发现问题 | 三项属性及数值、正负号一致。 |
| entry-03472 | 仅建议 | C21 |
| entry-03473 | 待确认 | C22 |
| entry-03474 | 未发现问题 | 经验惩罚及 15% 保留。 |
| entry-03475 | 仅建议 | C23 |
| entry-03476 | 未发现问题 | 接受拒绝并仍祝好运的对话功能保留。 |
| entry-03477 | 未发现问题 | “我在里面”承接救援者询问，是语境支持的明示。 |
| entry-03478 | 存在问题 | C24 |
| entry-03479 | 存在问题 | C25 |
| entry-03480 | 未发现问题 | 开袋时散发令人作呕烟雾的描述完整。 |
| entry-03481 | 存在问题 | C26 |
| entry-03482 | 未发现问题 | `%s`、颜色及增加 1 觉醒点与奖励分支对应。 |
| entry-03483 | 未发现问题 | `%s`、颜色及增加 1 技能树点与奖励分支对应。 |
| entry-03484 | 未发现问题 | `%s`、颜色及增加 1 职业技能点与奖励分支对应。 |
| entry-03485 | 未发现问题 | `%s`、颜色及增加 1 通用技能点与奖励分支对应。 |
| entry-03486 | 未发现问题 | `%s`、颜色及增加 3 属性点与奖励分支对应。 |
| entry-03487 | 未发现问题 | 控制球未响应的交互反馈完整。 |
| entry-03488 | 未发现问题 | 封闭状态及玩家认为可以打开的判断完整。 |
| entry-03489 | 未发现问题 | 封闭状态及玩家认为可以打开的判断完整。 |
| entry-03490 | 未发现问题 | 封闭状态及玩家认为可以打开的判断完整。 |
| entry-03491 | 未发现问题 | 绿色黏液状细胞及其所属生物、防御功能保留。 |
| entry-03492 | 未发现问题 | 颜色、接近玩家及配合生物体其他部分攻击的关系完整。 |

下文 `A/`、`C/` 分别指本包 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/`、`sources/dlc/cults/tome-cults/`；`A+/` 指清单授权的 Ashes 额外源码根下 `tome-ashes-urhrok/`。完整路径清单见文末。所有 DLC 证据均来自哈希匹配快照，**源码仓库及 commit 未固定**；涉及目标版本机制适用性的结论保留待确认。

### C01 | entry-03454 | 存在问题

原文：“3 arms”；译文：“三只手”。

这里直接描述恶魔的身体构造，原文计数对象是手臂，译文变成手，改变了明确的解剖部位。状态：**confirmed，文本事实错误**。证据：`A/data/zones/searing-halls/npcs.lua:73`，`mutilator.desc`。

### C02 | entry-03454 | 存在问题

原文：“ready to mutilate you”；译文：“准备切割你”。

原文表达使人残缺、残毁的行为结果；译文仅说明切割这一动作，同时将方式限定为切割，未保留残毁含义。状态：**confirmed，语义损失**。证据：同文件第 72、73 行，生物名称与实验性残害描述共同限定语境。

### C03 | entry-03455 | 存在问题

原文：“fighting against overwhelming odds”；译文：“与势不可挡的敌人战斗”。

原文描述己方处于压倒性劣势的战斗局面；译文转为敌人本身势不可挡的属性。前后文反复强调敌群和成群对手，不能将这种局面信息完全等同于敌人强大。状态：**confirmed，关系与语义偏移**。证据：`A/init.lua:31`。

### C04 | entry-03455 | 存在问题

原文：“feeding on the flames and suffering … to stay alive”；译文：“吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬”。

译文保留吸收和杀敌，却遗漏吸收这些力量用于维持自身生存的目的。状态：**confirmed，文本信息遗漏**。

证据：`A/init.lua:31`。快照中的补充机制证据为 `A/data/timed_effects.lua:179` 的 `CURSED_FLAMES.on_timeout`：调用 `eff.src:heal(eff.heal)`，随后恢复活力；该快照确有向来源提供治疗的消费逻辑，但其目标版本适用性未固定。

### C05 | entry-03455 | 存在问题

原文：“a squad of Fire Imps”；译文：“召唤火焰恶魔”。

原文明确是一队特定种类的小恶魔；译文泛化为火焰恶魔，遗漏小队规模及具体生物类别。状态：**confirmed，数量与对象信息遗漏**，不依赖强制专名译法。证据：`A/init.lua:32`；`A+/data/talents/corruptions/demonic-pact.lua:27`、第 314 行另可确认快照中存在独立的 `fire imp` 种子类型。

### C06 | entry-03455 | 待确认

原文：“Demons have persistent health”；译文：“恶魔具有更持久的生命值”。

疑点是将跨次召唤保留生命状态，表述为生命值更加持久、更加耐用。

快照证据：`A+/data/talents/corruptions/demonic-pact.lua:326` 的 `availableDemonSeed` 返回种子中已有的恶魔对象及当前生命值；`Bind Demon.action` 在第 788–815 行取该对象并传给 `setupDemonSummon`。后者位于 `A+/data/talents/corruptions/corruptions.lua:93`，没有将生命值重置为满值。复活分支另在 `demonic-pact.lua:935` 将生命设为最大生命的 15%。

状态：**pending**。快照内支持“生命状态保留”的解释；仍缺该 DLC 快照与目标版本的绑定证据，不能将此机制判断提升为目标版本已确认缺陷。

### C07 | entry-03455 | 存在问题

原文：“disposable necromancer skeletons”；译文：“死灵法师易碎的骷髅”。

`disposable` 说明可消耗、用后可替换的性质；“易碎”说明承伤脆弱。译文把资源管理上的比较改成了耐久性比较。状态：**confirmed，比较依据改变**。证据：`A/init.lua:32`，该句紧接恶魔生命状态与复活说明。

### C08 | entry-03455 | 存在问题

原文：“Shalore who've taken to the demonic alterations especially well”；译文：“那些被恶魔的力量所改变的永恒精灵”。

译文仅保留受到改造，遗漏这些精灵尤其适应恶魔改造的限定条件，扩大了这段种族说明所指人群。状态：**confirmed，限定信息遗漏**。证据：`A/init.lua:35`。

### C09 | entry-03455 | 存在问题

原文：“their metaphorical skulls”；译文：“他们的头骨”。

原文明示头骨是比喻性的战绩展示，译文删除这一性质，成为将敌人头骨悬挂到个人页面的直接陈述。状态：**confirmed，语义限定遗漏**。证据：`A/init.lua:40`，该项明确介绍成就和个人资料页。

### C10 | entry-03455 | 仅建议

原文：“all-new art”；译文：“全新的艺术”。

游戏地区介绍中，这一表达具有明显直译感。不过上下文仍能将它理解为地区的视觉艺术内容，没有足够证据认定具体功能或事实被改变。状态：**advisory，仅自然度意见**。证据：`A/init.lua:33`。

### C11 | entry-03456 | 存在问题

原文：“As you recover … splits … memories flood your mind”；译文：“当你醒来后……和主大陆分离的焦土……记忆渐渐涌来”。

原文将恢复、地块分裂和记忆猛然涌回写成同时发生的转折；译文变成醒来后发现分离已经完成，记忆再逐渐恢复。改变了事件时序和记忆恢复的速度。状态：**confirmed，叙事时序偏移**。证据：`A/overload/data/texts/intro-ashes-urhrok.lua:27`。这是冻结叙述本身可证的差异，不据此推断实际地图生成时序。

### C12 | entry-03458 | 存在问题

原文：“created many dark cults”；译文：“通过黑暗仪式”。

原文讲建立多个黑暗教团，译文讲举行仪式；组织被换成活动，“建立多个组织”的事实也随之消失。状态：**confirmed，对象与行为错误**。证据：`A/overload/data/texts/unlock-corrupter_demonologist.lua:22`。

### C13 | entry-03458 | 待确认

原文：“It does not regenerate, and can only be stolen from your foes”；译文：“不会自己回复，而必须从你的目标身上偷取”。

这项疑点主要**沿袭上游的绝对化说明**，不能归因于翻译新增。

固定本体 `game/modules/tome/class/Actor.lua:254` 将默认 `vim_regen` 设为 0，但第 602 行仍调用资源恢复；`game/modules/tome/data/resources.lua:147` 将活力绑定到 `vim_regen`。`ActorResource.lua:201` 的 `regenResources` 按恢复字段增加资源。DLC 快照的 `A+/data/talents/corruptions/demonic-pact.lua:214`、第 231 行则向特定戒指种子效果提供正的 `vim_regen`。

状态：**pending**。默认不恢复与任何情况下都不能恢复并不相同；快照存在例外，但目标 DLC 版本绑定缺失，故保留机制适用性待确认。

### C14 | entry-03460 | 存在问题

原文：“earned the right to make … characters”；译文：“魔化精灵应运而生”。

原文明示玩家取得创建该种族角色的权限；译文变成种族由此产生的叙述，遗漏了这段解锁通知最直接的玩家操作信息。状态：**confirmed，解锁结果遗漏**。证据：`A/overload/data/texts/unlock-race_doomelf.lua:20`、第 24 行，标题和正文共同构成种族解锁通知。

### C15 | entry-03460 | 待确认

原文：“Instant cast phase door”；译文：“使用加速技能，瞬间穿梭空间”。

疑点在于“加速技能”可能被理解为提高行动或移动速度，而原文强调瞬发位移。

`A+/data/talents/misc/races.lua:35` 的 `Haste of the Doomed` 设置 `no_energy=true`；`action` 在第 68 行执行 `teleportRandom`，第 73 行附加防御和抗性效果，同回合第二次使用在第 82 行扣除行动能量。这个快照中的对应技能并未提供速度增益。

状态：**pending**。快照内支持上述机制区分；仍缺 DLC 目标版本绑定，不能只凭名称 `Haste` 或此快照断言目标版本的技能分类。

### C16 | entry-03464 | 仅建议

原文：“+3 Magic”；译文：“+3 魔法”。

这里明确是六项属性中的一项。术语子集记录“Magic／魔力”，但状态为 `existing`，且标签为 `stat name`，本条为 `_t`，不足以据此判定强制术语违规。状态：**advisory，仅属性命名一致性意见**。证据：`C/data/birth/demented.lua:81` 的属性标题、第 83 行说明和第 87 行 `mag=3`。

### C17 | entry-03465 | 待确认

原文：“Life per level: +3”；译文：“每等级生命加值：+3”。

`C/data/birth/demented.lua:122` 实际增加 `life_rating=3`。固定本体 `Actor.lua:4020` 的升级逻辑还会调用 `getRankLifeAdjust`；该函数在第 1851 行依据等级和阶级缩放输入。因此，`+3` 并不普遍等于实际每级额外增加 3 点最大生命。

状态：**pending，上游标签精度疑点**。译文沿袭原文；目标 DLC 快照适用性未固定。

### C18 | entry-03466 | 待确认

原文：“Life per level: -4”；译文：“每等级生命加值：-4”。

`C/data/birth/demented.lua:175` 修改的是 `life_rating=-4`，随后仍经过固定本体 `Actor.lua:4020` 的生命成长计算，不能普遍解释为每级直接少 4 点最大生命。

状态：**pending，上游标签精度疑点**。不是翻译新增数值错误；缺 DLC 目标版本绑定。

### C19 | entry-03468 | 仅建议

原文：“+2 Magic”；译文：“+2 魔法”。

属性数值及其所指没有改变。与子集中的“魔力”存在命名差异，但该记录为 `existing`，不构成强制改名依据。状态：**advisory，仅一致性意见**。证据：`C/data/birth/drem.lua:31`、第 33 行及第 37 行 `inc_stats.mag=2`。

### C20 | entry-03469 | 待确认

原文：“Life per level: 12”；译文：“每等级生命加值：12”。

`C/data/birth/drem.lua:51` 设置的是基础 `life_rating=12`；固定本体 `Actor.lua:1851`、第 4020 行仍对其作等级与阶级调整，并非所有等级都固定增加 12 点最大生命。

状态：**pending，上游标签精度疑点**。数值转录正确，机制适用性缺 DLC 目标版本绑定。

### C21 | entry-03472 | 仅建议

原文：“-2 Magic”；译文：“-2 魔法”。

六属性列表的对象和数值明确，负号完整。与术语子集 existing 记录的区别仅作为命名一致性意见，不判强制术语错误。状态：**advisory**。证据：`C/data/birth/krog.lua:31`、第 33 行及第 38 行 `inc_stats.mag=-2`。

### C22 | entry-03473 | 待确认

原文：“Life per level: 13”；译文：“每等级生命加值：13”。

`C/data/birth/krog.lua:55` 设置 `life_rating=13`。实际消费者仍是固定本体 `Actor.lua:4020` 及 `getRankLifeAdjust`，不能将 13 当作所有等级固定的生命增量。该 DLC 文件第 34 行的注释也明确指出上游标签应称 life rating；结论依据是实际计算，并非仅凭注释。

状态：**pending，上游标签精度疑点**。目标 DLC 版本适用性尚未绑定。

### C23 | entry-03475 | 仅建议

原文：“feel like I have potential to grow”；译文：“觉得我的潜能增长了”。

译文偏抽象，原文更着重于感到自己有继续成长的潜力。不过这是接受属性奖励后的感想，没有承诺具体数值或新的成长机制，当前语境下不足以认定玩法信息错误。状态：**advisory，仅表达重心与自然度意见**。证据：`C/data/chats/godfeaster-malyu-escaped.lua:53` 跳转 `stats`，第 73 行显示该回应。

### C24 | entry-03478 | 存在问题

原文：“An object rolls from the sack”；译文：“一个物品……掉了出来”。

原文明确描述滚出，译文改成掉出，丢失并替换了物品的运动方式。状态：**confirmed，轻微但可直接核验的动作语义错误**。

证据：`C/data/general/events/digestive-sack.lua:107` 放置物品，第 108 行显示此日志。代码没有另外提供足以证明译文是在纠正上游动画描述的证据。

### C25 | entry-03479 | 存在问题

原文：“foe burst out”；译文：“敌人……掉了出来”。

原文描写敌人突然冲出，译文变成被动掉落，改变了出场动作及其突发性。状态：**confirmed，动作语义错误**。

证据：`C/data/general/events/digestive-sack.lua:109` 的守卫分支在附近放置敌方 actor，第 117 行显示此日志。它与上一条物品出现属于不同对象、不同动作的叙述。

### C26 | entry-03481 | 存在问题

原文：“already scavenged what you could understand and use”；译文：“已经找遍了你能理解和使用的东西”。

原文说明可利用物品已经搜取，译文只说明找过，未表达物品已经取得、此处可用资源已被搜取的结果。状态：**confirmed，完成结果遗漏**。

证据：`C/data/general/events/space-dwarf-ship.lua:62` 在 `searched_dwarf` 已设置时显示该消息；首次交互则在第 70 行通过 `addObject` 将物品加入背包，第 71 行设置该标记。快照中的消费逻辑与原文“已搜取”一致；文本遗漏本身不依赖 DLC 版本判定。

实际读取范围与版本如下。

本包根路径 `P`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g08-20260923
```

读取了以下冻结材料；40 条原文、译文及顺序已逐条核对一致：

```text
P/INPUT.md
P/entries.json
P/context.lua
P/source-access.json
```

读取了以下 21 个本组源码文件。每个文件均完成 SHA-256 校验，与 `source-access.json.files_sha256` 一致；均为 DLC 未固定仓库／commit 的快照：

```text
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/zones/searing-halls/npcs.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua
P/sources/dlc/cults/tome-cults/data/achievements/all.lua
P/sources/dlc/cults/tome-cults/data/birth/demented.lua
P/sources/dlc/cults/tome-cults/data/birth/drem.lua
P/sources/dlc/cults/tome-cults/data/birth/krog.lua
P/sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu-escaped.lua
P/sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu.lua
P/sources/dlc/cults/tome-cults/data/general/events/digestive-sack.lua
P/sources/dlc/cults/tome-cults/data/general/events/space-dwarf-ship.lua
P/sources/dlc/cults/tome-cults/data/general/grids/fonts.lua
P/sources/dlc/cults/tome-cults/data/general/grids/fortress-multiverse.lua
P/sources/dlc/cults/tome-cults/data/general/grids/godfeaster.lua
P/sources/dlc/cults/tome-cults/data/general/grids/maggot.lua
P/sources/dlc/cults/tome-cults/data/general/grids/slimy_godfeaster.lua
P/sources/dlc/cults/tome-cults/data/general/npcs/blobs.lua
```

额外 DLC 源码根路径 `D`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok
```

以下文件均属于 `dlc_additional_sources` 白名单，且读取前核对哈希一致：

| 实际路径 | 已读引用来源 |
|---|---|
| `D/tome-ashes-urhrok/data/talents/misc/races.lua` | `DemonologistsDLC.hookLoad:34` 的显式加载。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/corruptions.lua` | `DemonologistsDLC.hookLoad:35` 的显式加载。 |
| `D/tome-ashes-urhrok/data/birth/corrupted.lua` | `DemonologistsDLC.hookLoad:39` 的显式加载。 |
| `D/tome-ashes-urhrok/data/general/objects/world-artifacts.lua` | `DemonologistsDLC.hookEntityLoadList:47` 的显式加载；核对 Shadow Power 和手套描述。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua` | `corruptions.lua:153` 的显式加载；追踪种子召唤及生命保存。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/wrath.lua` | `corruptions.lua:162` 的显式加载，以及神器引用的 `T_OBLITERATING_SMASH`。 |

本体只通过 `/workspace/t-engine4` 的 `git show` 读取以下单文件，版本均为 **`624a67329fe2ad440c5b344785a9c73fcf22ae63`**：

| 源码路径 | 调用链或符号来源 |
|---|---|
| `game/modules/tome/class/Actor.lua` | 出生定义的 `life_rating`、已读源码的 Actor 调用及活力恢复字段，追踪实际消费者。 |
| `game/modules/tome/class/Player.lua` | `Actor` 中的 `game.player` 与升级逻辑，核对玩家的继承及 `fixed_rating`。 |
| `game/modules/tome/class/interface/PlayerStats.lua` | `Player.lua:27`、第 46 行显式引用；检查生命成长方法是否被覆盖，未找到相应覆盖。 |
| `game/engines/default/engine/interface/ActorResource.lua` | `Actor.lua:31` 的 `require` 及第 602 行 `regenResources()`。 |
| `game/modules/tome/data/resources.lua` | 已读 `vim_regen` 与 `ActorResource.defineResource`，核对活力资源的具体绑定。 |

未读取其他报告、当前翻译文件、其他语言答案、SPEC／STATE 或当前源码工作树；未创建子 agent、临时文件或修改仓库。默认沙箱首次启动失败后，仅以获准的只读命令完成访问。无读取范围越界；未能核验的主要限制是 DLC 快照与目标版本的绑定。以上为独立审核观察，不是生产完成认证。
