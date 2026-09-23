已复核全部 40 条并裁决 82 项观察：**8 条 ISSUE、1 条 PENDING、31 条 OK；归并为 28 项确认缺陷**。OK 包含仅措辞或排版建议。

以下源码简称对应文末实际读取路径；DLC 均为哈希核验通过的公开快照，**源码 commit 及目标版本对应关系未固定**。确认缺陷依据冻结原译与完整文本语境；依赖 DLC 运行机制适用性的结论另列 P，不混入 D。

| entry-ID | 判定 | canonical D／P 编号或简短依据 |
|---|---|---|
| entry-03693 | ISSUE | D01：遗漏迅速吞食的信息 |
| entry-03694 | ISSUE | D02：遗漏迅速吞食的信息 |
| entry-03695 | OK | 攻击动作、对象及颜色标记保留 |
| entry-03696 | OK | FontSacrifice:151 将后缀附于高级词缀名称 |
| entry-03697 | ISSUE | D03–D06：所属、情报来源、消息性质及贬称 |
| entry-03698 | OK | 完整仓库语境不足以证明新增独立手动存储要求 |
| entry-03699 | PENDING | P01：“上传”是否用于离线分支未知 |
| entry-03700 | OK | 在线传输错误、重试要求及 `%s` 保留 |
| entry-03701 | OK | 离线传输、对象占位符保留 |
| entry-03702 | OK | 刚存入及等待后取出条件保留 |
| entry-03703 | OK | 同上；未据缺失源码臆断实际等待机制 |
| entry-03704 | OK | 字面意义成立；文化引用译法仅建议 |
| entry-03705 | OK | 同名职业和武器的区分合理 |
| entry-03706 | OK | 对手、复活目标及拯救对象保留 |
| entry-03707 | OK | 三项属性、数值和标记对应 |
| entry-03708 | OK | 每级生命加值与 `+0` 对应 |
| entry-03709 | OK | 生命加值 2；快照 `copy_add.life_rating=2` |
| entry-03710 | OK | 三项属性及数值对应 |
| entry-03711 | OK | 三项属性及数值对应 |
| entry-03712 | OK | 生命加值 −1；快照定义对应 |
| entry-03713 | OK | 属性修正与快照 `stats` 对应 |
| entry-03714 | ISSUE | D07：全部伤害的明确范围遗漏 |
| entry-03715 | OK | 三项属性及数值对应 |
| entry-03716 | OK | 三项属性及数值对应；existing 术语不强制改名 |
| entry-03717 | OK | 生命加值 12 与种族定义对应 |
| entry-03718 | OK | 12% 与快照 `experience=1.12` 对应 |
| entry-03719 | OK | 三个天赋名称语义成立；句号仅排版建议 |
| entry-03720 | OK | 三项属性及数值对应 |
| entry-03721 | OK | 三项属性及数值对应 |
| entry-03722 | OK | 生命加值 14 与种族定义对应 |
| entry-03723 | OK | 15% 与快照 `experience=1.15` 对应 |
| entry-03724 | OK | 三项属性及数值对应 |
| entry-03725 | OK | 三项属性及数值对应 |
| entry-03726 | OK | 生命加值 13 与种族定义对应 |
| entry-03727 | OK | 12% 与快照 `experience=1.12` 对应 |
| entry-03728 | OK | 两类技能、两项初始天赋及 `%s` 消费对应 |
| entry-03729 | ISSUE | D08–D11；另有 P02、P03 |
| entry-03730 | ISSUE | D12–D14：刻字对象、刻字方式、地点邻近关系 |
| entry-03731 | ISSUE | D15–D19：启动、基座、面板及显示针动作 |
| entry-03732 | ISSUE | D20–D28：构造、家庭关系、动作及目标影响 |

确认缺陷表中的“翻译新增”均指**相对于英文新增的偏差或遗漏**，不表示由本次标点修改首次引入。本次未确认需要归因为沿袭上游机制错误的 D 项。

