# 译文审核操作指南

本指南是译文审核（每批 80 条）与合并修复窗口的**现行操作入口**，整理自第 1–275 批与修复窗口 1–26
的实际运行经验。约束以 [`AGENTS.md`](../AGENTS.md)、[工作流](agent-workflow.md)、
[编排契约](paseo-orchestration-v2-contract.md) 和两份审核契约（
[surface v1](paseo-translation-surface-screen-v1-contract.md)、
[contextual v2](paseo-translation-context-review-v2-contract.md)）为准；本文只写操作顺序、判据与已知陷阱，
不放宽任何契约。脚本参数的权威说明见 [`tools/orchestration/README.md`](../tools/orchestration/README.md)。

旧的累积式 runbook（`docs/baseline-batch-runbook-2026-09-06.md`，§1–§41）与两份旧交接已于 2026-09-24
移除；其中仍生效的裁决已并入本文第六节。需要追溯历史细节时用
`git log --diff-filter=D -- docs/baseline-batch-runbook-2026-09-06.md` 找到删除提交，再 `git show <提交>^:<路径>`。

---

## 一、角色、授权与节奏

| 项 | 现行设定 | 出处 |
| --- | --- | --- |
| 编排者 | 主代理任 ORCHESTRATOR：范围、裁决、验证、提交与推送 | AGENTS.md |
| surface 筛查 | `codex/gpt-6-sol`，thinking `medium`，mode `auto-review`，每批 4 条 lane × 20 条 | 用户 2026-09-23 |
| contextual 复核 | `claude/claude-opus-5-5`，thinking `medium`，mode `auto`，full-000 只复核 surface 标出的条目 | 用户 2026-09-23 |
| 修复 EXECUTOR | `codex/gpt-5.6-sol`，`auto-review`，`medium`；REVIEW 用 gpt-6-sol，FINAL 用 opus-5-5 | 同上 |
| 连续运行 | 审核批次逐批自动推进，不必逐批确认；每批完全收口后 push | 用户 2026-09-19 / 09-23 |
| 修复节奏 | **攒批**：确认的修复先记入积压，累计 ≥20 条再开一个合并修复窗口（取代旧 1:1 交替） | 用户 2026-09-24 |
| 争议条目 | 记 `pending`，登记到 [`evidence/quality/pending-user-review.md`](../evidence/quality/pending-user-review.md)，不修、不阻塞 | 用户 2026-09-23 |
| 暂停 | 用户要求暂停时，让正在写批次状态的命令跑完，不再启动新阶段；记录停点后交回 | — |

**必须停下交回用户**的情形见 AGENTS.md「必须停下并交回用户」；常见的是需要新拟术语或全局改名、
门禁失败且一次诊断无法归因、子 agent 归档状态无法确认。

---

## 二、硬约束（每条都出过事故）

1. **批次进行期间禁止提交**。从 `batch start` 到 evidence 提交之间，任何提交都会让 active batch
   因 base drift 锁死（`production_review_v2_lite_batch.py` 检查 base commit 与 finalize parent）。
   工具维护、文档修改只能放在批次或修复窗口之间；每次提交后都要 `queue rebuild`。
2. **投影内存是硬上限**。一次历史重放约 10 GB、约 245 s（第 275 批实测）；两个投影并发会换页，
   耗时从分钟级变成小时级。同一时刻只跑一个投影命令，长阶段用工具级后台运行（不要 `nohup`，
   否则跑完不通知）。
3. **不要在界面里打开 reviewer 的 agent tab**。打开会把 `attentionReason` 清成 null，
   harvest／reject／archive 三条路都会失败，只能整批 abandon。
4. **reviewer 结束后先记 archive-intent 再归档**，归档后必须回读 `closed` + `archivedAt` 再 confirm。
   一次运行结束的 child 不得发 follow-up 续跑；无效输出按「归档 → fresh retry（attempt=2）」处理。
5. **派发必须显式传 `--mode`**，否则子 agent 卡在权限弹窗。
6. **修复前全仓库 grep**：同一 runtime key 可能横跨 tome／cults／orcs 等 11 个组件，漏改会触发
   `06-runtime-collision-scan`。
