# 机制修正第018包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的3条target/3个原confirmed claim；允许文件：tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM142：TwilitEchoes刷新只在DARKNESS且darkecho duration<echo_dur且>0，不是任意其他来源伤害均刷新。
UPSTREAM020：AUTOMATED_REPAIR_SYSTEM activate将eff.heal/resist/life写成addTemporaryValue返回的id；long_desc随后直接显示这三id，不能代表原治疗、全抗和负生命阈值。
UPSTREAM016：药膏效果说明把power/2显示成治疗系数百分比，实际临时字段加同数值倍率，未除100。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-018-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

全条目核验补充：上述3条完整target中的相关首施/刷新条件、显示参数与消费者量纲均属授权范围；额外源码定位见 .artifacts/i18n/modified-mechanics-repair-20261002/host-extra-source-018.json，不把宿主观察当作事实。
