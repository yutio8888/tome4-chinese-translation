# repair-w30-20260925 implementation

## Scope

- Modified only the 23 frozen translation targets in `tome-ashes-urhrok.lua` and this task's implementation evidence.
- Preserved every source, source tag, section, args order, special value, runtime key, and all records outside the frozen workset.
- Did not modify terminology, pending proper names, task records, or unrelated untracked files. Did not stage, commit, push, or create an agent.
- All 12 public Ashes source files matched the SHA-256 values frozen in `SOURCE-ANCHORS.json`. The Ashes repository and commit remain unpinned.

## Per-entry changes

1. `ba84fb707016f47d9bff23b4838b1fb1d12c4233c369db21f28cdef2509fe949`: repaired the Draebor lore sentence by translating the mass-producible artifact as a mass-producible magical creation and the portal work as reverse engineering; also corrected arrival wording and paired punctuation.
2. `bade8870357b885b3eb441349fa0f7a00831fc6e831a8d8d31a8b9a0268d6ef4`: restored teleportation to Mal'Rok and corrected “作为”.
3. `bc6203b66b5f56bbc28c1834d803b1b7538831416d05cb536a574b2877428fc1`: aligned the lore title to “玛·洛克的历史（误译）”.
4. `bce9bc97c2ad35db7b4227c632fe25671f0b0bde9a1beee476a1dab2eaceabdf`: repaired the full demonologist briefing, including conditional capability, fireball/acid-burst wording, neutral power attribution, energy/shield meaning, teleport pattern, and the three approved pronoun-function substitutions.
5. `bfd436bc1b4938003fcbf546411e9745c0470e363808c1a927abc8270e7977b4`: removed the duplicated range wording while retaining the implementation-backed fixed-4-tile note.
6. `c254cf06e2185f14bd3d84fccda22b1f04e7f3f18992fe585e33a7c6296eecb1`: restored the flames' deliberate search for more fuel.
7. `c6e8c8e40ebf4cc6b84ef26c2cd2fdc567a15be8d7713943fb8c85371886924b`: clarified that the target's own damage dealt is increased.
8. `cdac06c97945087b597d5db73e5dd09e220ff8e15e1dd6f2818f056edb37a40a`: restored the naming joke and the massive sword's power in the Dethblyd description.
9. `ce3b54895d49edbdf483d73d8901a370ad0c2e32121ab624a1863edd3fc77c8d`: repaired the full Lost Memories passage: wretchling identity, face-clinging action, both healing instructions, missed eyes, subpar damage, screaming instruction, torn skin, bubbling skin, and the handler's healing spell.
10. `d3c0b76c51ea9a2d4e205eea79d505dacdbee9d022539c42f888731f50ad7d31`: restored both continuation lines to two TABs.
11. `d3db2e0afe622cb0b7334175689de0ee7503a30077262683d6fc67ec219803b3`: restored the quoted Black Plate text about wreckage around the viewer and what remains inside.
12. `dac57e56ba34a2eab7c2d776820329f1c6b1c68f55a99aa7a2a3808158734466`: repaired the full battle note: neutral target wording, isolation, blown connectors, detached platform, jerked pen, double-bladed katana, giant construct label, and interrupted writing.
13. `de010befadb30a314e41c3d011d9d48ac526781bba885795e92f3116e238270b`: added the in-sight target scope while retaining “火球” to match the established Flame Bolts talent name.
14. `de5854b6490f22ca119ce6a4f91a2233f264350f6c36731cdb8172e7e08c8f22`: repaired the complete quasit lore, including the three child names, Eyal front line, arsenal research, constructs, bolted-on armor, machine-like nature, reinforced muscles, retained minds, eagerness, discipline, and combat ability.
15. `df5ab191262015cda6abdc60ab9de3f096eefe794b85bc2fc67509a4e5998a70`: restored the continuation line to three TABs.
16. `e6985dcdeca1588eefe0bcbc083c6736bc39dd7c6b60f1e6d9e38fab14d8074a`: repaired the complete Forge-Giant lore, including the “infinite” exception, unavailable effort, granted hammers, energy efficiency, hammer-forging process, usable equipment, extreme strength, and emergency deployment.
17. `e781f9306f0e88ecd58067161dd9caa7a69bd4bebd85b2e718dbc3c7e696e09a`: repaired the complete Lithfengel lore, including the intact portal, reaching Eyal, prospective travelers, and his refusal to risk other subjects.
18. `ea1d8fcb0b64e634030eb0c5fe37dbc85d0f8399d01079b3d2601a3b6ac52a17`: restored the seed's attempt/chance semantics, unique-demon restriction, “always try” qualification, daze spacing, and exact blank-line TAB structure. The target uses Lua string concatenation solely to produce runtime `LF + TAB TAB + LF` without physical trailing whitespace.
19. `eb38d586e7308527eab2644743dd5081bbedbf1c593abb263f93973f0eca7d60`: corrected the unidentified item to flames shaped like a cloak.
20. `ebb709fd1b3014abfabf6738e5d1500f4612372b4e5d70d76643ee768b573bf0`: restored the continuation line to two TABs.
21. `ee89209326cf70a26b2e5b60089e53eaae69122e9da291ef178c8ce86347f272`: restored Urh'Rok's name in the shield-energy description.
22. `f13d578c105ef5a5aa4d9da0fc47128ae6b87b21ba0ac7c6f19be7dc8e4d31e6`: restored the quoted Black Maul description without the unsupported added idiom.
23. `f3b3b2e5abdbf359607b1ac31ece00f9f57185a847dc519da400c1410b10ec12`: restored the target to the source's four-line structure and kept the delayed-damage increase in its source sentence.

## Risks and handoff

- Source provenance risk remains: the Ashes checkout's repository and commit are not pinned. This implementation relied on the frozen per-file SHA-256 anchors, all of which matched.
- The long narrative rewrites require the contract's independent REVIEW/full and FINAL_REVIEW/full; no unresolved mechanical invariant remains in the executor result.
- Final `tome-ashes-urhrok.lua` SHA-256: `bc45e766a74e1a960670404b76553eab761ba4078be47b995e882f7ef08a99b9`.
