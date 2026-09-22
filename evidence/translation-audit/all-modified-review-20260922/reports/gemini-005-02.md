### 批次与基准核验

- **复核文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-005.md`
- **文件哈希**：`7a890c630970417f32b64688901b44f8fb5b1b3f3ee6d63fcc24b2264ee718cc`（校验一致）
- **复核范围**：`entry-00173` 至 `entry-00200`（共 28 条，全部属于 `mod-tome/class/Actor.lua`）
- **公开源码基准**：固定 commit [`624a67329fe2ad440c5b344785a9c73fcf22ae63`](file:///workspace/t-engine4) 下的 [`game/modules/tome/class/Actor.lua`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua)
- **译文基准**：[`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua)

---

### 逐条复核报告

#### entry-00173
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2077`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2077)（`("#ffa0ff#Predator: +%d acc, +%d apr#LAST#"):tformat(predatorATK, predatorAPR)`）。两处 `%d` 占位符分别对应命中（ATK）与护甲穿透（APR），颜色码 `#ffa0ff#` 与 `#LAST#` 闭合完整，术语与参数顺序完全吻合。

#### entry-00174
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2147`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2147)（`("#LIGHT_BLUE#Main:#LAST#%s"):tformat(o:getShortName(...))`）。主手武器简名格式化，颜色标签 `#LIGHT_BLUE#` 与 `#LAST#` 配对无误，`%s` 占位符保留，全角冒号规范。

#### entry-00175
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2158`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2158)（`("#LIGHT_BLUE#Off :#LAST#%s"):tformat(...)`）。原文为与 `Main:` 保持视觉等宽而在 `Off` 后带空格，译文「副手：」采用全角冒号自然等宽，颜色码与 `%s` 占位符完整。

#### entry-00176
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2169`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2169)（`("#LIGHT_BLUE#Psi :#LAST#%s"):tformat(...)`）。念力挂载槽位显示，译文「灵能：」与上下文槽位命名一致，`%s` 占位符与颜色标签无误。

#### entry-00177
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2180`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2180)（`("#LIGHT_BLUE#Ammo:#LAST#%s"):tformat(...)`）。箭袋弹药槽位显示，`#LIGHT_BLUE#...#LAST#` 及 `%s` 占位符完整，术语准确。

#### entry-00178
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2191`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2191)（`("#LIGHT_BLUE#Unarmed:#LAST#%s"):tformat(...)`）。徒手且装备手套时的前缀，`%s` 接收手套简名，格式化与颜色码完全匹配。

#### entry-00179
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2201`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2201)（`_t"#LIGHT_BLUE#Unarmed:#LAST#"`）。徒手且未装备手套时的伤害前缀，无占位符，颜色标签与标点无误。

#### entry-00180
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2504`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2504)（`game:delayedLogMessage(self, nil, "mitosis_damage", "#DARK_GREEN##Source# shares damage with %s oozes!", string.his_her(self))`）。`%s` 接收 `string.his_her(self)` 代词所有格（如“他的”/“它的”），译文「#Source#和%s软泥怪平分伤害！」通顺无误，标签 `#Source#` 与感叹号保留完整。

#### entry-00181
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2515`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2515)（`game:delayedLogMessage(..., "#CRIMSON##Source# teleports some damage to #Target#!")`）。移位护盾转移伤害机制，`#CRIMSON#`、`#Source#`、`#Target#` 及末尾感叹号均匹配。

#### entry-00182
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:2972`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L2972)（`game:delayedLogMessage(..., "#CRIMSON##Source# steals life from #Target#!")`）。生命吸取战斗日志，标签 `#CRIMSON#`、`#Source#`、`#Target#` 完备，语意契合机制。

#### entry-00183
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:3159`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L3159)（`game.flyers:add(..., _t"RESURRECT!", ...)`）。复活飘字提示，感叹号保留，翻译准确。

#### entry-00184
- **结论**：存在疑点
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:3974`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L3974)（`Dialog:simpleLongPopup(_t"Level 50!", _t"You have achieved #LIGHT_GREEN#level 50#WHITE#, congratulations!\n\nThis level is special, it granted you #LIGHT_GREEN#10#WHITE# more stat points, #LIGHT_GREEN#3#WHITE# more class talent points and #LIGHT_GREEN#3#WHITE# more generic talent points.\nNow go forward boldly and triumph!", 400)`）。
  1. **换行缺失**：英文原文在第一段「祝贺你！」与第二段「这个等级很特殊」之间存在空行（即 `\n\n` 双换行），而译文仅保留单换行 `\n`，弹窗排版缺少段落间空行。
  2. **细微语病**：末句「勇敢的向前」在修饰动词「向前」时按规范宜作状语「勇敢地向前」。
  3. 四处 `#LIGHT_GREEN#...#WHITE#` 颜色标记与数值顺序均正确。

#### entry-00185
- **结论**：细微观察
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4047`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4047)（`game.log("#00ffff#Welcome to level %d [%s].", self.level, self:getName():capitalize())`）。
  1. 原文方括号为紧凑无空格 `[%s]`，译文增加了两侧内空格作 `[ %s ]`。
  2. 占位符 `%d`（等级）、`%s`（角色名）顺序及颜色码 `#00ffff#` 均准确无误。

