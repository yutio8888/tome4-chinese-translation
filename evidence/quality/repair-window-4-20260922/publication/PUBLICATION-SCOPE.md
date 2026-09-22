# 窗口4出版范围补充

依原SPEC的后续出版条款，本阶段唯一EXECUTOR仅可写：evidence/quality/repair-window-4-20260922/、handoff.md、docs/runtime-key-collisions.md（已有sidecar改动须保留）、候选目录的五个对应仓库文件，以及evidence/production-review-v2-lite/migrations/662b5a600a6702658db4397c077036c84d59a3eb32c87cb010d5508cce1c46bc.json。
不改任何Lua、术语、规则、工具、旧批次证据或.ai；不stage/commit/push，不启动agent，不重新运行queue/catalog/migration/full gates。

将PACK-MANIFEST.json的309条source逐字复制到 evidence/quality/repair-window-4-20260922/orchestration/<relative_destination>；每项先验证SHA256，目的地相同则保留，异则停止。两任务STATE来源是immutable checkpoint，严禁替换为现在的可变STATE。复制manifest为orchestration-pack-manifest.json。
将.artifacts/i18n/repair-window/window4-20260922-candidate-catalog/内五文件逐字复制到对应仓库相对路径；migration.json逐字复制到其migration_id路径。migration-chain已真实成功且已apply，18 revision_changed、29810 unchanged、0 ambiguous/unmapped、18 queued successors，禁止重做。
新增publication/子目录保存宿主PACK-REPLAY-PROBE、CATALOG-CHANGE-VERIFICATION、COMBINED-CANDIDATE-VERIFICATION、TRANSLATION-COMMIT、PUBLICATION-SCOPE及本说明逐字副本，以及window4-20260922-queue-1.log、queue-1-timing.json、catalog.log、catalog-timing.json、migration-timing.json（均在.artifacts/i18n/repair-window/；文件不存在时报告真实名称，不编造）。

新增PUBLICATION.md并更新handoff.md当前进度（保留必要历史）：窗口4主任务17条=三次真实preflight16条+宿主独立回忆录1条；额外独立runtime sibling任务修1条Cults共享键，不伪称主17清单扩展为18或均来自preflight。译文commit df8a73a3c9b54f6696cf47baf297f01dc7105ce4。完整门禁首次16/17通过，runtime碰撞诊断后修复；retry run.tb2mt5it 17/17通过含构建，两个任务DONE_VERIFIED。主最终原始结果16OK+1范围外ISSUE，宿主裁决scope无accepted/deferred后completed，并非17allOK；Cults有效REVIEW/FINAL均1OK，首次review input被宿主判无效（fixed_source_identity格式错误）已修复后fresh retry，原始材料全部保留。Cults实际公开源码SHA6cc08be3041889e6e7223c27b056f6d8db173e75108e881fb20aea64234b5cb9，upstream commit/版本未固定；catalog snapshot不是源码commit。共享key存在于官方core，所以该key不重复加入DLC overlay，不能声称全部Cults不发布。回忆录source164、198/210范围外观察保持pending/advisory，不自动修复；Archmage和旧blocked保持排除。
目录新ID4763c0b4c71f1ba7a64a5603aca78da83e689f658738d6bc31feaaa9d8f68f08；本阶段证据commit、第二次queue rebuild和push仍待宿主执行，禁止写成已完成。下一批250默认80条，须在出版闭合后开始。

验证：309文件SHA逐字一致、两个独立snapshot DONE重放（见verify_pack.py命令，工具会写.ai宿主报告，因此EXECUTOR不调用该脚本，可自行运行其中只读检查），五文件与migration精确copy、Lua仍与译文commit一致、新写文档链接/空白。原始冻结源码及SPEC可能含literal行末空格，保持字节不清洗并如实指出。报告实际输出与检查。
