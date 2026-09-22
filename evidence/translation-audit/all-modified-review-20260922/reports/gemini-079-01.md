### batch-079 译文复核报告

#### 预检与元数据核验
- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-079.md`
- **文件 SHA-256 核验**：`af54359ebfa376cae9cc35faf3cc4a152dcf6b5fdc6a2fd5322bddbfd4e844b0`（核验一致）
- **条目范围**：`entry-02538` 至 `entry-02571`，共 34 条，已实现逐条全覆盖核验。
- **源码比对基准**：
  - engine / tome 公开源码固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 译文仓库比对终点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`

---

### 逐条复核记录

#### entry-02538
- **位置**：`mod-tome.lua:33287`
- **Section**：`mod-tome/data/texts/tutorial/stats-tier/tier4.lua`
- **复核结论**：细微观察
- **依据**：
  1. 原文：“Ahead are a series of bored elves who will happily blast you with whatever spell they have handy. Examine the tooltip of each effect they inflict on you.”
  2. 译文：“前面有几个无聊的精灵，他们会很高兴在你身上施展各种他们所学会的法术，测试一下这些持续效果在你身上的作用，注意查看鼠标提示。”
  3. 译文中增补了「测试一下这些持续效果在你身上的作用」这句原句中不存在的从句，并将「Examine the tooltip of each effect they inflict on you」（仔细查看他们施加在你身上的每种效果的鼠标提示）略缩意译为「注意查看鼠标提示」，未严格对应「每种效果」。末尾换行与空格保留完整，符合新手教程指引大意，但有轻微意译增删。

#### entry-02539
- **位置**：`mod-tome.lua:33589`
- **Section**：`mod-tome/data/texts/unlock-adventurer.lua`
- **复核结论**：未发现问题
- **依据**：核对固定 commit `game/modules/tome/data/birth/classes/adventurer.lua` 源码，冒险家开局设定为 `unused_talents_types = 7`，且拥有全技能树列表待解锁，译文「初始拥有 7 点技能树解锁点，并且可以解锁游戏中的任何职业技能树和通用技能树」准确反映机制；颜色码 `#LIGHT_GREEN#...#WHITE#` 与加粗标签 `#{bold}#...#{normal}#` 配对完整无误。

#### entry-02540
- **位置**：`mod-tome.lua:33604`
- **Section**：`mod-tome/data/texts/unlock-afflicted_cursed.lua`
- **复核结论**：未发现问题
- **依据**：职业名「被诅咒者（Cursed）」与系别「痛苦系（Afflicted）」契合术语规范，颜色控制符 `#LIGHT_GREEN#` 格式完整。

#### entry-02541
- **位置**：`mod-tome.lua:33605`
- **Section**：`mod-tome/data/texts/unlock-afflicted_cursed.lua`
- **复核结论**：细微观察
- **依据**：
  1. 原文第 6 行包含 `You have "lifted" the curse of Ben Cruthdar.`，其中 `"lifted"` 带引号以表达通过击杀本·克鲁塞达尔解除诅咒的双关/讽刺意味；译文处理为「你战胜了本·克鲁塞达尔的诅咒」，未保留引号和双关语气，属于轻微语气平化。
  2. 机制与专名方面，Gloom 译为「黑暗光环」、hate 译为「仇恨值」、stunning 译为「震慑」、confusing 译为「混乱」，与固定源码及术语表一致；`#LIGHT_GREEN#...#WHITE#` 及 `#YELLOW#...#WHITE#` 标签闭合准确。

#### entry-02542
- **位置**：`mod-tome.lua:33642`
- **Section**：`mod-tome/data/texts/unlock-afflicted_doomed.lua`
- **复核结论**：未发现问题
- **依据**：职业「末日使者（Doomed）」与类别「痛苦系（Afflicted）」译名准确，颜色标签格式与源码一致。

#### entry-02543
- **位置**：`mod-tome.lua:33682`
- **Section**：`mod-tome/data/texts/unlock-birth_transmo_chest.lua`
- **复核结论**：未发现问题
- **依据**：专名「Transmogrification Chest」对应「转化之盒」，颜色标记 `#LIGHT_GREEN#` 正确。

#### entry-02544
- **位置**：`mod-tome.lua:33710`
- **Section**：`mod-tome/data/texts/unlock-campaign_arena.lua`
- **复核结论**：未发现问题
- **依据**：战役标题「The Arena: Challenge of the Master」准确译为「竞技场：擂主的挑战」，颜色标签一致。

