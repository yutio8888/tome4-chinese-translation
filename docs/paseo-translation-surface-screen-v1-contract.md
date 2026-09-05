# Paseo 译文表层筛查契约 v1（translation_surface_screen_v1）

版本 `translation-surface-screen/1.0`。本契约只绑定 `role=reviewer`、
`purpose=translation_surface_screen_v1`、当前 task/workspace/direct parent lineage 和冻结输入；
REVIEWER 全程只读。本契约实现
`docs/translation-review-production-convergence-spec.md` 中 surface-screen 任务的最小生产
pilot 闭环，不复用也不改写 `translation_contextual_v1`／`translation_contextual_v2` 的
terminals、stages、`DONE` 语义或 completion 记录；同一 task 不得把本契约与任一语境审核
契约混用。筛查结果只产 `OK|ISSUE` observation，不得升级为 adjudicated finding 或修复指令；
`OK` 也不得宣称 deep review 或 repair 完成。

## 一、版本与身份

使用本契约的 task 使用 `review_contract=translation_surface_screen_v1`、
`labels.purpose=translation_surface_screen_v1` 和 `schema_version >= 5`，任务 `mode` 只能是
`review_only`（deep／repair 是生产 SPEC 中另行的独立 task）；每次失败或无效输出
的重试都创建 fresh child，保持 role、purpose、workspace、parent lineage 与冻结输入字节，
并分配新的 dispatch_id 与 agent_id。dispatch ID、group ID 与 task ID 必须是文件名安全
identifier（dispatch/group `^[0-9a-z][0-9a-z-]{0,31}$`，task `^[0-9a-z][0-9a-z-]{0,127}$`），
任何 stage 的 envelope/raw/manifest 路径都必须由它们精确推导。身份只绑定冻结的筛查
bundle，不绑定运行时
provider/model/mode/thinking；任何阶段都禁止从 provider 或 model 名称推断覆盖、稳定性或
完成度。四 lane 必须同组重试，旧 attempt 不补写 completion record。

## 二、双层 entry 身份与 canonical bytes

canonical JSON bytes 使用 UTF-8、`ensure_ascii=false`、递归 key 排序、紧凑分隔符、
`allow_nan=false`；identity bytes 不含尾随换行，仅落盘 artifact 允许一个尾随换行。

每个 entry 的稳定主键是逻辑身份，版本化 revision 在其之下：

~~~text
logical_entry_identity = SHA-256(canonical({schema_version:1, component, normalized_path, call_locator, source_tag}))
rules-v1/其他既有规则：
entry_revision_identity = SHA-256(canonical({schema_version:1, logical_entry_identity, source_sha256, target_sha256, fixed_source_identity, terminology_snapshot_sha256, rules_version}))
production-review-v2-lite-rules-v2：
entry_revision_identity = SHA-256(canonical({schema_version:1, logical_entry_identity, source_sha256, target_sha256, fixed_source_identity, rules_version, args_order}))
~~~

其中 `source_sha256`／`target_sha256` 是 source/target 冻结字符串 UTF-8 bytes 的 SHA-256，
`terminology_snapshot_sha256` 是 payload `terminology_snapshot` 字符串 UTF-8 bytes 的
SHA-256。identity recipe 只由 exact `rules_version` 确定；`production-review-v2-lite-rules-v2`
仅从 revision recipe 排除全局术语 snapshot，payload/envelope 仍必须记录并按 exact 当前值验证
该 snapshot provenance。rules-v2 的 `args_order` 是 `null` 或非空的整数 permutation（恰为
`1..n` 的一次排列），并同时作为 catalog risk 数据和 revision identity 输入；只改该值也必须
重新审核。其他既有 rules 字符串保持历史配方，因而 v1 live/history bytes 可按原式重验。任何 locator／`source_tag` 变化都会产生新的 logical_entry_identity，必须以显式
migration edge（ledger 记录 `migration_from_logical_entry_identity`）进入新逻辑身份；
source、target、固定源码 identity 或 rules_version 变化在 logical_entry_identity 不变的前提下
产生新 revision；术语 snapshot 变化只在历史配方下改变 revision；`source_tag` 属于逻辑身份。

