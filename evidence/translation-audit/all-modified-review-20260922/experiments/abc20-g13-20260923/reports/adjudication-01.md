完成全 40 条复核及 71 项匿名观察归并：**9 条 ISSUE、4 条 PENDING、27 条 OK；确认 19 项独立缺陷**。OK 包含仅措辞或排版建议。

下文 `S/` 指本包 `sources/dlc/cults/tome-cults/`，`A/` 指获准额外快照中的 `tome-cults/`。这些 DLC 文件均已核对清单哈希，但源码仓库、commit 及目标版本对应关系未固定。`E/` 指本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的路径。

| entry-ID | 判定 | canonical D／P 编号或简短依据 |
|---|---|---|
| entry-03653 | OK | 缓慢转移至禁忌之书，语义与状态描述相符。 |
| entry-03654 | PENDING | P01：实际清除调用排除 `other` 类；英文亦有同样概括。 |
| entry-03655 | OK | 五个参数顺序、类型与含义一致；标点仅建议。 |
| entry-03656 | OK | 身体进化的获得提示准确。 |
| entry-03657 | OK | 熵能包覆的获得提示准确。 |
| entry-03658 | ISSUE | D01：观看者与被观看者颠倒。 |
| entry-03659 | OK | “裂缝／裂隙”及省略号差异仅建议。 |
| entry-03660 | OK | 训练傀儡用途准确。 |
| entry-03661 | OK | 人类学徒准确。 |
| entry-03662 | OK | 永恒精灵学徒准确。 |
| entry-03663 | OK | 半身人学徒准确。 |
| entry-03664 | OK | 尖叫提示及颜色标记准确。 |
| entry-03665 | OK | 源码为格朗格攻击后激怒强大存在，主客体准确。 |
| entry-03666 | OK | 发言者名称及 `%s` 消费准确。 |
| entry-03667 | OK | 安全存放物品的含义保留。 |
| entry-03668 | ISSUE | D02：遗漏书页与所指书册的归属关系。 |
| entry-03669 | ISSUE | D03：滚出改为掉出。 |
| entry-03670 | OK | 颜色、章节名两个 `%s` 顺序正确。 |
| entry-03671 | OK | 尖叫提示及颜色标记准确。 |
| entry-03672 | OK | 胃液预警和躲入凹室的操作信息保留。 |
| entry-03673 | PENDING | P02：跨组件同键覆盖的实际输入与加载顺序未获准核验。 |
| entry-03674 | OK | 商店名称译义可接受。 |
| entry-03675 | OK | 商店名称译义可接受。 |
| entry-03676 | OK | 攻击命令及 `@himher@` 保留。 |
| entry-03677 | OK | 德瑞姆邪教徒准确。 |
| entry-03678 | PENDING | P03：与 P02 相同的独立条目疑点。 |
| entry-03679 | OK | 商店名称译义可接受。 |
| entry-03680 | OK | 商店名称译义可接受。 |
| entry-03681 | ISSUE | D04：遗漏骨杖作响；位置重复仅建议。 |
| entry-03682 | OK | 回答语气与对话分支相符。 |
| entry-03683 | ISSUE | D05–D07：辱骂习语误解、修饰信息遗漏、状态变化误写。 |
| entry-03684 | ISSUE | D08–D12；另有 P04：时代专名译法待确认。 |
| entry-03685 | ISSUE | D13–D16：语法、因果、修饰归属及适用术语问题。 |
| entry-03686 | OK | 职业与类别准确；冒号排版仅建议。 |
| entry-03687 | PENDING | P05、P06：狂热范围及黑血主体的快照差异，目标版本未固定。 |
| entry-03688 | OK | 种族解锁标题准确。 |
| entry-03689 | ISSUE | D17、D18；另有 P07、P08：借代术语与抗性描述范围。 |
| entry-03690 | OK | 技能树解锁标题准确。 |
| entry-03691 | ISSUE | D19；另有 P09：数量关系的目标版本及过滤范围。 |
| entry-03692 | OK | 整段明确保留浮动概率；没有证实“必然触发”误述。 |

确认缺陷均为**译文相对英文新增的偏差**，不是沿袭英文的机制误述；这里的“新增”不表示由本次历史提交首次引入。

