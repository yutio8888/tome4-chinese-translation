# 原生 parser 版本维护（2026-09-23）

本机 Codex CLI 升至 0.156.0、Claude Code 升至 2.1.280，`review_lifecycle.py` 原先只接受
0.153.0 / 2.1.259，审核254的 `harvest --native-log` 因此失败（当批以版本替换副本 + `--raw` 绕行）。

改动：
- `CODEX_NATIVE_VERSIONS=('0.153.0','0.156.0')`、`CLAUDE_NATIVE_VERSIONS=('2.1.259','2.1.280')` 白名单；其他版本仍拒绝。
- Claude 会话内所有 `version` 必须一致（混用两个已核验版本也拒绝）。
- Claude 2.1.280 在 child 归档时于日志末尾追加一条 `cost-state`；只接受恰好一条、位于最后一行、sessionId 一致且不含消息字段。
- README 同步说明，并注明 Codex 归档后日志移到 `archived_sessions/`。

验证：
- `tests.i18n.test_review_lifecycle` 73 项通过（新增版本白名单、混用版本、cost-state 位置/身份负例）。
- 10 份真实会话（254 批 4×codex 0.156.0 + 1×claude 2.1.280；253 批 5×codex 0.153.0）用新 parser 解析，
  提取 bytes 与当初 harvest 的 raw SHA 全部一致，见 `real-log-check.json`。
- `tools/ci-gates.sh --skip-build` 16/16 通过（不改 addon 输出，按矩阵跳过构建），见 `gates-results.json`。

提交时机：审核254已 finalize、无活动批次；`production_review_v2_lite_batch.py:1084/1909` 会拒绝
活动批次期间 HEAD 偏离 `base_commit`，故工具提交只能放在批次之间。
