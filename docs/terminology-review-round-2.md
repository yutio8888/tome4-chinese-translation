# 第二轮术语审核框架

## 1. 审核基线与目标

- 工作分支：`audit/terminology-review-round-2`
- 基线分支：`develop`
- 基线提交：`a781a356b8fa98042f7634761d728205dd052ca6`
- 游戏版本清单：`i18n/versions/tome-1.7.6.json`
- 核心源码固定提交：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
- 规范输入：`terminology.tsv` 与版本清单声明的 11 个 Lua 翻译组件
- 外部边界：框架设计阶段不调用 Pi 或其他 provider；机制核验只读使用固定版本公开源码。DLC 按仓库基线与项目授权的公开正式版源码核验。

本轮不是简单扫描同词多译，而是依次回答三个问题：

1. **完整性**：应进入术语治理范围的概念是否都已登记；
2. **合理性**：每个登记术语的译法、类别、领域、作用域和语境是否有依据；
3. **一致性**：规范译法是否在所有适用译文中统一，语境差异是否被明确记录。

完成标准是所有必审术语都有可追溯裁决，所有适用译文中的未授权漂移清零，并通过术语审计、译文门禁、构建与一轮全新只读复审。

## 2. 当前基线画像

2026-08-10 在上述基线上执行 `doctor`、静态审计、动态审计和领域标注，得到：

- 规范译文共 **30,308** 条，覆盖 11 个组件；
- 术语表共 **693** 条：`preferred=254`、`existing=439`、`review=0`；
- 领域分布（TSV 声明 domain 计数）：combat 152、talents 212、classes 45、resources 12、items 55、creatures 72、places 46、society 33、narrative 52、ui 12、tech 2；`annotate_domains` 推导 domain 为 combat 148、resources 17、creatures 71，两套口径共 6 处不一致（均为 advisory，随批裁决）；
- 作用域分布：core 358、global 136、dlc 198、multi 1，当前没有 `addon` 条目；
- 227 条 `existing` 没有 notes；结构门禁只要求 `preferred` 填 notes，因此它们不是格式错误，但尚无逐条审核依据；
- 静态审计报告 1 组同源同类别多译、14 个类别边界疑点；
- 动态审计报告 64 条 preferred 无精确活动匹配、1 条 target 不一致、28 个未记录的多译 source；
- 领域标注无未映射项，但有 6 个声明领域与推导领域不同的 advisory；
- `TERMINOLOGY.md` 中手工维护的领域计数和“当前 review 示例”已经与 TSV 现状不一致，后续应改为自动生成或由门禁校验。

现有动态审计只能检查“整个 source 与术语 source 精确相等”的条目，并以出现至少 15 次的完整 source 生成候选。它不能证明术语表完整，也不能发现术语作为短语出现在长技能说明、日志或叙事文本中的漂移。

- 动态审计 S2.2 的“高频未录候选”（译文出现 ≥15 次的完整 source，当前共 5 条）是 B 类候选的优先入口，纳入完整性流水线输入，直接进入人工裁决；
- 运行时标签体量：`_t` 14,929 条、`tformat` 3,842 条、`logPlayer`/`logSeen`/`log`/`logCombat` 约 2,059 条、`nil` 115 条。这些是运行时键与格式模板空间，不作为逐条术语候选全集，治理边界见 3.A。

### 2.1 现有术语登记覆盖率仅作缺口信号

下表按 `(组件, source, source_tag)` 检查是否存在作用域和标签均匹配的术语行。它不是最终完整性分母，但能说明当前术语表仍是种子集。匹配口径固定为 `workset._scope_matches` 语义（`global`/`multi` 匹配任意组件；`dlc` 只匹配 Ashes/Cults/Orcs；`core` 匹配非 DLC 组件；`addon` 只匹配 addon-dev/items-vault/possessors）。匹配口径已在生成器（`tools/audit_dynamic.py` r2 inventory）落地为单一事实来源，本表数字与生成器输出（`coverage.json`）完全一致。

| source_tag | 候选单元 | 已登记 | 缺失 | 覆盖率 |
| --- | ---: | ---: | ---: | ---: |
| `talent name` | 1871 | 124 | 1747 | 6.6% |
| `talent category` | 34 | 25 | 9 | 73.5% |
| `talent type` | 364 | 88 | 276 | 24.2% |
| `birth descriptor name` | 101 | 63 | 38 | 62.4% |
| `damage type` | 205 | 38 | 167 | 18.5% |
| `effect subtype` | 263 | 90 | 173 | 34.2% |
| `stat name` / `stat short_name` | 38 | 38 | 0 | 100% |
| `entity type` | 117 | 53 | 64 | 45.3% |
| `entity subtype` | 305 | 41 | 264 | 13.4% |
| `faction name` | 16 | 6 | 10 | 37.5% |
| `achievement name` | 200 | 1 | 199 | 0.5% |
| `newLore category` | 74 | 39 | 35 | 52.7% |

