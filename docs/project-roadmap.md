# ToME4 汉化项目 Roadmap

> 状态：当前执行路线图，记录日期 2026-08-16。
> 本文规定近期工作的优先级和阶段依赖，不替代质量 contract、审核契约、门禁或发布流程。
> 事实或用户裁决变化时更新本文；不因长期阶段存在而默认启动 provider、Paseo task、push 或发布。

## 一、当前判断

项目已经完成确定性基础设施建设期，当前主线转为译文质量优化：

```text
真实语料差异 / 风险信号
            ↓
玩家可见性与源码机制核验
            ↓
小批量翻译或修订
            ↓
语境审核 + 宿主裁决
            ↓
完整门禁
            ↓
提交与发布决策
```

截至记录日：

- 目标游戏版本为 ToME4 1.7.6；官方 DLC 源码基线为 1.7.4。
- `develop` HEAD 为 `5b2f8d0`，领先 `origin/develop` 19 个提交，未 push。
- tracked 工作树干净；没有活跃 implement-mode Paseo task，也没有未解决的 accepted finding。
- v3 campaign、正式 120 条、M5/M6、Gold/Silver TM 均为 deferred。
- 现有“不 push”裁决继续有效，直至下一轮译文质量优化完成或用户另行指示。

## 二、阶段总览

| 阶段 | 状态 | 核心交付物 | 退出条件 |
|---|---|---|---|
| P0 确定性基础 | 已完成 | baseline、身份轴、lint、CI、runtime key、术语和审核路由 | 当前门禁和历史独立复审通过 |
| P1 核心译文优化 | **当前主线** | Tome 高风险有界 workset、源码核验和实际译文修订 | accepted finding 清零，语境审核与门禁通过 |
| P2 组件扩展 | 待 P1 验证 | DLC、UI、运行日志、对话和叙事的分层批次 | 每批独立闭环，不积累未经裁决的大队列 |
| P3 集成与发布 | 待质量优化完成 | 累计门禁、构建、提交整理和 push/release 决策 | 用户明确批准后才 push 或同步发布仓库 |
| P4 正式质量试点 | deferred | 新校准设计、正式 120 条、M5 人工裁决和 M6 报告 | 四项解除条件全部满足，并得到启动决定 |
| P5 精确 TM | 长期 | Gold/Silver 精确译文库和修订失效机制 | 正式裁决证据与 Go/No-Go 报告支持投产 |
| P6 模糊检索与反馈 | 远期 | Top-K 联想、采纳反馈和持续校准 | 精确 TM 成熟，且冻结基准达到预定精度 |

## 三、P1：下一轮核心译文优化

### 3.1 输入口径

workset 只从以下输入构造：

1. 固定源码版本之间的真实 source diff；
2. 当前 revision inventory 的确定性风险规则；
3. 已核验且尚未解决的 finding。

不得把 `status.changed` 或 `canonical_only` 当作缺陷/待译队列。前者包含本项目有意改进的
译文，后者表示只在规范仓库出现的键，两者都不自动代表需要处理。

当前 Tome 1.7.4 → 1.7.6 三方合并结果为：

- runtime source 新增 18、删除 18；当前规范译文已经覆盖新增项；
- `added = 0`，`source-changed = 0`；版本升级本身没有产生新待译批次；
- `untranslated-existing = 100`，但包含调试文本、测试数据、占位文本和格式片段；
- `obsolete-or-unextracted = 101`，不作为翻译队列；
- 当前未解决 accepted finding 为 0。

因此，100 条 `untranslated-existing` 只能先作为可见性核验 workset，不能直接交给翻译 agent。

**已核验裁决（2026-08-16，源码固定 commit `624a673`）**：对 100 条逐条按 `source_tag`＋内容做
可见性三方核验后，其可翻译的玩家可见自然语言内容为 **0**，本队列不产生译文批次。分布：

- 约 66 条为纯格式／markup 片段（`%s`、`#GOLD#%s#LAST#`、`%d%%`），无自然语言；
- 27 条为战术 AI 调试日志（`log` tag，`improved_tactical.lua`／`ActorAI.lua`／`maintenance.lua`，
  如 `CACHE MISMATCH`、`Invoking improved tactical AI`），非玩家可见；
- 3 条为占位乱码天赋名（`malleable-body.lua` 的 `azdadazdazdazd` 等）、`gem.lua` 的 `..` 实体名、
  2 条 `test.lua` 测试 vault 串——源码内开发占位；
- 5 条边界项经固定源码核验后均确认按约保持原文：`Game.lua:2099` 的 `_t"Imperium courrier"`
  在 `Chat.new("tareyal+test", …)` 测试链内；`GraphicMode.lua:38-39` 的 `Old RPG`／
  `Altefcat/Gervais` 为图块包专名、`64x64` 为尺寸标签；`shertul.lua:100` 的 `'Meas Abar.'`
  为按 `speaks_shertul` 门控的族内 Sher'Tul 语，官方 `zh_hans.lua` 亦保留原文（其含义
  "The Great Sin." 由另一独立串承载）。

该裁决关闭 `untranslated-existing` 作为待译来源；后续升级若使该队列出现新的玩家可见自然语言项，
才重新按可见性核验纳入。

### 3.2 首批选择

