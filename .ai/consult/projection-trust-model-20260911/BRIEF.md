# 咨询：是否应把 SQLite 队列从「派生层」提升为「权威层」以消除重复历史重放

仓库：`/workspace/tome4-chinese-translation`（ToME4 汉化的翻译审核流水线）
分支：`develop` @ `3575d72`
本文自洽，但欢迎你直接读源码核验每一条。**只读**：除了写你自己的回答文件，不要修改任何文件、不要提交、不要跑任何 `tools/i18n production` 的写命令（`queue rebuild` / `batch *` / `migration apply` 等）。

---

## 1. 问题

`_reconcile_checkpoint`（`tools/i18nlib/production_review_v2_lite_batch.py:994`）目前每次都从 Git 完整重放整段证据历史：

```python
current_projection = queue._projection(root, "HEAD")
```

但它实际只用到这个五元组的**第 4 项** `overrides`（`batch.py:997`）：

```python
committed = {row[0]: row for row in current_projection[3]}
```

而 `overrides` 正好逐行存在 `.artifacts/i18n/production-review-v2-lite/queue.sqlite3` 的 `state_override` 表里，`meta` 表还存着 `catalog_id` 与 `evidence_head`。

**是否应该改成：当 `meta.evidence_head == git rev-parse HEAD` 且 `meta.catalog_id` 匹配时，直接从 SQLite 读 overrides，跳过重放？**

请给出：采纳 / 不采纳 / 有条件采纳（条件是什么），理由，以及**如果你判断错了，故障会长什么样**。

---

## 2. 成本事实（已实测，非估计）

一次 `queue._projection(root, "HEAD")` 在当前规模（117 批证据 / 72 个 migration / catalog 29828 条 / 35MB entries.jsonl）：

- 干净计时 **164.8 秒**
- 历史对照：96 批 / 49 迁移时是 125.4 秒（见 `docs/baseline-batch-runbook-2026-09-06.md` §37）
- 斜率约 **1.9 秒 / 已完成批次**，随项目推进线性增长

cProfile 热点（226.5s 含剖析器开销那次）：

| 项 | 累计 | 占比 |
|---|---|---|
| `_validated_migration_edges` | 173.2s | 76.5% |
| └ `validate_catalog_files`（73 次 × 1.65s） | 120.2s | 53.1% |
| └ └ `json.dumps` 13,200,259 次 | 72.4s | 32.0% |
| └ `reconcile`（71 个 sparse 迁移） | 44.5s | 19.6% |
| git 子进程（11,183 次 spawn） | 51.0s | 22.5% |

一批 80 条的完整周期约 60–75 分钟，其中约 14–18 次投影 ≈ 45–50 分钟（65–70%）。
剩余待审 21796 条 ≈ 273 批。若不动，投影成本会涨到约 730 秒/次，届时一批光重放约 3.6 小时。

**已经做掉的一项**（commit `3575d72`，不是本次咨询的对象，仅供参照）：
`preflight` 原本在同一进程、同一个钉死的 HEAD 上把历史重放了**两遍**（`batch.py:994` 一次，`batch.py:1074` → `_reconcile_phase_tuples` → `queue.strict_check` 又一次）。已改为透传同一个投影，复用前用 `_head` 重新解析证据提交、不同则照旧完整重放。每个子命令 335s → ~175s。

---

## 3. 现行信任模型（请核验）

**第 1 层 · 权威（唯一真相）**：`evidence/production-review-v2-lite/` 里**已提交**的字节 —— `catalog/`（entries/exclusions/manifest）、`migrations/`、`batches/`。身份全是内容哈希。

**第 2 层 · 派生（永远不受信任）**：`queue.sqlite3`。模块 docstring 第一行：
`"""Rebuildable personal-scale SQLite projection for production-review WP2-Lite."""`
`_check_projection`（`production_review_v2_lite_queue.py:791`）每次都拿它跟现算的投影逐行比，不符即 `queue database state/evidence projection drift`。

**第 3 层 · 未提交的活动状态**：`.artifacts/.../active-batch.json`。唯一「还没进 Git 就必须被采信」的东西，代价是每次打开都对着 Git 全量重验（selection / attempt / batch_id / catalog_id / base_commit / 每条 entry row / 每个 raw ref 的 sha256 与 candidate identity）。

**第 4 层 · 完全不受信任**：reviewer 子 agent 的输出。只以字节进 checkpoint，靠 sha256 与 candidate identity 绑定；源码树钉死在 commit `624a6732`。

支撑机制：仓库级排他锁（`writer_lock`，flock 非阻塞，单 writer）；`_clean_evidence` 在 evidence 目录有任何未提交改动时拒绝执行；批次期间 `base_commit` 必须等于 HEAD；对不上一律 fail closed，从不猜测。

