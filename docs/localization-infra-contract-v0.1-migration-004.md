# migration-004 — infra-contract-004 消费链缺口修复

> 修订版本：`contract/0.1`（infra-contract-004 修订）
> 冻结条款：§4.5 身份哈希、§6.1 指纹公式、§7.1 baseline 格式 —— **零改动**
> 关联契约章节：§4.4（BC2 加载语义澄清）、§8.2/§8.4（增量澄清）、§9（规则签名澄清）、§15（修订历史）

## 1. 背景与证据链（外部评审 4 High）

接管时真实 identity artifact `.artifacts/i18n/identity/current/` 含 8 组件索引：**396 个 conflict**，
其中仅 2 个 ERROR，其余均为 weak `identity_conflict`（CONTEXT）：

| 组件 | code | anchor | sites |
|---|---|---|---|
| tome | duplicate-talent-id | `T_IRON_WILL` | `mod-tome/data/talents/psionic/focus.lua:149`、`mod-tome/data/talents/psionic/mental-discipline.lua:55` |
| orcs | duplicate-talent-id | `T_TWILIT_ECHOES` | `tome-orcs/data/talents/celestial/crepescula.lua:3`、`tome-orcs/data/talents/celestial/void.lua:122` |

### H1 duplicate-id 规则未进 Baseline/CI

- `build_component_index` 正确计算 BC2 conflicts 并写入 `identity.json`（`ComponentIndex.to_dict` 含
  conflicts）；但 `read_index_files` 从 `entities.jsonl` + `tu_index.jsonl` 重建时**硬编码
  `conflicts=()`**，pipeline `extract_enriched` → `run_enriched_lint`/incremental/rule/translation 域
  收集到的 `index.conflicts` 恒为空 → `build_finding_records` 的 conflicts 分支永不产出 duplicate-id
  Finding → 基线空、report 0 ERROR。
- **加载语义误报边界（关键）**：
  - `T_IRON_WILL`：focus.lua 与 mental-discipline.lua 各定义 `newTalent{name="Iron Will"}`（独立定义、
    不同 type）；但 `game/modules/tome/data/talents/psionic/psionic.lua:174` 为
    `--load("/data/talents/psionic/mental-discipline.lua")`（**注释掉**），focus.lua 被加载
    （psionic.lua:184）。运行时无冲突（`ActorTalents.lua:92-93` 加载期 assert 只对实际加载定义生效）。
  - `T_TWILIT_ECHOES`：crepescula.lua 与 void.lua 各定义一次；`celestial-empyreal.lua:27-31` 只加载
    sol/cosmic/energies/reflection/void.lua，**crepescula.lua 无任何加载引用**。void.lua 被加载。
  - 两冲突均来自**未加载遗留文件**：直接恢复透传 → 2 个误报 ERROR。

### H2 source 增量漏新 TU

- `incremental.py` 原 `affected_tus` 仅从 base 索引收集 → head 新实体/新 UID/部分改名在 base 无对应
  TU → 不进 affected → 新 TU finding 从 `F_new` 静默消失（不跑 self-check 时不报）。
- `_stage_affected_files` 对 head 已删除文件 `read_blob` 抛 `ExtractionError`（missing blob），且在
  try 之外 → 删除文件直接崩溃；仅删除导致空 stage 时缺 `i18n_list.lua` 也会崩。

### H3 source `--ci` 全量 ERROR 当 new ERROR

- `cli.py` 原 `new_error_count = sum(severity == "error")` 遍历最终全量 records，未与 base
  （F_previous）error fingerprints 求差 → base 存在合法 legacy ERROR（技术债）时增量 CI 误失败。

### H4 translation/rule 域缺口

- translation 域：base 文件缺失（head-only 新文件）→ `continue` → head-only 新条目不进 affected 且
  base_records 缺该组件；`specs_base` 不加载 base copy fragment → base_records 缺 copy finding →
  kept 集错误；affected 只遍历 base entries → head-only 新条目漏报。
- rule 域：`affected_rules |= base_entries ^ head_entries` 只比较 rule_id 集合 → 同 rule 的
  schema_version/severity/evidence_key_spec 变化判「无规则变化」；policy 变化硬编码 4 条 rule 需核对
  实际消费关系。

## 2. 设计决策
### D1 未加载遗留文件误报边界（H1 前置）

