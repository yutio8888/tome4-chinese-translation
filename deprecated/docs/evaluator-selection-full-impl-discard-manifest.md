# 处置记录：pre-Lite evaluator selection 全量实现产物（丢弃）

> 类型：处置裁定记录（disposition record），非契约、非门禁、非 backlog。
> 记录日期：2026-08-17。
> 本文件是 [`translation-quality-evaluator-selection-lite-v1.md`](translation-quality-evaluator-selection-lite-v1.md)
> §6.2 所指"独立的 hash-preserving archive／cleanup 任务"的执行记录。

## 一、裁定

采用 Selection-Lite v1 之前写就的全量实现产物**全部丢弃**，不进入版本控制、不移入
`archive/`、不作为 Lite 实现的依据或起点。本文件保留其精确身份（路径、行数、SHA-256），
以便未来若触发完整协议的 escalation 条件时，可以确认某份重建产物是否与当时的历史字节一致。

丢弃而非归档的理由：

1. Lite SPEC §6.2 已明确这批内容属于"仅回收概念"与"不得原样复用"两类，没有一项被批准原样
   进入 Lite；保留文件只会让全量假设经由复制或改名悄然回流。
2. `tests/i18n/test_quality_selection.py` 会被测试收集器发现并实际参与门禁（28 tests），
   使一批未被采纳的契约事实上获得门禁地位。
3. 这些文件从未提交，仓库历史中不存在它们；把 1,459 行未采纳实现新增进 `archive/` 属于为
   已延期的设施付出持续维护成本，与 roadmap §7「明确暂缓」相悖。

## 二、被丢弃文件的身份（丢弃前工作树字节）

| 路径 | 行数 | SHA-256 |
|---|---|---|
| `tools/i18nlib/quality_selection.py` | 825 | `dc96b568d0e3fe223e5b384f540766a87a2f859e5a8e02fd67a151129376ea0c` |
| `tests/i18n/test_quality_selection.py` | 634 | `7f5a7b877b7484d1cac798ec0150872e9f4b96079dba3cff7920312e7b8666af` |
| `i18n/quality/selection/protocol-v1.json` | 162 | `abe31cec788f16816086e70940b80eebb4273cc69d1f1d29faf19257fe4a6368` |
| `i18n/quality/schemas/evaluator-selection-protocol-v1.schema.json` | 189 | `e01edde7a901118e4b8ee7d9a305e616d48948c57372411ae965c2c7ad834cc8` |
| `i18n/quality/schemas/evaluator-selection-execution-preregistration-v1.schema.json` | 110 | `b4b83a9f60ae506678f4a21307531001dcf0ebbe523a941cb8b5f04372e63777` |
| `i18n/quality/schemas/evaluator-selection-sampling-preregistration-v1.schema.json` | 70 | `144f7fd1b32a1b36738efffda160900614b2b35f8232cc8fea8a1b6c64235963` |
| `i18n/quality/schemas/evaluator-selection-sample-commitment-v1.schema.json` | 29 | `afb3ee2b3605ab802f69246abcc08653f8bb3089e323fa3eefd85f5652ae3cd2` |
| `i18n/quality/schemas/evaluator-selection-assessment-v1.schema.json` | 79 | `b38332655f9755ff0aa015fc1eb1c52a34df9fb0b9ff8091020606de18c8e9ee` |
| `i18n/quality/schemas/evaluator-selection-result-v1.schema.json` | 57 | `02539ed59d542ce3040aa15b2120c784ff7f61abc6d97876d4d0674508daa4f7` |
| `i18n/quality/schemas/evaluator-selection-run-manifest-v1.schema.json` | 83 | `8afc821346d7aea4dccd50acc9c2d65e9df4f836308ea688e71d00fe1d683996` |
| `i18n/quality/schemas/evaluator-selection-report-v1.schema.json` | 72 | `3afcf8976e60f81eab983a9266801ca73ff5f440005cbb31f30f371be18f7e3b` |

`i18n/quality/selection/` 目录随之删除。

## 三、一并回退的文档登记

`i18n/quality/README.md` 中登记上述产物为既有契约资产的两处改动同时回退：

- 契约表中 `selection/protocol-v1.json` + `evaluator-selection-*-v1.schema.json` +
  `tools/i18nlib/quality_selection.py` 的表格行；
- 「边界」小节中关于 "evaluator selection contract foundation 为离线资产" 的段落。

回退理由：这些文字宣称仓库中存在 8 份 evaluator-selection 契约资产，而该批资产已按本文件丢弃。
同一次改动中属于 Task A 的运行时身份 stale 修复（第 3 项 "第二 evaluator 未定"）予以保留。

## 四、不受影响的内容

- [`translation-quality-evaluator-selection-v1.md`](translation-quality-evaluator-selection-v1.md)
  继续是 `design-reference / full protocol deferred` 的升级规范；本次丢弃不改变其状态，
  也不使其变成 backlog。
- Lite SPEC 本身不因本次丢弃获得实现授权；是否进入 IMPLEMENT 仍受其 §9 成本闸门约束。
- 历史 v1/v2/v3 契约、Facts 研究 artifact、`dataset-registry-v1` 与任何既有
  assessment/adjudication/report 均未触及。
- `purpose=evaluator_selection_v1` 保持 inactive。
