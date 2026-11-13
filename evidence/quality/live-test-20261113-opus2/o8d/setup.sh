#!/bin/bash
# setup.sh (host-provided, host-tested): debug-console setup for o8d; prints S8 lines from game.log
cd /home/paseo/tome-live/testers/o8d; X="/home/paseo/tome-live/bin/tl-x o8d 204"
$X mousemove 1200 880; timeout 1 tail -f /dev/null
c(){ for i in 1 2 3; do if ./con.sh "$@"; then return 0; fi; timeout 2 tail -f /dev/null; done; echo "SETUP STEP FAILED"; return 1; }
c 'P=game.player Z=game.zone L=game.level A2=engine.Map.ACTOR'
c 'M=nil for _,a in pairs(L.entities) do if a.define_as=="COUNCIL2" then M=a end end if not M then M=Z:makeEntityByName(L,"actor","COUNCIL2") end' 'FX=nil for d=1,5 do for dx=-d,d do for dy=-d,d do local x,y=P.x+dx,P.y+dy if not FX and L.map:isBound(x,y) and not L.map(x,y,A2) and not L.map:checkEntity(x,y,engine.Map.TERRAIN,"block_move") then FX,FY=x,y end end end end' 'if M and not M.x and FX then Z:addEntity(L,M,"actor",FX,FY) end M=M print("S8M","COUNCIL2",M and M.name,M and M.x,M and M.y)' 'if M and M.x then print("S8S","COUNCIL2",L.map:getTileToScreen(M.x,M.y)) end'
c 'print("S8K",P:knowTalent(P.T_SMITH),P:knowTalent(P.T_THERAPEUTICS),P:knowTalent(P.T_EXPLOSIVES))'
grep -a "S8" game.log | tail -4
