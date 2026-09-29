已完成全部 40 条复核和 61 项匿名观察裁决：**12 条 ISSUE、4 条 PENDING、24 条 OK；归并为 15 项确认缺陷、8 项未决问题。**未修改仓库，未创建子 agent。

下文 `S/` 表示本包冻结的 `sources/dlc/cults/tome-cults/`；`A/` 表示白名单追加快照中的 `tome-cults/`；`T/` 表示本体固定 commit 下的路径。完整路径与版本列于末尾。**所有 DLC 源码均已核验快照哈希，但仓库、commit 和目标版本映射未固定。**

| entry-ID | 判定 | canonical D或P编号／简短依据 |
|---|---|---|
| entry-03613 | OK | 护甲、护盾吸收量、持续时间及恢复前不能再次触发均保留；`void.lua:101–103,175–177`。 |
| entry-03614 | ISSUE | D01；另有 P01。全抗用词仅建议。 |
| entry-03615 | OK | `void shards` 在此恢复的是 `T_VOID_STARS` 计数，译为“虚空之星”有依据；`void.lua:313–317`。 |
| entry-03616 | ISSUE | D02：禁用对象从触手改成整个技能。 |
| entry-03617 | OK | 自爆、伤害、范围和召唤者死亡条件保留；`args_order=[2,1]` 正确。“光荣的血肉”仅措辞建议。 |
| entry-03618 | OK | 传送技能名称与冻结邻文一致；`misc.lua:67–68`。 |
| entry-03619 | OK | 法术失败日志语义相符；`misc.lua:80–82`。 |
| entry-03620 | ISSUE | D03：适用机制术语。“力量”分支标签及无类型限定的“伤害”不足以另立机制缺陷。 |
| entry-03621 | OK | 上下文明确为玻璃碎片；`misc.lua:265–294`。 |
| entry-03622 | ISSUE | D04：遗漏动作娴熟程度。 |
| entry-03623 | ISSUE | D05：遗漏尖刺尺寸。“可见”“黑血”有源码支持。 |
| entry-03624 | ISSUE | D06：精神诡计改成精神冲击。 |
| entry-03625 | OK | 召唤空间不足语义正确；冻结术语的 `logSeen` 行不能强制覆盖本条 `logPlayer` 标点。 |
| entry-03626 | ISSUE | D07；另有 P02。段落重排未改变参数消费。 |
| entry-03627 | ISSUE | D08、D09；另有 P03。 |
| entry-03628 | OK | 当前选项标记、颜色和斜体标记保留；`races.lua:264–268`。 |
| entry-03629 | PENDING | P04；六个参数按 `[1,3,2,4,5,6]` 重排正确。 |
| entry-03630 | ISSUE | D10：教团与地点指称混用。 |
| entry-03631 | OK | 保留“试图咬”的尝试语义及双方占位符；`races.lua:392`。 |
| entry-03632 | PENDING | P05、P06；命中后回复生命的条件、数值与持续时间相符。 |
| entry-03633 | ISSUE | D11、D12、D13。“全凭本能”结合技能名仅作表达建议。 |
| entry-03634 | OK | 战斗指令与堡垒撤离承诺保留；`timed_effects.lua:48,56–60`。 |
| entry-03635 | OK | 黑血开始流出的状态日志相符；`timed_effects.lua:91`。 |
| entry-03636 | OK | 黑血停止流出的状态日志相符；`timed_effects.lua:92`。 |
| entry-03637 | OK | 被黏稠触须捕获的对象和事件相符；`timed_effects.lua:120`。 |
| entry-03638 | OK | “逃脱”在状态解除日志中表达脱离束缚，不要求额外主动行动；`timed_effects.lua:121`。 |
| entry-03639 | OK | 触手缠绕语义与冻结状态名相符；`timed_effects.lua:129–137`。 |
| entry-03640 | ISSUE | D14：叙述中的攻击动作改成现身；不据此认定实际触发要求攻击。 |
| entry-03641 | OK | 保留恐魔攻击目标及目标惊恐的关系；`timed_effects.lua:281`。 |
| entry-03642 | OK | 层数和全部伤害增幅保留；语序仅建议，`timed_effects.lua:292,305`。 |
| entry-03643 | OK | “牺牲者”在此可指受害对象，不必然指死亡或献祭；用词仅建议。 |
| entry-03644 | OK | 变成恐魔及颜色标记保留；`timed_effects.lua:496`。 |
| entry-03645 | ISSUE | D15：遗漏短暂目睹真恐怖的事件。 |
| entry-03646 | PENDING | P07：伤害调用链支持 Sanity Warp 分支，但缺中文名称映射和目标版本证据。 |
| entry-03647 | OK | “降低至”结合跨越阈值的语境成立；快照条件为从阈值以上降至其以下或相等，`timed_effects.lua:956,967,978`。 |
| entry-03648 | OK | 创伤来源、承受者及颜色标记相符；`timed_effects.lua:1071`。 |
| entry-03649 | OK | 日志中的 `%s` 是承载该效果的生物名称，“从其身上出现”成立；`timed_effects.lua:1689–1701`。 |
| entry-03650 | OK | 三项显示参数与对应叠层增益一致；“闪避所有伤害”仅有措辞区分建议。 |
| entry-03651 | PENDING | P08；新增治疗覆盖规则与层数消耗说明符合快照。 |
| entry-03652 | OK | 传送状态名与同组技能名一致；`timed_effects.lua:1830–1832`。 |

