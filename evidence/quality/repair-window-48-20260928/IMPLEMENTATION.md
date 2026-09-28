# Repair window 48 implementation

Task: `repair-w48-20260928`

Baseline: `ed7f9c750494adf8960a73860def7200e43e467d`

## Files changed

- `terminology/creatures.tsv`: appended the two SPEC-authorized preferred rows, byte-for-byte with the prescribed eight TAB-separated fields.
- `mod-tome.lua`: changed three frozen targets.
- `tome-ashes-urhrok.lua`: changed eighteen frozen targets.
- `tome-orcs.lua`: changed one frozen target.

No source, source tag, argument order, special field, placeholder, markup sequence, or target newline count changed. No files under `.ai/task/` were modified.

## Changed entries

- `175effe253b96a8e948f7adbbc22e58dedd6fd5484d25e593bd7fbcadd9740c9`: restored “世界之间” and “埃亚尔”; made the meteor land nearby, its shockwave knock the player down, and the handler die instantly.
- `196ce36308d7acda3481aaff411fb7d580918d3d50a49e2ef4f74e10695a7546`: corrected the same meteor causality and changed “水晶体” to “水晶”.
- `1c39a9e76d99c403df2c8b1a4e92c950225555e22e6ce43a9ccecda43ae89db4`: renamed wretchling to “小劣魔”.
- `3626a664159b512cecd555e75c734070f403f267a1344b44ef73c65e07029300`: restored the qualifiers “十分规律地”, “几乎”, and “罕见”.
- `3e4633fa50203e6813c8c62d00b29cb8e478476b1999e901840498f41de5d563`: renamed water imp to “水小鬼”.
- `5ae7f508b5e957037dfadc8ab5814f56bdc6dbf3f66fd4819bc8f3abbf8f7f2d`: renamed wretchling to “小劣魔”.
- `5e73a630079200a2ad23ec06d01ddfdce4345ea8012926fdd966ca05722be210`: rendered `unreasonably lethal` as “致命得最离谱”.
- `633ee7605b9c379078bbd321cc06f2b56cad15f34ac77c1ba50ae6c8398d877d`: renamed all three occurrences, including the plural form, to “小劣魔”.
- `6a71689b25a51f37307e6a31ee27c17db6a3cadc96aa5233fd77f2c90fe1eee1`: renamed water imp and wretchling to “水小鬼” and “小劣魔”; unified the pronoun to “它们”.
- `8c101775476baaff25a3bda5be6a52d102fba656118f664e9a20a10f8a407051`: renamed wretchling to “小劣魔”.
- `92a2fd32a245001c36a5dd177e86c66b40579b3ad945d9af732deb96d36929e3`: renamed “一只小水怪” to “一只水小鬼”.
- `a9fdf64994c6f59f7ff7c25bfc0ac446d8efe8cbe8731557a419d5b7ccd8e24a`: renamed wretchling to “小劣魔”.
- `ab5e6afeb14b3f6dd9f35d5b6db6c20b279f536956960d170cfff5d843826bcd`: renamed “一只酸液树魔” to “一只小劣魔”.
- `ae4cc0af7a48981a15f1be7cc567b9ee60dd123c5ed5c46829b6539e1a1a8c05`: restored the Sher'Tul's “狡诈用心”, “一波波烈焰”, wandering minotaurs, the revenge cause, and “绿翡翠之子”.
- `b7b0565f203cf5bc1dcbef5f43be1f8597b6b4a41fdabb9faa1c81faa0d8c659`: renamed “一只酸液树魔” to “一只小劣魔”.
- `b98e293eb11dbf077a3a34eaadfefc9a729c84e1c736926b349290cfe5288f4d`: renamed “恶魔雕像：酸液树魔” to “恶魔雕像：小劣魔”.
- `ba5e371016a3ec1ccee0c31c6fc51d7c9df32359966be306084fb1cdff3c1d83`: corrected the past-time reverence, non-duplicative lifetime comparison, eastward farportal experiment, and Linaniil's `perhaps`/battlefield assertion.
- `cb8edf8808e60c4317e8a966f7b64755591854be189d6bb2050ac6ce8c8da17f`: renamed “恶魔雕像：小水怪” to “恶魔雕像：水小鬼”.
- `d0aff018a9b82598d774ff4cf45515056d1f600428bbe9176294276eacc906b3`: renamed wretchling to “小劣魔”; retained “绿翡翠之子”.
- `dc3200b76ddf5f8a6d2db60023aa13a2dc8e2ea3fb28f8898cf9906c0e175281`: changed the Abashed Expanse to being “抛入星辰之间的虚空”.
- `e983810c8cf9bb078525284781ccc9705bc260ce9f0c3209485bd91c19f464d0`: renamed every singular occurrence of wretchling to “小劣魔”.
- `ec6efb83efbfbd981ea6f4abcba0a9d06ee8c08e4aec49ef39a8c4bbfe5a5c2b`: renamed both control and mutant wretchlings to “小劣魔”.

