# 修复窗口 60 发布记录

## 范围

本窗口包含 6 条译文（全部位于主游戏 `mod-tome.lua`）以及 `terminology/talents.tsv` 的 1 行插入、1 行替换，依据用户 2026-10-01 的两项裁决：

- “将deeprock技能树修改为深岩”：`926d166627` 的 talent type deeprock 由“深岩形态”改为“深岩”；技能 Deeprock Form 保持“深岩形态”。`1ebce25bfc` Mountainhewn 说明中指该形态的两处统一为“深岩形态”：第二行 while Deeprock Form is active 由 execute-01 修改；首行 while in deeprock form 由“当你进入深岩元素形态时”改为“处于深岩形态时”，在 FINAL f0a2 确认后修复。
- “一并修复之前发现的非阻断问题”（窗口 59 `ADJUDICATION-F2` advisory）：Korbek 实验笔记 part one–four 的正文标题由“：一/二/三/四”改为“，第一部分”等（`874773600`、`b9fa6649f1`、`58faaf57f6`、`233e49293a`）。

术语库新增 deeprock＝深岩（preferred），并将 Deeprock Form 改为 preferred。主游戏内容按 manifest 固定 commit `624a673` 核验；无同键兄弟。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-*.json`](publication/)：execute-01 → REVIEW(0) r0a1（GPT-6.1 Sol）6 OK → FINAL(0) f0a2（Opus 5.5）1 确认（首行“进入…时”误作瞬时且使用了 Deeprock Elemental 译法；宿主 setup 时误把首行判为普通描述）→ execute-02 → RE_REVIEW(1) r1a1 6 OK → FINAL(1) f1a2 6/6，cycle 1 收敛（`max_cycles` 5）。

## 门禁

首次运行发生在修复前，已作废（`SUPERSEDED-GATES-pre-fix1`）。修复后运行门禁 03 失败，原因是单测钉死术语行数 915，而新增 deeprock 行后为 916（`SUPERSEDED-GATES-count-pin`）。宿主随后将 SCOPE 扩至 `tests/i18n/test_toolchain_static_audit.py` 与 `TERMINOLOGY.md`（见 [`publication/SCOPE.json`](publication/SCOPE.json) 的 `scope_expansions`）；execute-03 仅将 915 改为 916（两处），并将 talents 计数 347 改为 348，译文与术语文件 SHA 均未改变。重跑 17/17 全过，包含严格构建；状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`d62fe6ffd5845af719f43caf7a79611a366c6e3d`
- 新 catalog：`456e88e5f2bc316309b070d4d2b10e19660191676cd7e0529f2fbaff478bd21f`
- migration：`8bdc639e15e39bbe828cbe73cbd87ce54883705b28c1a689e9b3efc04d7bbb9a`

## 后续

6 个 successor 必须重新审核，不继承旧 done；其中 Korbek 4 条原为窗口 59 的 successor，以本窗口版本为准。窗口 61 积压 0 条。

本 publication child 待宿主归档。
