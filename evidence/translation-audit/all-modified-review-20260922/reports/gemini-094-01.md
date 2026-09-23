本次复核针对批次 **batch-094**（条目范围：`entry-03132` 至 `entry-03171`，共 40 条）。
已核对批次文件 SHA-256 哈希值为 `5d2b5ac10761b2ea140310659ccfef392fe3c1a9016cfcaee51c09d3f3e51943`，哈希校验一致。
公开源码依据 `source-access.json` 规定的固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/`）进行比对验证。

逐条复核报告如下：

---

### entry-03132
- **编号**：entry-03132
- **位置**：`mod-tome.lua:40557`（`mod-tome/data/zones/town-point-zero/npcs.lua`）
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **结论**：未发现问题
- **核验依据**：源码中对应 `BASE_NPC_POINT_ZERO_TOWN` 的 `anger_emote`。引擎人称代词标记 `@himher@` 完整保留，感叹号全角化，翻译准确无误。

---

### entry-03133
- **编号**：entry-03133
- **位置**：`mod-tome.lua:40560`（`mod-tome/data/zones/town-point-zero/npcs.lua`）
- **原文**：`elemental`
- **译文**：`元素生物`
- **结论**：未发现问题
- **核验依据**：源码中对应 `BASE_NPC_LOSGOROTH` 的 `type = "elemental"`。在 `entity type` 语境下完全符合术语库 preferred 规范（统一为“元素生物”，与作为效果/关键词的“元素”区分）。

---

### entry-03134
- **编号**：entry-03134
- **位置**：`mod-tome.lua:40562`（`mod-tome/data/zones/town-point-zero/npcs.lua`）
- **原文**：`Losgoroth are mighty void elementals, native to the void between the stars; they are rarely seen on the planet's surface.`
- **译文**：`洛斯格罗斯是强大的虚空元素生物，原生于群星之间的虚空。在星球表面几乎看不到这种生物。`
- **结论**：未发现问题
- **核验依据**：源码对应 `BASE_NPC_LOSGOROTH` 的实体描述 `desc`。“void elementals”准确对应“虚空元素生物”，分句通顺，语义与原文完全一致。

---

### entry-03135
- **编号**：entry-03135
- **位置**：`mod-tome.lua:40564`（`mod-tome/data/zones/town-point-zero/npcs.lua`）
- **原文**：`Zemekkys, Grand Keeper of Reality`
- **译文**：`泽梅基斯，现实至高守护者`
- **结论**：未发现问题
- **核验依据**：源码对应 NPC `ZEMEKKYS` 的名称。头衔“Grand Keeper of Reality”完全符合术语库既有 preferred 规范（“现实至高守护者”），音译与头衔均准确。

---

### entry-03136
- **编号**：entry-03136
- **位置**：`mod-tome.lua:40576`（`mod-tome/data/zones/town-point-zero/objects.lua`）
- **原文**：`An iridescent shard of violet crystal.  Its light ebbs and flows, sometimes fast and sometimes slow, keeping pace with the chaotic streams of time itself.  It makes you feel both old and young, a newborn child and an ancient being, your flesh simply one instance in a thousand refractions of a single timeless and eternal soul.`
- **译文**：`这是一块闪着虹彩的紫色水晶碎片。它的光芒忽明忽暗、时缓时快，与时间本身的混乱流动同步。握着它时，你感到自己既年轻又苍老，既是初生的婴孩又是远古的存在；你的肉身不过是同一个超越时间的永恒灵魂在千重折射中的一个影像。`
- **结论**：未发现问题
- **核验依据**：源码对应神器 `TIME_SHARD`（Shard of Crystalized Time）的描述。行文优雅流畅，修辞准确契合原意，标点符号规范。

---

### entry-03137
- **编号**：entry-03137
- **位置**：`mod-tome.lua:40586`（`mod-tome/data/zones/town-point-zero/traps.lua`）
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **结论**：细微观察
- **核验依据**：源码中对应零点圣域的剑类商店入口（`SWORD_WEAPON_STORE`）。术语快照中词头记录为“长剑铁匠铺”（`Swordsmith	长剑铁匠铺	T.GAME.ENTITY	places	entity name`）。经查 `mod-tome.lua`，全库所有 5 处城镇商店（第 40275、40313、40403、40586、40618 行）均统一译为“铸剑铺”。“铸剑铺”符合中文商业门牌表达且全库完全统一，但与术语快照存在细微字面出入。

---

