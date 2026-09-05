# 生产译文审核 WP2-Lite 实施计划

## 0. 文档状态与目标

本文是个人维护者可实施的 WP2-Lite 正式审核计划，不是当前工具契约。实施必须另建任务、受审并通过本文门禁后才能启用正式 writer。本文只规划正式 catalog、一个本地队列、一个活动批次、现有 Paseo 审核适配、批次证据、修复边界和 WP1 退役；不启动全量审核。

冻结基线为 commit `a287652`。WP1 当前向量是 30,308 occurrences，其中 29,828 eligible、480 exclusions；这些数是该版本向量，不是永久常量。WP1 的全部 marker 仍为 false，既不能派发，也不能改标、提升或成为正式身份的父记录。

## 1. 可复用能力与硬约束

### 1.1 WP1 可直接复用的算法

实现应复用并在新 schema 下重新运行以下已测试能力，而不是重写第二套：

- `LocaleDocument.translations` 的稳定枚举及 11-component 守恒；
- occurrence、locator allocation、风险字段、terminology snapshot 和 typed source identity 的提取；
- UTF-8、sorted-key、compact JSON、禁止 NaN、JSONL 末尾 LF 的 canonical 编码；
- manifest/loader/terminology/source identity 漂移检查；
- 80 条稳定优先排序、catalog/batch 集合守恒和 reconciliation；
- ordinary-file、no-symlink、原子文件写入、目录 fsync、128 MiB 占用预检；
- production、surface manifest/result、translation ledger focused tests。

复用的是实现和测试能力，不是 WP1 的 locator、catalog、policy、journal、checkpoint、batch ID 或 bytes。

### 1.2 个人项目尺度原则

以下是实现验收条件，而非风险免责声明：

1. 只支持单机、单维护者、单工作树 writer；仓库级一把排他锁覆盖所有写操作。
2. Git commit 保存长期历史；运行时只恢复尚未提交的当前批次。
3. 恢复点只有批次开始前、审核结果汇总前和 commit 前；活动批次内部不追求逐操作历史证明。
4. catalog 中 eligible 且没有例外记录的 revision 隐式为 `queued`，禁止为全量默认行写初始化记录。
5. 只有一个 authoritative catalog、一个 SQLite 队列文件和一个活动批次 checkpoint。
6. 删除运行时文件后，必须能从当前 authoritative catalog 与已提交 evidence 重建同一当前状态。
7. 新机制必须对应 WP1 已见漂移/崩溃测试、现有 consumer 要求、pilot 观察或明确用户目标。
8. 业务状态最多七个：`queued|reserved|screened|deep_required|repair_required|done|blocked`。

### 1.3 非目标与不保证事项

WP2-Lite 刻意不保证：

- 多 writer、跨主机并发、公平调度、恶意同用户防护或远程服务高可用；
- 每次 SQLite page 写入都对应可审计的长期事件；
- 活动批次中途修改 catalog、译文或术语后仍能续跑；
- surface `OK` 等同于语义深审，或 `done` 等同于“永不再审”；
- 自动裁决 observation、自动修改译文、自动改变术语库或自动开始余下数万条；
- 对 ambiguous/unmapped identity 作猜测；
- 用一套额外的代际历史系统复制 Git 的职责；
- 为每个默认 queued revision 建立初始 transition；
- 在 pilot 尚未通过时提供 daemon、Web UI、指标平台或跨批预取。

## 2. 唯一路径布局与责任边界

### 2.1 受跟踪权威数据

正式实现只使用以下新前缀：

```text
i18n/quality/production-review-v2-lite/
  catalog-v1.schema.json
  queue-v1.schema.sql
  active-batch-v1.schema.json
  evidence-v1.schema.json
  policy-v1.json

evidence/production-review-v2-lite/
  catalog/manifest.json
  catalog/entries.jsonl
  catalog/exclusions.jsonl
  migrations/<migration_id>.json
  batches/<batch_id>/manifest.json
  batches/<batch_id>/results.jsonl
  batches/<batch_id>/adjudications.jsonl
  batches/<batch_id>/gates.json
  batches/<batch_id>/raw/<contract>/<run_id>/<accepted-input-or-output>
```

`catalog/` 恰好表示当前 checkout 的一个权威 catalog。旧 catalog 的长期 bytes 由 Git commit 保存，不在工作树保留多份快照。`migrations/` 只保存实际 catalog 边界的一次 reconciliation 结果；一个边界恰一个文件。`batches/` 保存人工审核结论及复核所需锚点。

### 2.2 唯一运行时数据

```text
.artifacts/i18n/production-review-v2-lite/queue.sqlite3
.artifacts/i18n/production-review-v2-lite/active-batch.json
.artifacts/i18n/production-review-v2-lite/repository.lock
```

- `queue.sqlite3` 是唯一持久队列实现，使用 Python 标准库 `sqlite3`；它是可重建投影，不进 Git。
- `active-batch.json` 是唯一 coordinator checkpoint；没有活动批次时必须不存在。
- `repository.lock` 是唯一写锁：Linux/POSIX 下用 Python 标准库 `fcntl.flock(fd, LOCK_EX|LOCK_NB)`，从 writer preflight 一直持有同一 fd 到写入、fsync 和校验结束；争锁失败立即退出。锁只保护合作进程，不声称抵御恶意进程。
- SQLite 自身短暂的 `-wal/-shm` 或 journal sidecar 只是数据库实现细节，必须位于同一 ignored 目录，不能成为第二个队列或长期事实来源。

现有 surface/contextual 契约要求的 `.ai/task/...` envelope、manifest、STATE 与 `.ai/reviews/...` raw 输出保持原路径和 schema；它们是 Paseo task artifact，不是第二个 coordinator checkpoint。WP2-Lite 记录运行时 exact path/hash、调用现有 validator，并按第 7.2 节只复制 validator 实际接受的 adapter input/output bytes 到本批 tracked raw evidence；不改写 consumer 字段。

## 3. Authoritative catalog

### 3.1 新身份与输入绑定

正式 build 必须从届时 live input 重新 harvest，不读取 WP1 ID 作为 seed 或 parent。除 migration record 外，所有正式对象使用 `schema_version=1`；migration record 的 exact-version 分派与兼容规则见第 8.1 节。所有正式对象使用 `kind=production_review_v2_lite_*`，从而与 shadow kind 明确分离。

`call_locator` 的 core 恰含：

```json
{"component":"...","duplicate_index":0,"function_name":"t","normalized_source_tag":"...","section":"...","source":"...","translation_path":"..."}
```

