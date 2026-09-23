# 三模型复核试验入口

本目录是在原译文审核 campaign 旁增加的有界研究分支，样本固定为 batch-095 的 40 条。它不恢复旧 campaign，也不修改译文、术语或生产状态。

- [40 条最终结果](RESULT.md)：正确率、精确率、召回率及资格限制；[机械指标](METRICS.json)可复算。
- [实际 prompt 审计](PROMPT-AUDIT.md)：为什么 v1 仅作协议预试验，以及 v2 统一了哪些约束。
- [v2 协议](protocol-v2/PROTOCOL.md)与[冻结输入](protocol-v2/INPUT.md)：三个模型收到同样的 40 条、源码、上下文和分类规则。
- [派发一致性凭证](protocol-v2/DISPATCH-VERIFICATION.json)：相同 prompt/input 哈希及实际模型配置。
- [用户临时文件授权](TEMP-FILE-AUTHORIZATION.md)：后续实验可使用任务专属临时文件，仓库和冻结输入仍只读。
- [独立参考流程](REFERENCE-PLAN.md)：先全量盲审，再匿名逐 claim 核验；结论是暂定参考，不是人工金标准。
- [运行与归档记录](STATE.json)、[恢复交接](HANDOFF.md)、[协议偏离](PROTOCOL-DEVIATIONS.md)：保留所有初次运行和重试，不择优挑报告。
- [机械计分程序](score.py)：填写可追溯的 SCORING.json 后，执行 `python3 -B score.py SCORING.json`。程序不裁决译文语义。

后续试验需要另建目录和冻结版本；不得覆盖本目录历史输入。将临时文件许可写入三组共同 prompt，在派发前冻结；样本、输入顺序、提示词和检错门槛一致，实际提供方/档位与流程偏离分别记录。原始四类判定、待确认 claim 和最终参考裁决必须分开保存，不能事后把未确认疑点改算成正确检出。

本次授权止于这 40 条试验，不自动扩大样本或继续生产审核。
