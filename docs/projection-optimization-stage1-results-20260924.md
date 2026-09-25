# 投影优化第一阶段结果（2026-09-24）

状态：EXECUTOR 实施完成，待宿主独立核验与复审。本文只陈述本次实测与代码事实；没有测到的内容单独列出，不作外推。

方案见 [投影重放优化方案：个人项目版](projection-optimization-plan-20260924.md)。本阶段只做计量和两项局部去重，不含磁盘缓存或 HMAC，也不改变门禁、发布、恢复语义。

## 1. 冻结输入与实现身份

| 项 | 值 |
| --- | --- |
| 任务 | `projection-opt-stage1-20260924` |
| baseline commit / 测量 treeish | `a04b44365f4ad691b07cbef19d0d48cbb0a6a080`（两次测量前后 HEAD 均未变） |
| 当前 catalog | `cdc76147d080c57a246273344897b397c53eded5051d701a3d7974dcb1f9e0f8`，29828 条 |
| 生产 queue.sqlite3 | 两次测量前后 sha256 均为 `9cc36cf5…1dbe73`；无 active checkpoint |
| 基线 `production_review_v2_lite_queue.py` | `073a02d0361737f668a68a8ca981bb3f1610dc9b1c15ae37e109560a502158ef`（= HEAD） |
| 候选 `production_review_v2_lite_queue.py` | `38669a91c25505695fa6227b9dfe28f6dfee202806a303f161ec9ec502a26b7f` |
| 两侧相同 | reader `64d7cf69…`、migration `fc46b4fd…`、progress `b03beb89…`、`benchmark_projection.py` `f00bf919…`、stage1 harness `38fd8c37…` |
| 机器 | 16 核、45 GiB；测量时负载约 1；OS page cache 未控制，两侧准备方式相同 |

`python3 -B tools/i18n doctor` 在首次调用时通过，只有既有的三条 DLC `source-unpinned` 警告。

派生产物位于 `.artifacts/i18n/projection-opt-stage1-20260924/`，被 Git 忽略：

- `baseline-1.json`，sha256 `681cd900…fd7da`
- `candidate-1.json`，sha256 `b3bda8cb…9a8b6`
- 对应的 `.log` 文件与 `focused-tests.log`

本文已抄录下文使用的全部数值。

## 2. 实际改动

1. **计量工具（新增）：`tools/orchestration/benchmark_projection_stage1.py`。**
   - 原样复用 `benchmark_projection.run()`，保留单进程单次 `_projection(root, commit, progress={})` 调用、身份摘要、完整 progress 和 HEAD/queue/checkpoint 守卫。
   - 只在这一次投影期间包装以下函数，按独占时间统计，因此各分段互不重叠：
     - catalog：`_catalog_view`、`_catalog_from_tree`
     - migration：`_validated_migration_edges`、`reconciliation_rows_for_tree`、`_migration_chain`、`_unchanged_rows_through_chain`
     - publication：`_publication_commit`、`_migration_publication_commit`
     - batch：`_batch_rows`
     - progress：`observe`、`report`
     - 投影内联剩余部分：HEAD/tree 读取、历史 manifest 校验、拓扑序和 winner 汇总
   - 同时按子命令统计 `git` 子进程的数量和墙钟。这部分时间落在上述分段内部，不能与分段相加。
   - `--compare` 使用本任务的新规则：身份和 progress 完全一致，候选墙钟和峰值 RSS 均不超过基线的 110%。
   - 没有改动旧 PERF-1 阈值、`benchmark_projection.py` 或已有产物。
2. **当前 migration 边界的完整 reconciliation 复用：`production_review_v2_lite_queue.py`。**
   - `_projection_contents` 把当前 `(catalog_id, catalog 内容身份)` 传给 `_validated_migration_edges`。catalog 内容身份即五个候选文件的 blob OID。
   - 只有发布提交处 catalog 内容身份与当前树完全相同的那一条边，会额外保留 `_migration_rows(normalized)` 的完整有序七元组，其中含 `reason` 和 `migration_id`。其他历史边仍只保留紧凑映射。
   - 新增 `_current_reconciliation` 选择 reconciliation 来源：
     - 无匹配边界返回 `[]`，与独立函数在相同记录校验后的回答相同。
     - 匹配边保留了完整行时，直接复用。
     - 其他情况仍调用原 `migration.reconciliation_rows_for_tree`。
   - 多个匹配边界时报错的位置和文本不变。独立入口 `reconciliation_rows_for_tree` 本身未改，直接调用时仍做完整校验。
   - 等价性依据：
     - 原独立函数重新读取全部 migration 记录，并做同样的 `_validate_migration_record`。
     - 它对 base catalog 的检查项与边校验相同：manifest 字节哈希、`catalog_id`、`entries/exclusions_sha256`。
     - 它随后以相同记录、相同 old/new entries 调用 `validate_migration`。
     - 复用条件要求 new entries 来自与当前 catalog 相同的五个 blob，因此结果必然相同。
