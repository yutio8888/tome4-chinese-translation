# Paseo 译文语境审核 v1 技术契约（translation_contextual_v1）

> 状态：规范。
>
> 契约版本：`translation-contextual/1.2`。
>
> 1.2：规范短派发 prompt 收敛为任务／输入／输出三行（未实例化规范模板 ≤800
> UTF-8 字节，唯一动态值
> `<candidate_identity>` 与 `<input_path>`），不再指示阅读 `.ai/roles/reviewer.md`；
> schema、恢复、身份、只读守卫与 fresh-session 规则不变，仍由本文磁盘规范承载。
>
> 上位规则：[`AGENTS.md`](../AGENTS.md)；编排细节见
> [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md)。
> 本文定义译文审核 contract `translation_contextual_v1` 的输入、候选身份、结果
> schema、校验、分离、恢复与只读失败语义。

## 一、定位与边界

`translation_contextual_v1` 是译文审核的唯一路由（旧 `translation_v2` blind runner
已退役，见 `archive/docs/pi-review-v2-contract.md`）：

- 它由现有 Paseo REVIEWER 角色以 `purpose=translation_contextual_v1` 载体执行，不引入
  第四个 Paseo 角色；
- 它独立记录与指标，是语义 observation 进入质量指标的唯一契约；
- 本契约是 ORCHESTRATOR 与语境 REVIEWER 之间的技术契约，不授权模型自动裁决：
  severity、确认状态与修复建议一律由 ORCHESTRATOR 独立作出。

## 二、运行时元组与创建

语境 REVIEWER 固定使用 Pi provider 的 `opencode-go/deepseek-v4-flash`，无 mode，
thinking `max`。完整元组为：

```text
pi / opencode-go/deepseek-v4-flash / mode null / thinking max
```

规范形式与其他规范文档一致：`pi`/`opencode-go/deepseek-v4-flash`/null 或缺失/`max`。

创建必须由 ORCHESTRATOR 直接调用 agent-scoped MCP `create_agent`（CLI 等价：
`paseo run --provider pi --model opencode-go/deepseek-v4-flash --thinking max
--workspace <workspace-id> --label task_id=<task-id> --label role=reviewer
--label purpose=translation_contextual_v1 --label candidate_identity=<sha256>
--label dispatch_id=<dispatch-id> --json '<短派发 prompt 的精确文本（见第四节）>'`），
不得使用 provider 原生 `spawn_agent`，也不得手写 parent label。创建前必须先冻结
候选、计算 `candidate_identity`、为本次 create attempt 生成唯一任务作用域
`dispatch_id`，并把紧凑派发 envelope 的 UTF-8 字节写入任务作用域 workspace 相对
输入文件 `input_path`（见第四节）；常规计划派发总是创建 fresh 语境 REVIEWER，
不挪用其他候选或旧 dispatch 的 agent。`create_agent.initialPrompt` 只携带第四节
短派发 prompt（唯一动态值是候选身份与输入路径），不是派发 envelope，
也不是 inner rendered_briefing 本身。CLI 等价中，`paseo run` 的 positional prompt
（`paseo run ... <prompt>`）与 MCP `create_agent.initialPrompt` 是同一份短 prompt
的精确同一文本；`--json` 只控制 CLI 输出格式，不携带 prompt 或 envelope。MCP 载荷：

```json
{
  "workspaceId": "<workspace-id>",
  "title": "reviewer-contextual <task-id>",
  "provider": "pi/opencode-go/deepseek-v4-flash",
  "initialPrompt": "<第四节短派发 prompt 的精确文本>",
  "labels": {
    "task_id": "<task-id>",
    "role": "reviewer",
    "purpose": "translation_contextual_v1",
    "candidate_identity": "<sha256>",
    "dispatch_id": "<dispatch-id>"
  },
  "settings": {"thinkingOptionId": "max"}
}
```

