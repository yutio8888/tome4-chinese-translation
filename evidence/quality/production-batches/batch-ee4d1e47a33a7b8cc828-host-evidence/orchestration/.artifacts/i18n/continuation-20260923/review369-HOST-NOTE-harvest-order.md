# Host note: contextual-000 harvest order (batch 369)

Claude Code was upgraded to 2.1.284 during the pause before this batch. `harvest --native-log` for contextual-000 failed with `unsupported Claude version`, because the repository pins `CLAUDE_NATIVE_VERSIONS = ('2.1.259', '2.1.280')`. That harvest attempt and `archive_agent` were issued in the same parallel step, so the agent was archived (06:03:48.671Z) before `archive-intent`.

Recovery used the recorded batch-254 method. `native_extract_v284.py` runs the repository's `_parse_native_final` from a temp copy in which only the whitelist tuple gains `'2.1.284'`, writing `review369-contextual-native/full-000.raw` plus `.proof.json`. `harvest --raw` then passed with output_valid=True. `archive-intent` and `archive-confirm` were recorded after the fact against the same terminal and archive captures. The repository tool is unchanged. Adding 2.1.284 to the whitelist is a separate bounded tool-maintenance task.
