---

核验基准：engine 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`。

### Claim 1：译文把“概率完全抵消暴击”误译成“降低暴击额外伤害”

**结论：refuted**

源码证据：

- `game/modules/tome/data/talents/gifts/ooze.lua:256-269`
  - 技能赋予 `ignore_direct_crits = t.critResist(...)`，数值范围为 15–50。
  - 英文说明仍写成 `%d%% chance to shrug off`。
- `game/modules/tome/data/damage_types.lua:130-153`
  - 没有进行概率检定。
  - 每次 `crit_power > 1` 时，确定性计算：
    `reduce = (crit_power - 1) * ignore_direct_crits / 100`
  - 随后从暴击倍率中扣除该值并重算伤害。
- `game/modules/tome/class/interface/Combat.lua:1938-2000、2011-2029、2060-2077`
  - 物理、法术、精神暴击都将实际暴击倍率写入 `crit_power`，再进入上述统一伤害结算。
- `game/modules/tome/class/Object.lua:1763-1765`
  - 引擎自身将该属性显示为 `Reduces incoming crit damage`，并与降低对手暴击率的 `combat_crit_reduction` 明确区分。

例如暴击倍率为 1.5、`ignore_direct_crits=50` 时，最终倍率为 1.25，即暴击的额外 0.5 伤害被削减一半；并不是有 50% 概率把整个暴击降为普通命中。只有属性达到 100 时才会把暴击额外伤害全部消除。

因此 [mod-tome.lua:25320](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua:25320) 的“直接暴击……额外伤害降低 %d%%”准确对应固定源码行为。错误在英文 tooltip 已滞后，Gemini 的机制判断与实际调用链相反。

**人工决策：** 无需修改该句；建议保留现译。

### Claim 2：`wounds` 必须译为“创伤”，“流血”属于错误或术语不一致

**结论：refuted（作为译文缺陷不成立）**

源码证据：

- `game/modules/tome/data/talents/gifts/ooze.lua:259-263`
  - 技能实际添加的是 `cut_immune`，不存在 `wound_immune`。
- `game/modules/tome/class/Actor.lua:7554-7584、7622-7628`
  - `cut` 状态映射到 `cut_immune`，并以其数值进行概率免疫检定。
- `game/modules/tome/data/timed_effects/physical.lua:123-162`
  - `CUT` 与 `DEEP_WOUND` 都同时带有 `wound=true, cut=true, bleed=true`，其表现是持续流血。
- 同文件 `1094-1107`
  - `CRIPPLE` 只有 `wound=true`，没有 `cut=true`；因此该技能的 `cut_immune` 并不能泛化为所有“创伤”效果。
- `game/modules/tome/class/interface/PlayerDumpJSON.lua:276-280`
  - `cut_immune` 对外明确显示为 `Bleed Resistance`。
- `game/modules/tome/class/Object.lua:1775-1778`
  - 装备界面称其为 `Cut immunity`。
- [terminology/combat.tsv:53](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/terminology/combat.tsv:53) 与下一行分别规定 `bleed → 流血`、`cut → 流血`；[mod-tome.lua:856](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua:856) 也将 `Cut immunity` 译为“流血免疫”。

虽然术语表对孤立的 `wound` 规定为“创伤”，但本条英文 tooltip 的 `wounds` 同样已经滞后于实际属性。改成“创伤免疫”反而会错误暗示它能抵抗 `wound` 类但不含 `cut` 的效果。

**人工决策：** 无需修改“流血”；应按固定源码保留。若要消除英文与机制的偏差，应处理上游英文说明，而不是把中文改成“创伤”。

### Claim 3：`blindness` 译为“目盲”违反既定术语“致盲”

**结论：confirmed**

源码及术语证据：

- `game/modules/tome/data/talents/gifts/ooze.lua:259` 实际赋予 `blind_immune`。
- `game/modules/tome/class/Actor.lua:7554-7584、7622-7628` 将 `blind` 状态映射至 `blind_immune`。
- [terminology/combat.tsv:52](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/terminology/combat.tsv:52) 明确规定效果 subtype `blind → 致盲`。
- [mod-tome.lua:853](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua:853) 的通用属性界面也使用“致盲免疫”。
- 当前条目 [mod-tome.lua:25321](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/mod-tome.lua:25321) 使用“目盲免疫”，确实与规范术语不一致。

仓库其他技能说明仍可见“目盲免疫”，例如 `mod-tome.lua:21487、26804`，说明这是存量表面不一致，但不能覆盖当前术语表和通用属性界面的规范译法。

**必要人工决策：** 本条应改为“致盲免疫”。无需借此扩大为全仓“目盲”统一整改；其他存量条目应另行授权和建集处理。
