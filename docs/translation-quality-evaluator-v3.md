# 翻译质量 AI Evaluator v3：可观察差异与确定性定级

v3 与 v2 平行存在，方法版本为 `mqm-pilot-v3`。它不重解释历史 v1/v2
artifact，也不改变正式 120 条 revision。

模型逐条输出 `revision_id`、`assessment_state` 和 `findings`。finding 只包含
error code、phenomenon、meaning change、原译文证据与解释；模型不再填写
severity、defect class、impact facts、anchor、传播范围、profile 或复用建议。
其中 `meaning_change` 是从 bundle 的 `meaning_change_types` 选择的标量字符串，
不是带摘要的对象；解释统一写在 `explanation`。
纯流畅度/样式、技术结构、catalog、source、机制源码结论仍由宿主门禁、源码核验
或人工处理。

宿主按固定优先级处理：运行损坏为 blocker，单条显示损坏为 major；校准集内同
revision 且规范化证据范围完全一致的人工 anchor 优先；数值、范围、条件、极性、
对象、作用域和触发时机的明确语义变化为 major；单位标签遗漏、术语/专名、普通
遗漏/增译/歧义和其他实质错误为 minor。单位的非遗漏语义改变为 major。

`unknown`、`other`、模糊或缺失证据、上下文不足，以及双 evaluator 跨越
major/minor 边界时，一律派生 `minor + provisional + requires_adjudication`，并输出
稳定 reason code；不再使用 `needs-adjudication` severity。错误码、phenomenon 和
meaning change 不兼容时严格拒绝，不进入人工队列。

校准和封存数据沿用 v2 的 32+32 revision 选择与 shard 顺序，但以 v3 policy 和
schema 重新计算 sample identity。稳定性同时报告 raw-model 与 anchor-normalized
指标，以保留漏检和负 anchor 拒绝的可见性。固定 shard 大小为 20，因此 32 条样本
恒为 2 shards。校准运行必须提供冻结的 preregistration 和 `--run-number {1,2}`，并
禁用缓存。宿主在忽略目录中按 preregistration identity 维护原子 campaign ledger：
两 evaluator × 两轮 × 两 shard 共 8 个一次性传输槽；发送前占用，连接或内容失败
也永久消耗，不重试、不替换。一个 assessment 的所有 shard 完成后才进行整体严格
校验；任一 shard 或合并后的 assessment 无效时，本次已占用槽全部标记失败，只有整体
通过时才一起标记成功。preregistration 冻结每位 evaluator 的两个 bundle ID 与完整
bundle hash；ledger 逐槽绑定 round、execution、shard index 和实际 bundle ID。
runner report 绑定这些 shard 状态和规范语义摘要。

holdout 运行必须提供同一 preregistration，以及 reviewer-a、reviewer-b 各一份严格
验证且 `passed=true` 的 stability-v3 report。`stability-v3` 只将通过报告 ID 原子登记到同一
campaign ledger，失败报告不登记，既有 evaluator 登记不得替换；holdout 还要求 ledger 中 8 个传输槽
全部成功，且传入的两个报告 ID 与登记值逐项一致。宿主在调用 provider 前完成这些
验证。holdout 缓存身份额外绑定 preregistration 和两份 clearance report。模型
finding 仍保留在 raw/normalized 指标中，但存在 host gate 时最终 issue 集只包含一个
宿主 technical gate issue。

`report-v3` 显式记录所用 `adjudication_validation_id`（无裁决时为 `null`）；宿主读取时
用 match 与对应裁决重新构建完整报告，不能仅凭可重算的 `report_id` 接受汇总指标。

离线流程：

```bash
python3 -B tools/i18n quality calibration-v3 --inventory <inventory.jsonl>
python3 -B tools/i18n quality evaluator-bundles-v3 --sample <calibration.json> --evaluator reviewer-a
tools/pi-quality-evaluator --sample <calibration.json> --evaluator reviewer-a --no-cache \
  --preregistration i18n/quality/stability-preregistration-v2.json --run-number 1
python3 -B tools/i18n quality match-v3 --sample <calibration.json> --assessment <a.json> --assessment <b.json>
python3 -B tools/i18n quality report-v3 --match <issue-match.json>
```

外部校准仍须在首次发送 v3 bundle 前报告 provider、model、32 条和 2 shards 并取得
授权；校准通过前不得运行重新绑定的封存集。
