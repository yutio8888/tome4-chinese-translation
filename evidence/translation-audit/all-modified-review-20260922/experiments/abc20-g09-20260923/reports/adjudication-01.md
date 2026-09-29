完成全 40 条复核及 129 项匿名观察裁决：**9 条 ISSUE，31 条 OK**；归并为 **59 项确认缺陷**。DLC 结论限定于获准的哈希快照，目标发行版本适用性另列 P01。

| entry-ID | 判定 | canonical D或P编号／简短依据 |
|---|---|---|
| entry-03493 | OK | Maggot 区域及脊髓实体支持巨大生物语境；无适用的强制专名要求。 |
| entry-03494 | OK | 攻击细胞、接近及分散注意力的关系保留。 |
| entry-03495 | OK | 反讽语气及 radiant horror 指称保留。 |
| entry-03496 | ISSUE | D01、D02；nether 的机制混淆指控不成立。 |
| entry-03497 | ISSUE | D03、D04。 |
| entry-03498 | ISSUE | D05。 |
| entry-03499 | OK | 战斗状态禁止脱下与日志一致。 |
| entry-03500 | OK | 穿戴、物品参数及与体内恐魔协调的关系保留。 |
| entry-03501 | OK | “使用法杖掌控”的操作语境已表明能够交谈；仅建议。 |
| entry-03502 | OK | `combat_spellcrit` 增加 3，与译文一致。 |
| entry-03503 | OK | `combat_spellresist` 增加 10，与译文一致。 |
| entry-03504 | OK | `mag` 增加 5，与译文一致。 |
| entry-03505 | OK | `wil` 增加 5，与译文一致。 |
| entry-03506 | OK | `combat_def` 增加 10，与译文一致。 |
| entry-03507 | OK | `movement_speed` 增加 0.1，与译文一致。 |
| entry-03508 | OK | `dex` 增加 5，与译文一致。 |
| entry-03509 | OK | `cun` 增加 5，与译文一致。 |
| entry-03510 | OK | 两个参数依次为装备与目标；触手抓握符合回调语境。 |
| entry-03511 | OK | 穿戴回调、玩家为 Krog 及共鸣增强的完整语境成立；仅建议。 |
| entry-03512 | OK | 双武器套装完成与力量增强的提示相符。 |
| entry-03513 | ISSUE | D06。 |
| entry-03514 | OK | “两件”可指两件鞋类装备；量词仅建议。 |
| entry-03515 | OK | 三个参数依次为使用者、所属代词、装备名；未见消费顺序错误。 |
| entry-03516 | OK | 当前及后续巡逻实体均处理移动速度；永久减缓说明相符。 |
| entry-03517 | ISSUE | D07–D21。 |
| entry-03518 | OK | 卷章及标题含义相符。 |
| entry-03519 | OK | 标题与拒用纹身的正文语境相符。 |
| entry-03520 | OK | 卷章及永恒精灵受苦的含义保留。 |
| entry-03521 | OK | Medical Treatment 译作“医疗”可接受。 |
| entry-03522 | ISSUE | D22–D33。 |
| entry-03523 | OK | 人名、将军身份与卷章相符。 |
| entry-03524 | OK | 离开埃尔瓦拉及卷章相符。 |
| entry-03525 | OK | 大门口及卷章相符。 |
| entry-03526 | OK | 交换情报及卷章相符。 |
| entry-03527 | ISSUE | D34–D46。 |
| entry-03528 | OK | 标题与火灾、狂热行为的语境相符。 |
| entry-03529 | OK | 暴行及贬斥含义保留。 |
| entry-03530 | OK | 灵能诡计及卷章相符。 |
| entry-03531 | ISSUE | D47–D58。 |
| entry-03532 | ISSUE | D59。 |

以下证据简称均对应实际读取的源码：`W`＝`tome-cults/data/general/objects/world-artifacts.lua`，`H`＝`tome-cults/data/general/npcs/horror.lua`，`D`＝`tome-cults/data/lore/dremwarves.lua`，`F`＝`tome-cults/data/lore/fay-willows.lua`。这些是**哈希固定、源码 commit 未固定的 DLC 快照**。