路径是规范化仓库相对 POSIX 路径；null tag 规范为 `""`。`call_locator = SHA-256(UTF-8 canonical({"kind":"production_review_v2_lite_call_locator_v1","locator":core}))`。禁止裸行号。若未来同 core 出现重复，build fail closed；WP2-Lite 不自行扩展 duplicate 语义。

为兼容现有 `translation_surface_screen_v1`，每条 entry 继续按该契约的双层 identity 配方计算 `logical_entry_identity` 与 `entry_revision_identity`。identity recipe 由 exact `rules_version` 确定且不增加 schema/store/contract family：历史 `production-review-v2-lite-rules-v1` 配方继续绑定全局 terminology snapshot；新 build 固定使用 `production-review-v2-lite-rules-v2`，revision 配方绑定 logical identity、source、target、当前 `fixed_source_identity`、rules version 与 exact `args_order`，但不绑定全局 terminology snapshot。v1→v2 允许一次 identity 变化。两版的 manifest、每条 catalog entry、surface/contextual envelope 与 batch evidence 仍记录并验证 exact 当前 terminology snapshot provenance；普通 catalog validator 同时接受 exact v1 history 与 exact v2 current policy/catalog bytes，未知或混配规则 fail closed。WP1 的同名 identity 即使碰巧相等也不构成继承关系，formal validator 仍机械拒绝 tracked shadow provenance。

### 3.2 catalog 文件 schema

`manifest.json` 恰含：

```text
schema_version, kind, catalog_id, rules_version, recorded_at, recorded_by,
manifest_sha256, loader_contract_path, loader_contract_sha256, lua_runtime,
manifest_component_ordinals, component_counts, occurrence_count, entry_count,
exclusion_count, entries_sha256, exclusions_sha256, terminology_snapshot_sha256,
source_identities, policy_sha256
```

`catalog_id` 是上述除 `catalog_id/recorded_at/recorded_by` 外字段的 canonical SHA-256；它只标识当前 catalog，不建立 ancestry。rules-v2 的 terminology-only catalog boundary 会改变 catalog/provenance bytes，但 entry revision identity 不变；migration 将这些 rows 分类为 `unchanged`，从而在 apply、Git-tree rebuild、SQLite 删除后重建与 revert 中保留 durable `done|repair_required|blocked` overrides。target/source/fixed-source/logical/rules/args_order 变化仍产生新 revision 或 logical identity 并要求重新验证。

`entries.jsonl` 每行恰含：

```text
schema_version, component, normalized_path, section, call_locator,
logical_entry_identity, entry_revision_identity, source, target, source_tag,
source_sha256, target_sha256, fixed_source_identity,
terminology_snapshot_sha256, rules_version, risk
```

`risk` 在 rules-v1 复用 WP1 的 `has_args_order/has_special/source_utf8_bytes/target_utf8_bytes/component_group_size/component_group_last`；rules-v2 在同一 risk 对象中另保存 exact `args_order`（`null` 或非空的 `1..n` integer permutation），并要求 `has_args_order` 与其是否为 null 一致。entries 按 `entry_revision_identity` lowercase ASCII bytes 严格递增且唯一。

`exclusions.jsonl` 每行恰含 `schema_version,occurrence_identity,component,reason_code`；reason 优先级与 WP1 相同。exclusions 按 occurrence identity 严格递增。validator 必须证明：

```text
occurrence_count = entry_count + exclusion_count
sum(component_counts.values()) = occurrence_count
```

pilot 首次 build 预期重验 `30,308 = 29,828 + 480`；不相等先作为 drift 停止，只有明确审核输入变化后才能接受新版本向量。

### 3.3 catalog 发布

build 先写 ignored 临时目录并完成 schema、hash、source identity、守恒和 128 MiB prospective tracked occupancy 检查。只有无活动 checkpoint、持有仓库锁且工作树目标路径与预期 preimage 相等时，才允许把 `catalog/` 作为一个普通 Git 变更提交候选。Git index/commit 是正式发布边界；工具不在背后自行 commit。

## 4. 单一 SQLite 队列模型

### 4.1 数据库 schema

`queue.sqlite3` 固定 `PRAGMA foreign_keys=ON`、`journal_mode=WAL`，schema 只有三张业务表：

```sql
meta(
  singleton INTEGER PRIMARY KEY CHECK(singleton=1),
  schema_version INTEGER NOT NULL CHECK(schema_version=1),
  catalog_id TEXT NOT NULL,
  evidence_head TEXT NOT NULL,
  rebuilt_at TEXT NOT NULL
);

state_override(
  entry_revision_identity TEXT PRIMARY KEY,
  logical_entry_identity TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN
    ('reserved','screened','deep_required','repair_required','done','blocked')),
  batch_id TEXT,
  attempt INTEGER NOT NULL CHECK(attempt>=0),
  result_sha256 TEXT,
  updated_at TEXT NOT NULL
);

reconciliation(
  old_logical_entry_identity TEXT NOT NULL,
  old_entry_revision_identity TEXT NOT NULL,
  new_logical_entry_identity TEXT,
  new_entry_revision_identity TEXT,
  disposition TEXT NOT NULL CHECK(disposition IN
    ('unchanged','revision_changed','logical_moved','removed','ambiguous','unmapped')),
  reason TEXT NOT NULL CHECK(reason IN
    ('unchanged','target_changed','source_changed','source_tag_changed',
     'call_locator_changed','fixed_source_changed','terminology_changed',
     'rules_changed','args_order_changed','removed','ambiguous','unmapped')),
  migration_id TEXT NOT NULL,
  PRIMARY KEY(migration_id,old_entry_revision_identity)
);
```

不设 queued row：当前 catalog entry 在 `state_override` 缺行即为 `queued`。不在当前 catalog 的 row 是损坏，除非处于一个尚未 apply 的 quiescent reconciliation transaction；正常 `queue check` 必须拒绝。`evidence_head` 是构建该投影时的 Git commit；dirty evidence 下只允许 active batch 操作，禁止声称 rebuild 完成。

`reconciliation` 是唯一迁移表。每次 catalog 边界 apply 前清空并装入一个 migration；apply 后只保留最近一次表内容用于诊断，长期映射由受跟踪 migration evidence 与 Git 保存。

### 4.2 重建规则

`queue rebuild` 必须在无 active batch、clean tracked evidence、持锁时：

