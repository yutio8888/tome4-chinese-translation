# 窗口16证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-16-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/456baa4ae824b48ffdd8c7ec72c1c93055e8fb4c51077e79eab0852d8c2747a0.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-16-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window16-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window16-20260923-migration.json逐字复制到上列目标。迁移已成功（7 revision_changed、29821 unchanged、0 ambiguous/unmapped、7 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window16-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window16-20260923- 前缀命名）。

写 evidence/quality/repair-window-16-20260923/PUBLICATION.md，说明：
- 范围：262批7条确认（50级祝贺段间空行与“勇敢地”；星辰契约 bond=羁绊、光辉引力拉向被击中目标、\t\t 缩进恢复；不死猎人指南六处增译/夸大/因果/弱化/巫妖段反义修正，并把多拆出的段落并回，LF 86→72 与原文一致；矮人送药“加了点好料，明早可有你受的”；成就“以自身为祭品关闭虚空传送门”；牺牲死讯“牺牲了%s，将维网带给众生”；强化弹药 Venomous“自然伤害”）。
- 任务 repair-w16-20260923：execute-01（codex/gpt-5.6-sol）实施7条；宿主 verify 暴露 lore 段落拆分，execute-02 只合并段落；REVIEW(0)/full（codex/gpt-6-sol）6 OK/1 ISSUE（Eyal=“埃亚尔大陆”，advisory，pending #16）；FINAL(1)/full（claude-opus-5-5）6 OK/1 ISSUE（署名“不死猎人”歧义；宿主初判 advisory，但 DONE 检查要求最新 FINAL 无 ISSUE，改判二级并有界修复）；execute-03 只改署名为“一名不死生物猎人的指南”；RE_REVIEW(2)（gpt-6-sol）6 OK/1 ISSUE（同一 Eyal 观察，advisory）；FINAL(3)/full（claude-opus-5-5）7 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 3a21f17035b51c61f592858e2b5ca7a6e9c51d6d；新 catalog 9b4f2e06ce73c07cc0ca9810db96caba529a5f15b175558803b21f1313fb2b4e；migration 456baa4ae824b48ffdd8c7ec72c1c93055e8fb4c51077e79eab0852d8c2747a0；7个 successor 待重新审核，不继承 done。
- 待用户审阅新增第16项（Eyal 全库译法）、第17项（lore 标题“不死猎人指南”两处），由宿主在证据提交中写入 pending-user-review.md。
- 所有 child（3 个 executor、4 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口16已完成；待宿主发布收尾，随后审核263）”。
- 在审核262段（以“可复用窗口15 helper（verify_migration 有两处条数硬编码），失败的 FINAL 之后必须接 RE_REVIEW。”结尾）后追加窗口16结果（按 PUBLICATION.md 摘要，含提交、catalog、migration、pending #16/#17）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核263（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w16-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-16-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
