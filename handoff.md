# ToME4 翻译质量 Evaluator 交接说明

更新时间：2026-08-07

## 1. 当前工作区

- 工作区：`/Users/yun/projects/tome4-chinese-translation-review-fixes`
- 分支：`codex/review-findings-20260802`
- HEAD：`34ac1c473d4e830325dd2b04a968439c9d0ca97c`
- 主工作区 `/Users/yun/projects/tome4-chinese-translation` 位于 `tools-i18n` 分支，不是本轮工作区。
- 当前工作树包含大量尚未提交的 Evaluator v3、Facts Study、schema、prompt、测试和文档改动。它们均属于当前工作，不能清理、reset、checkout 或用旧文件覆盖。
- 本轮没有提交、推送、发布或修改规范 Lua、术语内容与正式 120 条样本。

仓库级运行、安全、DLC 源码和审核规则以根目录 `AGENTS.md` 为准。首次使用工具仍先运行：

```bash
python3 -B tools/i18n doctor
```

当前离线闭环的决策完整实施方案见
[`docs/translation-quality-offline-closure-plan.md`](docs/translation-quality-offline-closure-plan.md)。
本文只维护状态、实验结论和继续工作的安全边界，不重复实施细节。

## 2. 当前目标与决策

原目标是降低 AI 翻译质量 evaluator 的主观性。Evaluator v3 已把 severity、技术门禁和 anchor 归一化移到宿主，但外部校准分析进一步确认：当前瓶颈已经从 JSON/schema 合法性转为以下三件事是否具有统一语义：

1. 模型是否报告同一个问题；
2. 模型、anchor、matcher 和 stability 是否把它识别为同一个 claim；
3. Facts 是否帮助模型发现真实问题，还是改变注意力并诱发过度解释。

当前决定：

- 不运行 v4 holdout 或正式 120 条。
- 不降低稳定性门槛，不追加调用刷出一次通过。
- 不修改或重新解释 v1–v3 历史 artifact。
- 先完成隔离的 `facts-study-v1/v2` 因果研究，再决定是否把 Facts 通道纳入 v4 draft.3。
- 当前没有可执行的外部 Facts Study preregistration；下一次外部传输必须重新冻结输入并取得新的明确授权，不能沿用此前 calibration 授权。

## 3. Evaluator v3 已实现内容

主要实现与契约：

- 独立模块：`tools/i18nlib/quality_v3.py`
- 设计文档：`docs/translation-quality-evaluator-v3.md`
- policy/rubric/prompt：
  - `i18n/quality/policy-v3.json`
  - `i18n/quality/rubric-v3.md`
  - `i18n/prompts/pi-quality-evaluator-v3.md`
- severity matrix 与 anchors v2：
  - `i18n/quality/severity-matrix-v1.json`
  - `i18n/quality/anchors-v2.json`
- v3 assessment、adjudication、match、report、stability 等 schema 已隔离新增。
- CLI 已增加 v3 版本化入口；`tools/pi-quality-evaluator` 可按 sample contract 区分旧契约与 v3。
- v2 文件和历史读取语义保持兼容，缓存身份不应跨 v2/v3 命中。

v3 的核心方向是：模型只报告可观察的实质语义差异；宿主根据 error-code/phenomenon 矩阵、技术 gate、anchor 和确定性规则派生分类、severity 与人工路由。

此前校准分析发现：DeepSeek 两轮 findings 发生明显整体翻转，Luna 更稳定但存在稳定伪阳性。更严重的是历史实现曾同时存在 exact-span anchor、负 anchor 标签绕过、多个 matcher 和稀疏人工队列指标等不一致。相关诊断已经沉淀到文档和当前 v3/Facts Study 设计中；封存集仍保持冻结。

## 4. Facts Study 当前实现

主要文件：

- 实现：`tools/i18nlib/facts_study.py`
- 外部 runner：`tools/i18nlib/pi_facts_study.py`、`tools/pi-quality-facts-study`
- 协议：
  - `i18n/quality/facts-study-v1.json`
  - `i18n/quality/facts-study-v2.json`
  - `i18n/quality/facts-study-exclusions-v1.json`
