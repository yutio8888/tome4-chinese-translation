建议把已批准的 **512 MiB 政策与新批次 group 去重作为一个实施提交**；第 3 项单独提交、单独开关，获批后与前两项在同一最终候选上做一次完整验收。第 3 项不能按“把 `derive` 的字典存到磁盘，再检查自带 SHA”实现。

本设计对第 3 项的建议是：**始终从 Git 重验发布边界；跨进程只保存经过认证的纯函数验证凭据和紧凑 reconciliation 计划。** 认证需要缓存目录之外的本机密钥，并明确把正确的验证程序和密钥列为信任根。若维护者不接受这个新增信任边界，就不启用 catalog/reconcile 的跨进程成功缓存；保留现有重算。不能同时承诺“任意同用户篡改也可信”和“免于重新证明计算结果”。

本次为设计咨询。BRIEF §1、§2 的规模与计时直接作为已复算的输入；实现核验基准为 `3d641d72d3149ea1526e4937f6029deb41999c21`。开始时 HEAD 为 `7809b7bb92f23bdbf60b3ffeeb091d4cd2eb4c93`，二者仅 `handoff.md` 不同，本文涉及的实现相同。`confirmed` 指以下源码核对及小范围复现；设计选择为 `advisory`，改造后的测试、实际性能和完整历史重放均为 `pending`。没有运行全量 `_projection`、生产写命令或提交；唯一写入为本答复。

**1. 合并实施方案：文件、函数和提交边界**

下表中的新模块、函数和参数是待实施接口，不是当前已有命令或能力。

| 项目 | 文件及函数 | 具体改法 |
| --- | --- | --- |
| 统一容量政策 | 新增 `tools/i18nlib/production_capacity.py` | 定义只追加的政策注册表、当前写入政策 ID、`resolve_policy()`、`validate_receipt_capacity()`、`assert_within_limit()`；政策记录含额度和计量口径。禁止从 receipt 自报额度创建政策 |
| 四处容量消费 | `production_review_v2_lite_evidence.py` 的 `prospective_bytes/prospective_tracked_bytes`；`production_review_v2_lite.py` 的 `prospective_occupancy/retirement_preflight`；`production_review_v2_lite_batch.py` 的 `_committed_production_bytes/finalize/_recover_committed_checkpoint`；`production_review_v2_lite_queue.py` 的 `_batch_rows` | 前两类使用当前或显式冻结的生产政策；提交后使用该批冻结的政策；历史 replay 根据 receipt 版本选择历史政策。删除两套独立可调数值，错误消息输出实际 policy ID、bytes、limit |
| 批前计量 | evidence 模块新增 `_existing_production_sizes()`、`measure_current_occupancy()`；batch 的 `start/prepare_evidence` | 抽出既有 index/worktree 保守计量，供 admission 与最终精确计量复用；见第 2 项。不要为得到当前占用而伪造一个 candidate 目录 |
| 新批次运行格式 | batch 的 `CHECKPOINT_KEYS/_load/_new_checkpoint/_reconcile_checkpoint` | 新 checkpoint 使用 exact schema 2、kind `production_review_v2_lite_active_batch_v2`，在原字段外固定 `capacity_policy_id`、`capacity_policy_sha256`、`raw_layout`。schema 1 保留原 exact parser，并映射至 legacy 128 MiB 与旧 raw 布局；不改写已有 checkpoint |
| 新容量 receipt | batch 的 `prepare_evidence`；queue 的 `_batch_rows` | 新 `gates.json` 外层 schema 3，含政策 ID/hash；旧 schema 1/2 按历史规则读取。内层统一门禁 `result` 仍为现有 schema 2，`gate_results.validate_historical()` 不改成执行缓存 |
| group 去重 | batch 的 `_raw_evidence_name/_prospective_declared_paths/prepare_evidence`，新增 `_raw_copy_plan()` | 由一个确定性 plan 同时生成 raw 路径集合、每个 ref 的目的路径、去重复制任务。group 以完整 SHA-256 命名、批内共享；input/output 保持逐 ref 独立 |
| 恢复与清理 | batch 的 `_validate_prepare_resume/_validate_abandon_prospective/_remove_generated_prospective_temps/abandon` | 统一使用冻结布局对应的 plan；先核对 canonical 清单，再处理明确属于清单的临时文件或 postimage，不能扫描后把未知文件补进授权清单 |
| 缓存存取 | 新增 `tools/i18nlib/projection_memo.py`；`git_evidence_reader.py` 的 `projection_scope/derive` | 新建受认证凭据存取层；保留现有 scope 内存缓存和退出清理。不要把通用 `derive(kind, identity, load)` 自动全部持久化；只给列明的 catalog、reconcile、publication 类型专用接口 |
| 缓存接线 | queue 的 `_projection/_catalog_from_tree/_publication_commit/_migration_publication_commit/_validated_migration_edges` | 加每次投影独立的 `MemoSession`、当前 Git 图和非磁盘缓存的边界核对。publication 命中条件见第 3 项；不得从磁盘直接返回五元组 projection 或 winner |
| reconciliation | migration 的 `reconcile/validate_migration/_validate_v1_migration/reconciliation_rows_for_tree` | 保留无缓存参考算法；分离“生成完整 mapping”和“按原约束核对 mapping”。只在 queue 已验证的 Git catalog pair 上允许认证的紧凑计划生成完整 mapping；v1 snapshots、v2 exceptions、行哈希、顺序与守恒仍核对。当前 projection 已有的 validated edges 可显式复用，避免最新边界再算一次 |
| 可观测与退出开关 | `cli_production.py` 的 `register/dispatch`、queue 公共读取接口 | 新增只读 `production queue verify --treeish COMMIT --projection-cache=off\|authenticated --json`，直接报告 Git projection，不读写业务 SQLite。缓存默认 `off`，获批上线后才切换默认；所有 writer 的入口也可用同一显式选项强制 `off` |
| 文档和测试 | `i18n/README.md`、`docs/translation-production-review-v2-lite-plan.md`、`docs/agent-workflow.md`；已有 `test_production_review_v2_lite*.py/test_git_evidence_reader.py`，新增对应政策与 memo 测试 | 记录新旧格式、容量解释、缓存信任边界及回退命令；补第 4 项用例。保留历史 runbook 的原始事件叙述，不全文替换历史的“128 MiB” |