约束：

- 路径必须是仓库相对 POSIX 路径，非空、normalized，且不得含 `.`／`..` 段、空段、
  绝对路径、边缘分隔符、反斜杠或 NUL；
- `call_locator` 是 extractor-stable revision key，禁止用裸行号（纯数字或 `L`／`line`
  前缀的行号形式）替代，也不得形如 entry `normalized_path` 后接数字行号 token
  （`<path>/<line>`、`<path>.<line>`、`<path>:<line>`）；与 entry 路径无关的层级数字 key
  （如 `3/2/1`）仍有效；缺字段、canonical 失败或 identity 不匹配一律 fail closed；
- `fixed_source_identity` 仅为 `commit:<40 lowercase hex>` 或 `snapshot:<64 lowercase hex>`，
  form 由来源机制决定，与语境契约相同；
- `rules_version` 为非空字符串；`source`／`target` 非空；`source_tag` 可为空字符串；
- rules-v1 entry 的 canonical 表示恰含 `logical_entry_identity`、`entry_revision_identity` 与六个
  语义字段；rules-v2 另恰含 `args_order`，共七个语义字段。两个 identity 都必须能由对应
  rules-version 的语义字段按上式重算，否则拒绝。

payload 恰含六键：`contract`（精确 `translation_surface_screen_v1`）、`entries`、
`fixed_source_identity`、`terminology_snapshot`、`rules_version`、`rendered_briefing`。
`entries` 必须按 canonical `entry_revision_identity` 的稳定字节序严格递增且唯一；空
`entries` 拒绝（n=0 不 dispatch）。`rendered_briefing` 不得嵌入任何 64 位 identity。
`candidate_identity`（screen identity）为 `SHA-256(canonical payload bytes)`；envelope 恰含
`candidate_identity` 与 `payload`。

## 三、batching、carry-over 与 lane manifest

设 n 为冻结并按 canonical `entry_revision_identity` 排序后的 entry 总数：

- `n=0`：不 dispatch，记录零项结果；
- `1≤n≤3`：一个 `full` 成员覆盖全部 n 项，权威 artifact 为
  `.ai/task/<task_id>/SURFACE-SCREEN-ENVELOPE-<dispatch_id>.json`；
- `4≤n≤80`：以 `q=floor(n/4)`、`r=n mod 4` 切成四个连续 lane；前 r 条 lane 长度为 q+1，
  其余为 q；不得空 lane，四 lane 的有序并集必须精确等于 screen 集合；
- `n>80`：fail closed；必须先用 `split_carry_over` 在 manifest 构造之前形成 stable
  carry-over（排序后前 80 项进本批 screen，其余按相同顺序保留给下一批并优先处理），
  carry-over 绝不得记为完成。切分必须落盘为 canonical pre-manifest artifact
  `.ai/task/<task_id>/SURFACE-SCREEN-CARRY-OVER.json`：恰含 contract、task_id、algorithm
  （`surface-carry-over/1`）、`original_count`、`screen_count=80`、`carry_over_count`、按序
  `ordered_screen_entry_revision_identities` 与 `ordered_carry_over_entry_revision_identities`；
  两个有序数组的拼接必须逐项等于原始冻结排序，两组不得相交，本批 manifest 的 screen 集合
  必须精确等于 artifact 记录的 first-80 集合；DONE 同时要求 STATE 以统一的
  `surface_screen_input_path` 绑定实际冻结输入 draft（canonical compact bytes），重跑
  strict validator 证明拼接逐项等于该输入，任何计数篡改、overlap、omit 或 extra 一律 fail
  closed；draft 超过 80 项时该 carry-over artifact 是强制绑定，删除 carry 绑定绝不能把
  n=85 冒充为整屏 n=80。

