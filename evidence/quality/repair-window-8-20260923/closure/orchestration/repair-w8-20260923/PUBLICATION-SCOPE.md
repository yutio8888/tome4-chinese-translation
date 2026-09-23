# 窗口8证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-8-20260923/（保留已有 IMPLEMENTATION.md、FIX-R0.md、VALIDATION.json 等实施报告）
- evidence/quality/pending-user-review.md（新建，见下）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/518ce6ed86c6d746184ff38b10a45cd9755ff56c2c57a0af650d7aa03252552f.json

不改Lua、术语、规则、工具、旧证据、.ai；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中109项、共999605 bytes到evidence/quality/repair-window-8-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。STATE来自immutable checkpoint。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window8-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window8-20260923-migration.json逐字复制到上列目标。迁移已成功（6 revision_changed、29822 unchanged、0 ambiguous/unmapped、6 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window8-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json。

新建 evidence/quality/pending-user-review.md：标题“待用户集中审阅的争议条目”，说明来源为用户2026-09-23指示（有争议条目列入pending，不修、不阻塞），列三条（均来自窗口8 ADJUDICATION-R0.json，含revision前10位、英文要点、现译、争议双方理由、建议选项）：
1. e92433bcba unlock-yeek：cunning 现译“灵巧”（术语库 Cunning=灵巧 为 stat name、status=existing）；三个模型认为叙事语境应为“机敏/狡黠”。选项：保持“灵巧” / 叙事语境改“机敏”。
2. e951739433 毒素风暴：Each possible effect is equally likely 现译“中毒几率在可能的毒素效果中平分”；源码 damage_types.lua 先等概率抽效果再判能否中毒；宿主曾判等价，reviewer 认为应写“各可能效果出现几率相同”。选项：保持 / 改为“各种可能的效果出现几率相同”。
3. e988482539 龙族传说：“嘲笑我把龙作为单独列出的智慧种族”含原文无的第一人称；该系列为 Loremaster Greynot 第一人称著作。选项：保持 / 改为“嘲笑将龙归为智慧种族的想法”。
另列254批宿主补充观察 e923d2b8d0（The target is using talents without consuming resources → “不再消耗能量”，resources 被窄化），以及254批 advisory：ALL_DREAMS 以外无；rogues do it from behind 标题双关、SPELLSHOCKED 省略 temporarily。

更新 handoff.md 顶部“当前授权与实测状态”：
- 用户2026-09-23指示：先做工具维护，然后持续推进审核，无需手动确认；争议条目列 pending 集中审阅，见 evidence/quality/pending-user-review.md。
- 工具维护已提交 b626eaf1c30ed389dff0b0a633e393225ea46843：原生 parser 支持 Codex 0.156.0 / Claude Code 2.1.280（含 cost-state 尾记录），10 份真实会话验证；原“工具版本偏差”段改为已解决并指向 evidence/quality/native-parser-versions-20260923/summary.md。
- 核实结论：活动批次（batch start 到 finalize）期间不能插入任何提交（production_review_v2_lite_batch.py:1084 base commit drift、:1909 finalize parent 检查）；修复窗口中 preflight 之后插入提交会使 preflight 失效需重跑；提交后都需 queue rebuild。工具维护只放在批次/窗口之间。
- 修复窗口8已完成：译文提交 9b71efd8714678d10419f9522a93a25c92f3e841；6条目标（无尽狩猎描述、ALL_DREAMS、yeek换行、Thalore诗句含紫杉与鸫鸟猫头鹰行、麻痹毒素伤害方向、龙族传说四处）；REVIEW/full（codex/gpt-6-sol）2 OK/4 ISSUE，其中诗句确认追加一轮有界修复，其余3条转 pending；FINAL_REVIEW/full（claude/claude-opus-5-5）6 OK/0 ISSUE；完整门禁 run.2f4mryxp 17/17含严格构建；DONE_VERIFIED；4个实施/复审child均已归档，本发布child待宿主归档。
- 新catalog 8580c7207ae19005bb206138eabe0daf3fb00a7eb0513c113b64c922adbc5cf2；migration 518ce6ed86c6d746184ff38b10a45cd9755ff56c2c57a0af650d7aa03252552f；6个successor待重新审核，不继承done。
- 下一步：本证据提交、第二次queue rebuild、push由宿主执行，随后继续审核255（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、Lua与译文commit相同、文档链接/UTF8/空白。可只读运行python3 -B tools/ai_state_check.py .ai/task/repair-w8-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-8-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
