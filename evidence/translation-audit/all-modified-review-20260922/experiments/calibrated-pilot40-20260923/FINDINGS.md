# 40条最终观察与证据

研究宿主裁决，非人工金标准；ISSUE是文本可证偏差，PENDING是未决事实，OK包括仅建议。DLC实现佐证限哈希快照；目标发行版本未固定。

| entry-ID | 判定 | 确认/未决编号 |
|---|---|---|
| entry-03778 | OK | 未发现确认偏差 |
| entry-03788 | ISSUE | D01 |
| entry-03814 | OK | 未发现确认偏差 |
| entry-03817 | OK | 未发现确认偏差 |
| entry-03824 | PENDING | P02 |
| entry-03830 | OK | 未发现确认偏差 |
| entry-03844 | PENDING | P01 |
| entry-03846 | ISSUE | D02、D03、D04 |
| entry-03847 | ISSUE | D05、D06、D22 |
| entry-03848 | ISSUE | D07、D08、D09 |
| entry-03855 | ISSUE | D10、D11 |
| entry-03863 | ISSUE | D12、D13 |
| entry-03869 | ISSUE | D14、D15、D16、D17 |
| entry-03876 | OK | 未发现确认偏差 |
| entry-03880 | OK | 未发现确认偏差 |
| entry-03885 | PENDING | P03 |
| entry-03886 | OK | 未发现确认偏差 |
| entry-03895 | ISSUE | D18 |
| entry-03907 | ISSUE | D19 |
| entry-03928 | OK | 未发现确认偏差 |
| entry-03929 | OK | 未发现确认偏差 |
| entry-03945 | OK | 未发现确认偏差 |
| entry-03947 | OK | 未发现确认偏差 |
| entry-03948 | PENDING | P04 |
| entry-03964 | OK | 未发现确认偏差 |
| entry-03982 | OK | 未发现确认偏差 |
| entry-03988 | OK | 未发现确认偏差 |
| entry-03989 | OK | 未发现确认偏差 |
| entry-03999 | OK | 未发现确认偏差 |
| entry-04031 | OK | 未发现确认偏差 |
| entry-04036 | OK | 未发现确认偏差 |
| entry-04067 | OK | 未发现确认偏差 |
| entry-04068 | OK | 未发现确认偏差 |
| entry-04073 | OK | 未发现确认偏差 |
| entry-04103 | OK | 未发现确认偏差 |
| entry-04113 | OK | 未发现确认偏差 |
| entry-04120 | OK | 未发现确认偏差 |
| entry-04128 | ISSUE | D20 |
| entry-04133 | ISSUE | D21 |
| entry-04144 | OK | 未发现确认偏差 |

## D01 · entry-03788

原文：`confusing nearby enemies`；译文：`混乱周围生物`。

混乱对象从敌人扩大为周围生物。

最强反证及处理：生物可泛指敌人，但同句周围没有敌方限定；会改变对盟友的理解。

证据：`tome-orcs/data/general/objects/tinkers/chemistry.lua`；chemistry.lua:284,301-315 -> damage_types.lua:296-314 explicitly separates hostile confusion from friendly smoke cover。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D02 · entry-03846

原文：`home steam-pipes`；译文：`蒸汽阀`。

法定检查对象由管道缩为阀门。

最强反证及处理：上句同时提到阀门和接头，但本句home steam-pipes是管路整体。

证据：`tome-orcs/data/lore/emporium.lua`；emporium.lua:77 onward, inspection paragraph。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D03 · entry-03846

原文：`over 40%`；译文：`减少40%`。

超过40%的阈值限定消失。

最强反证及处理：括号仍说明因人而异，但未保留原文最低幅度关系。

证据：`tome-orcs/data/lore/emporium.lua`；emporium.lua, collection-suit paragraph。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D04 · entry-03846

原文：`up to four years in prison`；译文：`并处四年监禁`。

刑期上限改成固定四年；仅文学世界内语义判断。

最强反证及处理：译文的最高只修饰3000金币罚金，后面并处四年没有上限限定。

