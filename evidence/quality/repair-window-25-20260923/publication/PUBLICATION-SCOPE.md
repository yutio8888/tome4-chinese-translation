# 窗口25证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-25-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/f2ddf2cbd8e0610b40955d746594ed530f3dbadc05dee7153fff88b708434f38.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-25-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-25-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window25-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window25-20260923-migration.json逐字复制到上列目标。迁移已成功（8 revision_changed、29820 unchanged、0 ambiguous/unmapped、8 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window25-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window25-20260923- 前缀命名）。

写 evidence/quality/repair-window-25-20260923/PUBLICATION.md，说明：
- 范围：271批8条确认（疲劳圣印：经过圣印的敌人会减速；指令水晶球（亡灵）：“黑暗的幻象充满你的脑海”；血祭施法效果：“堕落系法术消耗生命值而非活力值”；减速说明恢复末尾换行与缩进；摄魂剑·莫瑞格日志：“汲取了%s的被困灵魂，施展%s”；第一滴血：补回“命中时”与“（若能标记）”；阿马克泰尔壁画 lore 逐句重译；盗匪首领日志恢复威胁语气与“绑在柱上烧死”）。
- 任务 repair-w25-20260923：execute-01（codex/gpt-5.6-sol）实施8条，宿主逐条逐行核对行数、空行下标与行首 TAB；execute-01 原生日志含 2 次 Codex `wait` function_call，仓库解析器白名单未收录，宿主经仅增补这两类条目的临时解析器副本收取（见 HOST-EXECUTOR-AUDIT.json）。REVIEW(0)/full（codex/gpt-6-sol）7 OK、1 ISSUE：血祭施法效果的英文原句本身与 incVim 实现不符（仅在活力不足时以生命支付缺额），译文忠实原句，宿主判 advisory，登记 pending 第 19 项；FINAL(1)/full（claude-opus-5-5）8 OK，收敛，无修复轮。完整门禁全部通过含严格构建，DONE_VERIFIED。
- 译文提交 805a9f155dff64cc18cf644b0af2856b0936e06f；新 catalog 38cb5f33c905a333728676e30a67692632830852be8790e532980702de21a18f；migration f2ddf2cbd8e0610b40955d746594ed530f3dbadc05dee7153fff88b708434f38；8个 successor 待重新审核，不继承 done。本窗口新增 pending 第 19 项（宿主维护 pending 文件）。
- 所有 child（1 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口25已完成；待宿主发布收尾，随后审核272）”。
- 在审核271段（以“范围见 `.ai/task/batch-ae5b45a9e4a7a8ffdb3e/WINDOW25-REPAIR-DECISION.json`。”结尾）后追加窗口25结果（按 PUBLICATION.md 摘要，含提交、catalog、migration、pending 第 19 项）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核272（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w25-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-25-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
