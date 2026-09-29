# v2 public 复审裁决（2026-09-24，含 17:30 复核）

task_id: `human-review-adjudication-20260923`

结果：**confirmed 19** ／ advisory 19 ／ deferred 1。

## 0. 官方仓库 Undead 翻译现状（用户要求确认）

来源：`engine game/modules/tome/data/locales/zh_hans.lua` @ `624a6732`

**结构化术语（机制/运行时）：**

| source | target | tag | 次数 |
|---|---|---|---|
| `undead` | **亡灵** | entity type | 18 |
| `undead` | **亡灵** | talent category | 2 |
| `undead` | **亡灵** | effect subtype | 2 |
| `Undead` | **不死族** | birth descriptor name | 1 |

**自由文本（`_t` / log / tformat / entity name）里 undead 的落点：**

| 用词 | 次数 | 例 |
|---|---|---|
| 亡灵 | 10 | 「地上的亡灵正在复活！」 |
| 不死 / 不死系 | 10 | 「一系列不死系技能」 |
| 不死族 | 8 | 「装备者将被视为不死族。」 |
| 不死生物 | 5 | 「不知疲倦的不死生物」 |

**结论**：官方把 `undead`（实体类型/技能类别/效果子类型）固定为**亡灵**，把种族 `Undead` 固定为**不死族**；自由文本官方自己就混用四种，lore 叙述用「不死族」与官方现行做法一致 → `entry-01256` 维持 advisory，不改。

## 1. 本轮记录、暂不修改的族级问题

### magic-stat — Magic 作为属性值：统一为「魔力」还是保留「基于魔法」
- 状态：`recorded_no_change_this_round`；涉及：entry-01605, entry-01625
- 属性名 stat name = 魔力（mod-tome.lua:43206 / official zh_hans.lua:43130 / terminology Magic=魔力 existing）
- 自由文本 based on Magic：本仓 基于魔法 21 vs 基于魔力 3；（基于魔法）11 vs（基于魔力）2
- 处置：本轮记录，不修改

### frenzy-effect — frenzy 效果统一为「狂乱」还是「狂热」
- 状态：`recorded_no_change_this_round`；涉及：entry-01976
- 该状态是 EFF_FRENZY，由吞噬者技能 horrors.lua:149 / Bloodrage npcs.lua:1692 / 神器 boss-artifacts-far-east.lua:273 施加；Cursed 的 Frenzy 技能（cursed/slaughter.lua:86）不使用它
- 效果自身显示名 = 狂热（mod-tome.lua:36143 t("Frenzy","狂热","_t")；on_gain 陷入杀戮狂热 :36147；on_lose 狂热状态消失 :36068）
- terminology/combat.tsv:56 frenzy=狂乱（effect subtype, existing）；talent name Frenzy=狂热
- 处置：本轮记录，不修改

### undead-narrative — undead 自由文本是否统一为亡灵
- 状态：`official_survey_confirmed`；涉及：entry-01256
- 处置：已确认官方现状（见 official_undead_survey）：结构术语 undead=亡灵、Undead=不死族，自由文本官方自身即混用；本条保持 advisory，不修改

## 2. confirmed（待修复）

