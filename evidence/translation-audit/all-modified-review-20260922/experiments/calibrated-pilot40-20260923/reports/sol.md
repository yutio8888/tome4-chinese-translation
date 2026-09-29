# 40 条独立复核报告

本轮仅审阅冻结的 40 条译文及允许的语境、术语和源码材料；未修改文件，也未读取其他审核报告。表中的 **ISSUE** 是本轮确认的译文问题，**PENDING** 表示关键事实仍无法判定，**OK** 表示未发现足以确认的问题。兽人 DLC 源码是哈希匹配但未固定提交的快照；附身者 DLC 源码缺失。因此，下列文本结论不等于已确认其适用于某个实际安装版本。

| 序号 | 条目 | 结论 | 复核要点 |
|---:|---|---|---|
| 01 | entry-03778 | OK | 生命上限、生命下限及数值与调用一致。 |
| 02 | entry-03788 | ISSUE | “附近敌人”扩大成“周围生物”；见 C01。 |
| 03 | entry-03814 | OK | 日志主语、物品参数和目标标记保留。 |
| 04 | entry-03817 | OK | “一次走 3 格”与说明及移动回调相容。 |
| 05 | entry-03824 | OK | 译文忠实于英文日志；英文与实现的范围差异另记 C18。 |
| 06 | entry-03830 | PENDING | `sessali` 是否应译为“延龄草”缺少可判定依据；见 C02。 |
| 07 | entry-03844 | OK | 长篇广告的信息结构和标记可对应；个别戏谑词的译法不足以确认缺陷。 |
| 08 | entry-03846 | ISSUE | “超过 40%”及“最高四年”两处数值限定丢失；见 C03–C04。 |
| 09 | entry-03847 | ISSUE | 录音开头、喝茶条件、行程状态有意义变化；见 C05–C07。 |
| 10 | entry-03848 | ISSUE | `posterity` 误作“繁荣”，并给声音添加“血液”来源；见 C08–C09。 |
| 11 | entry-03855 | OK | 通读整封信后，抽签、交易、校准与威胁的主要关系仍在。 |
| 12 | entry-03863 | ISSUE | “不能直接干预”的主体被改为说话者一方；见 C10。 |
| 13 | entry-03869 | ISSUE | 添加灾害归因、漏掉观察时间，并反转 `invasive` 的关系；见 C11–C13。 |
| 14 | entry-03876 | OK | 战役结局中的因果和专名基本对应。 |
| 15 | entry-03880 | ISSUE | 放置“引爆器”变成安装“炸弹”；见 C14。 |
| 16 | entry-03885 | OK | 伤害、负能量递减、上限及占位参数保留。 |
| 17 | entry-03886 | OK | 射程、抵达传送及速度说明对应。 |
| 18 | entry-03895 | ISSUE | 返程距离上限被说成折返前的飞行距离；见 C15。 |
| 19 | entry-03907 | ISSUE | “所有敌人”扩大成“所有单位”；见 C16。 |
| 20 | entry-03928 | OK | 外骨骼承伤和修复比例对应。 |
| 21 | entry-03929 | OK | 参数顺序与冻结的 `args_order` 对应；英文两处时长说明的差异另记 C19。 |
| 22 | entry-03945 | OK | 日志参数和底盘名称保留。 |
| 23 | entry-03947 | OK | “强制攻击”措辞偏强，但原文 `provokes ... to attack it` 也表达引导攻击；不足以单独确认译错。 |
| 24 | entry-03948 | OK | 冲锋、尾锯、嘲讽及属性替代关系对应。 |
| 25 | entry-03964 | OK | 范围、回合、技能失败率和蒸汽强度对应。 |
| 26 | entry-03982 | OK | `(known)` 作为列表后缀时，前导空格和颜色标记均保留。 |
| 27 | entry-03988 | OK | 炮台分类、数值占位和效果结构对应；“获得最大生命值”措辞可改进，但上下文可读作增加。 |
| 28 | entry-03989 | OK | 守卫炮台、伤害转移及技能名与相邻译文对应。 |
| 29 | entry-03999 | OK | “全属性（力量除外）”在此主属性语境下可成立。 |
| 30 | entry-04031 | OK | 熔铁血液的状态日志对应。 |
| 31 | entry-04036 | OK | “受到额外伤害”可表达全来源承伤增加；不据此判定范围丢失。 |
| 32 | entry-04067 | OK | 火焰药膏的三种 affinity 与使用设备保留；术语候选的 `source_tag` 不适用于本条，不能仅凭候选强制改名。 |
| 33 | entry-04068 | OK | 静水药膏同上；效果类型与冻结源码对应。 |
| 34 | entry-04073 | OK | 传送门的不确定性、目的地与地名可对应。 |
| 35 | entry-04103 | OK | UI 数值参数和“蒸汽强度”对应。 |
| 36 | entry-04113 | OK | 放置炸弹前不能回归的条件对应。 |
| 37 | entry-04120 | OK | 等级生命加值和 `-4` 保留；附身者源码不可用。 |
| 38 | entry-04128 | ISSUE | 整句关于“存在本身侵扰敌人心智”的铺垫被删，并把既有联系改写为主动链接；见 C17。 |
| 39 | entry-04133 | OK | 灵能网、收存身体、阶级及类型参数保留；附身者实现未核。 |
| 40 | entry-04144 | OK | 技能等级不足及对本体、克隆的永久选择对应；附身者实现未核。 |

