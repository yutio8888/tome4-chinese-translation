# ToME4 汉化项目交接清单

更新时间：2026-08-03（深夜，第一轮审核 finding 处置完成，队列清零）

本文记录当前翻译工具、术语库和发布流程的状态，供后续继续开发、审校或发布使用。

## 一、当前目标

- 以本仓库为唯一规范译文源。
- 建立可复现的术语库和翻译工具链。
- 发布插件只包含相对源码/官方 locale 的必要覆盖译文；源码已有且未改变的译文不重复打包。
- 对公开源码和闭源 DLC 使用不同的输入边界，避免工具绕过受保护提取流程。

## 二、已完成事项

### 翻译与术语

- 已建立 `terminology.tsv` 和 `TERMINOLOGY.md` 的术语库工作流。
- 当前术语表共 653 条：`existing` 440 条、`preferred` 210 条、`review` 3 条。
- 相比上一版交接基线净增 183 条术语，并修订 7 条既有术语；新增内容主要覆盖核心技能、实体、状态、专名和 DLC 术语。
- DLC 首轮候选已通过受审计提取器处理 `ashes-urhrok`、`cults`、`orcs`，未直接读取受保护源码。
- 当前仍保留 3 条待审校术语：`Constrict`、`eldritch` 和 `Atmos Tribe`。
- 已保留翻译条目的 `source_tag`，并为术语补充 `T.*` 分类及语境说明。
- 核心与 DLC 规范 Lua 已完成一轮大批量术语统一和译文校正，并已连同回归测试提交冻结（commit `89744ab`），后续 finding 修订在冻结基线上分批提交，不能视为已发布版本。

### 工具链

- `doctor`、`extract`、`lint`、`status`、`merge`、`workset`、`context`、`proposal`、`review`、`build` 已统一到 `python3 -B tools/i18n` 入口。
- 审核流程：`tools/i18n review --scope code|translations` 显式生成只读 Pi 审核 bundle，`tools/pi-review --bundle` 严格校验 findings、分配宿主 `R-NNN` 并优先复用精确缓存，`tools/pi-remediate --bundle --review` 产生修订建议；修订需由主代理校验后应用，MVP 不自动执行模型建议。
- 构建工具现在支持最小 addon 覆盖层：官方已有且语义未改变的译文只计入继承统计，不写入插件。
- 显式指定组件时，例如：

  ```bash
  python3 -B tools/i18n build --profile addon --component tome --require-complete
  ```

  只检查所选组件，不会把未选择的 DLC、旧 lore 或 Nullpack 层算作不完整。
- addon 构建报告现在包含 `inherited_entries`、`override_entries`、`new_entries`，并对重复运行键进行去重。
- 所有工具报告和候选文件仍只写入被忽略的 `.artifacts/i18n/`。

### 本次发布边界决策

- 核心发布层固定为 `tome`，状态为 `releaseable`，继续使用 `build --profile addon --component tome --require-complete`；DLC 和外部覆盖层不再作为核心构建的隐式依赖。
- `ashes-urhrok`、`cults`、`orcs` 已登记受保护提取快照的哈希基线；`items-vault`、`possessors` 暂时忽略，保留规范译文但不再探测来源，也不计入 addon 候选或 DLC 发布层完整性。
- DLC addon 层当前仍为 `baseline-pending`：已有受保护快照哈希不能替代发布所需的可验证官方/源码基线。
- `legacy-lore-overlay` 与 `nullpackreloaded` 各自拆为独立可选外部层。当前不把 addon 仓库提交当作它们的官方源码基线，也不把它们计入核心发布完整性。
- 以上边界已写入 `i18n/versions/tome-1.7.6.json` 的 `release_layers`；后续严格构建需要按层选择并验证，不应通过忽略缺失来源来伪造全量通过。

## 三、最近验证结果

以下结果是当前工作区最近一次验证的基线：

