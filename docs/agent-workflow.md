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

### 机制 claim 与运行时组合

遇到下列任一客观条件时，必须为相关数值 placeholder 建立 directional value-flow 记录，而不能先
凭作者判断它是否属于复合机制：quantity kind 为 damage／heal／shield；同句数值与 duration
共现；中文新增英文没有的 scope／时序／触发限定；数值经过 DamageType、timed effect、projector
或等价运行时层；reviewer 或 lint 对 scope 提出冲突。每个数值 placeholder 至少记录 index 和
quantity kind，不能可靠分类时写 `unknown`。

新增或修改受跟踪 claim、anchors-only briefing 或 runtime composition fixture 后运行：

```bash
python3 -B tools/i18n claims check \
  --registry evidence/quality/semantic-claim-regressions-v1.json \
  --strict
```

exact schema、directional anchor、结构化 decomposition、完整句重渲染和来源固定规则见
[`semantic-claim-runtime-composition-v1.md`](semantic-claim-runtime-composition-v1.md)。关键词扫描
只生成候选，不直接决定 finding 或阻断批次。

`tools/ci-gates.sh` 的 semantic claim 两步使用 `*.out`，而非 `*.log`。这是因为既有
`tests/i18n/test_toolchain.py` 会对门禁产生的 `*.log` 集合做精确相等断言，而该测试不在本任务
allowlist；新增 gate 因而不受该 frozen exact-log contract 覆盖，不借此扩大修改范围。

数值 claim 与 anchors-only briefing 都必须填写 `args_order=null` 或 source placeholder 的完整排列，
并保持 target/candidate target 的完整 raw-token permutation；`placeholder_index` 始终按 source 顺序
绑定。数值 claim 必须同时填写 source/target explicitness；target 更明确时只能在非 pending 且所有 required
anchor 固定的情况下显式 justification，没有增加明确度时 justification 必须为 false。固定分解还要
声明适用条件；已有 timed effect 会触发 merge 时，不得把仅 `effect_absent` 成立的 tick 分布写成
unconditional。runtime composition 必须为每个运行时表面 variant 登记非空、含 required 项的
anchors，按适用性分列 call-site、helper 与 locale 来源，并冻结其全部组合的完整句。

Paseo 激活时，EXECUTOR 仍是任务内容与 adjudicated evidence 的唯一写入者；REVIEWER 只读并从
anchors-only briefing 独立重建，不接收预填 scope、components、tick count、total 或期待 verdict；
ORCHESTRATOR 核验源码、裁决 finding 并写编排／review record。required anchor 未固定或数据流
无法闭合时，自行降级为 `pending`，采用不比英文更明确的保守中文，不自动进入机制性改写，并在
批次简报记录。首次同 revision 的高风险字段分歧进入正常 FIX／RE_REVIEW；重复实质分歧、固定
源码仍不能支持唯一结论、达到 `max_cycles`，或需要跨批次策略时进入 `WAIT_USER`。普通 accepted
finding 清零且门禁通过后方可收束。

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
   记录每个调用的 `args_order`。冻结脚本必须显式传 `tools/i18n context --limit 500`（默认 50
   会静默截断），断言冻结条数等于该 section 的词法 `t()` 调用数，并在核验英文键时同时接受
   原文与转义形式（引擎把换行写成 `\n` 两字符转义）。详见
   [`lessons-learned.md`](lessons-learned.md) 第 12 条。
3. 写 `.ai/task/<task>/SPEC.md|PLAN.md|SCOPE.json|STATE.json`；复用上一批的 envelope builder
   时先改 revision key 前缀。
4. 派发 EXECUTOR → 机械核验 diff 范围与键漂移 → 归档 → 冻结候选 → preflight → 派发独立复审。
5. 按固定源码裁决 observation；`confirmed` 进 fresh EXECUTOR 修复。schema 4 的
   translation implement 任务按下节执行中间 closure 或不确定时的 `RE_REVIEW/full`，收敛后做
   一次最终全量复审。
6. 最终全量复审收敛后运行五步门禁 + 适用的完整门禁 → `ai_state_check.py`
   `DONE_VERIFIED` → 单独提交译文批次与
   evidence；交接与记忆随后单独提交。
7. 给出批次简报，直接进入下一批。

停下条件、以及哪些情况自行处理不必停，见 [`AGENTS.md`](../AGENTS.md) 的「连续批次模式」。
连续运行不豁免本文件的任何门禁或证据要求；批次之间不得为了赶进度合并、跳过或延后门禁。

### 译文三阶段收敛复审（schema 4 implement）

