# r5fix 执行报告

修改：mod-tome.lua 共 54 条（45 条 target 修改，9 条新增）。未提交 git；工具、文档、terminology/ 及历史 evidence 未修改。

## 裁决与范围

- r5-opus-06：依规格跳过。terminology/places.tsv:16–17 为 preferred/global/entity name，规定 next level→前往下一层、previous level→前往上一层。通道名修改与其冲突，未改这两项或任何专用通道名。因此通道名引起的原有病句仍存在；待术语裁决后处理。
- r5-opus-08：用户后续明确允许分号后一个半角空格，分号前不加空格；按该裁决完成，不改 lint。首次无空格版本触发 17 条 talent-placeholder-spacing，最终版本已全部消除。
- r5-opus-13：查询全术语库，无相关 preferred；items.tsv:74–75 是 entity name 的 existing 记录。仅修改 calendar allied 月份，同名物品仍为炎华／霜华。
- r5-opus-17：按规格不执行代码钩子。
- r5-opus-05：全仓未发现其他“日记页（…）”同族手札标题。
- 同 source 同 tag 全仓字面 grep 核查见 /tmp/r5fix/source-matches.txt；运行译文范围只有 mod-tome.lua 需要修改。历史 evidence 的冻结上下文保留原貌。

## 逐条修改与代入通读

### r5-opus-09/16 · mod-tome.lua:174

- source：`#LIGHT_GREEN#%d healing #LAST##AQUAMARINE#(%d psi heal)#LAST#`；tag：`tformat`
- 旧 target："#LIGHT_GREEN#%d 治疗 #LAST##AQUAMARINE#(%d 灵能值治疗)#LAST#"
- 新 target："#LIGHT_GREEN#%d 点治疗#LAST##AQUAMARINE#（%d 点灵能值治疗）#LAST#"
- 代入通读：棕色霉菌受到88 点治疗（12 点灵能值治疗）。

### r5-opus-09/16 · mod-tome.lua:175

- source：`#LIGHT_GREEN#%d healing#LAST#`；tag：`tformat`
- 旧 target："#LIGHT_GREEN#%d 治疗#LAST#"
- 新 target："#LIGHT_GREEN#%d 点治疗#LAST#"
- 代入通读：棕色霉菌受到88 点治疗。

### r5-opus-09/16 · mod-tome.lua:501

- source：`#Target# receives %s from #Source#.`；tag：`logMessage`
- 旧 target："#Target#受到来自#Source#的%s。"
- 新 target："#Target#从#Source#获得%s。"
- 代入通读：Opus从纹身：治疗获得69 点治疗。

### r5-opus-01 · mod-tome.lua:717

- source：`%s, %s apr`；tag：`tformat`
- 旧 target："%s, %s 护甲穿透"
- 新 target："%s，%s 护甲穿透"
- 代入通读：铁质装备（12-17 伤害，2 护甲穿透）。

### r5-opus-01 · mod-tome.lua:718

- source：`%d/%d, %s, %s apr`；tag：`tformat`
- 旧 target："%d/%d, %s, %s 护甲穿透"
- 新 target："%d/%d，%s，%s 护甲穿透"
- 代入通读：铁质装备（20/20，12-17 伤害，2 护甲穿透）。

### r5-opus-01 · mod-tome.lua:721

- source：`%s, %s block`；tag：`tformat`
- 旧 target："%s, %s 格挡"
- 新 target："%s，%s 格挡"
- 代入通读：铁质装备（12-17 伤害，30 格挡）。

### r5-opus-12 · mod-tome.lua:835

- source：`Talent %s: `；tag：`tformat`
- 旧 target："技能%s: "
- 新 target："技能%s："
- 代入通读：技能精通：+0.20 自然/史莱姆。

### r5-opus-03 · mod-tome.lua:1079

- source：`#YELLOW_GREEN#There is %s here (press '<', '>' or right click to use).`；tag：`logPlayer`
- 旧 target："#YELLOW_GREEN#这里有%s(按 '<', '>' 或右键使用)。"
- 新 target："#YELLOW_GREEN#这里有%s（按“<”“>”键或右键使用）。"
- 代入通读：这里有一个通往世界地图的出口（按“<”“>”键或右键使用）。

