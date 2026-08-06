# ToME4 汉化项目交接清单

更新时间：2026-08-06（质量 Evaluator v2 重校准已执行；两模型稳定性均未通过，M4d No-Go）

本文记录当前翻译工具、术语库和发布流程的状态，供后续继续开发、审校或发布使用。

## 一、当前目标

- 以本仓库为唯一规范译文源。
- 建立可复现的术语库和翻译工具链。
- 发布插件只包含相对源码/官方 locale 的必要覆盖译文；源码已有且未改变的译文不重复打包。
- 对公开源码和闭源 DLC 使用不同的输入边界，避免工具绕过受保护提取流程。

## 二、已完成事项

### 翻译与术语

- 已建立 `terminology.tsv` 和 `TERMINOLOGY.md` 的术语库工作流。
- 当前术语表共 693 条：`existing` 439 条、`preferred` 254 条、`review` 0 条（相比交接基线 653 条净增 40 条，含 16 条高频术语与 light 共享键裁决后的补录）。
- 相比更早的 510 条术语基线净增 183 条，并修订 7 条既有术语；新增内容主要覆盖核心技能、实体、状态、专名和 DLC 术语。
- DLC 首轮候选已通过受审计提取器处理 `ashes-urhrok`、`cults`、`orcs`，未直接读取受保护源码。
- 3 条待审校术语已全部裁决（2026-08）：`Constrict`→缠绕、`eldritch`→骇异、`Atmos Tribe`→气之部族，均升为 `preferred` 并按术语库流程先改 TSV 再同步规范 Lua。
- 已保留翻译条目的 `source_tag`，并为术语补充 `T.*` 分类及语境说明。
- 核心与 DLC 规范 Lua 已完成一轮大批量术语统一和译文校正，并已连同回归测试提交冻结（commit `89744ab`），后续 finding 修订在冻结基线上分批提交，不能视为已发布版本。

### 工具链

- `doctor`、`extract`、`lint`、`status`、`merge`、`workset`、`context`、`proposal`、`review`、`build` 已统一到 `python3 -B tools/i18n` 入口。
- 审核流程：`tools/i18n review --scope code|translations` 显式生成只读 Pi 审核 bundle，`tools/pi-review --bundle` 严格校验 findings、分配宿主 `R-NNN` 并优先复用精确缓存，`tools/pi-remediate --bundle --review` 产生修订建议；修订需由主代理校验后应用，MVP 不自动执行模型建议。
- 源码核验变体（Skill `$tome4-pi-file-review`，2026-08-04 新增）：`tools/pi-review-files --bundle`（headless）与 `tools/pi-tmux review-files --bundle`（tmux 分屏可见）与隔离审核共用 bundle、findings 契约、严格校验、报告格式与授权门槛，但 Pi 以 `--tools read,bash` 白名单启动，可按提示契约只读核验仓库、公开游戏源码（`/Users/yun/projects/t-engine4`）与公开 DLC 源码（`/Users/yun/projects/tome4-dlcs/`）来验证证据；`edit`/`write` 永不启用、cwd=仓库根、缓存命名空间与隔离审核分离；系统提示为 `i18n/prompts/pi-reviewer-files.md`，可读范围与禁止范围（`.artifacts/`、凭据、网络、一切写入）写死在提示中。Pi 内置 `bash` 不是 OS 沙箱，会继承 Pi 进程权限与 provider 凭据；工具现自动比较运行前后的版本控制范围的内容级 worktree 快照（受管 diff、非忽略未跟踪文件内容与 Git exclude；不覆盖其他忽略路径或其余 `.git` 元数据），主代理仍须独立确认工作树未被改动。需要强隔离时必须在只读挂载、网络/凭据隔离的容器或 VM 中运行。
- 构建工具现在支持最小 addon 覆盖层：官方已有且语义未改变的译文只计入继承统计，不写入插件。
- 显式指定组件时，例如：

  ```bash
  python3 -B tools/i18n build --profile addon --component tome --require-complete
  ```

  只检查所选组件，不会把未选择的 DLC、旧 lore 或 Nullpack 层算作不完整。
- addon 构建报告现在包含 `inherited_entries`、`override_entries`、`new_entries`，并对重复运行键进行去重。
- 所有工具报告和候选文件仍只写入被忽略的 `.artifacts/i18n/`。

### 本次发布边界决策

