# P5 实现结果：职责拆分、契约身份校验与文档去重

本报告覆盖 `tooling-optimization-p5-20260905` 的全部五项实现要求，基线为
`0913d0b98f6f038d1357f8a325a196be96427f97`。Part A 完成 CLI 七族、测试职责拆分和旧模块调查；
用户批准 TEST-BOUNDARY 后，Part B 完成条款身份检查、真实行为映射及文档去重。
独立复审、任务 closure、commit/push 仍由宿主负责，本报告不宣布 DONE_VERIFIED。

下列“实际实现”至“Part A 实施记录”为 A 当时的验证结果与中间回执；B 的明确替换和最终
组合内容验证在后续章节。修复轮 1 的最终实际结果以
`.artifacts/i18n/tooling-optimization-p5-fix-1/latest-receipt.json` 及其指向的原始门禁日志为准；
报告在该轮最终完整门禁之前完成，不预写尚未执行的通过结论，B 回执仅绑定修复前内容。

## 实际实现

- `tools/i18nlib/cli.py` 仅组合七族注册、解析参数、调用注册的 handler 和处理公共错误。
  每族的 `register` 用正常 `set_defaults(handler=dispatch)` 绑定自己的路由；quality 等族内的子命令分派随该族迁移，未留在顶层。
- 新增 `cli_doctor`、`cli_localization`、`cli_identity`、`cli_lint`、`cli_review`、`cli_quality`、`cli_production`。
  `cli_common` 承载 manifest、JSON、组件选择及 DLC 环境辅助函数。
  原有 71 个非入口处理函数和辅助函数的 AST 函数体保持不变；`main()` 和真实 CLI 入口保持有效。
- 真正调用辅助函数的测试已改用定义模块：build→localization、baseline／identity→identity、增量 lint→lint、quality→quality、production→production、组件选择→common。
  `affected_rule_ids` 保留在 `cli_lint`，其活跃调用者是同模块的增量规则处理函数；没有为私有 patch 路径建立兼容 facade。
- 删除原大型 `tests/i18n/test_toolchain.py`，迁至下面 20 个职责模块；无测试删除、替代或新增重复发现。
  `toolchain_fixtures.py` 仅共享 fixture 生命周期和两个构造函数，不包含或导入 TestCase 类。
  TestFixtureIsolation 的子进程改为导入真实 fixture 所有者。
  Pi 质量测试借用 QualityValidationTests fixture 的既有关系改为通过模块引用，未把 TestCase 类导入第二个测试模块。
- `test_groups.json` 仍为唯一注册表：原 toolchain 成员替换为拆分模块，其他原直接成员、组、间接加载和排除语义不变。
  `docs/agent-workflow.md` 只把五步门禁中的旧测试入口改为 `python3 -B tools/test_groups.py --group toolchain`。

## 逐族门禁

每族移动前保存实际消费者查询／结果，移动时一并完成注册、处理函数和族内路由归属，定向回归通过后才运行完整 `tools/ci-gates.sh`；每个下表回执均为 **17/17 PASS，含严格 addon 构建**。
只有前一族完整门禁成功后才移动下一族。identity 先于 lint，因为后者的基线模式依赖 identity 辅助函数。
已经门禁通过的族模块在后续各步保持字节一致。

所有 `*-hashes.json`、help、查询及定向回归日志位于被忽略的
`.artifacts/i18n/tooling-optimization-p5-implement-a/`；中间哈希只绑定该步，不冒充最终内容。

