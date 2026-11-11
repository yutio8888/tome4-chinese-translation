# dk4 实机巡检报告（Ashes of Urh'Rok / Forbidden Cults）

- 测试员 dk4，显示 :164（1600×900），GPU 渲染（TL_GPU=1）
- 插件：0.3.12 公开发布 teaa（sha256 22706f10…），游戏 1.7.6 + 三 DLC，作弊模式开启
- 角色：`playerDk4ash`（人类/高等人类 × 堕落系/毁灭使者，简单/冒险），开局区域 **乌鲁洛克之烬 灼热大厅**
- 时间：15:10–15:35 UTC 左右；结束时游戏进程已 kill -9 清理

## 结论摘要

- 新增确认缺陷：**0 条**。`findings.jsonl` 为空。
- 场景组覆盖：Ashes 开局对话、升级界面（堕落系全部已显示技能树名）、一条技能提示（鬼魂形态）、战斗/日期日志、存读档往返、Lua 错误统计。
- Cults 未覆盖：未创建 Cults 角色，控制台 changeLevel 到 `cults+town-kroshkkur` 两次未生效。
- 本轮 6 处插件修复中，属于 dk4 范围的「DLC 对话快捷回复 [离开]」与「DLC 物品 living 增伤行」均为 **not_reached**（原因见 acceptance.jsonl 与下文）。

## 覆盖的界面/内容

1. 主菜单、新游戏模组选择、角色创建（种族/职业树、名称、战役/难度/死亡模式、Play 按钮）
2. Ashes 开局剧情对话（标题与正文）
3. 升级窗口：属性/职业点/技能树解锁点/通用点，堕落系 6 组技能树 + 种族技能/高等人类
4. 技能提示：鬼魂形态（冷却/飞行速度/使用速度/类型/介绍）
5. 使用技能窗口（快捷键列、被动技能组）
6. 游戏菜单（保存游戏/主菜单等 14 项）、存读档
7. 物品栏窗口与物品名；战斗/日期 [LOG] 行；Lua 错误统计

## 未覆盖与原因

- **Forbidden Cults 全组**：未建角色；控制台 `game.player:changeLevel(1,"cults+town-kroshkkur")` 两次输入后无 Loading zone 记录（判断为控制台未接收该行，非游戏报错），时间与读图预算已到收尾阈值。
- **快捷回复「[离开]」**：DLC chats 无 quick_reply（`grep -rln quick_reply /workspace/tome4-dlcs` 无命中）；本源问题属本体 corruptor-quest 对话，已由主 agent 在候选验收中截图覆盖，本轮未独立复现。
- **物品 living 增伤/减伤行**：未获得该词条物品；DLC 对象定义无 `inc_damage_type = {living=…}`（仅本体 ego `hateful`/ammo 有），控制台生成尝试因 makeEntity 过滤器签名报错（`/loader/pre-init.lua:49: attempt to compare number with boolean`）中止，未继续消耗预算。
- **捕熊陷阱「定身」/效果类型 otber / 子类型 parasitic**：本场景组自然游玩未触发；未用 setEffect 构造（console 不能作自然验收）。
- **Embers 压力作战服**：不在 dk4 场景组。
- 未做：DLC 商店/物品悬停细查、蠕虫区域、恶魔种子、恐魔形态效果、成就面板。

## 观察（非缺陷，未计入 findings）

1. **新游戏 → 模组选择**右侧 `Tales of Maj'Eyal: Age of Ascendancy` 简介整段为英文。该界面在模组数据加载阶段显示，属既有「启动/模组菜单官方旧译」类问题（2026-11-04 disposition 标为 out-of-scope），本次不新报。官方模块 zh_hans locale 有对应译文（`t-engine4 …/locales/zh_hans.lua:42983`），但插件未在此时机接管。
2. 角色创建标题「已解锁：20/20 职业，4/4 种族技能，…」中的「种族技能」沿用 talent category 共享键（core-05 已裁决不改），非新问题。
3. 日志中 `#{bold}##PURPLE#虚空爆炸。#{normal}##LAST#` 为日志原文记录，屏内渲染正常，非缺陷。
4. 物品栏中只有「鉴定水晶球」与一条调试生成物「黄水晶」，未见开局大剑/锁甲；疑为早期一次控制台未聚焦时把长命令当按键输入（日志有 SDL keysym 警告）导致的操作副作用，未作为问题上报，也未据此下结论。

## 计数与停止原因

- 读图 **28/30**，其中全屏 **5/5**（boot、新游戏、模组加载、角色创建、进游戏各 1）
- 工具调用代理计数 **≈75/120**（模型侧可观测调用数，是 HTTP 请求数的下界近似，非强制限制）
- 停止原因：读图达到 27 张收尾阈值后继续收尾（最终 28），Cults 场景未展开；属 **budget** 停止，不是完成整组
- `progress.md` 有分阶段计数记录。

## 关键截图

- `shots/151735-gamestart.png`（升级界面）
- `shots/151810-start1-c.png`、`shots/151825-start2-c.png`（Ashes 开局对话）
- `shots/152840-tip1-c.png`（鬼魂形态提示）
- `shots/152923-menu1-c.png`（游戏菜单，保存/主菜单）
- `shots/153218-inv1-c.png`（读档后物品栏）
