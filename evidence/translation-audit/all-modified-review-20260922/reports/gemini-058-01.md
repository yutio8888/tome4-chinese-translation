# batch-058 译文复核报告

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-058.md`
- **文件校验和**：`d3deeca82308bfe2d81cb79f8188819f9a86d272a5e2680ed7c328683ea6491b`（核对一致）
- **核验基准**：
  - 固定公开源码仓库 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/talents/cunning/` 各文件）
  - 译文比对终点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua`）
- **覆盖条目**：`entry-01706` 至 `entry-01745`，共 40 条逐条核对结果如下。

---

### entry-01706
- **位置**：`mod-tome.lua:23297`（`mod-tome/data/talents/cunning/called-shots.lua`）
- **判定**：细微观察
- **依据**：源码对应 `SKIRMISHER_SLING_SNIPER`。3 个占位符 `%d%%`、`%d%%`、`%d%%` 的类型、顺序与参数完全一致。细微观察在于原文首句“Your mastery of called shots is unparalleled.”被译为“你对射击的掌握程度无与伦比。”，其中技能系专名“called shots”（精准射击系）在句首被略译为“射击”（后文均已准确译为“精准射击系技能”），对数值和机制理解无实质阻碍。

### entry-01707
- **位置**：`mod-tome.lua:23306`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/stealth-base` 与 `cunning/stealth` 的技能类别描述。译文“使你的角色进入潜行。”准确对应原文“Allows the user to enter stealth.”，语义通顺准确。

### entry-01708
- **位置**：`mod-tome.lua:23308`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/trapping` 类别描述。译文“关于布设陷阱与各式诡计的知识。”完整忠实对应原文“The knowledge of trap laying and assorted trickeries.”。

### entry-01709
- **位置**：`mod-tome.lua:23310`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：细微观察
- **依据**：源码对应 `cunning/traps`（存放已解锁陷阱的具体技能树）描述。原文为名词短语“Collection of known traps.”（已掌握陷阱合集），译文意译为动词短语“学会制造各种功能的陷阱。”，作为技能树悬停提示语义通畅，无机制冲突。

### entry-01710
- **位置**：`mod-tome.lua:23312`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/poisons` 类别描述。译文“关于毒物的知识，以及如何用它们取得“良好”的效果。”准确对应原文，英文单引号 `'good'` 相应转化为中文双引号 `“良好”`，标点与语义无误。

### entry-01711
- **位置**：`mod-tome.lua:23313`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：细微观察
- **依据**：源码对应 `cunning/poisons-effects` 类别描述。原文为名词短语“Collection of known poisons.”（已掌握毒素合集），译文意译为动词短语“制造各种不同毒素。”，与 entry-01709 处理方式一致，语境表达清晰。

### entry-01712
- **位置**：`mod-tome.lua:23315`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/dirty` 类别描述。译文“使你学会令你目标致残的技能。”准确表达“Teaches various talents to cripple your foes.”。

### entry-01713
- **位置**：`mod-tome.lua:23317`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/lethality` 类别描述。译文“让你的对手尝尝什么是真正的痛苦……”风格化渲染得当，符合游戏文本语境。

### entry-01714
- **位置**：`mod-tome.lua:23319`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/shadow-magic` 类别描述。译文“融合魔法与阴影。”忠实对应原文“Blending magic and shadows.”。

### entry-01715
- **位置**：`mod-tome.lua:23323`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/survival` 类别描述。译文“让你认识到世界中的各种危险，并学会如何有效避免它们。”忠实对应原文。

### entry-01716
- **位置**：`mod-tome.lua:23325`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/tactical` 类别描述。译文“战斗中使用的策略技巧。”准确对应原文“Tactical combat abilities.”。

### entry-01717
- **位置**：`mod-tome.lua:23327`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/scoundrel` 类别描述（该系官方中文译名为“街头格斗”）。译文“街头格斗中使用的卑劣技巧。”结合技能系名称进行了语境融合，准确传达“ungentlemanly techniques”之意。

### entry-01718
- **位置**：`mod-tome.lua:23329`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：细微观察
- **依据**：源码对应 `cunning/artifice` 类别描述。原文为“Create and use cunning tools.”，译文为“制造并使用工具。”，漏译了修饰词“cunning”（精巧/诡计工具），但句子整体主旨未出现实质性偏差。

### entry-01719
- **位置**：`mod-tome.lua:23333`（`mod-tome/data/talents/cunning/cunning.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `cunning/called-shots` 类别描述。译文“对敌人身上的特定部位施加极致的痛苦。”准确忠实对应原文。

### entry-01720
- **位置**：`mod-tome.lua:23340`（`mod-tome/data/talents/cunning/dirty.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `DIRTY_FIGHTING`。占位符 `%d%%`（徒手伤害）、`%d`（物理豁免削减）、`50%%`（字面 50% 转义）、`%d`（持续回合）数量、顺序与格式完全吻合；“physical save”对应“物理豁免”，“stun, blind, confusion and pin immunities”对应“震慑、致盲、混乱、定身免疫”，机制核验准确。

