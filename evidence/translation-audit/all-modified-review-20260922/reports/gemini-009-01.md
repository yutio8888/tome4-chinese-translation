### batch-009 译文复核报告

**复核说明：**
- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-009.md`
- **文件哈希**：`53b0d48ef3b2c663a51650680776a4f39f1668b13368f7c0026d44d275f81238`（已核验一致）
- **条目范围**：`entry-00321` 至 `entry-00360`（共 40 条，全部位于 `mod-tome.lua`）
- **核验源码基准**：公开源码库 `t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`

---

#### entry-00321
- **位置**：`mod-tome.lua:1233`
- **section**：`mod-tome/class/UserChatExtension.lua`
- **原文**：`#ANTIQUE_WHITE#has linked a talent: #WHITE# %s`
- **译文**：`#ANTIQUE_WHITE#链接了一个技能：#WHITE# %s`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/UserChatExtension.lua:83` 中通过 `addMessage` 格式化玩家在聊天频道发送的技能链接，占位符 `%s` 前空格及颜色控制码 `#ANTIQUE_WHITE#`、`#WHITE#` 均与原文一致，`talent` 译为“技能”符合术语惯例。

---

#### entry-00322
- **位置**：`mod-tome.lua:1250`
- **section**：`mod-tome/class/WorldNPC.lua`
- **原文**：`#Source# kills #Target#.`
- **译文**：`#Source#击杀了#Target#。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/WorldNPC.lua:114, 140` 在大地图遭遇战计算中调用 `logCombat(src, self, ...)`，日志标签 `#Source#` 与 `#Target#` 正确保留，标点转换正确。

---

#### entry-00323
- **位置**：`mod-tome.lua:1251`
- **section**：`mod-tome/class/WorldNPC.lua`
- **原文**：`#Target# kills #Source#.`
- **译文**：`#Target#击杀了#Source#。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/WorldNPC.lua:136` 调用 `self:logCombat(target, "#Target# kills #Source#.")`，日志标签 `#Target#` 与 `#Source#` 保留完整，战斗主被动关系与源码逻辑一致。

---

#### entry-00324
- **位置**：`mod-tome.lua:1274`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`Boss fight!`
- **译文**：`Boss战！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:204, 218, 232, 249` 用于竞技场各 Boss 生成时弹出的对话框标题（`Chat.new("arena", {name=_t"Boss fight!"}, ...)`），翻译准确，感叹号匹配。

---

#### entry-00325
- **位置**：`mod-tome.lua:1275`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`Victory!!`
- **译文**：`胜利！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:209, 223, 237, 256` 用于竞技场 Boss 击败结算对话框标题（`Chat.new("arena", {name=_t"Victory!!"}, ...)`），双感叹号正确转换为全角。

---

#### entry-00326
- **位置**：`mod-tome.lua:1280`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：` appear!!`
- **译文**：` 出现了！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:319` 中 `if e.wave > 1 then verb = _t" appear!!" ...`，随后与怪物名拼接在日志输出；译文保留了词首前导空格与双感叹号。

---

#### entry-00327
- **位置**：`mod-tome.lua:1281`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：` appears!!`
- **译文**：` 出现了！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:319` 中 `else verb = _t" appears!!" end`（单怪波次），译文保留了词首前导空格与双感叹号。

---

#### entry-00328
- **位置**：`mod-tome.lua:1282`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_RED#WARNING! %s appears!!!`
- **译文**：`#LIGHT_RED#警告！%s 出现了！！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:354` 在生成竞技场 Boss 时输出警报日志，颜色码 `#LIGHT_RED#`、占位符 `%s` 及感叹号均匹配。

---

#### entry-00329
- **位置**：`mod-tome.lua:1286`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_RED#WARNING! Rej Arkatis, the master of the arena, appears!!!`
- **译文**：`#LIGHT_RED#警告！竞技场主宰瑞吉·阿卡提斯，出现了！！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:395` 生成预设竞技场霸主时输出日志，专名 Rej Arkatis 译音准确，颜色码与标点一致。

