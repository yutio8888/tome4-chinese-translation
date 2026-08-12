"""Pinned-source extraction using the historical ToME4 Lua parser."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .config import ComponentSpec, ExtractorSpec, Manifest
from .errors import ExtractionError, ValidationError
from .git_source import GitRepository
from .identity import (
    ComponentIndex,
    SLOT_REGISTRY_RELATIVE_PATH,
    SlotRegistry,
    build_component_index,
    parse_enrichment_records,
    read_index_files,
    write_index_files,
)
from .locale_model import LocaleLoader
from .report import atomic_write_bytes, create_run_directory, write_json
from .runtime import LuaRuntime


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
KNOWN_PARSE_FAILURES = (
    "too many pending calls/choices",
    "empty loop in rule 'functioncall'",
)


def _enrichment_helpers(*, bucket_patched: bool) -> str:
    """Lua helpers appended to the staged extractor in --enrich mode.

    The sidecar is produced by the SAME Luafish AST traversal as
    i18n_list.lua (contract §4.3): every capture site is replaced with an
    enrichment_capture() call that mirrors the original locale bucket write
    byte-for-byte and appends one metadata record per occurrence.
    """
    bucket_init = (
        "locales[file] = locales[file] or new_locale_bucket()"
        if bucket_patched
        else "locales[file] = locales[file] or {}"
    )
    return f"""local enrichment = {{}}