确认缺陷均为**相对英文的译文新增偏差**，不表示这些偏差一定由最近一次修改引入。下表的 DLC 行号是哈希冻结快照行号，不能称为固定 DLC commit 证据。

| D-ID | entry-ID | 内容、归因及源码／语境证据 |
|---|---|---|
| D01 | entry-03614 | **遗漏尝试限定。**`attempt to daze` 只剩“施加眩晕”。`S/data/talents/demented/void.lua:279` 明确保留尝试语气；`:242–257` → `A/data/damage_types.lua:105–116` 的投射检查 `canBe("stun")` 后才设置效果。确认限定信息遗漏，不把中文“施加”单独解释为绝对无视免疫。 |
| D02 | entry-03616 | **禁用对象扩大。**宿主主语是 `Your tentacle hand`，译文却指定“该技能”。`S/data/talents/demented/writhing-body.lua:53–64` 展示拼接关系；`:32–40` 控制触手战斗属性可用性；`context.lua:54–60` 的中文宿主同样指触手。 |
| D03 | entry-03620 | **适用术语偏差。**`global speed` 译为“整体速度”；冻结术语中匹配 `tformat`、全局行动速度机制的 preferred 行明确要求“全局速度”。`S/data/talents/misc/misc.lua:247,258` → `S/data/timed_effects.lua:2219` 写入 `global_speed_add`。 |
| D04 | entry-03622 | **动作方式遗漏。**`expertly` 所表达的娴熟程度未保留。`S/data/talents/misc/misc.lua:325` 是完整日志；不据此主张额外命中或伤害加成。 |
| D05 | entry-03623 | **外观尺寸遗漏。**`small spikes` 只译“尖刺”，没有保留“小”的信息。`S/data/talents/misc/races.lua:74`；其他句子也未承载该信息。 |
| D06 | entry-03624 | **精神作用的叙述含义改变。**`mind tricks` 的欺骗、迷惑意味被“精神冲击”替代。`S/data/talents/misc/races.lua:90–97` 的语境为精神豁免和混乱免疫，没有给“冲击”提供对应依据。此项不宣称精神豁免只针对某一种控制机制。 |
| D07 | entry-03626 | **复数泛指收窄。**`things that dwell deep beneath the surface` 指地下深处的一类事物，“地下深处某物”转为单一不明对象。`S/data/talents/misc/races.lua:172–176` 未将这些事物指定为唯一实体。 |
| D08 | entry-03627 | **首次对象的选取条件改变。**`first creature hit` 变为“攻击的第一个生物”。主句虽保留造成伤害条件，括号仍可能把首次攻击但未命中的对象算作首个对象。`S/data/talents/misc/races.lua:205–209`；`S/data/timed_effects.lua:1945–1953` 在正伤害回调内处理首次触发。 |
| D09 | entry-03627 | **补充漏项：对象范围收窄。**`can only stun a creature once per turn` 译为“每个敌人……一次”，将生物范围收窄为敌人。`S/data/talents/misc/races.lua:207`；`S/data/timed_effects.lua:1945–1953` 按 `target.uid` 限制，未在此检查敌对关系。 |
| D10 | entry-03630 | **专名指称错误。**创建者 `ziguranth` 被写成地点译名“伊格”。`S/data/talents/misc/races.lua:288,361` 与 `context.lua:217–240` 支持同一教团主体；冻结术语明确区分教团“伊格兰斯”和据点“伊格”。 |
| D11 | entry-03633 | **适用术语偏差。**同 D03，`global speed` 使用“整体速度”。`S/data/talents/misc/races.lua:424,427–429` 的实际属性是 `global_speed_add`。 |
| D12 | entry-03633 | **应对质量信息遗漏。**`faster and better` 仅保留“反应速度更快”，没有表达应对得更好。`S/data/talents/misc/races.lua:427`；不据此推导额外数值效果。 |
| D13 | entry-03633 | **反应对象信息遗漏。**`to aggressions` 的攻击／侵扰对象未保留。`S/data/talents/misc/races.lua:427`；“全凭本能行动”不包含这一对象。与 D12 分开计。 |
| D14 | entry-03640 | **叙述动作替换。**`horror duo attacking them` 改成“两只恐魔的现身”。`S/data/timed_effects.lua:276,281–282` 均有攻击叙述。但实际施加链 `:262–267` 是范围效果，所以本 D 仅确认叙述变化，不确认“必须遭受攻击才触发”的机制断言。 |
| D15 | entry-03645 | **目睹事件遗漏。**`briefly saw what True Horror means` 被压缩为“被真正的恐惧吓倒”，丢失短暂目睹、领略的事件。`S/data/timed_effects.lua:555–561` 的说明和获得日志均支持“看见”；`context.lua:365–367` 也一致。技能失败参数正确。 |

