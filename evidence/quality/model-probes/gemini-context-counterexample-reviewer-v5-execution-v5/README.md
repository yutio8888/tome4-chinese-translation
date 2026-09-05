# Gemini context-counterexample REVIEWER — V5 execution v5

这是 `research-gemini-context-counterexample-reviewer-v5-execution-v5` 的新鲜、本地、非计分路径验证包，不是模型效果结果。

## 边界与前序

- execution-v3 因不兼容的模型列表 argv 停止；没有产生模型效果证据。
- execution-v4 因其绑定的 route binary 消失而终止，权威树 SHA-256 为 `40240912722cebed3f1a3319c73ec5a6ba48d9c9a9508262042e64da3865f323`；其 2 个进程、1 次非计分推理、ledger、captures、qualification 产物、reuse/relocation contract 和 PILOT 结果均不得进入 v5。
- execution-v5 只验证新鲜四进程路径。即使未来 pilot 完成，也不能据此声称 A/C 协议效果、模型能力或泛化；完整 32-request 实验仍需另行授权。

## 固定路由和预算

唯一可执行文件是：

`/home/yun/.local/lib/agy-pinned/f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e/agy`

固定 SHA-256：`f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e`。

`/home/yun/.local/bin/agy` 是 updater-managed 路径，不得使用。qualification 和 runner 在每次 ledger START 与 spawn 之前核验固定路径是普通可执行文件且哈希匹配。call 1 argv 严格为 `['models']`；模型清单严格解析为两字段 TSV，目标模型必须在第一字段恰好出现一次。agy 双通道只在 `structured_output.items` 与 JSON 解析后的 `response.items` 完全相等时接受。

授权上限是 4 个进程、3 次推理，`MAX_ATTEMPTS=1`：models、synthetic、A、C。失败不重试；A 必须成功并解析后才能运行 C。production CLI 的失败或无效解析返回非零。

## 冻结与门禁

freezer 确定性生成 64 samples、32 requests、35 个冻结目标，并要求 7 次 exact-source append、无内部标识泄漏。qualification 初始必须没有任何 inherited ledger/capture；capture 与 finalization 分成两阶段，只有 task owner 写入的 archived receipt 才允许纯 finalization。包代码只读取而不写入三个 task-owned gates：

1. `PACKAGE-REVIEW-GATE.json`
2. `QUALIFICATION-GATE.json`
3. `EXECUTION-AUTHORIZATION.json`

本实现阶段禁止运行 production qualification、agy、模型或网络。测试只使用 mock invoke，并清理全部 `/tmp/v5x5-*` fixture。

## 零调用检查

```bash
node --check *.mjs tests/*.mjs
node build-frozen-base.mjs --check
node build-manifest.mjs --check
node freezer.mjs --check
node tests/test-package.mjs
node preflight.mjs   # 预期 NO_GO_REQUIRED_GATES，NO_RUN，0 process / 0 inference
```
