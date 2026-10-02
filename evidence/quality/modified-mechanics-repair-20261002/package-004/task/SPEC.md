# 机制修正第四包：DLC物品与自动装置机制

schema5 implement standard translation_contextual_v2 max_cycles3。仅REPAIR-INPUT的10条10原confirmed claim，允许文件 tome-cults.lua, tome-orcs.lua，只改对应10个target。唯一EXECUTOR内容写入。原只读audit里的automatic_fix_authorized=false反映当时审查边界，本次用户修正请求已授权这些confirmed修复，不追溯改旧审查记录。

接受问题：REPAIR-INPUT中10个confirmed claim，包括熵反冲治疗窗口、Magic魔力属性、技能失败限定、射线锥形中心、实际物理暴击消费者、全局速度和飞爪半径。机制以固定core/可核验DLC快照调用链为准，DLC来源未固定必须记录。沿计算→实参→消费者验证，不把源码上游描述误差保留在机制中文里。

保留source/source_tag/args_order/special/placeholder种类顺序/markup/newline/tabs和其余所有target/字节，前两包及restorative修正须保留。不改术语库、游戏源码、工具、.ai、旧evidence或用户文件，不stage/commit、不创建child。只允许自己的/tmp及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-004-report.json。超范围或源码推翻claim时报告，不自动扩张。

验收：strictlint/proposal、范围字节及全部非target字段不变量、固定源码与DLC hash、runtime collision0/分类、空白、strictcoreaddon及实际受影响DLC dry-run consumer；full独立REVIEW、必要FIX/RE_REVIEW及最终whole-workset FINAL_REVIEW，所有child归档、DONE_VERIFIED/evidence提交。n>=4可full，本包采用whole-workset full≤10条/24000字符，不要求不合规的立即启动四lane。

FIX cycle1：仅FIX-1冻结的召唤吞噬者条目将轮改回合，其他9条不变。允许报告executor-004-fix1-report.json。毒箭顺序finding经fixed I18N.default_tformat真实LuaJIT执行撤销，保留args_order与target。

FIX cycle2：FIX-2冻结原熵杖entry仅写实际10回合并将第一%d保留为时长提示值，以fixed/冻结实际消费者优先。其他9条/placeholder/source/args保持，禁止游戏源码和工具变更。允许executor-004-fix2-report.json。
