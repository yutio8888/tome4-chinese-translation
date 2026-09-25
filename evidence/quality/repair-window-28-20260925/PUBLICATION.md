# 修复窗口 28 发布记录

窗口 28 覆盖审核第 278–280 批确认的 24 条问题，现已全部修复，且修改均位于
`tome-ashes-urhrok.lua`。Ashes of Urh'Rok 仅固定并核验了相关源码文件的 SHA-256，源码仓库与
commit 未固定；主游戏源码固定 commit 见冻结 manifest。

## 复审与裁决

- 复审历经 7 个 cycle 收敛。多轮 FINAL 在长 lore 条目中持续发现旧译措辞问题，宿主对长条目逐句
  预检后合并修复；最终 `FINAL_REVIEW` cycle 7（`f7a1`）为 24/24 OK。
- 用户明确授权 reviewer 写入 `/tmp`、追加 cycle，并要求“持续修复直到 FINAL 同意”；授权原件见
  [`publication/`](publication/) 中的 `USER-AUTH-*.json`。
- `f2a1` 因覆盖不全、`f6a1` 因 JSON 前带导语而无效，均按重试规则处理且未被采纳；无效尝试及
  失败回执保留在冻结编排快照中。
- 坐标勘误把 cycle 3、4、5、7 的 FINAL 记录逻辑 attempt 从 1 改为 2。该勘误经用户明确同意，
  原件保留；原 DONE 失败回执也未删除或覆盖。

完整门禁 17 项全部通过，其中包含严格构建；任务状态达到 `DONE_VERIFIED`，参与本窗实现与复审的
全部 executor/reviewer 均已归档。

## 发布身份

- 译文提交：`483ca8ace3cf3b69d26fb61e08a640b0133435a1`
- 新 catalog：`14da6ac25310ff098f018e62cd3b4cbf7fffa94762152c21a94c7705882c9f0f`
- migration：`a5e902a351ff3790162775e8280e90503f4e7d0a07b67c76820f6312276d0f0e`
- catalog 变更：24 个 revision changed，29804 个 unchanged，0 ambiguous，0 unmapped。
- migration 生成 24 个 successor；这些 successor 必须重新审核，不继承旧 revision 的 done 状态。

## 证据索引

- 冻结编排快照：[`orchestration/`](orchestration/)
- 快照清单：[`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)
- 发布附件：[`publication/`](publication/)
- 实施记录：[`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- 实现验证：[`VALIDATION.json`](VALIDATION.json)

本 publication child 完成本记录与证据安装后，仍待宿主确认归档。宿主后续还需提交本窗证据、执行
关闭后的 queue rebuild 并 push；本文不提前宣称这些宿主动作已经完成。
