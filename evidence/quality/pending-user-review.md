# 待用户集中审阅的争议条目

以下条目依据用户 2026-09-23 指示集中记录：有争议的条目列入 pending，不在当前修复窗口修改，也不阻塞窗口收束。前三条均来自窗口 8 的 `ADJUDICATION-R0.json`。

## 窗口 8 待审阅

1. `e92433bcba`（unlock-yeek）
   - 英文要点：叙事文本中的 `cunning`。
   - 现译：“灵巧”。术语库记录 `Cunning=灵巧`，类别为 stat name，`status=existing`。
   - 争议理由：宿主此前依据术语记录判定保持；surface、Opus contextual 与本轮 reviewer 共三个模型认为叙事语境应译为“机敏”或“狡黠”，且 `existing` 不代表覆盖所有语境。
   - 建议选项：保持“灵巧” / 叙事语境改“机敏”。
   - **已裁决（2026-09-27，用户）**：保持现译。夺心魔种族加值 Wil +6、Cun +4 为全部可玩种族最高，“cunning and willful” 对应灵巧与意志两项属性，现译用属性名呼应，不改。第 4 项随之。

2. `e951739433`（毒素风暴）
   - 英文要点：`Each possible effect is equally likely`。
   - 现译：“中毒几率在可能的毒素效果中平分”。
   - 争议理由：源码 `damage_types.lua` 先等概率抽取效果，再判断目标能否中毒；宿主曾判现译与等概率语义等价，reviewer 认为现译把“效果等概率”写成了“中毒几率分配”。
   - 建议选项：保持 / 改为“各种可能的效果出现几率相同”。
   - **已裁决（2026-09-27，用户）**：改为“各种可能的效果出现几率相同。”（源码 damage_types.lua:4013–4043 每次命中必定施加一种毒素，效果等概率抽取；现译引入原文没有的“中毒几率”）。排入下一修复窗口；第 5 项随之。

3. `e988482539`（龙族传说）
   - 英文要点：“The common man may scoff at the idea of classifying dragons as an intelligent race”。
   - 现译：“嘲笑我把龙作为单独列出的智慧种族”，含原文没有的第一人称。
   - 争议理由：reviewer 两次指出原文没有“我”；宿主认为该系列是 Loremaster Greynot 的第一人称著作，语境允许这一增译。
   - 建议选项：保持 / 改为“嘲笑将龙归为智慧种族的想法”。
   - **已裁决（2026-09-27，用户）**：改为“一般人也许会嘲笑将龙归为智慧种族的想法”（删增译的“我”与“单独列出”），同段一并修“另人→令人”、subtle“最狡猾→最精明”。排入下一修复窗口。

## 审核 254 的其他观察

- 宿主补充观察 `e923d2b8d0`：`The target is using talents without consuming resources` 现译为“不再消耗能量”，将 `resources` 窄化为“能量”。
- 审核 254 advisory：`ALL_DREAMS` 以外无其他同类项；另保留 `rogues do it from behind` 标题双关，以及 `SPELLSHOCKED` 省略 `temporarily` 两项建议。

## 审核 255 待审阅

4. `14568237c4`（种族解锁叙事，yeek）
   - 英文要点：`yet they are a cunning and willful race`。
   - 现译：“非常灵巧而且意志强大”。
   - 争议理由：与第 1 项为同一 `cunning=灵巧` 叙事语境争议的另一条目，应随第 1 项一并裁定。
   - 建议选项：同第 1 项。
   - **已裁决（2026-09-27，用户）**：同第 1 项，保持现译。

5. `a1e95a2f4c`（毒素风暴，另一副本）
   - 英文要点：`Each possible effect is equally likely`。
   - 现译：“中毒几率在可能的毒素效果中平分”。
   - 争议理由：与第 2 项相同措辞的另一条目，应随第 2 项一并裁定。
   - 建议选项：同第 2 项。
   - **已裁决（2026-09-27，用户）**：同第 2 项。

6. `ea75bd3673`（技能名 `Matter is Energy`）
   - 源码：`psionic/finer-energy-manipulations.lua:126`，消耗一颗宝石换取每回合超能力值。
   - 现译：“宝石能量”，按功能意译，没有体现原名“物质即能量”。
   - 争议理由：改技能名会影响跨条目引用和命名策略；contextual reviewer 判为 OK。
   - 建议选项：保持“宝石能量” / 改为“物质即能量”（需同步引用处）。
   - **已裁决（2026-09-27，用户）**：技能名改为“物能转化”，与其效果名（timed_effects/mental.lua:1534，mod-tome.lua:36086）一致；无其他引用。排入下一修复窗口。

- 审核 255 advisory：巫妖外观名 `Lich Regalia` 译作“巫妖王冠”；召唤触手描述 `Ewwww..` 译作“额……”，语气偏迟疑。

## 审核 256 待审阅

8. `eab2ffb632`（技能名 `Blunt Thrust`）
   - 源码：`spells/staff-combat.lua:141`，法杖近战单体攻击并眩晕。
   - 现译：“钝器挥击”；Thrust 为刺击/戳击，现名把动作译成挥击。
   - 争议理由：改技能名需同步技能引用与日志文本（如 `You cannot use Blunt Thrust without a staff weapon!`）。
   - 建议选项：保持“钝器挥击” / 改为“钝击突刺”或“法杖突刺”等（需同步引用处）。
   - **已裁决（2026-09-27，用户）**：技能名改为“法杖突刺”；同技能 info 首句“挥动法杖对目标造成”改为“以法杖击打目标，造成”（原文 Hit a target）。使用条件日志不含技能名，不改。排入下一修复窗口。

9. `eb6bf55a91`（传说标题 `If I Should Die Before I Wake`）
   - 源码：`lore/misc.lua:623`，标题借用睡前祷词句式。
   - 现译：“从噩梦中惊醒，还是在梦魇中永眠？”，为意译改写。
   - 争议理由：非机制内容，是否直译属风格取舍。
   - 建议选项：保持意译 / 改为“若我在醒来前死去”。
   - **已裁决（2026-09-27，用户）**：经 Gemini 3.8 Flash 咨询后，标题改为“若我死于醒来之前”（保留祷词未完条件句的不祥感）。排入下一修复窗口。

10. `eb71935d6c`（神器名 `Crystal Shard`）
    - 源码：`boss-artifacts-maj-eyal.lua:643–648`，magestaff 唯一神器，未鉴定名 crystalline tree branch。
    - 现译：“水晶之杖”，以物品类型替换 Shard（碎片）；surface 与 contextual 均提出。
    - 争议理由：神器专名改名属命名决定。
    - 建议选项：保持“水晶之杖” / 改为“水晶碎片”。
    - **已裁决（2026-09-27，用户）**：经 Gemini 3.8 Flash 咨询，改为“碎晶”（避开炼金材料“红色水晶碎片”撞名与使用日志“碎片上的碎片”复沓）。排入下一修复窗口。

