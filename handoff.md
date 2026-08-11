# 第二轮术语审核正式交接文档

更新时间：2026-08-10

状态：**P0 已退出（修复+门禁+全新只读复审完成，无新确认 finding）；下一步 P1**

本文件是当前第二轮术语审核工作线的正式交接入口。接手者应先阅读本文件、根目录 `AGENTS.md`、`docs/terminology-review-round-2.md`，再按本文“下一步”继续。所有尚未明确确认的 observation 不得直接进入 remediation。

---

## 1. 工作线、目标与停止点

- 工作分支：`audit/terminology-review-round-2`
- 基础：`develop` / `a781a35`
- 工作目标：审核现有汉化的术语**完整性、合理性、一致性**，并在独立裁决后分批修复。
- 当前停止点：P0 清单已完成一轮源码核验和独立裁决；**没有修改 TSV、规范 Lua 或译文**。
- 后续修复需要主代理按 finding 建立有界任务，并在用户授权后执行；不得因本文件已有确认结论而自动修改。
- 不得创建 commit 或 checkpoint，除非用户明确授权。

历史工作线 Evaluator/Facts Study/addon 0.2.5 已收口，不属于本轮交接范围；其结论见历史文档，不应重新打开。

---

## 2. 固定基线与审核边界

### 2.1 版本基线

- 游戏版本清单：`i18n/versions/tome-1.7.6.json`
- 核心源码固定提交：
  `624a67329fe2ad440c5b344785a9c73fcf22ae63`
- DLC 源码：公开正式版 1.7.4（Ashes of Urh'Rok、Cults of Entropy、Embers of Rage）
- 机制判定原则：以固定版本源码实际行为为准；现有译文、术语表和模型 observation 不能覆盖源码事实。

### 2.2 本轮审核范围

- A 类权威注册表：
  - damage type：205 条
  - effect subtype：238 条
- 现有术语表相关行：107 条
- candidate inventory：7,490 个去重候选单元
- 长文本 projection 候选：369 条
- P0 workset：`.artifacts/i18n/terminology-review-r2/worksets/P0-core-v2.json`

B 类描述性字符串、单次出现的内部键和长文本投影候选不能仅凭候选命中自动登记。机制关键标签仍需人工判断。

---

## 3. 已完成的工具链工作

1. `docs/terminology-review-round-2.md`
   - 定义 A/B/C 分类、P0–P4 批次、证据 rubric、投影精度策略、分工边界和退出标准。
2. `tools/audit_dynamic.py`
   - 已加入 r2 inventory：`build_candidate_units`、`annotate_units`、`_coverage_totals`、`run_terminology_inventory`、`run_projection`。
3. 已生成并保留在忽略目录 `.artifacts/i18n/terminology-review-r2/` 的报告：
   - `baseline.json`
   - `candidate-inventory.json`
   - `coverage.json`
   - `exclusions.json`
   - `projection-candidates.json` / `projection-candidates.md`
4. 已提取源码注册表：
   - `source-registries/damage-effect-registry.json`
5. 已生成 P0 blind translation semantic v2 审核 bundle，并完成审核：
   - 47 bundles
   - 455 items
   - 108 items 产生 observation
   - 114 findings
   - 0 bundle 失败
6. 测试和静态检查此前已通过：
   - `tests/i18n/test_toolchain.py`
   - `tests/i18n/test_terminology_inventory.py`
   - `git diff --check`

本次仅更新交接文档；翻译批次门禁（`lint --strict`、运行键扫描等）应在后续实际修复收束后统一运行，不因本次文档变更重复执行全量门禁。

---

## 4. P0 审核输入及外发留痕

P0 预审核使用项目已授权的 translation v2 blind bundle：

- provider：`opencode-go`
- model：`deepseek-v4-flash`
- thinking：`high`
- bundles：47
- items：455
- item 字符数：53,691
- artifact 总字节数：375,263
- 实际 provider payload：83,400 bytes

本次主代理独立裁决**未调用 provider**。Pi 输出仅提供 `assessment_state`、语义观察和 source/target evidence；确认状态、严重度、是否修复均由主代理独立决定。

完整预审核汇总：

- `.artifacts/i18n/terminology-review-r2/p0-review/summary.json`
- `.artifacts/i18n/terminology-review-r2/p0-review/summary.md`
- `.artifacts/i18n/terminology-review-r2/p0-review/bundle-manifest.json`

