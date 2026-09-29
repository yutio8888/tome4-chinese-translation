### 批次与环境核验

- **复核批次**：`batch-011`（共 40 条，编号范围 `entry-00401` 至 `entry-00440`）
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-011.md`
  - 预期 SHA-256：`fc8774a52967fe8a5c673380cf93f77d0a0550aac45fc80853ff2b1462938681`
  - 实际核验结果：`fc8774a52967fe8a5c673380cf93f77d0a0550aac45fc80853ff2b1462938681`（核验一致）
- **源码依据**：公开源码 `engine/tome` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git -C /workspace/t-engine4 show` 读取）。
- **译文终点**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（工作区当前 `mod-tome.lua` 与该终点一致）。

---

### 逐条复核报告（entry-00401 至 entry-00440）

#### entry-00401
- **位置**：`mod-tome.lua:2314`；section：`mod-tome/class/uiset/Classic.lua`
- **原文**：`Press 'm' to setup`
- **译文**：`按 M 键设置`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Classic.lua:365` 在快捷栏鼠标提示中追加 `_t"Press 'm' to setup"`。译文将单引号快捷键规范转换为中文界面习惯的大写字母“按 M 键设置”，准确无误，无占位符或控制字符。

#### entry-00402
- **位置**：`mod-tome.lua:2323`；section：`mod-tome/class/uiset/Classic.lua`
- **原文**：`Linked by: `
- **译文**：`链接者： `
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Classic.lua:422` 中 `tstring{..., _t"Linked by: "}` 后通过 `merge(str)` 拼接发送链接的角色名称。译文保留了原文字符串尾部的空格，全角冒号规范，拼接逻辑正确。

#### entry-00403
- **位置**：`mod-tome.lua:2364`；section：`mod-tome/class/uiset/ClassicPlayerDisplay.lua`
- **原文**：`Encumbered! (%d/%d)`
- **译文**：`超重！(%d/%d)`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/ClassicPlayerDisplay.lua:300` 调用 `("Encumbered! (%d/%d)"):tformat(player:getEncumbrance(), player:getMaxEncumbrance())`。译文字符 `%d/%d` 占位符数量与类型完全一致，感叹号与括号标点无损。

#### entry-00404
- **位置**：`mod-tome.lua:2383`；section：`mod-tome/class/uiset/ClassicPlayerDisplay.lua`
- **原文**：` [Boss]`
- **译文**：` [Boss]`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/ClassicPlayerDisplay.lua:450` 用于竞技场波次 UI 显示头目等级。同组条目保留通用术语 `[Boss]` 并保留前导空格（与 ` [小Boss]`、` [最终战]` 一致），排版与语义未破坏。

#### entry-00405
- **位置**：`mod-tome.lua:2438`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`[MiniBoss]`
- **译文**：`[小Boss]`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1072` 在竞技场事件赋值 `_event = _t"[MiniBoss]"`。译为 `[小Boss]` 准确恰当，括号完整。

#### entry-00406
- **位置**：`mod-tome.lua:2439`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`[Boss]`
- **译文**：`[Boss]`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1074` 赋值 `_event = _t"[Boss]"`。保留通用游戏词汇 `[Boss]`，与整体风格一致。

#### entry-00407
- **位置**：`mod-tome.lua:2440`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`[Final]`
- **译文**：`[最终]`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1076` 赋值 `_event = _t"[Final]"`，后续拼接至波次字符串后展示。译为 `[最终]` 准确。

#### entry-00408
- **位置**：`mod-tome.lua:2441`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`Wave(TOP) %d %s`
- **译文**：`波次（最高）%d %s`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1081` 调用 `aprint(px, py, ("Wave(TOP) %d %s"):tformat(arena.currentWave, _event), 255, 255, 100)`。占位符 `%d %s` 顺序与类型完全一致，(TOP) 译为“（最高）”符合语义。

#### entry-00409
- **位置**：`mod-tome.lua:2446`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`Saving... %d%%`
- **译文**：`正在保存…%d%%`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1126` 调用 `("Saving... %d%%"):tformat(p * 100)`。占位符 `%d%%`（整数与转义百分号）准确保留，省略号规范转为中文 `…`。

#### entry-00410
- **位置**：`mod-tome.lua:2466`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`\nTurns remaining: %s`
- **译文**：`\n剩余回合数：%s`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1432` 中 `text = text..("\nTurns remaining: %s"):tformat(a.summon_time)`。前导换行符 `\n` 及占位符 `%s` 完整对应，冒号转全角。

