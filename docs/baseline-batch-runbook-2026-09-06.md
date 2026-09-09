# 80 条基线批次审核运行手册（2026-09-06）

> 供主编排者（ORCHESTRATOR）后续阅读并继续开展 80 条基线批次审核工作。
> **新接手的 agent 请先读 §22（交接：当前状态、模型分工、待决事项）与 §23（缺陷类型学），
> 操作脚本见 [`tools/orchestration/`](../tools/orchestration/README.md)。**
> 本手册记录截至 2026-09-06 已完成的第 6、7、8 个 fill-80 基线批次
> （`batch-cab1369cd860e4cef670`、`batch-1d8c83650b49f5b4b3ac`、`batch-762830cafd3ebe687678`）
> 的完整可复现操作链，以及下一批的推进规则。正式约束以
> [`AGENTS.md`](../AGENTS.md)、[工作流](agent-workflow.md)、
> [WP2-Lite 正式方案](translation-production-review-v2-lite-plan.md) 与
> [当前交接](production-review-handoff-2026-09-05.md) 为准；本文只是操作说明，不放宽任何契约。

## 1. 背景与授权状态

- 用户 2026-09-06 指示“按照 80 一批的标准继续扩大审核范围”，并在本批进行期间要求
  撰写一份说明文档供主编排者续跑基线批次。这恢复了吞吐优化说明中“5 批最多 80 的有界
  基线”之后的**有界连续基线推进**，每批仍须完整走完门禁与 finalize；到达用户指定边界或
  停止条件即停。
- 恢复前暂停快照（2026-09-05）：S／done 2,226，D 47，R 0，隐式 queued 27,602；
  5 个 fill-80 基线批次（`batch-d6af5f1f…` … `batch-c557a49b…`）已完成 400 条 surface_only。
- 本手册对应的第 6 批 `batch-cab1369cd860e4cef670`（base `7468fb08d`）已于 2026-09-06
  完成并 finalize：80 条全 OK、12 个 lane child 全部有效并已归档、三 run 逐 run
  `DONE_VERIFIED`、evidence 提交 `792f99c`。批次用时 1186.9 秒（约 19.8 分钟），
  速率 242.7 selected/hour；child 12、retry 0、actual_tokens unknown。

## 2. 权威入口与当前队列

- 批次结果：`evidence/production-review-v2-lite/batches/<batch_id>/`
- 源码工作集：`evidence/quality/production-batches/<batch_id>-source-workset.json`
- 运行时队列：`.artifacts/i18n/production-review-v2-lite/queue.sqlite3`（可重建投影）
- 活动批次 checkpoint：`.artifacts/i18n/production-review-v2-lite/active-batch.json`
  （无活动批次时不存在）
- 每批开始前必须先重放：`python3 -B tools/i18n production queue check`；
  HEAD 变化后如需重建用 `queue rebuild`（仅在无活动 checkpoint 时）。
- 当前（第 8 批 finalize 后）：S/done 2,866（surface_only 2,819；deep_reviewed 47），
  D 47、R 0、I 97、隐式 queued 26,962。数字是快照，实际以 `queue status --json` 为准。

## 3. 每批操作步骤（可复现模板）

命令均从仓库根运行；`BATCH=<id>`、`BASE=<40-hex commit>` 为本批实际冻结值。

### 3.1 启动批次

```bash
python3 -B tools/i18n doctor                  # 工具链自检（首次或环境变化时）
python3 -B tools/i18n production batch show   # 必须 active=false
python3 -B tools/i18n production batch start --limit 80
python3 -B tools/i18n production batch show   # 记录 batch_id/phase/selected/base_commit
```

- batch 可混合来源；不得因 `fixed_source_identity` 变化截短 selected。
- selected 为 revision 数（1..80），不是文本 group 数；不得合并重复文本来超额领取。
- 记下每 run 的 task ID：多 run 时 `<batch-id>-surface-000/-001/...`；单 run 保留
  batch task ID。

### 3.2 冻结源码工作集（逐条源码核验）

```bash
# 对 80 个 entry_snapshot（batch show 输出）生成 <BATCH>-source-workset.json：
#  pinned 组件（tome/engine/boot，fixed_source_identity 形如 commit:<sha>）：
#    解析到 /workspace/t-engine4 下 public 路径（tome: game/modules/tome/... 等），
#    计算文件 SHA-256，逐行字面量匹配，记录 matching_literal_lines，
#    source_pinning=pinned, verification_status=confirmed
#  unpinned DLC（cults/orcs/ashes-urhrok，snapshot:<sha>）：
#    解析到 /workspace/tome4-dlcs/<dlc>/tome-<dlc>/ 下 section 相对路径，
#    source_pinning=unpinned，记录 provenance_note；source repository/commit 未固定，
#    提取快照不是源码 pin（doctor 的 WARN source-unpinned 属预期）
```

字段 schema 与既有 workset 完全一致（`kind=production_batch_public_source_workset_v1`、
`schema_version=1`、entries + source_verification 各 80 项）。每个 section 的 public
路径映射规则：

| 组件 | translation section 前缀 | public 根 |
| --- | --- | --- |
| tome | `mod-tome/...` | `/workspace/t-engine4/game/modules/tome/` |
| engine | `engine/...`（含 `engine/modules/boot/...`） | `/workspace/t-engine4/game/engines/default/` |
| boot | `mod-boot/...` | `/workspace/t-engine4/game/engines/default/modules/boot/` |
| cults/orcs/ashes-urhrok | `tome-cults|tome-orcs|tome-ashes-urhrok/...` | `/workspace/tome4-dlcs/<dlc>/tome-<dlc>/` |

字面量匹配：source 字符串出现在源文件某行即命中；80/80 命中才继续（任何
`source_file_sha256=null` 或 literal_source_match=false 都必须先归因修复）。

### 3.3 surface-export 冻结 consumer envelope

```bash
python3 -B tools/i18n production batch surface-export
```

- 在 `.artifacts/.../surface/` 生成 `run-NNN-group.json`、`run-NNN-lane-LL.json`
  （每 lane 是完整 envelope），checkpoint phase → `surface_ready`。
- 把 group、lane envelope、INPUT-DRAFT 按 consumer 期望布局落到
  `.ai/task/<task-id>/SURFACE-SCREEN-GROUP-group-NNN.json`、
  `SURFACE-SCREEN-ENVELOPE-lane-NNN-L.json`、`SURFACE-SCREEN-INPUT-DRAFT.json`
  （canonical compact JSON，无尾随换行；用 `tools/surface_screen_manifest.py check`
   验证每个 group）。
- 每 run 建 `.ai/task/<run-task>/STATE.json`（schema 5、review_only、
  `review_contracts=[translation_surface_screen_v1]`，初始
  `completed_review_contracts=[]`、`pending=[]`；DONE 检查要求完成后
  `completed==contracts`、`pending=[]`）。

### 3.4 派发 REVIEWER（独立 lane）

- 每个 lane 一个 child：`paseo run --background --provider codex/gpt-6-astra`（或等价
  可用 profile），title 记 `surface-<dispatch_id>`；labels 必须含 task_id、role=reviewer、
  purpose=translation_surface_screen_v1、candidate_identity、dispatch_id、
  lane_group_identity、lane_index、paseo.parent-agent-id=<当前 ORCHESTRATOR agent id>。
- prompt 为固定三行模板（≤800 bytes）：
  `任务：筛查 input_path 中全部冻结 entry；只报告有证据的明显错译、标记/占位符破坏、参数顺序或格式等表层问题；否则判 OK。`
  `输入：candidate_identity=…；input_path=…。全程只读；仅读该文件、其明确引用内容及 docs/paseo-translation-surface-screen-v1-contract.md 第六节；禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。`
  `输出：仅返回第六节单一紧凑 JSON；按冻结顺序恰好覆盖全部 entry 并回显 identity；首字节{、末字节}，无其他文字、Markdown 或围栏。`
- 每 run 是独立 whole-screen stage：n<=3 用 full；n>=4 用 4 lane；lane 组只能整组发布。
- 记录实际并发（当前操作配置 3），child 完成后逐 child harvest。

### 3.5 harvest / 验证 / 归档 / DONE_VERIFIED

```bash
# 每个 child：取 paseo logs 中最后一个合法 JSON 输出（首{末}）
#   落盘 .ai/reviews/<run-task>/raw-<dispatch_id>.txt
python3 -B -c "from surface_screen_result_check import validate_result_bytes; ..."  # 逐 raw 用 consumer validator
paseo archive <child-id>                                  # 立即归档
# 更新 run STATE：child_dispatches（lifecycle=archived, archive_confirmed=true,
#   runtime_observation 只录当次 live metadata）、review_records、
#   surface_evidence_binding（algorithm surface-evidence-binding/1、terminal whole_screen、
#   artifact_sha256 覆盖 draft+envelope+raw）、surface_screen_input_path、state=DONE
python3 -B tools/ai_state_check.py .ai/task/<run-task>/STATE.json --target DONE  # 必须 DONE_VERIFIED
```

### 3.6 聚合导入与收尾

```bash
python3 -B tools/i18n production batch surface-import --input <index.json>
# index: {"0": "<raw 文件路径>", ...}，refs 顺序 = run0 lanes → run1 lanes → ...
python3 -B tools/i18n production batch adjudicate --input <empty-decisions.json>   # surface-only 空裁决
python3 -B tools/i18n production batch prepare-evidence   # 生成 prospective evidence（含 17 项门禁）
cp -r .artifacts/.../prospective/evidence/production-review-v2-lite/batches/<BATCH> evidence/production-review-v2-lite/batches/
git add evidence/production-review-v2-lite/batches/<BATCH> evidence/quality/production-batches/<BATCH>-source-workset.json
git diff --cached --check && git commit -m "Record fill-80 baseline surface review <BATCH>"
python3 -B tools/i18n production batch finalize --commit <HEAD>
python3 -B tools/i18n production batch show        # 应 active=false
python3 -B tools/i18n production queue status --json
```

- `prepare-evidence` 内部已运行完整 17 项门禁（含严格 addon build，`skip_build=false`）
  并写入 gates.json；正式批次不接受 `--skip-build`。
- finalize 校验 commit parent == batch base_commit、128 MiB 预算、durable evidence 重放，
  然后移除 checkpoint 并重建 SQLite 投影。

## 4. 计时（可选，供吞吐分析）

```bash
python3 -B tools/review_phase_timing.py start --log .artifacts/i18n/timing/<BATCH>.json \
  --batch-id <BATCH> --base-commit <BASE> --selected 80 --concurrency 3 --phase source_verification
# 阶段切换 mark（prepare_dispatch/wait_reviewers/import_adjudication/gates/closure），结束 finish
python3 -B tools/review_phase_timing.py summary --log .artifacts/i18n/timing/<BATCH>.json
```

仅记录；不替代门禁或 DONE 验证。

## 5. 状态机要点与停止条件

- 七状态：queued（隐式）→ reserved → screened/deep_required → done/repair_required/blocked。
  `ISSUE` observation 进入 `deep_required`，须另建 contextual review-only 任务并按源码
  裁决后才可 repair；`OK` 只给 `surface_only` completion，不授予 deep_reviewed。
- 有活动 checkpoint 时任何 writer 操作都先恢复该 batch；不得删除 checkpoint 另开批次。
- 停止条件（AGENTS.md 与 WP2-Lite §14）：ambiguous/unmapped migration、queue 无法从
  committed evidence 重建、active checkpoint/raw/evidence identity 不一致、128 MiB 超限、
  术语库/全局策略变更需授权、门禁失败无法一次有界归因、生命周期无法确认等，交回用户。
- 本批期间未做：独立质量诊断、机械候选扫描校准、扩批（160/240）评估——这些仍是
  未授权/未执行的后续项；准备文件不算实验结果。

## 6. 下一批推进

- 完成本批交付与简报后，直接 `batch start --limit 80` 领取下一批（隐式 queued 域按稳定
  policy 排序），从 §3.2 开始重复；无需用户逐批确认（有界连续基线授权内）。
- 每批简报记录：实际 selected、来源/run 分布、child 数、重试、无效输出、确认缺陷、
  人工负担；缺失项记 unknown/未执行，不填零。
- 用户新指令（暂停/推送/停止/扩容）优先于本文默认推进。

## 7. 关键文件与产物清单

| 类型 | 路径 |
| --- | --- |
| 批次 evidence（durable） | `evidence/production-review-v2-lite/batches/<BATCH>/` |
| 源码工作集（durable） | `evidence/quality/production-batches/<BATCH>-source-workset.json` |
| run task artifacts | `.ai/task/<BATCH>-surface-NNN/`（gitignored） |
| review raw/records | `.ai/reviews/<run-task>/`（gitignored） |
| runtime surface scratch | `.artifacts/i18n/production-review-v2-lite/surface/` |
| prospective evidence | `.artifacts/i18n/production-review-v2-lite/prospective/evidence/…` |
| 计时日志 | `.artifacts/i18n/timing/<BATCH>.json` |

## 8. 本次完成记录（供主编排者核验）

- 批次：`batch-cab1369cd860e4cef670`，base `7468fb08d1129ad109d7e13770f3f74a7f37245e`，
  3 run：surface-000 Tome 54（pinned commit `624a6732`）、surface-001 Ashes 6（snapshot
  `104ad823`）、surface-002 Cults 20（snapshot `ed0b1126`）。
- 源码工作集 80/80 字面量命中；54 pinned + 26 unpinned（provenance 注明）。
- REVIEWER：12 个 lane（4+4+4），codex/gpt-6-astra，全部输出 OK 且经 consumer validator
  接受；child 全部归档确认。三 run 均 `DONE_VERIFIED`。
- surface-import 80/80 exact-union；adjudicate 空裁决；prepare-evidence 17 项门禁通过
  （含严格 addon build）；evidence commit `792f99cc5dd5c6026d0bf8e3cc3be5e8d21ea711`；
  finalize 成功；无活动 checkpoint。
- 队列增量：done 2,706（surface_only +80），implicit queued 27,122。

## 9. 第 7 批完成记录

- 批次：`batch-1d8c83650b49f5b4b3ac`，base `ea6eef3b8ab94b6e4269d87d2cf93c9f4ae1f930`，
  2 run：surface-000 Cults 22、surface-001 Orcs 58（全部 DLC snapshot unpinned）。
- 源码工作集 80/80：76 直接字面量命中；4 个 `birth facial category` 生成键
  （`Facial features`/`Special`，来自 `facial_features`/`special` 表键名）经
  `host_generated_key_verification` 记录 extractor 规则确认（extractor commit
  `bdc19d2`、行 [174,180]）。
- REVIEWER：8 个 lane（4+4），codex/gpt-6-astra，全部 OK、consumer validator 接受、
  已归档；两 run `DONE_VERIFIED`。
