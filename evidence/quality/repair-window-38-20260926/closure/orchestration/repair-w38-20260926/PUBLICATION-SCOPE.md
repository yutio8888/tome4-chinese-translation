# 窗口38证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-38-20260926/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、如候选含有则 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/c67c525de5411f674069c31420a67d1c370a3f820cb84f90aeb755ecbec7d57b.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w38-20260926/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-38-20260926/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window38-20260926-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `window38-20260926-migration.json` 逐字复制到上述 migration 目标。已验证 24 revision_changed、29804 unchanged、0 ambiguous/unmapped、24 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`、`HOST-EXECUTOR-AUDIT-execute-01.json`、`INVALID-F2A2.json`、`INVALID-F2A3.json`；复制 `.artifacts/i18n/repair-window/window38-20260926-publish-chain.log`、`window38-20260926-publish-chain-timing.json`、`window38-20260926-migration.json`、`window38-20260926-migration-timing.json`，去掉 `window38-20260926-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 315、316、317、318、319 共 24 条确认问题已修（tome-cults.lua 2 条、tome-orcs.lua 22 条；全仓库同 source 检查无跨组件同键）。Cults 与 Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前一个只读助手逐段比对 2 条最长条目（2d9e3f67 心灵传讯《马基埃亚尔的传说》、281445cd 艾琳日记），宿主逐字核验引文 14/14 后并入修复（ADJUDICATION-HOST-PRECHECK-C0）。
   - 复审路径：
     - execute-01 修复 24 条，宿主精确 diff 核验。
     - REVIEW(0) r0a1 确认 1 条：2d9e3f67 None can say what our champion did（做了什么，非去向）。
     - execute-02 → RE_REVIEW(1) r1a1 24/24 OK → FINAL(1) f1a2 确认 2 条：21c042dd 维序者广告引语补「」（对齐同文件同类广告引语）；2d9e3f67 “出于”→“处于”。
     - execute-03 → RE_REVIEW(2) r2a1 24/24 OK → FINAL(2) f2a2、f2a3 输出截断（24 条只回 3 条与 2 条、末个 key 残缺）被契约拒收（INVALID-F2A2、INVALID-F2A3），重派 f2a4 确认 1 条：1bc7d052 涌血末行斜体引语 The marvels of technology, now at the service of true butchery!
     - execute-04 → RE_REVIEW(3) r3a1 确认 1 条：2d9e3f67 格鲁希纳克部落“力量与钢铁的蛮攻并不够强大”（原译增“精英部队”“最强大”），宿主同段并入加伯特部落同位语。
     - execute-05 → RE_REVIEW(4) r4a1：2485f3aa/354df698 tinker 术语（existing“蒸汽工具”）refuted，六条同族技能一致用“…道具”，属跨条决定，记 advisory；宿主对 2d9e3f67 全文逐句复核 26 项（22 组精确替换）确认。
     - execute-06（结果与宿主预构 target 逐字相同）→ RE_REVIEW(5) r5a1 24/24 OK → FINAL(5) f5a2 24/24 OK。max_cycles=5 用满后收敛。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `e34291e7ae890b3f4af1bc0a62b823732d018e2a`；新 catalog `d2b34cb7355c28f94293a3c5665fc46c0d61d3e06251d83b6f01dc42aef39441`；migration `c67c525de5411f674069c31420a67d1c370a3f820cb84f90aeb755ecbec7d57b`。
   - 后续：24 个 successor 必须重新审核，不继承旧 done。窗口外宿主补充项待下个窗口按 revision 核实后纳入：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖。待用户审阅第32项（Thunder Grenade）、第33项（Voltaic Bolt）不变。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-26（修复窗口38已完成、待宿主证据提交与推送，下一步审核第320批）`。
   - 第一节以“- 修复窗口已闭合至 **37**”开头的那一整行改写为：`- 修复窗口已闭合至 **38**：第 315–319 批共 24 条确认问题已修复；译文提交 `e34291e7ae890b3f4af1bc0a62b823732d018e2a`；migration `c67c525d…` 的 24 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 39 积压 0 条，从审核320重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项：只把“修复积压达 20 再开窗口 38（模板 `setup_window37.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w37-20260926/wd.sh`、`/tmp/w37-*.sh`）。”改为“修复积压达 20 再开窗口 39（模板 `setup_window38.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w38-20260926/wd.sh`、`/tmp/w38-*.sh`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 37 已完成”开头的那一整行）为：“2. 窗口 38 已完成（REVIEW、RE_REVIEW×5、FINAL×3〔cycle 2 两次输出截断拒收后重派〕；max_cycles 5 用满后收敛；17/17）。窗口 39 积压 **0** 条（第320批起）：从审核320起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window38.py`、`.artifacts/i18n/repair-w38-20260926/wd.sh` 与 `/tmp/w38-*.sh`。”。紧随其后以“   第319批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   - 第五节第 4 项：只把“（当前 31 项；”改为“（当前 33 项；”，并在该项括号内“第 31 项软蹄族／软蹄者（Soft-foot）”之后追加“；第 32 项 Thunder Grenade 闪电榴弹；第 33 项 Voltaic Bolt 闪电球”。
   第五节第 3、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w38-20260926/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-38-20260926/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
