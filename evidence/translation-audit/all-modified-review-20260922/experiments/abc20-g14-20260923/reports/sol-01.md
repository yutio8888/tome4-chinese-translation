以下是 `entry-03693` 至 `entry-03732` 的独立复核观察。表中恰好覆盖冻结顺序的 40 条；“存在问题”指译文中有可由冻结文本或所列源码核实的信息差异。DLC 快照的仓库与 commit 未固定，不能据此确认目标版本的机制适用性。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03693 | 存在问题 | C01：遗漏即时性 |
| entry-03694 | 存在问题 | C02：遗漏即时性 |
| entry-03695 | 未发现问题 | 攻击对象与动作吻合 |
| entry-03696 | 未发现问题 | 列表中的高级词缀标记吻合 |
| entry-03697 | 存在问题 | C03、C04：来信人身份、侦察证据 |
| entry-03698 | 存在问题 | C05：服务器存储的执行主体改变 |
| entry-03699 | 待确认 | C06：“上传”是否适用于该提示 |
| entry-03700 | 未发现问题 | 错误、在线仓库及 `%s` 保留 |
| entry-03701 | 未发现问题 | 离线仓库及 `%s` 保留 |
| entry-03702 | 未发现问题 | 近期放入与等待移除吻合 |
| entry-03703 | 未发现问题 | 近期放入与等待移除吻合 |
| entry-03704 | 未发现问题 | 标题含义吻合 |
| entry-03705 | 未发现问题 | 职业与武器的同名关系清楚 |
| entry-03706 | 未发现问题 | 击败对象和拯救范围吻合 |
| entry-03707 | 未发现问题 | 属性及数值吻合 |
| entry-03708 | 未发现问题 | 生命加值及数值吻合 |
| entry-03709 | 未发现问题 | 生命加值及数值吻合 |
| entry-03710 | 未发现问题 | 属性及数值吻合 |
| entry-03711 | 未发现问题 | 属性及数值吻合 |
| entry-03712 | 未发现问题 | 生命加值及数值吻合 |
| entry-03713 | 未发现问题 | 属性及数值吻合 |
| entry-03714 | 未发现问题 | 伤害增益与持续时间吻合 |
| entry-03715 | 未发现问题 | 属性及数值吻合 |
| entry-03716 | 未发现问题 | 属性及数值吻合 |
| entry-03717 | 未发现问题 | 生命加值及数值吻合 |
| entry-03718 | 未发现问题 | 经验惩罚及数值吻合 |
| entry-03719 | 未发现问题 | 三项天赋均列出 |
| entry-03720 | 未发现问题 | 属性及数值吻合 |
| entry-03721 | 未发现问题 | 属性及数值吻合 |
| entry-03722 | 未发现问题 | 生命加值及数值吻合 |
| entry-03723 | 未发现问题 | 经验惩罚及数值吻合 |
| entry-03724 | 未发现问题 | 属性及数值吻合 |
| entry-03725 | 未发现问题 | 属性及数值吻合 |
| entry-03726 | 未发现问题 | 生命加值及数值吻合 |
| entry-03727 | 未发现问题 | 经验惩罚及数值吻合 |
| entry-03728 | 未发现问题 | 两类技能树、两项技能及 `%s` 吻合 |
| entry-03729 | 存在问题 | C07–C10：材料、用途及默认设置条件 |
| entry-03730 | 存在问题 | C11、C12：刻字所属、等待情绪 |
| entry-03731 | 存在问题 | C13–C15：底座与面板的运动 |
| entry-03732 | 存在问题 | C16–C18：人物关系、身份及小鬼所处位置 |

### C01 | entry-03693 | 存在问题

原文“**promptly** swallows and eat Melinda”中的迅速动作，在“吃下了梅琳达”中消失。这是动作时序的遗漏，不影响被吃的对象。证据：`sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua:350–354`；该句是选择项，选择后的 `good_meal()` 执行动作。

### C02 | entry-03694 | 存在问题

与 C01 相同的时序遗漏分别发生在艾琳这一条：“**promptly** swallows and eat Aeryn”译为“吃下了艾琳”。证据：同一冻结源码 `CultsDLC.lua:355–359`。

### C03 | entry-03697 | 存在问题

“Protector Myssil **of Zigur**”译成“守护者米歇尔”，遗漏来信人的伊格所属信息。信件正文提到“伊格附近”，但不等于补回其身份。证据：`sources/dlc/cults/tome-cults/superload/mod/class/Game.lua:59–69`；整段作为信件弹窗显示。

### C04 | entry-03697 | 存在问题

“**From what the scouts can tell**”是侦察员据所得情报作出的判断；“侦察员**看见**他们被……带走”改成了亲眼目睹。后半句的“可能”只限定实验目的，未消除这处证据性质变化。证据：同一 `Game.lua:62–63`。

### C05 | entry-03698 | 存在问题

原文说功能需要在服务器存放数据（“**it needs to store things**”）；译文说“这项功能需要**你**在服务器上存储数据”，把存储动作归给玩家，可能使注册、绑定之外又显得需要玩家手动存储。此项是原译直接可证的主体变化；`items-vault` 源码缺失，未据此断言实际操作机制。语境证据：冻结 `INPUT.md` 的本条，以及 `context.lua:138–145`。

### C06 | entry-03699 | 待确认

原文仅称物品已“**sent to** the Item’s Vault”，译文称已“**上传到**共享仓库”。同一允许的相邻语境含在线和离线传输提示（`context.lua:160–169`），但缺少 `ItemsVaultDLC.lua` 的实际调用位置，无法确认这条通用提示是否也会在离线路径显示。所缺证据是该提示的触发分支；因此不判为已证实错误。

