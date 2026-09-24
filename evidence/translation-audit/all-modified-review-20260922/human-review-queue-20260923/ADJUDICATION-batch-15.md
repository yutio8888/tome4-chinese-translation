# 批阅裁决台账 — batch-15

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`e23cf3f3f07e9b4a4c5b8855c06019083aef2fffe990284f653e6a70909853c1`
- 决策行：30；冻结修订（含孪生载体）：25
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 24 |
| deferred | 1 |

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
| hrq-00572 | entry-04019 | tome-orcs.lua:6320 | fix | accepted | 是 | 独立核验通过；“爆炸状态”和 2 码伤害虽提示范围攻击，却没有说明命中目标才爆炸及爆点；冻结 Archery.lua 在命中坐标触发爆炸，补明触发与中心。Orcs DLC 来源未固定。 |
| hrq-00573 | entry-04022 | tome-orcs.lua:6348 | refuted | accepted | 否 | 驳回模型主张；英文 frost aura 与“烈火光环”字面不符，但 FIERY_SALVE 效果及火焰、光系、闪电亲和，与相邻道具 fiery aura 一致；现译纠正了上游误写，无需改。Orcs DLC 来源未固定。 |
| hrq-00574 | entry-04023 | tome-orcs.lua:6354 | refuted | accepted | 否 | 驳回模型主张；英文 frost aura 与“静水光环”字面不符，但 WATER_SALVE 效果和相邻道具 water aura 均支持静水；现译符合效果身份。Orcs DLC 来源未固定。 |
| hrq-00575 | entry-04028 | tome-orcs.lua:6404 | no_change | accepted | 否 | 无需修改；“主人”可由战斗语境理解为飞锯的施加者；冻结源码将飞回方向指向 eff.src，并未译反。“施加者”更精确但属措辞澄清。Orcs DLC 来源未固定。 |
| hrq-00576 | entry-04035 | tome-orcs.lua:6445 | fix | accepted | 是 | 独立核验通过；前句抛起蒸汽枪能补足下落背景，却不能表达 somehow 的意外感；现句也省略落下动作，补出两处叙事信息。Orcs DLC 来源未固定。 |
| hrq-00577 | entry-04046 | tome-orcs.lua:6500 | no_change | accepted | 否 | 无需修改；“忍受痛苦，不能集中精力制造伤害”已表达受苦导致输出受限；“遭受”“造成”较自然，属于二级措辞建议。Orcs DLC 来源未固定。 |
| hrq-00578 | entry-04047 | tome-orcs.lua:6515 | no_change | accepted | 否 | 无需修改；闪电之网“覆盖”可作环绕式防护理解，所有伤害减免数值已保留；crackling 的声响属风味描写润色，尚不足以重开。Orcs DLC 来源未固定。 |
| hrq-00579 | entry-04049 | tome-orcs.lua:6525 | no_change | accepted | 否 | 无需修改；“力量强化”已表达力量增强，与解除提示相承；涌动感的取舍是措辞建议。Orcs DLC 来源未固定。 |
| hrq-00580 | entry-04053 | tome-orcs.lua:6557 | no_change | accepted | 否 | 无需修改；“打击”保留攻击者、目标及颜色标记；strikes down at 的力度可润色，但冻结源码仅表明自动攻击，不能据此强制写空间方向。Orcs DLC 来源未固定。 |
| hrq-00581 | entry-04054 | tome-orcs.lua:6568 | no_change | accepted | 否 | 无需修改；“被困在其中”可作处在毒云中的叙事用语；冻结效果仅见范围施加而不见定身，现译可能引起歧义但尚无充分证据证明玩家会读为无法离开。Orcs DLC 来源未固定。 |
| hrq-00582 | entry-04055 | tome-orcs.lua:6572 | no_change | accepted | 否 | 无需修改；中文多出的武器类型与每回合第一次限定有 callbackOnHit 的 weapon_type 和 turn_procs.miasma 条件支持；未穷尽全部攻击消费路径，故不采纳绝对的“100%吻合”说法。Orcs DLC 来源未固定。 |
| hrq-00583 | entry-04056 | tome-orcs.lua:6574 | refuted | accepted | 否 | 驳回模型主张；英文说每回合发射，但冻结效果赋予 Rocket Barrage，技能可手动再次发射，使用其他技能则结束效果；现译与消费机制吻合，差异来自英文概述。Orcs DLC 来源未固定。 |
| hrq-00584 | entry-04066 | tome-orcs.lua:6777 | no_change | accepted | 否 | 无需修改；药剂与“你身上”“需通过注射器使用”连读时，获得光环者仍是使用者；改为“使你获得”更清楚，但尚非机制错译。所引源码描述在 55–56 行而非模型所称 51–53 行。Orcs DLC 来源未固定。 |
| hrq-00585 | entry-04088 | tome-orcs.lua:7456 | no_change | accepted | 否 | 无需修改；英文 Amulet 是护符，但物品名含 Light of God，“神的光辉”可借代护符之光；没有把施法主体确定为神的充分依据。Orcs DLC 来源未固定。 |
| hrq-00586 | entry-04092 | tome-orcs.lua:7901 | fix | accepted | 是 | 独立核验通过；“毁灭敌人”概括伤害，却未表达 damage and debilitate 并列的削弱作用；职业特性列表需要保留两项作用。Orcs DLC 来源未固定。 |
| hrq-00587 | entry-04101 | tome-orcs.lua:8071 | fix | accepted | 是 | 独立核验通过；“无处遁形”可修辞性表达难敌枪法，却没有保留 weaken 的削弱效果；只补“削弱敌人”，不采用缺乏证据的“降低枪击抗性”窄化解释。Orcs DLC 来源未固定。 |
| hrq-00588 | entry-04106 | tome-orcs.lua:8143 | no_change | accepted | 否 | 无需修改；“实验的工匠”在称号语境可理解为做实验的工匠；事件叙述证实其正在试验，改“进行实验的”仅使语法更顺。Orcs DLC 来源未固定。 |
| hrq-00589 | entry-04109 | tome-orcs.lua:8177 | no_change | accepted | 否 | 无需修改；“创造插件”已表达制作完成的结果；“制作”更贴切但只是措辞。“tinker→蒸汽工具”是 existing 且为实体类型，不强制覆盖本日志的“插件”。Orcs DLC 来源未固定。 |
| hrq-00590 | entry-04110 | tome-orcs.lua:8178 | no_change | accepted | 否 | 无需修改；此系统的配方与随后显示的名称已让 tinker 限定可从语境恢复；补“插件”可更明晰，但“配方”符合 preferred schematic 条目，未构成确认漏义。Orcs DLC 来源未固定。 |
| hrq-00591 | entry-04115 | tome-orcs.lua:8341 | defer | deferred | 否 | C03：This IS relevant 与“无关紧要”相反，须改肯定；C04：Neither 承接前句两派，“我们”错置主体；C05：filthy 非“狡猾”；N01：profane 在记录中指粗俗发言，非宗教“亵渎”。C06：“这决定了”在议会语境仍可理解为决议，属文体建议；N02：“在辞职时”可宽泛指辞职过程，仅建议澄清。最强范围反证是 tome-orcs.lua:2757 另有同一议会文本的运行时载体，英文键仅空格不同：C03  |
| hrq-00597 | entry-04116 | tome-possessors.lua:5 | fix | accepted | 是 | 独立核验通过；“你自己的被诅咒的影子”可泛指遭诅咒的分身，但固定本体源码命名 Doomed Shade of %s，现有 Doomed 职业译名为“末日使者”；“使用比尔的身体”也易误把比尔当成被使用的工具，按附身视角明确。该本体实体证据只支持名称，不证明 Possessors 成就触发机制；Possessors DLC 来源未固定。 |
| hrq-00598 | entry-04123 | tome-possessors.lua:56 | no_change | accepted | 否 | 无需修改；“目标”在反击句中可承接造成该次伤害的攻击者，未证明错误指向；明确写“伤害来源”会更清楚，属于指代澄清。Possessors DLC 来源未固定，未据未固定源码断言运行行为。 |
| hrq-00599 | entry-04129 | tome-possessors.lua:119 | fix | accepted | 是 | 独立核验通过；“直线冲锋”暗示沿线移动，却未交代首个生物身后的所有生物也受招；后句单数“目标”亦未承接 targets 复数。补出沿线对象及复数指代，仅依据冻结英汉文本，不宣称核实 Possessors 运行机制；DLC 来源未固定。 |
| hrq-00600 | entry-04137 | tome-possessors.lua:270 | no_change | accepted | 否 | 无需修改；“射出一道冲击波”保留向敌人施加力量的动作，后续伤害、上限和吸收条件也齐全；ghastly finger 与命其死去的意象是风味描写建议，未证明机制失义。Possessors DLC 来源未固定。 |
| hrq-00601 | entry-04141 | tome-possessors.lua:356 | fix | accepted | 是 | 独立核验通过；“分享痛苦”可表示传递，却无根据地写成“自己的”，与下一句敌人专注于他们自己的痛苦冲突；移除所有格并保留施加动作。仅依冻结英汉文本判定，不宣称核实 Possessors 运行机制；DLC 来源未固定。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
