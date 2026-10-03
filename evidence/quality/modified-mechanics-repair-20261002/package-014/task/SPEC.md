# 机制修正第014包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：tome-cults.lua, tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM030：WrithingOne写入ignore_direct_crits，固定消费者按百分比减额外暴击伤害；说明却称有%d%概率无视暴击，未使用概率判定。
UPSTREAM119：Tendrils Eruption把attackTargetWith首返回值用于hit；Combat首返回combatSpeed而非第二hitted，因此目标存在但攻击未命中也会设置hit、获得疯狂；麻木检定也未以hitted为条件。
UPSTREAM120：SPLIT callbackOnHit保留cb.value*eff.resist/100；resist=80-modifier，显示却称减伤该百分比，方向互补。clone inc_damage.all减100-(40+modifier)也不是对原伤害乘该比率。
UPSTREAM123：两次LOS扫描均在自身召唤物时seen=false，其他actor时true；后遍历召唤物能覆盖此前目击者，且召唤物自身豁免anyothercreature限制。
UPSTREAM023：ForbiddenTomeHome阅读警告声称5回合，物品book_change_timeout=3并由dialog直接用于CULTS_BOOK_TIMEOUT，自然到期转换书区。
UPSTREAM069：Lunar Orb按路径非本人及非本人召唤物actor结算伤害/负能量，包括友方；不是只敌人。
UPSTREAM124：Twilit Echoes campaign doEcho仅Light/Dark>=1但无来源self过滤；英文your限定过窄。ECHOED_LIGHT初始power=dam*.001未cap，只有merge才min(max)。
UPSTREAM050：Plasma Bolt显示moveSlow=slow*neg，talentSlow=slow*.6*(1-neg)，实际LIGHT_DARK在dark/light damage>0时分别完整slow和slow*.6持续5turn，没有按能量比例缩减。
UPSTREAM062：Starscape设置ZERO_GRAVITY effect但不设置level.data.zero_gravity；效果自身只加负重，不减速。movement consumer依赖level flag；STARSCAPE也没有其他三倍slow字段，投射物实体只外围冻结而内部不减速。
UPSTREAM125：Mindwave target type=ball、自身中心radius5，英文cone。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-014-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

2026-10-03用户已批准拆为9＋2条（USER-DECISION-SPLIT.json）。原REPAIR-INPUT.json只作初始历史，现行主包输入为REPAIR-INPUT-SPLIT.json／SCOPE-SPLIT.json（9条），暮光回响UPSTREAM124交独立2条companion；本次EXECUTOR仅按REPARTITION-0.json撤回暂存暮光target并校准读书倒计时文案。报告允许写.artifacts/i18n/modified-mechanics-repair-20261002/executor-014-repartition-report.json。完成后主包不得保留暮光改动；其余原权限不变。


FIX cycle1范围校准：按一级缺陷reopen规则接受同一原entry的客观关系问题：apply_power用于检定，不是35%混乱强度。仅对一条target做FIX-1逐字澄清，格式/source/args不变量及9原keys/source identity保持，游戏源码和工具不变。非术语库/全局策略扩张。

FIX-1执行报告允许写 .artifacts/i18n/modified-mechanics-repair-20261002/executor-014-fix1-report.json；仅一条Mindwave的末句澄清，其余9条主包及2条待修副本边界保持。
