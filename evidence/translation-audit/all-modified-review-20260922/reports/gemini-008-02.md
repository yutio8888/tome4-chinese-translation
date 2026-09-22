### batch-008 译文只读复核报告

#### 1. 冻结文件校验
- **复核批次**：`batch-008`
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-008.md`
- **预期 SHA-256**：`f0dcdb6b78022895014da18d163146db0523dfdeac1ce6ca44b3cd2fa8740d4c`
- **核验结果**：`f0dcdb6b78022895014da18d163146db0523dfdeac1ce6ca44b3cd2fa8740d4c`（完全匹配）
- **核验环境与基准**：公开源码基于 `t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，译文上下文基于 `mod-tome.lua` 终点 commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

#### 2. 逐条复核记录（entry-00281 至 entry-00320，共 40 条）

##### entry-00281
- **位置与词条**：`mod-tome.lua:963`（`mod-tome/class/Object.lua`）
- **原文**：`Learn shield attack talent or enable 'Always show shield combat' to see combat stats.`
- **译文**：`学习盾牌攻击技能，或者开启 '强制显示盾牌战斗数据' 选项来查看战斗数据。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:1993`。设置项名称对应 `game/modules/tome/dialogs/GameOptions.lua:425` 中的 `Always show shield combat properties`，在 `mod-tome.lua:41745` 确译为“强制显示盾牌战斗数据”，单引号内的引用名称与游戏设置实际文本一致，标点映射规范。

##### entry-00282
- **位置与词条**：`mod-tome.lua:984`（`mod-tome/class/Object.lua`）
- **原文**：`Talent level: %+d %s.`
- **译文**：`技能等级：%+d %s。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2112`，调用为 `("Talent level: %+d %s."):tformat(lvl, t and t.name or "???")`。占位符 `%+d %s` 格式与顺序一致，冒号与句号映射准确。

##### entry-00283
- **位置与词条**：`mod-tome.lua:985`（`mod-tome/class/Object.lua`）
- **原文**：`Talent level: %s.`
- **译文**：`技能等级：%s。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2117`，调用为 `("Talent level: %s."):tformat(data.desc)`。占位符 `%s` 匹配，中文标点映射正确。

##### entry-00284
- **位置与词条**：`mod-tome.lua:986`（`mod-tome/class/Object.lua`）
- **原文**：`Talent on hit(spell): %s (%d%% chance level %d).`
- **译文**：`技能（法术）命中后释放：%s (%d%% 几率等级 %d)。`
- **复核结论**：未发现问题（附细微观察）
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2127, 2134`；触发机制见 `game/modules/tome/data/damage_types.lua:641`（`src.talent_on_spell` 在法术伤害 `t.is_spell` 时触发释放技能 `d.talent`）。参数 1 为技能名（`%s`），参数 2 为几率（`%d%%`），参数 3 为技能等级（`%d`），占位符数量与顺序匹配。细微观察：中文语序“技能（法术）命中后释放：%s”略带紧凑倒装感，但含义明确且与游戏通用装备描述一致。

##### entry-00285
- **位置与词条**：`mod-tome.lua:987`（`mod-tome/class/Object.lua`）
- **原文**：`Talent on hit(nature): %s (%d%% chance level %d).`
- **译文**：`技能（自然）命中后释放：%s (%d%% 几率等级 %d)。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2147, 2154`；机制见 `damage_types.lua:652`（`src.talent_on_wild_gift` 在自然系伤害 `t.is_nature` 时触发）。占位符、百分号转义及标点完全一致。

##### entry-00286
- **位置与词条**：`mod-tome.lua:988`（`mod-tome/class/Object.lua`）
- **原文**：`Talent on hit(mindpower): %s (%d%% chance level %d).`
- **译文**：`技能（精神）命中后释放：%s (%d%% 几率等级 %d)。`
- **复核结论**：未发现问题（附细微观察）
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2167, 2174`。机制见 `damage_types.lua:663`（`src.talent_on_mind` 触发判定为 `t.is_mind`，即精神系技能/伤害）。细微观察：英文原文写为 `mindpower`，但底层机制校验的是精神攻击类别（`is_mind`）而非角色的精神强度属性（Mindpower），译文使用“（精神）”不仅与前文的“（法术）”、“（自然）”保持三系攻击对齐，且精确反映了真实机制，未生搬硬套属性术语。