### entry-01721
- **位置**：`mod-tome.lua:23352`（`mod-tome/data/talents/cunning/dirty.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `BLINDING_POWDER`。占位符 `%d`（锥形半径）、`%d`（命中降低）、`%d%%`（移速减缓）、`%d`（持续回合）与换行缩进 `\t\t` 均与原文及格式严格对齐；属性术语“命中”、“移动速度”翻译准确。

### entry-01722
- **位置**：`mod-tome.lua:23356`（`mod-tome/data/talents/cunning/dirty.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `TWIST_THE_KNIFE` 战斗日志。颜色标签 `#CRIMSON#` 与 `#LAST#` 完整，两个 `%s` 占位符保留且顺序正确。

### entry-01723
- **位置**：`mod-tome.lua:23357`（`mod-tome/data/talents/cunning/dirty.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `TWIST_THE_KNIFE` 驱散增益日志。颜色标签 `#CRIMSON#` 与 `#LAST#` 完整，两个 `%s` 占位符保留且顺序正确。

### entry-01724
- **位置**：`mod-tome.lua:23358`（`mod-tome/data/talents/cunning/dirty.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `TWIST_THE_KNIFE` 缩短增益持续时间日志。颜色标签 `#CRIMSON#` 与 `#LAST#` 完整，两个 `%s` 占位符保留且顺序正确。

### entry-01725
- **位置**：`mod-tome.lua:23387`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `APPLY_POISON` 抵抗日志。占位符 `%s` 准确保留，“vile poison”译为“邪恶毒素”，符合技能树统称。

### entry-01726
- **位置**：`mod-tome.lua:23427`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `VENOMOUS_STRIKE`。占位符 `%d%%`（武器伤害比例）与 `%s`（各毒素效果文本块）顺序与类型正确；换行缩进结构完整；“Throwing Knives”对应“飞刀投掷”，“Venomous Throw”对应“剧毒飞刀”，机制描述准确。

### entry-01727
- **位置**：`mod-tome.lua:23437`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：细微观察
- **依据**：源码对应 `NUMBING_POISON`。占位符 `%d%%` 匹配正确。细微观察在于本条将“Deadly Poison”译为“致命剧毒”，而同系列技能 entry-01728 至 entry-01731 均采用“致命毒素”，存在批内术语略微不一致，但不影响机制理解。

### entry-01728
- **位置**：`mod-tome.lua:23439`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `INSIDIOUS_POISON`。占位符 `%d%%`（治疗降低百分比）对应无误，文本表达精炼准确。

### entry-01729
- **位置**：`mod-tome.lua:23441`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `CRIPPLING_POISON`。占位符 `%d%%`（施法失败几率）准确保留，机制说明清晰。

### entry-01730
- **位置**：`mod-tome.lua:23443`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `LEECHING_POISON`。占位符 `%d%%`（吸血比例）准确保留，机制转换叙述清楚。

### entry-01731
- **位置**：`mod-tome.lua:23445`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `VOLATILE_POISON`。占位符 `%d%%` 与字面量 `50%%` 转义均正确，目标伤害与波及相邻伤害机制叙述准确。

### entry-01732
- **位置**：`mod-tome.lua:23449`（`mod-tome/data/talents/cunning/poisons.lua`）
- **判定**：存在疑点
- **依据**：源码对应 `STONING_POISON`。存在以下可核验问题：
  1. **机制与原意偏差严重**：源码中该技能属于持续生效的毒素增强（vile poison sustain），其触发机制为 `proc = function(...)`，即“在涂毒技能施加致命毒素时附带触发”。原文为“Enhance your Deadly Poison with a stoning agent. Whenever you apply Deadly Poison, you afflict your target with an additional earth-based poison...”。译文直接译作“在你的武器上涂上石化毒素...”，不仅漏译了“致命毒素（Deadly Poison）”以及“每当你施加致命毒素时（Whenever you apply Deadly Poison）”的前置触发关系，还漏译了“earth-based poison”（土系毒素），使玩家误以为这是一个独立的武器涂层技能。
  2. **占位符数值单位缺失**：原文第二个占位符为“stacking up to %d damage per turn”，译文仅为“（可叠加至 %d）”，漏掉了“伤害/每回合”的单位描述。
  3. **用词不统一**：同一句内混用了“每轮 %d 点自然伤害”与“持续 %d 回合”。

### entry-01733
- **位置**：`mod-tome.lua:23462`（`mod-tome/data/talents/cunning/scoundrel.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SCOUNDREL`。占位符 `%d%%`（暴击倍率降低）、`%d%%`（遗忘技能几率）、`%d`（遗忘持续回合）共 3 个，顺序与格式完全吻合，每目标每回合限触发一次的规则翻译准确。