- 文档：
  - `docs/translation-quality-facts-study-v1.md`
  - `docs/translation-quality-facts-study-v2.md`
- 七个 arm prompt：`i18n/prompts/pi-quality-facts-study-{a,b,c,d,n,l,f}.md`
- 独立语言通道边界：`i18n/quality/language-channel-v1.json`
- 测试：`tests/i18n/test_facts_study.py`

研究架构：

- A：最小 baseline
- B：开放式实质语义 checklist
- C：裸 Facts
- D：checklist + Facts-first
- N：与 Facts 等形状、等 canonical JSON 字节长度的 neutral padding
- L：Facts-late 位置诊断
- F：独立、全新会话的 Facts-only verifier
- T：宿主对 B 与 F 做 union/dedupe，不额外调用模型

预注册设计上限为 33 次一-shard 传输：Luna 七个 arm 各三轮，共 21 次；DeepSeek 对 B/D/L/F 各三轮，共 12 次。缓存关闭，失败消耗 slot，不允许替换。

Facts v2 已改为 supplemental-only：

- Facts 作者不得看到 target 或 gold。
- 每项允许 0–4 条事实；没有真正补充信息时必须为零。
- 禁止复述 source、item kind、source tag 或 bounded context。
- provenance 只允许 `terminology`、`public-source`、`versioned-context`。
- v1 packet/schema 仍保留历史语义。

## 5. 三轮人工数据实验

### 5.1 失败 pilot：Facts v1

目录：

`.artifacts/i18n/quality/runs/20260806T171711.716744Z-facts-study-build/`

结论：Facts 作者生成的 49 条事实中有大量公共输入复述，表面满足的 addressed 数没有有效因果意义。该轮已经登记为 failed pilot；其 20 个 revision 被 `facts-study-exclusions-v1.json` 排除。不要将该轮恢复为可用研究集。

### 5.2 supplemental-only v2 随机候选轮

目录：

`.artifacts/i18n/quality/runs/20260806T230158.697398Z-facts-study-build/`

身份：

- study ID：`ff5931a835e6efa884b3dfeeda385bce260046a2c8940482008951d6cc0dab47`
- Facts：20 条，1 个零事实项
- 独立 Gold A/B：各 8 claims
- 最终裁决：8 claims，1 fact-addressed、7 fact-unaddressed、15 clean、8 fact traps、3 acceptable localization

宿主 lineage、evidence 和 provenance 校验通过，但 frozen gold 正确拒绝：未达到至少 8 addressed + 8 unaddressed。没有进入 33-slot fake/external replay。

关键 artifact：

- `fact-packets.agent-facts-v2.json`
- `gold-review-a.agent-v2.json`
- `gold-review-b.agent-v2.json`
- `gold-adjudication.agent-v2.json`

### 5.3 长文本优先轮

最终有效目录：

`.artifacts/i18n/quality/runs/20260806T235802.809162Z-facts-study-build/`

不要使用此前生成后舍弃的重复候选目录：

`.artifacts/i18n/quality/runs/20260806T235703.429602Z-facts-study-build/`

有效轮身份与数据：

- study ID：`69f99f7e021bfbd5d74dcd7104bf340200969828f4541e952387da3167cb15d4`
- 20 个唯一 source/target 对
- 与失败 pilot、v2 随机候选和舍弃候选均零 revision 重叠
- source 长度：中位数 199、平均 653.5、范围 25–1514；上一轮中位数 33、平均约 141
- Facts：23 条，4 个零事实项；10 条 terminology、13 条 public-source
- Gold A：28 claims，3 addressed、25 unaddressed
- Gold B：19 claims，1 addressed、18 unaddressed
- 最终裁决：29 claims，3 addressed、26 unaddressed、8 clean、7 traps、5 acceptable localization
- adjudication SHA-256：`f830d1104f319c89be546f0983366854984b83fcb872358aab83d9b943ecc54d`

关键 artifact：

- `sample.json`
- `fact-packets.agent-facts-long-v2.json`
- `gold-review-a.agent-long-v2.json`
- `gold-review-b.agent-long-v2.json`
- `gold-adjudication.agent-long-v2.json`