| D-ID | entry-ID | 内容、归因及源码／语境证据 |
|---|---|---|
| D01 | entry-03658 | `at the sight of the horror` 是目标看见恐魔；“在恐魔的视线中”反转观看关系。`S/data/timed_effects.lua:2330` 为获得提示。只确认叙述关系，不把英文修辞判成实际视线触发条件。 |
| D02 | entry-03668 | `A page of the tome` 的定指归属被缩为“书页”。`S/data/zones/ft-horrors/objects.lua:25–32`：三份 NOTE 共用该描述，名称为分卷标题，未另外明确补回“属于所指书册”的关系。 |
| D03 | entry-03669 | `rolls` 的滚动动作改为“掉了出来”。`S/data/zones/ft-illusory-castle/grids.lua:92–97`：开箱放置物品后输出该叙述。物品生成逻辑没有使两种动作成为同义。 |
| D04 | entry-03681 | `creeking and vibrating` 只留下“颤动”，遗漏作响信息。`S/hooks/bonestaff.lua:22–26` 的骨杖开场及振动回应，使 `creeking` 的拼写误差可按 creaking 理解。 |
| D05 | entry-03683 | `pathetic excuse of a "necromancer"` 贬斥对方不配称为死灵法师，却译成对方“用……借口”。`S/hooks/bonestaff.lua:64,114–117`：要求停止召唤→骨杖辱骂→玩家解释理由。 |
| D06 | entry-03683 | 同句 `Stupid useless` 的“愚蠢、无用”评价遗漏；“蹩脚”在译文中修饰借口，不能承载对人的这两项评价。`S/hooks/bonestaff.lua:115`。与 D05 的习语指向错误分列。 |
| D07 | entry-03683 | `stays calm` 是持续平静，“平静了下来”新增由不平静到平静的变化。`S/hooks/bonestaff.lua:114–115`；相邻 enabled 分支的剧烈振动不是该节点必经前情。 |
| D08 | entry-03684 | 外界敌视 `such activities`，译文改为对“这些知识”不友好，改变敌视对象。`S/overload/data/texts/intro-cults.lua:23` 明确指向钻研活动。 |
| D09 | entry-03684 | 独立的保密规则被收束为仅对知识保密。`S/overload/data/texts/intro-cults.lua:25` 将“避难所被发现便遭摧毁”与 `secrecy and safeguarding…knowledge` 连成因果，保密范围不只是知识内容。 |
| D10 | entry-03684 | `tunneling directly towards` 中掘进的移动方式遗漏，“直接冲向”未保留。`S/overload/data/texts/intro-cults.lua:27`。属于场景信息损失，不依赖运行时寻路行为。 |
| D11 | entry-03684 | 离开选项的 `while it is safe to do so` 遗漏。`S/overload/data/texts/intro-cults.lua:27,29`：前段“在蠕虫到来之前”并未明确提供末段的当前安全性判断。 |
| D12 | entry-03684 | `If nothing is done` 的“不采取行动”改为“不迅速做出决断”，替换了威胁描述的条件，并加入速度修饰。`S/overload/data/texts/intro-cults.lua:27`。仅确认叙述条件差异，不断言游戏把决策动作作为触发器。 |
| D13 | entry-03685 | “而你这样克罗格却……”的指示结构残缺，构成明确语法问题。`S/overload/data/texts/intro-krog.lua:24` 的 `you a Krog` 是说明玩家种族的同位结构。 |
| D14 | entry-03685 | 反魔力量来自对身体的改造，译文用“上面条件的附加作用”替代明确原因。`S/overload/data/texts/intro-krog.lua:24–26`；前段只交代剥除符文与自然力量维生，不能完整替代改造因果。 |
| D15 | entry-03685 | `by the Ziguranth` 修饰“对身体作出的改变”，译文改成“伊格兰斯的反魔法力量”，把改造施事改为力量所属者。`S/overload/data/texts/intro-krog.lua:26`。与 D14 分别记录因果和修饰归属。 |
| D16 | entry-03685 | `_t` 世界地名 `Maj'Eyal` 使用已被取代的“马基埃亚尔”。`S/overload/data/texts/intro-krog.lua:26` 与 INPUT 中 `Maj'Eyal / T.PN.WORLD / _t / preferred` 的明确要求直接匹配。 |
| D17 | entry-03689 | 遗漏 `while they are magic users` 的让步条件。`S/overload/data/texts/unlock-race_krog.lua:22–24`：符文维生背景仍在，但“尽管使用魔法，教团仍同情他们”的关系未保留。 |
| D18 | entry-03689 | `A mastery of infusions like no others` 的独有比较程度被缩为“自然纹身的大师”。`S/overload/data/texts/unlock-race_krog.lua:33`：“大师”表达高超，未表达“其他人无法相比”。这是轻微的语义信息遗漏。 |
| D19 | entry-03691 | `corrupted beyond hope` 描述腐化达到无可挽救的程度，译文“被绝望所腐化”改成腐化原因。`S/overload/data/texts/unlock-wyrmic_scourge.lua:21–22`，完整句法即可确认。 |