- 核心发布层固定为 `tome`，状态为 `releaseable`，继续使用 `build --profile addon --component tome --require-complete`；DLC 和外部覆盖层不再作为核心构建的隐式依赖。
- `ashes-urhrok`、`cults`、`orcs` 已登记受保护提取快照的哈希基线；`items-vault`、`possessors` 暂时忽略，保留规范译文但不再探测来源，也不计入 addon 候选或 DLC 发布层完整性。
- DLC addon 层当前仍为 `baseline-pending`：已有受保护快照哈希不能替代发布所需的可验证官方/源码基线。
- `legacy-lore-overlay` 与 `nullpackreloaded` 各自拆为独立可选外部层。当前不把 addon 仓库提交当作它们的官方源码基线，也不把它们计入核心发布完整性。
- 以上边界已写入 `i18n/versions/tome-1.7.6.json` 的 `release_layers`；后续严格构建需要按层选择并验证，不应通过忽略缺失来源来伪造全量通过。

### 翻译质量系统（第一阶段 M0–M3 + M4 dry-run，2026-08-04）

- 设计文档：`docs/translation-quality-system.md`（整体方案）与 `docs/translation-quality-phase-1.md`（阶段计划）。
- 权威规则已版本化：`i18n/quality/taxonomy-v1.json`（37 个 MQM 风格错误码、8 类 profile、severity、门禁、risk flag、profile 分类规则）、`i18n/quality/policy-v1.json`（身份契约、120 条试点参数与 6 项覆盖约束）、四份 JSON schema。
- `tools/i18n quality {inventory,sample,validate,report}` 已接入统一入口；实现位于 `tools/i18nlib/quality.py`。
- 全量 current revision inventory：**30,177 个 revision**（与 LocaleLoader 条目数守恒），含结构签名、profile、相关术语、确定性 gate signal 与 risk flag；相同输入重复运行 SHA-256 一致（`048359c2…`）。
- 120 条试点样本（代表性 60 / 风险富集 40 / 对照 20±1）满足全部覆盖约束，固定 seed `tome4-quality-pilot-v1` 可逐字节复现；对照桶覆盖近重复原文、尾空格多译、跨语境同源等真实争议案例。
- strict validate 已能拒绝：未知错误码/等级、绝对路径、重复 finding ID、不完整覆盖、sample 不匹配、悬空裁决、confirmed blocker/major 晋级 Gold 等；report 输出一致率、加权 κ、错误分布与校准目标对照。
- 当前 evaluator 开发批次门禁全过：lint --strict 0/0、433 项单元测试、运行时键扫描 0 冲突、1,717 条重复键均为合法跨文件重复、`git diff --check` 通过。
- 2026-08-04 首轮 Pi 代码审核（provider opencode-go / model deepseek-v4-flash，bundle `3a6898f1…`）：8 条 finding 全部独立核验属实并已修复——术语匹配最长优先+前缀归并（R-001）、可合并错误码对称匹配（R-002）、profile 分歧改从 assessment 推导（R-003）、新增 format_shape_match 信号（R-004）、新增 cross_component_variant 事实（R-005）、对照桶组原子性（R-006）、relevant_terms 携带 domain（R-007）、handoff 测试数对齐（R-008）。修复后全量 inventory 重建：domain_hints 3,120 条、跨组件变体 0、格式形状差异 0；120 条样本可逐字节复现。
- 2026-08-04 第二轮 Pi 代码审核（provider deepseek / model deepseek-v4-flash，bundle `3176637b…`，tmux pane 实时流式 293s）：3 条 finding 全部核验属实并已处置——对照组兜底超员有界并补注释说明（R-001）、handoff 内部数字矛盾已对齐（R-002，测试数 87、minor/note 完成态、pending=0）、quality validate 默认执行 policy 的 strict_unknown_fields（R-003）。
- 2026-08-04 第三轮 Pi 代码审核（provider deepseek / model deepseek-v4-flash，bundle `2e1d3535…`，pane 渲染升级后 302s）：5 条 finding 全部核验属实并已处置——section 模式改段感知匹配（R-001，`ui` 不再误伤 `data/guilds`）、category 指标双侧计入合并匹配（R-002）、inventory 空 target 回读放行（R-003）、strict 未知字段覆盖根级/evaluator（R-004）、handoff 测试数统一为 89（R-005）。
- 2026-08-04 质量 M4 dry-run 里程碑：12 条 dry-run 样本完成 reviewer-a/reviewer-b 两份完整 assessment 与裁决（`quality validate --dry-run --strict` 通过，severity 加权 κ=0.92、实质缺陷一致率 91.7%、风险标志覆盖率 1.0），`quality report` 管线在 dry-run 集全链路验证；冻结清单 `.artifacts/i18n/quality/runs/*-dry-run/dry-run-frozen-manifest.json`（含 4 条 rubric 观察：物品未识别名/天赋名 profile 应归 term-name、zones 长叙事应归 narrative、术语表缺组合实体词、contrast finding 身份记账）；`quality validate` 新增 `--dry-run` 模式（adjudication 可选）。dry-run 两份评估由同一代理会话产生，按 M4 约定不计入正式一致性与缺陷率，正式 120 条需两位真正独立的 evaluator。
- 2026-08-04 AI quality evaluator 盲测：新增 `tools/pi-quality-evaluator`、`tools/i18nlib/pi_quality.py` 与隔离 prompt，模型保持无工具/无会话/无项目上下文，宿主固定 evaluator 元数据并严格校验完整覆盖；DeepSeek V4 Flash 与 GPT-5.6 Luna 均用 max thinking 完成 12 条多轮独立盲评。首轮缺陷一致率 50%、κ=0.1875；统一逐项检查表后的最佳轮达到缺陷一致率 83.33%、major-or-worse 91.67%、κ=0.5833；severity 锚点复测受随机差异影响回落至 58.33%/0.34，说明当前 pair 的 severity 稳定性未达到 κ≥0.70，正式 120 条暂缓。一次 DeepSeek 输出完整 items 但遗漏最外层 `}`，runner 仅允许该唯一确定性 envelope 修复并有回归测试，其他畸形输出仍拒绝。
- AI evaluator v2 落地方案已写入 `docs/translation-quality-evaluator-v2.md`：模型改为输出问题证据与三态影响事实，宿主规范化/匹配问题并按版本化规则派生 severity，分歧走匿名事实裁决；现有 12 条降为探索回归集，后续使用与正式 120 条互斥的 32 条校准集和 32 条封存验证集，避免在固定小样本上调参过拟合。
- 2026-08-06 Evaluator v2 离线里程碑已完成（`dfbe516`、`ca887d4`、`7b3ac2b`、`cbd83ad`，最终复审修订见后续提交）：新增严格 v2 policy/rubric/schema、版本化 impact rules 与空 anchors；独立 `quality_v2` 实现 Unicode span、assessment 身份、规则定级、同 revision 二部图匹配、匿名 dispute/身份映射、事实裁决重算、数据集/分片/报告；`tools/pi-quality-evaluator` 已兼容 v2 shard，并仅用 fake runner 验证。真实 30,177 条 inventory 一次加载生成校准 `28c1a2e4…` / 封存 `4931d451…` 各 32 条，与探索 12 和正式 120 两两互斥；重复生成字节一致（9.81s/9.88s），正式 sample ID/内容保持不变；封存 profile 按正式分布精确缩放为 8/6/5/4/3/3/3，组件组为 19/9/4，四个长度桶均有覆盖；两套数据各生成 2 个不超过 20 条且不拆 contrast group 的 shard。最终 artifact 为 `.artifacts/i18n/quality/runs/20260806T000836.350031Z-calibration-v2/`，未调用外部 provider、未修改规范译文。v1 `quality.py` 在 `d92ffc8` 与当前内容 blob 相同，三次正式 sample 基准中位 3.596s，因此本批不存在 v1 核心采样回退。
- 2026-08-06 经逐项授权执行新 lineage 校准 `e29bf49…`：DeepSeek V4 Flash 主跑/强制复跑分别产生 2/10 个 finding，稳定性 Jaccard `0.200`；GPT-5.6 Luna 主跑/强制复跑分别产生 3/5 个 finding，稳定性 Jaccard `0.600`。两者 schema coverage、结构失败、关键事实一致率和派生 severity 一致率均通过，但均未达到预注册 finding Jaccard `>=0.70`，因此 M4d 为 **No-Go**，不得冻结该 evaluator 配置或进入封存验证。两模型主跑交叉匹配为 3 个 issue（1 full、1 partial、1 Luna-only），Jaccard `0.667`；其中 1 条“英文感叹号未保留”进入匿名人工队列。稳定性、匹配、争议与报告分别保存在 `.artifacts/i18n/quality/runs/20260806T050532.754110Z-stability-v2/`、`20260806T054146.351003Z-stability-v2/`、`20260806T054200.719628Z-issue-match-v2/`、`20260806T054210.581923Z-disputes-v2/` 和 `20260806T054210.584959Z-report-v2/`；封存集和正式 120 条均未发送或查看 evaluator 结果。
- 2026-08-04 最终工作区代码 diff 有界 Pi 复审（provider deepseek / model deepseek-v4-flash，bundle `0bb8d57f…`）：5 条 finding 已独立核验。R-002（runner 未自动核验 worktree）与 R-003（code bundle/tmux 测试缺口）确认并修复：headless/tmux 初步增加前后 `git status --porcelain` 快照，新增 code bundle 与 tmux 回归测试；R-005（术语净增基线表述）确认并改为明确的 510 条早期基线；R-004（测试数应为 94）不采纳，实际 HEAD 为 92、复审时工作区为 97，模型把更早的 89 条叙述误当直接基线，首次修订后实测为 99。R-001（`bash` 无 OS 沙箱且继承凭据）部分确认：Pi 官方文档明确内置工具不是沙箱，已在 AGENTS/Skill/handoff/系统提示中纠正“硬性只读”表述、记录强隔离要求；provider 通信凭据无法在同一 Pi 进程内彻底与内置 bash 隔离，当前只允许经逐次授权、受监控运行，强安全场景必须使用只读挂载及网络/凭据隔离的容器或 VM。
- 2026-08-04 修订后二轮 Pi 复审（同 provider/model，bundle `0ea1ff0c…`）：3 条 finding 全部确认并修复。R-002 指出脏工作树下 porcelain 状态不随已修改/未跟踪文件内容变化，现改为哈希 HEAD、受管 binary diff、非忽略未跟踪文件内容与 Git exclude 的版本控制范围内容级快照，并新增脏 tracked/untracked 文件回归测试；R-001 指出 headless 篡改路径在落盘 raw output 前失败，现调整为先保存 stdout/stderr 与哈希再检查快照；R-003 指出系统提示中的禁止范围只是受监控契约，现明确其非 OS 技术边界及强隔离要求。测试总数升至 100。
- 2026-08-04 三轮修订复审（同 provider/model，bundle `bb20a5ff…`）：3 条 finding 已独立核验。R-001 部分确认：忽略路径与绝大多数 `.git` 元数据不属于版本控制工作树且 `.artifacts` 会被宿主正常写入，无法纳入同一无噪音快照；已把报告字段与 AGENTS/Skill/handoff 表述收窄为 `versioned_worktree_*` 和“受管 + 非忽略未跟踪 + info/exclude”的最佳努力范围，强隔离要求不变。R-002 确认并新增 fake Pi 实际篡改 tracked 文件的集成测试，断言运行失败、`versioned_worktree_unchanged=false` 且 raw output/report 已落盘。R-003 不采纳：`cli.py` 明确将 `run_validation` 导入别名为 `quality_run_validation`，`dry_run` 已在该函数签名中接收并透传；为消除回归疑虑仍新增 runner 级 dry-run 测试。测试总数升至 102。
- 2026-08-04 收敛复审（同 provider/model，bundle `2f14a759…`）：2 条 finding 均已处置。R-001 确认：headless 与 tmux worker 现均以独立进程组启动 Pi，并在成功、失败或超时时清理整个进程组后再取 worktree 快照；报告显式记录 `process_group_cleanup=true` 与无法覆盖自行脱离进程组的 `detached_descendants_checked=false`，强隔离场景仍按容器/VM 要求执行。R-002 作为防误用建议采纳：dry-run 使用官方 `SAMPLE_CONTRACT` 时继续允许管线试跑，但 validation/report 现产生明确的 non-official 警告，不能作为已裁决正式 pilot 门禁证据；既有测试增加警告断言。
- 2026-08-04 最终收敛复审（同 provider/model，bundle `cad8ed9c…`）：3 条 finding 已核验。R-001 与 R-002 确认：headless 不再用 `communicate()` 全量缓冲事件流，改为 daemon pump 流式落盘并过滤累积 `message_update`；headless/tmux 的 stream reader 均使用有界 join，无法在进程组清理后收敛时报告失败而非无限挂起。R-003（正常退出后清理同组残留存在极低概率 PGID 复用）不采纳：正常退出后杀同组残留是防止后台写绕过快照的必要步骤，调用紧随已记录 PID 的退出且复用窗口可忽略；自行 `setsid` 的后代仍按已记录残余边界处理。
- pane 可见性改造：pi 审核/修订/翻译命令从 `--mode text`（完全缓冲）切换为 `--mode json`（实时事件流），新增事件流提取（`extract_event_stream_output`）与 pane 增量预览（`_preview_event_line`），reasoning/文本增量实时可见；deepseek provider 凭据经 `_pi_environment` 注入 `DEEPSEEK_API_KEY`（此前因 `PI_CODING_AGENT_DIR` 重定向找不到 auth.json）。
- pane 渲染二次升级（`PaneStreamRenderer`）：增量按换行组装成完整行、推理暗色/状态行青色，与常规终端一致；`message_update` 行不再写入 raw 文件（每行携带累积 partial，曾致单次运行 5.9GB，现 ~756KB）。