### entry-03138
- **编号**：entry-03138
- **位置**：`mod-tome.lua:40607`（`mod-tome/data/zones/town-shatur/npcs.lua`）
- **原文**：`Catch @himher@!`
- **译文**：`抓住@himher@！`
- **结论**：未发现问题
- **核验依据**：源码对应夏特尔镇守卫的 `anger_emote`。人称标记 `@himher@` 准确保留，感叹号全角化。

---

### entry-03139
- **编号**：entry-03139
- **位置**：`mod-tome.lua:40618`（`mod-tome/data/zones/town-shatur/traps.lua`）
- **原文**：`Swordsmith`
- **译文**：`铸剑铺`
- **结论**：细微观察
- **核验依据**：源码对应夏特尔镇的剑类武器商店（`SWORD_WEAPON_STORE`）。同 entry-03137，全库城镇商店均统一译为“铸剑铺”，与术语快照“长剑铁匠铺”存在字面差异。

---

### entry-03140
- **编号**：entry-03140
- **位置**：`mod-tome.lua:40619`（`mod-tome/data/zones/town-shatur/traps.lua`）
- **原文**：`Nature's Punch`
- **译文**：`自然的重击`
- **结论**：未发现问题
- **核验依据**：源码对应夏特尔镇的重锤武器店（`MAUL_WEAPON_STORE`）。店名翻译生动形象，与伊格镇的同名商店（entry-03142）保持一致。

---

### entry-03141
- **编号**：entry-03141
- **位置**：`mod-tome.lua:40622`（`mod-tome/data/zones/town-shatur/traps.lua`）
- **原文**：`Night's Star`
- **译文**：`暗夜之星`
- **结论**：未发现问题
- **核验依据**：源码对应夏特尔镇的灵晶商店（`MINDSTAR`）。商店专名翻译准确得体。

---

### entry-03142
- **编号**：entry-03142
- **位置**：`mod-tome.lua:40665`（`mod-tome/data/zones/town-zigur/traps.lua`）
- **原文**：`Nature's Punch`
- **译文**：`自然的重击`
- **结论**：未发现问题
- **核验依据**：源码对应伊格镇的钉头锤武器店（`MACE_WEAPON_STORE`）。与 entry-03140 保持一致，翻译准确。

---

### entry-03143
- **编号**：entry-03143
- **位置**：`mod-tome.lua:40705`（`mod-tome/data/zones/trollmire/npcs.lua`）
- **原文**：
```text
Big, brawny, powerful and with a taste for Halfling.
He is wielding a small tree trunk and lumbering toward you.
This is the troll the notes spoke about, no doubt.
```
- **译文**：
```text
高大、魁梧、力大无穷，且嗜食半身人。
他抡着一根小树的树干，正笨重地朝你挪来。
这就是那些碎纸片上提到的巨魔，绝对没错。
```
- **结论**：未发现问题
- **核验依据**：源码对应首领巨魔比尔（`TROLL_BILL`）的描述。换行严格对齐，“Halfling”符合术语规范“半身人”，情节描写传神贴切。

---

### entry-03144
- **编号**：entry-03144
- **位置**：`mod-tome.lua:40710`（`mod-tome/data/zones/trollmire/npcs.lua`）
- **原文**：`and clobbered into soup`
- **译文**：`并被打成肉泥`
- **结论**：未发现问题
- **核验依据**：源码对应巨魔比尔的 `killer_message`，在击杀玩家时拼接在日志后。译为“并被打成肉泥”符合中文语法与击杀语境。

---

### entry-03145
- **编号**：entry-03145
- **位置**：`mod-tome.lua:40732`（`mod-tome/data/zones/tutorial/npcs.lua`）
- **原文**：
```text
Green-skinned and ugly, this massive humanoid glares at you, clenching wart-covered green fists.
He looks hurt.
```
- **译文**：
```text
绿皮丑陋，这只巨大的人形生物正盯着你，握紧了满是肉瘤的绿色拳头。
他看起来受伤了。
```
- **结论**：未发现问题
- **核验依据**：源码对应教程中半死森林巨魔（`TUTORIAL_NPC_TROLL`）的描述。“humanoid”准确翻译为“人形生物”（符合术语规范），换行对齐一致。

---

### entry-03146
- **编号**：entry-03146
- **位置**：`mod-tome.lua:40766`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`This portal will bring you back to the Tutorial Lobby.`
- **译文**：`这道传送门将把你带回教程大厅。`
- **结论**：未发现问题
- **核验依据**：源码对应 `PORTAL_BACK` 和 `PORTAL_BACK_2` 的描述，语义准确明了。

---

