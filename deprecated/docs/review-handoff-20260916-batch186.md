# 翻译审核交接：第 179–186 批完成 + 一轮修复批，下一批为第 187 批

最后更新：2026-09-16 · 分支 `develop` · HEAD `0aec51d`
交叉复核模型：**`claude/claude-opus-5`**（用户本会话指定，已逐批核验）

本文取代 [第 165 批交接](review-handoff-20260915-batch165.md)。
只写手册里没有、或踩过坑才知道的部分；流程细节见
[`baseline-batch-runbook-2026-09-06.md`](baseline-batch-runbook-2026-09-06.md)。

---

## 1. 当前状态

| 项 | 值 |
| --- | --- |
| 已完成批次 | 第 179–186 批，均 review_only，17/17 门禁逐批通过 |
| 修复批 | `64a18db` → merge `0aec51d`，49 条 revision |
| surface 覆盖 | 16399 / 29828（**54.98%**） |
| deep_reviewed | 788 |
| **pending_repair** | **489**（见第 5 节，这是本次交接最需要注意的一项） |
| 未 push | `origin/develop` 停在 `2ad075c`，本地领先 **8 个提交** |
| 工作树 | 干净；`.ai/consult/` 是唯一 `??`，**严禁读取、暂存或清理** |

### 批次提交对照

| 批 | batch_id | evidence | 裁决 |
| --- | --- | --- | --- |
| 179 | `batch-343ae74a69305505cf8b` | `fe60c4f0` | confirmed 8 |
| 180 | `batch-0fddfd3e3ee9b08eb8f4` | `49ab709b` | confirmed 9 / advisory 8 / refuted 3 |
| 术语修复 | — | `893d337` → `2ad075c` | 61 条（Kyless/Zone-wide/Trollmire/The Master） |
| 181 | `batch-8ffba614b11fbda0391b` | `0b0253ff` | confirmed 12 / advisory 4 / refuted 2 |
| 182 | `batch-2c2856af72f9a562dd04` | `227b3ed7` | confirmed 5 / advisory 3 |
| 183 | `batch-e8091bc9e208567f5ce0` | `1b415cba` | confirmed 5 / refuted 3 / advisory 1 |
| 184 | `batch-34e32753445351e6c8a1` | `1464d3d5` | confirmed 8 / advisory 2 |
| 185 | `batch-2812a8e51db8160858ae` | `7af3a4b8` | confirmed 9 / advisory 6 / pending 3 / refuted 2 |
| 186 | `batch-e87bfaee8dbe226648bb` | `0b87e498` | confirmed 6 / advisory 3 / pending 2 / refuted 2 |
| 修复批 | — | `64a18db` → `0aec51d` | 49 条 revision |

---

## 2. 用户本会话的裁决（全部已落地，后续直接执行不必再问）

| 项 | 裁决 | 落地情况 |
| --- | --- | --- |
| The Master | 保持「领主」 | `2ad075c` |
| Trollmire | 「巨魔沼泽」 | `2ad075c`，`terminology/places.tsv:28` 升为 preferred |
| yeek | 保持「夺心魔」 | 不动，不再作为缺陷登记 |
| Zone-wide | 「区域效果」 | `2ad075c` 统一术语；`0aec51d` 补齐标点 |
| Kyless | 「凯勒斯」 | `2ad075c`，37 条 |
| **死亡描述类** | **保持 pending，且 `killer_message` 一并计入冻结范围** | 见下 |
| Rogue Plight | 「盗贼之厄」 | `0aec51d`，3 条 + `terminology/items.tsv` |
| immunity / Zone-wide 标点 | 需修 | `0aec51d` |
| Archmage(24) / Travel Speed(6) / vial | **不动** | — |
| 其余族级议题 | 保持 pending | — |
| 同族连带条目 | **一并修复** | `0aec51d` |

### 死亡描述类的冻结范围（2026-09-16 扩展）

原范围是 `data/damage_types.lua` 里各伤害类型的 `death_message` 词表（约 16 条增添器官／意象）。
用户本会话裁定 **各阵营 NPC 的 `killer_message` 一并计入**。

据此已置 pending 的条目：
- `cleaved`（第 185 批，`damage_types.lua:778` PHYSICAL 表）
- `timewarped`（第 186 批，`damage_types.lua:1006` TEMPORAL 表）
- `and burned on a pyre`（第 186 批，`ziguranth.lua:29` `killer_message`）

**后续遇到同类不必再提请界定，直接 pending。**

---

## 3. 本会话确立的判定规则（对后续裁决有约束力）

