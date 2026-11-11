# dk3 progress — Embers of Rage 场景组（0.3.12 发布版验收）

- 15:09 起：主菜单 / 新游戏 / 模组列表 / 性格创建（战役=兽人战役：余烬怒火，种族=兽人，职业=狂战士）
  reads=15/30 full=3/5 calls≈22/120
- 15:16 进入战役：开场弹窗（欢迎来到马基·埃亚尔的传说）、任务提示、克鲁克部落起始地牢
  reads=20/30 full=4/5 calls≈35/120
- 15:21 尝试 Lua 控制台导出文本：ctrl+l 需先窗口聚焦并在打开后点入输入框才接收输入；控制台每条命令约 80 字符上限，且 require("mod.class.Object") 在该环境返回 nil
  reads=21/30 full=4/5 calls≈55/120
- 15:31 控制台 game:changeLevel(1,"kaltor-shop") 触发 Game.lua:541 Lua 错误，游戏画面全黑，只能 kill -9 重启并从主菜单「读取游戏」重载存档（存读档流程）
  reads=23/30 full=4/5 calls≈70/120
- 15:42 尝试调试菜单（ctrl+a）：Esc 先打开了游戏主菜单导致 ctrl+a 无效；之后 ctrl+a 打开调试列表，但按键选择「Create Items」未生效
  reads=25/30 full=4/5 calls≈100/120
- 15:50 放弃获取作战服，收尾：grep "Lua Error" = 0；写 findings/acceptance/REPORT
  reads=25/30 full=4/5 calls≈118/120
