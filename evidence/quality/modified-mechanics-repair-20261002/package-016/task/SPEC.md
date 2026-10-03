# 机制修正第016包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：tome-orcs.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM130：Corrosive Flechette通过MeleeHit/ArcheryHit且攻击者hostile才消耗一枚，英文每attack没有命中/敌对限定。
UPSTREAM131：DEBILITATING_ACID turn_procs计数<=6会结算六次dam*inc，info额外上限binc*5。
UPSTREAM132：StaticShock只为summoner=self且turret的召唤物施STATIC_SHIELD，英文minions未限定炮台。
UPSTREAM057：Overrun定义tg2为radius球但实际project(tg)使用原typebolt，嘲讽只该投射目标，不按显示radius作用全部敌人。
UPSTREAM133：PincerStrike localhit取attackTargetWith首返回speed，未命中也可能clamp（canBe pin成立）。
UPSTREAM134：BLOODSTAR当distance>=free即停止；英文morethantwice与中文超过均为>。
UPSTREAM027：Steamstar说明每追加受害者产汽减少66%，实际incSteam(steam*0.3^nb_done)使后续量为前一成功目标的30%，即递减70%。
UPSTREAM043：Fatal Attractor说明5回合，action NPC summon_time=8，NPCactBase每回合减1到0死亡，无5回合设置。
UPSTREAM136：rng.avg(1,steamCrit(dam),3)而info下限dam/3；ball未friendlyfire=false，附近友方也可能受电弧。
UPSTREAM054：Shocking Touch的tier只限制随机选中target数量；对每个连接使用beam，对路径格的其他actor仍投闪电，故命中敌人总数可超过tier。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-016-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

## 收束范围调整

宿主与EXECUTOR均核实UPSTREAM054的默认range=1反证，撤回“beam可令总命中数超过tier”的旧推论；entry1520已恢复baseline。保留原REPAIR-INPUT不变，当前实施/复审范围以REPAIR-INPUT-SPLIT.json的9条target/9个claim为准。该条pending移至包外holdout记录，不作为本次9条已接受修复，也不扩大到未验证的替代机制修订。SCOPE的允许文件/section不扩大，非目标字节验证须覆盖该条未变。

## 用户批准的有界扩展

用户于2026-10-03明确批准电击棒未命中击退一句修订，并额外授权一轮修复与全量复审。自此max_cycles由3前瞻调整为4，当前cycle4；只执行FIX-4该句及9条全量RE_REVIEW/FINAL与适用门禁。保留全部原周期/dispatch历史，不授权无限重试。成功后继续017/018。决定详见USER-DECISION-SHOCKSTAFF-KNOCKBACK.json。
