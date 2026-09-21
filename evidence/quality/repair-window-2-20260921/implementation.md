# Repair window 2 implementation evidence

## Scope and provenance

- Role: the task's sole `EXECUTOR`; this record is implementation evidence, not an independent review or a `DONE` assertion.
- Translation file: `mod-tome.lua`.
- Frozen component/source identity: `tome`, `commit:624a67329fe2ad440c5b344785a9c73fcf22ae63`.
- Frozen source excerpts: `SOURCE-ANCHORS.json`, copied byte-for-byte from `.ai/task/repair-w2-20260921/SOURCE-ANCHORS.json` (SHA-256 `b7acb74cdc38a3c4d8e09c8ca06ddd0fa547baa65775815f9f60be84f93a13e9`). These are host-provided `git show` excerpts; no external checkout was assumed.
- Repair preflight workset: `preflight-workset.schema1.json`, copied from the successful preflight output `.artifacts/i18n/repair-window/window2-20260921-preflight-2.json` and the identical `.ai/task/repair-w2-20260921/WORKSET.json` (source SHA-256 `5a4b9917ca71896a1d17af3f57fec84132e4b0b6bc3e59237439a78d02dda0c5`). The saved JSON has the same parsed content and one final LF added by the patch writer (saved SHA-256 `d5f0dc5b7ecdb9bbc9c2c4e1794f4339dc75b768214514565d772756f9075ce8`). It contains exactly five items.
- Frozen fields retained for every item: `source`, `source_tag`, `args_order`, `special`, placeholder token multiset/order, markup, and newline structure. Only the five authorized targets changed.

## Per-entry repair and fixed-source verification

### `de6a65ed2bf9694bcff086b4d961aeeffa14868f69aeb11d997a75a84d71e421` — Atamathon and Garkul

- Anchor: `game/modules/tome/init.lua:89-95` in the fixed commit.
- Before: `在烈火纪，人们建造了巨型傀儡阿塔玛森以对抗兽人首领吞噬者加库尔所领导的兽人军队。加库尔不仅孤身一人亲自干掉了傀儡王，在他倒下之前，还单枪匹马斩杀了上千人的部队。`
- After: `在烈火纪，人们建造巨型傀儡阿塔玛森的唯一目的，就是阻止兽人首领吞噬者加库尔。加库尔仅凭一己之力便摧毁了这尊傀儡，随后又屠戮了一支数千人的军队，最终这名如恶魔般的战士才被杀死。`
- Fixed-source fact: `sole purpose` targets stopping Garkul himself; Garkul destroys the giant golem alone, then slaughters an army of thousands before being slain.
- Translation decision: removed the invented army-led-by-Garkul relation and the incorrect “傀儡王”, retained an unbounded “数千人” and rendered `demonic fighter` as the source's fierce comparison rather than a literal creature classification.

### `de83a721c1a9495beac993ede15beb5c703bd06d906eee24febc902d799c26d7` — Gloves of the Firm Hand

- Anchor: `game/modules/tome/data/general/objects/world-artifacts.lua:1165-1190` in the fixed commit.
- Before: `这副手套让你觉得坚如磐石！这双充满魔力的手套从里面摸起来无比松软。在其外，魔法石创造了一个不断转动的粗糙表面。当你振作精神，一束包含大地能量的魔法射线会将它自动扎根在地面上，赋予你更高的稳定性。`
- After: `这副手套令你感觉稳如磐石！这副魔法手套的内侧触感极其柔软，外侧则由不断变动的魔法石构成粗糙表面。当你稳住身体时，一道大地能量形成的魔法射线似乎会自动将它们固定在地面上，让你站得更稳。`
- Fixed-source fact: the description says the outer stones are constantly shifting and that, when the wearer braces, a ray of earth energy *seems* to bind the gloves to the ground.
- Translation decision: corrected `brace yourself` to stabilizing one's body, `shifting` to movement rather than rotation, preserved the uncertainty in `seems`, and did not promote the flavor text into an additional gameplay mechanic.

### `de87dbd2517ed4a4264e7b26a3e43784a1c4a845521a6f2584062d624ec33e8d` — Wild Summon

