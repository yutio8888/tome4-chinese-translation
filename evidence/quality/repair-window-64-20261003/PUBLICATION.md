# 修复窗口 64 发布记录

## 范围

本窗口修复 26 条译文（`mod-tome.lua` 25 条、`engine.lua` 1 条），无术语改动。

- 2026-10-03 重新复审轮第 384–391 批宿主确认 25 条（各批 `HOST-FINAL-DECISIONS.json`）：
  - 换行不变量 9 条：科斯汀望远镜、扭曲的波法斯特、战斗属性教程、粘胶方块、升级教程、高等人类开场、属性教程 stats7.1、符文：粉碎痛苦、多元水晶球。
  - 忠实性、机制与术语 16 条：盾战士简介、内购欢迎词、巫妖、调试升级对话框、腐蚀蠕虫、冰冷杀戮、暗夜流光、破损的阿塔玛森、影之护甲、永恒精灵加载提示、占位技能 fungus、疯狂诅咒、暗影射击、埃亚尔的呼吸、生死珍珠、无尽追踪。
- 宿主补充 1 条：第 390 批裁决附记的骤然生长（Sudden Growth）“孢子”→“真菌”。
- 新译文由宿主按各条“修复：”与整句对照写定（[`publication/NEW-TARGETS.json`](publication/NEW-TARGETS.json)），EXECUTOR 逐字替换；宿主核验 26 条 after 与 new_target 逐字相等（[`publication/HOST-EXACT-DIFF.json`](publication/HOST-EXACT-DIFF.json)）。
- 主游戏与引擎按 manifest 固定 commit `624a673` 核验。四个 locale 文件中无同键兄弟。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）26 OK → FINAL(0) f0a2（Opus 5.5）26/26，cycle 0 收敛（max_cycles 5）。r0a1 的 archive_agent 与 archive-intent 同批发出，记录顺序仍成立，见 [`publication/HOST-NOTE-r0a1-archive-order.md`](publication/HOST-NOTE-r0a1-archive-order.md)。

门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交 `80b359b0c7ed26d96869106ac8f2842d4b82eb2b`；
- 新 catalog `302702bb0c32c7523d675b2e385b412e6ea71045ae6758e6b7d19a89c681308e`；
- migration `629e3b1e9540e64f5cc19bfa4f7aca45551eaf750c7ca33fa194b90da397229a`。

## 后续

- 26 个 successor 必须重新审核，不继承旧 done，随重新复审轮在第 392 批起审核。
- 窗口 65 积压 0 条。
- 本 publication child 待宿主归档。
