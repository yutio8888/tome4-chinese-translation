# Projection trust model 设计裁决 — gpt-6-astra

核验日期：2026-09-11。本文是只读咨询，没有实现改动。

流水线源码以 brief 指定的本地提交 `3575d720e7a37e3d75c6a747fff23e85559c0962` 为核验基线。开始检查时 HEAD 已是 `83816924f6b6dd6a6ec0c8ee20ea8992fce7f96e`；本次引用的 queue、batch、migration、catalog、Git reader、门禁定义及相关测试文件与该基线没有差异。`624a67329fe2ad440c5b344785a9c73fcf22ae63` 是游戏 engine 的固定提交，见 [版本 manifest](/workspace/tome4-chinese-translation/i18n/versions/tome-1.7.6.json:6)；已在本地 engine 仓库确认该 commit 对象存在，没有访问网络。

证据状态：`confirmed` 表示已核对源码、Git 字节或只读复现；`pending` 表示只有既有报告、未独立复测；`advisory` 表示设计建议。没有打开生产 SQLite、调用生产 CLI、运行门禁或完整历史重放；唯一写入是本回答文件。

## 1. 裁决

**不采纳：不能仅凭 `meta.evidence_head == HEAD` 且 `meta.catalog_id` 匹配，就把现有 `state_override` 当作 Git 重放得到的 committed overrides。**

决定性理由已经是 `confirmed`，不需要假设攻击者、磁盘损坏或罕见崩溃：**正常运行的活动批次就会使这两个对象不同，而两个 meta 字段仍然匹配。**

当前关系应写成：

```text
P(H) = 从提交 H 验证、重放得到的 committed projection
D    = SQLite 中的当前状态，包含活动批次对 P(H) 的覆盖

meta.evidence_head == H 不能推出 D.state_override == P(H).overrides
```

`_projection` 的 overrides 来自 durable evidence 的 winner，结果只允许 `done|repair_required|blocked`，见 [queue.py:522](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:522)、[winner 汇总](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:729)。但 `batch start` 会直接向同一张表 `INSERT OR REPLACE` 写入 `reserved`，并不更新 meta，见 [batch.py:1207](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1207)。后续阶段也修改该表，见 [phase transaction](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:965)。

因此，按提案直接替换后，正常 queued 批次的下一次 preflight 会把自己的 reservation 当作 committed winner，在 [_validate_mode_prior](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:771) 报：

```text
queued batch contains a committed winner
```

`retry_blocked` 更不能靠排除活动行解决：原来的 blocked winner 已被 reservation 覆盖，旧 `batch_id/attempt/result_sha256/updated_at` 不在该行里了。恢复和 abandon 需要完整旧 tuple；checkpoint 的 `prior_effective_state="blocked"` 不能重建它。见 [checkpoint 构造](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:789)、[精确恢复](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1238)及[既有测试](/workspace/tome4-chinese-translation/tests/i18n/test_production_review_v2_lite_queue.py:389)。

我只从源码 AST 提取 `_validate_mode_prior`，以合成 tuple 在内存中调用，未导入生产模块、未接触数据库。结果为：

```text
queued       + committed baseline → PASS
queued       + SQLite reservation → queued batch contains a committed winner
retry_blocked + committed baseline → PASS
retry_blocked + SQLite reservation → retry_blocked batch lacks its exact current committed blocked winner
```

**应优化重复验证。可接受的方向是复用已验证、与活动写入分离的 committed baseline，继续拿它校验当前 SQLite。** Git 保存唯一 durable truth，并不要求每条命令重新计算同一个函数；但现有可变业务表不具备这种缓存的语义。

## 2. 对 brief 第 4、5 节逐条回应

**支持理由 4.1：HEAD 钉死，因此投影一直有效。部分同意。**