同一个 source 可能因类别或语境不同而合法多译；因此正式审核不能只用英文字符串去重，也不能把上表的所有缺失项机械加入 TSV。

## 2.2 规模估计与工作总量

按 2.1 口径对可枚举候选去重求和（`(组件, source, source_tag)` 单元），并叠加全部 693 条现有术语行的复核，本轮工作分三类：

| 工作类 | 规模（生成器实测） | 说明 |
| --- | ---: | --- |
| A 类候选 | 1,443 单元 | 已登记 442 / 缺失 1,001（damage 167 + effect subtype 173 + talent category 9 + talent type 276 + birth descriptor 38 + faction 10 + entity type 64 + entity subtype 264）；stat 已 100% 登记 |
| B 类候选 | 6,047 单元 | 已登记 253 / 缺失 5,794 / 自动排除 2,299 / 需人工 3,495；entity name 3,048 + talent name 1,871 + achievement 200 + newLore 74 + entity keyword 434（provisional，待源码核验归属）+ 其余开放名称 |
| C 类不生成候选 | 约 19,465 单元 | `_t` 13,742 + tformat 3,766 + log* 1,792 + nil 115 等；仅治理已登记行（见 3.A 运行时标签边界） |
| 现有术语行复核 | 693 | 全部逐条裁决：254 preferred 复核 + 439 existing 升级/降级/迁移（227 条无 notes）；含运行时/格式标签行 142（`_t` 97、`nil` 23、`tformat` 16、`log*` 6，其中 39 条 existing） |

人工裁决单元合计 ≈ **5,189**（A 缺失 1,001 + B 需人工 3,495 + 现有行 693）；自动排除的 2,299 条 B 类长尾按批次抽样复核（≥5% 或每批 ≥20）。以上为生成器实测（`baseline.json`/`coverage.json`，2026-08-10，B-AUTO-1 含机制关键豁免：talent name/achievement name/newLore category 不自动排除），每批开工前再冻结该批分母（见 6）。

按批次（生成器实测：候选单元 / 已登记 / 缺失 / 自动排除 / 需人工 / 现有行复核）：

| 批次 | 候选单元 | 已登记 | 缺失 | 自动排除 | 需人工 | 现有行复核 | 备注 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P0 基础机制 | 506 | 166 | 340 | 0 | 340 | 107 | **注册表口径**：damage type 205（登记 38 / 缺失 167，其中 162 建议登记、5 条内部描述名建议排除）+ effect subtype 238（登记 50 / 缺失 188）；stat 已 100% 登记。注册表见 `.artifacts/i18n/terminology-review-r2/source-registries/damage-effect-registry.json`，裁决清单见 `worksets/P0-core-v2.json` |
| P1 角色结构 | 1,066 | 235 | 831 | 240 | 591 | 202 | talent category 9 + talent type 276 + birth descriptor 38 + faction 10 + entity type 64 + entity keyword 434 |
| P2 技能体系 | 1,871 | 124 | 1,747 | 0 | 1,747 | 100 | talent name 机制关键，全部人工裁决 |
| P3 实体与专名 | 3,526 | 130 | 3,396 | 1,869 | 1,527 | 95 | entity name 3,048 + entity subtype 264 + ingredient/gem 等；规则分流 + 抽样 |
| P4 叙事与界面 | 521 | 40 | 481 | 190 | 291 | 189 | newLore 35 + achievement 199 + 运行时/格式标签行 142 + chat_*/dialog 等 |

## 3. 完整性的可审计定义

先建立“候选全集”，再按治理等级裁决，避免把“术语表完整”误解为收录全部 30,308 个完整句子。

### A. 必须穷举登记的封闭词表

这些集合由源码定义或稳定的 `source_tag` 构成，目标是 100% 裁决：

