# ToME4 汉化工具

当前工具以 `tome4-chinese-translation` 为唯一译文源。manifest 固定的 engine、addon
和 extractor Git 对象用于公开源码与官方 locale；三个 GPL v3 官方 DLC 虽可公开读取，
manifest 只固定其提取器 commit 和快照基线，不固定 DLC 源码仓库、源码 commit 或源码版本。
提取流程仍统一通过受审计的 Lua 代理和固定快照基线。默认命令不会提取 DLC，所有报告写入
`.artifacts/i18n/`。

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

`tools/i18n review` 与 `tools/review_diff.py` 只生成离线 bundle／index／diff
artifact，不调用 provider、不构成审核结论；译文审核由 Paseo REVIEWER 的
`translation_contextual_v1` 路由承担（见
`docs/paseo-translation-context-review-v1-contract.md`），代码审核由 Paseo 常规
REVIEWER 承担；实际 role、purpose 和运行时 profile 由当前 Paseo 编排决定，外发内容与授权边界见
`AGENTS.md`「外发边界」。旧项目 Skill
`$tome4-pi-review` 已归档（见 `archive/`），不再作为审核入口；`tools/pi-review`
是当前仓库 tombstone，任何调用都非零退出并输出退役指引，不读取 bundle、不启动
provider。

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
  `AGENTS.md`「外发边界」取得授权，它不像 tombstone 那样不启动 provider。它只消费
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
