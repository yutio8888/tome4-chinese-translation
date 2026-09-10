# 迁移记录 — infra-contract-002（G10 talent.info 槽位实现 + baseline 重冻）

> 依据：`docs/localization-infra-contract-v0.1.md` 第十五节规则 3（涉及冻结条款外围的
> registry/baseline 元数据变更必须随附迁移方案）。本记录对应修订
> `contract/0.1`（Pilot A 验收后、PR 合并前的未推送修订）。

## 1. 变更摘要

- **槽位实现**：`i18n/quality/slot-registry-v1.json` 22→23 项，新增
  `{"ast_path": "newTalent.info", "semantic_slot": "talent.info"}`。
- **捕获机制**：官方提取器（pinned `bdc19d22862f7a6cfbe71d7136145720ecea7bf7`）newTalent
  分支对 info 字段的**单字面量模板**（`return ([[…]]):tformat(args)` / `return _t"…"` /
  `info = _t"…"` 三种确定性形态）做**原位重分类**：`_t`/`tformat` 通用分支对同一 AST 节点
  改发 `ast_path="newTalent.info"` 记录（entity_kind="talent"，anchor 取自 name/short_name/
  type），locales 写入与 source_tag（"tformat"/"_t"）逐字节不变。替换仍「每处恰好一次」
  fail-closed。
- **不变式（已实测）**：tDef 数、source_snapshot_sha256、i18n_list.lua/snapshot.jsonl
  字节全部不变；每 occurrence 恰一条 enrichment 记录（无同 editorial ID strong+fallback
  双映射）；enrichment↔snapshot 严格 join 通过。

## 2. Registry sha 变更

| 项 | 值 |
| --- | --- |
| 旧 slot_registry_sha256（22 项） | `219e7fdfe1a834245470fb640e03ae1c0810dd4efb85465e69b1c66346066895` |
| 新 slot_registry_sha256（23 项） | `8602a99092c953ad6769e14d6d534b84176712a170197752040c281a12d3fb4e` |
| 变更性质 | 数据行增补（§4.6 注册表数据变更，非冻结公式/quality 内容变更，见契约 §12 澄清） |

## 3. 基线重冻（规则 3 迁移执行）

- 旧基线 `i18n/baselines/*-29da216754dce5a8edceb49c6ae7692190d48583.{jsonl,meta.json}`
  （8 组件 × 2 文件）**全部 0 条 finding** → 旧指纹/TU UID 重登记集合为**空**（无 finding
  数据迁移负担；重冻 = 换 registry sha + 空基线）。
- 新基线 commit：`cd42f9aedd365b398e69b472326d953055f7f9fe`（实现提交），16 个新文件：
  `i18n/baselines/{ashes-urhrok,boot,cults,engine,example,example-realtime,orcs,tome}-cd42f9aedd365b398e69b472326d953055f7f9fe.{jsonl,meta.json}`。
- 每份 meta：`translation_commit` == cd42f9a…、`slot_registry_sha256` ==
  `8602a99092c953ad6769e14d6d534b84176712a170197752040c281a12d3fb4e`、jsonl 0 条 finding；
  `baseline report --commit cd42f9a…` ok=True、components=8、totals 全 0。
- 旧 `*-29da216*` 16 文件字节不变（freeze 前后 sha256 一致）。

## 4. 覆盖矩阵（真实数据，AST 全量实证，4 组件 0 解析失败）

| 状态 | 形态 | 数量 | 处置 |
| --- | --- | --- | --- |
| strong-deterministic | `return ([[…]]):tformat(args)` | 1702 | 重分类 talent.info |
| strong-deterministic | `return ([[…]]):tformat()` | 108 | 同上 |
| strong-deterministic | `return _t"…"`（含 Paren 包裹） | 18 | 同上 |
| strong-deterministic | `info = _t"…"`（直接字段） | 8 | 同上 |
| **strong 合计** | | **1836**（tome 1373 / ashes 88 / cults 109 / orcs 266） | AST 候选数；实际记录与 coalesce 后 TU 数见下「三口径度量」 |
| captured-nondeterministic-fallback | `local base = _t[[…]]` / 运行时拼接或条件返回（字面量已被通用分支捕获） | 5（tome：chant/dirge/hymn Acolyte、Beyond the Flesh、Clarity） | 不重分类，保持 free fallback |
| not-captured | `info = "…"` 纯字符串 / `return ""` 等无字面量形态 | 15（tome 11 纯字符串 + 4 无字面量；orcs 2） | 不捕获（新增会破坏快照/严格 join） |
| 动态调用 | `newTalent(t)` 变量表 | 14（tome 7 / orcs 7） | 无 AST info 可捕获 |

