-- Execute a locale-like Lua file in a constrained environment and emit JSONL.
-- This script intentionally targets Lua 5.1/LuaJIT semantics.

local input_file, output_file = ...
assert(type(input_file) == "string", "input locale path is required")
assert(type(output_file) == "string", "output JSONL path is required")

local output = assert(io.open(output_file, "wb"))

local function json_quote(value)
	assert(type(value) == "string")
	local parts = {'"'}
	for index = 1, #value do
		local byte = value:byte(index)
		if byte == 34 then
			parts[#parts + 1] = '\\"'
		elseif byte == 92 then
			parts[#parts + 1] = '\\\\'
		elseif byte == 8 then
			parts[#parts + 1] = '\\b'
		elseif byte == 9 then
			parts[#parts + 1] = '\\t'
		elseif byte == 10 then
			parts[#parts + 1] = '\\n'
		elseif byte == 12 then
			parts[#parts + 1] = '\\f'
		elseif byte == 13 then
			parts[#parts + 1] = '\\r'
		elseif byte < 32 then
			parts[#parts + 1] = ("\\u%04x"):format(byte)
		else
			parts[#parts + 1] = string.char(byte)
		end
	end
	parts[#parts + 1] = '"'
	return table.concat(parts)
end

local function table_is_array(value)
	local count, maximum = 0, 0
	for key in pairs(value) do
		if type(key) ~= "number" or key < 1 or key % 1 ~= 0 then
			return false, 0
		end
		count = count + 1
		if key > maximum then maximum = key end
	end
	if count == 0 then
		return false, 0
	end
	return count == maximum, maximum
end

local json_encode
json_encode = function(value, seen)
	local value_type = type(value)
	if value_type == "nil" then
		return "null"
	elseif value_type == "boolean" then
		return value and "true" or "false"
	elseif value_type == "number" then
		if value ~= value or value == math.huge or value == -math.huge then
			error("non-finite number cannot be serialized")
		end
		return tostring(value)
	elseif value_type == "string" then
		return json_quote(value)
	elseif value_type ~= "table" then
		error("unsupported locale value type: " .. value_type)
	end

	seen = seen or {}
	if seen[value] then error("cyclic locale value") end
	seen[value] = true
	local is_array, maximum = table_is_array(value)
	local parts = {}
	if is_array then
		for index = 1, maximum do
			parts[index] = json_encode(value[index], seen)
		end
		seen[value] = nil
		return "[" .. table.concat(parts, ",") .. "]"
	end

	local keys = {}
	for key in pairs(value) do
		if type(key) ~= "string" then
			error("locale object key is not a string")
		end
		keys[#keys + 1] = key
	end
	table.sort(keys)
	for _, key in ipairs(keys) do
		parts[#parts + 1] = json_quote(key) .. ":" .. json_encode(value[key], seen)
	end
	seen[value] = nil
	return "{" .. table.concat(parts, ",") .. "}"
end

local function emit(record)
	output:write(json_encode(record), "\n")
end

local function caller_line()
	local info = debug.getinfo(3, "l")
	return info and info.currentline or 0
end

local current_section = ""
local environment = {}

environment.locale = function(name)
	if type(name) ~= "string" then error("locale name must be a string") end
	emit({kind = "locale", locale = name, line = caller_line()})
end

environment.section = function(name)
	if type(name) ~= "string" then error("section name must be a string") end
	current_section = name
	emit({kind = "section", section = name, line = caller_line()})
end

local function translation(kind, line, source, target, source_tag, args_order, special)
	if type(source) ~= "string" then error(kind .. " source must be a string") end
	if type(target) ~= "string" then error(kind .. " target must be a string") end
	emit({
		kind = "translation",
		function_name = kind,
		section = current_section,
		source = source,
		target = target,
		source_tag = source_tag,
		args_order = args_order,
		special = special,
		line = line,
	})
end

environment.t = function(...)
	return translation("t", caller_line(), ...)
end

environment.t_old = function(...)
	return translation("t_old", caller_line(), ...)
end

environment.tc = function(source, target)
	if type(source) ~= "string" or type(target) ~= "string" then
		error("tc values must be strings")
	end
	emit({
		kind = "casefold",
		section = current_section,
		source = source,
		target = target,
		line = caller_line(),
	})
end

environment.tDef = function(source_line, source, source_tag)
	if type(source_line) ~= "number" then error("tDef line must be a number") end
	if type(source) ~= "string" then error("tDef source must be a string") end
	emit({
		kind = "definition",
		section = current_section,
		source = source,
		source_tag = source_tag,
		source_line = source_line,
		line = caller_line(),
	})
end

-- Locale headers use these configuration calls. They do not affect the
-- translation map and are deliberately not exposed beyond no-op handlers.
environment.setFlag = function() end
environment.forceFontPackage = function() end

setmetatable(environment, {
	__index = function(_, key)
		error("unsupported global in locale file: " .. tostring(key), 2)
	end,
})

local chunk, load_error = loadfile(input_file)
if not chunk then
	output:close()
	io.stderr:write(load_error, "\n")
	os.exit(1)
end
setfenv(chunk, environment)
local ok, runtime_error = xpcall(chunk, debug.traceback)
local close_call_ok, close_ok, close_error = pcall(function()
	return output:close()
end)
if not close_call_ok or not close_ok then
	io.stderr:write(close_error or "failed to close output file", "\n")
	os.exit(1)
end
if not ok then
	io.stderr:write(runtime_error, "\n")
	os.exit(1)
end
