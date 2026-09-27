# 窗口46证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-46-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/5c379350bcc72d8f444532921fc9b08056103ef8885bcc14101e71417df91d7c.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w46-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-46-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window46-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window46-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 20 revision_changed（均为 workset，无 runtime-sync）、29808 unchanged、0 ambiguous/unmapped、20 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`HOST-NOTES.md`、`HOST-SUPPLEMENT-CLAIMS.json`（源在 `.artifacts/i18n/repair-w46-20260927/`）、全部 `ADJUDICATION-*.json`；复制 `.artifacts/i18n/repair-window/window46-20260927-publish-chain.log`、`window46-20260927-publish-chain-timing.json`、`window46-20260927-migration.json`、`window46-20260927-migration-timing.json`，去掉 `window46-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：来源批次 353、354、355 共 15 条确认问题（353 批 6、354 批 4、355 批 5），加宿主补充 5 条（工匠制造技能 info 同族治疗学/化学/爆炸学/铁匠/机械“X道具”→“X蒸汽工具”，与窗口 45 的“电子蒸汽工具”一致，待审第 41 项，用户可否决），合计 20 条，均为 tome-orcs.lua，已全部修复；无跨组件同键兄弟（check_siblings 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 预检：开窗前宿主对口袋时间 lore 全文逐段预检（f466031dbb：自然精灵段全角逗号、孔克雷夫宝库、沙虫女皇之心、相位之门、“双手仍空着时”），写入 SOURCE-CLAIMS 并入首轮修复。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修复 20 条 → REVIEW(0) r0a1（GPT-6 Sol）1 条确认（沉睡洞穴忏悔书“凯尔帝勒和他的背教者们”）→ execute-02 → RE_REVIEW(1) r1a1 1 条确认（收容营欢迎信“第一步”句）→ execute-03 → RE_REVIEW(2) r2a1：Weirdling Beast“异形触手”为本库既定名 refuted，conjuration wands（of conjuration 词缀）advisory → FINAL(2) f2a2（Opus 5.5）1 条确认（治疗学/爆炸学配方两行与同族对齐）→ execute-04 → RE_REVIEW(3) r3a1 1 条确认（bone armour 骨盾→骨甲）→ execute-05 → RE_REVIEW(4) r4a1“奥术法力燃烧”为游戏内伤害类型名 advisory → FINAL(4) f4a2 1 条确认（七彩龙→多彩巨龙，按 preferred 术语“多彩”）→ execute-06 → RE_REVIEW(5) r5a1 2 条 advisory（conjuration 同前；埃尔瓦拉外交官措辞，二级 cycle≥3）→ FINAL(5) f5a2 20/20 OK，cycle 5 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `11e26bd86411afc9933aef21e49d161fb485806c`；新 catalog `a579d2d431de461ef2533cb4f102033abff721c86d24d5697a5eb4761d611883`；migration `5c379350bcc72d8f444532921fc9b08056103ef8885bcc14101e71417df91d7c`。
   - 后续：20 个 successor 必须重新审核，不继承旧 done。新增待审第 42 项（Destructicus 译名）与第 43 项（multi-hued：术语 preferred“多彩”与生物名“七彩龙”系分裂）。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-27（修复窗口46已完成、待宿主证据提交与推送，下一步审核第356批（窗口46的 20 个 successor））`。
   - 第一节以“- 修复窗口已闭合至 **45**”开头的那一整行改写为：`- 修复窗口已闭合至 **46**：第 353–355 批 15 条确认问题与宿主补充 5 条已修复（均为 tome-orcs.lua）；译文提交 `11e26bd86411afc9933aef21e49d161fb485806c`；migration `5c379350…` 的 20 个 successor 须重新审核，不继承旧 revision 的 done 状态。窗口 47 积压 0 条，从审核356重新累计（另有窗口外宿主补充项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 46（模板 `setup_window45.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w45-20260927/wd.sh`、`/tmp/w45-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开窗口 47（模板 `setup_window46.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w46-20260927/wd.sh`、`/tmp/w46-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 45 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w46-20260927/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第355批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w46-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-46-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