3. **carry 同时携带 projection 与完整 progress：`production_review_v2_lite_queue.py`。**
   - carry slot 元素由 `(root, projection)` 改为 `(root, projection, progress 或 None)`。
   - `rebuild` 写入 slot 时，progress 存入深拷贝。
   - `projection_for` 仍返回原五元组，行为不变。
   - 新增 `projection_and_progress_for`：
     - 同一 root、重新解析后的同一 commit、且 slot 带 progress 时才复用，并返回 progress 私有副本。
     - slot 只有 projection 时，带收集器重放一次，不从 winners 反推 progress。
     - 失败的重放不写 slot。
   - `init/rebuild/check/status/finalize/recovery` 的独立重放均未改。已有测试 `test_queue_check_replays_inside_a_carry_scope` 仍然通过。
4. **batch 包装器计时：`tools/orchestration/run_batch_steps.py`。**
   - 三处步骤循环在原 stderr 行 `--- <step>: exit=… elapsed=…s` 后追加 `projections=N projection_elapsed=…s`。
   - 做法是临时包装 `queue._projection`，与 `run_repair_steps._measure_projections` 相同，不替换也不短路原函数。
   - stdout 中的 CLI JSON 不变。`run_repair_steps.py` 已有等价计时，未改。
5. **测试与登记。**
   - 新增 `tests/i18n/test_projection_stage1.py`，共 19 项，并登记到 `tests/i18n/test_groups.json` 的 `production-shadow-surface-ledger` 组。
   - 没有修改任何已有测试。

`_reconcile_checkpoint` 在 return 之后的旧代码不可达，本次未清理，也未把它计作重放次数。

## 3. 测试

命令如下（宿主统一运行完整门禁，本 dispatch 未跑）：

```
python3 -B -m unittest tests.i18n.test_projection_stage1 tests.i18n.test_production_review_v2_lite_queue \
  tests.i18n.test_production_review_v2_lite_migration tests.i18n.test_production_review_v2_lite_progress \
  tests.i18n.test_git_evidence_reader tests.i18n.test_benchmark_projection tests.i18n.test_repair_steps \
  tests.i18n.test_test_groups
```

最终结果：338 项全部通过，耗时 42 s（`focused-tests-2.log`）。另外：

- `python3 -B tools/test_groups.py --check` 通过。
- `--group production-shadow-surface-ledger` 共 491 项通过，耗时 57 s（`group-ledger.log`）。

第一次合并运行（`focused-tests.log`）曾失败 20 项，耗时 557 s：

- 原因：新测试先导入了顶层 `i18nlib` 的 queue/batch/cli 等模块。之后 `ProjectionChainTests`/`AdjudicationChainTests` 的别名只在名字缺失时才绑定，导致它们的 gate mock 落空，真实门禁被执行。
- 这是新测试文件造成的测试间污染，不是运行时回归；这两个类单独运行时 30 项均通过。
- 修正：新测试在使用顶层名字时临时把 `i18nlib.*` 别名到已导入的 `tools.i18nlib.*`，并在结束时移除期间新增的全部 `i18nlib*` 模块。
- 只导入已有测试模块时就会出现的六个顶层 `i18nlib` 名字属于既有状态，未改动。

新测试以“原算法”为参照：在同一 fixture 中不向边传当前 catalog，并让 reconciliation 恒走独立函数。比较 entries、overrides、reconciliation 的完整内容与顺序，以及完整 progress。覆盖以下风险：

- 当前边界含 `target_changed` 行时与参照一致，且候选不再调用独立函数。`reason` 与 `migration_id` 逐行无损。
- 两条边界时只有当前边保留完整行；历史边的键集合与原先完全相同。同 catalog_id、不同内容身份时不保留。
- 最新 catalog 没有 migration 时 reconciliation 为 `[]`，与参照一致。
- 重复的当前边界仍报 `more than one migration boundary targets the current catalog`。
- 独立入口对被篡改的 entries 仍报错，对真实 entries 的结果与投影相同。
- carry 相关：
  - rebuild 交出的 projection/progress 与独立无 carry 重放完全相等，旧接口返回同一对象，调用者改动返回值不影响 slot。
  - 只有 projection 的 slot 为取 progress 恰好重放一次。
  - HEAD 移动后重新计算，结果与独立重放相等。
  - 不同 root 不共享；异常不写 slot，也不覆盖原有条目。
  - scope 外每次调用都重放。
