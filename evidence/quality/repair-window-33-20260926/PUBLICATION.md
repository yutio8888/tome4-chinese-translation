# 修复窗口 33 发布记录

## 范围与结果

- 来源批次：第 294、295、296、297 批。
- 共修复 21 条已确认问题，全部位于 `tome-cults.lua`。
- Cults 仅固定翻译文件 SHA，DLC 源码仓库及 commit 未固定；主游戏固定 commit 见本窗口 orchestration 快照中的 manifest。
- 开窗前，宿主已对长 lore 逐句预检并将结果并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。
- 竞技场名 `Commotion` 由“骚乱”改名，属于 SPEC 登记的改名例外。

## 复审与收敛

复审路径如下：

1. `REVIEW(0)` `r0a1`：确认 2 条——食人魔突围手记的“饶了你／任由狂热者摆布”；交战一节的“临死时的哀嚎声”；随后 `execute-02`。
2. `RE_REVIEW(1)` `r1a1`：确认 1 条——“为她处理伤口”；随后 `execute-03`。
3. `RE_REVIEW(2)` `r2a1`：确认 2 条——燃烧痛苦的 `inscriptions` 改为“刻印”（宿主将原 advisory 改判）；清理垃圾任务的 `Permanently` 改为“永久的代价”；随后 `execute-04`。
4. `RE_REVIEW(3)` `r3a1`：龙卷风鞋的 `spinning` 判为 refuted。
5. `FINAL(3)` `f3a1`：确认 1 条——纳格尔一节的 `sterner composition` 是恭维“更坚韧”，`livid` 为“怒不可遏”；随后 `execute-05`。
6. `RE_REVIEW(4)` `r4a1`：确认 1 条——新兵 `fell to the magical barrage` 改为“在魔法齐射中倒下”；随后 `execute-06`。
7. `RE_REVIEW(5)` `r5a1`：宿主确认 1 条——食人魔“打翻……扔进”多出“扔”的动作；在 `max_cycles=5` 停止点经用户裁决降为 advisory，不修。另有 2 条 advisory：`519f027d` 省略 `remember`、`61b8c541` 的“梦中的我”措辞。
8. `FINAL(5)` `f5a1`：21/21 OK，复审收敛。用户授权 `max_cycles=5`，本窗口用满 5 轮。

## 验证与发布标识

- 第一次门禁 05 因投影缓存并发测试计时抖动失败；对应单测 5/5 通过，记录见 [`publication/HOST-NOTE-GATES-ATTEMPT-1.md`](publication/HOST-NOTE-GATES-ATTEMPT-1.md)。重跑后 17 项全部通过，包含严格构建。
- FINAL 记录的 attempt 编号更正见 [`publication/HOST-NOTE-FINAL-ATTEMPT-RENUMBER.md`](publication/HOST-NOTE-FINAL-ATTEMPT-RENUMBER.md)。
- 任务状态为 `DONE_VERIFIED`；全部 reviewer 与修复 executor 均已归档。
- 译文提交：`bf6862841e08fb2791d61cbc2d1bea90bae41cff`。
- 新 catalog：`4e2f012517a766201d625309209c49c3684c2213ec70b54f40848ca9a9d9a330`。
- migration：`36102218c9582721a8ce510865b0bcf3f76192366b0491b96f8ae43aa54c7e4d`。
- 21 个 successor 必须重新审核，不继承旧 revision 的 done 状态。
- 本 publication child 尚待宿主归档；宿主的证据提交与推送尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