### r5-opus-10 · mod-tome.lua:1765

- source：`#GOLD#Dexterity#LAST#
Dexterity defines your character's ability to be agile and alert. It increases Accuracy, Defense, chance to shrug off critical hits and your damage with light weapons.
`；tag：`_t`
- 旧 target："#GOLD#敏捷#LAST#\n敏捷属性影响你的灵巧和警觉能力，提升敏捷可以提升命中，提升闪避，提升摆脱暴击伤害的几率，提升使用轻武器造成的伤害。\n"
- 新 target："#GOLD#敏捷#LAST#\n敏捷属性体现你身手灵活、反应警觉的能力，提升敏捷可以提升命中，提升闪避，提升摆脱暴击伤害的几率，提升使用轻武器造成的伤害。\n"
- 代入通读：敏捷
敏捷属性体现你身手灵活、反应警觉的能力，提升敏捷可以提升命中，提升闪避，提升摆脱暴击伤害的几率，提升使用轻武器造成的伤害。


### r5-opus-13 · mod-tome.lua:3894

- source：`Wintertide`；tag：`calendar allied`
- 旧 target："霜华"
- 新 target："霜华月"
- 代入通读：今天是马基·埃亚尔卓越纪122年，霜华月第2天。

### r5-opus-13 · mod-tome.lua:3900

- source：`Summertide`；tag：`calendar allied`
- 旧 target："炎华"
- 新 target："炎华月"
- 代入通读：今天是马基·埃亚尔卓越纪122年，炎华月第2天。

### r5-opus-21 · mod-tome.lua:11063

- source：`bear paw`；tag：`entity name`
- 旧 target："熊爪"
- 新 target："熊掌"
- 代入通读：材料：熊掌。这只熊掌又大又多毛，长着能撕裂血肉的利爪，闻起来略带鱼腥味。

### r5-opus-04 · mod-tome.lua:11456

- source：`letter to %s (%d)`；tag：`tformat`
- 旧 target："给%s的信 (%d)"
- 新 target："写给%s的信 (%d)"
- 代入通读：发现物品：写给罗尔夫的信 (1)。

### r5-opus-21 · mod-tome.lua:13590

- source：`bear paw`；tag：`ingredient name`
- 旧 target："熊爪"
- 新 target："熊掌"
- 代入通读：材料：熊掌。这只熊掌又大又多毛，长着能撕裂血肉的利爪，闻起来略带鱼腥味。

### r5-opus-21 · mod-tome.lua:13659

- source：`bear paw`；tag：`entity name`
- 旧 target："熊爪"
- 新 target："熊掌"
- 代入通读：材料：熊掌。这只熊掌又大又多毛，长着能撕裂血肉的利爪，闻起来略带鱼腥味。

### r5-opus-05 · mod-tome.lua:16662

- source：`journal page (kor'pul)`；tag：`_t`
- 旧 target："日记页（卡·普尔）"
- 新 target："日记书页（卡·普尔）"
- 代入通读：发现手札：日记书页（卡·普尔）。

### r5-opus-02 · mod-tome.lua:19716

- source：`tattered paper scrap (trollmire)`；tag：`_t`
- 旧 target："残破的纸片（巨魔沼泽）"
- 新 target："破烂的碎纸片（巨魔沼泽）"
- 代入通读：发现手札：破烂的碎纸片（巨魔沼泽）。

### r5-opus-07 · mod-tome.lua:20226

- source：`Escort: %s (level %s)`；tag：`tformat`
- 旧 target："护送：%s (%s)"
- 新 target："护送：%s（%s）"
- 代入通读：任务：护送：迷路的太阳骑士（卡·普尔废墟的第2层）。

### r5-opus-15 · mod-tome.lua:24538

- source：`#Target# blocks #Source#!`；tag：`logCombat`
- 旧 target："#Target# 挡住了 #Source#！"
- 新 target："#Target#挡住了#Source#！"
- 代入通读：Opus挡住了被诅咒者本·克鲁塞达尔！

