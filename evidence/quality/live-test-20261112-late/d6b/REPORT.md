# TESTER d6b — Forbidden Cults 后期：噬神者（The Godfeaster）

插件：v0.3.12 公开发布版（sha256 22706f10…，共享安装只读，未替换 game/addons）
角色：人类/高等人类 + 疯狂系/熵教徒，简单难度、冒险模式，调试升到 50 级并开半神模式
地图：噬神者 1 层（zone `cults+godfeaster`，180x50）

## 结论摘要

**本轮没有完成显示层验收**，因此没有 `verified=true` 的问题，也没有可宣告的通过项。
读图预算 19/20 已用尽，其中 **10 张消耗在从零创建角色**（种族/职业/难度/确认按钮逐屏确认）。
最终只做到：进入噬神者、取到 6 个「腐化团块」怪物的说明文本并逐条比对英文原文。

- 显示层（字体、截断、换行、重叠、颜色码泄漏、占位符实际渲染）：**完全未覆盖**。
- 技能/天赋、效果、装备/神器、Malyu / The Divine Writhing Mass：**未覆盖**。
- 文本级：6 条怪物说明与英文原文比对，语义无误；2 条可读性/术语一致性疑点（见 findings，均 `verified:false`）。

## 覆盖统计

| 对象类别 | 查看 | 通过 | 异常 | 未到达 | 方式 |
| --- | --- | --- | --- | --- | --- |
| monster（腐化团块 6 种） | 6 | 5 | 1（d6b-01 语序） | 2（Malyu、The Divine Writhing Mass） | console 取 `desc` 文本 |
| talent（熵系：Entropic Gift / Chaos Orbs / Void Stars / Netherblast / Insanity Pool） | 0 | - | - | 5 | 仅列出 id，未取说明 |
| effect（疯狂值/熵相关） | 0 | - | - | 全部 | 未做 |
| item / artifact | 0 | - | - | 全部 | 未生成 |
| 显示验收（任意项） | 0 | - | - | 全部 | 预算耗尽 |

问题统计：2 条 minor（1 awkward、1 inconsistent），均**未经显示验收**，属待核实。

## 使用的调试手段（详见 debug-actions.md）

- UI 建角（两次）：人类/高等人类 + 疯狂系/熵教徒。
- `ctrl+a` 调试菜单**在本机不响应**（多次尝试）；`ctrl+l` Lua 控制台可用。
- 控制台等价操作：`setEffect(EFF_DEMI_GODMODE)`、`forceLevelup(50)`、`game:changeLevel(1,"cults+godfeaster")`、`game.zone:makeEntity(...)` 取怪物文本。
  - **未**使用调试菜单的换区/升级/制造物品条目，属于对模板的偏离，已在此记录。
- 换区未用 `changeLevel` 之外的入口；本次 `game:changeLevel` 本身没有崩溃，但裸 zone id 会静默失败。

## 预算与停止原因

- 读图 19/20（全屏 2/3），工具调用 ≈88/100，累计读入图片 ≈4.1MB（收尾线 15MB、停止线 20MB）。
- 停止原因：**读图张数达到上限**。剩余范围需主代理另开新会话接续。

## 未覆盖的范围（建议优先补）

1. 噬神者内的怪物 tooltip 实际显示（名称+说明+抗性/状态），尤其首领 Malyu、The Divine Writhing Mass。
2. 熵系天赋与「疯狂/熵」资源提示、效果说明（含数值、`%d`/颜色码渲染）。
3. 禁忌邪教装备/神器：生成 2–3 件后悬停 + Ctrl 比较。
4. 战斗消息日志里怪物中文名与技能名（本次实例该层 actors=0，未产生战斗）。

## 给主代理的过程问题（重要）

1. **20 张读图预算不足以支撑「从零建角 + 换后期图 + 内容检查」**：建角单程就吃掉 10 张（50%）。
   建议后期图测试预置 50 级存档（放进 `testers/_base` 或每 lane 预置），或把内容检查会话的读图预算提到 30–40，并把建角单独剥离。
2. `ctrl+a` 调试菜单本机不响应（`ctrl+l` 正常）。可在模板注明备选：控制台执行
   `game:registerDialog(require("mod.dialogs.debug.DebugMain").new())`。
3. 换区 zone id 必须带 DLC 前缀（`cults+godfeaster`）；裸 `godfeaster` 会静默失败且**先存档再失败**。
4. `game:changeLevel` 会关闭 Lua 控制台，之后键入会打进游戏本体（本次因此触发意外状态、回合空转）。建议规定：任何输入前先用 `print` 探针确认控制台焦点。
5. 本次实例中噬神者 1 层生成后 `#game.level.actors == 0`，`makeEntity` 亦全为 nil；该层怪物疑由事件/延迟生成，建议模板注明先等待或触发事件再统计怪物。
6. `kill -9` 后存档只剩 `town-kroshkkur`（噬神者层与角色状态回滚）；重启后引擎停在主菜单背景演示（AI `player`，zone=`dungeon`），此时 `changeLevel` 报 `Game.lua:541`、直接载入也无效，必须先正常读取存档。
7. 静态扫描注意：`tome-cults.lua` 里 3357/4832/4833/4834/4835/4836 等英文未译条目都在 `--[==[ … ]==]` 注释块内（标注 `-- untranslated text`），**不是线上字符串**，不要当作漏译上报；另 539/558、4388/4554 存在重复条目，属卫生问题不是玩家可见缺陷。

## 原始证据

- 截图：`shots/`（153417-first-full.png 等，均为本地全屏原图；因预算未做裁切读图，故未用于结论）。
- 文本证据：`game.log` 中的 `^E[1-8]:`、`^I[1-4]N:`、`^NN:`、`^TI:` 行。
