# 修复窗口 8 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 6 个 target；source、section、source_tag、args_order、printf 与 markup 均未改变。`e92433bcba…` 按冻结要求将“……有点滑稽。\n不过他们是……”合为一行，使 target 恢复为与 source 相同的 12 个 LF；其中 `cunning=灵巧` 保持不变。其余 5 个 target 的 LF/TAB 序列保持基线。

## 实际修复

- `e8fc5b0a4a…`：恢复“每天拖起疲惫身体，开始无尽狩猎”的原义，删除“不知疲倦”和“下一个目标”的反向或新增信息。
- `e90949f925…`：仅将 `ALL_DREAMS` 成就名改为“做着我的梦”，不改描述。
- `e92433bcba…`：仅合并多出的换行；“灵巧”及其余文字保持不变。
- `e925366829…`：仅修复 `Once flowers rose to reach the sky` 与 `Now all lost, now all fled` 两行，分别译为“曾经鲜花高耸，直抵天际”和“如今一切尽失，一切消逝”；其余诗句保持不变。
- `e951739433…`：明确麻痹毒素使目标造成的全部伤害降低 `%d%%`，未改其他机制描述或占位符。
- `e988482539…`：仅补回 `over 40'`、`may be borne purely from ... delusions`、`The Daikara Pass and surrounding mountain chains` 与 `newly matured drakes` 四处语义；第一人称增译等 advisory 保持不变。

## 固定源码补查

按任务要求，以只读 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查了 cursed 技能树、`ALL_DREAMS`、Yeek 解锁文本、龙族传说与诗句、毒素风暴说明及 `NUMBING_BLIGHT` 效果实现。补查内容与冻结的 `SOURCE-ANCHORS.json`、`SOURCE-CLAIMS.json` 一致，未发现需要扩大范围的冲突。

## 不变量与验证

任务验证脚本通过 LuaJIT 全记录比较确认恰有 6 个 target 变化，其余记录字段不变；printf、markup、特殊 token 与适用的 LF/TAB 序列均满足冻结要求。严格 lint、语义 claim 回归和 `git diff --check` 均通过，真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH254.json` 是 `.ai/task/repair-w8-20260923/PREFLIGHT-BATCH254.json` 的逐字节副本，SHA-256 为 `1c0a95d6a586710c86b709b86fb7704cf475d177c4d8fa8705f2b7c91dd9f09f`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w8-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `4b36f7e9d941b1de7906a536d6d51dc43a705f73754d78c0b99952e57633955e`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w8-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `41eff6ef4cf24033ab0943d585b994072bd94a62cd6410746e46125f0919ac5f`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未更新仓库根 handoff。
