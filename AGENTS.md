# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 角色与协作

- **主代理**负责范围、裁决、验证和最终交付，通常也是仓库写入者。
- **审核子进程／项目 subagent**只返回 proposal、context 或 findings；其结果由主代理核验后再应用。
- **Paseo 编排**启用时，主代理任 ORCHESTRATOR；EXECUTOR 是任务内容文件的唯一写入 agent，REVIEWER 做常规独立复审，SENIOR_REVIEWER 做超过两轮后的范围校准和高影响流程交叉复审，SCOUT 做只读源码侦察（返回压缩代码上下文，不产生审核 contract 结果）。

无论采用哪种协作方式，模型输出都不是最终事实：机制以固定版本源码为准，修改以后文门禁和验收标准为准。

Paseo 从任务明确采用该编排并建立 task ID 时视为激活，直到任务进入 `DONE`／`STOP`，
或 ORCHESTRATOR 明确记录回退。旧项目 Skill（`$tome4-pi-review`、
`$tome4-pi-file-review`、`$tome4-pi-subagent`）已归档（见 `archive/`），不再参与任何审核
路由；委托、实现、源码侦察和独立复审只通过 Paseo 的
ORCHESTRATOR／EXECUTOR／REVIEWER／SENIOR_REVIEWER／SCOUT 角色完成。门禁和普通
检查仍可由 ORCHESTRATOR 作为工具直接调用，不视为启用已归档 Skill。

## Paseo 轻量编排（大型任务）

当前已核验的 Paseo 0.4.0（CLI 或等价注入的 agent-scoped Paseo MCP 操作）用于需要多步实现和独立复审的大型任务；小型修改由主代理直接完成。任务级 orchestration_transport 在 STATE 中只允许 cli|mcp，两种传输必须保持相同的 role、purpose、workspace、lineage、歧义恢复和 reviewer 只读语义。用户明确要求 Paseo 时必须使用；否则 Paseo 不可用时可以回退主代理执行并说明。角色 prompt 见 .ai/roles/，轻量设计说明见 docs/paseo-orchestration-v2-contract.md。

### 最小规则

