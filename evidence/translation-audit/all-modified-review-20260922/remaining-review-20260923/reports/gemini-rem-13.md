本审查报告由只读 REVIEWER 基于授权的自然语言审核旁路完成，严格遵循冻结材料与审核规则（未写入文件、未创建子代理、未读取历史审核报告）。

**DLC 源码版本限制说明**：本批条目涉及 DLC `orcs`（Embers of Rage）。其源码通过 `.artifacts/i18n/all-modified-review-20260922/sources/orcs` 提供的公开源码进行 SHA256 哈希核对（与 `source-access.json` 记录完全一致），但该 DLC 仓库 commit 及游戏最终目标版本未在清单中固定，不得宣称已核验固定 1.7.4 版本。

---

### 一、逐条审核结果总表

| 序号 | Entry ID | 审核判定 | Claim 编号 / 依据概要 |
| :--- | :--- | :--- | :--- |
| 1 | entry-03939 | 仅建议 | C01：`shock` 与紧邻的 `blow` 均译为“打击”，未区分冲击/电击与打击 |
| 2 | entry-03940 | 存在问题 | C02：被击退撞墙（`slams into`）错译为主动攻击（`击中了某物`） |
| 3 | entry-03941 | 未发现问题 | 术语与上下文一致（`植入物：蒸汽制造机`），无异常 |
| 4 | entry-03942 | 未发现问题 | 占位符与标点保留完整，机制语境吻合（击碎投射物） |
| 5 | entry-03943 | 未发现问题 | 语义简练忠实（`链接到召唤者。`） |
| 6 | entry-03944 | 未发现问题 | 占位符与机制完全对应（自爆造成火焰伤害，主人死亡可用） |
| 7 | entry-03946 | 仅建议 | C03：`cooldown twice as fast`（冷却速度翻倍）译作“冷却时间减半”存机制概念偏差 |
| 8 | entry-03949 | 未发现问题 | 负生命存活（`die_at = -life`）机制表达准确，占位符匹配 |
| 9 | entry-03950 | 存在问题 | C04：`metalstar` 错译为“灵晶射击”；漏译体内碎片；距离表述存在两倍乘法歧义 |
| 10 | entry-03951 | 仅建议 | C05：`tinkers` 意译为“药剂、附着物等道具”，建议规范对齐术语“蒸汽工具” |
| 11 | entry-03952 | 未发现问题 | 无弹药提示清晰忠实（`你没有子弹！`） |
| 12 | entry-03953 | 存在问题 | C06：核心机制类型 `ranged melee attack`（远程近战攻击）漏译关键成分 `melee` |
| 13 | entry-03954 | 未发现问题 | 召唤空格不足提示准确无误 |
| 14 | entry-03956 | 未发现问题 | 占位符与格式标签正确，机制对应定身（`canBe("pin")`）准确 |
| 15 | entry-03957 | 未发现问题 | 抓取拉近并定身机制准确，占位符匹配 |
| 16 | entry-03958 | 未发现问题 | 属性缩写、疾病伤害、占位符均完全正确 |
| 17 | entry-03959 | 未发现问题 | 挖掘沙墙（`DamageType.DIG`）机制对应准确 |
| 18 | entry-03960 | 存在问题 | C07：漏译限定词 `other`，未体现排除施法者自身的机制限制（`act ~= self`） |
| 19 | entry-03961 | 未发现问题 | 技能译名准确（`奥术干扰波`） |
| 20 | entry-03963 | 未发现问题 | 占位符与致盲检定机制（`apply_power`）表达对应准确 |

---

### 二、疑点详细分析（Claims）

