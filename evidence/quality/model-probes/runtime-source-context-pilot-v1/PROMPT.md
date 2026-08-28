# 机制翻译独立审核

你将收到 36 条按固定顺序排列的英文 `source` 与中文 `target`。部分输入还含有 `source_context`；它是从固定公开源码机械截取的原始 Lua 代码。

逐条判断中文是否对客观语义或运行时机制做出了错误陈述。只审核可由当前输入直接支持的客观问题；不要报告文风、措辞偏好、标点或术语风格。源码与英文描述冲突时，以可执行源码为准。没有 `source_context` 时，不要仅因中文包含英文未写出的额外细节就判错；缺少证据本身不是错误，也不要凭外部知识猜测。

每条只能给出一个最重要结论：

- `OK`：当前输入不能支持客观错误主张，`claim` 必须为 `null`。
- `FINDING`：当前输入直接证明存在客观错误。
- `UNCERTAIN`：当前输入给出了具体、可定位的冲突迹象，但不足以确定；不得把泛泛怀疑写成 `UNCERTAIN`。

非 `OK` 时，`claim` 必须包含：

- `target_span`：从该条 `target` 原样复制的、最小且连续的错误片段；必须是精确子串。
- `claim_type`：只能是 `VALUE`、`DIRECTION`、`CONDITION`、`SUBJECT`、`TIMING`、`SCOPE`、`ACTION`、`STATE`、`ORDER` 或 `OTHER`。
- `correction`：说明该片段应表达的客观事实，简洁明确。
- `evidence`：从该条 `source` 或 `source_context` 原样复制的一段直接证据；必须是精确子串，不得引用别条。

`observation` 用一句简短中文概括判断。不要提及实验、分组、变异、标签、reference、历史记录、模型来源、文件路径或你看不到的资料。不得使用工具或外部知识。严格覆盖全部 36 条，保持输入顺序与 ID，不得增删、合并或改序。只输出符合给定 schema 的 JSON。
