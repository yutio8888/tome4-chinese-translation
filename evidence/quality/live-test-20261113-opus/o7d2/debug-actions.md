# debug actions
00:34:27 boot.sh
00:35:37 setup.sh (console: make 3 tinkers, heavy armour, attach second skin, place COUNCIL2)
00:36:36 con.sh -k open inventory via triggerVirtual SHOW_INVENTORY
00:36:58 focus.sh; key i
00:37:19 con.sh -k registerDialog ShowEquipInven
- 00:36 key i 未打开物品栏（无效）
- 00:37 con.sh -k 'D=require("mod.dialogs.ShowEquipInven")' 'game:unregisterDialog(game.dialogs[#game.dialogs]) game:registerDialog(D.new("x",game.player))' -> 物品栏打开（triggerVirtual SHOW_INVENTORY 一次未生效）
- 00:37 悬停身体栏锁甲 (236,438)、配件槽 (196,430)
