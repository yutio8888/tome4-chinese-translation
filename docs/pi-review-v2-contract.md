# Pi 审核子进程 semantic observation v2 技术契约

> 状态：规范。本文件收纳 translation v2 的技术执行细节，供 runner 与子进程实现遵循；
> 角色与边界总纲以 `AGENTS.md` 为准，本文件不单独授权任何外部传输。

本文适用于 `tools/pi-review`、`tools/pi-tmux review` 启动的 translation semantic
observation v2 子进程。代码审校保留 legacy v1 finding 契约（见 `tools/i18nlib/pi_review.py`）。

## blind payload 与宿主 lineage 隔离

- blind provider payload 不注入 terminology/Facts、canonical membership 或任何宿主 lineage，
  只包含最小 revision/source/target 输入。
- 主代理阅读 `TERMINOLOGY.md` / `terminology.tsv` 不构成向 blind discovery 注入；
  术语/专名疑点只能在 observation 产生后按 claim 核验与裁决。

## 分包与身份绑定

- 按 10 条硬上限与 item canonical JSON 字符预算双重分包。
- `selection_sha256` 绑定跨 shard 的完整有序 revision 集。
- review index 分别记录宿主 `artifact_bytes` 与实际外发 `payload_bytes`。

## 精确 user message 发送（不得用 `@file`）

- v2 的精确 JSON user message 必须经 stdin 发送，不得使用会注入绝对路径 wrapper 的
  `@file` 展开。
- 必须用显式空 `--append-system-prompt` 关闭 project/global `APPEND_SYSTEM.md` 自动发现。
- Pi cwd 使用不含项目路径的系统临时根：优先 `/private/tmp`，不存在时回落到 `/tmp`。
  实际选择的 cwd 必须写入报告，并通过 system prompt 摘要进入 evaluator/cache identity；
  不得回落到仓库目录或用户目录。
- 实际 user/system prompt、runner、policy 与 normalizer 都必须进入 evaluator/cache identity。

## 模型返回契约

模型逐 item 返回：

- `assessment_state`
- 可观察语义差异
- 精确 source/target evidence

模型不得填写 severity、确认状态或 suggested fix；宿主只做结构、span、identity 与
pending 路由，主代理独立裁决。

## 相关入口

- 审核 bundle 生成：`tools/i18n review --scope translations`
- 交互执行：`tools/pi-tmux review --bundle <bundle.json>`（tmux 分屏，pane 保留至
  `tmux kill-pane -t <pane>`）
- headless 执行：`tools/pi-review --bundle <bundle.json>`
