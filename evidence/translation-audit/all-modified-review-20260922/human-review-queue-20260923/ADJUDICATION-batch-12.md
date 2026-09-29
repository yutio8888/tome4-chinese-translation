# 批阅裁决台账 — batch-12

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`2bb01f112eb875fcdb4b8bba1019221f71697073d8bb274da870a55498597f5f`
- 决策行：40；冻结修订（含孪生载体）：39
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 36 |
| deferred | 3 |

## 被驳回／未采纳的模型主张

| entry | 模型主张 | 裁决 | 理由 |
| --- | --- | --- | --- |
| entry-00244 | 去掉 ` area effect` 的前导空格造成中文拼接缺陷 | rejected | 模型主张补回空格。固定源码 MapEffects.lua:23 为 `dam_def.name .. _t" area effect"` 直接拼接，补空格会显示「火焰 范围效果」，反证模型建议有害。 |
| entry-00221 | 「离开地图」构成明显误译 | rejected | 模型自标 advisory。源码 Game.lua:926-936 的 can_change_level 阻止任何换层/换区域，「离开地图」覆盖该限制，功能含义正确；level/zone 统一译法属跨条目策略，非本条缺陷。 |
| entry-00345 | 「使这次攻击发生偏斜」弱化招架，应改「招架」 | rejected | 模型自标 advisory。源码确认招架成功挡住攻击，现译保留防御成功含义，属文风偏好，不构成缺陷。 |
| entry-00185 | 方括号内多空格 | rejected | 模型自标 advisory。用户策略明确纯静态排版不算缺陷；方括号不属「括号不一致」策略范围。 |
| entry-00254 | 「最大 50%」与同组「最大40%」排版不一致 | rejected | 模型自标 advisory；仅为数字前空格差异，属纯静态排版，按用户策略不整理。 |
| entry-00419 | 「超过1500点」与同组「超过 600 点」空格不一致 | rejected | 模型自标 advisory；纯静态排版差异，按用户策略不整理。 |
| entry-00428 | 三扇传送门句式与同系列不平行 | rejected | 模型自标 advisory；条件、数量、机制均正确，句式平行属文风偏好。 |
| entry-00334 | 「杀死」应为「击杀」 | rejected | 模型自标 advisory；日志在敌人 on_die 中输出，「杀死」与触发事实一致，击杀仅为界面习惯差异。 |
| entry-00434 | 「珠宝匠托付」应改为更贴近源码关系 | rejected | 模型自标 advisory；Master Jeweler 对应珠宝匠，译文为可接受意译，任务名已增补，无缺陷。 |
| entry-00393 | 复合后缀外层半角括号 | rejected_on_entry | 本条 entry-00393 本身已是全角；模型所指的半角外层括号实际出现在 entry-00395–00400（同一 hrq-00046 行的其他载体），已按 bracket_fullwidth 修复那些载体。 |
| entry-00184 | 「勇敢的向前」语病、段间缺空行 | accepted_upstream | 缺陷成立，但主工作区 HEAD 11b3e963 已修（已核逐字）。按 SPEC 规则不在本 worktree 重复修改，记 defer；不接受在本分支重复改。 |

## 逐条裁决