宿主验证结果：authoring lineage 完整，draft gold 合法；将其切换为 frozen 时 validator 因 addressed=3<8 正确拒绝。没有运行 33-slot fake replay，更没有外部 provider 调用。

实验结论：长文本把最终普通语义 claims 从 8 增加到 29，但 fact-addressed 只从 1 增加到 3。文本长度提高的是一般错误密度，不是 Facts 因果信息密度。

## 6. 本轮候选生成器改动

`tools/i18nlib/facts_study.py` 当前还包含以下未提交修订：

1. `_revision_ids_from_artifact()` 会继承输入 sample 的 `excluded_revision_ids`，避免只排除该 sample 的 20 个可见 items 而丢失上游 lineage。
2. seed 以 `tome4-facts-study-v2-long-source-v1` 开头时，启用可重算的长文本优先选择；profile 内长度得分在约 1500 字符达到峰值，避免单条万字文本吞噬一 shard。
3. 候选选择禁止同一个 `(source, target)` 对重复进入 20 条样本。
4. `tests/i18n/test_facts_study.py` 增加长文本选择、传递排除和唯一文本对回归测试。

不要删除这些修订；后续如果引入新的 curation contract，应决定保留为通用候选约束还是迁移到专用 curator。

## 7. 已确认的契约缺口

下一轮数据构建前必须处理：

1. `facts-study-gold-review-v1.schema.json` 和 gold schema 只严格约束顶层，没有正式定义 item/claim/evidence 对象；当前字段和枚举主要存在于 Python validator。上一轮不得不向无上下文审校者额外提供实现级字段定义。
2. public-source provenance 的 `reference` 有时写成 `path:line`，而 SHA-256 实际绑定整个文件；应把文件身份与 locator 拆成独立字段，不能依赖调用方剥离行号。
3. Facts statement 使用语言尚未冻结；不同轮次分别出现英文和中文事实，可能成为未控制的实验变量。
4. 版本化历史 exclusion registry 当前只正式登记 failed pilot。后续轮次依靠传入前一 sample 的传递排除实现零重叠；新 curation lineage 应显式冻结全部排除来源。
5. `other`、`unknown`、上下文不足、证据无效仍需保持不同的 uncertainty/routing 生命周期，不能重新折叠成 provisional minor。
6. 受控样本若加入，必须拥有独立 mutation lineage，并从 evaluator bundle 中完全隐藏。

## 8. 下一步推荐方案

不要进行第四轮随机或单纯长文本抽样。新增隔离的 `facts-study-curation-v1`，目标是构建“Facts 依赖性富集”而非“文本长度富集”的开发集。

推荐顺序：

1. **冻结 curation 契约**
   - 完整定义 Gold claim/evidence schema。
   - 为 sample 增加 `origin: natural|controlled`、selection stratum 和隐藏 mutation lineage。
   - 结构化 provenance 文件身份/locator/hash。
   - 冻结 Facts statement 语言。

2. **构建约 80 条 source-side 候选池**
   - 术语/专名约 20；机制/条件/数值约 20；实体关系约 15；UI role 约 15；clean fact-trap 候选约 10。
   - 长度约 80–1500，不再把长度本身当成功指标。
   - 排除正式 120、32+32、所有历史 Facts revision 和重复文本对。

3. **Facts 作者先 target-blind 标注并冻结**
   - 对整个候选池生成 supplemental-only Facts。
   - 此时任何 target-visible 角色尚未开始工作。

4. **独立 target-visible curator 分层**
   - `fact-dependent-defect`
   - `surface-defect`
   - `clean-fact-trap`
   - `acceptable-localization`
   - `unsuitable/uncertain`

5. **构建最终 20 条**
   - 8 个 fact-dependent defect items，目标至少 8 addressed claims。
   - 6 个 surface-defect items，目标至少 8 unaddressed claims。
   - 6 个 clean/acceptable items，其中至少 5 clean、3 fact traps。
   - 优先自然错误；不足部分可在隔离研究 artifact 中创建最小受控 target 变体，但 natural/controlled 指标必须分开，且不得修改规范译文。