1. strict-check 当前 catalog；
2. 只读取所选 treeish 的 tree 中以 ordinary file 当前存在的 `migrations/*.json` 与 `batches/*/{manifest,results,adjudications,gates}.json*` 候选，并按第 7.3 节验证其引用的 `raw/`；Git 历史只用于给这些当前存在的候选排序，所选 treeish 中 absent/deleted 的 path 不产生候选，因此 revert 后必须重建为该被撤销变更之前的状态；当前候选只在该 path 的 blob 相对其 parent 被引入或改变的 commit 定位其排序 commit，未改变的 descendant 不重复定位；
3. 校验每个 artifact 的 catalog/revision/path/hash 与其记录的 `base_commit`；包含该 artifact candidate 的 durable commit 由实际 Git treeish 提供，不写入 artifact 自身以避免自引用；
4. 对当前 revision 取已提交证据中的最终有效结果：若一个候选的 commit 是另一个的后代则后代胜出；其余按 `git rev-list --topo-order --reverse <treeish>` 给出的可达 commit 顺序取后者，同一 commit 内按 batch evidence 仓库相对 POSIX path 的 lowercase ASCII bytes 顺序取后者。该 winner 规则固定且由 commit ancestry/order 与稳定 path tie-break 决定；迁移映射只把明确的一对一结论带到 successor；
5. 无例外结果的 current revision 不插行，因而为 queued；
6. 在同目录创建新 SQLite 文件，事务提交、fsync 后替换旧文件，再运行 `queue check`。

人工结论必须存在于 committed evidence；只存在于 SQLite 或 active checkpoint 的结论在运行时丢失时最多导致本批重做，不得被报告为已完成。`reserved` 和 `screened` 只来自 active checkpoint，完整 rebuild 在无 active batch 时不会生成这两种状态。

## 5. 状态机与选择

### 5.1 七状态闭集

| 当前 | 允许下一状态 | 含义 |
|---|---|---|
| `queued`（隐式） | `reserved|blocked` | 当前 catalog eligible，尚无完成例外 |
| `reserved` | `screened|deep_required|blocked|queued` | 已进入唯一活动批次 |
| `screened` | `deep_required|done|blocked|queued` | surface exact result 已汇总但批次未提交 |
| `deep_required` | `repair_required|done|blocked|queued` | 必须按 contextual 契约深审/裁决 |
| `repair_required` | `done|blocked`，或修复后旧 revision 退场且 successor 隐式 `queued` | confirmed 修复需求已提交 |
| `done` | identity 变化后旧 revision 退场且 successor 隐式 `queued` | 当前 policy 要求的审核已完成 |
| `blocked` | `reserved|queued|deep_required|repair_required|done` | 需要用户/证据/输入修复；可由后续显式重试批次重新预留 |

`done` 必须在 evidence 中另存 `completion_level=surface_only|deep_reviewed|revalidated`，因此不夸大 surface 保证。durable batch 的每条结果只能终止于 `done|repair_required|blocked`；`deep_required` 只允许是 active checkpoint 中的中间态，未完成 contextual/裁决时必须在 prepare-evidence 前明确落为 `blocked`。状态本身不编码 provider、模型、owner 或长期阶段历史。

### 5.2 稳定选择与暂停

普通 `batch start` 只从隐式 queued 集合选择；`batch start --retry-blocked` 则只从当前 revision 且按第 4.2 节 winner 仍为 committed `blocked` 的集合选择，禁止暗中混入 queued。两种模式共用默认/硬上限 80、同一把锁、同一 active checkpoint 和同一优先键；blocked 重试是新 batch/attempt evidence，不建事件日志。优先键固定为：

```text
(policy risk rank descending,
 component_group_size descending,
 component_group_last descending,
 manifest component ordinal ascending,
 entry_revision_identity ascending)
```

以后修改优先规则必须改 `policy-v1.json` 并只在批次边界生效。没有活动 batch 才能 start；validator 以本次模式的候选域（queued 或 committed blocked）证明选集和剩余集合互斥且并集等于该域。暂停只是不再 dispatch，checkpoint 不变。个人项目不提供跨批预留、抢占、并行 active batch 或基于墙钟的优先级。

## 6. 唯一活动批次 checkpoint

### 6.1 `active-batch.json` schema

checkpoint 使用 canonical JSON + LF，原子 temp-write/replace/fsync。root 恰含：

```text
schema_version, kind, batch_id, catalog_id, base_commit, policy_sha256,
created_at, created_by, attempt, selection_mode, phase, selected, selected_sha256,
entry_snapshots, surface, contextual, adjudications, repair_candidates,
gates, last_safe_boundary
```

- `kind=production_review_v2_lite_active_batch_v1`。
- `phase` 闭集：`reserved|surface_ready|surface_collected|deep_ready|deep_collected|adjudicated|commit_ready`。
- `selection_mode=queued|retry_blocked`，冻结本批候选域；`selected` 是 1..80 个 revision identity 的优先顺序；`selected_sha256` 是其 canonical array raw SHA-256。
- `entry_snapshots` 与 selected 同集合，每项保存 catalog row 的 source/target/tag/path/locator/identities、row SHA-256 和选择前的有效状态。有效状态必须逐项冻结：隐式 queued 记为 `queued`，committed blocked 重试记为 `blocked`。
- `surface`/`contextual` 未进入阶段时为 null，否则为按第 6.2 节确定性 run 顺序的数组；每个 run 恰含 `contract,input_paths,input_sha256s,output_paths,output_sha256s,validator_status,intended_state_updates`，最后一项是由已验证 raw refs 确定性导出的逐 revision 更新。这只扩展同一个 checkpoint 内的 projection，不新增 store、checkpoint、STATE 或 consumer schema。
- `adjudications` 每项含 revision、observation hash、`confirmed|pending|advisory|refuted`、公开源码 path/commit（无固定 commit 时显式 null）、理由。
- `repair_candidates` 只含 confirmed 且需要改译文的 revision；本活动批次内禁止应用。
- `gates` 保存命令、exit code 和输出 SHA-256，不保存大段输出。
- `last_safe_boundary` 仅 `reserved|before_result_import|before_commit`。

每次打开 checkpoint 都重算 catalog rows、base commit、文件 hash 和现有 adapter validator。任一漂移停止，不自动改写 identity。

### 6.2 生命周期