- Anchors: `game/modules/tome/data/talents/gifts/summon-advanced.lua:104-143`, `.../summon-utility.lua:175-205`, `.../techniques/superiority.lua:74-106`, and `game/modules/tome/data/timed_effects/mental.lua:2094-2114` in the fixed commit.
- Before: the first line asserted that one wild summon was directly summoned; the turtle line described taunting; the rest of the target also omitted or weakened several surface details.
- After: the first line is `在 %d 回合内，你的召唤兽出现时有 100%% 几率成为野性版本。`; the turtle line is `乌龟：可以迫使半径内所有敌人进入近战范围`; the remaining lines preserve the full talent/power list and its activation/scaling statements.
- Fixed-source fact: activation only applies `EFF_WILD_SUMMON` for `t.duration(self,t)` with `chance=100`; the timed effect changes that chance each turn to `floor(chance * 0.66)`. Summon creation separately tests `rng.percent(wild_summon)`. A wild turtle gains `T_BATTLE_CALL`, whose action relocates affected enemies to free grids near the turtle; the base turtle already has `T_TAUNT` and invokes it independently.
- Translation decision: describes a decaying chance for later summons to appear wild, not an immediate summon. The turtle description follows Battle Call's forced relocation and does not conflate it with base Taunt.

### `de9af808fffcbe480b1c10f7948a421f6f7571f4015e5fa16557cc1cdc42fa85` — Indiscernible Anatomy

- Anchors: `game/modules/tome/data/talents/gifts/ooze.lua:248-274` and `game/modules/tome/data/damage_types.lua:29-55,123-156` in the fixed commit.
- Before: `你身体里的内脏全都融化在一起，隐藏了你的要害部位。\n\t\t你有 %d%% 几率摆脱任何（物理，精神，法术）暴击。\n\t\t你将额外获得 %d%% 的疾病、毒素、切割和目盲免疫。`
- After: `你体内的器官模糊难辨，掩盖了你的要害部位。\n\t\t你受到的直接暴击（物理、精神、法术）的额外伤害降低 %d%%。\n\t\t你将额外获得 %d%% 的疾病、毒素、切割和目盲免疫。`
- Fixed-source fact: the talent stores `t.critResist(self,t)` in `ignore_direct_crits`. For a direct critical hit (`crit_power > 1`), the projector deterministically subtracts `ignore_direct_crits / 100` of the bonus multiplier `(crit_power - 1)`, bounded to 0-100%, then recomputes damage. It does not make an RNG roll and does not reduce the base, non-critical portion of the hit. The four immunity fields receive `t.immunities(self,t)` and the displayed second value is `100 * t.immunities(self,t)`.
- Translation decision: explicitly supersedes the historical “chance to ignore direct critical hits” interpretation. The first placeholder now describes percentage mitigation of direct-critical *extra damage*, not a proc chance or total-damage reduction; the established immunity wording remains intact.

### `de9e666ad0b4d9f1774c91cd59a443c4bf424afe3f58e12961bad77bbdcb6336` — Honeywood Chalice description

- Anchor: `game/modules/tome/data/general/objects/world-artifacts.lua:5934-5955` in the fixed commit.
- Before: `这个酒杯里装满了粘稠的物质，尝一口能提神醒脑。`
- After: `这个木杯似乎总是盛满一种浓稠的树液状物质。尝上一口令人精神振奋，同时会让你的感知变得异常敏锐。`
- Fixed-source fact: the object is a wooden cup that seems perpetually filled with a thick sap-like substance; tasting it is exhilarating and produces intense awareness.
- Translation decision: restored `wooden`, `seems perpetually`, `sap-like`, and the heightened-awareness result without introducing wine.

## Numeric placeholder value flow

| Revision | Source placeholder index | Raw token | Quantity kind | Directional value flow | Target meaning |
| --- | ---: | --- | --- | --- | --- |
| `de87db...` | 1 | `%d` | duration (turns) | `duration()` → `setEffect(..., t.duration(self,t), {chance=100})` and the same `t.duration(self,t)` → `tformat` argument 1 | `%d 回合` |
| `de9af8...` | 1 | `%d%%` | critical bonus mitigation percentage | `critResist()` → `ignore_direct_crits` → `(crit_power - 1) * bound(value,0,100) / 100`; the same `critResist()` → `tformat` argument 1 | direct-critical extra damage reduced by `%d%%` |
| `de9af8...` | 2 | `%d%%` | immunity percentage | `immunities()` fractional value → four `*_immune` attributes; `100 * immunities()` → `tformat` argument 2 | `%d%%` disease/poison/cut/blindness immunity |

`100%%` in Wild Summon is an escaped literal percentage, not an additional format argument. Both entries retain `args_order=null`; source-order and target-order placeholder tokens are identical. The Anatomy target is intentionally more explicit than the stale English surface: every required anchor is fixed above and closes the value flow from the displayed value through `ignore_direct_crits` to the projector formula. No unsupported numeric scope, timing condition, or trigger was added.

## Validation boundary

The command receipts are in `validation.json`. Full gates, independent REVIEW/FINAL_REVIEW, commits, queue/catalog work, push, and `DONE_VERIFIED` remain host/orchestrator work and are not claimed here.
