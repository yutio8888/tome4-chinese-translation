建议先在批次边界调整容量政策，给本轮剩余工作留出预算；随后只优化新批次，优先消除重复的 surface group 文件，再处理源码快照复用。保留已发布批次和 migration 的原始字节。当前没有必要为了守住 128 MiB，先承担历史证据格式迁移的风险。

本次核验基准是 `3d641d72d3149ea1526e4937f6029deb41999c21`。以下实测来自 Git 树、实际 JSON 内容和源码，未把 BRIEF 的数字当作输入结论。只进行了读取和内存计算，未调用 production 写命令、未提交。特别说明验证边界：一次直接调用只读 `_projection(HEAD)` 的进程以退出码 143 终止，没有返回结果，原因未确认，**不能算全量重放通过**。随后完成了全部 76 个 migration 的发布边界及前后目录字节绑定核验；这也不等同于完整语义重放。

问题状态：文中明确复算或源码核实的事实为 `confirmed`；实现建议与容量预测为 `advisory`；完整重放、队列缓存读数的独立认证和改造后的端到端验收为 `pending`。本次没有自动进入任何修复。

**1. 我会怎么处置：具体方案与实施顺序**

第一步，在无活动 checkpoint 的批次边界做容量维护，冻结基准 commit、121 个批次包和 76 个 migration 的路径及哈希。先把既有完整重放跑通，留存逐 revision 的状态、winner、reconciliation 基准。容量修改本身不需要修改 catalog、译文、migration 或旧裁决。当前剩余空间只有 12,013,429 字节，应在下一轮昂贵审核开始前处理。

第二步，作为过渡，我建议把本轮生产的逻辑容量预算设为 **512 MiB**，同时落实第 4 问的计量、提前预警与历史政策分离。这个值有明确的阶段性依据：最近四个完整“证据＋修复”批次平均新增 843.394 KiB，以题设剩余 271 批计算，终点约为 **339.746 MiB**，512 MiB 留下约 172.25 MiB 余量。这是规划估计，不能把四批均值当作最坏情况保证。实施时应补看较长窗口的峰值与接下来切片的源码规模；新优化运行约八批后复核预测。

调整必须覆盖所有实际消费者。只改 `production_review_v2_lite_evidence.MAX_TRACKED_BYTES` 会留下 finalize 和历史重放仍使用 `production_review_v2_lite.TRACKED_LIMIT` 的问题。应集中定义当前容量政策，审计旧 WP1 入口是否仍需适用，并同步相关操作文档；历史批次的容量记录按当时政策解释，不能随当前配置浮动。详见第 2、4 问。

第三步，先优化**新批次的 group 文件复制**。目前 `prepare_evidence` 为每个 surface lane 分别复制同一份 group manifest；按精确字节或 SHA-256 去重，每批每份 group 保留一个普通文件，让四个 adapter ref 指向它即可。输入、输出和各 lane 的观察仍各自保留。

这是比改旧证据、引入新快照语法更小的改动。现有 `_validate_ref` 只要求 group 路径位于本批 `raw/` 下、哈希相符；后续比较的是被引用路径的集合，没有要求不同 ref 的 group 路径不同。本次在内存中把最新批次四个 group 路径合并为一个，五个 adapter ref 都通过现有验证器，raw 路径集合也相等。**这仅验证了消费者可接受该引用形状，没有模拟新发布提交。** 生产端还必须一起修改 `_prospective_declared_paths`、实际复制和恢复/abandon 所用清单，不能只删掉三个文件。[复制逻辑](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1583)、[清单生成](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1445)、[引用验证](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:300)

第四步，优化新裁决的源码存储时，优先评估**复用已有 `evidence_path + evidence_commit` 语法**：在生产前，把需要的公开源码原始字节按内容地址归档到本仓库受计量的 `evidence/production-review-v2-lite/sources/`，记录组件、上游路径、固定 commit 或未固定来源、原始 SHA-256；先提交这个归档，再冻结批次。裁决引用本仓库归档的 commit/blob，`evidence_snapshot` 可为空。新源码对象不得在冻结批次后随意另行提交而改变其 base。

