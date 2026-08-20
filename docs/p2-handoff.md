# P2 进行中交接

> 类型：当前状态记录，非契约、非门禁，也不表示 P2 完成。
> 权威阶段与退出条件仍见 [project-roadmap.md](project-roadmap.md)。
> 本文件取代同目录较早的 `p2-handoff-2026-08-19.md` 作为「下一步」说明；旧文件保留为当时快照。

## 0. 一句话状态

P1 已完成。P2 正在按用户指定的 **Ashes → Orcs → Cults** 顺序做分层小批次。三个官方
DLC 的 **mechanics、timed-effect 状态、UI／运行日志** 均已收束（各层最后一轮侦察为明确
无候选）。**对话／长叙事** 已各自提交一轮：Ashes 完成缟玛瑙生育率、起始任务流星、Walrog
弹出对话、玛·洛克历史（3）剩余段落；Cults 完成 Fay Willows 纹身书信一轮准确度修订；Orcs
修正 Var'Eyal／Mindwall 误用并改进多段对话准确度。三层批次均已核验、过门禁并提交，工作树
干净，等待用户决定下一批范围。当前裁决仍是 **不 push、不修改发布仓库、不构建或发布 addon**。

## 1. 仓库快照

- 分支：`develop`
- 最新译文提交：`4d928ad fix: correct Orcs Var'Eyal and Mindwall references, dialogue accuracy`
  （其前为 `9888a6f` Cults 纹身书信修订、`50d368a` Ashes 对话层剩余候选）。
- 本交接文档提交：见该文件入树后的 `docs: add current P2 handoff` 提交及后续更新。
- 工作树：干净。
- 相对 `origin/develop`（`346e022`）超前约 96 个提交；其中约 70 个是 P2 译文 `fix:`。
- 固定游戏版本：ToME4 1.7.6；DLC 公开源码基线 1.7.4。
- 公开 DLC 根：`/home/yun/projects/tome4-dlcs/{ashes-urhrok,cults,orcs}`。
- 核心源码：`/home/yun/projects/t-engine4`（核验共享键时需要）。
- `fixed_source_identity`（envelope 用 `snapshot:` 前缀）：
  - Ashes `104ad8232778010e72f736559c726ea6ba8291265c28de2ecdf2275ec76dc2f2`
  - Cults `ed0b1126c2636738204f2cafa3259812092fe47f5393ba3b81d696fb56865747`
  - Orcs `c49975dd444a5402e37267005027ab2c54e23745a37836d31fd27fd808ee7484`

## 2. 相对路线图的位置

[project-roadmap.md](project-roadmap.md) §四 的 P2 优先级：

1. 三官方 DLC mechanics（Ashes → Orcs → Cults）
2. UI、状态和运行日志
3. 对话与长叙事
4. 辅助 addon／example 中确认玩家可见的内容

用户把 1–3 收成 **每个 DLC 先走完 mechanics → 状态 → UI／日志，再进入对话**。当前停在
第 3 层的 Ashes 开端。第 4 层和 P3（累计全量门禁、addon 构建、smoke、push／发布决策）
都未开始；路线图本身不授权这些操作。

P4–P6（v3 campaign、正式 120 条、Gold／Silver TM）仍为 deferred。

## 3. 分层完成情况

每项均以固定版本源码核验、`translation_contextual_v1` 独立审核和翻译门禁闭环；译文提交
只改对应 `tome-*.lua`。下表列层结果与代表提交，不枚举全部 Orcs／Cults status 提交。

| 层 | Ashes | Orcs | Cults |
|---|---|---|---|
| Mechanics | 完成 `a6e1d9d` | 完成 `fd708f7` | 完成 `78fbb16` |
| 状态／timed-effect | 完成（Fiery Torment／Aegis、Plaguefire、Only Ashes Left；后续无候选） | 完成（Pain Suppressor、PES 至 Moss Tread `038108b`；B33 无候选） | 完成（Overgrowth 至 Fatebreaker `6480555`；后续 status／UI 侦察无候选） |
| UI／运行日志 | 完成：炼狱之门感知 4 回合 `c133d72`；苦痛链接「选择源生物:」`0207be6`；B3 无候选 | 完成：瞬间引导 `dba9ef7`；惊艳射击 `bfe613a`；机械蜘蛛底盘 `a03e849`；B4 无候选 | 完成：精华收割→虚空之星 `3910cca`；禁忌之书移动速度 `4ae382d`；异变之手去掉「开启」`2c23383`；B4 无候选 |
| 对话／长叙事 | 完成一轮：缟玛瑙生育率 `f8f049a`；起始任务流星、Walrog 弹出对话、玛·洛克历史（3）其余段落 `50d368a`；后续 lore／quests／chats 待侦察 | 完成一轮：Var'Eyal／Mindwall 误用、DESTRUCTICUS 广告与多段对话准确度 `4d928ad`；后续 lore／quests／chats 待侦察 | 完成一轮：Fay Willows 纹身书信准确度与术语一致性 `9888a6f`；后续 lore／quests／chats 待侦察 |

绑定术语：`resists.all` = **全部抗性**（Direct Control、Pain Suppressor 等已按此执行）。

## 4. 暂停点与接任后第一步

三层（Ashes／Orcs／Cults）对话层各完成一轮，均已核验源码、过门禁并提交
（`50d368a`／`9888a6f`／`4d928ad`）。此前记录的 Ashes 三项候选（起始任务流星、Walrog
弹出对话、玛·洛克历史（3）其余段落）已随 `50d368a` 一并核验实现，不再是待办。

