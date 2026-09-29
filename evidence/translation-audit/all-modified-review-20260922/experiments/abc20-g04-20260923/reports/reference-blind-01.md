| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03292 | 未发现问题 | 权重乘数含义准确 |
| entry-03293 | 未发现问题 | 禁用与默认权重含义准确 |
| entry-03294 | 存在问题 | C01：手动重启的操作条件扩大 |
| entry-03295 | 未发现问题 | 对话标题译名与冻结语境一致 |
| entry-03296 | 存在问题 | C02：随机选取被写成每次必然施放 |
| entry-03297 | 未发现问题 | 保留奥术格斗触发这一前提 |
| entry-03298 | 未发现问题 | 已学会及适用范围准确 |
| entry-03299 | 存在问题 | C03–C05：时间下限、灾害状态及公平治理信息变化 |
| entry-03300 | 未发现问题 | 震慑减速、减伤描述符合固定源码 |
| entry-03301 | 未发现问题 | 时代、力量来源及征服程度准确 |
| entry-03302 | 未发现问题 | 保留公开认知与隐藏群体传闻的对照 |
| entry-03303 | 未发现问题 | 宝石爆炸与傀儡保护含义保留 |
| entry-03305 | 未发现问题 | 死灵术历史及造物危害含义保留 |
| entry-03306 | 未发现问题 | 灾害、时间与责任含义保留；孤立引号省略不构成缺陷 |
| entry-03307 | 未发现问题 | 诅咒、控制困难及仇恨驱动含义保留 |
| entry-03308 | 未发现问题 | 地宫与新盘踞力量的叙述准确 |
| entry-03309 | 存在问题 | C06：可发现神器的事实被降为传闻 |
| entry-03310 | 未发现问题 | 职业特点与训练结果准确 |
| entry-03311 | 未发现问题 | 兽人训练及巨魔变化准确 |
| entry-03312 | 未发现问题 | 幸运脚与半身人的反感语气保留 |
| entry-03313 | 未发现问题 | 镶嵌对象及用途含义保留 |
| entry-03314 | 未发现问题 | 身体训练及战斗能力准确 |
| entry-03315 | 未发现问题 | 元素性质与发疯传闻准确 |
| entry-03316 | 未发现问题 | 普通斗篷与魔法斗篷功能准确 |
| entry-03317 | 存在问题 | C07：两种具体足部装备被泛化 |
| entry-03318 | 未发现问题 | 已备弹药含义准确 |
| entry-03319 | 存在问题 | C08：沿袭上游错误切换键 |
| entry-03320 | 存在问题 | C09：沿袭上游错误切换键 |
| entry-03321 | 存在问题 | C10：沿袭上游错误切换键 |
| entry-03322 | 存在问题 | C11：不消耗回合的断言不符合物品使用链 |
| entry-03323 | 存在问题 | C12–C13：灾变性质及人口变化信息不准确 |
| entry-03324 | 存在问题 | C14–C26：叙述逻辑、种族特征、时间及行为信息变化 |
| entry-03325 | 存在问题 | C27–C32：贿赂程度、未知原因、公会身份等信息变化 |
| entry-03326 | 存在问题 | C33：图书管理员身份遗漏 |
| entry-03327 | 待确认 | C34：无法确认日志参数是否为目录 |
| entry-03328 | 待确认 | C35：无法确认日志参数是否为目录 |
| entry-03329 | 未发现问题 | tags 表要求及示例保留 |
| entry-03330 | 未发现问题 | 上传错误含义准确 |
| entry-03331 | 未发现问题 | 更新与预览图上传成功含义准确 |
| entry-03332 | 未发现问题 | 更新上传成功含义准确 |

