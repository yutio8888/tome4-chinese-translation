## 40条译文复核判定汇总表

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
| :--- | :--- | :--- |
| entry-03573 | 未发现问题 | 机制描述与伤害数值格式均核验无误 |
| entry-03574 | 仅建议 | C01（建议优化“激励你的意志”措辞避免混淆意志属性） |
| entry-03575 | 存在问题 | C02（作用对象误译为听众且漏译前置从句） |
| entry-03576 | 存在问题 | C03（冷却缩减漏译时间单位“turns/回合”） |
| entry-03577 | 未发现问题 | 战斗日志占位符及语义核验无误 |
| entry-03578 | 仅建议 | C04（“一格”建议优化为“半径 1 的时空裂隙”避免范围歧义） |
| entry-03579 | 仅建议 | C05（暗影伤害建议规范术语统一，“非瞬间”建议优化为“非瞬发”） |
| entry-03580 | 未发现问题 | 技能描述简短核验无误 |
| entry-03581 | 存在问题 | C06（操作指引漏译“and talents/技能”） |
| entry-03582 | 仅建议 | C07（“%d 内”建议补充量词“范围/格”） |
| entry-03583 | 仅建议 | C08（纹身位建议补充“永久”增加明确度） |
| entry-03584 | 未发现问题 | 豁免与技能联动机制核验无误 |
| entry-03585 | 未发现问题 | 三系强度降低与叠加逻辑核验无误 |
| entry-03586 | 未发现问题 | 参数重排[2, 1]与伤害类型核验无误 |
| entry-03587 | 未发现问题 | 伤害加成与技能名引用核验无误 |
| entry-03588 | 仅建议 | C09（“湮灭”建议优化为更贴合原意的“引爆/爆炸”） |
| entry-03589 | 未发现问题 | 玩家提示日志核验无误 |
| entry-03590 | 未发现问题 | 施法失败日志及占位符核验无误 |
| entry-03591 | 未发现问题 | 传送吞噬日志及颜色标记核验无误 |
| entry-03592 | 未发现问题 | 抵抗传送日志及占位符核验无误 |
| entry-03593 | 仅建议 | C10（暗影与时空伤害数值间建议补充连词或标点） |
| entry-03594 | 存在问题 | C11（Nether spell 误译为“虚空法术”，严重误导技能系消耗机制） |
| entry-03595 | 未发现问题 | 状态持续时间增减机制核验无误 |
| entry-03596 | 未发现问题 | 虚空伤害拆分及百分号转义核验无误 |
| entry-03597 | 未发现问题 | 强化后缀标记格式核验无误 |
| entry-03598 | 未发现问题 | 视野判定提示日志核验无误 |
| entry-03599 | 未发现问题 | 参数重排[1, 3, 2]与护盾机制核验无误 |
| entry-03600 | 存在问题 | C12（违反 preferred 术语：global speed 误译为整体速度） |
| entry-03601 | 未发现问题 | 召唤物技能失败日志核验无误 |
| entry-03602 | 存在问题 | C13（违反 preferred 术语：global speed 误译为整体速度） |
| entry-03603 | 未发现问题 | 技能选择提示界面文本核验无误 |
| entry-03604 | 仅建议 | C14（建议补充明确“当你进行消化时”触发条件） |
| entry-03605 | 仅建议 | C15（“目标同侧”建议优化为“目标身侧/两侧”；冒号前有多余空格） |
| entry-03606 | 未发现问题 | 禁用提示文本与颜色标签核验无误 |
| entry-03607 | 未发现问题 | 触手拉取失败日志核验无误 |
| entry-03608 | 未发现问题 | 增益与负面状态持续时间削减机制核验无误 |
| entry-03609 | 仅建议 | C16（日志标点建议与全局 preferred 条目统一为句号） |
| entry-03610 | 未发现问题 | 轻甲装备限制提示核验无误 |
| entry-03611 | 未发现问题 | 伤害吸收转熵战斗日志及颜色标记核验无误 |
| entry-03612 | 存在问题 | C17（漏译“stacking up to 4 times”虚空之星 4 层叠加限制） |

