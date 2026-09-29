# 宿主逐项裁决记录

这是本轮研究参考集，不是人工金标准或生产验收。H 编号源于报告揭示前的独立初审，N 编号为揭示候选后补充。原始意见、初判与修订均另行保留；候选低影响并不自动撤销，合理等价读法也不自动确认为错译。

所有文本判断以冻结 entries.json 的完整原译为依据。Orcs 源码仅固定文件哈希，目标发布版本未固定；Possessors 源码不可用。表内 section 是冻结快照路径，不能称为固定 DLC commit。

| 编号 | entry-ID | 最终状态 | 影响 | 原译锚点与结论 | 最强反证／处理 | 证据 |
|---|---|---|---|---|---|---|
| H01 | entry-03740 | confirmed | 叙事事实 | binding John to it forever → 将约翰绑定到戒指上；永久绑定的时间限定遗漏。 | 绑定可以暗示持续，但未明确永久；后句只涉及召唤。 | sources/dlc/orcs/tome-orcs/data/chats/john-surrender.lua:116 |
| H02 | entry-03740 | confirmed | 机制/操作 | summon him for a few turns at will → 戒指现在具有召唤他的能力；召唤仅持续数回合的限制遗漏。 | 仍有召唤能力不等于保留持续时限；不另外指控无限次或随意使用。 | sources/dlc/orcs/tome-orcs/data/chats/john-surrender.lua:116 |
| H03 | entry-03744 | advisory | 表达建议 | consider you a customer for now → 将你视为顾客；暂时视为顾客的限定未直接保留。 | 后句违法即受攻击表达条件性接待；宜澄清，不必确认永久接待误述。 | sources/dlc/orcs/tome-orcs/data/chats/kaltor-entry.lua:21 |
| H04 | entry-03858 | confirmed | 叙事事实 | had already caught fire → 突然着火了；被拉入之前已着火，改成拉入时突然着火。 | 读不完标题的结果保留，不消除火起时序变化。 | sources/dlc/orcs/tome-orcs/data/lore/misc.lua:154 |
| H05 | entry-03862 | advisory | 叙事事实 | a pitiful, fallen reminder → 也没有留下一个可悲的警示；整段仍在否定祖先明确告诫兽人的危险；原判把否定作用域中的比喻当独立肯定事实。该转述可保留未作警示的意思，不确认主体反转。 | 段落仍说未直接劝告，但没有保留对兽人这一对象的评价。 | sources/dlc/orcs/tome-orcs/data/lore/palace-fumes.lua:59 |
| H06 | entry-03862 | confirmed | 叙事事实 | mercifully brief reign → 短暂的仁政；庆幸统治短暂误成仁慈的统治。 | 不是仁慈君主的独立设定，mercifully修饰brief。 | sources/dlc/orcs/tome-orcs/data/lore/palace-fumes.lua:59 |
| H07 | entry-03862 | confirmed | 叙事事实 | After a brief description of the events of the meeting → 简短地讨论了几件事后；正史简述会面变成会面前讨论事件。 | 后句仍讲会面，却不能把记录层的description变成场景里的discussion。 | sources/dlc/orcs/tome-orcs/data/lore/palace-fumes.lua:59 |
| H08 | entry-03862 | confirmed | 叙事事实 | yearly messages → 年度总结信息；每年来信被具体化成年度总结。 | 年度保留频率，但总结额外限定了消息内容。 | sources/dlc/orcs/tome-orcs/data/lore/palace-fumes.lua:59 |
| H09 | entry-03862 | confirmed | 叙事事实 | least of all ourselves → 这不可能对任何人有好处；尤其不利于自己的比较限定遗漏。 | 任何人包含自己，但不表达自身最受害的程度比较。 | sources/dlc/orcs/tome-orcs/data/lore/palace-fumes.lua:59 |
| H10 | entry-03866 | confirmed | 叙事事实 | ran face-first into a couple of them → 直接向几个兽人正面冲去；逃跑时迎面撞上兽人改成朝兽人冲去。 | 正在逃跑的前句使主动冲锋读法可疑，但中文朝目标冲去仍改变碰上事件。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H11 | entry-03866 | confirmed | 叙事事实 | tossed him around his lair → 在他的巢穴里把他扔了出去；在巢穴内反复抛掷改成扔出去。 | 扔的动作保留，空间方向和活动方式未保留。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H12 | entry-03866 | confirmed | 叙事事实 | swearing incomprehensibly about unfairness → 发表了一番关于不公平的费解的话；骂骂咧咧的说话方式未保留。 | 费解保留难懂，不保留swearing的辱骂语气。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H13 | entry-03866 | confirmed | 叙事事实 | right where she'd applied a wild infusion → 当她想用她仅有的那一个狂暴纹身时；击中纹身所在部位改成在尝试使用纹身时击中。 | 后句也尝试使用纹身，但不能代替原句的具体命中部位。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H14 | entry-03866 | pending | 叙事事实 | battleaxe → 双手斧；battleaxe 在游戏中可能对应具体双手武器类别；没有获准对应实体证据，不仅按一般词义判错。 | 角色还使用长剑；battleaxe词本身不能证明双手武器。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H15 | entry-03866 | confirmed | 叙事事实 | salivated at the prospect of traveling → 他旅行到远东；对未来赴远东残害兽人的期待变成已经赴远东并看到的事件。 | 后文确实到达远东，但不能反向抹掉此句当时的期待视角。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H16 | entry-03866 | advisory | 叙事事实 | direct combat → 近身战斗；后句为倒在烈火之刃下，近身战斗可承接当前情景；不足以确认对远程战斗另作错误声明。 | 烈火之刃提示近战场景，但原文比较的是直接作战适应性。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H17 | entry-03866 | confirmed | 叙事事实 | a demonic statue called out to her → 当她看到一个恶魔雕像时；雕像主动呼唤的事件被看到雕像取代。 | 看到可以与呼唤并存，但中文没有表达雕像发出呼唤。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H18 | entry-03866 | advisory | 表达建议 | effortlessly destroying any foe → 秒杀所有遇到的敌人；轻松消灭被限定为瞬间击杀。 | 秒杀可以夸张表达强大；是否构成实质时序限定宜保守，先记表达建议。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H19 | entry-03866 | pending | 叙事事实 | wild infusion → 狂暴纹身；术语候选野性纹身为core/entity name，本条DLC/_t不直接匹配；语义指称仍需中文映射。 | 不能凭该不适用术语行强制改名；缺可适用的同一技能中文映射。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:47 |
| H20 | entry-03867 | confirmed | 叙事事实 | a mere stepping stone on the way → 作为下一步攻入恐惧王座的据点；旅程中的过渡成就被具体化为攻城据点用途。 | 获得堡垒确实先于攻塔，但未证明把它作为军事据点。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H21 | entry-03867 | confirmed | 叙事事实 | in centuries → 那是和马基·埃亚尔分割了几个世纪的远东大陆；几个世纪以来首位跨大陆者，改成大陆隔绝几个世纪；首位的时间范围也失去。 | 历史隔绝可以解释无人来往，但不是本句原定量范围；按同一修饰归属变化计一项。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H22 | entry-03867 | confirmed | 叙事事实 | closed <?=Lore.pocket_time_winner.hisher?> eyes → 深吸一口气，穿过；穿越前闭眼的动作遗漏。 | 深呼吸和穿越保留，未包含闭眼。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H23 | entry-03867 | advisory | 叙事事实 | the wastes of Eruan → 艾露安的废墟；废墟也可作荒废地域描写；初判将其严格等同建筑残骸过强，尚无地貌冲突证据。 | 地名相同不能证明两类地貌等价。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H24 | entry-03867 | confirmed | 叙事事实 | Gerlyk, a god driven mad from isolation → 盖里克，在长期的隔绝之中陷入了无尽的疯狂；两个分支都未保留Gerlyk的神明身份。 | 远古威胁只说明危险性，不说明神明类别；重复分支合并一项。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H25 | entry-03867 | confirmed | 叙事事实 | what our champion did after that → 我们的英雄在之后去了哪里；不知后来做了什么缩为不知去了哪里。 | 后句不论如何是笼统承接，未补回活动范围。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H26 | entry-03867 | confirmed | 叙事事实 | the most trying challenge → 挑战者是出人意料的；最艰难的挑战改成出乎意料的挑战者。 | 艾琳是盟友使意外合理，但不能代替挑战难度评价。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H27 | entry-03867 | confirmed | 叙事事实 | despite the calls to help → 未能阻止法师们在灼烧之痕举行的仪式；听到求援仍未阻止仪式的让步信息遗漏。 | 前分支收到急报不属于此条件分支的必经文字；应按当前分支判断。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:72 |
| H28 | entry-03868 | confirmed | 叙事事实 | deeming many failures → 面对无数的困难；评估许多候选为失败改成讲故事者面对困难。 | 各种可能性保留选择背景，不能恢复失败评价的对象。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:102 |
| H29 | entry-03868 | confirmed | 叙事事实 | would be likely to find → 很快发现自己面对的东西；假设未来可能找到的敌人改成已发现的经历。 | 前句本可以保留一种假设，却被后句很快发现转成事实叙述。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:102 |
| H30 | entry-03868 | confirmed | 叙事事实 | inevitable doom in the Infinite Dungeon → 前往无尽地下城寻求无穷无尽的挑战；前往必然毁灭的结局改成寻求不断挑战。 | 无穷挑战并不必然表达角色死亡或毁灭。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:102 |
| H31 | entry-03868 | confirmed | 叙事事实 | to you in life → 我此生欠你这个机会；在现实生命中的你与传说人物的对照改为叙述者此生。 | 下一分句传说中的西方灾星支持现实/传说对照；不是叙述者寿命说明。 | sources/dlc/orcs/tome-orcs/data/lore/pocket-time.lua:102 |
| H32 | entry-03870 | pending | 叙事事实 | leaf-bound journal → 被书页包裹的笔记；树叶装订/包裹的笔记改成书页包裹。 | leaf可指书页，但随即枯萎及自然施法者日记语境支持植物叶；待核是否有更直接实体证据。 | sources/dlc/orcs/tome-orcs/data/lore/primal-forest.lua:88 |
| H33 | entry-03870 | confirmed | 叙事事实 | risk of mutating into something → 被人扭曲；奥术力量变异的风险加上人为施动者限制。 | 魔法有使用者，但原文没有把变异必然归于人。 | sources/dlc/orcs/tome-orcs/data/lore/primal-forest.lua:88 |
| H34 | entry-03870 | confirmed | 叙事事实 | support we'd otherwise lack → 我们过去所忽视的支持者；不用这种策略便得不到的支持，改成过去忽视的支持者。 | 新策略招募仍在，原文未说过去故意或无意忽视他们。 | sources/dlc/orcs/tome-orcs/data/lore/primal-forest.lua:88 |
| H35 | entry-03870 | confirmed | 叙事事实 | there were Ziguranth in the last century → 伊格兰斯一个世纪里招募的成员的数量；现有成员/上世纪成员的比较变成招募累计人数比较。 | 招募产生成员但不等于同一时点现有量；按比较对象一项计。 | sources/dlc/orcs/tome-orcs/data/lore/primal-forest.lua:88 |
| H36 | entry-03874 | confirmed | 叙事事实 | only allowed to live → 才被创造了出来；获准存活改成被创造的时点。 | 前段已说他们被造出，不能把允许生存等同首次创造。 | sources/dlc/orcs/tome-orcs/data/lore/weissi.lua:42 |
| H37 | entry-03874 | confirmed | 叙事事实 | I doubt any of them → 我们不认为众神中有人；叙述者个人看法变成群体共同看法。 | 全文多用我们描述种族，不自动把此处I的意见归给全体。 | sources/dlc/orcs/tome-orcs/data/lore/weissi.lua:42 |
| H38 | entry-03891 | confirmed | 机制/操作 | Whichever of your positive and negative energies is a higher percentage → 无论是你的正能量还是负能量都将用更高百分比的恢复；择占比更高的一种能量，改成正负能量均以更高百分比恢复。 | 后句两种速率都提高不等于前句两者都朝满值恢复；energies.lua:64–81分支支持。 | sources/dlc/orcs/tome-orcs/data/talents/celestial/energies.lua:124 |
| H39 | entry-03891 | confirmed | 机制/操作 | regenerates towards its max → 替代正常的休息值；朝最大值恢复的终点遗漏。 | 更高百分比不是最大值；正常静止值与最大值是不同概念。 | sources/dlc/orcs/tome-orcs/data/talents/celestial/energies.lua:124 |
| H40 | entry-03915 | confirmed | 机制/操作 | broken or cancelled → 攻击或者使用其他技能的动作都会中断效果，同时；主动取消时同样造成伤害的触发范围没有表达。 | 同时只承接攻击/使用技能中断；源码deactivate支持独立取消路径，目标版本另有限制。 | sources/dlc/orcs/tome-orcs/data/talents/steam/battlefield-management.lua:87 |
| H41 | entry-03994 | pending | 机制/操作 | ripples in radius 4 → 对半径 4 内的所有目标；中文全目标可能包含自身与召唤者，而快照明确排除二者。 | 英文也仅简述范围；这是中文新增全称与未固定实现之间的疑点，不能确认目标版本误述。 | sources/dlc/orcs/tome-orcs/data/talents/uber/mag.lua:41 |
| H42 | entry-04039 | advisory | 表达建议 | fully absorb any damaging actions → 几率吸收伤害；是否缺少完全吸收量的明确度。 | 吸收伤害可泛指整次拦截，未出现部分吸收限定；先作表达澄清。 | sources/dlc/orcs/tome-orcs/data/timed_effects/physical.lua:696 |
| H43 | entry-04078 | confirmed | 叙事事实 | did an amazing job of pain and destruction → 变成了一个恐怖的杀戮机器；对折磨者残害行为的评价改成雪人变成杀戮机器的结果。 | 装甲与链锯支持武器化外观，但不能代替原句对疼痛/摧残的评价。 | sources/dlc/orcs/tome-orcs/data/zones/gem/npcs.lua:94 |
| H44 | entry-04087 | advisory | 叙事事实 | The light of the Amulet → 神的光辉；在任何报告返回之前已撤销：同一护符名为 Gardanion, the Light of God；穿戴语境可用名称呼应其光辉。 | 护符可能带有神力，但原句的具体来源物品未保留。 | sources/dlc/orcs/tome-orcs/data/zones/slumbering-caves/objects.lua:57 |
| H45 | entry-04126 | pending | 机制/操作 | a third of the uses → 复制的数量除以 3；可用次数与额外复制数的分母是否相同。 | 更名为获得身体可承接收存机制；Possessors无源码，不能确认是总次数还是额外副本。 | 冻结原译；实现缺失 |
| N01 | entry-03841 | advisory | 叙事事实 | entity it detonates against → 引爆所波及；报告推定 against 只指碰撞命中，证据不足。 | 爆炸对目标引爆与波及目标有可接受交集；原广告没有 direct hit 或碰撞/范围对立。 | tome-orcs/data/lore/destructicus.lua |
| N02 | entry-03857 | confirmed | 叙事事实 | Assessment of the Species → 关于人种的调查；物种调查被收窄成人种。 | 同文件 misc.lua:136 系列另一章是 Steam Giants，支持跨物种分类。 | tome-orcs/data/lore/misc.lua |
| N03 | entry-03862 | advisory | 叙事事实 | shards of your ruined cities → 文明的废墟；整个人群覆灭的威胁中，文明废墟可作城市废墟的借代。 | 不据比喻转述推断实际搜寻范围扩大。 | tome-orcs/data/lore/palace-fumes.lua |
| N04 | entry-03867 | confirmed | 叙事事实 | Aeryn relented → 艾琳被击败了；罢手行为未表达；不确认胜负对象反转。 | 英文 winner 代词存在上游歧义；被打败本身不表达罢手，故仅保留遗漏这一子项。 | tome-orcs/data/lore/pocket-time.lua |
| N05 | entry-03868 | confirmed | 叙事事实 | Scourge from the West → 西方灾星；违反本包明确适用的 preferred 称号。 | terms.json society.tsv:34，_t/preferred/dlc，与本条完全匹配并明确排除灾星。 | tome-orcs/data/lore/pocket-time.lua |
| N06 | entry-03893 | advisory | 表达建议 | wall %d units long → 一堵墙长 %d；补单位和调整语序可改善清楚度。 | 已给墙长与持续时间两个独立参数，无证据表明读数被当成其他物理量。 | tome-orcs/data/talents/celestial/reflection.lua |
| N07 | entry-03734 | advisory | 叙事事实 | WASTE YOUR SHOT → 浪费子弹；确认提示中的惯用语成立。 | 子弹一词不承诺能补充弹药；一次性源码不能证明中文新增可重复使用。 | tome-orcs/data/chats/destructicus.lua |
| N08 | entry-03770 | advisory | 表达建议 | corrupted cave door → 被污染的山洞门；术语候选不是此 tag 的强制要求。 | entity subtype 与 entity name 不同；污染与腐化在此门名可作一致性建议。 | tome-orcs/data/general/grids/slumbering_cave.lua |
| N09 | entry-03862 | confirmed | 表达建议 | relations with our now-distant kin → 谈论过与我们今日的远亲风暴部族；与字结构缺中心语关系，语法残缺。 | 不是单纯省略连词；谈论过与某部族不能独立完成宾语。 | tome-orcs/data/lore/palace-fumes.lua |
| N10 | entry-03862 | confirmed | 表达建议 | recorded in a matter-of-fact nature → 确实完全实事求是的；缺判断词是，句尾的悬空。 | 可改为确实完全实事求是或确实是…的；现句不成立。 | tome-orcs/data/lore/palace-fumes.lua |
| N11 | entry-03862 | confirmed | 表达建议 | yearly messages → 在于在一条在；重复介词导致句法断裂。 | 该句同时存在年度信息内容问题，语法另计，未以标点风格判错。 | tome-orcs/data/lore/palace-fumes.lua |
| N12 | entry-03862 | advisory | 叙事事实 | yearly messages → 一条…年度总结信息；周期性仍由年度保留，不独立确认从每年变成一次。 | 具体化为总结已归 H08；不重复计入数量丢失。 | tome-orcs/data/lore/palace-fumes.lua |
| N13 | entry-03866 | confirmed | 表达建议 | when a skeletal warrior struck her → 这是，一个骷髅战士；这是应为这时，明确错字。 | 读者可猜到不等于文字无错。 | tome-orcs/data/lore/pocket-time.lua |
| N14 | entry-03866 | confirmed | 叙事事实 | lost his bearings → 失去平衡；失去方向感改成失衡。 | 抛掷可能同时造成失衡，但不能替代踩错方向的叙述。 | tome-orcs/data/lore/pocket-time.lua |
| N15 | entry-03867 | confirmed | 叙事事实 | way to challenge the grand magus Vor → 与大魔导师沃尔的战斗；途中风暴被放进与沃尔的战斗。 | 都在部落内不消除事件阶段差别。 | tome-orcs/data/lore/pocket-time.lua |
| N16 | entry-03867 | confirmed | 表达建议 | they were ever in danger → 出于怎样的危机；出于误作处于，明确错字。 | 不按专名间隔点另计缺陷。 | tome-orcs/data/lore/pocket-time.lua |
| N17 | entry-03867 | advisory | 表达建议 | Maj'Eyal → 马基埃亚尔／马基·埃亚尔；同名间隔点一致性建议。 | 两种字形都明确指同地；scope=core不绑定DLC，不能改称内部一致性后变相强制。 | tome-orcs/data/lore/pocket-time.lua |
| N18 | entry-03867 | confirmed | 叙事事实 | corrupted horrors of Yiikgur → 占据伊克格的恐魔；遗漏恐魔受到腐化的限定。 | 占据地点未表达腐化状态。 | tome-orcs/data/lore/pocket-time.lua |
| N19 | entry-03867 | confirmed | 叙事事实 | the dragon-tamers of Gorbat Pride, master wyrmics → 驯龙师和高阶龙战士；同位身份被拆成两类并列人物。 | 和在此没有即的同位释义。 | tome-orcs/data/lore/pocket-time.lua |
| N20 | entry-03867 | confirmed | 叙事事实 | Without a thought to where it led → 没有任何犹豫；未考虑目的地被泛化为不犹豫。 | 不犹豫也可能已知目的地；紧接未知传送场景不能自动补回该心理信息。 | tome-orcs/data/lore/pocket-time.lua |
| N21 | entry-03867 | confirmed | 叙事事实 | at her orders → 冲进了传送门中；奉艾琳命令这一行动来源遗漏。 | 前文艾琳在场不等于她下令。 | tome-orcs/data/lore/pocket-time.lua |
| N22 | entry-03868 | confirmed | 表达建议 | <? if Lore.pocket_time_winner.sacrifice then ?> → 站在了巅峰之上，<? if Lore.pocket_time_winner.sacrifice then ?>通过牺牲<?=Lore.pocket_time_winner.himher?>的生命来关闭了法师的远行传送门<? end ?>，从而；非牺牲分支产生双逗号，静态展开可重现。 | 这是实际重复字形而非要求原译标点一一相同；低影响显示文字错误，不称游戏崩溃。 | tome-orcs/data/lore/pocket-time.lua |
| N23 | entry-03868 | advisory | 表达建议 | it / its → 他／它；对拟人神灵的代词一致性建议。 | 指代仍唯一；他/它切换不证明性别、身份或作用主体改变。 | tome-orcs/data/lore/pocket-time.lua |
| N24 | entry-03868 | confirmed | 叙事事实 | whenever it found or created a threat → 直到它找到或者创造了；再次遇到威胁时想起他，被写成只记到某个终点。 | 愿意牢记直到找到虽保留承诺，但未保留原来的条件关系。 | tome-orcs/data/lore/pocket-time.lua |
| N25 | entry-03870 | confirmed | 表达建议 | also happen to be decent people → 碰巧上是好人；碰巧上是含衍字。 | 不影响大意仍属明确文字错误。 | tome-orcs/data/lore/primal-forest.lua |
| N26 | entry-03870 | confirmed | 表达建议 | significantly more credibility → 更加可信地多；地应为程度补语的得。 | 不是措辞偏好。 | tome-orcs/data/lore/primal-forest.lua |
| N27 | entry-03870 | confirmed | 叙事事实 | rogue mages → 游荡法师；失控或脱离约束的法师被改为移动状态。 | 反魔训练语境关注行为约束，不是法师是否游历。 | tome-orcs/data/lore/primal-forest.lua |
| N28 | entry-03870 | confirmed | 叙事事实 | attacks on Ziguranth patrols → 对伊格兰斯巡逻队的搜捕；袭击变为搜捕。 | 两者受事相同，否决报告所谓施受反转，仅确认行动性质差别。 | tome-orcs/data/lore/primal-forest.lua |
| N29 | entry-03870 | confirmed | 叙事事实 | the old guard → 过去的守护者；守旧派/元老派被当成昔日守护者。 | 与年轻自然精灵涌入并列构成派系代际对照。 | tome-orcs/data/lore/primal-forest.lua |
| N30 | entry-03870 | confirmed | 叙事事实 | alongside widespread acceptance of runes → 而没有意识到早在更早之前；并列原因被添加为未察觉的认知状态。 | 前文忽视政治趋势不等于此处已有认知失败。 | tome-orcs/data/lore/primal-forest.lua |
| N31 | entry-03870 | confirmed | 叙事事实 | mumbo-jumbo about the heavens → 有关天空的一系列繁文缛节；胡言说辞变成繁琐礼节。 | 包装奥术的论说不等于进行仪式；同句没有礼节证据。 | tome-orcs/data/lore/primal-forest.lua |
| N32 | entry-03870 | advisory | 叙事事实 | the raid on Zigur → 伊格被摧毁／对伊格的袭击；袭击及破坏结果的转述需一致性改善。 | 不凭孤立词推翻事件中已可能包含的摧毁结果；缺固定事件范围证据。 | tome-orcs/data/lore/primal-forest.lua |
| N33 | entry-03870 | advisory | 表达建议 | CAN → [b]真的可以[/b]；大小写强调转为有效粗体，未破坏信息结构。 | 不按标记集合机械相等判错。 | tome-orcs/data/lore/primal-forest.lua |
| N34 | entry-03877 | advisory | 叙事事实 | entire recorded history → 整个历史；历史记录语境可概括为整个历史。 | 无证据引入未记载时代，补有记载以来仅提高清楚度。 | tome-orcs/data/quests/amakthel.lua |
| N35 | entry-03915 | confirmed | 叙事事实 | The wheels of death! Amazing! → 冲锋！死亡之轮！！；赞叹真棒被改为冲锋命令。 | 不是感叹号数量问题；不同话语行为，低影响风味偏差。 | tome-orcs/data/talents/steam/battlefield-management.lua |
| N36 | entry-03923 | advisory | 叙事事实 | superheated steam → 蒸汽冲击波…火焰伤害；过热可由火焰伤害及后句更高温语境承接。 | 未额外指控基础波是冷蒸汽；可补词但不足确认错误。 | tome-orcs/data/talents/steam/engineering.lua |
| N37 | entry-03955 | pending | 机制/操作 | last 5 turns → 持续5回合；上游时长与快照 summon_time=8 不符。 | 忠实沿袭，不进入译文缺陷分母；目标版本未固定。 | tome-orcs/data/talents/steam/other.lua |
| N38 | entry-03962 | pending | 机制/操作 | cannot be used on rares → 稀有…无效；报告指出上游等级过滤疑点，需目标版本及rank语义核实。 | 即使成立也非中文新增；不以模型声称rank=3直接判定。 | tome-orcs/data/talents/steam/other.lua |
| N39 | entry-04078 | confirmed | 叙事事实 | several vital spots → 重要部分都；若干要害扩大为全部要害。 | 都的全称在此明确；非一般无类型限定伤害的既有豁免。 | tome-orcs/data/zones/gem/npcs.lua |
| N40 | entry-04078 | advisory | 表达建议 | its → 它／他；雪人代词一致性建议。 | 角色身份未变，不确认另一个对象。 | tome-orcs/data/zones/gem/npcs.lua |
| N41 | entry-04121 | advisory | 表达建议 | mainhand weapon and an offhand mindstar → 主手武器副手灵晶；可补和或顿号，现有并列可读。 | 主手/副手明确分隔，两项需求均在，不能凭缺连词判语法不成立。 | tome-possessors/data/talents/psionic/battle-psionics.lua |
| N42 | entry-04119 | advisory | 叙事事实 | strange and may be confusing to play for beginners → 机制相当奇怪，可能不适合新手使用；警告语境中的合理意译。 | 奇怪机制与可能不适合的完整句保留新手难掌握的警示；不等于禁止新手。 | tome-possessors/data/birth/psionic.lua |
| N43 | entry-04127 | pending | 机制/操作 | When you assume a form → 吞噬一具储备的身体，用来补充现在的身体；使用附身形态的限定明确度不足，原有当前身体也可承接。 | 无源码不能把 when assume 锁定为换身瞬间的唯一触发；先待确认，否决必然自动吞噬推断。 | tome-possessors/data/talents/psionic/body-snatcher.lua |
| N44 | entry-04127 | pending | 机制/操作 | As such may things that prevent healing → 阻止治疗的效果无法阻止吞噬生效；may疑为many，范围及实际豁免待核。 | 源句有误且缺组件源码；不将 many 推断直接升格为目标版本错误。 | tome-possessors/data/talents/psionic/body-snatcher.lua |
| N45 | entry-03866 | advisory | 表达建议 | Dazed and stumbling → 因震慑而失去平衡；叙事一般形容词不足以证明两种游戏效果混淆。 | effect subtype术语不匹配_t叙事，global不是所有语义和tag均强制。 | tome-orcs/data/lore/pocket-time.lua |
| N46 | entry-03866 | advisory | 叙事事实 | a couple of them → 几个兽人；couple 可在非计量叙事里泛指少数，几个是合理读法。 | 没有场景人数判定或后续数量对照锁定恰为二。 | tome-orcs/data/lore/pocket-time.lua |
| N47 | entry-03866 | advisory | 表达建议 | The Master → 吸血鬼领主／领主；增补身份与简称共存可接受。 | 报告自身认可身份正确；不以两个长度不同的称谓强迫同名。 | tome-orcs/data/lore/pocket-time.lua |
| N48 | entry-03866 | confirmed | 表达建议 | Climbing through the waves of shambling undead → 与一波波蹒跚的不死生物而战；与…而战搭配不成立。 | 可作与…战斗或为…而战；当前混合结构有误。 | tome-orcs/data/lore/pocket-time.lua |
| N49 | entry-03866 | advisory | 表达建议 | multi-hued wyrms → 七彩龙；七彩可作多色惯用语，不承诺恰有七色。 | entity subtype候选不得强加于_t叙事；不绕过tag限制。 | tome-orcs/data/lore/pocket-time.lua |
| N50 | entry-03868 | advisory | 表达建议 | in <?=Lore.pocket_time_winner.hisher?> legend → 传说中的西方灾星；完整末段明确是同一传奇人物，省略所有格不改变所指。 | 模板代词可按中文省略；不是位置格式参数错位，不按变量个数判错。 | tome-orcs/data/lore/pocket-time.lua |
| N51 | entry-03867 | confirmed | 叙事事实 | in the tower of High Peak → 在那里等待着的；牺牲分支首次地点高塔名称遗漏，那里缺先行词。 | 未显示另一非牺牲分支的准备进攻高塔段；后句高塔只给类型，未给专名。 | tome-orcs/data/lore/pocket-time.lua |
| N52 | entry-03867 | confirmed | 叙事事实 | what orcs are best known for → 以兽人中最强大的力量著称；兽人整体以蛮力著称改成该部落在兽人中最强。 | 强度的比较群体改变，不是主语省略。 | tome-orcs/data/lore/pocket-time.lua |
| N53 | entry-03867 | confirmed | 叙事事实 | orcs stood in → 格鲁希纳克部落的精英部队；增加精英部队身份。 | 部落强大不等于原句确认精英身份；只确认文本新增。 | tome-orcs/data/lore/pocket-time.lua |
| N54 | entry-03868 | advisory | 叙事事实 | reclaimed Sher'Tul fortress → 夏·图尔要塞；全文前段已说明主角夺回要塞。 | 所属对象已明确，同篇回指可压缩修饰；不单独计遗漏。 | tome-orcs/data/lore/pocket-time.lua |
| N55 | entry-03868 | confirmed | 叙事事实 | citizens of Eyal → 埃亚尔的世界；受害对象居民泛化为世界。 | 可能伤害世界也影响居民，不代表同一断言。 | tome-orcs/data/lore/pocket-time.lua |
| N56 | entry-03868 | confirmed | 叙事事实 | often with difficulty → 有时艰难取胜；经常艰难的频度被降为有时。 | 与sometimes/occasionally形成明确频度对照；低影响仍有可证区别。 | tome-orcs/data/lore/pocket-time.lua |
| N57 | entry-03868 | confirmed | 叙事事实 | room left for the rest of <?=Lore.pocket_time_winner.name?>'s life → 故事就此走到了尽头；故事不给人物余生留空间的信息未保留。 | 前句故事结束被重复，未保留人仍有余生的对照。 | tome-orcs/data/lore/pocket-time.lua |
| N58 | entry-03870 | confirmed | 叙事事实 | intimidation can get us anywhere → 暴力威慑是不能解决一切问题的；恐吓已无进展改成不能解决所有问题。 | 不能解决一切允许部分有效，与原文的阶段判断不同。 | tome-orcs/data/lore/primal-forest.lua |
| N59 | entry-03870 | confirmed | 叙事事实 | allowed the idea of supporting Nature over magic to survive → 我们高举着“自然胜过魔法”的旗号，从联合王国与晨曦之门的条约、对伊格的袭击，以及对伊格兰斯巡逻队的搜捕中幸存下来；存活的对象由理念变成组织成员。 | 高举理念不表达使理念免于消失，组织生存是另一个命题。 | tome-orcs/data/lore/primal-forest.lua |
| N60 | entry-03870 | advisory | 叙事事实 | further refine our techniques → 进一步锤炼自己…能力；教授我们的技法与精进学习者能力在课程语境可等价。 | 不足据所有格不同确认受益对象错误。 | tome-orcs/data/lore/primal-forest.lua |
| N61 | entry-03870 | advisory | 叙事事实 | old guard has been overrun with → 被…所代替；新人占主导可概括为旧派被替代。 | 未必断言每个旧成员离开；旧派译词问题已单列N29。 | tome-orcs/data/lore/primal-forest.lua |
| N62 | entry-03870 | advisory | 叙事事实 | damage magic may inflict → 魔法所造成的伤害；中文所造成可泛指潜在/一般结果。 | 没有时间词表明已经发生；不能仅因无may判事实化。 | tome-orcs/data/lore/primal-forest.lua |
| N63 | entry-03870 | confirmed | 叙事事实 | will make it more capable of resisting → 更加强大，才能抵挡；提升抵抗能力被改成必要条件。 | 才能比更能的逻辑强度更高；仅文本设定，不夸为游戏机制。 | tome-orcs/data/lore/primal-forest.lua |
| N64 | entry-03874 | advisory | 叙事事实 | no one of them → 没人；上句众神提供了量词范围。 | 不合理地把中文没人脱离紧邻主语扩大到整个宇宙。 | tome-orcs/data/lore/weissi.lua |
| N65 | entry-03874 | advisory | 叙事事实 | ire of the universe, of fate itself → 天怒人怨，被命运所诅咒；拟人化厄运的意译成立。 | 命运诅咒可作比喻；不必等于下段特定时空法术的实然断言。 | tome-orcs/data/lore/weissi.lua |
| N66 | entry-03874 | advisory | 叙事事实 | Or maybe … powerful enough to put → 或者我们只是激怒了…给我们施加了；或许假说仍统摄全句，未变为确定事实。 | 不能将局部给…施加从或许作用域中割离。 | tome-orcs/data/lore/weissi.lua |
| N67 | entry-03874 | advisory | 叙事事实 | carry it deep within ourselves → 在自身的存在中也一直传承下来；种族承载创造者情绪的完整段允许传承意象。 | 宾语可以承上文憎恨等，不证明新增特定代际事件。 | tome-orcs/data/lore/weissi.lua |
| N68 | entry-03915 | advisory | 表达建议 | two sentences / line breaks → 合并两句；换行/并句不构成独立缺陷。 | 主动取消信息遗漏已H40计，不重复把同一问题按换行计数。 | tome-orcs/data/talents/steam/battlefield-management.lua |
| N69 | entry-03923 | advisory | 表达建议 | (current factor %d%%) → 当前强度系数 %d%%。；括注另起一行仍明确补充前句。 | 未丢参数、范围或层级，规则禁止按换行数判错。 | tome-orcs/data/talents/steam/engineering.lua |
| N70 | entry-03923 | advisory | 表达建议 | radius %d → 半径 %d；原文也没有单位，参数语义相同。 | 不能以另一条有单位强判本条漏译。 | tome-orcs/data/talents/steam/engineering.lua |
| N71 | entry-03932 | advisory | 机制/操作 | evade/are missed by → 闪避或躲闪；攻击未命中在中文可说被躲闪。 | 报告未查callback且主动/被动语言不等于两种互斥机制；没有证据证明排除miss路径。 | tome-orcs/data/talents/steam/gunslinging.lua |
| N72 | entry-04078 | advisory | 叙事事实 | reinforced with stralite plating → 被斯莱特装甲所覆盖；装甲覆盖表达防护加强，可接受。 | 若干→全部另计N39；不将防护同义描写另拆。 | tome-orcs/data/zones/gem/npcs.lua |
| N73 | entry-04119 | advisory | 表达建议 | BEWARE: This class is very strange → 注意: 该职业机制相当奇怪；注意及机制是警告语境合理表达，半角冒号不构成缺陷。 | 不以强度感受或标点风格自动确认。 | tome-possessors/data/birth/psionic.lua |
| N74 | entry-04127 | advisory | 机制/操作 | you may cannibalize → 吞噬一具储备的身体；技能说明动词直陈不等于必然自动触发。 | may为可选操作，标题/技能说明语境允许此语法，不额外确认意愿变化。 | tome-possessors/data/talents/psionic/body-snatcher.lua |
| N75 | entry-04127 | advisory | 表达建议 | separate final sentence → 吞噬是治疗身体的唯一方法。；合段仍保留唯一方法的独立完整句。 | 不按换行行数推断信息损失。 | tome-possessors/data/talents/psionic/body-snatcher.lua |
| N76 | entry-03740 | advisory | 机制/操作 | at will → 具有召唤他的能力；玩家得到可发动的召唤能力允许主动使用的读法。 | 不另确认无限次或强制触发；持续数回合和永久绑定分别单列。 | tome-orcs/data/chats/john-surrender.lua |
| N77 | entry-03866 | pending | 叙事事实 | bone armor → 骨盾；骨甲与骨盾是否对应既有技能名待核。 | 未获准对应定义，不能以武器/护甲一般词典义覆盖游戏命名。 | tome-orcs/data/lore/pocket-time.lua |
| N78 | entry-03866 | confirmed | 叙事事实 | while leaving his hands free → 一种在空中挥动法杖的心灵潜能；悬空操杖同时解放双手的信息遗漏。 | 前文徒手格斗能力不等于本动作仍保持双手空闲。 | tome-orcs/data/lore/pocket-time.lua |
| N79 | entry-03866 | confirmed | 叙事事实 | master a few of these → 在这些方面都有了一些实战经验；掌握其中几项被改成各方面只有一些经验。 | 不是只删程度副词，熟练程度和涉及能力集合均改变，合计为能力状态一项。 | tome-orcs/data/lore/pocket-time.lua |
| N80 | entry-03866 | advisory | 表达建议 | a pair of earthen missiles → 一双石弹；量词生硬，但两枚含义仍在。 | 可改两发；不指控数值或对象错误。 | tome-orcs/data/lore/pocket-time.lua |
| N81 | entry-03867 | pending | 机制/操作 | fight by hisher side → 与<?=Lore.pocket_time_winner.hisher?>并肩作战；所有格模板值是否自带的需核对中文取值。 | 缺本地化短串，不能断言实际渲染一定语病；变量个数不单独判错。 | tome-orcs/data/lore/pocket-time.lua |
| N82 | entry-03870 | confirmed | 叙事事实 | they found themselves sliding into irrelevance → 不知道自己已经变成了无关紧要的局外人；落入边缘状态被增写成不知道该状态。 | found themselves 不必强调主动察觉，但也不表达不知道；具体认知否定是新增信息。 | tome-orcs/data/lore/primal-forest.lua |
| N83 | entry-03870 | advisory | 表达建议 | If … then … → 既然…淡忘。…那么，；跨句条件结构略拗口但完整逻辑仍在。 | 不按句号位置机械判残句。 | tome-orcs/data/lore/primal-forest.lua |
| N84 | entry-03870 | confirmed | 叙事事实 | These allies will help us support Nature → 这些盟友对我们在保护自然事业上的支持达到了；未来预期帮助被写成已达到的支持。 | 已拥有盟友不等于原文承诺的帮助已实现。 | tome-orcs/data/lore/primal-forest.lua |
| N85 | entry-03976 | advisory | 机制/操作 | it will vaporize → 子弹…将气化；it所指有歧义，湿润被移除的实现不能证明作者只指水。 | 译文动作与爆炸关系成立，未固定实现也不决定叙述主语唯一读法。 | tome-orcs/data/talents/steam/psytech-gunnery.lua |
| N86 | entry-03932 | advisory | 叙事事实 | Using small engines → 开启引擎；反射强化语境保留引擎作用，尺寸小可补充。 | 不按每个修饰词机械计遗漏。 | tome-orcs/data/talents/steam/gunslinging.lua |
| N87 | entry-03866 | advisory | 叙事事实 | as his friend was cut down → 在他的朋友被兽人战士砍倒后；as 在紧接的逃亡事件中可承接当时/随着，不足以确认可测的严格同时关系。 | 报告把一般事件连接词硬解为同时触发；这是时序明确度建议。 | tome-orcs/data/lore/pocket-time.lua |
| N88 | entry-03867 | confirmed | 表达建议 | far more dangerous → 可怕的多；程度补语应为可怕得多。 | 原文对应恐怖程度比较；属于明确错字，不是半角标点或版式偏好。 | tome-orcs/data/lore/pocket-time.lua |
| N89 | entry-03862 | advisory | 表达建议 | My fellow councilors, → 我的同僚们；空行和段落合并未改变呼语所属。 | 没有显示损坏或逻辑依赖证据，不能仅按23→21段认定结构缺陷。 | tome-orcs/data/lore/palace-fumes.lua |
| N90 | entry-03866 | advisory | 表达建议 | paragraph breaks → 额外空行；空行数量变化本身不是翻译缺陷。 | 段落、模板和事件仍可辨，没有信息丢失证据。 | tome-orcs/data/lore/pocket-time.lua |
| N91 | entry-03867 | advisory | 叙事事实 | ancient, impossibly advanced Farportal → 发达到让人难以置信的远行传送门；古老修饰可补充以提高清楚度。 | 叙述仍保留古代科技通路及其先进特征；未据遗漏一个修饰词另立事件或机制错误。 | tome-orcs/data/lore/pocket-time.lua |
| N92 | entry-03867 | advisory | 叙事事实 | held up the Orb of Many Ways to activate it → 手握着多元水晶球；举球激活的目的可以更明确。 | 该句接着描述通过作响旋转的传送门，球与通行的联系仍在，作为动作明确度建议。 | tome-orcs/data/lore/pocket-time.lua |
| N93 | entry-03874 | advisory | 叙事事实 | Long before their creation → 在他们被创造出来之前；可补很久以保留时间距离。 | 先于创造、众神尚年轻的完整历史关系保留；此处未给确定年代或数量边界。 | tome-orcs/data/lore/weissi.lua |
| N94 | entry-03955 | advisory | 表达建议 | newline indentation → 裸换行；缩进字符差异不足确认显示缺陷。 | 各说明行仍完整，未给出引擎中段落层级破坏的证据。 | tome-orcs/data/talents/steam/other.lua |
| N95 | entry-03962 | advisory | 表达建议 | newline indentation and trailing period → 全角空格及省略末尾孤立句点；等效缩进与删除英文残留句点不构成信息遗漏。 | 不按字符或换行计数机械判错；没有数值、目标或标记损坏。 | tome-orcs/data/talents/steam/other.lua |
| N96 | entry-03866 | advisory | 表达建议 | name template followed by comma → 半角逗号加空格；中英文标点形式差异仅为排版建议。 | 不是模板闭合、参数消费或动态分支损坏。 | tome-orcs/data/lore/pocket-time.lua |
| N97 | entry-03867 | advisory | 表达建议 | <?=Lore.pocket_time_winner.name?> refused to back down → <?=Lore.pocket_time_winner.himher?>绝不愿朝困难屈服；姓名改成同一人物的代词，完整语境指代明确。 | 中文无英语主宾格强制，himher实际中文短串也未获证；不能把变量种类差集当作错译。 | tome-orcs/data/lore/pocket-time.lua |
| N98 | entry-04126 | advisory | 表达建议 | copies. → 克隆体.；半角句点只需排版统一。 | 不改变句界、数值或运行解析，不计确认错译。 | tome-possessors/data/talents/psionic/body-snatcher.lua |
| N99 | entry-03915 | advisory | 表达建议 | Amazing! → 冲锋！死亡之轮！！；感叹号数量不构成独立错译。 | 话语行为变化已N35确认；不把其标点差异重复计为缺陷。 | tome-orcs/data/talents/steam/battlefield-management.lua |
| N100 | entry-03868 | advisory | 叙事事实 | a few different options → 各种各样的可能性；几种不同可能性可概括为各种可能性。 | 没有确切计量或场景数量约束，不把各种各样强解为数量很多。 | tome-orcs/data/lore/pocket-time.lua |
| N101 | entry-03868 | advisory | 叙事事实 | It considered → 他会综合考虑；中文会可描述人物一贯的考虑方式。 | 英文过去式不要求中文另设已完成标志；完整人物回顾允许此表达。 | tome-orcs/data/lore/pocket-time.lua |

