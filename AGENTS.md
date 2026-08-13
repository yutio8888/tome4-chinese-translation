# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 角色与协作

- **主代理**负责范围、裁决、验证和最终交付，通常也是仓库写入者。
- **审核子进程／项目 subagent**只返回 proposal、context 或 findings；其结果由主代理核验后再应用。
- **Paseo 编排**启用时，主代理任 ORCHESTRATOR；EXECUTOR 是任务内容文件的唯一写入 agent，REVIEWER 只做独立复审。

无论采用哪种协作方式，模型输出都不是最终事实：机制以固定版本源码为准，修改以后文门禁和验收标准为准。

Paseo 从任务明确采用该编排并建立 task ID 时视为激活，直到任务进入 `DONE`／`STOP`，
或 ORCHESTRATOR 明确记录回退。激活期间不得使用 `$tome4-pi-review`、
`$tome4-pi-file-review` 或 `$tome4-pi-subagent`；委托、实现和独立复审只通过 Paseo 的
ORCHESTRATOR／EXECUTOR／REVIEWER 角色完成。现有 blind translation runner、门禁和普通
检查仍可由 ORCHESTRATOR 作为工具直接调用，不视为启用旧 Skill。

## Paseo 轻量编排（大型任务）

Paseo CLI v0.3.1 用于需要多步实现和独立复审的大型任务；小型修改由主代理直接完成。用户明确要求 Paseo 时必须使用；否则 CLI 不可用时可以回退主代理执行并说明。角色 prompt 见 `.ai/roles/`，轻量设计说明见 `docs/paseo-orchestration-v2-contract.md`。

### 最小规则

1. 同一 workspace 同时只能有一个任务内容写入者；EXECUTOR 运行时，ORCHESTRATOR 仍可更新当前 task 的编排记录和验证产物。
2. EXECUTOR 只改任务允许的文件，不 commit、不 stage；REVIEWER 与其使用同一 workspace，但不得修改任何文件。
3. ORCHESTRATOR 独立核验测试和 finding，只把已接受的 finding 交给 EXECUTOR 修复。
4. 自动修复最多两轮；仍有重要问题或需要产品判断时询问用户。
5. Paseo 激活期间所有 agent 委托只使用 EXECUTOR／REVIEWER，不再调度旧 Skill 的 reviewer、scout 或 plan-reviewer。
6. 翻译 semantic observation v2 由 ORCHESTRATOR 直接运行现有 blind runner；Paseo REVIEWER 只审查代码、工具、文档和 legacy v1。混合任务可以共用任务记录，但两类审核必须分别运行。
7. EXECUTOR／REVIEWER 必须由 Paseo 托管的 ORCHESTRATOR 直接通过 `paseo run` 创建并继承
   `PASEO_AGENT_ID`；不得用 provider 原生 `spawn_agent` 代替。创建后必须用 `paseo inspect`
   确认 `ParentAgentId` 等于 ORCHESTRATOR agent ID，否则停止该 agent 并按基础设施错误处理。
8. EXECUTOR 使用 DeepSeek V4 Flash 时必须显式传入 `--thinking max`，并在 STATE 记录
   `thinking: "max"`。创建或恢复后必须确认 `Thinking` 为 `max`；不支持或设置失败时
   不得静默降级到 `high`／默认值，应停止并按基础设施错误处理。

### 工作流与记录

实现任务采用：`PLAN → IMPLEMENT → VALIDATE → REVIEW → ADJUDICATE →（FIX → VALIDATE → RE_REVIEW，最多两轮）→ FINAL_REVIEW → ADJUDICATE → FINAL_VALIDATE → DONE`。修复后的验证通过进入 RE_REVIEW；验证或复审发现问题时，有剩余轮次则进入 FIX，否则进入 WAIT_USER。仅审核任务采用：`PLAN → REVIEW → ADJUDICATE → DONE`。需要用户决定时记为 `WAIT_USER`；取消或无法继续时记为 `STOP`。

启用 Paseo 时只需维护以下已忽略文件：

- `.ai/task/<task_id>/SPEC.md`：范围、允许修改文件、验收标准；
- `.ai/task/<task_id>/PLAN.md`：大型任务的简短步骤，可在事实变化时直接更新；
- `.ai/task/<task_id>/BASELINE.patch`／`baseline/`：仅在任务需要修改既有脏文件时保存其起始 patch 或副本；
- `.ai/task/<task_id>/STATE.json`：当前状态、轮次、审核阶段与 contract 进度、ORCHESTRATOR／子 agent ID、provider/model、WAIT_USER 恢复点和 review 记录引用；
- `.ai/reviews/<task_id>/review-NN.json`：任务身份、审核阶段、review contract、结构化 finding 与主代理裁决。

每个新任务使用独立 task ID；旧的 flat `.ai/task/STATE.json`／`.ai/reviews/review-NN.json` 保持原样。STATE 在阶段转换后更新即可，不要求逐动作审计链、内容 hash、WAL 或不可变 artifact。进入 WAIT_USER 时记录原因和 `resume_state`。基础设施错误可重试一次；若 `paseo run` 是否成功不明确，先按 task/role label 查询现有 agent，不能唯一确认时再询问用户，不得盲目创建第二个写入 agent。

任务前脏文件默认不交给 EXECUTOR；确需修改时，SPEC 必须逐文件允许，并先保存可恢复的起始 patch 或副本。每轮验证用该基线生成任务自身的 baseline→current diff，确认用户原有内容未被意外覆盖，并把该 diff 交给相应 reviewer。`review_only` 的 DONE 只要求全部审核已完成、findings 已裁决且无 deferred；`implement` 的 DONE 还要求没有未解决 accepted finding，并通过最终验收。

