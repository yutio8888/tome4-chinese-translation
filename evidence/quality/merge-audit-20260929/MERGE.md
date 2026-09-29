# 合并 audit/modified-translations-20260921（2026-09-29）

用户 2026-09-29 选择“合并窗口”：以 git merge 保留分支全部提交与证据（`evidence/translation-audit/`、`evidence/spotchecks/` 共 3782 个文件及 TERMINOLOGY.md、docs/agent-workflow.md 两段规则），译文按条目裁决。

- 分支基点 `7c38a53b`（2026-09-21），分支头 `4ada4c29`（2026-09-25）；合并前 develop `27cd860d`。
- 分支共改 442 条译文（mod-tome 355、tome-orcs 62、engine 13、mod-boot 7、tome-possessors 5），其中 3 条为删除过期键（本次未采纳，见下）。
- 370 条 develop 自 09-21 起未改动：367 条改 target 的原样采用分支版（逐字复制分支的 target 字面量，`task/splice.py`；LuaJIT 加载核验逐条相符）；分支另删 3 个过期键（engine.lua “following chain...”、mod-tome.lua horrors.lua “Open a hole in space…”与 inscriptions.lua Heroism 长说明），但删键会改变正式版本向量（`tools/i18nlib/production_review_v2_lite.py` CURRENT_VECTOR 与 policy-v1.json 固定 30308/29828/480，门禁 05 报 drift），属工具与策略变更，本次合并恢复这 3 条、保持主线原文，删键另行立项（pending）。
- 2 条两边结果相同。
- 70 条两边改法不同：4 组只读 REVIEWER（claude-opus-5-5）逐条对照源码比对（`task/CONFLICTS-G*.json` → `task/CMP-G*-result.json`），宿主逐条核验后裁决（`task/HOST-CONFLICT-DECISIONS.json`）：保留主线 57（含 C48 宿主推翻：截断名遵循 09-27 毁灭号术语裁决）、采用分支 4（C30、C41、C47、C50）、合并 9（C05–C08、C10、C26、C34、C44、C55）。
- 09-21 之后的正式裁决优先：Writhing One＝蠕动者（engine.lua、mod-boot.lua 禁忌邪教简介两处由 EXECUTOR 改正）；Mind Drone＝精神无人机（冲突条目保留主线）；manaburn arcane 术语行保留主线“法力燃烧”（用户 09-27 裁决，分支为 09-24 的“奥术法力燃烧”）；分支的 global speed、Physical Power 两处 scope 扩为 global 照收。
- 9 条合并与 2 处裁决修正由 EXECUTOR（codex gpt-5.6-sol）按 `task/EXEC-PACKAGE.json` 撰写，宿主独立核验恰 11 个 target 变动（`IMPLEMENTATION.md`、`VALIDATION.json`）。
- advisory（未改）：C27 石化形态说明 LF 数与英文不一（三版相同，既有问题）；C05 a dozen 弱化、C07 漏 all carved out of flickering orange fire、C08 So, in turn 未译出（EXECUTOR 报告，均为 port 之外）。
- 全部合并后变动的条目成为新 revision，经 catalog/migration 发布后按常规审核批次重新审核，不继承旧 done。