现有验证器已经接受本仓库可取回的 commit/blob，所以并非必须先设计 `{sha256, ref}` 新格式。这仍需明确归档清单与来源核验规则，但能避免改旧包和增加裁决字段。源码应从固定 commit 的 blob 读取；DLC 来源未固定则明确记录。归档对象必须计入容量、随离线交付可取得，不能藏到忽略目录或移出前缀来规避统计。暂未归档的新源码可以继续使用现有内嵌形式，并纳入批前预算。[源码证据语法](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_evidence.py:65)

第五步，分别验收预算修改和新包去重。验收应覆盖临界字节数、索引/工作树不一致、被忽略但实际存在的 production 文件、group 共享路径、prepare 中断恢复、缺失/损坏源码对象，以及旧格式和新生成包的重放。完成适用 focused tests、完整门禁，并对候选发布提交执行真实历史重放；需要发布边界的试验先在隔离验证环境形成实际提交，通过后才进入共享发布历史。17 项门禁不能替代这一项。以后若有证据表明历史体积或离线分发成本仍不可接受，再单独立项讨论第 3 问的存储迁移。

**2. 增长分析和三条路径有哪些错误、遗漏？**

三个快照的总量、批次数与 migration 数都复算一致：

| Git 快照 | 批次 / migration | 四个前缀内逻辑字节 | 占 128 MiB |
|---|---:|---:|---:|
| `78037b2` | 96 / 49 | 100,828,781 | 75.1233% |
| `b4bdbee` | 118 / 73 | 119,258,700 | 88.8547% |
| `3d641d7` | 121 / 76 | 122,204,299 | 91.0493% |

HEAD 的实际构成为：

| 内容 | 字节 | MiB |
|---|---:|---:|
| batches 全部 | 50,009,757 | 47.6930 |
| 其中 raw JSON | 24,026,723 | 22.9137 |
| 其中 adjudications.jsonl | 16,304,686 | 15.5494 |
| 其中 results.jsonl | 7,014,379 | 6.6894 |
| 其中 gates.json | 1,430,849 | 1.3646 |
| 其中 manifest.json | 1,233,120 | 1.1760 |
| catalog 全部 | 35,315,244 | 33.6792 |
| migrations 全部 | 36,775,710 | 35.0720 |
| known-dead-keys、repairs、quality 文件合计 | 103,588 | 0.0988 |

**最划算的遗漏是 group manifest 重复。** 612 个 `*-group.json` 共 17,935,476 字节；在各自批次内按内容去重后是 153 份、4,483,869 字节，重复量 **13,451,607 字节，即 12.8285 MiB**。不需要跨批共享就能消除这种重复。它比 BRIEF 所指出的源码正文重复量还大。旧包原样保留时，这些历史字节不会回收，但最近四批仅这个优化平均就能少写约 **128.22 KiB/批**；历史节省潜力和未来增速改善必须分开列。

源码快照的核心统计也基本正确，但需限定口径。我读取了全部 656 条裁决，其中 432 条 confirmed；310 条带 `content` 快照，另有 136 条记录了非空 `evidence_path`，这两类并非互斥。310 份正文的 UTF-8 字节合计 **14,501,327**，占裁决文件的 **88.9396%**；SHA-256 均与正文一致。它们有 147 种内容，共 **2,933,944** 字节，重复 **11,567,383** 字节，即约 **11.0315 MiB**。

