# 归并问题清单（暂定源码裁决）

来源为三位参赛reviewer的75项观察及独立盲审的26项观察。重复观察按canonical D合并；原始状态和模型归属保留。确认是模型依据本组获准源码与语境的暂定核验结果，非人工金标准。译文尚未修改。

每个D的完整证据见[裁决原文](reports/adjudication-01.md)与[机器参考集](REFERENCE.json)。

| 缺陷 | 条目 | Opus | Sol | Gemini | 内容、归因及源码证据 |
|---|---|---|---|---|---|
| D01 | entry-03454 | C01（原建议） | C01（原问题） | C02（原建议） | **翻译新增，身体部位改变。** `3 arms` →“三只手”，明确计数对象由手臂变成手。实体描述见 `A/data/zones/searing-halls/npcs.lua:73`；不以“扒手”联想作为缺陷依据。 |
| D02 | entry-03454 | 未提出此缺陷 | C02（原问题） | 未提出此缺陷 | **翻译新增，行为结果遗漏。** `mutilate you` →“切割你”，只保留切割动作，未保留使身体残缺、严重损毁的结果。`A/data/zones/searing-halls/npcs.lua:72–73` 的实体名称及实验性伤害语境支持此区别。 |
| D03 | entry-03455 | C02（原问题） | 未提出此缺陷 | C03（原问题） | **翻译新增，明确术语要求未落实。** Maj’Eyal 使用已被取代的“马基埃亚尔”。`INPUT.md` 的 preferred 世界专名记录明确规定“马基·埃亚尔”；`A/init.lua:28` 所指正是该世界。 |
| D04 | entry-03455 | C03（原问题） | C03（原问题） | C05（原问题） | **翻译新增，同一专名内部不一致。** 同一 Fearscape 分别成为“恐惧空间”和“恶魔空间”。`A/init.lua:28、33` 明确指同一地点；本项不裁定应全局采用哪一译名。 |
| D05 | entry-03455 | C04（原问题） | C04（原问题） | C06（原问题） | **翻译新增，行动性质改变。** `under their scrutiny` →“在他们的破坏下”，审视、探查被改写为明确破坏。`A/init.lua:28`；不进一步推断原文未说的具体窥视法术。 |
| D06 | entry-03455 | 未提出此缺陷 | C06（原问题） | 未提出此缺陷 | **翻译新增，战斗关系偏移。** `against overwhelming odds` →“与势不可挡的敌人战斗”，己方处于悬殊劣势的局面变成敌人本身不可阻挡。`A/init.lua:31`。 |
| D07 | entry-03455 | C05（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，生存目的遗漏。** 吸收火焰、痛苦 `to stay alive` 的目的未译。`A/init.lua:31`；快照 `A/data/timed_effects.lua:179–181` 的治疗、恢复活力仅为补充佐证。 |
| D08 | entry-03455 | 未提出此缺陷 | C07（原问题） | 未提出此缺陷 | **翻译新增，诅咒关系遗漏。** `demon-cursed minotaur` →“恶魔牛头人”，未表达牛头人受到恶魔诅咒。`A/init.lua:32`。 |
| D09 | entry-03455 | C10（原建议） | C08（原问题） | C04（原问题） | **翻译新增，召唤对象泛化。** `Fire Imps` →“火焰恶魔”，特定 imp 类别丢失。`A/init.lua:32`；`A+/data/talents/corruptions/demonic-pact.lua:27、314` 另列具体 `fire imp` 类型；不依赖强制“小鬼”术语。 |
| D10 | entry-03455 | C10（原建议） | C08（原问题） | 未提出此缺陷 | **翻译新增，数量组织信息遗漏。** `a squad` 未体现成队召唤，只剩“召唤火焰恶魔”。`A/init.lua:32`。与 D09 分开记录。 |
| D11 | entry-03455 | 未提出此缺陷 | C09（原问题） | C04（原问题） | **翻译新增，攻击方式遗漏。** `pelt … to death` →“烧成灰烬”，连续投射攻击被燃尽结果替代。`A/init.lua:32`；不据此断言原攻击不是火焰伤害。 |
| D12 | entry-03455 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，敌人消耗结果遗漏；独立补充。** `exhaust themselves on your … defenses` →“在……防御面前无可奈何”，受阻保留，但敌人持续攻击并耗尽自身的结果未保留。`A/init.lua:32`。 |
| D13 | entry-03455 | C06（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，比较依据改变。** `disposable … skeletons` →“易碎的骷髅”，可消耗、用后替换变成承伤脆弱。`A/init.lua:32` 的召唤物珍贵程度比较；不依赖 P01 的机制裁决。 |
| D14 | entry-03455 | C07（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，人群限定遗漏。** `taken to … alterations especially well` →“被恶魔的力量所改变”，特别适应改造的一部分精灵变成一般被改造者。`A/init.lua:35`。 |
| D15 | entry-03455 | C09（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，敌我所属关系改变。** `the worst Urh’Rok’s forces can throw at you` →“乌鲁洛克最强大的敌人”，乌鲁洛克派来对付玩家的力量变成乌鲁洛克的敌人。`A/init.lua:40`。 |
| D16 | entry-03455 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，结果描写遗漏；独立补充。** `a pile of ash and gore` 只剩“灰烬”，血肉残骸这一并列结果消失。`A/init.lua:31`。不把“任何敌群”另外计入此项。 |
| D17 | entry-03456 | C12（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，空间关系遗漏。** `void between worlds` 只译“虚空”，世界之间的方位关系未保留。`A/overload/data/texts/intro-ashes-urhrok.lua:23`。 |
| D18 | entry-03456 | C13（原建议） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，程度目标改变。** `cause the most pain` →“造成更大的痛苦”，研究最大痛苦的目标降为一般增加痛苦。`A/overload/data/texts/intro-ashes-urhrok.lua:25`。 |
| D19 | entry-03456 | 未提出此缺陷 | C13（原问题） | 未提出此缺陷 | **翻译新增，致死方式被具体化。** 陨石附近落地并使看管者当场死亡，译为“砸死”，增添直接撞击致死的限定。`A/overload/data/texts/intro-ashes-urhrok.lua:25` 未给出该限定。 |
| D20 | entry-03456 | C11（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，意识状态被具体化。** `As you recover` →“当你醒来后”，加入此前失去意识的状态。`A/overload/data/texts/intro-ashes-urhrok.lua:25、27` 只明确倒地及恢复。 |
| D21 | entry-03456 | C11（原问题） | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，事件时序改变。** 恢复时地块正在分裂，变成醒来后发现自己身处已分离的焦土。`A/overload/data/texts/intro-ashes-urhrok.lua:27`；这是叙述时序判断，不推断地图生成时序。 |
| D22 | entry-03456 | 未提出此缺陷 | 未提出此缺陷 | 未提出此缺陷 | **翻译新增，记忆恢复速度改变。** `memories flood your mind` →“记忆渐渐涌来”，集中涌回改为逐渐恢复。`A/overload/data/texts/intro-ashes-urhrok.lua:27`。 |
| D23 | entry-03458 | C15（原问题） | C14（原问题） | C07（原问题） | **翻译新增，对象与行为改变。** `created many dark cults` →“通过黑暗仪式”，建立多个组织变成采用一种仪式手段。`A/overload/data/texts/unlock-corrupter_demonologist.lua:22`。 |
| D24 | entry-03460 | C20（原问题） | 未提出此缺陷 | C10（原问题） | **翻译新增，施放时序信息遗漏。** `Instant cast` 说明施放本身瞬发；“瞬间穿梭空间”只说明位移过程。`A/overload/data/texts/unlock-race_doomelf.lua:27`；`A+/data/talents/misc/races.lua:43、68、79–86` 支持区分施放与位移。目标版本有无速度增益另列 P06。 |
| D25 | entry-03460 | C19（原问题） | C18（原问题） | C11（原问题） | **翻译新增，玩家解锁结果改变。** 获得创建该种族角色的资格变成“魔化精灵应运而生”。`A/overload/data/texts/unlock-race_doomelf.lua:20、24` 的标题与正文构成解锁通知，正文却改成种族产生的叙述。 |
| D26 | entry-03460 | C21（原问题） | C17（原问题） | 未提出此缺陷 | **翻译新增，磨砺原因增加。** 严格训练之外增加“烈火”作为能力受磨砺的原因。`A/overload/data/texts/unlock-race_doomelf.lua:22`；地点具有火焰背景不能直接证明这一具体因果。 |
| D27 | entry-03475 | C27（原建议） | 未提出此缺陷 | C15（原问题） | **翻译新增，突发感受遗漏。** `suddenly feel` 的突然感未保留；“哦”仅表示反应，不能明确承担突然发生的意义。`C/data/chats/godfeaster-malyu-escaped.lua:53、72–73`。不据此宣称存在属性即时结算机制错误。 |
| D28 | entry-03478 | 未提出此缺陷 | C20（原问题） | 未提出此缺陷 | **翻译新增，动作方式改变。** 物品 `rolls` 出来变成“掉了出来”。`C/data/general/events/digestive-sack.lua:107–108`；放置物品代码没有提供纠正原叙述的依据。 |
| D29 | entry-03479 | C30（原问题） | C21（原问题） | C16（原建议） | **翻译新增，动作方式改变。** 敌人 `burst out` 的突然冲出变成“掉了出来”。`C/data/general/events/digestive-sack.lua:109–117`。不额外认定中文必然把活敌译成尸体。 |
| D30 | entry-03481 | 未提出此缺陷 | C22（原问题） | C17（原建议） | **翻译新增，搜取完成结果遗漏。** `already scavenged` →“已经找遍”，搜索完成没有表达已搜取得到物品。`C/data/general/events/space-dwarf-ship.lua:62–71`：先前交互加入背包，随后显示该提示。 |
| D31 | entry-03491 | 未提出此缺陷 | 未提出此缺陷 | C18（原问题） | **翻译新增，外观状态遗漏。** `oozing` 的渗出黏液状态未保留；“绿泥”只表达颜色与黏团形态。`C/data/general/npcs/blobs.lua:51–54`。句式改成判断句及使用黏团描写本身不构成错误。 |

