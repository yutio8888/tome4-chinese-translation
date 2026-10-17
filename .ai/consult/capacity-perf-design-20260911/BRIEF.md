# 设计委托：容量预算调整 + group 去重 + 投影的跨进程记忆

仓库：`/workspace/tome4-chinese-translation`，分支 `develop` @ `3d641d7`
承接你上一份 `.ai/consult/evidence-capacity-20260911/ANSWER-gpt-6-astra.md`。

**本次要的是可实施的设计，不是分析。** 但仍然**只读**：除了写
`.ai/consult/capacity-perf-design-20260911/ANSWER-gpt-6-astra.md`，不要修改任何文件、
不要提交、不要跑 `tools/i18n production` 的任何写命令。实施由别人做。

---

## 0. 维护者已批准的范围

维护者看过你上一份报告后裁定：

1. **把容量上限调到 512 MiB** —— 已批准
2. **group 去重** —— 已批准（按你的建议只作用于新批次，不动已发布字节）
3. **投影的跨进程记忆** —— 新增项，尚未批准，本次请你连设计带风险一起给，供裁定

三项改同一批文件，**一次做完比分三轮少两次全量验收**，所以请给一个合并的实施方案，
并明确哪些步骤必须分开提交、哪些可以同批。

---

## 1. 你上一份报告的核验结果：全部复现，无一夸大

我逐条独立复算过，以下你的数字**精确吻合**，可以直接当作设计输入：

- `*-group.json` 612 份 17,935,476 字节；批次内按内容去重后 153 份 4,483,869 字节；
  重复 **13,451,607 字节 = 12.8285 MiB**
- 76 个 migration 中最大 1 个 34,422,908 字节；其余 **75 个合计 2,352,802 字节，均值 31,370**
  （我此前写的「3.9 MiB / 53 KB」是错的，已更正）
- v1 全量 migration 的 29,828 行**全部**是 `revision_changed`；
  `old_rows` 7,964,077 + `new_rows` 7,964,077 = **15.19 MiB**，去掉后仍剩 17.64 MiB
- 裁决 **656 条 / confirmed 432 / 带 content 快照 310 / `evidence_path` 非空 136**；
  147 个不同快照，解码后 2,933,944 字节，**JSON 转义后 15,723,024 字节**
- 147 个快照中 **84 个与固定源码树某个 `.lua` 整文件逐字节相同，63 个是摘录/片段**
- 超限分支（`batch.py:1635-1639`）`rmtree` 删的是 prospective 暂存包，
  checkpoint 里的裁决与 raw 输入输出保留 —— 你对我「reviewer 输出作废」的更正成立

我另外查到一处你只提了一半的事实，请纳入设计：

**`TRACKED_LIMIT` 共有四个消费者**，且其中一个造成不对称：

| 位置 | 用途 |
|---|---|
| `production_review_v2_lite_evidence.py:18` `MAX_TRACKED_BYTES` | prepare 计量 |
| `production_review_v2_lite.py:26` `TRACKED_LIMIT`（`:611`、`:715` 消费） | catalog prospective |
| `production_review_v2_lite_batch.py:1692` | finalize 提交后复核 |
| **`production_review_v2_lite_queue.py:592`、`:620-621`** | **重放时校验历史 `gates.json`：`0 <= gates[key] <= catalog.TRACKED_LIMIT`** |

因为最后一处拿**当前**常量去校验**历史**记录，所以：
**调高对历史证据是安全的（旧值只会更低于新上限），调低会当场让合法旧批次变成无效证据。**
这条不对称请写进政策设计。

---

## 2. 性能实测（我刚测的，干净计时，非剖析器数据）

一次完整 `queue._projection(root, "HEAD")` = **167.8 秒**。

| 项 | 次数 | 耗时 | 占比 |
|---|---:|---:|---:|
| `validate_catalog_files` | 77 | 71.3s | 42.5% |
| `migration.reconcile` | 77（共 2,296,756 行） | 34.8s | 20.7% |
| `_publication_commit` | 121 | 34.7s | 20.7% |
| git 子进程合计 | 5,489 | 43.5s | 25.9% |
| └ `git log` | 2,626 | 35.5s | — |
| └ `git cat-file` | 2,298 | 7.3s | — |

