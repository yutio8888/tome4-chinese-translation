# EXECUTOR BRIEFING — SCOPE-21（public 19 项 confirmed 修复）

你是**唯一的内容写入者**。只执行，不裁决。

## 输入（只读）

`.ai/task/human-review-adjudication-20260923/APPLICATION-SPEC-21.json`

`edits[]` 给出 **19 条**的 `file` / `section` / `old_target` / `new_target`（逐字节精确）。
**不得改写 `new_target`**。`text_provenance` 说明这些 target 由
`pi/cpa/gemini-3.8-flash-high` 拟稿，编排者未撰写任何译文。

## 可编辑面

仅 `mod-tome.lua`（18 条）与 `tome-orcs.lua`（1 条）中这 19 个位置。

注意：`tome-orcs.lua` 是**受保护 DLC 组件，源码未固定**（`source_pinning: unpinned`）。

## 任务

对每条，把该 `t(...)` 调用第二个参数从 `old_target` 逐字节替换为 `new_target`。

**定位以 `old_target` 的唯一匹配为准**（已核验每条在各自文件中恰好出现 1 次），
不要按行号盲改。若 `old_target` 出现 0 次或 >1 次，**停止该条**并在报告 `notes` 记录。

特别当心：`entry-01221`、`entry-01223`、`entry-01228`、`entry-01282`、`entry-01302`、
`entry-01308`、`mod-tome.lua:14630`、`entry-03856` 是长 lore 串，**必须整体逐字节替换**，
包括串首/串尾空白与 `\n\n` 分段。

## 硬性禁止

- 不改 `source` / `source_tag` / 占位符 / markup / 颜色码 / 换行 / 首尾空白
  （除 `new_target` 已给出的差异外）。
- 不改这 19 处之外的任何位置或文件。
- 不改 `terminology/**`、`docs/**`、`tools/**`、`.ai/**`、`evidence/**`。
- 不 stage / commit / push。不创建子 agent。

## 报告

写入 `.ai/task/human-review-adjudication-20260923/EXECUTOR-REPORT-21.json`：

```json
{"schema_version":1,"role":"EXECUTOR","phase":"scope-21",
 "applied":[{"entry_id":"entry-XXXXX","file":"mod-tome.lua","old_target":"...","new_target":"..."}],
 "notes":"异常"}
```

`applied` 必须回写**实际写入**的 old/new。
附 `git diff --stat` 的实际输出。
最后回复：`APPLIED 19/19`。
