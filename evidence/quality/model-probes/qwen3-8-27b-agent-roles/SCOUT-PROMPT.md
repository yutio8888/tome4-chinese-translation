你是只读 SCOUT。只允许读取以下两个根目录，不得创建、修改或删除任何文件：

- `/home/yun/projects/t-engine4`
- `/home/yun/research/tome4-agent-eval`

任务：在固定 ToME4 源码中核验 Tannen 传送门任务对 `Orb of Many Ways` 的处理。找出“交出水晶球”和“拒绝交出水晶球”两条路径：各自是否从玩家物品栏移除水晶球、设置什么任务状态，以及后续 Telmur 开启所需材料如何被移除。追踪关键调用或数据定义，不依赖现有 adjudication 的结论。

禁止读取 `evidence/quality/model-probes/` 下除本 prompt 外的文件，也不要读取文件名含 `adjudication`、`.ai/task` 或 `.ai/reviews` 的内容。

最终仅输出一个 JSON object：

{"context":"简洁结论","files_read":["绝对路径"],"symbols":["符号或状态名"],"source_evidence":[{"path":"绝对路径","line_start":1,"line_end":1,"fact":"源码事实"}],"open_questions":[]}

`files_read` 必须列出实际读取的全部文件；证据行号必须可复核。不要输出 finding、severity 或修复建议。
