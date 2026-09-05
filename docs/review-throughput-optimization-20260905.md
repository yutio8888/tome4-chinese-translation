# 审核吞吐优化：步骤 1、2（2026-09-05）

本次提供按既定排序装满最多 80 条的执行入口和离线阶段计时工具。
`MAX_BATCH=80`、`stable_selection`、`partition_surface_entries` 已有对应行为，无需改动。
[当前交接](production-review-handoff-2026-09-05.md)明确允许 batch 混来源，由 adapter 拆同质
run；来源变更不能截短 selected。单 screen 仍 ≤80，selected 按 revision 而非文本 group 计数。
[原文归档](archive/production-review-handoff-2026-09-05-history.md)完整保留历史字节；归档相对
链接以原目录 `docs/` 解析。归档命令不再指挥当前工作。

尚未执行：5 批最多 80 的有界基线、独立质量诊断、候选机械扫描与校准、3 批 160 试点。
本次未调用模型或生产审核，不修改生产 schema、策略、译文、术语或上限。
准备下一 80 条时发现 21/37/22 三个 run 共用 task ID 会违反 consumer 的单 whole-screen
终态约束；已最小适配新导出的多 run task ID 为 `<batch-id>-surface-000` 等，单 run 保留
历史 batch task ID，已导出的 checkpoint／group 不迁移。逐 run 独立 Paseo task 完成
`DONE_VERIFIED` 后才由宿主聚合 exact-union 导入；不靠 cycle／attempt 区分 screen。
详见[正式方案](translation-production-review-v2-lite-plan.md)。
独立普通／交叉／最终复审及 DONE 验证由 ORCHESTRATOR 后续完成，工具计时结束不代表审核完成。
三份现有未跟踪分析／提案仅作输入，保留原样；其相关性和估算不能证明因果或已节省工时。

## 离线计时

在仓库根运行 [review_phase_timing.py](../tools/review_phase_timing.py)，仅用 Python 标准库，
依赖 Linux 的 boot ID、time namespace 和 `flock`。每个批次使用一个新的、显式指定的日志路径，
必须位于本仓库被忽略的 `.artifacts/i18n/` 下；拒绝越界、父级跳转、符号链接和硬链接日志。
日志只作派生操作记录，不写 evidence、正式队列、译文或 `.ai`，不产生审核完成含义。

以下是后续有界任务的命令模板；将 batch ID、base commit、selected 换为实际冻结值，
在逐条源码核验开始前 start。selected 是实际领取数量（1..80），不是上限或 group 数。

```bash
python3 -B tools/review_phase_timing.py start --log .artifacts/i18n/timing/BATCH.json --batch-id BATCH --base-commit FULL_40_HEX_COMMIT --selected 80 --concurrency 3 --phase source_verification
python3 -B tools/review_phase_timing.py mark --log .artifacts/i18n/timing/BATCH.json --phase prepare_dispatch
python3 -B tools/review_phase_timing.py mark --log .artifacts/i18n/timing/BATCH.json --phase wait_reviewers
python3 -B tools/review_phase_timing.py mark --log .artifacts/i18n/timing/BATCH.json --phase import_adjudication
python3 -B tools/review_phase_timing.py mark --log .artifacts/i18n/timing/BATCH.json --phase gates
python3 -B tools/review_phase_timing.py mark --log .artifacts/i18n/timing/BATCH.json --phase closure
python3 -B tools/review_phase_timing.py finish --log .artifacts/i18n/timing/BATCH.json
python3 -B tools/review_phase_timing.py summary --log .artifacts/i18n/timing/BATCH.json
```

六个阶段顺序互斥，mark 关闭前一个区间并开始新阶段，可按真实活动重复切换（包括返回先前
阶段）。时长是主编排当前活动的 wall time；并行 child 的时间不能相加。日志保留真实 UTC，
相邻事件差值使用同一 boot／time namespace 的 `CLOCK_BOOTTIME` 单调纳秒（包含系统休眠），
UTC 调钟不影响计时。
暂停也计入当前阶段；需要单独表示无法归类的区间时使用
`mark --log PATH --phase unknown --missing-reason '原因'`，恢复后 mark 回已知阶段。
未知阶段有实际经过时长，但阶段归属未知。

