# P3 结果：单次 projection 的 Git 对象读取缓存

用户已明确答复「同意调整」：以完整 40 位哈希缓存 blob bytes 和递归 `ls-tree`
的原始 bytes，作为 P3 最终实现范围；保留路径
`git log --full-history --format=%H --diff-filter=AM` 及其调用点，暂不实施可选阶段 B。
这是已批准的范围调整。独立复审、DONE 验证、提交和推送仍由宿主完成，本记录不宣告
这些步骤已经完成。

## 实现边界

- `tools/i18nlib/git_evidence_reader.py`：每次 projection 创建新的同步调用作用域。
  正常退出和异常退出均清空缓存；嵌套 projection 使用独立 reader，退出后恢复外层。
  reader 绑定解析后的仓库根目录；其他仓库的直接读取绕过缓存，其他仓库的 projection
  建立自己的作用域。仓库路径仅用于隔离 reader，不是对象缓存键。
- `tools/i18nlib/production_review_v2_lite_queue.py`：只接入 `_tree`、`_blob` 和
  `_projection` 的作用域包装。树命中后仍重新解析 bytes，因此调用者修改返回的 dict
  不会污染缓存。Git 失败不入缓存；`_git` 及 blob 错误中的当前 label 保留。
- 非完整哈希表达式每次重新解析：先对原表达式执行 `rev-parse --verify`，再对完整
  哈希执行类型剥离。不能直接把 `^{blob}` 或 `^{tree}` 拼到 `HEAD:path` 后面，
  那会变成路径的一部分。真实 Git 回归覆盖文件、目录和同一作用域内移动 HEAD。
- 所有身份、内容哈希、catalog 解析及历史 publication 校验仍逐次执行；没有缓存校验
  结论、解析后的 catalog、路径查询或 ref。没有更改扫描／解析循环的推进逻辑，
  没有持久缓存、跨 projection 缓存、SQLite schema 修改、依赖或历史遍历重写。
- 测试修改为 `tests/i18n/test_git_evidence_reader.py`、
  `tests/i18n/test_production_review_v2_lite_queue.py` 和单一注册表
  `tests/i18n/test_groups.json`。保留全部原有测试与分组，包括 merge、sibling publication、
  split publication、replacement/revert 等历史校验。真实 projection 测试先在禁用缓存时
  确认存在重复 blob 读取，再验证启用后每个 blob 在每次调用中仅读取一次，且输出一致。

## 验证与测量

宿主固定基线为 `e949fa8b1b4e17a419172c147ef66ac90a5a4aca`，以任务目录的
`baseline-measurements.json`、`BASELINE-PROJECTION.json` 和
`BASELINE-EVIDENCE-HASHES.json` 为准。SCOUT 曾引用的 505 数字已撤销，不用于比较。

派生 runner 和完整测量输出位于 `.artifacts/i18n/tooling-optimization-p3-executor/`。
runner 参照宿主 `measure.py`，只读取宿主基线，所有写出都在自己的 artifact 目录。
耗时计量窗口和 canonical JSON 序列化格式沿用宿主方式；每轮均将完整 projection bytes
与宿主基线直接比较，而不只比较摘要。

执行命令：

```bash
python3 -B tools/i18n doctor
PYTHONPATH=tools python3 -B -m unittest tests.i18n.test_git_evidence_reader tests.i18n.test_production_review_v2_lite_queue
python3 -B tools/test_groups.py --check
python3 -B .artifacts/i18n/tooling-optimization-p3-executor/measure.py
tools/ci-gates.sh
git diff --check
```

初次 focused 运行 144 项，其中 1 项失败，原因是 `HEAD:a^{blob}` 的路径表达式回归；
宿主也独立确认了该问题。修正为两步归一化并增加目录表达式回归后，145 项通过。

加强真实 projection 的禁用缓存对照断言后，最终 focused 复验为 **145 项通过**，
耗时 23.166 秒，日志 `focused.log`。注册表检查和 doctor 通过；doctor 对受保护源码
工作树扫描的既有跳过提示不影响通过。

三轮固定基线对照结果：

| 运行 | 宿主基线秒数 | 本次秒数 | 基线 Git 进程 | 本次 Git 进程 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 40.696060 | 40.063633 | 1733 | 1359 |
| 2 | 45.620073 | 39.109423 | 1733 | 1359 |
| 3 | 67.781872 | 39.980105 | 1733 | 1359 |
| 中位数 | 45.620073 | 39.980105 | 1733 | 1359 |

每轮的 Git 操作计数完全一致：

| 操作 | 基线 | 本次 | 减少 |
| --- | ---: | ---: | ---: |
| rev-parse | 7 | 7 | 0 |
| ls-tree | 75 | 29 | 46 |
| cat-file（含其他 evidence 消费者） | 1046 | 718 | 328 |
| log | 536 | 536 | 0 |
| rev-list | 25 | 25 | 0 |
| merge-base | 44 | 44 | 0 |
| 合计 | 1733 | 1359 | 374 |

