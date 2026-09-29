# 投影内存优化任务说明（perf-projection-20260911）

状态：**实现完成，独立性能验收通过；最终门禁与终轮复审待 ORCHESTRATOR 执行。**
独立 Opus 验收（两次串行 candidate 重放 + 聚焦测试）与独立跨模型复审（Opus5
normal_review、GPT6 high cross_review）均已完成并通过；最终交付状态以
`.ai/task/perf-projection-20260911/STATE.json` 为准，本文件不宣称 DONE 或门禁通过。
本文如实记录初测失败、必要修复、可行性测量与独立验收结果，不预报完成。

## 1. 目标与边界

- 目标：在不改变 Git 提交证据权威性、不新增持久信任层的前提下，降低
  `production-review-v2-lite` 单次投影的常驻内存；顺带在可安全验证的范围内处理
  时间成本。
- 基线提交：`d95ee7f2eda7ca3ecd2822defe40112645888c30`。
- 本轮只实现 **PERF-1**。PERF-2/3 已确认但不在本轮，PERF-4 为 advisory。
- 不修改 validator／publication 查询／6a／CLI wrapper。生产运行时代码只动
  `git_evidence_reader.py`、`production_review_v2_lite_queue.py`、
  `production_review_v2_lite_progress.py`；测试、benchmark 与本文档在允许范围内新增。

## 2. 基线

同 harness、同 treeish、单个 `_projection(root, commit, progress={})` 进程
（`.artifacts/i18n/perf-projection-20260911/baseline.json`）：

| 项 | 值 |
|---|---|
| wall | 141.7094 s |
| self user / children user | 91.78 s / 34.89 s |
| total user | 126.67 s |
| self sys / children sys | 2.58 s / 12.74 s |
| peak self RSS（`RUSAGE_SELF.ru_maxrss`） | 14,090,612 KiB（≈13.44 GiB） |
| 八字段与完整 progress | 见 baseline.json |

## 3. 确认的问题

- **PERF-1（本轮）**：`git_evidence_reader` 全程缓存历史 blob 与解析后的 catalog；
  `_validated_migration_edges` 另外保留 old/new 完整 catalog、`normalized` 展开行、
  `batch_records` 保留 `source_entries`。仅清缓存无法释放被外部引用的对象。
  基线一次重放保留 84 份 catalog／2,505,552 行与 2,475,724 份展开 mapping。
- **PERF-2（未做）**：`_publication_commit`／`_migration_publication_commit` 每条证据路径
  重复扫描 Git 历史（一次重放 2,708 次 `git log`，约 39.97 s）。6a 仍是未合入的
  worktree patch（`/workspace/handoff/6a-uncommitted.diff`），只有历史部分验证。
- **PERF-3（未做）**：细粒度 CLI 调用重复投影同一 HEAD；现有
  `run_batch_steps.py` 只支持部分 action，migration 不支持，属契约扩展。
- **PERF-4（advisory，未做）**：`_tree` 重复解码实测 exclusive 0.861 s，
  不支持为它新增缓存层。

## 4. 采用的 PERF-1 算法

1. **blob LRU**（`BLOB_CACHE_LIMIT_BYTES = 128 MiB`）：blob 字节按字节计量做 LRU；
   单个 blob 超过上限则直接返回不缓存；tree 缓存保持原样；OID 解析、root 隔离、
   失败不缓存不变。
2. **轻量 catalog 视图**：投影内 `_catalog_view(root, tree)` 每次都重验 catalog 子树集合
   与五个候选路径的 ordinary-file 元数据，键为“五个路径＋blob OID”的内容身份；
   首次命中该身份才读取全部五份文件并完整执行 `validate_catalog_files`，成功后缓存
   manifest、`VerifiedRows` 与实际 manifest SHA-256。`_catalog_from_tree` 的完整 files
   接口保留，两个入口共享同一内容验证结果。
