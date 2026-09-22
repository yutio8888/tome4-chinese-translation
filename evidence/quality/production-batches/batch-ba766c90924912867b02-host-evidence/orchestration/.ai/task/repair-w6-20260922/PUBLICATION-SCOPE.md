# 窗口6证据归档与交接范围

既有SPEC和连续提交授权下，本阶段唯一EXECUTOR仅写：
- evidence/quality/repair-window-6-20260922/（保留已有实施报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json
- evidence/production-review-v2-lite/migrations/92da0238e3a17f7b5d3b4e46156ef0b9d5bacfd653bb2e00618d6f0ede25a83d.json

不改Lua、术语、规则、工具、旧证据、.ai；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json中97项，共765623 bytes到evidence/quality/repair-window-6-20260922/orchestration/<relative_destination>。逐项核SHA；存在同字节则保留，异则停止。STATE来自immutable checkpoint，不用可变STATE替换。manifest逐字复制为orchestration-pack-manifest.json。冻结证据中的literal空白保持原样。

将.artifacts/i18n/repair-window/window6-20260922-candidate-catalog/内五文件逐字复制到对应仓库路径；window6-20260922-migration.json逐字复制到上列目标。迁移已实际成功，2 revision_changed、29826 unchanged、0 ambiguous/unmapped、2 queued successors，不重复运行。

publication/目录逐字复制以下附件：
本task的PUBLICATION-SCOPE.md、PACK-REPLAY-PROBE.json、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json、HOST-AUDIT-COUNT-CORRECTION.json。
.artifacts/i18n/repair-window/下window6-20260922-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json（文件名前缀均window6-20260922-）。
.artifacts/i18n/continuation-20260922/review252-push-verification.json（证明252收尾早已推送，不重做）。

新增PUBLICATION.md并更新handoff.md当前状态，保留必要历史：
- 252批78done/2repair的收尾提交805b67263c3359441a4e6e12f3ebd0d2bdc5a0da、queue同步及push已于13:27核验完成；交接原先待执行描述改为已完成。
- 窗口6因252确认newline问题提前修复，范围恰两条真实preflight：日记仅恢复省略号前后两空行，全部文字不变；古战场成就补回主动惊扰和后果关系。source/tag/args_order/printf/markup/TAB未变，无术语库改动。
- 译文提交38e666aaae9e5738819e3b6525398b9bfc9872eb；首轮full REVIEW及最终full FINAL_REVIEW原始结果均2OK、0ISSUE。没有追加修复轮或senior升级，默认max_cycles3未扩展。
- 完整门禁run.ko6u_j8h为17/17，严格构建及DONE_VERIFIED通过；97文件独立快照重放通过。3个实施/复审child全部归档；本出版child待宿主收获归档，不提前宣称。
- HOST-AUDIT-COUNT-CORRECTION只更正审计汇总数字12为真实11个调用，已逐项检查全部实际调用；不改历史快照，不改变范围裁决。
- 新catalog 6f08ccf5394d2f0431a066c1315ba5abcdeaed1928e4781a0b1cb65e37e68405；migration 92da0238e3a17f7b5d3b4e46156ef0b9d5bacfd653bb2e00618d6f0ede25a83d。一次build和migration-chain已完成；2个successor待重新审核，不继承done。
- 本次证据提交、第二次queue rebuild、push待宿主执行；完成后继续253默认80条，开启新修复窗口。不要提前宣称这些后续步骤完成。
- 旧Archmage、旧回忆录pending、RW1-SIB-01/02、blocked及252范围外格式pending不扩大、不清零。保留.ai/consult/、recipe、15个旧source-workset。

验证逐字副本、catalog/migration精确copy、Lua与译文commit相同、文档链接/UTF8/空白。可只读运行python3 -B tools/ai_state_check.py .ai/task/repair-w6-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-6-20260922/orchestration --target DONE。不要运行verify_pack.py，它向.ai写宿主报告。最后报告实际产出与验证。
