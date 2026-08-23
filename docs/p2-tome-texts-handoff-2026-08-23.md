# P2 核心文本复核交接（2026-08-23）

> 类型：收尾记录，非契约、非门禁。
> 权威路线仍见 [`project-roadmap.md`](project-roadmap.md)；Paseo 编排与语境审核契约见
> [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md)（2.18-draft）与
> [`paseo-translation-context-review-v1-contract.md`](paseo-translation-context-review-v1-contract.md)。

## 0. 一句话状态

`p2-tome-texts-b<N>` 轨道已完成 5 个译文批次（2026-08-22 至 08-23）：核心 `mod-tome.lua` 的
`data/texts/intro-*`、全部 `unlock-*`、`data/talents/misc/inscriptions.lua` 全段，以及教程／帮助
文本 part A。共复核 **246 个 `t(...)` 对**，修订 **97 个 section**，语境审核确认并修复
**45 个 finding**；所有提交均在本地 `develop`，**未 push、未发布**。

## 1. 批次结果

| 批次 | 口径 | 条目 | 修订区块 | confirmed finding | 提交 |
|---|---|---:|---:|---:|---|
| b1 | `data/texts/intro-*.lua`（18 区块） | 18 | 14/18 | 9 | `5efe265` |
| b2 | `unlock-*.lua` 前 22 区块（adventurer…mage_geomancer） | 44 | 20/22 | 9 | `ff25042` |
| b3 | `data/talents/misc/inscriptions.lua` 全段 | 120 | 17 对 | 4（另 2 条撤回） | `1feed76` → 修正 `9097c6f` |
| b4 | `unlock-*.lua` 其余 21 区块（mage_necromancer…yeek） | 42 | 18/21 | 10 | `f3c6bba` |
| b5 | 教程关卡说明、stats1–9、最后的希望来信（21 区块） | 22 | 16/21 | 7 | `888fc54` |

finding 数只计语境审核（`translation_contextual_v1`）中宿主裁决为 confirmed 的观察；EXECUTOR 在
读-改阶段直接修正的条目（每批 25–75 行）另见各批次 `evidence/quality/p2-batches/*-host-verification.json`
的 `adjudicated_findings` 与 `items`。每批的工作集冻结文件同目录，均记录 `fixed_source_identity`
（`commit:624a673…`）与逐条 `pinned_source_match`。

典型修正：Point Zero「使时空法术得以存在」（原译为「时空行者方能进入」）；竞技场／无尽地下城
「没有出口」被译成「只有一个出口」；转化之盒凭空多出「无法储存能量」；时空守卫「中型与小型武器」
被译成「或」；堕落者「死星之力」被译成重力；纹身 Wild「减少受到的伤害」；Rune of Vision／
Dissipation 的 `args_order` 误判（见 §3）；最后的希望第二封来信整句遗漏「请务必调查」。

## 2. 本轮基础设施变更（已独立提交、交叉复审）

| 提交 | 内容 |
|---|---|
| `7085a98` | `contextual_anchor_preflight.py` 接受 `ordered_titles: []` 的 whole-section window（契约 2.17-draft）。b1 首次消费 2.16 preflight 时发现其只能表达 Fay Willows 式章节标题锚点，对任何无章节标题的 section 都无法构造合法 SCOPE。 |
| `a2e86d4` | preflight 读取 `t()` 第四参数 `args_order`（规范形式 `{i,j,...}`，接受 `;` 与尾随分隔符），并要求 `bounded_context.context` 精确披露 `args_order={...}` 标记，否则 fail closed（契约 2.18-draft；标记入 `paseo_contract_check` 与 toolchain inventory）。 |
| `90acafe` + `d347d52` | 术语表新增 `Keeper of Reality=现实守护者`、`Wayist=维网信徒`；`d347d52` 修复 `90acafe` 未同步 `test_real_terminology_is_fully_mapped` 的 708→710 行数而导致的红 HEAD。 |

## 3. 必须知道的教训

