# 基线批次编排脚本

供 ORCHESTRATOR 跑 80 条一批的 fill-80 基线审核。正式约束以 [`AGENTS.md`](../../AGENTS.md)、
[工作流](../../docs/agent-workflow.md)、[WP2-Lite 方案](../../docs/translation-production-review-v2-lite-plan.md)
与三份 Paseo 契约为准；**本目录只是操作辅助，不放宽任何契约**。
完整操作链与踩坑记录见 [`docs/baseline-batch-runbook-2026-09-06.md`](../../docs/baseline-batch-runbook-2026-09-06.md)。

## 脚本

当前流程（surface + 交叉复核两轮）：

| 脚本 | 作用 |
| --- | --- |
| `_orch.py` | 共用件：身份运行时发现、带返回码检查的 paseo 调用、原子写 |
| `freeze_workset.py <batch>` | 冻结公开源码工作集，逐条核验；必须 80/80 命中。批次已 finalize 时从受跟踪证据确定性重建（runbook §34.0） |
| `stage_surface.py <batch>` | 把 surface-export 产物落成 `.ai/task/<task>/` 布局并写 dispatch-plan |
| `dispatch_surface.py <plan> <children>` | 逐 lane 派发 surface REVIEWER；派发前后各落一次盘，可幂等重跑 |
| `harvest_reviews.py <children> <outdir> [--key results\|verdicts]` | 收割输出，**当场**校验 identity 相等与覆盖/顺序完全一致 |
| `build_import_index.py <kind> <rawdir> <out>` | 按 candidate_identity（不是 lane 编号）建 import index |
| `stage_contextual.py <batch>` | 按 checkpoint 的 contextual refs 建 `.ai/task/<batch>-contextual-NNN/` |
| `dispatch_contextual.py <ctx> <children>` | 派发交叉复核 child，同样的崩溃安全与幂等语义 |
| `close_review_tasks.py <kind> <spec> <children> <rawdir>` | 写 review record、**确认式**归档 child、填 STATE 并校验 DONE_VERIFIED |

上一代脚本，保留供对照，新批次不要再用：
`dispatch_reviewers.py`、`harvest_reviewers.py`、`harvest_contextual.py`
（它们的职责已分别并入 `dispatch_surface.py`、`harvest_reviews.py`、`close_review_tasks.py`）。

`write_states.py` 原本也在这份名单里，2026-09-11 **删除**而不是留作对照：它把
`runtime_observation` 的 provider/model/thinking 写成模块级常量，同时把该字段标成
`source: live_agent_metadata` / `capture_status: captured`，而 `ai_state_check.py:166-171`
只校验这两个字面量、校验不了内容是否真来自实况。它作为死代码没有危害，但作为
「字段自称实测、实则写死」的现成模板，被复用一次就会变成真的假话——留着对照的价值
低于这个风险。它的职责在 `close_review_tasks.py`。

## 身份与路径：一律运行时发现，不得硬编码

统一由 `_orch.py` 提供，脚本里不再出现任何字面 id：

- `PASEO_AGENT_ID` —— 当前 ORCHESTRATOR 自己，用作 child 的 `paseo.parent-agent-id`。
  Paseo 会自动注入。**抄用别的 agent 的 id 会写错 lineage，`ai_state_check.py --target DONE` 会失败。**
- workspace id —— 按 cwd 匹配 `paseo workspace ls --json`（CLI 返回裸数组，MCP 返回
  `{"workspaces":[...]}`，两种都兼容）；必要时用 `TOME_PASEO_WORKSPACE` 覆盖。
- `TOME_ENGINE_ROOT` / `TOME_DLC_ROOT` —— 公开源码根，由 Paseo 环境提供。

## 每批流程

```bash
python3 -B tools/i18n production queue rebuild && python3 -B tools/i18n production queue check
python3 -B tools/i18n production batch start --limit 80
B=$(python3 -c "import json;print(json.load(open('.artifacts/i18n/production-review-v2-lite/active-batch.json'))['batch_id'])")
TOME_ENGINE_ROOT=/workspace/t-engine4 TOME_DLC_ROOT=/workspace/tome4-dlcs \
  python3 -B tools/orchestration/freeze_workset.py $B          # 必须 80/80
python3 -B tools/i18n production batch surface-export
python3 -B tools/orchestration/stage_surface.py $B --out /tmp/plan-$B.json
python3 -B tools/surface_screen_manifest.py check <每个 group manifest>   # MANIFEST_VERIFIED
python3 -B tools/orchestration/dispatch_surface.py /tmp/plan-$B.json /tmp/kids-$B.json
# …等 child 全部结束…
python3 -B tools/orchestration/harvest_reviews.py /tmp/kids-$B.json /tmp/raw-$B
git status --short                                            # 证明 reviewer 未写入任何文件
python3 -B tools/orchestration/close_review_tasks.py surface /tmp/plan-$B.json /tmp/kids-$B.json /tmp/raw-$B
python3 -B tools/orchestration/build_import_index.py surface /tmp/raw-$B /tmp/idx-$B.json
python3 -B tools/i18n production batch surface-import --input /tmp/idx-$B.json
# 有 ISSUE 才需要（注意顺序：contextual-import 前对应 task 必须已 DONE_VERIFIED）：
python3 -B tools/i18n production batch contextual-export
python3 -B tools/orchestration/stage_contextual.py $B --out /tmp/ctx-$B.json
python3 -B tools/orchestration/dispatch_contextual.py /tmp/ctx-$B.json /tmp/ctxkids-$B.json
# …等 child 结束…
python3 -B tools/orchestration/harvest_reviews.py /tmp/ctxkids-$B.json /tmp/ctxraw-$B --key verdicts
python3 -B tools/orchestration/close_review_tasks.py contextual /tmp/ctx-$B.json /tmp/ctxkids-$B.json /tmp/ctxraw-$B
python3 -B tools/orchestration/build_import_index.py contextual /tmp/ctxraw-$B /tmp/ctxidx-$B.json
python3 -B tools/i18n production batch contextual-import --input /tmp/ctxidx-$B.json
python3 -B tools/i18n production batch adjudicate --input <decisions.json>
python3 -B tools/i18n production batch prepare-evidence       # 内含 17 项门禁
cp -r .artifacts/.../prospective/.../batches/$B evidence/production-review-v2-lite/batches/
git add … && git commit && python3 -B tools/i18n production batch finalize --commit $(git rev-parse HEAD)
git push origin develop
# 有 confirmed 才需要：repair preflight → worktree → 改译文 → catalog build → migration → 门禁 → merge
```

