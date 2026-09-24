# 批阅裁决台账 — batch-03

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`202e1b86397880f8803595b3007ee5840a04cf8547047a3349c4977571a753b4`
- 决策行：40；冻结修订（含孪生载体）：40
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 38 |
| deferred | 2 |

## 被驳回／未采纳的模型主张

| entry | 模型主张 | 裁决 | 理由 |
| --- | --- | --- | --- |
| entry-00244 | 去掉 ` area effect` 的前导空格造成中文拼接缺陷 | rejected | 模型主张补回空格。固定源码 MapEffects.lua:23 为 `dam_def.name .. _t" area effect"` 直接拼接，补空格会显示「火焰 范围效果」，反证模型建议有害。 |
| entry-00221 | 「离开地图」构成明显误译 | rejected | 模型自标 advisory。源码 Game.lua:926-936 的 can_change_level 阻止任何换层/换区域，「离开地图」覆盖该限制，功能含义正确；level/zone 统一译法属跨条目策略，非本条缺陷。 |
| entry-00345 | 「使这次攻击发生偏斜」弱化招架，应改「招架」 | rejected | 模型自标 advisory。源码确认招架成功挡住攻击，现译保留防御成功含义，属文风偏好，不构成缺陷。 |
| entry-00185 | 方括号内多空格 | rejected | 模型自标 advisory。用户策略明确纯静态排版不算缺陷；方括号不属「括号不一致」策略范围。 |
| entry-00254 | 「最大 50%」与同组「最大40%」排版不一致 | rejected | 模型自标 advisory；仅为数字前空格差异，属纯静态排版，按用户策略不整理。 |
| entry-00419 | 「超过1500点」与同组「超过 600 点」空格不一致 | rejected | 模型自标 advisory；纯静态排版差异，按用户策略不整理。 |
| entry-00428 | 三扇传送门句式与同系列不平行 | rejected | 模型自标 advisory；条件、数量、机制均正确，句式平行属文风偏好。 |
| entry-00334 | 「杀死」应为「击杀」 | rejected | 模型自标 advisory；日志在敌人 on_die 中输出，「杀死」与触发事实一致，击杀仅为界面习惯差异。 |
| entry-00434 | 「珠宝匠托付」应改为更贴近源码关系 | rejected | 模型自标 advisory；Master Jeweler 对应珠宝匠，译文为可接受意译，任务名已增补，无缺陷。 |
| entry-00393 | 复合后缀外层半角括号 | rejected_on_entry | 本条 entry-00393 本身已是全角；模型所指的半角外层括号实际出现在 entry-00395–00400（同一 hrq-00046 行的其他载体），已按 bracket_fullwidth 修复那些载体。 |
| entry-00184 | 「勇敢的向前」语病、段间缺空行 | accepted_upstream | 缺陷成立，但主工作区 HEAD 11b3e963 已修（已核逐字）。按 SPEC 规则不在本 worktree 重复修改，记 defer；不接受在本分支重复改。 |

## 逐条裁决