lane 模式的权威 artifact 为 `.ai/task/<task_id>/SURFACE-SCREEN-GROUP-<group_id>.json`，外层
恰含 `group_identity`、`payload`；`group_identity` 是 payload canonical bytes 的 SHA-256。
payload 恰含 `contract`（精确 `translation_surface_screen_v1_lane_group`）、task/group ID、
`review_phase`（仅 `REVIEW`；surface 的 fresh retry 以更高 attempt 换新 dispatch/group IDs，
从不出 `RE_REVIEW`）、cycle、attempt、`lane_count=4`、完整 workset
（恰含 `entries`、`fixed_source_identity`、`terminology_snapshot`、`rules_version`、
`rendered_briefing`）、`lane_boundaries` 和 `lanes`。每条 lane 恰含 `index`、`dispatch_id`、
`input_path`、`candidate_identity`；lane envelope 的 payload 与 workset 仅 `entries` 切片
不同，因此四条 lane briefing 字节相同且 lane-neutral。validator 必须证明 indices 1..4、
正长度、q/r 平衡、无 gap/overlap、尾端等于 n，以及四个 envelope 切片的 ordered union
精确等于 workset；manifest、envelope、dispatch、record 四方 identity/path/index 必须相等。

## 四、STATE、raw evidence 与 terminal predicate

解析前把 exact returned bytes 保存为 `.ai/reviews/<task_id>/raw-<dispatch_id>.txt`。每个
接受的 record 写同一路径及 exact bytes 的 `raw_output_sha256`；路径由 task/dispatch 精确
推导，必须是 workspace 内 ordinary non-symlink file。DONE checker 重算 hash 并用对应
envelope 重新严格解析结果；任一漂移 fail closed。record 与 dispatch 都必须显式保存
`workspace_id == STATE.workspace_id`、`parent_agent_id == STATE.orchestrator_agent_id`、
`lineage_verified=true` 与精确创建 labels；任一处字段缺失即失败。`candidate_identity` 在
冻结后不可变，dispatch、labels、record 与 envelope 四处必须逐字相等。

n≥4 的四条 lane record 只能整组发布：任一 member 无效或基础设施失败时只保留 child/raw
诊断，归档整组后以更高 attempt fresh retry 重建完整 group，partial publication 不得当作
完成。group ID、group identity、manifest path 三者各自都不得跨 stage 复用。

terminal predicate 只记录 surface completion：全部冻结 screen entry 已按本契约运行且每项
有一个 `OK|ISSUE` 结果及 evidence 绑定。它不宣称 deep review 完成，不宣称 repair 完成，
不把 `OK` 写成 `deep_reviewed` 或 `closed`；后续 deep／repair 阶段按生产 SPEC 另行派发。
surface 是 review_only 任务，拥有独立 whole-screen terminal：恰一个覆盖完整 screen 集合的
`REVIEW/full` 或 `REVIEW/lane_group` 成功 stage 即终止，不借用 contextual 契约的
implement 收敛（RE_REVIEW/FINAL_REVIEW 升级序列不属于本契约）；完整的 surface 重试历史
必须可验证：失败 attempt 之后跟随成功 stage 时，attempt 必须单调递增，且成功 stage 与后续
失败 attempt 都不得复用任何失败 child 的 dispatch_id、agent_id 或 lane
group_id／group_identity／group manifest path；失败 child 包含已派发、已归档但从未发布
completion record 的 orphan failed child（由 child_dispatches 与其 lane_group_identity 绑定的
group manifest 重建其 group／attempt 状态，manifest 缺失或被覆写即 fail closed；orphan full
child 无持久化 attempt，仅强制身份新鲜）；只含失败 attempt 的历史绝不能关闭任务。
`n=0` 不 dispatch，改以
canonical 零项 artifact（`.ai/task/<task_id>/SURFACE-SCREEN-ZERO.json`，恰含 contract、
task_id、`screen_count=0`、`proves_no_surface_dispatch=true`、`reason="zero/no-dispatch"`、
`algorithm`（`surface-zero-workset/1`）与可重算 empty-workset/input snapshot
`workset_identity`）证明没有发生任何 surface dispatch；n=0 的 build 不得声明任何
dispatch/group/cycle/attempt 输入；DONE 重算 `workset_identity`。该 artifact 存在时不得同时
存在任何 surface dispatch，也不得绑定 carry-over artifact。surface 任务必须使用
`change_class=translation_workflow`，并在 STATE 携带独立的不可变 surface evidence
reconciliation binding `surface_evidence_binding`（恰含 `algorithm`
（`surface-evidence-binding/1`）、`task_id`、`terminal`（`zero|whole_screen`）与
`artifact_sha256`（终端 artifact 路径→SHA-256 的精确映射：zero terminal 绑定零项 artifact
与 `surface_screen_input_path` draft，whole_screen terminal 绑定每个 surface record 的
input_path 与 raw_output_path、`surface_screen_input_path` draft，以及已绑定的
carry-over artifact））；DONE 从当前字节重算该映射，缺失、漂移、额外或遗漏 artifact 一律
fail closed。该绑定独立于
code/contextual sidecar terminal，但存在真实 code record 时 sidecar reconciliation 绝不因
surface 而豁免。

