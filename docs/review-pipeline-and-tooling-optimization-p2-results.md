# P2 统一门禁执行结果（2026-09-05）

基线：`2f705018dd30cb9d696ac1ea211287bde43ec82b`。范围仅 P2；未改译文、术语、历史 evidence、角色或编排记录，未执行 P3–P6。EXECUTOR 不 stage/commit；独立复审及任务终态由宿主处理。

## 执行与覆盖

公开 `tools/ci-gates.sh` 委托 Python 入口；批次消费者直接调用同一 shared runner。
默认 full build，只有显式 `--skip-build` 才移除 build 项，授权规则不变。
旧 16 项 ID 全部保留，新增 `11-staged-whitespace`。定义及记录顺序唯一，全部日志为 `.log`。

| 稳定 ID（旧 ID 原样保留） | 实际 argv 对应命令 |
| --- | --- |
| `01-doctor` | `python3 -B tools/i18n doctor` |
| `02-strict-lint` | `python3 -B tools/i18n lint --strict` |
| `03-test-group-registration` | `python3 -B tools/test_groups.py --check` |
| `03-toolchain-unit-tests` | `python3 -B tools/test_groups.py --group toolchain` |
| `04-quality-facts-unit-tests` | `python3 -B tools/test_groups.py --group quality-facts` |
| `04-semantic-claim-unit-tests` | `python3 -B tools/test_groups.py --group semantic-claim` |
| `04-semantic-claims-strict-registry` | `python3 -B tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict` |
| `05-contract-suite-unit-tests` | `python3 -B tools/test_groups.py --group contract-suite` |
| `05-production-shadow-surface-ledger-tests` | `python3 -B tools/test_groups.py --group production-shadow-surface-ledger` |
| `06-runtime-collision-scan` | `python3 -B tools/scan_runtime_collisions.py` |
| `07-runtime-key-classification` | `python3 -B tools/classify_runtime_keys.py` |
| `08-terminology-static-audit` | `python3 -B tools/audit_static.py` |
| `09-terminology-dynamic-audit` | `python3 -B tools/audit_dynamic.py` |
| `10-domain-annotation` | `python3 -B tools/annotate_domains.py` |
| `11-worktree-whitespace` | `git diff --check` |
| `11-staged-whitespace` | `git diff --cached --check` |
| `12-core-addon-build` | `python3 -B tools/i18n build --profile addon --component tome --require-complete` |

旧封装额外的 `git diff --check`、doctor、strict lint 分别合并到 11-worktree、01、02；
`git diff --cached --check` 映射到新增 11-staged。旧 wrapper 本身不是新增成功检查。
旧独立消费者命令的覆盖为：

| 消费者 | 实际执行检查 |
| --- | --- |
| test_surface_screen_manifest.py | 05-production-shadow-surface-ledger-tests |
| test_surface_screen_result_check.py | 05-production-shadow-surface-ledger-tests |
| test_contextual_result_check.py | 05-contract-suite-unit-tests，经 test_ai_state_check.load_tests |

P1 分组一致性测试读取 shared command 定义，精确核对全部分组、consumer owner 与实际
load_tests 输出及唯一 test ID；新增测试登记到 toolchain。没有另跑或伪造消费者执行记录。

## schema 与绑定

新 gates.json exact schema 为 `{schema_version: 2, result, prospective_bytes, committed_bytes}`。
result 的 schema_version 同为 2；包含 binding、coverage、checks、起止时间、complete、success、error。
每个 check 含唯一 ID、argv、渲染命令、整数 exit_code、相对 log_path、输出 SHA-256 和起止时间。
失败继续收集其他检查，仍写独立 results.json；失败、缺项、不完整、重复/乱序 ID、错误命令、
无效类型/版本/时间/路径/摘要或覆盖关系均不能通过成功校验。正常返回码与结果成功状态一致。

候选绑定为 batch/catalog/base/policy 和完整有序 entry revision 集合及其 SHA-256。
工具记录 commit、工具版本、runner 版本和 Python 版本；batch 的工具 commit 必须等于 base。
工作树 hash 覆盖 Git index 清单及所有 tracked 和 nonignored untracked 文件的内容/模式；
配置 hash 覆盖 i18n、terminology、test_groups 配置及环境摘要（不记录环境明文）。
检查集 hash 绑定完整 ID/argv 定义。复用时重新计算实际绑定并校验日志 bytes，不能仅信自报 hash。

prepare 先执行一次；生成 prospective 后只复验这次 receipt，不再执行第二次完整门禁。
漂移拒绝复用并保留原恢复边界；新 prepare 命令重新运行，不接受已保存 receipt 作为缓存。
ignored prospective/log 文件不触发假漂移。测试仅通过进程内 execute/runner seam 注入，
生产不因缺少脚本、最小仓库或 `I18N_CI_GATES_FROM_PRODUCTION=1` 跳过必要检查。

