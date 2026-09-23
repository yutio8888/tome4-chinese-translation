# 修复窗口 8 出版证据与交接

## 范围与成果

- 窗口 8 仅处理审核 254 冻结的六个 target：无尽狩猎描述、`ALL_DREAMS` 成就名、Yeek 解锁文本换行、Thalore 诗句、麻痹毒素伤害方向和《龙族传说》四处语义。
- 译文提交为 `9b71efd8714678d10419f9522a93a25c92f3e841`，只修改 `mod-tome.lua`；没有修改术语库、规则或工具。
- R0 确认诗句中的“紫衫”应为“紫杉”，并恢复鸫鸟与猫头鹰两个主体及其叫声含义；该项经单轮有界修复后进入最终复审。
- publication EXECUTOR 没有修改 Lua、术语、规则、工具、旧证据或 `.ai`，也没有重跑 queue、catalog、migration-chain、复审或完整门禁。

## 独立复审、裁决与 pending

- `REVIEW/full`（`codex/gpt-6-sol`）原始结果为 2 `OK` / 4 `ISSUE`。诗句 finding 为一级 confirmed，完成一轮有界修复；Yeek `cunning`、毒素风暴等概率表述和龙族传说第一人称三项转为 pending，不在本窗口修改。
- `FINAL_REVIEW/full`（`claude/claude-opus-5-5`）原始结果为 6 `OK` / 0 `ISSUE`，决定为 `converged`。历轮原始 finding 与裁决均保留，没有被最终结果改写。
- 三项争议及审核 254 的补充观察集中列于[待用户集中审阅的争议条目](../pending-user-review.md)，不阻塞本窗口收束。
- 四个实施/复审 child 均已归档；本 publication child 待宿主在收获本次结果后归档。

## 门禁、冻结归档与重放

- 最终完整门禁 `.artifacts/i18n/ci-gates/run.2f4mryxp/results.json` 为 17/17 通过，包含严格 addon build；最终译文 SHA-256 为 `94d4d4afeae685dd435dfab0b25ad66655f7a782f75441ad3b6c93c6da889d70`。
- [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer 的 `PACK-MANIFEST.json` 逐字节相同。109 个目标均按声明的 SHA-256 和字节数复制，合计 999,605 bytes；归档 `STATE.json` 来自 immutable `STATE-review-validation-checkpoint.json`，冻结输入的 literal 空白保持原样。
- 本出版阶段对受跟踪归档只读运行 `ai_state_check.py`，目标为 `DONE`；结果为 `DONE_VERIFIED: DONE predicate verified`。

## Catalog、迁移与计时

- 第一次 queue rebuild：RC 0，`221.73383699299302` 秒。
- 单次候选 catalog build：RC 0，`3.5409652779926546` 秒。
- 单次 migration-chain：成功，总计 `233.8068169449689` 秒；plan 为 RC 0、`225.9491630020202` 秒，check 为 RC 0、`3.2508091630297713` 秒，apply 为 RC 0、`4.5657484289840795` 秒；投影调用一次。
- catalog 从 `0fece77f6c05306c2706b263729cc1a3b5fcdf1dc29f58bd41af380204595696` 迁移到 `8580c7207ae19005bb206138eabe0daf3fb00a7eb0513c113b64c922adbc5cf2`。6 条 revision changed、29,822 条 unchanged，0 ambiguous、0 unmapped；6 个 successor 已入队，必须重新审核，不能继承旧 revision 的完成态。
- migration ID 为 `518ce6ed86c6d746184ff38b10a45cd9755ff56c2c57a0af650d7aa03252552f`。catalog entries、exclusions、manifest 的 SHA-256 依次为 `1cfec8d197c1c97cce779a174fb1687858037350646cfb47123366be65221cab`、`1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、`0b6c7cbf6b4eea2954eda907740d9aab6347866d1fdf80250215b217f93ebb47`。
- 五个候选 catalog 文件、migration 以及 [publication/](publication/) 中 14 个附件均从冻结来源逐字节安装。

## 宿主后续

本 publication EXECUTOR 未 stage、commit 或 push。证据提交、提交后的第二次 queue rebuild、push、本 publication child 的归档，以及随后继续审核 255（默认 80 条），均由宿主继续执行；本文不提前宣称这些步骤完成。

旧 pending、旧 blocked、范围外 advisory、`.ai/consult/`、`recipe` 和 15 个旧 source-workset 均保持不变，不因本次发布而清零、扩大或清理。
