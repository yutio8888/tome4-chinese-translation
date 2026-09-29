# B3：独立反证核验（只读研究）

你是 REVIEWER，purpose=translation_contextual_v1。本次只读 A/B 研究，非生产 contract，不宣称 DONE_VERIFIED，不写文件、不创建子 agent。

先读 RULES.md。唯一文字输入：本文件、RULES.md、entries.json、context.lua、terms.json、source-access.json、FREEZE.json、B3-FREEZE.json、reports/P.md、reports/B2.md。源码只按 source-access.json 及已读调用的获准链核验。禁止读取 A2 报告、宿主记录、SPEC、结果统计、其他实验或仓库全量搜索。

任务：对 P 与 B2 两份报告的每一项候选观察，独立寻找其最强反证，并回到完整条目/相关分支及必要调用核验。候选报告不是事实；也不能为了“反证”强行撤销真实问题。不重做一次全量发现审查，按候选及其语境工作。可用脚本按 entry-ID 提取完整原译，避免无目的读入全部 context.lua；引用语境与源码必须真实核对。

输出：

1. 逐候选映射表，保留来源前缀 P:C01、B2:C01 等，覆盖原报告所有编号，包含 advisory/pending。复合候选必要时分为 .1/.2 子项；原编号仍须可回溯。逐项写 confirmed / pending / advisory / refuted，并给短理由。重复候选标共享 K 编号，但不可从映射中删除；表外未编号但带具体疑点的观察另建 U 编号，说明来源。
2. K01… 去重结论表：每项包含 entry-ID、精确原译短引、具体意义变化、最强反证与处理、所用证据路径/行号、text_status / snapshot_fact / target_applicability / impact。仅仅“不影响机制”不构成撤销叙事事实偏差的理由。仅仅“不是逐词对应”也不构成确认理由。规则第5条用户定标不得重开。
3. 对全部40条给最终 entry-ID | ISSUE/PENDING/OK 表：依据核验后保留的本臂候选；对无候选条目写“本臂无保留候选”，不要伪称你重新全量盲审过。
4. 核验过程中偶然新增发现独立标 NEW01…，不能冒充原候选被保留；禁止读取未分配的其他仓库条目。
5. 列实际读取文件、证据不足的限制。直接一次返回完整报告，不只回计划。

不要给审核者/流程打分，也不要推测其他臂会发现什么。保持判定与证据紧凑且可追溯。
