# 修复窗口 11 — FINAL_REVIEW(1) F1 有界修复

## 修复范围

- 裁决：`.ai/task/repair-w11-20260923/ADJUDICATION-F1.json` 中唯一 `status=confirmed` 的 `F1-TORMENT-PER-TALENT-ROLL`
- revision：`ebcb3ef07162cd324a09d6a79dd7c76e4eb4ed2e7ef04b4c5121c6056309f6b3`
- 文件：`mod-tome.lua`
- source section：`mod-tome/data/talents/corruptions/torment.lua`
- source tag：`tformat`

## 固定源码依据

只读命令：

`git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/talents/corruptions/torment.lua | sed -n '144,149p'`

第 144–149 行在 `for tid, cd in pairs(self.talents_cd)` 循环内对每个技能分别调用 `rng.percent(c)`，仅将判定成功且非固定冷却的 `tid` 加入 `alt`，随后逐项减少 1 回合冷却。因此概率判定对象是每个冷却中的技能，而不是一次判定后让所有技能同时生效。

## 修改前后

修改前：

`你有 %d%% 概率降低所有技能 1 回合冷却时间。`

修改后：

`每个冷却中的技能各有 %d%% 概率减少 1 回合冷却时间。`

仅逐字替换上述短句。该条第一句前半、第二句、第三句、两个 `%d%%` 的顺序以及所有 TAB/LF 均未改动；其余 3 条 target 未改动。

## 检查结果

- `python3 -B .ai/task/repair-w11-20260923/verify.py`：通过（exit 0；`verified: true`；共 22989 条记录；相对基线仍恰为 4 个既定 revision 的 target 变化）。
- `python3 -B tools/i18n lint --strict`：通过（exit 0；检查 30308 条翻译，0 errors，0 warnings；报告为 `.artifacts/i18n/runs/20260923T091336.936261Z-2337658-lint/lint.json`）。
- `python3 -B tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict`：通过（exit 0；`OK  semantic claims numeric=1 briefings=1 compositions=1 pending=1`）。
- `git diff --check`：通过（exit 0，无输出）。

本次未修改规则、工具、术语库、handoff、catalog、migration 或 `.ai`，未 stage、commit、push，也未处理无关 untracked 文件。
