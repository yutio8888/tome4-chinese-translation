本批次（batch-093，条目 entry-03092 至 entry-03131，共 40 条）已完成逐条只读复核。

### 基础信息核验
- **批次文件 SHA-256 核验**：`ec200ae296e7278f8e01902c65b89534a46fb7852b0c716d5f9e5d810f57a220`（核验一致）
- **源码比对依据**：公开源码 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取对应文件）
- **译文基线上下文**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua`）

---

### 逐条复核报告

#### entry-03092
- **位置**：`mod-tome.lua:40038`；`mod-tome/data/zones/telmur/npcs.lua`
- **原文**：`Everybody thought Telos dead and his spirit destroyed, but it seems he still lingers in his old place of power.`
- **译文**：`所有人都认为泰勒已经形神俱灭了，但现在看起来他似乎仍徘徊在他旧日的力量之所。`
- **复核结论**：存在疑点
- **依据**：专名翻译在同 section 语境及上下文中不一致。同 section 的 `mod-tome.lua:40037` 为 `t("The Shade of Telos", "泰勒斯之影", "entity name")`，`mod-tome.lua:40046` 为 `t("Telos's Staff (Bottom Half)", "泰勒斯的法杖（下半部）", "entity name")`，`mod-tome.lua:40048` 为 `t("The bottom part of Telos' broken staff.", "泰勒斯折断法杖的下半部。", "_t")`，均统一译为“泰勒斯”。此处译文将人名“Telos”误译为了“泰勒”，容易与主线 NPC 泰恩（Tannen）或泰尔兰（Tarelion）产生混淆。

#### entry-03093
- **位置**：`mod-tome.lua:40040`；`mod-tome/data/zones/telmur/npcs.lua`
- **原文**：`Back and there again`
- **译文**：`归而复往`
- **复核结论**：未发现问题
- **依据**：源码中为泰勒斯之影死亡弹窗标题（`Dialog:simpleLongPopup(_t"Back and there again", ...)`）。术语快照中该倒装成就/任务标题 preferred 译法即为“归而复往”，译文准确契合。

#### entry-03094
- **位置**：`mod-tome.lua:40064`；`mod-tome/data/zones/tempest-peak/npcs.lua`
- **原文**：`and used in mad electrical reanimation experiments`
- **译文**：`并被用于他疯狂的电击复活实验`
- **复核结论**：未发现问题
- **依据**：源码中为风暴法师乌尔奇斯（Urkis）击杀玩家时的死亡墓碑信息拼接片段（`killer_message`）。译文通顺，准确传达原意。

#### entry-03095
- **位置**：`mod-tome.lua:40092`；`mod-tome/data/zones/temple-of-creation/objects.lua`
- **原文**：
```text
This incredibly beautiful -- and powerful -- trident is made of the rare metal orichalcum. An amazing pearl is seated in head of the trident, as it spreads into three razor sharp prongs.
It is imbued with the greatest strengths of all of the most powerful Naga warriors.
Slasul gave it to you as a sign of his faith in you. It is a sign of hope for all of the Naloren race, that one outside of their tribe could be so trusted.
```
- **译文**：
```text
这柄美得令人难以置信——且威力强大——的三叉戟由稀有的奥利哈刚金属打造而成。一颗璀璨的珍珠镶嵌在叉头处，向前分出三道锋利的尖刺。
它被灌注了所有最强大的娜迦战士的至高力量。
萨拉苏尔将它赐予你，作为他对你信任的象征。它也是纳鲁一族全体的希望——一个部落之外的人竟能获得如此信任。
```
- **复核结论**：未发现问题
- **依据**：源码中为神器“纳鲁一族的遗产”（Legacy of the Naloren）描述。两处换行分段完全对应，破折号使用规范，专名 Naloren（纳鲁一族）、Slasul（萨拉苏尔）、orichalcum（奥利哈刚）翻译精准贴合。

#### entry-03096
- **位置**：`mod-tome.lua:40102`；`mod-tome/data/zones/temple-of-creation/zone.lua`
- **原文**：`#AQUAMARINE#You arrive deep under water, at the sea floor, as you look upwards you only see a glimpse of light coming through.`
- **译文**：`#AQUAMARINE#你深入了水下，来到海床上。当你抬头仰望时，只能隐约看到一丝从水面透下的光。`
- **复核结论**：未发现问题
- **依据**：源码中为玩家初入创造神殿的海底进场提示日志。颜色控制码 `#AQUAMARINE#` 保持完整，语义翻译生动准确，标点无误。

