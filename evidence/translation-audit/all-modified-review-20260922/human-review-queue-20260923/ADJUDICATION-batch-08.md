# 批阅裁决台账 — batch-08

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`64717f88c6ac9ac5d41808042dafd34dfa9dba4c3bd2e533fcebed743b682d77`
- 决策行：40；冻结修订（含孪生载体）：40
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 37 |
| deferred | 3 |

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
| hrq-00292 | entry-01895 | mod-tome.lua:25031 | fix | accepted | 是 | 独立核验通过；源码 gifts.lua 该天赋类别描述为 foes around you；现译“向敌人”丢失空间限定，补“你周围的”。无其他反证：该串为类别说明，不承接前文。 |
| hrq-00293 | entry-01899 | mod-tome.lua:25114 | fix | accepted | 是 | 独立核验通过；术语 Resistances=抗性（preferred），“所有抵抗”“抵抗受…加成”改为抗性，本仓“所有抗性”已有 8 处。原 pending 的树名 claim 可由本仓核验：同节 mod-tome.lua:25026/25028 的 talent type 为“软泥利刃”“腐蚀利刃”，本条“软泥之刃/腐蚀之刃”与之不一致，按同节树名对齐；同时补 all the talents inside are exchanged 的“其中所有 |
| hrq-00294 | entry-01905 | mod-tome.lua:25165 | no_change | accepted | 否 | 无需修改；advisory 驳回：avoid any damaging attack 以 %d%% 几率完全不受伤害，“完全免疫任何伤害”在带几率限定下与原义等价，属措辞偏好；avoidance 译“免疫几率”与上句一致。refuted claim（数值后未重复“流血伤害”）同意驳回：“流血，每回合受到 %0.2f 点伤害”已表达。 |
| hrq-00295 | entry-01911 | mod-tome.lua:25260 | no_change | accepted | 否 | 无需修改；唯一 claim 为前两句换行被合并，属纯静态排版；SPEC 规定不改换行序列与硬换行，不整理。其余占位符与机制（几率、持续、上限、暴击延长 2 回合）正确。 |
| hrq-00296 | entry-01913 | mod-tome.lua:25288 | fix | accepted | 是 | 独立核验通过；三处均经固定源码核验成立：Actor.lua onTakeHit 在 value>0（受到伤害）时触发，“受到攻击”改为“受到伤害”并保留 may 为“可能会”，同时补 nearby within your line of sight（findFreeGrid 带视线参数）；getMax 取 checkMaxSummon 上限与技能等级的较小值，补“受技能等级和召唤上限限制”并补 so long as this talent is ac |
| hrq-00297 | entry-01917 | mod-tome.lua:25317 | no_change | accepted | 否 | 无需修改；暴击机制 refuted 成立：ignore_direct_crits 在 damage_types.lua:130-151 按比例削减暴击额外伤害，现译“额外伤害降低”准确。wounds→cut_immune，“流血”正确。blindness/目盲 claim 不采纳：passives 为 blind_immune，术语 blind=致盲 仅为 existing 不强制；本仓“目盲免疫”与“致盲免疫”并存（3/4），batch-07  |
| hrq-00298 | entry-01919 | mod-tome.lua:25331 | fix | accepted | 是 | 独立核验通过；getNatureDamage 为 base*min(5,level)^0.5/2.23，level 最多 5，即加成最多提升 4 次、最大值约为初始值的 2.24 倍而非 4 倍；“最多4倍”误译次数为倍率，改为“最多提升 4 次”，并补 to a creature 与 with later Acid damage。 |
| hrq-00299 | entry-01924 | mod-tome.lua:25467 | fix | accepted | 是 | 独立核验通过；补“伤害受精神强度加成”句末句号（漏句末标点）。refuted claim 同意驳回：“最多移动20次”并入首句属排版，不拆句。 |
| hrq-00300 | entry-01945 | mod-tome.lua:25683 | no_change | accepted | 否 | 无需修改；advisory 驳回：burn and crush your foes to death 概括为“摧毁敌人”，下一句“从很远的地方烧毁敌人”已承接烧灼意象，无机制缺失；补两层动作属文风。 |
| hrq-00301 | entry-01970 | mod-tome.lua:25806 | no_change | accepted | 否 | 无需修改；claim 自标 advisory：“25 %%几率”仅为数字与百分号间空格，属纯静态排版／数字格式，按用户策略不整理；占位符与机制（25%% 缴械 3 回合）正确。 |
| hrq-00302 | entry-01976 | mod-tome.lua:25875 | fix | accepted | 是 | 独立核验通过；末行两处“%d%% ,”为带前置空格的英文半角逗号，属中文标点错误，改为全角逗号。其余占位符顺序与 info tformat 相符。 |
| hrq-00303 | entry-01980 | mod-tome.lua:25892 | fix | accepted | 是 | 独立核验通过；固定源码 Knife Storm：getDuration 用于 map:addEffect 的效果持续时间（风暴存在时间），PHYSICALBLEED 的流血时长不由 %d 决定；原译“流血 %d 回合”错置。改为“使其流血，风暴持续 %d 回合”，末句“流血持续时间”改为“风暴持续时间”（getDuration 含 combatMindpower）。approaches 改“靠近的任何人”以贴合 anyone who approach |
| hrq-00304 | entry-01984 | mod-tome.lua:25923 | defer | deferred | 否 | 固定源码 horrors.lua:671 已是 for 15 turns（summon_time=15），本条英文“10 turns”在固定版本不会命中，属历史陈旧键；其译文对自身英文准确，改成 15 会造成与 source 不符。清理需删除条目，超出本任务可编辑面（仅限 target），按 hint 单独清理。 |
| hrq-00305 | entry-01988 | mod-tome.lua:25973 | defer | deferred | 否 | 固定源码 inscriptions.lua:245-248 的 Heroism info 已含 to a maximum of 100%%…，本条旧英文不会命中（活条目为 entry-02000），属历史陈旧键，需删除而非改 target，超出可编辑面，留单独清理。括号拆行属排版、“致死的伤害”属措辞，均 advisory，不在陈旧键上投入修改。 |
| hrq-00306 | entry-01989 | mod-tome.lua:25981 | fix | accepted | 是 | 独立核验通过；中英文分号混用属标点错误。同节 inscription short_info 族（如 mod-tome.lua 周边“治疗 %d; 冷却 %d”“伤害 %d; 持续 %d; 冷却 %d”）统一用半角“; ”，故将全角“；”改为半角以与族内一致，不制造新不一致。 |
| hrq-00307 | entry-01994 | mod-tome.lua:26029 | no_change | accepted | 否 | 无需修改；advisory 驳回：原文 stay out of phase 为小写描述性短语而非效果名引用，“脱离相位”准确；孪生条目 Rune: Phase Door（mod-tome.lua:26107，冻结外）同样用“脱离相位”，单改本条会制造族内不一致。 |
| hrq-00308 | entry-02000 | mod-tome.lua:26137 | no_change | accepted | 否 | 无需修改；括号数值拆行属纯静态排版且涉及换行序列，SPEC 禁止改；其余内容与固定源码 inscriptions.lua:245-248 一致，占位符顺序正确。 |
| hrq-00309 | entry-02004 | mod-tome.lua:26213 | no_change | accepted | 否 | 无需修改；advisory 驳回：beam down 本身是科幻传送俚语，“哔的一下”的拟声口语化保留了传送下降含义，属文风取舍，无机制偏差。 |
| hrq-00310 | entry-02015 | mod-tome.lua:26343 | fix | accepted | 是 | 独立核验通过；固定源码 Rushing Claws 的 message 在使用时显示；action 只移动并在相邻时施加 EFF_PINNED，无攻击伤害。“用尖利的爪子攻击”把 claws sharp and ready 动作化为攻击，与实现不符，改为“利爪蓄势待发”。 |
| hrq-00311 | entry-02022 | mod-tome.lua:26417 | fix | accepted | 是 | 独立核验通过；固定源码 Sever Lifeline 的 action 为一次性 setEffect(EFF_SEVER_LIFELINE, 4)，不是引导法术，施法者不受束缚；效果结算为时空伤害（info 以 damDesc TEMPORAL 显示），并非无条件立即死亡。三处 claim 成立，改为“开始离断目标的生命线。4 回合后，如果目标仍在你的视线内，它的存在将被终结（%d 时空伤害）。”，括号按 bracket_fullwidth 改全角。 |
| hrq-00312 | entry-02023 | mod-tome.lua:26441 | fix | accepted | 是 | 独立核验通过；术语 cold=寒冷（damage type）；本仓“寒冷伤害”71 处、“冰冷伤害”10 处，两处改为“寒冷伤害”。 |
| hrq-00313 | entry-02024 | mod-tome.lua:26456 | fix | accepted | 是 | 独立核验通过；原文 lightning damage 的伤害类型被漏译，补“闪电伤害”（术语 lightning=闪电）。 |
| hrq-00314 | entry-02025 | mod-tome.lua:26476 | fix | accepted | 是 | 独立核验通过；第二行缺句末句号，补“。”。 |
| hrq-00315 | entry-02026 | mod-tome.lua:26482 | no_change | accepted | 否 | 无需修改；claim 为概率与“额外获得”之间的硬换行；SPEC 明确硬换行属纯静态排版且不得改换行序列，不并句。语义与占位符正确。 |
| hrq-00316 | entry-02027 | mod-tome.lua:26488 | fix | accepted | 是 | 独立核验通过；Steady Mind 的背景句 Superior cunning and training…outthink and outwit your opponents' physical and mental assaults 被压缩为“大量的训练使你能保持清醒的头脑”，丢失灵巧、智取与肉体／精神攻击三层信息，补全。“近身闪避”为本仓 Defense 的既有译名（mod-tome.lua:1910），保留。 |
| hrq-00317 | entry-02028 | mod-tome.lua:26499 | fix | accepted | 是 | 独立核验通过；feel a surge of power 是自身感到力量涌起，“漏出一股汹涌的霸气”改变了方向（向外漏出）并夸张 power，改为“感到一股力量涌起”。bites the dust 的“扑街”属俚语风格 advisory，保留。 |
| hrq-00318 | entry-02032 | mod-tome.lua:26539 | fix | accepted | 是 | 独立核验通过；原文点名 Sweep，现译“这个技能”丢失技能名；同族 Momentum 日志（mod-tome.lua:26621）点名“急速切割”，按本节天赋名“横扫”（mod-tome.lua:26537）补回。 |
| hrq-00319 | entry-02043 | mod-tome.lua:26615 | fix | accepted | 是 | 独立核验通过；原文点名 Precision，现译“这个技能”丢失技能名；按本节天赋名“弱点打击”（mod-tome.lua:26614）补回，与 Momentum 同族日志一致。 |
| hrq-00320 | entry-02050 | mod-tome.lua:26667 | no_change | accepted | 否 | 无需修改；claim 为排版性（The circle lasts %d turns 拆为独立行），属纯静态排版且涉及换行序列，不改。占位符与机制正确。另注：同条“法阵／阵法”用词不一属二级 advisory，本行无 claim 覆盖，不扩大修改。 |
| hrq-00321 | entry-02058 | mod-tome.lua:26777 | refuted | accepted | 否 | 驳回模型主张；固定源码 action 施加 EFF_BLOCKING，d_types 为物理类型，效果不区分近战与远程；英文 melee 与实现矛盾。现译“减少所有物理伤害”贴合实现，按 hint 不补“近战”，上游文本问题另行记录。 |
| hrq-00322 | entry-02066 | mod-tome.lua:26894 | no_change | accepted | 否 | 无需修改；六项为物理强度、物理豁免、法术强度、法术豁免、精神豁免、精神强度，恰为全部三种强度与三种豁免，“所有强度和豁免”归纳无信息丢失；refuted claim 成立。 |
| hrq-00323 | entry-02067 | mod-tome.lua:26898 | defer | deferred | 否 | 固定源码 races.lua:692 为 tformat(duration, count)，与英文“Removes %d … for %d turns”顺序相反，属上游缺陷；现译忠实于英文。在中文中调换语序以适配实参属跨条目策略（上游修正后会反向出错），不得改 args_order，交维护者决定并记入上游问题清单。 |
| hrq-00324 | entry-02069 | mod-tome.lua:26910 | fix | accepted | 是 | 独立核验通过；Orcs 按术语 Orc=兽人（creatures.tsv）且本仓“兽人”402 处、“兽族”7 处，改为“兽人”。They→“你们”属视角 advisory，本条为玩家种族天赋，保留。占位符与机制正确。 |
| hrq-00325 | entry-02074 | mod-tome.lua:27062 | fix | accepted | 是 | 独立核验通过；首行缺句末句号，补“。”。机制与占位符正确。 |
| hrq-00326 | entry-02081 | mod-tome.lua:27179 | fix | accepted | 是 | 独立核验通过；bolts 为 Mind Storm 射出的 bolt 投射物（target type=bolt），“灵能值球”误作 psi 资源，五处改为“飞弹”。每枚消耗 5 点反馈值及四个占位符正确。 |
| hrq-00327 | entry-02097 | mod-tome.lua:27318 | fix | accepted | 是 | 独立核验通过；“震慑几率受精神强度加成”缺句末句号，补“。”。参数正确。 |
| hrq-00328 | entry-02103 | mod-tome.lua:27380 | fix | accepted | 是 | 独立核验通过；stamina 术语为“体力值”（resources.tsv，UI Stamina=体力值，mod-tome.lua:20901），“耐力”改为“体力值”。八个参数与资源对应正确。 |
| hrq-00329 | entry-02106 | mod-tome.lua:27408 | fix | accepted | 是 | 独立核验通过；标点：第一行缺句号补“。”，第二行半角“.”改“。”；同时修“小心的同步”→“小心地同步”（的/地混用）。refuted 的正号 claim 驳回：“提升 %d%%”已表达增量。“全属性”符合实现，保留。 |
| hrq-00330 | entry-02107 | mod-tome.lua:27420 | fix | accepted | 是 | 独立核验通过；for 2 turns 译“两轮”不符回合单位，改“2 回合”。penalty 省略 refuted：“（-15%% 伤害）”已表达惩罚方向，不补。 |
| hrq-00331 | entry-02109 | mod-tome.lua:27517 | fix | accepted | 是 | 独立核验通过；energy projection 指能量投射技艺，“灵能值运用”偏离原意，改为“你在能量投射技艺上的专长提升了。”；“变的更慢”→“变得更慢”。%d、%0.2f 与 tformat(cooldown, mast) 相符。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
