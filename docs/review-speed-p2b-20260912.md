# P2-B contextual adjudication chain：本轮实现与有界验证

任务 `review-speed-p2b-20260912`，EXECUTOR dispatch `execute-astra-01`。
基线 `8eee28ec75ea6f13e705dd1b634ed6c0bc7de199`，冻结候选
`2560f94a1be246ad05937e167b38435dd02088f906a1168a4690d079230fa0ba`。
只实现本轮六文件范围，无 stage/commit、agent 操作或规则／生产验证器变更。
最终状态以 [STATE](../.ai/task/review-speed-p2b-20260912/STATE.json) 为准。
本文不是独立验收、完整门禁、DONE 或提交证明。

## 实现及证据边界

新增固定 `contextual-adjudication-chain --input INDEX --spec SPEC --output FRESH --source-root ROOT`。
一个 carry scope 内依次调用真实 contextual-import CLI、可导入生成函数、真实 adjudicate
CLI、真实 prepare-evidence CLI。生成函数自己获取 writer lock、preflight，再读取本次已接受
observations；不在 wrapper 保留 checkpoint／数据库连接／观察对象。生成文件发布成功才
进入 adjudicate。旧六动作 parse、P1-C workset 分支及旧两位置生成 CLI 合法行为保留。

预检读取严格 JSON index/spec/workset，拒绝重复键、非法类型、重复 revision、非法决策值，
并检查普通文件和 fresh 输出边界。spec/workset 一次读取后固定；index/raw 在导入前和生成前
比较原 bytes。导入后的生成 preflight 才核验真实 batch/catalog/base、selected 冻结行与
verification 的完整绑定，以及 accepted 观察完整集合。复用 `validate_workset` 的无副作用
解析／绑定，不调用源码事实构建，不额外 replay。

仅 confirmed 读取显式根下的普通源码文件，公开相对路径拒绝穿越／绝对／symlink；匹配
冻结工作集 SHA 后原样 UTF-8 解码成 content/hash 快照。不宣称固定 commit／来源身份，
不默认回退 ENGINE。新链不转换非法 repair/disposition。旧 CLI 默认 ENGINE 当前 checkout
语义不变，旧普通输出覆盖行为仅在旧入口保留。
旧两位置 CLI 仍用 cwd 作为 root，现在会在 preflight 前取得 writer lock，可能创建
`<cwd>/.artifacts/i18n/production-review-v2-lite/repository.lock` 及其父目录，锁被其他
writer 占用时先行拒绝。原 baseline 的 preflight 也可能协调孤立 reservation／SQLite，
不能描述为纯只读；新增的是 writer lock 的创建与占用拒绝语义。

输出限定 production root 的 `.artifacts/i18n/adjudication-chain/` 内 fresh 文件。
独占随机 temp → 写完整 bytes → file fsync → hard-link 无覆盖原子发布 → directory fsync →
仅清理自有 temp。开始已存在、发布时竞态目标和非普通父目录拒绝；对方文件原样。
允许失败后留下创建的空目录；发布后异常仍失败，已发布文件需核验后交独立消费者恢复。
普通父目录检查没有扩成抵御恶意父目录并发替换的通用事务框架。