## 原子观察

以下源码路径均相对于指定实验目录中的 `sources/dlc/orcs/tome-orcs/`。每项“目标适用性待定”均指兽人 DLC 的实际目标提交未固定；它不降低已能直接从冻结英汉文本确认的译文结论。

**C01｜entry-03788｜confirmed。** 原文：“`confusing nearby enemies`”；译文：“`混乱周围生物`”。敌人被扩大为生物，可能让读者以为友方也在混乱范围内。最强反证是“周围生物”可在战斗叙述中泛指敌人，但此处没有该限定。**text_status：确认译文扩大对象；snapshot_fact：英文说明及触发代码已核；target_applicability：实际 DLC 版本待定；impact：装备效果理解。** 证据：`data/general/objects/tinkers/chemistry.lua:284`、`:301–315`。

**C02｜entry-03830｜pending。** 原文：“`stack of herbs (sessali)`”；译文：“`一束植物（延龄草）`”。若 `sessali` 是延龄草的游戏内称谓，译文可成立；若是另一种草药，名称便错误。冻结源码只给出名称及 `herb_sessali.png`，不能确定植物身份。**text_status：待确认；snapshot_fact：名称和图标路径已核；target_applicability：实际 DLC 版本及植物身份待定；impact：材料识别。** 证据：`data/ingredients.lua:73–79`；[context.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/calibrated-pilot40-20260923/context.lua) 中另一个“entity name”语境也沿用“延龄草”，但重复译法不能证明物种。

**C03｜entry-03846｜confirmed。** 原文：“`reduce the amount of power drawn from the geothermal system by over 40%`”；译文：“`减少40%来自地热系统的消耗`”。“超过”这一数量界限丢失。最强反证是整段仍传达显著节能，但 `40%` 与 `over 40%` 的阈值不同。**text_status：确认数值限定缺失；snapshot_fact：海报原文已核；target_applicability：实际 DLC 版本待定；impact：叙事中的量化信息。** 证据：`data/lore/emporium.lua:86`。

**C04｜entry-03846｜confirmed。** 原文：“`up to four years in prison, per tank`”；译文：“`每违法售出一罐将遭受最高3000金币罚金，并处四年监禁`”。“最高”只修饰罚金，监禁被写成固定四年。最强反证是读者可能把“最高”顺带读到整项处罚，但中文句法没有明确支持这种读法。**text_status：确认刑期上限信息丢失；snapshot_fact：海报原文已核；target_applicability：实际 DLC 版本待定；impact：世界观文本的处罚信息。** 证据：`data/lore/emporium.lua:88`。

**C05｜entry-03847｜confirmed。** 原文：“`"...thing on? Okay, good.`”；译文：“`“……什么事？好，好的。`”。录音开头是在确认设备是否开启，译文变成询问发生了什么。最强反证是英文句首残缺；但后接录音自报身份和结尾 `End log`，设备检查是更强的上下文解释。**text_status：确认场景动作改变；snapshot_fact：同篇录音上下文已核；target_applicability：实际 DLC 版本待定；impact：叙事场景理解。** 证据：`data/lore/gem.lua:20–32`。

**C06｜entry-03847｜confirmed。** 原文：“`Councillor Tantalos is getting his tea as soon as he can un-kick the hornet's nest that got us into this chaos`”；译文：“`坦塔洛斯议员还他妈的想喝茶，要不是他刚刚给我们捅了个大马蜂窝，把我们搞的一团糟`”。原文以“先收拾烂摊子，才有茶喝”回击命令；译文只说他制造了麻烦。最强反证是讽刺和愤怒语气仍在，但取得茶的条件确实不在。**text_status：确认条件关系缺失；snapshot_fact：同篇对话已核；target_applicability：实际 DLC 版本待定；impact：人物语气与因果。** 证据：`data/lore/gem.lua:28–32`。

