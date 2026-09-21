# 翻译审核当前交接

更新时间：2026-09-21（审核 243、修复窗口 1 语境复审补做完成后）
移交对象：Paseo / Codex / GPT-6-Astra
交接时 HEAD：`b490451`（develop）；工作树干净；`production batch show` → `active:false`

## 一、交接时的事实基线

先核对这些，再决定下一步。不要凭本文件的叙述代替实测。

| 项 | 值 |
|---|---|
| HEAD | `b490451` |
| 已 push 到远端的最后一个 commit | `3873a75` |
| **未 push 的本地提交** | `998699d`、`baa6307`、`6dd7ca6`、`a419d4b`、`7295c1e`、`d5b7665`、`b490451`（7 个，实测 `git log origin/develop..HEAD`） |
| 最后一次 queue rebuild | `rw1remed-queue-rebuild-2`，rc=0，216.048s，reconciliation 29828 |
| 当前 catalog_id | `4ec0ae983f6b435c31883e06cdc96800a88189758f2503f4e0c7e0375c203b8c` |
| 审核进度 | 已完成至批 **243**，下一审核批 **244** |
| 修复进度 | 修复批 266 已完成；修复窗口 1 已完成并已补做语境复审 |

**push 授权：本宿主全程未获得新增 push / PR / 发布授权，因此上述 7 个本地提交一律未推送。**
接手方若无维护者明确授权，同样不要推。仓库记忆中的「每批完成后 push」是 2026-09-19 的历史授权，
本轮 pilot 通知明确写了「此次通知不新增 push/PR/发布权限」，以后者为准。

## 二、本次完成了什么

### 1. 审核批 242、243（只读审核，已 finalize）

- 242：`batch-14af8bb1984fdbfbe44a`，80 条，6 confirmed / 2 advisory，evidence commit `baa6307`。
- 243：`batch-e32a241e8189e689d1e5`，80 条，10 adjudicated confirmed，evidence commit `7295c1e`。
  真实 finalize receipt 09:14:38.508 → 09:54:25.351 = **2386.843s**。

### 2. 修复窗口 1（commit `6dd7ca6` + `a419d4b`）

改了 4 条：Urh'Rok 火鞭、Time Skip、Shoot、missile launcher 槽位标签。

### 3. 修复窗口 1 的语境复审补做（本次主要工作）

修复窗口 1 当时**没有**契约内的 `translation_contextual_v2` 语境复审。本次建立
`.ai/task/remediate-w1-lines-20260921/` 补做，并在复审中发现并修正了一处真缺陷：

Time Skip 的 `removed from time` 原译「被从这个时空放逐」——「放逐」是 Banish 的技能名
（`mod-tome.lua:22310`），与同段出现的 Time Skip 撞名；语料中该短语一律作
「从时间流中移除／从时间中移除／移出时间线」，「放逐」零用例；「这个时空」是原文所无的增译。
改为「它有几率被移出时间线 %d 回合。」，保留 `may` 的不确定性限定。

- 译文 commit `d5b7665`（1 行）
- 证据 commit `b490451`：`revision_changed 1 / unchanged 29827`，`ambiguous 0`、`unmapped 0`、
  `queued_successors 1`，`old_catalog_id 7c517a18… → new_catalog_id 4ec0ae98…`
- 验收：`python3 -B tools/ai_state_check.py .ai/task/remediate-w1-lines-20260921/STATE.json --target DONE`
  → `DONE_VERIFIED`，**真实 exit 0**

stage 序列（全部经 `tools/contextual_result_check.py` 真实 exit 0 验证后才采纳）：

| stage | kind | 结果 | reviewer |
|---|---|---|---|
| (0,5) | REVIEW/full | PASS | codex/gpt-6-astra |
| (0,6) | FINAL_REVIEW/full | FINDINGS | claude/claude-opus-5 |
| (1,3) | RE_REVIEW/full | PASS | grok/grok-4.6 |
| (1,4) | FINAL_REVIEW/full | PASS | claude/claude-opus-5 |

## 三、本次踩过的坑（接手方最该读的一节）

这些都是实际发生并被纠正的错误，不是假设风险。