证据：`tome-orcs/data/lore/emporium.lua`；emporium.lua, last bullet。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D05 · entry-03847

原文：`...thing on?`；译文：`……什么事？`。

录音开场检查机器是否开着，被写成询问事情。

最强反证及处理：原文截断但同篇日志录音语境支持device on。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua:24-34; recording context。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D06 · entry-03847

原文：`journey to the Loyalist's last known position is underway`；译文：`正在准备前往忠诚者的上一个位置`。

正在进行旅程改成准备出发。

最强反证及处理：前句已说准时出发，不能消除本句的准备时序矛盾。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua:34。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D07 · entry-03848

原文：`for posterity`；译文：`为了繁荣`。

为后世留存记录误作繁荣。

最强反证及处理：下句保留子孙后代但不使开头繁荣成为等价目的。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua:39。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D08 · entry-03848

原文：`I assume`；译文：`我保证`。

推测口气被改成保证。

最强反证及处理：两者都可为应和，但认识确定性相反。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua, splendid dialogue。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D09 · entry-03848

原文：`Gurgling.`；译文：`血液流淌之声。`。

咕噜声被确定成血液流淌声。

最强反证及处理：暴力场景可含血，但没有确定声音来源的文字证据。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua, screams/gurgling/crashing direction。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D10 · entry-03855

原文：`the only type of person`；译文：`世界上唯一一个`。

唯一的一类人改成世界上唯一一个个体。

最强反证及处理：中文家伙可泛称，但世界上唯一一个直接收窄数量。

证据：`tome-orcs/data/lore/misc.lua`；misc.lua:106。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D11 · entry-03855

原文：`rich potion-brewer living comfortably`；译文：`安居乐业的普通药水贩子`。

富裕变成普通，去掉与疯狂炼金师相对的发财结果。

最强反证及处理：安居乐业表达舒适生活，但不等于富裕，普通是新增评价。

证据：`tome-orcs/data/lore/misc.lua`；misc.lua:108。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D12 · entry-03863

原文：`Neither can afford direct intervention, but some form of support will assuredly be available.`；译文：`不论是那种，我们都没法直接介入，不过确实可以提供某种支持。`。

谈外部两派无法直接干涉却可支援，被换为己方我们无法干涉并供援。

最强反证及处理：后文谈请小个子协助进一步确认原文支援方向。

证据：`tome-orcs/data/lore/palace-fumes.lua`；palace-fumes.lua, Palaquie reply between negotiation question and tinies response。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D13 · entry-03863

原文：`filthy little greenskins`；译文：`狡猾的小绿人们`。

肮脏的贬称改成狡猾的性格。

最强反证及处理：同为贬低但评价的具体性质不同。

证据：`tome-orcs/data/lore/palace-fumes.lua`；palace-fumes.lua, final Tantalos speech。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D14 · entry-03869

原文：`The damage left`；译文：`魔法大爆炸对那里所造成的伤害`。

把未限定来源的破坏明确归因于魔法大爆炸。

最强反证及处理：世界观可能相关，但本段原文及随后英雄战斗造成的损伤不能证明全由爆炸引起。

证据：`tome-orcs/data/lore/primal-forest.lua`；primal-forest.lua:52-54。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D15 · entry-03869

原文：`may once more tip towards ruin`；译文：`世界濒临毁灭的边缘`。

可能再次恶化改为已经濒临毁灭。

最强反证及处理：汉语描述危险，仍将可能趋势写成当前现实。

证据：`tome-orcs/data/lore/primal-forest.lua`；primal-forest.lua, opening paragraph。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D16 · entry-03869

原文：`where you explored, when`；译文：`记录下各种观察到的生物的分布和数量`。

调查记录要求的时间信息遗漏。

最强反证及处理：分布与数量涵盖地点和多少，不涵盖何时调查。

证据：`tome-orcs/data/lore/primal-forest.lua`；primal-forest.lua, learning/observing paragraph。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D17 · entry-03869