仅当 `schema_version >= 4`、`mode=implement` 且含 `translation_contextual_v1` 时启用：首轮
`REVIEW/full` 冻结完整有序工作集；中间修复轮只复审 changed target、open finding、共享
runtime key、叙事／术语 claim 和额外触及 target 的确定性依赖闭包；收敛后以
`FINAL_REVIEW/full` 对最新候选完整复审一次。闭包或 parent 不确定时直接使用
`RE_REVIEW/full`，不得猜测子集。

changed+dependency closure 由 ORCHESTRATOR 根据任务 diff、finding 与批内依赖确定，不新增
dependency graph、closure manifest 或其他 artifact。`ai_state_check.py` 只验证 review 记录与
七键 envelope 的 cycle／phase、parent、顺序、source 和 inclusion 自洽，不能替代 closure
完整性的编排判断；任何歧义都必须回退 full。强制 `FINAL_REVIEW/full` 是该轻量优化的
correctness backstop，不能由 closure 记录替代。
若一次 `FINAL_REVIEW/full` 失败，可在更高 cycle 完成 `RE_REVIEW/full|closure` 修复序列后再次
执行 final full；历史失败记录保留在顺序中，最新 terminal 仍必须是 STATE.cycle 的成功
`FINAL_REVIEW/full`。

新 STATE 的 `max_cycles` 默认 3，且 `cycle <= max_cycles`。只有用户明确授权时才可把上限设为
3 以上，并逐字保存 `max_cycles_user_authorized=true`；该轻量字段不记录授权文本或另建审批
artifact。维护者已为 4-lane 译文审核给出 standing authorization：此类任务创建时显式设置
`max_cycles=10` 和该 literal；2–3 lane 仍保持默认 3。schema 3 及更早任务和 `review_only`
保持原行为。

已被某个 revision 接受的译文只有在 fidelity、completeness、grammar、terminology、runtime
或 conspicuous translationese 缺陷有源码／语境证据时才可 reopen。纯偏好变化只记 advisory，
不得进入 accepted finding，也不得扩大 closure。

每个 cycle 在 contextual 派发前运行 preflight；修复后运行 strict lint、范围与
source／source_tag／args_order／special／markup／placeholder／newline 不变量检查，以及
`git diff --check`。五步门禁和完整 `tools/ci-gates.sh` 只在最终 `FINAL_REVIEW/full` 收敛后运行；
任一 per-cycle 检查失败仍须先修复，不能延后到最终门禁。

涉及 evidence-citing candidate 时，先用 `python3 -B tools/review_evidence.py inventory` 从 `.ai/reviews/` 源记录生成原始 finding 清单，再用 `check` 校验 proposer 的 `EVIDENCE-RECONCILIATION.json`；用 `render` 派生计数，不手填 counts。reviewer 仍须直接核对引用和未列出的相关记录。

### 受管 Phase 1 wave

并行只在 [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md) 的受管 wave
契约已经启用时执行。一个 wave ORCHESTRATOR 必须直接拥有 2–4 条 lane（默认 2 条）及 integration 的全部
child；每条 lane 使用不同 workspace，child dispatch 的 `workspace_id` 等于所属 task STATE，
并同时持久化与 WAVE／STATE 一致的 `task_id`、`parent_agent_id` 和非空 `purpose`，不得只信
`lineage_verified=true`，每个 child 的 `agent_id` 还必须不同于 wave ORCHESTRATOR，且不得创建 lane-orchestrator。ORCHESTRATOR 只写 ignored 编排记录；lane／integration 任务内容和
唯一 wave evidence 只能由各自 lineage 核验的 EXECUTOR 写入，只读角色不得改变 workspace。

派发前以 `WAVE.json` 为唯一入口运行：

```bash
python3 -B tools/wave_review.py preflight .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

`<workspace-root-args>` 必须对 WAVE 当前引用的每个 workspace ID 各包含一个
`--workspace-root WORKSPACE_ID=/absolute/git/worktree/root`。工具要求键集合 1:1、不同 ID 指向
不同真实 worktree、全部 root 共享同一 Git common-dir，并在 lane／integration 所属 root 内独立
做 escape／symlink 检查；root workspace 的同名影子文件不参与核验。

preflight 必须重算 pinned-manifest primary、workset／SCOPE／collateral 的等值关系、
`ordinary_non_collateral_paths=[]`、授权 remainder、三类集合 identity 与 pairwise intersection。
每条 lane SPEC 必须含独占一行的 `phase1_collateral: forbidden`。任何声明为空而重算非空、path
escape／symlink、identity 漂移或集合冲突都不得 DISPATCHED。
workset 必须非空；调用须由固定 manifest 与仓库 LuaJIT loader 在 `base_commit^{tree}` 和所属
lane 当前译文逐条唯一解析。runtime keys 从 `(source, source_tag)` 重建；本 dry-run 的
term/narrative 集合从每个 ordered revision key 重建为明确的 `narrative_closure` 依赖键，不能
自报空集合。

lane 外部 `DONE_VERIFIED` 后按冻结 queue 导出和验证 patch：

```bash
python3 -B tools/wave_review.py export-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py verify-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py apply-target-patch .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

