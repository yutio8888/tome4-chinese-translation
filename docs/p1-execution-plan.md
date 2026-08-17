# P1 核心译文优化执行规划

> 状态：执行规划，记录日期 2026-08-17。
> 上位文档：[`project-roadmap.md`](project-roadmap.md) §3。本文只把 roadmap §3.1–§3.3 的
> 原则落成可执行的批次定义、选择规则、命令序列和验收条件，不修改 roadmap 的阶段划分、
> 不新增契约、不授权 push 或发布。
> 本文不授权任何 provider 调用；每个批次的外发仍按 `AGENTS.md`「外发边界」逐次执行。

## 一、前提与已核实事实

以下事实在撰写日已核实，是本规划成立的基础；任何一项变化都要求重新评估批次定义。

**1.1 三项确定性输入当前都不产生待译批次**（roadmap §3.1）

- Tome 1.7.4 → 1.7.6：`added = 0`、`source-changed = 0`；
- 未解决 accepted finding = 0；
- `untranslated-existing = 100` 已按固定源码 commit `624a673` 逐条裁决，玩家可见可译自然
  语言为 **0**，该队列已关闭。

因此 P1 首批不是"翻译未译内容"，而是**对已译内容的有界质量核查**。这是 P1 迟迟没有推进的
真正原因：一直在等一个不会出现的待译队列。

**1.2 当前 revision inventory（2026-08-17 运行）**

```text
tools/i18n quality inventory   →  entries=32437  occurrences=30308  sha256=5ed11d8f62db1d47
component: tome 23294 / orcs 4161 / cults 2235 / engine 1061 / ashes-urhrok 914 / 其余 746
tome profile: mechanics 6941 / ui 7059 / dialogue 1973 / term-name 1554 / narrative 1196 /
              runtime-log 1620 / unknown 2951
```

**1.3 已存在但无归属的两份 artifact**

- `.artifacts/i18n/p1/batch1-visibility-triage.json` —— 100 条 `untranslated-existing` 的
  可见性三方核验记录，是 §1.1 第三条裁决的证据。**保留**，作为该裁决的依据被本规划引用。
- `.artifacts/i18n/p1-batches/p1-quality-random-batch-001.json` —— 25 条**随机**抽样批次
  （population 23294，seed 已记录，source_commit `624a673`），建于 2026-08-16，从未被审核、
  从未进入任何 task 或 review 记录，仓库中无任何引用。它不符合 §3.2 的风险维度排序口径。
  处置见 §6.2。

## 二、批次总体结构

P1 由若干**独立闭环的小批次**组成，每批 20–30 条，单一风险维度。批次之间不共享未裁决状态：
一批的 finding 必须在该批内裁决完毕并修复，才决定是否开下一批。

不预先承诺批次总数。每批结束后按 §7 的续做判据决定继续、换维度还是收束 P1。

## 三、首批（P1-B1）定义

### 3.1 维度选择

按 roadmap §3.2 的优先顺序，首批取第 2 项：**天赋公式、数值、单位与条件描述**。

理由：这类文本承载玩家的直接决策依据（伤害、加成、持续时间、触发阈值），译错的后果是实际的
误导而非风格瑕疵；同时它可以在固定源码上精确核验（公式和数值都能追到 talent 定义），最容易
在一批之内形成确定结论而不是留下一堆"待确认"。

### 3.2 候选池

确定性过滤条件（全部来自 `quality inventory` 的既有字段，不新增判据）：

```text
component == "tome"
profile   == "mechanics"
risk_flags 含 "source-has-number-or-unit"
len(source) >= 40
```

各维度池子实测规模（tome 全部 / 其中 mechanics / 再限 `len(source) >= 40`）：

| roadmap §3.2 维度 | risk_flags | tome | mechanics | 且 ≥40 字符 |
|---|---|---|---|---|
| 2 数值与单位 | `source-has-number-or-unit` | 4467 | 2281 | **1992** |
| 3 否定与条件 | `source-has-negation-or-condition` | 2379 | 846 | 822 |
| 4 printf／args／markup | `has-printf`／`has-args-order`／`has-markup`／`has-at-token` | 6048 | 2847 | 2071 |
| 5 术语与变体 | `preferred-term-present`／`term-variant-or-review` | 3229 | 531 | 439 |
| 6 长文本与英文残留 | `long-source`／`possible-untranslated-residue` | 1759 | 993 | 993 |

