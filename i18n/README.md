# ToME4 汉化工具

当前工具以 `tome4-chinese-translation` 为唯一译文源。公开源码和官方 locale
从固定 Git 对象读取；闭源 DLC 只能由受审计的 Lua 代理提取文本。默认命令不会
提取 DLC，所有报告写入 `.artifacts/i18n/`。

## 常用命令

```bash
tools/i18n doctor
tools/i18n extract
tools/i18n extract --component ashes-urhrok
tools/i18n lint
tools/i18n lint --strict
tools/i18n status
tools/i18n build --profile full
tools/i18n build --profile addon
tools/i18n build --profile addon --component tome --require-complete
tools/i18n build --profile addon --require-complete
tools/i18n merge --component tome --snapshot <extract-run>/tome/snapshot.jsonl
tools/i18n workset --merge-report <merge-run>/tome/merge.json --limit 50
tools/pi-subagent --workset <workset.json>
tools/i18n context --component tome --query Dreadfell --limit 20
tools/i18n proposal --workset <workset.json> --proposal <proposal.json> --strict
tools/i18n review --scope code
tools/i18n review --scope translations
tools/i18n review --scope code --scope translations
tools/pi-review --bundle <review-bundle.json>
tools/pi-remediate --bundle <review-bundle.json> --review <review.json>
```

在 Codex 中可直接要求使用 `$tome4-pi-review`。该项目 Skill 会生成有界 bundle、
逐批调用 `tools/pi-review` 并汇总已验证 findings。由于 bundle 会发送给外部 Pi
provider，首次调用前仍需明确确认 provider、model 和数据范围；项目没有开启全局
网络权限。

- `doctor` 检查 LuaJIT 5.1、项目 LuaRocks 树、LPeg 0.10.2、固定 Git commit
  和所有规范译文文件。对于 DLC 它只让 Lua 代理探测清单中预声明的组件，
  不遍历或列出 DLC 目录；包含 DLC 的 engine 工作树也不执行 Git 状态扫描。
- `extract` 默认提取 engine、boot 和 tome。可用 `--component boot` 缩小范围，
  用 `--component ashes-urhrok` 显式提取单个 DLC，或用 `--all` 尝试所有公开与
  受保护映射。受保护组件不可用时会失败关闭，不会自动搜索未知目录名。
- `lint` 通过 LuaJIT 执行 locale 文件，检查参数格式、空译文、运行键冲突、
  控制标记和术语 TSV。普通模式下控制标记差异是警告；`--strict` 会阻断警告。
- `status` 按 `(source, source_tag)` 比较当前规范译文和固定版本官方 locale。
- `build --profile full` 组合 `locale`、`*.copy.lua` 和规范译文，在 artifact
  中生成完整游戏目录结构，并重新加载产物确认语义没有变化。
- `build --profile addon` 生成相对固定官方 locale 的最小覆盖层，并模拟“官方
  locale → 模组 locale”加载结果。官方已有且未改变的译文只计入
  `inherited_entries`，不会写入插件；只有覆盖官方译文或官方没有的新增译文才会
  进入覆盖层。报告同时列出 `override_entries` 和 `new_entries`。
- 对核心插件可显式指定 `--component tome`，此时只检查选中的组件，不把未选择的
  DLC、旧 lore 或 Nullpack 层算作不完整；配合 `--require-complete` 可得到可发布的
  核心最小覆盖插件。未指定组件时仍会检查完整 addon 选择，缺少固定来源的层会
  明确标记 `INCOMPLETE`。

当前 manifest 将发布层明确分开：

- `core-addon` 只包含 `tome`，对应命令为
  `tools/i18n build --profile addon --component tome --require-complete`，当前可作为
  核心发布基线。
- `dlc-addon` 当前只包含 `ashes-urhrok`、`cults`、`orcs`，三者已登记受保护
  提取快照哈希。该层仍为 `baseline-pending`，不能被核心构建隐式继承。
  **基线已验证（2026-08-04）**：`extract` 对三组件的快照 SHA-256 与条目数
  与 manifest `source_baseline` 完全一致（ashes 999 / cults 2444 / orcs 4493 tDef），
  基线可复现。
  **DLC 译文发布（2026-08-04）**：`publish` 将三个 DLC 的专有条目
  （运行时 key 不在官方 tome/engine/boot locale 中）合并进发布仓库
  `data/locales/zh_hans.lua` 的独立 section（ashes 743 / cults 1555 /
  orcs 3126 条，跨组件重复 key 去重；官方已有的 key 留给核心层继承，
  DLC 层不遮蔽主游戏文本）。游戏 locale 加载机制自动读取同一文件，无需
  额外加载挂钩。