接任者 **不要自动开下一批**，等用户明确指示范围。三个 DLC 的对话／长叙事层都还有大量
未侦察的 lore／quests／chats，下一步需要先做一轮侦察（哪个 DLC、哪些文件）才能定出新的
候选清单；本文件当前不预先列出具体候选。

Ashes／Orcs／Cults 对话层之后才是第 4 层——辅助 addon／example 中确认玩家可见的内容。

## 5. 同键搁置（翻译无法单独特化）

运行时键是 `(source, source_tag)`。跨组件同 target 无覆盖风险；**不同 target 会覆盖**。
下列已核验为共享键，Ashes／Orcs 单独改中文会与核心冲突，除非所有发射点机制相同且同步改
`mod-tome.lua`（超出当前 DLC 批次）：

| 键 | 为何不能特化 |
|---|---|
| `The spell fizzles!` `logSeen` | 炼狱之门只表示定点传送失败、后续火焰／感知仍执行；核心多处表示整段法术失败并 `return` |
| `%s resists the shield bash!` `logSeen` | 恶魔之角：命中后免疫 `cut`；核心盾牌连击：命中后免疫 `stun` |
| `You require a weapon and a shield to use this talent.` `logPlayer` | Ashes 全是 `hasShield()`；核心 `Assault` 还要 `hasMHWeapon()` |
| `You have %d charges.` | Molten Point 等；曾改后因同键冲突而回退 |
| `%s is cured!` `logSeen` | 火焰净化与核心同键 |

`Pincer Strike` 的 `%d%%` 源格式本身无法在译文侧单独纠正。

## 6. 关键裁决（接任者不要推翻，除非新的源码证据）

- **源码是事实，不是英文表面措辞。** 炼狱之门英文写 sense 持续 3 回合，源码
  `setEffect(EFF_SENSE, 4)`；审核要求跟英文 3 被驳回（`c133d72`）。Track 对同一效果用
  `for %d turns` 对齐 `setEffect` 时长参数。
- Cacophony：额外时空伤害来自 `DARK_WHISPERS`／`SANITY_WARP`，不是 `EFF_HIDEOUS_VISIONS`。
- Moss Tread：`GRASPING_MOSS` 对占格生物结算；英文 passing-through 是天赋风味，不是代码门。
- 同键不能靠「这个技能特殊」改 DLC 译文；先 `grep` `mod-tome.lua`／另外两个 DLC。
- 审核 observation 不自动生效。SPEC 范围外的既有长文问题记下来，不在本批整篇重译。
  `f8f049a` 的审核即属此类。

## 7. 编排与执行约定

- 接任者是新的 ORCHESTRATOR：必须有非空 `PASEO_AGENT_ID`，在新任务 `STATE.json` 写入
  不可变的 `orchestrator_agent_id`。不要复用本会话的
  `204ac07d-909f-44a8-9509-7cfeab88e9fb`。
- 任务内容写入者同时只能有一个。Child 只通过 **agent-scoped** Paseo MCP `create_agent`
  创建，带 `labels.task_id`／`role`／需要时的 `purpose` 与 `dispatch_id`。
- 派发前 `paseo__list_profiles`：EXECUTOR 用 Utility — Luna（`codex/gpt-5.6-luna`，
  `auto-review`，thinking medium）；SCOUT／REVIEWER 用 Lead — Terra
  （`codex/gpt-5.6-terra`，`auto-review`，thinking **high**）。
- 译文审核：`role=REVIEWER`，`purpose=translation_contextual_v1`；短 prompt 三行；
  envelope 为紧凑 JSON；`candidate_identity = SHA-256(canonical payload)`。
- 收获后先把 `archive_attempts_started` 持久化再 `archive_agent`；确认归档后才进入下一阶段。
- EXECUTOR 不 stage、不 commit。门禁由 ORCHESTRATOR 独立重跑后再提交。
- 旧项目 Skill 已归档，不参与路由。

编排产物在 gitignored 的 `.ai/task/<task_id>/` 与 `.ai/reviews/<task_id>/`。最近完成任务：
`p2-ashes-dialogue-b1-001`（DONE，`commit=f8f049a`）。该任务的 SPEC 只授权单条缟玛瑙生育率
修订；`50d368a`／`9888a6f`／`4d928ad` 是该任务暂停期间在工作树中出现、经主代理直接核验源码
与术语后提交的后续工作，未走 Paseo child dispatch、无对应 STATE.json／review 记录——接任者
若要继续对话层，应开新任务并从侦察阶段开始，不要假设这三次提交延续了 `p2-ashes-dialogue-b1-001`
的编排状态。

## 8. 门禁（译文批次提交前）

按顺序，失败先修；不要用管道吞退出码。单测给至少 145–180 秒（454 项，常见 117–140 秒；
短超时不是挂起）。

```bash
python3 -B tools/i18n lint --strict; echo "exit=$?"
python3 -m unittest -q tests/i18n/test_toolchain.py; echo "exit=$?"
python3 -B tools/scan_runtime_collisions.py; echo "exit=$?"
python3 -B tools/classify_runtime_keys.py; echo "exit=$?"
git diff --check && echo DIFF_OK
```

当前基线（`4d928ad` 提交前独立重跑）：lint 30,308／0／0；454 tests OK（117.035s）；运行键
冲突 0；分类 1,711 桶 A／0 桶 B／0 桶 C。

术语表改动后另跑 `audit_static.py`、`audit_dynamic.py`、`annotate_domains.py`。

## 9. 不要做的事

- 不要 push；不要改 `tome4-chn-mod` 或构建／发布 addon。
- 不要为「零风险」去全量扫描 lore。
- 不要把英文说明或审核偏好盖过固定源码。
- 不要在未确认全部 child 归档时创建下一个写入 agent。
- 不要在用户未恢复暂停前自动开下一批。