---

#### entry-00330
- **位置**：`mod-tome.lua:1288`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_RED#WARNING! %s, the master of the arena, appears!!!`
- **译文**：`#LIGHT_RED#警告！竞技场主宰%s，出现了！！！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:438` 生成玩家历史霸主角色时调用（传入 `m.name`），占位符 `%s` 与称号结构处理恰当，颜色码一致。

---

#### entry-00331
- **位置**：`mod-tome.lua:1291`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_GREEN#The audience cheers!`
- **译文**：`#LIGHT_GREEN#观众发出欢呼！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:482, 487, 502` 在超杀、一击秒杀或击杀高等级敌人使 rank 提升幅度超过阈值时触发日志，颜色码 `#LIGHT_GREEN#` 匹配。

---

#### entry-00332
- **位置**：`mod-tome.lua:1293`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_GREEN#Your score multiplier increases by #WHITE#%d#LIGHT_GREEN#!`
- **译文**：`#LIGHT_GREEN#你的分数加成增加了#WHITE#%d#LIGHT_GREEN#！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:493` 传入怪物奖励倍率 `self.arenaBonusMult`，占位符 `%d` 与嵌套颜色码 `#WHITE#...#LIGHT_GREEN#` 保持一致。

---

#### entry-00333
- **位置**：`mod-tome.lua:1294`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#LIGHT_GREEN#Your score multiplier increases by #WHITE#0.1#LIGHT_GREEN#!`
- **译文**：`#LIGHT_GREEN#你的分数加成增加了#WHITE#0.1#LIGHT_GREEN#！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:498` 连续击杀数超过 5 时触发固定加成，数值与颜色码完全匹配。

---

#### entry-00334
- **位置**：`mod-tome.lua:1295`
- **section**：`mod-tome/class/generator/actor/Arena.lua`
- **原文**：`#YELLOW#You defeat an experienced enemy!`
- **译文**：`#YELLOW#你杀死了一名老练的敌人！`
- **结论**：未发现问题（细微观察）
- **可核验依据**：源码 `game/modules/tome/class/generator/actor/Arena.lua:500` 位于 `e.on_die` 死亡回调内部，当怪物等级高于玩家 3 级以上时触发。虽然 `defeat` 直译为“击败”，但在死亡触发语境下译为“杀死”符合实际机制事实，颜色标签 `#YELLOW#` 正确。

---

#### entry-00335
- **位置**：`mod-tome.lua:1341`
- **section**：`mod-tome/class/interface/ActorObjectUse.lua`
- **原文**：`%s activates %s %s!`
- **译文**：`%s激活了%s%s！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/ActorObjectUse.lua:214` 格式化调用为 `logSeen(self, "%s activates %s %s!", self:getName():capitalize(), self:his_her(), data.obj:getName(...))`。第二参数为物主代词（`his_her()` 返回 `他的/她/它的`），第三参数为物品名；译文 `%s激活了%s%s！` 组合后为“某某激活了他的[物品名]”，自然流畅且未额外引入“的”字导致叠词。

---

#### entry-00336
- **位置**：`mod-tome.lua:1343`
- **section**：`mod-tome/class/interface/ActorObjectUse.lua`
- **原文**：`(unknown object)`
- **译文**：`（未知物品）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/ActorObjectUse.lua:239` 在物品未被识别时作为备选名称显示；全角括号与术语翻译规范一致。

---

#### entry-00337
- **位置**：`mod-tome.lua:1360`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`You need a missile launcher (%s)!`
- **译文**：`你需要一件远程投射武器(%s)！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:82` 在角色装备弹药但未装备对应发射器时提示（传入 `ammo` 实体），占位符 `(%s)` 与术语“远程投射武器”一致。

---

