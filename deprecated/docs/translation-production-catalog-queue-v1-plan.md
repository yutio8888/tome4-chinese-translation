# 生产审核目录与队列 v1 实施计划

## 状态与边界

WP1（shadow calibration）已实现；WP2 及正式生产 writer 尚未实现。WP1 只能证明当前输入可被确定性枚举、冻结和重放，**不是权威目录，不可派发，不可提升**，不取得 ownership，不建立 formal epoch，不写译文，也不向正式 `translation_review_ledger` 追加记录。所有 shadow artifact 的 markers 固定为 `authoritative=false`、`dispatchable=false`、`promotable=false`。

WP2 必须从届时输入重新构造全新的 locator、catalog、policy、journal、checkpoint 和 batch ID 链；不得复用、改标或提升 WP1 shadow ID，shadow catalog 产生的合法 11-key ledger record 也不得进入正式 ledger。默认 CLI 始终合并工具仓库 ROOT 与所选 `--root` 下的 shadow manifest hash，`--root` 只重定向 ledger/path 解析，不能移除仓库 barrier；catalogs 不存在可返回空，但已有 child 的目录类型、manifest ordinary-file、canonical bytes 或最小结构异常均失败关闭。`--catalog-manifest` 选择的 formal consumer 在 WP2 authoritative schema/ID/domain/body/lineage validator 完成前拒绝所有 catalog，简单改 kind/marker 也不例外；未来 exact formal validator 仍必须同时应用该 forbidden set。generic ledger library replay 仍只是 legacy 状态机结构验证，不代表 formal catalog acceptance。当前 WP1 的 source locator 仅是校准 allocation；正式、可迁移的 source locator recipe 与旧 identity migration 是 WP2 必做，不得把 WP1 locator 当正式父节点。

## WP1 数据流

```text
11 manifest translations (LocaleDocument.translations emission order)
  -> locator bootstrap/check
  -> catalog build/check
  -> shadow-policy build/check
  -> one-shot shadow-journal bootstrap/check -> replay
  -> batch-draft --shadow
  -> reconciliation report (.artifacts only)
```

当前 baseline 枚举 30,308 个 occurrence：生产范围六组件 `engine/boot/tome/ashes-urhrok/cults/orcs` 为 29,828 个 catalog entry，其余五组件共 480 个逐项 exclusion。排除优先级固定为 `outside_initial_six_component_scope > empty_source > empty_target`，因此每个 occurrence 恰落入 entry 或 exclusion；exclusion 精确包含 schema version、occurrence identity、component 和 reason code。

### Identity 与 canonical bytes

全部对象采用 UTF-8、键排序、紧凑 JSON、禁止 NaN；JSONL 每行 canonical object 并以 LF 结束。ID 配方是：

```text
SHA256(domain-with-trailing-NUL || u64be(canonical-core-byte-length) || canonical-core)
```

对象 core 去掉自身 ID 字段，避免环。domain 闭集为 occurrence、call-locator、locator-snapshot、catalog、terminology-snapshot、shadow-queue-policy、journal-group、journal-event、journal-checkpoint、shadow-batch、ordered-set。术语 snapshot 依次纳入 `TERMINOLOGY.md` 和 `terminology/` 下按路径排序的普通文件，每个路径和内容分别用 u64be 长度 framing。

Occurrence 精确保留组件、译文路径、document ordinal、`t`、section、source、target、source_tag、args_order、special。allocation 只含 component/path/function/section/source/规范 tag/duplicate index；tag 的 null 规范为 `""`，duplicate index 在 WP1 必须唯一且为 0，target、args_order、special 和全局 ordinal 不参与 locator。logical/revision identity 精确复用现行 surface recipe。

Catalog 是只读 snapshot。风险向量只含 args/special、source/target UTF-8 byte 数，以及 `(component, source, normalized tag)` group 的 size/last。entry 按 logical identity 排序；exclusion 单独逐项保留。locator manifest 从 `Manifest.components` 独立冻结完整的 `(component, ordinal)` 有序绑定（不得从 occurrence 反推）；catalog 与 policy 再逐项绑定其中的 eligible component ordinals。policy 固定 batch size 80，format risk 优先，再按 group size 降序、group-last、冻结的 manifest component ordinal、revision bytes；不得从 source identity mapping 的迭代顺序推导 ordinal；carry/retry 都是 `not_applicable`。

### Shadow journal 与 batch

