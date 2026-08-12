# 第二轮术语审核正式交接文档

更新时间：2026-08-11

状态：**P0–P4 全部批次已收束（P4：198 撤销 + 3 确认 + 1 advisory，无已确认 finding；全批次仅 P0 12 根问题与 P2 Foul Convergence 为已确认 finding 且均已修复）**

本文件是当前第二轮术语审核工作线的正式交接入口。接手者应先阅读本文件、根目录 `AGENTS.md`、`docs/terminology-review-round-2.md`，再按本文“下一步”继续。所有尚未明确确认的 observation 不得直接进入 remediation。

---

## 1. 工作线、目标与停止点

- 工作分支：`audit/terminology-review-round-2`
- 基础：`develop` / `a781a35`
- 工作目标：审核现有汉化的术语**完整性、合理性、一致性**，并在独立裁决后分批修复。
- 当前停止点：P0–P4 全部收束。P4 workset（521 候选/291 需人工/20 抽样/189 行）冻结，blind discovery（66 bundles/618 items/202 observation）与分组源码裁决完成：198 撤销 + 3 确认 + 1 advisory（Dreadfell），**无已确认 finding**。全批次裁决完成，下一步：完整门禁 + 构建 smoke + 一轮独立只读复审（handoff 7.4）。
- P0 已修改 `terminology.tsv` 与规范 Lua，完整修订与验证结果见 5.5–5.7；后续不得重新打开已退出的 P0，除非出现新的源码证据或回归。
- P1 当前仅完成审核第一阶段，没有修改 TSV 或规范 Lua；pending observation 不得进入 remediation。
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
   - 已加入 r2 inventory：`build_candidate_units`、`annotate_units`、`_coverage_totals`、`run_terminology_inventory`、`run_projection`；
   - 已生成内容寻址的 `P1-role-structure-v1.json`，绑定生成器源码、TSV、组件、baseline、inventory 与 exclusions 摘要，并固定自动排除抽样。
3. 已生成以下忽略目录报告；`.artifacts/` 不受版本控制，换机或重新克隆后须由当前规范输入重建，不能假定历史文件仍存在：
   - `baseline.json`
   - `candidate-inventory.json`
   - `coverage.json`
   - `exclusions.json`
   - `projection-candidates.json` / `projection-candidates.md`
4. 历史 P0 环境曾提取源码注册表：
   - `source-registries/damage-effect-registry.json`
5. 历史 P0 环境已生成 blind translation semantic v2 审核 bundle，并完成审核：
   - 47 bundles
   - 455 items
   - 108 items 产生 observation
   - 114 findings
   - 0 bundle 失败
6. 当前宿主已修复 translation v2 匿名 cwd 与 Facts-study Node identity 的 Linux/macOS Homebrew 兼容路径，并移除不符合 claim-bound 契约的实验 `translation-reviewer`。最终完整门禁（含 quality/Facts、术语审计和 core addon strict build）全部通过，记录：`.artifacts/i18n/ci-gates/run.HhGfyo`。

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
- 完整门禁与全新只读复审随后已在 5.7 完成，不再列为待办。

## 5.6 子代理复审与用户裁决（2026-08-10）

- P0 曾临时使用源码感知 `translation-reviewer` 做逐条核验；该实验 agent 不属于
  `AGENTS.md` 正式声明的 scout/plan-reviewer 项目 subagent，也不满足 translation v2
  claim-bound verifier 契约，定义现已移除，后续批次不得继续调用。
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
- 下一步：P1 角色结构；当前规范输入重新冻结后的实际分母见 7.1。

## 6. 当前版本控制状态

本次进度提交包含：review v2 匿名 cwd 跨宿主修复、Facts-study Node runtime identity
兼容、P1 workset 生成与测试、实验 `translation-reviewer` 移除、契约/经验文档及本交接更新。
P1 semantic discovery 仅写入被忽略的 `.artifacts/`，没有修改 `terminology.tsv` 或规范 Lua。

完整裁决和审核结果不会随 Git 分支迁移；若当前宿主缺少对应文件，应从固定版本和当前
规范输入重建，不得伪造或沿用失去 lineage 的旧 artifact。接手时仍须重新记录
`git status --short`、`git diff --name-only` 与 `git diff --stat`，区分本提交后的新改动。

---

## 7. 接手后的下一步

### 7.1 P1 基线已冻结（2026-08-11，TSV scope 修正后重建）

本地生成器已从当前规范输入写出：

`.artifacts/i18n/terminology-review-r2/worksets/P1-role-structure-v1.json`