---

## 详细观察与 Claim 记录

### C01 | entry-03574 | 仅建议
- **原文短引**：`When a target becomes afraid it bolsters you to see their anguish, increasing your darkness and blight damage penetration by %d%% for 2 turns.`
- **译文短引**：`同时，敌人的恐惧和痛苦能激励你的意志，在 2 回合内增加你 %d%% 暗影和枯萎伤害抗性穿透。`
- **问题具体内容**：
  1. 措辞偏好：“激励你的意志”中使用了“意志”（在 ToME4 机制中为核心基础属性 Willpower），容易使玩家误以为本技能提升了角色“意志”属性；英文原文为“it bolsters you to see their anguish”，意为看到敌人的痛苦使你精神受到鼓舞/振奋。
  2. 语境关联：原文“When a target becomes afraid”表达的是目标陷入恐惧时带来增益的连带语境，译文作“同时”系将两者并列，虽契合源码中实际施加效果的实现，但句意上若将“意志”调整为普通鼓舞词汇并理顺衔接，体验更佳。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/disfigured-face.lua:190-202`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`affectTarget` 函数对目标施加 `EFF_GLIMPSE_OF_TRUE_HORROR` 并同时对自身施加 `EFF_GLIMPSE_OF_TRUE_HORROR_SELF`（提升暗影与枯萎抗性穿透），并未修改 `wil`（意志属性）。

### C02 | entry-03575 | 存在问题
- **原文短引**：`Weave your chosen prophecy into your speech, dooming your foe twice over. The chosen prophecy will apply instantly to your primary target whenever you cast any other prophecy at talent level %d.`
- **译文短引**：`对你的听众施加双重诅咒。每当你施加其他预言时，你选择的预言将同时施加给主要目标 (技能等级 %d)。`
- **问题具体内容**：
  1. 作用对象严重误译：原文“dooming your foe twice over”被翻译为“对你的听众施加双重诅咒”。“foe”意为敌人。本技能“双重诅咒（Twofold Curse）”的作用机制是施法时将所选预言附带施加给当前主要敌方单体（primary target），与同系中面向大范围群体敌人的“隆重演说（Grand Oration: speak to the masses）”截然不同；将“foe”译为“听众”直接曲解了该单体技能的作用对象。
  2. 句子结构与语义完全遗漏：原句前半句“Weave your chosen prophecy into your speech”（将你选择的预言编入你的演说之中）在译文中被彻底漏译。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/doom.lua:371-377` 及 `twofold_curse` 回调逻辑（第 89-94, 156-161, 226-230 行）（DLC 源码快照未固定 commit，source_pinning=unpinned）。当玩家激活双重诅咒时，施放其他预言会直接对当前所命中的敌方目标 `target` 触发所选预言的 `twofold_curse`，属于明确的敌方单体作用机制。

### C03 | entry-03576 | 存在问题
- **原文短引**：`Prophecy of Madness. Each time the target uses a talent one of your talents on cooldown has its cooldown reduced by %d turns.`
- **译文短引**：`疯狂预言：每次目标使用技能时，你的一个技能的冷却时间将减少 %d。`
- **问题具体内容**：
  单位信息缺失：原文明确包含冷却时间减少的量纲单位“turns”（回合）：`has its cooldown reduced by %d turns`，译文仅翻译为“减少 %d”，末尾遗漏了时间单位“回合”，导致机制描述数值信息不完整。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/doom.lua:411-423`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`getMadness` 计算减少的回合数（1–4 回合）并作为第一个参数填入 `%d turns`。

### C04 | entry-03578 | 仅建议
- **原文短引**：`a radius 1 rift in spacetime will be opened underneath the target for %d turns, increasing in radius by 1 each turn to a maximum of %d.`
- **译文短引**：`会在目标处产生一个持续 %d 回合的一格小型黑洞，每回合半径增加 1 直到 %d。`
- **问题具体内容**：
  范围表述偏好：原文为“a radius 1 rift in spacetime”（半径为 1 的时空裂隙），译文作“一格小型黑洞”。在 ToME4 坐标系中，半径 1 实际上是以目标为中心的 3x3 范围；“一格”容易让初见玩家误解为仅占 1 个地块。虽然下文接有“每回合半径增加 1”，但若调整为“半径 1 的小型黑洞/时空裂隙”会更加准确严谨。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/entropy.lua:119-131, 216-234`（DLC 源码快照未固定 commit，source_pinning=unpinned）。黑洞初始 `radius = 1`，通过 `core.fov.circle_grids` 获取范围并逐回合向外扩张。

