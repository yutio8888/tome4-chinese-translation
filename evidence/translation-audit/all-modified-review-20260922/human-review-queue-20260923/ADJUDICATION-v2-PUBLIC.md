# v2 public 复审裁决（2026-09-24，含 17:20 复核修订）

task_id: `human-review-adjudication-20260923`

范围：wave 1–3 之后的 public bundle finding（含 DLC 修复后复审 `ctx2-dlc-fix-01`），共 **39 条**。

结果：**confirmed 20** ／ advisory 19。

方法：以固定 commit 公开源码／术语库／仓内用法为准，reviewer severity 不作为事实。

策略：纯静态排版（空格、分段、换行数）不算缺陷；早前 601 行轮已裁决过的同一 claim 记 advisory；术语 `existing`（非 preferred）不强制。

## 修订记录（用户质询后）

- `entry-01256` confirmed → **advisory**：`undead` 实体类型术语为 `existing`，非强制；lore 叙述中「不死族」可接受，且同文件已混用。
- `entry-01976` confirmed → **advisory**：该状态是 **EFF_FRENZY**，由吞噬者技能（`horrors.lua:149`）／Bloodrage 施加，**不是** Cursed 的 Frenzy 技能；效果自身显示名即「狂热」。
- `entry-01605` 收窄为「Warp Mines→时空地雷」；「基于魔法／基于魔力」转为 advisory（族级约定问题）。
- `entry-01625` 维持 confirmed：六维属性枚举 + `Magic stat` → **魔力**。

## 一、confirmed（待修复）

