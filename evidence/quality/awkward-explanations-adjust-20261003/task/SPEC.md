# 生硬解释有界调整

用户要求调整刚交付扫描清单。范围16条：13条英文外机制扩写撤回采用，3条普通措辞精简；4条排除项不动。按CHANGES.json精确old_target→new_target落实。此次不重新判定游戏机制，不重开机制审查；以英文为描述边界，保持已确认普通翻译修正。历史证据不改写。

mode=implement; change_class=standard; schema5; max_cycles3; review_contract=code_legacy_v1。本任务沿用上一撤回任务的恢复完整性审查：核验明确授权的子句删改及raw diff/字段不变量，不作为新的游戏机制或正式生产语境审核。待核对英文与修改后target随CHANGES提供。

唯一EXECUTOR只可写SCOPE四个Lua的这16个target、自身/tmp、.artifacts/i18n/awkward-explanations-adjust-20261003/executor-report.json与CLI默认派生目录。禁止修改其他target、source、tag、args_order、special、术语、工具、规则、evidence/.ai、用户文档或外部仓库；禁止stage/commit/child。

需要时只允许按strict lint要求调整数字附近ASCII空格，须记录；除此之外任何偏离CHANGES均先报告。占位符序列、markup序列、decoded换行数必须保持。SCAN14通过重新分行保持原换行数，合并注句但保留英文mind-only限制。SCAN05英文同一百分比作用于两类持续时间，保持单placeholder，不增删数值。基线已有用户文件保持。

验收：精确16条与授权措辞、目标外字节及非target字段不变、strict lint、运行键冲突与分类、严格核心addon、DLC实际消费者dry-run、独立范围复审和终审、child归档及DONE检查；本地提交对应证据。无push或发布授权。