以下状态均为本次独立审核观察。源码简称 `G/` 表示 `game/modules/tome/`，`E/` 表示 `game/engines/default/`；版本均为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`。纯语义问题以冻结 `INPUT.md` 对应条目、段落为证据。

### C01 | entry-03294 | 存在问题

原文：“After turning them on here”；译文：“在你在这里调整之后”。

**confirmed，译文扩大操作条件。** 原文要求在这里重新开启光环后，手动关闭并重启持续技能；“调整之后”也包含隐藏光环的操作。

`G/dialogs/shimmer/ShimmerRemoveSustains.lua:94` 的 `toggleAura` 在隐藏分支直接移除粒子；恢复分支才考虑重启技能。第 103 行跳过 `no_sustain_autoreset` 技能的自动重启，第 155 行将这些技能标黄。因此手动重启要求具体对应恢复显示，不能泛指所有调整。

### C02 | entry-03296 | 存在问题

原文：“a spell selected automatically with each attack”；译文：“每次攻击时会随机施放一个法术”。

**confirmed，译文把选取写成必然施放。** `G/data/talents/techniques/magical-combat.lua:78` 的 `do_trigger` 先取得触发概率，第 86 行通过 `rng.percent(chance)` 后才建立候选并随机选择；第 124 行才执行 `forceUseTalent`。还存在资源与可用法术检查。

英文对话提示本身较简略，但明确使用的是“selected”；译文进一步作出了每次攻击都会施法的断言。

### C03 | entry-03299 | 存在问题

原文：“over ten thousand years”；译文：“长达一万年”。

**confirmed，数量下限遗漏。** 冻结条目第二段及 `G/init.lua:30` 明确表示超过一万年，译文只给出一万年这一时长。

### C04 | entry-03299 | 存在问题

原文：“The last effects … have been tamed”；译文：“所造成的影响已经渐渐减轻”。

**confirmed，灾害控制状态发生变化。** `G/init.lua:31` 表示最后的残余影响已经得到控制；译文表示影响逐渐减轻，遗漏“最后残余”及已被控制的结果状态。后句的大地缓慢恢复不能替代这项信息。

### C05 | entry-03299 | 存在问题

原文：“ruled the kingdoms with fairness”；译文：“王国天下太平”。

**confirmed，治理方式被替换。** `G/init.lua:34` 说明两位统治者公平治理；“天下太平”描述社会安定，没有保留公平性，也不能从原句推出。

### C06 | entry-03309 | 存在问题

原文：“Some Sher'Tul artifacts can still be found”；译文：“虽然有人说还能……找到夏·图尔的神器”。

**confirmed，事实陈述被降为传闻。** `G/init.lua:102` 的传闻限定“it is said”只修饰不可轻率对待神器的警告。译文额外把神器仍可发现这一陈述也归为“有人说”。

### C07 | entry-03317 | 存在问题

原文：“Sandals or boots”；译文：“鞋子”。

**confirmed，具体装备种类遗漏。** `G/load.lua:131` 将这段文字注册为 `FEET` 装备栏说明，明确列出凉鞋和靴子。译文保留穿戴部位，但丢失了两个具体种类；这是信息泛化，不只是措辞偏好。

### C08 | entry-03319 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** `G/load.lua:135` 的英文已经写成 X；固定版本 `E/data/keybinds/inventory.lua:66` 定义 `QUICK_SWITCH_WEAPON` 的默认绑定为 `sym:=q:false:false:false:false`。

`G/load.lua:114` 加载 inventory 键位定义；同版本不存在模块侧 `G/data/keybinds/inventory.lua` 覆盖文件。问题是默认按键说明失实，不是译文大小写错误。

### C09 | entry-03320 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** 本条对应 `G/load.lua:136` 的第二套副手说明；默认切换动作仍由 `E/data/keybinds/inventory.lua:66` 绑定至 Q。副手装备及技能条件部分未发现问题。

### C10 | entry-03321 | 存在问题

原文：“Press 'x'”；译文：“按 X 键”。

**confirmed，沿袭上游的操作说明错误。** 本条对应 `G/load.lua:137` 的第二套灵能聚焦物说明；默认切换动作同样绑定至 Q，证据为 `E/data/keybinds/inventory.lua:66`。念动力持物及增益用途部分未发现问题。

### C11 | entry-03322 | 存在问题

原文：“instantly used”；译文：“即时使用（不消耗回合）”。

**confirmed，译文增加了不成立的统一免耗时解释；上游措辞也有误导性。**

`G/data/talents/uber/dex.lua:117` 的 `no_energy=true` 属于无影手技能自身。其 action 在第 132 行调用 `playerUseObject`，后者在 `G/class/Player.lua:1483` 调用物品的 `use`。

`G/class/Object.lua:338` 只有在物品 `use_no_energy` 或使用结果 `ret.no_energy` 成立时才免耗时，否则调用 `useEnergy`。`use_talent` 分支在第 278 行读取的是物品所施放技能的 `no_energy`。无影手的物品栏初始化也没有统一设置零耗时。

因此物品是否耗时仍由其自身决定，不能统一解释为“不消耗回合”。

### C12 | entry-03323 | 存在问题

原文：“the Cataclysm”；译文：“大爆炸”。

**confirmed，译文给灾变加入了爆炸性质，并模糊了两个事件的区别。** 冻结条目第三段指土地沉海的 Cataclysm。`G/init.lua:132` 明确将其描述为魔法大爆炸数百年后再次撕裂大陆的灾变；第 131 行也将 Spellblaze 与 Cataclysm 并列。现有证据没有将后者定义为一次爆炸。

这项判断依据事件语境，不要求建立新的全局术语译名。

### C13 | entry-03323 | 存在问题

原文：“are few in number since”；译文：“数量急剧减少”。

**confirmed，人口状态被改成带速度的变化过程。** 冻结条目第三段说明灾变后肖尔塔人数量稀少，没有说明人口减少的速度。“急剧”是译文新增判断，而当前数量稀少的状态也未直接保留。

### C14 | entry-03324 | 存在问题

原文：“No text would be complete without at least a brief note”；译文：“没有任何文字可以诠释”。

**confirmed，开篇逻辑改变。** 冻结条目第一段说明完整著述应至少简述这些种族；译文却表示文字无法诠释它们，将“必须提及”变成“无法描述”。

### C15 | entry-03324 | 存在问题

原文：“do not hold any civilised society of note”；译文：“没有任何文化遗留”。

**confirmed，描述对象变化。** 第一段讨论这些种族是否具有值得一提的文明社会；“文化遗留”讨论文化遗产或遗存。社会组织状态的信息没有保留。

### C16 | entry-03324 | 存在问题

原文：“a thick, solid hide”；译文：“厚厚的煤黑色或花岗岩状的外观”。

**confirmed，身体结构信息遗漏。** 第二段说明石巨魔具有厚实坚固的皮肤，其外观类似煤或花岗岩。译文把“厚厚的”接到“外观”，没有明确保留厚实坚固的皮肤这一特征。

### C17 | entry-03324 | 存在问题

原文：“a more advanced form of speech”；译文：“更为敏捷的速度”。

**confirmed，语言能力误译成速度。** 第二段先比较森林巨魔与山地同类的语言能力，再另述移动更快。译文连续描述速度，遗漏了语言更发达这一独立特征。

### C18 | entry-03324 | 存在问题

原文：“towards the end of the Age of Pyre”；译文：“在烈火纪时”。

**confirmed，时代内的时间限定遗漏。** 第二段将兽人训练巨魔的时间限定在烈火纪接近结束时，译文扩大到了整个时代。

### C19 | entry-03324 | 存在问题

原文：“their tails extend several feet further”；译文：“他们的尾巴可能更长”。

**confirmed，确定的长度关系变成不确定描述。** 第四段说明陆地站立高度约六英尺，尾巴还延伸数英尺。译文既遗漏“数英尺”，又加入原文没有的“可能”。

### C20 | entry-03324 | 存在问题

原文：“the last few hundred years”；译文：“近一百年”。

**confirmed，时间数量错误。** 第四段的数百年被缩短为一百年。

### C21 | entry-03324 | 存在问题

原文：“only more recently have they been interpreted as more than … fantasies”；译文：“越来越多的证据表明他们并不是……幻觉”。

**confirmed，认识转变的时间信息被替换。** 第四段说明直到较近时期，人们才不再把相关记载视为醉酒水手的幻想。译文改成证据数量持续增加，没有保留“直到较近时期才”的限制。

### C22 | entry-03324 | 存在问题

原文：“formed from layers of thick shark-hide”；译文：“用鲨鱼皮制成”。

**confirmed，材料结构遗漏。** 第四段明确描述多层厚鲨鱼皮，译文只保留材质，没有保留层叠结构和厚度。

### C23 | entry-03324 | 存在问题

原文：“supported by certain studies by Shaloren archmages”；译文：“由永恒精灵魔导师们得出的”。

**confirmed，研究支持关系变成理论提出关系。** 第五段只说这些研究支持主要理论，没有说明该理论由这些法师提出或得出。译文改变了证据来源与观点归属的关系。

### C24 | entry-03324 | 存在问题

原文：“react oddly with our atmosphere”；译文：“表现出超乎我们想象的形态”。

**confirmed，与埃亚尔大气发生反应的信息遗漏。** 第五段将异常现象与血肉、皮肤接触当地大气联系起来；译文改为一般的奇异外形描述，丢失环境作用关系。

### C25 | entry-03324 | 存在问题

原文：“release hideous acids or belching clouds of darkness”；译文：“藏在酸雾里或是可怕的黑暗中”。

**confirmed，释放行为误成藏身状态。** 第五段说恶魔释放酸液或喷吐黑暗云团；译文表示恶魔躲藏在酸雾或黑暗中，改变了行为及其作用关系。

### C26 | entry-03324 | 存在问题

原文：“attacking communities”；译文：“攻击市民”。

**confirmed，攻击对象被缩小。** 第三段讨论巨人下到低地袭扰人类聚落，与偷走农场动物并列；译文改为攻击市民个人，没有保留聚落或社区这一对象。

### C27 | entry-03325 | 存在问题

原文：“unless hefty bribes are paid”；译文：“除非你给他们点好处”。

**confirmed，程度信息失真。** 第一段明确要求相当可观的贿赂，“点好处”却弱化为少量利益，改变了矮人透露自身信息的条件程度。

### C28 | entry-03325 | 存在问题

原文：“for no known reason”；译文：“无缘无故”。

**confirmed，未知原因被改成没有原因。** 第一段只限定外界不知道断绝联系的原因，译文作出了客观上没有缘由的判断。

### C29 | entry-03325 | 存在问题

原文：“several of their guild leaders”；译文：“他们的主要领导人”。

**confirmed，人物所属机构和数量信息遗漏。** 第一段明确是数位公会领袖；译文没有保留公会身份，并添加“主要”这一地位判断。后文公会委员会语境也不能补回会面对象的具体身份。

### C30 | entry-03325 | 存在问题

原文：“Their females … can usually be identified by the beads”；译文：“他们的性别……可以通过……珠饰来辨认”。

**confirmed，识别标志与女性的对应关系遗漏。** 第二段告诉读者珠饰通常用于识别女性；译文只说珠饰可辨性别，没有说明该标志对应女性。

### C31 | entry-03325 | 存在问题

原文：“allow no outsiders in”；译文：“从不欢迎外来者”。

**confirmed，准入禁令被弱化为态度。** 第四段说明不准外人进入，因此派商队到外界售卖；不欢迎外人并不等于禁止进入，改变了限制性质。

### C32 | entry-03325 | 存在问题

原文：“a great deal of young dwarves who venture”；译文：“越来越多的年轻矮人更加倾向于……出去冒险”。

**confirmed，新增数量增长及偏好增强趋势。** 第五段只说明有很多年轻矮人外出冒险；原文没有前后比较，也没有数量持续增加或意愿增强的判断。

### C33 | entry-03326 | 存在问题

原文：“appointing its own librarians”；译文：“指派了自己的记录者”。

**confirmed，具体身份遗漏。** 第一段说明被任命者是图书管理员，随后立即讨论该图书馆是否存在。“记录者”保留了他们记录故事的工作，却没有保留其与图书馆相联系的具体身份。

### C34 | entry-03327 | 待确认

原文：“Logs written to %s”；译文：“日志目录：%s”。

**pending。** 原文只说明日志写入某处，译文将 `%s` 限定为目录。需要 `tome-addon-dev/overload/engine/i18nhelper/ArrangeText.lua` 的格式化调用参数及日志写入逻辑，确认参数代表目录还是单个文件。

`source-access.json` 明确将 `addon-dev` 列为源码不可用组件，冻结邻近译文不能证明参数类型。单个 `%s` 及两行信息结构均保留，没有已证实的格式错误。

### C35 | entry-03328 | 待确认

原文：“Logs written to %s”；译文：“日志目录：%s”。

**pending。** 本条是重新编排完成后的另一处提示，仍需核验其独立调用点的 `%s` 参数是否为目录。该组件源码缺失，不能假定它与检查完成提示一定传入同类路径。

占位符及换行结构本身未发现问题。

---

共复核 **40 条：存在问题 13 条、待确认 2 条、仅建议 0 条、未发现问题 25 条**。全部条目的占位符和受检格式标记序列一致；上述缺陷均未提供修改方案。

实际读取范围如下。冻结包根目录为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g04-20260923/`

