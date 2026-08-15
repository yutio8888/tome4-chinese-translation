# Handoff — Paseo 语境翻译复审通道完成与质量审计恢复点

> 交接时间：2026-08-15
> 仓库：`tome4-chinese-translation`
> 当前分支：`develop`
> 当前 HEAD：`61bb370c33e46c4df4b2bbfd56113a0de1822300`
> 当前 `origin/develop`：`2c3d83c657def449343c71ff2ba31cdf0f9812da`（本地领先 6，落后 0）

## 一、当前恢复点

- Paseo 实现任务 `translation-context-review-mcp-001` 已进入 `DONE`，没有未解决或 deferred
  finding；当前没有运行中的 EXECUTOR／REVIEWER／SENIOR_REVIEWER。
- 最终任务候选：
  `92d54977e0ff6db6e97fcd4e6af8b747f12d23a11a1d909935e80fb9fcb15788`。
- 实现尚未 stage、commit 或 push；当前 task-content 工作树为：
  - `M AGENTS.md`
  - `M .ai/roles/orchestrator.md`
  - `M .ai/roles/reviewer.md`
  - `M docs/paseo-orchestration-v2-contract.md`
  - `M tests/i18n/test_toolchain.py`
  - `?? docs/paseo-translation-context-review-v1-contract.md`
  - `M handoff.md`（本文件，本次按用户要求重写）
- `.ai/task/translation-context-review-mcp-001/` 与对应 `.ai/reviews/` 为已忽略的编排记录，
  已完整保留候选 diff、candidate ref、审查和范围裁决，不进入提交。
- 除非用户明确要求，不 push；提交时不要混入其他任务或 ignored 编排产物。

## 二、本轮已完成：translation_contextual_v1

本轮新增了 Paseo 托管的、非盲且有上下文的补充翻译复审通道
`translation_contextual_v1`。它与既有 blind `translation_v2` 双向隔离：不会完成、替换或计入
blind v2 contract，也不会把 blind observation、历史 finding、裁决或修复建议注入语境复审。

### 1. REVIEWER 路由

同一个 REVIEWER 角色按审核契约和控制面 purpose 选路：

| review contract | `labels.purpose` / 记录 purpose | 载体 |
|---|---|---|
| `code_legacy_v1` | `normal_review` | Codex `gpt-5.6-sol` / `auto-review` / `xhigh` |
| `translation_contextual_v1` | `translation_contextual_v1` | Pi `opencode-go/deepseek-v4-flash` / mode null / `max` |

- code-only Codex 元组谓词只适用于 `normal_review`，不会误杀合法的语境 Pi REVIEWER；
- contextual 路由不静默降级、不回退 Codex；创建或恢复后核验完整
  Provider/Model/Mode/Thinking；不匹配即停止并按基础设施错误处理；
- agent 必须由 ORCHESTRATOR 通过 agent-scoped Paseo MCP `create_agent` 直接创建，继承同一
  workspace 和父级 lineage；MCP 无法提供可验证 lineage 时停止 child 并进入 `WAIT_USER`。

### 2. 候选身份与派发

- `candidate_identity` 是八键 canonical JSON payload 精确 UTF-8 字节的 SHA-256；键递归按字节序
  排序，数组保留冻结顺序，紧凑分隔符，`ensure_ascii=false`；
- payload 不包含计算后的 identity 值；外层 envelope 携带
  `{candidate_identity, payload}`，其精确 JSON 文本映射到 MCP `initialPrompt`，CLI 等价为
  `paseo run` 的 positional prompt；`--json` 仅控制 CLI 输出格式；
- 规范向量摘要保持：
  `ae6923cf13f7662ee609155c690da1abaa3117a8b0ce07ce079ada3284f9378b`；
- 哈希前及接受结果前都校验固定 contract、Pi runtime tuple、manifest 固定源码 commit、冻结
  revision 顺序以及 source/target；空 key/source/target 或语义不匹配均失败关闭；
- agent label、条件 STATE 字段和 review 记录中的 identity 是允许且必需的控制面副本，不参与
  payload 身份计算。

### 3. 恢复、结果和只读边界

- 正常 contextual 派发使用 fresh agent；创建结果不明时按 workspace、task、role、purpose、
  精确 `candidate_identity` 过滤后再做 0/1/多基数判定；
- 旧候选 agent 在 identity 过滤阶段排除，不算当前候选匹配；过滤后零匹配只允许现有的一次
  bounded retry；列表截断／不完整、缺省 purpose 歧义、多个当前候选或无法证明唯一性时进入
  `WAIT_USER`；
- 结果 envelope、revision 和 evidence 对象均为 closed schema；revision 集合与顺序必须精确，
  evidence source/target 与冻结值逐字节相等；任何缺失、额外字段、重复、乱序、错候选或畸形
  输出均失败关闭，不部分接受；
