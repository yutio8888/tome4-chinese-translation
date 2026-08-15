# 本地化基础设施实施契约

> 状态：`contract/0.1`——Pilot A 验收完成（G1–G12 + G4b 共 13 行全部 PASS，报告落
> `.artifacts/i18n/contract-pilot-a/gates-report.md`）；Identity / Fingerprint /
> Baseline 三份 schema 的字节级公式自 rc3 起冻结。**PR 待办**：本版本的修订（§13
> 测试位置列映射修正、G4/G8/G10/G12 测试强化、L2 修复、cli.py DLC 根可移植、契约
> 套件接入 ci-gates.sh、talent.info / effect.desc 槽位补齐（002/003 迁移记录））尚未
> 推送/合并，PR 由用户另行指示；PR 合并后本版本正式生效。
> 修订历史见文末第十五节。
> 适用范围：本仓库（`tome4-chinese-translation`）工具链的增量扩展。本契约不替代
> 任何现有文档；与既有行为冲突时按第十二节「接口稳定性承诺」处理。

---

## 一、契约元信息

- **契约版本**：`contract/0.1`（Pilot A 验收通过；PR 待办，合并后正式生效，见状态行）
- **冻结范围**：Entity UID / TU UID / Revision UID 公式、Finding Fingerprint 公式、
  Baseline 文件格式（第十四节冻结条款）
- **阶段范围**：Phase 0（Identity + Fingerprint + Baseline）、Phase 1（Invalidation +
  MigrationMatcher 扩展）
- **依赖钉死**（沿用 `i18n/versions/tome-1.7.6.json`，本契约不改变任何 pin）：
  - engine：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（tome-1.7.6）
  - 官方 i18n_tools：`bdc19d22862f7a6cfbe71d7136145720ecea7bf7`（`git_path: i18n_tools`，
    位于 t-engine4 仓库内，含 luafish LPeg 解析器）
  - addon：`439d13496ea37de7aa1742d9407852502ac3d6af`
- **评审记录**：
  - `0.1` 初稿 → rc2：身份公式矛盾修正（10 条修订 + 3 测试）
  - rc2 → rc3：实现唯一性收口（6 条 freeze blocker + 3 条收紧）

---

## 二、术语表

| 术语 | 定义 |
|---|---|
| **Component（组件）** | 现有组件 id：`tome`、`boot`、`engine`、`ashes-urhrok`、`cults`、`orcs` |
| **Section（节）** | snapshot 中的 `section` 字符串（如 `mod-tome/data/talents/spells/fire.lua`）。生成逻辑沿用现有 extract 流程；diff→section 映射必须经过 §8.3 的 `source_git_path_to_section()` |
| **Editorial Key / ID** | `(section, source, source_tag)` 及其哈希 `stable_entry_id()`（lint.py 既有实现，见 §4.5，**不得变更**） |
| **Entity（实体）** | 游戏逻辑实体（talent / effect / entity / talent_type 等） |
| **EntityAnchor（实体锚）** | 从 AST 推导的实体定位三元组 `(component, kind, anchor_key)` |
| **weak_anchor（弱锚）** | `base` 回退、`name\|type\|subtype` 组合、`lore category` 等无运行时唯一性保证的定位信息；**只作 evidence，不进入 strong Entity UID** |
| **Entity UID** | 实体的侧车稳定身份（§4.5） |
| **Semantic Slot（语义槽）** | 由 Slot Registry 解析的规范化槽位（§4.6）；`source_tag` 与 `ast_path` 只是证据与绑定输入，不直接进入身份 |
| **Discriminator（判别符）** | 同 (Entity, Semantic Slot) 内多 TU 的稳定区分符（§4.7） |
| **TU（Translation Unit）** | 本地化最小单元，由 TU UID 标识 |
| **Revision（修订）** | 某一 TU 的具体 source 文本状态（§4.5） |
| **Finding（发现）** | 一条 QA 输出；既有的 `lint.Issue` 保持原样，新增 `FindingRecord` 包装模型（§6.3） |
| **Fingerprint（指纹）** | Finding 的跨重构稳定身份（§6.1） |
| **Baseline（基线）** | 某汉化仓库 commit 上全部 Finding 指纹的冻结快照（§7） |
| **extraction_confidence** | 提取确定性：元数据是否被确定性地从 AST 提取（§4.3） |
| **identity_binding** | 身份绑定等级：`strong` 或 `fallback-editorial`（§4.1）。与 extraction_confidence 是两个独立概念 |
| **Enrichment Pass** | 官方提取器同一次 Luafish AST traversal 的 sidecar 元数据产出（§4.3） |

---

## 三、架构切分（宪法性条款）

**§3.1 语言边界不可移。** 语义执行层（LuaJIT 5.1：官方 `i18n_tools`、`load_locale.lua`
bridge）与流程策略层（Python `i18nlib`）的分界维持现状。本契约新增代码**全部落在
Python 层**；如需扩展 Lua 层，只能以 `extract.py::_patch_extractor()` 补丁机制的形式
提交，并进入 pin 管理。

**§3.2 新增四模块：**

```text
tools/i18nlib/identity.py       # EnrichmentPass 消费、EntityAnchor、TUIndex、MigrationMatcher
tools/i18nlib/fingerprint.py    # FindingFingerprint 规范实现 + Rule Registry 加载
tools/i18nlib/baseline.py       # baseline 快照读写、状态计算、CI 门
tools/i18nlib/invalidation.py   # 三分域失效、依赖图、增量算法、自检
```

**§3.3 零破坏承诺：** 不加新 flag 时，`extract`/`lint`/`merge` 的默认输出与现状
字节一致；`build`/`publish`/`status`/`quality`/`review` 一律不改动。

---

## 四、身份契约

### §4.1 三层身份与绑定等级

```text
Editorial ID （既有）: 文本+位置的编辑身份。任何重构都可能变。保留为现有下游主键。
Entity UID   （新增）: 实体身份。观察性稳定；v0.1 不承诺跨 rename 不变（§4.8）。
TU UID       （新增）: 最小翻译单元身份，按绑定等级分两种 scheme（§4.5）。
```

`identity_binding` 两级：

- `strong`：有可靠 EntityAnchor（§4.4 强锚）与 Semantic Slot；
- `fallback-editorial`：无可靠锚或槽，按 Editorial ID 派生；此类 TU **不进入稳定
  迁移逻辑**，仅在报告中按 editorial 语义处理。

### §4.2 稳定性承诺（R1）

```
R1a（strong）:        同一 TU 的 source 变化 → Revision 变，TU UID 不变。
R1b（fallback-editorial）: source 变化 → Editorial ID 变 → TU UID 变。
R1c:                 TU UID 一经发出不重用；无结构区分证据的重复 occurrence
                     合并（coalesce），不制造伪稳定身份。
```

### §4.3 Enrichment Pass 产出契约

**来源条款（实现唯一性）：** Enrichment 元数据（`entity_kind` / `anchor_hint` /
`ast_path` / source occurrence）**必须**由官方 i18n_tools 的**同一次 Luafish AST
traversal** 产出，实现方式为 `extract.py::_patch_extractor()` 在 `--enrich` 模式下
追加 sidecar 输出 `i18n_enrichment.jsonl`（与 `i18n_list.lua` 同次运行产出）。
Python 层**禁止**对 Lua 源码做第二套解析（正则或自建 AST 均禁止）。

