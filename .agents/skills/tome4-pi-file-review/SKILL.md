---
name: tome4-pi-file-review
description: 使用带 read/bash 白名单的 Pi reviewer，对 ToME4 code/legacy v1 bundle 做源码感知核验。用于需要读取项目、游戏或 DLC 公开源码来验证代码 finding 的场景；不用于 translation v2、隔离 bundle 审核、翻译生成或任何写入任务。
---

# ToME4 Pi file-reading review

使用源码感知 runner 核验 code/legacy v1 finding。该 runner 允许 `read,bash`，但没有
OS 级沙箱；可读范围、外发记录和授权直接遵循 `AGENTS.md` 及
`i18n/prompts/pi-reviewer-files.md`。

当前 runner 必须拒绝 translation v2。claim-bound translation verifier 实现前，
translation observation 由主代理按固定源码版本直接核验。

## 准备与运行

生成最小 code bundle，并在 `review-index.json` 中确认 `review_contract` 为
`tome4-review-v1`：

```bash
python3 -B tools/i18n review --scope code
```

记录运行前的 `git status --porcelain`，然后在 tmux 中运行一个 bundle：

```bash
tools/pi-tmux review-files --bundle <absolute-bundle-path>
```

无 tmux 时添加 `--fallback foreground`，或使用 headless 入口：

```bash
tools/pi-review-files --bundle <absolute-bundle-path>
```

- file-reading 审核始终新跑；不要传 `--cache`，`--force` 仅保留兼容性。
- 使用默认严格校验；除非用户明确要求，不覆盖 provider/model/thinking。
- 大索引逐 bundle 处理，不扩大允许读取或外发的范围。

## 核验结果

runner 会比较运行前后的版本控制范围快照。结束后主代理仍需再次运行
`git status --porcelain`，与原基线比较；原有脏工作树不得被清理或覆盖。

只读取已校验的 legacy `review.json` / `pi-review.json`，保留 `bundle_id`、`item_id`
和源码证据。模型 finding 只是建议；主代理根据固定版本源码独立确认、定级并决定
是否修复。不得由 reviewer 直接修改文件或自动应用建议。
