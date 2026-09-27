# 修复窗口 41 发布记录

## 范围

来源批次 328、329、330、331、332 共 22 条确认问题（328 批 2、329 批 3、330 批 7、331 批 5、332 批 5），均为 `tome-orcs.lua`，已全部修复；无宿主补充，无跨组件同键兄弟（`check_siblings` 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Sunwall 全库译名不一登记待用户审阅第 37 项，本窗口不改。

## 预检

开窗前宿主逐句预检 6 条长条目（`publication/ADJUDICATION-HOST-PRECHECK-C0.json`，13 处追加修复点），并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`。

- execute-01 修复 22 条 → REVIEW(0) r0a1 确认 2 条（`64ff1dc48e` 系统过载“大部分”技能、`6ce8f3f6ef` 科技法师加粗句）。
- execute-02 → RE_REVIEW(1) r1a1 确认 `7b2d6ea173` 两处“克鲁克部族”→术语“克鲁克部落”。
- execute-03 → RE_REVIEW(2) r2a1 22/22 OK → FINAL(2) f2a2 确认 `6ce8f3f6ef`“装入长袍后”与“当前蒸汽值”（源码 `electricity.lua` 奥术发电机 `on_subtype=cloth`、`steam/other.lua` `getSpellpower` 用 `getSteam()`）。
- execute-04 → RE_REVIEW(3) r3a1 22/22 OK → FINAL(3) f3a2 22/22 OK，cycle 3 收敛（`max_cycles` 5）。

## 门禁

17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`399a3ae5b406b3e59aa9ff39c39dd1ef203a4369`
- 新 catalog：`c0406a5df9c4132ce21f0e9cf497aa4a4db6c99515cdf9d1241c3ec4d963a186`
- migration：`db9e58d6af47f261dc6a92abc1745ba7cc563dbfb7d29c7bb82a850215e0f3ef`

## 后续

22 个 successor 必须重新审核，不继承旧 done。待用户审阅第 32–37 项不变。

本 publication child 待宿主归档。