queue 按 schema 明确分支，v2 从已验证 manifest 重建候选并验证 receipt；历史 v1 exact
validator 除缩进外逐字未变，包括旧无 occupancy fixture 的窄兼容、活跃命令/完整 CI/
consumer 约束与预算校验。未改写历史证据，也没有迁移旧 queue 格式。

## 验证

- doctor：通过（LuaJIT / Lua 5.1、LPeg 0.10.2）。
- focused：162 tests，通过；覆盖 execute failure、缺项/重复 ID/类型、候选顺序、工具/
  配置/工作树/index 漂移、日志篡改、同命令复用拒绝及恢复后 fresh run、环境 marker 负例。
- 既有 1/4/80 条公开 batch fixture prepare/finalize/rebuild/check 通过；每次 prepare
  精确断言完整 runner 一次。原预算、自引用 occupancy 四轮收敛、fail-closed、resume、
  postimage、abandon 和 publication 边界测试保留并通过。
- 15 秒 timeout 的有限输入探针：2 tests 在 0.043 秒通过。扫描先冻结有限 Git 文件名集合，
  常规文件以 1 MiB 分块读至 EOF；检查循环固定 17 项，occupancy 循环仍最多四轮。
- 完整门禁首轮：17 项成功，含 `build --profile addon --component tome --require-complete`。
- 最终 focused 复测：162 tests / 25.772 秒；最终 full gate：17 项全部通过，退出 0。
- `git diff --check`、P1 registry/coverage 检查通过；12 个修改路径均在 14 路径 allowlist 中，index 为空，HEAD 未变。

同基线 commit 完整 `queue._projection` 以 `production_review.canonical_bytes` 序列化后，
与任务保存的 BASELINE-PROJECTION.json **46,343,568 字节逐字节一致**：
`2ebefb1905db232d76c876cf7c6a44f7969a5d5b7d294ba8b040ee2f30fe4667`。
回放耗时 47.548 秒。BASELINE-EVIDENCE-HASHES.json 中 18 份历史 gates 原始 SHA-256 全部一致。
没有发布任何新的译文审核结果。

## 耗时与限度

基线旧 `_actual_gate_records` 两次封装分别 78.463、85.980 秒，合计 164.443 秒。
新统一入口首次完整运行 `tools/ci-gates.sh` 为 81.678 秒，退出 0；相对旧两次封装总和约减少
50.3%，单次耗时与旧两次的均值接近。此数字是 gate 执行测量，不是 prepare 的完整端到端
耗时；prepare 的投影、证据生成、额外 binding 校验和 occupancy 计算没有计入。

环境 Linux 7.2.2-1-cachyos / glibc 2.36、Python 3.11.2；首轮 loadavg 从
6.69/4.08/2.35 到 3.72/3.77/2.39。宿主有其他 C++ 编译负载，回放与门禁开始也有短暂重叠；
不能将单次差异解释为普适性能承诺。未做跨命令缓存、并行 gate 调度或 P3–P6 优化。

receipt 是绑定输入的检查记录，不是签名或防恶意并发修改的沙箱。历史回放不要求 ignored
日志仍存在，不能从历史 worktree/config 摘要重建当时未提交文件；实时复用才复算并核对日志。
环境摘要绑定外部运行时/源码路径配置，未对外部仓库或系统动态库做完整树快照；现有 doctor/
manifest/runtime checks 继续执行。工具版本和日志时间/schema 的变化不要求新旧 gates.json
全字节相同；不变性要求作用于已提交历史证据与同基线队列投影。

### 最终测量补记

加强 v2 tool commit/base 与版本字段校验后，重新运行 focused 和完整门禁。
最终 `tools/ci-gates.sh` **78.713 秒，退出 0，17 项通过且含严格 build**；
对全部结构化记录及 17 份日志 hash 再次校验通过。相对旧两次封装 164.443 秒总和减少
约 52.1%；相对旧单次 78.463/85.980 秒，应视为同量级而非单项检查加速。
最终 loadavg 从 0.75/2.57/2.13 到 2.40/2.63/2.18；该轮没有同时运行本任务回放。

可重生成诊断保存在 ignored `.artifacts/i18n/`：`p2-focused-final.log`、
`p2-full-final.log`、`p2-full-final-timing.json`、`p2-replay.json`；最终分步记录位于
`ci-gates/run.eudwzd_5/results.json`。本文是在最终门禁后补记测量值；补记未改变代码或测试。
没有实现计划偏差或未解决的测试失败；独立 REVIEWER/SENIOR_REVIEWER、终态核验和提交
不属于本次 EXECUTOR 派发权限，未代替宿主执行或宣称这些验收已完成。