契约 §4.3 禁止 Python 层对 Lua 源码做第二套解析（正则/AST 均点名禁止）→ **不做文本级 load() 图扫描**。
采用**人工核实豁免名单** `i18n/quality/unloaded-sources-v1.json`（schema_version 1；entries =
`{"component","section","evidence"}`，本次两条）：

```json
[
  {"component": "tome", "section": "mod-tome/data/talents/psionic/mental-discipline.lua",
   "evidence": "game/modules/tome/data/talents/psionic/psionic.lua:174 --load(...) 注释掉；focus.lua（psionic.lua:184 加载）携带冲突定义"},
  {"component": "orcs", "section": "tome-orcs/data/talents/celestial/crepescula.lua",
   "evidence": "celestial-empyreal.lua 加载链（sol/cosmic/energies/reflection/void）从不加载 crepescula.lua；orcs 源码树无任何 crepescula 加载引用"}
]
```

- conflicts 透传时：site 全部落在豁免 section → 不产 ERROR，并在 binding/report 元数据列出
  suppressed conflict；部分豁免 → 按剩余（已加载）site 判定，**≥2 才产 ERROR**（同 BC2）；剩余 <2 →
  不产 ERROR（运行时不可能冲突）。
- raw identity conflict **永不删除**：identity.json / identity audit 保留全部 396 个 conflict。
- 名单缺失/损坏 → `ValidationError` fail-closed，不静默放行。
- 未来新冲突的核实流程：加载入口核查（`load()` 引用 / 注释状态）→ 确认未加载 → 名单增补（证据 =
  源码路径:行 + 引用事实）。

### D2 conflicts 持久化通道（H1 实现选型）

`read_index_files` 新增 `conflicts_path: Path | None` 参数：`None` → `conflicts=()`（保持 merge 等
旧调用兼容）；提供时严格从 `identity.json` 恢复完整 `IdentityConflict`（缺失、损坏、schema/字段/
组件不匹配 → `ValidationError` fail-closed）。选型理由：`identity.json` 已是 `ComponentIndex.to_dict()`
的完整落盘（含 conflicts），无需新增 `conflicts.jsonl` 落盘文件；两调用点（pipeline
`extract_enriched` 与 extract `_store_enrichment_artifacts` 的 current-index 重读）语义一致，均传
`current/<id>/identity.json`；`cli._current_indexes_for`（identity show/audit）同样传，使 raw
conflicts 在 read 模型可见。

### D3 rule 域签名比较与 policy 语义

- affected rule 由完整签名 `(rule_id, schema_version, severity, evidence_key_spec)` 的 base/head
  差异驱动（纯 helper `affected_rule_ids`）；同 rule_id 的 schema/severity/evidence bump 改变指纹
  （§6.1）→ 必须重算。
- registry/policy 读取与解析 fail-closed：base 注册表/策略缺失或 JSON 损坏 → `ContractError`/
  `ValidationError` 中止（原实现 `except Exception: set()` 静默回退，已修）。
- ORCHESTRATOR 已核定 `i18n/policy.json` 三个 allowlist 的消费关系：`allowed_format_mismatches` 被
  `_format_issue`（format-mismatch）与 `_format_shape_issue`（format-shape-difference）消费、
  `allowed_empty_targets` 被 empty-target 消费、`allowed_runtime_collisions` 被 runtime-collision
  消费（lint.py 逐条核对）。policy 变化只重算这四条。

### D4 source 部分索引与 duplicate-id 的跨文件正确性

恢复 H1 后，单独提取受影响文件的 `head_partial` 无法发现「新/修改文件的 strong anchor 与未改文件
已有 anchor 重复」。实现选择：**对受影响 component 使用 full-head identity index**（D4 明确允许），
满足「conflict 输入与 full head 等价」：

- `--self-check` 开启时：full head 提取只跑一次，既作 conflict 输入又作绑定/重算索引（参与者与
  conflicts 一致 → incremental == full 字节一致）；
- 未开 `--self-check` 时：每个受影响 component 单独 full head 提取，该 full index **同时用于绑定与
  重算**（V8——partial 绑定会漏掉未改文件提供的 semantic-slot TUs，导致 participants/fingerprint 与
  full head 不一致）；未受影响 component 复用 base index（head == base）；
