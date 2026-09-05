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

固定三行 prompt：

```text
任务：审核 input_path 中全部冻结 revision；按其术语、上下文及所引固定源码，仅报有证据的实质语义、机制、术语、关系或跨条一致性问题；否则判 OK。
输入：candidate_identity=<candidate_identity>；input_path=<input_path>。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-context-review-v2-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。
输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 revision 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。
```

模板为 637 UTF-8 bytes；使用本任务 ID 和最长 32 字节 dispatch ID 时实例为 773 bytes。
模板和每次实例化 UTF-8 bytes 都必须 `<= 800`，且 full、closure、lane 和
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

REVIEWER 只可读其精确 input_path、其中明确引用的内容和第六节；不得读其他 `.ai/task/`、
`.ai/reviews/` 或先前 finding。机制结论必须绑定公开源码/固定 commit 或明确标记证据不足。
输出按本契约第五节原样持久化；通用只读、裁决及终态归档按[编排契约第七、八、十一节](paseo-orchestration-v2-contract.md#七托管-child-生命周期与即时归档)执行。
