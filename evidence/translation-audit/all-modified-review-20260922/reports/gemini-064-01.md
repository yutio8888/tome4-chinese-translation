# 译文复核报告：batch-064（entry-01948 至 entry-01987）

## 复核前置校验

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-064.md`
- **文件校验 SHA-256**：`f644ce5987f182800db1cb369915250184b60bdbce043619384f67eea99697d0`（核验一致）
- **条目数量**：40 条（entry-01948 至 entry-01987 全覆盖）
- **源码基准**：公开仓库 `t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取对应文件及调用链，本批涉及源码均属于 `game/modules/tome/`，无 DLC 依赖）
- **译文上下文基准**：译文终点 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

## 逐条复核详情

### entry-01948
- **位置**：`mod-tome.lua:25706`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a War Hound!`
- **译文**：`@Source@召唤了一只战争猎犬！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:90` 定义 `message = _t"@Source@ summons a War Hound!"`，实体标签 `@Source@` 完整保留，`War Hound` 对应“战争猎犬”，感叹号对应准确。

---

### entry-01949
- **位置**：`mod-tome.lua:25708`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`logPlayer`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:132` 为 `game.logPlayer(self, "Not enough space to summon!")`，语义准确，感叹号与英文原文一致。

---

### entry-01950
- **位置**：`mod-tome.lua:25709`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`tformat`
- **原文**：`%s (wild summon)`
- **译文**：`%s（野性召唤）`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:160` 为 `("%s (wild summon)"):tformat(_t(m.name))`，占位符 `%s` 正确保留，括号使用全角规范，wild summon 对应野性召唤无误。

---

### entry-01951
- **位置**：`mod-tome.lua:25710`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a War Hound for %d turns to attack your foes. War hounds are good basic melee attackers.
  		It will get %d Strength, %d Dexterity and %d Constitution.
  		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
  		The hound's Strength and Dexterity will increase with your Mindpower.
  ```
- **译文**：
  ```text
  召唤一只战争猎犬来攻击敌人，持续 %d 回合。
  		战争猎犬是非常好的基础近战单位。
  		它拥有 %d 点力量，%d 点敏捷和 %d 点体质。
  		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
  		猎犬的力量和敏捷受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:176-184` 传入参数为 `t.summonTime(self, t), incStats.str, incStats.dex, incStats.con`，译文 4 个 `%d` 顺序依次为回合、力量、敏捷、体质，完全匹配；属性与状态抗性术语一致；首句说明文字按句分行排版，不影响参数代入。

---

### entry-01952
- **位置**：`mod-tome.lua:25718`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`talent name`
- **原文**：`Jelly`
- **译文**：`召唤：果冻怪`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:187` 定义 `name = "Jelly"`，译文遵循该系列召唤技能统一使用“召唤：”前缀的既定规范以与野生生物区分。

---

### entry-01953
- **位置**：`mod-tome.lua:25719`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a Jelly!`
- **译文**：`@Source@召唤了一只果冻怪！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:192` 定义 `message = _t"@Source@ summons a Jelly!"`，标签 `@Source@` 保留完整，译名统一。

---

### entry-01954
- **位置**：`mod-tome.lua:25721`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`delayedLogMessage`
- **原文**：`#GREEN##Target# absorbs some damage. #Source# is closer to nature.`
- **译文**：`#GREEN##Target#吸收了伤害，#Source#更贴近自然了。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:281` 为 `game:delayedLogMessage(self.summoner, self, "jelly", "#GREEN##Target# absorbs some damage. #Source# is closer to nature.")`，颜色标签 `#GREEN#` 与目标/来源标签完整保留，机制上对应果冻怪分摊伤害并降低召唤者失衡值（closer to nature），语意准确。

---

### entry-01955
- **位置**：`mod-tome.lua:25731`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`talent name`
- **原文**：`Minotaur`
- **译文**：`召唤：米诺陶`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:315` 定义 `name = "Minotaur"`，遵循召唤系技能命名规范。

---

### entry-01956
- **位置**：`mod-tome.lua:25732`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a Minotaur!`
- **译文**：`@Source@召唤了一只米诺陶！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:320` 定义 `message = _t"@Source@ summons a Minotaur!"`，标签 `@Source@` 完整，译名统一。

