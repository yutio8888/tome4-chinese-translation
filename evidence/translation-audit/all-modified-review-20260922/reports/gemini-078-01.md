### 复核概况与文件哈希核对

- **复核批次**：batch-078
- **目标文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-078.md`
- **校验哈希（SHA-256）**：
  - 预期值：`210f0ede8bf0c58d9e4400ff79680d840161fa739d5f950cfd2bca8329708a6a`
  - 实测值：`210f0ede8bf0c58d9e4400ff79680d840161fa739d5f950cfd2bca8329708a6a`（核对一致）
- **覆盖范围**：entry-02510 至 entry-02537，共 28 条。
- **参考源码**：t-engine4 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

---

### 逐条复核报告

#### entry-02510
- **位置**：`mod-tome.lua:31939`
- **Section**：`mod-tome/data/talents/undeads/undeads.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码第 21 行 `newTalentType{ type="undead/base", name = _t("base", "talent type"), generic = true, description = _t"Undead's innate abilities." }`。英文原文 `Undead's innate abilities.` 译为 `不死族的天赋。`，其中 `Undead` 准确对应种族名术语“不死族”，句末标点一致，无格式缺陷。

#### entry-02511
- **位置**：`mod-tome.lua:31941`
- **Section**：`mod-tome/data/talents/undeads/undeads.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码第 22 行 `newTalentType{ type="undead/ghoul", name = _t("ghoul", "talent type"), generic = true, description = _t"Ghoul's innate abilities." }`。原文 `Ghoul's innate abilities.` 译为 `食尸鬼的天赋。`，专名“食尸鬼”与术语库完全对齐，标点一致。

#### entry-02512
- **位置**：`mod-tome.lua:31943`
- **Section**：`mod-tome/data/talents/undeads/undeads.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码第 23 行 `newTalentType{ type="undead/skeleton", name = _t("skeleton", "talent type"), generic = true, description = _t"Skeleton's innate abilities." }`。原文 `Skeleton's innate abilities.` 译为 `骷髅的天赋。`，种族名“骷髅”与术语库一致，句意准确，标点一致。

#### entry-02513
- **位置**：`mod-tome.lua:31945`
- **Section**：`mod-tome/data/talents/undeads/undeads.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码第 24 行 `newTalentType{ type="undead/vampire", name = _t("vampire", "talent type"), generic = true, description = _t"Vampire's innate abilities." }`。原文 `Vampire's innate abilities.` 译为 `吸血鬼的天赋。`，种族名与技能分类句意完整，标点一致。

#### entry-02514
- **位置**：`mod-tome.lua:31947`
- **Section**：`mod-tome/data/talents/undeads/undeads.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码第 25 行 `newTalentType{ type="undead/lich", name = _t("lich", "talent type"), generic = true, description = _t"Liches innate abilities." }`。原文 `Liches innate abilities.` 译为 `巫妖的天赋。`，专名“巫妖”对齐术语库，标点一致。

#### entry-02515
- **位置**：`mod-tome.lua:31954`
- **Section**：`mod-tome/data/talents.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `game/modules/tome/data/talents.lua:85` `t.name = ("#LIGHT_STEEL_BLUE#%s (Class Evolution)"):tformat(_t(t.name, "talent name"))`。译文 `#LIGHT_STEEL_BLUE#%s（职业进阶）` 完整保留占位符 `%s` 与颜色标签 `#LIGHT_STEEL_BLUE#`，英文半角圆括号转换为中文全角括号，符合规范。

#### entry-02516
- **位置**：`mod-tome.lua:31955`
- **Section**：`mod-tome/data/talents.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `game/modules/tome/data/talents.lua:89` `t.name = ("#SANDY_BROWN#%s (Race Evolution)"):tformat(_t(t.name, "talent name"))`。译文 `#SANDY_BROWN#%s（种族进阶）` 完整保留占位符 `%s` 与颜色标签 `#SANDY_BROWN#`，括号转全角，语义准确。