- surface-import 80/80；adjudicate 空裁决；prepare-evidence 17 项门禁全部通过（严格
  addon build）；evidence commit `f3c40cb94aab7ab443d75e6cdd006b9368e6e23a`；finalize 成功。
- 注意：跨批推进时 `.artifacts/.../surface/` 会残留上一批 run 文件；surface-export 只覆盖
  本批 run 编号，无妨，但提交/导入前以 checkpoint `surface` refs 为准（见 §3.3/§3.6）。
- 每批 finalize 后 HEAD 前进会使 queue meta evidence-head 漂移；下批 `batch start` 前需
  `queue rebuild`（无活动 checkpoint 时），随后 `queue check`。

## 10. 第 8 批完成记录

- 批次：`batch-762830cafd3ebe687678`，base `408c0df690cd68b2c079f7cdb5fe3271e924d1e1`，
  2 run：surface-000 Orcs 16（snapshot unpinned）、surface-001 engine/boot/Tome 64
  （pinned commit `624a6732`）。
- 源码工作集 80/80 直接字面量命中（含 UI 对话框/注册表等 boot 文本）。
- REVIEWER：8 个 lane（4+4），codex/gpt-6-astra，全部 OK、consumer validator 接受、已归档；
  两 run `DONE_VERIFIED`。
- surface-import 80/80；adjudicate 空裁决；prepare-evidence 17 项门禁通过；evidence commit
  `56f8acee3e98a5772dd44de0683dd2f241e35d7b`；finalize 成功；无活动 checkpoint。

## 11. 第 9-11 批完成记录（含 repair 与 catalog 重建）

### 第 9 批 batch-1b83e5acd0f0a73b543a（evidence cf985f1）
- 80 条 Tome pinned；1 run 4 lane；REVIEWER 全部 OK；源码 workset 80/80（含 1 条多行 tformat）。
- **2 条 confirmed**（surface+contextual 一致）：Earthen Missiles 技能描述漏 "target individually"（独立指定目标）；"open sky" 误译"晴朗的天空"（加天气语义）。adjudicate 4 obs confirmed → 2 repair_required（deep_reviewed）。
- 修复被 manifest/terminology 漂移阻断（catalog 建于 9-04，`c9a785e` 改 manifest 属性、`93aaf17` 改 TERMINOLOGY.md 说明文字 → snapshot hash 变）。
- **catalog 重建**（worktree `/workspace/tome4-catalog-repair`，分支 `repair/catalog-rebuild-cf985f1`）：
  - `authoritative-catalog build` 新 catalog `a885cdc6`；migration `07df0eca`：29,828 全 unchanged（仅 terminology_snapshot_sha256 provenance 字段变化，identity 不绑术语）→ commit 418b986 → merge bd59e9c。
- **repair**（修复后 catalog `e22c0cbf`，migration `44a1eba`：4 revision_changed）：
  - Earthen Missiles 描述 → "你可以为每个飞弹独立指定射程内的任意目标"（同键同步 dwarven-nature 副本）
  - open sky → "开阔的天空"（同键同步 tannen-tower 副本）
  - 修复 commit 667c320 → merge bd59e9c（同批）。完整门禁通过。

### 第 10 批 batch-f77b569d591bbeca6860（evidence 02b0106）
- 80 条 Tome pinned；1 run 4 lane；**1 条 confirmed**：xorn fragment 药材描述漏 "recently sentient"（曾具意识）→ 1 repair_required。
- repair（worktree `/workspace/tome4-repair-f77`，分支 `repair/f77b569d-repair`）：
  - 译文 → "它看起来和其他石头没什么两样，只不过这块不久前还具有意识，并且曾试图杀死你。"（同键同步 elixir-ingredients 副本）
  - catalog `e22c0cbf`→`a022bb9c`；migration `36de8d9`：2 revision_changed；修复 commit e8e0aba → merge eaf3dfe。

### 第 11 批 batch-4d81612fe16d8202457d（evidence 62590de）
- 80 条 Tome pinned；1 run 4 lane；全部 OK 无 ISSUE；源码 workset 80/80（1 条含 `\n` 转义源按 lessons-learned 第 12 条 unescape 后匹配）。
- surface-import 80/80 → 空裁决 → prepare-evidence → finalize 62590de。

### 队列推进（每批 finalize 后需 queue rebuild）
| 批次 | evidence commit | done | queued |
| --- | --- | --- | --- |
| 第 9 | cf985f1 | 2,944 | 26,884 |
| 第 10 | 02b0106 | 3,023 | 26,805 |
| 第 11 | 62590de | 3,103 | 26,725 |

### repair/catalog 流程要点（含 worktree）
1. repair preflight 需 live manifest/terminology == catalog 记录；漂移时先 `authoritative-catalog build` + `migration plan/check/apply`（quiescent：无 checkpoint、clean tree、queue 存在且 meta 匹配 old boundary）。
2. worktree 流程：`git worktree add -b repair/<batch> /workspace/tome4-repair-<batch> <evidence commit>`；init+rebuild queue（worktree 无 queue）；改译文（同 runtime key 多处须同步一致，否则 strict lint runtime-collision error）；strict lint；`authoritative-catalog build` 新 candidate；`migration plan/check/apply`（revision_changed = 改动 entry 数，successor 隐式 queued 不继承 done）；替换 catalog/ 三文件 + migration 到 `evidence/.../migrations/`；完整 `bash tools/ci-gates.sh`（17 项含 addon build）；commit → 主分支 `git merge --no-ff`；主 worktree `queue rebuild`；`git worktree remove`。
3. 术语/文档改动会改变 terminology_snapshot（TERMINOLOGY.md 计入 hash）——纯文档改动也会触发 catalog 漂移，注意 catalog 重建时 migration 会显示 29,828 全 unchanged（只 provenance 变）。

## 12. 复核模型分工（2026-09-06 用户指示，自第 12 批起生效）

- **常规 REVIEWER**（surface screen lane）：Paseo `claude/claude-opus-5`，`--thinking medium`。
- **交叉复核**（ISSUE 条目的 `translation_contextual_v2` 语境复核）：Paseo
  `codex/gpt-5.6-sol`，`--thinking medium`（**自第 21 批起**，用户 2026-09-06 指示；
  第 12-20 批为 `codex/gpt-6-astra` `low`）。注意 Sol 的默认 thinking 是 `low`，
  `medium` 必须显式传；派发后应从 `get_agent_status` 的 `effectiveThinkingOptionId` 读回确认。
- 判定规则不变：surface 与交叉复核**两轮一致**才可 `confirmed` 进入修复；两轮分歧记
  `advisory`，不修复，并在裁决 conclusion 中写明分歧与依据。
- **派发必须显式传 `--mode`（`auto` 或 `bypassPermissions`）**。claude provider 默认
  `default`（Always Ask）会让 child 在首次用工具时弹权限框并无限挂起，编排者只会看到
  status 长期不变。第 12 批因此需要用户手动点掉一个弹窗。reviewer 的只读语义仍由 prompt
  约束，并在 harvest 后用 `git status --short` 证明 child 未写入任何文件。

### 本次踩到的两个 STATE schema 细节

- surface INPUT-DRAFT 必须是**六键** canonical payload：`surface-export` 产出的
  `payload.workset` 只有五键，落盘前须补 `contract="translation_surface_screen_v1"`。
- `surface_evidence_binding` 恰含 `algorithm`／`task_id`／`terminal`／`artifact_sha256` 四键；
  `contextual_reviewers[i]` 恰含 `agent_id`／`candidate_identity`／`dispatch_id`／
  `input_path`／`purpose`／`role`（不含 `review_kind`）。
- child 归档后 `mcp__paseo__get_agent_status` 仍可读到 provider/model/thinkingOptionId，
  可据此补 `runtime_observation`；但仍应在归档前抓取。

## 13. 第 12 批完成记录

- 批次：`batch-a8b754e2b989f1feedf5`，base `9a707f3f`，1 run 4 lane，80 条 Tome pinned
  （`commit:624a6732`）；源码工作集 80/80 直接字面量命中。
- REVIEWER：4 lane，claude/claude-opus-5 medium，全部经 consumer validator 接受并归档；
  交叉复核 1 个 full child，codex/gpt-6-astra low，同样验证并归档；两 task 均 `DONE_VERIFIED`。
- 5 条 observation 裁决：**confirmed 2**（两轮一致）、**advisory 1**（两轮分歧）。
  - confirmed：`ingredients.lua` troll intestine 描述丢失 "appears…in some time" 的推测语气与
    时间限定；`egos/weapon.lua` entity keyword `blaze` 过译为“烈焰行者”。
  - advisory：`#GOLD#Life per level:#LIGHT_BLUE#` 译文在颜色标记后插空格——该写法在
    `mod-tome.lua` 出现数十次，属全库既定排版约定，标记与顺序完整保留；统一它属跨批次策略
    决定，超出本批授权。
- evidence commit `64769e9`；17 项门禁通过；finalize 成功。
- **repair**（worktree `/workspace/tome4-repair-a8b7`，分支 `repair/a8b754e2-repair`）：
  - troll intestine → “一截巨魔肠子。幸运的是，这只巨魔似乎已经有一段时间没吃东西了。”
  - `blaze` → “炽焰”。选词依据：`Object.lua:637-645` 把 keyword 经 `_t(key,"entity keyword")`
    译成短标签拼在已鉴定物品名后，故应为原词短对译；“烈焰”已被 `fiery` 占用，“炽焰”在
    entity keyword 内无冲突。两个 runtime key 各 2 处副本已同步。
  - catalog `a022bb9c`→`7794888d`；migration `0eccf0cb`：4 revision_changed、0 ambiguous、
    0 unmapped。完整 17 项门禁通过；修复 commit `b664eb0` → merge `eb9324d`。
- 队列：evidence head `eb9324d`，catalog `7794888d`，implicit queued 26,647。

### 可复用脚本（本批新写，置于 /tmp，未纳入仓库）

- `/tmp/freeze_ws.py <batch_id>`：从 active checkpoint 生成
  `evidence/quality/production-batches/<batch>-source-workset.json`；已含 pinned/unpinned
  路径映射、`\n`／`\t` 转义变体匹配与多行字面量回退，输出 `indent=1, sort_keys=True`。
- `/tmp/stage_surface.py <batch_id>`：把 `surface-export` 产物落成 `.ai/task/<batch>/` 下的
  GROUP／ENVELOPE／INPUT-DRAFT（canonical compact，无尾随换行）并写 `dispatch-plan.json`。

## 14. 第 13-19 批完成记录（2026-09-06）

每批均为 80 条 Tome pinned（`commit:624a6732`）、1 run 4 lane、源码工作集 80/80 命中、
17 项门禁通过。REVIEWER＝claude/claude-opus-5 medium，交叉复核＝codex/gpt-6-astra low。

| 批次 | evidence | repair merge | 裁决 |
| --- | --- | --- | --- |
| 13 `batch-6fa5a191…` | `8e39e48`（合并 `0906133`） | `43049a1` | confirmed 6、refuted 1、advisory 1 |
| 14 `batch-ab7bc44c…` | `6445a79` | `e95e559` | confirmed 2、pending 1、advisory 2 |
| 15 `batch-1e1449f8…` | `61c1b5e` | `e9683cf` | confirmed 2、pending 1、advisory 2 |
| 16 `batch-6998f500…` | `a5bf13c` | `db88296` | confirmed 2、refuted 1、advisory 1 |
| 17 `batch-bcb2332d…` | `1af5bb4` | `68e6a98` | confirmed 2、pending 1、advisory 2 |
| 18 `batch-fb66e92a…` | `8286eb2` | `d0db15f` | confirmed 5、refuted 1、pending 1 |
| 19 `batch-ebd23cb4…` | `64653f4` | `1367b4a` | confirmed 4、pending 3、refuted 1 |

### 已修复缺陷类型（供后续批次识别同型）

- **entity keyword 过译**：keyword 应是原词短对译（`Object.lua:637-645` 把它拼在已鉴定
  物品名后），不得把 ego 名的成分搬进来。已修 `blaze`→炽焰、`thought`→思维、
  `daylight`→日光、`delving`→挖掘。选词前必须确认该译名在 entity keyword 内无冲突。
- **severed / shining 一类修饰语整体漏译**：honey tree root、minotaur nose、
  black mamba head、Aeryn desc 均属此类。
- **专名被泛化或错指**：`wretchling eyeball`→"酸液树魔之眼"（全库孤立错名）、
  black mamba→"这条蛇"。判定前先 grep 该专名在库内的既定译法。
- **换行不变量破坏**：tutorial NPC desc 丢了 source 的 `\n`。target 内写 `\n` escape
  即可（与库内 `"\n顺带一提，"` 等写法一致），catalog 解码后须与 source 换行对齐。
- **别字**：`非生既死`→`非生即死`。

### 不应判为缺陷的类型（已 refuted，避免重复报）

- `arcane burst`→"奥术溅射伤害"：`combat.burst_on_hit` 经 `Object.lua:1161` 渲染为
  "Damage (radius 1) on hit"，"溅射"准确描述机制；字面直译不能推翻机制正确的既有译名。
- `yaech`→"夺魂魔"：与 yeek→"夺心魔" 配套的既定造词，库内 10 处一致。
- `luminous horror dust`→"金色恐魔的粉尘"：沿用 8276 行既定实体名。
- 无主语片段补出宿主物品名（hummerhorn wing→"翅膀"、storm wyrm claw→"这只爪子"、
  bloated horror heart→"心脏"）：指称无歧义，属二级语感，记 advisory。
- 中文句末半角标点：判据见 `translation-punctuation-convention-proposal-v1.md`，
  该文明确"待维护者批准"，批准前不得判 confirmed。
- `#GOLD#…： #LIGHT_BLUE#` 的空格：全库既定排版约定，标记与顺序完整保留。

### 待维护者决定（已置 pending，对应 revision 进入 blocked）

| 项 | 现译 | 问题 | workset 外影响 |
| --- | --- | --- | --- |
| `honey tree` | 蜜蜂树 | 字面是 bee tree | 实体名 8652 + 3 条目 |
| `Warden's Focus` | 专注守卫 | 中心词颠倒（36805 行已正确作"守卫者专注的"） | talent name 22082 + 5 处 |
| `farportal` | 远古传送门 | Far 被当作 ancient | 全仓库 83 处 |
| `Kryl-Feijan` | 卡洛·斐济 | 音节不符，「斐济」是 Fiji 固定译名 | 跨 ashes-urhrok 与 possessors 两组件 6+ 处 |
| `delving` | 挖掘／挖掘之（现状） | 两个 ego 共用该 keyword，掘具与护甲机制不同，见 §19 | keyword 2 处 + entity name 2 处 |

前四项每批都会被 reviewer 重新报出并重新裁决；授权后应另开有界 workset 一次性处理。
`delving` 一项的 revision 已因修复进入后继（非 `blocked`），只是译名取值待裁定，见 §19。