## Source basis

The edits follow `SOURCE-CLAIMS.json` and the frozen excerpts in `SOURCE-ANCHORS.json`. Core entries are anchored to ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`; Ashes and Orcs evidence is from the named public checkouts and remains source-unpinned as recorded by the task.

## Observations not changed

No additional issue was identified that required an out-of-scope edit. Existing unrelated working-tree changes and untracked files were left untouched.

## Repair round 1 (cycle 0 REVIEW findings)

Only the two `status=confirmed` findings in `ADJUDICATION-R0.json` were changed. No terminology row or `.ai/task/` file was modified in this round.

- `175effe253b96a8e948f7adbbc22e58dedd6fd5484d25e593bd7fbcadd9740c9`
  - Before: `当你醒来后，你发现你身处一处和主大陆分离的焦土，而你旧时的记忆渐渐涌来。你立时惊醒——恶魔们要毁灭你的故乡！`
  - After: `当你逐渐恢复意识、脚下这块灼热土地构成的平台正从主大陆分裂时，旧日的记忆涌入脑海。你终于清醒过来——恶魔们要毁灭你的故乡！`
  - Basis: public Ashes `tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua:27`; checkout file SHA-256 `313846d367490a70929a228528ee3279541ae6f9cafbcef941a4daa2bb577974` matched `SOURCE-ANCHORS.json`. The temporal relation now follows `As you recover, and ... splits` and aligns with frozen entry `196ce36308`.
- `633ee7605b9c379078bbd321cc06f2b56cad15f34ac77c1ba50ae6c8398d877d`
  - Before: `许多冒险家都遭遇过小劣魔。相当可怕，小劣魔们，成群出现，灼烧腐蚀。但这些冒险家们不知道，小劣魔只是它的未成熟的孩子。`
  - After: `许多冒险家都遭遇过小劣魔。相当可怕，小劣魔们，成群出现，撕咬，灼烧腐蚀。但这些冒险家们不知道，那些只是幼体。`
  - Basis: public Ashes `tome-ashes-urhrok/data/general/npcs/major-demon.lua:52`; checkout file SHA-256 `52dd4d14f552ddcafc6bf6f8fd5ea48018adfb393169b9dd10ea8381b66827cc` matched `SOURCE-ANCHORS.json`. This restores `gnashing` and gives `those are just the children` an explicit plural referent.

Manifest-backed `LocaleLoader` loaded the three baseline files and the three current translation files through LuaJIT. Relative to the task baseline, exactly the frozen 22 targets differ and no other record or metadata differs. Relative to the frozen cycle-0 REVIEW candidate, exactly the two revision keys above differ. Newline counts, markup/placeholders, LF-only encoding, and per-line leading whitespace are unchanged. Strict lint reported 30308 translations with 0 errors and 0 warnings; `git diff --check` and `git diff --cached --check` produced no diagnostics.

## Repair round 2 (cycle 1 RE_REVIEW findings)

Only the two `status=confirmed` findings in `ADJUDICATION-R1.json` were changed. The other 20 workset targets, terminology data, and `.ai/task/` files were not modified in this round.

- `ba5e371016a3ec1ccee0c31c6fc51d7c9df32359966be306084fb1cdff3c1d83`
  - Before: `“我已经同其他种族的首领接触过了，半身人非常支持这项计划，纳格尔的摄政王甚至同意将他们历史上对夏·图尔遗迹的部分研究成果同我们分享。”`
  - After: `“我已经同其他种族的首领接触过了，半身人非常支持这项计划，纳格尔的摄政们甚至已经向我们提供了他们历史上对夏·图尔遗迹的部分研究成果。”`
  - Basis: ToME commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`, `game/modules/tome/data/lore/elvala.lua`, frozen source sentence `The Nargol regents have even provided us with some of their historical research on Sher'Tul ruins.`
