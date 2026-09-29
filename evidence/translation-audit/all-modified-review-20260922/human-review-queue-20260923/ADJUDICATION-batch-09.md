# 批阅裁决台账 — batch-09

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`69a4eed889d294040db0348dbe91e99f5cdd1a8f64af60acab35b42ba3698499`
- 决策行：40；冻结修订（含孪生载体）：43
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 42 |
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
| hrq-00332 | entry-02110 | mod-tome.lua:27521 | fix | accepted | 是 | 独立核验通过；原句最后的“最大能量吸收量”可指护盾吸伤上限；源码 absorbLimit 实为每回合从该护盾取得的能量上限。统一为“灵能值”并明确取得上限；模型对具体消费链的额外归因不作为依据，三个占位符不变。 |
| hrq-00333 | entry-02113 | mod-tome.lua:27540 | no_change | accepted | 否 | 无需修改；后句“最多一共（净化和免疫）能影响 %d 种”已限定前句“所有”的实际配额，完整句段没有承诺无条件清除全部效果；%d 对应共享的 getRemoveCount，孤立截取前句不足以确认缺陷。 |
| hrq-00334 | entry-02115 | mod-tome.lua:27545 | no_change | accepted | 否 | 无需修改；源码判定 ghost subtype，现译“鬼魂”没有错认对象；英文括号移为“注”仍明确仅精神通道造成精神伤害，三个占位符保持原序。“ghost=幽灵”仅为 existing 术语，不强制改名。 |
| hrq-00335 | entry-02125 | mod-tome.lua:27629 | no_change | accepted | 否 | 无需修改；固定源码英文说明本身将 Accuracy/damage 的对应次序写反，译文忠实承接英文，不能把上游失准归为中文新增错误；四个 %d 与两个 %0.1f%% 对应 info 参数。 |
| hrq-00336 | entry-02128 | mod-tome.lua:27692 | fix | accepted | 是 | 独立核验通过；完整句段已说明关闭光环会释放跳跃电能，“发射射线”仍错称投射形态；改为“不释放这股电能”。LIGHTNING_DAZE 对应眩晕且与 preferred daze 一致，全部占位符及 50%% 不变。 |
| hrq-00337 | entry-02141 | mod-tome.lua:27826 | no_change | accepted | 否 | 无需修改；原文断言心灵感知范围之外无物存在，现译“没有任何事物能逃脱……感知”表达同一全称关系；精神力量的措辞属风味意译，未发现可核实的机制或叙事关系遗漏。 |
| hrq-00338 | entry-02148 | mod-tome.lua:27892 | fix | accepted | 是 | 独立核验通过；同文件实体名、日志和同段三次指代均指 dream projection，现译“梦境守卫”与“梦境投影”不一致；改用同节实体名。“可叠加”有 brainlock 逐次施加语境支持，不改变占位符。 |
| hrq-00339 | entry-02149 | mod-tome.lua:27906 | fix | accepted | 是 | 独立核验通过；原文和 getPsiDamageResist 均将人物等级减伤与剩余部分的技能等级减伤连续计算，现译只并列列数；补足“剩余部分再”关系，并把 global speed 明确为全局速度。源码 onTickEnd 用属性减 10 计算增补，故保留基数说明；占位符不变，第二行补句号。 |
| hrq-00340 | entry-02150 | mod-tome.lua:27917 | no_change | accepted | 否 | 无需修改；三个 %d%% 的对应关系正确；“基础值 10”来自同族 onTickEnd 对属性减 10 的计算，负体质的反向影响亦由算式直接推出。100 %% 和 10 %% 只是数字空格差异，按纯静态排版策略不改。 |
| hrq-00341 | entry-02153 | mod-tome.lua:27929 | fix | accepted | 是 | 独立核验通过；占位符正确，“基础值 10”有属性减 10 的代码依据；“鉴定”是技能检定用词错误，且现句遗漏只有检定成功才减伤的条件，改明成功条件并用“检定”。 |
| hrq-00342 | entry-02181 | mod-tome.lua:28344 | no_change | accepted | 否 | 无需修改；抗性在游戏里以百分比计，译文为 %d 加转义百分号明确单位，未改变 tformat 的 %d 占位符；原文数值单位省略不足以证明译文增补错误，静态格式也不单独整理。 |
| hrq-00343 | entry-02187 | mod-tome.lua:28406 | fix | accepted | 是 | 独立核验通过；源码选择目标生物并未限于“怪物或被护送者”，括注过度缩窄可选对象；删除括注。两处 %d 及目标区域半径保留。 |
| hrq-00344 | entry-02189 | mod-tome.lua:28417 | fix | accepted | 是 | 独立核验通过；源码同样不把可选生物限定为怪物或被护送者，删除该括注；minimum range 是随机传送下限，现译“最小半径”在此随机目标区域语境可理解为距离下限，证据不足以按模型主张单独改写。 |
| hrq-00345 | entry-02191 | mod-tome.lua:28437 | fix | accepted | 是 | 独立核验通过；概率穿越的 prob_travel 是移动遇到实体障碍时穿到另一侧，现译“击中”容易误作攻击触发；改为“移动碰到”，其余传送距离和不稳定回合关系已表达。 |
| hrq-00346 | entry-02192 | mod-tome.lua:28450 | fix | accepted | 是 | 独立核验通过；“最大 %d 回合”不能补足每个负面效果各延长一回合的关系；现译“降低……25%% 1回合”会误示固定持续。补“每个负面效果持续 1 回合”，保留最大值和全部占位符。 |
| hrq-00347 | entry-02207 | mod-tome.lua:28713 | no_change | accepted | 否 | 无需修改；“获得 %d%% 个额外回合”虽不够自然，仍表示按回合比例返还时间；20%% 最大生命阈值和其余参数均已表达，属二级措辞意见。 |
| hrq-00348 | entry-02210 | mod-tome.lua:28797 | fix | accepted | 是 | 独立核验通过；首句明确保护对象含你、傀儡和其他友方；第二句“它”承接该保护，译文缩为“你”遗漏受保护对象。源码爆炸在五级保护使友方伤害归零后提前返回，模型所引 target 排除行不在本版本可见逻辑中，不采纳其归因。 |
| hrq-00349 | entry-02212 | mod-tome.lua:28848 | defer | deferred | 否 | Flame→火球术只是 existing 术语，不是强制译名；本文件 Burning Wake（entry-02285，冻结外）称同一技能“火焰”，奇术师说明则称“火球术”。单改本技能名会制造同族不一致，需将 entry-02285 等引用纳入统一决策后处理；本次不改。 |
| hrq-00350 | entry-02227 | mod-tome.lua:29143 | fix | accepted | 是 | 独立核验通过；源码对非亡灵敌人施加 dazed，preferred daze=眩晕；现译“茫然”与效果身份和术语不符，改为“眩晕”，其他条件与参数保留。 |
| hrq-00351 | entry-02252 | mod-tome.lua:29537 | fix | accepted | 是 | 独立核验通过；原文 incinerate 明确是焚毁，现译“打击”只表达一般攻击；前后无句段补足燃烧结果，改为“焚毁”，保持风暴主体。 |
| hrq-00352 | entry-02258 | mod-tome.lua:29549 | fix | accepted | 是 | 独立核验通过；原文 and 并列更快旅行与追踪他人，现译“或者”误示互斥；同时“更快的旅行”在动词结构中误用“的”，改成“更快地旅行并追踪他人”。 |
| hrq-00353 | entry-02259 | mod-tome.lua:29551 | no_change | accepted | 否 | 无需修改；“可以使……能”虽显重复，但感知周围与搜寻隐藏事物两个作用均已表达，属于二级行文润色；报告没有指出一级语义或运行时缺陷。 |
| hrq-00354 | entry-02265 | mod-tome.lua:29638 | no_change | accepted | 否 | 无需修改；译文“该技能”在技能使用提示中有清楚指代，法杖前置条件完整；省略 Blunt Thrust 专名仅降低日志独立辨识度，属风格建议。 |
| hrq-00355 | entry-02267 | mod-tome.lua:29640 | fix | accepted | 是 | 独立核验通过；固定源码以 is_melee/attackTargetWith 执行近战攻击，melee damage 不是泛称近程；改“近战伤害”。第二句缺句号属标点错误，补“。”；震慑、必中与占位符保留。 |
| hrq-00356 | entry-02269 | mod-tome.lua:29662 | no_change | accepted | 否 | 无需修改；日志两个 %s 依次为装备和宝石，语义顺序正确；“安装”可描述将宝石置入装备，本技能内“附魔”与“镶嵌”也并存，暂无唯一规范词，改一条不能建立一致性。 |
| hrq-00357 | entry-02273 | mod-tome.lua:29694 | fix | accepted | 是 | 独立核验通过；原文区分不能主动移动与强制位移终止持续，现译“任何移动”漏掉后者限定；“土壤相关影响”丢失大地亲和含义；冷却“回合数：%d%%”误把百分比说成回合数。修正这三项，保留现有换行及五个参数。源码 never_move 只直接证实不能主动移动，模型所列击退、传送等一概终止的推断不采纳。 |
| hrq-00358 | entry-02277 | mod-tome.lua:29743 | fix | accepted | 是 | 独立核验通过；段落合并只是静态排版，不调整换行；但原译省略伤害送往未来与时间回复力场两个概念，且“时间屏障”违反 preferred Time Shield=时间盾。补足时空关系并统一术语，两个 %d 和 10%% 仍对应原值。 |
| hrq-00359 | entry-02278 | mod-tome.lua:29750 | no_change | accepted | 否 | 无需修改；新增段落换行属纯静态排版且冻结条件禁止改换行序列；源码无敌、目标时间停止、冷却和资源不回复均已由现译表达，唯一 %d 正确。 |
| hrq-00360 | entry-02280 | mod-tome.lua:29790 | no_change | accepted | 否 | 无需修改；补述法力充足时扣法力补满充能、否则解除持续有 callbackOnActBase 支持；首句省略 residual energies 是风味意象，后句仍明确射线施法后的免费移动，%d 和段落正确。 |
| hrq-00361 | entry-02290 | mod-tome.lua:29932 | no_change | accepted | 否 | 无需修改；末句拆行是纯静态排版；三处占位符顺序与命中、物理强度、震慑及定身抵抗一致，不改换行序列。 |
| hrq-00362 | entry-02303 | mod-tome.lua:30008 | fix | accepted | 是 | 独立核验通过；术语 Tumble 虽为 existing，但本文件同技能名和日志均用“翻筋斗”，本句“翻滚”造成同族名称不一致；改为“翻筋斗”。等级 3/5 拆段仅排版，参数和数值保持正确。 |
| hrq-00363 | entry-02306 | mod-tome.lua:30039 | fix | accepted | 是 | 独立核验通过；原文 Rapid Fire 是固定源码对 Rapid Shot 的旧称，译文“这个技能”避免错误专名；但生效的 on_pre_use 调用 archerPreUse(...,"sling")，弓并不能满足前置。改为只需投石索，驳回模型“弓或投石索限制准确”的判断。 |
| hrq-00364 | entry-02312 | mod-tome.lua:30077 | fix | accepted | 是 | 独立核验通过；源码仅对指定目标发射一发，沿途敌人不是追加受击对象；“穿透目标以外单位”既未限定你与目标之间，也可能误示穿透伤害。改为“越过你与目标之间的其他敌人”，%d%% 和命中加成不变。 |
| hrq-00365 | entry-02319 | mod-tome.lua:30115 | no_change | accepted | 否 | 无需修改；双持限制已完整表达，技能使用语境能指认“这个技能”；省略 Coup de Grace 专名仅是日志独立辨识度偏好。 |
| hrq-00366 | entry-02326 | mod-tome.lua:30194 | fix | accepted | 是 | 独立核验通过；第二行“（但不会小于 0%%）”后没有句末句号，下一行已另起完整句，属明确标点遗漏；物理抗性下限与两个占位符均正确，补标点即可。 |
| hrq-00367 | entry-02327 | mod-tome.lua:30200 | fix | accepted | 是 | 独立核验通过；固定源码该技能名为 Unstoppable，本文件 talent name 与状态名均译“势不可挡”，现说明“无双状态”无法对应同一技能；改为“势不可挡激活期间”。数值、不能使用物品和治疗条件已表达。 |
| hrq-00368 | entry-02337 | mod-tome.lua:30288 | fix | accepted | 是 | 独立核验通过；固定源码两次 heavy mail armour 指同一 heavy 装备子类，本段却先写“重甲”后写“锁甲”；本文件 heavy entity subtype 与同段前句均采用“重甲”，将后一处统一为“重甲”，保持 massive plate=板甲 及占位符不变。 |
| hrq-00369 | entry-02343 | mod-tome.lua:30369 | no_change | accepted | 否 | 无需修改；manage contact 的失败条件在源码中仍是必须双持，现译已提供玩家所需操作；省略具象说法仅文风偏好，同一族后备提示均用“这个技能”。 |
| hrq-00369 | entry-02344 | mod-tome.lua:30377 | no_change | accepted | 否 | 无需修改；双持前置条件明确，Offhand Jab 专名虽未写出但技能界面可提供指代；这是日志辨识度的风格建议，现译未改变操作条件。 |
| hrq-00369 | entry-02346 | mod-tome.lua:30386 | no_change | accepted | 否 | 无需修改；双持前置条件明确，Dual Strike 专名虽未写出但技能界面可提供指代；这是日志辨识度的风格建议，现译未改变操作条件。 |
| hrq-00369 | entry-02347 | mod-tome.lua:30393 | no_change | accepted | 否 | 无需修改；双持前置条件明确，Flurry 专名虽未写出但技能界面可提供指代；这是日志辨识度的风格建议，现译未改变操作条件。 |
| hrq-00370 | entry-02345 | mod-tome.lua:30379 | fix | accepted | 是 | 独立核验通过；完整句段虽已给主手加徒手两次攻击，仍未说明徒手攻击取代常规副手攻击；源码 action 与 info 同时确认这一替代关系。将其补在首句，四个占位符及混乱条件保留。 |
| hrq-00371 | entry-02352 | mod-tome.lua:30431 | no_change | accepted | 否 | 无需修改；双持前置条件完整，“这个技能”在 Lunge 技能使用界面有明确指代；省略技能专名仅属日志风格偏好。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