1. 同一 workspace 同时只能有一个任务内容写入 agent；EXECUTOR 运行时，ORCHESTRATOR 仍可更新当前 task 的编排记录和验证产物。
2. EXECUTOR 只改任务允许的文件，不 commit、不 stage；REVIEWER、SENIOR_REVIEWER 和 SCOUT 与其使用同一 workspace，但不得修改任何文件。
3. ORCHESTRATOR 独立核验测试和 finding，只把已接受的 finding 交给 EXECUTOR 修复；reviewer 的 severity、verdict 和范围建议都不自动生效。
4. 自动修复最多五轮。第二轮后若普通 review finding 仍要求进入下一轮 FIX，必须先由 SENIOR_REVIEWER 审查意见是否偏离设计意图、功能边界或个人项目规模；每个后续轮次都重新校准当轮意见。
5. 所有 agent 委托只使用 EXECUTOR、REVIEWER、SENIOR_REVIEWER、SCOUT；旧项目 Skill 已归档，不再调度，其输出不得计入任何 Paseo contract。SCOUT 只做只读源码侦察，不承担审核 contract、不产生 finding。
6. 译文审核由 Paseo REVIEWER 按 purpose=translation_contextual_v1 承担：有界、只读、独立记录与指标；SENIOR_REVIEWER 不承担该 purpose。语境候选冻结后先计算 candidate_identity，把外层 envelope 以紧凑 JSON 字节冻结到任务作用域 workspace 相对输入文件；initialPrompt 只携带任务、输入和输出三行的短派发 prompt。
7. EXECUTOR、REVIEWER、SENIOR_REVIEWER、SCOUT 必须是当前 ORCHESTRATOR 的 Paseo-managed child，并出现在其 Subagents track；创建只能走当前 Paseo 的 CLI 或 agent-scoped MCP `create_agent` 操作，不得使用其他 agent 创建接口。创建载荷必须带有任务／角色 `labels`。主代理必须有非空 `PASEO_AGENT_ID`，并在 STATE 保存不可变的 `orchestrator_agent_id`；创建或恢复后必须核验 workspace、role、purpose、parent lineage（`ParentAgentId` 或等价字段）和角色权限，无法验证 lineage 时停止并进入 WAIT_USER。
8. 角色是唯一的运行时路由约束。EXECUTOR 只承担 executor role；REVIEWER 按 purpose 区分 normal_review 与 translation_contextual_v1；SENIOR_REVIEWER 只承担 cross_review 或 scope_audit；SCOUT 只返回上下文。具体执行载体、版本、档位和回退选择不写入 STATE，不参与 candidate identity，也不作为契约验收条件。
9. 修改翻译流程或项目基础设施时，普通 REVIEWER 和 SENIOR_REVIEWER 必须从同一 SPEC、同一任务自身 diff 独立交叉审核，在两份输出都返回前不得互看结论。该 code-only 交叉审核不把译文本身交给普通 reviewer；译文语义审核走 translation_contextual_v1。
10. 每个 code review phase 冻结 SPEC 和一份独立路径的有界任务自身 diff，保持候选一致性。必要的 SPEC 修改一律视为新候选；candidate_ref 是 SPEC 与该 diff 的精确字节摘要。每次派发、返回和完成前都要重枚举当前实际变更路径集，路径集或配方改变即产生新候选。
11. 只有实际 diff 重构了可能阻塞测试进程的扫描或解析循环，才在更广测试前要求进度不变量说明和短超时、有限输入的微型探针。挂起、持续增大输出或 OOM 时先终止并确认子进程退出，不得无界重跑。
12. 任务前脏文件默认不交给 EXECUTOR；确需修改时，SPEC 必须逐文件允许，并先保存可恢复的起始 patch 或副本。review_only 的 DONE 只要求全部审核完成、findings 已裁决且无 deferred；implement 的 DONE 还要求无未解决 accepted finding 并通过最终验收。

### 工作流与记录

实现任务采用：PLAN → IMPLEMENT → VALIDATE → REVIEW → ADJUDICATE →（FIX → VALIDATE → RE_REVIEW，最多五轮）→ FINAL_REVIEW → ADJUDICATE → FINAL_VALIDATE → DONE。仅审核任务采用：PLAN → REVIEW → ADJUDICATE → DONE。需要用户决定时记为 WAIT_USER；取消或无法继续时记为 STOP。

启用 Paseo 时只需维护以下已忽略文件：

- .ai/task/<task_id>/SPEC.md：范围、允许修改文件、验收标准；
- .ai/task/<task_id>/PLAN.md：大型任务的简短步骤；
- .ai/task/<task_id>/BASELINE.patch 或 baseline/：仅在任务需要修改既有脏文件时；
- .ai/task/<task_id>/CODE_DIFF-<phase>-<cycle>-<attempt>.patch：仅 code review phase；
- .ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json：仅选择 translation_contextual_v1 时；
- .ai/task/<task_id>/STATE.json：当前状态、轮次、审核阶段、角色 ID、transport 和恢复点；
- .ai/reviews/<task_id>/review-NN.json：任务身份、审核阶段、review contract、reviewer role、purpose、candidate_ref、finding 与裁决。

每个新任务使用独立 task ID；旧的 flat STATE 和 review 记录保持原样。STATE 在阶段转换、contract 完成、agent ID 变化或出现错误时更新即可。不要求逐动作审计链、全工作树 hash 或 immutable artifact。基础设施错误可重试一次；若创建是否成功不明确，先按 `labels.task_id`、`labels.role` 和需要的 `labels.purpose` 查询，过滤先于基数判定：无匹配可重试一次，唯一匹配且身份正确才可复用，多个匹配或无法确认时进入 WAIT_USER。

