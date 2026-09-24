# 合并修复窗口 27：273–277 批共 28 条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement。基线 dba3309b82255a9ec5501204e32d01d75ccaee3b。用户已授权当前连续审核及本轮合并修复，要求本轮完成后安全暂停，不启动第278批。

唯一 EXECUTOR 仅可修改 `mod-tome.lua`、`tome-ashes-urhrok.lua` 中 WORKSET.json 的28个 target，以及 `evidence/quality/repair-window-27-20260924/` 下的修复证据。不得修改 source、source_tag、section、args_order、运行键、术语库、其他译文、规则工具或旧证据；不得 stage、commit、push、创建 agent 或修改 .ai/task。无关未跟踪文件保持不动。宿主负责 task 与审核记录、提交发布。

逐条对照 WORKSET 原文和 SOURCE-ANCHORS 源码，再按 SOURCE-CLAIMS 的已确认问题修复；同条若有显而易见的增删误译一并修正。主游戏源码固定 commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；Ashes DLC 文件 SHA 已按各批 workset 核验，源码仓库和 commit 未固定，绝不能把本机 checkout 当作固定版本。仅补查条目对应的有限公开源码和同族译名，不扫根目录或无关目录。沿用现有专名，禁止自行全局重命名或更改待用户裁决的 `Archlich`、`Armoured Leviathan`、`Corruption of the Doomed`。

保留 printf 占位符、`%%`、`#TAG#`、`#{italic}#` 等 markup 的数量、顺序及适用位置；保留 source_tag。LF/TAB 结构逐行核对，特别是三行墓志铭和 Demonic Blood 两级缩进，不能只看总数。用 LuaJIT 加载两文件，证明恰28个 target 变动且其他记录不变；执行 strict lint、适用的 claims/anchor 检查及 diff check。无需完整门禁，宿主在独立复审后统一运行17项。

审查：cycle-0 `REVIEW/full` 用 Codex GPT-6 Sol；确认问题合并给一次 EXECUTOR fix；收敛后 `FINAL_REVIEW/full` 用 Claude Opus 5.5。v2 FINAL 如有任何 ISSUE，先修复并完成 RE_REVIEW，再重新 FINAL。max_cycles=3。reviewer 只读冻结译文、术语和契约允许的有限源码，不读 SOURCE-CLAIMS 或其他 reviewer raw。

## 条目与已确认修复依据