#### entry-00411
- **位置**：`mod-tome.lua:2484`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`Press 'm' to setup`
- **译文**：`按 M 键设置`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1825` 工具栏快捷栏提示文本，与 entry-00401 相同，翻译准确一致。

#### entry-00412
- **位置**：`mod-tome.lua:2490`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`Left mouse to show known talents`
- **译文**：`左键点击显示已掌握的技能`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:1887` 工具栏技能按钮悬浮提示 `_t"Left mouse to show known talents"`。译文通顺准确，与同组 `左键点击显示物品栏`（2487）等平行条目风格统一。

#### entry-00413
- **位置**：`mod-tome.lua:2499`；section：`mod-tome/class/uiset/Minimalist.lua`
- **原文**：`Clicking will open#LIGHT_BLUE##{italic}#%s#WHITE##{normal}# in your browser`
- **译文**：`点击将会在你的默认浏览器中打开#LIGHT_BLUE##{italic}#%s#WHITE##{normal}#`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/class/uiset/Minimalist.lua:2080` 中通过 `toTString()` 解析颜色控制码 `#LIGHT_BLUE##{italic}#` 与 `#WHITE##{normal}#`，译文完整保留了控制码及 `%s` 占位符；句式语序根据中文表达习惯将状语“在你的默认浏览器中”置于谓语动词前，通顺自然。

#### entry-00414
- **位置**：`mod-tome.lua:2551`；section：`mod-tome/data/achievements/donator.lua`
- **原文**：`Bronze Donator`
- **译文**：`青铜捐赠者`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/donator.lua:22` 成就名称。严格遵循术语库 `Donator` -> `捐赠者`（preferred core，注明不写作“捐助者”），准确。

#### entry-00415
- **位置**：`mod-tome.lua:2557`；section：`mod-tome/data/achievements/donator.lua`
- **原文**：`Stralite Donator`
- **译文**：`斯莱特捐赠者`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/donator.lua:34` 成就名称。严格遵循术语库 `stralite` -> `斯莱特`（preferred global，不使用旧条目“蓝皓石”）与 `Donator` -> `捐赠者`，准确。

#### entry-00416
- **位置**：`mod-tome.lua:2573`；section：`mod-tome/data/achievements/events.lua`
- **原文**：`The Rat Lich`
- **译文**：`鼠巫妖`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/events.lua:45` 成就名称。遵循术语库 `Lich` -> `巫妖`（existing core），准确。

#### entry-00417
- **位置**：`mod-tome.lua:2574`；section：`mod-tome/data/achievements/events.lua`
- **原文**：`Killed the terrible Rat Lich.`
- **译文**：`杀死可怕的鼠巫妖。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/events.lua:47` 成就描述。专名、定语与句末标点准确对应。

#### entry-00418
- **位置**：`mod-tome.lua:2644`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Did over 600 damage in one attack.`
- **译文**：`在一次攻击中造成超过 600 点伤害。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/kills.lua:28` 伤害成就描述。数值与机制表述准确。

#### entry-00419
- **位置**：`mod-tome.lua:2646`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Did over 1500 damage in one attack.`
- **译文**：`在一次攻击中造成超过1500点伤害。`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/achievements/kills.lua:37`。语义无误，但在同组连续伤害成就中，entry-00418、00420、00421 均为“超过 600 点”、“超过 3000 点”、“超过 6000 点”（数字前后保留空格），本条为“超过1500点”（无空格），存在平行条目排版微小不一致。

#### entry-00420
- **位置**：`mod-tome.lua:2648`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Did over 3000 damage in one attack.`
- **译文**：`在一次攻击中造成超过 3000 点伤害。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/kills.lua:42` 伤害成就描述，数值与语义准确。

#### entry-00421
- **位置**：`mod-tome.lua:2650`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Did over 6000 damage in one attack.`
- **译文**：`在一次攻击中造成超过 6000 点伤害。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/kills.lua:47` 伤害成就描述，数值与语义准确。

