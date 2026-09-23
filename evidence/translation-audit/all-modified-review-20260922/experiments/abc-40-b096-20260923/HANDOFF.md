# batch-096 实验最终交接

本次40条续轮已完成，入口为 [RESULT.md](RESULT.md)，问题清单为 [MERGED-FINDINGS.md](MERGED-FINDINGS.md)。研究状态DONE，不是生产DONE_VERIFIED。

- 样本为未复核batch-096，entry-03212–03251，与上一轮不重复；三臂同prompt/input，临时文件统一允许。
- Opus5.5、GPT-6 Sol、AGY Gemini3.8 Flash均High，40/40覆盖且均可计分；本轮无重跑。
- 三臂28项观察+独立盲审8项观察，匿名36项逐项核验并全量检查40条。暂定参考：7条ISSUE、8个缺陷、无剩余pending，非人工金标准。裁决者Astra与参赛Sol同系列偏差已披露。
- 全40条正确数为Opus38、Sol36、Gemini35。Sol原待确认03236不算正确；共同明确判定集39条的正确数为37、36、34。原待确认已解除，不算误报，不追认明确判断。
- 8项确认缺陷的三臂并集均已命中；5项相对英文偏差、3项沿袭上游。误报、建议、mixed被否决部分和模型来源保留在归并清单。
- 5个child已live archivedAt确认归档，无活动child。此前旧campaign的两个未闭合child未接管。
- 译文、术语、旧campaign状态、上一轮实验和HEAD均未改；没有生产覆盖更新、提交或push。

复算：build_scoring.py -> score.py SCORING.json；render_findings.py生成清单；record.py guards核对冻结与基线。原始输出和活动在reports/及raw/，匿名来源映射为ANON-MAPPING-HOST-ONLY.json。没有必须继续的本轮工作；此交接不自行扩大为全库实验或译文修复。