**C07｜entry-03847｜confirmed。** 原文：“`projected journey to the Loyalist's last known position is underway`”；译文：“`正在准备前往忠诚者的上一个位置`”。`is underway` 表示行程已在进行，“正在准备前往”表示尚未出发。最强反证是译文前一句已有“我们的出发时间很准时”，可让读者推断已出发；紧接的“准备前往”仍直接改变当前状态。**text_status：确认时间状态改变；snapshot_fact：录音原文已核；target_applicability：实际 DLC 版本待定；impact：剧情时间线。** 证据：`data/lore/gem.lua:32`。

**C08｜entry-03848｜confirmed。** 原文：“`"...for posterity!`”；译文：“`“……为了繁荣！`”。`posterity` 指后世，与下一句“让未来世代听到”相连；“繁荣”改变目的。最强反证是后一句译文补回“子孙后代铭记”，可修复读者对整体意图的理解，但不能让开头的错误词义成立。**text_status：确认局部误译、段落有部分语境修复；snapshot_fact：连续两句已核；target_applicability：实际 DLC 版本待定；impact：叙事措辞。** 证据：`data/lore/gem.lua:39`。

**C09｜entry-03848｜confirmed。** 原文：“`Gurgling.`”；译文：“`血液流淌之声。`”。原文是咕噜声，没有指定来自血液；译文添加了声音来源。最强反证是尖叫和暴力场面可能让人联想到血，但这仍是推测。**text_status：确认增添未经原文支持的细节；snapshot_fact：舞台音效串已核；target_applicability：实际 DLC 版本待定；impact：叙事画面，较低。** 证据：`data/lore/gem.lua:49`。

**C10｜entry-03863｜confirmed。** 原文：“`Some want the Kruk exterminated, others imprisoned. Neither can afford direct intervention`”；译文：“`有些人想消灭克鲁克兽人，也有人想监禁他们。不论是那种，我们都没法直接介入`”。`Neither` 承接前面的两派；“我们”将无力直接介入的主体变为发言者一方。最强反证是谈话中“我们”也可能泛指相关各方，但此处由蒸汽议员发言，通常指其阵营。**text_status：确认主体关系改变；snapshot_fact：议会对话已核；target_applicability：实际 DLC 版本待定；impact：政治情节。** 证据：`data/lore/palace-fumes.lua:98–100`。

**C11｜entry-03869｜confirmed。** 原文：“`The damage left in the Scintillating Caverns, in Norgos' Lair, and in countless other places has only now become clear`”；译文：“`人们终于开始正视魔法大爆炸对那里所造成的伤害`”。原文没有把这些地点的损害归因于魔法大爆炸；译文给出明确原因。最强反证是世界观可能支持这种背景解释，但冻结段落未作此断言。**text_status：确认译文添加因果；snapshot_fact：传单原文已核；target_applicability：实际 DLC 版本待定；impact：世界观叙述。** 证据：`data/lore/primal-forest.lua:54`。

**C12｜entry-03869｜confirmed。** 原文：“`write down where you explored, when, and how many of these species you saw`”；译文：“`记录下各种观察到的生物的分布和数量`”。地点和数量可从“分布和数量”读出，观察时间没有对应信息。最强反证是“在四处探索”可暗示某次记录，但没有记录“何时”。**text_status：确认观察要求缺项；snapshot_fact：完整学习与观察段已核；target_applicability：实际 DLC 版本待定；impact：文本给出的操作信息。** 证据：`data/lore/primal-forest.lua:58`。

**C13｜entry-03869｜confirmed。** 原文：“`if one becomes endangered or invasive`”；译文：“`如果有一种生物濒临灭绝或受到入侵`”。`invasive` 指该物种成为入侵物种；“受到入侵”使它成了受害者。最强反证是读者可能从生态段落猜到“入侵物种”，但文字的施受关系相反。**text_status：确认生态关系反转；snapshot_fact：同段已核；target_applicability：实际 DLC 版本待定；impact：文本论点。** 证据：`data/lore/primal-forest.lua:58`。

**C14｜entry-03880｜confirmed。** 原文：“`You place the detonator`”；译文：“`你成功安装了炸弹`”。放置的对象从引爆器变成炸弹。最强反证是玩家此举确实启动爆破，口语可概称“安装炸弹”；但弹窗标题也是 `Cave Detonator`，此处具体对象明确。**text_status：确认物件替换；snapshot_fact：弹窗标题及调用已核；target_applicability：实际 DLC 版本待定；impact：任务操作提示，较低。** 证据：`data/quests/kruk-invasion.lua:76–81`。

