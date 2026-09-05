# P4：独立复审进度指标

任务 `tooling-optimization-p4-20260905`，实施基线
`563382eeda2db31f1bb49b4229f9a7afc0282344`（开始时 clean develop）。
本报告在完整门禁启动前定稿；完整门禁实际结果以本文指定的机器回执与日志为准，
不在运行期间回写本文，以免改变回执绑定的工作树。

## 实施与口径

`queue init/rebuild/check/status` 的用户可见报告均保留原字段，并新增 `progress`
和 `override_basis`。CLI 文本明确打印 committed evidence 的独立指标、共同分母和
`done` 的 completion-level 分解；原 `explicit_overrides` 只表示状态代码数量，
不是总体复审完成量。`strict_check` 和 `_replace` 继续作为内部业务 API。

纯内存 `Progress` 在同一次 `_projection` 中收集已经验证的结果元数据。
`_projection` 返回的五元组及 SQLite schema 完全不变。结果 blob 使用既有
invocation-scoped reader；仅再解析该已验证结果 blob，不执行第二次完整 projection。
不新增持久状态或全局 cache，不改变排序、winner、迁移校验或 queue 状态机。

四项指标均按当前 eligible revision 去重，以当前 catalog eligible 数量为共同分母：

- S `surface_covered`：有效当前版本结果确有 `surface_verdict=OK/ISSUE`。
- D `deep_reviewed`：有效当前版本结果的既有 `completion_level=deep_reviewed`。
- R `pending_repair`：既有排序选出的最新 durable winner 为 `repair_required`。
- I `historical_revision_invalidated`：历史已审结果沿已验证精确迁移链可定位到当前
  eligible successor，且链上曾发生 revision identity 改变。

S/D 累积有效当前版本证据，不由 `done` 或相互包含关系推断。后续 surface-only 结论
不会擦除同版本的既有 deep coverage，但最新 durable 结论可消除旧 repair。
`committed_done_by_completion_level` 按最新 done winner 的原始 completion level 分解，
因此其 deep 数量不必等于累计 D。被 blocked 的已接受审核证据仍可贡献覆盖率。

覆盖继承只使用原 `_unchanged_rows_through_chain` 结果。I 可以跟随 validated
`revision_changed` 或 `logical_moved` 精确映射；removed、ambiguous、unmapped、
缺失链接和不在当前 eligible 中的终点均不计入。即使 target 改动后恢复旧 revision ID，
也不能绕过中间 changed 边恢复旧 S/D；只有真实的新复审才能恢复当前覆盖。
历史失效独立保留，`invalidated_without_current_review` 则只数 I 中既无当前 S
也无当前 D 的条目，不把已经重审的 successor 描述为当前待审。

`progress.basis=committed_evidence` 始终来自 Git 已提交证据。
正常报告的 `override_basis=sqlite_state_codes` 保留数据库原计数；active writer 时
它可能包含未提交暂态。数据库缺失或 active-writer 检查失败触发既有 fallback 时，
`override_basis=committed_evidence_state_codes`，同时保留既有 `ok/active_writer`
等语义。未提交的 reservation/result 不贡献 durable coverage。

所有 16 个布尔交叉分类单元格（包括零值）都写入 JSON。按任一指标 flag 为 true
求和即可复算该指标，所有单元格求和等于 eligible。空 catalog 的 count/denominator
均为 0，ratio 为 null，避免除零或伪称覆盖率。

## 固定基线实测

`.artifacts/i18n/tooling-optimization-p4-implement/verification.json` 记录从实际
committed catalog、batch 和 validated migration 链回放得到的结果，无计数硬编码。
共同分母 **29,828**；S **1,339**，D **47**，R **0**，I **97**。
I 中已有当前复审 **91**，无当前复审 **6**。
最新 committed done 的层级分解为 surface_only **1,292**、deep_reviewed **47**。

非零交叉分类如下（所有行 R=false，其余单元格为零）：

| S | D | I | 条目数 |
|---|---|---|---:|
| false | false | false | 28,483 |
| false | false | true | 6 |
| true | false | false | 1,204 |
| true | false | true | 88 |
| true | true | false | 44 |
| true | true | true | 3 |

总数 `28483+6+1204+88+44+3=29828`；S=`1204+88+44+3=1339`；
D=`44+3=47`；I=`6+88+3=97`；I 与当前已审交集=`88+3=91`。
本基线 D 恰好包含在 S 内是实际证据的结果，并非算法假设。四个指标不能直接相加
当作完成总量；历史失效 97 也不是当前待重新审核量 6。

业务五元组序列化与宿主固定基线文件逐字节相等：**46,343,568 bytes**，
SHA256 `d8306ac7380b1faa442e0749a7b9c946813664ba835e963a42a77869f239a093`。
历史 evidence **700** 个文件的路径集和每个 SHA256 与宿主冻结清单完全一致；
检查同时覆盖当前文件系统路径集，防止新增未跟踪 evidence 被遗漏。

