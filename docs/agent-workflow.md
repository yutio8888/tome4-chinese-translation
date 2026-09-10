# 代理操作与门禁手册

本文件承载任务分流、操作步骤、验证矩阵和完成标准。仓库授权、不变量、外发边界和失败关闭顺序以上位文档 [`AGENTS.md`](../AGENTS.md) 为准；本文件不得放宽这些规则。工具与 Lua 的详细说明见 [`i18n/README.md`](../i18n/README.md)。按任务读取对应章节，无须通读全部操作流程。

## 开始前

明确任务是仅审核、实现还是审核并修复，确定范围、关注维度和完成标准，然后检查工作树：

```bash
git status --short
git diff --name-status
```

首次使用汉化工具环境、依赖或来源配置变化、相关运行失败时执行 `python3 -B tools/i18n doctor`；只读文档任务无需运行。正式流程和完整门禁自身要求的 doctor 仍由其入口执行。

保留任务前改动；需要修改既有脏文件时保存可恢复的 baseline，正式 Paseo 任务按 SPEC 记录。普通有界维护可在任务说明中记录范围和验收，不要求建立 SPEC／PLAN／SCOPE／STATE。

涉及 CRLF、外部仓库或脚本整文件重写时，读取 [`lessons-learned.md`](lessons-learned.md) 的相关条目并检查目标行尾／格式；其他编辑保留现有格式，编辑后检查实际 diff。已读且未变化的资料不重复读取。不得因相邻样式、无关重构或额外质量工程扩大范围。

### 任务分流

| 任务 | 操作入口 |
| --- | --- |
| 只读审查、普通有界维护 | 主代理直接检查或修改，按验证矩阵验收；不自动派发 child |
| 采用 Paseo 的实现或独立复审 | 读取编排契约及实际使用的角色；按任务建立记录 |
| contextual v1／schema 4 implement | 使用下文旧 P2 实现步骤与三阶段收敛；历史任务不迁移 |
| contextual v2 implement | 按 [v2 契约](paseo-translation-context-review-v2-contract.md) 准备与收束，不照搬 v1 的 lane 数和轮次升级规则 |
| WP2-Lite 正式审核 | 按[当前交接](../deprecated/docs/production-review-handoff-2026-09-05.md)和[正式方案](translation-production-review-v2-lite-plan.md)处理 checkpoint、队列、surface／deep、裁决及 evidence；active batch 内不修改译文 |
| WP2-Lite repair | 审核证据已提交且 checkpoint 已移除后运行 `repair preflight`，另建唯一 EXECUTOR 的实现任务；提交译文、repair evidence、catalog 和 migration 后 rebuild queue，successor 等待重新审核 |

有活动 checkpoint 时先按所属流程恢复；不能删除 checkpoint 或新开 writer 来套用另一条流程。

## 审核、修复与停止

先完成一轮只读检查再集中裁决；仅审核任务不得自行进入修复。译文检查源码机制、语境、术语、占位符／markup、运行键和中文表达；代码／工具检查输入、失败语义、下游消费者和实际复杂度；文档／配置核对真实实现与命令。finding 必须有源码或上下文证据并说明可触发行为或调用链；纯风格偏好、理论风险和无证据的性能猜测不算确认问题。

主代理独立把 finding 标为 `confirmed`、`pending` 或 `advisory` 并定级；只有 `confirmed` 可进入已授权修复。仅审核任务不修改；实现或审核并修复任务在已有授权内持续完成，不重复请求修复许可。普通维护由主代理按依赖顺序集中修复；Paseo 任务先冻结 finding 清单，把同一轮全部 accepted 项合并为一次 EXECUTOR 修复 dispatch，明确允许文件、最小测试和完成条件，并复核其输出。

对每轮实际修改按验证矩阵运行最接近的 lint／测试和 `git diff --check`；仅在新变化、失败或未解决的影响链要求时扩大、重跑检查，不对同一轮的每个 finding 逐条重复验证。若待检文件是 untracked，运行 `git diff --no-index --check -- /dev/null <path>` 检查其空白；该命令无需改动 index，可供只读审核使用；`--no-index` 无诊断且退出 1 仅表示文件有差异，空白诊断或读取错误仍须处理。是否需要独立复审取决于用户要求和已采用的任务契约；普通只读检查、小型维护不因此自动启动编排。

### 完成交付与整理

