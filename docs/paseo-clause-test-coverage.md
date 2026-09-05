# Paseo 条款行为覆盖边界（P5）

用户已批准 TEST-BOUNDARY：检查器仅证明 canonical clause 声明、引用和四个 live 版本一致；
正文变更由独立审核判断，不复制成字符串门禁。以下 11 条均为可执行或部分可执行；
“通过／违反”列是可直接传给 `python3 -B -m unittest` 的真实 selector。
同一 selector 出现两次表示该测试本身同时运行通过和违反分支。未宣称整条宿主流程已自动化。

| 条款 | 通过 selector | 违反 selector | 实际断言与人工余项 |
| --- | --- | --- | --- |
| `P2-SINGLE-WRITER` | `tests.i18n.test_check_allowed_files.MainTests.test_in_scope_paths_pass` | `tests.i18n.test_check_allowed_files.MainTests.test_out_of_scope_path_fails` | check_allowed_files.main 返回 0/1 验证允许文件面；不识别实时进程是否唯一 writer，宿主仍核验写入者。 |
| `P2-DIRECT-LINEAGE` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_v2_fixture_and_fail_closed_state_matrix` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_v2_fixture_and_fail_closed_state_matrix` | ai_state_check 对正常 v2 DONE 返回 DONE_VERIFIED；missing_parent_agent_id/missing_workspace_id 子用例失败。校验持久化身份，不证明 Paseo live 创建来源。 |
| `P2-RUNTIME-OBSERVATION` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_runtime_observation_is_optional_and_completion_neutral` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_runtime_observation_exact_schema_and_placement` | 真实 STATE checker 验证可选审计字段不改变 DONE/STOP；错误 schema、presence、NaN、放置层级均拒绝。首次 live 原样捕获仍由宿主执行。 |
| `P2-CANDIDATE-FREEZE` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_evidence_f_is_candidate_bound_and_on_disk_sidecar_is_checked` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_done_predicate_fails_closed_for_each_load_bearing_relationship` | 正常候选绑定通过，sidecar/changed_diff 漂移拒绝；工具重算 frozen bytes，宿主保证冻结时完整枚举任务路径。 |
| `P2-REVIEW-INDEPENDENCE` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_evidence_f_is_candidate_bound_and_on_disk_sidecar_is_checked` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_evidence_e3_reviewer_must_not_be_orchestrator` | evidence review 正常不同 agent 通过；reviewer=orchestrator 返回 1 且 agent_id must differ。仅身份分离可执行；不读取彼此 findings 的 live 隔离仍人工。 |
| `P2-HARVEST-ARCHIVE` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_review_only_does_not_require_final_validation_and_stop_is_narrow` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_done_predicate_fails_closed_for_each_load_bearing_relationship` | STOP 已归档可关闭，active/stopping/双 lifecycle 拒绝；DONE not_archived 子用例拒绝。归档调用前 harvest、原始 bytes 核验和预算持久化的真实顺序仍人工。 |
| `P2-FRESH-RETRY` | `tests.i18n.test_ai_state_check.SurfaceScreenContractTests.test_surface_retry_history_failed_then_success_is_done_verified` | `tests.i18n.test_ai_state_check.SurfaceScreenContractTests.test_surface_retry_identity_freshness_predicate` | surface 失败→fresh 成功历史可 DONE；真实 _surface_retry_history_valid 拒绝复用 dispatch/agent/group identity。实际 archive 后再 create 的时序仍人工。 |
| `P2-STOP-CLOSED` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_review_only_does_not_require_final_validation_and_stop_is_narrow` | `tests.i18n.test_ai_state_check.SurfaceScreenContractTests.test_surface_stop_rejects_dispatched_screen` | 普通已归档 STOP 可验证，已派发 surface 不得借 STOP 关闭；WAIT_USER 的现场判断、重试预算与取消流程仍人工。 |
| `P2-TRANSLATION-CONVERGENCE` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_schema4_translation_full_closure_final_full_can_close` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_schema4_translation_closure_cannot_finish` | 真实 STATE full→closure→final full 可关闭；closure 不能 final。补充 key/source/parent、latest parent、max_cycles 用例；依赖闭包完整性与缺陷分档由宿主裁决。 |
| `P2-TRANSLATION-CONTEXT-V2` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_v2_fixture_and_fail_closed_state_matrix` | `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_v2_well_formed_closure_with_wrong_parent_is_rejected` | v2 正常四 lane/final 通过，混用契约、缺 lane、raw 漂移及错误 parent coverage 拒绝；源码语义与主观审阅投入仍需独立审核。 |
| `P2-TRANSLATION-SURFACE-V1` | `tests.i18n.test_surface_screen_manifest.SurfaceManifestTests.test_build_cli_zero_records_no_dispatch_artifact` | `tests.i18n.test_ai_state_check.SurfaceScreenContractTests.test_surface_rejects_borrowed_implement_convergence` | 真实 manifest CLI n=0 写唯一 ZERO artifact 且重跑幂等；任何 dispatch 输入非零退出；surface checker 拒绝借 implement 收敛。OK/ISSUE 的实质裁决与深审策略仍人工。 |