> Lua 只提供语法事实（raw hints），Python 负责 Slot Registry → EntityAnchor →
> TU UID 的身份政策。这与 §3.1 的语言边界一致。

默认无 `--enrich` 时：不生成 sidecar，extraction 输出字节不变。

sidecar 记录示例（每 occurrence 一行）：

```json
{
  "schema_version": 1,
  "section": "mod-tome/data/talents/spells/fire.lua",
  "line": 31,
  "source": "Flame",
  "source_tag": "talent name",
  "entity_kind": "talent",
  "anchor_hint": {"name": "Flame", "short_name": null, "type": ["spell/fire", 1]},
  "ast_path": "newTalent.name",
  "extraction_confidence": "deterministic"
}
```

Python 归一化后追加：

```json
{
  "identity_binding": "strong",
  "semantic_slot": "talent.name",
  "anchor": {"type": "derived_short_name", "value": "T_FLAME"}
}
```

`explicit_refs`（`DamageType.X` / `EFF_X` / `T_X` 等引用扫描）字段保留 optional，
**Pilot A 不设覆盖 Gate**，Phase 1/2 再扩展。

### §4.4 EntityAnchor 推导契约

`anchor_key` 按 kind 推导（**观察时刻计算并入库**，不随未来改名变化）：

| entity_kind | 锚等级 | anchor_type | 推导规则 | 示例 |
|---|---|---|---|---|
| `talent` | strong | `derived_short_name` | `"T_" + (显式 short_name 字段，否则 name):upper():gsub("[ ']", "_")`（与 `ActorTalents.lua:84-86` 完全一致） | `T_FLAME` |
| `effect` | strong | `effect_name` | `"EFF_" + name:upper()`（与 `ActorTemporaryEffects.lua:48,59-61` 完全一致） | `EFF_BURNING` |
| `talent_type` | strong | `type_string` | `type[1]` 字面值 | `spell/fire` |
| `entity`（显式 define_as） | strong | `define_as` | `define_as` 字面值 | `BASE_NPC_ANT` |
| `stat` | strong | `stat_short_name` | `defineStat` 第二参数 | — |
| `achievement` | strong（待验证唯一性） | `achievement_name` | name | — |
| `entity`（base 回退） | weak | `base_fallback` | `base` 链首项 | — |
| `entity`（name/type/subtype） | weak | `composite` | `name \| type \| subtype` 组合 | — |
| `birth` / `gem` / `ingredient` / `faction` | weak | 各自 name 字面值 | 仅作 evidence | — |
| `lore` | weak | `lore_category` | category | — |
| `module_meta` | — | `module_short_name` | init.lua `short_name`（不产生 TU 实体绑定） | `tome` |
| `free` | — | — | 不绑定，直接 `fallback-editorial` | — |

**边界情况（必须逐条实现）：**

- **BC1** name 不是静态字符串（函数/变量拼接）→ 该实体整块标记 UNKNOWN，不猜；
- **BC2** 同 (component, kind) 下 **strong anchor** 重复：
  - talent → `DUPLICATE_TALENT_ID`（ERROR，对应 `ActorTalents.lua:92` 加载期 assert）；
  - effect → `DUPLICATE_EFFECT_ID`（ERROR，对应 `ActorTemporaryEffects.lua:59` 加载期 assert）；
  - 其他 strong anchor → 按该 kind 的运行时唯一性证据分别定义，无证据则 `identity_conflict`（CONTEXT）；
  - **weak anchor** 重复 → `identity_conflict`（CONTEXT），**不产生 ERROR**；
- **BC2 加载语义（infra-contract-004 澄清）**：BC2 预检面向**实际被游戏加载**的定义。提取器会捕获
  未被任何 `load()` 入口加载的遗留文件（如被注释掉的 `--load(...)`、无加载引用的孤立文件），这些定义
  在运行时不会与其它定义冲突（`ActorTalents.lua:92` 的 assert 只对实际加载的定义生效）。因此
  duplicate-talent-id / duplicate-effect-id 的 **ERROR 产出**必须经过
  `i18n/quality/unloaded-sources-v1.json`（schema 1）豁免：site 全部落在豁免 section → 不产 ERROR，
  并在 binding/report 元数据列出 suppressed conflict；部分豁免 → 按剩余（已加载）site 判定，≥2 才产
  ERROR。**R6/FR3**：部分豁免后幸存 ERROR 的参与者只纳入出现在已加载 site section 的 TU（
  `tu.sections ∩ 剩余 site sections ≠ ∅`），unloaded-only TU（如豁免文件的 info slot）不得进入
  participants/subject/fingerprint；且参与者必须 `tu.kind == conflict.kind`、
  `identity_binding == "strong"`（同 anchor 文本的另一 kind 或 fallback TU 不得污染
  subject/fingerprint）；无参与者才回退 fallback。
  名单缺失/损坏 → fail-closed（ValidationError）。**raw identity conflict 永不删除**：
  identity.json / identity audit 始终保留全部 conflict（含被豁免的 ERROR 记录），豁免只作用于 Finding
  层。豁免名单为人工核实的加载入口证据，Python 层禁止做第二套 Lua 解析（§4.3 来源条款）；新增冲突的
  核实流程见 §15 迁移记录。
- **BC3** 提取器已知 tag 词汇表（"talent name"/"tformat"/"entity name"/…）为**证据**，不作为 slot 规范来源（slot 规范见 §4.6）。

### §4.5 哈希规范（冻结条款）

**Editorial ID**（既有实现，逐字引用，不得变更）：

```python
tag_value = "<nil>" if source_tag is None else f"<string>{source_tag}"
payload = "\0".join((component, section, source, tag_value))
editorial_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

**新增身份（rc3 定稿，双 scheme 分离）：**

```python
Entity UID   = sha256("entity\0" + component + "\0" + kind + "\0" + anchor_key)   # strong 锚专用

# strong binding
TU UID       = sha256("tu/strong\0" + entity_uid + "\0"
                      + semantic_slot + "\0" + discriminator)

# fallback-editorial binding
TU UID       = sha256("tu/fallback-editorial\0" + editorial_id)

