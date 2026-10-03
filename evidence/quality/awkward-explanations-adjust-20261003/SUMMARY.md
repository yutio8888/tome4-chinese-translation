# 生硬解释调整完成（2026-10-03）

按用户“请将这些条目进行调整”的要求处理前次扫描清单：13 条英文外机制扩写恢复到英文描述边界，3 条重复或生硬措辞精简，共 16 条，涉及核心 7、禁忌教派 5、乌鲁洛克之灰 2、兽人 2。SCAN-11、12、15、17 四条排除项保持原样。

这次是明确条目的有界文本调整，不重新裁定英文与游戏源码的机制差异，也不代表采用此前的机制解释。前次 [扫描裁决](../awkward-explanations-scan-20261003/REPORT.md) 保留为历史记录；逐条英文、修改前后文本与原因见 [CHANGES.json](task/CHANGES.json)。

独立复审 GPT-6.1 Sol 与全量终审 GPT-6 Astra 均 PASS；宿主另外逐字节和 LuaJIT 加载核对，四文件恰好 16 个 target 改变，source、source_tag、args_order、special、其余条目、参数占位符、标记和换行不变。SCAN-04 删除解释中的字面量 `25%%`，不改变参数占位符。

验证采用工作流“有界译文修改”矩阵：四组件 strict proposal、strict lint（30,308 条，0 错误、0 警告）、运行键冲突扫描（0）、重复键分类（1,711 个，全部 A，B/C 为 0）、严格完整核心 addon 构建与 DLC 实际消费者 dry-run 均通过。相同最终候选复用已完成的门禁，绑定文件 SHA-256 与真实命令输出见 [最终验证记录](dispatch-evidence/final-validation.json) 和 [命令回执](dispatch-evidence/validation-receipts.json)。

任务 `awkward-explanations-adjust-20261003` 已 DONE_VERIFIED；三次 child dispatch 全部确认归档。复审冻结输入、原始输出、身份／生命周期核验及宿主验证保存在本目录，[ARTIFACT-MAP.json](ARTIFACT-MAP.json) 说明精确字节恢复方式。仅本地提交；对外 0.3.2 仓库、标签、Release 和资产未变，用户既有无关改动保留。
