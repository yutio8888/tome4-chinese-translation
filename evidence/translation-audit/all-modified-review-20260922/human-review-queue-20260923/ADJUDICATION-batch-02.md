# 批阅裁决台账 — batch-02

- 任务：`human-review-adjudication-20260923`
- 冻结包 SHA-256：`c3e6b1c47f9c8a3dd82eca059b3639f22fed78aacdcf20647f0479adda76f53a`
- 决策行：40；冻结修订（含孪生载体）：41
- 机械核验：通过（无越权、无不变量破坏、无绑定错误）

## ORCHESTRATOR 裁决分布

| verdict | 条数 |
| --- | --- |
| accepted | 37 |
| deferred | 4 |

## 被驳回／未采纳的模型主张

| entry | 模型主张 | 裁决 | 理由 |
| --- | --- | --- | --- |
| entry-00244 | 去掉 ` area effect` 的前导空格造成中文拼接缺陷 | rejected | 模型主张补回空格。固定源码 MapEffects.lua:23 为 `dam_def.name .. _t" area effect"` 直接拼接，补空格会显示「火焰 范围效果」，反证模型建议有害。 |
| entry-00221 | 「离开地图」构成明显误译 | rejected | 模型自标 advisory。源码 Game.lua:926-936 的 can_change_level 阻止任何换层/换区域，「离开地图」覆盖该限制，功能含义正确；level/zone 统一译法属跨条目策略，非本条缺陷。 |
| entry-00345 | 「使这次攻击发生偏斜」弱化招架，应改「招架」 | rejected | 模型自标 advisory。源码确认招架成功挡住攻击，现译保留防御成功含义，属文风偏好，不构成缺陷。 |
| entry-00185 | 方括号内多空格 | rejected | 模型自标 advisory。用户策略明确纯静态排版不算缺陷；方括号不属「括号不一致」策略范围。 |
| entry-00254 | 「最大 50%」与同组「最大40%」排版不一致 | rejected | 模型自标 advisory；仅为数字前空格差异，属纯静态排版，按用户策略不整理。 |
| entry-00419 | 「超过1500点」与同组「超过 600 点」空格不一致 | rejected | 模型自标 advisory；纯静态排版差异，按用户策略不整理。 |
| entry-00428 | 三扇传送门句式与同系列不平行 | rejected | 模型自标 advisory；条件、数量、机制均正确，句式平行属文风偏好。 |
| entry-00334 | 「杀死」应为「击杀」 | rejected | 模型自标 advisory；日志在敌人 on_die 中输出，「杀死」与触发事实一致，击杀仅为界面习惯差异。 |
| entry-00434 | 「珠宝匠托付」应改为更贴近源码关系 | rejected | 模型自标 advisory；Master Jeweler 对应珠宝匠，译文为可接受意译，任务名已增补，无缺陷。 |
| entry-00393 | 复合后缀外层半角括号 | rejected_on_entry | 本条 entry-00393 本身已是全角；模型所指的半角外层括号实际出现在 entry-00395–00400（同一 hrq-00046 行的其他载体），已按 bracket_fullwidth 修复那些载体。 |
| entry-00184 | 「勇敢的向前」语病、段间缺空行 | accepted_upstream | 缺陷成立，但主工作区 HEAD 11b3e963 已修（已核逐字）。按 SPEC 规则不在本 worktree 重复修改，记 defer；不接受在本分支重复改。 |

## 逐条裁决

