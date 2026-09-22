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

## 003/004 交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未改译文。完整 claim 见 [sol-003-004-01.md](reports/sol-003-004-01.md)。004 与 003 是同一组 boot 文本的另一载体，Sol 仍逐项给了结论。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00090 / entry-00124 | confirmed：结句“玩的开心”应为“玩得开心” | 是否修改这处语病 |
| entry-00092 / entry-00126 | confirmed： “这种情况不被支持的”语病；占位符与颜色码正确 | 是否改写句法 |
| entry-00094 / entry-00128 | pending：donator“赞助者/捐赠者”无法用允许输入裁定；00094 的句号位置 claim 为 refuted，列表标点不统一仅 advisory | 核对术语记录适用范围；是否统一列表标点 |
| entry-00102 / entry-00136 | confirmed：boot Flame 是 bolt 火焰攻击；refuted：并非必须改成“火球术”，也不是与主游戏完全同一机制；pending：术语表是否仍写“火球术” | 核对术语记录；不要仅凭名称改译文 |
| entry-00105 | confirmed：首行缺句号；pending：捐助者/捐赠者 | 是否补句号；核对术语 |
| entry-00139 | pending：捐助者；advisory：“角色备份”缩窄了 vault，但后文补出了用途 | 是否改服务名；核对 Donator |
| entry-00110 / entry-00144 | confirmed：写成“马基埃亚尔”，与同批“马基·埃亚尔”不一致；pending：项目 preferred 不能在允许输入内独立核验。来源未固定的 Ashes 简中本地化本身无间隔号 | 确认项目标准后再决定是否统一 |
| entry-00111 / entry-00145 | confirmed：出现“西方灾星”；refuted：DLC 并未统一为“西方天灾”或全篇“灵能射手”；pending：项目 canonical | 以项目术语为准，不以 Gemini 所称 DLC 一致性为准 |
| entry-00112 / entry-00146 | refuted：“蠕动者”“天灾之穴”指认；冻结 Cults 简中是“苦痛者”“瘟疫之穴”。confirmed：Nethergames 是 Nethergate 笔误，以及半角括号。pending：扭动者/蜿蜒怪人/苦痛者，以及“彼世之门”还是“虚空之门” | 裁定 Writhing One 与 nethergate 的正式译名；不要按本次 Gemini claim 改“瘟疫之穴” |

Sol 写明：确定成立的是两处重复语病、FirstRun 首行标点、半角括号，以及间隔号专名的批内不一致。译文未修改。

## batch-005 前三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-partial-01.md](reports/sol-005-partial-01.md)。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00164 | confirmed：颜色码和两个 `%s` 顺序正确；confirmed：中文句中无空格半角分号。建议改成全角分号或逗号仅为 advisory | 是否把半角分号当作需要修正的格式问题；若改，在 `；` 与 `，` 之间选择 |
| entry-00165 | confirmed：颜色码与占位符顺序、半角分号。pending：“技能树”是否为正式译法。改全角标点仅为 advisory | 用项目术语决定保留“技能树”或改用“技能类别”等；半角分号是否统一 |
| entry-00166 | confirmed：颜色码、占位符顺序、半角分号。改全角标点仅为 advisory | 是否统一成全角标点 |

Sol 的综合结论：半角分号的事实成立，但提升为必须修复只算 advisory；“技能树”是否可接受仍是 pending。译文未修改。
