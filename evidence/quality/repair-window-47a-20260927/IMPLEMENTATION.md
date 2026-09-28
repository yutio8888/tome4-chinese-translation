# repair-w47a-20260927 implementation

## Scope

- Modified exactly the 77 frozen translation targets: 46 in `mod-tome.lua`, 14 in `tome-ashes-urhrok.lua`, 1 in `tome-cults.lua`, and 16 in `tome-orcs.lua`.
- Modified only the SPEC-listed rows in `terminology/places.tsv`, `terminology/narrative.tsv`, `terminology/combat.tsv`, `terminology/creatures.tsv`, `terminology/talents.tsv`, and `terminology/items.tsv`.
- Preserved every translation source, source tag, argument order, special field, section, and all non-workset records.
- Preserved placeholder and markup token order and target LF/TAB counts for all 77 changed targets. No sentence-wide rewriting was performed outside the explicit pocket-time exception and the two additional sentence-level SOURCE-CLAIMS.
- Did not modify `.ai/task`, rules, tools, source code, or unrelated working-tree files. Did not stage, commit, push, or create an agent.

## Target changes

Keys below use unique 12-character prefixes.

- Numbing → “麻木” (25): `023ddaba771a`, `042f12de2757`, `152430348087`, `281346a1b7f8`, `28eb346c541b`, `28fe038d3b44`, `33e93322177c`, `398be454986e`, `4712cd9769ca`, `559980ea23c0`, `6da132f16a77`, `6df61a3ff972`, `79b6b06db518`, `82557081f5a9`, `871e1e25e061`, `91957e5f6df2`, `a1e95a2f4c1f`, `a26c7984d71f`, `b0febb8c6a2c`, `c1154b299ada`, `cb91dbb3e5d9`, `d2195ec38412`, `e540acef669a`, `f4807dcf9fdf`, `fd635c58e3bd`. Only numbing/numbed-aligned “麻痹” occurrences changed. The `a1e95a2f4c1f` target also changed “中毒几率在可能的毒素效果中平分。” to “各种可能的效果出现几率相同。” as explicitly claimed.
- Bare Eyal → “埃亚尔” (24): `16384320dfa6`, `31f87052433c`, `333d86a684f6`, `50fda5e279cd`, `52df9c480a9e`, `758dd3c2cd3a`, `76bb8e6e11ea`, `7f78c61479de`, `7fc7dac84ef9`, `80b99dd4dc78`, `85af2f1f5d30`, `85f56b381434`, `9b3c864b62bf`, `a0dab4d481f5`, `aa1834b83d32`, `c297480c281e`, `cacc45e5378d`, `ce428a8c9b51`, `cf17c8f6392c`, `cf4952bb7a80`, `e46519c32503`, `eb3aefa7d5f6`, `f5f092ac5dda`, `f684bba9951a`. Maj'Eyal and Var'Eyal references were retained; in particular, the Maj'Eyal occurrence in `7fc7dac84ef9` remains “马基·埃亚尔大陆”.
- Sunwall → “太阳堡垒” (5): `056346a0e269`, `252173d44fad`, `69c4df21cd81`, `6b539b16f261`, `c4abe2a925e1`. The explicit bastion sentence is now “摧毁太阳堡垒的要塞”; `c4abe2a925e1` also changes Var'Eyal from “瓦尔·埃亚尔” to “瓦·埃亚尔”.
- Ureslak → “乌瑞斯拉克” (9): `1916a8f0c542`, `21fea59fe6d5`, `2d656a94136a`, `4b91b1fbacc1`, `7b2da7e9a337`, `8963334cf43c`, `ab69e8c5ca0a`, `b158ca974ea1`, `fcfbb15427db`.
- Crimson Templar → “血色圣殿骑士” (6): `1ad20269f425`, `4ed2ab828aeb`, `b2a054270034`, `b6e17ee9e443`, `b86428fc6d35`, `f181f499b62e`.
- Gardanion full artifact name (1): `40cf688195f6` → “加尔达尼恩，神之光辉”.
- DESTRUCTICUS full name (6): `5e87535a9d3c`, `79d675f5e1b7`, `e50ac04aa0d4`, `f06518715f0c`, `f398f02999c3`, `f79246dcbe30` → “毁灭号，无礼的天空穿透者”; the interrupted council occurrence is “毁灭号，无礼的天空————”. Short-name “毁灭号” occurrences outside the full-name source were not changed.
- Pocket-time exception (1): `3724ff928412` now reads “在他的巢穴里把他扔来扔去，他晕头转向，踩在了————” and restores “七彩巨龙”. The exact Orcs checkout file SHA-256 remains `a5f2acd61ec4a5ac80bdd6ae7481d6ec55d8973e496a273e19a922ed7f2782ab`; the source repository/commit remains unpinned.

## Terminology changes

1. Added `Eyal` → `埃亚尔` in `places.tsv`.
2. Promoted `sunwall` to `preferred` and replaced its notes in `narrative.tsv`.
3. Added `numbing` → `麻木` and `paralyzed` → `麻痹` in `combat.tsv`.
4. Added the SPEC-provided notes to `manaburn arcane` without changing its target.
5. Replaced only the notes for `multi-hued`; its target remains `多彩`.
6. Added `Ureslak` → `乌瑞斯拉克` in `creatures.tsv`.
7. Added `Crimson Templar` → `血色圣殿骑士` in `talents.tsv`.
8. Added the Gardanion and DESTRUCTICUS full names in `items.tsv`.

All rows retain the eight-field TAB-separated order. The terminology loader read 729 rows, and all eight new/promoted normative rows matched the SPEC's source, target, category, domain, source tag, status, and scope.

## Validation and unresolved advisories

- Manifest-compatible LuaJIT loaded the four current files and their HEAD preimages. Record counts were unchanged; exactly 77 workset records had target-only changes, with zero non-workset or non-target-field changes.
- `python3 -B tools/i18n lint --strict`: pass, 30,308 translations, 0 errors and 0 warnings.
- `python3 -B tools/audit_static.py`: pass (`ok=true`, 0 blocking findings); 17 advisories remain, including the SPEC-mandated Gardanion item category boundary advisory.
- `python3 -B tools/audit_dynamic.py`: pass; the two preferred mismatches are unrelated existing rows (`Air`, `draining physical`). The new exact mechanism/name rows that have no standalone runtime key are reported as unused advisories where applicable.
- `git diff --check`: pass.
- Supplemental `python3 -B tools/annotate_domains.py` exited 1 after writing its report: its inference table cannot map the two new item proper names, and it advises `Ureslak` as `society` rather than the SPEC-mandated `creatures` domain. Fixing the inference tool is outside the allowed files, so no tool or category change was made. The declared TSV domains and categories remain exactly as required by the SPEC.
- Independent review and the host's 17-item gate remain host responsibilities.
