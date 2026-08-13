# 迁移记录 — infra-contract-003（effect.desc 槽位实现 + baseline 重冻）

> 依据：`docs/localization-infra-contract-v0.1.md` 第十五节规则 3（涉及冻结条款外围的
> registry/baseline 元数据变更必须随附迁移方案）。本记录对应修订
> `contract/0.1`（infra-contract-002 验收后、PR 合并前的未推送修订）。

## 1. 变更摘要

- **槽位实现**：`i18n/quality/slot-registry-v1.json` 23→24 项，新增
  `{"ast_path": "newEffect.desc", "semantic_slot": "effect.desc"}`（契约 §4.6 示例
  槽位，与 infra-contract-002（talent.info）机制完全同构）。
- **捕获机制**：官方提取器（pinned `bdc19d22862f7a6cfbe71d7136145720ecea7bf7`）newEffect
  分支对**顶层 `desc` 字段**的字面量形态做**原位重分类**：直接 `_t"…"` 字段值
  （`Call(Id(_t), ExpList(String))`）、function 单 Return（`return ([[…]]):tformat(args)`
  / `return _t"…"`，同 talent.info 三分支）、以及 `newEffect(table.merge(<expr>,
  {name, desc}))` 的**受限支持**（仅当 merge 实参末位为 Table 且 name/desc 均为静态
  字面量时按构造器同等处理）。通用 `_t`/`tformat` 分支对已注册 AST 节点改发
  `ast_path="newEffect.desc"` 记录（entity_kind="effect"，anchor 取自 name 字段，
  确定性锚 `EFF_`+name:upper()），locales 写入与 source_tag（"_t"/"tformat"）逐字节
  不变。替换仍「每处恰好一次」fail-closed。
- **字段边界（p2）**：仅 newEffect 构造器（或 merge 覆写表）**顶层** Field 键严格
  `== "desc"` 的值节点登记；`display_desc`/`long_desc` 字段值、long_desc 函数体内局部
  `desc` 字面量保持 free；`floorEffect.desc`（不同实体）不标 newEffect.desc。
- **不变式（已实测）**：tDef 数、source_snapshot_sha256、i18n_list.lua/snapshot.jsonl
  字节全部不变；sidecar 总记录数逐组件与变更前一致（纯原位重分类，零增删）；每
  occurrence 恰一条 enrichment 记录（无同 editorial ID strong+fallback 双映射）。

## 2. Registry sha 变更

| 项 | 值 |
| --- | --- |
| 旧 slot_registry_sha256（23 项） | `8602a99092c953ad6769e14d6d534b84176712a170197752040c281a12d3fb4e` |
| 新 slot_registry_sha256（24 项） | `75c59d774d23402f6b910c0e4e843329cea513ef1008f02e3721326acbde6645` |
| 变更性质 | 数据行增补（§4.6 注册表数据变更，非冻结公式/quality 内容变更，见契约 §12 澄清） |

## 3. 基线重冻（规则 3 迁移执行）

- 旧基线 `i18n/baselines/*-29da216754dce5a8edceb49c6ae7692190d48583.{jsonl,meta.json}`
  与 `i18n/baselines/*-cd42f9aedd365b398e69b472326d953055f7f9fe.{jsonl,meta.json}`
  （各 8 组件 × 2 文件）**全部 0 条 finding** → 旧指纹/TU UID 重登记集合为**空**
  （无 finding 数据迁移负担；重冻 = 换 registry sha + 空基线）。
- 新基线 commit：`1cff3d6f3b3a061624e5f74bd80c4d7e8186fd25`（实现提交），16 个新文件：
  `i18n/baselines/{ashes-urhrok,boot,cults,engine,example,example-realtime,orcs,tome}-1cff3d6f3b3a061624e5f74bd80c4d7e8186fd25.{jsonl,meta.json}`。
- 每份 meta：`translation_commit` == 1cff3d6…、`slot_registry_sha256` ==
  `75c59d774d23402f6b910c0e4e843329cea513ef1008f02e3721326acbde6645`、jsonl 0 条 finding；
  `baseline report --commit 1cff3d6…` ok=True、components=8、8/8 passed、totals 全 0。
- 旧 `*-29da216*` 与 `*-cd42f9a*` 共 32 文件字节不变（freeze 前后 sha256 一致，与
  提交内容比对 32/32 unchanged）。

## 4. 覆盖矩阵（真实数据，AST 全量实证，8 组件 0 解析失败）

| 状态 | 形态 | 数量 | 处置 |
| --- | --- | --- | --- |
| strong-deterministic | `desc = _t"…"`（直接字段值） | 803（tome 586 / boot 2 / ashes 38 / cults 69 / orcs 108） | 重分类 newEffect.desc |
| strong-deterministic（受限支持） | `newEffect(table.merge(…, {name, desc}))` | 2（tome：RIME_WRAITH / RIME_WRAITH_GELID_HOST） | 同上，锚取 merge 覆写表 name |
| captured-nondeterministic-fallback | 动态工厂/变量表：`e.desc = ("…"):tformat(name); newEffect(e)` 等 | 5（tome：Energy Alteration、floor.lua `newEffect(t)`；ashes/cults/orcs 各 1） | 不重分类，模板经通用 tformat 分支保持 free fallback |
| not-captured | `desc = "…"` 纯字符串（example / example_realtime ACIDBURN） | 2 | 不捕获（新增会破坏快照/严格 join） |
| floorEffect 边界 | tome 11 条纯字符串 + orcs 4 条 `desc=_t"…"` | 15 | floorEffect 分支隔离；`_t` 形态经通用分支保持 free，均不标 newEffect.desc |