代码文件未写前缀者均在 `tools/i18nlib/`。不修改 catalog 的 `policy-v1.json`：其中的 policy 是译文身份/审核规则，不是运行容量政策。复用那个 `policy_sha256` 会无谓地改变 catalog 和迁移链。批次 `_batch_id(mode, selected, attempt)` 的算法、有序 revision 集与 entry identity 同样保持原定义；checkpoint 的容量和布局是运行元数据。

提交安排如下。

1. **提交 A：已批准的 1+2。** 容量 registry、四个消费者、新旧 checkpoint/receipt 分派、group plan 与恢复测试一起交付。两项共享 checkpoint/prepare 的改造，一次引入 schema 2 比两个互不兼容的半成品更易实施；不要求为了“分项”硬拆这两项。其 focused tests 必须可在没有缓存模块的情况下通过。
2. **提交 B：待批准的 3。** 认证层、queue/migration 接线、绕过开关、故障测试及文档独立于 A。必须可单独撤销或禁用，不把 A 的容量读取能力绑在 B 上。第 3 项未获批时，A 可以交付，B 不进入启用状态。
3. **生产数据提交必须在上述工具提交之后另作。** 先完成无活动 checkpoint 的维护边界、独立复审和最终组合验收，再以新工具提交为祖先开始批次。不能在活动批内提交工具代码；它会改变冻结的 `base_commit`。不能把 reader 上线和第一份新 evidence 混成一个事先没有合法冻结 base 的批次。

A、B 可在一个有界维护任务中开发、复审，最终组合运行一次完整门禁；每个逻辑提交各有定向测试即可，不必机械地每个提交跑一次全量。真实发布提交的重放及故障注入仍是独立验收覆盖，不能被“只做一次门禁”取消。实施属于共享证据/恢复链路的大型变更，应按仓库约定由 Paseo 的唯一 EXECUTOR 写入、独立 REVIEWER 复审；本次只读设计不启动这套编排。

**2. 容量政策：512 MiB、历史解释、批前检查与预警**

政策 registry 至少包含：

```text
legacy-production-capacity-128-v1  -> 134217728 bytes
production-capacity-512-v1         -> 536870912 bytes  [当前新写入政策]
```

每项是 canonical 的只读描述，包含 `policy_id`、`limit_bytes`、支持的 measurement ID；`policy_sha256` 是该描述的 SHA-256。registry 是受审查的工具代码，已有 ID 的内容永久不改；未来改变额度或口径用新 ID。常量兼容名如需暂留，只能是 registry 的只读别名，生产逻辑不得分别 patch 两个 limit 决定行为；测试改为注入一份测试政策。

**计量口径保持明确，不能假装四处已经是同一算法。**

| 阶段 | 口径 |
| --- | --- |
| 批次 prospective / admission | 四个 `PRODUCTION_PREFIXES`；同路径取 index blob 与实际普通文件大小的较大值；含 untracked、ignored；保留 unstaged deletion、冲突、symlink/special 的拒绝规则 |
| 提交后 actual | 目标 commit 的四个前缀内普通 blob 逻辑字节之和；按路径计数，同 blob 在不同路径出现两次仍算两份 |
| catalog retirement prospective | 保留 `prospective_occupancy()` 现有 WP1 退役扣除、路径冲突和更宽的 `is_production_path()` 语义，登记为独立 measurement ID。此次只统一额度来源，不顺手缩小统计边界 |
| 历史 receipt | 解释当时记录的 prospective/committed 值及政策，不用今天的树大小代替当时的记录；不声称这一步重演了当时的 index/worktree |

这保留当前的保守防漏算行为。[现有实际计量](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_evidence.py:143)和[catalog 特殊口径](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite.py:600)应继续有独立用例。旧 WP1 模块中只统计 WP1 的历史入口不应顺带改成新批次入口，也不能被用来代替这四处检查。

新 `gates.json` 的 exact 外层字段为：

```text
schema_version = 3
result                         # 原有真实 full gate result，schema 2
capacity_policy_id
capacity_policy_sha256
prospective_bytes
committed_bytes
```

writer 从 `start` 时冻结的 checkpoint 取 ID/hash，不从调用者任意传入额度；prepare 前后重新确认它们与冻结值、registry 均相符，再参与 gates/manifest 哈希与占用定点收敛。新增字段改变 gates 自身长度，因此沿用当前收敛循环，不把政策字节当成免费开销。内层 gate candidate 不挪用 catalog policy 字段；在既有 live gate binding 检查之外，显式复核 checkpoint 容量政策和布局未漂移。

历史分派必须是精确版本分派：

- schema 1/2 没有容量政策字段的既有 receipt：使用固定 legacy 128 MiB。schema 1 原来允许无占用字段的窄兼容继续保留，不能反过来补造数值。schema 1/2 多出新字段时拒绝，不猜成 schema 3。
- schema 3：只接受 registry 中已知且 hash 精确匹配的政策；两数必须 `type(x) is int`，且 `0 <= x <= policy.limit_bytes`。未知 ID、错误 hash、bool/float、缺字段一律拒绝。
- `finalize` 用 checkpoint 政策，要求发布 receipt 与之相同，精确 committed 占用等于冻结计量；`_recover_committed_checkpoint` 同样按该发布政策恢复。将来降低当前写入预算，不能让“已提交、尚未来得及 finalize”的合法旧批次无法恢复。

