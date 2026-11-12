# d6b 调试动作记录（2026-11-12）

| 时间(UTC) | 手段 | 参数 | 结果 |
| --- | --- | --- | --- |
| 15:34 | 角色创建(UI) | 人类/高等人类 + 疯狂系/熵教徒, 简单, 冒险模式 | 成功，进入禁忌邪教战役开场（战役被职业自动切到 禁忌邪教） |
| 15:43 | ctrl+a 调试菜单 | - | 无反应（多次尝试均未打开；ctrl+l 控制台可用） |
| 15:45 | Lua 控制台 | game.player:setEffect(EFF_DEMI_GODMODE) | 半神模式生效（日志无报错） |
| 15:45 | Lua 控制台 | game.player:forceLevelup(50) | 升到 50 级，日志「欢迎来到等级 50」 |
| 15:47 | Lua 控制台 | game:changeLevel(1,"godfeaster") | 失败：zone id 需带 DLC 前缀，未切换 |
| 15:48 | Lua 控制台 | game:changeLevel(1,"cults+godfeaster") | 成功，进入 噬神者 1 层（180x50） |
| 15:49 | Lua 控制台 | makeEntity 生成 cults 怪物 | 该层 actors=0，makeEntity 全部返回 nil |
| 15:50 | - | 误将键入打到游戏（控制台已被 changeLevel 关闭） | 触发观察模式/异常实体，回合推进 |
| 15:52 | kill -9 + 重启 | 退出卡住的实例 | 存档只剩 town-kroshkkur，Godfeaster 未保存 |
| 15:56-16:00 | 主菜单/Load | 尝试读取存档 | 引擎停在菜单背景演示(dungeon + AI player)，changeLevel 报 Game.lua:541 错误 |
| 16:05-16:10 | 重新建角色(UI) + Lua | 同职业；forceLevelup(50)、半神模式、changeLevel(cults+godfeaster) | 成功进入噬神者，用 makeEntity + m.desc / m.name:t() 取怪物译文文本 |

备注：本轮**未能**按模板用 ctrl+a 调试菜单换区（该键位在本机不响应），改用 Lua 的 game:changeLevel；未使用调试菜单的「制造物品 / 玩家升级 / 切换半神模式」条目，等价操作以对应控制台调用完成并记录在此。
