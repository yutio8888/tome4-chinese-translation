# ToME4 汉化工具

当前工具以 `tome4-chinese-translation` 为唯一译文源。版本与 DLC 基线边界见[运行时配置](#运行时配置)，
公开源码许可见下方许可证说明；提取统一通过受审计的 Lua 代理和固定快照基线。
默认命令不会提取 DLC，所有报告写入 `.artifacts/i18n/`。

最新已推送 addon 版本、条目数和待发布事项见
[`docs/release-plan.md`](../docs/release-plan.md)。manifest 中的 `repositories.addon.commit`
是工具链可复现输入 pin，不等同于发布仓库的最新 HEAD；不能只因发布版本前进就改写该 pin。

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
tools/i18n claims check --registry evidence/quality/semantic-claim-regressions-v1.json --strict
tools/i18n review --scope code
tools/i18n review --scope translations
tools/i18n review --scope code --scope translations
tools/i18n production --help
```

## 运行时配置

`i18n/versions/tome-1.7.6.json` 是版本、组件映射、engine／addon／extractor commit、LuaJIT 语义和基线的权威 manifest；其中 DLC 基线仅记录提取快照哈希与条目数，不固定 DLC 源码仓库、源码 commit 或 1.7.4 源码版本。运行时由 `TOME_LUAJIT` 指向 manifest 兼容的 LuaJIT 可执行文件，项目 LuaRocks 树由 `TOME_LUAROCKS_ROOT` 指定；不要把本机绝对路径写入命令、报告或文档。

Tome4 与旧版汉化工具按 Lua 5.1 语义运行，一律使用 manifest 指定的 LuaJIT；不要退回系统 `lua`、`lua5.4` 或 `lua5.5`。工具会在同一次 LuaJIT 子进程调用中配置 `LUA_PATH` 和 `LUA_CPATH`。直接运行 Lua 脚本、单行命令或依赖检查时也必须在同一条命令中配置，不要拆开环境设置与 LuaJIT 调用：

```bash
: "${TOME_LUAJIT:?set TOME_LUAJIT to the manifest-compatible LuaJIT}"
: "${TOME_LUAROCKS_ROOT:?set TOME_LUAROCKS_ROOT to the project LuaRocks tree}"
env \
  LUA_PATH="$TOME_LUAROCKS_ROOT/share/lua/5.1/?.lua;$TOME_LUAROCKS_ROOT/share/lua/5.1/?/init.lua;;" \
  LUA_CPATH="$TOME_LUAROCKS_ROOT/lib/lua/5.1/?.so;;" \
  "$TOME_LUAJIT" <script-and-arguments>
```

首次使用或运行失败时，检查可执行文件和模块。项目依赖包括 `lfs`、`lpeg` 和 `rex_pcre`；历史 `luafish` 只使用已验证的 LPeg 0.10.2：

```bash
command -v "$TOME_LUAJIT"
env \
  LUA_PATH="$TOME_LUAROCKS_ROOT/share/lua/5.1/?.lua;$TOME_LUAROCKS_ROOT/share/lua/5.1/?/init.lua;;" \
  LUA_CPATH="$TOME_LUAROCKS_ROOT/lib/lua/5.1/?.so;;" \
  "$TOME_LUAJIT" -e 'require("lfs"); require("lpeg"); require("rex_pcre"); print(_VERSION, jit.version)'
```

需要安装或重装依赖时，沿用 manifest 的 LuaJIT 版本与项目树，并遵循当前任务的权限确认要求：

```bash
luarocks --lua-version=5.1 --lua-dir="$(cd "$(dirname "$TOME_LUAJIT")/.." && pwd)" \
  --tree="$TOME_LUAROCKS_ROOT" install luafilesystem
luarocks --lua-version=5.1 --lua-dir="$(cd "$(dirname "$TOME_LUAJIT")/.." && pwd)" \
  --tree="$TOME_LUAROCKS_ROOT" install --force lpeg 0.10.2-1
luarocks --lua-version=5.1 --lua-dir="$(cd "$(dirname "$TOME_LUAJIT")/.." && pwd)" \
  --tree="$TOME_LUAROCKS_ROOT" install lrexlib-pcre
```

审核命令的离线 artifact 和退役入口行为见下方 `review`／`tools/pi-review` 条目；
活跃 role、purpose 与外发授权统一见[编排契约](../docs/paseo-orchestration-v2-contract.md#十一外发与兼容)。

- `doctor` 检查 LuaJIT 5.1、项目 LuaRocks 树、LPeg 0.10.2、manifest 固定的 engine／addon／extractor commit
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

许可证说明（2026-08-08）：ToME4 与三个官方 DLC 均以 **GPL v3（or later）**
发布（依据：`t-engine4/COPYING` 全文、各 DLC `init.lua` 头部声明）。本规范/工具链
仓库的授权说明与 GPL v3 全文分别位于根目录 `LICENSE`、`COPYING`。GPL v3 §2
允许不分发的任何使用，包括 AI 读取、分析与提取；仅分发衍生作品（含译文）时
须遵守 §5（保留版权声明、GPL v3 兼容许可、提供对应源码；发布仓库 tome-chn-mod 按
ToME4 addon 惯例在 `init.lua` 头部声明 GPL v3 并注明上游版权与衍生作品
性质，提交 `d61c186`）。历史核验记录（非 manifest 权威，2026-08-08）：记录中的
三份受保护 baseline 仅与公开的 1.7.4 源码核验；两处公开源序列验证一致，cults/orcs
仅非 t() 内容差异。该记录不表示 manifest 固定了 DLC 源码仓库、源码 commit 或
1.7.4 源码版本。受保护提取机制保留为可复现基线
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
- `claims check` 对机制 claim、anchors-only reviewer briefing 与 runtime composition
  registry 执行无外部依赖的 exact-schema 校验。默认 registry 锚定 repository root 下的
  `evidence/quality/semantic-claim-regressions-v1.json`，因此从仓库外 CWD 调用绝对 `tools/i18n` 仍可用；
  规范／CI 调用使用显式 `--registry` 与 `--strict`。成功退出 0
  并报告三类记录及 pending 数，读取／JSON／schema／路径／anchor／placeholder binding／组成算术／
  explicitness 关系／args_order raw-token permutation／variant 多层 anchor／Lua 5.1 format token
  边界／sample conversion 类型／完整 variant 覆盖／完整句重渲染或 assertion 失败时以
  validation exit code 5 失败。pending 是诚实记录未固定来源，本身不是 schema 错误；无效 UTF-8
  也按读取 validation error 报错并退出 5，不输出 traceback。runtime composition v1 的
  `sample_value` 必须是 non-empty string；`%s` 只接受 raw bare token，`%q` 样例不得含除 LF 外的
  C0 或 DEL；数值机制证据留在 numeric claim／decomposition，数值 runtime
  composition 需由未来的版本化 renderer 支持。详细字段、保守默认与复用边界见
  [`docs/semantic-claim-runtime-composition-v1.md`](../docs/semantic-claim-runtime-composition-v1.md)。
- `production` 实现 WP1 production-review shadow calibration：按 manifest 的 11 个 translation 组件和 `LocaleDocument.translations` emission order 枚举 locator，生成只读 catalog、固定 shadow policy、一次性 `None→queued` journal、replay、`batch-draft --shadow` 和 reconciliation。所有 marker 固定为非权威／不可派发／不可提升；真实 surface 与正式 ledger catalog consumer 会拒绝 shadow；没有 append、ownership、formal epoch、provider dispatch 或译文写入。受跟踪内容寻址 artifact 位于 `evidence/production-review/`，schema/policy 位于 `i18n/quality/production-review/`，drift report 只写 `.artifacts/i18n/production-review/`；`locator check` 仅执行 frozen self-contained structural check（`live_bound=false`），旧 snapshot 可独立重验。WP1 publication 的 per-family 全局锁覆盖当前 family 的总占用预检、rename 与 fsync，并报告实际 bytes；WP1 locator/catalog 各只允许一个 baseline。默认正式 ledger CLI 会按工具仓库 ROOT 与所选 `--root` 的 forbidden set 并集拒绝 tracked shadow provenance，generic library replay 仍只是 legacy 状态机校验；`--catalog-manifest` 在 WP2 exact authoritative validator 实现前拒绝所有 catalog，未来 exact formal validator 也必须同时应用同一 forbidden set。WP2 publication 当前完全不可用：必须先实现新的单锁 generation transaction，在同一锁内精确验证并完成 WP1 retirement、父目录 fsync、各 family 与 128 MiB 总预算预检、五 family 全部 publication 或恢复；不得以布尔值声称 retirement，也不得复用 WP1 per-family publisher 伪装该事务。详见 [`docs/translation-production-catalog-queue-v1-plan.md`](../docs/translation-production-catalog-queue-v1-plan.md)。
- `review` 只生成离线审核 bundle／index／diff artifact（全部写入
  `.artifacts/i18n/`），不调用 provider、不构成审核结论。必须用 `--scope code`
  或 `--scope translations` 显式选择范围，重复参数才会同时选择两者。翻译使用
  `tome4-translation-review-bundle-v2`：以条目硬上限 10 和 24000 个 item canonical
  JSON 字符双重分包，携带稳定 `unit_id`/`revision_id`，但不注入 terminology 或
  Facts；index 分别记录 `item_character_count`、`item_character_budget`、宿主
  `artifact_bytes` 与实际 `payload_bytes`。完全相同的重复 canonical occurrence
  共享同一 `revision_id`，选择保留首个 occurrence 并按 revision 去重。代码 diff
  使用 legacy `tome4-review-v1`；混合 index 逐 bundle 记录实际 contract/channel。
  实际审核由当前 Paseo 编排中的对应 REVIEWER 在独立契约下承担，见
  `docs/paseo-translation-context-review-v1-contract.md`。
- `tools/pi-review` 已退役，是当前仓库 tombstone：任何调用都在产生任何副作用之前
  非零退出并输出退役指引，不读取 bundle、不启动 provider。入口退役后保留的
  `run_pi_review`／`run_tmux_review`／`run_tmux_file_review` 是残留 driver，已无
  活跃调用者，不构成审核入口；真正被质量评估器、Facts study 与兼容消费者复用的是
  低层原语（如 `pi_file_review._run_file_review_process`、
  `pi_review._canonical_sha256`、`pi_review._stage_validated_json`），详见
  `archive/README.md`。
- `.artifacts/i18n/cache/review-inventory/` 是当前宿主 producer 生成的可信派生缓存，
  自哈希、header 和 slice proof 能阻断缺失、陈旧与随机损坏，但不是抵御同一工作区内
  协调伪造 bundle+cache 的密码学证明。来自外部或不可信工作区的 bundle 不应直接使用，
  应在当前 checkout 用 `tools/i18n review` / `tools/review_diff.py` 重新生成。
- `tools/pi-remediate` 是 dormant 兼容消费者，不是活跃 dispatch。dormant 仅指不参与
  活跃审核 dispatch：实际调用它仍会启动外部 Pi provider 子进程，外发必须按
  `docs/paseo-orchestration-v2-contract.md`「外发与兼容」（§十一）取得授权，它不像 tombstone 那样不启动 provider。它只消费
  主代理已经确认并定级的既有 legacy assessment/finding artifact，生成修复 proposal；
  legacy v1 schema 本身没有可机器验证的 adjudication 字段，因此确认与定级是
  调用前的主代理流程门槛，不是工具能从 v1 JSON 独立证明的事实。translation v2
  assessment 是候选观察，不得直接进入 remediation。结构校验成功不等于事实确认。
- 旧的 code/legacy v1 文件审核入口 `tools/pi-review-files` 已归档到
  `archive/tools/`；code 审核统一由 Paseo 常规 REVIEWER 承担。translation v2
  的源码核验必须绑定既有
  observation，仅返回 `supported/refuted/insufficient`，不得开放式新增 finding；在该
  claim-bound runner 实现前，主代理直接按固定源码版本核验。
- `tools/pi-subagent` 把不超过 50 条的已校验 workset 和 proposal 模板注入一个
  无工具、无会话、无项目上下文的翻译进程。原始输出先保存在 artifact，再自动通过
  `proposal --strict`；它没有读取仓库、运行 shell 或修改 Lua 的能力。
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

使用 `tools/i18n` 命令时不需要也不应手动设置 `LUA_PATH` 或 `LUA_CPATH`；工具会在
同一次 LuaJIT 子进程调用中设置它们。

Pi 默认从现有环境、用户 Pi auth 或 macOS Keychain 的
`codex-pi-opencode-go` 项解析凭据。凭据只进入 Pi 子进程环境，不写入命令行、报告
或 proposal。模型输出即使通过机械校验，仍只是待人工/独立语言审校的提案。

## 提取成功条件

提取器来自版本清单固定的历史 Git commit，在临时副本中于 `luafish/parser.lua` 的
`local lpeg = require 'lpeg'` 后加入以下兼容设置，并保留同一源码文件中的重复出现
位置：

```lua
lpeg.setmaxstack(100000)
```

不要修改游戏源码工作区。未提高栈上限时，大型 Lua 文件会出现
`too many pending calls/choices`，而提取器仍可能以退出码 0 结束并写出不完整结果。
一次提取必须同时满足：

1. LuaJIT 进程退出码为零；
2. 输出 `i18n_list.lua` 存在且至少包含一个 `tDef(...)`；
3. 日志不包含 `In file `、`too many pending calls/choices` 或已知的 LPeg 空循环错误。

源码中的空 `_t`、界面占位符或 `game.log("")` 也可能被历史提取器记录为空
`tDef`。原始 `snapshot.jsonl` 保留这些记录，以维持已冻结 DLC 基线的哈希与数量；
`merge` 等语义消费者会忽略它们。手工定义中的空 source 仍然属于错误。

公开组件会生成原始 `i18n_list.lua`、规范化 `snapshot.jsonl`、完整日志和元数据。
以受保护映射处理的 DLC 只保留已提取文本：Lua 代理会把绝对源路径替换为逻辑 mount，Python
调度层丢弃代理的 stdout/stderr，不保存源码或解析日志。任何解析失败、空结果或
路径残留都会令提取失败；不能只以退出码 0 判定成功。

DLC 的 `i18n_list.lua`、`snapshot.jsonl`、merge、workset 和 proposal 虽然不含源码，
仍是派生工作 artifact。它们位于已忽略的 `.artifacts/i18n/`，默认不得提交；翻译
进程只能接收人工选定的 workset；审核流程只经 Paseo 对应 REVIEWER 接收有界翻译
bundle 或去敏后的公开代码 diff。
