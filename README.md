# ToME4 中文翻译规范与工具链

[![License: GPL v3 or later](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](./COPYING)

本仓库维护《Tales of Maj'Eyal》（ToME4）的规范中文译文、术语库，以及用于提取、
校验、审核、构建和发布译文的确定性工具链。玩家可直接安装的汉化补充插件位于
[`yutio8888/tome4-chn-mod`](https://github.com/yutio8888/tome4-chn-mod)。

## 当前基线

- 目标游戏版本：ToME4 1.7.6。
- 官方 DLC：Ashes of Urh'Rok、Cults of Entropy、Embers of Rage 使用已冻结提取快照；
  源码仓库／commit 未固定，不能据快照认定源码版本为 1.7.4。
- 规范译文：**30,317 条**（11 个组件），版本化术语库 **931 条**（11 领域）；完整 17 项 CI 门禁
  （`tools/ci-gates.sh`，含严格 lint、运行键冲突扫描、术语静态/动态审计与核心 addon 构建）全部通过。
- 最新公开插件：`tome-chn-mod` **[`v0.3.17`](https://github.com/yutio8888/tome4-chn-mod/releases/tag/v0.3.17)**（2026-11-20，发布提交 `c1c17b91`，来源本仓库 `10c6cf260`）；
  主 locale 共 **13,821 条**，其中核心覆盖 8,153 条、引擎覆盖 207 条、DLC 覆盖 5,461 条
  （Ashes 743 / Cults 1,569 / Embers 3,149；Nullpack 443 条由独立文件加载）。
- Facts 因果研究：正式结论为 `do-not-promote-facts-channel`，不授予 holdout
  准入；详见 [`docs/translation-quality-facts-study-report-v1.md`](deprecated/docs/translation-quality-facts-study-report-v1.md)。
- 当前执行路线（2026-11-20）：采用 2026-11-01 起启用的[轻量审核流程](docs/lite-review-workflow-20261101.md)，
  已完成 29,554 个 release-required 单元的全库双审、多轮专项清扫（开局 UI、装备提示、状态悬停、逆向资源、核心对话框、新手教程、铭文短描述）、
  说明文精简以及社区高频术语与经典专名回调（累计推进至第 **`0575`** 批）。当前 `develop` 上有待发布维护批 `0575`（`de3ff2869`），
  按维护者指示暂留 `develop` 尚未发布 `v0.3.18`。
  当前详细状态、现行编辑红线与待办见 [`handoff.md`](handoff.md)；
  历史 WP2-Lite 规则与生效裁决表见 [`审核操作指南`](docs/review-operations-guide.md)；编排脚本用法见
  [`tools/orchestration/README.md`](tools/orchestration/README.md)；历史阶段见
  [`项目路线图`](docs/project-roadmap.md)。已被取代的设计稿、阶段计划与一次性交接
  统一收在 [`deprecated/`](deprecated/README.md)，不作为任何操作依据。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `*.lua` | 各组件的规范中文译文 |
| `terminology/` / `TERMINOLOGY.md` | 版本化术语库及维护规则 |
| `i18n/versions/` | 固定游戏、源码和发布仓库身份 |
| `i18n/quality/` | 翻译质量规则、schema 和版本化协议 |
| `tools/i18nlib/` | 提取、校验、构建、审核与质量工具实现 |
| `tests/i18n/` | 工具链和质量系统回归测试 |
| `docs/` | 现行设计、审核契约与操作文档 |
| `deprecated/` | 已被取代、仅供历史查证的文档，勿作操作依据 |
| `archive/` | pi CLI 时代的路由层资产（Skill、subagent、旧契约） |

## 快速开始

项目统一通过 Python 入口调用工具；Lua 子进程的 LuaJIT 5.1 模块路径由工具自动
设置，无需手动导出环境变量。

```bash
python3 -B tools/i18n doctor
python3 -B tools/i18n status
python3 -B tools/i18n lint --strict
python3 -B tools/i18n build --profile addon --component tome --require-complete
tools/ci-gates.sh
```

上列命令展示工具入口，并非每次修改都要顺序执行。按 [`AGENTS.md`](AGENTS.md) 选择任务入口，
检查范围以[工作流验证矩阵](docs/agent-workflow.md#验证矩阵)为准。首次做译文工作时读
[`TERMINOLOGY.md`](TERMINOLOGY.md) 的使用规则，随后查询相关术语；工具命令和特殊操作按需查
[`i18n/README.md`](i18n/README.md) 与 [`lessons-learned.md`](docs/lessons-learned.md) 对应章节。

可重生成的 inventory、候选和构建结果写入已忽略的 `.artifacts/i18n/`，不会自动覆盖规范 Lua。
人工裁决和不可重生成核验锚点写入受跟踪的 `evidence/`；正式审核要求保留的原始输入／输出
按其契约随证据保存。外部模型调用遵守 `AGENTS.md` 的输入边界与既有授权。
三个旧项目 Skill 仅保留于 [`archive/`](archive/README.md)，归档正文不构成当前路由。

## 许可与上游

ToME4 及三个官方 DLC 的上游内容由 Nicolas Casalini “DarkGod” 及其他上游贡献者
持有版权，并按 GNU GPL v3 或任何更新版本发布。本仓库包含其中文本的中文本地化
衍生作品；项目新增译文、工具和文档由各自贡献者持有版权，并按相同的
**GNU GPL v3 或任何更新版本**发布。

项目授权说明见 [`LICENSE`](LICENSE)，GPL v3 全文见 [`COPYING`](COPYING)。本项目
与 Netcore Games 或官方 ToME4 项目没有隶属关系。
