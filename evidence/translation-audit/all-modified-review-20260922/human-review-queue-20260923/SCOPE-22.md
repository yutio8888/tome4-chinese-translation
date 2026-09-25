# SCOPE-22 报告：wave 1–3 confirmed 修复 + cycle-1 复审

task_id: `human-review-adjudication-20260923`
phase: `scope-22`（wave 1–3 的 11 项 confirmed 修复）
日期: 2026-09-25
baseline: `74decd75`
drafter: `pi/cpa/gemini-3.8-flash-high`（agent `7cf29501`，high）
executor: `codex/gpt-6-sol`（agent `9da1c89b`，medium）

## 1. 范围与更正

修复 `PUBLIC-WAVE{1,2,3}-ADJUDICATION.json` 中 **11 项 confirmed**（`00184`/`00492` 主工作区已修，不在本批）。

| entry | 文件 | 改动 |
| --- | --- | --- |
| `entry-00111` / `entry-00145` | `engine.lua` / `mod-boot.lua` | `嵌件系统`/`嵌件`（4 处）→ **蒸汽工具**（`terminology/items.tsv:24`） |
| `entry-00112` / `entry-00146` | `engine.lua` / `mod-boot.lua` | `扭动者` → **蜿蜒怪人**（`classes.tsv:43`） |
| `entry-00221` | `mod-tome.lua` | `你只能用自己的身体离开地图` → **切换楼层**（`changeLevelCheck`） |
| `entry-00560` | `mod-tome.lua` | brew `药剂` → **佳酿**（保留 brew/elixir 反差） |
| `entry-00579` / `entry-00581` | `mod-tome.lua` | `法师` → **巫师**（专名组） |
| `entry-00647` | `mod-tome.lua` | `终于破碎了` → **爆炸了**（过载引爆，去掉「终于」） |
| `entry-00746` | `mod-tome.lua` | `魔力` → **法力值**（Mana 资源，非 mag 属性） |
| `entry-00984` | `mod-tome.lua` | `那个地方` → **另一个地方**（并恢复复数「力量之地」） |

> **记录更正**：先前 `entry-00111` 的 `scope_note` 称「兄弟串 `engine.lua:1816`／`mod-boot.lua:404`
> 属工作集之外的另一个 revision」。逐字节复核后该说法**不成立**：`嵌件` 的全部 4 处都在
> **同一条 `t()` 字符串内**（`Tinker system` 行与 `Salves` 行），因此本批已一并修复，
> 不需要额外授权。已更正 `CONTEXTUAL-V2-FINDINGS-ALL.json` 与 `PUBLIC-WAVE1-ADJUDICATION.json`。

## 2. 生命周期

| 阶段 | agent | 结果 |
| --- | --- | --- |
| drafter | `7cf29501` | `DRAFTED 11/11`；`FIX-RAW-22.json` |
| executor | `9da1c89b` | `APPLIED 11/11`，无异常 |
| cycle-1 reviewer | `00c97813`（PI-07） | **0 issue**，`DONE_VERIFIED` |

主代理未撰写任何译文。

## 3. 门禁

| 检查 | 结果 |
| --- | --- |
| 逐字节 | `baseline + 11 处替换 == 当前文件`，三文件均 **EXACT MATCH** |
| 占位符／markup／颜色码／换行／`§` | **11/11 通过** |
| `tools/i18n lint --strict` | **30305 条，0 错 0 警** |
| `git diff --check` | clean |
| 运行键扫描 | **桶 B 0 / 桶 C 0** |

## 4. cycle-1 有界复审

`ctx2-fix22-pub-01`（11 修订，`commit:624a6732`，candidate `78e28b6d…`）→ **0 issue**，`DONE_VERIFIED`。
本 cycle 无一级 finding → **收敛**。

## 5. 结论

wave 1–3 与本轮 v2 复审的全部 confirmed（除用户裁定不改的 `restorative`）**均已落盘并收敛**。
未决事项只剩本轮记录的三个族级问题：`Magic` 属性值、`frenzy` 效果名、`undead` 自由文本。

## 补充门禁（2026-09-25）：严格构建

- `tools/i18n build --profile full` → **exit 0**（engine/boot/tome/example/example-realtime 全 OK）。
- `tools/i18n build --profile addon --require-complete` → exit 5，**既有** DLC 层 `baseline-pending`
  （官方 locale／源码未固定），与本批改动无关；core-addon（tome）层 OK。
- 构建产物只写入 `.artifacts/i18n/`，`git status` 保持干净。
