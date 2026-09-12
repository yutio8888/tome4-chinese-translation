# 审核效率有界优化：review-efficiency-20260912

本轮集中修复 EFF-1/2 的生命周期、CLI 创建兼容和观测边界；EFF-3..6 只做源码核验与后续设计。
基线 `fb09a21d71169de3553b7074b5fb202e389acc89`。不恢复翻译，不修第89批的5条待修项，
不修改 catalog／queue／checkpoint，不运行全历史投影，不应用旧6a。
本报告不是最终门禁、独立复审或任务 DONE 声明。

## 核验口径

第89批 TIMING 记录 reservation `02:19:39Z` 至 finalize `03:03:00.881926Z`，
墙钟 **2601.881926 秒（43分22秒）**；包括源码核验、派发、模型、失败重试、编排、
门禁和提交，不包括之前的性能提交与队列恢复。
运行记录只读参考 `.ai/task/batch-0ea72199906baf238871/` 及其 `-contextual-000` task，
未改写它们，也未读取 `.ai/consult/`。

| 项目 | 证据与结论 | 当前状态 |
|---|---|---|
| EFF-1 收获／归档／重派 | 首轮语境终态 `02:38:29.445` 至新 attempt 创建 `02:47:27.472`，538.027 秒。这是整段主代理处理与工具往返，不能归为 archive API 耗时 | confirmed；MCP 捕获路径已实现，实际省时未实测 |
| EFF-2 派发准备 | surface 各 child 62.217／73.893／79.357／72.574 秒；首次创建至全部结束247.192秒。各模型时段重叠，不能相加作墙钟 | confirmed；整 stage 预检和完整 lane labels 已实现 |
| EFF-3 输入事实不足 | 无效 full-000 313.541秒；有效 fresh full-001 210.475秒；首次创建至重试创建851.568秒，已包含上面的538.027秒 | confirmed 输入不足；设计已写，收益 pending |
| EFF-4 发布历史 | 旧固定 HEAD 的测量2708次 git log；发布相关函数 inclusive 38.273秒与1.696秒。当前三函数逐字未变 | confirmed 热点；设计已写，新版本收益未实测 |
| EFF-5 catalog | 旧 profile：84次完整验证 inclusive81.222秒；其中 JSONL解析约38.985秒，不能重复相加 | pending；必须在 PERF-1 后重新测量 |
| EFF-6 门禁 | 受跟踪 gates.json 的17项完整检查共88.790秒，占批次3.41%；production-shadow42.300秒、toolchain24.988秒、严格build1.158秒 | advisory；保持全部门禁 |

## EFF-1/2 实现

入口为 [review_lifecycle.py](../tools/orchestration/review_lifecycle.py)，接入
[两个派发 helper 与操作流程](../tools/orchestration/README.md)。journal 是单 ORCHESTRATOR
写入的派生操作记录；每次 save 先写 journal，再镜像已有 task STATE。外部 archive 调用前
两个持久化步骤都必须成功；中断后从 journal 重建同一 STATE 镜像，不能删旧 child。
原子写改为二进制写入、文件 fsync、rename、父目录 fsync。

- 所有独立 lane 的 envelope／candidate／input SHA／manifest／prompt 先一起验证，
  然后输出 prepared 创建参数。没有创建的 lane 可继续准备；create-intent 后的歧义
  不可盲目重派。group identity 与 index 同时进入创建 labels、journal 与 STATE。
- 每次 create-intent 保存该次 profiles 原始响应摘要和文件。实时查询、notes判断和运行时
  选择仍由 ORCHESTRATOR 在每个真实 create 前完成；捕获文件不自行证明查询的新鲜度。
- 首个完整 MCP live capture 核验直接 parent label、workspace、cwd、task、role、purpose、
  dispatch、candidate、lane；绑定输入 SHA。观测不做 profile 推断或字段回填，
  null／missing 分开保存，幂等绑定不覆盖第一次 runtime observation。