1. **`args_order` 是一等机制。** `t(source, target, tag, {2,1})` 的第四参数在运行时重排格式参数；
   `mod-tome.lua` 中有 51 条。lint 的 `format-mismatch` 已按 `args_order` 校验转换序列。b3 曾把
   两条带 `args_order` 的条目误判为「占位符顺序缺陷」，并在改写文本后遗留 `{2,1}`，引入真实回归
   （`1feed76`），随即由 `9097c6f` 修正、`779a4d3` 撤回证据中的两条 finding。任何重排译文占位符
   都必须同时更新或删除 `args_order`；宿主与 reviewer 检查占位符顺序时必须读取第四参数。
2. **术语行变更后必须重跑完整 toolchain 单测。** `tests/i18n/test_toolchain.py` 硬编码术语行数
   （现为 710）与 orchestrator.md 标记清单；只跑 preflight 或审计脚本会漏掉它。
3. **共享 runtime key 的术语修正会触发跨组件碰撞门禁。** b3 的「相位之门」落在与
   `tome-ashes-urhrok.lua` 共享的 `logPlayer` 键上；按 `docs/runtime-key-collisions.md` §3.3 先例，
   以 SPEC 修订把 DLC 行对齐为相同译文，而不是回退术语。
4. **reviewer 每轮重看整段。** 长段落通常需要 2–3 轮 FIX／复审才能收敛；这是正常成本，不要跳过
   复审。
5. **结果校验要机械化。** 从 Paseo activity 取回完整 JSON，按冻结 envelope 逐条 byte-compare
   evidence、顺序与 identity（b3 起已如此），不要目测。
6. **不要在工作树上用空的 `git stash`/`stash pop` 对。** 本轮一次 smoke test 误弹出了前一会话的
   stash；已折回 `stash@{0}`（README 链接 + `dependencies/` + `docs/container-dependency-inventory.md`），
   `stash@{1}` 为更早的 `infra-contract-008…` WIP，均未并入任何提交，去留由维护者决定。

## 4. 未完成与下一步

- **batch 6（已定范围、未启动）：** `data/texts/tutorial/stats*/` 其余 50 条单对 section
  （calc0–11、scale1–12、tier0–12、timed0–8、tactics1–2、talents、terrain）。它们是数值密集的
  战斗属性课程（公式、百分比、算例），EXECUTOR 简报应要求每个数字对照固定实现核验。
- 之后候选：`data/chats/`、`data/lore/` 的有界切片；roadmap 仍规定不自动启动。
- 已知 advisory（未改）：教程 intro「Tales of Maj'Eyal」作 ToME 4；竞技场标题「挑战主宰」；
  Vim 定义句用「活力」；岩石守卫「分身」。`Maj'Eyal` 在文件内 马基·埃亚尔／马基埃亚尔 并存，
  只在批次内统一，不做全局替换。
- P3 事项不变：`develop → master` PR、正式 release、teaa／te4.org／创意工坊发布均需新指示。

## 5. 单批操作清单（b5 实际流程）

1. 冻结工作集到 `evidence/quality/p2-batches/<batch>.json`：逐条用 `git show 624a673:<path>` 核验
   英文键，并记录每个调用的 `args_order`。
2. 写 `.ai/task/<task>/SPEC.md|PLAN.md|STATE.json`（schema 3、`change_class: standard`、
   `review_contracts: ["translation_contextual_v1"]`）。
3. EXECUTOR（Luna，`auto-review`/xhigh）读-改；宿主核验范围、英文键零变更、行结构，归档。
4. `SCOPE.json`（每个 section `ordered_titles: []`）→ 七键 payload（`bounded_context` 对带
   `args_order` 的调用写入 `args_order={...}`）→ `tools/contextual_anchor_preflight.py` →
   紧凑规范 envelope → REVIEWER（Sol）按契约第四节三行 prompt 派发，labels 含
   `candidate_identity`/`dispatch_id`。
5. 取回 activity 原文机械校验；宿主按固定源码裁决；confirmed 进 fresh EXECUTOR FIX，重新冻结
   envelope 复审，直至全部 OK。
6. 五步门禁 + `tools/ci-gates.sh`（含构建）→ 宿主核验记录 → `ai_state_check.py` DONE →
   单独提交译文批次；roadmap/记忆随后单独提交。
