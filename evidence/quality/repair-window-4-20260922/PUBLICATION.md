# 修复窗口 4 出版证据

## 范围与成果

- 窗口 4 主任务修正 17 个 target：审核 247—249 的三次真实 repair preflight
  共 16 条正式候选，另加审核 248 的回忆录宿主独立补充 1 条。该补充没有被伪装成
  preflight 结果。
- 另一个独立 runtime sibling 任务修正 Cults 的 `thalore wilder` 共享运行时键 1 条；
  它不属于主任务 17 条，也不把主 workset 扩写为 18 条。共享键在官方 core 中已经存在，
  因而不重复写入 DLC overlay；这不表示 Cults 组件整体不发布。
- 译文提交为 `df8a73a3c9b54f6696cf47baf297f01dc7105ce4`。本出版阶段未修改
  Lua、术语、规则或工具，也未重跑 queue、catalog、migration-chain 或完整门禁。
- tome 固定公开源码 commit 为
  `624a67329fe2ad440c5b344785a9c73fcf22ae63`。Cults 条目的实际公开源码快照
  SHA-256 为 `6cc08be3041889e6e7223c27b056f6d8db173e75108e881fb20aea64234b5cb9`；
  其上游仓库、commit 与版本未固定，catalog snapshot 不是源码 commit。

## 审核、门禁与冻结边界

- 完整门禁首次为 16/17 通过；定位跨组件 runtime key 碰撞并由独立 sibling 任务修复后，
  retry `run.tb2mt5it` 为 17/17 通过，包含严格 addon 构建。主任务与 runtime sibling
  两个 checkpoint 均为 `DONE_VERIFIED`。
- 主任务最终原始结果是 16 `OK` 加 1 个范围外 `ISSUE`，不是 17 `OK`。宿主裁决后
  scope 内没有 accepted 或 deferred finding，任务据此 completed；原始 `ISSUE` 没有被改写。
  回忆录 source 164 与 198/210 的范围外观察继续分别保持 pending/advisory，不自动修复。
- Cults 有效 `REVIEW` 和 `FINAL_REVIEW` 均为 1 `OK`。首次 review input 因
  `fixed_source_identity` 格式错误被宿主判为无效，修正输入后 fresh retry；无效尝试和
  原始材料均保留。
- Archmage 与旧 blocked 项继续排除；`RW1-SIB-01/02` 的既有排除不变。

归档的 [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer
manifest 逐字节相同。清单的 309 个目标在复制前后均按声明的 SHA-256 和字节数核对，
合计 2,926,264 bytes。两任务归档 `STATE.json` 均来自各自 immutable
`STATE-review-validation-checkpoint.json`，不是出版时可变 STATE。归档包保留原始字节；
其中 `SPEC.md` 有 36 个 literal 行末空格，两个 `lifecycle.py` 各有 1 个，未清洗。

本阶段从受跟踪归档目录分别重放：

- `python3 -B tools/ai_state_check.py .ai/task/repair-w4-runtime-sibling-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-4-20260922/orchestration --target DONE`
- `python3 -B tools/ai_state_check.py .ai/task/repair-w4-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-4-20260922/orchestration --target DONE`

两条命令均 RC 0，stdout 均为 `DONE_VERIFIED: DONE predicate verified`，stderr 为空。
producer 先前的独立回放结果保存在
[PACK-REPLAY-PROBE.json](publication/PACK-REPLAY-PROBE.json)。

## Catalog、迁移与真实计时

- 第一次 queue rebuild：RC 0，`231.38387920800596` 秒。
- 单次候选 catalog build：RC 0，`3.6432233370142058` 秒。
- 单次 migration-chain：成功，总计 `237.43798736698227` 秒；plan 为 RC 0、
  `229.4439968400402` 秒，check 为 RC 0、`3.2218385279993527` 秒，apply 为
  RC 0、`4.724910582008306` 秒；投影调用一次。
- catalog 从 `75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`
  迁移到 `4763c0b4c71f1ba7a64a5603aca78da83e689f658738d6bc31feaaa9d8f68f08`；
  18 条 revision changed、29,810 条 unchanged，0 ambiguous、0 unmapped，18 个
  successor 已入队且必须重新审核。
- migration ID 为
  `662b5a600a6702658db4397c077036c84d59a3eb32c87cb010d5508cce1c46bc`。
  catalog entries、exclusions、manifest 的 SHA-256 依次为
  `a41338026977731a5026eb32692d02ef42ab2ee9ae3cdebfadfeb2137629b0ec`、
  `1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、
  `ae05a749c5c4f4a8d9de6d27d046c011aa0b9372f3346c86b2ee716ccafad5bd`。
  候选 catalog/schema/policy 与 migration 均为逐字节安装，未编辑字段。

原始 producer 核验、计时与日志保存在 [publication/](publication/)；候选五文件、migration、
publication 原始附件以及 `mod-tome.lua`、`tome-cults.lua` 相对译文提交均已逐字节复核。

## 尚未完成的出版步骤

本文件生成时实际 `HEAD` 为译文提交 `df8a73a3…`，本地远端跟踪引用
`origin/develop` 为 `f9a2b3c7…`。本阶段证据/catalog/migration 提交、提交后的第二次
queue rebuild、push 与远端复核仍待宿主执行；本文不宣称这些步骤已完成。出版闭合后才开始
审核 250，默认 80 条。窗口 4 未借机处理回忆录范围外观察、Archmage、旧 blocked 或其他
advisory。