下表全部 D 均为**译文相对英文新增的偏差**，不是沿袭英文已有的同类错误；此处归因不表示它们一定由本次修改首次引入。

| D-ID | entry-ID | 内容、归因及源码证据 |
|---|---|---|
| D01 | entry-03496 | 漏掉水晶的 `strange` 描写；译文只有“高大”。H:131。 |
| D02 | entry-03496 | `pulsing` 的脉动变成“发射出”，改变能量运动方式。上游拼作 `pusling`，不影响辨认。H:131。 |
| D03 | entry-03497 | `writhing` 的持续扭动变成“扭曲／弯曲成”的形态描述，动态信息遗漏。W:99。 |
| D04 | entry-03497 | `roughtly warped into the form of a ring` 中“大致成形”的限定遗漏。W:99；不据此声称译文断言了完美圆形。 |
| D05 | entry-03498 | 漏译指环首次与佩戴者调谐的关系，直接进入选择觉醒技能。W:104；穿戴流程 W:201–215、`RingOfTheHunter.lua:55–64` 支持选择和授予机制。 |
| D06 | entry-03513 | `somehow do not like the idea` 的说不清缘由的抗拒，改为明确而强烈的“实在是太恶心了”。心理态度仍在，但不确定性及强度改变。W:800。 |
| D07 | entry-03517 | `such a concentration` 被写成“根本不可能存在于埃亚尔集中出现”，语法混杂，未清楚表达受限制的是这种能量的浓度。D:56。 |
| D08 | entry-03517 | 管道容纳“队伍中一人且有余量”变成容许“一个小队在里面行走”，改变人数和空间尺度。D:58、70。 |
| D09 | entry-03517 | 一台机器变成“一些巨大的机器”，末段同一房间的机器又变成“这些机器”。D:62、66、72 明确区分眼前一台与其他机器。 |
| D10 | entry-03517 | `half formed fetuses` 泛化为“不成型的生命体”，遗漏胎儿发育阶段。D:64；D:72 的起源推断依赖这一特征。 |
| D11 | entry-03517 | `latched onto my arm` 的攀附／扣住被确定为“咬了一口”，新增具体感染动作。D:66；前文利齿不能证明这里发生咬伤。 |
| D12 | entry-03517 | `my flesh wither away and turned into dried leather` 缩窄为“肌肉萎缩，看起来如同……皮革”，改变受损组织及变化描述。D:66。 |
| D13 | entry-03517 | “不止我感染”变为“其他人也都感染”，扩大为全员感染。D:68。 |
| D14 | entry-03517 | 叙述者个人接受命运的 `I am content` 变为“我们……充实和满足”，扩大感受主体。D:68。 |
| D15 | entry-03517 | 同一房间的后部变成“那些还有更多管子的房间里面”，丢失后部方位并改变房间关系。D:66、70。 |
| D16 | entry-03517 | `Feral Drem` 的野生／未开化状态变为“原生的德瑞姆”，替换为起源属性。D:72。 |
| D17 | entry-03517 | 制造异常的原因 `further disrepair and corruption` 只剩年久失修及退化，遗漏腐化因素。D:72。 |
| D18 | entry-03517 | 包覆机器的 `black growth` 变为“黑色怪物”，将增生物确定为生物个体。D:62 的 `malignant growth` 与 D:72 相互印证。 |
| D19 | entry-03517 | `judging by` 的证据—推断关系变为“正如……一样”的类比关系。D:72。 |
| D20 | entry-03517 | `tore into them` 的猛烈攻击变成已经“把他们撕成了碎片”，新增攻击结果。D:60。 |
| D21 | entry-03517 | **独立补充**：`I had planned to take a closer look` 变为“我们本来打算”，把个人意图扩展为队伍意图。D:58。 |
| D22 | entry-03522 | `tempt fate` 的冒险、拿性命碰运气变为“接受命运”，改变拒用纹身的态度。F:113。 |
| D23 | entry-03522 | 原文解释将来需要额外抵御感染，因而使用更多纹身；译文只写延误会感染，遗漏额外治疗用途这一因果环节。F:113。 |
| D24 | entry-03522 | `I should say` 后的标准比较被误接成“我应该对永恒精灵说”，新增说话对象。F:115。 |
| D25 | entry-03522 | 已经展开并经历阻碍的返程被改为“准备返回”，改变行动阶段。F:119；不把所有幸存者都判为已经抵达。 |
| D26 | entry-03522 | `move northwards around this area` 的向北绕行变为“在这个地区向北移动”，遗漏绕过区域的路线关系。F:121。 |
| D27 | entry-03522 | 复数 `gashes` 明确变为“一道”伤口，改变数量。F:125。 |
| D28 | entry-03522 | `blackened armor` 的变黑状态简化为本来“黑色”的盔甲，丢失状态变化；**不能由此确认一定经过烧灼**。F:125。 |
| D29 | entry-03522 | 待处理伤兵减少到易于应付，变成“痊愈士兵的数量……达到一定程度”，改变对象及医师抽身致谢的条件。F:131。 |
| D30 | entry-03522 | 医师 `looked behind me` 变为“看着我”，改变视线落点。F:131。 |
| D31 | entry-03522 | `fulfilling my end of the bargain` 变为“完成了我的交易”，丢失只履行己方义务的限定。F:90 的交换条件、131 的安排会面支持双方尚有不同义务。 |
| D32 | entry-03522 | `I noted` 在医师点头回应的对话中表示提出／指出，译为“意识到”后变为内心活动。F:131。 |
| D33 | entry-03522 | “甚至从来没有听说过符文的，甚至不知道……”出现悬空的“的”及重复接续，属于明确语法问题，不能仅因可猜出意思而豁免。F:127 对应冻结译文。 |
| D34 | entry-03527 | `I believe he may have been` 的推测被强化为“我极大程度上相信他还是……成员”。F:216。 |
| D35 | entry-03527 | `the day after` 变为“事后”，遗漏次日这一明确时间。F:216。 |
| D36 | entry-03527 | 惊讶于矮人出现在此地，变为惊讶于“他们这样做”，接到纳格尔人的供给行为。F:218、220。 |
| D37 | entry-03527 | 因矮人保密而难以知道其他家园，变成难以了解“矮人们的隐秘程度”，把原因误作认知对象。F:218。 |
| D38 | entry-03527 | `blasted mages` 的咒骂修饰语被解析为“法师制造的爆炸”；同时以爆炸摧毁替换住处坍塌的具体描述。F:220。宏观 Spellblaze 背景不使这处误析等价。 |
| D39 | entry-03527 | 向信使询问会被没收的物品，变为告知其没收行为，改变询问内容和信息方向。F:222；答复具体解释附魔物品。 |
| D40 | entry-03527 | 整句遗漏“官方声称平民携带此类物品太危险”，损失与信使“任何人，包括他们自己”之间的对照。F:224。 |
| D41 | entry-03527 | `a couple of halflings` 两次变为“半身人夫妇”，新增婚姻关系。同一关系重复出现只计一项。F:226。 |
| D42 | entry-03527 | 试探 `plans to deal with the Shaloren` 变为一般“有什么想法”，丢失对行动计划的询问。F:228、230。 |
| D43 | entry-03527 | “马基埃亚尔”违反本包明确适用的 `Maj'Eyal / _t / T.PN.WORLD / preferred`＝“马基·埃亚尔”。F:228、INPUT 术语子集。 |
| D44 | entry-03527 | `possibly ones that required secrecy` 的可能性限定消失，变成“计划还需要保密”的确定判断。F:232。 |
| D45 | entry-03527 | “我突然会想起”在回叙过去事件的句子中误用“会”，形成“回想起”的错字／语法问题。F:222 对应冻结译文。 |
| D46 | entry-03527 | “进城时”被限定为“今早进城”，新增未由文本确定的具体时段。F:177–183、195–209、222 只支持先后顺序，未确定上午。 |
| D47 | entry-03531 | 所见现象是灵能奴役者造成的“结果”，变为所见对象“可能是一个灵能奴役者”，混淆施术者与其制造的形象。F:289、299–301。 |
| D48 | entry-03531 | `enthralled to the slavers will` 的受控制／被奴役变为“被……意志所吸引”，改变支配关系。F:289；后文明确挣脱控制。 |
| D49 | entry-03531 | `unquestioningly` 的不加质疑地服从变为“毫无疑问地”，把服从方式换成确定性表达。F:289。 |
| D50 | entry-03531 | 两次 `thrown me` 变为“拉我／拉到这里”，改变被扔入帐篷的动作。F:282、291；两处合并。 |
| D51 | entry-03531 | 一记脚跟踢脸变为“又踢了一脚，脚踩在脸上”，增加踩踏阶段并丢失脚跟踢击。F:295。 |
| D52 | entry-03531 | `thought better of you` 的提高评价变为“更想念你”，改变人物态度。F:295；紧接“自然盟友”的解释。 |
| D53 | entry-03531 | `faceless humanoid` 的无面形象变成“面目全非的人形”，丢失无脸这一状态。F:299；此处不能据此认定为 Drem。 |
| D54 | entry-03531 | 斗篷人拜访信使变为“我……拜访过的那个人”，颠倒拜访者与受访者。F:226、301。 |
| D55 | entry-03531 | 半身人与人类站在人群中的身份回认被增写为一起“蛊惑群众”。F:303；F:266–278 将发言及煽动归于声音／被推测为发言者的人类，没有确认半身人也实施该行为。 |
| D56 | entry-03531 | `a moment` 的短暂反应变为“困惑许久”，改变时间尺度。F:305。 |
| D57 | entry-03531 | **独立补充**：落在帐篷后部 `towards the back of the tent` 被泛化为“跌入帐篷里”，遗漏落点方位。F:291。 |
| D58 | entry-03531 | **独立补充**：腹部踢击 `winding me` 的喘不过气被改为“因为这股剧痛”倒地，替换直接生理反应。F:295。 |
| D59 | entry-03532 | `Spared` 的被他人饶过只剩“死里逃生”的幸存结果，遗漏本章关键的赦免关系。F:311、314–318。并非指控“死里逃生”必然意味着自行逃走。 |

