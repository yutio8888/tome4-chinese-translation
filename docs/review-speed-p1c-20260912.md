# P1-C 可选源码事实输入：实现与有界验证

任务 `review-speed-p1c-20260912`，EXECUTOR dispatch `execute-astra-01`。
基线 `d0c4be17ce62b5eefbd3bc8fc0f91b345138be55`；11 项 SCOPE preimage 与接受设计 SHA
`0c8e90a2d6bc7e743a665c95280f1739c35dc9e90bf9d5fdd35afe71e316a2e5` 已核对。
本报告是实现交付，当前任务状态以
[STATE](../.ai/task/review-speed-p1c-20260912/STATE.json) 为准，不表示独立验收或 DONE。

## 实际改动与逐 AC 证据

| AC | 实现与实际验证 | 状态 |
| --- | --- | --- |
| 1 可选入口／兼容 | CLI `--source-workset` 传到 export；wrapper `contextual-export=<path>` 走相同 CLI。真实 Git/SQLite fixture 的 surface-import→export 两 run 保持独立调用 2 次、wrapper 1 次真实 `_projection`，checkpoint、业务行、envelope bytes 完全相等。v1、v2 无重排、v2 `{2,1}` 的原 payload/candidate/envelope 全字节比较通过。 | confirmed |
| 2 身份／冻结 | writer lock、preflight 后单次读取普通工作集；重复键、非法 schema/count/行号类型、batch/catalog/base、selected 精确覆盖、完整冻结行和 verification 对应字段均校验。仅 deep 条目进入包；测试精确顺序及浅审条目 source/target/revision 不泄漏。包 SHA 可从各 context 重建；原始 bytes、事实、合法术语绑定变化均改变 candidate。第二 run 错 SHA 或非法目标临时路径不写第一 run；已有 facts 不接受不同输入或裸重试。 | confirmed |
| 3 固定来源 | 无写入副作用的共享构建器、旧命令 main guard。manifest mount/section 决定实际来源，catalog component 单独保留。固定 A 在 checkout 改 B／删除后仍输出 A 和真实 blob SHA；错 commit、SHA、缺对象、非普通 blob、CRLF/非法 UTF-8、路径和 symlink 负例通过。extractor 取独立 commit A，engine commit 内的 extractor B 不被误用。DLC 同名文件跨组件隔离、engine.lua 跨 DLC、字节漂移与目录歧义检查通过。 | confirmed |
| 4 有限入口／术语／格式 | literal、interface require/literal、host key/extractor、dynamic call/sibling key、concat/argument、always_merge locale、legacy section/definition/marker 均有对应入口测试；多个归属并存不覆盖。自由 rule/confirmed 不进入事实。术语使用生产 path/length framing，保留文件/行/SHA、scope/tag/status/notes，nil 不配空串，不扫描其他条目现有译文。伤害／抗性／概率同 `%d%%` 与非伤害 `%0.2f` 全部 unknown。 | confirmed |
| 5 边界 | 默认 ±3 行；每 revision 8 入口／120 展示行／32 KiB，每 run 512 KiB，超限报错。真实超 32 KiB 内容以及各限额定向测试通过。一次构建内同仓库/commit 的 tree 只列一次，同 blob 只读一次，20 次读取探针只有 3 个 Git 命令；不逐行启动 Git，不递归发现调用链。 | confirmed |
| 6 消费链／测试 | 实际 contextual import 的 DONE_VERIFIED fixture 检查、adjudicate、prepare 路径通过；删除外部源码、术语工作副本、manifest 工作副本和工作集后仍消费冻结 envelope，raw evidence 原样保存。prepare 沿用既有 fixture gate seam，未运行生产门禁。新测试注册到 `production-shadow-surface-ledger`。 | confirmed |
| 7 交付 | 仅 11 个允许文件；README 给出 CLI/wrapper、配置、冻结和恢复边界；handoff 只更新 P1 已 DONE、本任务 STATE 入口及既有恢复顺序。完整 diff、逐次验证记录和文件摘要保存在 dispatch 产物目录，供主代理冻结全候选。 | executor 交付；独立验收 pending |