- artifact SHA-256（2026-08-11 重建）：`6321e1074dbaea0c75bfd82b25e8c4b83be39fa5ecf1053909925403a25b10ec`（旧 `af499642…` 已失效）
- 候选单元 1,066：已登记 239（+2）、缺失 827（−2）、自动排除 240、需人工 587（−2）；
- 人工候选分布：talent type 275、talent category 9、birth descriptor 38、faction 10、
  entity type 64、entity keyword 193；
- 现有术语行复核 204；provisional `entity keyword` 总体 434；
- 自动排除总体 240，按 `sha256(component, source, source_tag)` 固定抽样 20 条；
- workset 绑定 baseline、inventory、exclusions、TSV 与全部组件 SHA-256。

该步骤只冻结工作集和证据需求，没有修改 TSV 或规范 Lua。规则或规范输入变化后必须
重建 artifact 并更新摘要，旧 SHA 不得继续使用。

### 7.2 P1 blind semantic discovery 已完成（2026-08-11）

选择把 589 个未登记人工候选、204 条现有术语行的活动匹配和 20 条自动排除抽样映射到
规范译文 revision；按 revision 去重后覆盖 9 个组件、1,425 items、147 bundles。两个现有
TSV 行当时无活动匹配、未进入 bundle（2026-08-11 已核验并修正 scope：L428→core、
L538→dlc，见 7.3 第 1 步）。

外发留痕（项目级 translation v2 授权）：

- provider/model/thinking：`opencode-go` / `deepseek-v4-flash` / `high`；
- contract/channel：`tome4-translation-review-bundle-v2` / `semantic-observation`；
- review ID：`4f11ef0ef9bf388fb822fdcc9fb1efbe1c152ef34c1e6c533e106728a9cdc2f3`；
- 初始选择：147 bundles、1,425 items、165,549 item 字符、1,280,539 artifact bytes、
  257,750 provider payload bytes、0 oversized；
- 实际执行：147 bundles 全部成功；2 次首次输出结构不合规后重试，因此共 149 次
  charged-or-possible transfers、261,278 charged-or-possible payload bytes；
- reviewer payload 仅含 `revision_id/source/target`，没有 terminology、Facts、历史 finding、
  workset lineage、源码路径或工具上下文。

冻结结果：

- `.artifacts/i18n/terminology-review-r2/p1-review/observations.json`
- SHA-256：`dce24259756f84cfb42d731e48fa7495ea4ec623544b9dfeb242233d613a0ac6`
- assessed 1,419、context-insufficient 6、pending observations 329、manual queue 334；
- 329 条 observation 涉及 320 个 revision、239 个唯一 `(source,target,source_tag)` 组；
- observation tag 分布：birth descriptor 27、talent type 128、talent category 23、
  faction 5、entity type 48、entity keyword 98；
- context-insufficient：`Anorithil→星月术士`、`cun→灵巧`、`shalore→永恒精灵`、
  `thalore→自然精灵`、`yeek→夺心魔`、`drolem→龙傀儡`。

所有 observation 的 disposition 仍为 pending、severity 为 null；当前没有 P1 已确认
finding，不能进入 remediation，也不能把 329 当作错误数。

### 7.3 下一步：P1 独立裁决与修复闭环

1. ✅ **前置核验已完成（2026-08-11）**：6 条 context-insufficient（Anorithil/cun/shalore/
   thalore/yeek/drolem）经固定版本源码核验全部确认（support），与官方 zh_hans 逐字
   一致且游戏内显示机制均已验证；L428/L538 均属 scope 标注错误（target 与条目有效），
   已获用户授权修正 TSV scope（`ammo→core`、`Orc→dlc`），workset 重建
   （SHA `6321e107…`）、QualitySampling 黄金值随 TSV 输入同步更新。记录：
   `decisions/P1-context-insufficient-and-stale-rows.md`；门禁 1–5 全部通过
   （lint 0 错、单测 439、collision 0、桶 A 1711、diff --check OK）。
2. ✅ **P1 分组源码裁决已完成（2026-08-11）**：329 条 observation 按
   faction name → birth descriptor → talent category → talent type → entity type →
   entity keyword 分组，绑定固定版本源码逐条核验。239 个唯一组合：216 官方一致
   （core+3 DLC 官方 zh_hans 合并表）、15 偏离官方、8 官方无条目（possessors 未 pin
   源码，按规范译文语境评估）。**裁决：322 条撤销、7 条 advisory（5 组合：
   spiderkin/Manifold/doom/deep horror/Possessor），0 已确认 finding**。关键源码证据：
   earthen vines（"Control the stone itself…"）、mechstar（mindstar+steamtech）、
   paradox 资源条（紊乱值）、spell/infusion（官方"纹身"混淆两类）等。记录：
   `decisions/P1-adjudication.md`（含逐条映射 `P1-adjudication.json`）。