- 计量工具：独占计时不重叠且总和等于投影墙钟；投影外不计数；git 按子命令计数；拒绝嵌套投影。
  - 比较规则中每项检查可单独失败，上限为含边界值。
  - fixture 上真实运行后，各模块和 `subprocess.run` 均被还原。
  - 已存在的输出文件在重放前即被拒绝，内容不变。
- batch 包装器的 stderr 行计数与格式正确，并还原 `_projection`。

本次改动没有新增扫描或解析循环：边校验循环的结构和终止条件不变，只多一次常量级身份比较。因此没有另加终止探针。

## 4. 计时口径

- `wall_s`：单次 `_projection` 调用前后的 monotonic 墙钟，不含进程启动、导入和 queue 指纹计算。
- `peak_self_rss_kib`：`RUSAGE_SELF.ru_maxrss`。
- 分段：`perf_counter` 独占时间。各分段之和等于 `wall_s`，误差在微秒级。
- git：投影期间 `subprocess.run(["git", …])` 的调用次数和墙钟，已包含在分段内。
- 样本：基线、候选各一次，串行执行，`timeout -k 10s 600s`，没有并发重放。

## 5. 基线与候选（同一 root、同一 commit、各 1 个样本）

| 指标 | 基线 | 候选 | 变化 |
| --- | ---: | ---: | ---: |
| 投影墙钟 | 249.83 s | 252.37 s | +1.0% |
| total user（self+children） | 242.45 s | 244.67 s | +0.9% |
| 峰值 RSS | 3,112,160 KiB | 3,117,396 KiB | +0.17% |
| git 子进程 | 11512 | 11357 | −155（全部为 `cat-file`） |
| git 墙钟（包含在分段内） | 31.10 s | 31.01 s | −0.1 s |

| 独占分段 | 基线 | 候选 | 调用次数（基线/候选） |
| --- | ---: | ---: | --- |
| catalog | 205.51 s | 206.77 s | 704 / 703 |
| migration | 14.70 s | 14.18 s | 670 / 669 |
| publication | 11.60 s | 11.91 s | 518 / 518 |
| batch | 11.87 s | 13.14 s | 334 / 334 |
| 内联与汇总 | 5.83 s | 6.03 s | 1 / 1 |
| progress | 0.31 s | 0.33 s | 335 / 335 |

`--compare` 全部检查通过：

- 同一 root 和 treeish。
- 身份字段全部相同，包括 entries/overrides/reconciliation 的完整 repr 摘要：
  - `entries_d a9184a53…`
  - `overrides_d 40f91e49…`，24073 行
  - `reconciliation_d 7d2f5aed…`，29828 行
- progress 完全一致。
- 墙钟和 RSS 均在 110% 以内。
- HEAD 与 queue 均未变。

解读：

- 去重确实消除了一次重复工作：一次 `reconciliation_rows_for_tree` 调用。该调用会重新解析 HEAD 下全部 184 份 migration 记录，并读取 5 个 base catalog blob；其中部分 blob 命中投影内 LRU，不再调用 Git。对应 migration 分段减少 0.52 s，`cat-file` 实测少 155 次。
- 这项节省约为单次投影的 0.2%，小于单样本间 catalog、batch 等未改分段自身的波动（+1.3 s、+1.3 s）。
- 因此单样本**不能**得出候选变快或变慢的结论，只能确认：结果逐项一致，冷路径墙钟与峰值内存未超过 +10% 上限。
- 本次未做三样本中位数验收，也不宣称端到端提速。

## 6. 真实调用记录（已有日志，未新跑生产流程）

来源为 `.artifacts/i18n/continuation-20260923/review2NN-*-timing.json`，由宿主 `timed_command.py` 记录，覆盖批次 260–277。

| 批次 | 记录的工具命令 | 单命令墙钟 | 合计 |
| --- | --- | --- | ---: |
| 260–275（逐批） | start、surface-export、surface-import、contextual-export、adjudication-chain、finalize、post-closure queue rebuild | 除 adjudication-chain 外均约 222–256 s；adjudication-chain 为 369–412 s | 1774–1927 s（272 多一次 pre-queue rebuild，为 2141 s） |
| 276 | rollover-chain、surface-export、surface-import、contextual-export、finalize | 276–289 s | 1413 s（未记录 adjudication-chain 与 post-closure rebuild） |
| 277 | rollover-chain、surface-export、surface-import、contextual-export、finalize、post-closure rebuild | 251–267 s | 1542 s（未记录 adjudication-chain） |

修复窗口 27 的 `run_repair_steps preflight` 有真实计数：两组分别为 1 次投影 249.78 s（工具 260.62 s）和 1 次投影 251.34 s（工具 258.69 s）。