- 审核 256 advisory：Dark Vision “在黑暗之雾中”移速（实现为移入含黑暗之雾的格子）；贴图说明 tile 译“材质”；教程 NPC `Loitering elf` 译“流浪的精灵”。

## 修复窗口 9 待审阅

7. `e9e627f60c`（高阶奇术师解锁文本中的 Flame 名称）
   - 英文要点：`Flame, Manathrust, Lightning, Pulverizing Auger and Ice Shards permanently become 3-wide beam spells`。
   - 现译：“火球术”（基线，窗口 9 保持不变）。
   - 争议理由：术语库 `terminology/talents.tsv:117` 记录 `Flame=火球术`（`status=existing`），职业说明 `mod-tome.lua` 亦用“火球术”；但运行时技能名（`mod-tome.lua` / `mod-boot.lua` / `engine.lua` 的 talent name 行）为“火焰”。统一方向属术语决定。
   - 建议选项：改技能名为“火球术”并同步术语 / 改说明与术语库为“火焰”。
   - **已裁决（2026-09-23，维护者）**：经 gpt-6-astra / opus-5.5 / gemini-3.8-flash 三方一致推荐，统一为“火焰术”（术语库改为 preferred），技能名与全部技能引用同步；Shadow Mages 描述中的 Flames 实指 Shadow Flames，改为“暗影之火”。

## 修复窗口 10 待审阅

11. `eb0868d54c`（时空术士 Galsamae 入门笔记长信 `Warden-Master Galsamae's Orientation Notes`）
   - 源码：`lore/misc.lua:721`，`The ultimate power of time - the ability to reset and try again if you fail`。
   - 现译：“能够在你失败时不断重试”。
   - 争议理由：w10b `REVIEW(0)` 认为遗漏 reset（重置时间）；宿主认为该句紧接“有关时间的终极力量”，语境已含借时间重来之意，属措辞精度分歧而非机制错误。
   - 建议选项：保持 / 改为“能够在失败时重置时间、再来一次”。
   - **已裁决（2026-09-27，用户）**：改为“……——能够在失败时重置时间、再来一次，能够在调查进行之前预见其结果、从而节省时间。”（补回 reset，并把被拆成两项的 save time by seeing the results 合回一项）。排入下一修复窗口。

## 审核 261 待审阅

12. `f09f7b5baf`（技能名 `Virulent Strike`）
   - 源码：`talents/corruptions/scourge.lua:25–26`，显示名 Virulent Strike，short_name 仍为 `REND`；实现为双持两击，每次命中延长目标身上持续时间最短的一种疾病。
   - 现译：“撕裂”（沿用旧名 Rend），未体现 virulent（致病、剧毒），也不对应疾病延长的效果。
   - 争议理由：改技能名需要同步日志 `You cannot use Virulent Strike without two weapons!`（mod-tome.lua:22961），“撕裂”族另有 Lacerating Strikes=撕裂挥击 等；属于命名决定。
   - 建议选项：保持“撕裂” / 改为“瘟毒打击”“剧毒打击”一类（需同步引用处）。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“恶疫打击”（与同树“腐化打击”对仗，避开“毒”字对 Poison 体系的误导）；本库无“恶疫”既有用法。技能名与使用条件日志（mod-tome.lua:22947–22948）同步。排入下一修复窗口。

13. `f009c2b19b`（死亡描述 `grandfathered`，时间伤害）
   - 源码：`damage_types.lua:1006` 的时间伤害 death_message 列表；`PartyDeath.lua:71` 随机取一项代入死讯模板“was %s to death”，中文模板为“玩家%s……%s而死”（mod-tome.lua:1412）。
   - 现译：“因弹指间度过了无数美好的青葱岁月，转瞬间你已白发苍苍”，把祖父悖论梗改成衰老致死；句中含“你”，代入第三人称死讯后人称和句法错位。
   - 争议理由：死亡描述词表整族已由用户 2026-09-16 裁定继续 pending；本条是该族的新证据（人称错位，而不只是增添意象），单独修改会造成族内不一致。
   - 建议选项：保持并随整族处理 / 单独改为“被祖父悖论抹去”一类短语。
   - **已裁决（2026-09-27，用户）**：只修这条破坏死讯句法的短语，改为“被祖父悖论抹去”（代入模板“……被祖父悖论抹去而死”）；死亡描述词表其余“增添意象”条目仍按 2026-09-16 裁决 pending。排入下一修复窗口。

## 审核 262 待审阅

14. `f1403b3e60`（神器名 `Exiler`）
   - 源码：`objects/world-artifacts.lua:6833`，时空术士 Solith 的独特戒指（unided_name insignia ring）。
   - 现译：“放逐”，把施事名词译成了动作。
   - 争议理由：神器专名改名属命名决定（先例：Crystal Shard 已列 pending）。
   - 建议选项：保持“放逐” / 改为“放逐者”。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash（单独重派，首次并发派发串答作废）推荐“放逐者”（还原施事 -er，契合使用能力把敌人放逐出时间线）。排入下一修复窗口。

15. `f181f499b6`（技能系 `Crimson Templar`）
   - 源码：`talents/cursed/cursed.lua:46`，堕落圣骑士由 Guardian（守卫）转化而来的技能系（`uber/wil.lua:399`、`texts/unlock-paladin_fallen.lua:36`）。
   - 现译：“赤红守卫”，未体现 Templar（圣殿骑士），与 Guardian=守卫 只差修饰。
   - 争议理由：技能系改名需要同步说明与解锁文本中的引用，属命名决定。
   - 建议选项：保持“赤红守卫” / 改为“赤红圣殿骑士”“血色圣殿骑士”一类（需同步引用处）。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐全库统一为“血色圣殿骑士”（Templar＝圣殿骑士，血色呼应鲜血之力；深红圣武士易与 Paladin 混淆）。同步：技能系名 mod-tome.lua:24063、职业解锁说明两处（现“血红守卫”“赤红守卫”）、Orcs Boss“深红骑士约翰”→“血色圣殿骑士约翰”（tome-orcs.lua:6863/6994）、Orcs 对话“深红圣武士”（tome-orcs.lua:401 一带）；第342批 advisory b6e17ee9e4 随之关闭。本库无“圣殿骑士”既有用法。排入下一修复窗口。

## 修复窗口 16 待审阅