- 同时保留 staged 部分提取（H2 的删除保护 / 新 TU 收集 / `deleted_files` 报告 / 空 stage 处理），
  并补「不启用 self-check 的跨文件新增 duplicate-anchor」测试（断言新 ERROR 被检出并进入 CI
  new-error 判定，且增量 duplicate record 的 fingerprint/participants 与 full-head 直接组装完全一致）。

### D5 translation 双向比较边界

translation 与 copy fragment 按各自逻辑文件独立加载 base/head 并双向比较（新增、删除、语义变化都进
affected）；head-only 文件全部 head entries 受影响；每个 changed editorial 映射 index candidates，
无映射时加入冻结的 `tu_uid_fallback(editorial_id)`（与 `build_finding_records::_bind` 实际绑定一致）。

## 2.5 复审 FIX 轮（V1–V7，ORCHESTRATOR accepted findings）

| finding | 修复 |
|---|---|
| V1（High）| **baseline entity ownership**：`cli._records_by_component` 保留译文路径映射，并对
  duplicate entity finding（logical_path 为 source section）改用 **TU 身份证据**归属组件
  （subject/participants 所在 component index，绝不字符串匹配 section）；`_baseline_freeze` /
  `_baseline_report` / `lint --baseline` 三调用点传入 `pipeline["indexes"]`；`_baseline_report` 与
  baseline lint JSON 增加 `binding: pipeline["binding"]`（suppressed conflicts 可见）。测试：
  unsuppressed 合成 duplicate 经 `_records_by_component` 归到正确组件并经 `compute_baseline_state`
  成为 new ERROR。 |
| V2（High，fail-open）| 只有**确实不存在的 blob** 才视为删除/缺失。`GitRepository` 新增单一通道
  `read_blob_optional`：0 个 exact tree record → None；>1、git rc、非 blob/非 regular、cat-file 失败
  → ExtractionError；`read_blob` 复用并在 None 时保持原错误语义。source staging 与 translation
  base/head 共用；`_stage_affected_files` 与 translation 文档加载不再吞非 missing 错误（loader 错误
  fail-closed）。测试：非 missing ExtractionError 不被吞、directory 路径非 None、corrupt base 文档
  抛 ValidationError。 |
| V3（High，D2 不一致）| `extract._store_enrichment_artifacts` 的 current-index 扫描改为
  `_read_current_indexes`：完全没有 index artifacts 的目录跳过；一旦 entities/tu 任一存在，要求
  entities + tu_index + identity.json 三者齐全，`read_index_files` 的 ValidationError **向上冒泡**
  （不再 `except ... continue`）。测试：partial trio / corrupt identity 均 fail-closed。 |
| V4（High，Git head 语义）| translation 与 rule 域全部改从 **resolve 后的 base/head commit blobs**
  读取，不再依赖 worktree：translation/copy 每个逻辑文件分别读 base/head（真缺失按空侧比较；loader
  错误 fail-closed；`specs_head`/`specs_base` 由对应 commit blob 构造）；rule registry / policy /
  unloaded-sources registry 从 head blob 构造（required/fail-closed），base 从 base blob；
  `issues_head` 用 head_policy、`issues_base` 用 base_policy；translation 域两侧统一用 head_policy。
  测试：adversarial —— head commit 内容正确但 worktree 被改成损坏/不同内容，结果仍按 head commit。 |
| V5（Medium）| `ComponentIndex.to_dict()` 增加 `"schema_version": 1`，`_read_conflicts` 严格要求 1
  （缺失/非 1 → ValidationError fail-closed）；旧 artifact 需重新 extract。`suppressed_conflicts` 改报
  **实际命中**的豁免 section + 每条 registry `evidence`（`exemptions` 字段），reason 只列命中 section
  （不再列组件全部豁免）。 |
| V6（Medium）| rule 域测试补 §8.4 结果证明：真实 empty-target finding + schema_version bump → 指纹变、
  incremental canonical == full head（self_check PASS）、new error 语义正确；format-mismatch
  evidence_key_spec conversion-pair→constant 实际改变 evidence/指纹并 self_check PASS；policy
  allowlist 增/删实际增/删 finding 并 self_check PASS。 |
| V7（Low）| translation（及 rule）域保持旧 CLI 语义：ci 计数始终报告，但只有 `--ci` 时把 new_errors
  纳入 `report.ok` / raise。补断言（无 --ci 且 new_errors>0 时 ok 仍为 True）。 |