但“每条 confirmed 都内嵌整个 Lua 文件”不适用于全部历史。当前 `make_adjudication.py` 确实在 confirmed 分支读整个文件；其中 `cache` 只减少读取次数，JSON 序列化仍会重复写正文。历史快照也包含摘录和短文本。本次把唯一快照与固定 engine commit 的 Lua blob 逐字节匹配，84 种匹配完整文件，63 种没有匹配；后者中直接可见字符串摘录、带路径标题的代码片段，不能据此断言它们都是错误证据。[生成器](/workspace/tome4-chinese-translation/tools/orchestration/make_adjudication.py:38)

还需更正这些数字和推论：

- **75 个 sparse migration 只有 2,352,802 字节，即 2.2438 MiB，平均 31,371 字节。** BRIEF 的约 3.9 MiB / 53 KB 不符实际。前两个大文件合计占总量 **56.99%**，也不是 52%。
- **B 不能把 32.83 MiB 全算作可回收。** v1 migration 的 29,828 行全部是 `revision_changed`，没有 `unchanged` 行。现有 v2 只省略 unchanged，并去掉 `old_rows/new_rows` 快照；转换后仍需约 **18,494,730 字节，即 17.64 MiB**。仅去掉两份快照的节省约 **15.19 MiB**。这是表示大小测算，不是合法迁移产物；正式转换还涉及新 identity、路径和发布边界。若改用另一套更紧凑表达，必须另给方案与实测，不能把它称为现成 sparse v2 的收益。[v2 构造](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_migration.py:349)、[验证规则](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_migration.py:555)
- **A 的 11.03 MiB 是解码后正文重复量，不是精确的 Git 树净节省。** 正文在 JSON 字符串内转义后占 15,723,024 字节，还要计算删除字段、新引用和对象清单的开销。在内存中仅保留快照 SHA、每份正文另存一次，全部历史裁决的理论节省是约 **12.20 MiB，尚未扣新存储元数据**。这不是当前验证器可接受的格式。按最近四批、预先种入此前已有快照的同一假设计算，增速约 399.71 KiB/批；加 group 去重约 271.49 KiB/批，均未计完整新格式开销。这说明 461 KiB 不是已验证的生产常数，也不是可靠的长期斜率。
- 表中的增量实际是**四批、八次证据/修复提交**，不是“最近七次”。八个增量均核对相符，完整批次平均为 843.394 KiB。余量除以均值是 13.91 批，因此“约第十四批遇阻”合理，但不能承诺还可安全完成十四批。新源码文件大小、ISSUE 密度、迁移和批次组成会改变增速。
- **“三条都不够 271 批”对 C 不成立。** 512 MiB 在这个均值下有约 480 批余量；按原增速跑完 271 批预计为 339.746 MiB。只优化未来 group、完全保留旧包，同样预测终点为约 305.812 MiB。提高上限能解决本轮规模，是否值得以及长期如何维护是另一项判断。
- “剩余 271 批”可能略有滞后。只读 SQLite 的 meta 对应当前 HEAD/catalog，缓存为 done 8,255、blocked 1；与目录 29,828 条相减是 21,572 个隐式 queued，即 270 个最多 80 条的切片。由于本次完整重放没有完成，这个队列数字仍是**缓存读数，待全量重放确认**；本文容量规划继续采用题设 271 批，不依靠这一批的差额得出建议。

门禁统计范围也比 BRIEF 的简述复杂：