### C05 | entry-03579 | 仅建议
- **原文短引**：`increasing your darkness and temporal damage by %d%% and resistance penetration by %d%% at the cost of suffering %0.2f entropic backlash for each non-instant spell.`
- **译文短引**：`增加 %d%% 黑暗和时空伤害与 %d%% 抗性穿透。作为代价，每个非瞬间法术会带来 %0.2f 熵能反冲。`
- **问题具体内容**：
  1. 术语一致性：“darkness”伤害类型在游戏核心机制及同文件其他条目（如 entry-03573、entry-03578 等）中普遍规范为“暗影伤害”，此处作“黑暗伤害”略显脱节；鉴于术语快照中该词条标记为 `existing` 而非强制的 `preferred`，按规则不计为阻断缺陷。
  2. 措辞偏好：“non-instant”在技能描述中建议统一优化为更符合游戏行文习惯的“非瞬发法术”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/entropy.lua:246-283`（DLC 源码快照未固定 commit，source_pinning=unpinned）。机制为增加 `DamageType.DARKNESS` 与 `DamageType.TEMPORAL` 的增伤与穿透，触发检查为 `if ab.is_spell and not ab.no_energy ...`（非瞬发法术）。

### C06 | entry-03581 | 存在问题
- **原文短引**：`To change your horror's equipment and talents first transfer the equipment from your inventory then take control of it.`
- **译文短引**：`试图改变其装备时，先将装备交给它，再切换控制。`
- **问题具体内容**：
  关键操作指引遗漏：原文为“To change your horror's equipment and talents”（试图更改其装备与技能时），明确指导玩家若需为蠕虫合体调整装备及技能点，操作步骤都是先转移装备再控制该仆从。译文仅作“试图改变其装备时”，完全漏译了“and talents”（以及技能），导致缺失了如何为其加点或学习技能的操作说明。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:426-439`（DLC 源码快照未固定 commit，source_pinning=unpinned）。蠕虫合体作为全控型随从，玩家需要通过接管控制来进入其升级加点界面。

### C07 | entry-03582 | 仅建议
- **原文短引**：`teleport to an enemy in range %d and make a melee attack for %d%% damage.`
- **译文短引**：`同时传送至 %d 内的目标处，造成 %d%% 近战伤害。`
- **问题具体内容**：
  量词修饰偏好：原文“in range %d”在译文中仅翻译为“%d 内”，缺少了距离单位或量词，略显生硬，建议优化为“范围 %d 内”或“%d 格内的目标处”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:513-516`（DLC 源码快照未固定 commit，source_pinning=unpinned）。此处第一个参数固定传入距离数值 10。

### C08 | entry-03583 | 仅建议
- **原文短引**：`your Worm that Walks permanently gains an inscription slot every 2 raw talent levels (%d).`
- **译文短引**：`该技能每增加两级原始等级，你的蠕虫合体获得一个纹身位（当前：%d）。`
- **问题具体内容**：
  副词修饰偏好：原文中“permanently gains”带有“permanently”（永久），译文虽已准确表达了技能每 2 级获得 1 个纹身位的机制，但未显式译出“永久”，建议补充“永久获得”以进一步明确该效果非临时增益。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua:526, 545-549`（DLC 源码快照未固定 commit，source_pinning=unpinned）。技能定义设置了 `no_unlearn_last = true`，确保纹身槽位一旦解锁即永久固定。

