# debug-actions o7a
- 00:05 load save via 读取游戏→astajed→游玩 (no new char, no zone change)
- 00:05 console: print player pos and level entities
- 00:06 console: move uids 4228(GMA),4120(wyrmic),4089(high pyro),4345(soldier),4038(rare 兽人烈焰术士 未知的织梦) to free grids near player via util.findFreeGrid+move(x,y,true)
- 00:09 console: move 4120 wyrmic,4089 high pyro to free cells in column 47 (col 46 hover blocked)
- 00:10 console: game:registerDialog(CharacterSheet.new(__uids[4228])) to inspect GMA
- 00:11 console: register CharacterSheet for 4228 then unregister console dialog D
- 00:12 console: delayed (os.time+4s) registerDialog(CharacterSheet.new(__uids[4228]))
- 00:13 kill -9 702059 (own t-engine)