原文：`endangered or invasive`；译文：`濒临灭绝或受到入侵`。

物种成为入侵种变成物种受到入侵，生态监测对象关系反转。

最强反证及处理：前面的扩散监测不能改正后面明确的受动入侵。

证据：`tome-orcs/data/lore/primal-forest.lua`；primal-forest.lua, same paragraph。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D18 · entry-03895

原文：`at most %d distance to return to you`；译文：`最多飞行 %d 然后折回你`。

返程最大距离被移成折返之前飞行距离。

最强反证及处理：此前已经说明折返，但本句然后明确将数值接在折返前。

证据：`tome-orcs/data/talents/celestial/sol.lua`；sol.lua:52,58-79,102-103; newrange passed to homing return。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D19 · entry-03907

原文：`all foes in radius %d`；译文：`半径 %d 码内的所有单位`。

敌方范围扩大为所有单位。

最强反证及处理：首句目标没有限定扩散对象；所有单位明确包含盟友。

证据：`tome-orcs/data/talents/psionic/action-at-a-distance.lua`；action-at-a-distance.lua:186-197,209-213 friendlyfire=false corroborates text。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D20 · entry-04128

原文：`Your mere presence is a blight in your foes minds.`；译文：`链接目标，偷取目标一个技能。`。

存在本身侵蚀敌人心智的叙事前提没有表达；仅保留连接和偷技能。

最强反证及处理：机制句可以解释如何偷取，不能表达前句被删的存在影响。

证据：`tome-possessors/data/talents/psionic/deep-horror.lua`；Frozen entries.json and context.lua; Possessors source unavailable。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D21 · entry-04133

原文：`You may only steal the body`；译文：`你可能只会偷走`。

许可/限制may only误作可能性，弱化可偷取类型的硬性条件。

最强反证及处理：后句可学习新类型为限制提供线索，但不消除当前限定被写成概率。

证据：`tome-possessors/data/talents/psionic/possession.lua`；Frozen entries.json and context.lua; text claim only。

归因：translation-introduced unless explicitly noted。文本结论：confirmed；目标适用性：DLC target version unpinned; pure text findings independent of version; mechanism corroboration is snapshot-only。

## D22 · entry-03847

原文：`as soon as he can un-kick the hornet's nest`；译文：`要不是他刚刚给我们捅了个大马蜂窝`。

先解决自己制造的混乱才给茶的条件，被替换为只责备此前制造混乱。

最强反证及处理：讽刺与不给茶的态度仍可从语境读出，但先解决麻烦的条件没有保留。

证据：`tome-orcs/data/lore/gem.lua`；gem.lua:32, whole reply to tea-maker demand。

归因：translation-introduced。文本结论：confirmed；目标适用性：pure text; DLC target version unpinned。

## P01 · entry-03844

pinaciphobia 的罕见词义与笑点需要可靠词源/作者语境证据。Opus 未给词义来源，宿主不能仅凭其自信确认。

证据：Opus C02; emporium.lua:40; host supplementary lexical search found popular lists but not a decisive lexicographic entry in checked AlphaDictionary page.。文本：pending；适用性：lexical meaning gap, not DLC version gap。

## P02 · entry-03824

中英文都称附近所有生物，快照只收集hostile并检查teleport。属于上游范围概括，目标版本适用性未定。

证据：world-artifacts.lua:2245–2255。文本：translation faithful; upstream discrepancy；适用性：DLC unpinned。

## P03 · entry-03885

中英文限定敌人命中，快照负能量回复分支只排除自身与自身召唤物；是否包含其他友军需目标版本链路。

证据：cosmic.lua:50–61; host pre-reveal finding。文本：translation faithful; upstream discrepancy；适用性：DLC unpinned; local callback evidence only。

## P04 · entry-03948

中英文半径嘲讽与快照定义tg2但project(tg)不符；本体投射语义及DLC目标版本适用性仍有限定。

证据：mecharachnid.lua:760–770; host initial and Opus C18。文本：translation faithful; upstream discrepancy；适用性：DLC unpinned。
