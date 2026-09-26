# 修复窗口 35 发布记录

## 范围与预检

- 来源批次：第 302、303、304、305 批。
- 共修复 21 条已确认问题，全部位于 `tome-cults.lua`。
- Cults 仅固定文件 SHA，源码仓库与 commit 未固定；主游戏固定 commit 见本窗口 orchestration 快照中的 manifest。
- 开窗前，宿主已逐句预检 38 项并将结果并入修复，记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。

## 复审路径

1. `REVIEW(0)` `r0a1` 确认 4 条：克罗格锤“讯息贯彻到底”；传送克诺什库尔“未入门的目击者视野内”；纳格尔木桩“听到伊格兰斯的讯息”，宿主整句核对另补 4 处；天谴之坑手记 `dreams`→“梦想”。最后一条 reviewer 误挂在 `cac325d0`，宿主按内容改挂 `cd5fc3af`，`cac325d0` 记 refuted。
2. `execute-02` → `RE_REVIEW(1)` `r1a1` 确认 1 条：克罗格 `rogue mage`→“不法法师”。
3. `execute-03` → `RE_REVIEW(2)` `r2a1` 21/21 OK，收敛 → `FINAL(2)` `f2a2` 21/21 OK。

## 门禁与运行时键同步

- 首次 17 项门禁在 `06-runtime-collision-scan` 失败：`c26a569f` 的运行时键与 `mod-tome.lua`、`tome-orcs.lua` 同键不同值。
- 三个组件的源码都在 `on_gain` 发消息、`on_timeout` 才失去控制，所以“即将中断”对三处都成立。`execute-04` 将两处同步为与已复审目标逐字节相同的文本，记录见 [`publication/RUNTIME-SYNC.json`](publication/RUNTIME-SYNC.json) 与 [`publication/HOST-NOTE-RUNTIME-SYNC.md`](publication/HOST-NOTE-RUNTIME-SYNC.md)。
- 重跑门禁 17/17 全过，含严格构建；首轮失败日志在 orchestration 快照中保留为 `FINAL-GATES-attempt1-runtime-collision`。

## 发布说明与标识

- 复审记录在收敛后按时间顺序补发布，说明见 [`publication/HOST-NOTE-LATE-PUBLICATION.md`](publication/HOST-NOTE-LATE-PUBLICATION.md)。
- `SCOPE` 的 `allowed_files` 起初误含证据目录，冻结前已按先例改正，记录见 [`orchestration/.ai/task/repair-w35-20260926/HOST-NOTE-SCOPE.json`](orchestration/.ai/task/repair-w35-20260926/HOST-NOTE-SCOPE.json)。
- 任务状态为 `DONE_VERIFIED`；全部 reviewer 与 executor 已归档。
- 译文提交：`2282a5e7777cc73118fbe86226cd6363fd054df1`。
- 新 catalog：`687d896fc3a968806876ac4b4a452316768ed28277e1ffccf8a7ea39574df123`。
- migration：`d6d21bc18c0f1813c33133dda57a0b0429fa4262c8d3564922559baa89eaa46c`。

## 后续

- 23 个 successor 必须重新审核，不继承旧 done；其中 `mod-tome` 同步条目原 done 于 `batch-4fec420db52243e27db4`。
- 窗口外宿主补充项 3 处留给下一窗口：`tome-cults.lua` 起于第 1557 行的条目“马基埃亚尔”；`a9c22a10` `misery`→“困难”；`a5a712dc` `Writhing One` 技能名。
- 本 publication child 待宿主归档；宿主的证据提交与推送尚未在本文中宣称完成。

发布附件位于 [`publication/`](publication/)，完整审核验证快照位于 [`orchestration/`](orchestration/)，快照清单为 [`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)。
