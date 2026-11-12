# 当前恢复入口（2026-11-11 0.3.12 已发布，轻量审核队列空）

**状态。** 第 0001–0461 批已全部提交并经 `tools/push_github.sh` 推送；`lite_review.py` 的 `pending_A` 为 0，没有进行中的批次或 child。
插件 0.3.10 已于 2026-11-09 按用户指示发布（发布仓库 `4843901`，13,688 条＝核心 8,045＋引擎 182＋DLC 5,461，
凭据 [`evidence/releases/addon-0.3.10.json`](evidence/releases/addon-0.3.10.json)）。

**2026-11-11 死键扫描（只记录，暂不处理）：** 全库确认 22 条死键（21 条有在用副本，1 条上游已删），用户决定先不删，证据 `evidence/quality/dead-key-scan-20261111/`。修长文前先核对 section 与 1.7.6 源码字面量：`tome-orcs.lua` 挂在 DebugMain section 的两篇 lore 是死键，0456–0458 曾修错副本，第 0475 批已同步到在用副本。

**0.3.12 已发布**（2026-11-11，发布仓库 `495aa44`，含 0480–0495 批、混乱苔藓修复与 6 处插件代码修复 `a262ee4`），凭据 `evidence/releases/addon-0.3.12.json`，就绪审查 `evidence/releases/candidate-0.3.12/ACCEPTANCE.md`。

**PR 合并常驻授权（2026-11-11 维护者指示）：** ToME4 已授权任务产生的 PR，在适用检查和必要的既有独立复审通过、没有未解决的实质问题后，可以直接合并；如果只剩检查在等待且仓库支持，也可以设置自动合并。
- 合并前核对目标分支和当前 head，使用 head 一致性保护；head 变化后补足受影响的复审和检查。
- 草稿先转为 Ready；不为此修改仓库保护规则或新增服务。
- 这项授权不包括发布新版本。

**发布与验收分工（2026-11-11 维护者指示，现行流程）：** 本地只做版本、包、来源身份、构建/门禁和发布完整性核对，然后公开发布；实机验收由测试玩家在发布后进行。本地自然游玩和实机补测不再是发布前置条件，也不再为旧的验收清单开本地游戏或派发 DeepSeek 补测。细则见 `i18n/README.md` 开头。
- 0.3.12 发布后的 DeepSeek 第一轮记录照实保留在 `evidence/quality/live-test-20261111/accept-0312/ADJUDICATION.md`：活物、苔藓说明、存读档已在游戏中看到；捕熊陷阱「定身」和「寄生」只有控制台结果；「[离开]」、「其他」、压力作战服和 Cults 场景未到达。
- 这些未覆盖项已写进 Release v0.3.12 的说明，作为玩家检查点，反馈经发布仓库的 Issues。
- 第一轮遗留：Clork「克拉克」音译为 pending（纯名称问题，`tome-orcs.lua` 中 16 处，改名需授权），另有 3 条 advisory。

**0.3.11 已发布**（2026-11-11，发布仓库 `47f74c3`，含 0462–0479 批与 light 子类型插件代码 `4dd38b0`），凭据 `evidence/releases/addon-0.3.11.json`。

**2026-11-07～11-09 完成：**

1. 插件代码修复（用户 11-08 裁决：物品属性行 all 只在 getTextualDesc 期间显示「全部」；装备人偶只显示材质简称、分隔符改「、」）：
   发布仓库 `4a86895` 新增补充词条 `data/chn_supplement.lua`（独有键，避免改动 "nil" 兜底表）与 11 个 superload 包装
   （商店标题、按键分组、成就分类、立绘名牌、自动探索中断原因、裸字面量弹窗、Orcs 锁定职业描述、战役名、疯狂值双百分号、
   盾牌 add_name、装备组切换、使用技能窗口三列、开局「切换至 player」日志、人偶分隔符）。实机验证证据
   `evidence/quality/live-test-20261104/addon-fix-20261108/`。仍未做：引擎折行拆数字（I）、Steam: 前缀、Ashes 欢迎框种族列表。0.3.9 于 11-08 发布。
2. 固定神器名称与描述核对（0449–0452，证据 `evidence/quality/artifact-name-desc-check-20261108/`）：描述／未鉴定名对齐、
   Gemini 4 Argon 定名 18 件；用户指出第三组别扭后回退 9 个为官方译名（新规则：官方译名只在误译、撞名、专名冲突时改）。
3. 公开版 0.3.9 反向检查（0453–0458，证据 `evidence/quality/reverse-check-20261109/`）：32 个 Opus 子代理先读中文再核英文，
   99 条发现中 94 条修复（含 Embers 流血阈值「5 倍」→「5%」）；复审连带修 13 处；primal-forest lore 第三轮剩一条二级语感问题记 advisory。
4. 术语裁决（用户 11-09，0459–0461）：Jinx＝厄运、implant＝植入物（术语表已更新，terminology 行数 923）。

**现行裁决** 见 `docs/review-operations-guide.md` 第六节（本次新增：官方译名修改门槛、固定神器名、shot＝弹丸、Jinx、implant、Kar'Krul、Allure Wars）。

**未决／advisory：** Combat Veteran「战斗经验」待术语裁决；泰鲁戈洛斯（官方）与 -格罗斯 族不一致、非之家（区域名）记 advisory；
primal-forest lore 一处比较对象搭配（0458 advisory）。下文 11-03 入口的待决事项除已注明完成者外仍有效。

---

# 历史恢复入口（2026-11-03 轻量审核 A/B 双审全覆盖，队列空）

**状态。** 用户 2026-11-01 授权把全量审核改为轻量流程（方案 B，见
[轻量审核流程](docs/lite-review-workflow-20261101.md)）；旧审计证据冻结在 R296（`fab80aa3`），原样保留。
第 0001–0316 批已全部提交并经 `tools/push_github.sh` 推送（最新 `2fe3a7b20`）。29,545 个 release-required 单元
A（Opus 5.5）与 B（GPT 6.1 Sol）全部覆盖，`python3 -B tools/lite_review.py status` 显示 `pending_A` 0、
`pending_B_backfill` 0。账本 `evidence/lite-review/ledger.jsonl` 22,533 行：ok 21,580、confirmed 854、
advisory 70、rejected 29。当前没有进行中的批次或 child（各 lane 由 `tools/lite_dispatch.sh` 收取后归档）。

**本阶段完成的专项（均为维护批，改过的单元已由 A/B 复审）：**

1. 按实现改写（用户 11-02 定「按实际效果改写」）：0238 轻量 14 条、0241 旧流程 177 条（不改 25 条及理由在
   `batches/0241/maintenance.json`），复审 0239–0246 再修 15 条；组外发现核实 0252（19 条：改 11 行，驳回 selffire、
   石化凝视半径、BREACH 等），复审 0253 再修 1 条。
2. 命名积压交 Gemini 4 Argon：0247（15 项，含 末日招来者、实验体 Z、技能树解锁点、炼金术士、tinker＝配件／商店＝工匠），
   0250（用户采纳：steam drone＝蒸汽无人机械、drone＝无人机械、Mind Drones＝精神无人机械，取代 09-28 的「精神无人机」）。
3. B 补审（用户 11-02「请补做B审」）：0255–0312 共 58 批 4,450 单元；当批直改 9 处客观不一致（大嘴怪之牙、揭弱的、
   涌动的、堕落印记→污印 10 处、唯我论、重建傀儡提示、恶魔空间之荣耀等）；23 个自拟名入队后在 0313 交 Gemini 改 22 个
   （混合螺旋按 Threading＝螺旋惯例保留），0315 按用户要求把 Shattered Remains 技能名统一为「碎骨遗骸」。

