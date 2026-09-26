# 窗口33门禁第一次运行

第一次 `tools/ci-gates.sh`：16 项 PASS，仅 05-production-shadow-surface-ledger-tests FAIL，原因是
`tests.i18n.test_projection_cache.RetentionAndConcurrencyTests.test_concurrent_same_key_publication_is_atomic`
得到 `[False, True, True, True]`（547 个测试中唯一失败）。该测试验证四个并发写入者同键发布的原子性，与译文改动无关。

有界诊断：宿主单独运行该测试 5 次，5/5 OK；工具与测试文件自 d6dc518e 起未改。判定为并发门禁负载下的计时抖动，
第一次运行的日志与计时移到 `gates-attempt-1/`，随后完整重跑门禁。