`settings.modeId` 必须省略（Pi 无可选 mode）。不得静默降级 thinking，也不得在
Pi 元组不可用时回退到 Codex：`code_legacy_v1` 的 Codex 路由保持不变，语境审核
失败关闭。

每次派发、重跑与无效输出重试都创建 fresh agent 与独立 provider session，不通过
`send_agent_prompt` 复用旧语境 REVIEWER；每个 create attempt 拥有独立 `dispatch_id`
与独立 `input_path` 文件。

### dispatch_id 规范

`dispatch_id` 是任务作用域内每次 create attempt 的唯一短 token，同时用于 agent
label 与冻结输入文件名，必须既是 label 安全值也是文件名安全值。格式精确固定为：

```text
^[0-9a-z][0-9a-z-]{0,31}$
```

即：首字符必须是 ASCII 数字或小写字母（`[0-9a-z]`），后续字符只允许 ASCII 数字、
小写字母或连字符 `-`，总长 1–32。以下值一律拒绝：含 `/` 或 `\` 斜杠、含 `.` 的
任何点段（`.`、`..`、`.hidden`、`a.b` 等）、含空白（空格、制表、换行）、含任何
非 ASCII 字符（中文、全角符号、emoji 等）的值，以及超长（>32）或首字符不在
`[0-9a-z]` 的值。ORCHESTRATOR 必须在构造 `input_path` 与 labels 之前校验
`dispatch_id`；不合法即视为候选冻结失败，不得创建 agent、不得写入输入文件。
构造 `input_path` 后，若该精确路径已存在任何既有条目（文件、目录或符号链接），
则候选冻结失败：不得覆盖或写入该路径，不得创建 agent，必须换一个新的合法
`dispatch_id` 再尝试。

## 三、创建／恢复后核验

取得精确 agent ID 后立即用 `get_agent_status`（CLI `paseo inspect`）核验：

1. 父级 lineage：归一化 `ParentAgentId` 或保留 label `paseo.parent-agent-id` 必须
   精确等于 `orchestrator_agent_id`；MCP 状态面无法暴露可验证 lineage 时停止该
   agent 并进入 `WAIT_USER`，`STOP` 不作为该条件的直接替代（只用于用户明确取消或
   单独确立的终态条件）；
2. workspace 必须等于任务 `workspace_id`；
3. Provider 必须为 `pi`、Model 必须为 `opencode-go/deepseek-v4-flash`；
4. Thinking 必须为 `max`；
5. Mode（`currentModeId`／`runtimeInfo.modeId`）必须为 null／缺失；Pi 意外返回
   非 null mode 时停止并按基础设施错误处理。
6. ORCHESTRATOR 把精确 agent ID、当前 `dispatch_id`、`input_path` 与 `candidate_identity`
   写入 STATE 的条件字段
   `contextual_reviewer`（provider `pi`、model `opencode-go/deepseek-v4-flash`、mode null、
   thinking `max`、purpose `translation_contextual_v1`、candidate_identity、dispatch_id、
   input_path、agent_id）；
   该字段仅在 `review_contracts` 含 `translation_contextual_v1` 时存在，`reviewer` 块仍为
   `code_legacy_v1` 的 Codex 载体，未选择该 contract 的任务无迁移。
   已完成的历史语境 review 记录不改写；活动任务在下次语境派发时采用新字段。
7. 语境 review 记录必须记录 `candidate_identity`、`dispatch_id`、`input_path`、`agent_id`
   四个精确字段；`dispatch_id` 是宿主侧记录字段，不进入模型结果 schema（见第六节）。

任一不匹配时停止该 agent，不得使用其输出，不发送新的任务消息。上下文审核只在元组
完全匹配时有效；没有“部分接受”或降级使用。

### 恢复

创建结果不明确时，用 `list_agents` 限定任务 workspace／cwd（`includeArchived=false`、
`sinceHours` 覆盖任务开始时刻），在宿主侧先按 `labels.task_id`、`labels.role=reviewer`
过滤，再按目标 `labels.purpose=translation_contextual_v1`、`labels.candidate_identity`
与 `labels.dispatch_id` 精确过滤（**过滤先于基数判定**）。恢复只允许复用
同一 `dispatch_id` 的同一 create attempt（歧义 create 的精确恢复）；旧候选（
`candidate_identity` 与当前冻结值不同）与旧 dispatch（`dispatch_id` 不同）的 agent
被该精确过滤排除，不算作候选匹配，因此过滤后不存在“候选不匹配”分支；当前
dispatch 零匹配时只允许一次既有重试（新 create attempt 使用新 `dispatch_id` 与
fresh agent）。
`list_agents` 结果按 `limit` 截断，截断或不完整的列表不得当作零匹配。过滤后：
无匹配允许重试一次；唯一匹配且元组核验通过则复用；多个当前候选匹配、截断／
不完整的列表、缺省 purpose 歧义，或其他无法确立唯一性的状态，进入 `WAIT_USER`。
已选语境 contract 的任务中，缺省 purpose
的候选视为歧义，进入 `WAIT_USER`，不得按 `normal_review` 复用为语境载体。复用前
按上一节完整核验，并采用 STOP-on-mismatch：任何 Provider/Model/Mode/Thinking 不匹配
（包括 `Thinking` 不是 `max`、Mode 非 null）都停止该 agent 并按基础设施错误处理，
不使用 `update_agent` 改回该语境会话，不发送下一条任务。恢复复用的 agent 后，
把其 agent ID、`dispatch_id`、`input_path` 与 `candidate_identity` 同步到 STATE 的
`contextual_reviewer.agent_id`／`contextual_reviewer.dispatch_id`／
`contextual_reviewer.input_path`／`contextual_reviewer.candidate_identity`。

## 四、候选身份（candidate identity）

语境候选身份由**规范 payload 字节**计算而来。自我哈希循环只由把已计算的 identity
**值**嵌入被哈希的 payload 造成，不因提及字段名 `candidate_identity` 而产生：payload
根只允许既有的八个声明键、不得新增 `candidate_identity` 字段；`rendered_briefing`
可以提及结果字段名 `candidate_identity` 并展示完整严格结果 schema，但不得嵌入
已计算的 64 位十六进制 identity 值；payload 作为数据保持不含身份，外层派发
envelope 携带计算后的 identity。

### 规范 payload

payload 是一个 JSON object，包含恰好八个逻辑组件：

```json
{
  "contract": "translation_contextual_v1",
  "ordered_revision_keys": ["<key-1>", "<key-2>"],
  "translation_snapshot": [
    {"revision_key": "<key-1>", "source": "<冻结 source-1>", "target": "<冻结 target-1>"},
    {"revision_key": "<key-2>", "source": "<冻结 source-2>", "target": "<冻结 target-2>"}
  ],
  "fixed_source_commit": "<manifest 固定的公共源码 commit id>",
  "terminology_snapshot": "<渲染进 briefing 的精确术语子集字符串>",
  "bounded_context": [
    {"revision_key": "<key-1>", "context": "<source tags／runtime keys、邻近译文、公共源码证据片段>"},
    {"revision_key": "<key-2>", "context": "<source tags／runtime keys、邻近译文、公共源码证据片段>"}
  ],
  "rendered_briefing": "<计算身份前的最终渲染 briefing 字符串>",
  "runtime_tuple": "pi/opencode-go/deepseek-v4-flash/null/max"
}
```

约束（精确形状）：

- 根必须是 object，恰好包含八个声明的键：`contract`／`ordered_revision_keys`／
  `translation_snapshot`／`fixed_source_commit`／`terminology_snapshot`／
  `bounded_context`／`rendered_briefing`／`runtime_tuple`；
- `ordered_revision_keys` 是 string array；`translation_snapshot`／`bounded_context`
  是精确键 object array（仅 `revision_key`／`source`／`target` 或
  `revision_key`／`context`）；其余组件是 string；
- 每个标量叶子必须是 string：null、boolean、numeric 与任何非 string 值一律拒绝；
  额外键、缺失键、错误容器形状／类型一律拒绝；
- `translation_snapshot`／`bounded_context` 的每个元素必须与
  `ordered_revision_keys` 一一对应并保持冻结顺序；重复、乱序、错位的 revision
  条目一律拒绝；
- `terminology_snapshot` 与 `rendered_briefing` 是渲染后的精确字符串；
  `rendered_briefing` 可以提及结果字段名 `candidate_identity` 并包含完整严格结果
  schema，但不得嵌入已计算的 64 位十六进制 identity 值（payload 保持 identity-free
  数据；身份值经外层 envelope 携带给模型，控制面元数据副本不是 payload 组件）。

约束（语义值，哈希前与接受结果前都执行）：

- `contract` 必须精确等于 `"translation_contextual_v1"`；
- `runtime_tuple` 必须精确等于 `"pi/opencode-go/deepseek-v4-flash/null/max"`；
- `fixed_source_commit` 必须非空且精确等于该候选适用的 manifest 固定公共源码
  commit（由任务 manifest 证据固定）；
- `ordered_revision_keys` 必须精确等于实际冻结候选的有序 revision ID 列表；
  `translation_snapshot` 每个元素的 `revision_key`／`source`／`target` 必须精确等于
  冻结候选对应 revision 的 ID 与 source/target 字节；`bounded_context` 的
  `revision_key`／`context` 与冻结候选对齐（如前述 1:1 规则）；
- `revision_key`、`source`、`target` 都不得为空字符串——空值在候选冻结时、身份计算
  前即被拒绝；
- 哈希自洽不足以保证候选正确：上述语义相等性检查必须在哈希／派发之前执行，并在
  接受返回结果前（identity echo 与 evidence 绑定）重新执行。

任何不精确相等的语义值（错误 contract、错误 runtime tuple、错误 manifest commit、
错误 revision 选择／顺序／source/target）以及空 `revision_key`／`source`／`target`
都在候选冻结时被拒绝，不进入身份计算。

### 规范序列化与身份

canonical contextual payload bytes = UTF-8 JSON 序列化（确定性序列化），规则固定：

- object key 递归按字节序排序；array 保持冻结顺序不变；
- 分隔符精确为 `,`／`:`，无多余空白、无换行；
- `ensure_ascii=false`（非 ASCII 原样 UTF-8 输出），字符串按 JSON 转义规则；
- 任何违反上述精确形状的值（错误容器、非 string 标量、额外／缺失键）使序列化失败，
  候选无效。

```text
candidate_identity = SHA-256(canonical contextual payload bytes)
```

### 规范向量

下列最小 payload 满足全部八个组件、数组／object 与 1:1 revision 规则，并含非 ASCII
字符串以覆盖 `ensure_ascii=false`：

```text
{"bounded_context":[{"context":"tag=talents/foo; nearby: A, B","revision_key":"r1"}],"contract":"translation_contextual_v1","fixed_source_commit":"61bb370c33e46c4df4b2bbfd56113a0de1822300","ordered_revision_keys":["r1"],"rendered_briefing":"有界语境审核 briefing：revision r1","runtime_tuple":"pi/opencode-go/deepseek-v4-flash/null/max","terminology_snapshot":"术语：zone=区域","translation_snapshot":[{"revision_key":"r1","source":"Hello world","target":"你好，世界"}]}
```

即：`contract="translation_contextual_v1"`、`ordered_revision_keys=["r1"]`、
`translation_snapshot=[{"revision_key":"r1","source":"Hello world","target":"你好，世界"}]`、
`fixed_source_commit="61bb370c33e46c4df4b2bbfd56113a0de1822300"`、
`terminology_snapshot="术语：zone=区域"`、
`bounded_context=[{"revision_key":"r1","context":"tag=talents/foo; nearby: A, B"}]`、
`rendered_briefing="有界语境审核 briefing：revision r1"`、
`runtime_tuple="pi/opencode-go/deepseek-v4-flash/null/max"`。

该单行文本按上述规范 JSON 规则生成；其 UTF-8 字节的 SHA-256 为：

```text
ae6923cf13f7662ee609155c690da1abaa3117a8b0ce07ce079ada3284f9378b
```

测试与未来辅助脚本必须按同一 recipe 重新构造并得到相同字节与摘要；任何差异说明
recipe 或向量文本漂移。

### 派发 envelope 与冻结输入文件

ORCHESTRATOR 先计算 `candidate_identity`，再构造外层 envelope（payload object
原样不变）：

```json
{
  "candidate_identity": "<sha256>",
  "payload": {"…": "canonical payload 的八个组件，原样不变"}
}
```

派发 envelope 使用与规范 payload 相同的紧凑 JSON 规则序列化（object key 递归按字节序
排序；分隔符精确为 `,`／`:`，无多余空白、无换行；`ensure_ascii=false`）。该 JSON 文本
的 UTF-8 字节写入任务作用域的冻结输入文件——workspace 相对路径
`input_path = .ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json`，
每个 create attempt 一个文件，路径精确且必须是常规 JSON 文件。envelope 含
`candidate_identity` 与未改动的 payload object（含已渲染且不含身份的 `payload.rendered_briefing`）。
该文件是候选输入的唯一载体：派发前写入并冻结，
由 fresh 语境 REVIEWER 用只读 workspace 工具读取；`initialPrompt` 不再内联
envelope 或任何候选数据。ORCHESTRATOR 在创建前、返回后与接受结果前都从 payload
重算 identity，并核对输入文件字节未变；任何修改、替换、删除、符号链接替换或
身份不匹配都使输出无效。

`candidate_identity` 的**值**不得进入被哈希的八个键 payload 或
`payload.rendered_briefing`（字段名允许出现在 `rendered_briefing` 中）；它由外层
派发 envelope（冻结输入文件）与短派发 prompt 携带给模型。控制面元数据副本明确允许且必需：agent labels 的 `candidate_identity=<sha256>`、
STATE `contextual_reviewer.candidate_identity`、语境 review 记录的 `candidate_identity`——这些副本不是被哈希的 payload 组件，不参与
身份计算。返回结果的 `candidate_identity` 必须等于（echo）envelope 派发值。校验时
ORCHESTRATOR 从 payload 重算 identity，重算值、envelope 值与返回值三者不一致即
输出作废。

该身份**不得复用** code-diff 候选配方（`candidate_ref` 公式）。`candidate_identity` 写入语境 review 记录，
派发前与返回后都必须从冻结的候选字节重算并保持一致；不一致时输出作废。

### 短派发 prompt（规范模板）

`initialPrompt`（CLI positional prompt）只含下列三行任务／输入／输出短模板
（字节上限针对未实例化模板：≤800 UTF-8 字节），唯一动态值是 `<candidate_identity>`
与 `<input_path>`；模板不指示阅读 `.ai/roles/reviewer.md`，详细 schema、恢复、身份、
只读守卫与失败规则只在本磁盘规范中：

```text
任务：审核全部冻结 revision；据输入文件术语、上下文和所引固定源码，只报有证据的实质语义、机制、术语或关系错误，无问题填 OK。
输入：candidate_identity=<candidate_identity>；<input_path> 是唯一候选载体。全程只读，禁止写入任何文件；只读该文件及其所引译文/公开源码、docs/paseo-translation-context-review-v1-contract.md 第六节，不读其他 .ai/task/.ai/reviews。
输出：仅回第六节单一紧凑 JSON；冻结顺序全量覆盖并回显 <candidate_identity>；首字节{、末字节}，无其他文字、Markdown/围栏。
```

模板不内联派发 envelope、有序 revision 列表、source/target、术语、有界上下文、
源码片段或其他候选数据；`rendered_briefing` 保持不含身份的磁盘驻留组件，不作为 `initialPrompt`，
候选数据从不复制进短 prompt。JSON-only 输出规则位于模型可见文本。
字节上限只约束未实例化模板；实例化后的实际长度随 `<candidate_identity>`（64 位
十六进制）与 `<input_path>`（含任务 ID 与 `dispatch_id`）而定，本契约不设全局
实例化上限。
CLI 的 positional prompt 与 MCP `create_agent.initialPrompt` 是这份短 prompt 的
精确同一文本；`--json` 只控制 CLI 输出格式，不携带 prompt 或 envelope。

## 五、输入（有界 briefing）

语境 briefing 只包含任务范围内的有界上下文，经冻结输入文件（派发 envelope）交付，
不复制进 `initialPrompt`：

- 精确 source/target 对；
- source tags／runtime keys；
- 术语子集；
- 邻近译文（同文件／同 section 相邻条目）；
- 固定版本公共源码证据片段（manifest 固定 commit 内的公开源码）。

**禁止注入**：先前 finding、裁决决定、建议修复及任何宿主 lineage。

读取边界：语境 REVIEWER 只读取短 prompt 指定的精确 `input_path` 文件、
该文件明确引用的译文／公开源码路径，以及本契约第六节（严格结果 schema）；
不得阅读整份 `.ai/roles/reviewer.md` 或整份本契约文档；不得浏览本任务其他
`.ai/task` 文件或任何 `.ai/reviews` 记录。

## 六、结果 schema 与校验（fail closed）

输出必须是单一紧凑 JSON object：第一个字节为 `{`，最后一个字节为 `}`，无 prose、
Markdown 或代码围栏；解析失败即失败关闭。结果 object／envelope（键结构为
`contract`／`candidate_identity`／`revisions`，与派发
envelope 的 `candidate_identity`／`payload` 结构不同；结果只回显派发身份）：

```json
{
  "contract": "translation_contextual_v1",
  "candidate_identity": "<sha256>",
  "revisions": [
    {
      "revision_key": "<冻结 bundle 中的规范 key>",
      "observation": "问题描述或明确无问题的固定值 \"OK\"",
      "evidence": {"source": "<冻结 source 原样>", "target": "<冻结 target 原样>"}
    }
  ]
}
```

严格 schema（ORCHESTRATOR 执行，全部通过才算有效记录；任何违反都失败关闭）：

1. `contract`：string，必须精确等于 `"translation_contextual_v1"`；
2. `candidate_identity`：string，必须匹配 `^[0-9a-f]{64}$`，且等于（echo）派发
   envelope 的值；
3. `revisions`：array，长度必须等于冻结 revision 数；每个元素是 object；
4. 每个 object 层（envelope、revision、evidence）都 `additionalProperties=false`：
   只允许本 schema 规定的键，任何额外键（severity、确认状态或 suggested fix 等）
   都视为畸形；
5. `revision_key`：非空 string；每个 revision 恰好覆盖一次——revision key 集合
   与冻结集合精确相等（无缺失、无重复），数组顺序与冻结顺序精确一致（乱序失败
   关闭）；
6. `observation`：非空 string；明确无问题必须用固定值 `"OK"`，其他非空值为问题
   描述；
7. `evidence`：object，只允许 `source`／`target` 两个键，均为非空 string，且
   `evidence.source`／`evidence.target` 与冻结的 source/target 逐字节相等。
8. 接受结果前重新执行第四节「约束（语义值）」的全部相等性检查，与 identity echo、
   evidence 逐字节绑定一起作为接受条件；任何不匹配都失败关闭。
9. 结果必须来自 STATE 当前 `contextual_reviewer.agent_id` 的 agent，且该 agent 的
   派发 `dispatch_id` 等于当前派发值；`dispatch_id` 是宿主侧接受条件，不进入模型
   结果 schema（结果 object 只允许 `contract`／`candidate_identity`／`revisions`
   三键，`additionalProperties=false` 使任何额外键失败关闭）。
10. 发起新 dispatch（新 `dispatch_id`）或无效输出重跑前，先停止旧语境 REVIEWER
    （CLI `paseo stop`，MCP `cancel_agent`）；停止后旧 agent 的迟到输出一律作废，
    不得合并或计入记录，contract 保持 pending 直到当前派发返回有效结果。

任何违反（缺失、重复、乱序、错候选、畸形）都使该次审核记录无效，contract 保持
pending；ORCHESTRATOR 按基础设施／契约失败处理并重新派发，不得把部分输出合并为
有效结果（不得部分接受）。severity、确认与修复全部由 ORCHESTRATOR 独立裁决。

## 七、只读与失败语义

- 派发前冻结有界候选（bundle、渲染 briefing、`candidate_identity` 字节与冻结
  输入文件字节）；
- 冻结输入文件（`input_path`）属于只读守卫：任何修改、替换、删除、符号链接替换
  或 payload 身份不匹配都使输出无效；ORCHESTRATOR 在创建前、返回后与接受结果前
  重算 identity 并核对文件字节，派发后到 contract 完成前不得重写该文件；
- 派发前对**有界快照路径集**做精确快照：任务前既有脏／untracked 路径 + 任务候选
  路径；每个路径记录内容摘要（文本按 UTF-8 字节、二进制按原始字节）与 index-diff
  摘要；不对整个干净仓库做全量哈希；
- 返回后对同一路径集重算摘要并逐路径比较：任何内容变化、新增状态路径（即使
  `git status` 分类仍为 M）、删除或重命名都视为写入，使输出无效；
- 派发前记录仓库 HEAD OID（`git rev-parse HEAD`），返回后要求与派发前精确相等；
  HEAD 变化（即使随后工作树干净）都使输出无效并按基础设施错误处理；这只是单个 OID
  比较，保持不做全仓哈希的边界；
- 有界快照路径集**路径精确**地覆盖持有冻结语境输入或决策关键任务控制状态的
  ignored 文件（例如本任务冻结候选与 `CONTEXTUAL-ENVELOPE-<dispatch_id>.json`
  输入文件、`STATE.json`、本任务 review 记录）；不得通过
  排除整个 `.ai`／`.artifacts` 目录代替路径精确列举；
- ORCHESTRATOR 自有的任务／review 记录允许在审核区间合法变化的有限路径精确
  allowlist（例如本任务 `STATE.json` 与 review-NN 记录在后处理写入时）；
- 派发前快照与返回后比较必须在 ORCHESTRATOR 后处理写入之前完成（可行处）；
  观察到 reviewer 的任何写入都使输出无效；
- 通用 ignored 暂存空间（`.artifacts/` 内其他内容）不进行穷尽监控，本守卫只覆盖
  上述路径精确集合；不建立通用文件系统监控、runner／supervisor、
  全仓或全 ignored 树哈希，也不监控 workspace 之外；
- 语境 REVIEWER 造成任何写入（修改、创建、删除、stage、commit）都使输出无效，
  按基础设施错误处理，不复用该 agent；
- 候选冻结后到 contract 完成前若冻结内容改变（用户或其他改动），旧输出作废，
  重新冻结并派发 fresh REVIEWER。

## 八、分离与指标

- 语境记录与指标独立保存，任一 contract 的输出都不得改写另一 contract 的冻结输入；
- 译文语境输入携带术语子集与固定源码证据；先前 finding、裁决与建议修复不得注入。

## 九、外发

本契约即 `AGENTS.md`「外发边界」中用户已授权的 Pi 语境审核通道：允许向 Pi REVIEWER
发送上述有界译文语境内容并允许其只读读取任务范围内 workspace。范围外内容仍须用户
授权。