##### entry-00287
- **位置与词条**：`mod-tome.lua:1005`（`mod-tome/class/Object.lua`）
- **原文**：`%d out of %d/%d.`
- **译文**：`%d，总计%d/%d。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2221`，调用逻辑为前缀 `_t"Power cost: "` 拼接 `("%d out of %d/%d."):tformat(usepower(self.use_talent.power), self.power, self.max_power)`。三个 `%d` 依次传入“技能消耗能量”、“当前能量”、“最大能量”。在游戏内显示为“能量消耗：%d，总计%d/%d。”，参数数量、顺序及语义完全吻合。

##### entry-00288
- **位置与词条**：`mod-tome.lua:1031`（`mod-tome/class/Object.lua`）
- **原文**：`This object's appearance was changed to %s`
- **译文**：`这个物品的外观被改变为 %s。`
- **复核结论**：存在疑点
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2305-2307`：
  ```lua
  desc:merge(("This object's appearance was changed to %s"):tformat(oname:toString()):toTString())
  desc:add(_t".", {"color","LAST"}, true)
  ```
  英文原文末尾故意没有句号，因为第 2307 行源码紧接着显式追加了句点 `desc:add(_t".", {"color","LAST"}, true)`。译文在占位符 `%s` 后添加了中文句号 `。`，导致运行时在游戏内拼接后必定输出形如 `这个物品的外观被改变为 [外观名]。 .` 的多余重叠标点。

##### entry-00289
- **位置与词条**：`mod-tome.lua:1032`（`mod-tome/class/Object.lua`）
- **原文**：`Press <control> to compare`
- **译文**：`按住 Ctrl 键比较`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Object.lua:2310`，为物品比对快捷键说明；`<control>` 在游戏中是文本按键提示，译为“按住 Ctrl 键”符合通用习惯。

##### entry-00290
- **位置与词条**：`mod-tome.lua:1048`（`mod-tome/class/Party.lua`）
- **原文**：`#MOCCASIN#Character control switched to %s.`
- **译文**：`#MOCCASIN#角色切换至 %s。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Party.lua:299`，`game.logPlayer(actor, "#MOCCASIN#Character control switched to %s.", actor:getName())`。颜色代码 `#MOCCASIN#` 与占位符 `%s` 完好，标点正确。

##### entry-00291
- **位置与词条**：`mod-tome.lua:1058`（`mod-tome/class/Party.lua`）
- **原文**：`%s is dismissed!`
- **译文**：`%s 被遣散了！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Party.lua:408`，遣散队友日志。占位符 `%s` 与感叹号均匹配。

##### entry-00292
- **位置与词条**：`mod-tome.lua:1063`（`mod-tome/class/Party.lua`）
- **原文**：`close`
- **译文**：`较近了`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Party.lua:424`，护送任务中 NPC 判定传送门距离（`< 8` 为 `very close`“很近了”，`< 16` 为 `close`“较近了”，其余为 `still far away`“还很远”），并传入 `The portal is %s, to the %s.` 拼接。梯级语意贴合。

##### entry-00293
- **位置与词条**：`mod-tome.lua:1079`（`mod-tome/class/Player.lua`）
- **原文**：`Level change (%s)!`
- **译文**：`地图切换 (%s)！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:292`，角色踏上换层地形时的浮空文字 `game.flyers:add(..., ("Level change (%s)!"):tformat(g:getName()), ...)`。占位符与标点一致。

##### entry-00294
- **位置与词条**：`mod-tome.lua:1086`（`mod-tome/class/Player.lua`）
- **原文**：`LOW HEALTH!`
- **译文**：`生命值低！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:790`，生命值低于 30% 时的屏幕浮空红字提示。翻译简明准确。

##### entry-00295
- **位置与词条**：`mod-tome.lua:1093`（`mod-tome/class/Player.lua`）
- **原文**：`Automatic use of talent %s #DARK_RED#skipped#LAST#: cooldown too low (%d).`
- **译文**：`%s 的自动施法被#DARK_RED#跳过#LAST#了：冷却时间太低(%d)。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:971`，参数 1 为技能名（`%s`），参数 2 为冷却回合（`%d`）。占位符、颜色代码 `#DARK_RED#...#LAST#` 及冒号句号均正确。