| V8（High，D4 补强）| 未开 `--self-check` 时，受影响 component 的 full-head index 从「仅作 conflict
  输入」改为**同时用于 head 绑定/重算**（partial 绑定会漏掉未改文件提供的 semantic-slot TUs →
  participants/fingerprint 与 full head 不一致；删除/rename 后的 head issue 绑定同理）。recompute/kept
  升级为 record 身份级：participants 含 affected TU 即 touched；conflict-driven 记录按稳定
  evidence_key 匹配（其 Issue 每侧绑定都重新生成，entry_id 不可靠）。测试：无 self-check 的跨文件
  duplicate（changed 与 unchanged 定义暴露不同 slot 集）断言增量 record 的 fingerprint/participants
  与 full-head 直接组装完全一致（不只断言检出）。 |
| V9（Medium）| `_read_conflicts` 按当前 artifact 的封闭模型逐字段 fail-closed：code 仅
  duplicate-talent-id / duplicate-effect-id / identity_conflict；duplicate talent/effect 对应 kind 且
  severity=error；identity_conflict severity=context；sites ≥2 且唯一。不改公式。测试覆盖每类代表性
  损坏（typo code、kind/severity 错配、单 site、重复 site）。 |
| V10（Medium）| `cli._current_indexes_for` 复用 `extract._read_current_indexes`（返回 list 转
  dict），identity show/audit 的读取路径与 D2/V3 一致：partial trio / corrupt identity 同样
  ValidationError。测试覆盖 `_current_indexes_for`。 |

## 2.6 初审 review R1–R7（自动修复 cycle 2）

| finding | 修复 |
|---|---|
| R1（High）| **rename 双路径**：`GitRepository.changed_paths()` 改用
  `git diff --no-renames --name-only -z`，检测到的 rename 同时返回 preimage 与 postimage，旧 section
  的 base TU 进入 affected（否则其 finding 残留）。测试：真实 old.lua→new.lua + anchor/UID 改变、无
  self-check 的生产链，断言 affected sections 含两侧、旧 strong TU 无 record、增量 canonical ==
  full-head 直接组装（`_expected_full_records` + `_records_from_dicts`）。I2 保持（仍只经 GitRepository）。 |
| R2（High）| **translation participant-aware**：recomputed/kept 从只看 `record.tu_uid` 改为
  subject 或任一 participant ∈ affected_tus 即 touched（runtime-collision 的 subject 是 collision-id
  fallback，真实 editorial TUs 在 participants）。测试：无 self-check 的 collision add（new ERROR
  出现）与 delete（resolved 消失），`report["records"]` 与 full-head 组装 canonical 直接对比。 |
| R3（High）| **rule severity 权威**：`build_finding_records` 对每个 registered issue/conflict 用
  `dataclasses.replace(issue, severity=rule.severity)` 构造记录（message/path/line/entry_id 不变），
  `Issue` 类、`to_dict`、default lint 输出零改动；registry 的
  format-shape-difference=error 对 enriched 路径生效（§9.2 契约表）。测试：error→warning 端到端（head
  record 是 warning、self-check PASS、CI 不误计 new ERROR）+ 单元测试（registry severity 权威、输入
  lint Issue 保持 warning）。 |
| R4（High）| **unloaded-sources 是 rule 域依赖**：检测 `i18n/quality/unloaded-sources-v1.json`
  changed → affected 含 duplicate-talent-id / duplicate-effect-id；base/head 各从对应 commit blob
  严格加载 UnloadedSources（missing/corrupt fail-closed）；`records_for` 显式接收 unloaded（base records
  用 base、head 用 head）；no-change early return 纳入该依赖。测试：exemption remove（head 新增 2 个
  duplicate ERROR / new error）与 exemption add（resolved），用真实 fixture index（含 T_FLAME /
  EFF_BURNING 冲突），self-check PASS。 |
| R5（High）| **重复 editorial 的 multiset**：`_changed_editorial_keys` 改为每
  (section,source,source_tag) 一个 semantic payload Counter，base/head multiset 不同即 affected（dict
  折叠最后一条会漏掉重复的 defective occurrence）。测试：同 key 增/删 defective occurrence（无
  self-check），canonical 与 full-head 对比；与 R2 组合（runtime-collision 参与者含受影响 TU）。 |
