# 修复窗口 65 发布记录

## 范围

本窗口修复 11 条译文（`tome-orcs.lua` 8 条、`mod-tome.lua` 1 条、
`tome-ashes-urhrok.lua` 1 条、`tome-cults.lua` 1 条），无术语改动。

- 2026-10-03 重新复审轮第 392–395 批宿主确认 9 条（各批
  `HOST-FINAL-DECISIONS.json`）：
  - 换行与缩进不变量 3 条：物品教程删 2 个多余换行；雷鸣榴弹与精神碾压的全角空格改回
    `\t\t`，精神碾压同时补回末行。
  - 忠实性与机制 6 条：恶魔结合改为通过种子召唤恶魔；克罗格解锁文本补译并把伊格兰斯改回
    伊格；电子咒式补“或技能”；电力放出的电弧伤害补“闪电”；爆矢枪改为多管弩箭发射器与
    毒弹；任务“已死之神在等待”的通关描述补克鲁克部落与“高阶”。
- 宿主补充 2 条（不计积压，第 394 批 `HOST-FINAL-DECISIONS.json` 的
  `additional_host_observations`）：火箭靴补回 `\t\t` 并改末句；紧急蒸汽排出删多余换行并
  整句改写。
- 新译文由宿主按各条“修复：”与整句对照写定
  （[`publication/NEW-TARGETS.json`](publication/NEW-TARGETS.json)），EXECUTOR 逐字替换；
  宿主核验 11 条 after 与 new_target 逐字相等
  （[`publication/HOST-EXACT-DIFF.json`](publication/HOST-EXACT-DIFF.json)）。
- 主游戏按 manifest 固定 commit `624a673` 核验；三个 DLC 源码来源未固定，按公开源码核验并
  如实标注。四个 locale 文件中无同键兄弟。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-R0.json`](publication/ADJUDICATION-R0.json) 与
[`publication/ADJUDICATION-F0.json`](publication/ADJUDICATION-F0.json)：execute-01 →
REVIEW(0) r0a1（GPT-6.1 Sol）10 OK／1 ISSUE → FINAL(0) f0a2（Opus 5.5）11/11，
cycle 0 收敛（max_cycles 5）。r0a1 对 `557285f8a1`（电力放出）的 ISSUE：Orcs 源码最多
连到 nb−1 个其他目标，而英文写 “arcs to %d other targets”，译文与英文一致；按用户
2026-10-03 撤回决定，英文与实现矛盾不在译文中改写，宿主判 advisory carry_forward
（[`publication/ADJUDICATION-R0.json`](publication/ADJUDICATION-R0.json)），FINAL 判该条 OK。

门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交 `9079821a2d8f61ff9b84e1e7e111c2af65bd0cc1`；
- 新 catalog `fa20187008d51eaab572200028302cc7cfdf7bc69a16a4270d1f71013db6bff4`；
- migration `e437cb51838bcc569d772a905f70dfe23b175537a8b2a4a9f1e1b1c19022685f`。

## 后续

- 11 个 successor 必须重新审核，不继承旧 done。
- 下一个修复窗口（66）积压 0 条。
- 本 publication child 待宿主归档。