- `items-vault` 和 `possessors` 暂时忽略：规范译文文件仍保留并参与 lint，
  但 manifest 不再声明其受保护来源映射，也不把它们列为 addon 候选或发布层组件。
  后续恢复时应同时还原受保护来源映射、addon eligibility 和发布层归属。
- `legacy-lore-addon` 与 `nullpack-addon` 是独立可选外部层，不计入核心 addon
  的完整性判断；归属记录见 manifest `addon_external_requirements`：
  - `nullpackreloaded`：译文快照固定于发布仓库 tome-chn-mod `8dd657d`
    （`data/null_translation.lua`，464 个 `t()` 条目，section `nullpackreloaded`；
    运行时挂钩在 `hooks/load.lua`，覆盖 `/data-nullpackreloaded` 物品与特殊物品）；
    addon 上游源码/版本未固定。
  - `legacy-lore-overlay`：2026-08-04 调查结论——tome-chn-mod 历史与引擎公开源码树
    均无独立 legacy-lore 实体；来源与归属组件仍未固定，恢复前保持 optional。

核心 artifact 独立验证（2026-08-04）：同一输入两次构建 SHA-256 一致
（`aa712264…`，确定性构建）；产物在模拟 addon 运行时环境下经 LuaJIT 加载成功，
共 4,158 个运行时条目。完整门禁一键运行：`tools/ci-gates.sh`。

受保护组件的 baseline 只记录提取器 commit、规范化快照 SHA-256 和条目数量，不
保存 DLC 源码路径、源码片段或原始解析日志。

许可证说明（2026-08-04）：ToME4 与三个官方 DLC 均以 **GPL v3（or later）**
发布（依据：`t-engine4/COPYING` 全文、各 DLC `init.lua` 头部声明）。GPL v3 §2
允许不分发的任何使用，包括 AI 读取、分析与提取；仅分发衍生作品（含译文）时
须遵守 §5（保留版权声明、GPL v3 兼容许可、提供对应源码；发布仓库 tome-chn-mod 按
ToME4 addon 惯例在 `init.lua` 头部声明 GPL v3 并注明上游版权与衍生作品
性质，提交 `d61c186`）。提取来源已切换至
公开正式版 `/Users/yun/projects/tome4-dlcs/`（version 1.7.4；两处副本 t() src
序列验证一致，cults/orcs 仅非 t() 内容差异）。受保护提取机制保留为可复现基线
工具，不再视为闭源限制；快照含 origin 元数据，来源切换后 extract 若报基线
mismatch 属预期，重建基线即可（tdef_count 不变）。
- `merge` 将新快照、可选的旧快照和当前规范译文三方分类，只在 artifact 中生成
  `candidate.lua`、未翻译清单、疑似英文改写建议及废弃/未提取报告。没有
  `--base-snapshot` 时进入 bootstrap 覆盖率模式；疑似英文改写永远不会自动继承译文。
- `workset` 从 merge 报告中选取最多 500 个条目，附加相关术语、manifest/术语表
  摘要和稳定 `workset_id`，并生成一份 proposal 模板，作为 Pi subagent 或人工
  翻译的只读输入。术语只在相同 `source_tag` 和适用 scope 中生效。
- `context` 按 component、section 前缀或查询文本返回有界的现有译文与术语上下文。
- `proposal` 校验 Pi 或人工返回的结构化译文：workset 内容身份、条目覆盖率、原文、
  `source_tag`、Lua 值、printf 参数及首选术语。成功后只生成内容寻址的
  `*.validated.json`；`--allow-partial` 允许分批返回，`--strict` 会阻断警告。
- `review` 生成只读 Pi 审核 bundle；必须用 `--scope code` 或
  `--scope translations` 显式选择范围，重复参数才会同时选择两者。bundle 只写入
  `.artifacts/i18n/`，会去除绝对路径，不包含受保护 DLC 源码或受保护源码路径。
- `tools/pi-review --bundle` 使用独立的 reviewer prompt，在无工具、无会话、无项目
  上下文的 Pi 进程中运行，只生成结构化 findings artifact；宿主会分配稳定的
  `R-NNN` 引用，并在启动 Pi 前复用 provider/model/prompt/bundle 完全一致且已严格
  校验的缓存结果。`--force` 可做一次不改写缓存的 fresh run，`--no-cache` 可完全禁用
  缓存。该入口不会修改 Lua、Python 或其他工作区文件，也不会执行模型建议。
