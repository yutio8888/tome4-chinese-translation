# 匿名源码核验与归并：40 条 / 61 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方61项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好61行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03614

### C01 | entry-03614 | 存在问题

原文为“**attempt to daze**”，译文为“对……敌人**施加眩晕**”，将尝试写成必然生效。`tome-cults/data/talents/demented/void.lua:242–245,279–281` 每半回合投射 `MESMERIZE`；由该符号追到额外源码 `tome-cults/data/damage_types.lua:105–116`，其中先检查目标能否受震慑，再设置眩晕效果。状态：**已证实的译文偏差**。



## O002 | entry-03614

### C01 | entry-03614 | 存在问题

原文明确说“**attempt to daze**”，译文为“每半回合……**施加眩晕2回合**”，没有保留“尝试”的限定，弱化了能否成功施加的不确定性。这是可直接对照的语义遗漏。

补充证据：`S/data/talents/demented/void.lua:242–257` 将召唤者法术强度传给 `MESMERIZE`；`D/data/damage_types.lua:106–114` 先检查 `target:canBe("stun")`，通过后才调用 `setEffect(EFF_DAZED, 2, ...)`。并非对范围内所有敌人无条件生效。



## O003 | entry-03614

### C01 | entry-03614 | 存在问题
- **原文与译文：** 原文是「it will **attempt to** daze enemies…」，译文是「每半回合对 %d 码范围内敌人施加眩晕2回合」。
- **问题：** 译文删掉了「attempt」，把一次需要过判定的尝试写成了必定生效。
- **源码证据：**
  - `void.lua:243-247`：on_act 投射 `MESMERIZE`，并带上 `apply_power`。
  - 由这次调用引入的 `tome-cults/data/damage_types.lua:105-116`：只在 `target:canBe("stun")` 成立时才施加 `EFF_DAZED`，并且带 `apply_power` 豁免对抗。免疫或豁免成功的目标不会被眩晕。
- **状态：** confirmed，来源未固定。



## O004 | entry-03614

### C02 | entry-03614 | 仅建议
- 「%d%% all resist」译作「全体抗性」。术语表里「全部抗性」那一行是 `_t` 面板标签，本条是 tformat，不属于明确适用的术语要求，只是用词统一方面的偏好。



## O005 | entry-03614

### C02 | entry-03614 | 待确认

原文与译文都宣称“**every half a turn／每半回合**”。

快照的 `S/data/talents/demented/void.lua:242–245` 在巨石 `on_act` 中投射眩晕并清空行动能量，召唤定义未设置双倍行动速度。本体 `T/game/modules/tome/class/Actor.lua:168–170、761–773` 的默认速度为 1，满足行动能量门槛才调用 `on_act`；`T/game/engines/default/engine/GameEnergyBased.lua:124–129` 按速度累积能量。

现有链条没有支持固定“半回合一次”的调度。这是**沿袭英文的频率疑点**；尚缺与目标 DLC 版本对应的完整初始化、运行调度证据，不能直接裁定目标版本中的实际间隔。



## O006 | entry-03616

