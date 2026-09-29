| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03693 | 存在问题 | C01：遗漏立即吞食的时序 |
| entry-03694 | 存在问题 | C02：遗漏立即吞食的时序 |
| entry-03695 | 未发现问题 | 饥饿、攻击行为及对象对应 |
| entry-03696 | 未发现问题 | 标签附加于 greater ego 名称，语境成立 |
| entry-03697 | 存在问题 | C03、C04：人物所属信息遗漏；侦察情报变成目击 |
| entry-03698 | 未发现问题 | 注册、绑定及错误提示对应；仅作文本核验 |
| entry-03699 | 待确认 | C05：“上传”是否适用于该提示全部调用场景 |
| entry-03700 | 未发现问题 | 在线传输失败、重试提示及占位符对应 |
| entry-03701 | 未发现问题 | 离线传输及占位符对应 |
| entry-03702 | 未发现问题 | 最近存入、等待后移除的条件对应 |
| entry-03703 | 未发现问题 | 最近存入、等待后移除的条件对应 |
| entry-03704 | 未发现问题 | 成就标题含义及省略号表达成立 |
| entry-03705 | 未发现问题 | 职业与装备两个同名对象区分正确 |
| entry-03706 | 未发现问题 | 敌人、复活对象及拯救对象对应 |
| entry-03707 | 未发现问题 | 属性与数值对应；existing 不构成强制改名依据 |
| entry-03708 | 未发现问题 | 每级生命加值及正负号对应 |
| entry-03709 | 未发现问题 | 每级生命加值对应 |
| entry-03710 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03711 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03712 | 未发现问题 | 负生命加值保留 |
| entry-03713 | 未发现问题 | 三项属性及数值对应 |
| entry-03714 | 存在问题 | C06：遗漏伤害增益的全部类型范围 |
| entry-03715 | 未发现问题 | 三项属性及数值对应 |
| entry-03716 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03717 | 未发现问题 | 每级生命加值对应 |
| entry-03718 | 未发现问题 | 经验惩罚及百分数对应 |
| entry-03719 | 未发现问题 | 三个天赋名称语义对应，无适用的强制译名冲突 |
| entry-03720 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03721 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03722 | 未发现问题 | 每级生命加值对应 |
| entry-03723 | 未发现问题 | 经验惩罚及百分数对应 |
| entry-03724 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03725 | 未发现问题 | 三项属性、数值及正负号对应 |
| entry-03726 | 未发现问题 | 每级生命加值对应 |
| entry-03727 | 未发现问题 | 经验惩罚及百分数对应 |
| entry-03728 | 未发现问题 | 两个技能类别、两项入门技能及参数对应 |
| entry-03729 | 存在问题 | C07–C11 已确认；C12 为机制适用性待确认 |
| entry-03730 | 存在问题 | C13、C14：钥匙刻字范围及地点邻近信息遗漏 |
| entry-03731 | 存在问题 | C15–C19：启动、基座、面板及显示针动作误译或遗漏 |
| entry-03732 | 存在问题 | C20–C25：面板、家庭、视角、船员及射击后果信息失真 |

以下源码简记：`S` 为本输入目录的 `sources/dlc`；`A` 为 `source-access.json` 许可的 `abc20-20260923/sources/orcs`。两者均是哈希核验通过的 DLC 快照，**源码仓库、commit 及目标版本适用性未固定**。文本直接可证的结论与机制待确认项分别列出。

### C01 | entry-03693 | 存在问题

原文“**promptly swallows and eat Melinda**”；译文“吃下了梅琳达”。

状态：**confirmed，时序信息遗漏**。“吃下了”保留吞食结果，但没有表达立即发生。证据为冻结文本及 `S/cults/tome-cults/overload/mod/class/CultsDLC.lua:353`：该文本作为寄生兽替换后的对话选项显示，绑定 `good_meal()`。此结论不依赖推断游戏耗时。

### C02 | entry-03694 | 存在问题

原文“**promptly swallows and eat Aeryn**”；译文“吃下了艾琳”。