## 15. 本轮新增的操作约束（务必遵守）

1. **批次进行期间不得向 develop 提交任何东西**（含纯文档）。`batch start` 冻结
   `base_commit`；HEAD 一旦不等于它，`surface-import`／`contextual-import`／`adjudicate`
   甚至 `batch abandon` 全部报 `active batch catalog/base commit drift`，批次锁死。
   已经提交了的补救：`git checkout --detach <base_commit>` 恢复批次 → 在该 base 上完成
   evidence commit 与 finalize → `git checkout develop` 后 `git merge --no-ff <evidence commit>`。
   **不要对已推送的 develop 做 force push。** 文档更新只在两批之间的窗口做。
2. **修复前先全仓库 grep，不要只数 mod-tome.lua 内的副本**。同一 runtime key 可能同时存在于
   `tome-cults.lua`／`tome-orcs.lua` 等组件；漏改会让 `06-runtime-collision-scan` 失败。
   若已 `migration apply` 才发现，最干净的做法是 `git checkout -- evidence/.../catalog`、
   删掉刚 copy 的 migration json、删 `queue.sqlite3` 重新 `queue init`，补齐后重跑一遍
   catalog build + migration plan/check/apply，让整次修复只留一条 migration edge。
3. **子 agent 派发必须显式传 `--mode`**（claude 用 `bypassPermissions`，codex 用
   `full-access` 或 `auto-review`）。claude 默认的 `default`（Always Ask）会让 child 在
   首次用工具时弹权限框并无限挂起，编排者只看到 status 长期不变。reviewer 只读语义仍由
   prompt 约束，并在 harvest 后用 `git status --short` 证明 child 未写入任何文件。
4. **无效输出按契约 fresh retry**。第 18 批交叉复核的 `verdicts[3]` revision_key 被截断为
   50 hex，consumer validator 拒绝；归档该 child、以新 dispatch_id（`full-001`）重发，
   两次 dispatch 都要记进 STATE（失败的一次 `output_valid:false` 并写 `last_error`）。

## 16. 第 20 批完成记录（首个混合来源批次）

- 批次：`batch-7144a1b834f4da1448d5`，base `023a8d8`，evidence `dc28fc0`，修复合并 `4176b99`。
- **来源分布**：cults 62 + tome 9 + ashes-urhrok 9 → **3 个 surface run**（各 4 lane，共 12）
  与 **3 个 contextual run**。这是自第 6 批以来第一个非单一来源的批次。
- 源码工作集 80/80：77 条直接字面量命中；3 条为**宿主生成键**
  （`tome-cults/data/birth/krog.lua` 的 `Hairs`／`Facial features`／`Special`），
  按 §3.2 的 `host_generated_key_verification` 记录：extractor
  `i18n_tools/i18n_extractor.lua` 第 174-180 行，commit `bdc19d2`、sha256 已比对，
  规则 `cosmetic_options` 表键名 `gsub("_"," "):capitalize()`。71 条 unpinned DLC、9 条 tome pinned。
- 8 条 observation 裁决：**confirmed 4、refuted 2、pending 1、advisory 1**。

### 已修复（migration `cecd063b`，8 revision_changed；catalog `bde1c056`→`62d269cb`）

1. `mod-tome` `egos/digger.lua` entity name `" of delving"`→**"挖掘之"**。这正是第 18 批修
   entity keyword `delving`→"挖掘" 时记为「不在 workset 内、待其自身 revision 入队」的那条，
   本批入队后修复，keyword 与 entity name 恢复一致。**这条验证了「先修 keyword、把配对的
   ego 名留给它自己的 revision」这一处理方式确实会闭合，不会永久留半修状态。**
2. `tome-cults` `writhing-body.lua` 禁用提示片段：源片段经 tformat 填入
   `"Your tentacle hand currently has those stats%s:"` 的 `%s` 位、其后紧跟冒号，故源刻意不带
   句末标点；本库宿主串译文以全角「：」结尾，而原译在 `#WHITE#` 前多加句号，拼接后渲染为
   「……该技能暂时被禁用。#WHITE#：」——句号紧接冒号，格式破损。→ 删去句号。
3. `corrupted_blobs.lua`：`the rest of the organism`（生物体的其余部分）被误作「其他器官」（organs）。
4. `corrupted_blobs.lua`：一条描述缺句末标点（同 section 其余 4 条均以句号收尾），
   顺带把 `of the Maggot` 对齐既定专名「巨大蛆虫」。

### refuted（新增两条「不应重复报」的类型）

- `Walrog`→「乌尔罗格」：「乌」（wū）正是 W 起首的常规音译用字；`Urh'Rok` 的既定译名是
  「乌鲁洛克」（全仓库 68 处），与「乌尔罗格」是不同字串，**不存在撞名**；本译名在
  `tome-ashes-urhrok.lua` 10+ 处一致。
- `The Maggot`→「巨大蛆虫」：带定冠词的专名，指 cults 中可进入其体内的巨型蛆虫生物，
  与作为 entity subtype 的普通 `maggot`（蛆虫）本非同一所指，「巨大」正是用来区分二者；
  库内 4 处一致。

### 作废 dispatch（如实记录）

首次派发时 staging 脚本假设单 run 且 `task_id == batch_id`，断言失败导致 `dispatch-plan.json`
未生成，4 个 child 拿到缺失 `candidate_identity`／`input_path` 的残缺 prompt。已全部
`paseo agent stop` 后 archive（其中 2 个仍在运行，需先 stop 才能归档），
`git status --short` 确认无一写入工作树；修正脚本后重新派发 12 个有效 lane。
本批 child 计数：作废 4 + 有效 12 surface + 3 contextual。

## 17. 混合来源批次的额外要求（第 20 批新增）

1. **不要假设单 run**。`surface-export` 的 `runs` 字段与 `.artifacts/.../surface/run-NNN-*`
   决定 run 数；每个 run 是独立 task，任务名取自 `run-NNN-group.json` 的
   `payload.task_id`（形如 `<batch>-surface-000`），**不要用 batch_id 拼**。
   `contextual-export` 同样按 run 切分，需要建同样多个 `<batch>-contextual-NNN` 任务。
   每个 run 各自建 STATE 并各自 `DONE_VERIFIED`。
2. **派发前对每个 lane 硬断言**：`len(candidate_identity) == 64`、`input_path` 非空、
   prompt UTF-8 ≤ 800 bytes。shell 变量取空值时 `paseo run` 不会报错，会把残缺 prompt
   直接发出去——这类失败必须在派发前变成硬失败。
3. **DLC `birth facial category` 条目是宿主生成键**，源文件里没有字面量，不要算作未命中；
   按 §3.2 与本节 §16 的 `host_generated_key_verification` 格式记录 extractor 规则与行号。
4. surface-import 的 index 顺序必须是 run0 lanes → run1 lanes → …（与 checkpoint
   `surface` refs 顺序一致）；contextual-import 的 index 顺序同理按 run 序。

## 18. 交叉复核检出率观察（截至第 20 批）

交叉复核在 `low` 档对 surface 报出的 observation 独立复现率偏低：
第 12 批 2/3、13 批 2/6、14 批 0/5、15 批 0/5、16 批 1/3、17 批 0/5、18 批 1/6、19 批 3/5、
20 批 0/8。九批合计 46 条 observation 中独立复现 9 条。
其中「非生既死」别字、black mamba 专名泛化、`daylight`／`delving` keyword 误译等
客观可判条目都曾被判 OK。目前实际起决定作用的是主编排者按固定源码的逐条独立核验。
交叉复核也确实抓到过 surface 漏掉的点（第 19 批娜迦 desc 的遮挡关系颠倒）。
是否把交叉复核提到 `medium` 属用户设定，未经指示不自行更改；本文只记录观测值。

## 19. 更正：`delving` 裁决依据有误（2026-09-06，用户指出）

**被推翻的陈述。** 第 18 批（`batch-fb66e92acfe3fba2bd4b`）对 entity keyword `delving` 的
confirmed 裁决 conclusion 写了「ego 只给 lite 与 STR/CON，无任何探测效果」。**该陈述错误**，
据此推出的「词义与机制皆不符」也不再成立。

**事实。** 固定源码 `commit:624a6732` 下 `keywords = {delving=true}` 由**两个** ego 共用：

| ego | 路径 | 效果 |
| --- | --- | --- |
| 掘具 `" of delving"` | `data/general/objects/egos/digger.lua:24-40` | `lite = 1`、STR/CON 加成 |
| **护甲 `" of delving"`** | `data/general/objects/egos/armor.lua:237-256` | **`resolvers.charmt(Talents.T_TRACK, 2, 30)`**、STR 加成、物理/黑暗抗性、`lite` |

`T_TRACK`（`data/talents/cunning/survival.lua:78`，本库 23579 行译名「追踪」）的 info 为
"Sense foes around you in a radius of %d for %d turns"，即感知周围敌人——属探测类效果。
因此原译「探测」很可能正是依护甲 ego 的 Track 而来，**不是无据增译**；我当时只核验了
`digger.lua` 就下了结论。

**归因。** 违反了 §3.2 之外的一条隐含要求：entity keyword 的裁决必须枚举**全部**引用该
keyword 的 ego，而不是只看第一个命中的文件。正确做法是先
`git grep -n "<keyword>" <commit> -- game/modules/tome | grep -v /locales/` 取全集。

**维护者裁定（2026-09-06）：挂 pending，不改也不回退。** 现存译文维持为 keyword「挖掘」、
entity name「挖掘之」（提交 `ed5a402`／`3153b39`），登记为待决事项，与 `farportal`／
`Warden's Focus`／`honey tree`／`Kryl-Feijan` 一同在集中处理专名与术语时裁定。

取舍备忘（供裁定时参考）：两个 ego 共用同一 keyword 与同一 ego 名，只能选一个词。

| 候选 | 掘具 ego（挖掘） | 护甲 ego（Track 追踪） | 对应原词 delving |
| --- | --- | --- | --- |
| 「探测」（原译） | ✗ | ✓ | ✗ |
| 「挖掘」（现状） | ✓ | ✗ | ✓ |
| 「探掘」 | ✓ | 部分 | ✓ |

已提交的 evidence（`adjudications.jsonl`）按不可变原则不改写，本节即为对该记录的公开更正。
**在维护者裁定前，本条不得作为「同型缺陷」的先例引用**；`blaze`／`thought`／`daylight`
三条 keyword 修复不受影响——它们各自只有单一 ego 引用，已逐一核验。

注意：该 revision 在队列中已因修复而进入 `done` 的后继，**不是** `blocked` 状态；
本条 pending 是文档层面的待决事项，与 §14 表中那些 `blocked` revision 的机制不同。

**给后续批次的规则。** entity keyword／ego 名的裁决，必须先取该 keyword 的全部 ego 引用集，
并逐个记录其 `wielder`／`charmt`／`combat` 效果；单一文件的证据不足以支撑「机制不符」的结论。

## 20. 第 21 批完成记录（首个含 full 模式 run 的批次）

- 批次：`batch-11ddff0f3efcdfe1230e`，base `6dd3333`，evidence `69737ad`，修复合并 `4770964`。
- 来源：orcs 65 + cults 14 + **tome 1**。3 个 surface run：002/001 走 4-lane，
  **000 因 n=1 走 `full` 单成员路径**；2 个 contextual run。
- 交叉复核首次使用 `codex/gpt-5.6-sol medium`，独立复现 3/6，且给出 surface 未提供的机制反证
  （见下 gun 一条）。对照前九批 Astra low 的 9/46，检出质量明显提升。
- 裁决：confirmed 3 类（6 条）、pending 1、refuted 1、advisory 1。
  已修复：`Night's Star`→「暗夜之星」（单数专名被改成复数集合）、`Swordsmith`→「铸剑铺」
  （store 类别是 SWORD_WEAPON 整个剑类，「长剑」属无据收窄）、Orc Expeller desc
  「偶尔也杀杀巨人」→「不知怎的，对巨人也一样管用！」。
  pending：`stralite`→「蓝锆石」（金属档位名译成宝石名，跨 orcs+tome 8+ 处）。
  refuted：`You have %d charges.`→「叠加次数」——源码实参是 `eff.stacks`，机制上就是层数。

### full 模式（n≤3）的处理要点

契约 §3：`1≤n≤3` 用一个 `full` 成员覆盖全部 n 项，**不产出 group manifest**，
权威 artifact 是 `.ai/task/<task_id>/SURFACE-SCREEN-ENVELOPE-<dispatch_id>.json`。
因此该 run：

- staging 不能去读 `run-NNN-group.json`（不存在，且 scratch 里可能残留上一批的同名文件）；
- STATE 的 review record 必须 `review_kind="full"`、**不得含 `lane` 字段**、
  stage 成员 ordinal 为 0、entries 数在 1..3（`ai_state_check.py:1226-1237`）；
- child dispatch 的 labels 不带 `lane_group_identity`，`dispatch` 对象也不带
  `lane_group_identity`／`lane_index`；
- `input_path` 必须精确等于 `_surface_envelope_path(task_id, dispatch_id)`。

### staging 必须以 checkpoint refs 为权威（本批踩坑）

`.artifacts/.../surface/` 会跨批残留（§9 已警告）。本批首次 staging 用 glob 取 run 列表，
拿到的是**第 20 批残留的 `run-000-group.json`**，与本批 lane envelope 比对时断言失败。
正确做法：从 `active-batch.json` 的 `surface[].input_path` 反解 run 与 member 序号，
run 成员数 == 1 即 full 模式、== 4 即 lane 模式；并断言各 run entries 之和 == `len(selected)`。
`surface-import` 的 index 键必须用该 ref 的下标，不能自行编号。

## 21. 第 22-29 批完成记录（2026-09-06/07）

每批 80 条、源码工作集 80/80、17 项门禁通过。REVIEWER＝claude/claude-opus-5 medium；
交叉复核自第 21 批起＝codex/gpt-5.6-sol medium。

| 批次 | evidence | repair merge | 裁决 |
| --- | --- | --- | --- |
| 22 `batch-c939d69b…` | `15998df` | 无 | pending 1（Twilit Echoes） |
| 23 `batch-41a874b4…` | `56da671` | `99b62d6` | confirmed 3、refuted 1、advisory 3 |
| 24 `batch-b5eb9ca4…` | `730da8e` | 无 | refuted 1、advisory 2 |
| 25 `batch-e4e04b52…` | `6956d17` | `132678d` | confirmed 1、refuted 1、advisory 1、pending 1 |
| 26 `batch-21cf59e1…` | `d3b273c` | 无 | refuted 2、advisory 2 |
| 27 `batch-16bef3fe…` | `20b3a0d` | 无 | advisory 1 |
| 28 `batch-902676fa…` | `fdfca21` | `1b4cd48` | confirmed 2、advisory 1 |
| 29 `batch-09fa8053…` | `a86506a` | 无 | **80 条全 OK，零 ISSUE** |

