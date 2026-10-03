# 机制修正第014-companion包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的2条target/1个原confirmed claim及1个用户批准同键副本；允许文件：tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM124：Twilit Echoes campaign doEcho仅Light/Dark>=1但无来源self过滤；英文your限定过窄。ECHOED_LIGHT初始power=dam*.001未cap，只有merge才min(max)。
LOCAL-COMPANION-014：用户明确批准将相同runtime key的void副本一并修正，二者target必须一致；包括所有来源>=1光暗伤害、初次光减速不封顶、暗影初次4回合而刷新至3且仅剩余0<duration<3并受暗影伤害时刷新。DLC来源未固定。

用户明确授权见 evidence/quality/modified-mechanics-repair-20261002/USER-DECISION-014-SPLIT.json。还须核验ECHOED_LIGHT.on_merge只更新power并返回old_eff，固定ActorTemporaryEffects.setEffect合并路径不重置old.dur，故已有光减速叠加不刷新时长。必须独立核验暗影初次4回合、刷新条件与剩余伤害合并，不得仅复制旧的错误dark段。对应数值探针记录可读 .artifacts/i18n/modified-mechanics-repair-20261002/host-twilit-probe-014.json。两个target最终须完全相同；保留7个占位符顺序，合理阐明第6个值为刷新时长而非初始时长。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-014-companion-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。
