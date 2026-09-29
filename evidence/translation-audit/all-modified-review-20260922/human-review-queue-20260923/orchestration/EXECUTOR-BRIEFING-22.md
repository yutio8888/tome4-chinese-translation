# EXECUTOR BRIEFING — SCOPE-22（wave 1–3 confirmed 修复）

你是**唯一的内容写入者**。只执行，不裁决。

## 输入（只读）

`.ai/task/human-review-adjudication-20260923/APPLICATION-SPEC-22.json`

`edits[]` 给出 **11 条**的 `file` / `section` / `old_target` / `new_target`（逐字节精确）。
**不得改写 `new_target`**。`text_provenance` 说明这些 target 由
`pi/cpa/gemini-3.8-flash-high` 拟稿，编排者未撰写任何译文。

## 可编辑面

仅 `mod-tome.lua`（7 条）、`engine.lua`（2 条）、`mod-boot.lua`（2 条）中这 11 个位置。

## 任务

对每条，把该 `t(...)` 调用第二个参数从 `old_target` 逐字节替换为 `new_target`。

**定位以 `old_target` 的唯一匹配为准**（已核验每条在各自文件中恰好出现 1 次），
不要按行号盲改。若 `old_target` 出现 0 次或 >1 次，**停止该条**并在报告 `notes` 记录。

特别当心：`entry-00111`/`entry-00145`/`entry-00112`/`entry-00146`/`entry-00984` 是长串，
**必须整体逐字节替换**，包括串首/串尾空白、`\n` 分段与 `§` 分隔符。

## 硬性禁止

- 不改 `source` / `source_tag` / 占位符 / markup / 颜色码 / 换行 / `§` / 首尾空白
  （除 `new_target` 已给出的差异外）。
- 不改这 11 处之外的任何位置或文件。
- 不改 `terminology/**`、`docs/**`、`tools/**`、`.ai/**`、`evidence/**`。
- 不 stage / commit / push。不创建子 agent。

## 报告

写入 `.ai/task/human-review-adjudication-20260923/EXECUTOR-REPORT-22.json`：

```json
{"schema_version":1,"role":"EXECUTOR","phase":"scope-22",
 "applied":[{"entry_id":"entry-XXXXX","file":"mod-tome.lua","old_target":"...","new_target":"..."}],
 "notes":"异常"}
```

`applied` 必须回写**实际写入**的 old/new。
附 `git diff --stat` 的实际输出。
最后回复：`APPLIED 11/11`。