### entry-03147
- **编号**：entry-03147
- **位置**：`mod-tome.lua:40776`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Contains a snippet of ToME wisdom.`
- **译文**：`包含了 ToME 智慧的残片。`
- **结论**：未发现问题
- **核验依据**：源码对应教程路标（`SIGN` 等）的描述，语义通顺准确。

---

### entry-03148
- **编号**：entry-03148
- **位置**：`mod-tome.lua:40778`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Causes the player's brain to jettison all recently-acquired knowledge.`
- **译文**：`可以净化玩家的大脑，使玩家遗忘所有最近所学的技能。`
- **结论**：未发现问题
- **核验依据**：源码对应重置符文 `UNLEARN_ALL` 的描述，踩踏后触发 `unlearnTalent` 移除全部教程技能。译文将抽象的“knowledge”结合机制具体化为“技能”，准确符合游戏机制行为。

---

### entry-03149
- **编号**：entry-03149
- **位置**：`mod-tome.lua:40781`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Shove'.`
- **译文**：`可习得技能“推挤”。`
- **结论**：细微观察
- **核验依据**：源码对应 `LEARN_PHYS_KB` 的描述。译文采用中文双引号对应英文单引号，且与相邻日志行（第 40782 行“你学会了技能推挤”）一致。观察到同文件实体名第 40780 行使用了“冲撞”（“启蒙符文：冲撞”），talent name 处（第 27003 行）使用了“击退攻击”；虽存在同名技能在跨条目间的译名差异，但当前条目表意准确，无机制误导。

---

### entry-03150
- **编号**：entry-03150
- **位置**：`mod-tome.lua:40785`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Mana Gale'.`
- **译文**：`可习得技能“法力风暴”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_SPELL_KB` 的描述。与同文件实体名“启蒙符文：法力风暴”保持一致，标点规范，翻译准确。

---

### entry-03151
- **编号**：entry-03151
- **位置**：`mod-tome.lua:40788`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Telekinetic Punt'.`
- **译文**：`可习得技能“念力推送”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_MIND_KB` 的描述。与同文件实体名“启蒙符文：念力推送”保持一致，标点规范，翻译准确。

---

### entry-03152
- **编号**：entry-03152
- **位置**：`mod-tome.lua:40791`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Blink'.`
- **译文**：`可习得技能“闪现”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_SPELL_BLINK` 的描述。技能名“闪现”统一规范，标点正确。

---

### entry-03153
- **编号**：entry-03153
- **位置**：`mod-tome.lua:40794`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Fear'.`
- **译文**：`可习得技能“恐惧”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_MIND_FEAR` 的描述。符合术语库规范（fear -> 恐惧），标点正确。

---

### entry-03154
- **编号**：entry-03154
- **位置**：`mod-tome.lua:40797`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Bleed'.`
- **译文**：`可习得技能“流血”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_SPELL_BLEED` 的描述。符合术语库规范（bleed -> 流血），标点正确。

---

### entry-03155
- **编号**：entry-03155
- **位置**：`mod-tome.lua:40800`（`mod-tome/data/zones/tutorial-combat-stats/grids.lua`）
- **原文**：`Teaches the player 'Confusion'.`
- **译文**：`可习得技能“混乱”。`
- **结论**：未发现问题
- **核验依据**：源码对应 `LEARN_MIND_CONFUSION` 的描述。符合术语库规范（confusion -> 混乱），标点正确。

---

### entry-03156
- **编号**：entry-03156
- **位置**：`mod-tome.lua:40817`（`mod-tome/data/zones/tutorial-combat-stats/npcs.lua`）
- **原文**：
```text
Green-skinned and ugly, this massive humanoid glares at you, clenching wart-covered green fists.
He looks hurt.
```
- **译文**：
```text
绿皮丑陋，这只巨大的人形生物正盯着你，握紧了满是肉瘤的绿色拳头。
他看起来受伤了。
```
- **结论**：未发现问题
- **核验依据**：源码对应教程战斗测试区巨魔（`TUTORIAL_NPC_TROLL`）的描述。与 entry-03145 完全一致，换行及术语一致无误。

---

### entry-03157
- **编号**：entry-03157
- **位置**：`mod-tome.lua:40827`（`mod-tome/data/zones/tutorial-combat-stats/npcs.lua`）
- **原文**：`Pushy orc`
- **译文**：`推搡的兽人`
- **结论**：未发现问题
- **核验依据**：源码对应 NPC `PUSHY_ORC` 的名称，该 NPC 在教程中用来演示精神击退技能（`TUTORIAL_MIND_KB`）。译为“推搡的兽人”契合机制演示设定。

---

