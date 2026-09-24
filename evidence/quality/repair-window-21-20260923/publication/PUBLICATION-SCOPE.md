# 窗口21证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-21-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/e0b1d6770808ef8df692f46880076b2b792443a54134343b39bd72edf34400c2.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-21-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-21-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window21-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window21-20260923-migration.json逐字复制到上列目标。迁移已成功（5 revision_changed、29823 unchanged、0 ambiguous/unmapped、5 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window21-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window21-20260923- 前缀命名）。

写 evidence/quality/repair-window-21-20260923/PUBLICATION.md，说明：
- 范围：267批5条确认（Sun Flare 技能名按维护者2026-09-23批准由“日珥闪耀”改为“太阳耀斑”；敏捷防御格挡日志“(%d 敏捷防御)”误作技能名，改为“(%d 被抵挡)”，与同技能说明“抵挡攻击”一致；荒芜遗迹 lore 删去原文没有的换行与制表符；Solipsist 引言改“世界是其居民共同的梦……发掘梦境的潜能”；静电网说明补“每停留一回合”累加机制，3 个换行与制表符保持）。
- 任务 repair-w21-20260923：execute-01（codex/gpt-5.6-sol）实施5条；REVIEW(0)/full（codex/gpt-6-sol）4 OK/1 ISSUE，判 advisory（技能名行“静电网络”与说明“静电捕网”不一致，技能名行不在本窗口，留待后续窗口）；FINAL(1)/full（claude-opus-5-5）4 OK/1 ISSUE，确认日志“被偏转”与同技能说明“抵挡”不一致；execute-02 改为“被抵挡”；RE_REVIEW(2)/full（codex/gpt-6-sol）5 OK；FINAL(3)/full（claude-opus-5-5）5 OK，收敛。完整门禁全部通过含严格构建，DONE_VERIFIED。
- 译文提交 5342f1b06943cefb1d9f393d2a186c9c6cc8a6e6；新 catalog b7389c85c66e7e755fd3904f3072ca0d5688901a6bb548f8e662f4c11a9f77ae；migration e0b1d6770808ef8df692f46880076b2b792443a54134343b39bd72edf34400c2；5个 successor 待重新审核，不继承 done。本窗口无新增 pending；advisory“静电网络”技能名留作后续修复候选。
- 教训：SPEC 指定替换词前须先查同技能相邻条目（尤其 info）已用译法。
- 所有 child（2 个 executor、3 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口21已完成；待宿主发布收尾，随后审核268）”。
- 在审核267段（以“helper 从窗口20复制（条数 7→5）。”结尾）后追加窗口21结果（按 PUBLICATION.md 摘要，含提交、catalog、migration、太阳耀斑改名与“静电网络” advisory）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核268（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w21-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-21-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