所有循环只遍历本批有限输入／路径分量／已接受观察；没有新增扫描历史、阻塞解析重试或
轮询循环。串行测试使用有限 fixture 与外部 timeout；源码文件本身没有新增尺寸限额。
可复制操作与准备／恢复命令见 [README](../tools/orchestration/README.md#contextual-导入裁决生成与证据准备p2-b)。

## 冻结与旧测试保留

执行前重算 SPEC bytes + NUL + 空 diff 的候选 SHA；HEAD、所有 SOURCE-IMPLEMENT 输入
SHA、SCOPE preimages、candidate 文件 SHA 和 declared_absent 全通过。原始记录：
[freeze-check.json](../.artifacts/i18n/review-speed-p2b-20260912/execute-astra-01/freeze-check.json)。
没有读取、写入或 stage `.ai/consult`。

`BASELINE-TEST-METHODS.json` 的 **165 个方法 SHA 全匹配**，算法是
`SHA256(ast.get_source_segment(text, node).encode())`；另逐个与 baseline Git blob 比较完整
方法行文本，全相同。旧断言、测试体、helper 无修改。只追加一个直接继承 QueueFixture 的
AdjudicationChainTests 类，复用明确 helper，不继承旧测试方法。
[核验明细](../.artifacts/i18n/review-speed-p2b-20260912/execute-astra-01/old-tests-preserved.json)。

## 命令与实测结果

下列测试全部串行，最终生产代码相同；日志目录为
`.artifacts/i18n/review-speed-p2b-20260912/execute-astra-01/`。

```bash
timeout 60s python3 -B tools/i18n doctor
TOME_TEST_FIXTURE_ROOT=/tmp/p2b-fixtures PYTHONPATH=tools timeout 240s python3 -B -m unittest tests.i18n.test_production_review_v2_lite_queue -v
TOME_TEST_FIXTURE_ROOT=/tmp/p2b-fixtures PYTHONPATH=tools timeout 120s python3 -B -m unittest tests.i18n.test_review_source_facts tests.i18n.test_contextual_result_check -v
timeout 60s python3 -B tools/test_groups.py --check
timeout 60s python3 -B tools/paseo_contract_check.py
git diff --check
git diff --no-index --check -- /dev/null docs/review-speed-p2b-20260912.md
```

| 检查 | 实际结果 | 日志 |
| --- | --- | --- |
| doctor | exit 0；既有三个 DLC source-unpinned 提示 | doctor.log |
| 完整既有 queue 模块，含新独立类 | exit 0，222 tests，33.040s | queue-full.log |
| 独立 source-facts、contextual-result 消费者 | exit 0，29 tests，1.311s | source-context-consumers.log |
| registry | exit 0，PASS，未改 registry | registry.log |
| contract | exit 0，10 active documents / 4 live versions / 16 clauses | contract.log |
| tracked / 新文档 whitespace | 检查结果见 whitespace.json | whitespace.json |

进程参数、退出码、外层耗时见
[validation-results.json](../.artifacts/i18n/review-speed-p2b-20260912/execute-astra-01/validation-results.json)。
时间仅是本机小 fixture 单次执行时间，**生产秒数未测量**；不得从 P2-A 的约 106 秒推算
批次节省秒数，也不重复计算 P1-C 或既有两步链的收益。

计数包装真实 `queue._projection`，内部始终调用原函数；不 mock 投影或绕过 preflight。
显式 assert wrapper.queue、生成器 B/B.queue、CLI 的 production handler 与测试 spy
为同一模块对象。固定时钟／gate log 路径，同一个 fixture root 完整还原；创建／还原在
计数 scope 外。旧路径是独立 contextual-import、独立旧生成 CLI main、既有
adjudicate/prepare wrapper 三段；新路径是一个专用链 scope。

| 有界场景 | 旧投影 | 新投影 | 同步比较 |
| --- | --- | --- | --- |
| surface ISSUE + contextual ISSUE | 3 | 1 | 两条独立十字段观察裁决、confirmed 快照 |
| surface ISSUE + contextual OK | 3 | 1 | 仅一条 surface 观察裁决、confirmed 快照 |
| 无 ISSUE 的纯 surface | 沿既有 ProjectionChainTests 空裁决链 | 不伪造新 contextual 链 | 旧完整断言通过 |

前两场景逐步 CLI stdout、生成摘要、canonical adjudication bytes、完整 SQLite 业务行、
checkpoint bytes、prospective 文件与 gates receipt/binding 全相同。生成前后无业务状态
变化。快照包含中文、CRLF 与 LF，字节比较验证保真；非 confirmed 在源码删除后仍成功。
prepare 使用 QueueFixture 已有 `_actual_gate_records` seam，日志中的 fixture PASS 行
**不表示真实 17 门禁成功**。完整门禁／strict build 由宿主对最终候选执行。

## 错误时序与判别力

新链预检比逐个旧 CLI 更早拒绝缺失／结构非法输入和旧输出；不声称所有错误时序相等。
以下生产路径错误均 exit 1，后续阶段调用为 0；断言同时核验持久边界或输出 bytes。

| 故障 | 最后允许阶段与保留物 | 新测试方法（省略 test_） |
| --- | --- | --- |
| 重复 JSON 键、非法 bool/disposition、重复 entry、占用/越界输出 | 导入前；CLI 0，原 checkpoint/SQLite 不变 | precheck_invalid_inputs_and_stale_output_call_nothing |
| 缺失/额外决策、source SHA/文件/路径错误、batch/row 绑定错误 | import 后；CLI 1，deep_collected，无输出 | missing_extra_decisions_source_sha_and_workset_binding_fail_after_import |
| 生成锁被另一 writer 占有 | import 后；CLI 1，无输出 | generator_owns_lock_preflight_and_frozen_decisions |
| raw/DONE task identity 改动，步骤间 raw/SQLite/checkpoint/HEAD 漂移 | import 或生成前停止；CLI 1，无输出 | raw_state_checkpoint_sqlite_and_head_drift_stop_downstream |
| 竞态目标、file fsync、生成时 symlink 父目录 | import 保留；CLI 1，目标对方 bytes 或无文件，自有 temp 清理 | publish_race_fsync_failure_and_symlink_parent_preserve_import |
| directory fsync（已发布后）失败 | import 与已发布 bytes 保留；CLI 1；重跑拒绝旧输出，独立 adjudicate 可恢复 | post_publication_error_stops_and_does_not_adopt_existing_output |
| adjudication observation hash 损坏 | 生成文件保留，deep_collected；CLI 2，无 prepare | adjudicate_failure_preserves_output_and_prepare_failure_recovers |
| prepare gate failure | adjudicated 与文件保留；CLI 3；独立 prepare 再 replay/执行 gates | prepare_failure_in_chain_preserves_adjudicated_and_independent_retry |

生成锁测试在四次真实 preflight 内实际尝试 nonblocking flock，均确认已有锁；导入后
修改 spec/workset 磁盘内容，输出仍使用开始冻结的宿主决策。旧 root/HEAD 变化、正常／异常
scope 退出、独立 queue.check 完整 replay 与旧兼容分支继续由原 ProjectionChainTests、
SourceFactsChainTests 完整断言覆盖。

内存错误变体只在 disposable fixture 中启用，生产文件从未为变体改写：

| 错误变体 | 实测错误行为（用来证明正确断言有判别力） |
| --- | --- |
| 生成无 lock | 在已占有锁时错误生成，CLI 3 / exit 0；正确实现 CLI 1 / exit 1 |
| 生成复用旧 preflight checkpoint | SQLite drift 下错误生成，直到 adjudicate 才拒绝，CLI 2 / exit 1 |
| 不检查 source SHA | 错误接受改动源码并生成，CLI 3 / exit 0 |
| 允许复用/覆盖旧 output | 错误覆盖并继续，CLI 3 / exit 0；正确实现导入前 CLI 0 / exit 1 |
| 生成额外 carry scope | 真实 projection 2 次，不能通过生产预期 1 次的计数断言 |

## 逐 AC 状态与未解决事项

| AC | 本轮证据／状态 |
| --- | --- |
| 1 | 两种适用 contextual 场景真实 3→1，至少少一次达成；纯 surface 空裁决沿旧路径 |
| 2 | 逐阶段报告、生成 bytes、SQLite/checkpoint/prospective/receipt 全等；预检时序差异明确 |
| 3 | 真实 raw/candidate/DONE 消费者、四次独立 lock/preflight、冻结 workset/SHA；adjudicate 验证器未改 |
| 4 | 预检／导入后生成／发布后／adjudicate／prepare 故障和恢复有界验证，后续 0 |
| 5 | 原 scope/root/HEAD/独立 check 全部断言通过，无新 cache／scope／任意动作通路 |
| 6 | 最终测试隔离与兼容通过、旧方法全保留；**作者首轮曾误触主仓库 preflight，执行过程的隔离要求不能宣称全满足** |
| 7 | README、报告、handoff 已给准备/恢复及限制；独立双复审、完整 gates/build、生命周期、DONE/提交由宿主完成 |

首轮命令为（与最终新类运行同形，早期 fixture 尚未修正）：

```bash
TOME_TEST_FIXTURE_ROOT=/tmp/p2b-fixtures PYTHONPATH=tools timeout 180s python3 -B -m unittest tests.i18n.test_production_review_v2_lite_queue.AdjudicationChainTests -v
```

日志 `new-tests-first.log` 有完整终态：exit 1，`Ran 9 tests in 109.357s`，
`FAILED (failures=2, errors=1)`，其中包含主工作树 preflight 的
`ERROR: queue database meta/catalog/evidence-head drift` 拒绝行。
原因已定位到新测试只设置 I18N_REPOSITORY_ROOT，却用旧 main 的 cwd 语义调用
`B.preflight(Path('.'))`，误进入主仓库真实 preflight／投影路径；不能宣称从未接触实际 queue。
该失败调用不作为性能证据。宿主随后已核对当前影响，见
[HOST-INCIDENT-INITIAL-CHECK](../.ai/task/review-speed-p2b-20260912/HOST-INCIDENT-INITIAL-CHECK.json)
及 [HOST-EXECUTION-VALIDATION](../.ai/task/review-speed-p2b-20260912/HOST-EXECUTION-VALIDATION.json)：
queue SHA256 仍为 `c187d216aa0c72d3c0e8116d5165f68c15d3bc9c9490a2c30052db9724b91c15`，
无 checkpoint 或 wal/shm/journal sidecars，HEAD／index 未变，无需恢复当前持久状态。
Opus cycle0 独立完整组运行前后也核对同一指纹与状态；这证明已核对的当前影响，
不撤销首轮误触，也不证明历史执行全程隔离。

已修复新类 helper：旧 CLI main 只在 fixture cwd 调用并 finally 恢复；新类的所有真实
preflight 外包 fixture-root 断言，越界会在真正 preflight 前失败。旧 helper 无变化。
第二轮 `new-tests-second.log` 为 exit 1：9 tests 中两个测试本身失败，一个模块 identity
断言引用了错误导出位置；另一个以 STATE 单字段 STOP 当成 target=DONE 校验必然失败，
实际消费者并无该断言语义。修正为真实 CLI production handler 对象和 task identity 漂移，
没有修改／放宽生产验证器。第三轮同命令 `new-tests-third.log` exit 0，12 tests，3.816s；
再串行执行上述完整 222 + 29 tests，全部通过。

未自行启动新修复／复审轮，未运行主工作树 canonical gates/build、queue/checkpoint 命令或
生产 benchmark；首轮误触 preflight 的例外如上明确保留，当前影响已由宿主及 Opus 核对。
最终全候选复审、全门禁、提交与闭合 STATE 仍由宿主完成；任务验收提交后按既有授权
自动恢复第 92 批。

## Cycle1 集中修复与有界验证

`fix-astra-01` 从冻结 ref
`e88dbd24b33fa41355d2d084a9c030bd94f7762988f916faea181079452d9b75`
继续，起始六文件 SHA、只读 preimage 和已有 cycle0 完整 diff 均匹配。仅增量修改 wrapper、
既有 queue 测试、README、本文与 handoff；make_adjudication.py 逐字节保留。
合并 CROSS-ASTRA-001、P2B-R1、P2B-R2，不按模型 severity 扩大范围。

wrapper 现在与真实 CLI 使用同一真值规则：非空 configured root 才 resolve，未设置／空串
都用脚本仓库默认。新增一个测试方法，依次覆盖空串、未设置、绝对及相对 root；cwd 始终为
另一个临时目录，wrapper／生成器 ROOT 和 CLI 默认路径锚点均先设为同一个 fixture。
在执行前安装 root 防线，锁目录创建、真实 preflight、真实 projection 和输出预检均先验证
fixture 边界，再调用原实现。每个场景实际完成 import／generate／adjudicate／prepare，
四次 lock／preflight 顺序一致、生成两条裁决、checkpoint 达到 commit_ready，真实 projection
恰为 1，另一个 cwd 保持空目录。门禁仍使用既有 fixture seam。

先在尚未修复的旧 root 表达式上运行同一新增回归，exit 1：仅 empty 子场景被输出预检前的
root 防线拦截（`root escaped fixture`），其余三场景通过。随后只向前修正生产表达式，
未临时改回源码制造错误变体。此失败证明旧表达式与回归有判别力；修复后的空值场景须真实
成功，不能靠拒绝空值输入通过测试。此前 Astra 的隔离 probe 已另证旧代码导入后生成 root
分裂，见 [原 probe](../.artifacts/i18n/review-speed-p2b-20260912/cross-astra-0-1/probe.log)。

本轮日志均位于 `fix-astra-01/`，与作者／host／reviewer 的既有证据分开：

| 阶段 | 命令／结果 | 证据 |
| --- | --- | --- |
| 修复前旧 root 判别 | 新增 root 方法；exit 1，1 test，0.541s，仅 empty 失败 | old-root-regression.log、old-root-regression-command.json |
| 修复后串行小套件 | 既有 AdjudicationChainTests 全 12 项＋新增 1 项；exit 0，13 tests，4.535s | chain-tests.log、validation-results.json |
| registry／contract | 两项均 exit 0；registry 未修改 | registry.log、contract.log |
| 空白、方法保留及补丁重建 | 见交付核验记录 | whitespace.json、delivery-check.json |

小套件在临时 cwd 执行，精确 argv、cwd 和两项显式环境配置见
[validation-results.json](../.artifacts/i18n/review-speed-p2b-20260912/fix-astra-01/validation-results.json)：

```bash
env -u I18N_REPOSITORY_ROOT \
  TOME_TEST_FIXTURE_ROOT=/tmp/p2b-fix-final-so7n6eal/fixtures \
  PYTHONPATH=/workspace/tome4-chinese-translation/tools:/workspace/tome4-chinese-translation \
  timeout 60s python3 -B -m unittest tests.i18n.test_production_review_v2_lite_queue.AdjudicationChainTests -v
timeout 60s python3 -B tools/test_groups.py --check
timeout 60s python3 -B tools/paseo_contract_check.py
git diff --check
git diff --no-index --check -- /dev/null docs/review-speed-p2b-20260912.md
```

修复后原 ISSUE／OK 两场景仍实测 3→1，状态／bytes／receipt 等价断言不变。HEAD 基线
165 个和 cycle0 累计 183 个方法正文／断言均按 AST SHA 与完整方法行文本核对保留，
新总数为 184。独立 **440 tests／52.328s** 是 Opus 的 **cycle0** 实测，见
[原独立命令](../.artifacts/i18n/review-speed-p2b-20260912/review-opus-0-1/commands.md)，
本次未重跑，不混入 cycle1 的 13 项结果，也不据此声称修复后的全量门禁通过。

本轮无范围或计划偏差，无未解决的已接受实质项。一次集中修复交宿主安排完整候选终审；
主工作树完整 gates/build、生命周期、DONE_VERIFIED、提交仍待宿主，生产秒数仍未测量。