**现行授权与规则。** 连续推进不逐批确认；每批一次提交并推送（只用 `tools/push_github.sh`，对外发布须用户指示；0.3.7 已于 11-03 发布）。
宿主逐条按源码裁决（核心用固定提交 `624a6732…`，DLC 用 `/workspace/tome4-dlcs` 公开检出并标未固定）；运行时键全文件同改；
英文与实现不符按实现改写、占位符参数错误记 advisory；自拟名交 Gemini 4 Argon。生效的用户裁决见记忆与
`docs/review-operations-guide.md` 裁决表，近期新增：her＝她的、码→格、killer_message 凶手主语主动句、宝石、超距作用、
Exhaustion＝力竭、Parry＝招架、Summon＝召唤、Archmage＝元素法师、源码无法确认的跳过（Possessors 未公开）。

**恢复方法。** 驱动脚本已收入 `tools/`（`lite_dispatch.sh`／`lite_close.sh`／`lite_loop.sh`／`lite_queue_names.sh`），
用法见流程文档「驱动脚本」一节；须导出自己的 `PASEO_AGENT_ID` 与 `TOME_PASEO_WORKSPACE`。若译文再有改动，
`lite_review.py status` 会把改过的单元列为待审，按普通批次 `prepare N` → `lite_dispatch.sh N` → 裁决 → `lite_close.sh` 处理。

**实机测试减流流程（2026-11-11 维护者同意；只适用于维护者另行明确要求的本地实机测试，不是发布前置条件）。**
- 测试员 prompt 模板为本地 `~/tome-live/prompts/common.md`，主代理操作说明为 `~/tome-live/prompts/HOST.md`。两者都是本机运行环境文件，不入库。
- 文本先核对：字符串和数值先用 Lua 和日志核对；截图只用于字体、截断、布局和最终关键帧，日志不能代替显示验收。
- 只读裁切图：全屏原图留在本地，Read 只读目标区域的裁切图，裁切不得掩盖所测布局。
- 合并命令：已知导航、等待、截图和裁切合并成一条命令；遇到未知界面先停下观察。
- 独立会话：每个会话只做一个场景组，用 Paseo 新建，不 fork 主会话。
- 试行预算：读图 30 张，其中全屏 5 张；工具调用约 120 次。工具调用数是代理计数，不等于 HTTP 请求数，由测试员自行计数，没有自动强制。达到上限即保存并停止，剩余范围由新会话接续。
- 主代理优先读文本报告，只审必要的裁切关键帧。
- 每轮报告写明：场景、读图数（总数/全屏）、会话与调用计数、停止原因。流量减少未经实测前不报节省比例。

**2026-11-04 实机测试。** 官方 1.7.6＋汉化 0.3.7＋三 DLC 在 `~/tome-live`（Xvfb，见记忆 live-game-test-env）由三个测试员实测，67 条发现，处置见
[`evidence/quality/live-test-20261104/`](evidence/quality/live-test-20261104/REPORT.md)；修复提交 `aa29cbd12`（含 publish 把 engine 差异条目写进插件、
%-8.8s 放行、不休狂热、快枪手）。0.3.8 已于 2026-11-04 按用户指示发布（发布仓库 `f27c7dc`，13,439 条，凭据 `evidence/releases/addon-0.3.8.json`；含 null_translation.lua 删 21 条遮蔽项），
候选包复测 6 过 1 部分 1 未触发。改动的 61 个单元已在 0319–0321 复审。

**2026-11-04 第二轮（容器为接入显卡关闭前保存，最新提交 `bacfa7d65`）。**
- 规则：0322 盲审（prompt 不透露修改原因／已知问题）、语序与病句必报、改写者代入占位符通读（记忆 blind-review-and-rewrite-readthrough）。
- DeepSeek 盲审流畅度复查 197 个改写单元：0323 改 26 条、驳 9 条（证据 `evidence/quality/fluency-recheck-20261104/`）；0324 盲审再修 3 条，0325 无问题。
  `lite_review.py status` 队列为空（A／B 均 29,545）。
- 第二轮实测（结果在 `evidence/quality/live-test-20261104/round2/`）：r2-gpt 完成，1 条（纹身语序，已于 0323 修）；r2-sonnet 完成，2 条**未修**：
  r2-sonnet-01 休息日志「休息了0回合 (停止原因：…)」半角括号／缺空格；r2-sonnet-02 余烬怒火欢迎框「炽热金属轰鸣」措辞。
  r2-ds（DeepSeek）跑约 3 小时未写 findings 即因关机强制归档，无结果；如需可重开。
