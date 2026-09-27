# repair-w41-20260927 implementation

Role: Paseo EXECUTOR (single task-content writer)

## Scope

- Modified only the 22 frozen targets in `tome-orcs.lua`.
- Added this implementation report and `VALIDATION.json` under the SPEC-authorized evidence directory.
- Did not change source, source_tag, args_order, special/runtime keys, terminology data, task records, or unrelated files.
- Did not stage, commit, push, or create an agent.

## Source provenance

All 18 distinct Orcs files named by `SOURCE-ANCHORS.json` were read only at their frozen entry paths. Their SHA-256 values matched the frozen anchors. The locally available public Orcs source repository and commit remain unpinned; no checkout identity is treated as a fixed source version.

## Target changes

1. `64ff1dc48ef2` — Tech Overload: restored the security-override action, maximum-steam basis, steam-regeneration wording, and single flavor-text exclamation mark.
2. `65f41182e7ce` — Crimson Templar John description: restored the counterfactual respect, present hatred, emitted crimson light, and measured approach.
3. `67521c21a4c0` — Kaltor poster: restored the three-line opening and all source line breaks; corrected the bargain, counterfactual life-saving claim, decade-old production run, and public/charity referents.
4. `67f8f7d70315` — Radiant Horrorc: changed the achievement name to `光芒恐兽人`, preserving the radiant-horror/orc wordplay.
5. `6970e251f399` — telepathic message (3): corrected the adding-machine fate, `西方天灾`, Mal'Rokka causality, `大腐化者`, Demons/Master conjunction and title, prognostication condition, and countability claim; aligned frozen proper names.
6. `6ce8f3f6efa7` — Technomancer description: changed “精通” to “涉猎”, made the subject consistent, retained `元素法师`, and restored the missing paragraph break.
7. `6cf4f05c091b` — John’s letter to Trelle: restored the hypothetical concession, treaty-help meaning, addressee as the knowing wrongdoer, `technically`, and the final expression of disappointment.
8. `6dd4ec5d148e` — Saw Wheels description: restored steamsaws as propulsion, the separate break/cancel sentence, cancel behavior, movement scaling, and flavor text.
9. `70349db4017e` — Explosive Shell: restored the steamgun shot, per-shot target, ammunition explanation, punctuation, and two-tab continuation lines.
10. `71325aa1fba9` — Spinal Break: restored “up to”, “at least 3”, and the preferred `全局速度` mechanism term.
11. `72ac5778415f` — telepathic message (2): restored permission to live, removed the added contrast, changed singular narrator voice, and corrected Amakthel’s “pet project”.
12. `7305b0ef493f` — Pressurizer unidentified name: restored the cloak’s lining/hidden layer.
13. `741a80cfd4c4` — Reclaiming Garkul’s Heritage: restored the reclaiming action in the achievement name.
14. `7531d7a107f4` — Dominion Port ???: normalized all three question marks to ASCII while retaining `巨魔帝国港口`.
15. `75736fcf0dcf` — Signal description: restored the barrel’s large size.
16. `75aa2a58ee28` — Shockstaff: unified `电击棒`, restored frontal-arc enemies and attack semantics, and retained empty lines without adding line-end tabs.
17. `778c749fb25e` — slaver’s inquiry: corrected `马基·埃亚尔`, dispersal/convergence, both `反侦测枢纽` references, customer/actor roles, and the near-zero-profit statement.
18. `7a0daea12b44` — Twilit Echoes: changed the cap condition from single-hit to cumulative light damage.
19. `7aefb42eba5e` — dialogue option: changed the request to learning `插件制作`, without inventing a gendered teacher referent.
20. `7b2d6ea1732b` — Trelle journal page: retranslated sentence by sentence, including scouts, simultaneous mistaken identities, delayed notification, official policy, hypothetical covert action, italic emphasis, Atmos blame, and the uncontested territorial claim; retained `太阳堡垒`.
21. `7c3140c3eb27` — Incendiary Shell: restored two leading tabs on target continuation lines 2–4 without changing wording.
22. `7cbc8bea3178` — Uncertainty Principle: restored spatial quantum-state distortion and replacement of an incoming hit by adjacent relocation.

## Residual risk

- Orcs source provenance is public but repository/commit-unpinned, exactly as recorded by the frozen anchors.
- This EXECUTOR run performs implementation and bounded validation only. Independent REVIEW/FINAL_REVIEW, full production gates, task-state closure, commit, and push remain host responsibilities.
- Pending naming decisions listed by SPEC (including Sunwall naming) were not changed.

## Plan deviation

None. A diagnostic version of the bounded checker initially treated prose `100% sure` as a printf token and treated a baseline-preserved final space as newly introduced whitespace. The final check reused the repository format-token policy for formatting source tags and verified that no line-end whitespace was added.