- `doctor`：清单、Lua 5.1 / LuaJIT 2.1、LPeg 0.10.2 和受保护输入代理均正常。
- 单元测试：39 项通过，其中当前工作区新增 3 项安全/边界回归测试。
- 严格 lint：30,170 条翻译、653 条术语，0 个错误、0 个警告；`lint --strict` 已可作为当前门槛。
- lint 仍统计到 1,717 个重复运行键；这不是当前构建失败项，但仍需分类审校。
- 核心最小 addon：严格构建成功，19,023 个预期运行键全部验证通过。
- 核心补丁包含 1,391 个运行键：17,632 个官方已有译文继承不打包，1,382 个覆盖译文，9 个新增译文。
- 构建验证结果为 `missing=0`、`mismatched=0`、`unexpected=0`、`redundant=0`。
- 默认全量 addon 仍不能作为完整发布层；DLC 基线及可选外部层必须分别解决，不能借核心构建的成功宣称全量完成。

环境检查另有两个非阻断提示：公开引擎仓库因包含受保护输入而跳过通用 worktree 扫描；外部发布仓库 `tome-chn-mod` 当前存在工作区改动，正式安装或发布前必须先确认其归属。

### 审核闭环状态

- 主仓库已完成首轮全量 Pi 翻译审核：覆盖 609 个原始 translation bundle、30,170 条规范译文；累计报告记录 3,223 条 finding observation。
- 以稳定 `review_id` 去重并对缓存重放采用较晚裁决后，权威库存为 614 个 validated review observation、3,218 条 finding：2,816 条确认、146 条部分确认、247 条不采纳、9 条待语境裁决。
- review 工作树原队列中有 1,365 条与该权威库存精确关联；另有历史/代码审核观察，使原台账已处置总数为 1,425 条。
- 本次从尚未关联的 1,853 条中排除主仓库已裁决不采纳的 165 条，新增 1,688 条 `pending`：2 blocker、565 major、1,053 minor、68 note；其中 1,609 条确认、79 条部分确认。
- 同步清单为 `.artifacts/i18n/imports/pi-first-round-20260803/manifest.json`，完整差集为同目录的 `first-round-remaining-findings.json`；同时复制了 362 份 validated `review.json` 与 362 份绑定的有界 translation bundle，未复制 `raw-output.txt` 或含绝对源路径的 Pi 运行元数据。
- `remediation-queue.json` 现有 3,113 条：1,425 条为冻结前已处置、1,688 条为本次新增 pending；`remediation-ledger.json` 保留既有逐条处置记录并关联本次 import。首轮“发现”阶段已经完成，修订阶段正在推进（见下）。

### 审核闭环处置进度（2026-08-03 晚）

- 冻结批次：已处置的 1,425 条对应工作树改动已复跑严格 lint（0/0）、39 项测试和 `git diff --check` 后提交为 `89744ab`（8 个文件，+2,945/−2,673），与新增队列隔离。
- blocker：2 条全部处置（`303f788`）：R-002 删除 ShowPurchasable 中文末尾残留英文句并恢复“包括你自己”；R-007 补全 world-artifacts 的【待翻译】句并本地化 Veluca 为“维卢卡”。
- major：565 条全部处置（`d8d25db` 至 `c1c2771` 共 15 个批次，每批 40 条独立提交），覆盖 engine/boot/addon-dev/ashes-urhrok/cults/orcs/possessors/items-vault/tome 各组件；其中约 10 条经核验在冻结提交中已修复，按 `already_resolved` 记账，未重复改动。
- minor：803 条全部处置完毕（`020741b` 至 `9844f5a` 共 18 个批次：batch 6–21 每批 50 条 + batch 22 收尾 3 条），全部集中在 tome 组件；每批独立提交，个别条目经核验在先前批次已修复，按 `already_resolved` 记账，未重复改动。跨条目术语（如 Pyre Wars＝烈火战争、Wayist＝维网信徒、Infinite Dungeon＝无尽地下城、Pride＝部落）先更新 `terminology.tsv` 再统一同步。
- note：68 条全部处置完毕（`efebeaf` 50 条跨 6 组件 + `8494b5c` 18 条 tome），队列 `pending` 已清零。
- 队列终态：`remediation-queue.json` `pending=0`，`applied_pending_commit=2945`，`already_resolved=135`；`remediation-ledger.json` 已关联 2,795 条 finding 处置记录。
- 处置原则：每条 finding 以有界 bundle 的 source/target 为准独立核验（涉及公开机制时另核验固定源码），不直接照抄 Pi 建议；每批修改后运行 `lint --strict`（0 错误 0 警告）与 `git diff --check`，并在 `remediation-queue.json`/`remediation-ledger.json` 中逐条记账（`verification`、`verification_note`、`changes`）。
- 批次切分注意：生成批次时须从**当前 pending 列表**固定取 `[0:40]`/`[0:50]`，不得使用随列表缩短而漂移的 `[40n:40n+40]` 索引；此前曾因此系统性跳过条目，已通过剩余 pending 复核修正。
- 当前 pending 余量：871 条 = minor 803 + note 68；`queue summary.pending` 与 ledger `queued_bundle_findings_not_assessed` 同步维护。