3. ✅ findings 清单已冻结：无已确认 finding，不进入 remediation；advisory 仅记录。
4. ✅ **advisory 修复已完成（2026-08-11，用户授权）**：5 个组合全部修复——
   spiderkin→蜘蛛族（mod-tome.lua×3）、Manifold→多样（mod-tome.lua+TSV L310）、
   doom→末日（tome-cults.lua+TSV L213，对齐官方）、deep horror→深邃恐惧
   （tome-possessors.lua）、Possessor→占据者（tome-possessors.lua+TSV L405）。
   门禁 1–5 全部通过（lint 0 错、单测 439 全绿、collision 0、桶 A 1711、diff --check
   OK）；术语审计三件套通过；QualitySampling 黄金值随 TSV/Lua 输入同步更新（已验证
   归因）；workset 重建（SHA `65b4050b…`）。
5. ✅ **修复后全新只读复审已完成（2026-08-11）**：生成绑定新 revision 的 blind bundle
   （3 bundles/7 items，`.artifacts/i18n/runs/P1-advisory-review/`），provider
   `opencode-go`/`deepseek-v4-flash`/high，2 次首次输出不合规后重试共 5 次
   charged transfers。结果：tome 0 observation、cults 1（doom 撤销）、possessors 1
   （Possessor 撤销）、Manifold context-insufficient（主代理补上下文后确认）。
   **无新增已确认 finding，P1 退出条件满足**。记录：`decisions/P1-advisory-review.md`。

**P1 正式收束**。P2 进度：workset 冻结（`P2-talents-v1.json`，SHA `f066d648…`）；
blind discovery 完成（196 bundles/1,903 items，外发留痕见 `decisions/P2-adjudication.md`，
SHA `241e65aa…`）；分组源码裁决完成（851 撤销/5 advisory/1 已确认：Foul
Convergence→阴险同谋，建议“污秽夹击”），记录：`decisions/P2-adjudication.md` +
`P2-adjudication.json`。修复（2026-08-11，用户授权）：`Foul Convergence→污秽夹击`
（tome-cults.lua + TSV 新增行），门禁 1–5 与术语审计全部通过（TSV 行数 705→706、
QualitySampling 黄金值同步更新），workset 重建（SHA `4b254b67…`）；全新只读复审
（1 bundle/1 item，`P2-fix-review/`）：1 observation 撤销（源码机制“both teleport
and make a melee attack”=夹击，官方同译）。**P2 收束，无新增已确认 finding**，
记录：`decisions/P2-fix-review.md`。P3 进度（2026-08-12）：workset 冻结
（`P3-entities-v1.json`，SHA `e254a498…`）；blind discovery（296 bundles/2,828
items，外发留痕见 `decisions/P3-adjudication.md`，observations SHA `b12f06c7…`）；
分组源码裁决：745 撤销 + 33 确认（CI 补上下文，含 `long→很长的` 主代理直接核验），
**0 已确认 finding**（32 偏离中本仓库优占多数：d.steel/宝石标准译名/vial 系列等）。
记录：`decisions/P3-adjudication.md` + `P3-adjudication.json`。P4 进度（2026-08-12）：workset 冻结
（`P4-narrative-v1.json`，SHA `fbf555aa…`）；blind discovery（66 bundles/618 items，
observations SHA `01eec7f7…`）；分组源码裁决：198 撤销 + 3 确认（Infinite x40/50、
?...secar 加密 lore）+ 1 advisory（Dreadfell），**0 已确认 finding**。记录：
`decisions/P4-adjudication.md` + `P4-adjudication.json`。**P0–P4 全部批次裁决完成**。
下一步：完整门禁 + 构建 smoke + 一轮独立只读复审。

### 7.4 后续批次

- 依次处理 P2–P4；每批先冻结 observation，再集中修复。
- 对 projection 候选持续统计误报并收紧规则；复核 B 类自动排除样本。
- 全部批次结束后运行完整门禁、构建 smoke 和一轮独立只读复审。

---

## 8. 交接原则

- 审核子进程只能提供 proposal/findings/observation，不得直接写规范 Lua。
- 主代理负责源码核验、确认状态、严重度、修复范围和最终应用。
- partial/pending 项不得进入 `tools/pi-remediate`。
- 未经用户授权不得向翻译 v2 bundle 以外的 provider 发送任务、计划、代码或其他 artifact。
- 不得为了追求“零 advisory”而无限扩展审核范围；满足最终复审无新确认 finding 即可收束。