#### entry-02545
- **位置**：`mod-tome.lua:33711`
- **Section**：`mod-tome/data/texts/unlock-campaign_arena.lua`
- **复核结论**：细微观察
- **依据**：
  1. 原文前两句为同位阐释结构：“The arena, a way of violent entertainment. A delight for the audience, a source of wealth and glory. A place where...”，译文第二句「为了取悦观众，获得财富和荣耀的地方」带有目的状语误译痕迹（A delight for the audience 是名词性短语而不是目的状语从句），形成无主语句式，语法略显断裂。
  2. 特征列表条目「Exclusive scoring system... Scores are kept for bragging rights!」意译为「这里有一个积分系统……分数可是你向别人夸耀的资本哦！」，口语语气词「哦！」偏口语化；「Pure hack and slash MAYHEM!」译为口号式「尽情砍杀吧！」。
  3. 特性末尾无 `#WHITE#` 与英文源码一致，战役核心规则翻译准确。

#### entry-02546
- **位置**：`mod-tome.lua:33739`
- **Section**：`mod-tome/data/texts/unlock-campaign_infinite_dungeon.lua`
- **复核结论**：未发现问题
- **依据**：战役标题「Infinite Dungeon: The Neverending Descent」译为「无尽地下城：永无止境的下降」，颜色标签无误。

#### entry-02547
- **位置**：`mod-tome.lua:33740`
- **Section**：`mod-tome/data/texts/unlock-campaign_infinite_dungeon.lua`
- **复核结论**：未发现问题
- **依据**：
  1. 设定专名「Age of Haze」译为「混沌纪」，「Godslayers」译为「弑神者」，神祇「Ralkur」译为「瑞尔克」，均与背景设定及术语快照一致。
  2. 机制表述「No win condition: you WILL die in the dungeon...」准确传达无尽地下城无通关条件、以深入层数衡量成绩的核心玩法。
  3. 颜色标签 `#LIGHT_GREEN#...#WHITE#` 与 `#YELLOW#...#WHITE#` 配对闭合完整。

#### entry-02548
- **位置**：`mod-tome.lua:33769`
- **Section**：`mod-tome/data/texts/unlock-chronomancer_paradox_mage.lua`
- **复核结论**：未发现问题
- **依据**：职业「时空法师（Paradox Mage）」与类别「时空系（Chronomancer）」符合标准术语，颜色标签完整。

#### entry-02549
- **位置**：`mod-tome.lua:33803`
- **Section**：`mod-tome/data/texts/unlock-chronomancer_temporal_warden.lua`
- **复核结论**：未发现问题
- **依据**：职业「时空守卫（Temporal Warden）」与类别「时空系（Chronomancer）」符合标准术语，颜色标签完整。

#### entry-02550
- **位置**：`mod-tome.lua:33804`
- **Section**：`mod-tome/data/texts/unlock-chronomancer_temporal_warden.lua`
- **复核结论**：未发现问题
- **依据**：
  1. 叙事文本将「fabric that holds the universe together」译为「维系宇宙的经纬」，贴切典雅。
  2. 职业机制「Dual-wield a medium sized and a small weapon or attack from afar with your ranged weapon skills」准确译出时空守卫主副手双持与弓箭切换的机制。
  3. 核心资源「Paradox」译为「紊乱值」，标签 `#LIGHT_GREEN#...#WHITE#` 与 `#YELLOW#...#WHITE#` 格式正确。

#### entry-02551
- **位置**：`mod-tome.lua:33837`
- **Section**：`mod-tome/data/texts/unlock-corrupter_corruptor.lua`
- **复核结论**：未发现问题
- **依据**：职业「腐化者（Corruptor）」与类别「堕落系（Defiler）」准确一致，颜色标记正确。

#### entry-02552
- **位置**：`mod-tome.lua:33838`
- **Section**：`mod-tome/data/texts/unlock-corrupter_corruptor.lua`
- **复核结论**：存在疑点
- **依据**：
  1. 原文第 2 句：“Corruptors are mages that deal in dark, blighted, demonic magic to attain their goals.”
  2. 译文：“腐化者是使用黑暗、枯萎和恶魔法术来达到目的法师。”
  3. 「达到目的法师」漏掉定语助词「的」，存在明显语病，应为「达到目的的法师」。
  4. 其余部分中，「Grand Corruptor」译为「大腐化者」，「Fearscape」译为「恶魔空间」，「vim」译为「活力值/活力」，标签闭合无误。

#### entry-02553
- **位置**：`mod-tome.lua:33873`
- **Section**：`mod-tome/data/texts/unlock-corrupter_reaver.lua`
- **复核结论**：未发现问题
- **依据**：职业「收割者（Reaver）」与类别「堕落系（Defiler）」译名规范，颜色标签无误。