- 伤害类型、状态/效果类型、资源、属性及其短名（**以源码注册表为权威分母**：damage type 205 = damage_types.lua 中 `name = _t(..., "damage type")`（tome 178 + cults 11 + orcs 30，唯一 205）；effect subtype 238 = timed_effects/effects 定义中的 subtype 键（tome + DLC）。译文候选单元中的描述性噪音（如 `% chance of confusion`）以注册表口径过滤）；
- 职业、种族、阵营、实体类型/子类型等源码注册的封闭枚举（entity type 64、entity subtype 264、faction 10）；
- 技能树/技能类别与出生描述（talent category 9、talent type 276、birth descriptor 38）；
- 玩家可见且跨文本复用的机制标签；
- 跨组件或跨语境重复出现的专名（entity name 中跨组件复用子集）；
- **运行时标签与格式模板的治理边界**：`_t`（14,929 条）是运行时键空间，不作为逐条术语候选全集；治理对象是“高复用、玩家可见”的运行时标签——已登记 97 行逐一复核，新增候选来自运行时键扫描（`scan_runtime_collisions.py`/`classify_runtime_keys.py`）与 S2.2 高频未录候选。`tformat`/`log*`（约 5,900 条）是格式与日志模板，不逐条登记，已登记 22 行复核占位符完整性与译法；`nil` 标签行（23 条）按 `(component, section)` 语境归入对应领域后用 A/B 规则裁决。

每个候选必须进入 TSV，或进入带理由的排除清单。不能因当前译文恰好一致而跳过登记。

### B. 必须审核、按复用价值决定是否登记的开放词表

- 技能名、成就名、人物、地点、物品、生物、世界观事件；
- UI 标签、日志模板、叙事分类；
- 只出现一次但会与其他名称、说明或机制文本形成词族的名称。

这类候选全部做合理性和同源多译审核；以下任一条件成立时登记：跨组件、出现两次以上、存在词族、机制关键、专名关键、已有多译或容易与其他概念混淆。纯一次性且不存在复用风险的名称可留在有依据的排除清单中。

B 类规模约 5,500–6,000 个，必须**程序化分流 + 抽样复核**才能收束：先按固定规则（单次出现、无词族、非机制/专名关键、无跨组件复用、当前译文无多译）自动生成排除候选，人工只裁决命中登记条件的子集；**机制关键标签（talent name、achievement name、newLore category）不参与自动排除，一律人工裁决**；每批对自动排除结果按比例抽样（≥5% 或每批至少 20 条）复核规则正确性，规则变化后重算并记录。S2.2 高频未录候选（≥15 次，当前 5 条）直接进入人工裁决，不参与自动排除。

### C. 默认不登记但仍受译文质量门禁约束的内容

- 普通长句、一次性对话和普通叙述词；
- 仅内部调试且玩家不可见的字符串；
- `floor`、`wall` 等通用地形键，除非出现跨语境冲突或用户可见一致性风险。

排除不是忽略：候选生成报告必须记录规则、数量和样本，规则变化后可以重算。

## 4. 审核数据模型

审核单位不能只有 `source → target`，至少绑定：

- `component`、`section`、`source_tag`；
- `source`、当前 `target`、出现位置与频次；
- TSV 的 `category`、`domain`、`scope`、`status`、`notes`；
- 固定源码版本、定义位置和必要的机制证据；
- 词族关系（大小写、单复数、派生词、技能/状态/日志/说明）；
- 裁决：`preferred`、`review`、`excluded` 或 `stale`；
- 允许的译法及适用条件。

`existing` 只表示历史收集状态，不代表通过第二轮审核。第二轮完成时，范围内不能遗留未裁决的 `existing`：确认后升为 `preferred`，证据不足转为有说明的 `review`，无活动来源则确认迁移或删除。

### 4.1 裁决证据 rubric

`existing` → `preferred` 的最小证据集：

1. **定义证据**：固定版本源码中的定义位置（文件 + 行 + 对象/注册表条目）或受审计提取快照条目；
2. **复用证据**：跨组件 ≥2 处，或同组件 ≥2 处不同 section/语境；
3. **无冲突证据**：不存在未记录的同源异译（有则先拆分多行并补 notes）。

三条同时满足 → `preferred`；存在合法语境差异 → 拆多行、各行 notes 注明语境，仍可全部 `preferred`；有真实歧义或证据不足但存在复用风险 → `review` 并写明缺失证据与后续责任；无复用、无词族、单次出现 → 进入排除清单（带规则）。

64 条无活动匹配的 `preferred` 逐条按源码核验处置：源码中已删除/改名 → 记录迁移映射或降级；提取缺口 → 重新提取核验；source_tag 不匹配 → 修正标签。只有核验后仍无法解释的才算异常。