#### entry-03097
- **位置**：`mod-tome.lua:40115`；`mod-tome/data/zones/temporal-rift/grids.lua`
- **原文**：`The rift leads... somewhere.`
- **译文**：`裂缝通向…某个地方。`
- **复核结论**：未发现问题
- **依据**：源码中为时空裂隙入口地形描述。英文省略号转换为中文省略号，语义传达准确。

#### entry-03098
- **位置**：`mod-tome.lua:40124`；`mod-tome/data/zones/temporal-rift/npcs.lua`
- **原文**：`This crazed madman seems twisted and corrupted by temporal energy, his body shifting and phasing in and out of reality.`
- **译文**：`这个疯子似乎被时空能量扭曲并侵蚀，他的身体不断变换，在现实中时隐时现。`
- **复核结论**：未发现问题
- **依据**：源码中为畸变者本·克鲁斯达（Ben Cruthdar, the Abomination）的描述。temporal energy（时空能量）、phasing in and out of reality（在现实中时隐时现）翻译准确传神。

#### entry-03099
- **位置**：`mod-tome.lua:40127`；`mod-tome/data/zones/temporal-rift/npcs.lua`
- **原文**：`Claws and teeth. Ice and death. Dragons are not all extinct it seems...  and this one seems to have been corrupted by the time rift.`
- **译文**：`尖牙利齿，冰冷致命。似乎龙族并没有完全灭绝……而这一只似乎已被时空裂隙所腐蚀。`
- **复核结论**：未发现问题
- **依据**：源码中为畸变冰龙兰萨（Rantha the Abomination）的描述。短句节奏处理自然，省略号规范对应，time rift 译为“时空裂隙”，准确贴切。

#### entry-03100
- **位置**：`mod-tome.lua:40129`；`mod-tome/data/zones/temporal-rift/npcs.lua`
- **原文**：`A six-armed creature, dressed in robes, with black insectile eyes.`
- **译文**：`身穿长袍、有着黑色昆虫样眼睛的六臂生物。`
- **复核结论**：未发现问题
- **依据**：源码中为时空之石双子/克隆体（Chronolith Twin/Clone）的描述。外形特征翻译完整清晰，定语语序符合汉语表达习惯。

#### entry-03101
- **位置**：`mod-tome.lua:40179`；`mod-tome/data/zones/thieves-tunnels/npcs.lua`
- **原文**：`Assassin Lord`
- **译文**：`刺客领主`
- **复核结论**：未发现问题
- **依据**：盗贼密道 BOSS 实体名称，译为“刺客领主”，与全剧固定译名一致。

#### entry-03102
- **位置**：`mod-tome.lua:40181`；`mod-tome/data/zones/thieves-tunnels/npcs.lua`
- **原文**：`#DARK_GREY#The assassin lord throws a smoke bomb and disappears!`
- **译文**：`#DARK_GREY#刺客领主扔下了一个烟雾弹，消失了！`
- **复核结论**：未发现问题
- **依据**：源码中为刺客领主首次受击逃脱时的日志信息。颜色码 `#DARK_GREY#` 保留完好，感叹号匹配，翻译通顺准确。

#### entry-03103
- **位置**：`mod-tome.lua:40205`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`Remove @himher@!`
- **译文**：`干掉@himher@！`
- **复核结论**：未发现问题
- **依据**：源码中为安格利文首领莉娜尼尔与泰尔兰的愤怒喊话（`anger_emote`）。性别替换标记 `@himher@` 保留完整，感叹号对应，口吻自然。

