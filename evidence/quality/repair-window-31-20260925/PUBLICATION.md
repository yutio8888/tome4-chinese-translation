# 修复窗口 31 发布记录

## 范围与结果

- 来源批次：第 287、288、289 批。
- 共修复 23 条已确认问题：`tome-cults.lua` 17 条，`tome-ashes-urhrok.lua` 6 条。
- Cults 与 Ashes 仅固定翻译文件 SHA；DLC 源码仓库及 commit 未固定。主游戏固定 commit 见本窗口 orchestration 快照中的 manifest。
- 开窗前，宿主已对长 lore 逐句预检并将结果并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。

## 复审与收敛

复审路径如下：

1. `REVIEW(0)` `r0a1`：`11d3` 的 numbed 问题判为 refuted；随后 `execute-01`。
2. `FINAL(1)` `f1a1`：确认 2 条——艾德瑞尔是半身人王国而非人名；德瑞姆条目漏译 mindless；随后 `execute-02`。
3. `RE_REVIEW(2)` `r2a1`：确认 2 条——恐怖堡垒日志“士气大振”应改为护甲／防护含义；阿马克泰尔技能应为“召唤的”恐魔；随后 `execute-03`。
4. `FINAL(2)` `f2a2`：确认 3 条——应为向窗外望而非开窗、`not particularly wholesome` 含义缺失、酒馆招牌并非路标。`f985` 行尾两个 TAB 先由宿主判为 confirmed，后依第 `2812a8e5` 批先例及门禁 11（`git diff --check`）更正为 advisory；`execute-04` 已按原 prompt 补回，`execute-05` 撤回，详见 [`publication/HOST-NOTE-execute-04-f985-withdrawal.json`](publication/HOST-NOTE-execute-04-f985-withdrawal.json)。
5. `RE_REVIEW(3)` `r3a1`：确认 1 条——attune 改为“相协调”；`f985` 的效果／层数问题及 `11d3` 问题判为 refuted；随后 `execute-06`。
6. `FINAL(3)` `f3a2`：23/23 OK，复审收敛。

`11d3` 的 numbed→麻痹问题四次被 GPT-6 Sol 提出，已由宿主登记为 `pending-user-review.md` 第 30 项，交由用户裁决。

## 验证与发布标识

- 17 项门禁全部通过，包含严格构建；任务状态为 `DONE_VERIFIED`。
- 全部 reviewer 与修复 executor 均已归档。
- 译文提交：`4259b5ff762152c3da3c4df44bdd8f669b1ba13e`。
- 新 catalog：`537aef5ca467c11995bb2405b5b1b8b7e2b8268469d00262509769e3c4d3fc53`。
- migration：`bb2265e211b14ef5fecfb33b606abdbb40d72aa83fe73d750a8f77cc3d52bd2a`。
- 23 个 successor 必须重新审核，不继承旧 revision 的 done 状态。
- 本 publication child 尚待宿主归档；宿主的证据提交、关闭后 queue rebuild 与 push 尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
