# 窗口24证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-24-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/534b8e86c940f0be3dedb147e8e3381b12ec2a101b5b70958e3181b7ad8d41cd.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-24-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-24-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window24-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window24-20260923-migration.json逐字复制到上列目标。迁移已成功（6 revision_changed、29822 unchanged、0 ambiguous/unmapped、6 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window24-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window24-20260923- 前缀命名）。

写 evidence/quality/repair-window-24-20260923/PUBLICATION.md，说明：
- 范围：270批6条确认（飞镖发射器抵抗日志“睡眠”改“镇静”，与效果名“被镇静”一致；敏锐直觉说明去掉增译的“直觉”并恢复原文 3 行；狂热说明改为 4 次快速攻击、每次攻击造成伤害、附近有被追踪的猎物时总是攻击它，并恢复盾牌句前的空行；奥术至上法杖描述恢复两句间换行，末句改为“单独一件时似乎并不完整”（该法杖与奥术理解之帽成套）；吸食抗性说明删去多余换行恢复 2 行；意志属性说明删去增译的“精神力”）。
- 任务 repair-w24-20260923：execute-01（codex/gpt-5.6-sol）实施6条，宿主逐条逐行核对行数、空行下标与行首 TAB；REVIEW(0)/full（codex/gpt-6-sol）6 OK；FINAL(1)/full（claude-opus-5-5）6 OK，收敛，无修复轮。完整门禁全部通过含严格构建，DONE_VERIFIED。
- 译文提交 fc091427e93c42cd73fad1b49cd450580e9778e8；新 catalog 6870324089f8919e8cef200a38011d2493e276ac717690655f2abede3c1b7b3c；migration 534b8e86c940f0be3dedb147e8e3381b12ec2a101b5b70958e3181b7ad8d41cd；6个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 所有 child（1 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口24已完成；待宿主发布收尾，随后审核271）”。
- 在审核270段（以“范围见 `.ai/task/batch-b7ce18a7bdce48ba8086/WINDOW24-REPAIR-DECISION.json`。”结尾）后追加窗口24结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核271（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w24-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-24-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