1. **writer preflight／开始前**：每次持锁打开任一 writer 都先运行 reservation/checkpoint reconciliation，而不只在 `batch start` 运行。要求 catalog/queue strict-check、tracked worktree 无未说明改动。若 SQLite 有某 `batch_id` 的 orphan `reserved` 而 checkpoint 不存在，则从当前 treeish 的 committed evidence winner 逐项重建其预留前当前有效状态：先前隐式 queued 删除 override，先前 committed blocked 恢复 blocked，禁止无条件清为 queued；若存在 schema/hash 均有效的 checkpoint 而 reservation 缺失或与 `selected` 不同，则在尚无任何已接受 result 时按 checkpoint 的 selected 与冻结 prior state 精确恢复 reservation，已有已接受 result 时按下述 import recovery 处理或 fail closed。preflight 后若有效 checkpoint 仍存在或已恢复，writer 必须恢复并在其上操作；`batch start` 必须停止，不得选择新批。只有 preflight 后没有 checkpoint 才可按 `selection_mode` 选择最多 80 条。SQLite transaction 与 checkpoint 原子写仍各自独立，崩溃留下的单边状态由下一次持锁打开收敛，不声称二者共同 rollback。
2. **surface freeze/dispatch**：一个 active batch 可以混有不同 `fixed_source_identity`；adapter 按 `(fixed_source_identity,terminology_snapshot_sha256,rules_version)` 精确值分组。每个同质 run 的 membership 是 parent selected 中对应 entries 的有序子序列；run 按其最小 parent index 排序，`run_id` 是该顺序的 ordinal 加完整 tuple canonical SHA-256，因而 membership/run_id 均从 parent selected 顺序导出。每个 surface run 保留 identity→parent index 的显式映射，但发给现有 `translation_surface_screen_v1` consumer 的 entries 必须按 lowercase `entry_revision_identity` bytes 严格递增；分别构建 exact 六键 payload、envelope/lane group，并逐 run 使用该契约的 n=1..3 full、n=4..80 四 lane 和 strict result schema。validator 必须证明各 run 不相交，每条 parent identity 恰出现一次，并用 parent-index mapping 将 validated union 重排后逐项精确等于 selected；每个 payload 的全部 payload-level identity scalar 都同质，entry shape 按 `rules_version` 选择，rules-v2 必须从 catalog risk 投影 exact `args_order`。不改变 STATE/Paseo schema。
   新导出的多 run surface 批次，每个 run 使用确定性独立 Paseo task ID：
   `<batch-id>-surface-<三位run ordinal>`（如 `-surface-000`）；单 run 保留历史 batch task ID。
   每个 task 只有一个 whole-screen stage，不得用不同 cycle／attempt 伪装多个 screen。
   各 run 分别冻结、派发、归档并取得 `DONE_VERIFIED` 后，宿主才聚合全部 raw 进行 exact-union
   导入。group／envelope 使用该 run 的 task 路径；full 的 task 路径按同一命名规则构造。
   既有 stored checkpoint／group 不迁移，重复 export 保留已经验证的冻结字节与路径；历史
   stored group 仍按其原始 task ID 验证。此适配不更改 payload／candidate identity、parent
   映射、selected 数量／排序、consumer schema 或历史证据。
3. **结果汇总／导入**：回到 `before_result_import`，重验所有 raw bytes、candidate identity、路径、workspace/lineage、每个完整 run 及 validated run union。所有 surface/contextual result import 冻结为单向写序，并以现有 checkpoint 为恢复权威：只有全部适用 run 有效后，先把 validator 接受的 raw refs 和确定性 intended state updates 写入同一个 checkpoint，执行 atomic replace、文件 fsync 与目录 fsync；随后在一个 SQLite transaction 中应用这些更新。下一次 writer preflight 必须重验 checkpoint/raw，并幂等补齐 SQLite 中缺失或不一致但兼容的更新；若 SQLite 已含不兼容状态则 fail closed。不得为此增加日志、第二 checkpoint 或 kill matrix。`ISSUE` 至少进入 `deep_required`；`OK` 是否 surface-only done 或 deep 抽检由冻结 policy 决定。
4. **contextual**：只对 `deep_required` 构造现有 `translation_contextual_v2` exact 七键 payload；按该契约 payload-level identity scalars 的精确值确定性分区，entries 严格使用该契约冻结的 key order，不套用 surface 的 revision-identity 排序；rules-v2 的非空 `args_order` 必须在既有 `bounded_context.context` 中追加规范 `args_order={i,j,...}` token，未携带第四参数的 null 形式保持无该 token，rules-v1 bytes 保持不变。仍保存 parent-index mapping，并将 validated run union 重排证明等于 parent deep set。保守冻结为该契约的 review-only 单一 `REVIEW/full` 路径（`n<4` 必须 full，`n>=4` 也不选择可选四 lane），因此不会把四 lane group 当 terminal，也不需要 lane-plus-closing-full 序列。每个 run 只有对应 Paseo task 的 current DONE checker 已得到 `DONE_VERIFIED` 后才可 import；仍使用既有 raw evidence、源码身份和 compact result validator，不创建新的生产 contract。
5. **裁决**：ORCHESTRATOR 逐 observation 以固定源码/语境证据标记；只有 confirmed 可进入 `repair_required`。pending 进入 `blocked`，advisory/refuted 按 policy 可 `done`。
6. **commit 前**：生成受跟踪 batch evidence 候选，运行全部门禁，设置 `before_commit/commit_ready`。工具不得 commit。
7. **提交后 finalize**：维护者提供包含完整 batch evidence 的 commit。工具重验 commit/tree/hash 后更新 SQLite，移除 checkpoint 并 fsync 目录。只有这一步后结果是长期 durable。

### 6.3 安全放弃与重试

- `reserved` 或尚未接受任何 raw result：`batch abandon` 按 checkpoint 逐项恢复选择前有效状态再删除 checkpoint；先前隐式 queued 通过删除 override 恢复，先前 committed blocked 恢复 blocked，禁止把 blocked 重试无条件改成 queued。
- 已接受 raw result 但未 commit：默认保留 checkpoint 恢复；显式 `--discard-uncommitted-results` 才可放弃，并警告这些结果不是长期结论。重试增加 `attempt`，旧 child 必须按 AGENTS 生命周期归档，冻结 entry bytes 不变。
- 已生成 dirty evidence 但未 commit：只允许校验、commit 或 `batch abandon --restore-evidence` 精确删除本 checkpoint 声明且 preimage 为 absent 的路径；发现未知改动立即停止。
- commit 已包含 evidence 而 finalize 未执行：`batch recover --from-head` 重放 HEAD evidence，幂等 finalize；不得重复提交。
- catalog/input/terminology/manifest 漂移：活动批次 fail closed，只能先保存或放弃未提交结果；禁止迁移活动批次。

