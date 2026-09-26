# 修复窗口 34 发布记录

## 范围与结果

- 来源批次：第 298、299、300、301 批。
- 共修复 29 条已确认问题，全部位于 `tome-cults.lua`。
- Cults 仅固定翻译文件 SHA，DLC 源码仓库及 commit 未固定；主游戏固定 commit 见本窗口 orchestration 快照中的 manifest。
- 开窗前，宿主已对 10 条长 lore 逐句预检 39 项并将结果并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。
- 首个 EXECUTOR 会话发生上下文压缩，原生 harvest 不支持；依照窗口 27 先例记 `output_valid=null`，成果由宿主按精确 diff 独立核验，记录见 [`orchestration/.ai/task/repair-w34-20260926/HOST-EXECUTOR-AUDIT.json`](orchestration/.ai/task/repair-w34-20260926/HOST-EXECUTOR-AUDIT.json) 与 [`publication/HOST-NOTE-SCOPE-AND-EXECUTOR.md`](publication/HOST-NOTE-SCOPE-AND-EXECUTOR.md)。

## 复审与收敛

复审路径如下：

1. `REVIEW(0)` `r0a1`：确认 2 条——骨巨人之战的“护盾符文／遍体鳞伤”、伊胡拉什的“科技与超自然技艺”；背叛预言的“周围”按 `doom.lua` 10 格实现判为 refuted；随后 `execute-02`。
2. `RE_REVIEW(1)` `r1a1`：确认 1 条——蛆虫的“最后一餐”；随后 `execute-03`。
3. `RE_REVIEW(2)` `r2a1`：恐魔化的“重新考虑攻击目标”记 advisory，复审收敛。
4. `FINAL(2)` `f2a2`：仅返回 4/29 条，判无效；`f2a3` 确认 3 条术语——马基·埃亚尔、返回符文、梅琳达；随后 `execute-04`。
5. `RE_REVIEW(3)` `r3a1`：“周围”再次判为 refuted。
6. `FINAL(3)` `f3a2`：确认 2 条——狂热的 `inscriptions` 改为“刻印”以涵盖污印、食人魔与符文融合的指代；随后 `execute-05`。
7. `RE_REVIEW(4)` `r4a1`：`stralite=斯莱特` 判为 refuted，恐魔化记 advisory。
8. `FINAL(4)` `f4a2`：确认 1 条——将军朝中尉点头，护送者即中尉；随后 `execute-06`。
9. `RE_REVIEW(5)` `r5a1`：2 条 advisory——地道拟人、`staves` 木棍。
10. `FINAL(5)` `f5a2`：29/29 OK，复审收敛；`max_cycles=5` 用满。

复审记录在收敛后按时间顺序补发布，说明见 [`publication/HOST-NOTE-LATE-PUBLICATION.md`](publication/HOST-NOTE-LATE-PUBLICATION.md)。

## 验证与发布标识

- 17 项门禁首次全部通过，包含严格构建。
- 任务状态为 `DONE_VERIFIED`；全部 reviewer 与修复 executor 均已归档。
- 译文提交：`97f3d9ede57952764e6d9f34b8e2d5cf73844be3`。
- 新 catalog：`36168c582860a782955361806bdc67d1f9f39139e3ce18c0e191acbcfa811b78`。
- migration：`8256424947dd2716359d72d663d7c5841dd0df88eb881b5f7ac20afb47a76654`。
- 29 个 successor 必须重新审核，不继承旧 revision 的 done 状态。
- 窗口外同类写法 2 处登记为下一窗口宿主补充项：起于 `tome-cults.lua` 第 1557 行条目的“马基埃亚尔”、起于第 1815 行条目的“回归符文”。
- 本 publication child 尚待宿主归档；宿主的证据提交与推送尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
