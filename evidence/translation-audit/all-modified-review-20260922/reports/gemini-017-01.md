### 文件哈希核对

- 审查目标：`evidence/translation-audit/all-modified-review-20260922/batches/batch-017.md`
- 冻结 SHA-256：`df124d1da1f0e9bfe5f2a702ec02871df4159fafba2c6eef49f74a324d208631`
- 核验结果：**匹配一致**（`df124d1da1f0e9bfe5f2a702ec02871df4159fafba2c6eef49f74a324d208631`）
- 源码依据：根据 `source-access.json`，本批全部 40 条均归属于 `mod-tome`，通过 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/...` 读取固定 commit 公开源码进行机制与语境核验。

---

### 逐条复核报告（entry-00641 至 entry-00680）

#### entry-00641
- **条目位置**：`mod-tome.lua:6938`（`mod-tome/data/damage_types.lua`）
- **原文**：`Frozen!`
- **译文**：`冻结！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:1469` 中冰冻判定通过时的飞行浮动文字 `game.flyers:add(sx, sy, 30, ..., _t"Frozen!", {0,255,155})`，译文含义准确，感叹号标点一致。

#### entry-00642
- **条目位置**：`mod-tome.lua:6939`（`mod-tome/data/damage_types.lua`）
- **原文**：`Resist!`
- **译文**：`抵抗！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:1471` 中冰冻豁免时的飞行浮动文字 `game.flyers:add(sx, sy, 30, ..., _t"Resist!", {0,255,155})`，译文准确，标点一致。

#### entry-00643
- **条目位置**：`mod-tome.lua:6946`（`mod-tome/data/damage_types.lua`）
- **原文**：`%s is knocked back!`
- **译文**：`%s 被击退！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:1612` 中击退生效日志 `game.logSeen(target, "%s is knocked back!", target:getName():capitalize())`，占位符 `%s` 对应目标名称，空格与标点对应完整。

#### entry-00644
- **条目位置**：`mod-tome.lua:6957`（`mod-tome/data/damage_types.lua`）
- **原文**：`%s resists the frightening sight!`
- **译文**：`%s抵抗了恐惧！`
- **复核结论**：细微观察
- **核验依据**：源码 `data/damage_types.lua:1793` 中 `FEAR_KNOCKBACK` 的豁免分支。底层判定为 `target:canBe("fear")`（恐惧免疫/豁免检定）。英文表面是“frightening sight”（可怕景象），译文意译为“恐惧”，在机制上准确贴合底层恐惧豁免，无硬性缺陷。

#### entry-00645
- **条目位置**：`mod-tome.lua:6981`（`mod-tome/data/damage_types.lua`）
- **原文**：`#LIGHT_STEEL_BLUE#%s can't gain any more energy this turn! `
- **译文**：`#LIGHT_STEEL_BLUE#%s在本回合内无法得到更多能量！ `
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:2192` 中限制每回合时空能量获取次数的提示日志。颜色代码 `#LIGHT_STEEL_BLUE#`、占位符 `%s` 及英文原句末尾的尾随空格均准确保留。

#### entry-00646
- **条目位置**：`mod-tome.lua:6986`（`mod-tome/data/damage_types.lua`）
- **原文**：`item manaburn arcane`
- **译文**：`物品奥术法力燃烧`
- **复核结论**：细微观察
- **核验依据**：源码 `data/damage_types.lua:2267` 伤害类型 `ITEM_ANTIMAGIC_MANABURN` 的显示名称。同文件系列物品附魔均以“物品 + 元素/效果”命名。术语快照中 `manaburn arcane` 为 `法力燃烧`（未单独带“奥术”），本译文保留了修饰词“奥术”，与同组结构一致，但与纯术语表项略有差异。

#### entry-00647
- **条目位置**：`mod-tome.lua:7017`（`mod-tome/data/damage_types.lua`）
- **原文**：`#DARK_ORCHID#Your damage shield cannot be extended any farther and has exploded.`
- **译文**：`#DARK_ORCHID#你的伤害护盾不能再被延长，终于破碎了。`
- **复核结论**：细微观察
- **核验依据**：源码 `data/damage_types.lua:2732` 中护盾延长达 20 次上限后的销毁逻辑，底层执行 `target:removeEffect(target.EFF_DAMAGE_SHIELD)`（直接移除护盾，并无实际爆炸 AOE 判定）。英文字面为 `has exploded`，译文处理为“终于破碎了”，符合游戏实际运行结果（护盾破除），颜色代码对应无误。

