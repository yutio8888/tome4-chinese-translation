# 修正流程恢复入口

已按用户“请你发起修正流程”启动连续修正；169 confirmed claim 对应166条，18个有界包。范围见SCOPE.md，首包3条明确回归。尚未完成，不计任何包DONE。

活动task `.ai/task/mmrfix-20261002-001/STATE.json`，MCP传输；当前EXECUTOR `67c54973-045d-4365-a39e-f901fb301e9e`，dispatch `execute-0-a1`，已经live核验direct lineage/workspace/role。唯一内容写入者。报告预期 `.artifacts/i18n/modified-mechanics-repair-20261002/executor-001-report.json`。不得poll；收到结束通知后读取get_agent_status并核验activeTurn/attention、原生终稿和实际diff。自然结束收获后，先持久化archive_attempts_started，再软归档并readback确认；不send follow-up。若无产出，归档后fresh retry，连续两次无产出按AGENTS停止。

下一步：检查3条target及不变量、原源码value-flow；冻结中性contextual v2 envelope和preflight（旧finding只给EXECUTOR，绝不进入reviewer输入）。n=3使用REVIEW/full cycle0，收敛后再fresh FINAL_REVIEW/full；n>=4后续包用四lane初审及whole FINAL_REVIEW。新状态schema5 implement、max_cycles3。review_lifecycle.Journal和close_review_tasks.publish仅支持review_only，不能直接用于本任务；可以使用其中strict result/native final/身份函数，但须正确保存implement阶段与终态，最终由ai_state_check校验DONE_VERIFIED。

适用检查：strict proposal/lint，source/tag/args/special/placeholder/markup/newline不变量，runtime collisions/classification、空白、受影响组件严格build；数值动态展示与固定消费者核查。不得修改旧审查evidence、用户脏文件、术语库（无新全局策略授权）、共享工具/角色或游戏源码，不push/PR/发布。pending/advisory保留。程序按packages.json排队推进；范围受阻时完成不依赖项并按规则记录。