### C01 | entry-03616 | 存在问题
- **原文短引**：`, #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#`
- **译文短引**：`，#CRIMSON#由于副手非空，该技能暂时被禁用#WHITE#`
- **问题具体内容**：作用对象与事实错误。技能 `Mutated Hand`（`T_MUTATED_HAND`）本身为被动技能（mode="passive"），其提供的物理强度加成与触手武器伤害增益并不受副手装备限制；只有在副手非空时，触手副手武器攻击无法触发（`canTentacleCombat` 为 false，`getTentacleCombat` 返回 nil）。原文主句为 `Your tentacle hand currently has those stats%s:`，谓语动词 `is currently disabled` 的逻辑主语是“你的副手触手”（tentacle hand），而非技能本身。译文将其译为“该技能暂时被禁用”，错误地扩大了禁用对象，误导玩家以为整个被动技能失效。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/demented/writhing-body.lua:62`（未固定快照）。该段文本在 `info` 函数中作为 `%s` 拼接至 `Your tentacle hand currently has those stats%s:\n%s`，判断条件为 `allow_tcombat and "" or _t", #CRIMSON# but is currently disabled due to non-empty offhand#WHITE#"`。



## O007 | entry-03616

### C03 | entry-03616 | 存在问题

原文片段“**but is currently disabled**”的主语来自拼接宿主“**Your tentacle hand**”；译文自行指定为“**该技能暂时被禁用**”，改变了禁用对象。

`S/data/talents/demented/writhing-body.lua:53–64` 将本片段插入触手手部属性说明；`canTentacleCombat`（32–40 行）判断的是触手战斗是否可用。冻结语境支持“触手手部不可用”，不能据此扩大为整个技能被禁用。



## O008 | entry-03616

### C03 | entry-03616 | 存在问题
- **原文与译文：** 原文是「, but is currently disabled due to non-empty offhand」，译文是「，由于副手非空，该技能暂时被禁用」。
- **问题：** 原文的主语是外层句子里的「Your tentacle hand」（context 中译作「你的触手之手当前具有以下属性%s：」）。译文把被禁用的对象改成了「该技能」，作用对象错了。
- **源码证据：**
  - `writhing-body.lua:32-41`：`canTentacleCombat` 为假时，只让 `getTentacleCombat` 返回 nil，也就是只停用触手战斗属性。
  - `writhing-body.lua:64`：这句只在触手属性描述后作为后缀插入。
  - 该文件里没有任何代码据此停用整个技能。
- **状态：** confirmed，来源未固定。



## O009 | entry-03617

### C04 | entry-03617 | 仅建议

“**a glorious explosion of gore**”译为“自爆成一团**光荣的血肉**”，修饰搭配生硬。但自爆、血肉爆炸、伤害、范围及主人死亡条件均可理解，未发现可独立证明的机制信息错误。

这属于自然度建议。`S/data/talents/misc/misc.lua:47–61` 的使用条件及两个参数与译文一致，`args_order=[2,1]` 正确。



## O010 | entry-03620

### C02 | entry-03620 | 存在问题

原文“global speed”译为“整体速度”。本包术语快照对 `tformat` 的该机制明确采用“全局速度”；`tome-cults/data/talents/misc/misc.lua:257–260` 和 `tome-cults/data/timed_effects.lua:2209–2219` 也表明它作用于全局速度。状态：**已证实的适用术语问题**。



## O011 | entry-03620

### C02 | entry-03620 | 存在问题
- **原文短引**：`#ORCHID#Speed:#LAST# Increases global speed by %d%%.`
- **译文短引**：`#ORCHID#速度：#LAST# 增加 %d%% 整体速度。`
- **问题具体内容**：明确适用的 preferred 术语违规。快照术语表中明确规定：`global speed` 的 preferred 译名为“全局速度”，且在备注中特别强调“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文使用了明确被禁止的“整体速度”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:263`（未固定快照）。技能 `Twisted Evolution` 的 `info` 函数格式化输出，直接面向玩家展示全局速度增益数值。



## O012 | entry-03620

### C03 | entry-03620 | 存在问题

原文类别“Power”译成“力量”，容易指向力量属性；同句说明的是“增加所有伤害”。`misc.lua:246–249,257–260` 选择 `TWISTED_POWER`，`timed_effects.lua:2246–2257` 将其效果加到全部伤害，而非力量属性。状态：**已证实的类别标签偏差**。



## O013 | entry-03620

### C03 | entry-03620 | 存在问题
- **原文短引**：`#ORCHID#Power:#LAST# Increases all damage by %d%%.`
- **译文短引**：`#ORCHID#力量：#LAST# 增加 %d%% 伤害。`
- **问题具体内容**：语义与机制混淆，且存在信息遗漏。该技能的三项进化分支分别为 Speed（全局速度）、Form（全属性加成 `all stats by %d`）与 Power（全部伤害提升 `all damage by %d%%`）。在紧接上一行“全属性”的语境下，将“Power”直译为“力量”，极易让玩家将其误解为主属性“力量”（Strength）；同时，“all damage”漏译了“全部/所有”，弱化了其对全系伤害加成的机制覆盖表述。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:247-264`（未固定快照）。分支 3 施加效果 `EFF_TWISTED_POWER`，对应逻辑为提升全伤害比例，与主属性 Strength 无关。



## O014 | entry-03620

### C04 | entry-03620 | 存在问题
- **原文与译文：** 原文是「Increases global speed by %d%%」，译文是「增加 %d%% 整体速度」。
- **问题：** 术语快照中 global speed 的 tformat 行是 preferred「全局速度」，并注明「不写作'整体速度'或'全体速度'」，明确适用于本条。
- **源码证据：** `timed_effects.lua:2219` 的 TWISTED_SPEED 修改的是 `global_speed_add`，确实是全局速度。
- **状态：** confirmed。



## O015 | entry-03620

### C05 | entry-03620 | 仅建议

“global speed”译为“整体速度”，在此仍能表达全局行动速度。冻结术语中的相关 preferred 行标为 `scope=core`，本条属于 Cults DLC；本包没有明确给出该范围向 DLC 强制扩展的规则，因此不据此确认术语违规。

这里只保留名称一致性的建议，不计缺陷。`S/data/talents/misc/misc.lua:242–260` 支持随机进化、至多指定数量、五回合及三种增益。



## O016 | entry-03622

### C04 | entry-03622 | 存在问题

原文“**expertly** hurls a pebble”中的熟练程度在“投掷鹅卵石”中消失。`misc.lua:320–326` 是这条战斗日志的消费位置。状态：**已证实的信息遗漏**。



## O017 | entry-03622

### C04 | entry-03622 | 存在问题
- **原文短引**：`#Source# expertly hurls a pebble at #target#!`
- **译文短引**：`#Source#朝#target#投掷鹅卵石！`
- **问题具体内容**：语义修饰信息遗漏。原文包含副词 `expertly`（熟练地/娴熟地/巧妙地），用以刻画该技能虽然只是投掷鹅卵石但动作极其熟练的动作特征。译文将 `expertly` 完全略去未译。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/misc.lua:325`（未固定快照）。技能 `Throw Pebble` 动作执行时的战斗日志输出 `self:logCombat(target, "#Source# expertly hurls a pebble at #target#!")`。



## O018 | entry-03622

### C05 | entry-03622 | 存在问题
- **原文与译文：** 原文是「#Source# **expertly** hurls a pebble at #target#!」，译文是「#Source#朝#target#投掷鹅卵石！」。
- **问题：** 「expertly」（娴熟地）这个修饰被完全删掉，丢失了一项语义信息。它属于风味文本，不影响机制。
- **源码证据：** `misc.lua:325`。
- **状态：** confirmed，轻微。



## O019 | entry-03622

### C06 | entry-03622 | 存在问题

原文“**expertly hurls a pebble**”的译文只有“投掷鹅卵石”，遗漏了动作娴熟、熟练的方式信息。

这是轻微但明确的语义遗漏，不是单纯润色偏好。`S/data/talents/misc/misc.lua:325` 的完整战斗日志直接包含该修饰语；它不代表额外命中或伤害加成。



## O020 | entry-03623

### C06 | entry-03623 | 仅建议
- 「coated in dark blight」译作「被黑暗和枯萎力量覆盖」，把一个修饰短语拆成了两种力量。这只是风味描述：伤害类型已由第二行的「暗影伤害」准确给出（`timed_effects.lua:95`），所以只算措辞偏好。
- 其余部分与 `races.lua:57-71` 一致：每回合只触发一次、要求可见、距离不超过 2、有上限、全部抗性（`timed_effects.lua:109`）。



## O021 | entry-03623

### C07 | entry-03623 | 存在问题

原文“**small spikes**”译为“尖刺”，遗漏了尖刺尺寸小这一外观信息。该信息在其他句子中也没有保留，属于轻微语义遗漏。

证据：冻结原文及 `S/data/talents/misc/races.lua:74`。另行核对后，译文增加的“可见”“流着黑血”并非无依据扩张：同文件 62–70 行同时检查可见性、黑血状态和距离。



## O022 | entry-03624

### C05 | entry-03624 | 仅建议
- **原文短引**：`Your faceless visage is puzzling and emotionless, allowing you to more easily resist mind tricks.`
- **译文短引**：`你无面孔的脸没有情感，令人困惑。这让你更容易抵抗精神冲击。`
- **问题具体内容**：措辞修饰与个人偏好。首句“你无面孔的脸”略显直译和同义反复（faceless visage 表达无面之容）；后半句“mind tricks”指心智诡计/惑控伎俩（对应后文的精神豁免与混乱免疫），译为“精神冲击”略有偏离，但鉴于整句纯属背景叙述（flavour text），不影响后文属性与百分比豁免机制的理解与参数消费，故仅属表达层面的润色建议，不计作事实缺陷。
- **状态**：仅建议
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:100`（未固定快照）。技能 `Faceless` 的背景说明。