当前 Phase 1 实现只支持 no-change dry-run 的 `changes=[]`：首次 apply 仍要求 HEAD commit 等于
`base_commit`，index tree 与 tracked worktree tree 等于 `base_commit^{tree}`，且无任务内容
dirty／untracked；verify/apply 只接受合法 `INTEGRATING` WAVE，并要求每条 lane 的实际 STATE
持久化为 `DONE`、`ai_state_check` 返回 `DONE_VERIFIED`、唯一 final full completion record 与
dispatch/envelope 绑定且全部 child 已归档。工具按完整 merge queue 核验空 patch；每个 candidate
target 必须等于固定 base target 和 lane 当前 target，不能因 `changes=[]` 丢弃变化。非空 patch 一律 fail closed，不能把此
结果报告为生产 apply。

此外，每条 lane 的全部 `translation_fix_paths` 必须逐文件字节等于 `base_commit`，因此 workset
之外的 call／target 或其他文件字节漂移也会失败。apply 在处理 lane patch 前先核验 integration
task-derived STATE／SPEC／SCOPE、task／workspace／共同 orchestrator、唯一 translation+evidence
allowed-files union，以及恰好一个 lineage／`purpose=integration_apply` 绑定的 integration
EXECUTOR dispatch；实际调用进程还必须提供与该唯一记录 `agent_id` 相同的非空
`PASEO_AGENT_ID`，缺失、不等或由 `integration_fix` 冒充均失败关闭。

integration 的 final full envelope 必须按 MERGE-QUEUE 顺序精确合并每条 lane 的完整 workset 与
最终 envelope：ordered keys、source、target、context 全部逐项 1:1，并由 integration 当前译文
重新解析 target。`fixed_source_identity` 必须从 `base_commit` 固定字节的 manifest 按 public
commit／protected snapshot 机制重建；integration 的 terminology snapshot 与 briefing 按编排契约
规定的 canonical JSON recipe 从 queue 顺序、lane 冻结输入和 integration 实际 snapshot
确定性重渲染。空值或任意重算 payload identity 不能替代这些 provenance。lane 与 integration 的
final full review 还必须跨 `review_records`／`senior_review_records` 的合法 review phase 唯一指向
最大 `(cycle, attempt)` full completion；更新的 `CHANGES_REQUIRED` 也参与最大值并阻断 closure，
最大 tuple 平局、歧义或指向旧 completion 都失败关闭。

integration 完整复审和门禁通过后，先冻结 prospective DONE WAVE，再由唯一 fresh、归档确认的
`purpose=wave_evidence` integration EXECUTOR 写 evidence；该 dispatch 必须绑定唯一 evidence path
和 prospective identity，且不得复用 apply／fix agent ID。随后原子发布完全相同的 WAVE bytes，
最后运行：

```bash
python3 -B tools/wave_review.py verify-content-diff .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py prepare-publication .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
# integration EXECUTOR 写入绑定上一命令所报 identity 的唯一 wave evidence
python3 -B tools/wave_review.py publish .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py done .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

`prepare-publication` 在 GATED 状态冻结或复用 prospective；`publish` 在发布前重验 prospective、
evidence identity 与 translation hashes，并原子发布完全相同 bytes。prospective 缺失时只可从
唯一 GATED 绑定确定性重建；evidence 缺失时停下等待 integration EXECUTOR；已发布时重复
`publish` 幂等；identity／bytes 不一致一律失败关闭。`done` 只做发布后 closure，并复用
`ai_state_check` 验证每个 lane／integration STATE，追加 task workspace、共同
orchestrator、禁止 lane-orchestrator、child agent 不跨 task 复用、prospective／publication
字节全等、evidence binding、translation-only hash 未漂移及唯一 allowed-files 的最终 diff
closure。其 `DONE_VERIFIED` 只作为外部结果，不写回 WAVE。恢复时只续做缺失步骤：已有
prospective 就不重算，已有 evidence 就先核验引用再发布，已发布 WAVE 就只重跑 closure；字节或
identity 不一致时进入 `WAIT_USER`。
integration 的全部 `translation_fix_paths` 也必须逐文件字节等于 `base_commit`，且
`integration-content-diff/1.changed_paths` 与 `entries` 必须同时严格为空。

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
