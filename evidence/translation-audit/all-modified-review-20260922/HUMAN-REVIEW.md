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

## batch-005 其余五条交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-005-rest-01.md](reports/sol-005-rest-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00184 | confirmed：50 级弹窗少一段间空行；confirmed：“勇敢的向前”应为“勇敢地向前”；颜色码和 50/10/3/3 顺序正确 | 是否恢复双换行并改状语“地”；新增的“最终”可另定 |
| entry-00185 | advisory：方括号内多空格是事实，但没有强制排版规则，不是明确错误。占位符和颜色码正确 | 若项目要求紧凑格式，可统一为 `[%s]` |
| entry-00191 | confirmed：`space-time` 只译成“空间”，漏了“时间”；后半句和占位符顺序正确 | 是否改为“扭曲时空”一类 |
| entry-00195 | confirmed：资源名、技能名顺序正确；confirmed：“施展：%s”把动宾用冒号断开 | 是否改为“你没有足够的%s来施展%s。”一类 |
| entry-00198 | pending：片段会拼进母句，但母句冻结译文不在本包，不能独立确认缺停顿。失败结果和感叹号保留；“失手”措辞只是建议 | 先核对母句译文，再决定标点放在母句还是片段 |

Sol 的综合结论：明确要处理的是 00184 的换行与语病、00191 的“时空”漏译、00195 的冒号语病；00185 是可选排版；00198 保持 pending。

## batch-006 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-006-01.md](reports/sol-006-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00216 | confirmed：`Defiler` 是职业大系，译成“腐化者”把上位概念收成子职业 `Corruptor`。refuted：护送 NPC 不会从 Corruptor/Reaver 里随机分配职业 | 人物称谓如何名词化“堕落系”；“堕落者”等候选不能仅凭本条自动确定 |
| entry-00221 | confirmed：源码分开检查 level 与 zone，相邻离开区域的译文也写成“离开地图”。advisory：这仍传达了限制，不足以直接定为明显误译 | 项目里 `level` 统一用“层”“关卡”还是“当前地图”；若必须区分 level/zone，本条要调整 |
| entry-00223 | confirmed：悖论克隆阻止切换 level。refuted：源码没有把这次调用限定为楼梯。advisory：译成“离开地图”不是功能性错译 | 与 00221 共用同一个 level 术语决定；不单独硬改成“离开楼层” |
| entry-00226 | advisory：飘字“杀死（%d）”没有改变死亡事件或数值；“击杀”只是更常见的界面说法 | 按既有飘字风格选择，没有必须修改的机制依据 |
| entry-00231 | confirmed：括号前后各有一个感叹号。pending：方向词是否会展开成“北面方”，允许输入里没有这八个方向的冻结译文 | 是否去掉括号前的感叹号；方向拼接需先核对实际方向词 |

Sol 的综合结论：00216 有真实术语层级失真，但不是随机职业显示错误；00221/00223 是 level/zone 用词精度；00226 只是润色；00231 的重复感叹号成立，方向拼接仍 pending。

## batch-007 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-007-01.md](reports/sol-007-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00244 | refuted：去掉 ` area effect` 的前导空格没有造成中文拼接缺陷；补回空格会变成“火焰 范围效果” | 无须修改，除非项目另有强制的中文拼接空格规范 |
| entry-00247 | advisory：`element` 译成“伤害”后与普通 damage 的字面区别消失，但“火焰伤害”一类显示自然，不足以认定为实质误译 | 选择保留“伤害”，或改成更显式的“元素/属性”；不建议仅凭本条自动修改 |
| entry-00254 | confirmed：同组 entry-00250–00253 是“最大40%”等无空格写法，只有本条是“最大 50%”。护甲穿透和 50% 数值正确 | 若统一排版，改为“最大50%”；若允许数字前空格，需要解释为何只有本条例外 |

## batch-008 六处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-008-01.md](reports/sol-008-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00284 | advisory：机制和占位符正确；“技能（法术）命中后释放”稍紧，容易读成技能本身命中 | 是否改成“法术命中时释放技能”；最小改动可保留 |
| entry-00286 | confirmed：触发条件是来源技能的 `is_mind`，不是精神强度数值。语序仍紧凑 | 是否与法术、自然两条一起统一语序；不要改成“精神强度命中” |
| entry-00288 | confirmed：主体译文已有句号，源码还会再追加 `_t"."`。refuted：不能确定中间有空格，较可能是 `。.` | 主体句号和后续独立句点要一起改，避免只剩西文句点 |
| entry-00298 | confirmed：`forbid_arcane` 阻止使用奥术物品。pending：迁移历史不能在固定 commit 内确认。advisory：`logPlayer` 标签在固定版本没有找到直接消费者 | 先确认旧条目是否仍被兼容路径使用，再决定保留、改措辞或清理 |
| entry-00299 | confirmed：这是当前 `:tformat` 活动译文；“反魔法技能打断了”额外引入技能，并把物品当打断宾语 | 在“你的反魔法干扰了 %s”和“你的反魔法使 %s 无法使用”之间选择 |
| entry-00318 | confirmed：多个避开动作已带“了”，模板再加“了一个陷阱”。refuted：玩家日志在 `Trap.lua:288`，不是 290 | 让模板不再额外加“了”，并核对所有动作片段都能接宾语 |

Sol 的综合结论：实质问题是 00288 的重复标点、00299 的机制措辞、00318 的双“了”。00284 是风格建议，00286 的机制疑虑排除，00298 主要是旧标签残留。

## batch-009 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-009-01.md](reports/sol-009-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00334 | confirmed：日志在敌人 `on_die` 中，等级差超过 3 时输出。“杀死”没有机制误译 | 是否改成更贴近 defeat 的“击败了一名强敌”；不因准确性强制修改。实际日志在 `Arena.lua:555` |
| entry-00344 | confirmed：第二个 `%s` 展开为“她的/它的/他的”，后面再加“的”会稳定变成“的的盾牌” | 最小修正是删掉占位符后的额外“的” |
| entry-00345 | confirmed：双持这条不会叠词，招架成功会挡住攻击。advisory：“发生偏斜”偏生硬，弱化了招架 | 若统一文风可改成“用%s双持武器招架了这次攻击”；否则不必改。日志在 `Combat.lua:482` |
| entry-00354 | confirmed：去掉数量括号前的半角空格不影响占位符和机制 | 无实质待决。“搜集/收集”和空格只是文风 |

## batch-010 十一处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-010-01.md](reports/sol-010-01.md)。译文未修改。Sol 的总括是 3 条 confirmed、8 条 advisory，没有 refuted 或 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00368 | confirmed：首句把失衡值说成“能力”，容易暗示数值越高越强，和“接近 0 更平衡”相反 | 是否改成“反映你在自然平衡中的状态”一类 |
| entry-00373 | confirmed：原文改变的是技能使用者，译文后半改成“给玩家” | 在“永久改变你/角色/使用者”之间选全篇口吻 |
| entry-00374 | confirmed：这里是基础属性 Magic，面板和源码简中是“魔力”，提示写成“魔法” | 标题和属性代称是否统一为“魔力”，魔法能量仍可保留“魔法” |
| entry-00393–00400 | advisory：模式和难度含义、占位符都对；单模式用全角括号，复合后缀用半角外括号。多数行号被 Sol 按固定 commit 更正 | 是否给整组后缀定统一排版；不统一也不必单条修改 |

## batch-011 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-011-01.md](reports/sol-011-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00419 | advisory：数值正确，只是“超过1500点”和同组“超过 600 点”等空格不一致 | 是否统一为“超过 1500 点” |
| entry-00423 | confirmed：`life-saving talent` 被写成任意“技能”，漏掉免死/替死限制 | 选用“保命技能”“免死技能”或“借助技能免于死亡”，并决定数字空格 |
| entry-00428 | advisory：关闭三扇传送门的条件和数量都对，只是句式与一扇、两扇不平行 | 是否按同系列模板改写 |
| entry-00429 | confirmed：`Maj'Eyal` 被写成“旧大陆”。pending：术语库是否强制“马基·埃亚尔”不在本次允许输入内 | 专名泛化已有源码依据；正式译名仍待术语记录确认 |
| entry-00434 | confirmed：任务名是 `Lost Knowledge`。advisory：增补“遗失的知识”有助于检索，但“珠宝匠托付”比源码关系更解释性 | 保留任务名增补，或收成更贴近原文的说法；若保留，确认“遗失的知识”是否为正式译名 |

