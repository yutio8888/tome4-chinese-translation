# 待用户集中审阅的争议条目

以下条目依据用户 2026-09-23 指示集中记录：有争议的条目列入 pending，不在当前修复窗口修改，也不阻塞窗口收束。前三条均来自窗口 8 的 `ADJUDICATION-R0.json`。

## 窗口 8 待审阅

1. `e92433bcba`（unlock-yeek）
   - 英文要点：叙事文本中的 `cunning`。
   - 现译：“灵巧”。术语库记录 `Cunning=灵巧`，类别为 stat name，`status=existing`。
   - 争议理由：宿主此前依据术语记录判定保持；surface、Opus contextual 与本轮 reviewer 共三个模型认为叙事语境应译为“机敏”或“狡黠”，且 `existing` 不代表覆盖所有语境。
   - 建议选项：保持“灵巧” / 叙事语境改“机敏”。

2. `e951739433`（毒素风暴）
   - 英文要点：`Each possible effect is equally likely`。
   - 现译：“中毒几率在可能的毒素效果中平分”。
   - 争议理由：源码 `damage_types.lua` 先等概率抽取效果，再判断目标能否中毒；宿主曾判现译与等概率语义等价，reviewer 认为现译把“效果等概率”写成了“中毒几率分配”。
   - 建议选项：保持 / 改为“各种可能的效果出现几率相同”。

3. `e988482539`（龙族传说）
   - 英文要点：“The common man may scoff at the idea of classifying dragons as an intelligent race”。
   - 现译：“嘲笑我把龙作为单独列出的智慧种族”，含原文没有的第一人称。
   - 争议理由：reviewer 两次指出原文没有“我”；宿主认为该系列是 Loremaster Greynot 的第一人称著作，语境允许这一增译。
   - 建议选项：保持 / 改为“嘲笑将龙归为智慧种族的想法”。

## 审核 254 的其他观察

- 宿主补充观察 `e923d2b8d0`：`The target is using talents without consuming resources` 现译为“不再消耗能量”，将 `resources` 窄化为“能量”。
- 审核 254 advisory：`ALL_DREAMS` 以外无其他同类项；另保留 `rogues do it from behind` 标题双关，以及 `SPELLSHOCKED` 省略 `temporarily` 两项建议。

## 审核 255 待审阅

4. `14568237c4`（种族解锁叙事，yeek）
   - 英文要点：`yet they are a cunning and willful race`。
   - 现译：“非常灵巧而且意志强大”。
   - 争议理由：与第 1 项为同一 `cunning=灵巧` 叙事语境争议的另一条目，应随第 1 项一并裁定。
   - 建议选项：同第 1 项。

5. `a1e95a2f4c`（毒素风暴，另一副本）
   - 英文要点：`Each possible effect is equally likely`。
   - 现译：“中毒几率在可能的毒素效果中平分”。
   - 争议理由：与第 2 项相同措辞的另一条目，应随第 2 项一并裁定。
   - 建议选项：同第 2 项。

6. `ea75bd3673`（技能名 `Matter is Energy`）
   - 源码：`psionic/finer-energy-manipulations.lua:126`，消耗一颗宝石换取每回合超能力值。
   - 现译：“宝石能量”，按功能意译，没有体现原名“物质即能量”。
   - 争议理由：改技能名会影响跨条目引用和命名策略；contextual reviewer 判为 OK。
   - 建议选项：保持“宝石能量” / 改为“物质即能量”（需同步引用处）。

- 审核 255 advisory：巫妖外观名 `Lich Regalia` 译作“巫妖王冠”；召唤触手描述 `Ewwww..` 译作“额……”，语气偏迟疑。

## 审核 256 待审阅

8. `eab2ffb632`（技能名 `Blunt Thrust`）
   - 源码：`spells/staff-combat.lua:141`，法杖近战单体攻击并眩晕。
   - 现译：“钝器挥击”；Thrust 为刺击/戳击，现名把动作译成挥击。
   - 争议理由：改技能名需同步技能引用与日志文本（如 `You cannot use Blunt Thrust without a staff weapon!`）。
   - 建议选项：保持“钝器挥击” / 改为“钝击突刺”或“法杖突刺”等（需同步引用处）。

9. `eb6bf55a91`（传说标题 `If I Should Die Before I Wake`）
   - 源码：`lore/misc.lua:623`，标题借用睡前祷词句式。
   - 现译：“从噩梦中惊醒，还是在梦魇中永眠？”，为意译改写。
   - 争议理由：非机制内容，是否直译属风格取舍。
   - 建议选项：保持意译 / 改为“若我在醒来前死去”。

