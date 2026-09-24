# 修复窗口 27 发布记录

窗口 27 覆盖审核第 273–277 批确认的 28 条问题，现已全部修复。主游戏源码依据固定 commit
`624a67329fe2ad440c5b344785a9c73fcf22ae63`；Ashes of Urh'Rok 仅固定并核验了相关源码文件的
SHA-256，源码仓库与 commit 未固定。

## 复审与裁决

- 初轮有效复审结果为 26 OK / 2 ISSUE。
- 第一次修复后，F1 为 26 OK / 2 结构 ISSUE。
- 第二次修复后，R2 为 27 OK / 1 免疫率 ISSUE。
- 最终修复后，F2 为 28 OK。
- 另有一次 reviewer 尝试因输入身份格式无效而未被采纳；其失败回执与生命周期证据均保留。

宿主在闭合期间修正了证据验证器中的旧断言，并对最终复审记录坐标作了勘误；原始失败回执没有
删除或覆盖。完整门禁 17 项全部通过，其中包含严格构建；任务状态达到 `DONE_VERIFIED`，参与本窗
实现与复审的全部 executor/reviewer 均已归档。

## 发布身份

- 译文提交：`defcc44d6d01a1329d83b37b0dcbb83c56e4b631`
- 新 catalog：`cdc76147d080c57a246273344897b397c53eded5051d701a3d7974dcb1f9e0f8`
- migration：`b8289b4f700157310fc4a583dab34cbd726be7c2a55895b4d24a942b607f8c63`
- catalog 变更：28 个 revision changed，29800 个 unchanged，0 ambiguous，0 unmapped。
- migration 生成 28 个 successor；这些 successor 必须重新审核，不继承旧 revision 的 done 状态。

## 证据索引

- 冻结编排快照：[`orchestration/`](orchestration/)
- 快照清单：[`orchestration-pack-manifest.json`](orchestration-pack-manifest.json)
- 发布附件：[`publication/`](publication/)
- 实施记录：[`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- 实现验证：[`VALIDATION.json`](VALIDATION.json)

本 publication child 完成本记录与证据安装后，仍待宿主确认归档。宿主后续还需提交本窗证据、执行
关闭后的 queue rebuild 并 push；本文不提前宣称这些宿主动作已经完成。