---

### entry-01957
- **位置**：`mod-tome.lua:25734`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a Minotaur for %d turns to attack your foes. Minotaurs cannot stay summoned for long, but they deal high damage.
  		It will get %d Strength, %d Constitution and %d Dexterity.
  		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
  		The minotaur's Strength and Dexterity will increase with your Mindpower.
  ```
  - **译文**：
  ```text
  召唤一只米诺陶来攻击敌人，持续 %d 回合。米诺陶不会呆很长时间，但是它们会造成极大伤害。
  		它拥有 %d 点力量，%d 点体质和 %d 点敏捷。
  		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
  		米诺陶的力量和敏捷受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:420-428` 参数列表为 `t.summonTime(self,t), incStats.str, incStats.con, incStats.dex`，译文中 4 个 `%d` 顺序依次对应回合、力量、体质、敏捷，与传参完全一致。

---

### entry-01958
- **位置**：`mod-tome.lua:25741`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`talent name`
- **原文**：`Stone Golem`
- **译文**：`召唤：岩石傀儡`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:431` 定义 `name = "Stone Golem"`，遵循召唤系命名规范，golem 统一译为傀儡。

---

### entry-01959
- **位置**：`mod-tome.lua:25742`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a Stone Golem!`
- **译文**：`@Source@召唤了一只岩石傀儡！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:436` 定义 `message = _t"@Source@ summons a Stone Golem!"`，标签完整，译名统一。

---

### entry-01960
- **位置**：`mod-tome.lua:25743`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`_t`
- **原文**：`It is a massive animated statue.`
- **译文**：`一座巨型的活化雕像。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:493` 岩石傀儡描述 `desc = _t[[It is a massive animated statue.]]`，译文准确自然。

---

### entry-01961
- **位置**：`mod-tome.lua:25744`
- **section**：`mod-tome/data/talents/gifts/summon-melee.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a Stone Golem for %d turns to attack your foes. Stone golems are formidable foes that can become unstoppable.
  		It will get %d Strength, %d Constitution and %d Dexterity.
  		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
  		The golem's Strength and Dexterity will increase with your Mindpower.
  ```
- **译文**：
  ```text
  召唤一只岩石傀儡来攻击敌人，持续 %d 回合。岩石傀儡是可怕的敌人并且不可阻挡。
  		它有 %d 点力量，%d 点体质和 %d 点敏捷。
  		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
  		傀儡的力量和敏捷受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-melee.lua:530-538` 参数传递为 `(summonTime, incStats.str, incStats.con, incStats.dex)`，占位符 `%d` 顺序完全吻合；源码中该傀儡自带技能 `Talents.T_UNSTOPPABLE`，文本“become unstoppable”译为“不可阻挡”贴合机制。

---

### entry-01962
- **位置**：`mod-tome.lua:25766`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`talent name`
- **原文**：`Turtle`
- **译文**：`召唤：乌龟`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:66` 定义 `name = "Turtle"`，遵循召唤系命名规范。

---

### entry-01963
- **位置**：`mod-tome.lua:25767`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a Turtle!`
- **译文**：`@Source@召唤了一只乌龟！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:71` 定义 `message = _t"@Source@ summons a Turtle!"`，标签 `@Source@` 完整，译名统一。

---

### entry-01964
- **位置**：`mod-tome.lua:25769`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`logPlayer`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:132` 为 `game.logPlayer(self, "Not enough space to summon!")`，语义与感叹号一致。

---

### entry-01965
- **位置**：`mod-tome.lua:25770`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`tformat`
- **原文**：`%s (wild summon)`
- **译文**：`%s（野性召唤）`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:164` 为 `("%s (wild summon)"):tformat(_t(m.name))`，占位符与全角括号规范正确。

---

### entry-01966
- **位置**：`mod-tome.lua:25771`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a Turtle for %d turns to distract your foes. Turtles are resilient, but not very powerful. However, they will periodically force any foes to attack them, and can protect themselves with their shell.
  		It will get %d Constitution, %d Dexterity and 18 willpower.
  		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
  		Their Constitution will increase with your Mindpower.
  ```