#### entry-02517
- **位置**：`mod-tome.lua:32010`
- **Section**：`mod-tome/data/texts/intro-chronomancer.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `intro-chronomancer.lua` 为时空系职业开局背景介绍。译文中占位符 `@name@`、颜色代码 `#LIGHT_GREEN#` 与 `#WHITE#` 完好；核心专名“现实守护者”（Keeper of Reality）、“零点圣域”（Point Zero）、“魔法大爆炸”（Spellblaze）、“马基·埃亚尔”（Maj'Eyal）及“现实至高守护者泽梅基斯”（Grand Keeper of Reality Zemekkys）全部与术语库一致；段落结构与换行完全对齐。

#### entry-02518
- **位置**：`mod-tome.lua:32033`
- **Section**：`mod-tome/data/texts/intro-cornac.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `intro-cornac.lua` 为柯纳克人类开局介绍。占位符 `@name@`、颜色码 `#LIGHT_GREEN#` 与 `#WHITE#` 保留；地名与阵营专名“联合王国”（Allied Kingdoms）、“德斯”（Derth）、“自然精灵森林”（Thaloren forest）、“巨魔沼泽”（Trollmire）、“卡·普尔废墟”（Kor'Pul）及“害虫和亡灵生物”（vermin and undead）全部对齐术语库；段落结构一致；首句句号改用感叹号属自然汉化语气润色，无阻断性问题。

#### entry-02519
- **位置**：`mod-tome.lua:32158`
- **Section**：`mod-tome/data/texts/intro-ogre.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `intro-ogre.lua` 为食人魔开局背景。专名“食人魔”（Ogre）、“埃尔瓦拉”（Elvala）、“魔法狩猎”（Spellhunt）、“永恒精灵”（Shalore）、“马基·埃亚尔”（Maj'Eyal）、“闪光洞穴”（Scintillating Caves）及“罗兰精灵”（Rhaloren）全部符合术语库；占位符与颜色码无误，段落与标点对齐。

#### entry-02520
- **位置**：`mod-tome.lua:32306`
- **Section**：`mod-tome/data/texts/intro-tutorial.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `intro-tutorial.lua`。首行原文 `#LIGHT_GREEN#Welcome to Tales of Maj'Eyal!#LAST#` 译为 `#LIGHT_GREEN#欢迎你来到 ToME 4！#LAST#`，此处将游戏全称意译为通用的简称“ToME 4”，与成就/手札中的常规译名《马基·埃亚尔的传说》不完全一致，但教程正文中多处英文原文即直接使用 ToME4，属可理解的俗称。颜色代码闭合正常，专名“孤狼”（Lone Wolf）及按键提示 `#LIGHT_BLUE#Esc 键#LAST#` 均准确。

#### entry-02521
- **位置**：`mod-tome.lua:32352`
- **Section**：`mod-tome/data/texts/message-last-hope.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `message-last-hope.lua`。占位符 `@playername@` 保留；专名“最后的希望”（Last Hope）、“高尔布格”（Golbug）、“瑞库纳”（Reknor）准确。末尾落款原文为 15 个空格缩进 `               #GOLD#-- Tolak, King of the Allied Kingdoms`，译文为 3 个制表符加 3 个空格 `\t\t\t   #GOLD#-- 托拉克，联合王国国王。` 并在末尾增加了句号。在游戏 `ShowText` 对话框中不影响显示与阅读，属细微排版差异。

#### entry-02522
- **位置**：`mod-tome.lua:32371`
- **Section**：`mod-tome/data/texts/message-last-hope.lua`
- **结论**：存在疑点
- **核验依据**：
  1. **引号配对错误**：第 32391 行中的“以便将一个”包裹”送过传送门”，前后引号字符均为右双引号（Unicode U+201D `”`），缺少前双引号（U+201C `“`）。同 section 的 entry-02521 中该处为正确的 `“包裹”`。
  2. **段落拆分不一致**：原文第四段与第五段（`While you were gone... We could not stop them...` 与 `He did not know much...`）在英文中为单换行紧跟段落；译文在第 32388 行与 32390 行之间插入了一个空行（`\n\n`），导致段落被多拆分了一次。
  3. **落款排版**：落款缩进同 entry-02521 使用了制表符且末尾带句号。

