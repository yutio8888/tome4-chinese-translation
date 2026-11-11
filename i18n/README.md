# ToME4 汉化工具

当前工具以 `tome4-chinese-translation` 为唯一译文源。版本与 DLC 基线边界见[运行时配置](#运行时配置)，
公开源码许可见下方许可证说明；提取统一通过受审计的 Lua 代理和固定快照基线。
默认命令不会提取 DLC，可重生成的工具报告写入 `.artifacts/i18n/`；人工裁决与不可重生成核验锚点
按所属契约保存在受跟踪的 `evidence/`。本文件按命令查询，不是每次修改前的必读清单；检查选择见
[工作流验证矩阵](../docs/agent-workflow.md#验证矩阵)。

最新已推送 addon 版本：**0.3.12**（2026-11-11，发布仓库 tome4-chn-mod `495aa44`，由本仓库
`581914a01` 经 `tools/i18n publish --apply --bump` 构建：13,802 条＝核心 8,152＋引擎 189＋DLC 5,461，sha256 `4e1819f9…`；
插件代码在 0.3.11 基础上新增 `a262ee4`：[leave]、捕熊陷阱 pinned、otber、parasitic、Embers 压力作战服说明、物品增伤行 living（`living##item_property`）。
GitHub Release [`v0.3.12`](https://github.com/yutio8888/tome4-chn-mod/releases/tag/v0.3.12) 附带 `tome-chn-mod.teaa`（tag 指向 `495aa44`，包 sha256 `22706f10…`），已回下载核对完整哈希。
发布凭据见 [`addon-0.3.12.json`](../evidence/releases/addon-0.3.12.json)。打包方式与游戏内置 `utils/te4_pack_module.sh`
一致：`git archive` 取干净树后在其中 `zip -r -0`，`init.lua` 位于根目录，文件名为 `for_module-short_name.teaa`（引擎只识别 `tome-` 前缀）。
`publish --bump` 只递增补丁号，次版本号需手动改发布仓库 `init.lua`（该文件为 CRLF 行尾）。

**发布前置与验收分工（2026-11-11 维护者指示起生效，替代此前的本地实机补验要求）**：
- **发布前，本地只负责技术与完整性核对，然后公开发布。** 核对内容：
  - 版本号；
  - 来源提交与候选身份；
  - 适用的构建与门禁/CI；
  - `publish` 运行时校验（0 mismatched/missing）；
  - `smoke_release.py`；
  - 包的结构，以及与发布提交 `git archive` 结果的一致性；
  - 上传后回下载核对哈希。
- **本地自然游玩覆盖和玩家实机验收不是公开发布的前置条件。** 不为补齐旧的验收清单而开本地游戏或派发测试员。
- **实机验收由测试玩家在发布后进行。** 发布说明要写明这一点，并列出尚未在游戏中实际确认的检查点，同时区分正常游玩与调试/控制台结果，不得声称已完整验收。反馈入口是发布仓库的 GitHub Issues；发布说明附简短反馈格式（版本、场景、复现步骤、截图/日志、触发方式）。不主动联系玩家。
- 已有的本地实机记录照实保留在 `evidence/quality/`，作为参考，不作为发布门槛。
早期发布计划见 [`deprecated/docs/release-plan.md`](../deprecated/docs/release-plan.md)（已弃用）。manifest 中的 `repositories.addon.commit`
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

### 来源属性与 doctor 扫描

manifest schema 1 增量支持四项独立属性。字段写在 `repositories.<name>` 与每个组件的
`protected_source` 中；后者及 `protected_source_roots`、doctor JSON 的 `protected_sources`
是保留兼容的 broker 接口名称，不表示其中的官方 DLC 是私有源码。

| 字段 | 语义 | 旧 repository 配置默认 | 旧 broker 配置默认 |
| --- | --- | --- | --- |
| `visibility` | `public` / `protected`，源码公开性 | `public` | `protected` |
| `extraction_mode` | `full-tree` / `lua-extractor-only`，提取访问方式 | `full-tree` | `lua-extractor-only` |
| `source_pinning` | `pinned` / `unpinned`，源码身份是否固定 | `pinned` | `unpinned` |
| `scan_allowlist` | doctor 允许扫描的字面路径数组 | `["."]` | `[]` |

这四项不相互推断，也不按公开性切换提取路由。当前 repository 的 `commit` 仍为必填完整
Git OID，doctor 独立验证其可用性；`source_pinning` 不关闭 commit 验证。broker 映射没有
源码仓库/commit 字段，只支持 `lua-extractor-only`、`unpinned` 和空扫描列表，矛盾配置报错。
公开的 ashes-urhrok、cults、orcs 均显式为 `public` + `lua-extractor-only` + `unpinned` + `[]`；
父 engine 的 commit 和 DLC 提取快照哈希都不是 DLC 源码 pin。doctor 为每个 DLC（包括不可用
输入）输出 `source-unpinned` 警告，指出源码仓库/commit 未知、提取快照不等于源码固定。

repository 扫描路径相对仓库根，broker 路径语义相对所选组件源码根，但当前不支持 broker
工作树扫描，必须为空。`[]` 明确表示不运行 `git status`（`clean=null`、`worktree_checked=false`）。
唯一根哨兵 `.` 必须单独出现，表示显式全仓库扫描；其他路径必须为规范 POSIX 相对路径，
拒绝绝对路径、盘符、父级/点段、空段、尾斜线、反斜线、NUL 和重复项。通配符、方括号及
冒号仍为文件名字符，传给 Git 时使用 `:(top,literal)`，不能扩大扫描范围。

当前 engine 只扫描六个公开组件挂载目录和 `i18n_tools`，不扫描 `game/dlcs` 或其他兄弟目录。
完整列表以 manifest 为准，新增组件时应一并复核扫描列表。扫描检查当前工作树；提取器目录
可以只存在于固定 extractor commit，提取仍读取该 Git 对象。addon 显式使用 `["."]`。
普通 `GitRepository.validate()` 调用未传 allowlist 时仍检查整个工作树；`check_worktree=False`
仍关闭检查。脏工作树和缺失的可选仓库保持警告/退出 0，实际 Git status 失败仍为错误。
doctor 的文本与 JSON 均展示四项属性，包括缺失的可选仓库与不可用的 DLC。

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
  不遍历或列出 DLC 目录；Git 状态按 repository 的 `scan_allowlist` 进行字面路径扫描，
  engine 不扫描 `game/dlcs` 或整棵工作树。
- `extract` 默认提取 engine、boot 和 tome。可用 `--component boot` 缩小范围，
  用 `--component ashes-urhrok` 显式提取单个 DLC，或用 `--all` 尝试所有公开与
  受保护映射。受保护组件不可用时会失败关闭，不会自动搜索未知目录名。
- `lint` 通过 LuaJIT 执行 locale 文件，检查参数格式、空译文、运行键冲突、
  控制标记和术语 TSV。普通模式下控制标记差异是警告；`--strict` 会阻断警告。
  技能说明另有 `talent-placeholder-spacing`（错误）：`*/talents/*` 段、`source_tag` 为
  `tformat` 的译文里，数值占位符（`%d`、`%0.2f%%` 等，不含 `%s`）在升级预览中所在的
  片段若连带汉字即报错，并给出应插 ASCII 空格的位置。依据是升级预览按
  `tokenize(" ()[],")` 切分后逐段对比（tome `class/Actor.lua:6851`、engine
  `utils.lua:1969`），全角标点不算分隔；规则细节见审核操作指南 §6.4。
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
  首选术语按词边界匹配，散文里的普通词（材质 stone、短语 by the name of 的 name）
  可能只是拼写相同；宿主核实后把 (entry_id, 术语) 登记进 `i18n/term-sense-exemptions.json`，
  该对不再报 preferred-term-missing，报告的 `term_sense_exemptions` 列出实际生效的登记。
  英文原词是常见词的标签术语（stone、Life、Name、Exhaustion、Air、unknown）登记在
  `i18n/term-match-scope.json` 的 `exact_label_only`：只有条目源文去首尾空白、忽略大小写后
  恰好等于原词时才检查（2026-11-01 用户决定），名称与散文中的同形词不再逐条登记豁免。
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
  [`docs/semantic-claim-runtime-composition-v1.md`](../deprecated/docs/semantic-claim-runtime-composition-v1.md)。
- `production authoritative-catalog/queue/batch/migration/repair` 为已实施的正式 WP2-Lite
  入口；受跟踪 catalog、迁移与批次证据位于 `evidence/production-review-v2-lite/`。
  SQLite 与活动 checkpoint 位于 `.artifacts/i18n/production-review-v2-lite/`，可从 Git
  重建。无活动批次时以 `production queue rebuild` 同步当前提交，再执行 `queue check`；
  活动批次必须先按 `batch show` 和恢复契约处理，不能直接删 checkpoint。
  可选同 commit 投影缓存以 `I18N_PROJECTION_CACHE=on` 显式启用（默认关闭），写入
  `.artifacts/i18n/projection-cache-v1/`，可随时删除；只有普通 batch 步骤与 `repair preflight`
  的历史基线读取会命中，`queue`、`finalize`、`recover`、`abandon` 与 migration 仍完整重放。
  `I18N_PROJECTION_CACHE_TRACE=1` 在 stderr 逐次打印命中／未命中原因。开启缓存的 shell
  可直接跑完整批次链与门禁，不需要先 unset：门禁子进程照常继承环境（回执绑定不变），
  投影相关测试 fixture 在建库前自行固定默认关闭并在用例结束后恢复，缓存测试再显式开启。
  `tools/orchestration/profile_projection.py` 对一次 cache-off 完整投影做函数级剖析（只读，
  计时含 cProfile 开销，不能当基准）；加 `--no-profile` 则无剖析计时同一次调用，并列出实际加载的
  实现文件哈希。单次投影内，已在前一个 catalog 完整校验通过的相同 entry 行只重查 manifest
  相关字段，跨行与文件级检查照常每次执行。布局与失效条件见
  [WP2-Lite 方案 §2.2](../docs/translation-production-review-v2-lite-plan.md#22-唯一运行时数据)。
  `queue status --json` 分开报告当前表层／深审覆盖、待修复和历史失效，不把表层通过
  当作深审。当前操作入口见[审核交接](../deprecated/docs/production-review-handoff-2026-09-05.md)，
  正式设计见[WP2-Lite 方案](../docs/translation-production-review-v2-lite-plan.md)。
  旧 `locator/catalog/shadow-policy/shadow-journal/replay/batch-draft/reconciliation`
  子命令保留用于 WP1 shadow 校准及历史校验；shadow marker 仍非权威、不可派发或提升，
  不能作为正式身份父节点。WP1 历史设计中“WP2 publication 不可用”描述的是当时尚未
  实现的五 family 方案，不能用于判断现已实施的独立 WP2-Lite writer。
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
- full-review 历史前驱检查缓存默认关闭；仅 `I18N_FULL_REVIEW_CACHE=on` 开启，
  `I18N_FULL_REVIEW_CACHE_TRACE=1` 将命中、未命中、发布或跳过原因写到 stderr。
  `.artifacts/i18n/full-review-cache-v1/` 是可删除的派生结果，最多保留最近 8 个键，
  总量上限 4 GiB（导出与合并的条目键不同、各约 300 MB，须能同时保留）。命中仍重新散列文件、列目录和核对路径探测；实现、manifest、
  前驱 seal 或 `_outputs_only` 改变即失效。只缓存成功的历史递归结果，当前轮的
  源码、preflight、迁移及 seal 检查照常执行；历史计算触及 Git／FixedReader 时不发布。
  关闭开关可独立完整重放，不读写或创建缓存目录。缓存不提供生产审核或门禁 credit。
- 修改 `tools/` 下验证代码后，以及每次 release candidate 前，必须运行独立完整重放：
  `I18N_FULL_REVIEW_CACHE=off python3 -B tools/full_review.py check --directory <round>`。
- `I18N_FULL_REVIEW_TIMING=1` 将分段计时与调用次数写到 stderr，默认关闭。
  `exclusive_seconds` 互斥，可相加；`outer_seconds` 包含子分段、同名递归只记最外层，
  不可跨名称相加。历史 outer 时间可与总墙钟对照，另列 inventory、import、解析、
  读取、覆盖继承／汇总和 cache key／load／serialization／publish。
  单次 check 还复用精确相同字节的 JSON 与结果解析，最多保留 4096 项、64 MiB 原始
  字节键（解析对象另占内存）；inventory 沿用原有有界快照。文件每次仍重新读取并检查
  路径，失败解析不缓存；退出释放缓存，后续调用重新校验。
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
  `archive/tools/`；委托 code 审核由 Paseo 常规 REVIEWER 承担，主代理可直接进行范围内检查。
  历史 translation v2 的 claim-bound 核验设计以既有 observation 为输入，只返回
  `supported/refuted/insufficient`，不承担开放式发现；该设计不限制主代理主动登记具体疑点后
  按固定源码核验。归档 Skill 不构成当前路由，现行 REVIEWER 只读其冻结输入契约允许的资料。
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

### 全量轮次入口（M1，离线）

`python3 -B tools/full_review.py --help` 提供 `inventory / successor / export / task-gates / import / check /
assemble / install / restore`。它不调用 provider、不创建 child、不写旧 catalog/queue/surface
状态或 `.ai/`。ORCHESTRATOR 负责 schema 5 的 v2 `review_only`、单一 `REVIEW/full`
任务、生命周期、独立复审和正式 evidence 提交。实现与验证边界见
[M1 报告](../evidence/full-review/release-20261013/m1/REPORT.md)；本轮条目 A/B 尚为 0。

恢复入口先跑 `check --directory evidence/full-review/<round>`：重算当前 occurrence 的
rules-v2 身份与额外 special guard，重验冻结 input/workset/SCOPE、实际源码文件哈希、strict raw、
任务自身 DONE_VERIFIED 和已归档 producer。task SPEC 必须有且仅有一行
`full_review_binding=<JSON>`，绑定 export ref 中的
`round_id, export_id, freeze_sha256, input_sha256`；task SCOPE 须为宿主冻结的确切字节。
相同 candidate 的历史任务没有本轮 SPEC 绑定也拒收。结果只通过验证时不计有效覆盖。
相同字节导入幂等；冲突 raw、部分/乱序 verdict、跨轮、旧 revision、未知模型和未归档输出拒收。
无效终态 child 由宿主归档后 fresh retry，不能续跑。

```bash
# 重用 M0 已验证快照；不重跑提取。实际新轮由 ORCHESTRATOR 生成。
python3 -B tools/full_review.py inventory --round-id <round> \
  --directory evidence/full-review/<round> \
  --source-provenance evidence/full-review/release-20261013/m0/SOURCE-PROVENANCE.json \
  --snapshot-report .ai/task/full-review-20261013-m0-bootstrap/validation/extract-fixed-core.json \
  --snapshot-report .ai/task/full-review-20261013-m0-bootstrap/validation/extract-ashes-corrected.json \
  --snapshot-report .ai/task/full-review-20261013-m0-bootstrap/validation/extract-cults-corrected.json \
  --snapshot-report .ai/task/full-review-20261013-m0-bootstrap/validation/extract-orcs-corrected.json
python3 -B tools/full_review.py export --directory evidence/full-review/<round> \
  --selection <ordered-unit-ids.json> --source-workset <neutral-workset.json> \
  --scope <host-SCOPE.json> --export-id <fresh-export> --lane A \
  --task-id <fresh-task> --dispatch-id <fresh-dispatch> \
  --workspace-id <workspace> --parent-agent-id <orchestrator>
python3 -B tools/full_review.py import --directory evidence/full-review/<round> \
  --export-id <fresh-export> --raw <strict-result.json> --binding <producer-binding.json>
python3 -B tools/full_review.py check --directory evidence/full-review/<round>
python3 -B tools/full_review.py check --directory evidence/full-review/<round> --require-complete
python3 -B tools/full_review.py check --directory evidence/full-review/<round> --require-release-ready
```

`selection` 是 1–80 个按序 unit_id。workset 是 `{round_id, entries}`；entries 按同序保存
`unit_id, context, source_files, b_reasons, b_exemption`。context 必须是中性宿主冻结语境，
数字参数的 quantity kind、方向流和 unknown 由宿主如实披露。source_files 每项含
`component, public_source_path, sha256`，可用 `line_start / line_end` 指定最多 200 行的片段
（默认前 100 行）。固定来源读 manifest commit 的 Git blob；DLC 另含绝对 `inner_root`，
工具只剥离 logical mount 一次，再读 relative tail，不把 mount 重复接到内层 root。
绝对路径只作为冻结 envelope 的取证位置，受跟踪说明不写本机路径。每个实际来源保留独立
pin/unpinned 声明和文件哈希，提取 snapshot 不冒充 DLC commit。

B 的适用原因先冻结为 `mechanics / long-text / A-observation`；不适用也要写理由。
A/B 用不同 fresh dispatch 和不同精确运行 model。binding 必含
`round_id, export_id, task_id, dispatch_id, workspace_id, parent_agent_id, model,
input_sha256, raw_sha256, gate_evidence_path, gate_evidence_sha256`，与正式任务和 live runtime observation 核验。
宿主合并裁决写到本轮 `adjudications/<id>.json`，绑定 `unit_id, revision_key, round_id`、
各 lane `raw_sha256`、`source_verified, accepted_successor`、`confirmed, blocking_pending`、
`status=effective-complete`、受跟踪 `evidence=[{path, sha256}]`。
需要 B 时，只有 A 输出不能先计有效完成。严格 A raw 的 `ISSUE` 强制对应 B，宿主省略或设置
`a_observation_requires_b=false` 不能取消；该字段为 true 只能扩大义务。B 中性 workset 必须与已验证 A
的 unit/context/source_files 相同，不能加入 A observation 文本或结论。B policy 可单调扩大，
不改变中性 source/context 身份或旧 A raw；`A-observation` 原因须有当前 revision 的 validated A ISSUE。

最终分母在宿主冻结 `closure.json` 并通过守恒核验之前保持未冻结。closure 绑定
`round_id / inventory_sha256 / candidate_path / candidate_sha256`，完整列出 `occurrences`
与 `supplements`（零遗漏、零重复）、`runtime_keys` 的实际加载层、逐文件哈希和生效 target/
args_order/special；并提供 `retained_layers / dynamic_contexts / relations / successors`
的闭合证据。不能把源码可见缺译、官方继承/过滤/去重、wrapper addon、copy 文本或发行保留层
静默删去。`--require-complete` 只要求语言覆盖和关系守恒；`--require-release-ready` 还要求
Engine 实际加载、game launch 和最终场景证据（场景未测须有明确用户接受证据）。
I18N closure 另冻结 `runtime_semantics`：repository=`engine`、commit=`624a67329fe2ad440c5b344785a9c73fcf22ae63`、
path=`game/engines/default/engine/I18N.lua`、sha256=`a099d023bcf9c91d83592331666aeaa86c901a469eadf59346bcbd279c7ef31d`、
capability=`fixed-i18n-literal-chain-v1`。工具读取固定 Git blob，在 manifest LuaJIT 中执行，
拒绝不同 pin/hash；不使用当前 checkout 替代。所有 I18N runtime key 须列出同一个完整、按实际顺序
冻结的 `layers`（层名唯一），不会只加载含当前 key 的文件；空参数记录可清空影响另一 key 的 tag 桶。
每项显式给 `query={source, tag, method}`，source 与 key[0] 相同，tag 可为 null 或未知 tag；
method 为 `_t / default_tformat / string.tformat`，最后一种 tag 必须是 `tformat`。
query 的 source 与归一化 method/tag 必须绑定 runtime key；null 默认归一化为 `_t`，
`string.tformat` 对应 `tformat`。真实未知 tag fallback 允许，但 key 也须声明该查询 tag，
`effective_registration.source_tag` 保留实际回退注册的 tag。宿主须以调用证据冻结查询，
未解析调用仍由 dynamic_contexts 阻断，不能用注册 tag 代替所有调用。
`effective_registration={layer, ordinal, line, source_tag}` 记录实际供应 target 的 t 注册行（ordinal
在层内从1计），回退也保留该行原 tag；没有注册的 source fallback 须显式给 null 和
`effective_layer=source-fallback`，原文仍进入分母。args_order/special 用固定源码 accessor 查询实际
桶及 fallback，不从该 target 行推断。`string.tformat` 的特殊分支按实际 nil args fallback 查询。
query 可加 `arguments`，此时执行真实格式化并要求 mapping 的 `formatted` 精确匹配。

离线能力只涵盖 zh_hans 的受限 locale/section/t、标量 setFlag 与字体包声明；字体声明不检验 GUI。
`tformat_special` 自定义处理器、其它 locale、未知全局/游戏依赖、tc/t_old、函数元数据等不能证明时
拒绝 closure，不能假造生效结果；language-bytes 的执行证据与字节锚点路径保持原契约。
单次重放所有冻结查询，进程15秒超时；仍须宿主证明完整加载链、调用语境与最终游戏场景。

普通 `check` 始终报告剩余项，不把历史 done 或验证过的 raw 当作本轮有效覆盖。

```bash
python3 -B tools/full_review.py assemble --candidate-id <id> --release-commit <exact-40-hex-commit>
python3 -B tools/full_review.py install \
  --candidate .artifacts/i18n/release-candidate/<id> \
  --target .artifacts/i18n/isolated-game/<id> \
  --target-spec <target-spec.json> --operation-id <fresh-id>
python3 -B tools/full_review.py restore --target .artifacts/i18n/isolated-game/<id> \
  --operation-id <same-id>
```

assemble 从固定发行 commit `git archive` 创建隔离 addon，建立独立 Git 元数据，跑 doctor、
publish dry-run/apply（无 commit）与 Engine full，产出 zip -0、根 init.lua、Engine companion
`engine/data/locales/engine/zh_hans.lua` 和全部文件 hash 清单。candidate 有漂移即拒绝重用。
target-spec 含 `version=tome-1.7.6, layout=bare|teae, engine_path, original_sha256,
addon_original_sha256, guards=[{path,sha256}]`；不存在的旧资源 hash 用 null。
只支持隔离 `game/engines/<bare-name>` 或 `game/engines/te4-1.7.6.teae`，核对固定 loader、
Engine init/version 字节。Engine 资源位于 loader 先挂载到 `/` 的树中，addon 包进入
`game/addons/`。全部备份持久化后才发布 intent，之后替换 Engine/addon；回退核对目标、备份和
当前安装 hash，任一漂移拒收。旧 intent 缺备份仅在资源仍精确等于 before hash 时允许恢复。
中断后若两份资源均已安装，可重复 install 补成功记录；部分安装先 restore，再选 fresh operation。
安装仅检查 game-dir 布局，输出 `game-dir-structure-only / home-unverified`；homepath 会参与
Engine 发现和 VFS 优先级，不能据此声称 actualinit 生效。M0 源码树 binary 退出127是历史观察；
主代理已启动隔离官方1.7.6并验证 prototype Engine 早期locale、CJK和“图像设置”标题及原teae回退。
能力/prototype PASS 不替代 exact 最终 candidate、三DLC玩法或M4实际加载验收。

### M1 task 级完整门禁与终态锚点

`review_only/full` 原 DONE 契约保持；语言内容 task 使用 `change_class=standard`。adapter 在既有
DONE 验证之外追加 task 自己的完整 gate/build 验证，不借 M1 实现门禁或旧队列 receipt。
ORCHESTRATOR 在冻结 export 后创建 task SPEC/SCOPE/BASELINE-MANIFEST：SPEC 的
`full_review_binding` 和 SCOPE 字节须精确匹配 ref；BASELINE-MANIFEST 的 `head` 为此次运行实际 HEAD。
在 task/源码/工具/报告输入稳定后执行（不能在 gate 运行期间改 REPORT）：

```bash
PATH=/usr/local/bin:$PATH TOME_PASEO_WORKSPACE=<workspace> \
  python3 -B tools/full_review.py task-gates \
  --directory evidence/full-review/<round> --export-id <export> \
  > .artifacts/<task>-gate-binding.json
# 若仅归档阶段中断，恢复同一 task-bound 运行；不能传普通无绑定或其它 task 的 results。
python3 -B tools/full_review.py task-gates \
  --directory evidence/full-review/<round> --export-id <export> \
  --results .artifacts/i18n/ci-gates/run.<run>/results.json
```

命令复用现有 runner 与 receipt validator，全检查集含 `12-core-addon-build`，不 skip-build；
返回 `gate_evidence_path / gate_evidence_sha256`，宿主将两字段加入 import binding。
独立保存到本轮 `task-gates/<task>/<export>/results.json` 和逐项 `output.log`，不共享任务 receipt。
绑定精确 task/dispatch/lineage、round/export/freeze、candidate、有序 revisions、guards、input、
中性 workset、SCOPE、SPEC、工具/配置/测试输入及 task baseline。缺项、错 candidate、跨 task、
乱序、源码/context/工具漂移、缺 build 或日志不匹配均拒收。归档恢复只复用这个 exact 已执行运行，
新 prepare/新 task 仍执行自己的门禁；原 review_only 终态语义未放宽。
首次 import 与 task-gates 严格校验当前 execution_inputs、runner 定义、完整 gate/build 和日志。
首次成功 import 的 receipt 另冻结 accepted gate_selection；完整 receipt/raw/终态锚点存在且匹配时，
幂等 import、check/export 预检查与 predecessor 重放使用既有 validate_historical 验证同一 receipt。
仍精确核对 task/dispatch/round/export/freeze/candidate、有序 revision/guards、input/workset/SCOPE/SPEC/base
及受跟踪日志 hash；无关工具或 runner 定义变化不会重置已接受覆盖。缺 receipt 的部分写入仍走首次严格校验，
语言、源码、参数、special 或中性 context 的实质漂移仍拒收。

export 的 `source-anchors/<sha256>.bin` 保存实际公开源码字节（DLC仍标 unpinned）。
import 另保存 `imports/<export>/task-anchors/` 的 STATE/SPEC/SCOPE/baseline、review records、
input/raw 和引用终态锚点实际字节；task gate logs 也保留实际字节，不能只引用 ignored 文件 hash。
正式 records 的文件定位使用 workspace-relative 路径，归档副本可以作为重建根运行
`ai_state_check.py --workspace-root <重建根>`；恢复生产 check 时按原定位重建这些冻结记录，
保留原身份及归档事实，不能改成新的 child。小 fixture 的 DONE/拒收/副本重放已由真实 predicate
验证，模拟命令输出明确标作受控测试，不计生产覆盖。

closure 中非 Boot official-inheritance 文本不能用 loading-only 跳过语言审核。
outside-release-followup 只允许实际发行外组件；RELEASE 五组件、Boot、release-addon namespace
和 retained-layer 均不能使用此处置。发行语言仍须真实已审 unit、同一 actualchain 的 shadow 证明，
或有具体源码字节及行锚点的 unreachable proof。Boot loading-only 与无语言文本的 copy/retained/loading 核查保持。
非 Boot copy/retained-layer/wrapper-addon 的 `language_literals=[]` 只是声明，不能证明无文本。
loading-only 会核验 copy 的冻结 content/path/hash 与当前字节、retained 的公开 addon 固定 commit/blob/hash，
以及 wrapper 显式 `source_file`（component/public_source_path/sha256/inner_root 或固定来源）。
复用 Lua 字符串及注释词法，只允许字体/locale 控制标识与已知布尔 flag 的有限指令证明无语言；
table/string flag payload、文字字段及英文同样需要语言审核，未知或动态输入失败关闭。
LocaleLoader 的 translations=[] 不构成此证明。真实 engine.copy 三行可通过，mod-tome.copy 随机神器词库不可豁免。
A/B 派发前与已冻结 opposite lane 比较 neutral unit/context/source_files；导入合并及继承合并按各自
origin/workset hash 再核对。B policy 不进入 neutral identity，但包括尚未导入 exports 的 applicability 不能缩小。
check 从已逐项 replay 核验的当前冻结 exports 汇总必做 B 义务，独立于 import 状态；当前裁决和
successor merged completion 共用该义务。兼容 predecessor 的未导入冻结义务按 unchanged revision/guard
及精确 neutral context/source_files 继承，即使宿主 contexts 遗漏新增 reason，也不能据 A 单独完成或缩小后续 policy。
独立改变语境或 revision 的 successor 仍按既有规则处理，不继承不兼容义务。
同语境并行冻结、旧 A 加新 B 与 policy-only 扩大仍可用。
可声明 `shadowed`，但须绑定 actual ordered chain 中该 official 文件 pin/hash、
`shadowed_registration` 的 layer/ordinal/tag 和实际 record，消费已复审且与 actual effective
target/args/special 相符的 unit；无覆盖则阻断。`unreachable` 需具体 `source_proof` 文件 pin/hash
及 `line_start/line_end`，保留 reason/source_verified 与 tracked evidence，不能无证 N/A。

发行 readiness 的 `engine_actual_loading / game_launch / scenarios[]` 各自是
`{status, binding, evidence}`（明确接受未测场景使用 `user_acceptance`）。每份测量 JSON 本身
也必须有相同 binding/status；binding 包含 exact `candidate_sha256, target, spec_sha256,
operation_id, installed_sha256`，绑定 durable installed.json/intent.json 和确切安装字节。
旧 prototype、旧 candidate、缺绑定或已回退/漂移 operation 不能通过最终发行 readiness。
原 GUI 能力记录的 `final_candidate_tested=false` 和 `A_B_credit=0` 保持。

### M1 同轮 successor 与非规范语言 unit

`python3 -B tools/full_review.py successor --directory <冻结前版本> --output <新版本> --request <宿主迁移.json>`
在同一 `round_id` 下建立独立不可变版本；两个目录均须位于
`evidence/full-review/` 或 `.artifacts/i18n/` 下，互不包含。
旧 inventory、export、raw、裁决和 task 记录全部保持原字节。
迁移前须完成旧版本的证据登记；发布 successor 后旧目录不能追加证据。
相同请求可重复执行，inventory 写入前中断可恢复；不同请求/旧目录字节漂移拒绝。
不允许跨 round 迁移，也不将人工 accepted 标志直接兑换覆盖。

宿主 request 必须包含：

- `round_id`、`before_sha256`（旧 inventory 字节）、`evidence`（受跟踪路径与 sha256）。
- `mapping`：旧/新 unit ID 并集每个一次，字段 `unit_id/status/reason`；status 为
  `unchanged/changed/added/removed`，guard/revision 自动核对，每次至多 80 个非 unchanged units。
- `supplements`：完整当前补充记录；`supplement_mapping` 对旧/新 supplement ID 并集守恒，
  使用 `supplement_id/status/reason`，不能静默遗漏新增、删除或变更记录。
- `contexts`：当前全部 unit ID → 与 export 中性 workset entry 完全一致的对象，包含
  `unit_id/context/source_files/b_reasons/b_exemption`，逐文件核验源码。
- `language_units`：完整当前非规范语言 units（无则 `[]`），格式如下。

未改 unit 仅在 guard/revision、完整中性 workset 和实际源码 hash 均未变时继承原有效 A/B；
旧 producer 仍须有自身精确绑定 DONE_VERIFIED、归档及裁决证据。
改变 source/target/args/special 或中性 context/source guard 的 unit 必须在 successor 中重新
export/import/adjudicate，重新绑定其自己的 task 闭合。无关术语行不改变 rules-v2 revision；
special 仍单独 guard，既有 catalog 身份函数不变。

非规范 language unit 使用独立 `language_id`（有界 token，稳定标识具体语言 unit），
不是 canonical `t()` locator，也不生成 surface ISSUE。宿主明确提供：

```json
{
  "language_id": "copy-label-one",
  "origins": ["<实际 supplement_id>"],
  "language": {"source": "hello", "target": "你好", "source_tag": null,
               "args_order": null, "special": null},
  "anchors": {
    "source": {"path": "<当前实际文本文件>", "sha256": "<文件hash>", "start": 0, "end": 5},
    "target": {"path": "<当前实际文本文件>", "sha256": "<文件hash>", "start": 6, "end": 12}
  },
  "context": "中性的实际使用语境",
  "source_files": [{"component": "engine", "public_source_path": "engine/test.lua",
                    "sha256": "<实际固定文件hash>", "line_start": 1, "line_end": 10}],
  "evidence": [{"path": "evidence/<宿主源码/运行层取证>", "sha256": "<hash>"}]
}
```

start/end 是 UTF-8 原始字节半开区间；必须等于当前真实 source/target。
source-only 缺译用实际运行回落原文作 target，不能虚构中文；继承使用实际不同 target；
copy 非 `t()` 文本使用实际语言字节及运行层取证。多 origins 合并还须 `merge_reason` 与宿主证据。
同一文件可有多个不同语言 unit；相同字节锚点/实际五字段不能重复登记，须明确合并来源。
实际参数、special、来源、语境与宿主证据全部 guard；snapshot 型 source identity 明示其证据集合，
不将 DLC 源码变成 pinned commit。

导出同时冻结 `preflight.json`（adapter 类型、实际结果、scope/payload hash 与 unit guards），
回放核对其精确字节并重新执行适用预检；旧无此字段的 exports 保持原验证语义。
export/import/check 仍走原七键 v2 review_only/full、≤800-byte prompt、strict 完整按序结果、
producer DONE_VERIFIED 与 A/B 独立 model/dispatch 检查。canonical 使用原 Lua anchor preflight；
非规范 unit 使用同形 SCOPE 路径验证与独立真实字节 preflight，范围文件不能冒充 `t()` 调用。
补充 unit 的两个 anchor 文件都须在 `allowed_files` 中；`anchor_scopes` 标明真实语言上下文。
closure 的 occurrences 映射包括当前新增语言 units，supplements 的 `review_units` 必须消费
其绑定的全部当前语言 units；未审核时仍阻断 complete。
非 `t()` runtime key 可明确 `kind: "language-bytes"`，提供 tracked execution `evidence`，
每层原文件 hash 与 `target_anchor: {start,end}`；普通 Lua runtime 链不变。
最终实际分母、GUI 和 game readiness 仍须宿主实测闭合，来源存在不抵语言审核。

FIX cycle1 的 successor 先合并来源目录正确的 validated outputs，再统一检查 A/B fresh/model 和裁决。
完成状态只整体继承当前必需 A/B 齐全的 merged completion；丢掉某 lane 语境时，合法 A 仅保留
validated 状态，可当前补 B/重新裁决。document_ordinal/line 仅作定位，不进入 semantic guard；
真实 Lua loader 的前插/删除测试同时验证未改 unit guard/revision 与 successor 覆盖稳定。

full-review task-gates 默认生成 schema 3 receipt。可复用经读审计的 registration、semantic-claim、
contract-suite 和 production-shadow-surface-ledger 四组测试。toolchain 读取 full-review
路径和可变 ignored inventory cache；quality-facts 读取未绑定的 Pi／Node 安装闭包，两组均每次执行。
所有其他检查（含 build）也每份 receipt 执行。每组 identity 绑定其读取的全部输入。
registration identity 包含 tools/、tests/、i18n/ 的全部 tracked 与 nonignored 输入
（含模式、symlink 和额外 discovered ignored tests／Python bytecode）、argv、Python／工具／runner
版本和完整环境。另三组扩大为全仓 tracked／nonignored 文件，但排除经读审计确认不依赖的
`evidence/full-review/`、`.ai/task/`、`.ai/reviews/` 和 `.artifacts/`；另显式绑定 ignored
`.artifacts/i18n/production-review/reconciliation.json`（含不存在状态）和上述 bytecode。
扩大身份还绑定 HEAD、index、Git refs／有效配置／exclude／graft／shallow 输入、manifest 固定
extractor archive 与其仓库 HEAD、Lua runtime／rocks 模块、Git／shell／Node 程序及其动态库字节。身份哈希复用 binding
的 stat cache；读审计及依赖证明见 maintenance gate-speedup REPORT。
复用仅取同 round 的 task-gates/ 已归档 full PASS receipt，并绑定其实际字节、日志和测试 identity。
测试 identity 另绑定符号链接解析目标内容；目标未覆盖或位于未列出的排除目录时，全部测试执行。
复用记录无自身退出码或时间戳；首次及历史验证均递归检查来源，拒绝循环和跨轮引用。
完整环境仅参与门禁复用选择及同次执行验证；后续消费／导入验证冻结 identity 与来源链，
不重新计算消费进程环境的 identity。
`I18N_GATE_TEST_REUSE=off` 禁用复用。普通 ci-gates 及 production-review-v2-lite 保持 schema 2。

binding 的忽略缓存位于 `.artifacts/i18n/gate-binding-cache.json`，严格 JSON、原子替换；
文件路径、size、mtime_ns、ctime_ns、inode、device、mode 全部相同才复用内容 hash。
`I18N_GATE_BINDING_CACHE=off` 使用原始逐字节路径；缓存损坏或写入失败仅影响速度。
在同用户脚本可信、仅防意外损坏的模型下，若字节被修改却连 ctime 等全部 stat 字段都相同，
缓存可能漏检；恢复 mtime 但 ctime 变化仍会重算。所有其他绑定字段和执行前后漂移检查保持有效。