#### entry-03104
- **位置**：`mod-tome.lua:40210`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：源码中为安格利文城镇守卫基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03105
- **位置**：`mod-tome.lua:40214`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`An archmage specializing in fire magic.`
- **译文**：`一位精通火焰法术的大法师。`
- **复核结论**：未发现问题
- **依据**：源码中为炎法师（pyromancer）的描述。符合术语 fire -> 火焰，语义准确。

#### entry-03106
- **位置**：`mod-tome.lua:40216`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`An archmage specializing in ice magic.`
- **译文**：`一位精通冰系法术的大法师。`
- **复核结论**：未发现问题
- **依据**：源码中为冰法师（cryomancer）的描述。法术专精表述通顺自然，与同组实体相称。

#### entry-03107
- **位置**：`mod-tome.lua:40218`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`An archmage specializing in earth magic.`
- **译文**：`一位精通土系法术的大法师。`
- **复核结论**：未发现问题
- **依据**：源码中为地法师（geomancer）的描述。翻译准确通顺。

#### entry-03108
- **位置**：`mod-tome.lua:40220`；`mod-tome/data/zones/town-angolwen/npcs.lua`
- **原文**：`An archmage specializing in lightning magic.`
- **译文**：`一位精通闪电法术的大法师。`
- **复核结论**：未发现问题
- **依据**：源码中为风暴法师（tempest）的描述。符合术语 lightning -> 闪电，翻译准确。

#### entry-03109
- **位置**：`mod-tome.lua:40230`；`mod-tome/data/zones/town-angolwen/objects.lua`
- **原文**：`Lecture on the nature of magic by Archmage Tarelion.`
- **译文**：`大法师泰尔兰关于魔法本质的演讲。`
- **复核结论**：未发现问题
- **依据**：源码中为安格利文传记物品实体描述。专名 Archmage Tarelion 在全库固定统一译为“大法师泰尔兰”，句末标点正确。

#### entry-03110
- **位置**：`mod-tome.lua:40257`；`mod-tome/data/zones/town-derth/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：德斯城镇居民基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03111
- **位置**：`mod-tome.lua:40268`；`mod-tome/data/zones/town-derth/npcs.lua`
- **原文**：`Hey you. Come here.`
- **译文**：`喂！说你呢，到我这儿来。`
- **复核结论**：未发现问题
- **依据**：源码中为德斯城竞技场引路人（ARENA_AGENT）看到玩家时的气泡喊话（`doEmote`）。译文口语化生动贴切，标点准确。

#### entry-03112
- **位置**：`mod-tome.lua:40275`；`mod-tome/data/zones/town-derth/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。相关术语快照明确登记：`Swordsmith | 长剑铁匠铺 | T.GAME.ENTITY | places | entity name | existing | core | 城镇商店实体`。当前译文采用了“铸剑铺”，与术语快照指定的“长剑铁匠铺”不一致。

#### entry-03113
- **位置**：`mod-tome.lua:40293`；`mod-tome/data/zones/town-elvala/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：埃尔瓦拉城镇居民基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03114
- **位置**：`mod-tome.lua:40313`；`mod-tome/data/zones/town-elvala/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。同 entry-03112，术语快照登记为“长剑铁匠铺”（城镇商店实体），当前译文为“铸剑铺”。

#### entry-03115
- **位置**：`mod-tome.lua:40330`；`mod-tome/data/zones/town-gates-of-morning/grids.lua`
- **原文**：`Farportal: Last Hope`
- **译文**：`远行传送门：最后的希望`
- **复核结论**：未发现问题
- **依据**：晨曦之门传送门实体名。Last Hope 符合术语快照“最后的希望”，Farportal 规范译为“远行传送门”，全角冒号匹配。