bootstrap 是唯一 journal 生成路径；模块故意不提供 `append_record`。每个 event 只嵌入现行 ledger 的精确 11-key `None -> queued` / `revision_frozen` / `revision_freeze_record`，attempt=0，batch/task/handoff=null，genesis previous hash=null。replay 验证 event ID、hash chain、checkpoint、logical/revision 唯一性和 catalog provenance，并投影一次 materialized view。

Batch eligible 集合 E 为全部 queued revision。先按 policy 取优先序前 80 为 B，其余为 C，再各自按 revision lowerhex byte 序冻结；S 永远为空。验证 `E=B⊎C`、全部 ordered hash、priority hash、marker 与 content ID。surface dispatch gate 明确拒绝 shadow batch。

## 路径、原子发布与预算

- schema/policy：`i18n/quality/production-review/`
- locator snapshot、catalog、shadow journal、batch：`evidence/production-review/`
- drift/reconciliation report：`.artifacts/i18n/production-review/`

受跟踪 artifact 按完整目录树发布：WP1 的 per-family publication 使用 production-review 全局文件锁覆盖“在目标 family parent 下清理跨 content ID 的、有界且严格 content-addressed 的非 symlink staging directory→读取现有总占用→校验类别与本 family／总预算→no-replace rename→parent fsync”的整个临界区，使先前崩溃的不同 ID publication residue 不会阻塞该 family 唯一 baseline；final directory、无关目录和 symlink directory 均保留。跨 family residue 不做全局清扫，而由重新运行对应 family 来恢复。existing-identical 与 rename race 的 `ALREADY_PRESENT` 也必须 parent fsync 后返回。这只能保护一次 WP1 family publication，不是未来整代事务。repository-root publication 强制提供类别，WP1 locator/catalog 各只允许一个 baseline。同目录 sibling temp 内写齐全部文件（locator 固定为 `manifest.json + occurrences.jsonl + locators.jsonl`），逐文件 fsync、逐层 temp directory fsync、atomic no-replace rename、parent directory fsync。相同目标目录 + 完整树逐文件同名同 bytes 才返回 `ALREADY_PRESENT`；缺件、多件或不同 bytes 均失败关闭。family 预算依次为 locator 32 MiB、catalog 32 MiB、policy 1 MiB、journal 48 MiB、batch 8 MiB，总预算 128 MiB；WP1 当前 family 的预检和 rename 共用同一把锁，不能并发越过总预算。时间必须是 UTC 整秒，`recorded_by` 非空；同一 baseline 的 locator、catalog、policy、journal/checkpoint 固定使用相同值。

## 操作与验收

所有入口统一为 `python3 -B tools/i18n production ...`：

- `locator bootstrap|check`
- `catalog build|check`
- `shadow-policy build|check`
- `shadow-journal bootstrap|check`
- `replay`
- `batch-draft --shadow`
- `reconciliation report`

验收要求 production suite、surface manifest/result、translation ledger 四套 focused tests通过，真实 baseline 的全部 check/replay/reconciliation 通过，Paseo contract check 与 `git diff --check` 通过。CI 显式执行上述四套测试；reconciliation 的 drift 报告不进入 CI 或受跟踪 evidence。

## WP2 入口条件

WP2 只能消费届时重新 harvest 的 11-component occurrence 向量，并发布全新正式 ID 链。开始前须另行批准：formal authoritative marker 的签发主体、正式 source locator/migration recipe、append writer、ownership event、epoch 生命周期、迁移/reconciliation、并发/backpressure 和正式 surface/deep handoff。WP1 的一次性 queued journal、shadow policy、batch 或统计不得作为这些能力存在的证据，也不得成为 WP2 artifact 的 parent。

WP2 publication 当前完全不可用。启用前必须实现并审核一个新的单锁 generation transaction：在同一个锁临界区内精确验证并完成受跟踪 WP1 shadow candidate directories 的 retirement，fsync 其父目录，预检 locator/catalog/policy/journal/batch 各 family MiB（1 MiB = 1,048,576 bytes）及 128 MiB 总预算，并完成五 family 的全部 publication；中断时也必须在同一事务协议内恢复到可核验的一致代。retirement 必须由精确路径、bytes 和实际删除/替换事实证明，不得用布尔参数声称；WP1 的 `atomic_publish_directory` per-family 锁不能替代该事务。在此 transaction 落地前，不得实现或启用 WP2 writer，也不得在锁外临时超预算后再清理。
