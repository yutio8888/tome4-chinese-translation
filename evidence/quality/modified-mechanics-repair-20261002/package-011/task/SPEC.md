# 机制修正第011包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：mod-tome.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM034：Headshot英文与旧新译均称只能对已标记单位，但action允许target已MARKED或施法者维持CONCEALMENT。
UPSTREAM061：Vitality固定源码只有setEffect(EFF_RECOVERY)引用，全game无RECOVERY效果定义；所声明8回合生命回复缺少可执行消费者。
UPSTREAM106：徒手攻击实际乘数dam_mult+1.25，显示tformat第二参数却为dam_mult*1.25；例如基础mult1时实际225%，显示125%。
UPSTREAM046：Crushing Hold说明额外效果不需抵抗检查，但固定Combat startGrapple明确canBe(silence)失败时silence=0，沉默免疫仍生效。
UPSTREAM108：AlloyedVenomous显示getPoisonRadius TL>=3为2，实际Venomous callback ball radius=1常量。
UPSTREAM109：Aim消费者把distance-3上限设为8，所以实际range11达最大8*dam，而info声称range8最大5*dam。
UPSTREAM110：TouchDeath四tick指数0/1/2/3，displaytotal却使用0/2/3/4，缺少一次1指数并多计4。
UPSTREAM028：ReflexDefense描述暴击倍率降低%d%，实际只降低超过普通伤害1倍的额外暴击部分：(crit_power-1)*percent。
UPSTREAM042：Battle Cry同一cone没有敌我过滤，BATTLE_CRY施于所有非self actor；英文/旧新称敌人漏友方影响。
UPSTREAM058：Irresistible Sun实际project ball friendlyfire=false排除友军，英文all creatures及旧新所有生物却声称全部被拉扯。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-011-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。
