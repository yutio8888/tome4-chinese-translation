# 修复窗口 42 发布记录

## 范围

来源批次 333、334、335、336、337、338 共 23 条确认问题（333 批 1、334 批 7、335 批 3、336 批 2、337 批 3、338 批 7），均为 `tome-orcs.lua`，已全部修复；无宿主补充，无跨组件同键兄弟（`check_siblings` 0）。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。Sunwall 全库译名不一仍为待用户审阅第 37 项，本窗口不改。

## 预检

开窗前宿主逐句预检 2 条长条目（`publication/ADJUDICATION-HOST-PRECHECK-C0.json`：纪律报告、修复者招募海报，6 处追加修复点），并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`。

- execute-01 修复 23 条 → REVIEW(0) r0a1 确认 `a12d4bf519` 正文“技巧射击”→本库技能名“魔术射击”；`95496f3e7a` 观星台/瞭望台、`9ebc22deed` 毒镖同族记 advisory。
- execute-02 → RE_REVIEW(1) r1a1 无一级缺陷（同两条 advisory）→ FINAL(1) f1a2 确认 `9ebc22deed` 爆矢枪每次攻击只引爆一枚（源码 `timed_effects/physical.lua` `CORROSIVE_FLECHETTE` `eff.nb-1`）及同条“镖弹/毒镖”不一。
- execute-03 → RE_REVIEW(2) r2a1 无一级缺陷（观星台 advisory；`9e927259f8`“收发无误”措辞 advisory）→ FINAL(2) f2a2 23/23 OK，cycle 2 收敛（`max_cycles` 5）。

## 门禁

17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`0feb97fecdb3bbd0713f822f0d671bbb470b937c`
- 新 catalog：`cd1afc43cdabae9f40521720398d0e814a5125adcc1919f763af383d05456086`
- migration：`9a9f81fd0fade576f78e109a5053b76d9cb7a36ce00c1da84fc9db7b695cea9a`

## 后续

23 个 successor 必须重新审核，不继承旧 done。待用户审阅第 32–37 项不变。

本 publication child 待宿主归档。
