# 第 278 批工具链隔离分析

分析基线：`35cae04614c8710b0287b6d7870f80bdd7c374ea`。
工作树：`/workspace/tome4-projection-analysis-20260925`。
分支：`analysis/projection-review278-20260925`。

本轮只做隔离实验和报告，不修改运行时代码、测试源码、审核契约或主工作树，不启动生产批次。Git 工作树共享对象库，但实验使用独立临时 fixture，不对生产历史、配置或状态执行写操作。主工作区前后核验记录在本工作树 `.artifacts/i18n/review278-analysis/`。

## 1. 已复现：缓存环境污染发生在 fixture 初始化阶段

同一工作树、同一解释器，运行以下三个既有测试，仅改变进程环境：

- `test_repair_steps.RepairStepTests.test_two_preflights_match_standalone_bytes_and_replay_once`
- `test_projection_cache.SwitchAndEntryTests.test_off_never_reads_writes_or_creates`
- `test_projection_cache.MissAndFallbackTests.test_symlinked_cache_directory_is_never_used`

| 环境 | 结果 | 用时 |
| --- | --- | ---: |
| `I18N_PROJECTION_CACHE=off` | 3 项通过 | 1.16 s |
| `I18N_PROJECTION_CACHE=on` | 6 个断言失败、1 个 error（含 subtest） | 1.52 s |

日志：`off-targeted.log`、`on-targeted.log`、`targeted-results.json`。

进一步隔离验证：实验父进程设置 `I18N_PROJECTION_CACHE=on`，只对子进程 env 副本设置 off 并去除 trace，运行 `python3 -B tools/test_groups.py --group production-shadow-surface-ledger`。532 项全部通过（测试计时 73.78 s，父进程计时 74.05 s），返回后父进程仍为 on。见 `sanitized-group.log`、`sanitized-group.json`。这是完整相关测试组的隔离实验，不是修改后的 gate runner 集成验收，也不是完整 17 项门禁。

源码依据：`gate_results._execute` 未传 `env`，直接继承宿主环境；缓存测试 `_Fixture.setUp` 先建立、发布 fixture，测试体才设置开关。外部 on 因而可能在 setUp 阶段创建缓存目录。之后测试体即使明确 off，也无法撤销已经创建的目录。另一类测试依赖重放计数，磁盘缓存命中让计数由 1 变为 0。

这不是业务缓存忽略 off 的证据，也不是只改单个 off 测试就能解决的问题。

建议最小实施边界：

1. 测试 fixture 在任何生产模块调用之前冻结默认 off，并恢复原环境；缓存测试在所需范围内显式 on。覆盖直接 unittest 入口，不能只依赖统一 runner。
2. 门禁测试子进程显式设置缓存环境，避免用户 shell 改变基线测试语义；主进程不变，prepare-evidence 历史读取仍可命中缓存。保留真实 CLI 冷/暖/off 测试，避免把开启路径从测试中排除。
3. 若在 gate runner 层改环境，回执须明确绑定实际子进程环境或固定环境策略版本。当前 binding 包含父进程环境摘要，不能不说明就把该摘要当作清洗后环境的身份。不要在 run 中临时修改全局 os.environ，避免首尾回执绑定不一致。
4. 验收：父进程 on/off 两种环境下完整门禁均通过；测试执行前后父进程开关不变；模拟原门禁失败后仍保留 adjudicated，恢复只重跑 prepare-evidence。

## 2. 已定位：surface 两次失败都是条目身份回显错误

来源为已提交快照：
`evidence/quality/production-batches/batch-2dd6d21e34b360ebb6d9-host-evidence/orchestration/`。

`review278-surface-children.json` 明确记录：

- 首轮 `lane-001-0` 的 index 2 回显了错误的 `entry_revision_identity`。
- 第二轮 `lane-001-r2-2` 的 index 11 回显了错误的 `entry_revision_identity`。

`HOST-SURFACE-BOUNDARY-AUDIT.json` 记录实际派发 14 个 child、未派发 2 个 lane；14 个均已归档，无写入或越界读取。14 个结果中 2 个无效，12 个有效，但失败组里的 4 个有效结果不能用于最终发布。最终两个四 lane 组只需 8 个有效结果。

因此本批重试首先是机械身份回显问题，不是译文实质意见不一致，也没有证据要求提高模型推理强度。失败记录必须按 entry_revision_identity 与 candidate_identity 分类，不能统称 identity 错误。

建议先做精确校验器自动输出错误位置、预期值与实际值，并绑定 dispatch/input hash。若继续出现，可单独设计模型仅输出冻结序号和 verdict、可信适配器生成身份字段的契约版本；适配器须验证数量、顺序、唯一性，保留原始输出及模型来源，不得给错误旧结果事后改 identity 后接收。当前契约明确整组重试，不在操作脚本中擅自改为局部重试。

## 3. 重放与收益边界

第 278 批计时记录显示普通 surface/contextual 导出导入已约 2 秒，contextual-import 在链日志中为 1.6 秒且 projections=0。继续合并这些步骤主要减少操作复杂度，已没有旧版每步约 250 秒的收益。

失败链 168.70 秒、清除缓存后的 prepare-evidence 补跑 403.68 秒；不能把两者总和视为可节省时间，正常流程也需要门禁。prepare-evidence 是现行 READ_ENTRIES 中的缓存允许入口；补跑的完整历史重放是清除父进程缓存开关造成的，不是该入口永远不可缓存。

主流程保留 on、仅测试子进程 off，有望同时避免失败门禁和补跑的完整重放。新环境策略尚未接入生产门禁，不能据隔离测试宣称实测生产端到端节省。

rollover 253.52 秒、finalize 255.61 秒、关闭后 rebuild 251.96 秒，三者约 12 分 41 秒。finalize 和关闭后 rebuild 中间存在 closure commit；当前契约和实现要求分别验证，不可跳过或只更新 SQLite evidence HEAD。

先前 catalog 段约占完整重放 82%，仅是前版本测量。当前源码 `_catalog_view` 已按完整 catalog blob identity 做单次重放内去重，`_intern_catalog_rows` 也已复用相同行；不能再把这些已有优化当新方案。下一步应剖析不同 catalog 之间的逐行重复校验/解析成本，再决定是否做投影内纯函数结果复用；本轮没有执行真实全量投影或新增性能统计，不承诺减半。

## 4. 实施顺序与停止边界

优先实施测试环境隔离及其集成回归；随后整理 identity 失败的自动诊断和派发清单。catalog 进一步优化以新剖析为进入条件。快照工具统一消费 created/terminal/archived/undispatched 状态，保留所有必要证据，不减少审计范围。

暂不改变四 lane 独立性、整组重试、发布门禁、finalize/rebuild 边界；暂不增加跨提交缓存。本轮结果可用于后续实施 SPEC，但本轮不实施、提交或合并这些改动。

核验收尾：主工作区 HEAD、git status 与实验前记录的队列/checkpoint 文件摘要均未变化，生产 active-batch.json 不存在。工作树仅新增本报告；实验日志位于忽略目录。未提交、未合并。