## 验证命令与产物

所有派生产物位于 `.artifacts/i18n/tooling-optimization-p4-implement/`：

- `python3 -B tools/i18n doctor`：通过，`doctor.log`。
- `PYTHONPATH=tools:. python3 -B -m unittest tests.i18n.test_production_review_v2_lite_progress tests.i18n.test_production_review_v2_lite_queue tests.i18n.test_production_review_v2_lite_migration`：168 tests 通过，`focused-final.log`。
- `PYTHONPATH=tools:. timeout 30s python3 -B -m unittest tests.i18n.test_production_review_v2_lite_queue.QueueTests.test_progress_cli_all_public_queue_reports tests.i18n.test_production_review_v2_lite_progress`：5 tests 通过，`cli-fixture-and-bounded-final.log`。覆盖 init/rebuild/check/status 的 JSON 及 status 文本；同时是有限输入、短超时的 helper 终止探针。此前误指定 `QueueFixture` 的测试选择器失败保留在 `cli-fixture-and-bounded.log`；改为实际 `QueueTests` 后通过，无测试弱化。
- `python3 -B tools/test_groups.py --check`：通过，`registry.log`。新测试注册到既有 production-shadow-surface-ledger 组。
- `python3 -B .artifacts/i18n/tooling-optimization-p4-implement/verify.py`：通过，`verification.json`、`verification.log`、`projection.json`。脚本记录精确基线、序列化比较、历史 hash/pathset 检查及指标。
- `python3 -B tools/i18n production queue init`；`python3 -B tools/i18n production queue status --json`；`python3 -B tools/i18n production queue status`：实际 CLI 回执为 `cli-init.json`、`cli-status.json`、`cli-status.txt` 及对应 `.err`。开始时派生数据库不存在，首次 status 的 missing-database 错误是既有行为；随后只在 ignored `.artifacts` 初始化 SQLite 后验证。
- `git diff --check`，新增文件另以 `git diff --no-index --check /dev/null PATH` 检查，不修改 index。
- **完整门禁：`tools/ci-gates.sh`，不传 `--skip-build`**。报告定稿后执行，stdout/stderr 为 `full-gates.log`；门禁打印独立 `.artifacts/i18n/ci-gates/run.*/results.json` 回执路径，每项实际 argv、退出码、日志 hash、build 与绑定均在该回执中。执行后只向 ignored `post-gate-verification.json` 写入退出码、回执位置和内容 hash 不变检查，不改动本文或实现文件。focused 夹具的模拟门禁日志不作为这次真实完整门禁的成功证据。

新增夹具验证表层单独、深审单独、二者兼具、pending repair、repair 被后续结论覆盖、
重复结果去重、零分母、缺失/removed/unmapped/ambiguous 映射、精确 logical move、
unchanged chain、changed→revert、失效后实际重审，以及 active SQLite 的暂态 done
不污染 committed coverage。真实 Git 迁移夹具验证 changed→revert 两个连续 publication，
不是只检查同 revision 原始结果存在。公开 API 夹具计数验证每个报告仅有一次完整 projection。

首次完整门禁回执为 `.artifacts/i18n/ci-gates/run.0_vsyu4h/results.json`：
除 production-shadow-surface-ledger 分组的一项异常清理测试外均通过，strict addon build
也通过。失败是 `_projection` 在未请求 metadata 时仍传 `progress=None`，使既有双参数
测试替身报 `TypeError`；已恢复无 metadata 的原调用形式，不修改该测试或 reader。
首次日志保留为 `full-gates-first.log`，首次内容 hash 检查保留为
`post-gate-verification-first.json`（该次运行内容未漂移）。修正后的针对性验证命令为
`PYTHONPATH=tools:. timeout 30s python3 -B -m unittest tests.i18n.test_git_evidence_reader tests.i18n.test_production_review_v2_lite_queue.QueueTests.test_progress_cli_all_public_queue_reports tests.i18n.test_production_review_v2_lite_progress`，
12 tests 通过，日志为 `reader-compatibility.log`。报告记录这次有界归因后重新定稿，再执行包含 build
的完整门禁；最新实际结果仍由 `full-gates.log` 和 `post-gate-verification.json` 指向。

## 边界

只写 SPEC 的 8 个允许路径及 ignored `.artifacts`。没有改写历史 evidence、译文、术语、
`.ai`，没有持久化第二套完成状态。未创建 children，未 stage/commit/push。
本次只实现 P4 报告；采样、路由策略、P5/P6、独立复审与任务终态由宿主处理。
新增聚合循环只遍历有限 validated source rows、有限 migration chain 和当前 eligible 集合，
每步推进到下一条或下一条边，遇到不可映射链接即停止，不引入重试或无界扫描。