语境 REVIEWER 恢复只允许复用同一候选、同一 dispatch_id、同一 role/purpose 和同一创建尝试的唯一 agent。每次新的派发、重跑或无效输出重试都创建 fresh agent；不得用旧会话部分输出拼接新结果。其他角色需要更换 child 时，也必须保持同 role、同 purpose、同 workspace 和同 lineage，旧未验收输出作废。

### 外发边界

外发权限按角色、purpose 和输入边界授权：

- EXECUTOR：任务 briefing、SPEC 允许的 workspace 内容；
- 普通 REVIEWER：有界代码、工具、文档 diff、SPEC 和必要上下文；
- SENIOR_REVIEWER：同一 SPEC、diff 及 scope audit 所需的当轮 finding；
- SCOUT：组件范围、公开源码根和机制问题；
- translation_contextual_v1 REVIEWER：冻结的有界译文语境 bundle，以及其中明确引用的译文和公开源码。

bundle 不得包含先前 finding、裁决或建议修复。改变外发内容范围、目的或读取边界仍须用户授权；执行载体选择不构成额外的授权轴。质量 evaluator 的运行身份、预注册、campaign ledger 和历史 assessment 由独立质量契约管理，不因本编排契约改变。

## 汉化工具入口

- 自动化统一使用 `python3 -B tools/i18n <command>`；首次运行先执行 `doctor`，译文修改后执行 `lint`。工具自动配置 LuaJIT 模块路径。
- 报告和候选文件写入已忽略的 `.artifacts/i18n/`；除显式安装／发布命令外，不改写游戏源码或发布仓库。
- 翻译使用 `tools/pi-subagent --workset <workset.json>`（可见运行用 `tools/pi-tmux translate`）。子进程只输出 proposal，主代理通过 `proposal --strict` 校验后应用。
- 译文审核由 Paseo REVIEWER 的 `translation_contextual_v1` 承担（契约见 `docs/paseo-translation-context-review-v1-contract.md`）。
- code/legacy v1 审核由 Paseo 常规 REVIEWER 承担；译文审核的机制核验由主代理按固定源码版本核验。
- 质量抽样使用 `tools/pi-quality-evaluator`；`tools/pi-remediate` 是 dormant 兼容入口：只消费既有 assessment/finding artifact 生成修复 proposal，不参与任何活跃审核 dispatch，也不替代 Paseo REVIEWER 路由。两者只产出 assessment/proposal，不直接改规范 Lua 或代码。
- 审核、源码侦察与计划审查统一走 Paseo 角色路由（REVIEWER／SENIOR_REVIEWER／EXECUTOR／SCOUT）；旧项目 Skill 已归档（见 `archive/`），不再作为回退路径。
- 外发按上文「外发边界」执行；常设通道只需报告 role、purpose 和大致内容范围。

## DLC 源码输入（GPL v3 公开）

- ToME4 与三个官方 DLC 为 GPL v3（or later）公开源码，可以直接读取、分析和提取。正式版位于 `/Users/yun/projects/tome4-dlcs/`（ashes/cults/orcs，1.7.4）；版本依据以 manifest 固定值为准。
- 分发译文／addon 时保留版权声明、使用 GPL v3 兼容许可并提供对应源码。
- 译文审核发送有界译文语境 bundle（`translation_contextual_v1`）；代码审核发送去除本机绝对路径的公开 diff。Paseo 的 REVIEWER／EXECUTOR／SCOUT 及主代理可以读取上述公开源码，输出由主代理核验后应用。

## Lua 运行环境

- Tome4 及本仓库的旧汉化工具按 Lua 5.1 语义运行。
- 一律使用 `luajit`，不要使用 Homebrew 安装的 `lua`、`lua5.4` 或 `lua5.5`。
- LuaRocks 模块安装在 `/Users/yun/.local/share/tome4-luarocks`，其中应包含 `lfs`、`lpeg` 和 `rex_pcre`。
- 旧版 `luafish` 只能使用已验证的 LPeg 0.10.2；LPeg 0.12.2 和 1.1 会令所有文件出现 `empty loop in rule 'functioncall'`。
- 不要要求用户在每次执行脚本前手动 `export` 环境变量。

