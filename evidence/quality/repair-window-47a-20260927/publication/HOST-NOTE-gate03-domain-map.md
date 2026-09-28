# 宿主说明：首次收口门禁 03 失败（领域映射）

首次运行收口门禁（run.1nfdpwo2，2026-09-28）在 `03-toolchain-unit-tests` 失败：`test_real_terminology_is_fully_mapped` 调用 `tools/annotate_domains.py`，本窗口新增的三个 `T.GAME.ENTITY` 术语行（Fire Imp、Gardanion, the Light of God、DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY）没有领域映射，报为未映射；测试另断言的术语行数 722、声明/推导领域不一致数 6 也随新增行变为 730 与 7（新增的 Ureslak 行放在 creatures.tsv、类别为 T.PN.PERSON，推导为 society，属 advisory）。

处理：在 `tools/annotate_domains.py` 把 Fire Imp 加入 CREATURE_SOURCES、两个物品全名加入 ITEM_SOURCES，并把测试期望更新为 730／730／7。两文件随译文提交（依赖同一提交中的术语行）。宿主中止了失败的运行，旧日志移至 `.artifacts/i18n/repair-w47a-20260927/stale-gates/`，重跑（run.gqyrhm6h）17/17 全过，含严格构建。译文与术语未因此改动。
