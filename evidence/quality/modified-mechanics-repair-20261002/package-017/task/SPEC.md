# 机制修正第017包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM070：Voltaic Sentry info20..100按创造者蒸汽强度，实际Bolt20..350按召唤物蒸汽强度；未设置damcloud覆盖。
UPSTREAM067：Incendiary Shell实际放置搜索radius3，英文和旧新都写radius2。
UPSTREAM137：MOSS_TREAD只有callbackOnMove且moved/notforce调用铺苔藓，没有站立每turn回调，英文walkorstand。
UPSTREAM064：Arcane Dynamo按照activated spell声明mana费用增steam，排除有steam字段技能，不依据实际扣除mana（cost调整/减免/零消耗）。英文per mana spent及旧新每消耗描述过宽。
UPSTREAM138：Bloodstream只改EFF_CUT而非所有bleeding；cut.power乘getDamage/100，而info声称按getDamageInc增加，其函数不同且增加应1+。
MMR-UPSTREAM-004：英文与中文写减速4回合，action设EFF_SLOW5。
UPSTREAM139：FlameVortex半径实际3+eff.range/2，Upgrade展示第六值range；当range2实际4显示2。
UPSTREAM140：spawn findFreeGrid半径5并非必相邻；GUARDIAN_SHIELD施友方无guardian过滤，消费者只排src==self，因此其他guardian也可分担。
UPSTREAM013：无人机 NPC desc 仍称160%奥术伤害，实际回调和技能info均130%。
UPSTREAM141：Dynamo只在is_spell/ab.mana/notab.steam/activated时增加蒸汽，不是任意消耗法力；SP=steam*.8-20，steam<25负加成。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-017-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。