1. **族内一致度达惯例门槛时，单条修复有害**（→ advisory + 登记）；**未达门槛时按单条机制正确性处置**（→ confirmed）。
2. **「删限定词」是一类系统性缺陷**（may / chance / up to / each / high level / every turn），
   按机制正确性判定，**不走惯例门槛**。
3. **机制术语上译文与英文串冲突时，先查引擎字段再判谁错**——英文源串有时才是不准确的一方。
4. **交叉复核看不到语料**。它关于「族内既有译法」的结论，**无论 ISSUE 还是 OK**，
   都必须经宿主查全库后才能采信。本会话共 8 次同类反证（第 179/180/181/182/183/184/185/186 批各一）。
5. **「两方一致」同样不等于可采信**（第 185 批 Travel Speed）：表层与交叉复核都判 ISSUE，
   但本库第 1864 行存在库内定义句，已先行消解歧义，单条修复反而制造不一致。
6. **专名改名归用户裁决**，不自行决定（Kyless、Rogue Plight 两次先例）。

### 已实测的惯例门槛（判 advisory / confirmed 的量化依据）

| 信号 | 比例 |
| --- | --- |
| 换行数保持 | 1865 : 244（88%） |
| 制表符保持 | 857 : 41（95%） |
| `unided_name` 无句末句点 | 397 : 12（97%），12 例外全是 `vial of <colour> fluid` |
| 句末 `!` 保持 | 1486 : 19（98.7%） |
| 数字紧贴 `%%` | 641 : 15（97.7%） |
| **伤害类型词直接修饰「伤害」** | 19 : 7（**73.1%**）——**低于门槛区间，不可作为判缺陷的依据** |

---

## 4. 修复批 `0aec51d` 的内容与要点

catalog `72472f84` → `2496c91d`，migration `762f9587`
（`revision_changed 49`、`ambiguous 0`、`unmapped 0`、`queued_successors 49`）。
**四哈希绑定核验四项全部一致**。strict lint 30308 条 0 错 0 警，17/17 门禁通过。

- immunity→免疫 10 条：ZONE_AURA 系列 11 条中仅 36698「击退免疫」原本正确。
- Zone-wide 标点 11 条：冒号 11 处 + 行内逗号 9 处。**全库另有 10 处 ` , ` 不在 Zone-wide 行内，未动。**
- 族内连带 22 条：lure 高等级 4、Repel/Surge 顺序 3、exotic weapons 3、Highborn's Bloom 2、
  `[Boss]`/`[MiniBoss]` 3、Rogue Plight 3、Distortion Bolt 2、crackling spot 1、Herah 1、`150 %%` 间距 1。
- 整句重写 7 条：念力/充能护盾、Distortion Bolt 引爆条件、Eyal、沙漏、软泥使、Sher'Tul 训谕。

### 三个容易重复踩的坑

1. **`[Boss战]` 不能全局替换**——`mod-tome.lua:1274` 的 `Boss fight! → Boss战！` 是**正确的**，
   必须用方括号精确限定（`\[Boss战\]`、`\[小Boss战\]`）。
2. **新增 `T.GAME.ENTITY` 术语行必须同步登记 `tools/annotate_domains.py` 的 `ITEM_SOURCES`**，
   否则 `10-domain-annotation` 门禁报 `unmapped T.GAME.ENTITY source` 直接失败。
   `T.PN.PERSON` 等走 `CATEGORY_DOMAIN`，不需要改工具——Kyless 那次就没遇到。
3. **改术语表会动 `tests/i18n/test_toolchain_static_audit.py` 的行数基线**（本次 721→722）。
   改基线前必须先跑 `python3 -B tools/annotate_domains.py` 确认
   `unmapped 0 / declared_domain_mismatch_count 6 / ok True` 三项语义指标未变，
   **只有条目数变化才允许改基线**——不要把语义失败当成基线失败。

### 护盾两条的处置说明

以同族 `36111` 热能护盾为范本改写，因此**没有**补译 `powerful`——范本自己也没译。
族内一致优先于逐词对齐。交叉复核曾指出 `powerful` 被删，宿主未采纳该点并已在证据里说明。

---

## 5. ⚠ `pending_repair` = 489，这是最需要接手人注意的一项

**`repair_required` 是活的待办清单，不是历史留痕。** 验证方法：
runbook 中记录了 repair merge 的批次（第 43/44/47 批）在 `state_override` 里
**全部为 `done`、零 `repair_required`**。

