# 窗口37证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-37-20260926/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、如候选含有则 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/0d087c7cad2d48953faf2b826bb30182a8a925a8acc5319159caeab2975d551b.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w37-20260926/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-37-20260926/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window37-20260926-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `window37-20260926-migration.json` 逐字复制到上述 migration 目标。已验证 25 revision_changed、29803 unchanged、0 ambiguous/unmapped、25 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`、`HOST-EXECUTOR-AUDIT-execute-01.json`、`INVALID-F1A2.json`；复制 `.artifacts/i18n/repair-window/window37-20260926-publish-chain.log`、`window37-20260926-publish-chain-timing.json`、`window37-20260926-migration.json`、`window37-20260926-migration-timing.json`，去掉 `window37-20260926-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 310、311、312、313、314 共 25 条确认问题已修（tome-cults.lua 6 条、tome-orcs.lua 19 条；全仓库同 source 检查无跨组件同键）。Cults 与 Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前两个只读助手逐段比对 4 条最长条目（fbe22d02、0b55d129、1094f94c、0b59fe6a），宿主逐字核验引文 44/44 后并入修复（ADJUDICATION-HOST-PRECHECK-C0）；其中 1094f94c 的 [b] 强调当时判为保留，后在 FINAL(1) 被推翻。
   - 复审路径：
     - execute-01 修复 25 条，宿主精确 diff 核验。
     - REVIEW(0) r0a1 确认 3 条：克林布尔手记卡巴萨进帐篷后才死去；静电震击“造成伤害”才触发（callbackOnHit）；时间盛宴“每次对目标施加衰亡效果时”（衰亡为被动施加）。“软蹄族”译名记 advisory 并登记待用户审阅第31项。
     - execute-02 → RE_REVIEW(1) r1a1 无一级确认：烟雾覆盖（cancel_damage_chance）与 Cunning=灵巧 refuted，软蹄与拘留营末信 “No.” 记 advisory。
     - FINAL(1) f1a2 输出截断（25 条只回 3 条）被契约拒收（INVALID-F1A2），重派 f1a3 确认 1 条：1094f94c 新增的两对 [b] 与源 markup 不一致。
     - execute-03 → RE_REVIEW(2) r2a1 确认 1 条：Kruk Pride 按术语库对齐“克鲁克部落”（条目内一处）。
     - execute-04 → RE_REVIEW(3) r3a1 25/25 OK → FINAL(3) f3a2 25/25 OK。
   - 门禁：首轮 17 项中门禁 11 因宿主追加待审阅第31项时在 pending-user-review.md 末尾多留一空行而失败（结果保留为 prior gate run），去掉空行后重跑 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `4061b447db0e5320a86d4d50ee7428b6f3451f26`；新 catalog `00d4950120d06e517727b73e5cd17ce47185a5765a9956a2dfc891cb10baf235`；migration `0d087c7cad2d48953faf2b826bb30182a8a925a8acc5319159caeab2975d551b`。
   - 后续：25 个 successor 必须重新审核，不继承旧 done。窗口外宿主补充项留给下一窗口：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致；f6030742 导师文物 Sher'Tul“夏图尔”→“夏·图尔”；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10` misery→“困难”；`a5a712dc` Writhing One 技能名。待用户审阅新增第31项（软蹄族／软蹄者）。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-26（修复窗口37已完成、待宿主证据提交与推送，下一步审核第315批）`。
   - 第一节以“- 修复窗口已闭合至 **36**”开头的那一整行改写为：`- 修复窗口已闭合至 **37**：第 310–314 批共 25 条确认问题已修复；译文提交 `4061b447db0e5320a86d4d50ee7428b6f3451f26`；migration `0d087c7c…` 的 25 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 38 积压 0 条，从审核315重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项：只把“修复积压达 20 再开窗口 37（模板 `setup_window36.py`、`.artifacts/i18n/repair-w36-20260926/wd.sh`、`/tmp/w36-*.sh`）。”改为“修复积压达 20 再开窗口 38（模板 `setup_window37.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w37-20260926/wd.sh`、`/tmp/w37-*.sh`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 36 已完成”开头的那一整行）为：“2. 窗口 37 已完成（REVIEW、RE_REVIEW×3、FINAL×2〔cycle 1 首次尝试输出截断拒收后重派〕；17/17）。窗口 38 积压 **0** 条（第315批起）：从审核315起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；Codex executor 会话压缩时按窗口27先例宿主 diff 核验；窗口模板为 `setup_window37.py`、`.artifacts/i18n/repair-w37-20260926/wd.sh` 与 `/tmp/w37-*.sh`。”。紧随其后以“   第314批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   - 第五节第 4 项：只把“（当前 30 项；”改为“（当前 31 项；”，并在该项括号内“第 30 项 numbed→麻痹（Numbing 族）”之后追加“；第 31 项软蹄族／软蹄者（Soft-foot）”。
   第五节第 3、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w37-20260926/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-37-20260926/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
