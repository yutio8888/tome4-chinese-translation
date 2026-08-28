# Translation reviewer task

Review every English source / Chinese target pair for a **material translation defect**.

Material means that the Chinese can change or materially obscure a player's understanding of a mechanic, action, condition, quantity, polarity, target, scope, timing, causality, speaker, referent, or narrative fact. Pure style, fluency, punctuation, or preference differences that preserve substantive meaning are not material.

When `fixed_context` is non-empty, it is public game source surrounding the exact English string. Use it to resolve runtime behavior, referents, branches, and display-string inaccuracies. Actual fixed source behavior may show that the Chinese correctly clarifies an incomplete or inaccurate English display string. Do not invent facts that are absent from both the pair and the supplied context.

For each item, return exactly one verdict:

- `FINDING`: a material translation defect is established.
- `OK`: no material translation defect is established.
- `UNCERTAIN`: the supplied evidence is insufficient or contradictory.

Return all items exactly once, in input order. `material_issue` must briefly state the defect when `FINDING`; for `OK`, briefly state why the meaning is preserved; for `UNCERTAIN`, state what evidence is missing. `evidence` must cite the relevant words or supplied source behavior. Output only the JSON object required by the schema.