- 11-04 GPU 重跑 r2-ds（`TL_GPU=1`，60 fps 帽）；按键绑定「退出目录」(Exit menu) 已记录，属引擎启动期求值、需代码钩子，用户 11-04 定暂不处理，见 `round2/pending-fixes.json`。
- 规则：11-04 用户授权允许唤醒已停止（idle 未归档）的 agent，AGENTS.md 与 Paseo 契约已改；仍不得向运行中的 agent 发消息。
- 11-04 第二轮收口：r2-ds 重跑 11 条（01 按键名延后），连同 r2-sonnet 2 条由执行者修复（0326），盲审 0327 再修 1 条（欢迎框战役名对齐菜单「兽人战役：余烬怒火」）、驳 2 条（占位符空格是库内惯例），0328 无问题；队列空（`173974720`）。
- 11-04 第三轮（Sonnet 5.5 实际游玩，GPU，本地开发版插件 locale e3763098…，0.3.8 备份在 ~/tome-live/addon-backup/）：约 2h50m（唤醒 1 次）只到 2–3 级、未击败普罗克斯（按键脚本盲打）；11 条，修 7 条（0329，含 tome-possessors 同键），驳 2、advisory 2（round3/adjudication.md）；0330 盲审无问题，队列空（`40229264f`）。
- 11-04 第四轮（DeepSeek v4.1 Flash，14:00–20:30）只到 1 级；5 条修 3（0331），驳 2（其一因测试插件陈旧重报已修项——宿主失误，已更正）；盲审 0332–0337 连带修种族开场文本 18 处语病／方位／漏译，0337 收敛；测试插件已按 `18629a961` 重建（locale acaf7c1d…，13,461 条）。
- 11-05 第五轮（Opus 5.5）：9 级、击败普罗克斯、德斯商店、古老森林；23 条，修 17（0338）＋盲审 0339 再修 2（敏捷暴击按实现改写、纹身「解除%s负面效果」），0340 无问题，队列空（`7e491372b`）。**待用户决定**：① 9 条新增条目（Easy×2、6 个金库湿身怪名、shield entity combat talented）需把冻结的版本向量 30308→30317（production_review_v2_lite.CURRENT_VECTOR 与 policy-v1.json，门禁 05），见 round5/pending-additions.txt；② 楼梯地形名「前往下一层／上一层」是 preferred 术语但代入「这里有一个%s」成病句，建议改「通往下一层／上一层的通道」。
- 11-05 用户批准新增 9 条（版本向量 30308→30317）与楼梯地形名「通往下一层／上一层的通道」（0341–0342）。第六轮（Opus 5.5 半身人星月术士）8 级、清卡·普尔、到黑暗之心；13 条全修（0343，含官方 args_order 残留：全库仅 3 条补 {1,2}，见记忆 official-args-order-residue）；0344 再修 2、advisory 3（预先存在的换行布局），0345 无问题，队列空。名后空格已由用户批准统一清理：0348 扫 131 条，0349 再修 19、0350 再修 9，0351 无问题。第六轮第二段（同一角色，agent 71afca35）击败黑暗之心 Boss、进夏特尔与迷宫，止于 10 级（未达 12）；新增 5 条：15/16/17 由主代理修（0352，0353 盲审），14/18 为源码硬编码半角逗号，与其他 addon code 项一并暂缓。
- 11-05 流畅度定向复查（用户「请按照之前拟定的优先级开始扫描」）：P1（11-01 后 AI 改写、11-04 严格盲审前最后修改，1,205 单元）＋P2（10-13～10-31 修复窗口，646 单元）在 0354–0381 全部盲审完毕，confirmed 90 / advisory 10 / rejected 9，见 evidence/quality/fluency-recheck-20261105/README.md。0372 修复曾因管道吞错未落地，已补。用户 11-05 裁决：lore 中 equilibrium 两种译法均可（不改）；fay-willows 8d6b9fc7fd55 交 Gemini 4 Argon 整段重译（0382，0383 再修 1 句，0384 无问题）；lore 中 yard 译「码」（全库仅 2 处，已改，见 docs/distance-unit-ge-20261101.md 例外节）。
- 11-05 Lore 单独筛查（evidence/quality/lore-screen-20261105/）：16 条需整体重译（retranslate-list.md，orcs 1c73f145ab27/4ca4e02e13e6 互换对须同步重译），169 条 LOCAL 待执行器分批修，均待用户批准。
- 11-05/06 第六轮实机第三段（r6-opus，角色 Opus 10 级永久死亡，需新角色再测）：r6-opus-19..29 中 8 条在 0385 修复，0386–0388 盲审连带修 17 条（伤害吸收日志标签语序统一为「（X 抵消 %d 点）」、#Target# 空格、！#LAST#。双标点等），0389 收敛；r6-opus-25/29 为插件代码问题延后，21 advisory。Barrier 首行源串含「空格+TAB」，改该行会挂门禁 11，「最多」改由第二行表述。
- 11-06 Lore 单独审核收尾（用户「交给gemini 4进行重译」「局部修改需慎重，复审又有问题应考虑重译」）：Gemini 4 Argon 共整篇重译 34 条（筛查 16＋局部修改后复审仍有意思错误或执行器标 ESCALATE 的 18 条），见 evidence/quality/lore-retranslate-20261106/；169 条 LOCAL 由 codex 执行器分 9 块修（fixed 160、escalate 9），见 evidence/quality/lore-local-20261106/；盲审 0386–0421 收敛，队列空。规则：复审后仍有意思错误或问题遍布→重译；短条目单句或用词问题→原地改。lore 中 foot/feet 用「英尺/英寸」（曾在 Gemini 提示中误写「尺」，已全部更正）。0386 起漏跑的 strict/record 已于 0420 补记。
- 11-06 第七轮实机（r7-opus，兽人链锯屠夫，余烬怒火，10 级，7 条）已修并盲审收敛（0422–0424）：配件名模板去空格（不加「质」）、attach 统一「安装」、Not now→以后再说、植入物双句号；盲审连带修配件等级模板与标题一致（电击之触/伏特守卫/致命诱饵）、%s腕、背部支撑架。r7-01/03/07 为插件代码问题延后（裁决见 round7/adjudication.md）；用户 11-06：战斗日志 (%d 护盾吸收) 式短标签保持，6797/6801–6805 已改回。
- 11-06 第七轮第二段 r7-09/10/11 已修（0427 蒸汽发生器，0428–0429 收敛）。第八轮实机（r8-opus，半身人星月术士，主战役 9 级，7 条）：0430 修 01（用户选 C：弹药基础名去「一袋」）、03–07；02 盾牌 add_name 不经 `_t`，插件代码延后；0431 盲审 A 0 条，B 5 条均为投石索弹药「子弹→弹丸」，跨条目改名，用户 11-06「改成弹丸」，0432 统一（terminology shot＝弹丸），0433 盲审 0 条。法阵系未测（9 级前未解锁）。裁决见 round8/adjudication.md。第二段（12 级，法阵系已解锁并核对，暗影之阵实测）新增 08/09：0434 修占位符空格 7 处、以技能命名的伤害类型 8 处对齐技能名（healing light 治愈之光等），0435 盲审连带修传染撕咬「咬住」、绞杀施加日志与说明「勒住喉咙」，0436 收敛。区域名「德斯」在旧存档中仍显示，待新角色复核。
- 11-07 第九轮实机（r9-opus，人类散兵新存档，6 级，15 条）：新存档确认「德斯镇」等修复生效；0437 修 01/02/03/06/08/11/12/14/15（以牙还牙次数、投石索技能「弹丸」、抛射物方向、解除陷阱、护甲训练暴击、面色阴沉的斗士；Gemini 定名 Buckler Expertise＝格挡专精、lost defiler＝迷路的堕落术士），07（升级预览空格规则）、13（r3-sonnet-05 重复）驳回，04/05/09/10 插件代码延后；0438 盲审连带修 5 条（双倍射速、快速射击、连环炮击、两处换行数），0439 收敛。裁决见 round9/adjudication.md。
- 11-07 全职业／种族巡检（36 职业 × 轮换种族覆盖 18 种族；Opus→额度耗尽后改 Sonnet/DeepSeek，DeepSeek 长会话 429 后改每角色新开子代理）：第一批 68 条 → 0440 修 71 处（7 组改名经 Gemini：俯身闪躲、时空守护、梦境铁匠/梦境熔炉、坚石肌肤、大地藤蔓、奥术之盾/奥术岩石、空间之锚/空间系绳），0441–0444 收敛；第二批 51 条 → 0445 修 31 处，0446–0448 收敛。驳回多为说明与实现不符、现译贴合实现；延后插件代码：引擎折行拆数字、人偶短名截断、共享键 all 抗性行、main/off 武器组名、上游 %%%% 转义；advisory：Combat Veteran「战斗经验」待术语裁决。证据 evidence/quality/live-test-20261104/class-sweep/。
- 下一步：视用户指示发布 0.3.9 或再测（未覆盖：圣洁之阵/守护之阵/天体潮涌实战、工匠商店购买、深层区域／Boss、手札大部分）。再测前须重建测试插件。

**待用户决定／未完成：**

1. 最终分母冻结、补充行分类与最终候选的游戏场景验收（`evidence/full-review/release-20261013/m0/SCENARIOS.json`）。
2. 0.3.7 已于 2026-11-03 按用户指示发布（发布仓库 `d98780e`，由 `9fe51e84` 构建，13,242 条＝核心 7,781＋DLC 5,461），GitHub Release `v0.3.7` 已回下载核验，凭据 [`evidence/releases/addon-0.3.7.json`](evidence/releases/addon-0.3.7.json)。
3. 0168 已于 2026-11-04 实机测试中修复（policy 逐条放行）。另待决：17 条硬编码英文需插件 superload（H.Key、按键分组、成就分类、对话头像名等），（0.3.8 已发布）硬编码英文按用户 11-04 指示先记录暂不处理。
4. 无法在译文修正的上游问题（advisory）：Taint: Telepathy 持续回合写死 5、坍缩显示值为实际一半、防御投掷两处伤害实为同值、
   石化凝视实为震慑、暮光回响 action 不返回 true（疑似不进冷却）等，清单在 0241／0252／0253 的 maintenance 或 decision。
5. 残留行／死键候选（最终分母时处理）：0031 TooltipsData 旧键、0236 tome-orcs.lua DebugMain 旧 lore 副本；0036 超强七彩龙实体名待复核（拉克·肖译名已全库一致，无需再对齐）。
6. `AGENTS.md`、`docs/agent-workflow.md` 仍描述旧 Paseo 正式批次流程，尚未按轻量流程修订（规则文件，需用户授权）。

---

# 历史恢复入口（2026-10-13 全量发行审核，旧审计流程已于 R296 冻结）