- **译文**：
  ```text
  召唤一只乌龟来吸引敌人攻击，持续 %d 回合。
  		乌龟具有很强的生命力，并不能造成很多伤害。
  		然而，它们会周期性的嘲讽敌人并用龟壳保护自己。
  		它拥有 %d 点体质，%d 点敏捷和 18 点意志。
  		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
  		乌龟的体质受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:181-189` 参数传递为 `(t.summonTime(self, t), incStats.con, incStats.dex)`，占位符 `%d` 依次对应回合、体质、敏捷，源码硬编码数值 `18 willpower` 对应 `18 点意志` 无误。

---

### entry-01967
- **位置**：`mod-tome.lua:25780`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`talent name`
- **原文**：`Spider`
- **译文**：`召唤：蜘蛛`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:191` 定义 `name = "Spider"`，遵循召唤系命名规范。

---

### entry-01968
- **位置**：`mod-tome.lua:25781`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ summons a Spider!`
- **译文**：`@Source@召唤了一只蜘蛛！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:196` 定义 `message = _t"@Source@ summons a Spider!"`，标签完整，译名统一。

---

### entry-01969
- **位置**：`mod-tome.lua:25782`
- **section**：`mod-tome/data/talents/gifts/summon-utility.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a Spider for %d turns to harass your foes. Spiders can poison your foes and throw webs to pin them to the ground.
  		It will get %d Dexterity, %d Strength, 18 Willpower and %d Constitution.
  		Your summons inherit some of your stats: increased damage%%, resistance penetration %%, stun/pin/confusion/blindness resistance, armour penetration.
  		Their Dexterity will increase with your Mindpower.
  ```
