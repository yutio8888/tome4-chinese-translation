# 窗口9证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-9-20260923/（保留已有 IMPLEMENTATION.md、FIX-R0.md、VALIDATION.json 等实施报告）
- evidence/quality/pending-user-review.md（追加，见下）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/bdf355b65bef33ded7ac24e48c577770f33d67312fed83ab8de9d1f4c4a538d1.json

不改Lua、术语、规则、工具、旧证据、.ai；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中259项、共1987893 bytes到evidence/quality/repair-window-9-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。本包同时含已取代的 STOP 任务 repair-w9-20260923 及其复审记录。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window9-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window9-20260923-migration.json逐字复制到上列目标。迁移已成功（5 revision_changed、29823 unchanged、0 ambiguous/unmapped、5 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.ai/task/repair-w9-20260923/ 下 ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-F2.json、ADJUDICATION-FINAL.json（以 w9- 前缀命名）；.artifacts/i18n/repair-window/下 window9-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json。

写 evidence/quality/repair-window-9-20260923/PUBLICATION.md，说明：
- 范围：255批5条确认（高阶奇术师解锁文本、潜行说明、runes active、夏之眼、回归之杖描述）。
- 首轮任务 repair-w9-20260923：REVIEW/full（codex/gpt-6-sol）4 OK/1 ISSUE（nothing else 确认修复；Flame 名称转 pending 并恢复基线“火球术”）；FINAL F1（claude-opus-5-5）4 OK/1 ISSUE（回归之杖换行确认修复）；FINAL F2 4 OK/1 ISSUE（潜行第2、6行删限定词确认修复）；FINAL F3 5 OK/0 ISSUE；门禁17/17。但宿主在 FINAL 失败后直接进入下一轮 FINAL 而非 RE_REVIEW，违反 translation_v2_convergence 阶段结构，无法 DONE，故以 STOP_VERIFIED 关闭（原因记录在其 STATE.last_error）。
- 重跑任务 repair-w9b-20260923：唯一EXECUTOR逐字应用首轮收敛文本（与 CANDIDATE-FINAL 逐字节一致），REVIEW(0)/full（gpt-6-sol）5 OK、FINAL(1)/full（opus-5-5）5 OK，不再开修复轮；完整门禁 run.hna9wv8w 17/17 含严格构建；DONE_VERIFIED。
- 译文提交 78be6b5a752cb5a24d0ef1e8337f0ba301180f21；新 catalog 0e554a74d6738064f4245525bed6f1be8a8463ea3df7f683ab2327e0fe0de510；migration bdf355b65bef33ded7ac24e48c577770f33d67312fed83ab8de9d1f4c4a538d1；5个 successor 待重新审核，不继承 done。
- 所有 child（首轮 4 个 executor 与 4 个 reviewer 共 8 个、重跑 3 个）均已归档确认；本 publication child 待宿主归档。

evidence/quality/pending-user-review.md 追加一节“修复窗口 9 待审阅”，新增第 7 项：
7. `e9e627f60c`（高阶奇术师解锁文本中的 Flame 名称）
   - 英文要点：`Flame, Manathrust, Lightning, Pulverizing Auger and Ice Shards permanently become 3-wide beam spells`。
   - 现译：“火球术”（基线，窗口9保持不变）。
   - 争议理由：术语库 terminology/talents.tsv:117 `Flame=火球术`（status=existing），职业说明 mod-tome.lua 亦用“火球术”；但运行时技能名（mod-tome.lua / mod-boot.lua / engine.lua 的 talent name 行）为“火焰”。统一方向属术语决定。
   - 建议选项：改技能名为“火球术”并同步术语 / 改说明与术语库为“火焰”。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口9已完成；待宿主发布收尾，随后审核256）”。
- 把现有“审核255……下一步开修复窗口9……”段后追加窗口9结果（按 PUBLICATION.md 摘要，含 STOP+重跑说明、提交、catalog、migration、Flame pending）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核256（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w9b-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-9-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
