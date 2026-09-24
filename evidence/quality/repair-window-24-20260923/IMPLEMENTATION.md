# 修复窗口 24 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 6 个 target，并在本目录保存冻结副本与真实验证结果；source、section、source_tag、args_order、printf 占位符、`%%`、markup 均未改变。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `f99ebf3aa3…`（飞镖发射器日志）：将“抵抗了睡眠”改为“抵抗了镇静”，与 `Sedated` 的现有译名“被镇静”一致。
- `f9b4a1d58a…`（敏锐直觉）：首句改为从未来的片刻中获取信息，不再增译“直觉”；侦测隐形、侦测潜行、法术暴击三项合回原文第二行，恢复为 3 行。
- `fa2a8ff283…`（狂热）：明确 4 次“快速”攻击且伤害是“每次”计算；附近有被追踪猎物时“总是攻击它”；第二句补回每个被命中目标均会被压倒的含义，并恢复盾牌句前空行。
- `fa465502e5…`（奥术至上法杖）：补回亮银色符文，恢复两句之间的换行，并将结尾改为“单独一件时似乎并不完整”。
- `fa46681a10…`（吸食抗性）：将“对‘所有’抗性无效”并回第一行，只在“效果受精神强度加成”前保留原文的一处 `\n\t\t`。
- `fa9d429c2d…`（意志说明）：删去原文没有的“精神力”，按原文保留法力值、体力值、灵能值上限与精神豁免。

## 固定源码补查

仅使用 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查六条对应源码。飞镖日志使用 `EFF_SEDATED`；狂热循环执行 4 次攻击且附近的被追踪猎物每次均被选中；奥术至上法杖与奥术理解之帽互为套装；其余源串与冻结 `SOURCE-ANCHORS.json` 一致。未发现范围冲突。

## LF/TAB 逐行核对

以 1 为起点记录空行下标；TAB 数组按每行行首 TAB 数排列。六条 source/target 结果分别为：

- 飞镖日志：`1/1` 行，空行 `[]/[]`，TAB `[0]/[0]`。
- 敏锐直觉：`3/3` 行，空行 `[]/[]`，TAB `[0,2,2]/[0,2,2]`。
- 狂热：`5/5` 行，空行 `[4]/[4]`，TAB `[0,2,2,0,2]/[0,2,2,0,2]`。
- 奥术至上法杖：`2/2` 行，空行 `[]/[]`，TAB `[0,0]/[0,0]`。
- 吸食抗性：`2/2` 行，空行 `[]/[]`，TAB `[0,2]/[0,2]`。
- 意志说明：`1/1` 行，空行 `[]/[]`，TAB `[0]/[0]`。

窗口专用验证脚本同时按全记录比较确认恰有 6 个 target 变化，且每条 LF/TAB 序列与 source 一致。

## 冻结副本

- `PREFLIGHT-BATCH270.json` 是 `.ai/task/repair-w24-20260923/PREFLIGHT-BATCH270.json` 的逐字节副本，SHA-256 为 `4bbf76b98beb5a5bdfd04de7d71774affeada44c021042673c20599c3808122f`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w24-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `42920fed3f175dfc903fbc85e05de5b6a49703ab307a08c321b6bf8fcb93ddb9`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w24-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `af315186bd3137bdec96dd521b15719c60f1e0f4d54cf5c3a577815ec17b903c`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未修改 `.ai`、规则、工具、术语库或 handoff。