恢复只覆盖上述三个安全边界；批次开始时的 reservation/checkpoint 交叉对象修复属于 `reserved` 边界的一次确定性收敛，不新增安全边界，也不枚举 kill-point 矩阵。

## 7. Adapter、evidence 与 Git 边界

### 7.1 不改现有 consumer

surface 输入必须逐字满足 `translation_surface_screen_v1` 的六键 payload 及按 `rules_version` 选择的 entry identity/shape（rules-v2 含 exact `args_order`）；contextual 输入必须逐字满足 `translation_contextual_v2` 的七键 payload（rules-v2 的非空 mapping 通过既有 `bounded_context.context` token 披露）。WP2-Lite adapter 只做：

```text
catalog/checkpoint projection -> existing envelope bytes -> existing validator
existing exact raw result bytes -> existing validator -> normalized batch evidence
```

checkpoint/evidence 对每个 run 保存 `contract,input_path,input_sha256,output_path,output_sha256,candidate_identity`；lane 另存现有 group manifest path/hash。run 必须按第 6.2 节分区并证明 validated run union 等于 parent selected/deep set，任一现有 surface/contextual payload 的所有 payload-level identity scalars 必须同质。禁止把 queue state、裁决、旧 finding 或运行时 provider/model 注入 candidate identity。

### 7.2 每批受跟踪 evidence

`manifest.json` 恰含 catalog/policy/base commit、batch/attempt、ordered revisions/hash、entry snapshot hash、adapter refs、结果/裁决/gates 文件 hash、producer task IDs 和 recorded metadata；每个 adapter ref 还记录下述 tracked raw copy 的仓库相对 path 与 SHA-256。

`results.jsonl` 每个 selected revision 恰一行，含 source/target/tag/path/locator、logical/revision identity、surface verdict/observation（可 null）、deep verdict/observation（可 null）、exact input/output hash、最终 queue state 和 completion level；最终状态只允许 `done|repair_required|blocked`。`adjudications.jsonl` 对每个 observation 恰一行，保存 disposition、证据来源、固定 commit/snapshot、结论与 repair_required boolean。`gates.json` 保存实际命令、exit code、版本和输出 SHA-256。

`.ai/task/` 与 `.ai/reviews/` 是 gitignored，不可作为 durable 引用。prepare-evidence 只把本批每个 run 经现有 validator 实际接受的 exact adapter input/output bytes 逐字复制到 `batches/<batch_id>/raw/<contract>/<run_id>/`；lane group manifest 是 validator 接受的 adapter input，除此之外不得复制旁路文件。文件名、path、length、SHA-256 都冻结，禁止复制其他 STATE、child metadata、历史 task 或未接受 attempt。strict validator 必须从 commit tree 重读这些 raw copies 并与 manifest/ref/result hash 逐字核对。人工复核者仅凭当前 commit 中 catalog row、四个核心 evidence 文件、该 bounded raw 子树和公开源码定位，即可确认“审核了哪条、看到了什么、如何裁决、为何进入最终状态”。大体积可重生成诊断留在 `.artifacts/`。

### 7.3 Durable 定义

只有同时满足下列条件才是 durable batch：

- 四个核心 batch evidence 文件及 manifest 精确引用的 bounded `raw/` files 均在同一受审 Git commit；
- commit 的 parent 等于 checkpoint `base_commit` 或有显式、已复核的 rebase preflight；
- strict validator 从 commit tree（不是 dirty worktree）重算全部 hash/集合与 accepted raw bytes；
- catalog 和 adapter 输入仍匹配；
- durable results 的最终状态只含 `done|repair_required|blocked`；
- applicable CI gate 通过；
- catalog、四个核心文件、bounded raw copies 及其他现存 production-review tracked bytes 全部计入同一个 128 MiB prospective/actual gate。

SQLite commit、checkpoint phase、child terminal 或未提交 evidence 都不是 durable history。

## 8. Catalog 迁移与修复边界

### 8.1 Quiescent reconciliation

catalog rebuild 只允许：无 active checkpoint、无 reserved/screened row、tracked worktree clean、持仓库锁。工具比较旧/新 occurrence 并生成一个 `migrations/<migration_id>.json`，其 rows 与 SQLite `reconciliation` schema 同义，另含 old/new catalog hashes、counts 和 row hash。migration kind 保持 `production_review_v2_lite_migration_v1`；representation 由 exact `schema_version` 分派：历史 `schema_version=1` 是 self-contained full record，必须保留完整 `old_rows`、`new_rows` 和覆盖每条旧 entry 的 mapping rows，继续按原 exact schema 读取且不重写；新 plan 固定生成 `schema_version=2` sparse record，保留相同的 catalog／commit／tree／hash／count／metadata bindings，但省略 `old_rows`、`new_rows`，`rows` 恰好只保存完整 reconciliation 中 disposition 非 `unchanged` 的有序 exception。v1 缺少 snapshot 等 full key 时不得按 v2 解释，v2 出现 snapshot、`unchanged` row 或额外 key 同样拒绝。

所有 v2 consumer 共用一个 catalog-bound normalization／expansion 路径：从 migration 绑定的 old Git catalog 与 publication／candidate new catalog 重新执行完整 `reconcile(old,new)`，要求 artifact sparse rows 与重算结果的非 `unchanged` 子序列逐字精确相等，再把重算的 full mapping 交给 check/report、apply、migration-chain traversal 和 SQLite reconciliation projection。没有同时取得并核验 exact old/new catalog bindings 时，缺失 row 绝不默认视为 `unchanged`。omitted、extra、reordered、duplicated、显式 unchanged 或 misclassified exception 一律 fail closed；added revision 仍因没有旧 row 而隐式 queued，removed、ambiguous、unmapped 以及 target/source/fixed-source/rules/args-order 等变化继续作为显式 exception。

确定映射规则按顺序：

1. exact logical + exact revision：`unchanged`；
2. exact logical、revision 改变：按 target/fixed source/terminology/rules 的实际差异标 `revision_changed`；
3. source、source_tag 或 call locator 改变：只有 component/path/section/function 与局部唯一邻接证据共同给出一对一映射时才 `logical_moved`；
4. 旧条目确实消失且无候选：`removed`；
5. 多候选为 `ambiguous`，无足够证据为 `unmapped`。

`ambiguous|unmapped` 一律不 apply、不替换 catalog，交用户裁决；禁止按行号或相似文本猜测。source/tag/target 的变化及结果携带规则由同一张表处理，不另建迁移层。