期间另有两次授权术语修复：`db14760`（farportal／honey tree／Warden's Focus，75 revision）
与 `1b4cd48` 内的 `stralite`→斯莱特（61 revision）。

### 本段新增的形态与教训

- **第三类源码归属：interface 混入**（第 25 批）。`"#LIGHT_GREEN#Quest '%s' completed!"` 的
  section 记作 `mod-tome/class/Player.lua`，但字面量在 `class/interface/PlayerQuestPopup.lua:71`，
  Player.lua 于 31/49 行 require 并混入该 interface。按 `interface_mixin_verification` 记录。
- **零 ISSUE 批次没有 contextual run**（第 29 批），`write_states` 需容忍 ctx 文件不存在。
- **单 run 批次的 `task_id` 就是 `batch_id`**（第 23 批），不带 `-surface-000` 后缀。
- **`stralite` 的顾问讨论**（第 28 批后）：经 Paseo 交付 antigravity/gemini-3.8-flash 与
  codex/gpt-5.6-sol 各一轮，查实候选「蓝钢」已被 `b.steel` 占用、现译撞游戏自身的
  `zircon`→「锆石」。这类跨批次专名值得先做一轮多模型讨论再交用户裁定。

## 22. 交接：给接手的新 ORCHESTRATOR（2026-09-07）

### 当前状态

| 项 | 值 |
| --- | --- |
| develop HEAD | `a86506a`（= origin/develop，无未推送提交） |
| 最后完成批次 | 第 29 批 `batch-09fa8053df61f02226a5`（80 条全 OK，零 ISSUE） |
| catalog | `d3e56077` |
| 隐式 queued | 约 25,400 / 29,828 |
| 活动批次 | 无 |
| 未归档 child | 无 |

本轮（第 12–29 批）共完成 **1,440 条**，修复 30 条译文缺陷 + 4 项授权术语重命名。
每批的 evidence 与 repair 均已推送，17 项门禁逐批通过。

### 从哪里开始

读本文件 §3（可复现模板）、§15／§17／§18（操作约束）、§23（缺陷类型学），
然后用 [`tools/orchestration/`](../tools/orchestration/README.md) 的脚本直接开下一批。
脚本已通用化：身份取 `PASEO_AGENT_ID`、workspace 按 cwd 发现、源码根取 `TOME_ENGINE_ROOT`／
`TOME_DLC_ROOT`，**不要硬编码前任 agent 的 id**。

### 模型分工（用户指定，改前先确认）

- 常规 REVIEWER：`claude/claude-opus-5` `--thinking medium`
- 交叉复核：`codex/gpt-5.6-sol` `--thinking medium`（第 12–20 批曾用 gpt-6-astra low，
  检出率 9/46 偏低，第 21 批起换 Sol medium 后明显改善）
- 派发一律显式传 `--mode`（claude 用 `bypassPermissions`，codex 用 `full-access`）

### 用户的常驻授权与偏好

- **连续运行**：一批 finalize + repair + push 后直接开下一批，不问「要不要继续」。
- **回合纪律**：每轮结束时要么有在跑的后台任务，要么说明在等什么。
- 跨批次专名／术语记 pending 交回用户，但不阻塞推进。

### 仍待用户裁定的 pending

| 项 | 现译 | 问题 |
| --- | --- | --- |
| `Kryl-Feijan` | 卡洛·斐济 | 音节不符；「斐济」是 Fiji 固定译名。跨 ashes-urhrok 与 possessors 两组件 6+ 处 |
| `Twilit Echoes` | 微光回响 | Twilit 指暮光／明暗交界；技能同时处理 Light 与 Dark 伤害。**术语库 preferred 条目** |
| `delving` | 挖掘／挖掘之 | 两个 ego 共用该 keyword：掘具无探测效果，护甲却经 `charmt(T_TRACK)` 授予追踪。见 §19 |

已解决：`farportal`→远行传送门、`honey tree`→蜂蜜树、`Warden's Focus`→守卫者专注、
`stralite`→斯莱特（均为用户授权后执行）。

### 已知但不在任何批次 workset 内的同类缺陷

修复时发现、按证据纪律未动，待其各自 revision 入队时处理：

- `mod-tome.lua:38525` `"A Human warrior, clad in shining plate armour…"` —— 同样漏译 shining
- `tome-orcs/data/lore/primal-forest.lua` 的 lore 文本 —— `herbal infusions` 同样误作「草本纹身」
- `dreamer's `→「梦想家的」（4 处）与复数 keyword `dreamers`→「梦想家」—— 同 `dreamer` 的语义问题
- `" of daylight"`→「黎明之」 —— 同 `daylight` 的语义问题

## 23. 缺陷类型学（第 12–29 批实证，供快速判定）

### 应判 confirmed 的类型

- **entity keyword 过译**：keyword 经 `Object.lua:637-645` 拼在已鉴定物品名后作短标签，
  应是原词短对译，不得把 ego 名的成分搬进来。已修 `blaze`→炽焰、`thought`→思维、
  `daylight`→日光、`delving`→挖掘、`restorative`→疗愈。
  **判定前必须 `git grep` 取该 keyword 的全部 ego 引用集**（§19 的教训）。
- **修饰语整体漏译**：severed／shining／slim 等。
- **专名被泛化或错指**：`wretchling eyeball`→「酸液树魔之眼」（全库孤立错名）、
  black mamba→「这条蛇」。判定前先 grep 该专名在库内的既定译法。
- **换行不变量破坏**：target 内写 `\n` escape 即可，catalog 解码后须与 source 对齐。
- **拼接后格式破损**：片段类 source 被 tformat 填入宿主串时，多加的句号会撞上宿主的冒号。
- **别字**：`非生既死`→`非生即死`。
- **店铺／商品性质被改变**：`Sarah's Herbal Infusions` 的 store 是 `GATES_POTION`，
  译作「纹身店」会让玩家找错商店。

### 应判 refuted 的类型（已反复出现，勿重复报）

| 报告内容 | 为何不成立 |
| --- | --- |
| `X burst`→「X溅射伤害」是增译 | `burst_on_hit` 经 `Object.lua:1161` 渲染为 "Damage (radius 1) on hit"，溅射准确 |
| `massive armour`→「板甲」是术语误译 | `massive`(entity subtype)→板甲 跨 orcs+tome 既定；「重甲」另对应 heavily armoured |
| `travel speed`→「飞行速度」应作移动速度 | 这是**弹药** randart 词条，作用对象是投射物；改「移动」会与角色移速混淆 |
| `#Target# loses sight!`→「失明了」误作致盲 | 该串正是 `BANE_BLINDED` 的 on_gain，配对短消息就是 `+Blind` |
| `elemental ` 尾随空格丢失 | 中文无需分隔空格，整个 ego 名前缀家族一律不保留 |
| `Running...`→「跑步中」意为"运行中" | 四个调用点全是角色连续移动的弹窗标题，与程序运行无关 |
| `You have %d charges.`→「叠加次数」 | 源码实参是 `eff.stacks`，机制上就是层数 |
| `yaech`→「夺魂魔」无对应 | 与 yeek→「夺心魔」配套的既定造词，库内 10 处一致 |
| `The Maggot`→「巨大蛆虫」增译 | 带定冠词的专名，「巨大」用于区分独一无二的巨型生物与普通 maggot |
| `luminous horror dust`→「金色恐魔的粉尘」 | 沿用既定实体名（8276 行） |

### 应判 advisory 的类型

- 无主语片段补出宿主物品名（hummerhorn wing→「翅膀」等）：指称无歧义，属二级语感。
- 中文句末半角标点：判据见 `translation-punctuation-convention-proposal-v1.md`，
  该文明确「待维护者批准」，批准前不得判 confirmed。
- `#GOLD#…： #LIGHT_BLUE#` 的标记间空格：全库既定排版约定，本轮已出现 5 次。
- 技能提示泛化（`You cannot do that currently.`、`Death Dance`→「这个技能」）：
  调用点语境明确，且家族内部一致。

## 24. 第 30-33 批完成记录（2026-09-07，接手后第一轮）

每批 80 条、全部 tome pinned（`commit:624a6732`）、单 run 4 lane、源码工作集 80/80
直接字面量命中、17 项门禁通过。REVIEWER＝claude/claude-opus-5 medium；
交叉复核＝codex/gpt-5.6-sol medium。四批合计 320 条，**零 confirmed、零修复**。

| 批次 | evidence | 裁决 |
| --- | --- | --- |
| 30 `batch-2b114359…` | `32bd0e4` | refuted 1、advisory 2 |
| 31 `batch-49d5203d…` | `23ed40b` | advisory 1 |
| 32 `batch-f33d2bae…` | `6a6c4ea` | advisory 5（含交叉复核独立提出的 1 条） |
| 33 `batch-28513bd9…` | `8ddd953` | advisory 1 |

### 本段新增的形态与教训

- **`contextual-import` 先要求 STATE `DONE_VERIFIED`**，`surface-import` 没有这道检查。
  顺序必须是 harvest → archive → `write_states.py` → `ai_state_check.py --target DONE` →
  `contextual-import`；顺序反了报 `contextual task is not current DONE_VERIFIED bound to
  exact task/candidate/input/output`。已写进 `tools/orchestration/README.md` 的硬约束。
- **交叉复核可以对同一 revision 提出与 surface 不同的第二条 observation**（第 32 批的
  VIMSENSE_DETECT long_desc：surface 报缺句末标点、交叉复核报「看到」对 detection 精度不足）。
  此时 `_accepted_observations` 会给出两条 observation，`adjudicate` 的 decisions 必须两条都写；
  返回值里的 `adjudicated` 按 revision 计数（5 条 decision 对 4 个 revision → 显示 4），
  以 checkpoint 的 `adjudications` 长度为准。
- **两轮理由不同不算「两轮一致」**。第 32 批 ritch desc 的 `native` 重复译出
  （「原产于……干旱地区」+「土著昆虫」）是真实冗余，但交叉复核判 OK，按规则记 advisory；
  该 runtime key 另有 `mod-tome.lua:8661/39547` 与 `tome-orcs.lua:867` 三处副本，
  将来若获授权修复必须三处同步。
- **新增两个编排脚本**：`dispatch_contextual.py`／`harvest_contextual.py`，
  把此前手写的交叉复核派发与收割固化下来（含 prompt ≤800 bytes 与 identity 硬断言、
  归档前读回 provider/model/thinking）。脚本按 `AGENTS.md` 探测仓库根，可从任意位置运行。

### 新增的 advisory 判例（可直接引用，勿重复深挖）

| 报告内容 | 判定依据 |
| --- | --- |
| `Press 'm' to setup`→「按M键设置」大小写 | 引擎 `sym:=m` 有无 shift 分属 USE_TALENTS 与 SHOW_MESSAGE_LOG，大小写机制上有别；但库内大写（38477「请按P使用」）与原样（42091「按x键」）两种写法并存，统一属跨批次策略 |
| `You receive: %s`→「你收到：%s 。」多出的空格与句号 | 同键两处一致，源自带句号的姊妹条同排版；标点判据文档待维护者批准 |
| 无主语片段补出宿主物品名（`electric eel tail` 的 desc→「……的尾巴」） | 与 hummerhorn wing→「翅膀」同型，指称无歧义 |
| `luminous horror dust`→「金色恐魔的粉尘」 | 源码 `horror.lua:409 color=colors.YELLOW`，库内既定实体名 5 处一致 → refuted |

### 仍待用户裁定的 pending（沿用 §22，无新增）

`Kryl-Feijan`／`Twilit Echoes`／`delving` 三项未变；本轮新增两项跨批次**排版/术语**议题
（键位提示大小写、`detection`→「侦测」的用词统一），均记在 advisory 结论里，不阻塞推进。

---

## 25. 第 43-50 批完成记录（含两次全库规范化与一次工具链修复）

| 批次 | evidence | repair merge | 裁决 |
| --- | --- | --- | --- |
| 43 `batch-3e4971d4…` | `0c7eb87` | `7a6b4b5` | confirmed 4、refuted 1、advisory 2 |
| 44 `batch-a43dd031…` | `c860f1f` | `99763bc` | confirmed 1、refuted 1 |
| 45 `batch-ce7b903d…` | `c95b97d` | 无 | 零 ISSUE（surface-only 路径） |
| 46 `batch-0963c598…` | `1b43086` | 无 | advisory 4 |
| 47 `batch-c5377b56…` | `dd9fdc2` | `c1dbe52` | confirmed 4、refuted 1、advisory 1 |
| 48 `batch-fbe69128…` | `44f08a8` | 无 | refuted 1、advisory 6 |
| 49 `batch-861b374d…` | `8aa0eae` | `1bad3fe`（并入清理） | confirmed 2、refuted 2、advisory 3 |
| 50 `batch-a76760d3…` | 见本批 | 无 | advisory 2 |

另有两次维护者授权的全库改动：
- `0a82c8a` 专名改名：`Kryl-Feijan`→「克里尔·费扬」（23 处）、`Twilit Echoes`→「暮光回响」
  （6 处 + `terminology/talents.tsv` 的 preferred 条目）。**术语库条目必须同步，否则挂 08/09 门禁。**
- `1bad3fe` 标点/空白清理（P1–P4c，1003 个 revision）与 `_lua_string` 修复。

### 本段新增的形态与教训

- **`surface-import` 要的是「全部 lane 一次性提交」的 index.json**，不是逐个 raw 文件。
  CLI 只接受一个 `--input`，内容是 `{"<ref 序号>": "<raw 路径>"}`；序号必须覆盖 checkpoint
  `surface` refs 的全部下标。逐 lane 调用会报
  `surface result keys must be exact strings with no missing or extra keys`。
  混合来源批次（多 run）时 ref 顺序与 `raw-lane-*`／`raw-full-*` 文件名不一一对应，
  **要按 `candidate_identity` 建映射**，不要按 run/lane 编号猜。
- **`freeze_workset.py` 第六种归属形态 `dynamic_tag_sibling_key_verification`**：
  `_t(<expr>, "<自定义 tag>")` 的运行时取值来自**同目录兄弟文件**的表键。第 47 批的
  `tome-cults` 幻境城堡分支名 `left` 即此形态——调用点 `generatorMap.lua:106`，
  字面量是 `zone.lua:142` 的 `local paths = { left=…, right=…, main=… }`。
  判据：条目所属文件里存在带该 tag 的 `_t(` 调用行 + 兄弟文件里有同名表键，两处都记行号与 SHA-256。
- **同一 runtime key 可能在同一文件里登记两次**。`Physical/Spell/Mental save: ` 在
  `mod-tome.lua` 的 854-856 与 42059/42065/42066 各有一份，只改一半必挂
  `06-runtime-collision-scan`。修复前对 key 做 `grep -c` 是必须动作，不能只看 catalog 的一行。
