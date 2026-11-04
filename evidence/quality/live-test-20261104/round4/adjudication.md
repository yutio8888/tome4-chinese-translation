r4-ds (DeepSeek v4.1 Flash, 14:00-20:30, GPU; level 1 only, goal not reached)
01 confirm: mod-tome.lua:3217 Achievements are not granted 不能完成游戏成就 -> 不会获得游戏成就
02 confirm: opening texts 欢迎你 #LIGHT_GREEN#@name@ -> 欢迎你，#LIGHT_GREEN#@name@ (mod-tome.lua 14 places, tome-orcs.lua:7876)
03 confirm: mod-tome.lua:1093 #00ff00#%s技能 %s 已经可以使用。 -> #00ff00#%s技能%s已经可以使用了。 (matches engine.lua:1523 wording)
04 reject: Accuracy bonus " crit mult" = critical power; 暴击伤害 is the library's established rendering for crit power (46 uses), not a different concept
05 reject: already fixed in 0329; tester saw it because the installed test addon was built at 11:21 (fixes through 0328 only), not through 0330 as the host stated. Host error, corrected; test addon rebuilt after this batch.