| queue_id | entry_id | 文件:行 | 模型意见 | ORCHESTRATOR 裁决 | 是否落实 | 理由 |
| --- | --- | --- | --- | --- | --- | --- |
| hrq-00092 | entry-00730 | mod-tome.lua:8265 | defer | deferred | 否 | all 的强调有遗漏，但固定源码同串还用于 arena/npcs.lua，仓内 mod-tome.lua:37898（entry-02906）共享同一运行时键。该载体不在本批冻结集合；只改本条会造成跨组件同键多译冲突。须与冻结外条目联动，故 defer。独立核验：entry-02906 确实存在且不在队列中。 |
| hrq-00093 | entry-00731 | mod-tome.lua:8266 | fix | accepted | 是 | 术语库无 eldritch eye 条目；creatures.tsv:24 备注「专名（Eldritch eye 艾尔德里奇之眼…）保留音译」。但该备注本身即指定音译形式，而现译「骇异之眼」用的是语义直译。属未授权术语决定，记 no_change 并列入术语待办。 |
| hrq-00094 | entry-00733 | mod-tome.lua:8298 | fix | accepted | 是 | pulsates 漏译；「不停的扭动」应为状语「不停地」。 |
| hrq-00095 | entry-00740 | mod-tome.lua:8402 | fix | accepted | 是 | 「在毁灭生者」把 seek to destroy 的目的/意图写成进行时，改变机制含义。 |
| hrq-00096 | entry-00746 | mod-tome.lua:8418 | fix | accepted | 是 | losgoroth 为本仓已有实体专名「洛斯格罗斯」（mod-tome.lua:8416），泛译「虚空生物」丢失专名。mana 译「魔力」与同节一致。 |
| hrq-00097 | entry-00752 | mod-tome.lua:8515 | fix | accepted | 是 | 「两只巨大的双手」量词重复且身体意象错误；蛇尾本是支撑身体的下身而非「在腿部长着」。 |
| hrq-00098 | entry-00763 | mod-tome.lua:8718 | fix | accepted | 是 | torn away from 译为「赶出来」改变语义；home world 译「老家」漏 world 且语域不合。 |
| hrq-00099 | entry-00768 | mod-tome.lua:8734 | fix | accepted | 是 | serviceable condition 的核心是仍然可用，译「值得信赖」语义漂移。 |
| hrq-00100 | entry-00780 | mod-tome.lua:8953 | no_change | accepted | 否 | humanoid 为 entity type，散文自由描述用「类人生物」与同批「人形生物」并存不构成缺陷。不改。 |
| hrq-00101 | entry-00781 | mod-tome.lua:8969 | fix | accepted | 是 | brothers and sisters 被概括为「集体行动」，且后半句由单数改复数；源码 make_escort 配置要求生成护卫。 |
| hrq-00102 | entry-00804 | mod-tome.lua:9191 | fix | deferred | 是 | 实体名已为「腐烂泰坦」（mod-tome.lua:39335），本描述用「腐化泰坦」不一致。该 NPC 实体名条目不在本批冻结集合，单改制造不一致，故 defer。 |
| hrq-00103 | entry-00805 | mod-tome.lua:9194 | fix | accepted | 是 | 漏 other（其他生物）；within radius %d 被误作名词修饰。 |
| hrq-00104 | entry-00820 | mod-tome.lua:9332 | fix | accepted | 是 | 「深渊咆哮的存在」为无据增译；corruption and power 被合并为「腐蚀力量」；blackened 译「被玷污」有误。 |
| hrq-00105 | entry-00840 | mod-tome.lua:9487 | fix | accepted | 是 | 同族统一为「一瓶<颜色>液体」（mod-tome.lua:9450/9456/9461/9466），本条「黄色液体小瓶」句式不一致，改齐。 |
| hrq-00106 | entry-00843 | mod-tome.lua:9495 | no_change | accepted | 否 | 日志已表达核心技能能力提升，未改机制，advisory，不改。 |
| hrq-00107 | entry-00852 | mod-tome.lua:9627 | fix | accepted | 是 | 同 ego「抓握之/抓握」与本日志「抓取藤蔓」用词不一致，改齐。 |
| hrq-00108 | entry-00866 | mod-tome.lua:9858 | fix | accepted | 是 | 同一 ego 的 entity name「振奋的」与 entity keyword「疗愈」两套译法割裂。按 ego 名称语境统一。 |
| hrq-00109 | entry-00873 | mod-tome.lua:9973 | fix | accepted | 是 | 披风 ego 同样存在「振奋的/疗愈」割裂。 |
| hrq-00110 | entry-00881 | mod-tome.lua:10051 | refuted | accepted | 否 | naturalist's 与 natural 是不同源串；本条「自然」非专名，不要求与 naturalist's 字面同译，术语条目亦允许 entity keyword 另译。refuted 主张成立，不改。 |
| hrq-00111 | entry-00899 | mod-tome.lua:10488 | no_change | accepted | 否 | conjuration 词族现译内部一致，源码无改称「咒术师」的机制依据；「魔术师」为既有选择。advisory，不改。 |
| hrq-00112 | entry-00914 | mod-tome.lua:10798 | refuted | accepted | 否 | 固定源码本条即为感叹号，Gemini 行号不准但结论不影响；「应改句号」主张不成立。不改。 |
| hrq-00113 | entry-00918 | mod-tome.lua:10816 | no_change | accepted | 否 | 与 00899/00900/00919 同词族一致；缺术语或源码证据支持单条改名。advisory，不改。 |
| hrq-00114 | entry-00972 | mod-tome.lua:11460 | no_change | accepted | 否 | Artelia 无术语条目、无官方读音，不能仅凭音节断言「亚特莱」有误。advisory，不改。 |
| hrq-00115 | entry-00980 | mod-tome.lua:11596 | fix | accepted | 是 | 「变的暗淡」应为「变得暗淡」，属语法错误。 |
| hrq-00116 | entry-00984 | mod-tome.lua:11658 | fix | accepted | 是 | 增译「如果你想保留物品」的目的条件，改变原意。 |
| hrq-00117 | entry-00992 | mod-tome.lua:12145 | fix | accepted | 是 | 原译括号提前闭合，把「十回合」与能力清单割裂；cut 按实际效果应作「流血」（combat.tsv:54）。重译保留全部占位符与格式码。 |
| hrq-00118 | entry-00997 | mod-tome.lua:12286 | fix | accepted | 是 | 「不断的向下滴血」应为「不断地」。 |
| hrq-00119 | entry-01000 | mod-tome.lua:12326 | fix | accepted | 是 | 「基于魔法」应作「基于魔力」（Magic stat，combat.tsv:120）。 |
| hrq-00120 | entry-01001 | mod-tome.lua:12335 | fix | accepted | 是 | 「（基于魔法）伤害半径 %d」缺标点连跑；同时修正属性专名为「魔力」。 |
| hrq-00121 | entry-01002 | mod-tome.lua:12357 | fix | accepted | 是 | grand 漏译；「7把」数字格式属静态排版，不改。 |
| hrq-00122 | entry-01029 | mod-tome.lua:12548 | fix | accepted | 是 | pull 是拉扯而非抓取（grab）；与前一条日志用词冲突。 |
| hrq-00123 | entry-01032 | mod-tome.lua:12552 | fix | accepted | 是 | wound 为物品实际筛选的效果子类型；术语 wound→创伤（combat.tsv:74）。 |
| hrq-00124 | entry-01038 | mod-tome.lua:12614 | fix | accepted | 是 | 首句主语错置（达克顿打造臂铠而非时代）；unparalleled 被弱化为「强大的」；these 误作「那些」。 |
| hrq-00125 | entry-01068 | mod-tome.lua:12825 | fix | accepted | 是 | 第三个 %s 是物主代词而非敌人数量，属运行时可见的语义错误。 |
| hrq-00126 | entry-01074 | mod-tome.lua:12857 | fix | accepted | 是 | 占位符与颜色标记完整；「放出了被束缚的灵魂」与 tap 的机制语义有偏差。 |
| hrq-00127 | entry-01081 | mod-tome.lua:12872 | fix | accepted | 是 | 漏 once brilliant；decayed 的腐朽语义被泛化为「破旧」；heavily 程度未显著削弱，该 refuted 主张成立。 |
| hrq-00128 | entry-01085 | mod-tome.lua:12879 | fix | accepted | 是 | cone 应与同批「锥形范围」一致；「至多两项」为译文额外添加信息，该 refuted 主张不成立，一并修正。 |
| hrq-00129 | entry-01096 | mod-tome.lua:12927 | fix | accepted | 是 | charge 译「当前增幅」有机制歧义；括号空格属静态排版不改。 |
| hrq-00130 | entry-01116 | mod-tome.lua:13089 | fix | accepted | 是 | 漏 when it proved necessary。 |
| hrq-00131 | entry-01120 | mod-tome.lua:13125 | fix | accepted | 是 | light/darkness 伤害类型应作「光系/暗影」（mod-tome.lua:6886/6893）；Magic 应作「魔力」。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
