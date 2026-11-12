# d6b2 debug actions
16:13:45 dbgopen (ctrl+a) demigod-menu
16:19:49 ctrl+a debug menu opened (dbgopen.sh)
16:21:54 debug menu: d = demigod toggle
16:22:05 debug menu: k = advance player (level up)
16:22:58 advance player: level field=50, checked 学习技能(最高等级), 接受
16:23:32 debug menu: a = change zone; console read-only index query
16:24:02 debug menu: Home + Down x33 (index 34/129) + Return x2 -> scourged pits
16:22:58 advance player: level field=50, checked 学习技能=最高等级, 接受 -> 等级50 confirmed (shots/162258-t9-lvl-lvl.png)
16:24:39 debug menu a = change zone; console read-only query -> IDX 34 / 129 zones
16:25:00 Home + Down x33 + Return x2 -> zone cults+scourged-pits (verified via console print + 天灾之穴(1) on screen)
16:26:56 console read-only: game.level.actors is nil in this build; enumerated actors via game.level.map(x,y,Map.ACTOR)
16:28:48 console read-only: game.level.map:getTileToScreen coords (world px, display_x/display_y = 0)
