# P2 核心文本复核交接（2026-08-23）

> 类型：收尾记录，非契约、非门禁。
> 权威路线仍见 [`project-roadmap.md`](project-roadmap.md)；Paseo 编排与语境审核契约见
> [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md)（2.18-draft）与
> [`paseo-translation-context-review-v1-contract.md`](paseo-translation-context-review-v1-contract.md)。

## 交接更新（2026-08-24）

- 提交基线为 `a5c3ac6`（b6–b19）；其后仅有 b20 的 5 条未提交 `mod-tome.lua` 译文改动。
- b20：`last-hope-weapon-store.lua`（10 条）。将「军事训练」润色为「战斗训练」，补足两类训练的「基础使用方法」表述；保留 `Technique/Combat-training=技巧/战斗训练系`、`Shoot=射击天赋`、金额、source 与 source_tag。冻结身份 `660d64018b6cd24732efa26e35bfdf71fb3e263638936e246855ff204d4f2798`；独立语境复审 10/10 `OK`，严格 lint、`git diff --check`、完整 `tools/ci-gates.sh`、契约与 DONE 状态检查均通过。
- b21：`limmir-valley-moon.lua`（2 条）。固定源码核验后无改动；独立语境复审身份 `139f5312c3d97567e2052b00896bad8c5fc089388bb0636461105764592d447d`，2/2 `OK`。任务产物位于忽略的 `.ai/task/p2-tome-texts-b21-001/` 与 `.ai/reviews/...`。
- b20 已单独提交为 `507d2dc`；本交接文档的 b20／b21 记录提交为 `01179b7`。
- b22：`lost-merchant.lua`、`lumberjack-quest-done.lua`、`lumberjack-quest.lua`、`mage-apprentice-quest.lua` 共 33 条，提交 `6bcf55b`，修订 18 条 target。冻结工作集恢复为受跟踪的 `evidence/quality/p2-batches/p2-tome-texts-b22-lost-merchant-lumberjack-mage.json`（b19–b21 曾只留在忽略的 `.ai/`），33/33 英文键按固定 commit `624a673` 逐条字节核验，窗口内无 `args_order`。
- b22 主要修正：安格利文揭示处原译「为你开启了一个传送门」与固定源码不符——`access_angolwen` 放置城镇与入口传送门地形并 `locationRevealAround`，实为在地图上标出而非开启通路；`everybody in my village` 曾被译成「所有村子里的人」；学徒两个分支的「已收集到一些物品」与「祝你学业顺利」的 studies 从句均曾遗漏；本恩临终的结巴与未尽之言被抹平。`Kar'Krul` 批内统一为「卡·克鲁尔」，与同文件另一处及 `unlock-mage.lua` 一致，不做全局替换（`lore/elvala.lua` 仍为「卡库罗尔」）。
- b22 复审：两轮 `translation_contextual_v1` 全量复审同一冻结集，身份 `471b63ef…`（ctx-01，32/33 `OK`）与 `f2b42ddc…`（ctx-02，32/33 `OK`）。两轮就同一条 `b22-24`「The keepers of ar...」给出相互矛盾的意见（ctx-01 要求补回 keeper 关系，ctx-02 反对补回后的动词化形式）；按本文档规则升级维护者裁决，维护者选择保留「他们守护着奥……」，记为 advisory 未改。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）、契约检查与 `DONE_VERIFIED` 均通过。
- b23：`magic-store.lua`、`melinda-beach-end.lua`、`melinda-beach.lua`、`melinda-fortress.lua` 共 40 条，提交 `f8d8504`，修订 19 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b23-magic-store-melinda.json`，40/40 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b23 主要修正：`that tank` 原译「通道」与固定源码不符——`shertul-fortress-butler.lua` 说明梅琳达每天需在 `regeneration tank` 中治疗八小时，应为「再生槽」，旧译并漏掉每晚回来接受治疗；`I want to train at Zigur?` 误用阵营名「伊格兰斯」，`Zigur` 是地点「伊格」（`terminology/places.tsv`），这是全文件唯一偏离（其余 45 处均正确区分）；`Shadow` 原为「堡垒幻影」，全文其余 9 处均作「堡垒之影」；`We will find a cure` 漏掉治愈目标，而同段伊格兰斯分支保留了「治好你」；`still tainted` 曾误作「肯定」且漏译 `foul`，`raving zealots` 曾夸大为「杀人狂魔」，`I had no idea this would happen` 整句遗漏，沙滩叙述凭空添加阳光与「五颜六色」。另统一了中文文本内的半角 `!?,...`。
- b23 保留项：magic store 的欢迎语与范围外 `jewelry-store.lua` 共用英文键且两处译文一致，单改一侧会拆散共享运行时键，故按 `docs/runtime-key-collisions.md` 保留。
- b23 复审：两轮全量复审，`20b80a8d…`（ctx-01，39/40）与 `09224ef4…`（ctx-02，40/40 `OK`）。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- **教训：复用上一批的 envelope builder 时必须改 revision key 前缀。** b23 的 ctx-01 冻结集沿用了 b22 的 `b22-` 前缀，虽不影响正确性（payload／envelope／返回值内部一致，preflight 通过），但会与上一批的 key 命名空间冲突、误标批次来源；已在 ctx-02 重新冻结时改正为 `b23-`。
- 术语待办（未做）：建议新增 `Ziguranth → 伊格兰斯`（`T.PN.FACTION`，`society`），并注明与地点 `Zigur → 伊格` 严格区分。全文一致使用 27 次却不在术语库，正是 b23 该行发生偏离的原因。新增术语行需同步 `test_real_terminology_is_fully_mapped` 的硬编码行数，属独立小任务。
- 术语：`Ziguranth = 伊格兰斯`（`T.PN.FACTION`／`society`）已加入术语库，提交 `1a4a236`，同时把 `Zigur = 伊格` 行补上交叉引用并把 `test_real_terminology_is_fully_mapped` 的行数 710→711。固定源码证据：`anti-antimagic.lua` 同句「The defenders of Zigur were crushed, the Ziguranth scattered and weakened.」区分据点与教团；引擎另有 Zigur zone 与 `Zigur (Town)` grid 实体，`init.lua` 称 Ziguranth 为 an ancient order。地点用「伊格」，教团用「伊格兰斯」。
- 随后 `8fb41dd` 修正 `maj-eyal-npcs.lua` 的实体名 `ziguranth patrol`：伊格巡逻队 → 伊格兰斯巡逻队，与 `ziguranth.lua` 的三个同类实体一致。该实体在固定源码中 `faction = "zigur"`、`hates_arcane = 1`，是教团的游荡队伍而非地点（小写 faction id 是内部键，不是显示文本）。此偏离由「术语改动后用固定 Lua 桥加载 `mod-tome.lua` 复核」发现，lint 与三项术语审计都不会报——两种写法各自合法。
- b24：`message-last-hope.lua`、`myssil.lua`、`norgan-saved.lua`、`orc-breeding-pits.lua`、`paradoxology.lua`、`player-inscription.lua`、`point-zero-zemekkys.lua`、`pre-charred-scar-eruan.lua`、`pre-charred-scar.lua` 共 40 条，提交 `0b25434`，修订 25 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b24-myssil-point-zero.json`，40/40 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b24 主要修正：`Grand Keeper` 原作泛指的「伟大的守护者」，按术语库 `Keeper of Reality` 行及 `intro-chronomancer.lua`／`npcs.lua` 统一为「现实至高守护者」；育种棚拒绝分支原译成「一个人做不到」（能力不足），固定源码是玩家拒绝亲手行凶并交由艾琳处置，下一分支还凭空多出「一个人足以解决它们全部」；泽梅奇斯把「更年轻的我」讲反；临终太阳骑士的陈述凭空多出「一万倍」并漏掉手绘地图、吃力递交与最后恳求的目光；米歇尔的任务说明漏掉 eldritch forces／powerful／responsible／All corrupted，并把 `high in the Daikara mountains` 误作「最高峰」；另有 `then rest` 等整句遗漏与中文内半角标点。
- b24 复审：`ad8bc967…`（ctx-01）首轮即 40/40 `OK`，无修复轮。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- b24 宿主 advisory（未改）：`paradoxology.lua` 的 `What the...` 由「我X！」改为直译「这是什么……」。直译更贴字面，但削弱了被打断的惊愕语气；复审未提出异议，按编辑裁量记录，不作缺陷。
- 待办（超出当批窗口）：`zemekkys-start-chronomancers.lua` 存在同样的 `Grand Keeper` 偏离，留待轮到该 section 的批次处理。
- 流程变更（2026-08-24，提交 `5a57f2f`）：译文复核改为**连续批次模式**，一批 `DONE` 并提交后直接开始下一批，不再逐批等待批准。停下条件与自行处理范围见 `AGENTS.md`「连续批次模式」；连续运行不豁免任何冻结、复审、门禁与生命周期要求。
- 流程变更（2026-08-24，提交 `e21e01e`）：判定 child 挂起或调用 stop／cancel 前必须先做有界终态取证——重查实时状态并读 `attentionReason`／activeTurn，再看工作树（未产出改动的 EXECUTOR 留下空 diff）。EXECUTOR 结束却无工作成果时输出无效：先归档再 fresh retry，不得对已结束 child 发 follow-up。已写入的故障归因被推翻必须同轮更正。见 `docs/lessons-learned.md` 第 11 条。
- b25：`ring-of-blood-master.lua`、`ring-of-blood-orb.lua`、`ring-of-blood-win.lua`、`sage-kitty.lua`、`shadow-crypt-yeek-clone.lua` 共 37 条，提交 `9ab2a60`，修订 20 条 target。冻结集 `evidence/quality/p2-batches/p2-tome-texts-b25-ring-of-blood-shadow-crypt.json`，37/37 英文键按 `624a673` 字节核验，窗口内无 `args_order`。
- b25 主要修正：竞技场规则原译承诺奖品是「一个戒指」——任务代码确认「鲜血呼唤」确为戒指，但该句台词只点名奖品，故删去凭空补充的说明，并修正 `会……了` 时态冲突、补回 our pawns；十轮回合数与玩家经水晶球控制奴隶的机制已按任务源码复核。`slave fodder` 曾被译成「像奴隶一样的炮灰」（改变了所指）；`Normally you would be taken as a slave` 漏掉被掳为奴；`standard fee` 遗漏且凭空多出「每次」；小猫漏译橘色却多出「眼泪汪汪」。
- b25 复审：`0cbb7c58…`（ctx-01）首轮即 37/37 `OK`，无修复轮。五步门禁、完整 `tools/ci-gates.sh`（12/12，含构建）与 `DONE_VERIFIED` 均通过。
- b25 生命周期：首个 EXECUTOR dispatch 结束却无任何产出（无 diff、无报告），按新规归档为 spent，另建 fresh retry child 完成本批；两者均已确认归档。
- 当前预期工作树：干净，仅用户本地未跟踪 `.claude/`；不得提交、删除或混入 `.claude/`。`.ai/` 与 `.artifacts/` 是忽略的派生产物。
- 接手步骤：继续审校时跳过已核验且无改动的 `limmir-valley-moon.lua` 与已完成的 b22–b25 共 22 个 section，从 `shertul-fortress-butler.lua` 起继续下一个有界切片（该 section 单独 53 条，建议自成一批）。每批把冻结工作集写入受跟踪的 `evidence/quality/p2-batches/`；复用上一批的 envelope builder 时先改 revision key 前缀。连续批次模式下不必逐批请示，按 `AGENTS.md` 的停下条件判断何时交回维护者。
- 复审记录格式注意：`.ai/reviews/` 记录必须带 `status`（或 `result`）且取值属于 `completed`／`completed_with_findings`／`PASS`／`CHANGES_REQUIRED`／`FINDINGS`／`OK`，否则 `ai_state_check.py` 的 `candidate_bindings_valid` 会拒绝 DONE。