状态：**confirmed，时序信息遗漏**。与上一条相同，立即吞食这一叙事信息没有保留。证据：`S/cults/tome-cults/overload/mod/class/CultsDLC.lua:358`，对应艾琳对话替换选项。

### C03 | entry-03697 | 存在问题

原文“**Protector Myssil of Zigur**”；译文“守护者米歇尔”。

状态：**confirmed，人物所属信息遗漏**。后文的“伊格附近”描述废墟位置，并未表达写信者来自或属于伊格。证据：`S/cults/tome-cults/superload/mod/class/Game.lua:59`；整封信由 `simpleLongPopup` 显示，`%s` 在第69行消费为玩家名字。

### C04 | entry-03697 | 存在问题

原文“**From what the scouts can tell**”；译文“侦察员看见”。

状态：**confirmed，信息来源被强化**。原文仅归因于侦察员掌握或判断出的情报，没有说明他们亲眼看见绑架过程；译文增加了目击事实。证据：同文件第63行，属于弹窗信件正文。

### C05 | entry-03699 | 待确认

原文“**sent to the Item’s Vault**”；译文“上传到共享仓库”。

状态：**pending**。“上传”限定为网络传送，而许可语境中同一组件同时存在在线与离线存入提示：`context.lua:167`、`:170`。尚不知道本条是否仅在在线存入后出现，还是两条路径共用。

缺失证据：`ItemsVaultDLC.lua` 中本字符串的调用位置及在线／离线分支关系。`items-vault` 已列为源码不可用；不能据此确认误译。

### C06 | entry-03714 | 存在问题

原文“**increase all their damage**”；译文“增加伤害”。

状态：**confirmed，作用范围信息遗漏**。译文保留增伤，却未明确原文强调的全部伤害范围。

证据：DLC 种族描述 `S/orcs/tome-orcs/data/birth/races/orc.lua:115`，第125行授予 `T_ORC_FURY`。固定本体 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 中：

- `game/modules/tome/data/talents/misc/races.lua:731`：施加 `EFF_ORC_FURY`，持续3回合。
- `game/modules/tome/data/timed_effects/mental.lua:1999`、`:2007`：效果说明明确全部伤害，激活时写入 `inc_damage` 的 `all` 增益。

这是原文范围信息的遗漏；不将本体 commit 视为 DLC 的版本固定依据。

### C07 | entry-03729 | 存在问题

原文“**lumps of metal**”；译文“铁块”。

状态：**confirmed，材料范围被缩窄**。金属不限于铁，译文将产物指定成了某一种金属。文本证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`。

快照辅助证据：`A/tome-orcs/superload/mod/class/Actor.lua:299` 的 `transmoInven` 按物品材质等级构造材料 ID，并调用 `collectIngredient`，没有在这个分支把所有金属固定成铁。这里不凭材料 ID 推断各等级具体名称。

### C08 | entry-03729 | 存在问题

原文“**infusions into herbs**”；译文“将纹身转化为植物”。

状态：**confirmed，产物类别信息丢失**。“植物”没有保留 herbs 所指的草药类别。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`；这是物品处理结果说明，并非泛指自然植物的叙事。

### C09 | entry-03729 | 存在问题

原文“**which are used to craft tinkers**”；译文无对应内容。

状态：**confirmed，用途信息遗漏**。材料与制造蒸汽工具的关系完全消失，玩家得不到收集这些产物的用途说明。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`。

快照中的 `A/tome-orcs/overload/mod/class/interface/PartyTinker.lua:81` 也显示 `canMakeTinker` 会检查配方所需材料；此处仅辅助解释用途，不扩大到具体配方结论。

### C10 | entry-03729 | 存在问题

原文“**when you destroy items**”；译文“你可以选择使用它或者转化之盒”。

状态：**confirmed，操作适用情境遗漏**。原文限定的是销毁物品时选择处理工具，译文没有交代这个选择针对什么操作。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:49`，位于加粗的操作说明内。

### C11 | entry-03729 | 存在问题

原文“**You can choose the default one by using it**”；译文“使用它则设置为默认使用”。

状态：**confirmed，选择行为被写成自动结果**。原文说使用后可以选择默认工具；译文承诺使用即完成设置，省去了选择这一操作。证据为冻结文本及 `S/orcs/tome-orcs/data/chats/aaf.lua:49`。具体运行条件另列 C12。

