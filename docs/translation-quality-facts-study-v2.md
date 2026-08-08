# Facts 因果研究 v2：supplemental-only 数据契约

`facts-study-v2` 修订数据契约，不改变已完成但未准入的 v1 pilot artifact。v1 pilot 的 20 条 revision 已登记到 `i18n/quality/facts-study-exclusions-v1.json`，后续 `facts-study-build` 会自动排除。

## 修订原因

v1 pilot 的 49 条 Facts 中有 15 条只是公共英文 source 的释义。裁决后的 16 个 gold claims 中，12 个引用了 Fact，但其中 11 个只引用 source 重述，只有 1 个得到真正新增的源码或规范信息支持。因此旧的 `fact-addressed` 分层没有测量 supplemental Facts 的增量作用。

## Fact packet v2

- contract 为 `tome4-quality-fact-packet-v2`，并声明 `supplemental_only=true`。
- 每项允许 `0–4` 条 Fact。没有真实补充信息时必须留空，不得为了保持形状而重述 source。
- Facts 作者仍然只能看到 target-blind author bundle；lineage 必须声明 `common_input_restatements_excluded=true`。
- Fact 不得从模型公共输入中的 source、source context、item kind 或 source tag 直接推出。
- provenance 只允许：
  - `terminology`：版本化规范术语；
  - `public-source`：固定公开源码中的机制或 UI 契约；
  - `versioned-context`：未出现在公共 bounded context 中、但已固定版本和摘要的外部上下文。
- provenance 不得指向 `facts-author-bundle` 或 `sample.json`。宿主可以校验结构和 lineage；“是否只是同义改写”仍需作者与冻结审查者共同确认。

Facts author bundle 升级为 `tome4-quality-facts-author-bundle-v2`，直接携带上述 policy。neutral packet 允许空 facts 数组；非空条目仍逐 item 保持 canonical JSON 同形状、等字节，且由宿主替换 Fact ID。

## 指标语义

只有 claim 引用了同条目、直接支持该 claim 的 v2 supplemental Fact，才计为 `fact-addressed`。其余 claim 均为 `fact-unaddressed`。公共 source 的字面或释义证据只能支撑 gold claim 本身，不能把它归入 fact-addressed。

8 addressed、8 unaddressed、5 clean、3 fact-trap 的冻结门槛保持不变。若真实裁决不满足门槛，必须废弃该候选集并重新选样，不能修改 Facts 或补造 claim。

## 版本与执行

- v1 protocol、schema 和失败 pilot 保留原义；最新命令加载 `i18n/quality/facts-study-v2.json`。
- sample、gold、bundle、assessment 和 report 的结构未变；packet contract 和 author bundle contract 通过 artifact hash 与 preregistration 进入完整 lineage。
- v2 真实 Gold 冻结并通过 33-slot fake replay 前，不得申请外部传输授权。
