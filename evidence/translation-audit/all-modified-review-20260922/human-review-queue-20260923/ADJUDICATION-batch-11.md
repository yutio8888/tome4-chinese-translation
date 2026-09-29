# 批阅裁决台账 — batch-11

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`4bfd535961e783822d07158f14251fe671f5070edf339abcafc5f8756e20ec3d`
- 决策行：40；冻结修订（含孪生载体）：40
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 39 |
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
| hrq-00412 | entry-02559 | mod-tome.lua:34096 | no_change | accepted | 否 | 无需修改；后段已明确“特殊能力”由正能量驱动，前段增补并未造成错误；晨曦之门和正能量沿用仓内译名，后者有 preferred 记录。 |
| hrq-00413 | entry-02565 | mod-tome.lua:34230 | fix | accepted | 是 | 独立核验通过；原文 noble 带引号，现译首个右引号确属标点错误；“黑暗的时代／混乱的时代”重复只是文风。Age of Pyre 在本仓及 preferred 术语中为烈火纪，故不能据被撤回主张改作派尔纪元。 |
| hrq-00414 | entry-02568 | mod-tome.lua:34302 | no_change | accepted | 否 | 无需修改；颜色码完整，码后空格属纯静态排版；列表句末标点可统一但属二级语法意见。自始以来属文风。固定仓内 Hurricane 技能名为飓风，眩晕亦保留原句 daze 的控制含义，撤回的风暴之怒主张不成立。 |
| hrq-00415 | entry-02570 | mod-tome.lua:34330 | fix | accepted | 是 | 独立核验通过；原文末项明确为 3-wide beam，现译末句遗漏射线这一中心词；其余法术、技能及觉醒技译名沿用本仓，boss 英文留存属低影响本地化意见。 |
| hrq-00416 | entry-02576 | mod-tome.lua:34475 | no_change | accepted | 否 | 无需修改；完整段落中梦境既是织梦者的信念也是力量来源，末段复述未新增原文不支持的机制；灵能转化与资源回复保留。无冒号及列表末句标点差异不影响语义，属二级意见。 |
| hrq-00417 | entry-02579 | mod-tome.lua:34541 | no_change | accepted | 否 | 无需修改；颜色标记、职业特征、体力资源与解锁句均完整；Class features 独立成行只改变排版，解锁句不用冒号仍是成立的中文句子。 |
| hrq-00418 | entry-02586 | mod-tome.lua:34673 | no_change | accepted | 否 | 无需修改；原文 wanderer 与 the 的笔误已合理理解，粗体码成对；标签旁空格及五级／10级的数字体例都是纯静态排版，不据此改 target。 |
| hrq-00419 | entry-02598 | mod-tome.lua:34849 | no_change | accepted | 否 | 无需修改；原文先叙述数世纪受奴役，再说烈火纪获得自由，现译“之前”由时间顺序直接承接且未改变史实；硬换行没有分隔新段，专名及颜色码与仓内一致。 |
| hrq-00420 | entry-02599 | mod-tome.lua:34882 | fix | accepted | 是 | 独立核验通过；四个数值占位符顺序正确，但源码用 living 分类检查，非活体并不限于不死族；现译把适用排除范围缩窄。 |
| hrq-00421 | entry-02601 | mod-tome.lua:34884 | fix | accepted | 是 | 独立核验通过；反证是现译法力值确为其中一种消耗；但 activate 同时设置 mana、vim、paradox、正负能量的暴击消耗，故“只消耗法力值”缩窄了资源范围。 |
| hrq-00422 | entry-02609 | mod-tome.lua:35003 | no_change | accepted | 否 | 无需修改；“看到看不到的东西”口语化，但原文 detection of unseen things 的发现能力仍被表达，未证实机制反转；本行只有二级意见。 |
| hrq-00423 | entry-02614 | mod-tome.lua:35068 | no_change | accepted | 否 | 无需修改；原文明确 Radiance radius 暂降至 1，现译光照半径 1 码保留该机制；技能名不够鲜明仅是表达建议。 |
| hrq-00424 | entry-02636 | mod-tome.lua:35331 | fix | accepted | 是 | 独立核验通过；GHOUL_ROT 的效果名及说明均用“尸鬼腐蚀”，本条疾病泛称虽描述了感染却遮蔽同一状态名；与移除日志一起对齐。 |
| hrq-00425 | entry-02637 | mod-tome.lua:35332 | fix | accepted | 是 | 独立核验通过；同一 GHOUL_ROT 的 on_lose 与 on_gain 成对；改用效果名后两条同步一致，且保留摆脱状态的原意。 |
| hrq-00426 | entry-02638 | mod-tome.lua:35347 | fix | accepted | 是 | 独立核验通过；on_gain 仅建立针对某伤害类型的 ward，真正吸收在 absorb 回调发生；现译在获得状态时宣称已经吸收攻击，时间与动作均错。 |
| hrq-00427 | entry-02640 | mod-tome.lua:35379 | no_change | accepted | 否 | 无需修改；focused by arcane vortex 在状态获得日志里表示受到漩涡作用，现译“围绕”保留空间关系；无证据表明机制条件因此错误。 |
| hrq-00428 | entry-02643 | mod-tome.lua:35393 | no_change | accepted | 否 | 无需修改；10%% 后与可选后缀 %s 之间空格只影响静态排版，数值及占位符不变；按本批纯空格不改规则不修。 |
| hrq-00429 | entry-02644 | mod-tome.lua:35394 | no_change | accepted | 否 | 无需修改；本条是拼接后缀，开头中文逗号可接前条；争议的半角空格在另一条，当前 target 无独立语义缺陷。 |
| hrq-00430 | entry-02688 | mod-tome.lua:35800 | no_change | accepted | 否 | 无需修改；源码效果是骷髅拾取死去同伴的遗骨，on_lose 又称 additional bones；“骨头”有直接上下文依据，死亡已由骷髅遗骨语境承接。改作遗骸属文风偏好。 |
| hrq-00431 | entry-02694 | mod-tome.lua:35928 | fix | accepted | 是 | 独立核验通过；两个 50%% 与四技能均正确，但 CD 为未本地化缩写，且“冷却速度变慢一倍”含混；原文 twice as slow 是冷却所需时间翻倍。 |
| hrq-00432 | entry-02700 | mod-tome.lua:35945 | no_change | accepted | 否 | 无需修改；五个占位符及其顺序正确，“攻击目标时”承接猎物受击条件；%s 后英文句点照原文保留。“Bonus level”简作等级在本状态加成说明中仍可理解为加成等级。 |
| hrq-00433 | entry-02735 | mod-tome.lua:36391 | no_change | accepted | 否 | 无需修改；近战受击反伤及参数顺序准确；ice 对应寒冰的既有术语记录与现译一致。 |
| hrq-00434 | entry-02740 | mod-tome.lua:36441 | fix | accepted | 是 | 独立核验通过；冷却参数与“使用越多、冷却越长”的机制完整；但 taints 对应本仓 preferred 技能类别“污印”，堕落印记是旧称，应对齐。 |
| hrq-00435 | entry-02747 | mod-tome.lua:36505 | fix | accepted | 是 | 独立核验通过；生命线是受事且 severed 指被切断，收割隐含另一动作；原译不能由同句或日志宿主反证。 |
| hrq-00436 | entry-02759 | mod-tome.lua:36574 | fix | accepted | 是 | 独立核验通过；效果名 Shroud of Weakness 支持“虚弱帷幕”；但原文像沉重负担般压在身上的描写在整句均未出现，是明确遗漏。 |
| hrq-00437 | entry-02763 | mod-tome.lua:36582 | fix | accepted | 是 | 独立核验通过；15 个参数及 20%% 保持原序；Harrow 在本段译折磨而关联日志译惊扰，应成对对齐。双空格只属排版，术语全规范的概括无独立证据；Plagued by Visions 的受扰者是本人，现译“扰乱幻象”倒置关系。 |
| hrq-00438 | entry-02764 | mod-tome.lua:36593 | fix | accepted | 是 | 独立核验通过；两个 %s 与颜色码完整；同一 Harrow 在状态长描述中为折磨，日志“惊扰”削弱同一机制识别，成对改为折磨。 |
| hrq-00439 | entry-02765 | mod-tome.lua:36600 | fix | accepted | 是 | 独立核验通过；原文共有九个格式参数，译文类型与顺序保持；双空格属排版，闪避术语不据泛称断言。Power 1 those around you 是你身边的人而非围绕你的努力；Power 4 will increase 是自动生效而非玩家可选择。 |
| hrq-00440 | entry-02775 | mod-tome.lua:36662 | fix | accepted | 是 | 独立核验通过；源文 cold 与本批同类区域效果的寒冷伤害／寒冷抗性一致；当前寒冰在同族内构成属性名不一致，数字不变。 |
| hrq-00441 | entry-02789 | mod-tome.lua:36707 | fix | accepted | 是 | 独立核验通过；现译“按比例损失生命”未指出基数，源码按 max_life*dam/100 计算；补明最大生命值，同时保留逐回合递增及当前比例。 |
| hrq-00442 | entry-02790 | mod-tome.lua:36739 | fix | accepted | 是 | 独立核验通过；日志在从 reprieve 地图返回原地点后出现，省略主语可以成立；但“被从避难所带了回去”方向和施动表达含混，改明你已返回。 |
| hrq-00443 | entry-02791 | mod-tome.lua:36742 | defer | deferred | 否 | %s 填所有格短语时“和%s时空克隆”语法可成立；但同一效果说明在冻结外使用“时空复制体”。如统一专名须同时改该关联载体，当前仅改单条会制造族内不一致，留待扩展 workset。 |
| hrq-00444 | entry-02798 | mod-tome.lua:36788 | fix | accepted | 是 | 独立核验通过；此处 +20 magic 是核心属性而非魔法系统泛称；本仓 Magic 属性既有译名“魔力”，应与属性栏对齐，其他数值不变。 |
| hrq-00445 | entry-02801 | mod-tome.lua:36794 | no_change | accepted | 否 | 无需修改；冒号后空格属纯静态排版；两次“同时”显得重复，但水减两项、增一项的机制与数值完整，属二级语法建议。 |
| hrq-00446 | entry-02805 | mod-tome.lua:36800 | fix | accepted | 是 | 独立核验通过；power burns 的火焰隐喻可支持现译，不单独据此判错；但源码明确 reflects teleportation magic，现译“可能干扰”改变确定性和作用性质。 |
| hrq-00447 | entry-02806 | mod-tome.lua:36802 | fix | accepted | 是 | 独立核验通过；冒号后空格仅属排版；源文明确 dreaming sleep state，现译只说进入梦境，遗漏睡眠状态，数值虽正确也不能弥补。 |
| hrq-00448 | entry-02807 | mod-tome.lua:36804 | no_change | accepted | 否 | 无需修改；冒号后半角空格是纯静态排版；尽管英文少写百分号，固定源码 inc_damage[LIGHTNING]=10 是百分比增伤，中文 +10% 准确反映运行机制。 |
| hrq-00449 | entry-02828 | mod-tome.lua:37132 | no_change | accepted | 否 | 无需修改；与魔法效果同文；“看到看不到的东西”偏口语，但仍表达感知不可见事物，detection 的范围差别不足证明机制误译。 |
| hrq-00450 | entry-02830 | mod-tome.lua:37192 | fix | accepted | 是 | 独立核验通过；源码在 on_gain 插入“逃跑”或“为下一次击杀”；现译“准备了为下一次击杀”不成句。括注使两种已冻结填充值都可作准备事项，且无需改孪生条目。 |
| hrq-00451 | entry-02846 | mod-tome.lua:37383 | fix | accepted | 是 | 独立核验通过；on_merge 说明此日志是旧诅咒伤口重新裂开，并可能提高治疗削减；“再次遭受创伤”弱化重新裂开的动作，修复该叙述而不额外宣称每次必加深。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