设计文档 `docs/translation-production-review-v2-lite-plan.md` §1.2 不变量 6：
> 删除运行时文件后，必须能从当前 authoritative catalog 与已提交 evidence 重建同一当前状态。

§1.3 明确**不保证**：多 writer、跨主机并发、**恶意同用户防护**、每次 SQLite page 写入都可审计。
—— 即威胁模型是「漂移与误操作」，不是「攻击者」。

---

## 4. 支持采纳的理由

1. 批次进行期间 HEAD 被钉死（`batch start` 到 `finalize` 之间禁止任何提交，这是硬规矩），所以 batch start 时那次 `queue rebuild` 验过的投影，到 finalize 为止一直有效。
2. `meta.evidence_head` 是 40 位 commit sha；提交 sha 在密码学上决定其全部祖先与树。key 相同即内容相同。
3. SQLite 本来就是投影的载体，`_replace` 写入前刚做过 `_check_projection`。
4. 收益巨大且随时间增长：每批省约 35–40 分钟，且能把线性斜率压掉大半。
5. §1.3 已排除恶意同用户；缓存被伪造不在威胁模型内。

## 5. 反对采纳的理由

1. `batch.py:991-993` 的注释把这条边界写死了：
   > Rebuild all checkpoint identity inputs from the authoritative Git projection **before opening SQLite**.
   这是有意的设计决定，不是疏忽。
2. **17 项门禁不校验 migration↔catalog 的绑定关系**，只有 `queue rebuild` 会走 `_validated_migration_edges`。历史上出过一次事故：改了 addon 组件 → 重建 catalog → 只 diff 了 `entries.jsonl` → 用新 catalog 覆盖了 `exclusions.jsonl`，`catalog_id` 变了而 migration 的 `new_catalog_id` 还指向旧值。**17 项全绿，问题完全没被发现，而且无法用后续提交修复。**（runbook「一次事故换来的规矩」）
3. 今晚实测到一次真实漂移：`queue.sqlite3` 的 `evidence_head` 停在 `2d5e6a7`，而 HEAD 已是 `b4bdbee`（第 80 批收尾的纯文档提交之后没补 `queue rebuild`）。是「不信 SQLite」这条规矩把它报出来的。若采纳本提案，这类漂移会在 `evidence_head` 不匹配时被 fail closed 挡住 —— 但请评估：**是否存在 evidence_head 匹配、而 SQLite 内容仍然错误的情形？**
4. 不变量 6 要求「删掉运行时文件后能重建同一状态」。采纳后该性质仍成立（缓存可重建），但**日常路径不再验证它**，退化只会在下一次 rebuild 时才暴露。

## 6. 备选方案（不改信任模型的）

- **B. 把 §37 的内容标识记忆从进程内延到磁盘**：`validate_catalog_files` 已是纯函数（只吃 bytes），key 是三份目录文件的 blob id 三元组（`queue.py:195-197`），可用 manifest 里现成的 `entries_sha256`/`exclusions_sha256` 自校验。预计 165s → ~45s。
- **C. 批量化 git 调用**：11183 次 spawn，`_publication_commit` 的 117 次 `git log` 占 32.6s。预计 −40s/次。
- **D. 相邻 CLI 步骤合进一个进程**：投影次数 ~18 → ~9，零语义改动。

**请一并评估：B+C+D 的组合（把单次重放压到 ~45s、次数减半）是否已经足够，从而使本咨询的提案不必要？**

---

## 7. 关键源码位置

- `tools/i18nlib/production_review_v2_lite_queue.py`：`_projection` 639、`_projection_contents` 646、`_check_projection` 791、`strict_check` 943、`rebuild` 928、`_catalog_from_tree` 175、`_validated_migration_edges` 1041、`_clean_evidence` 203
- `tools/i18nlib/production_review_v2_lite_batch.py`：`_reconcile_phase_tuples` 931、`preflight` 1176、`_reconcile_checkpoint` 990
- `tools/i18nlib/production_review_v2_lite_migration.py`：`reconcile` 283、`validate_migration` 555
- `docs/baseline-batch-runbook-2026-09-06.md` §36–§38
- `docs/translation-production-review-v2-lite-plan.md` §1.2 / §1.3

## 8. 回答格式

写到 `.ai/consult/projection-trust-model-20260911/ANSWER-<你的模型名>.md`，包含：

1. **裁决**：采纳 / 不采纳 / 有条件采纳（条件）
2. **理由**（针对上面第 4、5 节逐条回应，同意或反驳）
3. **如果你错了**：故障长什么样，多久才会被发现，能否事后修复
4. **对第 6 节的看法**：B+C+D 是否已足够
5. **你认为本 brief 里哪条陈述最可能是错的**，以及怎么验证

只写你有证据支撑的结论。不确定就说不确定。
