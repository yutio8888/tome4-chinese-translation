# 机制修正第013包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：tome-ashes-urhrok.lua, tome-cults.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

MMR-UPSTREAM-010：Voracious Blade加100点物理暴击率，固定physicalCrit仍减目标暴击率削减，未设置auto_phys_crit；必定暴击有例外。
MMR-UPSTREAM-009：Destroyer info冷却缩减ceil(dest/3)，实际Draining Assault使用ceil(dest/2)。
MMR-UPSTREAM-011：Demonologist解锁文案仍用Corruptors远程法师概述，出生职业说明及配置为melee shield fighter。
UPSTREAM114：Jinx失去LOS在连续第二次timeout即fading>=2移除，文案morethan2表示超过两回合。
UPSTREAM115：Tongue did_hit仅hit且target.canBe(disease)设置，命中疾病免疫目标不会增加insanity，原文声称至少命中1敌即gain。
UPSTREAM059：Prophecy of Treason实际随机初timer后以power累加，>100才攻击且SpellSave可把累加减半，并非每turn独立power%机会。
UPSTREAM039：Power Overwhelming反冲条件实际还要求self.in_combat，英文与旧新译每次非瞬间法术漏战斗内限定。
UPSTREAM022：FoulConvergence显示WTW Blindside冷却减少getBlindside，更新宠物写talent_cd_reduction=1+getBlindside；固定消费者直接减该字段，实际基础冷却减值比显示多1。
UPSTREAM117：Nihil候选只检查半径10和reaction<0，没有canSee/LOS，英文称youcansee。
UPSTREAM026（本轮消费者核验已校准）：NIHIL回调计算eff.numb*负面魔法效果数量nb，但固定Actor.takeHit在伤害结算后调用且忽略返回值，实际不施加该减伤。译文须保留显示系数placeholder并说明未生效；按负面魔法数量追加时空伤害保留。详见HOST-CONSUMER-CALIBRATION-013.json。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-013-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

首次独立复审前补完：fresh EXECUTOR按COMPLETE-0.json精确修改1054/1191两处，报告写入.artifacts/i18n/modified-mechanics-repair-20261002/executor-013-complete-report.json；其余权限不变。

补完后的严格lint错误已归因：EXECUTOR仅按SPACING-0.json补充Erase占位符后的ASCII空格，报告写入.artifacts/i18n/modified-mechanics-repair-20261002/executor-013-spacing-report.json；不涉及机制重审或新修复轮。
