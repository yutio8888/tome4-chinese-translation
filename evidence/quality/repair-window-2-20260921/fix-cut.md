# Repair window 2 cycle 1 — Anatomy status-name correction

## Scope

- Revision: `de9af808fffcbe480b1c10f7948a421f6f7571f4015e5fa16557cc1cdc42fa85`.
- Only the already-authorized Anatomy target changed in cycle 1: `疾病、毒素、切割和目盲免疫` → `疾病、毒素、流血和目盲免疫`.
- The other four repaired targets and the rest of the Anatomy target remain byte-for-byte unchanged from cycle 0. No source field, source tag, placeholder, markup, newline, terminology data, old evidence, or task record was changed.

## Fixed-source verification and decision

- Frozen source: component `tome`, commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; exact excerpts are preserved in `SOURCE-CUT-ANCHORS.json`.
- `game/modules/tome/data/talents/gifts/ooze.lua:254-272` assigns the displayed immunity value to `cut_immune` alongside disease, poison, and blindness immunity.
- `game/modules/tome/class/Actor.lua:7554-7584` maps status type `cut` to the `cut_immune` attribute.
- `game/modules/tome/data/timed_effects/physical.lua:123-133` defines `CUT` with the player-visible description `Bleeding` and wound/cut/bleed subtypes.
- Existing corpus usage aligns this player-visible status as `流血`: `terminology/combat.tsv:54`, `mod-tome.lua:856`, `mod-tome.lua:22123`, and `mod-tome.lua:35713,36955,36957`.
- Therefore the prior cycle-0 statement that “切割” was already correct is superseded for this target. The immunity mechanism and the word `免疫` remain correct; this cycle changes only the status name to `流血`.

`HOST-CUT-01` is a host-confirmed fixed-source/corpus adjudication, not a result accepted from the rejected r0a1 stage. The old `implementation.md` remains the cycle-0 implementation record and is intentionally not rewritten.

## Validation boundary

Command receipts for this correction are recorded separately in `validation-c1.json`. This file does not claim independent review, final review, full gates, `DONE_VERIFIED`, staging, commit, or push.