- **`mod-example.lua` / `mod-example_realtime.lua` 不在 catalog 内，但 06 门禁会读**。
  全库替换类改动必须把它们算进去（本轮 `Kill!`、`LOW HEALTH!` 两个 key 因此同步）。
- **`_lua_string` 的长括号层级缺陷（已修）**：`tools/i18nlib/build.py:18` 原来只检查闭合串是否
  出现在内容**里**，未考虑内容以 `]` 结尾——`value + "]]"` 会拼出 `]]]`，Lua 在倒数第二个
  字符处提前闭合。此前无译文同时「含换行」且「以 `]` 结尾」，故长期潜伏；P4b 去掉一条以
  `[/b]` 结尾的多行文案的尾随换行后首次触发，表现为 `03-toolchain-unit-tests` 与 addon
  publish 预写校验失败。回归用例已加进 `tests/i18n/test_toolchain_locale_extract.py`。
  **自己写任何 Lua 字面量改写器时都要复现这条判据。**
- **改写多行 `[[ ]]` 字面量会让块内既有的行尾空白变成「新增行」**，从而触发
  `11-worktree-whitespace`。这是把 P4c（行尾空白）并进清理的直接原因。
- **多模型会诊对事实性前提有效**。给 gemini-3.8-flash / gpt-6-astra / fable-5.1 的简报里，
  我把键串字段序写成了 `sym:<键>:<shift>:<ctrl>:…`；gpt-6 与 fable 都独立查 `KeyBind.lua:146`
  的 `makeKeyString(sym, ctrl, shift, alt, meta)` 纠正为 **ctrl 在 shift 前**（已复核属实），
  gemini 未发现。**给外部顾问的简报里的「事实依据」必须标注可核验位置，并预期被推翻。**

### 新增的 advisory 判例（可直接引用，勿重复深挖）

| 报告内容 | 判定依据 |
| --- | --- |
| `Community Managers`→「社区经理」 | 中文业界通行译法，源文无区分「经理/管理员」的信息 → refuted |
| `Text Editors`→「文本编辑」 | `Credits.lua:156` title=1 后接三个人名，与 `Chinese Translators` 同构，是**职衔标题**不是软件名 → refuted |
| `try online at te4.org`→「在网站上注册」 | 同 else 姊妹分支（`Game.lua:649`）原文即 "you may also register on https://te4.org/" → refuted。**两轮都判 ISSUE 也不改变结论**，两轮均未查姊妹分支 |
| `"Online profile "` 尾随空格丢失 | `ProfileLogin.lua:30` 拼接后中文为「在线账户登录」，英文分词空格中文不需要 → refuted |
| `Manathrust`→「奥术射线」 | `spells/arcane.lua` is_beam_spell、3 级变 beam、ARCANE 伤害，机制相符；术语库 existing → advisory（丢了 mana 一层，属术语裁定） |
| `mountain troll thunderer`→「闪电山岭巨魔」 | 中心语前置/后置的命名风格，指称无歧义，本库对「X + 变体后缀」无统一判据 → advisory |

### 仍待维护者裁定的 pending

1. `delving`→「挖掘/挖掘之」——用户已裁定「保持 pending，既不改也不回退」。
2. **P2 的镜像规则**：源文句末为 `.`、译文却升格为「！」「？」，全库 63 条。
   提案只写了 P2（`!`/`?` 的语气必须保留），未写反向；本轮 P3 把这类的半角叹号
   规范成了全角，语气不符被保留了下来（第 50 批 `d329bba1` 即此例）。
3. **源文以 `.` 结尾、译文无句末标点**，全库 315 条。需先设计缩写守卫
   （`Enc.`、`Crit.` 这类补「。」是错的）才能机械处理。
4. **`without a two-handed weapon` 族的技能名泛化**：`mod-tome.lua` 9 条里 8 条把技能名
   压成「这个技能」，只有 `Crush`（26389）正确译出「压碎」。本批只有 Death Dance 进 workset，
   其余 7 条待授权或待各自 revision 进批。
5. `Birther` 的 `确定`/`接受`（源文两处均为 accept，`Birther.lua:146` 确认同一动作）、
   `ShowPurchasable` 的 `Bonus perk:`→「额外特效」（源文指附赠便携反射之镜这一福利）。
   两条证据链均完整、修复方案明确，但只有单轮提出，按 §23 记 advisory 未升级。

### 已知但未触及的同型缺陷（等各自 revision 进 workset）

`degenerated skeleton archer`（mod-tome.lua:8734）、`degenerated ogric mass`（38150）、
shining plate armour（38525）、orcs primal-forest lore 的 herbal infusions、`dreamer's`、
`" of daylight"`，以及上述第 4 项的 7 条。

## 26. pending 清偿轮与 I/S 两次全库清理（2026-09-08）

第 50 批后暂停期间，维护者逐项裁定了积压的 pending 并授权了两次全库清理。
本节记录改动、判据与新踩到的坑。

| merge | 内容 | 规模 |
| --- | --- | --- |
| `b374c55` | pending 1/2/3：P2 镜像语气、句末缺标点、双手武器技能名 | 366 条 |
| `e0d9976` | pending 2/3/4/5/6/8/9：术语对齐与语义订正 | 16 条 |
| `3a82568` | I 系列：中文正文内混入的半角标点 | 474 条 |
| `1f849ff` | S 系列：全角标点与 ASCII 空格粘连 | 524 + 14 条 |

维护者裁定「维持现状」的两项：`delving`→「挖掘之」；`tome-orcs.lua`
岩石守卫 lore 的 `herbal infusions`→「草本纹身」（与萨拉店招那条 confirmed
不同——店招上下文是 `resolvers.store("GATES_POTION", …)` 的药剂店，
lore 上下文里 infusion 与 mindstar 并列，是 `terminology/talents.tsv:9`
定义的游戏内「纹身」，原译成立）。

### 规则与守卫（可直接复用）

- **P2 镜像规则**（源文句末 `.`、译文却作「！」）：候选 63 条，实改 57。
  三类守卫各排除 2 条：源文实为 `!.`／`?.`（多余尾点，译文语气本就对）、
  源文以省略号结尾、译文把陈述句改写成疑问句（属语义问题，另行处理）。
- **句末补「。」**：候选 315 条，实改 300。守卫为**源文单 token**——
  `Enc.`／`implac.`／`invigor.`／`fortif.`／`serend.` 等 11 条缩写全部命中，
  零漏零误。省略号源文另排除 4 条。
- **I 系列**：I1 汉字紧邻的 `, : ; ! ? .` 全角化（603 处）；
  I2 译文**末尾**、跟在 `#TAG#` 或半角括号之后的 `.`（58 处，如
  `#Source#击杀了#Target#.`）——I1 的「汉字紧邻」条件抓不到这类，
  上一轮 P1–P4 也漏了；I3 只折叠刚全角化的标点后的空格。
  守卫：ASCII 省略号 87 处不按句末句点处理。
- **S 系列**：S1 全角标点后的单空格（544 处）、S2 全角标点前的单空格（194 处）。
  **守卫：只折叠单个半角空格，连续空格与制表符一律不动。**
  角色面板用空格做列对齐，折叠会破坏排版：
  `'#ANTIQUE_WHITE#弹药：      #ffffff#%d'`、`'所有伤害    ：#00ff00#%s'`、
  `'#LIGHT_BLUE#属性值：       基础值/当前值'`、
  `'#GOLD#杀死的总生物数：          #ANTIQUE_WHITE#%d'`，
  以及 tooltip 的 `\t\t` 缩进。排除 14 条 / 64 处，降级率 2.6%。

### 新踩到的坑

- **全库清扫的文件集合是「六组件 + 全部 addon 组件 + example」，不是「目录内文件」。**
  权威目录只覆盖 engine/boot/tome/ashes-urhrok/cults/orcs 六个，但
  `06-runtime-collision-scan` 读的是 `production_review_v2_lite_batch.py:199`
  列出的全部 11 个组件。S 系列首次运行漏了 `tome-possessors.lua`、
  `tome-items-vault.lua`、`tome-addon-dev.lua`，`'#GOLD#Life per level:#LIGHT_BLUE# -4'`
  在 cults/possessors/tome 三者间产生冲突而挂门禁。§25 记的
  「`mod-example*.lua` 也要算」是这条规律的特例，不要只记特例。
  addon 组件的改动只动 catalog 的 `exclusions.jsonl`（occurrence identity），
  `entries.jsonl` 逐行不变，**因此 migration 不必重做**——提交前 diff 验证。
- **`migration plan` 会在 HEAD 前进后报 `queue database meta/catalog/evidence-head drift`。**
  上一轮 apply 把 meta 的 evidence_head 固定在当时的 HEAD，一旦 commit+merge，
  下一轮就漂移。处理：`git stash` → `queue rebuild` → `git stash pop` → 重新 plan。
  `queue rebuild` 要求 tracked evidence worktree 干净，所以必须先 stash。
- **`authoritative-catalog build --output DIR` 产出的是完整仓库树**，
  catalog 三件套在 `DIR/evidence/production-review-v2-lite/catalog/` 下，
  不是 `DIR/catalog/`。
- **`migration apply` 依赖 `.artifacts/` 下的 SQLite 队列，该目录不随 worktree 走。**
  在 `git worktree add` 出来的独立工作树里跑会报
  `migration apply requires the existing SQLite queue`。全库清理要在主工作树开分支做。
- **`dreamer` 的收尾**：`08faeff` 修 keyword 时在提交信息里明确写了
  「entity name `dreamer's `（4 处）与复数 keyword `dreamers`（1 处）不在本批
  workset 内」。这类**自记的尾巴要能被后续检索到**——本轮靠
  `git log -S` 找回。修一半时务必把另一半写进提交信息。

### 待立项的残留（见 GitHub Issue）

半角省略号规范化、行中半角句点（26 条真候选）、ASCII 引号（约 88 条）。

## 27. 全库清理的强制检查表（一次事故换来的）

§26 记的「清扫集合是六组件 + 全部 addon 组件 + example」这一条，我在紧接着的
Issue #1 清理里**又犯了一次**——脚本写成 `for p in sorted(by)`（by 来自 catalog），
`mod-example*.lua` 的 `Saving game...` 没跟着改，被 `06-runtime-collision-scan` 拦下。
光把规律写进文档不够，下面这份检查表必须逐项执行。

### 事故：证据链在门禁全绿的情况下损坏

`1f849ff`（S 系列）提交时：为修 gate 06 补扫了 `tome-possessors.lua` 等 addon 组件
→ 重建 catalog → **只 diff 了 `entries.jsonl` 就认为 migration 不受影响** →
用新 catalog 覆盖了 `exclusions.jsonl` / `manifest.json`。

结果：`entries.jsonl` 确实逐行未变，但 addon 组件的改动会改变
`exclusions.jsonl` 里的 occurrence identity，`catalog_id` 随之改变，而 migration
记录里的 `new_catalog_id` 仍指向重建前的值。

**17 项门禁全部通过，问题完全没被发现**——`ci-gates.sh` 不校验 migration 与 catalog
的绑定关系，只有 `queue rebuild` 会走 `_validated_migration_edges`，报
`migration publication catalog identity drift`。等到下一次要做 migration 时才炸。

更麻烦的是**这个错误无法用后续提交修复**：校验读的是
`_migration_publication_commit` 找到的那个提交当时的 catalog，不是 HEAD 的。
最后只能改写历史——把正确的 migration 记录 amend 进 `f5373e4`、重放 merge 与后续提交、
`push --force-with-lease`（`1f849ff`+`1d3e328` → `ad7ee4e`+`520752c`）。

### 强制检查表

1. **改动源文件时，集合 = 六组件 + `mod-example*.lua` + `tome-possessors.lua` +
   `tome-items-vault.lua` + `tome-addon-dev.lua`。**
   权威目录只有六个组件，但 gate 06 读
   `production_review_v2_lite_batch.py:199` 列的全部 11 个。
   脚本里**不要**写 `for p in catalog_paths`，要写
   `for p in sorted(CATALOG | EXTRA)`。
2. **catalog 必须在所有源文件改完之后才构建。**先构建再补改文件 = 必然不一致。
3. **`migration apply` 之后、`git commit` 之前，逐项比对四个值**：
   `new_catalog_id` / `new_entries_sha256` / `new_exclusions_sha256` /
   `new_manifest_sha256` 对上 `catalog/manifest.json` 与其文件 SHA-256。
   只比 `entries.jsonl` 不够——这正是本次事故的成因。
4. **合入 develop 后立刻跑一次 `queue rebuild`。**它是唯一会校验证据链绑定的环节，
   通过了才算这批真正落地。失败必须当场处理，不要推进到下一批。
5. 若中途发现 catalog 需要重建（例如补扫了目录外组件），
   **必须整轮重做 plan/apply**：`git stash` → `queue rebuild`（回滚 meta）→
   `git stash pop` → 用最终 catalog 重新 plan/check/apply。
   直接覆盖 catalog 文件而保留旧 migration 记录，就是本次事故。

### 空格折叠的第三条守卫（第 51 批抓出的回归）

§26/§27 已记的守卫是「只折叠单个半角空格」（防列对齐被破坏）。**这不够。**
第 51 批筛查轮报出 `#YELLOW#-- 正在连接到服务器…--` 格式破坏，追查是
`f363485`（Issue #1 省略号归一）的折叠规则

    (…+)( )(?=[^ \t])

造成的回归：它只要求后继是**非空白字符**，没区分「后继是正文」与
「后继是格式性分隔符」。源文 `-- connecting to server... --` 的 `-- X --`
是对称包围格式，收尾 `--` 前的空格属格式本身——同目录 `ko_KR.lua:1191`
与上游 `zh_hans.lua:1113/1176` 都保留了它。

**守卫补充：后继为 `-` `=` `*` `_` `|` `~` 等分隔／包围类符号时不得折叠空格。**
更保险的写法是白名单：只在后继为中日韩字符、`#`（色彩／样式标签）或
`%`／`@`（占位符）时才折叠。

审计口径：全角标点后直接跟上述符号、**且源文同位置有空格**。全库真候选
只有这一个 runtime key 的 2 处，影响面封闭。注意 `，-2 敏捷` 这类
负数前的逗号是正常中文排版，不能算进来——审计正则若不加「源文有空格」
这个条件会产出数百条噪声。

### 本轮其他可复用的判据

- **Issue #2 的分类法**：行中半角句点看似高风险，按**前一个字符**归类后
  1550 处可机械排除（数字→版本号/格式符、字母→URL、`%`→`%.1f`、`.*`→正则），
  真候选只剩 26 处，零假阳性。**先按上下文特征分类，再谈假阳性率。**
