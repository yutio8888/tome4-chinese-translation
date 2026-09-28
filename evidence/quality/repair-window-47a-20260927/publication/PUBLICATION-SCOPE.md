# 窗口47a证据发布范围

唯一 publication EXECUTOR 只写：`evidence/quality/repair-window-47a-20260927/`、`handoff.md`、候选 catalog 内对应的 `evidence/production-review-v2-lite/catalog/` 三文件、候选所含 `i18n/quality/production-review-v2-lite/catalog-v1.schema.json` 与 `policy-v1.json`、以及 `evidence/production-review-v2-lite/migrations/ac10dc6364c2c5edafce574d5b15610cb800a2d4551f61f5f76db4ddd056b7c2.json`。不改 Lua、术语、规则、工具、其他 evidence、`.ai/task`、`.ai/reviews`、`pending-user-review.md`；不 stage/commit/push，不创建 agent，不重跑 queue/catalog/migration/门禁。窗口目录中已有的 `IMPLEMENTATION.md` 与 `VALIDATION.json` 保持不动。

1. 按 `.ai/task/repair-w47a-20260927/PACK-MANIFEST.json` 将全部 `files` 精确安装到 `evidence/quality/repair-window-47a-20260927/orchestration/<relative_destination>`，逐项核 SHA-256。已有同字节可保留，异字节必须停止。将 manifest 逐字复制到窗口根目录 `orchestration-pack-manifest.json`。
2. 将 `.artifacts/i18n/repair-window/window47a-20260927-candidate-catalog/` 内所有文件按相对路径逐字复制到仓库对应路径；将 `.artifacts/i18n/repair-window/window47a-20260927-migration.json` 逐字复制到上述 migration 目标。已验证 77 revision_changed（均为 workset，无 runtime-sync）、29751 unchanged、0 ambiguous/unmapped、77 successor 新队列，无须重跑。
3. 在本窗口 `publication/` 逐字复制 task 的 `PUBLICATION-SCOPE.md`、`CATALOG-CHANGE-VERIFICATION.json`、`MIGRATION-HOST-VERIFICATION.json`、`TRANSLATION-COMMIT.json`、全部 `ADJUDICATION-*.json`；从 `.artifacts/i18n/repair-w47a-20260927/` 逐字复制 `HOST-SUPPLEMENT-CLAIMS.json`、`CARRY-FORWARD-47B.md` 与全部 `HOST-NOTE-*.md`（共 5 个）；复制 `.artifacts/i18n/repair-window/window47a-20260927-publish-chain.log`、`window47a-20260927-publish-chain-timing.json`、`window47a-20260927-migration.json`、`window47a-20260927-migration-timing.json`，去掉 `window47a-20260927-` 前缀作为 publication 文件名。
4. 写本窗口 `PUBLICATION.md`，内容如下：
   - 范围：A 组（用户 2026-09-27 对待审清单的裁决中涉及术语库改动与全局改名的部分），77 条＝第356批确认项 `3724ff9284` 1 条＋宿主补充 76 条：Eyal“埃亚尔大陆”→“埃亚尔”24（含 Orcs 一处瓦·埃亚尔）、Numbing 族→“麻木”25、Sunwall→“太阳堡垒”5、Ureslak→“乌瑞斯拉克”9、Crimson Templar→“血色圣殿骑士”6、DESTRUCTICUS 6、Gardanion 1；第356批条目为口袋时间 lore（巨魔 tossed around 与七彩巨龙）；涉及 mod-tome.lua、tome-ashes-urhrok.lua、tome-cults.lua、tome-orcs.lua 四个文件。术语库 6 个 TSV 先于译文修改：新增/调整 Eyal、numbing、paralyzed、Ureslak、Crimson Templar、两个物品名、sunwall 升 preferred、manaburn 与 multi-hued 注释、Fire Imp＝火焰小鬼（用户 2026-09-28 裁决），并把 affinity 行更正为游戏界面用语“伤害亲和”。领域映射 `tools/annotate_domains.py` 登记三个新实体名。Ashes/Cults/Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。
   - 范围扩展：首轮 FINAL 后按 `HOST-NOTE-scope-widening.md`，把 workset 内经源码确认的旧缺陷一并修复（长 lore 条目的漏译、所属关系颠倒、“黑暗麻木”→“暗影麻木”、“伤害吸收”→“伤害亲和”等），不扩大条目集合；workset 外同类问题转入窗口 47b（见 `CARRY-FORWARD-47B.md`）。
   - 轮次：用户为本窗口单独授权放宽 max_cycles（先至 6、再至 7，最终至多 10），其他窗口仍为 5。
   - 复审路径（各轮裁决见 publication/ADJUDICATION-*.json）：REVIEW(0)、RE_REVIEW(1)–(10)（GPT-6 Sol）与 FINAL(0)(6)(7)(9)(10)（Opus 5.5）；共十一次修复（execute-01…11）；r5a1 因输出顺序无效、f9a2 因原生日志并行 tool_use 侧枝被 parser 拒收（宿主登记其发现），均不计轮次。已驳回：Weirdling Beast、Ureslak 套装加成、Aeryn 已死、workset 内“莎西·凯希”写法；advisory：`f5f092ac5d` 歌词 ogre/over 双关、Destructicus 瞄准措辞。cycle 10 FINAL f10a2 77/77 OK。
   - 工具：`tools/orchestration/review_lifecycle.py` 放行两种良性原生日志形状（Codex 跨零点 environment_context 注入、Claude 并行 tool_use 侧枝），各附单测；见 `HOST-NOTE-execute-01-date-rollover.md` 与 `HOST-NOTE-f9a2-parallel-branch.md`。
   - 门禁：17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。
   - 标识：工具提交 `94e5a35cf5c1333e8801ba43c0f8ea91baec4c41`；译文提交 `78123847745c86c76033048b0b07b63cb89cc4f1`；新 catalog `c7abbba1362d6924552bd273e7d7e5466876f9a7921185fa6aacf6cd86790481`；migration `ac10dc6364c2c5edafce574d5b15610cb800a2d4551f61f5f76db4ddd056b7c2`。
   - 后续：77 个 successor 必须重新审核，不继承旧 done。下一步窗口 47b（B 组单条措辞与名称，并纳入 `CARRY-FORWARD-47B.md` 转入项）。
   - 本 publication child 待宿主归档。