## 交付文件与复现命令

修改/新增共 12 路径：

- tools/ci-gates.sh
- tools/ci_gates.py
- tools/i18nlib/gate_results.py
- tools/i18nlib/production_review_v2_lite_batch.py
- tools/i18nlib/production_review_v2_lite_queue.py
- tests/i18n/test_ci_gates.py
- tests/i18n/test_groups.json
- tests/i18n/test_test_groups.py
- tests/i18n/test_toolchain.py
- tests/i18n/test_production_review_v2_lite_queue.py
- docs/agent-workflow.md
- docs/review-pipeline-and-tooling-optimization-p2-results.md

```bash
python3 -B tools/i18n doctor
python3 -B -m unittest -q \
  tests.i18n.test_ci_gates \
  tests.i18n.test_test_groups \
  tests.i18n.test_toolchain.CiGatesScriptTests \
  tests.i18n.test_production_review_v2_lite_queue \
  tests.i18n.test_production_review_v2_lite_batch \
  tests.i18n.test_production_review_v2_lite_evidence
python3 -B tools/test_groups.py --check
tools/ci-gates.sh
git diff --check
```

## Cycle 1 已裁决修复

SR-P2-01：新增独立 `validate_historical(result, selected=...)`，queue 的 schema 2
回放只调用此入口。历史 receipt 保留 exact schema、完整构建标志、候选/base 绑定、
成功退出、非空且唯一的安全 ID、有序非空字符串 argv、记录定义的 check-set SHA-256、
非空且引用现有 ID 的 coverage，以及版本语法、时间、日志路径、hash 和类型校验。
它不再与后来变更的 CHECKS/COVERAGE/VERSION 比较；不从历史 receipt 授权生产运行。
默认 `validate` 继续固定当前三项定义，expected_binding 和实际日志 hash 校验仍保留；
prepare 的生产调用未改变，v1 分支未改变。结构检查先于哈希集合操作、正则和 shlex，
畸形 ID/argv/coverage 等输入以 GateError 失败。

SR-P2-02：将恢复测试中的 string-in-dict 无效断言替换为字面量 17 项检查 ID 的精确顺序断言。
新增两个 focused 测试，并扩展真实 queue fixture：分别升级 CHECKS、COVERAGE、VERSION
时历史校验通过且生产校验拒绝；三项同时升级时 queue rebuild/check 仍通过。
重复 ID 即使重算摘要也拒绝，缺项、乱序、错误候选/base、非完整构建、失败退出和畸形结构均拒绝。
本轮仅在原有实现上修改 gate_results、queue、对应两份测试及本文，共五个 SCOPE 内容文件。

初次 focused 为 164 tests、1 error：新断言误将 checkpoint commands 列表按 result 字典读取。
已修正为直接读取记录列表；该错误位于测试断言，非历史 validator 的异常泄漏。
后续结果及实际产物见下方补记。本轮校验只遍历有限 receipt 列表，未重构阻塞扫描或解析循环。

### Cycle 1 最终验证补记

最终代码修改后实际执行以下命令（focused 的完整模块列表与前文复现命令相同）：

```bash
python3 -B tools/i18n doctor
python3 -B -m unittest -q \
  tests.i18n.test_ci_gates \
  tests.i18n.test_test_groups \
  tests.i18n.test_toolchain.CiGatesScriptTests \
  tests.i18n.test_production_review_v2_lite_queue \
  tests.i18n.test_production_review_v2_lite_batch \
  tests.i18n.test_production_review_v2_lite_evidence
tools/ci-gates.sh
PYTHONPATH=. python3 -B .artifacts/i18n/p2-cycle1-replay.py
git diff --check
```

- doctor 通过；最终 focused **164 tests / 23.831 秒，退出 0**。
- full **17 项全部成功 / 96.322 秒，退出 0**，未使用 skip-build。五个分组分别为
  toolchain 484、quality-facts 202、semantic-claim 44、contract-suite 470、
  production-shadow-surface-ledger 277，合计 **1,477 tests**。
- 严格 addon 构建 complete，4,260 runtime keys，artifact identity `515ebd8d97f6d9dd`；
  输出为 `.artifacts/i18n/runs/20260905T015909.337140Z-1195675-build-addon/addon/data/locales/zh_hans.lua`。
- full 结果通过默认生产 `gate_results.validate(result, root=Path.cwd())` 复验，
  17 份日志 hash 相符。此调用复验记录及日志，不宣称在门禁结束后再次执行门禁。
