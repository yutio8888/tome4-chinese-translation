# 宿主预复核：重冻入口的预检查顺序

`stage_contextual.py` 在 `--refreeze-id` 路径先调用 `contextual_export()` 写入新 input 与 checkpoint，随后才检查 `--out` 报告路径是否已存在，以及新 task 目录是否已存在。若报告路径已存在，重冻事件已持久化而 stage 失败；现行 `_validate_refreeze_old_refs()` 又要求旧 refs 每个都有已归档 child，新 refs 尚无 child，下一次无法安全重试。应在执行 `contextual_export()` 前预检报告路径；对 task 目录冲突则由 export 的新 task 路径检查覆盖。需要独立 reviewer 复核此 finding，再让 EXECUTOR 有界修复。当前不触发生产重冻。
