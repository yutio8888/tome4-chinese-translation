# 常见操作陷阱记录（Lessons Learned）

> 本文件记录工具链开发与发布操作中实际踩过的坑，避免后续重复犯错。
> 每次踩坑修复后应在此追加条目（含日期、场景、根因、正确做法）。

## 1. 外部仓库 / CRLF 文件的行尾保护（2026-08-04，tome-chn-mod）

**场景**：修改发布仓库 `tome-chn-mod` 的 `data/null_translation.lua`（CRLF 行尾）。
**事故**：Python `Path.read_text()` / `write_text()` 默认 universal newlines，
读入时把 `\r\n` 归一化为 `\n`，写回后整文件变 LF——git diff 显示 2027 行
噪音（本应只有 ~100 行），被迫 `git reset` 重做。
**正确做法**：

```python
text = path.read_bytes().decode("utf-8")   # 保留 \r\n
# ... 做替换 ...
path.write_bytes(text.encode("utf-8"))
```

修改任何**已有版本控制文件**前，先检测行尾：

```bash
file <path>                                   # 显示 "with CRLF line terminators"
python3 -c "d=open(p,'rb').read(); print(d.count(b'\r\n'), d.count(b'\n'))"
```

## 2. CRLF 文件内 Lua 字面量的换行（2026-08-04，tome-chn-mod）

**场景**：在 CRLF 文件中定位 `t([[多行 source]], ...)` 的 source 字面量。
**事故**：用 loader 解码的 source（内部 `\n`）直接构造 `"[[" + src + "]]"`
去 `text.find()`——文件里实际是 `\r\n`，全部定位失败。
**正确做法**：构造字面量时把 `\n` 转为 `\r\n`：

```python
src_lb = "[[" + src.replace("\n", "\r\n") + "]]"
```

同理，替换后的新字面量内部换行也应写 `\r\n` 以保持文件风格一致。

## 3. `re.sub` 替换字符串中的 `{}`（2026-08-04，publish --bump）

**场景**：`re.sub` 把 `addon_version = {0,2,0}` 替换为新版本号。
**事故**：替换串 `"{0,2,1}"` 中 `{0,2}` 被 Python re 解析为**量词**，
结果 "addon_version = " 前缀被吞，行变成 `{0,2,1}`。
**正确做法**：替换串必须包含完整匹配段：

```python
new_version = f"addon_version = {{{major},{minor},{patch + 1}}}"
```

