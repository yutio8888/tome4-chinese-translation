# 窗口5证据归档与交接范围

依既有SPEC出版条款和连续提交授权，本阶段唯一EXECUTOR仅可写：
- evidence/quality/repair-window-5-20260922/（保留已有IMPLEMENTATION/VALIDATION报告）
- handoff.md
- evidence/production-review-v2-lite/catalog/entries.jsonl、exclusions.jsonl、manifest.json
- i18n/quality/production-review-v2-lite/catalog-v1.schema.json、policy-v1.json
- evidence/production-review-v2-lite/migrations/198b6812cf2fc2865016eb39153f90a70f244d3984a6ca81009bde8c2e897b6a.json

不改Lua、术语、规则、工具、旧批次证据或.ai；不stage/commit/push，不创建agent，不重跑queue/catalog/migration/完整门禁。

逐字安装PACK-MANIFEST.json中的738项，共8798915 bytes，到 evidence/quality/repair-window-5-20260922/orchestration/<relative_destination>。每项先核SHA256；目的地若已存在，相同则保留，异则停止。STATE源为immutable checkpoint，不得用当前可变STATE替换。manifest逐字复制为orchestration-pack-manifest.json。冻结源码/SPEC/原始报告可能有literal行末空白，保持字节不清洗。
将.artifacts/i18n/repair-window/window5-20260922-candidate-catalog/内五文件逐字复制到对应仓库路径；将window5-20260922-migration.json逐字复制到上列migration路径。迁移已实际plan/check/apply成功，18 revision_changed、29810 unchanged、0 ambiguous/unmapped、18 queued successors，禁止重复运行。

新增publication/子目录保存以下文件的逐字副本：本PUBLICATION-SCOPE.md、PACK-REPLAY-PROBE.json、CATALOG-CHANGE-VERIFICATION.json、MIGRATION-HOST-VERIFICATION.json、TRANSLATION-COMMIT.json（在本task目录）；window5-20260922-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration.json、migration.log、migration-timing.json（完整文件名前缀均window5-20260922-，位于.artifacts/i18n/repair-window/）。

新增PUBLICATION.md并更新handoff.md当前状态，保留必要历史和既有无关文件：
- 250、251两批已完成；窗口5因高影响机制问题提前至251安全边界修复。18条=真实preflight16条（250十条、251六条）+251独立补充2条，不伪称18均来自生产repair_required。
- 译文commit f0560f5d888a9c5a84f21c1216e43eb1645437d3。只改mod-tome.lua的18个target；source/source_tag/args_order等保持，唯原授权e56b布局恢复源码1LF/2TAB。无术语库变更。
- 三轮上限后最终复审发现188段hum被译作呼吸，真实暂停WAIT_USER。用户“同意”额外一轮，SENIOR范围校准keep，仅改为嗡嗡作响。max_cycles=4是本次用户授权，不能推导以后默认四轮。
- 最新最终全量原始结果16 OK+2 ISSUE；宿主按范围裁决无accepted/deferred后completed，并非18allOK。memoir358清醒时喂水及380前往Elvala未编辑子句保留pending；Corruptor职业birth descriptor existing条目不强制映射叙事_t，保留advisory。其他历轮范围外memoir和称谓建议保留原记录；不新增修复。
- 拒收的身份/读取边界复审尝试与fresh retries均保留；不能把无效结果当审核依据。全部有效独立审查、两次scope_audit、用户暂停/授权、三次不同候选的完整门禁及生命周期记录归档。当前完整门禁run.rlohbmvk为17/17含严格构建，DONE_VERIFIED及738文件独立snapshot重放均通过。
- 新catalog c267a00eaf39f49b99266912241cfed79dfcbda440903763975ea2e4334a239d，migration 198b6812cf2fc2865016eb39153f90a70f244d3984a6ca81009bde8c2e897b6a，单次build及migration-chain已完成。18个successor已queued，后续重新审核，不继承旧revision完成态。
- 本次证据commit、第二次queue rebuild与push待宿主执行，不能提前写成已完成。完成后继续252默认80条。旧Archmage/pending/blocked及RW1-SIB-01/02不扩大。
- .ai/consult/、recipe、15个旧source-workset保留，不纳入提交或清理。

验证：738文件SHA精确相同、五catalog文件及migration精确copy、mod-tome.lua仍与译文commit一致、新写文档链接/UTF8/末尾换行/空白。可运行python3 -B tools/ai_state_check.py .ai/task/repair-w5-20260922/STATE.json --workspace-root <仓库绝对路径>/evidence/quality/repair-window-5-20260922/orchestration --target DONE，只读验证归档快照。不要运行verify_pack.py，因为它会向.ai写宿主报告。报告实际产出与检查，保留全部旧报告。