| 步骤 | 定向测试数 | 完整门禁回执 | 当步内容哈希 |
| --- | ---: | --- | --- |
| 1 doctor | 3 | `.artifacts/i18n/ci-gates/run.ps9uqald/results.json` | `01-doctor-hashes.json` |
| 2 localization | 13 | `.artifacts/i18n/ci-gates/run.f0rb52gu/results.json` | `02-localization-hashes.json` |
| 3 identity | 74 | `.artifacts/i18n/ci-gates/run.9i4wyh3o/results.json` | `03-identity-hashes.json` |
| 4 lint | 62 | `.artifacts/i18n/ci-gates/run.lnthcm5e/results.json` | `04-lint-hashes.json` |
| 5 review | 48 | `.artifacts/i18n/ci-gates/run.qyqmbdjr/results.json` | `05-review-hashes.json` |
| 6 quality | 77 | `.artifacts/i18n/ci-gates/run.7rjwe7yg/results.json` | `06-quality-hashes.json` |
| 7 production | 144 | `.artifacts/i18n/ci-gates/run.nch_pue0/results.json` | `07-production-hashes.json` |

首族移动前原始查询：

```sh
rg -n 'i18nlib.cli|from .*cli import|cli\.' tests tools --glob '*.py'
```

结果为 `cli-consumers-baseline.txt`；后续各族的 `<NN>-<family>-consumers.txt` 内同时记录原命令及当步输出：

```sh
rg -n 'i18nlib.cli|from .*cli import|cli\.|affected_rule_ids' tools tests docs --glob '*.py' --glob '*.md'
```

## 测试与兼容性核对

- 编辑前冻结全部 **92 个 argparse 帮助节点**，逐步保存原始帮助文本，并比较命令／选项集合、参数默认值及帮助说明，均相等。
  顶级命令展示次序因族注册改变；没有使用 argparse 内部排序修补。
  `handler` 是注册附带的内部路由默认值，不是新增公开选项。
- 原 **53 类／468 个测试方法** 完整保留并各加载一次；toolchain 组连同原有注册表／门禁测试共 **484 项**。
  原契约测试类的完整源码原样迁入 contracts 模块，没有修改正文契约断言。
- `final-comparison.json` 记录类／方法、帮助语义、原 CLI 函数体、SCOPE、注册表及 **700 份 evidence 的路径集合与 SHA-256 全等**核对。
  `baseline-*.json` 为编辑前基线，`final-*.json` 为最终内容；`test-responsibility-map.json` 保留逐类映射。
- 拆分后的 `python3 -B tools/test_groups.py --group toolchain`：484 项 PASS；注册表检查 PASS；
  `python3 -B tools/paseo_contract_check.py`：10 份活跃文档检查 PASS；`git diff --check` PASS。
- 最终报告先写入，再生成 `final-hashes.json` 并运行最终完整门禁，期间不编辑任务内容。
  最终门禁真实结果见 `final-gates.log` 指向的 `ci-gates/run.*/results.json`，并由 `final-receipt.json` 保存索引。
  本报告不预写尚未运行的最终门禁结果；以该回执的 complete／success／17 项退出码及最终交付说明为准。

