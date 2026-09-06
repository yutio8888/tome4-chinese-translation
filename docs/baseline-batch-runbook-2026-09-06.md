# 80 条基线批次审核运行手册（2026-09-06）

> 供主编排者（ORCHESTRATOR）后续阅读并继续开展 80 条基线批次审核工作。
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
  `codex/gpt-6-astra`，`--thinking low`。
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
