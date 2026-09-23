# 窗口14证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-14-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/a3f47a5e5f30a66b9a56b4ba416a571a91a906ea9562229f4e4c52d5c8632d1d.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-14-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window14-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window14-20260923-migration.json逐字复制到上列目标。迁移已成功（3 revision_changed、29825 unchanged、0 ambiguous/unmapped、3 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-R1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window14-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window14-20260923- 前缀命名）。

写 evidence/quality/repair-window-14-20260923/PUBLICATION.md，说明：
- 范围：260批3条确认（珠宝师对话 Wintertide Moon 传说：补“融化”、删增添的“融入大地”、“更强大”改“强力”，月亮名定为“霜华之月”；Guided Shot 补 telekinetic nudges 念力微调与“精确地”；巨狼描述 snaps at you 改“朝你猛咬”）。
- 任务 repair-w14-20260923：execute-01（codex/gpt-5.6-sol）实施3条；REVIEW(0)/full（codex/gpt-6-sol）3 OK，宿主另立发现 R0-HOST-WINTERTIDE-NAME（“冬潮之月”沿用了宿主 SPEC 措辞，本库既有名为“霜华”）并由 execute-02 修为“霜华的一部分”；RE_REVIEW(1)（gpt-6-sol）2 OK/1 ISSUE，确认 R1-WINTERTIDE-MOON-SENSE（裸“霜华”兼作日历月份名，丢失“月亮”义；elvala 传说已用“霜华之月”），execute-03 改为“霜华之月的一部分”；RE_REVIEW(2)（gpt-6-sol）3 OK；FINAL(3)/full（claude-opus-5-5）3 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 5babfdaf1c331e52df1efc5480794457449f4c99；新 catalog fb1a42e597f4bcec63cb05b5ed0d66aa29272e60581584c31f96ea6acb8f7c50；migration a3f47a5e5f30a66b9a56b4ba416a571a91a906ea9562229f4e4c52d5c8632d1d；3个 successor 待重新审核，不继承 done。
- 所有 child（3 个 executor、3 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口14已完成；待宿主发布收尾，随后审核261）”。
- 在现有“下一步按 1:1 节奏开修复窗口14……失败的 FINAL 之后必须接 RE_REVIEW。”段后追加窗口14结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核261（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w14-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-14-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
