# C01–C09 修复记录（2026-10-13）

本次 EXECUTOR 仅修改冻结的 4 个 Lua 文件内 11 条 target，以及本文件；advisory/pending 未纳入。旧评估报告与 source-anchors.json 保持历史快照。不 stage/commit，不写 .ai 元数据，不启动子代理。

## 修复结果

| 问题 | 文件／行 | 修改 |
| --- | --- | --- |
| C01 | [mod-tome.lua:3148](../../../mod-tome.lua#L3148) | 重甲改为板甲，保持武器／盾牌限制。 |
| C03 | [mod-tome.lua:4065](../../../mod-tome.lua#L4065) | 恢复“不是为了自己”的受益者限定，并保留治屁股的语境。 |
| C04 | [mod-tome.lua:4082](../../../mod-tome.lua#L4082) | 恢复继续帮忙、协助配制药剂的角色对话。 |
| C04 | [mod-tome.lua:4098](../../../mod-tome.lua#L4098) | 恢复继续帮忙、协助配制药剂的角色对话。 |
| C02 | [tome-ashes-urhrok.lua:524](../../../tome-ashes-urhrok.lua#L524) | half-starved 恢复为“饿得半死”。 |
| C07 | [tome-ashes-urhrok.lua:1186](../../../tome-ashes-urhrok.lua#L1186) | 并列描述恢复与传播；保留近战命中、燃烧结束移除、50%传播几率、两层范围、未受诅咒目标及总伤害，删除伤害分摊的实现旁白。 |
| C09 | [tome-cults.lua:817](../../../tome-cults.lua#L817) | 普通鞋与合成鞋两条均将防御改为闪避，数字及换行不变。 |
| C09 | [tome-cults.lua:822](../../../tome-cults.lua#L822) | 普通鞋与合成鞋两条均将防御改为闪避，数字及换行不变。 |
| C05 | [tome-cults.lua:3807](../../../tome-cults.lua#L3807) | 将首次触发、后续几率、每目标每回合一次概括为一句玩家规则。 |
| C08 | [tome-orcs.lua:1411](../../../tome-orcs.lua#L1411) | 光明伤害改为光系伤害。 |
| C06 | [tome-orcs.lua:6410](../../../tome-orcs.lua#L6410) | 更正原先以“你”为主语的结论，统一用“目标”指代受伤、沉默和拉回对象，去掉 `%s` 前固定空格；保留自然到期、施加者仍在场及击退免疫限制。 |

## 源码证据与必要条件

主程序只经 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取 manifest 固定版本，没有以当前工作树或 HEAD 代替。DLC 从 SPEC 指定的 `/workspace/tome4-dlcs/<component>/tome-<component>` 只读取证；源码仓库／commit／版本 **unpinned**，文件哈希仅锚定本次可读内容，版本适用性仍待确认。已逐个复核原 source-anchors.json 中 C01–C09 所用文件 SHA-256 与逐行摘录，两者完全一致。

- C01：`Actor.lua` 的徒手门禁调用 `hasMassiveArmor()`；`Combat.lua` 只匹配 `armor.subtype == "massive"`，因此使用板甲而不扩大为重甲。
- C02–C04：欧尼路格 lore 的 `half-starved wolves` 与隐士对话原文核实了饥饿程度、`for me` 限定、`MORE AID` 和 `WHICH ELIXIR` 语境。
- C05：`KROG_WRATH.callbackOnDealDamage` 排除死亡目标、非正伤害与不能被震慑的目标；本回合尚无 `turn_procs.krog_wrath` 时绕过概率检验，随后按 `rng.percent(eff.power)` 判定，并以 `target.uid` 防止重复触发。`setEffect(EFF_STUNNED, 3, {apply_power=...})` 是震慑尝试，不把绕过随机几率说成绕过状态抵抗／豁免的保证。正文用“触发震慑”而非“必定震慑”。
- C06：`EXPLOSIVE_WOUND.on_timeout` 造成物理伤害；`deactivate` 在 `eff.dur >= 0`、来源不存在／已死／无坐标时直接返回，自然到期且来源仍在场才造成火焰伤害；`canBe("knockback")` 允许时调用 `pull(eff.src.x, eff.src.y, eff.range)`。正文恢复爆炸、飞回、拉回的动作，同时保留会改变结果的限制。
- C06 指代更正：撤回原先“以你为受伤和沉默主语”的结论。固定 core 的 `Game.lua:2552–2561` 中，`SHOW_CHARACTER_SHEET_CURSOR` 将光标目标传给 `CharacterSheet.new(target)`；`CharacterSheet.lua:40–46` 保存为 `self.actor`，`:478–485` 将其赋给局部 `player`，`:875–887` 对该角色的效果调用 `e.long_desc(player, p)`。因此效果描述可显示任意被查看角色，使用“目标”同时适用于玩家与 NPC。`并被沉默` 本身没有代词，所谓该片段混入第三人称的子意见不成立。
- C06 运行组合句法：实际将 `%s` 代入同文件现译“并被沉默”，得到“目标受到飞锯切割，每回合受到 12.34 物理伤害并被沉默。”；空串时为“目标受到飞锯切割，每回合受到 12.34 物理伤害。”。受伤／沉默与后文“将目标拉回”指向同一目标；去掉 `%s` 前固定空格后，两种组合均无标点前多余空格，参数顺序不变。
- C07：`INFERNO_NEXUS.callbackOnMeleeAttack` 仅在 `hitted` 时施加 `CURSED_FLAMES`；`callbackOnActBase` 在自身半径 10 内查找诅咒目标，每个目标以 50% 几率向其半径 1 内敌人传播，排除已受诅咒者及当回合已传播命中的目标；局部 `is_burning` 计算未被用作传播条件，故不要求接收者预先燃烧。调用 `FIREBURN.projector` 后于 tick end 施加诅咒。
- C07：`CURSED_FLAMES.on_timeout` 先执行 `eff.src:heal(eff.heal)` 与 `incVim(eff.vim)`，再检查带 `subtype.fire`、`power` 的负面效果；不再燃烧时移除诅咒。因此未燃烧的近战目标也可在移除前提供一次恢复，正文用“每个受诅咒敌人每回合恢复；不再燃烧时诅咒消失”覆盖此顺序，不错误限定为仅仍在燃烧时才恢复。核心固定版本 `FIREBURN` 默认总伤害一半立即造成，余下一半在 3 回合内造成；正文只写燃烧和总伤害，分配留在证据。
- C08：水晶刀刃的 on-hit 实际调用 `DamageType.LIGHT`，并提供 `combat_critical_power`。本次只修该条，与组件现有光系伤害用语对齐，不改术语 scope 或策略。
- C09：两双鞋的 `special_desc` 对应 `EFF_SHOES_SLOWLY`；该效果分别向 `combat_def` 和 `combat_armor` 添加 `stacks * 2`，叠加上限 12。因此两条均写闪避和护甲，而非统称防御。

### 已核验源码锚点

| 锚点 | 公开源码路径／行 | SHA-256 |
| --- | --- | --- |
| core-brawler-desc | `game/modules/tome/data/birth/classes/warrior.lua:339–346` | `f1206f33a02b0707c23c64febed3bfb940dcf1e7b26599fd054e125a185910d3` |
| core-unarmed-gate | `game/modules/tome/class/Actor.lua:5785–5800` | `e839397f675ca77d46aa345b81ea49c341c7109b4d3064e6b3598639be5fa711` |
| core-massive-check | `game/modules/tome/class/interface/Combat.lua:2691–2701` | `0cfaba3995f19a0ddb9e716b2ae8ab68e916c1e1784bb753f72b159bfd17af13` |
| core-hermit-intro | `game/modules/tome/data/chats/alchemist-hermit.lua:125–160` | `970170cf3b4da2358f4119a08ea333fbfda95ad98ac64a3d5d6d0c26bae205d8` |
| core-hermit-repeat | `game/modules/tome/data/chats/alchemist-hermit.lua:272–285` | `970170cf3b4da2358f4119a08ea333fbfda95ad98ac64a3d5d6d0c26bae205d8` |
| core-hermit-choice | `game/modules/tome/data/chats/alchemist-hermit.lua:435–449` | `970170cf3b4da2358f4119a08ea333fbfda95ad98ac64a3d5d6d0c26bae205d8` |
| ashes-onilug | `ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:319–333` | `d3adada58124ab822393a43a8ec21060a5d465bfca69ff02d4b46df31b92e142` |
| ashes-devouring-flames | `ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/heart-of-fire.lua:101–147` | `9169ec6910a96af6ce469ef88c4b257165955f96ce7828c8508e2d36372a92b5` |
| cults-krog-wrath | `cults/tome-cults/data/timed_effects.lua:1936–1963` | `0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c` |
| cults-slow-shoes | `cults/tome-cults/data/general/objects/world-artifacts.lua:938–990` | `27af5b2ae30c5b2db7f1d585b8334bc28ee1284e771a8a9f5c198f892edbc92a` |
| cults-slow-shoes-effect | `cults/tome-cults/data/timed_effects.lua:2260–2296` | `0d3139ebf8a4b1add13f340c166f42efbd90c26c901b7999eb0608f82d76ac9c` |
| orcs-explosive-saw | `orcs/tome-orcs/data/timed_effects/physical.lua:445–474` | `d3332099148953cd03cb1d14c2bdd2390e091905144fd49311d9bd8c33b6e37e` |
| orcs-crystal-edge | `orcs/tome-orcs/data/general/objects/tinkers/smith.lua:106–137` | `f3bef5246737c0b052dc544df65f5f899dbaaa54ace6357297e7afae41559dc9` |
| ashes-cursed-flames | `ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua:168–193` | `eb183d02dba83a010aac5c7938cf590307b9f99a88de9b7222be7e58f4863f8d` |
| core-fireburn | `game/modules/tome/data/damage_types.lua:1186–1205` | `67ecccac9c811dcd18607d573c6a1efd9762e13cea14db005ef1256109b7f479` |
| core-cursor-character-sheet | `game/modules/tome/class/Game.lua:2552–2561` | `dcd6dc85d9b2cf74741e82ac9156128b782193d23a459d53f7cda324b099092a` |
| core-character-sheet-effect-description | `game/modules/tome/dialogs/CharacterSheet.lua:40–46, 478–485, 875–887` | `d6c8555c085249893e02be80b079079f6c6a98f2533ac35e2085c724ea5f2582` |

## 验证与交接

- F01 本轮验证：`python3 -B tools/i18n proposal --workset .artifacts/i18n/quality-fix-20261013/orcs.workset.json --proposal .artifacts/i18n/quality-fix-20261013/orcs.proposal.json --strict` 覆盖 2/2，0 errors／warnings；`python3 -B tools/i18n lint --strict` 检查 30,308 条，0 errors／warnings。空串及“并被沉默”两种代入均通过；将本次 C06 target 反向替换后，tome-orcs.lua 与本 dispatch 起点逐字节一致，其他 10 条 target 及所有范围外已有文件哈希保持。
- F01 小修复：本次 fresh EXECUTOR 仅改 C06 target、对应说明及 orcs proposal；固定 core 角色表调用链的文件哈希和逐行摘录已重新核验。其他 10 条 target 及用户改动保留，不重复构建／运行键检查，最终复审由宿主负责。

- `python3 -B tools/i18n doctor`：LuaJIT／Lua 5.1、LPeg 0.10.2、固定仓库 pin 通过；三个 DLC 的 source-unpinned 提示如实保留。
- `python3 -B tools/i18n lint --strict`：最终候选 30,308 条，0 errors、0 warnings。
- 四组件 `python3 -B tools/i18n proposal --workset ... --proposal ... --strict`：tome 4/4、ashes-urhrok 2/2、cults 3/3、orcs 2/2，均 0 errors／warnings。输入是从冻结 confirmed-workset 派生的 repair adapter，不代表新源码提取或覆盖率评估。
- LuaJIT 前后逐记录比较：恰好 11 条 target 改动；所有其他字段、参数占位符及顺序、markup、换行与缩进不变。将 11 个 target 字面量反向替换后，四文件逐字节匹配任务前 baseline，证明 target 外格式也不变。
- `python3 -B tools/scan_runtime_collisions.py --out-dir .artifacts/i18n/quality-fix-20261013/runtime-collisions`：最终候选跨组件运行键冲突 0。
- `python3 -B tools/classify_runtime_keys.py --out-dir .artifacts/i18n/quality-fix-20261013/runtime-classification`：1,711 个重复键，全部 A 类且运行值一致；B/C 均 0。
- `git diff --check` 及新增本文件的 `git diff --no-index --check`：无空白诊断。
- 显示文字会改变构建产物；依宿主补正与当前指令，核心及受影响 DLC 的严格 addon 构建由 ORCHESTRATOR 补跑。EXECUTOR 不宣称构建或正式任务整体已经完成；独立复审、候选冻结、preflight、FINAL_REVIEW、状态闭合与生命周期管理亦由 ORCHESTRATOR 负责。
- 校验工件、Lua baseline、内容不变量结果与完整源码摘录保存在 `.artifacts/i18n/quality-fix-20261013/`；本文件包含人工判断与完整哈希，可受跟踪保存。
- 文件范围核对：四 Lua 的字节级改动仅为冻结 target；任务前用户文件哈希均保持，宿主在同一次运行中补正的 SPEC.md 为已说明的外部变更，本 EXECUTOR 未写入该文件。
- 未决：DLC 的源码版本适用性未固定；未扩展修复原报告 advisory/pending。没有其他 EXECUTOR 范围内阻断问题。
