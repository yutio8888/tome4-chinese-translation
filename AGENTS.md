# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 汉化工具入口

- 当前版本的自动化入口统一为 `python3 -B tools/i18n <command>`；`tools/i18n` 可执行位可用时也可直接调用。
- 首次运行先执行 `tools/i18n doctor`，译文修改后执行 `tools/i18n lint`。
- 工具会在启动 LuaJIT 子进程时自动设置本文件规定的 `LUA_PATH` 和 `LUA_CPATH`，不得要求用户手动导出。
- `extract`、`lint`、`status`、`merge`、`workset`、`context`、`proposal`、`review` 和 `build` 的报告或候选文件只写入已忽略的 `.artifacts/i18n/`；没有显式安装命令时不得改写游戏源码仓库或发布模组仓库。
- Pi 翻译入口为 `tools/pi-subagent --workset <workset.json>`（需要实时观察时可用 `tools/pi-tmux translate --workset <workset.json>`，在 tmux 分屏中执行）。该进程必须保持无工具、无会话、无项目上下文，只能输出 proposal artifact；其结果必须通过 `proposal --strict`，不得直接写规范 Lua。
- Pi 审核入口为 `tools/i18n review` 生成 bundle，再用 `tools/pi-tmux review --bundle <bundle.json>` 执行（默认在当前 tmux 会话分屏运行，便于观察审核过程；无 tmux 环境用 `--fallback foreground`，脚本场景可直接用 `tools/pi-review`）。翻译使用独立的 semantic observation v2：blind provider payload 不注入 terminology/Facts 或 canonical membership 等宿主 lineage，只包含最小 revision/source/target 输入；按 10 条硬上限与 item canonical JSON 字符预算双重分包，`selection_sha256` 绑定跨 shard 的完整有序 revision 集，index 分别记录宿主 `artifact_bytes` 与实际外发 `payload_bytes`。v2 的精确 JSON user message 必须经 stdin 发送，不得用会注入绝对路径 wrapper 的 `@file`；必须用显式空 `--append-system-prompt` 关闭 project/global `APPEND_SYSTEM.md` 自动发现，Pi cwd 固定为 `/private/tmp`，实际 user/system prompt、runner、policy 与 normalizer 都必须进入 evaluator/cache identity。模型逐 item 返回 `assessment_state`、可观察语义差异和精确 source/target evidence，不得填写 severity、确认状态或 suggested fix；宿主只做结构、span、identity 与 pending 路由，主代理独立裁决。代码 diff 保留 legacy v1 finding 契约。Pi 始终无工具、无会话、无项目上下文，不得直接修改文件。
- 源码核验变体（Skill `$tome4-pi-file-review`）的现有 `tools/pi-tmux review-files --bundle <bundle.json>`（headless 用 `tools/pi-review-files`）只接受 code/legacy v1。translation v2 的源码核验必须绑定既有 observation identity，只能返回 `supported/refuted/insufficient` 并禁止新增 finding；在该 claim-bound runner 实现前，现有工具必须失败关闭，由主代理按固定源码版本直接核验。legacy file reviewer 以 `--tools read,bash` 白名单启动，所读源码片段和路径可能进入 provider 请求；首次授权必须同时披露可读公开根与这一外发边界。`edit`/`write` 永不启用，但 Pi 的内置 `bash` 不提供 OS 沙箱，仍继承 Pi 进程权限与 provider 凭据；工具会自动比较运行前后的版本控制范围内容级快照，主代理运行后仍须独立确认工作树未被改动。需要强隔离时必须使用只读挂载、网络/凭据隔离的容器或 VM。
- Pi 完整质量评价入口为 `tools/pi-quality-evaluator --sample <sample.json> --evaluator <reviewer-id>`。该进程保持无工具、无会话、无项目上下文，只接收有界 quality sample，宿主补齐并严格校验 assessment 身份；不得向任一 evaluator 展示另一份 assessment、裁决、历史 finding 或预期等级。模型评价仍受首次外部传输授权门槛约束，不能替代后续人工裁决。
- Pi 处理审核意见入口为 `tools/pi-tmux remediate --bundle <bundle.json> --review <review.json>`（headless 可用 `tools/pi-remediate`）。只有主代理已独立确认并定级的 finding 才可进入 remediation；translation v2 pending observation 不得直接进入，当前 runner 会显式拒绝。该进程只能输出绑定到 finding/item 的 remediation proposal；主代理必须独立校验并应用修订，再重新运行审核，不得让 Pi 直接写规范 Lua 或代码。
- 当用户要求开展 Pi 审核时（无论主代理是 Codex 还是 Pi），使用项目 Skill `$tome4-pi-review`；交互式审核默认在 tmux 分屏中运行，pane 保留至 `tmux kill-pane -t <pane>`。首次向外部 provider 发送 bundle 前，必须明确报告 provider、model、bundle 类型、条目数量、字符预算与实际 payload 大小并取得用户授权；不得用项目级全局网络放行绕过该授权。