#### entry-02523
- **位置**：`mod-tome.lua:32407`
- **Section**：`mod-tome/data/texts/tutorial/done.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `tutorial/done.lua`。译文在第 312-313 行“巨魔通常不\n会这么友善！”、第 315-316 行“按键设定(你也可以\n根据你的需要改变设置)。”、第 318-319 行“游戏中还存\n在许多其他种族和职业”存在多处行内硬回车换行，在单词或词组中间（如“不\n会”、“还存\n在”）切断，在游戏 UI 渲染时可能产生过早换行。此外第 315 行包含半角左括号 `(`。颜色码 `#GOLD#...#WHITE#` 完整，语义表达无误。

#### entry-02524
- **位置**：`mod-tome.lua:32437`
- **Section**：`mod-tome/data/texts/tutorial/levelup.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `tutorial/levelup.lua`。六维属性译名“力量、敏捷、魔力、意志、灵巧和体质”完全符合术语库；各项升级点数数值逻辑（每级 3 点属性点；职业点每级 1 点、逢 5 多 1 点；通用点非 5 倍数级 1 点）翻译准确。细微观察为第 350-353 行、第 358-359 行段落内存在人工硬回车换行（“获得\n不同的”、“能获\n得3个点数”、“怪物\n来获得”），属于早期断行格式遗留，无机制阻断问题。

#### entry-02525
- **位置**：`mod-tome.lua:32506`
- **Section**：`mod-tome/data/texts/tutorial/move.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/move.lua` 为移动操作教学。键盘操作（方向键、Shift 奔跑、小键盘 5 待命、z 键自动探索）与鼠标操作条目完整，格式、缩进、颜色代码 `#GOLD#...#WHITE#` 与原列表高度吻合。

#### entry-02526
- **位置**：`mod-tome.lua:32580`
- **Section**：`mod-tome/data/texts/tutorial/quests.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/quests.lua`。目标实体“孤狼”（Lone Wolf）符合术语库，快捷键 'j' 描述准确，颜色标签 `#GOLD#Beware and fight with honour!#WHITE#` 完整保留，段落结构一致。

#### entry-02527
- **位置**：`mod-tome.lua:32677`
- **Section**：`mod-tome/data/texts/tutorial/stats/stats3.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats/stats3.lua`。三大属性标签 `#LIGHT_GREEN#Physical power: #WHITE#`、`#LIGHT_GREEN#Spellpower: #WHITE#`、`#LIGHT_GREEN#Mindpower: #WHITE#` 分别准确翻译为“物理强度：”、“法术强度：”、“精神强度：”，与术语库 snapshot 完全对齐；包括拳头（徒手）攻击的解释准确，颜色标签与换行完全一致。

#### entry-02528
- **位置**：`mod-tome.lua:32729`
- **Section**：`mod-tome/data/texts/tutorial/stats/stats5.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats/stats5.lua`。攻防属性“命中”（Accuracy）、“闪避”（Defense）、“物理豁免”（Physical save）、“法术豁免”（Spell save）、“精神豁免”（Mental save）术语全部准确；定身（pinned）、致盲（blinded）、击退（knocked flying）机制效果表述与游戏机制吻合；颜色标签与段落对应准确。

#### entry-02529
- **位置**：`mod-tome.lua:32746`
- **Section**：`mod-tome/data/texts/tutorial/stats/stats6.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats/stats6.lua`。狂战士（berserker）震慑（stun）两阶段判定机制：第一阶段命中（Accuracy）对抗闪避（Defense），第二阶段物理强度（Physical power）对抗物理豁免（Physical save），译文逻辑严密，术语与颜色标签完整。

#### entry-02530
- **位置**：`mod-tome.lua:32784`
- **Section**：`mod-tome/data/texts/tutorial/stats/stats7.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `tutorial/stats/stats7.lua`。法术“火焰冲击”（Flameshock）机制说明：伤害由“法术强度”（Spellpower）决定并受“火焰抗性”（fire resistance）影响，“震慑”（stun）作为物理状态效果由受害者“物理豁免”（Physical save）防御，施法者以“法术强度”判定成功率。机制叙述与源码逻辑完全一致。细微观察为第 541-544 行段落内存在断行换行符（如“目标\n以”、“目标的\n#LIGHT_GREEN#物理豁免#WHITE#”），不影响机制传达。

#### entry-02531
- **位置**：`mod-tome.lua:32804`
- **Section**：`mod-tome/data/texts/tutorial/stats/stats8.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats/stats8.lua`。攻击性战斗属性（命中、物理强度、法术强度、精神强度）与防御性战斗属性（闪避、物理豁免、法术豁免、精神豁免）对应列表完整；两大规律（防御按效果类别判定、职业多专注单一攻击属性）表述准确；颜色代码及编号列表完好。

#### entry-02532
- **位置**：`mod-tome.lua:33045`
- **Section**：`mod-tome/data/texts/tutorial/stats-scale/scale10.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats-scale/scale10.lua`。属性边际衰减教学：精神豁免（Mental Save）处于层级 3（tier 3，`#00FF80#`），装备提供的 +6 仅实际提升 2 点。译文数值与颜色标签全部准确，疑问语气契合。

#### entry-02533
- **位置**：`mod-tome.lua:33109`
- **Section**：`mod-tome/data/texts/tutorial/stats-scale/scale3.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `tutorial/stats-scale/scale3.lua`。战斗属性 1~100 分布与每 20 点为一个层级（tier）的定义解释准确，颜色标签 `#GOLD#` 完整。细微观察为第 625-626 行段落内存在人工硬换行（“在装备提示文字中也\n用类似的色调”）。

#### entry-02534
- **位置**：`mod-tome.lua:33121`
- **Section**：`mod-tome/data/texts/tutorial/stats-scale/scale4.lua`
- **结论**：细微观察
- **核验依据**：固定 commit 源码 `tutorial/stats-scale/scale4.lua`。层级 1 至层级 5 的数值区间（1~20, 21~40, 41~60, 61~80, 81~100）及十六进制颜色码（`#B4B4B4#`, `#FFFFFF#`, `#00FF80#`, `#0080FF#`, `#8d55ff#`）完全正确对应。细微观察为前四行在“显示为”后带有空格（如“显示为 #B4B4B4#灰色#WHITE#。”），第 654 行层级 5 处缺少空格（“显示为#8d55ff#紫色#WHITE#。”），格式轻微不一致。

#### entry-02535
- **位置**：`mod-tome.lua:33184`
- **Section**：`mod-tome/data/texts/tutorial/stats-scale/scale9.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats-scale/scale9.lua`。层级 2（tier 2，`#FFFFFF#`）下 +6 属性实际仅提升 3 点的衰减规律推导与提问，数值、颜色标签及专名“精神豁免”（Mental save）均准确。

#### entry-02536
- **位置**：`mod-tome.lua:33195`
- **Section**：`mod-tome/data/texts/tutorial/stats-tier/tier0.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats-tier/tier0.lua`。新手教程解锁机制引导，专名“启蒙符文”（Rune of Enlightenment）与技能（talent）翻译准确，语句通顺，标点一致。

#### entry-02537
- **位置**：`mod-tome.lua:33263`
- **Section**：`mod-tome/data/texts/tutorial/stats-tier/tier3.lua`
- **结论**：未发现问题
- **核验依据**：固定 commit 源码 `tutorial/stats-tier/tier3.lua`。持续状态效果（timed effects）与属性层级交互思考题，编号列表结构、问题语气与颜色标签 `#GOLD#combat stat#WHITE#` 完全对齐，翻译清晰无误。

---

### 复核总结汇总

- **覆盖条目**：28 条（entry-02510 至 entry-02537，100% 覆盖）。
- **存在疑点（需关注修复）**：
  - **entry-02522**：第 32391 行引号录入错误（`一个”包裹”` 前后均为 U+201D 右双引号，需修正前引号为 U+201C `“`）；且比原文多出一个空行将单一段落拆分。
- **细微观察（排版/非阻断格式）**：
  - **entry-02520**：游戏名称 `Tales of Maj'Eyal` 意译为常用简称 `ToME 4`。
  - **entry-02521 / entry-02522**：落款缩进使用了 `\t\t\t   ` 代替 15 个空格，末尾添加了句号。
  - **entry-02523 / entry-02524 / entry-02530 / entry-02533**：部分长段落正文内遗留硬回车断行（如“不\n会”、“还存\n在”）。
  - **entry-02534**：层级 5 的颜色标签前缺少与其他行一致的空格。
- **未发现问题**：其余 22 条译文在占位符、颜色代码、换行结构及游戏核心机制术语上均与固定源码保持高度一致。