## 四、待办事项

### P0：发布基线

- [x] 将核心 `tome`、DLC 和外部覆盖层拆为独立发布边界，并让核心层通过严格构建。
- [ ] 整理并提交当前术语、译文和回归测试批次；提交前对最终 diff 做一次有界独立复审。
- [x] 为当前 DLC 发布层中的 `ashes-urhrok`、`cults`、`orcs` 建立可验证的官方/源码基线（2026-08-04 extract 验证：快照 SHA-256 与 tDef 数与 manifest 一致）；`items-vault`、`possessors` 仅在重新纳入发布范围时恢复来源映射并补建基线。
- [x] 为 `legacy-lore-overlay` 固定来源、版本和归属组件（2026-08-04 调查：tome-chn-mod 与引擎公开源码均无独立 legacy-lore 实体，结论记录于 manifest external_requirements 与 i18n/README）。
- [x] 为 `nullpackreloaded` 固定源码来源和版本，或拆成独立可选插件（译文快照固定于 tome-chn-mod `8dd657d`：null_translation.lua 464 条目 + hooks/load.lua；上游 addon 版本未固定，保持 optional 层）。
- [x] 在发布仓库工作区干净且归属明确后，生成并独立验证核心发布 artifact（核心 addon 确定性重建 SHA-256 一致 `aa712264…`；产物经 LuaJIT 加载验证 4,158 条目；`tools/ci-gates.sh` 一键门禁 10 步全过）。

### P1：翻译质量

- [x] 清理控制标记、`@token` 大小写/缺失和格式差异等 lint 问题；当前严格 lint 为 0/0。
- [x] 同步首轮全面审核余量，建立 1,688 条待处理 finding 的本地快照、队列和台账关联。
- [x] 冻结已处置的 1,425 条工作树并形成可审核提交（`89744ab`），与新增队列隔离。
- [x] 处理 2 条 blocker（`303f788`）；每项均以有界 bundle、术语库及必要的固定公开源码独立核验，不能直接套用 Pi 建议。
- [x] 处理 565 条 major（`d8d25db`–`c1c2771` 共 15 批，每批 40 条独立提交并逐条记账）。
- [ ] 分组件处理 1,053 条 minor 和 68 条 note；高复用术语先更新 `terminology.tsv`，再同步规范 Lua。（进度：minor 250/1,053，note 0/68）
- [ ] 审定 `Constrict`、`eldritch`、`Atmos Tribe` 等多译法术语，并按术语库流程先改 TSV，再改 Lua。
- [ ] 检查 1,717 个重复运行键，确认是合法覆盖、历史重复，还是需要清理的冲突来源。
- [ ] 对每个 remediation 批次运行严格 lint 和定向测试、更新台账；全部完成后对最终 diff 做有界 Pi 复审，并为接受、修订或撤销的 finding 留下闭环证据。

### P2：流程与工程化

- [ ] 为默认构建、核心最小构建和基线缺失场景补充 CLI 集成测试。
- [ ] 建立持续集成检查：LuaJIT 加载、普通 lint、单元测试、核心 build，以及禁止受保护目录越界读取。
- [ ] 评估是否需要安全的人工审核后 apply 流程；当前 `merge`/`proposal` 只生成候选和校验结果，不会原地修改规范 Lua。
- [x] 新增的 `i18n/`、`tools/`、`tests/` 文件已纳入本次工具链提交；发布仍需单独执行。
- [x] 为受保护提取器陈旧输出、空编辑键和越界 merge report 路径补充回归测试；当前测试总数为 39。

## 五、推荐工作顺序