#### entry-00648
- **条目位置**：`mod-tome.lua:7021`（`mod-tome/data/damage_types.lua`）
- **原文**：`hindering blight`
- **译文**：`阻碍性枯萎`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:2796` 伤害类型 `BLOOD_BOIL`，机制为枯萎伤害并附加减速（`EFF_SLOW`），译文“阻碍性枯萎”准确对应其减速控场机制。

#### entry-00649
- **条目位置**：`mod-tome.lua:7025`（`mod-tome/data/damage_types.lua`）
- **原文**：`temporal darkness`
- **译文**：`时空暗影`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:2864` 伤害类型 `VOID`，机制为各 50% 的时空伤害与暗影伤害，译文与术语库 `temporal`（时空）、`darkness`（暗影）完全一致。

#### entry-00650
- **条目位置**：`mod-tome.lua:7048`（`mod-tome/data/damage_types.lua`）
- **原文**：`draining physical`
- **译文**：`物理汲取`
- **复核结论**：存在疑点
- **核验依据**：源码 `data/damage_types.lua:3244` 伤害类型 `DEVOUR_LIFE`。相关术语快照明确规定：`draining physical`（category: `T.GAME.DAMAGE`, source_tag: `damage type`）的 preferred 规范译法为 **`生命汲取`**，其备注明确注明“从目标汲取生命造成物理伤害并治疗施法者；不写作‘物理吸收’；P0 审核确认”。当前译文为 `物理汲取`，与已裁决的术语库 preferred 译名不符。

#### entry-00651
- **条目位置**：`mod-tome.lua:7049`（`mod-tome/data/damage_types.lua`）
- **原文**：`#Source# consumes %d life from #Target#!`
- **译文**：`#Source#从#Target#身上吸取了%d生命！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:3259` 中战斗日志 `src:logCombat(target, "#Source# consumes %d life from #Target#!", heal)`，占位符 `#Source#`、`#Target#`、`%d` 及标点感叹号对应准确完整。

#### entry-00652
- **条目位置**：`mod-tome.lua:7054`（`mod-tome/data/damage_types.lua`）
- **原文**：`manaworm arcane`
- **译文**：`法力蠕虫奥术`
- **复核结论**：存在疑点
- **核验依据**：源码 `data/damage_types.lua:3315` 伤害类型 `MANAWORM`，机制为造成奥术伤害（DamageType.ARCANE）并附加法力蠕虫状态。英文为 `<效果名> <元素属性>`。译文处理为“法力蠕虫奥术”，语序机械直译导致偏正关系倒置（修饰语后置），与中文习惯修饰结构不符（对比 entry-00653 的“奥术法力燃烧”）。

#### entry-00653
- **条目位置**：`mod-tome.lua:7071`（`mod-tome/data/damage_types.lua`）
- **原文**：`manaburn arcane`
- **译文**：`奥术法力燃烧`
- **复核结论**：细微观察
- **核验依据**：源码 `data/damage_types.lua:3559` 伤害类型 `MANABURN`。术语快照记录 `manaburn arcane` 对应为 `法力燃烧`（existing）。当前译文添加了前置修饰词“奥术”，虽与机制（燃烧奥术资源）相符，但与术语库纯粹表项略有偏离。

#### entry-00654
- **条目位置**：`mod-tome.lua:7085`（`mod-tome/data/damage_types.lua`）
- **原文**：`%s resists pinning!`
- **译文**：`%s抵抗了定身！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:3840` 中念力推挤撞墙后的定身免疫判定日志 `game.logSeen(src, "%s resists pinning!", target:getName():capitalize())`，占位符 `%s`、术语 `pin`（定身）及标点感叹号均一致。

#### entry-00655
- **条目位置**：`mod-tome.lua:7102`（`mod-tome/data/damage_types.lua`）
- **原文**：`%s<smoke>#LAST#`
- **译文**：`%s<烟雾>#LAST#`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/damage_types.lua:4135` 中延迟伤害标签生成 `("%s<smoke>#LAST#"):tformat(...)`，颜色代码占位符 `%s`、尖括号标签 `<烟雾>` 与闭合标记 `#LAST#` 结构完整对应。

