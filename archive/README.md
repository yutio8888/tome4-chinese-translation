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

- `.agents/skills/tome4-pi-review/` —— 旧译文/代码审核 Skill（translation v2 与 code/legacy v1）。
- `.agents/skills/tome4-pi-file-review/` —— 旧 code/legacy v1 源码感知文件审核 Skill。
- `.agents/skills/tome4-pi-subagent/` —— 旧 scout／plan-reviewer subagent 调度 Skill。
- `.pi/agents/scout.md`、`.pi/agents/plan-reviewer.md` —— 旧只读 subagent 定义。
- `.pi/extensions/subagent/` —— 旧 subagent 调度扩展（agents.ts／index.ts／live-output.mjs）。
- `tools/pi-review-batch.py`、`tools/_p2_run_review.py`、`tools/_p3_run_review.py`、
  `tools/_p4_run_review.py` —— 旧 v1 批量审核编排脚本。
- `tools/pi-review-files` —— 旧 code/legacy v1 文件审核 headless 入口。
- `docs/pi-review-worker-tuning.md` —— 旧 v1 并发 worker 调优历史记录。
- `docs/pi-review-v2-contract.md` —— 旧 translation v2 blind runner 契约，已退役；
  译文审核改由 Paseo `translation_contextual_v1` 承担（见
  `docs/paseo-translation-context-review-v1-contract.md`）。

## 未归档（仍活跃，Paseo 直接调用）

以下资产**不是**旧 Skill，仍由 ORCHESTRATOR 作为工具直接调用，继续活跃：

- `tools/pi-subagent --workset`（`tools/i18nlib/pi_agent.py`）与
  `tools/pi-tmux translate`（`tools/i18nlib/pi_tmux.py` 的 `translate` 子命令）——
  翻译 proposal 生成。pi-tmux 只有 `translate` 是活跃子命令；`review`／`review-files`
  在 `main` 中先于一切副作用被拦截（tombstone 分支，见下），不属活跃 review。
- `tools/pi-quality-evaluator`、`tools/pi-quality-facts-study`、`tools/pi-quality-role`
  （`tools/i18nlib/pi_quality.py`、`pi_facts_study.py`、`pi_roles.py`）—— 质量抽样。
- `tools/i18nlib/pi_file_review.py` 与 `tools/i18nlib/pi_review.py` 的低层原语被
  质量评估器、Facts study 与兼容消费者复用：例如
  `pi_file_review._run_file_review_process` 供 pi_quality／pi_facts_study 调用，
  `pi_review._canonical_sha256` 供 pi_quality 使用，
  `pi_review._stage_validated_json` 供 pi_remediate／pi_file_review 使用。两个模块的
  code/legacy v1 审核**入口**不属活跃路径：`tools/pi-review-files` 已归档，
  `pi_review.main` 已无任何入口引用。

## Tombstone、残留 driver 与 dormant 消费者

- `tools/pi-review` 与 `tools/pi-tmux review`／`review-files` 是当前仓库 tombstone：
  任何调用都在产生任何副作用之前非零退出并输出退役指引，不读取 bundle、不启动
  provider。入口退役后保留的 `run_pi_review`（`tools/i18nlib/pi_review.py`，仅被
  本模块未挂接的 `main` 内部引用，除 `tests/i18n/test_toolchain.py` 回归测试外无生产
  调用者）／`run_tmux_review`／`run_tmux_file_review`
  （`tools/i18nlib/pi_tmux.py`，除 `tests/i18n/test_toolchain.py` 回归测试外无生产
  调用者）是残留 driver，**不**因复用而保留，也不构成活跃审核入口；`pi_file_review.main` 同属残留路径。
- `tools/pi-remediate`（含 `tools/pi-tmux remediate`）是 dormant 兼容消费者，不是活跃
  审核 dispatch：只消费既有、已确认的 legacy assessment/finding artifact 生成修复
  proposal，不再列入「仍活跃审核」。dormant 仅指不参与活跃审核 dispatch；实际调用它
  仍会启动外部 Pi provider 子进程，外发必须按 `AGENTS.md`「外发边界」取得授权，它
  不像 tombstone 那样不启动 provider。