#### entry-02554
- **位置**：`mod-tome.lua:33874`
- **Section**：`mod-tome/data/texts/unlock-corrupter_reaver.lua`
- **复核结论**：未发现问题
- **依据**：
  1. 解锁条件「slain numerous humanoids」译为「杀死了许多人形生物」（对应击杀 1000 个人形生物的解锁事实）。
  2. 机制「heavy melee with spellcasting support」译为「以法术辅助的重型近战职业」，「power of bones」对应白骨系技能。
  3. 资源「vim」对应「活力值/活力」，颜色标签与分段完整。

#### entry-02555
- **位置**：`mod-tome.lua:34022`
- **Section**：`mod-tome/data/texts/unlock-difficulty_madness.lua`
- **复核结论**：细微观察
- **依据**：
  1. 排版与标点存在格式细节瑕疵：首段末尾出现半角空格加感叹号「之一 !」；特征标题后冒号前有多余空格「特点 :#YELLOW#」；末尾行 `#WHITE# 祝你玩的愉快，死的开心！` 颜色码后有多余空格，且「玩的愉快」应为「玩得愉快」。
  2. 机制术语比对：
     - `Insane mode` 译为「疯狂模式」（对应角色创建项 `Insane` -> `疯狂`）；
     - `Madness` 译为「绝望模式」（对应角色创建项 `Madness` -> `绝望`）；
     - `Roguelike or Adventure permadeath mode` 译为「永久死亡模式或冒险模式」，对应游戏出生选项中 `Roguelike`（永久死亡模式）与 `Adventure`（冒险模式），机制概念完全对齐。

#### entry-02556
- **位置**：`mod-tome.lua:34055`
- **Section**：`mod-tome/data/texts/unlock-divine_anorithil.lua`
- **复核结论**：未发现问题
- **依据**：职业「星月术士（Anorithil）」与类别「天空系（Celestial）」符合官方译名体系，颜色标签无误。

#### entry-02557
- **位置**：`mod-tome.lua:34056`
- **Section**：`mod-tome/data/texts/unlock-divine_anorithil.lua`
- **复核结论**：细微观察
- **依据**：
  1. 第 3 段「他们在与兽人部落的战斗中学会了如何同时掌控光与影的能量方法」存在句式杂糅（将「如何……掌控」与「……的方法」混杂拼接），宜调整为「学会了如何同时掌控光与影的能量」或「掌握了……的方法」。
  2. 其余专名及机制表述准确：「Orc Pride」为「兽人部落」，「Sun Chants and Moon Hymns」为「太阳赞歌和月亮圣诗」，「positive and negative energies」为「正能量和负能量」，标签配对完整。

#### entry-02558
- **位置**：`mod-tome.lua:34095`
- **Section**：`mod-tome/data/texts/unlock-divine_sun_paladin.lua`
- **复核结论**：未发现问题
- **依据**：职业「太阳骑士（Sun Paladin）」与类别「天空系（Celestial）」规范准确，颜色标签格式无误。

#### entry-02559
- **位置**：`mod-tome.lua:34096`
- **Section**：`mod-tome/data/texts/unlock-divine_sun_paladin.lua`
- **复核结论**：细微观察
- **依据**：
  1. 第 3 段第 1 句原文为 `Sun Paladins are warriors who are trained in special magic to focus the powers of the Sun.`，译文处理为「太阳骑士是受过特殊魔法训练的战士，他们学会聚焦太阳的力量施展他们的特殊能力」，在句末增补了「施展他们的特殊能力」（引申自文末资源说明），文义通顺但不完全镜像原文。
  2. 解锁地点「Gates of Morning」译为「晨曦之门」，技能树「Chants」译为「太阳赞歌」，资源「positive energy」译为「正能量」，标签闭合规范。

#### entry-02560
- **位置**：`mod-tome.lua:34135`
- **Section**：`mod-tome/data/texts/unlock-mage.lua`
- **复核结论**：未发现问题
- **依据**：职业「元素法师（Archmage）」与颜色代码 `#LIGHT_GREEN#` 格式正确。

#### entry-02561
- **位置**：`mod-tome.lua:34136`
- **Section**：`mod-tome/data/texts/unlock-mage.lua`
- **复核结论**：未发现问题
- **依据**：
  1. 背景设定专名均严格符合最新裁决与术语库：「Spellhunt」译为「魔法狩猎」；「Maj'Eyal」译为「马基·埃亚尔」；「Angolwen」统一为「安格利文」；「Age of Dusk」为「黄昏纪元」。
  2. 机制特征「Space and Time」、「Phantasms and Illusions」及资源「mana（法力值）」翻译精准，颜色代码闭合无误。

