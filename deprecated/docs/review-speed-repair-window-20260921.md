# Repair window 与投影复用实现说明（2026-09-21）

## 目标与边界

本次只改变同一进程、同一 repository root、同一 HEAD 下的投影分组与修复调度，不改变 durable evidence、
workset、migration 或 SQLite 的权威关系。standalone CLI 保持可用并是失败恢复入口；没有跨进程缓存、持久
信任层、自动 commit/rebuild 或并发 writer。

`repair_preflight` 先取得一次当前投影，把同一对象交给 `strict_check` 和 repair winner 构建。复用前再次解析
HEAD；HEAD 漂移直接拒绝。current winner、历史 batch、live translation preimage、catalog manifest、SQLite
business rows 等原验证仍执行，SQLite 仍只是可重建投影而不是证据权威。

新 `tools/orchestration/run_repair_steps.py` 提供两个有界入口：

- `preflight`：1–3 个互异来源 batch，各自执行真实 CLI preflight、各自保留原 schema workset；
- `migration-chain`：严格执行真实 CLI plan、check、apply，apply 后结束。

所有路径参数先检查；正式输出及既有 writer 使用的固定 `.<name>.tmp` 临时名 fresh 且全串互不碰撞。首次
step 失败不再运行后续 step，前步文件和事务结果保留，可回到 standalone CLI 恢复。wrapper 输出和固定
临时名不得位于 `.artifacts/i18n/production-review-v2-lite/` 可变状态目录的任何位置，避免碰触 queue、
checkpoint、lock 或 SQLite sidecar。每一步仍重新读取
候选/输入、获取自身 writer lock、验证 SQLite；carry scope 只
复用纯 Git evidence projection，且以 root+HEAD 为键。

## 计时口径

每次入口必须提供 fresh `--timing-output`。fresh 由开始前和最终 timing 写入前的拒绝检查保证，底层写入仍沿用
既有临时文件加替换协议；这里不宣称对未授权并发进程提供超出该协议的原子保留。报告记录每步
`perf_counter` wall time、exit code、总 elapsed、
success/failure step，以及真实 `_projection` 的调用数、总 wall time和逐次样本。包装函数总是调用原实现，
并在 `finally` 计时；因此失败投影也会被计数。该报告是忽略目录中的观测产物，不是 evidence、checkpoint
或恢复权威。

timing 写入失败与业务结果隔离：stderr 列出已经完成的业务步骤，明确产物或 SQLite 变更可能已落地且不得
盲目重跑；原业务非零 exit 保持不变，原异常继续抛出。只有业务全部成功而 timing 写失败时返回专用 exit 9。

fixture 验收固定生成时间后比较 workset/migration exact bytes，并比较 SQLite business/meta rows；时间只
断言为实际非负样本，不设虚构性能阈值。生产 baseline/candidate 各一次同 HEAD 实测由主代理在其已隔离的
旧/新代码进程中完成，本 EXECUTOR 不运行主仓库 production 投影。主代理记录的旧实现拒绝路径 baseline 为：
同一历史 batch 因部分 repair rows 已非 current winner 而正确拒绝，2 次真实投影约 210.35 秒和 210.91 秒，
总墙钟 423.89 秒，queue/checkpoint 未变。候选验收要求在相同输入上保持同一拒绝和零 workset，并把投影降为
1 次；不得放宽 winner 校验来制造生产成功样本，正向成功只由临时 Git/SQLite fixture 证明。

## Fixture 验证记录

2026-09-21 在临时 Git/SQLite fixture 上运行：

```text
python3 -B -m unittest tests.i18n.test_production_review_v2_lite_migration tests.i18n.test_repair_steps tests.i18n.test_test_groups
52 tests, 5.436s, OK

python3 -B -m unittest tests.i18n.test_production_review_v2_lite_queue.ProjectionChainTests
14 tests, 1.499s, OK
```

断言覆盖 standalone preflight 1 次投影、两个合法来源 workset exact bytes 等价且 N→1、migration
plan/check/apply exact artifact 与 SQLite/meta 等价且 3→1、current winner/live preimage/HEAD/lock 拒绝、输入/
候选/SQLite 步间漂移、失败后保留前步产物并停止，以及正式输出与其他输出固定临时名的全串碰撞预检。
新增回归还覆盖 production 可变状态目录对 preflight/migration-chain 的调用前拒绝，以及 timing 写失败时保留
业务返回码、原异常和“业务成功但计时失败”的专用 exit 9。
fixture 的秒数只记录本次测试墙钟，不外推生产收益。

## 三批 / 20 revision 窗口

审核最多连续三批。新增 confirmed 且可执行的 repair revision 去重累计达到 20，或出现机制/运行/placeholder
等高影响 finding 时，在当前批 finalize 且无 checkpoint 的边界提前修复。来源 batch 分别 preflight 后，
一个 IMPLEMENT 任务显式冻结来源、revision 和获准同族范围；完整复审/门禁后集中提交翻译，只构建一次
catalog/migration。实际顺序为：译文 commit → 计时 queue rebuild → catalog build → migration-chain → 必要
repair evidence commit → 再次计时 queue rebuild；第一次同步 translation HEAD 供 migration strict check 使用，
第二次同步 evidence HEAD，两次都不能省略。无可执行项不创建空窗口；历史术语/口径 pending 单列报告且不计阈值。

首轮执行审核 242–244（达到阈值或高影响 finding 时提前收束）及其必要修复窗口。完成后原宿主暂停并回报
当前主代理以收集测量；这个暂停是操作节点，不要求用户再次批准，主代理可在既有连续审核授权范围内根据结果
继续安排。报告同时包含审核与修复耗时、投影/门禁耗时、提交、积压、未决和失败恢复，不能只凭审核侧样本
宣称端到端收益。
