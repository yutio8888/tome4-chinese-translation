# Grok 4.7 复核推进交接

## 用户授权与任务

用户要求复核本轮生产审核启动以来全部已修改译文，已确认范围；当前两批及交叉核验完成后，把后续推进与记录交给 Grok 4.7。你接替 ORCHESTRATOR，仅整理、派发、核对覆盖/证据/生命周期、更新进度；不能自行裁决译文、修复或改术语。继续推进剩余批次，不逐批询问。用户明确不要强制 Gemini 输出 JSON；接受中文自然语言，结构化记录由宿主整理。所有疑点交 Paseo/Codex/GPT-5.6-Sol/Medium 只读交叉核验，归因保留，不把模型 severity 当事实。

## 工作区和范围

沿用本独立 worktree `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`，workspace `wks_ac28b30c4bf45d5b`，branch `audit/modified-translations-20260921`。不得写主工作区 `/workspace/tome4-chinese-translation`，不得 push/merge/改生产 queue/catalog/handoff。只写当前审核 campaign 的 evidence、编排记录和必要临时派生文件。

根目录下 `evidence/translation-audit/all-modified-review-20260922/` 简称 E：
- PLAN.md：完整规则、角色、范围、顺序与验收。
- inventory.json：4144 条完整冻结清单，11 组件，157 次 first-parent 相关提交（含 merge）。基线 `d77becdaf5f9860cae396741a4f1f319bb4ef5d5` 来自首批 `batch-c7f8a5c77bbeaa7f3b89` manifest；译文终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。4143 净变更+1 改后恢复，删除0。
- STATE.json、PROGRESS.md：实时批次/交叉结果/生命周期，优先于 inventory 内初始状态字段。
- batches/batch-001.md 至 batch-130.md：预先冻结的候选包，最多40条及约28KB原文+译文。禁止读他批审核意见污染 Gemini。
- source-access.json：固定 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 用 git show 查，允许沿相关调用链读；DLC 的只读冻结缓存位于本树 .artifacts/i18n/all-modified-review-20260922/sources，逐文件hash已记，来源仍 unpinned。addon-dev/items-vault/possessors 公共源码尚未定位，不能套用 engine pin；证据不足交 Sol 标 pending。
- reports/：原始自然语言结果；HUMAN-REVIEW.md：转录的人工待决点。
- INVENTORY-CORRECTIONS.md：先前4123漏计merge其他组件，已更正4144；旧11条抽查中Night Terror由于未区分source_tag误纳，只有10条属本范围，现清单已用section/source/source_tag/occurrence正确区分。

## 接手点

已有 Gemini 覆盖10条；batch001/002新增80条，共90/4144。后续从 batch-003 开始，共128批4054条。当前全部结果/归档以交接时 STATE 为准。原始第一批2条疑点、第二批3条疑点+2条细微观察均已交Sol。不要重新跑已覆盖条目，不沿用旧宿主语义裁决。

## 后续运行

每次派发读 live list_profiles notes，Gemini 指定 antigravity/gemini-3.8-flash high（当前profile mode dangerously-skip-permissions, auto_accept=true，但prompt严格只读）；Sol 指定 codex/gpt-5.6-sol medium mode auto-review。模型/档位必须查 live metadata确认。通常最多2 Gemini+1 Sol并行，模型不可用不擅自换用户指定模型。启动后用notifyOnFinish等待通知，不轮询。

每个包完整逐条覆盖，报告可用列表/表格。只报有证据疑点，允许同section语境/固定公开源码。主代理仅核对覆盖，不裁决语言。疑点及细微观察形成只读Sol包，授权其读原始观察+冻结候选+必要源码；Sol逐claim confirmed/refuted/pending/advisory附证据。之后原样记录并汇总人工清单；无自动修复。

终态先收获原文、核对冻结input/hash、locale hash和HEAD未变，再archive（每次调用前持久化archive_attempts_started，最多2），用live archivedAt确认，才派后继。失败fresh child不续跑已结束agent；第二批首次TLS握手超时已按此处理。活动review期间不提交以保持HEAD守卫；可在批次屏障全部归档时提交本任务记录，不push。`get_agent_activity` 可能包含宿主文件变动的[Edit]通知，不应单凭该标签断言reviewer写入；检查实际hash。原始报告取完整文本，通知截断时用activity更大limit；不重写原始输出。

## lineage与交接

此campaign既有 `orchestrator_agent_id=ebbf6ea8-83ee-4fdf-85dc-bb82fbd25fe8` 及已归档dispatch身份是历史事实，不可改写成你的ID。为你的新编排session创建新task ID，例如 `all-modified-review-20260922-grok01`，在新STATE写当前非空PASEO_AGENT_ID，新child均由你通过agent-scoped Paseo创建并核验父级。共享campaign的progress/queue可由你作为唯一当前记录者更新，用新session关联新dispatch，保留旧记录。用户明确handoff是角色授权例外，不是让你当REVIEWER或让旧主代理继续并发写。

用户自然语言输出、Sol看疑点以及主代理只记录的当前指令优先于仓库旧JSON/盲审/宿主语义裁决规则。不能伪造旧严格contract checker的DONE_VERIFIED；记录实际用户授权与机械验收。完成条件：全部4144有Gemini覆盖、每个疑点有Sol交叉结果、未决人工项清楚、所有审核child归档、证据已落盘。不要求pending清零，不修复译文。

## 已完成的交接屏障

当前两批和全部3次 Sol 交叉复核已完成；本 session 的6个 child dispatch（含1次启动失败）均已确认归档。已核对全部 locale 冻结哈希、候选输入哈希和原始报告哈希；仅提交审核证据，不运行不适用于只读报告的译文构建门禁。剩余4054条从003批接续。HUMAN-REVIEW.md 已汇总6个含 confirmed 意见的条目及2个仅 advisory 条目，语义结论作者均是 Sol，等待人工决定，禁止据此自动修复。

本交接由 paseo-handoff skill 执行。Grok 4.7 没有匹配现有 profile，已通过 live provider/model metadata 确认可用，按用户指定使用 grok/grok-4.7、medium、auto_accept=true。你启动后成为唯一后续记录者；旧宿主停止写入。
