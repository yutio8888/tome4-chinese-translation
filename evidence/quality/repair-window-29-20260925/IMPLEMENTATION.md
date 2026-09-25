# repair-w29-20260925 implementation

## Scope

- Modified only the 21 frozen translation targets in `tome-ashes-urhrok.lua`.
- Preserved every source, source tag, argument order, special field, and all non-workset records.
- Did not modify terminology, task state, rules, source code, or unrelated working-tree files.
- Ashes source repository/commit remains unpinned. Every referenced source file matched the SHA-256 frozen in `SOURCE-ANCHORS.json` before implementation.

## Target changes

1. `6b24dee87b2b`: corrected the Harkor'Zun lore's anomalies/phenomena, predictable fragment sizing, reverse engineering, standard troops, design intent, and excessive sturdiness.
2. `72a3b3331598`: restored the single source-aligned continuation and changed shield duration from `轮` to `回合`; retained implementation-accurate radius 10.
3. `747d29c92481`: restored the fiery bringer of doom and “crush your foes” meanings and unified second-person usage.
4. `78452093a6e8`: restored two-tab indentation on all four continuation lines.
5. `7975a16239bd`: corrected the Fire Imp lore's commitment, fused earth, contained magic, desertion/demoralization, and majority/alteration-project meanings.
6. `80f87941078f`: restored one source-aligned line break and two-tab continuation in Voracious Blade.
7. `84ca86e56a3b`: retranslated the whole Mal'Rok history entry sentence by sentence, including causality, hidden cities, weaker returning storms, delicious feast, negotiation, altruistic-god motivation, data point, willing deaths, and self-determined destiny.
8. `880a05d14dd0`: restored the successful-melee-hit condition and all five source-aligned line breaks/two-tab continuations, including the trailing continuation.
9. `89a4d5c92f7b`: restored the quoted Black Crown joke: `“送给应有尽有的恶魔。”`.
10. `8d7b28975599`: removed the target-only line break from Abduction.
11. `8ead58568837`: removed the added flames/truth specificity, restored unlock eligibility and instant Phase Door meaning, and retained all source line breaks/markup.
12. `90ae8f40d2a0`: restored `mottled` in the unidentified Imp Claw name.
13. `9ac85a7a89f1`: restored the missing line break, the verb structure `%s纳鲁精灵`, the loyalty/fate meaning, the overhead bubbles, and removed the added giant-body wording; runtime substitution now reads `背叛纳鲁精灵` / `屠戮纳鲁精灵`.
14. `9d7afbedda50`: replaced the invented obsidian material with black in the unidentified Black Maul name.
15. `9e25a17b1f56`: restored `chaos and death` as `混沌与死亡`.
16. `a6fd631ea297`: restored the two-tab continuation in Eternal Suffering.
17. `aaaaf55ee42b`: restored the “often evil, but a few” contrast in the Demonologist description.
18. `ac2347dac63f`: applied the sole authorized effect rename, `无尽恐惧` → `压倒性恐惧`.
19. `ae8c122720e4`: restored the two-sentence, one-line-break shield enchantment description and source-aligned duration placement.
20. `af918013e6cf`: restored random/up-to teleport semantics, seed provenance, fizzle wording, and the worn-equipment condition.
21. `b281c0e29d35`: restored the requirement to use powers through demon seeds attached to equipment and removed the invented human-learning claim.

## Risks and retained decisions

- Source provenance is an unpinned public Ashes checkout; exact frozen file hashes matched, but no repository commit can be claimed.
- `Fiery Aegis` retains radius 10 because the frozen source implementation hard-codes radius 10 even though its English description says 5.
- `Overwhelming Fear` was changed only at its single authorized occurrence. No terminology file or other proper name was changed.
- Long lore wording remains subject to independent language review; mechanical and source-claim checks passed.