BRIEF 指出的不对称成立：当前 queue 的两处旧 receipt 校验用 `catalog.TRACKED_LIMIT`，**调高不会使原先合法的历史失败，调低则会**。只把常量改大甚至会放宽旧 receipt 的验收域。本设计既让新批次用 512 MiB，也把旧 receipt 继续限制在原来的 128 MiB；因此历史解释不随当前政策浮动。[现有两处分支](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:581)

批前检查放在 `batch.start()` 的 authoritative preflight、stable selection 完成后，**新 checkpoint 和 reservation 写入之前**。这里允许既有 preflight 按原规则恢复 orphan，但容量不通过时不能新增 reservation 或 dispatch reviewer。返回当前占用、候选条数、估算预留、剩余空间与预警。`prepare_evidence()` 在完整门禁之前再按已经存在的 raw、裁决和结果计算更精确的候选增量；之后仍执行完整门禁和现有最终精确计量。

建议首版采用以下固定参数，并在实施政策文档中明示它们是 admission/预测策略：

```text
L = 536870912
U = 当前 index/worktree 保守占用
D20 = 最近最多 20 个已验证完整批次区间的正向占用增量
       （含该区间 repair/catalog/migration 增长，不仅是 batches/ 子树）
R = max(4 MiB, 2 * max(D20, default=0), 已知候选新增字节)
admit = U + R <= L
```

实际未满但预留不足时，明确报“批前预留不足”，而不是谎报已超 512 MiB；可缩小下一批切片或做容量维护后重试。样本来自已验证的提交区间，仅用于估算，可作为 derived 报告缓存；不让未经校验的 SQLite 业务状态决定容量。缺历史样本用 4 MiB 起步并标注。`R` 不是 reviewer 输出的数学上界，极大新源码/大量 ISSUE 仍可能超出，因此不能去掉 prepare/finalize 的硬门禁。

预警建议：当前或预计下一批占用达到 **75%（384 MiB）** 为 warning，达到 **90%（460.8 MiB）** 为 urgent；预计全轮终点超过 90%，或按近期 P95 增量估算 runway 少于 30 批，也 urgent。这些提示不改变旧 evidence 的有效性。每批结束更新；新策略运行 8 批后复核 R 与预测。题设 271 批按原均值预计约 339.746 MiB，仅未来 group 去重预计约 305.812 MiB，都只是规划输入。

缓存不在 production evidence 四个前缀，不参与上述逻辑额度；单独报告缓存磁盘占用和重放资源。不得把唯一源码快照、迁移记录或 raw 输出迁到缓存来绕过统计。由于删缓存不丢任何证据，它不是新的归档层。

**3. group 去重与投影跨进程记忆的完整设计**

先把 group 的生成/恢复接口定死，避免实施时只改复制循环。

`raw_layout` 允许 `per-ref-v1`、`shared-group-sha256-v1` 两值，新 checkpoint 选后者。schema 1 隐含前者。`_raw_copy_plan(checkpoint)` 是无写入的确定性函数，返回 `declared_paths`、有序 `adapter_refs` 模板与 `dest -> [(source_path, expected_sha)]` 复制任务；只依赖冻结 checkpoint，因而 abandon 不需要原 scratch 输入还在才能判断目的路径。

```text
input/output: raw/{surface|contextual}/{原 enumerate 序号}-{原名称}.json
group:        raw/groups/sha256-{完整 64 位 group_manifest_sha256}.json
```

对没有 output 的 section 保留当前跳过规则和原 enumerate 序号；不能重新编号导致 input/output 路径漂移。四个 ref 的 group hash 相同，plan 中就是一个目的文件、四个引用；不同 hash 就是不同文件。只去重 group，不合并 observation、envelope、input/output 或 lane，不跨批共享。

prepare 顺序：校验原 checkpoint/accepted refs → 生成 plan、核对已有 prospective 清单 → 跑本次真实 full gates → 将每个源文件读入本次内存并核对**冻结的** expected SHA → 对共享 hash 额外确认源字节相同 → 原子写 checkpoint 的完整 `prospective={path: null}`、`preimage_absent` → 按唯一 destination 写普通文件 → 用同一 plan 生成 manifest refs → 收敛容量及核心文件 hash → 核对实际文件集合恰等于 plan → 写完整 postimage 清单并进入 `commit_ready`。

复制和消费者字节绑定使用刚核验的同一份内存 raw，不在生成 refs 时从变化中的输入重新“接受一个新 hash”。同名不同字节不会合并；哈希相同而字节不同也报冲突，不以重写 ref 来掩盖。使用 `_write_fsynced()`，不使用 hardlink/symlink。

恢复必须覆盖三种状态：

- **写首个文件前或半包中断：** checkpoint 已冻结全量路径、hash 全 null；只允许 canonical 清单的普通文件子集，重跑时用冻结源字节覆盖这些 scratch。已知 `.目标名.tmp` 按现有 ordinary-file 检查处理；未知 `.tmp` 和未知目录/文件不是可自动删除的缓存。
- **完整 postimage 已登记：** `_validate_prepare_resume` 保留现有逐路径 hash 相等要求；删文件、改共享 group 或混入旧 `NNN-group.json` 必须先报错，不先覆盖。`commit_ready` 走原 finalize/recover 流程，不重新 prepare。
- **abandon：** 先要求 `set(gates.prospective) == plan.declared_paths == set(preimage_absent)`，再按原 null/postimage 两种规则验证。授权通过以后才恢复 SQLite、删除该批 prospective。不同 ref 指向一个 group 不会变成“多次删除”；仍按目录下的一份实际文件处理。

新旧布局不能通过“看到磁盘上哪个文件就选哪个”来猜。升级入口要求没有活动 checkpoint；保留 schema 1 reader 是兼容恢复格式，不是授权绕开活动批的 base 冻结。[现有清单与恢复代码](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1445)、[消费者允许共享引用](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:300)

