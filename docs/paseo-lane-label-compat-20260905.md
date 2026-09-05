# Paseo lane label compatibility repair（2026-09-05）

本次仅修复 contextual-v2 与 surface-v1 的创建 `labels.lane_index` 比较。两处共用
`_creation_lane_label_matches`，接受 JSON 整数 1..4 或精确 ASCII 字符串 `"1"`..`"4"`，
并匹配原有 numeric lane index；显式拒绝 bool、float、null、缺失、错 lane 及非精确字符串。
checker 不改写持久化 labels。dispatch、pointer、record、manifest 的数值字段校验未放宽。

变更文件：`tools/ai_state_check.py`、`tests/i18n/test_ai_state_check.py`、
`docs/paseo-translation-context-review-v2-contract.md`、
`docs/paseo-translation-surface-screen-v1-contract.md` 及本报告。
两份契约仅补充传输表示兼容说明，无版本升级；identity 公式、terminal predicate、
分组、重试、provenance、独立性及源码范围均未变。

验证结果：

- `PYTHONPATH=tools:. python3 -B -m unittest tests.i18n.test_ai_state_check`：131 tests，PASS。
  复用现有 file-backed fixture builders，验证两份契约的完整终态接受全部四个字符串／历史
  整数 labels 且不改写 STATE；覆盖 malformed／missing／错 lane 的拒绝、dispatch／record／
  manifest indices 不接受字符串，并单独验证 contextual lane pointer 的数值绑定。
- `python3 -B tools/paseo_contract_check.py`：PASS，10 active documents、4 live versions、
  16 clause declarations。
- `git diff --check`：PASS；本新增报告另经 `git diff --no-index --check` 检查，无空白诊断。

计划偏差：无。未解决实现问题：无。未运行生产批次或完整 gate；按 SPEC，独立 paired
REVIEW／FINAL_REVIEW 后的完整 `tools/ci-gates.sh`（含 build）、DONE_VERIFIED 与提交由宿主执行。
未修改 orchestration records、fixture identities、译文、术语或既有 frozen source evidence；
未 stage、commit、push 或创建 child。无新增长循环，无需性能探针。