| 职责模块（tests/i18n/） | 类数 | 方法数 | 原测试类 |
| --- | ---: | ---: | --- |
| `test_toolchain_git_config.py` | 3 | 10 | TestFixtureIsolationTests, GitRepositoryValidationTests, ManifestTests |
| `test_toolchain_doctor.py` | 1 | 3 | DoctorTests |
| `test_toolchain_static_audit.py` | 2 | 14 | StaticAuditTests, DomainAnnotationTests |
| `test_toolchain_dynamic_audit.py` | 1 | 18 | DynamicAuditTests |
| `test_toolchain_runtime_keys.py` | 3 | 13 | RuntimeCollisionScannerTests, RuntimeKeyClassifierTests, SemanticSignatureTests |
| `test_toolchain_review_scope.py` | 1 | 25 | ReviewScopeTests |
| `test_toolchain_review_diff.py` | 1 | 33 | ReviewDiffTests |
| `test_toolchain_cli_preflight.py` | 3 | 13 | PublishPreflightTests, CliLightweightPreflightTests, ComponentSelectionTests |
| `test_toolchain_build.py` | 5 | 31 | BuildApiComponentDeduplicationTests, BuildSemanticComparisonTests, StatusTests, AddonBuildTests, SmokeReleaseTests |
| `test_toolchain_lint.py` | 2 | 12 | FormatTests, LintCommandTests |
| `test_toolchain_locale_extract.py` | 4 | 27 | LuaLocaleTests, ProtectedExtractionTests, ExtractionNormalizationTests, MergeTests |
| `test_toolchain_terminology.py` | 1 | 9 | TerminologyTests |
| `test_toolchain_review_bundle.py` | 2 | 32 | ReviewBundleTests, TranslationReviewV2Tests |
| `test_toolchain_context_workset_proposal.py` | 3 | 19 | ContextPreflightTests, WorksetTests, ProposalTests |
| `test_toolchain_pi.py` | 7 | 54 | PiRemediationValidationTests, PiRunOptionPreflightTests, PiAgentTests, PiTmuxTests, PiQualityEvaluatorTests, PiEventStreamTests, PiPanePreviewTests |
| `test_toolchain_quality_config.py` | 3 | 29 | QualityConfigurationTests, QualityIdentityTests, QualityStructureTests |
| `test_toolchain_quality_sampling.py` | 4 | 25 | QualitySampleOptionPreflightTests, QualitySamplingTests, QualityRuntimeSemanticTests, QualityInventoryIntegrationTests |
| `test_toolchain_quality_validation.py` | 2 | 50 | QualityValidationFlagPreflightTests, QualityValidationTests |
| `test_toolchain_quality_reports.py` | 1 | 5 | QualityMetricsTests |
| `test_toolchain_contracts.py` | 4 | 46 | CiGatesScriptTests, ProjectSubagentDefinitionTests, PaseoTranslationContextReviewTests, PaseoRuntimeNeutralContractTests |

## 旧模块消费者与归档决定

逐模块执行下式，其中 MODULE 取下表模块名；不限制扩展名，以包含 `tools/pi-quality-role` 等入口。
完整实际查询与输出保存为 `legacy-consumers-final.json`，下表列可直接复查的活跃代码／测试消费者。

```sh
rg -n '\bMODULE\b' tools tests docs archive
```

| 模块 | 活跃消费者示例 | 决定 |
| --- | --- | --- |
| `pi_agent` | `tools/i18nlib/pi_tmux.py:39`、`tools/i18nlib/pi_review.py:17` | 保留 |
| `pi_facts_study` | `tools/pi-quality-facts-study:13`、`tests/i18n/test_facts_study.py:33` | 保留 |
| `pi_file_review` | `tools/i18nlib/pi_tmux.py:55`、`tools/i18nlib/pi_quality.py:21` | 保留 |
| `pi_quality` | `tools/pi-quality-evaluator:13`、`tools/i18nlib/cli_quality.py:26` | 保留 |
| `pi_remediate` | `tools/i18nlib/pi_tmux.py:47`、`tools/pi-remediate:14` | 保留 |
| `pi_review` | `tools/i18nlib/pi_tmux.py:64`、`tools/i18nlib/pi_quality.py:22` | 保留 |
| `pi_roles` | `tools/pi-quality-role:12` | 保留 |
| `pi_run_options` | `tools/i18nlib/pi_tmux.py:54`、`tools/i18nlib/pi_agent.py:18` | 保留 |
| `pi_tmux` | `tools/pi-tmux:14`、`tests/i18n/test_toolchain_pi.py:43` | 保留 |
| `quality` | `tools/i18nlib/pi_quality.py:25`、`tools/i18nlib/cli_quality.py:27` | 保留 |
| `quality_v2` | `tools/i18nlib/pi_quality.py:34`、`tools/i18nlib/quality_v3.py:19` | 保留 |
| `quality_v3` | `tools/i18nlib/pi_quality.py:47`、`tools/i18nlib/cli_quality.py:55` | 保留 |
| `quality_claims` | `tools/i18nlib/quality_v2.py:740`、`tools/i18nlib/quality_v2.py:746` | 保留 |
| `quality_contracts` | `tools/i18nlib/facts_curation.py:56`、`tools/i18nlib/dataset_registry.py:16` | 保留 |

归档集合为空。`pi_quality` 的 CLI／质量消费者和 `pi_roles` 的无扩展名入口仍真实存在；不删除消费者测试制造“死代码”。
旧项目审核路由已归档的政策不等于现有质量工具模块无消费者。