下面是第 3 项的缓存设计。

**3.1 先纠正 BRIEF 的三个前提。**

`validate_catalog_files(bytes)` 在**固定实现和规则常量下**才是纯函数。跨进程还跨工具版本；输入身份必须覆盖全部五个 `CANDIDATE_FILES`，不仅是 entries，也不是仅三个 catalog 文件。既有 `derive` 中的 Python 对象来自本次实际验证；磁盘中的 `valid=true` 没有这个来源保证。

migration/batch 发布 commit 对象不可变，但“在当前 H 可达历史中，它是不是唯一符合当前路径/bytes/base 的发布”是一个查询。增加合并父系可出现两个 sibling publication，切换历史可能使原 C 不再可达。仓库已有[双发布歧义测试](/workspace/tome4-chinese-translation/tests/i18n/test_production_review_v2_lite_queue.py:875)；不能把不可变对象与不可变查询答案等同。

`key = SHA(inputs)`、`payload_sha = SHA(payload)` 只能检测错绑和未同步修补的损坏。写缓存的人可以把 payload 改成成功并重算自带 SHA；它没有证明 `payload = validate(inputs)`。因此 BRIEF 第 4 条不能靠自哈希、SQLite integrity check、文件权限或 atomic rename 单独实现。

**3.2 信任边界与保存位置。**

默认目录：`.artifacts/i18n/production-review-v2-lite/projection-cache/v1/<repo-scope>/<verifier-fingerprint>/`；每种 kind 下以 key 的 SHA-256 为文件名。`repo-scope` 绑定已解析的 git common directory 与 object format 的摘要，路径只作命名空间，不是结果有效性的 key。不同 clone 默认不共享认证凭据。

认证密钥建议为本机 32 字节随机值，保存在 `~/.local/state/tome4-i18n/projection-cache-keys/<repo-scope>.key`，不在仓库、`.artifacts`、日志或 evidence 中。目录 0700、文件 0600，拒绝 symlink、错误 owner、可被其他用户写入的父目录；原子独占创建、fsync，创建竞争时重新读已完成对象。默认关闭模式不创建密钥。现有密钥格式或权限异常时禁用缓存并重算，不能通过自动覆盖一个异常密钥假装状态正常。正常缺失可生成新 key，旧缓存自然全部 miss。

缓存 record 保存 exact schema 的 `{kind, key_descriptor, verifier, key_id, payload, mac}`；`mac = HMAC-SHA256(secret, domain_separator || canonical(record_without_mac))`。key descriptor 由调用端从 Git 和当前 verifier 独立构建，不使用缓存自报值选择输入或密钥。MAC 用固定时间比较；只在 MAC 与 descriptor 都匹配后解释 payload。使用 JSON/有界二进制整数数组，不反序列化 pickle 或可执行对象。

只允许成功的无缓存参考函数产生新凭据；缓存失败路径不得“读旧 payload 后重新签名”。原子临时文件、flush/fsync、replace 后才成为命中项；异常或不完整结果不存。不同进程同时计算相同 key 可以重复计算，最后写入同一确定性结果即可，不要求新增生产业务锁。记录默认最大 16 MiB、总量软限 256 MiB，超限就不写/淘汰；大输入仍走参考算法，资源上限不改变证据结论。时间戳只用于淘汰，绝不用于判定有效性。

**这里新增的是有限缓存信任，不是消灭信任。** 能改缓存文件、重算普通摘要但拿不到密钥的污染会被识别；能读取该密钥并运行任意同 UID 代码者能伪造 MAC，0700/0600 不防同用户。验证器本身算错并给错误结果签名也不靠 HMAC 自愈。若第 4 条意指连这两类都必须自动识别，就应裁定不启用成功 memoization；没有独立信任根或等价重算，无法兑现。下面的事故边界核对则不依赖缓存认证，即使内部测试强行送入“已认证成功”也仍须发现该事故。

**3.3 完整 key、失效与读取行为。**

| kind | 调用端独立构造的 key 输入 | payload / 命中后的工作 |
| --- | --- | --- |
| catalog-valid | format/domain；verifier fingerprint；按路径排序的五个文件 `(path, mode, object-kind, blob-OID)`，并绑定本次实际读取 raw 的长度与 SHA-256 | 小型“这组确切 bytes 通过此验证器”的认证凭据，不保存权威 manifest/entries Python 对象。命中仍从本轮 Git raw 解码数据；可以略过已被认证的 canonical/schema/逐行身份复算 |
| reconcile-plan | format/domain；reconcile verifier；old/new 两组 catalog 身份，顺序明确；old/new entries 的 raw hash/长度 | 紧凑的非 unchanged 选择计划，见下节；不缓存 SQLite 行或整份 normalized migration |
| publication | format/domain；Git 查询环境 fingerprint；verifier；base B；当前 required 路径的完整 `(path, mode, kind, blob-OID)` 集合 | 已由原算法验证的发布 C 及当时 H0。只能按下节的当前图检查复用，不能仅凭 MAC 返回 C |

verifier fingerprint 不能只用人为写的 `CACHE_VERSION=1`，也不能使用每次 evidence commit 都变化的 HEAD。首版宁可保守：对本进程采用的 `tools/**/*.py`、`tools/i18n` 的路径和实际源码内容作统一摘要，加 cache format、Python 实现/完整版本、相关运行选项与 Git 版本。导入路径落在未覆盖位置、验证期间源码改变、无法确认实际实现与摘要一致时禁用持久命中；正式使用要求这批工具源码稳定。新模块或依赖文件变化必须自动进入摘要，测试覆盖这条依赖边界。catalog schema/policy 是上述五份数据输入，运行容量 registry 位于被 fingerprint 覆盖的工具代码内。