## batch-012 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-012-01.md](reports/sol-012-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00443 | confirmed：统计的是 `COLD` 伤害。pending：必须改成“寒冷伤害”缺少冻结术语依据，“冰冷伤害”本身能传达含义 | 提供术语裁决后才能决定“冰冷”还是“寒冷” |
| entry-00448 | confirmed：格式码完整；“一切为了随机”偏离 `most of all`。advisory：“他”指代职业只是表达问题 | 是否改成“最重要的是，它完全随机”；代词可改“它”或省略 |
| entry-00455 | advisory：引号改冒号是风格。confirmed：末句把“在我们的力量面前无人通过”说成反抗的力量通过 | 是否改成“在我们的力量面前，谁也休想通过” |
| entry-00458 | confirmed：在该职业里“灰色的黎明”不合适，应靠拢“暮光”。refuted：不能说 twilight 绝对不能指黎明。advisory：“微光/暮色”不如“暮光”贴切 | 若无相反术语，优先“灰色暮光”或“灰暗暮光” |
| entry-00476 | confirmed：线索指向维网，但只有伊克族对话才解锁灵能系；译文漏了 way/The Way 双关；“打开钥匙”搭配不当 | 记录解锁限定；决定如何同时保留“道路”和“维网”；英文原句本身也不寻常，修法需人工选定 |

## batch-013 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-013-01.md](reports/sol-013-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00486 | advisory：后半少了“时”。refuted：这里把 using 译成“装备”没有词义偏移 | 是否只为整齐补上“时” |
| entry-00489 | advisory：“最大的伤害”把修辞收成最高级。confirmed：双手高伤害没有机制错误 | 是否改成更贴近“强大的破坏力” |
| entry-00492 | confirmed：漏了 pit-fighter；amateur practitioner 译成“门外汉”把身份说反了 | 选定 pit-fighter 译名；业余练习者不宜再写成门外汉 |
| entry-00500 | confirmed：“奥术技艺”符合该职业的奥术机制。pending：不能据此认定必须改成 Cults 的“骇异”。advisory：诡秘色彩变弱 | 若要跨组件统一，另核术语适用范围；否则可保留 |
| entry-00501 | advisory：感叹号改逗号，以及“玩家/你”切换。confirmed：被追猎的机制说明准确 | 是否统一人称和感叹号 |

## batch-014 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-014-01.md](reports/sol-014-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00522 | confirmed：这里译成“食尸鬼跳跃”，冻结术语快照的 preferred 是“定向跳跃” | 决定改介绍还是校准术语库；不能只凭其他技能条目反向改术语 |
| entry-00527 | confirmed：“不死系技能”把免疫和生理特性收窄了，同节食尸鬼句用的是“不死系能力” | 是否统一为“不死系能力” |
| entry-00553 | confirmed：冒烟的大坑被并进半身人；“待得太久”把未来风险说成当前停留 | 恢复两个并列对象，并重译“越晚回来” |
| entry-00560 | confirmed：眼皮被写成脸上；perhaps 被写成传说中的唯一。pending：物品中文名是否还需对齐物品栏 | 恢复具体部位和“也许”；物品标准名另行核对 |

## batch-015 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-015-01.md](reports/sol-015-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00570 | confirmed：开引号和闭引号都是右双引号 `”` | 开引号改为 `“` |
| entry-00574 | confirmed：搭配不成立，但不只是把“达到”改成“到达” | 选“建造一座通往马基·埃亚尔的新远行传送门”或等义说法 |
| entry-00579 | advisory：成就里有“巫师”，但固定简中本身对 Sorcerers 并不统一，不能单凭这条判“法师”错误 | 先做全局术语决定，再决定是否改这一条 |
| entry-00581 | advisory：与 00579 是同一指称的失败分支 | 与 00579 一起改，不要只改一个分支 |

## batch-016 七处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-016-01.md](reports/sol-016-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00604 / entry-00605 | advisory：两句都是“请……？”，语义和换外观机制都对 | 成对润色或成对保留 |
| entry-00615 | advisory：“研究”重复有后文依据，不是无根据增译 | 若润色，只改后一句即可 |
| entry-00620 | confirmed：“玩的开心”“勇敢的前进”是助词误用 | 是否列入低风险校正 |
| entry-00621 | confirmed：“陷阱”削弱了 death trap 的致命意味 | 选用“送命的陷阱”或“死路”一类 |
| entry-00623 | refuted：“保护”没有把兽人写成友军。confirmed：定语被逗号切断，读起来像使用了地下深处 | 不要按善意保护来改；若改，按“位于……、由兽人把守”整理 |
| entry-00634 | confirmed：stabbed 是物理死亡片段。pending：不能证明最终一定显示“被刺杀而死”。advisory：“被刺杀”比刺伤更强 | 先核对完整死亡模板或实际渲染，再决定是否改 |

## batch-017 八处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-017-01.md](reports/sol-017-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00644 | advisory：省掉了“可怕景象”，抵抗成功和恐惧机制是对的 | 是否补回诱因 |
| entry-00646 | confirmed：奥术法力燃烧有源码依据。pending：术语库是否要求只写“法力燃烧” | 对照冻结术语记录再决定 |
| entry-00647 | confirmed：这里只移除护盾，没有爆炸范围伤害。advisory：“终于破碎了”可以接受 | 文风选择“破碎”或“爆裂” |
| entry-00650 | confirmed：机制是汲取生命并造成物理伤害。pending：是否必须改成“生命汲取” | 核对术语记录后再改 |
| entry-00652 | confirmed：“法力蠕虫奥术”语序不自然 | 选“奥术法力蠕虫”或“法力蠕虫（奥术）” |
| entry-00653 | refuted：原文就是 manaburn arcane，“奥术”不是增译。pending：术语库是否要求省略属性 | 没有术语裁决前不必因忠实度改 |
| entry-00657 | advisory：“阴影地宫”指向正确，只是把入口说成了路 | 若强调地格类型可用“阴影地宫入口” |
| entry-00660 | confirmed：漏了 muffled，并多加了“陌生” | 去掉“陌生”，并补上低沉或隔墙的听感 |

Sol 的汇总：确认的是 00652 的语序和 00660 的两项忠实度问题。00646、00650、00653 的术语冲突因没有原始术语记录而保持 pending。

## batch-018 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-018-01.md](reports/sol-018-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00683 | confirmed：raises 是举起头骨，不是让它站起来；眼窝被写成眼中。日志实际在 `rat-lich.lua:73` | 选用举起、高举或托起；眼窝可一并改 |
| entry-00684 | confirmed：dust of decay 译成灰烬，多了燃烧意象 | 保留意译，或改成腐朽的尘埃 |
| entry-00712 | confirmed：impenetrable 译成结实，弱于难以穿透 | 在坚不可摧和较克制的说法之间选择 |
| entry-00713 | confirmed：wants honey 被改成喜欢蜂蜜并加了萌化语气。advisory：标点累赘；“会吃掉玩家”不是源码明说 | 是否恢复“想要蜂蜜”，不要补写原文没有的“吃掉你” |
| entry-00719 | confirmed：formation 被写成生物。refuted：同批基础描述译的是水晶结构，不是生物。pending：其他颜色晶体是否另有惯例 | 描述用水晶簇还是保留生物；更窄的一致性主张先不要当已核实 |

## batch-019 九处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录，未作语义裁决。完整文本见 [sol-019-01.md](reports/sol-019-01.md)。译文未修改；本节在暂停收尾时转录，证据未提交。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00722 | confirmed：首句把实体写成抽象的“非生命力量”；confirmed：“unearthly limbs, of purest black”修饰关系被译错 | 重写首句保留实体中心；用“非尘世的纯黑肢体”一类语序 |
| entry-00723 | confirmed：withering 译作“腐蚀”有轻微语义偏移。advisory：增译“周围的一切”属合理显化；“不断”连用三次 | 是否改成“使万物枯萎、灼烧”；重复用词只作顺手润色 |
| entry-00728 | pending：carrion worm mass 是否违反固定术语“腐肉虫群”，允许输入不含术语正文，无法独立确认 | 查冻结术语记录；确认规范后再接受该 finding |
| entry-00730 | confirmed：漏译 all，丢掉“全部眼睛一并落地”的机制信息；confirmed：条件分句后缺逗号 | 补“所有/全部”并加逗号，可合并处理 |
| entry-00731 | pending：eldritch eye 是否必须按术语音译“艾尔德里奇之意”，意译“骇异之眼”脱离术语时可成立 | 核对术语记录的 section、source_tag 与备注 |
| entry-00733 | confirmed：漏译 pulsates；confirmed：“不停的扭动”助词误用 | 补出“脉动/跳动”，整句重写时改用“地” |
| entry-00740 | confirmed：seek to destroy 被译成进行体“在毁灭”；advisory：it 由“生命”具体化为“生者” | 改“企图/试图毁灭”；是否回“生命”属忠实度取舍 |
| entry-00746 | confirmed：losgoroth 被泛化成“虚空生物”，与同批“洛斯格罗斯”不一致；pending：两处 mana 是否违反“法力值” | 恢复“洛斯格罗斯”专名；核对 Mana 冻结术语 |
| entry-00752 | confirmed：“两只巨大的双手”量词重复且身体意象错误；confirmed：蛇尾与腿的关系被译反 | 改“巨大的双手”或“两只巨大的手”；重写蛇尾句 |

