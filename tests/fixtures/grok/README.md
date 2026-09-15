# Grok native fixtures

These are directory-level trims of the two real Grok sessions used by the
native-export probe.  The source directories were:

- `/home/paseo/.grok/sessions/%2Fworkspace%2Ftome4-chinese-translation/01a0a5aa-d667-7e32-a7f1-3059e248dc43`
- `/home/paseo/.grok/sessions/%2Fworkspace%2Ftome4-chinese-translation/01a0a533-505a-7f80-9381-29b7df50148a`

Only `summary.json`, `events.jsonl`, and `chat_history.jsonl` are included.
Those three files are copied byte-for-byte from the source; no user text is
redacted or replaced.  Thus the trim removes only unrelated session sidecar
files, and there is no synthetic content in these fixtures.  If an unrelated
user record is redacted in a future fixture, its content must remain a list of
`{type: "text", text: ...}` blocks.

## Source hashes and mapping

| session | file | source SHA-256 | fixture records |
| --- | --- | --- | --- |
| `01a0a5aa-d667-7e32-a7f1-3059e248dc43` | `summary.json` | `d2da2623dd44b7a20a411ec74dc4eb87d3fdd5824859c34409b3b0d5ce5fe5ef` | complete source file |
|  | `events.jsonl` | `789565b6a2eeed309c7c358106f19088d921d8a1af7583abe6c7c0fc9920f01b` | source lines 1–1631 |
|  | `chat_history.jsonl` | `67651a7a9596e3e0b1fdaf7b7dcaaa9b84074237988c70a9f0a12f2cc49e6791` | source lines 1–62 |
| `01a0a533-505a-7f80-9381-29b7df50148a` | `summary.json` | `4c07249d3eefb2ab6e803933111dbaa40a2982b7207024e861d21b28e26f0dff` | complete source file |
|  | `events.jsonl` | `362d87b85dfc289d7e6abf39bb43c3f7bd6c2bfc3c93736cc17d175f0cc771c8` | source lines 1–2748 |
|  | `chat_history.jsonl` | `276eca3bce61b528f25fda139123f7510454ba8f0de22e2d8a217573a1608734` | source lines 1–91 |

For each session, chat records map one-to-one and in order: system record,
five user records (the `<user_info>` record, host/system notices, the frozen
`<user_query>` record, and the final host notice), then each reasoning /
assistant / tool-result sequence.  The assistant records retain their real
`tool_calls` objects with `id`, `name`, and `arguments`; every call ID remains
paired with its source `tool_result` record.  The last assistant record is the
real final answer and is intentionally unchanged.  Events likewise map
one-to-one and in order, including the MCP bootstrap prefix, the single
`turn_started`, all observed loop/tool/permission events, and the trailing
completed `turn_ended`.

The real final-answer SHA-256 values are:

- `01a0a5aa-d667-7e32-a7f1-3059e248dc43`: `922c643f53d65c98cca10b35e94f1786ffbf3871d7678291f92bc1ddbdf5043e`
- `01a0a533-505a-7f80-9381-29b7df50148a`: `8a9a7881aa6789af9b0b253b57cf7c671d9c943873a930ddcfe4821716093afa`

Synthetic negative fixtures, if needed later, belong under
`tests/fixtures/grok/synthetic/` and must be labeled non-real.
