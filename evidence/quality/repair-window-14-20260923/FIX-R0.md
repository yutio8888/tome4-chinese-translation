# 修复窗口 14 — REVIEW(0) 有界修复记录

## 范围与裁决

本 fresh EXECUTOR run 只执行 `ADJUDICATION-R0.json` 中唯一的 `status=confirmed` finding：`R0-HOST-WINTERTIDE-NAME`。修复对象为 `mod-tome.lua` 珠宝师对话条，revision `ef7d5a43a10dc8eae43e1f4e8f15d7ca626123291c6d722daf5395cf2080324e`。

## 修改前后

- 修改前：`冬潮之月的一部分`
- 修改后：`霜华的一部分`
- 依据：`mod-tome.lua` 中 `t("Wintertide (Moon of Eyal)", "霜华（埃亚尔的卫星）", "entity name")`。

仅逐字替换上述片段；该 target 的其余文字、颜色标记与换行未改，另外 2 条 target 未改。

## 检查结果

- `python3 -B .ai/task/repair-w14-20260923/verify.py`：通过（exit 0，`verified: true`，22989 条记录，相对基线仍恰有冻结 workset 的 3 个 revision 变更）。
- `python3 -B tools/i18n lint --strict`：通过（exit 0，30308 translations，0 errors，0 warnings）。
- `python3 -B tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict`：通过（exit 0，`numeric=1 briefings=1 compositions=1 pending=1`）。
- `git diff --check`：通过（exit 0，无输出）。

本次未修改规则、工具、术语库、handoff/catalog/migration 或 `.ai`；未 stage、commit 或 push，并保留无关 untracked 文件。
