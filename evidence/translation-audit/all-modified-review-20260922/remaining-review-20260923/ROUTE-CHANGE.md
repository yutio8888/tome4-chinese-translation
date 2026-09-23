# CPA 通道续审

用户在检查 Agy 尾输出后明确要求“请尝试用CPA通道继续”。2026-09-23 起，剩余 Gemini 初审改用 Paseo → Pi → `cpa/gemini-3.8-flash-high`，thinking=high；GPT 6 Sol 交叉路由保持 `codex/gpt-6-sol`。CPA 精确模型 ID 来自本次实时 `list_models(pi)`，未用别的模型替代 Gemini。上游模型名称是提供商声明及运行元数据，未作独立鉴定。

此前失败的 rem-05 两次运行，经 [原生输出检查](OUTPUT-RECOVERY.json) 确认没有完整报告，不计覆盖。原冻结 [BATCHES.json](BATCHES.json) 与 [FREEZE.json](FREEZE.json) 不变；尚未完成的较大批次被有界拆分为最多 20 条，执行顺序见 [EXECUTION-BATCHES.json](EXECUTION-BATCHES.json)，新增输入哈希见 [EXECUTION-FREEZE.json](EXECUTION-FREEZE.json)。原 308 个 ID、源译内容和顺序不变。

Gemini 调用仍串行。报告是否可采用依据内容完整性与覆盖检查，不单凭进程终态：完整但超时的报告可保留使用；缺少最终报告的运行只保留失败记录。