### 三口径度量（实跑数字，2026-08-13，run 20260813T095107）

| 组件 | 口径 1：AST 候选 occurrence | 口径 2：sidecar 记录 | 口径 3：coalesced strong TU | 共享 desc 一对多组 |
| --- | --- | --- | --- | --- |
| tome | 588 | 588 | 588 | 12 |
| boot | 2 | 2 | 2 | 0 |
| ashes-urhrok | 38 | 38 | 38 | 2 |
| cults | 69 | 69 | 69 | 5 |
| orcs | 108 | 108 | 108 | 2 |
| **合计** | **805** | **805** | **805** | **21** |

- **口径 1（AST 候选）**：与提取器同遍历逻辑的 luafish 调查计数；tome 588 = 586 直接
  `_t` + 2 merge 覆写表。
- **口径 2（实际 enrichment sidecar 记录数，逐 occurrence 一条）**：与候选一致；每
  occurrence 恰一条记录（(section,line,source) 键无重复），同 occurrence 不同时
  strong+fallback（elseif 互斥）。
- **口径 3（TU 索引层 coalesce 去重后的 strong TU 数）**：与记录数一致——无同实体同槽
  coalesce 事件（desc 单 TU 槽，每 occurrence 独立成 TU）。
- **一对多 shared desc（p1）**：同一 editorial ID 映射到多个 strong TU，共 21 组
  （tome 12 / ashes 2 / cults 5 / orcs 2），例如：
  - tome `GREATER_INVISIBILITY`/`INVISIBILITY` 同 `desc = _t"Invisibility"`
    （magical.lua:258/288）；
  - tome `BLINDED`/`FORGONE_VISION` 同 `Blinded`、`STEAMROLLER`/`STEAMROLLER_USER` 同
    `Steamroller`、`MIRROR_IMAGE_REAL`/`MIRROR_IMAGE_FAKE` 同
    `Protected by a Mirror Image`、`SHIVGOROTH_FORM`/`SHIVGOROTH_FORM_LORD`、
    `DET_TETHER`/`BEN_TETHER`、`TEMPORAL_DESTABILIZATION`/`…_START` 等；
  - ashes `BLACKICE`/`BLACKICE_DET`、`DEMON_SEED_BLOOD_DRINKER_BUFF`/`_DEBUFF`；
  - cults `SUSPEND_BEN`/`SUSPEND_DET`、`FATEBREAKER`/`FATEBREAKER_TEMP`、
    `GASTRIC_WAVE_BUFF`/`_DEBUFF`、`CULTS_BOOK_TIMEOUT`/`CULTS_BOOK_HOME_TIMEOUT`、
    `GLIMPSE_OF_TRUE_HORROR`/`…_SELF`；
  - orcs `FORCED_GESTALT`/`FORCED_GESTALT_FOE`、`LOCK_ON_BEN`/`LOCK_ON_DET`。

## 5. 受影响 TU 重建策略

- 旧基线 0 条 finding → **重登记集合为空**：无需任何 finding 指纹迁移。
- TU UID 影响：本次变更使 desc 字面量 occurrence 的 `ast_path` 从 `_t`/`tformat` 原位
  改为 `newEffect.desc` → 该类 occurrence 从 fallback-editorial TU 转为 strong TU
  （effect 锚 + `effect.desc` 槽）。TU UID 公式（§4.5 冻结）未动；旧 fallback TU UID
  不再产生（其 editorial ID 仍保留在 editorial_to_tu 映射，指向新 strong TU，共享
  desc 时一个 editorial ID 指向多个 strong TU）。
- identity.sqlite 为 current-state cache（§10.1），删除重建即得新状态，无需数据迁移。

## 6. 回滚边界（三档）

回滚涉及两个版本化提交：**实现提交 `1cff3d6f3b3a061624e5f74bd80c4d7e8186fd25`**
（registry 行 + extract.py 三分支替换 + 覆盖矩阵/字段边界测试）与**交付提交**
（迁移记录 + 契约文档 §15 修订 + 16 个新基线文件，由 ORCHESTRATOR 执行）。

1. **完整版本化回滚（逆序）**：
   - `git revert <交付提交>` —— 撤销迁移记录、契约文档 §15 修订与 16 个新基线文件；
   - `git revert 1cff3d6` —— 撤销实现（registry 行、extract.py 分支、测试）；
     registry sha 回到 `8602a990…` 后旧基线 `*-cd42f9a*`/`*-29da216*` 重新有效。
2. **仅基线数据层回滚**：删除 16 个新基线文件
   （`rm i18n/baselines/*-1cff3d6f3b3a061624e5f74bd80c4d7e8186fd25.{jsonl,meta.json}`）
   即可回到冻结前状态，旧基线文件未动；注意此操作**不撤销**迁移记录、契约文档修订
   与实现（新基线删除后，`baseline report`/CI 将按旧基线判定，直至重新 freeze）。
3. **依赖**：实现提交与基线重冻为两阶段提交——基线绑定受审实现，重冻不可先于实现
   提交（freeze 的 translation_commit 必须是已存在的实现提交 1cff3d6）。

迁移记录（含本文件）属于交付提交内容，随档 1 逆序回滚一并撤销；档 2 不回滚文档/代码。

## 7. PR 待办

- 本修订（契约文档 §15、本迁移记录、16 个新基线文件、实现提交 1cff3d6 内容）
  未推送/合并；PR 由用户另行指示，PR 合并后 `contract/0.1` 正式生效。
- 后续任务：`floorEffect.desc` 槽位（不同实体，另行任务，机制同 newEffect.desc
  原位重分类，需先固定 floorEffect 的实体身份语义）。
