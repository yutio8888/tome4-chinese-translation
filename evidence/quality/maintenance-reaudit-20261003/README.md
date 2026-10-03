# 重新生产复审：目录迁移（2026-10-03 维护）

**来由**：用户 2026-10-03 要求“重新再走一轮生产复审流程”。第 382 批收口（`bfde8c53`）之后，译文经过机制修正与撤回、补充解释精简、生硬描述扫描 A／B 档及两轮交叉复核修正，这些改动都没有进入 WP2-Lite 复审目录。本次按 2026-10-01 补空格维护的先例（`evidence/quality/maintenance-placeholder-spacing-20261001/`），在译文 HEAD `ca558992` 上迁移目录，让改动过的条目以 successor 身份重新排队复审。

**门禁**：在 `ca558992` 上运行 `tools/ci-gates.sh`，17 项全过（`GATES-results.json`，实测 140.7 s）。

**catalog / migration**：`run_repair_steps.py publish-chain`（queue rebuild → catalog build → migration plan/check/apply，实测 170.8 s）。

- 旧 catalog `d33f8ddd7a549757946beed25f832e2b945b12d26868df9b3acbd13a5a207c50`（窗口 63）
- 新 catalog `c5d72508fd13ea589b9f3f37dd200b5096c71875d97d70882bf46a2d732e9e1b`
- migration `22b293c475cc9a132ae6955c2a366e3c1624001ef7e21ff44bc5d894ed643316`：993 条 `revision_changed`（全部为 `target_changed`），28,835 条不变，unmapped 0，ambiguous 0。

**核对**（`CATALOG-CHANGE-VERIFICATION.json`）：`diff_targets.py` 用 LuaJIT 分别加载 `bfde8c53` 与 `ca558992` 的六个目录文件，逐条比较译文，得到 993 处改动；`verify_migration.py` 确认 migration 每一行都是同一逻辑条目（路径、section、原文、source_tag 不变）的译文变化，且两边的（路径、section、原文、tag、旧译、新译）多重集完全一致，双方均无多余条目。分文件：mod-tome 680、tome-orcs 150、tome-cults 82、tome-ashes-urhrok 41、engine 25、mod-boot 15。

**来源阶段**（`STAGE-BREAKDOWN.json`，按提交区间分别比较）：

| 区间 | 内容 | 目录内改动 |
|---|---|---:|
| `bfde8c53..31c93a10` | 机制修正及撤回后保留的普通修正 | 44 |
| `31c93a10..1663a0a7` | 补充解释精简 | 16 |
| `1663a0a7..df5535a3` | 生硬描述 A 档修复包 | 626 |
| `df5535a3..ccedc7a0` | A 档交叉复核修正 | 6 |
| `ccedc7a0..4f626890` | 生硬描述 B 档修复包 | 322 |
| `4f626890..f2667fdc` | B 档交叉复核修正 | 4 |

其中 25 条在多个阶段都改过，按最终译文只算一次，合计 993。`tome-possessors.lua`（11 条）与 `tome-items-vault.lua`（2 条）的改动不在目录组件内，不进入复审队列；排除表中 11 条 Possessors 记录随译文变化更新了 occurrence 标识（条数不变，仍为 480）。

这 993 个 successor 须重新审核，不继承旧 `done`，约 13 批（993/80，估算）。
