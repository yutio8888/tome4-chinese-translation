# 第329批 surface 边界人工核验

- lane-000-0（codex/gpt-6-sol）先以 exec_command 读取本 lane envelope 与契约，随后调用 Paseo MCP `create_terminal`（名 surface screen read，id 5ef8e922-64c5-4e93-8ccf-f7e507ce7d51）。经 `send_terminal_keys` 发送的 keys 逐条为：
  1. `cat .ai/task/batch-dd7c9f57b4d10b8580df/SURFACE-SCREEN-ENVELOPE-lane-000-0.json docs/paseo-translation-surface-screen-v1-contract.md`
  2. `stty cols 300` 与 `python3 -c '...json.load(open(".ai/task/batch-dd7c9f57b4d10b8580df/SURFACE-SCREEN-ENVELOPE-lane-000-0.json"))...print(...)'`（打印本 lane envelope 的条目数、briefing、术语快照、fixed_source_identity、rules_version）
  3. `python3 -c '...'`，打印本 lane envelope 各条目的 identity、source、target
  4. `python3 -c '...'`，只打印本 lane envelope 各条目的 identity
  另有 capture_terminal 读回。全部只读，只涉及本 lane 的 envelope 与契约，无写入。宿主 harvest 后用 list_terminals 找到该遗留终端，capture 首行确认为上述 cat，随后 kill_terminal。
- lane-000-1、lane-000-2、lane-000-3：只以 exec_command cat 契约与各自 envelope（含 ALL_TOOLS 过滤列举），无写入模式命中。

结论：四条 lane 读边界均成立，无写入副作用；遗留终端已清理。
