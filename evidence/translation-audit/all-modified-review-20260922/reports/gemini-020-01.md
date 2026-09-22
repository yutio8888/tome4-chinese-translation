本批次复核针对 **batch-020**（条目范围：`entry-00761` 至 `entry-00800`，共 40 条）。

### 批次与环境核验
- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-020.md`
- **文件 SHA-256 核验结果**：`7ff91a09b9333bebed00b267732d30a8601b29abd9158d9bc463a6163b73ebe9`（与冻结哈希完全一致）
- **源码依据**：公开源码仓库 `t-engine4` 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取对应 `game/modules/tome/` 路径）
- **译文语境**：工作树当前版本 `mod-tome.lua`（无未提交改动，对齐译文终点 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`）

---

### 逐条复核报告

#### entry-00761
- **位置/条目**：`mod-tome.lua:8704` / `entry-00761`（`mod-tome/data/general/npcs/shade.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `Through some terrible process that remains mysterious, this creature's shadow has been torn from its body and given unlife.` 对应译文 `通过某种神秘的可怕手段，这只生物的影子被从身体上剥离出来，并被赋予了亡灵般的存在。`。对暗影生物被剥离本体、赋予亡灵生命的描述准确通顺，无格式与占位符问题。

#### entry-00762
- **位置/条目**：`mod-tome.lua:8715` / `entry-00762`（`mod-tome/data/general/npcs/shivgoroth.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `BASE_NPC_SHIVGOROTH` 的 `type = "elemental"`，source_tag 为 `entity type`。译文 `元素生物` 完全符合术语表中 `elemental -> 元素生物 (creatures entity type preferred)` 的规范。

#### entry-00763
- **位置/条目**：`mod-tome.lua:8718` / `entry-00763`（`mod-tome/data/general/npcs/shivgoroth.lua`）
- **结论**：存在疑点
- **核验依据**：原文 `Shivgoroth are mighty ice elementals, torn away from their home world by a powerful magic.` 译文为 `西弗格罗斯是强大的寒冰元素，它们被一股强大的魔法从老家里赶出来。`。
  1. `torn away from` 表示“被强行剥离/撕裂带离（原本的世界）”，译成“赶出来”在语义机制上发生偏差（从异界被法术强行撕扯/传送走变成了被逐出家门）；
  2. `home world` 指其“故乡世界/原生位面/原生世界”，译为口语化且语域不符的“老家”，在奇幻背景设定叙事中过于突兀且失真。

#### entry-00764
- **位置/条目**：`mod-tome.lua:8727` / `entry-00764`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `degenerated skeleton warrior` 译为 `退化骷髅战士`，符合 `Skeleton -> 骷髅` 与 `warrior -> 战士` 术语，命名准确。

#### entry-00765
- **位置/条目**：`mod-tome.lua:8728` / `entry-00765`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `A haphazard collection of crumbling bones, with jerky movements that remind you of a child playing with a marionette. It only has one arm, but that's all it needs to hold a sword.` 译文 `一堆杂乱拼凑、摇摇欲坠的骨骸，动作僵硬抽搐，令你想起孩童手中玩弄的木偶。它只有一条手臂，但握住一把剑也就够了。`，表意生动准确，标点完整。

#### entry-00766
- **位置/条目**：`mod-tome.lua:8729` / `entry-00766`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `degenerated skeleton archer` 译为 `退化骷髅弓箭手`，符合 `Archer -> 弓箭手` 术语，准确无误。

#### entry-00767
- **位置/条目**：`mod-tome.lua:8730` / `entry-00767`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：原文描述骷髅手腕刻有凹槽以拉动弓弦（`...a notch has been carved into its wrist to let it pull back a bowstring regardless.`），译文 `一具脆弱的骨架；几乎只有双臂的骨头没有开裂。它缺少了一只手，不过手腕上刻了一道凹槽，刚好可以卡住弓弦拉弓上箭。` 达意流畅。

#### entry-00768
- **位置/条目**：`mod-tome.lua:8734` / `entry-00768`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：细微观察
- **核验依据**：原文后半句 `It's still wearing its old armor, in rusty but servicable condition.` 译为 `它仍然穿着它原来的那件老盔甲，锈迹斑斑却值得信赖。`。`servicable`（可用的、尚堪使用、能发挥机能）被意译为“值得信赖”（trustworthy/reliable），虽不影响整体理解，但存在一定程度的情感色彩增添与语义漂移。

