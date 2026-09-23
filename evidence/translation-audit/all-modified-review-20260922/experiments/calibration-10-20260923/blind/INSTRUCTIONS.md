# 10条独立校准输入

本任务为用户明确授权的 Codex 内置子代理只读校准，不是正式生产批次。只读本目录的 entries.json、context-*.lua、terms.tsv、TERMINOLOGY.md、source-access.json 和本说明。不要读取本目录之外的报告、映射、分数、建议或其他模型输出；不要创建子代理或修改文件。TERMINOLOGY.md 的外部链接不扩大读取权限。

审核 entries.json 中 K01 至 K10 全部条目。先读完整段落及对应 context；不按遗漏单个英文词自动判错，也不因问题轻微自动降为建议。明确指出信息为何被改变、遗漏或由中文／上下文等价保留。已确认的细微信息遗漏仍算缺陷。不要给自己或模型打分。

术语行来自原冻结子集；本次明确提供当前 HEAD 的完整术语适用规则，按 scope、source_tag、category 与语境共同匹配。existing 不强制改名。不得扩大为全局术语决策。

可从每条 source_file 起沿实际符号或调用链读取 source-access.json 白名单中的单个 DLC 文件，读取前核对 SHA-256。只检查有关文件，禁止全文库搜索、读取其他语言 locales、读取当前生产译文来找答案。本体只能用 git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<相关单文件>。DLC 哈希固定，仓库、commit、目标版本映射未固定；快照事实与目标版本适用性分别记录。上游问题、中文新增与源码支持的可能上游纠正分开。

动态文本须分别检查可见的不同分支，记录实际拼接关系。可以直接展示文本组合，无需运行整个游戏；模拟输出不能宣称为游戏实测。

输出中文：

1. 恰好10行 K-ID | ISSUE/PENDING/ADVISORY/OK | claim编号或短理由。一条有confirmed则ISSUE；否则有pending则PENDING；否则有advisory则ADVISORY；否则OK。
2. 每个原子claim给原译精确短引、支持证据、最强反证／等价解释、裁定confirmed/pending/advisory/refuted、独立的影响说明，以及来源路径:行号。不要将一个有误的机制解释附在另一个真实文本缺陷上一起确认。
3. 对认为无问题的条目也给最重要的核验理由。存在语言解释分歧且无足够证据排除时保持pending或advisory，并明确区别二者。
4. 列所有实际读取路径、哈希核验结果、未解决的证据缺口。总输出尽量控制在6000中文字符左右；完整覆盖优先。

这些是模型校准观察，不是人工金标准，不宣称 DONE_VERIFIED。旧报告在本轮判断结束前不会提供。
