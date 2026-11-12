# d6a2 progress（远东——沃尔部落）
- 16:00 UTC 启动 Xvfb :179 与游戏（TL_GPU=1），首次启动 40s 内黑屏，重启一次成功。reads=1 full=1 calls≈6 img_bytes=0.05/15
- 16:05 主菜单→新游戏→T.o.M.E→随机（y=724 处才是按钮行）→游玩。角色为亡灵/食尸鬼 死灵法师。reads=8 full=2 calls≈22 img_bytes=0.7
- 16:13 开场对话须一路选到「[攻击]」才关闭，之后 ctrl+a 可开调试菜单。pressed d。reads=20 full=3 calls≈50 img_bytes=2.4
- 16:18 切换地图到 沃尔部落(3) 成功。此后 ctrl+a 不再响应，ctrl+l 从未打开。reads=27 full=4 calls≈72 img_bytes=3.4
- 16:20 悬停自身/地面提示框，文字正常；未能悬停到怪物（怪物已不在视野内）。收尾。reads=32 full=4 calls≈95 img_bytes=4.98/15