- **省略号不是一族**：UI/进度提示类 28:3:0 用「…」，是**真约定**；叙事类
  497:86 用「……」。同一符号在不同语境下有不同正确形态，
  统计前先按 `section` 分层，否则会把约定当成不一致抹平。
- **引号不配对要逐条对照源文，不能靠计数补齐**：`“` 多于 `”` 与反之两种都有，
  成因是极性写反（该写 `”` 写成了 `“`）或多插一个开引号，位置各不相同。
  另有 1 条 refuted——`mod-tome/data/lore/misc.lua` 的诗节源文自身就只有一个
  未闭合的 `"`，译文是忠实镜像。**源文自身的引号缺陷不算译文缺陷。**

## 28. 第 51 批完成记录

批次 `batch-00bf6c036c8fa5651b16`，base `7f0f6a5`，80 条
（tome 67 / engine 5 / orcs 4 / cults 2 / boot 2），源码工作集 80/80 命中 0 缺口。
3 run：surface-000 四 lane 74 条、surface-001 full 2 条、surface-002 四 lane 4 条。
evidence `c477a45`，repair merge `d5fc49c`。

裁决：**confirmed 1、refuted 1、advisory 4**（surface 报 6，交叉复核 0 复现）。

- confirmed：`-- connecting to server... --` 的收尾空格丢失（见上节守卫）。
  这是**审核流程抓到主编排者自己引入的回归**，来源是同一天的 Issue #1 提交。
- refuted：`You have %d charges.`→「叠加次数：%d。」。筛查轮主张应作「充能次数」；
  固定源码 `tome-orcs/data/timed_effects/physical.lua:530` 与 `magical.lua:409`
  的实参是 `eff.stacks`——所指就是叠加层数，译法成立；上游 `zh_hant.lua:1646`
  同样作「疊加次數」。
- advisory ×4：`The rift leads... somewhere.`→「裂缝通向…某个地方。」的单省略号。
  属 Issue #1 裁定中**明确暂不统一**的叙事类既有 86 条，不是本批新缺陷。
  5 处同源串彼此一致，无 runtime 冲突。

### 本批踩到的操作细节

- **`.artifacts/.../surface/` 下会残留上一批的 `run-NNN-*` 文件。**
  本批 run-001 只有 1 个 ref 且 `group_manifest_path` 为 null（full stage），
  但目录里存在上一批留下的 `run-001-group.json` 与 `run-001-lane-01..03.json`。
  **run 的构成必须以 checkpoint 的 `surface` refs 为准，不能 ls 目录推断**，
  否则会把 full stage 误当四 lane 组，`ai_state_check` 报
  `surface lane stage must contain exactly members 1..4`。
- **`surface_evidence_binding.artifact_sha256` 必须是精确集合**：
  `surface_screen_input_path` + 每条 record 的 `input_path` 与 `raw_output_path`，
  多一个（如 group manifest）少一个都报
  `surface tasks must bind an exact surface_evidence_binding object`。
  键集固定为 `{algorithm, artifact_sha256, task_id, terminal}`，`task_id` 不可省。
- **lane 元数据取自 group manifest 的 `lane_boundaries`，不要自己算 offset**；
  同时 `child_dispatches[i]` 必须带 `lane_group_identity` 与 `lane_index`，
  否则报 `lane N record/dispatch/manifest binding mismatch`。
- **`SURFACE-SCREEN-INPUT-DRAFT.json` 是 envelope payload 的形状**
  （顶层 `contract`/`entries`/`fixed_source_identity`/`rendered_briefing`/
  `rules_version`/`terminology_snapshot`），`entries` 是该 run 全部 lane 按
  lane 序拼接的结果，canonical compact 无尾随换行。
- **`adjudicate --input` 的精确 schema**：顶层 `{batch_id, decisions}`；每条决议
  的键集恰为 `{entry_revision_identity, observation_contract, observation_identity,
  observation_sha256, disposition, evidence_path, evidence_commit,
  evidence_snapshot, conclusion, repair_required}`——**没有 `schema_version`**。
  `observation_sha256` 是 `sha256(observation 文本的 UTF-8 字节)`，
  不是整条 observation 对象的哈希。决议必须一一覆盖
  `_accepted_observations(checkpoint)`（只含 ISSUE，交叉复核判 OK 不产生 observation）。

## 29. 第 52 批完成记录与编排工具化

批次 `batch-d738009724950b3fe20d`，base `e84b164`，80 条，源码工作集 80/80 命中 0 缺口。
3 run（lane 74 / full 2 / lane 4）。evidence `9f9ad7f`，repair merge `e377b95`。
裁决：**confirmed 9、refuted 2、advisory 1**，7 条 revision 修复、50 条 revision 变更。

### 派发 prompt 引用了不存在的契约文件（一直存在的缺陷）

contextual 派发 prompt 里写的是 `docs/paseo-translation-contextual-v2-contract.md`，
**该文件不存在**——真实文件名是 `docs/paseo-translation-context-review-v2-contract.md`
（`context-review`，不是 `contextual`）。后果是交叉复核 REVIEWER 从来读不到契约第六节。
第 51 批两个 run 恰好都吐出了合法形状所以没暴露；第 52 批 full-001 自创了
`{"results":[{"decision":"rejected",...}]}` 的 schema，`contextual-import` 会拒收。

此外我此前的「任务」行是自拟措辞（"独立复核筛查轮的主张…不得复述筛查轮理由"），
与契约第六节的官方模板（"仅报有证据的实质语义、机制、术语、关系或跨条一致性问题"）不符。
**派发模板必须逐字取自契约第六节**，不要自己改写。

修正后重新派发（旧 child 归档、产物删除、不作为证据），实例 755 bytes。

### 本批固化的编排工具（`tools/orchestration/`）

前两批的失误多数出在手工步骤上，已逐个工具化并内置硬断言：

| 工具 | 作用与内置断言 |
| --- | --- |
| `stage_surface.py` | **run 构成只以 checkpoint refs 为准**（不 ls `.artifacts`，那里有上批残留）；自动识别 full stage（单 ref 且无 group manifest）；lane 元数据取自 group manifest 的 `lane_boundaries`；生成正确形状的 INPUT-DRAFT；断言总 entry 数 == selected |
| `dispatch_surface.py` | **派发时即记录 agent_id**（`paseo run --json` 的键是 `agentId`，不是 `agent_id`/`id`）；断言 identity 64 位、input_path 非空、prompt ≤800 字节 |
| `dispatch_contextual.py` | 用契约第六节官方模板；import 时 `assert` 契约文件存在 |
| `harvest_reviews.py` | 取最后一个合法 JSON；校验 identity 回显；任一 child 失败即 exit 1 |
| `build_import_index.py` | **按 candidate_identity 建映射**，不按 run/lane 编号猜 |
| `close_review_tasks.py` | 写 review record、归档 child、填 STATE、逐 run 跑 `ai_state_check --target DONE` |

第 52 批用这套工具后，5 个 run 的 `DONE_VERIFIED` 一次通过（第 51 批手工做时失败了 5 轮）。

### 本批的裁决判据

- **`profile name`→「Steam用户名」**（confirmed，两轮同因）：`ProfileSteamRegister.lua:44`
  该字段是 `c_login` Textbox（`title=_t"Username: "`、`max_len=20`、`login_filter` 只收
  小写字母数字），其值经 `okclick` 传给 `profile:performloginSteam`，**与 Steam ticket 分开传递**。
  即用户在此新建的 te4.org 账号名；Steam 用户名反而可能被过滤器拒绝。
- **`Online profile disabled`**（confirmed，主编排者核验）：`Module.lua:1156` 注释即
  `-- Disable the profile if ungood`。库内既有译法是「在线账户」「在线用户档案」，
  而「存档」在本库对应 savefile。**同一词在库内已有主导译法时，孤例即缺陷。**
- **`#GOLD#Life per level:` 前导空格**（confirmed，主编排者核验，交叉复核判 OK）：
  `chronomancer.lua:66-71` 显示它与 `#GOLD#Stat modifiers:` 是同一描述列表的并列行；
  本库兄弟行「#GOLD#属性修正：」「#GOLD#经验惩罚：」都无前导空格，唯此行有，三行并排时缩进不齐。
  **47 处横跨五个组件**（mod-tome 34 / orcs 5 / cults 4 / ashes-urhrok 3 / possessors 1）。
- **`charges`→「叠加次数」**（refuted，**两轮同因但均与源码不符**）：
  `magical.lua:406-441` 的 DEATH_MOMENTUM 里 `charges = function(self, eff) return eff.stacks end`，
  `setCharges` 按 `eff.stacks` 线性叠加 `movement_speed`/`flat_damage_armor`/`inc_damage`，
  `on_merge` 用 `util.bound(stacks+1, 1, max_stacks)` 递增，**全定义无任何消耗路径**。
  是叠加层数不是可消耗资源；「充能次数」反而误导。
  **两轮一致也不等于正确——§23 的两轮判据是升级门槛，不是免检通行证。**

## §30 第 53–54 批记录：surface task_id 规则与两轮分歧的处理

### 30.1 单 run 批次的 surface task_id 等于 batch id 本身

`production_review_v2_lite_batch.py:379`：

```python
batch_task_id = checkpoint["batch_id"].replace("_", "-")
task_id = (batch_task_id if len(runs) == 1 else
           f"{batch_task_id}-surface-{run['run_index']:03d}")
```

group manifest 的 `payload.task_id` 由此决定，而 `ai_state_check` 要求
manifest 落在 `.ai/task/<payload.task_id>/SURFACE-SCREEN-GROUP-<group_id>.json`，
且 `manifest_payload["task_id"] == state["task_id"]`。

`tools/orchestration/stage_surface.py` 原先无条件写 `<batch>-surface-NNN`，
单 run 批次就会报 **`surface lane manifest is invalid: manifest path does not bind task_id/group_id`**。
第 51、52 批都是多 run，所以这个缺陷一直到第 53 批才暴露。

已修：`stage_surface.py` 按上游同一规则算 task 名，并对
`g['payload']['task_id'] == task` 做硬断言；group manifest 路径改由 plan 的
lane 项携带（`group_manifest_path`），`close_review_tasks.py` 不再用
`task.split('-')[-1]` 反推——单 run 批次的 task 名末段是 batch id 的十六进制尾巴，反推必错。

**教训**：凡是上游工具已经算好的标识（task_id、group_id、路径），
编排脚本一律**读取**，不要**重算**。重算在多数情况下碰巧相等，只在边界情况炸。

### 30.2 P8 补句号规则的第二次回归：双句号

第 53 批表层报 `engine.lua` 的
`'……你不需要再次进行汇报。(除非你认为这一情况和之前有所不同)。'`
两个句号。`git log -S` 直接命中：全库同型 10 处，其中 3 处由本人的 `12da190` 引入。

P8「译文缺句末句号则补」的规则缺一条前置判断：**目标已有句中句号且尾随括号补充时不得再补**。
统一修复口径：**句中句号删除、句末保留**；源文本无句末句号的（如
`"You feel your rampage slowing down. (-1 duration)"`）反过来删末尾句号，保持镜像。

检出正则：`grep -Hn '。([^)]*)。\|。（[^）]*）。' *.lua`。

### 30.3 两轮报不同问题时的处理

第 53 批 `c36c46a4`（Cults 简介）：表层报实体名误译，交叉复核报专名丢失 + 程度限定丢失。
按 §23 这不是「两轮一致」，两条都只能算 advisory——但 advisory ≠ 不查。
逐条独立取证后：

- **成立**：`Nethergames`（源码唯一一处，是 `nethergate` 的笔误）「虚空蠕虫」与
  `t("nethergate","彼世之门")` 及 `nether`→「彼」的既定译法冲突；
  `horror` 作「寄生兽」与本库 `parasite` 的既定译法撞车；
  `partly insane` 的程度限定丢失。
- **驳回**：`Occult Egress`→「神秘的出口」是本库既定专名译法（`entity name` 共 5 处），
  不是「泛称化」；`Scourge Pits` 在 Cults 源码中根本没有同名区域。

第 54 批同理：表层报 `infusions`→「纹身」误译，**驳回**——「纹身」是本库
`infusion` 的既定译法（`runes and infusions`→「符文和纹身」、
`Infusion of Wild Growth`→「纹身：野性生长」、`Facial Infusions 1`→「脸部纹身1」），
且与维护者对挂起项 7 的裁定一致。

**教训**：审核方报「与游戏概念不符」时，先查**本库自己的既定译法**再查源码。
本库译法一致 ≠ 正确，但**孤立地改一条**必然造成不一致，代价大于收益。

### 30.4 维护者裁定：换行结构不作镜像归一

全库审计（30559 条）发现源/译换行数不等 **378 条**，双向都有：
源1→译2 共 48、源2→译3 共 37、源1→译0 共 34、源3→译4 共 32、
源0→译1 共 20、源3→译2 共 18……

**维护者 2026-09-09 裁定：暂不按源文镜像统一。**
今后表层轮再报「换行结构被改动」一律判 `advisory` / 不修复，不必重复取证。

### 30.5 引号约定：本库无直角引号

按 `t(...)` 条目扫描译文侧：

| 形式 | 出现 | 条目 |
|---|---|---|
| `“ ”` | 1048 / 1047 | 395 / 394 |
| `' '` ASCII 单 | 131 | 53 |
| `" "` ASCII 双 | 122 | 45 |
| `‘ ’` | 21 | 14 |
| `「」`『』 | **0** | **0** |

**本库既定约定是 `“ ”`，嵌套内层用 `‘ ’`；直角引号从未使用。**
讨论引号问题时不要写成「是否转『「」』」——正确的问法是是否转 `“ ”`。

### 30.6 维护者裁定：顶层单引号改双引号；UI 选项名不按引文处理

维护者 2026-09-09 裁定三条：

1. **换行不作镜像归一**（见 §30.4）。
2. **单引号改为双引号处理。** 落实为：**顶层**单引号（ASCII `' '` 与全角 `‘ ’`）
   一律改 `“ ”`；**嵌套在 `“ ”` 内的内层 `‘ ’` 保留**——本库 1047 处 `“ ”`
   的配套约定就是内层用 `‘ ’`，一律改双会得到 `“…“…”…”`。
   判定方式是按 `“`/`”` 计算层深自动分流，不逐条主观取舍。
3. **UI 选项名不按引文处理**，保留 ASCII（与源文 `'Always show glove combat'` 一致）。

实际改写 17 条（catalog 内 16 条 + 非 catalog 组件 possessors 1 条）。
不动的 38 处 ASCII 单引号：占位符/颜色标记/命令字面量/按键名 36 处 + UI 选项名 2 处。

### 30.7 辅助扫描器不识别 Lua 块注释——全库统计会虚高