#### entry-00656
- **条目位置**：`mod-tome.lua:7157`（`mod-tome/data/general/encounters/fareast.lua`）
- **原文**：`Shadow Crypt`
- **译文**：`阴影地宫`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/encounters/fareast.lua:46` 实体定义 `name = "Shadow Crypt"`，实体名翻译准确无误。

#### entry-00657
- **条目位置**：`mod-tome.lua:7159`（`mod-tome/data/general/encounters/fareast.lua`）
- **原文**：`Entrance to a dark crypt`
- **译文**：`通向阴影地宫之路`
- **复核结论**：细微观察
- **核验依据**：源码 `data/general/encounters/fareast.lua:53` 地图遭遇生成入口地貌 `g.name = _t"Entrance to a dark crypt"`，其目标区域为 `change_zone="shadow-crypt"`。译文将通用的“dark crypt”特化结合区域名意译为“阴影地宫”，符合游戏具体语境。

#### entry-00658
- **条目位置**：`mod-tome.lua:7186`（`mod-tome/data/general/encounters/maj-eyal.lua`）
- **原文**：`#LIGHT_RED#You carefully open the trap door and enter the underground tunnels...`
- **译文**：`#LIGHT_RED#你小心打开地板上的活门进入了地下通道……`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/encounters/maj-eyal.lua:61` 玩家进入被困商人地道时的日志，颜色码 `#LIGHT_RED#` 与中文省略号准确对应。

#### entry-00659
- **条目位置**：`mod-tome.lua:7190`（`mod-tome/data/general/encounters/maj-eyal.lua`）
- **原文**：`Sect of Kryl-Faijan`
- **译文**：`克里尔·费扬教派`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/encounters/maj-eyal.lua:71` 遭遇实体定义 `name = "Sect of Kryl-Faijan"`，专名音译与教派实体名准确。

#### entry-00660
- **条目位置**：`mod-tome.lua:7191`（`mod-tome/data/general/encounters/maj-eyal.lua`）
- **原文**：
```text
You find an entrance to an old crypt. An aura of terrible evil emanates from this place. You feel threatened just standing there.
You hear the muffled cries of a woman coming from inside.
```
- **译文**：
```text
你发现了一个古老地宫的入口，里面笼罩着恐怖的邪恶气息，仅仅站在门口你就已经感受到了它的威胁。
你听到了里面传来了陌生女人的哭声。
```
- **复核结论**：存在疑点
- **核验依据**：源码 `data/general/encounters/maj-eyal.lua:81` 遭遇弹窗文本。原文第二句为 `You hear the muffled cries of a woman coming from inside.`，其中 "muffled"（被掩住的、低沉/沉闷微弱的）被漏译；同时译文自行添加了原文不存在的主观修饰词“陌生”（“陌生女人的哭声”）。

#### entry-00661
- **条目位置**：`mod-tome.lua:7194`（`mod-tome/data/general/encounters/maj-eyal.lua`）
- **原文**：`#LIGHT_RED#You carefully open the door and enter the underground crypt...`
- **译文**：`#LIGHT_RED#你小心翼翼地打开门，进入了地下的地宫……`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/encounters/maj-eyal.lua:86` 进入克里尔·费扬地宫时的玩家日志，颜色码 `#LIGHT_RED#` 与省略号对应完整。

#### entry-00662
- **条目位置**：`mod-tome.lua:7196`（`mod-tome/data/general/encounters/maj-eyal.lua`）
- **原文**：`Enter the crypt`
- **译文**：`进入地宫`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/encounters/maj-eyal.lua:89` 弹窗选项按钮文本，简明准确。

#### entry-00663
- **条目位置**：`mod-tome.lua:7220`（`mod-tome/data/general/events/antimagic-bush.lua`）
- **原文**：`%s (antimagic aura)`
- **译文**：`%s（反魔光环）`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/antimagic-bush.lua:44` 地形重命名逻辑 `("%s (antimagic aura)"):tformat(_t(g.name))`，占位符 `%s` 匹配原地形名，中文全角括号与术语一致。

