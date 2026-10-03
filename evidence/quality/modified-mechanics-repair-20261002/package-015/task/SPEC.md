# 机制修正第015包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM126：反击受src.turn_procs.metatemporal_spinner_retaliate限制同攻击者每turn1且dam>0，英文anysuccessfulmelee未限定。
UPSTREAM052：Grinding Shield近战减伤实际按src距离<=1判断，近处非近战伤害也减；maxLife伤害cap按每次DefaultProjector伤害调用截断，不能保证复合一击所有元素总伤害不超该值。
UPSTREAM066：Tempest of Metal只有成功近战命中且每turn一次才追加攻击；每次攻击说明缺条件。
UPSTREAM021：Overcharge Saws说明称有效技能等级增加power%，实际给四树mastery加power/100；固定effectiveTL=rawTL*mastery，原mastery非1时相对增加不等于power%。
UPSTREAM053：Dazzling Jump英文all creatures半径3减速，但实际ball设置friendlyfire=false，排除友军。
UPSTREAM033：%d%% chance to avoid being critically hit/几率避免暴击沿用英文，但ignore_direct_crits按比例削減crit power额外部分，不进行rng判定。
UPSTREAM127：Molten Metal触发条件getSteam()>15而cleanActor耗15，正好15不会触发；stack10时本次不触发而之后伤害callback才检查。
UPSTREAM128：修复只在steamtech技能post且ab.steam存在时按定义cost，未覆盖维持drain或非该系steam消耗；英文eachtimeyouspendsteam过宽。
UPSTREAM038：Flamethrower的范围5和不会落空与当前可核验实现不符：FlameJet cone半径steamgun_range，固定Archery仍作checkHit；phasing没有绕过命中。
UPSTREAM129：Stormstrike localhit取attackTargetWith首返回speed，非hitted；未命中也施STORMSTRIKE。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-015-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

FIX cycle1：同一火焰喷射entry补充FIREBURN默认一半即时、一半3回合燃烧的客观时序；仅FIX-1.json指定target一句，其余9条、格式和source identity不变。

FIX cycle2用户裁决：直接删除熔点烧伤免疫整行，不加替代句。FIX-2.json唯一target的新文本为准；明确授权该一行连同一个换行及两个tab的删除，其他格式/source/args/9条target不变。该用户决定覆盖原newline/tabs不变要求的这一处；report可写executor-015-fix2-report.json。

FIX cycle2最新用户裁决覆盖此前删除方案：保留风味，将保护限定为此次高温。只按FIX-2-FLAVOR.json逐字替换一条target中的一句；不删行，全部newline/tab/placeholder/markup及其余9条保持。前一删除dispatch已取消且无改动；fresh fix-2-a2执行。允许报告executor-015-fix2-flavor-report.json。
