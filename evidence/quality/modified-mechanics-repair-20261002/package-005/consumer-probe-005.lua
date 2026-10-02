local ts = {}
function newTalent(t) ts[t.name] = t end
dofile('/tmp/mmrfix005/game/modules/tome/data/talents/celestial/chants.lua')
local t = assert(ts['Chant Radiant'])
for _, limit in ipairs{1, 1.2, 1.999, 2, 2.7, 3} do
 local self = {turn_procs={}, T_CHANT_OF_FORTRESS=1, T_CHANT_OF_FORTITUDE=2, T_CHANT_OF_RESISTANCE=3, count=0}
 function self:isTalentActive(_) return true end
 function self:combatTalentScale(_, low, high) if low == 1 then return limit else return 4 end end
 function self:incPositive(_) self.count=self.count+1 end
 for j=1,10 do
  if j % 2 == 0 then t.callbackOnArcheryHit(self,t,{}) else t.callbackOnMeleeHit(self,t,{}) end
 end
 assert(self.count==math.floor(limit)+1)
 assert(tonumber(string.format('%d',limit))+1==self.count)
 print('radiant limit='..limit..' displayed='..string.format('%d',limit)..' actual='..self.count)
end
local resist = assert(ts['Chant of Resistance'])
local self = {}
function self:combatTalentLimit() return 25 end
local src={x=5,y=0}
core={fov={distance=function() return 5 end}}
self.x=0;self.y=0
local result=resist.callbackOnTakeDamage(self,resist,src,0,0,nil,100)
assert(result.dam==75)
assert(resist.getDamageChange(self,resist)==-25)
print('negative argument=-25; damage 100 -> '..result.dam)