| O-ID | 状态 | 命中D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | mixed | D01 | confirmed：遗漏 `attempt`，见 `void.lua:279`。refuted：仅凭“施加”不能断言译文明确承诺无条件生效；快照免疫检查见 `A/data/damage_types.lua:112–113`。 |
| O002 | confirmed | D01 | 原文的尝试限定未保留；`void.lua:242–257,279` 和 `MESMERIZE` 条件支持这种限定有实际意义。 |
| O003 | mixed | D01 | confirmed：尝试限定遗漏。refuted：“写成必定生效”的绝对化表述过强。快照检查与目标版本适用性必须分开。 |
| O004 | advisory | — | 冻结抗性条目是面板／`_t` 语境，不能直接构成本条 `tformat` 的强制名称要求；“全体抗性”在此仍指全抗。 |
| O005 | pending | — | P01。`void.lua:242–245` 清空行动能量；本体 `Actor.lua:168–170,761–773` 和 `GameEnergyBased.lua:124–129` 未支持固定半回合调度。 |
| O006 | mixed | D02 | confirmed：拼接主语是触手，见 `writhing-body.lua:62–64`。pending：关于各项被动加成完全不受限制的扩展机制断言，本次未追完其全部消费实现，不作为 D02 的必要依据。 |
| O007 | confirmed | D02 | 中文和英文宿主都指触手；`context.lua:54–60`、`writhing-body.lua:53–64` 直接证明对象被改写。 |
| O008 | confirmed | D02 | `canTentacleCombat`／`getTentacleCombat` 与说明拼接支持触手对象，不能扩大为整个技能停用；`:32–40,64`。 |
| O009 | advisory | — | 自爆和血肉爆炸信息仍在；问题为“光荣的血肉”的搭配。`misc.lua:47–61` 与参数重排一致。 |
| O010 | confirmed | D03 | 匹配冻结 `tformat` 机制术语；实际写入 `global_speed_add`，见 `timed_effects.lua:2219`。 |
| O011 | confirmed | D03 | preferred 行明确排除“整体速度”；准确说明位置为 `misc.lua:258–260`，不是观察所引的 `:263`。 |
| O012 | refuted | — | “力量”是分支标题，紧接“增加伤害”明确解释其效果；`misc.lua:257–260` 没有把该标题断言为 Strength 属性加成。可建议换词，不能确认机制混淆。 |
| O013 | mixed | — | refuted：完整句子没有将 Power 写成力量属性增益。advisory：“所有伤害”可更明确，但无类型限定的“增加伤害”未明确收窄范围；`timed_effects.lua:2257` 为全伤害。 |
| O014 | confirmed | D03 | `global_speed_add` 与冻结机制术语一致，见 `timed_effects.lua:2219`。 |
| O015 | refuted | — | 本包明确按 `source_tag/category/语境` 适用；匹配行的备注覆盖技能与状态说明。不能仅凭 `scope=core` 推出本 DLC 获得该名称要求的豁免。 |
| O016 | confirmed | D04 | `misc.lua:325` 的 `expertly` 未被其他译文成分承载。 |
| O017 | confirmed | D04 | 确认动作娴熟程度遗漏；不涉及额外机制数值。 |
| O018 | confirmed | D04 | 同 D04，属于轻微但具体的语义信息遗漏。 |
| O019 | confirmed | D04 | 完整日志直接支持修饰信息；`:325`。 |
| O020 | advisory | — | 在风味句中“黑暗和枯萎力量”不必然断言两种独立伤害类型；实际伤害句明确为暗影。`races.lua:74–78`、`timed_effects.lua:95`。 |
| O021 | confirmed | D05 | “小”这一外观信息确实遗漏；可见、黑血和距离限制则有 `races.lua:62–70` 支持。 |
| O022 | mixed | D06 | advisory：“无面孔的脸”的自然度。confirmed：`mind tricks` 改成“精神冲击”；风味叙述不因此免于语义审核。 |
| O023 | confirmed | D06 | `races.lua:90–97` 支持精神防护语境，原句的欺骗／迷惑含义未保留。 |
| O024 | confirmed | D06 | 确认词义改变；不采纳由此进一步推导“精神豁免只针对心智操控”的排他机制解释。 |
| O025 | confirmed | D06 | 原文和冻结上下文均没有将 tricks 指定为冲击或伤害；`:83–97`。 |
| O026 | mixed | D07 | confirmed：复数泛指变成单一不明对象。refuted：不能说“某物”已经指明了某个身份确定的实体；缺陷是范围收窄。 |
| O027 | pending | — | P02。`races.lua:149–162` 的首次强制使用与 `misc.lua:117` 的冷却 2 已核验；之后的实际 AI 调度未闭合。 |
| O028 | confirmed | D08 | 主句的伤害条件不能完整消除括号中“首次攻击”和“首次命中”的顺序差异；`timed_effects.lua:1945–1953`。 |
| O029 | pending | — | P03。死亡、非正伤害、震慑免疫检查先于首次记录建立；快照事实明确，目标版本适用性未固定。 |
| O030 | pending | — | P04。`races.lua:238–241` 排除 `worthExp<=0`，而文字只说 100 个敌人；沿袭英文。 |
| O031 | confirmed | D10 | 教团／地点指称区分成立；准确原句在 `races.lua:361`，不是 `:369`。 |
| O032 | confirmed | D10 | `ziguranth` 是创建者，冻结邻文将同一主体译为“伊格兰斯”；`context.lua:217–240`。 |
| O033 | confirmed | D10 | 本项既有术语区分，又有同组指称证据；无需新命名策略。 |
| O034 | advisory | — | 除 D10 已单独确认的专名外，句式生硬不再另计缺陷。 |
| O035 | confirmed | D10 | 确认同一教团被换成据点译名；`races.lua:288,361`。 |
| O036 | pending | — | P05。`getChance` 进入说明，但咬击动作没有消费该展示概率；`races.lua:382,398–412`。 |
| O037 | pending | — | P05。本体 `canBe` 检查状态免疫，不能替代缺失的体质派生概率抽取；仍缺 DLC 版本映射。 |
| O038 | pending | — | P06。`races.lua:398` 允许恰好 20% 的存活目标继续检查；英文和译文均写严格不足 20%。 |
| O039 | confirmed | D11 | 冻结机制术语适用；`races.lua:424` 为全局速度属性。 |
| O040 | confirmed | D11 | 与 D03 相同的术语偏差，另一个 entry 独立覆盖。 |
| O041 | confirmed | D11 | `races.lua:424,428–429` 的机制与格式语境吻合。 |
| O042 | mixed | D12 | confirmed：遗漏 `better`。advisory：“全凭本能”可由 `Ultra Instinct／终极本能` 与无思维干扰的上下文支持，不单独确认无依据新增。 |
| O043 | refuted | — | 与 O015 相同，`scope=core` 本身不足以推翻本包明确的适用规则及机制备注；命中 D11。 |
| O044 | confirmed | D12、D13 | 分别遗漏应对质量和反应对象；`races.lua:427`。不据此主张额外未显示数值。 |
| O045 | confirmed | D14 | 确认叙述从“攻击”变成“现身”；不将此确认扩展为实际必须持续围攻才施加状态。 |
| O046 | confirmed | D14 | `timed_effects.lua:276,281–282` 支持叙述变化；实际范围施加链另见 `:262–267`。 |
| O047 | confirmed | D14 | 获得／解除日志也保留攻击叙述；实际触发不依赖攻击事件这一点不被隐去。 |
| O048 | advisory | — | “+%d%% 所有造成的伤害”语序不自然，但层数、增幅及范围保留；`timed_effects.lua:292,305`。 |
| O049 | advisory | — | “牺牲者”有不同语感，但不必然指献祭对象；吸血语境见 `:466–483`。 |
| O050 | advisory | — | 汉语在这里省略显式所有格仍可承载受害关系；没有改成他人的受害者或无关对象。 |
| O051 | refuted | — | `victim→牺牲者` 不必然增加死亡、献祭或自愿牺牲条件；回调排除死亡目标也不能证明该中文词只指死者。 |
| O052 | mixed | D15 | confirmed：观察自己指出的短暂目睹事件确有遗漏。refuted：不能仅因属于背景叙述就全部降为润色建议。 |
| O053 | confirmed | D15 | `timed_effects.lua:557,561` 支持目睹事件；确认事件遗漏，不把“恐惧／恐怖”另算一项缺陷。 |
| O054 | confirmed | D15 | 短暂目睹信息未在说明句中保留；`talent_fail_chance` 数值句正确，`:565`。 |
| O055 | confirmed | D15 | 名称、说明与获得日志共同支持目睹语境；合并到 D15，不重复计数。 |
| O056 | pending | — | P07。名称不一致可见，但 `madness.lua:123–134` 支持 Sanity Warp 作为额外伤害分支，不能只按状态名称判错。 |
| O057 | pending | — | P07。`HIDEOUS_VISIONS` 与 `CACOPHONY` 的定义本身不足以排除译文按实际伤害技能归属修订英文。 |
| O058 | mixed | — | pending：主名称问题归 P07。refuted：“额外时空伤害只在 Dark Whispers 结算”；`madness.lua:130–133` 还有幻象死亡后的时空投射。 |
| O059 | pending | — | P07。独立核验支持其调用链判断；缺 `Sanity Warp↔失智冲击` 冻结映射及目标版本证据。 |
| O060 | advisory | — | 数值闪避与“闪避所有伤害”可区分，后者不必然被理解为一次防御对抗；`timed_effects.lua:1600–1602,1637`。 |
| O061 | pending | — | P08。致命伤害转移不等于无条件处死；`:1716–1738`。治疗量由不幸覆盖幸运、并消耗对应效果的说明核验相符。 |

