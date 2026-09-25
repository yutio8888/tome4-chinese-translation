# 审核工具耗时优化：A 环境隔离、B 投影剖析与 B 行校验复用结果

任务：`review-tool-speed-20260925`（implement / infrastructure）。基线
`35cae04614c8710b0287b6d7870f80bdd7c374ea`，工作树
`/workspace/tome4-projection-analysis-20260925`。EXECUTOR 未写主工作树，未 stage／commit／push，
未建立本树生产 queue、checkpoint 或 active batch。派生数据只在本树
`.artifacts/i18n/review-tool-speed-20260925/`。既有
`docs/review278-isolated-analysis-20260925.md` 保留未改。

## A. 父进程 `I18N_PROJECTION_CACHE=on` 时门禁测试失败

### 问题

`gate_results._execute` 不传 `env`，门禁子进程完整继承宿主环境；这与回执
`binding.config_sha256` 中的 `environment_sha256 = digest(dict(os.environ))` 一致。
父 shell 开启缓存后，投影相关测试在 fixture 的 `setUp` 里就已发布并命中磁盘缓存，
测试体里的显式 off 撤销不了已建目录，重放计数也由 1 变 0。

实测（修复前，父 on，`production-shadow-surface-ledger` 组）：532 项中
failures=34、errors=2，分布在 `test_projection_cache`、`test_production_review_v2_lite_queue`、
`test_repair_steps`、`test_projection_stage1` 四个模块。日志 `pre-on-ledger.log`。

### 取舍

SPEC A.3 给了两条路：fixture 显式隔离，或门禁子进程环境策略。选择前者，理由：

- 回执 binding 当前绑定的是父进程完整环境，子进程也确实收到这份环境；
  不改 `_execute` 就不需要新的 gate 环境格式、binding 字段或历史回放兼容层，
  `validate`／`validate_historical` 的要求一个字都没放宽。
- 门禁内的 prepare-evidence 历史读取、以及门禁外的整条批次链，仍然按父进程开关
  命中缓存；只有测试 fixture 自己钉住生产默认值。
- 全局清除父进程环境会让 prepare-evidence 回到完整重放（第 278 批 403.68 s
  补跑的根因），SPEC 明确禁止。

### 实现

- `tests/i18n/test_production_review_v2_lite_migration.py`：新增
  `pin_projection_cache_default(case)`：`mock.patch.dict(os.environ)` 快照后移除
  `I18N_PROJECTION_CACHE` 与 `I18N_PROJECTION_CACHE_TRACE`，`addCleanup` 恢复整个环境。
  `MigrationFixture.setUp` 第一行调用。
- `tests/i18n/test_production_review_v2_lite_queue.py`：`QueueFixture.setUp` 与
  `PublicationHistoryTests.setUp` 第一行调用同一 helper。

这两个基类覆盖所有使用 fixture 的模块（cache、repair、stage1、queue、batch、migration，
`grep` 确认没有其他模块继承它们）。钉在基类 `setUp` 而非 `setUpModule`，
跨模块继承的子类也能自动覆盖，直接 `python -m unittest` 与 `tools/test_groups.py`
两种入口行为一致。缓存测试仍在测试体内用 `mock.patch.dict(os.environ, ON)` 显式开启；
真实 CLI 冷／暖／off 测试（`RealEntryTests`）不变。没有删除测试，也没有放宽计数断言。

### 新增测试

`tests/i18n/test_projection_cache.py::ParentEnvironmentTests`：

- `test_pin_is_scoped_to_the_case_and_restores_the_parent`：父 on + trace 下，
  用例内两个变量都不存在，用例结束后父环境原样恢复。
- `test_direct_unittest_entry_under_parent_on`：子进程父 on，`python -m unittest`
  直接跑三个修复前失败的用例（cache off 断言、repair 重放计数、queue 链计数）。
- `test_test_groups_loader_entry_under_parent_on`：同样三个用例经
  `test_groups.validate_registry`／`load_group` 装载后运行，结束后打印父进程开关仍为 `on`。