## Part A 实施记录

- 第一族初次提取把同一源代码行中的两条 argparse 语句重复复制，产生选项冲突；提取器已按 AST 语句边界修正，族级 dispatch 同步落实，随后全部重新验证通过。
  初次失败回执保留在 `.artifacts/i18n/ci-gates/run.07hxyozs/results.json`。
  当次帮助捕获中断，未生成独立逐文件哈希快照；该失败运行只有门禁自带的 worktree binding，不计入上表通过回执。
- localization 定向回归曾揭示跨族预检的 `load_policy` mock 所有者不正确；已指向真实 lint 所有者，未增加生产代码兼容属性，13 项重跑通过。
- production 的两段子进程测试最初仍从旧模块导入；已改为真实 `tools.i18nlib.cli_production` 所有者，并重跑完整定向套件，未改变输出／错误码断言。
- 测试拆分首跑缺少 Pi 测试的两个原有 fake 脚本常量；已逐字节迁入 Pi 职责模块，保留原测试断言后重跑整个 toolchain 组。
- 其他历史计划／阶段报告中出现旧 `test_toolchain.py` 路径；本轮按明确边界只更新活跃五步门禁入口，不改历史文档或扩大到规范去重。
- A 阶段未实施的契约、覆盖矩阵和文档部分已在 B 阶段完成，见下文；宿主独立复审、.ai 记录和 Git 操作仍不属于 EXECUTOR 交付。

## Part B 实际实现与边界

- `tools/paseo_contract_check.py` 删除全部正文 marker 副本与固定运行时词串扫描，只验证
  明确声明区的 16 个唯一 clause ID、角色引用集合／authority link，以及四份 live 契约版本。
  原来后文两个单独标题对应的 ID 已加入声明表，专属正文仍保留。历史提及不能补足 live 声明。
  CLI 继续以 0 表示通过、1 表示契约检查失败，并保留 PASS/FAIL 输出；缺文件／坏 UTF-8
  也以 1 报错，不发生 traceback。未更改 ai_state_check、bounded runner 或任何专属 validator 行为。
- [条款覆盖表](../../docs/paseo-clause-test-coverage.md) 列出 11 条 executable/partial 条款的真实正反
  selector、实际断言与人工余项，明确 5 条宿主流程缺口。28 项选定的真实测试已运行通过；
  mapping 不是“测试存在”的替代证明，已读取函数断言并保存执行日志。
- Part A 的 53 类／468 方法原始清单仍作为基线。B 显式替换 contracts 中 36 项正文镜像／
  本地仿真测试，新增 7 项 identity mutation：432 个原方法保留，当前 54 类／439 方法，
  toolchain 组含既有注册表／CI tests 共 455 项，无重复发现。另一文件的两项 anchor 正文镜像
  替换为两项正文容忍／live 版本测试，原 42 项真实 anchor 行为测试全部保留。
  每一个旧 selector 及替代理由均记录在覆盖表，不删除普通工具测试。
- 文档去重将操作命令留在 workflow／README，schema、身份和状态语义留在对应契约；
  未改 AGENTS、角色 prompt、译文、术语或 700 份 evidence，未提前实施 P6 doctor 扫描改动。
  下表逐项给出被移除正文的权威去向与保留内容；完整逐字 before 片段保存在
  `doc-dedup-map.json` 便于复核，人工判断的权威交付是本表与覆盖表。

## 文档去重映射

