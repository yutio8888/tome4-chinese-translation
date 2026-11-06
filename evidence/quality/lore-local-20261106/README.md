# Lore 局部修复（2026-11-06）

用户 2026-11-06：「对于局部修改的lore需要慎重，如果修改后复审又发现问题，应当考虑重译。」

- 输入：lore-screen-20261105/summary.json 中 final=LOCAL 的 169 条，按文件顺序切为 9 块（chunk-NN.json，每块约 60K 英文字符），附 A/B 两位筛查者各自的问题描述。
- 执行：每块一个 codex/gpt-6.1-sol EXECUTOR（prompt：~/tome-live/prompts/lore-local.md），逐条核实问题、整句重写、不动未点名段落；问题过多的条目标 ESCALATE 不改。报告存 report-NN.json。
- 复审：每块修改后进 lite 盲审（A/B，不告知修改原因）。复审仍对已局部修改的条目报出问题的，该条目升级为 Gemini 4 Argon 整篇重译，不再做第二轮局部修补。