| O-ID | 状态 | 命中D-ID | 具体证据与理由 |
|---|---|---|---|
| O001 | refuted | — | `maggot/zone.lua:21–64` 将 Maggot 定义为含脊髓、房间的区域；`maggot/npcs.lua:33` 明确其神经系统。巨大生物语境成立；大写不自动要求另一个固定中文专名。 |
| O002 | confirmed | D02 | H:131，脉动被改为向外发射。 |
| O003 | mixed | — | **refuted**：独立 NETHER／VOID 属性论据不成立，`nether.lua:61、72` 使用 VOID 并称 void energy；H:143 亦为 VOID。**advisory**：邻近译名一致性和“一团”量词。不能借用同条 D01、D02。 |
| O004 | mixed | — | **advisory**：context.lua:30–31 确有“彼世”邻近译法。**refuted**：不同英文词及 existing 技能树术语不能单独证明本句机制混淆；Netherblast 反而使用 VOID。 |
| O005 | confirmed | D01、D02 | H:131，strange 遗漏，pulsing 改为发射。 |
| O006 | confirmed | D03 | W:99，正在扭动的描述被静态形状替换。 |
| O007 | confirmed | D04 | W:99，粗略成形的限定确实遗漏；不采纳“因此明确表示完全规则形状”的额外推断。 |
| O008 | confirmed | D05 | W:104，调谐关系缺失。 |
| O009 | confirmed | D05 | W:104、205 支持调谐叙述；不把它升级成额外独立数值机制。 |
| O010 | confirmed | D05 | 仅确认共鸣叙述遗漏；选择和穿戴条件仍保留。W:104。 |
| O011 | confirmed | D05 | W:208–211、RingOfTheHunter:55–64 支持选取及装备授予；本项缺陷仍只有调谐遗漏。 |
| O012 | advisory | — | W:268 的完整提示含“使用法杖掌控”，交谈能力已有操作语境支持；不是因为“愿意”在逻辑上必然等于“能够”。 |
| O013 | advisory | — | W:559、566 的拉拽及两个参数支持现有表述；“伸出触手”只是更自然。 |
| O014 | advisory | — | W:684–689 仅在玩家穿戴且为 Krog 时输出；“你感受到你的剑和克罗格的身躯共鸣”在此语境可回指自身，未证实第三者或条件误导。 |
| O015 | advisory | — | W:686–689 确实增加伤害等；“解放力量”可表达共鸣后增强。 |
| O016 | mixed | D06 | **confirmed**：不确定性、态度强度变化。**refuted**：“心理主干完全漏译”，恶心仍表达排斥。**advisory**：“上面”重复。W:800。 |
| O017 | confirmed | D06 | W:800，somehow 消失，克制的不喜欢变成强烈恶心。 |
| O018 | advisory | — | “上面”重复可改善，没有新增事实错误。W:800 对应译文。 |
| O019 | advisory | — | W:971–994 合并两个装备对象；“两件”未变为两只鞋。 |
| O020 | advisory | — | “双”更自然，但完整装备语境下“两件”仍能指两件鞋类装备，数量错误未成立。W:938、971–994。 |
| O021 | advisory | — | 两件装备的数量保留，属于量词优化。W:994。 |
| O022 | confirmed | D08 | D:58，一名队员变成整支小队。 |
| O023 | confirmed | D09 | D:62、66，眼前一台机器被写成复数。 |
| O024 | confirmed | D10 | D:64，胎儿阶段泛化成生命体。 |
| O025 | confirmed | D08 | D:58，人数及容纳方式改变。 |
| O026 | confirmed | D11 | D:66，只明确附着，未说明咬一口。 |
| O027 | confirmed | D13 | D:68，“还有感染者”扩大为所有其他人。 |
| O028 | confirmed | D09 | D:62、66，机器单复数证据明确。 |
| O029 | confirmed | D10 | D:64、72，胎儿阶段参与起源推断。 |
| O030 | confirmed | D18 | D:72，黑色增生物被确定为怪物。 |
| O031 | confirmed | D08 | D:58、70，容纳单人的培育管语境不支持小队行走。 |
| O032 | confirmed | D12 | D:66，flesh 不等同于只描述肌肉。 |
| O033 | confirmed | D07 | D:56，语序混杂且浓度限定未清楚表达。 |
| O034 | confirmed | D13 | D:68，感染范围扩大。 |
| O035 | confirmed | D15 | D:70，房间后部关系丢失；依据是实际译文“那些……房间”，而非单独把“里面”视为另一个房间。 |
| O036 | confirmed | D14 | D:68，个人态度扩大为队伍共同态度。 |
| O037 | confirmed | D15 | D:66、70，已经封闭的同一房间内继续向后探索。 |
| O038 | confirmed | D07 | D:56，受限制的是能量浓度，不是能量在埃亚尔的一切存在。 |
| O039 | confirmed | D16 | D:72，feral 描述生活状态，不表示原生起源。 |
| O040 | confirmed | D08 | D:58，one of our party 不是一个小队。 |
| O041 | confirmed | D17、D18 | D:62、72，腐化原因遗漏，增生物变成怪物；两种信息分列。 |
| O042 | advisory | — | D:60 的否定式强调可自然表达为“不自然”；“显得”仍保留观察判断，不足以认定推测变成客观断言。 |
| O043 | refuted | — | D:62 此时仍在巨蛋中探索，“这里”可以回指巨蛋；译文随后才定位中心房间及机器，未必提前宣布找到具体机器。 |
| O044 | confirmed | D09 | D:62、72 的同一机器两次复数化合并计一项。 |
| O045 | confirmed | D13 | D:68，not the only one 不支持其余全部感染。 |
| O046 | confirmed | D14 | D:68，确认主语扩大；“充实”不另拆一个同源情绪缺陷。 |
| O047 | confirmed | D15 | D:70，后部空间关系未保留。 |
| O048 | confirmed | D16 | D:72，仅按普通语义判定，不强加术语策略。 |
| O049 | confirmed | D18、D19 | D:72，既改变对象性质，也改变证据关系，分别计项。 |
| O050 | mixed | D20 | **confirmed**：猛攻变成撕碎的完成结果。**advisory**：“考虑到防御力”及“本能地”有邻句推理语境。D:52、60；“不矛盾”不能豁免前一结果增译。 |
| O051 | confirmed | D23 | F:113，额外抵御感染这一治疗用途遗漏。 |
| O052 | confirmed | D29 | F:131，their numbers 回指伤兵。 |
| O053 | confirmed | D30 | F:131，behind me 不是看着我。 |
| O054 | confirmed | D22 | F:113，tempt fate 表示冒险，不是接受命运；不沿用报告的夸张严重度。 |
| O055 | confirmed | D24 | F:115，to the shalore 属于生活标准比较。 |
| O056 | confirmed | D29 | F:131，待治疗人数减少，不是痊愈人数达到某值。 |
| O057 | confirmed | D22 | F:113，拒绝治疗的态度变化成立。 |
| O058 | confirmed | D24 | F:115，原文是叙述者补充说明，没有向永恒精灵说话。 |
| O059 | confirmed | D26 | F:119–121，返程阻碍解释依赖绕行。 |
| O060 | confirmed | D27 | F:125，复数 gashes 被限定为一道。 |
| O061 | confirmed | D29 | F:131，医师能够抽身的条件改变。 |
| O062 | confirmed | D30 | F:131，视线落在叙述者身后。 |
| O063 | confirmed | D31 | F:90、131，己方义务和整个交易不能等同。 |
| O064 | confirmed | D22 | F:113，同一习语误译。 |
| O065 | confirmed | D24 | F:115，同一句法挂接错误。 |
| O066 | mixed | D25 | **confirmed**：“准备返回”错误降低行动阶段。**refuted**：不能将原句概括为所有幸存者均已抵达；同段明确仅几百人成功返回。F:119。 |
| O067 | confirmed | D26 | F:121，绕过区域变为区域内移动。 |
| O068 | mixed | D27、D28 | **confirmed**：复数变单数、变黑状态丢失。**refuted**：blackened 本身不能证明一定烧焦或熏黑。F:125。 |
| O069 | confirmed | D29 | F:131，伤兵变为痊愈士兵；译文没有保留可应付的处理量。 |
| O070 | confirmed | D30、D32 | F:131，对外提出变为内心意识；看向身后变为看本人。 |
| O071 | confirmed | D33 | 冻结译文明显出现悬空“的”及重复接续；可理解不等于仅建议。F:127。 |
| O072 | confirmed | D36 | F:218，惊讶对象为矮人在此地出现。 |
| O073 | confirmed | D38 | F:220，原句为法师造成坍塌；爆炸来自对 blasted 的误析。 |
| O074 | confirmed | D39 | F:222，对物品的询问变成对没收行为的告知。 |
| O075 | confirmed | D39 | F:222，委婉询问句的信息方向被改变。 |
| O076 | confirmed | D40 | F:224，官方理由整句遗漏。 |
| O077 | confirmed | D40 | F:224，官方与个人意见的对照缺一半。 |
| O078 | confirmed | D41 | F:226，人数描述不提供婚姻关系。 |
| O079 | confirmed | D38 | F:220，blasted 修饰 mages，是贬斥用语。 |
| O080 | confirmed | D42 | F:228、230，探查行动计划被泛化为询问看法。 |
| O081 | confirmed | D43 | F:228；本包 preferred 地名条目明确适用。 |
| O082 | confirmed | D43 | `_t`、地名语境和术语规定吻合。 |
| O083 | confirmed | D35 | F:216，次日信息被泛化。 |
| O084 | confirmed | D36 | F:218–220，紧接矮人其他家园的话题。 |
| O085 | confirmed | D37 | F:218，保密是难以获知的原因。 |
| O086 | confirmed | D39 | F:222，答复具体物品，证明原问不是告知没收行为。 |
| O087 | confirmed | D40 | F:224，平民携带危险的说辞完全缺失。 |
| O088 | confirmed | D41 | F:226，两次夫妇称呼是同一关系增译。 |
| O089 | confirmed | D42 | F:228，对付永恒精灵的计划不等于一般态度。 |
| O090 | confirmed | D43 | INPUT 的 `_t` 地名规范适用，不涉及新增命名政策。 |
| O091 | confirmed | D34 | F:216，may 的保留态度被明显强化；不将“相信”解作绝对事实。 |
| O092 | confirmed | D36 | F:218，“出现在这里”变为“这样做”。 |
| O093 | confirmed | D37 | F:218，因果状语误作宾语内容。 |
| O094 | confirmed | D39 | F:222，打听消息变为告诉对方。 |
| O095 | confirmed | D40 | F:224，anyone 与 civilians 的对照被破坏。 |
| O096 | mixed | D41 | **confirmed**：夫妇关系无依据。**advisory**：不采纳报告把 couple 固定解释为“两三个”；本项无需裁定精确人数即可确认关系增译。F:226。 |
| O097 | confirmed | D42 | F:228–230，试探与后续邀请均围绕行动计划。 |
| O098 | confirmed | D43 | INPUT 明确旧拼写已被首选拼写替代。 |
| O099 | advisory | — | F:230 的 they 可泛指采用该称呼的人，“你们”也可泛指对方所属群体；回答“别人告诉我的”并不逻辑冲突。可更精确，但未证实实质指代错误。 |
| O100 | confirmed | D44 | F:232，保密计划的可能性限定遗漏。 |
| O101 | confirmed | D38 | F:220，确认修饰语误析及描述变化；Spellblaze 背景不能使其降为纯语气建议。 |
| O102 | confirmed | D45、D46 | F:222 的错字和新增“今早”分别成立；F:177–183、195–209 未提供上午时段。 |
| O103 | confirmed | D52 | F:295，评价更高不是想念；只采语义错误，不采“灾难级”等未经证明的严重度判断。 |
| O104 | confirmed | D47 | F:289，result of 与施术者本人不同。 |
| O105 | confirmed | D48、D49 | F:289，支配关系及服从方式各有独立偏差；不依靠不匹配的术语标签确认。 |
| O106 | confirmed | D48 | F:289，被支配变成被吸引。 |
| O107 | mixed | D53 | **confirmed**：无脸变成面目全非。**refuted**：本段是心理幻象消退，不足以认定 Drem 种族；所引另一族群特征不能覆盖 F:289、299–301。 |
| O108 | confirmed | D50 | F:291，扔入改成拉入。 |
| O109 | confirmed | D50 | F:291 两处属于同一动作误译。 |
| O110 | confirmed | D52 | F:295，后文盟友判断支持评价含义。 |
| O111 | confirmed | D53 | F:299，无面状态不等于面容变得难以辨认。 |
| O112 | confirmed | D54 | F:301，拜访者应为斗篷人。 |
| O113 | confirmed | D48 | F:289，后续服从命令不能补回被精神控制的关系；鲜血之环术语不适用。 |
| O114 | confirmed | D50 | F:282、291，前章动作与本章回指均为扔入。 |
| O115 | confirmed | D51 | F:295，一记脚跟踢击不是踢后踩脸。 |
| O116 | confirmed | D52 | F:295，同一评价习语误译。 |
| O117 | confirmed | D53 | F:299，幻象先失去面部形态，再消失。 |
| O118 | confirmed | D54 | F:226、301，两段一致显示斗篷人拜访信使。 |
| O119 | confirmed | D56 | F:305，片刻变成许久。 |
| O120 | confirmed | D48、D49 | F:289，enthralled 与 unquestioningly 分别误译；不套用鲜血之环 slaver 术语。 |
| O121 | confirmed | D50 | F:282、291，原动作有直接互证。 |
| O122 | confirmed | D52 | F:295，thought better of 表示评价较高。 |
| O123 | confirmed | D53 | F:299，无脸这一形态特征遗漏。 |
| O124 | confirmed | D54 | F:301，关系从斗篷人→信使变为叙述者→斗篷人。 |
| O125 | confirmed | D55 | F:303 只回认共同站立；F:266–278 未确认半身人也在煽动。其后来救人本身不是判错依据。 |
| O126 | confirmed | D56 | F:305，短暂反应与困惑许久不同。 |
| O127 | advisory | — | F:297，译文紧接“头突然被……砸在地上”，中断行为仍在；标点改变未独立造成可证的情节损失。“他们”有语境支持。 |
| O128 | confirmed | D59 | F:311、314–318，标题聚焦半身人选择饶过她；仅表达幸存遗漏该关系。 |
| O129 | confirmed | D59 | 不认定“死里逃生”必然是自行逃跑，但原有他人饶命的信息确实未表达，按 INPUT 不因轻微降为建议。 |

