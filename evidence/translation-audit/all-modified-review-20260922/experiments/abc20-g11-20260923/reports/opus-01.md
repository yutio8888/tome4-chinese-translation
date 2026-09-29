40 条已全部核对完，下面是复核结果。

| 完整 entry-ID | 四类判定 | claim 编号或简短依据 |
|---|---|---|
| entry-03573 | 未发现问题 | 每回合值、总值、每种疾病的枯萎伤害都与 disfigured-face.lua:128-131 一致 |
| entry-03574 | 未发现问题 | 失败几率、穿透、2 回合都对得上，见 disfigured-face.lua:188-201 |
| entry-03575 | 仅建议 | C01 |
| entry-03576 | 存在问题 | C02、C03 |
| entry-03577 | 未发现问题 | 标记与参与者都保留，见 entropy.lua:138 |
| entry-03578 | 未发现问题 | 持续时间、半径成长、熵加成都与 entropy.lua:215-233 一致 |
| entry-03579 | 仅建议 | C04 |
| entry-03580 | 未发现问题 | friend-of-the-worm.lua:39 |
| entry-03581 | 存在问题 | C05（问题）；C06（建议） |
| entry-03582 | 仅建议 | C07 |
| entry-03583 | 未发现问题 | 半径 3、5 回合、纹身位 floor(raw/2)，见 friend-of-the-worm.lua:527-547 |
| entry-03584 | 未发现问题 | 物理豁免对抗法术强度、震慑、法术豁免/闪避降低，见 friend-of-the-worm.lua:561-581 |
| entry-03585 | 未发现问题 | 叠加上限 stat*3 表述正确，见 madness.lua:49,62-65 |
| entry-03586 | 未发现问题 | args_order [2,1] 让 %d 取半径、%0.2f 取伤害，映射正确，见 madness.lua:174-175 |
| entry-03587 | 未发现问题 | madness.lua:208-226 |
| entry-03588 | 未发现问题 | 同一目标每回合最多吃一次爆炸（turn_procs），见 damage_types.lua（cults）RIFT_EXPLOSION |
| entry-03589 | 未发现问题 | nether.lua:190 |
| entry-03590 | 未发现问题 | nether.lua:216 |
| entry-03591 | 未发现问题 | 颜色标记保留，见 nether.lua:225 |
| entry-03592 | 未发现问题 | nether.lua:228 |
| entry-03593 | 仅建议 | C08 |
| entry-03594 | 存在问题 | C09（问题）；C10（建议） |
| entry-03595 | 未发现问题 | 目标数、半径 10、8 回合都对得上，见 oblivion.lua:30-58 |
| entry-03596 | 未发现问题 | 译文补的“暗影时空各 50%%”与 VOID 伤害类型的对半分配一致（引擎 damage_types.lua:2864-2870） |
| entry-03597 | 未发现问题 | rift.lua:168,539 |
| entry-03598 | 未发现问题 | rift.lua:221 |
| entry-03599 | 未发现问题 | args_order [1,3,2] 映射为范围、吸收量、回合，正确，见 rift.lua:255-257 |
| entry-03600 | 存在问题 | C11（问题）；C12（建议） |
| entry-03601 | 未发现问题 | rift.lua:594 |
| entry-03602 | 存在问题 | C13；“连锁至 3 个额外目标”与实现一致（首个目标 + 最多 3 个，rift.lua 同段），不算问题 |
| entry-03603 | 未发现问题 | slow-death.lua:56 |
| entry-03604 | 未发现问题 | slow-death.lua:101-106 |
| entry-03605 | 未发现问题 | 两侧追加攻击与实现一致（superload Combat.lua:40-49），占位符都保留 |
| entry-03606 | 仅建议 | C14 |
| entry-03607 | 未发现问题 | tentacles.lua:262 |
| entry-03608 | 未发现问题 | timethief.lua:82-83,144-145 |
| entry-03609 | 未发现问题 | 术语条目限定 source_tag 为 logSeen，本条是 logPlayer，不适用；两者只差标点 |
| entry-03610 | 未发现问题 | void.lua:31 |
| entry-03611 | 未发现问题 | 标记和 #Target#/#Source# 顺序都保留，见 void.lua:73 |
| entry-03612 | 存在问题 | C15 |

