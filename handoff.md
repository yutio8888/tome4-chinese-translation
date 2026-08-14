# Handoff — 本地化基础设施契约（contract/0.1）工作交接

> 交接时间：2026-08-13
> 交接范围：`tome4-chinese-translation` 仓库的本地化基础设施契约推进、强身份槽位
> 迁移、以及最新外部评审暴露的消费链缺口。
> 状态：`develop` @ `82a1985`（已推送 origin/develop），工作树干净。

---

## 一、当前状态速览

- **HEAD**：`82a1985 docs(i18n): record external-review advisories and PR-pending scope`
- **远端**：`origin/develop` == `82a1985`；`origin/master` == `f6b23ed`（未合并、未开 PR）
- **发布仓库** `/home/yun/projects/tome-chn-mod`：本地 `eb6f142`（addon 0.2.6），**未推送**
- **工作树**：干净（所有成果已提交并推送）

### 本轮已完成并推送的提交链（`91cb462..82a1985`）

| 提交 | 内容 |
|---|---|
| `cd42f9a` | contract 0.1 Pilot A 验收 + talent.info 槽位 + L2 rename 修复 + ci-gates 接线 + cli.py 可移植 |
| `dc74ee2` / `a2f5b2b` / `19b8790` | talent.info 基线重冻 + 迁移记录 + 度量/回滚文档修正 |
| `1cff3d6` / `c192bb2` / `d72f1c8` | effect.desc 槽位 + 基线重冻 + 迁移记录 + per-occurrence 测试强化 |
| `9fbd9cd` | TERMINOLOGY.md 计数刷新 + release-plan.md 状态 |
| `82a1985` | 外部评审 advisory 归档（A2/A3 + PR 待办范围 + table.merge 假设声明） |

---

## 二、已达成（身份底座）

- **契约 §4.6 四个强身份槽位全部落地**：`talent.name`、`talent.info`、`effect.desc`、`entity.name`。
- **冻结公式**（§4.5 身份哈希 / §6.1 指纹 / §7.1 baseline 格式）零改动，字节级稳定。
- **原位重分类机制**：`talent.info` / `effect.desc` 通过 Lua 补丁「每处恰好一次」重分类，
  locales 写入与 source_tag 逐字节不变，tDef 数 / source_snapshot_sha256 / i18n_list.lua
  字节不变，无 strong+fallback 双映射。
- **覆盖矩阵实证**：talent.info 1836 strong；effect.desc 805 strong + 21 组共享 desc 一对多 TU。
- **门禁**：781 工具链/契约测试全绿、ci-gates 12/12、严格 lint、扫描、审计、addon 完整构建全过。
- **基线重冻**：3 代（29da216 / cd42f9a / 1cff3d6）各 8 组件 × 2 文件，均 0 finding，迁移记录
  完整（registry sha 对照、覆盖矩阵、三档回滚、PR 待办）。

---

## 三、最新外部评审结论（**关键，交接重点**）

上一轮外部只读评审（本地主代理 + 生产运行证据）判定：**「身份底座成功，端到端质量门
尚未成功」**。G1–G12 的 Gate 测试证明了公式稳定性和 happy path，但未覆盖真实变更类型
下的消费链。**不建议据此进入 Phase 2 或合并相关 PR**（这正是契约 §15 规则 6 预警的
「Phase 2 前吸收 Pilot A 实测教训」场景）。

经本会话独立逐条核验，4 个 High 属实、1 个 Medium 重分类：

| # | 级别 | 问题 | 证据（file:line） | 核验 |
|---|---|---|---|---|
| 1 | High | duplicate-id 规则未进 Baseline/CI：`read_index_files` 硬编码 `conflicts=()`，提取期算出的实体冲突（T_IRON_WILL / T_TWILIT_ECHOES，见 `.artifacts/i18n/identity/current/*/identity.json`）不进入 finding 管线 → 8 基线空、report 报 0 ERROR。且冲突来自未加载遗留文件，直接恢复传递会误报 | `tools/i18nlib/identity.py:839`、`pipeline.py:149` | ✅ 属实 |
| 2 | High | source 增量漏新 TU：affected_tus 仅从 base 索引收集，recomputed 只保留旧 UID → 新增实体/新 UID/部分改名静默漏报；删除文件在 try 之外读 head 已删 blob；G8 只测 UID 不变的数值修改 | `tools/i18nlib/incremental.py:288,318,364`、`tests/i18n/incremental/test_incremental.py:305` | ✅ 属实 |
| 3 | High | source `--ci` 把全量 ERROR 当 new ERROR（未与 base fingerprints 求差），有合法 legacy 债务时误失败 | `tools/i18nlib/cli.py:1440` | ✅ 属实 |
| 4 | High | translation 域漏 head-only 新条目、不读 base copy fragment；rule 域只比较 rule_id 集合，同 rule 的 schema_version/severity/evidence 变化被判「无规则变化」 | `tools/i18nlib/cli.py:1495,1725` | ✅ 属实 |
| 5 | ~~Medium~~ | L1 不携带旧译文（previous_definition=None → merge 丢弃） | `identity.py:1197`、`merge.py:192` | ⚠️ **重分类**：契约 §5 明写 L1「不产 migration candidate」，实现与契约一致；属设计级观察，非实现缺陷 |

