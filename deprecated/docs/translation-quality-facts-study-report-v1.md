# ToME4 翻译质量 Facts 因果研究：正式报告 v1

> 状态：最终报告。日期：2026-08-08。
>
> 研究设计：[`translation-quality-facts-study-v1.md`](./translation-quality-facts-study-v1.md)
> 与 [`translation-quality-facts-study-v2.md`](./translation-quality-facts-study-v2.md)；
> 数据构建与执行过程：
> [`translation-quality-offline-closure-plan.md`](./translation-quality-offline-closure-plan.md)；
> 版本化机器契约：[`../i18n/quality/facts-study-v2.json`](../i18n/quality/facts-study-v2.json)。
>
> 本报告基于**真实外部评估**（33 槽全部完成），结论按预注册判据给出，
> 不经由任何内部校准或事后选择。

## 1. 研究问题与预注册假说

**问题**：在翻译质量 AI 评估中，为每条译文额外提供一份
supplemental-only 的"事实包"（游戏机制、规范术语、UI 角色等经核验的
补充信息），能否帮助评估者发现仅凭 source/target 对无法确认的隐藏错误，
而不至于诱发过度解释（在干净条目上误报）？

**预注册设计**（`facts-study-v2` 契约，33 个一次性一-shard 传输槽）：

| 臂 | 内容 | 对照意义 |
|---|---|---|
| A | 最小 baseline（无 checklist、无 Facts） | 最低成本基线 |
| B | 开放实质语义 checklist | 主 baseline |
| C | 裸 Facts（无 checklist） | Facts 独立效应 |
| D | checklist + Facts-first | 组合效应 |
| N | 与 Facts 等形状等字节长的 neutral padding | 位置/形状对照（排除"多一块内容"的干扰） |
| L | Facts-late（翻译块在前、Facts 在后） | 位置效应 |
| F | 独立会话 Facts-only verifier | 复核通道 |
| T | 宿主对 B 与 F 做对称 union（非模型臂） | 两阶段组合 |

**冻结门槛**（Gold 配额）：≥8 fact-addressed claims、≥8 fact-unaddressed
claims、≥5 clean items、≥3 fact traps。**推广判据**（预注册）：
Luna 新增 ≥2 个稳定 true claims 且 precision 降幅 ≤3pp 且 trap 假阳性
每轮增加 ≤1；DeepSeek 方向一致且新增 ≥1 个稳定 fact-addressed claim。

## 2. 方法与数据

- **样本**：20 条（study `fbc99a59f920e061…`，v5 契约配额修订后选择：
  12 fact-dependent + 2 surface + 6 clean/acceptable，5 个 trap 诱饵，
  全部 natural，五文本类型全覆盖）。候选池为 v4 长文本富集池
  （80 条，70/80 ≥300 字符，排除历史 356 个 revision）。
- **Gold**：双独立评审（分片执行 + 宿主确定性 claim id 重编号，已记录）+
  独立 adjudicator；14 addressed + 8 unaddressed + 7 clean + 7 traps；
  全部 lineage 哈希绑定（gold 文件 sha256 `1b90741c…`）。
- **Facts**：80 条候选池由 target-blind 作者产出 208 条事实（147 个
  public-source 文件哈希全部核验通过、61 条 terminology 行号有效）；
  冻结 20 条子集（file sha256 `09b737e0…`）。
- **执行**：并行×4、传输层重试×3（manifest 授权）、单槽超时 5400s、
  缓存关闭、失败不替换。宿主规范化（全部记录于 runner report）：
  revision-id 转录修复（编辑距离 ≤1 唯一匹配）、items 顺序重排、
  标点/空白/CJK 空格规范化、finding 级容错（单条违规 finding 丢弃计数）。

## 3. 执行历程

正式 campaign 之前经历 9 轮失败与契约修订（详见 handoff §14–§15），
失败模式与修复：

| 轮 | 阻断原因 | 修复 |
|---|---|---|
| 1–2 | 自然池配额不足（surface/trap 稀缺） | v5 契约修订（用户授权） |
| 3–4 | 模型 quote 非逐字精确 | prompt 证据精度指令 + B2 标点/空白规范化（用户授权） |
| 5 | 无 Facts 臂引用 fact_id | prompt fact 引用范围指令 |
| 6 | 模型输出被 markdown 围栏包裹 | 围栏剥离（机械修复） |
| 7 | 并行 ledger 竞态 | 读重试+跳过（工程修复） |
| 8 | pi 可执行文件被外部更新（身份漂移） | 重建 prereg 绑定新身份 |
| 9 | Luna 传输层不可靠（无 final text/超时） | 传输层重试契约：超时归入传输层、重试×3、timeout 5400（用户授权） |

**最终 campaign（campaign 10）**：33/33 槽全部通过。

## 4. 最终执行与数据质量