#### entry-00664
- **条目位置**：`mod-tome.lua:7226`（`mod-tome/data/general/events/bligthed-soil.lua`）
- **原文**：`%s (blighted aura)`
- **译文**：`%s（枯萎光环）`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/bligthed-soil.lua:44` 地形重命名逻辑 `("%s (blighted aura)"):tformat(_t(g.name))`，占位符 `%s` 匹配原地形名，全角括号与术语一致。

#### entry-00665
- **条目位置**：`mod-tome.lua:7245`（`mod-tome/data/general/events/cultists.lua`）
- **原文**：`From death comes life!`
- **译文**：`死亡带来生命！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/cultists.lua:105` 邪教徒自杀献祭时的台词，标点感叹号与语义一致。

#### entry-00666
- **条目位置**：`mod-tome.lua:7279`（`mod-tome/data/general/events/fearscape-portal.lua`）
- **原文**：`#VIOLET# You escape the Fearscape!`
- **译文**：`#VIOLET# 你逃脱了恶魔空间！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/fearscape-portal.lua:36` 离开恶魔空间日志，颜色码 `#VIOLET#` 后的空格准确保留，术语 `Fearscape` 统一对应“恶魔空间”，标点感叹号一致。

#### entry-00667
- **条目位置**：`mod-tome.lua:7283`（`mod-tome/data/general/events/fearscape-portal.lua`）
- **原文**：`#VIOLET#The portal is broken!`
- **译文**：`#VIOLET#传送门被破坏了！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/fearscape-portal.lua:149` 传送门损坏日志，颜色码 `#VIOLET#` 与感叹号一致。

#### entry-00668
- **条目位置**：`mod-tome.lua:7287`（`mod-tome/data/general/events/fearscape-portal.lua`）
- **原文**：`Do you wish to enter the portal, destroy it, or ignore it (press escape)?`
- **译文**：`你想要进入传送门，摧毁它，还是无视它（按 Esc 键）？`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/fearscape-portal.lua:167` 传送门交互弹窗提问，按键提示（press escape -> 按 Esc 键）、括号与问号标点准确。

#### entry-00669
- **条目位置**：`mod-tome.lua:7289`（`mod-tome/data/general/events/fearscape-portal.lua`）
- **原文**：`#VIOLET#Ignoring the portal...`
- **译文**：`#VIOLET#你忽略了传送门……`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/fearscape-portal.lua:169` 选择忽略传送门时的日志，颜色码 `#VIOLET#` 与省略号一致。

#### entry-00670
- **条目位置**：`mod-tome.lua:7292`（`mod-tome/data/general/events/fearscape-portal.lua`）
- **原文**：`#VIOLET#A demon steps out of the %s!`
- **译文**：`#VIOLET#一个恶魔走出了%s！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/fearscape-portal.lua:203` 传送门刷新恶魔日志 `game.logSeen(m, "#VIOLET#A demon steps out of the %s!", portal.name)`，占位符 `%s` 匹配传送门名称，颜色码与标点一致。

#### entry-00671
- **条目位置**：`mod-tome.lua:7310`（`mod-tome/data/general/events/glimmerstone.lua`）
- **原文**：`%s is affected by the glimmerstone!`
- **译文**：`%s 受到了闪光石的影响！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/glimmerstone.lua:47` 闪光石眩晕影响日志 `game.logSeen(target, "%s is affected by the glimmerstone!", target:getName():capitalize())`，占位符 `%s` 匹配目标，标点感叹号一致。

#### entry-00672
- **条目位置**：`mod-tome.lua:7318`（`mod-tome/data/general/events/glowing-chest.lua`）
- **原文**：`#GOLD#An object rolls from the chest!`
- **译文**：`#GOLD#一件物品从宝箱中掉了出来！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/glowing-chest.lua:76` 打开宝箱掉落物品日志，颜色码 `#GOLD#` 与标点感叹号一致。

#### entry-00673
- **条目位置**：`mod-tome.lua:7319`（`mod-tome/data/general/events/glowing-chest.lua`）
- **原文**：`#GOLD#But the chest was guarded!`
- **译文**：`#GOLD#但是这个宝箱有怪物守护！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/glowing-chest.lua:84`，底层机制生成了敌对守卫 NPC（`chest_guards`），译文“有怪物守护”贴合实际机制与语境，颜色码 `#GOLD#` 正确。

