# 翻译审核流水线交接说明（截至第 127 批）

写于 2026-09-14，交接时基线 `7d1909d5e670ceeeb5962481dddb5bd0c0ac9692`（分支 `develop`）。

本文只写接手就能用的东西：当前状态、必须守的规矩、完整跑批配方、踩过的坑、以及需要用户拍板才能动的悬而未决项。流程为什么这么设计写在 `docs/translation-production-review-v2-lite-plan.md` 与 `docs/paseo-orchestration-v2-contract.md`，不在这里重复。

---

## 1. 交接时的状态

| 项 | 值 |
|---|---|
| 分支 | `develop`（主分支是 `master`，但审核工作一直在 `develop`） |
| HEAD | `7d1909d` review: complete batch 127 evidence with seven repair findings |
| 活动批次 | 无。`python3 -B tools/i18n production batch show` 返回 `{"active": false, "ok": true}` |
| 工作树 | 干净。`git status --porcelain` 只有 `?? .ai/consult/`，这是刻意保持的未跟踪状态 |
| contextual 暂存槽 | 已清空。`.artifacts/i18n/production-review-v2-lite/contextual/` 为空目录 |
| 引擎工作树 | `/workspace/t-engine4` HEAD == 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，跟踪文件零改动 |
| 已提交批次证据 | 165 个批次目录，累计 12487 条 entry 结果 |
| 累计裁决 | 1093 条：confirmed 848、advisory 160、refuted 56、pending 29 |

**接手后第一件事**：`git rev-parse HEAD` 确认还是 `7d1909d`。如果不是，说明期间有别的写入者动过，先查清楚再开批——批次开始到 finalize 之间任何提交都会让 active batch 锁死。

---

## 2. 硬约束（用户历次明确要求，不要自行放宽）

1. **`.ai/consult/` 保持未跟踪，严禁读取、stage 或清理。** 它会一直出现在 `git status` 里，这是正常的。
2. **允许本地提交，不允许 push / PR / 任何外部发布。**
3. **不得删除或改写已派发的候选，不可无差别清理 runtime。**
4. **不改 profile，不得伪造 runtime 数据。**
5. **运行中不轮询、不取消。** 一个 child 只跑一次；失效的先归档再 fresh retry，不发 follow-up prompt。
6. **每次 `create_agent` 之前实时调用 `list_profiles`，读全部 notes，并把原始响应存进 profile capture。** 这不是形式——capture 会被 `create-intent` 复制成不可变记录。
7. **所有「已完成」的声称都要以实际日志或 commit 为准**，不靠记忆。
8. **子 agent 查原生源码只允许必要目录与 Git metadata**，禁止全仓扫描或读其他 `.ai` 内容。
9. **`paseo.parent-agent-id` 必须是你自己实际的 `PASEO_AGENT_ID`**，不能复用前任宿主的。既有历史记录不可改写。

第 9 条的背景：宿主换过一次，历史 journal 里留着旧宿主的 id。那些不要动，新建的 child 用你自己的。

---

## 3. 一批的完整流程

`$D = .artifacts/i18n/batch<N>-orchestration`，`$BID` 是 `batch start` 返回的 batch_id。

### 3.1 搭脚手架

从上一批复制 8 个文件，然后改批次号：

```bash
P=.artifacts/i18n/batch127-orchestration
D=.artifacts/i18n/batch128-orchestration
mkdir -p "$D"
cp "$P"/{run-host-phase.py,submit-event.py,submit-ctx-event.py,emit-create-args.py,\
make-profiles-capture.py,dispatch-contextual-hardened.py,\
surface-profiles-template.json,contextual-profiles-template.json} "$D"/
sed -i 's#batch127-orchestration#batch128-orchestration#g' "$D"/*.py
grep -rn 'batch127' "$D"/ || echo "无残留，正确"
mkdir -p "$D"/surface-raw "$D"/contextual-raw
```

8 个文件里只有 3 个带批次目录字符串（`run-host-phase.py`、`submit-event.py`、`submit-ctx-event.py`），`grep` 必须返回空。

**归档上一批的 contextual 暂存**——本次交接已经替第 128 批做完了，槽是空的，可以跳过。但**从第 129 批起每批都要做**：

```bash
S=.artifacts/i18n/production-review-v2-lite/contextual
# 先 sha256 比对 run-000-{input,output}.json 与上一批已提交的
# evidence/.../raw/contextual/004-{input,output}_path.json，确认 MATCH
# 再 mv（不是 rm）进 $D/prior-batch-runtime-scratch/，附 NOTE.json
```

