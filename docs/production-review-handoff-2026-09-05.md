# 正式审核当前交接（2026-09-05）

本文是当前执行入口，记录恢复基线及连续审核授权；不修改审核契约。后续批次结果以
Git 中 `evidence/production-review-v2-lite/batches/` 和当前队列重放为准，本文数字是
恢复时快照。旧 P2 handoff 保留历史原文，不再作为“下一批”的指令。

## 当前基线

恢复起点为 `4bcdd257c9dee7ec54158ce5f57163c8faa08187`，工作树干净。六项工具优化已全部
按批准范围完成，详见[完成记录](review-pipeline-and-tooling-optimization-plan.md)。
初始恢复修复派生队列与进度文档；后续派发兼容修复与审核续跑见文末。译文、术语及旧审核证据未改。

正式 catalog ID 为 `113687afa1f6fe8f9d890979a6ef08c342e5e3256a58b0eddc5282615022adc5`。
共 30,308 occurrences，29,828 eligible、480 exclusions。现行 policy 的审核范围为
engine、boot、tome、ashes-urhrok、orcs、cults；catalog 的组件清单不等于 eligible 范围。

18 个已提交批次共含 1,440 条历史结果（1,314 surface_only、126 deep_reviewed）。
历史结果含后续失效版本，不能作为当前覆盖。重建后 `queue check` 的当前版本统计为：

| 指标 | 条目数 |
| --- | ---: |
| 当前表层覆盖 S | 1,339 |
| 当前深审覆盖 D | 47 |
| 当前待修复 R | 0 |
| 曾发生历史版本失效 I | 97 |
| I 中已有当前审核 | 91 |
| I 中尚无当前审核 | 6 |
| 当前 done | 1,339（surface_only 1,292；deep_reviewed 47） |
| 当前隐式 queued | 28,489 |

S、D、R、I 是可重叠指标，共同分母为 29,828，不相加作完成总量。旧 P1／P2 的有界
源码复核成果不自动继承为正式队列的当前认证；没有当前证据也不等于已经确认存在缺陷。

## 队列恢复与验证

恢复前 `batch show` 为 `active=false`。只读 SQLite meta 核验发现 catalog ID 与当前
catalog 一致，但 `evidence_head` 仍为工具优化 P3 提交
`563382eeda2db31f1bb49b4229f9a7afc0282344`。

标准 `production queue rebuild` 已成功，随后 `production queue check` 通过，后者
`active_writer=false`、`ok=true`，证据头绑定恢复起点。受跟踪恢复记录见
[`queue-recovery-20260905.json`](../evidence/reconciliations/production-review-v2-lite/queue-recovery-20260905.json)。
重建调用自身持锁，因此其返回的 `active_writer=true` 不表示遗留另一个 writer。

交接文档提交也会推进 HEAD。开始下一批前必须再重建同步该提交并检查；不能把普通
HEAD 更新产生的过期投影误判为 catalog 内容损坏。常规恢复顺序：

```bash
python3 -B tools/i18n doctor
python3 -B tools/i18n production batch show
# 仅在无活动 checkpoint 时：
python3 -B tools/i18n production queue rebuild
python3 -B tools/i18n production queue check
python3 -B tools/i18n production batch start --limit 80
```

若有活动批次，先按[正式审核方案](translation-production-review-v2-lite-plan.md)的恢复
分支处理，不删除 checkpoint、不另开 writer。

## 继续审核与保留边界

维护者在本会话明确授权：“执行重建修复工作，修复交接完成后继续主持审核”。按现行
policy 的稳定排序领取最多 80 条；每批先表层筛查，ISSUE 进入独立语境审核及宿主源码
裁决。confirmed 才进入修复，修复在批次边界单独完成，不能在活动 catalog 上改译文。
每批保持工作集固定源码核验、Paseo 角色分离、候选冻结／preflight、适用门禁、
`DONE_VERIFIED`、本地提交和 child 归档；之后直接领取下一有界批次。

本次授权不改变术语库／全局重命名的停下规则，也不启用表层 OK 抽样比例或高风险
直接深审策略；push、PR、发布和 P3 外部操作仍需另行指示。重复实质分歧、无法归因的
门禁失败、生命周期无法确认等条件按 [AGENTS.md](../AGENTS.md) 停下交回维护者。

三个官方 DLC 的公开性已确认，但源码仓库／commit 未固定；固定提取快照不是源码
pin，也不证明源码版本为 1.7.4。机制核验必须记录实际公开源码与来源未固定的事实。

## 历史记录的使用

- [项目路线图](project-roadmap.md)：P0–P6 的历史阶段；与工具优化 P1–P6 编号不同。
- [旧 P2 交接](p2-tome-texts-handoff-2026-08-25.md)：截至 b43 的文本批次证据及旧 b44
  边界；不能仅据 workset 存在认定 b44 已完成。