据此可以确认：

- **单个普通命令的耗时几乎全部是一次完整投影。** 修复 preflight 有实测：投影约占工具墙钟的 96–97%。batch 单步墙钟与本次单投影基线（约 250 s）相当。batch 单步的旧日志没有投影计数，“每步一次投影”是依据代码路径加墙钟对照的推断，不是计数。本次给 `run_batch_steps` 加计数，正是为了以后能直接记录。
- **进程内重复已基本消除。** 已使用的 chain 均只重放一次：rollover-chain 为 rebuild+start，adjudication-chain 为 import/adjudicate/prepare，修复 preflight 同批内也只重放一次。adjudication-chain 多出的约 130 s 主要来自 prepare-evidence 的门禁；旧日志中单独记录的 prepare-evidence 为 137 s。
- **单次投影内部，catalog 校验占 82%（206 s / 250 s）。** 这是对历史 catalog 字节的纯校验；同一内容在一次投影内已只校验一次，由 derive 按内容身份去重。migration、publication、batch 合计约 38 s，progress 可忽略。
- **剩余的重复主要来自跨进程的同 commit 重放。** 一个审核批次从 start 到 contextual-export/adjudication 共 4–5 个独立进程，都在同一 HEAD 上重放。finalize 和 post-closure rebuild 在同一个新 commit 上各重放一次；277 批之后下一批的 rollover rebuild 又在该 commit 上重放一次。
  - 按每批约 7 次投影、只涉及 2 个不同 commit 估算：同 commit 的重复约有 4–6 次，按单次 250 s 计约 1000–1500 s，占每批工具时间 1800–1900 s 的 55–80%。
  - 这是按次数乘以单次时长的**估算**，不是实测。其中哪些可以命中缓存，受方案 4.1 入口表约束：rebuild、check、finalize 保持独立重放。

## 7. 未测项与偏差

- 只有一个基线样本和一个候选样本，没有三样本中位数，也没有交替采样。按 SPEC，这一步只验证可行性。
- 没有在隔离副本上重放完整审核或修复流程，第 6 节的流程数据全部来自已有日志。batch 单步的投影计数是推断。
- 没有测暖缓存，本阶段不存在缓存。
- 没有统计每次投影中不同 catalog 内容的实际校验次数（derive 未命中次数）。第 6 节“同一内容只校验一次”依据的是 derive 的代码语义，未另行计数。
- 新 API `projection_and_progress_for` 在当前生产 chain 中没有调用方：现有 chain 不在 rebuild 之后读取 progress。它对现有流程的实测收益为 0；本次只提供带测试的正确性基础，没有把 `status` 或 `check` 接到 carry 上。
- `run_batch_steps` 的 stderr 行多了两个字段。未发现有测试或工具解析该行；若宿主脚本按旧格式 grep 该行，需要同步调整。
- 本阶段完成后，候选 `production_review_v2_lite_queue.py` 没有再改动；候选基准之后只改了 `run_batch_steps.py` 和测试文件。
- 新测试的模块污染问题已在交付前修正并复跑，见第 3 节。

## 8. 第二阶段建议

结论：数据支持进入**同 commit 已提交投影缓存**的评估。理由如下：

1. 第一阶段可做的进程内去重，收益已低于测量噪声，继续做局部去重没有意义。
2. 剩余普通命令的耗时几乎全部是完整投影，而且多数是跨进程对同一 commit 的重复重放，正符合方案 3.3 的“进入第二阶段”条件。
3. 常用路径的受益面有真实调用记录支撑：surface-export、surface-import、contextual-export、adjudication-chain、batch start 或 rollover 都属于方案 4.1 表中“可命中”的入口。

受益上限需在第二阶段开始前由宿主独立计量并冻结，上面的 55–80% 仅为估算。

另有两点供宿主裁决，本次均未实施：

- **不改代码的流程收益：** 在确认两步之间没有别的依赖后，把 surface-import 与 contextual-export 放进一次 `run_batch_steps.py` 调用（包装器已支持）；在紧接 rollover-chain 时省去 post-closure queue rebuild（276 批就是这样做的）。两项各可省一次约 250 s 的投影，均为估算，需先核对宿主流程。
- **不可缓存的独立重放仍会各花约 250 s：** 包括 finalize、rebuild、check 和恢复路径，其中 82% 是 catalog 字节校验。如果第二阶段之后这部分仍是主要等待，应另行评估两条路：按 blob 内容键缓存 catalog 校验结果（属于方案第 5 节暂缓的跨 commit 内容缓存），或对 `validate_catalog_files` 做算法优化。本次数据不足以在两者之间取舍。
