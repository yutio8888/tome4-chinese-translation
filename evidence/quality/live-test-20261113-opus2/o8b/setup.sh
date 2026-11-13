#!/bin/bash
# setup.sh (host-provided, host-tested): debug-console setup for o8b; prints S8 lines from game.log
cd /home/paseo/tome-live/testers/o8b; X="/home/paseo/tome-live/bin/tl-x o8b 202"
$X mousemove 1200 880; timeout 1 tail -f /dev/null
c(){ for i in 1 2 3; do if ./con.sh "$@"; then return 0; fi; timeout 2 tail -f /dev/null; done; echo "SETUP STEP FAILED"; return 1; }
c 'P=game.player Z=game.zone L=game.level A2=engine.Map.ACTOR'
c 'M=nil for _,a in pairs(L.entities) do if a.define_as=="VOR" then M=a end end if not M then M=Z:makeEntityByName(L,"actor","VOR") end' 'FX=nil for d=1,5 do for dx=-d,d do for dy=-d,d do local x,y=P.x+dx,P.y+dy if not FX and L.map:isBound(x,y) and not L.map(x,y,A2) and not L.map:checkEntity(x,y,engine.Map.TERRAIN,"block_move") then FX,FY=x,y end end end end' 'if M and not M.x and FX then Z:addEntity(L,M,"actor",FX,FY) end V=M print("S8M","VOR",M and M.name,M and M.x,M and M.y)' 'if M and M.x then print("S8S","VOR",L.map:getTileToScreen(M.x,M.y)) end'
c 'for _,inv in ipairs{V:getInven(V.INVEN_INVEN),V:getInven("HEAD")} do for i=#inv,1,-1 do local o=inv[i] if o.define_as=="ORB_ELEMENTS" or inv==V:getInven("HEAD") then V:removeObject(inv,i,true) o:identify(true) P:addObject(P.INVEN_INVEN,o) print("S8O",o.define_as,o:getName{do_color=false}) end end end'
c 'P:setEffect(P.EFF_SLOW,30,{power=0.3}) P:setEffect(P.EFF_DAZED,30,{})' 'for id in pairs(P.tmp) do print("S8E",id) end'
grep -a "S8" game.log | tail -10