`tests/i18n/test_production_review_v2_lite_queue.py::ProjectionChainTests::test_parent_cache_on_prepare_hits_history_keeps_gate_failure_and_retries_alone`
（SPEC A.4，走真实 `tools.i18nlib.cli` 与 `run_batch_steps` 调用链，Git 环境隔离，
门禁仍是既有 `_actual_gate_records` 测试 seam）：父 on 下 `batch.start` 发布当前 HEAD；
`adjudicate=… prepare-evidence` 链在门禁失败时 `_projection` 调用 0 次、有 `hit` 事件，
stderr 暴露 gate 错误，phase 保持 `adjudicated`；随后单独 `prepare-evidence` 成功，
步骤序列只有 `prepare-evidence`（不重复导入裁决），仍为命中，phase 进入 `commit_ready`，
`adjudications` 未变。

负对照：把 helper 临时改成空操作（已恢复），`ParentEnvironmentTests` 三项全部失败，
并连带三个敏感用例共 7 个失败，说明测试确实能抓到回归。

### 验证（本 EXECUTOR 实测，串行、`timeout -k 10s 900s`）

| 命令 | 父环境 | 结果 | 墙钟 |
| --- | --- | --- | ---: |
| `tools/test_groups.py --group production-shadow-surface-ledger` | on | 538 tests OK | 77.43 s |
| 同上 | off | 538 tests OK | 78.29 s |
| `tools/test_groups.py --group toolchain`（含 `test_ci_gates`） | on | 468 tests OK | 26.56 s |
| `tools/test_groups.py --check` | — | PASS | — |

538 = 原 532 + `ParentEnvironmentTests` 3 + prepare-evidence 链 1 + profile harness 2。

一次 on 运行在我运行中新建 `tools/orchestration/profile_projection.py` 时产生 30 个失败，
原因是缓存按设计拒绝在进程启动后改动的 `tools/**.py`（事件
`store-skipped code input modified after process start`）。这是我的并发编辑污染，
不是缺陷；日志另存为 `post-on-ledger.contaminated.log`，随后无编辑重跑全部通过。
**宿主跑门禁期间不要编辑 `tools/` 下代码**，否则缓存测试会按设计失败。

未执行：完整 17 项门禁（含 doctor／build），按 SPEC 交宿主在 on／off 统一执行。

### 回执兼容与命令可用性

- `gate_results.py` 未修改：`VERSION`、check set、binding 字段、`environment_sha256`
  语义、`validate`／`validate_historical` 全部不变，历史 receipt 照常回放。
- 不缓存 gate receipt，不合并跨 HEAD 的 finalize／rebuild，门禁／构建／源码审计数量不变。
- 生产缓存仍默认 off；显式 on 的 shell 可以直接跑完整批次链和门禁，不需要先 unset
  （README 已补一句说明）。

## B. 一次 cache-off 完整投影的函数级剖析

### 方法

新增 `tools/orchestration/profile_projection.py`：复用 `benchmark_projection.run` 的
HEAD／queue／checkpoint 守卫（有 active checkpoint 就拒绝），在唯一一次
`queue._projection(root, commit, progress={})` 外开关 `cProfile`；进程内移除两个缓存变量，
调用处再套 `projection_cache.disabled()`，并断言 `cache.events` 为空。输出目录必须不存在或为空。
配套测试 `tests/i18n/test_projection_optimization.py`（已登记在 ledger 组）：在 fixture 上，
即使父 on + trace，输出 identity 与 cache-off oracle 一致、不建缓存目录、fixture 的
`git status --ignored` 不变；已用过的输出目录和 active checkpoint 都拒绝。
旧 benchmark 的验收阈值未改动。

命令（父进程故意设 on，以证明 harness 自行关闭缓存）：

```
I18N_PROJECTION_CACHE=on timeout -k 10s 900s python3 -B tools/orchestration/profile_projection.py \
  --root . --treeish 35cae04614c8710b0287b6d7870f80bdd7c374ea \
  --output-dir .artifacts/i18n/review-tool-speed-20260925/profile-off-35cae046 --top 60
```

开始前确认无其他投影／测试进程，可用内存 35 GiB。

### 结果（实测，含 cProfile 开销）

- 退出 0；墙钟 423.86 s（进程 424.19 s）；self user 392.42 s，children user 23.79 s；
  峰值 RSS 3,125,876 KiB（约 3.0 GiB）；major faults 0。
- identity：head `35cae046…`，entries 29,828，overrides 24,153，reconciliation 29,828，
  entries_d `a9184a53…`，overrides_d `1b5009a2…`，reconciliation_d `7d2f5aed…`。