| queue_id | entry_id | 文件:行 | 模型意见 | ORCHESTRATOR 裁决 | 是否落实 | 理由 |
| --- | --- | --- | --- | --- | --- | --- |
| hrq-00052 | entry-00443 | mod-tome.lua:2864 | fix | accepted | 是 | cold 术语 existing，但游戏内 damage type 显示名（mod-tome.lua:6855 寒冷）与术语库一致；同节姊妹成就用「火焰伤害」。成就引用伤害类型须与其显示名一致，独立核验通过。 |
| hrq-00053 | entry-00448 | mod-tome.lua:2886 | fix | accepted | 是 | 原译「一切为了随机」把 most of all RANDOM（最主要特点是随机）改成目的状语，且 by no means 被弱化为「显然」。重译保留全部格式码与「随机」强调。 |
| hrq-00054 | entry-00455 | mod-tome.lua:2932 | fix | accepted | 是 | against our strength none shall pass 的主语是「无人」；原译「任何反抗我们的力量都休想通过」把力量变成主语，语义偏移。 |
| hrq-00055 | entry-00458 | mod-tome.lua:2943 | fix | accepted | 是 | 本句为星月术士（光暗平衡）座右铭；同节 twilight places=暮光之境、glyph of twilight=暮光圣印。twilight→暮光 与同节一致；refuted 主张（twilight 绝不能指黎明）不采纳，模型 refuted 判断本身成立。 |
| hrq-00056 | entry-00476 | mod-tome.lua:3046 | fix | accepted | 是 | locked_desc 谜语；the way 有两条解锁路径（wayist 对话与 Dogroth Caldera 成就），不能坐实为「维网」。原译「通往你精神世界的钥匙」失当，重译保留 find the way 的重复。 |
| hrq-00057 | entry-00486 | mod-tome.lua:3128 | no_change | accepted | 否 | 后半括号缺「时」导致结构不对称，属标点/结构修正；using 译「装备」的 refuted 主张不采纳（原文本即 when using）。 |
| hrq-00058 | entry-00489 | mod-tome.lua:3136 | fix | accepted | 是 | for the sheer destruction they can bring 是擅长的原因；原译删去因果并引入原文没有的最高级「最大的伤害」。 |
| hrq-00059 | entry-00492 | mod-tome.lua:3145 | defer | deferred | 否 | 缺陷成立（漏 pit-fighter；amateur practitioner 误作「门外汉」；the Brawler's skills 未体现职业名）。但主工作区 HEAD 8e06944f 该条已修（已逐字核对）。按 SPEC 规则 8 defer，不在本 worktree 重复修改；本 worktree 曾试改后已还原。 |
| hrq-00060 | entry-00500 | mod-tome.lua:3192 | no_change | accepted | 否 | eldritch 在 creatures.tsv 为骇异（preferred），但本条是 Stone Wardens 职业描述的「奥术技艺」，与同职业技能 Eldritch Stone→奥术岩盾（preferred）一致；不机械套用实体子类型条目。原译「奥术技艺」正确，不改。 |
| hrq-00061 | entry-00501 | mod-tome.lua:3250 | no_change | accepted | 否 | 机制说明准确，人称/标点属 advisory，不改。 |
| hrq-00062 | entry-00522 | mod-tome.lua:3705 | no_change | accepted | 否 | 术语库 Ghoulish Leap=定向跳跃 为 existing（记录现状，非背书），而游戏内技能名已是「食尸鬼跳跃」（mod-tome.lua:31850 talent name）。本条种族介绍与实际技能名一致；应校准的是术语库陈旧记录，不是译文。独立核验通过。 |
| hrq-00063 | entry-00527 | mod-tome.lua:3748 | fix | accepted | 是 | undead abilities 所列（毒素免疫、无需呼吸等）是生理特性而非可施放技能；同节食尸鬼对应句（mod-tome.lua:3700）已用「不死系能力」。改「能力」与同节统一。 |
| hrq-00064 | entry-00553 | mod-tome.lua:4090 | fix | accepted | 是 | a SMOKING CRATER AND ONE TRULY IRATE HALFLING 是两个并列对象，原译并成「冒着黑烟的半身人」；THE LONGER YOU WAIT 指越晚回来风险越大，原译误为当下停留。 |
| hrq-00065 | entry-00560 | mod-tome.lua:4118 | fix | accepted | 是 | eyelids 泛化为「脸上」丢失刻意的具体部位；perhaps the last 被改成「传说中唯一」，把不确定改确定、把「最后仅存」改「唯一」。物品标准名 entity name 为「堕落印记：清除」（mod-tome.lua:9510），一并对齐。 |
| hrq-00066 | entry-00570 | mod-tome.lua:4681 | fix | accepted | 是 | 开引号误用右双引号「”」，属标点错误。 |
| hrq-00067 | entry-00574 | mod-tome.lua:5070 | fix | accepted | 是 | 「创造一个远行传送门达到马基·埃亚尔」动补搭配不成立且漏 new；改为「建造一座通往马基·埃亚尔的新远行传送门」。 |
| hrq-00068 | entry-00579 | mod-tome.lua:5136 | no_change | accepted | 否 | Sorcerers 无术语条目，固定简中语料不统一（成就用「巫师」、任务用「法师」、sorcerer-end 用「魔法师」）。统一译名属未授权跨条目术语决定；与失败分支 00581 首句逐字一致，两条同不改以保持联动。 |
| hrq-00069 | entry-00581 | mod-tome.lua:5140 | no_change | accepted | 否 | 与 00579 同一指称的失败分支，首句逐字相同；两条同为 no_change 以保持联动。 |
| hrq-00070 | entry-00604 | mod-tome.lua:5978 | fix | accepted | 是 | 原文 Can you try…please? 为礼貌请求疑问句；原译「请试着…？」祈使句配问号。与 00605 成对修改。 |
| hrq-00070 | entry-00605 | mod-tome.lua:5979 | fix | accepted | 是 | 性别变体孪生行，与 00604 成对修改，仅「男/女」不同，措辞风格一致。 |
| hrq-00071 | entry-00615 | mod-tome.lua:6287 | no_change | accepted | 否 | 相邻两句重复「研究」属文风冗余，advisory，不改。 |
| hrq-00072 | entry-00620 | mod-tome.lua:6417 | fix | accepted | 是 | 「勇敢的」应为状语「勇敢地」；「玩的开心」应为「玩得开心」。已核主工作区未修此条，故不 defer，直接修。 |
| hrq-00073 | entry-00621 | mod-tome.lua:6472 | fix | accepted | 是 | death trap 为固定说法强调致命；原译「陷阱」丢失核心信息。 |
| hrq-00074 | entry-00623 | mod-tome.lua:6557 | fix | accepted | 是 | 原译逗号切断地点定语（读作「使用了地下深处」）且缺主语；refuted 主张（「保护」把兽人写成友军）不成立，不按善意改，只修结构。 |
| hrq-00075 | entry-00634 | mod-tome.lua:6817 | defer | deferred | 否 | stabbed 属 PHYSICAL death_message 表（damage_types.lua:778）。该表已由用户于 2026-09-16 裁定「暂不处理，继续保持 pending」。独立核验：该裁定在 production-review-v2-lite 与 quality 证据中多处记载。按归属处置，不改。 |
| hrq-00076 | entry-00644 | mod-tome.lua:6957 | no_change | accepted | 否 | 「恐惧」压缩 frightening sight，但不变机制且属可接受意译，advisory，不改。 |
| hrq-00077 | entry-00646 | mod-tome.lua:6986 | defer | deferred | 否 | tdesc 为 arcane resource burn（damage_types.lua:2267-2281），「奥术」有源码依据，模型「增译」主张不成立。但术语库 manaburn arcane=法力燃烧（existing/global）与现译不一致；登记新译或回退属术语决定，未授权。与 00653 一并 defer，现两条内部一致。 |
| hrq-00078 | entry-00647 | mod-tome.lua:7017 | no_change | accepted | 否 | 原文 exploded 指护盾被移除而非范围爆炸；「终于破碎了」可接受，advisory，不改。 |
| hrq-00079 | entry-00650 | mod-tome.lua:7048 | fix | accepted | 是 | 术语 draining physical=生命汲取 为 preferred（combat.tsv:156），必须采用；源码 DEVOUR_LIFE 造成物理伤害并按伤害治疗施法者。 |
| hrq-00080 | entry-00652 | mod-tome.lua:7054 | fix | accepted | 是 | 原译「法力蠕虫奥术」把属性后置读作「法力蠕虫的奥术」；源码 MANAWORM 先造成奥术伤害再施加效果，同节惯例为「属性+名称」（arcane silence→奥术沉默）。改「奥术法力蠕虫」。注：若 manaburn 系列按术语库回退，本条需同步，见待决项。 |
| hrq-00081 | entry-00653 | mod-tome.lua:7071 | defer | deferred | 否 | 模型 refuted 主张成立：原文即 manaburn arcane，「奥术」非增译。但术语库条目（existing）与现译不一致，属未授权术语决定。与 00646 一并 defer。 |
| hrq-00082 | entry-00657 | mod-tome.lua:7159 | fix | accepted | 是 | 该串是地格名 g.name（fareast.lua:57），实为 dungeon entrance 地格；同节 Entrance to a underwater cave→水下洞窟入口 同构。改「阴影地宫入口」。 |
| hrq-00083 | entry-00660 | mod-tome.lua:7191 | fix | accepted | 是 | muffled 漏译，「陌生」无依据增译；重译补「隐约」「沉闷」并去增译。 |
| hrq-00084 | entry-00683 | mod-tome.lua:7393 | fix | accepted | 是 | 源码 rat-lich.lua:73 参数依次为使用者、his_her、物品名；raises 是举起头骨，原译「令…站了起来」误译；eye sockets 与物品描述「眼窝」（mod-tome.lua:7390）一致。 |
| hrq-00085 | entry-00684 | mod-tome.lua:7394 | fix | accepted | 是 | dust of decay 为腐朽的尘埃；该召唤为 necroSetupSummon（rat-lich.lua:92-93）非火焰，原译「灰烬」带入燃烧意象。 |
| hrq-00086 | entry-00712 | mod-tome.lua:7985 | fix | accepted | 是 | impenetrable 意为难以穿透/坚不可摧，「结实」明显弱化。 |
| hrq-00087 | entry-00713 | mod-tome.lua:8009 | fix | accepted | 是 | 'Cause this bear wants honey 是因果句；原译「喜欢蜂蜜哦～。」删因果、把 wants 改 likes，且「～。」标点累赘。不补写原文没有的「吃掉你」。 |
| hrq-00088 | entry-00719 | mod-tome.lua:8096 | no_change | accepted | 否 | npcs/crystal.lua 定义的是会行动施法的 NPC（type=immovable, ai=dumb_talented_simple），称「生物」符合实体性质；同节七个彩色晶体描述一致用「由X色水晶构成的生物」，单改会制造族内不一致。不改。 |
| hrq-00089 | entry-00722 | mod-tome.lua:8183 | fix | accepted | 是 | 首句主语是实体（dreadmaster，ghost.lua:83）而非抽象力量；unearthly limbs, of purest black 修饰关系错置；wither flesh 译「血肉成灰」偏离。 |
| hrq-00090 | entry-00723 | mod-tome.lua:8187 | fix | accepted | 是 | withering and searing 是枯萎与灼烧，原译「腐蚀」偏离，且连用三次「不断」。 |
| hrq-00091 | entry-00728 | mod-tome.lua:8258 | fix | accepted | 是 | carrion worm mass=腐肉虫群（creatures.tsv:42，备注「统一实体名、生成日志及疾病描述」）；实体名（mod-tome.lua:8982）与疾病生成日志（35324）均已用「腐肉虫群」。 |

## 待用户决定（未授权范围）

- `entry-00216` / `hrq-00025`：`Defiler` 人物称谓名词化。术语库 `Defiler=堕落系`（existing，类别名），`Corruptor=腐化者`。现译「迷路的腐化者」把上位概念收窄为子职业；但「堕落系」如何名词化无 preferred 条目。
- `entry-00112` / `entry-00146`（`hrq-00015`）：`Writhing One` 现译「扭动者」，术语库为「蜿蜒怪人」（existing）；`Nethergate` 现译「彼世之门」未登记。均为未授权术语决定。
- `entry-00288`：串尾去掉「。」后显示为西文句点，因为源码追加的 `_t"."` 未汉化；该条目不在本批冻结集合。
- `entry-00344`：女性角色时为「用她盾牌」，因 `_t"her"` 与 `him_her` 共用，需在 engine 词条另作决定。
- 跨条目策略：`level`／`zone` 是否统一为「层／地图」（影响 00221/00223 等）。