## 0. 一句话状态

`p2-tome-texts-b<N>` 轨道已完成 15 个译文批次（2026-08-22 至 08-23）：核心 `mod-tome.lua` 的
`data/texts/intro-*`、全部 `unlock-*`、`data/talents/misc/inscriptions.lua` 全段，以及教程／帮助
文本 part A、教程／帮助文本 part B、竞技场、炼金术士、安格利文与阿尔德胡格对话、工艺工具 UI 与刺客领主对话、遥远太阳化身对话、时空与指挥法杖文本，以及 Conclave、腐化者、德斯镇、恐惧王座、东部传送门、艾德隆位面、埃莉萨、护送任务与堕落艾琳对话。共复核 **690 个 `t(...)` 对**，修订 **157 个 section**，语境审核确认并修复
**62 个 finding**；b1–b5 提交均在本地 `develop`，b6–b15 尚未提交；**未 push、未发布**。

## 1. 批次结果

| 批次 | 口径 | 条目 | 修订区块 | confirmed finding | 提交 |
|---|---|---:|---:|---:|---|
| b1 | `data/texts/intro-*.lua`（18 区块） | 18 | 14/18 | 9 | `5efe265` |
| b2 | `unlock-*.lua` 前 22 区块（adventurer…mage_geomancer） | 44 | 20/22 | 9 | `ff25042` |
| b3 | `data/talents/misc/inscriptions.lua` 全段 | 120 | 17 对 | 4（另 2 条撤回） | `1feed76` → 修正 `9097c6f` |
| b4 | `unlock-*.lua` 其余 21 区块（mage_necromancer…yeek） | 42 | 18/21 | 10 | `f3c6bba` |
| b5 | 教程关卡说明、stats1–9、最后的希望来信（21 区块） | 22 | 16/21 | 7 | `888fc54` |
| b6 | 教程／帮助 part B：calc、scale、tier、timed、tactics、talents、terrain（50 区块） | 50 | 23/50 | 4（另 3 条经高级校准撤回） | 未提交 |
| b7 | `data/chats/arena-start.lua`、`arena-unlock.lua`、`arena.lua` | 65 | 3/3 | 3（波次标签） | 未提交 |
| b8 | 炼金术士 Derth、Elvala、傀儡对话全段；Hermit／Last Hope 共享门锁键 | 93 | 5（3 全段 + 2 单键） | 2（门锁提示语义） | 未提交 |
| b9 | Angolwen 领袖／法杖店、反魔结局、Ardhungol 起止对话 | 46 | 5/5 | 0 | 未提交 |
| b10 | 工艺工具 UI、刺客领主及其喽啰对话 | 29 | 5/5 | 3（所有权、准备过程、复数处置关系） | 未提交 |
| b11 | 遥远太阳解锁与化身对话 | 29 | 2/2 | 0 | 未提交 |
| b12 | 时空异常／时间线／指挥法杖；共享取消键同步至 Ward、傀儡与 Cults | 41 | 6（3 全段 + 3 单键） | 4（取消语义、死后延续、法杖形态、问因） | 未提交 |
| b13 | Conclave 守卫、腐化者招募、德斯镇袭击结局、恐惧王座伏击 | 36 | 4/4 | 0 | 未提交 |
| b14 | 东部传送门结局、艾德隆位面、埃莉萨占卜水晶球与商店对话 | 38 | 4/4 | 0 | 未提交 |
| b15 | 护送任务起止、堕落艾琳对话 | 17 | 3/3 | 1（护卫已死事实） | 未提交 |