| 原文位置／重复主题 | 权威去向 | 保留的独有约束 |
| --- | --- | --- |
| D01 `docs/paseo-orchestration-v2-contract.md`：Before selecting any reviewer profile, ORCHESTRATOR must freeze the implementation candidate, r | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D02 `docs/paseo-orchestration-v2-contract.md`：The persisted candidate_author_agent_id must point to the latest accepted output that was produ | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D03 `docs/paseo-orchestration-v2-contract.md`：When the candidate changes, ORCHESTRATOR must recompute candidate_author_agent_id before the ne | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D04 `docs/paseo-orchestration-v2-contract.md`：candidate_author_agent_id is null for review-only work and for an implement candidate that pred | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D05 `docs/paseo-orchestration-v2-contract.md`：The immutable per-dispatch author pointer is copied to every candidate-bound reviewer dispatch  | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D06 `docs/paseo-orchestration-v2-contract.md`：not_applicable is used for review-only work, implement candidates predating any managed EXECUTO | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D07 `docs/paseo-orchestration-v2-contract.md`：Before consuming the transport's explicit provider, ORCHESTRATOR must query live Paseo metadata | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D08 `docs/paseo-orchestration-v2-contract.md`：The same-provider budget exception is allowed only when the author-provider resolution is verif | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D09 `docs/paseo-orchestration-v2-contract.md`：If the author record is missing, any of the author agent id, workspace, task/role labels, paren | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D10 `docs/paseo-orchestration-v2-contract.md`：At creation of the second reviewer, ORCHESTRATOR must obtain both live exact model identities,  | docs/paseo-orchestration-v2-contract.md §一.15–18 / §五 运行时 profile 路由 | 保留冻结事件、当前 lineage 作者、null、不可变副本、lookup 身份、verified 预算例外及精确 model proof。 |
| D11 `docs/paseo-orchestration-v2-contract.md`：Only the corresponding reviewer entry in STATE child_dispatches records author_provider_resolut | docs/paseo-orchestration-v2-contract.md §一.16–17 | 记录时点与恢复时点不丢失。 |
| D12 `docs/paseo-orchestration-v2-contract.md`：After ambiguous-create reconciliation or recovery, ORCHESTRATOR must re-resolve author_provider | docs/paseo-orchestration-v2-contract.md §一.17 | 暂缺 enum 不强制 WAIT_USER。 |
| D13 `docs/paseo-orchestration-v2-contract.md`：When paired reviewer exact model identities collide, archive the second child before creating a | docs/paseo-orchestration-v2-contract.md §一.18 | 保留碰撞先归档、一次重试、完整成对 proof、身份不可推断及离线 completion neutral。 |
| D14 `docs/paseo-orchestration-v2-contract.md`：If either exact model identity remains unavailable after one retry, enter WAIT_USER and do no | docs/paseo-orchestration-v2-contract.md §一.18 | 保留碰撞先归档、一次重试、完整成对 proof、身份不可推断及离线 completion neutral。 |
| D15 `docs/paseo-orchestration-v2-contract.md`：If a second reviewer exists or was unambiguously adopted but either model_diversity_verified  | docs/paseo-orchestration-v2-contract.md §一.18 | 保留碰撞先归档、一次重试、完整成对 proof、身份不可推断及离线 completion neutral。 |
| D16 `docs/paseo-orchestration-v2-contract.md`：Operational author_provider_resolution and model_diversity_verified fields are excluded from ru | docs/paseo-orchestration-v2-contract.md §一.18 | 保留碰撞先归档、一次重试、完整成对 proof、身份不可推断及离线 completion neutral。 |
| D17 `docs/paseo-orchestration-v2-contract.md`：list_profiles 是每次 child 调度前的实时发现入口；profile notes 和当前能力共同决定 | docs/paseo-orchestration-v2-contract.md §一.13–19 | 不同 provider 优先与无法组成不同 model 的 WAIT_USER 显式保留。 |
| D18 `docs/paseo-orchestration-v2-contract.md`：## 七、托管 child 生命周期与即时归档 | docs/paseo-orchestration-v2-contract.md §七 | 从 workflow 移入通知、两轮预算和精确 runtime cleanup 顺序。 |
| D19 `docs/agent-workflow.md`：传输状态面可能过期，单一 status 不足以判定终态。create_agent 的 | docs/paseo-orchestration-v2-contract.md §七 | 原四步顺序与两轮预算全部移入 canonical 生命周期段。 |
| D20 `docs/agent-workflow.md`：若待检文件是 untracked，先以 git add -N -- <path> 让其以 intent-to-add 形式进入工作树 diff，再运行 git diff --check | docs/agent-workflow.md §审核、修复与停止 | 保留 untracked whitespace 覆盖，避免 reviewer 更改 index。 |
| D21 `docs/agent-workflow.md`：仅当 schema_version >= 4、mode=implement 且含 translation_contextual_v1 时启用：首轮 | v1 §三 full/closure；orchestration §一.4；AGENTS 收敛下限 | 保留操作顺序；完整依赖词表、parent、不完整回退、final失败后修复和最新terminal由v1及编排契约承载。 |
| D22 `docs/agent-workflow.md`：并行只在 [paseo-orchestration-v2-contract.md](../../docs/paseo-orchestration-v2-contract.md) 的受管 wave | docs/paseo-orchestration-v2-contract.md §五 受管 Phase 1 wave | 四组真实命令、workspace-root 参数和执行时序留在 workflow；初次去重遗漏 verify/apply 的 INTEGRATING 与首次 apply 固定干净基线前置条件，修复轮 1 已补回契约，并保留运行时路径与合法 ignored 产物例外。 |
| D23 `docs/paseo-orchestration-v2-contract.md`：规范门禁命令为： | docs/agent-workflow.md §受管 Phase 1 wave | 命令完整保留在操作手册，schema/参数语义仍在契约。 |
| D24 `i18n/README.md`：tools/i18n review 与 tools/review_diff.py 只生成离线 bundle／index／diff | i18n/README.md review / pi-review 条目；orchestration §十一 | 保留实际 tombstone 副作用与 exit 行为，下方原说明不变；doctor P6 前语义不变。 |
| D25 `docs/paseo-translation-context-review-v2-contract.md`：全部 reviewer 只读；输出由 ORCHESTRATOR 原样持久化、验证、裁决并在 child 终态后归档。 | docs/paseo-orchestration-v2-contract.md §七/八/十一；v2 §五 | 保留精确输入白名单、源码不足标记、raw bytes 与 v2 identity。 |
| D26 `docs/paseo-translation-context-review-v1-contract.md`：创建、传输和查询错误按一般基础设施规则重试一次。若需要新会话，必须保持相同 role、 | docs/paseo-orchestration-v2-contract.md §六–八；v1 §二 | 保留专属 dispatch ID 与禁止混用旧输出；只读快照范围完整保留。 |
| D27 `docs/paseo-translation-surface-screen-v1-contract.md`：REVIEWER 只可读其精确 input_path、其中明确引用的内容和第六节。ORCHESTRATOR 负责裁决： | docs/paseo-orchestration-v2-contract.md §八/十一；surface §五 | 保留第五节精确输入边界和第七节 surface OK/ISSUE、R-low、ledger 的全部专属语义。 |
| D28 `i18n/README.md`：当前工具以 tome4-chinese-translation 为唯一译文源。manifest 固定的 engine、addon | i18n/README.md §运行时配置与许可证说明 | 唯一译文源、Lua代理、默认不提取DLC和artifact输出保留；manifest固定范围在运行时配置。 |

