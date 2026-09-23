# 窗口11证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-11-20260923/（保留已有 IMPLEMENTATION.md、FIX-F1.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/5033b3e3c151150bebed931811e95f1cd91e7838e16773d0fe2e43bf4135a176.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-11-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window11-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window11-20260923-migration.json逐字复制到上列目标。迁移已成功（4 revision_changed、29824 unchanged、0 ambiguous/unmapped、4 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window11-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window11-20260923- 前缀命名）。

写 evidence/quality/repair-window-11-20260923/PUBLICATION.md，说明：
- 范围：257批4条确认（Trollmire 日记残页两处空行与 get wind of 习语、Torment 伤害阈值与判定方式、鼠巫妖头骨未鉴定名、角色面板“状态效果抗性”标题）。
- 任务 repair-w11-20260923：execute-01 实施4条；REVIEW(0)/full（codex/gpt-6-sol）3 OK/1 ISSUE（Torment 每个冷却技能分别判定，torment.lua:144–149；reviewer 回显 revision_key 有一段重复，经原生日志核实后宿主 hand-attribution，原始字节保留于 r0a1-original.raw；宿主先判 pending）；FINAL(1)/full（claude-opus-5-5）3 OK/1 ISSUE（同一机制问题），宿主按 AGENTS.md“机制以源码实际行为为准”更正为 confirmed 一级缺陷（R0 的 pending 记录已标 superseded，不列入待审阅清单），execute-02 有界修复为“每个冷却中的技能各有 %d%% 概率减少 1 回合冷却时间”；RE_REVIEW(2)（gpt-6-sol）4 OK；FINAL(3)（opus-5-5）4 OK。完整门禁17/17含严格构建（execute-01 后一次、execute-02 后最终一次），DONE_VERIFIED。
- 译文提交 6eca6f9952781a1e98d117d35fac2c7028bacb85；新 catalog 5020a313d684c44e837ce0bd2bd8a4062ad42a784b356cc802a934d6dfa1d957；migration 5033b3e3c151150bebed931811e95f1cd91e7838e16773d0fe2e43bf4135a176；4个 successor 待重新审核，不继承 done。
- 所有 child（2 个 executor、4 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口11已完成；待宿主发布收尾，随后审核258）”。
- 在现有“下一步按 1:1 节奏开修复窗口11……必须接 RE_REVIEW。”段后追加窗口11结果（按 PUBLICATION.md 摘要，含 Torment 由 pending 改判 confirmed 的说明、提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核258（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w11-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-11-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