| R6（Medium）| **partial exemption 参与者**：duplicate 记录参与者只纳入
  `tu.anchor_key==anchor` 且 `tu.sections` 与过滤后（已加载）site sections 有交集的 TU；无参与者才
  fallback。测试：两个 loaded site 定义 name + 一个 exempted 第三 site 额外有 info slot，surviving
  ERROR 不含 unloaded-only info TU，subject/fingerprint 与 loaded-only 组装一致。 |
| R7（Medium）| **identity-only artifact 不静默跳**：`extract._read_current_indexes` skip 条件改为
  三件套都不存在才 skip；identity.json-only 目录进入读取并因 entities/tu 缺失 ValidationError；
  `cli._current_indexes_for` 复用路径同样断言。 |

## 2.7 复审 cycle 3（R2/R8/R9，用户授权的最后修复轮）

| finding | 修复 |
|---|---|
| R2（High，participant 补强）| translation 域对 runtime-collision records 建立**跨 base/head 的稳定
  family key** `(rule_id, issue.entry_id)`（collision_id = component/source/source_tag 的哈希，两侧
  同 family）；任一侧 record direct touched（subject 或任一 participant ∈ affected_tus）→ 该 family 的
  base record 移出 kept、head record 重算（反例：base A+B 已冲突、head 加 C 且只有 C affected，旧 A+B
  与新 A+B+C 不得共存）。不按本侧 participant intersection 误关联。测试（无 self-check）：2→3
  （previous=1/kept=0/recomputed=1/incremental=1，canonical == full-head 组装、无 stale base
  fingerprint）与 3→2 对称（base A+B+C 经 C participant direct touched，head A+B 经 family 重算不消失）。 |
| R8（High，occurrence evidence）| `build_finding_records` 对需具体 entry 建 evidence 的分支（
  conversion-pair / formatter-tag）按 Issue 的 occurrence location 精确选择：`entry.logical_path ==
  issue.logical_path` 且 `entry.line == issue.line`，必须唯一；0 或 >1 → ambiguous/unbindable，计入
  skipped 并 continue（fail-closed，不伪造 evidence）。runtime-key / constant 分支不受影响；`Issue`
  类/to_dict/default lint 零改动。`_changed_editorial_keys` 的 multiset 计入 occurrence line
  （(semantic, line) 对），纯重排也重算 head 侧，避免 kept 携带 stale 行元数据破坏
  canonical == full。测试：unit（同 editorial id 一 valid 一 defective，顺序互换/行号改变 → evidence
  恒为 defective conversion pair、fingerprint 稳定；指向 valid occurrence → conv:d|d；ambiguous →
  skipped）+ 端到端 translation（重排与前置插入 valid duplicate：无 false new/resolved，canonical ==
  full head，无 self-check）。 |
| R9（Medium，空 exemption registry）| `UnloadedSources.from_dict` 允许 `entries=[]`（返回
  entries=()，合法的「当前无任何豁免」状态）；missing / non-array / 坏 schema / 坏 entry 仍 fail-closed。
  测试：empty 成功、missing key 失败、non-array 失败；R4 exemption removal 测试改为真实 2 条 →
  `entries=[]` 过渡（rule incremental 暴露 duplicate ERROR、canonical self-check PASS、new ERROR
  计数正确）。 |

## 2.8 closure cycle 4（FR1–FR3，ORCHESTRATOR 裁决后最小修复）

| finding | 修复 |
|---|---|
| FR1（Medium）| **identity binding 不依赖文档存在**：translation 域 `records_for` 构造 bound 后经
  `_bind_identity_contexts` 为 `indexes` 中每个选中 component 确保 component-key 的
  identity-only `FindingContext(component, entries=(), index)`（已有 main context 保留 entries 并绑
  index；copy-only 时也补 component-key）。entity conflict 的 `contexts.get(component)` 稳定命中，
  base 无主文档 / head 新增时两侧都强绑定（不再 base fallback + head strong 并存、误报 new）。
  `_bind` 仍遍历 main/copy contexts，translation entries 不丢不重；source/rule/baseline 路径零改动。
  测试：base 无 main、head 新 main，index 含 unsuppressed T_DUP duplicate（两个 strong
  participant）：无 self-check，previous=1 / 最终单条 legacy duplicate（new_errors=0 /
  legacy_errors=1）/ canonical == full-head；另 defective head-only empty-target 仍为 new。 |
