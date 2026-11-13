# debug-actions o7a2
00:34 boot.sh 启动读档
00:35 控制台 makeEntity weapon/armor ego_chance=1000 level50, identify, addObject 到物品栏; 列出实体
00:36 控制台 triggerVirtual SHOW_INVENTORY 打开物品栏
00:39 控制台 game.player:showEquipInven("Inventory") 打开物品栏（标题为自传英文参数）；悬停 xdotool keydown ctrl
00:39 控制台 CharacterSheet.new(entities[4120] icy orc wyrmic)
00:41 关角色面板；控制台 entities[3683] orc high cryomancer :move(46,25,true) setTarget(player)
00:42 控制台 entities[3683] orc high cryomancer :move(46,25,true) setTarget(player)；KP_5 等待
00:44 控制台 entities[3683] orc high cryomancer move(46,25) setTarget(player)；6×KP_5 等待
00:45 控制台 C:forceUseTalent(T_FREEZE,{ignore_energy,force_target=player,ignore_cd})（等待键 KP_5/s 未推进回合 game.turn=0）
00:46 kill -9 773885（本会话 t-engine）
