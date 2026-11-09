local cur = ""
local n = 0
local function j(s) return '"' .. s:gsub('[%c"\\]', function(c) if c == '"' then return '\\"' elseif c == "\\" then return "\\\\" elseif c == "\n" then return "\\n" elseif c == "\t" then return "\\t" else return string.format("\\u%04x", c:byte()) end end) .. '"' end
local env = setmetatable({}, {__index=function() return function() end end})
env.section = function(s) cur = s end
env.t = function(s, d, tag, order)
  n = n + 1
  io.write('{"i":', n, ',"sec":', j(cur), ',"en":', j(s), ',"zh":', j(d), ',"tag":', j(tostring(tag)), '}\n')
end
local fn = assert(loadfile(arg[1])); setfenv(fn, env); fn()
