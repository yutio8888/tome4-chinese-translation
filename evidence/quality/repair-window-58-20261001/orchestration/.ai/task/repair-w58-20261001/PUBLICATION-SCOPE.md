# 窗口58证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-58-20261001/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/2f023eaf7da8e87222d2d242509b8b9ef2d040b0a77226c598dff8ae6265894d.json`。不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w58-20261001/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-58-20261001/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window58-20261001-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window58-20261001-migration.json` 逐字复制到上述 migration 目标。已验证 3 revision_changed（均为 workset 条目）、29825 unchanged、0 ambiguous/unmapped、3 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json` 与 `INVALID-F1A2.json`；从 `.artifacts/i18n/repair-w58-20261001/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`、`HOST-EXACT-DIFF.json` 与 `HOST-EXACT-DIFF-POST-FIX1.json`；复制 `.artifacts/i18n/repair-window/window58-20261001-publish-chain.log`、`window58-20261001-publish-chain-timing.json`、`window58-20261001-migration.json`、`window58-20261001-migration-timing.json`，去掉 `window58-20261001-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：窗口57 的 87 个 successor 经第373批（`batch-eb93936e38c73186d222`）与第374批（`batch-2e8beab0b2f9b05c4c94`）审核后确认 3 条，审核队列耗尽、积压 3 条；用户 2026-10-01 指示“开小窗口修这 3 条”。主游戏 1（`2822ed0142` age-allure 副歌“嘿，我，现为守卫”→“嘿，你”4 处）、Cults 1（`e2c9218ea9` fay-willows：骷髅转而去夺取城门、步步逼近的亡灵大军、排成射击队列，及 FINAL 确认的两处 lockstep“步调一致”）、Orcs 1（`cc6d1a5034` pocket-time：练到足以精通其中几项、与吸血鬼领主正面交锋、含糊不清地咒骂了一通不公平）。主游戏按 manifest 固定 commit 624a673 核验；DLC 来源仓库与 commit 未固定。不改术语库；无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 修改 3 条 → REVIEW(0) r0a1（GPT-6.1 Sol）3 ISSUE：pocket-time“秒杀”按第374批裁决驳回，age-allure 歌词意译与 fay-willows lockstep 记 advisory → FINAL(0) f0a2（Opus 5.5）1 确认（fay-willows 两处 lockstep，由 advisory 升为 confirmed）→ execute-02 → RE_REVIEW(1) r1a1 1 advisory（age-allure 食人魔化歌其余意译句，carry_forward）→ FINAL(1) f1a2 在 /workspace/tome4-dlcs 下 grep ashes-urhrok，越出输入指定源码位置，拒收（INVALID-F1A2.json，不计轮次）→ fresh retry f1a3 3/3 OK，cycle 1 收敛（max_cycles 5）。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：译文提交 `54c307a7300b08c917b16d6f4ff0001c19e70b9d`；新 catalog `34b6eb1b93d977a0919cb2f67967632f079c88904afd5992e602b9d5587e9ecf`；migration `2f023eaf7da8e87222d2d242509b8b9ef2d040b0a77226c598dff8ae6265894d`。
   - 后续：3 个 successor 必须重新审核（第375批），不继承旧 done。窗口 59 积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下五处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-10-01（修复窗口58已完成、待宿主证据提交与推送；下一步审核窗口58的 3 个 successor，第375批）`。
   - 第一节以“- 修复窗口已闭合至 **57**”开头的条目（单行）整体替换为一行：`- 修复窗口已闭合至 **58**：第373、374批确认的 3 条（age-allure 副歌人称、fay-willows 夺取城门／亡灵大军／射击队列／步调一致、pocket-time 两段）已修复；译文提交 `54c307a7`；migration `2f023eaf…` 的 3 个 successor（主游戏 1、Cults 1、Orcs 1）须重新审核，不继承旧 revision 的 done 状态。`
   - 第一节以“- 2026-09-30：用户恢复工作”开头的那一行之后插入一行：`- 2026-10-01：审核队列耗尽、积压 3 条，用户选择“开小窗口修这 3 条”，开窗口58。`
   - 第三节第 1 项第一行（以“1. 继续审核第 **375** 批”开头）整行改为：`1. 继续审核第 **375** 批：窗口58的 3 个 successor（主游戏 1、Cults 1、Orcs 1，混合来源批）；之后审核队列再次耗尽，积压按窗口59重新计数。`；该项其余续行保留。
   - 第三节第 2 项：从以“2. 窗口 57 已完成”开头的行起，到以“   窗口 58 积压 **3** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w58-20261001/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第374批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第三节第 3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w58-20261001/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-58-20261001/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
