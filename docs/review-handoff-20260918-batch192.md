# 翻译审核交接：第 187–192 批 + 修复批 207–213，下一步为修复批 214

最后更新：2026-09-18 · 分支 `develop` · HEAD `395e2d8`
交叉复核模型：**`claude/claude-opus-5`**（dispatch_contextual.py，逐批核验）

本文取代 [第 186 批交接](../deprecated/docs/review-handoff-20260916-batch186.md)。
只写手册里没有、或踩过坑才知道的部分；流程细节见
[`baseline-batch-runbook-2026-09-06.md`](baseline-batch-runbook-2026-09-06.md)。

---

## 1. 当前状态

| 项 | 值 |
| --- | --- |
| 已完成审核批 | 第 187–**193** 批（每批 80 条），均 review_only，17/17 门禁逐批通过 |
| 已完成修复批 | 第 207–**214** 批（每批 20 条），catalog + migration 均已落地 |
| done | **17849** |
| **repair_required** | **280** |
| blocked | **9**（第 193 批新增 pending：the Sorcerers 术语统一 ad393c54） |
| HEAD | `6932fbe`（batch 193 finalize）；无活动批次 |
| 未 push | `origin/develop` 停在旧位置，本地领先多个提交 |
| 工作树 | 干净；`.ai/consult/` 是唯一 `??`，**严禁读取、暂存或清理** |
| 交替节奏 | **严格 1:1**（80 条审核 → 20 条修复），当前轮到**修复批 215** |

### 第 214 修复批 + 第 193 审核批（2026-09-18，本会话）
- 修复批 214：20 条（青金石/换行不变量/删限定词/施受方向/master-of-bones 召唤上限/兽人 lore 因果与称号/半身人脚粗绳等），migration `2734d4f8`，evidence `e2a9faf`。
- 审核批 193（`batch-45074f76e6ee8c10db28`，evidence `6932fbe`）：80 条，表层 4 lane（gpt-5.6-sol，MCP 手工驱动）+ 交叉复核 1 child（opus-5）。裁决 confirmed 9 / refuted 9 / advisory 2 / **pending 1**，5 条 entry 入 repair_required。
- **表层派发全程走 MCP 手工 lifecycle**（emit→create_agent→intent/bind/harvest/archive/confirm→close），详见记忆 `mcp-review-lifecycle-manual-drive` 与 `surface-raw-extraction-trailing-newline`。

### 批次提交对照（自上一份交接以来）

| 批 | 类型 | evidence commit | 裁决摘要 |
| --- | --- | --- | --- |
| 187 | 审核 | `92611d7` | — (old format) |
| 修复 207 | 修复 | `9bf6b8a` | 20 revisions |
| 188 | 审核 | `da48642` | confirmed 5 / refuted 4, repair 4 |
| 修复 209 | 修复 | `3ab6fb3` | 21 revisions |
| 189 | 审核 | `12c51fb` | confirmed 4 / refuted 3, repair 3 |
| 修复 211 | 修复 | `ae3db2b` | 20 revisions |
| 190 | 审核 | `6c44be4` | confirmed 6 / refuted 9, repair 4 |
| 修复 212 | 修复 | `d7a9840` | 20 revisions |
| 191 | 审核 | `e3fdb1c` | confirmed 8 / refuted 6, repair 8 |
| 修复 213 | 修复 | `97ceee3` | 20 revisions |
| 192 | 审核 | `395e2d8` | confirmed 8 / refuted 14, repair 4 |

注：批次 187 使用旧格式提交（contextual-export 直接写到 batch commit 里），从 188 起改用
surface-export → contextual-export → adjudicate → prepare-evidence → commit → finalize 的标准流程。

---

## 2. 审核与修复交替节奏（常驻指令）

用户授权**连续主持**，逐批自动推进不必确认。节奏：

- **每一批 80 条审核后，必须接一批 20 条修复**，严格 1:1 交替
- 审核使用 `batch start --limit 80` 从 queue 选取
- 修复不走 batch lifecycle，而是手动：查 repair_required 条目 → 查对应 observation → 修复 mod-tome.lua → Lua 语法检查 → commit → authoritative-catalog build → migration plan/apply → commit evidence → queue rebuild
- 修复批编号与审核批编号独立（审核 192，修复 213）

---

## 3. 修复批工作流（非 batch lifecycle）

修复不使用 `batch start`（那只选 queued 条目）。手动流程：

```bash
# 1. 查 repair_required 条目
python3 -B -c "
import sqlite3
db = sqlite3.connect('.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
rows = db.execute(\"SELECT entry_revision_identity FROM state_override WHERE state='repair_required' LIMIT 20\").fetchall()
for r in rows: print(r[0])
"

# 2. 查对应 observation（从 evidence batches 的 adjudications.jsonl）
# 找 entry_revision_identity 匹配且 repair_required=true 的条目，读其 conclusion

# 3. 修复 mod-tome.lua（或其他组件文件）
# 注意：同一 runtime key 可能横跨 tome/cults/orcs 文件

# 4. Lua 语法检查
luac -p mod-tome.lua

# 5. commit 修复
git add mod-tome.lua && git commit -m "repair: N revisions — 修复批 XXX"

# 6. authoritative-catalog build
python3 -B -c "
import sys; sys.argv = ['cli', 'production', 'authoritative-catalog', 'build', '--output', '/tmp/batchXXX-catalog', '--json']
from tools.i18nlib.cli import main; main()
"

# 7. migration plan + apply
python3 -B -c "
import sys; sys.argv = ['cli', 'production', 'migration', 'plan', '--candidate-catalog', '/tmp/batchXXX-catalog', '--output', '/tmp/batchXXX-migration.json']
from tools.i18nlib.cli import main; main()
"
python3 -B -c "
import sys; sys.argv = ['cli', 'production', 'migration', 'apply', '--input', '/tmp/batchXXX-migration.json', '--candidate-catalog', '/tmp/batchXXX-catalog']
from tools.i18nlib.cli import main; main()
"

# 8. 拷贝 catalog + migration 到 evidence/
cp /tmp/batchXXX-catalog/evidence/production-review-v2-lite/catalog/* evidence/production-review-v2-lite/catalog/

# 9. commit evidence + queue rebuild
git add evidence/ && git commit -m "evidence: batch XXX repair — catalog + migration (N revisions)"
# queue rebuild 用 batch recover-from-head（如果 lock 卡住，先删 repository.lock）
```

