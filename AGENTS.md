# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 汉化工具入口

- 当前版本的自动化入口统一为 `python3 -B tools/i18n <command>`；`tools/i18n` 可执行位可用时也可直接调用。
- 首次运行先执行 `tools/i18n doctor`，译文修改后执行 `tools/i18n lint`。
- 工具会在启动 LuaJIT 子进程时自动设置本文件规定的 `LUA_PATH` 和 `LUA_CPATH`，不得要求用户手动导出。
- `extract`、`lint`、`status`、`merge`、`workset`、`context`、`proposal`、`review` 和 `build` 的报告或候选文件只写入已忽略的 `.artifacts/i18n/`；没有显式安装命令时不得改写游戏源码仓库或发布模组仓库。
- Pi 翻译入口为 `tools/pi-subagent --workset <workset.json>`（需要实时观察时可用 `tools/pi-tmux translate --workset <workset.json>`，在 tmux 分屏中执行）。该进程必须保持无工具、无会话、无项目上下文，只能输出 proposal artifact；其结果必须通过 `proposal --strict`，不得直接写规范 Lua。
- Pi 审核入口为 `tools/i18n review` 生成 bundle，再用 `tools/pi-tmux review --bundle <bundle.json>` 执行（默认在当前 tmux 会话分屏运行，便于观察审核过程；无 tmux 环境用 `--fallback foreground`，脚本场景可直接用 `tools/pi-review`）。审核 bundle 可以覆盖全部规范翻译条目（按批次）和当前公开工作区代码 diff；Pi 必须保持无工具、无会话、无项目上下文，只能输出结构化 findings artifact，不得直接修改文件。
- Pi 处理审核意见入口为 `tools/pi-tmux remediate --bundle <bundle.json> --review <review.json>`（headless 可用 `tools/pi-remediate`）。该进程只能输出绑定到 finding/item 的 remediation proposal；主代理必须独立校验并应用修订，再重新运行审核，不得让 Pi 直接写规范 Lua 或代码。
- 当用户要求开展 Pi 审核时（无论主代理是 Codex 还是 Pi），使用项目 Skill `$tome4-pi-review`；交互式审核默认在 tmux 分屏中运行，pane 保留至 `tmux kill-pane -t <pane>`。首次向外部 provider 发送 bundle 前，必须明确报告 provider、model、bundle 类型和条目数量并取得用户授权；不得用项目级全局网络放行绕过该授权。

## 闭源 DLC 输入边界

- `/Users/yun/projects/t-engine4/game/dlcs` 及 `TOME_DLC_ROOT` 指向的目录是闭源受保护输入。代理不得用 `ls`、`find`、`rg`、`grep`、`cat`、`sed`、Git 命令、Python/Node 文件 API 或编辑器直接读取、枚举或搜索其中的文件和目录。
- 只有仓库内受审计的 Lua 提取脚本可以读取受保护目录。非 Lua 调度层只能传入预先声明的组件路径，且只能读取 Lua 生成的文本快照和去敏摘要。
- 受保护提取不得保存或显示源码、源码片段、原始解析日志、绝对 DLC 路径或未声明的目录清单。解析失败必须静默、失败关闭，只报告组件和错误类别。
- Pi 翻译、Pi 审核、其他 subagent 以及人工审校输入都不能获得受保护源码路径或文件读取工具。翻译审校只能接收规范翻译条目的有界 bundle；代码审校只能接收去除绝对路径后的公开代码 diff。任何审核结果都只能写入 `.artifacts/i18n/`，不得自动应用到规范 Lua 或代码。

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
- **译文批量修改后**在提交前运行门禁 1–5；涉及 Pi 复审时按 `docs/runtime-key-collisions.md` 与 `docs/pi-review-worker-tuning.md` 的流程执行（并行批处理默认 `--workers 6`，8 起限速劣化）。
- 审计与扫描脚本均在 `tools/` 下版本控制，输出只写入 `.artifacts/i18n/`（忽略目录），不直接改写规范 Lua。

## 校对判定依据

- 当翻译、术语、审核意见或英文表面含义对游戏机制的描述存在分歧时，以当前版本清单固定的游戏源代码实际行为为最终判定依据；现有译文、术语库和模型 finding 都不能覆盖源码事实。
- 核验机制时应记录对应组件、公开源码路径、固定 commit 和关键调用或数据定义，并据此确认、部分确认、撤销或修订审核结论；当前工作树与固定 commit 不一致时，默认以版本清单固定的 commit 为准，除非用户明确指定其他目标版本。
- 公开游戏源码可以在只读范围内直接核验。闭源 DLC 的机制核验仍必须遵守“闭源 DLC 输入边界”：只能使用受审计 Lua 提取器生成的去敏快照或有界证据，不得为确认机制而直接读取、枚举或搜索受保护目录；证据不足时应将结论标为待确认，不得猜测。

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology.tsv`。
- 新增或修改高复用术语时，先更新 `terminology.tsv`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
