# 窗口15证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-15-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/de68e389782940517c064da7cdaaa19d6207e7dc1da4c1ca4dc5728b05e25d71.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-15-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window15-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window15-20260923-migration.json逐字复制到上列目标。迁移已成功（2 revision_changed、29826 unchanged、0 ambiguous/unmapped、2 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window15-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window15-20260923- 前缀命名）。

写 evidence/quality/repair-window-15-20260923/PUBLICATION.md，说明：
- 范围：261批2条确认（半身人创世论 lore/misc.lua:214–235：other gods were responsible 误作“其他创造者也很负责”并漏 lesser gods copied his grand design、ridiculous ideals 误作“可笑形象”、entitlement 心态被写成既成所有权，并逐句修正其余明显增删；半身人遗迹紧急召回提示删去原文没有的“救他”，改“发誓日后再回来”）。
- 任务 repair-w15-20260923：execute-01（codex/gpt-5.6-sol）实施2条；REVIEW(0)/full（codex/gpt-6-sol）2 OK；FINAL(1)/full（claude-opus-5-5）1 OK/1 ISSUE，确认 F1-LORE-PRESUME-LOGIC（232 夏·图尔段推测语气颠倒、234 众神冲突前提被降为并列选项），execute-02 有界修复末两段；RE_REVIEW(2)（gpt-6-sol）2 OK；FINAL(3)/full（claude-opus-5-5）2 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 a039ff12c97f0c2f5071f7111442b17b465166f3；新 catalog f4d10da25eb9e968b74997635ef6bcb09cdaf25095caef96a3f220db494c660b；migration de68e389782940517c064da7cdaaa19d6207e7dc1da4c1ca4dc5728b05e25d71；2个 successor 待重新审核，不继承 done。
- 所有 child（2 个 executor、4 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口15已完成；待宿主发布收尾，随后审核262）”。
- 在现有“下一步按 1:1 节奏开修复窗口15……失败的 FINAL 之后必须接 RE_REVIEW。”段后追加窗口15结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核262（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w15-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-15-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
