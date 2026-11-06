# 第七轮实机测试裁决（2026-11-06）

测试员 r7-opus（Opus 5.5，agent 4c0e0567）：余烬怒火战役，兽人链锯屠夫 Opus7，10 级，克鲁克部落→隧道→雪人洞穴（击败族长）→蒸汽商场；约 60 个界面；中途因 Claude 额度中断一次，宿主唤醒后继续。7 条发现，均为 minor。

- r7-opus-02 confirmed（用户 2026-11-06「同意建议」）：tinkers 各 section 共 61 个「%s 名称」模板去掉空格（「铁 火箭靴」→「铁火箭靴」）。未加「质」：基础装备译名本身不统一（铁战斧/铁盔/铁质重靴；钢、矮人钢、斯莱特、沃瑞钽从不带「质」），模板统一加「质」会出现「钢质/沃瑞钽质」与基础装备不一致。
- r7-opus-04 confirmed：tome-orcs.lua「implant on your skin.」译文去掉句号，避免外层模板「它可以用于%s。」出现「。。」（同基础游戏纹身条目做法）。
- r7-opus-05 confirmed（用户 2026-11-06「同意建议」）：配件 attach 统一为「安装」：日志「你将%s安装到%s上。」「你未能将%s安装到%s上。」、菜单「安装到物品」「从物品上拆下」「安装配件」、弹窗与提示；「装有配件时不能这么做，请先移除配件。」。物品名「附着尖刺」与恶魔种子说明未改。
- r7-opus-06 confirmed：共享键「Not now.」（谢尔图管家、骨杖、梅塔什三处）改为「以后再说。」，三处语境都通顺；三个组件文件同步。
- r7-opus-01、03、07 confirmed，延后（插件代码）：被锁职业 locked_desc 裸字符串「Once freed, twice shy.」（worlds.lua:147/170 未包 _t）；工匠商店 kruk-tinker-shop.lua:25 `store:interact(player)` 用商店实体自身 name（未经翻译，锻炉商店走 npc.name 所以正常）；开局「角色切换至 player」为改名前的运行时名字。

## 第二段（2026-11-06 08:42–10:55，agent 703811c4，同一角色 Opus7）

11 级（目标 14 级未达成），4 次死亡后冒险模式生命耗尽；泰勒西斯未击败。复核：02、05、06 及背部支撑架已生效。新增 4 条：
- r7-opus-09 confirmed：「Created tinker: %s」两处（log/saySimple）「创造配件」→「配件制造完成：%s」，与技能名「制造配件」一致。
- r7-opus-10 confirmed：manacave ground「法力山洞地面」→「魔法洞穴地面」，与对话、手札的 Mana Caves＝魔法洞穴一致。
- r7-opus-11 confirmed（用户 2026-11-06「第11点开始修复」）：steam generator 统一为「蒸汽发生器」，terminology/items.tsv 新增 preferred 行；tome-orcs 6 处改动（蒸汽发生器植入物、植入物：蒸汽发生器及其说明、灵能、熔炉、武器连接三处技能说明），其余 3 处原已是蒸汽发生器。
- r7-opus-08 confirmed，延后（插件代码）：vaporous-emporium/npcs.lua:60 男性平民 emote_random 为裸字符串，未包 _t。