或使用 `lambda m: ...` / `re.escape` 避免量词解析。凡是 repl 中含 `{`/`\`
的都要警惕。

## 4. `luajit -e` 管道模式下 stdout 缓冲不可信（2026-08-04，artifact 验证）

**场景**：`luajit -e '...f(); print("entries:", n)'` 验证 artifact 加载。
**事故**：stdout 重定向到管道时全缓冲，print 顺序错乱（`entries: 0` 先于
函数内的 print 出现），计数结果不可信，误以为加载失败。
**正确做法**：验证逻辑写成**独立脚本文件**（`/tmp/xxx.lua`），用 `io.write`
输出，再 `luajit 脚本.lua <参数>` 执行：

```lua
local f, err = loadfile(arg[1])
assert(f, err)
f()
io.write("entries: ", n, "\n")
```

## 5. JSON 编辑前先检查原文件缩进（2026-08-04，manifest）

**场景**：编辑 `i18n/versions/tome-1.7.6.json`（原文件 2 空格缩进）。
**事故**：`json.dump(..., indent=1)` 重写后整文件 283+283 行噪音 diff。
**正确做法**：先看原文件缩进与尾部格式，dump 时保持一致：

```bash
head -5 <file>; tail -3 <file>
```

manifest 用 `indent=2`；写完后再 `git diff --stat` 确认无噪音（理想为仅
目标行变化）。

## 6. 提交纪律：测试失败不得提交（2026-08-04，publish 初版）

**场景**：`test_publish_bump_version_regex` 失败（教训 3 的连带），
但 `git commit` 已先行执行。
**正确做法**：任何改动先跑相关测试（`python3 -m unittest -q
tests/i18n/test_toolchain.py`），**全绿后再提交**；失败则修复后补提交。

## 7. 脚本细节：dict 解包 tuple key（2026-08-04，差异分析）

**场景**：`for s, t in null_map` 遍历 `{(source, tag): target}` 字典。
**事故**：`s, t` 解包的是 key 元组，`t` 拿到的是 `tag` 而不是 `target`，
打印结果误导排查方向。
**正确做法**：`for (src, tag), target in d.items()`；不确定键结构时先打印
`next(iter(d))` 确认。

## 8. 门禁的即时价值（2026-08-04）

跨组件同键多译扫描（`scan_runtime_collisions.py`）首次纳入门禁即捕获
6 条漂移（三轮 Pi 复审修改造成的组件间不一致）。结论：**每次译文批量
修改后每批必须先按 `docs/agent-workflow.md` 跑五步快速门禁；翻译、术语或工具行为变更收束时再跑完整门禁（`tools/ci-gates.sh`）**。

## 9. 匿名 provider cwd 不能假定 `/private/tmp` 存在（2026-08-11）

**场景**：translation review v2 为避免向 provider 暴露项目路径，将 Pi cwd 固定为
`/private/tmp`。该目录在 macOS 存在，但 Linux 宿主通常只有 `/tmp`，导致 runner 在
发起请求前即以 `FileNotFoundError` 失败，三条 toolchain 测试阻断。

**正确做法**：匿名系统临时根按固定顺序选择：存在 `/private/tmp` 时使用它，否则使用
`/tmp`；把实际选择写入报告，并连同 system prompt 进入 evaluator/cache identity。
不得回落到仓库目录、用户目录或由项目路径派生的临时目录。测试必须按实际选择断言，
不能硬编码单一操作系统路径。

## 10. Node runtime identity 不能只识别 Homebrew receipt（2026-08-11）

**场景**：Facts-study preregistration 通过向上查找 `INSTALL_RECEIPT.json` 冻结 Node
运行时树。Homebrew Node 提供该文件，Debian/Ubuntu 的 `/usr/bin/node` 不提供，导致
所有构建 preregistration 的离线测试在 Linux 上失败。

**正确做法**：优先保留 Homebrew package-tree identity；缺少 receipt 的 Linux 宿主用
`ldd` 解析 Node 的精确动态库闭包，对 Node 可执行文件和每个解析出的绝对库文件逐个
流式计算摘要。不得遍历整个 `/usr/bin` 或 `/usr`，也不得只记录版本字符串；无法解析
闭包或出现 `not found` 时继续失败关闭。

## 11. 传输状态面陈旧字段导致的误判挂起（2026-08-24，p2-tome-texts-b25）

**场景**：b25 的 EXECUTOR 派发后，宿主轮询显示 `status: running`、activeTurn 非空，而
`updatedAt` 已约 34 分钟未变，output token 仅数百。

**事故**：宿主据此断定 child「卡在一条引号不闭合的 shell 命令上」，并据该结论准备
`cancel_agent`。该诊断被用户拒绝后，child 随即自行结束——它其实在派发后约 2 分钟就已结束，
只回了一段「前置检查已完成，接下来再开始改」的进度说明，没有做任何修改。`status: running`
与陈旧的 `updatedAt` 是过期状态，`attentionReason: "finished"` 才是事实。宿主又把 child 的
工具轨迹倒推去支持已经形成的假设，把一条正常的 `rg` 命令读成了挂起原因。

**根因**：只读单一 `status` 字段就下结论；未读 `attentionReason`／activeTurn；未检查工作树。
一个什么都没做的 EXECUTOR 会留下空 `git diff`——这条最便宜的证据可以直接证伪「做到一半卡住」，
却被跳过。

**正确做法**：宣布挂起、调用 stop／cancel 或写下任何故障归因之前，按顺序取证：

```bash
# 1) 重新查询一次实时状态：读 attentionReason／attentionTimestamp 与 activeTurn
#    activeTurn 为空 = 没有进行中的运行 = 已结束，不是挂起
# 2) 检查工作树
git status --short
git diff --stat
```

字段长时间未更新本身不是挂起证据。EXECUTOR 结束却无工作成果（无 diff、无报告，或只回了
计划／进度说明）时输出无效：先归档，再创建 fresh retry；已结束的 child 即使仍为 idle 且未
归档也不得发 follow-up 续跑。已写入的故障归因被推翻时，必须同一轮更正 STATE 与
`child_dispatches.last_error` 并向用户说明。

规则已写入 [`AGENTS.md`](../AGENTS.md)、
[`docs/paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md) 第七节、
[`.ai/roles/orchestrator.md`](../.ai/roles/orchestrator.md) 与
[`docs/agent-workflow.md`](agent-workflow.md)。
