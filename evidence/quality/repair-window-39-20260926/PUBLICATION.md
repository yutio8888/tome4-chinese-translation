# 修复窗口 39 证据发布

## 范围

来源批次 320、321、322、323 共 25 条确认问题加 2 条宿主补充（HOST-SUPPLEMENT-CLAIMS），合计 27 条 workset 已修（均为 tome-orcs.lua）。另按用户 2026-09-26 裁决把 steamsaw 在 `terminology/items.tsv` 升为 preferred「蒸汽链锯」，并将 tome-orcs.lua 其余 15 条「蒸汽锯」经 terminology-sync（RUNTIME-SYNC.json）统一。Orcs 仅固定文件 SHA，源码仓库与 commit 未固定。

## 预检

开窗前宿主逐句预检 7 条长条目（ADJUDICATION-HOST-PRECHECK-C0），并入首轮修复。

## 复审路径

各轮裁决见 `publication/ADJUDICATION-*.json`。

- execute-01 修复 27 条 → REVIEW(0) r0a1 确认 4 条（38df4d785d 武器全称“裂天者 毁灭号”、3f615510ad 采石场笔记、4a4f53d70c 仁慈结局、4cad070d1e 游戏志愿者局请愿）。
- execute-02 → RE_REVIEW(1) 确认 2 条（431cacf5c7 地热公告副标题、4cad070d1e 背书句）→ execute-03 → RE_REVIEW(2) 确认 43d64e16d1 五彩爆炸 → execute-04 → RE_REVIEW(3) 确认 3fbaffc6c4 沃瑞钽、431cacf5c7 蒸汽采石场 → execute-05 → RE_REVIEW(4) 确认 3f615510ad、431cacf5c7 → execute-06 → RE_REVIEW(5) 收敛 → FINAL(5) f5a2 确认 393ceabce5（“我同情他”）、3bb826649c（创造之魔法、正统主宰）。
- 用户授权 max_cycles 5→6：execute-07 → RE_REVIEW(6)（r6a1 非紧凑 JSON 拒收，r6a2 收敛）→ FINAL(6)（f6a3 截断拒收，f6a4 报 43cbe69c78 steamsaw 译名不一致）。
- 用户裁决统一 steamsaw 并授权 6→8：execute-08（术语行 + 43cbe69c78 + 15 条 sync）→ RE_REVIEW(7) 确认 43d64e16d1 genocide→种族灭绝（驳回 tinker 术语、手炮沃瑞钽两条旧质疑）→ execute-09 → RE_REVIEW(8) 收敛 → FINAL(8) f8a2 确认 4a4f53d70c “wonder aloud”（另并入麦芽酒、数千年来）。
- 用户授权 8→11：execute-10 → RE_REVIEW(9) 收敛 → FINAL(9) f9a2 27/27 OK。
- advisory 未改：38e3195b27“全军戒备”、4cad070d1e“科幻”、上一名目标／瞄准画面措辞。

## 记录

各轮 stage 记录未在复审后即时发布，FINAL 通过后宿主一次性补发 14 条（校验与理由见 `publication/HOST-NOTE-LATE-PUBLICATION.md`）。

## 门禁

17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

译文提交 `e19736293f1f9854175520be0f6d2dd04c5504d2`；新 catalog `7158f4b0958a74fb8acc01f732dc0f97a4ac6fad159f6cf1051687db04cc12f0`；migration `734a72ac2bf19c1561b029234f3214bab995d355f497e3cd6467cd5742a3b218`。

## 后续

42 个 successor 必须重新审核，不继承旧 done。窗口外遗留：`4e560f2e5a`（emporium 公告仍作“蒸汽矿场”，应为“蒸汽采石场”）。待用户审阅第32–34项（Thunder Grenade、Voltaic Bolt、Supercharge Bullets）不变。

本 publication child 待宿主归档。
