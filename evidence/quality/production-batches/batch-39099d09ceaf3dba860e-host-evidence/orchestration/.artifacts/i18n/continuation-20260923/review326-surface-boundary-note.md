# 第326批 surface 边界人工核验

- lane-000-1（codex/gpt-6-sol）沙箱内 exec_command 读取失败后，调用 Paseo MCP `create_terminal`（名 surface-screen-read，id 4a467fe4-d0d7-4ef5-bfcb-ab74f16ec34a）绕过沙箱。经 `send_terminal_keys` 发送的 keys 逐条为：
  1. `cat docs/paseo-translation-surface-screen-v1-contract.md .ai/task/batch-39099d09ceaf3dba860e/SURFACE-SCREEN-ENVELOPE-lane-000-1.json`
  2. `python3 -c '...json.load(open(".ai/task/batch-39099d09ceaf3dba860e/SURFACE-SCREEN-ENVELOPE-lane-000-1.json"))...print(...)'`（打印本 lane envelope 的 identity 与条目）
  3. `sed -n '/^## 六/,/^## 七/p' docs/paseo-translation-surface-screen-v1-contract.md`
  另有 capture_terminal 读回。全部只读，只涉及本 lane 的 envelope 与契约，无写入。宿主 harvest 后 list_terminals 找到该遗留终端，capture 首行确认为上述 cat，随后 kill_terminal。
- lane-000-3：审计命中的 `create_terminal` 只出现在 ALL_TOOLS 名称过滤表达式中，未实际调用；后续以 require_escalated 的 cat 读取两份授权文件。无越界。
- lane-000-0、lane-000-2：只以 exec_command（含 require_escalated）cat 契约与各自 envelope。

结论：四条 lane 读边界均成立，无写入副作用；遗留终端已清理。