- progress：surface_covered 24,153／29,828，deep_reviewed 777，pending_repair 7，
  historical_revision_invalidated 1,772。
- HEAD 前后不变，queue／checkpoint 状态不变。
- `summary.json` sha256 `4031858d…`，`profile.pstats` sha256 `d9536a9f…`。

**这个墙钟不能当基线**：cProfile 在 Python 函数调用密集的路径上开销最大；
第 278 批无剖析的重放约 250 s（rollover 253.52 s），两者不可相减。
下列占比只说明时间在剖析下的分布。

累计时间（cumtime）主干：

| 函数 | 调用 | cumtime | 占 423.9 s |
| --- | ---: | ---: | ---: |
| `_validated_migration_edges` | 1 | 371.16 s | 88 % |
| `git_evidence_reader.derive`（catalog） | 36,477 | 354.35 s | — |
| `_catalog_view` | 704 | 346.18 s | 82 % |
| `_validated_catalog` | **185** | 328.78 s | 78 % |
| `production_review_v2_lite.validate_catalog_files` | **185** | 312.82 s | 74 % |
| `production_review.parse_jsonl` | 1,384 | 113.48 s | 27 % |
| `json.dumps`（canonical 复算） | 22,315,166 | 106.95 s | 25 % |
| `json.loads` | 5,664,070 | 45.73 s | 11 % |
| `surface.entry_revision_identity` | 5,544,267 | 44.72 s | 11 % |
| `_batch_rows` | 335 | 38.59 s | 9 % |
| `subprocess.run`（git） | 11,396 | 32.59 s | 8 % |
| `_plain_id`（call locator） | 5,518,180 | 27.55 s | 7 % |
| `_tree` | 1,558 | 23.20 s | 5 % |

exclusive 热点（tottime）：`json.encoder.iterencode` 74.17 s，`validate_catalog_files`
自身 42.27 s，`select.poll`（等待 git 子进程）27.66 s，`json.decoder.raw_decode` 15.72 s，
`_unique_pairs` 14.42 s，sha256 13.51 s（44.3 M 次），`re.fullmatch` 13.37 s（41.7 M 次）。

### 解读

- 已有的 blob identity 去重生效：704 次 `_catalog_view` 只触发 185 次完整校验；
  行 intern 也生效（`intern_row` 5,518,180 次，7.95 s）。这些不是新收益。
- 剩余成本来自 **185 个互不相同的 catalog 版本各自逐行完整校验**：每行一次
  `json.loads`、一次 canonical `json.dumps` 比对、两次 sha256、`_plain_id`、
  logical／revision identity 各一次复算。
- 补充只读测量（`catalog-line-dup.txt`，10.8 s）：基线历史上
  `evidence/production-review-v2-lite/catalog/entries.jsonl` 恰有 185 个不同 blob，
  共 5,518,180 行（与 `intern_row` 调用数完全一致），但**不同行只有 392,467 条（7.11 %）**，
  约 465 MB。逐行工作有约 93 % 是在不同 catalog 间重复校验完全相同的字节。

### 给 host 的最小优化候选（execute-01 提出；host 已批准，实施见下节「B 实施」）

**投影作用域内、按精确行字节记忆的 catalog 行校验复用。**

- 位置：`validate_catalog_files` 的 entries 逐行段（配合 `parse_jsonl` 的逐行解析），
  只在 `git_evidence_reader.projection_scope` 活跃时启用，作用域退出即释放，
  与现有 `derive`／`rows` 池同生命周期。不跨进程、不落盘、不跨提交。
- 键：**精确行字节**（bytes 作 dict 键，命中时 Python 按全字节比较，没有摘要碰撞绑定，
  符合 `intern_row` 注释里“digest alone is not enough”的约束）＋该行校验读取的
  manifest 上下文：`rules_version`、`terminology_snapshot_sha256`、
  `source_identities[row.component]`。
- 值：已解析且通过全部单行检查的 row 对象（以及该行 digest）。
- 每个 catalog 仍然执行的跨行／文件级检查：revision 严格有序且唯一、logical 唯一、
  component 计数、entries／exclusions 文件 sha256、条目守恒、policy／schema 字节、
  manifest 校验与 `VerifiedRows` 对齐。
- 预期：单行工作从 5.52 M 降到约 0.39 M 次。剖析下单行相关 cumtime 约 200–250 s，
  但无剖析实际节省必须按 SPEC 在实施后用同一输入、同一 harness 冻结前后边界实测；
  这里不给百分比承诺。
