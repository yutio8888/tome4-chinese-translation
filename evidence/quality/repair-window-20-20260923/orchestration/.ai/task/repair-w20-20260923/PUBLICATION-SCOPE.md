# 窗口20证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-20-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/99c7ebd419a3f9ceebf2bba12de24d4561cbba3805972d941cda1f7fa83c6def.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-20-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-20-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window20-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window20-20260923-migration.json逐字复制到上列目标。迁移已成功（7 revision_changed、29821 unchanged、0 ambiguous/unmapped、7 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window20-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window20-20260923- 前缀命名）。

写 evidence/quality/repair-window-20-20260923/PUBLICATION.md，说明：
- 范围：266批7条确认（念力核心项圈外观保留“似乎”、去掉增译的“所有”；邪眼 bloodshot 改“布满血丝”；Utterly Destroyed 说明 creature 改“生物”、thrill of the death 改“击杀带来的快感”；离线模式说明“版本检查：不再检查插件是否有新版本”，并按复审把“角色备份”改为“角色仓库……上传到在线仓库来展示你的荣耀”、补“有关游戏更新的信息”、把错位的空行移回原位；时空法术类别说明改“操控时间的法术学派”；梅琳达成就改“落难少女拯救者”；蛛毒魔棒未鉴定名 wand 改“魔杖”）。
- 任务 repair-w20-20260923：execute-01（codex/gpt-5.6-sol）实施7条；REVIEW(0)/full（codex/gpt-6-sol）6 OK/1 ISSUE，确认 Characters vault 误作备份并增 te4.org；execute-02 仅改该行；FINAL(1)/full（claude-opus-5-5）6 OK/1 ISSUE，确认空行错位（LF 总数不变但空行从“游戏内新闻”后移到 CRIMSON 警告前）与漏“关于游戏更新”；execute-03 修复；RE_REVIEW(2)/full（codex/gpt-6-sol）7 OK；FINAL(3)/full（claude-opus-5-5）7 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 ffa53351b8e490c859ec029fdc655bd4c8f3bab5；新 catalog e97aaf89de5fca113d500beccb80df23b2c5731eb3f8215495e93805b6c4c76c；migration 99c7ebd419a3f9ceebf2bba12de24d4561cbba3805972d941cda1f7fa83c6def；7个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 教训：verify.py 只比 LF/TAB 计数，看不出空行挪位；多段 target 须逐行比对空行下标。
- 所有 child（3 个 executor、4 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口20已完成；待宿主发布收尾，随后审核267）”。
- 在审核266段（以“helper 从窗口19复制（verify/verify_catalog/verify_migration 的条数 4→7）。”结尾）后追加窗口20结果（按 PUBLICATION.md 摘要，含提交、catalog、migration 与空行教训）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核267（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w20-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-20-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
