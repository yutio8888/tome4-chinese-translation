# 修复窗口 9 出版证据

## 范围与结果

本窗口处理审核 255 的 5 条确认项：高阶奇术师解锁文本、潜行说明、`%d runes active`、
夏之眼和回归之杖描述。译文提交为
`78be6b5a752cb5a24d0ef1e8337f0ba301180f21`。

首轮任务 `repair-w9-20260923` 的 `REVIEW/full`（`codex/gpt-6-sol`）结果为
4 OK / 1 ISSUE：`nothing else` 问题确认修复；`Flame` 名称争议转入 pending，并恢复基线
“火球术”。`FINAL` F1（`claude/claude-opus-5-5`）为 4 OK / 1 ISSUE，确认修复回归之杖
换行；F2 为 4 OK / 1 ISSUE，确认删除潜行第 2、6 行的限定词；F3 为 5 OK / 0 ISSUE。
完整门禁 17/17 通过。但宿主在 `FINAL` 失败后直接进入下一轮 `FINAL`，没有按
`translation_v2_convergence` 阶段结构返回 `RE_REVIEW`，因此任务无法进入 `DONE`，最终以
`STOP_VERIFIED` 关闭；原因保存在该任务的 `STATE.last_error`。

重跑任务 `repair-w9b-20260923` 由唯一 EXECUTOR 逐字应用首轮收敛文本，结果与
`CANDIDATE-FINAL` 逐字节一致。`REVIEW(0)/full`（`gpt-6-sol`）为 5 OK，
`FINAL(1)/full`（`opus-5-5`）为 5 OK，不再开启修复轮。完整门禁
`run.hna9wv8w` 17/17 通过并包含严格构建，任务达到 `DONE_VERIFIED`。

## Catalog 与迁移

新 catalog 为 `0e554a74d6738064f4245525bed6f1be8a8463ea3df7f683ab2327e0fe0de510`，
migration 为 `bdf355b65bef33ded7ac24e48c577770f33d67312fed83ab8de9d1f4c4a538d1`。
迁移结果为 5 条 `revision_changed`、29,823 条 `unchanged`、0 条
`ambiguous/unmapped`；5 个 successor 等待重新审核，不继承原 revision 的 done 状态。

## 生命周期与后续边界

首轮 4 个 executor 与 4 个 reviewer（共 8 个 child）以及重跑任务的 3 个 child 均已确认归档。
本 publication child 尚待宿主归档。证据提交、第二次 queue rebuild 和 push 仍由宿主执行，
此处不提前宣称完成。
