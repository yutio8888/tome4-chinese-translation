# 投影优化第二阶段结果：同 commit 投影缓存（2026-09-24）

状态：EXECUTOR 实施与测量已完成；cycle 1 修复（FIX-1，见 §8.1–§8.4）、SR-001 修复（FIX-2，见 §8.5）与 NR-001 修复（FIX-3，见 §8.6）已完成，待宿主核验、独立复审和默认启用裁决。缓存**当前默认关闭**，只有显式设置 `I18N_PROJECTION_CACHE=on` 才会启用；本文不宣称缓存已默认上线。

依据：[方案第 4 节](projection-optimization-plan-20260924.md#4-第二阶段只缓存同一-commit-的已提交投影)，[第一阶段结果](projection-optimization-stage1-results-20260924.md)。本阶段不做 HMAC，也不做跨 commit 内容缓存。

下文把两类内容分开标注：

- **实测**：本次运行产出的派生数据，位于 `.artifacts/i18n/projection-opt-stage2-20260924/`（被 Git 忽略）。
- **判定**：依据源码和测试作出的人工判断，未经真实生产流程验证。

## 1. 冻结输入与身份

| 项 | 值 |
| --- | --- |
| 任务 | `projection-opt-stage2-20260924`；baseline 为含 stage1 未提交改动的工作树 |
| HEAD / 测量 commit | `a04b44365f4ad691b07cbef19d0d48cbb0a6a080`，全部 9 个样本、FIX-1 回归 3 个样本及 FIX-2 回归 2 个样本前后不变 |
| 生产 `queue.sqlite3` | 测量前后 sha256 均为 `9cc36cf5…1dbe73`；全程无 active checkpoint |
| 实现指纹 `code_sha256` | 9 个样本相同（compare 检查项 `same_implementation_code_sha256`） |
| 投影身份 | catalog `cdc76147…`；entries 29828，`entries_d a9184a53…`；overrides 24073，`overrides_d 40f91e49…`；reconciliation 29828，`reconciliation_d 7d2f5aed…`。与第一阶段记录一致 |
| 机器 | 16 核、45 GiB；测量期间负载约 1；OS page cache 未控制，三种模式准备方式相同 |

`doctor` 未重跑。本阶段没有改变 Lua、依赖或来源配置，沿用第一阶段的通过记录。

## 2. 实际改动

相对 baseline 的改动文件：

| 文件 | 改动 |
| --- | --- |
| `tools/i18nlib/projection_cache.py`（新增） | 缓存本体：开关、入口作用域、实现指纹、键、严格编解码、Git 复查、原子发布与淘汰 |
| `tools/i18nlib/git_evidence_reader.py` | 新增 `recording()` 和 `note_object()`，只记录重放读到的对象名，不改变读取内容 |
| `tools/i18nlib/production_review_v2_lite_evidence.py` | source evidence 校验成功后，登记 `commit` 与 `commit:path` |
| `tools/i18nlib/production_review_v2_lite_queue.py` | 新增 `_replay`；`_carried` 在读作用域内先查缓存；`init/rebuild/check/status` 改走 `_replay`（关闭时仍是原来的调用）；FIX-2 起 `_replay` 在重放前取 Git 设置快照并交给 `store` |
| `tools/i18nlib/cli_production.py` | `dispatch` 按 (command, action) 打开或重置读作用域 |
| `tools/i18nlib/production_review_v2_lite_batch.py` | 用 `_independent_replay` 包装 `abandon/finalize/recover/recover_from_head` |
| `tools/orchestration/benchmark_projection_cache.py`（新增） | off/cold/warm 基准与 compare |
| `tests/i18n/test_projection_cache.py`（新增）、`tests/i18n/test_groups.json` | 风险测试，登记到 `production-shadow-surface-ledger` 组：初版 33 项，FIX-1 增 2 项，FIX-2 增 3 项，FIX-3 增 3 项，共 41 项 |
| `docs/translation-production-review-v2-lite-plan.md` §2.2、`i18n/README.md`、`docs/agent-workflow.md` | 布局、开关与计时记录说明 |

以下内容未改：`run_batch_steps.py`、`run_repair_steps.py`、migration 模块、旧 benchmark 及其阈值、第一阶段结果文件，以及任何生产 queue、checkpoint、evidence、译文。

### 2.1 数据与格式

- **文件路径**：`.artifacts/i18n/projection-cache-v1/v1-<commit>-<key 摘要前 32 位>.json`。
- **文件结构**：第一行是规范 JSON 头，含 `format`、`key_sha256`、`payload_bytes`、`payload_sha256`；其后是 payload。
- **payload 内容**：
  - 完整 key。
  - projection 五元组：`VerifiedRows` 以行数据加逐行 digest 保存，overrides 和 reconciliation 以 7 元数组保存。
  - 同次重放的完整 progress。
  - 带类型的 Git 对象清单 `[名称, oid, 类型]`。
- **不使用的机制**：pickle、HMAC、第二数据库、事务日志。
- **写入前检查**：
  - 行必须是精确 tuple，且字段类型严格：override 的 attempt 是 `int`（`bool` 不算），可空字段只能是 `str` 或 `None`。
  - 其余值必须能按原类型经 JSON 往返，否则放弃写入。
- **读取时检查**：
  - 头部键集、长度和摘要。
  - 严格 JSON：拒绝重复键和 NaN/Infinity。
  - payload 键集，完整 key 相等。
  - `evidence_head` 等于 commit。
  - 各行结构与类型。
  - `VerifiedRows` 能否重建（要求 revision 唯一、digest 与行对齐）。
  - 任一项失败都按未命中处理。
- **还原**：读取后行恢复为 tuple，entries 恢复为 `VerifiedRows`，`digest_by_revision` 与原来一致。
- **真实载荷（实测）**：54,986,633 字节。512 MiB 上限可容纳 3 个 commit，余量充足，因此不建议调整上限。

### 2.2 键与实现指纹

键由以下部分组成：

- 格式版本。
- `root.resolve()`、`--absolute-git-dir`、`--git-common-dir`。
- 精确 commit。
- Git 设置 `git_settings`（FIX-2 加入，见 §8.5）：`diff.renames` 的有效值，由 `git config --includes --type=bool --get diff.renames` 在仓库根、以重放命令继承的同一环境读取，记为 `true`/`false`/`unset`。布尔别名由 Git 归一；无效值或读取失败时不用缓存。
- 实现身份：
  - `code_sha256`：覆盖运行代码根下 `tools/**/*.py`（跳过 `__pycache__`）、已知无后缀入口 `ENTRY_SCRIPTS`（目前只有 `tools/i18n`，FIX-1 加入）和 `i18n/quality/` 全部普通文件，按相对路径、长度和内容摘要计算。新增、删除和未提交修改都会改变它；遇到 symlink 目录或非普通文件时拒绝缓存。
  - tools 树内的已加载模块必须是现存的 `.py` 文件或 `ENTRY_SCRIPTS` 中的入口，否则拒绝缓存；其他无后缀文件（如 `tools/pi-review`）作为模块加载时仍拒绝。
  - 已加载模块中，位于 stdlib 与该 tools 树之外的模块，按“模块名、路径、内容摘要”计入。本机是 `_distutils_hack` 与 `sitecustomize`；在测试进程中，测试模块也会计入。
  - runtime：Python 版本、实现、cache_tag、解释器 realpath、平台、`git --version` 和 git realpath。

**热改防护**：

- 读取 `/proc/self/stat` 得到进程启动时刻。若任一指纹输入的 mtime 不早于“启动时刻 − 2 秒”，本进程不再使用缓存（poison）。
- 每个进程第一次算出的 `code_sha256` 与 runtime 被冻结。之后任何变化都会 poison 本进程，因此不会把新磁盘字节配给旧的已加载代码。
- 缓存命中和发布前都会重新计算一次。
- 无法取得启动时刻（非 Linux）时关闭缓存。

**非 Python 依赖核对**：

- 判定（源码核对）：catalog 的 schema 与 policy 字节、capacity 注册表都嵌在 Python 常量里，不在目录外读文件。
- 实测：off-1 以 audit hook 记录了一次完整投影期间 `.git` 之外打开的全部文件，只有 6 个惰性导入的 `.pyc`：4 个 stdlib 模块、`tools/i18nlib` 下的 `gate_results`/`production_review_v2_lite_migration`。没有数据文件。对应源码已由 `tools/**/*.py` 覆盖。

### 2.3 命中时的动态复查

1. 重新解析 `HEAD`，得到的 commit 进入键。
2. 用 `queue._publication_git_environment` 检查 Git 环境，与发布快路径使用同一白名单。以下情况都算未命中：未列入白名单的 `GIT_*` 环境变量、未知配置键、shallow、`info/grafts`、`refs/replace`。
3. `git cat-file --batch-check` 逐项比对对象清单，oid 与类型必须完全相同。清单来自成功重放期间实际读到的对象：
   - reader 读取的 commit/tree-ish 与 blob；
   - `validate_source_evidence` 直接用 git 验证的 `commit` 与 `commit:path`，这些对象可以不在 HEAD 的可达范围内。

   只要清单中含 `INCOMPLETE`（名称无法精确复查），就不发布。
4. `git rev-list --objects --quiet <commit>` 检查可达对象闭包是否连通，覆盖 ls-tree 读到但清单没有点名的子树。本仓库约 2.7 万个对象，耗时约 30 ms。这不是 fsck，不校验对象内容。
5. 最后再做一次实现身份复查。

命中只替代“已提交 Git 证据的投影计算”。命中后，调用方的 `strict_check`/`_check_projection`（SQLite schema、integrity、meta、行比对）、checkpoint 与 phase 校验、锁检查照常执行。`batch start` 中的 `_catalog_from_tree` 当前 catalog 校验也照常执行。

### 2.4 入口隔离

| 入口 | 读缓存 | 可写缓存（开关打开时） |
| --- | --- | --- |
| `batch start/surface-export/surface-import/contextual-export/contextual-import/adjudicate/prepare-evidence`、`repair preflight` | 可以，经 `projection_for` 或 `projection_and_progress_for` | 未命中后成功重放即可写 |
| `queue init/rebuild/check/status` | 不读，直接调用 `_replay`，从不经过 `_carried` | 成功重放后可写 |
| `batch finalize/recover/recover-from-head/abandon` | 不读：CLI 不开读作用域，函数本身还被 `projection_cache.independent()` 包装 | 走 `projection_for` 的成功重放可写；直接调用 `_projection` 的路径不写 |
| `batch show/host-block`、`migration plan/check/apply` 及其他 production 命令 | 不读：`entry_scope` 显式重置 | 走 `projection_for` 的成功重放可写 |
| 开关关闭（未设置或非 `on`）及 `projection_cache.disabled()` | 不读 | 不写，也不建目录 |

- `READ_ENTRIES` 是唯一的允许表。`run_batch_steps.py`/`run_repair_steps.py` 通过 `cli_main` 逐步经过同一 `dispatch`，因此 `rollover-chain` 里 rebuild 不读、start 可读；进程内 carry slot 仍然优先。
- `_projection` 保持原签名和原语义，始终可以作为独立 oracle。
- 原算法失败时异常原样抛出，结果不写缓存。
- 缓存读写的任何异常都只记录为 `miss` 或 `store-skipped`，不改变命令的退出码或 stdout。
- 诊断手段：`I18N_PROJECTION_CACHE_TRACE=1` 时，每次决定在 stderr 打印一行 `projection-cache: <event> <reason>`；进程内事件保存在 `projection_cache.events`。常规 stdout 字段不变。

### 2.5 保存、并发与淘汰

- **目录**：逐级 `lstat`，任一级是 symlink 或非目录就放弃。
- **写入**：在同目录内 `mkstemp`，写入后 `fsync`，再 `os.replace`。并发写同一键时允许重复计算，最终文件总是完整的。
- **写入键的 Git 设置**（FIX-2）：`_replay` 在重放前用 `replay_settings` 取一次快照，`store` 重新读取；两者不同或快照不可读就不写，因此不会把某一设置下的重放结果登记在另一设置的键下。
- **读取**：使用 `O_NOFOLLOW`，并用 `fstat` 确认是普通文件且大小有界。
- **上限**：单文件超过 512 MiB 不写。
- **淘汰顺序**：
  1. 先保留刚写入的文件；
  2. 按最近写入时间保留 3 个 commit；
  3. 若总量仍超过 512 MiB，从最旧的文件开始删。
- **淘汰范围**：只删除本目录中匹配 `v1-<40hex>-<32hex>.json` 的普通文件，以及超过 1 小时的本模块临时文件。symlink 和其他文件一律不碰。

## 3. 测试

测试命令如下。宿主统一执行完整门禁，本次 dispatch 未跑：

```
python3 -B -m unittest tests.i18n.test_projection_cache tests.i18n.test_projection_stage1 \
  tests.i18n.test_production_review_v2_lite_queue tests.i18n.test_production_review_v2_lite_migration \
  tests.i18n.test_production_review_v2_lite_batch tests.i18n.test_production_review_v2_lite_progress \
  tests.i18n.test_git_evidence_reader tests.i18n.test_benchmark_projection tests.i18n.test_repair_steps \
  tests.i18n.test_test_groups
```

结果：388 项全部通过，耗时 51.7 s（`focused-tests-1.log`）。另有：

- `python3 -B tools/test_groups.py --check` 通过。
- 已有测试均未修改，第一阶段 19 项仍然通过。

新增的 33 项测试以 `cache.disabled()` 下的原 `_projection` 为 oracle，比较完整 repr、tuple 类型、`VerifiedRows` digest 和完整 progress。覆盖范围：

- **命中等价**：
  - hit 与 oracle 完全相等。
  - `projection_for` 与 `projection_and_progress_for` 命中时不重放；carry 与命中共用结果。
  - 含 unchanged/target_changed/removed（None 字段）的 reconciliation 能精确往返。
- **跨进程**：两个新进程，冷进程重放 1 次并发布，暖进程 0 次重放并命中，两者 digest 与 progress 都等于 oracle。
- **隔离**：
  - 同 commit 的 clone 根目录不共享缓存。
  - 把缓存文件以对方会算出的文件名植入，也因 key 摘要不符而未命中。
- **损坏**：截断、翻转一个字节、空文件、重复键、错误类型、行被改成对象、digest 不对齐、override attempt 改为 `bool`、NaN、另一个 key、symlink 文件。其中重复键、错误类型、行改成对象、digest 不对齐、attempt 改 `bool`、NaN、另一个 key 这些样本都重新签了摘要，只有严格解析能拒绝。每种情况都未命中，随后的重放与 oracle 相等。
- **写失败只影响速度**：oversize（上限打补丁）、目录不可写、目录 symlink、编码器异常，都不影响 rebuild 成功；原算法报错时照常抛出且不写缓存。
- **实现与规则变化（HEAD 不动）**：用伪代码根做了五种改动，每种都在新进程里未命中：修改 `.py`、新增 `.py`、删除 `.py`、修改 `i18n/quality` 文件、在其下新建子目录文件。非 `.py` 的 tools 文件不参与指纹（FIX-1 起 `ENTRY_SCRIPTS` 中的 `tools/i18n` 除外）。
- **热改**：同一进程内改代码后被 poison，改回原内容也不恢复；mtime 晚于进程启动时直接拒绝。
- **Git**：
  - shallow、grafts、replace、未知配置、`GIT_OBJECT_DIRECTORY` 都导致未命中，撤销后恢复命中。
  - 清单中 HEAD 不可达的对象被删除时未命中。
  - 可达 blob 被删除时，命中阶段未命中，随后重放的原错误照常暴露。
  - 未点名的可达子树被删除时，由连通性检查拦下。
  - 含 `INCOMPLETE` 的清单不发布。
- **HEAD 变化**：新增 `tools/ci-gates.sh` 并提交后未命中，重放结果等于 oracle。
- **入口**：
  - 开关关闭时（未设置、`off`、`ON`、`1`、空串）不读、不写、不建目录，也不产生事件。
  - 非允许入口在嵌套于允许作用域内时仍不可读。
  - 缓存有效时，`queue rebuild/check/status` 仍各重放 1 次且不调用 `load`。
  - `finalize/recover/recover_from_head/abandon` 在允许作用域内被调用时，内部读许可为假，`load` 调用 0 次；`recover` 仍完整重放。
  - CLI 实际路径：`queue check` 重放 1 次，随后 `batch start` 命中、0 次重放。
- **活动状态仍独立校验**：
  - 命中后若 SQLite 被篡改，`batch start` 以 drift 失败，不写 checkpoint。
  - 两份相同的 fixture 分别开关缓存运行 `batch start`：退出码与 stdout 相同，SQLite 行、reconciliation、meta 和 checkpoint（除 `created_at` 外）完全相同。重放计数为 on 0 次、off 1 次。
- **并发与保留**：
  - 4 线程同键并发发布，结果是 1 个完整文件且能命中。
  - 4 个 commit 只保留最新 3 个；无关文件、`.bak` 和同名 symlink 不被删除。
  - 总量上限触发时淘汰旧文件，但保留新写入的文件。
  - 陈旧临时文件被清理，新的临时文件保留。
- **基准工具**：
  - fixture 上 off/cold/warm 三种模式的身份与 progress 相同。
  - 没有缓存文件时 warm 拒绝测量；已有输出文件不会被覆盖；存在 active checkpoint 时拒绝测量。
- **终止探针**：新增的扫描循环是 `os.walk`（不跟随 symlink）和 `os.scandir`。探针在 tools 下放一个指向自身的 symlink 目录，用子进程加 20 s 超时运行，立即以 `symlinked directory` 拒绝。

## 4. 真实测量

- 命令：`benchmark_projection_cache.py run --mode <m> --root . --treeish a04b4436…`。
- 执行方式：每个样本都是新进程，逐个串行运行，各自套 `timeout -k 10s 600s`，全部退出码为 0。
- 计时范围：每个样本测量一次 `projection_and_progress_for`（位于 `batch start` 读作用域内）。`process_elapsed_s` 还包含进程启动和导入时间，但不包括报告摘要构造和进程退出，因此不是完整 CLI 命令的端到端耗时。
- **适用范围**：本节 9 个样本属于 FIX-1 之前的候选（`code_sha256` `db0ced6d…`）。FIX-1 改变了实现指纹，其回归样本见 §8.3；本节数据不代表修复后候选。
- 样本顺序：off-1、cold-1、warm-1 是可行性样本；实现未变，随后按 off/cold/warm 交替追加第 2、3 轮，共 9 个样本。cold 运行前只删除本模块的缓存文件。

| 模式 | wall 中位（范围） | 进程总时长中位 | 峰值 RSS 中位（范围） |
| --- | ---: | ---: | ---: |
| off | 250.41 s（249.51–251.43） | 250.62 s | 3,118,508 KiB（3,113,712–3,118,512） |
| cold | 250.26 s（250.09–251.41） | 250.47 s | 3,119,076 KiB（3,118,764–3,120,388） |
| warm | 0.280 s（0.277–0.281） | 0.477 s | 360,888 KiB（360,672–362,228） |

`compare-3x.json`（sha256 `92bdb6d8…`）的全部检查项都通过：

- 9 个样本身份一致、progress 一致；HEAD 与 queue 未变；实现指纹和 harness 指纹一致。
- warm 中位为 off 的 0.11%，门槛 ≤ 20%。
- cold 中位为 off 的 99.9%，门槛 ≤ 110%。
- cold RSS 中位为 off 的 100.02%，门槛 ≤ 110%。

解读：

- 冷路径的附加成本（收集进度与对象、batch-check、编码约 55 MB、fsync）小于样本间波动，本次没有单独拆出这部分时间。
- 暖命中约 0.28 s，其中包括指纹计算、Git 环境检查、batch-check、连通性检查、读取与校验 55 MB 文件；峰值 RSS 约 0.36 GB。

样本文件 sha256：

- off-1/2/3：`3e170141…`、`ea23badf…`、`ab30e986…`
- cold-1/2/3：`375a7367…`、`fb3e879f…`、`5eab1a3a…`
- warm-1/2/3：`1cbb0665…`、`ee224e82…`、`c0282c32…`

## 5. 端到端影响（判定，非实测）

下面是依据第一阶段计数和代码路径作出的**估算**。本次没有在隔离副本上跑完整审核流程的 A/B 对比，因此**不宣称端到端实测提速**。

- **可节省的部分**：一个审核批次中，rollover-chain 的 rebuild 会发布缓存（rebuild 本身仍完整重放）。随后在同一 commit 上作为独立进程运行的 surface-export、surface-import、contextual-export 和 adjudication-chain，理论上都可以命中。每个命中步骤约省 250 s，合计约省 1000 s。
- **不变的部分**：finalize 与 post-closure rebuild 在新 commit 上独立重放；prepare-evidence 的门禁和 `batch start` 的当前 catalog 校验也不受影响。
- **修复窗口**：repair preflight 可以命中，前提是同一 commit 此前已有成功的发布重放，例如之前跑过 rebuild、check 或 status。

## 6. 默认启用建议（供宿主裁决）

建议分两步：

1. **先在宿主流程中显式启用（`I18N_PROJECTION_CACHE=on`）至少一个完整批次。** 用 `run_batch_steps` 的 `projections=0/1` 和 `I18N_PROJECTION_CACHE_TRACE=1`，核对实际命中的入口，并记录真实工具链总时间。
2. **确认无误后再改默认值。** 默认范围只覆盖 §2.4 表中列出的普通读取入口；恢复、finalize 和 queue 命令保持不读。改默认需要另行修改开关判断（`enabled()`），属于本任务之外的一次小改动，并需同步文档。

## 7. 偏差、未测项与未解决问题

- **未改动文件**：`run_batch_steps.py` 与 `run_repair_steps.py` 都在允许范围内，但没有改动。命中后 `projections=0` 已足够说明结果，stderr 不再追加字段。
- **publish 耗时**：cold 路径的发布成本没有单独计时，只能说明它低于样本波动。
- **未做真实 A/B**：没有在隔离副本上重放完整审核或修复流程，只在 fixture 里比较了 `batch start` 的 on/off 结果。
- **指纹的已知边界**：
  - mtime 可以被人为回拨，例如 `touch -d` 或 `cp -p`。如果在进程启动之后、首次计算指纹之前替换了文件并回拨 mtime，就会漏检。这符合个人项目的威胁模型，已接受。
  - 同一进程中途首次导入某个第三方模块，只会导致键不同而未命中，不会误命中。
- **内容完整性**：对象复查只检查存在性、类型和可达闭包连通，不做 fsck。对象内容损坏仍由独立无缓存重放和 Git 自身报错暴露。
- **残留缓存文件**：生产工作树的 `.artifacts/i18n/projection-cache-v1/` 中留有测量产生的 1 个缓存文件（约 55 MB，commit `a04b4436`）。它是可删除的派生产物；开关关闭时不会被读取。是否保留由宿主决定。
- **完整门禁**：完整共享链门禁由宿主统一执行，本 dispatch 未运行（FIX-1、FIX-2、FIX-3 之后同样未运行）。
- **FIX-1 之前的缺陷**：§3、§4 的测试和测量都不经过 `tools/i18n` 入口（harness 与测试直接导入模块），因此没有发现 R1。修复前经标准入口运行的正式 CLI 从不读写缓存，见 §8.1。

## 8. 修复记录（FIX-1、FIX-2、FIX-3）

### 8.1 R1：标准入口从不读写缓存（已确认、已修复）

- **缺陷**：`python3 -B tools/i18n …` 运行时，`__main__.__file__` 是无后缀的 `tools/i18n`。`_loaded_modules` 要求 tools 树内的已加载模块都是 `.py`，于是每次都以 `loaded tools module has no current source file: __main__` 拒绝。正式 CLI 因此从不读、也从不写缓存；业务结果不受影响，只是没有提速。
- **修复**（`tools/i18nlib/projection_cache.py`）：新增 `ENTRY_SCRIPTS = {tools/i18n}`。`_code_digest` 把该入口的路径、长度和字节计入 `code_sha256`，`_loaded_modules` 只放行这个已知入口。其他无后缀文件（如 `tools/pi-review`）既不计入指纹，作为模块加载时也仍然拒绝。热改防护照旧适用于入口：mtime 晚于进程启动或同进程内字节变化都会拒绝。`tools/i18n` 本身未改。
- **负对照（实测）**：在代码副本中把判断还原为只认 `.py`，经标准入口在 fixture 上运行两次 `batch start`，两次都是 `miss`/`store-skipped …: __main__`，且没有建出缓存目录（`fix1-negative-control/trace.txt`）。

### 8.2 新增测试（`RealEntryTests`，2 项）

- **真实入口端到端**：把 `tools/` 与 `i18n/quality/` 复制到临时代码根，以子进程运行 `python3 -B tools/i18n production batch start --limit 1`，仓库根指向隔离 fixture（`I18N_REPOSITORY_ROOT`）。不调用 `cli.main`，也不伪造 `__main__`。
  - 冷：`stored`，无 `hit`，写出 1 个缓存文件。
  - 用同一入口 `batch abandon`（不读缓存），恢复初始状态。
  - 暖（新进程）：`hit`，无 `miss`；stdout 与冷运行相同；HEAD 与 `git status --porcelain --ignored` 与冷运行后相同。
  - off（fixture 的副本，另建）：无任何 cache trace，不建目录，stdout 与冷运行相同。
  - 入口字节变化（HEAD 不动）：在副本的 `tools/i18n` 末尾追加一行注释，新进程为 `miss no cache file for this key`，不命中旧文件；stdout 不变，目录中变为 2 个文件。
- **只认已知入口**：`__main__` 指向 `tools/i18n` 时通过，指向 `tools/pi-review` 时拒绝；改 `tools/pi-review` 不改变 `code_sha256`，改 `tools/i18n` 会改变。

测试结果（实测）：§3 同一条命令共 390 项全部通过，耗时 53.9 s（`fix1-focused-tests.log`）；`python3 -B tools/test_groups.py --check` 通过。

### 8.3 真实投影回归（实测）

与 §4 相同的命令、仓库与 commit，off-1、cold-1、warm-1 各一个新进程，串行运行，各自套 `timeout -k 10s 600s`，退出码全部为 0。运行前后 HEAD 均为 `a04b4436…`，`queue.sqlite3` 均为 `9cc36cf5…`，无 checkpoint（`fix1-pre.txt`/`fix1-post.txt` 相同）。

| 模式 | wall | 进程总时长 | 峰值 RSS | 缓存事件 |
| --- | ---: | ---: | ---: | --- |
| off | 251.36 s | 251.57 s | 3,114,984 KiB | 无 |
| cold | 250.49 s | 250.70 s | 3,118,700 KiB | `miss no cache file for this key` → `stored` |
| warm | 0.283 s | 0.479 s | 364,436 KiB | `hit` |

`fix1-compare.json`（sha256 `9929a3a8…`）全部检查项通过：身份与 progress 一致（entries_d `a9184a53…`，与 §1 相同），HEAD 与 queue 不变，三个样本的实现指纹相同，为新值 `69ddc27c…`。按比例计算，warm 为 off 的 0.11%，cold wall 为 99.7%，cold RSS 为 100.1%。

这只是每种模式 1 个样本的回归对比，不是新的 3 轮中位数；§4 的 3 轮数据只属于修复前候选。harness 直接导入模块，不经过 `tools/i18n` 入口，因此标准入口的功能验收以 §8.2 的隔离 fixture 为准。样本 sha256：off `a7a94faa…`、cold `50e4fcaa…`、warm `1bf0a8d7…`。

生产工作树的缓存目录现在仍只有 1 个文件：cold 按 harness 规则先删除了旧键文件，随后写入新键文件 `v1-a04b4436…-136069d0….json`。

### 8.4 SR-001：`diff.renames` 与候选提交（FIX-1 时的诊断记录）

> 本小节是 FIX-1 当时的有界实验，结论只适用于其 fixture（历史中该路径始终是文件）。宿主随后在“历史目录→文件”边界复现了差异，SR-001 已确认为缺陷并在 FIX-2 修复，最终裁决见 §8.5。

- **相关调用**（`production_review_v2_lite_queue.py`）：`_candidate_commits`（第 340 行）和 `_migration_publication_commit`（约第 1435 行）都运行 `git log --full-history --format=%H --diff-filter=AM <treeish> -- <path>`。其中 path 取自 `_tree`（`ls-tree -r`，只列 blob）或已校验为 blob 的证据文件路径，都是单个文件路径。调用中没有 `--follow`，并且 `_publication_git_environment` 只接受 `log.follow` 为假。
- **有界 fixture 实验（实测，git 2.39.5）**：结果在 `fix1-sr001-diagnosis/result.txt`。临时仓库中依次提交：新增 `d/old.json`；纯改名为 `d/new.json`；修改；改名兼修改为 `d/new2.json`；再合入一个侧分支。在 `diff.renames` 未设、`true`、`false` 三种设置下，逐一对三条路径直接调用真实的 `_candidate_commits`，结果完全相同，环境检查也都通过。作为对照，对目录 `d` 使用 pathspec（源码中不存在这种调用）时，`true` 与 `false` 的结果不同。
- **机制说明**：路径限定先于改名检测生效，改名的另一端不在比较集合里，因此单文件 pathspec 不会被判为 `R`。
- **当时结论（已被 §8.5 取代）：该 fixture 未复现，未修改**。另有一个理论边界：某条证据路径在历史上曾是目录，后来某次提交把目录换成同名文件，且目录内文件与该新文件内容相近。此时两端都匹配这个 pathspec，改名检测有可能介入。这个情形没有做实验。候选提交随后还要逐一比对该路径的 blob 与父提交，但本次不据此断言结论。此项交宿主裁决。

### 8.5 FIX-2：SR-001 已确认并修复

#### 8.5.1 裁决

- **SR-001 是缺陷（宿主已确认）**。宿主在 `HOST-SR001-BOUNDARY.json` 中给出复现：先提交目录 `x/child`，再把同样的字节移成文件 `x` 并删除原目录。对当前是单文件的 `x` 运行源码原命令 `git log --full-history --format=%H --diff-filter=AM HEAD -- x`（git 2.39.5）：`diff.renames=true` 时只返回最初提交目录的那个提交；`false` 时还会返回目录换成文件的那个提交。
- **影响**：`_candidate_commits` 与 `_migration_publication_commit` 随后都要求候选提交里该路径的 blob 与当前一致、父提交等于 `base_commit`。候选集合变了，定位到的发布提交就会变，整次重放可能从成功变成失败，或者反过来。`_publication_git_environment` 把 `diff.renames` 的 true/false 都视为合规环境，而修复前的缓存键不含这个值，因此在一种设置下写入的结果会在另一种设置下命中。
- **§8.4 的适用边界**：FIX-1 的实验只覆盖“路径在历史中始终是文件”的纯改名、修改、改名兼修改和合并，那些情形下结论仍然成立（单文件 pathspec 不会被判为 `R`）。它没有覆盖“历史上曾是目录”的边界，所以不能用来否定本缺陷。
- **可到达的调用**（判定，源码核对）：批次证据路径（`batches/<batch>/…`）不含 `base_commit` 的摘要，可以出现上述历史，见 §8.5.3 的 fixture。migration 路径是 `migrations/<migration_id>.json`，而 `migration_id` 是含 `base_commit` 的内容摘要；要让 `base_commit` 本身事先包含以这个摘要命名的目录，几乎不可能构造出来。因此 fixture 走批次路径。缓存键修复对两类调用同样有效。

#### 8.5.2 修复（`tools/i18nlib/projection_cache.py`、`tools/i18nlib/production_review_v2_lite_queue.py`）

- **键**：新增 `git_settings = {"diff.renames": <值>}`。读取命令是 `git config --includes --type=bool --get diff.renames`，在仓库根执行，继承与重放中所有 `_git` 调用相同的进程环境，因此 `include.path`/`includeIf`、`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` 的效果都由 Git 自己解析。
  - 未设置（退出码 1、无输出）记为 `unset`，与 `true`、`false` 区分，不假定 Git 的默认值。
  - 布尔别名（yes/on/1、no/off/0）由 `--type=bool` 归一为 `true`/`false`。
  - 其他值（例如 `copies`，环境检查本来也拒绝）或读取失败：抛出 `_Skip`，本次不读也不写缓存。
- **写入身份与重放一致**：`_replay` 在完整重放之前调用 `replay_settings(root)` 取快照（不可读时为 `None`），`store(..., settings=快照)` 在写入前重新读取。两者不同或快照为 `None` 时，记为 `store-skipped git settings changed or unreadable during the replay`，不写入。`store` 的 `settings` 是必填关键字参数。
- **同进程切换**：每次 `load`/`store` 都会重新读取设置，键随设置变化，所以同一进程中切换设置后找不到旧键的文件。
- **未改动**：独立重放、发布快路径和 `_candidate_commits`/`_migration_publication_commit` 的算法与语义都没变，`_publication_git_environment` 也没变。没有加入 HMAC，也没有跨 commit 缓存。默认仍为关闭。
- **有意不纳入键的设置**（判定）：环境白名单只额外允许 `log.follow`（只接受假值，而“未设置”本来就等于不跟踪）、若干 `core.*` 工作树设置、`include*`，以及 `user.`/`remote.`/`branch.`/`credential.`/`safe.`/`init.`/`filter.` 前缀。这些都不影响本重放所用的 `log`/`ls-tree`/`cat-file`/`rev-parse`/`rev-list` 的输出。`core.precomposeunicode` 只在 macOS 上生效，runtime 中的 `platform` 已进入键。
- **已知边界**：快照与写入前各读一次设置。如果设置在重放期间被改动后又改回原值，两次读取一致，无法察觉（ABA）。这与 §7 记录的指纹 mtime 边界属于同一类，已接受。

#### 8.5.3 新增测试（`GitSettingsTests`，3 项）

- **目录→文件的真实历史**：在隔离 fixture 中新增批次 `boundary`。它的发布基线提交中，`…/raw/translation_surface_screen_v1/input.json` 是目录 `input.json/child`，内容与后来的文件完全相同；发布提交再把这个目录换成同名文件，manifest 的 `base_commit` 指向该基线。
  - 直接调用真实的 `_candidate_commits`：`false` 时发布提交排在第一位；`true` 时发布提交不出现。
  - 无缓存 oracle（`cache.disabled()` 下的原 `_projection`）：`false` 时重放成功；`true` 时抛出 `durable batch core/raw files were not published in one commit …`；未设置时与 `true` 相同（git 2.39.5）。
  - 同一进程依次切换 `false → true → 未设置 → false → true`，每次都走真实读路径 `projection_and_progress_for`（`batch start` 读作用域，开关打开）：`false` 首次写入、之后命中，结果与 oracle 完全相同；`true` 和未设置都是 `miss`、没有任何 `hit`，抛出的错误与 oracle 的错误文本相同，且失败结果不写入。目录中始终只有 1 个文件；最后切回 `false` 时命中。
- **取值与读取失败**：`true`/`yes`/`on`/`1` 都归一为 `true`，`false`/`no`/`off`/`0` 都归一为 `false`，未设置为 `unset`。在 `on` 下写入后，改为 `1` 仍命中，改为 `off` 则未命中（`no cache file for this key`）。设为 `copies` 时 `replay_settings` 返回 `None`，`_git_settings` 抛出 `_Skip`，读取未命中。经 `include.path` 引入的设置能被读到。
- **写入身份不一致时不写**：快照为 `true`、实际重放在 `false` 下完成，或快照为 `None` 时，`store` 返回 False，原因为 `git settings changed or unreadable during the replay`，也不产生文件。经真实 `_replay` 路径模拟“快照后设置被改”，结果相同。
- **负对照（实测）**：在代码副本中把键里的设置固定为常量，并去掉写入前的比对，即修复前的行为。同一测试失败 3 处：`true`、未设置、第二次 `true` 都命中了 `false` 下写入的成功结果，而 oracle 在这些设置下抛出错误（`fix2-negative-control/result.txt`）。

测试结果（实测）：§3 同一条命令共 393 项全部通过，耗时 54.8 s（`fix2-focused-tests.log`）；`python3 -B tools/test_groups.py --check` 通过。日志中出现的 `GATES FAILED`、`FAILED comparison checks` 是已有负向测试的预期输出。

#### 8.5.4 真实投影回归（实测）

按 FIX-2 briefing，这次不再跑 off，只跑 cold-1 与 warm-1。与 §4 同一 harness、仓库与 commit，两个新进程串行运行，各自套 `timeout -k 10s 600s`，退出码均为 0。运行前后 HEAD 均为 `a04b4436…`，`queue.sqlite3` 均为 `9cc36cf5…`（`fix2-pre.txt`/`fix2-post.txt` 相同）。运行期间和运行后都确认 `active-batch.json` 不存在（`fix2-checkpoint-during.txt`）；harness 自身也会拒绝在有 checkpoint 时运行。

| 模式 | wall | 进程总时长 | 峰值 RSS | 缓存事件 |
| --- | ---: | ---: | ---: | --- |
| off（沿用 FIX-1 的 off-1） | 251.36 s | 251.57 s | 3,114,984 KiB | 无 |
| cold（FIX-2） | 250.52 s | 250.74 s | 3,119,572 KiB | `miss no cache file for this key` → `stored` |
| warm（FIX-2） | 0.280 s | 0.476 s | 362,624 KiB | `hit` |

- 生产仓库未设置 `diff.renames`（`git config --get` 退出码 1），写入文件的键中记为 `{"diff.renames": "unset"}`。文件 54,986,673 字节，比 FIX-1 多 40 字节，差额就是这个键字段。
- `fix2-compare.json`（sha256 `e6de69b0…`）以 `fix1-off-1` 加本次两个样本作比较：身份一致、progress 一致，HEAD 与 queue 不变，harness 指纹相同；warm/off = 0.11%，cold/off wall = 99.7%，cold/off RSS = 100.1%，均在预定门槛内。
- compare 的退出码为 1，唯一失败项是 `same_implementation_code_sha256`：off 样本属于 FIX-1 指纹 `69ddc27c…`，本次两个样本属于 FIX-2 指纹 `60452c87…`。这是 briefing 规定“与既有 off 比对”的必然结果，不是回归问题。
- **统计界限**：每种模式只有 1 个样本，off 来自前一个实现指纹，不能当作新的 3 轮中位数；§4 的 3 轮数据只属于 FIX-1 之前的候选。harness 直接导入模块，不经过 `tools/i18n` 入口。样本 sha256：cold `bf8b2032…`、warm `a19e8030…`。
- 生产缓存目录现在只有 1 个文件：cold 按 harness 规则先删除了 FIX-1 键文件，随后写入 `v1-a04b4436…-11c03732….json`。

#### 8.5.5 未解决与偏差

- 完整共享链门禁没有运行，由宿主统一执行。
- `fix2-pre.txt`/`fix2-post.txt` 的 checkpoint 行沿用了错误的判定方式（按文件名中是否含 “checkpoint” 查找）。实际的 checkpoint 文件名是 `active-batch.json`，已另行确认它不存在，见上文。
- 默认启用建议（§6）不变，仍由宿主裁决。

### 8.6 FIX-3：NR-001 打开 FIFO 时阻塞（已确认、已修复）

#### 8.6.1 裁决与修复

- **NR-001 是缺陷（宿主已确认）**。`load` 在 `fstat` 之前用 `O_RDONLY | O_NOFOLLOW` 打开缓存文件。如果该键的文件名是一个没有写端的 FIFO，`open` 本身就会阻塞，进程卡死，而不是 miss 后回算。宿主的 1 秒超时探针（`HOST-NR001-PROBE.json`）已复现。
- **修复**（`tools/i18nlib/projection_cache.py`，仅 `load` 的一行 flags 加一行注释）：打开时加上 `O_NONBLOCK`。打开后照旧对同一个 descriptor 做 `fstat`，只接受常规文件且不超过大小上限的情况，所以 FIFO 等非常规文件会以 “cache file is not an ordinary bounded file” miss。对常规文件，`O_NONBLOCK` 不影响 `read` 的结果（判定）。`store` 用 `os.replace` 发布，`_evict` 用 `lstat` 跳过非常规文件，两处都不会打开 FIFO，未改动。
- 其他前序修复全部保留，默认仍关闭。

#### 8.6.2 新增测试（`FifoCacheFileTests`，3 项）

每次打开都在子进程里进行，并设短超时（20 s）。所以即使回归，测试也会有界结束，不会挂住测试进程。缓存由一个新子进程先冷跑写入（键必须是新进程算出的那个），随后删掉该文件，并在同名位置 `mkfifo`。

- 修复后的 `load` 很快 miss，原因正确；随后普通调用重放 1 次，digest 与 progress 都等于无缓存 oracle。
- 原重放失败（spy 抛出 `ProductionReviewError`）时，错误照常传播；FIFO 原样保留，没有被写入。
- 负对照：对同一个 FIFO 使用旧 flags 打开，2 s 内触发 `TimeoutExpired`。`subprocess.run` 超时后会结束子进程。

#### 8.6.3 验证（实测）

- `python3 -B -m unittest tests.i18n.test_projection_cache tests.i18n.test_projection_stage1 tests.i18n.test_test_groups`：67 项通过，16.6 s（`fix3-focused-tests.log`）。
- §3 同一组关联测试：396 项通过，57.6 s（`fix3-associated-tests.log`）。其中 FIX-2 时为 393 项，新增的就是这 3 项。
- `python3 -B tools/test_groups.py --check` 通过。测试文件已按文件登记，`test_groups.json` 不需要改动。
- **负对照**：在 `/tmp` 的代码副本中去掉 `O_NONBLOCK`，并把 mtime 回拨，以免触发热改防护。`FifoCacheFileTests` 在该副本里 2 项 error，均为 20 s 时的 `TimeoutExpired`，负对照项通过，耗时共 43.0 s（`fix3-negative-control/result.txt`）。工作树中的源码从未被改动。
- 测试前后 HEAD 均为 `a04b4436…`。生产缓存目录仍只有 FIX-2 写入的那个文件，没有产生新文件；测试只使用临时 fixture。

#### 8.6.4 未重测与未解决

- **没有重跑真实全量投影**（按 FIX-3 briefing）。§4、§8.3、§8.5.4 的耗时与内存都属于各自旧的实现指纹。FIX-3 改变了 `code_sha256`，新候选没有同版本的 off/cold/warm 样本，更没有 3 轮中位数验收。判定：这次修复对常规文件的读取内容不变，预计性能不受影响，但这一点未经测量。
- §8.5.4 的 compare 退出码为 1（跨指纹比对）。本文不宣称任何一次 compare 全部通过，也不宣称新候选已通过预定门槛。
- 生产目录中已有的缓存文件使用 FIX-2 的键，FIX-3 之后不会命中，只会 miss 后重算。它仍是可删除的派生产物。
- 完整共享链门禁没有运行，由宿主统一执行。默认启用建议（§6）不变。
