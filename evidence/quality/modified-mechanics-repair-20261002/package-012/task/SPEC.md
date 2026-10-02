# 机制修正第012包

schema5 implement standard translation_contextual_v2；max_cycles3。仅冻结REPAIR-INPUT的10条target/10个原confirmed claim；允许文件：mod-tome.lua, tome-ashes-urhrok.lua。用户已恢复连续修正，不需逐包批准。原audit的automatic_fix_authorized=false仅指当时只读阶段；本修正范围由SCOPE.md明确授权，不追溯改旧记录。

UPSTREAM049：Commander of the Dead callback排除ab.no_energy==true瞬间法术，说明Upon spell cast与旧新译未限定非瞬间。
UPSTREAM073：Madness解锁文本写区域等级+150%+6，固定descriptor2.5倍+2且到玩家10级才完全生效。
UPSTREAM015：BLOODCASTING英文声称生命替代活力；固定Actor实际先付现有活力，只有不足部分转换生命。
UPSTREAM113：FieryGrasp原文startingfromlevel4，代码doSilence严格TL>4，不在等于4时触发。
MMR-UPSTREAM-001：显示声称至多1+ceil(level/2)个飞弹；实现while nb>0但nb从未递减，目标列表逐个移除直到空。
MMR-UPSTREAM-002：恶魔种子说明%d%%恢复生命；updateSeed实际调用demon:heal(getHeal)，传的是绝对治疗量。
MMR-UPSTREAM-005：英文感知3回合，action EFF_SENSE4，旧新中文4符合源码。
MMR-UPSTREAM-007：英文吸收燃烧半径5，而action半径10；旧新中文10符合实现。
MMR-UPSTREAM-006：回血每回合至多1的英文与旧新中文限制不存在于DEMONIC_CUT回调。
MMR-UPSTREAM-008：英文描述可变爆炸半径%d，action实际固定3，%d用于knockback dist。

EXECUTOR唯一内容写入；先逐字核对baseline。只改对应target，保留source/source_tag/args_order/special、placeholder种类顺序、markup、newline/tabs及其余字节；保留之前各包修正及用户改动。技能数值placeholder按现行strict lint保留ASCII分隔空格。实际机制以固定core commit624a67329fe2ad440c5b344785a9c73fcf22ae63和可核验DLC快照为准；DLC来源/commit未固定时如实标注。沿计算→实参→消费者核验，不机械采信finding；无法唯一证明则报告pending，不擅自用文本宣称游戏实现已修好。占位符是错误显示值时明确显示值与实际机制的区别，避免作无证据数值保证。

不改游戏源码/术语库/共享工具/角色/.ai/旧evidence/用户文档，不stage/commit、不创建child。只可写允许Lua的冻结target、自己的/tmp，以及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-012-report.json。需要术语库/跨批策略时报告，不越权。

报告包含完整旧新target、固定源码路径commit/hash/精确摘录、每个placeholder index/quantity kind/计算→消费链、范围逆向字节证明、测试和未解决项。验收：strictlint/proposal、全部字段及字节不变量、源码消费者核验、runtime collision/分类、空白、strictcoreaddon及真实DLC publish dry-run（不apply），独立whole-workset REVIEW/full→必要FIX/RE_REVIEW→FINAL_REVIEW/full、全部child归档、DONE_VERIFIED及本包译文/evidence提交。采用≤10条whole-workset full，n>=4不强制四lane。无push/PR/发布授权。

验收补充：这是10条有界核验，不强制10条都产生diff。若现译已准确体现源码（尤其1035感知4回合、1039半径10、1052固定爆炸半径3及动态击退距离），须保留现译并报告逐项源码证据/无修改理由；不得为制造diff而改写。全10条仍进入冻结独立复审。