以下保留未决、建议与被否决部分；mixed可能同时命中上表D，不能整项丢弃。

| 匿名观察 | 来源与原状态 | 条目 | 裁决状态 | 理由 |
|---|---|---|---|---|
| O001 | Opus C01（原建议） | entry-03454 | mixed | 手臂计数已改变，不能认定事实全部保留；“扒手”联想及 Nope 的语气处理仅 advisory。见 `A/.../searing-halls/npcs.lua:73`。 |
| O004 | Gemini C01（原问题） | entry-03454 | advisory | Nope 重复否定并制造语气；“不是娱乐，而是实验”保留命题，未发现独立事实遗漏。不能将 Nope 固定解释为“才怪”。 |
| O005 | Gemini C02（原建议） | entry-03454 | mixed | 部位区别 confirmed；“扒手”联想 advisory。“只属偏好”的总判断不成立。 |
| O015 | Gemini C04（原问题） | entry-03455 | mixed | 类别泛化、投射方式遗漏 confirmed；“Imp 恒为小鬼”的强制术语说法无依据；“风筝”无证；防御配合并未全部丢失。 |
| O017 | Sol C05（原问题） | entry-03455 | advisory | `A/init.lua:28` 的奴隶、玩物、受折磨语境允许以“拷问”表现虐待；不能必然解释为新增审讯取供机制。更宽泛措辞可作建议。 |
| O019 | Gemini C05（原问题） | entry-03455 | mixed | 内部两译 confirmed；existing 的 fearscape 记录并非强制统一“恶魔空间”的依据。 |
| O020 | Opus C05（原问题） | entry-03455 | mixed | 生存目的遗漏 confirmed；敌群信息已在该段“削弱敌群”中出现，未另确认整体群体定位遗漏。 |
| O022 | Gemini C06（原问题） | entry-03455 | mixed | scrutiny 被改为破坏 confirmed；“仅凭窥视与法术试探”“尚未全面突破”的额外细节并非该句全部明示，不采信。 |
| O023 | Opus C06（原问题） | entry-03455 | mixed | disposable → 易碎 confirmed；persistent health 的具体机制解释 pending，见 P01。 |
| O024 | 独立盲审 C06（原待确认） | entry-03455 | pending | P01。已核实复用恶魔对象、保留生命值的快照调用链；缺目标版本绑定。 |
| O030 | Opus C08（原问题） | entry-03455 | advisory | unsteady in combat 不必指物理站立失衡；`A+/.../races.lua:183–206` 的效果、冷却干扰也不支持必然“站不稳”。现译较泛，但不能据此认定平衡机制误译。 |
| O031 | 独立盲审 C09（原问题） | entry-03455 | advisory | `A/init.lua:40` 同句明确是成就、个人页面，中文仍处于虚拟战绩展示语境；未确认变成实体头骨机制。明示比喻仅建议。 |
| O033 | Opus C09（原问题） | entry-03455 | mixed | 乌鲁洛克势力与其敌人的所属关系 confirmed；metaphorical 的明确化仅 advisory，理由同 O031。 |
| O034 | 独立盲审 C10（原建议） | entry-03455 | advisory | 新地区“全新的艺术”具有直译感，但仍能指美术内容，未证功能或事实变化。 |
| O035 | Opus C10（原建议） | entry-03455 | mixed | 类别、队伍信息遗漏 confirmed，不需要强制术语；宣传语“会想要”及它／他属于 advisory。 |
| O036 | Sol C10（原待确认） | entry-03455 | pending | P01。此次已补足对象选取和再召唤链；剩余缺口为 DLC 目标版本适用性。 |
| O037 | Sol C11（原问题） | entry-03455 | advisory | 同 O031；完整成就界面语境仍保留比喻性展示。 |
| O040 | Sol C12（原问题） | entry-03456 | refuted | “主人”带引号；`A/init.lua:28` 已明确奴隶、玩物关系，开场又是受控制参与实验。不能脱离语境认定凭空新增所有权关系。 |
| O042 | Opus C13（原建议） | entry-03456 | mixed | 最高程度变比较程度 confirmed；带引号“主人”属于语境允许的表达，不构成另一缺陷。 |
| O044 | Opus C14（原待确认） | entry-03457 | pending | P02。existing Corruptor 不能强制改名；固定本体及 DLC 快照还显示 Defiler 大类与 Corruptor 子职业的区别，不能只核一个中文名称。 |
| O046 | Gemini C08（原问题） | entry-03458 | refuted | “召唤并控制”已表达役使关系；`A+/.../corruptions.lua:22` 的 “do your bidding” 支持该语境。不能把 binding 固定解释成另一项契约操作。 |
| O047 | Gemini C09（原问题） | entry-03458 | pending | P04。远程词确实未译，但 `A+/data/birth/corrupted.lua:118` 明示恶魔使者为近战者；不能绕过上游职业指代问题直接确认修复方向。 |
| O049 | 独立盲审 C13（原待确认） | entry-03458 | pending | P05。默认活力恢复为零与永不恢复不同；已查恢复消费者及种子例外，缺 DLC 目标版本绑定。 |
| O051 | Sol C15（原问题） | entry-03458 | refuted | 本段已将对象界定为施法职业；`A+/.../corruptions.lua:21–36` 的相关能力类别也标记 is_spell。未证“法术”在此排除了某项应包含的活力能力。 |
| O053 | Sol C16（原问题） | entry-03458 | refuted | 连续战斗语境中的“你的目标”可指被攻击敌人，并未宣称所有非敌对对象均可供抽取；不能仅凭一个名词判定机制范围扩大。绝对资源说明另见 P05。 |
| O054 | Opus C16（原问题） | entry-03458 | pending | 与 O047 同一 P04；源文远程定位与职业语境存在冲突。 |
| O055 | Opus C17（原待确认） | entry-03458 | pending | P03。需核对实际大类／子职业指代和显示映射；不是 existing 术语违例。 |
| O056 | Opus C18（原建议） | entry-03458 | advisory | 系／者、种子两称及“注射”可改善一致性；役使已由“控制”表达，分段保留信息结构。 |
| O057 | Gemini C10（原问题） | entry-03460 | mixed | 瞬发施放信息遗漏 confirmed；目标版本无加速增益的判断 pending（P06）；强制使用核心技能名“相位之门” refuted，快照对应技能为 Haste of the Doomed。 |
| O060 | 独立盲审 C15（原待确认） | entry-03460 | pending | P06。快照是瞬发位移及防御抗性效果，并有第二次施放耗能分支；目标版本绑定仍缺失。 |
| O064 | Opus C20（原问题） | entry-03460 | mixed | 施放瞬发与位移瞬间的区别 confirmed；必须出现核心技能专名的主张 refuted；“加速”是否误导实际技能机制 pending（P06）。 |
| O066 | Opus C22（原待确认） | entry-03460 | refuted | 此次获准读取的 `A+/data/lore/demon.lua:448、450、458` 说明三位探险者调查埃亚尔与灾变、恶魔对埃亚尔的归因失实。“有关埃亚尔大陆”有背景支持。 |
| O067 | Opus C23（原待确认） | entry-03460 | pending | P07。`A+/.../races.lua:183–195` 实际改动 `p.dur`，快照支持“延长／缩短”；目标 DLC 版本适用性仍待确认。 |
| O068 | Gemini C12（原问题） | entry-03464 | advisory | 六属性语境和 `mag=3` 对应明确；Magic 记录为 existing，不能认定强制“魔力”规范违例。 |
| O069 | 独立盲审 C16（原建议） | entry-03464 | advisory | 同意仅作命名一致性意见；`C/data/birth/demented.lua:81–87` 支持属性身份。 |
| O070 | Opus C24（原建议） | entry-03464 | advisory | `context.lua:404、407、412、414` 同组使用“魔法”；不扩大为全库术语策略。 |
| O071 | 独立盲审 C17（原待确认） | entry-03465 | pending | P08。`life_rating=3` 经过固定本体等级、阶级调整；属上游标签疑点，缺 DLC 目标版本绑定。 |
| O072 | 独立盲审 C18（原待确认） | entry-03466 | pending | P09。`life_rating=-4` 是成长系数修正，并非所有等级固定少四点生命。 |
| O073 | Gemini C13（原问题） | entry-03468 | advisory | 与 O068 同理；`C/data/birth/drem.lua:31–37` 的属性身份、数值未变。 |
| O074 | 独立盲审 C19（原建议） | entry-03468 | advisory | 同意仅一致性建议。 |
| O075 | Opus C25（原建议） | entry-03468 | advisory | 与 O070 同类意见，独立覆盖该条。 |
| O076 | 独立盲审 C20（原待确认） | entry-03469 | pending | P10。`life_rating=12` 仍进入等级、阶级调整，目标版本绑定不足。 |
| O077 | Gemini C14（原问题） | entry-03472 | advisory | 与 O068 同理；`C/data/birth/krog.lua:31–38` 中负号、属性对象正确。 |
| O078 | 独立盲审 C21（原建议） | entry-03472 | advisory | 同意仅一致性建议。 |
| O079 | Opus C26（原建议） | entry-03472 | advisory | 与 O070 同类意见，独立覆盖该条。 |
| O080 | 独立盲审 C22（原待确认） | entry-03473 | pending | P11。`life_rating=13` 与实际升级增量有区别；结论来自消费者，不仅凭注释。 |
| O081 | Gemini C15（原问题） | entry-03475 | mixed | suddenly 的突发感遗漏 confirmed；“成长潜力／潜能增长”在赠予属性的回应中仅 advisory。不能由该聊天节点证明属性已即时结算。 |
| O082 | Sol C19（原建议） | entry-03475 | advisory | 该观察针对潜力重心：上下文为提供属性增益，未出现具体成长机制承诺。未借用它没有指出的 D27。 |
| O083 | 独立盲审 C23（原建议） | entry-03475 | advisory | 同 O082，表达重心可改善，不计玩法机制错误。 |
| O084 | Opus C27（原建议） | entry-03475 | mixed | 突然感的遗漏 confirmed；潜力措辞 advisory。“语境基本一致”不足以消除明示突发感的损失。 |
| O085 | Opus C28（原建议） | entry-03476 | advisory | `C/.../godfeaster-malyu-escaped.lua:79–82` 的拒绝、祝愿均保留，主要是语气差别。 |
| O086 | Opus C29（原建议） | entry-03477 | advisory | `C/.../godfeaster-malyu.lua:29–33` 问是否有人，增补只是明确 YES 的指代；可直接视为无问题。 |
| O092 | Opus C30（原问题） | entry-03479 | mixed | 冲出→掉落 confirmed；“中文会读成残骸、丢失活敌提示”的推断 refuted，“敌人”并未被译成尸体。 |
| O096 | Opus C32（原建议） | entry-03488 | advisory | `C/.../godfeaster.lua:135` 完整对应；“你觉得”是自然等价表达，可直接视为无问题。 |
| O097 | Opus C33（原建议） | entry-03489 | advisory | 独立核对 `C/.../maggot.lua:136`，同 O096。 |
| O098 | Opus C34（原建议） | entry-03490 | advisory | 独立核对 `C/.../slimy_godfeaster.lua:135`，同 O096。 |
| O099 | Gemini C18（原问题） | entry-03491 | mixed | 渗液状态遗漏 confirmed；“绿泥”为凭空实体称谓的断言 refuted，`BASE_NPC_BLOB`、绿色和黏团语境支持这种形态描写；判断句改写合法。 |
| O100 | Gemini C19（原建议） | entry-03491 | advisory | maggot 记录是 existing 实体子类型，不是强制专名；“巨大”未证明改变所指。仅可提一致性建议。 |
| O101 | Opus C31（原待确认） | entry-03491 | refuted | 大写本身不能建立必须逐字采用某个中文正式名的要求；已读蛆虫内部地图与细胞描述支持该所指，不保留仅因缺正式译名而产生的疑点。 |

原报告与归并映射均保留；仅建议不进入确认缺陷，原待确认／建议即使后来确认也不追算明确检出。计分见[RESULT.md](RESULT.md)。