- **译文**：
  ```text
  召唤一只蜘蛛来扰乱敌人，持续 %d 回合。
  		蜘蛛可以使敌人中毒并向目标撒网，将目标固定在地上。
  		它拥有 %d 点敏捷，%d 点力量，18 点意志和 %d 点体质。
  		你的召唤物继承你部分属性：增加百分比伤害、抗性穿透、震慑/定身/混乱/致盲抵抗和护甲穿透。
  		蜘蛛的敏捷受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `summon-utility.lua:319-327` 参数传递为 `(t.summonTime(self, t), incStats.dex, incStats.str, incStats.con)`，占位符 `%d` 依次对应回合、敏捷、力量、体质，硬编码 `18 Willpower` 对应 `18 点意志`，完全正确。

---

### entry-01970
- **位置**：`mod-tome.lua:25806`
- **section**：`mod-tome/data/talents/gifts/venom-drake.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Spray forth a glob of acidic moisture at your enemy.
  		The target will take %0.2f Mindpower-based acid damage.
  		Enemies struck have a 25%% chance to be Disarmed for three turns, as their weapon is rendered useless by an acid coating.
  		At Talent Level 5, this becomes a piercing line of acid.
  		Every level in Acidic Spray additionally raises your Mindpower by 4, passively.
  		Each point in acid drake talents also increases your acid resistance by 1%%.
  ```
- **译文**：
  ```text
  向你的敌人喷出一团酸液。
  		目标会受到 %0.2f 点基于精神强度的酸性伤害。
  		受到攻击的敌人有 25 %%几率被缴械 3 回合，因为酸液将他们的武器给腐蚀了。
  		在技能等级 5 时，这道酸液可以穿透一条线上的敌人。
  		每点技能等级被动地增加精神强度 4 点。
  		每一点毒龙系技能同时也能增加你的酸性抗性 1%%。
  ```
- **复核结论**：细微观察
- **核验依据**：
  1. 占位符与格式化：第三行中 `25 %%几率` 的数字与转义百分号 `%%` 之间多包含了一个半角空格，经 `string.format` 格式化后会呈现为 `25 %几率`（带异常空格），而非紧凑的 `25%几率` 或 `25% 几率`。
  2. 机制与术语：源码 `gifts/gifts.lua:35` 中该技能树定义为 `type="wild-gift/venom-drake", name = _t("venom drake aspect", "talent type")`（即“毒龙形态/毒龙系”），末尾英文虽写作 `acid drake talents`，但其内部代码逻辑与描述指向的就是当前 venom-drake 技能树（学习该树每点技能均被动 +1% 酸抗），译为“毒龙系技能”在语境上准确贴合。唯一瑕疵在于 `25 %%几率` 处的半角空格。

---

### entry-01971
- **位置**：`mod-tome.lua:25850`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`Physical talents of the various horrors of the world.`
- **译文**：`世界上各种恐魔的物理能力。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:19` 技能类型描述，horror 译为恐魔，physical 译为物理，准确通顺。

---

### entry-01972
- **位置**：`mod-tome.lua:25852`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`Psionic talents of the various horrors of the world.`
- **译文**：`世界上各种恐魔的灵能能力。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:20` 技能类型描述，psionic 对应灵能，符合术语规范。

---

### entry-01973
- **位置**：`mod-tome.lua:25856`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`Spell talents of the various horrors of the world.`
- **译文**：`世界上各种恐魔的法术能力。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:22-23` 技能类型描述，spell 对应法术，准确通顺。

---

### entry-01974
- **位置**：`mod-tome.lua:25860`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`Unclassified talents of the various horrors of the world.`
- **译文**：`世界上各种恐魔的无法分类的能力。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:24` 技能类型描述，Unclassified 译为“无法分类的”准确贴切。

---

### entry-01975
- **位置**：`mod-tome.lua:25872`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`@Source@ tries to bite @Target@ with razor sharp teeth!`
- **译文**：`@Source@尝试用尖锐的牙齿咬 @Target@！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:124`，`@Source@` 与 `@Target@` 实体标签完整，译文自然。

---

### entry-01976
- **位置**：`mod-tome.lua:25875`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Bites the target for %d%% weapon damage, potentially causing it to bleed for %d%% weapon damage over five turns.
  		If the target is affected by the bleed it will send the devourer into a frenzy for %d turns (which in turn will frenzy other nearby devourers).
  		The frenzy will increase global speed by %d%%, physical crit chance by %d%%, and prevent death until -%d%% life.
  ```
- **译文**：
  ```text
  咬伤目标，造成 %d%% 武器伤害，可能让目标进入流血状态，在五回合内造成 %d%% 武器伤害。
  		如果目标进入流血状态，吞噬者会进入狂热状态 %d 回合（也会让周围的其他吞噬者进入狂热状态）。
  		狂热状态会增加全局速度 %d%% , 物理暴击率 %d%% , 同时降至 -%d%% 生命时才会死去。
  ```
- **复核结论**：细微观察
- **核验依据**：
  1. 标点格式：末行译文中出现英文半角逗号且逗号前带有异常半角空格（`全局速度 %d%% , 物理暴击率 %d%% , 同时`），未规范使用全角中文逗号。
  2. 占位符与机制：6 个占位符（基础武器伤害百分比、流血百分比、狂乱持续回合、全局速度、暴击率、免死负生命值比例）与源码 `horrors.lua:172-181` `(damage, bleed, duration, power, power, power)` 顺序与对应关系完全一致；“prevent death until -%d%% life”译为“降至 -%d%% 生命时才会死去”符合 `dieat = -power` 机制。

---

### entry-01977
- **位置**：`mod-tome.lua:25880`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`talent name`
- **原文**：`Abyssal Shroud`
- **译文**：`深渊裹幕`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:185` 定义 `name = "Abyssal Shroud"`，译名准确。

---

### entry-01978
- **位置**：`mod-tome.lua:25887`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`logPlayer`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:294`（虚空碎片 Void Shards 技能中 `game.logPlayer(self, "Not enough space to summon!")`），译文准确一致。

---

