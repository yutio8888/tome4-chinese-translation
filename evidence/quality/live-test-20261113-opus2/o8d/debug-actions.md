# o8d debug actions
06:32 boot.sh (start+load save)
06:33 setup.sh (console: place COUNCIL2 Tormak, check talents)
06:34 console: CT=require mod.dialogs.CreateTinker; registerDialog(CT.new(game.party,game.player))
06:35 console: game.party:giveAllIngredients(20); reopen CreateTinker
06:36 CreateTinker: clicked Create (tier5 痛苦压制药剂) after giveAllIngredients
06:37 console: CS=require mod.dialogs.CharacterSheet; registerDialog(CS.new(M)) (M=Tormak)