### entry-03158
- **编号**：entry-03158
- **位置**：`mod-tome.lua:40834`（`mod-tome/data/zones/tutorial-combat-stats/npcs.lua`）
- **原文**：`Pushy elf`
- **译文**：`推搡的精灵`
- **结论**：未发现问题
- **核验依据**：源码对应 NPC `PUSHY_ELF` 的名称，该 NPC 在教程中演示法术击退技能（`TUTORIAL_SPELL_KB`）。与 entry-03157 结构对称统一。

---

### entry-03159
- **编号**：entry-03159
- **位置**：`mod-tome.lua:40860`（`mod-tome/data/zones/tutorial-combat-stats/objects.lua`）
- **原文**：`A beautiful amulet that increases your Mindpower by 3.`
- **译文**：`一条精美的项链，可以提高你3点精神强度。`
- **结论**：未发现问题
- **核验依据**：源码对应 `MINDPOWER_AMULET` 的描述，属性加成为 `combat_mindpower = 3`。“Mindpower”符合术语库 preferred 规范“精神强度”（与 Willpower 意志区分），数值与机制对应准确。

---

### entry-03160
- **编号**：entry-03160
- **位置**：`mod-tome.lua:40912`（`mod-tome/data/zones/unhallowed-morass/grids.lua`）
- **原文**：
```text
The rift has brought you back to Point Zero, and the source of the disturbances.
A temporal defiler is attacking the town, all the Keepers in range are attacking it!
```
- **译文**：
```text
这个裂隙将你带回到了零点圣域，你看到了这些混乱的源头。
一只时空污秽魔正在攻击圣域，附近所有的守卫都在攻击它！
```
- **结论**：未发现问题
- **核验依据**：源码对应返回零点圣域传送门（`RIFT_HOME`）触发的长弹窗文本。“Point Zero”符合术语库 preferred 规范“零点圣域”；“temporal defiler”准确对应前置文件中的首领怪物名称“时空污秽魔”（`mod-tome.lua:40571`）；换行对齐一致。

---

### entry-03161
- **编号**：entry-03161
- **位置**：`mod-tome.lua:40932`（`mod-tome/data/zones/unhallowed-morass/npcs.lua`）
- **原文**：`Easily as big as a horse, this giant spider menaces at you with claws and fangs.`
- **译文**：`这只巨型蜘蛛足有一匹马那么大，用利爪和獠牙威胁着你。`
- **结论**：未发现问题
- **核验依据**：源码对应命织蛛（`fate spinner`）的描述，语义忠实生动。

---

### entry-03162
- **编号**：entry-03162
- **位置**：`mod-tome.lua:41014`（`mod-tome/data/zones/void/grids.lua`）
- **原文**：`The rift leads... somewhere.`
- **译文**：`裂缝通向…某个地方。`
- **结论**：未发现问题
- **核验依据**：源码对应虚空区域 `RIFT` 的描述，省略号规范转为中文省略号，翻译准确。

---

### entry-03163
- **编号**：entry-03163
- **位置**：`mod-tome.lua:41023`（`mod-tome/data/zones/void/npcs.lua`）
- **原文**：
```text
During the Age of Haze nearly all gods were destroyed by the Sher'tul Godslayers. However, a small number escaped.
Gerlyk, the creator of the Human race, prefered to flee into the void between the stars than to face death. He has been trapped ever since.
The sorcerers tried to bring him back and nearly succeeded.
Now you have come to finish what the Sher'tul began. Become a Godslayer yourself.
```
- **译文**：
```text
在混沌纪，几乎大部分神祇都被夏·图尔的弑神者所杀。但仍有少部分逃离。
盖里克，人类缔造者，则选择走进群星间的虚空来避免死亡。他从此一直被困在那里。
巫师们曾试图将他召回，并且险些成功。
现在是你结束夏·图尔人未完成事业的时刻了，去成为一名弑神者吧。
```
- **结论**：未发现问题
- **核验依据**：源码对应创世神盖里克（`GOD_GERLYK`）的描述。换行完全一致；专名“Age of Haze”（混沌纪）、“Sher'tul”（夏·图尔）、“Godslayer/Godslayers”（弑神者）、“Gerlyk”（盖里克）全部符合术语库既有 preferred 规范。第一句“几乎大部分”在语感上稍显冗余，但无机制或设定歧义。

---

### entry-03164
- **编号**：entry-03164
- **位置**：`mod-tome.lua:41040`（`mod-tome/data/zones/vor-armoury/npcs.lua`）
- **原文**：`This ugly orc looks really nasty and vicious. He wields a huge two-handed sword and means to use it.`
- **译文**：`这名丑陋的兽人看起来凶恶残暴。他手持一把巨大的双手剑，并且打算好好用上它。`
- **结论**：未发现问题
- **核验依据**：源码对应军械库首领战争大师纳格（`Warmaster Gnarg`）的描述。其装备为双手巨剑 `MURDERBLADE`，译文准确贴切。