6. **重新执行四角色 Gold 流程**
   - target-blind Facts 作者；Gold A；Gold B；独立 adjudicator。
   - 宿主只做 schema、hash、evidence、lineage 和 coverage 验证，不补造 claims。

7. **离线验收**
   - 8 addressed + 8 unaddressed + 5 clean + 3 traps。
   - 完整 33-slot fake replay。
   - natural/controlled 指标分离。
   - 一轮全新、只读、无上下文复审。

8. **外部执行门槛**
   - 重新冻结 prompt、sample、Facts、gold、arm schedule、seed 和全部 hash。
   - 再次报告 Luna/DeepSeek provider、model、thinking、20 条、一 shard、21+12 次上限。
   - 取得新的明确外部传输授权后才能执行。
   - controlled subset 只能证明 Facts 的机制增益，不能单独授予 v4 holdout clearance。

## 9. 最近验证基线

当前相关验证：

- `python3 -B tools/i18n doctor`：通过；公开引擎仓库的 protected-source scan warning 为既有提示。
- `tests/i18n/test_facts_study.py`：22/22 通过。
- `tests/i18n/test_toolchain.py`：401/401 通过。
- strict lint：30,177 translations，0 errors，0 warnings。
- runtime collisions：0。
- duplicate runtime keys：1,717，桶 B=0、桶 C=0，均为合法跨 section 重复。
- `py_compile`：通过。
- `git diff --check`：通过。

早先在 v2 contract 修订完成后，quality-v3 + facts-study 组合测试和 v2 legacy 回归也已通过；后续改动仅涉及候选选择与对应 Facts Study 测试。

## 10. 常用命令

```bash
python3 -B tools/i18n doctor
python3 -m unittest -q tests/i18n/test_facts_study.py
python3 -m unittest -q tests/i18n/test_quality_v3.py tests/i18n/test_facts_study.py
python3 -m unittest -q tests/i18n/test_quality_v2.py
python3 -m unittest -q tests/i18n/test_toolchain.py
python3 -B tools/i18n lint --strict
python3 -B tools/scan_runtime_collisions.py
python3 -B tools/classify_runtime_keys.py
git diff --check
```

当前 Facts candidate build 入口：

```bash
python3 -B tools/i18n quality facts-study-build \
  --inventory <inventory.jsonl> \
  --exclude-sample <prior-sample.json> \
  --seed <frozen-seed>
```

不要直接运行 `tools/pi-quality-facts-study`。真实 provider 调用必须在完整 preregistration、冻结输入、独立复审和新的用户授权之后进行。

## 11. 交接停止点

当前工作停在“长文本人工裁决完成但 Facts coverage 不足”的诊断终点。正确的继续动作是先实现并审核 `facts-study-curation-v1` 数据契约和富集流程，而不是继续随机抽样、运行 holdout、发送正式 120 条或启动外部 33-slot campaign。

## 12. 离线闭环实施状态（2026-08-07 更新）

`docs/translation-quality-offline-closure-plan.md` 的工程部分已完成并全部通过
门禁；五个隔离角色（Facts author、curator、Gold A/B、adjudicator）执行在外部
授权边界之前停止（见 §13）。

已落地：

- **共享核心**：`tools/i18nlib/quality_contracts.py`（canonical JSON/SHA-256、
  严格字段/枚举/SHA/相对路径校验、结构化 provenance
  kind/resource/locator、subject identity、ArtifactRef）与
  `tools/i18nlib/quality_claims.py`（evidence span 规范化、exact
  claim_signature、legacy-v2/v3/facts 与 canonical-v1 四个兼容 profile、
  对称最大权匹配、稳定聚类、独立不确定性路由：unknown/other/
  taxonomy-unknown/context-insufficient → manual，evidence-invalid → rejected，
  均不自动派生 minor）。`quality_v2.py`、`facts_study.py` 通过 re-export 调用
  公共实现，重构前后同一 fixture 的兼容基线逐字节一致（探针
  `.artifacts/i18n/quality/offline-closure/probe_compat.py`）。