3. **完整行复用**：仅在完整验证成功后，以 `VerifiedRows.digest_by_revision` 的
   canonical 行摘要查投影局部行池，再核对整行相等才复用。禁止只按 revision 复用；
   摘要相同但内容不同（含碰撞）一律不合并。重建的 `VerifiedRows` 各自保留本 catalog 的
   顺序与 revision→digest 映射；不修改共享行及其嵌套 `risk`／`args_order`。
4. **紧凑 migration mapping**：每条边完成 publication、old/new catalog 哈希与
   `validate_migration` 全量检查后，只保留 `path`、`old_catalog_id`、`new_catalog_id`、
   `base_commit`、`publication_commit` 与 `old_revision -> (old_logical, disposition,
   new_logical, new_revision)`。不再保留 `normalized`、展开 `rows`、v1 `old_rows/new_rows`、
   `old_entries/new_entries` 或无消费者的 manifest。progress 与 `_unchanged_rows_through_chain`
   同步读取该紧凑元组；changed→reverted 仍不能恢复旧审核覆盖。
5. **生命周期**：reader、行池、tuple 池都属于同一个 `projection_scope(root)`；嵌套 scope
   独立，正常返回与异常退出都在 `finally` 清空并恢复外层 reader。错误不被吞掉，失败不缓存。
6. **每行不再重验 root**：池操作使用已验证 reader 的方法；`active_reader(root)` 只在每份
   catalog/edge 外层调用一次（见 §6 的必要修复）。

## 5. 实现文件

运行时（生产改动）：

- `tools/i18nlib/git_evidence_reader.py`：blob LRU；`GitEvidenceReader.intern_row` /
  `intern_tuple`；`projection_scope` 清理行/tuple 池；跨 root／嵌套 scope 语义保持。
  模块级 `intern_row`／`intern_tuple` 仅作便捷包装（每次调用会重新核验 root，热路径禁止使用）。
- `tools/i18nlib/production_review_v2_lite_queue.py`：`_catalog_paths`／`_catalog_identity`／
  `_ordinary_object`／`_validated_catalog`／`_catalog_view`；`_intern_catalog_rows`；
  `_compact_mapping_rows`；`_validated_migration_edges` 紧凑边；`_migration_chain`、
  `_unchanged_rows_through_chain`、`matching_edges` 改读紧凑字段。
- `tools/i18nlib/production_review_v2_lite_progress.py`：`Progress.observe` 读紧凑元组。

测试与工具：

- `tests/i18n/test_git_evidence_reader.py`：LRU 淘汰／oversize 不驻留／失败重试、
  行与 tuple 整值共享与摘要碰撞拒绝、嵌套／异常 scope 清理与 root 隔离。
- `tests/i18n/test_production_review_v2_lite_queue.py`：catalog 视图命中仍重验候选文件与
  子树、缺文件／symlink／额外文件拒绝、blob 或 manifest 身份变化重新验证、
  等值行跨 catalog 对象复用。
- `tests/i18n/test_production_review_v2_lite_migration.py`：紧凑边与
  `migration.reconcile` 展开结果等价、同 revision 不同 provenance 不共享、scope 退出后
  池清空、链缺失／分叉／循环 fail-closed、catalog 验证成功但后续 batch 失败后再次独立投影。
- `tests/i18n/test_production_review_v2_lite_progress.py`：紧凑元组字段按位置读取，
  `_unchanged_rows_through_chain` 精确身份保留。
- `tools/orchestration/benchmark_projection.py`（新）：单进程单次 `_projection`，
  输出八字段、完整 progress、wall／self／children user+sys、peak self RSS、实现文件摘要、
  HEAD/queue/checkpoint 前后不变检查；`--compare` 校验等价性与冻结阈值，失败返回非零。

前任 EXECUTOR 的部分实现保存在
`.ai/task/perf-projection-20260911/PARTIAL-execute-01.patch`，本轮在其基础上接续，
初始失败测量保存在 `candidate-1.json`（**不覆盖、不冒充验收**）。

## 6. 必要修复：per-row `root.resolve()`

初版实现中 `intern_row`／`intern_tuple` 每次调用 `active_reader(root)`，其中
`root.resolve()` 约 4.6 µs，一轮重放约 500 万次，外推约 23 s，且实测与
`candidate-1.json` 的 self user 增量（+21.5 s）吻合。