## O023 | entry-03624

### C05 | entry-03624 | 存在问题

原文“resist **mind tricks**”指精神诡计或蛊惑，译文“抵抗**精神冲击**”改成了冲击性作用。`tome-cults/data/talents/misc/races.lua:90–97` 的效果是精神豁免与混乱免疫，也未提供“冲击”的依据。状态：**已证实的语义偏差**。



## O024 | entry-03624

### C07 | entry-03624 | 存在问题
- **原文与译文：** 原文是「resist **mind tricks**」，译文是「抵抗精神冲击」。
- **问题：** 「把戏、诡计」被改成了「冲击」，语义信息被改写。本技能实际提供的是精神豁免和混乱免疫（`races.lua:90-93`），针对的是心智操控类效果，不是冲击类伤害。
- **状态：** confirmed，轻微。



## O025 | entry-03624

### C08 | entry-03624 | 存在问题

原文“resist **mind tricks**”译为“抵抗**精神冲击**”，把精神欺骗、迷惑手段改成了冲击，丢失了原句的欺骗性含义。

`S/data/talents/misc/races.lua:83–97` 的语境是无面容、无情绪、精神豁免及混乱免疫，没有把这里的 `mind tricks` 指定为冲击或伤害。数值句本身没有发现问题。



## O026 | entry-03626

