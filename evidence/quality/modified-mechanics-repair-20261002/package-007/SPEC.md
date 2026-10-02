# 机制修正第七包：时空、疾病与诅咒触发条件

schema5 implement standard translation_contextual_v2 max_cycles3。仅REPAIR-INPUT的10条10原confirmed claim，允许文件 mod-tome.lua，只改对应10个target。唯一EXECUTOR内容写入。原只读audit里的automatic_fix_authorized=false反映当时审查边界，本次用户修正请求已授权这些confirmed修复，不追溯改旧审查记录。

接受问题：REPAIR-INPUT中10个confirmed claim：Time Shield只缩短负面非other效果；Temporal Hounds按既有counter补召；Virulent Disease三回合触发间隔；Blinding Powder友方范围；Blade Flurry每回合最多一次且命中；Scoundrel Strategies仅一个可用技能时不触发CD；Shadowstrike嵌套目标属性条件；Harass Prey未定义cooldown变量导致无所述CD；Heighten Fear提示与实际完整伤害差异；Deflection耗仇恨的伤害条件。机制以固定core/可核验DLC快照调用链为准，DLC来源未固定必须记录。沿计算→实参→消费者验证，不把源码上游描述误差保留在机制中文里。

保留source/source_tag/args_order/special/placeholder种类顺序/markup/newline/tabs和其余所有target/字节，前六包及restorative修正须保留。不改术语库、游戏源码、工具、.ai、旧evidence或用户文件，不stage/commit、不创建child。只允许自己的/tmp及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-007-report.json。超范围或源码推翻claim时报告，不自动扩张。

验收：strictlint/proposal、范围字节及全部非target字段不变量、固定源码与DLC hash、runtime collision0/分类、空白、strictcoreaddon及实际受影响DLC dry-run consumer；full独立REVIEW、必要FIX/RE_REVIEW及最终whole-workset FINAL_REVIEW，所有child归档、DONE_VERIFIED/evidence提交。n>=4可full，本包采用whole-workset full≤10条/24000字符，不要求不合规的立即启动四lane。

FIX cycle1：同两条冻结target澄清Shadowstrike脱离潜行的通用暴击加成，以及Heighten Fear实际使用Instill Fear等级、5回合窗口；属于可源码判定的一级消费者关系缺陷，不扩大术语或代码范围。逐字应用FIX-1，保持全部格式不变量。