#### entry-03116
- **位置**：`mod-tome.lua:40331`；`mod-tome/data/zones/town-gates-of-morning/grids.lua`
- **原文**：
```text
A farportal is a way to travel incredible distances in the blink of an eye. They usually require an external item to use. You have no idea if it is even two-way.
This one seems to go near the town of Last Hope in Maj'Eyal.
```
- **译文**：
```text
远行传送门能让人眨眼间跨越难以想象的距离。它们通常需要借助外部物品才能使用。你甚至不知道它是否能双向通行。
这座传送门似乎通往马基·埃亚尔最后的希望城附近。
```
- **复核结论**：未发现问题
- **依据**：两段换行对应完整。专名 Maj'Eyal 符合维护者 2026-08-25 裁定的“马基·埃亚尔”，Last Hope 符合“最后的希望”，语义表达严谨通顺。

#### entry-03117
- **位置**：`mod-tome.lua:40346`；`mod-tome/data/zones/town-gates-of-morning/npcs.lua`
- **原文**：`A beautiful woman, clad in shining plate armour. Power radiates from her.`
- **译文**：`一位身披闪亮板甲的美女。力量从她身上散发出来。`
- **复核结论**：未发现问题
- **依据**：高阶太阳骑士艾琳（Aeryn）描述，翻译完整准确，标点无误。

#### entry-03118
- **位置**：`mod-tome.lua:40361`；`mod-tome/data/zones/town-gates-of-morning/traps.lua`
- **原文**：`Sarah's Herbal Infusions`
- **译文**：`萨拉的草药浸剂店`
- **复核结论**：细微观察
- **依据**：该商店源码绑定 `GATES_POTION`，实际售卖的是自然刻印“纹身”（`type="scroll", subtype="infusion"`）。英文实体名属于双关/字面招牌（表面为草药浸剂/茶，实为纹身店）。译文“萨拉的草药浸剂店”直译了该店名招牌，语义通顺，与 entry-03129（最后的希望同名店铺）保持一致。

#### entry-03119
- **位置**：`mod-tome.lua:40363`；`mod-tome/data/zones/town-gates-of-morning/traps.lua`
- **原文**：`Zemekkys Home`
- **译文**：`泽梅基斯的家`
- **复核结论**：未发现问题
- **依据**：时空法师泽梅基斯住所实体名，专名统一，翻译准确。

#### entry-03120
- **位置**：`mod-tome.lua:40380`；`mod-tome/data/zones/town-irkkk/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：伊尔克城镇居民基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03121
- **位置**：`mod-tome.lua:40384`；`mod-tome/data/zones/town-irkkk/npcs.lua`
- **原文**：`You can literaly feel the mental energies emitted by this yeek.`
- **译文**：`你几乎能真切地感受到这名夺心魔散发出的精神能量。`
- **复核结论**：未发现问题
- **依据**：源码中为夺心魔念力使者描述。yeek 遵循术语快照译为“夺心魔”，mental energies 译为“精神能量”，文意贴切通顺。

#### entry-03122
- **位置**：`mod-tome.lua:40403`；`mod-tome/data/zones/town-irkkk/traps.lua`
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **复核结论**：存在疑点
- **依据**：术语不一致。同 entry-03112、entry-03114，术语快照登记为“长剑铁匠铺”（城镇商店实体），当前译文为“铸剑铺”。

#### entry-03123
- **位置**：`mod-tome.lua:40420`；`mod-tome/data/zones/town-iron-council/grids.lua`
- **原文**：`The Deep Bellow`
- **译文**：`深渊咆哮`
- **复核结论**：未发现问题
- **依据**：铁王座矮人副本地下城入口实体名，全库高度统一译为“深渊咆哮”，准确无误。

#### entry-03124
- **位置**：`mod-tome.lua:40431`；`mod-tome/data/zones/town-iron-council/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：铁王座城镇居民基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03125
- **位置**：`mod-tome.lua:40460`；`mod-tome/data/zones/town-last-hope/grids.lua`
- **原文**：`Farportal: Gates of Morning`
- **译文**：`远行传送门：晨曦之门`
- **复核结论**：未发现问题
- **依据**：最后的希望传送门实体名。Gates of Morning 遵循术语快照译为“晨曦之门”，Farportal 规范译为“远行传送门”，标点匹配。

