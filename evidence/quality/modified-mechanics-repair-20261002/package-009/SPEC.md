# 机制修正第九包：纹身、NPC与灵能消费者

schema5 implement standard translation_contextual_v2 max_cycles3。仅REPAIR-INPUT的10条10原confirmed claim，允许文件 mod-tome.lua，只改对应10个target。唯一EXECUTOR内容写入。原只读audit里的automatic_fix_authorized=false反映当时审查边界，本次用户修正请求已授权这些confirmed修复，不追溯改旧审查记录。

接受问题：REPAIR-INPUT中10个confirmed claim：两条Heroism到期不保证生命置1；Telepathy缺20%最大生命自伤；Blightzone显示/实际伤害公式不同；NPC Body Shot体力扣除非线性；Sticky Smoke视野降低不保证近身潜行；HideInPlainSight清AI目标不依赖潜行成功；Block抗性50%额外格挡输入未接通；StaticCharge需近战命中仍存活目标；Distortion次级爆炸降抗输入字段错位。机制以固定core/可核验DLC快照调用链为准，DLC来源未固定必须记录。沿计算→实参→消费者验证，不把源码上游描述误差保留在机制中文里。

保留source/source_tag/args_order/special/placeholder种类顺序/markup/newline/tabs和其余所有target/字节，前八包及restorative修正须保留。不改术语库、游戏源码、工具、.ai、旧evidence或用户文件，不stage/commit、不创建child。只允许自己的/tmp及 .artifacts/i18n/modified-mechanics-repair-20261002/executor-009-report.json。超范围或源码推翻claim时报告，不自动扩张。

验收：strictlint/proposal、范围字节及全部非target字段不变量、固定源码与DLC hash、runtime collision0/分类、空白、strictcoreaddon及实际受影响DLC dry-run consumer；full独立REVIEW、必要FIX/RE_REVIEW及最终whole-workset FINAL_REVIEW，所有child归档、DONE_VERIFIED/evidence提交。n>=4可full，本包采用whole-workset full≤10条/24000字符，不要求不合规的立即启动四lane。