为什么必须做：这个槽是**全局单份、文件名不带批次号**。`tools/i18nlib/production_review_v2_lite_batch.py:620-634` 在写入前会把已存在的 input 与新候选逐字节比对，不同就抛 `frozen source-facts candidate differs`。晚一步就撞不可变检查，而且事后没法补救。

### 3.2 各阶段命令

全部通过 `run-host-phase.py` 跑，它会写 `<name>.log` 与 `<name>-result.json`，**如果任一文件已存在就拒绝执行**（防重复跑）。

```
batch-start:                 timeout -k 10s 900s  python3 -B tools/i18n production batch start --limit 80
freeze-workset:              timeout -k 10s 900s  python3 -B tools/orchestration/freeze_workset.py $BID
surface-export:              timeout -k 10s 900s  python3 -B tools/i18n production batch surface-export
stage-surface:               timeout -k 10s 600s  python3 -B tools/orchestration/stage_surface.py $BID --out $D/surface-stage-plan.json
dispatch-surface-prepare:    timeout -k 10s 600s  python3 -B tools/orchestration/dispatch_surface.py .ai/task/$BID/dispatch-plan.json $D/surface-children.json --emit $D/surface-emit.json --select-transport mcp --mode auto-review
（此处派发 4 条 lane，见 3.3）
close-surface:               timeout -k 10s 600s  python3 -B tools/orchestration/close_review_tasks.py surface $D/surface-plan.json $D/surface-children.json $D/surface-raw
surface-index:               timeout -k 10s 600s  python3 -B tools/orchestration/build_import_index.py surface $D/surface-raw $D/surface-index.json
surface-import:              timeout -k 10s 900s  python3 -B tools/i18n production batch surface-import --input $D/surface-index.json
contextual-export:           timeout -k 10s 900s  python3 -B tools/i18n production batch contextual-export --source-workset evidence/quality/production-batches/$BID-source-workset.json
stage-contextual:            timeout -k 10s 600s  python3 -B tools/orchestration/stage_contextual.py $BID --out $D/contextual-stage-plan.json
dispatch-contextual-prepare: timeout -k 10s 600s  python3 -B $D/dispatch-contextual-hardened.py $D/contextual-stage-plan.json $D/contextual-children.json --emit $D/contextual-emit.json --select-transport mcp
（此处派发 1 个 contextual child，见 3.3）
close-contextual:            timeout -k 10s 600s  python3 -B tools/orchestration/close_review_tasks.py contextual $D/contextual-plan.json $D/contextual-children.json $D/contextual-raw
contextual-index:            timeout -k 10s 600s  python3 -B tools/orchestration/build_import_index.py contextual $D/contextual-raw $D/contextual-index.json
adjudication-chain:          timeout -k 10s 1800s python3 -B tools/orchestration/run_batch_steps.py contextual-adjudication-chain --input $D/contextual-index.json --spec $D/host-decisions.json --output .artifacts/i18n/adjudication-chain/$BID.json --source-root /workspace/t-engine4
finalize:                    timeout -k 10s 1800s python3 -B tools/i18n production batch finalize --commit <证据提交的 sha>
```

两处容易漏的 `cp`：`close_review_tasks.py` 的 spec 参数其实就是 stage plan，但宿主惯例叫 `*-plan.json`，所以 close 之前必须
`cp $D/surface-stage-plan.json $D/surface-plan.json` 和 `cp $D/contextual-stage-plan.json $D/contextual-plan.json`。漏了会连废 close 和 index 两个阶段。

耗时参考：`batch-start` / `surface-export` / `contextual-export` / `finalize` 各约 110 秒，`adjudication-chain` 约 240–250 秒，其余都在几秒内。

### 3.3 派发 child 的生命周期（顺序不能乱）

每个 child 严格按这个顺序，**同一时刻只能有一个 create 在飞**：

```
list_profiles（实时，MCP）
  → make-profiles-capture.py 写 $D/$BID-<dispatch_id>-profiles.json
  → review_lifecycle.py create-intent ... --profiles <那个文件>      ← 输出里有要逐字照抄的 labels
  → MCP create_agent（labels 逐字照抄，settings 见下）
  → submit-event.py create <key> <创建响应文件> <started_at>
  → MCP get_agent_status（第一次实况）
  → 程序化比对 labels（不要肉眼看）
  → review_lifecycle.py bind ... --capture <状态响应文件>            ← 注意 bind 没有 --agent-id 参数
```

