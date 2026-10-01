# 修复窗口 62 发布记录

## 范围

- 53 条译文（mod-tome.lua 44、tome-cults.lua 5、tome-ashes-urhrok.lua 3、tome-orcs.lua 1），无术语改动。
- 用户 2026-10-01 裁决 pending #50 B：其余 50 条 killer_message 改为以凶手为主语的主动分句（“并将其…”；Wrathroot、Norgos、Tannen 三条按语义写作“并让树人们将其化为养分”“并任由群狼分食其尸”“并使其从此下落不明、杳无音讯”）。
- 用户 2026-10-01 裁决 pending #51 B：dreadfell dark Master 2 条→“黑暗领主”（`df8aa7a487`、`b662213a98`）。
- 窗口61 FINAL advisory carry_forward：Ashes 苦痛链接效果说明 `5dc5712a74`→“当目标受伤害时，另一名受害者也会承受 %d%% 的伤害。”
- 逐条改写与依据见 publication/`rewrites.json` 与 `SOURCE-CLAIMS.json`。Cults `0071abb36c` 同串为死键，未改。
- 主游戏按 manifest 固定 commit 624a673 核验；Ashes／Cults／Orcs 公开源码来源未固定。

## 复审路径

各轮裁决见 publication/ADJUDICATION-*.json；REVIEW/RE 用 GPT-6.1 Sol，FINAL 用 Opus 5.5。

- execute-01 → REVIEW(0) r0a1 2 ISSUE 均确认：苦痛链接漏译 an other（“另一名受害者”）、Murgol 的 flushed out to sea（“冲进了大海”）；
- execute-02 → RE_REVIEW(1) r1a1 53 OK → FINAL(1) f1a2 1 确认：Tannen 一条以全角逗号起头，而 PartyDeath.lua:94 以 `" "..src.killer_message` 拼接，渲染为“坦能 ，”；
- execute-03 → RE_REVIEW(2) r2a1 53 OK → FINAL(2) f2a2 53/53，cycle 2 收敛（max_cycles 5）。

门禁 17/17 全过，含严格构建；DONE_VERIFIED；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交 `1f4395f69e5d8bbe0fc328e9cb7db1da2148f022`；
- 新 catalog `8051f4edc57ac47c811ee73dc5cf1ec51044df25e2ee5db991fbf3e111b12027`；
- migration `67a73acfc5b796718ea8628dc6cdc6781f7388488e2959930023d868090404ec`。

## 后续

- 53 个 successor 必须重新审核，不继承旧 done；连同窗口61 的 22 个。
- 窗口63 积压 0 条。
- 本 publication child 待宿主归档。