7. **自然语言正文不经过 shell 插值**：heredoc 定界符一律加引号（`<<'EOF'`）。
8. **给子 agent 的 prompt 文件不带尾换行**；Paseo 投递时会去掉尾 LF，harvest 会报 prompt mismatch。

---

## 三、环境与宿主脚本

```bash
cd /workspace/tome4-chinese-translation
C=.artifacts/i18n/continuation-20260923        # 宿主工作目录（已 gitignore）
export TOME_PASEO_WORKSPACE=wks_420314270844170b
# 上游源码固定版本：/workspace/t-engine4 @ 624a67329fe2ad440c5b344785a9c73fcf22ae63
```

每批使用一组按批号命名的宿主脚本，从上一批复制后替换批号与 batch id：

| 脚本 | 作用 | 每批怎么来 |
| --- | --- | --- |
| `prepare_reviewN.py` | 建 surface 任务 SPEC/PLAN/SCOPE | 上一批复制，替换批号 |
| `laneN.py precheck <i>` | harvest 前逐位比对 native log 回显的 80 个 identity 与 envelope | 同上 |
| `mkliveN.py` / `mktermN.py` | 由 `get_agent_status` 的观测值构造 live／terminal 捕获 | 同上 |
| `mkarch257.py` | 构造 archived 捕获（通用，不随批号变） | 固定 |
| `audit_native_tools.py` | 从原生日志提取每个 lane 的工具调用，供边界审计 | 固定 |
| `prepare_surfaceN_decisions.py` | **每批手写**：surface ISSUE 的逐条宿主裁决 | 手写 |
| `prepare_contextualN.py` | 构建 contextual draft、SCOPE 与 anchor preflight | 上一批复制 |
| `finalize_hostN.py` | **每批改写**：contextual 裁决、摘要、积压决定 | 由上一批派生后改写 |
| `snapshot_reviewN.py` / `stage_reviewN.py` | 17 门禁、快照重放、证据暂存 | 上一批复制 |
| `close_reviewN.py` | finalize 回执与运行时边界回执 | 上一批复制 |
| `timed_command.py` | 计时包装，产出 `<prefix>.log` 与 `<prefix>-timing.json` | 固定 |

宿主目录已 gitignore，但每批的主要脚本会随证据归档进
`evidence/quality/production-batches/<batch>-host-evidence/orchestration/.artifacts/i18n/continuation-20260923/`。
归档里没有的辅助件（lane／mklive／mkterm／mkarch、harvest 函数、close 脚本与提交说明模板）
已存成 [`review-operations/templates/`](review-operations/templates/README.md)。

**生成新一批脚本**（以 275→276 为例）：

```bash
python3 - <<'EOF'
import re
C='.artifacts/i18n/continuation-20260923'
for n in ['close_review','lane','mklive','mkterm','prepare_contextual','prepare_review','snapshot_review','stage_review']:
    s=open(f'{C}/{n}275.py').read()
    open(f'{C}/{n}276.py','w').write(re.sub(r'(?<![0-9])275(?![0-9])','276',s))
EOF
# batch start 之后再把旧 batch id 换成新 id：
sed -i 's/batch-54d2d16b94c511082107/<新 batch id>/g' $C/*276.py
```

批号替换必须带数字边界：`s/260/261/g` 曾把日期 `20260923` 改成 `20261923`。替换后逐个 diff。

---

## 四、审核批次流程（80 条）

### 4.1 开批与冻结

```bash
python3 -B $C/timed_command.py $C/reviewN-start python3 -B tools/i18n production batch start --limit 80
B=<输出里的 batch_id>
python3 -B tools/orchestration/freeze_workset.py $B        # 必须 matched 80 / missing 0
python3 -B $C/prepare_reviewN.py
python3 $C/timed_command.py $C/reviewN-surface-export python3 -B tools/i18n production batch surface-export
python3 -B tools/orchestration/stage_surface.py $B --out $C/reviewN-surface-plan.json
python3 -B tools/orchestration/dispatch_surface.py $C/reviewN-surface-plan.json $C/reviewN-surface-children.json \
  --emit $C/reviewN-surface-emit.json --select-transport mcp \
  --provider codex/gpt-6-sol --thinking medium --mode auto-review
```