M0、M1 已 DONE_VERIFIED 并提交。M2 当前 revision 有效 A=30、B=20。
窗口-02 十一条 target 修正已通过独立初审／最终全量复审、完整 17 项门禁含 build 和 DONE_VERIFIED，
本地提交 `241a069c7`；新增五条仅为同 source/tag 装备提示的运行键同步，既有 dirty 保留。
当前 ledger 为 round-v3，round-v1/v2 均被冻结；30,297 未改单元、57,879 补充项及 19A/9B 覆盖守恒。
window02r 十一条 fresh 当前 revision A/B 已闭合：核心3／Ashes8来源分组，四task各自完整17项门禁、
确认归档和 DONE_VERIFIED，新增11A/11B；下一步按既定顺序 p03s1 Cults 继续。实现复审不给生产覆盖。恢复检查：
`python3 -B tools/full_review.py check --directory evidence/full-review/release-20261013/round-v3`。
最终分母和最终候选游戏场景未闭合，连续授权仍有效，未外部写入。
详见 [执行状态](evidence/full-review/release-20261013/STATUS.md)。以下旧记录按其当时节点理解。

# 当前恢复入口（2026-10-13 全量发行复核 M0 探针完成、待复审闭合）

用户授权按 [全量发行复核计划](docs/full-translation-review-plan-20261013.md) 开始执行。当前 task `full-review-20261013-m1-entry` FIX cycle1：M0已DONE_VERIFIED并提交；M1代码与隔离验证已实现，A/B生产审核均为0，最终分母未冻结，M2仅准备237条未审。恢复先读 [M0 报告](evidence/full-review/release-20261013/m0/REPORT.md)、[基线](evidence/full-review/release-20261013/m0/BASELINE.json)、[M1-SPEC](evidence/full-review/release-20261013/m0/M1-SPEC.md)，由 ORCHESTRATOR 完成独立复审、裁决、状态闭合与提交；本段不宣称任务 DONE 或 child 已归档。

既有 12 条修正（11＋P01 用户裁决）已纳入基线，不计新轮已审。11 文件 loader 清点 30,308 次，审核单元/发行运行键分母未冻结。三个 DLC 的错误输入为外层 wrapper，包含 boot 子包并将 section 前缀翻倍；Ashes 的两项额外记录已定位到 boot init。改用真实 inner addon roots 后，原 extract 三次全部成功，999/2444/4493 及 manifest 原 hash 均一致。旧“未归因／需用户旧快照／停止 DLC”诊断撤回；exact root-layout、归因、doctor、corrected extract 及 smoke 探针原 bytes/hash 已嵌入 BASELINE，并提供便携 TOME_DLC_ROOT 配置和隔离 HEAD＋patch 重放配方。DLC commit 仍 unpinned，wrapper 与 corrected addon 逐文件取证清单明确分开。

Engine full与隔离publish/存储式zip通路通过；M0源码树binary启动退出127（动态库/ABI）为历史观察。后续主代理已用隔离官方1.7.6启动并核验prototype Engine早期locale、CJK、“图像设置”标题和原teae精确回退；这是能力PASS，最终candidate/三DLC玩法仍未测。最终候选完成后按 [最小场景](evidence/full-review/release-20261013/m0/SCENARIOS.json) 交付未测项，不提前豁免。这些游戏验收缺口按计划不阻断本地 M1 进入；M1 已实现并完成合并FIX，待 ORCHESTRATOR 同candidate两路复审闭合后继续；不启动生产审核或伪造 surface ISSUE，不借旧 done 抵本轮。未授权外部发行仓库写入/push/PR/发布。历史入口完整保留如下。

---

# 历史恢复入口（2026-10-12 修复窗口68 完成，168 个 successor 已在第406–408批审完）

用户 2026-10-12 先要求分析近期改动并评估能否对外发布，随后选择“先开 Magic 属性名修复窗口”。窗口68 已完成并推送：106 条 source 中 Magic 指属性、译文写作“魔法”的条目统一为界面属性名“魔力”（主游戏 78、Ashes 7、Cults 11、Orcs 10；译文 `19fd9ec0`，catalog `6ae69b9a…`，migration `6b99f6e0…`，详见 `evidence/quality/repair-window-68-20261012/PUBLICATION.md`）。复审中另修同批条目的 5 处旧错（Cults 彼世法术、Arcane Destruction 基础物理强度与当前加成、Orcs 光系伤害、3 条换行结构），cycle 4 收敛。窗口68 的全部 child 在证据提交前已由宿主确认归档，当前没有进行中的批次、窗口或 child。待办与待决：

1. 窗口68 的 168 个 successor（修复 106 条＋目录同步 62 条；目录同步的 62 条是 `c7ea0683b` 官方对照审核修订在 WP2-Lite 流程外改过的译文，窗口68 只做 catalog/migration 登记、未改译文）：第406批（`batch-266bad83c925bc67c3bf`）80 条：80 done / 0 repair_required，证据提交 `ae5d0a48`；第407批（`batch-be1e4f20608fd9ddf22b`）80 条：80 done / 0 repair_required，证据提交 `18e295ae`；第408批（`batch-b16d21ce8d7beaefe449`）8 条：8 done / 0 repair_required，证据提交 `20d724e0`；合计已审 168（168 done、待修 0），审核队列已无待审 successor。
2. 下一个修复窗口（69）积压 1 条：`tome-orcs.lua:1411` “造成大量光明伤害”应为“光系伤害”（窗口68 RE_REVIEW r1a1 同族发现）；另宿主补充 1 条：`5a0aebf5c0` Orcs 磁化射击（steam/other.lua:1637）三行行首补回 \t\t（第407批预扫）。
3. 待用户裁决：官方对照审核（`evidence/translation-audit/official-mechanics-20261009/`）经 GPT 6 Astra 核验仍有 pending 178／需裁决 15 项，其中 Magic 属性名一类已由窗口68 处理；Cults “咬一口”秒杀几率（M264，上游英文与实现矛盾）在窗口68 RE_REVIEW r3a1 再次被报，按 2026-10-03 撤回机制改写的决定记 advisory。
4. 对外发布仍停在 0.3.6；是否发 0.3.7 待用户决定（已于 2026-11-03 发布，见顶部）。

---

# 历史恢复入口（2026-10-06 窗口67 successor 已在第405批审完，0.3.6 已对外发布）

用户 2026-10-05 要求开始生硬描述扫描 C 档（对话与 lore），已完成并推送：1,446 条全部裁决，修复包 12–16 修正 485 处，DeepSeek 交叉复核后再修正 8 处；搁置的 21 条由主代理逐条查源码，用户同意后改 16 行（含同运行键同步 1 行），GPT-6.1 Sol 复核无异议。见[扫描报告](evidence/quality/awkward-scan3-20261003/REPORT.md)的“C 档”一节与[搁置项处理](evidence/quality/awkward-scan3-20261003/holds-c.md)。至此 A、B、C 三档全部完成。

用户随后要求发布新版本：0.3.4 已推送至发布仓库 `yutio8888/tome4-chn-mod`（提交 `3f031fa`，由本仓库 `aea17710` 构建，12,450 条＝核心 6,989＋DLC 5,461），GitHub Release `v0.3.4` 安装包已回下载核验。凭据见 [`evidence/releases/addon-0.3.4.json`](evidence/releases/addon-0.3.4.json)。