### r5-opus-08 · mod-tome.lua:25913

- source：`heal %d; %d cd`；tag：`tformat`
- 旧 target："治疗 %d; 冷却 %d"
- 新 target："治疗 %d； 冷却 %d"
- 代入通读：纹身／符文（治疗 18； 冷却 3）。

### r5-opus-08 · mod-tome.lua:25916

- source：`heal %d; cd %d`；tag：`tformat`
- 旧 target："治疗 %d; 冷却 %d"
- 新 target："治疗 %d； 冷却 %d"
- 代入通读：纹身／符文（治疗 18； 冷却 3）。

### r5-opus-08 · mod-tome.lua:25923

- source：`res %d%%; %s; dur %d; cd %d`；tag：`tformat`
- 旧 target："减伤 %d%%; 解除 %s; 持续 %d; 冷却 %d"
- 新 target："减伤 %d%%； 解除 %s； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（减伤 18%； 解除 精神； 持续 14； 冷却 20）。

### r5-opus-08 · mod-tome.lua:25926

- source：`affinity %d%%; reduction %d; dur %d; cd %d`；tag：`tformat`
- 旧 target："伤害亲和 %d%%; 减少 %d; 持续 %d; 冷却 %d"
- 新 target："伤害亲和 %d%%； 减少 %d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（伤害亲和 18%； 减少 3； 持续 14； 冷却 20）。

### r5-opus-08 · mod-tome.lua:25935

- source：`speed %d%%; cd %d`；tag：`tformat`
- 旧 target："%d%% 加速 ; %d 冷却"
- 新 target："加速 %d%%； 冷却 %d"
- 代入通读：纹身／符文（加速 18%； 冷却 3）。

### r5-opus-08 · mod-tome.lua:25945

- source：`die at -%d; dur %d; cd %d`；tag：`tformat`
- 旧 target："-%d 死亡底线; 持续 %d; 冷却 %d"
- 新 target："死亡底线 -%d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（死亡底线 -18； 持续 3； 冷却 14）。

### r5-opus-08 · mod-tome.lua:25950

- source：`rad %d; dur %d;`；tag：`tformat`
- 旧 target："范围 %d 持续 %d"
- 新 target："范围 %d； 持续 %d"
- 代入通读：纹身／符文（范围 18； 持续 3）。

### r5-opus-08 · mod-tome.lua:25953

- source：`range %d; cd %d`；tag：`tformat`
- 旧 target："范围 %d; 冷却 %d"
- 新 target："范围 %d； 冷却 %d"
- 代入通读：纹身／符文（范围 18； 冷却 3）。

### r5-opus-08 · mod-tome.lua:25956

- source：`absorb %d; dur %d; cd %d`；tag：`tformat`
- 旧 target："吸收 %d; 持续 %d; 冷却 %d"
- 新 target："吸收 %d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（吸收 18； 持续 3； 冷却 14）。

### r5-opus-08 · mod-tome.lua:25959

- source：`absorb and reflect %d; dur %d; cd %d`；tag：`tformat`
- 旧 target："吸收并反弹 %d 持续 %d ; 冷却 %d"
- 新 target："吸收并反弹 %d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（吸收并反弹 18； 持续 3； 冷却 14）。

### r5-opus-08 · mod-tome.lua:25966

- source：`damage %d; dur %d; cd %d`；tag：`tformat`
- 旧 target："伤害 %d; 持续 %d; 冷却 %d"
- 新 target："伤害 %d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（伤害 18； 持续 3； 冷却 14）。

### r5-opus-08 · mod-tome.lua:25979

- source：`regen %d%% over %d turns; mana %d; cd %d`；tag：`tformat`
- 旧 target："法力回复 +%d%%， 持续 %d 回合；瞬回 %d 法力；冷却 %d"
- 新 target："法力回复 %d%%； 持续 %d； 瞬回法力 %d； 冷却 %d"
- 代入通读：纹身／符文（法力回复 18%； 持续 3； 瞬回法力 14； 冷却 20）。

### r5-opus-08 · mod-tome.lua:25994