apply 在一个 SQLite transaction 内建立新投影：unchanged 保留状态；revision_changed/logical_moved 的旧 `done` 不自动授予新 revision，新 revision默认 queued；`repair_required` 只有在下述受审修复证据明确绑定 successor 时才可将旧项记入历史并让 successor queued；removed 不进入新投影。随后生成 catalog + migration 的同一 Git 变更候选。Git commit 后才能以新 catalog rebuild queue。

### 8.2 修复

修复必须发生在批次已经以 Git commit 保存审核/裁决证据、checkpoint 已移除之后。流程是：

1. `repair preflight` 从 committed `repair_required` evidence 生成有界 workset并核对当前 target preimage；
2. 独立 implementation task 由唯一 EXECUTOR 修改译文，按仓库流程复审；
3. 运行 lint/源码核验和适用门禁；
4. 从修改后 live input rebuild catalog，生成旧→新 reconciliation；
5. 同一受审 Git 变更提交译文、repair evidence、新 catalog 和 migration；
6. commit 后 `queue rebuild`，successor revision 隐式 queued，等待后续 revalidation batch。

不允许在 active batch 中修译文，不允许把 parent 的 `done` 复制给 successor，不允许 repair 后跳过重新审核。

## 9. WP1 retirement 与首次发布

WP1 retirement 与首个 WP2-Lite catalog 必须是一个明确、人工可恢复的受审 Git 变更，不需要额外运行时历史协议。

### 9.1 精确 retire 集合

preflight 从 baseline `a287652` 验证并删除且仅删除以下 tracked WP1 family：

```text
evidence/production-review/locator-snapshots/ea8e0f5bf078e63d4411ed5518f79950960bf9aa7b36ea621ae14ead6dadcec5/
evidence/production-review/catalogs/1001066b5d575524a5c2966d462e03b3a06b38c3232c098eaa459de1e0a29567/
evidence/production-review/shadow-journals/705606c15ec0fc1526cf40345c23f7b79205b992007e2cc873fa3c0cb272184c/
evidence/production-review/batches/35eee018cacf0048ebcad2c5de01423dce900777a92d52a7b4c89e0085862306/
i18n/quality/production-review/schemas-v1.json
i18n/quality/production-review/shadow-policies/a177ad59ed744a00b98af91b3fbcd989db4097b631bd46c1fc23ddb3f5d8af58/
```

实现 fixture 必须固定这 12 个文件的 baseline SHA-256：

```text
018970f667b3ee1093e5175ed59936b85dd8a29ee4641c76247761a2dd7c77d5  batches/.../manifest.json
1c69eb09dba94e8f7879af60e2ec05e430429e7028340d4d608e38acfccd2621  catalogs/.../entries.jsonl
35b161d41302e493cb6d45d2be946ca0122c92012ca1edd50d94b99d88231e43  catalogs/.../exclusions.jsonl
e579e48c4095bb1565f28d01fff6ed2cf4c5713f675d813c14307336f73d02e3  catalogs/.../manifest.json
f6a2d8ac1a5500d466a9c32ddaa6d76311d6817516754be4e499e69163e968ef  locator-snapshots/.../locators.jsonl
dae1b2bed19b168f9a4dc98eb7ed30edeea4a3b21f3b0832e887c70b02f277f2  locator-snapshots/.../manifest.json
cfb3e83c043cfe419ab6f0d7ffdf000e2ea01406db3adf61ae713dc7fa216ab4  locator-snapshots/.../occurrences.jsonl
9916bfc9fb66f9ff006b7ec4a59693045db7a8d9939d0b4b1ab9fb302911d9c8  shadow-journals/.../checkpoint.json
7001ac7d4458c37f6e3d91c44b75169ad05db4118cee555ad2a9159828ba5e39  shadow-journals/.../events.jsonl
8ff3e7123801fe5e08e329a372aedc86b34b66ce4253939d8fcb8698f528f4fd  shadow-journals/.../group.json
7881ce527032927b34dcc6b7ec050be6669e2f76f70b0a3ccd1f72666e7390fd  schemas-v1.json
b2e2bc0f67e6376baea3243aa7e9a15c16543512c9d5af48baae1819f24413fd  shadow-policies/.../policy.json
```

省略号只缩短本表显示，精确路径以上方六个前缀与 basename 拼接。多件、缺件、bytes 不同、额外 tracked WP1 child 或 symlink 均停止。不能用布尔 flag 声称已 retire。

### 9.2 首次发布顺序

1. clean worktree、无 active checkpoint、持仓库锁；
2. 重新 harvest live input，构造全新 formal catalog，重验当前版本向量；
3. 校验 exact WP1 preimages 与新文件 schema/hash；
4. 按 Git prospective tree 计算 `evidence/production-review*` 与 `i18n/quality/production-review*` 全部 tracked bytes，要求 `<=128 MiB`，不要求旧新数据在 tracked worktree 外长期双份保存；
5. 工作树中形成“精确删除 WP1 + 新增 WP2-Lite schema/policy/catalog”的单一候选 diff；
6. 运行门禁并人工复审；
7. 维护者一次 commit。若 commit 前失败，`git restore` 可恢复 WP1；若 commit 后需要回滚，以普通 Git revert 恢复完整受审树。

该首次 commit 不包含 queued 初始化行、不自动创建首批、不把 WP1 shadow 作为 parent。formal consumer 只接受新 schema 且继续拒绝 forbidden shadow bytes。

## 10. CLI 表面

统一入口仍为 `python3 -B tools/i18n production`，新增子命令：

```text
authoritative-catalog build --output <ignored-dir>
authoritative-catalog check [--treeish <commit>]
wp1-retirement preflight --candidate-catalog <dir>
queue init
queue rebuild [--treeish HEAD]
queue check
queue status [--json]
batch start [--limit 80] [--retry-blocked]
batch show
batch surface-export
batch surface-import
batch contextual-export
batch contextual-import
batch adjudicate --input <canonical-json>
batch prepare-evidence
batch abandon [--discard-uncommitted-results] [--restore-evidence]
batch recover --from-head
batch finalize --commit <sha>
migration plan --candidate-catalog <dir>
migration check --input <path>
migration apply --input <path>
repair preflight --batch-id <id>
```

所有 writer 子命令先持同一 repository lock；read-only `check/status/show` 不持写锁但必须报告检测到的 active writer。未知 schema、extra key、duplicate JSON key、非法 UTF-8、symlink/special file、hash 漂移或超预算一律非零退出。CLI 不提供 `--force` 绕过 identity、evidence、active-batch 或 migration gate。