#### C01 (entry-03939)
- **条目**：entry-03939 (`tome-orcs/data/talents/steam/heavy-weapons.lua:738`)
- **原文短引**：`%s resists the stunning shock!`
- **原译短引**：`%s抵抗了震慑打击！`
- **具体意义差异**：在重装武器精通的电击棒效果中，主目标抵抗震慑时提示 `%s resists the stunning blow!`（抵抗了震慑打击！），而周围冲击波波及目标抵抗时提示 `%s resists the stunning shock!`。译文将两者均翻译为“%s抵抗了震慑打击！”，未能区分主目标的近战打击（blow）与周围扩散的电击/冲击（shock）。
- **最强等价读法与处理**：机制上两者均代表对震慑状态（stun）的抵抗，战斗逻辑不破坏。建议将此处澄清为“%s抵抗了震慑电击！”或“%s抵抗了震慑冲击！”，以与主目标打击区分。
- **状态**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua:738`
- **缺失证据**：无

#### C02 (entry-03940)
- **条目**：entry-03940 (`tome-orcs/data/talents/steam/heavy-weapons.lua:988`)
- **原文短引**：`%s slams into something solid, emitting a pulse of stunning lightning!`
- **原译短引**：`%s击中了某物，放出一股震慑闪电冲击！`
- **具体意义差异**：源码中这是电击棒过载击退（knockback）的回调，当被击退的目标撞上地形阻挡（`block_move`，如墙体）时触发。主语 `%s` 是受害者自身被撞在坚固障碍物上（slams into something solid）。原译译为“%s击中了某物”，将受害者被动撞墙误译为主动出手击打物体，主客体动作方向与叙事逻辑严重颠倒。
- **最强等价读法与处理**：无法等价解释。被击退的目标撞上障碍物并自身爆发脉冲，必须译为“%s撞上了坚固的物体，放出一股震慑闪电脉冲！”或“%s撞上实物，……”。
- **状态**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua:988`
- **缺失证据**：无

#### C03 (entry-03946)
- **条目**：entry-03946 (`tome-orcs/data/talents/steam/mecharachnid.lua:699`)
- **原文短引**：`...and all of its talents cooldown twice as fast.`
- **原译短引**：`...所有技能冷却时间减半。`
- **具体意义差异**：源码底层 `EFF_MECHARACHNID_PILOTING_BUFF` 的实现为每回合 `on_timeout` 时使冷却额外扣减 1 回合（`talents_cd[tid] = talents_cd[tid] - 1`），即冷却流逝速度翻倍。这与技能初始基础冷却时间除以 2（cooldown halved）在机制上不完全相同（在有界持续时间结束后未走完的冷却恢复原速）。
- **最强等价读法与处理**：日常语境中玩家常将冷却速度加倍通俗理解为冷却所需时间减半。从严谨机制出发，建议改为“所有技能冷却恢复速度翻倍”或“冷却速度加倍”，作为表达澄清。
- **状态**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/mecharachnid.lua:699` 及 `data/timed_effects/other.lua:450`
- **缺失证据**：无

#### C04 (entry-03950)
- **条目**：entry-03950 (`tome-orcs/data/talents/steam/mechstar.lua:79`)
- **原文短引**：`When you fire your metalstar... with the shrapnel still inside... twice away from the radius of Metalstar (currently %d)...`
- **原译短引**：`每次你使用灵晶射击时...与灵晶碎片建立血液灵能联系...超过金属灵晶范围（当前 %d）的两倍时...`
- **具体意义差异**：
  1. `metalstar` 是该系列基础技能“金属灵晶”（本段第四句和前文 talent name 均准确译为金属灵晶），第一句却译作“灵晶射击”，造成同一技能出现未知的错译名称且前后不统一；
  2. `with the shrapnel still inside` 遗漏了 `still inside`（残留在目标体内的弹片/碎片）；
  3. 代码传入参数 `%d` 即为 `self:getTalentRadius(mt) * 2`（已乘 2），原译文写为“超过金属灵晶范围（当前 %d）的两倍”，把“的两倍”放在数值括号后，严重诱导玩家理解为要在 `%d` 基础上再乘 2（例如显示为 6 时被理解为 12 格断裂，实际为 6 格断裂）。
- **最强等价读法与处理**：无法等价解释第一句的术语错位。应修正为：“当你发射金属灵晶时，你将与残留其体内的弹片建立血液灵能联系……当目标脱离金属灵晶半径的两倍距离（当前为 %d 格）时，效果终止。”
- **状态**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/mechstar.lua:79-84` 及 `data/timed_effects/physical.lua:745`
- **缺失证据**：无

