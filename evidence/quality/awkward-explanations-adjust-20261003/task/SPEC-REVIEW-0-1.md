# 生硬解释有界调整

用户要求调整刚交付扫描清单。范围16条：13条英文外机制扩写撤回采用，3条普通措辞精简；4条排除项不动。按CHANGES.json精确old_target→new_target落实。此次不重新判定游戏机制，不重开机制审查；以英文为描述边界，保持已确认普通翻译修正。历史证据不改写。

mode=implement; change_class=standard; schema5; max_cycles3; review_contract=code_legacy_v1。本任务沿用上一撤回任务的恢复完整性审查：核验明确授权的子句删改及raw diff/字段不变量，不作为新的游戏机制或正式生产语境审核。待核对英文与修改后target随CHANGES提供。

唯一EXECUTOR只可写SCOPE四个Lua的这16个target、自身/tmp、.artifacts/i18n/awkward-explanations-adjust-20261003/executor-report.json与CLI默认派生目录。禁止修改其他target、source、tag、args_order、special、术语、工具、规则、evidence/.ai、用户文档或外部仓库；禁止stage/commit/child。

需要时只允许按strict lint要求调整数字附近ASCII空格，须记录；除此之外任何偏离CHANGES均先报告。占位符序列、markup序列、decoded换行数必须保持。SCAN14通过重新分行保持原换行数，合并注句但保留英文mind-only限制。SCAN05英文同一百分比作用于两类持续时间，保持单placeholder，不增删数值。基线已有用户文件保持。

验收：精确16条与授权措辞、目标外字节及非target字段不变、strict lint、运行键冲突与分类、严格核心addon、DLC实际消费者dry-run、独立范围复审和终审、child归档及DONE检查；本地提交对应证据。无push或发布授权。

## 冻结复审输入

独立核对全部16条，既查精确实施又查英文边界，防止删除英文原有信息或引入漏译。旧译文原有问题不计本次缺陷；不重新判定游戏机制，不重新引入英文以外解释。

- 全量 source/before/after 及宿主范围证明：.ai/task/awkward-explanations-adjust-20261003/CANDIDATE-REVIEW-0-1.json，SHA256 `596bee250519f34dd72883478b59b565744ffc037e7e6be31a68dd1ed1678d3d`。证明是待独立核对的宿主 assertion。
- 授权改动逐条见 .ai/task/awkward-explanations-adjust-20261003/CHANGES.json。
- 任务diff：.ai/task/awkward-explanations-adjust-20261003/CODE_DIFF-REVIEW-0-1.patch。可复现：`git diff 31c93a100507f57dfa39628f11b76af7410f6386 -- mod-tome.lua tome-ashes-urhrok.lua tome-cults.lua tome-orcs.lua`。
- 允许只读以上输入、四个当前Lua及本任务baseline；不得浏览其他review/scan结果、写文件、运行产生报告的工具或创建child。
- normal_review输出每项恰为 ID / Severity / File / Location / Problem / Evidence / Impact / Recommended fix，severity仅 blocker|high|medium|low，末尾 VERDICT: PASS|CHANGES_REQUIRED。无finding仅输出 VERDICT: PASS。