#### entry-00422
- **位置**：`mod-tome.lua:2690`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Killed all four bosses of the Slime Tunnels.`
- **译文**：`杀死史莱姆通道的4个boss。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/kills.lua:250` 成就描述。地名“史莱姆通道”（Slime Tunnels）及头目数量准确。

#### entry-00423
- **位置**：`mod-tome.lua:2694`；section：`mod-tome/data/achievements/kills.lua`
- **原文**：`Avoid death 50 times with a life-saving talent.`
- **译文**：`使用技能躲避50次死亡。`
- **复核结论**：存在疑点
- **可核验依据**：
  1. 源码成就定义 `game/modules/tome/data/achievements/kills.lua:268`（成就 ID `AVOID_DEATH`）。
  2. 源码触发点：
     - `game/modules/tome/class/Actor.lua:2882`（受到致死攻击时触发 `T_SECOND_LIFE` 第二生命）；
     - `game/modules/tome/data/talents/uber/mag.lua:347`（受到致死伤害时触发觉醒技 `Cauterize` 溃灭/烧尽）；
     - `game/modules/tome/data/talents/cursed/one-with-shadows.lua:172`（致死时触发 `Shadow Decoy` 影分身替死）。
  3. 疑点分析：原文修饰词 `a life-saving talent` 明确指代游戏中的“免死技能/保命技能”。现译文“使用技能躲避50次死亡”漏译了 `life-saving`，且“躲避……死亡”容易误导玩家以为是通过位移、隐形或闪避躲开致死攻击，未能准确表达“凭借免死技能豁免/免除 50 次死亡”的机制实质。

#### entry-00424
- **位置**：`mod-tome.lua:2720`；section：`mod-tome/data/achievements/player.lua`
- **原文**：`Returned from the dead.`
- **译文**：`死而复生。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/player.lua:49`（成就“势不可挡” Unstoppable）。译文使用成语“死而复生”，精练且切合原意。

#### entry-00425
- **位置**：`mod-tome.lua:2732`；section：`mod-tome/data/achievements/player.lua`
- **原文**：`Survived the Fearscape!`
- **译文**：`在恶魔空间幸存下来！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/player.lua:107` 成就描述。符合术语库 `fearscape` -> `恶魔空间`（existing dlc），标点感叹号对应，翻译准确。

#### entry-00426
- **位置**：`mod-tome.lua:2780`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Fought the two Sorcerers and closed one invocation portal.`
- **译文**：`与两名巫师交战并关闭了1扇召唤传送门。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:142`（成就“传送门毁灭者” Portal destroyer）。主线最终战机制翻译准确。

#### entry-00427
- **位置**：`mod-tome.lua:2782`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Fought the two Sorcerers and closed two invocation portals.`
- **译文**：`与两名巫师交战并关闭了2扇召唤传送门。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:147`（成就“传送门收割者” Portal reaver）。与 00426 句式平行动词准确。

#### entry-00428
- **位置**：`mod-tome.lua:2784`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Fought the two Sorcerers and closed three invocation portals.`
- **译文**：`在关闭3扇召唤传送门的情况下，与两名巫师交战。`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:152`（成就“传送门终结者” Portal ender）。语义无误，但同系列 00426/00427 采用“与两名巫师交战并关闭了X扇……”，而本条倒置为“在关闭3扇……的情况下，与两名巫师交战”，系列句式风格不完全统一。

#### entry-00429
- **位置**：`mod-tome.lua:2788`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Win the game without ever setting foot on Maj'Eyal.`
- **译文**：`在没有去过旧大陆的情况下通关游戏。`
- **复核结论**：存在疑点
- **可核验依据**：
  1. 源码 `game/modules/tome/data/achievements/quests.lua:162`（成就“从未回头” Never Look Back And There Again）。
  2. 术语库明确规范：`Maj'Eyal` -> `马基·埃亚尔`（T.PN.WORLD，places，preferred core，明确注明“维护者于 2026-08-25 裁定采用‘马基·埃亚尔’；‘马基埃亚尔’已被取代”）。
  3. 现译文将专属世界/大陆名词 `Maj'Eyal` 意译为通俗称呼“旧大陆”，偏离了术语库裁定的专有名词译法。

#### entry-00430
- **位置**：`mod-tome.lua:2794`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Rescued the merchant from the assassin lord.`
- **译文**：`从刺客领主手中救回商人。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:177`。救商人支线成就描述准确。

#### entry-00431
- **位置**：`mod-tome.lua:2796`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Sided with the assassin lord.`
- **译文**：`与刺客领主同流合污。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:182`（成就“卑鄙小人” Poisonous）。用词生动贴切，符合反派支线语境。

#### entry-00432
- **位置**：`mod-tome.lua:2797`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Destroyer of the creation`
- **译文**：`造物的毁灭者`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:185` 成就名称，对应击杀萨拉苏尔任务线，翻译准确。

#### entry-00433
- **位置**：`mod-tome.lua:2800`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Killed Slasul even though you sided with him to learn the Legacy of the Naloren prodigy.`
- **译文**：`杀死萨拉苏尔，尽管你曾为习得觉醒技“纳鲁精灵的遗产”而与他结盟。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:191`。人名萨拉苏尔、觉醒技及专有名词“纳鲁精灵的遗产”均准确对应，语意流畅。

#### entry-00434
- **位置**：`mod-tome.lua:2804`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Completed the Master Jeweler quest with Limmir.`
- **译文**：`与利米尔一同完成了珠宝匠托付的任务“遗失的知识”。`
- **复核结论**：细微观察
- **可核验依据**：
  1. 源码 `game/modules/tome/data/achievements/quests.lua:204` 原文为 `Completed the Master Jeweler quest with Limmir.`。
  2. 源码 `game/modules/tome/data/quests/master-jeweler.lua:20` 中该任务在玩家任务日志中的正式名称为 `name = _t"Lost Knowledge"`（遗失的知识）。译文增补了任务实际名称“遗失的知识”，属于便于玩家检索的良性语境增补。