### entry-01979
- **位置**：`mod-tome.lua:25889`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`_t`
- **原文**：`It looks like a small hole in the fabric of spacetime.`
- **译文**：`看起来像时空结构中的一个小洞。`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:303` 为 void shard 召唤物描述 `desc = _t[[It looks like a small hole in the fabric of spacetime.]]`，翻译通顺准确。

---

### entry-01980
- **位置**：`mod-tome.lua:25892`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Summon a storm of swirling blades to slice your foes, inflicting %d physical damage and bleeding to anyone who approaches for %d turns.
  		The damage and duration will increase with your Mindpower.
  ```
- **译文**：
  ```text
  召唤旋转剑刃风暴将敌人切成碎片，对进入风暴的敌人造成 %d 点物理伤害并令其流血 %d 回合。
  		伤害和流血持续时间受精神强度加成。
  ```
- **复核结论**：存在疑点
- **核验依据**：
  1. 机制核验：固定 commit 源码 `horrors.lua:375-385, 399-402` 表明，技能产生一个持续 `t.getDuration(self, t)` 回合的地形效果 `knifestorm`，其伤害类型为 `DamageType.PHYSICALBLEED`。查阅 `damage_types.lua:1914`，`PHYSICALBLEED` 施加的割裂状态持续时间固定为 5 回合（`target:setEffect(target.EFF_CUT, 5, ...)`）。
  2. 语意偏差：英文原文“inflicting %d physical damage and bleeding to anyone who approaches for %d turns”中，“for %d turns”修饰的是旋刃风暴持续 %d 回合（对这 %d 回合内任何靠近者施加物理伤害与流血）。
  3. 译文错误地将其挂载到流血状态上：“对进入风暴的敌人造成 %d 点物理伤害并令其流血 %d 回合。伤害和流血持续时间受精神强度加成”。这完全抹去了风暴自身存在 %d 回合的描述，且错误宣称流血持续时间由精神强度加成（实际受精神强度加成的是风暴存在时间，流血固定为 5 回合）。存在明显机制描述偏差与语意误导。

---

### entry-01981
- **位置**：`mod-tome.lua:25897`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Pull all foes toward you in radius 5 while dealing %d physical damage.
  The damage will increase with your mindpower.
  ```
- **译文**：
  ```text
  将 5 码范围内的所有敌人拉向你并造成 %d 物理伤害。
  伤害受精神强度加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:434-436`，占位符 `%d` 对应伤害，`radius 5` 译为 5 码（符合 ToME 距离译法习惯），精神强度加成机制准确。

---

### entry-01982
- **位置**：`mod-tome.lua:25916`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Spit slime at your target doing %0.2f nature damage and slowing it down by 30%% for 3 turns.
  		The damage will increase with the Dexterity stat
  ```
- **译文**：
  ```text
  向目标喷射黏液，造成 %0.2f 自然伤害，并使其减速 30%%，持续 3 回合。
  		伤害受敏捷值加成。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:560-563`，占位符 `%0.2f` 与 `30%%` 完整，译文与原文一致。（注：源码 action 中伤害实际调用 `wil` 判定，但 info 文本原文字符串确实写为 `Dexterity stat`，译文如实忠实于原文字符串）。

---

### entry-01983
- **位置**：`mod-tome.lua:25921`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`talent name`
- **原文**：`Animate Blade`
- **译文**：`活化利刃`
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:625` 定义 `name = "Animate Blade"`，技能译名准确。

---

### entry-01984
- **位置**：`mod-tome.lua:25923`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Open a hole in space, summoning an animated blade for 10 turns.
  ```
- **译文**：
  ```text
  在空间中打开一个孔洞，召唤一把活化之剑 10 回合。
  ```