§一中路由的中英双写已合并；恢复时点、暂缺 enum 不触发 WAIT_USER、成对 proof、collision
先归档、一次重试后 model 仍未知必须 WAIT_USER，以及 operational 字段不参与离线 closure
均保留。通用生命周期从 workflow 移入契约时，显式保留 notifyOnFinish 非成功信号、两轮
非紧密 live requery 预算、精确 process cleanup 与 cancel 的区别。wave 的完整 schema、
workspace root map、no-change 范围、唯一 integration caller、最新 terminal 和 publication
恢复判据仍在编排契约；workflow 保留全部可执行命令及顺序。

## B 验证与最终冻结方式

所有可重生成回执位于 `.artifacts/i18n/tooling-optimization-p5-implement-b/`：

| 检查 | 实际结果／回执 |
| --- | --- |
| 首次 doctor | PASS，`doctor.log` |
| 条款真实行为 | 28 tests PASS，`behavior-tests.log`；完整 selector 与断言见 `behavior-selectors.json`、`behavior-assertions.txt` |
| 身份 mutation + anchor | 61 tests PASS，`mutations-anchor.log`；含全部 16 ID 删除、四版本缺失／损坏／不符／重复／历史冒充、角色引用错误与正文变更容忍 |
| 完整 toolchain | 455 tests PASS，`toolchain.log`；最终门禁会在最终字节上重新运行 |
| 完整 contract-suite | PASS，`contract-suite.log`；最终门禁会在最终字节上重新运行 |
| 注册表 | `python3 -B tools/test_groups.py --check` PASS；未增加第二套测试注册入口 |
| 全部 92 帮助节点 | B 重新抓取原始 help，命令／选项集合、默认值与帮助说明与 A 前基线相等；仅 A 记录过的顶级展示顺序改变 |
| 内容保护 | `comparison.json`：700 evidence 路径与哈希全等；全部 Lua、terminology、AGENTS 和角色字节不变；scope PASS |
| 文档／链接／空白 | `doc-links.json` 检查具体本地 Markdown 文件与 heading fragment；`git diff --check` 及 untracked 的只读 no-index 空白检查通过 |
| 最终完整门禁 | 报告先冻结，再运行真实 `tools/ci-gates.sh`（含严格核心 addon 构建）；`final-receipt.json` 绑定 `final-hashes.json`、完整日志与 gate results，期间不写任务内容 |

