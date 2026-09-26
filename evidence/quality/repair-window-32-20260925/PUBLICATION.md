# 修复窗口 32 发布记录

## 范围与结果

- 来源批次：第 290、291、292、293 批。
- 共修复 26 条已确认问题，全部位于 `tome-cults.lua`。
- Cults 仅固定翻译文件 SHA，DLC 源码仓库及 commit 未固定；主游戏固定 commit 见本窗口 orchestration 快照中的 manifest。
- 开窗前，宿主已对长 lore 逐句预检并将结果并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。

## 复审与收敛

复审路径如下：

1. `REVIEW(0)` `r0a1`：确认 2 条——德瑞姆手记中的 `latched onto` 并非“咬”；返回符文是 `presented`（“递向”）而非交给；随后 `execute-02`。
2. `RE_REVIEW(1)` `r1a1`：确认 2 条——`half formed fetuses` 改为“胎儿”；污秽夹击应为双方各攻击一次；随后 `execute-03`。
3. `RE_REVIEW(2)` `r2a1`：确认 2 条——将军 `occupied` 删去“公务”；`let alone active` 指行动而非思维；随后 `execute-04`。
4. `RE_REVIEW(3)` `r3a1`：26/26 OK。
5. `FINAL(3)` `f3a2`：确认 2 条——卫兵一句的让步关系倒置；天谴之龙解锁文本四行 `#WHITE#` 后存在多余空格；随后 `execute-05`。
6. `RE_REVIEW(4)` `r4a1`：衰亡“尝试切断”依据 `checkHit` 与即死免疫判为 refuted；`flesh`→“肌肉”记为 advisory。
7. `FINAL(4)` `f4a2`：26/26 OK，复审收敛。用户授权 `max_cycles=5`，实际用到第 4 轮。

## 验证与发布标识

- 17 项门禁全部通过，包含严格构建；任务状态为 `DONE_VERIFIED`。
- 全部 reviewer 与修复 executor 均已归档。
- 译文提交：`cfc207c1eb27b6209fe8de608935fcb4909eeffb`。
- 新 catalog：`a15b2104c19bc1eaa3a3a3351c651712b55b30234a2acfaf52dd9933f71ef29e`。
- migration：`da80ce55e962bb196d2e462f673ff03d0100218a03f5d577ddb40ef11104f416`。
- 26 个 successor 必须重新审核，不继承旧 revision 的 done 状态。
- 本 publication child 尚待宿主归档；宿主的证据提交、关闭后 queue rebuild 与 push 尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
