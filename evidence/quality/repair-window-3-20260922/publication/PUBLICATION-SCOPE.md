# 修复窗口3出版阶段范围补充

本阶段由新鲜 EXECUTOR execute-04 唯一写入任务内容，属于既有SPEC已授权的确定性出版。译文已提交254ad2b418e2660a1dd5c967889691c24925e6cb，不得再修改。

允许文件：handoff.md；evidence/quality/repair-window-3-20260922/ 下新增归档和说明；evidence/production-review-v2-lite/catalog/{entries.jsonl,exclusions.jsonl,manifest.json}；evidence/production-review-v2-lite/migrations/5dccee54c4aed46e7b80f17a523eb61d9058add7926f7e292ba5eb45350ad0bf.json；i18n/quality/production-review-v2-lite/catalog-v1.schema.json 和 policy-v1.json。

catalog/schema/policy只能逐字节安装已核验候选目录 .artifacts/i18n/repair-window/window3-20260922-candidate-catalog/ 下对应相对路径，不得编辑字段。migration只能逐字节复制 .artifacts/i18n/repair-window/window3-20260922-migration.json。已存在且相同的文件不用改写。任务证据保留既有历史，不覆盖不同字节。

禁止修改Lua、术语、规则、工具、其他证据或.ai；禁止stage/commit/push、调度agent。原始producer执行结果和每步计时必须忠实记录，不声称未来提交、第二次同步或push已完成。此阶段只做出版与快照回放，不重跑译文审核和完整门禁。
