# 基线批次编排脚本

供 ORCHESTRATOR 跑 80 条一批的 fill-80 基线审核。正式约束以 [`AGENTS.md`](../../AGENTS.md)、
[工作流](../../docs/agent-workflow.md)、[WP2-Lite 方案](../../docs/translation-production-review-v2-lite-plan.md)
与三份 Paseo 契约为准；**本目录只是操作辅助，不放宽任何契约**。
完整操作链与踩坑记录见 [`docs/baseline-batch-runbook-2026-09-06.md`](../../docs/baseline-batch-runbook-2026-09-06.md)。

## 脚本

| 脚本 | 作用 |
| --- | --- |
| `freeze_workset.py <batch>` | 冻结公开源码工作集，逐条核验；必须 80/80 命中 |
| `stage_surface.py <batch>` | 把 surface-export 产物落成 `.ai/task/<task>/` 布局并写 dispatch-plan |
| `dispatch_reviewers.py <batch>` | 每 lane/full 成员派发一个 REVIEWER child |
| `harvest_reviewers.py <batch>` | 收割输出，逐个过 consumer validator 后落盘 |
| `dispatch_contextual.py <batch>` | 按 checkpoint 的 contextual refs 落成 `.ai/task` 布局并派发交叉复核 child |
| `harvest_contextual.py <batch>` | 收割交叉复核输出，过 validator、读回 runtime metadata 后归档 child |
| `write_states.py <batch> <base>` | 写 STATE 与 review record，使其满足 DONE 谓词 |

## 身份与路径：一律运行时发现，不得硬编码

- `PASEO_AGENT_ID` —— 当前 ORCHESTRATOR 自己，用作 child 的 `paseo.parent-agent-id`。
  **抄用别的 agent 的 id 会写错 lineage，`ai_state_check.py --target DONE` 会失败。**
- workspace id —— 按 cwd 匹配 `paseo workspace ls --json`（CLI 返回裸数组，MCP 返回
  `{"workspaces":[...]}`，脚本两种都兼容）。
- `TOME_ENGINE_ROOT` / `TOME_DLC_ROOT` —— 公开源码根，由 Paseo 环境提供。

## 每批流程

```bash
python3 -B tools/i18n production queue rebuild && python3 -B tools/i18n production queue check
python3 -B tools/i18n production batch start --limit 80
B=$(python3 -c "import json;print(json.load(open('.artifacts/i18n/production-review-v2-lite/active-batch.json'))['batch_id'])")
python3 -B tools/orchestration/freeze_workset.py $B          # 必须 80/80
python3 -B tools/i18n production batch surface-export
python3 -B tools/orchestration/stage_surface.py $B
python3 -B tools/surface_screen_manifest.py check <每个 group manifest>   # MANIFEST_VERIFIED
python3 -B tools/orchestration/dispatch_reviewers.py $B
# …等 child 全部结束…
python3 -B tools/orchestration/harvest_reviewers.py $B
git status --short                                            # 证明 reviewer 未写入任何文件
python3 -B tools/i18n production batch surface-import --input <index.json>
# 有 ISSUE 才需要（注意顺序：import 前必须先 write_states 拿到 DONE_VERIFIED）：
python3 -B tools/i18n production batch contextual-export
python3 -B tools/orchestration/dispatch_contextual.py $B
# …等 child 结束…
python3 -B tools/orchestration/harvest_contextual.py $B
paseo archive <每个 child>
python3 -B tools/orchestration/write_states.py $B <base_commit>
python3 -B tools/ai_state_check.py .ai/task/<task>/STATE.json --target DONE   # 每个 task 都要 DONE_VERIFIED
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
   顺序必须是 harvest → archive → `write_states.py` → `ai_state_check.py --target DONE` →
   `contextual-import`；顺序反了会报
   `contextual task is not current DONE_VERIFIED bound to exact task/candidate/input/output`。
4. **派发必须显式传 `--mode`**。claude 默认 Always Ask 会让 child 卡在权限弹窗上，
   编排者只看到 status 长期不变。
