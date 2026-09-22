### 批次复核说明与环境核验

- **复核批次**：`batch-023`
- **条目范围**：`entry-00882` 至 `entry-00921`（共 40 条）
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-023.md`
  - 预期 SHA-256：`85fcec7b1b9abcad92934946c3a67e4fcd32e7692bcd2cf991e7b043e4e9b626`
  - 实测 SHA-256：`85fcec7b1b9abcad92934946c3a67e4fcd32e7692bcd2cf991e7b043e4e9b626`（校验匹配）
- **固定公开源码基准**：t-engine4 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（本批条目全部归属 `mod-tome/data/general/objects/egos/`，无 DLC 或未固定源码条目）
- **译文基准**：汉化仓库 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00` 之 `mod-tome.lua`

---

### 逐条复核报告

#### entry-00882
- **位置**：`mod-tome.lua:10111`
- **Section**：`mod-tome/data/general/objects/egos/gloves.lua`
- **原文**：`archer`
- **译文**：`弓箭手`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `gloves.lua:683` 中为词缀 ` of archery`（弓道之）定义的关键词 `keywords = {archer=true}`。译文“弓箭手”与角色职业/词缀体系通用译法完全一致，符合相关术语表基准。

#### entry-00883
- **位置**：`mod-tome.lua:10154`
- **Section**：`mod-tome/data/general/objects/egos/helm.lua`
- **原文**：`cleansing `（带末尾空格）
- **译文**：`洁净的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `helm.lua:198` 头盔前缀词缀 `name = "cleansing ", prefix=true`。译文“洁净的”符合术语快照中 `cleansing ` 针对核心装备前缀名称的 preferred 条目要求，保留修饰语属性。

#### entry-00884
- **位置**：`mod-tome.lua:10155`
- **Section**：`mod-tome/data/general/objects/egos/helm.lua`
- **原文**：`cleanse`
- **译文**：`洁净`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `helm.lua:199` 关键词 `keywords = {cleanse=true}`。译文“洁净”符合术语快照针对核心装备 ego keyword 的 preferred 规范。

#### entry-00885
- **位置**：`mod-tome.lua:10217`
- **Section**：`mod-tome/data/general/objects/egos/light-armor.lua`
- **原文**：`%s uses %s %s!`
- **译文**：`%s使用了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `light-armor.lua:146` 调用 `game.logSeen(who, "%s uses %s %s!", who:getName():capitalize(), who:his_her(), self:getName{...})`。三个 `%s` 顺序对应施法者名称、代词、装备名称；译文占位符数量与类型完全一致，标点为全角感叹号，语序流畅。

#### entry-00886
- **位置**：`mod-tome.lua:10256`
- **Section**：`mod-tome/data/general/objects/egos/lite.lua`
- **原文**：`dreamer's `（带末尾空格）
- **译文**：`梦者的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `lite.lua:193` 光源前缀词缀 `name = "dreamer's ", prefix=true`。译文“梦者的”准确传达灵能所属属性，格式规范。

#### entry-00887
- **位置**：`mod-tome.lua:10257`
- **Section**：`mod-tome/data/general/objects/egos/lite.lua`
- **原文**：`guide`
- **译文**：`向导`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `lite.lua:194` 中该词缀的运行键定义为 `keywords = {guide=true}`。译文“向导”与源码关键词完全吻合。

#### entry-00888
- **位置**：`mod-tome.lua:10317`
- **Section**：`mod-tome/data/general/objects/egos/mindstars.lua`
- **原文**：`#GREEN#The mindstars pulse with life.`
- **译文**：`#GREEN#灵晶脉动着生命。`
- **source_tag**：`logPlayer`
- **复核结论**：未发现问题
- **核验依据**：源码 `mindstars.lua:224` 在灵晶套装激活时调用 `game.logPlayer(who, "#GREEN#The mindstars pulse with life.")`。颜色标记 `#GREEN#` 完整闭合，句末标点匹配，灵晶术语标准。

