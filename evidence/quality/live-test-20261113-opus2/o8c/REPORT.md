# o8c 报告 — 天灾之穴（Scourged Pits）1 层：madness 树后两条技能与疯狂值

- 基线：公开 v0.3.12（共享安装，只读未改）＋官方 1.7.6/三 DLC；存档 50 级半身人炼金术士 Astajed；模型 Opus。
- 到场：boot.sh 读档，区域裁切确认「天灾之穴 (1)」；setup.sh 学会 demented/madness、疯狂槽及四技能各 3 级（S8T true true 0 100）。全部为 debug 来源，见 debug-actions.md。

## 覆盖（均为 debug-ui）
| 对象 | 界面 | 结果 |
|---|---|---|
| 失智冲击 Sanity Warp | 升级窗口悬停 | ok：被动；伤害 %0.2f 暗影伤害、半径 %d 与源码 madness.lua:164–176 一致（{2,1} 重排正确，半径 1,1,1,2,2 / 伤害逐级值） |
| 心灵尖啸 Cacophony | 升级窗口悬停 | ok：疯狂值消耗 10（源码 insanity=-10，Cults superload Actor.lua:alterTalentCost 取反＝消耗 10，显示正确）；冷却 15、半径 10、持续 3–5、额外时空伤害 59–121%、「失智冲击」名称前后一致 |
| 心灵尖啸 | 快捷栏槽 1 悬停（hotkey[1]=T_CACOPHONY） | ok：简版提示与升级窗口一致，等级 3 实际值持续 4 回合、95% |
| 火焰充能 Fire Infusion | 快捷栏槽 2 悬停（误触，顺带） | ok |
| 疯狂值资源栏 | P.insanity=60 后左上资源栏 | ok：「60% (18% 混沌度)」无截断 |
| 疯狂值资源栏悬停提示 | 资源栏悬停 | ok：「幅度最多为 混沌度%」照英文 "up to chaotic%" 直译，前轮 o7b 已判与资源栏用词一致不报，本轮不重复 |

统计：talent 4 条查看（4 通过）、other 2（2 通过），异常 0，未到达 0。

## 问题
无新问题（findings.jsonl 为空）。Lua：game.log 12 条均为加载期 aiParseTalent 上游 tactical 解析噪声（projection.lua/hymns.lua 等 self nil），与文本无关；插件相关 LuaError 0。

## 未覆盖
- 技能说明中随疯狂值数值变化的部分：Sanity Warp/Cacophony 说明本身不依赖当前疯狂值，未见可变部分；未实际施放技能（不攻击，避免触发首领）。
- 疯狂槽（Insanity Pool）技能说明未单独悬停。

## 计数与停止
- 读图 10 张（全屏 1：升级窗口布局定位），累计图片 1.69 MB；工具调用≈37/100。
- 停止原因：done（范围完成）。游戏进程已 kill -9；Xvfb :203 未动，留主代理回收。
