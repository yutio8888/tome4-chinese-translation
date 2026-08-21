# Paseo Provenance/Schema Redesign 交接

> 类型：当前状态记录，非契约、非门禁。
> 权威设计内容见任务自身产物（下列路径），本文件只是导航和裁决摘要。

## 0. 一句话状态

`paseo-provenance-schema-redesign-001` 的**设计／validator 审核循环已完成并被用户
接受关闭**（2026-08-20）。产出：provenance anchor 机制（§2）、STATE schema 决策
（§3，`lifecycle` + 大小写混合角色，canonical write + backward-compatible read）、
以及一套用命名 predicate 表达的 `DONE(task)` closure 契约（§3.4–§3.9），配一份
经过 5 轮独立审核验证的参考实现 `validate_fixtures.py`。**尚未开始**：`tools/
ai_state_check.py`（P0-1，真正的 offline checker）和它的生产级 fixture 套件
（P0-4）。这两项是**新任务**，不在本任务范围内。

## 1. 产物位置

全部在 gitignored 的 `.ai/task/paseo-provenance-schema-redesign-001/` 和
`.ai/reviews/paseo-provenance-schema-redesign-001/` 下，**接任者必须先读，本仓库
git 历史里找不到这些文件**：

- `.ai/task/paseo-provenance-schema-redesign-001/DESIGN.md`（1023 行，权威设计
  文档，§0–§11，含每轮审核 ledger）——**唯一的规范来源**，本交接文档只是索引。
- `.ai/task/paseo-provenance-schema-redesign-001/validate_fixtures.py`（592 行，
  参考实现，29 个 adversarial fixture + real-corpus dry-run；明确不是
  `tools/ai_state_check.py`）。
- `.ai/task/paseo-provenance-schema-redesign-001/SPEC.md`（round 5 的窄范围
  SPEC，历史存档，不是下一步任务的 SPEC）。
- `.ai/task/paseo-provenance-schema-redesign-001/STATE.json`（`state: "DONE"`，
  完整 `child_dispatches` 历史，10 个 child，5 轮）。
- `.ai/reviews/paseo-provenance-schema-redesign-001/review-01.json` 至
  `review-10.json`（5 轮 × 2 reviewer 的完整审核记录）。

## 2. 五轮审核摘要（不要重新论证已裁决内容）

| 轮 | Reviewer A / B | 结果 | 内容 |
|---|---|---|---|
| 1 | Sol / Sonnet | `CHANGES_REQUIRED` | 9 blocker + 1 hardening（原始设计） |
| 2 | Sol / Grok | `CHANGES_REQUIRED` | round 1 的 9 个修复中 5 个不完整 + 2 个 low |
| 3 | Sol / Grok（fresh） | `CHANGES_REQUIRED` | round 2 修复仍有 5 个 blocker——根因是
  closure 模型本身（独立布尔检查清单），不是零散 bug。触发**closure/lineage
  contract normalization**：`DONE(task)` 改写为具名 predicate 组合，新增
  `completion_records` 外键关系（`dispatch_id` → role/purpose/agent_id 匹配） |
| 4 | Sol / Grok（fresh，verification round） | `CHANGES_REQUIRED` | round 3 规范
  文本本身正确，但 `validate_fixtures.py` 有 3 处未真正实现规范
  （`schema_valid` 未接入、`candidate_bindings_valid` 大量绕过、legacy delivery
  lineage 未真正按 `dispatch_id` 匹配）。**只改代码，`DESIGN.md` §3 规范文本未动** |
| 5 | Sol / Grok（fresh，narrow remediation verification） | **`PASS`/`PASS`** |
  确认 round 4 的 3 个 blocker 均已修复，双方各自构造额外对抗输入未发现新问题 |

**非 Claude cross-reviewer 是本任务的硬性要求**（用户明确指示，因为 `DESIGN.md`
是 Claude 撰写的）：Reviewer A 固定用 `codex/gpt-5.6-sol`；Reviewer B 优先非
Claude、非 OpenAI（本任务全程用 `grok/grok-4.6`，因为 Gemini/GLM 的 Paseo
profile 当时都限定在 prep/implementation 用途，不适用于 review 角色——如果接任者
要用 Gemini/GLM 做 review，需要先跟用户确认 profile override）。

## 3. 关键裁决（接任者不要推翻，除非有新的、可复现的 counterexample）

- **STATE schema**：canonical write 用 `lifecycle` + `EXECUTOR|REVIEWER|SCOUT|
  senior-reviewer`；legacy `status` 和小写角色仍作为**只读兼容别名**，不迁移
  历史文件。`DESIGN.md` §3 记录了 ACCEPTED 决策原文，不可重新论证。