#### entry-00338
- **位置**：`mod-tome.lua:1362`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`#ORCHID#Your %s CANNOT SHOOT (Resource: %s%s#LAST#).`
- **译文**：`#ORCHID#你的%s无法射击(资源：%s%s#LAST#)。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:108, 123, 138` 传参依次为武器名称、资源颜色代码（如 `#SALMON#`）、资源名称，尾随 `#LAST#` 闭合资源颜色；译文占位符与颜色闭合控制结构完全一致。

---

#### entry-00339
- **位置**：`mod-tome.lua:1364`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`#ORCHID#Target out of range.  Hold <ctrl> to force your weapon to fire at targets beyond its range (%d).`
- **译文**：`#ORCHID#目标超出范围。按住<ctrl>来强制射击超出范围(%d)的目标。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:178` 射击射程判定提示，占位符 `(%d)` 对应 `tg.warn_range`，颜色码 `#ORCHID#` 与按键标记 `<ctrl>` 均保持一致。

---

#### entry-00340
- **位置**：`mod-tome.lua:1365`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`#ORCHID#You COULD NOT SHOOT your %s (Resource: %s%s#LAST#).`
- **译文**：`#ORCHID#无法使用%s射击(资源：%s%s#LAST#)。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:216, 244` 在执行单发或连射时因资源不足中断，传参同样为武器名、资源颜色代码和资源名；译文采用符合中文习惯的无主句，占位符与颜色闭合标签对应准确。

---

#### entry-00341
- **位置**：`mod-tome.lua:1367`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`#{bold}##Source# performs a ranged critical strike against #Target#!#{normal}#`
- **译文**：`#{bold}##Source#对#Target#发起一次远程暴击！#{normal}#`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:404` 输出远程暴击日志，字体标签 `#{bold}#`、`#{normal}#` 及战斗标签 `#Source#`、`#Target#!` 对应完整。

---

#### entry-00342
- **位置**：`mod-tome.lua:1368`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`#Source# misses #target#.`
- **译文**：`#Source#没有命中#target#。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:455` 源码自身使用全小写 `#target#`（`self:logCombat(target, "#Source# misses #target#.")`），译文忠实保留该大小写，标点转换正确。

---

#### entry-00343
- **位置**：`mod-tome.lua:1371`
- **section**：`mod-tome/class/interface/Archery.lua`
- **原文**：`You must wield a ranged weapon (%s)!`
- **译文**：`你必须装备一件远程武器(%s)！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Archery.lua:689` 在进行射击但未装备远程武器时输出日志（传入 `ammo`），占位符 `(%s)` 与感叹号正确。

---

#### entry-00344
- **位置**：`mod-tome.lua:1379`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#ORCHID#%s cleverly deflects the attack with %s shield!#LAST#`
- **译文**：`#ORCHID#%s用%s的盾牌机智地偏转了这次攻击！#LAST#`
- **结论**：存在疑点
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:466` 为 `game.logSeen(target, "#ORCHID#%s cleverly deflects the attack with %s shield!#LAST#", target:getName():capitalize(), string.his_her(target))`。第二参数 `string.his_her(target)` 在 `engine/utils.lua:939` 分支中对男性实体返回 `_t"his"`（在 `engine.lua:1410` 中固定翻译为“他的”），对无性别实体返回 `_t"its"`（固定翻译为“它的”）。
  由于译文写为 `%s用%s的盾牌...`，当角色为男性或无性别时，格式化结果会出现“他的的盾牌”或“它的的盾牌”叠词语病；对比同一文件下一行 1380（entry-00345 的 `%s用%s双持武器`）及行 1381（`%s本能地硬化%s皮肤`）均未带“的”以适配“他的/它的”。

---

#### entry-00345
- **位置**：`mod-tome.lua:1380`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#ORCHID#%s parries the attack with %s dual weapons!#LAST#`
- **译文**：`#ORCHID#%s用%s双持武器使这次攻击发生偏斜！#LAST#`
- **结论**：未发现问题（细微观察）
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:484` 为双持武器的剑刃防护（Blade Ward）触发成功时的提示。译文 `%s用%s双持武器` 妥善规避了男性/中性物主代词“他的/它的”叠词问题。观察点：原文 `parries the attack` 意为“招架了攻击”，译文译作“使这次攻击发生偏斜”，略偏向意译，但完整表达了防御成功使攻击落空的游戏机制，未产生语法或格式错误。

---

#### entry-00346
- **位置**：`mod-tome.lua:1382`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#Target# repels an attack from #Source#.`
- **译文**：`#Target#击退了#Source#的进攻。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:508` 在近战格挡、招架、偏转或石肤属性生效（`repelled == true`）时调用，表示防御方化解了进攻。“击退了...的进攻”准确传达了化解攻势的机制含义，避免误解为位移击退角色本身，战斗标签与句号匹配。

