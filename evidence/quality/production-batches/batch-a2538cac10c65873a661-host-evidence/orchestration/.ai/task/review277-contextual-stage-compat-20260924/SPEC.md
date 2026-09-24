# 第 277 批 contextual 初次 stage 与预建草案目录兼容

第 277 批 `batch-a2538cac10c65873a661` 已在 surface import 后按现行工作流写入 contextual task 的 `CONTEXTUAL-INPUT-DRAFT.json`、`SCOPE.json`、`SPEC.md`、`PLAN.md` 和 `ANCHOR-PREFLIGHT.json`，anchor preflight 为 `PREFLIGHT_VERIFIED`。生产 contextual export 已成功并发布 checkpoint；`stage_contextual.py` 首次 stage 因 task 目录存在而拒绝，尚未写候选、STATE 或 report。

目标：
1. 让普通（非 refreeze）stage 在目录只含上述预建草案/任务记录、且冻结 draft 与 checkpoint input 严格匹配时安全继续；缺少或漂移的 draft、未通过 anchor preflight、符号链接、额外文件、已有候选/STATE/raw/review 必须拒绝。
2. 保持 refreeze 的同 event 中断恢复、完整 STATE 绑定、无覆盖写入和报告冲突门禁；不得放宽 reviewer 读取边界。
3. 对本批 11 条 contextual 冻结输入做无写入预检，证明 stage 可恢复且原目录文件不被覆盖；增加必要定向测试，并运行适用契约/单元验证。
4. 不改译文、术语、生产 checkpoint、已冻结 input 或旧 reviewer 输出。不提交、不 push；完成后由 ORCHESTRATOR 独立复审并恢复本批 stage。

允许任务内容文件：`tools/orchestration/stage_contextual.py`、`tests/i18n/test_review_prompts.py`；若需修改其他文件，先报告原因。