### C06 | entry-03626 | 存在问题

原文“affinity with **things** that dwell deep beneath the surface”泛指地下深处的一类事物；“同地下深处**某物**的联系”将其收窄为一个特定对象。语境见 `races.lua:171–176`。状态：**已证实的范围收窄**。



## O027 | entry-03626

### C09 | entry-03626 | 待确认

原文与译文都说巨口“**Each turn／每回合**”拉拽敌人。

`S/data/talents/misc/races.lua:149–162` 为巨口配置 `T_DREM_CALL_OF_AMAKTHEL`，召唤时强制使用一次；该技能在 `S/data/talents/misc/misc.lua:113–135` 设置 `cooldown=2`，通过技能动作执行拉拽。现有证据不能支持其随后固定每回合拉拽。

这是沿袭英文的频率疑点。尚缺该快照实际使用的 `dumb_talented` AI 调度实现及目标 DLC 版本映射；没有据此确认译文错误。



## O028 | entry-03627

### C07 | entry-03627 | 存在问题

原文是每回合“first creature **hit**”，译文为“攻击的第一个生物”。`races.lua:204–209` 给出说明；`timed_effects.lua:1945–1953` 在造成正数伤害后才进入首次目标的处理。攻击但未命中或未造成伤害不满足该条件。状态：**已证实的触发条件偏差**。



## O029 | entry-03627

### C10 | entry-03627 | 待确认

译文说“**每回合攻击的第一个生物100%%**”，英文也是“first creature hit”。

快照 `S/data/timed_effects.lua:1945–1953` 先排除死亡目标、非正伤害及不能被震慑的目标，然后才检查或建立本回合的触发记录。因此首次命中若不符合这些条件，后续符合条件的目标仍可能享有第一次触发待遇。

“第一个生物”没有准确区分首次命中与首次符合条件的伤害事件。该简化也存在于英文；快照内条件已核实，但目标 DLC 版本未固定，故保留待确认。



## O030 | entry-03629