- `prospective_tracked_bytes` 按四个精确目录前缀计量：同路径取 Git index blob 与工作树大小的较大值，包含 untracked 及被 ignore 的实际文件，再加候选包。暂存删除与未暂存删除处理不同，并拒绝候选路径冲突。因此 `git ls-tree HEAD` 是已提交基准；脏工作树下不是门禁值。它计算逻辑文件大小，不是磁盘块、唯一 Git blob 大小或压缩包大小。[实际计量](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_evidence.py:143)
- `prospective_bytes` 的 138–139 行是独立 helper；当前 prepare 调用的是上述函数，不是两个检查点都会走到。finalize 另按目标 commit 统计实际生产字节，并与 receipt 比较。[提交后检查](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1684)
- catalog 的 `prospective_occupancy` 使用更宽的字符串前缀匹配，且有 WP1 retirement 处理；旧 `production_review.py` 的 `_production_total` 只遍历两个 WP1 目录，并不统计 v2-lite。它们不能被描述成三个完全等价的统一门禁。[catalog 计量](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite.py:600)、[WP1 计量](/workspace/tome4-chinese-translation/tools/i18nlib/production_review.py:809)
- queue replay 还检查旧 `gates.json` 中的容量字段是否低于当前 `catalog.TRACKED_LIMIT`；这一检查不是重新统计当前整棵树。修改预算时遗漏它，会形成生产和消费两套标准。[历史容量验证](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:581)
- 超限会阻止 prepare，但**该分支没有自动作废或删除 reviewer 原始输出**。它删除本次 prospective scratch 包并抛错；checkpoint 中裁决和原始输入输出仍在。若后续通过提交代码改变 HEAD，则可能因冻结 base 等条件不能原样恢复，需要另行按恢复规则处理。这是应该提前维护预算的原因，不能把后果简写为“容量错误必然让 reviewer 输出当场作废”。[失败分支](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_batch.py:1635)

其他杠杆存在，但成本不同。内存压缩试验中，catalog entries 的 gzip 大小约 10.04 MiB，v1 migration 约 12.55 MiB，说明文本压缩潜力很大；现有消费者要求精确文件集合和 canonical JSON，不能直接改后缀就获得这些收益。Git 自身已经对相同文件 blob 复用，并对存储做压缩；当前树去重不能等额降低完整 Git 历史的克隆成本。不要用减少审核 lane、丢弃原始观察或清理仍有重放意义的证据来解决存储问题。

**3. 改已发布证据格式，在证据链上可接受吗？**

**按当前契约，不接受原地实施 A；经单独批准、保持原始字节和发布身份可验证的存储迁移，可以接受。** “语义相同”不足以证明当前链不受影响。

当前批次 manifest 绑定 adjudications/results/gates 的 SHA-256；adapter refs 绑定 raw 文件，且 raw 路径集合必须完全相等。`_publication_commit` 还要求**当前 core/raw 的确切 Git tree entries**，是在 parent 等于原 `base_commit` 的同一个提交中发布。只改裁决会先报哈希错；重算 manifest 哈希后，仍找不到满足这个条件的原发布提交。migration 同样绑定当前 blob、原 base 和原发布时的 catalog。[批次发布边界](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:275)、[迁移发布边界](/workspace/tome4-chinese-translation/tools/i18nlib/production_review_v2_lite_queue.py:1015)

若未来要回收旧包在当前树中的空间，迁移方案至少必须包含以下可审计内容：

- 冻结原始 commit、每个逻辑文件的原路径、原始长度、原 SHA-256、原发布提交/base 关系；转换不得改变 observation identity、裁决、状态或顺序。
- 新存储清单绑定去重对象的哈希、长度、位置及明确的表示版本。若使用压缩，同时校验存储字节和解压后的原始字节，并限制解压资源。应能**逐字节恢复原裁决文件**，包括编码、转义、字段顺序及换行；单纯把恢复内容重新序列化成“等价 JSON”不够。
- 先交付兼容 reader 和验证流程，再生成新表示。原始 Git 发布提交必须保持可达；验证仍针对原发布树及其原字节进行，新存储身份通过独立的转换清单绑定。当前 reader 从 HEAD 枚举批次，需要显式支持归档清单及其覆盖范围，不能仅放宽旧哈希检查，或把新表示伪装成旧提交当时已有的字节。
- 切换前，用旧 reader/原表示和新 reader/新表示重放同一条链，比较每个 revision 的状态、winner、各批次观察、迁移映射和 reconciliation，不能只比总数。还要在没有外部 engine 工作树、没有现存 queue/cache 的离线环境验证缺失对象、篡改对象会失败。
- 用新的追加提交记录转换输入、工具版本、输出对象清单和等价性报告。只有验证完成且回退路径明确，才考虑从当前树退役旧表示。旧提交及原始证据仍需保留；只新增对象而保留当前树的全部旧内嵌内容，不会回收这部分空间。