- 只读审查：交付问题位置、影响、证据状态和建议即完成，不要求 findings 清零。
- 实现或审核并修复：范围内验收满足、accepted finding 全部解决、适用验证与复审通过后交付。非阻断 pending／advisory 说明影响即可，不自动扩大任务；影响验收或授权的未决项须给出证据和所需决定，不能报告完成。
- 正式任务：仍须满足所属契约的 `DONE_VERIFIED`、证据、提交／finalize、队列重放及 child 生命周期要求；surface 完成不代表 deep review 或 repair 完成。
- 提交：按任务授权提交范围内文件，核对暂存 diff 与空白；译文和对应证据保持该流程要求的提交边界。只有与本次验收相关的失败才阻断；基线问题不得静默忽略或顺带修复，若正式消费者因此拒绝则按该流程处理。
- 交接与记忆：恢复入口、状态或后续操作变化时更新交接；只把可复用的新结论写入记忆。相关文档可随同一逻辑改动提交，不要求每批另作固定的交接／记忆提交。
- 整理：只清理由本任务创建、已无恢复或核验用途的临时产物；可重生成报告留在忽略目录，人工裁决和不可重生成核验锚点进入受跟踪的 `evidence/`。不整树清理、不删除恢复 checkpoint，不要求用户既有改动或忽略目录清空。

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
[`semantic-claim-runtime-composition-v1.md`](../deprecated/docs/semantic-claim-runtime-composition-v1.md)。关键词扫描
只生成候选，不直接决定 finding 或阻断批次。

`tools/ci-gates.sh` 委托 `tools/ci_gates.py`，统一使用
`tools/i18nlib/gate_results.py` 的检查定义。默认包含严格 addon build；`--skip-build`
适用条件见验证矩阵。每次在 `.artifacts/i18n/ci-gates/run.*/` 生成独立 `results.json` 与逐项
`.log`，按稳定检查 ID、argv、退出码、输出 hash 和时间验证，扩展名不再承载覆盖语义。

批次 `prepare_evidence` 只调用一次统一入口。原 16 项保留，增加 staged whitespace；
doctor、lint、worktree whitespace 不再在外层重复。surface manifest/result 两个消费者
映射到 production-shadow-surface-ledger 分组，contextual result 映射到 contract-suite 的
`test_ai_state_check.load_tests`；coverage 是已有执行的覆盖关系，不是额外执行记录。

新 `gates.json` 使用 schema 2（result、prospective_bytes、committed_bytes），历史 schema 1
仍按原 exact validator 回放。result 绑定完整有序 revision 集合及 batch/catalog/base/policy、
工具 commit/version、实际工作树与 index、配置和检查集。prepare 后半段复用前重新核对
这些绑定及日志 hash；漂移或缺项失败关闭。忽略的 prospective 产物不参与工作树 hash。
不提供跨命令缓存；恢复后的新 prepare 重新执行，不接受环境 marker 跳过检查。

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
源码仍不能支持唯一结论、达到 `max_cycles`，或需要尚未授权的跨批次策略时进入 `WAIT_USER`。普通 accepted
finding 清零且门禁通过后方可收束。

### 子 agent 通知、终态与取消顺序