**P01：DLC 目标版本适用性未确认。** 已核验的是清单指定的快照内容，尚缺 DLC 源码仓库、commit 及其与目标发行版本的对应证明。这是共同的来源适用性缺口，不等于每条译文都有未决缺陷，因此没有机械地把所有 OK 改为 PENDING。上述文本可直接证明的 D 不依赖其他发行版本的机制推测；对装备及技能行为的陈述均限定为快照内事实。

主要分歧按完整语境裁决：没有把 `nether` 强制当成不同伤害属性，也没有把装备日志中省略显然可见的穿戴动作、鞋类装备的“两件”等直接计为缺陷；反之，原文明确给出的数量、关系、时段、动作和因果信息，即使影响较轻或玩家可以猜回，也保留为缺陷。独立补充项为 D21、D57、D58。

实际读取范围如下。设：

- `B`＝[本次冻结包目录](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g09-20260923)
- `R`＝`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults`

读取了 `B/ADJUDICATION-INPUT.md`、`B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。40 条原译文均与 INPUT 对应；context.lua 仅作为获准邻近语境使用。

读取并核验了以下六份本组源码，SHA-256 全部与清单相符：

- `B/sources/dlc/cults/tome-cults/data/general/npcs/corrupted_blobs.lua`
- `B/sources/dlc/cults/tome-cults/data/general/npcs/horror.lua`
- `B/sources/dlc/cults/tome-cults/data/general/objects/world-artifacts.lua`
- `B/sources/dlc/cults/tome-cults/data/glyph_sequences/cults.lua`
- `B/sources/dlc/cults/tome-cults/data/lore/dremwarves.lua`
- `B/sources/dlc/cults/tome-cults/data/lore/fay-willows.lua`

额外单文件均在授权清单中，读取前核验哈希相符：

- `R/tome-cults/data/zones/maggot/zone.lua`：由 `corrupted_blobs.lua:58` 的 Maggot 指称引入。
- `R/tome-cults/data/zones/maggot/npcs.lua`：追查区域的 `SPINAL_CORD` 实体。
- `R/tome-cults/data/zones/maggot/objects.lua`：追查区域 `post_process` 中的 NOTE1–NOTE3；后续拟查的 `data/lore/maggot.lua` 不在清单，未读取。
- `R/tome-cults/data/talents/demented/nether.lua`：由 H:164 的 `T_NETHERBLAST` 引入。
- `R/tome-cults/data/damage_types.lua`：由 H:143 及 Netherblast 的 `DamageType.VOID` 引入。
- `R/tome-cults/overload/mod/dialogs/RingOfTheHunter.lua`：由 W:210 的明确 `require` 引入。

本体仅用 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取：

- `game/modules/tome/class/Actor.lua`：追查装备属性及 Actor 继承。
- `game/engines/default/engine/Actor.lua`：追查 W:1029 的 `who:his_her()`。
- `game/engines/default/engine/utils.lua`：追查 `string.his_her()` 的所属代词返回逻辑。

未将本体 commit 套用于 DLC，未读取其他语言答案或运行实际游戏界面。未查找模型身份、来源映射、其他报告或 STATE；未修改仓库、未创建临时文件、未创建子 agent。本交付仅为独立复核与归并裁决。