## 三、最近验证结果

以下结果是当前工作区最近一次验证的基线：

- `doctor`：清单、Lua 5.1 / LuaJIT 2.1、LPeg 0.10.2 和受保护输入代理均正常。
- 单元测试：440 项通过（`test_toolchain.py` + `test_quality_v2.py`）；覆盖契约/身份/path、span、每条 severity 规则的 yes/no/unknown、确定性技术门禁、匹配图、匿名裁决、分片完整性、全缓存身份、fake runner 成功/失败 artifact、报告和稳定性预注册校验。
- 严格 lint：30,177 条翻译、693 条术语，0 个错误、0 个警告；`lint --strict` 已可作为当前门槛。
- lint 仍统计到 1,717 个重复运行键；这不是当前构建失败项，但仍需分类审校。
- 核心最小 addon：严格构建成功，19,023 个预期运行键全部验证通过。
- 核心补丁包含 1,391 个运行键：17,632 个官方已有译文继承不打包，1,382 个覆盖译文，9 个新增译文。
- 构建验证结果为 `missing=0`、`mismatched=0`、`unexpected=0`、`redundant=0`。
- 默认全量 addon 仍不能作为完整发布层；DLC 基线及可选外部层必须分别解决，不能借核心构建的成功宣称全量完成。

环境检查另有两个非阻断提示：公开引擎仓库因包含受保护输入而跳过通用 worktree 扫描；外部发布仓库 `tome-chn-mod` 当前存在工作区改动，正式安装或发布前必须先确认其归属。

