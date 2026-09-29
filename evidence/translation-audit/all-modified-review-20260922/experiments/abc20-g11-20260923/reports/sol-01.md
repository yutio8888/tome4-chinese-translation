以下判定只针对冻结的 40 条译文，以及本包中哈希匹配的 Cults DLC 公开源码快照。该 DLC 的源码仓库和 commit 未固定；快照与目标游戏版本是否完全对应，仍待确认。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03573 | 未发现问题 | 伤害、时长及疾病加伤一致 |
| entry-03574 | 未发现问题 | 豁免、恐惧及抗性穿透一致 |
| entry-03575 | 未发现问题 | 双重施加条件与目标一致 |
| entry-03576 | 存在问题 | C01：漏掉“处于冷却中”的限定 |
| entry-03577 | 未发现问题 | 日志语义与标记一致 |
| entry-03578 | 未发现问题 | 黑洞范围、成长及伤害一致 |
| entry-03579 | 未发现问题 | 增益与反冲代价一致 |
| entry-03580 | 未发现问题 | 链接说明一致 |
| entry-03581 | 存在问题 | C02：操作说明漏掉技能 |
| entry-03582 | 存在问题 | C03：两次近战攻击未明确表达 |
| entry-03583 | 未发现问题 | 距离、抗性及纹身位数量一致 |
| entry-03584 | 未发现问题 | 震慑与共享疯狂效果一致 |
| entry-03585 | 未发现问题 | 三项强度削减及叠加上限一致 |
| entry-03586 | 未发现问题 | 参数重排正确 |
| entry-03587 | 未发现问题 | 额外层数、幻象几率及伤害一致 |
| entry-03588 | 存在问题 | C04：裂隙爆炸限制的范围译错 |
| entry-03589 | 未发现问题 | 操作提示一致 |
| entry-03590 | 未发现问题 | 失败日志一致 |
| entry-03591 | 未发现问题 | 日志及颜色标记一致 |
| entry-03592 | 未发现问题 | 抵抗传送的日志一致 |
| entry-03593 | 未发现问题 | 传送、伤害及反冲一致 |
| entry-03594 | 存在问题 | C05：彼世技能误称虚空法术 |
| entry-03595 | 未发现问题 | 效果及持续时间一致 |
| entry-03596 | 未发现问题 | 武器攻击与两种伤害一致 |
| entry-03597 | 未发现问题 | 强化后名称格式一致 |
| entry-03598 | 未发现问题 | 视线提示一致 |
| entry-03599 | 未发现问题 | 护盾参数重排正确 |
| entry-03600 | 存在问题 | C06：全局速度术语不符 |
| entry-03601 | 未发现问题 | 技能失败日志一致 |
| entry-03602 | 存在问题 | C07：全局速度术语不符 |
| entry-03603 | 未发现问题 | 菜单提示一致 |
| entry-03604 | 存在问题 | C08：凭空加入器官破损 |
| entry-03605 | 存在问题 | C09、C10：动态说明显示错误；人群范围改变 |
| entry-03606 | 未发现问题 | 禁用后缀本身及颜色标记一致 |
| entry-03607 | 未发现问题 | 拉动失败日志一致 |
| entry-03608 | 未发现问题 | 效果数量及持续时间一致 |
| entry-03609 | 未发现问题 | 召唤空间提示一致 |
| entry-03610 | 未发现问题 | 轻甲条件一致 |
| entry-03611 | 未发现问题 | 伤害吸收日志及标记一致 |
| entry-03612 | 存在问题 | C11：漏掉最多四颗的上限 |

### C01 | entry-03576 | 存在问题

原文限定为“one of your talents **on cooldown**”，译文只有“你的一个技能的冷却时间将减少 %d”。这漏掉了只能选取当前处于冷却中的技能，容易被理解为降低任意技能的冷却设定。快照中预言效果遍历施法者的 `talents_cd`，再调用 `alterTalentCoolingdown`；见 [doom.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/doom.lua:415) 与 [timed_effects.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/timed_effects.lua:896)。

### C02 | entry-03581 | 存在问题

原文末句说更改恐魔的“equipment **and talents**”前，要先转交装备，再取得控制权。译文末句仅说“试图改变其装备时”，漏掉更改技能也属于这段操作说明的范围。其可完全控制的设置见 [friend-of-the-worm.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:237)，原说明见同文件第 425–438 行。

### C03 | entry-03582 | 存在问题