收到 `notifyOnFinish` 或需判断 child 状态时，读取实时元数据并运行
`git status --short`、`git diff --stat`，按[生命周期契约](paseo-orchestration-v2-contract.md#七托管-child-生命周期与即时归档)
完成取证、harvest、适用的精确清理及归档；通知本身不代表成功。

### 连续批次循环

仅在已授权的连续任务范围内，一批收束后直接开始下一批；到达指定批数、切片边界或暂停点即交付。
WP2-Lite 按任务分流中的正式入口执行；其审核证据必须先提交并 finalize，修复另建任务。

以下步骤只用于旧 P2 的 contextual v1 实现批次，不作为 WP2-Lite 的审核或修复模板：

1. 选定下一个有界切片（按既定推进顺序，规模参照近期批次），并确认它与已完成批次不重叠。
2. 冻结工作集到受跟踪的 `evidence/quality/p2-batches/`，逐条按固定 commit 字节核验英文键，
   记录每个调用的 `args_order`。冻结脚本必须显式传 `tools/i18n context --limit 500`（默认 50
   会静默截断），断言冻结条数等于该 section 的词法 `t()` 调用数，并在核验英文键时同时接受
   原文与转义形式（引擎把换行写成 `\n` 两字符转义）。详见
   [`lessons-learned.md`](lessons-learned.md) 第 12 条。
3. 写 `.ai/task/<task>/SPEC.md|PLAN.md|SCOPE.json|STATE.json`；复用上一批的 envelope builder
   时先改 revision key 前缀。
4. 派发 EXECUTOR → 机械核验 diff 范围与键漂移 → 归档 → 冻结候选 → preflight → 派发独立复审。
5. 按固定源码裁决 observation；一个 cycle 的全部 `confirmed` finding 合并为**一次** fresh
EXECUTOR 修复 dispatch，在同一次运行内按依赖顺序处理，不逐条派发。schema 4 的
   translation implement 任务按下节执行中间 closure 或不确定时的 `RE_REVIEW/full`，收敛后做
   一次最终全量复审。
6. 最终全量复审收敛后按验证矩阵完成门禁覆盖（完整入口已覆盖五步时不重复）→ `ai_state_check.py`
   `DONE_VERIFIED` → 提交译文批次与 evidence；按需更新交接与记忆。
7. 给出批次简报，在已授权范围内进入下一批。

停下条件、以及哪些情况自行处理不必停，见 [`AGENTS.md`](../AGENTS.md) 的「连续批次模式」。
连续运行不豁免本文件的任何门禁或证据要求；批次之间不得为了赶进度合并、跳过或延后门禁。

### 译文三阶段收敛复审（schema 4 implement）

按 [v1 full／closure 记录契约](paseo-translation-context-review-v1-contract.md#schema-4-implement-的记录层-fullclosure-语义)
选择 `REVIEW/full` → `RE_REVIEW/full|closure` → `FINAL_REVIEW/full`；无法确定闭包时选择 full。
cycle／授权上限见[编排契约第一节](paseo-orchestration-v2-contract.md#一设计取舍)，
新建任务与默认收敛规则见 [AGENTS.md](../AGENTS.md#复审收敛下限)。

译文 contextual 复审默认 **2 个并行独立 lane**，`max_cycles` 保持默认 3。4-lane 是升级路径，
不是默认值，只在下列客观条件之一成立时启用，并在 STATE 记录启用理由：两个 lane 对同一
revision 的**一级**缺陷给出实质冲突结论；或批次内容承载可影响玩法的机制描述（数值、时序、
触发条件、目标选择）。维护者对 4-lane 译文审核的 standing authorization 仍然有效：启用
4-lane 时显式设置 `max_cycles=10` 与该 literal。schema 3 及更早任务和 `review_only` 保持原行为。

新建的译文 `implement` 任务一律使用 `schema_version >= 4`，使三阶段收敛复审生效；schema 3
会让每个 cycle 重复全量复审，不得用于新批次。

已被某个 revision 接受的译文只有在缺陷有源码／语境证据时才可 reopen，并按两级收敛阈值分档：

- **一级（阻断级，任何 cycle 均可 reopen）**：fidelity、completeness、terminology、runtime，
  以及 placeholder／markup／newline 不变量。这些都能对固定源码或不变量检查做客观判定，
  两名独立 reviewer 面对同一固定源码应当收敛到同一结论。
- **二级（有界级，只在 `cycle <= 2` 可 reopen）**：grammar、conspicuous translationese。这类
  判断依赖读者语感而非固定源码，多个独立 lane 会持续产出互不相同且互不等价的改写建议，
  不存在收敛点。从 `cycle >= 3` 起，二级缺陷一律只记 advisory，不得进入 accepted finding，
  也不得扩大 closure。

纯偏好变化在任何 cycle 都只记 advisory。二级缺陷若同时构成一级缺陷（例如语法错误已经改变
机制含义），按一级处理，但裁决记录必须写明触发的是哪一条一级依据。

**收敛下限**：某个 cycle 的裁决结果不含任何一级 confirmed finding 时，该批次即视为收敛，
直接进入 `FINAL_REVIEW/full`，不再开新的修复轮。二级 advisory 不阻断收敛。批次靠
`max_cycles` 耗尽而结束属异常路径，必须在批次简报写明未收敛原因。

**已裁定 out-of-scope 的 revision**：ORCHESTRATOR 在 STATE 维护 `declined_scope`，记录被永久
裁定为超出 SPEC 允许编辑面的 revision key 及其客观依据（SPEC 条款或固定源码事实）。该清单
只以「SPEC 边界事实」形式进入 briefing——说明哪些 revision 不在本任务可编辑范围内——不携带
severity、既往 verdict、finding 计数或期待结论，因此不破坏 anchors-only 独立性。对已列入
`declined_scope` 的 revision key 再次提出同类 observation 时直接记 advisory，不重新裁决。

每个 cycle 在 contextual 派发前运行 preflight；修复后运行 strict lint、范围与
source／source_tag／args_order／special／markup／placeholder／newline 不变量检查，以及
`git diff --check`。批次最终门禁只在 `FINAL_REVIEW/full` 收敛后按验证矩阵运行，完整入口已覆盖的五步检查不重复；
任一 per-cycle 检查失败仍须先修复，不能延后到最终门禁。

涉及 evidence-citing candidate 时，先用 `python3 -B tools/review_evidence.py inventory` 从 `.ai/reviews/` 源记录生成原始 finding 清单，再用 `check` 校验 proposer 的 `EVIDENCE-RECONCILIATION.json`；用 `render` 派生计数，不手填 counts。reviewer 仍须直接核对引用和未列出的相关记录。

### 受管 Phase 1 wave

按[受管 Phase 1 wave 契约](paseo-orchestration-v2-contract.md#受管-phase-1-wave)准备 WAVE 与各 task。
该节唯一规定拓扑、单写权限、root map、canonical schema、集合重算、no-change dry-run、
apply caller、final completion 选择、prospective/evidence/publication 与恢复顺序。
`<workspace-root-args>` 对 WAVE 当前每个 workspace ID 各传一个
`--workspace-root WORKSPACE_ID=/absolute/git/worktree/root`。依次执行：

```bash
python3 -B tools/wave_review.py preflight .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

```bash
python3 -B tools/wave_review.py export-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py verify-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py apply-target-patch .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

```bash
python3 -B tools/wave_review.py verify-content-diff .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py prepare-publication .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
# integration EXECUTOR 写入绑定上一命令所报 identity 的唯一 wave evidence
python3 -B tools/wave_review.py publish .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py done .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

先完成各 lane 的外部 `DONE_VERIFIED` 再导出／验证 patch；integration 完整复审和门禁通过后
准备 prospective，由唯一 fresh integration evidence EXECUTOR 写绑定 evidence，再发布并执行 done。
当前工具仅支持 `changes=[]`，不得将 dry-run 报为生产 apply；失败按契约恢复，不修补哈希。

### Production-review shadow 校准

WP1 只用于校准枚举、identity、预算和守恒，不进入连续生产批次。统一用 `python3 -B tools/i18n production` 的 locator/catalog/shadow-policy/shadow-journal/replay/batch-draft/reconciliation 子命令；完整链与参数见 [`translation-production-catalog-queue-v1-plan.md`](../deprecated/docs/translation-production-catalog-queue-v1-plan.md)。shadow marker 必须始终为非权威／不可派发／不可提升；不得 append、取得 ownership、建立 formal epoch 或写译文。受跟踪 immutable snapshot 在 `evidence/production-review/`，schema/policy 在 `i18n/quality/production-review/`，drift/reconciliation report 只在 `.artifacts/i18n/production-review/`。

收束至少运行 production、surface manifest、surface result、translation ledger 四套 focused tests，逐件运行 check/replay/reconciliation，并执行 Paseo contract check 与 `git diff --check`。WP2 必须重新 harvest、完成正式 source locator migration 并建立全新正式 ID 链；不能把 WP1 baseline 改 marker 后复用，也不能引用它作为 parent。正式 ledger CLI 默认以工具仓库 ROOT 和所选 `--root` 的 forbidden set 并集机械拒绝 tracked WP1 shadow provenance；generic library replay 仅保留 legacy 状态机结构验证，`--catalog-manifest` 在 WP2 exact authoritative validator 完成前拒绝所有 catalog，未来 validator 仍须同时应用该 forbidden set。WP2 publication 当前完全不可用；启用前必须实现新的单锁 generation transaction，在同一锁内精确验证并完成 WP1 retirement、父目录 fsync、各 family 与 128 MiB 总预算预检，以及五 family 全部 publication 或恢复。不得用布尔值表示 retirement，也不得把 WP1 per-family publisher 当作该 transaction。

## 验证矩阵

任务开始时按下表确定验证范围；普通维护的依据写在交付说明即可，正式任务写入已有 SPEC。
文档说明的修订与工具行为变更分开判断：纯规则文档修改运行相关契约检查并人工核对语义，不因文档谈及基础设施就运行所有工具测试。

| 任务／实际影响 | 必要验证 |
| --- | --- |
| 只读审查、纯文档修订 | 核对相关事实、链接和命令；改动文件的空白检查；角色或契约修改追加 `python3 -B tools/paseo_contract_check.py` 及权限、流程语义核对 |
| 有界译文修改 | 严格 lint、源码／语境核验、source／source_tag／args_order／special／placeholder／markup／newline 不变量、运行键扫描和分类、空白检查；按采用的契约复审；影响 addon 输出或加载时追加严格构建 |
| 术语数据修改 | 上述适用译文检查，加下节三项术语审计及 LuaJIT 加载后的 source／target／source_tag 有效性核对；涉及全局策略先核对授权 |
| 局部工具行为修改 | 直接相关测试及实际消费者检查；输出、打包或加载路径变化时追加严格构建；未触及的质量研究、队列等测试不自动全跑 |
| 共享流程、身份、证据或发布链路的行为修改 | `tools/ci-gates.sh` 完整检查集，以及受影响的兼容、重放或恢复检查；符合下述条件时可跳过构建 |
| 正式生产批次，包括只写审核 evidence 的批次 | 保留所属消费者要求的完整门禁、严格构建、catalog／queue／evidence 校验、适用复审、`DONE_VERIFIED` 和提交／finalize 后的重放 |

需要独立执行严格核心 addon 构建时使用 `python3 -B tools/i18n build --profile addon --component tome --require-complete`；涉及其他组件或发布 profile 时同时验证实际受影响的产物，不能以核心构建代替。

`tools/ci-gates.sh` 默认含构建。非正式生产批次的任务若可据实际改动证明不影响 addon 输出、打包或加载，可记录依据后使用 `--skip-build`；不用另行请求许可或专门创建 SPEC。正式批次当前要求 full receipt，不接受 `--skip-build`。

同一最终候选的已完成检查不因汇报、交接或提交说明而重跑；输入或相关环境变化、检查失败、覆盖缺失时补充适用检查。正式 `prepare_evidence` 必须由现有统一入口生成并验证绑定结果；恢复后的新 prepare 仍重新执行，不提供跨命令缓存，不伪造或修补 receipt。

## 批次门禁

旧 P2 实现批次须覆盖以下五项；正式生产批次由统一门禁入口覆盖。下列是独立检查命令，完整入口已包含它们时，不在其前后再执行一轮。普通有界维护按上表选择检查。适用检查失败须处理，不得用管道吞掉退出码：

```bash
# 1) 规范译文静态校验
python3 -B tools/i18n lint --strict

# 2) 单元测试
python3 -B tools/test_groups.py --group toolchain

# 3) 跨组件同键多译扫描
python3 -B tools/scan_runtime_collisions.py

# 4) 重复运行键分类
python3 -B tools/classify_runtime_keys.py

# 5) 改动的空白检查（不要求工作树为空）
git diff --check
```

术语批次还须覆盖 `python3 -B tools/audit_static.py`、`python3 -B tools/audit_dynamic.py` 和 `python3 -B tools/annotate_domains.py`；完整门禁已含三项，不再追加执行。报告写入 `.artifacts/i18n/terminology-audit/`。涉及译文运行键时按需读取 [`runtime-key-collisions.md`](runtime-key-collisions.md)。审计与扫描只写入 `.artifacts/i18n/`，不直接改写规范 Lua。

完整门禁、构建与定向检查的选择以本文件验证矩阵为准。空白检查分别覆盖工作树和暂存区（`git diff --check`、`git diff --cached --check`）；任务新建文件按上文检查，不以无输出推断所有 untracked 文件已验证。

## 术语与源码判定

术语读取和疑点登记按 [`AGENTS.md` 的术语库工作流](../AGENTS.md#术语库工作流)执行：主代理首次读取 [`TERMINOLOGY.md`](../TERMINOLOGY.md) 使用规则，再查询 [`terminology/`](../terminology/) 的相关条目；reviewer 按冻结输入契约读取。确实新增或修改高复用术语时，先更新术语库再修改 Lua，不把普通译文修改变成术语库更新任务。保留 source_tag、category 和语境说明，按验证矩阵检查。

翻译、术语或英文表面含义与机制冲突时，对 manifest 固定源版本或 commit 的组件，以该固定源码实际行为为准，并记录组件、公开源码路径、固定 commit 和关键调用或数据定义；对源码仓库、commit 或版本未固定的 DLC，不得声称存在固定源码或 commit，应记录实际获授权的公开源码证据并明确标注来源未固定；证据不足时，将来源或机制结论标为待确认。