#### entry-00435
- **位置**：`mod-tome.lua:2817`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Back and there again`
- **译文**：`归而复往`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:223`。严格符合术语快照：`Back and there again` -> `归而复往`（preferred core，返回马基·埃亚尔后再前往远东的倒装成就名；与 There and back again 区分），完全匹配。

#### entry-00436
- **位置**：`mod-tome.lua:2824`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Dispatched the Weirdling Beast and took possession of Yiilkgur, the Sher'Tul Fortress for your own usage.`
- **译文**：`击败异形触手并占据了伊克格——夏·图尔堡垒，据为己用。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:254`。符合术语库 `Sher'Tul` -> `夏·图尔`、`Yiilkgur` -> `伊克格`；`Weirdling Beast` 在全库实体名（`npcs.lua:25`）及任务日志中均统一译为“异形触手”，全句翻译准确地道。

#### entry-00437
- **位置**：`mod-tome.lua:2830`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Saved Melinda from her terrible fate in the Crypt of Kryl-Feijan.`
- **译文**：`在克里尔·费扬地宫中把梅琳达从可怕的命运中拯救出来。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:265`。严格符合术语库 `Melinda` -> `梅琳达`（existing core），地名与剧情翻译无误。

#### entry-00438
- **位置**：`mod-tome.lua:2838`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Used the Sher'Tul fortress exploratory farportal at least 7 times with the same character.`
- **译文**：`同一角色至少使用 7 次夏·图尔堡垒的探索用远行传送门。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:293`。严格符合术语快照：`exploratory farportal` -> `探索用远行传送门`（preferred core）、`Sher'Tul` -> `夏·图尔`，数量与逻辑准确。

#### entry-00439
- **位置**：`mod-tome.lua:2841`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Wibbly Wobbly Timey Wimey Stuff`
- **译文**：`摇摇晃晃、时时空空的玩意儿`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:299` 成就名称。典故出自《神秘博士》（Doctor Who）关于时间的经典台词，译文叠字对仗契合时空主题与原作成就口吻，生动准确。

#### entry-00440
- **位置**：`mod-tome.lua:2844`；section：`mod-tome/data/achievements/quests.lua`
- **原文**：`Finished the whole Abashed Expanse zone without being hit by a single void blast or manaworm. Dodging's fun!`
- **译文**：`通关整个次元浮岛，全程未被任何一次虚空冲击或法力蠕虫命中。闪避真有趣！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/achievements/quests.lua:310`。地名 `Abashed Expanse` 全库统一为“次元浮岛”；准确完整翻译了 `void blast or manaworm`（虚空冲击或法力蠕虫）及口语短句 `Dodging's fun!`（闪避真有趣！），标点对应。

---

### 复核发现汇总

1. **存在疑点（共 2 条）**：
   - **`entry-00423`**（`mod-tome.lua:2694`）：原文 `Avoid death 50 times with a life-saving talent.` 译为 `使用技能躲避50次死亡。`。漏译关键限定词 `life-saving`（免死/保命技能），且将机制误导为“躲避死亡”，建议校准为体现“免死/保命技能免除死亡”实质。
   - **`entry-00429`**（`mod-tome.lua:2788`）：原文 `Win the game without ever setting foot on Maj'Eyal.` 译为 `在没有去过旧大陆的情况下通关游戏。`。未采用术语库裁定的 `Maj'Eyal` -> `马基·埃亚尔`（preferred core），使用了通俗意译“旧大陆”。

2. **细微观察（共 3 条）**：
   - **`entry-00419`**（`mod-tome.lua:2646`）：伤害成就平行条目中，“超过1500点”与同组条目的“超过 600 点”、“超过 3000 点”存在空格排版微小差异。
   - **`entry-00428`**（`mod-tome.lua:2784`）：主线传送门系列成就中，00426/00427 采用顺承结构，00428 倒置为介词条件句，风格轻微不一致。
   - **`entry-00434`**（`mod-tome.lua:2804`）：译文增补了任务日志的正式标题“遗失的知识”，属于便于玩家理解的良性语境意译增补。

3. **未发现问题（共 35 条）**：
   - 覆盖条目：`entry-00401` 至 `entry-00418`、`entry-00420` 至 `entry-00422`、`entry-00424` 至 `entry-00427`、`entry-00430` 至 `entry-00433`、`entry-00435` 至 `entry-00440`。术语、格式占位符、控制字符及标点均核验一致。