finish 可附 `--child-count N --retry-count N --actual-tokens N`，三项独立记录实际值；
未提供时各自为 `unknown`，0 必须来自实际观测，不估价。concurrency 是当批操作配置，
当前为 3，不是契约上限；缺失亦为 unknown，配置变化应另记实际操作情况。
若 start 晚于真实批次开始、漏记阶段切换等，finish 必须附
`--incomplete-reason '原因'`；不得从旧 gate 首启时间反推精确周期。
重启或 time namespace 变化会拒绝继续计时，保留旧日志为未完成，另开日志并注明缺失；
不能跨域拼接或宣称完整周期。

summary 输出 batch identity、base commit、selected、各阶段已记录秒数、已记录 wall、完整
总 wall 与 selected/hour。未 finish 的开放区间不推算；未结束、未知阶段或显式缺失均令
`timing_complete=false`、完整总 wall 和速率为 `unknown`，已记录时长仍可查看。
零时长的完整记录也不计算速率。未经进入的阶段为已记录 0，不表示该生产步骤可跳过。
坏记录、重复 start／finish、finish 后 mark、时钟回退或换域明确失败，不覆盖原日志。
写入先验证后原子替换，同目录锁串行化本工具命令；失败前原文件保持原样。

## 后续有界执行与判断

1. ORCHESTRATOR 另建任务执行 5 批最多 80 的基线；每批完整计时，记录实际 selected、来源／run
   分布、child 数、重试、无效输出、实际 token（缺失 unknown）、确认缺陷和人工负担。
   人工负担记录裁决／修复耗时及操作情况，不用模型等待时间代替。结果保留测量条件与缺失项。
2. 独立质量诊断先核验筛查能力，再做候选机械扫描与误报校准。候选不等于缺陷，未知质量不等于
   通过。术语、标点统一策略或排序调整依仓库授权规则另行裁决，本次不落地扫描器或更改判据。
3. 只有基线与质量证据支持时，另建经过授权及契约适配的 3 批 160 有界试点；当前代码仍拒绝
   超过 80，不能直接用 `--limit 160`。试点有收益且质量证据通过后才考虑 240，不自动扩容。

固定通过条件：身份绑定、selected 守恒、逐条结果和门禁保持不变；计时完整；无效输出／重试、
确认缺陷、人工负担均记录并可比；独立诊断的质量结论有证据支持。仅速率增加或 observation=0
不足以通过；缺失数据不填零。不同批次内容与来源可能影响时间，报告只描述关联，不推因果。

退出／暂缓扩容条件：发现确定性一级漏检，先解决原因并重新验证；身份／守恒／门禁任一异常，
或质量未知、计时不完整、无效输出／重试及人工负担无法解释时，不进入扩容。
生命周期、重复实质分歧、无法归因的门禁失败等按 [AGENTS.md](../AGENTS.md)停下；有界基线
结束即汇报，不默认为无界连续审核。不得把本工具日志当作正式质量证据或 DONE 认证。

## 本次实现验证

2026-09-05 本地执行：

- `python3 -B -m unittest tests.i18n.test_review_phase_timing tests.i18n.test_production_review_v2_lite_batch tests.i18n.test_test_groups -v`：29 项通过。
  计时覆盖真实跨进程时钟、并发重复 start、阶段累计、UTC 调钟、缺失值、坏记录／写失败保持原字节、
  越界路径和重复 finish。适配覆盖 21/37/22、多 run 的 1/2/3 full＋四 lane、单 run 历史路径及
  旧格式 stored group；使用真实 consumer 和逐 run 终态 checker，缺失完成记录拒绝，随后验证
  exact-union 导入及幂等重导入。合成 child／结果仅存在临时测试仓库，不是生产审核证据。
- `tools/ci-gates.sh`：17 项完整门禁全部通过，含严格 addon build，未使用 `--skip-build`。
- `git diff --check`、新增文件空白检查、归档与 baseline 原始字节比较、范围内 Markdown 相对
  文件链接检查、三份输入报告 SHA-256 基线比较均通过。

这些是实现验证结果。主任务的独立普通／交叉／最终复审和 `DONE_VERIFIED` 尚由 ORCHESTRATOR
完成；5 批生产基线及后续诊断／扩容仍未执行。