16. 世界名 `Eyal`（全库译“埃亚尔大陆”）
   - 源码：Eyal 是整个世界的名称（如 `mod-tome.lua:6013` 源文 “This orb seems to represent the world of Eyal as a whole”；`talents/uber/str.lua:311` “far beyond Eyal”），Maj'Eyal 才是大陆（术语库 places.tsv 已定“马基·埃亚尔”）。
   - 现译：“埃亚尔大陆”，把世界限定成了大陆；mod-tome.lua 与 tome-ashes-urhrok.lua 各 23 处，engine.lua、mod-boot.lua 各 1 处；术语库无 Eyal 记录。
   - 争议理由：窗口 16 REVIEW(0) 在星辰契约条目上提出；属全库改名与新增术语记录，超出现有授权，未在窗口内修改（advisory）。
   - 建议选项：保持“埃亚尔大陆” / 改为“埃亚尔”或“埃亚尔世界”（需新增术语记录并全库同步，含 `of Eyal`=“埃亚尔之”等派生）。
   - **已裁决（2026-09-27，用户）**：复核计数更正——全库裸“埃亚尔”约 267 处为多数，仅约 31 处（mod-tome 11、tome-ashes-urhrok 20）作“埃亚尔大陆”。改这 31 处为“埃亚尔”，术语库新增 `Eyal＝埃亚尔`（preferred，注明世界名、非大陆）；Maj'Eyal＝马基·埃亚尔、Var'Eyal＝瓦·埃亚尔（大陆）不动。排入下一修复窗口（先改术语库再改译文）。

17. `f18f9a4e90` 等（lore “An undead hunter's guide, by Aslabor Borys”）
   - 源码：`lore/fun.lua:217` 署名；同一 lore 的条目名与说明见 `mod-tome.lua:11440–11441`。作者是活人猎手（正文自述砍下吸血鬼头颅、请人喝酒）。
   - 现译：标题（11440–11441）“不死猎人指南”；正文署名已在窗口 16 第 2 轮改为“一名不死生物猎人的指南”以消歧；另一处 lore 中 undead hunters 译“亡灵猎手”。
   - 争议理由：窗口 16 FINAL(1) 认为“不死猎人”易读作“不死的猎人”；宿主认为“X猎人”惯例读作猎杀X者（如恶魔猎人），且标题属窗口外条目；为使 FINAL 收敛，窗口内只改了正文署名，两处标题留待决定。
   - 建议选项：标题保持“不死猎人指南” / 两处标题改为“不死生物猎人指南”与正文一致（或统一为“亡灵猎手”）。
   - **已裁决（2026-09-27，用户）**：三处统一为术语 undead＝亡灵：书本物品名““尘归尘”，亡灵猎手指南，作者：阿斯拉伯·波利斯”（mod-tome.lua:11440）、物品描述“亡灵猎手指南，作者：……”（11441）、lore 正文首行“一名亡灵猎手的指南”（15948 一带）；另把 lore 标题 Dust to Dust“土归土”（15875）统一为“尘归尘”（技能名 Dust to Dust 22109 不在本项）。排入下一修复窗口。

## 审核 267 待审阅

18. `f6cc31f278`（死亡描述，枯萎伤害）
   - 源码：`damage_types.lua:909` 枯萎伤害 death_message 列表中的 `debilitated by noxious blight before falling`；`PartyDeath.lua:71,107` 随机取一项代入死讯模板。
   - 现译：“死前吸入过多剧毒瘴气”，把“被剧毒枯萎削弱”写成吸入过量毒气；枯萎（blight）是腐化类伤害而非气体。
   - 争议理由：surface 与 Opus contextual 均判 ISSUE；但死亡描述词表整族已由用户 2026-09-16 裁定继续 pending（第 13 项先例），单改一条会造成族内不一致。
   - 建议选项：保持并随整族处理 / 单独改为“被剧毒枯萎折磨致衰弱”一类短语。
   - **已裁决（2026-09-27，用户）**：只修这条（原译“死前……”与模板“而死”重复），改为“被剧毒枯萎折磨得虚弱不堪”（代入模板“……被剧毒枯萎折磨得虚弱不堪而死”）；词表其余条目仍 pending。排入下一修复窗口。

## 修复窗口 25 待审阅

19. `fad7958eaa`（效果 `BLOODCASTING` 的长描述 “Corruptions consume health instead of vim.”）
   - 源码：`timed_effects/magical.lua:2455–2470` 效果只加 `bloodcasting=1`；`class/Actor.lua:5576–5592` 的 `incVim` 在活力足够时照常扣活力，只有活力不足时才以生命值支付缺额（倍率 `bloodcasting/100`，该效果下为 0.01；无此属性时为 2）。
   - 现译：“堕落系法术消耗生命值而非活力值。”——忠实于英文原句，但英文本身把“缺额用生命支付”说成了“以生命代替活力”。
   - 争议理由：窗口 25 REVIEW(0) 指出与机制不符；宿主核实机制属实，但这是上游原文与实现的矛盾，不是译文缺陷（advisory）。是否在译文中按实现改写原文说法属策略决定。
   - 建议选项：保持忠实原文 / 改为按实现描述，如“活力不足时，堕落系法术以生命值支付不足部分。”
   - **已裁决（2026-09-27，用户）**：保持忠实原文。另查实主游戏与三 DLC 均无处施加 EFF_BLOODCASTING（仅有定义），该文本几乎不会显示。

## 审核 276 待审阅

20. `ff891672cb`（神器名 `Sceptre of the Archlich`）
   - 源码：固定主游戏 `world-artifacts.lua:2637`，名称含 `Archlich`，与巫妖套装关联。
   - 现译：“死灵权杖”，未明确表达 Archlich；surface 与重冻 contextual 均提出。
   - 争议理由：神器专名改名须与套装及引用一致，术语库尚无 Archlich 的固定译法。
   - 建议选项：保持“死灵权杖” / 改为“大巫妖权杖”一类并同步相关引用。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“大巫妖权杖”（与同系列“大巫妖之戒”对齐）。本库无其他引用。排入下一修复窗口。

21. `0c451e854a`（DLC 技能与效果名 `Armoured Leviathan`）
   - 源码：公开 Ashes DLC `timed_effects.lua:637`；本批文件 SHA 匹配，来源仓库与 commit 未固定。同族技能、效果和日志使用同名。
   - 现译：“重装上阵”，统一意译但未表达 Leviathan 的巨兽意象；surface 提出，重冻 contextual 判 OK。
   - 争议理由：若改名，需同步技能、效果及 +/- 日志，属跨条命名决定。
   - 建议选项：保持“重装上阵” / 选定含巨兽意象的新名并同步同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“铁甲利维坦”（保留 Leviathan 意象并与本库“利维坦”一致，避开 Behemoth＝巨兽）。第 21、27、28 项同族同步：tome-ashes-urhrok.lua:866 技能名、1558 效果名、1561/1563 ±日志。排入下一修复窗口。