#### entry-00674
- **条目位置**：`mod-tome.lua:7338`（`mod-tome/data/general/events/naga-portal.lua`）
- **原文**：`#VIOLET#The portal is broken!`
- **译文**：`#VIOLET#传送门被破坏了！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/naga-portal.lua:136` 娜迦珊瑚传送门被破坏时的日志，颜色码 `#VIOLET#` 与感叹号一致。

#### entry-00675
- **条目位置**：`mod-tome.lua:7342`（`mod-tome/data/general/events/naga-portal.lua`）
- **原文**：`Do you wish to enter the portal, destroy it, or ignore it (press escape)?`
- **译文**：`你想要进入传送门，摧毁它，还是无视它（按 Esc 键）？`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/naga-portal.lua:153` 交互弹窗文本，按键提示、括号与问号标点准确。

#### entry-00676
- **条目位置**：`mod-tome.lua:7344`（`mod-tome/data/general/events/naga-portal.lua`）
- **原文**：`#VIOLET#Ignoring the portal...`
- **译文**：`#VIOLET#你忽略了传送门……`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/naga-portal.lua:155` 选择忽略传送门时的日志，颜色码 `#VIOLET#` 与省略号一致。

#### entry-00677
- **条目位置**：`mod-tome.lua:7347`（`mod-tome/data/general/events/naga-portal.lua`）
- **原文**：`#VIOLET#A naga steps out of the %s!`
- **译文**：`#VIOLET#一只娜迦从%s里走出！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/naga-portal.lua:189` 刷新娜迦日志 `game.logSeen(m, "#VIOLET#A naga steps out of the %s!", portal.name)`，占位符 `%s` 匹配传送门名称，量词与感叹号标点准确。

#### entry-00678
- **条目位置**：`mod-tome.lua:7364`（`mod-tome/data/general/events/old-battle-field.lua`）
- **原文**：`ramp up to %s`
- **译文**：`通往%s的上行坡道`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/old-battle-field.lua:42` 向上楼梯地貌名称 `("ramp up to %s"):tformat(game.zone.name)`，占位符 `%s` 对应上级区域名称，作为地表坡道入口命名准确。

#### entry-00679
- **条目位置**：`mod-tome.lua:7367`（`mod-tome/data/general/events/old-battle-field.lua`）
- **原文**：`Undead are rising from the ground! You must hold on!`
- **译文**：`亡灵正从地下升起！你必须坚持住！`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/old-battle-field.lua:70` 回合倒计时事件提示文本 `game.level.turn_counter_desc`，术语 `Undead` 对应“亡灵”，两个感叹号标点与语义准确。

#### entry-00680
- **条目位置**：`mod-tome.lua:7387`（`mod-tome/data/general/events/rat-lich.lua`）
- **原文**：`#VIOLET# As you leave the crypt, the stairway collapses in upon itself.`
- **译文**：`#VIOLET# 当你离开地宫的时候，楼梯崩塌了。`
- **复核结论**：未发现问题
- **核验依据**：源码 `data/general/events/rat-lich.lua:40` 离开鼠巫妖地宫时的日志，颜色码 `#VIOLET#` 后的空格准确保留，句末句号一致。

---

### 复核总结汇总

- **总复核条数**：40 条（entry-00641 至 entry-00680）
- **未发现问题**：33 条
- **细微观察**：4 条（entry-00644、entry-00646、entry-00647、entry-00657）
- **存在疑点**：3 条
  1. **entry-00650**（`draining physical` -> `物理汲取`）：偏离术语库中已明确裁决的 preferred 规范译名 `生命汲取`（`T.GAME.DAMAGE`）。
  2. **entry-00652**（`manaworm arcane` -> `法力蠕虫奥术`）：偏正语序机械倒置，修饰语后置不符合中文构词习惯。
  3. **entry-00660**（`You hear the muffled cries of a woman coming from inside.` -> `你听到了里面传来了陌生女人的哭声。`）：漏译修饰词 `muffled`（沉闷低沉/压抑的），并增译了原文未提及的“陌生”。