- **数据集登记**：`i18n/quality/dataset-registry-v1.json`（8 个登记项、276 个
  revision：正式 120、32+32、探索集、失败 pilot、随机/长文本/舍弃候选）；
  工具只读 registry 并生成 `registry-fragment`，主代理显式合入。
- **Curation 契约**：`facts-study-v3.json`（protocol v3，含 quota、length
  policy、controlled policy）与 15 个新 schema（quality-common-v1 公共
  claim/evidence/provenance $defs；pool/curator bundle/curator
  assessment/fact-packet-v3/facts-author-bundle-v3/sample-v2/gold-v2/
  gold-review-v2/gold-adjudication-v2/bundle-v2/assessment-v2/
  preregistration-v2/report-v2/validation-index-v2，全部带完整嵌套 $defs）。
- **Curation 命令**：`facts-study-curation-build/prepare/select` 三个新命令；
  `facts-study-bundles/validate/report` 按 sample/prereg/validation contract
  自动分派 v1/v2。`facts-study-curation-build` 已用最新 inventory
  （`20260807T061056.017006Z-inventory`，sha256 d8188a38…）真实运行，产出
  80 条 source-side 候选池（`20260807T061101.335922Z-facts-study-curation-build`，
  pool_id `58ade3e4…`），五个 stratum 均达配额；ui-role 因 80–1500 字符带内
  仅 2 条，按 policy 显式报告 relaxation（15 条全部为 relaxed short）；
  与 registry 276 个排除 revision 零重叠。
- **离线链条**：`facts-study-curation-validate --fake-runner` 只接受
  offline-frozen preregistration（外部 assessment/runner report 一律拒绝）；
  新 prereg 状态固定 `offline-frozen`，`tools/pi-quality-facts-study` 显式拒绝
  执行；33-slot fake replay 与 report v2（natural/controlled 指标分离、
  `non-evidentiary-offline-replay`）已通过 fixture 集成测试。
- **测试**：新增 `test_quality_contracts.py`（14）、`test_quality_claims.py`
  （36）、`test_dataset_registry.py`（17）、`test_facts_curation.py`（26），
  共 93 个新测试；`test_quality_v2.py`/`test_quality_v3.py` 补 tools 路径
  bootstrap，干净 shell 可直接运行。全部门禁通过：
  doctor 0、lint 30177 条 0 error 0 warning、quality 套件 185、toolchain
  401、collisions 0、classify 桶 B/C=0、`git diff --check` OK。

## 13. 停止点：五个隔离角色与 Gold 冻结

按方案与 `AGENTS.md` 授权门槛，以下步骤必须取得新的明确外部授权后才能执行
（provider=opencode-go，model=deepseek-v4-flash，bundle 类型：80 条
target-blind Facts author bundle、80 条 target-visible curator bundle、20 条
Gold review A/B、匿名 adjudication）：

1. Facts author（target-blind，禁读 target/gold/curator）→ 冻结 80 条 packet；
2. `facts-study-curation-prepare` → curator bundle + assessment 模板；
3. curator（target-visible，禁读 gold）→ 冻结 assessment；不足 8 条
   fact-dependent 时首次 select 返回退出码 2 与受控变体 request；
4. Gold A/B（只看最终 sample + Facts）与独立 adjudicator；
5. `facts-study-curation-select`（必要时带 `--controlled-variants`）→ 20 条
   sample v2 + Gold 模板 + registry fragment；
6. `facts-study-bundles --pool --facts-pool …` → offline-frozen prereg；
7. `facts-study-validate --fake-runner` + `facts-study-report` → 33-slot
   非证据性 fake replay 与 natural/controlled 分离报告。

受控变体仅补 fact-dependent 缺口（最多 8 条、每 base 一条、结构必须逐字节
保持），不授予任何后续 clearance。外部 33-slot campaign 还需要另建绑定用户
授权的 execution manifest。

## 14. curation-v1 真实角色执行结果（2026-08-07，已授权外部传输）

