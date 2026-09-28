# 修复窗口 49 发布记录

## 范围

- 第359批确认待修复 2 条：`d38555ee6a`（艾伦尼恩回忆录第一章：城堡、传说吓退的对象与“有信心”、incredulous 与增译两处、Very well、mock bow、burn foes）；`7c7be93333`（小劣魔雕像 lore 增译“同意”）。两项均为宿主补充，涉及 `mod-tome.lua`、`tome-ashes-urhrok.lua`；术语库未改；无跨组件同键兄弟（`check_siblings` 0）。
- 范围外 Archmage `8b977dd836` 未纳入，仍为 `pending_repair`。
- 主游戏按 manifest 固定 engine commit `624a673` 核验；Ashes 仅固定文件 SHA，源码仓库与 commit 未固定。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-*.json`](publication/)：

1. execute-01 修改 2 条。
2. REVIEW(0) r0a1（GPT-6 Sol）确认 2 条：小劣魔雕像“它们的酸液和我们的施法者”；尼耶拉“遗物千年无人触碰”。
3. execute-02 修复上述问题。
4. RE_REVIEW(1) r1a1 确认 2 条：Behold the humble wretchling；baldric 佩剑带。
5. 宿主随后逐句通读两条，再补 3 项同类缺陷：obstructions and shields 与人称统一；Understanding he proclaims 与 relics＝遗物；curt nod。
6. execute-03 修复上述问题。
7. RE_REVIEW(2) r2a1：2/2 通过。
8. FINAL(2) f2a2（Opus 5.5）：2/2 OK，cycle 2 收敛（`max_cycles` 5）。

## 结果

- advisory：`d38555ee6a` 中“our archmages”现译“法师团体”，archmage 措辞牵涉 Archmage 职业名裁决，本窗口不改。
- 门禁：17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。
- 译文提交：`8782cdf37f7a2b4df3e80c7e914045b409124a66`。
- 新 catalog：`1e92b9c03ee8e5d7b2ce7b769014b850c458b5b012dbcde22786434da2e661f0`。
- migration：`aec182045f0c9c3e6239285d1f3c5fa7b2ddef316ab34bff2af0bfad9a2fe851`。
- 后续：2 个 successor 必须重新审核，不继承旧 done。
- 本 publication child 待宿主归档。
