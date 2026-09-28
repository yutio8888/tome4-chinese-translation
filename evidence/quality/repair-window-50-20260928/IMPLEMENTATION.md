# repair-w50-20260928 implementation

Role: Paseo `EXECUTOR` (sole task-content writer)

Baseline: `68e1a83d859d239c84a55797930755d284f1f52d`

## Scope

- Updated the three SPEC-authorized terminology rows first, then modified exactly the 27 frozen targets: `mod-tome.lua` 3, `tome-ashes-urhrok.lua` 1, `tome-cults.lua` 7, and `tome-orcs.lua` 16.
- Did not modify source, source_tag, args_order, special, section, runtime keys, unrelated terminology rows, `.ai/task`, or unrelated translation records.
- Did not stage, commit, push, or create an agent.
- Read main-game source only from `/workspace/t-engine4` at fixed commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` using `git show`.
- Read DLC source only from the exact checkouts and paths frozen in `SOURCE-ANCHORS.json`. All ten DLC source-file SHA-256 values matched the frozen anchors; DLC repository commits remain unpinned.

## Terminology changes

### `terminology/classes.tsv`

- Before: `Writhing One	蜿蜒怪人	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业`
- After: `Writhing One	蠕动者	T.GAME.CLASS	classes	birth descriptor name	preferred	dlc	Cults of Entropy 职业；2026-09-28 Gemini 纯名称裁决统一为“蠕动者”（原记录“蜿蜒怪人”），同名技能亦作“蠕动者”`

### `terminology/talents.tsv`

Appended, in this order:

1. `Writhing One	蠕动者	T.GAME.TALENT	talents	talent name	preferred	dlc	恐怖之路第4级被动，与职业同名（2026-09-28 Gemini 纯名称裁决）`
2. `Mind Drones	精神无人机	T.GAME.TALENT	talents	talent name	preferred	dlc	钢铁之思技能：灵能与蒸汽科技融合的机械造物，drone＝无人机，不作“雄蜂”；效果 Mind Drone 与伤害类型 mind drone 同作“精神无人机”（2026-09-28 Gemini 纯名称裁决）`

All fields use one TAB separator, with no trailing whitespace and one final LF.

## Per-entry translation changes

### `mod-tome.lua`

- `dcb3be8789947060659081abe1d7fa05ef3c09c1a89193e5eb67a2fda0ddc0d4`
  - Before: `感谢夏图尔人在最后一刻阻止了你为疯狂的太阳开启传送门，通关ToME。`
  - After: `感谢夏·图尔人在最后一刻阻止了你为疯狂的太阳开启传送门，通关ToME。`
- `5ecf018f17a1b1332d8952bb03e6a01d1bdcb2b8e2d107a39cf61c40e5a86a77`
  - Before: `乌尔罗格，水之主，是水中的恐怖恶魔。水在他周围蠕动，仿佛想要逃离，使他的身形模糊不清。他看到你似乎并不惊讶。`
  - After: `乌尔罗格，水之主，望之令人生畏。水在他周围蠕动，仿佛想要逃离，使他的身形模糊不清。他看到你似乎并不惊讶。`
- `d5907b44fd13373c4b409075f8c61f09e1bda1b33a39683710568f2c8c8759d4`
  - Before: `你以惊人的意志力抵抗了关键的数秒，夏图尔人出现了，取走了法杖并杀死了你。`
  - After: `你以惊人的意志力抵抗了关键的数秒，夏·图尔人出现了，取走了法杖并杀死了你。`

### `tome-ashes-urhrok.lua`

- `a5ef7ca96fd9cdc73c8acebfc36ba8c20a82cb91e986602e499643800710a167`
  - Before: `乌尔罗格，水之主，是水中的#AQUAMARINE#恐怖#LAST#恶魔。水如同想要逃离一般在他的周围沸腾，蔓延的蒸汽使他的影子若隐若现。他面对你的表情似乎并不惊讶。`
  - After: `乌尔罗格，水之主，望之#AQUAMARINE#令人生畏#LAST#。他周围的水仿佛要逃离一般沸腾翻滚，翻涌的蒸汽使他的身形模糊不清。他面对你的表情似乎并不惊讶。`

### `tome-cults.lua`

- `a9c22a10e6919217ab1565fe13e496e10dbc8b9d91306eb2f5a1eb610357ae65`
  - Before: `这本书的封皮老而枯干。当你拿着它的时候，你感受到绝望、困难，痛苦，无助的感情向你袭来。书中的存在许诺着强大的力量，但是，代价是什么呢？`
  - After: `这本书的封皮老而枯干。当你拿着它的时候，许多感受涌上心头。绝望、苦难、走投无路与无望一齐向你袭来。这本书似乎还许诺着强大的力量，但是，代价是什么呢？`
- `5aece67353b2cb6a2c3602216c2e395c261f4e9f942e57e5b88d0542521b361c`
  - Before: `自一座古老的夏图尔远程传送门中现身`
  - After: `自一座古老的夏·图尔远程传送门中现身`
- `ae5ff796d91dda9b456c05543d5f7a2af33f3e33b74fa916a3d02e3f174b4e93`
  - Before: `暂时使目标从所受治疗中受到熵反冲，在 %d 回合内最多受到相当于治疗量 %d%% 的伤害。效果受魔力值加成。`
  - After: `暂时使目标从所受治疗中受到熵能反冲，在 %d 回合内最多受到相当于治疗量 %d%% 的伤害。效果受魔力值加成。`
- `3adf7808105acf588107df61015b408c0006903a07ac1d10af886172aab764c4`
  - Before: `有关必然性的课程——熵反馈和治疗`
  - After: `有关必然性的课程——熵能反冲和治疗`