### 审核闭环状态

- 主仓库已完成首轮全量 Pi 翻译审核：覆盖 609 个原始 translation bundle、30,170 条规范译文；累计报告记录 3,223 条 finding observation。
- 以稳定 `review_id` 去重并对缓存重放采用较晚裁决后，权威库存为 614 个 validated review observation、3,218 条 finding：2,816 条确认、146 条部分确认、247 条不采纳、9 条待语境裁决。
- review 工作树原队列中有 1,365 条与该权威库存精确关联；另有历史/代码审核观察，使原台账已处置总数为 1,425 条。
- 本次从尚未关联的 1,853 条中排除主仓库已裁决不采纳的 165 条，新增 1,688 条 `pending`：2 blocker、565 major、1,053 minor、68 note；其中 1,609 条确认、79 条部分确认。
- 同步清单为 `.artifacts/i18n/imports/pi-first-round-20260803/manifest.json`，完整差集为同目录的 `first-round-remaining-findings.json`；同时复制了 362 份 validated `review.json` 与 362 份绑定的有界 translation bundle，未复制 `raw-output.txt` 或含绝对源路径的 Pi 运行元数据。
- `remediation-queue.json` 现有 3,113 条：1,425 条为冻结前已处置、1,688 条为本次新增 pending；`remediation-ledger.json` 保留既有逐条处置记录并关联本次 import。首轮“发现”阶段已经完成，修订阶段正在推进（见下）。