```bash
python3 - <<'PY'
import sqlite3
db = sqlite3.connect('.artifacts/i18n/production-review-v2-lite/queue.sqlite3')
cur = db.cursor()
cur.execute("SELECT state, COUNT(*) FROM state_override GROUP BY state")
print(dict(cur.fetchall()))
PY
```

当前 489 条，横跨约 95 批。按 `updated_at` 看，**修复动作在 2026-09-12 之后就停了**，
此后每天新增约 100 条：

| 日期 | 批次数 | 新增待修条数 |
| --- | ---: | ---: |
| 09-12 | 6 | 22 |
| 09-13 | 28 | 148 |
| 09-14 | 13 | 68 |
| 09-15 | 29 | 150 |
| 09-16 | 20 | 121 |

修复批 `0aec51d` 只覆盖了用户明确批准的范围（49 条），**其余 489 条一条未碰**。

> **这是一份未向用户交付方案的待办。** 宿主向用户提了三种做法
> （分批清理 / 集中清理 / 先抽样评估类型分布再定），并明确倾向第三种——
> 因为没读过那 489 条的内容，给任何工期或分批建议都是猜的。
> **用户尚未答复。接手人不要在未经用户裁决的情况下自行清理。**

---

## 6. 仍在 pending 的族级议题（用户已裁定「保持 pending」）

| 议题 | 规模 | 备注 |
| --- | ---: | --- |
| Haunted 族 | 5 | 含与 `entangle` 的「纠缠」双向撞名 |
| talent type 尾词策略 | 6 | `drake aspect` 5 条 + `higher draconic abilities` 1 条，同一条目块 |
| 格式规范化规则 | 4+ | 需要的是**一条规则**而非逐条改：原文硬折行是否保留、行尾空白保持还是清除 |
| `Unity` / 维网联动 | 1 | 弱，可不做 |
| 死亡描述类 | ~16 + killer_message | 用户裁定冻结 |

用户已明确**不动**的：`Archmage→元素法师`（24 处）、`Travel Speed→飞行速度`（6 处 + 第 1864 行定义句）、
vial 族（去句点 12 条 + 形容词忠实度）。

---

## 7. 恢复入口（第 187 批）

用户授权**连续主持**，逐批自动推进不必确认。当前无 active batch，可直接开批。

```bash
# 1. 脚手架（沿用上一批，清掉上一批产物）
cp -r .artifacts/i18n/batch186-orchestration .artifacts/i18n/batch187-orchestration
D=.artifacts/i18n/batch187-orchestration
rm -rf $D/raw $D/native $D/batch-e87bfaee8dbe226648bb* $D/*.log $D/*-result.json \
       $D/BID $D/CTX_AGENT $D/LANE3 $D/SURFACE_AGENTS $D/contextual-* $D/surface-* \
       $D/host-* $D/status-*.json $D/ctx-tool-audit.json $D/workspace-mcp-capture.json \
       $D/publication-check.json $D/create-*.json $D/harvest-*.json $D/archive-*.json
sed -i 's/batch186-orchestration/batch187-orchestration/g' $D/*.py
grep -rln 'batch186\|batch-e87bfaee' $D/    # 必须无输出

# 2. 开批（注意是 --limit，不是 --count）
python3 -B $D/run-host-phase.py batch-start python3 -B tools/i18n production batch start --limit 80
echo <新 batch_id> > $D/BID
```

阶段顺序（**不可跳步**，`run-host-phase.py` 会因 log 已存在而拒绝重跑，
失败重跑用新阶段名如 `xxx-2`）：

```
freeze-workset → surface-export → stage-surface → dispatch-surface-prepare
→ [create lane 0-2 → 收一条再 create lane 3] → close-surface → surface-import
→ contextual-export → stage-contextual → dispatch-contextual-prepare → create ctx
→ harvest/archive → audit-ctx-tools → close-contextual → contextual-import
→ 写 host-decisions.json → build-host-artifacts → adjudication-chain
→ publish-check → persist-host-review → commit → finalize → 归档 scratch
```

### profile id（固定）

- 表层：`agent_profile_mt3s8sou_fggrhfnq1gj`（`codex/gpt-5.6-sol`，medium，`auto-review`）
- 交叉复核：`agent_profile_mtjlooyy_myzr9tapied`（`claude/claude-opus-5`，medium，`auto`）
- 工作区：`wks_420314270844170b`

### 几个必须照做的细节