---

#### entry-00347
- **位置**：`mod-tome.lua:1386`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#{bold}##Source# performs a melee critical strike against #Target#!#{normal}#`
- **译文**：`#{bold}##Source#向#Target#发起一次近战暴击！#{normal}#`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:598` 输出近战暴击日志，格式控制标签 `#{bold}#`、`#{normal}#` 与战斗标签完整无误。

---

#### entry-00348
- **位置**：`mod-tome.lua:1390`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#F53CBE#Your rampage is invigorated by your fierce attack! (+1 duration)`
- **译文**：`#F53CBE#你强力的攻击延长了你的暴走时间！（+1持续时间）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:1098` 在暴走（Rampage）状态下产生暴击且习得野蛮（Brutality）技能时增加 1 回合持续时间（`eff.dur = eff.dur + 1`），机制翻译准确，颜色码 `#F53CBE#` 与括号标注匹配。

---

#### entry-00349
- **位置**：`mod-tome.lua:1394`
- **section**：`mod-tome/class/interface/Combat.lua`
- **原文**：`#Source#'s grapple fails because #Target# is too big!`
- **译文**：`#Source#的抓取失败了，因为#Target#体型过大！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/Combat.lua:2782` 处于抓取体型判定函数 `grappleSizeCheck` 中，当目标体型阶数大于自身超过 1 级时触发失败；术语“抓取”与体型逻辑对应准确。

---

#### entry-00350
- **位置**：`mod-tome.lua:1405`
- **section**：`mod-tome/class/interface/PartyDeath.lua`
- **原文**：` (the fool)`
- **译文**：` （笨蛋）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyDeath.lua:94` 为玩家自杀时的幽默死因后缀之一，译文保留了词首半角空格与全角括号。

---

#### entry-00351
- **位置**：`mod-tome.lua:1411`
- **section**：`mod-tome/class/interface/PartyDeath.lua`
- **原文**：` (how embarrassing)`
- **译文**：` （真令人尴尬）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyDeath.lua:100` 同样为自杀死因后缀之一，译文保留了词首半角空格与全角括号。

---

#### entry-00352
- **位置**：`mod-tome.lua:1414`
- **section**：`mod-tome/class/interface/PartyDeath.lua`
- **原文**：` (yet again)`
- **译文**：` （又来了）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyDeath.lua:107` 在击杀者为玩家个人档案中击杀次数最多的凶手时追加提示（`src.name == top_killer and _t" (yet again)" or ""`），译文保留了前导空格与括号。

---

#### entry-00353
- **位置**：`mod-tome.lua:1427`
- **section**：`mod-tome/class/interface/PartyIngredients.lua`
- **原文**：`You collect a new ingredient: #LIGHT_GREEN#%s%s#WHITE#.`
- **译文**：`你搜集了一个新的材料：#LIGHT_GREEN#%s%s#WHITE#。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyIngredients.lua:83` 获取无限量材料时调用，格式化参数分别为材料图标显示串和材料名称，双 `%s` 与颜色标签对应完整。

