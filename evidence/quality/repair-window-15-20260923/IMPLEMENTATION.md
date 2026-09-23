# 修复窗口 15 实施记录

固定来源为 ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。本次仅修改 `mod-tome.lua` 中 `HOST-WORKSET.json` 列出的 2 个 target，并写入本 evidence 目录；source、section、source_tag、args_order、printf 占位符、markup、LF 与 TAB 均未改变。未扩展 advisory、pending 或其他 repair。

## 实际修复

- `f0d4b3e8f3…`：保留半身人创世论的 9 个段落边界。将 `ridiculous ideals` 恢复为“可笑观念”；将对马基·埃亚尔的 `feelings of entitlement` 恢复为半身人自认一切理应归己的心态；将 `other gods were responsible` 恢复为别的低等神明造了其他种族，并补回其模仿宏伟设计的信息；紧接句恢复“手法拙劣、毫无雅致，远逊于造就我们的精妙与完美”。
- `f0d4b3e8f3…` 逐句对照还修复了同一 target 内的明显增删或错指：精灵被真相蒙羞而非“故意隐藏”，人类每村的是当地传说而非特指创世故事，神创造了独立于自身并行走大地的生灵，永恒精灵进行的是魔法实验，夏·图尔远行传送门及 `elder brethren` 的指向也已恢复。其余已忠实句子未重写。
- `f0fdd62c2d…`：保留 `#GOLD#` 和“回归之杖”，将 `vowing to come back later` 改为“发誓日后再回来”，删除原文没有的“救他”。

## 固定源码补查

仅以 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 补查了 `game/modules/tome/data/lore/misc.lua:214-235` 和 `game/modules/tome/data/zones/halfling-ruins/npcs.lua:84-95`。结果与冻结的 `SOURCE-ANCHORS.json` 和 `SOURCE-CLAIMS.json` 一致，未发现范围冲突。专名已先在 `mod-tome.lua` 查证，沿用“马基·埃亚尔”、“夏·图尔”、“永恒精灵”、“自然精灵”、“远行传送门”和“回归之杖”。

## 不变量与验证

窗口专用验证脚本通过全记录比较确认恰有 2 个 target 变化，其他记录字段不变；source/tag/args_order、printf 占位符、markup、LF 与 TAB 均保持基线。严格 lint、语义 claim 回归和 `git diff --check` 均通过，真实命令与结果记录于 `VALIDATION.json`。

## 冻结副本

- `PREFLIGHT-BATCH261.json` 是 `.ai/task/repair-w15-20260923/PREFLIGHT-BATCH261.json` 的逐字节副本，SHA-256 为 `676ca1a50ad4bd2b6ffd4955d6943bb693fe1784d22122a2c35fd342810ad6f9`。
- `HOST-WORKSET.json` 是 `.ai/task/repair-w15-20260923/WORKSET.json` 的逐字节副本，SHA-256 为 `78b09fc8e98c9d9fef71965aff9c2b5a3a7517594b12f54cf9c70621e803da69`。
- `SOURCE-ANCHORS.json` 是 `.ai/task/repair-w15-20260923/SOURCE-ANCHORS.json` 的逐字节副本，SHA-256 为 `59d2dd363cf0163fc798cf27ad1419cbf9e01611863b6bd9ac8e88c8d8612bf9`。

## 宿主后续

本记录只覆盖唯一 EXECUTOR 的实施和用户指定的定向检查。独立 REVIEW、FINAL_REVIEW、完整门禁、严格构建与 `DONE_VERIFIED` 仍由宿主继续；本执行未 stage、commit、queue、catalog/migration 或 push，也未更新 handoff。