##### entry-00296
- **位置与词条**：`mod-tome.lua:1097`（`mod-tome/class/Player.lua`）
- **原文**：`losing breath!`
- **译文**：`窒息！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:1078, 1219`，角色因空气不足（`self.air_regen < 0`）终止休息或探索的提示。

##### entry-00297
- **位置与词条**：`mod-tome.lua:1098`（`mod-tome/class/Player.lua`）
- **原文**：`losing health!`
- **译文**：`生命值下降！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:1079`，角色生命回复非正（`self.life_regen <= 0`）导致无法安全休息时的提示。

##### entry-00298
- **位置与词条**：`mod-tome.lua:1115`（`mod-tome/class/Player.lua`）
- **原文**：`Your antimagic disrupts %s.`
- **译文**：`你的反魔法技能打断了 %s。`
- **复核结论**：未发现问题（附细微观察）
- **可核验依据**：源码溯源显示，该字符串历史位于 `game/modules/tome/class/Player.lua:playerUseObject`，在 commit `5f7e8cb9a3` 重构至 `game/modules/tome/class/Object.lua:199` 的 `canUseObject`。细微观察：机制层面是角色的反魔法被动禁魔属性（`forbid_arcane`）使得奥术物品（`arcane`）无法激活（日文译作“反魔之力妨害了”，韩文译作“反魔法妨碍了”），译文“反魔法技能打断了”系早期汉化沿用表述，占位符 `%s` 正确。

##### entry-00299
- **位置与词条**：`mod-tome.lua:1116`（`mod-tome/class/Player.lua`）
- **原文**：`Your antimagic disrupts %s.`
- **译文**：`你的反魔法技能打断了 %s。`
- **复核结论**：未发现问题（附细微观察）
- **可核验依据**：对应重构后 `Object.lua:199` 中 `("Your antimagic disrupts %s."):tformat(...)` 调用的条目，与 entry-00298 相同。

##### entry-00300
- **位置与词条**：`mod-tome.lua:1123`（`mod-tome/class/Player.lua`）
- **原文**：`You use the %s on the pedestal. There is a distant 'clonk' sound.`
- **译文**：`你在基座上使用了 %s。你听到远处传来一声“咔嗒”声。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:1680`，宝珠基座解密日志。占位符 `%s` 匹配，拟声词引号转换规范。

##### entry-00301
- **位置与词条**：`mod-tome.lua:1124`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_RED#%s briefly catches sight of you!`
- **译文**：`#LIGHT_RED#%s 短暂地瞥见了你！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Player.lua:1703`，潜行或隐形中被敌人瞬间瞥见的警告日志。颜色代码、占位符与标点一致。

##### entry-00302
- **位置与词条**：`mod-tome.lua:1132`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Accepted quest '%s'!#WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#接受了任务“%s”！#WHITE#（按 J 键查看任务日志）`
- **复核结论**：未发现问题（附历史残留观察）
- **可核验依据**：源码溯源显示，任务弹窗逻辑已在 `game/modules/tome/class/interface/PlayerQuestPopup.lua:59` 统一实现，当前代码中的文本在感叹号后带空格（`! #WHITE#`），`mod-tome.lua:1132` 属于 `-- old translated text` 历史保留条目。译文本身的颜色码 `#LIGHT_GREEN#` / `#WHITE#`、占位符 `%s` 及标点映射完全正确。

##### entry-00303
- **位置与词条**：`mod-tome.lua:1133`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Accepted quest '%s'!`
- **译文**：`#LIGHT_GREEN#接受了任务“%s”！`
- **复核结论**：未发现问题
- **可核验依据**：对应任务接取提示，颜色代码与占位符匹配正确。

