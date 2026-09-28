# repair-w47b-20260928 implementation

## Scope

- Modified exactly the 56 frozen translation targets: 19 in `mod-tome.lua`, 17 in `tome-ashes-urhrok.lua`, and 20 in `tome-orcs.lua`.
- Applied only the phrases or sentences named by `SOURCE-CLAIMS.json`; repeated old names inside the same target were all changed, with no other rewriting.
- Preserved every source, source tag, argument order, special field, section, runtime key, placeholder/markup sequence, and target LF/TAB structure. No terminology file was changed.
- Did not modify `.ai/task`, rules, tools, old evidence, or unrelated working-tree files. Did not stage, commit, push, or create an agent.

## Target changes

Keys below use unique 12-character prefixes.

- Death descriptions (2): `f6cc31f278f8` → “被剧毒枯萎折磨得虚弱不堪”; `f009c2b19b56` → “被祖父悖论抹去”.
- Damage name (1): `123925877bf9`, “物品黑暗麻木” → “物品暗影麻木”.
- Fire Imp (6): `1e8feab62d47`, `e13a60d3f0e4`, `bd0554dcaedb`, `ffd70790b79a`, `39a08268fdec`, `abe3b2a5577a`; every named “火魔婴” occurrence became “火焰小鬼”, including all three occurrences in `ffd70790b79a`.
- Crystal Shard (1): `eb71935d6c74`, “水晶之杖” → “碎晶”.
- Undead hunter guide (3): `ce71cfc8faa2`, `20d3ae5730a4`, `51f734f82eba`; the named guide wording became “亡灵猎手指南”.
- Dust to Dust lore title (1): `1b52d593ad36`, “土归土” → “尘归尘”.
- Artifact names (2): `ff891672cbe4`, “死灵权杖” → “大巫妖权杖”; `f1403b3e60a7`, “放逐” → “放逐者”.
- Dragon lore sentence (1): `6322a36dca31`; changed only the three claimed fragments to “一般人也许会嘲笑将龙归为智慧种族的想法”, “令人难以置信”, and “最精明和富有智慧”.
- Lore title and chronomancy sentence (2): `eb6bf55a9134` → “若我死于醒来之前”; `474d73f5c99e` received the exact claimed reset/foreknowledge sentence.
- Virulent Strike (2): `f09f7b5baf80`, `9cc12a9996a9`; “撕裂” → “恶疫打击” in the talent name and its use-condition log.
- Matter is Energy (1): `ea75bd367336`, “宝石能量” → “物能转化”.
- Blunt Thrust (2): `eab2ffb63224`, `e98dfa62b625`; talent name → “法杖突刺”, and the info opening → “以法杖击打目标，造成 %d%% 近程伤害”.
- Shasshhiy'Kaish statue (1): `9169ef3a2bbe`, “莎西凯希” → “莎西·凯希”.
- Armoured Leviathan (4): `df20e157440a`, `676590b08fdf`, `0c451e854a29`, `fb23faa260fe`; name/effect/log forms changed from “重装上阵” to “铁甲利维坦”.
- Corruption of the Doomed (4): `958319eb5e74`, `fc9cbd524311`, `bee297d9160b`, `1dafd3a72823`; name/effect/log forms changed from “腐化形态” to “末日腐化”.
- Osmosis Regeneration (3): `b3497840432c`, `3747432e7d1b`, `dcfd031f9352`; effect/log forms changed from “渗透吸收” to “渗透回复”.
- Soft-foot (3): `acf4d1b0e902`, `b7abfa6898a5`, `deea5de8301a`; “软蹄者/软蹄族” became “软脚者/软脚族”, including all three occurrences in `deea5de8301a`.
- Thunder Grenade (3): `58592ec9fcb3`, `711ee7a6226f`, `19137076a943`; “闪电榴弹” → “雷鸣榴弹”.
- The Lumberator (1): `c8a0b6d86f40`, “播种机” → “伐木机”.
- Supercharge Bullets (3): `36ece3ede88b`, `9d032cc60dc9`, `4b493bbbd0bc`; the named “超速” forms became “增压”.
- Awesome Toss (3): `b85fbbe5e3f5`, `d06dfea85a58`, `5e7cd06b60fb`; “致命翻转” → “华丽抛枪”.
- Create Tinker (2): `3c56f9eac2a2` → “制造蒸汽工具”; `e9f4b2bd8518` → “允许你制造蒸汽工具。”.
- Voltaic Bolt (2): `219d179f63f1` → “伏特电箭”; `1fbc26a864f8` received the exact claimed “发射一枚闪电箭” opening.
- Electricity (3): `da3a33562bb8`, `7fd021e75118`, `9af7773a4c3d`; the named talent, tinker description, and class-description occurrence changed from “电子” to “电力”.