| O-ID | 状态 | 命中 D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | advisory | — | `S/data/timed_effects.lua:2124,2138–2141` 的五项数值与译文对应；空格、逗号不改变消费。 |
| O002 | advisory | — | 同上；混乱免疫的百分数显示与 `confusion_immune` 改变量对应。 |
| O003 | confirmed | D01 | 获得提示确实反转观看关系；不据 `eff.src` 推定视线机制。 |
| O004 | confirmed | D01 | `S/data/timed_effects.lua:2330`；`A/data/talents/misc/races.lua:164–165` 给召唤者施加效果，未改变句法主体。 |
| O005 | mixed | D01 | **confirmed**：观看关系错误。**refuted**：“同处一室目睹存活即获得”不是调用条件；施加还检查 `T_STONE_FORTRESS`，持续检查包含来源仍在当前层。 |
| O006 | mixed | D01 | **confirmed**：语义反转。快照未检查视线；但**refuted**“只要活着”这一充分条件概括，`:2337` 还检查层与实体存在。不能将快照提升为目标版本结论。 |
| O007 | advisory | — | `S/data/zones/entropic-void/grids.lua:34,39` 是同一裂隙；描述中的普通名词与实体标题无需逐字相同。 |
| O008 | confirmed | D02 | `objects.lua:25–32` 确认 NOTE 描述；只确认“所指书册”归属遗漏，不指定书名。 |
| O009 | confirmed | D02 | 三份 NOTE 共用描述；冻结上下文没有其他明确归属文字抵消该遗漏。 |
| O010 | mixed | D02 | **confirmed**：定指归属遗漏。**refuted**：同文件定义 `FORBIDDEN_TOME_HOME` 不能证明它就是这几页所属书册。 |
| O011 | confirmed | D03 | `grids.lua:95–96` 的消息明确叙述滚出；生成物品与动作细节是不同层面。 |
| O012 | advisory | — | `S/data/zones/godfeaster/zone.lua:137–145` 仍保留胃液将至和避险命令；“虫子”只是语体选择。 |
| O013 | mixed | — | **pending**：P02，同键覆盖是否实际发生。**refuted**：覆盖必然导致同名商店各自显示不同；`E/…/engine/I18N.lua:41–69,100,141–143` 本身使用共享键。 |
| O014 | mixed | — | **pending**：P03。**refuted**：由键相同直接推出运行时显示不一致；本包两条译文实际相同。 |
| O015 | confirmed | D04 | `S/hooks/bonestaff.lua:24` 并列两个感官动作，译文仅保留振动。 |
| O016 | mixed | D04 | **confirmed**：声音信息遗漏。**advisory**：“手中／手上”的位置重复，未额外改变事实。 |
| O017 | confirmed | D04 | 同一开场文本中作响信息遗漏；不依赖音效是否播放。 |
| O018 | confirmed | D04 | 同上；影响轻微不改变遗漏事实。 |
| O019 | advisory | — | 位置表达冗余；标记、引号及说话者结构仍完整。 |
| O020 | confirmed | D05、D06 | `bonestaff.lua:64,115,117` 支持习语误译和辱骂修饰遗漏；后续解释不能把先前辱骂变成“提出借口”。 |
| O021 | mixed | D05 | **confirmed**：习语指向错误。**refuted**：触发前情是拒绝献技能点；实际入口是要求停止召唤，`:64` 跳转该节点。 |
| O022 | confirmed | D05 | 对身份的贬损被改成对借口的指责，`:115` 可直接判定。 |
| O023 | confirmed | D07 | `stays` 与“了下来”的持续／转变关系不同。 |
| O024 | confirmed | D05、D06 | 对话顺序及修饰词遗漏均由 `:64,115,117` 支持。 |
| O025 | confirmed | D07 | 观察指出的状态差异成立；不能仅因结果都平静就降为措辞偏好。 |
| O026 | confirmed | D08 | `intro-cults.lua:23` 指活动，译文指知识，宾语范围改变。 |
| O027 | confirmed | D09 | `intro-cults.lua:25` 的发现—摧毁—保密因果支持独立的隐匿要求。 |
| O028 | pending | — | P04。`Haze` 不等于 `chaos` 的词典区别，尚不足以证明专名“混沌纪”指向另一个时代；冻结术语未给适用命名裁决。 |
| O029 | confirmed | D10 | `intro-cults.lua:27` 明示掘进，“冲向”遗漏该方式。 |
| O030 | confirmed | D11 | `intro-cults.lua:29` 的当前安全说明没有译出。 |
| O031 | mixed | D11 | **confirmed**：安全条件遗漏。**refuted**：“现在”必定只修饰传送门选项；“你可以现在 A 或者 B”可以共同覆盖两选项，不能另立时序缺陷。 |
| O032 | confirmed | D12 | 行动条件被替为迅速决断，`:27` 可作文本层面对照。 |
| O033 | mixed | D10 | **confirmed**：掘进信息遗漏。**advisory**：禁忌知识、过去阴影及禁止实验的重复表达，完整段落未显示另一个具体事实错误。 |
| O034 | confirmed | D16 | INPUT 的 preferred 记录直接适用，不是根据一般间隔号习惯判错。 |
| O035 | mixed | D14 | **confirmed**：明确改造因果被弱化替换。**refuted**：必须恢复“外科”手术细节的论据，原句并未说明外科方式。 |
| O036 | confirmed | D13 | “你这样克罗格”的结构残缺客观存在，源文同位关系清楚。 |
| O037 | advisory | — | `kor'pul` 记录为 existing 且属 `newLore category`；另有 D16 不会扩大此记录权限。 |
| O038 | confirmed | D14 | `intro-krog.lua:24–26` 的明确身体改造原因被不明确回指替代。 |
| O039 | confirmed | D16 | 与适用 preferred 世界地名记录冲突。 |
| O040 | confirmed | D14、D15 | 原因和 `by the Ziguranth` 的修饰归属分别改变。 |
| O041 | confirmed | D16 | 原文标签、地名语境与术语记录匹配。 |
| O042 | confirmed | D16 | 正文违反明确术语要求；相邻标题采用新译可作辅助，非唯一依据。 |
| O043 | confirmed | D14、D15 | 译文回指替代身体改造，并把施事改成力量所属者。 |
| O044 | advisory | — | existing 名称不强制；段落仍可辨，空行减少没有证实结构丢失。 |
| O045 | advisory | — | `unlock-demented_cultist_entropy.lua:20` 的职业、类别与颜色均保留，冒号样式无损。 |
| O046 | advisory | — | 与 O045 同一排版建议，不另立缺陷。 |
| O047 | pending | — | P05。`A/data/talents/misc/races.lua:36–43`、`A/superload/mod/class/Actor.lua:113–123` 支持快照有限制；英文摘要也省略限制，目标版本未固定。 |
| O048 | pending | — | P06。`races.lua:57–60` 给攻击者施加效果，`S/data/timed_effects.lua:85–95` 在该攻击者身上流血、结算伤害；存在上游同类误述，目标版本待确认。 |
| O049 | pending | — | P07。此处 `Zigur` 是创造种族的施事，有借地名指共同体的可能，不能直接当作纯地点用途套用。 |
| O050 | pending | — | P07。术语确实区分地点与教团，但现有备注没有明确裁决此处施事借代；同段保护对象实际正确译作“伊格”。 |
| O051 | refuted | — | 冻结译文是“伊格的坚实保护者”，不是该观察引用的“伊格兰斯”。不能借同条其他问题确认此项。 |
| O052 | advisory | — | 段末缺感叹号存在，但随后空行明确结束段落；未造成错误显示或信息结构损失。 |
| O053 | mixed | — | **pending**：P08，抗性描述范围。**refuted**：反魔种族抵抗魔法必然违背设定；抵抗能力不等于施法。实际龙血定义在 `races.lua:215–296`，是可选一种类型，非同时获得所列六种抗性。 |
| O054 | pending | — | P08。补查到龙血定义及本体抗性消费；快照按伤害类型处理，目标版本对应关系仍缺。 |
| O055 | confirmed | D17 | `unlock-race_krog.lua:24` 的显式让步关系遗漏。 |
| O056 | pending | — | P07。原文专名交替可证明用词不同，尚不能单独排除本句的借代译法。 |
| O057 | pending | — | P08。“魔法”是增译，但整段未写“仅限施法来源”；不能只靠该词宣布排他机制条件已证实。快照范围证据支持继续核验。 |
| O058 | confirmed | D17 | 同 O055；前段符文背景不能替代让步关系。 |
| O059 | pending | — | P07。借代适用性确有未决点，不扩大为全局术语策略。 |
| O060 | pending | — | P08。相关天赋实际位于获准额外清单，可由龙血能力追查；原观察“不能引入”的限制判断不成立，但目标版本缺口仍在。 |
| O061 | mixed | D18 | **confirmed**：“无人能及”的比较程度遗漏。**advisory**：段末标点；“纹身”本身没有术语问题。 |
| O062 | confirmed | D19 | 程度被误写为腐化原因，完整句法明确。 |
| O063 | mixed | D19 | **confirmed**：`beyond hope` 误解。**pending／不采作证据**：附带的具体腐化成因没有在本次读取链中证实，也不是确认 D19 所必需。 |
| O064 | advisory | — | “受伤的地方”直译生硬，但后半句明确说明负面效果增加伤害；没有足够依据把修辞判成必须存在实体伤口的条件。 |
| O065 | advisory | — | 缺句号但空行和“技能列表”清楚分隔，未证实运行时或结构缺陷。 |
| O066 | confirmed | D19 | 仅采其句法误译观察；附带的其他条目统计与自述读取结果不作为本次证据。 |
| O067 | confirmed | D19 | 与 D19 同义归并，不重复计数。 |
| O068 | pending | — | P09。快照 `scourge-drake.lua:129–138` 明确按过滤后的效果数量逐次追加伤害，支持数量关系；目标版本及过滤范围须分别保留。 |
| O069 | advisory | — | 段落仍可辨，标记完整；句末标点和“天谴龙／天谴之龙”的叙述名称差异不足以立缺陷。 |
| O070 | refuted | — | 同一资源描述第三段明确写“浮动的几率”；整体未将随机触发改成必然。 |
| O071 | refuted | — | “下一句不能补回”的绝对判断不成立。`CultsDLC.lua:47` 传入完整三段说明；`E/…/ActorResource.lua:45–58` 保存整段 description，概率文字属于同一说明。 |

