# P1 门禁测试覆盖实现与验证

任务：`tooling-optimization-p1-20260905`。EXECUTOR 实现记录，2026-09-05。
基线：`67589f1f6f449b6fc143bf8b820987b25b8faeef`，初始工作树干净。

## 实现

- `tests/i18n/test_groups.json` 是唯一模块分组清单，保留原来的 5 个分组与顺序。
  当前共 35 个直接模块、2 个间接模块，`excluded` 为空；覆盖 `tests/` 下全部 37 个 `test_*.py`。
- `tools/test_groups.py --check` 递归检查注册完整性，拒绝缺失文件、重复登记、非法路径、
  非法结构、重复 JSON 键和缺少原因的排除项。间接登记必须引用直接模块并说明原因。
- `--group` 每次先验证完整清单，再通过 unittest 原有加载机制（包括 `load_tests`）执行。
  加载失败、重复 test ID、未声明的实际模块或间接模块未实际加载均失败关闭。
  日志先列出加载计数，再通过 verbose unittest 逐项记录实际执行及结果。
- `ci-gates.sh` 用分组入口替代内联测试列表；其他检查、严格参数、失败累积和含构建的默认行为保持。
  原有 `.log` 集合及 `.out` 文件名不变，仅新增 `03-test-group-registration.out`。
- 针对性测试验证缺漏注册、补登记、配置错误、排除原因、间接加载、重复执行、测试失败和导入异常，
  并检查清单分组与 shell 消费入口一一对应，防止新增分组未被门禁执行。
  既有日志测试继续精确断言 `.log`，并新增 `.out` 精确集合和失败路径断言。
- 修改前确认两个既有文件 `tools/ci-gates.sh`、`tests/i18n/test_toolchain.py` 均为 LF；保持 LF。
  未修改扫描／解析的既有循环；新注册扫描只遍历有限 `tests/` 文件树，不重试。
  临时 fixture 的每次 CLI 探针均设置 15 秒超时。

## 基线逐项对照

从基线 `git show HEAD:tools/ci-gates.sh` 提取 5 条 unittest 命令，逐项比较有序清单：
原 31 个直接模块和 2 个间接模块全部保留，无删除、无移组；新增 4 个直接模块。

