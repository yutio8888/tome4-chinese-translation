# EXECUTOR BRIEFING — SCOPE-20（DLC 语境审核 19 项 confirmed 修复）

你是**唯一的内容写入者**。只执行，不裁决。

## 输入（只读）

`.ai/task/human-review-adjudication-20260923/APPLICATION-SPEC-20.json`

`edits[]` 给出 **14 条**（共 19 个 confirmed 缺陷）的
`file` / `section` / `old_target` / `new_target`（逐字节精确）。
**不得改写 `new_target`**。`text_provenance` 说明这些 target 由
`pi/cliproxyapi/gemini-3.8-flash-high` 拟稿，编排者未撰写任何译文。

## 可编辑面

仅 `tome-orcs.lua`（12 条）与 `tome-possessors.lua`（2 条）中这 14 个位置。

注意：两者都是**受保护 DLC 组件，源码未固定**（`source_pinning: unpinned`）；
`tome-possessors` 源码在本机不可用。

## 任务

对每条，把该 `t(...)` 调用第二个参数从 `old_target` 逐字节替换为 `new_target`。

**定位以 `old_target` 的唯一匹配为准**（已核验每条在各自文件中恰好出现 1 次），
不要按行号盲改。若 `old_target` 出现 0 次或 >1 次，**停止该条**并在报告 `notes` 记录。

特别当心：`entry-03735`、`entry-03852`、`entry-03853`、`entry-03856`、`entry-03861`、
`entry-03865` 是长 lore 串，**必须整体逐字节替换**，包括串首/串尾的空白与 `\n\n` 分段；
`entry-03856` 与 `entry-03853` 的现译串**末尾有尾随空格**，改动后仍须保持原有的
首尾空白与换行布局（`new_target` 已逐字节给出，照抄即可）。

## 硬性禁止

- 不改 `source` / `source_tag` / 占位符 / markup / 颜色码 / 换行 / 首尾空白
  （除 `new_target` 已给出的差异外）。
- 不改这 14 处之外的任何位置或文件。
- 不改 `terminology/**`、`docs/**`、`tools/**`、`.ai/**`、`evidence/**`。
- 不 stage / commit / push。不创建子 agent。

## 报告

写入 `.ai/task/human-review-adjudication-20260923/EXECUTOR-REPORT-20.json`：

```json
{"schema_version":1,"role":"EXECUTOR","phase":"scope-20",
 "applied":[{"entry_id":"entry-XXXXX","file":"tome-orcs.lua","old_target":"...","new_target":"..."}],
 "notes":"异常"}
```

`applied` 必须回写**实际写入**的 old/new。
附 `git diff --stat` 的实际输出。
最后回复：`APPLIED 14/14`。
