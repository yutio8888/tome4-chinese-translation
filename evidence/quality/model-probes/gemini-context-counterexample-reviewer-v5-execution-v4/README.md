# Gemini context-counterexample REVIEWER — V5 execution v4

这是 `research-gemini-context-counterexample-reviewer-v5-execution-v4` 的本地路径验证包，不是模型效果结果。

## 状态与边界

- execution-v3 是不可变前序包。其权威树哈希为
  `83201688dfa55420330766ef8b1c75954058cd4103ed10f4fee418979d5867c6`，共 74 个文件。
- v3 没有产生模型证据；此前的停止原因是调用了不兼容的 `models list --json` 路由，不是模型结果。
- 原 capture 路由 `/home/yun/.local/bin/agy` 当时绑定的合格字节为
  `d492241f19f90ea06cb9f85f7788c371dbce3386206d734ddc2c7ec84fa3ddca`；该路径当前已升级为被拒绝的
  `f3575050ae826d1944913f595b32f827a4674ec42e59ff0476450e2bac5fa39e`。v4 仅把未来执行路径迁移到
  `/home/yun/.local/bin/agy.1788410029995956792.old`，其字节仍是同一合格哈希；model、effort 和 argv
  均不变。`ROUTE-RELOCATION-CONTRACT.json` 显式绑定原 route SHA-256 `742529e3...`、当前迁移后
  route SHA-256 `f82ac7fd...`、两条路径及合格/拒绝哈希。历史 capture 继续保留原路径和原 route，
  只有该同字节迁移契约有效时才可复用，不把升级后二进制洗成已 qualification。call 1 仍固定为
  `agy models`；qualification 与 A/C runner 在每次未来 spawn 前都重新核验 backup 路径和实际 SHA-256。
- v4 `retries=0`：qualification 和执行 cell 每个最多一次 attempt；失败、超时或不可解析结果不会产生第二次 spawn。
- call 1 和 call 2 的成功捕获分别由 `qualification/REUSE-CONTRACT.json` 与 `qualification/SYNTHETIC-REUSE-CONTRACT.json` 绑定；两个契约都在 `MANIFEST.json` 中列出。契约保存原候选 manifest、旧 PACKAGE gate、route/executable、argv（call 2 为 argv 哈希）与 stdout/stderr 哈希。call 2 契约只绑定 ledger 最前面的四条规范 qualification START/FINISH 行及其确定性前缀哈希；后续合法执行行可继续 append，但这四行的内容、顺序或哈希漂移都会 fail closed。复用前会逐项校验这些绑定，失败即停止，不会 respawn。
- 本次 P0 实现、测试、冻结和 preflight/post-run 均不调用 agy、模型或网络；v4 的 call 1、call 2 复用是既有成功捕获的确定性读取，不产生新的进程。双通道 envelope 只接受 `structured_output` 为权威、且 JSON 字符串 `response.items` 与其逐字节相等的情况。
- 即使后续获得门禁授权，四进程 pilot 也只是 CLI 路径验证，不支持协议效果或模型能力结论；完整 32 请求运行需要另行授权。

## v4 变更

v4 从 v3 的静态源码和测试重建，初始复制时排除 execution、qualification、PILOT、SCORES、请求、sealed reference 以及冻结阶段生成的样本/请求清单。`build-frozen-base.mjs` 只从既定前序源码重放 64 个 bases 和前序绑定；`freezer.mjs` 再确定性生成 64 samples、sealed reference 和 32 个请求。

模型列表解析器只接受 UTF-8 明文 TSV：CRLF 归一化、逐字段 trim、忽略空行；每个非空行必须严格为 `model_id<TAB>display_name` 两字段且字段非空，目标模型必须作为第一字段恰好出现一次。缺失、重复、空字段、非 TSV、额外字段或仅作为子串出现均 fail closed。模型清单调用没有 `list`、`--json` 或 `--version`。

## 固定门禁

包代码只读取、从不写入以下 v4 task-owned gate；门禁顺序固定为三项：

1. `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/PACKAGE-REVIEW-GATE.json`
2. `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/QUALIFICATION-GATE.json`
3. `.ai/task/research-gemini-context-counterexample-reviewer-v5-execution-v4/EXECUTION-AUTHORIZATION.json`

执行仍由一个 append-only ledger、一个 scorer 和一个 preflight 约束。qualification 也只能在 execution ledger 中 journal；本轮不写入 task gate、receipt、ledger 或既有 capture，复用凭据仅记录既有 call 1 的来源。

## 文件与验证

- `MANIFEST.json`：自排除、按字节序排列的源码哈希清单；`ROUTE-RELOCATION-CONTRACT.json` 和两个 reuse contract 是冻结 provenance source，qualification 的 capture/request/draft/raw/evidence 仍是生成文件。
- `EXPERIMENT.json`、`DESIGN-CONTRACT.json`、`REQUEST-CONTRACT.json`、`ROUTE-CONTRACT.json`、`GATES.json`：v4 身份及契约。
- `build-frozen-base.mjs`：验证终止 V5 前序文档/树，并绑定不可变 execution-v3 树。
- `freezer.mjs`：确定性构建/检查 64 samples、reference 和 32 request identities；期望 `exact_source_appended_count=7`。
- `qualification.mjs`、`runner.mjs`、`parser.mjs`、`ledger.mjs`、`scorer.mjs`、`preflight.mjs`、`post-run.mjs`：分别负责受门禁路由、双通道解析、ledger、计分和只读检查。qualification draft/evidence 贯穿两个 reuse contract 的路径、哈希和完整 provenance。
- `tests/test-package.mjs`：只使用 mock invoke，不产生 agy 或网络调用；覆盖前冻结和后冻结行为。

推荐本地检查顺序：

```bash
node --check *.mjs tests/*.mjs
node build-frozen-base.mjs --check
node build-manifest.mjs --check
node freezer.mjs --check
node tests/test-package.mjs
node preflight.mjs       # 当前已有 call-1 前缀：NO_GO_REQUIRED_GATES + 1 process + 0 inference
node post-run.mjs        # 门禁/qualification 尚未完成时应拒绝作为结果
```

本轮不运行 `agy`、`qualification` 生产路径或 `run.mjs`；只读校验既有 call 1–2 captures，不写 v4 task gates/receipts，不修改 v3 或更早目录，也不进行 git 操作。
