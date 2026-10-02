# 机制修正第010包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：mod-tome.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM031：Biofeedback说明反馈衰减每回合最多newDecay百分比，实际getFeedbackDecay=max(1,feedback*mult/10)，有最低1点。
UPSTREAM025：反馈增幅说明宣称反馈获得受Mindpower缩放；实际getFeedbackGain仅技能等级，基础getFeedbackRatio仅角色等级，受击消费者直接乘ratio。
UPSTREAM044：Beyond the Flesh ranged分支英文和旧新译把Will/Str对应命中、Cun/Dex对应伤害（respectively），固定Combat实际Cun代Dex用于Accuracy，Will代Str用于伤害。
UPSTREAM102：Dreamscape投影inc_damage.all减50个百分点，并非独立乘.5；本体已有100%增伤时，投影150%/本体200%=75%，而不是50%。
UPSTREAM103：Bowman技能配置包含T_AIM，没有RapidShot；英文及旧新说明称learn Rapid Shot。
UPSTREAM037：Fiery Hands末句effects随Spellpower提高过宽：体力回复实际只getTalentLevel/3，Combat和Archery命中均消费该值。
UPSTREAM105：禁止自行击杀触发的killer条件被注释；Actor无条件发送召唤死亡callback，因此文案neverworkswhenyoukillownminions与实现不符。
UPSTREAM018：等级5设置auto_melee_hit前，Combat攻击结算仍先处理抵消和checkEvasion，因此cannot miss/必中不能排除躲闪。
UPSTREAM017：Congeal Time全局速度显示百分比与真实组合不符：显示100*s，action传s/(1+s)，负global_speed_add最终按倒数缩放。
UPSTREAM107：RapidShot能量返还限制写在target.turn_procs中，逐个不同目标可各触发一次；效果RAPID_MOVEMENT实际dur1而文案2turn。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-010-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

cycle1 FIX补充：fresh EXECUTOR仅按FIX-1.json逐字修正2个target，其余8条不变；本次允许独立报告 .artifacts/i18n/modified-mechanics-repair-20261002/executor-010-fix1-report.json。原报告/冻结envelope/raw保持。参考HOST-RAPID-TIMING-010.json解释撤回dur1=玩家1回合的推断，保持全局max_cycles3预算。