child 返回后：

```
MCP get_agent_status
  → submit-event.py harvest <key> <状态响应文件> <started_at> --notified <attentionTimestamp> NATIVE_LOG=<原生日志路径>
  → review_lifecycle.py archive-intent ... --capture <同一个状态响应文件>
  → MCP archive_agent
  → submit-event.py archive-response <key> <{"success":true}> <started_at>
  → MCP get_agent_status（新的一次，此时应为 closed）
  → submit-event.py archive-confirm <key> <closed 状态响应文件> <archivedAt>
```

要点：

- journal key 格式是 `<task_id>|<dispatch_id>`。surface lane 的 task_id 就是 `$BID`；contextual 的是 `$BID-contextual-000`。
- **`harvest` 要的是 `get_agent_status` 的响应（`{status, snapshot}`），不是 child 返回的契约 JSON。** 输出正文由 `review_lifecycle.py` 从 `--native-log` 里提取。
- `--notified` 传 snapshot 的 `attentionTimestamp`。
- `started_at` 必须 ≤ `ended_at`，用 `date -u -d '-N seconds' +%Y-%m-%dT%H:%M:%S.%3NZ` 取一个略早的时刻。
- 原生日志位置：Codex 在 `/home/paseo/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<sessionId>.jsonl`；Claude 在 `/home/paseo/.claude/projects/-workspace-tome4-chinese-translation/<sessionId>.jsonl`。sessionId 取自 snapshot 的 `persistence.sessionId`。
- host-event 的 summary 字典**不带** `lineage_verified`，要确认得直接读 journal 文件。
- 收尾正确的样子：`validation_state=completed`、`archive_confirmed=true`、`lifecycle=archived`、`lineage_verified=true`。

### 3.4 两类 child 的固定配置

两个 profile 已冻结多批未变，`list_profiles` 返回的 11 条 profile 自第 124 批起逐字节相同（canonical sha256 `09eb86a681f32e36c220354f27de7d8f7e049422d294a569a9192599134d3940`）。**每批仍要实时调用**，变了要停下来看。

| | surface lane ×4 | contextual ×1 |
|---|---|---|
| profile | `legacy_favorite:codex:gpt-5.6-sol`（Review Gate — Sol） | `agent_profile_mtjlooyy_myzr9tapied`（Cross Reviewer - Opus） |
| provider | `codex/gpt-6-astra` | `claude/claude-opus-5` |
| settings | `{"modeId":"auto-review","thinkingOptionId":"xhigh"}` | `{"modeId":"auto","thinkingOptionId":"xhigh"}` |
| features | 不传 | 不传 |
| 典型耗时 | 每条 60–110 秒 | 130–480 秒 |

`create_agent` 的 emit 里**没有** `features` 键，不要自己加。

surface lane 的提示词由 `dispatch_surface.py` 生成，照抄 `create-intent` 输出即可。contextual 的提示词由 `$D/dispatch-contextual-hardened.py` 里的 `build_prompt` 生成，**有 800 字节硬上限的 assert**，改动前先量字节。

---

## 4. 证据发布与提交（一步都不能省）

顺序固定：

1. 确认目标目录**不存在**：`evidence/production-review-v2-lite/batches/$BID`
2. `cp -r` 一次（重跑会嵌套目录，不要重跑）
3. `diff -r` 源与目标
4. 两边逐文件 sha256 集合比对
5. 文件账目：磁盘上 15 个 ↔ manifest 记账 15 个（4 个顶层 + 4 surface in/out + 1 group manifest + 1 contextual in/out）
6. 重算 4 个可验证内容哈希：`results_sha256`、`adjudications_sha256`、`gates_sha256`、`ordered_revisions_sha256`（后者 = `_sha(wp1.canonical_bytes(man['ordered_revisions']))`）。`entry_snapshots_sha256` 存在 sqlite 里，**这一步验不了，不要假装验过**
7. 14 条 `adapter_refs` 哈希断言（5 个 ref：4 surface 各 3 项 + 1 contextual 2 项）
8. `manifest.base_commit` == 提交前 HEAD
9. journal 的 `raw_output_sha256` == 已发布 contextual 的 `output_sha256`
10. 4 条 surface lane 的 journal 输出哈希集合 == 已发布集合
11. 每条裁决的 `conclusion` / `disposition` / `repair_required` 与 `host-decisions.json` **逐字**相同
12. `git add` 用显式路径（两条：证据目录 + `evidence/quality/production-batches/$BID-source-workset.json`），**绝不 `git add -A`**
13. 确认 `.ai/consult/` 没进暂存
14. commit，然后 `finalize --commit <新 sha>`

