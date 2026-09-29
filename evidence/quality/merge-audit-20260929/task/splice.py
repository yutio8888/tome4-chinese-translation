"""Entry-level splice of translation targets between Lua locale files.

Indexes every literal t(source, target, tag) call per section, then rebuilds a
develop file with chosen targets copied verbatim (raw literal bytes) from the
branch file, and optionally deletes whole calls.
"""
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
import contextual_anchor_preflight as AP  # noqa: E402


def _literal(text, pos):
    """Return (value, start, end) for the Lua string literal at pos, or None."""
    pos = AP._skip_space_and_comments(text, pos)
    if pos >= len(text):
        return None
    if text[pos] in ('"', "'"):
        value, end = AP._decode_lua_string(text, pos)
        return value, pos, end
    opening = AP._long_bracket_opening(text, pos)
    if opening is None:
        return None
    content_start, closing = opening
    end = text.index(closing, content_start)
    value = text[content_start:end]
    # Lua drops a newline that immediately follows the opening bracket.
    if value.startswith('\r\n'):
        value = value[2:]
    elif value.startswith('\n'):
        value = value[1:]
    return value, pos, end + len(closing)


def _comma(text, pos):
    pos = AP._skip_space_and_comments(text, pos)
    return pos + 1 if pos < len(text) and text[pos] == ',' else None


def index(text):
    """Map (section, source, tag) -> list of call spans."""
    sections, calls = AP._scan_lua(text)
    out = {}
    for call in calls:
        section = None
        for s in sections:
            if s.start < call.start:
                section = s.path
            else:
                break
        paren = AP._skip_space_and_comments(text, call.start + 1)
        a = _literal(text, paren + 1)
        if a is None:
            continue
        c1 = _comma(text, a[2])
        b = _literal(text, c1) if c1 else None
        if b is None:
            continue
        c2 = _comma(text, b[2])
        c = _literal(text, c2) if c2 else None
        if c is None:
            continue
        close = AP._skip_space_and_comments(text, c[2])
        if close < len(text) and text[close] == ',':
            # Optional fourth argument: an args_order table such as {1,2,3,5,4}.
            brace = AP._skip_space_and_comments(text, close + 1)
            if brace >= len(text) or text[brace] != '{':
                continue
            end_brace = text.index('}', brace)
            close = AP._skip_space_and_comments(text, end_brace + 1)
        if close >= len(text) or text[close] != ')':
            continue
        key = (section, a[0], c[0])
        out.setdefault(key, []).append(dict(call_start=call.start, call_end=close + 1,
                                            target=b[0], t_start=b[1], t_end=b[2]))
    return out


def splice(dev_text, br_text, take, delete):
    """take: keys whose target literal is copied from br; delete: keys to remove."""
    di, bi = index(dev_text), index(br_text)
    edits = []
    for key in take:
        assert len(di.get(key, [])) == 1, ('dev occurrences', key[1][:60], len(di.get(key, [])))
        assert len(bi.get(key, [])) == 1, ('branch occurrences', key[1][:60], len(bi.get(key, [])))
        d, b = di[key][0], bi[key][0]
        edits.append((d['t_start'], d['t_end'], br_text[b['t_start']:b['t_end']]))
    for key in delete:
        assert len(di.get(key, [])) == 1, ('dev occurrences for delete', key[1][:60])
        d = di[key][0]
        line_start = dev_text.rfind('\n', 0, d['call_start']) + 1
        line_end = dev_text.find('\n', d['call_end'])
        line_end = len(dev_text) if line_end < 0 else line_end + 1
        assert dev_text[line_start:d['call_start']].strip() == '', 'call not at line start'
        assert dev_text[d['call_end']:line_end].strip() == '', 'trailing code after call'
        edits.append((line_start, line_end, ''))
    edits.sort(key=lambda e: e[0], reverse=True)
    out = dev_text
    last = None
    for start, end, new in edits:
        assert last is None or end <= last, 'overlapping edits'
        out = out[:start] + new + out[end:]
        last = start
    return out


if __name__ == '__main__':
    print('library module; import splice')