##### entry-00304
- **位置与词条**：`mod-tome.lua:1134`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' status updated!#WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#任务“%s”状态已经更新！#WHITE#（按 J 键查看任务日志）`
- **复核结论**：未发现问题
- **可核验依据**：对应任务状态更新日志，颜色代码、占位符与标点一致。

##### entry-00305
- **位置与词条**：`mod-tome.lua:1135`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' updated!`
- **译文**：`#LIGHT_GREEN#任务“%s”已更新！`
- **复核结论**：未发现问题
- **可核验依据**：对应任务更新简报，颜色代码与占位符匹配正确。

##### entry-00306
- **位置与词条**：`mod-tome.lua:1136`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' completed!#WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）`
- **复核结论**：未发现问题
- **可核验依据**：对应任务完成日志，颜色代码、占位符与标点一致。

##### entry-00307
- **位置与词条**：`mod-tome.lua:1137`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' completed!`
- **译文**：`#LIGHT_GREEN#任务“%s”已完成！`
- **复核结论**：未发现问题
- **可核验依据**：对应任务完成简报，颜色代码与占位符匹配正确。

##### entry-00308
- **位置与词条**：`mod-tome.lua:1138`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' is done!#WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）`
- **复核结论**：未发现问题
- **可核验依据**：对应任务达成日志，颜色代码、占位符与标点一致。

##### entry-00309
- **位置与词条**：`mod-tome.lua:1139`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_GREEN#Quest '%s' done!`
- **译文**：`#LIGHT_GREEN#任务“%s”已完成！`
- **复核结论**：未发现问题
- **可核验依据**：对应任务达成简报，颜色代码与占位符匹配正确。

##### entry-00310
- **位置与词条**：`mod-tome.lua:1140`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_RED#Quest '%s' is failed!#WHITE#(Press 'j' to see the quest log)`
- **译文**：`#LIGHT_RED#任务“%s”失败！#WHITE#（按 J 键查看任务日志）`
- **复核结论**：未发现问题
- **可核验依据**：对应任务失败日志，颜色代码 `#LIGHT_RED#`、占位符与标点一致。

##### entry-00311
- **位置与词条**：`mod-tome.lua:1141`（`mod-tome/class/Player.lua`）
- **原文**：`#LIGHT_RED#Quest '%s' failed!`
- **译文**：`#LIGHT_RED#任务“%s”失败了！`
- **复核结论**：未发现问题
- **可核验依据**：对应任务失败简报，颜色代码与占位符匹配正确。

##### entry-00312
- **位置与词条**：`mod-tome.lua:1174`（`mod-tome/class/Store.lua`）
- **原文**：`This entity can not access inventories.`
- **译文**：`该实体无法使用物品栏。`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Store.lua:282`，针对无物品栏实体（`who.no_inventory_access`）访问商店的提示。语义准确。

##### entry-00313
- **位置与词条**：`mod-tome.lua:1188`（`mod-tome/class/Trap.lua`）
- **原文**：`(beneficial)`
- **译文**：`（有益）`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:132`，陷阱提示信息中的属性标签，全角括号转换规范。

##### entry-00314
- **位置与词条**：`mod-tome.lua:1189`（`mod-tome/class/Trap.lua`）
- **原文**：`(beneficial to enemies)`
- **译文**：`（对敌人有益）`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:134`，敌对陷阱增益标签，全角括号规范，语义准确。

##### entry-00315
- **位置与词条**：`mod-tome.lua:1190`（`mod-tome/class/Trap.lua`）
- **原文**：`(safe)`
- **译文**：`（安全）`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:137`，安全陷阱标签，全角括号规范。

##### entry-00316
- **位置与词条**：`mod-tome.lua:1201`（`mod-tome/class/Trap.lua`）
- **原文**：`\n#LIGHT_BLUE#Trap Description:#WHITE#\n`
- **译文**：`\n#LIGHT_BLUE#陷阱说明：#WHITE#\n`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:232`，拆解陷阱确认框中的描述前缀。首尾两个换行符 `\n` 及颜色码严格保留一致。

##### entry-00317
- **位置与词条**：`mod-tome.lua:1213`（`mod-tome/class/Trap.lua`）
- **原文**：`You set off the trap!`
- **译文**：`你触发了陷阱！`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:249`，拆除陷阱失手引爆提示，感叹号匹配，语义准确。