- source：`range %d; phase %d; cd %d`；tag：`tformat`
- 旧 target："范围 %d; 相位 %d; 冷却 %d"
- 新 target："范围 %d； 相位 %d； 冷却 %d"
- 代入通读：纹身／符文（范围 18； 相位 3； 冷却 14）。

### r5-opus-08 · mod-tome.lua:25999

- source：`power %d; resist %d%%; move %d%%; dur %d; cd %d`；tag：`tformat`
- 旧 target："强度 %d; 抗性 %d%%; 移动 %d%%; 持续 %d; 冷却 %d"
- 新 target："强度 %d； 抗性 %d%%； 移动 %d%%； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（强度 18； 抗性 3%； 移动 14%； 持续 20； 冷却 8）。

### r5-opus-08 · mod-tome.lua:26004

- source：`threshold %d; blocks %d; dur %d; cd %d`；tag：`tformat`
- 旧 target："阈值 %d; 次数 %d; 持续 %d; 冷却 %d"
- 新 target："阈值 %d； 次数 %d； 持续 %d； 冷却 %d"
- 代入通读：纹身／符文（阈值 18； 次数 3； 持续 14； 冷却 20）。

### r5-opus-08 · mod-tome.lua:26007

- source：`%d turns; %s`；tag：`tformat`
- 旧 target："%d 回合；%s"
- 新 target："持续 %d； %s"
- 代入通读：纹身／符文（持续 18； 火焰、寒冷各 1 次）。

### r5-opus-08 · mod-tome.lua:26018

- source：`dur %d; cd %d`；tag：`tformat`
- 旧 target："持续 %d; 冷却 %d"
- 新 target："持续 %d； 冷却 %d"
- 代入通读：纹身／符文（持续 18； 冷却 3）。

### r5-opus-08 · mod-tome.lua:26025

- source：`absorb %d; cd %d`；tag：`tformat`
- 旧 target："吸收 %d; 冷却 %d"
- 新 target："吸收 %d； 冷却 %d"
- 代入通读：纹身／符文（吸收 18； 冷却 3）。

### r5-opus-20 · mod-tome.lua:26744

- source：`Melee retaliation`；tag：`talent name`
- 旧 target："近战报复"
- 新 target："近战反伤"
- 代入通读：近战反伤击中Opus造成9 寒冷伤害。

### r5-opus-11 · mod-tome.lua:29788

- source：`A #LIGHT_BLUE#wave of icy water#LAST# erupts from the ground!`；tag：`logSeen`
- 旧 target："一股 #LIGHT_BLUE#冰冷的水流#LAST# 从地面上涌现！"
- 新 target："一股#LIGHT_BLUE#冰冷的水流#LAST#从地面涌出！"
- 代入通读：一股冰冷的水流从地面涌出！

### r5-opus-19 · mod-tome.lua:42056

- source：`#LIGHT_GREEN#New#LAST# Quest!`；tag：`_t`
- 旧 target："#LIGHT_GREEN#新#LAST# 任务！"
- 新 target："#LIGHT_GREEN#新#LAST#任务！"
- 代入通读：新任务！

### r5-opus-19 · mod-tome.lua:42057

- source：`Quest #AQUAMARINE#Updated!`；tag：`_t`
- 旧 target："任务 #AQUAMARINE#更新了！"
- 新 target："任务#AQUAMARINE#更新了！"
- 代入通读：任务更新了！

### r5-opus-19 · mod-tome.lua:42058

- source：`Quest #LIGHT_GREEN#Completed!`；tag：`_t`
- 旧 target："任务 #LIGHT_GREEN#已完成！"
- 新 target："任务#LIGHT_GREEN#已完成！"
- 代入通读：任务已完成！

### r5-opus-19 · mod-tome.lua:42059

- source：`Quest #LIGHT_GREEN#Done!`；tag：`_t`
- 旧 target："任务 #LIGHT_GREEN#完成！"
- 新 target："任务#LIGHT_GREEN#完成！"
- 代入通读：任务完成！

### r5-opus-19 · mod-tome.lua:42060