排除规则：info 函数体（不含嵌套闭包）内 Return 节点总数 ≠ 1 → 不注册（tome 5 例真实
条件返回；仅含嵌套闭包 Return 的 3 例正确纳入 strong）。

### 三口径度量（实跑数字，2026-08-13）

| 组件 | 口径 1：AST 候选 occurrence | 口径 2：实际 sidecar 记录 | 口径 3：coalesced strong TU |
| --- | --- | --- | --- |
| tome | 1373 | 1369 | 1367 |
| ashes-urhrok | 88 | 88 | 88 |
| cults | 109 | 109 | 109 |
| orcs | 266 | 266 | 265 |
| **合计** | **1836** | **1832** | **1829** |

- **口径 1（AST 调查 occurrence 总数，strong-deterministic 候选）**：按形态匹配计数
  （last-direct-return 规则，未做多 return 排除），tome 1373 = tformat 1366 + `_t` 7。
- **口径 2（实际 enrichment sidecar 记录数，逐 occurrence 一条）**：tome 1369 =
  候选 1373 − 5（多 return 结构排除）+ 1（重复 info 字段死模板：feedback.lua
  Amplification 同一 talent 表两个 info 字段，候选调查按 talent 合并计 1 而提取器按字段
  注册 2 条）；ashes/cults/orcs 与候选一致。
- **口径 3（TU 索引层 coalesce 去重后的 strong TU 数）**：tome 1369 → 1367，orcs
  266 → 265，共 3 个 coalesce 事件（同实体 UID + 同槽 talent.info → 同 TU UID）：
  - tome `T_AMPLIFICATION`（feedback.lua 重复 info 字段死模板，2 记录 → 1 TU、2 revisions）；
  - tome `T_IRON_WILL`（psionic/focus.lua 与 mental-discipline.lua 两个同名 talent 定义，
    2 记录 → 1 TU、2 revisions）；
  - orcs `T_TWILIT_ECHOES`（celestial/crepescula.lua 与 celestial/void.lua 两个同名
    talent 定义，2 条同文本记录 → 1 TU、revision 去重为 1）。

## 5. 受影响 TU 重建策略

- 旧基线 0 条 finding → **重登记集合为空**：无需任何 finding 指纹迁移。
- TU UID 影响：本次变更仅使 info 模板 occurrence 的 `ast_path` 从 `_t`/`tformat` 原位改
  为 `newTalent.info` → 该类 occurrence 从 fallback-editorial TU 转为 strong TU（实体
  anchor + `talent.info` 槽）。TU UID 公式（§4.5 冻结）未动；旧 fallback TU UID 不再产生
  （其 editorial ID 仍保留在 editorial_to_tu 映射，指向新 strong TU）。
- identity.sqlite 为 current-state cache（§10.1），删除重建即得新状态，无需数据迁移。

## 6. 回滚边界（三档）

回滚涉及两个版本化提交：**实现提交 `cd42f9aedd365b398e69b472326d953055f7f9fe`**（registry 行 +
extract.py 三分支替换 + G10/矩阵测试 + 契约 0.1 状态，含 infra-contract-001 基础设施）与
**交付提交 `dc74ee2ce5e86c736a84b669c92894c0296ee153`**（迁移记录 + 契约文档 §12/§13/§15
修订 + 16 个新基线文件）。

1. **完整版本化回滚（逆序）**：
   - `git revert dc74ee2` —— 撤销迁移记录、契约文档 §12/§13/§15 修订与 16 个新基线文件；
   - `git revert cd42f9a` —— 撤销实现（registry 行、extract.py 三分支、G10/矩阵测试、
     契约 0.1 状态）；registry sha 回到 `219e7fdf…` 后旧基线 `*-29da216*` 重新有效。
2. **仅基线数据层回滚**：删除 16 个新基线文件
   （`rm i18n/baselines/*-cd42f9aedd365b398e69b472326d953055f7f9fe.{jsonl,meta.json}`）即可
   回到冻结前状态，旧 29da216 文件未动；注意此操作**不撤销**迁移记录、契约文档修订与
   实现（新基线删除后，`baseline report`/CI 将按旧 29da216 基线判定，直至重新 freeze）。
3. **依赖**：实现提交与基线重冻为两阶段提交——基线绑定受审实现，重冻不可先于实现提交
   （freeze 的 translation_commit 必须是已存在的实现提交）。

迁移记录（含本文件）属于交付提交内容，随档 1 逆序回滚一并撤销；档 2 不回滚文档/代码。

## 7. PR 待办

- 本修订（契约文档 §12/§13/§15、本迁移记录、16 个新基线文件、实现提交 cd42f9a 内容）
  未推送/合并；PR 由用户另行指示，PR 合并后 `contract/0.1` 正式生效。
- 后续任务：`newEffect.desc` 槽位实现（另行任务，机制同 talent.info 原位重分类）。
