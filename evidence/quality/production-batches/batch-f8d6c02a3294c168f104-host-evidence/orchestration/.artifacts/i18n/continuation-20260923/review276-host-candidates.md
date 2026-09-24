# 第 276 批宿主预检（未裁决）

仅作宿主只读预检；不供 reviewer 使用，不代替独立复审或正式裁决。

- `ff98c01bb5` 抓取说明：英文 `attempt to grapple`，中文写成“并抓取”。固定主游戏 `game/modules/tome/data/talents/techniques/grappling.lua:104`；`class/interface/Combat.lua:2825-2833` 在目标不能被定身时明确返回 false。候选 fidelity 问题。
- `ffb21dd4cc` 超载傀儡结束日志：英文 `seems less dangerous`，中文“平静了下来”。固定主游戏 `game/modules/tome/data/timed_effects/magical.lua:600-618` 只是移除伤害和生命回复增益。候选语义问题。
- `fff8487389` 岩石傀儡说明：英文 `can become unstoppable`，中文“并且不可阻挡”。固定主游戏 `game/modules/tome/data/talents/gifts/summon-melee.lua:500-538` 赋予傀儡 `T_UNSTOPPABLE`，并非持续不可阻挡。候选条件遗漏。
- `0ae36fb978` 火焰披风说明：英文治疗量是 `10% of the damage dealt`，中文“你受到10%伤害值的治疗”未明说已造成伤害；DLC 文件 `tome-ashes-urhrok/data/general/objects/world-artifacts.lua:118,136-143`，本批哈希匹配，源码 commit 未固定。候选措辞精度问题。
- `0c22616dae` 黑色靴子描述：`treacherous road to the top of the world` 现译“背叛之路，直通天际”。可能是意译风格问题，暂无机制锚点；待 reviewer 观察后判断 advisory/pending。