##### entry-00318
- **位置与词条**：`mod-tome.lua:1223`（`mod-tome/class/Trap.lua`）
- **原文**：`#CADET_BLUE#You %s a trap (%s).`
- **译文**：`#CADET_BLUE#你%s了一个陷阱(%s)。`
- **复核结论**：存在疑点
- **可核验依据**：源码位于 `game/modules/tome/class/Trap.lua:290`：
  ```lua
  game.log("#CADET_BLUE#You %s a trap (%s).", avoid, self:getName())
  ```
  第一个参数 `avoid` 来自同一文件第 272-280 行，其在 `mod-tome.lua:1218-1222` 的对应译文为：
  - `ignore` -> `无视`
  - `simply ignore` -> `轻松无视了`
  - `carefully avoid` -> `小心避开了`
  - `somehow avoid` -> `不知怎么避开了`
  - `dodge` -> `躲开了`
  在 5 种回避动作中，除“无视”外，其余 4 种在译文中均已自带“了”或动结补语（“轻松无视了”、“小心避开了”、“不知怎么避开了”、“躲开了”）。模板译文固定带“了一个陷阱”，运行时代入会形成重叠双“了”语病（如：“你轻松无视了了一个陷阱”、“你躲开了了一个陷阱”）。对比第 1224 行第三人称日志的译法 `t("#CADET_BLUE#%s %ss %s.", "#CADET_BLUE#%s%s%s。", "logSeen")` 未附带多余的“了”，本条模板存在拼接瑕疵。

##### entry-00319
- **位置与词条**：`mod-tome.lua:1231`（`mod-tome/class/UserChatExtension.lua`）
- **原文**：`#ANTIQUE_WHITE#has linked an item: #WHITE# %s`
- **译文**：`#ANTIQUE_WHITE#链接了一件物品：#WHITE# %s`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/UserChatExtension.lua:79`，用于玩家在公聊频道发送物品超链接。颜色码与占位符 `%s` 匹配无误。

##### entry-00320
- **位置与词条**：`mod-tome.lua:1232`（`mod-tome/class/UserChatExtension.lua`）
- **原文**：`#ANTIQUE_WHITE#has linked a creature: #WHITE# %s`
- **译文**：`#ANTIQUE_WHITE#链接了一个生物：#WHITE# %s`
- **复核结论**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/class/UserChatExtension.lua:81`，用于公聊频道发送生物超链接。颜色码与占位符 `%s` 匹配无误。

---

#### 3. 疑点与观察汇总

1. **标点重复疑点（entry-00288）**：
   - 条目：`This object's appearance was changed to %s`
   - 原因：源码 `Object.lua:2307` 在该语句后紧跟调用 `desc:add(_t".", ...)` 追加英文句号。译文末尾自带中文句号 `。`，导致游戏内实际显示为重叠标点 `。 .`。
2. **语境拼接冲突疑点（entry-00318）**：
   - 条目：`#CADET_BLUE#You %s a trap (%s).` -> `#CADET_BLUE#你%s了一个陷阱(%s)。`
   - 原因：传入 `%s` 的回避动作（`avoid`）在同一 section 译文中大多已带“了”（“躲开了”、“小心避开了”等），代入后产生“躲开了了一个陷阱”的双“了”病句。
3. **机制与译名细节观察（entry-00284/00286、entry-00298/00299、entry-00302-00311）**：
   - entry-00286 英文写为 `mindpower`，但实际对应 `t.is_mind` 攻击类型，译文使用“精神”准确反映机制。
   - entry-00298/00299 对应奥术与反魔法冲突的 `canUseObject` 校验，沿用了早期汉化的“反魔法技能打断了”习惯译法。
   - entry-00302 至 entry-00311 为 `mod-tome.lua` 内标注的 `-- old translated text` 历史保留条目，新版弹窗实现已移入 `interface/PlayerQuestPopup.lua`。