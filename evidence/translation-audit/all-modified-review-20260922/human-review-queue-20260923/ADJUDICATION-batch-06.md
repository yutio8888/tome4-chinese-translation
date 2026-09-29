# 批阅裁决台账 — batch-06

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`ebfa6fbaeb8651c3e9d2c28081c071e5616f6f04b64840e3b8614b4b5df68837`
- 决策行：40；冻结修订（含孪生载体）：40
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 40 |

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
| hrq-00212 | entry-01333 | mod-tome.lua:19365 | fix | accepted | 是 | 独立核验通过；按用户提示整段重译。最强反证：petty gods 按术语库 preferred 已译“伪神”，保留；但 fled before his glory 是逃散而非“慑服”，方向相反；made the Sun from his breath 是以气息造出太阳，现译“深呼吸后把太阳举起”丢了创造；All that this light touches shall be mine 的所有权宣告被改成“即我所至”；his might surpas |
| hrq-00213 | entry-01334 | mod-tome.lua:19370 | no_change | accepted | 否 | 无需修改；外层直引号换成中文双引号只是引文呈现方式，异语音节、内部半角双引号与斜体标签全部保留；嵌套引号体例属 advisory，用户提示不升级为正确性问题。 |
| hrq-00214 | entry-01347 | mod-tome.lua:19639 | no_change | accepted | 否 | 无需修改；源文首段与第二段之间为单换行，译文多一个空行；这是纯静态分段差异，内容无增减，且本批禁止改变换行序列；先例 hrq-00209 同样不改。 |
| hrq-00215 | entry-01382 | mod-tome.lua:20175 | fix | accepted | 是 | 独立核验通过；现译确实漏掉 A few Sun Paladins made it there with you（是随你一同赶到的几名太阳骑士），且 hold the line at the cost of their lives 被压成“顶在最前线用生命帮你”。补出“与你一同赶到”并按原文拆句；Sun Paladin 按术语库“太阳骑士”。 |
| hrq-00216 | entry-01384 | mod-tome.lua:20177 | fix | accepted | 是 | 独立核验通过；“来的太晚”补语应用“得”，属语法修正，改为“来得太晚”。the sorcerers 指前文要阻止的施法者，“那些法师”已是定指，不构成误译。称谓一致性 claim：本节 logPlayer 两条用“巫师们”，但 high-peak 节与全库 Sorcerers 为 巫师10／法师9 并存，术语库无条目；统一属跨批次策略，未授权，本条不改名。 |
| hrq-00217 | entry-01385 | mod-tome.lua:20178 | fix | accepted | 是 | 独立核验通过；go back to the Far East 是返回，现译“到达”丢失返回方向，改“返回”；*MUST* 在源串中用星号强调，现译无强调，按源串保留星号“*必须*”。远东大陆沿用本仓既有译法。 |
| hrq-00218 | entry-01386 | mod-tome.lua:20179 | fix | accepted | 是 | 独立核验通过；departed 为离开，现译“被驱散”把自行离开改成被动驱散，与同节日志“巫师们已经离开”也矛盾；“终于”无原文依据。改为“及时赶到并打断了仪式，法师们已经离去”。称谓沿用本条原“法师”，统一问题同 hrq-00216。 |
| hrq-00219 | entry-01389 | mod-tome.lua:20192 | fix | accepted | 是 | 独立核验通过；原文句末为句号，“～。”是凭空加入的语气符号且叠用标点，删“～”。整体语域 advisory 不在本条处理。 |
| hrq-00220 | entry-01391 | mod-tome.lua:20194 | fix | accepted | 是 | 独立核验通过；from time to time 是“不时”，现译“不断有”强化频率，属 fidelity 偏差，改“仍不时有”；“已被尘封已久”重复“已”属语病，一并改为“已被尘封许久”。 |
| hrq-00221 | entry-01392 | mod-tome.lua:20195 | fix | accepted | 是 | 独立核验通过；You are great 是肯定，“比较”弱化程度，删除；同句重写时“牛 X”这一粗俗俚语不合任务日志语域，替换为“你很了不起”。None…has come back yet 的 yet 补“至今”，现译“活着回来”增加的“活着”一并去掉。 |
| hrq-00222 | entry-01400 | mod-tome.lua:20216 | fix | accepted | 是 | 独立核验通过；swapped the orb for a false one 是掉包成假货，现译“换了个错的水晶球”未表达蓄意伪造，改“用一个假水晶球掉了包”。demonic plane 改“恶魔位面”的 claim 驳回：术语库无条目，本仓“恶魔空间”28 处、“恶魔位面”2 处，现译顺势对齐为主流“恶魔空间”，不另立新译名。 |
| hrq-00223 | entry-01408 | mod-tome.lua:20263 | fix | accepted | 是 | 独立核验通过；Orc Pride 术语库为“兽人部落”，本仓同名其余 5 处均为“兽人部落”，“兽人军团”造成同族不一致；vanquished the masters 是击败各部落首领（同文件其余处也写 defeated the Sorcerers），“征服”不合，改“击败了兽人部落的首领们”。 |
| hrq-00224 | entry-01409 | mod-tome.lua:20264 | no_change | accepted | 否 | 无需修改；bend the world to their will 是让世界屈从其意志，“妄图扭曲这个世界”侧重不同但仍表达了威胁世界的图谋；模型自标 advisory，用户提示为文风取舍，不构成一级缺陷。 |
| hrq-00225 | entry-01410 | mod-tome.lua:20265 | fix | accepted | 是 | 独立核验通过；the peak 指巅峰（High Peak）这座山峰，“塔顶”错译地点，改“峰顶”；orbs of command 在本仓实体名一律“指令水晶球”（mod-tome.lua:11613-11620、20477），现译“指令水晶”缺“球”造成同族不一致，补齐。 |
| hrq-00226 | entry-01424 | mod-tome.lua:20357 | fix | accepted | 是 | 独立核验通过；现译“没能成功地将她护送出地宫”缺主谓语 protect her，且把失败对象从“保护”改成“护送到位”；改为“你没能在护送她离开这个地宫时保护好她”。crypt 保持同节“地宫”。 |
| hrq-00227 | entry-01432 | mod-tome.lua:20426 | fix | accepted | 是 | 独立核验通过；“目的从句实质误译”的 claim 驳回：so she can come and go freely 的含义现译已表达。“他让”是“好让”的错字，同时引入原文未有的性别代词；按错字改为“好让她能够自由来去”，不做实质改写。 |
| hrq-00228 | entry-01438 | mod-tome.lua:20463 | fix | accepted | 是 | 独立核验通过；gems 在同节日志译“宝石的力量”（mod-tome.lua:20466），本条“珠宝”造成同节不一致且不准确；ancient tome 的“古老典籍”被弱化为“旧书”。改“你发现了一本关于宝石的古籍”。 |
| hrq-00229 | entry-01450 | mod-tome.lua:20566 | no_change | accepted | 否 | 无需修改；任务名 Till the Blood Runs Clear 的确切引申义（战至血尽／冲洗至血色褪去）无源码或设定证据可定；现译“直到鲜血流清”是保守直译，未与同节任何内容矛盾。直译感属二级 advisory；pending claim 缺证据，不据以改名。 |
| hrq-00230 | entry-01462 | mod-tome.lua:20631 | fix | accepted | 是 | 独立核验通过；“一队兽人小队”量词与名词重复，属语病修正；对齐同节孪生分支 mod-tome.lua:20633 句式“当你走出恐惧王座时，你遭到一队兽人伏击”，ambushed 也由“偷袭”改“伏击”与同节一致。 |
| hrq-00231 | entry-01463 | mod-tome.lua:20634 | fix | accepted | 是 | 独立核验通过；They asked about the staff 是兽人向你问起法杖，现译“从你那里得知了法杖的消息”颠倒信息流向，并与同源分支后句 You told them nothing（mod-tome.lua:20636“你什么也没告诉他们”）矛盾；该键在源码第 32、36 行两个分支共用。对齐同节 20632“他们问起了法杖的事”，改为“他们问起了法杖的事，并把它从你手中抢走了”。 |
| hrq-00232 | entry-01464 | mod-tome.lua:20637 | no_change | accepted | 否 | 无需修改；“辐射出的力量和危险”仅有直译感，力量、危险与不敢使用均已表达；模型自标 advisory，属二级文风。 |
| hrq-00233 | entry-01468 | mod-tome.lua:20691 | fix | accepted | 是 | 独立核验通过；源码前一句是你和诺尔甘须赶回钢铁议会报信，Let nothing stop you 是“别让任何东西阻挡你”；现译加入“不惜一切代价”和“冲出去”两层原文没有的含义，后者还把回国报信改成突围。改为忠实版。 |
| hrq-00234 | entry-01474 | mod-tome.lua:20754 | fix | accepted | 是 | 独立核验通过；carve a place for yourself in the world 是在世上为自己谋得一席之地，现译“找到属于自己的栖息地”缩成找住处，且丢了 try 与 in the world；改译并按原文两句断句。 |
| hrq-00235 | entry-01479 | mod-tome.lua:20781 | fix | accepted | 是 | 独立核验通过；far west 是遥远的西面，“远一点的西面”弱化距离；只改该短语，保留同节“在德斯镇……是……”句式。 |
| hrq-00236 | entry-01482 | mod-tome.lua:20800 | no_change | accepted | 否 | 无需修改；最强反证：同节前一条（mod-tome.lua:20799）已写“你经由远行传送门抵达了一处山洞”，本句紧接其后，Upon arrival 的时间承接已由上下文表达；模型自标 advisory，不构成漏译。 |
| hrq-00237 | entry-01486 | mod-tome.lua:20813 | fix | accepted | 是 | 独立核验通过；his side of the story 是萨拉苏尔一方的说法，与前条乌克勒姆斯维奇的指控对立，决定谁堕落正依赖这一对立；“关于他的故事”丢了立场含义。只改该短语，问号保留原文问句。 |
| hrq-00238 | entry-01491 | mod-tome.lua:20857 | fix | accepted | 是 | 独立核验通过；randomly attacks villagers 是随机袭击，现译“肆意屠杀村民的凶手”把袭击强化为屠杀并加了“凶手”定性，属 fidelity 偏差；改为“那头会随机袭击村民的孤狼”。Lone Wolf 按术语库 preferred“孤狼”。 |
| hrq-00239 | entry-01496 | mod-tome.lua:20882 | no_change | accepted | 否 | 无需修改；源码 west-portal.lua:74-80 在放置传送门地形（makeEntityByName cportal）后输出此日志，传送门此时已建成可用，“传送门已经开启”与场景一致；模型已将 claim 标 refuted。Zemekkys 沿用同节“泽梅基斯”。 |
| hrq-00240 | entry-01498 | mod-tome.lua:20894 | fix | accepted | 是 | 独立核验通过；原文顺序是找到路（Find it）→ 探索远东 → 寻找线索（looking for clues 修饰 explore），现译把“寻找线索”提到找路之前，动作关系颠倒；同句 far east 被译成“远东大陆”与“遥远的东方”两个称呼。按原文顺序重排并统一为“远东大陆”。 |
| hrq-00241 | entry-01508 | mod-tome.lua:21014 | no_change | accepted | 否 | 无需修改；8 个占位符数量、类型、顺序正确；标点与斜杠前空格不统一属纯静态排版，模型自标 advisory，按用户策略不整理。 |
| hrq-00242 | entry-01509 | mod-tome.lua:21029 | fix | accepted | 是 | 独立核验通过；占位符 claim 成立无需改。机制 claim 经源码核实：Chant Adept.doCure 只对 e.type == type 且 subtype["cross tier"] 的效果全部移除，其余同类型负面效果 rng.tableRemove 随机移除最多 cures 个。现译列出三种越层效果并说“解除自身的越层效果”，读作全部解除；“额外解除 %d 项”也缺随机与“至多”。改为“解除所有相应类型的越层效果（……或……），并随机 |
| hrq-00243 | entry-01510 | mod-tome.lua:21053 | no_change | accepted | 否 | 无需修改；半径、伤害、持续时间三个 %d 顺序正确；最后一句另起一行属纯静态排版，且本批禁止改变换行序列。 |
| hrq-00244 | entry-01512 | mod-tome.lua:21076 | no_change | accepted | 否 | 无需修改；%0.1f 与 %d 对齐；“护盾至少持续 2 回合”一句在冻结英文源串中本就不存在，不是译文遗漏，不能凭其他版本补入。 |
| hrq-00245 | entry-01514 | mod-tome.lua:21091 | fix | accepted | 是 | 独立核验通过；四个占位符含义与顺序正确。首行原文 (up to %d, Current: %d). 带括号和句号，现译“至多 %d 点，当前 %d 点”后缺句末标点，属标点修正；按原文补全角括号与句号，additional 补“额外”。换行保持不变。 |
| hrq-00246 | entry-01516 | mod-tome.lua:21110 | fix | accepted | 是 | 独立核验通过；三个 %d%% 对应正确。“%d%% , 持续”在中文句中用了半角逗号，属标点错误，改全角“，”。 |
| hrq-00247 | entry-01517 | mod-tome.lua:21116 | fix | accepted | 是 | 独立核验通过；四个占位符正确。“%d%% , 同时”半角逗号改全角“，”。“灼烧痕迹”未点名 EFF_LIGHTBURN 状态名属 advisory：源码第 119 行确实施加 LIGHTBURN，但现译已表达持续伤害与减甲机制，状态命名一致性需另核效果名译法，不在本条改。 |
| hrq-00248 | entry-01518 | mod-tome.lua:21122 | fix | accepted | 是 | 独立核验通过；两个 %d%% 对应正确；两行合并为一行属排版 advisory 不改。源码第 168 行施加 EFF_FLASH_SHIELD，timed_effects/other.lua 中效果为 cancel_damage_chance=100，即 1 回合免疫所有伤害；现译“吸收 1 回合内的所有攻击”把对象从伤害缩成攻击（非攻击伤害如持续伤害也被免疫），改为“免疫 1 回合内的所有伤害”。 |
| hrq-00249 | entry-01528 | mod-tome.lua:21308 | no_change | accepted | 否 | 无需修改；五个占位符与颜色码正确；末行补句号、补“圣印”后缀是可接受整理，未改变机制。 |
| hrq-00250 | entry-01531 | mod-tome.lua:21343 | no_change | accepted | 否 | 无需修改；否定句改写为必要条件句语义等价；源码 guardian.lua:202 在无盾时输出此日志。Crusade 在同节 talent name 译“十字军打击”（mod-tome.lua:21342），本条一致。 |
| hrq-00251 | entry-01534 | mod-tome.lua:21433 | no_change | accepted | 否 | 无需修改；源码 damage_types.lua HEALING_POWER：治疗、无护盾则建护盾否则累加、dur=max(2,dur)、延长 20 次后 removeEffect，与现译一致；英文末行无句号而中文补句号属可接受整理。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
