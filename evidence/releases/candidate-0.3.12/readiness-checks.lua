local p = game.player
local tag = AF_PHASE or "?"
local function out(k, v) print("[AFTEST2 " .. tag .. "] " .. k .. " = " .. tostring(v)) end
local TE = require "engine.interface.ActorTemporaryEffects"
local defs = TE.tempeffect_def
-- effects (same defs the tooltips read)
out("dozing.type", _t(defs.EFF_DOZING.type))
out("rime.subtype", table.concat(table.ts(table.keys(defs.EFF_RIME_WRAITH.subtype), "effect subtype"), "/"))
p:setEffect(p.EFF_BEAR_TRAP, 5, {power=0.3, dam=4, src=p})
local e = p:hasEffect(p.EFF_BEAR_TRAP)
out("bear.long_desc", e and defs.EFF_BEAR_TRAP.long_desc(p, e) or "NOT APPLIED")
p:setEffect(p.EFF_PRESSURE_SUIT, 5, {})
local s = p:hasEffect(p.EFF_PRESSURE_SUIT)
out("suit.long_desc", s and defs.EFF_PRESSURE_SUIT.long_desc(p, s) or "NOT APPLIED")
-- compare mode (lv1-01 was seen with Ctrl compare)
local Object = require "mod.class.Object"
local function ring(name, w)
  local o = Object.new{type="jewelry", subtype="ring", name=name, display="=", identified=true, desc="AF", wielder=w}
  o:resolve() o:resolve(nil, true) return o
end
local a = ring("AF ring A", {inc_damage_actor_type={living=5, unliving=5}})
local b = ring("AF ring B", {inc_damage_actor_type={living=3, all=2}})
out("compare.desc", tostring(a:getTextualDesc({b})):gsub("\n", " | "))
if tag == "pre" then p:addObject(p.INVEN_INVEN, a) p:addObject(p.INVEN_INVEN, b) p:wearObject(b, true, false) end
-- the plain "living" key elsewhere is untouched
out("plain.living", _t"living" .. " / " .. _t("living", "entity keyword"))
-- real NPC chat file (data/chats/corruptor-quest.lua)
local Chat = require "engine.Chat"
local c = Chat.new("corruptor-quest", p, p)
local n = 0
for id, ch in pairs(c.chats) do if id:find("^quick_reply") then n = n + 1 out("real." .. id, ch.text:sub(1, 40) .. " -> " .. ch.answers[1][1]) end end
out("real.quick_reply_count", n)
_G.AF_REAL = c