- REVIEWER 只读。派发前后比较 HEAD OID、候选路径、任务前脏／未跟踪路径以及路径精确的
  decision-critical ignored 文件；ORCHESTRATOR 合法写入只使用有限的路径精确 allowlist。
  不建设通用文件系统监控，也不对整个仓库或 ignored tree 做全量哈希。

### 4. 条件 STATE 记录

任务选择 `translation_contextual_v1` 时，STATE 需要独立的 `contextual_reviewer`：

```json
{
  "provider": "pi",
  "model": "opencode-go/deepseek-v4-flash",
  "mode": null,
  "thinking": "max",
  "purpose": "translation_contextual_v1",
  "candidate_identity": null,
  "agent_id": null
}
```

未选择该 contract 的任务不添加字段，也不迁移；既有 `reviewer` 块仍是 code
`normal_review` 的 Codex 载体。

## 三、验证与审核结果

- `PaseoTranslationContextReviewTests` + `ProjectSubagentDefinitionTests` + STATE tests：80 tests OK；
- `tests/i18n/test_toolchain.py`：480 tests OK；
- `tools/ci-gates.sh --skip-build`：全部门禁通过；
- `git diff --check`：通过；无 staged 文件；
- 第 9 轮 normal / senior re-review：双 PASS；
- 第 9 轮 normal / senior FINAL_REVIEW：双 PASS，无 actionable finding；
- final diff SHA-256：
  `2c2ad9552e1a0f283b253e7db26bb97573dc3085b6288b216e5a6e0bf444fb6d`；
- final candidate ref：
  `92d54977e0ff6db6e97fcd4e6af8b747f12d23a11a1d909935e80fb9fcb15788`。

Claude Opus 首选路由本任务因 provider 明确返回未登录错误而在有效输出前失败；任务按契约锁定
Codex `gpt-5.6-sol` / `auto-review` / `xhigh` fallback。该情况已记录，不是候选缺陷。

## 四、仍在等待决定：quality-audit-002

`.ai/task/quality-audit-002/STATE.json` 仍为 `WAIT_USER`，恢复点是 `REVIEW`。已冻结：

- component：`tome`；
- offsets：`13661`、`12591`；
- 每组 10 条，共 20 个互不重叠 revision；
- 固定引擎源码 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`；
- translation SHA：
  `7b6e39e0de6895fda30503a0fb095b50685dfeaa9d222bbf849c4119ba2ba05f`；
- selection SHA：
  `51ea7148283a5d4b8329bf199d99434799d48357eb137d8cfa0746b9c30c22a6`。

此前三次旧 `$tome4-pi-review` 尝试均已作废：Paseo 已激活时不应使用旧 Skill，且前两次还受
Codex sandbox 网络限制影响，没有有效结果。不要复用这些输出。

新实现的 `translation_contextual_v1` 是补充通道，不能替代 `quality-audit-002` 已冻结的 blind
`translation_v2` contract。因此继续前需要用户明确选择：

1. 允许 ORCHESTRATOR 直接运行现有 blind translation-v2 runner（不是旧 Skill），恢复
   `quality-audit-002`；或
2. 暂停 blind audit，另建独立任务，用 `translation_contextual_v1` 对明确选择的 revisions 做
   有上下文补充复审；结果独立记录，不计入 quality-audit-002 的 blind 指标。

## 五、推荐下一步

1. 先由用户决定是否提交当前 7 个工作树路径；若提交，建议单独提交本次 Paseo contextual
   review contract，不混入 ignored task/review 记录，也不 push；
2. 再对 `quality-audit-002` 的两条恢复路线作出明确选择；
3. 若恢复 blind route，先重新核验冻结 selection 与当前 translation/manifest SHA 未漂移，再从
   STATE 的 `REVIEW` 恢复；
4. 若选择 contextual route，新建独立 task ID，冻结 candidate identity 和条件
   `contextual_reviewer` STATE，不改写 `quality-audit-002` 的历史记录。

## 六、持续约束

- Paseo 激活期间不使用 `$tome4-pi-review`、`$tome4-pi-file-review` 或
  `$tome4-pi-subagent`；委托与复审只走 Paseo 角色；
- blind `translation_v2` 仍不得注入术语、Facts、源码或历史 finding；语境复审也不得看到
  blind observation；
- Facts 通道仍为 `do-not-promote-facts-channel`；
- 机制事实以 manifest 固定源码为准；译文、术语和模型 finding 不能覆盖源码行为；
- 自动化统一使用 `python3 -B tools/i18n <command>`；Lua 只用项目 LuaJIT / Lua 5.1 环境；
- 译文或术语修改后按 `AGENTS.md` 运行对应完整门禁；
- 未经用户明确要求不 push。
