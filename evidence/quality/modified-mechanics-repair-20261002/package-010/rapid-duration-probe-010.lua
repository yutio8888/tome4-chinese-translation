local _M={tempeffect_def={RAPID={decrease=1}}}
function _M:timedEffects(filter)
	local todel = {}
	local def
	local effs = {}
	for eff, p in pairs(self.tmp) do
		effs[eff] = p
	end
	for eff, p in pairs(effs) do
		def = _M.tempeffect_def[eff]
		if not filter or filter(def, p) then
			if p.dur <= 0 then
				todel[#todel+1] = eff
			else
				if def.on_timeout then
					local old_source
					if p.src then
						old_source = p.src.__project_source
						p.src.__project_source = p 
					end -- intermediate projector source
					if def.on_timeout(self, p, def) then
						todel[#todel+1] = eff
					end
					if p.src then p.src.__project_source = old_source end
				end
			end
			p.dur = p.dur - def.decrease
		end
	end

	while #todel > 0 do
		self:removeEffect(table.remove(todel))
	end
end
local actor=setmetatable({tmp={RAPID={dur=1}}}, {__index=_M})
function actor:removeEffect(id) self.tmp[id]=nil end
assert(actor.tmp.RAPID.dur==1)
actor:timedEffects()
assert(actor.tmp.RAPID and actor.tmp.RAPID.dur==0)
actor:timedEffects()
assert(not actor.tmp.RAPID)
print('PASS: duration1 survives first normal timedEffects tick as0; removed on second tick')