#### entry-00769
- **位置/条目**：`mod-tome.lua:8738` / `entry-00769`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `This skeleton has been imbued with far more magical energy than normal, and serves as a conduit of its master's spellcasting prowess.` 译为 `这只骷髅的身上充盈着远超常规的魔法力量，充当其主人施法威能的导管。`，用词贴切，忠实于原文。

#### entry-00770
- **位置/条目**：`mod-tome.lua:8740` / `entry-00770`（`mod-tome/data/general/npcs/skeleton.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `It feels no pain. It moves with fluidity and strength that would tear natural muscles apart. It must be from a fresh corpse, since its bones, armor, and weapon are all in pristine condition. And it's furious.` 译文 `它感觉不到疼痛。它的动作流畅而有力，足以撕裂天然的肌肉。它一定来自一具新鲜的尸体，因为它的骨头、装甲和武器都完好如新。而且，它怒不可遏。`，短句节奏与语气皆还原到位。

#### entry-00771
- **位置/条目**：`mod-tome.lua:8792` / `entry-00771`（`mod-tome/data/general/npcs/spider.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `These cunning spiders terrorize those who enter the ever-growing borders of their lairs. Those who encounter them rarely return.` 译为 `这些狡猾的蜘蛛威胁着踏入其巢穴那不断扩张的边界的生物。遭遇它们的人鲜有生还。`，语义通顺，语法完整。

#### entry-00772
- **位置/条目**：`mod-tome.lua:8796` / `entry-00772`（`mod-tome/data/general/npcs/spider.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `This spider seems to command the flow of mana, which pulses freely through its body.` 译为 `这只蜘蛛似乎能掌控法力的流动，法力在它体内自由涌动。`，术语 `mana -> 法力` 在叙事语境中恰当自然。

#### entry-00773
- **位置/条目**：`mod-tome.lua:8802` / `entry-00773`（`mod-tome/data/general/npcs/spider.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `A tiny arachnid that phases in and out of reality.` 译为 `一只小小的蜘蛛，它不断地在现实中时隐时现。`，准确反映时空编织者幼体（weaver young）在现实内外穿梭的机制与叙事。

#### entry-00774
- **位置/条目**：`mod-tome.lua:8834` / `entry-00774`（`mod-tome/data/general/npcs/sunwall-town.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `elven sun-mage` 的描述 `An elf dressed in glowing robes.` 译为 `一位穿着荧光长袍的精灵。`，短句精准。

#### entry-00775
- **位置/条目**：`mod-tome.lua:8855` / `entry-00775`（`mod-tome/data/general/npcs/telugoroth.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `doTeluvortaSwap` 中换位失败时的日志调用 `game.logSeen(self, "The spell fizzles!")`，译文 `法术失败了！` 符合战斗日志规范。

#### entry-00776
- **位置/条目**：`mod-tome.lua:8857` / `entry-00776`（`mod-tome/data/general/npcs/telugoroth.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `BASE_NPC_TELUGOROTH` 的 `type = "elemental"`，source_tag 为 `entity type`。译文 `元素生物` 符合统一术语。

#### entry-00777
- **位置/条目**：`mod-tome.lua:8887` / `entry-00777`（`mod-tome/data/general/npcs/thieve.lua`）
- **结论**：未发现问题
- **核验依据**：影刃描述 `Stealthy fighters trying to achieve victory with trickery. Be careful or they will steal your life!` 译为 `善用诡计取胜的潜行斗士。小心，他们会偷走你的生命！`，准确传达警告意图与叙事风格。

#### entry-00778
- **位置/条目**：`mod-tome.lua:8897` / `entry-00778`（`mod-tome/data/general/npcs/troll.lua`）
- **结论**：未发现问题
- **核验依据**：森林巨魔描述 `Green-skinned and ugly, this massive humanoid glares at you, clenching wart-covered green fists.` 译为 `这只绿皮丑陋的庞大人形生物正盯着你，同时它握紧了满是疣的绿色拳头。`，`humanoid` 译为 `人形生物`，词义精准。

#### entry-00779
- **位置/条目**：`mod-tome.lua:8903` / `entry-00779`（`mod-tome/data/general/npcs/troll.lua`）
- **结论**：未发现问题
- **核验依据**：山地巨魔描述 `A large and athletic troll with an extremely tough and warty hide.` 译为 `一只高大且强壮的巨魔，皮肤异常坚韧且长满疣。`，符合 `troll -> 巨魔` 术语。

