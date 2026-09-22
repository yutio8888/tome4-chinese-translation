# 清单更正

首版临时统计 4123 未完整计入 merge commit 对其他组件的修改。现对每个 first-parent commit（含 merge）与其第一父提交逐文件比较，最终每个组件的语义记录再与冻结 HEAD 全量相等核对，得到 4144 条、11 组件。

先前抽查 11 条中的 Night Terror/talent name 在本轮基线与终点之间未修改；旧抽查提取以 section/source 对应而未区分 source_tag，误把同名 _t 条目的译文作为对比。该条保留为历史额外覆盖，不计本轮已修改清单；其余 10 条可复用。新清单使用 section/source/source_tag/occurrence 区分，不按 source 单独匹配。