#### entry-02562
- **位置**：`mod-tome.lua:34173`
- **Section**：`mod-tome/data/texts/unlock-mage_cryomancer.lua`
- **复核结论**：未发现问题
- **依据**：技能类别「Ice」译为「冰系」，「Talent Category」译为「技能树」，颜色标记一致。

#### entry-02563
- **位置**：`mod-tome.lua:34201`
- **Section**：`mod-tome/data/texts/unlock-mage_geomancer.lua`
- **复核结论**：未发现问题
- **依据**：技能类别「Stone」译为「石系」，颜色标记一致。

#### entry-02564
- **位置**：`mod-tome.lua:34229`
- **Section**：`mod-tome/data/texts/unlock-mage_necromancer.lua`
- **复核结论**：未发现问题
- **依据**：职业「死灵法师（Necromancer）」与颜色标记匹配。

#### entry-02565
- **位置**：`mod-tome.lua:34230`
- **Section**：`mod-tome/data/texts/unlock-mage_necromancer.lua`
- **复核结论**：细微观察
- **依据**：
  1. 标点问题：第 4 段中「那些所谓的”高贵”的元素法师们」，前引号错误使用了右双引号 `”`（U+201D）而非左双引号 `“`（U+201C）。
  2. 文风重复：第 3 段中出现「这是一个黑暗的时代……来到了这个混乱的时代」，句尾短语重叠。
  3. 专名与机制：「Age of Dusk and the Age of Pyre」译为「黄昏纪元和烈火纪元」，终极目标「Lich / Lichdom」译为「巫妖 / 成为巫妖」，颜色标签正确。

#### entry-02566
- **位置**：`mod-tome.lua:34273`
- **Section**：`mod-tome/data/texts/unlock-mage_pyromancer.lua`
- **复核结论**：未发现问题
- **依据**：技能类别「Wildfire」译为「焱系」，严格符合术语库中技能树名称规范，颜色标签无误。

#### entry-02567
- **位置**：`mod-tome.lua:34301`
- **Section**：`mod-tome/data/texts/unlock-mage_tempest.lua`
- **复核结论**：未发现问题
- **依据**：技能类别「Storm」译为「风暴系」，颜色标签无误。

#### entry-02568
- **位置**：`mod-tome.lua:34302`
- **Section**：`mod-tome/data/texts/unlock-mage_tempest.lua`
- **复核结论**：细微观察
- **依据**：
  1. 技能列表格式差异：原文为 `- #YELLOW#Nova: #WHITE#...`，译文在 `#YELLOW#` 后插入了空格与全角冒号，变为 `- #YELLOW# 闪电新星：#WHITE# ...`，4 个列表项均带有内部空格；列表各条末尾标点未统一（第 1、3、4 项带句号，第 2 项无句号）。
  2. 开头「Since the dawn of time」译为「自始以来」，较为生硬。
  3. 机制核验：核对固定 commit `game/modules/tome/data/talents/spells/storm.lua`，4 个技能名称「Nova -> 闪电新星」、「Shock -> 闪电之击」、「Hurricane -> 飓风」、「Tempest -> 无尽风暴」与技能定义严格一致；「daze」对应「眩晕」符合术语规范。

#### entry-02569
- **位置**：`mod-tome.lua:34329`
- **Section**：`mod-tome/data/texts/unlock-mage_thaumaturgist.lua`
- **复核结论**：未发现问题
- **依据**：职业进阶「高阶奇术师（High Thaumaturgist）」与基底职业「元素法师（Archmage）」翻译规范，颜色标签正确。

#### entry-02570
- **位置**：`mod-tome.lua:34330`
- **Section**：`mod-tome/data/texts/unlock-mage_thaumaturgist.lua`
- **复核结论**：细微观察
- **依据**：
  1. 原文描述：“A 3-wide beam of pure thaumic energy that can never be resisted.”
  2. 译文：“这一宽度为3的纯粹奇术能量永远无法被抵抗。”
  3. 译文漏译了核心名词「射线 / 光束（beam）」，丢失量词与中心词。
  4. 首句「杀死了一个boss」保留了英文全小写「boss」未作本地化处理。
  5. 技能名称核验：5 个基础法术「Flame（火球术）」、「Manathrust（奥术射线）」、「Lightning（闪电术）」、「Pulverizing Auger（粉碎钻击）」、「Ice Shards（寒冰箭）」以及 4 个奇术技能「Orb of Thaumaturgy（奇术之球）」、「Multicaster（多重施法）」、「Slipstream（能量滑流）」、「Elemental Array Burst（元素阵爆发）」均与对应文件及术语完全对齐；「prodigies」译为「觉醒技」准确无误。

