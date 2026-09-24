# 复审 Prompt 与流程审计（2026-09-24）

审计对象：`ctx-public-20260924`（497 修订）与 `ctx-dlc-20260924`（89 修订）两条 contextual
复审 run 的派发 prompt、流程约束与输出格式要求。

## 结论

**Prompt 正确；流程有两处缺陷**，其中缺陷 A 直接导致 public run 不可能完成。

## 一、Prompt 审计：**通过**

| 检查项 | 结果 |
| --- | --- |
| 与契约 §4 模板一致 | ✅ 4 个 prompt 文件实例化后**逐字节一致** |
| 未实例化模板 ≤ 800 字节 | ✅ 656 字节 |
| 实例化 prompt ≤ 800 字节 | ✅ 793 / 790 字节 |
| 完整投递三行 | ✅ raw log `[User]` 段含全部三行 |
| 流程约束告知 | ✅ 「全程只读，禁止写入任何文件；只读该文件及其所引译文/公开源码、`docs/paseo-translation-context-review-v1-contract.md` 第六节，不读其他 `.ai/task`/`.ai/reviews`」 |
| 输出格式告知 | ✅ 「仅回第六节单一紧凑 JSON；按 envelope 冻结顺序全量覆盖并回显 `<candidate_identity>`；首字节 `{`、末字节 `}`，无其他文字、Markdown/围栏」 |
| agent 是否读契约 §6 | ✅ 两条 run 的 raw log 均出现该文件与「第六节」 |

**Prompt 侧无需修改。**

## 二、缺陷 A：契约选型 —— v1 无法承载该规模

v1 契约 §6 的 result schema **要求每条 revision 回显冻结字节**：

```json
{"revision_key":"…","observation":"OK","evidence":{"source":"<冻结 source 原样>","target":"<冻结 target 原样>"}}
```

并规定第 7 条：「evidence 的 source／target 必须与冻结字节精确一致」。

对 **public run 497 条**，仅「回显」一项就需约 **440 KB（≈128 K tokens）** 输出，
**超出任何模型的单次输出上限** → 该任务在物理上不可能产出合规记录。

对照 v2 契约 §6 的唯一结果形状：

```json
{"contract":"translation_contextual_v2","candidate_identity":"<64 hex>","verdicts":[{"revision_key":"r1","verdict":"OK"},{"revision_key":"r2","verdict":"ISSUE","observation":"…"}]}
```

**不回显 source/target**，输出量可小两个数量级。

**生产流程实际使用 v2**：已核验 `evidence/quality/production-batches/batch-04a55612…-host-review/contextual/`
的记录 `review_contract = translation_contextual_v2`。

## 三、缺陷 B：工作集规模未按惯例限界

生产导出工具 `tools/i18n review` 的边界：

- `--batch-size`：translation v2 上限 **10**
- `--character-budget`：默认 **24000**

已核验真实生产 contextual envelope：**9 修订 / 37 KB**。

本次拆分（497 / 89）远超该惯例。即便按 v2 四 lane 平摊，public 每 lane 仍约 124 条。

## 四、次要观察

- **载体内容过滤**：public `full-01` 被 **Gemini 自身安全过滤器**在中途拦停
  （`"This request was blocked by Gemini's filters"`，lore 文本触发），未产出终结 JSON。
  载体选择因此不是无关变量。
- **长串转录漂移**：两条 Gemini run 都在长 lore 串的 `evidence` 上出现首尾空白差异
  （DLC `full-01` 2 条、`full-02` 3 条），另有 1 条缺失结尾 `\n`。
  v1 强制回显长串本身就是易错设计；v2 不回显即规避。
- **Claude 载体未遵格式**：public `full-02`（Opus 5.5）返回散文分析 + **未闭合 JSON 片段**，
  同样不构成合规记录（即便 prompt 已明确要求）。

## 五、影响与建议

**影响**：两条 run 都不会产出合规记录，因此父任务的 `translation_contextual_v1` 复审
无法以当前形态闭合。DLC run 报出的 4 项缺陷结论**仍然有效**（ORCHESTRATOR 已逐条独立核实）。

**建议**：

1. 复审改用 **`translation_contextual_v2`**（`schema_version >= 5`），获得不回显的紧凑 schema；
2. 按 **≤10 修订 / ≤24000 字符**切分 bundle，每 bundle 一个任务；`n >= 4` 时用四 lane；
3. DLC 的 4 项 confirmed finding 先进入修复；
4. 派发前对每个 lane 保留现成的硬断言（identity 长度、input_path 非空、prompt ≤800 字节）。

## 附：DLC run 的 4 项 confirmed finding

| entry | 位置 | 问题 | 权威依据 |
| --- | --- | --- | --- |
| `entry-03853` | `tome-orcs.lua:2545` | `马基埃亚尔` 缺间隔号 | `terminology/places.tsv:46` preferred |
| `entry-03856` | `tome-orcs.lua:2625` | `探险远行传送门` | `terminology/items.tsv:37` preferred |
| `entry-04088` | `tome-orcs.lua:7455-7456` | `The light of the Amulet` → 「神的光辉」 | fidelity：Amulet=护符 |
| `entry-04092` | `tome-orcs.lua:7901` | `temporal` 伤害类型 → 「时间」 | `terminology/combat.tsv:12` temporal=时空 |
