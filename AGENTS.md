# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

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

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology.tsv`。
- 新增或修改高复用术语时，先更新 `terminology.tsv`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
