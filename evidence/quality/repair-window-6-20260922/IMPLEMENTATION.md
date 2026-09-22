# 修复窗口 6 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的两个 target；source、section、source_tag、args_order、special、printf、markup 与 TAB 均未改变。

## 实际修复

- `e7091b21dc…`：只在省略号前后各恢复一个空行，使 target 从 3 个 LF 恢复为与 source 相同的 5 个 LF；全部文字保持不变。
- `e7e5e7f4e5…`：改为“惊扰了古战场，并在由此引发的后果中幸存下来。”，恢复玩家主动惊扰古战场以及从相应后果中幸存的语义；target 的 LF 保持 0。

固定源码中，`game/modules/tome/data/general/events/old-battle-field.lua` 的坟墓交互先询问玩家是否要 `disturb the grave`，确认后挖掘导致地面坍塌并进入古战场事件；玩家熬过亡灵袭击计时后，源码调用 `world:gainAchievement("EVENT_OLDBATTLEFIELD", ...)` 授予成就。因此第二条译文同时保留主动触发和后果关系。

## 不变量与数值 placeholder

任务验证脚本以 LuaJIT 全记录比较确认恰有两个 target 变化，其余记录字段不变；printf、markup、特殊 token 与 TAB 序列均保持。两条 source/target 均无数值 placeholder，因此 directional value-flow 不适用。

## 冻结副本

- `PREFLIGHT-BATCH252.json` 是 `.ai/task/repair-w6-20260922/PREFLIGHT-BATCH252.json` 的逐字节副本，SHA-256 为 `3ab167b07c2cb4ff2166c72a0ced6ddc0df984281ba419cfed320e350ca11140`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w6-20260922/WORKSET.json` 的逐字节副本，SHA-256 为 `dfc159bd916c2f1ab2cc503ba59289bde9f07b00817c03101f909d26255f50bc`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w6-20260922/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `ca1c8d0dce34b58a5ef4d7e53a7337d5db53dc4ca83be439a1192d10a836f615`。

## 尚未执行的后续阶段

本记录仅覆盖唯一 EXECUTOR 的实施与用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建、`DONE_VERIFIED`、stage、commit、catalog/migration、queue rebuild 与 push 均未执行，也不在本记录中声称通过。