固定 H 下，先前验证的 committed baseline 可以保持有效；这不能保证后来被修改的 SQLite 仍等于它。另有一个生命周期措辞错误：禁止的是批内无关提交，正式 evidence commit 必须发生在 finalize 之前；`finalize` 检查的是新提交的 parent 等于 `base_commit`，然后重放新提交，见 [batch.py:1696](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1696)。仓库锁也是每次 writer 调用持有的合作式锁，不是整个批次期间阻止任意 Git 操作的锁，见 [writer_lock](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:221)。

**支持理由 4.2：相同 SHA 决定相同 Git 内容。同意前提，反驳推论。**

问题不在 SHA 的密码学强度，而在 SQLite 的行没有被这个 SHA 覆盖。`evidence_head` 是数据库自报的构建来源，schema 没有将它与全表内容绑定，见 [meta/state schema](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:35)。同一 H 下的一次合法 SQL 更新，可以保留所有 meta 字段。若进一步设计缓存，`catalog_id` 必须与独立从固定 Git tree 得到的 catalog 匹配，不能让两份可变运行时数据相互作证。

**支持理由 4.3：`_replace` 刚验证过数据库。只在其发布时成立。**

实际顺序是先创建并写入临时数据库，再对照传入的 projection 检查，替换目标文件后再检查，见 [_replace](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:850)。它证明当时的结果，不证明之后所有 writer 都未改变结果。批次 writer 会正常改变 overrides；migration transaction 还会更新 meta，见 [migration.py:832](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_migration.py:832)。meta 不是不可变的验证凭据。

**支持理由 4.4：收益巨大。同意必须解决性能问题。**

以 brief 的无 profiler 耗时作预算，14–18 次重放是每批约 38.5–49.4 分钟。这个数量级足以支持专门优化，不必等项目结束才处理。但它不能使两个不同的数据对象变成等价对象；每批实际能省多少，取决于保留哪些独立验证以及消除哪些调用。

**支持理由 4.5：排除恶意同用户，因此伪造缓存不在威胁模型。前半句同意，结论不成立。**

正常 reservation 已足以反证。另一个属于误操作的例子，是维护脚本把某个合法 revision 的 `blocked` 改成 `done`，却没有对应 evidence。SQL 状态约束、`integrity_check` 和两个 meta 字段都可以通过；现有 schema 没有业务证据外键或全表内容摘要。见 [schema](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:42)、[_schema_check](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:777)。这是源码允许的反例，**不是声称生产库已发生这种损坏**。

**反对理由 5.1：注释明确要求先取得 Git 权威输入。同意它的设计意图。**

关键是 expected 与 actual 独立。[_reconcile_phase_tuples](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:934) 用 committed baseline 检查无关 overrides 和未选中 winner；如果 expected 也来自同一张当前表，这两项检查就会退化为自我比较。注释不意味着永远不能改性能实现；已经验证的独立 baseline 可以满足这个意图。`3575d72` 的同进程复用保留了它，见 [strict_check](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:943)。

**反对理由 5.2：门禁漏过 migration/catalog 绑定事故。同意事故根因，但“只有 rebuild 会验”不对。**

我直接核对了旧提交 `f5373e4` 的 migration `0eafbff19953399dc0ba143d837c49a528b3e740ee28d795e5fd3915ffe176db.json`：它的 `new_entries_sha256` 与发布提交的 entries 相同，但 `new_catalog_id/new_exclusions_sha256/new_manifest_sha256` 都不匹配。其中 catalog ID 是 migration 的 `bf106c02…` 对发布 catalog 的 `ba75b711…`。其 `base_commit` 确实等于发布提交的 parent。修正后的发布提交 `e296503` 使用新 migration，catalog 绑定相符。事故的核心字节关系为 `confirmed`；“当时 17 项全绿”的运行结果仅有 [runbook 记录](/workspace/tome4-chinese-translation/docs/baseline-batch-runbook-2026-09-06.md:916)，本次未重跑。