#### entry-00186
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4048`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4048)（`_t"Press p to use them."`）。玩家自身升级时的按键提示，大写键位并译作「P 键」符合界面规范，标点正确。

#### entry-00187
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4049`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4049)（`("Select %s in the party list and press G to use them."):tformat(self.name)`）。非玩家队友升级时的按键提示，占位符 `%s` 保留，键位与标点无误。

#### entry-00188
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4073`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4073)（`game.logPlayer(self, "#AQUAMARINE#You have gained one more life (%d remaining).", self.easy_mode_lifes)`）。简单模式获得复活生命数提示，颜色码 `#AQUAMARINE#`、占位符 `%d` 及全角括号使用正确。

#### entry-00189
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4190`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4190)（`game.flyers:add(..., _t"+ENCUMBERED!", ...)`）。超重状态产生时的飘字提示，前缀 `+` 与叹号保留完整。

#### entry-00190
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4199`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4199)（`game.flyers:add(..., _t"-ENCUMBERED!", ...)`）。解除超重状态时的飘字提示，前缀 `-` 与叹号保留完整。

#### entry-00191
- **结论**：细微观察
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:4530`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L4530)（`game.logSeen(self, "%s warps space-time to equip: %s.", self:getName():capitalize(), names)`）。
  1. 原文 `warps space-time` 对应时空守卫快速切换武器特性，译文译为「扭曲空间」，漏译了“时间”（同文件 entry-00193 将 `spacetime` 译为「时空」）；
  2. 后半句 `to equip: %s` 意译为「切换武器至：%s」准确契合该处快速切换武器语境；两个 `%s` 占位符顺序与冒号标点无误。

#### entry-00192
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:5486`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5486)（`game.logPlayer(self, "#STEEL_BLUE#You've moved to another time thread.")`）。时空分支移动日志，颜色码 `#STEEL_BLUE#` 与句末标点完整，术语“时间线”贴合时空系语境。

#### entry-00193
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:5531`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5531)（`game.logPlayer(self, "#LIGHT_RED#You feel the edges of spacetime begin to ripple and bend!")`）。悖论值不稳警告，颜色标签 `#LIGHT_RED#` 与感叹号保留，翻译流畅。

#### entry-00194
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:5541`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5541)（`game.logPlayer(self, "#LIGHT_BLUE#Spacetime has calmed...  somewhat.")`）。时空稳定日志，颜色码 `#LIGHT_BLUE#` 与省略号对应完整，语气契合原文。

#### entry-00195
- **结论**：细微观察
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:5857`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5857)（`game.logPlayer(self, "You do not have enough %s to use %s.", res_def.name, ab.name)`）。
  1. 占位符参数第一位为资源名，第二位为技能名，译文顺序正确；
  2. 原文为无冒号普通陈述句，译文在第二个占位符前添加了冒号「施展：%s。」（同模块其他类似资源不足提示均无冒号）。

#### entry-00196
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:5983`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L5983)（`game.logSeen(self, "%s fumbles and fails to use %s, injuring %s!", self:getName():capitalize(), ab.name, self:his_her_self())`）。三个 `%s` 分别为角色名、技能名、自身代词，译文「%s使用%s失败，还弄伤了%s！」三个占位符顺序完全一致，标点正确。

#### entry-00197
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:7017`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L7017)（`("%s will now be used as often as possible automatically."):tformat(t.name:capitalize())`）。技能自动释放弹窗说明，`%s` 占位符保留，语意通顺完整。

#### entry-00198
- **结论**：细微观察
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:7805`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L7805)（`if not dir then dir = _t"but fumbles!" else ... end; self:logCombat(who, "#Source# deflects the projectile from #Target# %s", dir)`）。
  1. 该句为抛射物偏转未计算出偏移坐标时的局部拼接片段，填入母句 `"#Source# deflects the projectile from #Target# %s"`。母句在 `mod-tome.lua:355` 中翻译为「#Source#偏移来自#Target#的抛射物%s」（占位符前无空格或逗号），拼接后日志呈现为「……抛射物但是失败了！」，语流略欠停顿；
  2. 词条本身翻译「但是失败了！」（或可译“但是失手了！”）准确保留了感叹号及失败语意。

#### entry-00199
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:7807`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L7807)（`dir = ("to the %s!"):tformat(dir)`）。`%s` 接收罗盘方位词（由 `compassDirection` 返回，如“北”/“南”），拼接后为「到北！」等，占位符 `%s` 及感叹号保留完好。

#### entry-00200
- **结论**：未发现问题
- **可核验依据**：源码见 [`game/modules/tome/class/Actor.lua:7953`](file:///workspace/t-engine4/game/modules/tome/class/Actor.lua#L7953)（`game.logPlayer(self, "You can not drop items while sleeping.")`）。睡眠状态下丢弃物品拦截提示，无占位符，句末句号与语意均准确。