### 审核闭环处置进度（2026-08-03 晚）

- 冻结批次：已处置的 1,425 条对应工作树改动已复跑严格 lint（0/0）、39 项测试和 `git diff --check` 后提交为 `89744ab`（8 个文件，+2,945/−2,673），与新增队列隔离。
- blocker：2 条全部处置（`303f788`）：R-002 删除 ShowPurchasable 中文末尾残留英文句并恢复“包括你自己”；R-007 补全 world-artifacts 的【待翻译】句并本地化 Veluca 为“维卢卡”。
- major：565 条全部处置（`d8d25db` 至 `c1c2771` 共 15 个批次，每批 40 条独立提交），覆盖 engine/boot/addon-dev/ashes-urhrok/cults/orcs/possessors/items-vault/tome 各组件；其中约 10 条经核验在冻结提交中已修复，按 `already_resolved` 记账，未重复改动。
- minor：803 条全部处置完毕（`020741b` 至 `9844f5a` 共 18 个批次：batch 6–21 每批 50 条 + batch 22 收尾 3 条），全部集中在 tome 组件；每批独立提交，个别条目经核验在先前批次已修复，按 `already_resolved` 记账，未重复改动。跨条目术语（如 Pyre Wars＝烈火战争、Wayist＝维网信徒、Infinite Dungeon＝无尽地下城、Pride＝部落）先更新 `terminology.tsv` 再统一同步。
- note：68 条全部处置完毕（`efebeaf` 50 条跨 6 组件 + `8494b5c` 18 条 tome），队列 `pending` 已清零。
- 队列终态：`remediation-queue.json` `pending=0`，`applied_pending_commit=2945`，`already_resolved=135`；`remediation-ledger.json` 已关联 2,795 条 finding 处置记录。
- 处置原则：每条 finding 以有界 bundle 的 source/target 为准独立核验（涉及公开机制时另核验固定源码），不直接照抄 Pi 建议；每批修改后运行 `lint --strict`（0 错误 0 警告）与 `git diff --check`，并在 `remediation-queue.json`/`remediation-ledger.json` 中逐条记账（`verification`、`verification_note`、`changes`）。
- 批次切分注意：生成批次时须从**当前 pending 列表**固定取 `[0:40]`/`[0:50]`，不得使用随列表缩短而漂移的 `[40n:40n+40]` 索引；此前曾因此系统性跳过条目，已通过剩余 pending 复核修正。
- 当前 pending 余量曾为 871 条（minor 803 + note 68）；后续批次全部处置完毕后 `pending` 已清零（见队列终态）。

