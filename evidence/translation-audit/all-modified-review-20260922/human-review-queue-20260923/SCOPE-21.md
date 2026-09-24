# SCOPE-21 报告：public 19 项 confirmed 修复 + cycle-1 复审

task_id: `human-review-adjudication-20260923`
phase: `scope-21`（v2 public 复审裁决 confirmed 项的修复）
日期: 2026-09-24
baseline: `6bbd2e3e`
drafter: `pi/cpa/gemini-3.8-flash-high`（agent `451814a2`，high）
executor: `codex/gpt-6-sol`（agent `a66e6c98`，medium）

## 1. 范围

`ADJUDICATION-v2-PUBLIC.json` 中 **19 条 confirmed**（18 条 public + 1 条 DLC 修复后复审）。

- 已排除：`restorative`（用户裁定不改）、`Magic` 属性值（deferred）、`frenzy` 效果名（advisory/deferred）、
  以及 19 条 advisory。
- 主代理**未撰写任何译文**：`new_target` 全部由 Gemini 拟稿。

## 2. 拟稿与落盘

| 阶段 | 产物 | 结果 |
| --- | --- | --- |
| 拟稿输入 | `FIX-REQUEST-21.json` | 19 条，含 source/current_target/what_must_change/invariants；每条 source、target 在文件中均唯一匹配 |
| 拟稿输出 | `FIX-RAW-21.json` | 19/19；`author=pi/cpa/gemini-3.8-flash-high` |
| 落盘 spec | `APPLICATION-SPEC-21.json` | 19 条 old/new |
| 落盘报告 | `EXECUTOR-REPORT-21.json` | `APPLIED 19/19`，无异常 |

落盘位置：`mod-tome.lua` 18 处、`tome-orcs.lua` 1 处。

**逐字节验证**：`baseline + 19 处替换 == 当前文件`（两文件均 **EXACT MATCH**），
即除这 19 处外没有任何额外改动。

## 3. 门禁

| 检查 | 结果 |
| --- | --- |
| 占位符 / markup / 颜色码 / 换行 不变量 | **19/19 通过**（placeholders、markup、`\n` 计数全等） |
| `tools/i18n lint --strict` | **30305 条，0 错 0 警** |
| `git diff --check` | clean |
| 运行键扫描 `classify_runtime_keys.py` | 1711 重复键，**桶 A 1711 / 桶 B 0 / 桶 C 0**（无新增同 section 冲突） |
| 术语审计 `audit_static` / `audit_dynamic` | 与既有基线一致（既有 S1.1 Aeryn、Air mismatch，与本批无关） |
| 术语键族一致性 | `stun→震慑`(4)、`ice→寒冰`(10)、`darkness→暗影`(9)、`wound→创伤`(3)、`inscriptions→刻印`(2)、`construct→构装体`(5) 结构术语保持统一 |

> `tools/i18n proposal --strict` 不适用：工具链 workset 以 `stable_entry_id`（sha256）为键，
> 本任务以 `entry-NNNNN` 为键，命名空间不兼容，无法构造对应 workset；
> 已改用等价的严格检查（不变量 parity + 落盘后 `lint --strict`）。

## 4. cycle-1 有界复审

修复后按 `translation_contextual_v2` 重建候选并复审（拆 public/DLC 两条以满足单一 `fixed_source_identity`）：

| task | 修订 | candidate_identity | issue |
| --- | --- | --- | --- |
| `ctx2-fix21-pub-01` | 18 | `5cc21598…` | **0** |
| `ctx2-fix21-dlc-01` | 1 | `cb857acd…` | **0** |

两条均 `DONE_VERIFIED`。本 cycle 无一级 confirmed finding → **本批收敛**，不再开新修复轮。

## 5. 本批不改（记录在案）

- `entry-01625` / `entry-01605` 的 **Magic 属性值**：deferred（族级决定）。
- `entry-01976` 的 **frenzy 效果名**：advisory（族级决定）。
- `entry-01256` 的 **undead 自由文本**：advisory（官方自由文本本身混用）。
- 17 条 advisory 其余项：见 `ADJUDICATION-v2-PUBLIC.md`。

## 6. 生命周期

- drafter `451814a2`、executor `a66e6c98`、reviewer `214ff7f9`（pub）、`4a7ab6f0`（dlc）均已结束；
  reviewer 已 `archive`；其余为一次性运行，无 live child。
