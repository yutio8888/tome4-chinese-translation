# P2-A 发布历史查询：EXECUTOR 实现报告

任务 `review-speed-p2a-20260912`，当前 dispatch `fix-astra-01`、FIX cycle1。
本轮输入 candidate ref 为 `685291a5d93c1c6424e508e7feee59dc441ed83afd14b3d15a77991ecdc11fee`；
起始 HEAD 和 CYCLE1-START 六文件 SHA 均匹配。以下旧验证与测量明确保留为 cycle0 历史，
本轮验证见文末；最终状态仍以 STATE 为准，不宣称 DONE。

cycle0 dispatch `execute-astra-01`；输入 HEAD
`793e45aeb0b1d43539baeda05708c393de200995`，candidate ref
`90499abb8e02b0b05bab24c8ebb74523a6540c834e89f10a9ddf3b183fba42d2`。
初始五文件 SHA、报告缺失声明、空 tracked diff 均匹配冻结输入。
任务状态以 [STATE](../.ai/task/review-speed-p2a-20260912/STATE.json) 为准。

## 算法与边界

唯一生产代码改动是 `tools/i18nlib/production_review_v2_lite_queue.py`。
原 `_publication_commit` 函数主体完整保留为 `_publication_commit_slow`，包装器只在
成功得到唯一发布 commit 时提前返回。所有其他已有生产函数及原有测试方法的 AST
均与输入相同；migration 验证、发布定位及完整 progress 消费路径不变。

快路径要求相同 root 的活动 projection scope、完整小写 40 位 commit OID 的 head/base、
同一批次目录下的规范安全 ASCII 路径，以及当前条目为普通 blob。
base 别名不解析后冒充原字符串：不满足上述要求即调用旧算法。
`ls-tree -r -t -z --full-tree` 严格解析包含空 tree 的布局，证明批次目录及全部后代
不存在，且 evidence 的三个祖先位置没有文件、symlink 或 gitlink 阻挡。
通过既有 `derive` 仅缓存固定 OID 的 commit 解析结果，以及
`(祖先阻挡标志, 已占用批次名称 frozenset)`；不保留第二份完整布局字典或成功许可。cycle1 另存一个仅属于当前 root/scope 的禁用标志。
临时解析集合随 loader 结束释放，scope 的既有 finally 清除派生缓存。

候选仍来自 `sorted(paths)[0]` 的原始完整
`git log --full-history --format=%H --diff-filter=AM <head> -- <anchor>`。
逐个遍历全部候选，检查全部当前 mode/type/OID 精确相等，且恰有一个 parent
等于原始 base 字符串；恰有一个匹配才快返回。
其余路径在该 base 中不存在、在候选中为普通文件，因而属于逐路径 AM 的 A 子集。
零匹配、多匹配或探测错误均回退；慢算法的异常类型与稳定诊断照旧传播。
不修改 `_git(root, "log", ...)` 的参数结构或计数入口。

尚未禁用的 scope 每次请求均在路径资格判断前重新运行有效配置及覆盖状态 guard：
Git 自行展开系统、全局、仓库和 includes。仅允许 `GIT_PAGER`、`GIT_EDITOR`、
`GIT_CONFIG_GLOBAL`、`GIT_CONFIG_SYSTEM`；其他 `GIT_*`（含环境配置和自定义 replace namespace）
保守回退。两个 selector 只选择实际读取的文件，绝非可信标记；所有 Git 调用与 config
检查继承完全相同环境，没有为 guard 临时清理或替换环境。
配置只允许无关的常规 user/remote/branch/credential/safe/init/filter、列明的 core 设置、
`core.editor`、include 指令，以及布尔 `diff.renames` 和显式假值 `log.follow`；未知设置保守回退。
因此 copies/follow、外部 diff/textconv 驱动及未审定 diff/log 设置均不获快路径许可。
通过 Git 解析真实 git/common 目录，检查 shallow、graft、replace refs；支持 `.git` 为文件的
linked worktree。额外检查 `--show-prefix` 为空：子目录 cwd 的 log pathspec 与 full-tree
布局坐标不同，必须回退。观察到 unsafe 或环境探测异常后，在当前 reader 的 derived 中
保存 `("publication-fast-disabled-v1", "scope") = True`，该 scope 剩余请求只走旧 slow。
不清除已缓存 tree，不修改 reader 运行时或发布判定。fresh、nested、不同 root 隔离，
scope 的 finally 同时清除禁用标志；元数据 loader 失败仍不缓存并可重试。
guard 不记录配置原值；原 slow 自身的异常继续按旧语义传播。