批次关闭后若要紧接开新批，可用 `run_batch_steps.py rollover-chain --limit 80`，
把关闭后的 queue rebuild 与下一批 start 合在一个进程里，只重放一次历史。

`freeze_workset` 出现 MISS 是信号不是故障：常见成因是孤儿目录行、运行时拼接，或上游改串后
locale key 没重新生成（死键）。死键走 batch host-block 放行，不要用全库字面量回退把问题盖住。

### 4.2 surface 四条 lane（并发上限 3）

每条 lane 严格按以下顺序，先建 lane 0–2，任一 lane 收完再建 lane 3：

1. `review_lifecycle.py create-intent <children> "$B|lane-000-<i>" --profiles $C/profiles-live-01.json`
   （上一个 child 未 bind 时会被拒绝）。
2. MCP `create_agent`：title = `lane-000-<i>`，labels = emit 里的 labels **去掉 `paseo.parent-agent-id`**，
   prompt = emit 原文，settings `{"modeId":"auto-review","thinkingOptionId":"medium"}`。
3. 立即 `get_agent_status`，用观测到的 id／sessionId／createdAt／updatedAt／turnStartedAt 运行
   `mkliveN.py`，再 `review_lifecycle.py bind ... --capture <live.json>`。
4. 收到完成通知后先 `get_agent_status`（应为 idle／finished），按模板里的 `h()` 函数执行：
   `mktermN.py` → `laneN.py precheck <i>`（必须 `match True 20 20`）→ `harvest --native-log <codex 会话日志>`
   → `archive-intent`。
5. MCP `archive_agent` → 回读 `closed` 与 `archivedAt` → `mkarch257.py` → `archive-confirm`。

四条 lane 收完后：

```bash
python3 $C/audit_native_tools.py $C/reviewN-surface-children.json .ai/task/$B > $C/reviewN-surface-audit.txt
# 人工逐条看工具调用，写 .ai/task/$B/HOST-SURFACE-BOUNDARY-AUDIT.json
mkdir -p $C/reviewN-surface-raw
python3 -B tools/orchestration/close_review_tasks.py surface $C/reviewN-surface-plan.json $C/reviewN-surface-children.json $C/reviewN-surface-raw
python3 -B tools/orchestration/build_import_index.py surface $C/reviewN-surface-raw $C/reviewN-surface-index.json
python3 $C/timed_command.py $C/reviewN-surface-import python3 -B tools/orchestration/run_batch_steps.py surface-import=$C/reviewN-surface-index.json
python3 -B $C/prepare_surfaceN_decisions.py            # 写 HOST-SURFACE-DECISIONS.json
```

**边界审计要点**：reviewer 只读自己的 envelope 与契约。codex 沙箱初始化失败后用 `require_escalated`
重读同一批授权文件属正常；列工具目录（ALL_TOOLS）无 I/O；`python3 -c` 读自己的 envelope 打印到
stdout 可接受，但必须核实没有写文件。若 reviewer 通过 Paseo `create_terminal` 执行了命令，
要逐条核对发送的按键内容，并用 `list_terminals` 清理遗留终端。

### 4.3 contextual full-000

```bash
python3 -B $C/prepare_contextualN.py                      # anchor preflight 必须 PREFLIGHT_VERIFIED
python3 $C/timed_command.py $C/reviewN-contextual-export python3 -B tools/orchestration/run_batch_steps.py \
  contextual-export=evidence/quality/production-batches/$B-source-workset.json
python3 -B tools/orchestration/stage_contextual.py $B --out $C/reviewN-contextual-plan.json
python3 -B tools/orchestration/dispatch_contextual.py $C/reviewN-contextual-plan.json $C/reviewN-contextual-children.json \
  --emit $C/reviewN-contextual-emit.json --select-transport mcp --provider claude/claude-opus-5-5 --thinking medium --mode auto
python3 -B tools/orchestration/review_lifecycle.py create-intent $C/reviewN-contextual-children.json "$B-contextual-000|full-000" --profiles $C/profiles-live-01.json
```