### C11 | entry-03629 | 待确认

原文及译文均概括为杀死“**100 enemies／100个敌人**”。

`S/data/talents/misc/races.lua:238–241` 的计数回调先执行 `target:worthExp(self) <= 0` 则返回，只有通过此条件才增加计数；223 行以计数达到 100 决定能否使用，275 行在变更类型后清零。

因此快照并非所有敌人死亡都计入。这是英文已存在、译文继续沿用的条件遗漏疑点；目标 DLC 版本中的相同行为仍待确认。



## O031 | entry-03630

### C06 | entry-03630 | 存在问题
- **原文短引**：`You were created by ziguranth for one purpose only, to wage war on magic!`
- **译文短引**：`你被伊格制造的唯一理由：对魔法作战！`
- **问题具体内容**：专名术语混淆。术语快照关于 `Zigur` 与 `Ziguranth` 有极其明确的严格区分：“教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换”。Krog 是由反魔教团（Ziguranth）通过龙血融合改造制造的战士，动作的施动者是教团而非据点地名。译文将其译为“被伊格制造”，将教团专名误套为据点地名，违反了术语快照的强制区分规则。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:369`（未固定快照）。Krog 种族大招 `Drakeblood Strike` 的技能说明首句背景描述。



## O032 | entry-03630

### C08 | entry-03630 | 存在问题

原文“created by **ziguranth**”译成“被**伊格**制造”。本包术语快照区分教团 **Ziguranth＝伊格兰斯** 与地点 **Zigur＝伊格**；`races.lua:361–364` 指创建者，是教团语境。状态：**已证实的专名指称错误**。



## O033 | entry-03630

### C08 | entry-03630 | 存在问题
- **原文与译文：** 原文是「You were created by **ziguranth**…」，译文是「你被**伊格**制造的唯一理由」。
- **问题：** 术语快照中 Ziguranth 是 preferred「伊格兰斯」（教团），Zigur 才是「伊格」（地点），并注明「两者不得互换」。这里指的是教团，却用了地名；同段 entry-03629 用的就是「伊格兰斯」。
- **源码证据：** `races.lua:361`。
- **状态：** confirmed。



## O034 | entry-03630

### C09 | entry-03630 | 仅建议
- 「你被…制造的唯一理由：对魔法作战！」句式生硬，但信息没有丢失，只是自然度问题。



## O035 | entry-03630

### C12 | entry-03630 | 存在问题

原文“created by **ziguranth**”译成“被**伊格**制造”，将教团／人群换成了地点。

冻结术语明确区分 Ziguranth「伊格兰斯」与 Zigur「伊格」；同组 entry-03629 也将同一主体译作伊格兰斯。`S/data/talents/misc/races.lua:361` 明确写的是 `ziguranth`。这是指称错误，不依赖新的全局命名决定。



## O036 | entry-03632

### C09 | entry-03632 | 待确认

原文与译文都称低于 20% 生命后有“`%d%%` 几率”直接杀死。冻结快照 `races.lua:381–383,387–405` 虽计算 `getChance`，实际咬击流程在满足生命阈值及 `canBe("instakill")` 后没有概率抽取。这是**原文已有、译文沿袭的机制误述**，不是译文新增。DLC 快照哈希已核对，但其源码仓库和提交未固定；缺少目标版本源码，故目标版本适用性仍**待确认**。



## O037 | entry-03632

### C13 | entry-03632 | 待确认

原文及译文宣称存在随体质增长的“**%d%% chances／%d%%几率**”秒杀。

快照 `S/data/talents/misc/races.lua:382、398–403、412` 中，`getChance` 只用于说明文字；实际动作在生命条件满足后检查 `canBe("instakill")`，然后调用 `die`，没有消费该展示几率。本体 `T/game/modules/tome/class/Actor.lua:7599–7635` 的 `canBe` 消费免疫条件，不消费这里的体质派生展示值。

这是**沿袭英文的几率说明与动作实现不一致**。快照内事实明确，目标 DLC 版本适用性待确认。



## O038 | entry-03632

### C14 | entry-03632 | 待确认

原文“**under 20%%**”与译文“生命**不足20%%**”都排除了恰好 20%。

快照 `S/data/talents/misc/races.lua:398` 仅在生命比例 **大于** 20 且目标未死亡时提前返回；恰好 20% 的存活目标会继续进入秒杀检查。译文沿袭了英文的边界误述。

此边界在快照内可核验，但 DLC 目标版本未固定，故不升级为目标版本的已确认缺陷。



## O039 | entry-03633

### C07 | entry-03633 | 存在问题
- **原文短引**：`Increases global speed by %d%%.`
- **译文短引**：`整体速度增加 %d%%。`
- **问题具体内容**：明确适用的 preferred 术语违规。快照术语表中明确规定：`global speed` 的 preferred 译名为“全局速度”，且备注严格限定“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文使用了被明确禁止的“整体速度”。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/talents/misc/races.lua:422`（未固定快照）。寄生项圈被动技能 `Ultra Instinct`（`T_ULTRA_INSTINCT`）为角色提供 `global_speed_add`，其 `info` 显示全局速度加成。



