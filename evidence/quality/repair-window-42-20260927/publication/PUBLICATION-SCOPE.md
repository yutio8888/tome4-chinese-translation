# 窗口42证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-42-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/9a9f81fd0fade576f78e109a5053b76d9cb7a36ce00c1da84fc9db7b695cea9a.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w42-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-42-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window42-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window42-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 23 revision_changed（均为 workset，无 runtime-sync）、29805 unchanged、0 ambiguous/unmapped、23 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；复制 `.artifacts/i18n/repair-window/window42-20260927-publish-chain.log`、`window42-20260927-publish-chain-timing.json`、`window42-20260927-migration.json`、`window42-20260927-migration-timing.json`，去掉 `window42-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 333、334、335、336、337、338 共 23 条确认问题（333 批 1、334 批 7、335 批 3、336 批 2、337 批 3、338 批 7），均为 tome-orcs.lua，已全部修复；无宿主补充，无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Sunwall 全库译名不一仍为待用户审阅第 37 项，本窗口不改。
   - 预检：开窗前宿主逐句预检 2 条长条目（ADJUDICATION-HOST-PRECHECK-C0：纪律报告、修复者招募海报，6 处追加修复点），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：
     - execute-01 修复 23 条 → REVIEW(0) r0a1 确认 a12d4bf519 正文“技巧射击”→本库技能名“魔术射击”；95496f3e7a 观星台/瞭望台、9ebc22deed 毒镖同族记 advisory。
     - execute-02 → RE_REVIEW(1) r1a1 无一级缺陷（同两条 advisory）→ FINAL(1) f1a2 确认 9ebc22deed 爆矢枪每次攻击只引爆一枚（源码 timed_effects/physical.lua CORROSIVE_FLECHETTE eff.nb-1）及同条“镖弹/毒镖”不一。
     - execute-03 → RE_REVIEW(2) r2a1 无一级缺陷（观星台 advisory；9e927259f8“收发无误”措辞 advisory）→ FINAL(2) f2a2 23/23 OK，cycle 2 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `0feb97fecdb3bbd0713f822f0d671bbb470b937c`；新 catalog `cd1afc43cdabae9f40521720398d0e814a5125adcc1919f763af383d05456086`；migration `9a9f81fd0fade576f78e109a5053b76d9cb7a36ce00c1da84fc9db7b695cea9a`。
   - 后续：23 个 successor 必须重新审核，不继承旧 done。待用户审阅第32–37项不变。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口42已完成、待宿主证据提交与推送，下一步审核第339批）`。
   - 第一节以“- 修复窗口已闭合至 **41**”开头的那一整行改写为：`- 修复窗口已闭合至 **42**：第 333–338 批共 23 条确认问题已修复（均为 tome-orcs.lua）；译文提交 `0feb97fecdb3bbd0713f822f0d671bbb470b937c`；migration `9a9f81fd…` 的 23 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 43 积压 0 条，从审核339重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 42（模板 `setup_window41.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w41-20260927/wd.sh`、`/tmp/w41-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开窗口 43（模板 `setup_window42.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w42-20260927/wd.sh`、`/tmp/w42-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 41 已完成”开头的那一整行）为下面一整行（逐字）：
     2. 窗口 42 已完成（REVIEW、RE_REVIEW×2、FINAL×2；FINAL(1) 按源码确认爆矢枪每次攻击只引爆一枚腐蚀性毒镖后 cycle 2 收敛；门禁 17/17）。窗口 43 积压 **0** 条（第339批起）：从审核339起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：“stack of herbs”同族四条“一束植物”→“草药”（advisory，跨条）；Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）；`95496f3e7a` 等：区域名“太阳堡垒观星台”与 lore 分类名“太阳堡垒瞭望台”（术语 existing，tome-orcs.lua:2494）不一，随待审第 37 项 Sunwall 译名一并统一；第337批 advisory `9a75f2d93d`（精神雄蜂 bores into）、`9af7773a4c`（A.P.E. 缩写）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window42.py`、`.artifacts/i18n/repair-w42-20260927/wd.sh` 与 `/tmp/w42-*.sh`；开窗 setup 后先跑 `.artifacts/i18n/repair-w42-20260927/check_siblings.py <WORKSET>` 列跨组件同键兄弟并写 RUNTIME-SYNC（窗口 35、40 都因漏列在门禁 06 失败）；每轮复审 harvest/归档后须立即跑 `publish.py` 发布 stage 记录（窗口 39 漏跑、事后补发，见 HOST-NOTE-LATE-PUBLICATION.md）。
     紧随其后以“   第338批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w42-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-42-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