几个容易被自己骗过去的地方：

- `wp1` 的导入方式是 `sys.path.insert(0,'tools')` 后 `from i18nlib import production_review as wp1`。
- `adapter_refs` 里合同字段叫 `contract`，**不叫 `kind`**。
- `adapter_refs` 里的路径是**仓库相对**，不是批次目录相对。
- `gates.json` 的 check 行用 `exit_code` 判定成败，**没有 `status` 字段**。写 `c.get('status')=='PASS'` 会全体返回 None 然后判 False，看起来像门禁挂了。
- `adjudications.jsonl` 的行**没有 `layer` 字段**，层次要从 `observation_contract` 推（`translation_surface_screen_v1`→surface，`translation_contextual_v2`→contextual）。
- `finalize` **必须**带 `--commit <sha>`。

---

## 5. host-decisions.json 的写法

顶层恰好两个键：`{workset, decisions}`。`workset` 是 `evidence/quality/production-batches/$BID-source-workset.json`。

`decisions` 的键是 `<revision identity 前 10 字符>|surface` 或 `|contextual`。**键的数量 = surface 判 ISSUE 的条数 + contextual 判 ISSUE 的条数**，OK 的不出现。

每个值恰好三个字段：`{disposition, repair_required, conclusion}`。合法 disposition：`confirmed` / `pending` / `advisory` / `refuted`。**非 confirmed 的必须 `repair_required: false`。**

`conclusion` 是写给未来的人看的，不是给流水线看的。惯例是写清楚：结论成不成立、按固定 commit 的哪一行、目录里哪几行、修复范围到哪为止、哪些同族行不在本批因此要另行清理、跨组件核查结果。两层都判 ISSUE 时，contextual 那条主要写它比 surface 多给了什么。

---

## 6. 每批要写的四个宿主文件

都放在 `$D/` 下，不进 git（`.artifacts/` 被 ignore）：

| 文件 | 内容 |
|---|---|
| `host-independent-research.json` | **在 contextual child 返回之前写定**。对每条 surface ISSUE 独立复核，按固定 commit 查实现、回目录查同族行。这样裁决时手上有一份不受 child 影响的判断 |
| `contextual-tool-audit.json` | 从 child 的原生日志里提出全部工具调用，跑下面第 7 节的检查 |
| `host-decisions.json` | 裁决 spec，见第 5 节 |
| `prior-batch-runtime-scratch/NOTE.json` | 归档上一批 contextual 暂存时的记录 |

---

## 7. contextual 子 agent 的工具边界审计

每批从原生日志提取工具调用后跑这几项：

- **A**：有没有直接读 `locales/` 或任何译文/术语文件。应为 0。
- **B**：每一次 `git grep` 是否都带 `':!*/locales/*'`。注意区分 `git grep`（需要 pathspec）和 `git show <pin>:<path> | grep`（作用域已被单文件限定，不需要也不能带）。
- **C**：引擎访问是否按固定 commit 定址（`git show <sha>:path` / `git grep <sha>`），而不是读工作树路径。
- **D**：有没有写文件（重定向、tee、mkdir、cp、mv、rm）。应为 0。
- **E**：除本批输入信封外有没有碰别的 `.ai` 路径。应为 0。
- **F**：child 判 OK 而 surface 判 ISSUE 的条目，从它的调用记录看它到底查没查过。**这一项直接决定裁决时能不能推翻它**——查过之后的 OK 要带理由才能推翻，漏看的 OK 可以直接不采。

A/B 两项的由来：第 122 批发现 contextual child 通过 grep 读到了 locale 行，等于绕过了「不看现有译文」的独立性前提。提示词在第 123、124 批两次收紧，第 124 批立了「连续三批干净才算关闭」的门槛。124/125/126 三批达标，已关闭。第 127 批还额外做到了**直接观测到拦截**——6 次 grep 里有 2 次的排除实际挡下了共 16 行 locale（第 126 批只能证明合规，因为那批唯一的查询本来也不会泄漏）。