---

## 四、建议的下一步（infra-contract-004，待用户授权）

修复 4 个 High + 补测试 + 重新做消费链验收。范围建议：

1. **duplicate-id 透传**：`read_index_files` 真实透传 conflicts 进 finding 管线；先摸清
   T_IRON_WILL / T_TWILIT_ECHOES 的真实加载语义，处理「未加载遗留文件」误报边界
   （不能简单恢复传递）。
2. **source 增量**：补 add/delete/rename/new-UID 处理 + 删除文件的异常保护；
   补 G8 之外的真实变更类型测试。
3. **source `--ci`**：改为与 base fingerprints 求差，legacy ERROR 只作技术债报告。
4. **translation/rule 域**：补 head-only 新条目、base copy fragment、rule
   schema/severity/evidence 语义变化检测。
5. **补测试**：add/delete/rename/new-UID、head-only translation、copy fragment、
   rule schema bump、真实 duplicate-id reachability（含误报率）。
6. **重新验收**：更新 gates-report 与契约状态，明确「身份底座已验收、消费链修复后
   再验收」。

---

## 五、未决的用户决策

1. **addon 0.2.6 发布**：暂缓（用户明确）。发布仓库 `eb6f142` 停在本地。
2. **master PR 合并**：暂缓（0.1 正式生效需 PR 合并，与发布一起做）。
3. **infra-contract-004（消费链修复）**：**待用户授权**（本 handoff 交接时尚未启动）。
4. **effect.desc 之后是否继续其他槽位**：已无契约示例槽位缺口（四槽位齐）。

---

## 六、关键协议/工作流要点（供后续会话）

- **多代理编排协议**：大型任务用 Paseo 三角色（ORCHESTRATOR=本会话主代理、
  EXECUTOR=`paseo run --provider pi --model opencode-go/deepseek-v4-flash --thinking max`、
  REVIEWER=`paseo run --provider codex/gpt-5.6-sol` auto-review 只读）。
  - 状态机事实源：`.ai/task/STATE.json`（用 `python3 -B tools/ai_state_check.py .ai/task/STATE.json` 校验转移合法性）。
  - **commit 是 ORCHESTRATOR 宿主检查点**（EXECUTOR 不 commit/stage）；大型任务用「两阶段提交」（实现提交 → 基线重冻 → 交付提交），复审收敛后 commit、避免先 commit 再改。
  - 外发检查点：plan-reviewer / EXECUTOR / REVIEWER briefing 发送前记录 provider/model/内容类型/量级。
- **门禁**：`python3 -B tools/i18n doctor` → `lint --strict` → `unittest discover -s tests/i18n -q` → `scan_runtime_collisions` → `classify_runtime_keys` → 术语审计（audit_static/dynamic/annotate_domains）→ `git diff --check`；完整集成用 `tools/ci-gates.sh`。
- **基线重冻**：`python3 -B tools/i18n baseline freeze --commit <实现SHA>`（需导出 `TOME_DLC_*_ROOT=/home/yun/projects/tome4-dlcs/...`）；旧代文件「冻结后不修改」，迁移记录标注 superseded。
- **测试口径陷阱**：`unittest` 传裸包路径（如 `tests/i18n/fingerprint`）会加载 0 个测试或 import 报错；必须用 `tests.i18n.<pkg>.<module>` 模块路径或 `discover -s`。
- **A2/A3 advisory**（已归档入契约 §15）：A2=legacy validate pin 失败 exit 2；A3=§8 I1 实现为 component 级加宽（契约要求 section 级）。

---

## 七、运行期 artifact 状态

- `.ai/task/STATE.json`：当前为 `infra-contract-003`，终态 `DONE`（step=15）。
- `.ai/reviews/`：infra-contract-001/002/003 各轮 review JSON 均已落盘（R1/R2/R3/FR/final）。
- `.ai/task/SPEC.md` / `PLAN.md`：当前为 infra-contract-003 内容（plan_rev 1）。
- EXECUTOR/REVIEWER agent 已 `paseo archive`。
- 门禁日志与验收报告：`.artifacts/i18n/{contract-pilot-a,contract-pilot-a-g10,contract-pilot-a-effect-desc}/`（忽略目录）。

---

## 八、启动 infra-contract-004 时需先读

1. `docs/localization-infra-contract-v0.1.md`（契约全文，尤其 §4.3/§5/§7/§8/§13/§15）。
2. 本 handoff 第三节的 4 个 High 证据链。
3. `.artifacts/i18n/identity/current/*/identity.json`（duplicate-id 冲突原始证据）。
4. `tools/i18nlib/{identity,incremental,merge,pipeline}.py` + `tools/i18nlib/cli.py` 的
   增量/CI 分支。