- 代价：精确字节键额外约 0.5 GB 峰值内存（当前 3.0 GiB），需在实施时实测；
  若不可接受，替代方案是以 sha256 为键、命中时复算 canonical bytes 比对。这样安全，
  但会保留约 74 s 的 dumps 成本，收益明显变小。
- 必要测试：命中／未命中结果与无记忆 oracle 全等（rows、`VerifiedRows` digests、
  progress、错误信息）；上下文任一字段不同即不复用；非法行在第二个 catalog 出现时照样报错；
  作用域退出后记忆为空；作用域外调用行为不变；超时有界的循环终止探针。

## B 实施：单次投影内逐行成功校验复用（execute-02）

依据 `IMPLEMENT-B.md`。修改前副本为任务目录 `baseline-B/`（与 execute-01 交付一致，
开工时逐文件 sha256 核对无漂移）；整任务最终 diff 基线仍是 `baseline/`。

### 实现

- `production_review.parse_jsonl`：新增可选 `known`（精确行字节 → `(digest, row)`）与
  `lines`（按序收集行字节）。命中只在整行字节相等时发生（bytes 作 dict 键，命中时
  CPython 做全字节比较），复用该行已有的 row 与 digest，不再解析；文件级 LF 检查和其余行
  处理不变。两个参数缺省时与原函数逐字等价。
- `production_review_v2_lite.validate_catalog_files`：新增仅关键字参数 `line_memo`（缺省
  `None` = 原算法，每行完整校验）。对命中行：
  - 跳过纯由行字节决定的单行检查（键集、schema、risk 结构、字符串类型、路径规范化、
    call locator 格式与身份、source/target 哈希与 UTF-8 长度、args_order、logical／revision
    身份复算）；
  - **每次重查**依赖当前 manifest 的三项，且保持原顺序：`rules_version`（支持集且等于
    manifest）→ 跨行有序唯一／logical 唯一 → `source_identities[component]` 与
    `terminology_snapshot_sha256`。给定这三项相等，被跳过的检查只读行字节，结果与原算法相同；
  - 未命中行走原完整检查，通过后先暂存；**只有整个 catalog（含计数、文件哈希、守恒、
    policy、`VerifiedRows` 对齐）全部成功后**才写入 memo。失败的校验什么也不记。
  - 所有跨行与文件级检查（严格排序与唯一、logical 唯一、component 计数、entries／exclusions
    sha256、守恒、policy/schema 字节、manifest 校验）每个 catalog 照常执行；exclusions 不复用。
- `git_evidence_reader.GitEvidenceReader`：新增 `catalog_lines` dict，与 `rows`／`tuples`
  池同生命周期，`projection_scope` 的 `finally` 清空；嵌套作用域是新 reader、新空 memo。
- `production_review_v2_lite_queue._validated_catalog`：仅当 `active_reader(root)` 存在
  （本 root 的投影作用域内）时传入 `reader.catalog_lines`；作用域外或他 root 作用域传 `None`。
  migration、`check_catalog_tree` 等非投影入口不传，仍完整校验。
- 没有新增跨进程、落盘或跨提交缓存，也没有开关；原算法即 `line_memo=None` 路径。

### 所有权

投影内 `_intern_catalog_rows` 本来就把不同 catalog 中字节相同（digest 相同且整行相等）的
row 替换为同一个池化对象交给所有消费者。memo 命中返回的正是首次成功校验时入池的那个对象
（测试断言 `is` 同一：`reader.rows[digest]`、`reader.catalog_lines[line]` 与两个 catalog
的返回行三者相同），所以消费者看到的共享面与改动前完全相同，没有引入新的可变对象共享。
`validate_catalog_files` 自身不修改 row。作用域外无 memo、无 intern，每次返回新对象。

### 测试（`tests/i18n/test_projection_optimization.py`，新增 9 项）

