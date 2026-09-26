# 窗口33 FINAL 记录的 attempt 更正

v2 契约第四节规定 terminal 坐标为 `(cycle,attempt,member_ordinal)`，stage key 为前两维且必须唯一。
宿主把 FINAL_REVIEW(3) 与 FINAL_REVIEW(5) 按 attempt 1 发布（`publish.py FINAL_REVIEW 3 1`／`5 1`），
与同 cycle 的 RE_REVIEW(3) r3a1、RE_REVIEW(5) r5a1 坐标重复，`ai_state_check --target DONE` 报
`v2 terminal three-dimensional coordinates must be unique`。窗口32的做法是同 cycle 的 FINAL 用 attempt 2（f3a2）。

更正：`.ai/reviews/repair-w33-20260926/f3a1.json` 与 `f5a1.json` 的 `attempt` 由 1 改为 2（原字节保存在
`attempt-renumber/`），其余字段不动。dispatch_id `f3a1`／`f5a1` 是 child 创建时的真实 label，保持不变；
raw 输出、envelope、candidate identity、agent/lineage 均未变。更正后 `ai_state_check --target DONE` 为 `DONE_VERIFIED`。
驱动 `wd_freeze` 以后对同 cycle 的 FINAL 须传 attempt 2。