### C09 | entry-03588 | 仅建议
- **原文短引**：`After 3 turns the rift detonates, dealing %0.2f temporal damage to adjacent enemies. Targets cannot be struck by more than a single rift explosion at once.`
- **译文短引**：`3 回合后裂缝湮灭并对周围敌人造成 %0.2f 时空伤害。一次湮灭不能多次伤害同一目标。`
- **问题具体内容**：
  动词选词偏好：原文机制为裂隙引爆，英文使用“detonates”和“rift explosion”。译文采用了玄奥风格的“湮灭”，但在物理及游戏语义中，引爆（爆炸）更符合对其周围造成范围伤害的动态描述，且与后文“single rift explosion”对应更贴切。属于译者文风偏好，列为建议。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:138-159`（DLC 源码快照未固定 commit，source_pinning=unpinned）。机制是在第 3 回合对周围 1 格范围播放 `fireflash` 爆炸音效并结算伤害。

### C10 | entry-03593 | 仅建议
- **原文短引**：`Enemies will take %0.2f darkness and %0.2f temporal damage.`
- **译文短引**：`敌人将受到 %0.2f 暗影 %0.2f 时空伤害。`
- **问题具体内容**：
  标点/连词偏好：译文“%0.2f 暗影 %0.2f 时空伤害”中，两种伤害数值之间直接为空格分隔，缺少中文连词或顿号，格式上建议补充为“%0.2f 暗影和 %0.2f 时空伤害”或“%0.2f 暗影、%0.2f 时空伤害”。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:286-293`（DLC 源码快照未固定 commit，source_pinning=unpinned）。`damDesc` 分别生成暗影和时空伤害描述并依次填充。

### C11 | entry-03594 | 存在问题
- **原文短引**：`on reaching 5 sparks your next Nether spell will consume all sparks to empower itself:`
- **译文短引**：`当你拥有 5 个火花时，你的下一次虚空法术将消耗所有火花来获得强化效果。`
- **问题具体内容**：
  1. 技能系别严重误译（实质机制错误）：原文“your next Nether spell”被误译为“你的下一次虚空法术”。在 Cults of Entropy DLC 中，“Nether”是独立的“彼世系”（demented/nether），而“虚空系”（demented/void）是另一个完全不同的技能系。源码实现中严格匹配 `if ab.type[1]:find("^demented/nether")`，只有施放“彼世系”法术（如彼世冲击、裂缝切割、空间扭曲）才会消耗 5 层火花并触发强化；施放虚空法术根本无法消耗火花。此误译直接颠倒了技能交互对象，给玩家造成严重误导。
  2. 属性术语偏差（附带观察）：文末“your Magic stat”被译为“魔法属性”，在游戏机制术语中应规范为“魔力”（Magic 属性）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/nether.lua:308-324`（DLC 源码快照未固定 commit，source_pinning=unpinned）。强化触发只响应 `demented/nether` 系法术；术语快照中 `nether` 对应 `彼世`，`void` 对应 `虚空`。

### C12 | entry-03600 | 存在问题
- **原文短引**：`Temporal Vortex: Inflicts %0.2f temporal damage each turn to enemies in radius 4 and reduces their global speed by 30%%.`
- **译文短引**：`时空漩涡：每回合对半径 4 内的敌人造成 %0.2f 时空伤害，并使其整体速度降低 30%%。`
- **问题具体内容**：
  1. 违反明确适用的 preferred 术语规范：原文“global speed”被译为“整体速度”。本批冻结术语快照中包含明确规则：`global speed -> 全局速度`，status 为 `preferred`，并在 notes 中明确要求：“技能与状态说明中的全局行动速度机制；不写作‘整体速度’或‘全体速度’”。译文直接使用了禁止采用的“整体速度”。
  2. 属性术语偏差（附带观察）：末尾“Magic stat”同样译为了“魔法属性”（规范应为“魔力”）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/rift.lua:558-570`（DLC 源码快照未固定 commit，source_pinning=unpinned）；术语快照中条目：`global speed -> 全局速度 (preferred core, 不写作“整体速度”或“全体速度”)`。

