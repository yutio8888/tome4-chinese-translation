---
name: tome4-pi-file-review
description: Run bounded, read-only Pi audits where the reviewer may read project, game and DLC source files to verify evidence (read/bash tools only, no write tools, no session, no skills). Use for source-verification review passes over translation bundles or public code changes when findings should be checked against actual sources; do not use for isolated bundle reviews (use $tome4-pi-review), translation generation, or any task needing write access.
allowed-tools: read bash
---

# ToME4 Pi file-reading review

与 `$tome4-pi-review` 同源的审核变体，唯一区别：Pi 子进程带 `--tools read,bash`
白名单启动，按提示契约只读核验项目、公开游戏与 DLC 源码来验证证据；`edit`/`write`
始终未启用，会话、skills、上下文文件仍然禁用。Pi 内置 `bash` 不是 OS 沙箱，
会继承 Pi 进程权限与 provider 凭据，因此该变体只能用于已授权、受监控的核验；
需要强隔离时须使用只读挂载、网络/凭据隔离的容器或 VM。bundle 边界、item_id
绑定、findings 契约、严格校验与报告字段与隔离审核兼容。file-reading 审核不会
复用结果缓存，因为 `read/bash` 可观察 bundle 外的可变源码状态，现有缓存键无法
可靠绑定这些输入。

每个审核或修复调用默认最多 20 分钟（1200 秒），保持该 per-bundle 超时，
除非用户明确要求其他时限。

## 准备审核

1. 先阅读当前 `AGENTS.md`；翻译审核还需先读 `TERMINOLOGY.md` 和
   `terminology.tsv`。
2. 用最小范围生成 bundle：
   - 翻译：`python3 -B tools/i18n review --scope translations`
   - 公开变更：`python3 -B tools/i18n review --scope code`
   - 两者：`python3 -B tools/i18n review --scope translations --scope code`
3. 阅读生成的 `review-index.json`（只读索引，不读受保护路径），报告 bundle
   数量与范围后再调用 Pi。

## 授权外部审核

Pi 会把每个有界 bundle 发送给配置的外部 provider。首次真实调用前，必须明确
说明 provider、model、bundle 类型、条目数量，以及 bundle 内容会离开本地
沙箱并取得用户明确授权。不得启用项目级网络放行或绕过审批；被拒绝就停止，
不得间接调用 Pi 或经其他通道复制数据。

## 运行（tmux 分屏可见）

一次只调用一个已校验 bundle（工具默认使用当前 tmux 会话）：

```bash
tools/pi-tmux review-files --bundle <absolute-bundle-path>
```

`review-files` 子命令与 `review` 相同的 pane 行为：默认保留 pane 供检查
（结束提示 `tmux kill-pane -t %N`）、`--no-keep-pane` 关闭、`--layout`/
`--percent`/`--session` 控制布局、`--fallback foreground` 无 tmux 时前台运行。
file-reading 审核每次都会启动新的 pane（或按配置回退前台），不会命中旧结果。

无 tmux / 脚本场景用 headless 入口：

```bash
tools/pi-review-files --bundle <absolute-bundle-path>
```

`--cache` 会被明确拒绝；`--force` 仅为既有调用兼容而保留，用它表达“必须新鲜”
是安全的，但因每次 file-reading 审核本来都会新跑而无需特意添加。两者都绝不
用于绕过外部传输授权。大索引分批处理，报告进度，且只在已授权范围内继续。
provider/model/thinking 默认沿用项目默认，除非用户要求覆盖。

## 运行后检查

1. 工具会比较运行前后的版本控制范围内容级快照（受管 diff、非忽略未跟踪
   文件内容与 Git exclude）并在发生变化时失败；该检查不覆盖其他忽略路径或
   其余 `.git` 元数据。runner 会清理 Pi 进程组后再比较快照，但无法覆盖自行
   脱离进程组的后代。主代理仍须再次运行 `git status --porcelain`，确认结果与运行前一致（工作树原本可为非空），
   并确保 `git diff --check` 通过。`--tools read,bash` 只限制工具种类，不是
   文件系统、网络或凭据沙箱。
2. 只读已校验的 `review.json` / `pi-review.json` artifact（与 headless 管线
   形状一致）。按 severity 汇总 findings，保留 `bundle_id` 与 `item_id`，
   区分 Pi 的声称与独立核实的事实。
3. 不得自动应用建议或修改规范 Lua/代码；修订走 `tools/pi-tmux remediate`
   或人工审校流程。

## Pi 的读取边界

系统提示（`i18n/prompts/pi-reviewer-files.md`）规定：

- 可读：仓库根（规范译文 `tome-*.lua`、`i18n/`、`tools/`、`tests/`、`docs/`、
  `TERMINOLOGY.md`、`terminology.tsv`）、`/Users/yun/projects/t-engine4`
  （GPL v3）、`/Users/yun/projects/tome4-dlcs/`（ashes-urhrok、cults、orcs，
  GPL v3）。
- 禁止：`.artifacts/`（其他审核/缓存/工作清单）、bundle 文件本身（已内联）、
  凭据、钥匙串、`~/.pi/`、可读根之外的绝对路径、网络、git 写操作、一切文件修改。

主代理不得把受保护 DLC 路径、凭据、任意工作区文件或工具交给 Pi。

## 证据与判定

- 机制核验以版本清单固定的 commit 为准（见 `AGENTS.md` 校对判定依据）：记录
  组件、公开源码相对路径与关键调用；工作树与固定 commit 不一致时以固定 commit
  为准。
- 依赖工具证据的 finding 应含「证据：<相对路径>」；证据不足标待确认，不得臆测。
- 闭源 DLC 输入边界不变：即使有文件读取权限，也不得为核验机制直接读取、枚举
  或搜索受保护目录。