[17 项门禁定义](/workspace/tome4-chinese-translation/tools/i18nlib/gate_results.py:21)没有对当前生产 Git 历史直接执行 queue replay 的检查；测试覆盖算法不等于验证这份真实历史。但是 `_projection_contents` 无条件调用 `_validated_migration_edges`，所以 `check/status/strict_check/finalize` 也会走此验证，见 [queue.py:661](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:661)、[check/status](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:962)、[finalize](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1705)。

这个事故支持保留**每个新发布边界的独立验证**，不证明同一个已验证 H 必须每条命令完整重验。正确缓存不能把“出现新 HEAD”处理成只更新 meta。

**反对理由 5.3：HEAD 不匹配能拦漂移，匹配时是否也会错？明确会。**

第 1 节是正常运行的确定性反例，4.5 是业务误写的反例。`2d5e6a7 → b4bdbee` 的旧 meta 事件在 `git show --no-patch --format=fuller 3575d72` 的提交说明里有记录；本次未恢复当时 SQLite，所以该次运行事实为 `pending`。单纯 HEAD 不匹配是缓存失效，不足以证明数据库行已损坏。

**反对理由 5.4：可重建性质仍在，只是日常不验。需要加条件。**

忠实缓存当然可以保留该性质。但“删掉后能从 Git 算出一个状态”，不等于“删掉后能重建此前对外声称的同一 durable 状态”。如果仅存在于 SQLite 的 `done` 被采信，重建会回到 `blocked/queued`，这时不变量 6 已经不成立。活动批次未提交成果本来就允许丢失、重做，不能把它与 durable 状态混在一起，见 [计划 §4.2](/workspace/tome4-chinese-translation/docs/translation-production-review-v2-lite-plan.md:195)。

## 3. 如果我错了：故障、发现时间和恢复边界

| 情形 | 故障长相与发现时间 | 能否事后修复 |
| --- | --- | --- |
| 我拒绝得过于保守，其他优化达不到吞吐要求 | 重放继续占据批次时间，排队进展缓慢；下一次完整批次计时即可发现，不必等到几百批以后 | 可以后续引入经过验证的缓存；单纯优化决策保守不要求重写已有 evidence |
| 直接把当前表当 committed overrides | 正常 start 后的下一次 preflight 报第 1 节两个错误之一；立即可见 | 恢复正确 reconciler，按现有 checkpoint 恢复流程处理；该错误发生在这次 reconciliation 写 SQL 之前 |
| 为让快路径工作，又绕过 prior/selection 或把未选中 SQL 行当 expected | 可能误报 done、漏掉 blocked 重试、选择错误批次或错误推导 attempt；可能在同一 HEAD 的后续步骤中一直未被发现 | 若只改变本提案位置而保留 finalize 等独立重放，纯 SQLite 漂移会在后续独立检查时报错，或在 finalize 重建时被纠正；已经浪费的审核时间无法追回 |
| 进一步跳过新提交验证，错误进入 migration/catalog 发布历史 | 重放报 publication identity/hash drift 或 migration chain 错误；其他 17 项门禁不保证发现，暴露时间取决于下一次真正独立的重放 | 改 HEAD 当前文件不能自动修复原发布绑定；保留原证据意义时可能需要改写相关发布边界，或者显式撤销边界及依赖成果 |

第三、四行是要区分的故障层次。**不能把“采信一次错误 SQLite”直接说成“永久伪造了已提交审核结果”。** 当前 `finalize` 仍从 Git 重放，而 durable result 的 `final_state` 也必须由 accepted observations/adjudications 推导，见 [queue.py:567](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:567)。只有这些边界也被削弱，或错误确实成为新证据，持久后果才会扩大。

同样，“事故无法用后续提交修复”应精确理解为：不能在保持原 publication/base 绑定的同时，随手补写当前 catalog 或替换 migration blob 来修复它。[_migration_publication_commit](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:1015)同时绑定当前 blob 和原 parent；但候选又只取当前 tree 中仍存在的文件，见 [_projection_contents](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:646)。因此，撤销错误边界及其依赖是一种不同的恢复策略，不能把“任何后续提交都绝不可能恢复”当成已证明的定理。本次没有设计或执行恢复序列。