- source：`Quest #CIMSON#Failed!`；tag：`_t`
- 旧 target："任务 #CIMSON#失败了！"
- 新 target："任务#CIMSON#失败了！"
- 代入通读：任务失败了！

### r5-opus-10 · mod-tome.lua:43127

- source：`Dexterity defines your character's ability to be agile and alert. It increases your chance to hit, your ability to avoid attacks, and your damage with light or ranged weapons.`；tag：`_t`
- 旧 target："敏捷属性影响你的灵巧和警觉能力，提升敏捷可以提升命中，提升闪避，提升使用轻武器和远程武器造成的伤害。"
- 新 target："敏捷属性体现你身手灵活、反应警觉的能力，提升敏捷可以提升命中，提升闪避，提升使用轻武器和远程武器造成的伤害。"
- 代入通读：敏捷属性体现你身手灵活、反应警觉的能力，提升敏捷可以提升命中，提升闪避，提升使用轻武器和远程武器造成的伤害。

### r5-opus-14 · mod-tome.lua:3211

- source：`Easy`；tag：`birth descriptor name`
- 旧 target：无（新增行）
- 新 target："简单"
- 代入通读：难度：简单 / 冒险模式。

### r5-opus-14 · mod-tome.lua:3212

- source：`Easy`；tag：`_t`
- 旧 target：无（新增行）
- 新 target："简单"
- 代入通读：难度：简单 / 冒险模式。

### r5-opus-22 · mod-tome.lua:8658

- source：`wet honey tree`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："湿漉漉的蜂蜜树"
- 代入通读：Opus击中湿漉漉的蜂蜜树造成65 物理伤害。Opus击杀了湿漉漉的蜂蜜树！

### r5-opus-22 · mod-tome.lua:8659

- source：`soaked honey tree`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："浸透的蜂蜜树"
- 代入通读：Opus击中浸透的蜂蜜树造成65 物理伤害。Opus击杀了浸透的蜂蜜树！

### r5-opus-22 · mod-tome.lua:8660

- source：`drenched honey tree`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："湿透的蜂蜜树"
- 代入通读：Opus击中湿透的蜂蜜树造成65 物理伤害。Opus击杀了湿透的蜂蜜树！

### r5-opus-22 · mod-tome.lua:8649

- source：`wet giant venus flytrap`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："湿漉漉的巨大捕蝇草"
- 代入通读：Opus击中湿漉漉的巨大捕蝇草造成65 物理伤害。Opus击杀了湿漉漉的巨大捕蝇草！

### r5-opus-22 · mod-tome.lua:8650

- source：`soaked giant venus flytrap`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："浸透的巨大捕蝇草"
- 代入通读：Opus击中浸透的巨大捕蝇草造成65 物理伤害。Opus击杀了浸透的巨大捕蝇草！

### r5-opus-22 · mod-tome.lua:8651

- source：`drenched giant venus flytrap`；tag：`entity name`
- 旧 target：无（新增行）
- 新 target："湿透的巨大捕蝇草"
- 代入通读：Opus击中湿透的巨大捕蝇草造成65 物理伤害。Opus击杀了湿透的巨大捕蝇草！

### r5-opus-23 · mod-tome.lua:12109

- source：`shield`；tag：`entity combat talented`
- 旧 target：无（新增行）
- 新 target："盾牌"
- 代入通读：副手（盾牌）：命中值 31，伤害 23，格挡值 43。

## 源码与运行时核验

以下 engine／tome 均核验 manifest 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

