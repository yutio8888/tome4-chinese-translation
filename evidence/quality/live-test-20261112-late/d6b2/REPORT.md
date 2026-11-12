# TESTER d6b2 — Forbidden Cults / 天灾之穴 (Scourged Pits)

## 场景组
Cults 第 2 次尝试：新建主战役角色 → 半神模式 + 调试升级 50 → 调试菜单换区到 `cults+scourged-pits`。
插件为公开发布 v0.3.12（`22706f10…`，共享安装只读，未修改 game/addons）。

## 到场过程（可复现）
1. `TL_GPU=1 tl-start d6b2 181`；主菜单「新游戏」(487,92) → 双击 T.o.M.E (200,157) → 「随机！」(360,724) → 「游玩！」(260,722)。
2. 开场教程对话（死灵法师 welcome2/welcome3）**Esc 不能关闭**，必须点对话里唯一的选项按钮（约 600,862）才能推进；共点 6 次后对话结束、进入地图。见 debug-actions.md。
3. `dbgopen.sh`（ctrl+a）首次 4 次失败（对话未结束），对话结束后 1 次成功。
4. 调试菜单 `d` = 半神模式（`[LOG] #LIGHT_BLUE#半神模式打开`）；`k` = 升级角色，等级填 50、勾选「学习技能=最高等级」、点「接受」→ 左上显示「等级50」（shots/162258-t9-lvl-lvl.png）。
5. 调试菜单 `a` = 切换地图；控制台只读查询得到 `IDX 34 / 129`，`Home` + `Down`×33 + `Return`×2 → 到达「天灾之穴 (1)」，控制台复核 `game.zone.short_name = cults+scourged-pits`。

## 覆盖情况
- 到达 天灾之穴 1 层，角色等级 50，地图内有怪物（console 枚举到 luminous horror ×3、scourge drake hatchling 十余只，另 gold pile）。
- 实际悬停读到 **1 个怪物提示框**（debug-ui）：`shots/d6b2-mon1-tooltip.png`（天谴龙幼仔）。
- 悬停提示内容：天谴龙幼仔 / 龙 / 天谴 / 分级：小怪 / 等级：39 / 生命值 672(99%) +0.27 / 抗性 100% 枯萎，23% 火焰 / 护甲强度/护甲值 30% / 5 / 体型：较小 / 命中值 42 闪避值 7 / 物理强度 45 物理豁免 31 / 法术强度 25 法术豁免 23 / 精神强度 23 精神豁免 18 / 徒手 (69) / 近战反伤 4 / 阵营：敌人（敌对，-100）。中文显示、颜色、数值、术语均正常，无截断、无残留英文、无占位符。
- 三项统计：monster 通过 1、异常 0、未到达 3（look 详情/技能列表、制造物品、效果提示）。

## 未覆盖（预算停止）
- 按 `l` 的观察详情窗口与怪物技能列表：未做。
- 调试菜单「制造物品」生成 Cults 物品、悬停与 Ctrl 比较：未做。
- 怪物施放效果提示、疯狂值相关技能/效果说明：未做。
- 另 2–4 种怪物：未做。

## 问题统计
confirmed 0 条。findings.jsonl 为空。

补充（非插件缺陷，环境事实）：本机共享安装里的 `game/addons/tome-cults.teaa` 自带 `data/locales/zh_hans.lua` 及本地化数据（同时有 ja_JP/ko_KR）。所以 Cults 怪物说明的**显示文本来自 DLC 包本身**，不一定来自 0.3.12 插件：
- 屏幕显示「一条幼龙。它本身并不强大，但是它们经常集体行动。」← 出自 `tome-cults.teaa data/locales/zh_hans.lua:612`，源串为分号版 `A drake hatchling; not too powerful by itself, but it usually comes with its brothers and sisters.`（DLC `data/general/npcs/scourge-drake.lua:49`）；
- 插件 0.3.12 的对应条目是逗号版源串，`data/locales/zh_hans.lua:4654`：「一条幼龙。它本身并不强大，但它通常与兄弟姐妹结伴出现。」
两条并存导致同义描述两种措辞。归因不在插件（未在本库找到分号版源串），DLC 来源未固定，仅记录，不计确认缺陷。做 Cults 类显示检查必须区分 DLC 包自带译文与插件译文。

## 限制与备注
- 悬停：到达后前段悬停可出提示框；随后对同一批怪物瓦片多次 mousemove（含小幅抖动）均不再出现提示框，原因未查明（未再消耗预算排查）。只有 t10 那一张提示框是有效显示证据。
- 未产生 `game.teag`：存档目录只有 `save/koridir/zone-blighted-ruins.teaz`（换区自动保存的 zone 文件），本次未执行菜单手动保存，接续会话不能依赖该存档。
- game.log 中 `aiParseTalent ... attempt to index local 'self' (a nil value)` 多处为引擎 AI 解析既有噪声（多 talents 路径），与文字无关，未计入。
- 未修改 /workspace 下任何文件（只在 /tmp 解包只读核对，未提交）。

## 预算与计数
- 读图 **20/20**（其中全屏或整图缩览 **3/3**：t3-loaded、t10-pits、t11-con 的缩览/整屏判断）。
- 图片累计文件字节 ≈ **6.1 MB** / 收尾 15 MB。
- 工具调用代理计数 ≈ **96/100**。
- 停止原因：**budget**（读图达到 20 张上限，先写盘后结束）。
- 游戏实例仍在运行（t-engine pid 2319952，Xvfb :181 pid 2319260），未 kill。
