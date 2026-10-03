# 窗口64证据发布范围

唯一 publication EXECUTOR 只写以下内容：

- `evidence/quality/repair-window-64-20261003/`；
- `handoff.md`；
- 候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件；
- 候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`；
- `evidence/production-review-v2-lite/migrations/629e3b1e9540e64f5cc19bfa4f7aca45551eaf750c7ca33fa194b90da397229a.json`。

除此之外，不改 Lua、术语、规则、工具、测试、其他 evidence、`docs/`、`.ai/task`、`.ai/reviews`、`pending-user-review.md`。不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。`docs/README.md` 上有他人未提交改动，不得触碰。

1. 按 `.ai/task/repair-w64-20261003/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-64-20261003/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。再将 manifest 逐字复制到窗口根目录，命名为 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window64-20261003-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window64-20261003-migration.json` 逐字复制到上述 migration 目标。该 migration 已验证，无须重跑：revision_changed 26、unchanged 29802、queued_successors 26、ambiguous 0、unmapped 0。
3. 在本窗口 `publication/` 下逐字复制以下文件：
   - task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、`SCOPE.json`、`SOURCE-CLAIMS.json`、`NEW-TARGETS.json`、`HOST-NOTE-r0a1-archive-order.md` 与全部 `ADJUDICATION-*.json`；
   - `.artifacts/i18n/repair-w64-20261003/` 的 `HOST-SUPPLEMENT-CLAIMS.json` 与 `HOST-EXACT-DIFF.json`；
   - `.artifacts/i18n/repair-window/` 的 `window64-20261003-publish-chain.log`、`window64-20261003-publish-chain-timing.json`、`window64-20261003-migration.json`、`window64-20261003-migration-timing.json`，复制时去掉 `window64-20261003-` 前缀作为文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：26 条译文（mod-tome.lua 25、engine.lua 1），无术语改动。
     - 2026-10-03 重新复审轮第384–391批宿主确认 25 条（各批 `HOST-FINAL-DECISIONS.json`）：换行不变量 9 条（科斯汀望远镜、扭曲的波法斯特、战斗属性教程、粘胶方块、升级教程、高等人类开场、属性教程 stats7.1、符文：粉碎痛苦、多元水晶球）；忠实性、机制与术语 16 条（盾战士简介、内购欢迎词、巫妖、调试升级对话框、腐蚀蠕虫、冰冷杀戮、暗夜流光、破损的阿塔玛森、影之护甲、永恒精灵加载提示、占位技能 fungus、疯狂诅咒、暗影射击、埃亚尔的呼吸、生死珍珠、无尽追踪）。
     - 宿主补充 1 条：第390批裁决附记的骤然生长（Sudden Growth）“孢子”→“真菌”。
     - 新译文由宿主按各条“修复：”与整句对照写定（`publication/NEW-TARGETS.json`），EXECUTOR 逐字替换；宿主核验 26 条 after 与 new_target 逐字相等（`publication/HOST-EXACT-DIFF.json`）。
     - 主游戏与引擎按 manifest 固定 commit 624a673 核验。四个 locale 文件中无同键兄弟。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）26 OK → FINAL(0) f0a2（Opus 5.5）26/26，cycle 0 收敛（max_cycles 5）。r0a1 的 archive_agent 与 archive-intent 同批发出，记录顺序仍成立，见 `publication/HOST-NOTE-r0a1-archive-order.md`。
   - 门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：
     - 译文提交 `80b359b0c7ed26d96869106ac8f2842d4b82eb2b`；
     - 新 catalog `302702bb0c32c7523d675b2e385b412e6ea71045ae6758e6b7d19a89c681308e`；
     - migration `629e3b1e9540e64f5cc19bfa4f7aca45551eaf750c7ca33fa194b90da397229a`。
   - 后续：
     - 26 个 successor 必须重新审核，不继承旧 done，随重新复审轮在第392批起审核。
     - 窗口65积压 0 条。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行段落中的子串 `**993 个 successor** 排队待审（约 13 批，估算；第383–391批已审 720，余 273）`：替换为 `**993 个 successor**（另加窗口64 的 26 个）排队待审（约 13 批，估算；第383–391批已审 720，余 299）`；同一文件中子串 `确认待修项累计 ≥20 条再开合并修复窗口 64。` 替换为 `确认待修项累计 ≥20 条再开合并修复窗口（窗口 64 已于 2026-10-03 完成，下一个为窗口 65）。`（这两处子串替换算作第一处）。
   - 以 `更新时间：` 开头的行：整行改为 `更新时间：2026-10-03（修复窗口64已完成、待宿主证据提交与推送；下一步继续审核第392批）`。
   - 第一节以“- 修复窗口已闭合至 **63**”开头的单行条目：整体替换为一行 `- 修复窗口已闭合至 **64**：窗口63（译文 `7a7d8653`）与窗口64（第384–391批重新复审确认 25 条＋宿主补充 1 条，译文 `80b359b0`，migration `629e3b1e…`）均已修复；窗口64 的 26 个 successor 须重新审核，不继承旧 revision 的 done 状态。`
   - 第三节第 2 项：从以“2. 窗口 63 已完成”开头的行起，到以“   窗口 64 积压 **25** 条”开头的行止（含两端），整体替换为宿主已存的 `.ai/task/repair-w64-20261003/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）；其后以“   第391批计时（实测”开头的一行必须原样保留。

   第三节第 1、3 项及第四节必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：

- 逐字副本与 SHA；
- catalog/migration 精确复制；
- 文档链接、UTF-8 与空白；
- 只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w64-20261003/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-64-20261003/orchestration --target DONE`。

不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