- **Legacy 判定机制是冻结的 `.ai/legacy-cohort-manifest.json`**（尚未实际创建，
  P0-1 实现时才需要），不是 commit/timestamp 推断——后者已被证明不可行
  （`.ai/task/`、`.ai/reviews/` 是 gitignored，不进 git 历史）。
- **`legacy_profile` 由 manifest 冻结、不在 check time 重新推导**——这是用户
  明确裁决的（round 4 reviewer 之间对此有分歧，用户直接定案）。
- **10 个真实 `p2-*-dialogue-b*-001` delivery 任务的正确结果是
  `LEGACY_UNVERIFIABLE`，不是 `LEGACY_VERIFIED`**——因为它们从未持久化
  `review_records` 字段。**这不是缺陷，不要"修到"让它们变成 VERIFIED**；这正是
  `LEGACY_UNVERIFIABLE` 这个结果存在的原因（诚实地表达"这条历史记录没有可机检的
  证据"，不代表已交付的工作有问题）。
- **`.ai/roles/orchestrator.md` 的 `candidate_ref` 拼接方式仍未精确定义**
  （只说"SPEC 与 diff 精确字节的 SHA-256"，没说拼接顺序/分隔符/编码）。已记录为
  backlog item，本任务明确不解决——这属于修改 `orchestrator.md` 契约文件本身，
  超出本任务范围（`DESIGN.md` 开头即声明"scope: this document only"）。

## 4. 暂停点与接任后第一步

**当前没有暂停的工作——round 5 是干净的终态。** 唯一悬而未决的是：

1. **是否以及何时启动 P0-1（`tools/ai_state_check.py`）和 P0-4（生产 fixture
   套件）的实现。** 这是新任务，需要用户明确授权范围（是否新开
   `paseo-ai-state-checker-001` 之类的 task_id）。`validate_fixtures.py` 可以
   作为实现的起点参考，但它本身是 throwaway 设计验证脚本，不能直接改名当
   production 工具用——至少需要：加真实文件 I/O（当前是纯内存 dict）、真正解析
   `.ai/legacy-cohort-manifest.json`（当前 fixture 用内联 dict 模拟）、把
   `candidate_ref` 拼接方式的 backlog item 解决掉。
2. 上述新任务如果要走 Paseo 编排，接任者是新 ORCHESTRATOR：必须有非空
   `PASEO_AGENT_ID`，写入新任务自己的 `orchestrator_agent_id`，不要复用本任务的
   `aeb4c6e3-e627-4ce1-8271-c9435a8b288e`。

**接任者不要自动开始 P0-1/P0-4 实现**，等用户明确指示范围和是否新开任务。

## 5. 编排约定（沿用本任务已验证的模式）

- 每轮 review 前先冻结候选（本任务用"哪些章节 + 哪些历史 review 记录"的组合），
  写清楚 in-scope / out-of-scope，避免 reviewer 重新探索已裁决内容。
- 每个 child 收获后先持久化 `archive_attempts_started` 再调用
  `archive_agent`，确认归档后再更新 `archive_confirmed: true`。
- 发现 blocker 后 ORCHESTRATOR 独立核验每一条 finding（对照实际文件/代码），不
  直接采信 reviewer 自报的严重程度或结论——本任务全程如此，多次发现 reviewer
  的部分论断需要修正或降级（例如 round 4 中 Grok 把某项从 blocker 降级为
  hardening，ORCHESTRATOR 独立复核后认可）。
- 如果同一根因连续多轮产生新 blocker（本任务 round 2→3 即是），考虑是否需要
  "normalization"式的结构性重写，而不是继续逐条打补丁——round 3 的教训。
- Verification round（确认修复是否真正生效）应该用**收紧的 blocker 判据**
  （必须有可复现的 execution path/artifact state，不接受"理论上还能更严格"），
  否则容易变成新一轮开放式 design review——round 4/5 SPEC 的写法可以直接复用。

## 6. 不要做的事

- 不要重新论证 §3 的 schema 决策、legacy manifest 机制、`legacy_profile` 
  trust-not-derive 裁决——均已 ACCEPTED，需要新的可复现 counterexample 才能
  重新讨论，单纯"觉得还可以更好"不算。
- 不要为了让 10 个真实 delivery 任务显示 `LEGACY_VERIFIED` 而弱化
  `legacy_verify()` 的匹配逻辑——`LEGACY_UNVERIFIABLE` 是诚实的正确结果。
- 不要在没有用户明确授权的情况下开始 P0-1/P0-4 实现。
- 不要把 `validate_fixtures.py` 直接当 production 工具使用或引用——它是纯内存、
  无文件 I/O 的设计验证脚本，明确标注"NOT tools/ai_state_check.py"。
- 不要用 Claude 模型做本任务后续任何审核角色（reviewer 或 senior-reviewer）——
  `DESIGN.md` 由 Claude 撰写，用户明确要求独立性。
