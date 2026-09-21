# 翻译审核当前交接

更新时间：2026-09-21（修复窗口 2 已推送；审核 244 复核与宿主裁决已完成）
移交对象：Paseo / Codex / GPT-6-Astra

## 当前结论

- 审核已推进至批 **244**（`batch-f426f5a2d72329efe102`），80 条均属固定来源 tome；四路初筛及有效上下文复核全部 `DONE_VERIFIED`，6 个子进程全部确认归档（其中一次上下文输出因越界读取/写入判废，fresh retry 有效）。
- 本批 3 条初筛与 3 条有效上下文 observation 已逐项裁决：念动弓、阴影召唤两条 revision 需要修复；巨石恐魔的“凭空增义”判断撤销，强调固着的改名意见只记 advisory。念动弓只修每回合和伤害信息等已确认遗漏，不恢复与实际随机选敌代码不符的“最近目标”。本批未改译文。
- 修复窗口 2 的五条译文已提交为 `14c755659d18a5f0989ec75d67f0245de3f0cc13`，有效独立复审、FINAL_REVIEW/full、17 项完整门禁与严格构建均通过，冻结快照可独立回放为 `DONE_VERIFIED`。
- 首次 queue rebuild、单次 authoritative catalog build 和 migration check/apply 已真实成功。migration ID 为 `0e4ad828eb000567f49f34b1b7a9e8c823550740697b51a4d616d72cc9dac454`，结果为 5 changed / 29823 unchanged、`queued_successors=5`、`ambiguous=0`、`unmapped=0`。
- `migration apply` 只先更新 SQLite。随后 EXECUTOR 已按 SPEC 将核验过的候选 catalog 五文件及新 migration JSON 逐字节安装到六个精确工作树路径；所有目的文件均与来源 bytes/SHA-256 一致，没有手改、重建或覆盖旧迁移。
- 窗口 2 的证据/catalog/migration 已提交为 `e117983a360b8dcb360ab35f0b5414148d534605`。第二次 queue rebuild 成功，reconciliation 为 29828；五个新 revision 均为 queued。译文提交和证据提交已推送，2026-09-21 再查远端 `develop` 为 `e117983a360b8dcb360ab35f0b5414148d534605`。不要重复窗口 2 的 catalog build、migration 或 queue 同步。
- 当前用户已明确授权本轮**每批完成后 push**。旧交接中“未获得 push 授权”的描述只属于历史，不再构成当前限制。

## 当前恢复位置与后续顺序

1. 先读取实时 active checkpoint 和已提交 batch manifest。本文在第 244 批证据准备前更新，不预填未来提交或推送事实；按实际 phase 继续导入/裁决/门禁/提交/finalize，已经成功的步骤不重做。
2. 第一次带 source-workset 的上下文导出因旧批 243 的 `contextual/run-000-input.json` 占位而拒绝。宿主已核实旧文件与已提交证据逐字节一致、旧任务均 DONE/归档，将此临时副本保留到本批诊断目录，保持 checkpoint 不变后重试成功。诊断、源码定向流向和有效/无效复核边界见 `evidence/quality/production-batches/batch-f426f5a2d72329efe102-host-evidence/`。不要删除当前已冻结的 contextual 输入。
3. 本批完整门禁、证据提交、finalize 和 push 以检查点及远端实测为准。活动批次内禁止译文或无关提交；消费者进入 `commit_ready` 后，本批证据提交是 `finalize --commit` 的必要前置。若已无 active batch 且本批证据已提交并推送，直接推进下一批。
4. 本批为修复窗口 3 的首个审核批；随后推进 245、246。默认每三批收一个修复窗口；达到 20 个新增可执行 revision 或出现高影响 confirmed 问题时提前收口。仍须逐批完成后 push，授权持续有效。

完整窗口事实、有效/判废 stage、门禁时间、快照边界与出版收据见 `evidence/quality/repair-window-2-20260921/summary.md`、`snapshot-replay.json`、`orchestration/` 和 `publication/`。

## 固定边界与待处理项

- 五个 successor 需要重新生产审核；其中阿塔玛森、手套、野性召唤三个新 revision 已进入第 244 批。进入队列或表层 OK 不等于生产深审完成。
- Archmage revision `8b977dd836…` 保持范围外 pending：不改译、不清状态、不计入新增可执行 revision 阈值，也不阻塞后续审核。
- `RW1-SIB-01`、`RW1-SIB-02` 永久排除；同类 observation 只记 advisory，除非维护者另行明确授权新切片。
- 本窗口没有术语库修改、全局重命名或跨批次策略变更。
- 固定源码为 tome commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；五条均为 tome，无 DLC。
- 历史批次与旧事故细节见 `docs/handoff-history-through-20260919.md`；历史文字不扩大当前授权。

## 继续工作时必须重查

先实测而非照抄本文：

- `git status --short`、`git log`、当前分支与远端差距；
- 当前 catalog manifest ID 及 migration 文件是否已提交；
- 当前队列 reconciliation 与 successor 状态（窗口 2 的第二次 rebuild 已完成，不重复执行）；
- `production batch show` 的 active checkpoint；
- push 是否实际成功及远端 HEAD。

保持单一 production writer；不伪造 ISSUE/done，不改写冻结复审记录，不修改检查器、角色或契约以绕过门禁。提交前只纳入本批授权内容，保留用户既有无关文件。