create_agent 的 settings 是 `{"modeId":"auto","thinkingOptionId":"medium"}`。live 捕获由上一批的
`ctx-live.json` 更新 id、时间戳、sessionId／nativeHandle、candidate_identity 与 task_id 得到；
claude 的 `runtimeInfo.model` 在运行中为 null，终态捕获里补 `runtimeInfo` 并以
`persistence.metadata.model` 核验模型。harvest 使用
`~/.claude/projects/-workspace-tome4-chinese-translation/<sessionId>.jsonl` 作为 native log；
随后写 `NATIVE-TOOLS.json` 与 `HOST-BOUNDARY-AUDIT.json`，按 archive-intent → archive → 回读 → confirm 收口，
再 `close_review_tasks.py contextual` 与 `build_import_index.py contextual`。

`prepare_contextualN.py` 目前断言 phase 为 `surface_collected`，所以 surface-import 与
contextual-export 仍分开跑。契约只要求 anchor preflight 在冻结／哈希之前执行，因此可以把断言
放宽到 `deep_ready`，再把两步合成一次 `run_batch_steps.py surface-import=<idx> contextual-export=<workset>`
（尚未实施，首次采用时要核对 draft 与导出 payload 逐字节一致）。

opus 在 JSON 前多写一句话会被判 invalid：按 `retry_of`、`attempt=2`、新 dispatch_id 重派，
重派时不要再传 `--select-transport`。

### 4.4 裁决、快照与收口

```bash
python3 -B $C/finalize_hostN.py        # 写 HOST-FINAL-DECISIONS、HOST-SUMMARY、REPAIR-BACKLOG-DECISION、reviewN-host-decisions.json
python3 $C/timed_command.py $C/reviewN-adjudication-chain python3 -B tools/orchestration/run_batch_steps.py \
  contextual-adjudication-chain --input $C/reviewN-contextual-index.json --spec $C/reviewN-host-decisions.json \
  --output .artifacts/i18n/adjudication-chain/reviewN-<日期>-attempt01.json --source-root /workspace/t-engine4
python3 -B $C/snapshot_reviewN.py      # 17 门禁 + 两任务快照重放 DONE_VERIFIED
python3 -B $C/stage_reviewN.py         # 暂存证据；只允许本批路径
bash /tmp/closeN.sh                    # evidence commit → finalize → 回执 → handoff → closure commit → queue rebuild → push
```

`closeN.sh` 模板见 `review-operations/templates/`。写 `finalize_hostN.py` 前，摘要里出现的每个技能名、
物品名都要先按 `name=` 或 entity name 行查本库现行译名，不能凭英文自拟；LF 等数字先实测再写。
`stage` 报 `raw_whitespace_exit_code: 2` 且只指向归档的 `reviewN-start.out` 时属已知例外。

---

## 五、合并修复窗口

积压 ≥20 条时开一个窗口，覆盖积压中的全部来源批次（积压台账见 handoff）。

1. `run_repair_steps.py preflight`：每个来源批次一个 `--batch-id` + `--output`（一次最多 3 个，
   超过就分次跑到不同输出），保留各自 workset 与 provenance。preflight 之后若有提交，必须重跑。
2. 建有界 IMPLEMENT 任务（`.ai/task/repair-wNN-<日期>/`）：SPEC 显式列出来源 batch、去重后的 revision
   与获准的同族附属范围；由 `setup_windowNN_task.py` 生成（以上一窗口为模板）。
3. EXECUTOR 派发（prompt 文件不带尾换行）→ harvest → 原生工具审计 → 归档确认。
4. `REVIEW`（gpt-6-sol）→ 宿主裁决；有 confirmed 就进入 `FIX`（同一 cycle 的全部 confirmed 合并成一次
   EXECUTOR 派发）→ `FINAL_REVIEW`（opus-5-5）。v2 的 FINAL 里出现任何 ISSUE（即使宿主判 advisory）都算失败，
   必须回到 `RE_REVIEW`，不能 FINAL→FINAL，否则 DONE 永远不过。