#### entry-00889
- **位置**：`mod-tome.lua:10338`
- **Section**：`mod-tome/data/general/objects/egos/mindstars.lua`
- **原文**：`#YELLOW#%s has their %s spell disrupted for for %d turns!`
- **译文**：`#YELLOW#%s的%s法术被干扰%d回合！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `mindstars.lua:493` 传入参数为 `target:getName():capitalize(), t.name, turns`。英文源文包含轻微原生笔误“for for”，译文正确过滤多余介词并准确对齐各占位符（人物名、法术名、回合数），颜色标签 `#YELLOW#` 完整，标点匹配。

#### entry-00890
- **位置**：`mod-tome.lua:10354`
- **Section**：`mod-tome/data/general/objects/egos/mindstars.lua`
- **原文**：`dreamer's `（带末尾空格）
- **译文**：`梦者的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `mindstars.lua:640` 灵晶前缀词缀 `name = "dreamer's ", prefix=true`。译文“梦者的”正确无误。

#### entry-00891
- **位置**：`mod-tome.lua:10355`
- **Section**：`mod-tome/data/general/objects/egos/mindstars.lua`
- **原文**：`dreamers`
- **译文**：`梦者`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `mindstars.lua:641` 对应关键词 `keywords = {dreamers=true}`。译文“梦者”与词缀名保持一致。

#### entry-00892
- **位置**：`mod-tome.lua:10365`
- **Section**：`mod-tome/data/general/objects/egos/mindstars.lua`
- **原文**：`%s feeds %s %s with psychic energy from %s!`
- **译文**：`%s用%s%s吸收%s的精神力量！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `mindstars.lua:745` 饥渴灵晶附魔主动技能日志，调用为 `game.logSeen(who, "%s feeds %s %s with psychic energy from %s!", who:getName():capitalize(), who:his_her(), self:getName(...), target:getName():capitalize())`。参数 1~4 依次为：玩家名、代词（他的）、装备名（饥渴灵晶）、目标名。中文译为“【玩家】用【他的】【灵晶】吸收【目标】的精神力量！”，占位符顺序保持自然天然对应（1, 2, 3, 4），4 个 `%s` 齐全，机制理解完全准确。

#### entry-00893
- **位置**：`mod-tome.lua:10416`
- **Section**：`mod-tome/data/general/objects/egos/ranged.lua`
- **原文**：`%s uses %s %s!`
- **译文**：`%s使用了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `ranged.lua:290`（真菌远程武器附魔使用日志），参数为使用人、物主代词、武器名称。占位符数量（3 个 `%s`）、语序及标点完全一致。

#### entry-00894
- **位置**：`mod-tome.lua:10418`
- **Section**：`mod-tome/data/general/objects/egos/ranged.lua`
- **原文**：`blaze`
- **译文**：`炽焰`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `ranged.lua:306` 对应前缀词缀 `blazebringer's `（烈焰行者的）的关键词 `keywords = {blaze=true}`。译文“炽焰”准确合适。

#### entry-00895
- **位置**：`mod-tome.lua:10442`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：` of tenacity`（带前置空格）
- **译文**：`不屈之`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `rings.lua:62` 戒指后缀词缀 `name = " of tenacity", suffix=true`（增加生命值）。译为“不屈之”（生成如“不屈之戒”）准确自然。

#### entry-00896
- **位置**：`mod-tome.lua:10443`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：`tenacity`
- **译文**：`不屈不挠`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `rings.lua:63` 关键词 `keywords = {tenacity=true}`。译文“不屈不挠”表意精准。

#### entry-00897
- **位置**：`mod-tome.lua:10484`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：`sneakthief's `（带末尾空格）
- **译文**：`窃贼的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `rings.lua:360` 敏捷/技巧双属性戒指前缀词缀 `name = "sneakthief's ", prefix=true`。译文“窃贼的”规范。

#### entry-00898
- **位置**：`mod-tome.lua:10485`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：`sneakthief`
- **译文**：`窃贼`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `rings.lua:361` 关键词 `keywords = {sneakthief=true}`。译文与词缀名完全一致。

#### entry-00899
- **位置**：`mod-tome.lua:10488`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：`conjurer's `（带末尾空格）
- **译文**：`魔术师的`
- **source_tag**：`entity name`
- **复核结论**：细微观察
- **核验依据**：源码 `rings.lua:392` 为魔力/意志双属性戒指前缀词缀 `name = "conjurer's ", prefix=true`。在通用奇幻 RPG 中 conjurer 常作“咒术师/咒法师/召唤师”，此处译为“魔术师的”偏现代魔术或泛法术，但该译法与同文件 entry-00900（keyword 魔术师）、entry-00918（魔术之）、entry-00919（魔术）统一成套，未造成歧义或机制冲突。