### C13 | entry-03602 | 存在问题
- **原文短引**：`Dimensional Gate: Voidling Skitterers will be frenzied, increasing their global speed by %d%%.`
- **译文短引**：`维度之门 :#LAST# 虚空造物将会变得狂暴，增加他们 %d%% 的整体速度。`
- **问题具体内容**：
  违反明确适用的 preferred 术语规范：原文“global speed”再次被译为“整体速度”。同样违反了术语快照中 `global speed -> 全局速度 (preferred)` 的显式约束要求（“不写作‘整体速度’或‘全体速度’”）。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/rift.lua:620-629`（DLC 源码快照未固定 commit，source_pinning=unpinned）；术语快照 `global speed -> 全局速度`。

### C14 | entry-03604 | 仅建议
- **原文短引**：`When you digest you can steal a random talent from your victim and can use it for yourself at talent level %d.`
- **译文短引**：`你可以窃取并使用它的一个随机技能（技能等级 %d）。`
- **问题具体内容**：
  条件状语省略：原文第二句开头的明确触发动作“When you digest”（当你消化目标时）未在译文中显式译出。虽然第一句已铺垫了“正在被你消化的目标”，但第二句若补充“当你进行消化时”能更明确指出窃取技能的时机是在施放“消化（Digest）”击杀目标时发生。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/slow-death.lua:42-68, 100-107`（DLC 源码快照未固定 commit，source_pinning=unpinned）。被动技能“苦难折磨（Painful Agony）”在主动技能“消化（Digest）”斩杀目标时触发窃取逻辑。

### C15 | entry-03605 | 仅建议
- **原文短引**：`hit your target and those on the side whenever you hit with a basic attack.` / `Your tentacle hand currently has these stats%s:\n\t\t%s`
- **译文短引**：`副手空闲时，当使用普通攻击，触手会自动攻击目标以及目标同侧的其他单位。` / `你的触手当前属性为 %s :\n\t\t%s`
- **问题具体内容**：
  1. 方位措辞偏好：“those on the side”被译为“目标同侧”，语意容易被理解为“与目标在同一侧”；机制上是指攻击目标周围身侧/两侧的相邻单位，建议优化为“目标身侧/两侧的其他单位”。
  2. 排版小瑕疵：文末“当前属性为 %s :”中，冒号前包含多余的半角空格。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/tentacles.lua:66-82`（DLC 源码快照未固定 commit，source_pinning=unpinned）。

### C16 | entry-03609 | 仅建议
- **原文短引**：`Not enough space to summon!`
- **译文短引**：`没有足够的空间召唤！`
- **问题具体内容**：
  标点偏好：本条译文末尾使用了感叹号“！”，与英文原文“!”对应；术语快照中存在 preferred 条目 `Not enough space to summon! -> 没有足够的空间召唤。`（域为 logSeen，以句号结尾）。本条在源码中的标签为 logPlayer，标点差异不造成信息损失或运行时故障，但建议依项目偏好统一标点。
- **判定状态**：仅建议
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/timethief.lua:200`（DLC 源码快照未固定 commit，source_pinning=unpinned）。

### C17 | entry-03612 | 存在问题
- **原文短引**：`You regenerate 1 star every %d turns, stacking up to 4 times.`
- **译文短引**：`虚空之星每经过 %d 回合自动恢复一颗。`
- **问题具体内容**：
  关键机制上限数值严重漏译：原文第三行包含核心限制从句“stacking up to 4 times”（最多叠加 4 颗 / 叠加上限 4 颗）。译文仅翻译了“虚空之星每经过 %d 回合自动恢复一颗”，将后半句关于层数上限的描述“stacking up to 4 times”完全漏译。这导致玩家无法从技能描述中获知虚空之星最大只能累积 4 颗这一关键机制限制，属于重要机制信息的遗漏。
