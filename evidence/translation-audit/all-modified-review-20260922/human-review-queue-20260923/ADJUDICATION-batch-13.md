# 批阅裁决台账 — batch-13

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`5581d7db222219432fdde0339727e90884985db23437d75cf03801899850f595`
- 决策行：40；冻结修订（含孪生载体）：27
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 27 |

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
| hrq-00492 | entry-03815 | tome-orcs.lua:1613 | fix | accepted | 是 | 独立核验通过；hrq-00492：单说“第三下攻击”或可理解为周期中的第三下，但既未明确每轮重复，也把命中写成攻击；冻结兽人源码命中后计数并清零，支持周期性修正。hrq-00493：原英文称当次命中必暴击，但冻结兽人源码在命中处理后才设置 physcrit，固定引擎射击流程先判定暴击；因此依源码写明下一次攻击获 100% 物理暴击率，不沿用模型所称当次必暴击。兽人 DLC 来源未固定。 |
| hrq-00494 | entry-03823 | tome-orcs.lua:1740 | fix | accepted | 是 | 独立核验通过；hrq-00494：后句已保留流血意象，是最强反证；但 spilt 是倾洒而非“分离”，首句仍反转动作，故修正并保留原有换行。兽人 DLC 来源未固定。 |
| hrq-00495 | entry-03827 | tome-orcs.lua:1791 | no_change | accepted | 否 | 无需修改；hrq-00495：“怎么用”在口语中也能泛指这副护目镜如何起作用；虽然“怎么运作”更贴近漆黑护目镜的讶异语气，现译未被证实失义，仅记表达建议。兽人 DLC 来源未固定。 |
| hrq-00496 | entry-03845 | tome-orcs.lua:2041 | no_change | accepted | 否 | 无需修改；hrq-00496：“全身心信任”仍承载托付安危的语境，“伸出援手”也保留劝购作用；well-being 与 If nothing else 的字面精度可提升，但目前是二级表达建议，不改长文。兽人 DLC 来源未固定。 |
| hrq-00497 | entry-03849 | tome-orcs.lua:2195 | fix | accepted | 是 | 独立核验通过；hrq-00497：“第一个”可勉强指最先可搭的门，但“这个大陆上的”让它变成大陆内编号；those tinies 又被改成第二人称“你们”，与巨人逃离大陆的第三人称蔑称不等价，故修正。兽人 DLC 来源未固定。 |
| hrq-00498 | entry-03851 | tome-orcs.lua:2218 | fix | accepted | 是 | 独立核验通过；hrq-00498：“合作部队”可宽读为联合力量，但 join forces with 的动作主体是食人魔及派遣他们的永恒精灵，原译误造出一支部队，故改为携手合作。兽人 DLC 来源未固定。 |
| hrq-00499 | entry-03852 | tome-orcs.lua:2523 | fix | accepted | 是 | 独立核验通过；hrq-00499：“在那场异常中牺牲”可暗示致死关系，但 expensive combatants 不是精英卫兵，且 at the hands of 把库马纳及这些战斗人员的死亡都归于 Anomaly；据原句修正，不臆定 Anomaly 的实体性质。兽人 DLC 来源未固定。 |
| hrq-00500 | entry-03853 | tome-orcs.lua:2545 | fix | accepted | 是 | 独立核验通过；hrq-00500：前文“你不是唯一一个买奴隶的人”足以提示其他买家，是最强反证；但随后“你想”明确把第三方买家的要求误归收信人，故修正主语。兽人 DLC 来源未固定。 |
| hrq-00501 | entry-03854 | tome-orcs.lua:2559 | fix | accepted | 是 | 独立核验通过；hrq-00501：原句“为了莱娜尼尔的爱”可作感叹语宽读，但不自然；“使用奴隶的安全设施”把奴隶受益的安全安排改为使用奴隶的设施。accommodations 不限于食宿，故不采用模型的食宿断言。hrq-00502：“大力药”自然指增力药，与 extra-strength medicine 的强效药不等价；三处一并修正。兽人 DLC 来源未固定。 |
| hrq-00503 | entry-03856 | tome-orcs.lua:2625 | fix | accepted | 是 | 独立核验通过；hrq-00503：薄雾句可让人推知排气不明显，但随后“封闭或扩张它们”所指是毛孔及通风口；careless intervention 是轻率介入而非发明。IMMOLATUS 无当前术语条目或官方读音，既有译名不据模型臆改；两处可证实的动作与指代错误已修。兽人 DLC 来源未固定。 |
| hrq-00504 | entry-03860 | tome-orcs.lua:2690 | fix | accepted | 是 | 独立核验通过；hrq-00504：“推出”可以宽读成提出候选，但紧接桌面游戏会误作发布，而原文是正式支持，故修正。hrq-00505：团长与队长都能指指挥官，仍是同篇同一职位，趁修改统一。hrq-00506：“精神上的技能”承接远见、急智等例子，尚可理解为心智能力，纯表达建议不另改。hrq-00507：“使用后”给不超过一个月的释放期限增添了原文未定的起点，故删除。兽人 DLC 来源未固定。 |
| hrq-00508 | entry-03861 | tome-orcs.lua:2708 | no_change | accepted | 否 | 无需修改；复核发现原拟修改会删除 [b]...[/b] markup，违反本批「禁止改 markup」不变量，已撤回该改动并把本条记为 no_change（保留冻结原值与 markup）。另：正文标点与措辞无一级缺陷。 |
| hrq-00510 | entry-03864 | tome-orcs.lua:2808 | fix | accepted | 是 | 独立核验通过；hrq-00510：争吵时“抱怨”可含指责，但紧接“这是你的错”明确在争事故责任，故两处改为指责。hrq-00511：官方调查已通过是最强反证，但 the first order of business at the next session 明确是下次会议的首项议程，非调查第一部分。hrq-00512：原译仍有不愿介入之意，但 As far as I am concerned 与 responsibility 分别是个人立场和责任归属 |
| hrq-00513 | entry-03865 | tome-orcs.lua:2874 | fix | accepted | 是 | 独立核验通过；hrq-00513：“毁天灭地”有夸张喊名效果，但同一武器专名 DESTRUCTICUS 的 preferred DLC 译名明确为“毁灭号”，故采用。hrq-00514：“不准”可口语化指不灵，却像准确性问题，原句是隐形不足以瞒过兽人，故修正。hrq-00515：dispose of 可泛指解决威胁，原文未确定灭绝方式，保留“赶走”。hrq-00516：多把钥匙不能使单数 it 变成多把武器，故改为那件武器。兽人 DLC 来源未固定。 |
| hrq-00517 | entry-03871 | tome-orcs.lua:3307 | refuted | accepted | 否 | 驳回模型主张；hrq-00517：完整专名 High Sun Paladin Aeryn 的 preferred 记录限定 core 与完整头衔；本句为兽人 DLC 的 our High Paladin，现译“至高太阳骑士”词义可通，模型的术语违规主张被适用范围反驳。兽人 DLC 来源未固定。 |
| hrq-00518 | entry-03875 | tome-orcs.lua:3579 | fix | accepted | 是 | 独立核验通过；hrq-00518：钩子意象或使“拔起”像拔钩，但 lift them up 的 them 指维西一族，与现实被拖入深渊相对，原译反转为拔除，故改托起；同时修正“在你过来时前”的错序。hrq-00519：同篇敌视背景可补足宇宙想忘却的意味，“宇宙也忘不了”未证实失义，维持不动。兽人 DLC 来源未固定。 |
| hrq-00520 | entry-03883 | tome-orcs.lua:3893 | no_change | accepted | 否 | 无需修改；hrq-00520：trained 虽未落在本句，但同节任务与使用动作已交代雪人受训；“来协助你”也承接召到身边的用途，仅属独立说明精度建议。兽人 DLC 来源未固定。 |
| hrq-00521 | entry-03890 | tome-orcs.lua:3965 | fix | accepted | 是 | 独立核验通过；hrq-00521：“持续能量”在维持技能语境中可被理解，机制含义未确定错误；但“算向最大值”生硬且数值后英文句点是明确标点错误，改为维持技能占用能量计入上限并改中文句号。兽人 DLC 来源未固定。 |
| hrq-00522 | entry-03892 | tome-orcs.lua:3977 | fix | accepted | 是 | 独立核验通过；hrq-00522：“地块”可提示效果位置，但“创造一个地块”明确把 at the target tile 当作创造对象，漏掉 distortion；“改变方向”又漏掉 face away，故两处修正。兽人 DLC 来源未固定。 |
| hrq-00523 | entry-03912 | tome-orcs.lua:4559 | fix | accepted | 是 | 独立核验通过；hrq-00523：“持续 4 回合”可同时修饰伤害和沉默，但未说明 %0.2f 是每回合伤害；冻结兽人源码的效果按回合造成 eff.power 伤害，故补明频率。兽人 DLC 来源未固定。 |
| hrq-00524 | entry-03913 | tome-orcs.lua:4573 | fix | accepted | 是 | 独立核验通过；hrq-00524：“恢复 %d%% 蒸汽值”通常可按上限比例理解，不单凭省略判一级错；但原文与冻结源码都明确按最大蒸汽值计算，趁修正斜体句中重复叹号的标点错误，一并写清上限。兽人 DLC 来源未固定。 |
| hrq-00525 | entry-03918 | tome-orcs.lua:4796 | fix | accepted | 是 | 独立核验通过；hrq-00525：“无尽地痛苦”仍能让人理解痛苦无尽，但“地”用字错误且原文是带感叹号的完整陈述句，按明确的错字及句末标点规则修正。兽人 DLC 来源未固定。 |
| hrq-00526 | entry-03921 | tome-orcs.lua:4930 | fix | accepted | 是 | 独立核验通过；hrq-00526：周围敌人确能让角色兴奋，是最强语境反证；但 thrill of the hunt 是狩猎者的快感，不是被猎杀的危险，现译反转动作视角，故修正。兽人 DLC 来源未固定。 |
| hrq-00527 | entry-03924 | tome-orcs.lua:4969 | fix | accepted | 是 | 独立核验通过；hrq-00527：本句属性加成已正确，不需要调整；但前句把“冒险有时是技艺所需、你的风险经过更多计算”误作经历更多危险和计算力超凡，故按原文修正。兽人 DLC 来源未固定。 |
| hrq-00528 | entry-03925 | tome-orcs.lua:4985 | fix | accepted | 是 | 独立核验通过；hrq-00528：相邻熔炉技能可提示关联，但本说明单看像常驻减伤；原文 While Furnace is on 与冻结兽人源码的激活检查均限定熔炉开启，故补明条件。兽人 DLC 来源未固定。 |
| hrq-00529 | entry-03926 | tome-orcs.lua:5007 | fix | accepted | 是 | 独立核验通过；hrq-00529：“只是”保留轻描淡写语气，但 flesh burn 指局部皮肉烫伤，现译成肉体正在燃烧；趁修机制数字一并修正风味。hrq-00530：%d 是最多可驱散的状态数，原译写成固定驱散 %d 个；冻结兽人源码把它作为移除上限，故补“最多”。兽人 DLC 来源未固定。 |
| hrq-00531 | entry-03931 | tome-orcs.lua:5089 | fix | accepted | 是 | 独立核验通过；hrq-00531：“在移动中射击”总述可暗示两动作相连，但未写定身时不可移动，也把扫射次数误作消耗弹药数；冻结兽人源码使用 turns 与弹药容量确定装填数，并检查移动限制。双持蒸汽枪可由相邻提示推知，仍在本说明补明；同时纠正只有移动时才需比较移动速度的条件。兽人 DLC 来源未固定。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
