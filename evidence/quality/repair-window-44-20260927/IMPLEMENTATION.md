# repair-w44-20260927 implementation

- Role: Paseo `EXECUTOR`
- Completed: `2026-09-27T10:50:24Z`
- Baseline commit: `4231a5c38dbd9cfc009c997cb097f008692e05ab`
- Content file: `tome-orcs.lua`
- Frozen workset: 24 entries from batches 343–348
- Source provenance: public Orcs DLC checkout under the frozen `SOURCE-ANCHORS.json` root; all 21 referenced file SHA-256 values matched. The repository and source commit remain unpinned.

## Implemented changes

1. `ba3d263f1b03…`: renamed Lingering Cloud from “厚重云雾” to “滞留云雾”, matching the five-turn vapour-linger mechanic.
2. `bc838cd6cd3d…`: restored Psyshot's blank line and per-line TAB depth; corrected the offhand pure-mindstar condition, kinetic projection, psiblade exclusion, and active-shot sentence.
3. `c000e44be506…`: restored the three-line closing-sale heading and both paragraph breaks; retranslated the notice, including over twenty years, entrusting safety to the Guard, proper disarming, and “if nothing else”.
4. `c13869e9eb19…`: removed the invented player ownership of automation discoveries and translated the armour's intrinsic protection mechanisms.
5. `c1d81b80fa5c…`: restored all eight paragraph blank lines and corrected the Kruk history's contempt, blame, mountaintop, Atmos, pipe/hose, and battle wording; used “克拉克半岛”.
6. `c299fd5842d1…`: used “克拉克半岛” and “西方天灾”; restored the unseen condition and the person's agency.
7. `c307e5b14900…`: restored the attack yeti's long-trained anger and corrected “地”.
8. `c37dbbf403c2…`: restored the two leading TABs on the second Viral Needlegun line only.
9. `c43a6a0caade…`: corrected the farportal as one leaving the continent and `tinies` as the giants' “小不点”.
10. `c5ae4cd6edb0…`: restored the four-line Bloodstar layout; kept the healing reduction parenthetical on its source line; restored embedded shrapnel and unified “金属灵晶”; treated the displayed `%d` as the already-doubled range.
11. `c8bb77ca52d4…`: corrected hallway, slightly teal-tinged light, spike series, and the repeated reassurance/telepathy wording.
12. `c9d0e0bae7a9…`: restored tinker-crafting output, mandatory destroy-time choice, no-items default selection, generic metal lumps, and herbs.
13. `d01ecec1c2da…`: retranslated the four paragraphs with the original qualifications (`possible`, `lesser`, `maybe`, `yet`, `some`), the lone megalomaniac, and `do not condone`; restored the terminal LF.
14. `d270e6e378bc…`: corrected the leaf-bound journal and Menders account, including otherwise-lacking support, the old guard being overrun, “our techniques”, and rogue mages; removed the added `[b]` pair while preserving both source `[i]` pairs.
15. `d2f78524c5a1…`: corrected who meant no harm, the desire to forgive, and the unembellished lost lives.
16. `d499e0ed13d3…`: restored the full Steam Powered Boots joke.
17. `d4e2ee9c3cb6…`: restored `somehow` and the falling steamguns in the paired effect log.
18. `d5c5e8c307e1…`: merged No Hope back to one line.
19. `d6139c786c24…`: restored sensing beyond sight even through walls.
20. `d789f21728ba…`: restored `most` of the forces being outside.
21. `d7cb7c69a53f…`: replaced the unsafe single `%` with wording using “一半”, retaining `%d%%` and the implementation-backed mechanics.
22. `d8abd0fc7560…`: restored two leading TABs on Voltaic Bolt's second line only; kept the existing “闪电球” name.
23. `dc6704a553d5…`: restored the missing paragraph break and corrected the Fire Imp as flying near no important target.
24. `dcb810596c1a…`: restored the blank line after the constituents heading.

## FINAL_REVIEW cycle-0 fix

- `c000e44be506…`: replaced the two product references with the repository entity names “精良的自动装填式兽人驱逐装置” and “压力强化型防斩击作战服”; retained “小小大惊喜”.
- `c1d81b80fa5c…`: changed only the final sentence to “我们不会怀念他们那娇气怯懦的无知和浮夸的自以为是。”.
- `c43a6a0caade…`: changed only the three sound terms to “闷哼声，挤压声，劈砍声”, retaining the following punctuation.
- LuaJIT HEAD/worktree semantic comparison still reports exactly 24 changed WORKSET targets and zero non-target field changes; strict lint and `git diff --check` pass.

## Scope and residual risk

- No source, source tag, args order, special field, runtime key, terminology file, rule/tool file, or task record changed.
- Pending naming decisions for Thunder Grenade, Voltaic Bolt, Supercharge Bullets, Awesome Toss, Gardanion, and Sunwall remain untouched.
- Orcs source repository/commit identity is not pinned; validation proves the local anchor files matched the frozen SHA-256 values, not a repository commit.
- Per SPEC, the EXECUTOR ran bounded validation only. Independent review, the 17-item final gate, commit, and push remain host responsibilities.
- No file was staged, committed, or pushed; no agent was created.
