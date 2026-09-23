# 待用户集中审阅的争议条目

以下条目依据用户 2026-09-23 指示集中记录：有争议的条目列入 pending，不在当前修复窗口修改，也不阻塞窗口收束。前三条均来自窗口 8 的 `ADJUDICATION-R0.json`。

## 窗口 8 待审阅

1. `e92433bcba`（unlock-yeek）
   - 英文要点：叙事文本中的 `cunning`。
   - 现译：“灵巧”。术语库记录 `Cunning=灵巧`，类别为 stat name，`status=existing`。
   - 争议理由：宿主此前依据术语记录判定保持；surface、Opus contextual 与本轮 reviewer 共三个模型认为叙事语境应译为“机敏”或“狡黠”，且 `existing` 不代表覆盖所有语境。
   - 建议选项：保持“灵巧” / 叙事语境改“机敏”。

2. `e951739433`（毒素风暴）
   - 英文要点：`Each possible effect is equally likely`。
   - 现译：“中毒几率在可能的毒素效果中平分”。
   - 争议理由：源码 `damage_types.lua` 先等概率抽取效果，再判断目标能否中毒；宿主曾判现译与等概率语义等价，reviewer 认为现译把“效果等概率”写成了“中毒几率分配”。
   - 建议选项：保持 / 改为“各种可能的效果出现几率相同”。

3. `e988482539`（龙族传说）
   - 英文要点：“嘲笑将龙作为单独列出的智慧种族”的说法。
   - 现译：“嘲笑我把龙作为单独列出的智慧种族”，含原文没有的第一人称。
   - 争议理由：reviewer 两次指出原文没有“我”；宿主认为该系列是 Loremaster Greynot 的第一人称著作，语境允许这一增译。
   - 建议选项：保持 / 改为“嘲笑将龙归为智慧种族的想法”。

## 审核 254 的其他观察

- 宿主补充观察 `e923d2b8d0`：`The target is using talents without consuming resources` 现译为“不再消耗能量”，将 `resources` 窄化为“能量”。
- 审核 254 advisory：`ALL_DREAMS` 以外无其他同类项；另保留 `rogues do it from behind` 标题双关，以及 `SPELLSHOCKED` 省略 `temporarily` 两项建议。
