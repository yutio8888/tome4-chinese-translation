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
| **strong 合计** | | **1836**（tome 1373 / ashes 88 / cults 109 / orcs 266） | 实际产出 1832 条记录（tome 1369 含 1 条重复 info 字段死模板，同实体同槽 coalesce 为同一 TU） |
| captured-nondeterministic-fallback | `local base = _t[[…]]` / 运行时拼接或条件返回（字面量已被通用分支捕获） | 5（tome：chant/dirge/hymn Acolyte、Beyond the Flesh、Clarity） | 不重分类，保持 free fallback |
| not-captured | `info = "…"` 纯字符串 / `return ""` 等无字面量形态 | 15（tome 11 纯字符串 + 4 无字面量；orcs 2） | 不捕获（新增会破坏快照/严格 join） |
| 动态调用 | `newTalent(t)` 变量表 | 14（tome 7 / orcs 7） | 无 AST info 可捕获 |

排除规则：info 函数体（不含嵌套闭包）内 Return 节点总数 ≠ 1 → 不注册（tome 5 例真实
条件返回；仅含嵌套闭包 Return 的 3 例正确纳入 strong）。

## 5. 受影响 TU 重建策略

- 旧基线 0 条 finding → **重登记集合为空**：无需任何 finding 指纹迁移。
- TU UID 影响：本次变更仅使 info 模板 occurrence 的 `ast_path` 从 `_t`/`tformat` 原位改
  为 `newTalent.info` → 该类 occurrence 从 fallback-editorial TU 转为 strong TU（实体
  anchor + `talent.info` 槽）。TU UID 公式（§4.5 冻结）未动；旧 fallback TU UID 不再产生
  （其 editorial ID 仍保留在 editorial_to_tu 映射，指向新 strong TU）。
- identity.sqlite 为 current-state cache（§10.1），删除重建即得新状态，无需数据迁移。

## 6. 回滚边界

- 仅删除本轮 16 个新基线文件（`rm i18n/baselines/*-cd42f9aedd365b398e69b472326d953055f7f9fe.{jsonl,meta.json}`）
  即可回到冻结前状态；旧 29da216 文件未动。
- 代码回滚：撤销实现提交 `cd42f9a…`（registry 行 + extract.py 三分支替换 + G10/矩阵测试
  + 契约文档修订）；registry sha 回到 `219e7fdf…` 后旧基线即重新有效。
- 实现提交与基线重冻的依赖：基线绑定受审实现（两阶段提交），重冻不可先于实现提交。

## 7. PR 待办

- 本修订（契约文档 §12/§13/§15、本迁移记录、16 个新基线文件、实现提交 cd42f9a 内容）
  未推送/合并；PR 由用户另行指示，PR 合并后 `contract/0.1` 正式生效。
- 后续任务：`newEffect.desc` 槽位实现（另行任务，机制同 talent.info 原位重分类）。