5. 更新 `handoff.md`，只改以下四处，其余逐字保留：
   - 第3行“更新时间”行改为：`更新时间：2026-09-28（修复窗口47a已完成、待宿主证据提交与推送，下一步开修复窗口47b）`。
   - 第一节以“- 修复窗口已闭合至 **46**”开头的那一整行改写为：`- 修复窗口已闭合至 **47a**：A 组术语库改动与全局改名 77 条（第356批 1 条＋宿主补充 76 条，四个 Lua 文件）已修复；译文提交 `78123847745c86c76033048b0b07b63cb89cc4f1`；migration `ac10dc63…` 的 77 个 successor 须重新审核，不继承旧 revision 的 done 状态。下一步窗口 47b（B 组单条措辞与名称及 47a 转入项，见第五节第 2 项）。`
   - 第五节第 1 项续行：只把“修复积压达 20 再开窗口 47（模板 `setup_window46.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w46-20260927/wd.sh`、`/tmp/w46-*.sh`；setup 后先跑 `check_siblings.py`）。”改为“修复积压达 20 再开下一窗口（模板 `setup_window47a.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`.artifacts/i18n/repair-w47a-20260927/wd.sh`、`/tmp/w47a-*.sh`；setup 后先跑 `check_siblings.py`）。”，其余文字保留。若该句原文与此不完全一致，只替换其中的窗口号与模板路径并在报告中说明。
   - 第五节第 2 项：只替换第一行（以“2. 窗口 46 已完成”开头的那一整行）为宿主已存的 `.ai/task/repair-w47a-20260927/HANDOFF-ITEM2.txt` 全文（逐字取用，不带末尾换行）。
     紧随其后以“   第356批计时（实测”开头的一行必须原样保留（下一批 handoff 生成器依赖它）。
   第五节第 3、4、5 项必须原样保留，不得删除或改写。不要在 child 文档里提前宣称宿主动作已完成。

验收：逐字副本与 SHA、catalog/migration 精确复制、文档链接/UTF-8/空白；只读运行 `python3 -B tools/ai_state_check.py .ai/task/repair-w47a-20260927/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-47a-20260927/orchestration --target DONE`。不要运行 `verify_pack.py`。最后报告实际文件和验证结果。