## 审核 277 待审阅

22. `1dafd3a728`（Ashes 效果名 `Corruption of the Doomed`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:1045–1052`，本批 workset 文件 SHA 匹配；来源仓库与 commit 未固定。效果名及 +/- 日志同族使用，相关条目现译统一“腐化形态”。
   - 现译：“腐化形态”，没有表达 `Doomed`；surface 提出，合规重冻 contextual 判 OK。
   - 争议理由：更名需同步四处效果／日志及可能的技能引用，属于跨条专名决定，本批不单改。
   - 建议选项：保持“腐化形态” / 选定包含“厄运”或“受诅者”含义的新名并同步同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“末日腐化”（与同树 Haste of the Doomed＝末日加速对齐）。第 22、25、29 项同族同步：tome-ashes-urhrok.lua:1413 技能名、1641 效果名、1644/1645 ±日志。Gemini 另建议 Resilience of the Doomed“强韧”→“末日强韧”，不在 pending 范围，未采纳，待用户另定。排入下一修复窗口。

## 审核 278 待审阅

23. `3747432e7d`（Ashes 效果日志 `+Osmosis Regen`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:523–530`，效果名 `Osmosis Regeneration`，日志 `+/-Osmosis Regen`；长描述说明在效果期间回复生命值。本批 workset 文件 SHA 匹配，来源仓库和 commit 未固定。
   - 现译：“+渗透吸收”；同族效果名和减益日志也统一使用“渗透吸收”。
   - 争议理由：现译未明示 Regen 的回复含义，但单改一条日志会破坏同族命名一致性，需要决定整族译名。
   - 建议选项：保持“渗透吸收” / 确定包含“回复”或“再生”的新名并同步效果名及 +/- 日志。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“渗透回复”（对应 3 回合持续回血，与护盾“吸收伤害”区分）。第 23、24、26 项同族同步：tome-ashes-urhrok.lua:1535 效果名、1537/1538 ±日志；护盾技能名“渗透护盾”与日志“转化为渗透”不改。排入下一修复窗口。

## 审核 283 待审阅

24. `b349784043`（Ashes 效果名 `Osmosis Regeneration`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:521–530`，效果 `OSMOSIS_REGEN` 为持续回复生命（subtype heal，on_timeout 调用 `self:heal`），由渗透护盾吸收伤害后施加。本批 workset 文件 SHA 匹配，来源仓库和 commit 未固定。
   - 现译：“渗透吸收”；与第 23 项 `+/-Osmosis Regen` 日志同族统一。
   - 争议理由：surface 与合规重冻 contextual 均认为未表达 Regeneration 且易与渗透护盾的吸收混淆；更名须与第 23 项一并同步效果名及 +/- 日志。
   - 建议选项：保持“渗透吸收” / 改“渗透回复”或“渗透再生”并同步第 23、24 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“渗透回复”（对应 3 回合持续回血，与护盾“吸收伤害”区分）。第 23、24、26 项同族同步：tome-ashes-urhrok.lua:1535 效果名、1537/1538 ±日志；护盾技能名“渗透护盾”与日志“转化为渗透”不改。排入下一修复窗口。

## 审核 284 待审阅

25. `bee297d916`（Ashes 效果日志 `+Corruption of the Doomed`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:1045–1052`，本批 workset 文件 SHA 匹配；来源仓库与 commit 未固定。
   - 现译：“+腐化形态”，未表达 `of the Doomed`；与第 22 项同族效果名统一。
   - 争议理由：surface 提出，contextual 判 OK；单改一条日志会破坏同族一致性，须与第 22 项一并决定整族译名。
   - 建议选项：保持“腐化形态” / 选定包含“厄运”或“受诅者”含义的新名并同步第 22、25 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“末日腐化”（与同树 Haste of the Doomed＝末日加速对齐）。第 22、25、29 项同族同步：tome-ashes-urhrok.lua:1413 技能名、1641 效果名、1644/1645 ±日志。Gemini 另建议 Resilience of the Doomed“强韧”→“末日强韧”，不在 pending 范围，未采纳，待用户另定。排入下一修复窗口。

## 审核 286 待审阅

26. `dcfd031f93`（Ashes 效果日志 `-Osmosis Regen`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:521–530`，效果 `OSMOSIS_REGEN` 的减益日志；本批 workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“-渗透吸收”；与第 23、24 项同族统一。
   - 争议理由：surface 提出未表达 Regen，contextual 判 OK；单改会破坏同族一致性，须与第 23、24 项一并决定。
   - 建议选项：保持“渗透吸收” / 改“渗透回复”或“渗透再生”并同步第 23、24、26 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“渗透回复”（对应 3 回合持续回血，与护盾“吸收伤害”区分）。第 23、24、26 项同族同步：tome-ashes-urhrok.lua:1535 效果名、1537/1538 ±日志；护盾技能名“渗透护盾”与日志“转化为渗透”不改。排入下一修复窗口。

27. `df20e15744`（Ashes 技能名 `Armoured Leviathan`）
   - 源码：公开 Ashes DLC `data/talents/corruptions/demon-seeds.lua:689`；本批 workset 文件 SHA 匹配，来源仓库与 commit 未固定。同名效果与日志见第 21 项。
   - 现译：“重装上阵”，未表达 Leviathan 的巨兽意象；surface 提出，contextual 判 OK。
   - 争议理由：更名须同步技能名、效果名及 +/- 日志，属跨条命名决定。
   - 建议选项：保持“重装上阵” / 选定含巨兽意象的新名并同步第 21、27 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“铁甲利维坦”（保留 Leviathan 意象并与本库“利维坦”一致，避开 Behemoth＝巨兽）。第 21、27、28 项同族同步：tome-ashes-urhrok.lua:866 技能名、1558 效果名、1561/1563 ±日志。排入下一修复窗口。

## 审核 287 待审阅

28. `fb23faa260`（Ashes 效果日志 `-Armoured Leviathan`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:638`，效果 `ARMOURED_LEVIATHAN` 的减益日志；本批 workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“-重装上阵”；与第 21、27 项同族统一。
   - 争议理由：surface 提出丢失“巨兽”意象，contextual 判 OK；单改会破坏同族一致性，须与第 21、27 项一并决定。
   - 建议选项：保持“重装上阵” / 选定含巨兽意象的新名并同步第 21、27、28 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“铁甲利维坦”（保留 Leviathan 意象并与本库“利维坦”一致，避开 Behemoth＝巨兽）。第 21、27、28 项同族同步：tome-ashes-urhrok.lua:866 技能名、1558 效果名、1561/1563 ±日志。排入下一修复窗口。

