# 修复窗口 5 第一次合并修复实施记录

本轮以 `.ai/task/repair-w5-20260922/BEFORE-FIX-1.lua` 为逐字符基线，只在 `mod-tome.lua` 的 3 个既有 revision 中实施 `FIX-1-REPLACEMENTS.json` 指定的 5 处 before/after 子句替换：

- `323606655f…`：“我们的魔法师找到了”改为“我们的族人破解了”。
- `e5dc6a60be…`：“操纵超越想象的力量”改为“玩弄我们无法控制的力量”；来袭者复仇意图改为佩里萨根据眼前人类叙述所作的引述。
- `e56b636891…`：黑暗触手的轨迹改为“不断蔓延的黑暗之雾”；伤害加成对象改为“任何进入你的黑暗之雾的目标”。

没有全面重译回忆录，也没有改动 source、source_tag、placeholder、markup 或其他 target。`RW5-R0-04.before` 在全文同时出现于范围外的 `Dark Torrent` 和本轮目标 `Dark Tendrils`；实施时按 revision 与 source 上下文只替换 `Dark Tendrils`，保留 `Dark Torrent` 不变。

实施后 `mod-tome.lua` SHA-256 为 `d161b1f96669e4efaf65b92bec72059dd7cedfd7605daf109ee70ad640fdd2f5`。本轮未修改 `.ai`、旧证据、其他译文、术语、规则或工具，也未 stage、commit、执行 handoff/catalog/migration 或完整门禁。
