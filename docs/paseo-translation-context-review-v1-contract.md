# Paseo 译文语境审核 v1 技术契约（translation_contextual_v1）

> 状态：规范，运行时解耦版。
>
> 契约版本：translation-contextual/1.5。
>
> 1.5：译文语境审核只绑定 role=reviewer 与 purpose=translation_contextual_v1，不再把
> 运行时载体、版本、档位或回退选择写入契约、STATE 或 candidate identity。候选 envelope、
> 短 prompt、输入边界、严格结果 schema、lineage、workspace、只读守卫和 fresh-session
> 语义保持不变。

## 一、定位与边界

本契约定义 Paseo REVIEWER 的译文语境审核分支。它不是普通代码 review，也不是质量
evaluator 的预注册实验。

控制面必须使用：

- role=reviewer；
- purpose=translation_contextual_v1；
- 当前 task 的 workspace；
- 当前候选的 candidate_identity 和本次创建尝试的 dispatch_id。

运行时载体由 ORCHESTRATOR 按当前环境选择，不属于本契约的身份、授权或验收条件。
本文不要求发现、比较或记录某个具体运行时；Paseo 创建接口所需的其他参数按其当前
接口和本地配置提供。

旧 translation_v2 blind runner 已退役；本契约是活跃译文语境审核的唯一结果契约。

## 二、创建与恢复

语境 REVIEWER 必须由当前 ORCHESTRATOR 直接通过 agent-scoped Paseo 创建接口创建，
并位于当前 task workspace。创建载荷至少包含：

~~~json
{
  "workspaceId": "<workspace-id>",
  "title": "reviewer-contextual <task-id>",
  "initialPrompt": "<第四节短派发 prompt 的精确文本>",
  "labels": {
    "task_id": "<task-id>",
    "role": "reviewer",
    "purpose": "translation_contextual_v1",
    "candidate_identity": "<sha256>",
    "dispatch_id": "<dispatch-id>"
  }
}
~~~

创建操作的其余接口字段不由本契约固定。不得使用 top-level placement、其他 agent
创建接口或手写 parent label 替代 ORCHESTRATOR 的 agent-scoped 创建。

### dispatch_id 规范

dispatch_id 必须同时是 label 安全值和任务作用域冻结文件名安全值，格式为：

~~~text
^[0-9a-z][0-9a-z-]{0,31}$
~~~

创建、重跑和无效输出重试各分配新的 dispatch_id。同一次创建结果不明确时，恢复只允许
复用同一 task、role、purpose、candidate_identity 和 dispatch_id 的唯一 agent；确认是
新的创建尝试后必须使用新的 dispatch_id。

### 创建／恢复后核验

接受任何输出前，ORCHESTRATOR 必须核验：

1. agent ID 是当前 STATE 的 contextual_reviewer.agent_id；
2. workspace 等于当前 task 的 workspace_id；
3. labels.task_id、labels.role、labels.purpose、labels.candidate_identity 和
   labels.dispatch_id 精确匹配；
4. parent lineage 精确等于 orchestrator_agent_id；
5. 当前候选 envelope、工作树和 HEAD OID 未被修改；
6. 返回结果符合第六节 schema。

状态面无法暴露可验证 parent lineage 时，停止该 agent 并进入 WAIT_USER，不把不可验证
状态当作通过。

恢复查询必须先按 workspace／cwd 限定，再按 task_id、role、purpose、candidate_identity
和 dispatch_id 精确过滤，最后才进行 0／1／多匹配判定。列表被截断或完整性不可确认时，
不得视为零匹配。多个匹配或身份无法唯一确认时进入 WAIT_USER，不得盲目创建第二个 agent。

## 三、候选身份（candidate identity）

候选身份只绑定冻结的译文语境 payload，不绑定运行时载体。

### 规范 payload

payload 是一个 JSON object，包含恰好七个逻辑组件：