29. `fc9cbd5243`（Ashes 效果名 `Corruption of the Doomed`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:1042`（效果 `CORRUPTION_OF_THE_DOOMED` 的 desc，±日志见 :1048–1049）；本批 workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“腐化形态”，未表达 `Doomed`；surface 提出，contextual 判 OK。
   - 争议理由：与第 22、25 项同族，更名须同步效果名与 ±日志，属跨条命名决定。
   - 建议选项：保持“腐化形态” / 选定包含“厄运”或“受诅者”含义的新名并同步第 22、25、29 项同族条目。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“末日腐化”（与同树 Haste of the Doomed＝末日加速对齐）。第 22、25、29 项同族同步：tome-ashes-urhrok.lua:1413 技能名、1641 效果名、1644/1645 ±日志。Gemini 另建议 Resilience of the Doomed“强韧”→“末日强韧”，不在 pending 范围，未采纳，待用户另定。排入下一修复窗口。

## 修复窗口 31 待审阅

30. `11d347416e`（Cults 技能 info，`numbed` 的译法）
   - 源码：公开 Cults DLC `data/talents/demented/tentacles.lua:228–234`（施加 `SLIMY_TENDRIL`），效果定义 `data/timed_effects.lua:113–125` 只设置 `numbed`，即目标造成的伤害降低；窗口 31 SOURCE-ANCHORS 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“被麻痹”，同句写明“5 回合内伤害降低 %d%%”；本库 Numbing 族一贯用“麻痹”（如 Numbing Poison“麻痹毒素”），均为降伤。
   - 争议理由：GPT-6 Sol 复审在第 289 批与窗口 31 的 r0a1、r2a1、r3a1 中四次提出“麻痹”易被理解为无法行动；宿主按本库同族译法与同句定义判 refuted，Opus 终审均判 OK。改动须同步整个 Numbing 族，属跨条术语决定。
   - 建议选项：保持“麻痹” / 全族改“麻木”等不暗示失能的词并同步 Numbing 族条目与术语库。
   - **已裁决（2026-09-27，用户）**：Numbing 全族改“麻木”（新证据：本库 Paralyzed＝麻痹（mod-tome.lua:37297/37299 ±日志、麻痹圣印），与降伤的 Numbing 同词冲突；物品伤害类型已作“物品黑暗麻木”）。范围：Numbing Poison 麻痹毒素→麻木毒素（技能名、效果名、±日志、info 与各引用）、Numbing Blight 麻痹枯萎毒素→麻木枯萎毒素、Numbing Darkness 黑暗麻痹→黑暗麻木、dark numbing melee 近战暗影麻痹伤害→近战暗影麻木伤害、numbing darkness 爆炸日志、剧毒风暴等 info 中的“麻痹毒素效果”、Cults 触手 numbed“被麻痹”→“被麻木”；Paralyzed/Glyph of Paralysis 的“麻痹”不动。术语库新增 Numbing＝麻木（preferred）。排入下一修复窗口（开窗时全仓 grep numb 逐条核对）。

## 修复窗口 37 待审阅

31. `0b55d129c8`（Orcs lore 克林布尔手记；同族 `Soft-foot` 条目 tome-orcs.lua:506、508）
   - 源码：公开 Orcs DLC `tome-orcs/data/lore/krimbul.lua`（soft-footed／soft-feet，米诺陶对无蹄种族的称呼）；窗口 37 SOURCE-ANCHORS 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“软蹄族”（本条 3 处）与“软蹄者”（Soft-foot，2 处），全 DLC 一致。
   - 争议理由：窗口 37 r0a1 GPT-6 Sol 指出 foot 被写成“蹄”，颠倒米诺陶（有蹄）对他族（软脚）的称呼关系；改动须同步 5 处且属跨条译名决定，本窗口未授权，宿主记 advisory。
   - 建议选项：保持“软蹄族／软蹄者” / 统一改为“软脚族／软脚者”（或“软足者”）并同步 506、508 与本条。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐群体称“软脚族”、对人称“软脚者”（纠正有蹄/无蹄视角颠倒）；Gemini 另给的呼格“软脚的”在“克鲁克部落的软脚的”中不通，宿主取其并列候选“软脚者”。同步 lore 3 处（tome-orcs.lua:2443 一带）与对话 2 处（499/501）。排入下一修复窗口。

## 第 315 批待审阅

32. `19137076a9`（Orcs 工匠物品／技能名 `Thunder Grenade`；同名条目 tome-orcs.lua:1349「%s thunder grenade」、5523 talent name、6669 _t）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/other.lua` `TINKER_THUNDER_GRENADE` 以 `DamageType.PHYSICAL` 造成伤害并施加 `EFF_STUNNED`；配方 `data/tinkers/explosive.lua` desc「Small radius, but stuns quite well.」；造成闪电伤害的是 `Shock Grenade`（本库“震荡榴弹”，`data/talents/steam/demolition.lua`）。第 315 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“闪电榴弹”（3 处一致）。
   - 争议理由：第 315 批 GPT-6 Sol 表层筛查指出 Thunder 是雷鸣而非闪电，宿主按源码确认“闪电”暗示闪电属性、与实际物理＋震慑不符；Opus contextual 判 OK。改名须同步 3 处并定新译名，且与“震荡榴弹”（Shock）的命名互相牵连，属跨条译名决定，本批记 advisory。
   - 建议选项：保持“闪电榴弹” / 改“雷鸣榴弹”（或“震爆榴弹”）并同步 1349、5523、6669 三处。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“雷鸣榴弹”（还原 Thunder 声响意象，消除与放电的“震荡榴弹”混淆）。同步 tome-orcs.lua 当前行 1342（“%s 雷鸣榴弹”）、5527、6680。排入下一修复窗口。

## 第 316 批待审阅