`/tmp/lua_entry_scan.py` 用 `(?m)^t\(` 匹配条目，**不排除 `--[==[ … --]==]`
块注释里的 `t(` 行**。全库共 **251 行**这样的注释条目
（mod-tome 131、tome-cults 27、engine 24、tome-orcs 20、mod-example 20、
mod-example_realtime 19、tome-addon-dev 5、tome-ashes-urhrok 4、mod-boot 1）。

后果：本次清扫一度误改了注释块内标注 `-- untranslated text` 的
`t("#{italic}#'Meas Abar.'#{normal}#", "#{italic}#'Meas Abar.'#{normal}#", "_t")`
——该占位的语义就是 source==target，改了等于破坏占位。已回退。

**规矩**：
- 用该扫描器出的全库统计一律要注明「含注释条目」，或先按块注释区间过滤；
- 任何全库改写落盘后，必须用「改动行是否落在 `--[=*[ … --]=*]` 区间内」再验一遍；
- 权威口径永远以 `authoritative-catalog build` 的 entries/exclusions 为准——
  它正确忽略注释条目（`Meas Abar` 在新旧目录里都查不到）。

## §31 第 56 批记录：状态标签撞车、专名撞名与脚本落盘陷阱

### 31.1 状态标签撞车是可机械证明的缺陷

`-Imploding`→「-压制」被两轮同时报出。取证时发现更硬的证据：
本库已有 `t("+Overwhelmed","+压制")` / `t("-Overwhelmed","-压制")`，
两个不同状态在界面上显示**同一标签**。修复锚定同族已有译名——
`t("Implode","碎骨压制")`、`t("Imploding (slow)","碎骨压制（减速）")——
故 ± 两条改「+碎骨压制」「-碎骨压制」，消歧且不动技能名。

**方法**：报「术语译错」时，除了查源码语义，还要**反查该译名是否已被别的源术语占用**。
反向撞名（多个 source → 同一 target）门禁不查，只能靠人工反查。

### 31.2 修一处术语可能制造新的撞名

`spellblaze scar` 从「奥术之痕」改为「魔法大爆炸之痕」后，
与既有区域名 `Mark of the Spellblaze`→「魔法大爆炸之痕」
（`data/zones/mark-spellblaze/zone.lua`，一整张地图）撞名。
最终定为 `spellblaze scar`/`Spellblaze Scar`→「魔法大爆炸伤痕」（地面效果），
`Mark of the Spellblaze`→「魔法大爆炸之痕」（地图）保持不变。

**规矩**：改术语后必须 `grep` 新译名，确认没有落到别的源术语头上。

### 31.3 批量改写脚本的落盘陷阱

第 56 批修复脚本把全部替换做在内存里、循环结束才 `write_text`。
第 5 条断言失败 → 前 4 条改动**一起丢失**，而我已经开始跑跨组件检查。
是那次检查的输出（`奥术之痕` 仍在）才暴露问题。

**规矩**：
- 批量改写脚本失败后，**必须重跑全部**，不能假设「报错前的部分已生效」；
- 改完一律用 `grep` 复核每一条目标串确实变了、旧串确实没了，
  不要只看脚本打印的 `ok`。

### 31.4 句内半角逗号：I 系清理的匹配器缺口

第 56 批表层报 `护甲增加 %d, 获得` 句内半角逗号。全库复查发现
**56 处**残余（mod-tome 24、tome-orcs 15、possessors 11、
ashes-urhrok 3、cults 3）——属此前已授权的全库内部半角标点清理，
当时的匹配器漏了逗号一类。

检出式：`([一-鿿]) ?, ?(?=[一-鿿])`，只处理中日韩字符之间的半角逗号，
不触碰 `%s, %d` 一类占位符列表与代码。

### 31.5 句末句号判定规则（已执行，Fable 5.1 顾问方案 + 逐条核定）

维护者授权后，49 条候选逐条核定并执行：不动 7、纯追加句号 32、改写 5、
外加 §30.2 家族漏网 2 处。落地提交见 `style: 补齐译文缺失的句末句号`。

**house style 依据**：全库 `）。` 311 处 vs `。）` 30 处 —— 本库是明确的
「句内括号」式（GB/T 15834 的句内括号，点号放在 `）` 之后），不是句外括号式。

#### 判定算法（可被检查器实现）

前提：源文 `rstrip()` 后以单个 `.` 结尾（排除 `..`/`...`）。

```
0. 免检
   - tag ∈ {entity name, talent name, achievement name, entity type}
   - 源文无空白（单 token）：只报不改。缩写（Enc./implac./fortif./serend./
     invigor.）与单词句（Thanks./Farewell.）无法机械区分。
   - 显式豁免表（按源文 key）：Enc.、
     "Be of size category 'big' or larger. This is also required to use it."
     （前者是 width=8 列头，后者是 require.special.desc，同族 30+ 条均无句号）

1. T = tgt.rstrip()；W = tgt[len(T):]。W 原样保留，禁止触碰（§27 教训）。
2. T 末字 ∈ {。！？} 或以 …… / … 结尾              → 达标，不动。
3. T 末字 ∈ {” ’}
   a. 倒数第二字 ∈ {。！？} 或 ……                  → 达标（引文为完整句，句号在引号内）
   b. 否则（引文是术语/技能名）                     → 在 ” 之后补 。
4. T 末字 = ）或 )
   a. 「。）」且源文以 `.)` 结尾                     → 达标（独立括注句）
   b. 「。）」且源文以 `).` 结尾                     → 报「句号入括」，人工处理
   c. T 匹配 `。（[^（）]*）$` 或 `。\([^()]*\)$`     → **E1：移位**
      删掉紧贴左括号前的 。，在 ） 之后补 。。**绝不追加**
   d. 其他                                          → 在 ） 之后补 。
      半角 `)` / `).` 收尾一并转全角 `）。`
5. 其他任意字符收尾（含 %s / #TAG# / 汉字）         → 直接补 。
6. 写回 tgt = T' + W。
```

#### 后置断言（任一失败整批回滚）

- `grep '。。\|。）。\|。)。\|！。\|？。' *.lua` 命中数不增加；
- 每条的 `%` 占位符数、`#…#` 色标数、尾部空白 W 完全不变；
- 除移位/改写类外，`len(T') == len(T)+1`；
- 同一 key 跨文件多次出现的必须同步（runtime-collision 门禁）；
- 改动行无一落在 `--[=*[ … --]=*]` 块注释内（§30.7）。

#### 自动化边界

只有「纯追加一个 `。`」的四类（引号收尾术语、括号收尾、纯遗漏、句中有 `。`
但末尾非括注）将来可自动化。**E1 移位、半角转全角、括注还原为独立句，
永远人工**——E1 正是 §30.2 双句号回归的形态，机械追加必然复发。

#### §30.2 检出式的两个缺口（本次一并修好）

- `。）。`：旧式 `。（[^）]*）。` 要求 `。` 紧贴 `（`，句号落在括号**内**时漏网
  （`（……最大生命值。）。`）。检出式应补上 `。）。`；
- 源文**根本没有**句末句号、译文却有句中 `。` 的反向情形
  （`Be lucky already (at least +5 luck)` → `拥有大运气。（至少有+5幸运属性）`），
  镜像原则要求删掉。

#### 顾问机制的价值

本节方案来自 Fable 5.1 顾问的逐条分类，我逐条复核了它的每一项论据
（house style 计数、同族兄弟条目、`Enc.` 的列头来源、`require.special.desc`
同族无句号）后才执行。**它发现了两处我自己漏网的 §30.2 残余。**
在「规则已造成过自伤回归」的场景下，先请外部意见做逐条分类，
比自己再写一版启发式扫描器可靠。

## §32 第 57 批记录：匹配器缺口与「译名归属」误判

### 32.1 §31.4 半角逗号检出式的缺口

原式 `([一-鿿]) ?, ?(?=[一-鿿])` 要求逗号**两侧**均为中日韩字符，
左侧是标记或占位符时全部漏网：

- `#WHITE#, 祝贺你！`
- `t("%s, the lost warrior", "%s, 迷路的战士")` 及同族 20+ 条

补充检出式：`(#[A-Za-z_]+#|%[a-zA-Z]) ?, ?(?=[一-鿿])`，全库 28 处，已清理，残余 0。

**教训**：写标点检出式时，左右上下文不要都限定成汉字。
译文里紧邻标点的常常是 `#COLOR#` 色标或 `%s` 占位符。

### 32.2 「译名归属」误判：审核方可能搞错哪个词对哪个词

第 57 批表层报 `yeek mindslayer`→「夺心魔心灵杀手」丢失 yeek、
且把 mindslayer 重复译成「夺心魔」与「心灵杀手」。

实际本库：`yeek`→「夺心魔」（`yeek illusion`→夺心魔幻象、
`yeek psionic`→夺心魔灵能力者），`mindslayer`→「心灵杀手」。
兄弟条目 `yaech mindslayer`→「夺魂魔心灵杀手」直接佐证构词方式。
译文完全正确——审核方把「夺心魔」误当成了 mindslayer 的译名。

**方法**：报「复合词译错」时，先把复合词**拆开分别 grep**，
确认每个成分在本库的既定译名，再看合起来对不对。
不要凭译名的字面语感推断它在译哪个词。

### 32.3 zone / level 的既定对应

交叉复核报 `current zone`→「当前地图」混淆了 zone 与 level。不成立：
`t("Debug the problem (move to the failed zone/level)", "调试问题 (进入失败的地图/楼层)")`
—— 本库在调试串里就是 zone=地图、level=楼层。

### 32.4 空格问题的处理边界（§27 的续篇）

`#CRIMSON# %s的%s 被解除了！#LAST#` 的两处多余半角空格判成立，
但只改 `stripped`/`extended`/`disrupted` 这 3 条，**不立通用空格规则**。

依据是双重佐证：
- 源文 `#CRIMSON#%s's %s was stripped!#LAST#` 无对应空格；
- 同文件兄弟 `t("#CRIMSON#%s's beneficial effect was stripped!#LAST#",
  "#CRIMSON#%s的有益效果被除去了！#LAST#")` 无空格。

§27 的回归正是通用空格规则删掉了 `#YELLOW#-- 正在连接到服务器…--` 里
必须保留的分隔空格。**空格一律个案处理，必须有兄弟条目佐证。**

### 32.5 待裁决：半角括号内含中文（472 处）

`\([^()\n]{0,60}[一-鿿][^()\n]{0,60}\)` 命中 472 处：
mod-tome 314、tome-orcs 54、tome-cults 35、engine 34、
tome-possessors 13、tome-ashes-urhrok 12、mod-boot 8、tome-addon-dev 2。

**未擅自处理**：其中混有 `(WASD 方向键)`、`(等级 %d)` 这类中英/占位符混排，
未必都该转全角，需要维护者先定口径。
本批只统一了 RandomActor 单个条目**内部**的全半角混用（同一条目里
`(也是Lua控制台使用的环境)` 半角、`（可以…调整）` 全角），不扩及全库。

## §33 领域约定与协作教训（第 58 批）

### 33.1 领域约定：`%d%%` 是武器伤害百分比，`%0.2f` 是固定点数伤害

维护者 2026-09-09 指出：ToME4 的伤害分两类——
`%0.2f` 是**固定点数伤害**，`%d%%` 是**基于武器基础伤害的百分比伤害**。
所以译文里「造成 %d%% 奥术武器伤害」的「武器」二字是**必要消歧**，不是增译。

全库实证：

| 组合 | 条数 |
|---|---|
| `%0.2f` + 武器伤害 | **0** |
| `%0.2f` + 伤害 | 637 |
| `%d%%` + 武器伤害 | 150 |
| `%d%%` + 伤害（无「武器」） | 343 |

`%0.2f` **从不**带「武器」是单向铁律。`%d%%` 只是「通常」带（150/493），
所以**不得据此做全库扫描**——只作为判读依据。

**用途**：审核方看到译文比源文多出「武器」二字时容易报「增译」。
遇到这类报告，先查源文的伤害格式符再下结论。
我本人就曾据此误判 `eldritch-shield.lua:58`
（源文 `hitting the target with your weapon and shield for %d%% arcane damage`
本就是武器伤害），已更正。

### 33.2 内置 subagent 会在会话交接时被拆掉

第一次派发 Fable 5.1 顾问失败，UI 显示
`The user doesn't want to take this action right now`。**并非有人拒绝**：

- 拒绝出现在工具调用后 **7 毫秒**，人点不出来；
- `~/.claude/settings.json` 中 `defaultMode: auto`、`deny`/`ask` 为空、无 hooks；
- 当前 `claude` 进程的启动时间恰是那一秒 —— 旧进程正被替换；
- 同一秒 batch-57 的 `batch start` 后台 shell 也被报告 `stopped`；
- 20 分钟后以相同权限重发，一次成功。

**该文案被 Claude Code 复用于所有拒绝路径（含程序化取消），不可按字面理解。**
诊断方法：看响应间隔 + `ps -o lstart` 查 claude 进程启动时间。

避免办法（按性价比）：

1. **内置 subagent 一律 `run_in_background: true`** —— 前台调用与当前回合绑定，
   回合结束即被拆；后台调用可跨回合存活。
2. **昂贵或有状态的工作走 Paseo** —— paseo server 与 `claude` 是兄弟进程
   （同为 PID 1 侧的子进程），不随 claude 重启而死。编排者 agent
   `c62dba7e-…` 已跨多次会话存活；整条审核流水线本就建立在这个基础上。
3. **派发前在 `.ai/consult/` 留持久化意图标记**，成功后删除。
   会话交接后看到孤儿标记即知有咨询丢失——这次我完全没察觉，是维护者问起才发现。
4. **会话刚恢复的第一个回合不要起长任务**，先做廉价状态检查。

### 33.3 空格改动必须跑「全库首尾空白零变化」断言

括号转全角时顺手删除紧贴的半角空格，首版脚本误删了
`t(" (progress will be saved)", " (游戏进度会被保存)")` 的**开头空格**
——那是拼接分隔符，与上批驳回的 `" network of corridors"` 判例同型，
也是 §27 空格折叠回归的重演。抽查发现后整体回退重做（§31.3）。

正则要在**原始字面量区间**上跑，所以「字符串开头」不是索引 0，
而是紧跟在 `"` 或 `[[` 之后。四条守卫：

```python
# 只删单个半角空格；不动 tab、不动连续空格、
# 不动紧跟定界符 " / [[ 之后与行首的空格、不动 ） 后紧接 " / ]] 的空格
new = re.sub(r'(?<=[^\s"\[\n]) （', '（', new)
new = re.sub(r'） (?=[^\s"\]\n])', '）', new)
```

**新增强制断言**（比抽查可靠得多，此后所有空格类改动都要跑）：
逐条比对改前改后每个条目译文的**首尾空白长度**，必须全库零变化。
本批检查 30399 条，变化 0 处。

### 33.4 译名定夺可以请多模型讨论，但决断依据仍是库内证据

