# 修复窗口 30 发布记录

窗口 30 覆盖审核第 284–286 批确认的 23 条问题，现已全部修复，且修改均位于
`tome-ashes-urhrok.lua`。Ashes of Urh'Rok 仅固定并核验了相关源码文件的 SHA-256，源码仓库与
commit 未固定；主游戏源码的固定 commit 见冻结 manifest。

## 复审与裁决

- 开窗前，宿主对长 lore 逐句预检，并把结果并入修复；记录见
  [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。
- 复审路径为 `REVIEW(0)` `r0a1` → `execute-02` → `FINAL_REVIEW(1)`。`f1a1` 输出无效，按同一
  envelope 重派 `f1a2`，确认 3 条问题：空间控制者击杀信息的句中句号、轨道基地便条的灯光音响命令、
  恶魔种子治疗／复活条件被误写为无条件。
- `execute-03` 修复后，`RE_REVIEW(2)` 为 23/23 OK；`FINAL_REVIEW(2)` `f2a2` 确认“遗失的记忆（1）”
  的 4 处种族名模板占位符被改成“同族”，由 `execute-04` 恢复。
- `RE_REVIEW(3)` 为 23/23 OK；`FINAL_REVIEW(3)` `f3a2` 确认“血之契约”的“黑暗伤害”应使用本库
  伤害类型名“暗影伤害”。任务达到 `max_cycles=3` 后停止，用户授权第 4 轮，随后将审批轮次常驻放宽到 5；
  授权见 [`publication/USER-AUTH-CYCLE4.json`](publication/USER-AUTH-CYCLE4.json) 与
  [`publication/USER-AUTH-MAX-CYCLES-5.json`](publication/USER-AUTH-MAX-CYCLES-5.json)，任务 STATE
  已记录 `max_cycles_user_authorized=true`。
- `execute-05` 修复后，`RE_REVIEW(4)` `r4a1` 确认轨道基地便条的“最后一个 O”在中文无所指，改为
  “最后一笔”；“黑之锤”中 `the Champion` →“冠军”的意见记为 advisory，未修改。`execute-06` 修复后，
  `FINAL_REVIEW(4)` `f4a2` 为 23/23 OK，本窗收敛。
- 首次门禁因同一 cwd 出现第二个 Paseo workspace，导致第 05 项单测无法确定 workspace 而失败；该失败
  与译文无关。钉住 `TOME_PASEO_WORKSPACE=wks_420314270844170b` 后，17 项门禁全部通过，其中包含
  严格构建；任务状态达到 `DONE_VERIFIED`，参与本窗实现与复审的全部 executor/reviewer 均已归档。

## 发布身份

- 译文提交：`941824e9642823b8a3575eee10bea5217be2afc5`
- 新 catalog：`274ebb14863a03c5b126f0e6eae11007566251a2abf907c975d715c6523b4a54`
- migration：`daf1db308df9338220de2ec659ddb41f69cbf7de75601f44d95dc1b20787baf8`
- catalog 变更：23 个 revision changed，29805 个 unchanged，0 ambiguous，0 unmapped。
- migration 生成 23 个 successor；这些 successor 必须重新审核，不继承旧 revision 的 done 状态。

## 证据索引

- 冻结编排快照：[`orchestration/`](orchestration/)
- 快照清单：[`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)
- 发布附件：[`publication/`](publication/)
- 实施记录：[`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- 实现验证：[`VALIDATION.json`](VALIDATION.json)

本 publication child 完成本记录与证据安装后，仍待宿主确认归档。宿主后续还需提交本窗证据、执行
关闭后的 queue rebuild 并 push，然后继续审核第 287 批；本文不提前宣称这些宿主动作已经完成。