finding 数只计语境审核（`translation_contextual_v1`）中宿主裁决为 confirmed 的观察；EXECUTOR 在
读-改阶段直接修正的条目（每批 25–75 行）另见各批次 `evidence/quality/p2-batches/*-host-verification.json`
的 `adjudicated_findings` 与 `items`。每批的工作集冻结文件同目录，均记录 `fixed_source_identity`
（`commit:624a673…`）与逐条 `pinned_source_match`。

典型修正：Point Zero「使时空法术得以存在」（原译为「时空行者方能进入」）；竞技场／无尽地下城
「没有出口」被译成「只有一个出口」；转化之盒凭空多出「无法储存能量」；时空守卫「中型与小型武器」
被译成「或」；堕落者「死星之力」被译成重力；纹身 Wild「减少受到的伤害」；Rune of Vision／
Dissipation 的 `args_order` 误判（见 §3）；最后的希望第二封来信整句遗漏「请务必调查」。

## 2. 本轮基础设施变更（已独立提交、交叉复审）

| 提交 | 内容 |
|---|---|
| `7085a98` | `contextual_anchor_preflight.py` 接受 `ordered_titles: []` 的 whole-section window（契约 2.17-draft）。b1 首次消费 2.16 preflight 时发现其只能表达 Fay Willows 式章节标题锚点，对任何无章节标题的 section 都无法构造合法 SCOPE。 |
| `a2e86d4` | preflight 读取 `t()` 第四参数 `args_order`（规范形式 `{i,j,...}`，接受 `;` 与尾随分隔符），并要求 `bounded_context.context` 精确披露 `args_order={...}` 标记，否则 fail closed（契约 2.18-draft；标记入 `paseo_contract_check` 与 toolchain inventory）。 |
| `90acafe` + `d347d52` | 术语表新增 `Keeper of Reality=现实守护者`、`Wayist=维网信徒`；`d347d52` 修复 `90acafe` 未同步 `test_real_terminology_is_fully_mapped` 的 708→710 行数而导致的红 HEAD。 |