（git 与 `_publication_commit` 重叠：后者开销基本就是那 2,626 次 `git log --full-history`。）

cProfile 补充：13,919,631 次 `json.dumps`（76.8s 累计）、20,813,592 次 `sha256`、
108,428,518 次 `isinstance`。我实测过「复用单个 `JSONEncoder` 实例」只有 **1.09×**
（全程省约 5.1s），**微优化无效，唯一杠杆是少做几次**。

**一批约 8 个子命令各做一次重放 ≈ 22 分钟/批，剩余 271 批。**

---

## 3. 第 3 项的设计要点（我的初步论证，请你审）

这三块之所以每个进程都重算，不是因为正确性要求，而是因为**已有的记忆没有跨进程保存**：

- `validate_catalog_files(bytes)` 是字节的纯函数
- 某个 migration 的 base／发布提交永不改变
- 某个批次一旦发布，它的发布提交永不改变

代码**已经**在做这件事：`git_evidence_reader.derive`，键是从 blob ID 算出的内容身份
（`queue.py:195-197`），正是它把 275 次 catalog 读折叠成 77 次校验；
其 docstring 自己写着「re-parsing identical bytes cannot produce a different answer」。
但 `projection_scope` 每次新建 reader 并在退出时 `clear()`（`git_evidence_reader.py:48-52`）。

可缓存部分 71.3 + 34.8 + 34.7 = **140.8 秒 = 84%**，全热时一次重放理论上剩约 27 秒。

**我认为必须写死的边界**（请你审，并补我漏掉的）：

1. 键必须是 git 对象 ID／内容哈希，不能是路径或时间戳
2. 缓存放 `.artifacts/`，**不得进入证据树**，不得被计入或规避容量统计
3. **删掉缓存必须永远安全** —— 缓存只能是加速，不能是任何结论的唯一来源
4. 缓存损坏或被篡改时必须**失败关闭**（回落重算），而不是静默采信

第 4 条是这项的核心风险：重放存在的意义就是抓那次「17 项全绿却毫无察觉」的漂移，
而一个被污染的缓存恰好能掩盖同一类漂移。

---

## 4. group 去重的已知实施面

你上一份指出 `_validate_ref`（`queue.py:300`）只要求 group 路径位于本批 `raw/` 下且哈希相符，
没要求不同 ref 的 group 路径互异，所以多个 adapter ref 可以指向同一份。
你也指出生产端必须同步改 `_prospective_declared_paths`、实际复制
（`batch.py:1583`）、清单生成（`batch.py:1445`）以及恢复/abandon 所用清单。

请在设计里把这几处的改法写具体，并说明**中断恢复**路径怎么保证一致。

---

## 5. 请你交付

1. **合并实施方案**：三项的改动清单（文件 + 函数 + 改法），以及提交切分建议
   （哪些必须独立提交、为什么）
2. **政策设计**：512 MiB 怎么落地才能覆盖全部四个消费者、历史 receipt 怎么保持稳定解释、
   批前预算检查放在哪一步、预警阈值取什么
3. **投影跨进程记忆的完整设计**：缓存位置、键的构造、失效条件、失败关闭的具体机制、
   以及它与 `_publication_commit`（121 次）和 `reconcile`（77 次）各自怎么配合
4. **验收方案**：每一项分别怎么验，哪些必须做真实发布提交才能验，
   以及怎样证明「加了缓存之后，那次 catalog/migration 脱钩事故仍然会被抓到」
5. **回滚方案**：三项各自怎么回退，回退后是否需要重建任何东西
6. **如果你的设计有错，故障会长什么样、最早在哪一步暴露**

答案写进 `.ai/consult/capacity-perf-design-20260911/ANSWER-gpt-6-astra.md`。
