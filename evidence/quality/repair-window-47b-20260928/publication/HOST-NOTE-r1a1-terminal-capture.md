# 宿主说明：r1a1 终端快照重建

宿主在 r1a1 完成后误以占位时间戳（lastUserMessageAt、attentionTimestamp 为 "x"）调用了一次 `wd_rev_done`。harvest 只读原生会话日志：原生 provenance、raw 输出与 SHA 均来自原生日志，output_valid=True，未受占位值影响；受影响的只有 `r1a1-terminal.json`。宿主随后按 get_agent_status 的实时字段（updatedAt 2026-09-28T07:01:49.631Z、lastUserMessageAt 06:59:05.237Z、attentionTimestamp 07:01:49.630Z）重建该快照，确认文件中不再有占位值，再重跑原生审计（audit=0、10 次工具调用、0 flagged），然后才写 archive-intent 并归档。