- 同基线完整 `_projection` replay **47.717 秒，退出 0**；46,343,568 字节与
  BASELINE-PROJECTION.json 逐字节相同，SHA-256 仍为
  `2ebefb1905db232d76c876cf7c6a44f7969a5d5b7d294ba8b040ee2f30fe4667`；
  18 份历史 gates 原始文件摘要全部未变。
- `git diff --check` 通过；另以只读字节检查覆盖 untracked 文件尾随空白。
  累计 12 个任务改动路径均在 SCOPE 中，index 为空，HEAD 为原基线。
- 本次 full 与 replay 串行运行；full loadavg 从 1.714/1.778/1.819 升至
  5.096/2.838/2.187。未控制宿主其他负载，本轮耗时不能归因为本修复的性能变化。

ignored 可重生成产物：

- `.artifacts/i18n/p2-cycle1-focused.log`（首轮断言错误记录）
- `.artifacts/i18n/p2-cycle1-focused-final.log`
- `.artifacts/i18n/p2-cycle1-full.log`
- `.artifacts/i18n/p2-cycle1-full-timing.json`
- `.artifacts/i18n/ci-gates/run.uep29prr/results.json` 及同目录 17 份 `.log`
- `.artifacts/i18n/p2-cycle1-replay.py`、`p2-cycle1-replay.log`、`p2-cycle1-replay.json`

本文补记发生在最终门禁后，只记录实际结果，未再改变代码或测试。无未解决测试失败，
无范围扩展；未 stage/commit、创建 children 或写 `.ai` 编排记录。交回宿主独立复审和终态处理。


## Cycle 2 最小修复与用户决定

用户已明确：「历史记录只做自洽校验即可，个人项目不需要过多防御措施。」
历史校验沿用 cycle 1 的自洽语义，不新增历史检查下限或防伪措施；生产严格校验保持现状。
本轮仅修复 FIX-2 指定的 SR-P2-02：batch 首次门禁结果校验及 prospective 生成后
复用校验的两个 handler，将 `subprocess.SubprocessError` 与 `ValueError/OSError`
一并转换为 `ProductionReviewError`，保留原诊断前缀和异常原因链。

本轮只改三个文件：`tools/i18nlib/production_review_v2_lite_batch.py`、
`tests/i18n/test_production_review_v2_lite_queue.py` 及本文；既有工作全部保留。
新增两个有限 fixture 故障注入测试，分别在首次 live binding 和 prospective manifest
已写出后的 live binding 注入 Git `CalledProcessError(128)`。断言诊断前缀与原因链，
后者同时验证只运行一次 gate、失败阶段仍为 adjudicated，并在解除故障后以 fresh gate
恢复至 commit_ready。没有扫描／解析循环重构，未改 queue/replay 逻辑，按 FIX-2
无需重复既有精确回放。未修改 `.ai`、stage/commit 或创建 children。

### Cycle 2 最终验证

最终代码修改后执行 doctor、前文完整模块列表的 focused unittest 命令、
`tools/ci-gates.sh`（无 skip-build）及 `git diff --check`，均退出 0。

- 新增两个故障注入测试单独执行：**2 tests / 0.433 秒**，通过。
- focused：**166 tests / 31.546 秒**，通过。
- full：**17/17 项 / 86.482 秒**，全部通过；五个分组分别为 toolchain 484、
  quality-facts 202、semantic-claim 44、contract-suite 470、
  production-shadow-surface-ledger 279，合计 **1,479 tests**。
- 严格 addon build complete：**4,260 runtime keys**，identity `515ebd8d97f6d9dd`；
  输出 `.artifacts/i18n/runs/20260905T022708.941476Z-1650655-build-addon/addon/data/locales/zh_hans.lua`。
- 用生产 `gate_results.validate(result, root=Path.cwd())` 复验完整 receipt 与
  **17 份日志 hash**，通过。full loadavg 由 4.941/2.090/1.890 至 7.445/3.864/2.551，
  未控制宿主其他负载，不将此次耗时差异归因为本修复。

实际 ignored 产物路径：

- `.artifacts/i18n/p2-cycle2-doctor.log`
- `.artifacts/i18n/p2-cycle2-regression.log`
- `.artifacts/i18n/p2-cycle2-focused.log`
- `.artifacts/i18n/p2-cycle2-full.log`
- `.artifacts/i18n/p2-cycle2-full-timing.json`
- `.artifacts/i18n/p2-cycle2-validation.json`
- `.artifacts/i18n/ci-gates/run.qwi7lo0f/results.json` 及同目录 17 份 `.log`

本文在门禁后补记实际结果，代码与测试未再修改；无计划偏差或未解决测试失败。
独立复审、任务终态及提交留给 ORCHESTRATOR。