Sol 自报共 17 个 claim：11 confirmed、3 pending、3 advisory、0 refuted。补充说明 Gemini 报告的若干源码行号并非实际描述行（`ghost.lua:83`、`ghost.lua:131`、`lich.lua:78`、`losgoroth.lua:75`），文本对象仍对应，引用行号不宜沿用。术语类 00728、00731、00746 因允许输入不含术语正文保持 pending，未由主代理代为裁决。

## batch-020 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-020-01.md](reports/sol-020-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00763 | confirmed：torn away from 被译成“赶出来”，动作性质从被带离变成被驱逐；confirmed：home world 译“老家”丢了 world 且语域偏口语。pending：断言为“跨位面传送”缺源码依据 | 改成“被强行带离/从故乡世界剥离”；机制措辞不要写死 |
| entry-00768 | confirmed（轻微）：serviceable condition 译成“值得信赖”，强于“尚堪使用” | 是否收束为“锈迹斑斑，但尚能使用” |
| entry-00780 | advisory：“类人生物”与同批 entry-00778 的“人形生物”不一致，仅行文问题 | 项目要求统一自由叙事用词时再改 |
| entry-00781 | confirmed：brothers and sisters 被概括成“集体行动”，遗漏同胞关系；confirmed：后半句单数改复数；confirmed：make_escort 配置要求三只同名护卫，但“运行时必定三只”这一绝对说法 refuted；pending：是否必为“同窝亲生”无机制依据 | 改成“与兄弟姐妹一同出现”，审核证据写“配置会尝试添加三只”，不要写成运行时保证 |

共 10 个 claim：6 confirmed、2 pending、1 advisory、1 refuted。Sol 同时撤回了 Gemini 报告里“运行时固定伴随三只”的绝对表述，属证据强度修正，仍由人工决定最终措辞。

## batch-021 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-021-01.md](reports/sol-021-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00804 | pending：源码确认两处指向同一专名 `Rotting Titan`，但冻结输入未含该 NPC 现行中文译名，无法独立证实“腐化/腐烂”不一致 | 核对 `Rotting Titan` 规范译名后再裁决 |
| entry-00805 | confirmed：漏掉 other；confirmed：`within radius %d` 修饰的是作用范围而非生物，译文改了修饰关系 | 改为“击退半径 %d 范围内的其他生物”，措辞自定 |
| entry-00820 | confirmed：无端增译“的存在”，并把 corruption 与 power 糅合成“腐蚀力量”。advisory：blackened 译“被玷污”偏象征 | 去掉“的存在”，按设定裁定 its power 指代与“发黑/玷污”取舍 |
| entry-00840 | confirmed：与同系列 9 处“一瓶[颜色]液体”句式不一致。refuted：“严重破坏排比”程度被夸大，应按低影响处理 | 若要求系列统一，改为“一瓶黄色液体” |

共 7 个 claim：4 confirmed、1 pending、1 advisory、1 refuted。两处 refuted/advisory 是对 Gemini severity 的下修，原样转录，未由主代理改写。

## batch-022 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-022-01.md](reports/sol-022-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00843 | advisory：“提升了你核心技能的能力”修饰关系生硬，未造成机制误解；Gemini 所写源码行号不准，实际在 brotherhood-artifacts.lua:203、263 | 若要顺，可改“运用核心技能的能力” |
| entry-00852 | confirmed：“抓取藤蔓”与同 ego“抓握之/抓握”不一致，且可被读成“去抓藤蔓” | 在“抓握藤蔓/缠绕藤蔓”中择一，是否强制与 ego 名统一属风格裁决 |
| entry-00866 | confirmed：靴子 ego 名称“振奋的”与关键字“疗愈”两套译法，关键字会显示在已鉴定物品名里 | 统一方向由人工定；按治疗机制 Sol 认为“疗愈”更直接 |
| entry-00873 | confirmed：披风 ego 同样“振奋的/疗愈”割裂 | 与 00866 同批裁决，不要分开改 |
| entry-00881 | refuted：`naturalist's` 与 `natural` 是两个不同源串，术语快照也映射 `natural → 自然`，不要求中文字面相同 | 无必办事项；除非另立“关键词必须与名称词干统一”规则 |

共 5 个 claim：3 confirmed、1 refuted、1 advisory、无 pending。译文未修改。

## batch-023 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-023-01.md](reports/sol-023-01.md)。译文未修改。三条均无 confirmed 的译文错误。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00899 | confirmed：奥术戒指前缀机制描述准确；confirmed：同批 00900/00918/00919 同词根内部一致。advisory：“魔术师”偏舞台魔术；advisory：一致性不等于最佳译法 | 若要把 conjurer 词根奇幻化，需连关联条目和术语策略整体处理 |
| entry-00914 | confirmed：调用实际在 totems-powers.lua:132，Gemini 行号不准。refuted：按句号改标点不成立，源码是感叹号。pending：术语快照另有 logSeen 句号版本无法在允许输入内确认 | 除非要跨日志语境统一句末标点，否则本条无需修改 |
| entry-00918 | confirmed：名称在 wands-powers.lua:91；confirmed：与同词根条目字面一致。advisory：“魔术之”奇幻感弱；advisory：Gemini“既有译法故无问题”论证不足 | conjuration/conjure 是否统一奇幻化译名，连同戒指条目一起裁决 |

共 11 个 claim：5 confirmed、4 advisory、1 refuted、1 pending。confirmed 均为源码事实与一致性核验，不是译文错误裁决。

## batch-025 八处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-024-01.md](reports/sol-024-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-00972 | advisory：“亚特莱”音节可能不完整，源码无官方读音不能判错。pending：所谓“全仓统一译法”无法在允许输入内验证 | 要不要改成“阿特利亚”类形式，交专名策略决定 |
| entry-00980 | confirmed：“变的暗淡”应为“变得暗淡”。refuted：并非“其余内容完整准确”，`runes of power` 只译成“符文”漏了 `of power` | 修文法；是否补“力量符文/强力符文” |
| entry-00984 | confirmed：无中生有“如果你想保留物品”的目的条件。pending：是否属有意复用无法证明 | 若要求逐句对应，改为直述“要取出物品，只需……” |
| entry-00992 | confirmed：括号提前闭合，把“十回合”插进三组效果之间造成断裂。confirmed：`cut` 应按术语译“流血”，现作“撕裂” | 重排括号与持续时间；此处改“流血免疫” |
| entry-00997 | confirmed：“不断的向下滴血”应为“不断地”。confirmed：Gemini 对专名与身份的正面判断成立 | 修文法即可，无阻断项 |
| entry-01000 | confirmed：“基于魔法”应为“基于魔力”（源码 combatStatScale("mag")）。advisory：“疾病和毒素”有合计上限歧义 | 统一“基于魔力”；歧义可选改“疾病或毒素状态中的至多 %d 项” |
| entry-01001 | confirmed：“（基于魔法）伤害半径 %d”缺标点连跑。confirmed：同样应为“基于魔力” | 补成“……物理伤害（基于魔力），半径为 %d” |
| entry-01002 | confirmed：`grand` 漏译。advisory：“炼金师”是叙事称谓不必然违反职业术语。advisory：“7把”数字格式 | 选“大炼金术师/伟大的炼金师”；数字格式按仓库风格 |

共 17 个 claim：10 confirmed、2 pending、4 advisory、1 refuted。译文未修改。

## batch-026 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-025-01.md](reports/sol-025-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01029 | confirmed：抵抗的是触须的拉扯（pull），不是抓取（grab）；源码 656–662 行先抓住再拉近，译文与前一条日志直接冲突 | 改成“抵抗了触须的拉扯/牵引”，措辞自选 |
| entry-01032 | confirmed：`wound` 是该物品实际筛选的三个效果子类型之一。pending：“必须译为创伤”的术语条目不在允许输入内，无法确认 | 主代理按术语库核对该条 category/section/source_tag 后再定是否升级 |
| entry-01038 | confirmed：主语错置，达克顿打造的是臂铠不是“厄流纪”；confirmed：`unparalleled` 被弱化；confirmed：`these` 译成“那些” | 重写首句恢复主体，另选“无与伦比/举世无双”和近指词 |

共 6 个 claim：5 confirmed、1 pending。译文未修改。

## batch-027 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-026-01.md](reports/sol-026-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01068 | confirmed：第三个 `%s` 是物主代词（`who:his_her()`），不是敌人数量，现译“%s个敌人”是运行时可见的占位符语义错误 | 改句式保留物主关系，或按中文习惯处理该占位符，不能删参破坏参数契约 |
| entry-01074 | confirmed：占位符、`@Source@`、`#SALMON#`、`#LAST#` 与参数角色完整。confirmed：“放出……被束缚的灵魂”与机制不符（剑只是调用被拘禁灵魂的力量，不会释放）。advisory：“模仿了%s”对应 `xmanifesting`（源码本身疑似拼写错误） | 改“调用/汲取/借用……力量”一类不暗示灵魂获释的措辞 |
| entry-01081 | confirmed：遗漏 `once brilliant`。confirmed：`decayed` 被泛化为“破旧”，与 3723/3778/3802/3826/3850 的阶段词序列冲突。refuted：问题不是漏 `heavily`，程度已由“十分”承接 | 补“曾经辉煌/昔日璀璨”；`decayed` 改“严重朽坏/严重腐蚀” |

