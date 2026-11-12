# o6b5 报告 — Embers of Rage 烟雾宫殿装备专项（接续 o6b4）

- 场景：读取既有存档（50 级半神兽人快枪手，烟雾宫殿 1 层，区域名裁切确认「烟雾宫殿 (1)」）。插件 v0.3.12 共享安装，未改动。
- 调试手段（详见 debug-actions.md）：仅「h) 制造物品」生成 Golden Gun / Jetpack / Medical Urgency Vest 到玩家物品栏（每次生成弹出手札，已关闭）。未用控制台、未换区、未升级。
- 证据类别：全部为 debug-ui（调试生成物品后，在真实物品栏悬停/Ctrl 比较看到）。无 natural、无 console。

## 覆盖
| 对象 | 方式 | 结果 | 截图 |
|---|---|---|---|
| 金枪 Golden Gun | 悬停 + Ctrl 比较 | ok | shots/160601-gun-l.png, shots/160638-gunc-c2.png |
| 飞行背包 Jetpack | Ctrl 比较 | issue（o6b5-01） | shots/160703-jetc-l.png |
| 医疗急救背心 Medical Urgency Vest | Ctrl 比较（对比已装备「粗制」身甲） | ok | shots/160727-vestc-l.png |
| 便携式自动材料提取仪（配件/能量） | 悬停 | issue（o6b5-02） | shots/160743-tk218-l.png |
| 洞穴炸弹（配件/炸弹） | 悬停 | ok | shots/160745-tk193-l.png |
| 铁质蒸汽枪（已装备，人偶悬停） | 悬停 | ok | shots/160807-mh-l.png |

统计：item 共 6（含 Ctrl 比较 3 次），通过 4，异常 2，未到达 0；monster/talent/effect 0（按接续说明不在本会话范围）。

核对但不报：金枪「每累计命中三次，下一次攻击的物理暴击率变为 100%」与源码（orcs world-artifacts.lua GOLDEN_GUN special_on_hit 在第三次命中后置 physcrit=100 供下一击）一致，属按实现改写；Ctrl 比较「攻击使用：2.0(-)蒸汽」中 (-) 位于数值与资源名之间是引擎 Object.lua:1187 结构，非翻译问题。game.log 中 12 处 `attempt to index local 'self'` 均为启动时 aiParseTalent 解析上游技能战术表的噪声，与文字无关。

## 问题
- o6b5-01 format/minor：「避免压力陷阱： 」全角冒号后多半角空格（mod-tome.lua:958，同组 951/953）。
- o6b5-02 inconsistent/minor：提取仪说明正文保留「APE」缩写，与同提示框「提取仪」不一致（tome-orcs.lua:1140）。

## 未覆盖
- 未看飞行背包/金枪的非 Ctrl 普通悬停单独截图（Ctrl 版已含全部行）；未看「获得技能」授予的火箭突进、医疗急救背心技能说明；未生成其他蒸汽科技词缀随机装备；未看工匠植入物。

## 预算与停止
- 读图 18 张（其中全屏/整屏缩略 2 张），图片累计 1.87 MB；工具调用代理计数 ≈52。
- 停止原因：budget（读图接近 20 张上限，按收尾线结束）。游戏进程已 kill -9。