- 原始 terminal bytes 先不可变留档，再调用现有 strict validator；前后文字、Markdown、
  换行、错误 identity／顺序／覆盖／shape 均拒绝。另有证据型 reject，供 ORCHESTRATOR
  记录已通过 JSON 但违反只读／冻结读取边界的输出；不改原始 raw。
- 只处理收到通知且有 activeTurn／attention 终态事实的 child。无通知、不完整查询、
  歧义创建、归档回读不明确均拒绝推进；有绑定 dispatch 的 host 零匹配审计入口，无 sleep、轮询、stop／cancel。
- 归档预算先持久化，最多2次；返回码不是确认。中断恢复先回读，确认 closed/archivedAt
  后才解锁后继。预算耗尽保持 WAIT_USER/archive_pending，可用只读回读恢复。
  输出获取失败留 terminal_fetch_errors 历史，保持可恢复，不判废或归档；明确放弃需要具体原因与证据。
  raw 的 pending 验证可从保存字节恢复，completed/rejected 不重验。wait.resume_state 保留首次恢复阶段。
- full retry 保留 candidate 与 input bytes；contextual 还保持 exact input_path。
  新 attempt、dispatch、agent 不覆盖失败历史。surface 四 lane 只能整组重试和接受。
- close 先检查原 workspace 普通文件与路径，保留复制的 symlink 语义，再在临时 workspace 用真实 `ai_state_check.check_state` 验证 prospective 完整状态；
  通过才写接受记录，STATE 作为最后原子发布指针。没有替换生产 import 或 evidence 消费者。
- `Journal.timed` 可包裹外部工具调用；fake transport 组合入口自动记录工具调用与收获／归档。
  模型窗口来自实际 snapshot 的起止字段；缺端点时不猜。并行时段按类别取区间并集，
  不把不同类别再次相加。手工 MCP 调用须显式使用计时接口，才能测得其 tool_call 分项。

扫描只遍历显式有限 plan、journal、stage、task artifacts；surface 受现有1..80条规则约束。
归档每次入口最多消耗一次预算，不含无限重试。定向测试同时作为短超时终止探针。
测试只涉及 fake transport、临时文件和现有临时 Git fixture，没有真实 agent 操作或生产队列访问。

### cycle-1 修复与来源限制

| 裁决 | 本轮实现与有判别力的 fixture |
|---|---|
| FIX-1 | 原路径普通文件检查、复制保留 symlink；原 envelope/已存在发布 raw 为 symlink 均拒绝且不发布 DONE |
| FIX-2 | pending/completed/rejected 与传输失败分开；验证前中断重载后只读保存 raw；完成判废不重验；显式放弃不可重新接受 |
| FIX-3 | 原始 list_agents request/response 与完整身份捕获留档；严格小于 limit 才可证明未截断；过滤/历史排除后零匹配允许一次创建重试；计划成员不伪装 child；partial stage 不发布 |
| FIX-4 | 全部 capture/终态验证后一次更新 row；同 Journal 无效→有效绑定测试验证首次有效事实 |
| FIX-5 | 无 --emit 位置参数入口恢复 CLI 创建，新增 host 实时 --profiles 参数；fake CLI 实际 subprocess 返回 ID→created→完整 live 接通；下一 child 等待绑定；save 校验实际创建传输 |
| FIX-6 | cycle-2 用已核验版本的 native-export/harvest 替换 SDK 诊断支线；两份授权真实来源纯解析 SHA 一致，严格消费者使用合成 fixture 验证 |
| FIX-7 | wait.resume_state 持久化首次阶段，重复 save 不覆盖，归档确认后恢复；同次 save 编辑顺手跳过 DONE/STOP 字节重写（CR-4 advisory） |