## 四、待办事项

### P0：发布基线

- [x] 将核心 `tome`、DLC 和外部覆盖层拆为独立发布边界，并让核心层通过严格构建。
- [x] 整理并提交当前术语、译文和回归测试批次；最终 diff 已完成有界独立复审，源码核验变体与 M4 dry-run 收敛批次提交为 `aa382da`。
- [x] 为当前 DLC 发布层中的 `ashes-urhrok`、`cults`、`orcs` 建立可验证的官方/源码基线（2026-08-04 extract 验证：快照 SHA-256 与 tDef 数与 manifest 一致）；`items-vault`、`possessors` 仅在重新纳入发布范围时恢复来源映射并补建基线。
- [x] 为 `legacy-lore-overlay` 固定来源、版本和归属组件（2026-08-04 调查：tome-chn-mod 与引擎公开源码均无独立 legacy-lore 实体，结论记录于 manifest external_requirements 与 i18n/README）。
- [x] 为 `nullpackreloaded` 固定源码来源和版本，或拆成独立可选插件（译文快照固定于 tome-chn-mod `8dd657d`：null_translation.lua 464 条目 + hooks/load.lua；上游 addon 版本未固定，保持 optional 层）。
- [x] 在发布仓库工作区干净且归属明确后，生成并独立验证核心发布 artifact（核心 addon 确定性重建 SHA-256 一致 `aa712264…`；产物经 LuaJIT 加载验证 4,158 条目；`tools/ci-gates.sh` 一键门禁 10 步全过）。

### P1：翻译质量

