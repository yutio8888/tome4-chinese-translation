# o7d3 REPORT — 烟雾宫殿(1) 接续：首领观察详情、工匠技能

- 基线：公开 v0.3.12（共享安装，未改动），官方 1.7.6+三 DLC；boot.sh 读档，区域裁切确认「烟雾宫殿 (1)」。模型 Opus。
- 证据分类：全部为 debug-ui（调试到场/生成后在真实界面查看）；console 仅用于定位与核对字段（M.type 等），不作显示证据。

## 覆盖
1. 议员托马克（Council Member Tormak, COUNCIL2，setup.sh 放置）角色面板：常规页、技能页（技能列表 19 项，分类/名称均中文），悬停 2 条技能：太阳风 Solar Wind（shots/tt1-solarwind-c.png）、黄昏降临 Crepuscule（shots/tt2-crep-c.png）。数值、占位符、颜色正常，与 tome-orcs.lua:3999、mod-tome.lua:28201 对应。
2. 升级窗口（key p 无响应，改用控制台 LevelupDialog.new(game.player)）：技能树列表（shots/lvl2-left-c.png）；悬停 3 条蒸汽科技技能：强壮体魄 Massive Physique（铁匠树，tt3-smith-c.png）、治疗学 Therapeutics（化学树，tt-chem-c.png + 右侧换行核对 tt-chem-r-c.png）、铁匠 Smith（物理树，tt-phys-c.png）。配方列表、「已学会」标记、长句换行均正常，无截断/溢出。

## 统计
- 对象：monster 1（ok 1）、talent 5（ok 5）、other 1（ok 1）；异常 0；未到达 0。
- findings：0。Lua Error：0（game.log）。

## 非翻译观察（不计 finding）
- 托马克常规页「类型:」「子类:」值为空。已查证为上游显示逻辑：CharacterSheet.lua:619/622（624a67329fe2）对非玩家只要存在 descriptorDisplayName 方法（Actor.lua:379 对所有 actor 定义）就取 subrace/subclass，怪物无 descriptor → 空串；实际 M.type=giant, M.subtype=steam，本库 tome-orcs.lua 已有「巨人」「蒸汽」译文。英文版同样为空，非汉化问题（shots/cs-gen-type-c.png）。
- 技能说明标题显示 T_MASSIVE_PHYSIQUE 等内部 ID，为作弊模式行为。
- 风格（未报）：Crepuscule「prioritizing the ones further away」译「优先攻击最远的敌人」，可接受。

## 调试手段
setup.sh（控制台生成配件/锁甲、放置 COUNCIL2）；控制台打开 CharacterSheet.new(M) 与 LevelupDialog；详见 debug-actions.md。

## 预算与停止
- 读图 13/20（全屏 3/3，均为缩小整屏用于找坐标：角色面板、悬停定位、升级窗口未打开判断）；工具调用≈46/100；读入图片 1.76 MB/15。
- 停止原因：done（本会话两项范围均完成）。全屏额度已用尽，故未继续扩展。

## 未覆盖
- 托马克其余技能说明（仅看 2 条）、攻击/防御/装备页未看；l 观察浮窗未看。
- 升级窗口内蒸汽科技其它树（枪支训练/快枪手/子弹掌握/闪避/飘忽身法/自动化）未悬停；工匠技能的主动型（如配件制造界面）未覆盖。
