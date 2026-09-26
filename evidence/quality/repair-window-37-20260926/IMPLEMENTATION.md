# Repair window 37 implementation

Task: `repair-w37-20260926`

Base commit: `3f18f6efb7492d08697dd5a72a9b7bf4dfdd472c`

Scope: only the 25 frozen targets in `tome-cults.lua` and `tome-orcs.lua` were changed. No source, source tag, section, args order, special field, runtime key, terminology record, or task record was changed.

## Per-entry changes

1. `016c0578` — restored the already-burning temporal relation in Graynot chapter 83.
2. `03eccaa9` — stated that Smoke Cover can completely absorb any damaging action.
3. `046aa43c` — restored the nested advertising quotation and translated “a shot” as one fired shot.
4. `07679a7e` — translated `packs a punch` as strong impact rather than weight.
5. `0a43ee37` — aligned the on-gain log with the established “自动飞锯” wording. The adjacent on-lose source/target was checked; it is outside this frozen target and was not changed.
6. `0b55d129` — repaired the Krimbul account’s causality, uncertainty, chronology, sensory terms, and all additional sentence-level issues frozen by the host precheck.
7. `0b59fe6a` — restored the two separator blank lines; unified `To:`; corrected “再”; translated `inspection` as “视察”; and restored the growing-impatience sign-off.
8. `0daa4319` — restored the condition that the damage reduction applies while Furnace is active.
9. `10291d1d` — translated Mindwall’s split mind and the orcs subdued under his control without the previous additions.
10. `1094f94c` — repaired the warning’s uncertainty, scope, treant reaction, infection inference, conditional great-tree statement, and other host-prechecked sentence issues.
11. `10a2bd7c` — changed only the recipe category `electricity` from “电子学” to “电学”.
12. `12378ea3` — clarified the per-target once-per-turn limit and lack of Counterstrike interaction.
13. `14ab7a98` — made Golden Gun’s critical hit rule explicitly periodic: every third hit.
14. `14f18b1e` — translated the tantalizing notion of eternal life as an enticing idea.
15. `15bfd5dc` — restored both source-matching two-tab line prefixes in Iron Grip.
16. `16499122` — restored Embedded Restoration Systems to four source-matching lines and described its trigger as a cooldown ceiling.
17. `16531ad8` — restored all three two-tab prefixes; translated the toxic shot, ammo explanation, toxin scaling, and global-speed term completely.
18. `179e471e` — removed the source-absent two-tab prefix from Surekill’s second line.
19. `17d6df13` — restored Grinder’s kitchen-tool origin, carcass sense, referent, and sinister quality.
20. `f9cadd37` — restored the Worm that Walks robe decay, splitting seams, spilling worms, mucus-soaked maggots, pus, and writhing droplets.
21. `fa9f7169` — added only the missing third tab on Temporal Feast’s second line; the implementation-aligned surrounding-range wording was retained.
22. `fbe22d02` — repaired the armor gashes and all additional Fay Willows sentence issues frozen by the host precheck.
23. `fd188846` — described Black Hole’s effect as a radius-1 spacetime rift and referred to the rift center.
24. `ff1e300b` — restored the bone-staff creaking/vibration wording and terminal punctuation.
25. `ffc35a30` — restored the chance qualifier and maximum amplitude for insanity’s damage/cooldown variation.

## Validation summary

- The LuaJIT loader compared both current files with the frozen base commit: 25 changed targets exactly (`tome-cults.lua`: 6; `tome-orcs.lua`: 19), with all other records and non-target fields unchanged.
- All changed targets preserve preimage placeholder, markup, and template-expression sequences; line count, blank-line indices, and leading-tab shape match their source strings; file-final newlines are unchanged.
- All 25 public-source file SHA-256 values match `SOURCE-ANCHORS.json`. The DLC repository and commit remain unpinned, as recorded by the task.
- Strict lint completed with 30308 translations, 0 errors, and 0 warnings.
- `git diff --check` completed with no diagnostics.

No files were staged, committed, or pushed.
