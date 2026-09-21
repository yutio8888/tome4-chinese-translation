# 修复窗口 2 收口摘要

## 范围与译文结果

- 本窗口只处理审核批 243 已授权的五个 revision；译文提交为 `14c755659d18a5f0989ec75d67f0245de3f0cc13`。
- 固定源码为 tome commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；五条均属 tome，无 DLC，来源锚点见本目录及冻结编排快照。
- Atamathon/Garkul：恢复“建造的唯一目的在于阻止加库尔本人”，去掉虚构的“加库尔率领军队”和“傀儡王”，保留数千人大军及 `demonic fighter` 的凶悍比喻。
- Gloves of the Firm Hand：将 `brace yourself` 落为稳住身体，将 `shifting` 与旋转区分，并保留 `seems` 的不确定语气，不把风味描述升级成额外机制。
- Wild Summon：首行改为 `%d` 回合内召唤兽出现时成为野性版本的概率；实际初始概率为 100%，每回合乘 0.66 并取整。乌龟按 `T_BATTLE_CALL` 的移位效果写为迫使半径内敌人进入近战范围，不与基础 `T_TAUNT` 混同；全条其余能力、激活条件与缩放信息一并补全。
- Indiscernible Anatomy：固定源码的 `ignore_direct_crits` 是按 `%d%%` 削减直接暴击的额外伤害倍率，不是 RNG 概率免疫，也不是总伤害减免；第二个 `%d%%` 仍是疾病、毒素、流血与目盲免疫。`HOST-CUT-01` 另据固定源码和现有术语独立确认 `cut_immune` 的玩家可见状态名应为“流血”，因此撤销 cycle 0 的“切割已吻合”判断，仅修正同一获授权 target，未改术语库。
- Honeywood Chalice：补回木杯、似乎永远盛满、树液状物质和饮用时感官异常敏锐，未引入“酒”。
- `%d` 时长、`%d%%` 直接暴击额外伤害削减和 `%d%%` 状态免疫的值流及 placeholder/markup/newline 不变量，已记录于 `implementation.md`、`fix-cut.md`、`validation.json` 与 `validation-c1.json`。

## 独立复审与验证边界

- 有效 stage 为：cycle 0 attempt 2 的四个独立 lane 全部 `PASS`；cycle 1 attempt 1 的 Anatomy closure 为 `PASS`；cycle 1 attempt 3 的 `FINAL_REVIEW/full` 为 `PASS`。
- cycle 0 attempt 1 因 lane 4 读取未引用的历史输入而整组判废；其余 lane 的诊断输出也未计入有效通过。cycle 1 attempt 2 因原生日志的 cwd 与任务工作区不匹配而判废。两次判废尝试均不算通过，其 observation/finding 未被自动采纳。
- 完整 ci-gates 共 17 项，含严格 lint 和 tome addon 严格构建；收据记录 `2026-09-21T12:34:21.117279+00:00` 开始、`2026-09-21T12:36:28.266183+00:00` 结束，实际跨度 `127.148904` 秒，17 项 exit code 均为 0。`DONE-review-validation-checkpoint.json` 在 `2026-09-21T12:37:02.989651+00:00` 记录真实 `DONE_VERIFIED`、exit code 0。
- `orchestration/` 是按 `orchestration-pack-manifest.json` 逐字节归档的 159 文件冻结快照。其中 STATE 表示全部译文执行/复审 child 已归档、完整门禁已通过、译文提交前的验证边界；它不是本次证据整理 child 完成后的实时 STATE，也不表示后续出版步骤已经完成。
- 本轮以该归档目录为 `--workspace-root` 再次运行 `tools/ai_state_check.py`，真实 exit code 为 0，stdout 为 `DONE_VERIFIED: DONE predicate verified`，stderr 为空；实际 argv 见 `snapshot-replay.json`。

## 首轮同步、catalog 与迁移

- 首次 queue rebuild 实际 exit code 0，`2026-09-21T12:37:24.501702+00:00` 至 `2026-09-21T12:41:25.148851+00:00`，CLI wall `240.6471595110197` 秒。
- authoritative catalog build 实际 exit code 0，`2026-09-21T12:41:49.340822+00:00` 至 `2026-09-21T12:41:53.134098+00:00`，CLI wall `3.793275818985421` 秒。
- migration chain 成功，CLI elapsed `250.31913208699552` 秒；plan/check/apply 均 exit code 0。以上均为各 CLI 的实际计时，不是窗口端到端耗时，不得相加冒充端到端时间。
- catalog 从 `4ec0ae983f6b435c31883e06cdc96800a88189758f2503f4e0c7e0375c203b8c` 迁移至 `2a8b6f4ac30dba6abff9e96dc37295d5e0f20acb5e4b97067160261b346e358d`。宿主比较结果为 5 `revision_changed` / 29823 `unchanged`，来源和术语未变；migration `0e4ad828eb000567f49f34b1b7a9e8c823550740697b51a4d616d72cc9dac454` 的实际结果为 `queued_successors=5`、`ambiguous=0`、`unmapped=0`。
- `migration apply` 只先更新了 SQLite，并未安装工作树 catalog 文件。依 SPEC 的确定性安装授权，本轮随后把已核验候选 catalog 的五个文件逐字节安装到同名工作树路径，并把已 check/apply 的 migration JSON 逐字节安装到上述新 migration ID 路径；相同 bytes 的三个支撑文件未重写，所有六个目的文件均已复核与来源 bytes/SHA-256 一致。没有手改、重建或改写旧迁移。
- 五个 successor 只表示进入待审核队列，仍需重新审核；不得称为生产深审已完成。

## 排除项与尚未完成的出版步骤

- Archmage revision `8b977dd836…` 仍为范围外 pending，不计入可执行 revision 阈值，也不阻塞后续审核。
- `RW1-SIB-01`、`RW1-SIB-02` 永久排除；本窗口没有术语库变更、全局重命名或跨批次策略变更。
- 本摘要产生时，证据/catalog/migration commit、第二次 queue rebuild 和 push 均尚未执行；这三项由宿主随后完成，不在本记录中提前声称完成。
