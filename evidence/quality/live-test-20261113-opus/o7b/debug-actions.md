# debug actions
00:03 tl-start o7b 192 (TL_GPU=1)
00:04 load save: click 读取游戏(512,115), 角色(212,130), 游玩(205,808)
00:05 welcome: 关闭所有联网功能→全部禁用; reload save
00:06 console: print player pos; list level entities
00:06 console: move void horror/netherworm mass/scourge wyrm near player via util.findFreeGrid + e:move(x,y,true); P:doFOV()
00:07 hover void horror (928,352) + shift+c (SHOW_CHARACTER_SHEET_CURSOR)
00:09 hover scourge wyrm (992,480)+shift+c, tab t
00:09 hover netherworm mass (928,608)+shift+c, tab t, hover first talent
00:10 console: makeEntityByName SPINAL_CAGE, ROD_ENTROPY; identify; addObject INVEN
00:12 console: P=game.player; P:learnTalentType("demented/madness",true); P:learnTalent(P.T_INSANITY_POOL,true); print insanity (debug menu k) 升级 not used due budget)
00:13 kill -9 701609 (end session)
