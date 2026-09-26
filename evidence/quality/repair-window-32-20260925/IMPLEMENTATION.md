# repair-w32-20260925 implementation

Role: Paseo EXECUTOR

Baseline: `ece7c2cf1615bbee68e92f99ff14db88feb3e1ab`

Scope: the 26 frozen `tome-cults.lua` targets in `WORKSET.json`; no source, source tag, section, argument order, runtime key, terminology, task record, or unrelated file was changed.

## Per-entry changes

1. `1cd6be4130` — corrected the castle-shifting logic, attackers' intent, tome capacity, and the sacrificed treasure; removed two unsupported embellishments.
2. `1fa32c1a9c` — corrected the single-person pipe width, concentrated-energy sentence, partial infection, Feral Drem name, black growth inference, machine number, teeth uncertainty, speaker number, and two unsupported additions.
3. `207cee7b93` — restored the source's single `LF + 2 TAB` sentence break and used the established `暗影` damage term.
4. `226a7774f7` — changed the assertion to `我们在哪里都格格不入`, leaving Kroshkurr as the following contrast.
5. `25d776f587` — removed the extra first-sentence line break; the target now has the source's two `LF + 2 TAB` breaks.
6. `272a8bbc7c` — corrected `organise anything`, the room relocation, and removed the unsupported evidentiary phrase.
7. `27ddebe5f3` — repaired the undead-battle narration: viewpoint, skeleton rows, wall fire, uncertainty, captain title, pursuit and gate direction, spell preparation causality, and stray grammar.
8. `283cf77312` — removed three added continuation indents, restored singular pronouns, and made secondary stats scale with creature level.
9. `28b401e79b` — distinguished the target's remaining `时间线` from its `生命线`; retained `尝试切断` per implementation evidence.
10. `2b501aeaa3` — restored the first continuation to three TABs.
11. `2b62b6a2bc` — translated the divine being, touch, and alteration of beings without changing the referent.
12. `2ceaa318de` — repaired the combat rules, attack directions, shoulder graze, brief duration, staff awareness, social disapproval, cloak wording, arm hit, and staggering under blows.
13. `2efb21d224` — translated the idiomatic ship name as `无心之失`.
14. `2f62b393f4` — restored `of pain` and made the digesting-weapon phrase grammatical.
15. `361c68c7f2` — changed the entity name to `畸形生物`, consistent with its vaguely humanoid description.
16. `375276147b` — restored `applied or increased`, removed the extra line break, and stated the opposed duration changes with the original placeholders.
17. `3793a03188` — restored rune-activation instruction, catching breath, guards whispering, event order, uncertainty, and the worried guard's viewpoint.
18. `39b42b7c4c` — restored both rescue from death and successful escape, without the unsupported giant-worm/escort wording.
19. `3a4713aa3b` — repaired the Shroud destination, settlement term, cloaked-figure consistency, `in full view`, and `the rest` as the remaining skeletons.
20. `3aec400709` — restored `filth` as `污秽`.
21. `3b3a38f90d` — restored `attempt to daze`; the effect remains resistible.
22. `3bdd721e24` — restored the three-TAB continuation and the consecutive out-of-sight removal condition.
23. `3c623f8392` — restored the three-TAB continuation.
24. `3cfa2ffbf9` — restored all three paragraph gaps; corrected the Ziguranth body changes, `马基·埃亚尔`, and `卡·普尔`.
25. `4003c28c70` — corrected `corrupted beyond hope`, restored the missing paragraph gap, and aligned `天谴之龙` wording.
26. `4555f7111c` — corrected collapse from exhaustion, uncertainty, commander naming, eye glow, unconscious duration, and eating at the cleared table rather than eating cobwebs.

## Validation summary

- Manifest-compatible LuaJIT loaded baseline and current `tome-cults.lua`: 2043 records, exactly 26 target changes, zero non-target field changes.
- LuaJIT line-shape check: all 26 changed targets match their source for LF count, TAB depth after every LF, and trailing-newline state.
- All 26 source queries (20 unique files) matched the SHA-256 values frozen in `SOURCE-ANCHORS.json`, using only `/workspace/tome4-dlcs/cults/<public_source_path>`.
- `python3 -B tools/i18n lint --strict`: 30308 translations, 0 errors, 0 warnings.
- `git diff --check`: passed.

The first anchor-check attempt incorrectly stripped the leading `tome-cults/` path component and failed with `FileNotFoundError`; the corrected bounded command used each frozen `public_source_path` directly beneath `cults_checkout` and passed all hashes. This did not modify any file.

## Residual risk

The public Cults checkout and commit are not pinned. File hashes match the frozen anchors, so this implementation is tied to those exact file bytes, but it must not be represented as verification against a repository commit. Independent review and the host's final production gates remain outstanding.