- **复核结论**：细微观察
- **核验依据**：
  1. 源码与版本演变：在固定 commit `624a67329f` 的 `horrors.lua:671` 中，英文原文实际已为 `Open a hole in space, summoning an animated blade for 15 turns.`（源码提交 `ceda5d6f` 早已将召唤时长描述修正为 15 回合以匹配 `m.summon_time = 15` 代码）。
  2. 文件内分布：本条目（line 25923）是 10 回合的历史陈旧条目；而匹配当前源码的 15 回合条目在 `mod-tome.lua` 的废弃分隔符下方（line 25939，即 entry-01986）。
  3. 译文本身对该 10 回合英文串的翻译是准确的（召唤生物 `ANIMATED_BLADE` 在 `horror.lua:1136` 中名为 `Animated Sword`，译为活化之剑相契合），但当前 1.7.6 引擎运行时检索的是 15 回合条目，本行在游戏实际运行中为未命中条目。

---

### entry-01985
- **位置**：`mod-tome.lua:25930`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Latch on to the target and suck their blood, doing %0.2f physical and %0.2f acid damage per turn.
  		After 5 turns of drinking, drop off and gain the ability to Multiply.
  		Damage scales with your level.
  		
  ```
- **译文**：
  ```text
  抓住目标，吸取他们的血液，每回合造成 %0.2f 物理和 %0.2f 酸性伤害。
  		5 回合后脱落并获得繁殖能力。
  		伤害随等级上升。
  		
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:722-726` 传入参数为 `Pdam, Fdam`，两个 `%0.2f` 顺序与物理/酸性伤害对应准确；Multiply 译为繁殖能力准确；尾部换行与缩进排版保持一致。

---

### entry-01986
- **位置**：`mod-tome.lua:25939`
- **section**：`mod-tome/data/talents/misc/horrors.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  Open a hole in space, summoning an animated blade for 15 turns.
  ```
- **译文**：
  ```text
  在空间中打开一个孔洞，召唤一把活化之剑 15 回合。
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `horrors.lua:671` 定义正是 `Open a hole in space, summoning an animated blade for 15 turns.`，代码实现 `m.summon_time = 15`，译文准确对应当前 1.7.6 版本的实际调用。

---

### entry-01987
- **位置**：`mod-tome.lua:25962`
- **section**：`mod-tome/data/talents/misc/inscriptions.lua`
- **source_tag**：`tformat`
- **原文**：
  ```text
  affinity %d%%; reduction %d; dur %d; cd %d
  ```
- **译文**：
  ```text
  伤害亲和 %d%%; 减少 %d; 持续 %d; 冷却 %d
  ```
- **复核结论**：未发现问题
- **核验依据**：固定 commit 源码 `inscriptions.lua:198-200`（原初纹身 Infusion: Primal 的 `short_info`），参数传递为 `(data.power + data.inc_stat*10, math.floor((data.reduce or 0) + data.inc_stat * 2), data.dur, data.cooldown)`，占位符 `%d%%`、`%d`、`%d`、`%d` 顺序完全一致；机制上对应伤害亲和比例（受到伤害转化为治疗）、减少随机负面状态持续回合、生效持续回合与冷却时间；半角分号与同 section 其他纹身简报风格保持一致。

---

## 复核汇总

- **覆盖范围**：entry-01948 至 entry-01987（共 40 条，全部逐条覆盖完成）
- **存在疑点**（1 条）：
  - **entry-01980**（旋刃风暴 Knife Storm 机制语意偏差）：原文“for %d turns”实指风暴地图效果存在时间，但译文译为“令其流血 %d 回合”，且将受精神强度加成的风暴持续时间误写为“流血持续时间受精神强度加成”（源码中流血实为固定 5 回合）。
- **细微观察**（3 条）：
  - **entry-01970**：`25 %%几率` 处数字与百分号间多包含半角空格，格式化后输出带有不规范空格（`25 %几率`）。
  - **entry-01976**：末行包含英文半角逗号及前置空格（`%d%% , 物理暴击率 %d%% , 同时`），标点未规范使用全角中文标点。
  - **entry-01984**：为 10 回合的历史陈旧条目，当前 1.7.6 源码为 15 回合（匹配 entry-01986），本行在实际游戏中未被调用。
- **其余条目**（36 条）：均未发现问题，占位符、标签、参数顺序与固定源码机制核验一致。