publication 还依赖有效 Git 查询配置；固定本程序 query argv，并对影响 Git 行为的有效配置/环境取摘要，原值不进日志。首版遇到 shallow repository、replace refs、grafts 或无法解释的历史替代配置就走现有无缓存路径，不能把这些语义静默归一成普通历史。hash 算法不受支持同样回退；现有 reader 对非 SHA-1 本来也不提供相同快路径。

每次 projection 先把 `treeish` 解析成固定 H，此后用 H。H 变化不必清掉所有 catalog/reconcile 内容缓存，但必须重新枚举当前树、migration/batch 集合和 Git 拓扑；旧发布可达性/唯一性重新核对。修改 exclusions、schema、policy 或 manifest 即使 entries 不变也产生新 catalog key。v2 中术语 provenance 不改 revision，也可能改 row bytes，所以不能拿 revision ID 单独当 row 或 reconcile 输入 key。

缺文件、未知版本、截断、JSON 重复键/非法类型、超长、MAC 不符、key 不符、不可写目录：记一次可诊断的 miss，回落对应原函数；原函数失败就把原证据错误向上传递，**不能返回空 edges、旧 projection 或“status unavailable 但 ok”**。权限/读取故障只禁用本次缓存，不应妨碍从 Git 判真。损坏项可由缓存管理器按固定目录边界淘汰；不能因此删除 checkpoint、queue 或 evidence。需要诊断的只读入口使用 `--projection-cache=off` 时连缓存读写都禁止。

**3.4 与 77 次 catalog 校验、77 次 reconcile 的配合。**

catalog 命中前仍执行 `_catalog_from_tree` 的目录集合、quality sibling、普通文件/mode 检查，以及五份 raw 的实际 Git 读取；每个 blob 在本轮内存 reader 中可复用。证据 raw 不从磁盘 memo 取得。认证凭据只省逐行重复校验，不向调用者提供可伪造的另一个 catalog。首次、版本变化或任何 miss 执行原 `validate_catalog_files(files)`，成功才签发凭据。[当前五文件验证入口](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:173)

reconcile 不把 77 份约 29,828 行的完整 Python/JSON 映射落盘；那会把省下的计算变成大量 IO、解码与内存负担。持久计划采用：

```text
old_entry_count, new_entry_count
exceptions = 按 old ordinal 严格递增的
  [old_ordinal, new_ordinal_or_null, disposition, reason]
未列出的 old ordinal 表示 exact unchanged
```

miss 时跑原 `reconcile(old, new)`，从完整结果提取计划、认证保存。hit 时先验 MAC/schema/ordinal 范围/顺序/唯一性，然后遍历本轮从 Git 得到的所有 old rows：未列出的必须在 new 中有完全相同 logical/revision 的行；例外按指定 ordinal 构造 `_mapping_row` 等价结果，摘要取实际 old/new row bytes。对 non-null 目标保留原唯一映射约束；不得让“省略”意味着删除旧行。最后按原 old revision 顺序生成 full mapping，数量必须等于 old 行数。

为避免仍执行数百万次 canonical dumps，可在本轮 catalog 读取视图中建立每行原始 canonical JSON bytes（不含末尾 LF）的 SHA-256，供 row hash 复用。视图记录既有 raw 中的 offset/length，按需散列后释放临时切片，不再复制 77 份全量行文本。只有本轮验证或认证成功的**确切 Git 行**能提供这个摘要，且仅用于该固定输入视图；不能按 revision ID 缓存，也不能把外部可变 dict 的 hash 偷换成旧值。固定视图的行不能被调用者修改；需要修改的消费者取副本。原公共 `reconcile(list, list)` 仍使用原 `_row_sha` 路径；queue 的固定视图内部接口显式传入行摘要，普通调用者不能自行宣称“verified”。这种本轮复用不新增磁盘信任。

生成的 mapping 仍送入原 migration 约束：v1 的 old/new snapshots 与完整 rows 精确一致，v2 的完整结果去掉 unchanged 后必须**恰等于**记录中的 sparse rows；不能只检查缓存计划“看起来合理”。`_reason_changed` 的 precedence、v1/v2 args_order、removed/ambiguous/unmapped 的含义不变。缓存只是认证复用既有分类计算，并不授予迁移记录跳过语义匹配的资格。[原分类及行哈希](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_migration.py:179)、[v2 完整比较](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_migration.py:555)

内部可把 `validate_migration` 拆为 `_validate_record_and_snapshots`、`_compare_reconciled_rows`，让公共函数始终先调用原 reconcile；queue 专用入口只接收由本轮固定 catalog pair 产生的结果，再执行相同后两步。不能增加可由 CLI 传入的 `assume_valid/expanded_rows` 绕过参数。

`_projection_contents` 已有每个边界的 normalized rows。计算当前 SQLite reconciliation 时优先复用**本次** `validated_edges` 中唯一匹配当前 catalog 的边，并确认当前 entries 输入与该边一致；否则保留 `reconciliation_rows_for_tree` 的完整校验路径。这个对象不跨进程，禁止拿 cache/SQLite 自报的 edge 列表替代当前 Git 枚举。这样消除第 77 次重复，不改变当前链路检查。

**3.5 与 121 次 `_publication_commit` 的配合。**

本轮先用一次 `git rev-list --parents --topo-order --reverse H` 建立完整可达 commit 集、真实父列表、`single_parent_children[B]` 和 winner 所用 order；首版每次从 Git 获取这张图，不持久采信它。对普通历史采用以下保守快路径，batch 和 migration 共用：