## 3. 必须知道的教训

1. **`args_order` 是一等机制。** `t(source, target, tag, {2,1})` 的第四参数在运行时重排格式参数；
   `mod-tome.lua` 中有 51 条。lint 的 `format-mismatch` 已按 `args_order` 校验转换序列。b3 曾把
   两条带 `args_order` 的条目误判为「占位符顺序缺陷」，并在改写文本后遗留 `{2,1}`，引入真实回归
   （`1feed76`），随即由 `9097c6f` 修正、`779a4d3` 撤回证据中的两条 finding。任何重排译文占位符
   都必须同时更新或删除 `args_order`；宿主与 reviewer 检查占位符顺序时必须读取第四参数。
2. **术语行变更后必须重跑完整 toolchain 单测。** `tests/i18n/test_toolchain.py` 硬编码术语行数
   （现为 710）与 orchestrator.md 标记清单；只跑 preflight 或审计脚本会漏掉它。
3. **共享 runtime key 的术语修正会触发跨组件碰撞门禁。** b3 的「相位之门」落在与
   `tome-ashes-urhrok.lua` 共享的 `logPlayer` 键上；按 `docs/runtime-key-collisions.md` §3.3 先例，
   以 SPEC 修订把 DLC 行对齐为相同译文，而不是回退术语。
