# 修复窗口 29 发布记录

窗口 29 覆盖审核第 281–283 批确认的 21 条问题，现已全部修复，且修改均位于
`tome-ashes-urhrok.lua`。Ashes of Urh'Rok 仅固定并核验了相关源码文件的 SHA-256，源码仓库与
commit 未固定；主游戏源码的固定 commit 见冻结 manifest。

## 复审与裁决

- 开窗前，宿主对哈卡祖雕像、火魔婴雕像、乌鲁洛克创世史三条长 lore 逐句预检，并把结果并入修复；
  记录见 [`publication/ADJUDICATION-HOST-PRECHECK-C0.json`](publication/ADJUDICATION-HOST-PRECHECK-C0.json)。
- `REVIEW(0)` 的 `r0a2` 结果为 19 OK / 2 ISSUE。`72a3b333` 的“半径 10”由公开 Ashes 实现硬编码，
  因此驳回该 finding；`9ac85a7a` 的 `%s` 填充词为动词“背叛／屠戮”，finding 确认，并把
  “纳鲁精灵的%s”改回“%s纳鲁精灵”。
- `execute-02` 修复后，`FINAL_REVIEW(1)` 的 `f1a1` 为 21/21 OK；本窗一个 cycle 收敛。
- `r0a2` 的 attempt 1 因 SCOPE 把证据目录列入允许文件，在 anchor preflight 报 `INPUT_ERROR`，未派发；
  该无效尝试已如实保留在冻结编排快照中。
- 唯一获准的单条改名为 `Overwhelming Fear`：“无尽恐惧”→“压倒性恐惧”；宿主已做双向冲突核查。

完整门禁 17 项全部通过，其中包含严格构建；任务状态达到 `DONE_VERIFIED`，参与本窗实现与复审的
全部 executor/reviewer 均已归档。

## 发布身份

- 译文提交：`67a3a394b02b92a60a32b21c5df203ac08a1651e`
- 新 catalog：`595fa838eb8ae17f3d022c0f3cf9ab9af48eebe6ad7f4ea04160d51a255c1c8f`
- migration：`33667e0f131e372a7f313763a9e2bbac876a263a88eb1784c9c063a2f50da619`
- catalog 变更：21 个 revision changed，29807 个 unchanged，0 ambiguous，0 unmapped。
- migration 生成 21 个 successor；这些 successor 必须重新审核，不继承旧 revision 的 done 状态。

## 证据索引

- 冻结编排快照：[`orchestration/`](orchestration/)
- 快照清单：[`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)
- 发布附件：[`publication/`](publication/)
- 实施记录：[`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- 实现验证：[`VALIDATION.json`](VALIDATION.json)

本 publication child 完成本记录与证据安装后，仍待宿主确认归档。宿主后续还需提交本窗证据、执行
关闭后的 queue rebuild 并 push，然后继续审核第 284 批；本文不提前宣称这些宿主动作已经完成。
