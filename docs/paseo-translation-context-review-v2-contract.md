# Paseo 译文语境审核契约 v2

版本 `translation-contextual/2.0`。本契约只绑定 `role=reviewer`、
`purpose=translation_contextual_v2`、当前 task/workspace/direct parent lineage 和冻结输入；
REVIEWER 全程只读。v1 task 和 artifact 不迁移，同一 task 不得混用 v1/v2。

## 一、版本与身份

新任务使用 `review_contract=translation_contextual_v2`、`labels.purpose=translation_contextual_v2`
和 `schema_version >= 5`。candidate identity 只绑定本文件第三节的七键 payload，不绑定运行时
provider/model。dispatch ID 与 group ID 必须是文件名安全 identifier；每次失败或无效输出的
重试都创建 fresh child。四 lane 必须同组重试，旧 attempt 不补写 completion record。

## 二、七键候选与哈希

payload 恰含：`contract`、`ordered_revision_keys`、`translation_snapshot`、
`fixed_source_identity`、`terminology_snapshot`、`bounded_context`、`rendered_briefing`；
`contract` 精确为 `translation_contextual_v2`。revision keys 为非空唯一字符串，两个 object
数组按 keys 等长同序；source 非空，target/context 可空，全部叶子均为字符串。
`fixed_source_identity` 仅为 `commit:<40 lowercase hex>` 或 `snapshot:<64 lowercase hex>`。
briefing 不得嵌入 64 位 identity。

canonical bytes 使用 UTF-8、`ensure_ascii=false`、递归 key 排序、紧凑分隔符、
`allow_nan=false`；`candidate_identity=SHA256(canonical payload bytes)`。envelope 恰含
`candidate_identity` 与 `payload`。v1 最小向量仅把 contract 改为 v2 后，固定 hash 为
`fb95fa08bd65b4f626bb1b5f0f5a2035a72ef359d584cb088c30609f3fa94067`。

## 三、四 lane manifest

`n >= 4` 可冻结四 lane；`n < 4` 必须 full。权威 artifact 路径为
`.ai/task/<task_id>/CONTEXTUAL-LANE-GROUP-<group_id>.json`，外层恰含 `group_identity`、
`payload`；identity 是 payload canonical bytes 的 SHA-256。payload 恰含 contract
`translation_contextual_v2_lane_group`、task/group ID、`review_phase`、cycle、attempt、
`lane_count=4`、完整五项 workset、`lane_boundaries` 和 `lanes`。每条 lane 绑定 index、
dispatch ID、实际 envelope path 和 candidate identity。

令 `q=n//4,r=n%4`，第 j 条长度为 `q+(1 if j<=r else 0)`，offset 为此前长度和。
validator 必须证明 indices 1..4、正长度、平衡差不超过 1、无 gap/overlap、尾端等于 n，
以及四个 envelope slice 的 ordered union 精确等于 workset。四条 lane briefing 字节相同且
lane-neutral；`rendered_briefing` 不使用 dispatch prompt 的 800-byte 上限。manifest、envelope、
dispatch、record 四方 identity/path/index 必须相等。

lane record 的 `review_kind=lane`，`lane` object 恰含 `group_id`、`group_identity`、
`group_manifest_path`、`index`、`count=4`、`offset`、`length`。dispatch 及创建 labels 都保存
`lane_group_identity` 和 `lane_index`。四个 dispatch/agent 必须不同，均为 ORCHESTRATOR 的
direct child；reviewer 彼此不得读取其他 lane raw/findings。四 lane 不要求模型多样性。

创建 `labels.lane_index` 兼容历史 JSON 整数 1..4 与传输返回的精确 ASCII 字符串
`"1"`..`"4"`，且必须对应同一 numeric lane index；拒绝 bool、float、null、缺失、
前导零、空白、符号、非 ASCII 数字、越界与错 lane。按实际返回值保存 labels，不规范化或
重写 STATE／历史记录。此兼容只适用于创建 label；dispatch／pointer 的 `lane_index`、
record 的 `lane.index` 与 manifest indices 仍为数值。candidate／envelope／group identity
公式及 terminal、分组、重试、provenance、独立性与源码范围均不变。

## 四、STATE、stage 与恢复

v2 禁止单数 `contextual_reviewer`，使用 `contextual_reviewers`。lane 创建时仅允许同组有序
前缀 1..k，四条全部创建并核验后方可 dispatch；发布时恰含四条。full/closure 指针恰含一条，
不带 lane 字段。

