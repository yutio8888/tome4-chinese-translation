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