- `ae4cc0af7a48981a15f1be7cc567b9ee60dd123c5ed5c46829b6539e1a1a8c05`
  - Before: `最近我们也开始在我们的大陆上饲养米诺陶`
  - After: `最近我们也开始在我们的大陆上繁育米诺陶`
  - Basis: public Ashes `tome-ashes-urhrok/data/lore/demon.lua:356`; checkout file SHA-256 `d3adada58124ab822393a43a8ec21060a5d465bfca69ff02d4b46df31b92e142` matched `SOURCE-ANCHORS.json`; source remains repository/commit-unpinned as frozen.

Manifest-backed `LocaleLoader` loaded the three baseline files and the three current translation files through LuaJIT. Relative to the task baseline, exactly the frozen 22 targets differ; relative to the frozen cycle-1 RE_REVIEW candidate, exactly the two revision keys above differ. Metadata, target newline counts, markup/placeholders, LF-only encoding, and per-line leading whitespace are unchanged. Strict lint reported 30308 translations with 0 errors and 0 warnings; `git diff --check` produced no diagnostics.

### execute-04 fresh retry verification

The two round-2 target edits left by the terminated `execute-03` run were already correct, so `execute-04` made no translation change. It independently confirmed both current targets against the frozen workset, adjudication, and source anchors: the Nargol sentence uses plural regents and completed provision, and the minotaur sentence uses “繁育”. The other 20 workset targets and the terminology data were not changed.

The manifest-backed LuaJIT comparison again loaded all three baseline and current translation files and reported exactly 22/22 frozen target changes with no metadata, newline, markup, placeholder, LF, or leading-TAB drift. `python3 -B tools/i18n lint --strict` again reported 30308 translations with 0 errors and 0 warnings, and `git diff --check` produced no diagnostics.

## Repair round 3 (cycle 2 RE_REVIEW findings)

Only the two `status=confirmed` findings in `ADJUDICATION-R2.json` were changed. The other 20 workset targets, terminology data, and `.ai/task/` files were not modified in this round.

- `e983810c8cf9bb078525284781ccc9705bc260ce9f0c3209485bd91c19f464d0`
  - Before: `每一只战斗过的小劣魔都为我们的目标奉献了一切。`
  - After: `每一只参战的小劣魔都为我们的事业作出了巨大贡献。`
  - Basis: public Ashes `tome-ashes-urhrok/data/lore/demon.lua:295`; frozen source `every wretchling that fights does an incredible service to our cause`; source remains repository/commit-unpinned as recorded in `SOURCE-ANCHORS.json`.
- `a9fdf64994c6f59f7ff7c25bfc0ac446d8efe8cbe8731557a419d5b7ccd8e24a`
  - Before: `把环境中的魔力转化为热量能量`
  - After: `把环境中的魔力转化为身体所需的能量`
  - Basis: public Ashes `tome-ashes-urhrok/data/lore/demon.lua:52`; frozen source `convert ambient magic into caloric energy`; source remains repository/commit-unpinned as recorded in `SOURCE-ANCHORS.json`.

The manifest-backed LuaJIT comparison loaded all three baseline and current translation files. Relative to the task baseline, exactly the frozen 22 targets differ; relative to frozen `CONTEXTUAL-ENVELOPE-r2a1.json`, exactly the two revision keys above differ. Metadata and target LF/TAB/markup/placeholder sequences are unchanged, and all three translation files remain LF-only. Strict lint reported 30308 translations with 0 errors and 0 warnings; `git diff --check` produced no diagnostics.

The first bounded comparison attempt used an over-strong source-to-target placeholder equality assertion and stopped on unchanged revision `ab5e6afeb14b3f6dd9f35d5b6db6c20b279f536956960d170cfff5d843826bcd`. This was a verifier-only false positive, not a translation regression. The corrected comparison checks the frozen R2 target against the current target and passed.