首批候选池 = 1992 条，其中 `data/talents` 占 1515 条，711 条同时带 `source-has-negation-
or-condition`。

`len(source) >= 40` 的作用是排除纯数值片段和短标签，使每条都具备可核验的语义结构；它是
**池子定义的一部分**，不是事后筛选。

### 3.3 选择规则（结果可见前冻结）

```text
批次规模 n = 24                （20–30 区间内取值；24 = 3 个 review bundle × 8 条）
排序键     revision_id 升序     （确定性，与文件顺序无关）
种子       "tome4-p1-b1|" + inventory_sha256 + "|" + source_commit
选择       种子驱动的确定性洗牌后取前 24 条
```

冻结产物写入 `.artifacts/i18n/p1-batches/p1-b1-mechanics-numeric.json`，必须记录：
`inventory_sha256`、`source_commit`、过滤条件、排序键、种子字符串、池子大小、
以及 24 条的 `revision_id` / `revision_uid` / `tu_uid` / `section` / `line` / `source` /
`target` / `source_tag`。

**冻结之后不得以"这条不好判"为由替换条目。** 无法判定的条目按 §5 标为待确认并计入指标——
这正是衡量该维度是否值得继续投入的信号。

风险 flag 只负责**把这 24 条选出来**，不表示其中任何一条是缺陷。基线预期是其中多数正确。

## 四、工具路径与两个必须绕开的陷阱

**4.1 `tools/i18n workset` 走不通。** 它只能从 merge report 的
`added`／`untranslated-existing`／`source-changed` 三种分类构造，而三者当前均为 0（§1.1）。
首批不经由 workset。

**4.2 不使用 `tools/i18n quality sample`。** 它绑定 v1 质量试点契约（policy pilot size 120、
分层桶、assessment 模板），会把 deferred 的正式 120 条／M5／M6 机制拖回当前工作。首批只把
`quality inventory` 的输出当作**只读的确定性排序来源**，选择逻辑独立完成。

**4.3 因此需要一个小的选择脚本**（约 60–80 行，`tools/` 下版本控制，输出只写
`.artifacts/i18n/p1-batches/`）：读 inventory.jsonl，按 §3.2 过滤、§3.3 排序抽样，写冻结
JSON。它不做判断、不改写任何 Lua、不调用 provider。这是本规划唯一新增的工具面，且刻意做成
一次性可复用的薄脚本，不是新契约。

## 五、单批闭环（roadmap §3.3 的可执行版本）

```text
S1  冻结批次        →  S2  宿主源码核验  →  S3  术语前置
S4  译文修订        →  S5  语境审核      →  S6  宿主裁决
S7  修复与复审      →  S8  门禁          →  S9  提交
```

**S1 冻结批次。** 运行 §4.3 的选择脚本，产出冻结 JSON。同时记录 `git status --short`。

**S2 宿主源码核验（本批最重的一步，由主代理承担）。** 对 24 条逐条在固定源码 commit
`624a673` 上核验：数值与公式是否与 talent 定义一致、单位是否正确、条件与阈值方向是否正确、
`%s`／`%d` 对应的运行时参数是什么。每条记录组件、公开源码路径、关键调用或数据定义。
证据不足的标为**待确认**，不猜测。

这一步先于任何模型参与。roadmap §3.2 的"风险 flag 只负责排序，不自动确认缺陷"和
`AGENTS.md`「校对判定依据」的源码优先原则都在这里落地。

**S3 术语前置。** 若 S2 发现高复用术语需要调整，**先**改 `terminology/`，再改译文
（`AGENTS.md` 术语库工作流）。术语改动后追加运行 `audit_static.py`、`audit_dynamic.py`、
`annotate_domains.py`。

**S4 译文修订。** 只修订 S2 中已确认的问题条目。翻译 agent 只产出 proposal，主代理用
`tools/i18n proposal --strict` 校验后应用。未确认的条目不动。