**关闭不等于免疫。** 后续任何一批出现没带排除的 grep，按新证据处理直接重开，不需要重新攒三批。A/B 继续每批跑。

---

## 8. 需要用户拍板的悬而未决项

这几项我都刻意没有自行决定，接手后也请不要单方面定：

1. **上游英文与实现矛盾时跟哪边**（第 101 批提出，第 127 批 `5066bd7e75` 是第二个具体样本）。
   装置掌握的英文把「所有可用物品」只挂在能量消耗上，但 `Object.lua:211-220` 与 `:290-303` 显示缩减对全部可用物品生效、且能量与冷却都管。中文比英文更贴近代码。第 127 批裁了 advisory 不修复（保守：不把更准的描述改成更不准的），但政策本身没定。

2. **gauntlets 的译名是否全目录改**（第 127 批新提）。
   `gauntlets.lua:22-35` 的 BASE_GAUNTLETS 是 `slot="HANDS"`、`subtype="hands"`，desc 写明是覆盖手到前臂中段的金属手套。目录译作「臂铠」共 26 处，含三条基础物品名；另有「护手」7 处并存。单改一行只会更乱，要改就是全目录术语决定。

3. **冻结 matcher 是否加「全库字面量回退」**（多批累积）。
   目前证据是 1 支持（第 124 批的 `loadChatFile` 间接引用 MISS）对 2 反对（第 115 批 `41daf7da3d`、第 119 批 `463ead50e5`）。我一直建议**不加**：回退会锚到 locale 文件，把问题盖住而不是解决。那个支持案例之所以干净，靠的是我显式排除了 `locales/`，而提案本身没有这一条。

4. **Elvala 回忆录是否整篇清查**（第 120/123/125 批分别在第 2、4、6 章由互不相干的 lane 查出缺陷）。
   三章三次独立命中，整篇质量存疑。但这是主动扩大范围，没有用户的话不开。

5. **修改条目的归因汇总工具**（早前提过没做）。
   走 migration 链聚合被改过的条目，按 `recorded_by` / 批次归因。

---

## 9. 只观察、暂不清扫的缺陷形态

这些是反复出现的模式，记着有助于在审读 lane 输出时判断，但不要据此主动发起全库清扫：

- **邻行串条**：正确译法就在同族的几行之外。累计 7 例以上，目前最稳定的形态。
- **同族例外**：一族里只有一条译错，其余都对。第 124–125 批集中出现。
- **整族同错**：全族共享同一处错误，族内自洽反而掩盖问题。第 124 批巫师成就、第 127 批 Momentum 的两条提示。
- **同族分裂**（第 127 批新记）：族内两种译法各半，谁也不占多数。四条龙息兄弟行里 `apply power` 两条译「强度」（对）两条译「几率」（错）。**这种形态下拿同族一致性做交叉验证会完全失效**，两边都能找到支持自己的兄弟行。
- **术语撞车**：一个中文词被两个不同英文机制占用。第 126 批「撕裂位面」。
- **跨分支串条**（第 127 批新记）：文本从同文件另一个聊天分支串过来。第 127 批 `4f371d118c` 的「你在这等着」出自 `alchemist-hermit.lua:348` 的另一分支。比邻行串条更难发现，因为两段文本在游戏里不会同时出现。

候选译名要**双向**查冲突：既查候选撞不撞别人，也查它自己是否已被别的英文词占用。

---

## 10. 已记录但超出批次范围的后续清理

按批次记的，没有合并成清扫任务：

- 第 126 批：`:12669`（众生之皮的 logPlayer 行，与 `:12668` 同一处「人皮」错误）
- 第 127 批：`:24736`（冰龙龙息同样把 apply power 译作「几率」）
- 第 127 批：`:26627`（Momentum 另一条提示同样丢「近战」，且这条才是持弓玩家实际看到的）
- 第 127 批：`:26614`（装置掌握 npc 版把 charms 译作「饰品」，与 `:23569` 的「护符」不一致）
- 第 127 批：`:26765`（Morrigor 专名未译，与 `:12847`「摄魂剑·莫瑞格」不一致）
- 第 127 批：`:24722` `:27097` `:31221` 三处「受技能等级」未核对英文原文
- 更早：`:28007` bowman 描述凭空多出「身穿皮甲」；巫师成就 5 行；`:12864`/`:12868`/`:12870`/`:12872` 臂铠行；孤儿行 `:25931`；`:9465` glowing cyan→炽热；`:12762` 无来源的「白」
- 标记内多余空格清理：291 处单向不对称，清理窗口自第 76 批后开启，Rimebark 保持「召唤：雾凇」
- 第 95 批遗留 advisory C3：mid-log `atis-latch` 形态未充分验证