`Arcane Combat` 的译名经 Paseo 双模型讨论：
`antigravity/gemini-3.8-flash` 首选「奥术格斗」，`codex/gpt-6-astra` 首选「奥术战斗」，
二者互列对方为备选，并共同反对「奥术连击」「奥术附法」。

最终取「奥术格斗」，依据是库内证据而非投票：
本技能所属技能树即 `technique/magical-combat`→「魔法格斗」，
同树同一英文词须同译；且本库 `X Combat` 作技能树名时「格斗」为主流
（时空格斗/掠夺格斗/法杖格斗/魔法格斗 对 螺旋战斗，4:1）。
顾问共同反对的「奥术连击」经查已被 `t("Eldritch Fury","奥术连击")` 占用
——再次印证 §31.1「反查译名是否已被别的源术语占用」。

### 33.5 半角括号：维护者裁定与处理边界

维护者 2026-09-09 裁定：**混排的记为 pending，纯中文的处理**。

- **已处理 256 对**：括号内仅含中日韩、全角标点、数字、空白及 `%` `/` `+` `-` `.`；
- **pending 206 处**：含拉丁字母、占位符 `%s`/`%d`、颜色标记 `#TAG#`、
  强调星号 `*…*`，以及 `(按 '<', '>' 或右键使用)` 这类按键名。

分类式：

```python
PURE  = r'^[一-鿿，。、；：！？…—～·《》“”‘’0-9%/+.\-\s]+$'
MIXED = r'[A-Za-z*#]|%[-+0-9.]*[a-zA-Z]'   # 命中即 pending
```

## §34 源码工作集补齐（第 54–58 批）与 freeze_workset 两处缺陷

### §34.0 已 finalize 的批次可以从受跟踪证据确定性重建工作集
`freeze_workset.py` 原先只认 `.artifacts/.../active-batch.json`，而该文件在 finalize 后即消失，
于是第 54–58 批没有留下逐条源码工作集。新增 `rebuilt_from_evidence` 路径，来源全部是已提交证据：

| 需要的东西 | 来源 |
| --- | --- |
| 80 个 revision 与顺序 | `manifest.json:ordered_revisions` |
| 每条目录行 | `git show <base_commit>:evidence/.../catalog/entries.jsonl` |
| `row_sha256` | `sha256(canonical_bytes(目录行))`，与 `batch.py:795` 同一函数 |
| `prior_effective_state` | 由 `batch.py:794` 的规则套用反推出的 `selection_mode` |

`selection_mode` 不在 manifest 里，但 `batch_id = sha(mode|selected|attempt)`（`batch.py:71`），
合法取值只有 `queued`/`retry_blocked` 两个，**各算一遍看哪个复现 batch_id 即为证明**；
命中 0 个或 2 个一律拒绝，不许猜。重建完成后再用 manifest 的
`ordered_revisions_sha256` 与 `entry_snapshots_sha256` 双重比对才允许写出。

验证方式：用新路径重算第 53 批（唯一同时有原件的批次），与受跟踪原件**逐字节一致**。
这条回归必须保留——它是「重建 == 当时的 checkpoint」的唯一证明。

### §34.1 CRLF 文件让跨行字面量假性未命中
上游 tome 模块有 16 个 `.lua` 是 CRLF。目录抽取时行尾已规范为 LF，
而 `freeze_workset` 按字节 `split('\n')`，`\r` 留在行尾：
单行字面量因为是子串仍能命中，**跨行字面量则永远匹配不上**。
第 57 批 `higher-draconic.lua` 的 `You breathe crippling poison...` 就是这样被误报 MISS 的。

规矩：匹配用的文本按 `\r\n -> \n` 规范化；`source_file_sha256` 仍取磁盘**原始字节**摘要
（文件身份不能因规范化而改变）；规范化必须留痕，逐条写 `line_ending_normalization`。
**未命中先怀疑匹配器，再怀疑证据**——本次两个 MISS 没有一个是真的缺证据。

### §34.2 第七类归属：运行期拼接的实体名
`gem.lua:83` `name = "alchemist "..name:lower()`，实参在 `gem.lua:107` `newGem("Fire Opal", ...)`，
运行期拼出 `alchemist fire opal`。两半都不是完整字面量，逐行/整文匹配都必然落空。
新增 `concatenated_entity_name_verification`：记前缀、解析出的实参、拼接处行号、实参行号。
匹配限定 `source_tag == 'entity name'` 且要求 `source.startswith(前缀)` 后剩余部分
恰好等于某次具名调用实参的小写形式——不满足就仍然报 MISS，不放宽。

## §35 编排脚本加固：让"恢复"和"完成"两个状态可信

起因：编排记录只在流程顺利时才正确，一旦中途失败，留下的记录既不足以恢复、
也不足以证明当时做过什么。三条都不是假设，是脚本里真实存在的写法。

### §35.1 派发记录必须即时落盘，不能攒到最后
`dispatch_surface.py` / `dispatch_contextual.py` 原先把 `kids` 攒在内存里、
循环结束才 `json.dump`。中途任何一次失败，**已经建出来的 agent 就失去了记录**，
只能事后翻日志反推——而这正是这两个脚本的文档里说要避免的事。

现在：调 paseo **之前**先写一条 `status=dispatching` 的意图记录，
拿到 id **之后**立刻改写成 `dispatched`，两次都是原子写。于是：

| children.json 里的状态 | 含义 | 重跑行为 |
| --- | --- | --- |
| 无记录 | 没派发过 | 正常派发 |
| `dispatching` | 正好中断在建 agent 的瞬间，**可能已经有 agent 在跑** | 停下，要求按 `dispatch_id` 标签核对 |
| `dispatched` + agent_id | 已派发 | 跳过，不重复建 |

「可能已经有」这一档是关键：盲目重跑会建出重复 agent（§33 就踩过一次）。

### §35.2 收割必须当场校验，`if not o.get('candidate_identity')` 等于没查
原 `harvest_reviews.py` 只检查 identity **非空**。identity 写错、少答、多答、
顺序错位，全都能过。现在逐条对着**冻结输入信封**查三件事，任一不符即整批失败：
identity 必须**相等**；逐条 revision 必须与冻结顺序**完全一致**（顺序即覆盖，
多答少答错序一起管）；每条必须有 verdict。
surface 用 `entry_revision_identity`，contextual 用 `revision_key`，两种都认。

用真实产物做过故障注入，四类都能抓到：身份写错／少答一条／顺序错位／verdict 缺失。

### §35.3 归档要回读确认，返回码不是权威信号
`close_review_tasks.py` 原先 `subprocess.run(...archive..., capture_output=True)`
连返回码都不看，紧接着无条件写 `archive_confirmed: True`——归档失败时，
证据链上留下的是一句假话，而 `ai_state_check` 只认字面 `true`，正好被蒙混过去。

要注意 **`paseo agent archive` 对已归档的 agent 返回 rc=1**（"already archived"），
所以简单地"查返回码"反而会让幂等重跑失败。权威信号是回读：
先尽力归档并记下错误，再 `paseo agent inspect` 看 `Archived` 是否为 `true`，
同时核对 `ParentAgentId` 与本编排一致才写 `lineage_verified`。
确认不了就直接失败，**不降级写 false 蒙混**。`archived_at` 用服务端返回的 `ArchivedAt`。

### §35.4 顺带清掉的同类问题
- 编排脚本里不再有任何字面 agent/workspace id：`PASEO_AGENT_ID` 由 Paseo 注入，
  workspace 按 cwd 匹配 `paseo workspace ls --json`（README 早就这么要求，脚本没照做）。
- 所有 paseo 调用统一走 `_orch.paseo/paseo_json`，非零返回码立即失败——
  原先失败会静默变成"无输出"继续往下走。
- `harvest_contextual.py` 原先只打印 `bad: [...]` 就正常返回 **0**，
  编排者按退出码判断成功时会把失败当成功；现在有 bad 即非零退出。
- 落盘一律「同目录临时文件 + rename」，中途崩溃不留半个文件。

## §36 净进展报表：把"审了 80 条"换算成"前进了多少"

`tools/orchestration/batch_progress.py` 只读受跟踪证据，批次进行期间也能安全跑。

### §36.1 返工不是意外，是全库清扫的必然后果
改译会让条目产生新 revision 并重新入队。截至第 58 批：

| 指标 | 数 |
| --- | --- |
| 已审 revision | 6967 |
| 净新增覆盖的逻辑条目 | 6418 |
| 重复审到 | 549（7.9%） |
| 47 次修复/清扫改动的条目 | 3303（首次全量发布的 29828 条不计） |
| **已改动但尚未重审** | **约 2754 条 ≈ 34 个批次** |

单次最大的一笔改了 1003 条，等于给后面压了 12.5 个批次的返工。
所以「顺手做一次全库清扫」的成本不能只看当时改了多久——
**要按它会占掉多少个后续批次来算**（这正是 §35 之后要把清扫排进独立维护窗口的理由）。

返工分布极不均匀：有三个批次是 80/80 全部重审，净新增为 0。
这类批次的产出不该按 80 条计。

### §36.2 深审覆盖率 4.5%，漏报率仍然无法估计
6967 条里只有 311 条走过第二轮，其余只有表层一轮。
两轮一致才算 confirmed（§23），而单轮批次没有第二个独立观察者，
**因此现在没有任何数据能支持"漏报率是多少"这类说法**——不要凭 ISSUE 数反推质量。

### §36.3 两个把失败读成成功的坑
- **`bash tools/ci-gates.sh | tail -6` 的退出码是 `tail` 的，不是门禁的。**
  真实退出码 1 被换成 0，我据此把一次失败的门禁当成通过。查门禁必须直接看退出码。
- **门禁运行期间不得改动工作树。** `gate_results.run` 在开始和结束各算一次 binding
  （含 `ls-files --stage` 与文件内容摘要），中途变了就报
  `gate binding changed during execution`，整轮作废——
  哪怕 17 项 check 全部 `exit_code=0`，`success` 仍然是 false。
  日志里只有末尾一行 `GATES FAILED`，没有任何 `FAIL` 行，很容易误判成偶发。
  失败时先看 `.artifacts/i18n/ci-gates/run.*/results.json` 的 `error` 字段。

## §37 历史重放：先测量，再优化（2.5 倍，输出逐字段不变）

### §37.1 测量结果
在 96 个批次、49 个迁移的规模上跑一次 `_projection`（`queue status/check/rebuild`
以及 `migration plan/check/apply` 每次都要跑）：

| 函数 | 次数 | 秒 | 占比 |
| --- | --- | --- | --- |
| `_catalog_from_tree` | 196 | 223.0 | 68.9% |
| └ `validate_catalog_files` | 196 | **216.8** | **67.0%** |
| `_validated_migration_edges` | 1 | 136.0 | 42.0%（与上行嵌套重叠） |
| `_git` | 4409 | 35.4 | 10.9% |
| `_batch_rows` | 96 | 29.1 | 9.0% |

git 子命令里 `log` 2147 次占 26.5s，`cat-file` 1839 次占 7.9s。

关键比值：**97 个批次 base_commit 只对应 43 份不同的目录内容**（有一份被 29 个提交共用）。
原先 `git_evidence_reader` 只缓存 Git 原始字节，**解析与校验每次都重做**——
同一份字节被验了 196 遍。

### §37.2 改动
`validate_catalog_files(files: dict[str, bytes])` 只吃字节、不读 root/commit，是纯函数；
队列与迁移两个模块都不改动它返回的 `manifest`/`entries`（已逐个调用点核过）。
因此按**不可变内容标识**（三份目录文件的 blob id 三元组）在同一次 projection 内记忆其结果。

刻意保留的东西：每个受跟踪文件仍然逐个 `_ordinary_blob` 读取并校验 mode/kind，
目录子树集合检查照旧，迁移发布边界校验、事务前候选重读、17 项门禁全部不动。
**只省掉「对同一份字节重复做同一个纯函数」**。

### §37.3 验证方式
不能只看变快了。改动前后各跑一次完整重放，比对 8 个字段：
`head`/`catalog_id`/`entries_n`/`overrides_n`/`reconciliation_n` 与
`overrides`/`reconciliation`/`entries` 三个内容摘要——**全部一致**。
随后 `queue rebuild` + `queue check` 成功（reconciliation 29828、surface_covered 6365），
17 项门禁全绿。

耗时 **314.8s → 125.4s（2.5 倍，省 189s）**。`rebuild + check` 两次投影合计 4m14s。
剩下的大头是 `git log`（2147 次）与 `_batch_rows`，暂不动——
优化过的地方必须有测量支撑，没量过的不要顺手改。

## §38 全库清扫：排进独立维护窗口，并且只用 sweep.py 做

### §38.1 清扫要单独排期，理由是返工账
§36.1 的数字：一次改 1003 条的清扫，等于给后面压了 12.5 个批次的重审。
目前已改动但尚未重审的约 2754 条 ≈ 34 个批次。所以：

- **不在批次里顺手做全库清扫。** 清扫另起维护窗口，单独一条 migration，
  提交信息里写明改动条数与由此产生的预期返工批次数（`改 N 条 ≈ N/80 个批次`）。
- 一个窗口只做**一类**改动。混做会让 migration 的 `rows` 无法归因，
  也让「哪次清扫造成了哪批返工」查不回来。
- 窗口结束后立刻 `queue rebuild`，让返工进入正常批次流，不要另开特殊通道。

### §38.2 清扫必须走 `tools/orchestration/sweep.py`
`sweep.py plan|apply <rules.json>`：对整份文件做正则替换，再用 LuaJIT 桥
**重新语义解析改后的字节**逐条比对，全过才落盘（原子写），一条不符即整轮放弃。

核心判据是一条可检验的等式：

    文件里实际发生的替换次数 == 各条译文里匹配次数之和

不相等就说明有匹配落在注释、源文或代码上。逐条守卫另有四道：
源文/`source_tag`/`args_order`/`special` 不得变化；译文**首尾空白**不得变化；
占位符转换序列不得变化；`#...#` 标记序列不得变化；条目数与顺序不得变化。

文件集合默认就是 11 个组件，少给会打印警告（§27 漏组件挂门禁）。
跨组件同 runtime key 会单独列出，提示必须各组件改成一致。

用真实库做过四项对抗测试，全部符合预期：

| 测试 | 结果 |
| --- | --- |
| 规则命中注释里的串（77 次） | 拦下：文本 77 次 / 语义 0 次 |
| 删掉译文行首空格（§27 拼接陷阱） | 拦下：首尾空白序列被改变 |
| 把 `%d` 改成 `%s` | 拦下：占位符序列被改变 |
| 正常术语替换 | 通过 |

**手写一次性脚本做清扫的做法到此为止。** 之前每一次都踩到上面某一条：
§27 删掉拼接空格、§30.6 改到被注释掉的条目、§31.3 断言失败后半个文件已经写出去。