- [x] 清理控制标记、`@token` 大小写/缺失和格式差异等 lint 问题；当前严格 lint 为 0/0。
- [x] 同步首轮全面审核余量，建立 1,688 条待处理 finding 的本地快照、队列和台账关联。
- [x] 冻结已处置的 1,425 条工作树并形成可审核提交（`89744ab`），与新增队列隔离。
- [x] 处理 2 条 blocker（`303f788`）；每项均以有界 bundle、术语库及必要的固定公开源码独立核验，不能直接套用 Pi 建议。
- [x] 处理 565 条 major（`d8d25db`–`c1c2771` 共 15 批，每批 40 条独立提交并逐条记账）。
- [ ] 分组件处理 1,053 条 minor 和 68 条 note；高复用术语先更新 `terminology.tsv`，再同步规范 Lua。（已完成：minor 1,053/1,053、note 68/68，见推荐工作顺序 §4）
- [x] 审定 `Constrict`→缠绕、`eldritch`→骇异、`Atmos Tribe`→气之部族（2026-08 裁决，先改 TSV 再同步 Lua）。
- [x] 检查 1,717 个重复运行键（2026-08-03 `930b9c2` 分类完成：全部为跨文件合法重复，0 个同文件冗余；分类结果见 `tools/classify_runtime_keys.py` 报告）。
- [x] 对每个 remediation 批次运行严格 lint 和定向测试、更新台账；全部完成后对最终 diff 做有界 Pi 复审，并为接受、修订或撤销的 finding 留下闭环证据（2026-08-04，`0bb8d57f…` 至 `cad8ed9c…` 五轮收敛复审，处置记录见本节）。
- [ ] 翻译质量系统 M4d–M6：首轮 32 条校准双评、匿名裁决与公开源码核验已完成并保留为历史；确认 `omission`/`unit` 同证据重复匹配缺口后，已在 `ecc79c8`–`cd87c36` 增加受限合并规则、6 个仅来自人工裁决校准案例的严格 provenance anchors、稳定性预注册/CLI、配置单次加载和陈旧 sample/policy 拒绝。新校准 ID 为 `e29bf49…`、封存 ID 为 `08e7df73…`，与旧版条目集合相同但 policy/sample identity 已更新，旧 assessment 不得复用。已获授权的两模型各两次新校准运行均完成，但 DeepSeek/Luna finding Jaccard 分别仅为 `0.200`/`0.600`，低于预注册 `0.70`，M4d 已按失败语义停止；下一步应先修订 evaluator 方法并建立新的冻结 lineage，再重新预注册和另行申请外部授权，不得补跑当前 lineage、查看封存结果或运行正式 120 条。

### P2：流程与工程化

- [ ] 为默认构建、核心最小构建和基线缺失场景补充 CLI 集成测试。
- [ ] 建立持续集成检查：LuaJIT 加载、普通 lint、单元测试、核心 build，以及禁止受保护目录越界读取。
- [ ] 评估是否需要安全的人工审核后 apply 流程；当前 `merge`/`proposal` 只生成候选和校验结果，不会原地修改规范 Lua。
- [x] 新增的 `i18n/`、`tools/`、`tests/` 文件已纳入本次工具链提交；发布仍需单独执行。
- [x] 为受保护提取器陈旧输出、空编辑键、越界 merge report 与 AI evaluator v1/v2 隔离/严格输出补充回归测试；当前测试总数为 440。

## 五、推荐工作顺序

1. ✅ 已冻结已处置 1,425 条 finding 的工作树：复跑严格 lint、39 项测试和 `git diff --check` 后形成提交 `89744ab`，避免与新增队列混写。
2. ✅ 已处理 2 条 blocker（`303f788`），完成事实核验、译文修订、关联台账和定向验证。
3. ✅ 已将 565 条 major 按 `component + section + ordinal` 切成有界批次（15 批，每批 40 条）全部处理完毕，优先覆盖机制反转、参数/占位符、伤害类型、触发条件和长篇错配；每批独立提交并逐条记账。
4. ✅ 已处理 1,053 条 minor 与 68 条 note（1,053/1,053、68/68），队列 `pending` 清零；跨条目术语先走术语库流程，重复运行键在同批同步，但不得无证据全局替换。
4b. ✅ 与基线（相邻仓库 HEAD `84e5573`，即本分支基线）逐条对比后，发现早期批次约 14 条标记 `applied` 但条目未落盘的遗漏，已全部补修（`5d26960`，tome 8 / ashes 3 / cults 2 / engine 1 及标点统一 1 处），并全量复检确认除有意保留项外无遗漏。
5. 每批结束后更新 `remediation-queue.json`、`remediation-ledger.json` 和人类可读台账，运行严格 lint 与相关定向测试；涉及公开机制时记录固定 commit，涉及 DLC 时只使用已复制的有界规范 bundle。
6. 队列清零后运行完整 doctor、lint、当前全套测试（433 项）和核心严格 build，再对最终 diff 生成有界 Pi 复审（需要对照源码核验证据时可用 `$tome4-pi-file-review` 变体）；只有复审无未处置 finding，才更新为审核闭环完成。
7. 随后分类 1,717 个重复运行键（已判定全部为跨文件合法重复）并继续 DLC、legacy lore、Nullpack、CI 与发布基线工作；3 条 `review` 术语已裁决（见 P1）。