未决项单列如下，不计入 D：

- **P01｜entry-03654，独立补充。** `S/data/timed_effects.lua:2073–2074` 调用 `removeEffectsFilter(self,{status="detrimental"},999)`；`E/game/modules/tome/class/Actor.lua:7144–7180` 默认排除 `other`，再通过 `dispel` 清除。因此“所有负面效果”比已读实现宽，英文同样如此。归因为**沿袭上游概括**；尚缺 DLC 快照对目标版本的适用证明。
- **P02、P03｜entry-03673、entry-03678。** 已证实引擎不以 section 分键；未获准读取本体当前该键译文与实际加载顺序。`existing` 术语不能证明实际冲突，也不能强制改名。两条分别保留，不把假设覆盖判作已发生故障。
- **P04｜entry-03684。** 需要该时代的明确命名或指称证据，才能裁决“混沌纪”。目前不能由 `haze≠chaos` 直接推出译文换了时代。
- **P05｜entry-03687。** 快照狂热持续三回合，仅令符合条件的职业技能首次使用免冷却。解锁摘要没有这些限制，属于**上游与译文共有的简化**；既不能宣称所有技能每次免冷却，也不能把全部限制遗漏归给译者。目标版本适用性未决。
- **P06｜entry-03687。** 快照中攻击者自身流出黑血，译文呈现黑血溅到攻击者身上；英文 `your black blood on your attackers` 也存在主体误导。属于**至少部分沿袭上游**，目标版本未固定。
- **P07｜entry-03689。** “伊格终于创造……”的施事借代是否必须保留地名，冻结规则没有明确覆盖；纯地点语境下不得写“伊格兰斯”的规定，不能不经判定直接扩展到全部借代。需要针对本句的有界术语裁决。
- **P08｜entry-03689。** `A/data/talents/misc/races.lua:224–235,254–275` 向选定类型写入 `resists`；`E/game/modules/tome/data/damage_types.lua:352–374` → `E/game/modules/tome/class/interface/Combat.lua:2310–2321` 按类型消费，没有“必须由魔法造成”的来源过滤。**快照内该限制不存在**；但译文是否将“元素魔法伤害”用作排他分类，以及 DLC 目标版本适用性仍需确认，不能只按一个词立机制缺陷。
- **P09｜entry-03691。** 快照每个有效负面效果追加一段伤害，后一段为前一段的 75%，故“越多伤害越高”有依据。`effectsFilter` 排除 `other`，而摘要未说明这一范围，英文也未说明。目标版本对应关系未固定；保留该范围与适用性缺口，不认定数量关系是无据增译。