- 槽位：Luna（openai-codex/gpt-5.6-luna）21 + DeepSeek（opencode-go/
  deepseek-v4-flash）12；26 槽单次尝试，7 槽经传输层重试成功
  （attempts 分布：1×26、2×4、3×2、4×1）。
- 宿主规范化总量（1218 findings 中）：revision-id 转录修复 2 处、
  finding 级丢弃 12 条（0.99%）、标点/空白规范化 33 处；全部写入
  runner report 的 `normalization` 字段，外部 lineage 验证逐槽核对。
- 完整性：33 个 runner report、33 个 assessment、33 个 slot ledger
  全部绑定（执行 id 唯一、授权身份一致、哈希逐项匹配）；
  schema/evidence validity 33/33。

## 5. 结果

池化指标（3 个 replicate 汇总；P=precision、R=recall、addrR=fact-addressed
recall、unaddrR=fact-unaddressed recall、trapFP=fact-trap 条目假阳性/轮、
manual=人工队列 finding/轮）：

| 模型 | 臂 | P | R | F1 | addrR | unaddrR | trapFP | manual |
|---|---|---|---|---|---|---|---|---|
| Luna | A | 0.141 | 0.273 | 0.186 | 0.000 | 0.750 | 3.67 | 0.00 |
| Luna | B | 0.097 | 0.197 | 0.130 | 0.000 | 0.542 | 4.67 | 0.33 |
| Luna | C | 0.098 | 0.258 | 0.142 | 0.048 | 0.625 | 5.67 | 0.00 |
| Luna | D | 0.096 | 0.258 | 0.140 | 0.048 | 0.625 | 6.33 | 0.00 |
| Luna | F | 0.000 | 0.000 | — | 0.000 | 0.000 | 5.00 | 0.00 |
| Luna | L | 0.072 | 0.212 | 0.108 | 0.000 | 0.583 | 6.67 | 0.00 |
| Luna | N | 0.135 | 0.273 | 0.181 | 0.000 | 0.750 | 3.33 | 0.00 |
| Luna | T | 0.065 | 0.197 | 0.098 | 0.000 | 0.542 | 9.67 | 0.33 |
| DeepSeek | B | 0.344 | 0.167 | 0.224 | 0.000 | 0.458 | 1.67 | 2.00 |
| DeepSeek | D | 0.163 | 0.197 | 0.178 | 0.071 | 0.417 | 3.67 | 0.00 |
| DeepSeek | F | 0.240 | 0.182 | 0.207 | 0.262 | 0.042 | 3.00 | 3.67 |
| DeepSeek | L | 0.269 | 0.212 | 0.237 | 0.167 | 0.292 | 0.33 | 3.00 |
| DeepSeek | T | 0.272 | 0.333 | 0.299 | 0.262 | 0.458 | 4.67 | 5.67 |

关键 contrast（recall Δ，pooled）：

- Luna：B−A = −0.076；C−A = −0.015；**D−B = +0.061**；N−B = +0.076；
  L−D = −0.045；**T−B：recall +0.000、precision −0.032**。
- DeepSeek：**T−B：recall +0.167、precision −0.072**。

预注册判据：

| 判据 | 结果 |
|---|---|
| Luna 新增 ≥2 个稳定 true claims | **False**（`luna_stable=[]`） |
| Luna T−B precision 降幅 ≤3pp | **False**（−3.2pp） |
| Luna trap 假阳性每轮增加 ≤1 | **False**（4.67→9.67） |
| Luna unaddressed recall 不下降 | True |
| DeepSeek 方向一致（T recall ≥ B） | True（+0.167） |
| DeepSeek 新增 ≥1 个稳定 fact-addressed claim | True（adj-003、adj-010） |
| 结构与证据有效性 | True（33/33） |

**正式决策：`do-not-promote-facts-channel`**（Facts 通道不进入 v4
draft.3；holdout_clearance=false；报告 id `871d8a5d…`）。

## 6. 解读

1. **Luna：Facts 有害**。D−B recall +0.061 的增益被 precision 恶化与
   trap 假阳性翻倍（T 臂 9.67/轮）抵消；稳定层面零新增 true claims。
   N 臂（neutral padding）与 B 几乎一致（recall 0.273 vs 0.273、trapFP
   3.33 vs 4.67），说明 Luna 的退化是 Facts **内容**效应而非"多一块内容"
   的形状效应。
2. **DeepSeek：Facts 方向正确但成本高**。T−B recall +0.167 且 2 个
   稳定 fact-addressed claims（adj-003、adj-010）直接证明了 supplemental
   Facts 能带来仅凭 source/target 无法获得的发现；但 precision −7.2pp
   与 manual queue 5.67/轮说明两阶段并集把大量不确定输出推给了人工。
3. **F 臂信号**：DeepSeek F（facts-only verifier）addrR=0.262 为全表最高，
   而 D（前置 Facts）仅 0.071——支持"Facts 作为独立复核通道优于作为
   前置提示"的假说，是后续研究的优先方向。
