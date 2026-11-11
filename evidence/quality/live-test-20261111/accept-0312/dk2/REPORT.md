# dk2 实机巡检报告（场景组 dk2：核心技能与效果）

- 版本：ToME4 1.7.6 + 官方三 DLC + 汉化插件 0.3.12 公开发布版
  （`game/addons/tome-chn-mod.teaa` sha256 `22706f106ce23075f937bc0d316bb8d9737253d3f5b24f52eac6e3805f2f3fff`，与发布 hash 一致）
- 会话：2026-11-11 15:10–15:35 UTC，显示 :162，测试员 dk2
- 停止原因：**budget**（读图 30/30 达上限，其中全屏 1/5；工具调用代理计数 ≈95/120）
- 角色：自然精灵 / 软泥使（Oozemancer），等级 1，诺尔格斯巢穴；天赋与属性点由 Lua 控制台补齐（见下）

## 覆盖的界面与内容

| 项目 | 方式 | 结果 | 证据 |
| --- | --- | --- | --- |
| 新游戏 → 战役选择页 | 自然操作 | **问题 dk2-01** | `shots/151105-newgame.png` |
| 角色创建（种族/职业/战役字段） | 自然操作 | 无新问题；战役字段为中文 | `shots/151311-class-c.png` |
| 升级界面「迷幻苔藓」说明 | tooltip 实机显示 + 控制台取文本 | pass（debug-assisted） | `shots/152443-mossfull-c.png` |
| 捕熊陷阱效果 long_desc | 控制台施加效果后读插件 hook 后的函数 | pass（console，无截图） | game.log |
| 凛霜冰魂 effect subtype | `_t(…, "effect subtype")` 查表 | pass（console，无截图） | game.log |
| 打盹 DOZING 类型 | 控制台核对 type 拼写 + 查表 | not_reached（自然未到达） | game.log |
| 保存 → 退出 → 主菜单读取 → 复查 | 自然菜单流程 | pass | game.log `===AFTERLOAD===` |
| Lua 错误 | `grep -c "Lua Error"` | 0（两个会话日志均为 0） | `game.log`, `game.log.run1` |

### 关键文本（game.log 原文）

```
===MOSS=== 这种苔藓上沾满了奇怪的液体，每回合有 48% 概率使范围内的敌人混乱 2 个回合（混乱强度 40%）。
===TRAP=== 放置一个压力感应的捕熊陷阱，会捕获第一个经过的生物，造成 33.39 物理伤害，定身并减速 30%，持续 5 回合…
===EFF===  被捕熊陷阱捕获：定身, 减速 (30%), 每回合受到 10.00 物理伤害
===TAGS=== dozing.type=otber  tr=其他  rime=寄生/寒冷/死灵
===AFTERLOAD=== player 1 true table: 0x4285d038 turn=20
```

## 问题统计

- 新增问题：1（`findings.jsonl` dk2-01，untranslated，minor）
- 0.3.12 六处修复中落在本场景组的 4 项，文本层面全部为已修状态：
  - 捕熊陷阱「定身」：插件 hook 后 long_desc 已输出中文「定身」
  - 效果类型「其他」（上游 `type="otber"` 拼写错误 → `_t` 命中「其他」）
  - 效果子类型「寄生」：`寄生/寒冷/死灵`
  - 混乱苔藓说明：与 `mod-tome.lua:25197` 一致，tooltip 实机显示无截断、无颜色码泄露

### dk2-01（新问题，需主代理裁决）

新游戏 → 战役选择页整页英文（战役名 + 介绍正文），而角色创建页同一战役显示「马基·埃亚尔：卓越纪」。
源码核对：`game/modules/tome/init.lua` 的 `long_name` / `description = [[Welcome to Maj'Eyal. …]]` 是裸字符串，
未经 `_t`，模块注册时求值；插件虽有对应条目（`mod-tome.lua:42968`、`42970` 起），因为引擎从不调用 `t()`
所以不生效。属"存在译文但显示层不经过翻译"，不是文案缺失。

## 未覆盖 / 缺口（如实记录）

1. **自然战斗触发未做**：台账要求「学会后对敌人施放、在日志中看混乱效果」以及对被困敌人悬停查看「捕熊陷阱」说明。
   本会话在读图预算耗尽前只完成"学会 + 说明文本/显示"，未实际施放苔藓、未放陷阱、未让敌人踩中，
   因此**敌人状态图标悬停截图缺失**（`acceptance.jsonl` 中相关项的 `screen` 为 null）。
2. 凛霜冰魂只做了查表与 setEffect 复核，未自然施放、未取效果 tooltip 截图。
3. 打盹（Dozing）自然未到达，按要求记为 not_reached，未用控制台冒充。
4. 「活物」物品行属 dk1 场景组，本会话未测。

## 方法说明（debug / console 边界）

- 天赋学习：`game.player:learnTalent("T_HALLUCINOGENIC_MOSS"/"T_BEAR_TRAP"/"T_TRAP_MASTERY", true, 5)`（console）。
- 效果复核：`game.player:setEffect(EFF_BEAR_TRAP / EFF_RIME_WRAITH, …)`（console），读的是插件 hook 之后的
  `long_desc`，与状态图标 tooltip 渲染同一函数；**未作为自然验收**，已在 `acceptance.jsonl` 标 `method":"console"`。
- 存读档：`game:saveGame()` 写盘 → 结束进程 → 重启 → 主菜单「读取游戏」读回（菜单操作属正常流程）。

## 计数

- 读图 30/30（全屏 1/5）：`shots/` 下全部截图；含文字的裁切图未缩小。
- 工具调用代理计数 ≈95/120（模型请求下界近似，不等于 HTTP 请求数）。
- 会话未触及 120 次调用上限，因读图先到上限而收尾。