5. 完整门禁（`tools/ci-gates.sh`，17 项含严格构建）→ `VALIDATE` → 译文提交。
6. 在译文提交 HEAD 上：queue rebuild → `authoritative-catalog build` → migration plan/check/apply。
   可用一条命令：
   ```bash
   python3 -B tools/orchestration/run_repair_steps.py publish-chain \
     --candidate-catalog <新目录> --migration-output <json> --timing-output <json> \
     --catalog-recorded-by "repair-wNN ORCHESTRATOR"
   ```
   catalog 产物在 `<目录>/evidence/production-review-v2-lite/catalog/`；migration 不会写进 evidence，要自己复制。
7. PUBLICATION-SCOPE → `make_pack` → publication child → evidence 提交 → queue rebuild → push。
   `make_pack` 之后被打包的文件视为冻结；校验与 commit/push 放在同一条 `&&` 链里。

migration 结果里的 successor 要重新审核，不继承 `done`。

---

## 六、裁决判据

### 6.1 四种处置

- `confirmed`：有固定源码或库内证据的缺陷，进入修复积压。机械性客观事实（占位符、换行结构、
  标点、同一英文句两种不相容译法）单轮即可 confirmed。
- `refuted`：观察不成立（附证据）。
- `advisory`：可改可不改的偏好，不进修复。
- `pending`：需要维护者口径（新拟名、全局改名、跨批策略）或三方讨论全不一致；登记待审阅清单。

surface 与 contextual 的观察分别独立裁决。contextual 判 OK 并不推翻宿主基于客观源码证据的
confirmed；反之 contextual 的 ISSUE 也要宿主自己核验源码后才能采纳。没把握时走三方讨论
（gpt-6-astra / opus-5-5 / grok-4.7，同一份实测底稿并发），按多数；三方全不一致则记 pending。

### 6.2 应判 confirmed 的常见类型

- 删限定词：may／chance／attempts／each／per turn 被删，把不确定说成必然、把持续说成一次（批 275 恶魔空间）。
- 数量或对象写错：「每回合各除一项物理和一项魔法」写成「只能除一项」（批 274 裂解）。
- 触发条件写错：「处在粘液中」写成「经过」、「命中」写成「攻击」（批 274、275）。
- 专名丢核心义或误导机制：Unstoppable Nature→「自然世界」、Reflex Defense→「闪避神经」。
- 换行结构被合并或拆散（诗句、墓志铭；LF 数目要实测）。
- 同一英文句在库内两种不相容译法（任务名 vs 引文）。
- 称谓与物品名不一致（同条前后「王冠／皇冠」混用）。

### 6.3 应判 refuted 的常见类型（反复出现，勿重复报）

- ego 前后缀、冒号标签的尾随空格：中文按本库拼接不保留空格。
- 译文贴合实现、而上游英文与实现矛盾：以实现为准（例：Mercy 匕首「一击必杀」实为按损失生命加伤）。
  判「删了限定词」之前先查守卫变量是否真被读取。
- 本库既定惯例：`blind_immune` 百分比作「致盲／目盲免疫」、`Cunning`=灵巧、同族 keyword 名词化、
  兽人部落「你击败了X部落」同族一致。
- 「这个技能」指代技能本身；对话中对非人生物（如堡垒之影）用「它」。
- 意译专名只要概括机制且同族引用一致即可（「击退射击」）。
- 表层短标签是误报重灾区：判技能名、专名、面板标签之前先查同条 info、同族译法、区域正式名。

### 6.4 持续生效的维护者裁决