**S5 语境审核。** Paseo REVIEWER，`purpose=translation_contextual_v1`，按
`docs/paseo-translation-context-review-v1-contract.md`。用
`tools/i18n review --scope translations --batch-size 8` 导出有界 bundle（每 bundle ≤ 8 条、
默认字符预算内）。bundle 不含先前 finding、裁决或建议修复。

**S6 宿主裁决。** 每条 finding 标 confirmed／pending／advisory 并独立定级；模型自报等级不作为
事实。只有 confirmed 进入修复。

**S7 修复与复审。** 修复 confirmed finding，对**新 revision** 重新审核。

**S8 门禁**（按 `AGENTS.md` 顺序，不吞退出码）：

```bash
python3 -B tools/i18n lint --strict; echo "exit=$?"
python3 -m unittest -q tests/i18n/test_toolchain.py; echo "exit=$?"
python3 -B tools/scan_runtime_collisions.py; echo "exit=$?"
python3 -B tools/classify_runtime_keys.py; echo "exit=$?"
git diff --check && echo DIFF_OK
```

**S9 提交。** 译文批次**单独提交**，不混入基础设施改动（roadmap §3.3 第 9 条）。不 push。

## 六、Paseo 编排与 artifact 处置

### 6.1 编排

首批按 review_only 与 implement 混合的实际形态执行：S2 由主代理完成（不委派——源码裁决是宿主
职责），S4 可委派 EXECUTOR，S5 走 translation_contextual_v1 REVIEWER。task ID：
`p1-b1-mechanics-numeric-001`。

§4.3 的选择脚本属工具变更，按 `AGENTS.md` 第 9 条需 REVIEWER 与 SENIOR_REVIEWER 从同一
SPEC／diff 交叉审核。**该 code 审核与译文批次分开提交**。

### 6.2 随机批次 artifact 的处置

`p1-quality-random-batch-001.json`（§1.3）**不进入首批**。它不是风险维度切片，混入会让批次口径
不一致。两个可选去向，均非首批前置条件：

- **保留为后续的随机对照批**：风险排序批次天然高估缺陷率，一个无偏随机批次能给出整体缺陷基线，
  用来判断 P1 是否值得继续投入。若采用，它应在首批之后作为独立批次执行，并明确标注为随机对照。
- **丢弃**：若不打算做基线估计，按 §1.3 直接删除，避免再留一个无归属 artifact。

首批开始前不必决定；首批结束时按 §7 的数据一并决定。

## 七、验收、续做判据与停止条件

### 7.1 首批完成条件

1. 24 条全部完成 S2 源码核验，每条有明确结论（正确／确认缺陷／待确认）并附证据；
2. 全部 confirmed finding 已修复；
3. 无未解决 accepted finding；
4. 修订后的条目通过一轮新的独立语境审核；
5. §5 S8 全部门禁通过；
6. 至少形成一批实际译文改进，且已单独提交。

若第 6 项不成立（24 条全部正确），首批**照样算完成**——那是一个有价值的结论，说明该维度不是
问题富集区，应换维度而不是加大批量。

### 7.2 续做判据

首批结束时记录三个数字，作为后续决策依据：

- **命中率**：confirmed 缺陷 / 24；
- **待确认率**：证据不足 / 24；
- **宿主核验成本**：S2 实际耗时。

判据（首批后适用，不预设普适阈值）：

- 命中率明显偏低 → 换维度，不在同一维度加大批量；
- 待确认率偏高 → 说明维度定义太宽或证据链不足，先收窄池子定义；
- 核验成本高到无法维持 → 缩小批次规模，而不是降低核验标准。

### 7.3 明确不做

- 不为提高覆盖率而放弃逐条源码核验；
- 不把 `status.changed`（tome 3,335）或 `canonical_only` 当作缺陷队列；
- 不因首批结果启动 evaluator 选型 campaign——Selection-Lite 的成本闸门独立生效，
  见 [`translation-quality-evaluator-selection-lite-v1.md`](translation-quality-evaluator-selection-lite-v1.md) §9；
- 不在译文批次中夹带基础设施重构；
- 不 push、不同步发布仓库、不创建 release。

## 八、首批的下一个动作

`tools/i18n quality inventory` 已经运行、池子已经算出（§3.2）。开工的第一个具体动作是
实现 §4.3 的选择脚本并冻结 24 条批次；在此之前不需要任何新的决定。