| FR2（Medium）| **source --ci JSON ok 与 gate 一致**：`_lint_identity_mode` 在任何 render 前从
  `result.ci.new_errors` 取值，`--ci` 且 >0 时 `report["ok"] = False`（与 self-check 结果 AND）；无
  `--ci` 保持 V7（计数不置 ok=False）；legacy-only + `--ci` ok=True；异常类型/exit/首 fingerprint
  消息不变。测试：production CLI JSON 捕获——new error + `--ci` JSON ok=False 且 raise；legacy-only
  ok=True 不 raise；无 `--ci` new error ok=True。 |
| FR3（Medium）| **participants 遵循 conflict 身份作用域**：duplicate participant comprehension 增加
  `tu.kind == conflict.kind` 与 `tu.identity_binding == "strong"`（anchor_key 与 loaded-section
  相交条件保留；`anchor_type is not None` 保留但不替代 strong；kind 来自已封闭校验的
  identity.json conflict.kind，不用 code 前缀猜）。测试：synthetic index——T_DUP 两 strong talent TU
  + 同 anchor_key 另一 kind strong TU + fallback TU + unloaded-only TU，participants 只含两 talent
  strong TU，subject/fingerprint 与无噪音 index 一致。 |

## 3. 实现要点

- `tools/i18nlib/identity.py`：`UNLOADED_SOURCES_RELATIVE_PATH`、`UnloadedSourceEntry` /
  `UnloadedSources`（fail-closed 加载 + `sections_for(component)` + `from_dict`）、`_read_conflicts(path,
  component)`（严格要求 identity.json `schema_version: 1` + **封闭模型逐字段校验**：code/severity/kind
  组合绑定、sites ≥2 且唯一）、`read_index_files(..., conflicts_path=None)`；`ComponentIndex.to_dict()`
  携带 `schema_version: 1`。
- `tools/i18nlib/findings.py`：`_filter_duplicate_conflicts`（纯函数）+ `build_finding_records(
  ..., unloaded_sources=None)`；binding report 新增 `suppressed_conflicts`（含实际命中豁免的
  section + registry evidence）。
- `tools/i18nlib/pipeline.py`：`extract_enriched` 传 conflicts_path；`run_enriched_lint` 加载
  unloaded-sources 并传入。
- `tools/i18nlib/extract.py`：`_read_current_indexes`（current-index 扫描 fail-closed：缺任一 index
  artifact 即抛 ValidationError）替代 sibling 循环的静默 continue。
- `tools/i18nlib/git_source.py`：`read_blob_optional`（仅确实缺失的 blob 返回 None；git 失败 /
  ambiguous / 非 regular / cat-file 失败抛 ExtractionError）；`read_blob` 复用并在 None 时保持原错误语义。
- `tools/i18nlib/incremental.py`：`_stage_affected_files` 用 `read_blob_optional`（只有缺失才算删除）
  并返回 (staged_count, deleted)；`_empty_index`；`incremental_source_flow` affected = base∪head、
  record 身份级 recompute/kept（issue entry_id + participants + evidence_key，V8）、D4 conflict 输入
  与 head 绑定/重算均用受影响 component 的 full-head index、`deleted_files` / `ci`（new/legacy/new
  fingerprints）/ binding suppressed 报告。
- `tools/i18nlib/cli.py`：`_current_indexes_for` 复用 `extract._read_current_indexes`（V10 fail-closed）；
  `_records_by_component` 增加
  TU 身份证据归属（entity finding）+ 三调用点传 indexes；`_baseline_report` / baseline lint JSON 增加
  `binding`；source `--ci` 用 flow 报告的 `ci.new_errors`（消息含数量 + 首 fingerprint）；
  `_lint_incremental_rule` 完整签名比较 + base/head blob fail-closed 读取 + head_policy/base_policy 分侧；
  `_lint_incremental_translation` 从 base/head commit blobs 加载逻辑文档（V4）+ 双向比较 + fallback TU；
  纯 helper `_changed_editorial_keys` / `_rule_signature` / `affected_rule_ids` /
  `_load_document_at` / `_document_specs_at_commit` / `_read_commit_json`。

## 4. 测试

新增/强化（全部 `python3 -B -m unittest discover -s tests/i18n` 通过）：