## DLC 源码输入（GPL v3 公开）

- ToME4 及三个官方 DLC（Ashes of Urh'Rok、Cults of Entropy、Embers of Rage）以 **GPL v3（or later）** 发布，源码可自由读取、分析、提取。许可证依据：`t-engine4/COPYING`（GPL v3 全文）、各 DLC `init.lua` 头部声明；公开正式版位于 `/Users/yun/projects/tome4-dlcs/`（ashes/cults/orcs，version 1.7.4）。
- GPL v3 §2：不分发的使用（读取/分析/提取/翻译）无条件允许；禁止条款不适用于本场景。但**分发**基于 DLC 的衍生作品（含译文）时须遵守 §5：保留版权声明、以 GPL v3 兼容许可发布、提供对应源码。本项目译文与发布 addon 应随附 GPL v3 声明。
- 不再禁止直接读取 DLC 源码；可复现基线仍建议使用受审计提取脚本（extract 生成规范化快照 + SHA-256 基线，doctor/extract 自动校验）。提取来源已切换至公开正式版 `/Users/yun/projects/tome4-dlcs/`（2026-08-04 验证：两处副本 t() 的 src 序列完全一致，ashes 完全一致；cults 37 个 / orcs 2 个非 t() 内容差异不影响提取）。快照基线含 origin 元数据（section/origin_line），来源切换后若 extract 报基线 mismatch，属预期，重建基线即可（tdef_count 不应变化）。
- Pi 翻译、Pi 审核、其他 subagent 以及人工审校的输入边界不变：翻译审校只能接收规范翻译条目的有界 bundle；代码审校只能接收去除绝对路径后的公开代码 diff。任何审核结果都只能写入 `.artifacts/i18n/`，不得自动应用到规范 Lua 或代码。

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

本节是整个项目所有审核任务的共同底座，适用于译文、术语、代码/脚本、测试、配置、prompt、文档、artifact 契约以及构建发布流程。后文的 Pi 输入边界、源码判定依据、术语工作流和门禁检查仍是对应任务的附加硬约束；通用流程不得绕过它们。

审核开始时必须先明确并记录：

- 模式：仅审核，或审核并修复；
- 范围：组件、文件、diff、artifact 或具体调用链；
- 维度：翻译质量、术语一致性、功能正确性、性能、构建发布等；
- 外部边界：是否允许 Pi/provider、公开源码核验或外部仓库读取；
- 完成标准：交付 findings，或修复后收敛到一轮干净复审。

审核维度以用户明确范围为准，不得擅自扩展成安全对抗、全仓风格重构或无关质量工程；但会直接造成错误结果、数据丢失、状态破坏或明显性能退化的问题仍属于功能 finding。

### 1. 先固定基线和审核范围

- 开始前先记录 `git status --short`、`git diff --name-only` 和 `git diff --stat`，区分任务开始前已有改动、本轮改动和未跟踪文件；脏工作树不得被清理、重置或顺手格式化。
- 用户未明确授权时不得用 commit 作为 checkpoint；需要记录审核状态时，在对话或已忽略的 `.artifacts/i18n/` 中维护简短清单即可。
- 首次运行工具先执行 `python3 -B tools/i18n doctor`。先确认实际 changed/new 文件和任务指定输入，再决定需要阅读、核验和测试的子系统，不得把全仓无差别搜索当作默认起点。

### 2. 只读审核完成后再开始修复

- 第一阶段保持只读，先收齐并冻结一轮 findings；不要采用“发现一个、立刻修改、再从头审核”的无界循环。仅审核任务在 findings 冻结并完成证据核对后即可交付，不得自行进入修复。
- 按审核对象选择检查矩阵：
  - **译文/术语**：固定版本源码与实际机制 → section/source_tag/context → 术语与领域 → 占位符/markup/特殊参数 → 运行键覆盖 → 中文准确性与流畅度；
  - **代码/脚本/artifact**：上游输入与版本 → 身份/新鲜度摘要 → 缓存键 → 内存语义 → 写入/提交事务 → 失败与退出码 → 下游消费者 → 热路径复杂度；
  - **配置/prompt/文档**：权威 schema/实现 → 生产者与消费者 → 字段和版本 → 示例命令 → 失败语义 → 文档陈述是否与实际行为一致；
  - **构建/发布**：规范输入 → 生成内容 → 完整性标记 → 原子写入/回滚 → Git 状态 → 加载链与 smoke。