33. `219d179f63`（Orcs 工匠技能名 `Voltaic Bolt`；同名 tome-orcs.lua:5536 talent name、5538 info“释放一个闪电球”，伏特守卫说明 5619–5621“闪电球”）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/other.lua:1209` `TINKER_VOLTAIC_BOLT` 目标 `type="bolt"`（单体飞弹，info：Fires a bolt of lightning）；ToME 中 ball 是范围攻击的目标类型。第 316 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“闪电球”（技能名、info 与伏特守卫说明一致）。
   - 争议理由：第 316 批 GPT-6 Sol 表层筛查指出 Bolt 是飞弹而非球，宿主按源码确认“球”易让人误以为是范围攻击；Opus contextual 判 OK。改名须同步多处并定新译名，属跨条译名决定，本批记 advisory。
   - 建议选项：保持“闪电球” / 改“闪电箭”（或“伏特飞弹”）并同步 5536、5538、5619–5621。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐技能名“伏特电箭”（与伏特守卫/伏特弹同系，“箭”对应单体 bolt），info 首句改“发射一枚闪电箭，造成 %0.2f 闪电伤害。”。当前只剩 tome-orcs.lua:5540/5542 两处（伏特守卫说明已在窗口修复中改为“电流”）。排入下一修复窗口。

## 第 320 批待审阅

34. `36ece3ede8`（Orcs 蒸汽枪技能名 `Supercharge Bullets`；同族效果名 tome-orcs.lua:6320 `Bullet Mastery: Supercharged`“子弹掌握：超速”，技能名 4759“超速子弹”）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/bullets-mastery.lua:52–72` 设置 `EFF_ENHANCED_BULLETS_SUPERCHARGE`（kind="supercharge"），info：子弹可穿透多个目标，并提高护甲穿透；与飞行速度无关。第 320 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“超速子弹”（技能名）与“子弹掌握：超速”（效果名）一致。
   - 争议理由：第 320 批 GPT-6 Sol 表层筛查指出 Supercharge 是增压/超充而非超速，宿主按源码确认效果为穿透；Opus contextual 判 OK。改名须同步技能名与效果名并定新译名，属跨条译名决定，本批记 advisory。
   - 建议选项：保持“超速子弹” / 改“超充子弹”（或“增压子弹”）并同步 4759 与 6320 的“超速”。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“增压子弹”，效果名“子弹掌握：增压”，效果描述“子弹处于超速状态”→“子弹经过增压”（tome-orcs.lua:4761、6329、6330）。排入下一修复窗口。

## 第 327 批待审阅

35. `5e7cd06b60`（Orcs 效果名 `Awesome Toss`；同名技能名 tome-orcs.lua:4931 talent name、效果名 6442 _t，同族技能 info 4942“致命翻转”）
   - 源码：公开 Orcs DLC `tome-orcs/data/timed_effects/physical.lua:596–603`（on_gain：“#Target# tosses steamguns in the air, awesome!”）与 `data/talents/steam/elusiveness.lua`：把两把蒸汽枪抛向空中旋转射击，期间视为缴械；与“致命”“翻转”均无关。第 327 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“致命翻转”（技能名、效果名与 info 引用一致）。
   - 争议理由：第 327 批 GPT-6 Sol 表层筛查指出 Awesome 被译成“致命”、Toss 被译成“翻转”；宿主按源码确认字面与动作均不符，Opus contextual 判 OK。改名须同步技能名、效果名与 info 引用并定新译名，属跨条译名决定，本批记 advisory。
   - 建议选项：保持“致命翻转” / 改“华丽抛枪”（或“炫技抛枪”）并同步 4931、4942、6442。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“华丽抛枪”（还原抛枪动作与表演感，与同树“炫目大跳”协调）。同步 tome-orcs.lua:4940 技能名、4951–4952 炫目大跳 info 引用、6456 效果名。排入下一修复窗口。

## 修复窗口 40 待审阅

36. Orcs 神器名 `Gardanion, the Light of God`（tome-orcs.lua:7449 entity name；同物品描述 `595abf50af` 在窗口 40 修复）
   - 源码：公开 Orcs DLC `tome-orcs/data/zones/slumbering-caves/objects.lua:35`（name = "Gardanion, the Light of God"）；来源仓库与 commit 未固定。
   - 现译：“Gardanion，神之光辉”（专名保留英文，本库无 Gardanion 译名）。
   - 争议理由：第 326 批宿主发现物品名半英半中；补译需新造音译专名，本库与术语库均无先例，窗口 40 不自行新造。
   - 建议选项：保持现状 / 音译为“加达尼恩，神之光辉”（或“加尔达尼恩”）并登记术语库。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“加尔达尼恩，神之光辉”（保留 r 音、音节完整）。同步 tome-orcs.lua:7463，并在术语库登记 Gardanion＝加尔达尼恩。排入下一修复窗口。

## 第 329 批待审阅

37. Orcs 地名／势力名 `Sunwall` 全库译名不一（本批 `69c4df21cd`：tome-orcs.lua:279 世界介绍“free it from Sunwall scum”）
   - 源码：公开 Orcs DLC `tome-orcs/data/birth/worlds.lua`（“reclaim the far east and free it from Sunwall scum”）；Sunwall 指远东人类据点太阳堡垒（与其所在城市 Gates of Morning 不同）。第 329 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：tome-orcs.lua 同时用“太阳堡垒”（约 46 处）与“晨曦之门”（约 17 处，部分为 Sunwall 的译文，如第 31、53、272、276、279 行）；术语库 `sunwall`→“太阳堡垒”仅为 existing（narrative.tsv:28），无 preferred 条目。
   - 争议理由：第 329 批 GPT-6 Sol 表层筛查指出本条“回到远东”漏“夺回”；宿主核对后认为“并将其从……手中夺回”已覆盖 reclaim/free，但 Sunwall 被译成 Gates of Morning 的城名，与本库多数译法冲突。统一需跨条改名并定 preferred，超出批次授权，本批记 advisory。
   - 建议选项：统一为“太阳堡垒”（Gates of Morning 保留“晨曦之门”）并登记 preferred、在下一修复窗口按 revision 批量同步 / 保持现状。
   - **已裁决（2026-09-27，用户）**：复核更正——按原文拆分，真正把 Sunwall 译成“晨曦之门”的只有 tome-orcs.lua 5 条（31、53、272、276、279），其余“晨曦之门”对应 Gates of Morning，正确。改：31/272/276/279 用“太阳堡垒”，53 “the bastion of the Sunwall”改“摧毁太阳堡垒的要塞”；272 的“瓦尔·埃亚尔”顺改“瓦·埃亚尔”；术语 sunwall＝太阳堡垒升 preferred（注明势力/据点，城市 Gates of Morning＝晨曦之门）。排入下一修复窗口。

## 第 345 批待审阅

38. Orcs 神器名 `The Lumberator`（`c8a0b6d86f`，tome-orcs.lua:1711 entity name）
   - 源码：公开 Orcs DLC `tome-orcs/data/general/objects/world-artifacts.lua:1898–1904`（BASE_STEAMSAW，unided_name “vined coated steamsaw”，desc “this seed injecting steamsaw”，击杀时召唤树人）。第 345 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“播种机”，与上游官方 `data/locales/zh_hans.lua:1711` 一致。
   - 争议理由：第 345 批 GPT-6 Sol 表层筛查与 Opus contextual 均认为 Lumberator（lumber＋-ator）是伐木之义，“播种机”丢掉了字面义；宿主核对后认为现译贴合“注入种子、把敌人变成树”的设定，也沿用了官方译名。改名是专名决定，本批记 advisory。
   - 建议选项：保持“播种机” / 改为体现伐木与播种双关的译名（如“伐木播种机”或“伐木者”）并同步物品描述引用。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“伐木机”（紧扣链锯本体与 -ator 机械后缀）。同步 tome-orcs.lua:1710；物品描述未引用名称。排入下一修复窗口。

