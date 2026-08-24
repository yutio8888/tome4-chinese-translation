# 代理操作与门禁手册

本文件只承载操作步骤和命令。仓库授权、不变量、外发边界、失败关闭顺序和门禁触发条件以上位文档 [`AGENTS.md`](../AGENTS.md) 为准；本文件不得放宽这些规则。工具与 Lua 的详细说明见 [`i18n/README.md`](../i18n/README.md)。

## 开始前

明确任务是仅审核还是审核并修复，冻结范围、关注维度和完成标准，然后记录：

```bash
git status --short
git diff --name-status
python3 -B tools/i18n doctor
```

保留任务前改动；需要修改既有脏文件时，先按任务 SPEC 保存可恢复的 baseline。翻译、术语或工具行为变更的外发与审核路由仍须按 [`AGENTS.md`](../AGENTS.md) 执行。

修改外部仓库或已有版本控制文件前，先阅读 [`docs/lessons-learned.md`](lessons-learned.md)；编辑后运行 `git diff --stat`，检查行尾或缩进噪音。不得因相邻样式、无关重构或额外质量工程扩大范围。

## 审核、修复与停止

先完成一轮只读检查再集中裁决；仅审核任务不得自行进入修复。译文检查源码机制、语境、术语、占位符／markup、运行键和中文表达；代码／工具检查输入、失败语义、下游消费者和实际复杂度；文档／配置核对真实实现与命令。finding 必须有源码或上下文证据并说明可触发行为或调用链；纯风格偏好、理论风险和无证据的性能猜测不算确认问题。

主代理独立把 finding 标为 `confirmed`、`pending` 或 `advisory` 并定级；只有 `confirmed` 自动进入修复。只有用户要求修复时才修改：先冻结 finding 清单，按依赖顺序处理 accepted 项，给修复 agent 明确 finding、允许文件、最小测试和完成条件，并复核其输出与测试结果。

每个修复运行最接近的 lint／测试和 `git diff --check`；一批修复后运行组件级检查；收束时运行适用的完整门禁、构建和 smoke。审核并修复任务只有在 accepted finding 全部解决、门禁通过并完成新的独立复审后交付；只剩 pending/advisory 时说明并停止。

### 子 agent 状态取证（宣布挂起或取消之前）

委托给子 agent 时，传输状态面的字段可能过期，单一 `status` 不足以判定终态。宣布挂起、
调用 stop／cancel 或写下任何故障归因之前，按顺序取证：

```bash
# 1) 重新查询一次实时状态：除 status 外读 attentionReason／attentionTimestamp 与 activeTurn
#    activeTurn 为空 = 没有进行中的运行 = 已结束，不是挂起
# 2) 检查工作树：未产出改动的 EXECUTOR 留下空 diff
git status --short
git diff --stat
```

只有重新查询后仍确认有进行中的运行且无进展，才按挂起处理。字段长时间未更新本身不是挂起
证据。跳过工作树检查而得出的故障结论无效，必须撤回并更正记录。

EXECUTOR 结束却没有工作成果（无 diff、无报告，或只回了计划／进度说明）时，该次 dispatch
输出无效：先归档，再创建 fresh retry；不得向已结束的 child 发送 follow-up 续跑。

### 连续批次循环

译文复核默认连续运行，不逐批等待批准。一批收束后按下述顺序直接开始下一批：

1. 选定下一个有界切片（按既定推进顺序，规模参照近期批次），并确认它与已完成批次不重叠。
2. 冻结工作集到受跟踪的 `evidence/quality/p2-batches/`，逐条按固定 commit 字节核验英文键，
   记录每个调用的 `args_order`。
3. 写 `.ai/task/<task>/SPEC.md|PLAN.md|SCOPE.json|STATE.json`；复用上一批的 envelope builder
   时先改 revision key 前缀。
4. 派发 EXECUTOR → 机械核验 diff 范围与键漂移 → 归档 → 冻结候选 → preflight → 派发独立复审。
5. 按固定源码裁决 observation；`confirmed` 进 fresh EXECUTOR 修复，重新冻结后全量复审，直到干净。
6. 五步门禁 + 适用的完整门禁 → `ai_state_check.py` `DONE_VERIFIED` → 单独提交译文批次与
   evidence；交接与记忆随后单独提交。
7. 给出批次简报，直接进入下一批。

停下条件、以及哪些情况自行处理不必停，见 [`AGENTS.md`](../AGENTS.md) 的「连续批次模式」。
连续运行不豁免本文件的任何门禁或证据要求；批次之间不得为了赶进度合并、跳过或延后门禁。

涉及 evidence-citing candidate 时，先用 `python3 -B tools/review_evidence.py inventory` 从 `.ai/reviews/` 源记录生成原始 finding 清单，再用 `check` 校验 proposer 的 `EVIDENCE-RECONCILIATION.json`；用 `render` 派生计数，不手填 counts。reviewer 仍须直接核对引用和未列出的相关记录。

## 批次门禁

译文每批按以下顺序运行，任何失败都必须先修复，不得用管道吞掉退出码：

```bash
# 1) 规范译文静态校验
python3 -B tools/i18n lint --strict

# 2) 单元测试
python3 -m unittest -q tests/i18n/test_toolchain.py

# 3) 跨组件同键多译扫描
python3 -B tools/scan_runtime_collisions.py

# 4) 重复运行键分类
python3 -B tools/classify_runtime_keys.py

# 5) 工作树整洁度
git diff --check
```

术语批次在上述五步之后额外运行 `python3 -B tools/audit_static.py`、`python3 -B tools/audit_dynamic.py` 和 `python3 -B tools/annotate_domains.py`；报告写入 `.artifacts/i18n/terminology-audit/`。涉及译文审核时遵循 [`docs/runtime-key-collisions.md`](runtime-key-collisions.md)。审计与扫描只写入 `.artifacts/i18n/`，不直接改写规范 Lua。

翻译、术语或工具行为变更收束时运行 `tools/ci-gates.sh`。只有任务 SPEC 证明不影响 addon 输出或构建时才可使用 `tools/ci-gates.sh --skip-build`；工作树未变化时不重复运行长门禁；纯文档任务只运行相关文档／契约检查和 `git diff --check`。

## 术语与源码判定

开始翻译或审校前阅读 [`TERMINOLOGY.md`](../TERMINOLOGY.md) 和 [`terminology/`](../terminology/)。术语或专名疑点只能在审核 observation 产生后按 claim 核验；不得用术语库覆盖源码事实。新增或修改高复用术语时，先更新术语库，再修改 Lua；保留 `t(...)` 第三个参数的 `source_tag`，填写 `T.*` category，并在不同语境下于 `notes` 说明。修改术语后用 LuaJIT 加载翻译文件检查 `source`、`target` 和 `source_tag`。

翻译、术语或英文表面含义与机制冲突时，对 manifest 固定源版本或 commit 的组件，以该固定源码实际行为为准，并记录组件、公开源码路径、固定 commit 和关键调用或数据定义；对源码仓库、commit 或版本未固定的 DLC，不得声称存在固定源码或 commit，应记录实际获授权的公开源码证据并明确标注来源未固定；证据不足时，将来源或机制结论标为待确认。
