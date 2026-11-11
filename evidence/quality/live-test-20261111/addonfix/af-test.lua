local p = game.player
local function out(k, v) print("[AFTEST] " .. k .. " = " .. tostring(v)) end
local TE = require "engine.interface.ActorTemporaryEffects"
local defs = TE.tempeffect_def
-- 1 otber / 2 parasitic: header strings used by effect tooltips
out("dozing.type", defs.EFF_DOZING.type .. " -> " .. _t(defs.EFF_DOZING.type))
local keys = table.keys(defs.EFF_RIME_WRAITH.subtype)
out("rime.subtype", table.concat(keys, ",") .. " -> " .. table.concat(table.ts(table.keys(defs.EFF_RIME_WRAITH.subtype), "effect subtype"), "/"))
-- 3 bear trap pinned
p:setEffect(p.EFF_BEAR_TRAP, 5, {power=0.1, dam=10, src=p})
local e = p:hasEffect(p.EFF_BEAR_TRAP)
out("bear.long_desc", e and defs.EFF_BEAR_TRAP.long_desc(p, e) or "NOT APPLIED")
-- 4 pressure suit
if defs.EFF_PRESSURE_SUIT then
  p:setEffect(p.EFF_PRESSURE_SUIT, 5, {})
  local s = p:hasEffect(p.EFF_PRESSURE_SUIT)
  out("suit.long_desc", s and defs.EFF_PRESSURE_SUIT.long_desc(p, s) or "NOT APPLIED")
else out("suit", "EFF_PRESSURE_SUIT missing") end
p:setEffect(p.EFF_DOZING, 5, {})
p:setEffect(p.EFF_RIME_WRAITH, 5, {src=p})
-- 5 living damage line
local Object = require "mod.class.Object"
local o = Object.new{type="jewelry", subtype="ring", name="AF test ring", display="=", identified=true,
  wielder={inc_damage_actor_type={living=5, unliving=7, all=3}}}
o:resolve() o:resolve(nil, true)
out("ring.desc", tostring(o:getTextualDesc()):gsub("\n", " | "))
p:addObject(p.INVEN_INVEN, o)
-- 6 quick_reply [leave]
local Chat = require "engine.Chat"
local c = setmetatable({chats={}, quick_replies=0, npc=p, player=p, chat_env={}, data={}}, {__index=Chat})
c:addChat{id="welcome", text="AF quick reply test", answers={{"Answer", quick_reply="Quick reply text"}}}
c.default_id = "welcome"
out("quick_reply0.answer", c.chats.quick_reply0 and c.chats.quick_reply0.answers[1][1])
_G.AF_CHAT = c
