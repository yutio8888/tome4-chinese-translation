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
3. 并行派 A、B（Paseo），完成后从各 lane 写出的结果文件收取 JSON；最终回复只是一行摘要（2026-11-01 用户要求，减少宿主上下文）。
   2026-11-01 曾在每批派发前等待 3 分钟以放慢 Claude 额度消耗；2026-11-02 用户确认额度正常后取消（`LITE_DISPATCH_GAP` 默认 0 秒，需要时可再设为 180）。
4. 宿主逐条核对 ISSUE 的源码证据，写裁决；确认项直接修改译文，并同步同键条目。
5. 有译文改动时跑 strict proposal 与 `tools/lite_gates.py`；然后一次 git 提交（账本＋译文）。
6. 改过的单元在下一批自动重审。

## B 补审（2026-11-02 至 11-03，已完成）

旧流程中免 B 的 4,450 个名称类单元原先只有 A 结论。用户 2026-11-02 要求补做 B 审：
`lite_review.py prepare BATCH --lane B` 只选 A 已在当前 revision 审过、B 未审的单元，输入记 `"lanes": ["B"]`，
只派 B；`record` 按输入的 lanes 记账。裁决、修复与提交与普通批次相同，改过的单元回到 A／B 双审队列。
第 0255–0312 批完成补审；`status` 的 `pending_B_backfill` 归零后不再需要 `--lane B`。

## 宿主裁决的现行补充规则

- **英文与实现不符**（用户 2026-11-02）：译文按源码实际效果改写，证据写源码行并注明 upstream text differs；
  占位符必须保留，错误在传给占位符的数值本身时（如显示值与实际伤害不同）译文无法纠正，记 advisory。
- **自拟名称**（物品、神器、技能、效果名等）：按常驻规则交 Gemini 4 Argon（`pi/opencode-go/gemini-4-argon`，
  thinking high，经 `mcpcall.py create_agent`；antigravity 通道曾 OOM，勿用）。连续批次中不逐条停下：
  当批记 advisory 并入队（`tools/lite_queue_names.sh`），攒够一轮后交 Gemini，宿主做双向撞名检查，
  再开维护批执行。与库内既有译名、术语表 preferred 不一致的客观错误当批直接改。
- **维护批**：不经 A/B 的成批改动（命名轮、按实现改写、用户裁决）写
  `batches/NNNN/maintenance.json`（授权、改动清单、未改项与理由），随后由 `lite_close.sh` 提交；
  改过的单元下一批自动进入 A/B 复审。
- 运行时键 (source, tag) 在所有组件文件（含 `engine.lua`、`mod-boot.lua`）同改；修复对照整句；
  改写前比对英文原文的换行数。

## 驱动脚本（2026-11-03 收入 `tools/`）

| 脚本 | 作用 |
|---|---|
| `tools/lite_dispatch.sh BATCH` | 派 A、B（`LITE_LANE=B` 只派 B），等待、收取、归档 |
| `tools/lite_close.sh BATCH NEXT "subject" "body"` | 门禁（有译文或工具改动时）、提交、标记完整门禁、经 `tools/push_github.sh` 推送；NEXT 非空时 prepare 并派发 |
| `tools/lite_loop.sh START [N]` | 无 ISSUE 的批自动记账、提交、派下一批；有 ISSUE 时以退出码 2（NEEDS-ADJUDICATION）停下 |
| `tools/lite_queue_names.sh BATCH` | B 补审批的 ISSUE 全是自拟名时：入队、记 advisory、收口并继续循环 |

环境需导出 `PASEO_AGENT_ID`（当前编排者）与 `TOME_PASEO_WORKSPACE`，并 `unset I18N_FULL_REVIEW_CACHE OLDPWD LANES`；
脚本自行去掉 PATH 中的 `/opt/agents/bin`。有 ISSUE 的批：读 `batches/N/{input,A,B}.json`，核源码，改译文，
写 `decision.json`，依次跑 `tools/scan_runtime_collisions.py`、`lite_review.py strict N`、`lite_review.py record N`，
再在后台运行 `lite_close.sh N N+1 ... && lite_loop.sh N+1 20`。队列空时 `lite_close.sh` 在 prepare 处报
`nothing pending`，循环以 CLOSE-FAIL 结束，属正常收尾。单条 lane 因模型满载报错时：确认已归档，把该 lane 的
`/tmp/lite-review/N/*-LANE*` 移到 `attempt-1-LANE/`，用 `LITE_LANE=<lane> tools/lite_dispatch.sh N` 重派；
继续循环前若原批是双审批要 `unset LITE_LANE`。

## 进度

`python3 -B tools/lite_review.py status` 报告：当前单元总数、已审（A）、已审（B）、待审。
最终分母、补充行分类与游戏验收仍在全部条目审完后单独进行。

### 2026-11-03 状态

当前 29,545 个 release-required 单元 A、B 全部覆盖（`status`：`pending_A` 0、`pending_B_backfill` 0），
第 0001–0316 批，账本 22,533 行（ok 21,580、confirmed 854、advisory 70、rejected 29），维护批 7 个
（0238、0241 按实现改写；0247、0250、0313、0315 命名；0252 组外发现核实）。最终分母、补充行分类与游戏验收仍未做。
