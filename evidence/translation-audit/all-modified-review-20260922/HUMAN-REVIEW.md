# 人工复核清单（持续更新）

以下只转录交叉 REVIEWER 意见，不代表 ORCHESTRATOR 自行裁决或修复授权。

| 条目 | 位置 | Sol 交叉结论 | 人工待决事项 |
| --- | --- | --- | --- |
| entry-01917 | mod-tome.lua:25321 | confirmed：目盲/致盲术语不一致 | Sol 建议改为「致盲免疫」；保留报告供维护者取舍。与上一轮宿主 advisory 不同，本轮不由宿主再裁决。 |

暴击机制、wounds/流血两项被 Sol 判为 refuted，源码证据见 reports/sol-prior-01.md。译文未修改。

## 当前两批交叉结果

下表均为 Sol 的原始分档；主代理仅转录，未作语义裁决。完整源码依据和影响限定见 [第一批报告](reports/sol-001-01.md)、[第二批报告](reports/sol-002-01.md)。

| 条目 | Sol 分档与影响 | 人工待决事项 |
| --- | --- | --- |
| entry-00004 | confirmed：chain 译成「链接」有偏差；固定版本调用已删除，当前运行时无影响 | 是否整理此失效键译文 |
| entry-00039 | confirmed：两处标点问题和额外硬换行，影响轻微；「严重排版断裂」程度仅 advisory | 是否修正标点、整理换行 |
| entry-00041 | confirmed：句号遗漏、十秒确认时间条件表达不准确，低影响 | 是否改为「十秒内未确认」并补句号 |
| entry-00063 | confirmed：角色名后半角空格，同组日志轻微排版不一致 | 是否删除空格 |
| entry-00069 | confirmed：检查当前属性值，译成「属性点不足」可能误导 | 「属性值不足」或「属性不足」的选择 |
| entry-00061 | advisory：快捷键点号删除及全角括号不构成错误 | 可选排版整理，不强制修改 |
| entry-00075 | advisory：相邻文本括号形式不同 | 可选统一中文括号 |

Sol 修正了 Gemini 的一项证据措辞：entry-00069 对照行位于相邻 ActorInventory section，并非同一 section。以上结论无占位符或运行时风险；这一表述同样来自 Sol。累计6个条目含 confirmed 意见，另2个条目仅 advisory；不是缺陷 claim 数。译文均未修改。