- Player.lua:290 将 g:getName():a_an() 传入楼梯提示；engine/utils.lua:926–930 将 _t"a "／_t"an " 加在名称前；engine.lua:1401–1402 均译为“一个”。因此模板只写“这里有%s”。实际出口代入为“这里有一个通往世界地图的出口（按“<”“>”键或右键使用）。”06 若获术语授权，可读作“这里有一个通往下一层的通道（按“<”“>”键或右键使用）。”
- data/birth/descriptors.lua:149–150：内部 name=Easy，显示名=Easier。class/Game.lua:817 使用 birth descriptor name，:833 无 tag 调用 _t(e.descriptor.difficulty)。engine/I18N.lua:43–58、64–68 表明所有标签都会更新 nil 回退，_t 默认请求 _t 标签。因此只新增 birth descriptor name 已足够覆盖目前无标签调用；显式 _t 版并非技术必需，本次按规格允许的条件同时补齐，避免依赖隐式回退。全库无其他 Easy 译文或不同用法冲突。
- data/maps/vaults/forest-ruined-building2.lua:101、112 将 wet/soaked/drenched 拼接到 honey tree、giant venus flytrap，六条 entity name 与实际结果逐字匹配，保留既有“巨大捕蝇草”原名。
- 08 的参数顺序逐一核对 data/talents/misc/inscriptions.lua short_info；18 个模板均保留项与顺序。伤害／治疗／护盾／持续值取其 short_info 调用的原参数，未新增范围、时序或触发限定。固定源码副本与调用行见 /tmp/r5fix/inscriptions-source.lua。

08 数值流锚点（按模板参数 index 从 1 开始）：

|源码行|参数值流（依 index 顺序）|
|---|---|
|84|`return ([[heal %d; %d cd]]):tformat(data.heal + data.inc_stat, data.cooldown)`|
|132|`return ([[heal %d; cd %d]]):tformat(data.heal + data.inc_stat, data.cooldown)`|
|177|`return ([[res %d%%; %s; dur %d; cd %d]]):tformat(data.power + data.inc_stat, what, data.dur, data.cooldown)`|
|199|`return ([[affinity %d%%; reduction %d; dur %d; cd %d]]):tformat(data.power + data.inc_stat*10, math.floor((data.reduce or 0) + data.inc_stat * 2), data.dur, data.cooldown )`|
|224|`return ([[speed %d%%; cd %d]]):tformat(data.speed + data.inc_stat, data.cooldown)`|
|252|`return ([[die at -%d; dur %d; cd %d]]):tformat(data.die_at + data.inc_stat * 30, data.dur, data.cooldown)`|
|289|`return ([[rad %d; dur %d;]]):tformat(self:getTalentRadius(t), data.dur)`|
|326|`return ([[range %d; cd %d]]):tformat(data.range + data.inc_stat, data.cooldown)`|
|352|`return ([[absorb %d; dur %d; cd %d]]):tformat(self:getShieldAmount(data.power + data.inc_stat), self:getShieldDuration(data.dur), data.cooldown)`|
|394|`return ([[absorb and reflect %d; dur %d; cd %d]]):tformat(self:getShieldAmount(power), self:getShieldDuration(dur), data.cd)`|
|442|`return ([[damage %d; dur %d; cd %d]]):tformat(damDesc(self, DamageType.COLD, data.power + data.inc_stat), data.dur, data.cooldown)`|
|495|`return ([[damage %d; dur %d; cd %d]]):tformat(damDesc(self, DamageType.ACID, data.power + data.inc_stat), data.dur or 3, data.cooldown)`|
|540|`return ([[regen %d%% over %d turns; mana %d; cd %d]]):tformat(data.mana + data.inc_stat, data.dur, (data.mana + data.inc_stat) / 20, data.cooldown)`|
|691|`return ([[range %d; phase %d; cd %d]]):tformat(self:getTalentRange(t), power, data.cooldown )`|
|734|`return ([[power %d; resist %d%%; move %d%%; dur %d; cd %d]]):tformat(t.getPower(self, t), t.getResistance(self, t), t.getMove(self, t), t.getDur(self, t), data.cooldown)`|
|773|`return ([[threshold %d; blocks %d; dur %d; cd %d]]):tformat(t.getThreshold(self, t), t.getBlocks(self, t), t.getDur(self, t), data.cooldown  )`|
|808|`return ([[%d turns; %s]]):tformat(t.getDur(self, t), str:lower() )`|
|917|`return ([[dur %d; cd %d]]):tformat(t.getDur(self, t), data.cooldown)`|
|979|`return ([[absorb %d; cd %d]]):tformat(self:getShieldAmount(t.getShield(self, t)), data.cooldown)`|

## r5-opus-18：shield 调查（只调查不改）