每种 surface terminal（zero、full、lane）都必须以统一的 `surface_screen_input_path`
绑定一份不可变的实际 canonical 冻结输入 draft 路径及其 bytes/hash；绝不接受用常量空
identity 冒充实际输入。DONE 必须重读该 draft：zero terminal 要求 draft `entries==[]`；
n≤80 时 stage 覆盖必须与 draft 逐项精确相等；n>80 时必须存在已验证的 carry-over artifact
且 stage 覆盖恰为其记录的 first-80 集合——删除 carry 绑定不能把 n=85 重新分类为整屏
n=80。DONE 的 surface 检查从任何持久化 surface 活动激活（任何 surface purpose 的 child
dispatch、任何 surface completion record 或任何 surface terminal 绑定），因此把契约从
`review_contracts` 移除或降低 `schema_version` 都不能绕过这些检查，只会 fail closed。

## 五、REVIEWER 输入与边界

REVIEWER 只读取精确 input_path、其中明确引用的内容和本契约第六节；不得读取其他
`.ai/task/`、`.ai/reviews/`、lane raw 或先前 finding。冻结 payload 只含 source/target
快照、locator、术语 snapshot 哈希所绑定的术语子集、算法版本与 lane-neutral briefing；
禁止注入先前 finding、裁决、建议修复或宿主 lineage。

固定三行 dispatch prompt（模板与每次实例 UTF-8 bytes 均 `<= 800`，派发前逐条验证）：

```text
任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、参数顺序或格式等表层问题；否则判 OK。
输入：candidate_identity=<candidate_identity>；input_path=<input_path>。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-surface-screen-v1-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。
输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。
```

## 六、结果 schema 与校验（fail closed）

整个输出必须是单一紧凑 JSON object，且必须是 **canonical sorted compact bytes**：UTF-8、
递归 key 排序、`ensure_ascii=false`、紧凑分隔符 `{},:`、无尾随换行或任何前后附加字节。
下面是一个能被 validator 接受的真实样例（两个 entry，一项 OK、一项带 observation 的 ISSUE）：

```json
{"candidate_identity":"1f0e3dad618f6a4d9c5b8e1f8f5b8d0a9c5b8e1f8f5b8d0a9c5b8e1f8f5b8d0a","contract":"translation_surface_screen_v1","results":[{"entry_revision_identity":"0a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9","verdict":"OK"},{"entry_revision_identity":"9f8e7d6c5b4a39281706f5e4d3c2b1a09f8e7d6c5b4a39281706f5e4d3c2b1a0","observation":"占位符 %s 序列被破坏","verdict":"ISSUE"}]}
```

注意样例中 keys 已按字典序排列（`candidate_identity` 先于 `contract`；item 内
`entry_revision_identity` 先于 `observation` 再于 `verdict`）；围栏、缩进、未排序 keys、
尾随换行都会被拒绝。逐字规则：