---

### entry-03165
- **编号**：entry-03165
- **位置**：`mod-tome.lua:41068`（`mod-tome/data/zones/vor-pride/npcs.lua`）
- **原文**：`Vor, Grand Geomancer of the Pride`
- **译文**：`部落高阶地卜师沃尔`
- **结论**：未发现问题
- **核验依据**：源码对应沃尔部落首领 `VOR` 的名称。与全库其他三大部落首领命名格式（如第 38596 行“部落至高龙战士加伯特”、第 38632 行“部落战斗大师格鲁希纳克”、第 39332 行“部落死灵大法师拉克·肖”）保持完全一致。

---

### entry-03166
- **编号**：entry-03166
- **位置**：`mod-tome.lua:41136`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：`A quiet town at the crossroads of the north`
- **译文**：`一个位于北方十字要道的宁静村庄。`
- **结论**：未发现问题
- **核验依据**：源码对应大地图上德斯镇（`TOWN_DERTH`）的描述。陈述句补全中文句号，语义准确通顺。

---

### entry-03167
- **编号**：entry-03167
- **位置**：`mod-tome.lua:41138`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：`Capital city of the Allied Kingdoms ruled by King Tolak`
- **译文**：`联合王国首都（托拉克统治）`
- **结论**：存在疑点
- **核验依据**：
  1. **漏译头衔**：英文原文为 `ruled by King Tolak`，译文为“（托拉克统治）”，漏译了“国王”（King）头衔。
  2. **句式与同 section 不一致且添加了多余括号**：同文件下文第 41146 行夏特尔描述为“自然精灵领地的首都，由奈希拉·坦泰兰统治”（`Capital city of Thaloren lands, ruled by Nessilla Tantaelen`），第 41148 行埃尔瓦拉描述为“永恒精灵领地的首都，由阿兰尼恩·葛艾尔统治”（`Capital city of Shaloren lands, ruled by Aranion Gayaeil`），均采用规范的“……首都，由……统治”句式。此处使用了括号且省略了“国王”头衔，建议统一译为如“联合王国首都，由托拉克国王统治”。

---

### entry-03168
- **编号**：entry-03168
- **位置**：`mod-tome.lua:41140`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：
```text
Secret place of magic, set apart from the world to protect it.
Lead by the Supreme Archmage Linaniil.
```
- **译文**：
```text
魔法的隐藏圣地，隔绝于世。
由超阶魔导师莱娜尼尔统领。
```
- **结论**：未发现问题
- **核验依据**：源码对应大地图上安格利文（`TOWN_ANGOLWEN`）的描述。“Supreme Archmage Linaniil”译为“超阶魔导师莱娜尼尔”，与全库击杀成就（第 2688 行）及 NPC 实体名（第 40203 行）完全一致；换行结构完全对齐。

---

### entry-03169
- **编号**：entry-03169
- **位置**：`mod-tome.lua:41154`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：`Ziguranth main training ground`
- **译文**：`伊格兰斯的主要训练基地`
- **结论**：未发现问题
- **核验依据**：源码对应大地图上伊格镇（`TOWN_ZIGUR`）的描述。依据术语库规范：“教团／人群用「伊格兰斯」，地点用「伊格」”。原文明确为主格群体 `Ziguranth`（指反魔教团），故此处译为“伊格兰斯的主要训练基地”完全符合术语规则。

---

### entry-03170
- **编号**：entry-03170
- **位置**：`mod-tome.lua:41158`（`mod-tome/data/zones/wilderness/grids.lua`）
- **原文**：`Heart of the dwarven Empire`
- **译文**：`矮人帝国的心脏`
- **结论**：未发现问题
- **核验依据**：源码对应大地图上铁掌议会（`TOWN_IRON_COUNCIL`）的描述。“dwarven Empire”符合术语库 preferred 规范“矮人帝国”（不与“矮人王国”混淆），翻译准确。

---

### entry-03171
- **编号**：entry-03171
- **位置**：`mod-tome.lua:41215`（`mod-tome/dialogs/Birther.lua`）
- **原文**：`     Play!     `
- **译文**：`     游玩！     `
- **结论**：未发现问题
- **核验依据**：源码对应创角界面确定按钮（`self.c_ok = Button.new{text=_t"     Play!     ", ...}`）。原文首尾各有 5 个半角空格用于 UI 宽度排版，译文严格保留了前后各 5 个空格及全角感叹号，排版不变量完整。