CLI 0.7.2 `commands/agent/run.js` 的 addRunOptions/toRunResult 与 background 分支仍可创建，
输出 agentId。inspect/ls 显示字段缺失不影响创建能力，但不能用于完整身份绑定；CLI 创建后的
MCP capture 单独记为 live_observation_source，不改 task 的 cli。任务首个准备前可显式选择
mcp，存在 journal 准备或 child 历史时禁止切换。host 每个 create 前实时 profiles 仍为必要输入。

`reconcile-absent` 消费 host 的有界审计，不发明新的远端协议。已安装 MCP list_agents 源码
先含 archived 过滤，再按 limit 截断，响应无分页 cursor。故只接受 includeArchived、cwd、
覆盖意图时间的 sinceHours、明确 limit 且返回数量严格小于 limit 的完整查询；保留原始
structuredContent 与每个列表 ID 的完整身份捕获，核对二者 ID/cwd/labels 一致再排除历史、
过滤 workspace/parent/task/role/purpose/candidate/dispatch/lane。host 的完整性核验仍不可省略。

### cycle-2 原生终稿来源：已核验版本的有界收口

父代理的新证据提供了更小的来源：原生会话日志早于 Paseo 显示层加工。Python 标准库入口
`native-export` 与 `harvest --native-log` 只读明确路径，先校验通知、已登记 direct child、
完整终态、首次 provider/session、冻结 prompt 和输入绑定，再解析完整、稳定的普通文件。
生命周期仍使用原 CLI/MCP；不连 SDK、不操作 daemon、不安装依赖、不搜索其他会话。

| 实际只读来源 | final 边界 | 纯解析结果 |
|---|---|---|
| Codex 0.153.0 | session_meta 与终态 persistence 对应；创建 prompt 相等；第276行唯一 final_answer 的 output_text 与第279行同 turn_id 的 task_complete.last_agent_message 相等 | 873 bytes，SHA256 `2dd584de5a923a308865c6f59b0af7c6f55a1e9aafde733161b224c3ec4eb384` |
| Claude Code 2.1.259 | session/cwd/prompt 对应；第281行 end_turn text 由第282行 last-prompt.leafUuid 指向，父链完整；第280行 thinking 不进入结果 | 13575 bytes，SHA256 `7f1de819855d833b260a9109941e7666c3dfe8268bf54ec39312d178293729c7` |

真实文件 SHA 与父代理 proof 一致；纯解析产物仅在本 dispatch ignored 目录，未改历史
STATE/raw。两份文本是本任务实现/代码复审报告，**没有作为 translation strict 结果提交**；
它们证明真实来源提取，合成 fixture 与真实既有消费者另行证明导出到 strict/归档/发布的接线。
Codex 样本 curated 恰好额外含 `---\n\n`；Claude 样本 curated 恰与 native 相等。这些都是
样本事实，代码不按此前缀删文本，也不据此认定 curated 普遍无损。

解析拒绝未知 provider/版本、未知结构、多轮用户输入、错 session/cwd/prompt、断裂 UUID/turn、
多义 final、截断/重复键及读取中变化。最多16MiB/10000行，线性有限扫描；Claude 父指针严格向前，
遍历最多节点数。Codex 保留已核验的三块环境 bootstrap 边界，不能把它与新的用户轮次混淆。
raw 是 final 字符串直接 UTF-8 编码，包括首尾空白；首尾空白仍由原 strict validator 拒绝。
只存 raw 与精简 provenance，不存完整会话、初始 prompt 或 thinking。

来源失败留独立诊断而非判废结果，可修正路径/捕获后重试，不自动归档；已判废与人工 reject
保持不可重新接受。生产入口限首次通知后的归档前窗口；历史审核仅可用纯解析接口。
未知版本、无法定位日志、缺失首次 provider 或冻结 prompt SHA 的旧 journal 仍会拒绝，
需要独立证据处理，不自动升级/猜测/修复历史。最终候选状态仍以 STATE 为准。

### 保留的 SDK 来源限制（不再代表全部来源阻塞）

