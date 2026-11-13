#!/bin/bash
# setup.sh (host-provided, host-tested): debug-console setup for o8c; prints S8 lines from game.log
cd /home/paseo/tome-live/testers/o8c; X="/home/paseo/tome-live/bin/tl-x o8c 203"
$X mousemove 1200 880; timeout 1 tail -f /dev/null
c(){ for i in 1 2 3; do if ./con.sh "$@"; then return 0; fi; timeout 2 tail -f /dev/null; done; echo "SETUP STEP FAILED"; return 1; }
c 'P=game.player Z=game.zone L=game.level A2=engine.Map.ACTOR'
c 'P:learnTalentType("demented/madness",true) P:learnTalent(P.T_INSANITY_POOL,true)' 'for _,t in ipairs{"T_DARK_WHISPERS","T_HIDEOUS_VISIONS","T_SANITY_WARP","T_CACOPHONY"} do P:learnTalent(t,true,3) end' 'print("S8T",P:knowTalent(P.T_SANITY_WARP),P:knowTalent(P.T_CACOPHONY),P.insanity,P.max_insanity)'
grep -a "S8" game.log | tail -4