4. **语料事实**（数据构建阶段结论）：该语料隐藏错误（术语/机制类，
   需 Facts 确认）远多于表面可见错误；错误集中在长文本与专名术语。

## 7. 限制

- **单样本集**：20 条开发集（Gold 冻结于 v5 契约），结果不能外推至
  其他文本分布；正式 120 条 pilot 与封存集不参与。
- **单轮执行**：33 槽各 1 次（含传输重试但无评估重试）；模型输出
  存在固有噪声，槽间方差未独立估计。
- **宿主规范化**：0.99% 的 finding 被丢弃、33 处证据标点规范化、
  2 处 id 转录修复——全部记录且占比极小，但仍属宿主介入；对照
  N 臂确认形状效应不解释主结果。
- **模型/提供商**：Luna 传输可靠性差（重试 7 槽），thinking 行为
  与 DeepSeek 差异大；结论对模型敏感，不能推广到其他模型。
- **无 holdout clearance**：本研究的任何结果不构成对 v4 或正式样本的
  准入证据。

## 8. 结论

在冻结的 33-slot 预注册框架下，supplemental Facts 通道**未通过推广
门槛**：Luna 上明确有害（无 recall 增益、precision 与 trap 表现恶化），
DeepSeek 上方向正确（recall +0.167、2 个稳定隐藏错误被 Facts 发现）但
误报与人工成本过高。正式决策为不推广；DeepSeek 的正向信号与 F 臂
（facts-as-verifier）模式作为后续研究的优先候选，另行设计、另行授权。

## 9. 可复现性

| 身份 | 值 |
|---|---|
| study_id | `fbc99a59f920e06121ad8417284ac8197250ec40618ace637ec99f29b3916e15` |
| preregistration_id | `72df27596ee181e2d2187e0e36b7a36454467c45ce5f1648a42e97ed26105b6c` |
| execution manifest | `368396407a648f6561fbf936230b21d4e616503b26bfac99599f1df284d30f44` |
| validation_id | `ab0376bbce08cc773349d966f2c20bcab8738a7eba729192bb6ea66244009cb2` |
| report_id | `871d8a5dfa7eb6abfcd4b095af8625ab1f379f921611ab113fdec603adc6fb82` |
| sample.json | `aa3f83fea2490de51d143726…` |
| gold.frozen.json | `1b90741cf45bdc602f9ed28d…` |
| fact-packets.frozen.json (20) | `82d6fde93238a87fac8feb6e…` |
| fact-packets.frozen-v3.json (80) | `09b737e07b601b8faf9cb7d0…` |
| neutral-packets.json | `d412cf733b2b6036e219a499…` |

关键 artifact 原始逻辑目录（均位于工作期 `.artifacts/i18n/quality/runs/`）：

- 输入与选择：`20260807T111704.162347Z-facts-study-curation-build`、
  `20260807T124345.706087Z-facts-study-curation-select`
- bundles/prereg/manifest：`20260808T124932.424887Z-facts-study-curation-bundles`
- 33 槽执行：`20260808T1249…`–`20260808T17…` 各 `pi-facts-study-<slot>/`
- 外部验证：`20260808T175411.301395Z-facts-study-curation-external`
- 官方报告：`20260808T175419.274533Z-facts-study-curation-report`

不可重建证据另存于项目外 A-core 归档
`tome4-chinese-translation-archive-20260808`。归档索引身份为
`ee8973e1743c15b44af0f8893fe5d47a89806c8a085caa1c2fb629ef805855fa`，索引文件
SHA-256 为 `07a82cb3359ea2e7b9aabb1ec52829e8aa3a53a5a361b149bc9426b08558c851`，
顶层 manifest SHA-256 为
`cda00693799563205d6a0edf1241309553d6ae058c301323e003b0c51f28adaa`。A-core
保留 10 项冻结输入、33 份 assessment、33 份 runner report、campaign ledger、角色
审计记录和 Git bundle；逐项哈希均已核验。它不包含 provider 原始事件流，不进入本
源码仓库。

重建命令（全部确定性）：

```bash
python3 -B tools/i18n quality facts-study-validate --pool <pool> --sample <sample> \
  --facts-pool <facts80> --facts <facts20> --neutral <neutral> --gold <gold> \
  --preregistration <prereg> --execution-manifest <manifest> \
  --bundle <bundle-{a,b,c,d,n,l,f}.json> \
  --assessment <33×assessment.json> --run-report <33×runner-report.json>
python3 -B tools/i18n quality facts-study-report --validation <validation-index.json>
```

## 10. 参考

- `translation-quality-facts-study-v1.md` / `v2.md`：数据契约与修订
- `translation-quality-offline-closure-plan.md`：离线闭环与执行方案
- `i18n/quality/facts-study-v2.json` 与本报告 §9：冻结协议、长期归档身份和重建入口