共 8 个 claim：6 confirmed、1 advisory、1 refuted、无 pending。Sol 另注明 Gemini 行号偏移（实际 3251、3642、3778），不影响判断。译文未修改。

## batch-028 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-027-01.md](reports/sol-027-01.md)。译文未修改。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01085 | confirmed：`cone` 译“弧形区域”与同批 entry-01097“锥形范围”不一致。confirmed：“至多两项”是译文额外添加、但与源码行为一致。refuted：因此它不构成翻译问题。confirmed：占位符保留正确 | 统一为“锥形区域/范围”；“至多两项”保留，只调括号结构 |
| entry-01096 | confirmed：两个 `%d` 顺序正确。advisory：半角括号与中文标点混排，且空格规则不一致。confirmed：`charge` 是可积累可消耗的蓄能值，“当前增幅”有机制歧义 | 括号统一全角；改“当前充能/蓄能”或与 entry-01097“吸收量”统一 |
| entry-01116 | confirmed：漏译 `when it proved necessary`。advisory：与 `The Calm` 名称的对照属文学解读，源码未明写 | 补回条件语义，不扩写未明说的背景 |
| entry-01120 | confirmed：光明/黑暗应按伤害类型术语作“光系/暗影”。confirmed：`Magic` 应译“魔力” | 改成“爆发出光系和暗影伤害（受魔力加成）”一类表述 |

共 11 个 claim：8 confirmed、2 advisory、1 refuted、无 pending。Sol 引用的 entry-01091/01097 只是同批术语对照，不是交叉对象，未给分档。

## batch-029 十一处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-028-01.md](reports/sol-028-01.md)。译文未修改。Sol 汇总：9 confirmed、2 advisory，无 refuted/pending；优先处理 01132、01156、01162、01163。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01127 | confirmed（低影响）：`most foes` 漏“大多数” | 是否补“大多数敌人” |
| entry-01132 | confirmed：`time flows` 误作“时间线”，`through` 被改成聚焦位置 | 改“通过……汇聚时间流”一类表达 |
| entry-01137 | confirmed（低影响）：丢 `crackles` 动态、弱化 `vicious` | 文风选择 |
| entry-01145 | advisory：`imbue` 译“安装”，未体现力量注入 | 系统统一“镶嵌”还是“灌注”，由维护者定 |
| entry-01149 | confirmed（纯排版）：`50%%;降低伤害时` 半角分号 | 换全角分号 |
| entry-01155 | confirmed：「自命不凡的认为」的/地错误；“恶魔的老巢/地狱之焰”属增饰 | 保守直译还是保留叙事性意译 |
| entry-01156 | confirmed：`to foes who enter it` 被译“所有经过的生物”，暗示伤害自身与友方 | 限定为“进入其中的敌人” |
| entry-01160 | confirmed（低影响）：`biting colds` 意象偏移；“您/你”不统一 | 统一称谓与措辞 |
| entry-01161 | advisory：`tingly` 译“刺痛”偏重、“增强了你的思考”生硬 | 是否润色，不按机制错误处理 |
| entry-01162 | confirmed：`The blade` 是战斧刃部，译文写成剑身 | 改“斧刃” |
| entry-01163 | confirmed：`bright warm light` 译“微光”，亮度方向相反 | 改“明亮而温暖的光芒” |

共 11 个 claim：9 confirmed、2 advisory。译文未修改。

## batch-030 六处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-029-01.md](reports/sol-029-01.md)。译文未修改。共 21 个 claim：9 confirmed、5 advisory、7 refuted（其中 6 条 refuted 是 Gemini 所引源码行号不准）。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01183 | confirmed：`%s` 后半角空格不一致。refuted：Gemini 行号不准 | 删多余空格 |
| entry-01193 | confirmed：“牢牢的抓住”应为“牢牢地”。advisory：两句合并成逗号句；“挖地逃走”对原文的处理。refuted：行号不准 | 改“地”；是否拆回两句 |
| entry-01194 | confirmed：`It doesn't much matter.` 被语义改写成“没有确切的答案”。advisory：Gemini 称对任务指引无实质负面影响存疑。refuted：行号不准 | 恢复“那没什么要紧”一类原意 |
| entry-01196 | confirmed：“穿的”应为“穿得”；句号改省略号。refuted：「冰龙常换牙完全准确」不成立；行号不准 | 改“得”；标点按原句风格 |
| entry-01198 | confirmed：把字句杂糅；无依据增添“明天”。advisory：`stuff` 译“瓶子”。refuted：行号不准 | 改“把这个瓶子拿远一些”；去“明天” |
| entry-01201 | confirmed：后半句明显扩写；译文另有轻微表达问题。advisory：Gemini 称生动契合背景。refuted：行号不准 | 收束到原文信息量 |

译文未修改。多条 refuted 都是对 Gemini 证据质量（行号）的下修，原样转录。

## batch-031 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-030-01.md](reports/sol-030-01.md)。译文未修改。共 12 个 claim：8 confirmed、2 refuted、1 pending、1 advisory。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01205 | confirmed：译文增补“其他蠕虫”属轻微增译。refuted：与物品描述并不构成矛盾。pending：`knots` 是否只能理解为解开自身的结 | 若要贴近原文用“把缠结解开”，不锁定意象 |
| entry-01210 | confirmed：同列表“实验品 A-C”与“试验品 D-N”不一致。confirmed：专名、`#{bold}#` 等标签与语义完整 | 首项是否统一为“试验品 A-C”，人工决定 |
| entry-01211 | refuted：`second` 并未漏译，“传送回来”已表达返程。confirmed：格式与叙事信息完整。advisory：“口吻贴合”属文风评价 | 不必因 second 改；可选显化“第二次” |
| entry-01214 | confirmed：“截然而止”是误字应为“戛然而止”；confirmed：`sullied` 译“厌倦”语义偏移；confirmed：后段复数听众被改成单数“你”；confirmed：专名译法准确 | 改成语；`sullied` 定调；听众统一为“你们” |

译文未修改。entry-01211 的主疑点被 refuted，原样转录。

## batch-032 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-031-01.md](reports/sol-031-01.md)。译文未修改。共 12 个 claim：8 confirmed、3 advisory、1 pending、无 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01215 | confirmed：`base materials/components` 译“基本元素”，混淆物质组分与“埃亚尔元素”，且把无生命组分称作“他们”。confirmed：“明智的使用它”助词误用。confirmed：状语与主句粘连缺停顿。advisory：“双刃剑”替换了“可用于善或恶”。pending：控制码完整、译名同 section 一致的主张证据不足 | 改“基本成分/物质组分”“它们”“明智地”；补逗号；一致性另取冻结样本再确认 |
| entry-01216 | confirmed：`”被烧成焦炭”` 开引号方向错误。confirmed：该 Lore 解锁龙火陷阱，叙事与机制相符 | 首字符换左双引号 |
| entry-01218 | confirmed：四处对话以右双引号开引；确认问号句号与引号外标点重复；确认“舞会开始了”另拆段且缺句末标点。advisory：“魔法剑士技能组合”是联想不是机制证据；advisory：`Aranion` 添译“先生”拉远语气 | 四处引号、标点结构统一重排；是否并段、去“先生”属编辑风格 |

译文未修改。一条译名一致性主张因冻结输入不含术语正文保持 pending。

## batch-033 单条 Lore 交叉结果（entry-01220）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-032-01.md](reports/sol-032-01.md)。译文未修改。共 23 个 claim：21 confirmed、1 refuted、1 advisory，无 pending。Gemini「该条存在多处忠实度问题」的主结论被 confirmed。

| 类别 | Sol 分档要点 |
| --- | --- |
| 忠实度/漏译（confirmed） | `be no match to this` 曲解；`Expecting someone else?` 错移；`I wonder` 语气丢失；`know what we’re doing` 窄化；“提上日程”未表达发动日临近；`collapsed under their attacks` 力度降低；`Yet the alternatives seemed grim` 漏译；`naked form` 漏译；`I looked at her` 漏译；`brusquely` 漏译且臆增“许久的沉思后”；`visibly aroused` 被弱化；向东启程与气氛骤变漏译；火花主体漏失并臆增“天花板上的图案” |
| 语法/排版（confirmed） | “像着”错别字；“消失地无影无踪”应为“得”；“远行传送门周围的闪烁着……”句法残缺；三处 `？”，` 标点不规范 |
| 无缺陷项（confirmed） | 单手支头被译成“双手”属动作事实错误；格式控制符完整；点名的核心专名未发现实质错误 |
| 收窄 Gemini（refuted/advisory） | refuted：`I wonder` 并未“反转成附和”；advisory：`collapsed` 被定性“严重”过重，应按“力度降低”处理 |

