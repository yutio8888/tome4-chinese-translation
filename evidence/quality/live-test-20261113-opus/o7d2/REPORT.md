# o7d2 REPORT — 烟雾宫殿(1) 接续：配件附着行／首领观察／工匠技能

- 插件：公开 v0.3.12（共享安装，未改动）；模型 Opus；证据类型均为 debug-ui。
- 停止原因：**budget**（全屏额度 3/3 用尽）。1 张全屏用于物品栏首次打开时找坐标（但 key/triggerVirtual 未打开物品栏，画面仍是地图，属浪费）；另 2 张为缩小到 400×225 的整屏判断图（按 prompt 规则计入全屏额度）。按「任一项达到上限立即停止」收尾。
- 计数：reads=7/20，full=3/3，calls≈18/100，img_bytes≈1.30 MB/15。

## 覆盖
| 项 | 结果 | 证据 |
|---|---|---|
| 1. 配件附着行（锁甲悬停） | 通过：名称行显示「沃瑞钽锁甲 (5 闪避，10 护甲) <惊人的第二皮肤>」，配件的毒素/疾病/流血免疫+70%、生命回复+10.00 已并入锁甲属性；无英文残留、占位符或颜色码泄露 | shots/003754-armor-c.png |
| 1b. 已附着配件槽悬停 | 通过：「当安装到物品上时：」属性列表、说明「配件可以被安装到普通物品上，用蒸汽力量强化它！」正常 | shots/003811-tslot-c.png |
| 2. 托马克角色面板/技能 | 未到达 | — |
| 3. 工匠技能说明 | 未到达 | — |

对象：item 2 查看/2 通过/0 异常；monster 1 未到达；talent 1 未到达。问题 0 条。

## 调试手段
boot.sh、setup.sh（控制台生成 3 配件、锁甲并附着第二皮肤、放置 COUNCIL2；首次 con.sh 报 CONSOLE NOT OPEN 后重试成功，O7D2T=惊人的第二皮肤，托马克格 (12,4)，屏幕 (832,192)）。详见 debug-actions.md。

## 给接续会话的提示
- 本会话 `i` 键与 `triggerVirtual("SHOW_INVENTORY")` 都未打开物品栏；可用：`con.sh -k 'D=require("mod.dialogs.ShowEquipInven")' 'game:unregisterDialog(game.dialogs[#game.dialogs]) game:registerDialog(D.new("x",game.player))'`。
- 物品栏人偶：身体栏 (236,438)，其左配件槽 (196,430)；提示框出现在人偶右侧约 x 215–580，可用前后截图差分 bbox 自动裁切，无需全屏。
- 未覆盖：托马克面板技能页与技能说明、工匠/配件技能说明。