## 11. 实施 work packages

### WP2L-1：正式 catalog 与 WP1 retirement preflight

实现新 schema、formal build/check、当前向量守恒、formal consumer gate、exact WP1 preimage 清单和 prospective 128 MiB 检查；不执行审核。

**个人项目尺度说明**

- **复用的 WP1 能力：** harvest、locator allocation、canonical JSON、risk、source/terminology binding、守恒与预算检查。
- **本包新增的最小机制：** 一个当前 formal catalog schema和一次 exact retirement preflight。
- **对应的现实故障或用户目标：** shadow 不可派发，且现有 formal consumer 正确拒绝所有 catalog；必须建立新 authority 并安全移除 95,097,107-byte WP1 tracked baseline。
- **被拒绝的更复杂方案：** 多代并存的内容图、跨多个 family 的运行时交换协议和影子链提升。
- **预算状态：** 一个 catalog；无队列、无 checkpoint；prospective tracked 总量必须不超过 128 MiB，符合预算。

### WP2L-2：SQLite 投影与重建

实现三表 schema、隐式 queued、queue init/rebuild/check/status、一个 repository lock，并以小型 fixture 证明删除数据库可从 catalog+committed evidence恢复。

**个人项目尺度说明**

- **复用的 WP1 能力：** catalog validator、稳定顺序、replay/check 的 fail-closed 测试方式。
- **本包新增的最小机制：** 一个 stdlib SQLite 投影、六种非默认 override和一把锁。
- **对应的现实故障或用户目标：** 29,828 条不能靠手工列表推进；运行时文件丢失又不能丢人工结论。
- **被拒绝的更复杂方案：** 常驻服务、多 writer ownership、每行初始事件和替代 Git 的长期日志系统。
- **预算状态：** 一个 store、一个 lock、七状态闭集，符合预算。

### WP2L-3：单 active batch 与 surface adapter

实现 checkpoint schema、稳定 start/abandon/recover、现有 surface exact payload/result adapter和最多 80 条整组汇总。

**个人项目尺度说明**

- **复用的 WP1 能力：** 80 条优先排序、batch 守恒、原子写入；复用现有 surface contract/validator。
- **本包新增的最小机制：** 一个 active-batch 文件及 queue↔surface 的薄适配。
- **对应的现实故障或用户目标：** 中断不能造成重复/漏审，且 shadow batch 当前不可派发。
- **被拒绝的更复杂方案：** 多活动批次、跨批预取、远程租约和逐内部写点恢复矩阵。
- **预算状态：** 一个 checkpoint、默认 80、无新 consumer schema，符合预算。

### WP2L-4：contextual、裁决与 batch evidence

实现 deep_required 投影、现有 contextual v2 exact adapter、ORCHESTRATOR 裁决导入、四文件 evidence 和 commit/finalize/rebuild 边界。

**个人项目尺度说明**

- **复用的 WP1 能力：** source/terminology identities、canonical/hash validator；复用现有 contextual v2 和 Paseo STATE schema。
- **本包新增的最小机制：** 第二个薄 adapter与一套小型每批 evidence（仍共用同一 checkpoint/store）。
- **对应的现实故障或用户目标：** surface ISSUE 不能直接成为修复指令，人工结论必须在 SQLite 丢失后仍可复核。
- **被拒绝的更复杂方案：** 新审核 contract、跨任务承诺网络、每阶段独立长期 ledger和自动裁决。
- **预算状态：** 未增加 store/lock/checkpoint/business state，符合预算。

### WP2L-5：batch-boundary migration 与 repair

实现唯一 reconciliation 表、migration plan/check/apply、ambiguous/unmapped 停止，以及 committed review→repair→catalog rebuild→successor revalidation。

**个人项目尺度说明**

- **复用的 WP1 能力：** drift reconstruction、identity/rules/source/terminology 差异检测和 translation ledger 的身份迁移测试经验。
- **本包新增的最小机制：** 一张 quiescent reconciliation 表和一个受跟踪 migration 文件/边界。
- **对应的现实故障或用户目标：** source/tag/target 与修复会改变 identity；错误继承 done 会永久漏审。
- **被拒绝的更复杂方案：** 活动批次内迁移、多代并行、自动模糊匹配和跨代可变关系图。
- **预算状态：** 一套迁移表；状态仍七个；只在 batch boundary 运行，符合预算。

### WP2L-6：80 条 pilot 与首次正式提交

用 live input 运行 retirement+catalog 候选、初始化可重建队列、选择一个 80 条批次，完成 surface、按 policy 的 deep/裁决、evidence commit、故障恢复演练和 rebuild；不自动启动下一批。

**个人项目尺度说明**

- **复用的 WP1 能力：** 真实 30,308 occurrence 校准、80 条 draft、drift/reconciliation 和 focused gates。
- **本包新增的最小机制：** 只运行一次完整 WP2-Lite 闭环并记录实测时间、bytes、恢复结果。
- **对应的现实故障或用户目标：** 只有真实 pilot 才能证明个人维护者可操作、证据可审、失败可恢复。
- **被拒绝的更复杂方案：** pilot 前全量启动、自动连续几万条、动态扩容和基于假设的优化。
- **预算状态：** 1 active batch、最多 80 条、128 MiB gate；任何超限先停，符合预算。

## 12. 未来角色报告的比例原则

每个实现任务必须把下列要求写入 SPEC/验收：

### EXECUTOR 必答

报告必须逐项给出：

1. 复用了哪一项 WP1/现行 consumer 能力（具体 path/test）；
2. 实际新增的最小机制和文件；
3. 它对应的已见故障、pilot 事实或明确目标；
4. 拒绝了什么更复杂替代方案；
5. store/lock/checkpoint/migration/state/100 KiB/128 MiB 预算是否仍满足。

未回答五项、用“未来可能需要”作为唯一理由、或悄悄新增第二 store/lock/checkpoint，均不得交付。

### REVIEWER verdict 必答

verdict 开头先列本任务适用的个人项目原则。blocking finding 只限：有证据的 correctness 错误、数据损坏/丢失、无法按本文边界恢复、现有 consumer 被破坏、明确验收缺失或预算越界。形式更完备、额外 schema、额外 retention、更多并发和未来扩展建议必须标 `optional/advisory`，不能阻塞。

### ORCHESTRATOR 裁决必答

