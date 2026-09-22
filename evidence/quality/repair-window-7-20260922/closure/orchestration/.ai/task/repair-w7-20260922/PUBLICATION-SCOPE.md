# 窗口7证据发布与暂停交接范围
唯一EXECUTOR仅写 evidence/quality/repair-window-7-20260922/、handoff.md、evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json、i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json，以及 evidence/production-review-v2-lite/migrations/677e6622a2146f9f9686ee91c9d1bc3f02990c8d08547df721786877dd287325.json。
不得改Lua、术语、规则、工具、旧证据、.ai；不得stage/commit/push、创建agent、重跑queue/catalog/migration/完整门禁。

安装PACK-MANIFEST.json的452项、2317751 bytes至evidence/quality/repair-window-7-20260922/orchestration/<relative_destination>，逐项SHA核验；已有相同则保留，不同则停止。STATE必须来自manifest指定immutable checkpoint。manifest逐字复制为orchestration-pack-manifest.json；冻结字节不清洗空白。
候选catalog位于.artifacts/i18n/repair-window/window7-20260922-candidate-catalog，五文件逐字复制至对应仓库路径；window7-20260922-migration.json逐字复制至target_path。
publication/逐字复制本task的PUBLICATION-SCOPE.md、PACK-REPLAY-PROBE.json、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json；以及.artifacts/i18n/repair-window/window7-20260922-前缀的queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration-timing.json、migration-run.log、migration-run-timing.json；另复制.artifacts/i18n/continuation-20260922/中的review253-push-verification.json、review253-post-handoff-queue.log、review253-post-handoff-queue-timing.json，三件证明253实际收尾。

新增PUBLICATION.md，改写handoff.md顶部当前状态，保留必要历史并移除相互矛盾的旧当前指令：
用户于2026-09-22明确要求“这轮修复完成后暂停并撰写handoff文档”。窗口7完成后STOP；不得自动启动254，需新用户授权。此前连续授权不覆盖这次暂停后的新批次。
253已完全闭合，证据3927ca05a43daee81bb2a2fadaf77d2b3b881d0b、收尾e103379a5e809923401aa0099cfbdc9f104725ca及queue/push/远端核验均完成。
窗口7八条修复、限定边界、R0实际6OK/2ISSUE及宿主源码确认、后续复审的真实结果均按task记录写，不伪称全程无finding。四成员stage与full final分开描述。第二轮后SENIOR scope_audit对挽歌触发条件keep、对spinneret兄弟项narrow；宿主仅接受一个触发句修复，cycle3默认上限未扩大。原始ISSUE如被裁决为非阻断应如实记述，不冒充原始全OK。
译文commit 312dcd6844f80fff34911999bffab7a8f954e34f；完整门禁17/17含strict build，结果.artifacts/i18n/ci-gates/run.4d0v0980/results.json，DONE_VERIFIED和452项快照重放通过。实施/复审child共22个已归档；本publication child待宿主收获归档，不提前宣称。
一次catalog build和migration-chain已完成：catalog 0fece77f6c05306c2706b263729cc1a3b5fcdf1dc29f58bd41af380204595696、migration 677e6622a2146f9f9686ee91c9d1bc3f02990c8d08547df721786877dd287325；8 revision_changed、29820 unchanged、0 ambiguous/unmapped；8 successors queued需重新审核，不继承done。
此次证据提交、第二次queue/push及最终暂停交接收尾待宿主执行；后续实际完成将追加实测证据，不提前宣称。不要写继续254。
旧Archmage、旧回忆录pending、RW1-SIB-01/02、blocked和范围外兄弟条目保持原状态；保留.ai/consult/、recipe、15个旧source-workset。

验证字节副本、catalog/migration精确复制、Lua与译文commit相同、文档链接/UTF8/空白，可只读运行ai_state_check.py snapshot DONE。不要运行verify_pack.py（它写.ai）。报告实际产出。