10. `eb71935d6c`（神器名 `Crystal Shard`）
    - 源码：`boss-artifacts-maj-eyal.lua:643–648`，magestaff 唯一神器，未鉴定名 crystalline tree branch。
    - 现译：“水晶之杖”，以物品类型替换 Shard（碎片）；surface 与 contextual 均提出。
    - 争议理由：神器专名改名属命名决定。
    - 建议选项：保持“水晶之杖” / 改为“水晶碎片”。

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

## 审核 261 待审阅

12. `f09f7b5baf`（技能名 `Virulent Strike`）
   - 源码：`talents/corruptions/scourge.lua:25–26`，显示名 Virulent Strike，short_name 仍为 `REND`；实现为双持两击，每次命中延长目标身上持续时间最短的一种疾病。
   - 现译：“撕裂”（沿用旧名 Rend），未体现 virulent（致病、剧毒），也不对应疾病延长的效果。
   - 争议理由：改技能名需要同步日志 `You cannot use Virulent Strike without two weapons!`（mod-tome.lua:22961），“撕裂”族另有 Lacerating Strikes=撕裂挥击 等；属于命名决定。
   - 建议选项：保持“撕裂” / 改为“瘟毒打击”“剧毒打击”一类（需同步引用处）。

13. `f009c2b19b`（死亡描述 `grandfathered`，时间伤害）
   - 源码：`damage_types.lua:1006` 的时间伤害 death_message 列表；`PartyDeath.lua:71` 随机取一项代入死讯模板“was %s to death”，中文模板为“玩家%s……%s而死”（mod-tome.lua:1412）。
   - 现译：“因弹指间度过了无数美好的青葱岁月，转瞬间你已白发苍苍”，把祖父悖论梗改成衰老致死；句中含“你”，代入第三人称死讯后人称和句法错位。
   - 争议理由：死亡描述词表整族已由用户 2026-09-16 裁定继续 pending；本条是该族的新证据（人称错位，而不只是增添意象），单独修改会造成族内不一致。
   - 建议选项：保持并随整族处理 / 单独改为“被祖父悖论抹去”一类短语。

## 审核 262 待审阅

14. `f1403b3e60`（神器名 `Exiler`）
   - 源码：`objects/world-artifacts.lua:6833`，时空术士 Solith 的独特戒指（unided_name insignia ring）。
   - 现译：“放逐”，把施事名词译成了动作。
   - 争议理由：神器专名改名属命名决定（先例：Crystal Shard 已列 pending）。
   - 建议选项：保持“放逐” / 改为“放逐者”。

15. `f181f499b6`（技能系 `Crimson Templar`）
   - 源码：`talents/cursed/cursed.lua:46`，堕落圣骑士由 Guardian（守卫）转化而来的技能系（`uber/wil.lua:399`、`texts/unlock-paladin_fallen.lua:36`）。
   - 现译：“赤红守卫”，未体现 Templar（圣殿骑士），与 Guardian=守卫 只差修饰。
   - 争议理由：技能系改名需要同步说明与解锁文本中的引用，属命名决定。
   - 建议选项：保持“赤红守卫” / 改为“赤红圣殿骑士”“血色圣殿骑士”一类（需同步引用处）。

## 修复窗口 16 待审阅

16. 世界名 `Eyal`（全库译“埃亚尔大陆”）
   - 源码：Eyal 是整个世界的名称（如 `mod-tome.lua:6013` 源文 “This orb seems to represent the world of Eyal as a whole”；`talents/uber/str.lua:311` “far beyond Eyal”），Maj'Eyal 才是大陆（术语库 places.tsv 已定“马基·埃亚尔”）。
   - 现译：“埃亚尔大陆”，把世界限定成了大陆；mod-tome.lua 与 tome-ashes-urhrok.lua 各 23 处，engine.lua、mod-boot.lua 各 1 处；术语库无 Eyal 记录。
   - 争议理由：窗口 16 REVIEW(0) 在星辰契约条目上提出；属全库改名与新增术语记录，超出现有授权，未在窗口内修改（advisory）。
   - 建议选项：保持“埃亚尔大陆” / 改为“埃亚尔”或“埃亚尔世界”（需新增术语记录并全库同步，含 `of Eyal`=“埃亚尔之”等派生）。

17. `f18f9a4e90` 等（lore “An undead hunter's guide, by Aslabor Borys”）
   - 源码：`lore/fun.lua:217` 署名；同一 lore 的条目名与说明见 `mod-tome.lua:11440–11441`。作者是活人猎手（正文自述砍下吸血鬼头颅、请人喝酒）。
   - 现译：标题（11440–11441）“不死猎人指南”；正文署名已在窗口 16 第 2 轮改为“一名不死生物猎人的指南”以消歧；另一处 lore 中 undead hunters 译“亡灵猎手”。
   - 争议理由：窗口 16 FINAL(1) 认为“不死猎人”易读作“不死的猎人”；宿主认为“X猎人”惯例读作猎杀X者（如恶魔猎人），且标题属窗口外条目；为使 FINAL 收敛，窗口内只改了正文署名，两处标题留待决定。
   - 建议选项：标题保持“不死猎人指南” / 两处标题改为“不死生物猎人指南”与正文一致（或统一为“亡灵猎手”）。