状态机约束：`excluded` 只存在于 artifact 排除清单（TSV 合法 status 仅 `existing`/`preferred`/`review`），`stale` 用 notes 标记而非新状态。

## 5. 三条审核流水线

### 5.1 完整性流水线

1. 从固定版本提取结果和 11 个规范翻译组件构建候选全集；
2. 按 source_tag、源码注册表、重复频次和词族关系生成候选；
3. 与 TSV 按 `(source, source_tag, scope/category)` 对齐；
4. 将结果分为已登记、缺失、作用域不匹配、标签不匹配、排除；
5. 对 A 类逐条清零，对 B 类逐条登记或给出排除理由；
6. 输出按组件、领域、类别的覆盖率，禁止仅报告一个全局百分比。

### 5.2 合理性流水线

每个术语依次检查：

1. **源码事实**：实际对象、机制、触发条件和玩家可见语境；
2. **语义准确**：不增减含义，不混淆相邻机制或专名；
3. **中文质量**：自然、简洁，符合既有游戏语言习惯；
4. **分类正确**：category、domain、source_tag、scope 与实际用途一致；
5. **词族协调**：技能名、状态名、日志、说明及派生词相互兼容；
6. **技术完整**：占位符、颜色标记、大小写敏感键和尾随空格不受破坏；
7. **裁决记录**：preferred 必须有足够 notes；有真实歧义时保留 review，不猜测定稿。

现有 254 条 preferred 也必须复核，不能把历史状态当作正确性证据。机制分歧以固定版本源码行为为最终依据。

### 5.3 一致性流水线

一致性分三层检查：

1. **精确键一致性**：相同 `(source, source_tag, scope)` 的 target 是否符合 preferred；
2. **长文本投影**：英文 source 中出现术语短语时，中文 target 是否采用对应概念译法。实现按**高精度低召回**起步，避免误报淹没裁决：
   - 投影对象仅限 `preferred`（含本轮新提升）术语行；
   - 英文侧：词边界匹配、大小写不敏感（专名除外）、候选短语 ≥4 个字母；复数/派生形式使用每术语显式登记的变体表（notes 登记），不用自动词干化；
   - 中文侧：target 包含术语中文 target（≥2 字）或 notes 声明的允许变体；
   - 匹配前剥离 `#...#`、`@...@` 标记与 `%` 占位符参数区；
   - 通用词黑名单（master、wall、fire 等易混淆词）与出现频次阈值控制噪音；
   - 输出全部为“候选不一致”进入 triage，**不直接成为 finding**；只有经源码核验的确认漂移才进入 findings；
   - 首轮试点统计误报比（预期初始较高），超过阈值（如 60%）先收紧规则再扩大批次；全量报告写入 artifact，人工按抽样复核而非全量逐条；
3. **词族一致性**：名称、状态、日志、描述、UI 和跨组件变体是否遵循同一裁决。

每个不一致必须分类为：确认漂移、合法语境差异、误匹配或待源码核验。合法差异必须回写多行 TSV 或 notes，不能只放在临时报告中。

## 6. 分批顺序与工作集

按错误影响和依赖关系执行，先冻结一批 findings，再统一修复该批：

1. **P0 基础机制**：damage、effect、resource、stat；
2. **P1 角色结构**：class、race、talent category/type；
3. **P2 技能体系**：talent name 及其状态、日志、说明词族；
4. **P3 实体与专名**：item、creature、place、faction、person、world；
5. **P4 叙事与界面**：lore、achievement、UI、runtime log、format/internal。

每个优先级先 core，再按 Ashes、Cults、Orcs 分 DLC；addon-dev、items-vault、possessors 单列，避免重叠 scope 掩盖差异。单个工作集以一个领域 × 一个组件（或一个紧密词族）为边界，包含候选、所有出现位置、源码证据和当前 TSV 行。

批内规模（生成器实测，见 2.2 批次表）：P0 需人工 340 + 行 107、P1 591 + 202、P2 1,747 + 100、P3 1,527 + 95、P4 291 + 189。

**每批进度度量**：分母（生成器输出）→ 已裁决 / 待裁决 → 已确认 finding / 已修复 → 投影误报比与排除规则抽样复核结果。批次完成 = 分母清零 + 该批单批验证通过 + findings 冻结。

## 7. 产物与实施边界

分析报告和候选工作集写入忽略目录：

```text
.artifacts/i18n/terminology-review-r2/
  baseline.json
  candidate-inventory.json
  coverage.json
  exclusions.json
  worksets/
  findings/
  decisions/
```