terminal 坐标为 `(cycle,attempt,member_ordinal)`：full/closure ordinal=0，lane ordinal=index。
stage key 是前两维；single stage 恰有 member 0，lane stage 恰有 1..4，禁止 mixed stage、
重复或缺 member。group ID、group identity、manifest path 三者各自都不得跨 stage 复用；
任一字段复用即失败。lane 不额外消耗 cycle，也与旧式 `4-lane/max_cycles=10` 规则无关；四个
member 共同占用一个 stage/cycle。

v2 closure 仅用于 `RE_REVIEW`，使用普通 v2 子集 envelope，并写
`parent_review_kind=full|lane_group`、`parent_coverage_identity` 和与子集同序的 `inclusion`。
parent 是 stage 顺序中最新更早 full-coverage stage；full identity 是 candidate identity，
lane_group identity 是 group identity。reason 词表沿用 v1；禁止 v1 的
`parent_candidate_identity`。

无效 result/transport failure 只保留 child/raw 诊断，不形成 terminal。retry 使用更高 attempt
重建完整四 lane group。恢复必须重验 manifest/envelope/raw bytes、身份、`workspace_id`、必需的
direct `parent_agent_id` lineage、
archive 状态和完整 group，不得把 partial publication 当完成。

WP2-Lite 的已归档无效 full dispatch 若需要补充本机 DLC 取证位置，使用新的显式 refreeze event，
生成新 input path、candidate identity 与 task ID。入口仅在旧 checkpoint 处于 `deep_ready`、
旧 refs 均为 prepared、旧 task 无已接受 review record 且全部 child 确认归档时开放。
旧 envelope、candidate、raw 和 diagnostics 保持原字节；新冻结前逐项核对受跟踪 source workset
与本机 checkout 的 SHA-256。checkout 只作为这次 envelope 的取证位置，来源／commit 继续标为
unpinned。新 task 仍须重新执行 anchor preflight、stage 和 dispatch，旧输出不得进入新 task。

操作入口：`python3 -B tools/orchestration/stage_contextual.py <batch-id> --refreeze-id <fresh-token> --source-workset evidence/quality/production-batches/<batch-id>-source-workset.json --ashes-checkout <absolute-checkout>`。
若 export 已发布新 checkpoint，但 stage 在建立 task 或 report 时中断，使用**相同** batch、
`--refreeze-id`、`--source-workset`、`--ashes-checkout` 和 `--out` 原命令重试。入口识别 checkpoint
中同一 event 的 refs，逐项验证冻结 input 的 SHA-256、candidate identity、task 绑定、已有
candidate 字节、未启动 STATE 和 report 内容，随后只补齐缺失的 task 文件或 report；不覆盖已有
candidate、raw、review 或 report。已有 task 含 raw／review、状态已启动、冻结输入或 report
漂移时失败关闭，交回 ORCHESTRATOR 核验，不得手改 checkpoint 或改用新 event 绕过。
若 export 尚未发布 checkpoint，且入口已确认没有该 event 的 task/report，原命令可重试；
不同内容的已有 input 会由 export 拒绝。这个命令只冻结和建立 task，不执行 reviewer。

## 五、raw evidence 与 DONE

解析前把 exact returned bytes 保存为 `.ai/reviews/<task_id>/raw-<dispatch_id>.txt`。每个接受的
v2 record 写同一路径及 `raw_output_sha256`。路径必须由 task/dispatch 精确推导，是 workspace
内 ordinary non-symlink file。DONE checker 重算 hash，并用对应 envelope 重新严格解析第六节
结果；任一漂移 fail closed。

schema-5 implement DONE 扫描两个 review record 数组中全部 v2 terminal（含失败）。最早 stage
必须是 cycle-0 `REVIEW/full|lane_group` 并定义 origin keys/source/fixed source identity；后续
full coverage 不得漂移这些字段。intervening 只允许 `RE_REVIEW/full|closure|lane_group`；失败
`FINAL_REVIEW/full` 仅在更高 cycle 后续 RE_REVIEW 后可保留。`FINAL_REVIEW` 禁止 lane/closure。
唯一最新 stage 必须是 `STATE.cycle` 的成功 whole-workset `FINAL_REVIEW/full`，负责跨条术语、
专名和关系一致性；lane group 永不关闭任务。review-only v2 只允许单一 full。

## 六、REVIEWER 输入与紧凑输出

