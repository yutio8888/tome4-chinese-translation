你是本批次的只读译文复核员。用中文自然语言作答，不要求 JSON。

工作区：/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921

只读文件：
- evidence/translation-audit/all-modified-review-20260922/batches/batch-075.md
- evidence/translation-audit/all-modified-review-20260922/source-access.json

禁止读取：其他 batches、reports、STATE.json、PROGRESS.md、HUMAN-REVIEW.md、cross-*.md、HANDOFF、INVENTORY-CORRECTIONS，以及任何已有审核意见。禁止修改、创建或删除任何文件。禁止派发子代理。禁止自动修复或改术语。

本次是部分补跑：上一次派发的报告在 entry-02425 中途截断。**只核 entry-02425、entry-02426、entry-02427、entry-02428 这 4 条**，冻结 SHA-256：05d4a4b7207fc5fcb07c8283cfc3d35709929576cbe7d1f12217c34296e35a90（开始前核对）。其余 36 条不要重复复核，也不要读取任何已有结论。

规则：
- 允许同 section 语境，以及 source-access.json 规定的固定公开源码；engine/tome 用 git show 读固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63。不得只凭英文或属性名推断机制。术语不能压过源码。
- 核对占位符、颜色码、换行、标点和参数顺序。
- 没有疑点的条目也要列出编号并写「未发现问题」，附简短可核验依据；有疑点写「存在疑点」或「细微观察」，给出可核验依据。不要自行宣布最终裁决。
- 核对到足够证据后，立刻把全部 4 条的完整报告作为最终回复一次写完。

最终回复就是完整复核报告。不要把报告写进仓库。