---

#### entry-00354
- **位置**：`mod-tome.lua:1428`
- **section**：`mod-tome/class/interface/PartyIngredients.lua`
- **原文**：`You collect a new ingredient: #LIGHT_GREEN#%s%s (%d)#WHITE#.`
- **译文**：`你搜集了一个新的材料：#LIGHT_GREEN#%s%s(%d)#WHITE#。`
- **结论**：未发现问题（细微观察）
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyIngredients.lua:89` 获取有限量材料时调用，格式化参数为图标、名称及获得数量 `nb`。译文去掉了原文括号前的半角空格变为 `%s%s(%d)`，在中文语境下使物品名与数量更紧凑，占位符与颜色闭合控制码保持一致。

---

#### entry-00355
- **位置**：`mod-tome.lua:1434`
- **section**：`mod-tome/class/interface/PartyLore.lua`
- **原文**：`You can read all your collected lore in the game menu, by pressing Escape.`
- **译文**：`按 Esc 键，进入游戏菜单你可以查看所有你已经收集的札记。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PartyLore.lua:117` 首次获得手札弹出提示后输出的按键指引日志，语序前置按键说明，表意清楚准确。

---

#### entry-00356
- **位置**：`mod-tome.lua:1444`
- **section**：`mod-tome/class/interface/PlayerExplore.lua`
- **原文**：`You are exploring, press any key to stop.`
- **译文**：`你正在自动探索，请按任意键停止。`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PlayerExplore.lua:2514` 为玩家执行按键自动探索（'z' 键）时弹出的简易对话框提示文本，补充“自动”二字精准对应游戏实际功能。

---

#### entry-00357
- **位置**：`mod-tome.lua:1453`
- **section**：`mod-tome/class/interface/PlayerQuestPopup.lua`
- **原文**：`#LIGHT_GREEN#Accepted quest '%s'! #WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#接受了任务“%s”！#WHITE#（按 J 键查看任务日志）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PlayerQuestPopup.lua:55` 在接受任务时向玩家日志输出通知，任务名占位符 `%s` 采用中文引号，按键提示 `'j'` 转换为“按 J 键”，颜色码完全一致。

---

#### entry-00358
- **位置**：`mod-tome.lua:1454`
- **section**：`mod-tome/class/interface/PlayerQuestPopup.lua`
- **原文**：`#LIGHT_GREEN#Accepted quest '%s'!`
- **译文**：`#LIGHT_GREEN#接受了任务“%s”！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PlayerQuestPopup.lua:56` 在未开启弹窗设置时通过 `bignews:saySimple` 在屏幕中央大字显示，中文引号与颜色码匹配。

---

#### entry-00359
- **位置**：`mod-tome.lua:1455`
- **section**：`mod-tome/class/interface/PlayerQuestPopup.lua`
- **原文**：`#LIGHT_GREEN#Quest '%s' status updated! #WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#任务“%s”状态已经更新！#WHITE#（按 J 键查看任务日志）`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PlayerQuestPopup.lua:61` 任务子目标更新时输出日志，占位符 `%s`、颜色码与快捷键说明一致。

---

#### entry-00360
- **位置**：`mod-tome.lua:1456`
- **section**：`mod-tome/class/interface/PlayerQuestPopup.lua`
- **原文**：`#LIGHT_GREEN#Quest '%s' updated!`
- **译文**：`#LIGHT_GREEN#任务“%s”已更新！`
- **结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/interface/PlayerQuestPopup.lua:62` 任务子目标更新时的大字新闻横幅显示，格式与颜色码完整匹配。

---

### 汇总统计
- **总复核条数**：40 条（`entry-00321` ～ `entry-00360`）
- **未发现问题**：39 条（其中 3 条附带细微观察记录）
- **存在疑点**：1 条（`entry-00344`：物主代词 `%s` 传入“他的/它的”时导致“他的的盾牌/它的的盾牌”叠词语病）