这是存储表示迁移，不能直接套用“翻译 revision 迁移”的 `migration apply` 来重绑旧事件。全文改为摘录也不是无损格式迁移：它减少了当时可供复核的上下文，应作为新的证据选择决定处理。

事故的关键事实已独立核对：旧 `f5373e4` 中相关 migration 的 base 等于发布提交 parent，entries 哈希相符，但 catalog ID、exclusions 哈希、manifest 哈希不符。“当时 17 项全绿”本次依据的是 runbook 的历史记录；当前 [17 项定义](/workspace/tome4-chinese-translation/tools/i18nlib/gate_results.py:21)确实没有针对生产树直接执行完整 migration/catalog 重放。不能沿用“只有 queue rebuild 才会检查”的绝对说法，`check/status`、batch preflight/finalize 等也能进入 `_projection`。所谓“无法用后续提交修复”，应限定为保留原 publication/base 绑定时，不能随手补写 HEAD 修复旧边界；它不是对所有可能的退役或恢复协议的数学证明。[事故记录](/workspace/tome4-chinese-translation/docs/baseline-batch-runbook-2026-09-06.md:916)

**4. 128 MiB 应由什么替代？**

应替代为**有来源、按版本记录、在批前检查的容量政策**，并区分证据有效性与运行资源。128 MiB 在现有设计中确实是明确的政策约束；本次没有找到将它推导自托管平台硬限制、克隆时间目标或个人磁盘预算的依据。

| 维度 | 应记录什么 | 如何使用 |
|---|---|---|
| 当前生产树 | 已提交逻辑字节、索引/工作树保守占用、候选新增字节、按类别分解 | 延续现有防漏算规则；新 source 对象也必须覆盖 |
| 实际 Git 存储/离线分发 | 可达对象、pack/loose 大小、离线包大小、可复核性 | 衡量维护和分发成本；不能用 HEAD 文件大小替代 |
| 重放资源 | 完整冷重放耗时、峰值内存、临时空间需求 | 对应个人机器的可用资源与可接受等待时间 |
| 每批异常增长 | raw、快照、迁移各自增量，最大文件及解码后长度 | 拦截意外打包大量无关数据；保留正常新增证据能力 |
| 剩余工作 | 剩余条目/切片、近期分位数和峰值、即将使用的新源码对象 | 给出预计终点、余量和预计可运行批数，而非只报百分比 |

逻辑体积和真实成本并不等价。本次 `git count-objects -v` 返回 loose 对象 941,204 KiB、pack 111,543 KiB，范围是整个本地仓库，也受打包状态影响；这不是生产目录大小或一次 fresh clone 的下载量。它至少说明 116.54 MiB 的生产树指标不能直接代表实际仓库存储。调整 logical limit 应有实际磁盘余量和重放测量支撑。

在操作上，我建议：每批结束更新预测；当保守预测不能覆盖剩余已授权工作，或 runway 低于预先约定的维护提前量（例如 30 批）时就提示维护。在 `batch start` 之前检查预计最大候选包与资源保留量；prepare/finalize 的精确计量仍保留为最后一道保护。不要等 reviewer 全跑完后才首次发现总量不足。预测可用近期 20–30 批的分布和已知源码新增量；样本不足时明确范围，不把 P95 当作硬上界。

容量规则只保留一个当前定义，但**历史 receipt 必须有稳定解释**。现有 schema 的旧记录可继续按明确的 legacy 128 MiB 规则验证；新记录绑定新的政策版本/哈希、适用额度与测量口径，且在一次批次期间冻结。将来降低当前预算，应限制新增发布或触发维护，不应让合法旧批次忽然变成无效证据。不得让 receipt 自报任意上限后自行获准。