- `CatalogLineReuseTests`：以预热 memo 与无 memo 的完整校验做差分，比较
  (ok/error、异常类型与消息、manifest、rows、`digest_by_revision`、exclusions) 全等，
  16 个正反例：完全相同、超集、单行改动、仅 manifest terminology／fixed source／rules
  变化（行字节相同）、历史 v1 行、同 revision 不同的合法字节、同 revision 非法字节、
  乱序、重复行、logical 重复、非规范行、缺尾 LF、manifest 未重绑的多余行、复用行后跟非法
  新行。拒绝类用例另断言确实命中预定检查。并测：manifest 相关字段命中后仍报错且 memo 不变；
  命中不调用完整单行检查、未命中调用一次；失败校验（空 memo 与已预热 memo 两种）不写入；
  作用域外、他 root 作用域传 `None`，嵌套作用域独立且退出后清空，异常退出后清空，
  下一投影从空开始；复用行与 intern 池对象同一。
- `ProjectionLineReuseTests`：真实 migration 边界 + 批次发布的完整 `_projection`，
  复用与完整校验（patch 掉 memo）的投影元组与 progress 全等，并确认第二个 catalog 确有命中。
- `LineReuseTerminationTests`：子进程 60 s 超时探针，4,000 行全未命中再全命中，终止且返回同一对象。
- `ProfileHarnessTests::test_no_profile_mode…`：`--no-profile` 与 oracle 身份一致、只写 `summary.json`、
  报告的实现哈希等于本树文件。

负对照（临时注入后恢复，sha256 复核一致）：跳过命中行的 fixed source 重查 → 2 项失败；
在整 catalog 成功前写 memo → 4 项失败；作用域不清空 memo → 1 项失败。

| 命令（串行，`timeout -k 10s 900s`） | 父环境 | 结果 | 墙钟 |
| --- | --- | --- | ---: |
| `tools/test_groups.py --group production-shadow-surface-ledger` | on | 547 tests OK | 78.65 s |
| 同上 | off | 547 tests OK | 78.07 s |
| `tools/test_groups.py --group toolchain` | on | 468 tests OK | 26.19 s |
| `tools/test_groups.py --check`，`git diff --check` | — | PASS | — |

547 = 538 + 本轮新增 9。

### 测量（先冻结协议再取样）

协议在第一个样本前写入 `.artifacts/i18n/review-tool-speed-20260925/timing/PROTOCOL.md`
（sha256 `eeb3d911…`），阈值为 host 预先冻结：中位墙钟减少 ≥ 20%，中位峰值 RSS 增长 ≤ 20%。

- 同一 harness：`profile_projection.py --no-profile`（本轮新增模式：同一次
  `queue._projection(root, commit, progress={})`，无 cProfile，cache 环境移除并
  `projection_cache.disabled()`，断言无缓存事件；报告列出实际加载的全部 `tools/` 模块 sha256，
  并拒绝任何从被测仓库 `tools/` 或别处加载的 i18nlib 模块）。
- 同一输入：root 为本工作树，treeish `35cae04614c8710b0287b6d7870f80bdd7c374ea`。
- 基线实现：`.artifacts/…/oracle-b/tools`，为本树 `tools/` 的副本，其中 4 个实现文件取
  `baseline-B/`（与 `35cae046` 逐字节相同）。报告核实 B 与 C 加载的模块集合相同，
  差异恰为 `git_evidence_reader.py`、`production_review.py`、`production_review_v2_lite.py`、
  `production_review_v2_lite_queue.py` 四个文件；harness 文件本身两边相同。
- 串行新进程、无其他测试或投影、取样期间不改 `tools/`（前后 sha256 复核）。
  顺序 B1 C1（可行性）→ C2 B2 B3 C3（交替）。

| 样本 | 实现 | wall_s | total user s | self user s | children user s | 峰值 RSS KiB |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| B1 | 基线 | 252.06 | 243.56 | 219.78 | 23.78 | 3,122,500 |
| C1 | 候选 | 87.74 | 80.41 | 56.74 | 23.67 | 3,543,832 |
| C2 | 候选 | 87.58 | 80.45 | 56.77 | 23.68 | 3,544,520 |
| B2 | 基线 | 251.99 | 243.70 | 220.05 | 23.65 | 3,118,336 |
| B3 | 基线 | 251.47 | 243.73 | 220.06 | 23.67 | 3,122,132 |
| C3 | 候选 | 87.44 | 80.20 | 56.57 | 23.63 | 3,548,924 |

- 正确性：6 个样本 8 个 identity 字段、完整 progress（sha256 `c34b5eff…`）全部相同；
  HEAD 与 queue／checkpoint 前后不变；major faults 均为 0。