4. **reviewer 每轮重看整段。** 长段落通常需要 2–3 轮 FIX／复审才能收敛；这是正常成本，不要跳过
   复审。
5. **结果校验要机械化。** 从 Paseo activity 取回完整 JSON，按冻结 envelope 逐条 byte-compare
   evidence、顺序与 identity（b3 起已如此），不要目测。
6. **不要在工作树上用空的 `git stash`/`stash pop` 对。** 本轮一次 smoke test 误弹出了前一会话的
   stash；已折回 `stash@{0}`（README 链接 + `dependencies/` + `docs/container-dependency-inventory.md`），
   `stash@{1}` 为更早的 `infra-contract-008…` WIP，均未并入任何提交，去留由维护者决定。

## 4. 未完成与下一步

- **batch 6–7 已完成、待单独提交：** b6 为 `data/texts/tutorial/stats*/` 其余 50 条单对 section
  （calc0–11、scale1–12、tier0–12、timed0–8、tactics1–2、talents、terrain）。复核重点为公式、
  百分比、算例与运行时 UI 标签；b7 为竞技场的开始、解锁和对局对话，复核重点为人物关系、奖励与
  波次模式。两批的完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 8 已完成、待单独提交：** `alchemist-derth.lua`、`alchemist-elvala.lua`、
  `alchemist-golem.lua` 全段，并为 strict runtime-collision 门禁把 `alchemist-hermit.lua`、
  `alchemist-last-hope.lua` 的同一门锁提示对齐为“门锁着，无人回应你的敲门声”。93 条均经二轮
  `translation_contextual_v1` 冻结复审；完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 9 已完成、待单独提交：** `angolwen-leader.lua`、`angolwen-staves-store.lua`、`antimagic-end.lua`、
  `ardhungol-end.lua`、`ardhungol-start.lua` 共 46 条；语境审核全部 OK，完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 10 已完成、待单独提交：** `artifact-maker.lua`、`artifice-mastery.lua`、`artifice.lua`、
  `assassin-lord-thieves.lua`、`assassin-lord.lua` 共 29 条；三轮语境审核确认并修正了盗贼领主的
  所有权语气、工艺准备过程与“我们该怎么处置你”的复数关系，完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 11 已完成、待单独提交：** `avatar-distant-sun-unlock.chat`、`avatar-distant-sun.chat` 共 29 条；
  语境审核全部 OK，保留遥远太阳由伪善友好转为操控不耐的语气、烈焰展示、化身状态与拒绝后的觉醒点返还；完整五步门禁和 `tools/ci-gates.sh` 均已通过。