主要分歧按完整语境处理：保留“保持平静→平静下来”、声音遗漏、比较程度遗漏等具体信息差异；排版不齐不升级为缺陷；“任何攻击能够震慑”在种族特色中表达攻击类型能力，没有据此新增“每次必定震慑”的缺陷。概率说明、伤口修辞和抗性分类也分别核验，没有用观察数量代替证据。

实际读取范围如下。没有读取模型身份、来源映射、原始报告、STATE 或其他轮答案；O066 在入口内夹带的报告统计没有作为证据。未修改仓库、未创建临时文件、未创建子 agent。

本包根目录 `P`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923
```

读取的冻结输入：

```text
P/ADJUDICATION-INPUT.md
P/INPUT.md
P/entries.json
P/context.lua
P/source-access.json
```

读取并核对哈希的 23 个包内源码文件，以下相对 `P/sources/dlc/cults/tome-cults/`；内容阅读限于对应条目及相关上下文，哈希校验覆盖完整文件：

```text
data/timed_effects.lua
data/zones/entropic-void/grids.lua
data/zones/ft-cultist/npcs.lua
data/zones/ft-haze-cave/grids.lua
data/zones/ft-haze-cave/npcs.lua
data/zones/ft-haze-cave/zone.lua
data/zones/ft-home/grids.lua
data/zones/ft-horrors/objects.lua
data/zones/ft-illusory-castle/grids.lua
data/zones/ft-illusory-castle/zone.lua
data/zones/ft-yaech/grids.lua
data/zones/godfeaster/zone.lua
data/zones/test/traps.lua
data/zones/town-kroshkkur/npcs.lua
data/zones/town-kroshkkur/traps.lua
hooks/bonestaff.lua
overload/data/texts/intro-cults.lua
overload/data/texts/intro-krog.lua
overload/data/texts/unlock-demented_cultist_entropy.lua
overload/data/texts/unlock-race_drem.lua
overload/data/texts/unlock-race_krog.lua
overload/data/texts/unlock-wyrmic_scourge.lua
overload/mod/class/CultsDLC.lua
```

额外 DLC 根目录为清单明确授权的：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults
```

仅读取其中三个获准、哈希匹配的源码单文件：

- `tome-cults/data/talents/misc/races.lua`：由已读 `HORRIFIC_FORTRESS`、Frenzy、黑血和龙血种族能力引入。
- `tome-cults/superload/mod/class/Actor.lua`：由 `CultsDLC.lua:51` 的 `insanityEffectForce()` 及 `DREM_FRENZY` 冷却消费引入。
- `tome-cults/data/talents/demented/scourge-drake.lua`：由解锁说明明确列出的四个技能名称引入。

本体仅通过 `/workspace/t-engine4` 的 `git show` 读取固定 commit 下这些单文件：

```text
game/engines/default/engine/I18N.lua
game/engines/default/engine/interface/ActorResource.lua
game/modules/tome/class/Actor.lua
game/modules/tome/data/damage_types.lua
game/modules/tome/class/interface/Combat.lua
```

引入依据依次是 `_t／tformat` 键与参数消费、`defineResource`、`removeEffectsFilter／effectsFilter`、`DamageType.projector`、`combatGetResist`。40 条的格式参数、颜色／样式标记及名称替换标记也已比对，未发现不一致；换行差异另按信息结构审查。以上为只读审核裁决，不代表生产验收结论。
