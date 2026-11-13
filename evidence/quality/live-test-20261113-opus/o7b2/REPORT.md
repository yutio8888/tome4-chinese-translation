# o7b2 REPORT — 天灾之穴（Scourged Pits）1 层：Cults 物品 + madness 技能

基线：公开 v0.3.12（sha256 22706f10…），官方 1.7.6 + 三 DLC；共享安装未改动。模型 Opus 5.5。
停止原因：**预算收尾线**（读图达 16 张；全屏额度 3/3 已在定位物品栏/排查界面时用尽）。范围内目标均已到达。

## 覆盖（全部 debug-ui；调试步骤见 debug-actions.md）
| 类别 | 查看 | 通过 | 异常 | 未到达 |
|---|---|---|---|---|
| 物品 | 3 件（脊笼悬停 + Ctrl 比较、利牙项环、熵之魔杖） | 2 | 1 | 0 |
| 技能 | 2 条 madness（黑暗低语、惊骇幻象） | 2 | 0 | 0 |

- 疯狂值行：黑暗低语提示框显示「疯狂值获得：8」，与源码 `insanity = 8` 一致；惊骇幻象为被动无疯狂值行。
- Ctrl 比较：脊笼比较模式显示「抗性改变：+0%(-7%)全部/+15%物理」，正常。
- 未在本会话做：madness 树后两条（Sanity Warp、Cacophony）未查看；技能界面用快捷栏悬停代替（UseTalents 对话框在全屏额度用尽后无法定位坐标）；利牙项环的 Ctrl 比较无可比对象（未装备项链），未见差异。

## 问题统计
findings 1 条（minor mistranslation）：o7b2-01 利牙项环说明 neck stump 简化为「脖子」，tome-cults.lua:767。

## advisory（非翻译问题，不计入 findings）
- 熵之魔杖说明「在 6 回合内」与实际施加 EFF_ENTROPIC_ROD 10 回合不一致：上游源码 use_power.duration=6 而 setEffect 用 10（world-artifacts.lua:1014–1034，DLC 来源未固定），译文忠实。
- 物品与技能提示标题带 `(T_DARK_WHISPERS)` 等内部 ID：作弊模式显示，非问题。

## 调试手段与工具故障
- 控制台 makeEntityByName 生成 3 件物品；第一次批量输入中 ROD_ENTROPY 行丢失（O2 打印沿用上一件），单独重试成功。
- 物品栏：triggerVirtual("SHOW_INVENTORY") 与 i 键均未打开，改用 `P:showEquipInven("Inv")`（标题因此显示 Inv，非问题）。
- 技能：控制台 learnTalentType/learnTalent（未用调试菜单 k；**dbgopen.sh 的像素校验截的是 `o7b 192` 显示而非本会话 198**，为避免读取他人显示未使用，建议主代理修正）；`P.hotkey[1]/[2]` 放入快捷栏后悬停。
- con.sh 像素校验在控制台历史较多时误判未打开；一次输入因此落到游戏按键，触发了若干回合（测试存档，未保存）。

## 计数
reads=16/20，full=3/3，calls≈71/100，img_bytes≈2.27 MB/15（逐张 stat 累加）。