- 旧交接披露的五个 chats section 缺受跟踪锚点，以及 quests 的旧范围问题，仍是
  历史审计边界。本次不补造审核证据；现行六组件正式 policy 的逐项覆盖由队列计算。
- 正式质量研究、Gold／Silver TM 与发布事项不随本次恢复自动启动。

## 恢复过程中发现并关闭的派发兼容问题

交接修复已提交为 `5bf4471`。随后领取的 `batch-41de87485e4b4b8e8bb5` 共 80 条，
全部固定源码核验通过；其[源码工作集](../evidence/quality/production-batches/batch-41de87485e4b4b8e8bb5-source-workset.json)
只证明来源，**没有审核完成含义**。首次创建因 MCP labels 仅接受 string 而拒绝 numeric
`lane_index`，未创建任何 child、未得到任何审核结果；标准 `batch abandon` 已撤销预约。

接口兼容修复 `51ad055` 已完成独立普通／交叉及最终复审、17 项完整门禁和
`DONE_VERIFIED`，详见[完成记录](paseo-lane-label-compat-20260905.md)。仅创建 label 兼容
精确 `"1"`..`"4"`；历史整数 labels 保留，结构性 lane index 仍为数值，审核身份与策略未变。
之后从新 HEAD 重建并重新预约同一工作集，工具按工作集生成的 batch ID 保持不变；
原未派发 STATE 单独保留诊断，新的审核绑定新基线，不复用任何 child 或完成记录。

## 恢复后的首批完成

`batch-41de87485e4b4b8e8bb5` 已提交为 `b1a3318d0e1199d0d053900a8611dc0e020d754d`
并成功 finalize。四路独立 surface screen 共 80 条全部 OK，无 observation、无修复项；
整组 `DONE_VERIFIED`，四名 child 均已确认归档。17 项完整门禁全部通过，含严格 addon build。
正式证据见[批次 manifest](../evidence/production-review-v2-lite/batches/batch-41de87485e4b4b8e8bb5/manifest.json)。

该提交的队列状态校验通过：当前 S／done 为 1,419（surface_only 1,372；deep_reviewed 47），
D 为 47、R 为 0、I 为 97；I 中已有当前审核 95、尚无当前审核 2；隐式 queued 为 28,409。
19 个已提交批次合计 1,520 条历史结果。表层 OK 不构成深度语境复审。

下一批保留现行 policy 排序，截取前 78 条 Tome，在固定源码身份转为 Cults snapshot 之前
收束；78 条已逐项核验固定源码（71 个字面量、7 个 entity keyword AST 字段）。
Cults 保持后续顺序；其公开源码可读，但源码 commit 未固定，不能把提取快照当作源码 pin。

## 第二批完成与 Cults 边界

`batch-5ebe7845a46cb43dfd78` 的 78 条 Tome 表层审核全部 OK，无 observation／修复项，
已提交为 `85f7d163bac4683a9e3b1b8e843ad37128eba2e7` 并 finalize。四路原始结果通过校验，
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
第二路活动摘要出现展示层分隔线，已从对应原生会话的唯一 `final_answer` 取得纯 JSON，
确认与摘要 JSON 后缀逐字相同；正式 raw 不含展示分隔符。

当前队列校验通过：S／done 1,497（surface_only 1,450；deep_reviewed 47），D 47、R 0、
I 97，其中尚无当前审核 2；隐式 queued 28,331。20 个批次共 1,598 条历史结果。

前一次 80 条预览只显示末尾两条 Cults，并非 Cults 切片总量。第二批结束后重新按实际队列
展开，下一连续源码身份切片是 **12 条 Cults**，之后才是 Orcs。两条预览没有形成预约、
task 或完成证据。12 条英文键已在实际公开源码中逐条核验；源码 repository／commit
未固定，文件哈希及行号记录在对应 source workset，提取 snapshot 不作源码 pin。

## Cults 批次完成

`batch-5a2b64013f85006dd92c` 的 12 条 Cults 表层审核全部 OK，已提交为
`cbc176b61e6bf0b6a2b5171e9a93c045caa4baf1` 并 finalize。无 observation／修复项；
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
当前队列校验通过：S／done 1,509（surface_only 1,462；deep_reviewed 47），D 47、R 0、
I 97，其中尚无当前审核 2；隐式 queued 28,319。21 个批次共 1,610 条历史结果。

下一连续源码身份切片为 48 条 Orcs（`batch-40c65c6934a3b76978ee`），重新按当前队列排序
确认与预选一致；48 条英文键已在实际公开源码中逐条核验，源码 repository／commit 未固定。
本会话恢复后新增 170 条 surface_only；不把这些结果提升为 deep_reviewed。

