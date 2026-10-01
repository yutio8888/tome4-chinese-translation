# 修复窗口 61 发布记录

## 范围

- 共 22 条译文：`mod-tome.lua` 17 条、`tome-ashes-urhrok.lua` 2 条、`tome-cults.lua` 3 条；无术语改动。
- 第377–379批确认 9 条：`8efa510a7a`、`a2147f96a9`、`b19b6b1d34`、`bc2f66a5e1`、`de48fb09ea`、`56b7b501eb`、`b028c0ed3b`、`074d7c0b7e`、`fc1ebcae01`。
- 第377批宿主补充 1 条：`9987aef53c` Blindside＝闪电突袭。
- 2026-10-01 死亡信息表系统性分析 12 条，见 [`pending-user-review.md`](../pending-user-review.md) 同日一节，用户同意排入本窗口。
  - 死亡公告四个句式 `ab25e27abc`、`abf9674633`、`49f7781bff`、`7cba41f15f`：经 `args_order` 改为“在{区域}第{N}层…而死，杀死他（她）的是…”，特殊句式改为“在{区域}第{N}层{消息}”。
  - 拼接短语 8 条：`4ddf91a568`、`d798b563aa`、`7f5e27e174`、`ef3eefd58d`、`5fa2c1c3c1`、`17a76d1b3e`、`efaf9b0f43`、`0aba4d5ba2`。
- 其中 `17a76d1b3e`、`5fa2c1c3c1`、`ef3eefd58d` 按用户 2026-10-01 对 pending #50 的裁决（B：killer_message 以凶手为主语）改为主动句。
- 主游戏按 manifest 固定 commit `624a673` 核验；Ashes／Cults 公开源码来源未固定。无同键兄弟。

## 复审路径

各轮裁决见 [`publication/ADJUDICATION-*.json`](publication/)；REVIEW／RE_REVIEW 用 GPT-6.1 Sol，FINAL 用 Opus 5.5。

- execute-01 → REVIEW(0) r0a1 4 ISSUE：2 条 killer_message 主语颠倒、意志之力“魔法”→“魔力”、末日加速“相位外”→“脱离现实”；宿主另把同族 `5fa2c1c3c1` 并入。
- execute-02 → RE_REVIEW(1) r1a1 22 OK → FINAL(1) f1a2 1 确认（苦痛链接 victim 与选择提示“受害者”不一致）。
- execute-03 → RE_REVIEW(2) r2a1 OK → FINAL(2) f2a2 2 确认（异变之手“心灵护盾”→“灵能力场”；The Amalgamation 吸收进自身）。
- execute-04 → RE_REVIEW(3) r3a1 OK → FINAL(3) f3a2 1 确认（异变之手属性行与副手非空禁用说明拼接）。
- execute-05 → RE_REVIEW(4) r4a1 OK → FINAL(4) f4a2 22/22，cycle 4 收敛（max_cycles 5）。

门禁 17/17 全过，含严格构建；`DONE_VERIFIED`；全部 reviewer 与 executor 已归档。

## 标识

- 译文提交：`276e8b2df82095585a353d98717d1715f7ef33df`。
- 新 catalog：`b47c0ca115581428911c65baf9c48e7bcdbe4d050a4320c998f88763b931f18a`。
- migration：`70e37de35c9f044447a6ca0026a1d85448334de0628553f21910b62610de8598`。

## 后续

- 22 个 successor 必须重新审核，不继承旧 done。
- advisory carry_forward：Ashes 苦痛链接效果说明“牺牲生物”→“受害者”，排入窗口62。
- 窗口62 积压约 55 条（估算）：pending #50 B 的其余 killer_message 与 #51 B 的 dreadfell dark Master。
- 本 publication child 待宿主归档。