cycle-1 已核验安装包0.7.2的公开 API：refresh/current/timeline.refetch 提供 snapshot 和
canonical/projected timeline，未提供 provider-original final phase 与完整边界来源保证。
Codex provider 的 `ASSISTANT_MESSAGE_BOUNDARY_MARKDOWN` 可在 delta 前注入分隔符，
threadItemToTimeline 不传 final phase；公开 PaseoClient 根也没有 daemonVersion 接口。
安装版本不能证明运行中 daemon 版本，MCP activity/finish 的 trim/截断不能逆转。
这些限制仍成立，但已核验的原生日志提供独立观察来源，不需要从 SDK 反推。

本轮删除始终 UNPROVEN 的 SDK 导出支线与4项专属测试，关键空白/截断/歧义/身份拒绝覆盖
迁移到 native fixture；既有40项生命周期测试保留。没有 Node/网络/SDK 依赖，未声明任意
provider/版本均支持，也未测量或承诺生产节省秒数。

## EFF-3：producer 冻结事实包（仅设计）

已核对 `production_review_v2_lite_batch._contextual_payload`：七键 payload 包含文本快照、
固定来源 identity、术语、bounded_context 与通用 briefing；当前 `_contextual_bound_context`
没有绑定实际逐条源码证据包。`build_evidence_pack.py` 已能生成不含 finding 的事实包，
但按 pinned/unpinned 选择本地根并读取文件，不在读取时重验固定 commit/blob；
`matching_literal_lines` 空时不生成片段。不能直接把它接到 producer 后就宣称证据完整。

第89批受跟踪 [source-workset](../evidence/quality/production-batches/batch-0ea72199906baf238871-source-workset.json)
有80条，79 pinned、1实际来自 Cults 的 unpinned 条目。该条目录归属与实际 DLC 组件不同，
目录 source 多两处段首 ASCII 空格；记录明示是归属核验，不是 byte-exact runtime-key match。
后续输入至少要分别表达 catalog/runtime 归属、实际公开组件、源码路径、固定 commit（若有）、
实际文件 SHA、decoded literal 和两处差异，不能用 normalization 隐藏差异。

建议下一有界任务在 **producer 冻结 envelope 前**构造无结论事实包，并将包路径与 exact SHA
写进每条 bounded_context 或 inline 内容（保持七键契约）。包必须先受跟踪或具备同等明确
冻结步骤，引用路径要让 reviewer 权限明确；校验引用 bytes 和 key 覆盖，再计算 candidate。
包变化产生新 candidate，不能事后修改同一 candidate 输入来挽救失败 full-000。
验证重点：跨组件 DLC、未固定来源披露、固定commit与工作树漂移、动态宿主键、空 literal lines、
byte差异、不含先前 finding、失效 hash 拒绝派发。收益须在授权的新批次分项测量。

## EFF-4：发布历史查询（仅设计，未应用6a）

通过 AST 提取函数原文与固定旧 HEAD `d95ee7f2eda7ca3ecd2822defe40112645888c30`
对比，`_candidate_commits`、`_publication_commit`、`_migration_publication_commit`
三处函数逐字相同。前者逐路径 `git log --full-history --diff-filter=AM`；后两者要求当前
blob/mode/type 与候选提交一致，单 parent 恰为 base，且唯一匹配。

旧6a参考 diff 和文档仍存在；本次未应用或运行。旧交接记录的135.4→97.8秒只是历史单样本，
且不能把其中约200次函数级调用与另一次profile的2708个git log混为同一计数。
历史已发现 directory→file 与 pathspec-before-rename 问题：递归 ls-tree 的叶子缺项
不等于原路径不存在，`p/old.json → p` 的 rename 分类可使快慢路结论不同。

