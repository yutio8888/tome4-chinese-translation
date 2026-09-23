# 执行顺序

1. 冻结 series-group-12 的40条、十五个 section 上下文、术语子集、固定源码、统一 INPUT；记录基线及 SHA-256。
2. 逐次 live list_profiles，按用户指定精确模型发现可用路由；最多三路参赛者同时运行，Gemini 始终只有一路。相同输入 prompt，不透露其他臂。
3. 每次完成先收获原生最终回复、核验全40覆盖及只读守卫，再持久化 archive_attempts_started、archive、live archivedAt 确认。不续跑终态 child。
4. 不参赛 REVIEWER 全40盲审，冻结后 fresh REVIEWER 核验匿名 claims 并显式裁决每条；建立暂定参考。
5. 机械转录并交叉核对 claim 对应、分母、正确率和误报/漏报；交付 RESULT 与本实验 HANDOFF，原 campaign STATE 不变。

旧 campaign 两个未闭合记录不由本试验收养：live 为 closed/attentionReason=finished、archivedAt=null，父级 a2361362；没有按旧字段 running 判为挂起。既有报告和未提交修改均保留。本实验使用新 task_id 与当前直接父级。

本轮用户授权继续实验、使用未复核译文并归并三模型问题。沿用40条规模。临时文件允许，仓库和冻结输入只读；归并包括去重、源码核验、分歧状态和模型来源，不自动修改译文或更新生产覆盖。无参赛输出前预注册。

本组属于用户授权累计20组；完成后自动推进。来源规则以本组INPUT和source-access为准：本体固定commit，DLC快照commit未固定，缺源码机制项pending。40条可能跨旧生产batch边界，绝不复用已审条目。
