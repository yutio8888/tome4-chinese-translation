# Flame 技能名裁决（2026-09-23）

- 维护者提出：「火焰」作技能名过短、缺少法术感；要求 gpt-6-astra、opus 5.5、Gemini 3.8 flash 三方讨论。
- 底稿：同目录 `BRIEF.md`（源码 624a6732 `game/modules/tome/data/talents/spells/fire.lua:21`）。
- 结果（三方一致，均核验底稿事实无误）：
  - gpt-6-astra（agent e7c6fb4f）：RENAME 火焰术；备选 烈焰术。
  - claude-opus-5-5（agent 71569f08）：RENAME 火焰术；备选 烈焰术、灼焰术。
  - gemini-3.8-flash（agent 701b7dce）：RENAME 火焰术；备选 烈焰术、火焰弹。
- 宿主复核：「火焰术」不是任何技能名；既有两处出现为 Gwai 传说中的「火焰术士」（无关）与 Shadow Mages 描述。后者英文 `Flames` 经源码 `data/talents/cursed/shadows.lua:139,229,601` 核实指 `SHADOW_FLAMES`（暗影之火），同步改为「暗影之火」以免误指。
- 维护者批准：「同意修改为火焰术」。
- 修改：三个组件的 talent name 行；大法师职业描述与宽射线解锁文本（原「火球术」）；Burning Wake 描述（原「火焰」）；`terminology/talents.tsv` Flame → 火焰术（preferred）。技能树类型名 fire=火焰 不变。