## Cycle0 有界验证（历史）

所有测试均使用真实临时 Git 对象、tree、commit DAG 与 refs；正常语义不 mock 历史答案。
失败注入只覆盖探测/读错误，慢路径 spy 用于证明实际回退。
测试日志保存在
[execute-astra-01](../.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/)。

| 验证 | 结果与证据 |
| --- | --- |
| 正常新目录 | 快慢同 commit，明确断言恰一条原参数 log |
| split raw/core、相同 base 的相同 siblings、merge 自身发布 | 快慢均拒绝；多个 child 仅一个精确匹配可成功 |
| change/revert、删除恢复、不同 base | 比较绑定的原发布；已有目录的 M 仍走慢算法 |
| 批次外 rename/copy | 比较真实逐路径 AM；copies/follow 配置明确回退 |
| mode/type/OID | executable、symlink、gitlink 均作精确 tuple 比较 |
| 目录边界 | 文件/目录互换、空 tree、三层祖先普通文件/symlink/gitlink 阻挡均回退 |
| 路径边界 | 非 ASCII、空格、TAB/LF、反斜杠、glob/pathspec、跨批次、别名、子目录 cwd 均回退 |
| 可变 Git 状态 | includes 内容变化、环境配置及 pathspec 覆盖、replace/自定义 namespace、graft、真实 shallow clone、linked worktree |
| 失败与缓存 | 配置/目录解析/refs/tree 探测失败、畸形布局、原 Git 失败保持异常；正常、嵌套、跨 root、异常退出、HEAD 移动无作用域泄漏 |
| migration | 无任何 batch 引用的坏 migration 仍在完整投影中失败，快慢异常相同 |
| 三个有限错误变体 | 忽略 AM 错收 T、取首个匹配错收 siblings、仅比 OID 错收 mode 变化，全部被真实 fixture 检出 |

首次 `publication-first.log`：13 项，退出 1；唯一失败是新增 fixture 错将“只改 raw 再恢复”
预期为有效发布。慢算法及快算法均拒绝，因为 core 在恢复 commit 没有 AM 记录。
已保留失败日志并修正该新增断言，同时增加全部路径修改后恢复的有效 M 边界用例。
未删除或弱化原有断言。

四模块串行 `bounded-four-modules.log`：255 项、32.695 秒、退出 0。
此后补充子目录 cwd guard，针对受影响的发布历史与 reader 补跑
`final-boundary-tests.log`：27 项、1.171 秒、退出 0；未重复整套四模块。
最终唯一测试集合共 256 项，新增 17 项（发布历史 14、reader 2、migration 1）。
宿主冻结比较器的五项有界测试亦通过；它检查字段、非有限数、精确门槛边界、身份漂移及
拒绝覆盖，未调用旧 PERF-1 compare。

四模块的精确命令（cwd 为仓库根；仅显式设置以下两项测试环境）：

```sh
timeout -k 10s 1200s env PYTHONPATH=tools:. TOME_TEST_FIXTURE_ROOT=/workspace/tome4-chinese-translation/.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/fixtures python3 -B -m unittest tests.i18n.test_git_evidence_reader tests.i18n.test_production_review_v2_lite_queue tests.i18n.test_production_review_v2_lite_migration tests.i18n.test_production_review_v2_lite_progress -v
```

补跑使用同一 `env`，timeout 为 120s，模块为
`tests.i18n.test_production_review_v2_lite_queue.PublicationHistoryTests tests.i18n.test_git_evidence_reader`。
有限循环均遍历固定配置项、有限 tree 记录或有限 Git 候选；上述 120s 真 Git 测试同时作为终止探针。

## Cycle0 唯一可行性投影（历史，非修复候选测量）

cycle0 生产代码完成有界检查后，仅执行一次当时授权的完整只读投影，退出 0；未重跑、未覆盖样本。
未设置额外运行环境；计量器使用继承环境，guard 未写入任何配置原值。
精确命令：