用户随后要求对 C 档润色“再走一轮生产复核”：迁移 `87fb6882…` 排入的 494 个 successor 已于第397–403批全部审完（478 done、待修 16）。队列清空时积压 16 条＋宿主补充 9 条，未达 20 条阈值；用户选择“修完后再发一个插件版本”，窗口66 已修复这 25 条（2026-10-05，译文 `fd7c6a61`，migration `defcd152…`，详见 `evidence/quality/repair-window-66-20261005/PUBLICATION.md`）。窗口66 的全部 child 在证据提交前已由宿主确认归档，当前没有进行中的批次、窗口或 child。按用户指示随后发布 0.3.5：发布仓库提交 `d2575eb`（由本仓库 `d6def5d9` 构建，12,450 条＝核心 6,989＋DLC 5,461），GitHub Release `v0.3.5` 安装包已回下载核验，凭据见 [`evidence/releases/addon-0.3.5.json`](evidence/releases/addon-0.3.5.json)。待办与待决：

1. 窗口66 的 25 个 successor 已在第404批（`batch-8a80c5f58e2462772813`）审完：25 done / 0 repair_required，证据提交 `599bfb7b`；审核队列已无待审 successor。
2. 用户随后选择“小窗口67并含 422 行”：窗口67 已修复 2 条（宿主补充 `9d3fc01bdf` 奎科加章节“安格列文”→“安格利文”；用户授权的 `fc55a88fd6` 即 `mod-tome.lua:422` 护送奖励日志，对齐同族选项写法），复审中另确认同一奎科加条目的 2 处错误并一并修复（译文 `0de585f6`，migration `a0f4f220…`，详见 `evidence/quality/repair-window-67-20261005/PUBLICATION.md`）。窗口67 的全部 child 在证据提交前已由宿主确认归档。
3. 窗口67 的 2 个 successor 已在第405批（`batch-0009fb571152fc15b9a2`）审完：2 done / 0 repair_required，证据提交 `b674f274`；审核队列已无待审 successor。下一个修复窗口（68）积压 0 条，未达 20 条阈值；后续开窗或暂停待用户决定。
4. 按用户指示发布 0.3.6：发布仓库提交 `6f5a071`（由本仓库 `baf532e1` 构建，12,451 条＝核心 6,990＋DLC 5,461；核心多 1 条是护送奖励日志，改后不再与官方中文 locale 相同），GitHub Release `v0.3.6` 安装包已回下载核验，凭据见 [`evidence/releases/addon-0.3.6.json`](evidence/releases/addon-0.3.6.json)。

---

# 历史恢复入口（2026-10-04 窗口65 successor 已在第396批审完，0.3.3 已对外发布）

用户 2026-10-03 要求“重新再走一轮生产复审流程”，已全部审完：第383–395批共 13 批、**1019 个 successor**（migration `22b293c4…` 的 993 个＋窗口64 migration `629e3b1e…` 的 26 个），队列余 0。来源见[迁移记录](evidence/quality/maintenance-reaudit-20261003/README.md)，每批证据在 `evidence/quality/production-batches/<batch>-host-evidence/`。

结果：完成 981 条，host-block 4 条（`mod-tome/load.lua` 段已登记死键），确认待修 34 条。其中 25 条已在窗口64 修复并推送（`a2671655`），其余 9 条与宿主补充 2 条已在窗口65 修复（2026-10-04，译文 `9079821a`，migration `e437cb51…`，详见 `evidence/quality/repair-window-65-20261004/PUBLICATION.md`）。宿主裁决观察：confirmed 57 行、refuted 14 行、advisory 12 行（surface 与 contextual 同判的条目各记一行）。最后一批的收口提交是 `54a2cc9e`。窗口65 的 11 个 successor 已在第396批（`batch-24e16a565d59243f9467`）审完：11 done / 0 repair_required，证据提交 `3c2c3458`。

**用户 2026-10-03 指示：本轮完成后暂停并撰写 handoff；2026-10-04 用户指示开窗口65（“现在开”），窗口已完成；2026-10-04 用户指示“开始审核，审核后即可对外发布”，第396批已审完。** 第396批的 child 均已确认归档，当前没有进行中的批次、窗口或 child。待办与待决：

1. 对外发布已完成：0.3.3 已推送至公开发布仓库 `yutio8888/tome4-chn-mod`，提交 `9d1c9ac`；GitHub Release `v0.3.3` 安装包已回下载核验。凭据见 [`evidence/releases/addon-0.3.3.json`](evidence/releases/addon-0.3.3.json)。
2. 生硬描述扫描 C 档仍待用户决定。
3. 下一个修复窗口（66）积压 0 条，未达 20 条阈值；审核队列已无待审 successor。

`tome-possessors.lua`、`tome-items-vault.lua` 的 13 条改动不在目录内，没有进入复审。
---

# 历史恢复入口（2026-10-03 生硬解释调整完成）

机制改写撤回之后，用户要求调整补充扫描清单；已完成 16 条（13 条英文外扩写、3 条措辞精简），4 条排除项未动。两轮独立复审通过，适用门禁及 DONE_VERIFIED 通过，3 次 child dispatch 全部确认归档。见 [调整完成记录](evidence/quality/awkward-explanations-adjust-20261003/SUMMARY.md) 与 [扫描记录](evidence/quality/awkward-explanations-scan-20261003/REPORT.md)。

本次仅本地译文和证据交付，对外 0.3.2 未变。后续英文／源码差异处理原则及对外版本仍待讨论，无新机制改写、连续批次、规则修改或发布授权。用户无关改动保留。

---

# 历史恢复入口（2026-10-03 机制改写撤回完成）

用户要求撤回本轮因英文与代码不一致而做的机制改写，保留普通翻译修正；已在翻译仓库完成。165 条盘点中修改137条（122条撤回、15条混合），另28条完整保留普通修正。独立范围复审、修复后的完整终审与适用运行验证通过，任务 DONE_VERIFIED，6次 child dispatch 全部确认归档。

详见 [撤回完成记录](evidence/quality/mechanics-rollback-20261003/SUMMARY.md) 和 [后续讨论建议](evidence/quality/mechanics-rollback-20261003/WITHDRAWAL-DECISION.md)。本次只提交本地撤回及证据，对外0.3.2仓库、标签、Release和资产未动。下一步与用户讨论英文／源码差异的处理原则及对外版本；没有新机制改写、规则修改或发布授权。MMR-026“生命汲取（物理）”与UPSTREAM054撤销误报决定保留，用户无关改动保留。

下文为历史交接，旧连续推进指令、未决事项和采用状态均以本段及新撤回记录为准，不得据旧记录自动续跑。

---

# 当前恢复入口

第014主包及暮光回响两条伴随包均已DONE_VERIFIED；累计135/169原claim，14/18主包，3个附属任务。主包提交5bc6d339；伴随包准备提交后连续015—018。MMR-026术语决定仍待既有答复。全部child已确认归档，无push/PR/发布授权。

详见 evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md。用户无关改动保留。

---

# 当前恢复入口

第014主包9条已DONE_VERIFIED，累计134/169原claim、14/18主包；准备提交后先运行已授权暮光回响两条companion，再015—018。所有8次派发已归档。用户已批准撤销args_order误报；最终有效终审全部9条OK。

详见 evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md。保留用户无关改动，无push/PR/发布授权。

---

2026-10-03更新：用户已明确批准撤销参数顺序误报并继续。收束检查发现宿主给RE_REVIEW及FINAL_REVIEW重复cycle1/attempt1，旧final已保留为无效派发诊断（raw不改、用户裁决不改）；fresh FINAL_REVIEW attempt2 601d3a67-2732-467c-a8ff-169b39bf16a9运行中，candidate未变。完成后收束主包→companion→015—018。

# 当前恢复入口