## 审核 267 待审阅

18. `f6cc31f278`（死亡描述，枯萎伤害）
   - 源码：`damage_types.lua:909` 枯萎伤害 death_message 列表中的 `debilitated by noxious blight before falling`；`PartyDeath.lua:71,107` 随机取一项代入死讯模板。
   - 现译：“死前吸入过多剧毒瘴气”，把“被剧毒枯萎削弱”写成吸入过量毒气；枯萎（blight）是腐化类伤害而非气体。
   - 争议理由：surface 与 Opus contextual 均判 ISSUE；但死亡描述词表整族已由用户 2026-09-16 裁定继续 pending（第 13 项先例），单改一条会造成族内不一致。
   - 建议选项：保持并随整族处理 / 单独改为“被剧毒枯萎折磨致衰弱”一类短语。

## 修复窗口 25 待审阅

19. `fad7958eaa`（效果 `BLOODCASTING` 的长描述 “Corruptions consume health instead of vim.”）
   - 源码：`timed_effects/magical.lua:2455–2470` 效果只加 `bloodcasting=1`；`class/Actor.lua:5576–5592` 的 `incVim` 在活力足够时照常扣活力，只有活力不足时才以生命值支付缺额（倍率 `bloodcasting/100`，该效果下为 0.01；无此属性时为 2）。
   - 现译：“堕落系法术消耗生命值而非活力值。”——忠实于英文原句，但英文本身把“缺额用生命支付”说成了“以生命代替活力”。
   - 争议理由：窗口 25 REVIEW(0) 指出与机制不符；宿主核实机制属实，但这是上游原文与实现的矛盾，不是译文缺陷（advisory）。是否在译文中按实现改写原文说法属策略决定。
   - 建议选项：保持忠实原文 / 改为按实现描述，如“活力不足时，堕落系法术以生命值支付不足部分。”

## 审核 276 待审阅

20. `ff891672cb`（神器名 `Sceptre of the Archlich`）
   - 源码：固定主游戏 `world-artifacts.lua:2637`，名称含 `Archlich`，与巫妖套装关联。
   - 现译：“死灵权杖”，未明确表达 Archlich；surface 与重冻 contextual 均提出。
   - 争议理由：神器专名改名须与套装及引用一致，术语库尚无 Archlich 的固定译法。
   - 建议选项：保持“死灵权杖” / 改为“大巫妖权杖”一类并同步相关引用。

21. `0c451e854a`（DLC 技能与效果名 `Armoured Leviathan`）
   - 源码：公开 Ashes DLC `timed_effects.lua:637`；本批文件 SHA 匹配，来源仓库与 commit 未固定。同族技能、效果和日志使用同名。
   - 现译：“重装上阵”，统一意译但未表达 Leviathan 的巨兽意象；surface 提出，重冻 contextual 判 OK。
   - 争议理由：若改名，需同步技能、效果及 +/- 日志，属跨条命名决定。
   - 建议选项：保持“重装上阵” / 选定含巨兽意象的新名并同步同族条目。

## 审核 277 待审阅

22. `1dafd3a728`（Ashes 效果名 `Corruption of the Doomed`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:1045–1052`，本批 workset 文件 SHA 匹配；来源仓库与 commit 未固定。效果名及 +/- 日志同族使用，相关条目现译统一“腐化形态”。
   - 现译：“腐化形态”，没有表达 `Doomed`；surface 提出，合规重冻 contextual 判 OK。
   - 争议理由：更名需同步四处效果／日志及可能的技能引用，属于跨条专名决定，本批不单改。
   - 建议选项：保持“腐化形态” / 选定包含“厄运”或“受诅者”含义的新名并同步同族条目。

## 审核 278 待审阅

23. `3747432e7d`（Ashes 效果日志 `+Osmosis Regen`）
   - 源码：公开 Ashes DLC `data/timed_effects.lua:523–530`，效果名 `Osmosis Regeneration`，日志 `+/-Osmosis Regen`；长描述说明在效果期间回复生命值。本批 workset 文件 SHA 匹配，来源仓库和 commit 未固定。
   - 现译：“+渗透吸收”；同族效果名和减益日志也统一使用“渗透吸收”。
   - 争议理由：现译未明示 Regen 的回复含义，但单改一条日志会破坏同族命名一致性，需要决定整族译名。
   - 建议选项：保持“渗透吸收” / 确定包含“回复”或“再生”的新名并同步效果名及 +/- 日志。
