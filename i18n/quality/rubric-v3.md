# MQM pilot v3 rubric (`mqm-pilot-v3`)

The evaluator reports observable semantic deltas; the host owns classification and severity.

- Accuracy covers mistranslation, omission, addition, untranslated content, polarity, conditions,
  numbers/units, and entity roles.
- Terminology covers a demonstrably applicable preferred term, proper name, or inconsistent term.
- `FLU_AMBIGUITY` is allowed only when the Chinese introduces a substantive ambiguity absent from
  the source. `UI_CLARITY` is allowed only when a UI label changes or obscures meaning.
- Use the narrowest compatible phenomenon. Evidence must identify the same semantic scope described
  by the explanation. Do not infer technical failure or actual game mechanics beyond the bundle.
- A clean item has an empty findings array. Insufficient context is not itself a finding; when a
  visible possible defect is still reportable, mark the item `context-insufficient` and describe
  only the observable uncertainty.

The host rejects incompatible error-code/phenomenon/meaning-change combinations. It then applies
deterministic gates, exact human anchors, the severity matrix, and provisional/manual-queue rules.
