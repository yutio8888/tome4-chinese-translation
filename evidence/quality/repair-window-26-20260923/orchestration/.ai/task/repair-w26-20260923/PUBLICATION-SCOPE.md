# 窗口26证据归档与交接范围

用户2026-09-23授权持续推进，无需逐批确认。本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-26-20260923/（保留已有 IMPLEMENTATION.md、VALIDATION.json、ERRATUM-BATCH272-LF.md 等）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json（若候选目录内有）
- evidence/production-review-v2-lite/migrations/6f8736fb807babfeda9ddd927ffc5958251ddd23bba538dc87f6ee40d6314302.json

不改Lua、术语、规则、工具、旧证据、.ai、evidence/quality/pending-user-review.md；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中全部文件（数量与字节以manifest为准）到evidence/quality/repair-window-26-20260923/orchestration/<relative_destination>，逐项核SHA；同字节保留，异则停止。manifest逐字复制为 evidence/quality/repair-window-26-20260923/orchestration-pack-manifest.json（窗口根目录，不是 orchestration/ 之下）。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window26-20260923-candidate-catalog/内文件按其相对路径逐字复制到仓库对应路径；window26-20260923-migration.json逐字复制到上列目标。迁移已成功（5 revision_changed、29823 unchanged、0 ambiguous/unmapped、5 queued successors），不重复运行。

publication/目录逐字复制：本task的PUBLICATION-SCOPE.md、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、ADJUDICATION-R0.json、ADJUDICATION-FINAL.json；.artifacts/i18n/repair-window/下 window26-20260923-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（去掉 window26-20260923- 前缀命名）。

写 evidence/quality/repair-window-26-20260923/PUBLICATION.md，说明：
- 范围：272批5条确认（思维形态技能系说明“灵能召唤术”改“灵能召唤物”；写给威斯曼的信 (1) 逐段重译，补轻蔑、胆识与豪侠气概、巨蚁始祖、愚蠢等原意，地名用古老森林、德斯，恢复原文 8 个换行与署名前空行；泰坦的箭袋描述补“磨得锋利无比”“几乎无法折断”“比任何箭都更像长钉”；阿塔玛森丢失的红宝石眼睛描述删多余换行、明确被毁的武器是阿塔玛森这具傀儡并补“给兽人以重创”；梅琳达任务日志补“袭击队”）。
- 任务 repair-w26-20260923：execute-01（codex/gpt-5.6-sol）实施5条，宿主逐条逐行核对行数、空行下标与行首 TAB；execute-01 的冻结 prompt 因宿主写文件多一个尾换行，与 Paseo 实际投递文本差一个 LF，宿主核实后将冻结 prompt 对齐投递文本并保留原件（见 HOST-EXECUTOR-AUDIT.json）。REVIEW(0)/full（codex/gpt-6-sol）3 OK、2 ISSUE，宿主均判 confirmed：威斯曼信中 Old Forest 应按术语库与任务/lore 用“古老森林”（窗口 SPEC 误取区域名条目“古老树林”）；阿塔玛森眼睛描述中“它”易被读作眼睛，改为明确指阿塔玛森。execute-02 定点修复这两处；FINAL(1)/full（claude-opus-5-5）5 OK，收敛。完整门禁全部通过含严格构建，DONE_VERIFIED。另附勘误 ERRATUM-BATCH272-LF.md：审核272 surface 裁决写的“LF 10→9”实测为 8→9，裁决结论不变。
- 译文提交 df937b894d02a01ff4ca0c1b2d7ccfd22918b2c4；新 catalog 2a349020c440d5766776ac1396bd949c94f99c0c97852b314543776fc9acf280；migration 6f8736fb807babfeda9ddd927ffc5958251ddd23bba538dc87f6ee40d6314302；5个 successor 待重新审核，不继承 done。本窗口无新增 pending。
- 所有 child（2 个 executor、2 个 reviewer）均已归档确认；本 publication child 待宿主归档。

更新 handoff.md 顶部：
- 第3行更新时间改为“2026-09-24（修复窗口26已完成；待宿主发布收尾，随后审核273）”。
- 在审核272段（以“范围见 `.ai/task/batch-54be748f9582a3f09434/WINDOW26-REPAIR-DECISION.json`。”结尾）后追加窗口26结果（按 PUBLICATION.md 摘要，含提交、catalog、migration 与勘误说明）。
- 下一步：本证据提交、第二次 queue rebuild、push由宿主执行，随后继续审核273（默认80条）。不要提前宣称这些后续步骤完成。
保留其余历史段落。

验证逐字副本、catalog/migration精确copy、文档链接/UTF8/空白。可只读运行 python3 -B tools/ai_state_check.py .ai/task/repair-w26-20260923/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-26-20260923/orchestration --target DONE。不要运行verify_pack.py。最后报告实际产出与验证。
