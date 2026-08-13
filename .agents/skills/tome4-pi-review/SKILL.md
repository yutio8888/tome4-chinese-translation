---
name: tome4-pi-review
description: 为 ToME4 规范译文或公开代码变更生成有界 bundle，并通过无工具 Pi reviewer 运行 translation v2 或 code/legacy v1 复审。用于译文审校、代码审核和独立复审；不用于翻译生成、源码感知核验，或向 translation v2 注入术语、Facts、既有 findings。
---

# ToME4 Pi review

通过仓库 runner 构造、发送并校验审核 bundle。外发范围、provider/model 记录和主代理
裁决规则直接遵循 `AGENTS.md`，不要在本 Skill 中另建授权流程。

## 生成 bundle

选择满足任务的最小 scope：

```bash
python3 -B tools/i18n review --scope translations
python3 -B tools/i18n review --scope code
python3 -B tools/i18n review --scope translations --scope code
```

- translation 使用 blind semantic v2，只发送稳定的 revision/source/target provider
  projection；不得加入术语库、Facts、源码、历史 finding 或裁决。
- code 使用 legacy v1，仅包含公开变更。
- 读取生成的 `review-index.json`，按 descriptor 逐个选择 bundle，并确认 contract、
  channel、条目数和任务 scope 一致。

## 运行审核

在 tmux 中运行一个已校验 bundle：

```bash
tools/pi-tmux review --bundle <absolute-bundle-path>
```

- 无 tmux 时按场景添加 `--fallback foreground`，或在脚本中直接用
  `tools/pi-review --bundle <absolute-bundle-path>`。
- 默认使用严格校验和精确缓存；只有明确需要新观察时才使用 `--force`。
- pane 默认保留，检查完成后按工具输出的 `tmux kill-pane` 命令关闭。
- 大索引按 bundle 顺序处理，不扩大原审核范围。

## 解释结果

只读取 runner 生成的已校验 `review.json` / `pi-review.json`：

- translation v2 observation 保持 pending，保留 identity 与 evidence，由主代理核验和
  定级；空 observation 不能代表语言质量已全面通过。
- code v1 finding 可按 severity 汇总，但仍须由主代理独立确认。
- 不自动应用模型建议，不直接修改规范 Lua 或代码。

只有已确认的 legacy finding 可以进入 remediation：

```bash
tools/pi-tmux remediate --bundle <absolute-bundle-path> --review <validated-review.json>
```

translation v2 结果不兼容该 remediation runner；按 `AGENTS.md` 的 claim 核验与人工
裁决流程处理。