未决项另列，不计入确认缺陷：

- **P01｜entry-03614｜沿袭上游：巨石半回合频率。**`S/data/talents/demented/void.lua:242–245` 每次 `on_act` 投射并清空能量；本体默认速度和能量调度未给出半回合依据。尚缺完整初始化／调度闭合及 DLC 目标版本映射，不能断言实际一定是一回合。
- **P02｜entry-03626｜沿袭上游：巨口每回合拉拽。**召唤时强制释放一次，但技能冷却为 2。尚未取得该召唤物后续 `dumb_talented` 调度的完整证据，也缺版本映射。
- **P03｜entry-03627｜沿袭上游：首次命中的合格条件。**`S/data/timed_effects.lua:1946–1950` 先排除死亡、非正伤害和震慑免疫目标，才进入首次触发记录。英文与中文均未完整表达这一筛选；快照事实明确，版本适用性待确认。
- **P04｜entry-03629｜沿袭上游：击杀计数资格。**`S/data/talents/misc/races.lua:238–241` 只计 `worthExp>0` 的目标；并非任意敌人死亡都计入。缺目标版本对应证据。
- **P05｜entry-03632｜沿袭上游：秒杀展示概率。**动作不消费 `getChance`；本体 `canBe("instakill")` 消费的是免疫检查。缺目标 DLC 版本映射。
- **P06｜entry-03632｜沿袭上游：20% 边界。**快照允许恰好 20%，英文和中文都排除这一边界。与概率问题分开，版本适用性待确认。
- **P07｜entry-03646｜归因未定：联动技能名称。**`S/data/timed_effects.lua:741–754` 与 `A/data/talents/demented/madness.lua:118–175,224–226` 支持黑暗低语及 Sanity Warp 两条额外伤害路径。可能是译文纠正上游引用，也可能是名称错误；不能缺少中文映射便确认任一解释。
- **P08｜entry-03651｜沿袭上游：替死保证。**`S/data/timed_effects.lua:1734–1736` 投射伤害、调用 `on_fatebreaker_call` 后取消自身伤害；`T/game/modules/tome/data/damage_types.lua:2863–2869` 将 VOID 拆成时空和暗影伤害。缺具体目标回调和目标版本证据，尚不能证明所选目标必死。