1. 在当前树读取 required 集合及其 modes/kinds/OIDs，查对应 publication 凭据；batch 是四个 core 加**实际全部 raw**，migration 是该 canonical 文件。
2. 凭据必须已认证，C 必须在本轮可达集，父列表恰为 `[B]`，且 C 的树逐项等于当前 required entries。
3. **只有当前可达图中 B 的单父 child 恰为 `[C]` 时，才用这条快路径。** 原算法的所有合格发布都必须是这样的 child；因此此时不可能有第二个符合 base 的发布。C 本身当初已通过原算法的逐路径 AM history 条件，不能用一个未经原算法认证的“树恰好相同的空提交”代替。
4. 任一条件不满足，包括多个 sibling child，即调用现有 `_publication_commit` / `_migration_publication_commit` 全算法；唯一匹配才记录凭据，歧义照原错误拒绝。多 child 但实际只有一个合格发布的历史可能一直走慢路，首版接受这个性能代价，不削弱语义。

这既能减少线性生产历史下数千次 `git log`，也不会把“早先唯一”误当成“合并之后仍唯一”。C 或 B 被 rebase/amend 会改变 OID 或父关系；复制相同文件但缺原发布、同树空提交、删后重加、merged sibling 等必须保留原算法判定。不能为了命中而只保存某个路径的 `git log -1` 结果。[原发布算法](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:275)

**3.6 事故检测必须在缓存之外，顺序固定。**

把 `_validated_migration_edges` 的边界部分抽成 `_assert_migration_git_bindings()`，只接受本轮直接从 Git raw 解码的 migration、base/pub manifest 与 tree。不得接受 memo 提供的 manifest 或“bindings_ok”。其检查顺序为：

```text
当前 Git 树枚举 migration；读实际 blob 并校验原 record
  -> 定位并核对当前唯一 publication C，parent(C) == B
  -> base_tree == tree(B)
  -> 从 B / C 的真实 catalog manifest 和 blobs核对
     old/new catalog_id
     old/new manifest.json 的整个文件 SHA-256
     old/new entries / exclusions SHA-256、counts、schema/policy 数据绑定
  -> 以上全部成功，才用 catalog/reconcile 的认证复用结果继续
  -> 全量 migration chain、ancestry、batch evidence、winner 推导照常执行
```

可在当前 projection 的内存中复用已读的 Git bytes 和同一边界比较结果；禁止磁盘 `edge_valid=true` 短路整段。尤其要区分两种 manifest hash：这里比较的是 `SHA256(manifest.json 文件 bytes)` 与 migration 的 `new_manifest_sha256`，不是误取 catalog manifest 内部同名或近名字段。

本次用 `git show` 读取事故提交 `f5373e4991ee21eb2b355599bb876a0eae7a42c6` 及其 `0eafbff1…` migration，复核结果如下：

| 绑定 | 结果 |
| --- | --- |
| base 等于真实 publication parent | 相等 |
| new entries SHA-256 | 相等 |
| new catalog ID | migration 为 `bf106c02…`，实际为 `ba75b711…`，不等 |
| new manifest 文件 SHA-256 | `6b0b4d1f…` 对 `220c691b…`，不等 |
| new exclusions SHA-256 | `c0ffd55d…` 对 `db3c165f…`，不等 |

进一步在内存中从当前源码 AST 提取 `_validated_migration_edges`，让 record validator 和 `validate_migration` 都直接“成功”，publication 固定为实际事故 C，catalog 返回实际 Git raw 解出的 manifest。仍在调用 reconciliation 之前抛出：

```text
migration publication catalog identity drift
```

这是对“独立 Git 边界比较足以捕获这次事故”的小范围 `confirmed` 证据，不是新缓存实现的验收。它说明真正的保护是**独立读取真实发布 catalog 并逐项绑定**；仅靠新 key 导致一次 cache miss 不够，更不能把 entries 相同当作 catalog 相同。事故即使被人为预装“成功缓存”，这条独立比较也必须照样失败。

正常热缓存会减少验证、分类和历史搜索，仍需读/解码 catalog、展开 mapping、hash、查树、重验 raw/adjudications/gates、推导链与 winner。`167.8 - 140.8 = 27.0s` 只是把三项开销全部归零后的算术下界，**不是本设计承诺**；MAC、IO、解码、图检查和 mapping 展开都非零。验收目标建议热运行中位数不超过 60 秒，27 秒仅作探索目标。若不达标，先提交测量结果再决定下一优化，不以删边界检查达标。

**4. 验收方案：分别覆盖，最终组合验收**

实施前在无活动 checkpoint 的隔离验证环境冻结 production 路径、mode、blob/hash 清单与当前完整投影基准。当前 121 批、76 migration 的数字用于给定基准；实施时若 HEAD 前进，重新标记候选，不把不同树的结果放在同一性能比较中。开发测试允许在临时 Git 仓库形成实际提交；本咨询未执行这些写入。

| 项目 | 定向验收 | 必须有真实 Git 提交的覆盖 |
| --- | --- | --- |
| 512 MiB | 四个消费者逐个测 limit−1、limit、limit+1；legacy 两种 gates、v3、未知政策/hash/bool/负数；新政策下降时旧 receipt 仍有效；index 比 worktree 大、ignored 文件、路径冲突、删除歧义；admission 失败无新 reservation | 发布一份额度高于 128 MiB 且低于 512 MiB 的新 v3 包，再 finalize、删派生队列重建、恢复 commit-ready；可以用测试政策的小额度等比例夹逼走完整路径，同时用整数测试核对真实两项常量，不要求生产仓库制造巨型垃圾 |
| group | 4 refs/同 bytes→1 group；两组 bytes→2 group；不同源码路径同 bytes、同名不同 bytes、无 group、混合 contextual、序号空洞；input/output 数量与 hash 不减少；冻结 hash 不符及模拟 hash 碰撞拒绝 | 用真实 current-consumer raw 构造新共享 group 包，prepare→提交→finalize→独立进程重放；旧包也重放。仅 `_validate_ref` 的内存试验不能证明 publication/恢复正常 |
| 恢复 | 在冻结 inventory 后、首个 group `.tmp`、rename 后、写 refs/core 中途、定点收敛中、完整 postimage 后逐处注入中断；resume 或有显式授权的 abandon；未知文件/坏 postimage 拒绝时 DB/checkpoint 保持原值 | 提交后、`_replace` 前、checkpoint 删除前中断，按 `recover-from-head` 恢复；shared group 的所有 refs 和 postimage 清单最终一致 |
| cache | 每个 kind 做 off/cold/hot；截断、换 payload 后重算普通 SHA、错 key、旧 verifier、换 key、权限异常、写入竞争、key 丢失、cache 丢失、达到 cache 额度；篡改都 miss 并真实重算，真实证据错误不得吞掉 | 同一输入不同进程真命中；新 HEAD 新 catalog/migration；merged sibling、不可达 publication、同树空提交、路径替换/revert、shallow/replace 走慢路；保留现有歧义和重建回归用例 |