| D-ID | entry-ID | 内容、归因及源码／语境证据 |
|---|---|---|
| D01 | entry-03693 | 翻译新增遗漏：`promptly` 的迅速、立即意味未在“吃下了”中表达。CultsDLC:350–354，寄生兽替换选项；不据此推断游戏耗时。 |
| D02 | entry-03694 | 同类遗漏，独立覆盖艾琳条目。CultsDLC:355–359。 |
| D03 | entry-03697 | 翻译新增遗漏：`Myssil of Zigur` 丢失所属关系。Game:59；标题及废墟位置没有表达写信者的所属。 |
| D04 | entry-03697 | 翻译新增强化：`From what the scouts can tell` 变成“侦察员看见”，增加亲眼目击的证据性质。Game:63；“可能”只修饰实验目的。 |
| D05 | entry-03697 | 翻译新增语义变化：`grave news` 说明消息严重，“令人震惊”改为接收者的惊讶反应，两者不等价。Game:61–63。 |
| D06 | entry-03697 | 翻译新增遗漏：对死灵法师的贬称 `filth` 消失。Game:66；前文“肮脏的奥术势力”修饰不同对象，未补回此处侮称。 |
| D07 | entry-03714 | 翻译新增遗漏：`all their damage` 只剩“伤害”，失去明确的全范围限定；不据此声称译文限定为物理伤害。orc:115、125；本体 talents/misc/races:731 → timed_effects/mental:2007 的 `inc_damage={all=eff.power}`。 |
| D08 | entry-03729 | 翻译新增缩窄：`lumps of metal` 变成“铁块”。aaf:47；APE:28–29 同样泛称金属及矿块。无需依赖具体各级材料名称即可确认。 |
| D09 | entry-03729 | 翻译新增泛化：材料语境的 `herbs` 变成“植物”，丢失草药类别。aaf:47；Actor:304–308 为辅助快照证据。 |
| D10 | entry-03729 | 翻译新增遗漏：`which are used to craft tinkers` 无对应译文。aaf:47；APE:29、PartyTinker:81–83、114–117 辅助说明制造材料的用途与消费。 |
| D11 | entry-03729 | 翻译新增遗漏：未说明在 `when you destroy items` 的操作中选择处理工具。aaf:49 的加粗说明；前句介绍分解用途不等于保留这一操作适用条件。 |
| D12 | entry-03730 | 翻译新增遗漏：刻字位于一串钥匙中的 `one` 把这一所属限定消失。destructicus-lead:21。译文并未明确断言每把都有字。 |
| D13 | entry-03730 | 翻译新增细节遗漏：`etched` 的刻制方式未保留于“写着”。destructicus-lead:21；不反向断言译文一定指用笔书写。 |
| D14 | entry-03730 | 翻译新增遗漏：`just south` 的近处定位只剩“南边”。destructicus-lead:22。 |
| D15 | entry-03731 | 翻译新增误译：`whirrs to life` 是伴随嗡鸣启动，译为“启动了它的生命”，同时丢失声音信息。destructicus:30、37，明确为机械装置。 |
| D16 | entry-03731 | 翻译新增遗漏：`slightly rotating underneath you` 的旋转、幅度与空间关系，被笼统“开始运转”替代。destructicus:37。 |
| D17 | entry-03731 | 翻译新增具体化：`beaded panel` 被译作“珍珠板”，把珠状构造具体化为珍珠。destructicus:37 的显示针说明不支持该材质判断。 |
| D18 | entry-03731 | 翻译新增动作变化：面板滑至玩家面前，译成“从你前方滑过”。destructicus:37、44–53；后续继续观看并切换该面板目标。 |
| D19 | entry-03731 | 翻译新增遗漏：显示针 `pushing out and pulling back` 只剩伸出，丢失回缩动作。destructicus:37。 |
| D20 | entry-03732 | 翻译新增具体化：再次把同一 `beaded panel` 译成“珍珠面板”。destructicus:37、46。 |
| D21 | entry-03732 | 翻译新增遗漏：`Steam Giant families` 变成无家庭关系限定的“蒸汽巨人们”。destructicus:46、48 的撤离叙事。 |
| D22 | entry-03732 | 翻译新增动作泛化：`huddle` 的聚拢、挤成团动作变成“拥挤”状态；哭泣保留。destructicus:46。 |
| D23 | entry-03732 | 翻译新增动作变化：`pans around the cabin` 是在舱内扫视，译成切换到船舱。destructicus:46，此前已经显示飞船内部。 |
| D24 | entry-03732 | 翻译新增身份遗漏：`crew members` 只剩“成员”。destructicus:46 在家庭、守卫之后另述船员，不能把船上所有成员视为船员。 |
| D25 | entry-03732 | 翻译新增路径变化：`hurrying between` 两个舱室变成“走过”两处。destructicus:46；不额外要求原文必然表示多次往返。 |
| D26 | entry-03732 | 翻译新增替换：`near nothing of importance` 的周围无重要事物，变成“无害地飞舞”的行为评价。destructicus:50；52–53 给出两个射击对象。 |
| D27 | entry-03732 | 翻译新增语义变化：`would have little effect` 的影响有限变成“没什么意义”的价值判断。destructicus:50；后面的炫耀威力和低伤害描述没有完整保留前一命题。 |
| D28 | entry-03732 | 独立补充遗漏：`pausing to take worried glances` 包含奔忙中停下来张望，译文“偶尔忧虑地瞥向”只表达频率，未保留停下动作。destructicus:46。 |

