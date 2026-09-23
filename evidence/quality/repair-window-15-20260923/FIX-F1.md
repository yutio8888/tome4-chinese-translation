# 修复窗口 15 — FINAL_REVIEW(1) F1 有界修复

## 范围与裁决

本 fresh EXECUTOR run 只执行 `ADJUDICATION-F1.json` 中唯一的 `status=confirmed` finding：`F1-LORE-PRESUME-LOGIC`。修复对象为 `mod-tome.lua` 中半身人创世论条目，revision `f0d4b3e8f3bbab1a94fc6884d4dbc22c33995f7299f5c2d2a6d633bb2d439db1`；只改 target 的最后两段。

## 固定源码依据

对照固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的 `game/modules/tome/data/lore/misc.lua:232,234`：

- `One must presume that our god made this race before us, but was somehow unhappy with them, and so removed them and made us instead.`
- `One must presume strife between them, and that they killed themselves, or took their battle away from the world.`

前者的整个命题均在 `must presume` 的推测范围内，`somehow` 表示不清楚为何不满，而不是将“不满”降为可能。后者先推定众神间发生冲突，再在“同归于尽”与“把战斗带离世界”两种结局中二选一。

## 修改前后

1. 夏·图尔段的推测范围：

   - 修改前：`可以肯定我们的创造者在我们之前制造了他们，但是可能不满意他们，于是将他们移除，另外创造了我们。`
   - 修改后：`只能推测我们的神在我们之前创造了这个种族，却不知为何对他们不满，于是将其移除、改而创造了我们。`

2. 众神去向段的逻辑结构：

   - 修改前：`那么在那些神创造了这些种族后又发生了什么？肯定是他们之间发生了纠葛，或者他们同归于尽，亦或是他们的战场远离了这个世界。我们的创造者，看到其他众神，或是被杀或是离开，肯定是将这个世界委托给了我们半身人，因为他知道我们将代替他掌管这个世界。`
   - 修改后：`那么，那些神创造了我们如今所见的种族后，又发生了什么？只能推定众神之间发生了冲突，结局要么同归于尽，要么把战斗带离了这个世界。我们的创造者看到其他众神或被杀、或离开，想必随后便将这个世界委托给了我们半身人，因为他知道我们将代替他掌管这个世界。`

第 2 处同时补回 `which we see today` 的“我们如今所见”，并把 `must have then entrusted` 保持为“想必随后便……”的推定语气，理清 `other gods killed or left` 的受事关系。末两段的其余句子逐句对照后未发现断言/推测倒置或信息增删，均未改动。前七段、另一条 target 及段落换行未改。

## 检查结果

- `python3 -B .ai/task/repair-w15-20260923/verify.py`：通过（exit 0；`verified: true`；22989 条记录；相对基线仍恰有冻结 workset 的 2 个 revision 变更）。
- `python3 -B tools/i18n lint --strict`：通过（exit 0；30308 translations；0 errors，0 warnings）。
- `python3 -B tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict`：通过（exit 0；`numeric=1 briefings=1 compositions=1 pending=1`）。
- `git diff --check`：通过（exit 0，无输出）。

本次未修改规则、工具、术语库、handoff/catalog/migration 或 `.ai`；未 stage、commit 或 push，并保留无关 untracked 文件。
