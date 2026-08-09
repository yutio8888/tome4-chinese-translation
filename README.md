# ToME4 中文翻译规范与工具链

[![License: GPL v3 or later](https://img.shields.io/badge/License-GPLv3%2B-blue.svg)](./COPYING)

本仓库维护《Tales of Maj'Eyal》（ToME4）的规范中文译文、术语库，以及用于提取、
校验、审核、构建和发布译文的确定性工具链。玩家可直接安装的汉化补充插件位于
[`yutio8888/tome4-chn-mod`](https://github.com/yutio8888/tome4-chn-mod)。

## 当前基线

- 目标游戏版本：ToME4 1.7.6。
- 官方 DLC 源码基线：Ashes of Urh'Rok、Cults of Entropy、Embers of Rage 1.7.4。
- 规范译文：30,177 条，严格 lint、运行键扫描和核心 addon 构建均通过。
- 发布 addon：`tome-chn-mod` 0.2.4，固定提交 `947e624`。
- Facts 因果研究：正式结论为 `do-not-promote-facts-channel`，不授予 holdout
  准入；详见 [`docs/translation-quality-facts-study-report-v1.md`](docs/translation-quality-facts-study-report-v1.md)。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `*.lua` | 各组件的规范中文译文 |
| `terminology.tsv` / `TERMINOLOGY.md` | 版本化术语库及维护规则 |
| `i18n/versions/` | 固定游戏、源码和发布仓库身份 |
| `i18n/quality/` | 翻译质量规则、schema 和版本化协议 |
| `tools/i18nlib/` | 提取、校验、构建、审核与质量工具实现 |
| `tests/i18n/` | 工具链和质量系统回归测试 |
| `docs/` | 设计、发布、审核和研究文档 |

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

更完整的命令、输入边界和构建语义见 [`i18n/README.md`](i18n/README.md)。参与
译文维护前请先阅读 [`AGENTS.md`](AGENTS.md)、[`TERMINOLOGY.md`](TERMINOLOGY.md)
和 [`docs/lessons-learned.md`](docs/lessons-learned.md)。

所有 inventory、候选、评审输出和构建结果均写入已忽略的 `.artifacts/i18n/`，
不会自动覆盖规范 Lua。任何外部模型调用还必须遵守 `AGENTS.md` 的有界输入和明确
授权要求。

## 许可与上游

ToME4 及三个官方 DLC 的上游内容由 Nicolas Casalini “DarkGod” 及其他上游贡献者
持有版权，并按 GNU GPL v3 或任何更新版本发布。本仓库包含其中文本的中文本地化
衍生作品；项目新增译文、工具和文档由各自贡献者持有版权，并按相同的
**GNU GPL v3 或任何更新版本**发布。

项目授权说明见 [`LICENSE`](LICENSE)，GPL v3 全文见 [`COPYING`](COPYING)。本项目
与 Netcore Games 或官方 ToME4 项目没有隶属关系。
