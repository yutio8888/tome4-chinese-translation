local source = "thalore wilder"
local source_tag = "entity name"
local target = "自然精灵自然师"
local cults_section = "tome-cults/data/zones/test/npcs.lua"

local function load_locale(path, runtime, matches)
  local current_section
  local environment = {}

  environment.section = function(value)
    current_section = value
  end
  environment.t = function(...)
    local arity = select("#", ...)
    local actual_source, actual_target, actual_tag, args_order, special = ...
    local record = {
      source = actual_source,
      target = actual_target,
      source_tag = actual_tag,
      args_order = args_order,
      special = special,
      section = current_section,
      arity = arity,
    }
    if actual_source == source and actual_tag == source_tag then
      matches[#matches + 1] = record
    end
    runtime[actual_source .. "\0" .. tostring(actual_tag)] = record
  end
  setmetatable(environment, {__index = _G})

  local chunk, load_error = loadfile(path)
  assert(chunk, load_error)
  setfenv(chunk, environment)
  local ok, run_error = pcall(chunk)
  assert(ok, run_error)
end

local function verify_single(path, expected_section)
  local runtime, matches = {}, {}
  load_locale(path, runtime, matches)
  assert(#matches == 1, path .. " match count: " .. #matches)
  local record = matches[1]
  assert(record.source == source)
  assert(record.target == target)
  assert(record.source_tag == source_tag)
  assert(record.args_order == nil)
  assert(record.special == nil)
  assert(record.arity == 3)
  if expected_section then assert(record.section == expected_section) end
  return record
end

local cults = verify_single("tome-cults.lua", cults_section)
local tome = verify_single("mod-tome.lua")

local function verify_order(first, second)
  local runtime, matches = {}, {}
  load_locale(first, runtime, matches)
  load_locale(second, runtime, matches)
  local record = assert(runtime[source .. "\0" .. source_tag])
  assert(record.target == target)
  assert(record.args_order == nil)
  assert(record.special == nil)
  return record.target
end

local tome_then_cults = verify_order("mod-tome.lua", "tome-cults.lua")
local cults_then_tome = verify_order("tome-cults.lua", "mod-tome.lua")

io.write("lua=", _VERSION, " jit=", jit.version, "\n")
io.write(
  "cults_matches=1 source=", cults.source,
  " target=", cults.target,
  " source_tag=", cults.source_tag,
  " args_order=nil special=nil arity=", cults.arity,
  " section=", cults.section, "\n"
)
io.write("tome_matches=1 target=", tome.target, " arity=", tome.arity, "\n")
io.write("order_tome_then_cults=", tome_then_cults, "\n")
io.write("order_cults_then_tome=", cults_then_tome, "\n")
