# ToME4 汉化：技能名 "Flame" 译名讨论（只读，不得修改任何文件）

## 问题
维护者认为 Flame 当前译名「火焰」作为技能名过短、没有法术技能感。请判断是否需要改名；若改，推荐一个译名（可附 1-2 个备选），并说明理由。

## 源码事实（ToME 4 固定 commit 624a6732, game/modules/tome/data/talents/spells/fire.lua:21 起）
- 法师 Spell/Fire 技能树第 1 个技能；mana 12，冷却 3，射程 10，is_beam_spell。
- 描述原文：Conjures up a bolt of fire, setting the target ablaze and doing %0.2f fire damage over 3 turns. At level 5, it will create a beam of flames.
- 即：1-4 级为单体火焰箭（bolt），5 级起变为射线（beam）；大法师 Thaumaturgy 进阶可使其成为 3 格宽射线。伤害是 3 回合持续灼烧（FIREBURN）。不是球形/爆炸 AoE。

## 同树与相关技能现行译名（语料实测）
- Fire 树：Flame 火焰 / Flameshock 火焰冲击 / Fireflash 爆裂火球 / Inferno 地狱火
- 同类法师单体技能：Manathrust 奥术射线、Lightning 闪电术、Ice Shards 寒冰箭、Pulverizing Auger 粉碎钻击、Earthen Missiles 岩石飞弹、Chain Lightning 连锁闪电
- 其他火系：Blastwave 火焰新星、Wildfire 野火燎原、Burning Wake 无尽之焰、Cleansing Flames 净化之焰
- 已被占用：Flame Bolt（另一个技能）= 火焰箭；Flame Bolts（DLC）= 近战火球；Flame Jet 火焰喷射；Flame Fury 火焰之怒；Devouring Flame 火焰吞噬
- 以下候选在全部译文技能名中未被占用（实测）：火焰术、烈焰术、火焰弹、烈焰箭、炎爆术、火焰射线、灼焰术、焚焰术、燃焰术

## 现存不一致
- 术语库 terminology/talents.tsv:117 记 Flame → 火球术（status existing，不是 preferred，无背书力）。
- 运行时技能名（mod-tome.lua / mod-boot.lua / engine.lua）均为「火焰」。
- 大法师职业描述与宽射线解锁文本（mod-tome.lua:31623, 34351）用「火球术」指代它；Burning Wake 描述（29884）用「火焰」指代它。
- 注意「火球术」与 Fireflash「爆裂火球」同含「火球」，而 Flame 实际是 bolt/beam 而非 ball。

## 要求
1. 给出结论：保持「火焰」/ 改名。若改名给推荐译名 + 备选。
2. 理由需涵盖：与机制是否贴合（bolt→beam 演变）、与同树/同类技能命名风格一致性、与已有译名的冲突/混淆风险、玩家认知（中文 RPG 惯例）。
3. 你可以只读查看 /workspace/tome4-chinese-translation 与 /workspace/t-engine4 核验上述事实；如发现上述事实有误请指出。不要修改任何文件。
4. 回答用中文，控制在 400 字以内，最后一行格式：`VERDICT: KEEP` 或 `VERDICT: RENAME <推荐译名>`。