## Source and exclusions

- All 56 frozen source-anchor queries were used. The 19 core queries cite fixed ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; the 37 DLC queries remain explicitly repository/commit-unpinned.
- Recomputed SHA-256 for all 16 unique DLC files, using only the two checkouts and exact paths named in `SOURCE-ANCHORS.json`; all matched their frozen hashes.
- Confirmed unchanged exclusions: `Electron Incantation` remains “电子咒式” in both entries; `Osmosis Shield` remains “渗透护盾”; the talent-name entry `Dust to Dust` remains “土归土”.

## Validation and unresolved observations

- Manifest-compatible LuaJIT loaded the three current files and their frozen preimages. Record counts were unchanged (22,989 / 900 / 4,202); exactly 56 workset records had target-only changes, with zero non-workset or non-target-field changes.
- `python3 -B tools/i18n lint --strict`: pass, 30,308 translations, 0 errors and 0 warnings.
- `git diff --check`: pass.
- No additional translation doubts were discovered during this directed window. The expected `doctor` and source-evidence advisory remains that the public Ashes and Orcs repositories/commits are unpinned; their frozen per-file hashes matched.
- Independent review and the host's full gate remain host responsibilities.

## Cycle 1 confirmed-finding repair

- Repaired only the two status=confirmed findings from
  .ai/task/repair-w47b-20260928/ADJUDICATION-F0.json; the other 54 workset
  targets and all non-target fields remain unchanged.
- 9af7773a4c3d: in the Technomancer class description, changed
  “奥术发电机插件配方” to “奥术发电机蒸汽工具配方”,
  “蒸汽/物理系” to “蒸汽科技/物理系”, and “蒸汽/化学系” to
  “蒸汽科技/化学系”. The earlier cycle-0 change “机械和电子技能” to
  “机械和电力技能” remains intact.
- b7abfa6898a5: replaced the target with
  “我们其他人都已逃走，藏身在半岛各处的洞穴里……凭良心说，我不能为了我们，要求你在他的魔法面前直面必死的命运；但抢先出手或许是拯救你族人的唯一办法。他似乎在拖延入侵，为你争取了一些时间，但如果你不能在他最终发起进攻之前打他个措手不及……软脚者，我曾亲眼看见他的力量像穿过一片树叶一样洞穿山脉。面对那种魔法，不可能取胜。快跑，躲起来，祈祷他遭遇意外，或者失去仍让他能够施法的最后一丝理智吧。”
- The two exact Orcs source files were read only from the frozen
  SOURCE-ANCHORS.json checkout and matched their frozen SHA-256 values:
  f66debe2fe113ec88810ebaabc9a1c5674085445bc25a84a4f6175623ebd527b
  and
  3fc7895e851e1a3dd1ca6941387ddf9dbfa7cd9a5a532346e9f2431100ff9300.
- Manifest-compatible LuaJIT loading of all three translation files passed:
  22,989 / 900 / 4,202 records; exactly 56 target-only changes against the
  SCOPE baseline, exactly two changes against the cycle-1 preimage, and all
  other 54 workset targets unchanged. LF/TAB, placeholder, markup, source,
  source_tag, args_order, special, section, and runtime-key invariants passed.
- python3 -B tools/i18n lint --strict: pass, 30,308 translations,
  0 errors and 0 warnings.
- git diff --check: pass. No terminology file, .ai/task file, or unrelated
  working-tree file was modified; nothing was staged, committed, or pushed,
  and no agent was created.

## Cycle 2 confirmed-finding repair

- Repaired only the two `status=confirmed` findings from
  `.ai/task/repair-w47b-20260928/ADJUDICATION-R1.json`; the other 54 workset
  targets and all non-target fields remain unchanged.
- `acf4d1b0e902`: “所有阻挡他的人，都在他的独角射线下化为灰烬。” →
  “所有阻挡他的人，都在他的独角射线下连灰烬都没剩下。”
- `deea5de8301a`: “在多年的迫害中” → “在漫长岁月的迫害中”；
  “这种力量让我们的身体充满活力，返老还童” →
  “这种力量让我们始终精神焕发”。后文“并不是恢复的力量”未改。
- The two exact Orcs source files were read only from the frozen
  `SOURCE-ANCHORS.json` checkout and matched their frozen SHA-256 values:
  `3fc7895e851e1a3dd1ca6941387ddf9dbfa7cd9a5a532346e9f2431100ff9300`
  and `e0123bf37358aaa4a5dcbded131aca403bf8383501c606e2d3259670fcd2a8db`.
  The DLC repository/commit remains unpinned.