#### entry-00900
- **位置**：`mod-tome.lua:10489`
- **Section**：`mod-tome/data/general/objects/egos/rings.lua`
- **原文**：`conjurer`
- **译文**：`魔术师`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `rings.lua:393` 关键词 `keywords = {conjurer=true}`。译文与 entry-00899 词缀前缀完全对应。

#### entry-00901
- **位置**：`mod-tome.lua:10548`
- **Section**：`mod-tome/data/general/objects/egos/robe.lua`
- **原文**：`dreamer's `（带末尾空格）
- **译文**：`梦者的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `robe.lua:212` 长袍前缀词缀 `name = "dreamer's ", prefix=true`（赋予清醒梦境/睡眠免疫等）。译文“梦者的”准确。

#### entry-00902
- **位置**：`mod-tome.lua:10549`
- **Section**：`mod-tome/data/general/objects/egos/robe.lua`
- **原文**：`dreamer`
- **译文**：`梦者`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `robe.lua:213` 关键词 `keywords = {dreamer=true}`。译文与词缀名一致。

#### entry-00903
- **位置**：`mod-tome.lua:10572`
- **Section**：`mod-tome/data/general/objects/egos/robe.lua`
- **原文**：`slimy `（带末尾空格）
- **译文**：`黏滑的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `robe.lua:455` 长袍前缀词缀 `name = "slimy ", prefix=true`（反魔/受击释放史莱姆减速）。译文“黏滑的”准确生动。

#### entry-00904
- **位置**：`mod-tome.lua:10573`
- **Section**：`mod-tome/data/general/objects/egos/robe.lua`
- **原文**：`slimy`
- **译文**：`黏滑`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `robe.lua:456` 关键词 `keywords = {slimy=true}`。译文与词缀名完全对应。

#### entry-00905
- **位置**：`mod-tome.lua:10643`
- **Section**：`mod-tome/data/general/objects/egos/shield.lua`
- **原文**：`living `（带末尾空格）
- **译文**：`生命的`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `shield.lua:423` 盾牌前缀词缀 `name = "living ", prefix=true`（增加自然抗性、枯萎抗性与最大生命）。译文“生命的”符合盾牌命名习惯。

#### entry-00906
- **位置**：`mod-tome.lua:10668`
- **Section**：`mod-tome/data/general/objects/egos/shield.lua`
- **原文**：`Cause enemies within radius 6 to bleed for #RED#%d#LAST# physical damage over 5 turns (1/turn)`
- **译文**：`使6码范围内的敌人流血，在5回合内受到#RED#%d#LAST#物理伤害（1/回合）`
- **source_tag**：`tformat`
- **复核结论**：未发现问题
- **核验依据**：源码 `shield.lua:697`（弹片之盾格挡特效描述），格式化参数传入 `dam`。占位符 `%d` 与颜色标记 `#RED#`、`#LAST#` 齐全无损；术语“流血”（bleed）与“物理伤害”（physical damage）符合术语表标准，范围“6码”翻译准确。