## 执行 Lua 脚本

代理每次执行 Lua 脚本、单行 Lua 命令或依赖检查时，都必须在同一条命令中自动设置模块搜索路径：

```bash
env \
  LUA_PATH='/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?.lua;/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?/init.lua;;' \
  LUA_CPATH='/Users/yun/.local/share/tome4-luarocks/lib/lua/5.1/?.so;;' \
  luajit <脚本及参数>
```

例如：

```bash
env \
  LUA_PATH='/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?.lua;/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?/init.lua;;' \
  LUA_CPATH='/Users/yun/.local/share/tome4-luarocks/lib/lua/5.1/?.so;;' \
  luajit i18n_tools/extract.lua /Users/yun/projects/t-engine4
```

不能把环境设置和 `luajit` 拆成不同的终端调用，因为代理的每次终端调用都可能是新的 shell。

## 执行前检查

首次使用或运行失败时，先用以下方式检查运行时和模块；检查命令也必须使用上述项目环境：

```bash
command -v luajit

env \
  LUA_PATH='/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?.lua;/Users/yun/.local/share/tome4-luarocks/share/lua/5.1/?/init.lua;;' \
  LUA_CPATH='/Users/yun/.local/share/tome4-luarocks/lib/lua/5.1/?.so;;' \
  luajit -e 'require("lfs"); require("lpeg"); require("rex_pcre"); print(_VERSION, jit.version)'
```

预期版本语义为 `Lua 5.1`。如果 `luajit` 或依赖不存在，应明确报告缺失项或执行已获授权的安装步骤；不得退回使用新版 `lua`。

## 文本提取器兼容设置

运行历史版本的 `i18n_tools/i18n_extractor.lua` 时，应在提取器的临时副本中，于 `luafish/parser.lua` 的 `local lpeg = require 'lpeg'` 后加入：

```lua
lpeg.setmaxstack(100000)
```

不要为此修改游戏源码工作区。未提高栈上限时，大型 Lua 文件会出现 `too many pending calls/choices`，而提取器仍可能以退出码 0 结束并写出不完整结果。

一次提取只有同时满足以下条件才算成功：

- `i18n_extractor.lua` 退出码为 0。
- `i18n_list.lua` 存在且包含非零数量的 `tDef(...)`。
- 提取日志中没有以 `In file ` 开头的解析失败记录。

## 安装 LuaRocks 依赖

需要安装或重装依赖时，必须明确指定 Lua 5.1、LuaJIT 目录和项目专用模块目录：

```bash
luarocks \
  --lua-version=5.1 \
  --lua-dir="$(brew --prefix luajit)" \
  --tree="/Users/yun/.local/share/tome4-luarocks" \
  install luafilesystem

luarocks \
  --lua-version=5.1 \
  --lua-dir="$(brew --prefix luajit)" \
  --tree="/Users/yun/.local/share/tome4-luarocks" \
  install --force lpeg 0.10.2-1

luarocks \
  --lua-version=5.1 \
  --lua-dir="$(brew --prefix luajit)" \
  --tree="/Users/yun/.local/share/tome4-luarocks" \
  install lrexlib-pcre \
  PCRE_DIR="$(brew --prefix pcre)"
```

安装系统软件或 LuaRocks 模块前，仍须遵循当前任务的权限和确认要求。

## 项目通用审核与修复工作流

审核开始时明确模式（仅审核／审核并修复）、范围、关注维度和完成标准。先记录
`git status --short` 与实际 changed/untracked 文件；保留任务前改动，首次运行工具先执行
`python3 -B tools/i18n doctor`。

### 审核

- 先完成一轮只读检查再集中裁决；仅审核任务不得自行进入修复。
- 译文检查源码机制、语境、术语、占位符／markup、运行键和中文表达；代码／工具检查输入、
  失败语义、下游消费者和实际复杂度；文档／配置核对真实实现与命令。