| 事项 | 裁决 |
| --- | --- |
| `delving` | 维持「挖掘之」 |
| orcs-lore `herbal infusions` | 维持「草本纹身」 |
| 换行结构统一 | **不按源文镜像统一**全库；但单条换行被合并、拆散、挪位仍属缺陷 |
| 顶层单引号 | 改 `“ ”`；嵌套在 `“ ”` 内的 `‘ ’` 保留；UI 选项名保留 ASCII 引号 |
| 半角括号 | 纯中文内容转全角；混排（拉丁字母／`%s`／`#TAG#`／按键名）记 pending |
| `Arcane Combat` | 「奥术格斗」 |
| 伤害格式 | `%d%%` 是武器伤害百分比，`%0.2f` 是点数；译文中的「武器」是必要区分 |
| `zone` / `level` | 「地图」/「楼层」 |
| 抗性类 `%d` → `%d%%` | 保留百分比，不再报 |
| 速率加成 | 「regen N% over turns」是对回复速率的加成，不是「每回合回复 N%」 |
| The Master | 保持「领主」 |
| Trollmire | 「巨魔沼泽」 |
| yeek | 保持「夺心魔」 |
| Zone-wide | 「区域效果」 |
| Flame（技能名） | 「火焰术」；Shadow Mages 的 Flames 是「暗影之火」 |
| Sun Flare | 「太阳耀斑」 |
| Rimebark | 保持「召唤：雾凇」 |
| 术语库引证 | 只有 `preferred` 有背书力，`existing` 只是语料现状 |

新增或修改高复用术语时先改 `terminology/`，再改 Lua 译文；候选译名要双向查冲突
（候选是否撞别人，以及它是否已被别的英文词占用，例如 crypt→「地窖」撞 cellar）。

---

## 七、常见故障与处置

| 现象 | 成因 | 处置 |
| --- | --- | --- |
| harvest `raw output has leading or trailing bytes` | 抽取的 JSON 带尾换行 | 写盘前 rstrip；改用 `--native-log` |
| harvest invalid，identity 不符 | surface 回显 identity 有错字 | harvest 前用 `laneN.py precheck` 全集逐位比对；救回要清 harvest 锁并删 diagnostics 快照 |
| surface observation 描述的是别条 | observation 挂到了同 lane 更靠前的 revision | 逐条对照自身 source/target；救不回的登记待复查 |
| ISSUE 结果带多余字段 `output_valid=False` | gpt-5.6-sol 旧问题（约 25%） | 整条 lane 重跑 |
| native parser 拒绝新版本 | codex／claude 版本锁 | 修 `review_lifecycle.py` 白名单并补测试；临时可用副本 `--raw` |
| `LIFECYCLE_FAILED: first live metadata ... required` | 上一个 child 尚未 bind 就建下一个 intent | 先 bind 再 create-intent |
| 批次 start 报 queue drift | 工具提交后未 rebuild | `production queue rebuild` 后再 start |
| `contextual-import` 报多余裁决 | contextual-import 漏跑或顺序错 | 用 `contextual-adjudication-chain` 一次跑完 |
| stage TypeError（checkpoint 字段 None） | stage 在 export 之前运行 | 先 export 再 stage，以 result.json 的 started_at 判断顺序 |
| contextual export 撞不可变检查 | 上一批 contextual scratch 未归档 | 由 `close_reviewN.py` 在 finalize 后移入 finalized-runtime-scratch |
| `pkill -f` 后命令静默中止（exit 144） | 模式匹配到了自己的 shell | 先 `pgrep` 拿 PID 再 kill |
| source facts 超过 MAX_LINES | 高频短字面量（如 `" / "`） | 省略 `--source-workset` 是受支持的降级，记录证据不同构 |

判定 child 挂起前必须重新查询 `status`、`attentionReason`、`activeTurn`，并看 `git status` 与
`git diff --stat`；字段陈旧不是挂起证据。

---

## 八、计时与性能

- 每个涉及历史重放的步骤约 245–255 s（第 274/275 批实测），大部分是一次投影。
- 同一进程、同一 HEAD 的相邻步骤共享一次投影：`run_batch_steps.py`（surface-import + contextual-export、
  contextual-adjudication-chain、rollover-chain）与 `run_repair_steps.py`（migration-chain、publish-chain）。
- finalize 与关闭后的 queue rebuild **不在同一 HEAD**（中间有 closure 提交），不能合并。
- 报数字要标明实测还是估算；相减前确认同一量、同一环境、同一尺子。
