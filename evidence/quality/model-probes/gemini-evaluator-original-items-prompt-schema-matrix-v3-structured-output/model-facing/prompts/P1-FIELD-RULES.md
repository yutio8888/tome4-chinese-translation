Review each Chinese translation against its English source. Report only objective meaning or structural problems. Context, when present, is fixed public-source evidence.

Field rules:
- `target_span`: copy a contiguous substring of this item's `target`, character for character.
- `evidence`: copy a contiguous substring of this item's `source`, `target`, or `source_context` when present, character for character; it is a quotation, never explanation, translation, summary, or reasoning.
- `correction`: authored replacement text for `target_span`; it is the only one of these fields not copied.

Worked example (not an experiment item): for source "The cup is red." and target "杯子是蓝色的。", a candidate may use `target_span` "蓝色", `evidence` "red", and `correction` "红色".

Return exactly the registered JSON schema, preserve item order and IDs, and provide no free text or reasoning outside these JSON fields. If no objective candidate exists, return an empty candidates array.
