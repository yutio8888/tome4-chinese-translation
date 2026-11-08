-- usage: luajit extract.lua <component> <file>...  ; prints TSV: component \t file \t field \t text (escaped)
local comp = arg[1]
string.tformat = function(s) return s end
string.capitalize = string.capitalize or function(s) return s end
local function esc(s) return (s:gsub("\\", "\\\\"):gsub("\t", "\\t"):gsub("\n", "\\n"):gsub("\r", "")) end
local dummy
dummy = setmetatable({}, {__call = function() return dummy end, __index = function() return dummy end,
  __concat = function() return "" end, __add = function() return 0 end, __sub = function() return 0 end,
  __mul = function() return 0 end, __div = function() return 0 end, __unm = function() return 0 end,
  __lt = function() return false end, __le = function() return false end})
local out = {}
local function emit(file, e)
  if type(e) ~= "table" or not e.unique or type(e.name) ~= "string" then return end
  local function f(k, v) if type(v) == "string" and v ~= "" then out[#out+1] = table.concat({comp, file, k, esc(e.name), esc(v)}, "\t") end end
  f("name", e.name)
  f("desc", e.desc)
  f("unided_name", e.unided_name)
  f("special_desc_str", e.special_desc)
  if type(e.use_power) == "table" then f("use_power_name", e.use_power.name) end
end
for i = 2, #arg do
  local file = arg[i]
  local env
  env = setmetatable({
    _t = function(s) return s end, string = string, table = table, math = math, pairs = pairs, ipairs = ipairs,
    type = type, tostring = tostring, tonumber = tonumber, select = select, unpack = unpack, next = next, rawget = rawget,
    setmetatable = setmetatable, print = function() end, require = function() return dummy end,
    load = function() return dummy end, loadfile = function() return function() return dummy end end,
  }, {__index = function(_, k) return dummy end})
  env.newEntity = function(t) emit(file, t); return t end
  env.newArtifact = env.newEntity
  env.newEntityRandom = function() return dummy end
  local fn, err = loadfile(file)
  if not fn then io.stderr:write("LOADERR ", file, " ", tostring(err), "\n") else
    setfenv(fn, env)
    local ok, e = pcall(fn)
    if not ok then io.stderr:write("RUNERR ", file, " ", tostring(e), "\n") end
  end
end
io.write(table.concat(out, "\n"), "\n")