严格说库内原来没有 tag 为 nil 或 _t 的独立 `shield` 条目。“无 tag 的 shield=护盾”来自 engine/I18N.lua:set 的 nil 回退表：每次 t() 注册都会覆盖该回退值。mod-tome.lua 最后一个 shield 是 effect subtype→护盾，新增的 entity combat talented 在它之前，所以无 tag _t("shield") 仍得到“护盾”。

|文件:行|tag|target|
|---|---|---|
|mod-tome.lua:10973|entity keyword|防护|
|mod-tome.lua:12108|entity subtype|盾牌|
|mod-tome.lua:12109|entity combat talented|盾牌|
|mod-tome.lua:34891|effect subtype|护盾|
|mod-tome.lua:35993|effect subtype|护盾|
|mod-tome.lua:36365|effect subtype|护盾|
|mod-tome.lua:37544|effect subtype|护盾|
|tome-ashes-urhrok.lua:1492|effect subtype|护盾|
|tome-orcs.lua:6100|effect subtype|护盾|
|tome-orcs.lua:6532|effect subtype|护盾|

- Actor.lua:433 的盾牌速度分支，:6803–6809 以 speed_type="shield" 经 _t(speed_type) 生成技能使用速度，目前仍会显示“护盾（100%回合）”。此项按要求只调查。
- CharacterSheet.lua:896–897 的 combat.talented 使用 entity combat talented 标签，新增条目后得到“盾牌”，不再回退。
- 物品子类型通过 entity subtype 得到“盾牌”；实体关键字 shield→“防护”；效果子类型通过 effect subtype 得到“护盾”。ClassicPlayerDisplay.lua:177、Minimalist.lua:1163 使用带标签的效果子类型查询。
- 若修改现有 effect subtype 条目的 target，会把护盾效果（以及回退）一并改成盾牌，造成错误。若在末尾添加无标签 nil 条目，会改变所有缺少精确标签匹配的 shield 查询；若补 _t 条目，则影响全部无显式 context 的 _t("shield") 动态调用，而不会覆盖精确存在的 effect subtype／entity subtype。不能只凭单一速度调用作全局修改。本次未添加 nil／_t shield，也未改已有 shield 行。

## 验证

- doctor：通过；三个 DLC 按 manifest 显示 source-unpinned 警告，本次无 DLC 源码机制改动。
- 最终严格 lint：30317 translations，**0 errors，0 warnings**；命令 `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict`。
- source、source_tag、尾部 args_order／special 完整对比：原有条目未改变，45 条 target 修改、9 条新增；修改条目的格式占位符序列、颜色／markup 序列、换行数均保持。
- 全部 54 条均按以上示例代入并连同嵌入语境通读。字母与数字周围保留库内间距，中文词间不添加空格；08 分号后空格遵循用户最新裁决。
- 最终运行键扫描：0 collisions；重复键分类：1711 组均为桶 A（不同 section），桶 B／C 为 0。
- 最终严格构建：`python3 -B tools/i18n build --profile addon --component tome --require-complete` 通过；7859 runtime keys，artifact id `585a8de7fe9f9493`；产物 `.artifacts/i18n/runs/20261105T024731.969446Z-2909154-build-addon/addon/data/locales/zh_hans.lua`。
- `git diff --check`、`git diff --cached --check`：通过。
- 最终改动只有 `mod-tome.lua`，54 insertions、45 deletions；用户已有的未跟踪锁文件保留。未提交 git。
- 最终 lint JSON：`.artifacts/i18n/runs/20261105T024556.887850Z-2903942-lint/lint.json`。


## r5-opus-06 未改位置补充

- mod-tome.lua:7510 等：previous level/entity name，旧 target=新 target=“前往上一层”。
- mod-tome.lua:7511 等：next level/entity name，旧 target=新 target=“前往下一层”。
- 同键条目还在 tome-orcs.lua、tome-cults.lua、mod-example.lua、mod-example_realtime.lua；preferred 冲突使整组保持原样，无任何局部不一致修改。
- 原译文代入：“这里有一个前往下一层（按“<”“>”键或右键使用）。”病句已确认，但按本单禁止冲突 preferred 的要求未修复。
