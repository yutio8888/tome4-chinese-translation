# repair-w40-20260927 implementation

Role: Paseo `EXECUTOR` (sole task-content writer)

Baseline: `0ce668c95ab697649b099246acbdeb354adfcc2e`

## Scope

- Modified only the 23 frozen logical targets in `tome-orcs.lua` plus this authorized evidence directory.
- Did not modify source, source_tag, args_order, section, runtime keys, terminology, `.ai/task`, or unrelated records.
- Did not stage, commit, push, or create an agent.
- Verified the 17 exact Orcs source paths named by `SOURCE-ANCHORS.json`; every current file SHA-256 matched its frozen anchor. The Orcs source repository and commit remain unpinned.

## Per-entry changes

- `1bf82bee09`: restored the quoted sales pitch, “former enemies”, transformation into freshly grown trees, and “faster than ever” force.
- `4d968f8856`: changed Nacrush's reputation from indiscriminate killing to excessive firepower.
- `4e24ac36b0`: restored the source newline and the nearly indecipherable interlocking mechanism.
- `4e560f2e5a`: standardized Steam Quarry as “蒸汽采石场” and removed the source-absent blank line after the title.
- `4e9cf35b9f`: restored the Sher'Tul's mythic nature, rebellion against the old gods, and the narrator's unexplained imperative to stop the resurrection.
- `4f11cda37a`: corrected the two halfling factions as the subject, “filthy” greenskins, the deletion typo, singular addressee, implementation means, and resignation timing.
- `4fd92b3774`: restored the two-TAB continuation prefix in Arcane Disruption Wave.
- `5083f958a`: restored both Steamtech talent-category names and the per-category 100-gold fee.
- `50df66a4c3`: restored “other” and “harmless” in Sook's shop name.
- `52663fb95e`: corrected hunter/hunted agency and removed the source-absent first-sentence line break.
- `52bc32cb74`: restored the three-TAB continuation prefix and replaced the invented gauss cannon with a piercing-bullet turret.
- `5362d5e743`: corrected the recorder check, prior agreement terms, Eye name, chaos wording, tea condition, and journey already underway to the last known position.
- `56a78163e2`: corrected the pathogen injection's patient/agent relation.
- `56f374b8ee`: restored techno-psionics, a single yeti, mind hijacking, and mind transfer.
- `5801838b0a`: restored two steamguns tossed airborne, in-range firing, airborne disarm, agility wording, and all resistances.
- `58c3e2bf11`: restored all three two-TAB continuation prefixes in Corrosive Shell.
- `595abf50af`: restored the Amulet as the light source in the `saySimple` target; the distinct `logPlayer` record was left unchanged as required by the frozen workset.
- `5bb911ddb9`: restored the missing newline and two-TAB prefix before the multi-spiderbot dispatch sentence.
- `5d8d908f72`: restored the standalone salutation paragraph, fallen-example grammar, matter-of-fact contrast, Maj'Eyal spelling, mercifully brief reign, meeting sequence, annual messages, and “least of all ourselves”.
- `602a17b119`: restored the warning that confronting Kaltor is likely very dangerous.
- `612aaa387f`: corrected the inhabitants as living on the peninsula, not an island.
- `619199a9ea`: corrected the helmets to about twice the required weight and standardized Atmos absinthe as “气之部族苦艾酒”.
- `61d7c6c8d1`: restored the helmet subject and contrast in the Steam Powered Helm description.

## Validation outcome

- Manifest-compatible LuaJIT semantic load: PASS; 3904 baseline and 3904 current translations.
- Frozen-diff validation: PASS; exactly 23 logical target changes, all 23 workset revision keys present, zero missing or unscoped changes, and zero non-target field changes.
- Structure validation: PASS for LF count, blank-line indexes, per-line leading TAB depth, terminal newline state, no newly added trailing whitespace, printf/`%%` placeholders, markup, and `@...@` tokens.
- `python3 -B tools/i18n lint --strict`: PASS; 30308 translations, 0 errors, 0 warnings.
- `git diff --check`: PASS; no output.

The first verifier draft rejected a pre-existing terminal space in `4f11cda37a`; the final assertion was correctly narrowed to prohibit newly added trailing whitespace, and the complete comparison then passed.

## Residual risk

- The Orcs DLC source repository and commit are not pinned; validation relies on the frozen per-file SHA-256 anchors, all of which matched.
- Linguistic approval remains the orchestrator's independent REVIEW/FINAL_REVIEW responsibility.