下表按观察的**实际断言**裁决。某项原标“仅建议”但实际指出可证信息损失，仍记 confirmed；mixed 中分别交代被接受与未接受的部分。

| O-ID | 状态 | 命中 D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | confirmed | D01 | CultsDLC:353；迅速意味确实遗漏，动作结果正确不能豁免时序信息。 |
| O002 | confirmed | D01 | 同上；不是仅要求逐词直译，而是缺少对应的动作速度信息。 |
| O003 | confirmed | D01 | 冻结原译及 CultsDLC:353 支持；不推断回合耗时。 |
| O004 | confirmed | D01 | CultsDLC:350–354 支持该叙事遗漏。 |
| O005 | confirmed | D02 | CultsDLC:358；结果保留不等于信息无损。 |
| O006 | confirmed | D02 | 艾琳选项中的 `promptly` 无对应表达。 |
| O007 | confirmed | D02 | CultsDLC:355–359 支持。 |
| O008 | confirmed | D02 | 同上；即时意味与吞食结果分别判断。 |
| O009 | confirmed | D03 | Game:59、62；写信者所属与废墟位置是不同关系。 |
| O010 | confirmed | D03 | Game:59、69；整封信显示，所属确实遗漏。 |
| O011 | confirmed | D03 | 标题“伊格的紧急事件”没有补回写信者所属。 |
| O012 | confirmed | D03 | 接受 `of Zigur` 遗漏；不依赖观察附加的领袖身份断言。 |
| O013 | confirmed | D04 | Game:63；事实结论相同仍不能把情报判断改成目击。 |
| O014 | confirmed | D04 | 后半句“可能”没有限定“看见”。 |
| O015 | confirmed | D04 | 冻结文本直接支持信息来源被强化。 |
| O016 | mixed | D06 | confirmed：`filth` 贬称消失；advisory：`True Wrath` 的强调可由整句愤怒表达承载，不独立计 D。 |
| O017 | mixed | D05、D06 | confirmed：严重消息变为震惊消息、侮称遗漏；advisory：`True` 的修辞强调。 |
| O018 | refuted | — | context:130–146 已交代玩家通过仓库存放服务器物品；“需要你存储”不足以证明注册绑定之外新增独立手动操作。主体表达可更精确，但所述误导未证实。 |
| O019 | pending | — | P01；context:162、167、170 有在线／离线语境，缺字符串实际调用分支。 |
| O020 | pending | — | P01；不能仅因同文件含离线日志便断定此提示用于离线。 |
| O021 | pending | — | P01；items-vault 源码明确不可用。 |
| O022 | advisory | — | special:136–159 与邻近成就名支持文化引用讨论；直译本身成立，不把具体电影归属当缺陷证据。 |
| O023 | confirmed | D07 | 明确的 `all` 范围未保留；本体效果实现提供辅助证据。 |
| O024 | confirmed | D07 | orc:115、125 → 本体 races:731 → mental:2007；仅确认范围遗漏，不将本体 commit 套用于 DLC。 |
| O025 | advisory | — | whitehooves:118；末尾句号不改变列表内容。获准天赋文件能确认三个英文名称，未发现具体译名冲突证据。 |
| O026 | advisory | — | aaf:25–28、35；两类技能、两项天赋及 `npc.name` 对应，逗号属排版。 |
| O027 | confirmed | D08 | aaf:47、APE:29 均未限定为铁。 |
| O028 | confirmed | D08 | 文本已足够确认缩窄；Actor:299–302 仅辅助说明按材质等级分档。 |
| O029 | confirmed | D10 | aaf:47 的制造用途从句无译文。观察行号不准，以实际源码行号为准。 |
| O030 | confirmed | D09 | aaf:47 材料语境中，植物没有保留草药类别。 |
| O031 | confirmed | D09 | 同上；不是单纯更自然的同义词选择。 |
| O032 | confirmed | D11 | aaf:49 中销毁物品时的选择情境遗漏。 |
| O033 | confirmed | D10 | aaf:47；PartyTinker:81–83 辅助支持材料用于制造。 |
| O034 | confirmed | D10 | 用途从句整体消失，合并为同一 D。 |
| O035 | confirmed | D08 | 文本缩窄成立；快照确按 `material_level` 选择材料 ID，但不据 ID 推断具体材质名。 |
| O036 | mixed | D08、D09 | confirmed：金属缩成铁、草药泛化；pending：具体钢／矮人钢／沃瑞钽及注射药剂用途旁证未核实，见 P03。 |
| O037 | confirmed | D11 | aaf:49 支持操作适用情境遗漏。 |
| O038 | pending | — | P02；APE:45–62 确有背包标记与地面两步检查，目标版本适用性缺证。 |
| O039 | confirmed | D10 | aaf:47、APE:29 支持用途遗漏；Actor:304–308 辅助确认材料分支。 |
| O040 | mixed | — | refuted：“APE 不能称内部存物”的前提被 APE:28、41、76 的界面用语反证；pending：地面及确认分支适用性见 P02。背包有物品也不等于有 `__transmo` 物品。 |
| O041 | advisory | — | aaf:49 保留了通过使用来设默认的操作目的；译文没有明确写“自动、无需确认”。APE:55–57 的弹窗可支持更精确说明，不能仅据“则”认定排除了确认。 |
| O042 | mixed | D11 | confirmed：销毁物品的操作情境遗漏；advisory：在明确二选一语境下，“需要／可以”的措辞差异不另计缺陷。运行前提适用性仍见 P02。 |
| O043 | pending | — | P02；快照的地面检查属实，但不能直接提升为目标版本已确认机制错误。 |
| O044 | pending | — | P02；版本缺口判断正确，多工具前提也是英文未详述的内容。 |
| O045 | mixed | D09 | confirmed：草药类别泛化不能降为偏好；refuted：`infusions` 译“纹身”构成问题的可能性，没有支持。其局部 C 编号不用于跨观察归并。 |
| O046 | mixed | D12 | confirmed：“其中一把”限定遗漏；refuted：“上面”必然断言整串每把都有刻字，译文未作该排他断言。 |
| O047 | advisory | — | destructicus-lead:23；漏句末感叹号未破坏句法或标记闭合，不足以证明错误显示。 |
| O048 | advisory | — | destructicus-lead:21 的急切等待语境下，“焦急”可表达迫切等待；未充分证明新增独立忧虑事实。 |
| O049 | mixed | D12、D13 | confirmed：特定钥匙限定及刻制细节丢失；advisory：eagerly／焦急的情绪措辞。 |
| O050 | confirmed | D12 | 原文明确一把，译文仅指整串上的文字。 |
| O051 | advisory | — | 观察已承认“焦急等待”的急切用法；可作语气优化。 |
| O052 | confirmed | D14 | destructicus-lead:22；南侧方向与紧邻南侧并不等价。 |
| O053 | mixed | D12、D13 | confirmed：刻字所属和方式遗漏；advisory：“应该”已保留建议语气，不要求逐译 probably；感叹号属排版。 |
| O054 | confirmed | D16 | destructicus:37；一般运转未保留旋转及身下位置。 |
| O055 | confirmed | D15、D16 | 启动习语误译与基座动作遗漏是两个独立缺陷。实际位置为 destructicus:37。 |
| O056 | confirmed | D18 | destructicus:37、46 的持续观察语境支持滑至面前。 |
| O057 | confirmed | D17、D18 | 珍珠材质具体化与滑过动作分别成立；不额外认定装置的真实制造材料。 |
| O058 | confirmed | D15 | 机械启动被写成启动“生命”，并遗漏运转声。 |
| O059 | confirmed | D19 | destructicus:37；回缩动作没有被“电磁力量控制”补回。 |
| O060 | confirmed | D19 | 同上；不需要把装置扩张描述为现实中特定三维显示技术。 |
| O061 | confirmed | D16 | 旋转、幅度、身下位置都在该动作短语中。 |
| O062 | confirmed | D18 | 后文仍以面板观察目标，支持动作关系偏差；无需断言滑过后永远离开。 |
| O063 | mixed | D15、D16、D17、D19 | confirmed：前四组具体语义偏差；advisory：“磁力／电磁力量”的措辞不据现有语境判错。标记及专名核对通过。 |
| O064 | confirmed | D17 | beaded 未指定珍珠材质；显示针语境支持构造性理解。 |
| O065 | confirmed | D18 | destructicus:37、46 支持面板滑至观察位置。 |
| O066 | confirmed | D19 | 同一显示动作遗漏，合并 D19。 |
| O067 | confirmed | D21 | 家庭群体身份未在泛指巨人中表达。 |
| O068 | confirmed | D26 | destructicus:50；周围目标信息被换成行为评价。无需推测译者如何产生错误。 |
| O069 | confirmed | D24 | 船员与前面的家庭、守卫分述，泛指成员不能完整保留身份。 |
| O070 | confirmed | D24、D25 | crew 身份和 between 路径分别失真；不把英文扩成必然多次往返。 |
| O071 | confirmed | D26 | 附近没有重要事物与小鬼无害不是同一命题。 |
| O072 | confirmed | D26 | 环境说明遗漏成立；原文没有说附近绝对空无一物，不采纳该扩大表述。 |
| O073 | advisory | — | 原译仍有换行，句子和论述顺序完整；少一个空行不足以证明信息结构或渲染损坏。 |
| O074 | confirmed | D21、D22 | 家庭关系与聚拢动作分别遗漏；不将家庭身份直接扩大为全体都是平民的机制断言。 |
| O075 | confirmed | D20 | destructicus:46 延续同一面板的珍珠具体化。 |
| O076 | confirmed | D24、D25 | 人物身份、移动路径分开归并；未借用同条其他问题。 |
| O077 | mixed | D23 | confirmed：舱内扫视变成切换地点；advisory：空行及小鬼“他／它”不构成已证显示或指代错误。 |
| O078 | confirmed | D21 | destructicus:46、48 的家庭撤离语境支持。 |
| O079 | confirmed | D23 | 已显示飞船内部后继续扫视，与切换到船舱不同。 |
| O080 | confirmed | D24、D25 | 同一观察同时命中身份与路径两个 D。 |
| O081 | confirmed | D26 | 环境命题与行为评价不同；附近不重要不等于完全空无一物。 |
| O082 | confirmed | D27 | destructicus:50；影响大小被改成意义大小。后续“浪费射击”的措辞支持低实用价值，却不能抹去本句对影响的说明。 |