---

## 5. P0 独立裁决结果

正式逐条裁决记录：

`.artifacts/i18n/terminology-review-r2/decisions/P0-observation-adjudication.md`

该文件包含审核模式、源码依据、逐组理由、全部 observation 编号和后续处理限制。

### 5.1 数量结论

| 裁决 | observation 数 | 说明 |
|---|---:|---|
| 已确认 | 16 | 归并为 12 个根问题，可在授权后进入有界修复 |
| 部分确认 | 17 | 保留为 pending/advisory，不得直接 remediation |
| 撤销 | 81 | 不构成已确认 finding |
| 合计 | 114 | 与 P0 summary 一致 |

### 5.2 已确认根问题

| 根问题 | observation | 核心结论 |
|---|---:|---|
| `gloom effects` | 001 | `% chance of gloom effects` 实际随机施加 confusion、stun、slow，不是施加一个黑暗光环 |
| `aging temporal` | 004 | 译文保留 aging，漏掉 temporal 伤害/效果维度 |
| `debilitating acid` | 017 | `debilitating` 被改成 corrosion，改变修饰语语义 |
| `draining physical` | 023 | 源码是从目标汲取并治疗施法者，“物理吸收”方向不清且易反向理解 |
| `item antimagic scouring` | 034 | 源码降低 effective powers，不是灼烧 |
| `manaburn arcane` | 035、040 | `burnArcaneResources` 同时处理 mana、vim、positive、negative，不能限缩为法力 |
| `pulse detonator` | 047 | 与 `shock grenade` 混译；同 DLC 已有“脉冲爆弹”语境 |
| `cut` / `bleed` | 074–077 | 源码将 `cut` 作为独立的 `canBe("cut")` 类别，不能和 `bleed` 都译成“流血” |
| `horror` effect subtype | 089 | effect 类别不是生物实体“恐魔” |
| `power` effect subtype | 099 | 源码表示各种 power 强度，不是 energy |
| `superiority` | 108 | 源码为 superiority/高级战技类别，“战术优化”无充分语义依据 |
| `technique` | 109 | 该 subtype 也用于射击效果，译成“格斗”错误收窄 |

### 5.3 部分确认项目

以下编号暂不进入自动修复：

```text
002 009 010 011 012 014 020 032 033 036 037 041 057 058 086 102 103
```

这些项目主要涉及幻想专名、复合词的汉语重排、内部类别名是否需要展开，以及同一 subtype 在不同 effect 中的语境差异。详细理由见裁决文件。

### 5.4 已撤销项目

其余 81 条 observation 已撤销。典型误判来源：

- 把项目既有术语（如 `acid→酸性`、`blight→枯萎`、`darkness→暗影`、`temporal→时空`、`stun→震慑`、`infusion→纹身`）当作字面错误。
- 把汉语复合词的自然顺序变化当作 source/target scope 错误。
- 忽略源码已经支持译文中的具体机制，例如 armor sunder、生命汲取、经验倒退、火焰/燃烧磷和 flat damage reduction。
- 未读取 effect family，因而把 `gloom`、`veil`、`race` 等类别名的上下文译法误判为词典式错误。

---

## 5.5 P0 修复完成（2026-08-10，用户逐条确认后）

- 用户裁决：10 个根问题接受（001/004/017/023/034/047/089/099/108/109）、2 个拒绝
  （cut/bleed、manaburn，记录于 `decisions/P0-user-rulings.md`）。
- 译文 11 处 + TSV 12 行已修改（详见裁决记录）；`% chance of gloom effects` 记
  A 类排除理由（内部描述名，仅修译文）。
- power/superiority 同源多译以多行 TSV 记录语境，dynamic audit multi 回落 28。
- 验证：lint --strict 0 错误、审计三件套通过、466 项单测通过、`git diff --check` 通过。
- 待办：P0 批次收束后的完整门禁（运行键扫描/重复键分类）+ 重新生成 bundle 做一轮
  全新只读复审。

## 5.6 子代理复审与用户裁决（2026-08-10）

- 新增 subagent `translation-reviewer`（`.pi/agents/translation-reviewer.md`，
  deepseek/deepseek-v4-flash，只读逐条源码核验审阅，输出 verdict findings）。
