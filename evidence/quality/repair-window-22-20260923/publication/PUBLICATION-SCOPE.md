# 窗口22证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-22-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/1cd5583de937a86439dcbc7ae0c2953e201574c2c53aa687ab592d39a5479508.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-22-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-22-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window22-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window22-20260923-migration.json逐字复制到上列目标。迁移已成功（6 revision_changed、29822 unchanged、0 ambiguous/unmapped、6 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window22-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window22-20260923- 前缀命名）。

写 evidence/quality/repair-window-22-20260923/PUBLICATION.md，说明：
- 范围：268批6条确认（欺诈斗篷生效日志改“一层幻影出现在#Target#周围，让%s看起来像人类”；电鳗尾炼金说明改“电鳗到哪儿为止、尾巴又从哪儿开始？其实没多大关系”；厄奇斯成就补“疯狂的”与“猛攻”；太阳堡垒创建者挂坠改“赤铁矿之月遮蔽金色太阳”；腐化蒸汽补主语“腐化的蒸汽在目标位置升起”；分裂（Mitosis）补视线内、召唤上限、技能激活期间三处限定并恢复为与原文一致的 7 行）。
- 任务 repair-w22-20260923：execute-01（codex/gpt-5.6-sol）实施6条；REVIEW(0)/full（codex/gpt-6-sol）5 OK/1 ISSUE，确认欺诈斗篷漏“出现”；execute-02 修复；FINAL(1)/full（claude-opus-5-5）5 OK/1 ISSUE，确认电鳗句把 stop 译成起点（宿主 SPEC 措辞所致）；execute-03 修复；RE_REVIEW(2)/full（codex/gpt-6-sol）5 OK/1 ISSUE，宿主驳回（Cunning=灵巧 为本库属性名）；FINAL(3)/full（claude-opus-5-5）6 OK，收敛。完整门禁全部通过含严格构建，DONE_VERIFIED。
- 译文提交 e3ad691d2819f29598d974d99d0139a3b373de20；新 catalog b239aafd8d5887f41de2065795f6913737ac9847cac1725c390e2fc2a421a197；migration 1cd5583de937a86439dcbc7ae0c2953e201574c2c53aa687ab592d39a5479508；6个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 教训：SPEC 中给出的示例译文本身也须逐词对照原文。
- 所有 child（3 个 executor、4 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口22已完成；待宿主发布收尾，随后审核269）”。
- 在审核268段（以“范围见 `.ai/task/batch-35fcb3df1560de7c5b2d/WINDOW22-REPAIR-DECISION.json`。”结尾）后追加窗口22结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核269（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w22-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-22-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