- **判定状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/data/talents/demented/void.lua:38, 135-142`（DLC 源码快照未固定 commit，source_pinning=unpinned）。源码在休息恢复和状态维护时均硬编码限制最大星数 `local nb = 4`。

---

## 审查环境、核验路径与调用链来源说明

1. **冻结输入与参考文件**：
   - 唯一任务输入：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/INPUT.md`
   - 条目清单与元数据：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/entries.json`
   - 邻近上下文参考：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/context.lua`
   - 源码访问权限清单：`evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g11-20260923/source-access.json`

2. **读取的源码路径与版本**：
   - 本组 40 条译文所属组件均为 `cults`（Cults of Entropy DLC），根据 `source-access.json` 规则，DLC 源码仓库及 commit **未固定（unpinned）**，使用公开快照核验，对应单文件路径及 SHA-256 校验如下：
     - `sources/dlc/cults/tome-cults/data/talents/demented/disfigured-face.lua` (`92e1c785090559761bc7cbc0b3542816a1c0a1f3c91b2e4cd421302a2caa6c36`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/doom.lua` (`e68880092dbc5bfa5b8624f75b26297b163dca4b33d6dac38aba3760d6dd5b7e`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/entropy.lua` (`e8046402a99f3611d9f63cbc57bc060c9ce1039461e5bdfcbf5a64598fbcb69c`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/friend-of-the-worm.lua` (`e8c4508aa632de865c89ae398406cc6cad34b49349142c43bdf06fb8b68a1ed1`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/madness.lua` (`33e274b4e1f155bf677dae8d8cf29c61b9f2b99920a0a4ec80ab0f043f62dac4`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/nether.lua` (`4ee9687b048c9f911046444d2de07ce39515094dc7829ef5a9ab17e9b75c2688`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/oblivion.lua` (`3242012a234a5b9a8c9ebfdb57556803619c8b752954e150d2b653806cb1d44b`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/rift.lua` (`23ca78691a34de2e7cc9b589d19f244cf85596d15947688dddfd376e04455bde`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/slow-death.lua` (`469dd52ed0413b59395dc7ae46a0a8a0e4eaca5ce8c85e430df6e489e899a3d3`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/tentacles.lua` (`038841bc39a9c1ca209651fb5c8cbe248ef0abab6596c528407063eefbe25906`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/timethief.lua` (`d93d99fd05b45f16cb730c6bf46f7b0bf305e157de21513d539c0e648faa231f`)
     - `sources/dlc/cults/tome-cults/data/talents/demented/void.lua` (`19cb982e3487d52626f46c5e0623f5f75b4ad2e126c7580e000672c74ce934b1`)
   - 额外引入并核验的快照源码文件（调用链/符号引入）：
     - `.../sources/cults/tome-cults/data/timed_effects.lua` (`0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c`)：由 `disfigured-face.lua:192-193` 调用的状态 `EFF_GLIMPSE_OF_TRUE_HORROR` 及 `EFF_GLIMPSE_OF_TRUE_HORROR_SELF` 符号引入，用于核实恐惧与伤害穿透机制。

3. **临时文件路径与合规说明**：
   - 依据用户授权，审查期间创建了专属临时目录 `/tmp/abc20-g11-20260923-hiz_fsl6` 进行代码片段及占位符匹配辅助分析。
   - 所有中间脚本已在执行后即时清理并完全删除该目录。
   - 未读取任何其他模型的报告、历史输出、SPEC/PLAN/STATE 或未授权文件。

4. **越界与核验限制声明**：
   - 全程无越界行为；
   - 未修改仓库任何工作树文件；
   - 未创建子 agent；
   - 本输出仅为独立只读 REVIEWER 观察报告，不宣称生产 `DONE_VERIFIED`。