主要分歧的处理依据是：按完整句子判断“力量”“伤害”“牺牲者”等词，避免将普通措辞强行解释为排他机制；具体叙述遗漏仍按本包规则计入缺陷。术语方面，本包明确要求按 `source_tag/category/语境` 匹配，相关 global speed 行的备注直接覆盖这两条技能说明，因此本次不采纳仅凭 `scope=core` 排除适用性的意见。

实际读取路径如下。前缀与相对路径拼接即完整路径：

```text
B=/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g12-20260923
S=B/sources/dlc/cults/tome-cults
A=/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults
T=/workspace/t-engine4
```

- 冻结输入：`B/ADJUDICATION-INPUT.md`、`B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。
- 本组源码，SHA-256 均与白名单匹配：
  - `S/data/talents/demented/void.lua`：`19cb982e3487…`
  - `S/data/talents/demented/writhing-body.lua`：`37c7c1f3ebe5…`
  - `S/data/talents/misc/misc.lua`：`3b37fe925ecb…`
  - `S/data/talents/misc/races.lua`：`59b9b67cb0a3…`
  - `S/data/timed_effects.lua`：`0d3139ebf8a4…`
- 追加源码，哈希均匹配：
  - `A/data/damage_types.lua`：`6ec5f1659e60…`；由巨石的 `MESMERIZE` 投射引入。
  - `A/data/talents/demented/friend-of-the-worm.lua`：`e8c4508aa632…`；由 `WTW_TERRIBLE_SIGHT`／`WTW_SHARED_INSANITY` 及对应技能引入。
  - `A/data/talents/demented/madness.lua`：`33e274b4e1f1…`；由 `T_HIDEOUS_VISIONS.hideous_vision` 调用引入。
- 本体源码全部通过 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取：
  - `T/game/modules/tome/class/NPC.lua`；由召唤定义的 `require "mod.class.NPC"` 引入。
  - `T/game/modules/tome/class/Actor.lua`；由 NPC 的继承／调用及 `canBe` 核验引入。
  - `T/game/engines/default/engine/GameEnergyBased.lua`；由 NPC 的 `tickLevel` 调度注释引入。
  - `T/game/modules/tome/data/damage_types.lua`；由 `DamageType.VOID` 投射引入。

40 条冻结原译文均与 `INPUT.md` 一致；格式参数在应用 `args_order` 后全部匹配，颜色、样式和角色标记序列也全部匹配。未运行游戏，未将静态检查表述为运行验证。

未读取身份映射、原始报告、STATE、其他轮答案或当前译文；追加源码仅来自入口明确授权的白名单。未创建临时文件。首次普通沙箱读取在执行前因挂载隔离失败，随后经获准的只读命令完成读取。上述结果是独立复核裁决，不是生产完成认证。
