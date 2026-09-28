# 修复窗口 51 发布记录

## 范围

2 条宿主补充（队列耗尽、积压 1 时用户 2026-09-28 选择开窗）：`20fa052d6c`（第361批确认，成就 They Came Back For Eyal 漏 `your patron`、`portal to` 方向误译，改“开启通往你那疯狂的太阳主上的传送门”），`59339a8b7f`（窗口50漏纳入，科技法师进阶说明补回“（A.P.E.）”并去多余句号）；涉及 `mod-tome.lua`、`tome-orcs.lua`；术语库未改；无跨组件同键兄弟（`check_siblings` 0）。

不含：Archmage `8b977dd836`（pending_repair）、Sunwall 译名（待用户第 37 项）。主游戏按 manifest 固定 engine commit `624a673` 核验；Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`：execute-01 修改 2 条 → REVIEW(0) r0a1（GPT-6 Sol）2/2 OK → FINAL(0) f0a2（Opus 5.5）2/2 OK，cycle 0 收敛（max_cycles 5）。

## Advisory

相邻成就（`mod-tome.lua:2775`，以艾琳之手阻止 `your mad patron sun` 焚毁世界）同样漏 `your patron`，不在本 workset，留待后续窗口。

## 门禁

17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`c1f7bc5ef439c710db9b3e657f3ab91f14a17bb7`
- 新 catalog：`52f38b69945e3eb37146095d6f30b01e607e91fe53a8f6c75e0cb895fbc6c9fe`
- migration：`687fcef22dcc96338d3b422e84269100c17f5f45ac2c8aa51b4152e18b6b56ab`

## 后续

2 个 successor 必须重新审核，不继承旧 done。

本 publication child 待宿主归档。