#### entry-00780
- **位置/条目**：`mod-tome.lua:8953` / `entry-00780`（`mod-tome/data/general/npcs/vampire.lua`）
- **结论**：细微观察
- **核验依据**：吸血鬼描述 `It is a humanoid with an aura of power. You notice a sharp set of front teeth.` 译为 `这是一个散发着力量气场的类人生物，你注意到它长着一副锋利的门牙。`。术语快照中 `humanoid` 作为实体类型统一为“人形生物”；此处在自由描述文本（_t）中译为同义词“类人生物”，虽表意清晰且语境自然，但同 batch 内 `entry-00778` 译为“人形生物”，存在用词微小差异。

#### entry-00781
- **位置/条目**：`mod-tome.lua:8969` / `entry-00781`（`mod-tome/data/general/npcs/venom-drake.lua`）
- **结论**：细微观察
- **核验依据**：毒龙幼仔描述 `A corrosive venom drake hatchling; not too powerful by itself, but it usually comes with its brothers and sisters.` 译为 `一只腐蚀性的毒龙幼仔。它本身并不强大，但是它们经常集体行动。`。源码中该 NPC 确实固定伴随 3 只幼仔生成（`make_escort = {{name="venom drake hatchling", number=3}}`），机制上确实是群体出现；但译文将 `brothers and sisters`（同窝孵化的兄弟姐妹）抽象概括为“集体行动”，且主语后半句由单数“它”变为复数“它们”，略失原文拟人化的生物学色彩。

#### entry-00782
- **位置/条目**：`mod-tome.lua:9006` / `entry-00782`（`mod-tome/data/general/npcs/wild-drake.lua`）
- **结论**：未发现问题
- **核验依据**：尖塔巨龙描述 `A monstrous, coiled wyrm, patient and hateful. Its hide, studded with spikes and crests and blades, turns aside steel and sorcery with equal ease.` 译为 `一条骇人的盘曲巨龙，耐心而怀恨。它的表皮上布满棘刺、脊冠与利刃，无论钢铁还是法术都被它同样轻易地卸开。`。`steel` 与 `sorcery`（钢铁与法术）翻译精准，结构严整。

#### entry-00783
- **位置/条目**：`mod-tome.lua:9008` / `entry-00783`（`mod-tome/data/general/npcs/wild-drake.lua`）
- **结论**：未发现问题
- **核验依据**：相位巨龙描述 `A shifting, writhing, snake-like dragon, blinking in and out of existence, just waiting for you to turn your back.` 译为 `一只不断扭动变幻、忽隐忽现的蛇状巨龙，只等你一转身露出破绽。`。末句将 `turn your back`（背对着它）引申意译为“转身露出破绽”，符合怪物偷袭/背刺语境，通顺传神。

#### entry-00784
- **位置/条目**：`mod-tome.lua:9013` / `entry-00784`（`mod-tome/data/general/npcs/xorn.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `BASE_NPC_XORN` 中 `type = "elemental"`，source_tag 为 `entity type`。译文 `元素生物` 符合术语规范。

#### entry-00785
- **位置/条目**：`mod-tome.lua:9036` / `entry-00785`（`mod-tome/data/general/npcs/yaech.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `Yaeches are an aquatic subspecies of yeeks. They share the same psionic powers, but they refuse to take part in the Way.` 译为 `夺魂魔是夺心魔的一支水栖亚种。他们拥有同样的灵能，但夺魂魔拒绝加入维网。`。`Yeek -> 夺心魔`、`psionic -> 灵能`、`The Way -> 维网`，术语完全一致，准确可靠。

#### entry-00786
- **位置/条目**：`mod-tome.lua:9068` / `entry-00786`（`mod-tome/data/general/objects/2haxes.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `name = "stralite battleaxe"` 译为 `斯莱特双手斧`，遵循统一术语 `stralite -> 斯莱特`（四级金属材质），且双手斧分类明确。

#### entry-00787
- **位置/条目**：`mod-tome.lua:9069` / `entry-00787`（`mod-tome/data/general/objects/2haxes.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `short_name = "stralite"` 译为 `斯莱特`，材质短名完全对齐术语。

#### entry-00788
- **位置/条目**：`mod-tome.lua:9086` / `entry-00788`（`mod-tome/data/general/objects/2hmaces.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `name = "stralite greatmaul"` 译为 `斯莱特巨锤`，符合材质规范与巨锤大类命名。

#### entry-00789
- **位置/条目**：`mod-tome.lua:9087` / `entry-00789`（`mod-tome/data/general/objects/2hmaces.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `short_name = "stralite"` 译为 `斯莱特`，材质短名对齐。

