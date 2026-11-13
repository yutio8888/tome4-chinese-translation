# debug-actions o7d
00:03 tl-start
00:06 loaded save; welcome box: 关闭所有联网功能→全部禁用
00:06 console: makeEntityByName TINKER_SECOND_SKIN5/ROCKET_BOOTS5/GALVANIC_RETRIBUTOR5, identify, addObject INVEN
00:07 console: makeEntityByName TINKER_SECOND_SKIN5/ROCKET_BOOTS5/GALVANIC_RETRIBUTOR5, identify, addObject INVEN
00:08 UI 安装到物品→'你没有可供安装它的已装备物品'；console: makeEntity heavy armor, wearObject
00:10 UI 物品栏点击配件→安装到物品 键盘导航两次未成功(焦点落到地图操作菜单)；改用 console: P:doWearTinker(nil,nil,O3,BODY,1,A,false)
00:10 galvanic needs shield (on_subtype shield); console: doWearTinker O1 second skin → BODY armour
00:11 console: COUNCIL2 makeEntityByName/findFreeGrid/addEntity
00:12 结束：kill -9 本进程