合法 `[]`／null 且无归属入口的事实明确为 `pending/missing_evidence`。DLC 公开源码版本未固定，
目录提取 snapshot 不代表源码 commit；未带独立版本依据的辅助输入仅绑定本次 bytes。
这些状态不会被工具提升成机制结论。locale 入口证明 locale 记录，未宣称固定源码仍有运行调用。

## 验证记录

精确 argv、退出码、耗时及环境见 dispatch 目录下 `checks.jsonl`，逐次输出为同名 `.log`：
`.artifacts/i18n/review-speed-p1c-20260912/execute-astra-01/`。
测试统一 `PYTHONPATH=tools:.`，`TOME_TEST_FIXTURE_ROOT` 指向该目录的 `fixtures/`；
新纯源码测试使用 `/tmp/p1c-source.*` 并自动清理。

已完成的主要命令（退出码均为 0）：

```bash
# 220 tests；包含全部既有 batch/queue 测试及当时已有的新测试。
timeout -k 10s 1200s python3 -B -m unittest \
  tests.i18n.test_review_source_facts \
  tests.i18n.test_production_review_v2_lite_batch \
  tests.i18n.test_production_review_v2_lite_queue -v

# 最终行为增补：72 tests；新增源码事实／CLI 链路／兼容与既有直接消费者。
timeout -k 10s 300s python3 -B -m unittest \
  tests.i18n.test_review_source_facts \
  tests.i18n.test_production_review_v2_lite_queue.SourceFactsChainTests \
  tests.i18n.test_production_review_v2_lite_batch.SourceFactsCompatibilityTests \
  tests.i18n.test_contextual_anchor_preflight \
  tests.i18n.test_contextual_result_check -v

# 最后一次 export 写入前验证调整后：19 tests。
timeout -k 10s 300s python3 -B -m unittest \
  tests.i18n.test_production_review_v2_lite_queue.SourceFactsChainTests \
  tests.i18n.test_production_review_v2_lite_queue.ProjectionChainTests \
  tests.i18n.test_production_review_v2_lite_batch.SourceFactsCompatibilityTests -v

timeout -k 10s 300s python3 -B tools/test_groups.py --check
timeout -k 10s 300s python3 -B tools/paseo_contract_check.py
```

最后对受跟踪 diff 与两个新文件分别做 whitespace 检查；实际结果和命令见 `checks.jsonl`。
`git diff --check` 退出 0；两个 `git diff --no-index --check /dev/null <新文件>`
退出 1 且无诊断输出，1 表示新文件与空文件存在 diff，不是 whitespace 错误。
不将重叠测试次数相加为独立用例数，也不把 fixture 时间当生产省时。

开发中保留的失败记录：`facts-01`（新 fixture 的 DLC baseline 未同步独立 extractor commit）；
`chain-01`（复用 setup 的 super 绑定）；`chain-02`（fixture 配置非法 `../dlc`）；
`chain-03`（首次 fixture 时钟未冻结）；`chain-04`（CLI index 应传输出文件路径）；
`chain-05`（CLI stdout 为文本报告，测试误当 JSON）。对应 fixture 已修正，原断言未删除或弱化，
后续记录给出通过结果。

旧测试保留核验：基线 batch 的 13 个和 queue 的 96 个既有 `test_*` 方法，其 AST 与当前逐一相等；
原失败断言全部保留。共享 fixture 仅增加可选 `TOME_TEST_FIXTURE_ROOT`，默认位置不变，
用于把本 dispatch 的派生产物限制在授权目录；queue 测试 main guard 移至新类之后。
新增源 fixture 的完整 manifest 使用真实小 Git commit 和合法 snapshot，以支持新增入口，
不修改既有 catalog/queue 断言。

## 限制与剩余闭合

### cycle 1 集中修复（fix-astra-01）

起点 candidate `7eadf67d939332fb471eb8a6a5341b105ba836c87d5688907c17e8b2bbbc2ea8`
与 11 文件 SHA／preimage 均匹配。本轮只增量修改构建器、source facts 测试、README、
本报告和 handoff；其余 6 个候选文件保持字节不变。

