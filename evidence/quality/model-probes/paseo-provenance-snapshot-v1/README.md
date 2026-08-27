# Paseo 译文审核 provenance snapshot v1

状态：从本机 Paseo 控制面记录派生的脱敏、可重建快照。

日期：2026-08-27

## 目的

本目录将此前只存在于生产工作树 `.ai/task/`、`.ai/reviews/` 和本机 Paseo agent metadata 中的历史关系，固化为可由 Git 跟踪的研究证据。它回答的是：某个批次由哪个模型族编排、修改和审核，经历了多少轮 dispatch，保存了哪些 review artifact，以及 STATE 是否直接记录了交付 commit。

它不把实验 worktree 变成生产裁决来源，也不复制原始 prompt、译文、finding 文本或 Paseo 会话控制面数据。

## 文件

- `SNAPSHOT.json`：任务、dispatch、模型/模式、候选修改者归因、审核者组合、交付 commit 和 review artifact 的脱敏结构化摘要。
- `SOURCE-MANIFEST.json`：进入快照的 task、review 和相关 agent metadata 源文件的逻辑路径、字节数与 SHA-256；不含文件正文。
- `generate.mjs`：只读扫描生产仓库和 Paseo agent metadata，确定性生成前两份 JSON。
- `verify.mjs`：在临时目录重新生成，要求与跟踪文件逐字节一致，并扫描认证、session、native handle、MCP 配置和本机绝对路径等禁入模式。

## 冻结范围与选择规则

生成器先按以下 task ID 范围选取既有 P1/P2 任务：

```text
^(?:p1-b\d|p2-(?:ashes|cults|orcs)-|p2-tome-texts-b\d)
```

随后只保留满足任一条件的 contextual-review 任务：

- `review_contracts` 包含 `translation_contextual_v1`；
- 当前 `contextual_reviewer.purpose` 为该 contract；
- 历史 `child_dispatches` 中存在对应 reviewer dispatch。

第三条很重要，因为完成归档后当前角色槽位可能已经清空。任务和模型统计以历史 dispatch 为主，不以当前槽位是否仍有 agent ID 为准。

当前冻结结果包括 132 个任务，其中 128 个为 `DONE`；源清单包括 2,253 份文件指纹。128 个完成任务的主要 provenance 如下：

| 维度 | 结果 |
| --- | --- |
| 编排者模型族 | GPT/Codex 50，Claude 39，Grok 39 |
| 候选修改者归因 | GPT/Codex 113，Gemini 11，Claude 1，Muse 1，mixed 1，未解 1 |
| reviewer 关系 | 同族 only 96，跨族 only 25，同族与跨族并存 4，同族与未知 reviewer 并存 1，未解 2 |
| 重复执行 | 48 个任务有多次 executor dispatch；42 个任务有多次 contextual reviewer dispatch |
| 交付 commit | 43 个 STATE 明示 commit，43 个都可在源仓库解析 |

分阶段看，P1 的 8 个完成任务没有 GPT reviewer；P2 的 120 个完成任务中，113 个包含 GPT reviewer，107 个只出现 GPT reviewer。这里的“候选修改者”是 Paseo read-and-fix 流程中的实际修改者或一审执行者，不等于原始译文生成者。

所有明细与模型、mode、thinking 档位统计以 `SNAPSHOT.json` 为准，不应从本页的文字摘要反向补写数据。

## 脱敏边界

Agent metadata 采用严格字段白名单，只读取并输出：

- `id`；
- `provider`；
- `config.model`；
- `config.thinkingOptionId`；
- `config.modeId`；
- `createdAt`。

原始 agent JSON 不复制到仓库。`persistence`、session、native handle、MCP server 配置、认证 header、标题和 prompt 均被排除。Agent metadata 的 SHA-256 只用于证明重建时读取的是同一源文件，不泄露其正文。

Task/review 文件同样不复制正文。快照只保留枚举、计数、ID、candidate identity 哈希、逻辑输入路径和源文件指纹；finding、observation、validation、host note 和自由文本 result 均不保存。

## 重建

在能访问生产工作树和原始 Paseo metadata 的机器上运行：

```bash
cd evidence/quality/model-probes/paseo-provenance-snapshot-v1
node generate.mjs \
  --repo /path/to/tome4-chinese-translation \
  --agents /path/to/paseo/agents \
  --out .
node verify.mjs \
  --repo /path/to/tome4-chinese-translation \
  --agents /path/to/paseo/agents
```

生成器不写入源仓库或 Paseo metadata。它不写生成时间，因此在源文件、源仓库 HEAD 和生成器版本不变时应产生逐字节相同的 JSON。两份输出都记录生成器自身的 SHA-256；`SOURCE-MANIFEST.json` 的 `combined_sha256` 绑定全部源指纹，`SNAPSHOT.json` 再引用该 digest。

## 已知局限

- Paseo 任务多为对既有译文执行 read-and-fix；现有记录不能可靠识别更早的原始译文生成者。因此本快照不能直接完成 reviewer × original translation origin 分析。
- 40 个完成任务有显式 `candidate_author_agent_id`；79 个仅能按“所有 executor dispatch 属于同一模型族”推断；7 个 P1 任务按“完成且无 executor、由 orchestrator 直接修复”归因；其余 2 个未解。推断不能提升为显式事实。
- 一个历史 reviewer agent ID 已无本机 metadata，因此保留为 `Unknown`。
- 一个历史 review JSON 以无效 JSON 保存；快照记录其路径和哈希，不修补原始记录。该任务另有后续有效 review artifact。
- 只有 43/128 个完成 STATE 直接记录交付 commit。其余任务可能能由 Git 历史推断，但本版不做基于 commit message 的概率链接。
- 文件 SHA 可以证明“是否与本次冻结源相同”，不能让缺少原始忽略目录的第三方恢复其正文。本快照的可重建含义是：持有原始本机证据的人可以复算并验证；Git 本身保存的是脱敏派生证据，而不是敏感原始控制面档案。
- Dispatch 次数受重试、修复循环和归档策略影响，不能当作独立样本数。任务级统计应作为判断模型覆盖面的主口径。

## 研究解释

快照纠正了“此前译文审核基本全部由 GPT 完成”这一过强概括：P1 正式 reviewer 实际全部为非 GPT；但 P2 明显由 GPT reviewer 主导，且大量候选修改者也属于 GPT/Codex。因此风险不是全历史单一模型，而是 P2 中候选修改与正式审核的同族相关性，以及原始译文来源缺失。该事实支持开展受控变异和前瞻性未审样本实验，但本身不能证明 GPT 已经产生系统性偏差。