人工待决：按上表逐项决定改写；两项收窄意见不要写进修复理由。译文未修改。

## batch-034 单条 Lore 交叉结果（entry-01221）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-033-01.md](reports/sol-033-01.md)。译文未修改。共 17 个 claim：15 confirmed、1 advisory、1 refuted，无 pending。

| 条目 | Sol 分档要点 |
| --- | --- |
| entry-01221 | confirmed：`no normal day` 译反且漏 `day of reckoning`；confirmed：“希望的缰绳/扼住命运的咽喉/真正的和平”均为无依据增译；confirmed：`the steady hand` 单数比喻被破坏；confirmed：`rip out the flesh beneath` 的大地—血肉意象被泛化；confirmed：“这个恶魔就是兽人”“任何种族”改变原句关系；confirmed：“组织其她手下的法师”表面文本缺陷；confirmed：`taking courage from the duties of command` 施受关系被改变；confirmed：`Turning up her face` 译成反向动作；confirmed：“与我长吻”属无依据增添；confirmed：`pavilion` 重复译“营地”；confirmed：`doubt` 被弱化又无依据强化为“无尽的困扰”；confirmed：`raved` 贬义被改成褒义“慷慨激昂”；confirmed：`bringing my face close` 漏译并换成无依据动作；confirmed：`bravado` 漏译且“平日”无依据；confirmed：两处敬称均属增译且互不一致。advisory：「血肉意象呼应被焚村镇」只是合理解读非源码明示。refuted：“长吻必然与轻柔细腻冲突”不成立 |

人工待决：逐项决定改写；refuted/advisory 两项不要写进修复理由。译文未修改。

## batch-035 单条 Lore 交叉结果（entry-01222）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-034-01.md](reports/sol-034-01.md)。译文未修改。共 13 个 claim：10 confirmed、1 refuted、1 advisory、1 pending。

