# debug actions
15:48 ctrl+a d) 切换半神模式
15:48 ctrl+a k) 玩家升级
15:48 升级窗口：等级50，勾选学习技能，接受
15:49 ctrl+a a) 切换地图 → 第93项 烟雾宫殿 [orcs]
15:50 楼层1 接受
15:52 Lua控制台：每种怪物各取1只，u:move 到玩家附近空格（findFreeGrid 半径8）
15:55 Lua控制台：game:saveGame()
15:55 ctrl+a h) 制造物品 打开
15:56 制造物品：第116项 Golden Gun → 放入玩家物品栏
15:57 制造物品：Jetpack(136)、Medical Urgency Vest(153) → 玩家物品栏
15:58 Lua控制台：地面 Jetpack 移入物品栏（制造物品时被手札弹窗打断落地）；未制造 Medical Urgency Vest
15:59 Lua控制台：game:saveGame()（含金枪/飞行背包）
