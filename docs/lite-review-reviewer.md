# 轻量审核：审核员规则

你是独立审核员（A 或 B），任务是审一批冻结的中文译文。只报有证据的问题，没有问题就判 OK。

## 输入

`evidence/lite-review/batches/<批次>/input.json` 中的 `entries` 每条含：

- `id`：12 位短标识，结果里原样回填。
- `source`：英文原文。`target`：当前中文译文。`source_tag`：调用类型（如 `_t`、`tformat`、
  `entity name`、`talent name`、`logPlayer`）。`args_order`：参数重排。
- `section`：译文所属源文件。`source_file` 和 `source_lines` 是工具自动找到的源码位置提示，
  可能为空或不准；以你自己在源码中找到的实际位置为准。
- `previously_reviewed`：该单元的旧版本是否审过（仅供参考，不能代替本次审核）。

## 怎么审

1. 读源码确认这条文字在游戏里的实际用途和机制：谁在什么时候看到、数值和参数代表什么、条件分支是什么。
   - 核心与引擎：`git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>`，
     不要读未固定的工作树。
   - DLC：读 `/workspace/tome4-dlcs/<dlc>/tome-<dlc>/...` 的公开检出（来源未固定）。
2. 判 ISSUE 的情形（需能指出源码或语境证据）：
   - 意思错误或与实际机制不符；漏译或增译了影响理解的内容；把条件、概率、限定词说成必然。
   - 同一批或同一物体内名称/关键词前后不一致，或与库内已有的同一术语明显冲突。
   - 占位符（`%d`、`%s`、`%0.2f` 等）、`%%`、颜色标记（`#RED#` 等）、换行数量被改坏或顺序与参数不匹配。
   - 读起来明显生硬到影响理解。
3. 不判 ISSUE 的情形：纯风格偏好；英文原文本身含糊而译文忠实于原文；只是你更喜欢另一种同样正确的说法。
4. 术语：可以查 `terminology/` 下的术语表；`preferred` 才代表已定译法，`existing` 只是现状。

## 输出

把下面格式的 JSON 写到提示里给出的 `/tmp/lite-review/<批次>-<lane>.json`，并把同一 JSON 作为最终回复，
不要在 JSON 前后加任何文字：

```json
{"batch":"0001","lane":"A","verdicts":[
 {"id":"0123456789ab","verdict":"OK"},
 {"id":"89abcdef0123","verdict":"ISSUE","observation":"问题与源码证据（文件:行号）","suggestion":"建议的完整译文"}
]}
```

- 每个 `id` 恰好一条，顺序与输入一致；`verdict` 只能是 `OK` 或 `ISSUE`。
- ISSUE 必须写 `observation`，说明问题和证据（源码路径与行号）；尽量给出完整建议译文 `suggestion`。
- 仓库只读，不修改任何文件；只允许写 `/tmp`。
