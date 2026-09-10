# Facts 因果研究 v1 与语言质量通道边界

`facts-study-v1` 是独立研究 lineage，不是 evaluator v4，也不修改 v1–v3 artifact 的历史含义。它只回答：Facts、穷尽 checklist、token 负载、信息位置以及独立 Facts 核验分别如何改变模型的检出、误报和人工负荷。

## 冻结边界

- 研究集固定为全新 20 条、一 shard；不得与既有 calibration、holdout、正式 120 条或历史 Facts 实验 revision 相交。
- `facts-study-build` 只生成候选 sample、target-blind `facts-author-bundle.json`、空 Facts authoring packet 和 draft gold。Facts 作者只接收该 bundle；draft 不能生成 evaluator bundle 或 preregistration。
- `facts-study-bundles` 只有在两名不同审校者的 review 摘要、独立裁决摘要、8+8 claim 覆盖、5 个 clean 和 3 个 fact-trap 全部满足时才成功。
- Facts 作者不得读取 target 缺陷或 gold finding。该角色分离属于人工流程；工具通过 frozen lineage 和摘要绑定防止完成后替换。
- 所有 bundle 都不含 gold、anchors、risk flags、gate signals 或既有 assessment。A/B 没有 supplemental packet；N 只含逐 item 与 Facts canonical JSON 字节等长、同形状的 neutral packet；F 在全新会话中只做 Facts 核验。
- Facts 的 `fact_id` 必须采用 `fact-` 加 16 位小写十六进制。neutral packet 不复用作者 ID，而由宿主按冻结顺序生成同长度、无语义的序号 ID，避免十六进制或描述性编码泄露事实内容。
- T 不是模型 arm；它是宿主对同一 evaluator、同一 replicate 的 B 与 F assessment 做对称一对一对齐、去重后的并集。

## 外部执行

`tools/pi-quality-facts-study` 一次只执行 preregistration 中的一个 slot。runner 在发起前用 `--sample`、`--facts`、`--neutral`、`--gold` 和七个 `--bundle` 从当前协议完整重建 preregistration；preregistration 同时绑定全部本地 `i18nlib` 代码、runner 入口和解析器、完整 Pi npm 包树，以及 Node 可执行文件和安装树。gold 仅由宿主校验，不进入模型命令。缓存始终关闭；slot 在发起进程前写入不可替换 ledger，因此 provider、连接、结构或内容失败都会消耗该 slot。每个后续 slot 在发起前必须与已消费 slot 使用同一个授权摘要，避免在 campaign 结束后才发现授权 lineage 混用。runner 要求新的 `--authorization-id`，但该参数只记录授权 lineage，不能替代发起前向用户明确报告 provider、model、thinking、20 条、arms、三轮、一 shard 和最多 33 次传输。

外部汇总时，`facts-study-validate` 必须同时接收 33 份 assessment 和 33 份 runner report，并重新核对 campaign ledger、唯一 execution ID、同一授权摘要、assessment/report 字节摘要和完整 slot 身份。`--fake-runner` 生成的报告固定标记为 `non-evidentiary-offline-replay`，永远不能产生通道 promotion 决策。

当前 Pi/provider 接口不暴露可验证的 sampler seed。预注册 seed 作为每个请求唯一且冻结的 nonce 写入请求和 runner report，用于重算顺序与请求身份；报告不得把它描述成 provider 端可复现采样。

研究报告固定 `holdout_clearance=false`，不解封 v4 holdout 或正式集。

## 语言质量通道

本轮只冻结 [language-channel-v1.json](../i18n/quality/language-channel-v1.json) 的数据边界，不提供 runner，也不进行外部调用。该通道只判断自然度、搭配、语体、语法与中文可读性；不得看到 Facts、机制、risk/gate signals 或 semantic/Facts assessment。其 taxonomy、gold、稳定性门禁、人工路由和外部授权均为独立 lineage，结果不并入 semantic severity。
