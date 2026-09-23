# ABC40 实验最终交接

40 条有界试验已完成，入口为 [RESULT.md](RESULT.md)。本实验 state=DONE 是研究交付状态，不是生产 DONE_VERIFIED。

- 样本固定 entry-03172–03211；v1 仅协议预试验，正式口径来自统一 v2。三臂首轮收到同一 prompt/input。
- 内容正确率：Opus 38/40（诊断）、Sol 34/40（合规）、Gemini 36/40（合规）。Opus 两次 v2 使用当时禁止的临时文件，故没有合规主结果；诊断固定首份，不择优。
- Gemini CPA 两次失败后 AGY 成功；连接故障与内容错误分开。
- 参考由独立 Astra 全40盲审后匿名裁决52条观察建立，非人工金标准。7条 ISSUE、13个确认缺陷；P01“transitions／渐变”仍待确认，不改变已有 D09 的03206条目判定。
- 宿主仅机械映射。SCORING-DRAFT 保留原始判定；SCORING 保存映射；REFERENCE 保存裁决；METRICS 可由 build_scoring.py 和 score.py 复算。原待确认/建议不得事后算作明确检出。
- 用户已授权后续临时文件，见 TEMP-FILE-AUTHORIZATION.md；未来实验共同 prompt 应显式写入。旧记录不追改。
- 本实验12个 child 全部 live archivedAt 确认归档，STATE无活动child。不接管 BASELINE 中两个旧campaign未闭合child。
- 译文、术语、旧campaign STATE和HEAD未变；用户已有改动保留；未提交、push或恢复生产审核。

当前没有必须继续的实验工作。若另获扩大实验授权，应新建目录、统一临时文件许可、抽取独立样本并保持所有臂同输入；不要覆盖本轮证据。P01或其他边界可供后续人工核验，不因本交接自动启动新一轮。
