# 修复窗口18发布记录

修复窗口18仅处理审核264确认的4条问题，未扩大范围：

- “#Target# is being crushed.”由“被击碎”改为进行态“正被碾压”。
- 队友行为菜单 `Standby` 由“乖乖站好”改为与日志一致的“待命”。
- `Offhand Jab` 首句补出以出其不意的徒手攻击替代通常的副手攻击，并删去一处多余换行，使 LF 与原文一致。
- Z’quikzshl 日记改正 `trivial`、名字走音末句、代词与“艾德瑞尔红宝石”，并把 `not ready for the rites of lichdom` 改为“还没准备好接受巫妖仪式”。

任务 `repair-w18-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施4条修改。`REVIEW(0)/full`（`codex/gpt-6-sol`）给出3 OK / 1 ISSUE，确认 `R0-ZQUIK-RITES-READINESS`：“没有做巫妖的条件”把准备程度改成了资格判断。`execute-02` 仅修改该分句。`FINAL(1)/full`（`claude-opus-5-5`）给出4 OK，任务收敛。完整门禁17/17通过，包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `8f71effdeded7b84df4fa5d9625289d0d10a0b4b`；新 catalog 为 `2cd472deee7159e35cb53656b3311a9232752be19817adb5edee7e5db494b7c2`；migration 为 `4847d321cc828a85d29b12b3c05a399eee35a700288d9ade838f8b84a443f58f`。迁移结果为4条 `revision_changed`、29,824条 `unchanged`、0条 `ambiguous/unmapped`，4个 successor 待重新审核且不继承 `done`。本窗口无新增 pending。

两个 executor child 与两个 reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/4847d321cc828a85d29b12b3c05a399eee35a700288d9ade838f8b84a443f58f.json)。本证据提交、第二次 queue rebuild 与 push 均由宿主后续执行，尚未宣称完成。