下一任务先冻结快慢路等价条件，再考虑按 base 的唯一直接 child 做局部证明；
证据树、父关系、当前bytes、AM路径变更分类和唯一性都满足才走快路，无法证明时回到原扫描。
限定缓存生命周期为 root/固定commit 的一次投影；不新增持久“发布已验证”信任缓存。
fixture差分须涵盖：增加/修改/删除/重加、目录与文件互换、rename/copy及pathspec边界、
merge/多child、类型或mode变化、当前相同blob重复发布、shallow/replace/graft、非ASCII路径。
先有限Git fixture再申请固定HEAD串行基准；必须比较实际队列八字段/完整progress与异常拒绝行为。
本次无全历史性能实验，不报新速度收益。

## EFF-5：catalog 解析／验证（仅设计）

旧 [性能说明](projection-performance-20260911.md) 和派生 measurement.json 的81.222秒
包含约38.985秒 JSONL解析。PERF-1 后 `_catalog_view` 已复用 exact catalog OID组合的完整
验证结果，并在入口重验候选路径/普通文件元数据；`_validated_catalog` 完整验证后才行共享。
`validate_catalog_files` 仍验证五文件集合、policy/schema/rules、manifest、逐行shape与identity，
再产出 verified rows。新缓存不能绕过这些检查，也不能只以 revision identity 复用整个行。

先在当前固定HEAD用分项计时测解析、canonical/hash、逐行校验、共享与cache命中，记录inclusive
关系与峰值内存，再决定是否优化重复纯计算。候选方案仅限单次投影、exact bytes/context键，
失败不缓存、退出释放；每个catalog仍验证全量顺序、重复项、风险、args_order与跨行不变量。
旧缓存可能已经消除了部分重工，未复测前不承诺收益、不以旧 profile 推导额外81秒。

## EFF-6：门禁优先级（advisory）

第89批受跟踪 [gates.json](../evidence/production-review-v2-lite/batches/batch-0ea72199906baf238871/gates.json)
给出真实17项时间；88.790秒已包含在 adjudicate/prepare 的240.047秒里，不再相加。
优先优化编排间隔、失败重试输入和发布历史；不删门禁、不降低strict，不并发重型重放。
历史tree解码exclusive约0.861秒同属低优先级，暂不新增缓存层。

## 验证与 AC 状态

本轮精确命令、退出码与计数见任务派生目录
`native-final-01/validation-results.json` 和 `DELIVERY.md`；实际来源结果见
`native-final-01/real-source-results.json`。旧 cycle-1 的44项与206项结果保留为历史记录，
不能替代本候选验证。最终候选聚焦52项/3.705秒、既有契约/状态206项/2.030秒，均退出0；registry、契约检查、
两份真实来源纯解析均退出0。这里的测试时间是 fixture 耗时，不是生产提速测量。

```bash
timeout -k 10s 180s python3 -B -m unittest tests.i18n.test_review_lifecycle
python3 -B tools/test_groups.py --check
python3 -B tools/paseo_contract_check.py
timeout -k 10s 300s python3 -B .artifacts/i18n/review-efficiency-20260912/native-final-01/run_contract_tests.py
git diff --check
```

新 launcher 将既有测试临时目录限制到本 dispatch，不替换业务函数、validator 或旧断言；
模块仍为 `test_ai_state_check`（load_tests 含 contextual result/manifest）、
`test_contextual_anchor_preflight`、`test_surface_screen_manifest`、`test_surface_screen_result_check`。
全部 changed（含3个未跟踪新增文件）另行做 no-index 空白检查，不改 index。

AC-1：上述两个真实来源完成 exact extraction，合成 fixture 验证 strict 不掩盖空白/Markdown、
身份/次序/条数问题；生产 agent 收获未运行。AC-9：README 给出 session 定位、明确原生日志
路径、导出/strict harvest、可恢复错误和归档顺序。AC-2/3/4/5/6/7/8 保留既有修复与消费者
覆盖；AC-10 的详细交付由 DELIVERY 记录。EFF-3..6 未增加本轮实现，省时仍未实测。
最终全量门禁、完整独立复审、冻结、提交和状态闭合由父代理负责；此文不声明任务 DONE。