```sh
timeout -k 10s 420s python3 -B .artifacts/i18n/review-speed-p2a-20260912/benchmark_host.py --root /workspace/tome4-chinese-translation --treeish 793e45aeb0b1d43539baeda05708c393de200995 --output .artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/candidate-feasibility.json
```

[原始样本](../.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/candidate-feasibility.json)
与 [冻结比较器结果](../.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/feasibility-comparison.json)
保留完整 progress、八身份、Git 各类计数和资源记录。比较器退出 0，25 项检查全为 true。

| 指标 | baseline | candidate feasibility | 冻结上限 | 判定 |
| --- | ---: | ---: | ---: | --- |
| wall 秒 | 143.6211835530121 | 106.4133819109993 | 129.2590651977109 | 通过 |
| total user 秒 | 129.51 | 103.32000000000001 | 135.9855 | 通过 |
| peak self RSS KiB | 1883220 | 1883060 | 2071542，且 ≤4194304 | 通过 |
| 发布 log 次数 | 2753 | 212 | 275 | 通过 |
| self / children user 秒 | 93.38 / 36.13 | 93.12 / 10.2 | 使用 total user 门槛 | 通过 |
| self / children sys 秒 | 1.27 / 13.35 | 1.24 / 2.47 | 记录项 | — |
| total sys 秒 | 14.62 | 3.71 | 记录项 | — |
| 全部 Git 调用 | 6252 | 4357 | 记录项 | — |
| log 子进程 elapsed 秒 | 40.940808693441795 | 3.3408865108795 | 记录项，不另加到 CPU | — |

本次单投影 wall 减少 37.2078016420128 秒（25.9069%），user 为基线的 79.7776%，
RSS 为基线的 99.9915%。实际 212 条 log 与 129 批次加 83 migration 的条件计数一致。
这只是旧代码的一个 fresh-process 可行性样本；不能据此宣告修复候选性能或
完整性能验收，更不能推算整个审核批次节省分钟。

固定 root/treeish、八项 identity 及完整 progress 深等；两次运行各自的 HEAD 不变，
且运行间 HEAD 相同。queue/checkpoint 运行内及运行间指纹相同，checkpoint 均不存在，
database SHA 为 `c187d216aa0c72d3c0e8116d5165f68c15d3bc9c9490a2c30052db9724b91c15`。
未执行 rebuild/replace/status 或写入生产 queue、checkpoint、历史 evidence。

计量绑定（执行前后核对不变）：

- baseline SHA256：`393780fddbcca573f139a9eaa4ec80f3728dfc52ed4e3027e376d6dd7138d4a2`
- benchmark_host SHA256：`0af1ab9ab6ff79d1de3c465e9c0775cb2833f8a264705a000a0c2cc8fa2cfadd`
- 原 benchmark_projection SHA256：`f00bf919d8043b0b6e6750918a9c2003ff653ad5857cda47399f1843c50b0937`
- 宿主比较器 SHA256：`76f91bf978b21cc77c22838990ec92f5f8df28d91276ee0e9150490578e9fe95`
- 候选 queue SHA256：`6214d0c4ae2919258352061bc5c75cb1a0f56b6253e9ccb930f073ccbbd21dcd`
- feasibility SHA256：`401d54d4492a5324c8258d2bf7bb4f316c0912ffe16d5b0ae3f8db120203c1ca`

## Cycle0 交付与 AC 记录（历史）

- AC1–3：原慢算法和所有已有函数/断言保持；上表逐项真实差分、环境回退、三种错误变体通过。
- AC4–5：本 dispatch 的唯一可行性样本通过；两个独立 candidate 样本归宿主，尚非最终验收。
- AC6：四模块及受影响边界补跑、注册检查、契约检查、tracked/cached/new-file 空白检查通过。
  完整 17 门禁、strictbuild 及独立复审由宿主完成，本 dispatch 未执行。
- AC7：仅 SCOPE 六文件产生内容 diff；handoff 仅更新 P1-C DONE、P2-A 权威状态及 P2-B 后恢复 92。
  未写 `.ai`、未读 `.ai/consult`、未 stage/commit、未派生或操作 agent，未进入下一轮。

[execution-report.json](../.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/execution-report.json)
记录完整 argv、显式环境、退出码、日志路径、逐 AC 状态及六文件 SHA；
[完整 HEAD diff](../.artifacts/i18n/review-speed-p2a-20260912/execute-astra-01/HEAD-six-files.patch)
包含新报告。最终状态裁决、两次独立测量、门禁、归档与提交均交回宿主。