第001—013包完成，125/169原claim；第014主包9条已修并通过完整门禁及RE_REVIEW，FINAL_REVIEW对等离子飞弹提出与上一轮相反的缺失args_order疑点。宿主已证伪：冻结context及实际DLC产物均为{3,1,2,4,5}，固定formatter探针正确。按AGENTS同revision复审分歧规则WAIT_USER，等待是否撤销误报、保持候选并据宿主裁决收束。全部child已确认归档；无活动执行者。第014未DONE/未提交。

证据：package-014-review-wait/DECISION.json、published-args-014-proof.json、format-runtime-014-proof.json及task/reviews/dispatch-evidence。用户此前9＋2拆分授权持续有效，不重问；主包若获准收束后先做014-companion两条，再015—018。伴随包prepare helper已准备但未执行。用户无关文件不动；无push/PR/发布授权。

---

# 当前交接入口（2026-10-02）

当前工作是[修改译文机制修正任务](evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md)：已完成 **13/18 包、125/169 个原始claim**。第013包提交 `0c739d7f`，独立复审、终审与完整门禁通过，5个child均已归档；用户已回复“请继续”，用户已批准第014包拆为9＋2条，当前正在执行拆分；主9条及暮光2条伴随包分别完整验证后提交。当前细节见任务交接。下一步及MMR-026待决术语事项以该交接为准。

本轮用户要求更新handoff，已记录当前状态。既有连续修正范围保持；本任务未获push／PR／发布授权。下文保留第382批生产队列历史，其中旧授权、模型配置和“无未决项”等结论仅属当时任务，不覆盖当前机制修正交接。

---

# 翻译审核当前交接

更新时间：2026-10-12（第408批已 finalize，窗口68 successor 已审 168/168、余 0；窗口69积压 1 条）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。上一版交接（含第273–372批逐批结果表、
窗口27修复清单与 2026-09-24 工具维护记录）已归档为
[`deprecated/docs/review-handoff-20260929-batch372.md`](deprecated/docs/review-handoff-20260929-batch372.md)，
更早的版本见 `git log -p -- handoff.md`。当前会话授权优先。

## 一、当前状态

- 2026-09-30：用户恢复工作，要求用 Gemini 3.8 Flash 快速复核 09-21 以来修改过的 1190 条译文（证据提交 `c4728694`，确认 83 条），随后“请合并修复”开窗口57。是否连续审核第373批以当前会话指示为准。
- 2026-10-01：审核队列耗尽、积压 3 条，用户选择“开小窗口修这 3 条”，开窗口58。
- 2026-10-01：第376批后按维护者要求暂停；用户“先补术语库”（`8e2fae4e`，181 行），三方讨论改为 gpt-6-astra／opus-5-5／gemini-3.8-flash，同意统一 21 个名称并开窗口59；裁定 Phoenix＝凤凰、“恢复失衡值”保留不改。
- 2026-10-01：用户裁定 deeprock 技能树改“深岩”（Deeprock Form 保持“深岩形态”），并要求一并修复 Korbek 实验笔记标题等非阻断问题，开窗口60。
- 2026-10-01：审核队列清空后，用户要求系统性分析死亡信息表（`cd2d0d7e`）；同意把 12 条句式与拼接缺陷并入积压，开窗口61；随后裁定 pending #50（killer_message 改凶手主语）与 #51（dark Master→黑暗领主）均采用 B，排入窗口62。窗口62 已于同日完成并推送。
- 2026-10-05：生硬描述 C 档完成并发布 0.3.4 后，用户要求“再走一轮生产复核”。迁移 `87fb6882…`（catalog `47745ecc…`）把 C 档修复包、交叉复核修正与搁置项处理涉及的 494 个 successor 排入队列（证据 `evidence/quality/maintenance-reaudit-20261005/`）。
- 审核已闭合至第 **408** 批（`batch-b16d21ce8d7beaefe449`）：8 条，8 done / 0 repair_required。
  窗口68 successor 审核 8 条（Orcs 8）：surface 8 OK / 0 ISSUE；无 deep；无观察；无新增修复，窗口69积压 1；余 0 个 successor。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `20d724e0f505a8926ab57062ed24b8ee320c508e` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **68**：窗口68（用户 2026-10-12 授权的 Magic 属性名统一 106 条，译文 `19fd9ec0`，migration `6b99f6e0…`；另以目录同步登记 `c7ea0683b` 的 62 条），106＋62 个 successor 已在第406–408批审完。此前窗口66（第397–403批第二轮重新复审确认 16 条＋宿主补充 9 条，译文 `fd7c6a61`，migration `defcd152…`；25 个 successor 已在第404批审完）与窗口67（宿主补充 1 条＋用户授权 1 条，译文 `0de585f6`，migration `a0f4f220…`）均已修复；窗口67 的 2 个 successor 已在第405批审完（2 done / 0 repair_required）。
- 队列（第372批 finalize 后实测）：eligible 29828，surface 覆盖 29828/29828，done 29812
  （surface_only 28718＋deep_reviewed 1094），pending_repair 0，queued 0，**blocked 16**：
  - 10 条死键／冻结 MISS（上游改串未重生 locale key 等，已 host-block 登记，不动）；
  - 5 条按裁决保留现译、但工具没有“不改”收口路径（含 petty gods `b63b2d6946`、cleaved `922c0f9665`）；
  - 1 条 Toxic Death `aeae08fe72`，已裁定改名，列入窗口57积压。
- 待用户集中审阅的争议条目：[`pending-user-review.md`](evidence/quality/pending-user-review.md) 共 51 项，**全部已裁决**，
  无未决项。

