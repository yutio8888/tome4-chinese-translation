# 窗口10证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-10-20260923/（保留已有 IMPLEMENTATION.md、FIX-R0.md、FIX-F1.md、FIX-R2.md、VALIDATION.json 等实施报告）
- evidence/quality/pending-user-review.md（追加，见下）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/dd5ed9cefe8b85e6c255c7cfa49431e9b8d17e4b7e8774347123b62b25dbfc81.json

不改Lua、术语、规则、工具、旧证据、.ai；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-10-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。本包同时含已取代的 STOP 任务 repair-w10-20260923 及其复审记录。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window10-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window10-20260923-migration.json逐字复制到上列目标。迁移已成功（5 revision_changed、29823 unchanged、0 ambiguous/unmapped、5 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.ai/task/repair-w10-20260923/ 下 ADJUDICATION-R0.json、ADJUDICATION-F1.json、ADJUDICATION-R2.json、ADJUDICATION-F3.json（以 w10- 前缀命名）；.artifacts/i18n/repair-window/下 window10-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json。

写 evidence/quality/repair-window-10-20260923/PUBLICATION.md，说明：
- 范围：256批5条确认（Plate of the Blackened Mind 描述、魔法大爆炸区域传送反射警告、时空术士 Galsamae 入门笔记长信、剑刃风暴构装体效果、碾压擒抱挣脱日志）。
- 首轮任务 repair-w10-20260923：REVIEW(0)/full（codex/gpt-6-sol）3 OK/2 ISSUE（长信“无所不知”增译与 nigh 缺失、构造体→构装体术语，确认修复）；FINAL(1)（claude-opus-5-5）4 OK/1 ISSUE（长信整条复核修复）；RE_REVIEW(2) 4 OK/1 ISSUE（Sher'Tul 护盾条件等，确认修复）；FINAL(3) 4 OK/1 ISSUE（“被我和”→“被我们和”一字主语错误）。max_cycles=3 用尽未收敛，按 AGENTS.md 停止条件交回用户；用户选择以 w10b 重跑，首轮以 STOP_VERIFIED 关闭（原因记录在其 STATE.last_error）。
- 重跑任务 repair-w10b-20260923：唯一EXECUTOR逐字应用 FINAL-TARGETS（与 CANDIDATE-FINAL 逐字节一致），REVIEW(0)/full（gpt-6-sol）4 OK/1 ISSUE（长信 reset and try again 措辞，宿主判 pending 交用户，不开修复轮）、FINAL(1)/full（opus-5-5）5 OK；完整门禁 17/17 含严格构建；DONE_VERIFIED。
- 译文提交 a317634cd1be2102dce66e73a51cb36890b5068f；新 catalog 0cec1688df3ca1c26258e28198f3716e5f380f00ece6024f5a30a369c83aeb5d；migration dd5ed9cefe8b85e6c255c7cfa49431e9b8d17e4b7e8774347123b62b25dbfc81；5个 successor 待重新审核，不继承 done。
- 所有 child（首轮 executor 与 reviewer、重跑 executor 与 2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

evidence/quality/pending-user-review.md 在文件末尾追加一节“修复窗口 10 待审阅”，新增第 11 项：
11. `eb0868d54c`（时空术士 Galsamae 入门笔记长信 `Warden-Master Galsamae's Orientation Notes`）
   - 源码：`lore/misc.lua:721`，`The ultimate power of time - the ability to reset and try again if you fail`。
   - 现译：“能够在你失败时不断重试”。
   - 争议理由：w10b REVIEW(0) 认为遗漏 reset（重置时间）；宿主认为该句紧接“有关时间的终极力量”，语境已含借时间重来之意，属措辞精度分歧而非机制错误。
   - 建议选项：保持 / 改为“能够在失败时重置时间、再来一次”。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-23（修复窗口10已完成；待宿主发布收尾，随后审核257）”。
- 在现有“审核256……下一步按 1:1 节奏开修复窗口10……”段后追加窗口10结果（按 PUBLICATION.md 摘要，含 STOP+重跑说明、提交、catalog、migration、pending 第11项）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核257（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w10b-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-10-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
