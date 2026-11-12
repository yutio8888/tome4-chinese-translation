# o6b3 REPORT — Embers 后期：烟雾宫殿（Palace of Fumes）

## 停止原因：fault（预置存档不可用）
- 按接续说明执行 `TL_GPU=1 tl-start o6b3 176`，点「读取游戏」(494,117)。读取游戏窗口打开，但**角色列表为空**（全屏证据 shots/154448-full1.png），双击 (207,132) 无效果。
- 查本目录 `home/.t-engine/4.0/tome/save/`：只有 `world.teaw`、`quick_hotkeys` 和 `player/zone-orcs+town-kruk.teaz`（256,415 B，15:42）。**没有角色存档 `game.teag`，也没有烟雾宫殿的区域文件**。o6b2 目录内容相同（同为 15:42），o6b 目录没有 player。全部三个目录都找不到 `*.teag`。
- 推测（未核实）：o6b2 在日志显示「保存完毕」后不久被 kill -9，或只有离开城镇时的区域缓存写盘，角色存档没有写完整。复制到 o6b3 的就是这份不完整存档。
- 提示词要求「不要新建角色」，新建角色到场的流程正是前两次超预算的原因，所以本会话没有重建角色，直接停止，交回主代理决定（重新制作并核实存档 `save/player/game.teag` 存在，或授权本会话类测试员重建）。

## 覆盖
- 怪物、技能/效果、装备全部未到达；objects.jsonl、findings.jsonl 为空。
- 没有调试动作（debug-actions.md 为空）。没有 Lua 报错可报。

## 计数
读图 3（全屏 1），图片字节约 0.66 MB；工具调用约 13。游戏进程已 kill -9。

## 给下一会话
- 制作存档后，在派发前确认 `home/.t-engine/4.0/tome/save/player/game.teag` 存在，并且「读取游戏」列表非空。
- o6b2 REPORT 中的坐标（宫殿在切换地图列表第 93 项，升级窗口坐标等）仍可复用。