### C01 | entry-03575 | 仅建议
- 原文 “Weave your chosen prophecy into your speech, dooming your foe twice over.”；译文 “对你的听众施加双重诅咒。”
- 译文把 foe 换成了“听众”，并省略了“把所选预言织入话语”的描写。
- 核实的机制是所选预言附加给主要目标，见 doom.lua:110-113 和 twofold_curse 函数。下一句“施加给主要目标”已经正确交代了作用对象，所以这里只算措辞偏好。

### C02 | entry-03576 | 存在问题
- 原文 “…has its cooldown reduced by %d turns.”；译文 “你的一个技能的冷却时间将减少 %d。”
- 问题：丢了单位“回合”。同一技能树的疯狂预言本身是按百分比增加冷却（doom.lua:130），没有单位时，这个数既可以读成回合，也可以读成百分比。
- 源码：timed_effects.lua:896-913（cults）。callbackOnTalentPost 调用 `eff.src:alterTalentCoolingdown(tid, -eff.cd)`，按回合减少。eff.cd 来自 doom.lua:106 的 Revelation getMadness，即 doom.lua:389 的 math.floor(...)。

### C03 | entry-03576 | 存在问题
- 原文 “one of your talents on cooldown”；译文 “你的一个技能”。
- 问题：丢了“正在冷却中”这个范围限定。实现只从 `eff.src.talents_cd`（正在冷却的技能）里随机挑一个，且排除 fixed_cooldown，见 timed_effects.lua:901-911。
- 去掉限定后，译文可以读成任意技能，甚至读成技能本身的基础冷却时间被减少。

### C04 | entry-03579 | 仅建议
- 译文 “增加 %d%% 黑暗和时空伤害”。本批其他条目和术语快照（darkness，damage type，existing）都用“暗影”。
- 机制是 inc_damage/resists_pen 的 DARKNESS/TEMPORAL，见 entropy.lua:264-265，语义没有错。该术语是 existing，不是强制译名，所以只记为一致性建议。

### C05 | entry-03581 | 存在问题
- 原文 “Using this spell will ressurect your friendly horror if it died…”；译文 “使用该法术将复活已死亡的单位…”。
- 问题：作用对象从“你的友方恐魔（蠕虫合体）”泛化成了任意“已死亡的单位”。
- 源码：friend-of-the-worm.lua:357-374 只处理 `self.demented_wtw`。on_pre_use（:347）在蠕虫还活着时直接拒绝施放。

### C06 | entry-03581 | 仅建议
- 原文 “To change your horror's equipment and talents…”；译文 “试图改变其装备时…”，漏了 talents。
- 第二行“你可以完全控制、升级、更换它的装备和技能”已经交代了技能，所以不算信息丢失。

### C07 | entry-03582 | 仅建议
- 译文 “传送至 %d 内的目标处”，没有“范围/格”。数值 10 见 friend-of-the-worm.lua:515，意思能看懂，属于措辞完整度问题。

### C08 | entry-03593 | 仅建议
- 译文 “%0.2f 暗影 %0.2f 时空伤害”，两个数值之间缺“和”或顿号。参数顺序正确（nether.lua:292），可读性偏好。

### C09 | entry-03594 | 存在问题
- 原文 “your next Nether spell will consume all sparks”；译文 “你的下一次虚空法术将消耗所有火花”。
- 问题：Nether 指 demented/nether 技能树。源码里真正会消耗火花的是 Netherblast、Rift Cutter、Spatial Distortion 三个技能，都检查 `EFF_HALO_OF_RUIN charges==5`，见 nether.lua:50-58、103-110、196-201。
- 术语快照里 nether 对应“彼世”，void 对应另一棵技能树 demented/void“虚空”。同一条里的“彼世火花”“彼世冲击”都用了彼世。译成“虚空法术”会把适用范围错指到 Void 技能树。

### C10 | entry-03594 | 仅建议
- 原文 “your Magic stat”；译文 “魔法属性”，术语快照里 Magic 是“魔力”（existing）。机制是 stats=self:getMag()，见 nether.lua:242，语义正确，属一致性建议。

