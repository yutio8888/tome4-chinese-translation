# 窗口18证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-18-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/4847d321cc828a85d29b12b3c05a399eee35a700288d9ade838f8b84a443f58f.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-18-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window18-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window18-20260923-migration.json逐字复制到上列目标。迁移已成功（4 revision_changed、29824 unchanged、0 ambiguous/unmapped、4 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window18-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window18-20260923- 前缀命名）。

写 evidence/quality/repair-window-18-20260923/PUBLICATION.md，说明：
- 范围：264批4条确认（“#Target# is being crushed.”由“被击碎”改为进行态“正被碾压”；队友行为菜单 Standby 由“乖乖站好”改为与日志一致的“待命”；Offhand Jab 首句补出以出其不意的徒手攻击替代通常的副手攻击，并删去一处多余换行使 LF 与原文一致；Z’quikzshl 日记改正 trivial、名字走音末句、代词与“艾德瑞尔红宝石”，并把 not ready for the rites of lichdom 改为“还没准备好接受巫妖仪式”）。
- 任务 repair-w18-20260923：execute-01（codex/gpt-5.6-sol）实施4条；REVIEW(0)/full（codex/gpt-6-sol）3 OK/1 ISSUE，确认 R0-ZQUIK-RITES-READINESS（“没有做巫妖的条件”把准备程度改成资格判断）；execute-02 仅改该分句；FINAL(1)/full（claude-opus-5-5）4 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 8f71effdeded7b84df4fa5d9625289d0d10a0b4b；新 catalog 2cd472deee7159e35cb53656b3311a9232752be19817adb5edee7e5db494b7c2；migration 4847d321cc828a85d29b12b3c05a399eee35a700288d9ade838f8b84a443f58f；4个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 所有 child（2 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口18已完成；待宿主发布收尾，随后审核265）”。
- 在审核264段（以“可复用窗口17 helper（verify.py 的 LF/TAB 对照 source；verify_migration 有两处条数硬编码）。”结尾）后追加窗口18结果（按 PUBLICATION.md 摘要，含提交、catalog、migration）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核265（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w18-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-18-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
