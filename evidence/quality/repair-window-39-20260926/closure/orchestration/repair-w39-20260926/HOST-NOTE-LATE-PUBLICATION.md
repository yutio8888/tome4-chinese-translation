# 复审记录事后补发（窗口 39）

窗口 39 各轮复审 harvest、边界审计、归档确认均按时完成，但每轮之后漏跑了 `publish.py`，`.ai/reviews/repair-w39-20260926/` 只有 raw 输出、没有 stage 记录。FINAL f9a2 通过后宿主一次性补发 14 条记录（r0a1、r1a1、r2a1、r3a1、r4a1、r5a1、f5a2、r6a2、f6a4、r7a1、r8a1、f8a2、r9a1、f9a2）。

补发沿用 `publish.py` 的全部校验：归档已确认、lifecycle=archived、output_valid、read_boundary_valid、raw 字节经 `validate_result_bytes` 对各自冻结 envelope 重新校验、candidate_identity 三方一致。唯一省去的是「当前译文哈希等于 STATE」断言——该断言只在复审当时成立，事后必然失败；各 stage 的译文由其 envelope 的 candidate_identity 绑定。无效尝试 r6a1、f6a3 不发布（见 INVALID-*.json）。

记录时间：2026-09-27T00:03:35.598240+00:00