| entry / carrier | bundle | 类别 | 问题 | 
|---|---|---|---|
| `entry-01221` | ctx2-pub-09d | fidelity | elvala.lua:280 "as if it were warding against a dark and dangerous threat" rendered 仿佛要警告我提防某种黑暗而危险的威胁 |
| `entry-01223` | ctx2-pub-09f | completeness + fidelity | elvala.lua:358-400 four defects: brief periods of waking dropped and inverted to 不断给她水; gave her to the doctors with the strictest instructions became 让最好的治疗师; a bath of blood to wash over my sins misread; he could not fight back over-interpreted |
| `entry-01228` | ctx2-pub-09i | completeness (+ register) | lore/fun.lua skeleton/wight/lich sections: "fragile that a stiff breeze could break them apart" dropped; "a peculiar sense of exhaustion" dropped; "be a dear" idiom mis-rendered |
| `entry-01275` | ctx2-pub-10b | fidelity | "How can creation itself tolerate such an aberration?!" rendered 造物主 (creator) not 受造界/天地万物; and "think of what else it could have taken" truncated |
| `entry-01282` | ctx2-pub-10b | fidelity + completeness | misc.lua:230 "lesser gods than our own which copied his grand design ... the works of their design" — the copying clause is dropped and the sentence is rewritten as a comparison of handmade artworks |
| `entry-01302` | ctx2-pub-11b | terminology + fidelity | misc.lua:461 inscriptions rendered 符文 (subordinate concept) instead of the category term 刻印; regimen of runic inscription rendered 复杂的整体 |
| `entry-01308` | ctx2-pub-11b | fidelity | misc.lua:503 "to commune well in groups" rendered 团结一致的精神; "developed culture" rendered 优越文化 |
| `entry-01605` | ctx2-pub-15a | terminology + completeness | Warp Mines shortened to 地雷 (loses 时空) |
| `entry-01689` | ctx2-pub-15a | completeness | cunning/artifice.lua smoke bomb: the clause "even if their proximity would normally forbid it" is absent |
| `entry-01740` | ctx2-pub-15a | completeness (mechanic) | cunning/stealth.lua:148 "if there are foes in sight within range %d%s" — "in sight" is absent, turning it into any foe within range |
| `entry-02128` | ctx2-pub-19a | completeness (mechanic) | psionic/projection.lua:535-543 "on all your weapon hits, costing … per hit" rendered 每次攻击附加/每次攻击消耗 — drops 武器命中 and broadens to any attack |
| `entry-02451` | ctx2-pub-22a | terminology | techniques/weaponshield.lua Shield Wall "stun and knockback resistance" rendered 眩晕; stun is 震慑 (daze is 眩晕) |
| `entry-02474` | ctx2-pub-22a | terminology | "dealing %d ice damage to attackers" rendered 冰冻伤害 |
| `entry-02565` | ctx2-pub-23a | terminology | unlock-mage_necromancer.lua features: darkness rendered 黑暗, ice rendered 冰系, undead rendered 不死 |
| `entry-02576` | ctx2-pub-23b | fidelity | unlock-psionic_solipsist.lua:34 "Solipsists use their mind to manipulate the world around them." is replaced by a copy of the :26 sentence, dropping their mind |
| `entry-02763` | ctx2-pub-25a | fidelity (mechanic) | nightmares curse: "summon Terrors" rendered 召唤梦魇; and "chances to slow, deal %d Mind damage, and deal %d Darkness damage" rendered as unconditional 直接造成 |
| `entry-02846` | ctx2-pub-25a | terminology | CURSED_WOUND on_merge log renders cursed wound as 诅咒伤口 while the rest of the effect uses 诅咒创伤 |
| `mod-tome.lua:14630` | ctx2-pub-28a | fidelity + completeness | elvala.lua spellblaze-chronicles-1 (mod-tome.lua:14630): "if I judge right I see no mere impudent lass before me, but…" rendered 如果由我来说，我还从没见过如此失礼的姑娘，同时还是…; "to the east of here" dropped; "Alas" rendered 当然 with the subject of scaring inverted |
| `entry-03856` | ctx2-dlc-fix-01 | terminology + fidelity | orcs lore: constructs rendered 装置; and "most of our contact with the Atmos is still done via constructs dropped from airships" mistranslated |

## 3. deferred（本轮记录，不修改）

| entry | bundle | 类别 | 说明 |
|---|---|---|---|
| `entry-01625` | ctx2-pub-15a | terminology (recorded, no change this round) | temporal-hounds.lua renders the Magic stat as 魔法 (both in the six-stat list and in "based on your Magic stat") |

## 4. advisory（不修改，记录理由）

| entry | bundle | 类别 | 说明 |
|---|---|---|---|
| `entry-01256` | ctx2-pub-10a | terminology (existing only) | undead rendered 不死族 (lore narrative) |
| `entry-01976` | ctx2-pub-17a | terminology (conflicting in-repo usage) | frenzy rendered 狂热状态 (EFF_FRENZY) |
| `entry-01272` | ctx2-pub-10a | static typography | paragraph split only |
| `entry-01273` | ctx2-pub-10a | static typography | paragraph splits (9→13 newlines) |
| `entry-01318` | ctx2-pub-11c | register + static typography | Thank me later idiom and a lost blank line |
| `entry-01409` | ctx2-pub-13a | fidelity (style) | bend the world to their will rendered 妄图扭曲这个世界 |
| `entry-01512` | ctx2-pub-14a | stale key | frozen English lacks the shield-duration clause |
| `entry-01742` | ctx2-pub-15a | wording | outside of light radius → 阴影区域; power → 能力 |
| `entry-02028` | ctx2-pub-18a | register | bites the dust rendered 扑街 |
| `entry-02113` | ctx2-pub-19a | fidelity (minor) | 净化你当前所有的精神状态 adds 所有的 |
| `entry-02115` | ctx2-pub-19a | terminology (existing only) + typography | ghost → 鬼魂; added 注: paragraph; through an active mind link |
| `entry-02125` | ctx2-pub-19a | upstream defect | English itself swaps Accuracy/damage for the ranged entry |
| `entry-02141` | ctx2-pub-19a | fidelity (philosophy) | Nothing exists outside the mind’s ability to perceive it rendered 没有任何事物能逃脱精神力量的感知 |
| `entry-02212` | ctx2-pub-20a | terminology (family) | Flame talent rendered 火焰 |
| `entry-02269` | ctx2-pub-20a | wording | imbue rendered 安装 vs 镶嵌 |
| `entry-02520` | ctx2-pub-22a | proper noun | Welcome to Tales of Maj’Eyal rendered 欢迎你来到 ToME 4 |
| `entry-02644` | ctx2-pub-24a | upstream defect | poison resistance vs the poison_immune mechanic |
| `entry-02735` | ctx2-pub-24a | terminology (wording) | ice rendered 冰系 |
| `scope17:mod-tome.lua:17791` | ctx2-pub-28b | duplicate | same source string as entry-01282 (ctx2-pub-10b) |

## 5. 下一步

confirmed（19 条）→ Gemini 拟稿（proposal `--strict`）→ EXECUTOR 落盘 → cycle 1 有界复审 → 收尾。
