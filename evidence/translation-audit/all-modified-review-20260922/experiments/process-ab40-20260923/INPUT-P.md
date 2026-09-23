# 独立只读审核 P
全量独立初审。
严格按 entries.json 顺序审完恰好 40 条。唯一允许输入：本文件、RULES.md、entries.json、context.lua、terms.json、source-access.json、FREEZE.json，以及 source-access 允许的源码。不得读取 entries.json 的非分配条目作为审核目标、其他阶段输入/报告、SPEC、SAMPLING、宿主记录或任何旧实验。context.lua 的邻文仅作语境，不额外报未分配条目。遵守 RULES.md 的判定口径和报告格式。最终直接返回完整报告，不写文件。