REVIEWER 使用 `--mode auto-review --workspace <workspace-id>` 加入 ORCHESTRATOR 当前
workspace，并接收主代理提供的有界 diff／上下文。Codex `auto-review` 实际为
`workspace-write`，因此只读边界由 role briefing 约束，ORCHESTRATOR 必须在 REVIEWER
运行前后核对工作树；若 REVIEWER 造成任何改动，按基础设施错误处理。审核结束后
只归档 agent，不得归档正在使用的当前 workspace。大型输入按组件拆成新的 task ID，
不设固定字节或文件数配额。

EXECUTOR 与 REVIEWER 均不继承当前会话，briefing 必须包含范围、验收标准和必要上下文。provider/model 在任务开始时用 `paseo provider ls` 与 `paseo provider models --thinking <provider>` 确认，记录实际选择；DeepSeek V4 Flash 的 EXECUTOR thinking 固定为 `max`。

### 外发边界

以下项目级通道无需逐次确认：通过现有 blind runner 发送 translation v2 bundle；向 Codex REVIEWER 发送与 code/legacy v1 审核相关的代码、文档和必要上下文；向 pi EXECUTOR 发送任务 briefing 并允许其读取当前 workspace。任务记录只需注明 provider、model 和内容范围，不要求保存完整 payload manifest。使用其他 provider 或发送范围外内容前仍须取得用户授权。

## 汉化工具入口

- 自动化统一使用 `python3 -B tools/i18n <command>`；首次运行先执行 `doctor`，译文修改后执行 `lint`。工具自动配置 LuaJIT 模块路径。
- 报告和候选文件写入已忽略的 `.artifacts/i18n/`；除显式安装／发布命令外，不改写游戏源码或发布仓库。
- 翻译使用 `tools/pi-subagent --workset <workset.json>`（可见运行用 `tools/pi-tmux translate`）。子进程只输出 proposal，主代理通过 `proposal --strict` 校验后应用。
- 翻译审核先用 `tools/i18n review` 生成 bundle，再运行 `tools/pi-tmux review --bundle <bundle.json>`（headless 用 `tools/pi-review`）。semantic observation v2 的 blind 输入、输出和宿主裁决遵循 `docs/pi-review-v2-contract.md`；不得注入 terminology、Facts 或历史 finding。
- `$tome4-pi-file-review`／`tools/pi-review-files` 只处理 code/legacy v1。translation v2 在 claim-bound runner 实现前由主代理按固定源码版本核验。源码感知进程只有 `read,bash` 工具；其结果仍由主代理确认。
- 质量抽样使用 `tools/pi-quality-evaluator`；已确认 finding 的修复建议使用 `tools/pi-remediate`。两者只产出 assessment/proposal，不直接改规范 Lua 或代码。
- Paseo 未激活时，用户要求审核使用 `$tome4-pi-review`；源码侦察或计划审查使用 `$tome4-pi-subagent` 的 scout／plan-reviewer。Paseo 激活后不使用这三个项目 Skill，由 ORCHESTRATOR 按角色 briefing 直接路由任务和工具。
- 外发按上文「外发边界」执行；常设通道只需报告 provider、model 和大致内容范围。

## DLC 源码输入（GPL v3 公开）

- ToME4 与三个官方 DLC 为 GPL v3（or later）公开源码，可以直接读取、分析和提取。正式版位于 `/Users/yun/projects/tome4-dlcs/`（ashes/cults/orcs，1.7.4）；版本依据以 manifest 固定值为准。
- 分发译文／addon 时保留版权声明、使用 GPL v3 兼容许可并提供对应源码。
- 翻译审核只发送规范条目的 blind v2 bundle；代码审核发送去除本机绝对路径的公开 diff。scout／plan-reviewer 可以读取上述公开源码，输出由主代理核验后应用。

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
- **译文批量修改后**在提交前运行门禁 1–5；涉及 Pi 复审时按 `docs/runtime-key-collisions.md` 与 `docs/pi-review-worker-tuning.md` 的流程执行。`--workers 6`、8 起限速劣化仅是旧 v1 的历史数据，不能外推到 translation v2；v2 尚未重新校准，并发默认值与显式选择以当前 CLI 为准。
- 修改外部仓库或已有版本控制文件（尤其 CRLF 行尾、JSON、Lua 字面量）前，先阅读 `docs/lessons-learned.md` 的常见陷阱；改完用 `git diff --stat` 确认无行尾/缩进噪音。
- 审计与扫描脚本均在 `tools/` 下版本控制，输出只写入 `.artifacts/i18n/`（忽略目录），不直接改写规范 Lua。

## 校对判定依据

- 当翻译、术语、审核意见或英文表面含义对游戏机制的描述存在分歧时，以当前版本清单固定的游戏源代码实际行为为最终判定依据；现有译文、术语库和模型 finding 都不能覆盖源码事实。
- 核验机制时应记录对应组件、公开源码路径、固定 commit 和关键调用或数据定义，并据此确认、部分确认、撤销或修订审核结论；当前工作树与固定 commit 不一致时，默认以版本清单固定的 commit 为准，除非用户明确指定其他目标版本。
- 公开游戏与三个官方 DLC 源码可以直接核验；未公开组件只使用用户授权的证据。证据不足时标为待确认。

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology/`。
- 主代理阅读术语库不等于把术语或 Facts 注入 blind semantic discovery；术语/专名疑点只能在 observation 产生后按 claim 核验与裁决。
- 新增或修改高复用术语时，先更新 `terminology/`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