容量测试要覆盖 `_recover_committed_checkpoint`，不能只测 finalize。group 测试应扩展现有 C42/C46 中断/临时文件用例；publication 的现有 merged sibling 测试必须先暖旧分支缓存，再 merge 后检查，不然只能证明冷路径没坏。[现有中断用例](/workspace/tome4-chinese-translation/tests/i18n/test_production_review_v2_lite_queue.py:1939)、[现有临时文件用例](/workspace/tome4-chinese-translation/tests/i18n/test_production_review_v2_lite_queue.py:1814)

防事故验收分三层，三层都要有，不能互相替代：

1. **最小真实发布夹具。** 构造合法 catalog A、迁移 A→B；在发布 C 中使 entries 保持相同，却合法重建 exclusions/manifest/catalog ID，migration 仍指向原 B，且 parent/base 正确。即使门禁 receipt 全绿，`queue verify`、`check/status`、finalize/recover 的投影路径都必须拒绝。先用前一合法状态暖 catalog/reconcile/publication 缓存，再运行坏提交；冷、热、off 三种模式均拒绝。
2. **主动污染夹具。** 分别伪造带自洽普通摘要的 catalog 成功凭据、reconcile 计划、publication C，验证 MAC/key 检查触发重算。另在内部单元测试中故意把认证函数替成“通过”、提供伪造成功结果，以确认 `_assert_migration_git_bindings` 从真实 Git raw 仍拒绝上述脱钩；不能让 mock 接管该独立读取。它检验的是架构隔离，不能声称因此 HMAC 能防同 UID 攻击。
3. **历史事故锚点。** 只读验证固定 `f5373e4991ee21eb2b355599bb876a0eae7a42c6` 及该 migration，记录具体错误和 offending path。若隔离仓库不包含事故对象，显式导入/构造夹具后验证，不把对象不存在当成“事故被抓到”。修正后的对应历史/当前合法链应通过。正例与负例都必须比较证据错误原因，不能仅断言“命令返回非零”。

将 `_assert_migration_git_bindings` 的八个 old/new identity/hash 比较逐一做 mutant 测试：为每项构造只在该比较处不匹配的专项输入，直接测试这个边界函数；移除该比较后，相应的“应拒绝”测试必须失败。不能只用同时错三个字段的事故样本证明每项覆盖，也不能被无关 gate 提前挡住。另测 counts、base_tree、parent、reachability、uniqueness。新增只读 verify 命令不修改 queue；writer 拒绝路径则比较故障前后 SQLite 逻辑 tuple、checkpoint 字节及 evidence 清单，确认验证在其更新之前。

最终组合验证包含：

- `tools/ci-gates.sh` 完整检查集。工具维护本身若按验证矩阵证明不影响 addon，可记录 `--skip-build` 依据；正式批次验收仍要 full receipt 和严格 build，不跨命令缓存门禁结果。
- 对固定最终 H，分别用无缓存参考路径、冷认证路径、另一个进程的热路径，比较 catalog/entries、**每个 revision 的全部 override tuple**、winner commit/path、完整 reconciliation、迁移链及 progress 的稳定业务字段。不比较耗时、缓存计数或 rebuilt_at；只比 done 总数不足以发现错误迁移。
- 原有 evidence 路径/mode/字节清单不变。新包实际 group 文件数等于 distinct raw hash 数；逻辑节省等于少复制的原 group 字节再计入路径/refs/gates 元数据差额，不能把历史 12.8285 MiB 当作此次释放空间。
- 在临时完整 clone 中删除全部 projection memo 和 queue，执行无缓存只读重放/合法重建；证据结论一致，不依赖外部缓存密钥。活动 checkpoint 场景单独按恢复夹具验，不删除用户的活动恢复数据。
- 记录相同机器、同一 H 的冷/热/off 干净计时，各至少 3 次，计中位数、峰值 RSS、缓存磁盘字节、hit/miss reason、原函数执行次数、Git 子进程数。热路径已有 catalog/pair 不应再次执行完整验证/reconcile；实际字节读取和边界检查仍应发生。新追加一次小 migration 后，旧内容应命中，仅新输入 miss。

全量重放设置至少 600 秒单次预算，给未来增长留余量；以可轮询的进程运行，不能在 120 秒/短等待到期时自动判失败。若被 SIGTERM/143 终止，记录“未完成”，不记通过。八个子命令的整批 wall time 也要测，不能拿单次热查询代替批次吞吐结果。

缓存模式打开之前，必须完成独立 reviewer 对输入 key 覆盖、签发路径、热 publication 唯一性论证和非缓存边界路径的代码审查。缓存计时未达目标是性能未验收；出现证据差异则禁用 B 并保留 A，不得通过改 golden 结果让它通过。

**5. 回滚方案：按 writer、reader、运行时分别处理**

