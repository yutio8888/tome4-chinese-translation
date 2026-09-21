# 宿主独立核验

spot-06：ooze.lua:256–269 把 critResist 同时传入 ignore_direct_crits 与第一个数值占位符；damage_types.lua:130–154 把暴击倍率的超出 1 部分按该百分比降低。现译「额外伤害降低」有固定源码依据，不因英文旧描述使用 chance 就判为错译。此记录不提供给 REVIEWER。
