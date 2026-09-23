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