- **batch 12 已完成、待单独提交：** `chronomancy-bias-weave.lua`、`chronomancy-see-threads.lua`、`command-staff.lua`
  共 40 条，并同步 3 个共享运行时键（Ward、炼金傀儡、Cults 的龙血形态菜单）。41 条均经五轮
  `translation_contextual_v1` 冻结复审；共享 `Never mind` 键统一为“算了。”，跨组件碰撞归零；完整五步门禁、
  `tools/ci-gates.sh` 与状态契约检查均已通过。
- **batch 13 已完成、待单独提交：** `conclave-vault-greeting.lua`、`corruptor-quest.lua`、
  `derth-attack-over.lua`、`dreadfell-ambush.lua` 共 36 条；语境审核全部 OK，修正了 Conclave 守卫的时代错位、
  腐化者对魔法大爆炸裂隙的利用、德斯镇雷暴袭击的主谓关系与乌克鲁克索要法杖的威胁；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 14 已完成、待单独提交：** `east-portal-end.lua`、`eidolon-plane.lua`、
  `elisa-orb-scrying.lua`、`elisa-shop.lua` 共 38 条；语境审核全部 OK，保留东部传送门的部件交接、
  艾德隆位面的死亡／去留分支、维网识别流程及埃莉萨水晶球的远程通话和普通物品自动鉴定机制；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- **batch 15 已完成、待单独提交：** `escort-quest-start.lua`、`escort-quest.lua`、
  `fallen-aeryn.lua` 共 17 条；二轮语境审核确认并修正了堕落艾琳控诉中“有人为保护玩家而死”的既成伤亡事实，
  保留反魔护送分支将 NPC 送往伊格、自然之力使传送门失效及艾琳的毁灭轮回问责；完整五步门禁和
  `tools/ci-gates.sh` 均已通过。
- 下一候选：`data/chats/`、`data/lore/` 的有界切片；按当前持续处理指示继续选择下一批。
- 已知 advisory（未改）：教程 intro「Tales of Maj'Eyal」作 ToME 4；竞技场标题「挑战主宰」；
  Vim 定义句用「活力」；岩石守卫「分身」。`Maj'Eyal` 在文件内 马基·埃亚尔／马基埃亚尔 并存，
  只在批次内统一，不做全局替换。
- P3 事项不变：`develop → master` PR、正式 release、teaa／te4.org／创意工坊发布均需新指示。

## 5. 单批操作清单（b5 实际流程）

1. 冻结工作集到 `evidence/quality/p2-batches/<batch>.json`：逐条用 `git show 624a673:<path>` 核验
   英文键，并记录每个调用的 `args_order`。
2. 写 `.ai/task/<task>/SPEC.md|PLAN.md|STATE.json`（schema 3、`change_class: standard`、
   `review_contracts: ["translation_contextual_v1"]`）。
3. EXECUTOR（Luna，`auto-review`/xhigh）读-改；宿主核验范围、英文键零变更、行结构，归档。
4. `SCOPE.json`（每个 section `ordered_titles: []`）→ 七键 payload（`bounded_context` 对带
   `args_order` 的调用写入 `args_order={...}`）→ `tools/contextual_anchor_preflight.py` →
   紧凑规范 envelope → REVIEWER（Sol）按契约第四节三行 prompt 派发，labels 含
   `candidate_identity`/`dispatch_id`。
5. 取回 activity 原文机械校验；宿主按固定源码裁决；confirmed 进 fresh EXECUTOR FIX，重新冻结
   envelope 复审，直至全部 OK。
6. 五步门禁 + `tools/ci-gates.sh`（含构建）→ 宿主核验记录 → `ai_state_check.py` DONE →
   单独提交译文批次；roadmap/记忆随后单独提交。
