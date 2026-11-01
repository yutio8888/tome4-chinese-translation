# 轻量审核流程（2026-11-01 起）

用户于 2026-11-01 授权把全量审核从 release-20261013 的审计级流程改为轻量流程（方案 B）。
本文件是轻量流程的设计与操作说明；与旧流程冲突时，在轻量审核范围内以本文件为准。

## 保留什么

- **逐条对照源码核机制**：核心与引擎以 manifest 固定 commit
  `624a67329fe2ad440c5b344785a9c73fcf22ae63` 为准；三个官方 DLC 以本地公开检出为准并标注来源未固定。
- **A/B 独立双审**：A＝Opus 5.5（claude-opus-5-5），B＝GPT 6.1 Sol（codex/gpt-6.1-sol）。
  每批的全部条目同时派给 A 和 B（不再区分免 B 项，也就不需要补派 B）。
- **宿主独立裁决**：模型结论不是事实；`confirmed` 才进修复，名称题交 Gemini 4 Argon 讨论。
- **运行时键同步**：同一 (source, tag) 的所有出现必须同改。
- **门禁与严格校验**：修复目标先过 `tools/i18n proposal --strict`（`lite_review.py strict`）；
  有改动的提交跑 `tools/lite_gates.py`（2026-11-01 用户同意精简）。只改译文数据（根目录 `*.lua`、
  `terminology/*.tsv`、`evidence/lite-review/`）且 `tools/`、`tests/`、`i18n/` 与上次完整 PASS 相同时，
  只跑验证矩阵「有界译文修改」要求的检查：doctor、strict lint、语义声明登记、运行键扫描与分类、
  三项术语审计、空白检查、严格核心构建（实测约 5 s）。改动触及其他路径、工具树变化、距上次完整 PASS
  满 10 批或显式 `--full` 时，跑完整 `tools/ci-gates.sh`（含工具单测，实测约 170 s），通过后记入
  `evidence/lite-review/full-gates.json`。DLC 组件当前无法单独构建（缺固定官方基线），DLC 译文改动由
  strict lint 覆盖加载与格式；引擎组件不进 addon，同样由 lint 覆盖。

## 去掉什么

- full_review 的 successor 逐轮链、历史轮核对与投影重放（每阶段约 20 分钟）。
- 每条 lane 的 harvest／归档意向／归档确认／读取审计／自有门禁。
- 因格式细节（JSON 前导语等）整条作废重派：宿主取出结果中的 JSON 值即可，内容不完整才重派。
- SPEC／PLAN／SCOPE／STATE 等任务文件与 DONE_VERIFIED 闭合谓词。

## 账本

- 旧证据 `evidence/full-review/release-20261013/` 冻结在 R296（提交 fab80aa3），原样保留、不改写。
- `evidence/lite-review/seed-R296.json`：R296 时 A／B 有效完成的单元及其 revision，作为起点。
- `evidence/lite-review/batches/NNNN/`：每批的输入、A／B 原始结果、宿主裁决。
- `evidence/lite-review/ledger.jsonl`：每个已审单元一行（unit、revision、A/B 结论、裁决、批次）。
- 单元以 (component, section, source, source_tag) 标识；revision 另含 target、args_order、special。
  译文改动后 revision 变化，该单元自动回到待审，下一批重审。

## 每批步骤

1. 选批：按文件顺序取下一组未审单元，至多 80 条，小文件可合并。
2. 生成输入：每条附 section、源文、译文、tag 及源码位置提示，由工具自动定位。
3. 并行派 A、B（Paseo），完成后取最终 JSON。
4. 宿主逐条核对 ISSUE 的源码证据，写裁决；确认项直接修改译文，并同步同键条目。
5. 有译文改动时跑 strict proposal 与 `tools/lite_gates.py`；然后一次 git 提交（账本＋译文）。
6. 改过的单元在下一批自动重审。

## 进度

`python3 -B tools/lite_review.py status` 报告：当前单元总数、已审（A）、已审（B）、待审。
最终分母、补充行分类与游戏验收仍在全部条目审完后单独进行。