版本化文件只保存稳定契约和最终裁决：

- `terminology.tsv`：规范术语及语境差异；
- `TERMINOLOGY.md`：分类、纳入规则和维护流程；
- Lua 规范翻译：经确认 finding 对应的统一修订；
- `docs/terminology-review-round-2.md`：本轮框架和完成标准。

### 7.1 口径固定与工具单一事实来源

- 候选全集、覆盖率与投影匹配口径统一固定，生成器**扩展 `tools/audit_dynamic.py`（复用其 JSON 输出与候选逻辑）或直接消费其 `.artifacts` 输出**，不新建平行工具，避免双轨漂移；
- 作用域匹配口径固定为 `workset._scope_matches` 语义并写入表驱动测试；2.1 表格与生成器输出（`coverage.json`）完全一致，以生成器输出为唯一事实来源；
- 生成器输出 `baseline.json`、`candidate-inventory.json`、`coverage.json`、`exclusions.json`，每个文件绑定输入快照（TSV 与组件文件 SHA-256、版本清单、生成器版本），按内容寻址供消费方核对；
- `TERMINOLOGY.md` 的统计与示例（Constrict/eldritch/Atmos Tribe 实际已为 `preferred`）在生成器落地时同步改为自动生成或修正，不拖到收尾。

### 7.2 分工边界

- 可委派只读子代理（遵循 AGENTS.md 有界任务约束）：候选生成复核、源码证据收集（定义位置、出现位置列表）、投影候选整理、排除规则抽样初筛；
- 不委派：`preferred`/`review`/`excluded` 定级、译文修订、最终裁决记录——只在主代理；
- Pi 本轮不引入：术语裁决不进 blind discovery；若后续引入，只能遵循项目 translation semantic v2 的 blind observation 流程；术语表不能注入 discovery payload，模型 observation 不能直接成为裁决或改写规范 Lua。每次外发前另行取得授权。

## 8. 验证与退出标准

### 单批验证

- 该批分母清零且进度度量已记录（见 6）；
- 对应源码与上下文复核；
- 最小 `tools/i18n lint --strict`；
- 受影响术语的精确键、长文本投影和词族回归；
- `git diff --check`。

### 术语批次验证

- `python3 -B tools/audit_static.py`；
- `python3 -B tools/audit_dynamic.py`；
- `python3 -B tools/annotate_domains.py`；
- 对应领域覆盖率和排除清单重算。

### 最终门禁

按 `AGENTS.md` 顺序运行严格 lint、toolchain 单测、跨组件运行键扫描、重复键分类和 `git diff --check`；再运行适用构建与 smoke。

最终验收要求：

- A 类候选 100% 登记或有审计通过的排除理由；
- B 类候选 100% 完成裁决；
- 本轮范围内 `existing=0`，每个 `review` 都有明确缺失证据和后续责任；
- active preferred 无无法解释的缺失或 target mismatch；
- 未授权的精确键漂移、长文本术语漂移和词族漂移均为 0（投影按 5.3 精度策略运行，确认漂移清零，候选噪音以误报比记录并持续收紧规则）；
- category/domain/scope advisory 已裁决；
- 文档统计与 TSV 自动统计一致（TERMINOLOGY.md 已切换为自动生成或由门禁校验，不留手工口径）；
- 完整门禁通过后，进行一轮全新只读复审且无新的已确认 finding。

## 9. 下一步实施建议

1. 以本框架（含 2.2 规模、3.A 运行时标签归属、4.1 证据 rubric、5.3 投影精度策略、7.1 口径、7.2 分工）为契约；
2. **已完成**：只读生成器已在 `tools/audit_dynamic.py`（r2 inventory）落地并挂入 `audit_dynamic` 门禁，输出 `baseline + candidate-inventory + coverage + exclusions` 到 `.artifacts/i18n/terminology-review-r2/`；作用域口径写入 `tests/i18n/test_terminology_inventory.py`（15 项表驱动测试，2026-08-10 通过）；UNCLASSIFIED=0、覆盖率表与 2.1 完全一致、A 类缺失 1,001；
3. 以 P0/core 为试点：用实测分母验证排除规则抽样（首轮抽 ≥5% 或 ≥20 条）与投影误报比（见 5.3），试点后冻结 P1–P4 的最终分母与规模；
4. 按 P0→P4 逐批裁决（每批先冻结 findings 再统一修复），每批跑单批验证；
5. 全部批次收束后运行完整门禁与一轮全新只读复审。