~~~json
{
  "contract": "translation_contextual_v1",
  "ordered_revision_keys": ["<key-1>", "<key-2>"],
  "translation_snapshot": [
    {"revision_key": "<key-1>", "source": "<冻结 source-1>", "target": "<冻结 target-1>"},
    {"revision_key": "<key-2>", "source": "<冻结 source-2>", "target": "<冻结 target-2>"}
  ],
  "fixed_source_identity": "<manifest 固定的来源身份>",
  "terminology_snapshot": "<渲染进 briefing 的精确术语子集字符串>",
  "bounded_context": [
    {"revision_key": "<key-1>", "context": "<source tags／runtime keys、邻近译文、公共源码证据片段>"},
    {"revision_key": "<key-2>", "context": "<source tags／runtime keys、邻近译文、公共源码证据片段>"}
  ],
  "rendered_briefing": "<计算身份前的最终渲染 briefing 字符串>"
}
~~~

约束（精确形状）：

- 根必须是 object，恰好包含七个声明的键；
- ordered_revision_keys 是 string array；translation_snapshot／bounded_context 是精确
  键 object array；其余组件是 string；
- 每个标量叶子必须是 string；null、boolean、numeric、额外键、缺失键和错误容器形状
  一律拒绝；
- 两个 array 必须与 ordered_revision_keys 一一对应并保持冻结顺序；
- rendered_briefing 可以提及结果字段名 candidate_identity，但不得嵌入已计算的 64 位
  十六进制 identity 值。

约束（语义值）：

- contract 必须精确等于 translation_contextual_v1；
- fixed_source_identity 必须精确等于候选适用的 manifest 固定来源身份，且按该来源机制
  仅可取以下两种 typed form：manifest 固定的公共 Git 源码为
  `commit:<40-lowercase-hex>`；受保护 DLC extraction snapshot 为
  `snapshot:<64-lowercase-hex>`；
- 必须由候选适用的 manifest 来源机制选择对应 form：公共 Git 源码不得使用 `snapshot:`，
  受保护 DLC extraction snapshot 不得使用 `commit:`；非空任意字符串、裸 hash、未知
  identity type、大小写不符或长度不符一律拒绝；
- revision key、source、target 和 context 必须与冻结候选的字节精确相等；
- 哈希自洽不足以证明候选正确；语义相等性在哈希前和接受返回结果前都必须执行。

### 规范序列化与身份

canonical contextual payload bytes = UTF-8 JSON 序列化：

- object key 递归按字节序排序，array 保持冻结顺序；
- 分隔符精确为逗号和冒号，无多余空白、无换行；
- ensure_ascii=false，字符串按 JSON 转义规则；
- 错误容器、非 string 标量、额外／缺失键使序列化失败。

~~~text
candidate_identity = SHA-256(canonical contextual payload bytes)
~~~

规范最小向量：

~~~text
{"bounded_context":[{"context":"tag=talents/foo; nearby: A, B","revision_key":"r1"}],"contract":"translation_contextual_v1","fixed_source_identity":"commit:61bb370c33e46c4df4b2bbfd56113a0de1822300","ordered_revision_keys":["r1"],"rendered_briefing":"有界语境审核 briefing：revision r1","terminology_snapshot":"术语：zone=区域","translation_snapshot":[{"revision_key":"r1","source":"Hello world","target":"你好，世界"}]}
~~~

该单行文本的 UTF-8 字节 SHA-256 必须由测试按同一 recipe 重算；它不含运行时选择。

### 派发 envelope 与冻结输入文件

ORCHESTRATOR 先计算 candidate_identity，再构造：

~~~json
{
  "candidate_identity": "<sha256>",
  "payload": {"…": "七个组件，原样不变"}
}
~~~

该 envelope 按相同的紧凑 JSON 规则写入：

~~~text
.ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json
~~~

文件必须是任务作用域内的普通 JSON 文件；每次创建尝试独立写入，不覆盖旧 dispatch。
它是候选输入的唯一载体，由 fresh REVIEWER 用只读 workspace 工具读取。

candidate_identity 的值不得进入被哈希的 payload 或 payload.rendered_briefing；它由外层
envelope、labels、STATE、review 记录和短 prompt 携带。返回结果必须回显相同值。
ORCHESTRATOR 在派发前、返回后和接受结果前都从 payload 重算 identity；payload、
envelope 和返回值三者不一致即作废。