- 中位墙钟：基线 251.99 s，候选 87.58 s，比值 0.3475，**减少 65.2%**（门槛 ≥ 20%：通过）。
- 中位峰值 RSS：基线 3,122,132 KiB，候选 3,544,520 KiB，**增长 13.5%**（门槛 ≤ 20%：通过）；
  候选最大 3,548,924 KiB，为基线中位的 1.137 倍。增量约 412 MiB，与剖析时估计的
  约 465 MB 不同行字节量级一致。
- children user（git 子进程）两边都是约 23.7 s，未变；节省全部来自本进程 CPU。
- 原始数据：`timing/{B1,B2,B3,C1,C2,C3}/summary.json`、`timing/comparison.txt`、`timing/samples.log`。

### 限制

- 只测了一台机器、一个 HEAD、cache off、单次投影。缓存 on 且命中时根本不重放，本优化不改变
  命中路径；它缩短的是未命中／完整重放（rebuild、finalize、recover、abandon、migration、
  缓存失效后的首次重放）。
- 峰值 RSS 是 `RUSAGE_SELF.ru_maxrss`；memo 在单次投影内只增不减，没有字节预算。
  若历史继续增长，增量大致随「全历史不同行字节数」线性增长；当前约 0.4 GiB。
- 基线 oracle 是 `.artifacts/` 下的 `tools/` 副本（未跟踪，可重建）；`config.repo_root()`
  等以 `__file__` 定位仓库的代码在副本下会指向副本父目录，投影路径不使用它们，
  且 identity／progress 与候选全等，但该副本不适合跑投影以外的命令。
- 本轮未运行完整 17 项门禁、doctor 与 build，按 SPEC 交 host 在 on／off 统一执行。

次要观察（不建议本轮做）：`_tree` 1,558 次 23.2 s、git 子进程 11,396 次约 32.6 s。
其中批量化 git 是记忆里已有的待办；`_batch_rows` 38.6 s 可待主热点消除后再剖析一次。

## 变更文件

execute-02（B 实施）新增／修改：

- `tools/i18nlib/production_review.py`：`parse_jsonl` 的 `known`／`lines` 可选参数。
- `tools/i18nlib/production_review_v2_lite.py`：`validate_catalog_files(…, line_memo=None)`。
- `tools/i18nlib/git_evidence_reader.py`：作用域内 `catalog_lines`，退出清空。
- `tools/i18nlib/production_review_v2_lite_queue.py`：`_validated_catalog` 在投影作用域内传 memo。
- `tools/orchestration/profile_projection.py`：`--no-profile` 计时模式、实现哈希与加载来源校验、
  `progress_sha256`。
- `tests/i18n/test_projection_optimization.py`：上述 9 项测试。
- `i18n/README.md`：补充 `--no-profile` 与投影内行复用说明。
- 本文。

execute-01（A 与剖析）：

- `tests/i18n/test_production_review_v2_lite_migration.py`：pin helper，`MigrationFixture.setUp` 调用。
- `tests/i18n/test_production_review_v2_lite_queue.py`：导入 helper 与 `projection_cache`；
  两个 fixture `setUp` 调用；新增父 on prepare-evidence 链测试。
- `tests/i18n/test_projection_cache.py`：`ParentEnvironmentTests`（3 项）。
- `tests/i18n/test_projection_optimization.py`（新）：profile harness 测试（2 项）。
- `tests/i18n/test_groups.json`：登记上述新模块到 ledger 组。
- `tools/orchestration/profile_projection.py`（新）：只读剖析 harness。
- `i18n/README.md`：说明开启缓存的 shell 可直接跑门禁，并介绍 profile harness。
- `docs/review-tool-speed-results-20260925.md`：本文。

## 限制与未解决

- 完整 17 项门禁（doctor、lint、build 等）未由 EXECUTOR 运行，交宿主 on／off 统一执行；
  本树 doctor 能否通过（来源配置）未验证。
- prepare-evidence 父 on 集成测试使用既有门禁 seam，不证明真实 17 项门禁通过；
  真实门禁在父 on 下的通过由宿主完整门禁验证。
- B 剖析只做了一次，墙钟含 cProfile 开销；B 实施后的收益与内存已按上节协议实测（3＋3 样本）。
- 实施后未重新剖析；剩余热点（`_batch_rows`、`_tree`、git 子进程）留待后续有证据时再议。