## FIX cycle1：本轮交付

只增量修改 queue 生产模块、queue/reader 两个测试文件、本报告和 handoff；migration 测试文件
与 CYCLE1-START 逐字节相同。没有修改旧 reader 运行时、发布判定、baseline、harness、
原 benchmark 模块、比较器或失败样本；没有执行全历史投影、正式门禁、build、stage/commit、
agent 操作或真实 queue/checkpoint/HEAD 写入。四模块测试日志里的 gates/build 文本来自原有
临时 fixture 的模拟验证，不是执行仓库完整门禁。本轮全历史投影使用预算为 **0/0**。

### 三项 accepted 的闭合证据

1. **HOST-P2A-1**：复制宿主探针到本次输出目录，只把输出位置改为参数；没有覆盖宿主结果。
   [旧候选结果](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/old-mutable-scope/result.json)
   的 `equivalent=false`：replace 存在时 wrapper 走 slow 并缓存 replacement tree，移除后
   wrapper 错误成功，同 scope/fresh slow 拒绝。
   [新候选结果](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/new-mutable-scope/result.json)
   为 `equivalent=true`：移除 replace 后三者均以原异常拒绝。
   新测试另覆盖正常→unsafe→正常，以及 `HEAD` 别名首次进入 unsafe（路径资格不满足也须禁用）；
   显式检查旧缓存 bytes 对象没有被清除或替换，嵌套异常、safe outer/unsafe inner、不同 root 和
   fresh scope 均隔离。原 slow 的拒绝诊断未改。
2. **Opus R1，收窄采纳**：仅增加 `GIT_EDITOR`、`core.editor` 及两个 config 文件 selector。
   [真实 editor 对照](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/editor-comparison.json)
   先证明该默认配置无 editor 时旧 guard 为真，然后在同一 `GIT_EDITOR=true` 环境和真实 Git
   fixture 上比较冻结旧模块与修复模块：两者返回同一发布，旧 slow 调用 1 次，新 slow 0 次。
   selector 文件、include 内容、selector 自身切换、仓库配置均用真实 Git 检查；不安全内容回退，
   malformed config 的原错误保持，修复文件后原 scope 仍禁用。未放行其他 Git 变量或
   color/alias/pull/push/gc/commit 配置命名空间。
3. **Opus R2**：仅新增 P2 fixture 的 setup 进入确定性环境，移除继承的 `GIT_*` 后设置
   `GIT_EDITOR=true` 和两个专用空配置文件。全部 Git 调用与真实 guard 都在这个环境中执行。
   HOME、CODEX_HOME 与其他非 Git 环境项保持原值。两个 P2 reader 方法原体不改，移入独立
   `PublicationReaderTests`，其 setup 在调用旧 fixture setup 前隔离环境；旧 reader 测试没有被
   重复继承或改动。额外进程主动继承无效 GIT_DIR、不安全 global/system/include 及 external diff，
   三项 fixture 仍通过；测试内部又显式施加不安全环境/配置并验证回退，未 mock 正常 guard 或历史答案。

