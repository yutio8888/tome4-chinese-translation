# 翻译审核当前交接

更新时间：2026-09-21（审核 243 完成，修复窗口 2 待宿主完成最后出版步骤）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前结论

- 审核已完成至批 **243**；窗口 2 收口并完成安全边界后，下一审核批为 **244**。
- 修复窗口 2 的五条译文已提交为 `14c755659d18a5f0989ec75d67f0245de3f0cc13`，有效独立复审、FINAL_REVIEW/full、17 项完整门禁与严格构建均通过，冻结快照可独立回放为 `DONE_VERIFIED`。
- 首次 queue rebuild、单次 authoritative catalog build 和 migration check/apply 已真实成功。migration ID 为 `0e4ad828eb000567f49f34b1b7a9e8c823550740697b51a4d616d72cc9dac454`，结果为 5 changed / 29823 unchanged、`queued_successors=5`、`ambiguous=0`、`unmapped=0`。
- `migration apply` 只先更新 SQLite。随后 EXECUTOR 已按 SPEC 将核验过的候选 catalog 五文件及新 migration JSON 逐字节安装到六个精确工作树路径；所有目的文件均与来源 bytes/SHA-256 一致，没有手改、重建或覆盖旧迁移。
- 当前仍未完成：**证据/catalog/migration commit、第二次 queue rebuild、push**。这些由本宿主收尾；不要预填未来 commit ID、queue 结果或 push 结果。
- 当前用户已明确授权本轮**每批完成后 push**。旧交接中“未获得 push 授权”的描述只属于历史，不再构成当前限制。

## 宿主收尾顺序

1. 核对并提交窗口 2 的 evidence、确定性安装后的 catalog/migration 产物与本交接；不得夹带既有无关 untracked 文件。
2. 在证据提交后执行并计时第二次 `production queue rebuild`，保存实际结果；不要重复 catalog build 或 migration。
3. 重新实测 HEAD、catalog ID、queue 状态与 active checkpoint，确认安全边界后按现有授权 push。本文写入时观察到的 HEAD 为译文提交 `14c7556…`、catalog ID 为 `2a8b6f…`，但宿主后续提交/同步会改变实时状态，故不得把这些观察值当成未来完成事实。
4. 窗口 2 提交、第二次同步和 push 均成功后，再开始审核批 **244**；继续遵循“每批完成后 push”。批次活动 checkpoint 内仍不得提交。

完整窗口事实、有效/判废 stage、门禁时间、快照边界与出版收据见 `evidence/quality/repair-window-2-20260921/summary.md`、`snapshot-replay.json`、`orchestration/` 和 `publication/`。

## 固定边界与待处理项

- 五个 successor 需要重新生产审核；进入队列不等于生产深审完成。
- Archmage revision `8b977dd836…` 保持范围外 pending：不改译、不清状态、不计入新增可执行 revision 阈值，也不阻塞后续审核。
- `RW1-SIB-01`、`RW1-SIB-02` 永久排除；同类 observation 只记 advisory，除非维护者另行明确授权新切片。
- 本窗口没有术语库修改、全局重命名或跨批次策略变更。
- 固定源码为 tome commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；五条均为 tome，无 DLC。
- 历史批次与旧事故细节见 `docs/handoff-history-through-20260919.md`；历史文字不扩大当前授权。

## 继续工作时必须重查

先实测而非照抄本文：

- `git status --short`、`git log`、当前分支与远端差距；
- 当前 catalog manifest ID 及 migration 文件是否已提交；
- 第二次 queue rebuild 的真实收据、队列 reconciliation 与五个 successor 状态；
- `production batch show` 的 active checkpoint；
- push 是否实际成功及远端 HEAD。

保持单一 production writer；不伪造 ISSUE/done，不改写冻结复审记录，不修改检查器、角色或契约以绕过门禁。提交前只纳入本窗口授权内容，保留用户既有无关文件。
