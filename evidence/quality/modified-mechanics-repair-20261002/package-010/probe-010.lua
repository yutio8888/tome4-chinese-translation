local _M = {}
function _M:getFeedbackDecay(mult)
	local mult = self:callTalent(self.T_BIOFEEDBACK, "getDecaySpeed") or 1
	if self.psionic_feedback and self.psionic_feedback > 0 then
		local feedback_decay = math.max(1, self.psionic_feedback*mult / 10)
		return feedback_decay
	else
		return 0
	end
end
function _M:recomputeGlobalSpeed()
	if self.global_speed_add >= 0 then self.global_speed = self.global_speed_base + self.global_speed_add
	else self.global_speed = self.global_speed_base / (1 + math.abs(self.global_speed_add)) -- Symmetric scaling
	end
	self.global_speed = math.max(self.global_speed, 0.1)
end
local actor=setmetatable({}, {__index=_M})
function actor:callTalent() return self.mult end
local n=0
for _,f in ipairs({0,0.1,0.9,1,5,20,100}) do
 for _,mult in ipairs({0.1,0.5,0.85,1}) do
  actor.psionic_feedback=f;actor.mult=mult
  local actual=actor:getFeedbackDecay()
  local expected=f>0 and math.max(1,f*mult/10) or 0
  assert(math.abs(actual-expected)<1e-12)
  if f>0 and f*mult/10<1 then assert(actual==1) end
  n=n+1
 end
end
local speeds=0
for _,s in ipairs({0.08,0.16,0.4,0.6}) do
 actor.global_speed_base=1;actor.global_speed_add=-(1-1/(1+s));actor:recomputeGlobalSpeed()
 assert(math.abs(actor.global_speed-(1+s)/(1+2*s))<1e-12)
 assert(math.abs(1-actor.global_speed-s/(1+2*s))<1e-12)
 speeds=speeds+1
end
-- The no-other-modifiers clause matters: additive positive speed uses a different branch.
actor.global_speed_base=1;actor.global_speed_add=0.5-(1-1/1.6);actor:recomputeGlobalSpeed()
assert(math.abs(actor.global_speed-1.125)<1e-12)
print('PASS: '..n..' fixed Feedback decay cases; '..speeds..' isolated Congeal Time cases; positive-speed modifier counterexample')