检查器对有限文档集合使用有限行匹配和集合／计数校验，无外部递归或无界扫描循环；
声明／版本 mutation 套件还以 5 秒子进程 timeout 运行有限输入的终止探针，回执为
`bounded-probe.log`。这不修改其他扫描器，也不增加常驻监督器。

## 修复轮 1：P5-NR-01

宿主 confirmed finding 指出 D22 的“逐项机器不变量均已有 canonical 对应”断言不成立。
对照基线 workflow 229–233 行及 `tools/wave_review.py:1666–1715`，本轮在契约的
“受管 Phase 1 wave”补回合法 `INTEGRATING` WAVE 和首次 apply 的 HEAD／index／tracked
worktree 固定基线条件，以及无任务内容 dirty／untracked 要求；按源码保留四类运行时路径
例外和 `--ignored=no` 语义。既有 lane completion／dispatch／envelope／归档条款不重复。

本轮仅修改契约与本报告；其余 44 个既有候选路径（含一个删除项）保持字节／缺失状态一致。
文档完成后执行契约、具体本地 Markdown 链接与 whitespace 检查，再冻结全部 46 个候选路径，
运行 `tools/ci-gates.sh` 的严格 17 项门禁（含 build），不重跑历史七族中间门禁。
稳定回执 `.artifacts/i18n/tooling-optimization-p5-fix-1/latest-receipt.json` 记录实际测试数、
门禁日志和结果哈希、门禁前后候选哈希全等及其他候选保护结果；门禁期间不写任务内容，
门禁后只生成 ignored 回执。旧 B 回执不再作为修复后内容的最终绑定。

## B 有界偏差与未完成的宿主工作

- 新增的只读 untracked 空白检查揭示 A 的八个 CLI family/common 模块末尾各多一个空行。
  为使新文件的空白门禁真实成立，仅删除每文件最后一个 LF；`part-a-whitespace-dependency.json`
  逐项记录。验证把一个 LF 加回后 SHA-256 必须等于 A 接受版本，因而不是 handler 或注册行为改动。
  其他 A 内容字节保留（除本任务明确允许的 workflow、contracts tests 和结果报告）。
  七族中间完整门禁不重复，最终组合内容重新跑完整门禁。
- 无新增编排引擎、live author/model completion predicate、child 或范围扩张；未写 `.ai`，
  未 stage/commit/push。五项自动化缺口是用户批准的边界，不冒充实现缺陷已自动验证。
- 独立正常／交叉复审、最终复审对、宿主 STATE/DONE_VERIFIED 和 Git 发布操作待宿主完成。