1. **v2 REVIEWER 的 prompt 不要自己写。** 我自拟 prompt 要求 OK 时带 `observation: null`、
   外加 `review_phase`/`cross_entry_consistency` 顶层字段，结果**四份 raw 全部**被
   `contextual_result_check` 判非法（契约第六节 root 恰含三键，OK item 恰含
   `revision_key`/`verdict`）。正确做法：
   ```python
   sys.path.insert(0,'tools')
   from contextual_lane_manifest import render_dispatch_prompt
   prompt = render_dispatch_prompt(candidate_identity, input_path)   # 逐字用作 initialPrompt
   ```
   那四份非法 raw/record 仍留在 `.ai/reviews/remediate-w1-lines-20260921/` 作不可覆盖诊断，
   不在 `review_records` 里。**不要为了让它们通过而 strip/重排/删字段。**

2. **v2 child 创建时必须带 labels。** `tools/ai_state_check.py:1938-1956` 要求 dispatch 带
   `task_id` / `role` / `purpose` / `candidate_identity` / `dispatch_id` 五个精确 label。
   我第一轮（attempt 3/4）没设，结果两份**内容完全合法**的 raw 也不能当 terminal，只能以更高
   attempt 重做。事后往 STATE 里补写 labels 等于伪造未发生的派发事实——不要这么做。
   每次派发后用 live `get_agent_status` 回读，连 `workspace_id` 和 parent lineage 一起核验。

3. **范围越界。** 我把 root 明确排除的 `RW1-SIB-01` 仅凭一条 reviewer observation 写进 SPEC
   并派发修改，被巡检拦下。教训原文：**允许读取同 section 锚点 ≠ 允许修改整个 section；
   「显式改 SPEC 留痕」不自动获得 root 委托范围的扩展授权。** 已由 bounded EXECUTOR
   `revert-01` 定点回滚，证据在 `.ai/task/remediate-w1-lines-20260921/scope-violation-20260921/`。
   回滚时明令禁用 `git checkout/restore/stash`——整文件回滚会连带抹掉同一文件里必须保留的修复。

4. **`| tail` 的退出码不是真实 RC。** `migration-chain` 第一次因
   `--candidate-catalog` 指到了嵌套的 `catalog/` 子目录（要的是**根目录**，它校验 exact tree、
   需要 `evidence/…` 与 `i18n/…` 两棵子树）而失败，管道返回 0，`/tmp/ptime.sh` 记下真实 rc=1。
   这一失败浪费了一次 211.66s 投影。失败的 timing 文件保留为
   `window1-remediation-migration-timing.attempt1-failed.json`。

5. **同内容 raw 的 sha256 必然相同。** 同一 `candidate_identity`、同一冻结顺序的全 OK 结果在
   第六节紧凑形状下字节一致，所以 `(0,5)` 与 `(0,6)`、`(1,3)` 与 `(1,4)` 的 raw sha 各自成对相同。
   这不是证据复用，STATE 里已注明；接手方不要据此判定作弊，也不要反过来拿它当「两次独立验证」。

6. **record 的 `result` 只能取 `COMPLETION_VALUES`**（`completed`/`completed_with_findings`/
   `PASS`/`CHANGES_REQUIRED`/`FINDINGS`/`OK`）。我一开始写 `FAIL`，检查器直接拒绝。
   返回 ISSUE 的复审应记 `FINDINGS`。

## 四、待办队列（按建议顺序）

### A. 修复窗口 2 —— 批 243 的 5 条 confirmed

workset：`.artifacts/i18n/repair-window/batch-e32a241e8189e689d1e5.json`（5 items）。

**它的旧 preflight 已失效**：当时 `evidence_commit` 记的是 `7295c1e`，而 HEAD 已前进到
`b490451`。实施前必须**按原批 ID 重新 preflight 到新的输出路径**，不要复用旧产物。

窗口流程（不得省略任何一步）：
译文 commit → 计时 queue rebuild → **单次** catalog build → migration-chain → 证据 commit →
再次计时 queue rebuild。且必须有真正的 IMPLEMENT/EXECUTOR/REVIEW+FINAL 循环，不能重蹈
修复窗口 1「先改后补复审」的覆辙。

### B. 审核批 244

窗口 2 收口（且 push 或明确交接后）再开。批次进行期间不得提交任何东西。

### C. 永久 out-of-scope，不要顺手改

`.ai/task/remediate-w1-lines-20260921/STATE.json` 的 `declined_scope`：

- `RW1-SIB-01` — `mod-tome.lua:30986`「你的弹药与你的**远程发射武器**不匹配。」
  与 canonical「远程投射武器」不一致（全库唯一一处）。
