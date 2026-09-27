# repair-w39-20260926 implementation

Role: Paseo `EXECUTOR` (sole task-content writer)

Baseline: `5454fc6f6b1bb67b3ef35baba2a3c618d61a9308`

## Scope

- Modified only the 27 frozen targets in `tome-orcs.lua` plus this authorized evidence directory.
- Did not modify source, source_tag, args_order, section, runtime keys, terminology, `.ai/task`, or unrelated records.
- Did not stage, commit, push, or create an agent.
- Verified all 22 exact Orcs source paths named by `SOURCE-ANCHORS.json`; every current file SHA-256 matched its frozen anchor. The Orcs repository/commit remains unpinned.

## Per-entry changes

- `38df4d785d`: narrowed Destructicus's guarantee to entities directly hit/detonated against.
- `38e3195b27`: restored “southern” in the Dominion port objective.
- `393ceabce5`: restored the brief lapse, personal request/last thoughts, eventual Mana Caves retaking, and Kruk rebellion details.
- `3a43293d14`: restored Smithing's three continuation lines, level-1 schematic sentence, and “unless all are known”.
- `3bb826649c`: corrected the Amakthel prayer's gods/form/supreme-deity sentence and typo.
- `3c68b52ee2`: restored Rocket Boots' trail of fire.
- `3ea7432fdc`: restored steam pressure, serrated blade, and high-speed rotation; removed the redundant added damage claim.
- `3f615510ad`: changed “automation” to automatons, rendered “why” as an exclamation, and restored the terminal newline.
- `3f7dc08a62`: changed “your Pride” scope to all Orc Prides.
- `3fbaffc6c4`: restored the Hand Cannon continuation TAB line and ranged-melee/ranged-proc distinction.
- `431cacf5c7`: aligned the poster's title spacing, restored “over 40%” and “up to four years”, and removed the unsupported production claim for declogging tonics.
- `433071ee0f`: restored four `\t\t` continuation prefixes in Grasping Moss.
- `43cbe69c78`: restored the quoted Turbocutter sales line and trailing ellipsis.
- `43d64e16d`: restored window versus scrying-panel viewpoints, Var'Eyal, and source paragraph structure; removed the added crowding detail.
- `43d8bb19bc`: named the flying grapple drone, restored homing behavior and target-self collision, and merged the source-matching line.
- `44947e3a4c`: restored the guard-taunt meaning about cleaning blood from gears.
- `461ab2185c`: reduced all five advanced-grenade continuation prefixes from two TABs to one.
- `46b5e759b`: restored cone-shaped repair energy, “other” mechanical creatures, and the `\t\t` continuation prefix.
- `4712cc5e45`: restored the “safe for now” limitation.
- `482a7a631d`: restored the shaving/ruined-follicles joke without added escalation.
- `4831df6575`: repaired the arrival timing, universe-forgetting sentence, lift/drag contrast, and roughly arranged fragments.
- `49c7875073`: removed source-absent `[b]...[/b]` markup from `VOTE FISTICUFFS`.
- `49cf2e17cf`: renamed only this `Ramroller` entry from “剃刀平台” to “碾压战车”.
- `4a4f53d70c`: restored five-color explosion, barren mountaintop, targeting-view switch, mercy reaction, celebratory audience, scrying-panel term, and source paragraph structure.
- `4bc761fa2d`: changed destroyed “records” to the many destroyed depictions.
- `4cad070d1e`: unified Marshall of the City Guard as “城市卫兵队长”, corrected ill temper, spiritual consciousness/figurines, and the `unlikely` limitation.
- `4d3cfeb531`: restored John being bound forever and summonable at will for a few turns.

## Validation outcome

- LuaJIT semantic load: PASS (`Lua 5.1`, `LuaJIT 2.1.0-beta3`), 3904 baseline and 3904 current translations.
- Frozen-diff validation: PASS, exactly 27 changed targets; all 27 workset revision keys present; no missing or unscoped changes; zero non-target field changes.
- Per-entry structure validation: PASS for newline count, terminal newline, blank-line indexes, leading TAB count by line, and line-positioned `#...#` markup, `@...@` tokens, `[b]/[i]` markup, and applicable printf tokens.
- `python3 -B tools/i18n lint --strict`: PASS, 30308 translations, 0 errors, 0 warnings.
- `git diff --check`: PASS.

The first strict-lint attempt exposed an incomplete `[=[ ... ]=]` target delimiter after removing the source-absent bold markup. The delimiter was corrected immediately; the final strict lint and all subsequent checks pass.

## Residual risk

- Orcs DLC source repository and commit are not pinned; this implementation relies on the frozen per-file SHA-256 anchors, all of which matched.
- Linguistic review remains the orchestrator's independent REVIEW/FINAL_REVIEW responsibility.