Git 依据：官方 [Git 2.39 环境变量文档](https://git-scm.com/docs/git/2.39.0) 说明 editor 用于
需要交互编辑器的命令，两个 selector 选择实际 global/system 配置文件；
[git-var 2.39](https://git-scm.com/docs/git-var/2.39.0) 给出 GIT_EDITOR 与 core.editor 的关系。
结合本任务固定的非交互读取命令及真实 Git 2.39.5 fixture，采用 DECISIONS 的有界许可。
没有扩展至其他未经本轮必要性核验的变量或配置。未知环境/配置仍保守回退，不能保证这些环境的提速。

### Cycle0 新测试的必要更正

旧 baseline 的 53 个 queue 生产函数（只允许原发布函数改名）及三个测试文件的 201 个旧方法
逐段源码相同，其中旧 test 方法 141 个；
[保留证明](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/preservation.json)
记录逐文件数量。migration 本轮全文件 SHA 不变，reader 运行时与 HEAD 逐字节相同。
本轮只更正以下三个 cycle0 新测试固化的错误恢复预期：

- `test_effective_config_includes_and_same_scope_changes`：unsafe include 恢复安全后，
  同 scope 的 fast 预期从成功改为 None，另在 fresh scope 断言真实 fast 成功。
- `test_environment_overrides_are_rechecked_without_secret_output`：移除 unsafe 环境后，
  同 scope 仍禁用；fresh scope 仍断言 fast 成功。
- `test_probe_failures_retry_and_preserve_original_errors`：config/rev-parse/refs 环境探测失败后，
  同 scope 不再 fast，并实际比较 wrapper 与 slow；fresh scope 成功。ls-tree 元数据 loader
  与畸形布局的重试成功预期保留，增加失败派生值未入缓存的断言；原 Git 异常相等断言保持。

另外调整了新增 PublicationHistoryTests 的 setup 环境，并迁移两个新增 reader 方法的所属 class；
它们的测试主体及成功/失败断言未改。新增三个 test 方法补充本轮真实反例与环境边界。

### 本轮验证与命令

所有命令 cwd 均为仓库根；完整 argv、显式环境、退出码及日志路径见
[validation-commands.json](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/validation-commands.json)。

| 验证 | 结果 |
| --- | --- |
| 旧/新宿主探针（每次 timeout 120s） | 各退出 0；真实反例从不等价变为等价 |
| 旧/新 editor 探针（timeout 120s） | 退出 0；真实发布相同，新模块未调用 slow |
| 初步针对性测试 | 19 项，1.378s，退出 0；随后只补充 editor/config 断言 |
| 恶意调用者环境测试 | 3 项，0.233s，退出 0；覆盖补充后的 editor/config 及两个 reader fixture |
| 最终四模块串行一次 | **259 项，33.302s，退出 0**；调用者环境显式 `GIT_EDITOR=true` |
| test registry | `python3 -B tools/test_groups.py --check`，退出 0 |
| contract | `python3 -B tools/paseo_contract_check.py`，退出 0；10 文档、4 live versions、16 clauses |
| tracked / staged / 新报告空白 | `git diff --check`、`git diff --cached --check`、`git diff --no-index --check /dev/null docs/review-speed-p2a-20260912.md`；前两项退出 0，新文件 diff 退出 1，三项均无空白错误输出 |
| baseline 旧体 / 六份 preimage | `python3 -B .artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/preservation.py`，退出 0 |

最终四模块精确命令：

```sh
GIT_EDITOR=true PYTHONPATH=tools:. TOME_TEST_FIXTURE_ROOT=/workspace/tome4-chinese-translation/.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/fixtures timeout -k 10s 1200s python3 -B -m unittest tests.i18n.test_git_evidence_reader tests.i18n.test_production_review_v2_lite_queue tests.i18n.test_production_review_v2_lite_migration tests.i18n.test_production_review_v2_lite_progress
```

新增代码只遍历有限配置项和有限输入，仍沿用原完整 AM 候选扫描；120s 的小型真实 Git 探针与
针对性测试覆盖其有界终止。未重新运行已经通过的四模块套件，最终测试后未修改运行时或测试代码。

### 测量与剩余验收

保留 Opus [sample-1](../.artifacts/i18n/review-speed-p2a-20260912/review-opus-0-1/sample-1.json)：
继承 `GIT_EDITOR=true`，143.084446739s、2753 条 log，比较器退出 **1**；
[sample-2](../.artifacts/i18n/review-speed-p2a-20260912/review-opus-0-1/sample-2.json)：
去掉 editor，106.247793537s、212 条 log，比较器退出 **0**。
它们是两个不同环境诊断，不能称为两次成功正式验收；cycle0 executor 的 106.413381911s 也只属于
旧候选。修复改变运行时后，这三份旧样本均不能预报本轮候选性能。

宿主仍需对最终同一候选执行一次完整 FINAL_REVIEW；Opus 在同一继承 `GIT_EDITOR=true` 环境下
串行两次 fresh-process 测量，使用未变的 baseline/harness/comparator 和原阈值。
正式门禁、归档、提交及最终状态裁决由宿主处理，本 dispatch 不启动下一轮，不预报生产省时。

本轮五文件增量见 [cycle1-incremental.patch](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/cycle1-incremental.patch)，
最终六文件 SHA、精确命令及检查结果见 [execution-report.json](../.artifacts/i18n/review-speed-p2a-20260912/fix-astra-01/execution-report.json)。