### C12 | entry-03729 | 待确认

原文“**with no items to destroy**”；译文“在里面没有物品时”。

状态：**pending，目标版本中的条件适用性未固定**。

允许快照内已证事实：`A/tome-orcs/data/general/objects/quest-artifacts.lua:43` 的 `use_power.use` 先统计背包内标记待处理的物品；数量为零后，第52行还检查脚下物品。只有地面也为空、且具备多个处理工具时，第55行才弹出确认框；第56行在确认回调中设置默认工具。有地面物品时，第62行询问是否熔解它们。

因此，该快照中的“里面没有物品”不足以保证进入默认工具选择。缺失的是此 DLC 快照与目标版本的对应证据；不能将这项机制差异直接提升为目标版本已确认缺陷。上游英文也未详述多工具前提，这部分不能归为翻译新增。

### C13 | entry-03730 | 存在问题

原文“**etched into one**”；译文“一串钥匙，上面写着‘毁灭号’”。

状态：**confirmed，刻字所属范围遗漏**。原文明确刻在其中一把钥匙上，译文没有保留这一限定。证据：`S/orcs/tome-orcs/data/chats/destructicus-lead.lua:21` 的 `welcome` 对话正文。

### C14 | entry-03730 | 存在问题

原文“**just south of Kruk Pride**”；译文“克鲁克部落南边”。

状态：**confirmed，地点邻近信息遗漏**。南方方向保留，但紧邻南侧的定位信息丢失。证据：同文件第22行的前往地点说明。这是轻微的信息遗漏，不只是措辞偏好。

### C15 | entry-03731 | 存在问题

原文“**whirrs to life**”；译文“启动了它的生命”。

状态：**confirmed，动作语义误译**。原文描述机器伴随运转声启动，译文把惯用表达中的 life 当作被启动的“生命”，且未保留声音信息。证据：`S/orcs/tome-orcs/data/chats/destructicus.lua:37`；此前第30行已明确对象是武器装置。

### C16 | entry-03731 | 存在问题

原文“**its base slightly rotating underneath you**”；译文“它的基座开始运转”。

状态：**confirmed，具体动作与空间关系遗漏**。原文包含脚下基座轻微旋转；“开始运转”仅表示工作状态，未表达旋转、幅度及位于玩家下方。证据：同文件第37行，`welcome2` 正文。

### C17 | entry-03731 | 存在问题

原文“**a strange beaded panel**”；译文“一块奇怪的珍珠板”。

状态：**confirmed，构造被误作材质**。beaded 描述珠状或颗粒状构造，不指定珍珠材质；后续同句明确是磁力驱动的显示针形成图像。证据：同文件第37行，不需要外推装置的真实制造材料。

### C18 | entry-03731 | 存在问题

原文“**slides in front of you**”；译文“从你前方滑过”。

状态：**confirmed，移动关系改变**。语境是面板滑至玩家面前供其查看，译文写成从面前经过。后续第46行继续显示面板上的观察画面，支持其作为面前显示设备的语境。

### C19 | entry-03731 | 存在问题

原文“**pins pushing out and pulling back**”；译文“针伸了出来”。

状态：**confirmed，显示动作遗漏**。原文明确伸出与回缩共同形成图像；译文只剩伸出，后接“被电磁力量控制”也没有表达回缩。证据：同文件第37行。

### C20 | entry-03732 | 存在问题

原文“**The beaded panel**”；译文“珍珠面板”。

状态：**confirmed，构造被误作材质**。这是上一条叙事中的同一显示面板，仍把 beaded 无依据地具体化为珍珠。证据：`S/orcs/tome-orcs/data/chats/destructicus.lua:46`，并由第37行的磁力显示针说明提供前文语境。

### C21 | entry-03732 | 存在问题

原文“**Steam Giant families huddle and weep**”；译文“蒸汽巨人们拥挤而哭泣”。

状态：**confirmed，人物群体关系遗漏**。家庭群体变成不加区分的巨人群，丢失了撤离者以家庭聚集的叙事信息。证据：同文件第46行；第48行继续交代飞船正在撤离部族残余成员。