queue `_git` 调用从 1417 降至 1043；其中 blob 从 774 次降至 446 次，每个 blob
完整哈希仅读取一次。树从 75 次降至 29 次，每个树查询也只执行一次。
另外 272 次 cat-file 属于未改动的其他消费者。三轮中的全部 536 条 log 的完整 argv
及次数均与各自宿主基线精确一致，见 `calls-check.json`。

缓存保留量的测量方式：从上述 artifact 目录的 `optimized-calls-1.json` 中筛选
`argv` 为 `["cat-file", "blob", ID]` 的记录，将 ID 去重后逐行送入
`git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize)'`，统计 blob
数量、大小总和及最大值。本次 446 个不同 blob 保留 **283805782 bytes（约 283.8 MB）**，
最大单个 blob 为 **35219639 bytes（约 35.2 MB）**，MB 按十进制计；这些 bytes
保留至本次 projection 退出，保留量随实际读取的不同 evidence/catalog 对象的字节总量增长。
这是 blob bytes 的保留量，不是进程峰值 RSS，不能据此推断 RSS 增长倍数，
也不能推断每次迁移必然增加固定保留量。

三轮完整 canonical projection 均为 **46,343,568 bytes**，SHA-256 均为
`55ae0feb42bf67a17fec4080332231cc1707c44bf024ffdb8c953680971b4a34`，并通过直接 bytes
相等断言。`audit.py` 还按 `git ls-files` 取完整 evidence 路径集合，核验 **700 个文件**
的 SHA-256 映射与宿主冻结值完全一致，结果为 `evidence-check.json`。复验命令：

```bash
python3 -B .artifacts/i18n/tooling-optimization-p3-executor/audit.py
```

本次中位数比基线低 5.640 秒（12.36%），这是观测值，不是可保证的加速比。
宿主三轮范围为 40.696–67.782 秒，本次为 39.109–40.064 秒；两组不是交错运行，
操作系统缓存和同时段负载没有受控。基线一分钟 load 从约 1.36 到 4.96，本次从
约 1.29 到 3.49，完整起止三元 load 记录在 measurements JSON 中。本次未同时运行
focused 或完整门禁。计数减少 **374 次／21.58%** 是确定的收益，不能将所有耗时下降
归因于本次实现。

## 已批准的阶段 B 延后决定

用户已批准暂不实施 `cat-file --batch`，保留现有路径 log 和历史遍历。决定依据是剩余
读取成本占比较低：本次 queue 中
446 次 blob 读取的累计 `_git` 耗时仅为 0.878／0.845／0.845 秒，全部 queue `_git`
约 2.46／2.42／2.42 秒，而 projection 总耗时约 39–40 秒。消除单次读取进程的进一步
收益空间有限；另有 272 次 cat-file 属于独立 evidence 消费者，不能直接外推其成本或
默认将其纳入本次范围。上述计时不包含其他消费者的全部 Git 耗时，也不是严格性能剖析。

若继续阶段 B，应先独立测量剩余读取成本，再对 batch 子进程生命周期、部分输出和失败
传播做有界实验，并继续要求完整 projection bytes 和历史回归不变。现有结果不支持
承诺绝对耗时目标，也不支持为节省 536 次 log 而引入自定义历史重写。原计划 log 缓存
无法从当前 536 条互不重复的路径查询获得命中；完整 commit/blob 哈希本身也不能区分
路径历史。用户已批准以 blob/tree 缓存收束 P3，无需再次决定该范围调整。

## 完整门禁记录与交付限制

首次完整门禁 `.artifacts/i18n/ci-gates/run.a8uf44xx/results.json` 的各项命令虽退出 0，
但运行期间补写结果文档导致 `gate binding changed during execution`，总结果失败，
不作为有效通过凭据。

随后通过 `python3 -B .artifacts/i18n/tooling-optimization-p3-executor/final-gates.py`
完成完整门禁复跑。按 DOC-CLOSE 确认的有效最终记录为
`.artifacts/i18n/ci-gates/run.2ryqsj2n/results.json`：**17 项检查、1487 项测试通过，
含严格 build**。该结果对应已测试的实现；本轮仅按用户已批准的决定收束结果文档，
不重复完整长测，也不将旧门禁绑定描述为覆盖本轮文档编辑后的工作树。

本轮文档收束执行 `git diff --check`、本文件 whitespace 检查与源码哈希前后比对。
两个实现文件、两个测试文件和测试注册表的 SHA-256 均与本轮编辑前一致。
仅编辑本结果文档；未修改代码、测试或 `.ai`，未创建 children，未 stage/commit/push。
独立复审、DONE 验证及提交推送由宿主继续执行。
