# repair-w46-20260927 implementation

## Scope

- Modified only the 20 frozen translation targets in `tome-orcs.lua`.
- Preserved every source, source tag, argument order, special field, section, and all non-workset records.
- Wrote only this implementation evidence and `VALIDATION.json` outside the translation file.
- Did not modify terminology, task records, rules, source code, or unrelated working-tree files.
- Orcs source repository/commit remains unpinned. All 14 referenced source files matched the SHA-256 values frozen in `SOURCE-ANCHORS.json` before implementation.

## Target changes

1. `07f727721694`: changed only “化学道具” to “化学蒸汽工具”.
2. `533af4da88c5`: changed only “铁匠道具” to “铁匠蒸汽工具”.
3. `97a01b5c6a25`: changed only “爆炸学道具” to “爆炸学蒸汽工具”.
4. `d511b6b5f698`: changed only “机械道具” to “机械蒸汽工具”.
5. `eaca65fddbf8`: changed only “治疗学道具” to “治疗学蒸汽工具”.
6. `f466031dbbc9`: corrected the Dwarven berserker's accidental collision; restored Conclave Vault as “孔克雷夫宝库”, the wild-infusion impact relationship, and “这时”; fixed the Thalore punctuation; restored “沙虫女皇之心”, the future prospect being desired, and “相位之门” rune; restored the demonic statue's call and the Shalore's free hands; removed the extra blank line after the Doomelf paragraph.
7. `f4d9f76b597f`: restored the higher-percentage-only condition and regeneration toward that energy's maximum.
8. `f5df0b88f8fb`: removed invented timing, restored partial cheerblossom recovery, and restored the later request condition.
9. `f64bd7b5ede4`: restored two-tab indentation on both continuation lines only.
10. `f68acc60e695`: removed the one extra blank line after the first letter heading; in the bounded cycle-1 FIX, corrected the first letter so the Ogres and the Shaloren are joining forces with the Allied Kingdoms.
11. `f6d180323e53`: restored six source-aligned lines and two-tab indentation for all five continuation lines.
12. `f7fa4d6ac65b`: restored the Anomaly as the named agent responsible for both Khulmanar's and the costly combatants' deaths.
13. `f991285e5619`: restored hook-shot specificity, creature/location wording, “最多” distance limits, the no-ammo reason, punctuation, and all three continuation tabs.
14. `fa9e9b5cd31f`: restored the antimagic-shot identity, antimagic sap effect, “奥术法力燃烧”, the no-ammo reason, and all three continuation tabs.
15. `fb68502f3ed1`: restored fierce argument, application to as many recipients as possible, the non-forgiveness request wording, past cowardice, and the promised near-future result.
16. `fe6aea82cf87`: restored the temporary “for now” customer status.
17. `feb159a7c452`: changed “华丽的手枪” to the sibling-aligned “华丽的枪”.
18. `ff03daa8a279`: restored the instruction that the player must not let anything take the Prides' freedom again.
19. `ff110b738aaf`: aligned the Moon Radiance sentence with the sibling effect's stat wording and corrected punctuation.
20. `ff22e159c34f`: corrected Qog's Essentials to “寇格的必需品”.

## Risks and retained decisions

- The public Orcs checkout is source-unpinned. Exact frozen file hashes matched, but no repository commit can be claimed.
- The pocket-time lore was checked paragraph by paragraph. Only the frozen claims and directly associated sentence corrections were changed; unrelated existing wording was retained.
- The smoke-screen “仇恨丢失” wording was retained because it matches the anchored `setTarget(nil)` implementation.
- Pending terminology decisions listed in the SPEC, including Sunwall-related names, were not changed.
- Independent language review remains the host's next gate.

## Cycle-1 bounded FIX

- Replaced only the confirmed sentence in `f68acc60e695` with “我希望这是你们一族——当然，既指你们食人魔，也包括派遣你们过来的永恒精灵——与联合王国联手的第一步。”.
- Preserved all other text, markup, and the single blank line after the first heading.
- Revalidated the complete 20-target workset against HEAD; no additional target or non-target record changed.

## Cycle-3 bounded FIX

- In `f466031dbbc9`, replaced only “骨盾” with “骨甲” in the Ogre Reaver paragraph, matching the anchored `bone armor` source.
- Retained the adjudicated “异形触手” wording and preserved all other text, paragraphs, blank lines, and the terminal newline.
- Revalidated the complete 20-target workset against HEAD; no additional target or non-target record changed.

## Cycle-4 FINAL_REVIEW bounded FIX

- In `f466031dbbc9`, replaced only “一群无可言喻地强大的七彩龙” with “一群无可言喻地强大的多彩巨龙”, matching the confirmed preferred terminology for `multi-hued wyrms`.
- Preserved the rest of the target, its paragraphs, blank lines, and terminal newline.
- Revalidated the complete 20-target workset against HEAD; no additional target or non-target record changed.