| 条目 | Sol 分档要点 |
| --- | --- |
| entry-01222 | confirmed：格式与控制字符无问题；confirmed：“我过去已知依赖着”错别字（已知/一直）；confirmed：两处 `！”`，` 冗余标点；confirmed：`head in my lap` 译成“抱着……脸庞”；confirmed：`crisis` 译“毁灭”并加“瞬间”；confirmed：`burns` 泛化成“创口”；confirmed：末段声音/音符隐喻被抹平；confirmed：`bulwarks` 译“防线”；confirmed：“用我们的方式用力量……”句式套叠；confirmed：瞬时模板词高频重复。refuted：`seeping freely` 被“反向表达”不成立（但仍有轻微信息损失 advisory）。pending：`Kar’Krul` 与“卡·克鲁尔”跨文本不一致，允许输入内无法独立确认 |

人工待决：术语类 pending 需主代理按术语库核对后才能升级；refuted 项不进修复理由。译文未修改。

## batch-036 单条 Lore 交叉结果（entry-01223）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-035-01.md](reports/sol-035-01.md)。译文未修改。共 16 个 claim：14 confirmed、1 pending、1 advisory，无 refuted。Sol 总评：Gemini 的核心事实疑点大多成立，`this human` 指代倒错与 `none of this` 时间倒错最明确。

| 条目 | Sol 分档要点 |
| --- | --- |
| entry-01223 | confirmed：格式控制符与段落结构；confirmed：`this human` 指代被译错；confirmed：`none of this I knew` 时间指代错；confirmed：`saying to seek you out in Elvala` 漏译；confirmed：`I took on` 漏掉主动接战；confirmed：第 28 段漏句末标点；confirmed：第 29 段重叠标点；confirmed：第 32 段从句被句号截断；confirmed：第 22 段时间状语断裂；confirmed：`relapse` 弱化为“虚弱状态”；confirmed：`scared of that empty look` 译成“心如刀割”；confirmed：`empty` 译“空灵无物”；confirmed：`white stone` 译“磐石”；confirmed：`dealings` 译“交易”偏窄。pending：「白石是所有夏·图尔遗迹的普遍材质」广义设定主张证据不足。advisory：Gemini 称寻人遗命为“关键情节枢纽”略有夸大 |

人工待决：两处“关键情节遗漏”按 Sol 的收窄意见评估影响，不按完全丢失情节计。译文未修改。

## batch-037 单条交叉结果（entry-01224）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-036-01.md](reports/sol-036-01.md)。译文未修改。共 3 个 claim：2 confirmed、1 advisory。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01224 | confirmed：「床位」应为「床尾」，源码 `near the end of my bed`（elvala.lua:429），同章第二夜也用 `at the foot of my bed` | 改“床尾的一个身影”或更贴 near 的“床尾附近的一个身影” |
| entry-01224 | advisory：眼周皱纹特写被泛化成“脸上的痕迹”，且相邻分句重复“痕迹” | 若纳入本轮润色，恢复“眼睛周围布满操劳的皱纹” |
| entry-01224 | confirmed（低影响）：直接引语逗号置于后引号之外；Sol 认为 Gemini 视为中性的“排版习惯差异”略显宽松 | 先确认仓库对话标点体例，再决定优先级 |

译文未修改。

## batch-038 单条交叉结果（entry-01225）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-037-01.md](reports/sol-037-01.md)。译文未修改。共 19 个 claim：17 confirmed、2 pending、无 refuted/advisory。Sol 总评：Gemini 指出的断裂病句、方位错误、动作失真、漏标点、单复数与漏译均成立。

| 组 | Sol 分档 |
| --- | --- |
| 病句/方位/动作（全 confirmed） | “长着六肢的长而厚的身体之上”断裂病句；“我面对着背后的怪物”方位矛盾；“顺便跳进了我背后的门中”；`blade` 译“刀片”；“她冲破了她分开的门” |
| 标点（全 confirmed） | 第 41 段末漏句号；多处引号外标点 |
| 实体 `luminous horror` | confirmed：此处确指该游戏实体；**pending**：固定中文实体名是否必须是“金色恐魔”；confirmed：“还有一些某种……”语病 |
| 战斗动作（全 confirmed） | 单数误作复数；漏译剑上电火花并添“试图” |
| 其他措辞（全 confirmed） | `hanging with one hand from her staff`；“她的法杖被瞬间破碎”；“已死神的尸体”；`all my senses seemed on edge` |
| 正面项 | confirmed：富文本标记与占位符完整；confirmed（仅限本条目内部）：人名地名专名一致；**pending**：与传记前序章节“严格一致”的跨章节主张 |

人工待决：两项 pending 需主代理按术语库/前序冻结文本核对后才能定。译文未修改。

## batch-039 单条交叉结果（entry-01228）

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-038-01.md](reports/sol-038-01.md)。译文未修改。共 9 个 claim：4 confirmed、3 advisory、1 refuted、1 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01228 | confirmed：吸血鬼段增译并改写因果（“团体的力量”“自己的奴隶”“用钢剑刺穿喉咙”）。Sol 提醒“严重增译”程度标签不必照收 | 改回“因关系网络而成为统治者”“以冰冷的钢铁相待” |
| entry-01228 | confirmed：骸骨巨人段多处虚构修饰（“法师老头”“一向被视为力量象征”“每滴鲜血都令其饥渴”“有幸”） | 删除明确增饰；“有幸”是否保留属文风 |
| entry-01228 | advisory：“算个屁指南”“弱柳扶风”更粗俗且丢“强风吹散”意象，但叙述者本就口语粗豪 | 文风是否收敛由人工定 |
| entry-01228 | confirmed：`effort` 两次被具体化为“法力”，固定实现（master-of-bones.lua:233-274）只在施放末尾扣一次法力，无受损程度关联 | 改回“力量/心力/维持其复苏的力量” |
| entry-01228 | confirmed：巫妖段强行男性化并增“身体”（源码为复数/中性 `liches`/`they`）。refuted：“巫妖超越传说”被曲解不成立，后句已表达。pending：`abyssal power` 是否必须译“深渊力量” | 去掉男性限定；查授权术语记录后再定 abyssal |
| entry-01228 | advisory：尸妖段增“万幸的是”。advisory：单段被拆成多段、标题顿号 | 若要求严格贴合改“尽管如此”；拆段仅在要求结构对应时恢复 |

译文未修改。Sol 总结把核心 confirmed 列为四点（增改因果、无依据增饰、`effort`→法力、男性化与“身体”）。

## batch-040 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-039-01.md](reports/sol-039-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 refuted、1 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01230 | confirmed：对应 `elandar-1`，正文与专名含义相符；confirmed：控制标签闭合、标点合理。advisory：`too` 的斜体范围被扩大为“理智得过了头” | 斜体范围是否收束属排版取舍 |
| entry-01245 | confirmed：对应 `keepsake-kyless-journal-2`，正文、标签与叙事准确。advisory：“发现了什么——”有不定代词直译痕迹 | 是否顺译该破折号结构 |
| entry-01247 | confirmed：对应 `keepsake-kyless-journal-3`，剧情准确；confirmed：`priceless` 译“令我感到无比快意”合乎语境；refuted：把该译法当误译的主张不成立。pending：“呆在一起”通假俗写规范应为“待在一起” | 是否按规范改“待在”，属用字规范决定 |

译文未修改。Sol 三条正文核对均以源码条目 ID 对照，正面结论也原样记录。

## batch-041 六处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-040-01.md](reports/sol-040-01.md)。译文未修改。共 16 个 claim：8 confirmed、3 pending、3 advisory、2 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01252 | confirmed：整体未发现问题。advisory：句号改省略号属修辞润色 | 无必办项 |
| entry-01256 | confirmed：第二段被额外单换行切开；confirmed：末尾 `～。` 标点连用 | 并回段落、去重标点 |
| entry-01259 | confirmed：`peace` 译“胜利”；confirmed：`newly found military might` 被窄化；confirmed：`Army of Rogues` 译“游击军”损失命名词义；pending：是否必然是 Rogue 职业双关；advisory：标题序号与二十/30 写法不统一 | 专名与职业双关待术语核对；序号统一 |
| entry-01262 | pending：`Gaustadnes` 漏译 `-nes`；pending：是否为对 ToME 像素画师的致敬 | 需专名/彩蛋依据才能定 |
| entry-01263 | confirmed：格式与年份无问题。advisory：“先觉/察觉”双关译法可议 | 无必办项 |
| entry-01267 | confirmed：正文标题把 `Tract` 错成“治”并与系列译法冲突。refuted：“拾取名与打开名不一致”的说法；refuted：“无序之治”逻辑自相矛盾 | 统一系列译名，标题按 `Tract` 更正 |

译文未修改。两处 refuted 是对 Gemini 严重程度与连锁推断的下修，原样转录。

## batch-042 八处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-041-01.md](reports/sol-041-01.md)。译文未修改。共 29 个 claim：20 confirmed、5 advisory、2 refuted、2 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01270 | confirmed：娜迦赞叹句语气失真；confirmed：“Temple of Creation”术语不一致；confirmed：“变的”应为“变得” | 术语对齐 + 改“得” |
| entry-01271 | confirmed：漏掉德斯镇；confirmed：递进结构被打乱并加入原文没有的描写；confirmed：“挥舞的獠牙”误写动作；confirmed：“让传说延续”被改成“让生物繁衍” | 补地名、按原文结构重写 |
| entry-01272 | confirmed：Old Forest 专名偏离；confirmed：巨蚁始祖被实质改写；confirmed：外观与群体动作被改写；confirmed：漏译 `Such pluck and derring-do!`。advisory：自然段被拆分 | 专名与句法按源码回改 |
| entry-01273 | confirmed：无依据加入“巨鸟”且“煽动”用字错误；confirmed：“去他妈的”加入原文没有的粗口。advisory：“加急快递”现代口吻；advisory：两处段落拆分 | 删增饰与粗口，口吻取舍 |
| entry-01275 | confirmed：`nice and big` 误成“又大又美”；confirmed：触手代词及动作有偏差。advisory：内心独白拆成三段 | 重译该句、代词回正 |
| entry-01277 | advisory：“profits”财富意象被抹平。pending：罗尔夫是否确定是矮人、是否 profits/prophets 双关 | 双关需彩蛋/设定依据 |
| entry-01278 | confirmed：旁注改成煽情式“永远团聚”；confirmed：`half-gone` 译“神智尽失”程度过重。refuted：并非完全抹掉“两人合为怪物”机制 | 改回客观旁注、收束程度词 |
| entry-01280 | confirmed：“一个世纪”意象被改写；confirmed：`Am I alone?` 误作“我是独一无二的吗”；confirmed：两处“的”应为“地”。refuted：并非“极长时间→极短一瞬”完全反转。pending：`Alor?` 处理为“阿洛”是否正确 | 改问句与助词；专名与反转程度按收窄意见处理 |

译文未修改。两处 refuted 是对 Gemini 反转/机制推断的下修，原样转录。

## batch-043 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-042-01.md](reports/sol-042-01.md)。译文未修改。共 16 个 claim：13 confirmed、3 advisory、无 refuted/pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01282 | confirmed：`were responsible` 译成“其他创造者也很负责”；confirmed：`we halflings` 仅译“我们”丢失族称。advisory：`the same god` 译“同一个上帝” | 改动词结构、补“我们半身人” |
| entry-01283 | confirmed：遗漏 `slimly seen` 月相意象；confirmed：`walk abroad` 理解与两处 `Aye` 遗漏（核心语义）；confirmed：`moonsister` 增译“月亮女神”。advisory：叹词风格 | 补月相与叹词，`moonsister` 回到“月 Sister/月姊妹”一类 |
| entry-01286 | confirmed：七处——增添“刚睡醒的脑袋仍然一团浆糊”；`beyond the red star` 译“红色星星的上方”；`keep it held together` 译“将他们固定在一起”；`the lovely moonstone` 误作复数；`I shall wake up from` 译“我早该……醒来”；增添“该死的戒指”；`lava spilled up` 译“岩浆的波浪浮浮沉沉” | 逐句按源码回改，删除两处增译 |
| entry-01290 | confirmed：`Cataclysm` 译“大爆炸”，与 `Spellblaze` 混淆（应为“大灾变”）。advisory：`spellhunters` 译“猎魔者”易与 demon 混淆 | 事件名回“大灾变”；猎称按术语统一 |

译文未修改。

## batch-044 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-043-01.md](reports/sol-043-01.md)。译文未修改。共 20 个 claim：10 confirmed、5 pending、4 advisory、1 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01292 | confirmed：末尾换行差异；confirmed：“勇者图库纳”“公正之王托拉克”有上下文依据；confirmed：无占位符缺失。pending：与现行第一章译法是否完全一致；pending：术语是否均符合术语表。advisory：`enlisted the aid of sorcerers` 译“雇佣了一些术士” | 与第一章逐条对照 + 术语核对 |
| entry-01294 | confirmed：`physical suffering` 译“物理抵抗能力”；confirmed：`halls of stone` 译“石头洞穴”弱化意象；confirmed：段落与格式无异常。pending：钢铁王座、斯莱特、沃瑞钽等是否符合术语库 | 修措辞；术语待核 |
| entry-01296 | confirmed：漏译 `or` 且保留 `Shalore` 拉丁拼写；confirmed：内容对应完整。advisory：`arcane arts` 译“魔法”；advisory：引号风格与 entry-01298 不一致。pending：关键事件与专名是否均符合规范 | 补 `or`、统一引号风格 |
| entry-01298 | confirmed：`Thalore` 与 `Thaloren` 是同一种族的不同形式。refuted：“木精灵脱离官方源码既有用法”不成立。advisory：会让读者误以为存在两个分支。pending：“木精灵”是否全库仅此一处 | 分支指称需全库核对后再定 |

译文未修改。refuted 项是对 Gemini 术语推断的下修，原样转录。

## batch-045 两处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-044-01.md](reports/sol-044-01.md)。译文未修改。共 10 个 claim：8 confirmed、2 pending、无 refuted/advisory。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01302 | confirmed：`careful inscription` 误作“管理符文”；confirmed：`patient study` 与 `if properly motivated` 语义漂移；confirmed：`Conclave's Overseers` 译“孔克雷夫的长老会”缺乏依据；confirmed：`hijacked shipment of grain` 过度具体化为“满载粮食的货船被劫”；confirmed：无占位符、五段结构对应。pending：「全部专名均符合规范」中“埃尔瓦拉”在本批术语快照无记录 | 逐句按源码回改；埃尔瓦拉查术语记录 |
| entry-01306 | confirmed：`Other theories hold weight though` 判断谓语漏译；confirmed：`academic circles` 缩窄为“考古界”；confirmed：`crucible` 修饰语被省略。pending：`crucible` 具体译法 | 补谓语、放宽学界范围；`crucible` 译法定夺 |

译文未修改。Sol 同时确认了 Gemini 的正面项（占位符与结构），原样记录。