原文“**both** teleport … and **make a melee attack**”指玩家与蠕虫合体各自攻击。译文“你和蠕虫合体同时传送……造成 %d%% 近战伤害”未交代是各作一次攻击，可能被读成合计一次伤害。快照中玩家与伙伴分别调用 `attackTarget`，见 [friend-of-the-worm.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:492) 的第 492–507 行。

### C04 | entry-03588 | 存在问题

原文限制目标“at once”不能被**多次裂隙爆炸**击中；译文“一次湮灭不能多次伤害同一目标”把跨爆炸的限制说成单次爆炸内部的重复伤害。快照的爆炸投射使用 `RIFT_EXPLOSION`，其投射器以目标的 `turn_procs.rift_explosion` 阻止同一回合再次受此类爆炸伤害；见 [nether.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/nether.lua:128) 和 [damage_types.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults/tome-cults/data/damage_types.lua:39)。

### C05 | entry-03594 | 存在问题

原文的“your next **Nether** spell”被译为“下一次**虚空**法术”，改变了可触发强化的技能类别。快照将相关技能归在 `demented/nether`，另有独立的 `demented/void` 类别；本包术语子集也将 `nether` 技能类别记为“彼世”。见 [nether.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/nether.lua:22)、[void.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/void.lua:20)。

### C06 | entry-03600 | 存在问题

原文“global speed”译作“整体速度”。冻结术语子集对 `tformat` 技能说明中的该属性明确要求“全局速度”，并明确排除“整体速度”。快照的时空漩涡应用 30% 的速度降低，见 [rift.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/rift.lua:425)。

### C07 | entry-03602 | 存在问题

原文“increasing their global speed”再次译作“增加他们 %d%% 的整体速度”，与同一条明确适用的 `tformat` 术语要求不符。快照通过 `global_speed_base` 增加召唤物速度，见 [rift.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/rift.lua:538)。

### C08 | entry-03604 | 存在问题

原文只说受害者内在的“something breaks”，继而让施法者侵入其心智；译文明确写成“**内部器官不断破损**”。器官破损是新增的具体生理事实，原文和该技能的窃取逻辑都没有给出这一信息。见 [slow-death.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/slow-death.lua:100)；同文件第 44–63 行处理可窃取技能。

### C09 | entry-03605 | 存在问题

原文将第一个 `%s` 直接接在“stats”后，供禁用后缀插入；译文却写成“当前属性**为 %s :**”。后缀为空时显示“属性为 ：”，后缀非空时显示“属性为 ，由于副手非空……：”，两种状态下句子都被插值位置破坏。`tformat` 的实参选择及后缀见 [tentacles.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/tentacles.lua:66) 第 66–80 行；entry-03606 是该后缀的冻结译文。

### C10 | entry-03605 | 存在问题

原文带引号的“‘civilized people’”指“文明人”这一人群，译文改为“普通人”，改变了伪装效果所描述的人群范围。该措辞位于触手外观的心灵遮掩说明中，见 [tentacles.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/tentacles.lua:72) 第 72–79 行。

### C11 | entry-03612 | 存在问题

原文说明虚空之星每 `%d` 回合恢复一颗，**最多累积四颗**；译文只保留恢复频率，漏掉上限。快照的恢复逻辑仅在 `p.nb < 4` 时增星，图标也显示 `/4`；见 [void.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/sources/dlc/cults/tome-cults/data/talents/demented/void.lua:32) 第 32–51 行及第 135–141 行。

**读取范围与版本。** 实际读取了指定的 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/INPUT.md)、同目录的 `entries.json`、`context.lua`、`source-access.json`；以及其 `sections` 列明的 12 个 `sources/dlc/cults/tome-cults/data/talents/demented/` 单文件：`disfigured-face.lua`、`doom.lua`、`entropy.lua`、`friend-of-the-worm.lua`、`madness.lua`、`nether.lua`、`oblivion.lua`、`rift.lua`、`slow-death.lua`、`tentacles.lua`、`timethief.lua`、`void.lua`。额外读取的两份单文件是 `source-access.json` 所列 Cults 快照根目录下的 `tome-cults/data/damage_types.lua` 与 `tome-cults/data/timed_effects.lua`：前者由 `nether.lua` 的 `RIFT_EXPLOSION` 调用引入，后者由 `doom.lua` 的 `PROPHECY_OF_MADNESS` 及 `oblivion.lua` 的 `do_nihil`／`ENTROPIC_WASTING` 符号引入。14 份源码文件的 SHA-256 均与清单匹配。未读取其他报告、当前译文文件或其他源码版本；未创建临时文件，未修改仓库，未发现读取越界。本复核是审核观察，不是生产 `DONE_VERIFIED`。
