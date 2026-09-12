# P1 审核周转与归档前终稿实现

任务 `review-speed-p1-20260912`，初始 dispatch `execute-astra-01`，cycle1 修复 `fix-astra-01`；基线
`6c0c4d42d6860f721db117ed9eed5b3743280958`。本候选实现 P1-B1/B2 与收窄的 P1-A，
最终任务状态以 `.ai/task/review-speed-p1-20260912/STATE.json` 为准。翻译目前仍暂停；按
`RESUME-TRANSLATION-AUTHORIZATION.json`，报告各项优化完成验收与提交后自动恢复第 92 批。

实现集中于既有 `review_lifecycle.py`：可选 null session 别名不参与比较；Claude 2.1.259
在独立成功自然终态核验后支持无末尾 last-prompt 的精确导出；共享 harvest 拒绝错误终态；
完整 MCP 返回通过 stdin 保存、核验并调用原 Journal/native/strict 方法。
[README 的宿主配方](../tools/orchestration/README.md#mcp-宿主-stdin-配方p1)负责异步 MCP 顺序，
没有新调度服务、数据库、SDK 或生产 Node 依赖。

## 初始候选验收证据（execute-astra-01）

| AC | 本次结果与可复现证据 |
|---|---|
| 1：null 别名 | `test_p1_null_alias_pair_and_invalid_known_values` 覆盖真实位置的脱敏 first/terminal、全部未知首次值、非法已知值及不改写 capture/observation；原 first-terminal 漂移与 required session 测试保留。真实 batch91 首次 capture 在基线报 `invalid session alias`，新实现与 terminal 得到同一 session。 |
| 2：精确 native 导出 | 新 natural tail、历史中间元数据与 CLI 测试覆盖无末尾尾标、真实尾标形态、尾标后单 ai-title、完整 source hash、原样空白、唯一链与终态前置条件。固定字节前缀与真实后续尾标均通过纯 parser，raw SHA 相同；没有裁尾后冒称整个原文件，也没有补写 last-prompt。 |
| 3：错误与恢复 | 新 CLI 测试拒绝 error/error、idle/error、error/finished 的 `--raw`，验证归档前预算为 0、冻结 raw/proof 可在源文件消失后复用、冲突终态不能归档。旧 explicit reject、pending 重验、稳定文件变化、判废不复活和两次归档预算测试全部通过。 |
| 4：真实 MCP/宿主边界 | `replay_real_inputs.py` 对 SOURCE-INPUTS 全部哈希及 5 份完整外壳做只读核验；额外只读 list_profiles 返回保存在 `profiles-wire.json`，接口声明在 `tool-definitions.json`。create/profiles 文本中的计数/ID 前缀与其后 JSON 分别校验，payload 与 structuredContent 按 JSON 类型和内容一致才接受；未知形态、重复键、多文本块、冲突及 isError 拒绝。README 原代码经 shell/stdin 到真实 Python helper 执行，核验完整 settings 映射及每次 profiles→intent→create→ID→live bind。 |
| 5：容量与恢复 | README 同代码 fake 四成员、容量 3；首个确认归档即创建第 4 个，另两成员尚未归档。覆盖 create 返回丢失、ID 记录后中断、journal/STATE 间中断、archive 成功回读丢失、重复通知及两次预算耗尽。重载先修镜像、歧义创建不重发、归档先回读；没有运行中轮询或猜测取消。 |
| 6：有判别力测试 | 66 项 lifecycle focused 与 206 项原契约/状态测试通过。AST 复核确认 59 个旧测试体原样保留；仅修正旧 FakeTransport 的原生收获后状态 fixture，使其归档前回读继续携带已验证的 native 身份，不伪换成 `actual-provider`。真实前缀在旧实现报 `missing Claude final leaf`，新模式成功；旧默认模式仍拒绝。 |
| 7：测量 | timing 保留区间并集，补充 createdAt spread、终态/实际通知接收、工具调用与抛错起止/次数、归档意图/确认、stage 墙钟。实际通知时间须由宿主传入，缺失端点为 null/未测量；硬崩溃丢失的工具响应或终点不伪造。activeTurn 窗口包含工具时间。未实跑真实 stage，不报告生产省时。 |
| 8：闭合 | 本 dispatch 的 focused、原契约/状态、registry、contract、空白检查通过。普通＋不同精确模型交叉独立验收、完整 17 门禁、严格 build、DONE_VERIFIED、提交和真实 child 归档由 ORCHESTRATOR 完成；本 dispatch 未执行这些步骤，不预报 DONE。 |

## 复现入口与实际退出码

派生产物目录：`.artifacts/i18n/review-speed-p1-20260912/execute-astra-01/`（以下记为 `ART`）。
所有临时 fixture 在 `/tmp` 或本 dispatch 目录；不读取真实 queue/checkpoint，不跑历史投影。
`run_contract_tests.py` 沿用已核验的临时目录 launcher，仅重定向 TemporaryDirectory，不替换测试体或断言。

| 实际命令 | 退出码与结果 |
|---|---|
| `timeout -k 10s 180s python3 -B -m unittest tests.i18n.test_review_lifecycle` | 0；66 tests，`focused-final.log` |
| `timeout -k 10s 180s python3 -B .artifacts/i18n/review-speed-p1-20260912/execute-astra-01/run_contract_tests.py` | 0；206 tests，`contracts.log` |
| `python3 -B tools/test_groups.py --check` | 0；PASS test group registration |
| `python3 -B tools/paseo_contract_check.py` | 0；10 active documents、4 live versions、16 clause declarations |
| `python3 -B .artifacts/i18n/review-speed-p1-20260912/execute-astra-01/replay_real_inputs.py` | 0；`real-replay-result.json` 保存完整哈希与结构证明，不保存会话或 thinking |
| `git diff --check` | 0 |
| `git diff --no-index --check -- /dev/null docs/review-speed-p1-20260912.md` | 1；无空白诊断，表示新增文件有差异 |

单独复现 README 配方与故障链：

```bash
timeout -k 10s 180s python3 -B -m unittest \
  tests.i18n.test_review_lifecycle.LifecycleTests.test_p1_readme_recipe_four_members_and_fault_recovery
```

测试从 README 的 BEGIN/END 标记提取原 JS。当前 Node 可用，但环境禁止 Node child_process
（EPERM）；测试通过单请求 stdin/stdout 桥让 Python 执行相同 shell 文本，再返回给原 JS。
这仍测试真正的 shell 单引号转义、完整响应传递、stdin JSON、Journal/native/strict 及真实消费者；
MCP 调用由 fake 提供，不能据此声称已实跑真实通知驱动的生产 stage。

开发过程的失败保留在 `focused-initial-legacy.log` 与 `focused-first.log`：先导出后换输出目录复用
暴露旧路径兼容问题；新增归档身份检查暴露旧 fake 回读丢失身份；Node 直接 spawn 被环境拒绝。
问题已分别修复，未改阈值、删除旧失败测试或跳检查。`focused-second.log` 是当时 64 tests 通过的结果，
随后补充真实中间元数据及 profile 字段测试，最终以 66 tests 的结果为准。

## 真实日志与性能边界

batch91 的已冻结归档前前缀为 223,604 bytes/71 lines，SHA-256
`1830845645c4daec1d6c03448ccdbe39d0d828d4395b128610e58dd2a8256d01`；真实后续 last-prompt
使日志变为 224,035 bytes/72 lines，SHA-256
`f8fa379d31bccc4d91052acd825642d206e4a9dea1e0129f4f19db58098020a3`。
两者 final 均为第 71 行，raw 均为 1,808 bytes，SHA-256
`24bfc42915473b0e9be4bb045372c2dc0fad38ae0b3aacfd12d3303025b37768`。
真实日志在工具执行期间已有中间 last-prompt/ai-title，完整保留并检查其已知叶节点/session/形态；
这里“无尾标”指最终 assistant 后无尾标。最终 last-prompt 后再接 ai-title 的第三种情况仅用
显式 synthetic fixture 验证，不冒充该真实文件的后续字节。历史归档后解析只用于兼容性核验，
不能补足当时归档前缺失的生产接受条件。

第 91 批 80 条为 79 done、1 repair_required、0 blocked；提交 `6c0c4d42…` 后已 finalize，
5 个子 agent 已归档，17 门禁与严格 build 通过。本批 07:41:02Z 至 08:15:41.731358Z 为
2079.731358 秒（34 分 39.7 秒），比第 90 批 2771.567502 秒约少 25%；深审 1 对 9 条、
无重试对 1 次，不是可比性能结论。181.397 秒无活动窗口不等于可节省时间。
源码事实输入、历史查询及重复投影优化留给后续 P1-C/P2-A/P2-B，本候选不扩展范围。

## Cycle1 集中修复与验证（fix-astra-01）

起点候选 `0bc7358b5a676411523269629bd17065858baa92bec0241dfdd369852df6147b`，
五文件 SHA256 与 `CYCLE1-START.json` 完全一致，HEAD 与上述基线一致。
本轮仅修复 `CROSS-ASTRA-01` 与 `HOST-P1-MODE`；`OPUS-R1` proof 命名为 advisory，未修改。

共享 `Journal.create_intent` 在写新意图之前检查 DONE/STOP/WAIT_USER 和 journal 中尚未确认的
耗尽归档；宿主 fill 消费同一检查结果，停止新增工作。首绑定、读回、可用预算归档与确认仍可执行。
原 `save` 恢复算法、预算 2 和 `wait.resume_state` 保持不变；已有成员全部确认后按原条件恢复。
README 组合回归证明：A 两次未确认、B 归档释放名额时，D 创建数为 0，D 行与意图不变，A 预算
仍为 2，WAIT_USER 与恢复点不变。A 后续确认不增加归档调用；C 完成确认后恢复 REVIEW，再创建 D。
直接 Python 入口另覆盖非归档原因 WAIT_USER、DONE/STOP，以及 STATE 尚未镜像耗尽条件时的拒绝。

profile 可选设置按“是否声明”合并，两个来源分别验证类型：单方声明则使用该值；双方声明且不同
拒绝；双方缺失不传；null、空字符串及非法类型不算缺失。真实 Astra profile 省略 modeId，
仍能使用冻结的 `auto-review`，provider/model 与 `high` 保持原值，不补 runtime identity。
脱敏 fixture 经完整 MCP 外壳到真实 host-event 持久化 intent，覆盖三类设置的来源组合、冲突与非法值。

本轮产物目录 `.artifacts/i18n/review-speed-p1-20260912/fix-astra-01/`，以下记为 `FIX`。
完整命令、退出码与日志索引见 `FIX/validation-results.json`。实际验证如下：

| 命令 | 退出码／结果 |
|---|---|
| `timeout -k 10s 180s python3 -B -m unittest tests.i18n.test_review_lifecycle` | 0；69 tests，`focused.log` |
| `timeout -k 10s 180s python3 -B .artifacts/i18n/review-speed-p1-20260912/fix-astra-01/run_contract_tests.py` | 0；206 tests，`contracts.log`；launcher 只重定向自身目录下的临时 fixture |
| `CYCLE1_PROBE_PREIMAGE=1 timeout -k 10s 180s python3 -B .artifacts/i18n/review-speed-p1-20260912/fix-astra-01/probe_wait_user.py` | 0；冻结前像及其 README 原配方复现 D 创建 1 次 |
| `timeout -k 10s 180s python3 -B .artifacts/i18n/review-speed-p1-20260912/fix-astra-01/probe_wait_user.py` | 0；当前 README 原配方中 D 创建 0 次，仍 prepared |
| `python3 -B .artifacts/i18n/review-speed-p1-20260912/fix-astra-01/probe_profile.py` | 0；真实捕获前像报 modeId drift，当前实现保留 auto-review/high 成功 |
| `python3 -B .artifacts/i18n/review-speed-p1-20260912/fix-astra-01/replay_real_inputs.py` | 0；复跑 B1/B2 两个旧实现失败／当前成功的真实有界探针，原 native 证明保持成立 |
| 原 README 六故障场景＋本轮组合、真实形态 profile、直接停止入口四项定向 unittest | 0；`recipe-profile-focused.log`，精确命令见结果索引 |
| `python3 -B tools/test_groups.py --check` | 0；registry 通过 |
| `python3 -B tools/paseo_contract_check.py` | 0；10 active documents、4 live versions、16 clause declarations |
| `git diff --check`；`git diff --cached --check`；新增文档 `git diff --no-index --check -- /dev/null docs/review-speed-p1-20260912.md` | 0／0／1；均无空白诊断，最后的 1 表示新增文件有差异 |

`preservation-proof.json` 以 AST 逐一确认此前 66 个测试体全部保留，新添 3 个测试体。
必要 helper 调整仅为 `recipe_runner` 的 archive-budget 分支：确认 A 后继续收获／归档 B、C，
按原 all-settled 恢复条件再断言 D 已创建；其他故障场景仍断言首个名额释放即创建第 4 个。
native parser、B1/B2、归档及恢复算法的函数 AST 均未改变；此前真实 native 产物未覆盖。
`final-full.patch` 包含相对基线的五文件完整候选，`cycle1-incremental.patch` 仅包含本轮增量。

本轮没有真实 agent 调用、生产重放、全历史投影、17 门禁或 build，也没有 stage/commit。
真实生产 stage 与生产省时仍未实测。两项 accepted 问题的有界修复和验证已交付，随后由主代理执行
一次完整 FINAL_REVIEW 与最终门禁／提交／生命周期闭合，不因 advisory 增加修复循环；不预报 DONE。
