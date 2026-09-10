# ToME4 中文翻译规范与工具链

[![License: GPL v3 or later](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](./COPYING)

本仓库维护《Tales of Maj'Eyal》（ToME4）的规范中文译文、术语库，以及用于提取、
校验、审核、构建和发布译文的确定性工具链。玩家可直接安装的汉化补充插件位于
[`yutio8888/tome4-chn-mod`](https://github.com/yutio8888/tome4-chn-mod)。

## 当前基线

- 目标游戏版本：ToME4 1.7.6。
- 官方 DLC：Ashes of Urh'Rok、Cults of Entropy、Embers of Rage 使用已冻结提取快照；
  源码仓库／commit 未固定，不能据快照认定源码版本为 1.7.4。
- 规范译文：30,308 条；最近一次累计严格 lint、运行键扫描和核心 addon 构建均通过。
- 发布 addon：`tome-chn-mod` 0.2.7，发布提交 `9cdbd30`；主 locale 共 8,949 条，
  其中核心覆盖 3,488 条、DLC 覆盖 5,461 条（Nullpack 464 条由独立文件加载）。
- Facts 因果研究：正式结论为 `do-not-promote-facts-channel`，不授予 holdout
  准入；详见 [`docs/translation-quality-facts-study-report-v1.md`](deprecated/docs/translation-quality-facts-study-report-v1.md)。
- 当前执行路线（2026-09-10）：正式 WP2-Lite 审核以每批 80 条持续推进，已完成并
  finalize 至第 67 批；维护者授权连续主持，逐批自动推进。广泛的全库清扫作为独立的
  有界维护窗口执行，不混入正常批次。当前操作入口、每步命令与生效裁决表见
  [`基线批次 runbook`](docs/baseline-batch-runbook-2026-09-06.md)；编排脚本用法见
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
