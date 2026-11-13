#!/bin/bash
# setup.sh (host-provided, from o7d's verified console commands): create 3 tinkers, wear heavy armour, attach second skin to it, place Council Member Tormak; prints O7D2 lines from game.log
cd /home/paseo/tome-live/testers/o7d2; X="/home/paseo/tome-live/bin/tl-x o7d2 196"
$X mousemove 1200 880; timeout 1 tail -f /dev/null
c(){ for i in 1 2 3; do if ./con.sh "$@"; then $X keyup ctrl; return 0; fi; $X keyup ctrl; timeout 2 tail -f /dev/null; done; echo "SETUP STEP FAILED"; return 1; }
c 'P=game.player Z=game.zone L=game.level' 'O1=Z:makeEntityByName(L,"object","TINKER_SECOND_SKIN5")' 'O2=Z:makeEntityByName(L,"object","TINKER_ROCKET_BOOTS5")' 'O3=Z:makeEntityByName(L,"object","TINKER_GALVANIC_RETRIBUTOR5")' 'for _,o in ipairs{O1,O2,O3} do o:identify(true) P:addObject(P.INVEN_INVEN,o) end'; $X keyup ctrl
c 'A=Z:makeEntity(L,"object",{type="armor",subtype="heavy",ego_chance=-1000},nil,true)' 'A:identify(true) print("O7D2",P:wearObject(A,true,false),A:getName{do_color=false})'; $X keyup ctrl
c 'B=P:getInven("BODY")' 'print("O7D2W",P:doWearTinker(nil,nil,O1,B,1,A,false))' 'print("O7D2T",A.tinker and A.tinker:getName{do_color=false})'; $X keyup ctrl
c 'M=Z:makeEntityByName(L,"actor","COUNCIL2") A2=engine.Map.ACTOR' 'X2,Y2=util.findFreeGrid(P.x,P.y,5,true,{[A2]=true})' 'Z:addEntity(L,M,"actor",X2,Y2) print("O7D2M",M.name,X2,Y2)' 'print("O7D2S",L.map:getTileToScreen(X2,Y2))'; $X keyup ctrl
grep -a 'O7D2' game.log | tail -6