## O040 | entry-03633

### C10 | entry-03633 | 存在问题

原文“Increases **global speed**”译为“**整体速度**增加”。本包术语快照明确规定此 `tformat` 机制用“全局速度”；`races.lua:422–429` 实际写入 `global_speed_add`。状态：**已证实的适用术语问题**。



## O041 | entry-03633

### C10 | entry-03633 | 存在问题
- **原文与译文：** 原文是「Increases global speed by %d%%」，译文是「整体速度增加 %d%%」。
- **问题：** 与 C04 相同，违反 tformat 的 global speed preferred 术语。
- **源码证据：** `races.lua:424` 修改的是 `global_speed_add`。
- **状态：** confirmed。



## O042 | entry-03633

### C11 | entry-03633 | 存在问题
- **原文与译文：** 原文是「your body reacts faster **and better** to aggressions」，译文是「你的身体全凭本能行动，反应速度更快」。
- **问题：** 译文删掉了「and better」，又新增了原文没有的「全凭本能行动」，语义信息有增有减。属于风味文本，不影响机制。
- **状态：** confirmed，轻微。



## O043 | entry-03633

### C15 | entry-03633 | 仅建议

“global speed／整体速度”的情况与 C05 相同：机制含义没有直接译错；冻结 preferred 行的 `scope=core` 不足以单独证明本 DLC 条目违反明确适用的命名要求。

这是名称一致性建议，与本条另一个已确认的语义遗漏分开计算。



## O044 | entry-03633

### C16 | entry-03633 | 存在问题

原文“reacts **faster and better to aggressions**”，译文为“全凭本能行动，**反应速度更快**”。

译文保留了速度提升，但没有保留“对攻击／侵扰作出反应”的对象，以及“应对得更好”这一独立于快慢的描述。“全凭本能行动”不能完整承载这两项信息。

证据：冻结原文及 `S/data/talents/misc/races.lua:427–429`。本项为叙述信息遗漏，不主张存在未显示的额外战斗数值。



## O045 | entry-03640