## 六、常用命令

```bash
python3 -B tools/i18n doctor
python3 -m unittest -q tests/i18n/test_toolchain.py tests/i18n/test_quality_v2.py
python3 -B tools/i18n lint --json
python3 -B tools/i18n lint --strict
python3 -B tools/i18n status --json
python3 -B tools/i18n build --profile addon --component tome --require-complete --json
python3 -B tools/i18n build --profile addon --require-complete --json
python3 -B tools/pi-review-files --bundle <bundle.json>
python3 -B tools/pi-tmux review-files --bundle <bundle.json>
python3 -B tools/i18n quality validate --dry-run --sample <dry-run.json> --assessment <reviewer-a.json> --assessment <reviewer-b.json> --strict
python3 -B tools/i18n quality calibration --inventory <inventory.jsonl> --calibration-size 32 --holdout-size 32
python3 -B tools/i18n quality evaluator-bundles --sample <calibration.json> --evaluator reviewer-a --max-items 20
```

执行 Lua 相关检查时必须遵守 `AGENTS.md` 中的 LuaJIT 5.1 和模块路径要求。任何 DLC 提取、快照或上下文操作都必须通过仓库内受审计的工具完成；不得使用通用文件搜索、脚本 API 或 Git 命令直接读取受保护 DLC 输入。

## 七、当前分支与工作区范围

- 当前分支：`codex/review-findings-20260802`。
- 本次最终交接提交完成后，分支相对 `origin/master` 领先 157 个提交：在既有工具链/术语/审核闭环基础上，新增 Evaluator v2 设计提交 `c73c4c6`、四个分阶段离线实现提交 `dfbe516`、`ca887d4`、`7b3ac2b`、`cbd83ad`，以及最终有界复审修订/交接提交。
- 本轮 finding 处置涉及文件：`engine.lua`、`mod-tome.lua`、`tome-ashes-urhrok.lua`、`tome-cults.lua`、`tome-orcs.lua`、`tome-addon-dev.lua`、`tome-possessors.lua`、`tome-items-vault.lua`、`mod-boot.lua`、`mod-example.lua`、`mod-example_realtime.lua`。
- 当前工作区在本段更新提交后应保持干净；v1 evaluator 批次为 `af88a5b`，v2 重校准实现与冻结提交为 `ecc79c8`–`cdaa2dc`。v2 外部校准已按明确边界执行并因稳定性失败停止；封存集、正式 120 条、推送和发布均尚未执行。
- 工作树状态快照：`remediation-queue.json` 的 `pending` 为 0（全部处置），`applied_pending_commit` 2,945、`already_resolved` 135；`remediation-ledger.json` 已关联 2,795 条处置记录。
- 已处置但未改动规范文件的条目（有意保留）共 168 条：`already_resolved` 135（已含修复/与源码一致/术语裁决/代码基线已修复）+ `false_positive` 33（不采纳，原因均记录在台账 `verification_note`）。
- 术语表系统工程（2026-08）：新增 `domain` 列（11 领域 + lint 白名单）、静态/动态审计、补录基础术语（资源/面板属性/免疫/高频词）、3 条 review 术语裁决、33+26 条同键多译统一、light 共享键裁决、重复运行键分类（1,717 全部跨文件合法重复）、`tools/scan_runtime_collisions.py` / `classify_runtime_keys.py` / `review_diff.py` / `pi-review-batch.py`。
- 三轮 Pi 复审闭环（2026-08-03/04）：diff bundle 复审 3 轮，major 66→54→21→0，全部处置（含裁决保留）；处置记录在 `.artifacts/i18n/terminology-audit/findings_review{1,2,3}*.json`；worker 调优测试见 `docs/pi-review-worker-tuning.md`（最优 6 workers，4.2× 加速）。

上述状态说明核心插件已通过本地发布门槛，首轮全量 finding 队列已清零，术语与重复运行键分类均已完成。质量 v2 离线核心和互斥 32+32 数据准备已完成；新校准外部运行已结束，但两个 evaluator 均未通过预注册稳定性门槛。下一动作是分析并修订 evaluator 方法、建立新的冻结 lineage 和预注册，而不是补跑当前校准、进入封存集或正式 120 条。DLC 与外部层仍不属于已完成发布范围。