## 4. 对 B+C+D 的看法

**建议把 B+C+D 作为下一步有界优化；若达到题设的 45 秒 × 9 次，投影成本约为每批 6.75 分钟，足以显著缓解当前瓶颈。我不认为已有证据证明组合现在“已经足够”，也不认为应据此承诺全项目后半程的耗时。**

**B：值得做，但“搬到磁盘就不改变信任模型”不准确。**

当前进程内记忆来自刚执行成功的验证函数，并在 scope 结束时清空，见 [GitEvidenceReader](/workspace/tome4-chinese-translation/tools/i18nlib/git_evidence_reader.py:30)。磁盘命中还需要确认缓存没有错绑、损坏或由旧验证器生成。`entries_sha256/exclusions_sha256` 能把对应原始 bytes 绑定到 Git manifest，不能单独证明任意缓存的 Python 对象、overrides 或“验证成功”标志正确，也不验证 migration 的发布边界。

B 的最小设计要求应包括：key 覆盖实际全部输入和验证器版本；保留 Git 文件集合、类型和 mode 检查；缓存只由成功验证产生并原子发布；命中验证输入/载荷摘要与版本，缺失或不匹配走原路径；保留明确绕过缓存的参考重放。若字面要求“任何磁盘派生物永不受信”，B 也不能无条件豁免重新验证。这里可接受的是针对不可变验证结果的有限缓存信任，不是授予当前业务表权威。

brief 的 key 描述也需要纠正：[_catalog_from_tree:195](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:195)遍历全部 `CANDIDATE_FILES`，实际是 **5 份**文件：三个 catalog 文件，加 schema 和 policy，见 [定义](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite.py:28)。`validate_catalog_files` 在固定实现下只吃 bytes，但也依赖当前实现的 schema/rules 常量，见 [校验入口](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite.py:386)；跨版本缓存不能只用数据 blob ID。

**C：支持，且可以保留完整证据语义。**

批量读取 Git 对象、减少重复历史查询，针对的是已报告的子进程热点。实现必须保留 publication 唯一性、精确 parent、各路径当前 blob、Git 拓扑与 winner 顺序，不能把“找到一个相关提交”代替原规则。brief 的“117 次 git log”很可能把函数调用数当成了子进程数：[_publication_commit](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:275)对每个 core/raw path 分别调用 `_candidate_commits`，而后者每次执行一次 `git log`；117 次 publication 调用不是 117 次 log。

**D：支持显式复用，单纯合成一个进程不会自动减半。**

当前 [projection_scope](/workspace/tome4-chinese-translation/tools/i18nlib/git_evidence_reader.py:40)每次调用都创建新缓存，包括嵌套调用。必须实际传递同一个独立 projection，并在复用边界重新确认固定提交与适用输入；当前 checkpoint、raw outputs、phase tuple 和门禁输入仍需按各自规则验证。`3575d72` 已示范这种复用；此外普通 start 的 `_restore_orphans`、preflight 的 strict check、start 自身 strict check 仍可形成多次重放，见 [batch.py:800](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:800)、[batch.py:1176](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1176)。这比把活动表当历史 baseline 更有直接依据。

**性能估算不能混用 profiler 与干净计时。** B 删除的 120.2 秒来自总计 226.5 秒的 profile，不是 164.8 秒那次。因此不能计算 `164.8 - 120.2 ≈ 45` 来证明 B 单独的收益。即使按该 profile 理想地完全消掉这项，仍剩 106.3 秒；再理想地消掉全部 51 秒 Git 成本，仍剩 55.3 秒的 profiled 时间，尚未计入磁盘缓存读取成本。`reconcile` 的 44.5 秒也不是 B 所缓存的 catalog 校验。45 秒可以是待测目标，不能当既有事实。