- `170d34c156c4449569500568ddaa8aa4828e7b30df6b7967e78220adc9cefe22`
  - Before: `时间盛宴`
  - After: `时空盛宴`
- `a5a712dce8fd9267ebb6a31af38dc863f93d0251325fd918b56a1003250234d0`
  - Before: `蜿蜒`
  - After: `蠕动者`
- `703e6c3b71a1540920c5422520f06485ec6be35230aa0c2d4a853fa8adfe2a3c`
  - Before: `请选择#LIGHT_GREEN#蜿蜒怪人#WHITE#（位于疯狂系）作为你的职业`
  - After: `请选择#LIGHT_GREEN#蠕动者#WHITE#（位于疯狂系）作为你的职业`

### `tome-orcs.lua`

- `b437b99574b4dd3894e7d8c6da1b66057e68e30c469b1908a1d0142e4ab5ba6a`
  - Before: `没有任何一个自爱的工匠会被人发现没有佩戴它！`
  - After: `有自尊的工匠绝不会不戴它！`
- `b4679de67acbaa75761a363e8eaa145d6eed1827be25e348aec4d8d4f83a4f50`: `一束植物（蛇草）` → `一束草药（蛇草）` (`ingredient name`)
- `55e69bd264c61430bcd17d4852a005d14f70b11ff957f2494d02b50518c844ab`: `一束植物（延龄草）` → `一束草药（延龄草）` (`ingredient name`)
- `830097084214a46a8c3a9492f3e6759519fe1b16bebbb3df8af31ac369365b6f`: `一束植物（越桔）` → `一束草药（越桔）` (`ingredient name`)
- `7131acff97712e862cc59840d22c9999c2b92c46e4dd321cbd8e49cfd7d5bc83`: `一束植物（牛蒡）` → `一束草药（牛蒡）` (`ingredient name`)
- `0ecb437238bb31f7e7e89b2604c16ce7bcec4b57e145087b5bfcac43b88d59eb`: `一束植物（金叶）` → `一束草药（金叶）` (`ingredient name`)
- `5b7667fbda132a08e46320ec0c4d9fc95d3ccf0478498ed508af9473f912d274`: `一束植物（蛇草）` → `一束草药（蛇草）` (`entity name`)
- `7d1b6e5cefaffe0fdb12505341eb428ad9f14134ff19d3c4bc595516cd8b272e`: `一束植物（延龄草）` → `一束草药（延龄草）` (`entity name`)
- `d823125f848b645947c417d67affa54d81a163f15746032cbdc026b803fdf9a4`: `一束植物（越桔）` → `一束草药（越桔）` (`entity name`)
- `bd3b91fd9364f5a51118cc718df0d6e627705a5acd926bc89cc2bd509546f7af`: `一束植物（牛蒡）` → `一束草药（牛蒡）` (`entity name`)
- `857fac37468331b3722806e487c5ae4a4ad231b1fa213e03ea7aacdc38ea0504`: `一束植物（金叶）` → `一束草药（金叶）` (`entity name`)
- `071dea85dbeed66052328349353f61b48cc91a3219f32a398ca2a73061c60030`: `精神雄蜂` → `精神无人机`
- `c75f3d3e29577bdd7728386236fa6ef19f0af1c8bff0bfa593d4a6db41f27bbc`
  - Before: `将灵能和蒸汽科技结合，你在身边制造 5 只精神雄蜂飞向目标。`
  - After: `将灵能和蒸汽科技结合，你在身边制造 5 架精神无人机飞向目标。`
  - Before: `雄蜂接触到生物时，将进入其大脑 6 回合，干扰思考能力。`
  - After: `无人机接触到生物时，会附着其上并钻入其颅骨 6 回合，干扰思考能力。`
- `a8829bb799648837f489d5fc8030a7e07a4df60d2db42744030dffd5e54d8d3c`: `精神雄蜂` → `精神无人机`
- `9a75f2d93dafb66bd2c00befaa674742ff7ef5a58164d570c9c8b12a4bfe3e52`: `一个精神雄蜂飞入#Target#！` → `一架精神无人机钻入了#Target#！`
- `fd89f9a2d32a55e93a9ae2b84833e0ee68c54ee6d27620563b11798c66c0c8c1`: `#Target#脱离精神雄蜂影响。` → `#Target#脱离精神无人机影响。`

## Validation outcome

- Source anchors: PASS. All frozen source-file hashes matched. Main game was read at the fixed commit; DLC source repository/commit identities remain unpinned.
- LuaJIT semantic load/diff: PASS. Loaded baseline and current versions of all four translation files through the manifest-compatible LuaJIT bridge. Exactly 27 target fields changed (3/1/7/16); every changed target mapped to one WORKSET revision key; every other record and every non-target field remained equal.
- Newline invariants: PASS for all 27 changed targets. Strict lint additionally checked placeholders, markup, runtime keys, and terminology TSV structure.
- `python3 -B tools/i18n doctor`: PASS; Lua 5.1 / LuaJIT 2.1.0-beta3 and LPeg 0.10.2-1. Expected DLC source-unpinned warnings only.
- `python3 -B tools/i18n lint --strict`: PASS; 30,308 translations, 0 errors, 0 warnings.
- `git diff --check`: PASS.

## Residual findings

- In `a5ef7ca96fd9cdc73c8acebfc36ba8c20a82cb91e986602e499643800710a167`, the existing final sentence `他面对你的表情似乎并不惊讶。` adds “表情” relative to `He does not seem surprised to see you.`. SOURCE-CLAIMS explicitly required the final sentence to remain unchanged, so it was not modified.
- No other concrete out-of-scope issue was found during the bounded source check.
- Independent REVIEW/FINAL_REVIEW remains the orchestrator's responsibility.
