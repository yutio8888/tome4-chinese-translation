# 宿主辅助件模板

这些文件是第 275 批（`batch-54d2d16b94c511082107`）实际使用的宿主辅助件，未随批次证据归档，
所以存放在这里作为模板。用法见 [审核操作指南](../../review-operations-guide.md) 第三、四节。

使用前复制到 `.artifacts/i18n/continuation-20260923/`（或新的宿主目录），并把其中的批号 `275`、
batch id `batch-54d2d16b94c511082107` 与 `captures275` 等路径换成当前批次；替换要带数字边界，
替换后逐个 diff。

| 文件 | 用途 |
| --- | --- |
| `laneN.py` | `precheck <i>`：比对 codex native log 最终 JSON 的 20 个 identity 与 envelope，列出 ISSUE |
| `mkliveN.py` | 用首次 `get_agent_status` 观测值构造 surface lane 的 live 捕获 |
| `mktermN.py` | 由 live 捕获构造 idle/finished 终态捕获 |
| `mkarch.py` | 由终态捕获构造 closed/archived 捕获（原名 `mkarch257.py`，不随批号变） |
| `harvest-lane.sh` | `h <i> <updatedAt> <lastUserMessageAt> <attentionTimestamp> <sessionId>`：终态捕获 → precheck → harvest → archive-intent |
| `closeN.sh` | evidence 提交 → finalize → 回执 → handoff 更新 → closure 提交 → queue rebuild → push |
| `handoff-update.py` | closeN.sh 调用的 handoff 编辑脚本（每批改写正文） |
| `evidence-commit-message.txt`、`closure-commit-message.txt` | 两个提交说明模板 |

`closeN.sh` 通过 `/tmp/eN.txt`、`/tmp/cN.txt`、`/tmp/hN.py`、`/tmp/evidN` 引用这些文件；照搬时一并改名或改路径。
提交说明末尾保留 `Co-Authored-By` 行。