| 修复 | 实现与判别性验证 |
| --- | --- |
| FIX-1 | engine.lua 的 section 相对 manifest engine 根解析；测试直接提取未改生产者 resolver，覆盖 `engine/engine/`、`engine/modules/boot/`、`engine/data/`。固定 blob 经 checkout 改写和删除仍相同；错误 path/component/commit/SHA 拒绝，原跨 DLC 隔离测试保留。 |
| FIX-2 | 仅 always_merge 缺省 section 从已绑定条目取得，再查固定 locale 的真实 section；显式冲突拒绝，legacy 分支仍要求原字段。当前生产者真实字典和缺键输入均测试。 |
| FIX-3 | 独立命令用 `xb` 排他创建临时普通文件后替换；CLI 在目标不存在／已有同内容结果两种状态下拒绝输入 symlink、悬空 symlink、FIFO、目录及预存普通临时文件，冻结输入与旧 pack 字节不变。正常命令成功；替换失败注入也保留旧结果并清理本次临时文件。 |
| FIX-4 | 固定 base 的术语路径按 Path 部件排序，与生产摘要 framing 一致；`a-b.tsv` 与 `a-b/c.tsv` 在删除当前术语文件后仍从 base 成功，错误摘要拒绝。 |

**FIX-2 归因更正：**未修改的 `freeze_workset.py:263` 已输出 `locale_section`。
宿主 `probe_always_merge.py` 的五字段字典删掉了此字段，因此“与当前生产者完全同形”
的描述不成立；缺键输入触发 `KeyError` 可以复现，修复仍按授权覆盖该形状。
本轮测试从生产者 AST 取实际字典，并另测缺键变体；未改生产者或伪造其输出。

本轮 `focused-01` 首次运行退出 0：42 tests（source facts 23、SourceFactsChainTests 4、
SourceFactsCompatibilityTests 1、原 ProjectionChainTests 14），耗时 4.005s。
registry、Paseo contract 检查均退出 0。精确命令、环境、退出码见
`.artifacts/i18n/review-speed-p1c-20260912/fix-astra-01/checks.jsonl`。
同目录保留完整日志、HEAD diff、preimage 增量 diff、11 文件 SHA 和精确交付报告。
四项旧实现反例另保存在 `preimage-counterexamples.json` 与 `FIX-*-preimage.log`：
旧映射／locale／术语实现被新测试检出，旧 CLI 返回 0 却改写 victim 并生成 symlink pack；
这些是有意运行的反例，未删除失败日志或降低验收阈值。

17 个原 source facts 测试体及断言保持不变。共享 fixture 唯一形状修正为
`engine/a.lua` → `engine/engine/a.lua`，对应源文件不变，修正真实生产路径而非放宽校验。
F3 仅澄清 README 的元数据前提，缺元数据负例仍失败；不迁移历史证据。
本轮为 EXECUTOR 有界交付，独立最终复审和宿主完整门禁仍待完成；生产省时未测量。

生产省时**未测量**，没有生产吞吐或分钟收益预测。未操作真实 agent、队列、checkpoint、
全历史投影或旧 evidence，未执行完整 17 门禁／严格 build。日志中的 fixture gate PASS
仅证明既有 gate seam 的消费者行为，不是生产门禁通过声明。

本次没有新增运行依赖、数据库、持久缓存、机制推理器或全库 current usages 扫描。
有限入口不自动证明调用链或语义；源码超限直接拒绝，需宿主缩小入口或重新冻结。
已有候选恢复仍由原 batch 生命周期处理，不新增跨所有文件的事务平台；本实现保证所有
声明输入与目标路径在任何 run 写入前验证，底层 I/O 中断仍使用原恢复机制。

独立全候选复审、完整门禁／严格构建、最终 DONE_VERIFIED、生命周期闭合和提交由主代理完成；
本 EXECUTOR 不 stage/commit，不写 `.ai`，不读取 `.ai/consult`。P1-A/B 已在 `d0c4be1` DONE；
P1-C、P2-A、P2-B 依授权顺序完成后自动恢复第 92 批，优化期间翻译继续暂停。
