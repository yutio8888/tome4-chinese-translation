# 窗口47b证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-47b-20260928/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/2e88ba7a55900439acf3edb9f216e2b20fd272c338f3a4307dc8ba0d0c3d0809.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w47b-20260928/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-47b-20260928/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window47b-20260928-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window47b-20260928-migration.json` 逐字复制到上述 migration 目标。已验证 56 revision_changed（均为 workset，无 runtime-sync）、29772 unchanged、0 ambiguous/unmapped、56 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w47b-20260928/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json` 与全部 `HOST-NOTE-*.md`（共 2 个）；复制 `.artifacts/i18n/repair-window/window47b-20260928-publish-chain.log`、`window47b-20260928-publish-chain-timing.json`、`window47b-20260928-migration.json`、`window47b-20260928-migration-timing.json`，去掉 `window47b-20260928-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：B 组（用户 2026-09-27 对待审清单的裁决中单条措辞与名称的部分：第 3、6、8–14、17、18、20–29、31–35、38、39、41 项）48 条，加窗口 47a 转入 8 条（“火魔婴”→“火焰小鬼”6、“物品黑暗麻木”→“物品暗影麻木”1、雕像名“莎西·凯希”1），共 56 条宿主补充，涉及 mod-tome.lua、tome-orcs.lua、tome-ashes-urhrok.lua；名称类按用户指示采用 Gemini 3.8 Flash 结论；术语库未改；无跨组件同键兄弟（check_siblings 0）。Ashes/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 56 条 → REVIEW(0) r0a1（GPT-6 Sol）唯一 ISSUE 驳回 → FINAL(0) f0a2（Opus 5.5）2 条确认（科技法师进阶说明的蒸汽工具配方与技能树名；梅塔什对话漏译与增译，见 HOST-NOTE-f0a2-scope.md）→ execute-02 → RE_REVIEW(1) r1a1 2 条确认（less than ashes；米诺陶 lore 的 eons 与 rejuvenated）、2 条驳回（Archmage 职业名“元素法师”；死亡描述模板）→ execute-03 → RE_REVIEW(2) r2a1 通过（死亡描述驳回）→ FINAL(2) f2a2 2 条确认（亡灵猎手指南署名统一；华丽抛枪后续技能多余换行）→ execute-04 → RE_REVIEW(3) r3a1 1 条确认（梅塔什光束打穿岩层露出天空）→ execute-05 → RE_REVIEW(4) r4a1 通过 → FINAL(4) f4a2 56/56 OK，cycle 4 收敛（max_cycles 5）。死亡描述 f6cc31f278 被 GPT-6 Sol 连报五次，均按模板“%s而死”（mod-tome.lua:1413、1416）与待审 #18 用户裁决驳回。r1a1 的终端快照曾以占位时间戳生成后重建，见 HOST-NOTE-r1a1-terminal-capture.md。
   - advisory：9af7773a4c 的 A.P.E. 缩写本库一贯不译；f5f092ac5d 歌词 ogre/over 双关（47a 转入）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `a10222b7e4a6650d289ed90120e8d2acb867ed53`；新 catalog `580d8c9600d40dc4a19547e3f797e8efaeb5191416177fb9bf71b293af469e65`；migration `2e88ba7a55900439acf3edb9f216e2b20fd272c338f3a4307dc8ba0d0c3d0809`。
   - 后续：56 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-28（修复窗口47b已完成、待宿主证据提交与推送，下一步审核窗口47a/47b 的 successor）`。
   - 第一节以“- 修复窗口已闭合至 **47a**”开头的那一整行改写为：`- 修复窗口已闭合至 **47b**：B 组单条措辞与名称 48 条及窗口 47a 转入 8 条（三个 Lua 文件）已修复；译文提交 `a10222b7e4a6650d289ed90120e8d2acb867ed53`；migration `2e88ba7a…` 的 56 个 successor 须重新审核，不继承旧 revision 的 done 状态；窗口 47a 的 77 个 successor 同样待审。下一步审核第357批（见第五节第 2 项）。`
   - 第五节第 1 项续行：只把其中窗口模板句的 `setup_window47a.py`、`.artifacts/i18n/repair-w47a-20260927/wd.sh`、`/tmp/w47a-*.sh` 分别改为 `setup_window47b.py`、`.artifacts/i18n/repair-w47b-20260928/wd.sh`、`/tmp/w47b-*.sh`，其余文字保留。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 47a 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w47b-20260928/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第356批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w47b-20260928/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-47b-20260928/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