## 五项宿主流程自动化缺口

- `P2-LIVE-ROUTING`：实时 list_profiles、provider 可用性与预算选择；无仓库编排执行引擎。
- `P2-AUTHOR-PROVENANCE`：冻结时作者归属、含 archived 的 live lookup、一次重试及 unavailable/not_applicable；bounded runner author schema 不是 live provenance 证明。
- `P2-MODEL-DIVERSITY`：两名 live 精确 model 不同及成对 proof、碰撞归档 fresh retry；不把这些字段加入离线 closure。
- `P2-RECOVERY`：歧义创建过滤、完整列表、0/1/多匹配采用、live 状态 reconciliation；本地 frozen byte 恢复测试不能替代宿主流程。
- `P2-READ-ONLY`：live reviewer/scout 禁写、禁读其他 findings；文件快照由宿主取证，不虚构 mock orchestrator。

## 补充真实行为测试

- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_schema4_translation_closure_key_source_and_parent_drift_fail`
- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_schema4_translation_closure_parent_must_be_latest_earlier_full`
- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_schema4_translation_max_cycles_default_and_authorization`
- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_binding_checks_record_dispatch_envelope_and_payload`
- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_contextual_v2_dispatch_prompt_is_gated_for_all_records`
- `tests.i18n.test_ai_state_check.StateCheckerFixtureTests.test_nul_candidate_vector_is_exact_and_not_the_obsolete_separator`
- `tests.test_executor_runner.TestBoundedExecutor.test_executor_candidate_author_remains_accepted`
- `tests.test_executor_runner.TestBoundedExecutor.test_invalid_candidate_author_roles_fail_before_target_or_ledger_write`
- `tests.test_executor_runner.TestBoundedExecutor.test_archive_receipts_are_exact_typed_trusted_host_facts`
- `tests.i18n.test_contextual_anchor_preflight.ContextualAnchorPreflightTests.test_cults_b3_declared_chapter_passes`
- `tests.i18n.test_contextual_anchor_preflight.ContextualAnchorPreflightTests.test_cults_b3_wrong_chapter_regression_fails`

以上 selector 的真实函数断言已逐项读取；执行清单和 stdout/stderr 回执保存在
`.artifacts/i18n/tooling-optimization-p5-implement-b/behavior-selectors.json`、`behavior-tests.log`。
测试中的 fixture 和 mock 只给现有真实 validator 输入，不实现新编排引擎。

## 声明／版本 mutation

`tests.i18n.test_toolchain_contracts.PaseoClauseIdentityTests` 在临时完整 fixture 副本中验证：
16 个 canonical table 声明逐一删除（正文引用保留）全部失败；重复、未知、坏语法声明失败；
所有活跃文档仅改正文标点／措辞通过；四契约 live 版本缺失、格式损坏、版本不符、重复或
只有历史声明均失败；角色缺引用、未知引用、缺 authority link 和活跃文件缺失／坏 UTF-8 失败。
`ContextualAnchorContractGuardTests` 补充 anchor 标点容忍与 v1 历史版本不能替代 live 声明。
所有 mutation 不写仓库契约或角色文件。

## 有意替换的原测试

Part A 原样保留 53 类／468 方法；以下为 Part B 显式替换，并非普通工具测试删除。
原 contracts 模块其他 archive/fixture、候选向量和实际 prompt 示例检查保留。
所有原 anchor preflight 行为测试保留。以下旧 selector 若只验证文档字面，其替代不宣称
原本存在真实运行时执行保证；对应宿主部分明确属于上表人工余项或五项缺口。

| 原 selector | 替代与原因 |
| --- | --- |
| `tests.i18n.test_toolchain_contracts.PaseoRuntimeNeutralContractTests.test_runtime_neutral_versions_are_current` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_contextual_result_is_fail_closed_and_read_only` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_contextual_state_and_recovery_binding` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_contextual_fixed_source_identity_is_typed_and_mechanism_bound` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_contextual_contract_is_runtime_neutral` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_active_orchestrator_role_drives_translation_convergence` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.PaseoTranslationContextReviewTests.test_contextual_role_and_purpose_are_the_active_route` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_dispatch_history_and_review_records_retain_agent_identity` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_child_lifecycle_has_equivalent_cli_and_mcp_paths` | HARVEST-ARCHIVE、FRESH-RETRY、STOP-CLOSED 真实正反测试；live 调用时序仍人工。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_stop_transitions_require_archive_confirmation` | HARVEST-ARCHIVE、FRESH-RETRY、STOP-CLOSED 真实正反测试；live 调用时序仍人工。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_fallback_requires_no_children_or_confirmed_archives` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_archive_retry_budget_is_durable_and_contextual_retry_is_fresh` | HARVEST-ARCHIVE、FRESH-RETRY、STOP-CLOSED 真实正反测试；live 调用时序仍人工。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_recovery_separates_ambiguous_create_reconciliation_and_active_resume` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_child_lifecycle_ordering_and_archive_pending_recovery` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_completed_children_are_archived_across_active_consumers` | HARVEST-ARCHIVE、FRESH-RETRY、STOP-CLOSED 真实正反测试；live 调用时序仍人工。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_role_permissions_and_fresh_replacement_are_preserved` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_recovery_is_filtered_by_role_before_cardinality` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_paseo_transport_and_agent_scoped_creation_are_documented` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_paseo_roles_require_parent_lineage` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_runtime_route_identity_is_excluded_from_state_and_review_identity` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_fallback_is_fresh_and_preserves_bindings` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_provenance_markers_are_self_contained` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_runtime_observation_clauses_are_contract_owned_and_guarded` | RUNTIME-OBSERVATION exact-schema/placement 与 completion-neutral 测试。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_provenance_complete_clauses_make_guard_fail_closed` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_provenance_guard_markers_are_limited_to_normative_targets` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_reviewer_routing_provenance_is_recoverable_and_fail_closed` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_author_provider_avoidance_and_cross_review_model_deduplication` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_runtime_profiles_are_discovered_and_provider_neutral` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_active_route_docs_do_not_pin_runtime_identity` | CANDIDATE-FREEZE、DIRECT-LINEAGE、TRANSLATION-CONVERGENCE、CONTEXT-V2 的真实 STATE/候选测试；本地 regex 仿真不作为行为证明。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_complete_availability_and_budget_clauses_are_role_guarded` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_scout_output_markers_ignore_cjk_reflow_but_reject_clause_deletion` | 声明/角色引用 mutation；LIVE-ROUTING、AUTHOR-PROVENANCE、MODEL-DIVERSITY、RECOVERY、READ-ONLY 人工缺口；原测试仅检查正文。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_role_marker_matching_is_whitespace_normalized` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_role_prompts_resolve_clause_semantics_and_guard_exact_outputs` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_migrated_markers_stay_out_of_agents_with_exact_checker_owners` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_contract_guard_covers_canonical_persisted_role_markers` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_toolchain_contracts.ProjectSubagentDefinitionTests.test_active_roles_are_role_and_purpose_bound` | PaseoClauseIdentityTests 声明/版本/引用 mutation；输出 schema 由现有 contextual result/STATE 完整套件验证，宿主权限按 READ-ONLY 缺口记录。 |
| `tests.i18n.test_contextual_anchor_preflight.ContextualAnchorContractGuardTests.test_anchor_contract_clauses_are_complete_and_unique` | ContextualAnchorContractGuardTests 两项替代及 ContextualAnchorPreflightTests 真实正反输入；旧标点镜像不属于身份。 |
| `tests.i18n.test_contextual_anchor_preflight.ContextualAnchorContractGuardTests.test_deleting_or_mutating_each_anchor_clause_fails_the_guard` | ContextualAnchorContractGuardTests 两项替代及 ContextualAnchorPreflightTests 真实正反输入；旧标点镜像不属于身份。 |
