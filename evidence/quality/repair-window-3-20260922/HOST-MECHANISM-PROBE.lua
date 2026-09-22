assert(_VERSION == "Lua 5.1")
local effect
_t=function(s) return s end
newEffect=function(t) effect=t end
newEffect{
	name = "INSOMNIA", image = "effects/insomnia.png",
	desc = _t"Insomnia",
	long_desc = function(self, eff) return ("The target is wide awake and has %d%% resistance to sleep effects."):tformat(eff.cur_power) end,
	type = "mental",
	subtype = { psionic=true },
	status = "beneficial",
	parameters = { power=0 },
	on_gain = function(self, err) return _t"#Target# is suffering from insomnia.", _t"+Insomnia" end,
	on_lose = function(self, err) return _t"#Target# is no longer suffering from insomnia.", _t"-Insomnia" end,
	on_merge = function(self, old_eff, new_eff)
		-- Add the durations on merge
		local dur = old_eff.dur + new_eff.dur
		old_eff.dur = math.min(10, dur)
		old_eff.cur_power = old_eff.power * old_eff.dur
		-- Need to remove and re-add the effect
		self:removeTemporaryValue("sleep_immune", old_eff.sid)
		old_eff.sid = self:addTemporaryValue("sleep_immune", old_eff.cur_power/100)
		return old_eff
	end,
	on_timeout = function(self, eff)
		-- Insomnia only ticks when we're awake
		if self:attr("sleep") and self:attr("sleep") > 0 then
			eff.dur = eff.dur + 1
		else
			-- Deincrement the power
			eff.cur_power = eff.power * eff.dur
			self:removeTemporaryValue("sleep_immune", eff.sid)
			eff.sid = self:addTemporaryValue("sleep_immune", eff.cur_power/100)
		end
	end,
	activate = function(self, eff)
		eff.cur_power = eff.power * eff.dur
		eff.sid = self:addTemporaryValue("sleep_immune", eff.cur_power/100)
	end,
	deactivate = function(self, eff)
		self:removeTemporaryValue("sleep_immune", eff.sid)
	end,
}

local actor={sleeping=false, immunity=0}
function actor:addTemporaryValue(k,v) assert(k=="sleep_immune");self.immunity=v;return 1 end
function actor:removeTemporaryValue(k,id) assert(k=="sleep_immune" and id==1);self.immunity=0 end
function actor:attr(k) assert(k=="sleep");return self.sleeping and 1 or 0 end
for _,power in ipairs{8,10,16,20} do
 for _,dur in ipairs{1,3,10} do
  local e={power=power,dur=dur};effect.activate(actor,e)
  assert(math.abs(actor.immunity-power*dur/100)<1e-9)
  print("INSOMNIA",power,dur,actor.immunity)
 end
end
local e={power=16,dur=3};effect.activate(actor,e);effect.on_merge(actor,e,{dur=1});assert(e.dur==4 and e.cur_power==64)
print("MERGE",e.dur,e.cur_power)
e.dur=3;effect.on_timeout(actor,e);assert(e.cur_power==48);print("AWAKE_AFTER_DURATION_DECREMENT",e.dur,e.cur_power)
effect.on_merge(actor,e,{dur=20});assert(e.dur==10 and e.cur_power==160);print("DURATION_CAP",e.dur,e.cur_power)
_M={};util={bound=function(v,a,b)return math.max(a,math.min(b,v))end};rng={percent=function(p)return p>=100 end};game={player={hasQuest=function()return false end}}
function _M:checkHit(atk, def, min, max, factor, p)
	if atk < 0 then atk = 0 end
	if def < 0 then def = 0 end
	local min = min or 0
	local max = max or 100
	if game.player:hasQuest("tutorial-combat-stats") then
		min = 0
		max = 100
	end --ensures predictable combat for the tutorial
	local hit = math.ceil(50 + 2.5 * (atk - def))
	hit = util.bound(hit, min, max)
	print("checkHit", atk, "vs", def, "=> chance to hit", hit)
	return rng.percent(hit), hit
end
for _,damage in ipairs{20,50,80} do
 local _,chance=_M.checkHit({},50,damage);print("DISMISSAL_CHANCE",50,damage,chance)
 assert(chance==({[20]=100,[50]=50,[80]=0})[damage])
end