修复：把 root/scope 核验提升到每份 catalog（`_intern_catalog_rows`）与每条 edge
（`_compact_mapping_rows`）外层一次，池操作直接调用已验证 reader 的方法。
跨 root／嵌套 scope 语义不变；模块级包装函数仍对未核验调用者做一次核验。

## 7. 实测

### 7.1 初测（失败，保留）

`candidate-1.json`：wall **165.5136 s**、total user **148.39 s**、
peak self RSS **1,884,488 KiB**。八字段与完整 progress 与 baseline 相等；
RSS 通过（≤4 GiB 且 ≤35% baseline）；**wall 与 total user 未过 110% 阈值**。
这只是失败的初测，不作为验收。

### 7.2 修复后可行性（单次）

`candidate-feasibility.json`（本次运行的唯一一次最终代码重放）：

| 项 | candidate | baseline | 冻结上限 |
|---|---|---|---|
| wall | 142.8739 s | 141.7094 s | ≤155.8804 s（110%）→ 通过（+0.8%） |
| self user | 93.42 s | 91.78 s | — |
| children user | 35.22 s | 34.89 s | — |
| total user | 128.64 s | 126.67 s | ≤139.337 s（110%）→ 通过（+1.6%） |
| self sys | 1.23 s | 2.58 s | 单列 |
| children sys | 13.44 s | 12.74 s | 单列 |
| total sys | 14.67 s | 15.32 s | 单列 |
| peak self RSS | 1,884,736 KiB | 14,090,612 KiB | ≤4,194,304 KiB 且 ≤35%（4,931,714 KiB）→ 通过（13.4% baseline） |

- 八字段、完整 progress、HEAD 与 queue/checkpoint 前后不变：全部相等／不变。
- `--compare` 退出码 0（所有检查 passed）。
- RSS 相对 baseline 下降约 **86.6%**；wall 相对 baseline +0.8%，total user +1.6%。
- 这是**单次可行性样本**；SPEC 要求的两次独立 candidate 样本已由 Opus 独立验收完成（§7.3），
  本文件不作为验收记录。

### 7.3 独立验收（Opus，两次串行重放，同一冻结 candidate）

产物：`.artifacts/i18n/perf-projection-20260911/opus-review-0-1/`
（`acceptance.json`、`sample-{1,2}.json`、`unittest.log`）。同 harness、同 treeish
`d95ee7f2`，串行执行，每个重放 `timeout -k 10s 300s`；baseline 未重跑。

| 项 | baseline | sample-1 | sample-2 | 冻结上限 |
|---|---|---|---|---|
| wall | 141.7094446 s | 142.6791682 s | 142.0528916 s | ≤155.8804 s（110%）✅ |
| total user | 126.67 s | 129.19 s | 128.42 s | ≤139.337 s（110%）✅ |
| peak self RSS | 14,090,612 KiB | 1,883,888 KiB | 1,883,524 KiB | ≤4,194,304 且 ≤35%（4,931,714 KiB）✅ |

- 两个样本的八字段与完整 progress 全部与 baseline 相等；root/treeish 相同，HEAD、
  queue/checkpoint 前后不变；`--compare` 均退出 0。
- RSS 降至 baseline 的 **13.4%**（下降约 **86.6%**）；wall +0.68%／+0.24%，total user
  +2.0%／+1.4%。收益是固定输入下的常驻内存下降，**耗时基本持平，不能称为速度优化**。
- 聚焦测试（reader/queue/migration/progress）：`Ran 221 tests in 28.405s`，`OK`，退出 0。
- 独立复审：初轮 Opus5 `normal_review` 与 GPT6 high `cross_review` 为两个不同精确模型的
  独立复审，**均 PASS**（Opus 提出两个 low finding，见 §7.4；GPT6 无 finding）。
- 以上不是速度提升，也不替代 ORCHESTRATOR 的完整 17 项门禁、严格构建与终轮复审。

### 7.4 cycle 1 有界修复（已确认 finding）