#### entry-02571
- **位置**：`mod-tome.lua:34363`
- **Section**：`mod-tome/data/texts/unlock-paladin_avatar.lua`
- **复核结论**：未发现问题
- **依据**：职业进阶「Avatar of a Distant Sun」译为「日耀神使」（与游戏内该觉醒技天赋名称一致），职业「Sun Paladin」译为「太阳骑士」，颜色标记一致。

---

### 复核结果汇总

| 条目编号 | 复核结论 | 核心依据 / 备注 |
| :--- | :--- | :--- |
| `entry-02538` | 细微观察 | 增补「测试一下……作用」且略缩「每种效果鼠标提示」为「注意查看鼠标提示」 |
| `entry-02539` | 未发现问题 | 7 点解锁点与 `unused_talents_types = 7` 源码事实一致，格式标签完整 |
| `entry-02540` | 未发现问题 | 被诅咒者（痛苦系）规范准确，颜色标签一致 |
| `entry-02541` | 细微观察 | `"lifted"` 引号双关意译为「战胜了」且略去引号；光环、仇恨值术语准确 |
| `entry-02542` | 未发现问题 | 末日使者（痛苦系）规范准确，颜色标签一致 |
| `entry-02543` | 未发现问题 | 转化之盒译名与颜色标签准确 |
| `entry-02544` | 未发现问题 | 竞技场：擂主的挑战战役名准确 |
| `entry-02545` | 细微观察 | 第 2 句无主语偏正断裂；「这里有一个……资本哦！」偏口语化 |
| `entry-02546` | 未发现问题 | 无尽地下城：永无止境的下降战役名准确 |
| `entry-02547` | 未发现问题 | 混沌纪、弑神者、瑞尔克专名及机制表述准确 |
| `entry-02548` | 未发现问题 | 时空法师（时空系）规范准确，颜色标签一致 |
| `entry-02549` | 未发现问题 | 时空守卫（时空系）规范准确，颜色标签一致 |
| `entry-02550` | 未发现问题 | 时空经纬表述典雅，双持机制与紊乱值资源准确 |
| `entry-02551` | 未发现问题 | 腐化者（堕落系）规范准确，颜色标签一致 |
| `entry-02552` | **存在疑点** | 「达到目的法师」漏定语助词「的」，应为「达到目的的法师」 |
| `entry-02553` | 未发现问题 | 收割者（堕落系）规范准确，颜色标签一致 |
| `entry-02554` | 未发现问题 | 杀害人形生物解锁条件与白骨之力机制准确 |
| `entry-02555` | 细微观察 | 排版多处多余空格；「玩的愉快」错字；难度模式译名与设定一致 |
| `entry-02556` | 未发现问题 | 星月术士（天空系）规范准确，颜色标签一致 |
| `entry-02557` | 细微观察 | 「学会了如何同时掌控光与影的能量方法」句式杂糅；能量机制准确 |
| `entry-02558` | 未发现问题 | 太阳骑士（天空系）规范准确，颜色标签一致 |
| `entry-02559` | 细微观察 | 第 3 段末尾增译「施展他们的特殊能力」；专名准确 |
| `entry-02560` | 未发现问题 | 元素法师规范准确，颜色代码一致 |
| `entry-02561` | 未发现问题 | 魔法狩猎、马基·埃亚尔、安格利文专名均符合规范 |
| `entry-02562` | 未发现问题 | 冰系技能树与颜色标签一致 |
| `entry-02563` | 未发现问题 | 石系技能树与颜色标签一致 |
| `entry-02564` | 未发现问题 | 死灵法师与颜色标签一致 |
| `entry-02565` | 细微观察 | 「所谓的”高贵”」前引号误用为右闭双引号；段落词语重复残留 |
| `entry-02566` | 未发现问题 | 焱系技能树与颜色标签一致 |
| `entry-02567` | 未发现问题 | 风暴系技能树与颜色标签一致 |
| `entry-02568` | 细微观察 | 标签内空格与冒号排版瑕疵，标点未统一；4 个技能名与源码一致 |
| `entry-02569` | 未发现问题 | 高阶奇术师（元素法师）规范准确 |
| `entry-02570` | 细微观察 | 「Elemental Array Burst」漏译名词「射线」；保留英文小写「boss」 |
| `entry-02571` | 未发现问题 | 日耀神使（太阳骑士）与游戏内天赋名规范一致 |

本复核为只读检查，未对仓库进行任何写操作，未派发子代理，报告交付完毕。