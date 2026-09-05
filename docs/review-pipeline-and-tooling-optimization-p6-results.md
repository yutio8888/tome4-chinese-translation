# P6：来源属性与 doctor 扫描结果

实施基线为干净的 `3d67e874ed06e7de5809fb3e0b378cc835ce7d62`（P5 已完成并推送）。
本报告由 EXECUTOR 在最终完整门禁前完成；最终实际退出码与候选绑定见
`.artifacts/i18n/tooling-optimization-p6-fix-1/latest-receipt.json`，不预写门禁通过结论。
原实施回执 `.artifacts/i18n/tooling-optimization-p6-implement/final-receipt.json` 与基线比较保留。
独立复审、裁决、归档、DONE_VERIFIED、提交与推送由宿主继续完成，不属于本次 EXECUTOR 回执。

## 实施范围

- manifest schema 1 为两个 repository、三个官方 DLC 分别增加 `visibility`、`extraction_mode`、
  `source_pinning`、`scan_allowlist`；四项语义及兼容默认见 [工具说明](../i18n/README.md#来源属性与-doctor-扫描)。
- `config.py` 校验枚举、类型及扫描路径；broker 保留原路由，拒绝不支持的固定源码声明、
  full-tree 声明与非空扫描列表。官方 DLC 公开性不再从 broker 名称推断。
- `git_source.py` 为 validate 增加可选 allowlist：省略保持全树；空列表完全不调用 status；
  单独 `.` 是显式根哨兵；普通路径以 top/literal pathspec 传递。commit 验证保持独立。
- `cli_doctor.py` 根据 repository allowlist 扫描，移除因 broker 存在而跳过整个 engine 的逻辑。
  文本和 JSON 保留旧报告字段，并显示四项属性；每个 DLC 增加明确的 source-unpinned 警告。
  缺失可选仓库、脏工作树仍仅警告；Git status 失败仍报错。
- 两个已有测试模块增加有界真实 Git、配置与 doctor 回归；未新增测试模块或改动注册表。
  `extract.py`、Lua 路由、固定源码输入、提取快照、release layers 均无需修改。

## 已执行核验

验证文件均位于 `.artifacts/i18n/tooling-optimization-p6-implement/`，可重生成的产物不迁入历史 evidence。

| 核验 | 实际结果与产物 |
| --- | --- |
| 初始环境 | 编辑前运行真实 doctor JSON 和严格核心 addon build；`baseline-doctor.json`、`baseline-build.json` |
| 定向测试 | `python3 -B -m unittest tests.i18n.test_toolchain_git_config tests.i18n.test_toolchain_doctor`：17 tests PASS，`focused.log` |
| 真实 Git 边界 | 临时仓库覆盖内部干净/修改/暂存/未跟踪、外部忽略、默认全树、根哨兵、空列表不执行 status、字面 metacharacters、不存在 commit、status 故障 |
| doctor 模拟 | 三个 DLC 的全部 8 种可用性组合，分别验证 text/JSON、缺失 optional repo、精确 validate 参数、脏工作树警告与退出 0 |
| 真实 doctor | text/JSON 均退出 0；两个仓库可用且各自扫描范围内干净，三个 DLC 可用、公开且 unpinned；`final-doctor.text`、`final-doctor.json` |
| 实际扫描参数 | 包装真实 Git 调用记录完整 argv/退出码，未替换执行结果；`actual-git-argv.json` |
| 公开路径 | 六个组件路径存在于工作树及固定 engine commit；`i18n_tools` 不在当前工作树，但存在于固定 extractor commit；`public-path-checks.json` |
| 源码与保护集 | `comparison.json`：manifest 仅增加上述属性；700 个 evidence 文件、合计 730 个 evidence/Lua/术语保护文件的路径集和逐文件 SHA-256 相同 |
| catalog | 编辑前后重建完整 v2-lite catalog：29,828 条 entries 字节与 revision identities 不变；exclusions、schema、policy 字节相同；source identities 相同 |
| addon | 前后真实 `build --profile addon --component tome --require-complete --json`：输出字节相同；除运行目录/输出路径外报告全等，4,260 个 patch runtime keys，缺失/不符/冗余/意外条目均为 0 |

engine 的两个真实 doctor 调用均使用以下 status 参数（仓库根由环境配置解析）：

```text
status --porcelain --untracked-files=all --
:(top,literal)game/engines/default/data
:(top,literal)game/engines/default/engine
:(top,literal)game/engines/default/modules/boot
:(top,literal)game/modules/example
:(top,literal)game/modules/example_realtime
:(top,literal)game/modules/tome
:(top,literal)i18n_tools
```

没有 engine 全树或 `game/dlcs` 扫描。编辑前 doctor 对 engine 报告
`worktree_checked=false, clean=null`，并给出旧的全 engine skip 警告；编辑后为
`worktree_checked=true, clean=true`，旧警告消失，新增三个 source-unpinned 警告。

真实 manifest 原始哈希由
`192e95636a17f4de4e591ae0ad9c4b7de455f01c8383ebdc1bda02d4b1b2eace`
变为 `f62ac4fb8ff968deb3e582dd8d25129cfd23a94c7881e8f6b28b0e40afd85a1d`。
新生成 catalog manifest 仅 `manifest_sha256` 和由它计算的 `catalog_id` 改变，不能声称整个
catalog 字节不变；历史 evidence 未改写或迁移。addon 输出 SHA-256 为
`515ebd8d97f6d9ddfcf2eee2bc6083e0dddb5fec62699b88b8512f10c0ec8399`。

## 最终门禁绑定与边界

文档修复轮 1 按宿主 confirmed 的 P6-SR-1 修正 README 常用命令中遗留的“engine 不执行
Git 状态扫描”表述，改为按 repository `scan_allowlist` 进行字面路径扫描；保留 DLC 仅探测
预声明组件、不遍历目录，以及 engine 不扫描 `game/dlcs` 或整树的边界。其余六个候选路径
与宿主冻结哈希逐字节核对一致。此次修复及新回执产物位于
`.artifacts/i18n/tooling-optimization-p6-fix-1/`。

本报告先完成，再保存候选内容哈希并运行 `tools/ci-gates.sh`，包含严格 addon build；同时运行
Paseo contract check、tracked/untracked 文档空白检查。门禁期间不写任务内容；最终回执记录
完整 17 项门禁路径、退出码、日志哈希、严格回执校验与前后候选字节一致性，仅写 ignored 产物。

实施中真实 Git 测试发现 `:(top,literal).` 不具备全根扫描语义，已修正为单独的 `.` 分支并
通过回归。公开路径检查最初假设 extractor 目录存在于工作树；实际固定源码核验推翻该假设，
记录已更正为“工作树不存在、固定 extractor commit 存在”，没有修改外部源码仓库。
没有修改 `.ai`、index、译文、术语或历史 evidence，没有创建 child、stage、commit 或 push。