## 第 348 批待审阅

39. Orcs 技能名 `Electricity`（`da3a33562b`，tome-orcs.lua:5696 talent name）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/physics.lua:61`（steamtech/physics 第三个技能，info“Allows you to create electrical tinkers of level %d”）。第 348 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现译：“电子”；同技能 info 作“电子道具”（tome-orcs.lua:5700），出生说明作“电子技能”（6042），另有 Electron Incantation“电子咒式”（4413/6147）。
   - 争议理由：第 348 批 GPT-6 Sol 表层筛查与 Opus contextual 都指出 electricity 是电力/电学，“电子”（electron）字义不符。改名须跨条同步技能名、info 和出生说明，并避免与“电子咒式”混淆，属跨条译名决定，本批记 advisory。
   - 建议选项：保持“电子” / 改“电力”（或“电学”，与同系“机械”“铁匠”并列）并同步 5696、5700、6042。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐“电力”。同步 tome-orcs.lua:5704 技能名、5708 “电子蒸汽工具”→“电力蒸汽工具”、6052 “2级机械和电子技能”→“2级机械和电力技能”；“电子咒式”（Electron Incantation）不动。排入下一修复窗口。

## 修复窗口 45 待审阅

40. 专名 `Ureslak` 音译不一（本窗口 `e7dd1f391b`：tome-orcs.lua:15 成就“Killed Ureslak the Eternal while wielding Ureslak's Femur.”）
   - 源码：公开 Orcs DLC `tome-orcs/data/achievements/special.lua:68`；Boss 与物品指同一条七色巨龙（主游戏 Ureslak's Femur 描述“A shortened femur of the mighty prismatic dragon Ureslak”）。Orcs 来源仓库与 commit 未固定。
   - 现状：巨龙本体作“乌瑞斯拉克”（mod-tome.lua:8500“七色闪光，乌瑞斯拉克”，tome-orcs.lua:1073/2506/7675/7688/7743）；主游戏遗物作“乌尔斯拉克”（mod-tome.lua:12691–12712 股骨、蜕鳞、遗物日志等）。本窗口 RE_REVIEW 与 FINAL 都指出成就同句两种音译，成就句内已统一为“持用乌瑞斯拉克的股骨击杀永恒的乌瑞斯拉克。”（与巨龙实体名一致），但与主游戏物品名“乌尔斯拉克的股骨”仍不同。
   - 争议理由：全库统一须跨 mod-tome/tome-orcs 改一组实体名与描述，属全局更名，未授权，本窗口记 advisory。
   - 建议选项：保持现状 / 统一为“乌瑞斯拉克”（改 mod-tome 遗物一族约 8 条）/ 统一为“乌尔斯拉克”（改 Orcs 与主游戏巨龙名）。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐统一为“乌瑞斯拉克”（res 对应“瑞斯”，覆盖 Boss 本体与兽人 DLC）。改 mod-tome.lua:12691–12712 遗物一族“乌尔斯拉克”→“乌瑞斯拉克”（开窗时全仓 grep 乌尔斯拉克核对）；术语库登记 Ureslak＝乌瑞斯拉克。排入下一修复窗口。

41. Orcs 工匠制造技能 info 中 `tinker` 的译法（本窗口 `e49260a92e` Electricity；同族 tome-orcs.lua:4837/4845/4853/5690/5698/5706 六条 “Allows you to create X tinkers of level %d”）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/physics.lua:72`、`chemistry.lua:32/52/72`、`physics.lua:32/52`。Orcs 来源仓库与 commit 未固定。
   - 现状：六条 info 一律作“X道具”（治疗学道具、化学道具、爆炸学道具、铁匠道具、机械道具、电子道具）；术语 `terminology/items.tsv:24` tinker=“蒸汽工具”（existing，实体类型），Shocking Touch 等处用“蒸汽工具”。
   - 争议理由：窗口 45 RE_REVIEW（GPT-6 Sol）与 FINAL（Opus 5.5）都指出本条与术语不一致；只改本条会破坏六条同族一致，统一属跨条译名决定，本窗口记 advisory。与 #39（Electricity“电子”）相关。
   - 宿主处理：三轮独立复审（r2a1、f3a2、r4a1）一致指出，窗口 45 已把本条对齐术语改为“电子蒸汽工具”（技能名“电子”仍待 #39）；其余五条排入窗口 46 宿主补充同样对齐。
   - 建议选项：认可对齐“蒸汽工具” / 全部保持“道具”（则窗口 46 回退本条）。
   - **已裁决（2026-09-27，用户）**：认可六条“X蒸汽工具”（窗口 45/46 已改），并一并对齐 Create Tinker：技能名“制造道具”→“制造蒸汽工具”（tome-orcs.lua:5408），描述“使用该技能来制造药剂、附着物等道具。”→“允许你制造蒸汽工具。”（5409，删增译清单）。排入下一修复窗口。

## 第 354 批待审阅

42. Orcs 巨炮专名 `DESTRUCTICUS, IMPOLITE PENETRATOR OF THE SKY`（`f79246dcbe`，tome-orcs.lua:332 chats/destructicus.lua）
   - 源码：公开 Orcs DLC `tome-orcs/data/chats/destructicus.lua:30/37/98/102`、`data/lore/destructicus.lua:29`、`data/lore/palace-fumes.lua:170`、`data/zones/palace-fumes/objects.lua:34`（同一门防空巨炮的全称，均为粗体大写）。第 354 批 source workset 文件 SHA 匹配，来源仓库与 commit 未固定。
   - 现状：对话与 lore 六处作“裂天者 毁灭号”（tome-orcs.lua:330/332/379/383/1891 一带）；实体名作“毁天灭地，无礼的天空穿透者”（7289）；蒸汽议会记录作“毁天灭地、无礼的贯穿者————”（2923，原文在 OF- 处被打断）。
   - 争议理由：第 354 批 GPT-6 Sol 表层筛查指出“裂天者 毁灭号”没有译出 IMPOLITE（无礼）这一笑点；Opus contextual 判 OK。三处译名不一，统一须跨对话、lore 与实体名改多条，属全局更名，本批记 advisory。
   - 建议选项：保持现状 / 统一为实体名“毁天灭地，无礼的天空穿透者”（改对话与 lore 六处，议会记录截断版相应改为“毁天灭地，无礼的天空——”）/ 统一为“裂天者 毁灭号”（改实体名与议会记录）/ 另拟兼顾 Destructicus 与 impolite penetrator 的译名。
   - **已裁决（2026-09-27，按用户“纯名称改动直接采用 Gemini 结论”）**：Gemini 3.8 Flash 推荐全称“毁灭号，无礼的天空穿透者”（以全库 18 处简称“毁灭号”打头，保留 impolite 笑点），议会记录截断版“毁灭号，无礼的天空——”，简称保持“毁灭号”。同步 tome-orcs.lua:330/332/379/383/1891 一带“裂天者 毁灭号”、7288 实体名、2922 截断版。排入下一修复窗口。