### C08 | entry-03640 | 存在问题
- **原文短引**：`Terrified of the horror duo attacking them reducing defense and spell save by %d.`
- **译文短引**：`因两只恐魔的现身而惊恐，闪避和法术豁免降低 %d。`
- **问题具体内容**：语义与事实错误。原文明确指出恐慌的原因是遭受两只恐魔的围攻（`attacking them`），译文将其错误地翻译为“因两只恐魔的现身而惊恐”。将持续攻击动作（attacking）篡改为出现/现身（appearing），扭曲了状态的因果描述与动作事实。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:276`（未固定快照）。效果 `WTW_TERRIBLE_SIGHT` 的 `long_desc`，由步行蠕虫同伴机制在近身触发。



## O046 | entry-03640

### C11 | entry-03640 | 存在问题

原文因恐魔双体“**attacking them**”而惊恐，译文改成因“两只恐魔的**现身**”而惊恐，改变了原因。`timed_effects.lua:273–285` 是该减闪避和法术豁免状态的说明与生效逻辑。状态：**已证实的语义偏差**。



## O047 | entry-03640

### C12 | entry-03640 | 存在问题
- **原文与译文：** 原文是「Terrified of the horror duo **attacking them**」，译文是「因两只恐魔的**现身**而惊恐」。
- **问题：** 惊恐的起因从「正在攻击他们」改成了「现身」，事实被改写。同一效果的 on_gain／on_lose 日志（`timed_effects.lua:281-282`）也都写的是「horrors attacking him」。
- **状态：** confirmed。



## O048 | entry-03642

### C12 | entry-03642 | 仅建议

“`+%d%% 所有造成的伤害`”语序生硬；层数和全部已造成伤害的增幅仍可读出，与 `timed_effects.lua:289–292` 一致。状态：**仅措辞偏好**。



## O049 | entry-03643

### C13 | entry-03643 | 仅建议

“victim”写成“牺牲者”带有献祭语感；这条日志仍能表达受害对象的痛苦强化了目标。`timed_effects.lua:465–483` 显示其生命吸取语境。状态：**仅措辞偏好**。



## O050 | entry-03643

### C13 | entry-03643 | 仅建议
- 「the pain of its victim」译作「牺牲者的痛苦」，省略了所属的「its」，而且「牺牲者」与「受害者」色彩略有不同。
- INNER_TENTACLES（`timed_effects.lua:465-486`）是吸血类增益，语境已能表明是它造成伤害的对象，信息没有实质丢失，只算措辞偏好。



## O051 | entry-03643

### C17 | entry-03643 | 存在问题

原文“the pain of **its victim**”译为“**牺牲者**的痛苦”，改变了受害者与施害者之间的关系，并引入了牺牲意味。

`S/data/timed_effects.lua:466–483` 的语境是内在触手吸取受伤目标的生命；回调在目标已死亡时直接退出。这里的 victim 是受到其伤害的对象，文本和机制都不要求其成为牺牲者。属于角色关系的语义偏移。



## O052 | entry-03645

### C09 | entry-03645 | 仅建议
- **原文短引**：`Target briefly saw what True Horror means, deeply scaring it. %d%% chances to fail using a talent.`
- **译文短引**：`目标被真正的恐惧吓倒，%d%% 几率使用技能失败。`
- **问题具体内容**：叙述细节压缩与偏好建议。原文 `Target briefly saw what True Horror means, deeply scaring it.` 中，“briefly saw”（短暂瞥见）、“what True Horror means”（真正的恐怖意味着什么）及“deeply scaring it”（深受惊吓）具有较强的克苏鲁风格叙事色彩；译文过度精简为“目标被真正的恐惧吓倒”。由于该句为纯背景叙述，其后关键机制 `%d%% chances to fail using a talent.` 对应正确，未造成机制理解偏差，故判定为偏好建议。
- **状态**：仅建议
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:557`（未固定快照）。状态 `GLIMPSE_OF_TRUE_HORROR` 的 `long_desc`。



## O053 | entry-03645

### C14 | entry-03645 | 存在问题

原文说目标“**briefly saw** what True Horror means”，译文只说“被真正的恐惧吓倒”，丢失了短暂目睹这一事件，并将所见之物改写为恐惧本身。`timed_effects.lua:554–565` 的状态说明及获得日志均保留“saw”。状态：**已证实的信息遗漏与语义偏差**。



## O054 | entry-03645

### C14 | entry-03645 | 存在问题
- **原文与译文：** 原文是「Target **briefly saw** what True Horror means, deeply scaring it」，译文是「目标被真正的恐惧吓倒」。
- **问题：** 「短暂瞥见」这层信息被删掉了。它正对应效果名 Glimpse of True Horror（context 中译作「一瞥真惧」）。
- **源码证据：** `timed_effects.lua:556-557`。数值部分正确，由 `talent_fail_chance`（:565）实现。
- **状态：** confirmed，轻微。



## O055 | entry-03645

### C18 | entry-03645 | 存在问题

原文明确叙述目标“**briefly saw what True Horror means**”，译文只保留“被真正的恐惧吓倒”，遗漏了短暂目睹、领略真恐怖这一事件。

