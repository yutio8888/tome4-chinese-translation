# 已归档：pi CLI 审核/翻译旧契约

本目录收纳被 Paseo 轻量编排取代的旧「pi CLI 审核/翻译」契约与路由层资产。
这些资产在项目切换到 Paseo（`docs/paseo-orchestration-v2-contract.md`）后不再参与
任何审核或翻译路由，仅保留作为历史记录与回滚依据。

## 归档时间与依据

- 归档依据：Paseo 已成为审核/实现编排的唯一路由；旧项目 Skill 与 subagent 路由被
  ORCHESTRATOR／EXECUTOR／REVIEWER／SENIOR_REVIEWER 角色取代。
- 归档后，以下内容不再可用：`$tome4-pi-review`、`$tome4-pi-file-review`、
  `$tome4-pi-subagent` 三个项目 Skill，及其 scout／plan-reviewer subagent 路由。

## 归档清单

- `skills/tome4-pi-review/` —— 旧译文/代码审核 Skill（translation v2 与 code/legacy v1）。
- `skills/tome4-pi-file-review/` —— 旧 code/legacy v1 源码感知文件审核 Skill。
- `skills/tome4-pi-subagent/` —— 旧 scout／plan-reviewer subagent 调度 Skill。
- `pi/agents/scout.md`、`pi/agents/plan-reviewer.md` —— 旧只读 subagent 定义。
- `pi/extensions/subagent/` —— 旧 subagent 调度扩展（agents.ts／index.ts／live-output.mjs）。
- `tools/pi-review-batch.py`、`tools/_p2_run_review.py`、`tools/_p3_run_review.py`、
  `tools/_p4_run_review.py` —— 旧 v1 批量审核编排脚本。
- `tools/pi-review-files` —— 旧 code/legacy v1 文件审核 headless 入口。
- `docs/pi-review-worker-tuning.md` —— 旧 v1 并发 worker 调优历史记录。
- `docs/pi-review-v2-contract.md` —— 旧 translation v2 blind runner 契约，已退役；
  译文审核改由 Paseo `translation_contextual_v1` 承担（见
  `docs/paseo-translation-context-review-v1-contract.md`）。

## 未归档（仍活跃，Paseo 直接调用）

以下资产**不是**旧 Skill，仍由 ORCHESTRATOR 作为工具直接调用，继续活跃：

- `tools/pi-subagent --workset`（`tools/i18nlib/pi_agent.py`）、`tools/pi-tmux translate` ——
  翻译 proposal 生成。
- `tools/pi-quality-evaluator`、`tools/pi-quality-facts-study`、`tools/pi-quality-role`、
  `tools/pi-remediate`（`tools/i18nlib/pi_quality.py`、`pi_facts_study.py`、
  `pi_roles.py`、`pi_remediate.py`）—— 质量抽样与已确认 finding 修复建议。
- `tools/i18nlib/pi_file_review.py` —— 低层 provider 子进程调用与 file-review 工具原语，
  仍被质量评估器、Facts study 与 pi_tmux 复用；其 code/legacy v1 审核**入口**
  （`tools/pi-review-files`）已归档，但模块本身保留。`tools/i18nlib/pi_tmux.py` 的
  `review-files` 子命令与 `pi_file_review.main` 作为残留代码路径仍存在（已无任何文档
  入口），为不扰动活跃的 review/translate/remediate 子命令而未在本次一并删除。