### C07 | entry-03729 | 存在问题

“metallic items into **lumps of metal**”译为“金属物品转化为**铁块**”，把不限定金属种类的产物限定成铁。相关物品说明又称其为“lumps of ore”。证据：`sources/dlc/orcs/tome-orcs/data/chats/aaf.lua:45–49`，以及其 `:55` 加载的哈希固定文件 `tome-orcs/data/general/objects/quest-artifacts.lua:27–30`。

### C08 | entry-03729 | 存在问题

“infusions into **herbs**”译为“纹身转化为**植物**”，遗漏产物是草药这一材料类别。证据：`aaf.lua:46–47`；这是原译直接可证的类别信息损失。

### C09 | entry-03729 | 存在问题

原文说明这些材料“**are used to craft tinkers**”，译文在材料转换后结束句子，遗漏制造蒸汽工具的用途。证据：`aaf.lua:46–49`。

### C10 | entry-03729 | 存在问题

原文是在“**no items to destroy**”时使用提取仪来选默认工具；译文限定为“**在里面没有物品**时”，未涵盖脚下仍有待处理物品的情况。实际 `use_power` 先检查背包中标记待处理的物品，再检查脚下物品；两处都为空才进入默认设置弹窗。证据：`aaf.lua:49–55` 所引入的 `tome-orcs/data/general/objects/quest-artifacts.lua:41–60`。

### C11 | entry-03730 | 存在问题

原文是一串钥匙中“**one**”把钥匙刻有 `DESTRUCTICUS`；“交给你一串钥匙，**上面**写着‘毁灭号’”把刻字归到整串钥匙，失去“其中一把”的所属关系。证据：`sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:20–23`。

### C12 | entry-03730 | 存在问题

“**eagerly waiting**”描述迫切期待见面；“**焦急地等待**”加入了忧虑情绪。两种等待状态不同，属于人物状态的改变。证据：同一 `destructicus-lead.lua:21`。

### C13 | entry-03731 | 存在问题

“its base **slightly rotating underneath you**”译成“它的基座开始运转”，遗漏底座在玩家身下轻微旋转这一具体动作。证据：`sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua:36–40`。

### C14 | entry-03731 | 存在问题

面板“**slides in front of you**”表示滑到玩家面前；“**从你前方滑过**”表示从面前经过，改变了面板最终所在位置。后续面板供玩家观看、选择目标。证据：`destructicus.lua:36–53`。

### C15 | entry-03731 | 存在问题

显示轮廓的针会“**pushing out and pulling back**”；译文只写“针伸了出来，被电磁力量控制”，遗漏缩回的运动，损失成像方式的一半信息。证据：`destructicus.lua:37`。

### C16 | entry-03732 | 存在问题

“Steam Giant **families** huddle and weep”译为“蒸汽巨人们拥挤而哭泣”，遗漏他们是家庭成员这一叙事情境。证据：`destructicus.lua:43–48`。

### C17 | entry-03732 | 存在问题

“a few **crew members**”译成“一些成员”，遗漏这些往返船长室与引擎室的人是船员。证据：`destructicus.lua:46`。

### C18 | entry-03732 | 存在问题

火焰小鬼是在空中飞行且“**near nothing of importance**”；“在空中**无害地**飞舞”遗漏周围没有重要目标这一空间事实，并把“附近无重要物”改成“小鬼无害”。这关系到射击该目标的附带影响。证据：`destructicus.lua:48–53`；下一选项分别指向飞船和小鬼。

### 读取范围与限制

- 冻结包中实际读取：`INPUT.md`、`entries.json`、`context.lua`、`source-access.json`。路径均位于 [`abc20-g14-20260923`](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923/INPUT.md) 所在目录。
- 实际读取并按 `source-access.json` 的 SHA-256 核对的本组 DLC 文件：`CultsDLC.lua`、`FontSacrifice.lua`、cults 的 `Game.lua`；orcs 的 `achievements/special.lua`、`achievements/story.lua`、`birth/classes/empyreal.lua`、`birth/classes/tinker.lua`、`birth/races/orc.lua`、`birth/races/whitehooves.lua`、`birth/races/yeti.lua`、`chats/aaf.lua`、`chats/destructicus-lead.lua`、`chats/destructicus.lua`。它们均是冻结包 `sources/dlc/` 下的对应 `sections` 路径。
- 额外读取并核对哈希的 orcs 快照文件：`tome-orcs/data/talents/misc/races.lua`，由 `birth/races/whitehooves.lua` 的种族天赋列表引入；`tome-orcs/data/general/objects/quest-artifacts.lua`，由 `chats/aaf.lua:55` 的 `require` 和 `APE` 查找引入。两者均在 `source-access.json` 的 `dlc_additional_sources.orcs` 清单内。
- 本体只读取固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的单文件 `game/modules/tome/data/talents/misc/races.lua`，由 orcs `birth/races/orc.lua:125` 的 `T_ORC_FURY` 引入；其 `:700–739` 用于核对 entry-03714 的伤害增益。该译文未据此发现明确问题。
- DLC 文件仅有哈希固定的公开快照，**源码仓库、commit 与目标版本适用性未固定**。`items-vault` 在冻结输入中列为不可用；C06 因缺其调用源码而待确认。没有读取其他报告、当前译文或越界材料；没有创建临时文件、修改仓库或创建子 agent。本结果是审核观察，不声称生产 `DONE_VERIFIED`。
