# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的55项观察及独立盲审的16项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03658 | C02（原问题） | C01（原问题） | C02（原问题） | `at the sight of the horror` 是目标看见恐魔；“在恐魔的视线中”反转观看关系。`S/data/timed_effects.lua:2330` 为获得提示。只确认叙述关系，不把英文修辞判成实际视线触发条件。 |
| D02 | entry-03668 | C04（原问题） | C02（原问题） | 未提出此缺陷 | `A page of the tome` 的定指归属被缩为“书页”。`S/data/zones/ft-horrors/objects.lua:25–32`：三份 NOTE 共用该描述，名称为分卷标题，未另外明确补回“属于所指书册”的关系。 |
| D03 | entry-03669 | 未提出此缺陷 | C03（原问题） | 未提出此缺陷 | `rolls` 的滚动动作改为“掉了出来”。`S/data/zones/ft-illusory-castle/grids.lua:92–97`：开箱放置物品后输出该叙述。物品生成逻辑没有使两种动作成为同义。 |
| D04 | entry-03681 | C08（原问题） | C04（原问题） | C03（原问题） | `creeking and vibrating` 只留下“颤动”，遗漏作响信息。`S/hooks/bonestaff.lua:22–26` 的骨杖开场及振动回应，使 `creeking` 的拼写误差可按 creaking 理解。 |
| D05 | entry-03683 | C10（原问题） | C05（原问题） | C04（原问题） | `pathetic excuse of a "necromancer"` 贬斥对方不配称为死灵法师，却译成对方“用……借口”。`S/hooks/bonestaff.lua:64,114–117`：要求停止召唤→骨杖辱骂→玩家解释理由。 |
| D06 | entry-03683 | C10（原问题） | 未提出此缺陷 | 未提出此缺陷 | 同句 `Stupid useless` 的“愚蠢、无用”评价遗漏；“蹩脚”在译文中修饰借口，不能承载对人的这两项评价。`S/hooks/bonestaff.lua:115`。与 D05 的习语指向错误分列。 |
| D07 | entry-03683 | C11（原建议） | 未提出此缺陷 | 未提出此缺陷 | `stays calm` 是持续平静，“平静了下来”新增由不平静到平静的变化。`S/hooks/bonestaff.lua:114–115`；相邻 enabled 分支的剧烈振动不是该节点必经前情。 |
| D08 | entry-03684 | 未提出此缺陷 | C06（原问题） | 未提出此缺陷 | 外界敌视 `such activities`，译文改为对“这些知识”不友好，改变敌视对象。`S/overload/data/texts/intro-cults.lua:23` 明确指向钻研活动。 |
| D09 | entry-03684 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | 独立的保密规则被收束为仅对知识保密。`S/overload/data/texts/intro-cults.lua:25` 将“避难所被发现便遭摧毁”与 `secrecy and safeguarding…knowledge` 连成因果，保密范围不只是知识内容。 |
| D10 | entry-03684 | C14（原建议） | 未提出此缺陷 | 未提出此缺陷 | `tunneling directly towards` 中掘进的移动方式遗漏，“直接冲向”未保留。`S/overload/data/texts/intro-cults.lua:27`。属于场景信息损失，不依赖运行时寻路行为。 |
| D11 | entry-03684 | C12（原问题） | 未提出此缺陷 | 未提出此缺陷 | 离开选项的 `while it is safe to do so` 遗漏。`S/overload/data/texts/intro-cults.lua:27,29`：前段“在蠕虫到来之前”并未明确提供末段的当前安全性判断。 |
| D12 | entry-03684 | C13（原问题） | 未提出此缺陷 | 未提出此缺陷 | `If nothing is done` 的“不采取行动”改为“不迅速做出决断”，替换了威胁描述的条件，并加入速度修饰。`S/overload/data/texts/intro-cults.lua:27`。仅确认叙述条件差异，不断言游戏把决策动作作为触发器。 |
| D13 | entry-03685 | 未提出此缺陷 | 未提出此缺陷 | C07（原问题） | “而你这样克罗格却……”的指示结构残缺，构成明确语法问题。`S/overload/data/texts/intro-krog.lua:24` 的 `you a Krog` 是说明玩家种族的同位结构。 |
| D14 | entry-03685 | C16（原问题） | C08（原问题） | C06（原问题） | 反魔力量来自对身体的改造，译文用“上面条件的附加作用”替代明确原因。`S/overload/data/texts/intro-krog.lua:24–26`；前段只交代剥除符文与自然力量维生，不能完整替代改造因果。 |
| D15 | entry-03685 | C16（原问题） | 未提出此缺陷 | 未提出此缺陷 | `by the Ziguranth` 修饰“对身体作出的改变”，译文改成“伊格兰斯的反魔法力量”，把改造施事改为力量所属者。`S/overload/data/texts/intro-krog.lua:26`。与 D14 分别记录因果和修饰归属。 |
| D16 | entry-03685 | C15（原问题） | C09（原问题） | C05（原问题） | `_t` 世界地名 `Maj'Eyal` 使用已被取代的“马基埃亚尔”。`S/overload/data/texts/intro-krog.lua:26` 与 INPUT 中 `Maj'Eyal / T.PN.WORLD / _t / preferred` 的明确要求直接匹配。 |
| D17 | entry-03689 | C19（原问题） | 未提出此缺陷 | 未提出此缺陷 | 遗漏 `while they are magic users` 的让步条件。`S/overload/data/texts/unlock-race_krog.lua:22–24`：符文维生背景仍在，但“尽管使用魔法，教团仍同情他们”的关系未保留。 |
| D18 | entry-03689 | C22（原建议） | 未提出此缺陷 | 未提出此缺陷 | `A mastery of infusions like no others` 的独有比较程度被缩为“自然纹身的大师”。`S/overload/data/texts/unlock-race_krog.lua:33`：“大师”表达高超，未表达“其他人无法相比”。这是轻微的语义信息遗漏。 |
| D19 | entry-03691 | C23（原问题） | C13（原问题） | C13（原问题） | `corrupted beyond hope` 描述腐化达到无可挽救的程度，译文“被绝望所腐化”改成腐化原因。`S/overload/data/texts/unlock-wyrmic_scourge.lua:21–22`，完整句法即可确认。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O001 | Gemini C01（原建议） | entry-03655 | advisory | `S/data/timed_effects.lua:2124,2138–2141` 的五项数值与译文对应；空格、逗号不改变消费。 |
| O002 | Opus C01（原建议） | entry-03655 | advisory | 同上；混乱免疫的百分数显示与 `confusion_immune` 改变量对应。 |
| O005 | Gemini C02（原问题） | entry-03658 | mixed | **confirmed**：观看关系错误。**refuted**：“同处一室目睹存活即获得”不是调用条件；施加还检查 `T_STONE_FORTRESS`，持续检查包含来源仍在当前层。 |
| O006 | Opus C02（原问题） | entry-03658 | mixed | **confirmed**：语义反转。快照未检查视线；但**refuted**“只要活着”这一充分条件概括，`:2337` 还检查层与实体存在。不能将快照提升为目标版本结论。 |
| O007 | Opus C03（原建议） | entry-03659 | advisory | `S/data/zones/entropic-void/grids.lua:34,39` 是同一裂隙；描述中的普通名词与实体标题无需逐字相同。 |
| O010 | Opus C04（原问题） | entry-03668 | mixed | **confirmed**：定指归属遗漏。**refuted**：同文件定义 `FORBIDDEN_TOME_HOME` 不能证明它就是这几页所属书册。 |
| O012 | Opus C05（原建议） | entry-03672 | advisory | `S/data/zones/godfeaster/zone.lua:137–145` 仍保留胃液将至和避险命令；“虫子”只是语体选择。 |
| O013 | Opus C06（原待确认） | entry-03673 | mixed | **pending**：P02，同键覆盖是否实际发生。**refuted**：覆盖必然导致同名商店各自显示不同；`E/…/engine/I18N.lua:41–69,100,141–143` 本身使用共享键。 |
| O014 | Opus C07（原待确认） | entry-03678 | mixed | **pending**：P03。**refuted**：由键相同直接推出运行时显示不一致；本包两条译文实际相同。 |
| O016 | Gemini C03（原问题） | entry-03681 | mixed | **confirmed**：声音信息遗漏。**advisory**：“手中／手上”的位置重复，未额外改变事实。 |
| O019 | Opus C09（原建议） | entry-03681 | advisory | 位置表达冗余；标记、引号及说话者结构仍完整。 |
| O021 | Gemini C04（原问题） | entry-03683 | mixed | **confirmed**：习语指向错误。**refuted**：触发前情是拒绝献技能点；实际入口是要求停止召唤，`:64` 跳转该节点。 |
| O028 | Sol C07（原问题） | entry-03684 | pending | P04。`Haze` 不等于 `chaos` 的词典区别，尚不足以证明专名“混沌纪”指向另一个时代；冻结术语未给适用命名裁决。 |
| O031 | Opus C12（原问题） | entry-03684 | mixed | **confirmed**：安全条件遗漏。**refuted**：“现在”必定只修饰传送门选项；“你可以现在 A 或者 B”可以共同覆盖两选项，不能另立时序缺陷。 |
| O033 | Opus C14（原建议） | entry-03684 | mixed | **confirmed**：掘进信息遗漏。**advisory**：禁忌知识、过去阴影及禁止实验的重复表达，完整段落未显示另一个具体事实错误。 |
| O035 | Gemini C06（原问题） | entry-03685 | mixed | **confirmed**：明确改造因果被弱化替换。**refuted**：必须恢复“外科”手术细节的论据，原句并未说明外科方式。 |
| O037 | Gemini C08（原建议） | entry-03685 | advisory | `kor'pul` 记录为 existing 且属 `newLore category`；另有 D16 不会扩大此记录权限。 |
| O044 | Opus C17（原建议） | entry-03685 | advisory | existing 名称不强制；段落仍可辨，空行减少没有证实结构丢失。 |
| O045 | Gemini C09（原建议） | entry-03686 | advisory | `unlock-demented_cultist_entropy.lua:20` 的职业、类别与颜色均保留，冒号样式无损。 |
| O046 | Opus C18（原建议） | entry-03686 | advisory | 与 O045 同一排版建议，不另立缺陷。 |
| O047 | 独立盲审 C11（原待确认） | entry-03687 | pending | P05。`A/data/talents/misc/races.lua:36–43`、`A/superload/mod/class/Actor.lua:113–123` 支持快照有限制；英文摘要也省略限制，目标版本未固定。 |
| O048 | 独立盲审 C12（原待确认） | entry-03687 | pending | P06。`races.lua:57–60` 给攻击者施加效果，`S/data/timed_effects.lua:85–95` 在该攻击者身上流血、结算伤害；存在上游同类误述，目标版本待确认。 |
| O049 | Sol C10（原问题） | entry-03689 | pending | P07。此处 `Zigur` 是创造种族的施事，有借地名指共同体的可能，不能直接当作纯地点用途套用。 |
| O050 | Gemini C10（原问题） | entry-03689 | pending | P07。术语确实区分地点与教团，但现有备注没有明确裁决此处施事借代；同段保护对象实际正确译作“伊格”。 |
| O051 | Sol C11（原问题） | entry-03689 | refuted | 冻结译文是“伊格的坚实保护者”，不是该观察引用的“伊格兰斯”。不能借同条其他问题确认此项。 |
| O052 | Gemini C11（原问题） | entry-03689 | advisory | 段末缺感叹号存在，但随后空行明确结束段落；未造成错误显示或信息结构损失。 |
| O053 | Gemini C12（原问题） | entry-03689 | mixed | **pending**：P08，抗性描述范围。**refuted**：反魔种族抵抗魔法必然违背设定；抵抗能力不等于施法。实际龙血定义在 `races.lua:215–296`，是可选一种类型，非同时获得所列六种抗性。 |
| O054 | Sol C12（原待确认） | entry-03689 | pending | P08。补查到龙血定义及本体抗性消费；快照按伤害类型处理，目标版本对应关系仍缺。 |
| O056 | 独立盲审 C14（原问题） | entry-03689 | pending | P07。原文专名交替可证明用词不同，尚不能单独排除本句的借代译法。 |
| O057 | 独立盲审 C15（原问题） | entry-03689 | pending | P08。“魔法”是增译，但整段未写“仅限施法来源”；不能只靠该词宣布排他机制条件已证实。快照范围证据支持继续核验。 |
| O059 | Opus C20（原待确认） | entry-03689 | pending | P07。借代适用性确有未决点，不扩大为全局术语策略。 |
| O060 | Opus C21（原待确认） | entry-03689 | pending | P08。相关天赋实际位于获准额外清单，可由龙血能力追查；原观察“不能引入”的限制判断不成立，但目标版本缺口仍在。 |
| O061 | Opus C22（原建议） | entry-03689 | mixed | **confirmed**：“无人能及”的比较程度遗漏。**advisory**：段末标点；“纹身”本身没有术语问题。 |
| O063 | Gemini C13（原问题） | entry-03691 | mixed | **confirmed**：`beyond hope` 误解。**pending／不采作证据**：附带的具体腐化成因没有在本次读取链中证实，也不是确认 D19 所必需。 |
| O064 | Sol C14（原问题） | entry-03691 | advisory | “受伤的地方”直译生硬，但后半句明确说明负面效果增加伤害；没有足够依据把修辞判成必须存在实体伤口的条件。 |
| O065 | Gemini C14（原问题） | entry-03691 | advisory | 缺句号但空行和“技能列表”清楚分隔，未证实运行时或结构缺陷。 |
| O068 | Opus C24（原待确认） | entry-03691 | pending | P09。快照 `scourge-drake.lua:129–138` 明确按过滤后的效果数量逐次追加伤害，支持数量关系；目标版本及过滤范围须分别保留。 |
| O069 | Opus C25（原建议） | entry-03691 | advisory | 段落仍可辨，标记完整；句末标点和“天谴龙／天谴之龙”的叙述名称差异不足以立缺陷。 |
| O070 | Sol C15（原问题） | entry-03692 | refuted | 同一资源描述第三段明确写“浮动的几率”；整体未将随机触发改成必然。 |
| O071 | Opus C26（原问题） | entry-03692 | refuted | “下一句不能补回”的绝对判断不成立。`CultsDLC.lua:47` 传入完整三段说明；`E/…/ActorResource.lua:45–58` 保存整段 description，概率文字属于同一说明。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