读取了该目录内：

- `INPUT.md`
- `entries.json`
- `context.lua`
- `source-access.json`
- `sources/game/modules/tome/dialogs/orders/Talents.lua`
- `sources/game/modules/tome/dialogs/shimmer/ShimmerRemoveSustains.lua`
- `sources/game/modules/tome/dialogs/talents/MagicalCombatArcaneCombat.lua`
- `sources/game/modules/tome/init.lua`
- `sources/game/modules/tome/load.lua`

五份冻结源码均与清单 SHA-256 匹配，并另外通过指定 commit 的 `git show` 确认一致。

额外源码全部通过 `/workspace/t-engine4` 的指定 commit 读取，路径及引入依据如下：

| 实际读取的额外源码路径 | 已读调用、符号或加载关系 |
|---|---|
| `G/data/talents.lua` | `G/load.lua:174` 的 `ActorTalents:loadDefinition` |
| `G/data/timed_effects.lua` | `G/load.lua:177` 的状态定义加载 |
| `G/data/lore/lore.lua` | `G/load.lua:111` 的 lore 定义加载 |
| `G/data/talents/techniques/techniques.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/talents/spells/spells.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/talents/uber/uber.lua` | `data/talents.lua` 的明确 `load` |
| `G/data/timed_effects/physical.lua` | `data/timed_effects.lua` 的明确 `load`；核验震慑 |
| `G/data/talents/techniques/magical-combat.lua` | techniques 分类文件的明确 `load`；核验奥术格斗 |
| `G/data/talents/uber/cun.lua` | uber 分类文件的明确 `load`；查找无影手，未找到 |
| `G/data/talents/uber/dex.lua` | uber 分类文件的明确 `load`；找到并核验无影手 |
| `G/data/talents/spells/explosives.lua` | spells 分类文件的明确 `load`；核验宝石爆炸 |
| `G/data/talents/spells/stone-alchemy.lua` | spells 分类文件的明确 `load`；核验宝石镶嵌 |
| `G/class/Player.lua` | 无影手 action 调用 `playerUseObject` |
| `G/dialogs/SwiftHandsUse.lua` | 无影手 action 的明确 `require` |
| `G/class/Object.lua` | `playerUseObject` 调用物品 `o:use` |
| `G/class/Actor.lua` | Player 的明确继承引用；核验耗时处理 |
| `G/dialogs/SwiftHands.lua` | 无影手管理技能的明确 `require` |
| `E/engine/interface/ActorInventory.lua` | `load.lua` 的明确 `require` 及无影手 `initBody` 调用 |
| `E/engine/KeyBind.lua` | `load.lua` 的明确 `require`；核验键位加载路径 |
| `G/data/keybinds/tome.lua` | `load.lua` 的 `KeyBind:load` 包含 tome |
| `E/data/keybinds/inventory.lua` | 同一加载调用包含 inventory；核验默认切换键 |

另尝试读取同 commit 的 `G/data/keybinds/inventory.lua`，Git 明确返回该路径不存在；没有读取其他版本补替。

专属临时目录为 `/tmp/abc20-g04-20260923-554jakm3`，其中仅保存本次自行读取的固定版本源码副本。未读取他人临时材料、其他审核报告或当前译文文件，未创建子 agent，未修改仓库，未发生读取范围越界。

无法核验项为 C34、C35 的插件运行时参数。本包没有可读 DLC 源码，也未以本体 commit 代替 DLC 版本。本报告仅交付审核观察，不构成生产完成认证。
