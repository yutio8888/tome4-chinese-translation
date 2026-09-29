# 批阅裁决台账 — batch-10

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`f4378c86088485966dae47e9f5ccb0632663fbb4a2d50bc7a2fa318ee541a03d`
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
| hrq-00372 | entry-02354 | mod-tome.lua:30444 | fix | accepted | 是 | 独立核验通过；最强反证：技能 requires_target 且以 scan_on=PROJECTILE 的 bolt 目标选取抛射物，操作上确需选定，故“瞄准”不改变机制结果；但原文条件是 spot（察觉/发现）一枚抛射物，“瞄准”把察觉改成主动锁定，并漏了 shoot at it。改为“发现……时，你能立即向它射击将其击落”，without taking a turn（no_energy=true）译“不消耗回合”。占位符不变。 |
| hrq-00373 | entry-02356 | mod-tome.lua:30456 | no_change | accepted | 否 | 无需修改；唯一 claim 是第二段前的换行被并入上一句。先例 hrq-00295／hrq-00358 已裁定段落合并属纯静态排版，SPEC 与本批判据禁止改换行序列，故不补换行。现译已含拦截、完全瓦解、额外打击、射击伤害和击退，三个参数顺序与 info 一致。 |
| hrq-00374 | entry-02360 | mod-tome.lua:30524 | fix | accepted | 是 | 独立核验通过；采纳遗漏限定：源码 getSlow 经 GRAPPLED 写入 global_speed_add 负值，英文为 Reduces global action speed；被擒目标本就不能移动，“目标减速”易被理解为移动减速。术语 global action speed→“全局速度”为 preferred（terminology/combat.tsv），pending 的术语 claim 由此确认，改为“全局速度降低 %d%%”。#RED# |
| hrq-00375 | entry-02380 | mod-tome.lua:30682 | fix | accepted | 是 | 独立核验通过；claim 自标 advisory，但事实成立：源码首行以冒号引出三行弹药列表，现译首行无任何标点，属漏句末标点，按标点判据补全角冒号。其余十四个占位符与顺序不变，无机制问题。 |
| hrq-00376 | entry-02381 | mod-tome.lua:30692 | fix | accepted | 是 | 独立核验通过；采纳：tformat 以 damDesc(DamageType.NATURE) 格式化，吸血毒素效果按 NATURE 结算，“毒素伤害”把效果性质误作伤害类型，改为“自然伤害”，保留“吸血毒素”效果名。同时把燃烧弹行残留的半角逗号“1, ”改为全角。 |
| hrq-00377 | entry-02391 | mod-tome.lua:30811 | no_change | accepted | 否 | 无需修改；唯一 claim 是“隐匿”两侧空格。先例（hrq-00268 等）裁定贴字空格属纯静态排版，不整理；语义与 Concealment 提示一致，句末“！”对应原文感叹号。 |
| hrq-00378 | entry-02392 | mod-tome.lua:30812 | fix | accepted | 是 | 独立核验通过；采纳：Called Shots 在本仓两处技能名均译“精准射击”（mod-tome.lua:23332、30085），本条“精巧射击”与技能面板名不一致，改为“精准射击”。注：冻结外 mod-tome.lua:30597（Mark 说明）同样写“精巧射击”，本条改动不依赖它，另行登记。 |
| hrq-00379 | entry-02393 | mod-tome.lua:30818 | fix | accepted | 是 | 独立核验通过；采纳半角标点：“0, ”改全角逗号。采纳完整性：thick, disorientating smoke 的两个修饰被压成“烟雾”，补为“浓密烟雾，令人迷失方向”；视野削减等机制原本已译，非机制缺陷。advisory“带着烟雾弹的箭头”属文风，不改。四个占位符不变。 |
| hrq-00380 | entry-02394 | mod-tome.lua:30824 | fix | accepted | 是 | 独立核验通过；最强反证：下半句已正确写“三格外……8 格最大”，误导有限。但 at range 指远距离，“在射程内”暗示所有合法射程都受益，与 tformat(dam, dam*5) 的超过 3 格逐格增伤相悖，改为“这让你的远距离射击更有效”。占位符不变。 |
| hrq-00381 | entry-02399 | mod-tome.lua:30844 | no_change | accepted | 否 | 无需修改；advisory 驳回：同句前部已写“被混乱”，括号内“50%%强度”指代混乱强度无歧义；源码 DamageType.CONFUSION dam=50 与现译一致，属术语清晰度偏好。 |
| hrq-00382 | entry-02422 | mod-tome.lua:30940 | fix | accepted | 是 | 独立核验通过；采纳：原文两句为“提升机动性与闪避敌人的训练和技巧”与“在战场上，站位至关重要”；现译“确保你始终处于战斗的上风”丢失 positioning 主题并新增原文没有的承诺，属忠实度偏差。按原句重译。 |
| hrq-00383 | entry-02425 | mod-tome.lua:30968 | fix | accepted | 是 | 独立核验通过；采纳：Actor.lua 仅在使用 is_unarmed 技能时检查 hasMassiveArmor／isUnarmed 并拒绝施展，装备本身不受限制；“你不能装备……”是机制误导。改为“身穿板甲或装备武器、盾牌时无法施展”，与冻结外同族条目 unarmed discipline（mod-tome.lua:30974）已有表述一致。 |
| hrq-00384 | entry-02426 | mod-tome.lua:30970 | fix | accepted | 是 | 独立核验通过；采纳后半句：同 entry-02425，施展限制被误写成装备禁令，改为与 mod-tome.lua:30974 一致的“身穿板甲或装备武器、盾牌时无法施展”。advisory 驳回：“致命的”与单数化属文风，连击点消耗机制无误，前半句不改。 |
| hrq-00385 | entry-02427 | mod-tome.lua:30972 | fix | accepted | 是 | 独立核验通过；采纳后半句：同 entry-02425 的装备禁令误译，改为施展限制并与 mod-tome.lua:30974 对齐。advisory 驳回：Grappling 类别名本仓为“抓取”系，“抓取敌人的技巧”仍指向核心机制，改名属类别名一致性策略，不在本条扩改。 |
| hrq-00386 | entry-02428 | mod-tome.lua:30976 | fix | accepted | 是 | 独立核验通过；采纳两项：本条是 generic 的 unarmed-training（techniques.lua:90），原文 Teaches various martial arts techniques；现译“高级徒手格斗技能”混入上一条 unarmed-discipline 的 Advanced 并漏 Teaches，按本条原文改为“传授各种武术技巧”。后半句装备禁令同 entry-02425，改为施展限制。 |
| hrq-00387 | entry-02435 | mod-tome.lua:31034 | fix | accepted | 是 | 独立核验通过；采纳：Actor.lua 仅在 speed_type=="throwing" 分支应用 Quickdraw getSpeed，原文 with them 限定范围；现译泛称“攻击速度”会误导为全部攻击。改为“飞刀攻击速度增加 %d%%”，其余不变。 |
| hrq-00388 | entry-02439 | mod-tome.lua:31076 | refuted | accepted | 否 | 驳回模型主张；驳回遗漏触发前提：本条就是 Breathing Room 自身说明，源码在无相邻敌人的同一条件块内、技能等级≥3 时追加等量生命回复；“这个技能带给你等量的生命回复”承接首句条件，不产生不同机制。句末已为全角句号。 |
| hrq-00389 | entry-02449 | mod-tome.lua:31188 | no_change | accepted | 否 | 无需修改；唯一 claim 本身确认括注有源码依据：Shield Pummel 以 ignore_cd=true 强制 Block，引擎中该参数既跳过冷却检查也不触发冷却，“冷却中仍可获得”准确。“盾牌伤害”对应以盾牌进行的攻击。现有 \n\t\t 属换行序列，不改。 |
| hrq-00390 | entry-02451 | mod-tome.lua:31195 | fix | accepted | 是 | 独立核验通过；采纳：getArmor／getBlock 对力量与敏捷各调用相同曲线的 combatTalentStatDamage 并相加，原文 equally 表达等权；现译只说“受……影响”，漏了等权。补为“受你的敏捷和力量值同等影响”，不写成 1:1 换算。 |
| hrq-00391 | entry-02456 | mod-tome.lua:31266 | defer | deferred | 否 | pending 保持：原文 knowledge of corruption 字面为堕落，技能名本仓译“堕落之壳”（mod-tome.lua:31264），与说明的“枯萎能量”存在同条不一致；但解锁条件是承受 BLIGHT 伤害，“枯萎”并非无据。terminology 中 corruption→堕落仅为 existing 且 source_tag 为 talent category，无 preferred 可依，且 human_hint |
| hrq-00392 | entry-02460 | mod-tome.lua:31291 | no_change | accepted | 否 | 无需修改；颜色标签前空格属贴字静态排版，按先例不改。双感叹号规整 advisory 驳回：原文标签内外各一个“!”，合并为一个句末“！”不改变事件，属标点风格。 |
| hrq-00393 | entry-02466 | mod-tome.lua:31322 | fix | accepted | 是 | 独立核验通过；采纳：logSeen 参数依次为 self:getName() 与组装出的 TELOS_SPIRE 物品名；“%s 重组为 %s”把角色说成变成了物品，主宾颠倒。改为“%s 组装出了 %s！”，保留两参数顺序与颜色码。 |
| hrq-00394 | entry-02474 | mod-tome.lua:31333 | fix | accepted | 是 | 独立核验通过；采纳：六处彩色类别后为“ :”（空格加半角冒号），与首行“物理：”不一致，属半角标点错误，统一改为全角冒号；寒冷行缺句末句号，补“。”。8 个占位符及 %% 保持不变（第二个 claim 确认无误）。 |
| hrq-00395 | entry-02489 | mod-tome.lua:31513 | fix | accepted | 是 | 独立核验通过；采纳：源码对 name 为 dread／dreadmaster 的随从授予 Slumber，Dread 是独立亡灵幽灵随从；terminology 中 Dread→“噩灵”为 preferred（talents.tsv、creatures.tsv），mod-tome.lua:28559 同名技能亦为“噩灵”，pending 的替换词据此确认，改“梦魇”为“噩灵”。“和 毁伤”空格属静态排版不改；其余技能名一致性的 pending 缺逐项 |
| hrq-00396 | entry-02500 | mod-tome.lua:31700 | fix | accepted | 是 | 独立核验通过；采纳：原文 The strength of your bond is so strong 指你与恒星化身的羁绊牢固，现译“你的力量如此强大”把来源改成角色自身力量，属忠实度偏差；改为“你与它的羁绊如此牢固”。标签、%% 与机制完整（claim 2 确认）。关联技能名一致性 pending 缺冻结对照，不扩改；行首空格缩进为既有排版，不改。 |
| hrq-00397 | entry-02506 | mod-tome.lua:31869 | no_change | accepted | 否 | 无需修改；占位符 claim 确认无误。pending 驳回：terminology 中 Ghoulish Leap→“定向跳跃”仅为 existing，不强制；本仓该技能名条目实际为“食尸鬼跳跃”（mod-tome.lua:31850 talent name、37645），本条与技能面板一致，改为“定向跳跃”反而制造不一致。同意保留（advisory）。 |
| hrq-00398 | entry-02520 | mod-tome.lua:32306 | no_change | accepted | 否 | 无需修改；advisory 驳回：ToME 4 是 Tales of Maj'Eyal 的通行缩写，同一教程源码其他文本也用 ToME4，指代无误；terminology 无该标题的 preferred 条目。与成就／手札不一致的 pending 无冻结对照，不采信。颜色码、孤狼、按键完整。 |
| hrq-00399 | entry-02521 | mod-tome.lua:32352 | no_change | accepted | 否 | 无需修改；落款缩进（制表符 vs 空格）属纯静态排版且涉及空白序列，不改；落款句号为标点风格 advisory，不影响含义。refuted 的 ShowText 主张不影响本结论。占位符与专名正确。 |
| hrq-00400 | entry-02522 | mod-tome.lua:32371 | fix | accepted | 是 | 独立核验通过；采纳：“一个”包裹”” 的开引号为 U+201D，属标点错误，改为成对的“包裹”。额外空行与落款排版两项 advisory 属静态排版且涉及换行序列，不改。 |
| hrq-00401 | entry-02523 | mod-tome.lua:32407 | fix | accepted | 是 | 独立核验通过；硬换行 claim 不改：先例 hrq-00315／hrq-00308 裁定硬换行属纯静态排版，禁止改换行序列。半角括号按用户 standing policy bracket_fullwidth 统一为全角，括号内换行保持原位。颜色标签与语义完整。 |
| hrq-00402 | entry-02524 | mod-tome.lua:32437 | no_change | accepted | 否 | 无需修改；数值规则确认正确；行内硬换行属纯静态排版，禁止改换行序列，不改。术语 pending：力量、敏捷、魔力、意志、灵巧、体质与本仓属性译名一致，无相反证据。 |
| hrq-00403 | entry-02530 | mod-tome.lua:32784 | no_change | accepted | 否 | 无需修改；判定关系确认正确；refuted 的是 Gemini 的“完全一致”背书（震慑免疫为原教程简化），中文忠实复述英文，非翻译失真，不补条件。行内硬换行禁止改换行序列。括号已为全角。 |
| hrq-00404 | entry-02533 | mod-tome.lua:33109 | no_change | accepted | 否 | 无需修改；区间与 tier 定义确认正确；额外硬换行属纯静态排版且涉及换行序列，不改。 |
| hrq-00405 | entry-02534 | mod-tome.lua:33121 | no_change | accepted | 否 | 无需修改；五组区间与颜色码确认对应。第五行颜色码前缺空格属纯静态空格差异，advisory 不改；颜色码不显示，第五行实际呈现更符合中文排版。 |
| hrq-00406 | entry-02538 | mod-tome.lua:33287 | fix | accepted | 是 | 独立核验通过；采纳：原文为“精灵会乐意用手头的任何法术轰击你；查看他们施加在你身上的每一种效果的提示”。现译增补“测试一下这些持续效果”，并把 each effect 弱化为泛泛的“注意查看鼠标提示”，教程指令精度下降。改为“他们会很乐意用手头的任何法术轰击你。查看他们施加在你身上的每一种效果的鼠标提示。”末尾两个换行不变（claim 2 确认）。 |
| hrq-00407 | entry-02541 | mod-tome.lua:33605 | fix | accepted | 是 | 独立核验通过；采纳：原文 "lifted" 带引号，成就显示实为杀死 Ben Cruthdar，引号承载反讽；“战胜了……的诅咒”平化了该语气。改为“你“解除”了本·克鲁塞达尔的诅咒”。Gloom／hate 等映射确认无误，标签不变。 |
| hrq-00408 | entry-02545 | mod-tome.lua:33711 | fix | accepted | 是 | 独立核验通过；采纳：A delight for the audience, a source of wealth and glory 为同位描述，现译“为了取悦观众，获得财富和荣耀的地方。”变成目的状语且无主句，是残句。改为“它令观众欣喜，是财富与荣耀之源。”advisory 驳回：“哦！”与“尽情砍杀吧！”属文风。末尾无额外 #WHITE# 与源码一致。 |
| hrq-00409 | entry-02552 | mod-tome.lua:33838 | fix | accepted | 是 | 独立核验通过；采纳：“达到目的法师”漏定语标记“的”，是明确语病，改为“达到目的的法师”。Grand Corruptor／Fearscape／Vim 专名与标签确认无误，不扩改。 |
| hrq-00410 | entry-02555 | mod-tome.lua:34022 | fix | accepted | 是 | 独立核验通过；采纳：“之一 !”与“特点 :”为半角标点，改为全角“！”“：”；“玩的愉快，死的开心”中补语标记应为“得”，改为“玩得愉快，死得开心”。#WHITE# 后空格属贴字静态排版，不改。难度与模式映射确认正确。 |
| hrq-00411 | entry-02557 | mod-tome.lua:34056 | fix | accepted | 是 | 独立核验通过；采纳：“学会了如何……的能量方法”混用“如何……”与“……的方法”两种句式，是语病；原文 learned to harness 删去“方法”即可，改为“学会了如何同时掌控光与影的能量。”核心语义与标签确认一致。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