只把有源码、现有测试、可复现故障、pilot 数据或明确验收条款支持的 finding 标 confirmed。对每个确认修复说明它属于 correctness、data loss、recovery、consumer compatibility、acceptance 或 budget 哪一类；其他意见标 pending/advisory。不得为追求理论完备扩大实施包。

## 13. 测试、门禁与 pilot 验收

### 13.1 每包测试

- catalog：canonical/duplicate-key/UTF-8/path/symlink、11-component 守恒、现行 vector、source/terminology/manifest/loader drift、shadow provenance 拒绝；
- retirement：12 个 baseline 文件 exact hash、缺/多/变更拒绝、prospective 128 MiB、Git restore/revert 演练；
- queue：隐式 queued、七状态闭集、事务回滚、单锁互斥、数据库删除后 deterministic rebuild、所选 treeish 只重放当前 ordinary files 且 revert 忽略 absent/deleted path；
- batch：0 不 start、1/3/4/79/80 边界、稳定排序、selection mode 与 prior effective state 冻结、blocked abandon 精确恢复、重复 start拒绝、每次 writer open 的 reservation/checkpoint reconciliation、有效 checkpoint 阻止新选择、orphan reserved 依 committed winner 恢复、三个安全边界的中断恢复、安全放弃；
- adapters：现有 surface/contextual fixture hashes、mixed identity 的确定性同质 run 与 union、surface emitted entries 按 lowercase revision identity bytes 严格排序并以 parent-index mapping 回排、rules-v2 pilot `args_order` 投影与 revision 变更、contextual 冻结 key order、surface full/lane、contextual review-only single-full/DONE_VERIFIED、result import 的 checkpoint-first fsync/SQLite 单事务/幂等补齐/不兼容 fail-closed、raw bytes、wrong identity/path/hash/partial group拒绝；
- evidence：当前 commit tree 重放、bounded raw exact-copy/hash、同 revision 的 ancestry/order/path winner、durable 状态闭集、缺文件/extra row/hash 漂移/夸大 completion level拒绝；
- migration：target/source/tag/locator/fixed source/terminology/rules/args_order/removed，及 ambiguous/unmapped fail closed；
- repair：active batch 中拒绝、preimage drift拒绝、successor queued、parent done不继承、revalidation必需。

### 13.2 每批五步门禁

译文批次仍按 `docs/agent-workflow.md` 执行五步门禁，并追加：

1. `authoritative-catalog check`；
2. `queue check`；
3. `batch` evidence strict check；
4. surface manifest/result 与 contextual 适用 validator；
5. 从 commit candidate 重建 queue 并比较状态摘要。

涉及译文/术语/工具行为时运行 `python3 -B tools/i18n doctor`、适用 `lint` 和 `tools/ci-gates.sh`；只有 SPEC 证明不影响 addon 输出/构建时才 `--skip-build`。所有实现任务收束还必须运行 production、surface manifest、surface result、translation ledger focused suites、`python3 -B tools/paseo_contract_check.py` 和 `git diff --check`。

### 13.3 80 条 pilot 通过条件

在任何连续生产批次启用前，首个 80 条 pilot 必须同时满足：

- live vector 守恒已解释且 formal IDs 全新；WP1 exact retirement 与首次 formal publication 在一个受审 commit；
- prospective/actual tracked production-review 总量（含 bounded raw copies）均 `<=128 MiB`；
- 80 条选择可重算，mixed identity 被确定性分为同质 runs，surface lane/run union精确，所有 exact raw input/output bytes/hash 可从 commit tree 重验；
- deep_required 全部经 contextual review-only single-full 的 current `DONE_VERIFIED` 后导入并完成裁决，或在 durable evidence 中明确 blocked；confirmed 才进入 repair_required；
- committed evidence 足以逐条人工复核且 completion level 不夸大；
- 在 `reserved`、`before_result_import`、`before_commit` 各演练一次中断；恢复或安全放弃结果确定；
- 删除 queue.sqlite3 后从 catalog+committed evidence 重建，状态摘要和逐 revision override 完全一致；
- migration fixture 中 ambiguous/unmapped 停止；active batch 迁移被拒绝；
- Git revert 首次发布或 pilot commit 后能回到前一个完整受审状态；
- 全部门禁通过，且个人维护者记录实际操作时间、峰值 bytes、人工步骤和任何 WAIT_USER。

pilot 未通过时不领取下一批。通过只授权按现有默认参数开始下一有界批次，不授权自动全量运行。

## 14. 停止条件与升级触发

### 14.1 立即停止

除 AGENTS.md 的既有停止条件外，WP2-Lite 遇到以下情况停止并交用户：

- source/tag/locator migration ambiguous 或 unmapped；
- queue 无法从 committed evidence 重建相同结果；
- active checkpoint、adapter raw bytes 或 Git evidence identity 不一致；
- 128 MiB prospective/actual gate 超限；
- 需要修改术语库、全局重命名或制定跨批策略；
- pilot 任一门禁失败且一次有界诊断不能归因；
- 需要第二 writer、第二 active batch或第二 queue store才能继续。

### 14.2 只有实测触发才提升级

升级必须另建提案，且至少满足一个可核验证据：

- 两次真实 lock contention 阻碍单维护者流程，且不是残留进程/误操作；
- SQLite rebuild 或 check 在连续三个批次超过预先记录的个人可接受时间预算；
- 两次真实故障发生在本文三个安全边界之外并造成必须重做已接受人工结果；
- 128 MiB 在按 Git 历史退役旧当前数据后仍被必要的一个 catalog+committed evidence 超过；
- 现有 surface/contextual consumer 的已批准 schema 发生实际不兼容；
- pilot/连续批次证明 80 条或单 active batch 是主要瓶颈，且人工裁决/修复没有积压。

即使触发，也只批准解决该证据的最小下一机制；不自动批准多 writer、额外历史层或新 consumer。

## 15. 尚待 pilot 决定但不阻塞核心实现的参数

核心 choice 已冻结；未来实现不得自行改变。以下仅是 policy/操作参数，可由 pilot 在既有 schema 内取值：

- `OK` 中 surface-only 完成与进入 deep 抽检的比例/规则；
- 个人维护者可接受的 rebuild/check 时间预算；
- 每批 briefing 的具体 lane-neutral 文案；
- evidence 中公开源码定位的展示格式（字段语义和 fixed commit/null 规则已冻结）；
- pilot 通过后是否继续连续批次；此决定不改变每批门禁和停止条件。

任何参数选择都不得改变一个 store、一个 lock、一个 checkpoint、隐式 queued、七状态、batch-boundary repair/migration 或 Git durable history 的边界。
