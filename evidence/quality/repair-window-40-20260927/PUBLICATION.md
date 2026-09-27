# 修复窗口 40 发布记录

## 范围

来源批次 324、325、326、327 共 21 条确认问题，加第 324 批 2 条宿主补充（`4e560f2e5a` 蒸汽采石场、`50df66a4c3` 苏克商店全名），合计 23 条 workset 已修，均位于 `tome-orcs.lua`。另因门禁 `06-runtime-collision-scan` 发现跨组件同键，将 `mod-tome.lua` 中同名商店 2 条经 runtime-sync（[`publication/RUNTIME-SYNC.json`](publication/RUNTIME-SYNC.json)、[`publication/HOST-NOTE-RUNTIME-SYNC.md`](publication/HOST-NOTE-RUNTIME-SYNC.md)）同步为已复审文本。

Orcs 仅固定文件 SHA，源码仓库与 commit 未固定；主游戏按 t-engine4 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。Gardanion 物品名需新造音译，未入窗，登记待用户审阅第 36 项。

## 预检

开窗前宿主逐句预检 6 条长条目（[`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)），确认 10 处追加修复点，并入首轮修复。

## 复审路径

各轮裁决见 [`publication/`](publication/) 下的 `ADJUDICATION-*.json`。

- execute-01 修复 23 条 → REVIEW(0) r0a1 确认 3 条（`4e560f2e5a` 全局速度、`5362d5e743` 提出协议条件、`619199a9ea` 人际相处）。
- execute-02 → RE_REVIEW(1)（r1a1 revision_key 回显错误拒收，r1a2 确认 `5d8d908f72` 残暴行径；宿主另据源码确认 `52bc32cb74` 蒸汽枪掌握／等级）→ execute-03 → RE_REVIEW(2) 收敛 → FINAL(2) f2a2 确认 `4e560f2e5a` pinaciphobia→清单恐惧症。
- execute-04 → RE_REVIEW(3) 确认 `5bb911ddb9` 蜘蛛机器人只判定一次冻结（驳回 `58c3e2bf11` 弹药措辞）→ execute-05 → RE_REVIEW(4) 收敛（再次驳回 `58c3e2bf11`）→ FINAL(4)（f4a2 截断拒收，f4a3 23/23 OK）。
- 门禁首跑 `06-runtime-collision-scan` 报 Sook 店名跨组件冲突 → execute-06 runtime-sync `mod-tome.lua` 2 条 → 重跑 17/17。

## 门禁

17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`acae1e6d74fec03894d7e50ce531625da3b215c9`
- 新 catalog：`a1da5518961a538373c3b21cdca9ee57055372a5da9b5580549e9e85b1e838c5`
- migration：`5b6b372f3fa4e03b2c7fb46ffacfa62fd1e3a1b98ee4272fa7875084ae5a6d3e`

## 后续

25 个 successor 必须重新审核，不继承旧 done。待用户审阅第 32–36 项不变（第 35 项 Awesome Toss、第 36 项 Gardanion 为本轮新增）。

本 publication child 待宿主归档。