该身份不得复用 code-diff 的 candidate_ref 配方。

## 四、短派发 prompt

initialPrompt（CLI positional prompt）只含以下三行，未实例化模板不超过 800 UTF-8 字节；
唯一动态值是 <candidate_identity> 和 <input_path>：

~~~text
任务：审核全部冻结 revision；据输入文件术语、上下文和所引固定源码，只报有证据的实质语义、机制、术语或关系错误，无问题填 OK。
输入：candidate_identity=<candidate_identity>；<input_path> 是唯一候选载体。全程只读，禁止写入任何文件；只读该文件及其所引译文/公开源码、docs/paseo-translation-context-review-v1-contract.md 第六节，不读其他 .ai/task/.ai/reviews。
输出：仅回第六节单一紧凑 JSON；冻结顺序全量覆盖并回显 <candidate_identity>；首字节{、末字节}，无其他文字、Markdown/围栏。
~~~

模板不内联 envelope、revision、source/target、术语、上下文、源码片段或其他候选数据。
CLI positional prompt 与 MCP initialPrompt 必须是相同文本；输出格式选项不携带 prompt
或 envelope。

## 五、输入（有界 briefing）

冻结 envelope 只包含：

- 精确 source/target 对；
- source tags／runtime keys；
- 术语子集；
- 同文件／同 section 的邻近译文；
- 固定版本公共源码证据片段。

禁止注入先前 finding、裁决决定、建议修复或任何宿主 lineage。

REVIEWER 只读取短 prompt 指定的精确 input_path、该文件明确引用的译文／公开源码，
以及本契约第六节；不得浏览其他 task 或 review 记录。

## 六、结果 schema 与校验（fail closed）

整个输出必须是单一紧凑 JSON object：

~~~json
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
~~~

全部通过才算有效记录：

1. contract 精确等于 translation_contextual_v1；
2. candidate_identity 匹配 ^[0-9a-f]{64}$ 且等于 envelope 值；
3. revisions 长度等于冻结 revision 数；
4. envelope、revision、evidence 各层 additionalProperties=false；
5. 每个 revision 恰好覆盖一次，集合和顺序都与冻结输入精确一致；
6. observation 非空；无问题必须使用 OK；
7. evidence 的 source／target 必须与冻结字节精确一致；
8. 不得填写 severity、确认状态、suggested fix 或任何未声明字段。

结果来源必须是 STATE 当前的 contextual REVIEWER agent，且 dispatch_id 与当前派发一致。
迟到、停止后的结果或候选改变后的结果一律作废。

## 七、只读与失败语义

派发前记录 HEAD OID，并对任务前脏／untracked 路径、冻结 envelope、关键编排状态做
有界精确快照；返回后逐路径比较。reviewer 的任何写入、HEAD 改变、冻结文件替换、候选
身份变化或 lineage／workspace／role／purpose 不匹配，都使输出无效并按基础设施错误处理。
不对整个干净仓库或整个 ignored 树做全量哈希。

创建、传输和查询错误按一般基础设施规则重试一次。若需要新会话，必须保持相同 role、
purpose、workspace、lineage 和 candidate identity，并为新创建尝试分配新 dispatch_id；
不得混用旧会话的部分输出。

## 八、分离与指标

语境审核和 code review 共享 Paseo 角色但不共享输入、输出、finding 或裁决。语境结果
只记录 observation 和 evidence；severity、确认状态和修复建议由 ORCHESTRATOR 根据固定
源码和项目政策独立产生。

本契约不定义质量 evaluator 的运行身份、预注册或稳定性指标。质量 evaluator 由其独立
质量契约管理，不能把本契约的单次语境审核自动解释为质量校准通过。

## 九、外发

常设外发权限按 role=reviewer、purpose=translation_contextual_v1 和第五节输入边界授予：
只发送冻结的有界语境 bundle 及其明确引用的译文／公开源码，不发送先前 finding、裁决或
建议修复。改变读取范围或目的仍需用户授权。

活动任务可以在下一次 contextual dispatch 前补齐 role、purpose、candidate_identity、
dispatch_id、input_path 和 agent_id；已完成任务和历史 review 记录不改写。