Revision UID = sha256("rev\0" + tu_uid + "\0" + source_sha256)
```

- 所有拼接组件 UTF-8 编码，分隔符 `\0`，哈希为 hex digest；
- `source_sha256` = source 原文（无规范化）的 SHA-256；
- 两类 TU UID 通过 scheme 前缀做 domain separation，**不共用 `"tu"`**；
- 行为承诺：strong 下 source 变 → TU 不变、Revision 变；fallback 下 source 变 →
  Editorial ID 变 → TU 变。

### §4.6 Slot Registry 契约

新增 `i18n/quality/slot-registry-v1.json`，格式：

```json
{
  "schema_version": 1,
  "slots": [
    {"ast_path": "newTalent.name",       "semantic_slot": "talent.name"},
    {"ast_path": "newTalent.info",       "semantic_slot": "talent.info"},
    {"ast_path": "newEffect.desc",       "semantic_slot": "effect.desc"},
    {"ast_path": "newEntity.name",       "semantic_slot": "entity.name"}
  ]
}
```

解析规则：

```text
ast_path 已知且命中 registry → registry 定义的 semantic_slot
ast_path 已知但未登记        → "UNKNOWN:" + ast_path（不参与 strong binding）
ast_path 未知                → "UNKNOWN:" + source_tag（不参与 strong binding）
```

`source_tag` 仅作为 evidence 与绑定输入，**永不进入 TU 身份**。官方 extractor 未来
改变 tag 拼写（如 "talent name"→"talent_name"）不改变任何已冻结 TU UID。

### §4.7 Discriminator 契约

```text
单 TU 槽（talent.name / talent.info / effect.desc 等）→ discriminator = "default"
多 TU 槽 → 优先稳定结构键（AST 结构路径，如 combat_log:on_hit / message:activation）
无可区分结构 → coalesce 为同一 TU
```

**禁止**：source 文本、source 哈希、行号、出现序参与 discriminator。

### §4.8 事件契约（v0.1 简化）

两个 commit 间重算 Enrichment 后，对每 (component, kind) 生成事件流：

| 信号 | 事件 | 处置 |
|---|---|---|
| anchor、section 均存在且相同 | `unchanged` | 无 |
| 同 section 内 anchor A1 消失、A2 出现，且（同 slot 下）`SequenceMatcher(None, old_source, new_source, autojunk=False).ratio() ≥ 0.68` | `rename_candidate(A1→A2)` | **新 Entity UID**；产 migration-candidate（`automatic: False`，review_required） |
| anchor 消失且无候选 | `deleted` | Entity 标记 closed；其 TUs 标记 stale；不删历史报告 |
| 新 anchor 出现 | `created` | 新 Entity UID |
| 无法区分 renamed / deleted+created | `ambiguous` | 两条候选都登记，默认走 deleted+created，人工裁决 |
| 仅语义相似、无结构信号 | `hint` | 只提示，**禁止自动迁移 Curated 数据** |

**v0.1 不保留旧 Entity UID 跨 rename 不变**：无持久 identity ledger 前，rename 一律
产生新 UID + `rename_candidate` 链接。Phase 2 引入 Git 跟踪的 entity ledger 后再
恢复 alias 机制。

---

## 五、迁移匹配契约（MigrationMatcher）

扩展 `merge.py::_source_change_suggestions`，**不改其现有输出字段**（
`classification: "source-changed"`、`automatic: False` 保持兼容）。匹配层级
（rc3 定稿，自上而下命中即停）：

```text
L1 same Entity UID + semantic_slot + discriminator
   → direct binding（忽略 section）
   —— 同时吸收普通更新与文件移动；不产 migration candidate

L2 anchor changed + 结构性证据（同 section+slot、SequenceMatcher ≥ 0.68）
   → rename_candidate（automatic: False）

L3 同 section + fallback-editorial 兼容
   → 沿用现有 source-changed suggestion

L4 跨 section + fallback-editorial + 相似 ≥ 0.68
   → hint only（仅提示，不迁移 Curated 数据）

L5 其余
   → new TU（created）
```

- 文件移动（同 anchor 跨 section）由 **L1 自然吸收**：section 变、Entity UID 不变、
  TU UID 不变、相关 fingerprint 不变；
- 任何层级的自动迁移**都不**改写 canonical Lua 译文文件，只写入 TU 索引链接记录
  与报告；译文文件仍由现有 merge/人工流程处理。

---

## 六、Finding 指纹契约

### §6.1 指纹公式（冻结条款，rc3 定稿）

```python
fingerprint = sha256("\0".join([
    "fp/1",
    rule_id,
    str(rule_schema_version),              # rc3 新增
    subject_tu_uid,
    "\0".join(sorted(participant_tu_uids)), # 无参与者则为空串
    evidence_key,                           # §6.2
]).encode("utf-8")).hexdigest()
```

**契约性排除**（禁止进入指纹）：行号、逻辑路径、消息文本、severity、报告排序、
LLM 解释、模型置信度。

**行为承诺**：文件移动/行号漂移/无关文本修改 → 指纹不变；修复问题 → finding 消失；
参与实体变化 → 新指纹；**规则语义变更 → `rule_schema_version` bump → 新指纹**。

### §6.2 证据键规范化（按 Rule Registry 的 `evidence_key_spec`）

| evidence_key_spec | 规范化算法 | 示例 |
|---|---|---|
| `conversion-pair` | `"conv:" + 源转换序列 + "\|" + 目标转换序列`（序列 = 按出现顺序的 conversion 字符，`,` 连接） | `conv:d,d\|d` |
| `formatter-tag` | `"tag:" + source_tag + "\|args:" + canonical_args_order` | `tag:tformat\|args:2,1` |
| `constant` | 常量 | `empty` |
| `anchor-key` | `"dup:" + anchor_key` | `dup:T_FLAME` |
| `runtime-key` | `"collide:" + sha256(component∅source∅tag)[:16]`（与现有 `collision_id` 同源、不含 section） | — |
| `policy-ref` | `"pol:" + policy_id + "@" + policy_version`（Phase 2 启用） | — |

新增规则必须先在 Rule Registry 注册其 `evidence_key_spec`，否则指纹生成失败关闭
（fail closed）。

### §6.3 FindingRecord 与 Issue 的关系

**既有 `Issue` 及其 `to_dict()`（`asdict`）原样不动。** 新增包装模型：

```python
@dataclass(frozen=True)
class FindingRecord:
    issue: Issue
    rule_id: str
    rule_schema_version: int
    tu_uid: str
    participants: tuple[str, ...]
    evidence_key: str
    fingerprint: str
```

- `tools/i18n lint` 默认路径继续输出 `Issue.to_dict()`，字节不变；
- 仅 `lint --baseline` / `lint --incremental` 输出 FindingRecord。

---

## 七、Baseline 契约

### §7.1 冻结快照 + 环境元数据

```text
i18n/baselines/tome-<translation_commit>.jsonl        # 冻结后不修改
i18n/baselines/tome-<translation_commit>.meta.json
```

jsonl 每行（行序 = fingerprint 升序，同批更新字节级可复现）：

```json
{
  "schema_version": 1,
  "fingerprint": "…",
  "rule_id": "format-mismatch",
  "tu_uid": "…",
  "severity": "error",
  "status": "legacy_unreviewed"
}
```

meta.json：

```json
{
  "schema_version": 1,
  "component": "tome",
  "translation_commit": "…",
  "source_snapshot_sha256": "…",
  "engine_commit": "624a67329fe2ad440c5b344785a9c73fcf22ae63",
  "extractor_commit": "bdc19d22862f7a6cfbe71d7136145720ecea7bf7",
  "rules_registry_sha256": "…",
  "slot_registry_sha256": "…"
}
```

- `base_commit`（即文件名中的 `<translation_commit>`）定义为**汉化仓库 commit**：
  它回答"这一个翻译版本中，哪些 finding 已经是历史债务"；
- **生成环境不可重建的 baseline 视为失效**，禁止继续作为 CI 判定依据。

### §7.2 状态计算（不落盘）

```text
new      = current_findings − baseline
resolved = baseline − current_findings
```

`new` / `resolved` / `reopened` 等生命周期状态由每次运行计算，**不写入 baseline
文件**。Phase 2 需要何时 resolved/reopened 的历史时再引入独立 Finding History。

### §7.3 证据身份规则（B1，rc2 修正版）

```text
evidence identity changed → new fingerprint → 重新判定
same evidence identity    → same finding（保持 legacy_unreviewed）
```

即：历史存在 `%d` 缺失，译者仅把"造成大量伤害"改成"造成巨量伤害"而未补 `%d` →
证据键（conversion-pair）未变 → 同指纹、**保持 legacy**。另外报告
`legacy finding on touched TU` 提示供 reviewer 参考，**不升级为 NEW**。

### §7.4 CI 门语义

| 变化 | 行为 |
|---|---|
| new ERROR | **fail**（exit 1） |
| new WARNING | report（不 fail） |
| legacy ERROR | 技术债报告（默认折叠，`--legacy-report` 展开） |
| legacy WARNING | 静默（可查询） |

---

## 八、增量失效契约

### §8.1 依赖图

```text
Entity UID ──1:n──→ TU UID ──1:n──→ Revision UID ──1:n──→ Fingerprint
Entity UID ──1:n──→ Curated Record   （Phase 2 启用；v0.1 仅预留列）
```

### §8.2 三分域（rc2 新增）

`--incremental` 增加 `--domain ∈ {source, translation, rule}` 参数（缺省 source）：

| domain | 输入 diff | 处理 |
|---|---|---|
| `source` | engine 仓库 `base..head` | git path → `source_git_path_to_section()` → TU 集 |
| `translation` | 汉化仓库译文文件 diff | 按 Editorial/TU binding 找 target 变更的 TU，**不做 path→section 转换** |
| `rule` | Rule Registry / policy diff | 按规则依赖失效 findings |

### §8.3 `source_git_path_to_section()` 契约

新增纯函数：

```python
source_git_path_to_section(component, changed_git_path) -> str | None
```

规则（以 manifest 的 `sources[].git_path` / `mount` 为唯一依据）：

```text
game/modules/tome/data/talents/spells/fire.lua
        ↓ 相对 game/modules/tome