- `tools/pi-remediate --bundle --review` 把已校验的 findings 和原 bundle 交给独立的
  remediation prompt，只生成按 `finding_id`/`item_id` 绑定的修订建议。主代理必须
  复核、应用并重新审核；Pi 没有文件写入权限。
- `tools/pi-subagent` 把不超过 50 条的已校验 workset 和 proposal 模板注入一个
  无工具、无会话、无项目上下文的 Pi 翻译进程。Pi 的原始输出先保存在 artifact，
  再自动通过 `proposal --strict`；它没有读取仓库、运行 shell 或修改 Lua 的能力。
  若模型只返回 `proposals` 数组，工具只会补入已冻结的 `schema_version` 和
  `workset_id` 外壳，不会修补或猜测任何译文内容。
  provider、model 和 thinking 可分别用 `TOME_PI_PROVIDER`、`TOME_PI_MODEL`、
  `TOME_PI_THINKING` 覆盖，实际选项以 `tools/pi-subagent --help` 为准。

`merge` 的候选文件和校验后的 proposal 都不会覆盖根目录 Lua。只有报告中的
`safe_to_apply` 为真时，候选才具备进一步审核的前提；当前工具仍未提供原地
apply 命令。

proposal 顶层格式如下；每个条目必须保留模板中的 `entry_id`、`source` 和
`source_tag`：

```json
{
  "schema_version": 1,
  "workset_id": "<workset_id>",
  "proposals": [
    {
      "entry_id": "<entry_id>",
      "source": "%s has %d",
      "source_tag": "tformat",
      "target": "%d 属于 %s",
      "args_order": [2, 1],
      "special": null,
      "notes": "为中文语序调整参数顺序"
    }
  ]
}
```

所有命令都支持 `--json`。外部仓库默认从当前仓库的同级目录解析，也可以用绝对
路径环境变量覆盖：

```text
TOME_ENGINE_ROOT
TOME_ADDON_ROOT
TOME_DLC_ROOT
TOME_DLC_ASHES_ROOT
TOME_DLC_CULTS_ROOT
TOME_DLC_ORCS_ROOT
TOME_LUAJIT
TOME_LUAROCKS_ROOT
```

`TOME_DLC_ROOT` 默认按词法路径指向 engine 下的 `game/dlcs`；工具自身不会读取或
枚举该目录。若实际组件目录名不在版本清单的候选值中，可用对应的组件环境变量
提供绝对路径。环境变量只作为参数交给 Lua 代理，不能用于普通文件工具。

不需要也不应手动设置 `LUA_PATH` 或 `LUA_CPATH`；工具会在同一次 LuaJIT 子进程
调用中设置它们。

Pi 默认从现有环境、用户 Pi auth 或 macOS Keychain 的
`codex-pi-opencode-go` 项解析凭据。凭据只进入 Pi 子进程环境，不写入命令行、报告
或 proposal。模型输出即使通过机械校验，仍只是待人工/独立语言审校的提案。

## 提取成功条件

提取器来自版本清单固定的历史 Git commit，在临时副本中设置 LPeg 最大栈，并保留
同一源码文件中的重复出现位置。一次提取必须同时满足：

1. LuaJIT 进程退出码为零；
2. 输出存在且至少包含一个 `tDef`；
3. 日志不包含 `In file `、`too many pending calls/choices` 或已知的 LPeg 空循环错误。

公开组件会生成原始 `i18n_list.lua`、规范化 `snapshot.jsonl`、完整日志和元数据。
闭源 DLC 只保留已提取文本：Lua 代理会把绝对源路径替换为逻辑 mount，Python
调度层丢弃代理的 stdout/stderr，不保存源码或解析日志。任何解析失败、空结果或
路径残留都会令提取失败。

闭源 DLC 的 `i18n_list.lua`、`snapshot.jsonl`、merge、workset 和 proposal 虽然不含
源码，仍可能包含保密游戏文本。它们位于已忽略的 `.artifacts/i18n/`，不得提交或
公开；翻译 Pi 只能接收人工选定的 workset，审核 Pi 只能接收 `review` 生成的有界
翻译 bundle 或去敏后的公开代码 diff。
