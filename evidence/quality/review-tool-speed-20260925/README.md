# 工具耗时优化验收快照

Astra 与 Sol 独立复审均 PASS；所有 child 已确认归档；STATE 通过 DONE_VERIFIED。

缓存 on/off 的真实 17 项门禁（含 doctor 与严格 build）均通过。冻结候选、实现基线、复审原文及门禁回执按原相对路径归档。门禁 tool_commit 为修改前 HEAD，候选由 worktree 指纹及冻结清单绑定。

三对无缓存完整重放：中位 251.99 → 87.58 秒，RSS +13.53%；六样本 identity/progress 相同。不是完整生产批次端到端测量。

完整冻结输入保存在 acceptance.tar.gz；SHA256.json 为解包后逐文件摘要。归档 SHA-256：`598a34d439d40f1faa0ff076127899a9510e38d082a0a79be2970e92c99b53d7`。保留 patch 原字节，避免文本重排破坏候选身份。
