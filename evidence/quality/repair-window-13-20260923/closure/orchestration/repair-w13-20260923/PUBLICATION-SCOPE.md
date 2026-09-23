# 窗口13证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-13-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/52c71f8d968c2229e1d67f931e2585a4f32069ae74a26315acd0210ce9341aff.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-13-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window13-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window13-20260923-migration.json逐字复制到上列目标。迁移已成功（4 revision_changed、29824 unchanged、0 ambiguous/unmapped、4 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window13-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window13-20260923- 前缀命名）。

写 evidence/quality/repair-window-13-20260923/PUBLICATION.md，说明：
- 范围：259批4条确认（Self-Judgement 流血死亡信息“死得其所”改“罪有应得”；Body of Stone 描述改“化为石头”、恢复“强制位移”、冷却缩减按百分比；魔杖类型描述补“由强大的炼金术师和大法师制造”；Crushing Hold 用术语“全局速度”、补“每次抓取”、删 #RED# 后多余空格）。
- 任务 repair-w13-20260923：execute-01（codex/gpt-5.6-sol）实施4条；REVIEW(0)/full（codex/gpt-6-sol）3 OK/1 ISSUE（魔杖 Archmagi 与职业名“元素法师”不一致；宿主驳回：classes.tsv:22 仅约束职业名 birth descriptor name，非职业语境本库一致用“大法师”）；FINAL(1)/full（claude-opus-5-5）4 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 88dd316752e399c6d42957a7424bec1629773c23；新 catalog e3b869612116e4b4c4f837e0f0a35017d85f9793fdf80a1109226edf075df753；migration 52c71f8d968c2229e1d67f931e2585a4f32069ae74a26315acd0210ce9341aff；4个 successor 待重新审核，不继承 done。
- 所有 child（1 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口13已完成；待宿主发布收尾，随后审核260）”。
- 在现有“下一步按 1:1 节奏开修复窗口13……必须接 RE_REVIEW。”段后追加窗口13结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核260（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w13-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-13-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