- `RW1-SIB-02` — `mod-tome.lua:30988`「你需要一件**远程武器（弓、投石索等）**和弹药…」
  同一 `archeryAcquireTargets` 失败提示簇内 `missile launcher` 的第三种处理。

两条都**经宿主实测核验确有术语不一致**（`远程发射武器` 计数 1，`远程投射武器` 计数 3；
上游 `@624a67329f…` `techniques.lua:330/333/335` 三串确属同一提示簇）。但它们不在任何已授权任务的
可编辑面内，必须由维护者单独授权的切片或界定清楚的下一修复窗口处理。
按 `docs/agent-workflow.md:189-193`，再次出现同类 observation 直接记 advisory，不重新裁决。

### D. 未决术语，不得自动裁决

- `8b977dd836…`（Archmage → 元素法师）：保持 pending，不改译、不清状态、
  **不计入新增可执行 revision 阈值**，也不得因此阻塞后续审核。
- 批 242 的两条 advisory：`dccaeba2d4`、`dcea67f425`。
- 历史待维护者术语清单见 `docs/handoff-history-through-20260919.md`，本轮未改口径。

## 五、性能 pilot 数据（`perf-repair-window-20260921`）

计时锚点全部在被 git 忽略的 `.artifacts/i18n/perf-repair-window-20260921/pilot/`。
共 72 条 `ptime` 收据，**仅 1 条非零 RC**（上面第 4 点的 migration-chain 首次失败）。
收据时间跨度 05:47:40.010 → 11:31:38.122。

**投影复用确已生效**，本次补做的窗口是干净样本：

| 步骤 | wall | 其中投影 |
|---|---|---|
| queue rebuild #1 | 213.907s | — |
| catalog build | **3.484s** | 复用 |
| migration-chain（成功那次） | 222.906s | plan 215.10s 含唯一一次 211.89s 投影 |
| └ migration:check | **3.106s** | 复用 |
| └ migration:apply | **4.552s** | 复用 |
| queue rebuild #2 | 216.048s | — |
| 完整门禁（17 gates）× 5 次 | 116.3–118.7s | — |

**不要把命令耗时相加当端到端耗时。** 修复窗口 1 的端到端是 05:47:40 → 06:54:20 =
**66 分 41 秒**；此前出现过的 2725.621s 只是 CLI 计时之和，两者口径不同，不可互换。
本次补做未做端到端锚点，如需该数字请实测，**不要从 elapsed 反推**。

## 六、不变量（沿用，未放宽）

- 只允许一个 production writer；活动 checkpoint 内不改译文；`batch start` 到 finalize 之间不提交。
- 不得修改检查器 / 角色 / 契约来放宽门禁。本次五次被 `ai_state_check` 拒绝，全部靠改事实通过。
- 不伪造队列 ISSUE，不改写 `done` 状态，不跨任务借用别的批次的 DONE 当语境复审。
- 派发前先写 intent 与候选身份；归档前先写 archive 预算；归档后回读 status 确认 `closed`。
- 不要新建 `paseo ls` / `pgrep` 轮询等待 shell，用 `notifyOnFinish`。
  （历史上曾遗留三个自匹配、永不退出的 `until ! pgrep …` shell。）
- **不要打开 agent tab**：会把 `attentionReason` 清成 null，harvest/reject/archive 三条路全堵死。
- 子 agent 看不到上游检出（`/workspace/t-engine4` @ `624a67329fe2ad440c5b344785a9c73fcf22ae63`）；
  它们的源码主张宿主必须自己复核。
- 无漂移不要重复 rebuild。
- 2026-09-19 以前的批次细节与事故记录见
  [历史交接存档](docs/handoff-history-through-20260919.md)，只供追溯，不构成当前授权。

## 七、操作入口

- 修复窗口与投影复用命令：[orchestration README](tools/orchestration/README.md#repair-preflight-与-migration-有界串联)
- 调度、20-revision 阈值、无空窗口规则：[代理工作流](docs/agent-workflow.md#wp2-lite-三批修复窗口)
- v2 语境复审契约：`docs/paseo-translation-context-review-v2-contract.md`
- 结果校验：`python3 -B tools/contextual_result_check.py <envelope> <raw>`
- 锚点预检：`python3 -B tools/contextual_anchor_preflight.py <SCOPE.json> <PAYLOAD.json>`（注意是 payload，不是 envelope）
- 唯一权威验收：`python3 -B tools/ai_state_check.py <STATE.json> --target DONE|STOP`