`translation_snapshot` 是 REVIEWER 唯一可用的译文输入；术语依据只来自 envelope 内实际冻结的
条目正文，包括 `bounded_context[].context` 所含 `source_facts_v1.fact.terminology`。字段
`terminology_snapshot` 在 WP2-Lite 等生产输入中常是摘要；摘要、file／line／hash 只记录
provenance，不等于术语条目正文，也不授权读取或搜索当前译文、当前术语库。其他
引用内容必须在 envelope 中给出精确范围，且不得指向其他 task、review、lane raw 或先前 finding。
允许完整读取本契约作为流程说明，读取本契约的其他章节或标题元数据本身不构成越界。若冻结术语
依据不足，REVIEWER 不得自行搜库或凭偏好判错：只有存在具体可陈述的疑点时，才按既有 schema
返回 ISSUE 并在 `observation` 写明所缺证据；否则返回 OK。ORCHESTRATOR 应补充中性的最小快照，
重新执行适用 preflight 并 freeze；不得为此扩展结果 schema。

固定三行 prompt：

```text
任务：审冻结 revision；仅报有据的语义/机制/术语/关系/跨条问题，否则 OK。
输入：candidate_identity=<candidate_identity>；input_path=<input_path>。只读；可读输入、精确引用及完整 docs/paseo-translation-context-review-v2-contract.md；可沿调用链查冻结版相关源码，仅限输入指定位置；禁从 / 或无关目录全盘搜索，禁读其他 .ai/task/、.ai/reviews/、旧 finding、当前译文/术语库。
输出：仅回第六节紧凑 JSON，按序全覆盖、回显 identity；首{末}，无文字/围栏。
```

模板和每次实例化 UTF-8 bytes 都必须 `<= 800`；路径较长时仍按实际实例拒绝超限，且 full、closure、lane 和
`FINAL_REVIEW/full` 每条 record 在派发前都执行此门禁；超限禁止 dispatch。此上限只约束
dispatch prompt，不约束 payload `rendered_briefing`。唯一结果形状：

```json
{"contract":"translation_contextual_v2","candidate_identity":"<64 lowercase hex>","verdicts":[{"revision_key":"r1","verdict":"OK"},{"revision_key":"r2","verdict":"ISSUE","observation":"非空、有证据的问题"}]}
```

root 恰含三键。verdicts 数量和每个 revision_key 必须逐位置等于 frozen keys。OK item 恰含
revision_key/verdict；ISSUE 另且仅含 strip 后非空 observation。verdict 仅 `OK|ISSUE`；禁止
witness、index、revision_count、severity、adjudication、suggested fix、review_kind 或任意
额外字段。decoder 严格拒绝 duplicate JSON keys、BOM、非法 UTF-8、NaN/Infinity、围栏以及
前后附加字节。该验证证明候选绑定和显式覆盖，不声称证明 reviewer 的主观投入。

## 七、外发和源码证据

根据维护者 2026-09-12 授权，REVIEWER 可沿调用链补查冻结版本中与当前 revision 相关的公开源码，
不要求所有调用文件事先列入输入。2026-09-22 的流程修订另行授权读取精确 input_path、其中精确
范围的引用内容和完整本契约，并规定第六节的冻结译文／术语边界；两次授权不得互相追溯归因。
为定位该版本源码仓库，可在 envelope 明确指定的源码位置作必要的目录和 Git 对象元数据查询；不得从 `/` 或其他无关目录作全盘搜索。DLC checkout 的本机位置只用于本批取证定位，不等于来源、commit 或版本固定；每个实际引用文件仍须与受跟踪 workset 的 SHA-256 匹配。
不得读其他 `.ai/task/`、`.ai/reviews/` 或先前 finding，也不据此扩大译文候选或取得写入权限。

补查应记录组件、公开源码路径、固定 commit（或冻结快照）、关键调用及证据摘录或行范围。
ISSUE 的依据写入现有 `observation`；OK 仍只返回第六节规定的两键对象。ORCHESTRATOR 在收获
审计中依据只读调用记录补齐实际查询路径和证据，包含最终判 OK 的补查；不增加输出字段或改写 raw。
未固定来源须明确标记证据不足，不得自行换用其他版本；机制结论仍以可核验源码为准。
本节与第六节的统一边界只用于后续派发，不追溯改写已冻结的 prompt、candidate/hash、envelope、
raw 或审核记录；原先合法且已归档的输出不因本规则重跑。当前尚未采纳的旧派发输出由宿主按其
原 dispatch 边界审计后裁决。取证审计必须分别记录 JSON 声明、实际读取路径和 child 生命周期，
不得互相推定。
输出按本契约第五节原样持久化；通用只读、裁决及终态归档按[编排契约第七、八、十一节](paseo-orchestration-v2-contract.md#七托管-child-生命周期与即时归档)执行。
