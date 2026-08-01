# ToME4 汉化项目交接清单

更新时间：2026-08-01

本文记录当前翻译工具、术语库和发布流程的状态，供后续继续开发、审校或发布使用。

## 一、当前目标

- 以本仓库为唯一规范译文源。
- 建立可复现的术语库和翻译工具链。
- 发布插件只包含相对源码/官方 locale 的必要覆盖译文；源码已有且未改变的译文不重复打包。
- 对公开源码和闭源 DLC 使用不同的输入边界，避免工具绕过受保护提取流程。

## 二、已完成事项

### 翻译与术语

- 已建立 `terminology.tsv` 和 `TERMINOLOGY.md` 的术语库工作流。
- 当前术语表共 470 条，其中 152 条属于 `scope=dlc`。
- DLC 首轮候选已通过受审计提取器处理 `ashes-urhrok`、`cults`、`orcs`，未直接读取受保护源码。
- 当前保留少量待审校术语，包括 `Constrict`、`eldritch` 和 `Atmos Tribe` 等语境差异。
- 已保留翻译条目的 `source_tag`，并为术语补充 `T.*` 分类及语境说明。

### 工具链

- `doctor`、`extract`、`lint`、`status`、`merge`、`workset`、`context`、`proposal`、`review`、`build` 已统一到 `python3 -B tools/i18n` 入口。
- 审核流程：`tools/i18n review` 生成只读 Pi 审核 bundle，`tools/pi-review --bundle` 产生 findings，`tools/pi-remediate --bundle --review` 产生修订建议；修订需由主代理校验后应用。
- 构建工具现在支持最小 addon 覆盖层：官方已有且语义未改变的译文只计入继承统计，不写入插件。
- 显式指定组件时，例如：

  ```bash
  python3 -B tools/i18n build --profile addon --component tome --require-complete
  ```

  只检查所选组件，不会把未选择的 DLC、旧 lore 或 Nullpack 层算作不完整。
- addon 构建报告现在包含 `inherited_entries`、`override_entries`、`new_entries`，并对重复运行键进行去重。
- 所有工具报告和候选文件仍只写入被忽略的 `.artifacts/i18n/`。

### 本次发布边界决策

- 核心发布层固定为 `tome`，继续使用 `build --profile addon --component tome --require-complete`；DLC 和外部覆盖层不再作为核心构建的隐式依赖。
- `ashes-urhrok`、`cults`、`orcs` 已登记受保护提取快照的哈希基线；`items-vault`、`possessors` 已登记为受保护组件，但当前探测不到来源，仍属于 DLC 可选层的 `baseline-pending` 状态。
- `legacy-lore-overlay` 与 `nullpackreloaded` 各自拆为独立可选外部层。当前不把 addon 仓库提交当作它们的官方源码基线，也不把它们计入核心发布完整性。
- 以上边界已写入 `i18n/versions/tome-1.7.6.json` 的 `release_layers`；后续严格构建需要按层选择并验证，不应通过忽略缺失来源来伪造全量通过。

## 三、最近验证结果

以下结果是当前工作区最近一次验证的基线：

- 单元测试：30 项通过。
- 普通 lint：0 个错误、51 个警告。
- 核心最小 addon：构建成功，219 个覆盖键，其中 18,804 个官方已有译文未进入插件，210 个覆盖译文，9 个新增译文。
- full 构建：`engine`、`boot`、`tome`、`example`、`example-realtime` 均成功。
- 默认全量 addon：仍为 `INCOMPLETE`；加 `--require-complete` 应以退出码 5 阻断发布。

普通 lint 的 51 个警告主要集中在控制标记、`@token` 大小写/缺失，以及一处格式宽度差异。`lint --strict` 当前不能作为通过门槛。

## 四、待办事项

### P0：发布基线

- [ ] 为 `ashes-urhrok`、`cults`、`orcs`、`items-vault`、`possessors` 建立可验证的官方/源码基线，或在 manifest 中明确它们属于可选发布层。
- [ ] 为 `legacy-lore-overlay` 固定来源、版本和归属组件。
- [ ] 为 `nullpackreloaded` 固定源码来源和版本，或拆成独立可选插件。
- [ ] 明确发布策略：核心 `tome` 插件与 DLC/外部层是否分别发布；不要为了让全量构建通过而跳过基线校验。

### P1：翻译质量

- [ ] 逐条审校 51 个 lint 警告，区分真实控制标记错误和有意的颜色/占位符改写。
- [ ] 优先处理 `@Target@`/`@target@`、`#LIGHT_STELL_BLUE#` 等疑似大小写或拼写问题。
- [ ] 审定 `Constrict`、`eldritch`、`Atmos Tribe` 等多译法术语，并按术语库流程先改 TSV，再改 Lua。
- [ ] 检查 1,717 个重复运行键，确认是合法覆盖、历史重复，还是需要清理的冲突来源。

### P2：流程与工程化

- [ ] 为默认构建、核心最小构建和基线缺失场景补充 CLI 集成测试。
- [ ] 建立持续集成检查：LuaJIT 加载、普通 lint、单元测试、核心 build，以及禁止受保护目录越界读取。
- [ ] 评估是否需要安全的人工审核后 apply 流程；当前 `merge`/`proposal` 只生成候选和校验结果，不会原地修改规范 Lua。
- [x] 新增的 `i18n/`、`tools/`、`tests/` 文件已纳入本次工具链提交；发布仍需单独执行。

## 五、推荐工作顺序

1. 先确定核心插件与 DLC/外部层的发布边界。
2. 为需要发布的 DLC 建立固定基线，并让 `build --profile addon --require-complete` 能够按目标 profile 严格判断完整性。
3. 处理 lint 警告和重复运行键，再更新术语库中的待审校条目。
4. 补齐 CI 和构建集成测试。
5. 最后再生成发布 artifact，并进行独立 LuaJIT 加载验证。

## 六、常用命令

```bash
python3 -B tools/i18n doctor
python3 -m unittest -q tests/i18n/test_toolchain.py
python3 -B tools/i18n lint --json
python3 -B tools/i18n lint --strict
python3 -B tools/i18n status --json
python3 -B tools/i18n build --profile addon --component tome --require-complete --json
python3 -B tools/i18n build --profile addon --require-complete --json
```

执行 Lua 相关检查时必须遵守 `AGENTS.md` 中的 LuaJIT 5.1 和模块路径要求。任何 DLC 提取、快照或上下文操作都必须通过仓库内受审计的工具完成；不得使用通用文件搜索、脚本 API 或 Git 命令直接读取受保护 DLC 输入。

## 七、本次提交范围

本次工具链提交包括：

- `.gitignore`、`AGENTS.md`、`TERMINOLOGY.md`、`terminology.tsv`
- 新增工具目录 `i18n/`、`tools/`
- 新增测试目录 `tests/`
- 本交接文件 `handoff.md`

上述内容共同构成可复现的 i18n 工具链、受保护输入边界和首轮 DLC 术语基线；发布操作不包含在本次提交中。