- Manifest-compatible LuaJIT loading of all three translation files passed:
  22,989 / 900 / 4,202 records; exactly 56 target-only changes against the
  SCOPE baseline, exactly two changes against the cycle-2 preimage
  (`HOST-EXACT-DIFF-POST-FIX1.json`), and all other 54 workset targets
  unchanged. LF/TAB, placeholder, markup, source, source_tag, args_order,
  special, section, and runtime-key invariants passed.
- `python3 -B tools/i18n lint --strict`: pass, 30,308 translations,
  0 errors and 0 warnings.
- `git diff --check`: pass. No terminology file, `.ai/task` file, or unrelated
  working-tree file was modified; nothing was staged, committed, or pushed,
  and no agent was created.

## Cycle 4 confirmed-finding repair

- Repaired only the single `status=confirmed` finding from
  `.ai/task/repair-w47b-20260928/ADJUDICATION-R3.json`; the other 55 workset
  targets and all non-target fields remain unchanged. The refuted finding was
  not changed.
- `acf4d1b0e902`: kept the opening and final sentences unchanged. Replaced the
  middle account with “所有阻挡他的人，都在他的独角射线下连灰烬都没剩下；那道射线向上贯穿了他头顶的岩层，一直打通到我们能看见天空。他让我们中的一些人相信，他能用这股可怕的力量征服埃亚尔，又恐吓其余族人随他同行。”
- Read only the exact Orcs source file from the frozen
  `SOURCE-ANCHORS.json` checkout/path. Its SHA-256 matched the frozen anchor
  `3fc7895e851e1a3dd1ca6941387ddf9dbfa7cd9a5a532346e9f2431100ff9300`.
  The Orcs repository/commit remains unpinned.
- Manifest-compatible LuaJIT loading of all three translation files passed:
  22,989 / 900 / 4,202 records; exactly 56 target-only changes against the
  SCOPE baseline and exactly one semantic target change against
  `HOST-EXACT-DIFF-POST-FIX3.json`. The other 55 workset targets, all
  non-target fields, LF/TAB structure, placeholder/markup sequence, and
  runtime keys remain unchanged.
- `python3 -B tools/i18n lint --strict`: pass, 30,308 translations,
  0 errors and 0 warnings.
- `git diff --check`: pass. No terminology file, `.ai/task` file, or unrelated
  working-tree file was modified; nothing was staged, committed, or pushed,
  and no agent was created.

## Cycle 3 confirmed-finding repair

- Repaired only the two `status=confirmed` findings from
  `.ai/task/repair-w47b-20260928/ADJUDICATION-F2.json`; the other 54 workset
  targets and all non-target fields remain unchanged.
- `51f734f82eba`: “#{italic}#一名亡灵猎手的指南 作者：阿斯拉伯·波利斯#{normal}#” →
  “#{italic}#亡灵猎手指南，作者：阿斯拉伯·波利斯#{normal}#”. Markup is unchanged.
- `d06dfea85a58`: restored the target to the source's two-line structure by
  joining “持续 4 回合。” and the extra indented “反冲力也让你后退 %d 码。” line as
  “持续 4 回合，同时反冲力让你后退 %d 码。” This is the only newline change;
  placeholder order is unchanged.
- Read the two exact source files only from the frozen `SOURCE-ANCHORS.json`
  checkouts/paths. Their SHA-256 values matched the frozen anchors:
  `d766ff990174ad9ac3a5a7ac1d4633159a868e48cdbbda8d1fe609d98a14b1a3`
  and `a32a2aa6489e4aae99d2daa9f055435cc049a7a7b21bd84e39927c7c2cafa424`.
  The Orcs repository/commit remains unpinned.
- Manifest-compatible LuaJIT loading of all three translation files passed:
  22,989 / 900 / 4,202 records; exactly 56 target-only changes against the
  SCOPE baseline, exactly two semantic target changes against
  `HOST-EXACT-DIFF-POST-FIX2.json`, and all other 54 workset targets unchanged.
  Source, source_tag, args_order, special, section, runtime-key,
  placeholder/markup, and applicable LF/TAB invariants passed. The removed
  line shifts later locator-only line numbers in `tome-orcs.lua`; those do not
  represent target changes.
- `python3 -B tools/i18n lint --strict`: pass, 30,308 translations,
  0 errors and 0 warnings.
- `git diff --check`: pass. No terminology file, `.ai/task` file, or unrelated
  working-tree file was modified; nothing was staged, committed, or pushed,
  and no agent was created.