`untranslated-existing` 已按 §3.1 裁决关闭，`added`／`source-changed` 均为 0，未解决 accepted
finding 为 0——三项确定性输入当前都不产生待译批次。因此首批改为对 **已译核心 revision** 的
有界质量核查 slice：按单一确定性风险规则从约 3,348 条已译核心 revision 抽取，而非把
`status.changed`（tome=3,335）当作缺陷队列。首批保持约 20–30 条的有界规模，风险维度择一，
按下列顺序在该维度内排序选择：

1. 经源码确认玩家可见的未译项；
2. 天赋公式、数值、单位和条件描述；
3. 施法者/目标、上下限、持续时间、否定关系和先后顺序；
4. printf、参数顺序、markup 和 token；
5. 高复用术语及术语变体；
6. 长文本和疑似英文残留。

风险 flag 只负责排序，不自动确认缺陷。调试、测试或内部文本只有在源码可见性证据明确后
才排除；证据不足的条目标为待核验。

### 3.3 单批闭环

每个批次按以下顺序执行：

1. 冻结 workset 和固定源码证据；
2. 核验玩家可见性、机制、术语、占位符/markup、运行键和中文表达；
3. 高复用术语发生变化时先更新 `terminology/`；
4. 翻译 agent 只生成 proposal，主代理严格校验后应用 accepted 项；
5. 使用 Paseo REVIEWER `purpose=translation_contextual_v1` 做有界语境审核；
6. 主代理按固定源码独立核验并裁决 finding；
7. 修复 confirmed finding，并对新 revision 重新审核；
8. 运行适用的严格 lint、单测、runtime key 扫描、术语审计和 `git diff --check`；
9. 译文批次单独提交，不混入新一轮基础设施扩建。

P1 完成条件：选定批次全部裁决，confirmed 问题均已修复，没有 unresolved accepted finding，
全部适用门禁通过，并形成至少一批实际译文改进。

## 四、P2–P3：组件扩展、集成与发布

P1 完成后根据已核验的缺陷类型、命中率和宿主核验成本决定下一批，不预先承诺全量审核。
建议组件顺序：

1. Tome 核心 mechanics；
2. 三个官方 DLC；
3. UI、状态和运行日志；
4. 对话与长叙事；
5. 辅助 addon/example 中确认玩家可见的内容。

下一轮质量优化完成后执行累计全量门禁、addon 构建和 smoke，并整理本地提交。随后由用户决定：

- 是否 push `develop`；
- 是否同步 `tome4-chn-mod`；
- 是否形成新版本发布。

路线图本身不授权 push、修改外部发布仓库、上传 teaa 或创建 release。

## 五、P4：正式质量试点的解除条件

`stability-preregistration-v2.json` 及冻结输入保持
`inactive / deferred due to route incompatibility`，字节、身份和历史 hash 均不修改。

只有在明确准备启动正式评价链时，才讨论恢复 v3；以下四项必须同时完成：

1. 新 preregistration 版本；
2. `translation_contextual_v1` 结果到 v3 assessment/finding/match/stability/report 的
   fail-closed 映射契约；
3. 第二独立 evaluator 的 provider/model 选定和译文 bundle 外发授权；
4. 人工先标注的分层正负对照集。

解除后仍按依赖顺序执行：

```text
新校准设计
    ↓
8 槽校准与 stability 判定
    ↓
正式 120 条两份独立 assessment
    ↓
M5 人工裁决
    ↓
M6 Go / Go with changes / Exact-only / No-Go
```

`host_technical_derivation_agreement` 是 provider 调用前的宿主实现不变量，不是需要消耗
provider 槽位估计的模型指标；但该重分类不改变“两 evaluator × 两轮 × 两 shard”的 8 槽预算。

## 六、P5–P6：长期能力

正式报告支持投产后，先建设只读、精确匹配的 Gold/Silver TM：

- 质量证据绑定 current `tu_uid`、`revision_uid` 和 `revision_id`；
- source、target、版本、术语或结构变化使旧认证失效；
- 保留同源不同语境的合法 variant，不无证据合并；
- 只提供查询和导出，不自动写入规范 Lua。

精确 TM 成熟后才进入模糊匹配：先做结构兼容过滤，再做候选排序和高风险差异检测；在冻结
查询集达到预先定义的 Precision@K/Recall@K 后，才接入 proposal 工作流。任何建议仍需人工
采纳或修改，不直接改写译文。

## 七、明确暂缓

下列事项不进入当前近期待办：

- v3 bridge/campaign 和旧 preregistration 的 8 个槽；
- 正式 120 条、M5、M6；
- Gold/Silver TM 投产与模糊检索；
- entity ledger、Pilot B、Precedent/Exception 完整治理生命周期；
- Facts study 新迭代或新 provider campaign；
- 为了完善研究设施而新增与当前译文批次无直接产出的基础设施。

## 八、参考文档

- [`translation-quality-system.md`](translation-quality-system.md)：长期质量系统设计；
- [`translation-quality-phase-1.md`](translation-quality-phase-1.md)：阶段 1 数据契约与 M0–M6；
- [`../i18n/quality/README.md`](../i18n/quality/README.md)：权威质量规则与 v3 deferred 状态；
- [`paseo-translation-context-review-v1-contract.md`](paseo-translation-context-review-v1-contract.md)：
  现行译文语境审核契约；
- [`release-plan.md`](release-plan.md)：发布操作与历史决策。
