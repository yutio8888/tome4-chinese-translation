# 本轮机制改写撤回完成

用户授权仅在翻译仓库撤回本轮因英文与代码不一致而采用的机制改写，保留普通翻译修正；对外 v0.3.2 仓库、标签、Release 和资产保持原样。本次没有 push 或外部发布。

盘点修正前 `bfde8c53d50b065837ff34dc08639f7dbc5816f5` 至撤回前 `a8f2260c28d07ac3136d4e44aa0d3e4d76882c90` 的全部 165 条差异：28 条完整保留普通修正，122 条撤回机制改写，15 条按子句撤回机制改写并保留普通修正。共改动 137 个 target：主包 72、恶魔余烬 8、禁忌邪教 14、兽人战役 43；engine.lua 未变。

最终逐条采用状态以 [完整三方对照](task/CANDIDATE-FINAL_REVIEW-2-1.json) 为准；executor 初稿和 cycle 1 记录保留为历史，不覆盖最终对照。MMR-026“生命汲取（物理）”及 UPSTREAM054 撤销误报的既有决定保留。原机制修正任务的工作集、源码证据和审核记录全部未改写；此次撤回采用不表示重新证明英文或旧译文的机制正确性。

独立范围复审通过；首轮终审发现毒镖“命中”普通修正被一并撤回，宿主依英文 struck 确认，EXECUTOR 精确修复。第二轮完整终审通过。任务 `mechanics-rollback-20261003` 已 DONE_VERIFIED，6 次 child dispatch 均已确认归档，无未解决的 accepted finding。参见 [终态](task/STATE.json)、[最终复审](reviews/review-03.json) 与 [完成检查](dispatch-evidence/done-check.json)。

按有界译文维护验证矩阵完成验证：LuaJIT 全字段与 target 外原始字节不变证明；165 条的占位符、markup 和换行不变量；strict lint 30308 条、0 错误、0 警告；运行键冲突扫描和分类；严格核心 addon 构建；DLC 实际消费端 dry-run；工作树及本次暂存文本空白检查。最终 Lua 文件哈希绑定于 [验证结果](dispatch-evidence/final-validation.json)。工具、流程、术语数据均未修改，未扩大到无关工具测试或新的源码机制审查。

已保留用户原有文档、生产工作集等无关改动。后续讨论建议见 [撤回决定](WITHDRAWAL-DECISION.md)，尚未作为新规则实施。此前连续机制修正已被本次撤回与讨论任务替代，不从旧交接推导继续修改或发布授权。

审计镜像按 [ARTIFACT-MAP.json](ARTIFACT-MAP.json) 映射到原冻结路径；patch 和原始输出采用确定性 gzip 保存，解压后逐字节哈希与原件相同。恢复审计时在独立 checkout 中按映射解压，不覆盖活动任务。baseline／pre-repair 的 Lua 快照可按 BASELINE.json 两个提交恢复。体积较大的 fix-1 预运行文件哈希表只保留条目数及规范化摘要，其余人工判断和不可重生成核验记录完整保存。