- finding 必须有源码/上下文证据、可触发的错误行为、最小复现或明确调用链；单纯缺少测试、个人译法偏好、理论上的残留目录、风格问题或无法证明会被下游当作成功结果消费的部分产物，不得作为已确认 finding。
- finding 由宿主/主代理统一标记为“已确认”“待确认”或“advisory”，不能接受模型自报状态。只有已确认 finding 才由主代理定级并进入自动修复队列；待确认项必须写明缺失证据，不得猜测升级。
- 对内容寻址 artifact，必须一次性核对完整 lineage：审核者可见的完整 payload、所有会改变其语义的规范输入、规则/manifest、生成器版本和父 artifact 身份都应被绑定；消费者优先重算廉价字节摘要，不得为了新鲜度校验重建大型 inventory 或重复运行 Lua loader。
- 机制和语义结论遵循后文“校对判定依据”；性能结论必须基于调用次数、复杂度、数据规模或实际计时，不得仅凭代码观感报告性能 finding。

### 3. 有界修复和子代理使用

- 仅在用户授权修复时，才对已确认 findings 按依赖关系排序修改。即使用户要求逐项交付，也应先完成当前审核面的 finding 清单，再逐项修改，避免同一术语、机制或 artifact 契约被拆成多轮互相失效的补丁。
- 每个修复任务必须写明：唯一 finding、允许修改的文件、禁止扩展项、最小回归测试和完成条件。无上下文子代理必须在完成这些条件后立即回报，不得继续扩展搜索或重构相邻代码。
- 子代理的测试结果不能替代主代理的独立复核；但主代理和子代理不应在每个小修复后都重复完整门禁。出现长时间无可见进展、反复扩大测试或偏离 finding 时，主代理应先要求状态并及时收束或中断。
- 未获用户授权时不得为了提速擅自并行代理；获准并行时，仅并行互不写同一文件的只读审核或独立修复。

### 4. 分层验证，避免重复全量运行

按以下层级验证所有审核修订：

1. **单 finding**：译文/术语核对对应源码与上下文并运行最小 lint；代码运行最接近的测试类/表驱动回归和相关模块 `py_compile`；配置/文档核对实际消费者或 schema；所有改动检查受影响文件的 `git diff --check`。
2. **子系统批次**：按任务运行组件级 lint、术语审计、相关 `-k`/测试类或一条真实但无外部副作用的命令路径；性能修复应增加调用次数或不触发昂贵路径的断言。
3. **最终集成**：运行本任务适用的完整门禁、构建和 smoke，只在本批修复收束后统一执行。高风险共享基础设施改动可提前追加一次完整测试，但不要机械重复；任何外部 provider 调用仍须单独授权。

- 测试 fixture 应优先使用表驱动和共享 helper，避免为每个类型变体复制整段大型样本。
- 不要把包含数万行条目的 `--json` 结果直接输出到终端；优先使用普通摘要、将完整 JSON 留在 `.artifacts/i18n/`，或只读取需要核对的字段。
- 每次完整门禁只记录一次结果、耗时和对应代码状态；代码未变化时不得仅为“更放心”重复相同长门禁。

### 5. 明确停止条件

- **仅审核任务**：审核范围已完整覆盖，findings 已冻结并完成证据分级，即可交付；不要求擅自修复或无限追加复审。
- **审核并修复任务**：所有授权范围内的已确认 findings 已修复并通过定向验证；完整门禁、适用构建和 smoke 通过；再进行 **一轮** 全新、只读、无上下文复审，且没有新的已确认 finding。

对应模式满足上述条件即视为审核收束。若最终复审发现新问题，修复后再做一轮干净复审；若只剩待确认或 advisory，应明确记录并停止，不得以追求绝对零风险为由无限增加审核轮次。用户明确要求“直到没有问题”时，也以最后一轮独立复审无新确认 finding 作为可验证的完成标准。

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
- 公开游戏与三个官方 DLC 源码可以在只读范围内直接核验。若未来引入未公开组件，其机制核验只能使用受审计 Lua 提取器生成的去敏快照或有界证据，不得为确认机制而直接读取、枚举或搜索未授权目录；证据不足时应将结论标为待确认，不得猜测。

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology.tsv`。
- 主代理阅读术语库不等于把术语或 Facts 注入 blind semantic discovery；术语/专名疑点只能在 observation 产生后按 claim 核验与裁决。
- 新增或修改高复用术语时，先更新 `terminology.tsv`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