未决事项与主要分歧处理：

- **P01｜entry-03699**：缺少 `ItemsVaultDLC.lua` 中该提示的实际调用位置，无法判断是否覆盖离线仓库。仅凭相邻日志不能确认“上传”错误。
- **P02｜entry-03729**：允许快照中，APE:45–57 先统计背包内 `__transmo` 物品，再检查脚下物品，并在多处理工具条件下显示确认弹窗；地面有物品则进入 :62 的熔炼询问。缺少快照与目标版本的对应证据，因此具体运行差异保留 pending。多工具前提未详述属于英文也存在的简化；不能全部归为翻译新增。“APE 内的物品”则是源码自身采用的界面表达。
- **P03｜entry-03729，O036 的辅助断言**：未核实所列各级具体材质名称及草药用于注射药剂的具体配方。已读 Actor 分支证明按材料等级构造 ID，不能单凭 ID 证明这些名称和用途。这不影响 D08、D09 的直接文本判定。
- **新增漏项**：D28 未被 82 项观察提出；D22 从 O074 的复合叙述中单独拆出。未以重复次数或入口末尾的既有汇总作为证据。
- 全 40 条的 `%s`、`@playername@`、颜色及样式标记序列一致；`args_order`、`special` 全为冻结空值。没有发现可证的运行时格式缺陷。未将 existing 术语记录转为强制全局改名要求。