| queue_id | entry_id | 文件:行 | 模型意见 | ORCHESTRATOR 裁决 | 是否落实 | 理由 |
| --- | --- | --- | --- | --- | --- | --- |
| hrq-00452 | entry-02849 | mod-tome.lua:37431 | fix | accepted | 是 | 独立核验通过；采纳：宿主 physical.lua:2531-2533 为 ("...taking %0.2f physical damage %s"):tformat(eff.dam, ravaged)，本地化宿主 mod-tome.lua:37433 以 {2,1} 把片段置于“受到”之前，自带句号使界面显示“目标被疯狂扭曲，每回合。受到 X 物理伤害”，句中断句是客观拼接缺陷。删去片段句号即修复；句末句号应由宿主模板（冻结外 mod-tome. |
| hrq-00453 | entry-02850 | mod-tome.lua:37432 | defer | deferred | 否 | 逐条回应：①“无依据加入每回合”refuted 同意驳回——on_timeout（physical.lua:2541-2566）每回合执行一次 dispel，“每回合”符合实现且原文 turn 即此义；②未涵盖维持战技 advisory 驳回——英文原文亦只说 physical effect，译文忠于原文，扩写属上游文本问题；③缺句末标点成立，但本片段被宿主以 {2,1} 重排到句中（mod-tome.lua:37433），片段不能自带 |
| hrq-00454 | entry-02856 | mod-tome.lua:37514 | fix | accepted | 是 | 独立核验通过；采纳 defiantly 漏译：physical.lua:2881 on_gain 原文带 defiantly，补“倔强地”。Gemini“语序顺畅”判断驳回，但 %s 由 string.his_her 提供（engine utils.lua:939-944），zh 下 his→“他的”、its→“它的”、her→“她”（engine.lua:1405-1407，her 与宾格共用键无“的”），任何把 %s 挪到“与自然的联系”前的重排 |
| hrq-00455 | entry-02858 | mod-tome.lua:37532 | fix | accepted | 是 | 独立核验通过；采纳：physical.lua:3045 原文 stands strong 指挺立不倒，“十分强大”语义偏移；两个 %0.1f%% 依次对应全体抗性与抗性上限，顺序无误保持；半角逗号改全角。 |
| hrq-00456 | entry-02866 | mod-tome.lua:37558 | fix | accepted | 是 | 独立核验通过；采纳：同效果 PARASITIC_LEECHES 名称与描述均译“寄生水蛭”（mod-tome.lua:37553-37557），本条“寄生虫”同族不一致；Some 在源码中对应脱落的一堆水蛭（physical.lua:3190-3200,3210-3223），补“一些”；%s 为角色名，“从%s身上脱落”更准确。 |
| hrq-00457 | entry-02891 | mod-tome.lua:37712 | no_change | accepted | 否 | 无需修改；advisory 驳回：#OLIVE_DRAB# 后空格源自英文原文，属纯静态排版，按用户策略不整理；两个 %s 与 #LAST# 结构完好（physical.lua:4174）。 |
| hrq-00458 | entry-02921 | mod-tome.lua:37978 | fix | accepted | 是 | 独立核验通过；采纳：arena/zone.lua:405 game.log 四项奖励同构，现译前三处半角“! ”末处全角“！”，同一中文句中标点混用属标点错误，统一为全角“！”（去掉仅为半角惯例而加的空格）；13 个 %s 与颜色参数顺序不变。 |
| hrq-00459 | entry-02927 | mod-tome.lua:38083 | fix | accepted | 是 | 独立核验通过；采纳：charred-scar/npcs.lua:107 doEmote 以玩家名填 %s；“去吧%s!”半角叹号与后半全角混用，改“去吧，%s！”（补呼语逗号），%s 位置功能不变。 |
| hrq-00460 | entry-02929 | mod-tome.lua:38122 | fix | accepted | 是 | 独立核验通过；采纳：conclave-vault/npcs.lua:62-63 同实体描述为 huge mass of deformed flesh，本仓描述译“这团巨大的畸形血肉”（mod-tome.lua:38123）；“碎肉”（本仓用于 gore/guts）与一整团活体血肉形态不符，改“肉团”；degenerated→“退化的”保留。 |
| hrq-00461 | entry-02937 | mod-tome.lua:38228 | no_change | accepted | 否 | 无需修改；advisory 驳回：BOOM! 为 daikara 火山喷发弹窗标题，“火山喷发！”与紧随正文一致，仅损拟声感，属文风，非缺陷。 |
| hrq-00462 | entry-02957 | mod-tome.lua:38422 | fix | accepted | 是 | 独立核验通过；采纳：现译“??？”两半角一全角混用属标点错误。本仓其余 ??? 条目均保持半角（mod-tome.lua:20245、36919、42833），统一为半角“???”以与原文及族内一致。 |
| hrq-00463 | entry-02967 | mod-tome.lua:38557 | fix | accepted | 是 | 独立核验通过；采纳：PAIN GIVING SUBMODULES 为“施加痛苦的子模块”，“痛苦强化”把施痛改成强化，语义偏移且丢 sub-；改“致痛子模块”。纯喊话无机制影响。 |
| hrq-00464 | entry-02973 | mod-tome.lua:38568 | fix | accepted | 是 | 独立核验通过；采纳：原文 managed to deal a crippling blow by killing their leader，现译只剩“使首领走向死亡”，漏掉对兽人的重创这一结果；补“给了对方沉重一击”，并把“使…走向死亡”改为直接的“杀死了”。首行与 \n 保持不变；Garkul、Age of Pyre 沿用本仓译名。 |
| hrq-00465 | entry-02982 | mod-tome.lua:38735 | defer | deferred | 否 | 专名不一致成立但不可单改：原文 A farportal is a way… 这一描述族在本仓约 10 处（mod-tome.lua:38072、38486、38725、38730、38735、39362、39720、39793、40331、tome-orcs.lua:6936）统一以“传送门是…”起句，仅改本条会制造族内不一致，按判据 7 记 defer，需整族统一为“远行传送门”。连续“似乎”advisory 驳回：源自原文 seem |
| hrq-00466 | entry-03023 | mod-tome.lua:39312 | fix | accepted | 是 | 独立核验通过；采纳：terminology/society.tsv:30 Epoch→亚伯契 为 preferred（T.PN.PERSON，注明同名天赋与神器 Epoch's Curve 均沿用音译，不按“纪元”处理），必须采用；同仓天赋名 mod-tome.lua:22102 已为“亚伯契”。 |
| hrq-00467 | entry-03025 | mod-tome.lua:39318 | fix | accepted | 是 | 独立核验通过；采纳：同 society.tsv:30 preferred 注释点名 Epoch's Curve 沿用音译，“纪元之弧”违反 preferred。改“亚伯契之弧”，只替换专名、保留现译“之弧”，“的弧线/之弧”措辞属文风。 |
| hrq-00468 | entry-03027 | mod-tome.lua:39320 | fix | accepted | 是 | 独立核验通过；采纳：描述正文复述神器名，必须与 entry-03025 同步为“亚伯契之弧”，否则名称与说明不一致；其余正文不动。 |
| hrq-00469 | entry-03058 | mod-tome.lua:39725 | fix | accepted | 是 | 独立核验通过；两条 claim 均采纳：shertul-fortress/grids.lua:120-124 传送至 Caldizar 堡垒，原文 strangely familiar；后续 shertul-fortress-caldizar/zone.lua:74 又写“熟悉却又不同”，strangely 是铺垫的反差，现译只剩“熟悉”漏掉。补“莫名”→“一个莫名熟悉的地方”；hrq-00469（漏译）与 hrq-00470（弱化反差）以同一处修改 |
| hrq-00471 | entry-03092 | mod-tome.lua:40038 | fix | accepted | 是 | 独立核验通过；采纳：同 section mod-tome.lua:40037、40046、40048 均将 Telos 译“泰勒斯”，本仓“泰勒斯”共 18 处；本条“泰勒”同节专名不一致，改“泰勒斯”。“旧日的力量之所”保留。 |
| hrq-00472 | entry-03112 | mod-tome.lua:40275 | no_change | accepted | 否 | 无需修改；驳回：terminology/places.tsv:7 Swordsmith→长剑铁匠铺 仅为 existing，不强制改名；本仓 mod-tome.lua 5 处与 tome-cults.lua 2 处 Swordsmith 实体名全部统一为“铸剑铺”，单改本条反而制造不一致。 |
| hrq-00473 | entry-03114 | mod-tome.lua:40313 | no_change | accepted | 否 | 无需修改；驳回：同 entry-03112，术语为 existing 不强制，“铸剑铺”全库统一，单改会制造不一致。 |
| hrq-00474 | entry-03118 | mod-tome.lua:40361 | no_change | accepted | 否 | 无需修改；细微观察同意保留：店名为字面招牌（实售纹身，源码 store 绑定），“萨拉的草药浸剂店”直译招牌，与 mod-tome.lua:40509、tome-orcs.lua:6994 同名店一致；无术语条目，不改。 |
| hrq-00475 | entry-03122 | mod-tome.lua:40403 | no_change | accepted | 否 | 无需修改；驳回：同 entry-03112，术语为 existing 不强制，“铸剑铺”全库统一。 |
| hrq-00476 | entry-03129 | mod-tome.lua:40509 | no_change | accepted | 否 | 无需修改；细微观察同意保留：同 entry-03118，招牌直译且与同名店一致。 |
| hrq-00477 | entry-03137 | mod-tome.lua:40586 | no_change | accepted | 否 | 无需修改；细微观察同意保留：“铸剑铺”全库 7 处统一，术语仅 existing。 |
| hrq-00478 | entry-03139 | mod-tome.lua:40618 | no_change | accepted | 否 | 无需修改；细微观察同意保留：同 entry-03137。 |
| hrq-00479 | entry-03149 | mod-tome.lua:40781 | defer | deferred | 否 | 本条“推挤”与相邻日志 mod-tome.lua:40782“你学会了技能推挤”一致，但与冻结外技能名 mod-tome.lua:27003 “击退攻击”及符文名 40780“启蒙符文：冲撞”三处不一致；无术语条目，单改本条会破坏与日志的一致。记 defer，需统一 27003/40780/40781/40782 的 Shove 译名。句号与引号已正确。 |
| hrq-00480 | entry-03167 | mod-tome.lua:41138 | fix | accepted | 是 | 独立核验通过；采纳：原文 ruled by King Tolak，现译漏“国王”头衔；同节 mod-tome.lua:41146、41148 两条首都描述均为“……的首都，由……统治”句式，改“联合王国首都，由托拉克国王统治”，同时去掉与族内不一致的括号。 |
| hrq-00481 | entry-03735 | tome-orcs.lua:350 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定）：destructicus.lua:44-50 已写面板显示飞船内部，73 行原文并列“透过窗户看见导弹远去”与“在探知面板上看见它迎面冲向画面和惊恐乘客”两视角；现译合成窗外远眺并漏 on the scrying panel。改为“你透过窗户看见导弹离你远去，同时又在面板上看见它迎面冲向画面，冲向那些惊恐的乘客。”，“面板”沿用同 chat 上文译法；其余段落、颜色与 #{italic}# 标记不动。 |
| hrq-00482 | entry-03738 | tome-orcs.lua:410 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定）：john-surrender.lua:97-103 选项原文 alive and broken，现译漏 broken；改“一个活着却已崩溃的你对我更有用”，不限定具体折磨方式；颜色码与方括号不变。 |
| hrq-00483 | entry-03741 | tome-orcs.lua:426 | fix | accepted | 是 | 独立核验通过；advisory 部分采纳（来源未固定，john-worldmap.lua:25-33）：原文 Give it back! DIE!，“拿出来”未表达“归还”且“受死吧！！”多出一个叹号（冗余标点）；改“还给我！受死吧！”。其余标记、@playername@ 与前文不动。 |
| hrq-00484 | entry-03747 | tome-orcs.lua:467 | fix | accepted | 是 | 独立核验通过；advisory 驳回（来源未固定，kaltor-shop.lua:24-31、40-45、66-69）：选项含看货、攻击、不购物，“你要做什么呢？”可覆盖，措辞不改。另修中文句中半角“@playername@! ”为全角“！”（标点错误）；海报内引号与 markup 不动。 |
| hrq-00485 | entry-03748 | tome-orcs.lua:474 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定，kaltor-shop.lua:48-51）：bird's-eye view 与 front-row seat 对比远观与近处目睹，现译“坐在椅子上”丢失 front-row；改“我宁愿在上面鸟瞰你要做的事情，也不想坐在前排近距离观赏”。\t、颜色码与 @playername@ 不变。 |
| hrq-00486 | entry-03772 | tome-orcs.lua:957 | no_change | accepted | 否 | 无需修改；advisory 驳回（来源未固定，sunwall-mage.lua:114-131）：“魔术师”在奇幻语境可泛指施法者，未误指职业或机制；无术语条目，改名属命名风格。 |
| hrq-00487 | entry-03799 | tome-orcs.lua:1499 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定，world-artifacts.lua:142-151,174）：“These boots”指本物品 Anti-Gravity Boots（本仓译“反重力鞋”，描述用“这套鞋子”），“火箭靴”与工匠插件名“%s 火箭靴”（tome-orcs.lua:1381）冲突易误指；fail to operate properly 亦非单纯“失败”。改“这套鞋子有%d%%几率无法正常运作（随灵巧降低）。” |
| hrq-00488 | entry-03801 | tome-orcs.lua:1509 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定，world-artifacts.lua:275-280）：“导致目标被致残毒素”缺谓语，改“使目标感染致残毒素”；args_order {1,2,3,5,4} 与 tformat(range, damage/dur, fail, damage, dur) 对应正确，不动。 |
| hrq-00489 | entry-03807 | tome-orcs.lua:1551 | no_change | accepted | 否 | 无需修改；advisory 驳回（来源未固定，world-artifacts.lua:579-582）：传入 maxp - self.power 为剩余回合，“冷却时间：%d 回合”作状态标签可接受，“冷却中”属精度偏好；括号在本条内一致，不整理。 |
| hrq-00490 | entry-03809 | tome-orcs.lua:1560 | no_change | accepted | 否 | 无需修改；advisory 驳回（来源未固定，world-artifacts.lua:641-646）：“从天空引导”已保留空中方位，airborne 未丢失语义，“空中探针”属措辞偏好。 |
| hrq-00491 | entry-03811 | tome-orcs.lua:1569 | fix | accepted | 是 | 独立核验通过；采纳（来源未固定，world-artifacts.lua:714-720）：tg 以 start_x/start_y=target 为锥形起点，原文 from the target 漏译影响范围理解；shrapnel 为弹片而非“榴弹”。改“从目标处向外迸射弹片，在半径4的锥形范围内…”。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