## batch-046 七处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-045-01.md](reports/sol-045-01.md)。译文未修改。按叶子 claim 共 27 条：23 confirmed、2 advisory、1 refuted、1 pending（Sol 自报“问题类 confirmed 20 项”，差额是 3 条正面确认）。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01308 | confirmed×4：`communities` 误作“市民”；`move faster` 重复翻译；`towards the end of` 漏译；`swinging` 漏译 | 逐句回改 |
| entry-01310 | confirmed×3：“另人难以置信”错别字；`those` 指代误读；`borne purely from … delusions` 语义重心变化 | 改错别字、恢复指代 |
| entry-01312 | confirmed×4：`children grew diseased` 语法误读；`renowned` 被加“臭名昭著”；`zeal` 误作“问心无愧”；`to Nature` 漏译 | 逐句回改 |
| entry-01313 | confirmed×5：`otherworldly` 漏译；`peripheral vision` 泛化；`flicker in and out` 误作“飞舞”；`lucid` 漏译（有设定呼应）；`On a whim` 漏译。advisory：无源省略号。refuted：Gemini 称 `Lucid Dreamer` 是“被动天赋” | 补漏译；不要把“被动天赋”写进裁决依据 |
| entry-01314 | confirmed：`Love, Eden` 主客关系改变；confirmed：样式与换行无问题 | 修主客关系 |
| entry-01315 | confirmed：“防火胶布”加入源码没有的物件类型；confirmed：`luminous horror dust` 用冻结术语；confirmed：清单缩进与样式完整。advisory：截断破折号改双侧包裹。pending：“法罗的灰烬”是否固定译名 | 删臆造物件；查“法罗”术语记录 |
| entry-01316 | confirmed：`arcane abilities` 译“奥术能量”；confirmed：其余核心词义与排版无异常 | 视术语决定是否改 |

译文未修改。1 条 refuted 是对 Gemini 机制归因的下修，原样转录。

## batch-047 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-046-01.md](reports/sol-046-01.md)。译文未修改。共 23 个 claim：15 confirmed、4 advisory、2 refuted、2 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01317 | confirmed：并列意象被大幅扩写；confirmed：“大多数人”缩窄成“许多年轻人”；confirmed：`before all` 误作“前所未有”；confirmed：`too many` 改第二人称并增义。refuted：“他的主人”并未把英雄误认成另一位主人 | 扩写与范围词回改；身份解释不要写进修复理由 |
| entry-01318 | confirmed：`fair game`→“公平竞赛”；confirmed：`a few decades`→“一些时代”；confirmed：`once in a while`→“总有一天”；confirmed：烤雪人餐厅句增“只有我们”；confirmed：单数 benefactor 译成复数；confirmed：“被限制在于”句法杂糅。advisory：`Thank me later`→“一会儿谢”生硬 | 六处按源码回改 |
| entry-01319 | confirmed：`won’t claim me today` 决意语气丢失。advisory：粗体句点移到标记外；advisory：诗歌标点体例风格化。pending：“斯派德”跨条目一致性结论 | 诗文本身不判错；一致性另取冻结样本 |
| entry-01320 | confirmed：末句 `manage/corruption` 被曲解；confirmed：同句“它／他”指代不统一；confirmed：`trivial` 误作“太次”。refuted：Gemini 对“他无法施法，只能发出名字声音”的剧情解释无源码支持。pending：“太次”是否与红宝石昂贵性直接矛盾 | 改末句与指代；剧情解释不写成事实 |
| entry-01321 | confirmed：`Shellsea` 是前述村庄专名。advisory：诗歌标点前后不统一 | 保留专名；标点按体例统一 |

译文未修改。2 条 refuted 是对 Gemini 过度推断的下修，原样转录。

## batch-048 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-047-01.md](reports/sol-047-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、无 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01326 | confirmed：前两处分隔符后各多一个空行，第三处没有（源码每处只一空行） | 是否要求三处分段严格统一，低优先级 |
| entry-01328 | confirmed：`giant worms` 译“巨型沙龙”混淆 worm/wyrm；confirmed：破坏诗中龙／虫对照。pending：同 section 另两处已译“沙虫”“传奇巨虫”的附加论据（冻结输入未收录那两处） | 改“巨型沙虫”；附加论据需主流程另取冻结文本 |
| entry-01331 | advisory：外层直单引号被改成中文双引号，冻结语境本身风格混杂 | 若要统一引号，作为整个 section 的独立排版决策 |
| entry-01333 | confirmed×4：`made the Sun from his breath` 漏“创造太阳”；`fled before his glory` 反向译成“慑服”；`All that this light touches shall be mine` 所有权宣告遗漏；`his might surpassed all else` 窄化为“勇武震慑众人”。Sol 建议整句重译 | 按源码整段重译，不逐词补丁 |
| entry-01334 | advisory：外层中文双引号与内部半角双引号形成嵌套 | 统一嵌套引号规则后再处理，不升级为正确性问题 |

译文未修改。

## batch-049 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-048-01.md](reports/sol-048-01.md)。译文未修改。共 5 个 claim：4 confirmed、1 pending、无 refuted/advisory。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01347 | confirmed：“再告诉孩子们我爱他们。”后多一个空行（源码单换行）。Sol 建议按排版 advisory 处理，因该处正是话题转换、中文分段有可读性 | 项目若要求严格换行则删空行，否则可保留 |
| entry-01382 | confirmed：漏译 `A few Sun Paladins made it there with you.`，丢失“太阳骑士与你一同抵达”的剧情关系 | 补回该层意思，句式可调 |
| entry-01384 | confirmed：“你来的太晚了”应为“来得”；confirmed：`the sorcerers` 由执行链确认特指 Elandar 与 Argoniel。pending：同任务后文是否统一译“巫师们”（冻结输入未含 `mod-tome.lua:20180-20181` 目标译文） | 改“得”；称谓一致性需另取冻结译文再定 |

译文未修改。Sol 明确 `confirmed` 只代表 claim 事实成立、不代表严重度。

## batch-050 十处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-049-01.md](reports/sol-049-01.md)。译文未修改。共 17 个 claim：12 confirmed、4 advisory、1 pending、0 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01385 | confirmed：“到达”弱化 `go back to` 的返回方向；confirmed：遗漏 `*MUST*` 强调 | 改回“返回”、补强调 |
| entry-01386 | confirmed：`departed` 错成“被驱散了” | 改“已离开/已离去” |
| entry-01389 | confirmed：原文无句尾波浪号，译文凭空加“～”。advisory：波浪号是否符合该任务语域 | 删“～”，语域整体定 |
| entry-01391 | confirmed：“不断有”强化 `from time to time` 频率。advisory：“已被尘封已久”语病 | 改“时有”、修语病 |
| entry-01392 | confirmed：增加“比较”弱化肯定程度。advisory：“牛 X”属粗俗网络俚语 | 去“比较”、换俚语 |
| entry-01400 | confirmed：`false one` 误成“错的水晶球”，未表达蓄意造假/掉包。pending：`demonic plane` 是否必须统一“恶魔位面” | 改“假冒的水晶球”类；位面术语待核 |
| entry-01408 | confirmed：`Orc Pride` 错用“兽人军团”；confirmed：`vanquished` 译“征服了”不符实际行动 | 回“兽人部落/氏族”与“击败/覆灭” |
| entry-01409 | advisory：`bend the world to their will` 译“扭曲这个世界”改变强调重点 | 文风取舍 |
| entry-01410 | confirmed：`the peak` 错译“塔顶”；confirmed：`orbs of command` 译“指令水晶”遗漏 `orb` 实体 | 改“峰顶”与“宝珠”类 |
| entry-01424 | confirmed：遗漏主要谓语 `protect her` | 补谓语 |

译文未修改。Sol 汇总与其逐条一致（12/4/1/0）。

## batch-051 六处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-050-01.md](reports/sol-050-01.md)。译文未修改。共 13 个 claim：6 confirmed、3 pending、3 advisory、1 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01432 | refuted：“目的从句被实质误译”不成立。advisory：“他让”生硬并引入未明确的性别代词。pending：“他让”是否是“好让”错字 | 只按错字/语感处理，不按实质误译改写 |
| entry-01438 | confirmed：`gems` 译“珠宝”不精确；confirmed：`ancient tome` 译“旧书”弱化年代与典籍感。pending：与第 20466 行“宝石的力量”是否统一 | 改“宝石”“古老典籍”；一致性核后定 |
| entry-01450 | advisory：“直到鲜血流清”直译感。pending：英文是否必然理解为战至血流尽 | 需上下文/设定依据再定 |
| entry-01462 | confirmed：“一队兽人小队”量词重复 | 去重复 |
| entry-01463 | confirmed×3：`asked about` 误成“从你那里得知了消息”；兽人接触前已知法杖并直接索要；与“你什么也没告诉他们”冲突 | 按“盘问/索取”重译，修复逻辑冲突 |
| entry-01464 | advisory：“辐射出的力量和危险”直译腔 | 文风取舍 |

译文未修改。1 条 refuted 是对 Gemini 实质误译定性的下修，原样转录。