- finding 必须有源码或上下文证据，并说明可触发行为或调用链。纯风格偏好、理论风险和
  无证据的性能猜测不算确认问题。
- 主代理把 finding 标为 confirmed、pending 或 advisory，并独立定级；只有 confirmed
  finding 自动进入修复。模型自报等级不作为事实。

### 修复

- 只有用户要求修复时才修改；先冻结当前 finding 清单，再按依赖顺序处理 accepted 项。
- 给无上下文修复 agent 的指令应包含 finding、允许文件、最小测试和完成条件；subagent
  输出与自报测试结果都由主代理复核。
- 不为相邻风格、无关重构或额外质量工程扩大范围。

### 验证与停止

1. 每个修复运行最接近的 lint／测试并检查 `git diff --check`。
2. 一批修复完成后运行组件级检查。
3. 收束后统一运行适用的完整门禁、构建和 smoke；工作树未变化时不重复长门禁。

仅审核任务在 findings 核验完成后交付。审核并修复任务在 accepted findings 全部解决、
门禁通过，并完成一轮新的独立复审后交付；只剩 pending/advisory 时说明并停止，不追求
无界的“零风险”。外发遵循上文集中边界。

## 门禁检查（每次译文批量修改后必跑）

以下检查按顺序执行，任何一项失败都必须先修复再继续，不得用管道吞掉退出码：

```bash
# 1) 规范译文静态校验（必须检查退出码，勿用 `| tail` 吞掉）
python3 -B tools/i18n lint --strict; echo "exit=$?"

# 2) 单元测试
python3 -m unittest -q tests/i18n/test_toolchain.py; echo "exit=$?"

# 3) 跨组件同键多译扫描（应为 0 条；非零需先处理再继续）
python3 -B tools/scan_runtime_collisions.py; echo "exit=$?"

# 4) 重复运行键分类（全部应同 target；新增异 target 说明运行时覆盖风险）
python3 -B tools/classify_runtime_keys.py; echo "exit=$?"

# 5) 工作树整洁度
git diff --check && echo DIFF_OK
```

- **术语表改动后**额外运行：`python3 -B tools/audit_static.py`（静态审计：错字/标点/同源冲突）、`python3 -B tools/audit_dynamic.py`（动态审计：术语 vs 译文使用率/多译）、`python3 -B tools/annotate_domains.py`（领域标注一致性）。报告写入 `.artifacts/i18n/terminology-audit/`。
- **译文批量修改后**在提交前运行门禁 1–5；涉及译文审核时按 `docs/runtime-key-collisions.md` 的流程执行。`--workers 6`、8 起限速劣化仅是已归档 v1 的历史数据，不适用于 Paseo 译文审核通道。
- 修改外部仓库或已有版本控制文件（尤其 CRLF 行尾、JSON、Lua 字面量）前，先阅读 `docs/lessons-learned.md` 的常见陷阱；改完用 `git diff --stat` 确认无行尾/缩进噪音。
- 审计与扫描脚本均在 `tools/` 下版本控制，输出只写入 `.artifacts/i18n/`（忽略目录），不直接改写规范 Lua。

## 校对判定依据

- 当翻译、术语、审核意见或英文表面含义对游戏机制的描述存在分歧时，以当前版本清单固定的游戏源代码实际行为为最终判定依据；现有译文、术语库和模型 finding 都不能覆盖源码事实。
- 核验机制时应记录对应组件、公开源码路径、固定 commit 和关键调用或数据定义，并据此确认、部分确认、撤销或修订审核结论；当前工作树与固定 commit 不一致时，默认以版本清单固定的 commit 为准，除非用户明确指定其他目标版本。
- 公开游戏与三个官方 DLC 源码可以直接核验；未公开组件只使用用户授权的证据。证据不足时标为待确认。

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology/`。
- 术语/专名疑点只能在审核 observation 产生后按 claim 核验与裁决；不得用术语库覆盖源码事实。
- 新增或修改高复用术语时，先更新 `terminology/`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
