# 固定神器名称与描述匹配检查（2026-11-08，只读）

范围：固定源码 624a67329fe2 与三个 DLC（来源未固定）中 `unique = true` 的物品，排除随机神器与 lore，共 510 件。
方法：LuaJIT 沙箱提取名称/未鉴定名/描述/主动效果名 → 自动核对（整名交叉引用、同名多译、专名）→ 两轮独立语义审核（codex gpt-6.1-sol 4 lane、DeepSeek v4.1 flash 4 lane）→ 主代理逐条 grep 核实。

## 自动检查
- 名称同英文多译：0；描述中引用其他神器全名而译名不一致：0。
- 库内其他条目引用神器名不一致：Lightning Catcher 物品名「雷电接收器」，效果说明（mod-tome.lua:36269）写「闪电捕捉器」。

## A. 已确认：描述/未鉴定名/专名与名称或通行译名对不上（建议修）
| 神器 | 问题 | 建议 |
|---|---|---|
| Lightning Catcher 雷电接收器 | 增益效果说明称「闪电捕捉器」 | 效果说明改「雷电接收器」 |
| Wintertide 霜华 | 描述 Conclave 译「议会」，库内 37 处为「孔克雷夫」 | 改「孔克雷夫」 |
| Rod of Annulment 废除之杖 | 未鉴定名「黑暗的法杖」、描述「这根法杖」；实为 rod（魔杖） | 法杖→魔杖 |
| Rod of Spydric Poison 蜘蛛之毒杖 | 未鉴定名「魔杖」，描述「这根法杖」 | 描述改魔杖 |
| Nature's Vengeance 自然的复仇 | mace 译「木质粗权杖」「权杖」；库内 mace＝狼牙棒 | 改「粗重的木质狼牙棒」等 |
| Eldoral Last Resort 艾德瑞尔的最后手段 | 未鉴定名/描述 sling 译「投石器」；库内为投石索 | 改投石索 |
| Glowing Core 光亮之核 | 描述「灼热恐魔」，实体名与喊话为「灼光恐魔」 | 改灼光恐魔 |
| Earthen Beads 大地串珠 | 描述 Wilders 译「荒野行者」（全库仅此一处），术语 Wilder＝野性系 | 改野性系 |
| Spinal Cage 脊笼 | 未鉴定名「一堆脊柱碎片」，同一短语在描述中为「一大团……脊柱物质」 | 未鉴定名对齐描述 |
| Sealed Scroll of Last Hope 等 | 「最后希望」，术语与 62 处为「最后的希望」；同类还有 Harno 传令官名与描述、法瑞安传说（mod-tome.lua:12368、39288、39289、39301） | 统一「最后的希望」 |
| Thalore-Wood Cuirass 精灵木胸甲 / Thaloren-Tree Longbow 精灵树长弓 | Thalore＝自然精灵；「精灵木」是 elven-wood 的材质名，造成混淆；长弓描述本身写自然精灵 | 自然精灵木胸甲 / 自然精灵树长弓（改名，见 B 规则） |
| Snow Giant Wraps 冰霜巨人护手 | 库内 snow giant 全部「雪巨人」 | 雪巨人护手（改名） |
| Hydra's Bite 三头龙之牙 | 库内 hydra 为三头蛇/多头蛇，描述无龙 | 三头蛇之牙（改名） |
| Warmaster Gnarg's Murderblade 战争之王格纳哥的饮血剑 | 同一 NPC「战争领主格纳哥」；「饮血剑」与 Blood-Edge 撞名 | 战争领主格纳哥的…（刀名见 B） |
| Antimagic Wyrm Bile Extract 龙胆药剂（反魔） | Wyrm Bile 神器与饮用日志为「巨龙胆汁」 | 对齐巨龙胆汁 |
| Umbraphage 安布瑞吉·暗影吞噬者 | 英文无人名，效果日志只称「暗影吞噬者」 | 去掉音译（改名） |
| Spellblaze Shard 魔爆碎片 | 全库 Spellblaze＝魔法大爆炸 | 魔法大爆炸碎片（改名） |

## B. 待裁决：名称含义取舍（纯名称，按规则交 Gemini 4 Argon）
Unsetting Sun 永恒光辉（丢「太阳」）、Dragonskull Helm 龙骨之盔（与 dragonbone＝龙骨撞，描述是头骨）、Mighty Girdle 巨人腰带、Oozing Heart 史莱姆之心、Great Caller 伟大的召唤师（物品被称作人）、Anmalice 扭曲之刃·圣灵之眼（「圣灵」与恶意描述相反）、Skeletal Claw 白骨之握、Plate of the Blackened Mind 堕落灵魂之甲、Ring of Growth 生命之戒、Wrap of Stone 石化风衣（cloak 译风衣、「石化」与柔韧描述相反）、Murderblade 刀名。

## C. 不成立 / advisory
- Tome of Uttercold 极寒之书：书教冰风暴，与「绝对零度」技能无关，不改。
- Skin of Many、Helm of Knowledge：中英一致，矛盾来自英文原文（robe/crown），advisory。
- Witch-Bane 巫师毁灭者：witch 指施法者，不判错。
- Merkul's Second Eye「steal」、Glory of the Pride 的「之/的」：低置信或无关，advisory。
- 5 件 lore 类 unique（日记、黑色碟片）只是 tag 不同，不算缺失。