| 批次 | batch id | 结果 | surface（gpt-6-sol） | contextual（opus-5-5） | 裁决 |
| --- | --- | --- | --- | --- | --- |
| 368 | `batch-3cfa49c3b0ee7cc07337` | 49 done / 6 repair | 40 OK / 15 ISSUE | 11 OK / 4 ISSUE | 7 confirmed / 8 refuted / 4 advisory |
| 369 | `batch-ee4d1e47a33a7b8cc828` | 18 done / 1 repair | 14 OK / 5 ISSUE | 4 OK / 1 ISSUE | 2 confirmed / 3 refuted / 1 advisory |
| 370 | `batch-6bd34a6ffb2c19accea1` | 2 done / 0 repair | 2 OK / 0 ISSUE | 0 OK / 0 ISSUE |  |
| 371 | `batch-80b3265ec45a9b152247` | 7 done / 0 repair | 6 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 refuted |
| 372 | `batch-c9ca70f29bc203b33050` | 29 done / 0 repair | 27 OK / 2 ISSUE | 2 OK / 0 ISSUE | 2 refuted |
| 373 | `batch-eb93936e38c73186d222` | 78 done / 2 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 2 confirmed / 6 refuted / 6 advisory |
| 374 | `batch-2e8beab0b2f9b05c4c94` | 6 done / 1 repair | 6 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 confirmed |
| 375 | `batch-9da6a86a32b67cc82ddf` | 79 done / 1 repair | 79 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 confirmed |
| 376 | `batch-93dd0d869b4d3e8058dc` | 77 done / 3 repair | 72 OK / 8 ISSUE | 7 OK / 1 ISSUE | 4 confirmed / 3 refuted / 2 advisory |
| 377 | `batch-f66787c8049fa3542bf3` | 78 done / 2 repair | 75 OK / 5 ISSUE | 4 OK / 1 ISSUE | 3 confirmed / 2 refuted / 1 advisory |
| 378 | `batch-aab3f1f803f7e019bc0d` | 76 done / 3 repair | 72 OK / 8 ISSUE | 5 OK / 3 ISSUE | 6 confirmed / 5 refuted |
| 379 | `batch-0c287579511c7ffee8a8` | 76 done / 4 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 5 confirmed / 9 refuted |
| 380 | `batch-1c8107aa6a8d3b70ae53` | 38 done / 0 repair | 35 OK / 3 ISSUE | 3 OK / 0 ISSUE | 2 refuted / 1 advisory |
| 381 | `batch-4584eb6ddb5e3110acab` | 74 done / 1 repair | 74 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 confirmed |
| 382 | `batch-554490d4847b278842b9` | 1 done / 0 repair | 1 OK / 0 ISSUE | 0 OK / 0 ISSUE |  |
| 383 | `batch-fe24f4f2a420a35a72cc` | 80 done / 0 repair | 79 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 advisory |
| 384 | `batch-e63ec4963b48bd6eee9a` | 77 done / 3 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 5 confirmed |
| 385 | `batch-ea91b26c880d0eb75606` | 75 done / 4 repair | 76 OK / 4 ISSUE | 1 OK / 3 ISSUE | 7 confirmed |
| 386 | `batch-aa1fb47399d4777a57f0` | 78 done / 2 repair | 76 OK / 4 ISSUE | 2 OK / 2 ISSUE | 4 confirmed / 1 refuted / 1 advisory |
| 387 | `batch-96dcbe7098ab7a8a87f7` | 78 done / 1 repair | 76 OK / 4 ISSUE | 3 OK / 1 ISSUE | 2 confirmed / 2 refuted / 1 advisory |
| 388 | `batch-563560854ae20160c9d5` | 76 done / 3 repair | 76 OK / 4 ISSUE | 3 OK / 1 ISSUE | 4 confirmed / 1 advisory |
| 389 | `batch-8ddbfa00da4d0d50cdaa` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 refuted |
| 390 | `batch-f199ae8241b6a0369acf` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 advisory |
| 391 | `batch-ac27e658ed64b3f7f270` | 71 done / 8 repair | 71 OK / 9 ISSUE | 3 OK / 6 ISSUE | 14 confirmed / 1 refuted |
| 392 | `batch-3506bffc1094e8909c28` | 78 done / 2 repair | 75 OK / 5 ISSUE | 4 OK / 1 ISSUE | 3 confirmed / 1 refuted / 2 advisory |
| 393 | `batch-af9aadc82f05ae27f3d8` | 79 done / 1 repair | 76 OK / 4 ISSUE | 1 OK / 3 ISSUE | 2 confirmed / 5 refuted |
| 394 | `batch-f4001cace434a973dcfb` | 76 done / 4 repair | 72 OK / 8 ISSUE | 7 OK / 1 ISSUE | 5 confirmed / 3 refuted / 1 advisory |
| 395 | `batch-4158eeb47c02308774eb` | 57 done / 2 repair | 55 OK / 4 ISSUE | 2 OK / 2 ISSUE | 3 confirmed / 3 advisory |
| 396 | `batch-24e16a565d59243f9467` | 11 done / 0 repair | 10 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 refuted |
| 397 | `batch-eb3fc24942d20a7b5e71` | 78 done / 2 repair | 75 OK / 5 ISSUE | 3 OK / 2 ISSUE | 4 confirmed / 3 advisory |
| 398 | `batch-62c5a69973fcdab9c29f` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 advisory |
| 399 | `batch-32839b9d4e0ed9f6554b` | 79 done / 1 repair | 78 OK / 2 ISSUE | 1 OK / 1 ISSUE | 2 confirmed / 1 refuted |
| 400 | `batch-2fd158c709697a888ae1` | 77 done / 3 repair | 74 OK / 6 ISSUE | 3 OK / 3 ISSUE | 6 confirmed / 2 refuted / 1 advisory |
| 401 | `batch-58d155a7410203c41728` | 77 done / 3 repair | 70 OK / 10 ISSUE | 7 OK / 3 ISSUE | 5 confirmed / 1 refuted / 7 advisory |
| 402 | `batch-fd4663c4b4a995cd5928` | 76 done / 4 repair | 74 OK / 6 ISSUE | 3 OK / 3 ISSUE | 6 confirmed / 3 advisory |
| 403 | `batch-9ac9ee56fc05e6b82dbe` | 13 done / 1 repair | 12 OK / 2 ISSUE | 0 OK / 2 ISSUE | 2 confirmed / 2 advisory |
| 404 | `batch-8a80c5f58e2462772813` | 25 done / 0 repair | 25 OK / 0 ISSUE | 0 OK / 0 ISSUE | — |
| 405 | `batch-0009fb571152fc15b9a2` | 2 done / 0 repair | 2 OK / 0 ISSUE | 0 OK / 0 ISSUE | — |
| 406 | `batch-266bad83c925bc67c3bf` | 80 done / 0 repair | 73 OK / 7 ISSUE | 7 OK / 0 ISSUE | 7 refuted |
| 407 | `batch-be1e4f20608fd9ddf22b` | 80 done / 0 repair | 68 OK / 12 ISSUE | 12 OK / 0 ISSUE | 12 refuted |
| 408 | `batch-b16d21ce8d7beaefe449` | 8 done / 0 repair | 8 OK / 0 ISSUE | 0 OK / 0 ISSUE | — |

每批证据摘要在 `evidence/quality/production-batches/<batch>-host-evidence/summary.md`。

## 二、授权与节奏（用户指示，现行）

- 2026-09-23：持续推进审核，不需逐批确认；有争议的条目列入 pending，等用户集中审阅。
- 2026-09-24：修复先记录，**积压达到 20 条或以上再开一个合并修复窗口**。审核队列耗尽而积压不足 20 时，
  询问用户是开小窗口还是暂停。
- 每批（或每个窗口）完全收口后 push；批次进行期间不得提交任何东西。审核外发与 push 无需再次询问。
- 2026-09-25：修复窗口 `max_cycles` 默认 5（STATE 同时写 `max_cycles_user_authorized=true`）；reviewer 可写 `/tmp`
  scratch，仓库与工作区写入仍违规。
- 2026-09-27：纯名称类 pending 先双向查冲突，再由 Gemini 3.8 Flash 裁决并报告；非名称类仍逐条问用户。
  antigravity 认证失败时改用 Paseo 的 `pi/cpa/gemini-3.8-flash-high` 通道（2026-09-29 实测可用）。
- 审核模型：surface `codex/gpt-6.1-sol`（medium，auto-review），contextual `claude/claude-opus-5-5`（medium，auto）；
  修复 EXECUTOR `codex/gpt-5.6-sol`；修复窗口 FINAL 用 Claude Opus 5.5。
- 2026-09-30：用户指示此后凡用 GPT-6-Sol 处一律改用 `codex/gpt-6.1-sol`（显式 thinking medium）；Codex 0.159.1 原生会话已纳入 harvest 白名单（`88e29cf9`）。

## 三、下一步

