# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的41项观察及独立盲审的20项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03614 | C01（原问题） | C01（原问题） | 未提出此缺陷 | **遗漏尝试限定。**`attempt to daze` 只剩“施加眩晕”。`S/data/talents/demented/void.lua:279` 明确保留尝试语气；`:242–257` → `A/data/damage_types.lua:105–116` 的投射检查 `canBe("stun")` 后才设置效果。确认限定信息遗漏，不把中文“施加”单独解释为绝对无视免疫。 |
| D02 | entry-03616 | C03（原问题） | 未提出此缺陷 | C01（原问题） | **禁用对象扩大。**宿主主语是 `Your tentacle hand`，译文却指定“该技能”。`S/data/talents/demented/writhing-body.lua:53–64` 展示拼接关系；`:32–40` 控制触手战斗属性可用性；`context.lua:54–60` 的中文宿主同样指触手。 |
| D03 | entry-03620 | C04（原问题） | C02（原问题） | C02（原问题） | **适用术语偏差。**`global speed` 译为“整体速度”；冻结术语中匹配 `tformat`、全局行动速度机制的 preferred 行明确要求“全局速度”。`S/data/talents/misc/misc.lua:247,258` → `S/data/timed_effects.lua:2219` 写入 `global_speed_add`。 |
| D04 | entry-03622 | C05（原问题） | C04（原问题） | C04（原问题） | **动作方式遗漏。**`expertly` 所表达的娴熟程度未保留。`S/data/talents/misc/misc.lua:325` 是完整日志；不据此主张额外命中或伤害加成。 |
| D05 | entry-03623 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **外观尺寸遗漏。**`small spikes` 只译“尖刺”，没有保留“小”的信息。`S/data/talents/misc/races.lua:74`；其他句子也未承载该信息。 |
| D06 | entry-03624 | C07（原问题） | C05（原问题） | C05（原建议） | **精神作用的叙述含义改变。**`mind tricks` 的欺骗、迷惑意味被“精神冲击”替代。`S/data/talents/misc/races.lua:90–97` 的语境为精神豁免和混乱免疫，没有给“冲击”提供对应依据。此项不宣称精神豁免只针对某一种控制机制。 |
| D07 | entry-03626 | 未提出此缺陷 | C06（原问题） | 未提出此缺陷 | **复数泛指收窄。**`things that dwell deep beneath the surface` 指地下深处的一类事物，“地下深处某物”转为单一不明对象。`S/data/talents/misc/races.lua:172–176` 未将这些事物指定为唯一实体。 |
| D08 | entry-03627 | 未提出此缺陷 | C07（原问题） | 未提出此缺陷 | **首次对象的选取条件改变。**`first creature hit` 变为“攻击的第一个生物”。主句虽保留造成伤害条件，括号仍可能把首次攻击但未命中的对象算作首个对象。`S/data/talents/misc/races.lua:205–209`；`S/data/timed_effects.lua:1945–1953` 在正伤害回调内处理首次触发。 |
| D09 | entry-03627 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **补充漏项：对象范围收窄。**`can only stun a creature once per turn` 译为“每个敌人……一次”，将生物范围收窄为敌人。`S/data/talents/misc/races.lua:207`；`S/data/timed_effects.lua:1945–1953` 按 `target.uid` 限制，未在此检查敌对关系。 |
| D10 | entry-03630 | C08（原问题） | C08（原问题） | C06（原问题） | **专名指称错误。**创建者 `ziguranth` 被写成地点译名“伊格”。`S/data/talents/misc/races.lua:288,361` 与 `context.lua:217–240` 支持同一教团主体；冻结术语明确区分教团“伊格兰斯”和据点“伊格”。 |
| D11 | entry-03633 | C10（原问题） | C10（原问题） | C07（原问题） | **适用术语偏差。**同 D03，`global speed` 使用“整体速度”。`S/data/talents/misc/races.lua:424,427–429` 的实际属性是 `global_speed_add`。 |
| D12 | entry-03633 | C11（原问题） | 未提出此缺陷 | 未提出此缺陷 | **应对质量信息遗漏。**`faster and better` 仅保留“反应速度更快”，没有表达应对得更好。`S/data/talents/misc/races.lua:427`；不据此推导额外数值效果。 |
| D13 | entry-03633 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **反应对象信息遗漏。**`to aggressions` 的攻击／侵扰对象未保留。`S/data/talents/misc/races.lua:427`；“全凭本能行动”不包含这一对象。与 D12 分开计。 |
| D14 | entry-03640 | C12（原问题） | C11（原问题） | C08（原问题） | **叙述动作替换。**`horror duo attacking them` 改成“两只恐魔的现身”。`S/data/timed_effects.lua:276,281–282` 均有攻击叙述。但实际施加链 `:262–267` 是范围效果，所以本 D 仅确认叙述变化，不确认“必须遭受攻击才触发”的机制断言。 |
| D15 | entry-03645 | C14（原问题） | C14（原问题） | C09（原建议） | **目睹事件遗漏。**`briefly saw what True Horror means` 被压缩为“被真正的恐惧吓倒”，丢失短暂目睹、领略的事件。`S/data/timed_effects.lua:555–561` 的说明和获得日志均支持“看见”；`context.lua:365–367` 也一致。技能失败参数正确。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O001 | Sol C01（原问题） | entry-03614 | mixed | confirmed：遗漏 `attempt`，见 `void.lua:279`。refuted：仅凭“施加”不能断言译文明确承诺无条件生效；快照免疫检查见 `A/data/damage_types.lua:112–113`。 |
| O003 | Opus C01（原问题） | entry-03614 | mixed | confirmed：尝试限定遗漏。refuted：“写成必定生效”的绝对化表述过强。快照检查与目标版本适用性必须分开。 |
| O004 | Opus C02（原建议） | entry-03614 | advisory | 冻结抗性条目是面板／`_t` 语境，不能直接构成本条 `tformat` 的强制名称要求；“全体抗性”在此仍指全抗。 |
| O005 | 独立盲审 C02（原待确认） | entry-03614 | pending | P01。`void.lua:242–245` 清空行动能量；本体 `Actor.lua:168–170,761–773` 和 `GameEnergyBased.lua:124–129` 未支持固定半回合调度。 |
| O006 | Gemini C01（原问题） | entry-03616 | mixed | confirmed：拼接主语是触手，见 `writhing-body.lua:62–64`。pending：关于各项被动加成完全不受限制的扩展机制断言，本次未追完其全部消费实现，不作为 D02 的必要依据。 |
| O009 | 独立盲审 C04（原建议） | entry-03617 | advisory | 自爆和血肉爆炸信息仍在；问题为“光荣的血肉”的搭配。`misc.lua:47–61` 与参数重排一致。 |
| O012 | Sol C03（原问题） | entry-03620 | refuted | “力量”是分支标题，紧接“增加伤害”明确解释其效果；`misc.lua:257–260` 没有把该标题断言为 Strength 属性加成。可建议换词，不能确认机制混淆。 |
| O013 | Gemini C03（原问题） | entry-03620 | mixed | refuted：完整句子没有将 Power 写成力量属性增益。advisory：“所有伤害”可更明确，但无类型限定的“增加伤害”未明确收窄范围；`timed_effects.lua:2257` 为全伤害。 |
| O015 | 独立盲审 C05（原建议） | entry-03620 | refuted | 本包明确按 `source_tag/category/语境` 适用；匹配行的备注覆盖技能与状态说明。不能仅凭 `scope=core` 推出本 DLC 获得该名称要求的豁免。 |
| O020 | Opus C06（原建议） | entry-03623 | advisory | 在风味句中“黑暗和枯萎力量”不必然断言两种独立伤害类型；实际伤害句明确为暗影。`races.lua:74–78`、`timed_effects.lua:95`。 |
| O022 | Gemini C05（原建议） | entry-03624 | mixed | advisory：“无面孔的脸”的自然度。confirmed：`mind tricks` 改成“精神冲击”；风味叙述不因此免于语义审核。 |
| O026 | Sol C06（原问题） | entry-03626 | mixed | confirmed：复数泛指变成单一不明对象。refuted：不能说“某物”已经指明了某个身份确定的实体；缺陷是范围收窄。 |
| O027 | 独立盲审 C09（原待确认） | entry-03626 | pending | P02。`races.lua:149–162` 的首次强制使用与 `misc.lua:117` 的冷却 2 已核验；之后的实际 AI 调度未闭合。 |
| O029 | 独立盲审 C10（原待确认） | entry-03627 | pending | P03。死亡、非正伤害、震慑免疫检查先于首次记录建立；快照事实明确，目标版本适用性未固定。 |
| O030 | 独立盲审 C11（原待确认） | entry-03629 | pending | P04。`races.lua:238–241` 排除 `worthExp<=0`，而文字只说 100 个敌人；沿袭英文。 |
| O034 | Opus C09（原建议） | entry-03630 | advisory | 除 D10 已单独确认的专名外，句式生硬不再另计缺陷。 |
| O036 | Sol C09（原待确认） | entry-03632 | pending | P05。`getChance` 进入说明，但咬击动作没有消费该展示概率；`races.lua:382,398–412`。 |
| O037 | 独立盲审 C13（原待确认） | entry-03632 | pending | P05。本体 `canBe` 检查状态免疫，不能替代缺失的体质派生概率抽取；仍缺 DLC 版本映射。 |
| O038 | 独立盲审 C14（原待确认） | entry-03632 | pending | P06。`races.lua:398` 允许恰好 20% 的存活目标继续检查；英文和译文均写严格不足 20%。 |
| O042 | Opus C11（原问题） | entry-03633 | mixed | confirmed：遗漏 `better`。advisory：“全凭本能”可由 `Ultra Instinct／终极本能` 与无思维干扰的上下文支持，不单独确认无依据新增。 |
| O043 | 独立盲审 C15（原建议） | entry-03633 | refuted | 与 O015 相同，`scope=core` 本身不足以推翻本包明确的适用规则及机制备注；命中 D11。 |
| O048 | Sol C12（原建议） | entry-03642 | advisory | “+%d%% 所有造成的伤害”语序不自然，但层数、增幅及范围保留；`timed_effects.lua:292,305`。 |
| O049 | Sol C13（原建议） | entry-03643 | advisory | “牺牲者”有不同语感，但不必然指献祭对象；吸血语境见 `:466–483`。 |
| O050 | Opus C13（原建议） | entry-03643 | advisory | 汉语在这里省略显式所有格仍可承载受害关系；没有改成他人的受害者或无关对象。 |
| O051 | 独立盲审 C17（原问题） | entry-03643 | refuted | `victim→牺牲者` 不必然增加死亡、献祭或自愿牺牲条件；回调排除死亡目标也不能证明该中文词只指死者。 |
| O052 | Gemini C09（原建议） | entry-03645 | mixed | confirmed：观察自己指出的短暂目睹事件确有遗漏。refuted：不能仅因属于背景叙述就全部降为润色建议。 |
| O056 | Gemini C10（原问题） | entry-03646 | pending | P07。名称不一致可见，但 `madness.lua:123–134` 支持 Sanity Warp 作为额外伤害分支，不能只按状态名称判错。 |
| O057 | Sol C15（原问题） | entry-03646 | pending | P07。`HIDEOUS_VISIONS` 与 `CACOPHONY` 的定义本身不足以排除译文按实际伤害技能归属修订英文。 |
| O058 | Opus C15（原问题） | entry-03646 | mixed | pending：主名称问题归 P07。refuted：“额外时空伤害只在 Dark Whispers 结算”；`madness.lua:130–133` 还有幻象死亡后的时空投射。 |
| O059 | 独立盲审 C19（原待确认） | entry-03646 | pending | P07。独立核验支持其调用链判断；缺 `Sanity Warp↔失智冲击` 冻结映射及目标版本证据。 |
| O060 | Opus C16（原建议） | entry-03650 | advisory | 数值闪避与“闪避所有伤害”可区分，后者不必然被理解为一次防御对抗；`timed_effects.lua:1600–1602,1637`。 |
| O061 | 独立盲审 C20（原待确认） | entry-03651 | pending | P08。致命伤害转移不等于无条件处死；`:1716–1738`。治疗量由不幸覆盖幸运、并消耗对应效果的说明核验相符。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
