# 窗口48证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-48-20260928/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/70a471df192f0fc3db0a9e72c96ae12195ede2360d397d0b68e596f39cf30ee2.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w48-20260928/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-48-20260928/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window48-20260928-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window48-20260928-migration.json` 逐字复制到上述 migration 目标。已验证 22 revision_changed（均为 workset，无 runtime-sync）、29806 unchanged、0 ambiguous/unmapped、22 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w48-20260928/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json` 与全部 `HOST-NOTE-*.md`（共 1 个）；复制 `.artifacts/i18n/repair-window/window48-20260928-publish-chain.log`、`window48-20260928-publish-chain-timing.json`、`window48-20260928-migration.json`、`window48-20260928-migration-timing.json`，去掉 `window48-20260928-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：第357、358批遗留待修复 9 条（175effe253、196ce36308 Ashes 开场与起始任务的陨石句及控制水晶；3626a66415 莎西·凯希雕像 lore 三处限定词；5e73a63007 毁灭号“致命得离谱”；6a71689b25 水小鬼雕像 lore 代词；ae4cc0af7a 米诺陶雕像 lore；ba5e371016 艾伦尼恩回忆录；dc3200b76d 元素法师起始任务“抛入星辰之间的虚空”；d0aff018a9 夸塞魔雕像 lore），加全局改名宿主补充 13 条（water imp“小水怪”→“水小鬼”、wretchling“酸液树魔”→主游戏既有“小劣魔”，均为用户指示的 Gemini 3.8 Flash 咨询结论），共 22 条，涉及 mod-tome.lua、tome-orcs.lua、tome-ashes-urhrok.lua；术语库 terminology/creatures.tsv 新增 water imp、wretchling 两行，tools/annotate_domains.py 与静态审计测试行数随译文提交；无跨组件同键兄弟（check_siblings 0）。范围外 Archmage 8b977dd836 未纳入，仍 pending_repair。Ashes/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 22 条并加术语行 → REVIEW(0) r0a1（GPT-6 Sol）2 条确认（开场“当你逐渐恢复意识”同时关系；主要恶魔台词补 gnashing 与“那些只是幼体”）→ execute-02 → RE_REVIEW(1) r1a1 2 条确认（纳格尔摄政们已提供研究成果；饲养→繁育米诺陶）→ execute-03 因模型容量错误未回报即终止（改动正确，输出无效，见 HOST-NOTE-execute-03-capacity.md）→ fresh retry execute-04 核验并记录 → RE_REVIEW(2) r2a1 2 条确认（小劣魔雕像结句“作出了巨大贡献”；caloric energy 译“身体所需的能量”，与同文件第 97 行对应条目一致）→ execute-05 → RE_REVIEW(3) r3a1 22/22 通过 → FINAL(3) f3a2（Opus 5.5）22/22 OK，cycle 3 收敛（max_cycles 5）。
   - advisory：无。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `6d56a09f6dda8fe203eb44f9e08b23c97813ed72`；新 catalog `f1f3f7a2ef1022ced9224f77b7f3462c147878f10c9f587608d273c97560bb7d`；migration `70a471df192f0fc3db0a9e72c96ae12195ede2360d397d0b68e596f39cf30ee2`。
   - 后续：22 个 successor 必须重新审核，不继承旧 done。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下三处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-28（修复窗口48已完成、待宿主证据提交与推送，下一步审核窗口48的 successor，第359批起）`。
   - 第一节以“- 修复窗口已闭合至 **47b**”开头的那一整行改写为：`- 修复窗口已闭合至 **48**：第357、358批遗留 9 条及 water imp／wretchling 全局改名 13 条（三个 Lua 文件，术语库新增两行）已修复；译文提交 `6d56a09f6dda8fe203eb44f9e08b23c97813ed72`；migration `70a471df…` 的 22 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步审核第359批（见第五节第 1 项）。`
   - 第五节第 1 项（以“1. 继续审核第 **359** 批”开头）保持原样，不改。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 47b 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w48-20260928/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第358批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w48-20260928/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-48-20260928/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
