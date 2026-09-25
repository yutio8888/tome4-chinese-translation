# repair-w28-20260925 implementation

Role: Paseo `EXECUTOR`
Baseline: `43c048659721cdbf79f3f2c83e344ea24e3b86e2`
Content file: `tome-ashes-urhrok.lua`

Only the 24 frozen WORKSET targets were changed. Sources, source tags, argument order,
special values, sections, runtime keys, terminology files, and task records were not changed.

## Per-entry changes

- `2b3e15fe…`: restored the harmless-bauble, viewing-hole, and reversal meaning.
- `2f11be50…`: changed the unidentified breastplate material from “obsidian” to “pitch black”.
- `318a0c4d…`: restored the modified descendants, aggression comparison, and Eyalites' reluctance to stand and fight.
- `368ba81f…`: made `#Target#`'s weapon, rather than the actor, the subject of the threat reduction.
- `37030231…`: restored the dark cults and ranged-attacker details, unified “恶魔种子”/“堕落者”, and matched the source line layout.
- `39754d31…`: restored both binding demons and compelling them to obey.
- `3bd78dce…`: restored both second-level TAB indents, then corrected the implementation semantics: fixed radius 3, knockback distance `%d`, and fire damage including the primary target.
- `3c496fb5…`: changed the plaguefire action from summoning to firing a bolt.
- `3d80f4a5…`: changed the achievement condition from a summoning action to party composition.
- `4130b809…`: restored “towers above” and the nearby Fearscape-area qualifier, using “恶魔空间”.
- `43134b3d…`: restored the scouting-party subject and portals occasionally emitting a fallen shade.
- `435ca9b7…`: restored the second-line TAB only; the implementation-aligned 50%/FIREBURN wording was retained.
- `4dd916e4…`: restored the target's final LF only.
- `54a6a1b0…`: restored the eventual surface arrival and the reason that the player may be stronger later.
- `54ef1fbf…`: restored the second-line TAB only.
- `55bb0228…`: restored “any creature” rather than narrowing the beam path to enemies.
- `55dedd24…`: restored the two player gender macros and corrected “furthermore” and “familiarity”.
- `5666e9d8…`: restored the pillar forest, conventional-birth distinction, adequate performance, sustainable energy input, and mass-production condition.
- `5b6924a7…`: restored the second-line TAB only.
- `5e4738cd…`: corrected peasants, retaliating only when life was threatened, regrowing eyes with more nerve endings, `Mal'Rok`, and “恶魔空间”; the bounded FINAL fixes also restored the hypothetical intent, speaker-owned condemnation, “nearly-equal” qualifier, discourse-marker sense of “well”, the millennia-long time span, `endearing`, “in a moment of desperation”, and `illusions`.
- `614e1524…`: removed the non-source “traitor” addition and restored the indecision question; cycle 7 RE_REVIEW also restored the chuckling/bursting-bubbles action and made Urh'Rok the charging subject under the roar of boiling water.
- `620e36d2…`: restored the source's two-line LF/TAB structure while retaining the implementation-aligned cone wording.
- `64193308…`: restored Rogroth generating seeds from within its own frame; cycle 7 RE_REVIEW also corrected the inspiration, combat chassis, design-test data, and surface-grown invasion-force sentences.
- `69b36890…`: restored the source's three-line LF/TAB structure while retaining the implementation-aligned 4-turn duration.

## Scope and lifecycle

- No agents were created.
- No `.ai/task` file was modified.
- No staging, commit, or push was performed.
- Pre-existing unrelated untracked files were left untouched.

## Residual risk

The Ashes checkout is public but its repository/commit is unpinned. Every referenced file
matched the SHA-256 frozen in `SOURCE-ANCHORS.json`; the source provenance remains unpinned
as specified. Independent review and the host's full gate remain outside this EXECUTOR run.
