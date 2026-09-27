# 窗口39证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-39-20260926/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/734a72ac2bf19c1561b029234f3214bab995d355f497e3cd6467cd5742a3b218.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w39-20260926/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-39-20260926/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window39-20260926-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window39-20260926-migration.json` 逐字复制到上述 migration 目标。已验证 42 revision_changed（27 workset + 15 terminology-sync）、29786 unchanged、0 ambiguous/unmapped、42 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`RUNTIME-SYNC.json`、`HOST-NOTE-LATE-PUBLICATION.md`、全部 `ADJUDICATION-*.json`、`INVALID-R6A1.json`、`INVALID-F6A3.json`；复制 `.artifacts/i18n/repair-window/window39-20260926-publish-chain.log`、`window39-20260926-publish-chain-timing.json`、`window39-20260926-migration.json`、`window39-20260926-migration-timing.json`，去掉 `window39-20260926-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 320、321、322、323 共 25 条确认问题加 2 条宿主补充（HOST-SUPPLEMENT-CLAIMS），合计 27 条 workset 已修（均为 tome-orcs.lua）。另按用户 2026-09-26 裁决把 steamsaw 在 `terminology/items.tsv` 升为 preferred「蒸汽链锯」，并将 tome-orcs.lua 其余 15 条「蒸汽锯」经 terminology-sync（RUNTIME-SYNC.json）统一。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前宿主逐句预检 7 条长条目（ADJUDICATION-HOST-PRECHECK-C0），并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：
     - execute-01 修复 27 条 → REVIEW(0) r0a1 确认 4 条（38df4d785d 武器全称“裂天者 毁灭号”、3f615510ad 采石场笔记、4a4f53d70c 仁慈结局、4cad070d1e 游戏志愿者局请愿）。
     - execute-02 → RE_REVIEW(1) 确认 2 条（431cacf5c7 地热公告副标题、4cad070d1e 背书句）→ execute-03 → RE_REVIEW(2) 确认 43d64e16d1 五彩爆炸 → execute-04 → RE_REVIEW(3) 确认 3fbaffc6c4 沃瑞钽、431cacf5c7 蒸汽采石场 → execute-05 → RE_REVIEW(4) 确认 3f615510ad、431cacf5c7 → execute-06 → RE_REVIEW(5) 收敛 → FINAL(5) f5a2 确认 393ceabce5（“我同情他”）、3bb826649c（创造之魔法、正统主宰）。
     - 用户授权 max_cycles 5→6：execute-07 → RE_REVIEW(6)（r6a1 非紧凑 JSON 拒收，r6a2 收敛）→ FINAL(6)（f6a3 截断拒收，f6a4 报 43cbe69c78 steamsaw 译名不一致）。
     - 用户裁决统一 steamsaw 并授权 6→8：execute-08（术语行 + 43cbe69c78 + 15 条 sync）→ RE_REVIEW(7) 确认 43d64e16d1 genocide→种族灭绝（驳回 tinker 术语、手炮沃瑞钽两条旧质疑）→ execute-09 → RE_REVIEW(8) 收敛 → FINAL(8) f8a2 确认 4a4f53d70c “wonder aloud”（另并入麦芽酒、数千年来）。
     - 用户授权 8→11：execute-10 → RE_REVIEW(9) 收敛 → FINAL(9) f9a2 27/27 OK。
     - advisory 未改：38e3195b27“全军戒备”、4cad070d1e“科幻”、上一名目标／瞄准画面措辞。
   - 记录：各轮 stage 记录未在复审后即时发布，FINAL 通过后宿主一次性补发 14 条（校验与理由见 HOST-NOTE-LATE-PUBLICATION.md）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `e19736293f1f9854175520be0f6d2dd04c5504d2`；新 catalog `7158f4b0958a74fb8acc01f732dc0f97a4ac6fad159f6cf1051687db04cc12f0`；migration `734a72ac2bf19c1561b029234f3214bab995d355f497e3cd6467cd5742a3b218`。
   - 后续：42 个 successor 必须重新审核，不继承旧 done。窗口外遗留：`4e560f2e5a`（emporium 公告仍作“蒸汽矿场”，应为“蒸汽采石场”）。待用户审阅第32–34项（Thunder Grenade、Voltaic Bolt、Supercharge Bullets）不变。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口39已完成、待宿主证据提交与推送，下一步审核第324批）`。
   - 第一节以“- 修复窗口已闭合至 **38**”开头的那一整行改写为：`- 修复窗口已闭合至 **39**：第 320–323 批共 25 条确认问题及 2 条宿主补充已修复，steamsaw 按用户裁决统一为“蒸汽链锯”（另 15 条同步）；译文提交 `e19736293f1f9854175520be0f6d2dd04c5504d2`；migration `734a72ac…` 的 42 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 40 积压 0 条，从审核324重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项：只把“修复积压达 20 再开窗口 39（模板 `setup_window38.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w38-20260926/wd.sh`、`/tmp/w38-*.sh`）。”改为“修复积压达 20 再开窗口 40（模板 `setup_window39.py`＋`SPEC-TEMPLATE.md`、`.artifacts/i18n/repair-w39-20260926/wd.sh`、`/tmp/w39-*.sh`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 38 已完成”开头的那一整行）为下面一整行（逐字）：
     2. 窗口 39 已完成（REVIEW、RE_REVIEW×9、FINAL×4〔f6a3 输出截断拒收；r6a1 非紧凑 JSON 拒收〕；用户三次追加预算 max_cycles 5→6→8→11，cycle 9 收敛；17/17）。窗口 40 积压 **0** 条（第324批起）：从审核324起累计；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。窗口外宿主补充项待下个窗口按 revision 核实后纳入：`4e560f2e5a`（emporium 公告“蒸汽矿场”→“蒸汽采石场”，窗口39同族修复后仅剩此处）；Temporal Feast 技能名“时间盛宴”与效果名“时空盛宴”不一致（统一前双向查冲突）；`f6030742`（导师文物 Sher'Tul“夏图尔”→“夏·图尔”，窗口36 SPEC 误写）；tome-cults.lua 第2340行 lore 标题“熵反馈”与第829行“熵反冲”按“熵能反冲”对齐；`a9c22a10`（禁忌之书：《到来之日》描述把 misery 译成“困难”）；`a5a712dc`（技能名 Writhing One 现译“蜿蜒”，职业术语为“蜿蜒怪人”）。宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续批次覆盖；修复前全仓库 grep 同一 source（门禁 06 跨组件同键）；门禁与收口脚本须 `export TOME_PASEO_WORKSPACE=wks_420314270844170b`；窗口 SPEC 专名表写入前逐条在本库查证；超长 lore 条目（数千字）开窗前须全文逐句预检，否则每轮复审都会新挖出漏译；窗口模板为 `setup_window39.py`、`.artifacts/i18n/repair-w39-20260926/wd.sh` 与 `/tmp/w39-*.sh`；每轮复审 harvest/归档后须立即跑 `publish.py` 发布 stage 记录（窗口 39 漏跑、事后补发，见 HOST-NOTE-LATE-PUBLICATION.md）。
     紧随其后以“   第323批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   - 第五节第 4 项：只把“（当前 33 项；”改为“（当前 34 项；”，并在该项括号内“第 33 项 Voltaic Bolt 闪电球”之后追加“；第 34 项 Supercharge Bullets 超速子弹”。
   第五节第 3、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w39-20260926/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-39-20260926/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