| entry / carrier | bundle | 类别 | 问题 | 依据要点 |
|---|---|---|---|---|
| `entry-01221` | ctx2-pub-09d | fidelity | elvala.lua:280 "as if it were warding against a dark and dangerous threat" rendered 仿佛要警告我提防某种黑暗而危险的威胁 | fixed source game/modules/tome/data/lore/elvala.lua:280 @624a6732 — the subject "it" wards against the threat (防护/抵御); the next line (282) separately says "something tryi |
| `entry-01223` | ctx2-pub-09f | completeness + fidelity | elvala.lua:358-400 four defects: brief periods of waking dropped and inverted to 不断给她水; gave her to the doctors with the strictest instructions became 让最好的治疗师; a bath of blood to wash over my sins misread; he could not fight back over-interpreted | fixed source game/modules/tome/data/lore/elvala.lua:360 "giving her water during brief periods of waking"; :362 "gave her to the doctors with the strictest instructions"; |
| `entry-01228` | ctx2-pub-09i | completeness (+ register) | lore/fun.lua skeleton/wight/lich sections: "fragile that a stiff breeze could break them apart" dropped; "a peculiar sense of exhaustion" dropped; "be a dear" idiom mis-rendered | fixed source game/modules/tome/data/lore/fun.lua:234 and :247 @624a6732 |
| `entry-01275` | ctx2-pub-10b | fidelity | "How can creation itself tolerate such an aberration?!" rendered 造物主 (creator) not 受造界/天地万物; and "think of what else it could have taken" truncated | fixed source game/modules/tome/data/lore/misc.lua:131 and :135 @624a6732 |
| `entry-01282` | ctx2-pub-10b | fidelity + completeness | misc.lua:230 "lesser gods than our own which copied his grand design ... the works of their design" — the copying clause is dropped and the sentence is rewritten as a comparison of handmade artworks | fixed source game/modules/tome/data/lore/misc.lua:230 @624a6732 |
| `entry-01302` | ctx2-pub-11b | terminology + fidelity | misc.lua:461 inscriptions rendered 符文 (subordinate concept) instead of the category term 刻印; regimen of runic inscription rendered 复杂的整体 | terminology/talents.tsv:8 inscriptions=刻印 [T.GAME.TALENT_CATEGORY/preferred/global] "统一核心和兽人战役的技能类别译法；具体类型仍使用纹身/符文" |
| `entry-01308` | ctx2-pub-11b | fidelity | misc.lua:503 "to commune well in groups" rendered 团结一致的精神; "developed culture" rendered 优越文化 | fixed source game/modules/tome/data/lore/misc.lua:503 @624a6732 — commune = 交流/沟通, not 团结一致; developed culture is a degree (发达/成熟) not a value judgement |
| `entry-01605` | ctx2-pub-15a | terminology + completeness | Warp Mines shortened to 地雷 (loses 时空); *and* "(based on your Magic)" rendered 基于魔法 | in-repo talent name t("Warp Mines","时空地雷","talent name") (mod-tome.lua:22291); 8 uses of 时空地雷; the sibling entry :22280 uses 时空地雷 |
| `entry-01625` | ctx2-pub-15a | terminology | temporal-hounds.lua: the six-stat enumeration and "based on your Magic stat" render Magic as 魔法 | stat NAME is t("Magic","魔力","stat name") (mod-tome.lua:43206) and t("Magic","魔力","_t") (:42163); official zh_hans.lua:43130 is 魔力 too |
| `entry-01689` | ctx2-pub-15a | completeness | cunning/artifice.lua smoke bomb: the clause "even if their proximity would normally forbid it" is absent | fixed source game/modules/tome/data/talents/cunning/artifice.lua:582-585 @624a6732 — the talent’s core effect is the exemption from the proximity rule (stealth.lua:74 ste |
| `entry-01740` | ctx2-pub-15a | completeness (mechanic) | cunning/stealth.lua:148 "if there are foes in sight within range %d%s" — "in sight" is absent, turning it into any foe within range | fixed source game/modules/tome/data/talents/cunning/stealth.lua:148 and the :24-37 stealthDetection test (fov/actors/self and canSee) |
| `entry-02128` | ctx2-pub-19a | completeness (mechanic) | psionic/projection.lua:535-543 "on all your weapon hits, costing … per hit" rendered 每次攻击附加/每次攻击消耗 — drops 武器命中 and broadens to any attack | fixed source game/modules/tome/data/talents/psionic/projection.lua:535-543 and Combat.lua:961 (hitted and not target.dead) |
| `entry-02451` | ctx2-pub-22a | terminology | techniques/weaponshield.lua Shield Wall "stun and knockback resistance" rendered 眩晕; stun is 震慑 (daze is 眩晕) | terminology/combat.tsv:40 stun=震慑 [T.GAME.EFFECT/effect subtype/existing/core] |
| `entry-02474` | ctx2-pub-22a | terminology | "dealing %d ice damage to attackers" rendered 冰冻伤害 | terminology/combat.tsv:24 ice=寒冰 [T.GAME.DAMAGE/damage type/existing/global] |
| `entry-02565` | ctx2-pub-23a | terminology | unlock-mage_necromancer.lua features: darkness rendered 黑暗, ice rendered 冰系, undead rendered 不死 | terminology/combat.tsv:10 darkness=暗影 [T.GAME.DAMAGE/damage type/existing/core]; :24 ice=寒冰; terminology/creatures.tsv:12 undead=亡灵 |
| `entry-02576` | ctx2-pub-23b | fidelity | unlock-psionic_solipsist.lua:34 "Solipsists use their mind to manipulate the world around them." is replaced by a copy of the :26 sentence, dropping their mind | fixed source game/modules/tome/data/texts/unlock-psionic_solipsist.lua:26 vs :34 @624a6732 (the two sentences differ) |
| `entry-02763` | ctx2-pub-25a | fidelity (mechanic) | nightmares curse: "summon Terrors" rendered 召唤梦魇; and "chances to slow, deal %d Mind damage, and deal %d Darkness damage" rendered as unconditional 直接造成 | fixed source game/modules/tome/data/timed_effects/other.lua:1565-1575 npcTerror (name="terror", type="horror", subtype="eldritch"); in-repo t("horror","恐魔") |
| `entry-02846` | ctx2-pub-25a | terminology | CURSED_WOUND on_merge log renders cursed wound as 诅咒伤口 while the rest of the effect uses 诅咒创伤 | terminology/combat.tsv:74 wound=创伤 [T.GAME.EFFECT/effect subtype/existing/global] |
| `mod-tome.lua:14630` | ctx2-pub-28a | fidelity + completeness | elvala.lua spellblaze-chronicles-1 (mod-tome.lua:14630): "if I judge right I see no mere impudent lass before me, but…" rendered 如果由我来说，我还从没见过如此失礼的姑娘，同时还是…; "to the east of here" dropped; "Alas" rendered 当然 with the subject of scaring inverted | fixed source game/modules/tome/data/lore/elvala.lua:46, :56, :64 @624a6732 |
| `entry-03856` | ctx2-dlc-fix-01 | terminology + fidelity | orcs lore: constructs rendered 装置; and "most of our contact with the Atmos is still done via constructs dropped from airships" mistranslated | terminology/creatures.tsv:4 construct=构装体 [T.GAME.ENTITY/entity type/preferred/global] "不作机关" |

## 二、advisory（不修改，记录理由）

| entry | bundle | 类别 | 说明 | 依据／先例 |
|---|---|---|---|---|
| `entry-01256` | ctx2-pub-10a | terminology (existing only) | undead rendered 不死族 (lore narrative) | terminology/creatures.tsv:12 undead=亡灵 is status=existing (not preferred); terminology/creatures.tsv:54 Undead=不死族 is the race/birth-descriptor term |
| `entry-01976` | ctx2-pub-17a | terminology (conflicting in-repo usage) | frenzy rendered 狂热状态 (EFF_FRENZY) | the state is EFF_FRENZY, set by the Devourer talent (game/modules/tome/data/talents/misc/horrors.lua:149) and Bloodrage (misc/npcs.lua:1692) and an artifact — NOT by the  |
| `entry-01272` | ctx2-pub-10a | static typography | paragraph split only | prior hrq-00181: 分段本身仅排版且换行受冻结保护；user policy treats pure static typography as non-defect |
| `entry-01273` | ctx2-pub-10a | static typography | paragraph splits (9→13 newlines) | same static-typography policy; prior hrq-00182/00183 |
| `entry-01318` | ctx2-pub-11c | register + static typography | Thank me later idiom and a lost blank line | prior hrq-00205: “一会儿谢”仅口吻生硬，非一级错误 |
| `entry-01409` | ctx2-pub-13a | fidelity (style) | bend the world to their will rendered 妄图扭曲这个世界 | prior batch-06: model self-marked advisory; 用户提示为文风取舍，不构成一级缺陷 |
| `entry-01512` | ctx2-pub-14a | stale key | frozen English lacks the shield-duration clause | prior batch-06: 该句在冻结英文源串中本就不存在，不是译文遗漏，不能凭其他版本补入 |
| `entry-01742` | ctx2-pub-15a | wording | outside of light radius → 阴影区域; power → 能力 | prior batch-15: “能力增加 %d”已表达数值方向；power 由“能力”承接 |
| `entry-02028` | ctx2-pub-18a | register | bites the dust rendered 扑街 | prior batch-08: 属俚语风格 advisory，保留 |
| `entry-02113` | ctx2-pub-19a | fidelity (minor) | 净化你当前所有的精神状态 adds 所有的 | prior batch-08 no_change: 后句已限定前句“所有”的实际配额，孤立截取前句不足以确认缺陷 |
| `entry-02115` | ctx2-pub-19a | terminology (existing only) + typography | ghost → 鬼魂; added 注: paragraph; through an active mind link | prior batch-08 no_change: ghost=幽灵 仅为 existing 术语，不强制改名 |
| `entry-02125` | ctx2-pub-19a | upstream defect | English itself swaps Accuracy/damage for the ranged entry | prior batch-08 no_change: 原文说明本身次序写反，译文忠实承接英文；上游失准不计为中文新增错误 |
| `entry-02141` | ctx2-pub-19a | fidelity (philosophy) | Nothing exists outside the mind’s ability to perceive it rendered 没有任何事物能逃脱精神力量的感知 | prior batch-08 no_change: 现译表达同一全称关系；NOTE: the v2 reviewer reads this differently — recorded advisory, not reopened |
| `entry-02212` | ctx2-pub-20a | terminology (family) | Flame talent rendered 火焰 | user decision 2026-09-24: A 组 Flame 暂不修改；family unification (entry-02285 etc.) not authorized |
| `entry-02269` | ctx2-pub-20a | wording | imbue rendered 安装 vs 镶嵌 | prior batch-08 no_change: “安装”可描述置入，“附魔/镶嵌”并存，无唯一规范词 |
| `entry-02520` | ctx2-pub-22a | proper noun | Welcome to Tales of Maj’Eyal rendered 欢迎你来到 ToME 4 | prior batch-10 no_change: ToME 4 是通行缩写；NOTE in-repo elsewhere uses 马基·埃亚尔的传说 — recorded advisory, not reopened |
| `entry-02644` | ctx2-pub-24a | upstream defect | poison resistance vs the poison_immune mechanic | fixed source magical.lua:2794 itself says "poison resistance is reduced"; the mechanic is poison_immune (poisons.lua:576). English/behaviour mismatch is upstream; target  |
| `entry-02735` | ctx2-pub-24a | terminology (wording) | ice rendered 冰系 | prior batch-08 no_change: ice 对应寒冰的既有术语记录与现译一致 |
| `scope17:mod-tome.lua:17791` | ctx2-pub-28b | duplicate | same source string as entry-01282 (ctx2-pub-10b) | adjudicated once under entry-01282; duplicate key kept for traceability |

## 三、待定的族级决定

1. **Magic 作为属性值**：属性名（stat name）为 **魔力**（`t("Magic","魔力","stat name")`、terminology `Magic=魔力`）；但自由文本 `based on Magic` 仓内多数为「基于魔法」（21 处 vs 3 处）。需定统一方向。
2. **frenzy 效果**：terminology `frenzy=狂乱`（effect subtype, existing）与仓内效果自身用词「狂热」（`t("Frenzy","狂热","_t")`）冲突。需决定统一为「狂乱」还是「狂热」（并覆盖 effect 显示名／on_gain／技能信息／talent name）。
3. **undead**：`undead` 实体类型 = 亡灵（existing）、`Undead` 种族 = 不死族；自由文本是否统一为「亡灵」。

## 四、下一步

confirmed（20 条）→ Gemini 拟稿（proposal `--strict`）→ EXECUTOR 落盘 → cycle 1 有界复审 → 收尾。