实际读取路径如下。令：

`P = /home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923`

`A = /home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/orcs`

冻结输入：

- `P/ADJUDICATION-INPUT.md`
- `P/INPUT.md`
- `P/entries.json`
- `P/context.lua`
- `P/source-access.json`

本组源码，13 个文件全部核对 SHA-256：

- `P/sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua`（CultsDLC）
- `P/sources/dlc/cults/tome-cults/overload/mod/dialogs/FontSacrifice.lua`（FontSacrifice）
- `P/sources/dlc/cults/tome-cults/superload/mod/class/Game.lua`（Game）
- `P/sources/dlc/orcs/tome-orcs/data/achievements/special.lua`（special）
- `P/sources/dlc/orcs/tome-orcs/data/achievements/story.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/empyreal.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/tinker.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/orc.lua`（orc）
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/whitehooves.lua`（whitehooves）
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/yeti.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/aaf.lua`（aaf）
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua`（destructicus-lead）
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua`（destructicus）

追加源码均在白名单内且哈希匹配：

- `A/tome-orcs/data/general/objects/quest-artifacts.lua`（APE）：由 aaf:55 的明确加载路径引入。
- `A/tome-orcs/superload/mod/class/Actor.lua`（Actor）：由 APE:68、81 的 `who:transmoInven` 调用引入。
- `A/tome-orcs/overload/mod/class/interface/PartyTinker.lua`（PartyTinker）：沿材料进入 party 后的制造用途核验，检查 `canMakeTinker`／`makeTinker` 的材料消费。
- `A/tome-orcs/data/talents/misc/races.lua`：由 whitehooves:126–128 的 `race/whitehooves`、`T_WHITEHOOVES` 及其列举天赋引入。

本体仅通过 `/workspace/t-engine4` 的 `git show` 读取固定提交 **`624a67329fe2ad440c5b344785a9c73fcf22ae63`**：

- `game/modules/tome/data/talents/misc/races.lua`：由 orc:125 的 `T_ORC_FURY` 引入。
- `game/modules/tome/data/timed_effects/mental.lua`：由前文件 :731 的 `EFF_ORC_FURY` 引入。

未修改仓库，未创建临时文件或子 agent，未查找模型身份、来源映射、其他报告或其他轮答案。本结果为独立审查裁决，不是生产完成认证。