---

## 11. 踩过的坑

- **前台 Bash 有 2 分钟硬上限。** 长阶段用 `nohup ... &` 起，再在有界循环里轮询产出文件。
- **不要在 `run_in_background: true` 的 Bash 调用里再 nohup 一条链**——链会被回收。要用前台 Bash 调用起 `nohup ... &`，然后另起一次调用轮询。
- `run-host-phase.py` 只要发现 `<name>.log` 或 `<name>-result.json` 已存在就拒绝跑。重跑前要么换名字，要么确认真的该重跑再挪走旧文件。
- **数字要标明实测还是估算，算式两边都要带量纲。** 相减之前先对齐三元组：什么量、什么环境、什么尺子，三项不全同就不许相减。
- **「已拒绝」不代表没执行。** 重跑前按不可逆性从高到低查实际状态；`cp -r` 重跑会嵌套目录。
- **自然语言正文不经过 shell 插值**：heredoc 定界符要加引号（`<<'EOF'`），否则内容会被静默改写。
- **放行结论要先查前置条件**：说「可以开批了」得贴出命令和输出；退出码非 0 不等于「不存在」。
- **修复要对照整句改，不能只改被点名的从句**——第 84 批重写整句却留下同句旧错，第 85 批被重报。
- **投影内存是硬上限**：单次约 10 GB，两个并发会从 155 秒退化到 91 分钟。安静窗口是硬约束。
- `contextual-import` 必须先 `write_states` + `DONE_VERIFIED` 才能跑；漏跑的症状是报「多余裁决」且全是 contextual。第 81、82 批各犯过一次。

---

## 12. 最近五批结果

| 批次 | batch_id | commit | base | 冻结 | surface | contextual | 裁决 | 门禁 |
|---|---|---|---|---|---|---|---|---|
| 123 | `batch-d9a15a241fd52892ab09` | `a266ec0` | `8b0ddd7` | 80/80 | 74 OK / 6 ISSUE | 6 ISSUE / 0 OK | 12 键全 confirmed，6 条修复 | 17/17 `run.n0huwzs5` |
| 124 | `batch-990a37ec840dea1c222e` | `bfd909e` | `a266ec0` | 79/80（1 MISS） | 75 OK / 5 ISSUE | 5 ISSUE / 0 OK | 10 键全 confirmed，5 条修复 | 17/17 `run.jrstyzml` |
| 125 | `batch-b8a9ec0635c6b10ff589` | `57a5301` | `bfd909e` | 80/80 | 75 OK / 5 ISSUE | 4 ISSUE / 1 OK | 9 键：8 confirmed + 1 advisory，4 条修复 | 17/17 `run.fice43qx` |
| 126 | `batch-8924680824c91795046c` | `acd17fd` | `57a5301` | 80/80 | 78 OK / 2 ISSUE | 2 ISSUE / 0 OK | 4 键全 confirmed，2 条修复 | 17/17 `run.6plad8dh` |
| 127 | `batch-de3f7672e4bb0c4f11b3` | `7d1909d` | `acd17fd` | 80/80 | 72 OK / 8 ISSUE | 6 ISSUE / 2 OK | 14 键：13 confirmed + 1 advisory，7 条修复 | 17/17 `run.1wov4zu3` |

第 127 批两层在两条上判断相反，都带理由处理、没有默认取某一侧：`502b32c23d`（Momentum）推翻了 contextual 的 OK，`5066bd7e75`（装置掌握）采纳了它。推翻前先查了原生日志确认那个 OK 是知情判断——这个动作建议保留成惯例。

---

## 13. 接手后开第 128 批的最短路径

```bash
cd /workspace/tome4-chinese-translation
git rev-parse HEAD                                   # 应为 7d1909d
python3 -B tools/i18n production batch show          # 应为 {"active": false}
git status --porcelain                               # 应只有 ?? .ai/consult/
ls .artifacts/i18n/production-review-v2-lite/contextual/   # 应为空
```

四项都对就按第 3.1 节搭脚手架（**第 128 批可跳过暂存归档，已代做**），然后从 `batch-start` 顺次往下。