---

## 4. 审核批标准流程

```
batch start --limit 80
 → surface-export → stage_surface.py → dispatch_surface.py (4 lanes)
 → create agents (lane 0-2 先, 收一条再 lane 3, 并发上限 3)
 → harvest → archive → close → surface-import
 → contextual-export → dispatch_contextual.py (1 lane)
 → create agent → harvest → archive → close → contextual-import
 → adjudicate → prepare-evidence → copy prospective → commit → finalize
```

### 关键约束

- **batch start 到 finalize 之间不得有任何其他提交**
- **并发上限 3**：先建 lane 0–2，收割归档一条后再建 lane 3
- **finalize 要完整 40 位 sha**
- **归档 scratch 要在下一批 contextual-export 之前做**

### Profile ID（固定）

- 表层：`agent_profile_mt3s8sou_fggrhfnq1gj`（`codex/gpt-5.6-sol`，medium，`auto-review`）
- 交叉复核：`agent_profile_mtjlooyy_myzr9tapied`（`claude/claude-opus-5`，medium，`auto`）
- 工作区：`wks_420314270844170b`

### 裁决规则

- 表层 ISSUE + 交叉 ISSUE → **confirmed** + `repair_required=true`
- 表层 ISSUE + 交叉 OK → **refuted**
- confirmed 必须附 source evidence（`evidence_path="mod-tome.lua"` + `evidence_commit=<HEAD的40位hex>`）
- refuted 的 evidence 三字段全为 None

---

## 5. 判定规则（对后续裁决有约束力）

1. **族内一致度达惯例门槛时，单条修复有害**（→ advisory）；**未达门槛时按单条机制正确性处置**（→ confirmed）。
2. **「删限定词」是一类系统性缺陷**（may/chance/up to/each/high level/every turn），按机制正确性判定，不走惯例门槛。
3. **交叉复核看不到语料**。它关于「族内既有译法」的结论必须经宿主查全库后才能采信。
4. **专名改名归用户裁决**，不自行决定。
5. **死亡描述类冻结**：`death_message` + `killer_message` 一并计入，直接 pending。

---

## 6. 仍在 pending 的议题

| 议题 | 规模 | 备注 |
| --- | ---: | --- |
| Haunted 族 | 5 | 含与 `entangle` 的「纠缠」双向撞名 |
| talent type 尾词策略 | 6 | drake aspect 5 + higher draconic abilities 1 |
| 格式规范化规则 | 4+ | 原文硬折行保留与否、行尾空白 |
| 死亡描述类 | ~16 + killer_message | 用户裁定冻结 |

用户已明确**不动**的：`Archmage→元素法师`（24 处）、`Travel Speed→飞行速度`（6 处）、vial 族。

---

## 7. 恢复入口（修复批 215）

当前轮到修复批（1:1 交替节奏），280 条 repair_required 待清理。

```bash
# 查 repair_required 条目
python3 -B -c "
import sqlite3
db = sqlite3.connect('.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
rows = db.execute(\"SELECT entry_revision_identity FROM state_override WHERE state='repair_required' LIMIT 20\").fetchall()
for r in rows: print(r[0])
"
# 然后按第 3 节流程执行修复
```

修复批完成后继续审核批 193（`batch start --limit 80`），如此交替。

---

## 8. 已知陷阱（本轮新增经验）

1. **contextual-import 需要 DONE_VERIFIED 状态**：contextual task 的 STATE.json 必须有完整的
   `review_records`、`child_dispatches`（含 `lineage_verified: true`、`archive_confirmed: true`）、
   `completed_review_contracts`、`contextual_reviewers` 等字段，且 `state: "DONE"`，
   否则 `ai_state_check` 不会返回 DONE_VERIFIED，contextual-import 会拒绝。

2. **adjudicate 必须覆盖所有 observation**：`_accepted_observations()` 从 checkpoint 的
   surface 和 contextual refs 里读取所有 ISSUE 的 observation_identity，adjudication 必须
   一一对应，不能多也不能少。

3. **prepare-evidence 耗时较长**（~5 分钟），需要用 background 或长 timeout。

4. **finalize 需要完整 40 位 commit hash**，不能用缩写。

5. **smart quotes 陷阱**：Edit tool 有时会把 ASCII `"` 替换为 Unicode `"`，导致 Lua 语法错误。
   修复 Lua 文件时用 Python 写入，不用 Edit tool 处理含中文引号的行。