## Orcs 批次完成

`batch-40c65c6934a3b76978ee` 的 48 条 Orcs 表层审核全部 OK，已提交为
`7fa8170187329f95e5b61916c4299f7738c1cfc3` 并 finalize。无 observation／修复项；
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
当前队列校验通过：S／done 1,557（surface_only 1,510；deep_reviewed 47），D 47、R 0、
I 97，其中尚无当前审核 2；隐式 queued 28,271。22 个批次共 1,658 条历史结果。

恢复后四批新增 218 条 surface_only。下一批为 `batch-d0aae8bccea8e7c67418`，按现行排序
取前 80 条 engine／boot／Tome，均共享固定引擎源码身份。65 个字面量和 15 个由提取器
生成的关键词、类别及外观分类键已核验；生成键同时记录固定 extractor commit 与转换规则。

## 第五批完成

`batch-d0aae8bccea8e7c67418` 的 80 条 engine／boot／Tome 表层审核全部 OK，已提交为
`a5784784d17811ff39bfff8b5b59d4e75db08595` 并 finalize。无 observation／修复项；
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
当前队列校验通过：S／done 1,637（surface_only 1,590；deep_reviewed 47），D 47、R 0、
I 97，其中尚无当前审核 2；隐式 queued 28,191。23 个批次共 1,738 条历史结果。

恢复后五批新增 298 条 surface_only。下一连续源码身份切片为 8 条 Tome，
`batch-d960f8e6ecea55faff81`；随后才进入 Ashes snapshot。8 条固定源码依据已核验，
其中 `spell` 是 newTalentType 的 type 字段经固定提取器去除斜线后缀生成的类别键。

## 第六批完成

`batch-d960f8e6ecea55faff81` 的 8 条 Tome 表层审核全部 OK，已提交为
`76cce397caa81d66e85710a2e6e0d35017b578e3` 并 finalize。无 observation／修复项；
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
当前队列校验通过：S／done 1,645（surface_only 1,598；deep_reviewed 47），D 47、R 0、
I 97，其中尚无当前审核 2；隐式 queued 28,183。24 个批次共 1,746 条历史结果。

恢复后六批新增 306 条 surface_only。下一连续源码身份切片为两条 Ashes，
`batch-7aa51896d7e8e541699e`；两条均已核验实际公开源码，源码 repository／commit 未固定。
按 n<=3 的既有 surface 契约采用单个 full reviewer；仍须完成原始结果校验、归档、
`DONE_VERIFIED`、导入／裁决、完整门禁、本地提交和 finalize，之后按排序继续 Cults 切片。

## 第七批完成

`batch-7aa51896d7e8e541699e` 的两条 Ashes 表层审核全部 OK，已提交为
`44e8918f8c6d80bee64ceda6bc4b69bce1c8cff6` 并 finalize。无 observation／修复项；
单个 full reviewer 已确认归档，审核记录 `DONE_VERIFIED`；17 项完整门禁及严格 addon build
全部通过。当前 S／done 1,647（surface_only 1,600；deep_reviewed 47），D 47、R 0、I 97，
其中尚无当前审核 2；隐式 queued 28,181。25 个批次共 1,748 条历史结果。

恢复后七批新增 308 条 surface_only。下一连续源码身份切片为 9 条 Cults，
`batch-ba4a4d4e67a706e96fe2`；已按当前队列重新确定边界，全部英文键在实际公开源码中
逐条核验并冻结文件哈希和行号。源码 repository／commit 未固定，提取 snapshot 不作为
源码 commit。按既有契约派发四个分片 lane，最多同时运行三名 child；完成后继续排序队列。

## 第八批完成

`batch-ba4a4d4e67a706e96fe2` 的 9 条 Cults 表层审核全部 OK，已提交为
`5a5249c3180678ba3cf6281fba5c3e7d96f53e57` 并 finalize。无 observation／修复项；
整组 `DONE_VERIFIED`，四名 child 已确认归档；17 项完整门禁及严格 addon build 全部通过。
当前 S／done 1,656（surface_only 1,609；deep_reviewed 47），D 47、R 0、I 97，
其中尚无当前审核 2；隐式 queued 28,172。26 个批次共 1,757 条历史结果。

恢复后八批新增 317 条 surface_only。下一连续源码身份切片为 18 条 Orcs，
`batch-7e79a3c546be1764cef2`；已按当前队列重新确定边界，全部英文键在实际公开源码中
逐条核验并冻结文件哈希和行号。源码 repository／commit 未固定，提取 snapshot 不作为
源码 commit。继续采用四个分片 lane、最多三名同时运行的 child，完成后按排序继续。
