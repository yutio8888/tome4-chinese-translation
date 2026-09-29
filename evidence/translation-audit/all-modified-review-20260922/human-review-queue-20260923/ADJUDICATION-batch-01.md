# 批阅裁决台账 — batch-01

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`181a8ecbd88da134a8318f740770ad0016a1c6f7cf0d0e8dd79060aa6a242470`
- 决策行：40；冻结修订（含孪生载体）：50
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 35 |
| accepted_policy | 13 |
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
| hrq-00012 | entry-00105 | engine.lua:1697 | fix | accepted | 是 | 首行缺句末标点成立；两处捐助者违反 preferred Donator→捐赠者。 |
| hrq-00013 | entry-00110 | engine.lua:1779 | fix | accepted | 是 | Maj'Eyal 有 preferred 条目（马基·埃亚尔），无反证。 |
| hrq-00013 | entry-00144 | mod-boot.lua:364 | fix | accepted | 是 | 孪生载体，应用 hrq-00013 已接受决策；改后与主载体逐字节一致。 |
| hrq-00014 | entry-00111 | engine.lua:1800 | fix | accepted | 是 | Scourge from the West 与 Psyshot 均有术语条目，模型所称 DLC 一致性不作依据。 |
| hrq-00014 | entry-00145 | mod-boot.lua:385 | fix | accepted | 是 | 孪生载体，应用 hrq-00014 已接受决策；改后与主载体逐字节一致。 |
| hrq-00015 | entry-00112 | engine.lua:1823 | fix | accepted_policy | 是 | 仅落实 bracket_fullwidth；扭动者/彼世之门属未授权术语决定，保留。 |
| hrq-00015 | entry-00146 | mod-boot.lua:408 | fix | accepted | 是 | 孪生载体，应用 hrq-00015 的 bracket_fullwidth 决策；改后与主载体逐字节一致。 |
| hrq-00016 | entry-00139 | mod-boot.lua:282 | fix | accepted | 是 | 与 entry-00105 同源同文本的 boot 载体，同改避免分歧。 |
| hrq-00017 | entry-00164 | mod-tome.lua:103 | fix | accepted | 是 | 组内半角分号与同组全角不一致，属标点修正。 |
| hrq-00018 | entry-00165 | mod-tome.lua:104 | fix | accepted | 是 | 同上；技能树译法无 preferred 冲突，不改。 |
| hrq-00019 | entry-00166 | mod-tome.lua:105 | fix | accepted | 是 | 同上。 |
| hrq-00020 | entry-00184 | mod-tome.lua:225 | defer | deferred | 否 | 主工作区 HEAD 11b3e963 已修（恢复空行、勇敢地、去增译）；本 worktree 不改，待合并。 |
| hrq-00021 | entry-00185 | mod-tome.lua:232 | no_change | accepted | 否 | 方括号内空格属纯静态排版，按用户策略不算缺陷；不改。 |
| hrq-00022 | entry-00191 | mod-tome.lua:249 | fix | accepted | 是 | 固定源码 Actor.lua:4530 为 space-time，漏译时间维度属实。 |
| hrq-00023 | entry-00195 | mod-tome.lua:277 | fix | accepted | 是 | 源码 Actor.lua:5857 参数为资源名与技能名；原译冒号割裂动宾，语序缺陷成立。 |
| hrq-00024 | entry-00198 | mod-tome.lua:353 | fix | accepted | 是 | 已核母句 Actor.lua:7805 logCombat 拼接，缺停顿属实；片段首加逗号修好拼接。 |
| hrq-00025 | entry-00216 | mod-tome.lua:403 | defer | deferred | 否 | 术语库 Defiler=堕落系（existing）；人物称谓名词化无 preferred，属未授权术语决定。 |
| hrq-00026 | entry-00221 | mod-tome.lua:469 | no_change | accepted | 否 | 源码 Game.lua:926-936 分列 level 与 zone；原译未区分，但统一译法属跨条目策略，本条不改。 |
| hrq-00027 | entry-00223 | mod-tome.lua:471 | no_change | accepted | 否 | 源码确认由 EFF_PARADOX_CLONE 触发、不限楼梯；离开地图功能含义正确。 |
| hrq-00028 | entry-00226 | mod-tome.lua:501 | fix | accepted_policy | 是 | 击杀仅偏好差异不改；括号全角化落实 bracket_fullwidth。 |
| hrq-00029 | entry-00231 | mod-tome.lua:510 | fix | accepted | 是 | 已核 Map.lua:1508-1518 compassDirection 返回 _t(dir)，engine.lua 译北面；%s方 与重复感叹号属实。 |
| hrq-00030 | entry-00244 | mod-tome.lua:674 | refuted | accepted | 否 | 源码 MapEffects.lua:23 直接字符串拼接，前导空格会被中文吸收；补空格反而错误。 |
| hrq-00031 | entry-00247 | mod-tome.lua:719 | fix | accepted | 是 | 同一串内首个半角逗号与第二个全角逗号不一致，属标点修正。 |
| hrq-00032 | entry-00254 | mod-tome.lua:737 | no_change | accepted | 否 | 括号已全角，仅数字前空格差异，属静态排版，不改。 |
| hrq-00033 | entry-00284 | mod-tome.lua:986 | fix | accepted_policy | 是 | 语序偏紧为 advisory 不改；括号全角化落实 bracket_fullwidth。 |
| hrq-00034 | entry-00286 | mod-tome.lua:988 | fix | accepted_policy | 是 | 已核 Object.lua:2167 由 is_mind 判定，精神正确；括号全角化落实策略。 |
| hrq-00035 | entry-00288 | mod-tome.lua:1031 | fix | accepted | 是 | 已核 Object.lua:2305-2307 追加 _t"."；去掉串尾句号消除 。. 重复，残留西文句点属未冻结条目。 |
| hrq-00036 | entry-00298 | mod-tome.lua:1115 | fix | accepted | 是 | 已核 Object.lua:196-200 forbid_arcane 路径；原译引入技能并把物品当被拦对象，属误译。 |
| hrq-00037 | entry-00299 | mod-tome.lua:1116 | fix | accepted | 是 | 同上，且本条为活动 tformat 载体。 |
| hrq-00038 | entry-00318 | mod-tome.lua:1223 | fix | accepted | 是 | 已核 Trap.lua:271-288 片段已含「了」；去掉模板「了」后 ignore→你无视一个陷阱 仍通顺。 |
| hrq-00039 | entry-00334 | mod-tome.lua:1295 | no_change | accepted | 否 | on_die 触发与「杀死」一致，击败仅为偏好，不改。 |
| hrq-00040 | entry-00344 | mod-tome.lua:1379 | fix | accepted | 是 | 已核 Combat.lua:466 用 his_her；engine.lua 译他的/它的，删占位符后「的」修好叠词。 |
| hrq-00041 | entry-00345 | mod-tome.lua:1380 | no_change | accepted | 否 | 双持条无叠词、招架语义保留，偏斜仅文风建议，不改。 |
| hrq-00042 | entry-00354 | mod-tome.lua:1428 | fix | accepted_policy | 是 | 占位符与机制正确；括号全角化落实 bracket_fullwidth。 |
| hrq-00043 | entry-00368 | mod-tome.lua:1579 | fix | accepted | 是 | 原文指失衡值状态与施法难易，原译说成「能力」与越接近 0 越平衡相反，方向性错误成立。 |
| hrq-00044 | entry-00373 | mod-tome.lua:1689 | fix | accepted | 是 | 原文为 the user（技能使用者，含 NPC），原译改成「玩家」改变对象，属实。 |
| hrq-00045 | entry-00374 | mod-tome.lua:1772 | fix | accepted | 是 | 术语库 Magic=魔力（stat name）；属性提示标题须用属性名，改魔力。 |
| hrq-00046 | entry-00393 | mod-tome.lua:2281 | no_change | accepted_policy | 否 | 已为全角括号，符合 bracket_fullwidth；不改。 |
| hrq-00046 | entry-00394 | mod-tome.lua:2282 | no_change | accepted_policy | 否 | 已为全角括号，符合 bracket_fullwidth；不改。 |
| hrq-00046 | entry-00395 | mod-tome.lua:2283 | fix | accepted_policy | 是 | 外层半角括号，按 bracket_fullwidth 全角化。 |
| hrq-00046 | entry-00396 | mod-tome.lua:2284 | fix | accepted_policy | 是 | 同 hrq-00046 决策行；外层半角括号全角化。 |
| hrq-00046 | entry-00397 | mod-tome.lua:2285 | fix | accepted_policy | 是 | 同 hrq-00046 决策行；外层半角括号全角化。 |
| hrq-00046 | entry-00398 | mod-tome.lua:2286 | fix | accepted_policy | 是 | 同 hrq-00046 决策行；外层半角括号全角化。 |
| hrq-00046 | entry-00399 | mod-tome.lua:2287 | fix | accepted_policy | 是 | 同 hrq-00046 决策行；外层半角括号全角化。 |
| hrq-00046 | entry-00400 | mod-tome.lua:2288 | fix | accepted_policy | 是 | 同 hrq-00046 决策行；外层半角括号全角化。 |
| hrq-00047 | entry-00419 | mod-tome.lua:2646 | no_change | accepted | 否 | 数值与含义正确，空格差异属静态排版，不改。 |
| hrq-00048 | entry-00423 | mod-tome.lua:2694 | fix | accepted | 是 | 已核 kills.lua:265-275 AVOID_DEATH 绑定 life-saving talent；原译泛化为任意技能，completeness 缺陷成立。 |
| hrq-00049 | entry-00428 | mod-tome.lua:2784 | no_change | accepted | 否 | 条件与数量正确，句式不平行仅 advisory，不改。 |
| hrq-00050 | entry-00429 | mod-tome.lua:2788 | fix | accepted | 是 | Maj'Eyal 有 preferred 条目；旧大陆把专名泛化，属实。 |
| hrq-00051 | entry-00434 | mod-tome.lua:2804 | no_change | accepted | 否 | 任务名 Lost Knowledge 与本仓 mod-tome.lua 既有译名一致；增补有助于检索，不改。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