- 对 partial 17 + 撤销 81 = 98 条复审：94 support、4 new_evidence、0 overturn。
  81 条撤销中 79 条与官方 zh_hans 逐字一致；#114 veil 语境声明与源码吻合。
  记录：`decisions/P0-re-review-subagent.md`。
- 用户裁决 4 条 new_evidence：#20 对齐"时空锚"（已改译文+登记 TSV）、
  #83 统一"固定伤害减免"（已改译文+登记 TSV）、#103/#80 维持现状。
- 子代理未改动工作树（复验）；agent 集合测试已同步。

## 5.7 P0 退出（2026-08-10）

- 完整门禁通过：lint 0 错误、单测 466 项、scan_runtime_collisions=0、
  classify_runtime_keys 桶 A 1711 合法、git diff --check。
- 修复后重审：47+2 bundle 全部成功（1 个 bundle 模型输出不合规 3 次，拆 5+5 子集
  重审通过）；455 条目 110 findings（修复前 114）。
- 修复条目残留 8 条 observation 全部裁决撤销（机制/约定支持，组A/组C 判例）；
  记录：`decisions/P0-exit-review.md`。**P0 退出，无新确认 finding。**
- 下一步：P1 角色结构（talent category/type 591 需人工 + entity keyword 434 provisional
  归属核验 + 现有行 202）。

## 6. 当前版本控制状态

交接时工作树已有以下未提交改动；这些改动不得被清理、重置或顺手格式化：

```text
 M .agents/skills/tome4-pi-review/SKILL.md
 M AGENTS.md
 M docs/terminology-review-round-2.md
 M handoff.md
```

本次交接新增/更新的完整裁决文档位于被忽略的 `.artifacts/` 下，不会出现在 `git status`：

```text
.artifacts/i18n/terminology-review-r2/decisions/P0-observation-adjudication.md
```

没有修改规范翻译 Lua、`terminology.tsv`、游戏源码或发布 addon。

---

## 7. 接手后的下一步

### 7.1 用户/主代理先确认

1. 确认是否接受 16 条已确认 observation 作为 P0 修复范围。
2. 对 17 条 partial 项决定：保留现译、另立 advisory，或纳入人工术语裁决。
3. 确认是否把内部描述名（如 `% chance of gloom effects`）仅作为 B 类排除项，还是另行修订其玩家可见文本。

### 7.2 授权修复后

按根问题而非按单条 observation 批量处理：

1. 先更新 `terminology.tsv`（如需新增/修改高复用术语）。
2. 再修改对应规范 Lua，保留正确的 `source_tag` 和 `T.*` category。
3. 每批只处理已确认 finding，禁止扩展到 partial 或无关风格重构。
4. 运行单批最小核验：LuaJIT 加载、对应 lint、`git diff --check`。
5. P0 批次收束后运行完整门禁：

```bash
python3 -B tools/i18n lint --strict
python3 -m unittest -q tests/i18n/test_toolchain.py
python3 -B tools/scan_runtime_collisions.py
python3 -B tools/classify_runtime_keys.py

git diff --check
```

6. 若改动术语表，额外运行：

```bash
python3 -B tools/audit_static.py
python3 -B tools/audit_dynamic.py
python3 -B tools/annotate_domains.py
```

7. P0 修复完成后重新生成 bundle，进行一轮全新的只读复审；只有没有新的已确认 finding 才能退出 P0。

### 7.3 P0 之后

- 依次处理 P1–P4；每批先冻结 observation，再集中修复。
- 对 projection 候选进行误报抽样和规则收紧；当前试点误报约 45%，目标阈值为 60%。
- 复核 B 类自动排除样本（至少 5% 或每批至少 20 条）。
- 继续处理 entity keyword 的源码归属（434 个 provisional 单元）。
- 最终运行完整门禁、构建 smoke 和一轮独立只读复审。

---

## 8. 交接原则

- 审核子进程只能提供 proposal/findings/observation，不得直接写规范 Lua。
- 主代理负责源码核验、确认状态、严重度、修复范围和最终应用。
- partial/pending 项不得进入 `tools/pi-remediate`。
- 未经用户授权不得向翻译 v2 bundle 以外的 provider 发送任务、计划、代码或其他 artifact。
- 不得为了追求“零 advisory”而无限扩展审核范围；满足最终复审无新确认 finding 即可收束。