- `tests/i18n/identity/test_conflicts.py`：read_index_files conflicts 恢复 round-trip、None 兼容、
  组件/schema/缺失/损坏 fail-closed；UnloadedSources 加载校验（缺失/损坏/schema/重复）；duplicate
  ERROR 豁免矩阵（全豁免 suppressed、部分豁免 ≥2 产 ERROR、剩余 <2 suppressed、弱锚 CONTEXT 不受
  影响、指纹公式不变）。
- `tests/i18n/incremental/test_incremental.py`：生产链 add 新文件新 TU（self-check PASS）、delete
  文件（不崩溃 + `deleted_files` 报告 + kept 移除 + self-check PASS）、同文件实体 rename 新 UID
  （self-check PASS）、**不启用 self-check 的跨文件 duplicate-anchor**（新 ERROR 检出并进入 CI
  new-error）、H3 legacy ERROR 不误失败（new_errors=0 / legacy_errors>0）。
- `tests/i18n/incremental/test_domains.py`：translation 域 head-only main / head-only copy / base
  copy kept / head-only 条目与删除 / 语义变化 / fallback TU 成员断言；rule 域 schema/severity/
  evidence_key_spec bump、rule 增删、policy 四规则影响面、无变化早退、base 损坏 fail-closed；H3 CLI
  gate（legacy PASS、新 ERROR FAIL 消息含数量+首 fingerprint、修复后 PASS）。
- V1–V7 回归（同文件）：`BaselineEntityOwnershipTests`（`_records_by_component` TU 归属 + baseline
  new ERROR）、`GitReadBlobOptionalTests` / `StagingFailClosedTests`（V2 只把缺失 blob 当 None/
  删除）、`CurrentIndexScanTests`（V3 三件套 fail-closed）、`HeadCommitSemanticsTests`（V4 worktree
  对抗 + corrupt base 文档 fail-closed）、rule 域 V6（schema bump / evidence spec / policy allowlist
  增删 finding，均 self_check PASS + new-error 语义）、V7（无 --ci 时 new_errors 不置 ok=False）。
  `test_conflicts.py` 增 schema_version 严格要求与 suppressed `exemptions`（section+evidence）断言。

## 5. 真实数据验证（ORCHESTRATOR 复核）

- `python3 -B tools/i18n extract --enrich --all`：8 组件提取成功（engine 904 / boot 319 / tome
  25543 / example 47 / example-realtime 46 / ashes-urhrok 999 / cults 2444 / orcs 4493 tDef）。
- `read_index_files(conflicts_path=identity.json)` 恢复 **396 个 conflict**（与接管计数一致），
  含 2 个 ERROR（T_IRON_WILL / T_TWILIT_ECHOES），weak CONTEXT 全保留。
- `pipeline.run_enriched_lint`（CLI 同款 DLC env 注入）：**0 条 duplicate-id Finding**、
  suppressed_conflicts 恰为 2 条（含 evidence）、总 ERROR records = 0。
- `python3 -B tools/i18n lint --baseline 1cff3d6f...`：8 组件 gate 全 PASS（new_err=0 / legacy_err=0
  / resolved=0），与既有冻结基线（全部 0 finding）一致。
- **baseline 影响**：豁免后 0 finding 与既有 baseline 一致 → **无需重冻**，`i18n/baselines/` 字节
  不变（真实验证后确认）。

## 6. PR 待办

- 本修订全部内容（本迁移记录 + 契约 §4.4/§8/§9/§15 修订 + 实现 + 测试）未推送/合并；PR 由用户另行
  指示，PR 合并后 `contract/0.1` 正式生效。
- **并发提交排除**：外部宿主在本任务运行期间提交了 `88b25cf`（Paseo role routing and lineage）与
  `521771e`（require max thinking for DeepSeek executor）两个不重叠的 orchestration/Skill 文档提交；
  ORCHESTRATOR 已核验其与任务内容无交集并排除，本任务 diff 不含这两个提交内的文件。
- 冻结公式（§4.5/§6.1/§7.1）与既有 baseline 文件字节不变（`git diff` 核验）。
- `ComponentIndex.to_dict()` 新增 `schema_version` 后，既有 identity artifact 需重新
  `extract --enrich`（已执行，见 §5 真实数据）。**升级注意**：首次运行前需清除可重建缓存
  `.artifacts/i18n/identity/current/`（旧 schema 的 identity.json 按 fail-closed 拒绝，
  这正是 H1 缺口的防护语义；sqlite 随 `_store_enrichment_artifacts` 自动重建）。