**C15｜entry-03895｜confirmed。** 原文：“`The ball will travel at most %d distance to return to you.`”；译文：“`球体最多飞行 %d 然后折回你。`”。原文的上限约束返程，译文将上限放在“然后折回”之前。最强反证是可把整句勉强读成总行程上限，但“然后”的先后关系更直接地指向出程。源码把 `self:getTalentRange(t) * 4` 作为返程追踪射程。**text_status：确认方向与时序误导；snapshot_fact：说明及返程调用已核；target_applicability：实际 DLC 版本待定；impact：技能射程理解。** 证据：`data/talents/celestial/sol.lua:50–80`、`:99–103`。

**C16｜entry-03907｜confirmed。** 原文：“`the lightning propagates to all foes in radius %d`”；译文：“`闪电扩散，对半径 %d 码内的所有单位造成同样的伤害`”。敌方范围被扩大为全部单位。最强反证是玩家或许会按通常战斗习惯把“单位”理解为敌人，但该词本身也包括友方。源码投射参数设为 `friendlyfire=false`，与“所有单位”尤其不符。**text_status：确认目标范围扩大；snapshot_fact：说明与投射参数已核；target_applicability：实际 DLC 版本待定；impact：友方受伤风险判断。** 证据：`data/talents/psionic/action-at-a-distance.lua:186–197`、`:209–213`。

**C17｜entry-04128｜confirmed。** 原文：“`Your mere presence is a blight in your foes minds. Using this link you are able to reach out and steal a talent from a target.`”；译文开头：“`链接目标，偷取目标一个技能。`”。译文保留了偷取技能，却删去“存在本身侵扰敌人心智”的整句铺垫，并将由此形成的联系写成主动链接目标。最强反证是这句主要服务于氛围，后续功能描述仍完整；因此影响限于技能叙述，不能据此推断机制错误。**text_status：确认叙事信息删改；snapshot_fact：冻结英汉文本已核，附身者源码不可用；target_applicability：附身者实际来源待定；impact：技能叙述，较低。** 证据：[entries.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/calibrated-pilot40-20260923/entries.json) 的 `entry-04128`；相邻译文见 `context.lua`，不以其他组件的同名机制代替附身者源码。

**C18｜entry-03824｜advisory，属于英文源码自身与实现的差异。** 原文：“`teleports away all nearby creatures!`”；译文：“`传送走了周围的所有生物！`”。两者一致。实现先以 `"hostile"` 收集半径 1 内目标，且逐个检查能否传送，因此日志的 `all nearby creatures` 比实现宽。最强反证是日志可作戏剧化概述；它仍不能证明译文引入了错误。**text_status：译文 OK；snapshot_fact：该快照的收集与传送循环已核；target_applicability：实际 DLC 版本待定；impact：英文原始日志可能夸大效果。** 证据：`data/general/objects/world-artifacts.lua:2245–2255`。

**C19｜entry-03929｜advisory，属于两处英文源码说明不一致。** 冻结原文：“`dazes affected enemies for 3 turns`”；译文：“`眩晕目标 3 回合`”，数值一致。最强反证是效果的另一处 `long_desc` 写 `dazing for 2 turns`；实际投射调用使用 `DamageType.LIGHTNING_DAZE`，仅凭本轮获准文件不足以判定运行时长。**text_status：译文 OK；snapshot_fact：技能说明为 3、效果说明为 2、投射调用已核；target_applicability：实际 DLC 版本及运行时长待定；impact：上游技能说明一致性。** 证据：`data/talents/steam/gadgets.lua:205–212`；`data/timed_effects/physical.lua:1151–1172`。

## 材料与版本界限

实际读取了指定实验目录下的 `INPUT.md`、`entries.json`、`context.lua`、`terms.json`、`source-access.json`、`FREEZE.json`，以及 `source-access.json` 列出的全部 **25 个兽人 DLC 主源码文件**（`data/general/objects/` 下 3 个、`data/ingredients.lua`、`data/lore/` 下 5 个、`data/quests/` 下 2 个、`data/talents/` 下 8 个、`data/timed_effects/physical.lua`、`data/tinkers/therapeutics.lua`、`data/zones/gates-of-morning/grids.lua`、`overload/mod/class/OrcCampaign.lua`、`superload/mod/class/Actor.lua`）。冻结的五个输入文件和这 25 个主源码文件的 SHA-256 均与清单匹配。未读取额外源码、其他实验臂或既往报告。

清单给出了单独的 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，本轮未读取 engine 文件；兽人 DLC 快照未固定源码提交。附身者四条没有可用的对应源码，故其实现层判断仍受限。本报告是只读研究观察，**不宣称 `DONE_VERIFIED`**。