1. root 恰含三键；contract 精确等于 `translation_surface_screen_v1`；
2. `candidate_identity` 匹配 `^[0-9a-f]{64}$` 且等于 envelope 值；
3. `results` 数量与每项 `entry_revision_identity` 必须逐位置等于冻结 `entries`；
4. verdict 仅 `OK|ISSUE`；`OK` item 恰含 `entry_revision_identity`/`verdict`，`ISSUE` 另且
   仅含 strip 后非空 `observation`；
5. 禁止 severity、adjudication、suggested fix、witness、index、entry_count 或任何额外字段；
   表层结果不得升级为 finding 或修复指令；
6. decoder 严格拒绝 duplicate JSON keys、BOM、非法 UTF-8、NaN/Infinity、围栏以及前后附加
   字节；落盘 envelope 与 raw output bytes 必须是 canonical compact JSON。

该验证证明候选绑定与显式覆盖，不声称证明 reviewer 的主观投入，也不构成语义深审证明。

## 七、外发与边界

读取范围按本契约第五节；通用只读与裁决责任见[编排契约第八、十一节](paseo-orchestration-v2-contract.md#八角色执行与恢复)：
`ISSUE` observation 只是候选信号，必须经固定源码核验与裁决才能成为 finding；`OK` 只表示
表层筛查未命中，R-low 条目留在 ledger 待抽检，不得伪称深审完成。本契约不修改生产译文、
术语库、evidence 批次或既有 v1/v2 fixture；禁止在仓库行为中硬编码任何 provider/model。
entry-revision 的长期状态机（`queued`、`deterministic_pass`、`deterministic_failed`、
`screened`、`sampling_queued`、`deep_queued`、`deep_reviewed`、`revalidated`、
`finding_observed`、`adjudication`、`fixed`、`no_fix_closed`、`invalidated`、`reopened`、
`closed`）由 append-only ledger 工具独立校验；ledger 只记录持久化迁移，不从 provider/model
推导任何覆盖。每条 ledger 记录恰含十一个 canonical 键（含 `reason_code` 与 `provenance`）：
`reason_code` 只能取封闭机器原因集，且必须与具名 `(from_state,to_state)` 迁移匹配，自由
文本原因一律拒绝；每个具名迁移同时绑定其允许的 `provenance.kind` 集合，错位的 kind 一律
拒绝。进入 `invalidated` 只允许身份变化原因（source、fixed source、术语 snapshot、rules
version、`call_locator` 或 `source_tag` 变化）；`call_locator_changed`／`source_tag_changed`
是逻辑迁移原因：其后续新逻辑身份的首条 revision 必须紧随该 invalidation 记录，并携带指回
它的 `migration_from_logical_entry_identity` migration edge（migration edge 只能引用逻辑迁
移原因的 invalidation）；该 pending edge 是单次消耗边：恰被其后继 revision 消耗一次，此后
同一来源不得再被任何 migration edge 引用（fork 拒绝），已迁离的逻辑身份也不得在无新
pending edge 的情况下再生成 revision（复活 fork 拒绝）；逻辑身份自身不得作为自己的
migration 来源；当 locator 回归先前取值时，允许如实地迁回先前使用过的逻辑身份，但该
revert revision 必须紧随其后并携带指向另一不同 pending 来源的 migration edge；真实 revival
消耗 pending edge 后清除被复活身份的已迁离标记，使其后续普通 invalidation 仍可产生普通
revision bump，并可在再次逻辑迁离后重新作为 migration 来源，而已消耗来源的 fork／复用引用
仍一律拒绝；已关闭
revision 也只能因这些身份变化 invalidation 进入新
revision，`closed→reopened` 只接受新的 fidelity/completeness/grammar/terminology/runtime/
translationese 证据 code，偏好性 reopen 一律拒绝；首条 append 也必须按 prospective history
replay，且既有历史在任何 append（包括 exact-last-line 幂等返回）之前必须先完整 replay，
损坏的既有历史绝不能报告成功；任意位置的重复不可变事件（仅 exact last line 幂等）与跨逻
辑身份的 revision 复用都 fail closed。