data/talents/spells/fire.lua
        ↓ 前缀 mount "mod-tome"
mod-tome/data/talents/spells/fire.lua
```

**Parity test（round-trip 形式）**：对每个真实 snapshot section → inverse mount 映射
→ 原始源路径 → `source_git_path_to_section()` → 必须恢复原 section。fixture 覆盖
`tome` / `engine` / `boot` 三个 mount。（注：官方 extractor 只对捕获到条目的文件
生成 section，因此**不得**用"全部 Lua 文件映射集合 == section 集合"做断言。）

### §8.4 增量算法与全量自检（rc3 定稿）

```text
增量: F_new = (F_previous − findings(affected)) ∪ recompute(affected)
全量: F_full = 对全部 TU 运行适用规则
自检: canonical(F_new) == canonical(F_full)     # 整体比较，非投影比较
```

**Canonical Form 规范**：FindingRecord 按 `(fingerprint, rule_id, tu_uid, severity,
code)` 五元组升序排序；记录内字段固定顺序（severity, code, message, logical_path,
line, entry_id, rule_id, rule_schema_version, tu_uid, participants, evidence_key,
fingerprint）；UTF-8、`\n` 行尾、无尾随空行。

**约束 I1**：无法解析 diff（非 Lua 文件、解析失败）→ 该 section 全部 TU 进入受影响集；
**约束 I2**：`git_source.py::GitRepository` 是唯一 git 交互通道，增量命令不得另建
git 调用路径；
**自检失败** → exit 2，差异文件写入 `.artifacts/i18n/`，CI 必失败。

**§8.4 消费链澄清（infra-contract-004）**：

- **affected 集 = base 受影响 ∪ head 受影响**：新实体 / 新 UID / 部分改名在 base 无对应 TU，必须从
  head 侧（staged 部分索引或 full-head 索引的受影响 section）收集，否则其 finding 会从 `F_new` 静默消失。
- **recompute/kept 是 issue 级而非纯 TU 级**：base 与 head 共用同一份 lint Issues；rename / new-UID /
  删除会使 Issue 的绑定 TU 变化（base TU → head TU 或 fallback TU）。记录必须在其 Issue 绑定到任一侧的
  affected TU 时重算，否则旧绑定会永远留在 kept，自检发散。
- **删除文件**：head 已删除的 blob 跳过 staging 并在结果 `deleted_files` 报告；仅删除导致空 stage 时不
  得因缺 `i18n_list.lua` 崩溃（使用空 head 索引）；被删 section 的 base TU 由 base 侧收集，recompute 后
  finding 自然消失，符合 `F_new` 公式。
- **冲突输入与 full head 等价（D4）**：单独提取受影响文件无法发现「新/修改文件与未改文件形成的
  duplicate anchor」。source 增量的 conflict 输入必须等价于 full head——对受影响 component 使用
  full-head identity index（`--self-check` 时直接复用其 full 提取，并同时作为绑定索引；**未开
  `--self-check` 时该 full index 同样用于绑定/重算（V8）**，否则 partial 绑定会漏掉未改文件提供的
  semantic-slot TUs，participants/fingerprint 与 full head 不一致），保证 incremental == full 字节一致。
  不得在 Python 层解析 Lua。
- **source `--ci` 语义（H3/FR2）**：只有 recomputed 中 severity=error 且 fingerprint 不在 base error
  fingerprints 的记录视为 new（fail）；base 已存在的 legacy ERROR 仅作技术债报告（不 fail）。
  `incremental_source_flow` 直接报告 `ci.new_errors` / `ci.legacy_errors` 及 new fingerprints，CLI
  不从最终全量 records 误计；`--ci` 且 new_errors>0 时 JSON/text `ok` 在任何 render 前置 False（与
  gate 一致），无 `--ci` 保持 V7（计数不置 ok）。
- **translation 域（H4/D5）**：主 translation 与 copy fragment 是**独立的逻辑文档**，各自分别加载
  base/head（head-only 文件 = base 缺失 → 该逻辑文档全部 head entries 受影响）；base records 必须代表
  真实 base（含 copy fragment finding），否则 kept 集错误。新增 / 删除 / 语义变化（target/args_order/
  special）双向收集进 affected；每个 changed editorial 映射 index candidates，无映射时必须加入
  `tu_uid_fallback(editorial_id)`（与 `build_finding_records::_bind` 一致），否则 head-only finding 会漏掉。
  **R2**：recomputed/kept 是 participant-aware——runtime-collision 的 subject 是 collision-id fallback，
  真实 editorial TUs 在 participants，subject 或任一 participant 属于 affected 即重算/移出 kept；同一
  collision（family key = (rule_id, issue.entry_id)，collision_id 由 component/source/source_tag 固定）
  在 base/head 两侧关联，任一侧 direct touched 则两侧都重算/移出（A+B → A+B+C 不得新旧并存）。
  **R5/R8**：同一 (section,source,source_tag) 可重复出现，affected 判定用每个 key 的 occurrence
  multiset（(semantic payload, line) 对，base/head 不同即 affected），不得用 dict 折叠最后一条；
  occurrence 证据（conversion-pair / formatter-tag）必须按 Issue 的 logical_path+line 精确绑定到该
  occurrence（唯一匹配；0 或 >1 ambiguous → fail-closed 不计入 evidence）。**FR1**：entity conflict
  的 identity context 不依赖 translation 文档是否存在——`records_for` 为每个 indexed component 确保
  component-key identity-only FindingContext（已有 main context 保留 entries），base 无主文档/head 新增
  时两侧均强绑定 participants。
- **rule 域（H4/D3）**：affected rule 由**完整签名** `(rule_id, schema_version, severity,
  evidence_key_spec)` 的 base/head 差异驱动（同 rule_id 的 schema/severity/evidence bump 会改变指纹，
  必须重算）；registry/policy 读取与解析 fail-closed（缺失/损坏不得静默回退）。`i18n/policy.json` 三个
  allowlist 只被 `format-mismatch` / `format-shape-difference` / `empty-target` /
  `runtime-collision` 四条规则消费（D3 已核 `lint.py` 消费关系），policy 变化只重算这四条。
  **R3**：Rule Registry 的 severity 对 enriched finding 权威（§9）——`build_finding_records` 以
  registry severity 重建记录的 Issue，message/path/line/entry_id 不变；`Issue` 类、`to_dict` 与默认
  lint 输出零改动（format-shape-difference 在 enriched 路径按 registry 为 error，§9.2 契约表）。
  **R4**：`i18n/quality/unloaded-sources-v1.json` 是 rule 域依赖——变化影响 duplicate-talent-id /
  duplicate-effect-id；base/head 各从对应 commit blob 严格加载（missing/corrupt fail-closed），base
  records 用 base 注册表、head records 用 head 注册表，no-change early return 纳入该依赖。
- **baseline entity ownership（V1）**：duplicate entity finding 的 `Issue.logical_path` 是 source
  section，不是译文路径；baseline freeze/report/`lint --baseline` 的组件归属必须同时使用译文路径映射与
  **TU 身份证据**（subject/participants 所在 component index），不得字符串匹配 section。
- **Git head blob 语义（V4）**：translation 与 rule 域从 resolve 后的 base/head commit blobs 读取
  文档/registry/policy，不依赖 worktree（未提交内容不得冒充 head）；`GitRepository.read_blob_optional`
  是唯一「可选读」通道——只有确实不存在的 blob 返回 None，git 失败/ambiguous/非 regular/cat-file 失败
  与 Lua loader 错误一律 fail-closed 抛错。
- **rename 双路径（R1）**：`GitRepository.changed_paths()` 使用
  `git diff --no-renames --name-only -z`，检测到的 rename 同时返回 preimage 与 postimage 路径，旧
  section 的 base TU 进入 affected（否则 rename 后旧 finding 残留增量集）。
- **identity.json schema（V5）**：`ComponentIndex.to_dict()` 携带 `schema_version: 1`，
  `read_index_files` 的 conflicts 恢复严格要求 1（缺失/非 1 fail-closed）；旧 artifact 重新 extract。

---

## 九、规则注册契约（Rule Registry）

### §9.1 注册表 schema

`i18n/quality/rules-registry-v1.json`：

```json
{
  "schema_version": 1,
  "rules": [
    {
      "rule_id": "format-mismatch",
      "schema_version": 1,
      "severity": "error",
      "trust_class": "A",
      "subject_kind": "translation_unit",
      "evidence_key_spec": "conversion-pair",
      "pilot": "A"
    }
  ]
}
```

- 注册表内没有的 rule_id 不得产出带 fingerprint 的 Finding（fail closed）；
- trust_class ≠ A 的规则在 Phase 0/1 一律禁用（fail closed）。

### §9.2 Pilot A 规则清单（1:1 映射现有 lint，不重构 taxonomy）

| rule_id | 来源 | evidence_key_spec | severity |
|---|---|---|---|
| `format-mismatch` | 现有 lint 码（lint.py:225） | `conversion-pair` | error |
| `format-shape-difference` | 现有 lint 码（lint.py:268） | `formatter-tag` | error |
| `empty-target` | 现有 lint 码（lint.py:344） | `constant` | error |
| `runtime-collision` | 现有 lint 码（lint.py:442） | `runtime-key` | error |
| `duplicate-talent-id` | **新增**（ActorTalents.lua:92 assert 预检） | `anchor-key` | error |
| `duplicate-effect-id` | **新增**（ActorTemporaryEffects.lua:59 assert 预检） | `anchor-key` | error |

- `PLACEHOLDER_MISSING` / `PLACEHOLDER_EXTRA` 细分推迟到底盘验收后；
- `CURATED_POLICY_VIOLATION`（`pol:POL-0001@2`）属 Phase 2，**不在 Pilot A**（现有
  `policy.json` 只有三组 entry_id allowlist，无 policy identity/version）。

### §9.3 证据分级与权限上限（Phase 0/1 只启用 A）

| trust_class | 定义 | 权限上限 |
|---|---|---|
| A | deterministic（官方提取、AST 字面、占位符序列） | ERROR |
| B | calibrated high precision | WARNING（Phase 2 开放，须附 gold set 校准报告） |
| C | useful inference | CONTEXT |
| D | exploratory | CONTEXT only |

模型自报置信度**永不**作为 trust_class 依据。

---

## 十、存储契约

### §10.1 `identity.sqlite`（`.artifacts/i18n/identity/identity.sqlite`）

**v0.1 为 current-state cache（方案 A）**——不存不可重建历史：

```sql
entities(entity_uid TEXT PK, component, kind, anchor_key, status)
translation_units(tu_uid TEXT PK, entity_uid, semantic_slot, discriminator,
                  editorial_id, identity_binding)