## 四条硬约束

1. **批次进行期间不得向 develop 提交任何东西**（含纯文档）。`batch start` 冻结 `base_commit`，
   HEAD 一旦不等于它，import／adjudicate／甚至 abandon 全部报 drift，批次锁死。
   已经提交了的补救：`git checkout --detach <base_commit>` 恢复 → 在该 base 上做 evidence commit
   与 finalize → `git checkout develop` 后 `git merge --no-ff <evidence commit>`。**不要 force push。**
2. **修复前先全仓库 grep**。同一 runtime key 可能横跨 `mod-tome.lua`／`tome-cults.lua`／
   `tome-orcs.lua`／`engine.lua`／`mod-boot.lua`；漏改会让 `06-runtime-collision-scan` 失败。
3. **`contextual-import` 要求对应 task 已 `DONE_VERIFIED`**（surface-import 没有这道检查）。
   顺序必须是 `harvest_reviews.py` → `close_review_tasks.py <kind>` →
   `build_import_index.py <kind>` → `<kind>-import`；顺序反了会报
   `contextual task is not current DONE_VERIFIED bound to exact task/candidate/input/output`。
   `close_review_tasks.py` 内部已包含归档、填 STATE 与 `ai_state_check.py --target DONE`
   校验（`close_review_tasks.py:136-140` 直接调它并检查输出以 `DONE_VERIFIED` 开头），
   **不需要也不应再单独跑 `ai_state_check.py`**。少跑 `build_import_index.py` 则 import
   拿不到索引文件。
4. **派发必须显式传 `--mode`**。claude 默认 Always Ask 会让 child 卡在权限弹窗上，
   编排者只看到 status 长期不变。
5. **派发记录即时落盘**。`dispatch_*.py` 在调 paseo 之前先写 `status=dispatching`，
   拿到 id 后立刻改写为 `dispatched`。重跑会跳过已派发的 lane；若看到 `dispatching` 残留，
   说明上次正好中断在建 agent 的瞬间，**先按 `dispatch_id` 标签核对再处理，不要盲目重跑**。

## 派发方式：CLI 直派 与 MCP 两段式

`paseo run` CLI 不暴露 provider 的功能开关，claude 的 **fast mode** 只能经 MCP
`create_agent` 的 `settings.features.fast_mode` 传入。为此 `dispatch_surface.py` 与
`dispatch_contextual.py` 都支持两种派发方式，提示词始终由脚本唯一生成
（合约的 800 字节上限只在脚本里把关），崩溃安全语义两种方式一致。

**CLI 直派（默认）**

```
python3 -B tools/orchestration/dispatch_surface.py <plan.json> <children.json>
```

**MCP 两段式**

```
# 1) 写 dispatching 意图，并导出待创建项（含提示词与标签）
python3 -B tools/orchestration/dispatch_surface.py <plan.json> <children.json> --emit <emit.json>

# 2) 编排者据 emit.json 逐条调用 paseo MCP create_agent，
#    settings 传 { features: { fast_mode: true }, thinkingOptionId, modeId }

# 3) 回填 agent_id（ids.json 的键为 "task_id|dispatch_id"）
python3 -B tools/orchestration/dispatch_surface.py <plan.json> <children.json> --record <ids.json>
```

`--record` 会拒绝重复的 `agent_id`，也会在仍有未回填的意图记录时报错退出——
即「可能已经建了 agent 却没记下 id」的状态不允许留在盘上。

注意：fast mode 只有 Opus 系模型支持（`claude-opus-5`、`claude-opus-4-8/4-7/4-6` 及其 1M 变体）；
`claude-fable-5-1`、`claude-sonnet-5`、`claude-haiku-4-5` 均不支持。官方说明为
「以更高 token 成本换取更低延迟」，不改变模型能力，因此不影响两轮审核的裁决门槛。
