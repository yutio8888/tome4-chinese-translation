# 窗口17证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-17-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/5168dcc75a66cf6b89dc5c5ee1f0753064d427cc9461ad4a7ca1680c0fb084ec.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-17-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window17-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window17-20260923-migration.json逐字复制到上列目标。迁移已成功（5 revision_changed、29823 unchanged、0 ambiguous/unmapped、5 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window17-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window17-20260923- 前缀命名）。

写 evidence/quality/repair-window-17-20260923/PUBLICATION.md，说明：
- 范围：263批5条确认（猎头者挑战播报改为“你取下了 %s 的首级，令本层所有敌人为之迟疑”，不再误述为“暂停”；Exploit Weakness 写明近战攻击命中并恢复结尾 \n\t\t；单项效果抵抗提示改为“效果抵抗几率/完全抵抗该特定效果的几率”；教程完成文本删去 3 处词中硬换行，LF 14→11；思维形态说明恢复原文换行结构 LF 7→3，warrior 改用本库“战士”）。
- 任务 repair-w17-20260923：execute-01（codex/gpt-5.6-sol）实施5条；REVIEW(0)/full（codex/gpt-6-sol）4 OK/1 ISSUE，确认 R0-HEADHUNTER-OVERSTATE（execute-01 增译“失去对你的锁定”扩大了 setTarget 的实际范围）；execute-02 仅删去增译分句；FINAL(1)/full（claude-opus-5-5）5 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 8390dd69d6d3ea359ada0ea2ea838cd533e14aa4；新 catalog 78635878a70f7ff2d9a1d4e36e7ad9115ab8a80d906670ecff0fce7332abd239；migration 5168dcc75a66cf6b89dc5c5ee1f0753064d427cc9461ad4a7ca1680c0fb084ec；5个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 所有 child（2 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口17已完成；待宿主发布收尾，随后审核264）”。
- 在审核263段（以“FINAL 中任何 ISSUE（即使宿主判 advisory）都会让 DONE 检查失败。”结尾）后追加窗口17结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核264（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w17-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-17-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