#### C05 (entry-03951)
- **条目**：entry-03951 (`tome-orcs/data/talents/steam/other.lua:142`)
- **原文短引**：`Allows you to create tinkers.`
- **原译短引**：`使用该技能来制造药剂、附着物等道具。`
- **具体意义差异**：术语库中 `tinker` 规范译为“蒸汽工具”（`scope: dlc`, `status: existing`）。原译将其意译扩写为“制造药剂、附着物等道具”。
- **最强等价读法与处理**：按规则 existing 术语不强制改名，且意译内容有助于玩家理解制造界面包含的组件类型。仅建议规范对齐术语库，统一表述为“允许你制造蒸汽工具。”
- **状态**：`advisory`（仅建议）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:142`
- **缺失证据**：无

#### C06 (entry-03953)
- **条目**：entry-03953 (`tome-orcs/data/talents/steam/other.lua:358`)
- **原文短引**：`This shot is a ranged melee attack but will use the ranged procs of your ammo as well.`
- **原译短引**：`射击是远程攻击将会触发弹药特效。`
- **具体意义差异**：源码中该射击本质为 `self:attackTargetWith`（近战攻击判定，带攻击射程），因此属于特殊的“远程近战攻击”（ranged melee attack）。原文特意用连词 `but` 强调：虽然是近战攻击判定，但依然会破例触发弹药的远程特效。原译遗漏了关键核心词 `melee`（近战），直接译作“远程攻击”，不仅彻底丢掉了近战属性的机制事实，还破坏了转折因果逻辑。此外，“沃瑞钽钢”建议依 preferred 术语规范为“沃瑞钽”。
- **最强等价读法与处理**：无法等价解释。遗漏 melee 会使依赖近战触发/近战伤害加成装备的玩家产生严重误判。应修正为：“这次射击是一次远程近战攻击，但同时也会触发你弹药的远程触发特效。”
- **状态**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:344, 359`
- **缺失证据**：无

#### C07 (entry-03960)
- **条目**：entry-03960 (`tome-orcs/data/talents/steam/other.lua:916`)
- **原文短引**：`Throw a cone of healing with radius %d, healing other mechanical creatures (steam spiders) for %d.`
- **原译短引**：`释放一片锥形半径 %d 码的修理器，修复机械生物（蒸汽蜘蛛）%d 生命值。`
- **具体意义差异**：源码中治疗目标检查明确要求 `act ~= self`（`heal_check` 函数），英文原文亦明确标示 `other mechanical creatures`（其他机械生物）。译文漏译了限定词 `other`（其他），使描述变成“修复机械生物”，可能让玩家误以为该技能能够治疗自身。
- **最强等价读法与处理**：由于机制代码明确禁止治疗施法者自身，漏译其他导致作用范围的主客体界限模糊。应修正为：“……修复其他机械生物（蒸汽蜘蛛）%d 生命值。”
- **状态**：`confirmed`（存在问题）
- **来源路径行号**：`.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua:840, 916`
- **缺失证据**：无

---

### 三、审查汇总

- **本批总审核条目数**：20 条
- **未发现问题**：13 条
- **存在问题 (confirmed)**：4 条（entry-03940、entry-03950、entry-03953、entry-03960）
- **仅建议 (advisory)**：3 条（entry-03939、entry-03946、entry-03951）
- **待确认 (pending)**：0 条

---

### 四、实际读取路径与限制说明

1. **入口与规则文件**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/batches/rem-13.md`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/RULES.md`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/source-access.json`
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/terms.json`
2. **快照文件**：
   - `evidence/translation-audit/all-modified-review-20260922/remaining-review-20260923/snapshots/tome-orcs.lua`（行 5180 - 5520）
3. **公开冻结源码（SHA256 已核验）**：
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/heavy-weapons.lua` (0b4f50fb...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/inscriptions.lua` (7b2ad7cf...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/magnetism.lua` (b14b2da4...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/mecharachnid.lua` (d4a229c0...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/mechstar.lua` (e6e5f57a...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/talents/steam/other.lua` (4a12c054...)
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/other.lua`
   - `.artifacts/i18n/all-modified-review-20260922/sources/orcs/tome-orcs/data/timed_effects/physical.lua`
4. **限制说明**：
   - 严格遵循只读权限，未对工作树产生任何写操作；
   - 未启动或调用任何外部子代理及外部网络；
   - DLC `orcs` 源码仅基于快照哈希锚定核验，相关来源 commit 及实际 1.7.4 版本未固定。