冻结邻文 `context.lua:365` 将状态称为“一瞥真惧”；`S/data/timed_effects.lua:555–563` 的状态名、说明及获得日志也共同指向“看见”。技能失败几率保留正确，但这项叙述信息仍有遗漏。



## O056 | entry-03646

### C10 | entry-03646 | 存在问题
- **原文短引**：`...and causing them to take an additional %d%% temporal damage from Dark Whispers and Hideous Visions.`
- **译文短引**：`...并使他们从黑暗低语和失智冲击中受到额外 %d%% 时空伤害。`
- **问题具体内容**：状态/机制专名误译与内部不一致。原文提及的状态 `Hideous Visions` 在同文件上方第 761 行（对应本组 context.lua 第 398 行）已有唯一定名且翻译为“惊骇幻象”。译文在此处将其误译为一个完全无关的名称“失智冲击”，导致前后译名冲突，玩家在游戏界面中寻找对应联动状态时无法辨识。
- **状态**：存在问题
- **源码路径与消费逻辑**：`sources/dlc/cults/tome-cults/data/timed_effects.lua:779`（未固定快照）。状态 `CACOPHONY` 的 `long_desc`，联动强化 `Dark Whispers`（黑暗低语）与 `Hideous Visions`（惊骇幻象）的时空伤害。

---



## O057 | entry-03646

### C15 | entry-03646 | 存在问题

原文“**Hideous Visions**”译成“**失智冲击**”；冻结邻近译文 `context.lua:398` 将同一效果名称译为“**惊骇幻象**”，`timed_effects.lua:759–779` 也分别定义 `HIDEOUS_VISIONS` 与本条 `CACOPHONY`。现译会把玩家指向错误名称。状态：**已证实的指称错误**。



## O058 | entry-03646

### C15 | entry-03646 | 存在问题
- **原文与译文：** 原文是「…temporal damage from Dark Whispers and **Hideous Visions**」，译文是「从黑暗低语和**失智冲击**中受到…」。
- **问题：** Hideous Visions 在同一 section 的效果名译作「惊骇幻象」（context.lua 与 `timed_effects.lua:759-761`）。「失智冲击」与之不符，玩家无法把它对应到所指的效果或技能。
- **源码证据：** 引用关系见 `timed_effects.lua:743-748`，那里通过 `T_HIDEOUS_VISIONS`／`EFF_HIDEOUS_VISIONS` 调用该效果。
- **状态：** confirmed。
- **上游问题（不计入）：** 额外的时空伤害实际只在 Dark Whispers 的 on_timeout 中结算（:751-755）。



## O059 | entry-03646

### C19 | entry-03646 | 待确认

原文引用“**Hideous Visions**”，译文引用“**失智冲击**”；冻结邻文 `context.lua:398` 将 Hideous Visions 称为“惊骇幻象”。仅按名称对照存在不一致，但不能据此直接确认错译。

实际消费链如下：

- `S/data/timed_effects.lua:741–754`：黑暗低语在心灵尖啸状态下增加幻象生成几率，并产生额外时空伤害。
- `D/data/talents/demented/madness.lua:118–134`：幻象死亡后的额外时空伤害位于 `T_SANITY_WARP` 条件分支内。
- 同文件 163–175 行：该技能名为 **Sanity Warp**，作用是幻象死亡时产生伤害爆发。

因此“失智冲击”可能是在按实现纠正英文的技能归属。冻结材料没有提供 **Sanity Warp ↔ 失智冲击** 的名称映射，且 DLC 目标版本未固定；需要这两项证据才能裁定。此前名称不一致的表面观察不作为已确认错误。



## O060 | entry-03650

### C16 | entry-03650 | 仅建议
- 同一句里「defense」和「avoid all damage」都译作「闪避」，前后两次「闪避」含义不同。
- 占位符、数值和条件都正确：FORTUNE 在 stacks > 6 时才使用这条描述（`timed_effects.lua:1600-1602`），闪避所有伤害由 `cancel_damage_chance` 实现（:1637）。只算措辞偏好。



## O061 | entry-03651

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

