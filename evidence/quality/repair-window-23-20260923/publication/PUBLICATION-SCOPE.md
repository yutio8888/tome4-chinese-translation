# 窗口23证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-23-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/d2075cb1e0938d0607405e8d8d85400e38b06f9245584e5838e455993014585f.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-23-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-23-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window23-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window23-20260923-migration.json逐字复制到上列目标。迁移已成功（3 revision_changed、29825 unchanged、0 ambiguous/unmapped、3 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window23-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window23-20260923- 前缀命名）。

写 evidence/quality/repair-window-23-20260923/PUBLICATION.md，说明：
- 范围：269批3条确认（夺心魔任务开场补“至少”：“你被派去至少清除一个对夺心魔的威胁。”，保留末尾换行；埃亚尔之怒说明补“你周围的”；奥术漩涡说明改为射线射向视野内随机敌人、对附着目标与射线路径上所有目标造成伤害，无敌人时为本回合漩涡对附着目标造成的伤害提高 50%，目标死亡残余伤害转半径 2 奥术爆炸）。
- 任务 repair-w23-20260923：execute-01（codex/gpt-5.6-sol）实施3条；REVIEW(0)/full（codex/gpt-6-sol）2 OK/1 ISSUE，宿主核 timed_effects/magical.lua:2686-2687（624a673）确认无敌人分支是一次 eff.dam*1.5 伤害而非目标易伤；execute-02 修复该句；FINAL(1)/full（claude-opus-5-5）3 OK，收敛。完整门禁全部通过含严格构建，DONE_VERIFIED。
- 译文提交 78c3562727a947c49dd8ec65daff61707920b893；新 catalog c975ad861660d866b62f8d2530be93926af2977852846d6367216e28e5d9e480；migration d2075cb1e0938d0607405e8d8d85400e38b06f9245584e5838e455993014585f；3个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 所有 child（2 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口23已完成；待宿主发布收尾，随后审核270）”。
- 在审核269段（以“范围见 `.ai/task/batch-cfd398e96c387cc31dc0/WINDOW23-REPAIR-DECISION.json`。”结尾）后追加窗口23结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核270（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w23-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-23-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