- **并发上限 3**：先建 lane 0–2，收割归档一条后再建 lane 3。
- **`contextual-stage-plan.json` 是宿主手写的，不是拷贝来的**——
  本会话曾误把表层 `dispatch-plan.json` 复制成它。正确做法：
  读 `.ai/task/<BID>-contextual-000/CONTEXTUAL-ENVELOPE-final-full.json`，
  取 `candidate_identity` 与 `len(payload.ordered_revision_keys)`。
- **`surface-import` / `contextual-import` 要 `--input` 索引文件**，内容是 `{"序号": "raw 绝对路径"}`。
- **裁决键必须是 10 位 hex + `|surface`/`|contextual`**，值只含
  `{disposition, repair_required, conclusion}` 三个字段；
  `repair_required=true` 只允许出现在 `confirmed` 上。
- **`publish-check` 必须先于 `persist-host-review`**。
- **finalize 要完整 40 位 sha**。
- **归档 scratch 要在下一批 `contextual-export` 之前做**，且先与已提交证据逐字节比对：
  `git show HEAD:evidence/production-review-v2-lite/batches/<BID>/raw/contextual/004-{input,output}_path.json | sha256sum`
  ——**路径索引恒为 `004-`，不随 entries 数变化**，按条目数推算会读到空文件（`e3b0c442…` 是空输入的 SHA256，
  两边都返回它看着像「一致」，实则是两次失败的读取）。

---

## 8. 本会话新增的工具行为记录

- **冻结 MISS 连续 4 批为 0**（第 183–186 批）。第 182 批出现本会话唯一一次：
  `gem.lua | alchemist emerald`，成因是 `gem.lua:83` 的 `name = "alchemist "..name:lower()` 运行时拼接。
  系统处理正确——锚定到正确源文件、`matching_literal_lines` 为空、经 section 绑定得
  `verification_status: confirmed`，**未回退到 locale 文件掩盖问题**。binding 的 `literal 79 / sha 80` 即由此而来。
- **`D_write_attempts` 误报有两种形状**，不要因为前几次是某一种就默认这次也是：
  - 形状一（第 174/176/180/182 批）：引号内 Python 字面量 `'>>'`。
  - 形状二（第 183 批）：`2>/dev/null` 里的 `>`。
  核验三步：工具种类只有 Bash → 正则扫真正的写形状命中 0 → 两个工作树 `git status` 无该 agent 新增改动。
  第 184–186 批 D 类未触发。
- **`claude` 提供方的 `runtimeInfo.model`**：第 183 批起开始返回 `claude-opus-5` 而非 `null`，
  与 `persistence.metadata.model` 互证。但 `null` 的出现条件未知，**双读核验仍保留**。
- **`mcp__paseo__create_agent` 不接受 `cwd` 参数**（schema 只有 `title`/`provider`/`initialPrompt`/
  `settings`/`labels`/`notifyOnFinish`/`workspaceId`）。传了会报 `unrecognized_keys`，
  且错误信息里还会附带看似无关的 `relationship`/`workspace` 缺失报错，容易误导。

---

## 9. 多模型术语咨询的方法教训（本会话新增）

Rogue Plight 定名走了 **三轮**（Kyless 那次两轮即一致），多出来的一轮是宿主的错造成的。

第二轮我给三方的语料挑战里写「『厄』在本库 82 处，表意的仅约 3 处」，
**实际是音译 49 : 表意 33（40%）**。错因是只统计了 `t("...", "...厄...")` 短名对，
漏掉正文长文本里的用例，差了十倍。

后果：Opus 4.6 据此从「盗贼之厄」改投「盗贼之殃」，把本该 3:0 的一致变成 2:1。
更正后单独重问它，它撤回改判（「论据消失，结论不应保留」）。

**规则**：凡要写进 brief 的计数，用两种口径各算一次再比对；
字频类挑战必须区分「音译用字」与「表意用字」；
发现数字有误时**只向受影响的参与方重问**，并在 brief 里明说其论据建立在被更正的数字上。
完整记录见 `.artifacts/i18n/rogue-plight-consult/consult-record.json` 的 `host_correction` 段。

---

## 10. 交接收尾

- 本地领先 `origin/develop` **8 个提交**，**未 push**（用户上次只授权 push 到 `2ad075c`）。
  push 前请向用户确认。
- `.ai/consult/` 始终是唯一 `??` 条目，**严禁读取、暂存或清理**。
- review_only 批次**不修改**任何 Lua 译文、术语表或 catalog 文件；
  `batch start` 到 evidence 提交之间**不得有任何其他提交**。
- 待用户答复的唯一阻塞项：**第 5 节的 489 条 `pending_repair` 如何处理**。