1. ✅ 已冻结已处置 1,425 条 finding 的工作树：复跑严格 lint、39 项测试和 `git diff --check` 后形成提交 `89744ab`，避免与新增队列混写。
2. ✅ 已处理 2 条 blocker（`303f788`），完成事实核验、译文修订、关联台账和定向验证。
3. ✅ 已将 565 条 major 按 `component + section + ordinal` 切成有界批次（15 批，每批 40 条）全部处理完毕，优先覆盖机制反转、参数/占位符、伤害类型、触发条件和长篇错配；每批独立提交并逐条记账。
4. ✅ 已处理 1,053 条 minor 与 68 条 note（1,053/1,053、68/68），队列 `pending` 清零；跨条目术语先走术语库流程，重复运行键在同批同步，但不得无证据全局替换。
4b. ✅ 与基线（相邻仓库 HEAD `84e5573`，即本分支基线）逐条对比后，发现早期批次约 14 条标记 `applied` 但条目未落盘的遗漏，已全部补修（`5d26960`，tome 8 / ashes 3 / cults 2 / engine 1 及标点统一 1 处），并全量复检确认除有意保留项外无遗漏。
5. 每批结束后更新 `remediation-queue.json`、`remediation-ledger.json` 和人类可读台账，运行严格 lint 与相关定向测试；涉及公开机制时记录固定 commit，涉及 DLC 时只使用已复制的有界规范 bundle。
6. 队列清零后运行完整 doctor、lint、39 项测试和核心严格 build，再对最终 diff 生成有界 Pi 复审；只有复审无未处置 finding，才更新为审核闭环完成。
7. 随后再审定 3 条 `review` 术语、分类 1,717 个重复运行键，并继续 DLC、legacy lore、Nullpack、CI 与发布基线工作。

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

## 七、当前分支与工作区范围

- 当前分支：`codex/review-findings-20260802`。
- 分支相对 `origin/master` 领先 70+ 个提交：原工具链/术语库/测试批次 10 个，加本轮 finding 处置 37 个（冻结 1 + blocker 1 + major 15 + minor 18 + note 2 + 遗漏补修 1，minor/note 批次中个别文件合并提交），加术语表系统工程与三轮 Pi 复审闭环 25+ 个。
- 本轮 finding 处置涉及文件：`engine.lua`、`mod-tome.lua`、`tome-ashes-urhrok.lua`、`tome-cults.lua`、`tome-orcs.lua`、`tome-addon-dev.lua`、`tome-possessors.lua`、`tome-items-vault.lua`、`mod-boot.lua`、`mod-example.lua`、`mod-example_realtime.lua`。
- 当前工作区干净（无未提交改动、无已暂存文件）；分支未配置 upstream，提交、推送和发布均尚未执行。
- 工作树状态快照：`remediation-queue.json` 的 `pending` 为 0（全部处置），`applied_pending_commit` 2,945、`already_resolved` 135；`remediation-ledger.json` 已关联 2,795 条处置记录。
- 已处置但未改动规范文件的条目（有意保留）共 168 条：`already_resolved` 135（已含修复/与源码一致/术语裁决/代码基线已修复）+ `false_positive` 33（不采纳，原因均记录在台账 `verification_note`）。
- 术语表系统工程（2026-08）：新增 `domain` 列（11 领域 + lint 白名单）、静态/动态审计、补录基础术语（资源/面板属性/免疫/高频词）、3 条 review 术语裁决、33+26 条同键多译统一、light 共享键裁决、重复运行键分类（1,717 全部跨文件合法重复）、`tools/scan_runtime_collisions.py` / `classify_runtime_keys.py` / `review_diff.py` / `pi-review-batch.py`。
- 三轮 Pi 复审闭环（2026-08-03/04）：diff bundle 复审 3 轮，major 66→54→21→0，全部处置（含裁决保留）；处置记录在 `.artifacts/i18n/terminology-audit/findings_review{1,2,3}*.json`；worker 调优测试见 `docs/pi-review-worker-tuning.md`（最优 6 workers，4.2× 加速）。

上述状态说明核心插件已通过本地发布门槛，首轮全量“发现”已完成并同步到 review 工作树；1,688 条新增 finding 已全部处置（blocker 2/2、major 565/565、minor 1,053/1,053、note 68/68），队列 `pending=0`；下一步按进度第 6 条执行队列清零后的完整 doctor、lint、39 项测试与核心严格 build，再对最终 diff 生成有界 Pi 复审，之后再审定 3 条 `review` 术语并分类 1,717 个重复运行键。DLC 与外部层仍不属于已完成发布范围。