只改基准脚本，不改三个运行时文件，也不改计时 `run()` 测量体；两个独立样本继续有效。

- **OPUS-0-1-L1（same_root）**：`compare` 增加 `same_root` 检查，比较 run 规范化后的
  绝对 `root`；root 不同即判失败，避免把不同工作树的测量当成同一基线。
- **OPUS-0-1-L2（参数预检）**：`main` 在昂贵 `run` 之前先校验 `--compare` 文件存在、
  可读 JSON 且 `kind == projection_benchmark`，并预检 `--output`（必须是可写常规文件，
  父目录可建且可写，用一次性 probe 文件探测）。错误参数在 `run` 前即失败，既不浪费一次
  重放，也不截断既有输出；成功测量输出与原失败退出语义保持不变。
- 新增 `tests/i18n/test_benchmark_projection.py`：全部 mock `run`，覆盖缺失／错 kind／
  坏 JSON 的 `--compare`、目录／父路径为文件的 `--output`、被拒参数不截断既有输出、
  `same_root` 不一致失败、有效路径只测量一次并写出报告、冻结阈值不变；并在
  `tests/i18n/test_groups.json` 的 `production-shadow-surface-ledger` 注册。

## 8. 可运行命令

```bash
# 基线（已在运行时代码修改前完成，不要重跑/覆盖）
timeout -k 10s 300s python3 -B tools/orchestration/benchmark_projection.py \
  --root /workspace/tome4-chinese-translation \
  --treeish d95ee7f2eda7ca3ecd2822defe40112645888c30 \
  --output .artifacts/i18n/perf-projection-20260911/baseline.json

# 聚焦测试（四组）
timeout -k 10s 1200s python3 -B -m unittest \
  tests.i18n.test_git_evidence_reader \
  tests.i18n.test_production_review_v2_lite_queue \
  tests.i18n.test_production_review_v2_lite_migration \
  tests.i18n.test_production_review_v2_lite_progress

# 可行性重放（串行，独占机器；已有产物见 §7.2）
timeout -k 10s 300s python3 -B tools/orchestration/benchmark_projection.py \
  --root /workspace/tome4-chinese-translation \
  --treeish d95ee7f2eda7ca3ecd2822defe40112645888c30 \
  --compare .artifacts/i18n/perf-projection-20260911/baseline.json \
  --output .artifacts/i18n/perf-projection-20260911/candidate-feasibility.json

# 完整门禁（本 dispatch 未在主工作树单独跑，主流程在 FINAL_VALIDATE 统一跑）
timeout -k 10s 1800s bash tools/ci-gates.sh
git diff --check
```

约束：**绝不并发跑两个投影**；每个重放自带 `timeout`（300 s + 10 s kill grace）；
`--compare` 不因结果放宽阈值。`peak_self_rss_kib` 取 `RUSAGE_SELF.ru_maxrss`，
不是采样 RSS，也不是 self+children；`peak_children_rss_kib` 仅记录，不参与阈值。

## 9. 剩余工作

- **PERF-2**：publication 查询的历史扫描（2,708 次 `git log`）。6a 需作为独立冻结候选，
  对 merge、shallow、replace/graft、类型变更、目录替换与唯一 publication 做快慢路径差分验收。
- **PERF-3**：CLI 串联（migration 与移动 HEAD 的步骤），涉及事务／checkpoint／恢复边界，
  属契约扩展。
- **PERF-4**：`_tree` 解码缓存为 advisory，未做。
- **PERF-1 验收状态**：独立 Opus 验收（两次串行 candidate 重放 + 221 项聚焦测试）已完成，
  Opus5 normal_review 与 GPT6 high cross_review 两个不同精确模型均 PASS；cycle 1 修复
  L1/L2 已落地并有确定性回归。**剩余**：ORCHESTRATOR 的完整 17 项门禁 + 严格构建、
  FINAL_REVIEW 与 `ai_state_check DONE_VERIFIED`；最终交付状态引用
  `.ai/task/perf-projection-20260911/STATE.json`。
- 说明：本轮收益是固定输入下的实测，不承诺任意全量变化历史的常数内存。
