#!/bin/bash
# setup.sh (host-provided, host-tested): debug-console setup for o8a; prints S8 lines from game.log
cd /home/paseo/tome-live/testers/o8a; X="/home/paseo/tome-live/bin/tl-x o8a 201"
$X mousemove 1200 880; timeout 1 tail -f /dev/null
c(){ for i in 1 2 3; do if ./con.sh "$@"; then return 0; fi; timeout 2 tail -f /dev/null; done; echo "SETUP STEP FAILED"; return 1; }
c 'P=game.player Z=game.zone L=game.level A2=engine.Map.ACTOR'
c 'M=nil for _,a in pairs(L.entities) do if a.define_as=="ELANDAR" then M=a end end if not M then M=Z:makeEntityByName(L,"actor","ELANDAR") end' 'FX=nil for d=1,5 do for dx=-d,d do for dy=-d,d do local x,y=P.x+dx,P.y+dy if not FX and L.map:isBound(x,y) and not L.map(x,y,A2) and not L.map:checkEntity(x,y,engine.Map.TERRAIN,"block_move") then FX,FY=x,y end end end end' 'if M and not M.x and FX then Z:addEntity(L,M,"actor",FX,FY) end E1=M print("S8M","ELANDAR",M and M.name,M and M.x,M and M.y)' 'if M and M.x then print("S8S","ELANDAR",L.map:getTileToScreen(M.x,M.y)) end'
c 'M=nil for _,a in pairs(L.entities) do if a.define_as=="ARGONIEL" then M=a end end if not M then M=Z:makeEntityByName(L,"actor","ARGONIEL") end' 'FX=nil for d=1,5 do for dx=-d,d do for dy=-d,d do local x,y=P.x+dx,P.y+dy if not FX and L.map:isBound(x,y) and not L.map(x,y,A2) and not L.map:checkEntity(x,y,engine.Map.TERRAIN,"block_move") then FX,FY=x,y end end end end' 'if M and not M.x and FX then Z:addEntity(L,M,"actor",FX,FY) end E2=M print("S8M","ARGONIEL",M and M.name,M and M.x,M and M.y)' 'if M and M.x then print("S8S","ARGONIEL",L.map:getTileToScreen(M.x,M.y)) end'
grep -a "S8" game.log | tail -8
