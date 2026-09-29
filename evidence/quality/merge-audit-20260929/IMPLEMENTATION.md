# merge-audit-20260929 implementation

Role: Paseo EXECUTOR (single writer)

## Scope

Applied the nine `MERGE` items from `.ai/task/merge-audit-20260929/EXEC-PACKAGE.json` and the two listed ruling fixes. No terminology, task-state, staging, commit, merge-control, checkout, stash, or unrelated-file operation was performed.

For `base_version=DEV`, the final target uses `base_text` plus only the listed port. For `base_version=BR` (`C06`, `C07`), the current develop target was replaced by the branch `base_text`, then only the listed port corrections were applied.

## Target changes

- `C05` (`mod-tome.lua`, `mod-tome/data/lore/elvala.lua`):
  - `从夏·图尔传送门中提取能量` → `从夏·图尔远行传送门中提取能量`
  - `在此地以东的夏·图尔传送门上展开实验` → `在此地以东的夏·图尔远行传送门上展开实验`
- `C06` (`mod-tome.lua`, `mod-tome/data/lore/elvala.lua`, BR base): replaced the develop target with the branch target. A representative base change is `磐石也被其撕裂` → `白色石材纷纷碎裂`. The three required ports were applied to the branch base:
  - `这一切的受难者数不胜数……造成了更大的毁灭` → `死亡人数无法计数……又夺走了更多生命`
  - `带到了王宫的医院，将她交给医师` → `直接带到王宫的治疗场所，将她交给医生`
  - `想要操纵超越想象的可怕力量` → `玩弄我们无法控制的可怕力量`
- `C07` (`mod-tome.lua`, `mod-tome/data/lore/elvala.lua`, BR base): replaced the develop target with the branch target. A representative base change is `为什么你不是精灵们的领袖呢？` → `你为什么不当领袖？`. The three required ports were applied to the branch base:
  - `如果你成为了领袖，你可能会阻止这一切……或许我会一辈子恨你` → `如果你是领袖，你就能阻止这一切……我就不得不恨你`
  - the invented floating/force description → `整座塔都与大地分离，是某种来自群星的奇异之物，从天空坠落后沉睡在泥土之下`
  - `我们的魔法师找到了……墙壁似乎也呼吸着能量……巨大能量如同星云般在周围盘旋` → `我们的族人破解了……每个表面都闪耀着光芒，就连墙壁似乎也随着能量嗡嗡作响……高台上缓缓旋转着一片星云`
- `C08` (`mod-tome.lua`, `mod-tome/data/lore/fun.lua`):
  - rewrote only the listed skeleton explanation: `死的不能再死／消耗的法力／附着于其身上` → `死得不能再死／维持其复苏所需的力量／在创造它们时投入的那点微薄心力`
  - `只要靠近这种诡异的生物` → `靠近它们时会有一种奇特的疲惫感，仿佛`
  - `万幸的是……已经被证实` → `不过，尽管如此……已有记录证实`
  - `变相的壮大` → `变相地壮大`
  - `成功的摧毁……亲爱的请你一定要为我写一篇指南` → `成功地摧毁……劳驾行个好，为我写一篇指南吧`
  - retained the develop paragraph structure and the already-correct `骷髅兵通常都持有武器，有时甚至身披铠甲` wording.
- `C10` (`mod-tome.lua`, `mod-tome/data/lore/misc.lua`): `遇到一些……某种意义上的恩人` → `遇到一位……某种意义上的恩人`.
- `C26` (`mod-tome.lua`, `mod-tome/data/talents/spells/staff-combat.lua`): `震慑概率受法术强度加成` → `震慑概率受法术强度加成。`.
- `C34` (`mod-tome.lua`, `mod-tome/data/texts/unlock-mage_thaumaturgist.lua`): `这一宽度为3的纯粹奇术能量` → `这道宽度为3的纯粹奇术能量射线`.
- `C44` (`tome-orcs.lua`, `tome-orcs/data/lore/misc.lua`): `你现在就别抱怨这些了` → `你们现在就别私下议论了`.
- `C55` (`tome-orcs.lua`, `tome-orcs/data/talents/steam/gunslinging.lua`): `便会弹向下一个最近的敌人` → `都会按与第一个目标的距离由近及远弹向下一个敌人`.
- `WO-engine.lua` (`engine.lua`): Forgotten Cults description `蜿蜒怪人` → `蠕动者`.
- `WO-mod-boot.lua` (`mod-boot.lua`): Forgotten Cults description `蜿蜒怪人` → `蠕动者`.

## Source evidence

- Main-game evidence was read only with the package-provided `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:...` commands.
- Orcs evidence was read only from the package-provided checkout paths under `/workspace/tome4-dlcs/orcs/`.
- The Trick Shot implementation builds candidates with distance from the first target, sorts by `dist`, then consumes `table.remove(..., 1)`, supporting the `C55` wording.

## Findings intentionally not changed

- `C05`: `your alliance is worth a dozen lesser kings` remains `比一群小国王的支持更为重要`; the package classifies the weakened “a dozen” quantity as a minor unported defect.
- `C07`: `all carved out of flickering orange fire` remains omitted; the package says all three versions omit it and does not authorize a port.
- `C08`: `So, in turn` still lacks the explicit `反过来`; the package classifies it as a minor unported defect.

## Validation summary

- LuaJIT loaded the before/after copies of all four modified locale files. Record counts were unchanged; exactly 11 targets differed (`mod-tome.lua=7`, `tome-orcs.lua=2`, `engine.lua=1`, `mod-boot.lua=1`), while section, source, source_tag, argument count/order, and every other target remained identical.
- `python3 -B tools/i18n doctor`: passed; the expected unpinned-source warnings for the three DLCs remain.
- `python3 -B tools/i18n lint --strict`: passed, 30,305 translations, 0 errors, 0 warnings.
- `git diff --check`: passed with no output.