### C22 | entry-03732 | 存在问题

原文“**The view pans around the cabin**”；译文“视角切换到船舱”。

状态：**confirmed，观察动作改变**。原文是视野在船舱内扫动；此前已经显示飞船内部。译文改成切换到船舱这一地点转换。证据：同文件第46行前后连续叙述。

### C23 | entry-03732 | 存在问题

原文“**crew members hurrying between the captain’s quarters and the engine room**”；译文“一些成员匆忙走过船长室和引擎室”。

状态：**confirmed，人物身份及移动关系失真**。船员身份没有明确保留，尤其是“在两处之间奔忙”被改成“经过两处”。证据：同文件第46行；这段是在描述飞船撤离中的船员活动。

### C24 | entry-03732 | 存在问题

原文“**flying in the air near nothing of importance**”；译文“在空中无害地飞舞”。

状态：**confirmed，环境信息被替换为行为评价**。原文说明小鬼附近没有重要目标，译文却说它的飞行动作无害；两者不等价。附近环境解释了向它开火为何较少造成附带影响。证据：同文件第50行。

### C25 | entry-03732 | 存在问题

原文“**Firing on it would have little effect whatsoever**”；译文“向他开火没什么意义”。

状态：**confirmed，后果描述变成价值判断**。原文谈开火造成的影响有限，译文谈这件事没有意义。后半句保留展示威力的用途，仍不能补回对后果大小的说明。证据：同文件第50行及紧随其后的两个射击选择。

实际读取路径与版本如下。为避免重复长路径，定义：

- `P`＝`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923`
- `A`＝`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/orcs`

冻结输入：

- `P/INPUT.md`
- `P/entries.json`
- `P/context.lua`
- `P/source-access.json`

本组源码，全部与 `source-access.json` 的 SHA-256 匹配：

- `P/sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua`
- `P/sources/dlc/cults/tome-cults/overload/mod/dialogs/FontSacrifice.lua`
- `P/sources/dlc/cults/tome-cults/superload/mod/class/Game.lua`
- `P/sources/dlc/orcs/tome-orcs/data/achievements/special.lua`
- `P/sources/dlc/orcs/tome-orcs/data/achievements/story.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/empyreal.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/tinker.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/orc.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/whitehooves.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/yeti.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/aaf.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua`

追加 DLC 源码，全部在白名单内且哈希匹配：

| 路径 | 已读调用或符号来源 |
|---|---|
| `A/tome-orcs/data/general/objects/quest-artifacts.lua` | `aaf.lua:55` 明确加载此文件并创建 `APE` |
| `A/tome-orcs/superload/mod/class/Actor.lua` | APE 使用函数调用 `who:transmoInven` |
| `A/tome-orcs/overload/mod/class/interface/PartyTinker.lua` | 分解逻辑调用 party 材料接口，核查其制造材料消费关系 |
| `A/tome-orcs/data/talents/misc/races.lua` | 种族描述中的 `race/whitehooves`、`T_WHITEHOOVES` 及列出的天赋；同时检查 `T_ORC_FURY` |

本体源码仅通过 `/workspace/t-engine4` 的 `git show` 读取，统一固定 commit 为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`：

- `game/modules/tome/data/talents/misc/races.lua`：追踪种族授予的 `T_ORC_FURY`。
- `game/modules/tome/data/timed_effects/physical.lua`：沿 `EFF_ORC_FURY` 查找，未找到该定义。
- `game/modules/tome/data/timed_effects/mental.lua`：继续追踪同一效果，找到激活与移除逻辑。

共覆盖40条：**8条存在问题、1条待确认、31条未发现问题**。未发现占位符、显示标记或 `@playername@` 丢失；所有条目的 `args_order`、`special` 均为冻结的空值。未把合法标点、段落排版或 existing 术语差异单独判为缺陷。

无法完成的核验限于 items-vault 调用逻辑及 DLC 目标版本对应关系。未创建临时文件、子 agent，未修改仓库，未读取其他报告或越界材料。本输出为独立审核观察，不是生产完成认证。
