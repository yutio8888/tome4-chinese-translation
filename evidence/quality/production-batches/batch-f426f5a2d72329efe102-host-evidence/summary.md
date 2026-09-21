# 第 244 批宿主核验记录

本批冻结 80 条 tome revision，基线 `e117983a360b8dcb360ab35f0b5414148d534605`，源码固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。全部 80 条的来源字面及 60 个源文件哈希均已核验。

四路 surface 覆盖 80 条，77 条 OK、3 条 ISSUE；有效 contextual full 覆盖这 3 条。6 个 observation 逐项裁决：4 个 confirmed observation 归并为 2 个需要修复的 revision，1 个 refuted，1 个 advisory。修复对象是念动弓每回合/伤害信息遗漏，以及阴影召唤持续自动补召/数量上限遗漏。巨石恐魔按石质外形命名有固定源码根据；强调固着的改名意见只留 advisory。

念动弓原文 nearest 与实际代码不符：回调虽计算 nearest target，实际却用 rng.table(tgts) 得到 a 并向 a 的坐标射击。仅确认逐回合和伤害信息等遗漏，不恢复“最近”。属性/参数的定向流向和对应完整固定源码见 `HOST-SOURCE-CLAIM-EVIDENCE.json`；逐 observation 决策见 `HOST-DECISIONS.json`。另有一项调试窗口概述简写建议，仅作 host-only advisory，不修改生产状态。

第一次 contextual 导出受前批未绑定当前检查点的临时输入占位影响；核实与前批已提交输入逐字节相同且前批已归档后，仅迁移此临时副本，当前 checkpoint 不变，重试成功。`CONTEXTUAL-EXPORT-RECOVERY.json` 记录边界。

第一次 contextual reviewer 虽返回合法 JSON，但执行了全仓内容搜索、读取未引用的现有译文并写入 /tmp/o.json，整次输出判废。其原始输出、拒绝证据和身份记录保留，不作为有效审核意见。fresh retry 使用同一 candidate/input，边界与严格校验通过。共 6 个 reviewer child 全部确认归档；有效 surface 与 contextual 两个任务均为 DONE_VERIFIED。

`orchestration/` 保存原路径结构、冻结输入、任务/审核记录、生命周期 journal、原始输出和每次实时 profile 捕获；`ORCHESTRATION-INVENTORY.json` 绑定 52 个文件。`SNAPSHOT-REPLAY.json` 记录两个任务在快照中独立通过离线 DONE 检查。该快照冻结于本批 prepare-evidence 前，只证明复核、来源和归档边界，不预填后续门禁、commit、finalize 或 push。

本批没有修改译文、术语库、检查器或规则。完整门禁及最终生产状态由本批生成的 gates/manifest/results 与实时 checkpoint、提交和远端状态证明。本批是修复窗口 3 的首个审核批；默认继续 245、246 后收一个修复窗口，达到既定提前收口条件时例外。Archmage 范围外 pending 与 RW1-SIB-01/02 永久排除保持不变。