授权：provider=opencode-go、model=deepseek-v4-flash、thinking=max；bundle 类型
与条目数按 §13 报告并经用户明确授权。执行方式：`tools/pi-quality-role`
（新增，无会话/无技能/无项目上下文；facts-author 用 `--tools read,bash` 且
cwd 隔离到仅含 terminology.tsv 与固定公开源的工作目录，其余角色 `--no-tools`；
`isolation_mode=auditable-soft`）。

已完成的角色与产物：

1. **Facts author**（target-blind，80 条，177 条事实，0 条 source 重述）：
   `fact-packets.frozen-v3.json`（sha256 bde6bc62…）。provenance 全部通过宿主
   核验：100 个 engine 文件哈希、15 个 DLC 文件哈希全部匹配实际文件，62 个
   terminology 行号全部有效（1–693）。工具审计：141 次工具调用全部落在允许
   的公开源（t-engine4/tome4-dlcs）或工作目录内，无规范译文/凭据读取；1 次
   /tmp 草稿读取（自身 scratch，已记录）。author workdir 经 symlink 提供
   engine + 三个 DLC。
2. **curator**（target-visible，80 条）：两轮独立运行（v1.0 与校准 v1.1
   prompt）分布一致：68 clean、4 fact-dependent、3–5 acceptable/surface、
   **0 fact trap**。宿主抽查 14 条 clean 判定与 curator 一致；curator 判定
   随文本长度区分（17 条长文本 4 条缺陷 vs 63 条短文本 3 条），与历史长文本
   结论一致。冻结 assessment：
   `curator-assessment.frozen-v1.json`（sha256 2437485a…）。
3. **select**（真实数据）：按设计返回退出码 2 +
   `controlled-variants.request.json`（fact_dependent_needed=4）。

**本轮结论：配额失败，按方案不放宽门槛。** surface-defect 3/6 与 fact trap
0/3 无自然候选可补且按设计无受控补足机制（受控只能补 fact-dependent 缺口，
最多 8 条）；补足 fact-dependent 缺口（4→8）无法改变 outcome，故不执行
受控填充。sample v2、Gold、preregistration、33-slot fake replay 与 registry
fragment 均未冻结。完整证据见
`.artifacts/i18n/quality/curation-v1-round-report.json`。这与历史 v2 随机候选
轮（gold 配额拒绝）和长文本轮（addressed<8 拒绝）同类的设计内失败路径。

后续选项（需新的明确授权/契约修订）：A) 构建 trap/surface 富集的新 pool 并
重跑角色链；B) 修订冻结配额契约（破坏性变更，提升 contract 版本）后重选。

## 15. curation-v1 富集轮（v5 契约修订）完成（2026-08-07）

用户批准契约修订（方案 §14 选项 A）：`facts-study-v5` 协议把 select 阶段
surface 条目配额 6→2、fact-dependent 配额 8→12，**保留全部 claim 级冻结门槛**
（8 addressed + 8 unaddressed + 5 clean + 3 traps）。池复用 v4 长文本富集池
（`20260807T111704.162347Z-facts-study-curation-build`，pool_id 6556faac…，
80 条、70/80 ≥300 字符、排除 registry 276 + 旧池 80）。选择逻辑改为
trap-优先 clean + extra 优先未覆盖 stratum 的 acceptable（保证五 stratum 覆盖）。

执行（opencode-go / deepseek-v4-flash，沿用已授权范围）：

1. **Facts author**（v4 池，target-blind）：208 条事实，147 个 public-source
   文件哈希全部核验通过，61 条 terminology 行号有效；
   `fact-packets.frozen-v3.json` sha256 09b737e0…。
2. **curator**：两轮（v1.1 分布 13 fd/0 surface/0 traps；v1.2 修正 trap
   定义为"干净诱饵"后 13 fd/2 surface/5 traps）。冻结：
   `curator-assessment.frozen-v1.json` sha256 c90a1fd5…。
3. **select（v5 配额）**：20 条全 natural（12 fd + 2 surface + 5 clean trap
   + 1 acceptable ui），5 traps，五 stratum 全覆盖；
   study_id `fbc99a59f920e061…`。