local enrichment_NULL = {{}}
local function enrichment_json_escape(value)
\treturn (value:gsub("\\\\", "\\\\\\\\"):gsub('"', '\\\\"')
\t\t:gsub("\\n", "\\\\n"):gsub("\\r", "\\\\r"):gsub("\\t", "\\\\t")
\t\t:gsub("%c", function(character)
\t\t\treturn string.format("\\\\u%04x", string.byte(character))
\t\tend))
end
local function enrichment_json_encode(value)
\tif value == nil or value == enrichment_NULL then return "null" end
\tlocal kind = type(value)
\tif kind == "boolean" then return value and "true" or "false" end
\tif kind == "number" then
\t\tif value % 1 == 0 then return string.format("%d", value) end
\t\treturn string.format("%.14g", value)
\tend
\tif kind == "string" then return '"'..enrichment_json_escape(value)..'"' end
\tif kind ~= "table" then error("cannot encode enrichment value: "..kind) end
\tlocal keys, index, is_array = {{}}, 0, true
\tfor key in pairs(value) do keys[#keys+1] = key end
\ttable.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
\tfor _, key in ipairs(keys) do
\t\tif type(key) ~= "number" or key % 1 ~= 0 or key ~= index + 1 then
\t\t\tis_array = false
\t\t\tbreak
\t\tend
\t\tindex = key
\tend
\tlocal parts = {{}}
\tif is_array then
\t\tfor i = 1, index do parts[i] = enrichment_json_encode(value[i]) end
\t\treturn "["..table.concat(parts, ",").."]"
\tend
\tfor _, key in ipairs(keys) do
\t\tparts[#parts+1] = enrichment_json_encode(tostring(key))..":"..enrichment_json_encode(value[key])
\tend
\treturn "{{"..table.concat(parts, ",").."}}"
end
local function enrichment_capture(file, text, line, tag, meta)
\t{bucket_init}
\tlocales[file][text] = {{line=line, type=tag}}
\tif type(text) == "string" then
\t\tenrichment[#enrichment+1] = {{
\t\t\tschema_version = 1,
\t\t\tsection = file,
\t\t\tline = line,
\t\t\tsource = text,
\t\t\tsource_tag = tag,
\t\t\tentity_kind = meta.entity_kind,
\t\t\tanchor_hint = meta.anchor_hint,
\t\t\tast_path = meta.ast_path,
\t\t\textraction_confidence = meta.confidence,
\t\t}}
\tend
end
"""


_ENRICHMENT_SIDECAR_WRITER = """
local enrichment_output = os.getenv("I18N_ENRICHMENT")
if enrichment_output and enrichment_output ~= "" then
\tlocal enrichment_file = io.open(enrichment_output, "w")
\tif not enrichment_file then error("cannot open enrichment output file") end
\tfor _, record in ipairs(enrichment) do
\t\tenrichment_file:write(enrichment_json_encode(record), "\\n")
\tend
\tenrichment_file:close()
end
"""


def _apply_enrichment_patch(extractor: str, *, bucket_patched: bool) -> str:
    """Replace every locale capture site with the enrichment mirror.

    Each replacement must match the pinned official extractor exactly once
    (the log branches legitimately appear twice). A count mismatch fails
    closed: the enrichment patch is only valid for the pinned commit.
    """
    init = (
        "locales[file] = locales[file] or new_locale_bucket()"
        if bucket_patched
        else "locales[file] = locales[file] or {}"
    )
    NULL = "enrichment_NULL"
    replacements: list[tuple[str, str, int]] = [
        (
            f"\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][en[1][1]] = {{line=en[1].nline, type=tag}}",
            f'\t\t\t\t\t\t\t\t\t\tenrichment_capture(file, en[1][1], en[1].nline, tag, {{entity_kind="free", anchor_hint={NULL}, ast_path="_t", confidence="deterministic"}})',
            1,
        ),
        (
            f"\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][sn[1]] = {{line=sn.nline, type=\"tformat\"}}",
            f'\t\t\t\t\t\tenrichment_capture(file, sn[1], sn.nline, "tformat", {{entity_kind="free", anchor_hint={NULL}, ast_path="tformat", confidence="deterministic"}})',
            1,
        ),
        (
            f"\t\t\telseif e.tag == \"Id\" and newTalent_alias[e[1]] then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then for j, p in ipairs(en[1]) do\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"name\" then\n\t\t\t\t\t\tprint(colors(\"%{{bright green}}\".. e[1]), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"talent name\"}}\n\t\t\t\t\tend\n\t\t\t\tend end",
            f'\t\t\telseif e.tag == "Id" and newTalent_alias[e[1]] then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then\n\t\t\t\t\tlocal talent_name, talent_short, talent_type = {NULL}, {NULL}, {NULL}\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" then\n\t\t\t\t\t\t\tif p[1][1] == "name" and p[2].tag == "String" then talent_name = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "short_name" and p[2].tag == "String" then talent_short = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "type" and p[2].tag == "Table" then\n\t\t\t\t\t\t\t\tlocal type_array = {{}}\n\t\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\t\tif q.tag == "Field" and q[1] and q[1].tag == "Number" then\n\t\t\t\t\t\t\t\t\t\tlocal value = q[2]\n\t\t\t\t\t\t\t\t\t\tif value and value.tag == "String" then type_array[q[1][1]] = value[1]\n\t\t\t\t\t\t\t\t\t\telseif value and value.tag == "Number" then type_array[q[1][1]] = value[1]\n\t\t\t\t\t\t\t\t\t\telse type_array[q[1][1]] = {NULL} end\n\t\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\t\ttalent_type = type_array\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" then\n\t\t\t\t\t\t\tprint(colors("%{{bright green}}\".. e[1]), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "talent name", {{entity_kind="talent", anchor_hint={{name=talent_name, short_name=talent_short, type=talent_type, def_line=en.nline}}, ast_path="newTalent.name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\t\t\t\tprint(colors(\"%{{bright green}}newTalentType\"), cat)\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][cat] = {{line=p[2].nline, type=\"talent category\"}}",
            f'\t\t\t\t\t\tprint(colors("%{{bright green}}newTalentType"), cat)\n\t\t\t\t\t\tenrichment_capture(file, cat, p[2].nline, "talent category", {{entity_kind="talent_type", anchor_hint={{type=((p[2].tag == "String") and p[2][1] or {NULL}), def_line=en.nline}}, ast_path="newTalentType.type", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\telseif e.tag == \"Id\" and e[1] == \"newEntity\" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then for j, p in ipairs(en[1]) do\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"name\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"entity name\"}}\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"short_name\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"entity short_name\"}}\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"type\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"entity type\"}}\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"subtype\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"entity subtype\"}}\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"keywords\" then\n\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\tif q[1].tag == \"String\" then\n\t\t\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), q[1][1])\n\t\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\t\tlocales[file][q[1][1]] = {{line=p[2].nline, type=\"entity keyword\"}}\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"combat\" then\n\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\tif q.tag == \"Field\" and q[1].tag == \"String\" and q[1][1] == \"talented\" then\n\t\t\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), q[2][1])\n\t\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\t\tlocales[file][q[2][1]] = {{line=p[2].nline, type=\"entity combat talented\"}}\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"on_slot\" then\n\t\t\t\t\t\tif(p[2].tag == \"String\") then\n\t\t\t\t\t\t\tprint(colors(\"%{{green}}newEntity\"), p[2][1])\n\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"entity on slot\"}}\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend end",
            f'\t\t\telseif e.tag == "Id" and e[1] == "newEntity" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then\n\t\t\t\t\tlocal entity_name, entity_short, entity_type, entity_subtype = {NULL}, {NULL}, {NULL}, {NULL}\n\t\t\t\t\tlocal entity_define_as, entity_base = {NULL}, {NULL}\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[2].tag == "String" then\n\t\t\t\t\t\t\tif p[1][1] == "name" then entity_name = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "short_name" then entity_short = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "type" then entity_type = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "subtype" then entity_subtype = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "define_as" then entity_define_as = p[2][1]\n\t\t\t\t\t\t\telseif p[1][1] == "base" then entity_base = p[2][1]\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "base" and p[2].tag == "Table" then\n\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\tif q.tag == "Field" and q[2] and q[2].tag == "String" then\n\t\t\t\t\t\t\t\t\tentity_base = q[2][1]\n\t\t\t\t\t\t\t\t\tbreak\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\t\tlocal entity_anchor = {{define_as=entity_define_as, base=entity_base, name=entity_name, type=entity_type, subtype=entity_subtype, def_line=en.nline}}\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "entity name", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "short_name" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "entity short_name", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.short_name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "type" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "entity type", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.type", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "subtype" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "entity subtype", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.subtype", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "keywords" then\n\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\tif q[1].tag == "String" then\n\t\t\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), q[1][1])\n\t\t\t\t\t\t\t\t\tenrichment_capture(file, q[1][1], p[2].nline, "entity keyword", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.keyword", confidence="deterministic"}})\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "combat" then\n\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\tif q.tag == "Field" and q[1].tag == "String" and q[1][1] == "talented" then\n\t\t\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), q[2][1])\n\t\t\t\t\t\t\t\t\tenrichment_capture(file, q[2][1], p[2].nline, "entity combat talented", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.combat_talented", confidence=((q[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "on_slot" then\n\t\t\t\t\t\t\tif(p[2].tag == "String") then\n\t\t\t\t\t\t\t\tprint(colors("%{{green}}newEntity"), p[2][1])\n\t\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "entity on slot", {{entity_kind="entity", anchor_hint=entity_anchor, ast_path="newEntity.on_slot", confidence="deterministic"}})\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\telseif e.tag == \"Id\" and e[1] == \"newIngredient\" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then for j, p in ipairs(en[1]) do\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"name\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newIngredient\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"ingredient name\"}}\n\t\t\t\t\telseif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"type\" then\n\t\t\t\t\t\tprint(colors(\"%{{green}}newIngredient\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"ingredient type\"}}\n\t\t\t\t\tend\n\t\t\t\tend end",
            f'\t\t\telseif e.tag == "Id" and e[1] == "newIngredient" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then\n\t\t\t\t\tlocal ingredient_name = {NULL}\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" and p[2].tag == "String" then ingredient_name = p[2][1] end\n\t\t\t\t\tend\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newIngredient"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "ingredient name", {{entity_kind="ingredient", anchor_hint={{name=ingredient_name, def_line=en.nline}}, ast_path="newIngredient.name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\telseif p[1] and p[2] and p.tag == "Field" and p[1][1] == "type" then\n\t\t\t\t\t\t\tprint(colors("%{{green}}newIngredient"), p[2][1])\n\t\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "ingredient type", {{entity_kind="ingredient", anchor_hint={{name=ingredient_name, def_line=en.nline}}, ast_path="newIngredient.type", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"name\" then\n\t\t\t\t\t\tprint(colors(\"%{{bright red}}newAchievement\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"achievement name\"}}\n\t\t\t\t\tend",
            f'\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" then\n\t\t\t\t\t\tprint(colors("%{{bright red}}newAchievement"), p[2][1])\n\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "achievement name", {{entity_kind="achievement", anchor_hint={{name=((p[2].tag == "String") and p[2][1] or {NULL}), def_line=en.nline}}, ast_path="newAchievement.name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\telseif e.tag == \"Id\" and e[1] == \"newBirthDescriptor\" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tlocal dname, name = nil, nil\n\t\t\t\tif en then for j, p in ipairs(en[1]) do\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"name\" then\n\t\t\t\t\t\tname = p[2]\n\t\t\t\t\tend\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"display_name\" then\n\t\t\t\t\t\tdname = p[2]\n\t\t\t\t\tend\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"cosmetic_options\" then\n\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\tif q[1].tag == \"String\" then\n\t\t\t\t\t\t\t\tlocal name = q[1][1]:gsub(\"_\", \" \"):capitalize()\n\t\t\t\t\t\t\t\tprint(colors(\"%{{bright cyan}}newBirthDescriptor\"), name)\n\t\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\t\tlocales[file][name] = {{line=p[2].nline, type=\"birth facial category\"}}\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend end\n\t\t\t\tif dname then\n\t\t\t\t\tprint(colors(\"%{{bright cyan}}newBirthDescriptor\"), dname[1])\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][dname[1]] = {{line=dname.nline, type=\"birth descriptor name\"}}\n\t\t\t\telseif name then\n\t\t\t\t\tprint(colors(\"%{{bright cyan}}newBirthDescriptor\"), name[1])\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][name[1]] = {{line=name.nline, type=\"birth descriptor name\"}}\n\t\t\t\tend",
            f'\t\t\telseif e.tag == "Id" and e[1] == "newBirthDescriptor" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tlocal dname, name = nil, nil\n\t\t\t\tif en then\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" then\n\t\t\t\t\t\t\tname = p[2]\n\t\t\t\t\t\tend\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "display_name" then\n\t\t\t\t\t\t\tdname = p[2]\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\t\tlocal birth_anchor_name = {NULL}\n\t\t\t\t\tif dname and dname.tag == "String" and dname[1] then birth_anchor_name = dname[1]\n\t\t\t\t\telseif name and name.tag == "String" and name[1] then birth_anchor_name = name[1] end\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "cosmetic_options" then\n\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\tif q[1].tag == "String" then\n\t\t\t\t\t\t\t\t\tlocal facial_name = q[1][1]:gsub("_", " "):capitalize()\n\t\t\t\t\t\t\t\t\tprint(colors("%{{bright cyan}}newBirthDescriptor"), facial_name)\n\t\t\t\t\t\t\t\t\tenrichment_capture(file, facial_name, p[2].nline, "birth facial category", {{entity_kind="birth", anchor_hint={{name=birth_anchor_name, def_line=en.nline}}, ast_path="newBirthDescriptor.facial_category", confidence="deterministic"}})\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend\n\t\t\t\tif dname then\n\t\t\t\t\tprint(colors("%{{bright cyan}}newBirthDescriptor"), dname[1])\n\t\t\t\t\tenrichment_capture(file, dname[1], dname.nline, "birth descriptor name", {{entity_kind="birth", anchor_hint={{name=birth_anchor_name, def_line=en.nline}}, ast_path="newBirthDescriptor.name", confidence=((dname.tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\telseif name then\n\t\t\t\t\tprint(colors("%{{bright cyan}}newBirthDescriptor"), name[1])\n\t\t\t\t\tenrichment_capture(file, name[1], name.nline, "birth descriptor name", {{entity_kind="birth", anchor_hint={{name=birth_anchor_name, def_line=en.nline}}, ast_path="newBirthDescriptor.name", confidence=((name.tag == "String") and "deterministic" or "nondeterministic")}})\n\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\t\t\t{init}\n\t\t\t\t\tprint(colors(\"%{{cyan}}newGem\"), name)\n\t\t\t\t\tlocales[file][name] = {{line=en.nline, type=\"gem name\"}}\n\t\t\t\t\tprint(colors(\"%{{cyan}}newGem\"), a_name)\n\t\t\t\t\tlocales[file][a_name] = {{line=en.nline, type=\"alchemist gem\"}}\n\t\t\t\t\tprint(colors(\"%{{cyan}}newGem\"), subtype)\n\t\t\t\t\tlocales[file][subtype] = {{line=en.nline, type=\"gem subtype\"}}",
            f'\t\t\t\t\tprint(colors("%{{cyan}}newGem"), name)\n\t\t\t\t\tenrichment_capture(file, name, en.nline, "gem name", {{entity_kind="gem", anchor_hint={{name=en[1][1], def_line=en.nline}}, ast_path="newGem.name", confidence="deterministic"}})\n\t\t\t\t\tprint(colors("%{{cyan}}newGem"), a_name)\n\t\t\t\t\tenrichment_capture(file, a_name, en.nline, "alchemist gem", {{entity_kind="gem", anchor_hint={{name=en[1][1], def_line=en.nline}}, ast_path="newGem.alchemist", confidence="deterministic"}})\n\t\t\t\t\tprint(colors("%{{cyan}}newGem"), subtype)\n\t\t\t\t\tenrichment_capture(file, subtype, en.nline, "gem subtype", {{entity_kind="gem", anchor_hint={{name=en[1][1], def_line=en.nline}}, ast_path="newGem.subtype", confidence="deterministic"}})',
            1,
        ),
        (
            f"\t\t\telseif e.tag == \"Id\" and e[1] == \"newEffect\" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then for j, p in ipairs(en[1]) do\n\t\t\t\t\tif p[1] and p[2] and p.tag == \"Field\" and p[1][1] == \"subtype\" then\n\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\tif q[1].tag == \"String\" then\n\t\t\t\t\t\t\t\tprint(colors(\"%{{yellow}}newEffect\"), q[1][1])\n\t\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\t\tlocales[file][q[1][1]] = {{line=p[2].nline, type=\"effect subtype\"}}\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend end",
            f'\t\t\telseif e.tag == "Id" and e[1] == "newEffect" then\n\t\t\t\tlocal en = ast[i+1]\n\t\t\t\tif en then\n\t\t\t\t\tlocal effect_name = {NULL}\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "name" and p[2].tag == "String" then\n\t\t\t\t\t\t\teffect_name = p[2][1]\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\t\tfor j, p in ipairs(en[1]) do\n\t\t\t\t\t\tif p[1] and p[2] and p.tag == "Field" and p[1][1] == "subtype" then\n\t\t\t\t\t\t\tfor _, q in ipairs(p[2]) do\n\t\t\t\t\t\t\t\tif q[1].tag == "String" then\n\t\t\t\t\t\t\t\t\tprint(colors("%{{yellow}}newEffect"), q[1][1])\n\t\t\t\t\t\t\t\t\tenrichment_capture(file, q[1][1], p[2].nline, "effect subtype", {{entity_kind="effect", anchor_hint={{name=effect_name, def_line=en.nline}}, ast_path="newEffect.subtype", confidence="deterministic"}})\n\t\t\t\t\t\t\t\tend\n\t\t\t\t\t\t\tend\n\t\t\t\t\t\tend\n\t\t\t\t\tend\n\t\t\t\tend',
            1,
        ),
        (
            f"\t\t\t\t\t\tprint(colors(\"%{{yellow}}floorEffect\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"floorEffect desc\"}}",
            f'\t\t\t\t\t\tprint(colors("%{{yellow}}floorEffect"), p[2][1])\n\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "floorEffect desc", {{entity_kind="free", anchor_hint={NULL}, ast_path="floorEffect.desc", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\t\t\t\tprint(colors(\"%{{red}}newLore\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"newLore category\"}}",
            f'\t\t\t\t\t\tprint(colors("%{{red}}newLore"), p[2][1])\n\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "newLore category", {{entity_kind="lore", anchor_hint={{category=((p[2].tag == "String") and p[2][1] or {NULL}), def_line=en.nline}}, ast_path="newLore.category", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\t\t\t\t\tprint(colors(\"%{{bright red}}load_tips\"), text)\n\t\t\t\t\t\t\t{init}\n\t\t\t\t\t\t\tlocales[file][text] = {{line=p[2].nline, type=\"init.lua load_tips\"}}",
            f'\t\t\t\t\t\t\tprint(colors("%{{bright red}}load_tips"), text)\n\t\t\t\t\t\t\tenrichment_capture(file, text, p[2].nline, "init.lua load_tips", {{entity_kind="free", anchor_hint={NULL}, ast_path="load_tips.text", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\t\t\tprint(colors(\"%{{bright red}}init.lua description\"), text)\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][text] = {{line=en.nline, type=\"init.lua description\"}}",
            f'\t\t\t\t\tprint(colors("%{{bright red}}init.lua description"), text)\n\t\t\t\t\tenrichment_capture(file, text, en.nline, "init.lua description", {{entity_kind="free", anchor_hint={NULL}, ast_path="init.description", confidence=((en[1].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\t\t\tprint(colors(\"%{{bright red}}init.lua long_name\"), text)\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][text] = {{line=en.nline, type=\"init.lua long_name\"}}",
            f'\t\t\t\t\tprint(colors("%{{bright red}}init.lua long_name"), text)\n\t\t\t\t\tenrichment_capture(file, text, en.nline, "init.lua long_name", {{entity_kind="free", anchor_hint={NULL}, ast_path="init.long_name", confidence=((en[1].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
        (
            f"\t\t\t\t\tprint(colors(\"%{{blue}}defineStat\"), en[1][1])\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][en[1][1]] = {{line=e.nline, type=\"stat name\"}}\n\t\t\t\t\tprint(colors(\"%{{blue}}defineStat\"), en[2][1])\n\t\t\t\t\t{init}\n\t\t\t\t\tlocales[file][en[2][1]] = {{line=e.nline, type=\"stat short_name\"}}",
            f'\t\t\t\t\tprint(colors("%{{blue}}defineStat"), en[1][1])\n\t\t\t\t\tenrichment_capture(file, en[1][1], e.nline, "stat name", {{entity_kind="stat", anchor_hint={{stat_short_name=en[2][1], def_line=e.nline}}, ast_path="defineStat.name", confidence="deterministic"}})\n\t\t\t\t\tprint(colors("%{{blue}}defineStat"), en[2][1])\n\t\t\t\t\tenrichment_capture(file, en[2][1], e.nline, "stat short_name", {{entity_kind="stat", anchor_hint={{stat_short_name=en[2][1], def_line=e.nline}}, ast_path="defineStat.short_name", confidence="deterministic"}})',
            1,
        ),
        (
            f"\t\t\t\t\t\tprint(colors(\"%{{bright blue}}\"..log_type), en[order][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][en[order][1]] = {{line=en[order].nline, type=log_type}}",
            f'\t\t\t\t\t\tprint(colors("%{{bright blue}}"..log_type), en[order][1])\n\t\t\t\t\t\tenrichment_capture(file, en[order][1], en[order].nline, log_type, {{entity_kind="free", anchor_hint={NULL}, ast_path=log_type, confidence="deterministic"}})',
            2,
        ),
        (
            f"\t\t\t\t\t\tprint(colors(\"%{{blue}}newFaction\"), p[2][1])\n\t\t\t\t\t\t{init}\n\t\t\t\t\t\tlocales[file][p[2][1]] = {{line=p[2].nline, type=\"faction name\"}}",
            f'\t\t\t\t\t\tprint(colors("%{{blue}}newFaction"), p[2][1])\n\t\t\t\t\t\tenrichment_capture(file, p[2][1], p[2].nline, "faction name", {{entity_kind="faction", anchor_hint={{name=((p[2].tag == "String") and p[2][1] or {NULL}), def_line=en.nline}}, ast_path="Faction.add.name", confidence=((p[2].tag == "String") and "deterministic" or "nondeterministic")}})',
            1,
        ),
    ]
    patched = extractor
    for old, new, expected in replacements:
        count = patched.count(old)
        if count != expected:
            raise ExtractionError(
                f"enrichment patch site mismatch (expected {expected}, "
                f"found {count}): {old[:80]!r}..."
            )
        patched = patched.replace(old, new)
    # Sidecar writer after the i18n_list.lua write.
    if patched.count("f:close()") != 1:
        raise ExtractionError("cannot locate extractor output close")
    patched = patched.replace(
        "f:close()", "f:close()\n" + _ENRICHMENT_SIDECAR_WRITER, 1
    )
    return patched


def _patch_extractor(
    extractor_root: Path, spec: ExtractorSpec, *, enrich: bool = False
) -> dict[str, Any]:
    parser_path = extractor_root / "luafish" / "parser.lua"
    extractor_path = extractor_root / "i18n_extractor.lua"
    try:
        parser = parser_path.read_text(encoding="utf-8")
        extractor = extractor_path.read_text(encoding="utf-8")
    except OSError as error:
        raise ExtractionError(f"cannot read staged extractor: {error}") from error

    require_line = "local lpeg = require 'lpeg'\n"
    if parser.count(require_line) != 1:
        raise ExtractionError("cannot locate unique LPeg import in staged parser")
    parser = parser.replace(
        require_line,
        require_line + f"lpeg.setmaxstack({spec.max_stack})\n",
        1,
    )
    parser_path.write_text(parser, encoding="utf-8", newline="\n")

    duplicate_patch_applied = False
    if spec.preserve_duplicate_occurrences:
        locale_declaration = "local locales = {}\n"
        if extractor.count(locale_declaration) != 1:
            raise ExtractionError("cannot locate locale table in staged extractor")
        bucket_helper = """local locales = {}
local function new_locale_bucket()
\treturn setmetatable({}, {
\t\t__newindex = function(bucket, key, value)
\t\t\tif type(key) == \"string\" and type(value) == \"table\" then
\t\t\t\tvalue.__i18n_source = key
\t\t\t\trawset(bucket, #bucket + 1, value)
\t\t\telse
\t\t\t\trawset(bucket, key, value)
\t\t\tend
\t\tend,
\t})
end
"""
        if enrich:
            bucket_helper += _enrichment_helpers(bucket_patched=True)
        extractor = extractor.replace(locale_declaration, bucket_helper, 1)
        old_initializer = "locales[file] = locales[file] or {}"
        initializer_count = extractor.count(old_initializer)
        if initializer_count < 1:
            raise ExtractionError("cannot locate locale buckets in staged extractor")
        extractor = extractor.replace(
            old_initializer, "locales[file] = locales[file] or new_locale_bucket()"
        )
        old_output = """\tlocal list = {}
\tfor k, v in pairs(locales[section]) do
\t\tif type(k) == \"string\" then
\t\t\tlist[#list+1] = {text=k, line=v.line, type=v.type}
\t\tend
\tend
"""
        new_output = """\tlocal list = {}
\tfor _, v in ipairs(locales[section]) do
\t\tif type(v) == \"table\" and type(v.__i18n_source) == \"string\" then
\t\t\tlist[#list+1] = {text=v.__i18n_source, line=v.line, type=v.type}
\t\tend
\tend
"""
        if extractor.count(old_output) != 1:
            raise ExtractionError("cannot locate extractor output loop")
        extractor = extractor.replace(old_output, new_output, 1)
        extractor_path.write_text(extractor, encoding="utf-8", newline="\n")
        duplicate_patch_applied = True

    enrichment_patch_applied = False
    if enrich:
        if duplicate_patch_applied:
            # Helpers were appended to the bucket replacement above.
            pass
        else:
            locale_declaration = "local locales = {}\n"
            if extractor.count(locale_declaration) != 1:
                raise ExtractionError("cannot locate locale table in staged extractor")
            extractor = extractor.replace(
                locale_declaration,
                "local locales = {}\n" + _enrichment_helpers(bucket_patched=False),
                1,
            )
        extractor = _apply_enrichment_patch(
            extractor, bucket_patched=duplicate_patch_applied
        )
        extractor_path.write_text(extractor, encoding="utf-8", newline="\n")
        enrichment_patch_applied = True

    report = {
        "max_stack": spec.max_stack,
        "duplicate_occurrences_preserved": duplicate_patch_applied,
        "parser_sha256": hashlib.sha256(parser_path.read_bytes()).hexdigest(),
        "extractor_sha256": hashlib.sha256(extractor_path.read_bytes()).hexdigest(),
    }
    if enrichment_patch_applied:
        # Zero-breakage §3.3: the default (non-enrich) report is byte-identical.
        report["enrichment_patch_applied"] = True
    return report


def _minimal_mounts(component: ComponentSpec) -> list[str]:
    mounts = sorted(
        {PurePosixPath(source.mount) for source in component.sources},
        key=lambda value: (len(value.parts), value.as_posix()),
    )
    selected: list[PurePosixPath] = []
    for mount in mounts:
        if any(parent == mount or parent in mount.parents for parent in selected):
            continue
        selected.append(mount)
    return [mount.as_posix() for mount in selected]


def _clean_log_lines(log: str) -> list[str]:
    return [ANSI_RE.sub("", line).rstrip() for line in log.splitlines()]


def _protected_source_candidates(
    manifest: Manifest, component: ComponentSpec
) -> list[Path]:
    protected = component.protected_source
    if protected is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    configured = os.environ.get(protected.path_env)
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            raise ExtractionError(f"{protected.path_env} must be an absolute path")
        return [Path(os.path.normpath(str(candidate)))]
    root = manifest.protected_root_path(protected.root)
    return [root / candidate for candidate in protected.directory_candidates]


def _run_protected_extractor(
    manifest: Manifest,
    runtime: LuaRuntime,
    component: ComponentSpec,
    *,
    extractor_root: Path,
    stage: Path,
    timeout: int,
    extra_env: dict[str, str] | None = None,
) -> tuple[Path, list[str]]:
    protected = component.protected_source
    if protected is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    broker = manifest.root / "tools" / "lua" / "protected_extract.lua"
    output_file = stage / "protected_i18n_list.lua"
    result = runtime.run_protected(
        [
            broker,
            "extract",
            extractor_root / "i18n_extractor.lua",
            output_file,
            protected.mount,
            *_protected_source_candidates(manifest, component),
        ],
        cwd=stage,
        lua_paths=[extractor_root],
        timeout=timeout,
        extra_env=extra_env,
    )
    failures = {
        10: "declared protected source is unavailable",
        11: "protected extractor contract is invalid",
        20: "protected Lua extraction failed",
        21: "protected Lua parser reported a source parse failure",
        22: "protected extractor produced no valid text artifact",
        23: "protected extractor could not redact its source path",
    }
    if result.returncode != 0:
        reason = failures.get(result.returncode, "protected Lua extraction failed")
        raise ExtractionError(f"{component.id}: {reason}")
    if not output_file.is_file():
        raise ExtractionError(
            f"{component.id}: protected extractor produced no text artifact"
        )
    return output_file, [protected.mount]


def probe_protected_component(
    manifest: Manifest, runtime: LuaRuntime, component: ComponentSpec
) -> bool:
    if component.protected_source is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    broker = manifest.root / "tools" / "lua" / "protected_extract.lua"
    with tempfile.TemporaryDirectory(prefix="tome4-i18n-protected-probe-") as temporary:
        result = runtime.run_protected(
            [
                broker,
                "probe",
                *_protected_source_candidates(manifest, component),
            ],
            cwd=Path(temporary),
            timeout=30,
        )
    if result.returncode == 0:
        return True
    if result.returncode == 10:
        return False
    raise ExtractionError(
        f"{component.id}: protected source probe failed closed"
    )


def _normalized_definitions(
    *,
    component: str,
    records: Iterable[Any],
    origin_kind: str,
) -> list[dict[str, Any]]:
    if not isinstance(component, str) or not component:
        raise ExtractionError(
            "extraction field 'component' must be a non-empty string"
        )
    if (
        not isinstance(origin_kind, str)
        or origin_kind not in ("extracted", "manual")
    ):
        raise ExtractionError(
            "extraction field 'origin_kind' must be 'extracted' or 'manual'"
        )

    normalized: list[dict[str, Any]] = []
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ExtractionError(
                f"extraction record {position} must be an object"
            )
        if record.get("kind") != "definition":
            continue

        section = record.get("section")
        if not isinstance(section, str) or not section:
            raise ExtractionError(
                f"extraction record {position} field 'section' must be a "
                "non-empty string"
            )
        source = record.get("source")
        if not isinstance(source, str):
            raise ExtractionError(
                f"extraction record {position} field 'source' must be a "
                "string"
            )
        if not source and origin_kind == "manual":
            raise ExtractionError(
                f"extraction record {position} field 'source' must be a "
                "non-empty string for manual definitions"
            )
        # The historical extractor emits real records for _t"" and similar
        # placeholders. Keep them in raw snapshots so frozen hashes remain stable.
        source_tag = record.get("source_tag")
        if source_tag is not None and not isinstance(source_tag, str):
            raise ExtractionError(
                f"extraction record {position} field 'source_tag' must be a "
                "string or null"
            )
        source_line = record.get("source_line")
        if type(source_line) is not int:
            raise ExtractionError(
                f"extraction record {position} field 'source_line' must be an "
                "exact integer"
            )
        if source_line < 1:
            if origin_kind == "manual" and source_line == 0:
                origin_line = None
            else:
                sentinel_note = (
                    "manual definitions may use only 0 as the "
                    "unknown-line sentinel"
                    if origin_kind == "manual"
                    else "only manual definitions may use 0 as the "
                    "unknown-line sentinel"
                )
                raise ExtractionError(
                    f"extraction record {position} field 'source_line' must be "
                    f"greater than or equal to 1; {sentinel_note}"
                )
        else:
            origin_line = source_line
        logical_path = record.get("logical_path")
        if logical_path is not None and not isinstance(logical_path, str):
            raise ExtractionError(
                f"extraction record {position} field 'logical_path' must be a "
                "string or null"
            )

        normalized.append(
            {
                "component": component,
                "section": section,
                "source": source,
                "source_tag": source_tag,
                "origin_line": origin_line,
                "origin_kind": origin_kind,
                "origin_document": logical_path,
            }
        )
    return normalized


def _protected_source_root(
    manifest: Manifest, component: ComponentSpec
) -> str | None:
    """First existing candidate directory, normalized exactly like the broker."""
    if component.protected_source is None:
        return None
    for candidate in _protected_source_candidates(manifest, component):
        if candidate.is_dir():
            return re.sub(r"([^/])/+$", r"\1", str(candidate))
    return None


def _redact_enrichment_sections(
    records: list[dict[str, Any]],
    *,
    source_root: str,
    mount: str,
    component: str,
) -> list[dict[str, Any]]:
    """Mirror the protected broker's section redaction for the sidecar."""
    pattern = re.compile(re.escape(source_root) + r"(/)")
    redacted: list[dict[str, Any]] = []
    for record in records:
        section = record["section"]
        if source_root in section:
            record["section"] = pattern.sub(mount + r"\1", section)
        elif not section.startswith(mount + "/"):
            raise ExtractionError(
                f"{component}: enrichment section is neither redactable nor "
                f"mount-based: {section!r}"
            )
        if source_root in record["section"]:
            raise ExtractionError(
                f"{component}: enrichment section redaction failed: "
                f"{record['section']!r}"
            )
        redacted.append(record)
    return redacted


def _load_slot_registry(manifest: Manifest) -> SlotRegistry:
    return SlotRegistry.load(manifest.root / SLOT_REGISTRY_RELATIVE_PATH)


def _store_enrichment_artifacts(
    *,
    manifest: Manifest,
    component: ComponentSpec,
    component_directory: Path,
    sidecar_records: list[dict[str, Any]],
    source_root: str | None,
) -> dict[str, Any]:
    """Persist redacted sidecar + TU index + entities and update caches."""
    if source_root is not None and component.protected_source is not None:
        sidecar_records = _redact_enrichment_sections(
            sidecar_records,
            source_root=source_root,
            mount=component.protected_source.mount,
            component=component.id,
        )
    from .snapshot import read_snapshot

    snapshot = read_snapshot(
        component_directory / "snapshot.jsonl", expected_component=component.id
    )
    records = parse_enrichment_records(
        sidecar_records, source_label=component.id
    )
    slot_registry = _load_slot_registry(manifest)
    index = build_component_index(
        component=component.id,
        snapshot=snapshot,
        enrichment_records=records,
        slot_registry=slot_registry,
    )
    atomic_write_bytes(
        component_directory / "enrichment.jsonl",
        b"".join(
            (
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            ).encode("utf-8")
            for record in sidecar_records
        ),
    )
    write_index_files(component_directory, index)
    write_json(component_directory / "identity.json", index.to_dict())

    current = (
        manifest.root / ".artifacts" / "i18n" / "identity" / "current" / component.id
    )
    current.mkdir(parents=True, exist_ok=True)
    atomic_write_bytes(
        current / "enrichment.jsonl",
        (component_directory / "enrichment.jsonl").read_bytes(),
    )
    write_index_files(current, index)
    write_json(current / "identity.json", index.to_dict())

    from .storage import rebuild_identity_database

    indexes: list[ComponentIndex] = []
    for sibling in sorted(current.parent.iterdir()):
        if not sibling.is_dir():
            continue
        try:
            indexes.append(
                read_index_files(
                    component=sibling.name,
                    entities_path=sibling / "entities.jsonl",
                    tu_index_path=sibling / "tu_index.jsonl",
                )
            )
        except (OSError, ValidationError):
            continue
    from .baseline import baseline_directory, read_baseline

    baselines: list[Any] = []
    for baseline_path in sorted(baseline_directory(manifest.root).glob("*.jsonl")) if baseline_directory(manifest.root).is_dir() else []:
        name = baseline_path.name
        # tome-<commit>.jsonl
        if not name.endswith(".jsonl"):
            continue
        stem = name[: -len(".jsonl")]
        if "-" not in stem:
            continue
        component_name, commit = stem.split("-", 1)
        try:
            baselines.append(
                read_baseline(
                    manifest.root,
                    component=component_name,
                    translation_commit=commit,
                )
            )
        except ValidationError:
            continue
    storage_report = rebuild_identity_database(manifest.root, indexes, baselines)
    return {
        "identity": index.to_dict(),
        "identity_storage": storage_report.to_dict(),
    }


def extract_components(
    manifest: Manifest,
    runtime: LuaRuntime,
    components: Iterable[ComponentSpec],
    *,
    timeout: int,
    enrich: bool = False,
    commit_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    if type(timeout) is not int or timeout < 1:
        raise ExtractionError("timeout must be a positive integer")
    overrides = dict(commit_overrides or {})

    selected: list[ComponentSpec] = []
    seen_ids: set[str] = set()
    for component in components:
        if component.id in seen_ids:
            continue
        seen_ids.add(component.id)
        selected.append(component)
    if not selected:
        raise ExtractionError("no extractable components selected")
    for component in selected:
        has_public_source = (
            component.source_repository is not None and bool(component.sources)
        )
        if not has_public_source and component.protected_source is None:
            raise ExtractionError(
                f"component {component.id!r} has no pinned source mapping"
            )

    extractor_repo_path = manifest.repository_path(manifest.extractor.repository)
    extractor_repository = GitRepository(extractor_repo_path)
    extractor_repository.validate(manifest.extractor.commit, check_worktree=False)
    loader = LocaleLoader(runtime)
    run_directory = create_run_directory(manifest.root, "extract")
    component_reports: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="tome4-i18n-extract-") as temporary:
        temporary_root = Path(temporary)
        tool_stage = temporary_root / "tool"
        extractor_repository.materialize_lua_tree(
            manifest.extractor.commit,
            manifest.extractor.git_path,
            tool_stage,
            mount="i18n_tools",
        )
        extractor_root = tool_stage / "i18n_tools"
        patch_report = _patch_extractor(
            extractor_root, manifest.extractor, enrich=enrich
        )
        enrichment_env = (
            {"I18N_ENRICHMENT": "i18n_enrichment.jsonl"} if enrich else None
        )

        for component in selected:
            stage = temporary_root / f"component-{component.id}"
            stage.mkdir(parents=True)
            protected_access = component.protected_source is not None
            combined_log: str | None = None
            repository_name: str | None = None
            source_commit: str | None = None
            source_file_count: int | None = None
            if protected_access:
                if overrides:
                    raise ExtractionError(
                        f"{component.id}: commit overrides are not supported "
                        "for protected sources"
                    )
                output_file, mounts = _run_protected_extractor(
                    manifest,
                    runtime,
                    component,
                    extractor_root=extractor_root,
                    stage=stage,
                    timeout=timeout,
                    extra_env=enrichment_env,
                )
            else:
                repository_name = component.source_repository
                assert repository_name is not None
                repository_spec = manifest.repositories[repository_name]
                source_commit = overrides.get(
                    repository_name, repository_spec.commit
                )
                if source_commit != repository_spec.commit and component.source_baseline is not None:
                    raise ExtractionError(
                        f"{component.id}: commit override is not supported for "
                        "components with a protected source baseline"
                    )
                repository = GitRepository(manifest.repository_path(repository_name))
                repository.validate(source_commit, check_worktree=False)
                source_file_count = 0
                for source in component.sources:
                    source_file_count += repository.materialize_lua_tree(
                        source_commit,
                        source.git_path,
                        stage,
                        mount=source.mount,
                    )
                mounts = _minimal_mounts(component)
                extractor_result = runtime.run(
                    [extractor_root / "i18n_extractor.lua", *mounts],
                    cwd=stage,
                    lua_paths=[extractor_root],
                    timeout=timeout,
                    extra_env=enrichment_env,
                )
                combined_log = extractor_result.stdout
                if extractor_result.stderr:
                    combined_log += (
                        "\n"
                        if combined_log and not combined_log.endswith("\n")
                        else ""
                    ) + extractor_result.stderr
                clean_lines = _clean_log_lines(combined_log)
                parse_failures = [
                    line for line in clean_lines if line.startswith("In file ")
                ]
                known_failures = [
                    line
                    for line in clean_lines
                    if any(marker in line for marker in KNOWN_PARSE_FAILURES)
                ]
                output_file = stage / "i18n_list.lua"
                if extractor_result.returncode != 0:
                    raise ExtractionError(
                        f"extractor failed for {component.id} with exit code "
                        f"{extractor_result.returncode}: "
                        f"{extractor_result.stderr.strip() or extractor_result.stdout[-2000:]}"
                    )
                if parse_failures or known_failures:
                    sample = (parse_failures + known_failures)[:10]
                    raise ExtractionError(
                        f"extractor reported parse failures for {component.id}: "
                        + " | ".join(sample)
                    )
                if not output_file.is_file():
                    raise ExtractionError(
                        f"extractor produced no i18n_list.lua for {component.id}"
                    )
            try:
                extracted_document = loader.load_path(
                    output_file,
                    logical_path=f"generated:{component.id}/i18n_list.lua",
                )
            except ValidationError as error:
                raise ExtractionError(str(error)) from error
            definitions = _normalized_definitions(
                component=component.id,
                records=extracted_document.records,
                origin_kind="extracted",
            )
            if not definitions:
                raise ExtractionError(
                    f"extractor produced zero tDef entries for {component.id}"
                )

            extracted_tdef_count = len(definitions)
            manual_tdef_count = 0
            if component.id == "engine":
                for manual_path in manifest.manual_definitions:
                    manual_document = loader.load_path(
                        manifest.root / manual_path,
                        logical_path=manual_path,
                    )
                    manual_definitions = _normalized_definitions(
                        component=component.id,
                        records=manual_document.records,
                        origin_kind="manual",
                    )
                    definitions.extend(manual_definitions)
                    manual_tdef_count += len(manual_definitions)

            snapshot_data = b"".join(
                (
                    json.dumps(
                        definition,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                    + b"\n"
                )
                for definition in definitions
            )
            snapshot_sha256 = hashlib.sha256(snapshot_data).hexdigest()
            if component.source_baseline is not None:
                baseline = component.source_baseline
                if snapshot_sha256 != baseline.snapshot_sha256:
                    raise ExtractionError(
                        f"protected baseline snapshot mismatch for {component.id}: "
                        f"{snapshot_sha256} != {baseline.snapshot_sha256}"
                    )
                if len(definitions) != baseline.tdef_count:
                    raise ExtractionError(
                        f"protected baseline count mismatch for {component.id}: "
                        f"{len(definitions)} != {baseline.tdef_count}"
                    )
            component_directory = run_directory / component.id
            atomic_write_bytes(component_directory / "snapshot.jsonl", snapshot_data)
            atomic_write_bytes(
                component_directory / "i18n_list.lua", output_file.read_bytes()
            )
            identity_report: dict[str, Any] | None = None
            if enrich:
                sidecar_path = stage / "i18n_enrichment.jsonl"
                if not sidecar_path.is_file():
                    raise ExtractionError(
                        f"extractor produced no enrichment sidecar for {component.id}"
                    )
                try:
                    sidecar_data = json.loads(
                        "["
                        + ",".join(
                            line
                            for line in sidecar_path.read_text(
                                encoding="utf-8"
                            ).splitlines()
                            if line
                        )
                        + "]"
                    )
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
                    raise ExtractionError(
                        f"invalid enrichment sidecar for {component.id}: {error}"
                    ) from error
                identity_report = _store_enrichment_artifacts(
                    manifest=manifest,
                    component=component,
                    component_directory=component_directory,
                    sidecar_records=sidecar_data,
                    source_root=(
                        _protected_source_root(manifest, component)
                        if protected_access
                        else None
                    ),
                )
            component_report = {
                "component": component.id,
                "source_access": (
                    "lua-extractor-only" if protected_access else "pinned-git-object"
                ),
                "source_repository": repository_name,
                "source_commit": source_commit,
                "source_lua_files": source_file_count,
                "mounts": mounts,
                "tdef_count": len(definitions),
                "extracted_tdef_count": extracted_tdef_count,
                "manual_tdef_count": manual_tdef_count,
                "snapshot_sha256": snapshot_sha256,
                "snapshot": str(component_directory / "snapshot.jsonl"),
                "raw_i18n_list": str(component_directory / "i18n_list.lua"),
                "log": None,
            }
            if combined_log is not None:
                log_path = component_directory / "extract.log"
                atomic_write_bytes(log_path, combined_log.encode("utf-8"))
                component_report["log"] = str(log_path)
            if identity_report is not None:
                component_report["identity"] = identity_report["identity"]
                component_report["identity_storage"] = identity_report[
                    "identity_storage"
                ]
            write_json(component_directory / "metadata.json", component_report)
            component_reports.append(component_report)

    report: dict[str, Any] = {
        "ok": True,
        "version": manifest.version,
        "manifest": str(manifest.path),
        "extractor": {
            "repository": str(extractor_repo_path),
            "commit": manifest.extractor.commit,
            **patch_report,
        },
        "components": component_reports,
        "run_directory": str(run_directory),
    }
    if enrich:
        report["enrichment"] = True
    write_json(run_directory / "summary.json", report)
    return report