### entry-01734
- **位置**：`mod-tome.lua:23468`（`mod-tome/data/talents/cunning/scoundrel.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `MISDIRECTION`。占位符 `%d%%`（豁免失败几率）、`%d%%`（转移后的持续时间比例）、`%d`（增加闪避）保留完整且顺序无误；“defense”对应“闪避”，“Accuracy”对应“命中”，属性名称规范。

### entry-01735
- **位置**：`mod-tome.lua:23490`（`mod-tome/data/talents/cunning/shadow-magic.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SHADOW_COMBAT`。占位符 `%.2f` 浮点格式严格保留；“darkness damage”对应“暗影伤害”，“Spellpower”对应“法术强度”，机制核验一致。

### entry-01736
- **位置**：`mod-tome.lua:23494`（`mod-tome/data/talents/cunning/shadow-magic.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SHADOW_CUNNING`。占位符 `%d%%` 与 `%d` 顺序准确；“Spellpower”对应“法术强度”，“Cunning”对应“灵巧”，计算关系叙述准确。

### entry-01737
- **位置**：`mod-tome.lua:23503`（`mod-tome/data/talents/cunning/shadow-magic.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SHADOWSTEP` 视线判断日志（`self:hasLOS`）。译文“你没有视线。”简洁准确。

### entry-01738
- **位置**：`mod-tome.lua:23504`（`mod-tome/data/talents/cunning/shadow-magic.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SHADOWSTEP` 传送失败日志（`self:teleportRandom`）。译文“法术失败了！”符合游戏一贯惯例。

### entry-01739
- **位置**：`mod-tome.lua:23518`（`mod-tome/data/talents/cunning/stealth.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `STEALTH` 中拼接字符串 `xs`。前导空格保留，占位符 `%d` 准确，语义明确。

### entry-01740
- **位置**：`mod-tome.lua:23519`（`mod-tome/data/talents/cunning/stealth.lua`）
- **判定**：细微观察
- **依据**：源码对应 `STEALTH` 主描述。占位符 `%d`（潜行点数）、`%d`（半径）、`%s`（黑暗地格补充分支）数量及顺序正确。细微观察在于：
  1. 原文为 `within range %d%s.`，由于 `%s`（即 entry-01739）自身自带前导空格，译文中写为 `在半径 %d %s 内`，在 `%d` 与 `%s` 之间人为增加了一个空格，导致拼接后出现双空格（当 `%s` 为空串时也会在“内”前留有多余空格）。
  2. 原文“Any non-instant, non-movement action”译为“任何非瞬间非移动技能”，将涵盖更广的“行动（action）”局限为“技能（talent/skill）”，但常规游戏操作中基本一致。

### entry-01741
- **位置**：`mod-tome.lua:23535`（`mod-tome/data/talents/cunning/stealth.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `SHADOWSTRIKE`。占位符 `%d%%`（暴击伤害增益上限）与 `%d`（脱离潜行后持续回合）顺序及格式对齐；自动暴击限制与距离衰减规则翻译完整准确。

### entry-01742
- **位置**：`mod-tome.lua:23557`（`mod-tome/data/talents/cunning/survival.lua`）
- **判定**：细微观察
- **依据**：源码对应 `HEIGHTENED_SENSES`。3 个 `%d` 占位符（感知范围、隐形/潜行侦察、陷阱侦测强度）数量与顺序一致。细微观察在于原文第三句末尾写为 `(+%d detect 'power')`，译文简化为“使你发现周围的陷阱的能力增加 %d”，略去了“+”号和“强度（power）”字样，数值机制理解无根本障碍。

### entry-01743
- **位置**：`mod-tome.lua:23573`（`mod-tome/data/talents/cunning/survival.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `DANGER_SENSE`。格式化占位符 `+%d`、`%0.1f%%`、`%d%%` 以及 Lua 特殊的正负号整数占位符 `%+d` 均精确无误保留并对齐；暴击减免、未察觉伤害倍率缩减及额外豁免机制核查准确。

### entry-01744
- **位置**：`mod-tome.lua:23587`（`mod-tome/data/talents/cunning/survival.lua`）
- **判定**：未发现问题
- **依据**：源码对应 `DISARM_TRAP`。3 个占位符 `%d`（侦察强度）、`%d`（解除强度）、`%s`（前置技能名）完全对齐；即使进入地格尝试解除的机制描述忠实。

### entry-01745
- **位置**：`mod-tome.lua:23623`（`mod-tome/data/talents/cunning/traps.lua`）
- **判定**：未发现问题
- **依据**：源码对应陷阱放置校验（`game.level.map(x, y, Map.TRAP)`）。译文“这里已经有一个陷阱了。”准确对应原文“There is already a trap there.”。