## 修复窗口 46 待审阅

43. 修饰语 `multi-hued` 的译法分裂（本窗口 `f466031dbb` 口袋时间 lore：“an army of unspeakably powerful multi-hued wyrms”）
   - 源码：公开 Orcs DLC `tome-orcs/data/lore/pocket-time.lua:59`；主游戏生物见固定 commit 624a6732 `game/modules/tome/data/general/npcs/multihued-drake.lua`。Orcs 来源仓库与 commit 未固定。
   - 现状：术语 `terminology/creatures.tsv` multi-hued＝“多彩”（preferred，global，注明与 multihued 实体子类的“多彩”统一）；物品一族作“多彩”（多彩的龙鳞、多彩鳞片斗篷、多彩的鳞片护甲、多彩戒指）；但主游戏生物名作“七彩龙”（multi-hued drake）、“七彩龙幼仔”（hatchling）、“超强的七彩龙精英”（overpowered greater multi-hued wyrm）。
   - 宿主处理：窗口 46 FINAL（Opus 5.5）指出本条“七彩龙”与 preferred 术语不一，按 preferred 改为“多彩巨龙”；生物名一族未改（跨条更名，未授权）。
   - 建议选项：生物名统一为“多彩龙／多彩龙幼仔／多彩龙精英”以对齐术语 / 保留“七彩龙”并把术语改为按语境区分（生物名用七彩、物品与修饰语用多彩），则本条回退为“七彩龙”。
   - **已裁决（2026-09-27，用户）**：按语境区分——生物与角色名（七彩龙、七彩龙幼仔、强化七彩巨龙、超强的七彩龙精英、七彩龙战士、七彩龙之眼等）保持“七彩”，修饰语／物品前缀／实体子类型保持“多彩”；术语库 multi-hued 条目 notes 注明此分工（或新增 multi-hued drake/wyrm＝七彩龙/七彩巨龙 行）。口袋时间 lore（f466031dbb 系）“多彩巨龙”回退为“七彩巨龙”。排入下一修复窗口。

## 第 356 批待审阅

44. 伤害类型 `manaburn` ／ `arcane resource burn` 的译法（本批 `e59c510d73`：Antimagic Shell info “doing %0.2f arcane resource burn damage”）
   - 源码：公开 Orcs DLC `tome-orcs/data/talents/steam/other.lua`（Antimagic Shell 命中调用 `DamageType.MANABURN`）；主游戏固定 commit 624a6732 `game/modules/tome/data/damage_types.lua:3559`（MANABURN）→ `class/Actor.lua:7130–7140` `burnArcaneResources` 同时燃烧法力、活力、正能量与负能量，伤害取 max(mana, vim×2, pos×4, neg×4)。Orcs 来源仓库与 commit 未固定。
   - 现状：术语 `terminology/combat.tsv` manaburn arcane＝“法力燃烧”（existing，global）；伤害类型名作“奥术法力燃烧”（mod-tome.lua:7072）、物品版“物品奥术法力燃烧”（6987）；主游戏 tdesc “%d arcane resource burn” 作“法力燃烧”（6988）；本条作“奥术法力燃烧伤害”。
   - 争议理由：窗口 46 的 r4a1、r5a1 与第 356 批 surface、Opus contextual 共四次指出“法力”把被燃烧的资源窄化为法力；机制确实燃烧四种奥术资源。宿主因全库术语一致性记 advisory；改动属跨批次术语决定。
   - 建议选项：保持“法力燃烧”系 / 全库改为“奥术资源燃烧”（术语、伤害类型名、物品 tdesc 与本条同步）/ 仅在英文写作 arcane resource burn 的描述句改“奥术资源燃烧”，伤害类型名保留。
   - **已裁决（2026-09-27，用户）**：保持“法力燃烧”系不改。依据：主游戏 Mana Clash 原文明言 “This effect is called a manaburn”（燃烧法力/活力/正负能量），法力燃烧是官方机制名的忠实译法；arcane resource burn 只是同一机制的说明性写法。术语库 manaburn arcane 条目补 notes（涵盖四种奥术资源，引 Mana Clash 原文），供后续复审直接引用。

## 2026-09-29 集中审阅（审核队列耗尽后）

45. 死亡描述词族（`mod-tome/data/damage_types.lua` 各伤害类型 `death_message` 表；自 2026-09-16 整族 pending）
   - 源码：固定 commit 624a6732 `game/modules/tome/class/interface/PartyDeath.lua:69-71` 按致死伤害类型从 `death_message` 表随机取一词，代入 `"%s the level %d %s %s was %s to death by %s…"`；译文模板为“……{词}而死”（mod-tome.lua:1413、1416）。全族 95 词。
   - 现状：病句 2 条（`burnt`＝“烧焦的”→“烧焦的而死”，火焰表 10 取 1；`cosmeticed`＝“外观”→“外观而死”）；错义 3 条（`mauled`＝“被殴打”、`timewarped`＝“被时空隔断”、`psyched`＝“过度兴奋”）；约 14 条诙谐加工（被磨成豆浆、被切成葱花、被压成照片、被劈成渣渣、被重拳击中要害、被刺穿要害、被裂颅、被腰斩、被雷劈、被百万伏特电击、被炭烧、被爆炒、被精神强X、被树藤缠绕）。
   - **已裁决（2026-09-29，用户）**：只修病句与错义 5 条——`burnt`→“被烧焦”、`cosmeticed`→“被‘美化’”、`mauled`→“被撕咬致残”、`timewarped`→“被时间扭曲”、`psyched`→“被心灵摧毁”；约 14 条诙谐加工保持原样（与原文俏皮风格一致），同类指摘今后按本裁决驳回。排入修复窗口 55。

46. 审核 254 的其他观察（见上文“审核 254 的其他观察”）
   - `e923d2b8d0` 高等人类之绽放效果描述“不再消耗能量”：固定 commit `data/talents/misc/races.lua:116-` 遍历 `resources_def` 全部资源，“能量”窄化了 resources；同技能 info（`546a6e96d9`）“你的能量值仍需要满足……最低能量需求”同样窄化。
   - **已裁决（2026-09-29，用户）**：两条的“能量”改为“资源”，排入修复窗口 55；盗贼诗标题 `rogues do it from behind`＝“盗贼在你身后”与 SPELLSHOCKED 长描述省略 temporarily 两项保持不改，关闭。