| 项目 | 尚未发布新格式时 | 已发布/有活动新批次时 | 要不要重建 |
| --- | --- | --- | --- |
| 512 MiB | 可在无活动 checkpoint 时撤销新写入政策；已有 legacy reader 不受影响 | 保留 schema 3 和所有已发布 policy ID 的历史读取能力。若降低新生产额度，用新 policy ID 限制后续 admission；不能整块 revert 回 queue 只懂 128 MiB 的代码，也不能删除 registry 的 512 项 | 单改当前写入政策不需重建 catalog/migration/evidence；若工具回退改变 verifier，缓存自然 miss。预算不足只停止新增，不反判历史失效 |
| group 去重 | 将新 checkpoint 的默认 `raw_layout` 设回 `per-ref-v1` | 已开始的批次按冻结布局完成或正式 abandon；不在半包中改布局。已有共享 group 包保留字节，其引用形状本就被旧 durable ref validator 支持；同时保留该包需要的新 gates reader | 不重建已发布包、不复制回三份 group、不改 manifest。只有明确选择 abandon 的未提交候选会按既有流程重新准备 |
| 跨进程 memo | 所有入口切 `--projection-cache=off`，或撤销独立提交 B | 同样立即可禁用，既有 checkpoint/base、accepted raw 和门禁 receipt 不依赖 memo。不能通过删 queue/checkpoint 来“清缓存” | memo 目录可单独删除，认证 key 可废弃；以后开启从 Git 重算并重新填充。仅禁用缓存不要求重建业务队列；若怀疑错误结果曾被写入 SQLite，则先 off 模式验证，再按活动批恢复规则修复/重建 |

一旦发现缓存造成过错误投影，先保存失败输入和诊断、禁用缓存、跑无缓存比较；只存在于 SQLite 的错误按恢复协议处理。如果错误已经影响实际生产 evidence 的内容或发布边界，删除缓存不能修复历史，需要另行裁定 evidence/发布修复。不得把“缓存可删”误说成“任何使用缓存造成的后果都自动消失”。

维护升级必须在批次边界进行，这也使代码回退可控。A 的 reader 兼容层是长期能力；后续即使不用 group 去重、不再给新增生产 512 MiB，也不能随 writer 开关一并撤掉它。

**6. 如果设计有错：故障长相与最早暴露点**

| 设计/实现错误 | 故障长相 | 最早应暴露的步骤 |
| --- | --- | --- |
| 漏掉一个容量消费者，或恢复仍取当前 limit | prepare 通过，finalize/recover/replay 报旧 128 MiB 超限；未来降额后旧包失效 | 四消费者阈值夹逼、发布后降额兼容测试，早于真实生产 |
| 把容量 policy 写进 catalog policy | entry/catalog identity 或迁移需求意外改变，无关历史重算 | A 的旧 catalog/entries/identity 清单比较 |
| 新 receipt 增长未参加定点计量 | committed occupancy 与 gates 不等，或收敛后又变化 | prepare 最终测量；提交后 finalize 的精确比较 |
| admission 预留低估 | 审核后 prepare 仍超预算，或 gate 前候选估算报警 | prepare 前二次估算；极端情况只能最终精确门禁发现。checkpoint 裁决/raw 保留，删除的是 prospective scratch |
| group plan、refs、恢复清单各自实现 | 续跑报 canonical paths/postimage 不符；raw 集合与 refs 不相等 | 中断夹具；否则 prepare/finalize 的实际集合与重放检查 |
| 根据现有磁盘文件猜旧/新布局，或共享文件重新散列后接受 | 中断恢复混入旧副本，或输入漂移被悄悄“合法化” | frozen SHA 对照、未知文件拒绝、同名不同 bytes 测试 |
| 仅用 entries/revision ID 作为缓存 key | exclusions/manifest 改了却命中；v2 同 revision 不同 provenance 的 row hash 混用 | 对每个输入维度单独变更的 key 测试；事故夹具的独立边界核对仍应拒绝 |
| 自哈希被误当认证，或 fallback 把旧 payload 重新签名 | 构造 `valid=true` 并重算 SHA 后能跳过真实检查 | 主动污染测试；若没有该测试，可能一直静默通过 |
| 密钥泄露或验证器签发了错误结果 | 伪造凭据 MAC 合法，普通缓存读取无法辨认 | 无缓存参考重放/独立审查；没有“自动保证最早发现”的承诺。已保留的 Git 边界仍能独立抓到这次脱钩事故 |
| publication 缓存只验 ancestry，不验唯一性 | 合并两个相同 sibling 发布后旧“唯一”结果仍被使用 | 先暖缓存再运行 merged sibling 回归 |
| 把整个 `_validated_migration_edges` 缓存掉 | catalog/migration 脱钩被 `edge_valid` 覆盖，再现全绿漏检 | 强制伪造成功缓存的真实发布夹具；必须在 projection 更新 SQLite 前失败 |
| 紧凑 reconciliation 计划错误省略例外或改变 reason | changed successor 继承旧 done，或 removed/ambiguous 状态错传 | 未列出行 exact-match 检查、v1/full 与 v2/sparse 精确比较、逐 revision winner 差分 |
| 从 SQLite 取缓存 baseline | reserved 被当 committed，blocked retry 丢掉旧 tuple | start 后下一 preflight，或 retry/abandon 精确恢复测试；本设计禁止持久缓存 overrides，原测试仍保留 |
| 持久存完整 expanded rows 或不断全量 invalidation | 缓存占多 GiB、热路径仍慢、每次 evidence commit 都重新花 168 秒 | 缓存字节、原函数调用次数及三次热运行计时；不能以功能通过替代性能交付 |
| 验收只跑 17 gates，不跑真实候选提交重放 | 算法用例全绿，但本次真实发布边界损坏 | 指定最终 H 的 off/cold/hot 实际重放；这是发布前必须单列的检查 |

维护者对第 3 项需要裁定的具体内容，是是否接受上述**本机密钥与受认证验证凭据**的信任边界及默认启用，而不是笼统同意“加缓存”。批准后按 B 实施；不批准则交付 A、保持完整重算。无论如何，Git 发布边界的独立核对、旧 evidence 字节和历史容量解释均不依赖这一裁定。
