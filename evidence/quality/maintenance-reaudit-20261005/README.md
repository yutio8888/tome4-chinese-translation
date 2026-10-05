# 重新生产复审（第二轮）：目录迁移（2026-10-05 维护）

**来由**：用户 2026-10-05 要求对生硬描述扫描 A、B、C 档的润色“再走一轮生产复核”。A、B 档的改动已在 2026-10-03 那一轮（迁移 `22b293c4…`，第383–395批）复审过，本轮复审的是此后未经复审的改动：C 档修复包、C 档交叉复核修正与搁置项处理。按上一轮先例（`evidence/quality/maintenance-reaudit-20261003/`），在 HEAD `e1e6425c` 上迁移目录，让改动过的条目以 successor 身份重新排队。

**门禁**：在 `e1e6425c` 上运行 `tools/ci-gates.sh`，17 项全过（`GATES-results.json`，实测 142.4 s，取自该次运行 results.json 的起止时间）。

**catalog / migration**：`run_repair_steps.py publish-chain`（queue rebuild → catalog build → migration plan/check/apply，实测 182.2 s，见 `migration-timing.json`）。候选目录与 migration 产物由编排方逐字复制到 `evidence/production-review-v2-lite/`。

- 旧 catalog `fa20187008d51eaab572200028302cc7cfdf7bc69a16a4270d1f71013db6bff4`（窗口 65）
- 新 catalog `47745eccd033aa7f5e082751190f5e86788685412abdc5b37eebd6173d44cf36`
- migration `87fb68827c99166a0acf620f53072ff06efd65dbaefa74de7db74a537a85d01e`：494 条 `revision_changed`（全部为 `target_changed`），29,334 条不变，unmapped 0，ambiguous 0。

**核对**（`CATALOG-CHANGE-VERIFICATION.json`）：`diff_targets.py` 用 LuaJIT 分别加载 `9079821a`（窗口 65 译文，即旧 catalog 的基线）与 `e1e6425c` 的六个目录文件，逐条比较译文，得到 494 处改动；`verify_migration.py` 确认 migration 每一行都是同一逻辑条目（路径、section、原文、source_tag 不变）的译文变化，且两边的（路径、section、原文、tag、旧译、新译）多重集完全一致，双方均无多余条目。分文件：mod-tome 301、tome-cults 91、tome-orcs 77、tome-ashes-urhrok 25。

**来源阶段**（`STAGE-BREAKDOWN.json`，按提交区间分别比较）：

| 区间 | 内容 | 目录内改动 |
|---|---|---:|
| `9079821a..a1d40dfc` | 生硬描述 C 档修复包 12–16 | 482 |
| `a1d40dfc..e255bdfc` | C 档交叉复核修正 | 8 |
| `e255bdfc..aea17710` | C 档搁置项处理（含同运行键同步 1 行） | 16 |

其中 12 条在两个阶段都改过（交叉复核修正的 8 条、壁画前缀 4 条），按最终译文只算一次，合计 494。`tome-items-vault.lua` 的 3 条改动不在目录组件内，不进入复审队列。

这 494 个 successor 须重新审核，不继承旧 `done`，约 7 批（494/80，估算），从第397批起。