#### entry-03126
- **位置**：`mod-tome.lua:40464`；`mod-tome/data/zones/town-last-hope/grids.lua`
- **原文**：`#VIOLET#You enter the swirling portal and in the blink of an eye you set foot in sight of the Gates of Morning, with no trace of the portal...`
- **译文**：`#VIOLET#你进入了传送漩涡，一眨眼的功夫你已经来到了能望见晨曦之门的地方，此间毫无传送门的痕迹……`
- **复核结论**：未发现问题
- **依据**：传送门使用日志。颜色代码 `#VIOLET#` 完整，末尾省略号对应保留，专名晨曦之门一致，语义流畅准确。

#### entry-03127
- **位置**：`mod-tome.lua:40471`；`mod-tome/data/zones/town-last-hope/npcs.lua`
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **复核结论**：未发现问题
- **依据**：最后的希望城镇居民基类的愤怒喊话。占位符 `@himher@` 与标点正确。

#### entry-03128
- **位置**：`mod-tome.lua:40490`；`mod-tome/data/zones/town-last-hope/objects.lua`
- **原文**：`the Pale King part %s`
- **译文**：`苍白之王 第%s章`
- **复核结论**：未发现问题
- **依据**：源码调用 `("the Pale King part %s"):tformat(i==1 and _t"one" or _t"two")`。参数占位符 `%s` 保持完好，配合上下文将“one/two”替换后生成“苍白之王 第一章/第二章”，格式化完全正常。

#### entry-03129
- **位置**：`mod-tome.lua:40509`；`mod-tome/data/zones/town-last-hope/traps.lua`
- **原文**：`Sarah's Herbal Infusions`
- **译文**：`萨拉的草药浸剂店`
- **复核结论**：细微观察
- **依据**：同 entry-03118，源码绑定 `POTION` store（机制为出售纹身 Infusion），译文直译店铺招牌，与晨曦之门同名店保持一致。

#### entry-03130
- **位置**：`mod-tome.lua:40513`；`mod-tome/data/zones/town-last-hope/traps.lua`
- **原文**：`Tannen's Door`
- **译文**：`泰恩的门`
- **复核结论**：未发现问题
- **依据**：法师泰恩住所门扉实体。专名 Tannen 严格遵循术语快照 preferred 规定统一译为“泰恩”，准确无误。

#### entry-03131
- **位置**：`mod-tome.lua:40545`；`mod-tome/data/zones/town-point-zero/grids.lua`
- **原文**：`The rift leads to Maj'Eyal.`
- **译文**：`裂隙通往马基·埃亚尔。`
- **复核结论**：未发现问题
- **依据**：零点镇时空裂隙描述。Maj'Eyal 符合维护者 2026-08-25 裁定之“马基·埃亚尔”，句末标点正确，翻译严谨。

---

### 疑点与观察汇总
1. **专名一致性疑点**：
   - `entry-03092`：原文 “Telos” 在译文中被译为“泰勒”，而同 section 上下文及关联物品均一致译为“泰勒斯”（如 `The Shade of Telos` -> `泰勒斯之影`、`Telos's Staff` -> `泰勒斯的法杖`），此处人名翻译脱节。
2. **术语不一致疑点**：
   - `entry-03112`、`entry-03114`、`entry-03122`：原文商店实体名 `Swordsmith` 当前译为“铸剑铺”，而相关术语快照登记为 `长剑铁匠铺`（`T.GAME.ENTITY places entity name existing core 城镇商店实体`）。
3. **机制与字面观察（细微观察）**：
   - `entry-03118`、`entry-03129`：`Sarah's Herbal Infusions` 实际代码逻辑为出售各种自然纹身（Infusion）的商店，当前译文“萨拉的草药浸剂店”为英文双关招牌的字面译法，两城镇翻译一致，传达尚可。