### C11 | entry-03600 | 存在问题
- 原文 “reduces their global speed by 30%%”；译文 “使其整体速度降低 30%%”。
- 术语快照里 global speed 在 tformat 下是 preferred“全局速度”，备注明确写了“不写作‘整体速度’”。这是明确适用的术语要求。
- 源码：rift.lua 中 temporal_vortex 以 CHRONOSLOW slow=0.3 作用于半径 4（Pierce the Veil 段，约 rift.lua:425-426）。

### C12 | entry-03600 | 仅建议
- “你的虚空造物属性随你的等级和魔法属性提高而提高”，Magic 用了“魔法属性”，与 C10 同类。

### C13 | entry-03602 | 存在问题
- 原文 “increasing their global speed by %d%%”；译文 “增加他们 %d%% 的整体速度”，同样违反 global speed 的 preferred 术语。
- 源码：rift.lua:539-540 `m.global_speed_base = m.global_speed_base + self.mult`，确实是全局速度。

### C14 | entry-03606 | 仅建议
- 原文 “…but is currently disabled due to non-empty offhand”，主语是触手手；译文 “该技能暂时被禁用”。
- 本技能（变异之手）就是触手手本身。副手非空时 canTentacleCombat 返回 false，见 tentacles.lua:39-47 和 superload Combat.lua:32。
- 严格说，Diseased Tongue 用 force=true 仍能使用触手，见 disfigured-face.lua:39。英文原句同样有这种笼统，所以只作措辞建议。插入 03605 的 “%s :” 后能正常显示。

### C15 | entry-03612 | 存在问题
- 原文 “You regenerate 1 star every %d turns, stacking up to 4 times.”；译文 “虚空之星每经过 %d 回合自动恢复一颗。”
- 问题：漏了上限 4 颗这个数量限制。
- 源码：void.lua:49 `if p.nb < 4 then p.nb = p.nb + 1`，图标显示也是 “/4”（void.lua:35）。
- 其余内容已核实：40% 反冲是每回合 floor(reduce/20)、共 8 回合（void.lua:78），与译文一致。

## 读取路径与越界情况
- 入口和冻结输入（只读）：`experiments/abc20-g11-20260923/` 下的 INPUT.md、entries.json（身份与原文/译文字段）、context.lua（邻近译名）、source-access.json。没有读 SPEC、STATE、PLAN、SCORING、BASELINE、FREEZE、dispatches、raw、reports、脚本或其他实验文件。
- 本组 sections 源码：`sources/dlc/cults/tome-cults/data/talents/demented/` 下 12 个文件，sha256 全部与 source-access 一致。**DLC 快照未固定源码仓库和 commit**，上面的 DLC 机制结论只对该快照成立，是否适用于目标版本待确认。
- 额外读取的 DLC 单文件，根目录为 source-access 列明的 `abc20-20260923/sources/cults`，哈希都已比对一致：
  - `tome-cults/data/timed_effects.lua`：由 doom.lua 的 `EFF_PROPHECY_OF_MADNESS` 引入，只读了该效果段。
  - `tome-cults/data/damage_types.lua`：由 nether.lua 的 `DamageType.RIFT` / `RIFT_EXPLOSION` / `VOIDBURN` 及 oblivion.lua 的 `DamageType.VOID` 引入；查到 VOID 不在此文件中定义。
  - `tome-cults/superload/mod/class/interface/Combat.lua`：由 tentacles.lua 和 disfigured-face.lua 的 `tentacle_hand_prevent` 属性、`T_MUTATED_HAND` 调用引入。这一步是按消费者推断的：DLC 文件本身没有显式 require 这个 superload，如实记录为推断的调用链来源。
- 引擎（固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63），用 `git show` 读单文件：
  - `game/modules/tome/data/damage_types.lua`：VOID 定义，由上面的 `DamageType.VOID` 引入。
  - `game/modules/tome/class/interface/Combat.lua`：addCombatTraining、combatTrainingDamage，由 cults superload 中的 `_M:addCombatTraining("tentacles", …)` 引入。
  - 引擎代码只用来确认 DLC 调用的核心定义，没有拿引擎 commit 去替代 DLC 的版本。
- 检索方式都是单文件内 grep，没有整目录 grep/rg/find，没有读当前翻译文件、locales、历史审核或其他模型输出，没有创建子 agent，没有修改仓库，也没有创建临时文件或临时目录。
- 越界：无。
- 这些是审核观察，不是真值，不构成 DONE_VERIFIED。