1. **第二轮重新复审已完成**（第397–403批，494/494：478 done、待修 16）。窗口66 已修复，其 25 个 successor 已在第404批审完（25 done / 0 repair_required；surface 全 OK、无 deep 条目，按第360批先例走 surface-only 路径，派生件 `$C/finalize_host_gen_404.py`、`/tmp/mkfin_404.py`、`/tmp/handoff_gen_404.py`、`$C/close_tpl_404.sh`）；窗口67 的 2 个 successor 已在第405批审完（2 done / 0 repair_required；同样走 surface-only 路径，派生件 `$C/finalize_host_gen_405.py`、`/tmp/mkfin_405.py`、`/tmp/handoff_gen_405.py`、`$C/close_tpl_405.sh`）；窗口68 的 168 个 successor 自第406批起审核（派生件 `$C/finalize_host_gen_w68.py`／`_w68so.py`（surface-only）、`$C/mkfin_w68.py`、`$C/handoff_gen_w68.py`、`$C/close_tpl_w68.sh`，进度 `$C/w68-progress.json`）；本轮派生脚本见 `$C/reaudit2-helpers/`（start_re2.sh、derive_re2.sh、mkfin_re2.py、backlog66.json），收口用 `finalize_host_gen_re2.py` 与 `close_tpl_re2.sh`。
   窗口67 的派生件在 `.artifacts/i18n/repair-w67-20261005/`（rewrites.py、setup_window67.py、freeze_review.py、wd.sh、w67-tr.sh、w67-close.sh、w67-scope.tmpl、make_handoff_next.py），下一个窗口可从此派生；handoff 由宿主写好全文、publication child 核对基线 SHA 后整份替换。
   本轮新增经验（第392–395批）：
   - 一批有多个 contextual run 时，`finalize_host_gen_re.py` 与 `/tmp/mkfin_re.py` 已能处理；`close_review<N>.py` 的 `for run in (...)` 仍须按 run 数手改。
   - Orcs、Cults 等 DLC 死键（如 DebugMain section 的 lore 副本）带快照身份，不能 host-block；按第353/368批先例照常审核，被指出的问题记 advisory，并核对生效行。
   - contextual child 因 Claude 会话额度用尽而无输出时：harvest 会拒收，改用 `review_lifecycle.py reject --notified --capture <terminal> --evidence <证据>` → archive-intent → archive → archive-confirm；然后按 attempt 2（`full-001`，`retry_of`）重派，并在 snapshot 脚本中加入 `{batch}-*-rejection-evidence` 收录。fin 中可用 `contextual_reviewer_en` 覆盖 reviewer 描述（第395批先例）。
   - 宿主可对 workset 做 LF／TAB／全角空格的预扫描，这类问题 surface 常漏。没被任何 lane 指出的，只能经 `review<N>-extra.json` 作为宿主补充登记（第394批先例）。
2. 窗口 67 已完成（2 条：主游戏 1、Cults 1）：宿主补充 `9d3fc01bdf`（Cults 奎科加章节，源文 records of Anglowen，“安格列文”→“安格利文”，按 terminology/places.tsv:20）＋用户 2026-10-05 授权的 `fc55a88fd6`（`mod-tome.lua:422` 护送奖励日志“%s技能 %s（+%d 级）”，对齐 425 行与 tome-orcs.lua:582），新译文由宿主写定、EXECUTOR 逐字替换；窗口内复审另确认奎科加条目的 2 处错误并一并修复。复审路径：REVIEW r0a1（gpt-6.1-sol）1 OK／1 ISSUE，确认忠实性 1 条（奎科加章节 librarians 被译作“记录者”）＋宿主同条确认 1 条（might be 被写成“其实是”），execute-02 → RE_REVIEW r1a1 2/2 OK → FINAL f1a2（Opus 5.5）2/2 OK；第 1 轮收敛（max_cycles 5），无无效尝试；门禁 17/17。详见 `evidence/quality/repair-window-67-20261005/PUBLICATION.md`。
   窗口66（第二轮重新复审确认 16 条＋补充 9 条，第 3 轮收敛）详见 `evidence/quality/repair-window-66-20261005/PUBLICATION.md`；窗口65（重新复审确认 9 条＋补充 2 条）详见 `evidence/quality/repair-window-65-20261004/PUBLICATION.md`；窗口64 详见 `evidence/quality/repair-window-64-20261003/PUBLICATION.md`；窗口63（意志之力 maces 1 条）详见 `evidence/quality/repair-window-63-20261001/PUBLICATION.md`；窗口62 教训：killer_message 被 `" "..src.killer_message` 拼在凶手名后，译文不得以标点起头。
   窗口58遗留的 `2822ed0142` 食人魔化歌意译仍待 successor 审核时再评估。
   下一个修复窗口（69）积压 **1** 条（窗口68后重新计数，Orcs 1＋宿主补充 Orcs 1）：`tome-orcs.lua:1411` “造成大量光明伤害”应为“光系伤害”（窗口68 RE_REVIEW r1a1 同族发现）；另宿主补充 1 条：`5a0aebf5c0` Orcs 磁化射击（steam/other.lua:1637）三行行首补回 \t\t（第407批预扫）。 主游戏 `mod-tome/load.lua` 段的奎科加旧版副本（`e4824491182e`）是已登记死键（`batch-ac27e658…` 中经 host-block 放行），译文不生效，与 Cults 现行条目措辞不同步属预期，不登记。
   第408批计时（实测，投影缓存 on）：start 2.2 s；adjudication（surface-only）＋prepare-evidence（含 17 项门禁）194.2 s；finalize 198.2 s。
3. 窗口56的教训：长篇 lore 进窗口后每轮复审都会冒出旧错，第二轮起宿主应整条对照源文一次补齐；
   Opus FINAL 截断输出记 INVALID 后 attempt+1 重派，不计 max_cycles。

## 四、环境备忘

- 宿主工作目录 `.artifacts/i18n/continuation-20260923`（已 gitignore），Paseo workspace `wks_420314270844170b`；
  跑门禁或收口前 `export TOME_PASEO_WORKSPACE=wks_420314270844170b I18N_PROJECTION_CACHE=on`，并从 PATH 去掉 `/opt/agents/bin`。
- 上游源码 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；DLC 源码在
  `/workspace/tome4-dlcs/<component>`（仓库与 commit 未固定）。子 agent 看不到上游检出，
  它们报“commit 不存在、证据不足”时由宿主自查。
- 未跟踪文件 `.ai/consult/`、`recipe` 与旧的 `evidence/quality/production-batches/*-source-workset.json`（15 个）
  是既有遗留，保持不动。
- 发布插件：最新 0.3.4（2026-10-05，tome4-chn-mod `3f031fa`，对应本仓库 `aea17710`），凭据见 `evidence/releases/addon-0.3.4.json`。
- 历史保留边界：`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 不要打开 reviewer 的 agent tab（会清掉 attentionReason，harvest 失败只能整批 abandon）。

## 2026-10-13 M1 实现恢复入口

`tools/full_review.py` 与 `tools/i18nlib/{full_review,release_candidate}.py` 已实现离线入口。恢复先 `check --directory evidence/full-review/<round>`，不导入历史 done。M0 已提交 `74b81c8b4`；本次 EXECUTOR 不写 `.ai`、不 stage/commit，不创建 child。当前真实生产 A/B=0，分母未冻结。实现夹具、真实候选、两种 Engine VFS 结构安装回退与门禁日志均在忽略 `.artifacts/`；受跟踪 [M1 报告](evidence/full-review/release-20261013/m1/REPORT.md) 区分结构验证与尚未测的最终 Engine/game/GUI。下一步由 ORCHESTRATOR 独立 normal/senior 复审、裁决、任务闭合及生成正式 ledger，再进入 M2。

## 2026-10-13 M1 FIX cycle1 恢复

EXECUTOR m1-executor-04合并解决宿主11项accepted；范围仍为原11文件，未stage/commit/child，
保留全部既有dirty。复审先看[M1 REPORT](evidence/full-review/release-20261013/m1/REPORT.md)与
[task-gates/继承/发行绑定说明](i18n/README.md#全量轮次入口m1离线)。fresh候选`m1-fix-r1`基于
clean `6f5a071f81ce4e0d1312f89f32cd04a2c76efe08`，assemble/publish/Engine full/smoke和bare/teae
install/restore已跑；旧m1-delivery未改。report先冻结再运行完整gate，不在gate期间追加结果；
本dispatch最终receipt由ORCHESTRATOR记录。后续normal/senior复审、提交/DONE与真实生产台账
由ORCHESTRATOR负责；A/B仍0、分母未冻、237条draft不计已审，M4仍要exact最终candidate实测。