## 原始候选到参考项的映射

confirmed 候选降为表达建议时，host_decision=refuted 表示其“确认错译”主张不成立，并非否认它可以润色。pending 不计入真阳或假阳。复合候选按独立意义变化拆子编号；重复分支和重复措辞统一合并。

| 阶段与原编号 | 原状态 | 宿主裁决 | 参考编号 | 备注 |
|---|---|---|---|---|
| P:C01.1 | confirmed | accepted | H02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C01.2 | confirmed | refuted | N76 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C02 | confirmed | refuted | N01 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C03 | confirmed | accepted | N02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C04 | confirmed | accepted | H04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C05 | confirmed | accepted | H06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C06 | confirmed | accepted | H08 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C07 | confirmed | refuted | N03 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C08 | confirmed | accepted | H15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C09 | confirmed | accepted | H27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C10 | confirmed | accepted | N04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C11 | confirmed | accepted | N05 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C12 | confirmed | accepted | H33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C13 | advisory | accepted | H36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C14 | confirmed | accepted | H38 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C15 | advisory | advisory | N06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C16 | confirmed | accepted | H40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C17 | confirmed | refuted | H42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| P:C18 | confirmed | accepted | H43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C01 | confirmed | refuted | N07 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C02.1 | confirmed | accepted | H01 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C02.2 | confirmed | accepted | H02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C02.3 | confirmed | refuted | N76 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C03 | confirmed | refuted | H03 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C04 | pending | advisory | N08 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C05 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C06 | confirmed | accepted | N02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C07 | confirmed | accepted | H04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C08 | confirmed | accepted | H06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C09 | confirmed | accepted | H07 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C10.1 | confirmed | accepted | N09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C10.2 | confirmed | accepted | N10 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C10.3 | confirmed | accepted | N11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C10.4 | confirmed | accepted | H08 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C10.5 | confirmed | refuted | N12 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C11 | confirmed | accepted | H09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C12 | advisory | advisory | N17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C13 | confirmed | accepted | H13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C14 | confirmed | accepted | H15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C15 | confirmed | accepted | N13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C16.1 | advisory | accepted | H11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C16.2 | advisory | accepted | N14 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C17 | advisory | advisory | N49 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C18.1 | confirmed | accepted | H21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C18.2 | confirmed | accepted | H22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C19 | confirmed | accepted | N15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C20 | confirmed | accepted | H27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C21.1 | confirmed | accepted | N16 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C21.2 | confirmed | refuted | N17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C22.1 | confirmed | accepted | H20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C22.2 | confirmed | accepted | N18 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C23.1 | advisory | accepted | N19 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C23.2 | advisory | advisory | H23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C23.3 | advisory | accepted | N20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C23.4 | advisory | accepted | N21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C23.5 | advisory | accepted | H26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C24 | confirmed | accepted | N22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C25 | confirmed | accepted | N05 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C26 | confirmed | accepted | H28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C27 | confirmed | refuted | N23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C28.1 | advisory | accepted | H30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C28.2 | advisory | accepted | N24 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C29 | confirmed | pending | H32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C30.1 | confirmed | accepted | N25 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C30.2 | confirmed | accepted | N26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C31.1 | confirmed | accepted | N27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C31.2 | confirmed | accepted | N28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C31.3 | confirmed | accepted | N29 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C32.1 | confirmed | accepted | H34 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C32.2 | confirmed | accepted | N30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C33.1 | advisory | accepted | N31 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C33.2 | advisory | advisory | N32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C33.3 | advisory | advisory | N33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C33.4 | advisory | advisory | N83 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C34 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C35.1 | confirmed | accepted | H37 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C35.2 | confirmed | accepted | H36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C36 | advisory | advisory | N34 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C37.1 | confirmed | accepted | H38 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C37.2 | confirmed | refuted |  | 括注紧接正常的休息值，其参数归属可由原译相同结构承接。 |
| A2:C38 | advisory | advisory | N06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C39 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C40 | confirmed | accepted | H40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C41.1 | advisory | accepted | N35 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C41.2 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C42 | advisory | advisory | N36, N69 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C43 | advisory | pending | N37 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C44.1 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C44.2 | advisory | pending | N38 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C45 | advisory | pending | H41 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C46 | confirmed | refuted | H42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C47.1 | confirmed | accepted | H43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C47.2 | confirmed | accepted | N39 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C48 | advisory | advisory | N40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C49 | confirmed | refuted | H44 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C50 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C51 | confirmed | refuted | N41 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C52 | confirmed | refuted | N42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C53 | pending | pending | H45 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C54.1 | confirmed | pending | N43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C54.2 | confirmed | refuted | N74 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C55 | pending | pending | N44 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C56 | advisory | pending | N50, N81 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| A2:C57 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C01 | confirmed | refuted | N01 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C02 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C03 | confirmed | accepted | H06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C04 | confirmed | accepted | H07 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C05.1 | confirmed | refuted | N12 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C05.2 | confirmed | accepted | H08 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C05.3 | confirmed | accepted | N11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C06.1 | confirmed | accepted | H09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C06.2 | confirmed | refuted |  | 抱着意图虽生硬，但宾语与承接主语都在，未证句法残缺。 |
| B2:C07 | confirmed | refuted | N17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C08 | confirmed | accepted | N09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C09.1 | confirmed | accepted | N10 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C09.2 | confirmed | refuted |  | their boorish behavior 在本段讨论true nature语境下可作本性中的粗野举动；不独立确认新增人格本质判断。 |
| B2:C10 | confirmed | refuted | N45 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C11 | confirmed | accepted | H13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C12.1 | confirmed | accepted | H10 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C12.2 | confirmed | refuted | N46 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C13 | confirmed | refuted | N87 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C14.1 | confirmed | accepted | H11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C14.2 | confirmed | accepted | N14 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C15 | confirmed | refuted | N47 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C16.1 | confirmed | accepted | N13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C16.2 | confirmed | accepted | N48 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C17 | confirmed | refuted | N49 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C18 | confirmed | accepted | H15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C19 | confirmed | refuted | N50 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C20 | confirmed | accepted | N05 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C21 | confirmed | accepted | H21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C22 | confirmed | accepted | N51 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C23.1 | confirmed | accepted | H27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C23.2 | confirmed | refuted |  | 完整条目已明确两位法师要举行仪式，补法师们有同文依据。 |
| B2:C24 | confirmed | refuted | N17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C25 | confirmed | accepted | H20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C26 | confirmed | accepted | N15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C27 | confirmed | accepted | N19 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C28.1 | confirmed | accepted | N52 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C28.2 | confirmed | accepted | N53 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C29 | confirmed | refuted | H23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C30.1 | confirmed | accepted | N20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C30.2 | confirmed | accepted | N21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C31 | confirmed | accepted | H24 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C32 | confirmed | accepted | N22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C33.1 | confirmed | accepted | H28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C34 | confirmed | accepted | N24 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C35.1 | confirmed | accepted | H30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C35.2 | confirmed | refuted | N54 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C36.1 | confirmed | accepted | H29 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C36.2 | confirmed | accepted | N55 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C37 | confirmed | accepted | N56 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C38 | confirmed | accepted | N57 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C39 | confirmed | refuted | N23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C40 | confirmed | pending | H32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C41 | confirmed | accepted | N58 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C42 | confirmed | accepted | H34 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C43.1 | confirmed | accepted | N59 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C43.2 | confirmed | accepted | N28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C44.1 | confirmed | refuted | N60 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C44.2 | confirmed | accepted | N27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C45.1 | confirmed | accepted | N29 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C45.2 | confirmed | refuted | N61 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C46.1 | confirmed | refuted | N62 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C46.2 | confirmed | accepted | N63 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C47.1 | confirmed | accepted | N25 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C47.2 | confirmed | accepted | N26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C48 | advisory | advisory | N33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C49 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C50 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C51 | confirmed | accepted | H36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C52.1 | confirmed | accepted | H37 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C52.2 | confirmed | refuted | N64 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C53 | confirmed | refuted | N65 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C54 | confirmed | refuted | N66 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C55 | confirmed | refuted | N67 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C56.1 | confirmed | accepted | H38 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C56.2 | confirmed | accepted | H39 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C57 | confirmed | refuted | N06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C58 | advisory | advisory | N06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C59 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C60 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C61 | confirmed | accepted | H40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C62 | confirmed | refuted | N68 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C63.1 | confirmed | accepted | N35 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C64 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C65 | confirmed | refuted | N69 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C66.1 | confirmed | refuted | N70 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C66.2 | confirmed | refuted | N36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C67 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C68 | confirmed | refuted | N71 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C69 | advisory | advisory | N86 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C70 | advisory | advisory | N85 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C71 | confirmed | refuted | H42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C72 | confirmed | accepted | H43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C73.1 | confirmed | accepted | N39 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C73.2 | confirmed | refuted | N72 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C74 | confirmed | refuted | N40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C75 | confirmed | refuted | N42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C76 | confirmed | refuted | N73 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C77 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C78.1 | confirmed | pending | N43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C78.2 | confirmed | refuted | N74 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C79 | confirmed | pending | N44 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C80 | confirmed | refuted | N75 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U01 | advisory | advisory | N03 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U02 | advisory | pending | N77 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U03 | advisory | accepted | H17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U04 | advisory | accepted | N78 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U05 | advisory | accepted | N79 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U06 | advisory | advisory | N80 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U07 | pending | pending | N81 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U08 | pending | accepted | N04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U09 | advisory | accepted | H26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U10 | advisory | accepted | H22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U11 | advisory | accepted | H25 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U12 | advisory | accepted | N16 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U13 | advisory | accepted | N31 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U14 | advisory | accepted | H33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U15 | advisory | accepted | N82 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U16 | advisory | accepted | N30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U17 | advisory | advisory | N32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U18 | advisory | advisory | N83 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U19 | advisory | accepted | N84 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C33.2 | confirmed | refuted | N100 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C33.3 | confirmed | refuted | N101 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:C63.2 | confirmed | refuted | N99 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U20 | advisory | advisory | N89 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U21 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U22 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U23 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U24 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U25 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U26 | advisory | advisory | N90 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U27 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U28 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U29 | advisory | advisory | N91 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U30 | advisory | advisory | N92 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U31 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U32 | advisory | accepted | N88 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U33 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U34 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U35 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U36 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U37 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U38 | advisory | advisory | N93 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U39 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U40 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U41 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U42 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B2:U43 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K01.1 | confirmed | accepted | H02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K01.2 | confirmed | refuted | N76 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K02 | confirmed | refuted | N01 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K03 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K04 | confirmed | accepted | N02 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K05 | confirmed | accepted | H04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K06 | confirmed | accepted | H06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K07.1 | confirmed | accepted | H08 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K07.2 | confirmed | refuted | N12 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K07.3 | confirmed | accepted | N11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K08 | advisory | advisory | N03 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K09 | confirmed | accepted | H07 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K10 | confirmed | accepted | H09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K11 | confirmed | refuted | N17 | 映射表K11部分写advisory，去重表及B2:C24明确confirmed；按最终去重结论计，并披露内部不一致。 |
| B3:K12 | confirmed | accepted | N09 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K13.1 | confirmed | accepted | N10 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K13.2 | confirmed | refuted |  | 同B2:C09.2，完整本性语境允许该转述，非独立缺陷。 |
| B3:K14 | advisory | advisory | N45 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K15 | confirmed | accepted | H13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K16.1 | confirmed | accepted | H10 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K16.2 | confirmed | refuted | N46 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K17 | advisory | advisory | N87 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K18.1 | confirmed | accepted | H11 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K18.2 | confirmed | accepted | N14 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K19 | advisory | advisory | N47 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K20.1 | confirmed | accepted | N13 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K20.2 | confirmed | accepted | N48 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K21 | advisory | advisory | N49 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K22 | confirmed | accepted | H15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K23 | confirmed | accepted | H21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K24 | confirmed | accepted | N51 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K25.1 | confirmed | accepted | H27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K25.2 | confirmed | refuted |  | 同B2:C23.2，全文已说明两位法师举行仪式。 |
| B3:K26 | confirmed | accepted | H20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K27 | confirmed | accepted | N15 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K28 | confirmed | accepted | N19 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K29.1 | confirmed | accepted | N52 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K29.2 | confirmed | accepted | N53 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K30 | confirmed | refuted | H23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K31.1 | confirmed | accepted | N20 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K31.2 | confirmed | accepted | N21 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K32 | confirmed | accepted | H24 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K33 | pending | accepted | N04 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K34 | confirmed | refuted | N50 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K35 | confirmed | accepted | N05 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K36 | confirmed | accepted | N22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K37.1 | confirmed | accepted | H28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K37.2 | confirmed | refuted | N100 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K37.3 | confirmed | refuted | N101 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K38 | confirmed | accepted | N24 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K39.1 | confirmed | accepted | H30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K39.2 | confirmed | refuted | N54 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K40.1 | confirmed | accepted | H29 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K40.2 | confirmed | accepted | N55 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K41 | confirmed | accepted | N56 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K42 | confirmed | accepted | N57 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K43 | confirmed | refuted | N23 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K44 | confirmed | pending | H32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K45 | confirmed | accepted | N58 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K46 | confirmed | accepted | H34 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K47.1 | confirmed | accepted | N59 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K47.2 | confirmed | accepted | N28 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K48.1 | confirmed | refuted | N60 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K48.2 | confirmed | accepted | N27 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K49.1 | confirmed | accepted | N29 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K49.2 | confirmed | refuted | N61 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K50.1 | confirmed | refuted | N62 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K50.2 | confirmed | accepted | N63 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K51.1 | confirmed | accepted | N25 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K51.2 | confirmed | accepted | N26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K52 | advisory | advisory | N33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K53 | confirmed | accepted | H33 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K54 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K55 | pending | pending |  | 报告状态混用时保留其明确的证据缺口，不计确认发现。 |
| B3:K56 | confirmed | accepted | H36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K57.1 | confirmed | accepted | H37 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K57.2 | confirmed | refuted | N64 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K58 | confirmed | refuted | N65 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K59 | confirmed | refuted | N66 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K60 | confirmed | refuted | N67 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K61.1 | confirmed | accepted | H38 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K61.2 | confirmed | accepted | H39 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K62 | advisory | advisory | N06 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K63 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K64 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K65.1 | confirmed | accepted | H40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K65.2 | confirmed | refuted | N68 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K66.1 | confirmed | accepted | N35 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K66.2 | confirmed | refuted | N99 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K67 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K68 | confirmed | refuted | N69 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K69.1 | advisory | advisory | N70 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K69.2 | advisory | advisory | N36 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K70 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K71 | advisory | advisory | N71 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K72 | advisory | advisory | N86 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K73 | advisory | advisory | N85 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K74 | confirmed | refuted | H42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K75 | confirmed | accepted | H43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K76.1 | confirmed | accepted | N39 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K76.2 | confirmed | refuted | N72 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K77 | confirmed | refuted | N40 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K78 | advisory | advisory | N42 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K79.1 | confirmed | refuted | N73 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K79.2 | advisory | advisory | N73 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K80 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K81.1 | confirmed | pending | N43 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K81.2 | confirmed | refuted | N74 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K82 | confirmed | pending | N44 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:K83 | confirmed | refuted | N75 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U01 | confirmed | refuted | N89 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U02 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U03 | pending | pending | N77 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U04 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U05 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U06 | confirmed | accepted | H17 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U07 | confirmed | accepted | N78 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U08 | advisory | accepted | N79 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U09 | pending | pending |  | 报告状态混用时保留其明确的证据缺口，不计确认发现。 |
| B3:U10 | advisory | advisory | N80 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U11 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U12 | confirmed | refuted | N90 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U13 | pending | pending | N81 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U14 | confirmed | accepted | H26 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U15 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U16 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U17.1 | confirmed | refuted | N91 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U17.2 | confirmed | accepted | H22 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U17.3 | confirmed | refuted | N92 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U18 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U19 | confirmed | accepted | N88 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U20 | confirmed | accepted | N16 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U21 | confirmed | accepted | H25 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U22 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U23 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U24 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U25 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U26 | confirmed | accepted | N31 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U27 | confirmed | accepted | N82 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U28 | confirmed | accepted | N30 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U29 | advisory | advisory | N32 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U30 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U31 | advisory | advisory | N83 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U32 | advisory | accepted | N84 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U33 | confirmed | refuted | N93 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U34 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U35 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U36 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U37 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:U38 | advisory | advisory |  | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW01 | confirmed | accepted | H01 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW02 | confirmed | refuted | N94 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW03 | confirmed | refuted | N95 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW04 | confirmed | refuted | N96 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW05 | advisory | pending | H19 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW06 | confirmed | refuted | N97 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
| B3:NEW07 | confirmed | refuted | N98 | 见对应参考项；未挂参考编号的 advisory 为原报告的措辞/一致性建议，不作缺陷计分。 |
