# 机制修正第三包：条件与承受对象

schema5 implement standard translation_contextual_v2 max_cycles3。仅REPAIR-INPUT的10条10原confirmed claim，允许文件 mod-tome.lua, tome-ashes-urhrok.lua，只改对应10个target。唯一EXECUTOR内容写入。原只读audit里的automatic_fix_authorized=false反映当时审查边界，本次用户修正请求已授权这些confirmed修复，不追溯改旧审查记录。

接受问题：Stalk连续两turn近战命中；Dominate与通用Defense使用闪避属性；注射亲和基数写抗性减免前不能扩为所有伤害减免前；傀儡明确近战攻击伤害类型；闪电新星眩晕受影响单位可含友方；Quickdraw只近战命中触发；被诅咒者光环可能而非必然；疫火弹描述Magic stat用魔力；Incinerating Blows近战命中才触发燃烧/火焰爆发。机制以固定core/可核验DLC快照调用链为准，DLC来源未固定必须记录。沿计算→实参→消费者验证，不把源码上游描述误差保留在机制中文里。

保留source/source_tag/args_order/special/placeholder种类顺序/markup/newline/tabs和其余所有target/字节，前两包及restorative修正须保留。不改术语库、游戏源码、工具、.ai、旧evidence或用户文件，不stage/commit、不创建child。只允许自己的/tmp及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-003-report.json。超范围或源码推翻claim时报告，不自动扩张。

验收：strictlint/proposal、范围字节及全部非target字段不变量、固定源码与DLC hash、runtime collision0/分类、空白、strictcoreaddon及实际受影响DLC dry-run consumer；full独立REVIEW、必要FIX/RE_REVIEW及最终whole-workset FINAL_REVIEW，所有child归档、DONE_VERIFIED/evidence提交。n>=4可full，本包采用whole-workset full≤10条/24000字符，不要求不合规的立即启动四lane。


FIX cycle1范围校准：按一级缺陷reopen规则接受同两原entry的客观关系问题：亲和伤害结算后另行治疗且两效果共用duration；Dominate实际闪避减免等于护甲，但第三info参数为不同提示值。仅对两target做FIX-1逐字澄清，格式/source/args不变量及10原keys/source identity保持，游戏源码和工具不变。非术语库/全局策略扩张。

FIX cycle1格式收尾：FIX-1-SPACING.json只增加一个ASCII空格。允许报告 executor-003-spacing-report.json；原FIX-1与失败lint证据保持不变。

FIX cycle2：FIX-2.json仅同一Stalk条目补回命中/近战伤害增益对该猎物的限定，统一层数计数；其余9条及格式/source不变量保持。允许报告executor-003-fix2-report.json。
