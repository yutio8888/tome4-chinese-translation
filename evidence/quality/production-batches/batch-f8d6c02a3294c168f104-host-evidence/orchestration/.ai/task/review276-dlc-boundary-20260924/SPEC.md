# 第 276 批 DLC reviewer 源码定位边界修复

用户 2026-09-24 授权修正规则并重派。当前 Ashes DLC contextual reviewer 两次用 `find /` 扫描根目录，均已归档并拒收。原始输出不得进入 review record。

目标：
1. 前瞻性更新 contextual v2 固定三行 prompt、role 和契约：明确禁止从 `/` 或其他无关目录做全盘搜索；仅允许 envelope 指定的源码位置及相关调用链。保持 800 UTF-8 字节限制、现有 JSON schema 和 reviewer 只读边界。
2. 为第 276 批 DLC contextual 输入提供可核验的精确源码 checkout 位置 `/workspace/tome4-dlcs/ashes-urhrok`，只作本批本机取证定位，不把本机路径写成 DLC 版本来源或全局常量。必须保证每个实际引用文件仍按受跟踪 workset 的 SHA-256 匹配；来源/commit 未固定仍如实标记。
3. 支持在两个已归档无效 dispatch 之后按新冻结事件生成新的 candidate/input 路径和 task 绑定，旧 envelope、candidate、raw、diagnostics 不改写；重新执行 anchor preflight、stage、dispatch。若消费者不支持安全重冻，实现最小必要恢复入口，fail closed；不得手改 checkpoint 绕过工具。
4. 增加定向测试验证 prompt/契约一致、限长、源码边界、重冻不可改旧输入且不会混入旧无效输出。不要写仅镜像实现的测试。
5. 不改翻译、术语或源 workset，不执行 reviewer、不提交或 push。报告修改文件和验证结果。

允许的任务内容文件：`.ai/roles/reviewer.md`、`docs/paseo-translation-context-review-v2-contract.md`、`docs/paseo-orchestration-v2-contract.md`、`tools/orchestration/review_prompts.py`、`tools/orchestration/dispatch_contextual.py`、`tools/i18nlib/production_review_v2_lite_batch.py`、`tools/orchestration/stage_contextual.py`、`tools/orchestration/build_evidence_pack.py`、`tests/i18n/test_review_prompts.py`，以及完成上述目标所必需的有界新工具/测试文件。任何扩大范围先向 ORCHESTRATOR 说明。