#### entry-00790
- **位置/条目**：`mod-tome.lua:9104` / `entry-00790`（`mod-tome/data/general/objects/2hswords.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `name = "stralite greatsword"` 译为 `斯莱特大剑`，符合双手剑/大剑分类与材质规范。

#### entry-00791
- **位置/条目**：`mod-tome.lua:9105` / `entry-00791`（`mod-tome/data/general/objects/2hswords.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `short_name = "stralite"` 译为 `斯莱特`，材质短名对齐。

#### entry-00792
- **位置/条目**：`mod-tome.lua:9115` / `entry-00792`（`mod-tome/data/general/objects/2htridents.lua`）
- **结论**：未发现问题
- **核验依据**：原文：
  ```text
  A two-handed massive trident.
  Tridents require the exotic weapons mastery talent to use correctly.
  ```
  译文：
  ```text
  一个沉重的双手三叉戟。
  三叉戟需要特殊武器掌握技能才能正确使用。
  ```
  换行结构完全保留，技能名称 `exotic weapons mastery -> 特殊武器掌握` 准确无误。

#### entry-00793
- **位置/条目**：`mod-tome.lua:9141` / `entry-00793`（`mod-tome/data/general/objects/axes.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `name = "stralite waraxe"` 译为 `斯莱特战斧`，材质与单手战斧命名精准。

#### entry-00794
- **位置/条目**：`mod-tome.lua:9142` / `entry-00794`（`mod-tome/data/general/objects/axes.lua`）
- **结论**：未发现问题
- **核验依据**：源码 `short_name = "stralite"` 译为 `斯莱特`，材质短名对齐。

#### entry-00795
- **位置/条目**：`mod-tome.lua:9154` / `entry-00795`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：原文：
  ```text
  The power of the tides rush through this trident.
  Tridents require the exotic weapons mastery talent to use correctly.
  ```
  译文：
  ```text
  这把三叉戟上流动着潮汐的力量。
  三叉戟需要特殊武器掌握技能才能正确使用。
  ```
  换行结构一致，技能名称及神器特征表述准确。

#### entry-00796
- **位置/条目**：`mod-tome.lua:9158` / `entry-00796`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `A choker made of pure flame, casting forever shifting patterns around the neck of its wearer. Its fire seems to not harm the wearer.` 译为 `一个由火焰形成的护符，在佩戴者的颈部周围投射出不断变幻的光影。它的火焰似乎不会伤害到佩戴者。`。`choker` 作为护符部位译名通顺，叙事准确。

#### entry-00797
- **位置/条目**：`mod-tome.lua:9162` / `entry-00797`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：源码格鲁希纳克掉落神器戒指 `name = "Glory of the Pride"` 译为 `部落之荣耀`。在远东兽人剧情及同文件语境中，`The Pride` 统称为“兽人部落/部落”（如 Grushnak Pride 译为格鲁希纳克部落），译名一致贴合。

#### entry-00798
- **位置/条目**：`mod-tome.lua:9163` / `entry-00798`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `The most prized treasure of the Battlemaster of the Pride, Grushnak. This gold ring is inscribed in the now lost orc tongue.` 译为 `这是部落的战争领主格鲁希纳克最宝贵的财富。这枚金戒指上铭刻着失传的兽人语。`。头衔、人名及背景叙事均翻译精准。

#### entry-00799
- **位置/条目**：`mod-tome.lua:9172` / `entry-00799`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：源码神器大剑 `unided_name = _t"blood-etched greatsword"` 译为 `血蚀纹大剑`，结构精炼准确。

#### entry-00800
- **位置/条目**：`mod-tome.lua:9173` / `entry-00800`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **结论**：未发现问题
- **核验依据**：原文 `A blood-etched greatsword, it has seen many foes. From the inside.` 译为 `一把镌着血蚀纹路的大剑，它见过许多敌人——从体内。`。原文黑色幽默风格（剑刃刺入敌人体内“见过敌人”）通过破折号完整保留并准确呈现。

---

### 复核总结
- **核验总数**：40 条（`entry-00761` ～ `entry-00800`，逐条全覆盖）
- **未发现问题**：37 条
- **存在疑点**：1 条（`entry-00763`：`torn away from their home world` 被口语化错译为“从老家里赶出来”，存在机制与语域偏差）
- **细微观察**：2 条（`entry-00768`：`servicable` 偏向意译为“值得信赖”；`entry-00781`：`brothers and sisters` 概括意译为“集体行动”，且主语单复数发生转换；另注 `entry-00780` 中自由叙事使用“类人生物”与“人形生物”的同义互换）