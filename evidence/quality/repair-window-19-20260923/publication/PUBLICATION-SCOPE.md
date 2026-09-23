# 窗口19证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-19-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json 等实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/e5935d7e04f86d7d3a09d9a9e6d2afcc69c0f5e3a8c8b1ace3fac0e7a1649fec.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-19-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-19-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window19-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window19-20260923-migration.json逐字复制到上列目标。迁移已成功（4 revision_changed、29824 unchanged、0 ambiguous/unmapped、4 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window19-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window19-20260923- 前缀命名）。

写 evidence/quality/repair-window-19-20260923/PUBLICATION.md，说明：
- 范围：265批4条确认（念动弓说明补“每回合”、attack 译为“命中”并与同族一致、恢复行首 TAB；Burrow 说明第三行改回 TAB 分隔并补“土质墙壁”；Nightshade 陷阱补“中毒”，4 回合同时覆盖震慑与中毒；野蛮种族记载——mod-tome.lua 中 section mod-tome/load.lua 下因后写覆盖而实际生效的那一行——改正首句、言语能力、近几百年、烈火纪末期、恶魔酸液/黑暗之云，“supported by”改为研究支持该理论，并按 FINAL(1) 修正俗称、召唤主语、“被证明是不可能的”与 extremely slender 四处）。
- 任务 repair-w19-20260923：execute-01（codex/gpt-5.6-sol）实施4条；REVIEW(0)/full（codex/gpt-6-sol）2 OK/2 ISSUE 均确认；execute-02 修复；FINAL(1)/full（claude-opus-5-5）野蛮种族记载 1 ISSUE，确认4处子串；execute-03 修复；RE_REVIEW(2)/full（codex/gpt-6-sol）4 OK（该 reviewer 经 Paseo 终端绕过沙箱只读授权文件，宿主逐条审计并关闭终端）；FINAL(3) 第1次 f3a1 结论前带英文导语判 output_valid=false、不入账，第2次 f3a2 4 OK，收敛。完整门禁17/17含严格构建，DONE_VERIFIED。
- 译文提交 e602df35477fe2a6f2ffa9fd66029b51e83186a7；新 catalog c5085a75a7796f11c91d64f39f454ac2f10dea491b28565222fdea5883057d35；migration e5935d7e04f86d7d3a09d9a9e6d2afcc69c0f5e3a8c8b1ace3fac0e7a1649fec；4个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 范围外遗留：同 source 的 lore/misc 段那一行（运行时被覆盖、不生效）仍保留旧句，未在本窗口修改，留待后续审核。
- 所有 child（3 个 executor、4 个 reviewer，含无效的 f3a1）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口19已完成；待宿主发布收尾，随后审核266）”。
- 在审核265段（以“PUBLICATION-SCOPE 要写明 pack manifest 副本放在窗口根目录。”结尾）后追加窗口19结果（按 PUBLICATION.md 摘要，含提交、catalog、migration 和范围外遗留）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核266（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w19-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-19-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