长期追加的证据一定会增长，任何有限总量阈值都需要维护策略。未来达到实际磁盘、离线包或重放资源预算时，应提前选择扩容，或批准能够离线恢复完整原始链的归档/退役协议。只把老文件移到 Git 历史能减少 checkout 占用，不能自动缩小完整克隆，也不能让当前只枚举 HEAD 的 reader 自动理解它们。现在先保持单队列、单锁、单 checkpoint；用可测的触发条件决定是否需要更多存储机制。

**5. 如果建议错了，故障会是什么样，最早在哪暴露？**

| 可能的错误 | 故障表现 | 最早应暴露的位置 |
|---|---|---|
| 均值低估，512 MiB 仍不足 | 后续源码较大或 ISSUE 增多，runway 快速下降；极端情况下 prepare/finalize 超限或资源不足 | 每批预测更新、下一批开始前的预算检查；若只保留现状，会拖到审核后才报错 |
| 只改一个容量常量 | prepare 放行，finalize 或新历史重放仍报 128 MiB 超限 | 使用较小测试额度构造跨阈值发布，覆盖生产、提交后和重放三条路径 |
| group 复制去重但清单未同步 | prepare 恢复时报路径/postimage 不符，或 replay 报 raw 集合不等于 refs | 新包 prepare、受控中断恢复、候选提交的真实重放 |
| 去重按文件名或宽松文本比较 | 不同来源/内容被混为一份；若重写引用哈希，还可能让错误上下文通过表面校验 | 归档时逐字节比较和原始 SHA-256 校验；测试必须含同名不同内容对象 |
| 归档了错误源码版本或不相关片段 | 快照自哈希通过，但 confirmed 实际依据错误，属于可能静默通过的证据缺陷 | confirmed 形成之前的固定 commit/blob 比对和 claim 上下文核验；普通 JSON/hash gate 无法判断机制证据是否相关 |
| 直接改旧 adjudication/migration，或删旧文件省空间 | 改文件会触发哈希/发布边界错误；删掉整批则可能使 HEAD 枚举不再看到它，已完成状态退回 implicit queued | 原始字节清单比较、归档覆盖检查以及切换前后逐 revision/winner 重放比较；总数相等也不够 |
| 为压缩 v1 migration 把 changed 当成 unchanged | 错误继承旧 revision 的 done，或者丢失迁移映射 | 对原发布前后 catalog 调用现有 reconciliation 并比较完整映射；这里 29,828 行 changed 的基准尤其关键 |
| 引用对象只在开发机或不完整历史中可用 | 本机成功，fresh/offline replay 找不到 commit/blob 或解码失败 | 无外部源码、无 queue/cache 的完整离线复核；对象缺失必须失败，不能降级为相信 SHA 字符串 |
| 只看 17 项全绿就发布 | 再次把 catalog/migration 或发布身份不匹配写进共享历史 | 候选实际提交的历史重放；本次核对的旧事故就是这条路径 |

还要明确回退边界：一旦新政策下已有超过 128 MiB 的批次发布，就不能假设简单 revert 预算代码仍能消费这些合法历史。预算政策、reader 的兼容支持和数据回退必须一起设计；通常应保留已发布版本的读取能力，再限制未来写入。

目前最需要避免的误判，是把“容量数字变小”当作成功。我的建议可被证伪的验收标准是：旧证据路径/字节/发布身份保持可验证；新包的完整审核输入输出和裁决不减少；当前逐条队列状态和 winner 不因存储优化改变；独立离线重放可完成；每批增长和资源成本有实测下降或在明确预算内。本次已验证体积、重复来源、group 引用形状和 76 个迁移字节边界；**完整重放以及任何改造后的端到端行为，仍是实施前后必须完成的验收，不是本咨询已经通过的结果。**
