你是有界 EXECUTOR。工作目录是 `/home/yun/research/tome4-agent-eval`。

唯一允许修改的文件：
`evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua`

完成以下三个精确修复：

1. 第一条保留 `args_order={2,1}` 的占位符绑定，并补回英文 `up to` 的“最高”限定。
2. 第二条把 `all other creatures` 明确译为“所有其他生物”，不能遗漏 `other`。
3. 第三条明确伤害数值是“每个被清除的负面效果”分别贡献的护盾格挡量；不得改动占位符顺序。

只改三个 target 字符串；source、source_tag、special、args_order、文件结构和缩进均不得改变。不得修改、创建或删除其他文件，不得 commit 或 stage。

修改后运行：

- `git diff --check -- evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua`
- `git diff -- evidence/quality/model-probes/qwen3-8-27b-agent-roles/executor-fixture.lua`

最后简洁报告变更文件、测试结果、计划偏差和尚未解决的问题。