| 分组 | 模块 | 相对基线 |
|---|---|---|
| `toolchain` | `tests/i18n/test_toolchain.py` | 保留 |
| `toolchain` | `tests/i18n/test_test_groups.py` | 新增 |
| `quality-facts` | `tests/i18n/test_quality_contracts.py` | 保留 |
| `quality-facts` | `tests/i18n/test_quality_claims.py` | 保留 |
| `quality-facts` | `tests/i18n/test_dataset_registry.py` | 保留 |
| `quality-facts` | `tests/i18n/test_quality_v2.py` | 保留 |
| `quality-facts` | `tests/i18n/test_quality_v3.py` | 保留 |
| `quality-facts` | `tests/i18n/test_facts_study.py` | 保留 |
| `quality-facts` | `tests/i18n/test_facts_curation.py` | 保留 |
| `semantic-claim` | `tests/i18n/test_semantic_claims.py` | 保留 |
| `contract-suite` | `tests/i18n/identity/test_identity.py` | 保留 |
| `contract-suite` | `tests/i18n/identity/test_stability.py` | 保留 |
| `contract-suite` | `tests/i18n/identity/test_conflicts.py` | 保留 |
| `contract-suite` | `tests/i18n/fingerprint/test_fingerprint.py` | 保留 |
| `contract-suite` | `tests/i18n/fingerprint/test_findings.py` | 保留 |
| `contract-suite` | `tests/i18n/baseline/test_baseline.py` | 保留 |
| `contract-suite` | `tests/i18n/incremental/test_incremental.py` | 保留 |
| `contract-suite` | `tests/i18n/incremental/test_domains.py` | 保留 |
| `contract-suite` | `tests/i18n/qa/test_injected_defects.py` | 保留 |
| `contract-suite` | `tests/i18n/test_terminology_inventory.py` | 保留 |
| `contract-suite` | `tests/i18n/test_ai_state_check.py` | 保留 |
| `contract-suite` | `tests/i18n/test_contextual_anchor_preflight.py` | 保留 |
| `contract-suite` | `tests/i18n/test_review_evidence.py` | 保留 |
| `contract-suite` | `tests/i18n/test_wave_review.py` | 新增 |
| `contract-suite` | `tests/test_executor_runner.py` | 新增 |
| `contract-suite` | `tests/i18n/test_check_allowed_files.py` | 新增 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review_v2_lite.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review_v2_lite_migration.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review_v2_lite_queue.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review_v2_lite_batch.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_production_review_v2_lite_evidence.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_surface_screen_manifest.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_surface_screen_result_check.py` | 保留 |
| `production-shadow-surface-ledger` | `tests/i18n/test_translation_review_ledger.py` | 保留 |
| `contract-suite`（间接） | `tests/i18n/test_contextual_lane_manifest.py` | 保留，由 `test_ai_state_check.load_tests` 加载 |
| `contract-suite`（间接） | `tests/i18n/test_contextual_result_check.py` | 保留，由 `test_ai_state_check.load_tests` 加载 |

## 已执行的验证

1. `python3 -B tools/i18n doctor`：通过；保留既有 engine 工作树扫描警告。
2. `python3 -B -m unittest -q tests.i18n.test_test_groups tests.i18n.test_toolchain.CiGatesScriptTests`：
   最终 10 项通过。首轮失败经一次有界诊断定位为迁移脚本未完整捕获多行命令及导入异常退出码未统一；
   修复后通过。最后增补 shell 分组消费断言、抑制只读加载探针输出后，同一 focused 命令再次通过。
3. 漏登记正反探针：临时仓库新增空 `tests/nested/test_zzz.py`，`--check` 返回 2 并报告路径；
   加入分组后 `--check` 返回 0，`--group one` 返回 0，日志显示空模块 0 项，既有测试照常运行。
   此探针由上述 focused tests 实际执行，未向工作树添加范围外文件。
4. `tools/ci-gates.sh`（无 `--skip-build`）：退出 0，`ALL GATES PASSED`。
   日志目录：`.artifacts/i18n/ci-gates/run.wF8ogU/`（可重生成产物，已忽略）。
   本次完整门禁运行后段增补的仅是第 2 项所述测试断言／探针输出调整，已用 focused 命令验证；
   分组清单、runner 和 shell 实现未再变更。宿主最终验收门禁可在独立复审后另行记录。

| 测试分组 | 实际测试数 | 日志 | 结果 |
|---|---:|---|---|
| toolchain | 477 | `03-toolchain-unit-tests.log` | OK |
| quality-facts | 202 | `04-quality-facts-unit-tests.log` | OK |
| semantic-claim | 44 | `04-semantic-claim-unit-tests.out` | OK |
| contract-suite | 470 | `05-contract-suite-unit-tests.log` | OK |
| production-shadow-surface-ledger | 275 | `05-production-shadow-surface-ledger-tests.out` | OK |

合计 1,468 项。补齐的三个模块在 `05-contract-suite-unit-tests.log` 中分别有
`MODULE tests/i18n/test_wave_review.py: 24 tests`、
`MODULE tests/test_executor_runner.py: 40 tests`、
`MODULE tests/i18n/test_check_allowed_files.py: 7 tests`，并有逐条 `... ok` 的实际执行记录。
两个 contextual 模块分别为 7、6 项（indirect）；suite 加载的 470 个 test ID 全部唯一。
所有非测试门禁（doctor、strict lint、strict claims registry、collision scan、runtime key classification、
静态／动态术语审计、domain annotation、whitespace）均通过；
`12-core-addon-build.log` 对应 `build --profile addon --component tome --require-complete`，通过。

最终 `git diff --check` 通过；另对六个允许文件逐一执行无 index 的 whitespace 检查，
包含未跟踪的新文件，全部通过，且均保持 LF。allowed-files 两项负向测试会在 `...` 与 `ok`
之间输出预期的 `FAIL:` 诊断；逐测试块核验确认最终状态仍为 `ok`。

## 交付边界

仅修改 SPEC 列出的 6 个文件，不 stage／commit，不写编排记录，不创建子 agent。
未实施 P2–P6，无功能范围偏差。未解决的实现问题：无。
独立普通复审、senior cross review、宿主裁决、最终门禁及 `DONE_VERIFIED` 由 ORCHESTRATOR 完成；
本记录不宣称这些步骤已经通过。