4. **Gold A/B + adjudicator**：A 以两个 10 条分片运行（完整 20 条对模型过长，
   两次尝试均不完整；分片后有效）；B 的重复 claim id 由宿主确定性重编号
   （b-001…，内容不变，见 `normalization.record.json`）；adjudicator 合并出
   22 claims。冻结 gold（14 addressed + 8 unaddressed + 7 clean + 7 traps）
   通过 v5 配额与完整 lineage 校验；gold sha256 1b90741c…。
5. **bundles/validate/report**：`facts-study-bundles`（sample v2 分派）→
   offline-frozen preregistration（33 slots，prereg 25312c5b…）；
   `facts-study-validate --fake-runner` 33/33 通过；`facts-study-report` →
   report v2（non-evidentiary-offline-replay，natural 七 arm 指标分离，
   controlled 为空 = 全 natural 样本）。

修复的真实缺陷：neutral locator 等长填充（`_neutral_locator` 原实现用固定
{1,1} 导致真实行号下字节不匹配）；v1.1/v1.2 curator 与 gold-review prompt 的
trap 定义（契约语义是 clean 诱饵）。关键 artifact 均在
`.artifacts/i18n/quality/runs/20260807T124345.706087Z-facts-study-curation-select/`
与 `20260807T150743.324578Z-facts-study-curation-bundles/`。

## 16. 外部 33-slot campaign 完成（2026-08-08，用户授权）

经用户授权（B+B2、精确修订、传输层重试契约），campaign 10 完成 **33/33 槽全部通过**
并生成官方因果报告：

- **prereg**：`20260808T124932.424887Z-facts-study-curation-bundles`（prereg
  `a256…` 后重建为 `20260808T124932…`），execution manifest：parallel×4 +
  transmission retry×3 + timeout 5400。
- **执行**：Luna（openai-codex/gpt-5.6-luna）21 槽 + DeepSeek（opencode-go/
  deepseek-v4-flash）12 槽；26 槽 1 次尝试、7 槽经传输层重试成功（含 1 槽 4 次尝试）。
- **宿主规范化统计**：id 转录修复 2 处、finding 级丢弃 12 条（0.99% of 1218）、
  标点/空白规范化 33 处；全部记录于 runner report 的 normalization 字段。
- **验证**：`facts-study-validate`（external-assessments）33/33 通过，lineage/
  ledger/authorization 全绑定。
- **官方决策**：**`do-not-promote-facts-channel`**（report
  `20260808T175419.274533Z-facts-study-curation-report`，report_id
  871d8a5d…）。判据：Luna 3/7 失败（无稳定新增 true claims、T-B precision
  -3.2pp、trap FP 超限）；DeepSeek 判据全过（T-B recall +0.167、2 个稳定
  fact-addressed claims）但不足以单独推广。holdout_clearance=false。
- 关键指标（pooled×3）：Luna B P=0.097/R=0.197、D P=0.096/R=0.258（Facts
  无 recall 增益且 precision 恶化）；DeepSeek B P=0.344/R=0.167、T P=0.272/
  R=0.333。
- **结论**：Facts 通道在当前提示/样本下不能进入 v4 draft.3；DeepSeek 的
  方向性证据保留为后续研究输入。controlled subset 为空（全 natural 样本），
  natural/controlled 指标按契约分离报告。

## 17. 归档与正式报告（2026-08-08）

- **正式报告**：`docs/translation-quality-facts-study-report-v1.md`
  （问题→方法→10 轮执行历程→33 槽结果→判据→解读→限制→可复现性，
  含全部身份哈希与重建命令）。
- **campaign 归档**：`.artifacts/i18n/quality/facts-study-campaign-archive.json`
  （archive_id `ee8973e1…`；33 slot 清单与逐项哈希、normalization 总量：
  7 槽传输重试、2 处 id 修复、12 条 finding 丢弃、33 处标点规范化、
  1218 findings；campaign 1–10 失败/成功历史）。
- 结论与决策以报告 §8 为准：**do-not-promote-facts-channel**，
  holdout_clearance=false；DeepSeek 正向信号与 F 臂（facts-as-verifier）
  作为后续研究候选，需另行设计、另行授权。