#### entry-00907
- **位置**：`mod-tome.lua:10718`
- **Section**：`mod-tome/data/general/objects/egos/staves.lua`
- **原文**：`%s channels mana through %s %s!`
- **译文**：`%s在%s%s中传导魔力！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `staves.lua:268`（传导法杖激活法力激流日志），调用为 `game.logSeen(who, "%s channels mana through %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。三个占位符 `%s` 顺序对应人物、物主代词、法杖名，标点匹配，语意通顺。

#### entry-00908
- **位置**：`mod-tome.lua:10727`
- **Section**：`mod-tome/data/general/objects/egos/staves.lua`
- **原文**：`%s channels a cone of %s%s#LAST# energy through %s %s!`
- **译文**：`%s从%s%s中传导出一股呈锥形的%s%s#LAST# 能量！`
- **source_tag**：`logSeen`
- **args_order**：`[1, 4, 5, 2, 3]`
- **复核结论**：未发现问题
- **核验依据**：源码 `staves.lua:360` 祈祷法杖引导锥形元素能量日志，原始调用参数为：
  1. `who:getName():capitalize()`（使用者）
  2. `damTyp.text_color`（伤害颜色代码）
  3. `damTyp.name`（伤害类型名称）
  4. `who:his_her()`（代词：他的）
  5. `self:getName(...)`（装备名：祈祷法杖）
  译文配置 `args_order = {1, 4, 5, 2, 3}`，重排后第 1 位接使用者，第 2~3 位接物主代词和装备名，第 4~5 位接颜色与伤害名，拼合后为“【角色】从【他的】【法杖】中传导出一股呈锥形的【颜色】【伤害类型】#LAST# 能量！”，完美解决了英汉倒装语序问题。占位符数量均为 5 个 `%s`，颜色标签完整。

#### entry-00909
- **位置**：`mod-tome.lua:10762`
- **Section**：`mod-tome/data/general/objects/egos/torques-powers.lua`
- **原文**：`%s uses %s %s!`
- **译文**：`%s使用了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `torques-powers.lua:86`（强风项圈主动技能释放日志），参数为 `who:getName():capitalize(), who:his_her(), self:getName(...)`。3 个 `%s` 占位符、标点及语序无误。

#### entry-00910
- **位置**：`mod-tome.lua:10766`
- **Section**：`mod-tome/data/general/objects/egos/torques-powers.lua`
- **原文**：`%s activates %s %s!`
- **译文**：`%s激活了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `torques-powers.lua:129`（心灵爆炸项圈使用日志），参数为施法者、代词、物品名。格式与占位符完全匹配。

#### entry-00911
- **位置**：`mod-tome.lua:10774`
- **Section**：`mod-tome/data/general/objects/egos/totems-powers.lua`
- **原文**：`%s activates %s %s!`
- **译文**：`%s激活了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `totems-powers.lua:53`（治疗图腾使用日志），参数为人物名、代词、图腾名。占位符与标点正确。

#### entry-00912
- **位置**：`mod-tome.lua:10782`
- **Section**：`mod-tome/data/general/objects/egos/totems-powers.lua`
- **原文**：`tentacle`
- **译文**：`触手`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `totems-powers.lua:114` 对应 `keywords = {tentacle=true}`。译文“触手”标准无误。

#### entry-00913
- **位置**：`mod-tome.lua:10783`
- **Section**：`mod-tome/data/general/objects/egos/totems-powers.lua`
- **原文**：
  ```text
  (Tentacle Stats)
  Life:  %d
  Base Damage:  %d
  Armor:  %d
  All Resist:  %d
  ```
- **译文**：
  ```text
  （触手属性）
  生命值：%d
  基础伤害：%d
  护甲值：%d
  所有抗性：%d
  ```
- **source_tag**：`tformat`
- **复核结论**：未发现问题
- **核验依据**：源码 `totems-powers.lua:120` 格式化触手属性面板文本，参数依次为 `stats.max_life, stats.combat.dam, stats.combat_armor, stats.resists.all`。4 个 `%d` 完整对齐；术语遵循“生命值语境统一用‘生命值’”、“护甲/护甲值”的标准；换行数一致，冒号全角化。

#### entry-00914
- **位置**：`mod-tome.lua:10798`
- **Section**：`mod-tome/data/general/objects/egos/totems-powers.lua`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **source_tag**：`logPlayer`
- **复核结论**：细微观察
- **核验依据**：源码 `totems-powers.lua:134` 调用 `game.logPlayer(self, "Not enough space to summon!")`。英文源文末尾为感叹号 `!`，当前译文使用全角感叹号 `！`，并与 `mod-tome.lua` 中其余 15 处相同 source 的 `logPlayer` 译文完全一致。术语快照中存在 `T.RUNTIME.LOG / logSeen` 的 preferred 记录 `没有足够的空间召唤。`（以句号结尾），本条属于 `logPlayer` 语境且标点忠实于原文感叹号，不存在逻辑或显示缺陷。

#### entry-00915
- **位置**：`mod-tome.lua:10801`
- **Section**：`mod-tome/data/general/objects/egos/totems-powers.lua`
- **原文**：`#Source# points %s %s at #target#, releasing a writhing tentacle!`
- **译文**：`#Source#将%s%s指向#target#，释放出扭曲的触手！`
- **source_tag**：`logCombat`
- **复核结论**：未发现问题
- **核验依据**：源码 `totems-powers.lua:185` 战斗日志，参数 1 为 `who:his_her()`，参数 2 为 `self:getName(...)`。引擎宏 `#Source#` 与 `#target#` 准确保留，占位符 `%s%s` 顺序与指称正确，动作描写与标点符合规范。

#### entry-00916
- **位置**：`mod-tome.lua:10811`
- **Section**：`mod-tome/data/general/objects/egos/wands-powers.lua`
- **原文**：`%s uses %s %s!`
- **译文**：`%s使用了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `wands-powers.lua:39`（透视魔杖使用日志），参数为使用者名称、代词、魔杖名。3 个 `%s` 齐全，标点正确。

#### entry-00917
- **位置**：`mod-tome.lua:10815`
- **Section**：`mod-tome/data/general/objects/egos/wands-powers.lua`
- **原文**：`%s conjures a lightning storm from %s %s!`
- **译文**：`%s从%s%s中召唤出闪电风暴！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `wands-powers.lua:66`（闪电风暴魔杖日志），参数为 `who:getName():capitalize(), who:his_her(), self:getName(...)`。中文语序为“【角色】从【他的】【魔杖】中召唤出闪电风暴！”，占位符自然对应（1, 2, 3），数量一致，标点为全角感叹号。

#### entry-00918
- **位置**：`mod-tome.lua:10816`
- **Section**：`mod-tome/data/general/objects/egos/wands-powers.lua`
- **原文**：` of conjuration`（带前置空格）
- **译文**：`魔术之`
- **source_tag**：`entity name`
- **复核结论**：细微观察
- **核验依据**：源码 `wands-powers.lua:83` 魔杖后缀词缀 `name = " of conjuration", addon=true`（发射随机元素魔法箭）。译为“魔术之”（如“魔术之红宝石魔杖”），与 entry-00899/00900/00919 统一，属于词缀系统既有译法，无机制错误。

#### entry-00919
- **位置**：`mod-tome.lua:10817`
- **Section**：`mod-tome/data/general/objects/egos/wands-powers.lua`
- **原文**：`conjure`
- **译文**：`魔术`
- **source_tag**：`entity keyword`
- **复核结论**：未发现问题
- **核验依据**：源码 `wands-powers.lua:84` 对应 `keywords = {conjure=true}`。译文与 entry-00918 词缀名称完全对应。

#### entry-00920
- **位置**：`mod-tome.lua:10819`
- **Section**：`mod-tome/data/general/objects/egos/wands-powers.lua`
- **原文**：`%s activates %s %s!`
- **译文**：`%s激活了%s%s！`
- **source_tag**：`logSeen`
- **复核结论**：未发现问题
- **核验依据**：源码 `wands-powers.lua:108`（魔术魔杖主动释放元素箭日志），参数为人物、代词、装备名称。占位符与标点正确无误。

#### entry-00921
- **位置**：`mod-tome.lua:10865`
- **Section**：`mod-tome/data/general/objects/egos/weapon.lua`
- **原文**：` of daylight`（带前置空格）
- **译文**：`日光之`
- **source_tag**：`entity name`
- **复核结论**：未发现问题
- **核验依据**：源码 `weapon.lua:321` 武器后缀词缀 `name = " of daylight", suffix=true`（附带光系伤害并提升对不死生物伤害）。译文“日光之”表意准确，符合词缀体系规范。

---

### 复核总结

本批 `batch-023` 共 40 条译文，经对照固定提交公开源码 `624a67329fe2ad440c5b344785a9c73fcf22ae63` 与译文基准文件核验：
1. **未发现阻断性机制缺陷、占位符缺失、颜色标签破损或换行不一致问题**；
2. 特殊重排条目 `entry-00908` 的 `args_order = [1, 4, 5, 2, 3]` 经源码调用参数验证，映射精准，语序符合中文习惯；
3. 发现 3 处与术语快照或经典奇幻译法相关的“细微观察”（`entry-00899`、`entry-00914`、`entry-00918`），均已注明可核验事实依据，不构成破坏性疑点。全批 40 条核验完毕。