B/C 主要降低重放常数，D 降低重复次数；历史枚举和迁移处理仍随规模增长。若实测后仍慢，下一步应设计**独立、不可变、可丢弃的 committed projection 缓存**，将 HEAD、完整输入身份、验证器版本与载荷绑定，保留活动覆盖层及不命中时的原始重放。它的更新和校验契约需要单独明确；不能靠从现有 `state_override` 过滤几种状态凑出来。这仍然是对本提案的“不采纳”。

## 5. brief 最可能错的陈述，以及核验结果

**最关键的错误是第 1 节的“overrides 正好逐行存在 state_override 表里”，并进一步把它理解为当前两者等价。** 第 1 节给出的正常 start 路径和内存复现已推翻它，状态为 `confirmed`。核验不需要在生产库里做任何实验：读 `start` 的 INSERT、`_validate_mode_prior` 的 membership 判断、`retry_blocked` 的恢复逻辑即可。

其他需要更正或保留不确定性的陈述如下。

| 陈述 | 核验结果与状态 |
| --- | --- |
| `_reconcile_checkpoint` 实际只使用五元组第 4 项 | **confirmed：不准确。** 当前还在 `batch.py:1077` 将完整 tuple 传给 `_reconcile_phase_tuples`，再在 `:987` 传给 strict check；`queue.py:794` 解包全部五项，并检查 meta、catalog membership 和 reconciliation。替换为仅有 overrides 的查询并不能直接满足这个调用链 |
| `_check_projection` 不符一律报 drift | **confirmed：不准确。** `queue.py:818–825` 明确允许 active checkpoint 存在且所有 override 的 batch_id 非空时的差异；该分支甚至涵盖 reconciliation 差异。writer 的详细 override 核对由 phase reconciler 补充。“完整重放”与“每处无条件拒绝任何 DB 差异”不是同一事实 |
| 只有 rebuild 校验 migration/catalog 绑定 | **confirmed：错误。** 所有执行 `_projection_contents` 的入口都调用 `_validated_migration_edges`，详见第 2 节 |
| catalog memoization key 是三个 blob ID | **confirmed：错误。** 实际 key 覆盖五份 `CANDIDATE_FILES`，详见第 4 节 |
| 基线规模为 117 批、72 migrations | **confirmed：与指定 Git tree 不符。** 按源码当前候选枚举口径，`b4bdbee` 和 `3575d72` 都是 **118 个 batch manifest、73 个 migration**；其中 migration 为 v1 1 个、v2 72 个。开始咨询时的 `8381692` 是 119/73。不是仅由咨询期间 HEAD 前进导致的差异 |
| catalog 29828 条、entries 约 35 MB | **confirmed：吻合。** `3575d72` 的 manifest 为 29828 条，entries blob 为 35,223,150 字节 |
| rebuild 在 queue.py:928，migration edges 在 :1041，phase 调用在 batch.py:1074 | **confirmed：行号过时。** 本次基线分别是 **:932、:1048、:1077**；`_projection:639`、`_check_projection:791`、`strict_check:943`、`_reconcile_checkpoint:990` 及 migration 的两个函数起始行号吻合 |
| 干净计时 164.8 秒、profile 明细以及未来 730 秒 | **pending：本次未独立复测。** 旧 125.4 秒可核对 runbook §37，最近约 160–175 秒可核对 `3575d72` 提交说明；不能以这些记录声称重测了 164.8 秒。批次数与迁移数同时增加，两个历史点不足以把未来成本唯一归因于“每批 1.9 秒” |

数量核验使用的是 `git ls-tree -r --name-only <固定提交> -- evidence/production-review-v2-lite` 后在内存计数；manifest 读取、entries 大小及事故哈希核对均使用 `git show/cat-file` 的固定提交字节。没有把活动工作树的增量混入基线。