## batch-052 八处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-051-01.md](reports/sol-051-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 refuted、0 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01468 | confirmed：`Let nothing stop you.` 译“不惜一切代价冲出去”多出代价与突围两层含义 | 是否接受戏剧化意译；忠实版“别让任何东西阻挡你” |
| entry-01474 | confirmed：`carve a place for yourself` 译“找到属于自己的栖息地”，应为在世上谋得一席之地。advisory：原文两句被逗号连接 | 改“在这个世界谋得一席之地”；可顺带断句 |
| entry-01479 | confirmed：`far west` 被“远一点的西面”弱化 | 改“德斯镇遥远的西面” |
| entry-01482 | advisory：省略 `Upon arrival`；前句已交代抵达，无实质 completeness 问题 | 可选补“刚抵达时” |
| entry-01486 | confirmed：`his side of the story` 误成“关于他的故事”，削弱双方各执一词结构 | 改“他这一方的说法” |
| entry-01491 | confirmed：`randomly attacks villagers` 强化成“肆意屠杀村民的凶手” | 收束为“会随机袭击村民”或保留戏剧化 |
| entry-01496 | refuted：`The portal is done!` 译“传送门已经开启”**不成立**，源码显示 done 后即 functional 可用；Sol 另注 Gemini 行号 `:75` 应为 `:80` | 无必办；严格贴字才改“传送门完成了” |
| entry-01498 | confirmed：寻找线索的动作关系被颠倒（应先找到传送门进入远东，再调查线索）；confirmed：同一 `far east` 被译成两个地理称呼。Sol 另注 Gemini 行号 `:24` 应为 `:26` | 调整行动顺序句；统一地名 |

译文未修改。1 条 refuted 是对 Gemini 场景判断的下修，原样转录。

## batch-053 十四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-052-01.md](reports/sol-052-01.md)。译文未修改。共 35 个 claim：20 confirmed、10 advisory、3 refuted、2 pending。本轮以占位符/机制核对为主。

| 条目 | Sol 分档要点 |
| --- | --- |
| entry-01508 | confirmed：8 个占位符正确。advisory：句号与斜杠空格不统一 |
| entry-01509 | confirmed：两个 `%d` 正确；confirmed：机制为“先清当前赞歌类型全部 cross-tier 效果，再随机清最多 `%d` 个同类型普通负面状态”。refuted：Gemini 称括号补充“不影响实质机制理解”过于乐观 |
| entry-01510 | confirmed：三个 `%d` 顺序正确。advisory：末句另起一行 |
| entry-01512 | confirmed：`%0.1f`/`%d` 对齐；confirmed：版本差异属实——“强化护盾持续至少 2 回合”在冻结英文与译文都缺（源码 `shield.dur = math.max(2, shield.dur)`） |
| entry-01514 | confirmed：四占位符正确。advisory：首行缺句末标点、未保留英文括号 |
| entry-01516 | confirmed：三个 `%d%%` 对应正确。advisory：`%d%% , 持续` 逗号空格不规范 |
| entry-01517 | confirmed：四占位符正确。advisory：逗号前多余空格；advisory：“灼烧痕迹”未体现独立 `EFF_LIGHTBURN` 状态（无权威中文名） |
| entry-01518 | confirmed：两个 `%d%%` 对应半径1/2 伤害；advisory：两行合一行无遗漏。refuted：Gemini 称 4 级护盾“对齐无误”不准确，实为 `cancel_damage_chance = 100` 免疫所有伤害 |
| entry-01528 | confirmed：五占位符与颜色标签正确。advisory：补句号与“圣印”后缀属可接受整理 |
| entry-01531 | confirmed：改写语义等价，正确源码 `guardian.lua:183-203`（Gemini 写成 `:149`）。pending：`Crusade` 是否已定名“十字军打击” |
| entry-01534 | confirmed：四占位符正确；confirmed：`HEALING_POWER` 治疗+护盾+至少2回合+20次移除。advisory：英文无句号中文补句号 |
| entry-01536 | confirmed：四占位符正确；confirmed：`blindness resistance`→“免疫”符合 `blind_immune`。refuted：把 `normal light` 限定为“灯具”不准确（实为 `self.lite` vs `radiance_aura`）。pending：“光系伤害亲和/吸收”术语裁决 |
| entry-01543 | confirmed：源码为感叹号版本且位置 `twilight.lua:215-219`；confirmed：与术语快照句号规则不一致。advisory：仅标点差异 |
| entry-01554 之外的 entry-01544 | confirmed：采用第二座跃迁门实际子技能有源码依据；confirmed：`%d` 对应该子技能有效距离 |

译文未修改。3 条 refuted 与 2 条 pending 均原样转录；多处 Gemini 行号被 Sol 校正。

## batch-054 五处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-053-01.md](reports/sol-053-01.md)。译文未修改。共 10 个 claim：7 confirmed、2 advisory、1 pending、0 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01554 | confirmed：占位符及顺序正确；confirmed：末句把特定 `Shoot` 天赋泛化为“远程攻击”。advisory：“守卫伤害降低”译“灵矢伤害降低”但当前行为等价 | 是否恢复天赋名 |
| entry-01557 | confirmed：增译“你的”并漏 `threads` 意象。pending：Gemini 所举 Spin Fate 叠加“命运之丝”例证 | 补 threads 意象；例证需另取冻结文本 |
| entry-01563 | confirmed：三占位符正确；confirmed：“释放  ，”含两个多余半角空格 | 删空格 |
| entry-01565 | confirmed：时间回溯点被译成空间“地方” | 改“时点/时刻”类 |
| entry-01576 | confirmed：数值占位符正确。advisory：原文无“码”，译文额外指定单位 | 是否补单位属风格 |

## batch-055 四处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-054-01.md](reports/sol-054-01.md)。译文未修改。共 9 个 claim：5 confirmed、2 advisory、1 pending、1 refuted。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01586 | confirmed：现译与固定简中译名不一致（Epoch→纪元）。pending：是否必然指同名专名实体、必须音译“亚伯契” | 术语核对后再定音译 |
| entry-01588 | confirmed：省略 weave matter 动作及与技能名的呼应；confirmed：护甲/震慑免疫/流血免疫与机制吻合。advisory：`Magic` 译“魔力值” | 补呼应；`Magic` 译法待术语 |
| entry-01605 | confirmed：漏译 `(warp)`／“（扭曲）”。refuted：末句省略“时空地雷的”主语构成漏译不成立 | 补 warp；不按漏译改主语 |
| entry-01617 | confirmed：占位符正确。advisory：与同系三条 spellbound 译法不一致（事实已证实） | 是否统一系内译法 |

## batch-056 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-055-01.md](reports/sol-055-01.md)。译文未修改。共 8 个 claim：7 confirmed、1 refuted、0 advisory/pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01625 | confirmed：“你猎犬”缺“的”；confirmed：遗漏 `Upon activation`；confirmed：占位符与百分号格式正确。refuted：“将在 %d 回合内召唤”应改“%d 回合后”不成立 | 补“的”与激活条件；回合措辞不改 |
| entry-01659 | confirmed：“%d 码球形范围”误用单位并遗漏半径概念；confirmed：占位符数量和顺序正确 | 改为“半径 %d 码”类表述 |
| entry-01661 | confirmed：`carrion worm mass` 未统一“腐肉虫群”；confirmed：占位符正确、第五参数未被文本消费 | 按术语统一；死参数说明记录即可 |

## batch-057 三处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-056-01.md](reports/sol-056-01.md)。译文未修改。共 5 个 claim：2 confirmed、2 advisory、1 refuted、0 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01689 | advisory：条目结论仅属排版/风格 | 无必办项 |
| entry-01700 | advisory：条目结论仅属排版/风格 | 无必办项 |
| entry-01703 | confirmed：钩爪追加的是流血与中毒效果；confirmed：把 `physical` 写成“流血伤害”遗漏实际伤害类型。refuted：`nature` 被写成“自然毒素伤害”**并非“完全丢失”自然伤害类型**（Sol 注措辞仍属 advisory） | 按伤害类型表回改措辞 |

译文未修改。refuted 是对 Gemini 表述强度的下修，原样转录。

## batch-058 八处交叉结果

作者是 Codex/gpt-5.6-sol/medium。主代理只转录。完整文本见 [sol-057-01.md](reports/sol-057-01.md)。译文未修改。共 13 个 claim：10 confirmed、2 advisory、1 refuted、0 pending。

| 条目 | Sol 分档 | 人工待决 |
| --- | --- | --- |
| entry-01706 / 01709 / 01711 / 01718 / 01727 | 各 1 条 confirmed（条目结论成立） | 按 Gemini 原报告逐条修；完整措辞见报告 |
| entry-01732 | confirmed×3：漏掉致命毒素增强及触发关系；漏掉 `earth-based poison`；第二个 `%d` 缺每回合伤害单位。advisory：每轮／回合混用 | 按源码补效果与单位；统一用词 |
| entry-01740 | confirmed：`%d` 与 `%s` 拼接产生双空格；confirmed：action 被缩窄为技能 | 修空格；放宽措辞 |
| entry-01742 | refuted：“漏掉 `+` 导致数值机制缺失”不成立。advisory：省略 power 字样 | 不按漏机制改；power 字样可选 |

译文未修改。1 条 refuted 是对 Gemini 机制推断的下修，原样转录。
