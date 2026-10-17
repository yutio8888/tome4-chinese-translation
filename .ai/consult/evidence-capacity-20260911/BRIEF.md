# 咨询：生产证据即将撞上 128 MiB 硬门禁，如何处置

仓库：`/workspace/tome4-chinese-translation`（ToME4 汉化的翻译审核流水线）
分支：`develop` @ `3d641d7`
本文自洽，但请你直接读源码与仓库核验每一条。**只读**：除了写你自己的回答文件
`.ai/consult/evidence-capacity-20260911/ANSWER-gpt-6-astra.md`，不要修改任何文件、
不要提交、不要跑任何 `tools/i18n production` 的写命令
（`queue rebuild` / `batch *` / `migration apply` 等）。

---

## 1. 问题

`tools/i18nlib/production_review_v2_lite_evidence.py:18`：

```python
MAX_TRACKED_BYTES = 128 * 1024 * 1024
```

超限即在 `prepare-evidence` 抛错（`:138-139`、`:229-230`）：
`prospective tracked evidence exceeds 128 MiB`。
统计范围是 `PRODUCTION_PREFIXES`（`:19-24`），即 `evidence/production-review*/` 等四个前缀。
另有两处同名约束：`production_review.py:906`、`production_review_v2_lite.py:611`。

**当前已用 91.0%，按实测增速还能跑约 14 批，而剩余待审 271 批。**

这个流水线每批审核 80 条译文条目，每批产出一份不可变证据包并提交入库。
撞上限之后 `prepare-evidence` 直接失败，当批 reviewer 输出作废，生产停摆。

---

## 2. 实测数字（`git ls-tree -r -l` 按上述前缀逐快照统计，非估计）

| 快照 | 批次/迁移 | 已提交生产字节 | 占 128 MiB |
|---|---|---|---|
| `78037b2` | 96 / 49 | 100,828,781 | 75.1% |
| `b4bdbee` | 118 / 73 | 119,258,700 | 88.9% |
| **`3d641d7`（当前）** | **121 / 76** | **122,204,299** | **91.0%** |

余量 11.46 MiB。最近 7 次提交的实测增量：

```
80 ev  +493.8 KiB   80 fix  +3.2 KiB
81 ev +1117.5 KiB   81 fix  +4.4 KiB
82 ev +1297.4 KiB   82 fix  +5.1 KiB
83 ev  +444.8 KiB   83 fix  +7.4 KiB
```

均值约 843 KiB/批。→ 约 14 批后硬停。

### 构成（当前 HEAD）

| | 大小 |
|---|---|
| `evidence/production-review-v2-lite/batches/`（121 批） | 47.69 MiB |
| `evidence/production-review-v2-lite/migrations/`（76 个） | 35.07 MiB |
| `evidence/production-review-v2-lite/catalog/` | 33.68 MiB |

单文件前二占总量 52%：

- `catalog/entries.jsonl` **33.59 MiB** —— 29828 个条目的权威目录
- `migrations/840970875076f8086bb546e45c9e2ea2c355fa56b64665e3ab469f0f5aaed4fb.json`
  **32.83 MiB** —— 唯一的 v1 全量 migration；其余 75 个 v2 sparse 合计约 3.9 MiB（均值 53 KB）

### 增长的主因

`batches/*/adjudications.jsonl` 合计 15.55 MiB，其中 **88.9%（13.83 MiB）是
`evidence_snapshot.content`** —— 每条 `disposition=confirmed` 的裁决内嵌**整个源码
`.lua` 文件全文**（见 `tools/orchestration/make_adjudication.py` 中 confirmed 分支
读 `(ENGINE / rel).read_bytes()` 的逻辑）。

内容去重后：**147 个不同快照、合计 2.80 MiB**。纯重复冗余 **11.03 MiB**。

同一条目的 surface 与 contextual 两条裁决各存一份全文；同一源码文件跨批次反复内嵌。

---

## 3. 为什么存在这个快照

游戏源码不在本仓库 git 里（钉在外部 `/workspace/t-engine4` @ `624a6732`），
所以 `confirmed` 裁决无法用 `path + commit` 形式自证，改为内嵌
`{content, sha256}` 快照。证据包的用途是：任何人事后可以离线复核
「当时判定为 confirmed 的依据是什么」。

---

## 4. 约束

- `evidence/production-review-v2-lite/batches/` 下 121 个批次包**已经提交并发布**，
  是不可变证据链；`migrations/` 下 76 个迁移记录同理
- 有一套 17 项门禁（`tools/ci-gates.sh`）与 `queue rebuild` 的完整历史重放
  （`tools/i18nlib/production_review_v2_lite_queue.py` 的 `_projection` /
  `_validated_migration_edges`）会校验这些文件
- 曾有过一次事故：改了 catalog 却没同步 migration 的 `new_catalog_id`，
  17 项门禁全绿、问题完全没被发现，且**无法用后续提交修复**
- 128 MiB 这个数字的原始用意没有文档记载（推测与仓库体积／克隆成本有关）

---

## 5. 已推演的三条路径（数字已算，未实施，也未作取舍）

| 方案 | 回收 | 之后余量 | 之后增速 | 还能跑 |
|---|---|---|---|---|
| 现状 | — | 11.46 MiB | 843 KiB/批 | 约 14 批 |
| A 快照去重（存 sha256 引用 + 内容单独存一份） | 11.03 MiB | 22.49 MiB | 461 KiB/批 | 约 50 批 |
| B A + 重新表达 v1 全量 migration | +32.83 MiB | 55.32 MiB | 461 KiB/批 | 约 123 批 |
| C 调高 `MAX_TRACKED_BYTES` | — | 取决于新值 | 843 KiB/批 | 取决于新值 |

**三条都不够 271 批。**

---

## 6. 请你回答

1. **你会怎么处置？** 给出具体方案与实施顺序。可以不选上面任何一条。
2. 上面第 2 节「增长主因」的分析，以及第 5 节的三条路径，**有没有错或遗漏**？
   特别是：我是否漏掉了更划算的杠杆？
3. **方案 A 改动的是已发布批次的证据格式。** 这在证据链意义上可接受吗？
   若可接受，怎样做才能让「改格式」本身可审计、不破坏既有校验？
4. 如果最终仍需调高上限，**128 MiB 这类约束应该由什么来替代**，
   才不至于把同一个问题推迟到 512 MiB 再撞一次？
5. **如果你的建议被采纳而它是错的，故障会长什么样？** 最早在哪一步暴露？

请把回答写进 `.ai/consult/evidence-capacity-20260911/ANSWER-gpt-6-astra.md`。