revisions(revision_uid TEXT PK, tu_uid, source_sha)
findings(fingerprint TEXT PK, rule_id, rule_schema_version, tu_uid,
         participants, evidence_key)
baseline_lookup(fingerprint TEXT PK, baseline_file, status)
```

- `first_seen_commit`、rename/delete 历史、旧 anchor **不入库**；
- rename 事件以 migration report 输出（`.artifacts/i18n/`）；
- Phase 2 引入 Git 跟踪的 `i18n/identity/entity-ledger.jsonl` 后再扩展历史表。

### §10.2 重建确定性

- SQLite 可随时删除，从（snapshot.jsonl + tu_index.jsonl + 译文文件 + rules
  registry + slot registry + baseline 快照）重建；
- **Canonical Dump**：重建后按表序输出 INSERT（行按主键升序、值按列序），SHA-256
  与上次一致。任何不确定性（dict 顺序、时间戳）禁止进入库。

---

## 十一、CLI 契约

```text
tools/i18n extract --enrich                        # 追加产出 sidecar + tu_index.jsonl + 更新 identity.sqlite
tools/i18n identity show <tu_uid>                  # 该 TU 的 anchor/slot/revision/绑定等级
tools/i18n identity audit                          # UNKNOWN 率、冲突数、rename 待裁决队列
tools/i18n lint --baseline <translation_commit> [--ci]
tools/i18n lint --incremental <base>..<head> --domain <source|translation|rule> [--self-check] [--ci]
tools/i18n baseline report                         # new / legacy / resolved 统计
```

Exit codes：`0` 通过；`1` 存在 new ERROR（--ci 模式）；`2` 增量自检不一致；
`3` 内部错误（契约违反、注册表缺失、pin 校验失败）。

---

## 十二、接口稳定性承诺

1. 现有命令默认路径输出字节不变（§3.3 为验收硬门）；
2. `Issue` 及其 `to_dict()` 原样不动（§6.3）；
3. `merge` 现有字段与分类语义不变，仅新增 L1/L2/L4 锚定逻辑；
4. 所有新 artifact 只写入 `.artifacts/i18n/` 与 `i18n/baselines/`，不触碰
   `*.lua` 规范译文、`terminology/`、`i18n/quality/` 现有文件；
5. 违反上述任一条 → 该改动不属本契约，按普通评审流程处理。

**澄清（contract-pilot-a-g10）**：slot-registry（`i18n/quality/slot-registry-v1.json`）的
ast_path→semantic_slot **数据行增补**属注册表数据变更（§4.6），不属上述第 4 条所指的
「`i18n/quality/` 现有文件」quality 内容冻结范围；但此类增补会改变 `slot_registry_sha256`，
凡影响已冻结 baseline 元数据者，仍须按第十五节规则 3 评估并执行迁移方案（如
`docs/localization-infra-contract-v0.1-migration-g10.md`）。

---

## 十三、Pilot A 验收 Gate 与测试映射

| # | Gate | 判定方法 | 测试位置（实际文件:方法） |
|---|---|---|---|
| G1 | 既有全量回归（doctor/extract/lint/build/publish）字节不变 | 新旧两版本输出 diff 为空（跨版本字节对比，见 Pilot A gates-report） | `tests/i18n/test_toolchain.py` + quality/Facts 套件（ci-gates.sh 步骤 3–4） |
| G2 | spell/fire 范围候选 100% 进入 TU 索引 | extract --enrich 后索引覆盖 snapshot 全部定义 | `tests/i18n/identity/test_stability.py::CoverageTests::test_g2_index_covers_snapshot` |
| G3 | benign refactor（空行/注释/移文件/字段重排）下 TU UID 100% 稳定 | 合成 mini-tome fixture 七变换 | `tests/i18n/identity/test_stability.py::StabilityTests::test_g3_benign_transforms` |
| G4 | 英文改名触发 rename_candidate | `"Burning Shock" → "Burning Stun"`（ratio 0.7200，同 section 同 slot）→ rename_candidate + automatic=False | `tests/i18n/identity/test_identity.py::RenameEventTests`（test_g4_rename_candidate + test_g4_rename_merge_suggestion_is_not_automatic） |
| G4b | 改名+去空格（anchor 推导亦变） | `"Flame Bolt" → "Flamebolt"`（ratio 0.8421）→ 同上 | `tests/i18n/identity/test_identity.py::RenameEventTests`（test_g4b_rename_with_despace + test_g4b_rename_merge_suggestion_is_not_automatic） |
| G5 | 指纹六变换 100% 稳定 | §6.1 行为承诺逐条断言 | `tests/i18n/fingerprint/test_fingerprint.py` + `tests/i18n/fingerprint/test_findings.py` |
| G6 | 注入占位符缺陷检出率 100%、A 类 ERROR 误报 0 | fixture 缺陷集 | `tests/i18n/qa/test_injected_defects.py` |
| G7 | Baseline 区分 legacy/new 100% | 注入→检出 new→修复→resolved | `tests/i18n/baseline/test_baseline.py::BaselineLifecycleTests::test_g7_new_legacy_resolved` |
| G8 | 增量 == 全量（canonical 字节级，整体比较） | 修改 T_FLAME 数值后自检 | `tests/i18n/incremental/test_incremental.py`（test_g8_canonical_self_check + IncrementalSourceFlowTests::test_g8_incremental_source_flow_end_to_end） |
| G9 | identity.sqlite 重建 canonical dump 一致 | 删库重建两次 SHA 相同 | `tests/i18n/identity/test_stability.py::RebuildTests::test_g9_rebuild_determinism` |
| G10 | **仅改 source 文本（info）** → TU UID 不变、Revision UID 变 | `"Deals fire damage." → "Deals increased fire damage."`（strong binding；实际载体 = `talent.info` 槽，原位重分类，见迁移记录） | `tests/i18n/identity/test_identity.py::RevisionSemanticsTests::test_g10_revision_changes_tu_stays` |
| G11 | 无意义译文措辞修改 → 指纹不变、保持 legacy | `"造成大量伤害" → "造成巨量伤害"`（未补 %d） | `tests/i18n/baseline/test_baseline.py::BaselineLifecycleTests::test_g11_b1_same_evidence_stays_legacy` |
| G12 | 源文件移动 → section 变、Entity/TU/相关指纹不变（L1 吸收） | 移动 fixture + §8.3 round-trip parity（tome/engine/boot 三 mount） | `tests/i18n/identity/test_identity.py::FileMoveTests::test_g12_move_section_only` + `tests/i18n/incremental/test_incremental.py::SectionMappingTests::test_round_trip_parity` |

**Gate 语义**：任一 Gate 失败 → 不进入 Phase 2，不合并相关 PR。G1 是前置闸
（先行执行）。G10 优先级高于 G3（source 文本变化是身份层最危险的变换）。

---

## 十四、Non-Goals（v0.1 明确不做）

1. 不引入 tree-sitter 或任何第二套 Lua 解析（§4.3 来源条款）；
2. 不改引擎运行时、不改官方 locale 加载语义；
3. 不重写 quality v2/v3 claims 系统（facts study 裁定 `do-not-promote-facts-channel`
   继续有效，见 `docs/translation-quality-facts-study-report-v1.md`）；
4. 不迁移 policy allowlist 的 entry_id 键（Phase 2）；
5. 不做 Governance 生命周期（draft→superseded→retired）、Context Packet 预算/Profile、
   Namespace overlay 解析（Phase 2）；
6. Phase 0/1 禁用一切 LLM 与 trust_class ≠ A 的规则；
7. 不做完整实体知识图谱；free 类字符串不伪造身份；
8. **不引入持久 entity-ledger**（Phase 2；因此 rename 不保留旧 Entity UID，见 §4.8）；
9. `explicit_refs` 不做覆盖 Gate（Phase 1/2 扩展）。

---

## 十五、契约演进规则

**修订历史：**

| 版本 | 内容 |
|---|---|
| `0.1`（infra-contract-005 修订） | **Baseline provenance + 消费 fail-closed 加固**（外部独立架构审计确认 2 High + 1 中）：H1 `baseline freeze --commit` 现在解析为完整 commit OID 并要求等于汉化仓库 HEAD、tracked/index 工作树干净，文件名/meta 改用规范化完整 OID（`_verify_freeze_provenance` + 新增 `GitRepository.worktree_porcelain()`，`--commit` 仍必填、不改默认行为）；H2 `write_baseline` no-clobber——同名 baseline 已存在时仅字节完全相同视为幂等返回、差异或半套（meta/jsonl 缺一）拒绝覆盖（§7.1 冻结快照不修改）；H3 `read_baseline` 严格校验 meta 身份——键集恰为契约 8 键、`schema_version==1`、`component`/`translation_commit` 与请求标签一致，损坏/错挂/半套一律 ValidationError fail-closed；H4 消费链 fail-closed——新增 `_load_required_baselines` 以 `pipeline["indexes"]` 确定必须有 baseline 的组件（只有不可复现提取的组件允许显式 `skipped`），缺失/损坏组件 ValidationError 而非静默 `continue`，空有效集合不得返回成功（`baseline report`/`lint --baseline` 的 `all([])` 假阳堵死）；H5 `tools/ci-gates.sh` step 5 补入 `tests/i18n/identity/test_conflicts.py` 与 `tests/i18n/incremental/test_domains.py`（infra-contract-004 已列为其验证依据）。冻结公式 §4.5/§6.1/§7.1 与既有 baseline 字节零改动（meta 键集与既有 8 组件 baseline 完全一致，实测 `baseline report`/`lint --baseline` 对 commit `1cff3d6…` 全绿）；新增测试 `tests/i18n/baseline/test_baseline.py` 的 `MetaIdentityFailClosedTests`/`NoClobberFreezeTests`/`FreezeProvenanceTests`/`RequiredBaselinesLoaderTests`。**PR 待办**：本修订未推送/合并，PR 由用户另行指示。 |
| `0.1`（infra-contract-006 修订） | **one-to-many Finding 绑定修正**（外部独立架构审计 DICA finding）：`build_finding_records` 对**非 runtime-key 的 translation_unit 规则**（empty-target/format-mismatch/format-shape-difference）现以 `_bind(issue.entry_id, contexts)` 的**完整共享 TU 集**为 `participants`、`subject = participants[0]`（按字节序首位），使 §6.1「参与实体变化→新指纹」承诺落地——增删任一共享 TU（如多个 `newEntity` 共享同一 `(component,section,source,source_tag)` 但强锚不同、§4.7 保持 distinct）现正确产生新指纹，而非静默复用 sorted()[0]。runtime-key 分支（runtime-collision）**维持现状不动**：subject 仍为 collision fallback、聚合真实 TU 集为 participants，既有 runtime-collision 指纹语义保持稳定（用户修正第 1 点）。R8 location-aware evidence（按 `logical_path+line` 精确匹配 occurrence）不受影响；evidence_key_spec 分发（runtime-key→constant→其余）重构后语义不变。仅纠正指纹输入语义，**不触碰 §4.5/§6.1/§7.1 冻结字节与公式实现**；当前 8 组件 baseline 全为 0 finding，无需重冻 baseline，属「契约冻结条文未变、实现补回契约承诺」，不需 §15 冻结条款迁移方案，亦无独立 migration 文件。新增回归：`tests/i18n/fingerprint/test_findings.py::OneToManyParticipantBindingTests`（共享 editorial 绑定完整 participants、participant 集 2→3 产生新指纹、runtime-key subject 保持 collision fallback）与 `tests/i18n/incremental/test_domains.py` 端到端消费链用例（共享 editorial 的 empty-target finding 在共享 occurrence 变化时进 recompute、participants 绑定完整共享集、incremental canonical == full-head canonical、resolve 时无残留旧指纹）。**PR 待办**：本修订未推送/合并，PR 由用户另行指示。 |
| `0.1`（infra-contract-004 修订） | **消费链缺口修复**（外部评审 4 High + 复审 V1–V10 + 初审 review R1–R7 + 复审 cycle 3 R2/R8/R9 + closure cycle 4 FR1–FR3，见 `docs/localization-infra-contract-v0.1-migration-004.md`）：H1 duplicate-id 规则进 Baseline/CI——`read_index_files` 新增 `conflicts_path`（严格从 identity.json 恢复 IdentityConflict，缺失/损坏/schema/字段/组件不匹配 ValidationError fail-closed；`ComponentIndex.to_dict()` 携带 `schema_version: 1` 并严格要求；None → 空 conflicts 兼容 merge）；pipeline/`_store_enrichment_artifacts`（current-index 扫描 fail-closed：任一 index artifact 存在即要求三件套齐全、ValidationError 冒泡）/`_current_indexes_for` 均传 identity.json；新增 `i18n/quality/unloaded-sources-v1.json`（schema 1，两条 SPEC 所列 section+evidence），仅在 duplicate-talent-id/duplicate-effect-id ERROR 产出时按 section 豁免（全豁免不产 ERROR 并列出 suppressed conflict——含实际命中 section 的 registry evidence；部分豁免按剩余 site ≥2 才产 ERROR；名单缺失/损坏 fail-closed），raw conflict 保留可见、弱锚 CONTEXT 不变；H2 source 增量 affected = base∪head（新 TU/新 UID 不漏）、删除 blob 跳过 staging 并在 `deleted_files` 报告（仅确实不存在的 blob 视为删除，`GitRepository.read_blob_optional` 为唯一可选读通道）、空 stage 不崩溃、recompute/kept 升级为 issue 级（rename/new-UID 自检一致）；D4 source 增量 conflict 输入与 full head 等价（受影响 component 用 full-head identity index，`--self-check` 时复用并作绑定索引），不启用 self-check 也检出跨文件 duplicate-anchor，且受影响 component 的 full-head index 同时用于 head 绑定/重算（V8，participants/fingerprint 与 full-head 组装完全一致）；identity.json conflicts 按封闭模型逐字段校验（V9）；`_current_indexes_for` 与 extract 共用 fail-closed 扫描（V10）；H3 source `--ci` 只把 recomputed error 且 fingerprint ∉ base error fingerprints 视为 new（legacy ERROR 仅报告不 fail），flow 直接报告 new/legacy 计数与 new fingerprints；H4 translation 主文件/copy fragment 独立逻辑文档从 base/head commit blobs 分别加载（不依赖 worktree）、双向比较新增/删除/语义变化、无 index 映射用 `tu_uid_fallback(editorial_id)`；baseline 组件归属含 TU 身份证据（entity finding 的 section logical_path 不丢失）；rule 域按完整签名比较，registry/policy 从 base/head blobs 构造并 fail-closed，policy 三个 allowlist 仅影响 format-mismatch/format-shape-difference/empty-target/runtime-collision 四规则，registry severity 对 enriched finding 权威（R3）、unloaded-sources 注册表为 rule 域依赖（R4）；rename 用 `--no-renames` 双路径（R1）、translation recompute participant-aware 且 editorial 比较用 multiset（R2/R5）、partial exemption 参与者限已加载 site（R6）、identity-only artifact fail-closed（R7）、runtime-collision family 跨侧关联与 occurrence 证据精确绑定（cycle 3 R2/R8）、空 exemption registry 合法（R9）；entity conflict identity context 不依赖文档存在（FR1）、source JSON ok 与 CI gate 一致（FR2）、duplicate participants 限同 kind strong（FR3）；ci 计数始终报告、仅 `--ci` 纳入 gate（V7）。冻结公式（§4.5/§6.1/§7.1）与既有 baseline 字节零改动；新增测试 `tests/i18n/identity/test_conflicts.py`、`tests/i18n/incremental/test_domains.py` 及 test_incremental.py 的 H2/D4/H3 生产链测试（含 V1–V7 回归）；真实数据：396 conflict 恢复、T_IRON_WILL/T_TWILIT_ECHOES 均豁免不产 ERROR（raw 仍可见）、8 组件 baseline 无影响。**PR 待办**：本修订未推送/合并，PR 由用户另行指示。 |
| `0.1`（评审 advisory 归档） | 外部复审非阻塞意见归档，防静默漂移：**A2（遗留）**——增量命令的 `resolve_commit` 对不可解析 pin 抛 `ContractError`（exit 3），而 legacy `validate()` 仍抛 `ConfigurationError`（exit 2，零破坏保留，未统一）；**A3**——§8 约束 I1 契约要求「解析失败 → 该 section 全部 TU 受影响」（section 级），实现为 **component 级加宽**（incremental.py 解析失败时全组件受影响，保守过度近似、安全但粗于契约文字）。两者均为已知 advisory，留待下次修订行确认或修正。 |
| `0.1`（infra-contract-003 修订） | **effect.desc 槽位实现**（契约 §4.6 示例槽位 `newEffect.desc`，机制同 talent.info 原位重分类）：官方提取器 newEffect 分支对**顶层 desc 字段**字面量（直接 `_t"…"`、function 单 Return 的 tformat/`_t`、`table.merge(…,{name,desc})` 受限支持——仅 merge 末参为 Table 且 name/desc 静态）注册 AST 节点，通用 `_t`/`tformat` 分支改发 `ast_path="newEffect.desc"` 记录（确定性锚 `EFF_`+name:upper()）；locales 写入与 source_tag 逐字节不变，tDef 数/source_snapshot_sha256/i18n_list.lua 字节不变，sidecar 总记录数逐组件与变更前一致，每 occurrence 恰一条记录、无同 editorial ID strong+fallback 双映射；字段边界：仅构造器（或 merge 覆写表）**顶层** Field 键严格 `== "desc"`，`display_desc`/`long_desc`/局部 desc 字面量/floorEffect.desc 保持 free。真实数据 **805 个 strong-deterministic**（tome 588/boot 2/ashes 38/cults 69/orcs 108），5 个动态工厂/变量表 captured-nondeterministic-fallback、2 个 example 纯字符串 not-captured、floorEffect 边界 15；共享 desc 一对多 TU 21 组（含 GREATER_INVISIBILITY/INVISIBILITY 同 `Invisibility`）；覆盖矩阵与回滚边界见 `docs/localization-infra-contract-v0.1-migration-effect-desc.md`；slot-registry 23→24 项 → slot_registry_sha256 变更（`8602a990…` → `75c59d774d23402f6b910c0e4e843329cea513ef1008f02e3721326acbde6645`）→ 按规则 3 完成 **baseline 重冻**（8 组件 × 2 文件，commit `1cff3d6f3b3a061624e5f74bd80c4d7e8186fd25`，旧 `*-cd42f9a*`/`*-29da216*` 基线文件字节不变、全部 0 条 finding；`baseline report` ok=True、components=8）。测试：`EffectDescSlotTests` 8 项（强绑定 revision 语义、三态覆盖矩阵、字段边界负向 display/long/local desc 与 floorEffect、table.merge 受限、一对多 shared desc）。**PR 待办**：本修订未推送/合并，PR 由用户另行指示，PR 合并后 `contract/0.1` 正式生效。 |
| `0.1` | **Pilot A 正式验收**：G1–G12 + G4b 共 13 行全部 PASS（gates-report 落 `.artifacts/i18n/contract-pilot-a/`）。§13 测试位置列修正为实际文件:方法（原引用的 test_coverage/test_rename/test_revision/test_rebuild/test_move/test_b1.py 不存在，实际落点见第十三节）。测试强化：G4/G4b 断言 merge 输出的 **L2 迁移建议**（match_level L2、携带旧译文、automatic=False）；G8 改为**生产 `incremental_source_flow` 端到端**（合成 git 仓库 base→head 修改 T_FLAME 数值，真实 diff/受影响集/staged 部分提取/recompute/self-check，仅 stub 全量提取步骤，增量==全量字节级）；G10 已以 talent.info 强绑定落实（契约示例槽位 `newTalent.info` 实现：官方提取器 newTalent 分支对 info 字段单字面量模板做**原位重分类**——`_t`/`tformat` 通用捕获的同一 occurrence 改发 `ast_path="newTalent.info"` 记录，locales 写入与 source_tag 逐字节不变，tDef 数/source_snapshot_sha256/i18n_list.lua 字节不变，无同 editorial ID strong+fallback 双映射；真实数据 **1836 个 strong-deterministic**（tome 1373/ashes 88/cults 109/orcs 266），5 个 captured-nondeterministic-fallback、15 个 not-captured、14 个动态调用，覆盖矩阵与回滚边界见 `docs/localization-infra-contract-v0.1-migration-g10.md`）；slot-registry 22→23 项 → slot_registry_sha256 变更 → 按规则 3 完成 **baseline 重冻**（8 组件 × 2 文件，commit `cd42f9aedd365b398e69b472326d953055f7f9fe`，旧 `*-29da216*` 基线文件字节不变、全部 0 条 finding）；G12 补 Entity UID 与相关指纹稳定性断言 + §8.3 parity 覆盖 boot。实现修复（均经裁决 ACCEPT）：`match_migrations` L2 映射（rename_events_by_new）、L2 `previous_definition` 解析（merge 输出 L2 suggestion 携带旧译文）、L2 空 match 回退 L5（旧实体缺槽/歧义时不 emit 空 L2，落回 L5/legacy 路径，source-changed suggestion 不静默丢失，回归测试 test_rename_unmatched_slot_falls_back_to_legacy_suggestion）与 rename 反向唯一性校验（多旧实体→同一新实体不 emit L2、落 L5/legacy，不携带任意旧译文，回归测试 test_rename_two_old_entities_to_one_new_never_l2）；cli.py DLC 根可移植（TOME_PUBLIC_DLC_ROOT → ~/projects/tome4-dlcs → 原回退）。契约套件接入 `tools/ci-gates.sh`（显式测试文件列表）。**PR 待办**：本版本全部修订未推送/合并，PR 由用户另行指示，PR 合并后 `contract/0.1` 正式生效。 |
| `0.1` 初稿 | 六层架构 → 既有工具链差距分析；身份/指纹/基线/失效四模块设计 |
| `0.1-rc2` | 修正身份公式矛盾：discriminator 禁止 source hash、Revision 绑定 TU、Slot Registry、fallback 无跨 source 承诺、rename_candidate、删 M1、`source_git_path_to_section()`、三分域、FindingRecord、baseline 冻结快照；DUPLICATE 分 kind（talent/effect 均有加载期 assert） |
| `0.1-rc3` | 实现唯一性收口：双 scheme TU UID（`tu/strong` / `tu/fallback-editorial`）、`rule_schema_version` 进指纹、Enrichment 走官方 luafish 同次遍历 sidecar、G4/G10 fixture 修正、迁移层级五级化（L1 吸收文件移动）、baseline 环境元数据；parity round-trip、`extraction_confidence` 与 `identity_binding` 分名、`explicit_refs` 延后 |

**规则：**

1. 本契约以 `contract/0.1-rc3` 入库；G1–G12 全部通过后正式标记 `contract/0.1`；
2. 修订 = PR + 评审记录，修订后版本号递增（rc4、0.1、0.2…）；
3. 涉及**冻结条款**（§4.5 身份哈希、§6.1 指纹公式、§7.1 baseline 格式）的修改 →
   **必须**同时提交迁移方案（旧指纹/旧 TU UID 的重新登记流程），否则拒绝；
4. 契约与实现冲突时：**契约胜**——实现先行修正，或走修订流程；不允许"实现正确、
   契约落后"的静默漂移；
5. **冻结时机**：在第一份真实 baseline 生成之前，TU UID 与 Finding Fingerprint 的
   字节级公式必须彻底冻结；一旦真实历史数据开始依赖它们，修改成本将明显上升；
6. Phase 2 启动前，本契约必须完成一次评审修订（吸收 Pilot A 实测教训）。
