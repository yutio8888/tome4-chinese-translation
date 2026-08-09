-- Confidential source broker. Only the generated tDef locale is exported.
-- Source text, paths, parser diagnostics, and directory listings never reach stdout/stderr.
-- The broker prevents accidental stdout/stderr leakage but is not a sandbox:
-- the extractor runs with the default Lua environment and must be trusted
-- with confidential source access.

local lfs = require "lfs"
local arguments = {...}
local mode = arguments[1]

local function stop(code)
	os.exit(code)
end

local function first_directory(offset)
	for index = offset, #arguments do
		local candidate = arguments[index]
		if type(candidate) == "string" and lfs.attributes(candidate, "mode") == "directory" then
			return candidate
		end
	end
	return nil
end

if mode == "probe" then
	stop(first_directory(2) and 0 or 10)
end

if mode ~= "extract" then stop(11) end
local extractor_file = arguments[2]
local output_file = arguments[3]
local logical_mount = arguments[4]
if type(extractor_file) ~= "string" or type(output_file) ~= "string" or
   type(logical_mount) ~= "string" or logical_mount == "" then
	stop(11)
end
logical_mount = logical_mount:gsub("%%", "%%%%")
local source_root = first_directory(5)
if not source_root then stop(10) end
source_root = source_root:gsub("([^/])/+$", "%1")
os.remove(output_file)

stop = function(code)
	os.remove("i18n_list.lua")
	os.exit(code)
end

os.remove("i18n_list.lua")
local real_os_exit = os.exit
os.exit = function(code)
	os.remove("i18n_list.lua")
	if code == nil or code == true or code == 0 then
		if lfs.attributes(output_file, "mode") ~= "file" then
			real_os_exit(24)
		end
	end
	if code == true then
		real_os_exit(0)
	elseif code == false then
		real_os_exit(1)
	else
		real_os_exit(code or 0)
	end
end
local parse_failed = false
local original_print = print
print = function(...)
	for index = 1, select("#", ...) do
		local value = tostring(select(index, ...)):gsub("\27%[[0-9;]*m", "")
		if value:find("^In file ") or
		   value:find("too many pending calls/choices", 1, true) or
		   value:find("empty loop in rule 'functioncall'", 1, true) then
			parse_failed = true
		end
	end
end

local chunk = loadfile(extractor_file)
if not chunk then
	print = original_print
	stop(20)
end
local ok = xpcall(function()
	chunk(source_root)
end, function()
	return false
end)
print = original_print
if not ok then stop(20) end
if parse_failed then stop(21) end

local input = io.open("i18n_list.lua", "rb")
if not input then stop(22) end
local size = input:seek("end")
if not size or size < 1 or size > 268435456 then
	input:close()
	stop(22)
end
input:seek("set", 0)
local data = input:read("*a")
input:close()
if type(data) ~= "string" or #data ~= size then stop(22) end

local function escape_pattern(value)
	return (value:gsub("([%(%)%.%%%+%-%*%?%[%]%^%$])", "%%%1"))
end
data = data:gsub(escape_pattern(source_root) .. "([/])", logical_mount .. "%1")
if data:find(source_root, 1, true) or data:find("/%.%./") then stop(23) end

local output = io.open(output_file, "wb")
if not output then stop(22) end
local write_ok, write_result = pcall(function()
	return output:write(data)
end)
local close_ok, close_result = pcall(function()
	return output:close()
end)
if not write_ok or not write_result or not close_ok or not close_result then
	os.remove(output_file)
	stop(22)
end
os.remove("i18n_list.lua")
stop(0)