- 0523b49940c925506089a6f005215f40a9ffc1069275dcc1e83d11c6e9ff35a1 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/quests/start-ashes.lua | 公开 DLC start-ashes.lua:23–28（本批文件 SHA 匹配，仓库/commit 未固定）：原文恢复意识时灼热土地构成的平台正在从主大陆分裂；现译写成醒后发现已分离，并漏掉 searing earth。只修这一时序与土地意象；Eyal 的全局译名另在既有 pending。
- 0c22616daeea5c4344db3cc9e6d855db76afe7dce0d4e4df28338b7e744b32a2 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/general/objects/world-artifacts.lua | 公开 DLC world-artifacts.lua:691（本批文件 SHA 匹配，commit 未固定）：treacherous road to the top of the world 指通往世界之巅的险途；“背叛之路，直通天际”改动道路性质和终点。修复为保留引号的险途/世界之巅表达。
与 surface 同向：公开 DLC world-artifacts.lua:691 的 treacherous road 是险途，且原文有引号；本批 SHA 匹配，来源和 commit 未固定；并入同条修复。
- 0ed56881299d6e08842efe672f4bb7a42238c9b86d9c4f6b0f3b268ecc4a13df | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/birth/corrupted.lua | 公开 DLC corrupted.lua:114（本批文件 SHA 匹配，commit 未固定）：Most simply run 是多数人逃跑，现译“人们常畏惧”改变行动；destruction's engines 是毁灭的工具/引擎，现译添“战争机器”。修复该两处并保持原文的抒情节奏。
- 10419e2ec39499a69cf40dcc495d2c80d426c0390f5413e98031f4e6693a26cf | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/timed_effects.lua | 公开 Ashes 源码本批 SHA 匹配，来源/commit 未固定：black flame 是黑色火焰，现译“邪恶火焰”改变颜色信息。
- 119af89312a36d7600832a7efc3ccad32e9fd116d081ded65cff5166411e63f0 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/zones/searing-halls/npcs.lua | 公开 Ashes searing-halls/npcs.lua:99 的 italic 标记分别强调 extracting 与 willing；现译把标记放到“志愿者”和“获取”，对应关系颠倒。修复标记附着位置并保持原意。
- 120d3d48def6138fa01a3c4bcfd8a0951444c4c840f8a23638c3ba39c9ee38f0 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | 公开 Ashes 记忆对白原文要求踏上 plate、摆好手臂，以便安置 bindings；现译“站在那里别动……把它放好”遗漏板子和束缚装置。
与 surface 同向：公开 Ashes demon.lua:135–137 的 plate 与 bindings 在译文中遗漏；“standard-issue alteration”被加成思维修改，“自抵达以来第一次避开监视”也被删。按本批文件 SHA 匹配的公开源码修复；来源/commit 未固定。
- 12c3c45f81bdf4d981fef66a1e7df1fcef2e3da1d42e153350b255b078ed4a84 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/zones/searing-halls/npcs.lua | 公开 Ashes 源文 3 arms 是三条手臂，现译“三只手”误作手掌；本批文件 SHA 匹配，来源/commit 未固定。
- 1be82f2f199d6d783d5293ac49acef643b763a0bc1a5ef1fabb39d94cd53aefe | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/quests/re-abducted.lua | primary ambush 指主要/最初的伏击，现译“面前伏击”改为位置关系；应恢复伏击的阶段或主次含义。
与 surface 同向：公开 Ashes re-abducted.lua:29–30 在 ambush 完成后显示，found your way out 表已脱身；现译只找到方法且 primary 误作“面前”。来源/commit 未固定。
- 218c180b3f864dac59b93985e4631c2d6b566b1417cfa81b297286c57a8c2e0e | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | 公开 Ashes 叙事原文是父 Urh'Rok 直接而热情地认可 Khulmanar 的头脑，现译“精神受到父的指引”把认可改成指引。
与 surface 同向：公开 Ashes demon.lua 对父亲的 direct, enthusiastic approval 误作“指引”；本条 Urh'Rok 译名先“乌尔洛克”后“乌鲁洛克”，锦标赛错成竞标赛，physical endurance 也误作物理耐受。来源/commit 未固定。
- 21d89ecd3e11c60fe85d124c2f93d5d0b6724bd13211828528f1d6ffca4c11a7 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/lore/demon.lua | 公开 Ashes 叙事原文说全副武装的堡垒停在兵工厂与人口中心上方；现译“所有武器系统都瞄准了”增添主动瞄准，改变威胁方式。
与 surface 同向：公开 Ashes demon.lua 的堡垒位置误作主动瞄准；译文还把“怀”错成“坏”、“所拥有”错成“所有用”，且增添“强大的力量”限定。来源/commit 未固定。
- 28ea98973ddf0d08e7eb5940be2d71fac43c10cbe3fc628304267189dd3945e2 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua | 公开 Ashes demon-seeds.lua:737 写 fiery display of speed，现译“闪电般”把火焰意象换成闪电。
- 295b84f066bb5e2610c84354d9f94de40a32ef9ded864d97373d29cbf3df47c5 | tome-ashes-urhrok.lua | tome-ashes-urhrok/data/talents/corruptions/wrath.lua | wrath.lua:186–195 源文各后续行以两个制表符缩进，译文改成一个，影响多行技能说明结构。Obliterating Smash 的 range 实际赋给圆锥 radius（wrath.lua:32–37），因此“增加半径”本身有机制依据，不作为修复原因。
- fcb8219fb8c88087dac87b64051d6e829b43affe9c13dacd2c8e9844eef9b78e | mod-tome.lua | mod-tome/class/interface/TooltipsData.lua | class/interface/TooltipsData.lua Antimagic User 说明：The use of spells or arcane-powered equipment is impossible.——class/Actor.lua:5059、5139（624a673）反魔法技能设 forbid_arcane，奥术装备与法术被禁用，是硬性限制；现译“拒绝使用法术”把不能写成主动拒绝（一级 fidelity）。修复第三行为“无法使用法术，也无法使用奥术驱动的装备”一类，#GOLD#…#LAST#、3 个 LF 保持。
- fd267689be1e30a3bf2673d23f3bcd4548acbbdd5785bce4dd9b21ff17466b80 | mod-tome.lua | mod-tome/data/general/objects/world-artifacts.lua | world-artifacts.lua:1134 领袖的皇冠（Crown of Command）描述：many disappeared without a trace into his numerous prisons——现译“这些人大部分都…消失了”把 many 夸大为“大部分”（一级 fidelity，数量限定被改）；另 ruled over the Nargol lands 译“纳格尔大陆”不当，Nargol 是半身人王国（本库 3794、3848 行“纳格尔半身人王国”）。整条修复：数量改“许多人”，“纳格尔大陆”改“纳格尔的领土/国土”一类，其余逐句对照。
与 surface 同向并补充：enforced order and discipline 被写成“执行他的命令和法律”；loyal to the crown 漏宾语；同条前称“王冠”后称“皇冠”不一致（物品名为“领袖的皇冠”，统一为“皇冠”）；Nargol lands 非“大陆”。并入同条整句修复。
- fd89fad0e8ec3640021b78b985babd87ee52ab2d142c87e961d61faf45ea735e | mod-tome.lua | mod-tome/data/talents/chronomancy/matter.lua | chronomancy/matter.lua Disintegration（624a673 matter.lua:271–306）：doStrip 按伤害类型分别以 p.physical[target] 与 p.magical[target] 记录，每目标每回合可各除去一项物理和一项魔法增益；现译“每个生物每回合只能被除去一项效果”把上限写错（一级 fidelity）。首句 respectively 亦丢失：物理伤害除去物理增益、时空伤害除去魔法增益（what = type == "PHYSICAL" and "physical" or "magical"）。整句修复，%d%%、两处 LF+制表符保持。
与 surface 同向并补充：While active 与 temporary 限定亦应保留；按 doStrip 实现整句修复（物理伤害除去物理增益、时空伤害除去魔法增益；每目标每回合各至多一项）。
- fd9c72bf32f198729cede9b435055adc761bcf5985bc58a84de23e0ac605a8d4 | mod-tome.lua | mod-tome/data/talents/gifts/oozing-blades.lua | gifts/oozing-blades.lua 技能名 Unstoppable Nature：现译“自然世界”完全丢失 Unstoppable；技能效果为无视目标自然抗性并令软泥吐射（oozing-blades.lua:179–180），本库 Unstoppable 统一作“势不可挡”（mod-tome.lua:2720、30187、36745）。改“势不可挡的自然”一类；该名只此一处出现。
与 surface 同向：自然世界 与英文名及机制（无视自然抗性、软泥免费吐射）均不符；本库 Unstoppable=势不可挡，改“势不可挡的自然”一类。
- fda88c9668327a676dffe3451ca50e5ae9bc3b92c01a1c22d72b14198be541b6 | mod-tome.lua | mod-tome/data/talents/techniques/unarmed-training.lua | techniques/unarmed-training.lua 技能名 Reflex Defense：效果是提高架势的固定伤害减免并降低受暴击倍率（unarmed-training.lua:128），与闪避无关；现译“闪避神经”既非原义又误导机制（且与 Reflexive Dodging=闪避反射 混淆）。改“反射防御”一类；该名只此一处出现。
- fdff442a1e55fecae18f6dd9bb4761bb6c0572059c4f4a1706ef5d06fa3ff2d2 | mod-tome.lua | mod-tome/data/talents/gifts/mucus.lua | gifts/mucus.lua：damage_types.lua:3704–3717 MUCUS 对每回合处于粘液格上的友方生效（按格上 actor 结算，turn_procs 每回合一次），原文 friendly creatures in your mucus；现译“每个经过粘液的友方单位”把条件改为经过（一级 fidelity）。改“处在你粘液中的其他友方单位”，保持“为你和其自身各回复 1 点”，其余不变。
- fe42c359a5490ee337c6eb5084fb0103ac39e17315c25f59ef278b2823eceae5 | mod-tome.lua | mod-tome/data/chats/alchemist-hermit.lua | chats/alchemist-hermit.lua：THE LONGER YOU WAIT, THE MORE LIKELY … SMOKING CRATER AND ONE TRULY IRATE HALFLING——原意是越晚回来越可能看到冒烟的弹坑和暴怒的半身人；现译改为“你在这儿待的时间太长”，丢失弹坑并把冒黑烟挂到半身人身上（一级 fidelity）。整句修复末两句，#LIGHT_GREEN#/#WHITE# 与 LF 保持。
与 surface 同向：越晚回来越可能见到冒烟的弹坑和暴怒的半身人；现译改成“在这儿待太久”并丢失弹坑。整句修复末两句。
- fe5a84a1b4161500b909f7c7cccf4ff56e0c0f33c004784dbe94c0364943c4d4 | mod-tome.lua | mod-tome/data/talents/spells/enhancement.lua | spells/enhancement.lua 燃烧之手（Fiery Hands）：enhancement.lua:83–85（624a673）melee_project 火焰伤害作用于近战命中（含武器），体力回复为 stamina_regen_on_hit，仅命中时触发；现译第二行“每次攻击同时也会回复”把命中写成攻击（未命中也回复，一级 fidelity），首句亦漏“（及武器）”。修复：第一行补“双手（及武器）”，第二行改“每次命中”，%0.2f/%d%%、两处 LF+制表符保持。
与 surface 同向：首句漏“（及武器）”，并入同条修复（另含 surface 指出的“每次命中”）。
- fe90619ef2e1e48cab53d9352846971ad10ff1dfb3bbff4bfc27a5f58bea47f6 | mod-tome.lua | mod-tome/data/talents/corruptions/shadowflame.lua | corruptions/shadowflame.lua 恶魔空间（Fearscape）：原文 burn both of you … each turn，灼烧是持续每回合结算的光环（shadowflame.lua:219 设 level.demonfire_dam，zones/demon-plane-spell/grids.lua:23–26 熔岩地面 on_stand 每回合对站立者结算 DEMONFIRE）；现译“造成 %0.2f 火焰伤害”删去“每回合”，读作一次性伤害（删量词缺陷类，一级 fidelity）。另 When the spell ends 涵盖主动结束、目标死亡与活力耗尽，现译“当技能中断时”收窄，同句修为“法术结束时”。其余行与 LF+制表符不变。
与 surface 同向并补充：constant aura 译“永恒之焰”未表达持续光环，并入同条整句修复（每回合、法术结束时、持续火焰光环）。
- fec0939b43c92583f4d00aeb244393a5348b9d4d9d20be01e6b3cb39ceaa0d35 | mod-tome.lua | mod-tome/data/lore/last-hope.lua | lore/last-hope.lua 黑暗者古尔莫特墓志铭：原文斜体诗三行（In this bright age / Of new adventures / You are not forgotten），现译合并前两行为一行，LF 由 6 变 5（换行不变量，一级）。修复：拆回三行，例如“在这光明的时代\n在崭新的冒险中\n你不会被遗忘”，#{bold}#/#{normal}#/#{italic}# 与其余 LF 保持。
- ff47fb8608636c14b4edd992f2f91eb3cfefc2eeab07857e8bc51adbffa7457b | mod-tome.lua | mod-tome/init.lua | init.lua 加载提示：原意是回复纹身效果持续数回合，因此可预判即将承受的伤害并提前使用；现译删去“预判伤害、提前准备”这一要点，改写成泛泛的“更加从容”（一级 fidelity），且物品名本库为“回复纹身”（mod-tome.lua:12070 entity name）而非“恢复纹身”。整句修复。
与 surface 同向并补充：“开启后”暗示可开关技能，纹身为一次性使用物品；并入同条整句修复。
- ff585d0b17d2092a15ee66c669828233c547008396dfa8f6e1aa4adefd8af6a7 | mod-tome.lua | mod-tome/data/quests/deep-bellow.lua | quests/deep-bellow.lua 任务名 From bellow, it devours：同一短语在本库另一处作“来自深渊，吞噬四方。”（mod-tome.lua:38225，Deep Bellow=深渊咆哮），任务名却改成名词“地下吞噬者”，同一英文句两种不相容译法（跨条一致性/术语，一级）。修复为“来自深渊，吞噬四方”（任务名不带句号），与 38225 对齐。
- ff658fab2952efff6ddacb8a31c9598d2d5337642bdd2fa7d640b496bf77f6ee | mod-tome.lua | mod-tome/data/general/objects/world-artifacts.lua | world-artifacts.lua unided_name wispy purple cloak：wispy 指轻薄缥缈（同物系靴子 12911 行 wispy purple aura 作“紫色光环”），“脆弱的”义为易损，错译（一级 fidelity）。改“缥缈的紫色斗篷”一类。
与 surface 同向：该物品为 Ethereal Embrace，描述 waves and bends with shimmering light，wispy 应作缥缈/轻纱感。
- ffb21dd4ccd3ada3cb0abcecd6ee531904750bce1b6d8b41fdc441b29cf91839 | mod-tome.lua | mod-tome/data/timed_effects/magical.lua | 固定主游戏 magical.lua:600–618：SUPERCHARGE_GOLEM 结束移除伤害和生命回复增益；“seems less dangerous”是威胁降低，现译“平静了下来”误述情绪。修复为“#Target#看起来没那么危险了。”一类，保留 #Target#。
与 surface 同向：固定主游戏 magical.lua:600–618 的增伤效果结束，less dangerous 表威胁降低而非情绪平静；并入同条修复。
- ffe80f4c81073264933cfb717896ef7ecf7004171e9a9030e065ac3dab3101ae | mod-tome.lua | mod-tome/data/maps/vaults/auto/greater/portal-vault.lua | 固定主游戏 portal-vault.lua:133 原文 A strange portal to some place else，现译遗漏 strange 的“奇异”信息。补回该限定，不改运行键。
与 surface 同向：固定主游戏 portal-vault.lua:133 的 strange 被省略；并入同条修复。
- fff8487389cbed3c2897bfc85f6d3c264537cae71a0985cdbf5e67c64a34c076 | mod-tome.lua | mod-tome/data/talents/gifts/summon-melee.lua | 固定主游戏 summon-melee.lua:500–538：岩石傀儡获 T_UNSTOPPABLE 技能，可进入不可阻挡状态；原文 can become，现译“并且不可阻挡”误作恒定状态。修复为“有可能变得不可阻挡”。damage%% 已由“百分比伤害”表达，resistance penetration %% 为百分比属性，不把字面 %% 当运行时 placeholder 要求。
与 surface 同向：固定主游戏 summon-melee.lua:500–538 赋予 T_UNSTOPPABLE 技能，can become 为可触发状态；并入同条修复。
